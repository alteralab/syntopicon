"""스냅샷과 citekey — ingest에서 소급 불가능한 두 단계라 실패 경로를 먼저 본다."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from conftest import Repo


def kb(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")


# ── snapshot ─────────────────────────────────────────────────────────────────

def test_파일을_보존하고_다이제스트를_낸다(repo: Repo, tmp_path):
    kb(repo)
    source = tmp_path / "ch5.txt"
    source.write_text("원문")

    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))
    assert result.returncode == 0, result.stderr

    manifest = f"{hashlib.sha256('원문'.encode()).hexdigest()}  ch5.txt\n"
    expected = hashlib.sha256(manifest.encode()).hexdigest()
    assert f'snapshot_sha256: "{expected}"' in result.stdout
    assert "snapshot: /it/archive/k2017-ddia/" in result.stdout
    assert (repo.root / "it/archive/k2017-ddia/ch5.txt").read_text() == "원문"


def test_기존_스냅샷을_덮어쓰지_않는다(repo: Repo, tmp_path):
    kb(repo)
    source = tmp_path / "a.txt"
    source.write_text("첫 판")
    repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))

    source.write_text("다른 판")
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))
    assert result.returncode == 1 and "write-once" in result.stderr
    assert (repo.root / "it/archive/k2017-ddia/a.txt").read_text() == "첫 판"


def test_KB가_없으면_거부한다(repo: Repo, tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("x")
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-x", str(source))
    assert result.returncode == 1 and "KB 'it'가 없습니다" in result.stderr


def test_보존할_것이_없으면_거부한다(repo: Repo):
    kb(repo)
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-x")
    assert result.returncode == 1 and "필요합니다" in result.stderr


# ── citekey ──────────────────────────────────────────────────────────────────

def test_결정적_규칙으로_발급한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "Martin Kleppmann",
                      "--year", "2017", "--slug", "ddia")
    assert result.returncode == 0, result.stderr
    assert "발급  kleppmann2017-ddia" in result.stdout
    assert (repo.root / "it/sources/kleppmann2017-ddia.md").is_file()


def test_충돌은_숫자_접미로만_푼다(repo: Repo):
    kb(repo)
    for _ in range(2):
        repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    assert (repo.root / "it/sources/ongaro2014.md").is_file()
    assert (repo.root / "it/sources/ongaro2014-2.md").is_file()


def test_두번째_발급은_접미를_알린다(repo: Repo):
    kb(repo)
    repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    result = repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    assert "접미가 붙었습니다" in result.stdout


def test_한국어_저자는_로마자_표기를_요구한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "홍길동", "--year", "2024")
    assert result.returncode == 1 and "--romanized" in result.stderr
    assert not (repo.root / "it/sources/2024.md").exists(), "연도만 남은 키가 예약됐습니다"

    result = repo.run("citekey.py", "--kb", "it", "--author", "홍길동",
                      "--romanized", "hong", "--year", "2024")
    assert result.returncode == 0 and "발급  hong2024" in result.stdout


def test_CSL_타입군_밖의_type을_거부한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "X", "--year", "2020",
                      "--type", "tweet")
    assert result.returncode == 1 and "CSL 타입군에 없습니다" in result.stderr


def test_발급한_씨앗은_validate를_통과한다(repo: Repo):
    kb(repo)
    repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014",
             "--type", "paper-conference", "--title", "In Search of Consensus")
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_dry_run은_예약하지_않는다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "Ongaro",
                      "--year", "2014", "--dry-run")
    assert result.returncode == 0 and "ongaro2014" in result.stdout
    assert not (repo.root / "it/sources/ongaro2014.md").exists()


# ── pdf 판정·추출 (pdf-inspector — 원장 2026-08-16) ──────────────────────────

def _build_pdf(text: str) -> bytes:
    """오프셋을 계산해 만드는 유효 최소 PDF — 외부 기록기 의존 없이 fixture를 만든다."""
    header = b"%PDF-1.4\n"
    stream = f"BT /F1 18 Tf 72 720 Td ({text}) Tj ET".encode()
    bodies = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = header, []
    for i, body in enumerate(bodies, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_at = len(out)
    out += b"xref\n0 6\n0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    return out + (b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n"
                  + str(xref_at).encode() + b"\n%%EOF\n")


def test_스냅샷이_pdf_판정_경로를_밟는다(repo: Repo, tmp_path: Path):
    """판정 실행(의존 있음) 또는 크게 고지(의존 없음) — 조용한 생략은 없다."""
    kb(repo)
    source = tmp_path / "book.pdf"
    source.write_bytes(_build_pdf("Hello snapshot fixture"))
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "x2020", str(source))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "판정  book.pdf" in result.stdout or "판정 건너뜀" in result.stdout


def test_pdftext가_구간을_추출한다(tmp_path: Path):
    pytest.importorskip("pdf_inspector")
    import pdftext
    pdf = tmp_path / "b.pdf"
    pdf.write_bytes(_build_pdf("Hello extract"))
    out = tmp_path / "o.md"
    assert pdftext.main([str(pdf), "1", "1", "-o", str(out)]) == 0
    body = out.read_text()
    assert "Hello extract" in body and "=== PDF 1쪽 ===" in body
