"""SQLite 열기의 공통 골격 — derived(index_db)와 stats가 같은 3줄을 사본으로 들었다.

트랜잭션 계약은 여기서 정하지 않는다 — index_db는 호출자가 `with connection:`으로
빌드를 원자화하고, stats는 자체 contextmanager가 commit·close를 맡는다. 수명이
다른 두 소비자가 공유하는 것은 "열고, Row로 읽고, 스키마를 보장한다"까지다.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def open_db(path: Path, schema: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.executescript(schema)
    return connection
