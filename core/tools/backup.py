#!/usr/bin/env python3
"""백업 (PLAN §5 3계층).

| 데이터 클래스 | 1차 | 이 스크립트가 하는 일 |
|---|---|---|
| git 텍스트 | 로컬 클론 + GitHub | 분기 `git bundle --all` |
| archive/ 블롭·GGUF·타르볼 | 로컬 평문 | restic 스냅샷 (KB별 `--tag`) |
| SQLite 인덱스 | 사본이 1차 복구 경로 | `VACUUM INTO` 사본 + qmd 버전 라벨 |

**라이브 cp 금지.** SQLite 파일을 그냥 복사하면 쓰기 중인 페이지가 섞여 손상된 사본이
나온다 — `VACUUM INTO`만 쓴다(SQLite 공식).

대상 위치는 환경변수로 받는다. 저장소에 기기별 경로나 자격증명을 커밋하지 않고,
restic은 **자기 표준 변수**를 그대로 쓴다 — 우리가 새 변수를 만들면 restic CLI를
직접 부를 때와 갈라진다.

    SYNTOPICON_BACKUP_DIR=~/Backups/syntopicon   # bundle·인덱스 사본이 놓일 곳
    RESTIC_REPOSITORY=sftp:nas:/restic           # restic 표준
    RESTIC_PASSWORD_FILE=~/.restic-pass          # restic 표준

    uv run tools/backup.py bundle
    uv run tools/backup.py index
    uv run tools/backup.py restic
    uv run tools/backup.py all
"""

from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon.repo import ROOT

PIN_PATH = Path(__file__).resolve().parent / "qmd-pin.yaml"
QMD_INDEX = Path(
    os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "qmd" / "index.sqlite"


def destination() -> Path:
    raw = os.environ.get("SYNTOPICON_BACKUP_DIR")
    if not raw:
        raise SystemExit(
            "SYNTOPICON_BACKUP_DIR이 없습니다. bundle과 인덱스 사본이 놓일 곳을 지정하십시오.\n"
            "  예: export SYNTOPICON_BACKUP_DIR=~/Backups/syntopicon")
    path = Path(raw).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def cmd_bundle(_args) -> int:
    """`git bundle --all` — 원격이 전부 사라져도 이 파일 하나로 저장소가 산다.

    커밋 시점의 일관 스냅샷이라 다른 백업과 동시에 돌아도 안전하다(PLAN §2.5-7ⓕ).
    """
    target = destination() / f"syntopicon-{date.today():%Y%m%d}.bundle"
    subprocess.run(["git", "-C", str(ROOT), "bundle", "create", str(target), "--all"],
                   check=True)
    verify = subprocess.run(["git", "-C", str(ROOT), "bundle", "verify", str(target)],
                            capture_output=True, text=True)
    if verify.returncode != 0:
        print(f"번들 검증 실패:\n{verify.stderr}", file=sys.stderr)
        return 1
    print(f"번들  {target}  ({target.stat().st_size >> 10}KB)")
    print("복원: git clone <번들파일> <디렉터리>")
    return 0


def cmd_index(_args) -> int:
    """qmd 인덱스 사본. 재빌드는 폴백이고 사본이 1차 복구 경로다(PLAN §5).

    파일명에 qmd 버전을 박는다 — 사본은 **같은 버전으로만** 열어야 한다.
    """
    if not QMD_INDEX.is_file():
        print(f"qmd 인덱스가 없습니다: {QMD_INDEX}", file=sys.stderr)
        return 1
    version = yaml.safe_load(PIN_PATH.read_text())["qmd"]["version"]
    target = destination() / f"qmd-index-v{version}-{date.today():%Y%m%d}.sqlite"
    if target.exists():
        target.unlink()

    connection = sqlite3.connect(f"file:{QMD_INDEX}?mode=ro", uri=True)
    try:
        connection.execute("VACUUM INTO ?", (str(target),))
    finally:
        connection.close()

    print(f"인덱스 사본  {target}  ({target.stat().st_size >> 20}MB)")
    print(f"복원 후 `qmd status`와 테스트 검색으로 확인하십시오 (qmd {version} 전용).")
    return 0


def cmd_restic(args) -> int:
    """archive/ 블롭 + 벤더링 GGUF + qmd 타르볼. KB별 `--tag`(PLAN §4.5).

    태그는 파일시스템에서 산출한다 — 레지스트리를 따로 두면 그것이 곧 이중화다.
    """
    if not shutil.which("restic"):
        print("restic이 없습니다: brew install restic", file=sys.stderr)
        return 1
    if not os.environ.get("RESTIC_REPOSITORY"):
        print("RESTIC_REPOSITORY가 없습니다 (restic 표준 변수).\n"
              "  NAS는 SFTP나 rest-server를 쓰십시오 — SMB 마운트는 금지입니다(PLAN §5).",
              file=sys.stderr)
        return 1

    layout = layout_mod.load()
    pin = yaml.safe_load(PIN_PATH.read_text())
    vendor = Path(pin["vendor_dir"]).expanduser()

    failures = 0
    for kb in layout.kbs():
        archive = ROOT / kb / "archive"
        if not archive.is_dir():
            continue
        result = subprocess.run(
            ["restic", "backup", "--tag", kb, str(archive)], capture_output=not args.verbose)
        failures += result.returncode != 0
        print(f"  archive  {kb}  {'실패' if result.returncode else '완료'}")

    if vendor.is_dir():
        result = subprocess.run(
            ["restic", "backup", "--tag", "toolchain", str(vendor)],
            capture_output=not args.verbose)
        failures += result.returncode != 0
        print(f"  toolchain  {vendor}  {'실패' if result.returncode else '완료'}")

    if not layout.kbs() and not vendor.is_dir():
        print("백업할 것이 없습니다 — KB도 벤더링 모델도 없습니다.", file=sys.stderr)
        return 1

    print("\n무결성 검사는 별도 주기입니다: restic check --read-data-subset=5% (자동화),")
    print("연 1회 전수 restic check --read-data.")
    return 1 if failures else 0


def cmd_all(args) -> int:
    return max(cmd_bundle(args), cmd_index(args), cmd_restic(args))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="백업 (PLAN §5)")
    parser.add_argument("what", choices=["bundle", "index", "restic", "all"])
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)
    return {"bundle": cmd_bundle, "index": cmd_index,
            "restic": cmd_restic, "all": cmd_all}[args.what](args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
