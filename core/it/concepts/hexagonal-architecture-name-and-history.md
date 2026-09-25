---
type: concept
title: 헥사고날 아키텍처의 이름과 역사
description: 포트와 어댑터 패턴의 이름과 내력을 그 원저자 콕번이 직접 밝힌 원전 — "육각형(Hexagonal)"이 육각형의 여섯 변이 무엇을 뜻하는지 알기 전에 붙인 임시 이름이었고 여섯이라는 수에 특별한 뜻이 없어 실은 부적절하며 소프트웨어 어디에도 육각형이 나타나지 않는다는 실토, 그래서 진짜 포트와 진짜 어댑터가 있으므로 "포트와 어댑터"로 고쳐 부른 근거, 1988년의 첫 아픔에서 2005년 첫 기록과 2015년 구동/피구동과 2022년 요구 인터페이스와 2023년 Configurable Receiver까지의 연표, 그리고 이 패턴의 편익 여섯과 복잡도 비용 다섯 — 그 비용이 타입 선언 언어에서 더 크다는 조건과, 기술 변화에 데어 보지 않은 사람에게는 비용이 지나쳐 보인다는 관찰
generated: { by: "claude-opus-5", at: "2026-09-25T00:00:00Z" }
sources:
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
---

# 헥사고날 아키텍처의 이름과 역사

- [이름의 유래](#이름의-유래)
- [짧은 역사](#짧은-역사)
- [원문이 밝히는 더 긴 연표](#원문이-밝히는-더-긴-연표)
- [비용과 편익](#비용과-편익)
- [이어지는 페이지](#이어지는-페이지)

이 패턴의 규정 자체는 [포트와 어댑터 규정](ports-and-adapters-defined.md)에 있다. 이 페이지는
그 패턴에 왜 "헥사고날"이라는 이름이 붙었고 왜 "포트와 어댑터"로 고쳐 불리게 됐는지, 그것이 어떤
아픔에서 자라 나왔는지, 그리고 저자가 이 패턴의 비용과 편익을 어떻게 계상하는지를 담는다 — 모두
원저자 콕번이 직접 밝힌 것이다.

## 이름의 유래

- "헥사고날 아키텍처"라는 이름이 임시방편이었다는 것을 저자가 실토한다 (1장 §"1.3. Why the name
  "Hexagonal" Architecture?"):[^cockburn2024]

  > The name "Hexagonal Architecture" was a placeholder name I (Alistair) came up with years before
  > I understood what the sides of the hexagon stood for. I just knew they had to be there. As a
  > pattern name, it is not really appropriate, since the number six has no particular meaning. In
  > practice you might have three, five, or any number of ports, not six. Additionally, a hexagon is
  > just a geometric shape. It doesn't show up anywhere in your software.

  - 즉 여섯이라는 수에는 특별한 뜻이 없고, 실제로 포트는 셋일 수도 다섯일 수도 몇이든 될 수
    있으며, 육각형은 그저 기하 도형일 뿐 소프트웨어 어디에도 나타나지 않는다.
- 왜 육각형으로 그렸는지는 저자가 2005년 RSS 피드에 쓴 글에 있다 (1장 §"1.3. Why the name
  "Hexagonal" Architecture?"):[^cockburn2024]

  > Somewhere in the mid-90s I started drawing a symmetric architecture in which the database is
  > considered not at the "bottom of the stack", but fully outside the application, just as we
  > recommend doing with the user interface.
  >
  > To break up perceptions about top and bottom and left and right, I drew it with a hexagonal
  > shape, and came up with the rather lame name HexagonalArchitecture --- simply because I could
  > not identify think of what the "hexagon" meant, but knew it had to have facets, and no number
  > smaller than 5 made visual sense (and pentagons are harder to draw than hexagons).

  - 위와 아래, 왼쪽과 오른쪽이라는 인식을 깨뜨리려고 대칭 도형으로 그렸고, 다섯보다 작은 수는
    시각적으로 말이 안 되는 데다 오각형이 육각형보다 그리기 어려워 육각형이 됐다는 것이다.
    데이터베이스를 "스택의 바닥"이 아니라 사용자 인터페이스처럼 애플리케이션 완전히 바깥에 두는
    대칭 구조라는 착상이 이 그림의 요지다.
- 이름을 고친 근거는 정확함이다 — **이 책에서 우리는 정확하기를 원한다: 패턴의 이름은 "포트와
  어댑터"다. 진짜로 포트가 있고, 진짜로 어댑터가 있으며, 당신의 아키텍처가 그것들을 보여 줄
  것이기 때문이다** (1장 §"1.3. Why the name "Hexagonal" Architecture?").[^cockburn2024] 저자는
  "헥사고날 아키텍처"가 패턴으로 들어오는 갈고리로는 잘 기능했다고 — 기억하기 쉽고 대화를
  일으킨다고 — 인정하면서도, 올바른 이름은 포트와 어댑터라고 못 박는다.
- 저자는 책을 요약하는 7장에서 이 이름 문제를 실무 처방으로 되돌린다 — "헥사고날 아키텍처"라는
  이름의 진짜 문제는 사람들이 실제 포트와 어댑터 아키텍처를 구현하지도 않은 채 여기저기 육각형만
  그리며 "헥사곤"을 들먹이게 만드는 데 있다는 것이다. 그래서 저자는 **기술적 논의에 들어가거든
  "헥사곤"이라는 낱말을 버리고 대신 "포트"라 말하라**고 처방한다 — 그것이 아키텍처를 더 낫게 하고
  많은 오해를 걷어 낸다고 본다 (7장 §"7.4. Why the name "Hexagonal" Architecture?").[^cockburn2024]

## 짧은 역사

- 저자가 이 패턴의 연표를 아픔의 기록으로 적는다 (1장 §"1.2. Short history of the
  pattern"):[^cockburn2024]
  - 1988년 — 콕번이 자기 스몰토크 프로토타입에는 모델·뷰·컨트롤러를 무심코 구현했으나 함께 일한
    C 프로그래머는 그러지 않았다. 입력 소스를 바꿔야 하게 되자 C 프로그램을 뜯어 다시 써야 했다.
    첫째 아픔.
  - 1994년 — 고정가·고정 기한의 객체-관계 매퍼 프로젝트에서 인프라 설계자들이 성능을 위해 SQL
    데이터베이스 설계를 바꿔야 했는데, 애플리케이션 프로그래머들이 인메모리 시험용 데이터베이스로
    갈아 끼울 수 없어 프로젝트를 몇 주 멈추고 매퍼를 다급히 다시 썼다. 둘째 아픔.
  - 2000년 — 입력 소스와 알림 방식의 온갖 변종·버전으로 애먹던 친구의 문제를 포트와 어댑터
    아키텍처로 풀었다.
  - 2005년 — 콕번이 실제 프로젝트에(Spring으로) 처음 이 패턴을 구현하고 코드 사례와 함께 정리하며
    더 정확한 이름 "포트와 어댑터"를 붙였다.
  - 2015년 — 구동·피구동 어댑터라는 개념과 인터페이스를 "for_doing_something"으로 짓는 이름
    관례가 더해졌다.
  - 2022년 — 이 패턴을 "Component + Strategy"의 특수 사례로 정식화하고 **요구 인터페이스(required
    interface)** 개념을 세웠다.
  - 2023년 — 더 완전하고 정확한 **Configurable Receiver** 패턴이, 살짝 부정확했던 앞선 패턴
    "Configurable Dependency"를 대체했다.
  - 2024년 — 후안과 콕번이 협업을 마무리해 이 책의 프리뷰판을 냈다.
- 이 연표가 [포트와 어댑터 규정](ports-and-adapters-defined.md)의 두 요소와 이어진다 — 요구
  인터페이스가 2022년에, 구동/피구동 구분이 2015년에 자리 잡았다는 것이 그 규정이 한 번에
  완성된 것이 아니라 자라 온 것임을 보인다.

## 원문이 밝히는 더 긴 연표

위 [짧은 역사](#짧은-역사)는 1장의 압축된 연표이고, 6장 6.1절의 더 긴 연표가 그 계기와 정확한
연도를 원저자의 말로 채운다 — 후안이 이 책에 남긴 마지막 기여 하나가 이 연표를 다시 손봐 바로잡은
것이라고 콕번이 밝힌다 (6장 §"6.1. The longer history").[^cockburn2024]

- 이 패턴을 만든 동기가 대칭에 대한 갈증이었음을 저자가 밝힌다 — 그는 스몰토크의 모델-뷰-컨트롤러로
  **구동 쪽에서는** 드라이버를 쉽게 갈아 끼울 수 있었기에 **피구동 쪽에서도** 같은 것이 되어야
  한다고 당연히 기대했으나, 시스템 설계자들에게서 안 된다는 말만 들었다. 그 방어로 "어떻게 하면
  가능할까"를 스스로 묻기 시작했고, 처음엔 그것을 _shunt_, 그다음엔 _loopback_(목이 아직 발명되기
  전이다)이라 불렀으며, 2004–2005년에 이르러서야 그것을 실제로 해내는 코드를 쓸 상황이 됐다고 적는다
  (6장 §"6.1. The longer history").[^cockburn2024] 그는 자신이 응용 프로그래머로서 필요했던 안전과
  교체 기능을 갖기 위해 이 아키텍처를 만들었다고 못 박는다.
- 육각형 도형을 **처음 그린 해는 1994년**이다 — 객체 지향 프로그래밍을 다루던 그의 일주일짜리 수업
  "Design in Object Technology"(뒤에 책이 된다)의 슬라이드에 이미 육각형 모양과 기본 착상이 있었고,
  다만 그때는 면(facet)이 무엇을 뜻하는지 그 자신도 몰랐으되 그것들이 API여야 한다는 것만 알았다고
  적는다 (6장 §"6.1. The longer history", 그림 6.1 "가장 이른 육각형 그림, 1994년").[^cockburn2024]
- 위 짧은 역사가 2000년과 2005년 사이에 비워 둔 자리를 6.1이 채운다 — **2003년에 콕번이 워드
  커닝엄의 위키위키 웹(c2 wiki)에 "Hexagonal Architecture"라는 제목의 글을 처음 올렸다**
  (6장 §"6.1. The longer history").[^cockburn2024]
- 2005년의 정확한 날짜도 원문에 있다 — **2005년 9월 4일 콕번이 GoF(Gang of Four) 형식에 맞춰 패턴을
  정식으로 적고 올바른 이름 "Ports & Adapters"를 붙였으며, 9월 5일에 자기 사이트에 그 글을 올리고
  무엇을 왜 했는지 알리는 RSS를 내보냈다** (6장 §"6.1. The longer history").[^cockburn2024]
- 위 짧은 역사가 2015년으로 적은 구동·피구동 어휘의 자리를 6.1이 더 정확히 짚는다 — 콕번이 패턴의
  역사·의도·구조를 설명하는 강연을 하겠다고 청한 것이 2015년이고, **그 강연이 실제로 열린 것은
  2017년 파리에서**다. 토마 피에랭(Thomas Pierrain)이 청중 앞에서 예제를 라이브로 프로그래밍했고
  ("Alistair in the Hexagone"), 콕번은 이 자리에서 왼쪽·오른쪽을 가리키는 말 **"driving"과
  "driven"을 만들고 포트를 "for doing something" 형식으로 이름 짓는 관례**를 세웠다고 적는다
  (6장 §"6.1. The longer history").[^cockburn2024] 같은 자리에서 처음엔 피구동 액터를
  저장소(repository)와 수신자(recipient)로 갈랐으나, 그 구분은 뒤에 중요하지 않게 되어 2024년 저술
  시점에는 둘 다 "피구동 액터"로 부른다고 밝힌다.
- 2021년의 한 정정도 원문에 있다 — **2021년 10월 9일 콕번과 후안이 원문에서 구동 쪽의 어댑터와
  포트에 대한 오해를 부르던 한 문장을 함께 다시 썼다.** 콕번은 후안이 그 오랜 세월 그 글에서 찾아낸
  잘못된 문장이 이 하나뿐이었던 것을 사소한 기적으로 여긴다고 적는다 (6장 §"6.1. The longer
  history").[^cockburn2024] 이 문장 정정의 내용은 [포트와 어댑터 규정](ports-and-adapters-defined.md)의
  어댑터 규정에 2023년 주석과 함께 정박돼 있다.
- 저자가 이 30년 가까운 여정을 돌아보며 패턴 자체는 단순하다고 요약한다 — **앱이나 시스템 사방에
  API를 두고, 각 피구동 연결을 설정할 인수를 하나씩 넘기면 된다. 그 이상은 없다**
  (6장 §"6.1. The longer history").[^cockburn2024]

## 비용과 편익

- 저자가 드는 편익 여섯 (1장 §"1.4. The costs and benefits of this pattern"):[^cockburn2024]
  - 시험 — 프로덕션 연결 없이 시스템 수준 시험을 쓰고 돌릴 수 있어 더 순수하고 빠르다.
  - 시험을 더 논함 — 입력이든 출력이든 어느 연결이나 프로덕션 연결과 시험 연결을 재컴파일 없이
    맞바꿀 수 있다.
  - 누출 차단 — 애플리케이션을 둘러싼 시험의 벽이, 누군가 UI·기술 세부를 업무 구역으로, 또는
    업무 로직을 UI·외부 기술 구역으로 누출시킬 때마다 그것을 잡아낸다.
  - 큰 시스템의 분리 — 팀마다 자기 구역 코드를 독립적으로 개발하고 따로 시험한 뒤, 정의되고
    시험된 인터페이스에 따라 이을 수 있다.
  - 오래 도는 시스템 — 기술과 업무 필요가 여러 해에 걸쳐 바뀔 때 외부 연결 하나를 다른 것으로
    갈 수 있다.
  - 도메인 주도 설계 — 기술 요소가 애플리케이션 경계 밖으로 안전히 나가고 나면, 산만함 없이
    도메인 설계에 집중할 수 있다.
- 그리고 복잡도 비용 다섯 — 저자는 이 비용이 **타입 선언 언어에서 동적·타입 추론 언어보다 더
  크게 나타난다**고 조건을 단다 (1장 §"1.4. The costs and benefits of this
  pattern"):[^cockburn2024]
  - 피구동 액터마다 인스턴스 변수를 더하거나, 필요할 때마다 그 정보를 얻어 오거나 해야 한다.
  - 피구동 액터마다 생성자 인수나 세터 함수를 더하거나, 그 정보를 얻으려 Configurator를 호출해야
    한다.
  - Configurator를 설계하고 더해야 한다.
  - 타입 선언 언어에서는 요구 인터페이스를 선언해야 한다.
  - 타입 선언 언어에서는 포트 선언을 위한 폴더 구조를 더 두게 된다.
- 저울질에 대한 저자의 관찰이 냉정하다 — **기술 변화나 인터페이스 이동, 업무 로직의 누출, 외부
  기술 세부의 침입, 또는 시험과 프로덕션을 오가려 시스템을 재컴파일하는 일로 데어 본 적이 없는
  사람들은 이 비용이 패턴을 구현할 값어치에 비해 너무 높아 보인다고 말한다**
  (1장 §"1.4. The costs and benefits of this pattern").[^cockburn2024] 인터페이스 몇 개와 인스턴스
  변수 몇 개를 더하는 수고가 값어치가 있다고 사람들이 결정하는 데에는 대개 프로젝트에서 고생을
  겪는 일이 필요하다는 것이다.
- 저자 후안이 책을 요약하는 7장에서 이 회계를 다시 정리하며, 위 1.4절이 들지 않은 항목을 더한다
  (7장 §"7.3. The costs and benefits of this pattern"):[^cockburn2024]
  - 편익 쪽에 더한 것 — 시험 개선이 여러 갈래로 나타난다는 것(업무 로직 시험이 인메모리라 빠르고,
    앱과 어댑터를 서로 격리해 따로 시험한 뒤 나중에 통합하며, 이미 끝낸 시험이 회귀 시험이 된다),
    TDD·BDD 같은 방법론을 적용하기 쉬워지되 **패턴이 그 방법론을 처방하는 것은 아니라는** 단서(앱
    전체를 먼저 짜고 나중에 시험하는, 안에서 밖으로의 방법론도 쓸 수 있다), 유지보수성이 오르면
    기술 부채가 준다는 연결, 그리고 어떤 기술을 쓸지 몰라도 업무 로직을 개발할 수 있어 **기술
    결정을 미룰 수 있다**는 것.
  - 비용 쪽에 더한 것 — 전체 구조와 시작 과정과 빌드가 고전적 3층 아키텍처보다 복잡하다는 것,
    어댑터가 요구 인터페이스를 각 기술의 특정 인터페이스로 번역해야 하므로 피구동 쪽에 **간접이 한
    겹 더** 든다는 것, 도메인 모델의 개체를 영속 모델의 개체로 오가며 옮기는 **매퍼가 더 필요할 수
    있다**는 것, 이 아키텍처를 배우기가 어려워 경험이 필요하고 초보 프로그래머에게 버겁다는 것,
    그리고 새 프로젝트를 시작하는 데 시간이 더 들어 **중간 규모에서 큰 규모의 프로젝트에 가장
    알맞다**는 것.
- 저자 자신의 판단은 분명하다 — 2024년 저술 시점에 이것이 두 저자가 애플리케이션·시스템을 짓는
  기본 방식이며, 일회성 프로그램을 쓰는 것 같은 특별한 사정이 아니라면 이 패턴을 쓰지 않을 이유가
  없다고 적는다 (1장 §"1.4. The costs and benefits of this pattern").[^cockburn2024] 같은 회계
  — 패턴마다 비용을 함께 적는 형식 — 을 파이썬 축이
  [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md)의 "이 축을
  관통하는 회계"에서 되풀이한다.

## 이어지는 페이지

- [포트와 어댑터 규정](ports-and-adapters-defined.md) — 이 패턴의 규정과 다섯 요소
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 이 KB에서 사는 자리
- [헥사고날 아키텍처](../synthesis/hexagonal-architecture.md) — 이 축의 허브

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 1장 §"1.2. Short history of the pattern" ·
    §"1.3. Why the name "Hexagonal" Architecture?" · §"1.4. The costs and benefits of this pattern" ·
    6장 §"6.1. The longer history"(그림 6.1 "가장 이른 육각형 그림, 1994년" 포함 — 본문 서술이
    그 내용을 담으므로 이미지를 열지 않았다) · 7장 §"7.3. The costs and benefits of this pattern" ·
    §"7.4. Why the name "Hexagonal" Architecture?". EPUB(Calibre 변환본), 쪽 앵커 없음 — locator는 장·절 번호.
