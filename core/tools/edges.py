#!/usr/bin/env python3
"""링크 그래프 조회 — backlinks / neighbors / 링크 차수 (PLAN §4.1).

그래프 인프라는 불채택이고 그래프 **질의**만 채택했다. 큐레이션된 링크 위의
SQLite edges + 재귀 CTE면 충분하다는 것이 결론이었다.

    uv run tools/edges.py backlinks it/concepts/raft.md
    uv run tools/edges.py neighbors it/concepts/raft.md --depth 2
    uv run tools/edges.py degree --kb it --top 20
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import index_db, layout as layout_mod
from syntopicon.workspace import DEFAULT


def cmd_backlinks(connection, args) -> int:
    rows = index_db.backlinks(connection, args.path)
    for row in rows:
        anchor = f"#{row['anchor']}" if row["anchor"] else ""
        tag = "" if row["kind"] == "internal" else "  [cross-kb]"
        print(f"{row['src']}{anchor}{tag}")
    print(f"\n{len(rows)}건")
    return 0


def cmd_neighbors(connection, args) -> int:
    rows = index_db.neighbors(connection, args.path, args.depth, args.cross_kb)
    for row in rows:
        print(f"{row['hops']}홉  w={row['weight']:.4f}  {row['path']}")
    print(f"\n{len(rows)}건 (깊이 {args.depth}, 가중=경유 분기 역수 곱 — 고차수 경유는 강등)")
    return 0


def cmd_degree(connection, args) -> int:
    """허브 식별은 링크 차수 질의로 충분하다 — NetworkX 배치 분석은 불채택(PLAN §6).

    소비자: `<kb>/overview.md`의 Hubs 절 갱신 후보(kb-lint가 대조한다).
    """
    for row in index_db.degrees(connection, "in", kb=args.kb, top=args.top):
        print(f"{row['degree']:4}  {row['path']}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="링크 그래프 조회")
    sub = parser.add_subparsers(dest="command", required=True)

    back = sub.add_parser("backlinks", help="이 페이지를 가리키는 링크")
    back.add_argument("path")
    back.set_defaults(run=cmd_backlinks)

    near = sub.add_parser("neighbors", help="k-hop 이웃 (상한 4)")
    near.add_argument("path")
    near.add_argument("--depth", type=int, default=2)
    near.add_argument("--cross-kb", action="store_true", help="KB 경계를 넘어 탐색")
    near.set_defaults(run=cmd_neighbors)

    degree = sub.add_parser("degree", help="피링크 차수 상위 — 허브 후보")
    degree.add_argument("--kb", default=None)
    degree.add_argument("--top", type=int, default=20)
    degree.set_defaults(run=cmd_degree)

    args = parser.parse_args(argv)
    ws = DEFAULT
    if not ws.derived_db.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    with index_db.connect(ws) as connection:
        if reason := index_db.staleness(connection, layout_mod.load().kbs()):
            print(f"파생 인덱스가 낡았습니다 — {reason}. tools/reindex.py를 먼저 실행하십시오.",
                  file=sys.stderr)
            return 1
        try:
            return args.run(connection, args)
        except ValueError as error:
            print(f"중단: {error}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
