#!/usr/bin/env python3
"""한국어 형태소 검색 (PLAN §4.1 자체 레그 ①).

qmd의 음절 레그가 못 잡는 것을 맡는다: 조사 변형·활용형·복합명사. 질의를 색인과
**같은 Kiwi + 같은 POS 필터**로 분석해 phrase로 던진다 — 대칭이 아니면 본문
`읽 일관`과 질의 `읽기 일관성`이 영원히 만나지 못한다.

영문 부분문자열은 `rg`가, 음절 substring은 qmd 내장 레그가 담당한다(PLAN §4.1).

    uv run --group index tools/ksearch.py "읽기 일관성"
    uv run --group index tools/ksearch.py "복제 지연" --kb it -n 5
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import index_db, morph

SENTENCE = re.compile(r"(?<=[.!?。])\s+|\n{2,}")


def snippet(raw: str, needles: list[str], limit: int = 3) -> str:
    """질의 형태소를 품은 문장 1–3개. 형태소가 아니라 원문을 보여 준다 —
    사람이 읽을 것은 `읽 일관`이 아니라 "읽기 일관성"이다."""
    sentences = [s.strip() for s in SENTENCE.split(raw) if s.strip() and not s.startswith("#")]
    hits = [s for s in sentences if any(n in s for n in needles)]
    return " ".join((hits or sentences)[:limit])[:240]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="한국어 형태소 FTS")
    parser.add_argument("query")
    parser.add_argument("--kb", default=None, help="KB로 좁힌다 (읽기는 횡단이 기본)")
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args(argv)

    if not morph.available():
        print("kiwipiepy가 없습니다. uv sync --group index 를 먼저 실행하십시오.", file=sys.stderr)
        return 1
    if not index_db.DB_PATH.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    expression = morph.query_expression(args.query)
    if not expression:
        print(f"질의에서 색인 대상 형태소가 나오지 않았습니다: {args.query}\n"
              f"(유지 품사: {', '.join(sorted(morph.KEEP_TAGS))})", file=sys.stderr)
        return 1

    with index_db.connect() as connection:
        # unreviewed 라벨은 검역의 "보이는 저하"다(PLAN §4.4 쓰기 정책 ①) — inbox도
        # 검색에는 나오되, 아직 리뷰를 안 지났음이 결과 줄에서 바로 보여야 한다.
        # AfC의 실패 기전이 hiddenness였다(§8). LEFT JOIN: files에 없어도 결과는 산다.
        rows = connection.execute("""
            SELECT morph.path AS path, morph.anchor AS anchor, morph.line AS line,
                   morph.raw AS raw, bm25(morph) AS score, files.unreviewed AS unreviewed
            FROM morph LEFT JOIN files ON files.path = morph.path
            WHERE morph MATCH ? ORDER BY score LIMIT ?
        """, (f"body : {expression}", args.n * 3)).fetchall()

    needles = morph.analyze(args.query)
    shown = 0
    for row in rows:
        if args.kb and not row["path"].startswith(f"{args.kb}/"):
            continue
        location = f"{row['path']}#{row['anchor']}" if row["anchor"] else row["path"]
        label = "  [morph] [unreviewed]" if row["unreviewed"] else "  [morph]"
        print(f"{location}:{row['line']}{label}")
        print(f"    {snippet(row['raw'], needles)}\n")
        shown += 1
        if shown >= args.n:
            break

    print(f"{shown}건 · 분석된 질의: {expression}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
