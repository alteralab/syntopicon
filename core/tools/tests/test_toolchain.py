"""툴체인 핀과 백업. 네트워크·외부 도구에 기대는 부분은 빼고 회귀하기 쉬운 것만 본다."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import yaml

from conftest import Repo

TOOLS = Path(__file__).resolve().parents[1]


def load(name: str, module_name: str):
    """하이픈이 든 파일명은 import 문으로 못 부른다."""
    spec = importlib.util.spec_from_file_location(module_name, TOOLS / name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


qmd_setup = load("qmd-setup.py", "qmd_setup")


def test_핀_갱신이_주석을_지우지_않는다(tmp_path, monkeypatch):
    """YAML 라운드트립은 주석을 날린다. 이 파일에서 사라지면 곤란한 것이 정확히
    주석(왜 벤더링하는가·왜 sha256이 핀인가)이라 제자리 치환이어야 한다."""
    pin = tmp_path / "qmd-pin.yaml"
    pin.write_text((TOOLS / "qmd-pin.yaml").read_text())
    before = pin.read_text()
    comments = sum(1 for line in before.splitlines() if line.strip().startswith("#"))
    assert comments > 5, "픽스처에 주석이 없으면 이 테스트는 아무것도 재지 않는다"

    monkeypatch.setattr(qmd_setup, "PIN_PATH", pin)
    data = yaml.safe_load(before)
    data["models"]["embed"]["sha256"] = "f" * 64
    qmd_setup.record_digests(data)

    after = pin.read_text()
    assert sum(1 for line in after.splitlines() if line.strip().startswith("#")) == comments
    assert f'sha256: "{"f" * 64}"' in after
    assert yaml.safe_load(after)["models"]["embed"]["sha256"] == "f" * 64
    # 다른 모델의 값은 그대로여야 한다
    assert yaml.safe_load(after)["models"]["rerank"]["sha256"] == \
        yaml.safe_load(before)["models"]["rerank"]["sha256"]


def test_핀에_선언된_모델이_셋이다():
    pin = yaml.safe_load((TOOLS / "qmd-pin.yaml").read_text())
    assert set(pin["models"]) == {"embed", "rerank", "generate"}
    for role, spec in pin["models"].items():
        assert spec["sha256"] and len(spec["sha256"]) == 64, f"{role}: sha256 미기록"


def test_임베딩_세대_게이트가_모델_교체를_막는다(tmp_path):
    """차원이 같은 모델끼리(Qwen3 1024d ↔ KURE-v1 1024d)는 qmd가 못 막는다 —
    수용 검증 ②의 A/B가 정확히 그 조합이라 이 게이트가 유일한 방어다."""
    vendor = tmp_path / "models"
    vendor.mkdir()
    pin = {"models": {"embed": {"sha256": "a" * 64}}}

    assert qmd_setup.check_embed_generation(pin, vendor, rebuilt=False) is True
    assert (vendor / qmd_setup.ACTIVE_MARKER).read_text().strip() == "a" * 64

    pin["models"]["embed"]["sha256"] = "b" * 64
    assert qmd_setup.check_embed_generation(pin, vendor, rebuilt=False) is False
    assert (vendor / qmd_setup.ACTIVE_MARKER).read_text().strip() == "a" * 64, \
        "재빌드 전에 마커가 갱신되면 게이트가 한 번만 걸리고 만다"

    assert qmd_setup.check_embed_generation(pin, vendor, rebuilt=True) is True
    assert (vendor / qmd_setup.ACTIVE_MARKER).read_text().strip() == "b" * 64


def test_번들이_실제로_복원된다(repo: Repo, tmp_path, monkeypatch):
    """검증되지 않은 백업은 백업이 아니다 — 만들고 끝내지 않고 복원까지 본다."""
    repo.kb_new("it", "IT 지식", "설명")
    repo.commit()

    backups = tmp_path / "backups"
    result = subprocess.run(
        [sys.executable, str(TOOLS / "backup.py"), "bundle"],
        capture_output=True, text=True,
        env={**__import__("os").environ,
             "SYNTOPICON_ROOT": str(repo.root),
             "SYNTOPICON_BACKUP_DIR": str(backups)},
    )
    assert result.returncode == 0, result.stderr

    bundle = next(backups.glob("*.bundle"))
    restored = tmp_path / "restored"
    subprocess.run(["git", "clone", "-q", str(bundle), str(restored)], check=True)
    assert (restored / "it" / "overview.md").is_file()


def test_백업_대상이_없으면_말해준다(repo: Repo, tmp_path):
    result = subprocess.run(
        [sys.executable, str(TOOLS / "backup.py"), "index"],
        capture_output=True, text=True,
        env={**__import__("os").environ,
             "SYNTOPICON_ROOT": str(repo.root),
             "SYNTOPICON_BACKUP_DIR": str(tmp_path / "b"),
             "XDG_CACHE_HOME": str(tmp_path / "nocache")},
    )
    assert result.returncode == 1 and "qmd 인덱스가 없습니다" in result.stderr
