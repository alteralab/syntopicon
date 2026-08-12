"""세션 브리지. 핵심은 **내용 제외 계약** — 전사에 든 프롬프트·도구 입출력이
페이로드에 새지 않는지를 본다. 전송(네트워크)은 테스트하지 않는다."""

from __future__ import annotations

import json
from pathlib import Path

import langfuse_bridge as bridge

SECRET_PROMPT = "카프카 복제 지연의 비밀 노트"
SECRET_COMMAND = "cat ~/.ssh/id_ed25519"


def transcript(tmp_path: Path) -> Path:
    lines = [
        {"type": "user", "timestamp": "2026-08-13T01:00:00Z",
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
    assert summary["first_at"] == "2026-08-13T01:00:00Z"
    assert summary["last_at"] == "2026-08-13T01:02:00Z"
    assert summary["parse_errors"] == 1          # 깨진 줄은 계수로 드러난다


def test_페이로드에_내용이_새지_않는다(tmp_path: Path):
    summary = bridge.summarize(transcript(tmp_path))
    batch = bridge.build_batch("session-1", "/Users/x/workspace/syntopicon",
                               "clear", summary)
    raw = json.dumps(batch, ensure_ascii=False)
    assert SECRET_PROMPT not in raw
    assert SECRET_COMMAND not in raw and "id_ed25519" not in raw

    body = batch["batch"][0]["body"]
    assert batch["batch"][0]["type"] == "trace-create"
    assert body["id"] == "session-1" == body["sessionId"]   # 멱등 — 재전송은 갱신
    assert body["metadata"]["tools"] == {"Bash": 2, "Skill": 1}
    assert "syntopicon" in body["tags"]
