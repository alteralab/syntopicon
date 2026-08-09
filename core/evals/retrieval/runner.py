#!/usr/bin/env python3
"""검색 실측 러너 — qrels를 4개 레그(CLI 실사용 경로)에 던져 R@5·MRR·레이턴시를 잰다.

qmd bench(내부 API)가 아니라 CLI를 쓰는 이유: kb-query 실사용이 지나는 경로가
CLI/MCP이고, qmd 2.1.0 bench는 내부 store 경로에서 vector/hybrid 0건을 내는
결함이 실측됐다(직접 vsearch는 동일 질의 정답 1위).
"""
import json, re, subprocess, sys, time
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FIXTURE = REPO / "evals/retrieval/dw-books-2026-08.json"
QMD_LINE = re.compile(r"qmd://it/(\S+?\.md)")
KS_LINE = re.compile(r"^(it/\S+?\.md)")

def run(cmd, timeout=120):
    t0 = time.monotonic()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=REPO)
    return p.stdout, (time.monotonic() - t0) * 1000

def files_qmd(out):
    seen, ordered = set(), []
    for m in QMD_LINE.finditer(out):
        f = m.group(1)
        if f not in seen:
            seen.add(f); ordered.append(f)
    return ordered

def files_ksearch(out):
    seen, ordered = set(), []
    for line in out.splitlines():
        m = KS_LINE.match(line.strip())
        if m:
            f = m.group(1).split("#")[0].removeprefix("it/")
            if f not in seen:
                seen.add(f); ordered.append(f)
    return ordered

LEGS = {
    "bm25(search)":   lambda q: files_qmd(run(["qmd", "search", q, "-n", "10"])[0]),
    "vector(vsearch)": lambda q: files_qmd(run(["qmd", "vsearch", q, "-n", "10"])[0]),
    "hybrid(query)":  lambda q: files_qmd(run(["qmd", "query", q, "-n", "10"])[0]),
    "morph(ksearch)": lambda q: files_ksearch(run(
        ["uv", "run", "--group", "index", "tools/ksearch.py", q, "-n", "10"])[0]),
}

def score(found, gold, k=5):
    top = found[:k]
    hit = [g for g in gold if g in top]
    rr = 0.0
    for rank, f in enumerate(found, 1):
        if f in gold:
            rr = 1.0 / rank
            break
    return {"r_at_5": len(hit) / len(gold), "mrr": rr, "found_any": rr > 0}

def main():
    fx = json.loads(FIXTURE.read_text())
    rows, latency = [], defaultdict(list)
    for q in fx["queries"]:
        row = {"id": q["id"], "type": q["type"], "query": q["query"], "legs": {}}
        for leg, fn in LEGS.items():
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
        print(f"{q['id']:10s} " + " ".join(
            f"{leg.split('(')[0]}:{'O' if row['legs'][leg]['found_any'] else '·'}"
            for leg in LEGS), file=sys.stderr)

    # 집계: 레그×클래스
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
    out = {"rows": rows, "summary": summary}
    Path("retrieval-results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for leg in LEGS:
        print(f"\n== {leg}")
        for t, m in sorted(summary[leg].items()):
            print(f"  {t:13s} n={m['n']:2d} R@5={m['R@5']:.3f} MRR={m['MRR']:.3f} found={m['found%']}% p50={m['p50ms']}ms")

if __name__ == "__main__":
    main()
