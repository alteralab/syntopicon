#!/usr/bin/env python3
"""Claude Code 세션을 Langfuse 트레이스로 보내는 SessionEnd 훅 브리지.

관측 배선의 층 2다(층 1 = stats.sqlite events — 결정 루프는 로컬에 닫는다).
Claude Code의 OTel 내보내기는 logs·metrics인데 Langfuse OTLP 수신은 traces
전용이라 직결이 안 된다(2026-08-13 확인) — 그래서 공식 권장 패턴대로 훅에서
세션 요약을 ingestion API로 보낸다. OTel traces가 베타를 벗고 직결되면 이
파일을 지우는 것이 재심 트리거다.

원칙 셋:
- **내용 제외.** 프롬프트·응답·도구 입출력은 보내지 않는다. 보내는 것은 도구
  호출 횟수, 호출한 스킬 이름, 토큰·모델·소요뿐이다 — KB 내용은 집을 떠나지
  않는다.
- **세션을 막지 않는다.** 계측 실패는 본 작업의 실패가 아니다 — 모든 오류는
  로그 파일에 남기고 종료 코드 0으로 끝낸다(Tencent metric-tracking과 같은
  규율). 죽은 계측의 검출은 로그 파일과 Langfuse 쪽 공백이 담당한다.
- **멱등.** trace id = session id라 같은 세션이 다시 끝나도(재개 후 종료)
  같은 트레이스가 갱신될 뿐 중복이 쌓이지 않는다.

비밀은 gopass 3키(langfuse/secret-key·public-key·host)에서 실행 시점에 꺼낸다
— .env 사본을 만들지 않는다(금고 규약: 기계 소비자는 exec 주입만).

이 파일은 저장소 venv 밖(시스템 python3, 훅 컨텍스트)에서 돌므로 stdlib만 쓰고
3.9 문법으로 맞춘다 — tools/의 다른 도구와 요구 파이썬이 다른 유일한 예외다.

수동 실행(스모크): echo '{"session_id":"...","transcript_path":"..."}' | python3 tools/langfuse_bridge.py
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path.home() / ".claude" / "langfuse-bridge.log"
TIMEOUT = 15


def log(message: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp} {message}\n")


def gopass(name: str) -> str:
    proc = subprocess.run(["gopass", "show", "-o", name],
                          capture_output=True, text=True, timeout=TIMEOUT)
    if proc.returncode != 0:
        raise RuntimeError(f"gopass show {name} 실패: {proc.stderr.strip()[:200]}")
    return proc.stdout.strip()


def summarize(transcript_path: Path) -> dict:
    """전사 JSONL에서 **메타데이터만** 접는다 — 내용 필드는 읽되 밖으로 내지 않는다.

    전사 형식은 Claude Code 소유의 외부 형식이라, 모르는 항목 타입은 세기만
    하고 지나간다(우리 스키마가 아닌 것의 선별은 침묵 생략이 아니다). JSON으로
    안 읽히는 줄은 parse_errors로 계수해 드러낸다.
    """
    tools: dict = {}
    skills: list = []
    tokens = {"input": 0, "output": 0, "cache_read": 0, "cache_creation": 0}
    models: set = set()
    entry_types: dict = {}
    timestamps: list = []
    parse_errors = 0

    with transcript_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            kind = entry.get("type", "?")
            entry_types[kind] = entry_types.get(kind, 0) + 1
            if entry.get("timestamp"):
                timestamps.append(entry["timestamp"])

            message = entry.get("message") or {}
            usage = message.get("usage") or {}
            tokens["input"] += usage.get("input_tokens", 0) or 0
            tokens["output"] += usage.get("output_tokens", 0) or 0
            tokens["cache_read"] += usage.get("cache_read_input_tokens", 0) or 0
            tokens["cache_creation"] += usage.get("cache_creation_input_tokens", 0) or 0
            if message.get("model"):
                models.add(message["model"])

            content = message.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name", "?")
                        tools[name] = tools.get(name, 0) + 1
                        if name == "Skill":
                            skill = (block.get("input") or {}).get("skill")
                            if skill and skill not in skills:
                                skills.append(skill)

    return {
        "tools": tools, "skills": skills, "tokens": tokens,
        "models": sorted(models), "entry_types": entry_types,
        "first_at": min(timestamps) if timestamps else None,
        "last_at": max(timestamps) if timestamps else None,
        "parse_errors": parse_errors,
    }


def build_batch(session_id: str, cwd: str, reason: str, summary: dict) -> dict:
    """trace-create 한 건 — 세션당 1유닛이라 Hobby 한도(월 50k)에 넉넉하다."""
    now = datetime.now(timezone.utc).isoformat()
    return {"batch": [{
        "id": str(uuid.uuid4()),
        "type": "trace-create",
        "timestamp": now,
        "body": {
            "id": session_id,
            "name": "claude-code-session",
            "timestamp": summary["first_at"] or now,
            "sessionId": session_id,
            "environment": "claude-code",
            "tags": ["claude-code", Path(cwd).name if cwd else "unknown"],
            "metadata": {
                "cwd": cwd,
                "end_reason": reason,
                "ended_at": summary["last_at"],
                "models": summary["models"],
                "tokens": summary["tokens"],
                "tools": summary["tools"],
                "skills": summary["skills"],
                "entry_types": summary["entry_types"],
                "parse_errors": summary["parse_errors"],
            },
        },
    }]}


def send(host: str, public_key: str, secret_key: str, batch: dict) -> None:
    token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    request = urllib.request.Request(
        f"{host.rstrip('/')}/api/public/ingestion",
        data=json.dumps(batch).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Basic {token}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        if response.status not in (200, 207):
            raise RuntimeError(f"ingestion 응답 {response.status}")
        body = json.loads(response.read() or b"{}")
        if body.get("errors"):
            raise RuntimeError(f"ingestion 부분 실패: {body['errors'][:1]}")


def main() -> int:
    try:
        hook = json.loads(sys.stdin.read() or "{}")
        session_id = hook.get("session_id")
        transcript = hook.get("transcript_path")
        if not session_id or not transcript or not Path(transcript).is_file():
            log(f"입력 불충분 — session={session_id!r} transcript={transcript!r}")
            return 0

        summary = summarize(Path(transcript))
        batch = build_batch(session_id, hook.get("cwd", ""),
                            hook.get("reason", ""), summary)
        send(gopass("langfuse/host"), gopass("langfuse/public-key"),
             gopass("langfuse/secret-key"), batch)
    except Exception as error:                                  # noqa: BLE001
        # 계측은 세션을 막지 않는다 — 실패는 여기 로그가 유일한 흔적이다.
        log(f"전송 실패: {type(error).__name__}: {error}")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
