"""저장소 살림 검사 — 데이터 소스는 git 이력과 파일 시스템(저장소 밖 포함).

`check_skill_symlinks`는 이 저장소 검사기가 저장소 밖(~/.claude)을 보는 유일한
자리다 — 호출 표면이 심링크라 조용히 깨지는 유형이고, lint가 유일한 검출 지점이다.
"""

from __future__ import annotations

import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from ..repo import ROOT, added_at
from .base import Finding, check, kind

INBOX_P90_DAYS = 30            # PLAN §6
#: P90 경보의 표본 하한 — 자체 상수. 표본 1개면 int(1*0.9)=0이라 그 파일 나이가
#: P90 행세를 한다: 묵은 초안 하나가 "적체 파산" error를 울린 실측(2026-08-12)이
#: 이 하한의 근거다. 하한 미만이면 건별 inbox-age 경고만 낸다.
P90_MIN_SAMPLE = 5

kind("inbox-age", "warn", "임계를 넘긴 리뷰 대기 초안",
     "리뷰하거나 기각한다. 자동 승급 경로는 없다.")
kind("inbox-p90", "error", "inbox 나이 P90 임계 초과 (적체 신호)",
     "적체가 생겼다는 사실을 전하고 멈춘다. 발생한 적 없는 상황의 처방을 미리 두지 "
     "않는 것이 규율이므로(PLAN §4.4·§6) 대응책을 지어내지 말 것 — 무엇을 할지는 "
     "그때 사람이 정한다.")
kind("ingest-trailer", "warn", "소스 추가 커밋에 Ingest 트레일러 부재",
     "과거 커밋은 고치지 않고 다음 ingest부터 지킨다. 형식 확인은 "
     "git log --format=%B -1 | git interpret-trailers --parse.")
kind("skill-symlink", "error", "스킬 호출 표면 심링크 파손",
     "~/.claude/skills/<이름> 심링크를 정본(.agents/skills)으로 다시 건다 — "
     "기기당 1회 설치이며, 깨지면 스킬이 에러 없이 그냥 안 보인다.")


@check
def check_inbox(ctx):
    """inbox 나이 — P90이 임계를 넘으면 파산 신호다(PLAN §6 tripwire)."""
    ages: dict[str, list[int]] = defaultdict(list)
    for path, meta in ctx.meta.items():
        if meta["directory"] != "inbox":
            continue
        days = (datetime.now(timezone.utc) - added_at(path)).days
        ages[meta["kb"]].append(days)
        if days > INBOX_P90_DAYS:
            yield Finding("inbox-age", f"{days}일째 리뷰 대기", meta["kb"], path)

    for kb, values in ages.items():
        if len(values) < P90_MIN_SAMPLE:       # 표본 하한 — 상수 주석의 실측 근거
            continue
        ordered = sorted(values)
        p90 = ordered[min(int(len(ordered) * 0.9), len(ordered) - 1)]
        if p90 > INBOX_P90_DAYS:
            yield Finding("inbox-p90",
                          f"inbox 나이 P90 {p90}일 > {INBOX_P90_DAYS}일 — "
                          "적체 발생 신호입니다(대응은 사람이 정합니다 — "
                          "자동 승급 경로는 없습니다, PLAN §4.4)", kb)


@check
def check_ingest_trailers(ctx):
    """소스를 새로 들인 커밋에는 Ingest-Source:/Ingest-Run: 트레일러가 있어야 한다(§4.4-7)."""
    pathspecs = [f"{kb}/sources" for kb in ctx.layout.kbs()]
    if not pathspecs:
        return
    result = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%H", "--", *pathspecs],
        capture_output=True, text=True)
    for commit in result.stdout.split():
        body = subprocess.run(["git", "-C", str(ROOT), "show", "-s", "--format=%B", commit],
                              capture_output=True, text=True).stdout
        if missing := [t for t in ("Ingest-Source:", "Ingest-Run:") if t not in body]:
            yield Finding("ingest-trailer",
                          f"{commit[:8]} 가 소스를 추가했는데 {', '.join(missing)} 가 없습니다")


@check
def check_skill_symlinks(ctx):
    surface = Path.home() / ".claude" / "skills"
    skills_root = ROOT / ".agents" / "skills"
    if not skills_root.is_dir():          # 테스트 샌드박스·부분 체크아웃
        return
    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        link = surface / skill_dir.name
        if not link.is_symlink():
            yield Finding("skill-symlink",
                          f"~/.claude/skills/{skill_dir.name} 심링크 없음 — 전 프로젝트 호출 불가")
        elif link.resolve() != skill_dir.resolve():
            yield Finding("skill-symlink",
                          f"~/.claude/skills/{skill_dir.name} 이 정본이 아닌 {link.resolve()} 를 가리킴")
