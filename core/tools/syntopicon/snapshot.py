"""스냅샷 다이제스트 — `snapshot_sha256`의 계산 방식 한 곳.

PLAN §2.2는 `snapshot`이 디렉터리 루트이고 `snapshot_sha256`이 ingest 시점 1회 기록되는
변조 증거라는 것까지만 규정하고, 디렉터리를 어떻게 한 값으로 접는지는 정하지 않았다.
여기서 정한다: **매니페스트 해시** — 파일별 sha256과 상대 경로를 정렬해 한 줄씩 쓴 뒤
그 텍스트를 다시 sha256한다.

이 형태를 고른 이유는 PLAN §8이 근거로 든 BagIt이 정확히 매니페스트+체크섬 구조이기
때문이다. 파일 하나가 바뀌어도, 이름만 바뀌어도, 파일이 늘거나 줄어도 값이 달라진다.

ingest(스냅샷 기록)와 lint(변조 검사)가 같은 함수를 써야 한다 — 두 구현이 갈라지면
검사가 상시 불일치를 보고하거나 상시 침묵한다.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def manifest(root: Path) -> str:
    """`<sha256>  <상대 posix 경로>` 줄들. 사람이 읽고 diff할 수 있는 중간 산물이다."""
    lines = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    return "\n".join(lines) + "\n" if lines else ""


def digest(root: Path) -> str:
    return hashlib.sha256(manifest(root).encode()).hexdigest()
