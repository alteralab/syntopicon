"""lint는 검출만 한다 — 놓치면 조용하고, 과잉이면 사람이 무시하게 된다. 둘 다 검증한다."""

from __future__ import annotations

import hashlib
import sqlite3

from conftest import Repo
from test_validate import DDIA, SOURCE, concept, page


def base(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)


def lint(repo: Repo, *args: str):
    repo.run("reindex.py")
    return repo.run("lint.py", *args)


def findings(repo: Repo, check: str) -> list[str]:
    connection = sqlite3.connect(repo.root / "stats.sqlite")
    connection.row_factory = sqlite3.Row
    with connection:
        rows = connection.execute(
            "SELECT path, message FROM lint_findings WHERE check_name = ? "
            "AND run_id = (SELECT MAX(id) FROM lint_runs)", (check,)).fetchall()
    return [f"{r['path']}: {r['message']}" for r in rows]


def cited(body_note: str = "Kleppmann 2017, 5장", **extra) -> str:
    return concept(body=f"\n- 각주 단 주장.[^{DDIA}]\n\n[^{DDIA}]: {body_note}\n", **extra)


# ── 그래프 ───────────────────────────────────────────────────────────────────

def test_깨진_링크와_redirect_경유를_구분한다(repo: Repo):
    base(repo)
    repo.write("it/concepts/raft.md", cited())
    repo.write("it/concepts/old-raft.md", page({
        "type": "redirect", "title": "옛 라프트", "superseded_by": "raft"}))
    repo.write("it/concepts/consensus.md", cited() + (
        "\n- [스텁 경유](old-raft.md)\n- [없는 곳](missing.md)\n"))

    result = lint(repo)
    assert result.returncode == 0
    assert findings(repo, "broken-link") == ["it/concepts/consensus.md: → it/concepts/missing.md"]
    assert "raft 로 직접 걸 것" in findings(repo, "redirect-hop")[0]


def test_크로스_KB_링크를_경고한다(repo: Repo):
    base(repo)
    repo.kb_new("ops", "운영", "설명")
    repo.write("ops/concepts/runbook.md", cited().replace(
        f"/it/sources/{DDIA}.md", f"/it/sources/{DDIA}.md"))
    repo.write("it/concepts/raft.md", cited() + "\n- [런북](qmd://ops/concepts/runbook.md)\n")
    lint(repo)
    assert any("KB 자립성 위반" in f for f in findings(repo, "cross-kb-link"))


def test_고아_페이지를_찾되_진입점과_inbox는_뺀다(repo: Repo):
    base(repo)
    repo.write("it/concepts/lonely.md", cited())
    repo.write("it/inbox/draft-idea.md", cited(status="draft"))
    lint(repo)
    orphans = [f.split(":")[0] for f in findings(repo, "orphan")]
    assert "it/concepts/lonely.md" in orphans
    assert "it/inbox/draft-idea.md" not in orphans
    assert "it/overview.md" not in orphans
    # frontmatter sources[].resource로 인용되는 소스 메타는 고아가 아니다 —
    # 본문 링크만 세면 모든 소스가 영구 false positive가 된다(첫 ingest에서 발견).
    assert f"it/sources/{DDIA}.md" not in orphans


def test_고차수_synthesis를_Hubs_후보로_낸다(repo: Repo):
    base(repo)
    repo.write("it/synthesis/distributed.md", page({
        "type": "synthesis", "title": "분산", "description": "허브",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"}}))
    for name in ("a-page", "b-page", "c-page"):
        repo.write(f"it/concepts/{name}.md",
                   cited() + "\n- [분산](../synthesis/distributed.md)\n")
    lint(repo)
    assert any("Hubs 절에 없습니다" in f for f in findings(repo, "hub-candidate"))


# ── 메타 ─────────────────────────────────────────────────────────────────────

def test_만료된_stale_after를_재검토_큐로_낸다(repo: Repo):
    base(repo)
    repo.write("it/concepts/expired.md", cited(stale_after="2020-01-01"))
    lint(repo)
    assert any("2020-01-01 만료" in f for f in findings(repo, "stale"))


def test_한쪽만_적힌_모순은_오류다(repo: Repo):
    base(repo)
    repo.write("it/concepts/alpha.md", cited(contradicts=["beta"]))
    repo.write("it/concepts/beta.md", cited())
    lint(repo)
    assert any("상대는 적지 않았습니다" in f for f in findings(repo, "contradiction-one-sided"))

    repo.write("it/concepts/beta.md", cited(contradicts=["alpha"]))
    lint(repo)
    assert findings(repo, "contradiction-one-sided") == []
    assert len(findings(repo, "contradiction")) == 2


def test_쓰인_적_없는_스키마_필드를_보고한다(repo: Repo):
    base(repo)
    repo.write("it/concepts/plain.md", cited())
    lint(repo)
    # 메시지 부분문자열이 아니라 키 이름으로 비교한다 — container-title 같은 키가
    # "title"을 품고 있어서 느슨한 대조는 늘 통과한다.
    keys = {f.rsplit(": ", 1)[1] for f in findings(repo, "field-unused")}
    assert "superseded_by" in keys
    assert {"title", "description", "sources"} & keys == set()


# ── 페이지 ───────────────────────────────────────────────────────────────────

def test_각주_없는_claim_불릿과_인용되지_않은_소스(repo: Repo):
    base(repo)
    repo.write("it/concepts/loose.md", concept(
        body="\n- 출처 없는 주장이다.\n- [포인터만](../synthesis/x.md)\n"))
    lint(repo)
    claims = findings(repo, "claim-unfootnoted")
    assert len(claims) == 1 and "출처 없는 주장" in claims[0]
    assert any(DDIA in f for f in findings(repo, "source-uncited"))


def test_미정의_epistemic_토큰을_잡고_정의된_것은_통과시킨다(repo: Repo):
    base(repo)
    repo.write("it/concepts/tokens.md", cited() + (
        "\n- #hypothesis 이건 정의된 토큰이다.[^" + DDIA + "]\n"
        "- #maybe 이건 아니다.\n"
        "- `#nottoken` 코드 스팬은 세지 않는다.\n"))
    lint(repo)
    reported = " ".join(findings(repo, "epistemic-token"))
    assert "#maybe" in reported
    assert "#hypothesis" not in reported and "#nottoken" not in reported


def test_역어_드리프트를_잡되_산문_접두는_무시한다(repo: Repo):
    """같은 원어에 다른 역어 = 저장 어휘와 미래 검색어의 분열(실사례: 집계/애그리게이트).
    산문이 앞에 붙은 병기("모든 것이 비즈니스 역량(business capability)")는 접미
    관계라 드리프트가 아니다."""
    base(repo)
    repo.write("it/concepts/alpha-page.md", cited() + (
        "\n가치 흐름(value stream)은 가치를 전달한다.\n"
        "핵심은 비즈니스 역량(business capability)이다.\n"))
    repo.write("it/concepts/beta-page.md", cited() + (
        "\n값 흐름(value stream)이라고 부르는 이도 있다.\n"
        "모든 것이 비즈니스 역량(business capability) 위에 선다.\n"))
    lint(repo)
    drift = " ".join(findings(repo, "term-drift"))
    assert "value stream" in drift and "가치 흐름" in drift and "값 흐름" in drift
    assert "business capability" not in drift, "접미 관계를 드리프트로 오인했습니다"


def test_허브_분할_힌트(repo: Repo):
    base(repo)
    links = "\n".join(f"- [x{i}](../concepts/topic-{i:02d}.md)" for i in range(45))
    for i in range(45):
        repo.write(f"it/concepts/topic-{i:02d}.md", cited())
    repo.write("it/synthesis/fat-hub.md", page({
        "type": "synthesis", "title": "비대 허브", "description": "분할 후보",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"}}, body=f"\n{links}\n"))
    lint(repo)
    assert any("허브 분할 후보" in f for f in findings(repo, "hub-split-hint"))


def test_wikilink를_잡는다(repo: Repo):
    base(repo)
    repo.write("it/concepts/obsidian.md", cited() + "\n- [[라프트]] 로 연결.\n")
    lint(repo)
    assert any("Obsidian 전용 문법" in f for f in findings(repo, "wikilink"))


def test_500줄_백스톱과_TOC_부재(repo: Repo):
    base(repo)
    long_body = "\n".join(f"문단 {i}." for i in range(520))
    repo.write("it/concepts/huge.md", cited() + "\n" + long_body + "\n")
    lint(repo)
    assert any("줄 —" in f for f in findings(repo, "page-too-long"))
    assert any("TOC가 없습니다" in f for f in findings(repo, "toc-missing"))


def test_헤딩_구조를_본다(repo: Repo):
    base(repo)
    repo.write("it/concepts/badheads.md", cited() + "\n#### 갑자기 H4\n")
    lint(repo)
    assert findings(repo, "heading-skip")


def test_스냅샷_변조를_잡는다(repo: Repo):
    base(repo)
    archive = repo.root / "it" / "archive" / "kleppmann"
    archive.mkdir(parents=True)
    (archive / "ch5.txt").write_text("원문")

    manifest = f"{hashlib.sha256('원문'.encode()).hexdigest()}  ch5.txt\n"
    correct = hashlib.sha256(manifest.encode()).hexdigest()
    source = SOURCE.replace("---\n\n#", f"snapshot: /it/archive/kleppmann/\n"
                                        f"snapshot_sha256: \"{correct}\"\n---\n\n#")
    repo.write(f"it/sources/{DDIA}.md", source)
    lint(repo)
    assert findings(repo, "snapshot-mismatch") == []

    (archive / "ch5.txt").write_text("변조됨")
    lint(repo)
    assert any("변조 증거" in f for f in findings(repo, "snapshot-mismatch"))


def test_없는_스냅샷을_경고한다(repo: Repo):
    base(repo)
    repo.write(f"it/sources/{DDIA}.md",
               SOURCE.replace("---\n\n#", "snapshot: /it/archive/nowhere/\n---\n\n#"))
    lint(repo)
    assert any("연 3% 이상 부패" in f for f in findings(repo, "snapshot-missing"))


# ── 실행 방식 ────────────────────────────────────────────────────────────────

def test_증분_실행은_바뀐_페이지만_본다(repo: Repo):
    base(repo)
    repo.write("it/concepts/one.md", concept(body="\n- 각주 없는 주장.\n"))
    repo.write("it/concepts/two.md", concept(body="\n- 각주 없는 주장.\n"))
    # overview.md + 소스 1 + 개념 2 = 4
    assert "4/4개 페이지 검사(full)" in lint(repo).stdout

    result = lint(repo, "--incremental")
    assert "0/4개 페이지 검사(incremental)" in result.stdout

    repo.write("it/concepts/one.md", concept(body="\n- 고친 뒤에도 각주는 없다.\n"))
    result = lint(repo, "--incremental")
    assert "1/4개 페이지 검사(incremental)" in result.stdout
    assert [f.split(":")[0] for f in findings(repo, "claim-unfootnoted")] == ["it/concepts/one.md"]


def test_오류가_있어도_실패로_끝내지_않는다(repo: Repo):
    base(repo)
    repo.write("it/concepts/broken.md", cited() + "\n- [없는 곳](nowhere.md)\n")
    result = lint(repo)
    assert result.returncode == 0, "lint는 검출만 한다 — 커밋을 막는 것은 validate다"
    assert findings(repo, "broken-link")


def test_미구현_검사를_매번_알린다(repo: Repo):
    """조용한 미구현이 가장 위험하다 — 검사한 줄 알게 된다."""
    base(repo)
    result = lint(repo)
    assert "미구현 검사: page-overlap" in result.stdout


def test_재색인_없이는_거부한다(repo: Repo):
    base(repo)
    result = repo.run("lint.py")
    assert result.returncode == 1 and "파생 인덱스가 없습니다" in result.stderr
