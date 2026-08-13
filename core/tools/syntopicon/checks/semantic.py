"""의미·메타 검사 — 데이터 소스는 frontmatter 메타와 벡터·형태소 관측."""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
from pathlib import Path

from .. import schemas
from .base import Finding, check, kind

# overlap 후보 임계. 실측(2026-08-06, Qwen3-Embedding-0.6B) 네 대역:
#   · 근사 그대로 복제(문장만 다듬음):                       1.000  → 검출
#   · 재생성 중복(같은 용어, 다른 소스·문장·구조 — 주 사용례): 0.922  → 검출
#   · 관련되지만 서로 다른 개념(실 KB 전쌍):                  0.65–0.77 → 통과
#   · 어휘가 전혀 다른 의미 중복(SSOT 프로브):                0.542  → 사각!
# 임계는 0.77과 0.92 사이의 실측 간극에 있다. 교차 어휘 재서술(0.54)은 관련-상이
# 대역보다도 낮아 어떤 임계로도 분리되지 않는다 — 모델 능력의 한계라 숫자로 못
# 고친다. 그 사각은 inbox 리뷰 3문 ⑵·저장 전 검색이 담당하고, 수용 검증 ②의
# 임베딩 A/B(vs KURE-v1)가 한국어 특화 모델로 대역이 갈라지는지 재측정한다.
OVERLAP_THRESHOLD = 0.85
FRAGMENT_MIN_HITS = 2   # 한 번뿐인 파편은 오탐일 확률이 높다 — 자체 상수

# 원어 병기 쌍 `한국어 역어(english term)` — AST가 가른 텍스트 위의 어휘 스캔이다.
TERM_PAIR = re.compile(r"([가-힣][가-힣 ·]{0,30}?)\(([A-Za-z][A-Za-z /,–-]{2,60})\)")

kind("stale", "warn", "stale_after 만료",
     "내용을 확인했으면 stale_after를 옮기고, 낡았으면 status: deprecated + "
     "superseded_by로 은퇴시킨다(둘은 함께 간다).")
kind("contradiction", "info", "상호 기록된 모순 쌍",
     "연구 과제 큐다 — 자동 해소 금지, 최신성 단독 판단 금지. 해소 시 날짜·근거·"
     "대체 주장을 페이지에 남기고, 조건이 다른 두 주장이면 병합이 아니라 조건 "
     "명시로 푼다.")
kind("contradiction-one-sided", "error", "한쪽만 적힌 모순",
     "상대 페이지의 contradicts에도 적어 상호 기록으로 맞춘다(PLAN §2.1).")
kind("morph-fragmentation", "info", "형태소 파편화 (사용자 사전 후보)",
     "여러 페이지에서 반복되는 것만 schema/user-dict.yaml에 넣는다. 넣으면 "
     "재색인이 필요하다.")
kind("overlap", "info", "의미가 겹치는 페이지 쌍 (compaction 후보)",
     "병합 판단은 사람이 한다. 능력의 경계: 같은 용어의 재생성 중복(0.92)은 잡지만 "
     "어휘가 전혀 다른 재서술(0.54)은 못 잡는다 — 그쪽은 리뷰 3문 ⑵ 소관.")
kind("overlap-skipped", "warn", "overlap 검사 불능 (벡터 부재)",
     "qmd update && qmd embed 후 재실행한다 — 조용한 생략은 '검사했다'는 착각을 "
     "만들므로 크게 알린다.")
kind("term-drift", "info", "같은 원어의 역어 분열",
     "확정 역어 표를 따라 한쪽으로 통일한다 — 저장 어휘와 미래 검색어가 갈라지는 "
     "것을 막는 검사다. 병기된 것만 잡는다는 한계를 알고 읽을 것.")
kind("field-unused", "info", "선언됐지만 쓰인 적 없는 스키마 필드",
     "소비자 없는 필드가 쌓이는 신호다. 은퇴시키려면 tools/affected.py로 영향을 "
     "조회하고 schema/migrations.md 결번 대장에 적는다.")
kind("field-undeclared", "warn", "스키마에 없는 frontmatter 키",
     "확장은 custom 봉투나 x_ 접두만 허용된다(PLAN §2.7) — 오타이거나 무단 확장이다. "
     "정식 필드로 만들려면 스키마에 소비자와 함께 선언한다.")


@check
def check_stale(ctx):
    today = date.today().isoformat()
    for path, meta in ctx.meta.items():
        if meta["stale_after"] and meta["stale_after"] < today:
            yield Finding("stale", f"{meta['stale_after']} 만료 — 재검토 큐", meta["kb"], path)


@check
def check_contradictions(ctx):
    """모순은 상호 기록이어야 한다(PLAN §2.1). 자동 해소 금지 — 연구 과제 큐로만 낸다."""
    for path, meta in ctx.meta.items():
        for other in meta["frontmatter"].get("contradicts", []):
            counterpart = f"{meta['kb']}/{Path(path).parent.name}/{other}.md"
            listed = ctx.meta.get(counterpart, {}).get("frontmatter", {}).get("contradicts", [])
            if Path(path).stem not in listed:
                yield Finding("contradiction-one-sided",
                              f"{other} 를 모순으로 적었는데 상대는 적지 않았습니다",
                              meta["kb"], path)
            else:
                yield Finding("contradiction",
                              f"{other} 와 모순 — 해소 시 최신성 단독 판단 금지", meta["kb"], path)


@check
def check_fragments(ctx):
    """형태소 파편화 → 사용자 사전 후보 큐(PLAN §4.3).

    reindex가 관측해 둔 것을 읽기만 한다. 여러 페이지에서 같은 파편이 반복되면
    사전에 없는 복합어라는 신호가 강해진다.
    """
    rows = ctx.connection.execute("""
        SELECT surface, pieces, COUNT(*) AS hits, COUNT(DISTINCT path) AS pages
        FROM fragments GROUP BY surface, pieces
        HAVING hits >= ? ORDER BY hits DESC
    """, (FRAGMENT_MIN_HITS,)).fetchall()
    for row in rows:
        yield Finding("morph-fragmentation",
                      f"'{row['surface']}' 가 {row['pieces']} 로 부서집니다 "
                      f"({row['hits']}회/{row['pages']}페이지) — user-dict.yaml 후보")


@check
def check_overlap(ctx):
    """어휘가 달라도 의미가 겹치는 페이지 쌍 → compaction 후보 큐 (PLAN §2.6·§4.3).

    qmd의 청크 벡터를 재사용한다. 읽을 수 없으면 **크게** 건너뛴다 — 조용한 생략은
    "검사했다"는 착각을 만들고, 그 착각이 미구현 목록을 두던 이유였다.
    """
    from .. import overlap

    knowledge = {
        path for path, meta in ctx.meta.items()
        if meta["directory"] in ("concepts", "synthesis", "inbox")
        and meta["type"] != "redirect"
    }
    try:
        vectors = overlap.load_vectors(tuple(ctx.layout.kbs()))
    except overlap.QmdUnavailable as reason:
        yield Finding("overlap-skipped", f"overlap 검사를 건너뜀 — {reason}")
        return

    vectors = {path: matrix for path, matrix in vectors.items() if path in knowledge}
    if missing := knowledge - set(vectors):
        yield Finding("overlap-skipped",
                      f"임베딩 없는 페이지 {len(missing)}개 제외 — qmd update && qmd embed "
                      f"(예: {sorted(missing)[0]})")

    changed = None if ctx.overlap_full else ctx.changed
    pairs, examined = overlap.find_pairs(vectors, OVERLAP_THRESHOLD, changed)
    if examined:
        # 분모 없이 목록만 보면 "이 정도면 흔한 일"로 읽혀 오판이 난다(원장 실측).
        yield Finding("overlap",
                      f"비교 {examined}쌍 중 {len(pairs)}건이 임계 "
                      f"{OVERLAP_THRESHOLD} 초과 ({len(pairs) / examined:.2%})")
    for pair in pairs:
        yield Finding("overlap",
                      f"{pair.left} ↔ {pair.right}  유사도 {pair.similarity:.2f} — "
                      "compaction 후보(병합 판단은 사람)", ctx.kb_of(pair.left))


@check
def check_term_drift(ctx):
    """같은 원어가 서로 다른 역어로 병기되면 리포트한다 — 저장 어휘와 미래의 검색어가
    갈라지는 것이 이 검사가 막는 실패다("집계 도메인" vs "애그리게이트", 실사례).

    한계를 명시한다: **병기된 것만 잡는다.** 병기 없이 쓰인 역어("공통 진입로"가
    그랬다)는 기계가 원어를 알 수 없어 못 잡는다 — 그쪽은 리뷰 소관이고, 병기
    규율(§4.4-4)을 지킬수록 이 검사의 커버리지가 넓어진다.
    """
    renderings: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for path, md in ctx.files.items():
        for text in md.texts:
            for korean, english in TERM_PAIR.findall(text):
                renderings[english.strip().lower()][korean.strip()].add(path)

    def same_term(a: str, b: str) -> bool:
        """캡처에는 산문 접두가 붙는다(정규식이 leftmost에서 시작하므로). 같은 역어로
        보는 조건: 한쪽이 다른 쪽의 어절 접미이거나("핵심은 비즈니스 역량" ⊇ "비즈니스
        역량"), 공통 어절 접미가 2어절 이상 — 용어 자체가 겹친다는 뜻이다. 1어절
        공통("도메인"·"흐름")은 일반 명사 머리일 뿐이라 드리프트로 남긴다. 휴리스틱이고
        info 등급이다 — 판정은 사람이 한다."""
        ta, tb = a.split(), b.split()
        short, long_ = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
        if long_[-len(short):] == short:
            return True
        common = 0
        for x, y in zip(reversed(ta), reversed(tb)):
            if x != y:
                break
            common += 1
        return common >= 2

    for english, by_korean in sorted(renderings.items()):
        clusters: list[str] = []           # 대표 = 가장 짧은 표기
        for korean in sorted(by_korean, key=lambda k: (len(k.split()), len(k))):
            if not any(same_term(korean, seen) for seen in clusters):
                clusters.append(korean)
        if len(clusters) > 1:
            pages = sorted({p for paths in by_korean.values() for p in paths})
            yield Finding("term-drift",
                          f"({english}) 역어가 갈라짐: {' / '.join(clusters)} — "
                          f"{', '.join(pages)}")


@check
def check_field_usage(ctx):
    """선언 대비 실사용 대조(PLAN §2.7). 소비자 없는 필드가 쌓이는 것을 조회로 드러낸다."""
    used = {key for meta in ctx.meta.values() for key in meta["frontmatter"]}
    for key in sorted(schemas.declared_keys() - used - {"type"}):
        yield Finding("field-unused", f"스키마가 선언했지만 쓰인 적 없습니다: {key}")


@check
def check_field_undeclared(ctx):
    """미선언 키 검출 — field-unused의 역방향(집세 심사 R27·R28).

    JSON Schema는 미선언 키를 통과시키므로(OKF unknown-key 허용) 여기서만 보인다.
    허용 예외는 §2.7이 성문한 둘: custom 봉투와 x_ 접두.
    """
    declared = schemas.declared_keys() | {"custom"}
    for path, meta in sorted(ctx.meta.items()):
        for key in sorted(meta["frontmatter"]):
            if key not in declared and not key.startswith("x_"):
                yield Finding("field-undeclared",
                              f"스키마에 없는 키: {key}", meta["kb"], path)
