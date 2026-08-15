#!/usr/bin/env python3
"""검색 실측 러너 — qrels를 레그별 CLI 실사용 경로에 던져 R@5·MRR·레이턴시를 잰다.

qmd bench(내부 API)가 아니라 CLI를 쓰는 이유: kb-query 실사용이 지나는 경로가
CLI/MCP이고, qmd 2.1.0 bench는 내부 store 경로에서 vector/hybrid 0건을 내는
결함이 실측됐다(직접 vsearch는 동일 질의 정답 1위).

질문지는 qrels/<이름>.yaml 조각들이다 — 소스당 한 파일. 단일 고정 파일이던 초판
26문항은 DW 2권 시절에 멈춰 그 뒤 도메인(카프카·DDIA·Raft·JVM)을 한 문항도
커버하지 못했다(2026-08-14 실측) — 질문지는 ingest마다 자라야 하고, 조각 분할이
그 성장 모델이다(log/ 프래그먼트와 같은 결정).

주기 두 갈래(LLMOps 책 3장 실측 이관 — 원장 2026-08-14):
- 결정적 레그(--legs fast: bm25·vector·morph)는 단발 실행이 유효하고 분당 끝나
  promote 사슬이 매 승급마다 자동 실행한다(--record 로 stats 이벤트).
- hybrid 레그(qmd query)는 LLM 질의 확장이 껴 비결정·저속이라 사슬에서 빼고
  수시 측정(--legs all)에서만 돈다. 단발 점수 차이는 노이즈일 수 있다 —
  변경 판정은 반복 실행과 유의성 검정으로(책 pp.67-68).
"""
import argparse
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

CODE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CODE_ROOT / "tools"))

from syntopicon import stats  # noqa: E402
from syntopicon.workspace import DEFAULT  # noqa: E402

QRELS_DIR = DEFAULT.root / "evals" / "retrieval" / "qrels"
RUNS_DIR = DEFAULT.root / "evals" / "runs"
QUERY_KEYS = {"id", "query", "type", "description", "expected_files", "expected_in_top_k"}

# 경보 바닥 — 실측에서 여유폭을 뺀 값. 코퍼스가 크고 다양해지며 완만히 내려가는
# 것이 정상이라 규모가 뛰면 바닥도 재실측으로 재조정한다(임의 하향이 아니라 기록된
# 재캘리브레이션이어야 한다). 이력: vector 0.833(45문서, 2026-08-07) → 0.736
# (390페이지, 08-15) → 0.634(533페이지 112문항, 08-16 — 하락 추세 자체는 연간
# 임베딩 재평가의 재심 신호로 원장 등재). morph는 0.763 → 0.773 → 0.781로 안정.
# bm25는 분업상(영문 원어·부분토큰 전담) 전체 R@5 저조가 정상이라 바닥이 없다.
FLOORS = {"vector(vsearch)": 0.60, "morph(ksearch)": 0.55}

QMD_LINE = re.compile(r"qmd://it/(\S+?\.md)")
KS_LINE = re.compile(r"^(it/\S+?\.md)")


def load_queries() -> list[dict]:
    """qrels 조각 전부 — 스키마가 어긋나면 조용히 넘기지 않고 죽는다."""
    files = sorted(QRELS_DIR.glob("*.yaml"))
    if not files:
        raise SystemExit(f"qrels 조각이 없습니다: {QRELS_DIR}")
    queries, seen = [], set()
    for path in files:
        doc = yaml.safe_load(path.read_text())
        for q in doc["queries"]:
            unknown = set(q) - QUERY_KEYS
            if unknown:
                raise SystemExit(f"{path.name}: 모르는 키 {sorted(unknown)} (id={q.get('id')})")
            if q["id"] in seen:
                raise SystemExit(f"{path.name}: id 중복 {q['id']}")
            seen.add(q["id"])
            queries.append(q)
    return queries


def run(cmd, timeout=120):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=CODE_ROOT)
    return p.stdout


def files_qmd(out):
    seen, ordered = set(), []
    for m in QMD_LINE.finditer(out):
        f = m.group(1)
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered


def files_ksearch(out):
    seen, ordered = set(), []
    for line in out.splitlines():
        m = KS_LINE.match(line.strip())
        if m:
            f = m.group(1).split("#")[0].removeprefix("it/")
            if f not in seen:
                seen.add(f)
                ordered.append(f)
    return ordered


LEGS = {
    "bm25(search)": lambda q: files_qmd(run(["qmd", "search", q, "-n", "10"])),
    "vector(vsearch)": lambda q: files_qmd(run(["qmd", "vsearch", q, "-n", "10"])),
    "morph(ksearch)": lambda q: files_ksearch(run(
        ["uv", "run", "--group", "index", "tools/ksearch.py", q, "-n", "10"])),
    "hybrid(query)": lambda q: files_qmd(run(["qmd", "query", q, "-n", "10"])),
}
FAST_LEGS = ("bm25(search)", "vector(vsearch)", "morph(ksearch)")


def score(found, gold, k=5):
    top = found[:k]
    hit = [g for g in gold if g in top]
    rr = 0.0
    for rank, f in enumerate(found, 1):
        if f in gold:
            rr = 1.0 / rank
            break
    return {"r_at_5": len(hit) / len(gold), "mrr": rr, "found_any": rr > 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description="검색 실측 러너")
    parser.add_argument("--legs", choices=["fast", "all"], default="all",
                        help="fast = 결정적 3레그(사슬용), all = hybrid 포함(수시 측정)")
    parser.add_argument("--record", action="store_true",
                        help="집계를 stats.sqlite events에 기록(사슬이 켠다)")
    args = parser.parse_args(argv)

    legs = {n: LEGS[n] for n in (FAST_LEGS if args.legs == "fast" else LEGS)}
    queries = load_queries()
    rows, latency = [], defaultdict(list)
    for q in queries:
        row = {"id": q["id"], "type": q["type"], "query": q["query"], "legs": {}}
        for leg, fn in legs.items():
            t0 = time.monotonic()
            try:
                found = fn(q["query"])
            except subprocess.TimeoutExpired:
                found = []
            ms = (time.monotonic() - t0) * 1000
            latency[leg].append(ms)
            s = score(found, q["expected_files"])
            s["top3"] = found[:3]
            s["ms"] = round(ms)
            row["legs"][leg] = s
        rows.append(row)
        print(f"{q['id']:12s} " + " ".join(
            f"{leg.split('(')[0]}:{'O' if row['legs'][leg]['found_any'] else '·'}"
            for leg in legs), file=sys.stderr)

    agg = defaultdict(lambda: defaultdict(list))
    for row in rows:
        for leg, s in row["legs"].items():
            agg[leg][row["type"]].append(s)
            agg[leg]["ALL"].append(s)
    summary = {}
    for leg, by_type in agg.items():
        summary[leg] = {}
        for t, ss in by_type.items():
            summary[leg][t] = {
                "n": len(ss),
                "R@5": round(sum(x["r_at_5"] for x in ss) / len(ss), 3),
                "MRR": round(sum(x["mrr"] for x in ss) / len(ss), 3),
                "found%": round(100 * sum(x["found_any"] for x in ss) / len(ss)),
                "p50ms": round(sorted(latency[leg])[len(latency[leg]) // 2]),
            }

    breaches = {
        leg: {"r_at_5": summary[leg]["ALL"]["R@5"], "floor": floor}
        for leg, floor in FLOORS.items()
        if leg in summary and summary[leg]["ALL"]["R@5"] < floor
    }

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / f"retrieval-{date.today():%Y%m%d}.json"
    out_path.write_text(json.dumps({"rows": rows, "summary": summary}, ensure_ascii=False, indent=1))

    for leg in legs:
        print(f"\n== {leg}")
        for t, m in sorted(summary[leg].items()):
            print(f"  {t:13s} n={m['n']:2d} R@5={m['R@5']:.3f} MRR={m['MRR']:.3f} "
                  f"found={m['found%']}% p50={m['p50ms']}ms")
    for leg, b in breaches.items():
        print(f"\n⚠ 경보: {leg} R@5={b['r_at_5']:.3f} < 바닥 {b['floor']} — 회귀 의심. "
              "질문지 추가 직후라면 신규 문항의 정답 경로부터 확인.")

    if args.record:
        with stats.connect() as connection:
            stats.record_event(connection, "retrieval_eval", {
                "legs": args.legs,
                "n_queries": len(queries),
                "summary": {leg: summary[leg]["ALL"] for leg in summary},
                "breaches": breaches,
                "results_file": out_path.name,
            })
    return 0


if __name__ == "__main__":
    sys.exit(main())
