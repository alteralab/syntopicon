---
type: concept
title: 애플리케이션 개발 층
description: 모두가 같은 모델을 쓰는 세계에서 차별점이 만들어지는 층 — 개방형 출력 탓에 정답 목록을 만들 수 없어 커진 평가 문제와 그것을 드러낸 Gemini 벤치마크 사건, 가중치를 건드리지 않고 행동을 끌어내는 프롬프트 엔지니어링과 맥락 구성, 그리고 독립 제품에서 플러그인까지 넓어진 AI 인터페이스
generated: { by: "claude-opus-5", at: "2026-08-16T15:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 애플리케이션 개발 층

- [차별점이 여기로 옮겨 왔다](#차별점이-여기로-옮겨-왔다)
- [평가](#평가)
- [프롬프트 엔지니어링과 맥락 구성](#프롬프트-엔지니어링과-맥락-구성)
- [AI 인터페이스](#ai-인터페이스)
- [세 책임이 어떻게 옮겨 갔는가](#세-책임이-어떻게-옮겨-갔는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모두가 같은 모델을 쓸 수 있게 되면 무엇으로 제품을 가르는가.**

## 차별점이 여기로 옮겨 왔다

- **전통적 ML 엔지니어링에서는 팀이 자기 소유 모델로 애플리케이션을 만들었으므로 모델 품질이
  차별점이다. 많은 팀이 같은 모델을 쓰는 파운데이션 모델과 함께라면 차별화는 애플리케이션 개발 과정을
  통해 얻어져야 한다** (1장, p.44).[^huyen2025]
- **애플리케이션 개발 층은 다음 책임들로 이뤄진다: 평가, 프롬프트 엔지니어링, AI 인터페이스** (1장,
  p.44).[^huyen2025]

## 평가

- 정의 (1장, p.44):[^huyen2025]

  > *Evaluation* is about mitigating risks and uncovering opportunities.

- 어디에 필요한가 — **평가는 모델 적응 과정 전체에 걸쳐 필요하다. 모델을 선택하는 데, 진척을 벤치마크하는
  데, 애플리케이션이 배포 준비가 되었는지 판단하는 데, 그리고 프로덕션에서 문제와 개선 기회를 탐지하는
  데 평가가 필요하다** (1장, p.44).[^huyen2025]
- 왜 더 어려워졌는가 — **평가는 ML 엔지니어링에서 늘 중요했지만 파운데이션 모델과 함께라면 여러 이유로
  한층 더 중요하다. 그 난제는 주로 파운데이션 모델의 개방형 성질과 확장된 능력에서 온다** (1장,
  p.44).[^huyen2025]
- 정답이 없다는 것이 핵심이다 — **예컨대 사기 탐지 같은 폐쇄형 ML 과제에서는 모델 출력과 비교할 기대되는
  정답(ground truth)이 대개 있다. 모델 출력이 기대 출력과 다르면 모델이 틀렸다는 것을 안다. 그러나
  챗봇 같은 과제에서는 각 프롬프트에 가능한 응답이 너무 많아서 모델 응답과 비교할 정답을 남김없이 큐레이션
  하는 것이 불가능하다** (1장, p.44).[^huyen2025]
- 적응 기법의 수도 평가를 어렵게 만든다 — **어떤 기법으로는 성능이 나쁜 시스템이 다른 기법으로는 훨씬 잘할
  수 있다. 2023년 12월 구글이 Gemini를 출시했을 때 그들은 Gemini가 MMLU 벤치마크에서 ChatGPT보다 낫다고
  주장했다. 구글은 CoT@32라는 프롬프트 엔지니어링 기법으로 Gemini를 평가했다. 이 기법에서 Gemini에게는
  32개의 예가 주어졌고 ChatGPT에게는 5개만 주어졌다. 둘 다에게 5개의 예가 주어졌을 때는 ChatGPT가 더 잘
  했다** (1장, p.44).[^huyen2025]
- 그 실측값이다 (1장, p.45, Table 1-5 — Gemini 기술 리포트, 2023년 12월):[^huyen2025]

  | 모델 | MMLU (기법 표기) | MMLU (5-shot) |
  |---|---|---|
  | Gemini Ultra | 90.04% CoT@32 | 83.7% |
  | Gemini Pro | 79.13% CoT@8 | 71.8% |
  | GPT-4 | 87.29% CoT@32 (via API) | 86.4% (reported) |
  | GPT-3.5 | 70% 5-shot | |
  | PaLM 2-L | 78.4% 5-shot | |
  | Claude 2 | 78.5% 5-shot CoT | |
  | Inflection-2 | 79.6% 5-shot | |
  | Grok 1 | 73.0% 5-shot | |
  | Llama-2 | 68.0% | |

## 프롬프트 엔지니어링과 맥락 구성

- 정의 (1장, p.45):[^huyen2025]

  > *Prompt engineering* is about getting AI models to express the desirable behaviors from the
  > input alone, without changing the model weights.

- 그 위력의 실물은 바로 위 표에 있다 — **Gemini 평가 이야기는 프롬프트 엔지니어링이 모델 성능에 주는
  영향을 부각한다. 다른 프롬프트 엔지니어링 기법을 씀으로써 Gemini Ultra의 MMLU 성능은 83.7%에서
  90.04%로 갔다** (1장, p.45).[^huyen2025]
- 무엇까지 포함하는가 — **프롬프트만으로 모델이 놀라운 일을 하게 만드는 것이 가능하다. 올바른 지시는
  모델이 원하는 과제를, 당신이 고른 형식으로 수행하게 만들 수 있다. 프롬프트 엔지니어링은 모델에게 무엇을
  하라고 말하는 것만이 아니다. 주어진 과제를 하는 데 필요한 맥락과 도구를 모델에게 주는 일이기도 하다.
  긴 맥락을 가진 복잡한 과제에는 모델이 자기 이력을 추적할 수 있도록 메모리 관리 시스템을 제공해야 할
  수도 있다** (1장, p.45).[^huyen2025]

## AI 인터페이스

- 정의 (1장, p.45):[^huyen2025]

  > *AI interface* means creating an interface for end users to interact with your AI applications.

- 이전에는 인터페이스가 남의 제품 안에 있었다 — **파운데이션 모델 이전에는 AI 모델을 개발할 충분한 자원을
  가진 조직만이 AI 애플리케이션을 개발할 수 있었다. 이 애플리케이션은 흔히 그 조직의 기존 제품 안에
  내장되었다. 예컨대 사기 탐지는 Stripe·Venmo·PayPal에 내장되었다. 추천 시스템은 Netflix·TikTok·Spotify
  같은 소셜 네트워크와 미디어 앱의 일부였다** (1장, p.45).[^huyen2025]
- 지금은 자리가 열려 있다 — **파운데이션 모델과 함께라면 누구든 AI 애플리케이션을 만들 수 있다. AI
  애플리케이션을 독립 제품으로 서빙하거나, 다른 사람이 개발한 제품을 포함해 다른 제품에 내장할 수 있다.
  예컨대 ChatGPT와 Perplexity는 독립 제품인 반면, GitHub의 Copilot은 흔히 VSCode의 플러그인으로 쓰이고
  Grammarly는 흔히 Google Docs용 브라우저 확장으로 쓰인다. Midjourney는 독립 웹 앱으로도, Discord 통합을
  통해서도 쓸 수 있다** (1장, p.45).[^huyen2025]
- 인기를 얻고 있는 인터페이스들 (1장, p.46):[^huyen2025]
  - **독립 웹·데스크톱·모바일 앱.** 각주가 든 도구는 **Streamlit, Gradio, Plotly Dash**로, **AI 웹 앱을
    만드는 데 흔히 쓰인다** (1장, p.46 각주 26).[^huyen2025]
  - **사용자가 브라우징하면서 AI 모델에 빠르게 질의하게 해 주는 브라우저 확장.**
  - **Slack·Discord·WeChat·WhatsApp 같은 채팅 앱에 통합된 챗봇.**
  - **VSCode·Shopify·Microsoft 365를 포함한 많은 제품이 개발자가 AI를 플러그인과 애드온으로 자기 제품에
    통합하도록 API를 제공한다. 이 API는 AI 에이전트가 세계와 상호작용하는 데도 쓰일 수 있다.**
- 채팅만이 아니다 — **채팅 인터페이스가 가장 흔히 쓰이지만 AI 인터페이스는 음성 기반(음성 비서처럼)이거나
  체화된 것(증강 현실·가상 현실처럼)일 수도 있다** (1장, p.46).[^huyen2025]
- 피드백의 성질도 바뀐다 — **이 새로운 AI 인터페이스는 사용자 피드백을 수집하고 추출하는 새로운 방식도
  뜻한다. 대화 인터페이스는 사용자가 자연어로 피드백을 주기를 훨씬 쉽게 만들지만, 이 피드백은 추출하기가
  더 어렵다** (1장, p.46).[^huyen2025]

## 세 책임이 어떻게 옮겨 갔는가

- 저자가 정리한 대비표다 (1장, p.46, Table 1-6):[^huyen2025]

  | 범주 | 전통적 ML로 만들 때 | 파운데이션 모델로 만들 때 |
  |---|---|---|
  | AI interface | Less important | Important |
  | Prompt engineering | Not applicable | Important |
  | Evaluation | Important | More important |

## 이어지는 페이지

- [AI 엔지니어링 스택](../concepts/ai-engineering-stack.md) — 이 층이 놓인 자리
- [모델 개발 층](../concepts/ai-model-development-layer.md) — 그 아래 층의 세 책임
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프트 엔지니어링이 속한 분류
- [AI 제품의 기대치와 유지보수](../concepts/ai-product-expectations-and-maintenance.md) — 평가가 재는
  품질 지표가 사업 지표와 만나는 자리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 맥락 검색이 기대는 색인

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48). Table 1-5는 원문의 가로 표(모델이 열)를 세로로 돌려 옮겼고 값은 원문 표기를 그대로
    두었다 — 빈 칸은 원문에 값이 없는 자리다. Table 1-6은 원문 표기를 그대로 옮겼다.
