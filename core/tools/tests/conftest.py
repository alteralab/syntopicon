"""validate를 CLI 그대로 돌리기 위한 임시 저장소 픽스처.

모듈을 import해 내부를 찌르는 대신 서브프로세스로 실행한다 — 저장소 루트가
import 시점에 고정되는 구조라, 실제 호출 경로(pre-commit·ingest)와 같은 방식으로
돌리는 편이 정직하고 seam도 하나면 족하다.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

import pytest

REAL_ROOT = Path(__file__).resolve().parents[2]
VALIDATE = REAL_ROOT / "tools" / "validate.py"


@dataclass
class Repo:
    """임시 저장소 하나. schema/는 실물을 복사하므로 실제 규약을 검증한다."""

    root: Path

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip())
        return path

    def kb(self, name: str) -> None:
        self.write(f"{name}/overview.md", f"""
            ---
            type: guide
            title: {name}
            description: 테스트 KB
            ---

            # {name}

            ## Hubs
            """)

    def validate(self, *args: str) -> subprocess.CompletedProcess[str]:
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True,
                       capture_output=True)
        return subprocess.run(
            [sys.executable, str(VALIDATE), *args],
            capture_output=True, text=True,
            env=os.environ | {"SYNTOPICON_ROOT": str(self.root)},
        )


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    root = tmp_path / "repo"
    root.mkdir()
    shutil.copytree(REAL_ROOT / "schema", root / "schema")
    for name in ("SCHEMA.md", "overview.md", ".gitignore"):
        shutil.copy(REAL_ROOT / name, root / name)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    return Repo(root)
