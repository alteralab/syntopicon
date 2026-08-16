---
type: concept
title: 시스템 프롬프트와 사용자 프롬프트
description: 프롬프트를 둘로 가르는 API 관례와 그 아래에서 실제로 일어나는 일 — 과제 서술과 과제라는 역할 분담, 모델마다 다르고 버전마다 바뀌는 채팅 템플릿과 그것을 틀리면 조용히 성능이 무너진다는 실측, 시스템 프롬프트가 성능을 올린다는 통설과 둘이 결국 하나로 이어 붙여진다는 사실, 그리고 그 차이를 훈련으로 만든 지시 계층
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 시스템 프롬프트와 사용자 프롬프트

- [무엇을 어디에 넣는가](#무엇을-어디에-넣는가)
- [채팅 템플릿](#채팅-템플릿)
- [템플릿을 틀리면 조용히 실패한다](#템플릿을-틀리면-조용히-실패한다)
- [시스템 프롬프트가 성능을 올린다는 통설](#시스템-프롬프트가-성능을-올린다는-통설)
- [지시 계층](#지시-계층)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프롬프트를 시스템과 사용자로 가르는 것은 모델 쪽에서 실제로 무엇을 바꾸는가.**

## 무엇을 어디에 넣는가

- 관례 — **많은 모델 API가 프롬프트를 시스템 프롬프트(system prompt)와 사용자 프롬프트(user
  prompt)로 가르는 선택지를 준다. 시스템 프롬프트를 과제 서술로, 사용자 프롬프트를 과제로 생각할 수
  있다** (5장, p.215).[^huyen2025]
- 저자가 든 실물 — **부동산 공시를 이해하도록 구매자를 돕는 챗봇을 짓고 싶다고 하자. 사용자는 공시를
  올리고 "지붕이 몇 년 되었나요?"나 "이 부동산의 특이한 점은 무엇인가요?" 같은 질문을 할 수 있다. 이
  챗봇이 부동산 중개인처럼 행동하기를 원한다. 이 롤플레잉 지시를 시스템 프롬프트에 넣고, 사용자의
  질문과 업로드된 공시는 사용자 프롬프트에 둘 수 있다** (5장, p.215).[^huyen2025] 그 프롬프트다
  (5장, p.215):[^huyen2025]

  > **System prompt:** You're an experienced real estate agent. Your job is to read each disclosure
  > carefully, fairly assess the condition of the property based on this disclosure, and help your
  > buyer understand the risks and opportunities of each property. For each question, answer
  > succinctly and professionally.
  >
  > **User prompt:** Context: [disclosure.pdf] / Question: Summarize the noise complaints, if any,
  > about this property. / Answer:

- 누구의 지시가 어디로 가는가 — **ChatGPT를 포함해 거의 모든 생성 AI 애플리케이션이 시스템 프롬프트를
  갖는다. 통상 애플리케이션 개발자가 제공하는 지시는 시스템 프롬프트에, 사용자가 제공하는 지시는
  사용자 프롬프트에 들어간다. 그러나 창의적으로 지시를 옮겨 다닐 수도 있다 — 전부를 시스템
  프롬프트에 넣거나 사용자 프롬프트에 넣는 것처럼. 어느 쪽이 가장 잘 통하는지 보려고 프롬프트를
  구조화하는 서로 다른 방식으로 실험할 수 있다** (5장, p.215).[^huyen2025]

## 채팅 템플릿

- 둘은 하나로 합쳐진다 — **시스템 프롬프트와 사용자 프롬프트가 주어지면 모델은 통상 템플릿을 따라
  둘을 단일 프롬프트로 결합한다** (5장, p.215).[^huyen2025] Llama 2 채팅 모델의 템플릿이다 (5장,
  pp.215–216):[^huyen2025]

  ```text
  <s>[INST] <<SYS>>
  {{ system_prompt }}
  <</SYS>>

  {{ user_message }} [/INST]
  ```

  - 채워 넣으면 그대로다 — **시스템 프롬프트가 "Translate the text below into French"이고 사용자
    프롬프트가 "How are you?"이면 Llama 2에 입력되는 최종 프롬프트는 위 템플릿의 두 자리에 각각 그
    문장이 들어간 것이다** (5장, p.216).[^huyen2025]
- 저자가 구분하라고 상자를 둔 것 — **이 절에서 논의하는 모델의 채팅 템플릿(chat template)은
  애플리케이션 개발자가 자기 프롬프트를 특정 데이터로 채우는(하이드레이트하는) 데 쓰는 프롬프트
  템플릿(prompt template)과 다르다. 모델의 채팅 템플릿은 모델 개발자가 정의하며 대개 모델 문서에서
  찾을 수 있다. 프롬프트 템플릿은 어떤 애플리케이션 개발자든 정의할 수 있다** (5장,
  p.216).[^huyen2025]
- 템플릿은 고정된 것이 아니다 — **서로 다른 모델은 서로 다른 채팅 템플릿을 쓴다. 같은 모델 제공자가
  모델 버전 사이에 템플릿을 바꿀 수도 있다. 예컨대 Llama 3 채팅 모델에서 메타는 템플릿을 바꿨다**
  (5장, p.216).[^huyen2025] Llama 3의 템플릿은 `<|begin_of_text|>` 뒤에
  `<|start_header_id|>system<|end_header_id|>`, 시스템 프롬프트, `<|eot_id|>`,
  `<|start_header_id|>user<|end_header_id|>`, 사용자 메시지, `<|eot_id|>`,
  `<|start_header_id|>assistant<|end_header_id|>`가 이어지는 형태다 (5장, p.216).[^huyen2025]
  - 왜 이 표기인가 — **`<|`와 `|>` 사이의 각 텍스트 스팬, 예컨대 `<|begin_of_text|>`와
    `<|start_header_id|>`는 모델에 의해 단일 토큰으로 취급된다** (5장, p.216).[^huyen2025]

## 템플릿을 틀리면 조용히 실패한다

- 증상 — **실수로 잘못된 템플릿을 쓰면 어리둥절한 성능 문제로 이어질 수 있다. 템플릿을 쓸 때의 작은
  실수, 예컨대 여분의 새 줄 하나도 모델이 자기 행동을 크게 바꾸게 할 수 있다** (5장,
  p.216).[^huyen2025]
  - 각주의 단서 — **보통 기대되는 채팅 템플릿에서 벗어나면 모델 성능이 저하된다. 그러나 흔하지는
    않지만 모델이 더 잘 수행하게 만들 수도 있다** (5장, p.216 각주 3).[^huyen2025]
- 저자가 제시한 관행 셋이다 (5장, p.217):[^huyen2025]
  1. **파운데이션 모델용 입력을 구성할 때 당신의 입력이 모델의 채팅 템플릿을 정확히 따르는지
     확인하라.**
  2. **프롬프트 구성에 서드파티 도구를 쓴다면 그 도구가 올바른 채팅 템플릿을 쓰는지 검증하라.
     불행히도 템플릿 오류는 아주 흔하다. 이 오류들은 조용한 실패를 일으키기 때문에 발견하기 어렵다 —
     템플릿이 틀려도 모델은 그럴듯한 무언가를 할 것이다.**
  3. **모델에 질의를 보내기 전에 최종 프롬프트를 출력해 기대 템플릿을 따르는지 다시 확인하라.**
  - 각주의 실측 — **깃허브와 레딧에 충분히 시간을 쓰면 보고된 채팅 템플릿 불일치 이슈를 많이 찾게
    된다. 저자는 파인 튜닝 문제를 디버깅하는 데 하루를 썼다가 자기가 쓴 라이브러리가 새 모델 버전용
    채팅 템플릿을 갱신하지 않았기 때문임을 알게 된 적이 있다** (5장, p.217 각주 4).[^huyen2025]
  - 또 다른 각주 — **사용자가 템플릿 실수를 하지 않도록 많은 모델 API는 사용자가 특수 템플릿 토큰을
    직접 쓰지 않아도 되게 설계되어 있다** (5장, p.217 각주 5).[^huyen2025]

## 시스템 프롬프트가 성능을 올린다는 통설

- 제공자 쪽 주장 — **많은 모델 제공자가 잘 만들어진 시스템 프롬프트가 성능을 개선할 수 있다고
  강조한다. 예컨대 앤트로픽 문서는 "시스템 프롬프트를 통해 클로드에게 특정 역할이나 성격을 부여하면
  대화 전체에 걸쳐 그 인물을 더 효과적으로 유지해, 배역을 지키면서 더 자연스럽고 창의적인 응답을
  보인다"고 말한다** (5장, p.217).[^huyen2025]
- 그러나 아래에서 벌어지는 일 (5장, p.217):[^huyen2025]

  > Under the hood, *the system prompt and the user prompt are concatenated into a single final
  > prompt before being fed into the model.* From the model's perspective, system prompts and user
  > prompts are processed the same way.

- 그렇다면 이득은 어디서 오는가 — **시스템 프롬프트가 줄 수 있는 성능 향상은 다음 두 요인 중 하나
  또는 둘 다 때문일 가능성이 높다** (5장, p.217):[^huyen2025]
  1. **시스템 프롬프트는 최종 프롬프트에서 먼저 오고, 모델은 먼저 오는 지시를 처리하는 데 그저 더
     나을 수 있다.**
  2. **모델이 시스템 프롬프트에 더 주의를 기울이도록 사후 훈련되었을 수 있다.**

## 지시 계층

- 둘째 요인의 출처 — **OpenAI 논문 "The Instruction Hierarchy: Training LLMs to Prioritize
  Privileged Instructions"(Wallace et al., 2024)에 공유된 것이다. 시스템 프롬프트를 우선하도록 모델을
  훈련하는 것은 프롬프트 공격을 완화하는 데도 도움이 된다** (5장, p.217).[^huyen2025] 그 계층이
  실제로 무엇인지는 [프롬프트 공격 방어](../concepts/defenses-against-prompt-attacks.md)가 담는다.

## 이어지는 페이지

- [프롬프팅의 기본](../concepts/prompting-fundamentals.md) — 프롬프트의 세 부분과 그 안에서 시스템·
  사용자가 놓이는 자리
- [프롬프트 공격 방어](../concepts/defenses-against-prompt-attacks.md) — 지시 계층이 방어로 쓰이는 자리
- [탈옥과 프롬프트 주입](../concepts/jailbreaking-and-prompt-injection.md) — 시스템과 사용자 지시가
  구분되지 않는다는 사실이 공격 표면이 되는 자리
- [프롬프트 반복과 버전 관리](../concepts/prompt-iteration-and-versioning.md) — 프롬프트 템플릿을
  코드에서 떼어 관리하는 쪽
- [프롬프트 엔지니어링 도구](../concepts/prompt-engineering-tools.md) — 서드파티 도구가 템플릿을
  틀리는 실물
- [지시 따르기 역량](../concepts/instruction-following-capability.md) — 롤플레잉 지시를 얼마나 잘
  유지하는지 재는 자리

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 "System Prompt and
    User Prompt" 절(pp.215–217)을 담았다. 이 절에는 도판이 없다. Llama 2 채팅 템플릿은 원문 표기를
    그대로 옮겼고, Llama 3 템플릿은 원문의 두 줄 조판을 토큰 나열로 풀어 인라인 코드로 옮겼다.
    부동산 챗봇 예의 사용자 프롬프트는 원문에서 세 줄(Context·Question·Answer)로 조판된 것을 인용
    블록 한 줄에 슬래시로 이어 옮겼다. 앤트로픽 문서 인용과 Wallace et al.(2024)은 huyen2025를 통한
    전언이다.
