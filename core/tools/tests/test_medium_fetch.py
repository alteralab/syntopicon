"""medium_fetch의 순수 함수 — 링크 오프셋 산수와 문단 대응표.

네트워크·CDP 경로는 여기서 다루지 않는다(라이브 Chrome이 필요한 통합 검증은
스킬 절차의 실측 몫). 여기서 고정하는 것은 틀리기 쉬운 두 가지다:
UTF-16 코드 유닛 오프셋(이모지에서 코드 포인트 인덱스와 갈라진다)과,
대응표 밖 문단 타입이 조용히 사라지지 않는다는 계약.
"""

from medium_fetch import apply_links, paragraph_to_md


def test_링크가_인라인된다():
    out = apply_links("read the docs now", [{"start": 9, "end": 13, "href": "https://e.co"}])
    assert out == "read the [docs](https://e.co) now"


def test_오프셋은_utf16_코드_유닛이다():
    # '😀'(U+1F600)는 UTF-16에서 2유닛 — 코드 포인트로 세면 링크가 한 칸 밀린다.
    text = "😀 docs here"
    out = apply_links(text, [{"start": 3, "end": 7, "href": "https://e.co"}])
    assert out == "😀 [docs](https://e.co) here"


def test_겹치는_링크는_꼬리로_밀린다():
    out = apply_links("abcdef", [
        {"start": 0, "end": 4, "href": "https://a.co"},
        {"start": 2, "end": 6, "href": "https://b.co"},
    ])
    assert out == "[abcd](https://a.co)ef (링크: https://b.co)"


def test_범위_밖_오프셋은_본문을_망치지_않는다():
    out = apply_links("ab", [{"start": 1, "end": 9, "href": "https://a.co"}])
    assert out == "ab (링크: https://a.co)"


def test_문단_대응표():
    assert paragraph_to_md({"type": "H3", "text": "제목"}) == "### 제목"
    assert paragraph_to_md({"type": "BQ", "text": "인용"}) == "> 인용"
    assert paragraph_to_md({"type": "OLI", "text": "항목"}) == "1. 항목"
    assert paragraph_to_md({"type": "PRE", "text": "x = 1", "lang": "python"}) \
        == "```python\nx = 1\n```"


def test_PRE_본문에는_링크를_삽입하지_않는다():
    # 코드 안에 md 링크 문법이 들어가면 코드가 망가진다 — 원문 그대로.
    out = paragraph_to_md({"type": "PRE", "text": "curl docs", "lang": None,
                           "markups": [{"start": 5, "end": 9, "href": "https://e.co"}]})
    assert out == "```\ncurl docs\n```"


def test_미지원_타입은_마커로_남는다():
    out = paragraph_to_md({"type": "NEWTYPE", "text": "본문"})
    assert "미지원 문단 타입 NEWTYPE" in out and "본문" in out
