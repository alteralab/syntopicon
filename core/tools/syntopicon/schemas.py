"""per-type JSON Schema 로딩과 type 그룹 해석.

type 어휘의 정본은 schema/*.yaml이다. layout.yaml은 그룹 **이름**만 참조하고
값을 다시 열거하지 않는다 — 여기서 이름을 실제 type 집합으로 푼다.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from .repo import ROOT

SCHEMA_DIR = ROOT / "schema"


@dataclass(frozen=True)
class Schemas:
    #: 그룹 이름 → 그 그룹이 포괄하는 type 값들. 단일 type 스키마는 자기 이름이 그룹이다.
    groups: dict[str, frozenset[str]]
    #: type 값 → 그 type을 검증하는 validator
    validators: dict[str, Draft202012Validator]
    #: 스키마 문서 원본 (결번 키 대조용)
    documents: dict[str, dict]
    registry: Registry

    def group_of(self, type_value: str) -> str | None:
        return next((g for g, ts in self.groups.items() if type_value in ts), None)

    def shared(self, pointer: str) -> Draft202012Validator:
        """common.yaml의 공유 정의 하나를 단독 검증기로 꺼낸다 (예: 파일명=ID 검사)."""
        return Draft202012Validator(
            {"$ref": f"common.yaml#/$defs/{pointer}"}, registry=self.registry
        )


@cache
def load() -> Schemas:
    documents = {p.name: yaml.safe_load(p.read_text()) for p in SCHEMA_DIR.glob("*.yaml")}

    # $schema를 가진 것만 JSON Schema 리소스다. layout/vocabulary/user-dict는 설정이다.
    schema_docs = {n: d for n, d in documents.items() if "$schema" in d}
    registry = Registry().with_resources(
        (name, Resource.from_contents(doc, default_specification=DRAFT202012))
        for name, doc in schema_docs.items()
    )

    groups: dict[str, frozenset[str]] = {}
    validators: dict[str, Draft202012Validator] = {}
    for name, doc in schema_docs.items():
        spec = doc.get("properties", {}).get("type")
        if spec is None:      # common.yaml — 공유 정의뿐, 무엇도 검증하지 않는다
            continue
        # const면 단일 type, enum이면 파일 stem이 그룹 이름(예: source → CSL 10종)
        types = frozenset([spec["const"]] if "const" in spec else spec["enum"])
        groups[spec.get("const", Path(name).stem)] = types
        validator = Draft202012Validator(doc, registry=registry)
        validator.check_schema(doc)
        validators.update(dict.fromkeys(types, validator))

    return Schemas(
        groups=groups, validators=validators, documents=documents, registry=registry
    )


#: frontmatter를 규정하지 않는 스키마. 여기 키는 md 파일에 나타날 일이 없으므로 결번
#: 대조·사용률 검사의 우변에서 뺀다 — 넣으면 `covered`·`contents` 같은 키가 "선언됐지만
#: 쓰인 적 없음"으로 영구히 찍힌다(2026-08-12 실측: field-unused 12→19).
NOT_FRONTMATTER = frozenset({"progress.yaml"})


def declared_keys() -> set[str]:
    """현재 스키마가 선언한 frontmatter 키 전부 — 결번 대조의 우변."""
    return {
        key
        for name, doc in load().documents.items() if name not in NOT_FRONTMATTER
        for key in doc.get("properties", {})
    }
