"""마크다운 파일 하나를 frontmatter + AST 사실들로 읽는다.

구조 형식의 파싱은 전부 파서가 한다 — md는 AST, YAML은 PyYAML(PLAN §3).
regex는 문자집합 검증(정규 언어 그 자체)에만 쓴다.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Iterator

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin


@cache
def parser() -> MarkdownIt:
    """방언 = CommonMark + GFM 부분집합(테이블·각주). 그 이상은 켜지 않는다.

    linkify는 끈다 — 맨 URL의 자동 링크화는 규약에 없는 문법이고, 켜면
    본문에 적은 URL이 edges 파싱에 링크로 섞여 든다.
    """
    return (
        MarkdownIt("commonmark")
        .enable("table")
        .use(front_matter_plugin)
        .use(footnote_plugin)
    )


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

    #: HTML 블록의 줄 범위 (1-기준, 끝 포함). 주석은 사람에게 주는 지시지 본문이
    #: 아니므로 색인에서 뺀다 — 안 빼면 템플릿 주석이 모든 KB에서 거짓 히트를 낸다.
    html_ranges: tuple[tuple[int, int], ...]

    @property
    def type(self) -> str | None:
        return (self.frontmatter or {}).get("type")


def _bullets(tokens: list[Token]) -> list[Bullet]:
    """목록 항목의 인라인 내용을 모은다. 중첩 목록도 각각 하나로 센다."""
    found = []
    for index, token in enumerate(tokens):
        if token.type != "list_item_open":
            continue
        # 항목 안의 첫 문단이 그 항목의 진술이다. 그 뒤 중첩 목록은 자기 항목으로 다시 잡힌다.
        inline = next(
            (t for t in tokens[index + 1:index + 4] if t.type == "inline"), None
        )
        if inline is None:
            continue
        children = inline.children or []
        found.append(Bullet(
            line=(inline.map or [0])[0] + 1,
            text=inline.content,
            cites=any(child.type == "footnote_ref" for child in children),
            pointer_only=not _has_prose(children),
        ))
    return found


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

    return MdFile(
        path=relative,
        frontmatter=frontmatter,
        footnote_labels=frozenset(t.meta["label"] for t in nodes if t.type == "footnote_ref"),
        links=tuple(t.attrs["href"] for t in nodes if t.type == "link_open" and "href" in t.attrs),
        headings=tuple(headings),
        bullets=tuple(_bullets(tokens)),
        texts=tuple(t.content for t in nodes if t.type == "text" and t.content.strip()),
        line_count=len(source.splitlines()),
        first_body_line=first_body_line,
        html_ranges=tuple(
            (t.map[0] + 1, t.map[1]) for t in tokens if t.type == "html_block" and t.map
        ),
    )
