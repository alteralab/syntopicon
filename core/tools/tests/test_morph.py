"""형태소 레그. 이 레그의 존재 이유가 질의 대칭이라, 대칭이 깨지는 경우를 먼저 본다."""

from __future__ import annotations

import sqlite3

import pytest

from conftest import Repo
from test_validate import DDIA, SOURCE, concept

pytest.importorskip("kiwipiepy", reason="Tier B — uv sync --group index")

from syntopicon import morph  # noqa: E402


def test_POS_필터가_조사와_어미를_버린다():
    assert morph.analyze("복제 지연은 읽기 일관성을 깨뜨린다") == \
        ["복제", "지연", "읽", "일관", "깨뜨리"]


def test_nori_STOP_TAGS와_교집합이_없다():
    """PLAN §4.1의 "nori STOP_TAGS 정합" — Lucene 소스에서 확인한 30개.

    이 검사의 사각지대를 함께 못박아 둔다: nori에 대응물이 없는 태그(Kiwi 독자
    W_* 계열)는 교집합에 걸릴 수 없어 **원리적으로 검출되지 않는다**. 실제로
    W_HASHTAG 침묵 폐기가 이 검사를 통과한 채 14개 페이지를 검색 불가로 만들었다.
    그 부류는 아래 소비자 기반 검사가 담당한다.
    """
    nori_stop = {
        "EP", "EF", "EC", "ETN", "ETM", "IC", "JKS", "JKC", "JKG", "JKO", "JKB",
        "JKV", "JKQ", "JX", "JC", "MAG", "MAJ", "MM", "SP", "SSC", "SSO", "SC",
        "SE", "XPN", "XSA", "XSN", "XSV", "UNA", "NA", "VSV",
    }
    assert morph.KEEP_TAGS & nori_stop == set()
    assert not any(tag.startswith("W_") for tag in nori_stop)


def test_epistemic_폐쇄어휘가_색인에서_살아남는다():
    """`#hypothesis`/`#speculation`은 schema/vocabulary.yaml이 정의한 폐쇄 어휘다
    (PLAN §2.1). Kiwi가 통짜 W_HASHTAG로 무는 탓에 알맹이 `hypothesis`조차 SL로
    떨어지지 않아, KEEP_TAGS에서 빠지면 태그를 단 페이지 전부가 검색 0건이 된다
    (2026-08-11 실측: 14개 페이지 중 0건). 소비자가 있는 태그 부류의 회귀 방지."""
    for token in ("#hypothesis", "#speculation"):
        assert token in morph.analyze(f"이 주장은 {token} 이다"), \
            f"{token}이 색인에서 빠졌습니다"
        assert token in morph.index_text(f"근거가 얇다 {token}").split()
        assert f'"{token}"' in morph.query_expression(token)


def test_질의와_색인이_같은_함수를_지난다():
    """본문은 `읽 일관`으로 들어간다. 질의가 원형으로 가면 영원히 맞지 않는다."""
    indexed = morph.index_text("읽기 일관성을 보장한다")
    for term in morph.analyze("읽기 일관성"):
        assert term in indexed.split()


def test_낱말끼리는_OR_복합어만_phrase():
    """질의 전체 phrase는 recall 0.0(멀티홉 하네스 실측), 암묵 AND는 기능어
    형태소("어떻게"·"정해지나") 하나가 본문에 없으면 전멸시킨다 — qrels 26문항
    실측으로 OR+bm25가 전 클래스 우세(R@5 0.288→0.763). 홑항도 인용된다 —
    비인용 토큰은 FTS5 연산자(AND/OR/NOT)에 노출되기 때문."""
    assert morph.query_expression("읽기 일관성") == '"읽" OR "일관"'
    assert morph.query_expression("복제지연") == '"복제 지연"'       # 복합어 → phrase
    assert morph.query_expression("복제지연 읽기") == '"복제 지연" OR "읽"'


def test_불규칙_용언_어간을_버리지_않는다():
    """Kiwi는 불규칙 어간에 VV-I·VA-I 태그를 붙인다. 접미를 떼지 않으면 긋다·걷다·
    듣다·돕다·어렵다가 통째로 색인에서 빠진다 — 첫 실제 콘텐츠에서 발견된 구멍이다."""
    for word, stem in [("긋는다", "긋"), ("걷는다", "걷"), ("듣는다", "듣"),
                       ("돕는다", "돕"), ("어렵다", "어렵"), ("아름답다", "아름답")]:
        assert stem in morph.analyze(word), f"{word}의 어간 {stem}이 빠졌습니다"
    assert morph.base_tag("VV-I") == "VV" and morph.base_tag("VV") == "VV"


def test_활용형과_조사_변형이_같은_형태로_모인다():
    for variant in ("복제가", "복제를", "복제는", "복제로"):
        assert morph.analyze(variant) == ["복제"]


def test_NFD_본문과_NFC_질의가_만난다():
    """macOS 도구가 만든 NFD 본문은 바이트가 달라 검색 0건이 되던 버그의 회귀 방지 —
    색인·질의 공용 분석 지점에서 NFC 정규화."""
    import unicodedata
    nfd = unicodedata.normalize("NFD", "골든 소스")
    assert morph.analyze(nfd) == morph.analyze("골든 소스")
    assert morph.index_text(nfd) == morph.index_text("골든 소스")


def test_질의의_모든_항은_인용된다():
    """비인용 토큰은 FTS5 문법에 노출된다 — AND/OR/NOT이 연산자로 해석돼
    크래시하던 버그의 회귀 방지. 인용은 그 클래스 전체를 없앤다."""
    import re
    assert morph.query_expression("AND") == '"AND"'
    expression = morph.query_expression("복제지연 OR checksum")
    # phrase 안에 공백이 있으므로 공백 split이 아니라 전체 형태로 검사한다
    assert re.fullmatch(r'"[^"]+"( OR "[^"]+")*', expression), expression


def test_파편화를_관측한다():
    assert morph.fragments("정상적인 문장이다") == []
    found = morph.fragments("가 나 다 라")
    assert found and found[0].surface == "가나다라"


def test_섹션으로_자르고_HTML_주석은_뺀다(tmp_path):
    from pathlib import Path as P
    from syntopicon.mdfile import read
    text = ("---\ntype: concept\n---\n\n# 제목\n\n머리말\n\n"
            "## 첫 절\n\n<!-- 이 주석의 복제 라는 낱말은 색인되면 안 된다 -->\n\n내용\n\n"
            "## 둘째 절\n\n내용2\n")
    path = tmp_path / "s.md"
    path.write_text(text)
    md = read(path, P("s.md"))
    got = list(morph.sections(text, md))
    assert [(title, line) for title, line, _, _ in got] == [(None, 4), ("첫 절", 9), ("둘째 절", 15)]
    assert "복제" not in got[1][2], "HTML 주석이 섹션 본문에 남았습니다"


def test_코드_펜스는_원문에_남고_색인에서만_빠진다(tmp_path):
    """스니펫에는 코드가 보여야 하고(사람이 복사한다), 색인에는 들어가면 안 된다 —
    FTS5 BM25의 길이 정규화가 행 전체 토큰 수를 쓰므로 코드 토큰이 같은 절의 산문
    점수를 깎는다(2026-08-11 실측: 펜스가 든 절 5건 전부 하락, 1건은 1위 상실).
    HTML 블록과 달리 **원문에서는 지우지 않는다**는 것이 이 검사의 요지다."""
    from pathlib import Path as P
    from syntopicon.mdfile import read
    text = ("---\ntype: concept\n---\n\n# 제목\n\n## 절\n\n복제 지연을 줄이는 설정이다.\n\n"
            "```sql\nSELECT customer_id FROM orders WHERE paid = 1;\n```\n\n끝.\n")
    path = tmp_path / "c.md"
    path.write_text(text)
    md = read(path, P("c.md"))
    assert md.fences, "AST가 펜스 범위를 짚지 못했습니다"
    (_, _, section_raw, prose), = [s for s in morph.sections(text, md) if s[0] == "절"]
    assert "SELECT" in section_raw, "원문에서 코드가 사라졌습니다 — 스니펫이 비게 됩니다"
    assert "SELECT" not in prose and "customer_id" not in prose
    assert "복제" in prose and "복제" in section_raw
    assert "SELECT" not in morph.index_text(prose)


def test_앵커는_GitHub_규칙을_따른다():
    """앵커 계산의 유일한 구현은 mdfile이다 — 색인과 검사가 사본을 따로 들던 시절
    `\\s+` 접기 차이로 갈라져 엠대시 헤딩 54개 파일의 색인 앵커가 무효였다."""
    from syntopicon.mdfile import anchors_by_line, heading_anchor, page_anchors

    assert heading_anchor("읽기와 quorum") == "읽기와-quorum"
    assert heading_anchor("5.4 절: 읽기 경로") == "54-절-읽기-경로"
    # 구두점 양쪽 공백은 하이픈 둘로 남는다 — 접으면 GitHub과 갈라진다(실측 함정).
    assert heading_anchor("acks — 내구성의 다이얼") == "acks--내구성의-다이얼"

    headings = ((1, 1, "제목"), (2, 5, "같은 절"), (2, 9, "같은 절"))
    assert anchors_by_line(headings) == {1: "제목", 5: "같은-절", 9: "같은-절-1"}
    assert page_anchors(headings) == {"제목", "같은-절", "같은-절-1"}


def test_색인_앵커도_같은_구현을_쓴다(repo: Repo):
    """엠대시 헤딩의 색인 앵커에 하이픈 둘이 남아야 한다 — 사본 시절의 회귀 감시."""
    import sqlite3

    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/producer-acks.md", concept(
        body=f"\n## acks — 내구성의 다이얼\n\n응답 조건을 고른다.[^{DDIA}]\n"
             f"\n[^{DDIA}]: 3장\n"))
    repo.run("reindex.py")

    with sqlite3.connect(repo.root / "derived.sqlite") as db:
        anchors = {row[0] for row in db.execute(
            "SELECT anchor FROM morph WHERE anchor IS NOT NULL")}
    assert "acks--내구성의-다이얼" in anchors


# ── CLI ──────────────────────────────────────────────────────────────────────

def indexed(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/replication-lag.md", concept(
        body=f"\n## 읽기 일관성\n\n복제 지연은 읽기 일관성을 깨뜨린다.[^{DDIA}]\n"
             f"\n[^{DDIA}]: Kleppmann 2017, 5장\n"))
    repo.run("reindex.py")


def test_조사가_붙은_질의가_본문을_찾는다(repo: Repo):
    indexed(repo)
    result = repo.run("ksearch.py", "복제 지연이")     # 본문은 "복제 지연은"
    assert result.returncode == 0
    assert "it/concepts/replication-lag.md#읽기-일관성" in result.stdout
    assert "1건" in result.stdout


def test_스니펫은_형태소가_아니라_원문을_보여준다(repo: Repo):
    indexed(repo)
    result = repo.run("ksearch.py", "일관성")
    assert "복제 지연은 읽기 일관성을 깨뜨린다" in result.stdout
    assert "읽 일관" not in result.stdout.split("분석된 질의")[0]


def test_KB로_좁힌다(repo: Repo):
    indexed(repo)
    assert "0건" in repo.run("ksearch.py", "복제", "--kb", "ops").stdout
    assert "1건" in repo.run("ksearch.py", "복제", "--kb", "it").stdout


def test_inbox_결과에는_unreviewed_라벨이_붙는다(repo: Repo):
    """검역의 "보이는 저하"(PLAN §4.4 쓰기 정책 ①) — AfC의 실패 기전이 hiddenness였다.
    inbox도 검색에 나오되, 리뷰 전임이 결과 줄에서 바로 보여야 한다."""
    indexed(repo)
    repo.write("it/inbox/quorum-read.md", concept(
        status="draft",
        body=f"\n## 정족수\n\n정족수 읽기는 복제 지연을 가린다.[^{DDIA}]\n"
             f"\n[^{DDIA}]: Kleppmann 2017, 5장\n"))
    repo.run("reindex.py")

    result = repo.run("ksearch.py", "복제 지연")
    inbox_lines = [l for l in result.stdout.splitlines() if l.startswith("it/inbox/")]
    concept_lines = [l for l in result.stdout.splitlines() if l.startswith("it/concepts/")]
    assert inbox_lines and all("[unreviewed]" in l for l in inbox_lines)
    assert concept_lines and all("[unreviewed]" not in l for l in concept_lines)


def test_문맥_민감_활용형_질의가_색인과_만난다():
    """Kiwi는 문맥 민감이라 낱말별 재분석은 색인과 다른 형태소를 낸다 —
    "완만하게" 단독 분석은 완만하, 문장 분석은 완만(실측). query_expression은
    전문 일괄 분석 + 위치 기반 낱말 묶음이어야 색인과 같은 형태소를 낸다."""
    expression = morph.query_expression("완만하게 변하는 차원")
    assert '"완만"' in expression and '"완만하"' not in expression
    # 색인 경로와 동일한 형태소 집합
    assert set(morph.analyze("완만하게 변하는 차원")) == {"완만", "변하", "차원"}


def test_색인_대상_형태소가_없는_질의는_거부한다(repo: Repo):
    indexed(repo)
    # Kiwi는 홀로 선 조사도 명사로 읽으므로("은 는 이 가" → 은/늘/이) 진짜로 비는 것은
    # 구두점뿐이다. 이 경계를 규격으로 고정해 둔다.
    result = repo.run("ksearch.py", "!!! ...")
    assert result.returncode == 1 and "형태소가 나오지 않았습니다" in result.stderr


def test_reindex가_섹션과_파편화를_보고한다(repo: Repo):
    indexed(repo)
    result = repo.run("reindex.py")
    assert "형태소 레그: 섹션" in result.stdout

    connection = sqlite3.connect(repo.root / "derived.sqlite")
    with connection:
        count = connection.execute("SELECT COUNT(*) FROM morph").fetchone()[0]
    assert count > 0
