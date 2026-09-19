"""검사 레지스트리 — 결과 종류의 이름·등급·지침의 단일 출처.

등급과 판독 지침이 코드(리터럴 41곳)와 kb-lint SKILL(손 유지 목록)에 병렬로
존재하던 시절 표류 3건이 실측됐다: 안내 누락 17종, 계수 38 대 41, 낡은 독스트링.
이제 Kind 선언이 유일한 정본이다 — SKILL은 `lint.py --explain`으로 여기를
조회하고, 테스트가 "모든 Kind에 doc과 guidance가 있다"를 강제하므로 지침 없는
검사는 추가 자체가 안 된다.

검사 함수는 `@check`로 선언 지점에서 등록한다(수동 튜플 대체). Finding은
등급을 들고 다니지 않는다 — 등급의 정본은 Kind다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jsonschema import Draft202012Validator

from .. import layout as layout_mod
from ..mdfile import MdFile


@dataclass(frozen=True)
class Kind:
    name: str
    severity: str      # error | warn | info
    doc: str           # 무엇을 잡는가 — 한 문장
    guidance: str      # 리포트를 읽는 사람이 다음에 할 일


KINDS: dict[str, Kind] = {}


# 등급의 표시 순서 — lint 리포트·--explain이 공유한다. 사전 2벌이 lint.py 안에
# 따로 있었다(2026-08-13 상수 감사).
SEVERITY_ORDER = {"error": 0, "warn": 1, "info": 2}


def kind(name: str, severity: str, doc: str, guidance: str) -> None:
    """결과 종류 선언 — 검사가 사는 모듈의 머리에서, 검사 곁에서 한다."""
    if name in KINDS:
        raise ValueError(f"결과 종류 중복 선언: {name}")
    if severity not in ("error", "warn", "info"):
        raise ValueError(f"{name}: 등급은 error|warn|info다 ({severity})")
    KINDS[name] = Kind(name, severity, doc, guidance)


CHECKS: list = []


def check(fn):
    """코퍼스 단위 검사 등록. 페이지 단위 검사(page.check_page)는 실행 구조가
    달라(변경분만 돈다) 여기 등록하지 않고 lint CLI가 직접 부른다."""
    CHECKS.append(fn)
    return fn


@dataclass(frozen=True)
class Finding:
    check: str
    message: str
    kb: str | None = None
    path: str | None = None

    def __post_init__(self):
        # 미선언 종류는 만들 수 없다 — 이해 못 하는 것을 조용히 통과시키지 않는다(§3).
        if self.check not in KINDS:
            raise ValueError(f"선언되지 않은 결과 종류: {self.check}")

    @property
    def severity(self) -> str:
        return KINDS[self.check].severity


@dataclass
class Context:
    layout: layout_mod.Layout
    connection: object
    files: dict[str, MdFile]          # 경로 → 파싱 결과 (전수)
    changed: set[str]                 # 이번에 페이지 검사를 돌릴 대상
    overlap_full: bool = False        # 전쌍 비교 (부트스트랩·분기) — 기본은 changed×전체
    meta: dict[str, dict] = field(default_factory=dict)
    epistemic: frozenset[str] = frozenset()
    #: 읽는 시점 상대 낱말의 폐쇄 어휘(schema/vocabulary.yaml time-relative)와 예외 합성어.
    time_relative: frozenset[str] = frozenset()
    time_relative_except: frozenset[str] = frozenset()
    #: `_progress.yaml` 검증기 — 스키마 적재는 실행당 1회여야 하므로(schemas.load는
    #: 부를 때마다 파일을 읽는다) 페이지 루프 밖에서 만들어 들고 다닌다.
    progress_validator: Draft202012Validator | None = None

    def kb_of(self, path: str) -> str:
        return path.split("/", 1)[0]
