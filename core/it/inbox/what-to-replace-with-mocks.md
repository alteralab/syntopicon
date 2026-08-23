---
type: concept
title: 무엇을 목으로 대체할 것인가
description: 목을 쓸 자리를 소유나 편의가 아니라 관찰 가능성으로 가르는 판정과 그 근거 — 대역 다섯을 목과 스텁 둘로 묶는 축, 스텁과의 상호작용을 단언하지 말라는 규칙과 과잉 명세, 내부 통신은 구현 세부이고 시스템 간 통신은 관찰 가능한 행위라는 판정, 프로세스 밖 의존을 managed와 unmanaged로 가르는 정의와 후방 호환이라는 근거, 둘 다인 의존과 실물을 쓸 수 없는 경우의 처방, 목을 통합 테스트에만 두고 시스템 가장자리에서 검증하며 소유한 타입만 목하라는 지침 넷, 저자가 고전 학파를 고르면서 그 학파도 이상적이지 않다고 적는 자리, 그리고 이 판정이 목 객체 원전과 갈리는 축과 갈리지 않는 공통 지반
generated: { by: "claude-opus-5", at: "2026-08-24T06:00:00Z" }
status: draft
contradicts: [mock-objects-for-role-discovery]
sources:
  - { id: khorikov2020-unit-testing, resource: /it/sources/khorikov2020-unit-testing.md }
---

# 무엇을 목으로 대체할 것인가

- [이 소스의 지위와 이 페이지가 담지 않는 것](#이-소스의-지위와-이-페이지가-담지-않는-것)
- [대역 다섯이 둘로 묶인다](#대역-다섯이-둘로-묶인다)
- [스텁과의 상호작용을 단언하지 않는다](#스텁과의-상호작용을-단언하지-않는다)
- [내부 통신과 시스템 간 통신](#내부-통신과-시스템-간-통신)
- [managed 의존과 unmanaged 의존](#managed-의존과-unmanaged-의존)
- [경계가 흐려질 때와 실물을 못 쓸 때](#경계가-흐려질-때와-실물을-못-쓸-때)
- [목을 쓸 때의 지침 넷](#목을-쓸-때의-지침-넷)
- [저자가 고전 학파를 고르는 이유](#저자가-고전-학파를-고르는-이유)
- [학파 이름의 대응](#학파-이름의-대응)
- [이 판정과 갈리는 자리](#이-판정과-갈리는-자리)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트에서 무엇을 실물로 두고 무엇을 목으로 바꿔야 하는가, 그리고 그 선을
무엇으로 긋는가.**

## 이 소스의 지위와 이 페이지가 담지 않는 것

- **근거 등급은 `practitioner-norm`이다.** 이 책에는 측정이 없고 인용할 수치가 없다.
  아래 판정들은 학술 근거가 아니라 실무 규범이며, 저자의 자기 규정과 판(MEAP V03)에 관한
  실측은 [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md)의
  첫 절과 [소스 메타](../sources/khorikov2020-unit-testing.md)가 정본이다.
- **이 페이지의 판정은 앞 페이지의 판정에서 연역된다.** 거짓 양성의 유일한 원인이 구현
  세부에 대한 결합이라면, 대역을 어디에 쓸지는 **무엇이 구현 세부인가**의 문제가 된다.
  이 책이 실제로 그 순서로 논증한다.
- **이 물음에 대해 대조 대상으로 지목됐던 문헌 셋이 이제 이 KB에 있다.** 원문 대조가
  끝났으므로 그 결과를 여기 적는다.
  - **Freeman·Pryce·Mackinnon·Walnes, "Mock Roles, not Objects"(2004)** — 소유한 타입만
    목하라는 명제의 원전이자 **이 페이지의 모순 상대**다.
    [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md)가
    그 페이지다. **반입 판정 대장은 이것을 이 책의 "정확한 역명제"로 기재했으나 그 기재는
    틀렸다** — 이 책 9장 §9.2.4가 그 지침을 채택하며 **"I fully agree with this analysis"**
    라고 적고, 원문 §4.1도 같은 지침을 적는다. **갈리는 축은 다른 데 있다**(아래
    [이 판정과 갈리는 자리](#이-판정과-갈리는-자리)).
  - **Spadini et al., MSR 2017**과 **Xiao et al., EMSE 2024** — 실제 관행을 잰 실증 둘이고
    한 페이지가 소유한다:
    [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md).
    **방향이 이 책과 어긋나고**(그림 2의 `Database` 범주 의존 72%가 목으로 대체된다),
    **뒤엣것은 "무엇을 언제 목할 것인가"를 미해결로 명시한다.**
  - **수치는 이 페이지가 옮기지 않는다** — 분모와 그림 위치가 함께 가야 하므로 그
    페이지에서 읽는다.

## 대역 다섯이 둘로 묶인다

- **총칭의 정의부터 옮긴다** (5장 §5.1.1):[^khorikov2020-unit-testing]

  > A test double is an overarching term that describes all kinds of non-production-ready,
  > fake dependencies in tests.

  한국어 대응은 테스트 대역(test double)이다. 저자가 Meszaros의 다섯 갈래(dummy·stub·spy·
  mock·fake)를 그대로 받되 각주 [2]로 그 출처를 지목하고, **둘로 묶는다.**
- **묶는 축은 상호작용의 방향이다** (같은 절):[^khorikov2020-unit-testing]

  > Mocks help to emulate and examine outcoming interactions. These interactions are calls
  > the SUT makes to its dependencies to change their state.
  >
  > Stubs help to emulate incoming interactions. These interactions are calls the SUT
  > makes to its dependencies to get input data.

  - 나가는 상호작용(outcoming interaction)은 부수 효과를 남기는 호출이고, 들어오는
    상호작용(incoming interaction)은 입력을 받아 오는 호출이다.
  - **나머지 차이는 구현 세부로 강등된다** (같은 절) — 스파이는 손으로 쓴 목이고, 더미와
    가짜는 스텁과 같은 역할을 하되 정교함이 다를 뿐이라고 적는다. **가짜(fake)를 가르는
    기준이 "아직 없는 의존을 대신하려고 만들었는가"라는 만든 이유**라는 것도 여기 있다.
  - **목만이 검사까지 한다** (같은 절) — **"Mocks help to emulate and examine interactions
    between the SUT and its dependencies, while stubs only help to emulate those
    interactions."**[^khorikov2020-unit-testing]
- **도구로서의 목과 대역으로서의 목이 다른 낱말이다** (5장 §5.1.2) — 목 라이브러리의
  클래스는 목(도구)이고 그 인스턴스가 목(대역)인데, **같은 도구로 스텁도 만든다.**
  그래서 목 라이브러리를 썼다는 사실이 목을 썼다는 증거가 아니다.[^khorikov2020-unit-testing]
- **명령·질의 분리(CQS)와 정확히 겹친다** (5장 §5.1.5):[^khorikov2020-unit-testing]

  > Test doubles that substitute commands become mocks. Similarly, test doubles that
  > substitute queries are stubs.

  명령(command)은 부수 효과를 내고 값을 돌려주지 않으며, 질의(query)는 부수 효과가 없고
  값을 돌려준다. **부수 효과가 있는 자리에만 목이 선다**는 것이 이 대응의 뜻이다.
- **하나가 둘을 겸할 수 있다** (5장 §5.1.4) — 한 대역이 어떤 메서드에서는 답을 심어 주고
  다른 메서드에서는 호출을 검사하면, 그것은 여전히 목이라고 부른다.[^khorikov2020-unit-testing]

## 스텁과의 상호작용을 단언하지 않는다

- **규칙이 한 줄이다** (5장 §5.1.3, MEAP 판 표지 문자열을 뗀
  문면):[^khorikov2020-unit-testing]

  > Asserting interactions with stubs is a common anti-pattern that leads to fragile tests.

- **근거는 최종 결과가 아니라는 것이다** (같은 절):[^khorikov2020-unit-testing]

  > A call from the SUT to a stub is not part of the end result the SUT produces. Such a
  > call is only a means to produce the end result: a stub provides input from which the
  > SUT then generates the output.

- **이름이 붙어 있다** (같은 절) — 최종 결과가 아닌 것을 검사하는 일반형이 **과잉
  명세(overspecification)**이고, 그것은 대개 상호작용을 검사할 때 일어난다. 저자가 둘의
  난이도를 가른다: **스텁 쪽 위반은 찾기 쉽고(스텁과의 상호작용은 아예 검사하면 안 되므로),
  목 쪽은 복잡하다** — 목의 모든 사용이 취약성을 낳는 것은 아니기 때문이다.[^khorikov2020-unit-testing]

## 내부 통신과 시스템 간 통신

- **통신이 둘로 갈린다** (5장 §5.3.2) — 내부 통신(intra-system communication)은 응용
  안 클래스들 사이의 통신이고, 시스템 간 통신(inter-system communication)은 응용이 다른
  응용과 나누는 통신이다.[^khorikov2020-unit-testing]
- **판정 문장이 한 줄이다** (같은 절, 판 표지 문자열을 뗀 문면):[^khorikov2020-unit-testing]

  > Intra-system communications are implementation details; inter-system communications
  > are not.

- **각각의 근거가 다르다** (같은 절):[^khorikov2020-unit-testing]
  - 내부 통신이 구현 세부인 이유는 **도메인 클래스들이 한 연산을 해내려고 거치는 협력이
    그 클래스들의 관찰 가능한 행위가 아니기 때문**이다. 클라이언트의 목표와 직접 연결되지
    않는다.
  - 시스템 간 통신이 관찰 가능한 행위인 이유는 **후방 호환성(backward compatibility)**이다.
    응용을 아무리 리팩터링해도 외부 응용이 알아들을 수 있도록 통신 패턴은 그대로 있어야
    한다 — 외부 시스템은 배포 주기가 다르거나 통제 밖에 있어서 함께 바꿀 수 없기 때문이다.
- **그래서 결론이 이 문장이다** (같은 절):[^khorikov2020-unit-testing]

  > The use of mocks is beneficial when verifying the communication pattern between your
  > system and external applications. Conversely, using mocks to verify communications
  > between classes inside your system results in tests that couple to implementation
  > details and therefore fall short of the resistance-to-refactoring metric.

- **저자가 같은 업무 시나리오로 정당한 목과 부당한 목을 나란히 보인다** (5장 §5.3.3) —
  구매 사용례에서 SMTP 서비스로 나가는 영수증 호출을 목으로 검사하는 것은 정당하고,
  같은 시나리오 안에서 도메인 클래스 둘 사이의 재고 차감 호출을 목으로 검사하는 것은
  취약한 테스트를 만든다. **두 호출을 가르는 것은 응용 경계를 넘는가뿐이다.**[^khorikov2020-unit-testing]
- **그리고 "목이 행위를 검증한다"는 통념을 저자가 거의 전면 부정한다**
  (5장 §5.4.2):[^khorikov2020-unit-testing]

  > Mocks are often said to verify behavior. In the vast majority of cases, they don't.
  > The way each individual class interacts with neighboring classes in order to achieve
  > some goal has nothing to do with observable behavior; it's an implementation detail.

  - 비유가 붙는다 (같은 절) — 클래스 사이의 통신을 검증하는 것은 **뇌의 뉴런들이 주고받는
    신호를 재서 사람의 행동을 알아내려는 일**과 같다는 것이다. 결이 너무 곱다.
  - **목이 행위와 관계있는 경우가 조건 두 개로 좁혀진다** (같은 절) — 응용 경계를 넘는
    상호작용일 때, 그리고 그 부수 효과가 외부 세계에 보일 때뿐이다.[^khorikov2020-unit-testing]

## managed 의존과 unmanaged 의존

**이 KB는 이 둘의 역어를 만들지 않고 원어를 유지한다.** "관리/비관리"로 옮기면 판정 기준이
이름에서 사라지기 때문이다 — 아래 정의가 보이듯 이 구분의 기준은 소유나 관리가 아니라
**외부에서 관찰되는가**다.

- **정의를 문면 그대로 옮긴다** (8장 §8.2.1):[^khorikov2020-unit-testing]

  > Managed dependencies (out-of-process dependencies you have full control over). These
  > dependencies are only accessible through your application; interactions with them
  > aren't visible to the external world. A typical example is a database.
  >
  > Unmanaged dependencies (out-of-process dependencies you don't have full control over).
  > Interactions with such dependencies are observable externally. Examples include an
  > SMTP server and a message bus: both produce side effects visible to other applications.

- **처방이 한 줄이다** (같은 절, 판 표지 문자열을 뗀 문면):[^khorikov2020-unit-testing]

  > Use real instances of managed dependencies; replace unmanaged dependencies with mocks.

  - **그 "real instance"가 무엇인지는 이 책이 답하지 않는다.** 데이터베이스를 실물로 쓰라는
    말이 **같은 엔진**을 뜻하는지, 인메모리(in-memory) 공급자(provider)나 다른 데이터베이스로
    바꿔친 것도 실물로 치는지가 이 책의 주제가 아니다. 그 자리를 채운 문헌 셋이 이제 이 KB에
    있다 —
    [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md)이
    그 페이지이고, **이 처방의 실행 층**이다.
  - **그래서 이 처방을 문자 그대로 지키면서도 실패할 수 있다.** "목을 쓰지 않았다"는 조건이
    인메모리 공급자로 바꿔치기를 배제하지 못하기 때문이다. 그쪽 세 소스가 잃는 것으로
    드는 것이 트랜잭션 의미론·SQL 방언·제약과 격리 수준인데, **전부 이 책이 실물을 쓰라고
    한 이유와 같은 층의 것**이다.
- **연결 고리가 명시된다** (같은 절) — **"communications with managed dependencies are
  implementation details. Conversely, communications with unmanaged dependencies are part
  of your system's observable behavior."** 곧 이 구분은 위
  [내부 통신과 시스템 간 통신](#내부-통신과-시스템-간-통신)의 판정을 프로세스 밖 의존에
  적용한 것이다.[^khorikov2020-unit-testing]
- **5장이 이미 같은 말을 다른 낱말로 해 둔다** (5장 §5.4.1) — **"Not all out-of-process
  dependencies should be mocked out."** 외부에서 관찰될 수 없는 프로세스 밖 의존은 사실상
  응용의 일부로 작동하므로, 그것과의 통신 패턴은 구현 세부가 된다.[^khorikov2020-unit-testing]
  - **응용 데이터베이스가 그 예다** (같은 절) — 클라이언트에게 완전히 감춰져 있으므로
    **"you can even replace it with an entirely different storage mechanism, and no one
    will notice."** 그래서 저자가 이렇게 적는다: **"The database and your application must
    be treated as one system."**[^khorikov2020-unit-testing]
  - **깨지는 방식까지 적힌다** (같은 절) — 통제권이 온전한 프로세스 밖 의존에 목을 쓰면
    **테이블을 쪼개거나 저장 프로시저의 인자 타입을 바꿀 때마다 테스트가 붉어진다.**[^khorikov2020-unit-testing]
- **인터페이스를 언제 두는가도 여기서 정해진다** (8장 §8.4.2):[^khorikov2020-unit-testing]

  > Therefore, don't introduce interfaces for out-of-process dependencies unless you need
  > to mock those dependencies out. You only mock out unmanaged dependencies, and so the
  > guideline can be boiled down to this: use interfaces for unmanaged dependencies only.
  > Still inject managed dependencies into the controller explicitly but use concrete
  > classes for that.

  - 근거는 두 겹이다 (8장 §8.4.1~§8.4.2) — 구현이 하나뿐인 인터페이스는 추상이 아니고
    (**"Genuine abstractions are discovered not invented"** · 진짜 추상이려면 구현이 둘
    이상이어야 한다), 미래를 위해 미리 두는 것은 YAGNI 위반이라는 것이다. **그러므로
    구현 하나짜리 인터페이스의 유일한 정당한 이유가 목을 가능하게 하는 것이다.**[^khorikov2020-unit-testing]

## 경계가 흐려질 때와 실물을 못 쓸 때

- **한 의존이 둘 다일 수 있다** (8장 §8.2.2) — 다른 응용이 접근하는 데이터베이스가 그
  예다. 처방은 **의존을 쪼개는 것**이다: 외부에 보이는 테이블은 unmanaged 의존으로 보고
  목으로 대체하며, 나머지는 managed 의존으로 보고 최종 상태를 검사한다.[^khorikov2020-unit-testing]
  - 저자가 그 테이블들을 **"in effect act as a message bus with its rows playing the role
    of messages"**라고 적는다. 그리고 데이터베이스로 시스템을 통합하는 것 자체를 나쁜
    방식으로 판정하며 API나 메시지 버스를 권한다.[^khorikov2020-unit-testing]
- **실물을 쓸 수 없어도 목으로 가지 않는다** (8장 §8.2.3):[^khorikov2020-unit-testing]

  > Should you mock the database out anyway, despite it being a managed dependency? No,
  > because mocking out a managed dependency compromises the integration tests'
  > resistance to refactoring.

  - **대신 통합 테스트를 아예 쓰지 말라는 것이 처방이다** (같은 절) —
    **"If you can't test the database as is, don't write integration tests at all and
    instead focus exclusively on unit testing of the domain model."** 근거는 그렇게 만든
    통합 테스트가 단위 테스트 위에 더해 주는 것이 **컨트롤러가 어떤 리포지터리 메서드를
    부르는지**뿐이라는 것이다.[^khorikov2020-unit-testing]
  - 같은 논리의 일반형이 8장에 팁으로 적혀 있다 — **"No tests are better than bad tests.
    A test that doesn't provide significant value is a bad test."**(8장 §8.1.3)[^khorikov2020-unit-testing]

## 목을 쓸 때의 지침 넷

저자가 9장에서 지침을 모아 놓는다. 앞의 판정(unmanaged 의존에만)이 **"about two thirds of
success"**라고 적고 나머지를 여기 둔다(9장 도입).[^khorikov2020-unit-testing]

- **① 시스템의 가장 바깥 가장자리에서 검증한다** (9장 §9.1.1, 판 표지 문자열을 뗀 문면):[^khorikov2020-unit-testing]

  > When mocking, always adhere to the following guideline: verify interactions with
  > unmanaged dependencies at the very edges of your system.

  - 이유는 감싸개(wrapper)를 목으로 대체하면 그 감싸개 안쪽 코드가 검사 범위에서 빠지기
    때문이다 — 저자의 예에서 도메인 메시지를 정의하는 인터페이스가 아니라 그것이 올라타는
    실제 버스 인터페이스가 가장자리다.[^khorikov2020-unit-testing]
  - **가장자리라고 다 같은 정밀도를 요구하지는 않는다** (9장 §9.1.3) — 메시지 버스는 구조를
    한 글자도 바꾸면 안 되지만 로그의 정확한 텍스트 구조는 그만큼 중요하지 않다고 적고,
    그래서 로거는 도메인 로거 수준에서 목으로 두는 것으로 충분하다고 판정한다.[^khorikov2020-unit-testing]
- **② 목은 통합 테스트에만 쓴다** (9장 §9.2.1, 판 표지 문자열을 뗀 문면):[^khorikov2020-unit-testing]

  > Mocks are for integration tests only. Don't use mocks in unit tests.

  - 논증이 삼단이다 (같은 절) — 업무 논리와 오케스트레이션을 가르면 도메인 모델과
    컨트롤러 두 층이 생기고, 프로세스 밖 의존과 이야기하는 것은 컨트롤러뿐이며, 목은
    unmanaged 의존에만 쓰므로, 목은 컨트롤러를 검사할 때만 나온다는 것이다.[^khorikov2020-unit-testing]
  - **"테스트당 목 하나"는 오해라고 못 박는다** (9장 §9.2.2) — 목의 수는 그 연산에 참여하는
    unmanaged 의존의 수로 정해지지 사람이 고르는 것이 아니다. 그 밑에 깔린 더 근본적인
    오해가 **단위를 코드의 단위로 읽는 것**이라고 적는다.[^khorikov2020-unit-testing]
- **③ 호출 횟수까지 검증한다** (9장 §9.2.3) — 기대한 호출이 있는지만이 아니라 기대하지
  않은 호출이 없는지도 봐야 한다. 근거는 다시 후방 호환성이다 — **외부가 기대하는 메시지를
  빠뜨려서도 안 되고 예상치 못한 메시지를 내서도 안 된다.**[^khorikov2020-unit-testing]
- **④ 소유한 타입만 목한다** (9장 §9.2.4):[^khorikov2020-unit-testing]

  > The last guideline I'd like to talk about is mocking only types that you own. It was
  > first introduced by Steve Freeman and Nat Pryce. The guideline states that you should
  > always write your own adapters on top of third-party libraries and mock those adapters
  > instead of the underlying types.

  - **저자가 그 원전의 논거 셋을 옮기고 동의를 명시한다** (같은 절) — 서드파티 코드의
    동작을 깊이 알기 어렵다는 것, 내장 인터페이스를 목하면 목한 동작이 실제와 맞는지
    보장할 수 없다는 것, 어댑터가 비본질적 기술 세부를 감추고 관계를 자기 도메인 언어로
    다시 적는다는 것이다. 그리고 **"I fully agree with this analysis."**[^khorikov2020-unit-testing]
    - **각주가 쪽 번호까지 지목한다** (9장 각주 [5]) — **"See page 69 in Growing
      Object-Oriented Software, Guided by Tests by Steve Freeman and Nat Pryce
      (Addison-Wesley Professional, 2009)."** 어댑터를 안티커럽션 계층으로 부르는 대목의
      각주 [6]은 Evans의 *Domain-Driven Design*을 가리킨다.[^khorikov2020-unit-testing]
    - **그러므로 이 지침에 관한 한 이 책과 Freeman & Pryce는 대립하지 않는다.** 원전의
      OOPSLA 논문이 아니라 2009년 책을 지목한다는 것, 그리고 저자가 그것을 자기 지침으로
      채택한다는 것이 확보본에서 확인된 사실이다.
  - **적용 범위가 좁혀진다** (같은 절) — 이 지침은 프로세스 안 의존에는 걸리지 않는다.
    날짜·시간 API처럼 unmanaged 의존에 닿지 않는 라이브러리는 그대로 쓰면 되고, 외부에
    보이지 않는 데이터베이스에 접근하는 ORM도 감쌀 필요가 없다고 적는다.[^khorikov2020-unit-testing]

## 저자가 고전 학파를 고르는 이유

- **선택을 두 번 밝히고 두 번 다 이유를 적는다.** 2장에서 먼저다
  (2장 §2.3):[^khorikov2020-unit-testing]

  > As I mentioned previously, I prefer the classical school of unit testing. It tends to
  > produce tests of higher quality and thus is better suited for achieving the ultimate
  > goal of unit testing, which is the sustainable growth of your project. The reason is
  > fragility: tests that use mocks tend to be more brittle than classical tests.

- **두 학파를 가르는 것은 격리(isolation)라는 낱말의 뜻 하나다** (2장 §2.1·§2.2) — 런던
  학파는 **대상 시스템을 협력자로부터** 격리하는 것으로 읽고, 고전 학파는 **테스트를 서로**
  격리하는 것으로 읽는다. 나머지 차이가 전부 여기서 흘러나온다고 저자가 적는다.[^khorikov2020-unit-testing]

  **같은 표가 2장(표 2.1)과 5장(표 5.2)에 두 번 실린다. 열 이름과 칸 문면은 원문
  그대로다.**[^khorikov2020-unit-testing]

  | | Isolation of… | A unit is… | Uses test doubles for… |
  |---|---|---|---|
  | London school | Units | A class | All but immutable dependencies |
  | Classical school | Unit tests | A class or a set of classes | Shared dependencies |
- **저자가 런던 학파의 이점 셋을 먼저 나열하고 하나씩 반박한다** (2장 §2.3~§2.3.4) —
  더 고운 알갱이, 얽힌 객체 그래프를 테스트하기 쉬움, 실패 지점의 정확한 지목이다.[^khorikov2020-unit-testing]
  - **알갱이에 대한 반박** (2장 §2.3.1) — 단위는 코드의 단위가 아니라 **행위의
    단위**이고, 그 행위를 구현하는 데 든 클래스 수는 무관하다. 저자가 개를 부르는 비유를
    든다: "부르면 온다"가 하나의 이야기이고, 다리와 머리와 꼬리의 움직임을 따로 적은 것은
    이야기가 아니라는 것이다.[^khorikov2020-unit-testing]
  - **객체 그래프에 대한 반박** (2장 §2.3.2) — 큰 그래프를 어떻게 테스트할지 궁리하는
    대신 **그런 그래프를 갖지 않는 쪽**에 집중하라는 것이다. 테스트하기 어렵다는 사실
    자체가 설계 문제를 가리키는 좋은 부정 지표(negative indicator)이고, 목은 그 문제를
    **가릴 뿐 없애지 않는다**고 적는다.[^khorikov2020-unit-testing]
  - **연쇄 실패에 대한 반박** (2장 §2.3.3) — 테스트를 자주 돌리면 마지막 편집이 원인임을
    알고, 하나를 고치면 나머지가 함께 낫는다. 게다가 연쇄 실패에는 값이 있다 — **한 결함이
    많은 테스트를 무너뜨렸다는 것은 그 코드가 그만큼 값진 자리라는 정보**라는 것이다.[^khorikov2020-unit-testing]
  - **그리고 진짜 반대 논거는 따로 있다** (2장 §2.3.4) — **"the most crucial distinction
    between the schools is the issue of over-specification: that is, coupling the tests to
    the SUT's implementation details."**[^khorikov2020-unit-testing]
- **5장이 그 논거를 완성한다** (5장 §5.4):[^khorikov2020-unit-testing]

  > The London school encourages the use of mocks for all but immutable dependencies and
  > doesn't differentiate between intra-system and inter-system communications. As a
  > result, tests check communications between classes just as much as they check
  > communications between your application and external systems.

  - **핵심 비판이 "목을 많이 쓴다"가 아니라 "구분하지 않는다"라는 데 있다.** 무차별적
    사용(indiscriminate use)이 문제이고, 그 결과가 리팩터링 내성의 상실이다.
- **그런데 저자가 고전 학파도 이상적이지 않다고 적는다** (같은 절):[^khorikov2020-unit-testing]

  > But the classical school is not ideal in its treatment of inter-system communications,
  > either. This school also encourages excessive use of mocks, albeit not as much as the
  > London school.

  - **이 문장이 이 페이지에서 가장 자주 잊히는 자리다.** 고전 학파는 공유 의존을 대역으로
    바꾸라고 하는데, 공유 의존에는 응용 데이터베이스처럼 **목으로 바꾸면 안 되는 것**이
    섞여 있다. 그래서 이 책의 최종 판정은 두 학파 어느 쪽도 아니라 **관찰 가능성으로
    다시 그은 선**이다.

## 학파 이름의 대응

같은 갈림을 이 KB의 다른 페이지가 다른 이름으로 부른다. **이름이 다른 것은 소스가 다른
이름을 쓰기 때문이지 가리키는 것이 달라서가 아니다.**

| 이 책(khorikov) | [대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md)(fowler) | 같은 자리인 근거 |
|---|---|---|
| 고전 학파(classical school) | 클래시컬(classical) · 사람은 클래시시스트(classicist) | 두 소스 모두 Detroit를 별칭으로 든다 |
| 런던 학파(London school) | 모키스트(mockist) | 이 책이 London을 고르며 mockist를 피한다고 명시한다 |

- **이 책이 `mockist`를 피하는 것이 의도적 선택이다** (2장 곁글 "The classical and London
  schools of unit testing"):[^khorikov2020-unit-testing]

  > The London style is sometimes referred to as mockist. Although the term mockist is
  > widespread, people who adhere to this style of unit testing generally don't like it,
  > so I call it the London style throughout this book.

  - **그 이유가 앞 페이지에 이미 적혀 있다.** 그쪽 소스도 **"many mockist TDDers dislike
    that term"**이라고 적었다. **한쪽이 관찰로 남긴 것을 다른 쪽이 표기 규칙으로 실행한
    것**이 두 페이지의 관계다.
- **이 책이 양쪽 진영의 대표 문헌을 이름으로 지목한다** (같은 곁글) — 고전 학파의 정전으로
  Beck의 *Test-Driven Development: By Example*(2002), 런던 학파의 가장 두드러진 주창자로
  Freeman & Pryce와 그들의 *Growing Object-Oriented Software, Guided by Tests*(2009)다.
  **둘 다 2차 경유다** — 이 KB는 이름과 이 책이 옮긴 문면 밖으로 나가지 않는다.[^khorikov2020-unit-testing]

## 이 판정과 갈리는 자리

**이 페이지는 [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md)와
모순 관계에 있다. 그 모순은 해소하지 않고 남긴다.**

- **먼저 갈리지 않는 것을 적는다.** 위
  [목을 쓸 때의 지침 넷](#목을-쓸-때의-지침-넷)의 넷째("소유한 타입만 목한다")는 **공통
  지반**이다. 그쪽 원문 §4.1의 절 제목이 그대로 `Only Mock Types You Own`이고, 이 책이
  그것을 채택한다. **다만 근거가 다르다** — 그쪽은 **설계를 바꿀 수 있어야 하기 때문**
  이라고 적고, 이 책은 서드파티 동작을 알 수 없다는 것과 어댑터가 부패 방지 계층이 된다는
  것을 든다.
- **실제로 갈리는 축은 시스템 안쪽이다.** 그쪽 원문 §5.2의 제목이
  `Mock Objects should only be used at the boundaries of the system`인데, 그것이 **저자들이
  오해(misconception)라고 이름 붙인 항목**이다. 그 절의 문면이 이렇다 — **"We believe the
  opposite, that Mock Objects are most useful when used to drive the design of the code under
  test. This implies that they are most useful *within* the system where the interfaces can
  be changed."** 경계 밖 통신을 목으로 검사하는 것은 그들에게 **부차적**(secondary)이다.
- **이 책이 그 반대 자리에 선다.** 내부 통신은 구현 세부이고, 목은 시스템의 가장 바깥
  가장자리에서 unmanaged 의존에만 쓰며, 목은 통합 테스트에만 둔다. **곧 그쪽이 부차적이라
  부른 자리가 이 책에서는 목의 유일한 정당한 자리다.**
- **최대 하나만 참인 명제는 취약성에 관한 것이다.** 이 책은 시스템 안 클래스 사이의 통신을
  목으로 검사하면 구현 세부에 결합해 리팩터링 내성을 잃는다고 적고, 그쪽 §5.5는 그
  주장("Mock Objects inhibits refactoring because many tests break together")을 오해로
  분류하며 오히려 **실패가 더 초점 맞고 자명해진다**고 적는다.
- **양쪽 다 실증이 없다.** 이 책에 측정이 없고 그 논문에도 측정이 없다 — 그쪽의 근거는 네
  저자와 지인들의 프로젝트 경험이다. **어느 쪽도 학술 실증으로 인용되지 않는다.**
- **실측은 따로 있고 어느 쪽도 지지하지 않는다.**
  [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md)가
  그 자리이고, **두 처방이 유일하게 합의하는 "소유한 타입만 목하라"마저 관행이 어긴다**는
  값이 거기 있다.
- **해소하려면 무엇이 필요한지도 적어 둔다.** 두 주장은 "시스템 안쪽 협력자(collaborator)를
  목으로 검사한 테스트가 리팩터링에서 얼마나 깨지는가"라는 측정 가능한 물음으로 환원된다.
  **이 KB에 그 값을 잰 소스가 없다.**

## 이 소스의 사각

- **측정이 없다.** "목을 쓴 테스트가 더 잘 깨진다"는 이 페이지의 바닥 논거에 붙은 근거가
  저자의 경험 진술이다. 두 학파의 테스트가 실제로 얼마나 다르게 깨지는지 잰 값이 없다.
- **반대편 실증을 다루지 않는다.** 실제 프로젝트에서 데이터베이스 의존이 어떻게 다뤄지는지에
  대한 실측이 이 책에 없다. **그 실측은 이 책과 반대 방향을 가리킨다** —
  [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md)가
  정본이다.
- **미해결이라는 판정이 이 책 안에 없다.** 같은 물음을 **미해결로 명시한 심사 논문**
  (Xiao et al., EMSE 2024)이 있고 그 문면도 위 페이지에 있다. **이 책은 답을 확정된 것으로
  서술한다.**
- **`managed`/`unmanaged` 판정이 사람의 판단이다.** "외부에서 관찰되는가"를 누가 어떻게
  확정하는지는 다뤄지지 않고, 8장 §8.2.2가 다루는 것은 이미 알려진 공유 데이터베이스의
  경우뿐이다.
- **규모 전제가 적히지 않는다.** 이 지침들이 1인 프로젝트에서 어떻게 달라지는지, 팀 수와
  배포 주기가 후방 호환 요구에 어떻게 작용하는지가 서술되지 않는다.
- **언어 모델 시대의 정량 재검이 미확보다.** 생성된 테스트가 대역을 어떻게 쓰는지, 이
  선 긋기가 생성 도구 아래에서 유지되는지는 이 책의 주제가 아니다. **이 페이지의 판정은
  경험 법칙의 지위로 인용한다.**
- **확보본이 MEAP V03이다.** 최종 인쇄판과 대조하지 않았다.

## 이어지는 페이지

- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) —
  **먼저 읽는다.** 이 페이지의 모든 판정이 거기서 나온 잣대 하나에 기댄다
- [대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md) — 이 페이지가 쓰는
  대역 낱말과 학파 이름의 원전 쪽. 그쪽은 어휘를 소유하고 판정을 유보하며, 이 페이지는
  같은 갈림에 판정을 내리되 그 판정을 두 학파 밖에 세운다
- [가짜와 목](../concepts/fakes-versus-mocks.md) — 같은 고전 측 입장을 파이썬 실무로 적은 다른 소스.
  **그쪽이 "가진 적 없는 것을 목하지 마라"를 곁글 제목으로 쓰고, 이 페이지의 넷째 지침이
  같은 명제를 원전 귀속과 함께 다룬다**
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) — 같은 물음에
  **다른 축으로** 답한 자리. 그쪽은 실물 · 가짜 · 스텁 · 상호작용 검증의 선호 순서를 규모
  조건 위에 세우고, 이 페이지는 순서 대신 **경계 하나**로 답한다. **두 답이 데이터베이스에서
  갈리는지 겹치는지가 이 KB의 미해결 물음이다**
- [의존성 주입과 부트스트랩](dependency-injection-and-bootstrap.md) — 이 페이지의 판정이
  실행되려면 의존을 밖에서 꽂을 수 있어야 한다. 8장 §8.4.2가 "구현 하나짜리 인터페이스는
  목을 위해서만 둔다"고 좁히는 자리와 맞물린다
- [현재 동작을 오라클로 쓴다는 것](current-behaviour-as-oracle.md) — 구현에 결합한 테스트를
  다른 이름으로 부른 자리
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 작은 테스트를
  성립시키는 대역 이야기가 거기 걸려 있다
- [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md) —
  **모순 상대.** 위 [이 판정과 갈리는 자리](#이-판정과-갈리는-자리)가 그 축을 소유한다.
  "소유한 타입만 목하라"의 원전 문면(§4.1)도 거기 있다 — **이 책이 지목하는 2009년 책이
  아니라 2004년 논문이다. 그 책에 대해서는 이 책이 옮긴 문면 밖으로 나가지 않는다**
- [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md) —
  이 페이지의 판정과 실제 관행을 대조한 자리. **데이터베이스를 목으로 바꾸지 말라는 판정과
  가장 크게 어긋나는 값이 거기 있고, 그 논문 가운데 하나가 이 물음을 미해결로 적는다**
- [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md) —
  **이 페이지 처방의 실행 층.** 위 [managed 의존과 unmanaged 의존](#managed-의존과-unmanaged-의존)이
  managed 의존에 실물을 쓰라고 판정하고, 그쪽이 그 "실물"을 같은 엔진으로 좁히며 세우는
  방법(컨테이너)까지 적는다. **다만 근거의 격이 이 페이지와 같다** — 그쪽 세 소스도 전부
  측정 없는 실무 규범이다
- **아직 답이 없는 물음 하나**
  - **이 판정과 그 반대 판정 가운데 어느 쪽이 옳은가.** 두 소스 다 측정이 없고, 실증 둘은
    관행의 분포만 재었지 효과를 재지 않았다. **"시스템 안쪽 협력자를 목으로 검사한 테스트가
    리팩터링에서 얼마나 깨지는가"를 잰 소스가 이 KB에 없다.**

[^khorikov2020-unit-testing]: Khorikov, *Unit Testing: Principles, Practices, and
    Patterns*, Manning, **확보본은 MEAP V03**(2026-08-23 아카이브). **인쇄판 쪽 앵커가
    없어 locator는 장·절 번호와 원문 절 제목이다** — 2장 §2.1~§2.3.4(표 2.1 · 곁글 "The
    classical and London schools of unit testing") · 5장 §5.1 "Differentiating mocks from
    stubs"(각주 [2]) · §5.3 "The relationship between mocks and test fragility" · §5.4
    "The classical vs. London schools of unit testing, revisited"(표 5.2) · 8장 §8.1.3 ·
    §8.2 "Which out-of-process dependencies to test directly" · §8.4 "Using interfaces to
    abstract dependencies" · 9장 도입 · §9.1 "Maximizing mocks' value" · §9.2 "Mocking
    best practices"(각주 [5]·[6]). 직인용은 확보본 문면 그대로이되, MEAP 판 표지 문자열
    `V03`이 문장 앞에 붙은 자리에서는 그 접두를 떼어 냈다(조판 장치). 표 2.1은 원문 표를
    옮긴 것이고 열 이름도 원문 표기다. C# 예제 코드는 개념 설명에 필요한 조각만 인라인
    표기로 옮겼고 펜스로 옮기지 않았다. 그림은 전부 이미지로만 조판돼 있어 그림에서만
    읽히는 것은 옮기지 않았다. 근거 등급·판·참고문헌 상태·인용 규약은
    [소스 메타](../sources/khorikov2020-unit-testing.md)가 정본이고, 읽은 장과 건너뛴
    장은 `it/archive/khorikov2020-unit-testing/_progress.yaml`이 정본이다.
