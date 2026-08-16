---
type: concept
title: 함수 호출
description: 모델 제공자가 도구 사용을 지원하며 모델을 사실상 에이전트로 만드는 기전 — 도구는 함수이고 도구를 부르는 것이 함수 호출이라는 규정, 도구 목록을 선언하고 질의마다 쓸 도구를 지정하는 두 단계와 required·none·auto 설정, 모델이 어떤 도구를 어떤 파라미터로 부를지 스스로 생성한다는 것, 그리고 유효한 함수는 보장돼도 올바른 파라미터 값은 보장되지 않는다는 경계
status: draft
generated: { by: "claude-opus-5", at: "2026-08-16T17:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 함수 호출

- [도구는 함수다](#도구는-함수다)
- [두 단계](#두-단계)
- [저자가 든 의사 코드](#저자가-든-의사-코드)
- [무엇이 보장되고 무엇이 보장되지 않는가](#무엇이-보장되고-무엇이-보장되지-않는가)
- [응답의 모양](#응답의-모양)
- [저자가 붙인 경고](#저자가-붙인-경고)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델이 도구를 부르게 하려면 무엇을 선언하고 무엇을 넘겨받는가.**

## 도구는 함수다

- 규정 — **많은 모델 제공자가 자기 모델에 도구 사용을 제공하며, 이는 사실상 그 모델을 에이전트로
  만든다. 도구는 함수다. 따라서 도구를 호출하는 것은 흔히 함수 호출(function calling)이라 불린다.
  모델 API마다 작동 방식이 다르지만 일반적으로 함수 호출은 다음과 같이 작동한다** (6장,
  p.288).[^huyen2025]

## 두 단계

1. **도구 목록을 만든다(Create a tool inventory). 모델이 쓰기를 원할 만한 도구를 전부 선언한다. 각
   도구는 그 실행 진입점(예: 함수 이름)·파라미터·문서(예: 그 함수가 무엇을 하고 어떤 파라미터를
   필요로 하는가)로 서술된다** (6장, p.288).[^huyen2025]
2. **에이전트가 쓸 수 있는 도구를 지정한다(Specify what tools the agent can use). 질의마다 다른
   도구가 필요할 수 있으므로 많은 API가 선언된 도구 중 질의별로 쓸 목록을 지정하게 한다. 어떤 API는
   다음 설정으로 도구 사용을 더 통제하게 한다** (6장, p.288):[^huyen2025]
   - **`required` — 모델이 반드시 최소 하나의 도구를 써야 한다.**
   - **`none` — 모델이 어떤 도구도 쓰면 안 된다.**
   - **`auto` — 모델이 어떤 도구를 쓸지 결정한다.**

## 저자가 든 의사 코드

- **함수 호출은 Figure 6-10으로 예시된다. 이는 여러 API를 대표하도록 의사 코드로 쓰였다. 특정 API를
  쓰려면 그 문서를 참조하라** (6장, p.288).[^huyen2025] 원문 표기를 그대로 옮겼다 (6장, p.289,
  Figure 6-10 — 두 개의 단순한 도구를 쓰는 모델의 예):[^huyen2025]

  ```python
  def lbs_to_kg(lbs):
      return lbs * 0.45359237

  def ft_to_meters(ft):
      return ft * 0.3048

  lbs_to_kg_tool = FunctionDeclaration(
      name="lbs_to_kg",
      description="Convert from pounds to kilograms",
      parameters={
          "type": "object",
          "properties": {
              "lbs": {"type": "int", "description": "The value to be converted"}
          },
          "required": ["lbs"]
      },
  )

  ft_to_m_tool = FunctionDeclaration(name="ft_to_meters",...)

  messages = [{"role": "user", "content": [USER_QUERY]}]

  response = model_client.chat.completions.create(
      model=[MODEL_NAME],
      messages=messages,
      tools=[lbs_to_kg_tool, ft_to_m_tool],
      tool_choice="auto",
  )
  ```

  - 도판이 라벨로 가르는 부분 — **함수 정의(Tool definition), (1) 도구 서술(Tool description),
    사용자 질의(User query), (2) 이 질의가 쓸 수 있는 두 도구(This query can use two tools)** (6장,
    p.289, Figure 6-10).[^huyen2025]

## 무엇이 보장되고 무엇이 보장되지 않는가

- **질의가 주어지면 Figure 6-10처럼 정의된 에이전트는 어떤 도구를 쓸지와 그 파라미터를 자동으로
  생성한다. 어떤 함수 호출 API는 유효한 함수만 생성되도록 보장하지만, 올바른 파라미터 값은 보장할 수
  없을 것이다** (6장, p.289).[^huyen2025] 그 어긋남이 실패로 분류되는 자리는
  [에이전트의 실패 모드](../concepts/agent-failure-modes.md)에 있다.

## 응답의 모양

- 저자가 든 예 — **사용자 질의 "How many kilograms are 40 pounds?"가 주어지면 에이전트는 파라미터
  값 40 하나를 가진 도구 `lbs_to_kg_tool`이 필요하다고 결정할 수 있다** (6장, p.289).[^huyen2025]
  에이전트의 응답은 이렇게 보일 수 있다. 원문 표기를 그대로 옮겼다 (6장, p.289):[^huyen2025]

  ```python
  response = ModelResponse(
      finish_reason='tool_calls',
      message=chat.Message(
          content=None,
          role='assistant',
          tool_calls=[
              ToolCall(
                  function=Function(
                      arguments='{"lbs":40}',
                      name='lbs_to_kg'),
                  type='function')
          ])
  )
  ```

- 그다음 — **이 응답에서 함수 `lbs_to_kg(lbs=40)`을 불러내고 그 출력으로 사용자에게 줄 응답을 생성할
  수 있다** (6장, p.290).[^huyen2025]

## 저자가 붙인 경고

- **에이전트와 작업할 때는 언제나 시스템에게 함수 호출마다 어떤 파라미터 값을 쓰는지 보고하도록
  요청하라. 이 값들이 올바른지 점검하라** (6장, p.290).[^huyen2025]

## 이어지는 페이지

- [에이전트의 도구](../concepts/agent-tools.md) — 무엇을 도구로 줄지 정하는 쪽
- [계획 생성](../concepts/plan-generation.md) — 호출 시퀀스를 만드는 쪽
- [에이전트 계획](../concepts/agent-planning.md) — 검증된 계획이 이 호출로 넘어가는 자리
- [에이전트의 실패 모드](../concepts/agent-failure-modes.md) — 유효하지 않은 도구·파라미터의 실패
- [구조화 출력](../concepts/structured-outputs.md) — 모델 출력을 스키마에 맞추는 일반 문제
- [도구 선택](../concepts/agent-tool-selection.md) — 선언할 도구를 고르는 절차
- [에이전트란 무엇인가](../concepts/agents-defined.md) — 도구 사용이 에이전트를 규정하는 자리

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Plan generation" 항목
    안의 "Function calling" 하위 항목(pp.288–290)을 담았다. Figure 6-10(두 도구를 쓰는 모델의 의사
    코드, p.289)과 응답 예는 원문 표기를 그대로 옮기되, 도판이 세 상자로 나눠 조판한 코드를 하나의
    블록으로 이었고 상자 라벨은 따로 적었다. 코드 안의 생략 표시(`...`)도 원문 그대로다.
