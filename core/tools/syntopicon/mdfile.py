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
    headings: tuple[tuple[int, str], ...]  # (레벨, 텍스트)

    @property
    def type(self) -> str | None:
        return (self.frontmatter or {}).get("type")


def read(absolute: Path, relative: Path) -> MdFile:
    tokens = parser().parse(absolute.read_text())
    nodes = list(_walk(tokens))

    frontmatter = None
    if raw := next((t.content for t in nodes if t.type == "front_matter"), None):
        loaded = yaml.safe_load(raw)
        if not isinstance(loaded, dict):
            raise FrontmatterError("frontmatter가 매핑이 아닙니다")
        frontmatter = loaded

    headings: list[tuple[int, str]] = []
    for index, token in enumerate(nodes):
        if token.type == "heading_open":
            level = int(token.tag.removeprefix("h"))
            headings.append((level, nodes[index + 1].content))

    return MdFile(
        path=relative,
        frontmatter=frontmatter,
        footnote_labels=frozenset(t.meta["label"] for t in nodes if t.type == "footnote_ref"),
        links=tuple(t.attrs["href"] for t in nodes if t.type == "link_open" and "href" in t.attrs),
        headings=tuple(headings),
    )
