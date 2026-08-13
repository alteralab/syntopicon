"""상수 드리프트 가드 — 같은 문자열 리터럴이 여러 모듈에 독립 정의되면 실패.

QMD_SCHEME = "qmd://"가 세 파일에 독립 정의돼 있었다(2026-08-13 상수 감사).
같은 개념의 사본은 한쪽만 고치는 드리프트로 틀리므로, 상수 목록 문서 대신
기계 가드를 둔다 — 관제는 산문이 아니라 검사다(계측·대응표와 같은 결정).

AST로 모듈 레벨 `UPPER = "리터럴"` 할당만 본다(파서 우선, PLAN §3). 한계도
성문한다: 표현식 상수(Path 연산 등)는 리터럴이 아니라 못 잡는다 — 그쪽의
실중복(PIN_PATH)은 소유 모듈(syntopicon.pin)로 옮겨 구조로 막았다.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]

# 짧은 리터럴("error", "-" 등)은 개념 공유가 아니라 어휘 중복이라 잡지 않는다.
MIN_LEN = 4


def module_string_constants(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, value = node.targets[0], node.value
        if (isinstance(target, ast.Name) and target.id.isupper()
                and isinstance(value, ast.Constant) and isinstance(value.value, str)
                and len(value.value) >= MIN_LEN):
            found[target.id] = value.value
    return found


def test_no_duplicate_string_constant_definitions():
    by_value = defaultdict(list)
    for path in sorted(TOOLS.rglob("*.py")):
        if "tests" in path.parts or "__pycache__" in path.parts:
            continue
        for name, value in module_string_constants(path).items():
            by_value[value].append(f"{path.relative_to(TOOLS)}:{name}")

    duplicates = {v: sites for v, sites in by_value.items() if len(sites) > 1}
    assert not duplicates, (
        "같은 문자열 리터럴이 여러 모듈에 독립 정의돼 있습니다 — 한 모듈이 소유하고 "
        f"나머지는 import 하십시오: {duplicates}")
