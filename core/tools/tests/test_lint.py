"""lint는 검출만 한다 — 놓치면 조용하고, 과잉이면 사람이 무시하게 된다. 둘 다 검증한다."""

from __future__ import annotations

import hashlib
import sqlite3

from conftest import Repo
from test_validate import DDIA, SOURCE, concept, page


def base(repo: Repo) -> None:
    repo.seed_it()


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
    # redirect 스텁은 내부 링크 0이 정상 — 잔존 참조를 받는 것이 존재 이유다.
    repo.write("it/concepts/old-name.md", page({
        "type": "redirect", "title": "옛 이름", "superseded_by": "lonely"}))
    lint(repo)
    assert "it/concepts/old-name.md" not in [
        f.split(":")[0] for f in findings(repo, "orphan")]
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


def test_각주_밖_코드_펜스를_잡는다(repo: Repo):
    """소스에 없는 코드를 지어내면 예제가 아니라 발명한 claim이다(SCHEMA §3).
    기계가 볼 수 있는 것은 소속뿐 — 각주 단 불릿 안에 있는가. 그 안이면 각주를
    상속하므로 통과시키고, 절 바닥에 홀로 놓인 펜스는 잡는다."""
    base(repo)
    fence = "  ```sql\n  SELECT 1;\n  ```\n"
    repo.write("it/concepts/attached.md", concept(
        body=f"\n- 각주 단 주장.[^{DDIA}]\n\n{fence}\n[^{DDIA}]: Kleppmann 2017, 5장\n"))
    repo.write("it/concepts/orphan.md", cited() + "\n```sql\nSELECT 1;\n```\n")
    lint(repo)

    found = findings(repo, "code-unsourced")
    assert any("orphan.md" in f for f in found), "각주 밖 펜스를 놓쳤습니다"
    assert not any("attached.md" in f for f in found), \
        "각주 단 불릿 안의 펜스를 잘못 잡았습니다 — 하위는 부모 각주를 상속한다"


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


def test_overlap은_벡터가_없으면_크게_건너뛴다(repo: Repo):
    """조용한 생략이 가장 위험하다 — 격리된 픽스처엔 qmd 인덱스가 없으므로
    경고가 반드시 떠야 한다. --quiet에서도 살아남는 warn 등급이다."""
    base(repo)
    result = lint(repo)
    assert result.returncode == 0
    assert any("overlap 검사를 건너뜀" in f for f in findings(repo, "overlap-skipped"))


def test_재색인_없이는_거부한다(repo: Repo):
    base(repo)
    result = repo.run("lint.py")
    assert result.returncode == 1 and "파생 인덱스가 없습니다" in result.stderr


def test_반입_진행_파일을_검사한다(repo: Repo):
    """`_progress.yaml`은 재개점의 정본이다(kb-ingest 4단계). 소스 메타 산문이 그 자리를
    맡다가 아홉 런 뒤처져 재반입을 부를 뻔한 것이 이 검사의 발단이다(2026-08-12).

    validate가 아니라 lint인 이유는 `archive/`가 git 밖이라서다 — 스냅샷 검사와 같은 자리.
    """
    import yaml as _yaml
    base(repo)
    repo.write("it/concepts/page.md", cited())
    root = repo.root / "it" / "archive" / "kleppmann"
    root.mkdir(parents=True, exist_ok=True)
    (root / "src.pdf").write_bytes(b"x")
    repo.write(f"it/sources/{DDIA}.md",
               SOURCE.replace("---\n\n#", "snapshot: /it/archive/kleppmann/\n---\n\n#"))

    def progress(**over):
        doc = {"citekey": DDIA, "unit": "page", "total": "1p-10p",
               "contents": {"1ch": "1p-10p"}, "covered": ["1p-10p"],
               "skipped": [], "next": None}
        doc.update(over)
        doc = {k: v for k, v in doc.items() if not (k == "contents" and v is None)}
        (root / "_progress.yaml").write_text(_yaml.safe_dump(doc, allow_unicode=True))

    # 없으면 경고 — 산문에 기대면 표류한다
    lint(repo)
    assert any(DDIA in f for f in findings(repo, "progress-missing"))

    # 타입↔단위 정합: 소스는 book 인데 url 단위는 쓸 수 없다
    progress(unit="url", contents=None, covered=["a"], total=None)
    lint(repo)
    assert findings(repo, "progress-unit"), "type↔unit 불일치를 놓쳤습니다"

    # 접미 누락: 값만 인용되면 단위를 잃으므로 붙이게 한다
    progress(covered=["1-10"])
    lint(repo)
    assert findings(repo, "progress-suffix"), "단위 접미 누락을 놓쳤습니다"

    # 온전하면 조용하다
    progress()
    lint(repo)
    assert not findings(repo, "progress-suffix") and not findings(repo, "progress-unit")


def test_결과_종류_레지스트리가_완결이다():
    """이름·등급·지침의 정본은 Kind 레지스트리다. 지침 없는 검사는 추가 자체가
    안 되게 여기서 강제한다 — SKILL 손 유지 목록의 안내 누락 17종이 이 테스트의
    발단이다."""
    from syntopicon.checks import KINDS

    assert len(KINDS) == 41
    for k in KINDS.values():
        assert k.severity in ("error", "warn", "info"), k.name
        assert k.doc and k.guidance, f"{k.name}: doc·guidance는 필수다"


def test_링크_불릿은_claim이_아니다(repo: Repo):
    """`- [제목](경로) — 설명` 꼴은 §2.6이 허브에 요구하는 포인터 문법이다. 같은 모양이
    concept 페이지에서 각주 없는 claim으로 찍히던 것이 리포트의 84%(649/769)를 채운
    오검출이었다 — 링크로 시작하는 불릿은 claim 검사 대상이 아니다."""
    base(repo)
    repo.write("it/concepts/pointer-list.md", concept(body=(
        "\n- [개요](../overview.md) — 진입점으로 가는 포인터 설명\n")))
    lint(repo)
    assert findings(repo, "claim-unfootnoted") == []


def test_explain은_레지스트리를_조회한다(repo: Repo):
    result = repo.run("lint.py", "--explain", "broken-link")
    assert result.returncode == 0
    assert "broken-link" in result.stdout and "rename.py" in result.stdout
    assert repo.run("lint.py", "--explain", "없는종류").returncode == 1
