"""페이지 본문 검사 — 데이터 소스는 md AST(MdFile).

코퍼스 검사(@check)와 실행 구조가 다르다: 증분 실행에서 변경된 페이지만 돌므로
lint CLI가 페이지 루프에서 직접 부른다.
"""

from __future__ import annotations

import re
from urllib.parse import unquote

from ..mdfile import MdFile, page_anchors
from .base import Context, Finding, kind
from .provenance import check_progress, check_snapshot

# PLAN이 규정한 것: 500줄 백스톱·100줄 TOC(§2.6). 나머지는 자체 상수이고,
# PLAN §6대로 운영 데이터로 보정할 자리다.
PAGE_LINE_BACKSTOP = 500
TOC_REQUIRED_ABOVE = 100
MAX_HEADING_DEPTH = 4          # H4가 필요해지면 분할 신호(§2.6, 자체 휴리스틱)

# 본문 인라인 토큰. AST가 "코드도 링크도 아닌 텍스트"까지 갈라 준 **뒤에** 그 텍스트
# 안에서 어휘를 보는 것이라, PLAN §3이 허용한 정규 언어 검증에 해당한다.
EPISTEMIC_TOKEN = re.compile(r"(?<![\w#])#([a-z][a-z0-9-]*)")
WIKILINK = re.compile(r"!?\[\[[^\]]+\]\]")

kind("page-too-long", "warn", "500줄 백스톱 초과",
     "500줄은 백스톱이지 분할 기준이 아니다. 1차 완화는 TOC + 섹션 앵커이고, "
     "분할은 '한 페이지 = 하나의 질문'이 깨졌을 때만 한다.")
kind("toc-missing", "info", "100줄 초과인데 상단 TOC 부재",
     "H1 바로 아래에 링크 불릿 목차를 단다(§2.6).")
kind("heading-h1", "warn", "H1이 하나가 아님",
     "H1은 파일당 하나로 정리한다.")
kind("heading-skip", "warn", "헤딩 레벨 건너뛰기",
     "중간 레벨을 채우거나 깊이를 조정한다.")
kind("heading-depth", "info", "H4 초과 깊이",
     "깊이가 필요해졌다는 것 자체가 분할 신호다(§2.6).")
kind("anchor-broken", "warn", "페이지 안 앵커가 실제 헤딩과 불일치",
     "헤딩에서 앵커를 다시 딴다 — 구두점 주변 공백이 하이픈 둘로 남는 함정이 흔하다.")
kind("source-uncited", "warn", "선언했지만 인용되지 않는 소스",
     "죽은 소스 항목이거나 각주 정의 누락이다 — 후자면 본문에 [^…]가 평문으로 "
     "남아 있고 validate는 그것을 못 본다.")
kind("claim-unfootnoted", "info", "각주 없는 claim 불릿",
     "각주+locator를 달거나, claim이 아니면 산문으로 옮긴다. 링크로 시작하는 "
     "불릿은 포인터 문법(§2.6)이라 검사 대상이 아니다.")
kind("locator-missing", "info", "각주 앞 locator 괄호 부재",
     "각주 라벨 직전에 (장·절·쪽) 괄호를 단다 — claim은 각주+locator(§4.4-4).")
kind("code-unsourced", "warn", "각주 달린 claim 밖의 코드 펜스",
     "펜스를 각주 달린 claim 아래로 옮기고, 소스에 없는 코드면 지운다 — "
     "출처 없는 코드는 예제가 아니라 발명한 claim이다.")
kind("hub-grammar", "warn", "설명 없는 링크 불릿(허브 문법 위반)",
     "`- [제목](경로) — 한 줄 설명` 꼴로 설명을 단다(§2.6).")
kind("inline-dollar-math", "warn", "달러 기호 인라인 수식",
     "문장 속 기호는 유니코드 + 이름 병기, 여러 줄은 ```math 펜스로 바꾼다.")
kind("epistemic-token", "warn", "미정의 해시 토큰",
     "폐쇄 어휘는 #hypothesis·#speculation뿐이다 — 오타를 고치거나 토큰을 지운다"
     "(태그 체계 없음).")
kind("wikilink", "warn", "Obsidian 전용 위키링크 문법",
     "GFM 인라인 링크로 바꾼다 — 이 저장소는 GFM 부분집합만 쓴다.")


def check_page(ctx: Context, path: str, md: MdFile):
    meta = ctx.meta.get(path)
    if meta is None:
        return
    kb, front = meta["kb"], md.frontmatter or {}

    if md.line_count > PAGE_LINE_BACKSTOP:
        yield Finding("page-too-long",
                      f"{md.line_count}줄 — 분할 판단은 목적 기준으로(§2.6). "
                      "1차 완화책은 분할이 아니라 TOC + 섹션 앵커", kb, path)
    if md.line_count > TOC_REQUIRED_ABOVE and not _has_toc(md):
        yield Finding("toc-missing", f"{md.line_count}줄인데 상단 TOC가 없습니다", kb, path)

    yield from _check_headings(kb, path, md)

    # 페이지 안 앵커 링크(`](#…)`)가 실제 헤딩을 가리키는가. rename은 앵커를 재작성하지
    # 않으므로(PLAN §2.5-2) 여기가 유일한 검출 지점이다. 클릭해도 안 움직이는 링크는
    # 렌더도 성공하고 validate도 통과해서 조용히 남는다.
    anchors = page_anchors(md.headings)
    for href in md.links:
        if not href.startswith("#"):
            continue
        # markdown-it이 링크 목적지를 퍼센트 인코딩한다 — 한글 앵커는 디코드해야 비교된다.
        target = unquote(href[1:])
        if target not in anchors:
            yield Finding("anchor-broken",
                          f"#{target} 가 이 페이지의 헤딩과 맞지 않습니다 — "
                          f"구두점 주변 공백이 하이픈 둘로 남는 경우가 흔합니다", kb, path)

    # 각주 = 출처 귀속 전용 채널이므로, 선언한 소스가 인용되지 않으면 둘 중 하나다:
    # 죽은 소스 항목이거나, 정의가 빠져 평문이 된 각주(validate가 못 보는 그 경우).
    declared = {s["id"] for s in front.get("sources", []) if isinstance(s, dict) and "id" in s}
    for unused in sorted(declared - md.footnote_labels):
        yield Finding("source-uncited",
                      f"sources에 {unused} 를 선언했지만 각주가 없습니다 "
                      "(각주 정의 누락이면 본문에 [^…] 가 평문으로 남아 있습니다)", kb, path)

    if front.get("type") == "concept":
        for bullet in md.bullets:
            # 하위 열거 불릿은 부모 불릿의 각주를 상속하고(§2.1), 링크로 시작하는
            # 불릿은 claim이 아니라 포인터 문법이다(§2.6) — "이어지는 페이지" 절의
            # `- [제목](경로) — 설명` 꼴이 허브 문법으로는 필수이면서 여기서는
            # 위반으로 찍히던 것이 리포트의 84%(649/769)를 채운 오검출이었다.
            if (not bullet.cites and not bullet.pointer_only
                    and not bullet.inherits_cite and not bullet.link_led):
                yield Finding("claim-unfootnoted",
                              f"{bullet.line}행: {bullet.text[:40]}…", kb, path)
            if bullet.cites and not bullet.locator_before_cite:
                yield Finding("locator-missing",
                              f"{bullet.line}행: 각주 앞에 locator 괄호가 없습니다 — "
                              f"claim은 각주+locator(§4.4-4)", kb, path)

        # 코드 펜스는 각주 달린 claim 아래에 있어야 한다(SCHEMA.md §3). 소스에 없는
        # 코드를 지어내면 예제가 아니라 발명한 claim이고, 문법이 맞으면 그럴듯해
        # 보여서 산문보다 눈에 안 띈다. 검사 대상은 소속뿐 — 코드가 정말 그 소스에서
        # 왔는지는 기계가 못 본다(리뷰 양식이 담당).
        for fence in md.fences:
            if not fence.sourced:
                yield Finding("code-unsourced",
                              f"{fence.line}행: 코드 펜스가 각주 달린 claim 밖에 "
                              f"있습니다 — 출처 없는 코드는 넣지 않는다(§3)", kb, path)

    # 허브·overview 링크 불릿 문법(§2.6): 링크로 시작하는 불릿은 한 줄 설명을 진다.
    if front.get("type") in ("synthesis", "guide"):
        for bullet in md.bullets:
            if bullet.link_led and bullet.pointer_only:
                yield Finding("hub-grammar",
                              f"{bullet.line}행: 링크 불릿에 설명이 없습니다 — "
                              f"`- [제목](경로) — 한 줄 설명`(§2.6)", kb, path)

    for text in md.texts:
        if _inline_dollar_math(text):
            yield Finding("inline-dollar-math",
                          "`$…$` 인라인 수식은 쓰지 않습니다 — 문장 속 기호는 유니코드 + "
                          "이름 병기, 여러 줄은 ```math 펜스(SCHEMA.md §3). "
                          "어느 md 스펙에도 없어 파서가 백슬래시를 먹습니다", kb, path)
        for token in EPISTEMIC_TOKEN.findall(text):
            if token not in ctx.epistemic:
                yield Finding("epistemic-token",
                              f"미정의 토큰 #{token} — 폐쇄 어휘는 "
                              f"{sorted(ctx.epistemic)} 뿐입니다(태그 체계 없음)", kb, path)
        if match := WIKILINK.search(text):
            yield Finding("wikilink",
                          f"Obsidian 전용 문법 {match.group()} — GFM 부분집합만 씁니다", kb, path)

    yield from check_snapshot(kb, path, front)
    yield from check_progress(kb, path, front, ctx.progress_validator)


def _inline_dollar_math(text: str) -> bool:
    """`$…$` 인라인 수식이 있는가. 통화(`$50`)와 가르는 것이 이 함수의 존재 이유다.

    판별은 pandoc 규칙(MANUAL "Math"): 여는 `$`는 **바로 오른쪽이 공백이 아니어야**
    하고, 닫는 `$`는 **바로 왼쪽이 공백이 아니고 바로 오른쪽이 숫자가 아니어야** 한다.
    이 셋이 통화 오식별을 막는 유일하게 성문된 처방이고(jgm이 cmark#439에서 요구한
    바로 그 규칙), 실측에서 이 저장소 282파일에 오탐 0건이었다.

    입력은 AST의 순수 텍스트 노드다 — 코드 스팬·코드 펜스·링크 목적지는 이미 빠져
    있으므로 여기서 다시 가르지 않는다(파서 우선, PLAN §3).
    """
    opens = [
        i for i, ch in enumerate(text)
        if ch == "$" and i + 1 < len(text) and not text[i + 1].isspace()
    ]
    for start in opens:
        for end in range(start + 1, len(text)):
            if text[end] != "$":
                continue
            left_ok = not text[end - 1].isspace()
            right_ok = end + 1 >= len(text) or not text[end + 1].isdigit()
            if left_ok and right_ok:
                return True
            break          # 첫 후보가 닫기 조건을 못 채우면 이 여는 기호는 버린다
    return False


def _has_toc(md: MdFile) -> bool:
    """`**목차**:` 인라인 문단 또는 H2 앞 포인터 불릿 목록을 TOC로 본다.

    §2.6의 현행 정본은 링크 불릿 목록이다(2026-08-11 전환). 인라인 문단형은
    폐기됐으나 잔존 코퍼스 호환으로 아직 인정한다 — 형식 검사 강화는 규칙 집세
    심사(P5)에서 판정한다.
    """
    if md.inline_toc_line is not None:
        return True
    first_h2 = next((line for level, line, _ in md.headings if level == 2), md.line_count)
    return any(bullet.line < first_h2 and bullet.pointer_only for bullet in md.bullets)


def _check_headings(kb: str, path: str, md: MdFile):
    levels = [level for level, _, _ in md.headings]
    if levels.count(1) != 1:
        yield Finding("heading-h1", f"H1이 {levels.count(1)}개입니다 (파일당 하나)", kb, path)
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            yield Finding("heading-skip",
                          f"H{previous} 다음에 H{current} — 레벨 건너뛰기", kb, path)
            break
    if deepest := max((lvl for lvl in levels if lvl > MAX_HEADING_DEPTH), default=0):
        yield Finding("heading-depth",
                      f"H{deepest}까지 내려갑니다 — 분할 신호(§2.6)", kb, path)
