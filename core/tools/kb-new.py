#!/usr/bin/env python3
"""KB의 유일한 생성 경로 (PLAN §4.3 kb-new ②: 기계 단계).

판단 게이트 ①("기본 답은 만들지 마라" — 분리 대 동거 심사 3문)은 이 스크립트가 아니라
스킬이 대화로 수행한다. 여기 오는 시점엔 이미 "동거 KB를 만든다"가 정해져 있다.
저장소 분리는 별개의 비가역 경로이므로 여기에 git init은 없다(PLAN §4.5).

    uv run tools/kb-new.py it --title "IT 지식" --description "서적·논문·기술 문서"
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from string import Template

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import repo, schemas
from syntopicon.mdfile import read
from syntopicon.repo import ROOT
from syntopicon.rewrite import replace_section_body


def qmd_config() -> Path:
    """qmd 자신의 해석 순서를 그대로 따른다 (qmd 2.1.0 dist/collections.js getConfigDir).

    자체 환경변수를 만들지 않는 이유: 우리가 쓰는 파일과 qmd가 읽는 파일이 갈라지면
    등록은 성공했는데 검색은 안 되는 상태가 조용히 생긴다.
    """
    if directory := os.environ.get("QMD_CONFIG_DIR"):
        return Path(directory) / "index.yml"
    if xdg := os.environ.get("XDG_CONFIG_HOME"):
        return Path(xdg) / "qmd" / "index.yml"
    return Path.home() / ".config" / "qmd" / "index.yml"


class KbNewError(Exception):
    """만들면 경계가 어긋나는 상황. 아무것도 만들지 않고 멈춘다."""


def check_preconditions(layout: layout_mod.Layout, sch: schemas.Schemas, name: str) -> None:
    if errors := list(sch.shared("kb_name").iter_errors(name)):
        raise KbNewError(f"KB 이름 '{name}': {errors[0].message}")
    if name in layout.shared_names:
        raise KbNewError(f"'{name}'은 공유 자산 이름입니다 — 루트 완전 분할이 깨집니다")

    target = ROOT / name
    if target.exists() and any(target.iterdir()):
        raise KbNewError(f"{name}/ 이 비어 있지 않습니다 — 기존 디렉터리를 KB로 승격하지 않습니다")


def create_skeleton(layout: layout_mod.Layout, name: str, title: str, description: str) -> list[Path]:
    """layout.yaml의 골격에서 직접 생성한다 — 템플릿 파일을 따로 두지 않는다(PLAN §6)."""
    fields = {
        "kb": name,
        "title": title,
        "description": description,
        "now": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    created = []
    for directory in layout.skeleton_dirs:
        (ROOT / name / directory).mkdir(parents=True, exist_ok=True)
    for relative, template in layout.skeleton_files.items():
        path = ROOT / name / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # O_EXCL — check-then-write는 병렬 프로세스에서 덮어쓴다(PLAN §2.5-5).
        with open(path, "x", encoding="utf-8") as handle:
            handle.write(Template(template).substitute(fields))
        created.append(path.relative_to(ROOT))
    return created


def register_qmd(layout: layout_mod.Layout, name: str) -> str:
    """전역 config에 컬렉션을 등록한다.

    `qmd collection add`를 쓰지 않는 이유: 그 CLI에는 --ignore 플래그가 없어
    archive/ 제외를 걸 수 없다(qmd 2.1.0 소스 확인). 전역 config는 layout.yaml에서
    재생성 가능한 파생물이라(PLAN §5) 직접 쓰는 것이 규약에 맞는다. 다음 qmd 실행이
    syncConfigToDb로 DB에 반영한다.
    """
    path = qmd_config()
    config = yaml.safe_load(path.read_text()) if path.is_file() else None
    config = config or {}
    collections = config.setdefault("collections", {}) or {}
    config["collections"] = collections

    if (existing := collections.get(name)) and existing.get("path") != str(ROOT / name):
        raise KbNewError(
            f"qmd 컬렉션 '{name}'이 이미 다른 경로를 가리킵니다: {existing.get('path')}. "
            "컬렉션 이름은 전역이므로 KB 이름을 바꾸거나 기존 컬렉션을 정리하십시오.")

    collections[name] = {
        "path": str(ROOT / name),
        "pattern": layout.index_pattern,
        "ignore": list(layout.index_ignore),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
    return str(path)


def router_body(layout: layout_mod.Layout) -> str:
    """라우터의 KB 목록은 파일시스템에서 재생성한다 — 레지스트리 이중화 없음(PLAN §3)."""
    lines = [
        "",
        "<!-- 기계 소유 절: tools/kb-new가 파일시스템에서 재생성한다. 손으로 고치지 말 것. -->",
        "",
    ]
    for kb in layout.kbs():
        marker = ROOT / kb / layout.marker_path
        front = read(marker, Path(kb) / layout.marker_path).frontmatter or {}
        lines.append(f"- [{front.get('title', kb)}]({kb}/{layout.marker_path}) — "
                     f"{front.get('description', '')}")
    if not layout.kbs():
        lines.append("아직 없다. `/kb-new`가 KB의 유일한 생성 경로다.")
    lines.append("")
    return "\n".join(lines)


def update_router(layout: layout_mod.Layout) -> Path:
    router = ROOT / "overview.md"
    result = replace_section_body(router.read_text(), layout.sections["router"], router_body(layout))
    router.write_text(result.text)
    return router.relative_to(ROOT)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="KB 생성 (기계 단계)")
    parser.add_argument("name", help="KB 디렉터리 이름 = qmd 컬렉션 이름")
    parser.add_argument("--title", required=True, help="KB overview.md의 title")
    parser.add_argument("--description", required=True, help="한 줄 오리엔테이션")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-qmd", action="store_true", help="qmd 컬렉션 등록을 건너뛴다")
    args = parser.parse_args(argv)

    layout, sch = layout_mod.load(), schemas.load()
    try:
        check_preconditions(layout, sch, args.name)
    except KbNewError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"{args.name}/ 생성 예정")
        print(f"  디렉터리  {', '.join(layout.skeleton_dirs)}")
        print(f"  파일      {', '.join(layout.skeleton_files)}")
        print(f"  qmd       컬렉션 '{args.name}' → {qmd_config()}")
        print(f"  라우터    overview.md의 '{layout.sections['router']}' 절 재생성")
        print("\n--dry-run — 아무것도 쓰지 않았습니다.")
        return 0

    try:
        created = create_skeleton(layout, args.name, args.title, args.description)
        # 방금 만든 KB가 보이도록 캐시를 비운다. KB 목록의 정본은 파일시스템이고
        # 그 스냅샷을 visible_files가 들고 있다.
        repo.visible_files.cache_clear()
        layout_mod.load.cache_clear()
        layout = layout_mod.load()
        registered = None if args.no_qmd else register_qmd(layout, args.name)
        router = update_router(layout)
    except KbNewError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 1

    for path in created:
        print(f"  생성  {path}")
    print(f"  갱신  {router}")
    if registered:
        print(f"  등록  qmd 컬렉션 '{args.name}' → {registered}")
    # restic은 백업 시점에 layout.kbs()로 --tag를 산출한다 — 여기서 등록할 상태가 없다.
    # 레지스트리를 만들면 그것이 곧 이중화다(PLAN §3).
    print(f"  백업  restic --tag {args.name} 은 백업 스크립트가 파일시스템에서 산출한다")

    print(flush=True)   # validate의 출력과 섞이지 않게 먼저 비운다
    return subprocess.run([sys.executable, str(Path(__file__).parent / "validate.py")]).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
