"""파생 SQLite — frontmatter 메타 테이블 + edges (PLAN §4.1 자체 레그 ②, §4.4-9).

소모품이다. md에서 전량 재생성되므로 백업 대상이 아니고 git에도 들어가지 않는다.
qmd가 frontmatter를 파싱하지 않기 때문에 스코프 질의(type/status/stale_after)와
링크 그래프는 여기서 답한다.

**인덱스를 만들지 않는다.** 10⁴–10⁵행 풀스캔이 0.5–7ms라 주간 배치·CLI에 충분하고,
필요가 실측되면 그때 추가한다(retrofit O(1) — PLAN §4.1·§8).
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from . import morph
from .layout import Layout
from .mdfile import read
from .repo import ROOT, visible_files

DB_PATH = ROOT / "derived.sqlite"
LOCK_PATH = ROOT / "derived.sqlite.lock"
QMD_SCHEME = "qmd://"

SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
  path        TEXT PRIMARY KEY,   -- 저장소 루트 기준
  kb          TEXT NOT NULL,
  directory   TEXT,               -- sources/concepts/synthesis/inbox — 마커 등은 NULL
  type        TEXT NOT NULL,
  status      TEXT,               -- 부재 = stable
  stale_after TEXT,               -- YYYY-MM-DD
  unreviewed  INTEGER NOT NULL,   -- inbox 경로 + verified 부재 (PLAN §3)
  sha256      TEXT NOT NULL,      -- lint 증분 실행의 기준
  frontmatter TEXT NOT NULL       -- 필터 컬럼 외 전부 JSON
);

CREATE TABLE IF NOT EXISTS edges (
  src      TEXT NOT NULL,         -- 저장소 루트 기준
  dst      TEXT NOT NULL,         -- 해결되면 루트 기준 경로, 아니면 원문 href
  kind     TEXT NOT NULL,         -- internal | cross_kb
  anchor   TEXT,                  -- #헤딩 — 앵커 검증은 lint 소관
  resolved INTEGER NOT NULL
);

-- 한국어 형태소 레그. body만 색인하고 나머지는 결과 표시용이다.
-- 섹션 단위로 잘라 넣는 이유: 결과가 파일이 아니라 앵커를 가리켜야
-- "섹션 → 페이지 순 확장"이 된다(PLAN §4.1).
CREATE VIRTUAL TABLE IF NOT EXISTS morph USING fts5(
  path UNINDEXED, anchor UNINDEXED, line UNINDEXED, raw UNINDEXED, body,
  tokenize='unicode61'
);

-- 파편화 관측 → 사용자 사전 후보 큐. lint가 읽는다(PLAN §4.3).
CREATE TABLE IF NOT EXISTS fragments (
  path    TEXT NOT NULL,
  surface TEXT NOT NULL,
  pieces  TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class Counts:
    files: int
    edges: int
    unresolved: int
    sections: int = 0
    fragments: int = 0
    morph: bool = True


@contextmanager
def build_lock():
    """재색인은 단일 실행으로 직렬화한다(PLAN §2.5-7ⓐ). O_EXCL이 게이트다."""
    try:
        handle = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(
            f"재색인이 이미 실행 중입니다 ({LOCK_PATH.name}). 죽은 프로세스가 남긴 것이라면 "
            "파일을 지우고 다시 실행하십시오.") from None
    try:
        os.write(handle, str(os.getpid()).encode())
        os.close(handle)
        yield
    finally:
        LOCK_PATH.unlink(missing_ok=True)


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def _link_target(layout: Layout, src: Path, href: str) -> tuple[str, str, str | None, bool]:
    """링크 하나를 (kind, dst, anchor, resolved)로 푼다. 저장소 밖 링크는 None을 뜻하는 빈 kind."""
    target, _, anchor = href.partition("#")
    anchor = anchor or None

    if href.startswith(QMD_SCHEME):
        dst = target.removeprefix(QMD_SCHEME)
        return "cross_kb", dst, anchor, (ROOT / dst).is_file()
    if "://" in href or not target:
        return "", href, anchor, False
    dst = os.path.normpath(src.parent / target)
    return "internal", dst, anchor, (ROOT / dst).is_file()


def build(layout: Layout) -> Counts:
    """md 전량에서 다시 만든다. 증분이 아닌 이유: 이 규모에서 전량 재생성이 초 단위이고,
    증분은 삭제·이동을 놓치는 실패 모드를 들여온다."""
    files, edges, sections, fragments = [], [], [], []
    with_morph = morph.available()

    for relative in visible_files():
        if relative.suffix != ".md" or relative.parts[0] not in layout.kbs():
            continue

        raw = (ROOT / relative).read_bytes()
        md = read(ROOT / relative, relative)
        front = md.frontmatter or {}
        directory = layout.content_dir_of(relative)

        if with_morph:
            text = raw.decode()
            for title, line, body in morph.sections(text, md):
                if not body.strip():
                    continue
                sections.append((str(relative), morph.anchor(title), line,
                                 body, morph.index_text(body)))
            fragments += [
                (str(relative), fragment.surface, " ".join(fragment.pieces))
                for fragment in morph.fragments(text)
            ]

        files.append((
            str(relative),
            relative.parts[0],
            directory,
            front.get("type", ""),
            front.get("status"),
            front.get("stale_after"),
            int(directory == "inbox" and "verified" not in front),
            hashlib.sha256(raw).hexdigest(),
            json.dumps(front, ensure_ascii=False, sort_keys=True, default=str),
        ))

        for href in md.links:
            kind, dst, anchor, resolved = _link_target(layout, relative, href)
            if kind:   # 저장소 밖(http 등)은 그래프의 간선이 아니다
                edges.append((str(relative), dst, kind, anchor, int(resolved)))

    with connect() as connection:
        for table in ("files", "edges", "morph", "fragments"):
            connection.execute(f"DELETE FROM {table}")
        connection.executemany("INSERT INTO files VALUES (?,?,?,?,?,?,?,?,?)", files)
        connection.executemany("INSERT INTO edges VALUES (?,?,?,?,?)", edges)
        connection.executemany(
            "INSERT INTO morph (path, anchor, line, raw, body) VALUES (?,?,?,?,?)", sections)
        connection.executemany("INSERT INTO fragments VALUES (?,?,?)", fragments)

    return Counts(
        files=len(files),
        edges=len(edges),
        unresolved=sum(1 for edge in edges if not edge[4]),
        sections=len(sections),
        fragments=len(fragments),
        morph=with_morph,
    )


def backlinks(connection: sqlite3.Connection, path: str) -> list[sqlite3.Row]:
    return connection.execute(
        "SELECT src, kind, anchor FROM edges WHERE dst = ? ORDER BY src", (path,)
    ).fetchall()


def neighbors(connection: sqlite3.Connection, path: str, depth: int,
              cross_kb: bool = False) -> list[sqlite3.Row]:
    """k-hop 이웃. 탐색 기본 스코프는 KB 내부이고 상한은 4다(PLAN §4.1).

    상한 근거는 CTE 실측 — 10만 노드 depth-3 1.97ms 대 depth-5 218ms. 방향은 무시한다
    (링크 탐색은 backlink도 따라가는 것이 요점).
    """
    if not 1 <= depth <= 4:
        raise ValueError(f"탐색 깊이는 1–4입니다 (요청: {depth}) — PLAN §4.1 상한")

    scope = "" if cross_kb else "AND e.kind = 'internal'"
    return connection.execute(f"""
        WITH RECURSIVE walk(path, hops) AS (
            SELECT ?, 0
            UNION
            SELECT CASE WHEN e.src = w.path THEN e.dst ELSE e.src END, w.hops + 1
            FROM edges e JOIN walk w ON (e.src = w.path OR e.dst = w.path)
            WHERE w.hops < ? AND e.resolved = 1 {scope}
        )
        SELECT path, MIN(hops) AS hops FROM walk
        WHERE hops > 0 GROUP BY path ORDER BY hops, path
    """, (path, depth)).fetchall()
