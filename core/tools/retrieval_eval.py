#!/usr/bin/env python3
"""멀티홉 검색 평가 하네스 (PLAN §4.2·§4.6 ⑨).

PLAN이 이름 붙인 4종을 여기 모았다 — gen_corpus는 syntopicon.synth, build_edges는
**기존 reindex를 그대로 쓴다**(따로 만들면 정본 이중화), eval_retrieval과 graph_batch는
아래 run/report다.

측정 대상은 두 전략이다:
  · flat   — 형태소 FTS 상위 n
  · expand — flat 상위 3개를 시드로 k홉 확장 (2-hop 질문 k=1, 3-hop 질문 k=2)

메트릭은 ir_measures(R@k·RR)에 자작 하나를 더한다: **expansion-only recall** —
확장이 아니었으면 못 찾았을 정답의 비율. 기성 IR 메트릭에 없는, 이 설계가 실제로
답해야 하는 질문이다.

합성 코퍼스는 심긴 체인이라 상한 추정이다. 판정은 수용 검증의 실코퍼스 재측정(§6 ⑥).

    uv run --group index --group eval tools/retrieval_eval.py
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

SEED_COUNT = 3          # PLAN §4.2 "top-3 시드"
TOP_N = 10


def _run_in(root: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOLS / script), *args],
        capture_output=True, text=True,
        env=os.environ | {"SYNTOPICON_ROOT": str(root)},
    )


def prepare(root: Path, chains: int):
    """합성 코퍼스 생성 → git 초기화 → 색인. 색인은 운영과 같은 reindex를 쓴다."""
    from syntopicon import synth

    questions = synth.generate(root, chains=chains)
    for name in ("SCHEMA.md", "overview.md", ".gitignore"):
        (root / name).write_text((TOOLS.parent / name).read_text())
    (root / "schema").mkdir(exist_ok=True)
    for path in (TOOLS.parent / "schema").iterdir():
        (root / "schema" / path.name).write_text(path.read_text())

    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, capture_output=True)
    result = _run_in(root, "reindex.py")
    if result.returncode != 0:
        raise RuntimeError(f"색인 실패:\n{result.stderr}")
    return questions


def search_flat(connection, query: str, limit: int) -> list[str]:
    from syntopicon import morph

    expression = morph.query_expression(query)
    if not expression:
        return []
    rows = connection.execute(
        "SELECT path, bm25(morph) AS score FROM morph WHERE morph MATCH ? "
        "ORDER BY score LIMIT ?", (f"body : {expression}", limit * 3)).fetchall()
    seen: list[str] = []
    for row in rows:                       # 섹션 단위 히트를 페이지로 접는다
        if row["path"] not in seen:
            seen.append(row["path"])
    return seen[:limit]


def search_expand(connection, query: str, depth: int, limit: int) -> list[str]:
    """top-3 시드에서 k홉 확장. 점수 = (1/시드 순위) × 경로 가중.

    경로 가중은 neighbors가 준다(경유 분기 역수 곱) — 고차수 허브를 경유한
    이웃은 자연 강등되므로, 메가허브가 있어도 확장이 전 KB를 동점으로
    쏟아내지 않는다. 그 성질은 하네스의 메가허브 시나리오가 단언한다.
    """
    from syntopicon import index_db

    scores: dict[str, float] = {}
    # 확장 시드에서 synthesis(허브)는 제외한다 — 허브에서의 확장은 차수 가중의
    # 정의상 균등 1/N 잡음이라 시드 슬롯만 소모한다(하네스가 메가허브 시나리오에서
    # 실측: 허브가 시드 슬롯을 훔치면 recall 1.0→0.9). 허브는 flat 결과·이웃으로는
    # 그대로 돌아온다 — 시드 자격만 콘텐츠 페이지로 한정한다. type 기준이라 상수가 없다.
    flat_pool = search_flat(connection, query, SEED_COUNT * 3)
    seed_types = {
        row["path"]: row["type"] for row in connection.execute(
            f"SELECT path, type FROM files WHERE path IN "
            f"({','.join('?' * len(flat_pool))})", flat_pool)
    } if flat_pool else {}
    seeds = [p for p in flat_pool if seed_types.get(p) != "synthesis"][:SEED_COUNT]
    for rank, seed in enumerate(seeds, start=1):
        scores[seed] = max(scores.get(seed, 0), 1 / rank)
        for row in index_db.neighbors(connection, seed, depth):
            candidate = (1 / rank) * row["weight"]
            scores[row["path"]] = max(scores.get(row["path"], 0), candidate)
    return sorted(scores, key=lambda p: -scores[p])[:limit]


def evaluate(root: Path, questions) -> dict:
    from ir_measures import RR, R, calc_aggregate
    from syntopicon import index_db

    index_db.DB_PATH = root / "derived.sqlite"        # 하네스 전용 루트
    qrels = {q.qid: {q.gold: 1} for q in questions}
    runs: dict[str, dict[str, dict[str, float]]] = {"flat": {}, "expand": {}}
    expansion_only = defaultdict(lambda: [0, 0])      # hops → [확장으로만 찾음, 전체]

    with index_db.connect() as connection:
        for question in questions:
            flat = search_flat(connection, question.text, TOP_N)
            expand = search_expand(connection, question.text, question.hops, TOP_N)
            runs["flat"][question.qid] = {p: float(TOP_N - i) for i, p in enumerate(flat)}
            runs["expand"][question.qid] = {p: float(TOP_N - i) for i, p in enumerate(expand)}

            bucket = expansion_only[question.hops]
            bucket[1] += 1
            if question.gold in expand and question.gold not in flat:
                bucket[0] += 1

    measures = [R @ TOP_N, RR]
    report = {
        strategy: {str(m): round(v, 4)
                   for m, v in calc_aggregate(measures, qrels, run).items()}
        for strategy, run in runs.items()
    }
    report["expansion_only_recall"] = {
        f"{hops}hop": round(found / total, 4) for hops, (found, total)
        in sorted(expansion_only.items())
    }
    report["by_hop"] = _by_hop(questions, qrels, runs, measures)
    return report


def _by_hop(questions, qrels, runs, measures) -> dict:
    """graph_batch — 홉 그룹별 집계. 평균 하나로는 어느 홉이 무너졌는지 안 보인다."""
    from ir_measures import calc_aggregate

    grouped = defaultdict(list)
    for question in questions:
        grouped[question.hops].append(question.qid)

    return {
        f"{hops}hop": {
            strategy: {str(m): round(v, 4) for m, v in calc_aggregate(
                measures,
                {q: qrels[q] for q in qids},
                {q: run[q] for q in qids},
            ).items()}
            for strategy, run in runs.items()
        }
        for hops, qids in sorted(grouped.items())
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="멀티홉 검색 평가 하네스")
    parser.add_argument("--chains", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="집계만 JSON으로 출력")
    parser.add_argument("--keep", type=Path, default=None, help="합성 코퍼스를 남길 경로")
    args = parser.parse_args(argv)

    try:
        from syntopicon import morph
        if not morph.available():
            raise ImportError
        import ir_measures  # noqa: F401
    except ImportError:
        print("의존이 없습니다: uv sync --group index --group eval", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as temporary:
        root = args.keep or Path(temporary) / "bench"
        root.mkdir(parents=True, exist_ok=True)
        questions = prepare(root, args.chains)
        report = evaluate(root, questions)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"합성 코퍼스 {args.chains}체인 · 질문 {len(questions)}개 "
          f"(2-hop {sum(1 for q in questions if q.hops == 1)} / "
          f"3-hop {sum(1 for q in questions if q.hops == 2)})\n")
    for strategy in ("flat", "expand"):
        metrics = " · ".join(f"{k} {v}" for k, v in report[strategy].items())
        print(f"{strategy:8} {metrics}")
    print("\n홉별:")
    for hops, per_strategy in report["by_hop"].items():
        print(f"  {hops}  flat {per_strategy['flat']}  →  expand {per_strategy['expand']}")
    print(f"\n확장으로만 찾은 정답: {report['expansion_only_recall']}")
    print("\n심긴 체인이라 상한 추정입니다 — 판정은 수용 검증의 실코퍼스 재측정(PLAN §4.2).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
