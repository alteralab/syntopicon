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
차단하고(쿠키·헤더 무관 403), headless Chrome도 챌린지로 막는다(UA를 덮어도 통과
못 함 — 2026-08-16 실측). 그래서 도구는 **화면 밖(-32000,-32000)에 헤드풀 창**을
스스로 띄웠다 정리한다 — 사용자가 창을 보거나 만질 일이 없고, 탐지 회피 패치가
아니라 위치만 옮긴 진짜 브라우저다. 근거 실측·절단본 판정은 `tools/medium_fetch.py`
독스트링이 정본이다.

## 저장소 위치 확정 (cwd 독립 — 최초 1회)

```sh
cd "$(dirname "$(dirname "$(dirname "$(realpath "${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/medium-fetch}")")")")"
```

## 1. 취득 [스크립트]

브라우저 기동·정리는 도구가 알아서 한다 — 손으로 Chrome을 띄우지 않는다.

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
| 절단본(미리보기)입니다 | 세션 없음·만료 — `--login` 후 재실행(아래) |
| Cloudflare 챌린지 | `--login`으로 창을 띄워 사람이 통과시킨 뒤 재실행 |
| 구조를 이해하지 못했습니다 | Medium 개편 신호 — 임기 패치 말고 `medium_fetch.py`의 판정을 갱신 |

## 2. 로그인 [사람 — 연 1회 수준]

절단본으로 실패하면 세션이 없거나 만료된 것이다(`sid` 쿠키 수명 약 1년):

```sh
uv run --group ingest tools/medium_fetch.py --kb it --login
```

보이는 Chrome 창이 Medium 로그인 페이지로 뜬다 — **Sign in with Google**로 한 번
로그인하면 세션이 프로필(ui-observe와 공유)에 저장되고, 창은 닫아도 된다. 이후
취득은 다시 화면 밖에서 조용히 동작한다. 이 한 번이 유일한 수동 단계다.

## 3. 이후 — 반입은 kb-ingest

사용자가 반입까지 원하면 kb-ingest 파이프라인의 1단계(큐레이션)로 넘어간다:

- 스냅샷(2단계): `_unread`에서 꺼내 `snapshot.py`에 **파일로** 넘긴다(같은 흐름).
- 소스 메타(3단계): citekey는 `--type post-weblog`, CSL `URL`/`accessed`/`title`은
  `_fetch-<slug>.yaml`에서 옮긴다.
- `_progress.yaml`(2단계): `unit: url`, 글 하나 = 범위 하나.
