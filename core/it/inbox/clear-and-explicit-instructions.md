---
type: concept
title: 명확하고 명시적인 지시
description: 프롬프트 모범 관행의 첫 갈래인 지시 쓰기 — 낡는 요령과 남는 기법을 가르는 기준, 모호함을 없앤다는 것이 실제로 무엇인지, 페르소나가 관점을 바꾸어 점수를 바꾸는 실물, 예시가 애매함을 줄이되 토큰을 먹는다는 거래, 그리고 출력 형식을 지정하고 입력의 끝을 표시하는 마커
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 명확하고 명시적인 지시

- [낡는 요령과 남는 기법](#낡는-요령과-남는-기법)
- [모호함 없이 설명한다](#모호함-없이-설명한다)
- [페르소나를 맡긴다](#페르소나를-맡긴다)
- [예시를 준다](#예시를-준다)
- [예시 형식은 토큰을 먹는다](#예시-형식은-토큰을-먹는다)
- [출력 형식을 지정한다](#출력-형식을-지정한다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델에게 무엇을 하라고 말할 때, 명확하다는 것은 구체적으로 무엇을 적는 일인가.**

## 낡는 요령과 남는 기법

- 왜 요령이 낡는가 — **프롬프트 엔지니어링은, 특히 약한 모델에 대해서는, 엄청나게 해키해질 수 있다.
  프롬프트 엔지니어링 초기에는 "Questions:" 대신 "Q:"라고 쓰라거나 "정답에 300달러 팁"이라는 약속으로
  모델이 더 잘 응답하게 하라는 식의 요령을 담은 많은 안내서가 나왔다. 이 요령들이 어떤 모델에는
  유용할 수 있지만, 모델이 지시를 따르는 데 더 좋아지고 프롬프트 섭동에 더 견고해지면서 낡을 수
  있다** (5장, p.220).[^huyen2025]
- 그래서 저자가 고른 범위 — **이 절은 넓은 범위의 모델에서 통한다고 입증되었고 가까운 미래에도
  유효할 가능성이 높은 일반적 기법에 집중한다. 이 기법들은 OpenAI·앤트로픽·메타·구글을 포함한 모델
  제공자가 만든 프롬프트 엔지니어링 튜토리얼과 생성 AI 애플리케이션을 성공적으로 배포한 팀들이
  공유한 모범 관행에서 추려낸 것이다** (5장, p.220).[^huyen2025]
- 그 밖은 모델마다 다르다 — **이 일반적 관행 밖에서 각 모델은 특정 프롬프트 요령에 반응하는 자기
  나름의 특이성을 가질 가능성이 높다. 어떤 모델과 일할 때는 그 모델에 특화된 프롬프트 엔지니어링
  안내서를 찾아봐야 한다** (5장, p.220).[^huyen2025]
- 이 갈래의 전제 (5장, p.220):[^huyen2025]

  > Communicating with AI is the same as communicating with humans: clarity helps.

## 모호함 없이 설명한다

- **모델이 에세이를 채점하기를 원한다면 쓰고 싶은 점수 체계를 설명하라. 1에서 5인가 1에서 10인가?
  모델이 확신하지 못하는 에세이가 있다면 모델이 능력껏 점수를 고르기를 원하는가, 아니면 "모르겠다"를
  출력하기를 원하는가?** (5장, p.220).[^huyen2025]
- 관찰이 프롬프트로 되먹임된다 — **프롬프트로 실험하면서 조정을 요구하는 바람직하지 않은 행동을
  관찰할 수 있다. 예컨대 모델이 소수 점수(4.5)를 출력하는데 소수 점수를 원하지 않는다면, 정수 점수만
  출력하라고 모델에게 말하도록 프롬프트를 갱신하라** (5장, pp.220–221).[^huyen2025]

## 페르소나를 맡긴다

- 무엇을 바꾸는가 — **페르소나(persona)는 모델이 응답을 생성하는 데 써야 할 관점을 모델이 이해하도록
  도울 수 있다** (5장, p.221).[^huyen2025]
- 저자가 든 실물 — **"I like chickens. Chickens are fluffy and they give tasty eggs."라는 에세이가
  주어지면 기본 상태의 모델은 5점 만점에 2점을 줄 수 있다. 그러나 모델에게 1학년 교사의 페르소나를
  맡으라고 요청하면 그 에세이는 4점을 받을 수 있다** (5장, p.221, Figure 5-5).[^huyen2025] 도판의
  프롬프트에서 페르소나 요청은 나머지 지시("Give the essay below a score from 1 to 5, with 1 being
  very bad and 5 being very good. Be concise. Output only the score and nothing else.") 앞에 붙은
  "You're a first-grade teacher." 한 문장이다 (5장, p.221, Figure 5-5).[^huyen2025]

## 예시를 준다

- 무엇을 줄이는가 — **예시는 모델이 어떻게 응답하기를 원하는지에 대한 모호함을 줄일 수 있다. 어린
  아이들과 대화하는 봇을 짓는다고 상상해 보라. "Will Santa bring me presents on Christmas?"라는
  질문에 모델은 산타클로스가 허구의 인물이므로 누구에게도 크리스마스 선물을 가져다줄 수 없다고
  응답할 수 있다. 이 답은 당신의 봇을 사용자에게 사랑스럽게 만들지 못할 것이다** (5장,
  p.221).[^huyen2025]
- 막는 법 — **이를 막으려면 이빨 요정이 존재한다고 말하는 것처럼 허구의 인물에 대한 질문에 어떻게
  응답할지의 예를 모델에게 줄 수 있다** (5장, p.221).[^huyen2025] 저자가 클로드의 프롬프트
  엔지니어링 튜토리얼에서 착안해 실은 대비다 (5장, p.222, Table 5-1):[^huyen2025]

  | | User prompt | AI response |
  |---|---|---|
  | Without example | Will Santa bring me presents on Christmas? | Santa Claus is a fictional character that kids believe in, bringing magic and excitement to Christmas with stories of his sleigh, reindeer, and gift-giving journey on Christmas Eve. Many parents encourage this belief, as it adds a layer of fun and wonder for children. |
  | With example | Q: Is the tooth fairy real? A: Of course! Put your tooth under your pillow tonight. The tooth fairy might visit and leave you something. Q: Will Santa bring me presents on Christmas? A: | Yes, absolutely! Santa loves to bring presents to kids who believe in him and have been kind all year. Just make sure you're extra good, leave out some cookies, and you might wake up to find gifts under the tree on Christmas morning! |

## 예시 형식은 토큰을 먹는다

- 거래 — **뻔하게 들릴 수 있지만, 입력 토큰 길이가 걱정된다면 더 적은 토큰을 쓰는 예시 형식을
  택하라** (5장, p.222).[^huyen2025]
- 저자가 잰 실물 — 같은 식용·비식용 분류 프롬프트를 두 형식으로 쓴 것이다. 항목마다 `Input: chickpea`
  와 `Output: edible`을 두 줄로 쓰는 형식은 GPT-4 기준 38토큰이고, `chickpea --> edible`처럼 한 줄로
  쓰는 형식은 27토큰이다 (5장, p.222, Table 5-2).[^huyen2025]
  - 저자의 판단 — **둘의 성능이 같다면 둘째 프롬프트가 첫째보다 선호되어야 한다** (5장,
    p.222).[^huyen2025]

## 출력 형식을 지정한다

- 간결함부터 — **모델이 간결하기를 원한다면 그렇게 말하라. 긴 출력은 비쌀 뿐 아니라(모델 API는
  토큰당 과금한다) 지연도 늘린다. 모델이 "이 에세이의 내용에 근거하여 저는 …점을 주겠습니다" 같은
  머리말로 응답을 시작하는 경향이 있다면, 머리말을 원하지 않는다고 명시하라** (5장,
  p.223).[^huyen2025]
- 하류가 걸려 있을 때 — **모델 출력이 특정 형식을 요구하는 하류 애플리케이션에 쓰일 때는 출력이 올바른
  형식인지 보장하는 것이 필수적이다. 모델이 JSON을 생성하기를 원한다면 JSON의 키가 무엇이어야 하는지
  지정하라. 필요하면 예시를 주라** (5장, p.223).[^huyen2025]
- 입력의 끝을 표시하는 마커 — **분류처럼 구조화 출력을 기대하는 과제에는 구조화 출력이 시작되어야
  한다는 것을 모델이 알도록 프롬프트의 끝을 표시하는 마커를 쓰라. 마커가 없으면 모델이 입력에 계속
  덧붙일 수 있다** (5장, p.223).[^huyen2025] 저자가 든 대비에서, 마지막 줄이 `chicken`으로 끝나는
  프롬프트에 모델은 `tacos --> edible`을 이어 붙였고, 마지막 줄을 `chicken -->`로 끝낸 프롬프트에는
  `edible`만 출력했다 (5장, p.223, Table 5-3).[^huyen2025]
  - 조심할 것 — **입력에 나타날 가능성이 낮은 마커를 고르도록 하라. 그러지 않으면 모델이 헷갈릴 수
    있다** (5장, p.223).[^huyen2025]
  - 각주가 상기시키는 근본 — **언어 모델은 그 자체로는 사용자가 제공한 입력과 자기 자신의 생성을
    구별하지 않는다는 것을 기억하라** (5장, p.223 각주 8).[^huyen2025] 그 성질의 자리는
    [언어 모델과 토큰](../concepts/language-models-and-tokens.md)이고, 형식을 강제하는 기법 전체는
    [구조화 출력](../concepts/structured-outputs.md)이 담는다.

## 이어지는 페이지

- [구조화 출력](../concepts/structured-outputs.md) — 프롬프팅 밖의 세 자리까지 포함한 형식 강제 기법
- [인컨텍스트 학습](../concepts/in-context-learning.md) — 예시가 학습으로 작동하는 기제
- [프롬프트에 맥락 주기](../concepts/providing-context-in-prompts.md) — 같은 절의 다음 관행
- [프롬프트 분해](../concepts/prompt-decomposition.md) — 지시가 복잡해질 때의 다음 수
- [사고 사슬 프롬프팅](../concepts/chain-of-thought-prompting.md) — 지시로 생각할 시간을 주는 관행
- [프롬프팅의 기본](../concepts/prompting-fundamentals.md) — 과제 서술이 프롬프트에서 차지하는 자리
- [지시 따르기 역량](../concepts/instruction-following-capability.md) — 지시가 좋아도 못 따르면
  소용없다는 전제

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 "Prompt Engineering
    Best Practices" 절의 도입(p.220)과 하위 절 "Write Clear and Explicit Instructions"(pp.220–223)을
    담았다. Table 5-1(클로드의 프롬프트 엔지니어링 튜토리얼에서 착안, p.222)은 원문 표기를 그대로
    옮기되 셀 안의 줄바꿈을 공백으로 이어 붙였다. Table 5-2(형식별 토큰 수, p.222)와 Table
    5-3(마커 유무, p.223)은 표 자체를 옮기는 대신 두 형식의 차이와 수치를 산문으로 옮겼다 — 원문
    셀은 여러 줄 프롬프트다. Figure 5-5(페르소나 요청 전후의 채점 화면, p.221)는 화면 갈무리라
    옮기지 않았고 프롬프트 문구와 두 점수만 담았다.
