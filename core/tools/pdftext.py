#!/usr/bin/env python3
"""PDF 구간을 마크다운으로 추출한다 — 필터 차단 우회의 표준 추출기 (원장 2026-08-16).

비전 읽기가 콘텐츠 필터 오탐에 반복 차단될 때 오케스트레이터가 추출본을
공급하는 절차(kb-ingest 4단계)의 도구다. Data Mesh 5장에서 임시 pypdf
스크립트로 수행한 우회의 정식화 — pdf-inspector는 헤딩·표 구조를 보존한다.

    uv run --group ingest tools/pdftext.py <pdf> <시작쪽> <끝쪽> [-o out.md]

쪽 번호는 **1-기반 PDF 쪽**이다 — 책 내면 쪽이 아니다. 오프셋 대응은 그 소스의
`_progress.yaml` 머리말이 정본이다. 도판 내용은 추출본에 없다 — 반입 시 그
사실을 각주에 남기는 것은 소비자(추출 에이전트) 몫이다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="PDF 구간 마크다운 추출")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("start", type=int, help="시작 쪽(1-기반 PDF 쪽)")
    parser.add_argument("end", type=int, help="끝 쪽(포함)")
    parser.add_argument("-o", "--out", type=Path, help="출력 파일(생략 시 stdout)")
    args = parser.parse_args(argv)

    try:
        import pdf_inspector
    except ImportError:
        raise SystemExit("pdf-inspector가 필요합니다 — uv run --group ingest tools/pdftext.py …")
    if not args.pdf.is_file():
        raise SystemExit(f"파일이 없습니다: {args.pdf}")
    if args.start < 1 or args.end < args.start:
        raise SystemExit(f"쪽 범위가 성립하지 않습니다: {args.start}~{args.end} (1-기반, 시작<=끝)")

    result = pdf_inspector.extract_pages_markdown(
        str(args.pdf), list(range(args.start - 1, args.end)))
    chunks = []
    for page in result.pages:
        number = page.page + 1                      # 0-기반 → 1-기반
        chunks.append(f"=== PDF {number}쪽 ===")
        if page.needs_ocr:
            chunks.append(f"(이 쪽은 OCR 필요 판정 — 추출 신뢰 불가: {page.ocr_reason})")
        chunks.append(page.markdown.rstrip())
    text = "\n".join(chunks) + "\n"

    if args.out:
        args.out.write_text(text)
        print(f"{len(result.pages)}쪽 → {args.out} ({len(text)}자)", file=sys.stderr)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
