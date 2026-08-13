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
from datetime import datetime, timezone
from pathlib import Path

from . import morph
from .db import open_db
from .layout import QMD_SCHEME, Layout
from .mdfile import anchors_by_line, read
from .repo import ROOT, visible_files
from .workspace import DEFAULT, Workspace

# 경로 파생의 정본은 Workspace다 — 전역은 기본 인스턴스의 파생물(하위 호환).
DB_PATH = DEFAULT.derived_db
LOCK_PATH = DEFAULT.derived_lock

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

-- 세대 스탬프 — 빌드 시점 입력의 지문(fingerprint)·시각. 소비자가 staleness로
-- 대조한다: 낡은 색인의 조용한 소비가 증분 누락과 FileNotFoundError 크래시를
-- 만들었다(2026-08-13 감사 B4).
CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
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
def build_lock(ws: Workspace | None = None):
    """재색인은 단일 실행으로 직렬화한다(PLAN §2.5-7ⓐ). O_EXCL이 게이트다."""
    lock = (ws or DEFAULT).derived_lock
    try:
        handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(
            f"재색인이 이미 실행 중입니다 ({lock.name}). 죽은 프로세스가 남긴 것이라면 "
            "파일을 지우고 다시 실행하십시오.") from None
    try:
        os.write(handle, str(os.getpid()).encode())
        os.close(handle)
        yield
    finally:
        lock.unlink(missing_ok=True)


def connect(ws: Workspace | None = None) -> sqlite3.Connection:
    """파생 DB 연결 — 주입 가능(retrieval_eval의 벤치 루트가 소비자). 주입이 생기기
    전에는 호출자가 모듈 전역 DB_PATH를 멍키패치했다(2026-08-13 감사)."""
    return open_db((ws or DEFAULT).derived_db, SCHEMA)


def tree_fingerprint(kbs: tuple[str, ...]) -> str:
    """색인이 의존하는 입력의 상태 지문 — stat(mtime·size) 기반.

    범위는 **색인의 실제 입력만**이다: KB 내부 md + schema/. 전체 md로 잡았던
    초판은 색인에 들지 않는 문서(.agents 리뷰 등)의 커밋마다 불필요한 재색인을
    강요했다(2026-08-13 실기 발견 — 게이트 도입 당일 첫 오탐).

    내용 해시가 아닌 이유: 소비 시점마다 전량 재해시는 O(N 바이트)라 조회 도구의
    상수 비용이 되고, mtime 오탐(내용 같은데 touch)의 비용은 재색인 권고 한 번이라
    수용 가능하다. git(HEAD+status) 기반이 아닌 이유: md와 무관한 커밋·미추적
    파일이 지문을 흔든다.
    """
    lines = []
    for relative in visible_files():
        indexed = relative.suffix == ".md" and relative.parts[0] in kbs
        if not indexed and relative.parts[0] != "schema":
            continue
        stat = (ROOT / relative).stat()
        lines.append(f"{relative}\t{stat.st_mtime_ns}\t{stat.st_size}")
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()


def staleness(connection: sqlite3.Connection, kbs: tuple[str, ...]) -> str | None:
    """색인이 워킹 트리보다 낡았으면 사유, 최신이면 None — 소비 전에 반드시 묻는다.

    낡은 색인의 조용한 소비가 만든 실패 둘이 근거다: 증분 lint가 실변경 페이지를
    건너뛰고, 지워진 파일이 색인에 남아 read()가 traceback으로 죽는다(감사 B4).
    """
    row = connection.execute("SELECT value FROM meta WHERE key = 'fingerprint'").fetchone()
    if row is None:
        return "세대 스탬프가 없습니다(스탬프 도입 전 색인)"
    if row["value"] != tree_fingerprint(kbs):
        return "색인 이후 워킹 트리가 변했습니다"
    return None


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
    kbs = layout.kbs()          # 연산당 1회 — 루프 안 kbs()는 파일당 git 서브프로세스다
    # 지문은 읽기 **시작 전에** 뜬다 — 빌드 중 파일이 변하면 다음 staleness가
    # 보수적으로(낡음 쪽으로) 판정하게 되는 방향이 안전하다.
    fingerprint = tree_fingerprint(kbs)

    for relative in visible_files():
        if relative.suffix != ".md" or relative.parts[0] not in kbs:
            continue

        raw = (ROOT / relative).read_bytes()
        md = read(ROOT / relative, relative)
        front = md.frontmatter or {}
        directory = layout.content_dir_of(relative, kbs)

        if with_morph:
            text = raw.decode()
            # 앵커는 페이지 전체 헤딩 순서로 계산한다(중복 `-n` 순번이 전체 기준) —
            # 검사(checks/page)와 같은 mdfile 단일 구현을 쓴다.
            anchors = anchors_by_line(md.headings)
            # raw는 사람이 볼 스니펫(코드 포함), prose는 색인 대상(코드 제외) — morph.sections 참조
            for title, line, section_raw, prose in morph.sections(text, md):
                if not section_raw.strip():
                    continue
                sections.append((str(relative), anchors.get(line), line,
                                 section_raw, morph.index_text(prose)))
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

    # INSERT는 컬럼을 명명한다 — 위치 기반은 스키마 컬럼 순서에 암묵 결합돼
    # 순서 변경이 조용한 어긋남이 된다(2026-08-13 감사).
    with connect() as connection:
        for table in ("files", "edges", "morph", "fragments", "meta"):
            connection.execute(f"DELETE FROM {table}")
        connection.executemany(
            "INSERT INTO meta (key, value) VALUES (?,?)",
            [("fingerprint", fingerprint),
             ("built_at", datetime.now(timezone.utc).isoformat())])
        connection.executemany(
            "INSERT INTO files (path, kb, directory, type, status, stale_after, "
            "unreviewed, sha256, frontmatter) VALUES (?,?,?,?,?,?,?,?,?)", files)
        connection.executemany(
            "INSERT INTO edges (src, dst, kind, anchor, resolved) VALUES (?,?,?,?,?)", edges)
        connection.executemany(
            "INSERT INTO morph (path, anchor, line, raw, body) VALUES (?,?,?,?,?)", sections)
        connection.executemany(
            "INSERT INTO fragments (path, surface, pieces) VALUES (?,?,?)", fragments)

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


def degrees(connection: sqlite3.Connection, direction: str = "in",
            kb: str | None = None, top: int | None = None) -> list[sqlite3.Row]:
    """링크 차수 — 'in'=피링크(dst, 허브 후보), 'out'=발링크(src, 허브 크기). resolved만.

    edges 질의는 이 모듈이 소유한다(backlinks·neighbors와 같은 자리) — CLI(edges)와
    그래프 검사(checks/graph)가 같은 SQL의 사본 셋을 들고 있었다(2026-08-13 감사).
    """
    column = {"in": "dst", "out": "src"}[direction]
    return connection.execute(f"""
        SELECT {column} AS path, COUNT(*) AS degree FROM edges
        WHERE resolved = 1 AND (:kb IS NULL OR {column} LIKE :kb || '/%')
        GROUP BY {column} ORDER BY degree DESC, path LIMIT :top
    """, {"kb": kb, "top": -1 if top is None else top}).fetchall()


# 가중 탐색의 잡음 하한. 경로 가중이 이 아래로 떨어지면 확장을 멈춘다 —
# 평균 분기 ~5.6의 4-hop 체인(1/5.6⁴ ≈ 0.001)까지 생존하고, 그 너머는 근접
# 신호가 아니라 잡음이다. 깊이 상한 4와 같은 계보의 운영 상수이며, 부수 효과로
# 고차수 노드 경유의 행 폭발도 이 하한이 막는다.
WEIGHT_FLOOR = 0.001


def neighbors(connection: sqlite3.Connection, path: str, depth: int,
              cross_kb: bool = False) -> list[sqlite3.Row]:
    """k-hop 이웃 — **차수 가중**. 탐색 기본 스코프는 KB 내부, 상한 4(PLAN §4.1).

    가중 = 경유 노드 분기 수의 역수 곱(무방향 random walk 확률). 이것이 없으면
    고차수 노드(허브)가 만능 지름길이 되어 300링크 허브 하나로 KB 전체가 2-hop
    이내가 된다(실측: 개념 1개의 2-hop 이웃 = 301건 = 전 KB). 링크가 큐레이션된
    선별일 때만 "가까움"이 신호라는 전제를, 사람 규율이 아니라 질의가 강제한다.
    HippoRAG의 Personalized PageRank와 같은 계보다(PLAN §8이 인용한 메커니즘).

    고차수 노드 자체는 이웃으로 **돌아온다**(도달점) — 경유(transit)만 강등된다.
    깊이 상한 근거는 CTE 실측 — 10만 노드 depth-3 1.97ms 대 depth-5 218ms.
    방향은 무시한다(링크 탐색은 backlink도 따라가는 것이 요점).
    """
    if not 1 <= depth <= 4:
        raise ValueError(f"탐색 깊이는 1–4입니다 (요청: {depth}) — PLAN §4.1 상한")

    scope = "" if cross_kb else "AND e.kind = 'internal'"
    return connection.execute(f"""
        WITH RECURSIVE
        deg(node, branches) AS (
            SELECT node, COUNT(*) FROM (
                SELECT src AS node FROM edges WHERE resolved = 1
                UNION ALL
                SELECT dst FROM edges WHERE resolved = 1
            ) GROUP BY node
        ),
        walk(path, hops, weight) AS (
            SELECT ?, 0, 1.0
            UNION
            SELECT CASE WHEN e.src = w.path THEN e.dst ELSE e.src END,
                   w.hops + 1,
                   w.weight / (SELECT branches FROM deg WHERE node = w.path)
            FROM edges e JOIN walk w ON (e.src = w.path OR e.dst = w.path)
            WHERE w.hops < ? AND e.resolved = 1 {scope}
              AND w.weight / (SELECT branches FROM deg WHERE node = w.path) >= {WEIGHT_FLOOR}
        )
        SELECT path, MIN(hops) AS hops, MAX(weight) AS weight FROM walk
        WHERE hops > 0 AND path != ?
        GROUP BY path ORDER BY weight DESC, hops, path
    """, (path, depth, path)).fetchall()
