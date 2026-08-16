"""통합 질의 래퍼. 핵심은 둘 — 갈래 실행과 **자동 계측**(이벤트·search_miss).

계측이 스킬 산문에 걸려 있던 시절 search_miss가 0건이었다는 것이 이 도구의 존재
이유이므로, 테스트도 출력이 아니라 stats.sqlite에 남은 행을 본다.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
from pathlib import Path

import pytest

from conftest import Repo
from test_validate import DDIA, SOURCE, concept

pytest.importorskip("kiwipiepy", reason="Tier B — uv sync --group index")


def bin_without_qmd(tmp_path: Path) -> str:
    """git만 보이는 PATH — qmd 갈래의 '건너뜀' 경로를 결정적으로 만든다.

    실기기 qmd는 전역 인덱스를 보므로 픽스처 검사에 끼어들면 안 된다.
    리터럴 갈래는 순수 파이썬이라 PATH가 필요 없다.
    """
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    binary = shutil.which("git")
    assert binary, "git이 테스트 환경에 없습니다"
    (bin_dir / "git").symlink_to(binary)
    return str(bin_dir)


def seeded(repo: Repo) -> None:
    repo.seed_it()
    repo.write("it/concepts/replication-lag.md",
               concept(body="\n복제 지연은 리더와 팔로워 사이의 간격이다.[^kleppmann2017-ddia]\n\n"
                            "[^kleppmann2017-ddia]: 5장\n"))
    repo.commit()
    assert repo.run("reindex.py").returncode == 0


def events_of(repo: Repo) -> list[tuple[str, dict]]:
    if not (repo.root / "stats.sqlite").exists():   # 조기 종료 경로 — 기록 자체가 없다
        return []
    with sqlite3.connect(repo.root / "stats.sqlite") as db:
        rows = db.execute("SELECT kind, payload FROM events ORDER BY rowid").fetchall()
    return [(kind, json.loads(payload)) for kind, payload in rows]


def test_형태소와_rg가_잡고_이벤트가_남는다(repo: Repo, tmp_path: Path):
    seeded(repo)
    result = repo.run("search.py", "복제 지연",
                      extra_env={"PATH": bin_without_qmd(tmp_path)})
    assert result.returncode == 0, result.stdout + result.stderr
    assert "형태소" in result.stdout and "replication-lag" in result.stdout
    assert "qmd 갈래를 건너뜀" in result.stdout

    (kind, payload), = events_of(repo)
    assert kind == "query"
    assert payload["legs"]["morph"]["hits"] >= 1
    assert payload["legs"]["literal"]["hits"] >= 1
    assert "skipped" in payload["legs"]["qmd"]
    assert payload["miss"] is False


def test_전갈래_0건이면_miss가_기록된다(repo: Repo, tmp_path: Path):
    seeded(repo)
    result = repo.run("search.py", "양자내성암호 격자환원", "--kb", "it",
                      extra_env={"PATH": bin_without_qmd(tmp_path)})
    assert result.returncode == 0, result.stdout + result.stderr

    (_, payload), = events_of(repo)
    assert payload["miss"] is True
    with sqlite3.connect(repo.root / "stats.sqlite") as db:
        misses = db.execute("SELECT kb, query FROM search_miss").fetchall()
    assert misses == [("it", "양자내성암호 격자환원")]


def test_낡은_색인이면_형태소_갈래는_크게_건너뛴다(repo: Repo, tmp_path: Path):
    """낡은 색인은 형태소 갈래만 사유와 함께 건너뛴다 — 리터럴 갈래는 디스크를
    직접 읽으므로 검색 자체는 살아 있어야 하고, 사유는 계측에 남는다."""
    seeded(repo)
    repo.write("it/concepts/fresh-page.md", concept())    # 색인 후 변경 → 낡음

    result = repo.run("search.py", "복제 지연",
                      extra_env={"PATH": bin_without_qmd(tmp_path)})
    assert result.returncode == 0, result.stdout + result.stderr
    assert "색인이 낡음" in result.stdout

    (_, payload), = events_of(repo)
    assert "색인이 낡음" in payload["legs"]["morph"]["skipped"]
    assert payload["legs"]["literal"]["hits"] >= 1


def test_없는_kb는_거부한다(repo: Repo, tmp_path: Path):
    seeded(repo)
    result = repo.run("search.py", "복제", "--kb", "ops",
                      extra_env={"PATH": bin_without_qmd(tmp_path)})
    assert result.returncode == 1
    assert "ops" in result.stderr
    assert events_of(repo) == []          # 실행 전 거부 — 계측도 남지 않는다


def test_스코프_이웃은_무방향_2홉이다(repo: Repo):
    """scope.neighborhood — 씨앗에서 링크 그래프를 무방향으로 걷는다(원장 2026-08-16)."""
    import sqlite3
    seeded(repo)
    page = (repo.root / "it/concepts/kafka-basics-test.md").read_text() \
        if (repo.root / "it/concepts/kafka-basics-test.md").exists() else None
    body = "\n- 서술이다.[^shapira2021]\n\n[^shapira2021]: 1장, p.3\n"
    def concept(name, extra=""):
        repo.write(f"it/concepts/{name}.md",
                   "---\ntype: concept\ntitle: " + name +
                   "\ndescription: 테스트\nsources: [shapira2021]\n" +
                   'generated: { by: "human:me", at: "2026-08-16T00:00:00Z" }\n---\n\n# '
                   + name + "\n" + body + extra)
    concept("a", "- [b](b.md) 로 간다.\n")
    concept("b", "- [c](c.md) 로 간다.\n")
    concept("c")
    concept("d", "- [a](a.md) 를 가리킨다.\n")
    repo.run("reindex.py")
    from syntopicon import scope
    db = sqlite3.connect(repo.root / "derived.sqlite")
    db.row_factory = sqlite3.Row
    hop1 = scope.neighborhood(db, ["it/concepts/a.md"], hops=1)
    assert "it/concepts/b.md" in hop1 and "it/concepts/d.md" in hop1   # 무방향
    assert "it/concepts/c.md" not in hop1
    hop2 = scope.neighborhood(db, ["it/concepts/a.md"], hops=2)
    assert "it/concepts/c.md" in hop2
