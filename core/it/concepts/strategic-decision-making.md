---
type: concept
title: 전략 설계 결정하기
description: 전략 설계를 누가 어떤 과정으로 정하는가 — 위에서 내려오는 아키텍처가 대개 잘 통하지 않는다는 판정, 실제로 값을 낸 두 방식인 애플리케이션 개발에서 창발하는 구조와 상아탑이 아닌 고객 중심 아키텍처 팀, 의사 결정에 필요한 여섯 가지(결정이 팀 전체에 닿을 것·과정이 피드백을 흡수할 것·계획이 진화를 허용할 것·아키텍처 팀이 최고 인재를 빨아들이지 말 것·최소주의와 겸손·객체는 전문가이되 개발자는 제너럴리스트), 같은 편향이 기술 프레임워크에도 적용된다는 확장과 "바보를 위한 프레임워크를 쓰지 마라"는 금지, 그리고 마스터 플랜이 전체주의적 질서를 만들어 실패한다는 크리스토퍼 알렉산더의 진단과 점진적 성장을 위한 원칙 집합이라는 대안, 그리고 같은 경고를 19년 뒤에 다른 근거로 적는 소스 — 가장 적은 정보로 결정이 내려지고 투자가 매몰 비용과 비합리적 산출물 애착으로 굳는다는 기제와 지평을 짧게 자르라는 처방 셋
generated: { by: "claude-opus-5", at: "2026-09-14T21:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: ford2022-evolutionary, resource: /it/sources/ford2022-evolutionary.md }
---

# 전략 설계 결정하기

- [전통적 배치는 대개 잘 통하지 않는다](#전통적-배치는-대개-잘-통하지-않는다)
- [값을 낸 방식 하나 — 애플리케이션 개발에서 창발하는 구조](#값을-낸-방식-하나--애플리케이션-개발에서-창발하는-구조)
- [값을 낸 방식 둘 — 고객 중심 아키텍처 팀](#값을-낸-방식-둘--고객-중심-아키텍처-팀)
- [여섯 가지 필수](#여섯-가지-필수)
- [기술 프레임워크에도 같은 것이 적용된다](#기술-프레임워크에도-같은-것이-적용된다)
- [마스터 플랜을 경계하라](#마스터-플랜을-경계하라)
- [같은 경고를 2022년에 다른 근거로 적는 소스](#같은-경고를-2022년에-다른-근거로-적는-소스)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프로젝트 전체에 걸리는 설계 결정을 누가, 어떤 과정으로 내리는가.**

## 전통적 배치는 대개 잘 통하지 않는다

- 이 절의 첫 문장이 통념을 서술하고 곧바로 기각한다 (17장, p.490):[^evans2003]

> Traditionally, architecture is handed down, created before application development begins, by
> a team that has more power in the organization than the application development team. But it
> doesn't have to be that way. That way doesn't usually work very well.

  - **기각의 근거가 권한의 부당함이 아니라 성적이다.** "그럴 필요가 없다"와 "대개 잘 통하지
    않는다"는 두 문장이고, 뒤엣것이 이 절 전체의 논거가 된다.
- 그러면서 저자가 조직 형태 자체를 처방하지는 않는다 — **전략 설계는 정의상 프로젝트 전체에
  걸쳐 적용되어야 한다. 프로젝트를 조직하는 방법은 많고 나는 너무 규범적이고 싶지 않다. 그러나
  어떤 의사 결정 과정이든 효과적이려면 몇 가지 기본이 요구된다** (17장, p.490).[^evans2003]
  - **이 문장이 이 절의 구성을 정한다.** 조직 형태는 예시 둘로만 들고, 조문은 형태가 아니라
    아래 [여섯 가지 필수](#여섯-가지-필수)에 둔다. 형태가 달라도 여섯은 같아야 한다는 뜻이다.
- 예시 둘을 드는 범위도 저자가 제한한다 — **먼저 실무에서 얼마간 값을 내는 것을 본 두 가지
  방식을 빠르게 훑어보자(따라서 옛 "높은 곳에서 오는 지혜" 방식은 무시한다)** (17장,
  p.491).[^evans2003]

## 값을 낸 방식 하나 — 애플리케이션 개발에서 창발하는 구조

- 규정 (17장, p.491):[^evans2003]

> A self-disciplined team made up of very good communicators can operate without central
> authority and follow EVOLVING ORDER to arrive at a shared set of principles, so that order
> grows organically, not by fiat.

  - [질서의 진화](../concepts/evolving-order.md)가 여기서 **조직의 작동 방식**으로 쓰인다. 16장에서 그
    패턴은 구조를 미리 굳히지 말라는 설계 조항이었는데, 이 장은 그것을 중앙 권위 없이 굴러가는
    팀의 절차로 읽는다.
- 전형으로 드는 것이 XP 팀이다 — **이것이 익스트림 프로그래밍(Extreme Programming) 팀의 전형적인
  모델이다. 이론상 구조는 어느 프로그래밍 짝의 통찰에서 완전히 자발적으로 떠오를 수도 있다**
  (17장, p.491).[^evans2003]
- 그러나 실제로는 보완이 붙는다 — **더 흔하게는 대규모 구조에 대해 얼마간의 감독 책임을 가진
  개인이나 팀의 부분집합을 두는 것이 구조를 통일된 채로 유지하는 데 도움이 된다. 이 접근은
  그런 비공식 리더가 **직접 코드를 만지는 개발자**, 곧 중재자이자 소통자이며 아이디어의 유일한
  출처가 아닐 때 특히 잘 통한다** (17장, p.491).[^evans2003]
- 그리고 그 리더의 소속에 조건이 걸린다 — **이 자연스러운 리더가 누구든 그 사람은 여전히 개발
  팀의 구성원이다. 따라서 개발 팀에는 프로젝트 전체에 영향을 줄 설계 결정을 내릴 만한 역량의
  사람이 적어도 몇 명은 있어야 한다** (17장, p.491).[^evans2003]
  - **조직 형태가 팀 구성에 요구를 되돌려 건다.** 아래 넷째 필수(아키텍처 팀이 최고 인재를
    빨아들이지 말 것)와 같은 요구의 앞면이다.
- 구조가 여러 팀에 걸칠 때는 비공식 위원회가 된다 — **각 애플리케이션 팀이 여전히 대규모 구조의
  착상으로 이어지는 발견을 하되, 특정 선택지는 여러 팀의 대표로 이뤄진 비공식 위원회가 논의한다.
  설계의 영향을 평가한 뒤 참가자들은 그것을 채택하거나 수정하거나 보류할 수 있다** (17장,
  p.491).[^evans2003]
- 그 느슨한 연합이 성립하는 조건이 넷으로 명시된다 — **이 배치는 팀이 비교적 적을 때, 모두가
  서로 조율하는 데 헌신할 때, 설계 역량이 비슷할 때, 그리고 구조적 필요가 하나의 대규모 구조로
  충족될 만큼 비슷할 때 통할 수 있다** (17장, p.491).[^evans2003]
  - **네 조건 중 셋이 팀 사이의 대칭성을 요구한다.** 역량이 갈리거나 필요가 다르면 이 방식은
    성립하지 않고, 그때 두 번째 방식이 나온다.

## 값을 낸 방식 둘 — 고객 중심 아키텍처 팀

- 문제 설정 — **전략이 여러 팀에 공유될 때는 의사 결정의 얼마간의 중앙화가 매력적으로 보이기는
  한다** (17장, p.492).[^evans2003] 그러나 중앙화가 곧 상아탑을 뜻하지는 않는다 (17장,
  p.492):[^evans2003]

> The failed model of the ivory tower architect is not the only possibility. An architecture
> team can act as a peer with various application teams, helping to coordinate and harmonize
> their large-scale structures as well as BOUNDED CONTEXT boundaries and other cross-team
> technical issues. To be useful in this, they must have a mind set that emphasizes application
> development.

  - **핵심 낱말이 "peer"다.** 위가 아니라 옆이고, 조율하는 대상이 구조와 경계와 팀 사이의 기술
    쟁점이다. 경계를 조화시키는 일은 [컨텍스트 지도](../concepts/context-map.md)가 팀 조직의
    윤곽을 따라 생긴다고 적은 관찰과 같은 자리에서 벌어진다.
- 그리고 조직도로는 구별되지 않는다는 것이 이 방식의 판정이다 (17장, p.492):[^evans2003]

> On an organization chart, this team may look just like the traditional architecture team, but
> it is actually different in every activity.

  - 무엇이 다른지가 활동으로 열거된다 — **팀 구성원은 개발과 진정한 협업자이고, 개발자와 함께
    패턴을 발견하고, 여러 팀과 실험해 증류에 이르고, 손을 더럽힌다** (17장, p.492).[^evans2003]
  - **이 문장이 이 페이지에서 가장 실무적인 판별 기준이다.** 이름과 편제로는 두 모델이 같아
    보이므로, 무엇을 하는지로만 갈린다.

## 여섯 가지 필수

저자가 위 두 방식을 관통하는 조건을 여섯으로 든다. 각 항의 제목이 원문에서 기울임으로 조판된
처방문이다 (17장, pp.492–495).[^evans2003]

**하나.**

> Decisions must reach the entire team.

- 근거 — **당연하게도, 모두가 전략을 알고 따르지 않으면 전략은 무의미하다** (17장,
  p.492).[^evans2003] 그런데 그 요구가 낳는 반응이 함정이다 — **이 요구가 사람들을 공식
  "권한"을 가진 중앙 아키텍처 팀 중심으로 조직하게 만든다. 같은 규칙이 어디서나 적용되도록
  말이다** (17장, p.492).[^evans2003]
- 그 반응의 결과가 아이러니로 적힌다 — **아이러니하게도 상아탑 아키텍트는 흔히 무시되거나
  우회된다. 아키텍트가 자기 규칙을 실제 애플리케이션에 적용해 보는 실무적 시도에서 오는 피드백을
  갖지 못한 탓에 실용적이지 않은 설계가 나오면, 개발자에게는 선택의 여지가 없다** (17장,
  p.492).[^evans2003]
- 반대 방향의 관찰 — **소통이 아주 좋은 프로젝트에서는 애플리케이션 팀에서 떠오른 전략 설계가
  오히려 모두에게 더 효과적으로 닿을 수 있다. 그 전략은 적실할 것이고, 지적인 공동체 결정에
  붙는 권위를 가질 것이다** (17장, p.492).[^evans2003]
- 판정 (17장, p.492):[^evans2003]

> Whatever the system, be less concerned with the authority bestowed by management than with the
> actual relationship the developers have with the strategy.

**둘.**

> The decision process must absorb feedback.

- 근거는 지식의 소재다 — **조직 원리나 대규모 구조나 그 정도로 미묘한 증류를 만드는 일은
  프로젝트의 필요와 도메인의 개념에 대한 정말 깊은 이해를 요구한다** (17장,
  p.493).[^evans2003] 그리고 (17장, p.493):[^evans2003]

> The only people who have that depth of knowledge are the members of the application
> development team. This explains why application architectures created by architecture teams
> are so seldom helpful, despite the undeniable talent of many of the architects.

  - **"재능이 없어서가 아니다"가 이 항의 핵심이다.** 실패의 원인을 사람의 질이 아니라 지식의
    소재에 둔다. [지식 정련](../concepts/knowledge-crunching.md)이 모델의 출처를 도메인 전문가와 개발자의
    반복 대화에 두는 것과 같은 논리를 한 층 위로 올린 것이다.
- 전략 설계가 다른 일과 구별되는 점도 여기서 나온다 — **기술 기반 구조나 아키텍처와 달리 전략
  설계는 그 자체로 코드를 많이 쓰는 일을 포함하지 않는다. 다만 모든 개발에 영향을 준다. 그것이
  요구하는 것은 애플리케이션 개발 팀과의 관여다** (17장, p.493).[^evans2003]
- 실물 장치 하나가 기록된다 — **내가 함께 일한 어느 기술 아키텍처 팀은 자기 구성원을 그 팀의
  프레임워크를 쓰려는 여러 애플리케이션 개발 팀으로 실제로 순환시켰다. 이 순환은 개발자가 마주한
  도전의 실무 경험을 아키텍처 팀으로 끌어들이는 동시에 프레임워크의 미묘함을 적용하는 법에 대한
  지식을 옮겼다. 전략 설계도 이와 똑같이 빡빡한 피드백 고리를 필요로 한다** (17장,
  p.493).[^evans2003]

**셋.**

> The plan must allow for evolution.

- 근거 — **효과적인 소프트웨어 개발은 매우 동적인 과정이다. 최상위 결정이 돌에 새겨지면 팀은
  변화에 대응해야 할 때 선택지가 줄어든다** (17장, p.493).[^evans2003] 그 함정을 피하는 것이
  [질서의 진화](../concepts/evolving-order.md)다 — **깊어지는 통찰에 응답해 대규모 구조를 계속 바꾸는 것을
  강조함으로써 이 덫을 피한다** (17장, p.493).[^evans2003]
- 그리고 권한의 양이 조건으로 붙는다 — **조화를 만드는 원리가 값질 수는 있지만, 그것은 개발
  프로젝트의 계속되는 삶과 함께 자라고 바뀌어야 하며, 가뜩이나 힘든 일을 하는 애플리케이션
  개발자에게서 너무 많은 권한을 앗아 가서는 안 된다** (17장, p.493).[^evans2003]

**넷.**

> Architecture teams must not siphon off all the best and brightest.

- 힘의 방향이 양쪽에서 온다고 적는다 — **관리자는 가장 기술적으로 재능 있는 개발자를 아키텍처
  팀과 기반 구조 팀으로 옮기는 경향이 있다. 그 앞선 설계자들의 기술을 지렛대로 쓰고 싶어서다.
  개발자 쪽에서도 더 넓은 영향을 미칠 기회나 "더 흥미로운" 문제를 다룰 기회에 끌린다. 그리고
  엘리트 팀의 일원이라는 위신이 붙는다** (17장, p.494).[^evans2003]
- 결과 — **이 힘들은 흔히 실제로 애플리케이션을 만드는 자리에 기술적으로 가장 덜 세련된
  개발자만 남긴다. 그런데 좋은 애플리케이션을 만드는 데는 설계 기술이 든다. 이것은 실패로
  가는 배치다. 전략 팀이 훌륭한 전략 설계를 만들어 내더라도 애플리케이션 팀에 그것을 따를 설계
  세련도가 없을 것이다** (17장, p.494).[^evans2003]
- 반대 방향의 손실도 계상된다 — **역으로 그런 팀은 설계 기술은 약할지 몰라도 도메인 경험이 가장
  풍부한 개발자를 거의 포함하지 않는다. 전략 설계는 순수하게 기술적인 과업이 아니다. 깊은 도메인
  지식을 가진 개발자로부터 스스로를 끊어 놓는 것은 아키텍트의 노력을 더욱 절름거리게 한다**
  (17장, p.494).[^evans2003]
- 처방 (17장, p.494):[^evans2003]

> It is essential to have strong designers on all application teams. It is essential to have
> domain knowledge on any team attempting strategic design.

  - 수단은 열어 둔다 — **단순히 더 앞선 설계자를 채용해야 할 수도 있다. 아키텍처 팀을 시간제로
    두는 것이 도움이 될 수도 있다. 통하는 방법은 많을 것이라 확신하지만, 효과적인 전략 팀은
    모두 효과적인 애플리케이션 팀을 짝으로 두어야 한다** (17장, p.494).[^evans2003]
  - 이 항은 [핵심 도메인](../concepts/core-domain.md)의 진단과 같은 관찰을 조직 쪽에서 반복한다 — 그 페이지
    역시 뛰어난 개발자가 기술 인프라로 쏠리고 사업을 가르는 부분이 덜 숙련된 손에 남는다고 적는다.

**다섯.**

> Strategic design requires minimalism and humility.

- 근거 — **증류와 최소주의는 어떤 좋은 설계 작업에도 본질적이지만, 최소주의는 전략 설계에서
  더욱 결정적이다. 아주 약간만 맞지 않아도 앞길을 막을 무서운 잠재력이 있다** (17장,
  p.494).[^evans2003] 16장의 "맞지 않는 구조는 없는 것보다 나쁘다"가 조직 쪽에서 되풀이된다
  ([대규모 구조](../concepts/large-scale-structure.md)).
- 분리된 아키텍처 팀에 특히 위험한 이유가 둘 적힌다 — **분리된 아키텍처 팀은 애플리케이션 팀
  앞에 자기가 놓고 있을지 모르는 장애물에 대한 감이 덜하므로 특히 조심해야 한다. 동시에 자기
  주된 책임에 대한 아키텍트의 열의는 그들이 도를 넘기 쉽게 만든다** (17장, p.494).[^evans2003]
  저자 자신도 그 일을 했다고 적는다 — **나는 이 현상을 여러 번 보았고 나 자신도 해 봤다. 좋은
  생각 하나가 다른 생각으로 이어지고, 결국 역효과를 내는 과잉 구축된 아키텍처에 이른다** (17장,
  p.494).[^evans2003]
- 처방과 그 이유 — **대신 우리는 설계의 명료함을 유의미하게 개선하지 않는 것은 아무것도 담지
  않도록 깎아 낸 조직 원리와 핵심 모델을 만들도록 스스로를 단련해야 한다. 진실은 거의 모든
  것이 무언가의 앞을 막는다는 것이고, 그러니 각 요소는 그럴 값을 하는 편이 낫다. 당신의 가장
  좋은 생각이 누군가의 앞을 막을 법하다는 것을 깨닫는 데는 겸손이 든다** (17장,
  p.495).[^evans2003]

**여섯.**

> Objects are specialists; developers are generalists.

- 대조가 이 항의 전부다 — **좋은 객체 설계의 본질은 각 객체에 분명하고 좁은 책임을 주고 상호
  의존을 절대적 최소로 줄이는 것이다. 때때로 우리는 팀 위의 상호작용도 소프트웨어에서 그래야
  하는 만큼 가지런하게 만들려 한다** (17장, p.495).[^evans2003]
- 그러나 좋은 프로젝트는 그렇지 않다고 적는다 (17장, p.495):[^evans2003]

> A good project has lots of people sticking their nose in other people's business. Developers
> play with frameworks. Architects write application code. Everyone talks to everyone. It is
> efficiently chaotic. Make the objects into specialists; let the developers be generalists.

  - **"효율적으로 혼돈스럽다"(efficiently chaotic)가 이 항의 이름표다.** 모듈 설계의 잣대를
    조직에 그대로 옮기는 것을 이 항이 금지한다.
- 그리고 저자가 자기 책의 구분에 단서를 단다 — **내가 전략 설계와 다른 종류의 설계를 구분한 것은
  관련된 과업을 명확히 하기 위해서이므로, 두 종류의 설계 활동이 있다는 것이 두 종류의 사람이
  있다는 뜻은 아님을 지적해 두어야겠다** (17장, p.495).[^evans2003]
- 각각이 요구하는 자리가 다르다는 것이 그 근거다 — **깊은 모델에 근거한 유연한 설계를 만드는
  것은 앞선 설계 활동이지만 세부가 너무 중요해서 코드를 만지는 사람이 해야 한다. 전략 설계는
  애플리케이션 설계에서 떠오르지만, 여러 팀에 걸칠 수도 있는 활동의 큰 그림 시야를 요구한다**
  (17장, p.495).[^evans2003]
- 마지막 경고 — **사람들은 설계 전문가가 업무를 몰라도 되고 도메인 전문가가 기술을 이해하지
  않아도 되도록 과업을 잘라 낼 방법을 찾기 좋아한다. 한 개인이 배울 수 있는 양에는 한계가
  있지만, 과잉 전문화는 도메인 주도 설계에서 김을 빼 버린다** (17장, p.495).[^evans2003]

## 기술 프레임워크에도 같은 것이 적용된다

- 전제는 프레임워크의 이득이다 — **기술 프레임워크는 애플리케이션이 기본 서비스를 구현하지
  않아도 되게 하는 기반 구조 층을 제공하고 도메인을 다른 관심사로부터 격리하는 것을 도움으로써,
  도메인 층을 포함한 애플리케이션 개발을 크게 가속할 수 있다** (17장, p.495).[^evans2003]
- 그러나 위험이 붙는다 (17장, p.495):[^evans2003]

> But there is a risk that an architecture *can interfere with expressive implementations of the
> domain model and easy change.* This can happen even when the framework designers had no
> intention of venturing into the domain or application layers.

  - **의도와 무관하게 일어난다는 것이 이 문장의 무게다.** 4장이 프레임워크를 선택적으로만 쓰라고
    적은 조항의 근거가 여기서 한 줄 더 보강된다
    ([층을 잇기와 프레임워크](../concepts/relating-layers-and-frameworks.md)).
- 처방은 위 여섯을 그대로 가져온다 — **전략 설계의 하방을 제한하는 같은 편향이 기술 아키텍처에도
  도움이 될 수 있다. 진화와 최소주의와 애플리케이션 개발 팀과의 관여가, 앞길을 막지 않으면서
  애플리케이션 개발을 진짜로 돕는 서비스와 규칙의 집합을 계속 정련되게 이끌 수 있다** (17장,
  p.496).[^evans2003]
- 그 길을 따르지 않을 때의 두 결말이 적힌다 — **이 길을 따르지 않는 아키텍처는 애플리케이션
  개발의 창의성을 질식시키거나, 아키텍처가 우회되어 실용적인 목적에서 애플리케이션 개발이
  아키텍처 없이 남겨지는 것을 보게 될 것이다** (17장, p.496).[^evans2003]
  - 16장의 질서의 진화가 "구조에 맞춰 애플리케이션을 멍청하게 만들거나 아예 뒤엎는다"고 적은
    두 결말과 같은 쌍이다.
- 그리고 프레임워크를 확실히 망치는 태도 하나가 조문으로 붙는다 (17장, p.496):[^evans2003]

> Don't write frameworks for dummies.

- 근거 — **일부 개발자가 설계할 만큼 똑똑하지 않다고 가정하는 팀 분할은 애플리케이션 개발의
  어려움을 과소평가하기 때문에 실패하기 쉽다. 그 사람들이 설계할 만큼 똑똑하지 않다면 그들은
  소프트웨어 개발에 배치되지 말아야 한다. 똑똑하다면, 그들을 어르려는 시도는 그들과 그들이 필요한
  도구 사이에 장벽을 세울 뿐이다** (17장, p.496).[^evans2003]
- 그러나 캡슐화 자체가 금지되는 것은 아니다 — **무관한 기술 세부를 캡슐화하는 것은 내가 폄하하는
  종류의 사전 포장과 완전히 다르다. 프레임워크는 강력한 추상과 도구를 개발자 손에 쥐여 주고
  그들을 고역에서 풀어 줄 수 있다** (17장, p.496).[^evans2003]
- 둘을 가르는 실용적 판별법이 제시된다 (17장, p.496):[^evans2003]

> It is hard to describe the difference in a generalized way, but you can tell the difference by
> asking the framework designers what they expect of the person who will be using the
> tool/framework/components. If the designers seem to have a high level of respect for the user
> of the framework, then they are probably on the right track.

  - **판별의 대상이 산물이 아니라 설계자의 기대라는 점이 특이하다.** 코드를 읽어서는 갈리지
    않으므로 만든 사람에게 묻는다.

## 마스터 플랜을 경계하라

장의 마지막 자리에서 저자가 건축 쪽 선례를 인용한다.

- 출처와 취지 — **크리스토퍼 알렉산더(Christopher Alexander)가 이끄는 (실제 건물을 설계하는
  쪽의) 건축가 집단은 건축과 도시 계획 영역에서 점진적 성장(piecemeal growth)의 옹호자였다.
  그들은 마스터 플랜이 왜 실패하는지를 아주 잘 설명했다** (17장, pp.496–497).[^evans2003]
- 인용된 진단의 핵심 셋이다. 원전은 Alexander et al. 1975, *The Oregon Experiment*, pp.16–28
  이고 이 책은 그것을 인용한다 (17장, p.497):[^evans2003]

> . . . in practice master plans fail—because they create totalitarian order, not organic order.
> They are too rigid; they cannot easily adapt to the natural and unpredictable changes that
> inevitably arise in the life of a community.

> . . . Thus, as a source of organic order, a master plan is both too precise, and not precise
> enough. The totality is too precise: the details are not precise enough.

> . . . the existence of a master plan alienates the users [because, by definition] the members
> of the community can have little impact on the future shape of their community because most of
> the important decisions have already been made.

  - **세 진단이 서로 다른 실패 양식이다.** 첫째는 경직성이고, 둘째는 정밀도의 층위가 뒤집혔다는
    것(전체는 과하게 정밀한데 세부는 모자란다)이며, 셋째는 사람을 소외시킨다는 것이다. 셋째가
    위 첫째 필수("결정이 팀 전체에 닿아야 한다")의 뒷면이다.
  - 인용문에는 마스터 플랜을 옹호하는 대목도 함께 실려 있다 — 계획 과정이 아예 없으면 케임브리지
    대학 같은 깊고 조화로운 질서에 이를 가망이 없고, 마스터 플랜은 전체의 일관성을 주면서도
    개별 건물이 지역의 필요에 적응할 자유를 남기려는 시도라는 서술이다 (17장,
    p.497).[^evans2003] **저자가 "계획하지 말라"를 말하는 것이 아니라는 점이 이 대목으로
    분명해진다.**
- 대안이 마지막 문장에 있다 (17장, p.497):[^evans2003]

> Alexander and his colleagues advocated instead *a set of principles* for all community members
> to apply to every act of piecemeal growth, so that "organic order" emerges, well adapted to
> circumstances.

  - **이것이 16장 [질서의 진화](../concepts/evolving-order.md)의 출처 격 논거다.** 전체를 앞서 그리는 대신
    모든 구성원이 매번의 성장 행위에 적용할 원칙 집합을 둔다는 형식이 그 패턴의 형식과 같다.
  - 이 인용이 이 KB의 [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md)와
    만나는 자리는 그 페이지에 적었다.

## 같은 경고를 2022년에 다른 근거로 적는 소스

**위 §"마스터 플랜을 경계하라"와 같은 결론에 다른 길로 도착하는 소스가 있다.** 진화적 아키텍처
쪽은 그것을 **지나치게 긴 계획 지평(excessively long planning horizons)**이라는 함정으로 적는다
(8장 §"Pitfall: Excessively Long Planning Horizons", p.190).[^ford2022-evolutionary]

- **그쪽의 첫째 근거는 정보의 양이다** — 예산과 계획 절차가 가정과 이른 결정을 부르는데,
  **계획을 다시 볼 기회 없이 지평이 길수록 많은 결정이 가장 적은 정보로 내려진다** (8장,
  p.190).[^ford2022-evolutionary]
- **둘째 근거는 투자가 애착으로 굳는다는 것이다** — 이른 단계에서 개발자는 가정을 검증하려고
  조사에 상당한 노력을 쓰고, 그 시점의 "모범 사례"가 기본 가정이 된다. **가정에 노력을 더 많이
  넣을수록 그것이 여섯 달 뒤 거짓으로 드러나더라도 강하게 애착하게 된다.** 저자들이 그 기제에
  **매몰 비용 오류(sunk cost fallacy)**와 그 소프트웨어 판인 **비합리적 산출물 애착(irrational
  artifact attachment)**이라는 두 이름을 댄다 (8장, p.190).[^ford2022-evolutionary]
- **처방 셋** (8장, p.190):[^ford2022-evolutionary]
  - **아키텍트를 비가역 결정으로 몰아가는 긴 계획 주기를 경계하고 선택지를 열어 둘 길을 찾으라.**
  - **큰 작업 프로그램을 더 작고 이른 산출물로 쪼개** 아키텍처 선택과 개발 인프라 **양쪽의
    실현 가능성을 시험하라.**
  - **소프트웨어를 짓기 전에, 그리고 그 기술이 문제에 맞는지 최종 사용자 피드백으로 검증하기
    전에 상당한 선행 투자를 요구하는 기술**(예: 큰 라이선스와 지원 계약)을 따르지 마라.

### 두 경고가 겨루는가

**겨루지 않는다. 같은 결론에 서로 다른 실패 기제를 댄다.**

| | 에번스·알렉산더 (위 절) | 포드 외 (이 절) |
|---|---|---|
| 왜 실패하는가 | **구조**의 문제 — 경직되고, 전체는 과하게 정밀한데 세부는 모자라며, 사람을 소외시킨다 | **정보와 심리**의 문제 — 가장 적은 정보로 정해지고, 투자가 애착으로 굳는다 |
| 대안의 형식 | **계획을 원칙 집합으로 바꾼다**(매번의 성장 행위에 적용) | **지평을 짧게 자른다**(작고 이른 산출물, 선택지를 열어 둠) |
| 가역성을 말하는가 | 명시하지 않는다 | **명시한다** — "비가역 결정으로 몰아가는 계획 주기를 경계하라" |
| 누가 소외되는가 | 사용자와 공동체 구성원 | 이 소스는 이 축으로 적지 않는다 |

- **두 대안이 배타적이지 않고 층이 다르다.** 에번스 쪽은 **계획을 무엇으로 대체할 것인가**(원칙),
  포드 외는 **계획의 길이를 어떻게 자를 것인가**(보폭)를 답한다. 한 조직이 둘 다 할 수 있고,
  **위 §"여섯 가지 필수" 중 "계획이 진화를 허용할 것"이 두 답을 함께 받는 자리**다.
- **포드 외가 이 KB에 더하는 축 하나가 가역성이다.** 결정을 미루거나 되돌릴 수 있게 만드는 쪽의
  서술은 [되돌릴 수 있는 설계 결정](../concepts/reversible-design-decisions.md)에 있고, 긴 계획
  지평이 **가역성을 잡아먹는다**는 이 연결을 세우는 소스가 이쪽이다.
- **에번스 2003과 포드 외 2022가 19년을 사이에 두고 같은 경고를 낸다는 사실 자체가 실측이다** —
  두 소스는 서로를 인용하지 않는다. **이 KB가 대질해 세운 것이고**, 사이에 놓인 근거의 종류가
  건축 쪽 선례(1975년 *The Oregon Experiment*)에서 행동경제학 쪽 어휘(매몰 비용)로 바뀌었다.
  #hypothesis
- **같은 소스의 마지막 장이 이 경고를 예산 수립으로 옮긴다** — 엔터프라이즈 아키텍처의 전통적
  기능 여럿(예산 수립 같은)이 **소프트웨어 개발 생태계의 장기 추세를 예측할 수 있다는 능력에
  바탕을 두었는데, 동적 평형의 근본 성질이 예측 가능성을 파괴한다**는 것이다 (9장 §"CFO and
  Budgeting", p.207).[^ford2022-evolutionary] 그래서 **엔터프라이즈 아키텍트는 여전히 계획을
  세울 수 있지만 그 계획은 언제든 무효가 될 수 있다** (9장, p.225).[^ford2022-evolutionary]
  - **이것이 위 표의 "대안의 형식"에 한 줄을 더한다** — 포드 외는 지평을 자르는 것에 더해
    **계획의 지위 자체를 낮춘다**(무효가 될 수 있는 것으로 둔다). 그 자리에 그쪽이 놓는 것은
    계획이 아니라 **비용과 아키텍처 사이의 최적점을 계속 찾는 일**이고, 그 셈법은
    [아키텍처 퀀텀](../concepts/architectural-quantum.md)에 있다.
- 그쪽 장의 아홉 항목 전부와 안티패턴·함정을 가르는 정의는
  [진화적 아키텍처의 함정과 안티패턴](../concepts/evolutionary-architecture-antipatterns.md)에 있다.

## 이어지는 페이지

- [진화적 아키텍처의 함정과 안티패턴](../concepts/evolutionary-architecture-antipatterns.md) — 같은 경고를 2022년에 적는 소스와 나머지 여덟
- [되돌릴 수 있는 설계 결정](../concepts/reversible-design-decisions.md) — 긴 계획 지평이 잡아먹는 성질
- [전략 패턴을 함께 쓰기](../concepts/combining-strategic-patterns.md) — 이 장의 나머지 절반. 세 원리가
  맞물리는 방식과 평가부터 시작하라는 조항
- [전략적 설계](strategic-design.md) — 이 부의 틀. 이 층위의 결정이 팀 수준이거나 팀 사이
  협상이라는 규정
- [질서의 진화](../concepts/evolving-order.md) — 이 절이 조직의 작동 방식으로 다시 읽는 패턴
- [대규모 구조](../concepts/large-scale-structure.md) — 최소주의와 "맞지 않는 구조는 없는 것보다 나쁘다"의 원 자리
- [핵심 도메인](../concepts/core-domain.md) — 뛰어난 개발자가 기술 인프라로 쏠린다는 같은 진단의 설계 쪽 판본
- [층을 잇기와 프레임워크](../concepts/relating-layers-and-frameworks.md) — 기술 프레임워크 최소주의의 원 조항
- [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md) — 점진적 성장을 실제
  절차로 편 다른 소스
- [지식 정련](../concepts/knowledge-crunching.md) — 깊은 지식이 어디 있는가라는 둘째 필수의 근거가 오는 자리
- [실용주의 팀](../concepts/pragmatic-teams.md) — 같은 물음에 다른 소스가 답하는 자리
- [컨텍스트 지도](../concepts/context-map.md) — 아키텍처 팀이 조화시켜야 하는 경계들이 놓인 전체
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 17장 "Bringing the Strategy Together" §"Who Sets the Strategy?"
    (pp.490–492, 하위 절 "Emergent Structure from Application Development"와 "A Customer-Focused
    Architecture Team" 포함) · §"Six Essentials for Strategic Design Decision Making"
    (pp.492–495) · §"The Same Goes for the Technical Frameworks"(pp.495–496) ·
    §"Beware the Master Plan"(pp.496–497). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴
    이름을 작은 대문자로 조판하는 관례와 처방문의 기울임을 직인용에서 유지했다. 마스터 플랜 절의
    인용문은 이 책이 Alexander et al. 1975, *The Oregon Experiment*, pp.16–28에서 옮겨 실은
    것이고, 이 페이지는 그 재인용을 이 책의 쪽으로 단다 — 원전을 직접 확인하지 않았다.

[^ford2022-evolutionary]: Ford·Parsons·Kua·Sadalage 2022(2판), 8장 "Evolutionary Architecture
    Pitfalls and Antipatterns" §"Pitfall: Excessively Long Planning Horizons"(p.190). 쪽은
    인쇄판 쪽 번호(PDF 쪽 − 22, 실측). 이 절에는 직인용을 두지 않았다 — 그 절의 곁줄 조문은
    [진화적 아키텍처의 함정과 안티패턴](../concepts/evolutionary-architecture-antipatterns.md)이
    갖는다. 이 절은 이 소스가 이 페이지에 더하는 것만 든다. **두 경고를 나란히 놓는 표는 이 KB가
    두 소스를 대질해 만든 것이고 어느 소스도 상대를 인용하지 않는다.** 그 절에 도판과 코드
    목록은 없다.
