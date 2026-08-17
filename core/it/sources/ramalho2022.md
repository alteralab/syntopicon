---
type: book
title: "Fluent Python: Clear, Concise, and Effective Programming"
author: [{family: Ramalho, given: Luciano}]
issued: "2022"
publisher: "O'Reilly Media"
ISBN: "9781492056355"
edition: 2
snapshot: /it/archive/ramalho2022/
snapshot_sha256: "f3a13178916b151ed2c8c874a816949fe19491a335205dcd196a872fba5f1ffb"
accessed: "2026-08-17"
---

# Fluent Python, Second Edition

파이썬의 관용 표현(idiom)을 언어의 내부 규약에서부터 설명하는 참조서. 25개 장이
특수 메서드·자료 구조·일급 함수·클래스와 프로토콜·제어 흐름·메타프로그래밍을 훑는다.

이 KB에서 이 소스의 지위는 **1차 — 파이썬 관용 참조**다. 원전이 아니다. 코드 품질 축의
원리는 [Ousterhout](ousterhout2021.md)·[Fowler](fowler2018.md)·[Beck](beck2023.md)이
말하고, 그 원리의 파이썬 실물은 [Percival & Gregory](percival2020.md)가 보인다. 이 책은
그 실물이 쓰는 **언어 기능 자체의 정본 근거**를 댄다 — `dataclass`가 무엇을 생성하는지,
`typing.Protocol`과 추상 기반 클래스가 어떻게 갈리는지 같은 것들이다.

- **전권 반입 대상이 아니다.** 참조 반입으로 세 장만 들였다 — 1장(데이터 모델),
  5장(데이터 클래스 빌더), 13장(인터페이스·프로토콜·ABC). 나머지 22개 장은 이 KB의
  소비 맥락 밖이다. 판정 근거는 `it/archive/ramalho2022/_progress.yaml`의 `skipped`에
  장별로 적혀 있다.
- **⚠ 아카이브 스냅샷은 정식 출간본이 아니라 Early Release(사전 공개판) 12차
  릴리스(2021-07-27)다.** 판권장이 그렇게 적고 있고, 25개 장 전부와 서문·판권장에
  "A note for Early Release readers" 상자가 붙어 있다("the author's raw and unedited
  content"). 그래서 **이 소스에서 옮긴 직인용은 정식 출간본과 낱말이 다를 수 있다.**
  실측으로 확인된 차이 하나: 5장 §"Data class as a code smell"의 절 제목이 정식판
  표기(§"Data Class as a Code Smell")와 대소문자가 다르다. 각주 locator는 **이
  스냅샷의 표기를 그대로** 쓴다 — 각주는 정식판이 아니라 이 스냅샷을 가리킨다.
- **이 스냅샷은 파이썬 3.9 시점에서 쓰였다.** 저자가 13장에서 "As I review this in
  July 2021"이라 적는다. 그래서 파이썬 3.10이 `@dataclass`에 더한 `slots`·`kw_only`·
  `match_args` 옵션이 이 판본의 5장 표에 없다. 해당 자리에 버전 조건을 달아 두었다.
- 아카이브 스냅샷은 **EPUB**이다. **인쇄판 쪽 앵커가 없어 locator는 장 + 절 제목**이다 —
  검증 절차와 근거는 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
- **이 EPUB 변환본에는 5부·6부 도비라와 색인이 없다.** 정식판의 Part V(Control
  Flow)·Part VI(Metaprogramming)에 해당하는 구분 파일이 없어 16장 다음이 곧바로
  17장이다. 반입 범위 밖이라 영향은 없으나, 부(Part) 단위로 재개점을 잡을 수 없다는 뜻이다.
- 본문의 그림(Figure)은 전부 이미지로 조판돼 있어 산문 서술로만 옮겼다. 특히 13장의
  Typing Map(Figure 13-1)은 이 장 전체의 뼈대인데 이미지라 네 사분면의 축을 그림 설명
  캡션에서 판독해 옮겼다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.
- 반입 재개점의 정본은 `it/archive/ramalho2022/_progress.yaml`이다.
