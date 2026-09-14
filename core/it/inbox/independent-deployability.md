---
type: concept
title: 독립 배포 가능성
status: draft
description: 마이크로서비스를 정의하는 성질로 지목된 독립 배포 가능성 — 할 수 있다가 아니라 그렇게 한다는 규율이라는 규정, 이 책이 하나만 가져가라고 적은 처방, 그것을 세우려면 필요한 느슨한 결합과 명시적이고 잘 정의되고 안정된 계약이라는 조건, 데이터베이스 공유가 특히 나쁜 이유, 상태를 스스로 소유하는 것이 이 성질을 위한 수단이라는 배치, 하나를 목표로 걸면 나머지가 딸려 온다는 강제 함수 논리, 그리고 그 대가로 돌려받는 배포 용이성과 빠른 롤백, 그리고 같은 책 5장이 지목하는 이 성질을 거스르는 세 자리 — 보조를 맞춘 배포와 공유 라이브러리의 동시 갱신과 클라이언트 라이브러리의 업그레이드 시점
generated: { by: "claude-opus-5", at: "2026-09-15T15:00:00Z" }
sources:
  - { id: newman2021, resource: /it/sources/newman2021.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 독립 배포 가능성

- [정의 — 할 수 있다가 아니라 그렇게 한다](#정의--할-수-있다가-아니라-그렇게-한다)
- [이 책이 하나만 가져가라고 적은 것](#이-책이-하나만-가져가라고-적은-것)
- [성립 조건 — 느슨한 결합과 안정된 계약](#성립-조건--느슨한-결합과-안정된-계약)
- [상태를 스스로 소유하는 것이 이 성질을 위한 수단이다](#상태를-스스로-소유하는-것이-이-성질을-위한-수단이다)
- [같은 목표를 인코딩 쪽에서 본 다른 소스](#같은-목표를-인코딩-쪽에서-본-다른-소스)
- [강제 함수 — 하나를 걸면 나머지가 딸려 온다](#강제-함수--하나를-걸면-나머지가-딸려-온다)
- [그 대가로 돌려받는 것 — 배포 용이성](#그-대가로-돌려받는-것--배포-용이성)
- [5장이 이 성질을 거스르는 세 자리](#5장이-이-성질을-거스르는-세-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **무엇을 독립 배포 가능성이라 부르며, 그것 하나를 목표로 걸면 무엇이
따라오는가.**

## 정의 — 할 수 있다가 아니라 그렇게 한다

- [newman2021](../sources/newman2021.md)은 마이크로서비스의 핵심 개념 다섯 중 첫째로
  독립 배포 가능성(independent deployability)을 놓고 이렇게 규정한다
  (1장 §"Independent Deployability", p.6):[^newman2021]

  > Independent deployability is the idea that we can make a change to a microservice,
  > deploy it, and release that change to our users, without having to deploy any other
  > microservices.

  - **정의에 곧바로 단서가 붙는다** — 더 중요한 것은 그렇게 할 수 **있다**는 사실이
    아니라, 그것이 체계에서 배포를 관리하는 **실제 방식**이라는 것이다. 기본 릴리스
    방식으로 채택하는 **규율(discipline)**이며, 발상은 단순하되 실행은 복잡하다
    (1장, p.6).[^newman2021]
- 이 성질은 이 책의 마이크로서비스 정의 자체에 들어 있다 — 서문이 마이크로서비스를
  **독립적으로 바꾸고 배포하고 릴리스할 수 있는 잘게 나뉜 서비스**를 쓰는 분산 시스템
  접근이라 적는다 (서문, p.xvii).[^newman2021] 그 정의의 전문은
  [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)에 있다.

## 이 책이 하나만 가져가라고 적은 것

- 저자는 곁글 하나에 책 전체의 처방을 건다 (1장 §"Independent Deployability",
  p.6):[^newman2021]

  > If you take only one thing from this book and from the concept of microservices in
  > general, it should be this: ensure that you embrace the concept of independent
  > deployability of your microservices. Get into the habit of deploying and releasing
  > changes to a single microservice into production without having to deploy anything
  > else. From this, many good things will follow.

## 성립 조건 — 느슨한 결합과 안정된 계약

- 조건이 한 문장으로 온다 (1장 §"Independent Deployability", p.6):[^newman2021]

  > To ensure independent deployability, we need to make sure our microservices are
  > loosely coupled: we must be able to change one service without having to change
  > anything else. This means we need explicit, well-defined, and stable contracts
  > between services.

  - 그리고 그 조건을 깨는 구현 선택이 곧바로 지목된다 — **데이터베이스 공유가 특히
    문제**다 (1장, p.6).[^newman2021] 그 규칙의 전문은
    [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)의 데이터 경계
    절에 있다.
- 그래서 이 성질이 경계를 찾는 일의 출발점이 된다 — **안정된 인터페이스를 가진 느슨하게
  결합된 서비스에 대한 욕구가 애초에 마이크로서비스 경계를 어떻게 찾을지에 대한 사고를
  이끈다** (1장, p.7).[^newman2021] 그 어림법은
  [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md)에 있다.

## 상태를 스스로 소유하는 것이 이 성질을 위한 수단이다

- 서비스가 자기 데이터를 감추는 규칙은 이 성질에서 유도된다 — **독립 배포 가능성을
  현실로 만들고 싶다면 마이크로서비스에 대한 하위 호환을 깨는 변경을 제한해야 한다.
  상류 소비자와의 호환을 깨면 그들도 바꾸도록 강요하게 된다.** 내부 구현 세부와 외부
  계약 사이를 깨끗이 가르면 하위 호환을 깨는 변경의 필요 자체가 줄어든다 (1장
  §"Owning Their Own State", p.8).[^newman2021]
- 데이터베이스 공유에 대한 판정도 이 성질을 잣대로 내려진다 (1장 §"Owning Their Own
  State", p.9):[^newman2021]

  > Don't share databases unless you really need to. And even then do everything you can
  > to avoid it. In my opinion, sharing databases is one of the worst things you can do
  > if you're trying to achieve independent deployability.

## 같은 목표를 인코딩 쪽에서 본 다른 소스

- [kleppmann2026](../sources/kleppmann2026.md)은 같은 목표를 세운 뒤 그것이 데이터
  인코딩에 무엇을 강제하는지로 잇는다 — **서비스 지향/마이크로서비스 아키텍처의 핵심
  설계 목표는 서비스를 독립적으로 배포 가능하고 진화 가능하게 만드는 것**이고, 그래서
  **서버와 클라이언트의 옛 버전과 새 버전이 동시에 돌 것을 예상해야 하며 데이터 인코딩은
  서비스 API의 버전들에 걸쳐 호환돼야 한다** (5장, pp.180–181).[^kleppmann2026]
  - **두 소스가 같은 자리를 반대 방향에서 온다.** 이 책은 "독립 배포를 규율로 삼으면
    안정된 계약이 필요해진다"로 가고, 저쪽은 "독립 배포를 목표로 삼으면 인코딩 호환성이
    강제된다"로 간다. 전문은
    [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)의 독립 배포 절에
    있다.

## 강제 함수 — 하나를 걸면 나머지가 딸려 온다

- 저자가 이 개념에 매기는 값은 두 겹이다 — **독립 배포 가능성 그 자체로도 대단히
  값지다. 그러나 그것을 달성하려면 제대로 해야 할 다른 일이 아주 많고, 그것들 각각이
  또 자기 이득을 갖는다. 그래서 독립 배포 가능성에 대한 집중을 강제 함수(forcing
  function)로 볼 수도 있다** — 이것 하나를 결과로 삼고 집중하면 부수적 이득 여럿을
  함께 얻게 된다 (1장, p.6).[^newman2021]

## 그 대가로 돌려받는 것 — 배포 용이성

- 모놀리스 쪽의 비용이 먼저 서술된다 — **백만 줄짜리 모놀리식 애플리케이션에서 한 줄을
  바꾸려면 그 변경을 릴리스하기 위해 애플리케이션 전체를 배포해야 한다.** 그래서 그런
  배포는 영향이 크고 위험이 높으며, 이해할 만한 두려움 때문에 실무에서 드물게 일어나게
  된다. 그 결과 릴리스 사이에 변경이 쌓이고, **릴리스 사이의 차이가 클수록 무언가
  잘못될 위험도 높아진다** (1장 §"Ease of Deployment", p.25).[^newman2021]
- 마이크로서비스 쪽에서는 서비스 하나만 바꿔 나머지와 무관하게 배포한다. 그래서 코드가
  더 빨리 배포되고, **문제가 생기면 개별 서비스로 빠르게 좁혀져 빠른 롤백이 쉬워진다**.
  저자는 아마존과 넷플릭스가 이 아키텍처를 쓰는 주된 이유 하나로 이것을 든다 (1장
  §"Ease of Deployment", p.25).[^newman2021]

## 5장이 이 성질을 거스르는 세 자리

**1장이 이 성질을 세우고, 같은 책 5장이 그것을 실제로 갉아먹는 자리 셋을 지목한다.** 셋 다
같은 기제다 — **무언가를 함께 배포하게 만드는 것**이다.

- **① 보조를 맞춘 배포** — 인터페이스를 깨는 변경을 다루는 세 선택지 중 첫째인 보조 맞춘
  배포(lockstep deployment)는 **인터페이스를 노출하는 마이크로서비스와 그 인터페이스의 모든
  소비자를 같은 시점에 바꾸도록 요구한다.** 저자의 판정이 한 줄이다 — **그것은 독립 배포
  가능성을 정면으로 거스른다** (5장 §"Lockstep Deployment", p.149).[^newman2021]
  - **완전한 금지는 아니고 빈도가 기준이다** — 마이크로서비스와 소비자 전부를 같은 팀이 관리하고
    한 번뿐인 일이라면 정당화될 수 있으나, **한 번뿐이어야 할 일이 일상 업무가 되면 독립 배포
    가능성이 사라진다.** 저자의 표현으로 **보조 맞춘 배포를 너무 자주 쓰면 머지않아 분산
    모놀리스를 갖게 된다** (5장 §"Which Approach Do I Prefer?", p.152).[^newman2021]
  - 나머지 두 선택지와 저자의 선호는
    [계약을 깨는 변경의 관리](managing-breaking-api-changes.md)에 있다.
- **② 공유 라이브러리의 갱신** — 여러 마이크로서비스가 같은 라이브러리를 쓰더라도 보통 그것을
  **각자의 배포물에 패키징**하므로, 쓰는 판을 올리려면 **마이크로서비스를 다시 배포해야 한다.**
  모든 곳에서 정확히 같은 시점에 갱신하려 하면 **여러 마이크로서비스를 한꺼번에 광범위하게
  배포하는 일**이 된다 (5장 §"Sharing Code via Libraries", p.155).[^newman2021]
  - **그래서 조건부 허용의 조문이 이 성질에서 나온다** — 경계를 넘어 코드를 재사용하려면 **같은
    라이브러리의 여러 판이 동시에 존재할 수 있음을 받아들여야** 하고, 정말로 동시에 갱신해야
    한다면 **전용 마이크로서비스를 봐야 한다** (5장, p.155).[^newman2021] 전문은
    [DRY 원칙](../concepts/dry-principle.md)에 있다.
- **③ 클라이언트 라이브러리의 업그레이드 시점** — 클라이언트 라이브러리를 만든다면 지킬 것의
  마지막이 **클라이언트가 자기 라이브러리를 언제 업그레이드할지 쥐게 하는 것**이고, 저자가 대는
  이유가 곧 이 성질이다 — **서비스를 서로 독립적으로 릴리스할 능력을 유지해야 하기 때문**이다
  (5장 §"Client libraries", p.156).[^newman2021]
- **셋을 관통하는 것** — 이 페이지 위쪽의 성립 조건(느슨한 결합과 안정된 계약)은 **계약의
  모양**에 대한 요구인데, 5장이 지목하는 셋은 전부 **배포 시점의 동시성**에 대한 것이다.
  계약을 잘 지켜도 함께 배포해야 하면 이 성질은 없다.

## 이어지는 페이지

- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 이 성질이 들어 있는
  정의의 본체와 데이터 경계 규칙
- [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md) — 이 성질이
  요구하는 안정된 경계를 실제로 어디에 긋는가
- [마이크로서비스의 고통과 채택 판단](microservice-pain-points-and-adoption.md) — 이 성질을
  얻으려고 치르는 비용의 목록
- [모놀리스와 모듈](../concepts/monolith-versus-modular.md) — 배포 단위로 모놀리스를 정의하는
  쪽. 이 성질의 부재가 곧 모놀리스의 정의다
- [결합 끊기](../concepts/decoupling.md) — "느슨한 결합"이라는 조건의 일반형
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 안정된 계약을 실제로 정의하고
  버저닝하는 방법
- [하위 호환성과 상위 호환성](../concepts/backward-and-forward-compatibility.md) — 계약을
  깨지 않는다는 조건의 정의
- [계약을 깨는 변경의 관리](managing-breaking-api-changes.md) — 그 계약을 결국 깨야 할 때,
  이 성질을 지키며 깨는 법
- [DRY 원칙](../concepts/dry-principle.md) — 공유 코드가 배포를 묶는 자리
- [서비스 결합의 네 종류](service-coupling-types.md) — 이 성질을 갉는 결합의 분류

[^newman2021]: Newman 2021, 서문(p.xvii) · 1장 "What Are Microservices?"
    §"Independent Deployability"(pp.6–7) · §"Owning Their Own State"(pp.8–9) ·
    §"Ease of Deployment"(p.25) — 과 5장 "Implementing Microservice Communication"
    §"Lockstep Deployment"(p.149) · §"Which Approach Do I Prefer?"(p.152) ·
    §"Sharing Code via Libraries"(p.155) · §"Client libraries"(p.156). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은
    따옴표는 곧은 따옴표로 옮겼다. 이 절들에는 코드 목록도 도판도 없다. 5장 쪽 절들의
    전문은 [계약을 깨는 변경의 관리](managing-breaking-api-changes.md)와
    [DRY 원칙](../concepts/dry-principle.md)에 있고 여기에는 이 성질에 걸리는 대목만
    옮겼다 — 그래서 이 절의 직인용은 0건이다.

[^kleppmann2026]: Kleppmann & Riccomini 2026, 5장 "Encoding and Evolution". 이 절은 이
    소스가 이 페이지에 더하는 것만 든다 — 전문은
    [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)에 있다.
