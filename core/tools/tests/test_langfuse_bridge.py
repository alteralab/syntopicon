"""세션 브리지. 핵심은 셋 — **내용 제외 계약**(전사의 프롬프트·도구 입출력이
페이로드에 새지 않는다), 스캔 경계, 편승 스로틀 판정. 전송(네트워크)은 테스트하지
않는다."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import langfuse_bridge as bridge

SECRET_PROMPT = "카프카 복제 지연의 비밀 노트"
SECRET_COMMAND = "cat ~/.ssh/id_ed25519"


def transcript(tmp_path: Path) -> Path:
    lines = [
        {"type": "user", "timestamp": "2026-08-13T01:00:00Z",
         # ast-grep-ignore: machine-absolute-path — 시험 자료: 실재하지 않는 가짜 경로 값
         "cwd": "/Users/x/workspace/syntopicon",
         "message": {"content": SECRET_PROMPT}},
        {"type": "assistant", "timestamp": "2026-08-13T01:00:05Z",
         "message": {"model": "claude-fable-5",
                     "usage": {"input_tokens": 100, "output_tokens": 40,
                               "cache_read_input_tokens": 900},
                     "content": [
                         {"type": "tool_use", "name": "Bash",
                          "input": {"command": SECRET_COMMAND}},
                         {"type": "tool_use", "name": "Skill",
                          "input": {"skill": "kb-query"}},
                     ]}},
        {"type": "assistant", "timestamp": "2026-08-13T01:02:00Z",
         "message": {"model": "claude-fable-5",
                     "usage": {"input_tokens": 50, "output_tokens": 10},
                     "content": [{"type": "tool_use", "name": "Bash",
                                  "input": {"command": "ls"}}]}},
    ]
    path = tmp_path / "transcript.jsonl"
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n깨진 줄\n")
    return path


def test_요약은_메타데이터만_담는다(tmp_path: Path):
    summary = bridge.summarize(transcript(tmp_path))
    assert summary["tools"] == {"Bash": 2, "Skill": 1}
    assert summary["skills"] == ["kb-query"]
    assert summary["tokens"] == {"input": 150, "output": 50,
                                 "cache_read": 900, "cache_creation": 0}
    assert summary["models"] == ["claude-fable-5"]
    # ast-grep-ignore: machine-absolute-path — 시험 자료: 실재하지 않는 가짜 경로 값을 대조한다
    assert summary["cwd"] == "/Users/x/workspace/syntopicon"
    assert summary["first_at"] == "2026-08-13T01:00:00Z"
    assert summary["last_at"] == "2026-08-13T01:02:00Z"
    assert summary["parse_errors"] == 1          # 깨진 줄은 계수로 드러난다


def test_페이로드에_내용이_새지_않는다(tmp_path: Path):
    summary = bridge.summarize(transcript(tmp_path))
    event = bridge.trace_event("session-1", summary)
    raw = json.dumps({"batch": [event]}, ensure_ascii=False)
    assert SECRET_PROMPT not in raw
    assert SECRET_COMMAND not in raw and "id_ed25519" not in raw

    body = event["body"]
    assert event["type"] == "trace-create"
    assert body["id"] == "session-1" == body["sessionId"]   # 멱등 — 재전송은 갱신
    assert body["metadata"]["tools"] == {"Bash": 2, "Skill": 1}
    assert "syntopicon" in body["tags"]


def test_스로틀_판정(tmp_path: Path):
    now = datetime.now(timezone.utc)
    assert bridge.stale(None, now.timestamp())                       # 상태 없음
    assert bridge.stale("깨진 값", now.timestamp())                   # 못 읽으면 동기화 쪽
    assert bridge.stale(
        datetime.fromtimestamp(now.timestamp() - 2 * 86400,
                               tz=timezone.utc).isoformat(), now.timestamp())
    assert not bridge.stale(now.isoformat(), now.timestamp())        # 방금 동기화함


def test_스캔은_경계_이후_전사만_고른다(tmp_path: Path):
    projects = tmp_path / "projects"
    old = projects / "proj-a" / "old-session.jsonl"
    new = projects / "proj-b" / "new-session.jsonl"
    for path in (old, new):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n")
    boundary = 1_700_000_000
    os.utime(old, (boundary - 100, boundary - 100))
    os.utime(new, (boundary + 100, boundary + 100))

    found = bridge.sessions_since(projects, boundary)
    assert [p.stem for p in found] == ["new-session"]
    assert bridge.sessions_since(tmp_path / "없는곳", boundary) == []
