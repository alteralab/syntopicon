"""validate의 각 검사가 실제로 발화하는지. 게이트는 검증 없이 신뢰하지 않는다."""

from __future__ import annotations

import yaml

from conftest import Repo

DDIA = "kleppmann2017-ddia"


def page(frontmatter: dict, body: str = "") -> str:
    """frontmatter를 문자열로 수술하지 않고 yaml로 조립한다 — 픽스처가 규약을 어기면
    검사한 것이 실제 규칙인지 알 수 없게 된다."""
    dumped = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
    return f"---\n{dumped}---\n\n# {frontmatter.get('title', '제목')}\n{body}"


SOURCE = page({
    "type": "book",
    "title": "Designing Data-Intensive Applications",
    "author": [{"family": "Kleppmann", "given": "Martin"}],
    "issued": "2017",
    "ISBN": "9781449373320",
})


def concept(cite: str = DDIA, body: str = "", **extra) -> str:
    return page({
        "type": "concept",
        "title": "테스트 개념",
        "description": "한 줄 요약",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"},
        "sources": [{"id": cite, "resource": f"/it/sources/{cite}.md"}],
        **extra,
    }, body)


def failures(result) -> str:
    assert result.returncode == 1, f"통과해서는 안 되는데 통과했습니다:\n{result.stdout}"
    return result.stdout


def test_빈_저장소는_통과한다(repo: Repo):
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_KB는_마커_파일로_인식된다(repo: Repo):
    repo.kb("it")
    result = repo.validate()
    assert result.returncode == 0, result.stdout
    assert "KB 1개 (it)" in result.stdout


def test_정상_KB_한_벌은_통과한다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/replication-lag.md", concept(
        body=f"\n- 복제 지연은 읽기 일관성을 깨뜨린다.[^{DDIA}]\n\n[^{DDIA}]: Kleppmann 2017, 5장\n"))
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_분류되지_않은_루트_디렉터리를_잡는다(repo: Repo):
    repo.write("concepts/오타.md", "# 루트에 잘못 만든 디렉터리\n")
    assert "공유 자산도 KB도 아닙니다" in failures(repo.validate())


def test_BOM이_있어도_frontmatter를_읽는다(repo: Repo):
    """BOM이 구분선 인식을 죽여 'type 없음'이라는 엉뚱한 오류가 되던 버그의 회귀 방지."""
    repo.kb("it")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    target = repo.root / "it/concepts/bom-page.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"\xef\xbb\xbf" + concept().encode())
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_type_없는_md를_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/concepts/no-type.md", "# 제목만 있다\n")
    assert "typed frontmatter가 필요합니다" in failures(repo.validate())


def test_디렉터리와_type_불일치를_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/misplaced.md", concept())
    assert "그룹만 허용합니다" in failures(repo.validate())


def test_inbox의_draft_상태를_요구한다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/inbox/some-draft.md", concept())
    assert "status: draft 가 필요합니다" in failures(repo.validate())


def test_슬러그_문자집합_위반을_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/3-tier-architecture.md", concept())   # 번호 접두 금지
    assert "slug 규칙 위반" in failures(repo.validate())


def test_sources에_없는_각주를_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/orphan-footnote.md", concept(
        body="\n- 어딘가에서 온 주장.[^ongaro2014-raft]\n\n[^ongaro2014-raft]: Ongaro 2014\n"))
    assert "sources[]에 없습니다" in failures(repo.validate())


def test_짝이_깨진_각주는_validate가_못_잡는다(repo: Repo):
    """파서의 한계를 규격으로 고정한다 — 정의 없는 [^x]는 markdown-it이 평문으로
    흘리므로 AST에 나타나지 않는다. regex로 잡는 것은 금지(PLAN §3)이고, 이 경우는
    sources[]에 선언된 citekey가 인용되지 않은 것으로 kb-lint가 드러낸다."""
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/undefined-footnote.md",
               concept(body=f"\n- 정의 없는 인용.[^{DDIA}]\n"))
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_실존하지_않는_source_경로를_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/concepts/dangling.md", concept())   # sources/ 파일을 만들지 않았다
    assert "resource 경로가 없습니다" in failures(repo.validate())


def test_KB_안의_슬러그_중복을_잡는다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/replication.md", concept())
    repo.write("it/synthesis/replication.md", page({
        "type": "synthesis", "title": "복제", "description": "허브",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"}}))
    assert "중복" in failures(repo.validate())


def test_개정_대기_쌍은_중복이_아니다(repo: Repo):
    """concepts + inbox의 같은 슬러그 = 한 ID의 두 상태(개정 대기, PLAN §4.4-4·5).
    이 쌍을 막으면 기존 페이지 갱신이 검역을 지날 방법이 없다."""
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/replication.md", concept())
    repo.write("it/inbox/replication.md", concept(status="draft"))
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_synthesis가_끼는_쌍은_여전히_중복이다(repo: Repo):
    """synthesis는 인간 저작 전용 — 기계 초안의 검역 그림자를 가질 수 없다."""
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/synthesis/replication.md", page({
        "type": "synthesis", "title": "복제", "description": "허브",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"}}))
    repo.write("it/inbox/replication.md", concept(status="draft"))
    assert "중복" in failures(repo.validate())


def test_유사_ID는_경고일_뿐_막지_않는다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/replication-lag.md", concept())
    repo.write("it/concepts/replicationlag.md", concept())
    result = repo.validate()
    assert result.returncode == 0, result.stdout
    assert "유사 ID" in result.stdout


def test_결번_키를_잡는다(repo: Repo):
    repo.kb("it")
    ledger = repo.root / "schema" / "migrations.md"
    ledger.write_text(ledger.read_text().replace(
        "| 결번 키 | 은퇴일 | 대체 | 사유 |\n|---|---|---|---|\n",
        "| 결번 키 | 은퇴일 | 대체 | 사유 |\n|---|---|---|---|\n"
        "| as_of | 2026-08-05 | stale_after | 중복 필드 |\n",
    ))
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/revived.md", concept(as_of="2026-01-01"))
    assert "결번 키" in failures(repo.validate())


def test_superseded_by는_deprecated를_동반해야_한다(repo: Repo):
    repo.kb("it")
    repo.write("it/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("it/concepts/old-page.md", concept(superseded_by="new-page"))
    assert "'status' is a required property" in failures(repo.validate())


def test_규모_회귀_가드_파일당_서브프로세스_금지(repo: Repo):
    """2,113파일에서 validate가 247초 걸렸던 회귀의 재발 방지 — 원인은 루프 안
    kbs() 호출(파일당 git 서브프로세스)이었다. 300파일이 옛 병리 속도면 ~35초,
    정상이면 1~2초다. 경계 20초는 CI 흔들림을 허용하면서 그 클래스만 잡는다."""
    import time
    repo.kb("it")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    for i in range(300):
        name = chr(97 + i // 26) + chr(97 + i % 26)
        repo.write(f"it/concepts/scale-{name}.md", concept())

    start = time.monotonic()
    result = repo.validate()
    elapsed = time.monotonic() - start
    assert result.returncode == 0, result.stdout
    assert elapsed < 20, f"validate 300파일에 {elapsed:.1f}s — 파일당 서브프로세스 회귀 의심"
