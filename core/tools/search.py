#!/usr/bin/env python3
"""횡단 질의 — 세 갈래(qmd·형태소·rg)를 한 번에 돌리고 계측을 남긴다 (PLAN §4.1).

세 갈래를 사람이 명령 셋으로 나눠 치던 시절, 질의 계측(search_miss)은 스킬 산문이
기록을 지시했고 실측 0건이었다(lint 225런과 대조, 2026-08-13). 계측은 도구가
실행하는 김에 자동으로 남길 때만 산다 — 실행 진입점이 곧 기록 지점이어야 한다.

갈래 분담은 PLAN §4.1 그대로다: qmd는 낱말이 달라도 뜻이 비슷한 것, 형태소는
조사·활용·복합명사, rg는 글자 그대로(판 번호·코드 조각). 갈래가 빠지면 조용히
생략하지 않고 결과에 크게 적는다 — 조용한 생략은 "검색했다"는 착각을 만든다
(overlap 검사와 같은 규율).

    uv run --group index tools/search.py "읽기 일관성"
    uv run --group index tools/search.py "복제 지연" --kb it -n 5
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ksearch
import langfuse_bridge
from syntopicon import index_db, layout as layout_mod, morph, stats
from syntopicon.workspace import DEFAULT
from syntopicon.repo import ROOT, visible_files

#: 질의 확장·재정렬이 로컬 모델이라 첫 호출은 모델 적재까지 포함해 느리다.
QMD_TIMEOUT = 300
QMD_SCHEME = "qmd://"


def leg_qmd(query: str, kb: str | None, limit: int) -> tuple[dict, list[dict]]:
    """qmd 하이브리드 레그. (계측, 결과 목록)을 돌려준다 — 결과는 --json 그대로."""
    binary = shutil.which("qmd")
    if binary is None:
        return {"skipped": "qmd가 PATH에 없습니다"}, []

    argv = [binary, "query", query, "--json", "-n", str(limit)]
    if kb:
        argv += ["-c", kb]
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=QMD_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"skipped": f"{QMD_TIMEOUT}초 초과"}, []
    elapsed = int((time.monotonic() - started) * 1000)

    if proc.returncode != 0:
        return {"skipped": f"종료 {proc.returncode}: {proc.stderr.strip()[:200]}"}, []
    try:
        results = json.loads(proc.stdout)
    except json.JSONDecodeError as error:
        # 형식을 이해 못 하면 조용히 건너뛰지 않고 실패한다(PLAN §3) — qmd 판이
        # 바뀌어 출력이 달라졌다면 그것은 알아야 할 사건이지 빈 결과가 아니다.
        raise SystemExit(f"qmd --json 출력을 파싱하지 못했습니다: {error}\n"
                         f"머리 200자: {proc.stdout[:200]!r}") from error
    return {"hits": len(results), "ms": elapsed}, results


def leg_morph(query: str, kb: str | None, limit: int,
              kbs: tuple[str, ...]) -> tuple[dict, list, list[str]]:
    """형태소 레그 — ksearch와 같은 경로(hits)를 쓴다."""
    if not morph.available():
        return {"skipped": "kiwipiepy 미설치 (uv sync --group index)"}, [], []
    if not DEFAULT.derived_db.is_file():
        return {"skipped": "파생 인덱스 없음 (tools/reindex.py)"}, [], []
    expression = morph.query_expression(query)
    if not expression:
        return {"skipped": "색인 대상 형태소가 나오지 않음"}, [], []

    started = time.monotonic()
    with index_db.connect(DEFAULT) as connection:
        if reason := index_db.staleness(connection, kbs):
            # 다른 갈래(qmd·리터럴)는 살아 있으므로 실패 대신 크게 건너뛴다 —
            # 사유는 계측(legs)에 남아 낡은 색인의 빈도가 데이터가 된다.
            return {"skipped": f"색인이 낡음 — {reason} (tools/reindex.py)"}, [], []
        rows = ksearch.hits(connection, expression, kb, limit)
    elapsed = int((time.monotonic() - started) * 1000)
    return {"hits": len(rows), "ms": elapsed}, rows, morph.analyze(query)


def leg_literal(query: str, kb: str | None, limit: int,
                kbs: tuple[str, ...]) -> tuple[dict, list[str]]:
    """리터럴 레그 — 질의 문자열 그대로. 순위 없음, 존재 확인용(PLAN §4.1의 rg 자리).

    rg 서브프로세스 대신 파이썬 스캔인 이유: 대상 목록을 visible_files(git)에서
    받으므로 ignore·미추적 처리가 rg 플래그 튜닝 없이 저장소 정의와 정확히 같고,
    현 코퍼스(10² md)에서 수십 ms라 외부 의존을 살 이유가 없다. ripgrep 실물은
    이 기기에 있다(15.2.0, 2026-08-13 설치) — 스캔 지연이 체감으로 실측되는
    규모가 되면 이 함수만 rg 호출로 바꾼다(계약은 결과 줄 형식뿐).

    NFC로 맞춰 비교한다 — macOS 경유 본문이 NFD면 같은 글자도 바이트가 달라
    영원히 못 만난다(morph.analyze_tokens와 같은 함정).
    """
    scope = [kb] if kb else list(kbs)
    if not scope:
        return {"skipped": "검색할 KB가 없습니다"}, []

    started = time.monotonic()
    needle = unicodedata.normalize("NFC", query)
    found: list[str] = []
    for relative in visible_files():
        if relative.suffix != ".md" or relative.parts[0] not in scope:
            continue
        per_file = 0
        for number, line in enumerate((ROOT / relative).read_text().splitlines(), 1):
            if needle in unicodedata.normalize("NFC", line):
                found.append(f"{relative}:{number}:{line.strip()[:120]}")
                per_file += 1
                if per_file >= 3:              # 파일당 3건이면 존재 확인에 충분하다
                    break
    elapsed = int((time.monotonic() - started) * 1000)
    return {"hits": len(found), "ms": elapsed}, found[:limit]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="세 갈래 횡단 질의 (+ 자동 계측)")
    parser.add_argument("query")
    parser.add_argument("--kb", default=None, help="KB로 좁힌다 (읽기는 횡단이 기본)")
    parser.add_argument("-n", type=int, default=10)
    args = parser.parse_args(ksearch.split_query(argv))

    layout = layout_mod.load()
    if args.kb:
        layout.require(args.kb)
    kbs = layout.kbs()

    qmd_meta, qmd_rows = leg_qmd(args.query, args.kb, args.n)
    morph_meta, morph_rows, needles = leg_morph(args.query, args.kb, args.n, kbs)
    literal_meta, literal_lines = leg_literal(args.query, args.kb, args.n, kbs)

    if qmd_rows:
        print(f"── qmd ({qmd_meta['hits']}건) ──")
        for row in qmd_rows:
            path = str(row.get("file", "")).removeprefix(QMD_SCHEME)
            print(f"{path}  [qmd {row.get('score', 0):.2f}]  {row.get('title', '')}")
        print()
    if morph_rows:
        print(f"── 형태소 ({morph_meta['hits']}건) ──")
        ksearch.render(morph_rows, needles)
    if literal_lines:
        print(f"── 리터럴 ({literal_meta['hits']}건) ──")
        for line in literal_lines:
            print(f"  {line[:160]}")
        print()

    legs = {"qmd": qmd_meta, "morph": morph_meta, "literal": literal_meta}
    executed = [meta for meta in legs.values() if "hits" in meta]
    miss = bool(executed) and all(meta["hits"] == 0 for meta in executed)

    for name, meta in legs.items():
        if "skipped" in meta:
            print(f"주의: {name} 갈래를 건너뜀 — {meta['skipped']}")
    summary = " · ".join(
        f"{name} {meta['hits']}건" if "hits" in meta else f"{name} 건너뜀"
        for name, meta in legs.items())
    print(f"{summary}{'  — 세 갈래 모두 0건 (공백 기록됨)' if miss else ''}")

    with stats.connect(DEFAULT) as db:
        stats.record_event(db, "query", {
            "query": args.query, "kb": args.kb, "n": args.n,
            "legs": legs, "miss": miss,
        })
        if miss:
            # PLAN §6의 search-miss 경보가 읽는 표준 자리 — 이벤트 원장과 별개로
            # 스킬 시절부터 성문된 테이블을 도구가 처음으로 채운다.
            db.execute("INSERT INTO search_miss (at, kb, query) VALUES (?,?,?)",
                       (stats.now(), args.kb, args.query))

    langfuse_bridge.nudge()   # 층 2 편승 — 활동이 있는 날에만 하루 1회 백그라운드 동기화
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
