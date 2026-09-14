---
type: concept
title: 도메인 전문가
description: 업무 지식의 권위가 누구이고 소프트웨어를 만드는 사람과 어떤 관계인가에 대한 2021년 실무서의 규정 — 전문가는 요구사항을 모으는 분석가도 체계를 설계하는 엔지니어도 아니라는 경계, 요구를 내는 사람이거나 최종 사용자라는 어림법과 전문성의 범위가 사람마다 다르다는 단서, 우리가 전문가가 되는 것은 목표가 아니고 가능하지도 않으며 대신 그들의 사고 모형을 흉내 내는 것이 소프트웨어의 일이라는 판정, 가장 중요한 지식이 암묵적이라 질문으로만 접근된다는 진단과 모델을 함께 만들게 되는 일이 흔하며 그것이 핵심 하위 도메인에서 특히 잦다는 관찰, 그리고 원전이 같은 역할에 대해 말하는 것
generated: { by: "claude-opus-5", at: "2026-09-14T18:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 도메인 전문가

- [누구를 가리키는 낱말인가](#누구를-가리키는-낱말인가)
- [분석가도 엔지니어도 아니다](#분석가도-엔지니어도-아니다)
- [전문성의 범위는 사람마다 다르다](#전문성의-범위는-사람마다-다르다)
- [우리가 전문가가 되는 것이 목표가 아니다](#우리가-전문가가-되는-것이-목표가-아니다)
- [지식은 암묵적이고 때로는 함께 만들어진다](#지식은-암묵적이고-때로는-함께-만들어진다)
- [원전이 같은 역할에 대해 말하는 것](#원전이-같은-역할에-대해-말하는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 지식의 권위는 누구이고, 소프트웨어를 만드는 사람은 그와 어떤 관계에
서는가.**

## 누구를 가리키는 낱말인가

- 규정 (1장, p.17):[^khononov2021]

> Domain experts are subject matter experts who know all the intricacies of the business that
> we are going to model and implement in code. In other words, domain experts are knowledge
> authorities in the software's business domain.

- **어림법이 하나 딸린다** — **경험칙으로 도메인 전문가(domain expert)는 요구사항을 내놓는
  사람이거나 소프트웨어의 최종 사용자다. 소프트웨어는 그들의 문제를 푸는 것이 목적이다**
  (1장, p.17).[^khononov2021]
  - **어림법의 잣대가 직함이 아니라 관계라는 점이 요지다.** 누가 문제를 갖고 있고 누가 그 해법을
    쓰는가로 정해지므로, 조직도에서 같은 자리에 있는 사람이라도 프로젝트마다 이 역할에 들거나
    들지 않는다.

## 분석가도 엔지니어도 아니다

- 경계가 부정형으로 그어진다 (1장, p.17):[^khononov2021]

> The domain experts are neither the analysts gathering the requirements nor the engineers
> designing the system. Domain experts represent the business. They are the people who
> identified the business problem in the first place and from whom all business knowledge
> originates.

- 그러면 분석가와 엔지니어는 무엇을 하는가 — **시스템 분석가와 엔지니어는 업무 도메인에 대한
  그들의 사고 모형을 소프트웨어 요구사항과 소스 코드로 변환하고 있다** (1장,
  p.17).[^khononov2021]
  - **"그들의"가 이 문장의 무게를 진다.** 변환의 원본이 분석가의 이해가 아니라 전문가의 사고
    모형이라는 뜻이고, 그래서 변환 단계가 늘어날수록 손실이 쌓인다. 그 손실의 계산은
    [모델 주도 설계](../concepts/model-driven-design.md)와 [지식 정련](../concepts/knowledge-crunching.md)에
    있다.
- 같은 장이 그 손실을 한 문장으로 세운다. 2장의 제사로 알베르토 브란돌리니(Alberto Brandolini)의
  말이 실린다 (2장 장 도입, p.21):[^khononov2021]

> It's developers' (mis)understanding, not domain experts' knowledge, that gets released in
> production.

## 전문성의 범위는 사람마다 다르다

- **한 사람이 전부를 아는 것이 전제가 아니다** — **도메인 전문가의 전문성은 범위가 다를 수
  있다. 어떤 주제 전문가는 업무 도메인 전체가 어떻게 돌아가는지 상세히 이해하고, 어떤 사람은
  특정 하위 도메인을 전문으로 한다** (1장, p.17).[^khononov2021]
- 실물 — 온라인 광고 대행사라면 도메인 전문가는 **캠페인 관리자, 미디어 바이어, 분석가, 그
  밖의 업무 이해관계자**다 (1장, p.17).[^khononov2021]
- 장을 닫으며 다시 규정된다 — **도메인 전문가는 업무의 주제 전문가다. 그들은 회사의 비즈니스
  도메인 또는 그 하위 도메인 하나 이상에 대한 깊이 있는 지식을 갖고 있으며 프로젝트의 성공에
  결정적이다** (1장, p.18).[^khononov2021] 하위 도메인의 경계는
  [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md)에 있다.

## 우리가 전문가가 되는 것이 목표가 아니다

2장이 이 역할과 개발자의 관계를 정한다.

- 전제 — **효과적인 소프트웨어 해법을 설계하려면 업무 도메인의 기본 지식은 적어도 파악해야
  한다. 1장에서 논의했듯 이 지식은 도메인 전문가의 것이다. 업무 도메인의 모든 속사정을
  전문으로 하고 이해하는 것이 그들의 일이다** (2장, p.22).[^khononov2021]
- **그리고 선이 그어진다** (2장, p.22):[^khononov2021]

> By no means should we, nor can we, become domain experts. That said, it's crucial for us to
> understand domain experts and to use the same business terminology they use.

- 소프트웨어가 할 일이 그 자리에서 규정된다 — **효과적이려면 소프트웨어는 도메인 전문가가 문제에
  대해 생각하는 방식, 즉 그들의 사고 모형(mental models)을 흉내 내야 한다** (2장,
  p.22).[^khononov2021]
- **그렇게 하지 않으면 무엇이 남는지가 계상된다** — **업무 문제와 요구사항 뒤의 근거를 이해하지
  못하면 우리의 해법은 업무 요구사항을 소스 코드로 "번역"하는 데 그친다. 요구사항이 결정적인
  경계 사례를 빠뜨렸다면? 또는 업무 개념 하나를 서술하지 못해 미래 요구사항을 뒷받침할 모델을
  구현할 능력이 제한된다면?** (2장, p.22).[^khononov2021]
- 그리고 이 관계에 붙는 규정 하나 — 브란돌리니를 다시 인용해 **소프트웨어 개발은 학습 과정이고
  동작하는 코드는 부수 효과다.** 그래서 **소프트웨어 프로젝트의 성공은 도메인 전문가와 소프트웨어
  엔지니어 사이 지식 공유의 효과에 달렸다. 우리는 문제를 풀려면 그 문제를 이해해야 한다**
  (2장, p.22).[^khononov2021]

## 지식은 암묵적이고 때로는 함께 만들어진다

2장의 마지막 절이 이 역할에 접근하는 일의 실제 난이도를 적는다.

- **경로가 하나뿐이다** — **도메인 지식을 모으는 유일하게 믿을 만한 방법은 도메인 전문가와
  대화하는 것이다. 꽤 자주 가장 중요한 지식은 암묵적이다(tacit). 그것은 문서화되거나 성문화되어
  있지 않고 도메인 전문가의 머릿속에만 있다. 거기 닿는 유일한 방법은 질문하는 것이다** (2장,
  p.30).[^khononov2021]
- **그리고 발견이 아니라 공동 창작이 되는 일이 흔하다** (2장, p.30):[^khononov2021]

> As you gain experience in this practice, you will notice that frequently, this process
> involves not merely discovering knowledge that is already there, but rather co-creating the
> model in tandem with domain experts.

  - 근거는 전문가 쪽에도 빈틈이 있다는 것이다 — **도메인 전문가 자신의 업무 도메인 이해에도
    모호함과 심지어 백지가 있을 수 있다. 예를 들어 "행복한 경로" 시나리오만 정의하고 받아들여진
    가정에 도전하는 경계 사례는 고려하지 않는 식이다. 나아가 명시적 정의가 없는 업무 도메인
    개념을 마주칠 수도 있다** (2장, p.30).[^khononov2021]
  - **질문이 그 빈틈을 드러내는 장치가 된다** — **업무 도메인의 본질에 대해 질문하는 것이 흔히
    그런 암묵적 충돌과 백지를 명시적으로 만든다. 이것은 핵심 하위 도메인에서 특히 흔하다. 그런
    경우 학습 과정은 상호적이다. 당신은 도메인 전문가가 자기 분야를 더 잘 이해하도록 돕고 있는
    것이다** (2장, p.30).[^khononov2021]
  - **"핵심 하위 도메인에서 특히 흔하다"가 이 절을 분류와 잇는다.** 정의되지 않은 개념이 많은
    곳이 곧 회사가 남들과 다르게 하는 곳이라는 뜻이고, 그 판별은
    [하위 도메인의 세 종류](subdomain-types.md)에 있다.
- 이 대화가 무엇을 향해 가는지는 [유비쿼터스 언어](../concepts/ubiquitous-language.md)에 있다.

## 원전이 같은 역할에 대해 말하는 것

[evans2003](../sources/evans2003.md)은 이 역할을 따로 규정하는 절을 두지 않고 **활동 안에서**
다룬다. 두 소스가 겹치는 자리와 서로 다른 자리를 적어 둔다.

- **협업의 형태가 원전에 있다** — **지식 정련은 혼자 하는 활동이 아니다. 개발자와 도메인
  전문가로 이루어진 팀이 협업하며, 보통 개발자가 이끈다** (1장, p.14).[^evans2003]
  - **"보통 개발자가 이끈다"가 이 2021년 판본에 없는 문장이다.** 이 책은 누가 이끄는가를 말하지
    않고 **누가 권위인가**를 말한다. 두 서술은 겨루지 않는다 — 지식의 출처와 대화의 진행자는
    다른 물음이다.
- **모델이 이해되지 않을 때 누구를 의심하는가에서 원전이 더 강하게 나간다** (2장,
  p.33):[^evans2003]

> If sophisticated domain experts don't understand the model, there is something wrong with
> the model.

  - 위 [우리가 전문가가 되는 것이 목표가 아니다](#우리가-전문가가-되는-것이-목표가-아니다)가
    소프트웨어에 전문가의 사고 모형을 흉내 내라고 요구한다면, 원전의 이 문장은 그 요구를
    **검사 가능한 판정**으로 만든다. 전문은 [유비쿼터스 언어](../concepts/ubiquitous-language.md)에 있다.
- **전문가가 얻는 것도 원전에 적혀 있다** — **도메인 전문가는 자기가 아는 것을 본질로 증류하도록
  강제됨으로써 흔히 자기 이해를 스스로 다듬고, 소프트웨어 프로젝트가 요구하는 개념적 엄밀성을
  이해하게 된다** (1장, p.15).[^evans2003] 위
  [지식은 암묵적이고 때로는 함께 만들어진다](#지식은-암묵적이고-때로는-함께-만들어진다)의 상호
  학습이 원전에서는 같은 방향으로 이미 적혀 있다.
- **원전은 팀 구성까지 처방한다** — **장기적으로 전념하고 도메인 지식의 저장소가 되는 데 관심이
  있는 강한 개발자들과, 업무를 깊이 아는 한 명 이상의 도메인 전문가를 짝지은 팀을 꾸려 이
  순환을 깨는 것이 본질적이다** (15장, p.403).[^evans2003] 이 2021년 판본의 1장에는 그 처방이
  없다. 전문은 [핵심 도메인](../concepts/core-domain.md)에 있다.

## 이어지는 페이지

- [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md) — 이 전문성이 걸리는 범위
- [하위 도메인의 세 종류](subdomain-types.md) — 정의되지 않은 개념이 몰려 있는 곳이 어디인가
- [지식 정련](../concepts/knowledge-crunching.md) — 이 역할이 참여하는 활동
- [유비쿼터스 언어](../concepts/ubiquitous-language.md) — 이 대화가 만들어 내는 것
- [모델 주도 설계](../concepts/model-driven-design.md) — 변환 단계가 늘어날 때 잃는 것
- [핵심 도메인](../concepts/core-domain.md) — 이 역할과 개발자를 어떻게 짝지을 것인가
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^khononov2021]: Khononov 2021, 1장 "Analyzing Business Domains"
    §"Who Are the Domain Experts?"(p.17)와 §"Conclusion"(p.18) ·
    2장 "Discovering Domain Knowledge" 장 도입의 제사(p.21) · §"Knowledge Discovery"(p.22) ·
    §"Challenges"(pp.30–31). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 직인용의 굽은 따옴표는
    곧은 따옴표로 옮겼고 그 밖의 글자는 원문 그대로다. 브란돌리니의 두 인용은 이 책이 대는
    출처이고 이 KB가 직접 확인한 원전이 아니다 — 제사는 출처 표기 없이 이름만 달려 있고,
    "학습 과정" 쪽은 이 책의 각주가 Brandolini, *Introducing EventStorming*(Leanpub)을
    가리킨다.

[^evans2003]: Evans 2003, 1장 "Crunching Knowledge" §Knowledge Crunching(pp.14–15) ·
    2장 "Communication and the Use of Language" §"One Team, One Language"(p.33) ·
    15장 "Distillation" §"Who Does the Work?"(p.403). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측).
