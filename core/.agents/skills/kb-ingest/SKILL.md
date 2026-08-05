---
name: kb-ingest
description: 책·논문·기술 문서를 syntopicon 지식 베이스에 들인다. 새 소스를 정리해 넣을 때, 읽은 내용을 KB에 반영할 때, 웹에서 찾은 자료를 영구 보존할 때 쓴다. 스냅샷 보존과 citekey 발급부터 개념 페이지 갱신·검역·검증·커밋까지 한 파이프라인으로 처리한다.
compatibility: syntopicon 저장소 안에서 uv와 함께 실행한다. KB가 최소 하나 있어야 한다.
---

# kb-ingest

**신규 페이지 생성이 아니라 기존 페이지 갱신이 본체다.** 소스 하나가 신규 포함
10–15개 페이지를 건드리는 것이 정상이고, 새 페이지 하나 만들고 끝내는 것이 가장
흔한 실패다 — 같은 개념이 여러 페이지에 흩어져 몇 달 뒤 overlap lint로 돌아온다.

단계마다 **누가 하는 일인지**가 정해져 있다. 스크립트가 할 일을 손으로 하지 않는다.

## 0. KB 스코프 게이트 [스크립트]

`--kb`는 필수다. 대상 KB가 없으면 **여기서 멈춘다.**

```
uv run tools/validate.py       # KB 목록이 출력된다
```

KB가 없으면 "KB가 없습니다. kb-new를 먼저 실행하십시오"라고 말하고 끝낸다.
임의 위치에 파일을 흘리지 않고, 묻지 않고 KB를 만들지도 않는다.

## 1. 소스 큐레이션 [인간]

넣을 가치의 판단은 사용자 몫이다. 확인할 것 하나: **원서와 번역서가 둘 다 있으면
원서를 들인다.** 번역서는 확립 역어의 참조원으로만 쓴다.

## 2. 스냅샷 [스크립트] — 소급 불가능

파이프라인에서 되돌릴 수 없는 유일한 단계라 맨 앞에 있다. 원문을 먼저 고정한다.

```
uv run tools/snapshot.py --kb <kb> --citekey <citekey> <파일…>
uv run tools/snapshot.py --kb <kb> --citekey <citekey> --url <URL>
```

출력된 `snapshot` / `snapshot_sha256` / `accessed` 세 줄을 3단계 소스 메타에 그대로 넣는다.

## 3. 소스 메타 [LLM 제안 + 스크립트 발급]

citekey는 손으로 짓지 않는다 — 발급은 O_EXCL이어야 하고, 규칙은 결정적이다.

```
uv run tools/citekey.py --kb <kb> --author <성> --year <연도> [--slug <말>] --type <CSL타입>
```

만들어진 씨앗 파일에 CSL 필드를 채운다. 필드명은 CSL 원어 그대로
(`ISBN`/`DOI`/`URL`/`accessed`/`event-title`/`collection-title`/`authority`).
**날짜와 번호는 반드시 따옴표 문자열** — arXiv ID는 따옴표가 없으면 부동소수점이 된다.

## 4. 지식 추출 [LLM] — 본체

먼저 **닿을 페이지를 찾는다.** 새로 만들기 전에 갱신할 곳을 찾는 것이 순서다.

```
uv run --group index tools/ksearch.py "<개념>"
uv run tools/edges.py neighbors <관련페이지> --depth 2
```

쓰는 규칙:

- claim은 **각주 달린 불릿**. `[^citekey]` + 각주 텍스트에 locator(페이지·절).
- **한국어로 재서술**하되 개념 첫 등장에 원어 병기 — 영속성(persistence).
  확립 용어(TTA·국어원) 우선, 미확립이면 원어 유지.
- **정의·정리·수치는 번역하지 말고 원문 직인용**(인용 블록). 의미는 원문이,
  해설은 한국어가 담당한다.
- 불확실한 것은 `#hypothesis`, 근거가 얇으면 `#speculation`. 그 둘이 어휘의 전부다.
- 새 페이지를 만들면 **허브에 연결**한다(고아 페이지 방지). 슬러그는 영어 번역,
  소문자 kebab, 숫자 시작 금지.

## 5. inbox 격리 [구조]

기계 산출물은 전부 `<kb>/inbox/`에 착지한다. `concepts/`·`synthesis/` 직행은 없다.
`status: draft`를 단다.

사용자가 "내가 종합한 거니 synthesis에 바로 넣어달라"고 해도 마찬가지다 —
`synthesis/`의 경계 기준은 **작성 주체와 리뷰**이지 내용의 종합성이 아니다.

## 6. validate 루프 [기계 게이트]

```
uv run tools/validate.py
```

**통과할 때까지 고친다.** 통과 전에 다음 단계로 가지 않는다.

## 7. 커밋 [규약]

1런 = 1커밋. 트레일러 두 줄이 필수다.

```
<kb>: <소스 요지> ingest

왜 들였는지 1–3문장. 변경 파일 나열 금지 — diff가 담당한다.

Ingest-Source: <citekey>
Ingest-Run: <런ID>
```

실패해도 손해는 inbox 잔류뿐이다 — 본 코퍼스는 6단계까지 불변이었다.

## 8. 리뷰 [인간]

기준은 **무해성·구조**다: 각주 없는 claim, 기존 claim 훼손, 명백한 오류.
내용의 전수 정확성 검증이 아니다 — 그건 쓰는 시점에 한다(review-on-read).
기준을 넓히면 처리량이 0으로 수렴한다.

## 9. 재색인 [자동]

```
uv run tools/reindex.py        # 메타 + edges + 형태소
qmd update && qmd embed        # qmd 색인 (설치돼 있으면)
```

편집된 페이지는 청크 전량을 다시 만든다 — 옛 벡터가 남으면 조용히 오답을 낸다.

## 역방향

kb-query의 종합은 5단계로 들어오고, 웹에서 발견된 소스는 1단계부터 시작한다.
