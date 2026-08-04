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
    #: 저장소 **밖**에 둔다 — 안에 두면 validate의 루트 완전 분할 검사에 정당하게 걸린다.
    qmd_config_dir: Path

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

    def _git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def commit(self) -> None:
        """rename은 깨끗한 워킹 트리를 요구한다 — 되돌릴 수 있는 상태에서만 여러 파일을 고친다."""
        self._git("add", "-A")
        self._git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "fixture")

    def run(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        self._git("add", "-A")
        return subprocess.run(
            [sys.executable, str(REAL_ROOT / "tools" / script), *args],
            capture_output=True, text=True,
            # QMD_CONFIG_DIR은 qmd 자신의 테스트용 override다 — 우리가 만든 seam이 아니라
            # qmd와 같은 파일을 보게 하는 장치라서, 실제 홈 설정을 건드리지 않는다.
            env=os.environ | {
                "SYNTOPICON_ROOT": str(self.root),
                "QMD_CONFIG_DIR": str(self.qmd_config_dir),
            },
        )

    def validate(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run("validate.py", *args)

    def rename(self, old: str, new: str, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run("rename.py", old, new, *args)

    def kb_new(self, name: str, title: str, description: str,
               *args: str) -> subprocess.CompletedProcess[str]:
        return self.run("kb-new.py", name, "--title", title,
                        "--description", description, *args)

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text()


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    root = tmp_path / "repo"
    root.mkdir()
    shutil.copytree(REAL_ROOT / "schema", root / "schema")
    for name in ("SCHEMA.md", "overview.md", ".gitignore"):
        shutil.copy(REAL_ROOT / name, root / name)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    return Repo(root=root, qmd_config_dir=tmp_path / "qmdconfig")
