"""qmd 접점 — 캐시(인덱스·모델) 경로 해석과 전역 config의 컬렉션 쓰기.

이 저장소에서 qmd의 파일을 만지는 **유일한 모듈**이다. 경로 해석은 qmd 자신의
규칙(XDG → 홈)을 따른다 — 우리가 다른 파일을 보면 "백업은 됐는데 엉뚱한 인덱스",
"등록은 됐는데 검색은 안 됨" 같은 조용한 갈림이 생긴다. kb-new와 qmd-setup이
경로 해석과 컬렉션 등록의 사본을 따로 들던 시절, 충돌 검사 같은 불변식이
한쪽에만 있었다(2026-08-13 중복 감사).

벡터는 vec0(sqlite-vec) 가상 테이블에 있어서 확장을 로딩해야 읽힌다. 확장 실물은
qmd 패키지의 node_modules에서 찾는다 — 따로 설치하면 qmd와 버전이 갈라질 수 있고,
qmd가 있는 기기에는 반드시 함께 있다.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from pathlib import Path

import yaml

from .layout import Layout
from .repo import ROOT


class QmdUnavailable(RuntimeError):
    """qmd 인덱스나 벡터를 읽을 수 없는 상황. 소비자는 이유를 들고 크게 건너뛴다 —
    조용한 생략은 '검사했다'는 착각을 만든다."""


def index_path() -> Path:
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return cache / "qmd" / "index.sqlite"


def models_cache_dir() -> Path:
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return cache / "qmd" / "models"


def config_path() -> Path:
    """전역 config — qmd 자신의 해석 순서(qmd 2.1.0 dist/collections.js getConfigDir)."""
    if directory := os.environ.get("QMD_CONFIG_DIR"):
        return Path(directory) / "index.yml"
    if xdg := os.environ.get("XDG_CONFIG_HOME"):
        return Path(xdg) / "qmd" / "index.yml"
    return Path.home() / ".config" / "qmd" / "index.yml"


class CollectionConflict(RuntimeError):
    """같은 이름이 다른 경로를 가리킨다 — 신설 경로에서는 멈춰야 하는 상황."""


def load_config() -> dict:
    path = config_path()
    config = yaml.safe_load(path.read_text()) if path.is_file() else None
    return config or {}


def save_config(config: dict) -> Path:
    """전역 config를 다시 쓴다 — 이 파일은 qmd 자신도 기계로 쓰는 파생물이고
    (PLAN §5: layout.yaml에서 재생성 가능), 재생성물이라 통짜 직렬화가 규약에 맞다."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
    return path


def upsert_collections(config: dict, layout: Layout, names, *, overwrite: bool) -> None:
    """컬렉션 항목을 config dict에 넣는다(저장은 호출자가 save_config로).

    `qmd collection add`를 쓰지 않는 이유: 그 CLI에는 --ignore 플래그가 없어
    archive/ 제외를 걸 수 없다(qmd 2.1.0 소스 확인). 다음 qmd 실행이
    syncConfigToDb로 DB에 반영한다.

    overwrite 정책이 두 소비자를 가른다 — 기전은 하나, 의미는 둘:
    · kb-new(신설) = False. 동명 컬렉션이 다른 경로를 가리키면 CollectionConflict.
      컬렉션 이름은 전역이므로 남의 자리를 조용히 빼앗으면 안 된다.
    · qmd-setup(복구 런북) = True. 옛 기기의 경로가 남아 있는 것이 정상 전제라,
      현재 경로로 덮는 것이 재생성의 정의다.
    """
    collections = config.setdefault("collections", {}) or {}
    config["collections"] = collections
    for name in names:
        existing = collections.get(name)
        if (not overwrite and existing
                and existing.get("path") != str(ROOT / name)):
            raise CollectionConflict(
                f"qmd 컬렉션 '{name}'이 이미 다른 경로를 가리킵니다: {existing.get('path')}. "
                "컬렉션 이름은 전역이므로 KB 이름을 바꾸거나 기존 컬렉션을 정리하십시오.")
        collections[name] = {
            "path": str(ROOT / name),
            "pattern": layout.index_pattern,
            "ignore": list(layout.index_ignore),
        }


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
