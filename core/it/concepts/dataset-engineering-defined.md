---
type: concept
title: 데이터셋 엔지니어링이란
description: 예산 안에서 최선의 모델을 훈련할 수 있는 데이터셋을 만드는 일 — 데이터 노력이 GPT-3에서 GPT-4로 가며 두 명에서 여든 명으로 늘어난 실물, 데이터가 곁일에서 전담 직무로 옮겨 간 경위, 모델 중심 AI와 데이터 중심 AI의 갈림, 그리고 이 장이 사후 훈련 데이터를 고르는 이유
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 데이터셋 엔지니어링이란

- [목표](#목표)
- [데이터 노력이 커진 실물](#데이터-노력이-커진-실물)
- [곁일에서 전담 직무로](#곁일에서-전담-직무로)
- [세 덩어리와 그 순서](#세-덩어리와-그-순서)
- [왜 사후 훈련 데이터인가](#왜-사후-훈련-데이터인가)
- [모델 중심 AI와 데이터 중심 AI](#모델-중심-ai와-데이터-중심-ai)
- [자동화되지 않는 것](#자동화되지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터셋 엔지니어링(dataset engineering)이 하려는 것은 무엇이고 왜 지금 그 무게가
커졌는가.**

## 목표

- 장이 여는 자리에서 목표가 한 문장으로 못박힌다 (8장, p.363):[^huyen2025]

  > The quality of a model depends on the quality of its training data. The best ML team in the
  > world with infinite compute can't help you finetune a good model if you don't have data. The
  > goal of dataset engineering is to create a dataset that allows you to train the best model,
  > ideally within your allocated budget.

- 예산이 목표 안에 들어 있다는 점이 이 장 전체의 전제다 — 데이터는 무한히 모으는 것이 아니라
  할당된 돈 안에서 만드는 것이다 (8장, p.363).[^huyen2025]

## 데이터 노력이 커진 실물

- 왜 지금인가 — **모델을 처음부터 개발할 여력이 있는 기업이 줄어들면서, 더 많은 기업이 자기 AI
  성능을 차별화하려고 데이터로 돌아서고 있다. 모델이 더 많은 데이터를 요구하면서 데이터 취급은 더
  어려워지고 인재와 인프라에 더 많은 투자를 요구한다** (8장, p.363).[^huyen2025]
- 저자가 각주에 붙인 수치 대비 — **데이터의 중요성이 커진 것은 GPT-3에서 GPT-4로 가며 데이터
  노력이 어떻게 바뀌었는지에 반영된다. GPT-3의 기여자 목록(OpenAI, 2020)에서 훈련 데이터를 수집·
  필터링·중복 제거하고 겹침 분석을 수행한 것으로 인정받은 사람은 단 두 명이었다. 이것이 3년 뒤
  극적으로 바뀌었다. GPT-4(OpenAI, 2023)에서는 여든 명이 서로 다른 데이터 프로세스에 관여한 것으로
  인정받았다. 이 목록에는 OpenAI가 데이터 제공사를 통해 계약한 데이터 주석자가 아직 포함되지도
  않았다. ChatML 형식처럼 단순하게 들리는 것에 열한 명이 관여했고 그중 다수가 선임 연구자였다.
  2016년 AMA(ask me anything) 스레드에서 OpenAI 공동창업자 중 한 명인 Wojciech Zaremba는 자기
  연구의 대부분을 공개적으로 이용 가능한 데이터셋으로 수행할 작정이라고 말했다** (8장, p.363 각주
  1).[^huyen2025]

## 곁일에서 전담 직무로

- **데이터 운영은 사람들이 시간이 날 때 처리하는 곁일에서 전담 역할로 진화했다. 많은 AI 기업이
  이제 데이터 레이블러·데이터셋 제작자·데이터 품질 엔지니어를 고용하며, 이들은 핵심 엔지니어링
  팀에 통합되거나 그 옆에서 일한다** (8장, p.363).[^huyen2025]
- 요약이 같은 것을 다시 짚는다 — **데이터의 중요성 때문에 팀들은 프라이버시와 규정 준수를 보장하면서
  적절한 데이터셋을 확보할 책임을 지는 전담 데이터 역할을 도입하고 있다** (8장,
  p.403).[^huyen2025]
- 이 장이 무엇을 하는 자리인지 — **모델 지형이 수많은 제공물로 충분히 혼란스럽다면 데이터 지형은
  더욱 복잡하며, 끝없이 늘어나는 데이터셋과 기법의 배열이 도입되고 있다. 이 장은 데이터 지형의
  개관과 자기 데이터셋을 만들 때 고려할 것들을 준다** (8장, p.363).[^huyen2025]

## 세 덩어리와 그 순서

- **이 장은 데이터 큐레이션으로 시작해 어떤 데이터가 필요한가? 얼마나? 데이터가 고품질이라는 것은
  무엇을 뜻하는가? 같은 질문을 다룬다. 그다음 데이터 합성과 처리의 기법을 논한다. 데이터 큐레이션·
  생성·처리는 선형 경로를 따르지 않는다. 서로 다른 단계 사이를 오가야 할 가능성이 높다** (8장,
  p.364).[^huyen2025]
- 저자가 장 서두에 미리 놓는 각오 (8장, p.364):[^huyen2025]

  > There are best practices you can follow and tools that you can use to automate parts of the
  > process. However, data will mostly just be toil, tears, and sweat.

## 왜 사후 훈련 데이터인가

- 훈련 단계마다 데이터가 다르다 — **같은 모델에 대해서도 서로 다른 훈련 단계는 모델에게 서로 다른
  능력을 가르치는 것을 목표로 하고, 따라서 서로 다른 속성을 가진 데이터셋을 요구한다. 예컨대 사전
  훈련의 데이터 양은 흔히 토큰 수로 측정되는 반면 지도 파인 튜닝의 데이터 양은 흔히 예제 수로
  측정된다. 그러나 높은 층위에서 그 큐레이션 과정은 같은 원리를 따른다** (8장, p.364).[^huyen2025]
- 그래서 초점이 정해진다 — **이 장은 사후 훈련 데이터에 초점을 맞추는데, 그쪽이 애플리케이션
  개발자에게 더 관련되기 때문이다. 그러나 사전 훈련 데이터의 교훈이 사후 훈련에 통찰을 줄 때는
  그것도 포함하겠다** (8장, p.364).[^huyen2025] 사전 훈련 데이터 쪽의 실물은
  [훈련 데이터 큐레이션](../concepts/training-data-curation.md)에 있다.

## 모델 중심 AI와 데이터 중심 AI

- 저자가 사이드바로 떼어 놓은 구분이다 — **AI 개발 중 데이터에 대한 초점이 커지면서 모델 중심
  AI(model-centric AI)에 대비되는 데이터 중심 AI(data-centric AI)가 생겨났다** (8장,
  p.364).[^huyen2025]
  - **모델 중심 AI는 모델 자체를 개선해 AI 성능을 높이려 한다. 여기에는 새 구조를 설계하고 모델의
    크기를 키우고 새 훈련 기법을 개발하는 것이 포함된다** (8장, p.364).[^huyen2025]
  - **데이터 중심 AI는 데이터를 개선해 AI 성능을 높이려 한다. 여기에는 새 데이터 처리 기법을
    개발하고 더 적은 자원으로 더 나은 모델을 훈련할 수 있게 하는 고품질 데이터셋을 만드는 것이
    포함된다** (8장, p.364).[^huyen2025]
- 벤치마크의 방향이 뒤집혔다 — **딥러닝 초기에는 많은 AI 벤치마크가 모델 중심이었다. ImageNet 같은
  데이터셋이 주어지면 사람들은 같은 데이터셋을 써서 가능한 최선의 모델을 훈련하려 한다. 최근 몇 년
  사이 더 많은 벤치마크가 데이터 중심이 되었다. 같은 모델이 주어지면 사람들은 이 모델에 최선의
  성능을 주는 데이터셋을 개발하려 한다** (8장, p.364).[^huyen2025]
- 그 실물 — **2021년 앤드루 응은 참가자들이 잘못된 레이블 고치기·엣지 케이스 예제 추가하기·데이터
  증강 같은 기법을 적용해 같은 기반 데이터셋을 개선해야 하는 데이터 중심 AI 대회를 열었다** (8장,
  p.364).[^huyen2025]
- **2023년 DataComp(Gadre et al., 2023)은 CLIP 모델(Radford et al., 2021)을 훈련할 최선의 데이터셋을
  만드는 것을 목표로 하는 대회를 주최했다. 표준화된 스크립트가 제출된 각 데이터셋으로 CLIP 모델을
  훈련한다. 데이터셋의 품질은 그 결과 모델의 38개 하류 과제 성능으로 평가된다. 2024년에 그들은
  412M에서 7B 파라미터 규모의 언어 모델을 평가할 데이터셋을 위한 비슷한 대회를 열었다(Li et al.,
  2024). 비슷한 데이터 중심 벤치마크로 DataPerf(MLCommons, 2023)와 dcbench(Eyuboglu and Karlaš,
  2022)가 있다** (8장, p.364).[^huyen2025]
- 사이드바를 닫는 단서 — **모델 중심과 데이터 중심의 구분은 연구를 안내하는 데 도움이 된다. 그러나
  현실에서 의미 있는 기술적 진보는 흔히 모델과 데이터 양쪽의 개선에 대한 투자를 요구한다** (8장,
  p.365).[^huyen2025]

## 자동화되지 않는 것

- 요약이 이 장 전체의 결론으로 남기는 것 (8장, p.403):[^huyen2025]

  > Data is challenging because many steps in dataset creation aren't easily automatable. It's hard
  > to annotate data, but it's even harder to create annotation guidelines. It's hard to automate
  > data generation, but it's even harder to automate verifying it. While data synthesis helps
  > generate more data, you can't automate thinking through what data you want. You can't easily
  > automate annotation guidelines. You can't automate paying attention to details.

- 그럼에도 원리는 단순하다는 것이 요약의 첫 문장이다 — **훈련 데이터를 만드는 실제 과정이 엄청나게
  복잡함에도 데이터셋을 만드는 원리는 놀랄 만큼 단순하다. 모델을 훈련할 데이터셋을 만들려면, 모델이
  배우기를 원하는 행동을 먼저 생각하고 그 행동을 보여 줄 데이터셋을 설계한다** (8장,
  p.403).[^huyen2025]

## 이어지는 페이지

- [데이터 큐레이션의 요구 조건](../concepts/data-curation-requirements.md) — 무엇을 가르치려는지가
  데이터의 형식과 내용을 정하는 자리
- [훈련 데이터 품질](../concepts/training-data-quality.md) — 세 기준 중 첫째
- [훈련 데이터 커버리지](../concepts/training-data-coverage.md) — 둘째
- [훈련 데이터 수량](../concepts/training-data-quantity.md) — 셋째
- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 데이터를 프로그램으로
  만들어 내는 쪽
- [훈련 데이터 처리](../concepts/training-data-processing.md) — 모은 데이터를 쓸 수 있게 만드는 단계
- [모델 개발 층](../concepts/ai-model-development-layer.md) — 데이터셋 엔지니어링이 이름으로 정의되는
  자리
- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 사전 훈련 데이터의 출처와 품질

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404). 이 페이지는 장 도입부
    (pp.363–364), 사이드바 "A Data-Centric View of AI"(pp.364–365), 그리고 Summary(p.403)를 담았다.
    이 구간에는 도판이 없다. OpenAI(2020)·OpenAI(2023)·Gadre et al.(2023)·Radford et al.(2021)·
    Li et al.(2024)·MLCommons(2023)·Eyuboglu and Karlaš(2022)는 huyen2025를 통한 전언이다.
