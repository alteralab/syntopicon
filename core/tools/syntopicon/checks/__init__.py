"""lint 검사 패키지 — 검사는 데이터 소스별 모듈에, 조립은 base의 레지스트리에.

모듈 구분 = 검사가 읽는 데이터 소스다(크기가 아니라 성격으로 가른다):

| 모듈 | 데이터 소스 |
|---|---|
| graph | 파생 인덱스 edges |
| page | md AST (증분 대상 — CLI가 페이지 루프에서 직접 부른다) |
| provenance | archive/ (git 밖) |
| repo_ops | git 이력·파일 시스템 (저장소 밖 포함) |
| semantic | frontmatter 메타·벡터·형태소 관측 |

아래 서브모듈 import는 재수출이 아니라 **등록 부수효과**다 — 각 모듈이 import 시점에
Kind를 선언하고 @check로 검사를 등록한다.
"""

from .base import CHECKS, KINDS, Context, Finding, Kind, check, kind  # noqa: F401
from . import graph, page, provenance, repo_ops, semantic  # noqa: F401
from .page import check_page  # noqa: F401
