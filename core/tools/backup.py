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

    uv run tools/backup.py bundle       # git 번들 (+ 검증)
    uv run tools/backup.py index        # qmd 인덱스 사본 (VACUUM INTO)
    uv run tools/backup.py bootstrap    # 복구용 정적 restic 바이너리 동봉
    uv run tools/backup.py restic       # archive/·툴체인 스냅샷
    uv run tools/backup.py all
"""

from __future__ import annotations

import argparse
import bz2
import hashlib
import os
import shutil
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod, pin as pin_mod, qmdstore
from syntopicon.repo import ROOT

# 인덱스 경로 해석은 qmdstore가 유일한 구현이다 — 사본이 갈라지면 "백업은 됐는데
# 엉뚱한 인덱스"가 조용히 생긴다.
QMD_INDEX = qmdstore.index_path()


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
    version = pin_mod.load()["qmd"]["version"]
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
    pin = pin_mod.load()
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



def cmd_bootstrap(_args) -> int:
    """복구용 정적 restic 바이너리를 백업 대상 옆에 둔다 (PLAN §5).

    복구 시점의 기기에는 restic도 Homebrew도 없을 수 있다. "복원하려면 먼저 restic을
    설치하라"는 순환을 끊는 것이 이 파일 하나다. brew 사본이 아니라 공식 릴리스
    정적 바이너리를 받고, 어떤 판본인지 sha256으로 확정한다.
    """
    pin = pin_mod.load()
    spec = pin["restic"]
    target = destination() / f"restic-{spec['version']}"

    if not target.is_file():
        url = (f"https://github.com/restic/restic/releases/download/"
               f"v{spec['version']}/{spec['asset']}")
        print(f"내려받는 중  {spec['asset']}")
        compressed = target.with_suffix(".bz2")
        try:
            urllib.request.urlretrieve(url, compressed)
        except urllib.error.URLError as error:
            print(f"실패: {error}", file=sys.stderr)
            return 1
        target.write_bytes(bz2.decompress(compressed.read_bytes()))
        compressed.unlink()
        target.chmod(0o755)

    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    if spec.get("sha256") and spec["sha256"] != sha:
        print(f"sha256이 핀과 다릅니다\n  기록 {spec['sha256']}\n  실제 {sha}", file=sys.stderr)
        return 1
    if not spec.get("sha256"):
        pin_mod.record_restic_sha(sha)

    version = subprocess.run([str(target), "version"], capture_output=True, text=True)
    print(f"restic  {target}  {sha[:16]}…")
    print(f"        {version.stdout.strip().splitlines()[0]}")
    return 0


def cmd_all(args) -> int:
    return max(cmd_bundle(args), cmd_index(args), cmd_bootstrap(args), cmd_restic(args))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="백업 (PLAN §5)")
    parser.add_argument("what", choices=["bundle", "index", "bootstrap", "restic", "all"])
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)
    return {"bundle": cmd_bundle, "index": cmd_index, "bootstrap": cmd_bootstrap,
            "restic": cmd_restic, "all": cmd_all}[args.what](args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
