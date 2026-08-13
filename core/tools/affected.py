#!/usr/bin/env python3
"""영향 범위 조회 — 스키마·type·layout을 바꾸기 전에 무엇이 걸리는지 묻는다 (PLAN §6·§7).

10–20년 축에서 과거의 나는 타인이다. 영향 범위는 1인 장기 운영의 1위 실패 모드이고,
답은 기억이 아니라 조회에서 나온다. `migrations.md`에 변경을 기록하기 **전에** 돌린다.

    uv run tools/affected.py field stale_after
    uv run tools/affected.py type book --kb it
    uv run tools/affected.py dir inbox
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import index_db, schemas
from syntopicon.workspace import DEFAULT


class Hit(NamedTuple):
    """영향 파일 한 건 — 위치 인덱스(`row[1]`) 결합은 스키마가 바뀌면 조용히 어긋난다."""

    path: str
    kb: str
    detail: str


def by_field(connection, key: str) -> list[Hit]:
    """그 키를 실제로 담고 있는 파일. JSON 컬럼을 훑으므로 인덱스가 없어도 충분하다."""
    return [
        Hit(row["path"], row["kb"], json.dumps(json.loads(row["frontmatter"])[key],
                                               ensure_ascii=False, default=str))
        for row in connection.execute("SELECT path, kb, frontmatter FROM files")
        if key in json.loads(row["frontmatter"])
    ]


def by_column(connection, column: str, value: str) -> list[Hit]:
    rows = connection.execute(
        f"SELECT path, kb, type FROM files WHERE {column} = ? ORDER BY path", (value,))
    return [Hit(row["path"], row["kb"], row["type"]) for row in rows]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="스키마 변경의 영향 파일·KB 조회")
    sub = parser.add_subparsers(dest="axis", required=True)
    for axis, help_text in (("field", "frontmatter 키"),
                            ("type", "type 값"),
                            ("dir", "KB 콘텐츠 디렉터리")):
        command = sub.add_parser(axis, help=help_text)
        command.add_argument("value")
        command.add_argument("--kb", default=None)

    args = parser.parse_args(argv)
    ws = DEFAULT
    if not ws.derived_db.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    with index_db.connect(ws) as connection:
        match args.axis:
            case "field":
                rows = by_field(connection, args.value)
                if args.value not in schemas.declared_keys():
                    print(f"주의: '{args.value}'는 현재 스키마에 선언돼 있지 않습니다 "
                          "(결번 키이거나 오타일 수 있습니다).\n")
            case "type":
                rows = by_column(connection, "type", args.value)
            case _:
                rows = by_column(connection, "directory", args.value)

    if args.kb:
        rows = [row for row in rows if row.kb == args.kb]

    for row in rows:
        print(f"{row.path}\t{row.detail}")

    per_kb = Counter(row.kb for row in rows)
    summary = ", ".join(f"{kb} {count}" for kb, count in sorted(per_kb.items())) or "없음"
    print(f"\n{len(rows)}개 파일 · KB별: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
