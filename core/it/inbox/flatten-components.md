---
type: concept
title: 컴포넌트 평탄화
status: draft
description: 네임스페이스가 서로 얹혀 컴포넌트의 경계가 흐려졌을 때 무엇을 옮기는가를 정하는 셋째 분해 패턴 — 컴포넌트 위에 컴포넌트가 얹히면 서비스를 만들 때 무엇을 한 서비스로 볼지 답이 갈린다는 문제 제기, 그 딜레마를 컴포넌트를 네임스페이스의 리프 노드로 규정해 푸는 해법과 거기서 파생되는 루트 네임스페이스와 고아 클래스라는 두 이름, 도판을 아래에서 위로 그려 언덕을 보이는 조판 의도, 내려서 합치거나 올려서 가르는 두 방향과 소스 코드는 리프 노드에만 두라는 조문, 공유 코드도 고아 클래스라는 판정과 그것을 옮길 컴포넌트의 이름을 도메인에 없는 낱말로 고르라는 조언과 거기서 나오는 지표 둘, 루트 네임스페이스의 코드를 잡는 적합도 함수 하나, 책의 사례가 티켓은 올려서 가르고 설문은 내려서 합치는 두 방향을 한 번에 보이는 자리, 그리고 패턴 셋을 다 적용한 뒤의 컴포넌트 스무 개 목록
generated: { by: "claude-opus-5", at: "2026-09-17T23:45:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 컴포넌트 평탄화

- [문제 — 컴포넌트 위에 컴포넌트가 얹힌다](#문제--컴포넌트-위에-컴포넌트가-얹힌다)
- [규정 셋](#규정-셋)
- [도판을 아래에서 위로 그리는 이유](#도판을-아래에서-위로-그리는-이유)
- [평탄화의 두 방향](#평탄화의-두-방향)
- [공유 코드도 고아 클래스다](#공유-코드도-고아-클래스다)
- [공유 네임스페이스의 이름과 거기서 나오는 지표 둘](#공유-네임스페이스의-이름과-거기서-나오는-지표-둘)
- [거버넌스 — 적합도 함수 하나](#거버넌스--적합도-함수-하나)
- [책의 사례 — 평탄화](#책의-사례--평탄화)
- [평탄화 뒤의 컴포넌트 목록](#평탄화-뒤의-컴포넌트-목록)
- [같은 대상을 개념의 응집으로 가르는 소스와 나란히](#같은-대상을-개념의-응집으로-가르는-소스와-나란히)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **네임스페이스가 서로 얹혀 컴포넌트의 경계가 흐려졌을 때 무엇을 어디로 옮겨야
하는가.**

이 패턴은 [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)의 셋째다.

## 문제 — 컴포넌트 위에 컴포넌트가 얹힌다

- **문제의 규정이 정체성의 상실이다** — 컴포넌트가 **다른 컴포넌트 위에 지어지고 그것이 또 다른
  컴포넌트 위에 지어지면**, 컴포넌트들이 **정체성을 잃기 시작하고 저자들의 정의대로의 컴포넌트가
  되기를 멈춘다.** 이 패턴은 컴포넌트가 서로 얹히지 않고 **디렉터리 구조나 네임스페이스의 리프
  노드(leaf node)로 평탄하게 나타나도록** 하는 데 쓴다 (5장, p.101).[^ford2021-hard-parts]
- **네임스페이스가 늘어나면 그 앞 노드의 지위가 바뀐다** — 어떤 컴포넌트를 나타내는
  네임스페이스가 **확장되면**(네임스페이스나 디렉터리 구조에 노드가 하나 더 붙으면), 앞의
  네임스페이스나 디렉터리는 **더 이상 컴포넌트가 아니라 서브도메인(subdomain)이 된다** (5장,
  p.102).[^ford2021-hard-parts]
- **저자들의 실물이 설문 기능이다** (5장, p.102):[^ford2021-hard-parts]

| Component name | Component namespace | Files |
|---|---|---|
| → Survey | `ss.survey` | 5 |
| Survey Templates | `ss.survey.templates` | 7 |

- **개발자 눈에는 말이 되는 구조인데 문제를 만든다** — 템플릿 코드를 설문 처리와 떼어 두는 것이
  개발자 관점에서는 말이 되지만, **컴포넌트로서의 Survey Templates가 Survey 컴포넌트의 일부로
  간주된다**는 문제가 생긴다 (5장, p.102).[^ford2021-hard-parts]
- **하위 컴포넌트라고 부르면 문제가 서비스 만들기에서 터진다** — Survey Templates를 Survey의
  **하위 컴포넌트(subcomponent)**로 보고 싶어질 수 있지만, 이 컴포넌트들로 **서비스를 만들려 할 때
  문제가 생긴다. 둘 다 Survey라는 한 서비스에 들어가야 하는가, 아니면 Survey Templates가 Survey
  서비스와 별개의 서비스여야 하는가** (5장, p.102).[^ford2021-hard-parts]
  - **이 물음이 이 패턴의 존재 이유다.** 네임스페이스 계층이 서비스 경계를 결정하지 못하는 한,
    컴포넌트 목록은 서비스 후보 목록이 되지 못한다.

## 규정 셋

- **딜레마를 푸는 방식이 정의를 좁히는 것이다** — 저자들은 **컴포넌트를 네임스페이스나 디렉터리
  구조의 마지막 노드(리프 노드)로 정의해** 이 딜레마를 해결했다. 그 정의에 따르면
  `ss.survey.templates`는 컴포넌트이고 `ss.survey`는 컴포넌트가 아니라 **서브도메인**이다 (5장,
  p.102).[^ford2021-hard-parts]
- **세 낱말의 규정을 원문 그대로 옮긴다** (5장, p.103):[^ford2021-hard-parts]

  > *Component*
  >
  > A collection of classes grouped within a *leaf node namespace* that performs some sort of
  > specific functionality in the application (such as payment processing or customer survey
  > functionality).
  >
  > *Root namespace*
  >
  > A namespace node that has been extended by another namespace node. For example, given the
  > namespaces ss.survey and ss.survey.templates, ss.survey would be considered a root
  > namespace because it is extended by .templates. Root namespaces are also sometimes
  > referred to as *subdomains*.
  >
  > *Orphaned classes*
  >
  > Classes contained within a root namespace, and hence have no definable component
  > associated with them.

- **그래서 위 표의 다섯 클래스가 고아 클래스다** — `ss.survey`가 `.templates`로 확장되었으므로
  `ss.survey`는 더 이상 컴포넌트가 아니고 **따라서 어떤 클래스 파일도 담고 있어서는 안 된다**
  (5장, p.102).[^ford2021-hard-parts]
- **그림 5-6이 셋을 한 그림에 놓는다** (5장, p.103).[^ford2021-hard-parts] 도판이 이미지 조판이라
  재현하지 않고 배치만 옮긴다 — `ss` 위에 `.survey` · `.login` · `.ticket`이 놓이고, `.survey`
  위에 `.templates`가, `.ticket` 위에 `.assign`과 `.route`가 얹힌다. **코드를 담은 네임스페이스에
  C 상자가 붙고**, `ss.survey`와 `ss.ticket`의 C 상자가 고아 클래스로 지목된다.
  - **그 그림에서 컴포넌트인 것은 넷뿐이다** — `ss.survey.templates` · `ss.login` ·
    `ss.ticket.assign` · `ss.ticket.route` (5장, pp.103–104).[^ford2021-hard-parts]

## 도판을 아래에서 위로 그리는 이유

- **조판 의도가 명시된다** — 이 그림과 이런 종류의 모든 그림은 **의도적으로 아래에서 위로**
  그려진다. 애플리케이션 안의 **언덕(hills)**이라는 관념과 **네임스페이스가 서로 위에 쌓인다**는
  관념을 강조하기 위해서다 (5장, p.103).[^ford2021-hard-parts]
  - **"언덕"이 이 패턴의 진단 낱말이 된다.** 아래 [책의 사례 — 평탄화](#책의-사례--평탄화)에서
    적용 결과를 "언덕이 없다"로 확인한다.

## 평탄화의 두 방향

- **평탄화의 규정** — 이 패턴은 **고아 클래스를 옮겨서 디렉터리나 네임스페이스의 리프 노드로만
  존재하는 잘 정의된 컴포넌트를 만들고**, 그 과정에서 **잘 정의된 서브도메인(루트 네임스페이스)을
  만드는** 데 쓴다. 저자들은 평탄화를 **고아 클래스를 없애기 위해 애플리케이션 안의 네임스페이스를
  내리거나 올리는 것**이라고 적는다 (5장, p.104).[^ford2021-hard-parts]
- **방향 하나 — 내려서 합치기.** `ss.survey.templates`에 든 소스 코드를 `ss.survey`로 **내리면**
  `ss.survey`가 단일 컴포넌트가 된다. `.survey`가 그 네임스페이스의 리프 노드가 되기 때문이다
  (5장, p.104).[^ford2021-hard-parts]
- **방향 둘 — 올려서 가르기.** `ss.survey`에 든 소스 코드에 **기능 분해나 도메인 주도 설계**를
  적용해 루트 네임스페이스 안의 별개 기능 영역을 식별하고 그 영역들로 컴포넌트를 만든다. 저자들의
  예가 `ss.survey.create`(설문을 만들어 보낸다)와 `ss.survey.process`(돌아온 설문을 처리한다)다
  (5장, p.104).[^ford2021-hard-parts]
- **어느 방향이든 지켜야 할 것은 하나다** (5장, p.105, 조언 상자):[^ford2021-hard-parts]

  > Regardless of the direction of flattening, make sure source code files reside only in leaf
  > node namespaces or directories so that source code can always be identified within a
  > specific component.

  - **조문이 방향을 정해 주지 않는다는 것이 이 패턴의 성격이다.** 무엇을 내리고 무엇을 올릴지는
    도메인을 보고 정하고, 규칙은 결과 상태(리프 노드에만 코드가 있다)에만 걸린다.

## 공유 코드도 고아 클래스다

- **루트 네임스페이스에 코드가 남는 다른 흔한 경우가 공유 코드다** — 설문 기능이 세 컴포넌트
  (`ss.survey.templates` · `ss.survey.create` · `ss.survey.process`)에 있고, **인터페이스·추상
  클래스·공통 유틸리티 같은 공통 코드가 루트 네임스페이스 `ss.survey`에 있는** 경우다 (5장,
  p.105).[^ford2021-hard-parts]
- **판정은 같다** — `ss.survey`의 공유 클래스들은 **공유 코드라 해도 여전히 고아 클래스로
  간주된다.** 이 패턴을 적용하면 그 공유 고아 클래스들을 **`ss.survey.shared`라는 새 컴포넌트로
  옮겨** `ss.survey` 서브도메인에서 고아 클래스를 전부 없앤다 (5장,
  p.106).[^ford2021-hard-parts]
  - **공유라는 성질이 예외를 만들지 않는다는 것이 이 절의 요점이다.** 공유 코드에도 컴포넌트
    이름이 있어야 하고, 그래야 그 코드가 무엇인지 셀 수 있다 — 아래 절의 지표 둘이 그 귀결이다.

## 공유 네임스페이스의 이름과 거기서 나오는 지표 둘

- **이름을 고르는 조언** — 공유 코드를 별개 컴포넌트(리프 노드 네임스페이스)로 옮길 때는
  **그 도메인의 어느 기존 코드베이스에서도 쓰이지 않는 낱말**을 고르라는 것이다. 저자들의 예가
  `.sharedcode` · `.commoncode` 같은 **고유한 이름**이다 (5장, p.106).[^ford2021-hard-parts]
  - **이유가 계측이다** — 그래야 아키텍트가 **코드베이스 안의 공유 컴포넌트 수**와 **애플리케이션
    안에서 공유되는 소스 코드의 비율**로 지표를 낼 수 있다 (5장, p.106).[^ford2021-hard-parts]
- **지표 하나 — 공유 코드의 비율.** 이것이 **모놀리식 애플리케이션을 쪼개는 일이 실현 가능한지의
  좋은 표시**다. 저자들의 기준선이 하나 제시된다 — **`.sharedcode`로 끝나는 모든 네임스페이스의
  문장 수의 합이 전체 소스 코드의 45%를 차지한다면**, 분산 아키텍처로 옮겼을 때 **공유 라이브러리가
  너무 많아지고 공유 라이브러리 의존 때문에 유지보수가 악몽이 될 공산이 크다** (5장,
  p.106).[^ford2021-hard-parts]
  - **45%라는 수치의 근거를 저자들이 적지 않는다.** 예시로 든 값인지 경험에서 나온 임계인지가
    본문에서 갈리지 않는다.
- **지표 둘 — 공유 컴포넌트의 개수.** `.sharedcode`(또는 쓰기로 한 공통 공유 노드 이름)로 끝나는
  **컴포넌트의 수**다. 이 지표는 모놀리스를 쪼갰을 때 **몇 개의 공유 라이브러리(JAR·DLL 따위)나
  공유 서비스가 나올지**에 대한 통찰을 준다 (5장, p.106).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 산출물 형식 예시다. 저자들이 판을 적지 않는다.
  - **두 지표 모두 이름 규약이 지켜져야만 나온다.** 이름을 고유하게 고르라는 조언이 계측을 위한
    전제라는 것이 위 [공유 코드도 고아 클래스다](#공유-코드도-고아-클래스다)와 이 절을 잇는다.

## 거버넌스 — 적합도 함수 하나

- **저자들이 주관성을 먼저 밝힌다** — 이 패턴을 적용하는 데는 **상당한 주관성**이 든다. 리프
  노드의 코드를 루트 네임스페이스로 합칠 것인가, 루트 네임스페이스의 코드를 리프 노드로 옮길
  것인가가 그 예다 (5장, p.107).[^ford2021-hard-parts]
- **No source code should reside in a root namespace.** 배포 시점에 CI/CD 파이프라인으로 촉발되며
  **루트 네임스페이스에 있는 클래스, 곧 고아 클래스를 찾아낸다.** 이행 중에, 특히 이행 기간에
  모놀리스를 계속 유지보수할 때 **컴포넌트를 평탄하게 유지하는 데** 도움이 된다 (5장,
  p.107).[^ford2021-hard-parts]
- **알고리즘은 컴포넌트마다 네임스페이스 노드를 훑어, 마지막 노드가 아닌 노드가 소스 파일을
  담고 있으면 경보를 보내는 것**이다 (5장, p.107, 예제 5-6).[^ford2021-hard-parts]
  - **적합도 함수가 하나뿐인 것이 위 주관성 자백과 맞물린다** — 방향의 선택은 기계가 하지 못하고,
    기계가 검사하는 것은 **결과 상태 하나**(리프 노드에만 코드가 있다)다.

## 책의 사례 — 평탄화

- **적용 대상이 둘이다** — 앞 패턴을 적용한 뒤의 목록에서 **Survey와 Ticket 컴포넌트가 고아
  클래스를 담고 있었다** (5장, pp.107–108, 사가).[^ford2021-hard-parts]

| Component name | Component namespace | Statements | Files |
|---|---|---|---|
| Ticket | `ss.ticket` | 7,009 | 45 |
| Ticket Assign | `ss.ticket.assign` | 7,845 | 14 |
| Ticket Route | `ss.ticket.route` | 1,468 | 4 |
| Survey | `ss.survey` | 2,204 | 5 |
| Survey Templates | `ss.survey.templates` | 1,672 | 7 |

- **티켓 쪽에서 선택지 둘을 저울질한다** — 티켓 배정과 티켓 라우팅 컴포넌트의 코드를 `ss.ticket`
  으로 **합칠 것인가**, `ss.ticket`의 45개 클래스를 별개 컴포넌트로 **가를 것인가**다 (5장,
  p.109, 사가).[^ford2021-hard-parts]
  - **판정의 근거가 복잡도와 변경 빈도다** — **티켓 배정 기능의 복잡도와 잦은 변경** 때문에 그
    컴포넌트들을 따로 두기로 하고, `ss.ticket` 루트 네임스페이스의 고아 코드를 다른
    네임스페이스로 옮겨 새 컴포넌트를 만들었다 (5장, p.109, 사가).[^ford2021-hard-parts]
  - **가를 축은 그 45개 클래스가 실제로 하던 일에서 나온다** — **티켓 생성과 유지보수** ·
    **티켓 완료 로직** · **대부분의 티켓 기능에 공통인 공유 코드** 셋이다 (5장, p.109,
    사가).[^ford2021-hard-parts]
- **결과가 표 5-10이다** (5장, p.109, 사가):[^ford2021-hard-parts]

| Component | Namespace | Responsibility |
|---|---|---|
| Ticket Shared | `ss.ticket.shared` | Common code and utilities |
| Ticket Maintenance | `ss.ticket.maintenance` | Add and maintain tickets |
| Ticket Completion | `ss.ticket.completion` | Complete ticket and initiate survey |
| Ticket Assign | `ss.ticket.assign` | Assign expert to ticket |
| Ticket Route | `ss.ticket.route` | Send ticket to expert |

- **설문 쪽은 반대 방향으로 간다** — 설문 기능은 **거의 바뀌지 않고 그리 복잡하지도 않았다.**
  게다가 `ss.survey.templates` 네임스페이스를 처음 만든 개발자에게 물어보니 **템플릿을 자기
  네임스페이스로 떼어 놓을 강력한 이유가 없었다.** 그래서 일곱 클래스 파일을
  `ss.survey.templates`에서 `ss.survey`로 옮기고 `ss.survey.template` 컴포넌트를 없앴다 (5장,
  p.109, 사가):[^ford2021-hard-parts]

| Component | Namespace | Responsibility |
|---|---|---|
| Survey | `ss.survey` | Send and seceive surveys |

- **이 사가가 이 패턴의 두 방향을 한 번에 보인다** — 티켓은 **올려서 갈랐고**(그 결과 `ss.ticket`이
  서브도메인이 되었다) 설문은 **내려서 합쳤다.** 저자들이 결과를 **언덕(컴포넌트 위의 컴포넌트)도
  고아 클래스도 없고 모든 컴포넌트가 해당 네임스페이스의 리프 노드에만 들어 있다**고 확인한다
  (5장, p.110, 사가).[^ford2021-hard-parts]
  - **같은 진단에 반대 처방이 나온 이유가 기록돼 있다** — 티켓 쪽은 **복잡하고 자주 바뀌어서**
    갈랐고 설문 쪽은 **단순하고 거의 안 바뀌어서** 합쳤다. 위
    [평탄화의 두 방향](#평탄화의-두-방향)이 방향을 정해 주지 않는다고 적은 자리에 이 사가가 판정
    근거를 댄다 — **변경 빈도와 복잡도**다. **저자들이 그 둘을 방향 선택의 기준으로 일반화해
    적지는 않는다.** #hypothesis

## 평탄화 뒤의 컴포넌트 목록

**패턴 셋을 다 적용한 결과가 표 하나로 정리된다. 이 목록이 넷째 패턴부터의 입력이다** (5장,
p.111, 표 5-12).[^ford2021-hard-parts]

| Component | Namespace |
|---|---|
| Login | `ss.login` |
| Billing Payment | `ss.billing.payment` |
| Billing History | `ss.billing.history` |
| Customer Profile | `ss.customer.profile` |
| Expert Profile | `ss.expert.profile` |
| KB Maint | `ss.kb.maintenance` |
| KB Search | `ss.kb.search` |
| Notification | `ss.notification` |
| Reporting Shared | `ss.reporting.shared` |
| Ticket Reports | `ss.reporting.tickets` |
| Expert Reports | `ss.reporting.experts` |
| Financial Reports | `ss.reporting.financial` |
| **Ticket Shared** | `ss.ticket.shared` |
| **Ticket Maintenance** | `ss.ticket.maintenance` |
| **Ticket Completion** | `ss.ticket.completion` |
| **Ticket Assign** | `ss.ticket.assign` |
| **Ticket Route** | `ss.ticket.route` |
| Support Contract | `ss.supportcontract` |
| **Survey** | `ss.survey` |
| User Maintenance | `ss.users` |

- **굵은 글씨는 원문의 조판이다** — 이 패턴이 건드린 여섯 행을 원문이 굵게 찍어 표시한다. 티켓
  다섯은 올려서 갈린 결과이고 설문 하나는 내려서 합친 결과다. 위
  [책의 사례 — 평탄화](#책의-사례--평탄화)가 그 판정 근거를 갖는다.
- **개수가 열여덟에서 스물로 늘었다** — 1장이 소개한 원래 컴포넌트 목록과 견주면 그렇다. 목록의
  원본은 [Sysops Squad 사례](sysops-squad-case.md) §"컴포넌트 열여덟"에 있다. **저자들이 그
  증감을 세어 적지는 않는다.** #hypothesis
- **이 목록에는 아직 도메인이 없다.** 네임스페이스 접두가 제각각이고(`ss.billing` ·
  `ss.customer` · `ss.kb` · `ss.survey` · `ss.supportcontract` · `ss.users`) 그것을 도메인에
  맞추어 다시 짓는 일이 다섯째 패턴의 몫이다 —
  [컴포넌트 도메인 만들기](create-component-domains.md).

## 같은 대상을 개념의 응집으로 가르는 소스와 나란히

**이 KB에는 같은 대상(자바 패키지·네임스페이스)을 다른 기준으로 가르는 소스가 있다. 부딪히는지
보아 둔다.**

- [도메인의 모듈](modules-in-the-domain.md)은 모듈을 **기술 구획이 아니라 모델의 일부**로 다루고,
  **모듈 이름이 유비쿼터스 언어에 들어가며**, 묶는 기준이 **개념의 응집**이라고 적는다.
  기반 구조가 주도한 패키징이 모델을 조각낸다는 진단도 거기 있다.[^evans2003]
- **모순이 아니다 — 두 소스가 다른 물음에 답한다.** 이 페이지의 규칙은 **네임스페이스 트리의
  형태**에 걸린다(코드는 리프 노드에만). 저쪽의 규칙은 **무엇을 한 묶음으로 볼 것인가의 기준**에
  걸린다(개념이 응집하는 단위). 이 페이지는 무엇을 묶을지 말하지 않고, 저쪽은 트리의 깊이를
  제약하지 않는다.
- **오히려 이 패턴이 저쪽 기준을 불러 쓴다** — 위 [평탄화의 두 방향](#평탄화의-두-방향)에서
  올려서 가르는 쪽의 방법이 **기능 분해나 도메인 주도 설계**이고, 그것이 저쪽이 세운 기준이다.
  형태 규칙(리프 노드)과 내용 기준(개념의 응집)이 한 절차 안에서 층을 이룬다.
- **한 자리에서 긴장이 남는다.** 이 페이지는 공유 코드를 **별개 컴포넌트로 뽑으라**고 하고 그
  이름을 **도메인에 없는 낱말**(`.sharedcode`)로 고르라고 한다. 저쪽의 조항은 **모듈 이름이
  유비쿼터스 언어에 들어가야 한다**는 것이므로, 도메인 언어에 일부러 없는 이름을 만드는 이 조언과
  방향이 반대다. **다만 목적이 다르다** — 이쪽 이름은 사람이 읽는 이름이 아니라 **계측을 위한
  표식**이고, 그 쓰임이 위
  [공유 네임스페이스의 이름과 거기서 나오는 지표 둘](#공유-네임스페이스의-이름과-거기서-나오는-지표-둘)에
  적혀 있다. **이 대질은 이 KB가 세운 것이고 두 소스가 서로를 호명하지 않는다.** #hypothesis

## 이어지는 페이지

- [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md) — 이 패턴이 셋째로
  놓이는 절차
- [공통 도메인 컴포넌트 모으기](gather-common-domain-components.md) — 이 패턴 앞에 오는 둘째
- [컴포넌트를 식별하고 크기를 맞추기](identify-and-size-components.md) — 서브도메인이라는 이름이
  처음 나오는 첫째
- [컴포넌트 의존 판정](determine-component-dependencies.md) — 이 패턴 뒤에 오는 넷째. 위 결과
  목록을 입력으로 받는다
- [컴포넌트 도메인 만들기](create-component-domains.md) — 위 목록의 네임스페이스를 도메인에
  맞추어 다시 짓는 다섯째
- [도메인의 모듈](modules-in-the-domain.md) — 같은 대상을 개념의 응집으로 가르는 축
- [아키텍처 적합도 함수](architecture-fitness-functions.md) — 위 적합도 함수의 분류 어휘
- [Sysops Squad 사례](sysops-squad-case.md) — 위 사례가 대입되는 체계
- [마이크로서비스 소스와 빌드의 배치](microservice-source-layout.md) — 같은 낱말(저장소·폴더)을
  쓰지만 대상이 다른 축. 그쪽은 여러 서비스의 저장소와 빌드를 배치하고 이쪽은 한 배포 산출물 안의
  네임스페이스 트리를 다룬다
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) —
  이 페이지가 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 5장 "Component-Based
    Decomposition Patterns" §"Flatten Components Pattern"(pp.101–110) — 도입(p.101) ·
    §"Pattern Description"(pp.102–106) · §"Fitness Functions for Governance"(p.107) ·
    §"Sysops Squad Saga: Flattening Components"(pp.107–110). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 18, 실측). 직인용 둘(용어 규정 셋과 평탄화 방향의 조언 상자)은
    `pdftotext -layout` 추출로 문자 단위 대조했고 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한
    낱말로 이었다. 원문이 이탤릭으로 조판한 낱말은 인용 안에서 이탤릭을 유지했고, 원문이
    고정폭으로 조판한 네임스페이스는 인용 블록 안에서는 조판을 옮기지 않았다(인용 안의 인라인
    코드가 이 KB의 조판 규약에 없다). 원문의 용어 규정 셋은 들여쓴 정의 목록이라 인용 블록으로
    옮기며 항목 사이에 빈 줄을 넣었다 — 낱말은 보태거나 빼지 않았다. **표 5-8·5-9·5-10·5-11은
    `pdftoppm -r 160 -png`로 렌더해 눈으로 대조한 뒤 원문 열 머리글과 셀 값을 영어 그대로
    옮겼다.** 표 5-8의 Survey 행 앞에 붙은 화살표는 원문이 그 행을 지목하려고 찍은 조판 표시라
    그대로 두었다. **표 5-11의 `Send and seceive surveys`는 원문 오식이다**(receive) — 렌더
    이미지로 확인해 원문 그대로 옮겼다. **의사코드 예제 하나(5-6)는 펜스로 옮기지 않고 알고리즘만
    산문으로 적었다** — 실행되는 코드가 아니라 저자들이 만든 의사 언어이고, 이 KB의 적합도 함수
    대표 펜스는 ford2022 예제 2-1 하나로 유지한다(SCHEMA §3). 도판 일곱(그림 5-6 용어 셋 ·
    5-7 내려서 합치기 · 5-8 올려서 가르기 · 5-9 루트의 공유 코드 · 5-10 공유 코드의 컴포넌트화 ·
    5-11 고아 클래스를 가진 두 컴포넌트 · 5-12 평탄화 결과)은 `pdftoppm`으로 렌더해 눈으로
    읽었고, 도판 자체는 재현하지 않고 본문이 그 도판에 대해 적는 것과 그림 5-6의 배치만
    옮겼다. 인쇄판 p.110은 다음 절로 넘어가는 표 5-12를 예고하며 끝나고 그 표는
    p.111 첫머리에 있다 — 이 패턴의 결과 목록이므로 이 페이지가 갖는다. **표 5-12도
    `pdftoppm -r 160 -png`로 렌더해 눈으로 대조한 뒤 원문 열 머리글과 셀 값을 영어 그대로
    옮겼고, 원문이 여섯 행을 굵게 찍은 조판도 그대로 남겼다** — 네임스페이스는 이 KB의
    조판 규약에 따라 인라인 코드로 감쌌고 값 자체는 고치지 않았다. 굵은 글씨는 원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

[^evans2003]: Evans 2003, 5장 §MODULES (A.K.A. PACKAGES)(pp.109–116). 이 페이지는 그 기준을
    대질에만 쓴다 — 전문과 직인용은 [도메인의 모듈](modules-in-the-domain.md)이 갖는다.
