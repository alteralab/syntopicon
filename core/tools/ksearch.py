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
from syntopicon.workspace import DEFAULT

SENTENCE = re.compile(r"(?<=[.!?。])\s+|\n{2,}")

#: 이 도구의 플래그 전부. `--`를 자동 삽입하는 스캔이 이 표를 읽으므로 파서와
#: 단일 출처여야 한다 — 플래그를 늘리면서 여기를 빠뜨리면 그 플래그가 질의로 샌다.
FLAGS = {"--kb": "값 있음", "-n": "값 있음", "-h": "값 없음", "--help": "값 없음"}


def split_query(argv: list[str]) -> list[str]:
    """`-XX:+PrintGCDetails` 같은 질의를 argparse가 옵션으로 오인하는 것을 막는다.

    코드 식별자는 대시로 시작하는 것이 흔한데(JVM 옵션·CLI 플래그), argparse는
    그것을 미등록 옵션으로 보고 종료한다(실측 2026-08-11: `ksearch.py "-XX:+..."`
    → usage 출력 후 exit 2). 사람이 `--`를 앞에 붙이는 것을 알 리 없다.

    플래그 표를 순서대로 소비해 **비플래그 토큰(질의)을 뽑아낸 뒤, 플래그를 앞에
    두고 `--` 다음에 질의를 놓도록 재배열한다.** `--` 뒤는 전부 위치 인자이므로
    질의를 맨 뒤로 옮기지 않으면 뒤따르는 플래그가 위치 인자로 샌다(실측: 질의
    자리에만 `--`를 끼우면 `-n 2`가 "unrecognized arguments"가 된다).

    패턴 매칭이 아니라 등록된 플래그 목록을 읽는 것이라 모르는 입력을 추측하지
    않는다. 이미 `--`가 있으면 사용자의 의도를 존중해 손대지 않는다.
    """
    if "--" in argv:
        return argv
    flags: list[str] = []
    query: list[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token in FLAGS:
            step = 2 if FLAGS[token] == "값 있음" else 1
            flags += argv[index:index + step]
            index += step
            continue
        query.append(token)
        index += 1
    if not query:
        return argv                      # 질의 없음 — argparse가 제 문구로 실패한다
    return flags + ["--"] + query


def snippet(raw: str, needles: list[str], limit: int = 3) -> str:
    """질의 형태소를 품은 문장 1–3개. 형태소가 아니라 원문을 보여 준다 —
    사람이 읽을 것은 `읽 일관`이 아니라 "읽기 일관성"이다."""
    sentences = [s.strip() for s in SENTENCE.split(raw) if s.strip() and not s.startswith("#")]
    hits = [s for s in sentences if any(n in s for n in needles)]
    return " ".join((hits or sentences)[:limit])[:240]


def hits(connection, expression: str, kb: str | None, limit: int) -> list:
    """형태소 레그 한 번 — kb 필터와 건수 상한까지 적용한 행들.

    tools/search.py(통합 질의)가 같은 레그를 쓰므로 여기가 단일 경로다 —
    두 구현이 갈라지면 단독 실행과 통합 실행이 다른 답을 낸다.
    """
    # unreviewed 라벨은 검역의 "보이는 저하"다(PLAN §4.4 쓰기 정책 ①) — inbox도
    # 검색에는 나오되, 아직 리뷰를 안 지났음이 결과 줄에서 바로 보여야 한다.
    # AfC의 실패 기전이 hiddenness였다(§8). LEFT JOIN: files에 없어도 결과는 산다.
    rows = connection.execute("""
        SELECT morph.path AS path, morph.anchor AS anchor, morph.line AS line,
               morph.raw AS raw, bm25(morph) AS score, files.unreviewed AS unreviewed
        FROM morph LEFT JOIN files ON files.path = morph.path
        WHERE morph MATCH ? ORDER BY score LIMIT ?
    """, (f"body : {expression}", limit * 3)).fetchall()
    kept = [row for row in rows if not kb or row["path"].startswith(f"{kb}/")]
    return kept[:limit]


def render(rows, needles: list[str]) -> None:
    for row in rows:
        location = f"{row['path']}#{row['anchor']}" if row["anchor"] else row["path"]
        label = "  [morph] [unreviewed]" if row["unreviewed"] else "  [morph]"
        print(f"{location}:{row['line']}{label}")
        print(f"    {snippet(row['raw'], needles)}\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="한국어 형태소 FTS")
    parser.add_argument("query")
    parser.add_argument("--kb", default=None, help="KB로 좁힌다 (읽기는 횡단이 기본)")
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args(split_query(argv))

    if not morph.available():
        print("kiwipiepy가 없습니다. uv sync --group index 를 먼저 실행하십시오.", file=sys.stderr)
        return 1
    ws = DEFAULT
    if not ws.derived_db.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    expression = morph.query_expression(args.query)
    if not expression:
        print(f"질의에서 색인 대상 형태소가 나오지 않았습니다: {args.query}\n"
              f"(유지 품사: {', '.join(sorted(morph.KEEP_TAGS))})", file=sys.stderr)
        return 1

    with index_db.connect(ws) as connection:
        if reason := index_db.staleness(connection):
            print(f"파생 인덱스가 낡았습니다 — {reason}. tools/reindex.py를 먼저 실행하십시오.",
                  file=sys.stderr)
            return 1
        rows = hits(connection, expression, args.kb, args.n)

    render(rows, morph.analyze(args.query))
    print(f"{len(rows)}건 · 분석된 질의: {expression}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
