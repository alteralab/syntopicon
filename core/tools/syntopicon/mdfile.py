"""마크다운 파일 하나를 frontmatter + AST 사실들로 읽는다.

구조 형식의 파싱은 전부 파서가 한다 — md는 AST, YAML은 PyYAML(PLAN §3).
regex는 문자집합 검증(정규 언어 그 자체)에만 쓴다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

#: 방언 = CommonMark + GFM 부분집합(테이블·각주). 그 이상은 켜지 않는다.
#: linkify는 끈다 — 맨 URL의 자동 링크화는 규약에 없는 문법이고, 켜면
#: 본문에 적은 URL이 edges 파싱에 링크로 섞여 든다.
#:
#: 모듈 상수다(@cache 아님) — 입력이 없는 불변 설정 객체라 상태가 아니고,
#: 상태가 아닌 것은 상수 선언이 정직한 표현이다. 상태를 memoize하던 자리들
#: (layout·schemas·migrations)과 성격이 달라 제거가 아니라 상수화로 조치했다.
_PARSER = (
    MarkdownIt("commonmark")
    .enable("table")
    .use(front_matter_plugin)
    .use(footnote_plugin)
)


def parser() -> MarkdownIt:
    return _PARSER


def _walk(tokens: list[Token]) -> Iterator[Token]:
    for token in tokens:
        yield token
        if token.children:
            yield from _walk(token.children)


class FrontmatterError(ValueError):
    """frontmatter 자체가 읽히지 않는 경우 — 스키마 검증 이전 단계의 실패."""


@dataclass(frozen=True)
class Bullet:
    """목록 항목 하나. claim 불릿 검사(PLAN §4.3)의 단위다."""

    line: int              # 1-기준
    text: str
    cites: bool            # 각주로 출처를 달았는가
    pointer_only: bool     # 링크만 있는 항목 — 허브·목차의 포인터라 claim이 아니다
    link_led: bool         # 링크로 시작하는 항목 — 허브 문법 검사(§2.6)의 대상
    inherits_cite: bool    # 조상 불릿이 각주를 달았는가 — 하위 열거는 부모 각주 상속(§2.1)
    locator_before_cite: bool  # 각주 라벨 직전 텍스트가 locator 괄호로 닫히는가(§4.4-4)


@dataclass(frozen=True)
class Fence:
    """코드 펜스(또는 들여쓰기 코드 블록) 하나. 두 소비자가 있다 —
    형태소 색인의 제외 범위와, 출처 검사(SCHEMA.md §3 코드 표기)의 단위다."""

    line: int      # 1-기준 시작 줄
    end: int       # 1-기준 끝 줄(포함)
    sourced: bool  # 각주를 단 불릿 안에 들어 있는가 — 조상 상속 포함(§2.1)


@dataclass(frozen=True)
class MdFile:
    path: Path                       # 저장소 루트 기준
    frontmatter: dict | None         # None = frontmatter 블록 없음

    #: 각주 라벨. **참조와 정의가 짝을 이룬 것만 들어온다** — 실측 결과
    #: markdown-it의 각주 플러그인은 짝이 깨지면 참조·정의 양쪽 모두 토큰을 만들지
    #: 않고 평문으로 흘린다(GitHub 렌더링도 동일하게 `[^x]` 리터럴이 된다).
    #: 따라서 "정의 없는 참조"는 AST로 검출할 수 없고, regex로 잡는 것은 금지다(PLAN §3).
    #: 그 경우는 sources[]에 선언된 citekey가 여기 나타나지 않는 것으로 드러나므로
    #: kb-lint의 "각주↔sources.id 정합" 리포트가 담당한다(PLAN §4.3).
    footnote_labels: frozenset[str]

    links: tuple[str, ...]           # 본문 링크 href (코드 스팬은 제외됨 — AST가 구분)
    headings: tuple[tuple[int, int, str], ...]   # (레벨, 시작줄, 텍스트)
    bullets: tuple[Bullet, ...]

    #: 순수 텍스트 노드의 내용. 코드 스팬·코드 블록·링크 목적지는 들어오지 않는다 —
    #: AST가 이미 갈라 놓았기 때문이다. epistemic 토큰 검사가 이 위에서 돈다.
    texts: tuple[str, ...]

    line_count: int
    first_body_line: int             # frontmatter 다음 줄 (1-기준)

    #: 상단 인라인 TOC(`**목차**: …` 문단 — §2.6 형식 정본)의 시작 줄. 없으면 None.
    #: H1 이외의 첫 헤딩 이전까지만 본다 — TOC는 상단에 있어야 하기 때문이다.
    inline_toc_line: int | None

    #: HTML 블록의 줄 범위 (1-기준, 끝 포함). 주석은 사람에게 주는 지시지 본문이
    #: 아니므로 색인에서 뺀다 — 안 빼면 템플릿 주석이 모든 KB에서 거짓 히트를 낸다.
    html_ranges: tuple[tuple[int, int], ...]

    #: 코드 펜스. AST가 짚어 준 범위라 regex 파싱이 아니다(SCHEMA.md §3 코드 표기).
    fences: tuple[Fence, ...]

    @property
    def type(self) -> str | None:
        return (self.frontmatter or {}).get("type")


def _bullets_and_fences(tokens: list[Token]) -> tuple[list[Bullet], list[Fence]]:
    """목록 항목의 인라인 내용과 코드 펜스를 한 번에 모은다. 중첩 목록도 각각 하나로 센다.

    중첩은 open/close 짝의 스택으로 추적한다 — 하위 불릿의 각주 상속(§2.1)은
    조상 항목의 cites를 스택에서 읽는다. **펜스의 출처 판정도 같은 스택을 읽는다**:
    각주를 단 불릿 안에 들어 있으면 그 각주를 상속한다(SCHEMA.md §3). 두 산출물이
    같은 스택에 의존하므로 한 순회로 낸다 — 따로 걸으면 상속 규칙이 둘로 갈린다.
    """
    found = []
    fences: list[Fence] = []
    cite_stack: list[bool] = []
    for index, token in enumerate(tokens):
        if token.type == "list_item_close":
            if cite_stack:
                cite_stack.pop()
            continue
        if token.type in ("fence", "code_block") and token.map:
            fences.append(Fence(line=token.map[0] + 1, end=token.map[1],
                                sourced=any(cite_stack)))
            continue
        if token.type != "list_item_open":
            continue
        # 항목 안의 첫 문단이 그 항목의 진술이다. 그 뒤 중첩 목록은 자기 항목으로 다시 잡힌다.
        inline = next(
            (t for t in tokens[index + 1:index + 4] if t.type == "inline"), None
        )
        if inline is None:
            cite_stack.append(False)
            continue
        children = inline.children or []
        cites = any(child.type == "footnote_ref" for child in children)
        found.append(Bullet(
            line=(inline.map or [0])[0] + 1,
            text=inline.content,
            cites=cites,
            pointer_only=not _has_prose(children),
            link_led=_link_led(children),
            inherits_cite=any(cite_stack),
            locator_before_cite=_locator_before_cite(children),
        ))
        cite_stack.append(cites)
    return found, fences


def _link_led(children: list[Token]) -> bool:
    """항목이 링크로 시작하는가 — 허브·overview 링크 불릿 문법 검사의 대상 판별."""
    for child in children:
        if child.type == "link_open":
            return True
        if child.type == "text" and not child.content.strip():
            continue
        return False
    return False


def _locator_before_cite(children: list[Token]) -> bool:
    """모든 각주 라벨 직전 텍스트가 locator 괄호로 닫히는가(§4.4-4).

    검사는 괄호 존재까지만 — 괄호 안 내용(장·절·쪽)의 타당성은 판단 영역이라
    기계가 보지 않는다. 괄호와 라벨 사이 구두점은 **폐쇄 집합 `. , :`**(§4.4-4:
    마침표 `…(p.148).[^k]`·직인용 콜론 `…(p.152):[^k]`·문장 중간 쉼표
    `…(p.572),[^k]`) — 새 문자는 반례 발견 시 추가가 아니라 재심으로 넣는다.
    각주가 없는 항목은 참(공허하게 성립)이다.
    """
    ok = True
    last_text = ""
    for child in children:
        if child.type == "text":
            last_text = child.content
        elif child.type == "footnote_ref":
            if not last_text.rstrip(" :.,").endswith(")"):
                ok = False
            last_text = ""
    return ok


def _has_prose(children: list[Token]) -> bool:
    """링크 **바깥**에 실질 텍스트가 있는가.

    링크 안쪽 텍스트는 링크 레이블이지 진술이 아니다 — 이걸 세면 목차 항목과
    허브 포인터가 전부 "각주 없는 claim"으로 잡힌다.
    """
    depth = 0
    for child in children:
        if child.type == "link_open":
            depth += 1
        elif child.type == "link_close":
            depth -= 1
        elif child.type == "text" and depth == 0 and child.content.strip(" ·—-,.:"):
            return True
    return False


def heading_anchor(text: str) -> str:
    """GitHub 앵커 1개. 소문자화, 영숫자·공백·하이픈·언더스코어 외 제거, 공백을 하이픈으로.

    **공백은 하나씩 하이픈이 된다 — `\\s+` 접기 금지.** 구두점이 사라지면서 양쪽
    공백이 하이픈 둘로 남는 것(`제목 — 부제` → `제목--부제`)이 GitHub 실동작이고
    실측된 함정이다. 이 함수가 앵커 계산의 **유일한 구현**이다 — 색인(index_db)과
    검사(checks/page)가 따로 들고 있던 시절 `\\s+` 접기 차이로 갈라져, 엠대시 헤딩
    54개 파일의 색인 앵커가 전부 무효였다(2026-08-13 실측).
    """
    kept = "".join(c for c in text.lower() if c.isalnum() or c in " -_")
    return kept.replace(" ", "-")


def anchors_by_line(headings) -> dict[int, str]:
    """헤딩 시작 줄 → 최종 앵커. 같은 앵커가 반복되면 GitHub은 `-1`·`-2`를 덧붙인다 —
    그 순번은 **페이지 전체 헤딩 순서**로 매겨지므로 부분 집합(H2 이하만)으로
    계산하면 틀린다. 소비자는 여기서 전체를 받아 자기 줄만 골라 쓴다."""
    seen: dict[str, int] = {}
    anchors: dict[int, str] = {}
    for _, line, text in headings:
        base = heading_anchor(text)
        n = seen.get(base, 0)
        anchors[line] = base if n == 0 else f"{base}-{n}"
        seen[base] = n + 1
    return anchors


def page_anchors(headings) -> set[str]:
    """페이지의 실제 앵커 전부 — 앵커 링크 검증(lint)의 우변."""
    return set(anchors_by_line(headings).values())


def read(absolute: Path, relative: Path) -> MdFile:
    # BOM은 벗겨서 파싱한다 — 앞에 붙으면 frontmatter 구분선 인식이 통째로 죽어
    # "type 없음"이라는 엉뚱한 오류가 된다(적대 배터리 실측).
    source = absolute.read_text().removeprefix("\ufeff")
    tokens = parser().parse(source)
    nodes = list(_walk(tokens))

    frontmatter, first_body_line = None, 1
    if front := next((t for t in nodes if t.type == "front_matter"), None):
        loaded = yaml.safe_load(front.content)
        if not isinstance(loaded, dict):
            raise FrontmatterError("frontmatter가 매핑이 아닙니다")
        frontmatter = loaded
        first_body_line = (front.map or [0, 0])[1] + 1

    headings = [
        (int(token.tag.removeprefix("h")), (token.map or [0])[0] + 1, nodes[index + 1].content)
        for index, token in enumerate(nodes) if token.type == "heading_open"
    ]

    inline_toc_line = None
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag != "h1":
            break
        if token.type != "paragraph_open":
            continue
        inline = tokens[index + 1] if index + 1 < len(tokens) else None
        children = (inline.children or []) if inline is not None and inline.type == "inline" else []
        # 굵은 글씨 앞에 빈 text 토큰이 끼는 경우가 있다(파서 실측) — 비어 있으면 건너뛴다.
        meaningful = [c for c in children if not (c.type == "text" and not c.content.strip())]
        if (len(meaningful) >= 2 and meaningful[0].type == "strong_open"
                and meaningful[1].type == "text" and meaningful[1].content.strip() == "목차"):
            inline_toc_line = (token.map or [0])[0] + 1
            break

    bullets, fences = _bullets_and_fences(tokens)
    return MdFile(
        path=relative,
        frontmatter=frontmatter,
        footnote_labels=frozenset(t.meta["label"] for t in nodes if t.type == "footnote_ref"),
        links=tuple(t.attrs["href"] for t in nodes if t.type == "link_open" and "href" in t.attrs),
        headings=tuple(headings),
        bullets=tuple(bullets),
        texts=tuple(t.content for t in nodes if t.type == "text" and t.content.strip()),
        line_count=len(source.splitlines()),
        first_body_line=first_body_line,
        inline_toc_line=inline_toc_line,
        html_ranges=tuple(
            (t.map[0] + 1, t.map[1]) for t in tokens if t.type == "html_block" and t.map
        ),
        fences=tuple(fences),
    )
