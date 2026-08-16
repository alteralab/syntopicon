---
name: medium-fetch
description: Medium 글을 사용자의 로그인된 라이브 Chrome(CDP)으로 받아 KB의 _unread에 착지시킨다. 유료(member-only) 글을 전문으로 보존하고 싶을 때, Medium 글을 kb-ingest에 넘길 원문으로 확보할 때 쓴다. 절단본(미리보기)은 저장하지 않고 실패시키고, 반입 자체는 kb-ingest가 한다. 트리거 /medium-fetch <URL>
compatibility: macOS + Google Chrome. 어느 프로젝트에서든 호출 가능(본문 '저장소 위치 확정' 절이 core를 찾는다). uv 필요.
---

# medium-fetch — Medium 글 취득

**취득 전용이다.** libgen-dl(책)·paper-search(논문 후보)와 같은 계열 — 원문 파일을
확보해 `it/archive/_unread/`에 두는 데서 끝나고, 반입은 kb-ingest가 한다. 어떤
글을 넣을지는 사람이 고른다 — **일괄 수집·리딩리스트 동기화는 하지 않는다.**

왜 브라우저 경유인가: Medium은 Cloudflare가 비브라우저 요청을 TLS 지문 수준에서
차단한다(쿠키·헤더 무관 403). 로그인 세션이 있는 실제 Chrome만 통과한다 — 근거
실측과 절단본 판정 원리는 `tools/medium_fetch.py` 독스트링이 정본이다.

## 저장소 위치 확정 (cwd 독립 — 최초 1회)

```sh
cd "$(dirname "$(dirname "$(dirname "$(realpath "${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/medium-fetch}")")")")"
```

## 1. 디버그 Chrome [스크립트 + 최초 1회 사람]

```sh
lsof -i :9222 >/dev/null 2>&1 && echo PORT_BUSY || echo PORT_FREE
```

PORT_FREE면 (run_in_background로):

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.claude/ui-observe-chrome-profile \
  --no-first-run "https://medium.com" >/dev/null 2>&1
```

- 프로필은 **ui-observe와 공유**한다 — 라이브 브라우저 작업의 로그인 상태가
  한 프로필에 모인다. **최초 1회** 사용자에게 그 창에서 Medium 로그인을 요청한다.
  이후에는 세션이 프로필에 유지돼 로그인 없이 동작한다.
- PORT_BUSY인데 `curl -s http://localhost:9222/json/version`이 정상이면 그대로 재사용.
- ⚠ localhost 호출은 샌드박스가 막을 수 있다 → 해당 호출만 dangerouslyDisableSandbox.

## 2. 취득 [스크립트]

```sh
uv run --group ingest tools/medium_fetch.py --kb it <URL> [<URL>…]
```

성공 시 `it/archive/_unread/`에 세 파일이 남는다:

- `<slug>.html` — 렌더된 원문 전체. **스냅샷 대상(정본).**
- `_fetch-<slug>.yaml` — URL·accessed·저자·발행일·sha256. 소스 메타에 옮길 재료.
- `_text-<slug>.md` — 파생 참고용 본문(링크 보존, 서식 제거). 추출 런이 큰 HTML
  대신 읽는 용도이되, 직인용 대조는 정본 HTML로 한다.

실패 모드와 대응 (스크립트는 어느 경우에도 절단본을 저장하지 않는다):

| 메시지 | 대응 |
|---|---|
| 디버그 Chrome이 응답하지 않습니다 | 1단계로 |
| 절단본(미리보기)입니다 | 프로필 창에서 Medium 로그인·멤버십 확인 후 재실행 |
| Cloudflare 챌린지 | 열린 창에서 사람이 통과시킨 뒤 재실행 |
| 구조를 이해하지 못했습니다 | Medium 개편 신호 — 임기 패치 말고 `medium_fetch.py`의 판정을 갱신 |

## 3. 이후 — 반입은 kb-ingest

사용자가 반입까지 원하면 kb-ingest 파이프라인의 1단계(큐레이션)로 넘어간다:

- 스냅샷(2단계): `_unread`에서 꺼내 `snapshot.py`에 **파일로** 넘긴다(같은 흐름).
- 소스 메타(3단계): citekey는 `--type post-weblog`, CSL `URL`/`accessed`/`title`은
  `_fetch-<slug>.yaml`에서 옮긴다.
- `_progress.yaml`(2단계): `unit: url`, 글 하나 = 범위 하나.
