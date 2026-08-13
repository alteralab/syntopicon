"""링크 그래프 검사 — 데이터 소스는 파생 인덱스의 edges 테이블."""

from __future__ import annotations

from pathlib import Path

from .base import Finding, check, kind

# 허브 후보로 볼 최소 피링크 차수 — 자체 상수(PLAN §6대로 운영 데이터로 보정할 자리).
HUB_DEGREE = 3
# 허브 분할 힌트 임계. 근거: PLAN이 허브 페이지에 준 예산은 1–2k 토큰[선택]이고
# 실측 30링크 허브 ≈ 2.6KB ≈ 그 예산 규모다 — 40은 상단 여유를 둔 환산치.
# 탐색 고장은 차수 가중 neighbors가 임계 없이 막으므로(§4.1 구현), 이 검사가 지키는
# 것은 진입점 예산과 훑기 가능성뿐. 자체 상수 — 운영 데이터로 보정.
HUB_SPLIT_HINT = 40

kind("broken-link", "error", "해석되지 않는 내부 링크",
     "링크를 고친다. 승급 직전에는 새 페이지를 가리키는 깨진 링크가 정상 상태다 — "
     "merge 후 재실행으로 판별하고, 개명은 반드시 tools/rename.py 경유.")
kind("redirect-hop", "warn", "redirect 스텁을 경유하는 링크",
     "스텁의 superseded_by 대상으로 직접 건다.")
kind("cross-kb-link", "warn", "KB 경계를 넘는 링크",
     "KB 자립성 위반이자 저장소 분리 시 파손 예고다. 링크만 지우지 말고 "
     "KB 경계를 잘못 그은 신호인지 본다.")
kind("orphan", "info", "어디서도 가리키지 않는 페이지",
     "허브나 관련 페이지에서 링크를 건다. 페이지 삭제가 답인 경우는 드물다.")
kind("hubs-section", "warn", "KB 진입 문서에 Hubs 절 부재",
     "layout.yaml의 절 계약이다 — overview에 Hubs 절 헤딩을 복원한다.")
kind("hub-candidate", "info", "Hubs 절에 없는 고차수 synthesis",
     "overview Hubs 절의 갱신 후보. 자동으로 넣지 않는다 — 큐레이션은 사람이 하고 "
     "상한은 10~30개다.")
kind("hub-dangling", "warn", "Hubs 절이 없는 페이지를 가리킴",
     "목록에서 빼거나 대상 경로를 고친다.")
kind("hub-split-hint", "info", "출차수가 임계를 넘은 허브",
     "분할은 부모-자식 패턴(옛 허브가 자식들을 가리키는 부모로 남아 링크 불파손). "
     "새 허브 이름은 현재 내용 범위만큼만 좁게 — 넓은 이름은 description을 미래에 "
     "거짓으로 만든다(SCHEMA §5).")


@check
def check_links(ctx):
    redirects = {p for p, f in ctx.files.items() if f.type == "redirect"}
    for row in ctx.connection.execute("SELECT src, dst, kind, resolved FROM edges"):
        src, dst = row["src"], row["dst"]
        if not row["resolved"]:
            yield Finding("broken-link", f"→ {dst}", ctx.kb_of(src), src)
        elif dst in redirects:
            target = (ctx.files[dst].frontmatter or {}).get("superseded_by", "?")
            yield Finding("redirect-hop",
                          f"→ {dst} 는 스텁입니다. {target} 로 직접 걸 것", ctx.kb_of(src), src)
        if row["kind"] == "cross_kb":
            yield Finding("cross-kb-link",
                          f"→ {dst} (KB 자립성 위반 — 저장소 분리 시 파손)", ctx.kb_of(src), src)


@check
def check_orphans(ctx):
    """어디서도 가리키지 않는 페이지. 진입점과 검역 중인 초안은 제외한다.

    참조는 두 채널이다 — 본문 링크(edges)와 frontmatter의 `sources[].resource`
    (PLAN §2.4의 루트 기준 경로). 후자를 안 세면 인용되고 있는 소스 메타가 전부
    영구 false positive로 찍히고, 그런 소음은 리포트 전체를 무시하게 만든다.
    """
    linked = {row["dst"] for row in
              ctx.connection.execute("SELECT DISTINCT dst FROM edges WHERE resolved = 1")}
    cited = {
        source["resource"].lstrip("/")
        for meta in ctx.meta.values()
        for source in meta["frontmatter"].get("sources", [])
        if isinstance(source, dict) and "resource" in source
    }
    for path, meta in ctx.meta.items():
        if path in linked or path in cited or meta["directory"] in (None, "inbox"):
            continue
        if meta["type"] == "redirect":
            # 스텁은 잔존 참조를 받기 위해 존재한다 — 내부 링크 0이 정상 상태이고,
            # 경유하는 링크가 생기면 redirect-hop 검사가 따로 잡는다.
            continue
        yield Finding("orphan", "가리키는 페이지가 없습니다", meta["kb"], path)


@check
def check_hubs(ctx):
    """Hubs 절 ↔ 고차수 synthesis 대조 — overview 갱신 후보를 낸다(PLAN §4.3).

    자동 갱신하지 않는다. 목록 자동화는 생존하지만 큐레이션 자동화는 실패한다는 것이
    판정 원장의 결론이고, 무엇을 허브로 올릴지는 사람의 선정이다.
    """
    from ..index_db import degrees as degree_rows

    section = ctx.layout.sections["hubs"]
    degrees = {row["path"]: row["degree"] for row in degree_rows(ctx.connection, "in")}

    for kb in ctx.layout.kbs():
        marker = f"{kb}/{ctx.layout.marker_path}"
        if (overview := ctx.files.get(marker)) is None:
            continue
        listed = {
            str(Path(marker).parent / href.partition("#")[0])
            for href in overview.links if "://" not in href
        }
        if not any(text.strip() == section for _, _, text in overview.headings):
            yield Finding("hubs-section",
                          f"'{section}' 절이 없습니다 (layout.yaml의 절 계약)", kb, marker)
            continue

        for path, meta in ctx.meta.items():
            if (meta["kb"] == kb and meta["type"] == "synthesis"
                    and degrees.get(path, 0) >= HUB_DEGREE and path not in listed):
                yield Finding("hub-candidate",
                              f"피링크 {degrees[path]}회인데 {section} 절에 없습니다", kb, path)
        for missing in sorted(listed - set(ctx.meta) - {marker}):
            yield Finding("hub-dangling",
                          f"{section} 절이 없는 페이지를 가리킵니다: {missing}", kb, marker)


@check
def check_hub_size(ctx):
    """출차수가 임계를 넘은 synthesis 페이지 → 분할 후보 리포트.

    메가허브의 탐색 고장 자체는 차수 가중 neighbors가 막지만, 오리엔테이션 때
    통째로 읽히는 진입점이 예산(1–2k 토큰)을 넘게 크는 것과 훑기 불가능해지는
    것은 남는다. 분할 판단은 사람이 한다 — "주제가 갈라지면 허브를 나눈다".
    """
    from ..index_db import degrees as degree_rows

    for row in degree_rows(ctx.connection, "out"):
        if row["degree"] <= HUB_SPLIT_HINT:
            break                     # degree 내림차순 — 임계 이하부터는 전부 아래다
        if ctx.meta.get(row["path"], {}).get("type") == "synthesis":
            yield Finding("hub-split-hint",
                          f"링크 {row['degree']}개 > {HUB_SPLIT_HINT} — 허브 분할 후보 "
                          "(진입점 예산 1–2k 토큰, PLAN §3)",
                          ctx.kb_of(row["path"]), row["path"])
