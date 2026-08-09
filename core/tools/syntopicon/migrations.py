"""schema/migrations.md의 결번 대장을 읽는다.

은퇴한 키 이름은 영구 결번이다 — 재사용하면 과거 파일의 같은 이름이 다른 의미가
된다. 산문 규칙이 지켜진다고 가정하지 않으므로 validate가 대조한다(PLAN §2.7).
"""

from __future__ import annotations

from functools import cache
from pathlib import Path

from markdown_it.token import Token

from .mdfile import parser
from .repo import ROOT

MIGRATIONS_PATH = ROOT / "schema" / "migrations.md"

# migrations.md 안에서 기계가 붙잡는 유일한 지점. 문서 본문에도 명시돼 있다.
LEDGER_HEADING = "결번 대장"


def _rows(tokens: list[Token], start: int) -> list[list[str]]:
    """table_open 위치에서 시작해 셀 텍스트를 행 단위로 모은다."""
    rows: list[list[str]] = []
    row: list[str] = []
    for token in tokens[start:]:
        match token.type:
            case "tr_open":
                row = []
            case "inline":
                row.append(token.content.strip())
            case "tr_close":
                rows.append(row)
            case "table_close":
                break
    return rows


@cache
def retired_keys() -> frozenset[str]:
    """결번 대장 1열의 키 이름 집합. 표가 비어 있으면 빈 집합."""
    if not MIGRATIONS_PATH.is_file():
        return frozenset()

    tokens = parser().parse(MIGRATIONS_PATH.read_text())
    under_ledger = False
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            under_ledger = tokens[index + 1].content.strip() == LEDGER_HEADING
        elif token.type == "table_open" and under_ledger:
            header, *body = _rows(tokens, index)
            return frozenset(row[0] for row in body if row and row[0])
    raise LookupError(
        f"{MIGRATIONS_PATH.name}에서 '{LEDGER_HEADING}' 절의 표를 찾지 못했습니다 — "
        "표가 비어 있어도 헤더 행은 남겨야 합니다."
    )
