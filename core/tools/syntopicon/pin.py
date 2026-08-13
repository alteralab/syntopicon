"""tools/toolchain-pin.yaml — 툴체인 핀(PLAN §5)의 코드 쪽 접점.

경로·읽기·제자리 갱신을 여기서만 한다. PIN_PATH가 backup과 qmd-setup에
독립 정의 2벌로 있었고, 갱신 함수도 "주석 보존을 위해 sha256 줄만 고친다"는
같은 규율의 사본 2벌이었다(2026-08-13 상수 감사) — 한쪽만 고치는 드리프트를
막으려면 소유 모듈이 하나여야 한다.

제자리 갱신이 원칙인 이유: YAML 라운드트립은 주석을 전부 날리고, 이 파일에서
사라지면 곤란한 것이 정확히 주석(왜 벤더링하는가·왜 sha256이 핀인가)이다.
"""

from __future__ import annotations

from pathlib import Path

import yaml

PIN_PATH = Path(__file__).resolve().parents[1] / "toolchain-pin.yaml"


def load() -> dict:
    """핀 전체를 dict로 — 부를 때마다 현재를 읽는다(상태 함수 무캐시, PLAN §3)."""
    return yaml.safe_load(PIN_PATH.read_text())


def record_model_shas(pin: dict) -> None:
    """models 블록의 sha256 줄들을 제자리에서 고친다 — file: 키로 어느 모델의
    sha인지 추적한다."""
    lines = PIN_PATH.read_text().splitlines(keepends=True)
    wanted = {spec["file"]: spec["sha256"] for spec in pin["models"].values()}

    current = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("file:"):
            current = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("sha256:") and current in wanted:
            indent = line[: len(line) - len(line.lstrip())]
            lines[index] = f'{indent}sha256: "{wanted[current]}"\n'
            current = None
    PIN_PATH.write_text("".join(lines))


def record_restic_sha(sha: str) -> None:
    """restic 블록의 sha256 줄 하나를 제자리에서 고친다 — 블록 경계(비들여쓰기
    줄)로 범위를 잡는다. models 쪽과 매칭 기전이 달라 함수를 합치지 않는다."""
    lines = PIN_PATH.read_text().splitlines(keepends=True)
    in_block = False
    for index, line in enumerate(lines):
        if line.startswith("restic:"):
            in_block = True
        elif line and not line[0].isspace() and not line.startswith("#"):
            in_block = False
        elif in_block and line.strip().startswith("sha256:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[index] = f'{indent}sha256: "{sha}"\n'
            break
    PIN_PATH.write_text("".join(lines))
