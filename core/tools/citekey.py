#!/usr/bin/env python3
"""citekey 발급 (PLAN §4.4-3, §2.5).

발급은 결정적 규칙이다: `저자성last연도[-슬러그]`. 같은 소스는 KB가 달라도 같은 키로
수렴하고, 경로가 구분한다. 그래서 중앙 발급 서비스가 필요 없다.

**O_EXCL로 만든다.** check-then-write는 같은 기기의 병렬 프로세스에서 서로를 덮어쓴다
— 파일시스템의 원자성이 게이트다(PLAN §2.5-5). 여기서 만들어진 빈 파일이 곧 예약이다.

    uv run tools/citekey.py --kb it --author Kleppmann --year 2017 --slug ddia
    uv run tools/citekey.py --kb it --author 홍길동 --year 2024 --romanized hong
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import schemas
from syntopicon.repo import ROOT

# citekey 문자 집합은 정규 언어라 regex가 정확한 도구다(PLAN §3의 명시 예외).
NON_KEY = re.compile(r"[^a-z0-9_.-]+")

SEED = """---
type: {type}
title: "{title}"
issued: "{year}"
---

# {title}
"""


def propose(author: str, year: int, slug: str | None) -> str:
    """성(last name)만 소문자로. 한국어 저자는 --romanized로 넘긴다 —
    발급 후 불변이므로 여기서 로마자화를 추측하면 그 추측이 영구히 남는다.

    성이 문자집합에서 전부 걸러지면(한글·키릴 등) 빈 문자열이 남고, 그러면 키가
    연도만 남아 `저자성last연도` 구조가 무너진다. 문자집합 검증은 통과하므로
    여기서 막지 않으면 조용히 손상된 키가 영구히 박힌다.
    """
    last = NON_KEY.sub("", author.strip().split()[-1].lower())
    if not last:
        raise ValueError(
            f"저자 '{author}'에서 쓸 수 있는 성을 얻지 못했습니다. "
            "소스에 인쇄된 영문 표기를 --romanized 로 넘기고, 없으면 RR 로마자화를 "
            "한 번 정해 넘기십시오(발급 후 불변입니다).")
    return f"{last}{year}" + (f"-{NON_KEY.sub('-', slug.strip().lower())}" if slug else "")


def issue(directory: Path, base: str) -> tuple[str, Path]:
    """O_EXCL로 자리를 잡는다. 동일 저자·연도 충돌만 `-2` 접미로 푼다(§2.5-4 예외)."""
    for suffix in ("", *(f"-{n}" for n in range(2, 100))):
        candidate = f"{base}{suffix}"
        path = directory / f"{candidate}.md"
        try:
            path.touch(exist_ok=False)      # O_EXCL
        except FileExistsError:
            continue
        return candidate, path
    raise RuntimeError(f"{base}: 접미 99까지 모두 사용 중입니다")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="citekey 발급 (O_EXCL 예약)")
    parser.add_argument("--kb", required=True)
    parser.add_argument("--author", required=True, help="저자. 성만 쓰인다")
    parser.add_argument("--romanized", default=None,
                        help="한국어 저자의 영문 표기. 소스에 인쇄된 표기를 우선한다")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--slug", default=None, help="같은 저자·연도를 구분할 짧은 말")
    parser.add_argument("--type", default="book", help="CSL 타입 (schema/source.yaml의 enum)")
    parser.add_argument("--title", default="", help="소스 메타 씨앗에 넣을 제목")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    layout, sch = layout_mod.load(), schemas.load()
    if args.kb not in layout.kbs():
        print(f"KB '{args.kb}'가 없습니다. kb-new를 먼저 실행하십시오.", file=sys.stderr)
        return 1
    if args.type not in sch.groups.get("source", ()):
        print(f"type '{args.type}'은 CSL 타입군에 없습니다: "
              f"{', '.join(sorted(sch.groups['source']))}", file=sys.stderr)
        return 1

    try:
        base = propose(args.romanized or args.author, args.year, args.slug)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    if errors := list(sch.shared("citekey").iter_errors(base)):
        print(f"제안된 citekey '{base}': {errors[0].message}\n"
              "한국어 저자라면 --romanized 로 영문 표기를 넘기십시오.", file=sys.stderr)
        return 1

    directory = ROOT / args.kb / "sources"
    if args.dry_run:
        taken = (directory / f"{base}.md").exists()
        print(f"{base}{'  (이미 사용 중 — -2 접미가 붙습니다)' if taken else ''}")
        return 0

    directory.mkdir(parents=True, exist_ok=True)
    citekey, path = issue(directory, base)
    path.write_text(SEED.format(type=args.type, year=args.year,
                                title=args.title or citekey))

    print(f"발급  {citekey}")
    print(f"파일  {path.relative_to(ROOT)}  (CSL 필드를 채우십시오)")
    if citekey != base:
        print(f"주의  '{base}'가 이미 있어 접미가 붙었습니다 — 같은 소스가 아닌지 확인하십시오")
    print(f"각주  본문에서 [^{citekey}] 로 인용하고 sources[]에 같은 id를 넣으십시오")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
