---
type: concept
title: 계층 아키텍처
status: draft
description: 도메인 층을 격리하기 위해 프로그램을 층으로 가른다는 패턴의 원전 — 도메인 코드가 다른 코드에 퍼졌을 때 무엇이 불가능해지는가, 네 층의 이름과 각 층의 책임 규정, 애플리케이션 층을 얇게 유지하고 업무 규칙을 도메인 층에 두라는 배분, 층 사이 의존 방향의 원칙, 서비스라는 낱말이 세 층에 각각 있다는 구분, 이 분리를 패키징으로 강제하는 것이 유일하게 유용한 기술 구획이라는 판정과 티어 분할이 반대로 모델을 조각내는 대가, 규칙과 생성 책임이 각각 이 경계를 넘어 새는 두 방향, 모델에 대응하지 않는데도 도메인 층에 사는 구성물이 있다는 예외, 이 분리가 노리는 것이 무엇인가, 그리고 16장의 책임 층이 같은 낱말을 쓰되 도메인 층 안쪽을 도메인의 책임으로 다시 가르는 다른 구조라는 구분, 그 위에 2021년 실무가 같은 패턴을 표현·업무 로직·데이터 접근 세 층으로 적고 서비스 층을 변종으로 끼워 넣는 판본과 현대 시스템에서 넓어진 양 끝 층의 범위, 이름의 대응표, 이 패턴이 트랜잭션 스크립트와 액티브 레코드에 맞고 도메인 모델에는 맞지 않는다는 판정, 그리고 층과 티어가 논리 경계와 물리 경계로 갈린다는 구분
generated: { by: "claude-opus-5", at: "2026-09-15T00:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: ford2022-evolutionary, resource: /it/sources/ford2022-evolutionary.md }
---

# 계층 아키텍처

- [도메인 코드가 흩어졌을 때](#도메인-코드가-흩어졌을-때)
- [네 개의 층](#네-개의-층)
- [조항](#조항)
- [애플리케이션 층과 도메인 층의 경계](#애플리케이션-층과-도메인-층의-경계)
- [서비스는 세 층 모두에 있다](#서비스는-세-층-모두에-있다)
- [패키징으로 이 분리를 강제한다](#패키징으로-이-분리를-강제한다)
- [같은 규칙을 실행 가능한 검사로 만드는 소스](#같은-규칙을-실행-가능한-검사로-만드는-소스)
- [규칙이 도메인 층을 떠나면 남는 것](#규칙이-도메인-층을-떠나면-남는-것)
- [모델에 없는데 도메인 층에 사는 것들](#모델에-없는데-도메인-층에-사는-것들)
- [네 층 중 무엇이 이 방법론의 요구인가](#네-층-중-무엇이-이-방법론의-요구인가)
- [모델을 흐리는 다른 힘들](#모델을-흐리는-다른-힘들)
- [16장의 책임 층은 이 층 나누기가 아니다](#16장의-책임-층은-이-층-나누기가-아니다)
- [2021년 판본은 같은 패턴을 세 층으로 적는다](#2021년-판본은-같은-패턴을-세-층으로-적는다)
- [층 사이의 소통과 이름의 대응](#층-사이의-소통과-이름의-대응)
- [이 패턴이 맞는 자리와 맞지 않는 자리](#이-패턴이-맞는-자리와-맞지-않는-자리)
- [층과 티어는 다르다](#층과-티어는-다르다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인 모델이 사는 자리를 어떻게 격리하고, 그 격리는 무엇을 위한 것인가.**

## 도메인 코드가 흩어졌을 때

- 문제 설정 — 객체 지향 프로그램에서 **사용자 인터페이스·데이터베이스·기타 지원 코드가 흔히
  업무 객체에 직접 쓰인다. 추가적인 업무 로직이 사용자 인터페이스 위젯의 행동과 데이터베이스
  스크립트에 박힌다. 이런 일이 일어나는 것은 그것이 단기적으로 일을 되게 만드는 가장 쉬운
  방법이기 때문이다** (4장, p.69).[^evans2003]
- 그 대가가 넷으로 계상된다 (4장, p.69):[^evans2003]
  - **도메인 관련 코드가 그렇게 많은 다른 코드에 퍼지면 그것을 보고 그것에 대해 추론하기가
    극도로 어려워진다.**
  - **사용자 인터페이스의 표면적 변경이 실제로 업무 로직을 바꿀 수 있다.**
  - **업무 규칙 하나를 바꾸려면 사용자 인터페이스 코드·데이터베이스 코드·다른 프로그램
    요소를 꼼꼼히 추적해야 할 수 있다.**
  - **정합적이고 모델 주도적인 객체를 구현하는 것이 비실용적이 되고, 자동화된 테스트가
    어색해진다.**
- 층 나누기의 이름이 이 자리에서 나온다 — **업계는 경험과 관례를 통해 계층 아키텍처
  (LAYERED ARCHITECTURES)로, 그중에서도 몇 개의 꽤 표준적인 층으로 수렴했다** (4장,
  p.69).[^evans2003]
- 그 계층 아키텍처(layered architecture)가 지키는 원칙 한 줄 — **본질적 원리는 한 층의 어떤
  요소도 같은 층의 다른 요소나 그 "아래" 층의 요소에만 의존한다는 것이다. 위로 향하는 소통은 어떤 간접 기제를 거쳐야 한다**
  (4장, p.69).[^evans2003]
- 층 나누기의 값도 규정된다 — **층의 값은 각각이 컴퓨터 프로그램의 특정 측면에 특화된다는
  것이다. 이 특화가 각 측면의 더 응집된 설계를 가능하게 하고, 그 설계를 해석하기 훨씬 쉽게
  만든다** (4장, p.69).[^evans2003]

## 네 개의 층

- 저자가 수렴했다고 보는 네 층이다 (4장, p.70):[^evans2003]

| 층 | 원어 | 책임 |
|---|---|---|
| 사용자 인터페이스 층(표현 층) | User Interface (Presentation Layer) | 사용자에게 정보를 보이고 사용자의 명령을 해석한다. 외부 행위자는 사람이 아니라 다른 컴퓨터 시스템일 수도 있다 |
| 애플리케이션 층 | Application Layer | 소프트웨어가 해야 할 일을 정의하고 표현력 있는 도메인 객체를 지휘해 문제를 풀게 한다. 이 층이 책임지는 작업은 사업에 유의미하거나 다른 시스템의 애플리케이션 층과 상호작용하는 데 필요한 것이다 |
| 도메인 층(모델 층) | Domain Layer (Model Layer) | 사업의 개념, 사업 상황에 대한 정보, 업무 규칙을 표상한다. 사업 상황을 반영하는 상태가 여기서 통제되고 쓰이며, 그것을 저장하는 기술적 세부는 인프라스트럭처에 위임된다 |
| 인프라스트럭처 층 | Infrastructure Layer | 상위 층을 지원하는 범용 기술 능력을 제공한다. 애플리케이션을 위한 메시지 발송, 도메인을 위한 영속성, 사용자 인터페이스를 위한 위젯 그리기 같은 것들이다 |

- 도메인 층에는 한 줄 판정이 따로 붙는다 — **이 층이 업무 소프트웨어의 심장이다** (4장,
  p.70).[^evans2003]
- 그리고 네 층 중 무엇이 필수인지가 명시된다 — **어떤 프로젝트는 사용자 인터페이스 층과
  애플리케이션 층을 날카롭게 구분하지 않는다. 다른 프로젝트는 인프라스트럭처 층이 여럿이다.
  그러나 모델 주도 설계를 가능하게 하는 것은 도메인 층의 결정적인 분리다** (4장,
  p.70).[^evans2003]

## 조항

- 처방 문단 (4장, p.70):[^evans2003]

> Partition a complex program into layers. Develop a design within each layer that is cohesive
> and that depends only on the layers below. Follow standard architectural patterns to provide
> loose coupling to the layers above. Concentrate all the code related to the domain model in
> one layer and isolate it from the user interface, application, and infrastructure code.

- 그 격리가 도메인 객체에게 주는 것 — **자기를 표시하고, 자기를 저장하고, 애플리케이션 작업을
  관리하는 책임에서 자유로워진 도메인 객체는 도메인 모델을 표현하는 데 집중할 수 있다. 이것이
  모델이 본질적인 업무 지식을 담고 그것을 일하게 만들 만큼 풍부하고 명료하게 진화하도록
  허용한다** (4장, pp.70–71).[^evans2003]
- 이득이 셋으로 적힌다 (4장, p.71):[^evans2003]
  - **격리된 층은 유지 비용이 훨씬 덜 드는데, 서로 다른 속도로 진화하고 서로 다른 필요에
    반응하는 경향이 있기 때문이다.**
  - 분산 시스템에서 **층을 서로 다른 서버나 클라이언트에 유연하게 배치할 수 있게 해 소통
    부담을 최소화하고 성능을 개선한다.**
  - 사용자 인터페이스를 다른 것으로 갈아 끼워도 아래 층이 영향을 받지 않는다 — 다만 저자는 그
    이유를 실용성에 두지 않는다. **이 결합 해제가 중요한 것은 프로젝트가 사용자 인터페이스를
    자주 갈아 끼워야 해서가 아니라, 관심사의 깔끔한 분리가 각 층의 설계를 이해하고 유지하기
    쉽게 유지하기 때문이다** (4장, p.71).[^evans2003]

## 애플리케이션 층과 도메인 층의 경계

- 애플리케이션 층에 붙는 제약이 이 패턴에서 가장 자주 어긋나는 자리다 — **이 층은 얇게
  유지된다. 그것은 업무 규칙이나 지식을 담지 않고 작업을 조율하고 다음 층의 도메인 객체
  협업에 일을 위임할 뿐이다. 그것은 사업 상황을 반영하는 상태를 갖지 않지만, 사용자나
  프로그램을 위한 작업의 진행을 반영하는 상태는 가질 수 있다** (4장, p.70).[^evans2003]
- 은행 계좌이체 예제에서 그 경계가 한 문장으로 확인된다 — **애플리케이션 층이 아니라 도메인
  층이 근본적인 업무 규칙을 책임진다는 데 유의하라 — 이 경우 그 규칙은 "모든 대변에는 대응하는
  차변이 있다"이다** (4장, p.71).[^evans2003]
- 이 KB에서 그 경계를 파이썬 실물로 다루는 자리가
  [서비스 레이어](service-layer-pattern.md)이고, 그쪽이 경고하는 빈혈 도메인은 이 조항이
  뒤집힌 상태 — 업무 규칙이 애플리케이션 층으로 올라간 상태 — 다.

## 서비스는 세 층 모두에 있다

- 5장이 이 층 구분을 서비스에 적용한다 — **문헌에서 논의되는 서비스 대부분은 순전히 기술적이며
  기반 층에 속한다** (5장 §"SERVICES and the Isolated Domain Layer", p.106).[^evans2003]
  그러나 도메인 층과 애플리케이션 층에도 서비스가 있고, **그 셋을 구별하고 구별을 날카롭게
  유지하도록 책임을 인수분해하는 데 주의가 든다**고 적는다.
- **판정 기준이 이 페이지의 조항과 같다** — **기술 서비스는 업무적 의미를 전혀 갖지 않아야
  한다** (5장, p.106).[^evans2003] 은행 계좌이체 예제가 여기서도 쓰이는데, 이체 자체는
  **은행 도메인 언어에서 의미를 가지며 근본적인 업무 로직을 담고 있으므로** 도메인 서비스이고,
  거래를 스프레드시트로 내보내는 것은 **도메인에 "파일 형식"의 의미가 없고 업무 규칙도 없으므로**
  애플리케이션 서비스다 (5장, p.107).[^evans2003]
  - 위 [애플리케이션 층과 도메인 층의 경계](#애플리케이션-층과-도메인-층의-경계)가 같은 예제로
    같은 선을 긋는다. **서비스라는 낱말이 층을 말해 주지 않으므로 선은 내용이 긋는다.**
- 그리고 이 층 구조를 지키는 수단으로 도메인 서비스가 쓰인다 — 잘게 쪼개진 도메인 객체는
  **도메인에서 애플리케이션 층으로의 지식 누출에 기여할 수 있고**, 중간 굵기의 도메인 서비스를
  신중하게 들이면 **층 사이의 뚜렷한 선을 유지하는 데 도움이 된다** (5장,
  p.108).[^evans2003] 전문은 [도메인 서비스](../concepts/domain-services.md)에 있다.

## 패키징으로 이 분리를 강제한다

- 5장의 모듈 논의가 이 패턴을 패키징 규약으로 옮긴다 (5장, p.112):[^evans2003]

> An example of a very useful framework standard is the enforcement of LAYERED ARCHITECTURE by
> placing infrastructure and user interface code into separate groups of packages, leaving the
> domain layer physically separated into its own set of packages.

- **그리고 그것이 유일하게 허가되는 기술 구획으로 좁혀진다** (5장, p.115):[^evans2003]

> Use packaging to separate the domain layer from other code. Otherwise, leave as much freedom
> as possible to the domain developers to package the domain objects in ways that support
> their model and design choices.

- 반대 방향의 패키징은 이 패턴을 돕지 않고 모델을 조각낸다 — **티어 아키텍처는 모델 객체의
  구현을 조각낼 수 있다. 어떤 프레임워크는 단일 도메인 객체의 책임을 여러 객체에 흩고 그
  객체들을 별개의 패키지에 놓는 방식으로 티어를 만든다** (5장, p.113).[^evans2003]
  - **층(layer)과 티어(tier)를 가르는 자리다.** 이 페이지의 층은 **관심사**를 가르고, 그쪽
    티어는 **한 개념 객체의 구현**을 가른다. 앞은 모델을 드러내고 뒤는 가린다.
  - 저자가 겪은 프로젝트에서 그 결과가 **빈혈 도메인 모델**이었다 (5장, p.114).[^evans2003]
    위 [애플리케이션 층과 도메인 층의 경계](#애플리케이션-층과-도메인-층의-경계)가 경고하는
    상태에 **패키징만으로도 도달할 수 있다**는 기록이다. 전문은
    [도메인의 모듈](modules-in-the-domain.md)에 있다.

## 같은 규칙을 실행 가능한 검사로 만드는 소스

**에번스(Evans)가 패키징으로 강제하라고 적은 것을 포드 외(Ford et al.)는 빌드에서 도는 검사로
만든다.** 규칙은 같고 집행 수단이 다르다.

- **포드 외가 층 검사를 아키텍처 테스트 도구의 가장 흔한 쓰임으로 든다** — 아키텍트가 층 사이 변경을
  격리하려고 계층 아키텍처를 지었을 때, **의존은 인접한 층 사이에만 있어야 하고 한 층에 결합하는 층이
  많을수록 변경의 파급 부작용이 커진다.** 그들의 예제는 층 이름과 각 층에 접근할 수 있는 층을
  선언하는 규칙이다 (4장, pp.60–61).[^ford2022-evolutionary]
  - 이 KB는 그 예제 코드를 옮기지 않았다. 위 [조항](#조항)이 세운 의존 방향 규칙과 **내용이
    같다** — 다른 것은 그것이 문장인가 검사인가다.
- **그리고 문서와 검사의 차이에 대한 판정이 붙는다** — 많은 아키텍트가 그런 원칙을 위키에 써 두었고
  **아무도 읽지 않았다.** 그들의 조문은 이렇다 (4장, p.61):[^ford2022-evolutionary]

  > It's great for architects for express principles, but principles without enforcement are
  > aspirational rather than governance.

  - 원문 그대로다. **"for architects for express"는 원문의 오식**이고 이 KB는 고치지 않았다.
  - 뒤따르는 판정이 이 페이지에 직접 걸린다 — 아키텍트가 **층과 그 밑의 관심사 분리 원칙을 기술하는
    문서를 쓸 수는 있지만, 검사가 그것을 검증하지 않는 한 개발자가 그 원칙을 따를 것이라고 결코
    확신할 수 없다** (4장, pp.61–62).[^ford2022-evolutionary]
- **두 소스의 수단이 서로를 배제하지 않는다.** 위
  [패키징으로 이 분리를 강제한다](#패키징으로-이-분리를-강제한다)의 패키지 구획은 **구조로** 규칙을
  표현하고, 포드 외의 검사는 **그 구조가 지켜지는지를** 본다. 오히려 그들의 예제가 층을 정의하는
  방식이 **패키지 이름**이라, 에번스의 패키징 규약이 있어야 그 검사가 성립한다. #hypothesis
- **다만 대가에 대한 서술이 포드 외 쪽에만 있다** — 그들은 이런 결정이 **개발자에게 단기적 불편을
  주지만 진화와 격리 측면에서 장기적 이득이 있다**고 적고, 적합도 함수를 **몽둥이가 아니라
  체크리스트**로 놓으라는 자기 제한을 함께 적는다 (4장, pp.60, 78–79).[^ford2022-evolutionary]
  **에번스는 이 규칙의 집행 비용을 논하지 않는다.**
- 그 소스의 전문은 [자동화된 아키텍처 거버넌스](automated-architectural-governance.md)에 있다.

## 규칙이 도메인 층을 떠나면 남는 것

같은 원전이 9장에서 이 경계가 무너지는 두 방향과 각각의 대가를 적는다.

- **위로 새는 쪽.** 규칙 평가 코드가 도메인 객체를 압도할 때 흔한 대응은 그것을 애플리케이션
  층으로 리팩터링하는 것이고, 저자는 그것을 더 나쁜 선택으로 판정한다 — **이제 규칙은 도메인
  층에서 완전히 분리되어, 업무 모델에 내재한 규칙을 표현하지 못하는 죽은 데이터 객체를 뒤에
  남긴다** (9장, p.224).[^evans2003] 문제 설정이 한 문장에 있다 (9장, p.225):[^evans2003]

> But moving the rules out of the domain layer is even worse, since the domain code no longer
> expresses the model.

  - **위 [애플리케이션 층과 도메인 층의 경계](#애플리케이션-층과-도메인-층의-경계)가 금지하는
    상태의 원인 하나가 여기서 지목된다.** 규칙이 올라가는 것은 게으름이 아니라 도메인 객체를
    구하려는 시도의 부작용이며, 그 시도의 올바른 출구는
    [명세 패턴](specification-pattern.md)이 다루는 별도 규칙 객체다.
- **아래로 새는 쪽.** 질의를 명세가 SQL로 직접 내게 하면 반대 방향으로 샌다 — **테이블 구조의
  세부가 도메인 층으로 새어 나왔다; 그것은 도메인 객체를 관계형 테이블에 연결하는 매핑 층에
  격리되어야 한다** (9장, p.231).[^evans2003] 이 층 배분을 실물로 다루는 자리는
  [리포지터리 패턴](repository-pattern.md)이다.
- **제자리로 돌아오는 쪽도 기록돼 있다.** 이자 발생 사례의 리팩터링이 세는 이득 셋째가 그것이다
  — **어느 원장에 기표할지 같은 도메인 지식을 스크립트에서 도메인 층으로 옮긴다** (9장,
  p.215).[^evans2003] 화물 여정 사례에서도 같은 이동이 다섯째 이득으로 계상된다 — **예약
  보고서에서 도메인 로직을 걷어 내 격리된 도메인 층에 놓는다** (9장, p.210).[^evans2003]
  - 두 사례에서 업무 지식이 실제로 살고 있던 자리가 야간 배치 스크립트와 보고서였다는 점이
    위 [도메인 코드가 흩어졌을 때](#도메인-코드가-흩어졌을-때)의 진단을 뒷받침한다.

## 모델에 없는데 도메인 층에 사는 것들

같은 원전이 6장에서 이 층에 **모델의 무엇에도 대응하지 않는 요소**를 들이는 예외를 명시한다.
팩토리(FACTORY)와 리포지터리(REPOSITORY)가 그것이다.

- 배치의 근거가 먼저 나온다 — **복잡한 객체 생성은 도메인 층의 책임이지만, 그 과제는 모델을
  표현하는 객체들의 것이 아니다** (6장, pp.137–138).[^evans2003] 생성과 조립은 은행 계좌
  개설처럼 도메인의 이정표에 대응하는 경우도 있지만 **대개 도메인에서 아무 뜻도 없다. 그것은
  구현의 필요다** (6장, p.138).[^evans2003]
- 그래서 저자가 자기 규약의 예외를 선언한다 — **우리는 모델의 무엇에도 대응하지 않는 요소를
  설계에 더하고 있지만, 그럼에도 그것들은 도메인 층의 책임의 일부다** (6장,
  p.138).[^evans2003] 같은 규정이 장 도입에도 있다 — **리포지터리와 팩토리는 그 자체로는
  도메인에서 오지 않지만, 도메인 설계에서 유의미한 역할을 갖는다** (6장,
  p.124).[^evans2003]
  - **"도메인 층"과 "도메인 모델"이 같은 범위가 아니라는 것이 이 절의 요점이다.** 위
    [네 개의 층](#네-개의-층)이 도메인 층을 "업무 개념과 업무 상황에 대한 정보와 업무 규칙"의
    자리로 규정하는데, 6장은 그 층 안에 **모델을 날카롭게 유지하기 위한 보조 구성물**이 함께
    산다고 말한다.
- **그리고 생성을 클라이언트에 맡기면 경계가 무너진다** — 클라이언트가 도메인 객체를 조립하면
  내부 구조와 규칙을 알아야 하고 구체 클래스에 결합된다. 그 결과가 층으로 번진다 —
  **클라이언트가 애플리케이션 층의 일부라면 책임이 도메인 층 밖으로 완전히 새어 나간 것이다.
  애플리케이션이 구현의 세부에 이렇게 단단히 결합되면 도메인 층에서 얻는 추상의 이득 대부분이
  벗겨지고, 이후의 변경이 갈수록 비싸진다** (6장, p.137).[^evans2003]
  - 위 [규칙이 도메인 층을 떠나면 남는 것](#규칙이-도메인-층을-떠나면-남는-것)이 **규칙**의
    유출을 다뤘다면, 이 자리는 **생성 책임**의 유출이다. 증상이 같다 — 애플리케이션 층이
    두꺼워지고 도메인 객체가 비어 간다. 전문은 [팩토리 패턴](../concepts/factories-pattern.md)에 있다.
- 리포지터리 쪽 유출은 반대 방향이다 — **자유로운 데이터베이스 질의는 실제로 도메인 객체와
  애그리게이트(AGGREGATE)의 캡슐화를 깨뜨릴 수 있다. 기술 기반 구조와 데이터베이스 접근 기제의
  노출은 클라이언트를 복잡하게 만들고 모델 주도 설계를 흐린다** (6장, p.150).[^evans2003]
  전문은 [리포지터리 패턴](repository-pattern.md)에 있다.

## 네 층 중 무엇이 이 방법론의 요구인가

같은 장이 이 패턴을 소개한 뒤 자기 요구를 한 층으로 좁힌다.

- 전제는 넓다 — **계층 아키텍처는 여러 층 구성 방식으로 오늘날 대부분의 시스템에서 쓰이고,
  많은 개발 스타일이 층 나누기에서 이득을 볼 수 있다.** 그러나 **도메인 주도 설계가 존재를
  요구하는 층은 하나뿐이다** (4장, p.75).[^evans2003]
- 그 하나의 정의가 세 문장으로 나뉘어 있다 (4장, p.75):[^evans2003]
  - **도메인 모델은 개념의 집합이다.**
  - **"도메인 층"은 그 모델과 직접 관련된 모든 설계 요소의 발현이다.**
  - **업무 로직의 설계와 구현이 도메인 층을 이룬다.**
  - 그리고 [모델 주도 설계](model-driven-design.md)에서는 **도메인 층의 소프트웨어 구성물이
    모델 개념을 그대로 비춘다.**
- 그래서 격리가 선택이 아니라 선행 조건이 된다 (4장, p.75):[^evans2003]

> It is not practical to achieve that correspondence when the domain logic is mixed with other
> concerns of the program. Isolating the domain implementation is a prerequisite for
> domain-driven design.

  - **위 [네 개의 층](#네-개의-층)의 표는 관례를 기술한 것이고, 이 절이 그중 요구 사항을
    골라낸다.** 나머지 셋은 프로젝트 사정에 따라 합쳐지거나 늘어날 수 있다.
  - 같은 장 끝이 이 요구를 형태와 분리해 다시 적는다 — 아키텍처가 응집된 도메인 설계를 나머지와
    느슨하게 결합된 채로 격리한다면 그것이 네 층 구조인지는 묻지 않는다는 것이다. 전문은
    [스마트 UI 안티패턴 §최소 기준](smart-ui-antipattern.md)에 있다.

## 모델을 흐리는 다른 힘들

- 이 장이 닫히며 **기반 구조와 사용자 인터페이스 말고도 모델을 부패시키는 힘이 있다**고 적고
  둘을 지목한다 (4장, p.79):[^evans2003]
  - **모델에 온전히 통합되지 않은 다른 도메인 구성 요소들**을 다뤄야 한다.
  - **같은 도메인의 다른 모델을 쓰는 다른 개발 팀들**과 지내야 한다.
  - 그 대가가 같다 — **이런 요인들이 모델을 흐리고 쓸모를 앗아 갈 수 있다.** 그 자리를 다루는
    장이 14장이고 [경계 컨텍스트](../concepts/bounded-context.md)와 부패 방지 층이 그
    패턴들이다.
- 그리고 격리 자체로 풀리지 않는 문제가 하나 더 남는다 — **정말 복잡한 도메인 모델은 그것만으로도
  다루기 힘들어질 수 있다.** 그래서 도메인 층 **안에서** 다시 구분을 두어 본질적 개념을 주변
  세부에서 풀어 주는 일이 필요하고, 그것이 15장의 증류다 (4장, p.79).[^evans2003] 이 KB에서는
  [핵심 도메인](../concepts/core-domain.md)이 그 자리다.
  - **이 절이 이 페이지의 한계를 표시한다.** 층을 가르는 것은 도메인 코드를 **한자리에** 모으는
    일이고, 그 자리가 커진 다음의 물음은 이 패턴이 답하지 않는다.

## 16장의 책임 층은 이 층 나누기가 아니다

같은 책 16장에 [책임 층](responsibility-layers.md)이라는 대규모 구조가 나온다. **같은 낱말을
쓰지만 무엇을 가르는지가 다르므로 두 조항을 섞지 않는다.**

| | 이 페이지의 계층 아키텍처(4장) | 책임 층(16장) |
|---|---|---|
| 무엇으로 가르는가 | 기술적 관심사 — 사용자 인터페이스·애플리케이션·도메인·기반 구조 | 도메인의 책임 — 잠재력·운영·의사 결정 지원·정책·확약 |
| 어디를 가르는가 | 시스템 전체를 네 덩어리로 | **도메인 층 안쪽**을 다시 |
| 산물인가 | 패키지로 구현된다 | **코드 안의 산물이 아니다.** 모듈과 객체의 경계와 관계를 제약하는 규칙의 집합이다 |
| 필수인가 | 이 방법론의 전제 조건이다 | 선택 사항이다 |

- 16장은 이 구분을 배경으로 깔고 출발한다 — **J2EE 같은 기술 아키텍처가 여러 해에 걸쳐
  두드러진 반면 도메인 층의 대규모 구조는 많이 탐구되지 않았다** (16장,
  p.444).[^evans2003]
- 16장의 층 정의 자체는 이 페이지의 층과 같은 성질을 쓴다 — **각 구획의 구성원이 "아래" 층의
  서비스를 알고 쓸 수 있으나 "위" 층은 모르고 그것에 독립적인, 시스템의 구획들** (16장,
  p.450).[^evans2003] 다른 것은 **무엇을 구획의 기준으로 삼는가**다.
- 16장이 쓰는 판본이 명시된다 — **책임 층에 가장 잘 맞는 층 나누기 패턴은 완화된 층 시스템
  (RELAXED LAYERED SYSTEM, Buschmann et al. 1996, p.45)이라 불리는 변종이고, 그것은 한 층의
  컴포넌트가 바로 아래 층뿐 아니라 어느 아래 층에든 접근하도록 허용한다** (16장,
  p.451).[^evans2003]
- **둘은 포개진다.** #hypothesis 저자가 두 층 나누기가 어떻게 겹치는지를 한 문장으로 명시한
  대목은 없다. 근거는 16장이 시종 도메인 모델의 객체·애그리게이트·모듈을 대상으로 삼고 이
  페이지의 네 층 중 어느 것도 16장에서 층으로 다뤄지지 않는다는 것이다.
  - 다만 한 자리에서 두 구조가 만난다 — 16장은 의사 결정 지원 층이 **데이터 웨어하우스 기술로
    구현되어 별개의 경계 컨텍스트가 되는** 경우를 든다 (16장, p.462).[^evans2003] 그때는
    책임 층의 한 층이 통째로 다른 배치 단위가 된다.

## 2021년 판본은 같은 패턴을 세 층으로 적는다

[khononov2021](../sources/khononov2021.md)이 이 패턴을 **세 아키텍처 패턴 중 첫째**로 다시
세운다. 원전의 네 층과 이름도 개수도 다르되 같은 패턴이고, 이 판본이 더하는 것은 **왜 아키텍처
패턴이 필요한가**라는 문제 설정과 **어느 업무 로직 패턴에 맞는가**라는 판정이다.

- 문제 설정이 위 [도메인 코드가 흩어졌을 때](#도메인-코드가-흩어졌을-때)와 같은 진단이다
  (8장 §"Business Logic Versus Architectural Patterns", p.117):[^khononov2021]

> The variety of concerns that a codebase has to take care of makes it easy for its business logic to
> become diffused among the different components: that is, for some of the logic to be implemented in
> the user interface or database, or be duplicated in different components. Lacking strict
> organization in implementation concerns makes the codebase hard to change.

  - 대가의 계상도 같은 모양이다 — 업무 로직을 바꿔야 할 때 **코드베이스의 어느 부분이 영향을
    받아야 하는지 분명하지 않고**, 변경이 **무관해 보이는 부분에 예기치 않은 영향을** 주며,
    반대로 **고쳐야 할 코드를 놓치기 쉽다** (8장, p.117).[^khononov2021]
- 그래서 아키텍처 패턴의 정의가 이렇게 온다 (8장, p.117):[^khononov2021]

> Architectural patterns introduce organizational principles for the different aspects of a codebase
> and present clear boundaries between them: how the business logic is wired to the system's input,
> output, and other infrastructural components.

- 계층 아키텍처의 규정 (8장 §"Layered Architecture", p.118):[^khononov2021]

> Layered architecture is one of the most common architectural patterns. It organizes the codebase
> into horizontal layers, with each layer addressing one of the following technical concerns:
> interaction with the consumers, implementing business logic, and persisting the data.

  그리고 고전적 형태의 층이 셋으로 적힌다 (8장, p.118):[^khononov2021]

> In its classic form, the layered architecture consists of three layers: the presentation layer
> (PL), the business logic layer (BLL), and the data access layer (DAL).

  - **위 [네 개의 층](#네-개의-층)의 표와 견주면 애플리케이션 층 하나가 빠져 있다.** 이
    판본은 그 층을 필수가 아니라 **변종**으로 다룬다 — 아래 서비스 층 항목을 보라. 원전은
    반대로 네 층을 관례로 기술하고 그중 도메인 층 하나만 요구로 좁힌다(위
    [네 층 중 무엇이 이 방법론의 요구인가](#네-층-중-무엇이-이-방법론의-요구인가)).
    **대상이 같고 무엇을 기본으로 세울지가 다르다.**
- **양 끝 두 층의 범위가 현대 시스템에서 넓어졌다는 것이 이 판본의 갱신이다.**
  - 표현 층 — 원 형태에서는 웹 인터페이스나 데스크톱 애플리케이션 같은 그래픽 인터페이스를
    가리켰다. 그러나 (8장, p.118):[^khononov2021]

    > In modern systems, however, the presentation layer has a broader scope: that is, all means for
    > triggering the program's behavior, both synchronous and asynchronous.

    저자가 드는 것이 다섯이다 — GUI, 명령줄 인터페이스(CLI), 다른 시스템과의 프로그램적
    통합을 위한 API, 메시지 브로커의 이벤트 구독, 나가는 이벤트를 발행하는 메시지 토픽
    (8장, pp.118–119).[^khononov2021] 그래서 결론이 이렇다 (8장, p.119):[^khononov2021]

    > All of these are the means for the system to receive requests from the external environment and
    > communicate the output. Strictly speaking, the presentation layer is the program's public
    > interface.

  - 업무 로직 층 — **저자가 이 층의 규정을 원전에서 빌린다**. 업무 결정이 구현되는 자리이고,
    **에릭 에반스의 말대로 이 층이 소프트웨어의 심장이다** (8장, p.119).[^khononov2021]
    원문 판정은 위 [네 개의 층](#네-개의-층)에 있다. 그리고 이 층이 5장에서 7장의 업무 로직
    패턴들이 구현되는 자리로 지정된다 — 액티브 레코드나 도메인 모델이 여기 산다. 그 선택은
    [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md)에 있다.
  - 데이터 접근 층 — 원 형태에서는 시스템의 데이터베이스를 가리켰다. 넓어진 범위가 셋으로
    적힌다 (8장, pp.119–120):[^khononov2021] NoSQL 이후 한 시스템이 **여러 데이터베이스**를
    쓰는 것이 흔해졌고(문서 저장소를 운영 데이터베이스로, 검색 색인을 동적 질의에, 인메모리
    데이터베이스를 성능 최적화 연산에), 클라우드 객체 저장소나 메시지 버스처럼 **전통적
    데이터베이스가 아닌 저장 매체**가 들어오며, **외부 정보 제공자와의 통합**(외부 시스템의
    API, 클라우드 벤더의 관리형 서비스)도 이 층이 맡는다.
    - 저자가 각주로 경계를 하나 긋는다 — 여기서 메시지 버스는 **시스템 내부의 필요**에
      쓰이는 것이고, 공개적으로 노출된다면 표현 층에 속한다 (8장, p.120, 각주 3).[^khononov2021]
      **같은 기술이 어느 층에 속하는지를 용도가 정한다는 것**이고, 위
      [서비스는 세 층 모두에 있다](#서비스는-세-층-모두에-있다)가 서비스라는 낱말에 대해
      내리는 판정과 같은 모양이다.
- **서비스 층은 변종으로 들어온다** (8장 §Variation, p.121):[^khononov2021]

> It's common to see the layered architecture pattern extended with an additional layer: the service
> layer.

  - 그 층의 정의와 처방, 그리고 **언제 그것이 필요하고 언제 불필요한가**는
    [서비스 레이어](../concepts/service-layer-pattern.md)에 있다. 이 페이지는 그것이 계층
    아키텍처의 확장으로 온다는 사실만 갖는다.

## 층 사이의 소통과 이름의 대응

- 의존 방향의 조항이 위 [조항](#조항)과 같다 (8장 §"Communication Between Layers",
  p.120):[^khononov2021]

> The layers are integrated in a top-down communication model: each layer can hold a dependency only
> on the layer directly beneath it

  - 얻는 것도 같게 적힌다 — **이것이 구현 관심사의 결합 해제를 강제하고 층 사이에 공유되는
    지식을 줄인다** (8장, p.120).[^khononov2021]
  - **한 가지가 원전과 다르다.** 원전의 조항은 **"같은 층의 다른 요소나 그 아래 층의 요소에만"**
    의존한다고 적어 아래로 여러 칸 건너뛰는 것을 막지 않는다. 이 판본은 **바로 아래 층**으로
    좁힌다. 좁히는 쪽이라 모순 쌍으로 세우지 않았다. 원전 16장이 쓰는 완화된 층 시스템
    (아래 어느 층에든 접근 허용)까지 세면 같은 소스 안에도 세기 차이가 있다 — 위
    [16장의 책임 층은 이 층 나누기가 아니다](#16장의-책임-층은-이-층-나누기가-아니다)를 보라.
- **이름의 대응표를 저자가 직접 적는다** (8장 §Terminology, p.124):[^khononov2021]

| 이 판본의 이름 | 다른 데서 쓰는 이름 |
|---|---|
| Presentation layer | user interface layer |
| Service layer | application layer |
| Business logic layer | domain layer = model layer |
| Data access layer | infrastructure layer |

  - 저자 자신의 선택도 밝혀져 있다 (8장, p.124):[^khononov2021]

  > To eliminate confusion, I present the pattern using the original terminology. That said, I prefer
  > "user interface layer" and "infrastructure layer" as these terms better reflect the
  > responsibilities of modern systems and an application layer to avoid confusion with the physical
  > boundaries of services.

  - **이 표가 이 페이지와 그 판본을 잇는 사전이다.** 오른쪽 열이 위
    [네 개의 층](#네-개의-층)이 쓰는 이름이고, 저자가 선호한다고 적은 것도 그쪽이다.
    **두 소스가 서로 다른 개념을 말하는 것이 아니라 같은 층에 다른 이름을 쓴다.**

## 이 패턴이 맞는 자리와 맞지 않는 자리

이 판본이 더하는 판정이 이것이다 — **아키텍처 패턴의 선택이 업무 로직 패턴의 선택에 걸린다.**

- 맞는 자리 (8장 §"When to Use Layered Architecture", p.124):[^khononov2021]

> The dependency between the business logic and the data access layers makes this architectural
> pattern a good fit for a system with its business logic implemented using the transaction script or
> active record pattern.

- 맞지 않는 자리 (8장, p.125):[^khononov2021]

> However, the pattern makes it challenging to implement a domain model. In a domain model, the
> business entities (aggregates and value objects) should have no dependency and no knowledge of the
> underlying infrastructure. The layered architecture's top-down dependency requires jumping through
> some hoops to fulfill this requirement. It is still possible to implement a domain model in a
> layered architecture, but the pattern we will discuss next fits much better.

  - 장 맺음이 같은 판정을 한 문장으로 다시 적는다 — **이 패턴이 업무 로직을 데이터 접근
    구현과 결합시키므로 액티브 레코드 기반 시스템에 잘 맞는다** (8장,
    p.135).[^khononov2021]
  - **여기가 이 KB 안에서 판정이 갈리는 자리다.** 이 페이지의 원전은 층 나누기를 **도메인
    주도 설계의 전제 조건**으로 세우고(위
    [네 층 중 무엇이 이 방법론의 요구인가](#네-층-중-무엇이-이-방법론의-요구인가)), 이 판본은
    같은 패턴을 도메인 모델에 **맞지 않는** 것으로 판정한다.
    - **모순 쌍으로 세우지 않았다.** 대상이 다르기 때문이다. 원전이 요구하는 것은
      **도메인 층의 격리** 하나이고, 같은 장이 그 요구를 형태에서 떼어 낸다 — 응집된 도메인
      설계가 나머지와 느슨하게 결합된 채 격리되면 그것이 네 층 구조인지는 묻지 않는다(위
      [네 층 중 무엇이 이 방법론의 요구인가](#네-층-중-무엇이-이-방법론의-요구인가)의 마지막
      항목). 이 판본이 맞지 않는다고 판정하는 것은 **위에서 아래로만 의존한다는 형태**이고,
      그 형태를 뒤집어 격리 요구를 만족시키는 것이 다음 패턴이다.
    - 그 뒤집기는 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의 포트와
      어댑터 절에 있다. **이 KB에서 두 소스가 같은 결론에 이른다** — 파이썬 쪽 소스도 3층
      구조를 안팎으로 뒤집는 데서 출발한다.

## 층과 티어는 다르다

- 저자가 곁글 하나를 이 혼동에 쓴다 (8장 §"Optional: Layers Versus Tiers",
  p.125):[^khononov2021]

> The layers architecture is often confused with the N-Tier architecture, and vice versa. Despite the
> similarities between the two patterns, layers and tiers are conceptually different: a layer is a
> logical boundary, whereas a tier is a physical boundary.

- 가르는 기준이 배치 단위다 (8장, p.125):[^khononov2021]

> All layers in the layered architecture are bound by the same lifecycle: they are implemented,
> evolved, and deployed as one single unit. On the other hand, a tier is an independently deployable
> service, server, or system.

  - 저자의 예가 웹 시스템이다 — 브라우저, 요청을 넘기는 역방향 프록시, 웹 서버 위의 웹
    애플리케이션, 데이터베이스 서버. **전부 같은 물리 서버에서 컨테이너로 돌 수도 있고 여러
    서버에 흩어질 수도 있지만, 각 구성 요소가 나머지와 독립적으로 배치·관리될 수 있으므로
    그것들은 층이 아니라 티어다** (8장, p.125).[^khononov2021] 그리고 **층은 그 웹
    애플리케이션 안쪽의 논리 경계다.**
- **원전도 같은 구분을 하되 반대 방향에서 경고한다.** 위 [조항](#조항)의 이득 목록이 층을
  서로 다른 서버에 배치할 수 있다는 것을 이점으로 들고, 위
  [패키징으로 이 분리를 강제한다](#패키징으로-이-분리를-강제한다)가 티어 분할이 모델을
  조각내는 대가를 적는다. **두 소스가 같은 선을 긋고 서로 다른 쪽의 위험을 짚는다** — 이
  판본은 두 낱말을 섞어 쓰는 것을, 원전은 논리 경계를 물리 경계로 성급히 바꾸는 것을 경고한다.

## 이어지는 페이지

- [모델 주도 설계](model-driven-design.md) — 이 분리가 가능하게 하려는 것
- [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md) — 가른 층을 다시
  잇는 기제와 프레임워크를 얼마나 쓸 것인가
- [스마트 UI 안티패턴](smart-ui-antipattern.md) — 이 패턴을 쓰지 않는 것이 옳은 조건
- [화물 운송 예제](../concepts/cargo-shipping-example.md) — 이 조항이 한 도메인에서 애플리케이션 클래스
  셋으로 구체화되는 자리
- [명세 패턴](specification-pattern.md) — 규칙이 도메인 층에 남게 하는 형태
- [핵심 도메인](../concepts/core-domain.md) — 격리된 도메인 층조차 클 때 그 안에서 다시 무엇을 고르는가
- [서비스 레이어](service-layer-pattern.md) — 애플리케이션 층을 파이썬 실물로 다루는 자리
- [도메인 서비스](../concepts/domain-services.md) — 도메인 층에 서는 서비스의 원 규정
- [도메인의 모듈](modules-in-the-domain.md) — 이 분리를 패키징으로 옮기는 조항과 그 함정
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 도메인 층에 무엇을 두는가
- [리포지터리 패턴](repository-pattern.md) — 영속성이 인프라스트럭처로 위임되는 실물
- [팩토리 패턴](../concepts/factories-pattern.md) — 생성 책임이 도메인 층 안에 머무르게 하는 구성물
- [책임 층](responsibility-layers.md) — 같은 낱말을 도메인 책임으로 쓰는 16장의 층 나누기
- [대규모 구조](../concepts/large-scale-structure.md) — 그 층 나누기가 속한 구조의 층위
- [층이 다르면 추상도 달라야 한다](../concepts/different-layer-different-abstraction.md) — 층 나누기를
  다른 축에서 판정하는 자리
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴의 의존 방향을
  뒤집은 포트와 어댑터
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — 세 아키텍처 패턴 중 셋째
- [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md) — 어느 아키텍처 패턴을
  고를지가 걸리는 입력
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 층 구조를 파이썬으로 구체화한 축의 허브
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 4장 "Isolating the Domain"(§LAYERED ARCHITECTURE pp.68–71 ·
    §THE DOMAIN LAYER IS WHERE THE MODEL LIVES p.75 · §Other Kinds of Isolation p.79 ·
    §Example: Partitioning Online Banking Functionality into Layers pp.71–72) ·
    5장 "A Model Expressed in Software"(§SERVICES 중 §"SERVICES and the Isolated Domain
    Layer" pp.106–107·§Granularity p.108 · §MODULES 중 §"The Pitfalls of
    Infrastructure-Driven Packaging" pp.112–115) ·
    9장 "Making Implicit Concepts Explicit"(예제 "Hearing a Missing Concept in the Shipping
    Model" p.210 · 예제 "Earning Interest the Hard Way" p.215 · §SPECIFICATION pp.224–225 ·
    §"Applying and Implementing SPECIFICATION" p.231) ·
    6장 "The Life Cycle of a Domain Object"(도입 p.124 · §FACTORIES pp.137–138 ·
    §REPOSITORIES p.150) ·
    16장 "Large-Scale Structure"(§EVOLVING ORDER p.444 · §RESPONSIBILITY LAYERS의 층 정의와
    완화된 층 시스템 곁글 pp.450–451 · §"Choosing Appropriate Layers"의 데이터 웨어하우스
    관찰 p.462). 쪽은 인쇄판
    쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 계좌이체 시퀀스 다이어그램(Figure 4.1, p.72)은 도판이라 그 안의 판정 한 줄만
    옮겼다. 같은 장의 §Relating the Layers(pp.72–74)와 §Architectural Frameworks(pp.74–75)는
    물음이 달라 [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md)가,
    §THE SMART UI "ANTI-PATTERN"(pp.76–79)은 [스마트 UI 안티패턴](smart-ui-antipattern.md)이
    담는다.

[^khononov2021]: Khononov 2021, 8장 "Architectural Patterns"(도입과 §"Business Logic Versus
    Architectural Patterns" pp.117–118 · §"Layered Architecture" 도입 p.118 ·
    §"Presentation Layer" pp.118–119 · §"Business Logic Layer" p.119 ·
    §"Data Access Layer" pp.119–120 · §"Communication Between Layers" p.120 ·
    §Variation p.121 · §Terminology p.124 · §"When to Use Layered Architecture" pp.124–125 ·
    곁글 §"Optional: Layers Versus Tiers" p.125 · §Conclusion p.135). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 업무 로직 층 인용에서 본문 각주 번호 표지 하나("As Eric Evans
    says, 1")를 뺐다 — 그 각주가 가리키는 것이 이 페이지의 원전이다. 이름 대응표는 원문이
    불릿 목록이고 이 KB가 표로 옮겼으며 **값은 번역하지 않았다**(층 이름이 검색 키다).
    도판 일곱(Figure 8-1~8-7)은 도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다.
    §Variation의 C# 목록 셋(MVC 컨트롤러와 `CampaignManagementService` 인터페이스와 추출된
    `UserService`)은 [서비스 레이어](../concepts/service-layer-pattern.md)가 대표 하나를
    갖는다 — 이 페이지에는 펜스를 두지 않았다. 장 끝 연습문제 다섯(pp.135–136)은 claim이
    아니라 옮기지 않았다.

[^ford2022-evolutionary]: Ford·Parsons·Kua·Sadalage 2022(2판), 4장 "Automating Architectural
    Governance" §"ArchUnit"(pp.56–62, 하위 "Layer checks" 부분)과 §"Fitness Functions as a
    Checklist, Not a Stick"(pp.78–79). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 22, 실측). 직인용은
    `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 아포스트로피는 곧은 것으로 옮겼다.
    **인용문의 "for architects for express"는 원문의 오식이고 고치지 않았다.** 그 절의 도판(그림
    4-14 컴포넌트로 정의한 계층 아키텍처)은 이미지로 조판돼 있고 코드 목록(예제 4-8)은 옮기지
    않았다. 본문은 [자동화된 아키텍처 거버넌스](automated-architectural-governance.md)에 있고,
    이 페이지는 같은 규칙의 두 집행 수단을 대질하는 데에만 인용한다.
