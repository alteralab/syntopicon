"""링크 재작성 — 파일을 다시 쓰지 않고 링크 목적지만 고친다.

왜 이런 모양인가: markdown-it은 인라인 토큰에 문자 오프셋을 주지 않는다(`map`은 블록
토큰만). 렌더러로 왕복시키면 파일 전체가 재작성돼 diff가 무의미해지고, 이는
"도구는 파일 통짜 load-save 금지"(PLAN §2.1)와 정면으로 어긋난다.

그래서 **AST가 위치와 개수를 정하고, 치환은 그 줄 범위 안에서만** 한다. 링크 목적지는
`](경로)` 문맥에서만 나타나므로 이 문맥을 노리고, AST가 센 링크 수와 텍스트에서 센
출현 수가 다르면 **아무것도 고치지 않고 실패한다**. 참조형 링크·꺾쇠 목적지·제목 붙은
링크처럼 이 문맥에 안 맞는 형태는 전부 그 불일치로 걸러져 사람에게 보고된다 —
조용히 망가뜨리느니 멈추는 편이 낫다.
"""

from __future__ import annotations

from dataclasses import dataclass

from markdown_it.token import Token

from .mdfile import parser


@dataclass(frozen=True)
class Ambiguity:
    """AST와 원문이 합의하지 않은 지점. 여기서 멈추고 사람에게 넘긴다."""

    line: int          # 1-기준
    found: int         # 원문에서 센 `](경로)` 출현 수
    expected: int      # AST가 센 해당 href의 링크 수


@dataclass(frozen=True)
class Rewrite:
    text: str
    changed: int
    ambiguities: tuple[Ambiguity, ...]

    @property
    def ok(self) -> bool:
        return not self.ambiguities


def _inline_blocks(tokens: list[Token]) -> list[Token]:
    """`inline` 토큰은 전부 최상위 목록에 있다 — markdown-it의 블록 토큰 열은 평면이고
    중첩은 _open/_close 쌍으로 표현된다. 인라인 안에 인라인이 들어가는 일은 없다."""
    return [t for t in tokens if t.type == "inline" and t.map]


def rewrite_links(source: str, old_href: str, new_href: str) -> Rewrite:
    """본문 링크 목적지 `old_href`를 `new_href`로 바꾼 텍스트를 돌려준다.

    한 곳이라도 모호하면 아무 곳도 고치지 않는다 — 부분 적용된 파일이 가장 나쁘다.
    """
    tokens = parser().parse(source)
    lines = source.splitlines(keepends=True)

    needle, replacement = f"]({old_href})", f"]({new_href})"
    changed = 0
    ambiguities: list[Ambiguity] = []

    for block in _inline_blocks(tokens):
        expected = sum(
            1 for child in (block.children or [])
            if child.type == "link_open" and child.attrs.get("href") == old_href
        )
        if not expected:
            continue

        start, end = block.map
        span = "".join(lines[start:end])
        found = span.count(needle)
        if found != expected:
            ambiguities.append(Ambiguity(line=start + 1, found=found, expected=expected))
            continue

        # 치환은 줄 수를 바꾸지 않으므로 이후 블록의 map이 그대로 유효하다.
        lines[start:end] = span.replace(needle, replacement).splitlines(keepends=True)
        changed += found

    if ambiguities:
        return Rewrite(text=source, changed=0, ambiguities=tuple(ambiguities))
    return Rewrite(text="".join(lines), changed=changed, ambiguities=())


def replace_section_body(source: str, heading: str, body: str) -> Rewrite:
    """`## <heading>` 절의 본문을 통째로 갈아끼운다. 헤딩 자체와 다른 절은 건드리지 않는다.

    라우터의 KB 목록처럼 **기계가 소유하는 절**에만 쓴다 — 파일시스템이 정본인 목록은
    누적 편집이 아니라 재생성이 맞고, 그래야 삭제된 KB가 남지 않는다.
    """
    tokens = parser().parse(source)
    lines = source.splitlines(keepends=True)

    for index, token in enumerate(tokens):
        if token.type != "heading_open" or tokens[index + 1].content.strip() != heading:
            continue
        level, start = int(token.tag.removeprefix("h")), token.map[1]
        end = next(
            (t.map[0] for t in tokens[index + 1:]
             if t.type == "heading_open" and int(t.tag.removeprefix("h")) <= level),
            len(lines),
        )
        lines[start:end] = (body if body.endswith("\n") else body + "\n").splitlines(keepends=True)
        return Rewrite(text="".join(lines), changed=1, ambiguities=())

    raise LookupError(f"'{heading}' 절을 찾지 못했습니다")


def rewrite_frontmatter_path(source: str, old_path: str, new_path: str) -> Rewrite:
    """frontmatter의 저장소 루트 기준 경로만 바꾼다 — YAML 라운드트립은 하지 않는다.

    PyYAML로 load-save하면 주석·따옴표·키 순서가 전부 재작성된다(PLAN §2.1).
    front_matter 토큰의 줄 범위 안에서 경로 문자열만 교체하고, 출현 수가 예상과
    다르면 실패한다.
    """
    tokens = parser().parse(source)
    block = next((t for t in tokens if t.type == "front_matter" and t.map), None)
    if block is None:
        return Rewrite(source, 0, ())

    start, end = block.map
    lines = source.splitlines(keepends=True)
    span = "".join(lines[start:end])
    found = span.count(old_path)
    if not found:
        return Rewrite(source, 0, ())

    lines[start:end] = [span.replace(old_path, new_path)]
    return Rewrite("".join(lines), found, ())
