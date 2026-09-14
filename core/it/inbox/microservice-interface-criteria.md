---
type: concept
title: 마이크로서비스 인터페이스 기술의 다섯 조건
status: draft
description: 마이크로서비스 사이 통신 기술을 고르기 전에 그 기술에 요구할 것을 먼저 적어 두는 체크리스트 — 후진 호환을 쉽게 만들 것·인터페이스를 명시적으로 만들 것·API를 기술 중립으로 둘 것·소비자에게 쉽게 만들 것·내부 구현 세부를 감출 것이라는 다섯, 각 조건이 무엇을 막으려는 것인가, 넷째와 다섯째가 서로 당기는 자리(클라이언트 라이브러리가 채택을 쉽게 하면서 결합을 올린다), 그리고 이 다섯이 이 KB의 어느 페이지에서 전문으로 다뤄지는가, 그리고 같은 장의 뒤쪽이 이 다섯을 되부르는 자리 — 명시적 스키마가 정보 은닉의 경계를 긋는다는 조항, 스키마를 두지 않으면 문서가 더 많은 일을 한다는 노동의 이동, 그리고 클라이언트 라이브러리의 상충이 해소되는 조건 셋
generated: { by: "claude-opus-5", at: "2026-09-15T19:00:00Z" }
sources:
  - { id: newman2021, resource: /it/sources/newman2021.md }
---

# 마이크로서비스 인터페이스 기술의 다섯 조건

- [기술을 보기 전에 요구를 적는다](#기술을-보기-전에-요구를-적는다)
- [후진 호환을 쉽게 만들 것](#후진-호환을-쉽게-만들-것)
- [인터페이스를 명시적으로 만들 것](#인터페이스를-명시적으로-만들-것)
- [API를 기술 중립으로 둘 것](#api를-기술-중립으로-둘-것)
- [소비자에게 쉽게 만들 것](#소비자에게-쉽게-만들-것)
- [내부 구현 세부를 감출 것](#내부-구현-세부를-감출-것)
- [넷째와 다섯째가 서로 당긴다](#넷째와-다섯째가-서로-당긴다)
- [5장 후반이 이 다섯을 되부르는 자리](#5장-후반이-이-다섯을-되부르는-자리)
- [이 다섯이 전문으로 다뤄지는 자리](#이-다섯이-전문으로-다뤄지는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **마이크로서비스 사이 통신 기술을 고를 때 그 기술에 무엇을 요구해야 하는가.**

## 기술을 보기 전에 요구를 적는다

- [newman2021](../sources/newman2021.md)이 기술 선택지를 열거하기 전에 조건부터 세우는 이유를
  적는다 — 한 마이크로서비스가 다른 마이크로서비스에 말하는 방법의 선택지가 **어지러울 만큼
  많고**(SOAP인가 XML-RPC인가 REST인가 gRPC인가) **새 선택지가 늘 나온다**. 그래서 구체적인
  기술을 논하기 전에 **우리가 고르는 기술에서 무엇을 원하는지를 먼저 생각하자**는 것이다
  (5장 §"Looking for the Ideal Technology", p.121).[^newman2021]
- **이 다섯은 기술의 목록이 아니라 기술을 재는 자다.** 이어지는 절이 원격 프로시저 호출·REST·
  GraphQL·메시지 브로커를 차례로 평가할 때 되풀이해 걸리는 항목이 이 다섯이고, 같은 장의 뒤쪽이
  다루는 호환 깨짐의 관리와 스키마 논의도 첫째·둘째 조건을 되부른다 (5장, pp.121–123).[^newman2021]

## 후진 호환을 쉽게 만들 것

- 요구의 내용 — 마이크로서비스를 바꿀 때 **소비하는 마이크로서비스와의 호환을 깨지 않도록** 해야
  하고, 그러므로 고르는 기술이 **후진 호환되는 변경을 쉽게 만들도록** 보장해야 한다. 기준선이
  한 줄로 적힌다 (5장, p.121):[^newman2021]

  > Simple operations like adding new fields shouldn't break clients.

- **여기에 검증 요구가 붙는다** — 이상적으로는 우리가 한 변경이 후진 호환인지 **검증할 수 있는
  능력**을 원하고, 그 피드백을 **마이크로서비스를 프로덕션에 배포하기 전에** 받을 길을 원한다
  (5장, p.121).[^newman2021] 곧 이 조건은 "형식이 필드 추가를 견디는가"만이 아니라 "그 사실을
  배포 전에 기계가 말해 주는가"까지를 포함한다.

## 인터페이스를 명시적으로 만들 것

- 요구의 내용 (5장, p.122):[^newman2021]

  > It is important that the interface that a microservice exposes to the outside world is
  > explicit.

  - **두 방향으로 명시적이어야 한다.** 소비자에게는 **그 마이크로서비스가 어떤 기능을 노출하는지**가
    분명해야 하고, 그 마이크로서비스를 손보는 개발자에게는 **바깥쪽을 위해 어떤 기능이 그대로
    남아야 하는지**가 분명해야 한다. 노리는 것은 **마이크로서비스의 변경이 호환을 뜻하지 않게
    깨뜨리는 상황을 피하는 것**이다.
- 수단이 명시된다 — **명시적 스키마(explicit schemas)가 그 일에 크게 기여한다.** 살펴볼 기술 중
  어떤 것은 스키마를 요구하고 어떤 것은 스키마를 선택으로 두는데, 어느 쪽이든 저자는 **명시적
  스키마의 사용을 강하게 권하고**, 거기에 더해 **소비자가 그 마이크로서비스에 무엇을 기대할 수
  있는지가 분명해질 만큼의 뒷받침 문서**를 두라고 적는다 (5장, p.122).[^newman2021] 그 권고의
  근거와 반대 논변의 대질은 [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md)의
  구조적 깨짐과 의미적 깨짐 절에 있다.

## API를 기술 중립으로 둘 것

- 전제가 시간이다 — 지금은 .NET 가게일 수 있으나 **1년 뒤나 5년 뒤는 어떤가**, 그리고 더 생산적일
  수 있는 대안 기술 스택을 실험하고 싶어지면 어떤가 (5장, p.122).[^newman2021]
- 그래서 조문이 이렇다 (5장, p.122):[^newman2021]

  > This means avoiding integration technology that dictates what technology stacks we can use
  > to implement our microservices.

  - 저자가 이것을 **선택지를 열어 두는 일**이라 부르고, 자기가 마이크로서비스를 좋아하는 이유도
    거기라고 적는다 (5장, p.122).[^newman2021]

## 소비자에게 쉽게 만들 것

- 요구의 내용 (5장, p.122):[^newman2021]

  > We want to make it easy for consumers to use our microservice.

  - 이유가 한 문장으로 붙는다 — **아름답게 분해된 마이크로서비스라도 소비자로서 그것을 쓰는 비용이
    하늘을 찌르면 별 값어치가 없다** (5장, p.122).[^newman2021]
- 그런데 **수단이 서로 어긋난다** — 이상적으로는 클라이언트에게 **기술 선택의 완전한 자유**를 주고
  싶고, 다른 한편으로 **클라이언트 라이브러리를 제공하면 채택이 쉬워진다.** 그러나 그런 라이브러리는
  **우리가 이루려는 다른 것들과 흔히 양립하지 않는다** — 소비자를 편하게 하려고 클라이언트
  라이브러리를 쓰면 **결합이 올라가는 대가**가 따라온다 (5장, p.122).[^newman2021]

## 내부 구현 세부를 감출 것

- 요구의 내용과 그 연쇄 (5장, p.123):[^newman2021] 소비자가 우리 내부 구현에 묶이면 **결합이
  올라가고**, 그러면 마이크로서비스 안의 무언가를 바꾸고 싶을 때 **소비자도 함께 바꾸게 만들어
  그들을 깨뜨린다.** 그것이 **변경 비용을 올리고** — 저자가 "정확히 우리가 피하려는 것"이라 적는다
  — 나아가 **소비자를 업그레이드해야 한다는 두려움 때문에 변경 자체를 덜 원하게 되어 서비스 안에
  기술 부채가 쌓인다.**
- 그래서 결론이 금지 조항이다 (5장, p.123):[^newman2021]

  > So any technology that pushes us to expose internal representation detail should be avoided.

  - **이 조건이 뒤에서 기술을 떨어뜨리는 자리가 있다.** 같은 장이 RPC의 기술 결합을 평가하면서,
    자바 RMI처럼 특정 플랫폼에 묶이는 기제는 **내부 기술 구현 세부를 노출하는 한 형태**로
    볼 수 있다고 적는다 (5장, p.124).[^newman2021] 전문은
    [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md)에 있다.

## 넷째와 다섯째가 서로 당긴다

- **다섯이 독립적인 항목이 아니다.** 소비자를 쉽게 하려고 클라이언트 라이브러리를 내주면 넷째는
  좋아지고 다섯째는 나빠진다 — 저자 자신이 넷째 조건 안에서 그 상충을 적어 두고, 클라이언트
  라이브러리의 결합 문제를 같은 장의 뒤쪽(§"DRY and the Perils of Code Reuse in a Microservice
  World")으로 미룬다 (5장, pp.122·131).[^newman2021]
- 같은 상충이 REST를 평가할 때 되풀이된다 — REST over HTTP는 역사적으로 RPC 구현처럼
  클라이언트 쪽 코드를 생성할 수 없었고, 그래서 **REST API를 내면서 소비자용 클라이언트 라이브러리를
  함께 만드는 일이 잦았다.** 그 라이브러리가 **클라이언트와 서버 사이 결합의 문제를 일으킨다**
  (5장 §Challenges, p.131).[^newman2021]

## 5장 후반이 이 다섯을 되부르는 자리

**이 다섯은 기술을 고를 때만 쓰이는 자가 아니다.** 같은 장의 뒤쪽이 변경과 문서화와 디스커버리를
다루며 같은 항목을 다시 건다.

- **첫째(후진 호환)를 되부르는 곳** — §"Avoiding Breaking Changes"의 다섯 생각 중 **알맞은 기술
  고르기**가 이 조건의 되풀이이고, 거기서 저자가 재는 것은 **형식이 필드 추가를 견디는가**
  (프로토콜 버퍼의 필드 번호, 적재물에 스키마를 함께 싣는 Avro)와 **HATEOAS 같은 극단**이다
  (5장 §"Right Technology", p.146).[^newman2021] 그리고 이 조건에 붙어 있던 검증 요구("배포 전에
  기계가 말해 주는가")가 §"Catch Accidental Breaking Changes Early"에서 **스키마 비교 도구가
  CI 빌드를 실패시키게 하라**는 실무 항목이 된다 (5장, p.148).[^newman2021] 전문은
  [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md)에 있다.
- **둘째(명시적 인터페이스)를 되부르는 곳이 둘이다.**
  - 하나는 §"Explicit Interface"이고, 거기서 이 조건이 **정보 은닉의 언어로 다시 쓰인다** —
    **명시적 스키마는 정보 은닉의 경계를 더 명시적으로 만들고, 스키마에 드러난 것은 정의상
    숨겨진 것이 아니다** (5장, p.147).[^newman2021] **이것이 둘째 조건과 다섯째 조건을 잇는
    자리다** — 명시적 인터페이스와 내부 은닉이 서로 다투는 항목이 아니라 **같은 선의 안팎**임을
    말한다.
  - 다른 하나는 §"Documenting Services"다. 명시적 스키마는 **엔드포인트가 무엇을 드러내는지
    이해하기 쉽게 하는 데 크게 기여하지만 그것만으로는 흔히 부족하다** — 스키마는 구조를 보이되
    **엔드포인트의 행동을 전하는 데는 멀리 가지 못하므로** 소비자가 쓰는 법을 이해하려면 좋은
    문서가 여전히 필요할 수 있다 (5장 §"Explicit Schemas", pp.169–170).[^newman2021]
    - **스키마를 쓰지 않기로 하면 문서가 더 많은 일을 한다** — 엔드포인트가 무엇을 하는지에 더해
      **인터페이스의 구조와 세부까지 문서가 적어야 하고**, 게다가 **명시적 스키마가 없으면 문서가
      실제 엔드포인트와 맞춰져 있는지 알아내기가 더 어렵다.** 저자의 표현으로 **낡은 문서는 상시
      문제이고, 적어도 명시적 스키마는 문서가 최신일 가능성을 더 준다** (5장,
      p.170).[^newman2021]
    - **이것이 이 KB의 다른 절과 같은 모양이다** — [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md)이
      "스키마가 없으면 구조적 깨짐을 잡는 부담이 테스트로 넘어간다"고 적는 자리와 **노동이 옮겨
      가는 방향이 같다.** 스키마를 두지 않으면 그 일을 다른 산출물이 떠맡는다.
- **넷째와 다섯째의 상충이 해소되는 곳** — 이 페이지의
  [넷째와 다섯째가 서로 당긴다](#넷째와-다섯째가-서로-당긴다)가 저자를 따라 뒤로 미룬 자리가
  §"DRY and the Perils of Code Reuse in a Microservice World"의 클라이언트 라이브러리 절이다.
  저자의 결론은 **클라이언트 라이브러리를 금지하는 것이 아니라 셋을 지키라는 것**이다 — 전송
  프로토콜을 다루는 코드와 목적지 서비스에 관련된 코드를 가를 것, 라이브러리를 강제할지 정할 것,
  그리고 **업그레이드 시점을 클라이언트가 쥐게 할 것**이다 (5장 §"Client libraries",
  p.156).[^newman2021] 전문은 [DRY 원칙](../concepts/dry-principle.md)에 있다.
- **다섯 조건 밖에서 5장 후반이 새로 세우는 요구가 둘 있다.** 이 체크리스트에는 없던 것이라
  적어 둔다.
  - **찾을 수 있는가** — 인스턴스가 자신을 등록하고 소비자가 그것을 찾는 문제는 기술 선택의
    조건이 아니라 배치의 문제로 따로 다뤄진다.
    [서비스 디스커버리와 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md)이
    그 자리다.
  - **바뀔 때 무엇을 하는가** — 다섯 조건을 다 만족해도 깨는 변경은 남고, 그때의 선택지는
    [계약을 깨는 변경의 관리](managing-breaking-api-changes.md)에 있다.

## 이 다섯이 전문으로 다뤄지는 자리

이 페이지는 체크리스트의 조문만 둔다. 각 조건이 실제로 무엇을 요구하는지는 이 KB의 다른
페이지가 원전 층과 함께 갖고 있다.

- 첫째(후진 호환) — [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md).
  방향이 요청과 응답으로 갈려 걸리는 규칙과 그 강제 방식이 거기 있다.
- 둘째(명시적 인터페이스) — [데이터 인코딩 형식](../concepts/data-encoding-formats.md)과
  [소비자 주도 계약](../concepts/consumer-driven-contracts.md). 스키마가 무엇을 주는가와,
  계약을 제공자가 아니라 소비자의 기대에서 파생시키는 배치다.
- 셋째(기술 중립) — [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md)의
  기술 결합 절과 [웹 서비스와 REST](../concepts/web-services-and-rest.md).
- 넷째(소비자 편의) — [웹 서비스와 REST](../concepts/web-services-and-rest.md)의 IDL과 서비스
  프레임워크 절.
- 다섯째(내부 은닉) — [정보 은닉과 누출](../concepts/information-hiding-and-leakage.md).
  이 조건의 일반형이 거기서 모듈 설계의 문제로 서술된다.

## 이어지는 페이지

- [마이크로서비스 통신 스타일](microservice-communication-styles.md) — 이 조건들을 적용하기 전에
  먼저 정하는 것. 무엇으로 말할지보다 어떤 방식으로 협업할지가 앞선다
- [독립 배포 가능성](independent-deployability.md) — 다섯 조건이 함께 지키려는 그 성질
- [서비스 결합의 네 종류](service-coupling-types.md) — 넷째와 다섯째가 다투는 그 결합의 분류
- [정보 은닉과 누출](../concepts/information-hiding-and-leakage.md) — 다섯째 조건의 일반형
- [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md) — 이 자로 잰
  첫째 기술
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 이 자로 잰 둘째 기술
- [GraphQL](../concepts/graphql.md) — 이 자로 잰 셋째 기술
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 이 자로 잰 넷째 기술의 기반
- [계약을 깨는 변경의 관리](managing-breaking-api-changes.md) — 다섯 조건을 다 만족해도
  남는 문제
- [서비스 디스커버리와 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md) —
  이 체크리스트에 없던 요구. 그 기술을 어디서 찾는가
- [DRY 원칙](../concepts/dry-principle.md) — 넷째와 다섯째의 상충이 실제로 해소되는 자리

[^newman2021]: Newman 2021, 5장 "Implementing Microservice Communication"
    §"Looking for the Ideal Technology"(pp.121–123) — 다섯 소절
    §"Make Backward Compatibility Easy"(p.121) · §"Make Your Interface Explicit"(p.122) ·
    §"Keep Your APIs Technology Agnostic"(p.122) · §"Make Your Service Simple for
    Consumers"(p.122) · §"Hide Internal Implementation Detail"(p.123). 기술 결합이 내부
    구현 노출의 한 형태라는 대목은 §"Technology Choices" 안의 RPC 절(p.124)이고,
    클라이언트 라이브러리의 결합은 §REST의 §Challenges(p.131)다. **같은 장 후반에서
    이 다섯을 되부르는 네 자리가 마지막 절에 합류했다** — §"Right Technology"(p.146) ·
    §"Explicit Interface"(pp.146–147) · §"Catch Accidental Breaking Changes Early"(p.148) ·
    §"Client libraries"(p.156) · §"Documenting Services"의 §"Explicit Schemas"
    (pp.169–170). 그 절들의 전문은 각각
    [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md)과
    [DRY 원칙](../concepts/dry-principle.md)에 있고 여기에는 다섯 조건에 걸리는 대목만
    옮겼다. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은
    따옴표는 곧은 따옴표로, 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었다.
    이 절에는 도판도 코드 목록도 없다.
