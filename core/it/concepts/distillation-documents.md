---
type: concept
title: 증류 문서와 강조된 핵심
description: 모델과 코드를 고치지 않고 무엇이 핵심인지 팀에 알리는 두 보조 문서의 원전 — 모델이 아직 없을 때도 개발의 초점이 필요하고 핵심이 여러 경계 컨텍스트에 걸칠 수 있다는 문제, 한 쪽 분량으로 핵심 도메인과 그것이 가져올 값을 쓰라는 도메인 비전 선언의 조항과 무엇이 들고 무엇이 빠지는가의 대조, 비전 선언만으로는 영향이 거의 없다는 진단과 사람마다 날마다 핵심을 다르게 집어낸다는 관찰, 구조 변경이 이상적이지만 바로 그 시야가 없어서 구조 변경이 어렵다는 순환, 서너 쪽에서 일곱 쪽의 증류 문서와 그 위험 셋과 최소주의라는 대응, 이백 쪽 모델에 색인표와 형광펜을 더한 표시된 핵심 사례, 그리고 증류 문서를 변경의 중대성을 재는 계기로 쓰는 절차 규칙, 그리고 팀이 통째로 바뀐 인계에서 이 문서가 테스트 모음과 함께 설계의 의도를 전달한 결론의 기록
generated: { by: "claude-opus-5", at: "2026-09-14T13:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 증류 문서와 강조된 핵심

- [모델을 고치지 않는 증류](#모델을-고치지-않는-증류)
- [도메인 비전 선언](#도메인-비전-선언)
- [무엇이 비전 선언에 들고 무엇이 빠지는가](#무엇이-비전-선언에-들고-무엇이-빠지는가)
- [비전 선언만으로는 모자라다](#비전-선언만으로는-모자라다)
- [증류 문서](#증류-문서)
- [표시된 핵심](#표시된-핵심)
- [증류 문서를 절차의 계기로 쓰기](#증류-문서를-절차의-계기로-쓰기)
- [인계에서 이 문서가 한 일](#인계에서-이-문서가-한-일)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델과 코드를 고치지 않고 무엇이 핵심인지를 팀 전체가 같게 보게 하려면 무엇을
쓰는가.**

이 두 패턴을 한 페이지에 둔 것은 원전 자신이 둘을 한 묶음으로 소개하기 때문이다 — **이 장의
증류 패턴 대부분은 핵심 도메인을 증류하기 위해 모델과 코드를 어떻게 바꾸는지를 보인다. 그러나
다음 두 패턴인 도메인 비전 선언과 강조된 핵심은 보조 문서의 사용이 아주 작은 투자로 핵심에
대한 소통과 인식을 개선하고 개발 노력을 집중시킬 수 있음을 보인다** (15장,
p.414).[^evans2003] 그리고 뒤의 패턴이 앞의 패턴만으로는 부족하다는 데서 출발하므로 둘을
갈라 놓으면 각각이 상대를 요약해야 한다.

## 모델을 고치지 않는 증류

- 두 패턴이 닫히는 자리에서 그 지위가 다시 확인된다 — **비전 선언과 강조된 핵심은 알리고
  인도하지만 모델이나 코드 자체를 실제로 수정하지는 않는다** (15장, p.421).[^evans2003]
  모델을 실제로 바꾸는 쪽은 [일반 하위 도메인](generic-subdomains.md)과
  [격리된 핵심](segregated-core.md)이다.
- 그래서 이 두 패턴의 값은 **투자 대비**로 계상된다. [핵심 도메인](../concepts/core-domain.md)이 증류
  기법들을 급진성 순으로 늘어놓을 때 이 둘이 가장 앞에 선다.

## 도메인 비전 선언

- 문제 서술이 시점 셋을 든다 (15장, p.415):[^evans2003]

> At the beginning of a project, the model usually doesn't even exist, yet the need to focus its
> development is already there. In later stages of development, there is a need for an
> explanation of the value of the system that does not require an in-depth study of the model.
> Also, the critical aspects of the domain model may span multiple BOUNDED CONTEXTS, but by
> definition these distinct models can't be structured to show their common focus.

  - **셋째 문제가 이 패턴을 코드로 대체할 수 없게 만든다.** 핵심이 여러
    [경계 컨텍스트](../concepts/bounded-context.md)에 걸치면 어떤 코드 구조도 그 공통 초점을
    보일 수 없다. 문서만이 그 경계를 가로지른다.
- 기존 관행과의 차이가 규정된다. 많은 팀이 경영진용 비전 선언을 쓰고 **그중 최선은 애플리케이션이
  조직에 가져올 구체적 값을 펼쳐 놓는다.** 그러나 **보통 그 문서는 프로젝트가 예산을 받고 나면
  버려지고 실제 개발 과정에서 결코 쓰이지 않으며 기술 인력이 읽지도 않는다** (15장,
  p.415).[^evans2003]
- 도메인 비전 선언(domain vision statement)은 **그런 문서를 본떴지만 도메인 모델의 성질과
  그것이 기업에 어떻게 값진가에 초점을 둔다. 개발의 모든 국면에서 경영진과 기술 인력이 자원
  배분을 인도하고 모델링 선택을 인도하고 팀원을 교육하는 데 직접 쓸 수 있다. 도메인 모델이
  여러 주인을 섬긴다면 이 문서가 그들의 이해가 어떻게 균형 잡히는지를 보일 수 있다** (15장,
  p.415).[^evans2003]
- 처방 문단 (15장, p.415):[^evans2003]

> Write a short description (about one page) of the CORE DOMAIN and the value it will bring,
> the "value proposition." Ignore those aspects that do not distinguish this domain model from
> others. Show how the domain model serves and balances diverse interests. Keep it narrow.
> Write this statement early and revise it as you gain new insight.

- 쓰임이 둘로 적힌다 — **모델과 코드 자체를 증류하는 계속되는 과정에서 개발 팀을 공통의 방향에
  붙들어 두는 이정표로 쓸 수 있다.** 그리고 **비기술 팀원, 경영진, 심지어 고객과도 공유할 수
  있다(물론 독점 정보를 담은 경우는 빼고)** (15장, p.415).[^evans2003]

## 무엇이 비전 선언에 들고 무엇이 빠지는가

- 저자가 두 도메인에 대해 드는 대조다 (15장, p.416).[^evans2003] **중요하지 않아서 빠지는 것이
  아니라 도메인 모델에 대한 진술이 아니라서 빠진다**는 것이 이 대조의 요점이다.

| 도메인 | 비전 선언에 드는 것 | 중요하지만 비전 선언이 아닌 것 |
|---|---|---|
| 항공권 예약 | **모델은 승객 우선순위와 항공사 예약 전략을 표상하고 유연한 정책에 근거해 그것을 균형 잡을 수 있다. 승객 모델은 항공사가 단골 고객과 맺으려 애쓰는 "관계"를 반영해야 하고, 그래서 쓸모 있게 압축된 형태로 승객의 이력과 특별 프로그램 참여와 전략적 기업 고객과의 제휴 등을 표상해야 한다. 서로 다른 사용자의 서로 다른 역할이 관계 모델을 풍부하게 하고 보안 프레임워크에 필요한 정보를 먹이도록 표상된다. 모델은 효율적인 경로·좌석 검색과 기존 항공권 예약 시스템과의 통합을 지원해야 한다** | **UI는 전문 사용자에게 매끄럽되 처음 쓰는 사람도 접근할 수 있어야 한다. 웹과 다른 시스템으로의 데이터 전송 등으로 접근이 제공되므로 인터페이스는 XML을 중심으로 설계되고 변환 계층을 둔다. 로고의 다채로운 애니메이션 판이 클라이언트 기계에 캐시되어야 한다. 예약 제출 시 5초 안에 시각적 확인을 준다. 보안 프레임워크가 신원을 인증하고 역할에 따라 기능 접근을 제한한다** |
| 반도체 공장 자동화 | **도메인 모델은 웨이퍼 팹 안의 자재와 장비의 상태를, 필요한 감사 기록이 제공되고 자동 제품 라우팅이 지원될 수 있는 방식으로 표상할 것이다. 모델은 공정에 필요한 인적 자원을 포함하지 않되 레시피 다운로드를 통한 선택적 공정 자동화를 허용해야 한다. 공장 상태의 표상은 사람 관리자가 이해할 수 있어야 하며 그들에게 더 깊은 통찰과 더 나은 의사 결정 지원을 준다** | **소프트웨어는 서블릿으로 웹을 지원하되 대안 인터페이스를 허용하도록 구조화되어야 한다. 사내 개발과 유지 비용을 피하고 외부 전문성 접근을 최대화하기 위해 가능한 한 업계 표준 기술을 쓰고 오픈 소스 해법을 선호한다. 웹 서버는 전용 서버에서 돌고 애플리케이션도 단일 전용 서버에서 돈다** |

- **두 사례의 오른쪽 열이 전부 실제 요구사항이라는 점이 중요하다.** 저자가 그 열의 머리에
  **"이것도 중요하지만"**이라고 적는다. 비전 선언의 좁음은 중요도의 판정이 아니라 대상의
  판정이다.

## 비전 선언만으로는 모자라다

- 강조된 핵심(HIGHLIGHTED CORE)의 문제 서술이 앞 패턴의 한계에서 시작한다 — **도메인 비전
  선언은 핵심 도메인을 넓은 말로 식별하지만 구체적인 핵심 모델 요소의 식별은 개인의 해석에
  맡긴다. 팀에 예외적으로 높은 수준의 소통이 있지 않은 한 비전 선언만으로는 영향이 거의 없을
  것이다** (15장, p.417).[^evans2003]
- **관찰이 두 겹으로 적힌다** (15장, p.417):[^evans2003]

> Even though team members may know broadly what constitutes the CORE DOMAIN, different people
> won't pick out quite the same elements, and even the same person won't be consistent from one
> day to the next.

  - 그리고 그 부정확성이 비용으로 계상된다 — **핵심 부분을 식별하려고 모델을 끊임없이 거르는
    정신 노동은 설계 사고에 쓰는 편이 나은 집중력을 흡수하고, 모델에 대한 포괄적 지식을
    요구한다. 핵심 도메인은 보기 쉽게 만들어져야 한다** (15장, p.417).[^evans2003]
- **이상적인 해법이 순환에 걸린다는 진단이 이 패턴의 존재 이유다** (15장, p.417):[^evans2003]

> Significant structural changes to the code are the ideal way of identifying the CORE DOMAIN,
> but they are not always practical in the short term. In fact, such major code changes are
> difficult to undertake without the very view the team is lacking.

  - 일반 하위 도메인을 분할하는 것 같은 모델 조직의 구조 변경이 **모듈이 이야기를 말하게** 할
    수 있지만 **핵심 도메인을 알리는 유일한 수단으로 삼기에는 곧바로 겨냥하기에 너무 야심 차다**
    (15장, p.417).[^evans2003] 그래서 **더 가벼운 해법이 이 공격적인 기법들을 보충해야 한다.**
- 적용 상황이 셋 든다 (15장, p.417):[^evans2003]
  - **핵심을 물리적으로 분리하지 못하게 하는 제약이 있을 수 있다.**
  - **핵심을 잘 구별하지 못하는 기존 코드에서 출발할 수 있는데, 더 나은 증류를 향해 효과적으로
    리팩터링하려면 바로 그 핵심을 보고 그 시야를 공유해야 한다.**
  - **진전된 단계에서도 주의 깊게 선택된 몇 개의 도해나 문서가 팀에 정신적 닻과 진입점을
    제공한다.**
- **문서를 거의 쓰지 않는 팀에도 적용된다** — 이 문제는 **정교한 UML 모델을 쓰는 프로젝트와
  외부 문서를 거의 두지 않고 코드를 모델의 주 저장소로 쓰는 프로젝트에 똑같이 일어난다.**
  익스트림 프로그래밍 팀은 더 최소주의적이어서 **이 보충물을 더 격식 없고 더 임시적으로 둘 수
  있지만(예를 들어 모두가 보도록 벽에 손으로 그린 도해) 이 기법들은 그 절차에 잘 접힌다**
  (15장, pp.417–418).[^evans2003]
- **이 패턴의 지위가 한 줄로 규정된다** (15장, p.418):[^evans2003]

> Marking off a privileged part of a model, along with the implementation that embodies it, is
> a reflection on the model, not necessarily part of the model itself.

  - 그래서 수단은 자유롭다 — **모두가 핵심 도메인을 쉽게 알게 만드는 어떤 기법이든 된다.**
    저자는 그 부류를 대표하는 둘만 제시한다.

## 증류 문서

- 무엇을 쓰는가 — **핵심 도메인을 서술하고 설명하는 별도 문서를 만드는 일이 잦다. 그것은 가장
  본질적인 개념 객체의 목록만큼 단순할 수도 있고, 그 객체들에 초점을 맞춰 가장 결정적인 관계를
  보이는 도해 집합일 수도 있다. 근본적인 상호작용을 추상 수준에서 또는 예시로 훑을 수도 있다**
  (15장, p.418).[^evans2003] UML 클래스·시퀀스 도해, 도메인 특유의 비표준 도해, 주의 깊게
  쓰인 산문, 또는 그 조합 무엇이든 된다.
- **무엇이 아닌지가 더 중요하다** (15장, p.418):[^evans2003]

> A distillation document is not a complete design document. It is a minimalist entry point that
> delineates and explains the CORE and suggests reasons for closer scrutiny of particular
> pieces. The reader is given a broad view of how the pieces fit and guided to the appropriate
> part of the code for more details.

- 처방 문단 (15장, p.418):[^evans2003]

> Write a very brief document (three to seven sparse pages) that describes the CORE DOMAIN and
> the primary interactions among CORE elements.

- **별도 문서의 통상적 위험 셋이 그대로 열거된다** (15장, p.418):[^evans2003]
  - **문서가 유지되지 않을 수 있다.**
  - **문서가 읽히지 않을 수 있다.**
  - **정보 원천을 늘림으로써 복잡성을 꿰뚫는다는 자기 목적을 무너뜨릴 수 있다.**
- 대응이 하나로 좁혀진다 — **이 위험을 제한하는 최선의 방법은 절대적으로 최소주의가 되는
  것이다. 일상적 세부에서 떨어져 중심 추상과 그 상호작용에 집중하면 문서가 더 천천히 낡는데,
  모델의 이 수준이 보통 더 안정적이기 때문이다** (15장, p.418).[^evans2003]
- 독자가 지정된다 — **팀의 비기술 구성원이 이해할 수 있게 문서를 쓰라. 모두가 알아야 할 것을
  가르는 공유된 시야로, 그리고 모든 팀원이 모델과 코드의 탐사를 시작하는 안내서로 쓰라**
  (15장, pp.418–419).[^evans2003]

## 표시된 핵심

- 저자가 겪은 실물에서 나온 형태다 (15장, pp.419–420).[^evans2003] 대형 보험 회사 프로젝트
  첫날 그는 업계 컨소시엄에서 큰돈을 주고 산 이백 쪽짜리 "도메인 모델" 문서를 받았다. 보험
  증권의 상세 구성부터 사람들 사이 관계의 극도로 추상적인 모델까지 **온갖 클래스 다이어그램의
  뒤죽박죽**이었고 **인수분해의 품질은 고등학생 과제 수준부터 꽤 좋은 것까지 걸쳐 있었다.**
  문제는 하나였다 — **그런데 어디서 시작하는가. 이백 쪽이다.**
- 그 프로젝트의 문화는 추상 프레임워크 짓기를 크게 선호했고 선임자들은 사람과 사람, 사람과
  사물, 사람과 활동·합의의 관계에 대한 아주 추상적인 모델에 집중해 있었다. **관계에 대한 좋은
  분석이었고 그들의 모델 실험은 학술 연구 프로젝트의 성질을 띠었지만 보험 애플리케이션 근처에
  우리를 데려다주지 못하고 있었다** (15장, p.419).[^evans2003]
- **저자의 첫 본능이 기각되는 대목이 이 사례의 값이다** — **내 첫 본능은 베어 내기 시작해서
  물러설 작은 핵심 도메인을 찾고 그것을 리팩터링하면서 다른 복잡성을 다시 들이는 것이었다.
  그러나 경영진은 이 태도에 경계했다. 그 문서는 큰 권위를 부여받고 있었다** (15장,
  p.419).[^evans2003] 업계 전문가들이 참여해 만들었고 **어쨌든 그들은 저자에게 지불하는 것보다
  훨씬 많은 돈을 컨소시엄에 지불했으므로 급진적 변경 권고를 무겁게 받아들일 리 없었다.**
- 그래서 문서를 고치지 않고 표시만 했다. 일반 보험 업계와 지을 애플리케이션의 요구사항을 잘
  아는 업무 분석가의 도움을 받아 **우리가 작업해야 할 본질적이고 차별화하는 개념을 제시하는
  몇 안 되는 절들을 식별했고, 핵심과 그것의 보조 기능과의 관계를 분명히 보이는 모델 항해법을
  제공했다** (15장, p.419).[^evans2003] 그 관점에서 새 프로토타입이 시작되어 **요구 기능 일부를
  보이는 단순화된 애플리케이션이 빠르게 나왔다.**
- 그 결과가 한 줄로 요약된다 (15장, p.420):[^evans2003]

> Two pounds of recyclable paper was turned into a business asset by a few page tabs and some
> yellow highlighter.

- **기법이 종이에 한정되지 않는다** — UML 도해를 많이 쓰는 팀은 **"스테레오타입"으로 핵심
  요소를 식별할 수 있고**, 코드를 모델의 유일한 저장소로 쓰는 팀은 **주석을, 어쩌면 자바독으로
  구조화된 주석을 쓰거나 개발 환경의 어떤 도구를 쓸 수 있다.** 판정은 하나다 — **특정 기법은
  중요하지 않고, 개발자가 무엇이 핵심 도메인 안에 있고 무엇이 밖에 있는지를 힘들이지 않고 볼
  수만 있으면 된다** (15장, p.420).[^evans2003]
- 처방 문단 (15장, p.420):[^evans2003]

> Flag each element of the CORE DOMAIN within the primary repository of the model, without
> particularly trying to elucidate its role. Make it effortless for a developer to know what is
> in or out of the CORE.

- 얻는 것과 그 조건 — **핵심 도메인이 모델을 다루는 사람들에게 명확히 보이게 되며, 꽤 작은
  노력과 낮은 유지 비용으로 그렇게 된다. 적어도 모델이 부분들의 기여를 구별할 만큼 충분히 잘게
  인수분해되어 있는 한에서는 그렇다** (15장, p.420).[^evans2003]

## 증류 문서를 절차의 계기로 쓰기

- 이 절은 문서를 읽을거리가 아니라 계기로 바꾼다 (15장, pp.420–421).[^evans2003] 출발점은
  익스트림 프로그래밍의 코드 소유 규칙이다 — **이론상 어떤 쌍이든 시스템의 어떤 코드든 바꿀 수
  있다. 실제로는 어떤 변경은 큰 함의를 가져 더 많은 상의와 조율을 부른다. 인프라 층에서 일할
  때는 변경의 영향이 분명할 수 있지만 전형적으로 조직된 도메인 층에서는 그렇게 분명하지 않을 수
  있다.**
- 핵심 도메인 개념이 그 영향을 분명하게 만든다 — **핵심 도메인 모델에 대한 변경은 큰 효과를
  가져야 한다. 널리 쓰이는 일반 요소에 대한 변경은 많은 코드 갱신을 요구할 수 있지만 그래도
  핵심 변경이 만드는 개념적 이동을 만들지는 않는다** (15장, p.420).[^evans2003]
- **그래서 규칙이 문서를 기준으로 정해진다** (15장, p.421):[^evans2003]

> If the distillation document outlines the essentials of the CORE DOMAIN, then it serves as a
> practical indicator of the significance of a model change. When a model or code change affects
> the distillation document, it requires consultation with other team members. When the change
> is made, it requires immediate notification of all team members, and the dissemination of a
> new version of the document.

- 무엇이 그 계기에 걸리는지도 적힌다 — 개발자가 증류 문서 자체가 자기 코드나 모델 변경에 맞춰
  바뀌어야 함을 깨달을 때 상의가 필요하고, 그것은 **핵심 도메인의 요소나 관계를 근본적으로
  바꾸고 있거나 무언가를 더 넣거나 빼면서 핵심의 경계를 바꾸고 있다**는 뜻이다 (15장,
  p.420).[^evans2003]
- **그리고 반대쪽이 명시되면서 규칙이 자유를 보존한다** — **핵심 밖의 변경이나 증류 문서에
  포함되지 않은 세부에 대한 변경은 상의나 통지 없이 통합될 수 있고 다른 구성원들이 자기 작업
  중에 마주치게 된다. 그러면 개발자들은 익스트림 프로그래밍이 제안하는 완전한 자율을 갖는다**
  (15장, p.421).[^evans2003]

## 인계에서 이 문서가 한 일

책의 결론이 이 패턴의 쓰임 하나를 사례로 기록한다. 위 절들이 **같은 팀 안에서** 초점을 맞추는
용도를 다뤘다면, 여기서는 **팀이 통째로 바뀌는 자리**에서 이 문서가 무엇을 했는가다.

- 상황 — 저자와 다른 개발자 한 사람이 만든 유틸리티가 인계되었고, **처음 개발한 모두의 관여가
  그것으로 끝났다.** 전환이 급격했기에 저자는 조합 가능한 요소를 떠받치던 설계 특징이 혼란을
  주고 더 흔한 분기 로직으로 대체될 것이라 예상했다 (결론, pp.501–502).[^evans2003]
- 그런데 그렇게 되지 않았고, 저자가 드는 이유가 인계물의 구성이다 (결론,
  p.502):[^evans2003]

> When we handed off, the package included a thorough test suite and a distillation document.
> The new team members used that document to guide their explorations, and as they looked into
> things, they became excited by the possibilities the design presented.

- 결과가 언어로 나타난다 — 1년 뒤 저자는 **유비쿼터스 언어가 다른 팀으로 옮겨붙어 살아남았고
  계속 진화하고 있다**는 것을 알아차린다 (결론, p.502).[^evans2003]
  - **이 기록이 위 [증류 문서](#증류-문서)의 용도를 하나 늘린다.** 그 절은 이 문서를 팀의 초점을
    맞추고 변경의 중대성을 재는 도구로 두는데, 여기서는 **설계를 만든 사람이 아무도 남지 않은
    상태에서 설계의 의도를 전달한 유일한 안내물**이 된다.
  - 함께 인계된 것이 **철저한 테스트 모음**이라는 점도 같은 문장에 있다. 문서가 무엇을 의도했는지
    말하고 테스트가 무엇이 참인지 말하는 분담이다. #hypothesis 저자가 둘의 분담을 이 자리에서
    명시하지는 않는다 — 한 문장에 나란히 들었을 뿐이다.
- **이 문서가 설계를 얼리지는 않았다.** 다시 1년 뒤 그 팀은 상속받은 설계 안에서 새 요구를
  해결할 길을 찾지 못해 설계를 알아보기 어려울 만큼 바꿨고, 저자는 그것을 실패가 아니라 더 깊은
  모델로의 돌파로 읽는다 (결론, p.502).[^evans2003] 그 판정의 전문은
  [깊은 모델과 돌파](../concepts/deep-model.md)에 있다.

## 이어지는 페이지

- [핵심 도메인](../concepts/core-domain.md) — 이 문서들이 가리키는 대상
- [일반 하위 도메인](generic-subdomains.md) — 모델을 실제로 바꾸는 첫 기법
- [격리된 핵심](segregated-core.md) — 같은 표시를 코드 구조로 하는 자리
- [깊은 모델과 돌파](../concepts/deep-model.md) — 인계받은 팀이 그 설계를 바꾼 것을 어떻게 읽는가
- [경계 컨텍스트](../concepts/bounded-context.md) — 이 문서가 가로지르는 경계
- [유비쿼터스 언어](ubiquitous-language.md) — 이 문서가 쓰이는 말
- [유비쿼터스 언어](ubiquitous-language.md) —
  같은 원전이 문서 일반에 붙이는 조건
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 15장 "Distillation" §"An Escalation of Distillations"의 맺음
    (p.414) · §DOMAIN VISION STATEMENT(pp.415–416) · §HIGHLIGHTED CORE(pp.417–421) —
    §"The Distillation Document"(pp.418–419) · §"The Flagged CORE"(pp.419–420) ·
    §"The Distillation Document as Process Tool"(pp.420–421) 포함 ·
    결론 "Conclusion" §Epilogues(pp.501–502). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 패턴 도비라의 사진(pp.415·417)은 도판이라 옮기지 않았다. 비전 선언 대조표
    (p.416)는 원문에서도 표이고 표의 내용이 이 패턴의 교육 내용이라 표로 옮겼으며, 굵은
    글씨는 원문 문장의 직인용을 한국어로 옮긴 것이다. 이 절들에는 코드 목록이 없다.
