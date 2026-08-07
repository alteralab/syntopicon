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
import unicodedata
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


def base_tag(tag: str) -> str:
    """Kiwi의 불규칙 활용 변형 접미를 떼어 낸 기본 태그.

    Kiwi는 용언 어간을 규칙/불규칙으로 갈라 `VV-R`·`VV-I`·`VA-I` 같은 태그를 붙인다
    (실측: 긋다→긋/VV-I, 어렵다→어렵/VA-I, 먹다→먹/VV). 접미를 떼지 않으면 KEEP_TAGS의
    `VV`·`VA`에 걸리지 않아 **불규칙 용언이 통째로 색인에서 빠진다** — 긋다·걷다·듣다·
    돕다·어렵다·아름답다가 전부 그렇다. 한국어에서 이는 작은 누락이 아니다.
    """
    return tag.split("-", 1)[0]


def analyze_tokens(text: str):
    """색인·질의 양쪽이 쓰는 유일한 분석 경로(토큰 객체 — form과 원문 위치 포함).

    NFC로 정규화하고 들어간다 — macOS 도구가 만든 NFD 본문은 바이트가 달라
    NFC 질의와 영원히 못 만난다(적대 배터리 실측: NFD 페이지가 검색 0건).
    색인과 질의가 같은 함수를 지나므로 여기 한 곳이면 양쪽이 함께 고쳐진다.

    **호출자는 전체 텍스트를 한 번에 넣어야 한다.** Kiwi는 문맥 민감이라 같은
    낱말도 홀로 분석하면 다른 형태소가 나온다("완만하게" 단독 → 완만하,
    문장 속 → 완만 — 실측). 낱말별 재분석은 색인과 질의를 조용히 가른다.
    """
    text = unicodedata.normalize("NFC", text)
    return [t for t in _kiwi().tokenize(text) if base_tag(t.tag) in KEEP_TAGS]


def analyze(text: str) -> list[str]:
    return [t.form for t in analyze_tokens(text)]


def index_text(text: str) -> str:
    return " ".join(analyze(text))


def query_expression(text: str) -> str:
    """질의를 FTS5 구문으로 — **낱말 단위로** 분석해 낱말끼리는 AND, 낱말 안은 phrase.

    질의 전체를 한 phrase로 묶으면 모든 형태소가 본문에서 인접해야 하고, 그런 일은
    거의 없다(멀티홉 하네스 실측: 전체 phrase는 recall 0.0). PLAN §4.1이 phrase를
    말한 대상은 "compound는 성분 분해 + phrase 질의" — 복합어 하나이지 질의 전체가
    아니다. FTS5는 공백을 암묵 AND로 읽는다(실측 확인).

    분석은 **질의 전문을 한 번에** 하고(색인과 같은 입도 — analyze_tokens 주석의
    문맥 민감성), 낱말 묶음은 토큰의 원문 위치로 복원한다. 낱말별 재분석은
    "완만하게 변하는 차원"이 색인(완만)과 다른 형태소(완만하)를 내는 것이 실측돼
    금지다.
    """
    # 원문 문자 위치 → 낱말 번호 (공백 경계로 증가)
    word_id, ids = 0, []
    prev_space = True
    for ch in unicodedata.normalize("NFC", text):
        if ch.isspace():
            prev_space = True
            ids.append(-1)
        else:
            if prev_space:
                word_id += 1
                prev_space = False
            ids.append(word_id)

    grouped: dict[int, list[str]] = {}
    for token in analyze_tokens(text):
        wid = ids[token.start] if token.start < len(ids) else word_id
        grouped.setdefault(wid, []).append(token.form.replace('"', '""'))

    words = []
    for _, morphemes in sorted(grouped.items()):
        if len(morphemes) > 1:
            words.append('"' + " ".join(morphemes) + '"')   # 복합어 — 순서 보존
        else:
            # 홑항도 인용한다. 비인용 토큰은 FTS5 문법에 노출된다 — 영어 낱말
            # AND/OR/NOT이 연산자로 해석돼 크래시했다(적대 배터리 실측). 인용은
            # 키워드 블랙리스트와 달리 그 클래스 전체를 없앤다.
            words.append('"' + morphemes[0] + '"')
    return " ".join(words)


def fragments(text: str) -> list[Fragment]:
    """연속 1음절 한글 형태소 런을 찾는다 → 사용자 사전 후보(PLAN §4.3)."""
    found, run = [], []
    for token in _kiwi().tokenize(unicodedata.normalize("NFC", text)):
        single = (base_tag(token.tag) in KEEP_TAGS
                  and len(token.form) == 1 and HANGUL.match(token.form))
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
