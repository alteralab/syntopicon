#!/usr/bin/env python3
"""Claude Code 세션을 Langfuse 트레이스로 — 도구 편승 스캔 업로더.

관측 배선의 층 2다(층 1 = stats.sqlite events — 결정 루프는 로컬에 닫는다).

**기전이 훅도 스케줄러도 아닌 이유**: SessionEnd 훅과 launchd는 둘 다 기기 수준
대역외 등록물이라 생존을 워크플로의 무엇도 보장하지 않는다 — 새 기기에서 잊히고
죽어도 모른다(search_miss가 앓던 병). 이 저장소에서 계측이 살아남은 유일한
패턴은 "어차피 도는 도구에 얹기"이고, 전송도 같은 원리를 따른다:

    search·promote 실행 끝 → nudge() → 마지막 동기화가 24시간 이전이면
    분리 백그라운드 프로세스로 이 파일을 --scan 실행 → 전사 디렉터리에서
    최근 세션을 걷어 일괄 업로드.

주기 = 활동이다. KB를 쓰는 날에만 돌고, 크래시로 끝난 세션도 스캔이 수거하며,
새 기기는 git clone만으로 복원된다(등록물 없음). 재심 트리거: Claude Code의
OTel traces(베타)가 GA되고 스팬 내용의 제외 통제가 확인되면 이 파일을 지우고
설정(otelHeadersHelper)만 남긴다.

원칙 셋(전송 계층 공통):
- **내용 제외.** 프롬프트·응답·도구 입출력은 보내지 않는다 — 도구 호출 횟수,
  스킬 이름, 토큰·모델·소요·cwd뿐. KB 내용은 집을 떠나지 않는다.
- **본 작업을 막지 않는다.** nudge는 발사 후 대기하지 않고, 모든 실패는 로그
  파일로 가며 종료 코드는 0이다. 죽은 계측의 검출은 로그와 Langfuse 쪽 공백이
  담당한다.
- **멱등.** trace id = session id라 재스캔·중복 실행은 갱신일 뿐이다.

비밀은 gopass 3키(langfuse/secret-key·public-key·host)에서 실행 시점에 꺼낸다.
저장소 venv 밖(시스템 python3)에서도 돌 수 있게 stdlib만, 3.9 문법으로 쓴다.

    python3 tools/langfuse_bridge.py            # 수동 스캔 (상태 파일 기준)
    python3 tools/langfuse_bridge.py --since-days 14
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
LOG_PATH = CLAUDE_DIR / "langfuse-bridge.log"
STATE_PATH = CLAUDE_DIR / "langfuse-bridge.state"   # 마지막 성공 동기화 (ISO)
LOCK_PATH = CLAUDE_DIR / "langfuse-bridge.lock"

TIMEOUT = 15
SYNC_INTERVAL_S = 24 * 3600      # nudge 스로틀 — 하루 한 배치면 진단 창에 충분하다
SCAN_MARGIN_S = 3600             # 직전 동기화 시각의 경계 유실 방지 — 멱등이라 무해
FALLBACK_DAYS = 7                # 상태 파일이 없을 때의 초기 스캔 창
LOCK_STALE_S = 3600
CHUNK = 50                       # ingestion 배치 상한(3.5MB)에 넉넉한 안전 계수


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


# ── 요약과 조립 (내용 제외 계약은 여기서 지켜진다) ───────────────────────────

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
    cwd = None
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
            if entry.get("cwd"):
                cwd = entry["cwd"]

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
        "cwd": cwd,
        "first_at": min(timestamps) if timestamps else None,
        "last_at": max(timestamps) if timestamps else None,
        "parse_errors": parse_errors,
    }


def trace_event(session_id: str, summary: dict) -> dict:
    """trace-create 한 건 — 세션당 1유닛이라 Hobby 한도(월 50k)에 넉넉하다."""
    now = datetime.now(timezone.utc).isoformat()
    cwd = summary.get("cwd") or ""
    return {
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
                "ended_at": summary["last_at"],
                "models": summary["models"],
                "tokens": summary["tokens"],
                "tools": summary["tools"],
                "skills": summary["skills"],
                "entry_types": summary["entry_types"],
                "parse_errors": summary["parse_errors"],
            },
        },
    }


def send(host: str, public_key: str, secret_key: str, events: list) -> None:
    token = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    request = urllib.request.Request(
        f"{host.rstrip('/')}/api/public/ingestion",
        data=json.dumps({"batch": events}).encode(),
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


# ── 스캔과 편승 ──────────────────────────────────────────────────────────────

def stale(state_text: "str | None", now_ts: float) -> bool:
    """동기화가 필요한가. 상태가 없거나 못 읽으면 필요한 쪽으로 판정한다."""
    if not state_text:
        return True
    try:
        last = datetime.fromisoformat(state_text.strip()).timestamp()
    except ValueError:
        return True
    return now_ts - last >= SYNC_INTERVAL_S


def sessions_since(projects_dir: Path, since_ts: float) -> list:
    """mtime이 경계 이후인 세션 전사 전부. 파일명(uuid) = session id다."""
    found = []
    if not projects_dir.is_dir():
        return found
    for project in projects_dir.iterdir():
        if not project.is_dir():
            continue
        for transcript in project.glob("*.jsonl"):
            if transcript.stat().st_mtime >= since_ts:
                found.append(transcript)
    return sorted(found, key=lambda p: p.stat().st_mtime)


def acquire_lock() -> bool:
    try:
        os.close(os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        try:
            if time.time() - LOCK_PATH.stat().st_mtime > LOCK_STALE_S:
                LOCK_PATH.unlink()
                return acquire_lock()
        except FileNotFoundError:
            return acquire_lock()
        return False


def scan(since_days: "int | None" = None) -> int:
    if not acquire_lock():
        log("스캔 중복 — 다른 스캐너가 실행 중이라 건너뜀")
        return 0
    try:
        now_ts = time.time()
        if since_days is not None:
            since = now_ts - since_days * 86400
        elif STATE_PATH.is_file():
            state = STATE_PATH.read_text().strip()
            try:
                since = datetime.fromisoformat(state).timestamp() - SCAN_MARGIN_S
            except ValueError:
                since = now_ts - FALLBACK_DAYS * 86400
        else:
            since = now_ts - FALLBACK_DAYS * 86400

        transcripts = sessions_since(PROJECTS_DIR, since)
        if not transcripts:
            STATE_PATH.write_text(datetime.now(timezone.utc).isoformat() + "\n")
            print("동기화할 세션이 없습니다.")
            return 0

        host = gopass("langfuse/host")
        public_key = gopass("langfuse/public-key")
        secret_key = gopass("langfuse/secret-key")

        events, failures = [], 0
        for transcript in transcripts:
            try:
                events.append(trace_event(transcript.stem, summarize(transcript)))
            except Exception as error:                          # noqa: BLE001
                failures += 1
                log(f"요약 실패 {transcript.name}: {type(error).__name__}: {error}")
        for start in range(0, len(events), CHUNK):
            try:
                send(host, public_key, secret_key, events[start:start + CHUNK])
            except Exception as error:                          # noqa: BLE001
                failures += len(events[start:start + CHUNK])
                log(f"전송 실패: {type(error).__name__}: {error}")

        if failures == 0:
            # 상태는 무실패일 때만 전진한다 — 실패분은 다음 스캔이 다시 걷고,
            # 멱등이라 성공분의 재전송은 갱신일 뿐이다.
            STATE_PATH.write_text(datetime.now(timezone.utc).isoformat() + "\n")
        summary_line = f"세션 {len(events)}건 동기화, 실패 {failures}건"
        log(summary_line)
        print(summary_line)
        return 0
    finally:
        LOCK_PATH.unlink(missing_ok=True)


def nudge() -> None:
    """도구 편승 지점 — search·promote가 실행 끝에 부른다. 절대 본 작업을 막지 않는다.

    값싼 상태 확인 하나로 하루 한 번만 스캐너를 분리 발사한다. 발사 후 대기하지
    않으므로 도구 지연은 0이고, 스캐너 쪽 락이 동시 발사를 걸러 낸다.
    """
    try:
        if os.environ.get("SYNTOPICON_ROOT"):
            # 테스트 seam(repo.py) 아래다 — 픽스처 실행이 실계정 전송을 발사하면 안 된다.
            return
        state = STATE_PATH.read_text() if STATE_PATH.is_file() else None
        if not stale(state, time.time()):
            return
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve())],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as error:                                  # noqa: BLE001
        try:
            log(f"nudge 실패: {type(error).__name__}: {error}")
        except OSError:
            pass


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(description="세션 전사 스캔 → Langfuse 업로드")
    parser.add_argument("--since-days", type=int, default=None,
                        help="상태 파일 대신 최근 N일을 스캔한다")
    args = parser.parse_args(argv)
    try:
        return scan(args.since_days)
    except Exception as error:                                  # noqa: BLE001
        log(f"스캔 실패: {type(error).__name__}: {error}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
