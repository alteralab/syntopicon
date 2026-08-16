---
type: concept
title: 전통적 데이터 합성 기법
description: AI 이전부터 있던 두 갈래 — 템플릿과 난수로 채우는 규칙 기반 생성, 뒤집기·자르기·단어 치환 같은 절차적 변환과 편향 완화, 픽셀 하나로 분류를 뒤집는 섭동, 그리고 실험을 가상으로 돌리는 시뮬레이션
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 전통적 데이터 합성 기법

- [절차적 생성이라는 이름](#절차적-생성이라는-이름)
- [규칙 기반 데이터 합성](#규칙-기반-데이터-합성)
- [기존 데이터를 변환하기](#기존-데이터를-변환하기)
- [섭동](#섭동)
- [시뮬레이션](#시뮬레이션)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **AI를 쓰지 않고 데이터를 만들어 내는 방법에는 무엇이 있는가.**

## 절차적 생성이라는 이름

- 절이 여는 자리 (8장, p.383):[^huyen2025]

  > Data synthesis isn't unique to AI. It has a long history in software testing, gaming, and
  > robotics. Using algorithms to generate data is also called *procedural generation*, as opposed
  > to *manual generation*.

  **절차적 생성은 게임에서 레벨·맵·아이템·캐릭터 같은 콘텐츠를 즉석에서 생성하는 데 흔히 쓰인다. 이
  산업들에서 쓰이는 대부분의 데이터 생성 기법은 AI에 적용될 수 있다** (8장, p.383).[^huyen2025]
  - 각주가 드는 실물 — **많은 훌륭한 게임이 절차적 생성 덕분에만 가능하다. 『Minecraft』와 『No
    Man's Sky』 같은 게임은 잡음 함수와 프랙탈 알고리즘을 써서 방대하고 몰입감 있는 세계를 만든다.
    『Dungeons & Dragons』에서 절차적 생성은 무작위 던전·퀘스트·마주침을 만드는 데 쓰여, 예측 불가능성과
    끝없는 가능성이라는 요소를 더해 게임을 더 매력적으로 만든다** (8장, p.383 각주 10).[^huyen2025]
- 두 갈래 — **전통적으로 데이터 합성과 증강에는 두 접근이 있었다: 규칙 기반과 시뮬레이션. 진보된 AI
  모델이 가능하게 만든 더 새로운 방법은 AI 자체를 써서 데이터를 합성하는 것이다** (8장,
  p.383).[^huyen2025]

## 규칙 기반 데이터 합성

- **데이터를 생성하는 가장 단순한 방법은 미리 정의된 규칙과 템플릿을 쓰는 것이다. 예컨대 신용카드
  거래를 만들려면 거래 템플릿에서 시작해 Faker 같은 난수 생성기로 이 템플릿의 각 필드를 채운다**
  (8장, p.383).[^huyen2025] 저자가 실은 템플릿 예시다 (8장, p.383):[^huyen2025]

  ```text
  An example of a transaction template.
  Transaction ID: [Unique Identifier]
  Date: [MM/DD/YYYY]
  Time: [HH:MM:SS]
  Amount: [Transaction Amount]
  Merchant Name: [Merchant/Store Name]
  Merchant Category: [Category Code]
  Location: [City, State, Country]
  Payment Method: [Credit Card/Debit Card/Cash/Online Payment]
  Transaction Status: [Completed/Pending/Failed]
  Description: [Transaction Description]
  ```

- 왜 이렇게 하는가 — **거래 데이터의 민감성 때문에 많은 사기 탐지 모델이 실제 데이터에 접근하기 전에
  타당성을 입증하려고 이런 템플릿에서 생성된 합성 거래 데이터로 먼저 훈련된다** (8장,
  p.383).[^huyen2025]
- 템플릿이 닿는 범위 — **송장·이력서·세금 양식·은행 명세서·행사 일정·제품 카탈로그·계약서·설정 파일
  등 특정 구조를 따르는 문서를 생성하는 데 템플릿을 쓰는 것이 흔하다. 템플릿은 정규 표현식과 수학
  방정식처럼 특정 문법과 구문을 따르는 데이터를 생성하는 데도 쓰일 수 있다. AI 모델이 풀 수학 방정식을
  생성하는 데 템플릿을 쓸 수 있다. DeepMind는 올림피아드 수준의 기하 모델 AlphaGeometry를 합성 예제
  1억 개를 써서 훈련했다(Trinh et al., 2024)** (8장, p.384).[^huyen2025]

## 기존 데이터를 변환하기

- **단순한 변환을 적용해 기존 데이터에서 새 데이터를 절차적으로 생성할 수 있다. 이미지의 경우 이미지를
  무작위로 회전·자르기·크기 조정하거나 일부를 지울 수 있다. 뒤집힌 고양이 이미지는 여전히 고양이여야
  한다. 축구 경기를 살짝 자른 이미지는 여전히 축구 경기여야 한다. Krizhevsky et al.(2012)은
  AlexNet 논문에서 이 기법을 써서 ImageNet 데이터셋(Deng et al., 2009)을 증강함으로써 그 유용성을
  시연했다** (8장, p.384).[^huyen2025]
- 텍스트 쪽 — **텍스트의 경우 이 치환이 문장의 의미나 감성을 바꾸지 않으리라 가정하고 단어를 비슷한
  단어로 무작위 치환할 수 있다. 예컨대 원문 "She's a fantastic nurse"는 새 예제 "She's a great
  nurse"를 생성할 수 있다** (8장, p.384).[^huyen2025]
- 편향 완화로 쓰는 법 — **이 접근은 데이터의 잠재적 편향을 완화하는 데 쓰일 수 있다. 데이터에 젠더
  편향이 있어 예컨대 "nurse"가 여성과 결부되고 "doctor"가 남성과 결부되는 것이 걱정된다면, 성별이
  드러난 단어를 그 반대로 치환할 수 있다** (8장, p.384).[^huyen2025] 저자가 든 대비표다. 원문의
  기울임 강조를 그대로 두었다 (8장, p.384, Table 8-2):[^huyen2025]

  | Original data | Augmented data |
  |---|---|
  | She's a fantastic nurse. | *He*'s a fantastic nurse. / She's a fantastic *doctor*. |
  | The CEO of the firm, Mr. Alex Wang, … | The CEO of the firm, *Ms. Alexa Wang*, … |
  | Today, my mom made a casserole for dinner. | Today, my *dad* made a casserole for dinner. |
  | Emily has always loved the violin. | *Mohammed* has always loved the violin. |

- 어떻게 비슷한 단어를 찾는가 — **비슷한 단어는 동의어 사전으로 찾거나 단어 임베딩 공간에서 임베딩이
  서로 가까운 단어를 찾아 찾을 수 있다. AI에게 예제를 재구성하거나 번역해 달라고 요청해 단순한 단어
  치환을 넘어설 수 있다** (8장, p.384).[^huyen2025] 그 임베딩 공간 자체는
  [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.

## 섭동

- **흥미로운 변환 하나는 섭동(perturbation)이다: 기존 데이터에 잡음을 더해 새 데이터를 생성하는 것.
  처음에 연구자들은 데이터 표본을 살짝 섭동하면 모델을 속여 오분류하게 만들 수 있음을 발견했다. 예컨대
  배 사진에 백색 잡음을 더하면 모델이 그것을 자동차로 오분류하게 만들 수 있다. 논문 "One Pixel Attack
  for Fooling Deep Neural Networks"(Su et al., 2017)는 Kaggle CIFAR-10 테스트 데이터셋의 자연
  이미지의 67.97%와 ImageNet 테스트 이미지의 16.04%가 픽셀 하나만 바꿔 오분류될 수 있음을 보였다.
  이는 악용되면 심각한 위험을 낳는다. 공격자가 AI 모델을 속여 자신을 인가된 직원으로 오인하게 하거나
  자율주행차가 분리대를 차선으로 착각하게 만들어 사고로 이어지게 할 수 있다** (8장,
  p.385).[^huyen2025]
- 방어로 뒤집기 — **섭동된 데이터로 모델을 훈련할 수 있다. 섭동은 모델의 성능을 개선하고 공격에 더
  견고하게 만들 수 있다; Goodfellow et al., 2013과 Moosavi-Dezfooli et al., 2015를 보라. 2019년
  Hendrycks와 Dietterich는 밝기 변경·눈 추가·대비 변경·잡음 추가 같은 15가지 흔한 시각적 손상을
  ImageNet 이미지에 적용해 ImageNet-C와 ImageNet-P를 만들었다** (8장, p.385).[^huyen2025]
- 텍스트 쪽 실물 — **섭동은 텍스트에도 쓰일 수 있다. 예컨대 BERT를 훈련하는 데 저자들은 토큰의
  1.5%를 무작위 단어로 치환했다(Devlin et al., 2018). 그들은 이 섭동이 작은 성능 향상으로 이어짐을
  발견했다** (8장, p.385).[^huyen2025]
- 시각 자산 쪽 — **시각 데이터는 더 정교한 알고리즘으로 증강될 수 있다. Snap(2022)은 자기 자산을
  증강해 예상 밖의 코너 케이스를 만들고 데이터의 암묵적 편향을 완화하는 방법에 대한 훌륭한 사례
  연구를 갖고 있다. 캐릭터가 주어지면 그들은 피부색·체형·머리 모양·옷·표정까지 다른 비슷한 캐릭터를
  합성한다. 이 증강된 자산은 그다음 AI 모델을 훈련하는 데 쓰인다** (8장, p.385).[^huyen2025]

## 시뮬레이션

- **실제 세계에서 실험을 돌려 데이터를 수집하는 것은 비싸고 위험할 수 있으므로, 대신 이 실험을
  가상으로 시뮬레이션할 수 있다. 예컨대 자율주행차가 고속도로에서 말과 마주쳤을 때 어떻게 반응하는지
  시험하려고 고속도로에 실제 말을 풀어놓는 것은 위험할 것이다. 대신 가상 환경에서 이 상황을
  시뮬레이션한다. 자율주행 시뮬레이션 엔진의 예로 CARLA(Dosovitskiy et al., 2017), Waymo의
  SimulationCity, Tesla의 샌프란시스코 시뮬레이션이 있다** (8장, pp.385–386).[^huyen2025]
- 로보틱스 — **비슷하게 로보틱스를 위한 훈련 데이터를 가상 환경에서 시뮬레이션하는 것이 매우 흔하다.
  로봇에게 커피 따르기를 훈련하고 싶은데 각 관절이 어떻게 움직여야 동작이 성공하는지 정확히 모른다고
  하자. 서로 다른 관절 움직임을 가진 여러 시나리오를 시뮬레이션하고 커피가 성공적으로 따라진
  시나리오만 써서 로봇을 훈련할 수 있다** (8장, p.386).[^huyen2025]
- 무엇이 보장되고 무엇이 안 되는가 — **시뮬레이션은 사고와 물리적 손상을 피하면서 최소 비용으로 여러
  실험을 돌리게 해 준다. 시뮬레이션에서 작동하는 로봇이 실제 세계에서는 작동하지 않을 수 있지만,
  시뮬레이션에서 실패하면 실제 세계에서도 실패할 가능성이 높다. 시뮬레이션이 아무리 정교해도 그것은
  실제 세계의 단순화다. Sim2Real은 시뮬레이션에서 훈련된 알고리즘을 실제 세계에 적응시키는 데 초점을
  맞춘 하위 분야다** (8장, p.386).[^huyen2025]
- 도구 사용 데이터 — **시뮬레이션은 모델에게 도구 쓰는 법을 가르칠 데이터를 생성하는 데 흔하다.
  앞서 언급했듯 사람이 생성한 행동이 AI 에이전트에 항상 가장 효율적이지는 않을 수 있다. 시뮬레이션은
  사람이 간과하는 행동을 드러내는 데 도움이 될 수 있다. 질의가 주어지면 서로 다른 행동 시퀀스를
  시뮬레이션하고 이 시퀀스를 실행해 그 결과를 검증할 수 있다. 가장 효율적인 행동 시퀀스가 그다음 그
  질의의 주석된 응답으로 쓰인다** (8장, p.386).[^huyen2025]
- 희귀 사건 — **시뮬레이션은 희귀 사건의 데이터를 생성하는 데 특히 값지다. 예컨대 금융에서 연구자는
  기업의 성공적 상장이나 중대한 파산 같은 시나리오를 시뮬레이션해 그 시장 영향을 이해할 수 있다.
  제조업체는 재료나 조립품의 결함을 시뮬레이션해 이상 탐지와 품질 관리 모델을 훈련할 데이터를 생성할
  수 있다. 비슷하게 지구 시스템을 시뮬레이션해 기후 과학자는 기온 변화·강수 패턴·극단적 기상 시나리오의
  변형을 만들 수 있다. 이 합성 데이터는 그다음 AI 모델에 들어가 더 넓은 가능한 미래의 스펙트럼에서
  배울 수 있게 한다** (8장, p.386).[^huyen2025]
- 절을 닫는 문장 — **규칙 기반과 시뮬레이션 기반 기법 모두 많은 유스케이스에 유용했지만, 데이터 합성이
  정말로 도약한 것은 AI가 현실적이고 고품질인 데이터를 생성할 수 있게 되고 나서였다** (8장,
  p.386).[^huyen2025]

## 이어지는 페이지

- [AI 기반 데이터 합성](../concepts/ai-powered-data-synthesis.md) — 같은 목표를 모델로 하는 쪽
- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 두 낱말의 경계와 다섯 이유
- [합성 데이터 검증](../concepts/synthetic-data-verification.md) — 만든 데이터를 거르는 단계
- [데이터 큐레이션의 요구 조건](../concepts/data-curation-requirements.md) — 도구 사용 데이터가
  시뮬레이션으로 넘어가는 자리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 비슷한 단어를 찾는 공간
- [AI 안전 평가](../concepts/ai-safety-evaluation.md) — 적대적 예제가 평가 쪽에서 다뤄지는 자리

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Traditional Data Synthesis
    Techniques"(pp.383–386). 거래 템플릿 펜스(p.383)와 Table 8-2(p.384)는 원문 표기를 그대로
    옮겼다 — 템플릿은 실행할 것이 아니라 채울 자리표라 `text` 펜스로 두었다. 이 구간에는 도판이
    없다. Trinh et al.(2024)·Krizhevsky et al.(2012)·Deng et al.(2009)·Su et al.(2017)·Goodfellow
    et al.(2013)·Moosavi-Dezfooli et al.(2015)·Devlin et al.(2018)·Dosovitskiy et al.(2017)·
    Snap(2022)은 huyen2025를 통한 전언이다.
