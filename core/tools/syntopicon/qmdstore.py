"""qmd 인덱스(캐시 SQLite) 읽기 접근 — backup(사본)과 overlap(벡터)이 공유한다.

경로 해석은 qmd 자신의 규칙(XDG_CACHE_HOME → ~/.cache)을 따른다. 우리가 다른
파일을 보면 "백업은 됐는데 엉뚱한 인덱스" 같은 조용한 갈림이 생긴다.

벡터는 vec0(sqlite-vec) 가상 테이블에 있어서 확장을 로딩해야 읽힌다. 확장 실물은
qmd 패키지의 node_modules에서 찾는다 — 따로 설치하면 qmd와 버전이 갈라질 수 있고,
qmd가 있는 기기에는 반드시 함께 있다.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from pathlib import Path


class QmdUnavailable(RuntimeError):
    """qmd 인덱스나 벡터를 읽을 수 없는 상황. 소비자는 이유를 들고 크게 건너뛴다 —
    조용한 생략은 '검사했다'는 착각을 만든다."""


def index_path() -> Path:
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return cache / "qmd" / "index.sqlite"


def _vec_extension() -> Path:
    binary = shutil.which("qmd")
    if binary is None:
        raise QmdUnavailable("qmd가 PATH에 없습니다")
    package = Path(binary).resolve().parent.parent
    dylib = next(package.rglob("vec0.*"), None)      # .dylib / .so
    if dylib is None:
        raise QmdUnavailable(f"sqlite-vec 확장을 {package} 아래에서 찾지 못했습니다")
    return dylib


def connect_vectors() -> sqlite3.Connection:
    """벡터를 읽을 수 있는 읽기 전용 연결. 실패는 전부 QmdUnavailable로 모은다."""
    path = index_path()
    if not path.is_file():
        raise QmdUnavailable(f"qmd 인덱스가 없습니다: {path} — qmd update && qmd embed")

    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        connection.enable_load_extension(True)
        connection.load_extension(str(_vec_extension()).rsplit(".", 1)[0])
        connection.enable_load_extension(False)
        connection.execute("SELECT 1 FROM vectors_vec LIMIT 1")
    except (sqlite3.Error, AttributeError, OSError) as error:
        connection.close()
        raise QmdUnavailable(f"벡터 테이블을 열지 못했습니다: {error}") from error
    return connection
