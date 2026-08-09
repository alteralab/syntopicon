#!/usr/bin/env python3
"""커밋 게이트 — 구조 무결성만 본다.

검사 범위(PLAN §6 구축 ①): JSON Schema + 관계 규칙 + layout 완전 분할 + 결번 키 대조.
pre-commit과 ingest 양쪽에서 같은 코드가 돈다.

여기서 하지 않는 것은 전부 kb-lint 소관이다 — 각주 없는 claim 불릿, 스냅샷 누락,
500줄·TOC, 미정의 epistemic 토큰, 고아 페이지, overlap. validate는 "깨졌는가"를,
lint는 "품질이 어떤가"를 묻는다. 경계를 섞으면 커밋이 품질 논쟁에 막힌다.

    uv run tools/validate.py              # 저장소 전체
    uv run tools/validate.py a.md b.md    # 파일 지정(저장소 전역 검사는 그대로 수행)
"""

from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import migrations, schemas
from syntopicon.mdfile import FrontmatterError, MdFile, read
from syntopicon.repo import ROOT, top_level_entries, visible_files

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"


@dataclass(frozen=True)
class Problem:
    severity: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity:5}  {self.path}: {self.message}"


def check_partition(layout: layout_mod.Layout, kbs: tuple[str, ...]) -> list[Problem]:
    """루트 직하는 `공유 자산 ∪ KB`로 완전히 갈라져야 한다.

    어느 쪽도 아닌 항목은 대개 오타 디렉터리다 — 조용히 색인 밖에 놓이느니
    커밋에서 막히는 편이 낫다.
    """
    unclassified = top_level_entries() - layout.shared_names - set(kbs)
    return [
        Problem(SEVERITY_ERROR, name,
                "루트 직하 항목이 공유 자산도 KB도 아닙니다 "
                f"(KB라면 {layout.marker_path}가 필요하고, 아니면 layout.yaml에 선언하십시오)")
        for name in sorted(unclassified)
    ]


def check_retired_keys(files: list[MdFile]) -> list[Problem]:
    """결번된 키가 현재 스키마나 콘텐츠에 되살아나지 않았는지 대조한다."""
    retired = migrations.retired_keys()
    if not retired:
        return []

    problems = [
        Problem(SEVERITY_ERROR, "schema/", f"결번 키 '{key}'가 현재 스키마에 선언돼 있습니다")
        for key in sorted(retired & schemas.declared_keys())
    ]
    problems += [
        Problem(SEVERITY_ERROR, str(f.path), f"결번 키 '{key}'를 사용했습니다")
        for f in files
        for key in sorted(retired & set(f.frontmatter or {}))
    ]
    return problems


def _id_kind(layout: layout_mod.Layout, kbs: tuple[str, ...], relative: Path) -> str | None:
    """파일명이 어떤 종류의 ID여야 하는가. 예약 파일명(overview 등)은 None."""
    directory = layout.content_dir_of(relative, kbs)
    if directory is None:
        return None
    return "citekey" if directory == "sources" else "slug"


def check_file(layout: layout_mod.Layout, kbs: tuple[str, ...],
               sch: schemas.Schemas, f: MdFile) -> list[Problem]:
    problems: list[Problem] = []
    path = str(f.path)
    front = f.frontmatter

    if front is None or "type" not in front:
        return [Problem(SEVERITY_ERROR, path, "typed frontmatter가 필요합니다 (type 키 부재)")]

    kind = front["type"]
    validator = sch.validators.get(kind)
    if validator is None:
        return [Problem(SEVERITY_ERROR, path, f"알 수 없는 type '{kind}' — schema/에 정의가 없습니다")]

    problems += [
        Problem(SEVERITY_ERROR, path, f"{e.json_path}: {e.message}")
        for e in sorted(validator.iter_errors(front), key=lambda e: e.json_path)
    ]

    # 디렉터리는 뷰, type 정본은 frontmatter — 둘의 정합만 강제한다.
    if (directory := layout.content_dir_of(f.path, kbs)) is not None:
        allowed = layout.dir_types[directory]
        if sch.group_of(kind) not in allowed:
            problems.append(Problem(
                SEVERITY_ERROR, path,
                f"{directory}/ 는 {list(allowed)} 그룹만 허용합니다 (이 파일은 '{kind}')"))

        for key, want in layout.dir_constraints.get(directory, {}).items():
            if front.get(key) != want:
                problems.append(Problem(
                    SEVERITY_ERROR, path, f"{directory}/ 는 {key}: {want} 가 필요합니다"))

    # 파일명 = ID. 발급 후 불변이므로 문자집합 위반은 여기서 막는 것이 마지막 기회다.
    if (id_kind := _id_kind(layout, kbs, f.path)) is not None:
        if errors := list(sch.shared(id_kind).iter_errors(f.path.stem)):
            problems.append(Problem(
                SEVERITY_ERROR, path, f"파일명이 {id_kind} 규칙 위반: {errors[0].message}"))

        # redirect 대상이 어떤 ID 문법이어야 하는지는 스텁이 놓인 디렉터리가 정한다.
        # 스키마는 네 형태를 다 받으므로(sources/는 citekey) 여기서 좁힌다.
        if kind == "redirect" and (target := front.get("superseded_by")):
            name = target.rpartition("/")[2]   # 정규형 `<kb>/<이름>`의 KB 접두 제거
            if errors := list(sch.shared(id_kind).iter_errors(name)):
                problems.append(Problem(
                    SEVERITY_ERROR, path,
                    f"superseded_by '{target}'가 {id_kind} 규칙 위반: {errors[0].message}"))

    # 각주 = 출처 귀속 전용 채널이므로, 인용된 라벨은 sources[]에 있어야 한다.
    # 반대 방향(선언했는데 인용 안 함)은 lint 소관이다 — 깨진 각주도 그쪽으로 드러난다
    # (MdFile.footnote_labels 주석 참조).
    declared = {s["id"] for s in front.get("sources", []) if isinstance(s, dict) and "id" in s}
    problems += [
        Problem(SEVERITY_ERROR, path, f"각주 [^{label}] 가 sources[]에 없습니다")
        for label in sorted(f.footnote_labels - declared)
    ]

    # frontmatter 경로는 저장소 루트 기준이며 실존해야 한다(§2.4). OS 절대경로도
    # 여기서 걸린다 — 저장소 밖 경로는 루트 아래에 존재하지 않는다.
    problems += [
        Problem(SEVERITY_ERROR, path, f"sources[].resource 경로가 없습니다: {s['resource']}")
        for s in front.get("sources", [])
        if isinstance(s, dict) and "resource" in s
        and not (ROOT / s["resource"].lstrip("/")).is_file()
    ]
    return problems


def check_uniqueness(layout: layout_mod.Layout, kbs: tuple[str, ...],
                     files: list[MdFile]) -> list[Problem]:
    """ID 유일성 스코프는 KB다 — 슬러그는 concepts/synthesis/inbox를 가로질러 유일해야 한다.

    한 가지 쌍만 합법이다: **concepts + inbox의 같은 슬러그 = 개정 대기**. 기존 페이지
    갱신도 검역을 지나야 하므로(PLAN §4.4-4·5) 개정 초안은 같은 ID의 검역 그림자로
    inbox에 머문다 — 두 ID의 충돌이 아니라 한 ID의 두 상태이고, 정규 참조형
    `<kb>/<slug>`는 발행 위치(concepts)로만 해석되므로 모호함도 없다. synthesis가
    끼는 쌍은 여전히 오류다 — 기계 산출물의 synthesis 직행은 금지다.
    """
    problems: list[Problem] = []
    for kb in kbs:
        seen: dict[str, list[str]] = defaultdict(list)
        dirs: dict[str, set[str]] = defaultdict(set)
        for f in files:
            if f.path.parts[0] == kb and (d := layout.content_dir_of(f.path, kbs)) is not None:
                seen[f.path.stem].append(str(f.path))
                dirs[f.path.stem].add(d)

        problems += [
            Problem(SEVERITY_ERROR, kb, f"ID '{ident}' 중복: {', '.join(paths)}")
            for ident, paths in sorted(seen.items())
            if len(paths) > 1 and not (len(paths) == 2 and dirs[ident] == {"concepts", "inbox"})
        ]

        # 유사 충돌은 경고다 — 하이픈만 다른 이름은 사람이 헷갈리지만 규칙 위반은 아니다.
        similar: dict[str, list[str]] = defaultdict(list)
        for ident in seen:
            similar[ident.replace("-", "")].append(ident)
        problems += [
            Problem(SEVERITY_WARN, kb, f"유사 ID: {', '.join(sorted(names))}")
            for names in similar.values() if len(names) > 1
        ]
    return problems


def collect(layout: layout_mod.Layout, kbs: tuple[str, ...],
            only: list[Path] | None) -> tuple[list[MdFile], list[Problem]]:
    """typed frontmatter 범위의 md를 읽는다. 범위 밖 .md는 검사 대상이 아니다."""
    scope = [
        p for p in visible_files()
        if p.suffix == ".md" and _in_scope(layout, kbs, p) and (only is None or p in only)
    ]
    files, problems = [], []
    for relative in scope:
        try:
            files.append(read(ROOT / relative, relative))
        except (FrontmatterError, yaml.YAMLError) as error:
            problems.append(Problem(SEVERITY_ERROR, str(relative), f"frontmatter를 읽지 못했습니다: {error}"))
    return files, problems


def _in_scope(layout: layout_mod.Layout, kbs: tuple[str, ...], relative: Path) -> bool:
    """layout.yaml의 typed_frontmatter 포함 목록에 걸리는가. `<kb>/`는 KB 이름으로 푼다."""
    for pattern in layout.typed_frontmatter:
        if not pattern.startswith("<kb>/"):
            if str(relative) == pattern:
                return True
        elif relative.parts[0] in kbs:
            within = Path(*relative.parts[1:])
            if within.full_match(pattern.removeprefix("<kb>/")):
                return True
    return False


def main(argv: list[str]) -> int:
    layout = layout_mod.load()
    sch = schemas.load()
    # KB 스냅샷은 연산당 한 번 — kbs()는 호출마다 git 서브프로세스라 루프에 넣으면
    # 파일 수에 비례해 폭발한다(2,113파일에서 247초 실측 → 이 끌어올림으로 초 단위).
    kbs = layout.kbs()

    only = None
    if argv:
        only = [Path(a).resolve().relative_to(ROOT) for a in argv]

    files, problems = collect(layout, kbs, only)
    problems += check_partition(layout, kbs)
    problems += check_retired_keys(files)
    problems += check_uniqueness(layout, kbs, files)
    for f in files:
        problems += check_file(layout, kbs, sch, f)

    errors = [p for p in problems if p.severity == SEVERITY_ERROR]
    for problem in sorted(problems, key=lambda p: (p.severity, p.path, p.message)):
        print(problem)

    named = f" ({', '.join(kbs)})" if kbs else ""
    print(f"\n{len(files)}개 파일 · KB {len(kbs)}개{named} · "
          f"오류 {len(errors)} · 경고 {len(problems) - len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
