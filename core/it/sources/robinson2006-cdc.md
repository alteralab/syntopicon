---
type: webpage
title: "Consumer-Driven Contracts: A Service Evolution Pattern"
author: [{family: Robinson, given: Ian}]
issued: "2006-06-12"
container-title: "martinfowler.com"
URL: "https://martinfowler.com/articles/consumerDrivenContracts.html"
snapshot: /it/archive/robinson2006-cdc/
snapshot_sha256: "5ce4f0214f4940a0e2cde7eea22975a2f399c289c64d7d2bdd65c34bd1b9ebb9"
accessed: "2026-08-20"
---

# Consumer-Driven Contracts: A Service Evolution Pattern

서비스 제공자와 소비자 사이의 계약을 세 종류로 가르고, 그중 **소비자가 적은 기대에서
제공자 계약이 파생되는** 배치에 이름을 붙인 패턴 서술 글. 이 KB가 이것을 들이는 이유는
하나다 — 판정에 쓰이는 **사양 산출물을 누가 쓰는가**의 자리를 실무 문헌이 어떤 낱말로
적어 두었는가를 보이는 것이다.

## 지위 — 실무자 에세이이지 실증이 아니다

- **성격**: 패턴 서술 에세이(practitioner essay). 마틴 파울러 사이트에 실린 게스트 글이고
  저자는 당시 Thoughtworks의 컨설턴트다. 문면 그대로 — **"Ian Robinson is a Principal
  Consultant with Thoughtworks"**. 실험도 측정도 없고 수치가 한 개도 없다.
- **그래서 "학술 근거"로 인용하지 않는다.** 이 소스가 여는 것은 **정의와 그 정의를 지은
  사람의 자기 규정**이다. 글 자신이 서두에서 자기가 무엇을 하는지 규정한다 — 이 글은
  "the ‘Consumer-Driven Contract’ pattern, which imbues providers with insight into their
  consumer obligations, and focuses service evolution around the delivery of the key
  business functionality demanded by consumers"를 서술한다. 곧 **패턴을 제안하는 글**이지
  그 패턴이 효과가 있다는 것을 잰 글이 아니다.
- **저자 자신이 적용 범위를 좁혀 둔다.** 「Liabilities」 절이 단일 기업 또는 잘 알려진
  서비스들의 닫힌 공동체를 조건으로 못 박고, 결합도를 줄이지 않는다고 명시하고, 깨지는
  변경의 만병통치약이 아니라고 적는다. 인용할 때 이 절을 함께 읽는다.

## 판본과 열람일

- **개정이 없는 글이다.** 본문 말미 「Significant Revisions」가 한 줄뿐이다 —
  **"12 June 2006: First published"**. 페이지가 심은 `og:article:modified_time`도
  `2006-06-12`로, 발행일과 같다.
- 살아있는 페이지이므로 열람일을 남긴다. 웹에서 받은 날은 **2026-08-20**(`accessed`),
  그 파일을 이 KB의 아카이브로 옮긴 날은 **2026-08-22**다. 두 날 사이에 파일은 바뀌지
  않았고 `snapshot_sha256`이 그 파일의 동일성을 담보한다.
- **본문이 스스로 "더 나중 판이 있다"고 알린다** — "Since the original publication, there
  are some updates to this article. There is an updated version in the Thoughtworks
  Anthology and occasional blogs." 그 Anthology 개정판과 후속 블로그 글은 **이 KB가 원문을
  갖고 있지 않다.** 이 소스가 보증하는 것은 2006년 6월 12일 판 문면 하나뿐이고,
  개정판에만 있는 서술은 여기서 인용할 수 없다.

## 인용할 때 지킬 것

- **수치가 없다.** 이 글에는 인용할 측정값이 존재하지 않는다. 수치를 이 소스에 기대어
  적는 일은 어떤 경우에도 오인용이다.
- **글 안의 인용은 원전으로 간다.** 이 글이 옮겨 적는 남의 문장 — David Orchard가 든
  인터넷 프로토콜 견고성 원칙(Robustness Principle), W3C TAG의 버저닝 전략 분류,
  Pat Helland의 논문, Dare Obasanjo의 Must Ignore 서술 — 은 전부 **2차 경유**다.
  이 KB는 그 원문들을 갖고 있지 않으므로 이름과 이 글이 옮긴 문면까지만 쓴다.
- **후대 구현체는 이 글 밖이다.** 계약을 파일로 주고받는 오늘날의 도구들은 2006년 이
  글에 등장하지 않는다(스냅샷 전문 검색으로 확인 — `pact`는 `impact`·`impacts` 안에서만
  나온다). 도구 이름을 이 소스에 기대어 적지 않는다.
- **에이전트 시대로의 확장은 이 소스가 하지 않은 말이다.** 소비자 주도 계약을
  에이전트 사이의 계약(도구 스키마 따위)으로 옮기는 유추는 **미검증**이고, 이 소스는
  그 유추의 근거가 아니다.

## 이 소스가 닿을 자리

- [소비자 주도 계약](../concepts/consumer-driven-contracts.md) — 이 소스가 세우는 유일한 페이지
