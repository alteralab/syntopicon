#!/usr/bin/env python3
"""파생 인덱스 재생성 — frontmatter 메타 테이블 + edges (PLAN §4.4-9).

qmd 색인은 `qmd update && qmd embed`가 따로 담당한다. 이 도구는 qmd가 파싱하지 않는
두 가지, frontmatter와 링크 그래프만 맡는다.

    uv run tools/reindex.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import index_db
from syntopicon import layout as layout_mod
from syntopicon.workspace import DEFAULT


def main() -> int:
    layout = layout_mod.load()
    if not layout.kbs():
        print("KB가 없습니다. kb-new를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    try:
        with index_db.build_lock(DEFAULT):
            counts = index_db.build(layout)
    except RuntimeError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 1

    print(f"{index_db.DB_PATH.name}: 파일 {counts.files} · 간선 {counts.edges}"
          f" (미해결 {counts.unresolved})")
    if counts.morph:
        print(f"형태소 레그: 섹션 {counts.sections} · 파편화 후보 {counts.fragments}")
    else:
        print("형태소 레그 건너뜀 — kiwipiepy 미설치 (uv sync --group index). "
              "한국어 검색은 qmd 음절 레그만으로 돕니다.")
    if counts.unresolved:
        print("미해결 간선은 깨진 링크 후보입니다 — kb-lint가 리포트합니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
