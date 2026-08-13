"""작업 공간 값 객체 — 저장소 루트와 파생 경로의 단일 출처.

전에는 루트가 import 시점의 모듈 전역(repo.ROOT)이고 파생 경로(derived·stats·락)가
모듈마다의 전역 상수였다. 실측된 비용 셋이 이 객체의 근거다(2026-08-13 감사):
retrieval_eval이 다른 루트를 보려고 **자기 모듈을 멍키패치**했고(index_db.DB_PATH
덮어쓰기), 테스트는 in-process 주입이 불가능해 전부 서브프로세스이며, ROOT 직수입
15파일은 저장소 분리(PLAN §4.5) 시점의 전면 재설계 비용이다.

**비목표를 성문한다**: 한 프로세스에서 서로 다른 루트를 동시에 구동하는 것은
지원하지 않는다 — repo의 git 조회와 layout의 KB 판별은 여전히 프로세스 기본
루트(DEFAULT)에 묶인다. 이 객체가 지금 보장하는 것은 ⑴ 경로 파생 공식이 한
곳뿐이고 ⑵ DB 열기(connect)가 주입을 받아 멍키패치가 필요 없다는 것까지다.
전면 다중 루트는 실수요가 관측될 때의 재심 항목이다(3단계 보류 — 원장).

발견 규칙은 종전과 동일하다: SYNTOPICON_ROOT는 테스트 전용 seam(repo.py 주석이
정본)이고, 운영은 코드 위치 기준이다. DEFAULT는 import 시점에 한 번 발견된다 —
env는 프로세스 수명 동안 불변이라는 전제이며, repo.ROOT가 그랬던 것과 같다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Workspace:
    root: Path

    @property
    def derived_db(self) -> Path:
        return self.root / "derived.sqlite"

    @property
    def derived_lock(self) -> Path:
        return self.root / "derived.sqlite.lock"

    @property
    def stats_db(self) -> Path:
        return self.root / "stats.sqlite"

    @classmethod
    def discover(cls) -> "Workspace":
        # tools/syntopicon/workspace.py → 저장소 루트. resolve()가 심링크를 먼저 푼다 —
        # 스킬은 ~/.claude/skills/ 심링크를 거쳐 tools/를 부른다(PLAN §4.3).
        root = os.environ.get("SYNTOPICON_ROOT") or Path(__file__).resolve().parents[2]
        return cls(root=Path(root))


DEFAULT = Workspace.discover()
