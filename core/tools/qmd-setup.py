#!/usr/bin/env python3
"""qmd 툴체인 고정과 복구 (PLAN §5·§6 구축).

새 기기 런북의 실행 가능한 판본이다. 산문으로 적힌 절차는 복구 시점에 실행되지
않거나 틀리게 실행된다 — 그래서 스크립트가 정본이고 `tools/toolchain-pin.yaml`이 그 입력이다.

하는 일:
  1. qmd 설치 버전이 핀과 같은지 확인
  2. GGUF 3개를 **벤더링**하고 sha256을 핀에 기록 — hf: URI는 `resolve/main`을 치므로
     리비전을 고정하지 못한다(qmd 소스 확인). 내용 해시가 실질 핀이다.
  3. 전역 config에 모델을 **로컬 경로**로 기록
  4. layout.yaml에서 KB 컬렉션을 재등록 (전역 config는 재생성 가능한 파생물)
  5. npm pack 타르볼 보존 — 레지스트리에서 사라져도 설치할 수 있어야 한다

    uv run tools/qmd-setup.py --check     # 상태만 본다
    uv run tools/qmd-setup.py             # 벤더링 + config 기록
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon.repo import ROOT

PIN_PATH = Path(__file__).resolve().parent / "toolchain-pin.yaml"
# 현재 인덱스를 만든 임베딩 모델의 sha256. qmd가 이 사실을 신뢰할 수 있게 기록하지
# 못하므로(아래 check_embed_generation 주석) 우리가 따로 들고 있는다.
ACTIVE_MARKER = "embed-model.sha256"
CACHE_DIR = Path(
    os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "qmd" / "models"


def qmd_config_path() -> Path:
    """qmd 자신의 해석 순서를 따른다 (kb-new와 같은 규칙)."""
    if directory := os.environ.get("QMD_CONFIG_DIR"):
        return Path(directory) / "index.yml"
    if xdg := os.environ.get("XDG_CONFIG_HOME"):
        return Path(xdg) / "qmd" / "index.yml"
    return Path.home() / ".config" / "qmd" / "index.yml"


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            sha.update(block)
    return sha.hexdigest()


def installed_qmd() -> tuple[str, str] | None:
    binary = shutil.which("qmd")
    if not binary:
        return None
    out = subprocess.run([binary, "--version"], capture_output=True, text=True).stdout.strip()
    # "qmd 2.1.0 (977563e)"
    parts = out.replace("(", "").replace(")", "").split()
    return (parts[1], parts[2]) if len(parts) >= 3 else (out, "")


def acquire(spec: dict, vendor: Path) -> tuple[Path, str]:
    """벤더 디렉터리에 파일을 놓는다. 캐시에 이미 있으면 그것을 옮겨 쓴다 —
    같은 파일을 두 번 받을 이유가 없고, 캐시본은 이미 동작이 확인된 것이다."""
    target = vendor / spec["file"]
    if target.is_file():
        return target, digest(target)

    cached = CACHE_DIR / f"hf_{spec['hf_repo'].replace('/', '_')}_{spec['file']}"
    alternatives = [cached, *CACHE_DIR.glob(f"*{spec['file']}")]
    for candidate in alternatives:
        if candidate.is_file():
            shutil.copy2(candidate, target)
            print(f"  캐시에서 벤더링  {spec['file']}")
            return target, digest(target)

    revision = spec.get("hf_revision") or "main"
    url = f"https://huggingface.co/{spec['hf_repo']}/resolve/{revision}/{spec['file']}"
    print(f"  내려받는 중      {spec['file']}  ({revision[:7]})")
    partial = target.with_suffix(target.suffix + ".part")
    urllib.request.urlretrieve(url, partial)
    partial.rename(target)                     # 반쪽 파일을 벤더 디렉터리에 남기지 않는다
    return target, digest(target)


def record_digests(pin: dict) -> None:
    """sha256 줄만 제자리에서 고친다.

    YAML 라운드트립으로 통째로 다시 쓰면 주석이 전부 날아간다. 이 파일에서 사라지면
    곤란한 것이 정확히 주석(왜 벤더링하는가·왜 sha256이 핀인가)이므로, 값이 바뀌는
    줄만 바꾼다 — 저장소의 다른 도구들과 같은 규율이다(PLAN §2.1).
    """
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


def check_embed_generation(pin: dict, vendor: Path, rebuilt: bool) -> bool:
    """임베딩 모델이 바뀌었는지 우리 쪽에서 판정한다. 바뀌었으면 blue/green 전면 재빌드다.

    **qmd에 맡길 수 없는 이유(2026-08-05 실측):**
    · `generateEmbeddings`가 벡터에 기록하는 모델 id는 `options?.model ?? DEFAULT_EMBED_MODEL`
      인데 CLI가 그 옵션을 넘기지 않는다. config로 모델을 바꿔도 인덱스에는 **기본 모델
      이름이 박힌다** — 1024차원 벡터에 embeddinggemma-300M(768차원) 라벨이 붙는 것을 확인했다.
    · 차원 불일치는 qmd가 fail-loud로 막지만, **같은 차원끼리는 못 막는다.** 수용 검증 ②의
      A/B(Qwen3-Embedding-0.6B vs KURE-v1)가 정확히 둘 다 1024차원이라 이 구멍에 들어간다.
    그래서 "무경고 recall 붕괴"(PLAN §4.1)를 막는 것은 이 함수다.
    """
    marker = vendor / ACTIVE_MARKER
    current = pin["models"]["embed"]["sha256"]
    previous = marker.read_text().strip() if marker.is_file() else None

    if previous and previous != current and not rebuilt:
        print("\n임베딩 모델이 바뀌었습니다 — 기존 벡터와 섞으면 recall이 조용히 무너집니다.",
              file=sys.stderr)
        print(f"  이전 {previous[:16]}…\n  현재 {current[:16]}…", file=sys.stderr)
        print("  blue/green 전면 재빌드가 필요합니다:  qmd update && qmd embed -f", file=sys.stderr)
        print("  (-f 가 기존 벡터를 전부 지운다 — 소스 확인)", file=sys.stderr)
        print("  재빌드를 마쳤으면: uv run tools/qmd-setup.py --rebuilt", file=sys.stderr)
        return False

    marker.write_text(current + "\n")
    return True


def register_collections(config: dict, layout: layout_mod.Layout) -> int:
    """KB 컬렉션을 layout.yaml에서 재생성한다 — 전역 config는 파생물이다(PLAN §5)."""
    collections = config.setdefault("collections", {}) or {}
    config["collections"] = collections
    for kb in layout.kbs():
        collections[kb] = {
            "path": str(ROOT / kb),
            "pattern": layout.index_pattern,
            "ignore": list(layout.index_ignore),
        }
    return len(layout.kbs())


def save_tarball(pin: dict, vendor: Path) -> Path | None:
    target = vendor / pin["qmd"]["tarball"]
    if target.is_file():
        return target
    spec = f"{pin['qmd']['package']}@{pin['qmd']['version']}"
    result = subprocess.run(["npm", "pack", spec, "--pack-destination", str(vendor)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  타르볼 보존 실패 ({spec}) — npm이 없거나 레지스트리에 닿지 못했습니다",
              file=sys.stderr)
        return None
    produced = vendor / result.stdout.strip().splitlines()[-1]
    if produced != target and produced.is_file():
        produced.rename(target)
    return target


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="qmd 툴체인 고정·복구")
    parser.add_argument("--check", action="store_true", help="상태만 보고 아무것도 바꾸지 않는다")
    parser.add_argument("--rebuilt", action="store_true",
                        help="blue/green 재빌드를 마쳤음을 기록한다 (qmd embed -f 이후)")
    args = parser.parse_args(argv)

    pin = yaml.safe_load(PIN_PATH.read_text())
    vendor = Path(pin["vendor_dir"]).expanduser()
    layout = layout_mod.load()

    print("qmd 설치")
    if (found := installed_qmd()) is None:
        print(f"  없음 — npm i -g {pin['qmd']['package']}@{pin['qmd']['version']}", file=sys.stderr)
        return 1
    version, commit = found
    match = version == pin["qmd"]["version"]
    print(f"  {version} ({commit})  {'핀과 일치' if match else '핀 불일치: ' + pin['qmd']['version']}")

    print(f"\n모델 벤더링 → {vendor}")
    if args.check:
        for role, spec in pin["models"].items():
            path = vendor / spec["file"]
            state = "있음" if path.is_file() else "없음"
            recorded = "기록됨" if spec.get("sha256") else "미기록"
            print(f"  {role:9} {spec['file']:44} {state} · sha256 {recorded}")
        marker = vendor / ACTIVE_MARKER
        active = marker.read_text().strip() if marker.is_file() else None
        embed = pin["models"]["embed"]["sha256"]
        print(f"  임베딩 세대  {'일치' if active == embed else '불일치 — 재빌드 필요' if active else '미기록'}")
        print(f"\nqmd config: {qmd_config_path()}")
        print(f"KB 컬렉션 대상: {', '.join(layout.kbs()) or '없음 (kb-new 전)'}")
        return 0

    vendor.mkdir(parents=True, exist_ok=True)
    for role, spec in pin["models"].items():
        path, sha = acquire(spec, vendor)
        if spec.get("sha256") and spec["sha256"] != sha:
            print(f"  {role}: sha256이 핀과 다릅니다 — 벤더 파일이 바뀌었습니다\n"
                  f"    기록 {spec['sha256']}\n    실제 {sha}", file=sys.stderr)
            return 1
        spec["sha256"] = sha
        print(f"  {role:9} {path.name}  {sha[:16]}…  {path.stat().st_size >> 20}MB")

    record_digests(pin)

    config_path = qmd_config_path()
    config = yaml.safe_load(config_path.read_text()) if config_path.is_file() else None
    config = config or {}
    config["models"] = {role: str(vendor / spec["file"]) for role, spec in pin["models"].items()}
    registered = register_collections(config, layout)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))

    print(f"\nconfig  {config_path}")
    print(f"  models  로컬 경로 3개 (hf: 아님 — 리비전 고정 불가라 벤더링본을 쓴다)")
    print(f"  컬렉션  {registered}개 재등록")

    if tarball := save_tarball(pin, vendor):
        print(f"  타르볼  {tarball.name}")

    if not check_embed_generation(pin, vendor, args.rebuilt):
        return 1
    print(f"  임베딩 세대  {'재빌드 기록됨' if args.rebuilt else '변화 없음 (증분 embed로 충분)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
