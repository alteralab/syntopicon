#!/bin/zsh
# 일간 백업 래퍼 (launchd 진입점 — PLAN §5·운영 캘린더 "restic 백업은 자동화").
# 실패 가시성 3중: ⑴ 실패 시 macOS 알림 ⑵ last_run 상태 파일 ⑶ 근본 백스톱 = restic 스냅샷 나이.
# 성공은 조용하고 실패만 시끄럽다. 스케줄러는 이 스크립트를 부를 뿐 — 로직 이관 금지(스케줄러 불가지론).
set -u
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export SYNTOPICON_BACKUP_DIR="$HOME/Backups/syntopicon"
export RESTIC_REPOSITORY="rest:http://ds923plus.tail2f9fe3.ts.net:8000/syntopicon"
export RESTIC_PASSWORD_FILE="$HOME/.restic-pass"
export RESTIC_REST_USERNAME="syntopicon"
export RESTIC_REST_PASSWORD="$(cat "$HOME/.restic-rest-pass")"

CORE="$(cd "$(dirname "$0")/.." && pwd)"
STATE="$SYNTOPICON_BACKUP_DIR/last_run.json"
LOG="$HOME/Library/Logs/syntopicon-backup.log"

MIRRORS="$CORE/../docs-mirror/mirrors"

echo "=== $(date '+%F %T') backup 시작" >> "$LOG"
# docs-mirror 1겹 편승 (docs-mirror PLAN §3.5): mirror 태그로 스냅샷 — 실패해도 core 백업은 계속
if [ -d "$MIRRORS" ]; then
  restic backup --quiet --tag mirror "$MIRRORS" >> "$LOG" 2>&1 \
    || { echo "mirror 편승 실패 (비치명 — 캐시)" >> "$LOG"; \
         osascript -e 'display notification "mirrors 스냅샷 실패 (core 백업은 별도 진행)" with title "syntopicon 백업"' || true; }
fi
if (cd "$CORE" && uv run tools/backup.py all) >> "$LOG" 2>&1; then
  printf '{"last_run": "%s", "ok": true}\n' "$(date '+%FT%T')" > "$STATE"
  echo "=== $(date '+%F %T') 성공" >> "$LOG"
else
  rc=$?
  printf '{"last_run": "%s", "ok": false, "rc": %d}\n' "$(date '+%FT%T')" "$rc" > "$STATE"
  echo "=== $(date '+%F %T') 실패 rc=$rc" >> "$LOG"
  osascript -e 'display notification "backup.py all 실패 — ~/Library/Logs/syntopicon-backup.log 확인" with title "syntopicon 백업"' || true
  exit "$rc"
fi
