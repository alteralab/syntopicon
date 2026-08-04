"""한국어 형태소 레그 (PLAN §4.1 자체 레그 ①).

Kiwi로 분석 → POS 필터 → 공백 join → FTS5 unicode61. 색인과 질의가 **같은 함수**를
쓰는 것이 이 레그의 전부다: 본문 "읽기 일관성"이 `읽 일관`으로 들어가는데 질의가
원형 그대로 가면 영원히 맞지 않는다(실측 — Kiwi는 `읽기`를 읽/VV + 기/ETN,
`일관성`을 일관/NNG + 성/XSN으로 가른다).

Tier B다. kiwipiepy가 없으면 이 레그만 조용히 빠지고 나머지 색인은 돈다 —
소모품 인덱스가 필수 의존을 만들면 안 된다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

from .repo import ROOT

USER_DICT = ROOT / "schema" / "user-dict.yaml"

# 유지할 품사. PLAN §4.1의 "명사류 + SL/SH/SN + 용언 어간 + XR"을 mecab-ko 태그로 편 것이고,
# nori DEFAULT_STOP_TAGS 30개(EP EF EC ETN ETM IC JK* JX JC MAG MAJ MM SP SS* SC SE
# XPN XSA XSN XSV UNA NA VSV — Lucene 소스 확인)와 교집합이 없다.
#
# nori가 남기는 VX(보조용언)·VCP/VCN(지정사)은 뺐다. 기능어라 색인 가치가 없고,
# PLAN이 말한 것은 "용언 **어간**"이다. 이 집합의 정확한 경계는 수용 검증 ①의
# 측정 대상이다(PLAN §6) — 바꾸면 재색인이 필요하다.
KEEP_TAGS = frozenset({
    "NNG", "NNP", "NNB", "NNBC", "NP", "NR",   # 명사류
    "SL", "SH", "SN",                          # 외국어·한자·숫자
    "VV", "VA",                                # 용언 어간
    "XR",                                      # 어근
})

#: 연속 1음절 형태소가 이만큼 이어지면 사용자 사전 후보로 본다. 자체 상수 —
#: 한국어 실질 형태소는 대개 2음절 이상이라, 1음절 런은 사전에 없는 복합어가
#: 잘게 부서진 흔적일 때가 많다.
FRAGMENT_RUN = 3

HANGUL = re.compile(r"^[가-힣]+$")


@dataclass(frozen=True)
class Fragment:
    """파편화 관측 1건 — 사용자 사전 후보 큐의 원료."""

    surface: str
    pieces: tuple[str, ...]


def available() -> bool:
    try:
        import kiwipiepy  # noqa: F401
    except ImportError:
        return False
    return True


@cache
def _kiwi():
    from kiwipiepy import Kiwi

    kiwi = Kiwi()
    entries = yaml.safe_load(USER_DICT.read_text()).get("entries") or []
    for entry in entries:
        kiwi.add_user_word(entry["form"], entry.get("pos", "NNP"), entry.get("score", 0.0))
    return kiwi


def analyze(text: str) -> list[str]:
    """색인·질의 양쪽이 쓰는 유일한 분석 경로. 여기가 갈라지면 레그 전체가 무의미하다."""
    return [t.form for t in _kiwi().tokenize(text) if t.tag in KEEP_TAGS]


def index_text(text: str) -> str:
    return " ".join(analyze(text))


def query_phrase(text: str) -> str:
    """질의를 FTS5 구문으로. 복합어는 성분으로 분해되므로 phrase로 묶어 순서를 보존한다."""
    morphemes = analyze(text)
    if not morphemes:
        return ""
    escaped = " ".join(m.replace('"', '""') for m in morphemes)
    return f'"{escaped}"'


def fragments(text: str) -> list[Fragment]:
    """연속 1음절 한글 형태소 런을 찾는다 → 사용자 사전 후보(PLAN §4.3)."""
    found, run = [], []
    for token in _kiwi().tokenize(text):
        single = token.tag in KEEP_TAGS and len(token.form) == 1 and HANGUL.match(token.form)
        if single:
            run.append(token.form)
            continue
        if len(run) >= FRAGMENT_RUN:
            found.append(Fragment(surface="".join(run), pieces=tuple(run)))
        run = []
    if len(run) >= FRAGMENT_RUN:
        found.append(Fragment(surface="".join(run), pieces=tuple(run)))
    return found


def sections(text: str, md):
    """페이지를 헤딩 단위로 자른다. 검색 결과가 파일이 아니라 섹션을 가리켜야
    '섹션 → 페이지 순 확장'(PLAN §4.1)이 가능하다.

    HTML 블록은 비워 낸다. AST가 짚어 준 줄 범위만 지우므로 본문은 그대로다.
    """
    lines = text.splitlines()
    for start, end in md.html_ranges:
        lines[start - 1:end] = [""] * (end - start + 1)

    headings, first_body_line = md.headings, md.first_body_line
    starts = [(line, title) for level, line, title in headings if level >= 2]
    if not starts:
        yield None, first_body_line, "\n".join(lines[first_body_line - 1:])
        return
    if starts[0][0] > first_body_line:
        yield None, first_body_line, "\n".join(lines[first_body_line - 1:starts[0][0] - 1])
    for index, (line, title) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        yield title, line, "\n".join(lines[line - 1:end])


def anchor(title: str | None) -> str | None:
    """GitHub 헤딩 앵커. 소문자화 + 공백→하이픈 + 영숫자·하이픈·한글만 남긴다."""
    if title is None:
        return None
    slug = re.sub(r"[^\w\s-]", "", title.strip().lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", slug)
