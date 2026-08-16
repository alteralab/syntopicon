---
type: concept
title: AI 엔지니어링 스택
description: 매일 바뀌는 도구 대신 붙잡을 세 층 — 애플리케이션 개발·모델 개발·인프라가 각각 무엇을 맡고 어디서부터 내려가는지, 리포지토리 수로 본 층별 성장의 비대칭, 그리고 파운데이션 모델이 와도 그대로인 원리들
generated: { by: "claude-opus-5", at: "2026-08-16T15:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# AI 엔지니어링 스택

- [왜 층으로 보는가](#왜-층으로-보는가)
- [세 층](#세-층)
- [층마다 얼마나 자랐는가](#층마다-얼마나-자랐는가)
- [그대로인 것들](#그대로인-것들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **매일 새 도구가 쏟아지는 분야에서 무엇을 붙잡고 구조를 이해할 것인가.**

## 왜 층으로 보는가

- 문제의 진단 — **AI 엔지니어링의 빠른 성장은 엄청난 양의 하이프와 FOMO(fear of missing out)도
  불러왔다. 매일 도입되는 새 도구·기법·모델·애플리케이션의 수는 압도적일 수 있다. 계속 움직이는 모래를
  따라가려 하는 대신 AI 엔지니어링의 근본 구성 요소를 들여다보자** (1장, p.35).[^huyen2025]
- 출발점은 계보다 — **AI 엔지니어링을 이해하려면 AI 엔지니어링이 ML 엔지니어링에서 진화해 나왔다는
  것을 알아보는 것이 중요하다. 회사가 파운데이션 모델을 실험하기 시작할 때 기존 ML 팀이 그 노력을
  이끄는 것이 자연스럽다. 어떤 회사는 AI 엔지니어링을 ML 엔지니어링과 같은 것으로 취급한다** (1장,
  p.36).[^huyen2025]
- 조직마다 배치가 다르다 — **조직이 AI 엔지니어와 ML 엔지니어를 어디에 두든 그 역할은 상당히 겹친다.
  기존 ML 엔지니어는 AI 엔지니어링을 기술 목록에 더해 취업 전망을 넓힐 수 있다. 그러나 이전 ML 경험이
  전혀 없는 AI 엔지니어도 있다** (1장, p.36).[^huyen2025]

## 세 층

- 층의 목록과 진입 방향 — **어떤 AI 애플리케이션 스택에도 세 층이 있다: 애플리케이션 개발, 모델 개발,
  인프라. AI 애플리케이션을 개발할 때 당신은 맨 위 층에서 시작해 필요에 따라 아래로 내려가게 될
  가능성이 높다** (1장, p.37).[^huyen2025]
- 애플리케이션 개발(application development) (1장, p.37):[^huyen2025]

  > With models readily available, anyone can use them to develop applications. This is the layer
  > that has seen the most action in the last two years, and it is still rapidly evolving.
  > Application development involves providing a model with good prompts and necessary context.
  > This layer requires rigorous evaluation. Good applications also demand good interfaces.

- 모델 개발(model development) (1장, p.37):[^huyen2025]

  > This layer provides tooling for developing models, including frameworks for modeling,
  > training, finetuning, and inference optimization. Because data is central to model
  > development, this layer also contains dataset engineering. Model development also requires
  > rigorous evaluation.

- 인프라(infrastructure) (1장, p.37):[^huyen2025]

  > At the bottom is the stack is infrastructure, which includes tooling for model serving,
  > managing data and compute, and monitoring.

- 층마다 딸린 책임의 목록은 다음과 같다 (1장, p.38, Figure 1-14):[^huyen2025]

  | 층 | 책임 |
  |---|---|
  | Application development | AI interface · Prompt engineering · Context construction · Evaluation |
  | Model development | Inference optimization · Dataset engineering · Modeling & training · Evaluation |
  | Infrastructure | Compute management · Data management · Serving · Monitoring |

  - 평가(evaluation)가 위 두 층에 모두 걸려 있다 — **대부분의 사람이 애플리케이션 개발 층에서 그것을
    먼저 마주칠 것이므로 평가는 그쪽 절에서 논의한다** (1장, pp.40–41).[^huyen2025]

## 층마다 얼마나 자랐는가

- 저자의 측정 — **파운데이션 모델과 함께 지형이 어떻게 진화했는지 감을 잡으려고 2024년 3월 GitHub에서
  별 500개 이상인 모든 AI 관련 리포지토리를 검색했다. GitHub의 보급률을 고려하면 이 데이터가 생태계를
  이해하는 좋은 대리 지표라고 믿는다. 분석에는 애플리케이션 개발 층과 모델 개발 층의 산물인 애플리케이션
  리포지토리와 모델 리포지토리도 포함했다. 총 920개의 리포지토리를 찾았다** (1장, p.38).[^huyen2025]
- 그 결과의 요지 — **데이터는 Stable Diffusion과 ChatGPT의 도입 이후 2023년에 AI 도구 수가 크게
  도약했음을 보여 준다. 2023년에 가장 크게 증가한 범주는 애플리케이션과 애플리케이션 개발이었다. 인프라
  층도 얼마간 성장했지만 다른 층에서 본 성장보다 훨씬 적었다. 이는 예상된 바다. 모델과 애플리케이션이
  바뀌었어도 자원 관리·서빙·모니터링 등 핵심 인프라 요구는 그대로이기 때문이다** (1장,
  p.39).[^huyen2025]

## 그대로인 것들

- 흥분의 수준과 원리의 수준은 다르다 — **파운데이션 모델을 둘러싼 흥분과 창의성의 수준은 전례가 없지만
  AI 애플리케이션을 만드는 많은 원리는 그대로다** (1장, p.39).[^huyen2025] 저자가 드는 것은 넷이다
  (1장, p.39):[^huyen2025]
  - **기업 유스케이스에서 AI 애플리케이션은 여전히 사업 문제를 풀어야 하고, 따라서 사업 지표에서 ML
    지표로, 또 그 반대로 대응시키는 일이 여전히 필수적이다.**
  - **여전히 체계적인 실험을 해야 한다. 고전적 ML 엔지니어링에서는 서로 다른 하이퍼파라미터로 실험한다.
    파운데이션 모델과 함께라면 서로 다른 모델·프롬프트·검색 알고리즘·샘플링 변수 등으로 실험한다.**
  - **여전히 모델이 더 빠르고 싸게 돌기를 원한다.**
  - **프로덕션 데이터로 애플리케이션을 반복적으로 개선할 수 있도록 피드백 루프를 세우는 일이 여전히
    중요하다.**
- 그래서 축적이 이어진다 — **이는 ML 엔지니어들이 지난 십 년간 배우고 공유한 것의 많은 부분이 여전히
  적용된다는 뜻이다. 이 집단적 경험은 모두가 AI 애플리케이션을 만들기 시작하는 것을 더 쉽게 만든다.
  그러나 이 지속되는 원리들 위에 AI 엔지니어링 고유의 혁신이 많이 얹혀 있다** (1장,
  p.39).[^huyen2025]

## 이어지는 페이지

- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 맨 위 층의 세 책임
- [모델 개발 층](../concepts/ai-model-development-layer.md) — 가운데 층의 세 책임
- [AI 엔지니어링과 ML 엔지니어링](../concepts/ai-engineering-versus-ml-engineering.md) — 이 스택이
  전통적 ML 스택과 갈리는 지점
- [AI 엔지니어링이란](../concepts/ai-engineering-defined.md) — 이 스택을 다루는 분야의 정의
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 두 층에 걸쳐 있는 적응이라는 활동

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48). 도판 Figure 1-12·1-13(링크드인 채용 공고 스크린샷), Figure 1-14(세 층 그림 — 표로
    옮겼다), Figure 1-15(범주별 리포지토리 누적 추이)는 그림 자체를 옮기지 않았다.
