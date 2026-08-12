"""소스 출처 검사 — 데이터 소스는 archive/ 디렉터리(git 밖).

validate가 아니라 lint 소관인 이유가 이것이다: `archive/`는 git 밖이라
커밋 게이트가 볼 수 없다.
"""

from __future__ import annotations

import yaml

from .. import snapshot
from ..repo import ROOT
from .base import Finding, kind

kind("snapshot-missing", "warn", "선언된 스냅샷 디렉터리 부재",
     "archive에 원문을 복원하거나 restic에서 되찾는다. 외부 링크는 연 3% 이상 "
     "부패하므로 소급은 갈수록 불가능해진다.")
kind("snapshot-mismatch", "error", "스냅샷 다이제스트 불일치",
     "변조 증거다. snapshot_sha256은 write-once이므로 기록을 새 값으로 덮지 말고 "
     "무엇이 왜 바뀌었는지부터 본다.")
kind("progress-missing", "warn", "_progress.yaml 부재",
     "재개점 정본을 만든다 — 소스 메타 산문에 기대면 표류한다(아홉 런 뒤처진 실측).")
kind("progress-invalid", "error", "_progress.yaml 파싱·스키마 오류",
     "YAML과 스키마 오류를 고친다. 재개점 정본이 깨진 채면 다음 런이 중복 반입한다.")
kind("progress-unit", "warn", "소스 타입과 progress 단위 불일치",
     "타입에 맞는 단위로 고친다 — book은 page·chapter, webpage는 url, 논문은 whole.")
kind("progress-contents", "warn", "unit: page인데 장↔쪽 대응 부재",
     "contents를 목차에서 옮긴다 — covered 범위가 몇 장인지 읽히게 된다.")
kind("progress-suffix", "warn", "progress 값에 단위 접미 부재",
     "값마다 접미(p·ch)를 붙인다 — 값만 인용되면 단위를 잃는다.")


def check_snapshot(kb: str, path: str, front: dict):
    if not (declared := front.get("snapshot")):
        return
    root = ROOT / declared.lstrip("/")
    if not root.is_dir():
        yield Finding("snapshot-missing",
                      f"{declared} 가 없습니다 — 외부 링크는 연 3% 이상 부패합니다", kb, path)
        return
    if (recorded := front.get("snapshot_sha256")) and recorded != snapshot.digest(root):
        yield Finding("snapshot-mismatch",
                      f"{declared} 의 다이제스트가 기록과 다릅니다 — 변조 증거", kb, path)


#: 소스 타입 → `_progress.yaml`이 쓸 수 있는 단위. 소스가 나뉘는 방식이 타입마다 다르다.
#: 논문은 나눌 이유가 없고(한 편이 한 단위), 웹 문서는 스냅샷한 URL 하나가 한 단위다.
UNITS_FOR = {"book": {"page", "chapter"}, "webpage": {"url"},
             "paper": {"whole"}, "paper-conference": {"whole"}}


def check_progress(kb: str, path: str, front: dict, validator):
    """`archive/<citekey>/_progress.yaml` — 재개점의 정본(schema/progress.yaml).

    이 검사가 막는 실패는 하나다: 소스 메타 산문이 정본 노릇을 하다 아홉 런
    뒤처져 재반입을 부를 뻔했다(2026-08-12).
    """
    if not (declared := front.get("snapshot")):
        return
    progress = ROOT / declared.lstrip("/") / "_progress.yaml"
    if not progress.is_file():
        yield Finding("progress-missing",
                      f"{declared}_progress.yaml 이 없습니다 — 재개점을 소스 메타 산문에 "
                      f"기대면 표류합니다", kb, path)
        return
    try:
        document = yaml.safe_load(progress.read_text())
    except yaml.YAMLError as error:
        yield Finding("progress-invalid", f"_progress.yaml 파싱 실패: {error}", kb, path)
        return

    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "(루트)"
        yield Finding("progress-invalid", f"_progress.yaml {where}: {error.message}", kb, path)
        return

    # 타입↔단위 정합. 소스 타입은 frontmatter가 정본이다 — 경로에 인코딩하지 않는다(§3).
    allowed = UNITS_FOR.get(front.get("type"), set())
    if allowed and document["unit"] not in allowed:
        yield Finding("progress-unit",
                      f"type: {front['type']} 인데 unit: {document['unit']} — "
                      f"쓸 수 있는 것은 {sorted(allowed)}", kb, path)
    if document["unit"] == "page" and not document.get("contents"):
        yield Finding("progress-contents",
                      "unit: page 인데 contents(장↔쪽 대응)가 없습니다 — 목차에서 옮기면 "
                      "covered 범위가 몇 장인지 읽힙니다", kb, path)

    # 접미↔단위 일치. 값이 인용될 때 단위가 떨어져 나가는 것을 막으려고 값마다 붙이되,
    # 붙인 것이 `unit`과 어긋나면 두 정본이 되므로 여기서 묶는다(schema/progress.yaml).
    if suffix := {"page": "p", "chapter": "ch"}.get(document["unit"]):
        ranges = [*document["covered"], *(s["range"] for s in document["skipped"]),
                  *document.get("contents", {}).values()]
        for value in ranges + [document.get("total"), document.get("next")]:
            if value is None:
                continue
            for part in str(value).split("-"):
                if part and not part.endswith(suffix):
                    yield Finding("progress-suffix",
                                  f"unit: {document['unit']} 인데 `{value}` 에 접미 "
                                  f"`{suffix}` 가 없습니다 — 값만 인용되면 단위를 잃습니다",
                                  kb, path)
