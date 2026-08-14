---
type: concept
title: 공학 윤리와 책임
status: draft
description: 데이터 시스템을 만드는 사람이 그 결과에 지는 책임 — 데이터셋 대부분이 사람에 관한 것이라는 사실, 기술 자체는 좋지도 나쁘지도 않다는 흔한 말이 책임을 면제해 주지 않는 이유, 윤리 개념이 컴퓨팅의 다른 개념과 달리 확정적이지 않다는 점, 그리고 윤리가 체크리스트가 아니라 과정이라는 규정
generated: { by: "claude-opus-5", at: "2026-08-15T09:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 공학 윤리와 책임

하나의 질문: **시스템을 만드는 엔지니어는 그 시스템이 낳는 결과에 대해 무엇을 책임지는가.**

이 장의 제사로 저자들이 인용한 문장을 그대로 옮긴다 (14장, p.585):[^kleppmann2026]

> Feeding AI systems on the world’s beauty, ugliness, and cruelty, but expecting it to
> reflect only the beauty is a fantasy.
>     —Vinay Uday Prabhu and Abeba Birhane, “Large Datasets: A Pyrrhic Win for Computer
>     Vision?” (2020)

## 빠뜨린 논의

- 저자들이 마지막 장을 여는 이유 — **이 책 전체에서 우리는 데이터 시스템을 위한 광범위한
  아키텍처를 살피고, 그 장단점을 평가하고, 신뢰할 수 있고 확장 가능하고 유지보수 가능한 애플리케이션을
  짓는 기법을 탐구했다. 그러나 우리는 논의의 근본적인 부분 하나를 빠뜨렸고 이제 그것을 채워야
  한다** (14장, p.585).[^kleppmann2026]
- **모든 시스템은 어떤 목적을 위해 지어진다; 우리가 취하는 모든 행동은 의도한 결과와 의도하지 않은
  결과를 둘 다 갖는다. 그 목적은 돈을 버는 것만큼 단순할 수 있지만 그 결과는 멀리까지 미칠 수 있다.
  이 시스템을 짓는 우리 엔지니어에게는 그 결과를 신중히 고려하고 우리의 결정이 해를 끼치지 않도록
  보장할 책임이 있다** (14장, p.585).[^kleppmann2026]

## 데이터셋은 사람에 관한 것이다

- **우리는 데이터를 추상적인 것으로 이야기하지만, 많은 데이터셋이 사람에 관한 것임을 기억하라:
  그들의 행동, 그들의 관심, 그들의 정체성. 우리는 그런 데이터를 인간성과 존중으로 다뤄야 한다.
  사용자도 인간이며, 인간의 존엄이 최우선이다** (14장, p.585).[^kleppmann2026]
- 지침은 있으나 — **소프트웨어 개발은 점점 더 중요한 윤리적 선택을 포함한다. ACM 윤리·직업 행동
  강령(ACM Code of Ethics and Professional Conduct)처럼 소프트웨어 엔지니어가 이런 문제를
  헤쳐 나가도록 돕는 지침이 있지만, 그것들은 실무에서 논의되고 적용되고 집행되는 일이 드물다. 그
  결과 엔지니어와 프로덕트 매니저가 프라이버시와 제품의 잠재적 부정적 결과에 대해 때때로 무신경한
  태도를 취한다** (14장, p.585).[^kleppmann2026]

## 기술은 중립이라는 말의 한계

- 저자들의 정식화 — **기술 자체는 좋지도 나쁘지도 않다 — 중요한 것은 그것이 어떻게 쓰이고 사람에게
  어떻게 영향을 주는가다. 이는 검색 엔진 같은 소프트웨어 시스템에 대해서도 총 같은 무기에 대해서와
  거의 같은 방식으로 참이다. 윤리적 책임은 우리가 져야 하는 것이다; 소프트웨어 엔지니어가 기술에만
  배타적으로 집중하고 그 결과를 무시하는 것으로는 충분하지 않다** (14장,
  pp.585–586).[^kleppmann2026]

## 윤리는 컴퓨팅의 다른 개념과 다르다

- **그러나 컴퓨팅의 많은 부분과 대조적으로 윤리의 핵심에 있는 개념들은 그 정확한 의미가 고정돼
  있거나 확정적이지 않다; 그것들은 해석을 요구하며 그 해석은 주관적일 수 있다. 무엇이 어떤 것을
  "좋게" 또는 "나쁘게" 만드는지는 잘 정의돼 있지 않고, 이 주제에 대한 컴퓨팅 전문가들 사이의 진지한
  담론이 부족하다** (14장, p.586).[^kleppmann2026]
- 그래도 해야 하는 일이며, 그 정의가 명시된다 (14장, p.586):[^kleppmann2026]

> Reasoning about ethics is difficult, but it is too important to ignore. What does this
> entail? Ethics is not going through a checklist to confirm you comply; it’s a
> participatory and iterative process of reflection, in dialog with the people involved,
> with accountability for the results.

## 책의 마지막 문장이 남기는 것

- 마지막 장의 요약이 이 장에서 본 해악을 열거한다 — **데이터가 좋은 일을 하는 데 쓰일 수 있지만
  상당한 해도 끼칠 수 있음을 보았다: 사람들의 삶에 심각하게 영향을 주면서 항소하기는 어려운 결정을
  내리고, 차별과 착취로 이어지고, 감시를 정상화하고, 내밀한 정보를 노출하는 것. 우리는 또한 데이터
  유출의 위험을 무릅쓰며, 선의로 한 데이터 사용이 의도하지 않은 결과를 낳는 것을 발견할 수도 있다**
  (14장, p.598).[^kleppmann2026]
- 그리고 책은 이렇게 끝난다 (14장, p.598):[^kleppmann2026]

> Given the large impact that software and data have on the world, we as engineers must
> remember that we carry a responsibility to work toward the kind of world that we want to
> live in: a world that treats people with humanity and respect. Let’s work together toward
> that goal.

## 이어지는 페이지

- [예측 분석과 알고리즘의 해악](../concepts/predictive-analytics-and-algorithmic-harm.md) —
  데이터로 사람에 대한 결정을 내릴 때 벌어지는 일
- [감시와 동의](../concepts/surveillance-and-consent.md) — 데이터 수집 자체가 문제가 되는 자리
- [결정권으로서의 프라이버시](../concepts/privacy-as-a-decision-right.md) — 프라이버시가 비밀
  유지가 아니라 선택권이라는 정의
- [위험 자산으로서의 데이터](../concepts/data-as-a-hazardous-asset.md) — 쌓아 둔 개인 데이터가
  지는 위험과 규제
- [설계와 이해 가능성](../concepts/designing-for-understandability.md) — 시스템을 만드는 사람의
  다른 종류의 책임
- [데이터 레이크](../concepts/data-lake.md) — 데이터 최소화가 1장에서 나온 자리

[^kleppmann2026]: Kleppmann & Riccomini 2026, 14장 "Doing the Right Thing"
