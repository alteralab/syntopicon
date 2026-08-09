#!/usr/bin/env python3
"""kb-plain 검사기 — 사람이 읽는 산출물의 금지 기호와 비승인 어휘를 검출한다.

대상은 커밋되는 KB 페이지가 아니라 세션 산출물(리뷰 양식, kb-query --plain 답변,
브리핑)이다. 규칙 정본은 .agents/skills/kb-plain/SKILL.md, 어휘 정본은 같은 곳의
lexicon.txt — 검출만 하고 수정은 저자가 한다.

구현 규약(PLAN §3): md 구조는 markdown-it-py 파서로 읽는다 — blockquote와 code는
AST로 식별해 제외한다(원문 인용은 규칙의 예외). 검출은 정확 문자·정확 문자열
대조만 쓰고 regex를 쓰지 않는다(패턴 증식 금지). lexicon이 없거나 형식을 모르면
건너뛰지 않고 실패한다.

사용: uv run tools/plaincheck.py <파일>...   # 인자가 없으면 stdin
종료: 위반 있으면 1, 없으면 0, 입력·lexicon 문제는 2.
"""

import sys
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
LEXICON = ROOT / ".agents" / "skills" / "kb-plain" / "lexicon.txt"

# 규칙 1(엠대시·가운뎃점)과 규칙 2 중 기계 판정 가능한 화살표. 정확 문자 대조.
BANNED = {
    "—": ("엠대시", "쉼표, 마침표, 괄호, 줄바꿈으로 바꾼다"),
    "·": ("가운뎃점", "쉼표로 바꾼다"),
    "ㆍ": ("가운뎃점", "쉼표로 바꾼다"),
    "→": ("화살표", "완결 문장으로 푼다"),
}


def load_lexicon(path: Path):
    """'# error'/'# warn' 섹션의 `표현[<TAB>대체어]` 목록. 모르는 형식은 실패."""
    if not path.exists():
        print(f"lexicon 없음: {path}", file=sys.stderr)
        raise SystemExit(2)
    errors: dict[str, str] = {}
    warns: list[str] = []
    section = None
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if line == "# error":
            section = "error"
            continue
        if line == "# warn":
            section = "warn"
            continue
        if not line or line.startswith("#"):
            continue
        if section is None:
            print(f"{path}:{lineno}: 섹션 밖의 항목 — 형식을 모르면 실패한다", file=sys.stderr)
            raise SystemExit(2)
        term, tab, alt = raw.partition("\t")
        term = term.strip()
        if section == "error":
            errors[term] = alt.strip() if tab else ""
        else:
            warns.append(term)
    return errors, warns


def visible_segments(text: str):
    """(줄 번호, 텍스트) 목록 — blockquote 안과 code를 AST로 제외한, 사람이 읽는 조각.

    html_block(양식의 주석 포함)도 검사 대상에 넣는다 — 리뷰 양식은 raw md로
    읽히므로 주석도 사람이 읽는 표면이다. inline이 여러 줄에 걸치면 줄 번호는
    시작 줄로 근사한다.
    """
    tokens = MarkdownIt("commonmark").parse(text)
    segs: list[tuple[int, str]] = []
    depth = 0
    for tok in tokens:
        if tok.type == "blockquote_open":
            depth += 1
        elif tok.type == "blockquote_close":
            depth -= 1
        elif depth > 0:
            continue
        elif tok.type == "html_block":
            base = tok.map[0] + 1 if tok.map else 0
            for i, ln in enumerate(tok.content.splitlines()):
                segs.append((base + i, ln))
        elif tok.type == "inline":
            line = tok.map[0] + 1 if tok.map else 0
            parts = [c.content for c in (tok.children or []) if c.type == "text"]
            if parts:
                segs.append((line, " ".join(parts)))
    return segs


def check(name: str, text: str, errors: dict, warns: list):
    found_err: list[str] = []
    found_warn: list[str] = []
    for line, seg in visible_segments(text):
        for ch, (label, fix) in BANNED.items():
            if ch in seg:
                found_err.append(f"{name}:{line}: 금지 기호 {label}({ch}): {fix}")
        for term, alt in errors.items():
            if term in seg:
                hint = f" (대체어: {alt})" if alt else ""
                found_err.append(f"{name}:{line}: 비승인 어휘 '{term}'{hint}")
        for term in warns:
            if term in seg:
                found_warn.append(f"{name}:{line}: 재고 권고 '{term}'")
    return found_err, found_warn


def main(argv: list[str]) -> int:
    errors, warns = load_lexicon(LEXICON)
    inputs: list[tuple[str, str]] = []
    if argv:
        for a in argv:
            p = Path(a)
            if not p.is_file():
                print(f"파일 없음: {a}", file=sys.stderr)
                return 2
            inputs.append((a, p.read_text(encoding="utf-8")))
    else:
        inputs.append(("<stdin>", sys.stdin.read()))

    n_err = n_warn = 0
    for name, text in inputs:
        found_err, found_warn = check(name, text, errors, warns)
        for msg in found_err:
            print(msg)
        for msg in found_warn:
            print(f"warn: {msg}")
        n_err += len(found_err)
        n_warn += len(found_warn)
    print(f"위반 {n_err}건, 권고 {n_warn}건")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
