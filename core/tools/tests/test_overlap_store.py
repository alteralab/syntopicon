"""overlap의 벡터 적재(SQL·필터)와 lint 양성 경로.

순수 수학은 test_overlap.py가 고정한다. 여기가 닫는 것은 그동안 라이브 실행으로만
지나갔던 층이다 — 조인·collection 필터·sources 제외·active 제외·다중 청크 조립,
그리고 lint에서 finding이 실제로 뜨는 종단. 임베딩 모델은 필요 없다: qmd 인덱스는
그냥 SQLite라 같은 스키마의 가짜 인덱스에 합성 벡터를 넣으면 결정적으로 검증된다.
vec0 확장만은 실물이 필요해서(qmd 동봉) qmd 없는 기기에서는 건너뛴다.
"""

from __future__ import annotations

import shutil
import sqlite3
import struct
from pathlib import Path

import pytest

from conftest import Repo
from syntopicon import qmdstore
from test_validate import DDIA, SOURCE, concept

pytestmark = pytest.mark.skipif(
    shutil.which("qmd") is None, reason="vec0 확장은 qmd 동봉분을 쓴다")


def build_index(cache_dir: Path, rows: list[tuple[str, str, list[list[float]], int]]) -> None:
    """가짜 qmd 인덱스. rows = (collection, path, 청크 벡터들, active)."""
    path = cache_dir / "qmd" / "index.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.enable_load_extension(True)
    db.load_extension(str(qmdstore._vec_extension()).rsplit(".", 1)[0])
    dim = len(rows[0][2][0])
    db.executescript(f"""
        CREATE TABLE documents (collection TEXT, path TEXT, hash TEXT, active INTEGER);
        CREATE TABLE content_vectors (hash TEXT, seq INTEGER);
        CREATE VIRTUAL TABLE vectors_vec
            USING vec0(hash_seq TEXT PRIMARY KEY, embedding float[{dim}]);
    """)
    for index, (collection, rel, chunks, active) in enumerate(rows):
        content_hash = f"hash{index:04d}"
        db.execute("INSERT INTO documents VALUES (?,?,?,?)",
                   (collection, rel, content_hash, active))
        for seq, vector in enumerate(chunks):
            db.execute("INSERT INTO content_vectors VALUES (?,?)", (content_hash, seq))
            db.execute("INSERT INTO vectors_vec VALUES (?,?)",
                       (f"{content_hash}_{seq}", struct.pack(f"{dim}f", *vector)))
    db.commit()
    db.close()


def test_적재는_필터와_조립을_지킨다(tmp_path, monkeypatch):
    build_index(tmp_path, [
        ("it", "concepts/two-chunks.md", [[1, 0, 0, 0], [0, 2, 0, 0]], 1),
        ("it", "concepts/gone.md", [[1, 1, 1, 1]], 0),          # active=0 — 삭제된 판
        ("it", "sources/meta.md", [[1, 0, 0, 0]], 1),           # sources — 비교 제외
        ("it", "overview.md", [[1, 0, 0, 0]], 1),               # 콘텐츠 디렉터리 밖
        ("ops", "concepts/other-kb.md", [[1, 0, 0, 0]], 1),     # 다른 컬렉션
    ])
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    from syntopicon.overlap import load_vectors

    vectors = load_vectors(("it",))
    assert set(vectors) == {"it/concepts/two-chunks.md"}, \
        "필터(active·sources·디렉터리·컬렉션) 중 무언가가 샜습니다"
    matrix = vectors["it/concepts/two-chunks.md"]
    assert matrix.shape == (2, 4), "청크 조립이 깨졌습니다"
    import numpy
    assert numpy.allclose((matrix ** 2).sum(axis=1), 1.0), "정규화 누락 — 코사인이 아니게 됨"


def test_인덱스가_없으면_QmdUnavailable(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "empty"))
    from syntopicon.overlap import QmdUnavailable, load_vectors
    with pytest.raises(QmdUnavailable):
        load_vectors(("it",))


def _repo_with_pages(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/original-page.md", concept())
    repo.write("it/concepts/copied-page.md", concept())
    repo.write("it/concepts/unrelated-page.md", concept())


def test_lint_양성_경로가_종단으로_뜬다(repo: Repo):
    """finding이 실제 lint 실행에서 나오는가 — 지금까지 건너뜀 경로만 테스트돼 있었다."""
    _repo_with_pages(repo)
    # conftest가 XDG_CACHE_HOME을 qmd_config_dir/cache로 격리한다 — 그 자리에 가짜 인덱스.
    build_index(repo.qmd_config_dir / "cache", [
        ("it", "concepts/original-page.md", [[1, 0, 0, 0]], 1),
        ("it", "concepts/copied-page.md", [[0.99, 0.14, 0, 0]], 1),   # cos ≈ 0.99
        ("it", "concepts/unrelated-page.md", [[0, 0, 1, 0]], 1),
    ])
    repo.run("reindex.py")
    result = repo.run("lint.py", "--overlap-full")
    assert result.returncode == 0, result.stderr

    import sqlite3 as s3
    db = s3.connect(repo.root / "stats.sqlite")
    rows = db.execute(
        "SELECT message FROM lint_findings WHERE check_name='overlap' "
        "AND run_id=(SELECT MAX(id) FROM lint_runs)").fetchall()
    messages = [row[0] for row in rows]
    # 첫 줄은 분모다 — 목록 길이만 보고 판단하지 않게 하려고 항상 낸다(§8 실측).
    assert messages[0] == "비교 3쌍 중 1건이 임계 0.85 초과 (33.33%)", messages
    detail = [m for m in messages if "유사도" in m]
    assert len(detail) == 1, f"overlap 쌍 수가 다릅니다: {messages}"
    assert "original-page" in detail[0] and "copied-page" in detail[0]

    skipped = db.execute(
        "SELECT message FROM lint_findings WHERE check_name='overlap-skipped' "
        "AND run_id=(SELECT MAX(id) FROM lint_runs)").fetchall()
    # overview.md 등 벡터를 안 넣은 지식 페이지는 없다 — 3개 전부 넣었으므로 누락 경고 없음
    assert not any("임베딩 없는" in r[0] for r in skipped), skipped


def test_벡터가_일부만_있으면_누락을_경고한다(repo: Repo):
    _repo_with_pages(repo)
    build_index(repo.qmd_config_dir / "cache", [
        ("it", "concepts/original-page.md", [[1, 0, 0, 0]], 1),
    ])
    repo.run("reindex.py")
    repo.run("lint.py", "--overlap-full")

    import sqlite3 as s3
    db = s3.connect(repo.root / "stats.sqlite")
    rows = db.execute(
        "SELECT message FROM lint_findings WHERE check_name='overlap-skipped' "
        "AND run_id=(SELECT MAX(id) FROM lint_runs)").fetchall()
    assert any("임베딩 없는 페이지 2개" in r[0] for r in rows), rows
