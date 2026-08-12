"""텔레메트리 — git 밖의 로컬 stats DB (PLAN §3·§2.5-7ⓑ).

파생 인덱스(derived.sqlite)와 다른 파일인 이유: 저쪽은 md에서 언제든 재생성되는
소모품이고, 이쪽은 재생성되지 않는 누적 기록이다. 수명 주기가 다르면 파일도 다르다.
소실은 허용된다 — 백업 대상이 아니고 git에도 들어가지 않는다.

소비자: lint의 증분 실행 기준, 운영 임계 경보(tripwire), 재검토 큐.
"""

from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from .repo import ROOT

DB_PATH = ROOT / "stats.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS lint_runs (
  id       INTEGER PRIMARY KEY,
  at       TEXT NOT NULL,
  mode     TEXT NOT NULL,        -- full | incremental
  errors   INTEGER NOT NULL,
  warnings INTEGER NOT NULL,
  infos    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS lint_findings (
  run_id     INTEGER NOT NULL,
  check_name TEXT NOT NULL,
  severity   TEXT NOT NULL,
  kb         TEXT,
  path       TEXT,
  message    TEXT NOT NULL
);

-- lint 증분 실행의 기준선: 직전 실행이 무엇을 봤는지.
CREATE TABLE IF NOT EXISTS lint_seen (
  path   TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL,
  at     TEXT NOT NULL
);

-- kb-query가 공백을 만났을 때 남기는 이벤트 (PLAN §4.3 kb-query ④).
-- 기록자는 tools/search.py다 — 스킬 산문이 기록을 지시하던 시절 0건이 쌓였다
-- (225런 대조 실측, 2026-08-13): 계측은 도구가 자동으로 남길 때만 산다.
CREATE TABLE IF NOT EXISTS search_miss (
  at    TEXT NOT NULL,
  kb    TEXT,
  query TEXT NOT NULL
);

-- 파이프라인 이벤트 원장 — 질의·승급 런의 자동 계측 (append-only).
-- payload 스키마는 기록자(도구)가 소유한다. 소비자: 임계 경보·운영 리뷰.
-- session은 상관관계 키다 — 세션 추적(Langfuse 훅 브리지)과 조인할 때 쓴다.
CREATE TABLE IF NOT EXISTS events (
  at      TEXT NOT NULL,
  kind    TEXT NOT NULL,    -- query | promote
  session TEXT,
  payload TEXT NOT NULL     -- JSON
);
"""


@contextmanager
def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_event(connection: sqlite3.Connection, kind: str, payload: dict) -> None:
    """이벤트 한 건을 원장에 남긴다. 세션 ID는 환경에 있으면 자동으로 붙는다.

    실패해도 본 작업을 막지 않는 것은 **호출자가 정할 일이 아니다** — 여기는
    기록만 하고, 기록 실패는 예외로 드러낸다(조용한 생략 금지, PLAN §3).
    """
    connection.execute(
        "INSERT INTO events VALUES (?,?,?,?)",
        (now(), kind, os.environ.get("CLAUDE_SESSION_ID"),
         json.dumps(payload, ensure_ascii=False, sort_keys=True)),
    )


def baseline(connection: sqlite3.Connection) -> dict[str, str]:
    """직전 실행이 본 (경로 → sha256). 증분 실행이 바뀐 페이지만 고르는 데 쓴다."""
    return {row["path"]: row["sha256"]
            for row in connection.execute("SELECT path, sha256 FROM lint_seen")}


def record_run(connection: sqlite3.Connection, mode: str, findings, seen: dict[str, str]) -> int:
    counts = {level: sum(1 for f in findings if f.severity == level)
              for level in ("error", "warn", "info")}
    cursor = connection.execute(
        "INSERT INTO lint_runs (at, mode, errors, warnings, infos) VALUES (?,?,?,?,?)",
        (now(), mode, counts["error"], counts["warn"], counts["info"]),
    )
    run_id = cursor.lastrowid
    connection.executemany(
        "INSERT INTO lint_findings VALUES (?,?,?,?,?,?)",
        [(run_id, f.check, f.severity, f.kb, f.path, f.message) for f in findings],
    )
    connection.executemany(
        "INSERT INTO lint_seen VALUES (?,?,?) "
        "ON CONFLICT(path) DO UPDATE SET sha256 = excluded.sha256, at = excluded.at",
        [(path, sha, now()) for path, sha in seen.items()],
    )
    return run_id
