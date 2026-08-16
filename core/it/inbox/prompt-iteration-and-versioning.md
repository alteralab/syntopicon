---
type: concept
title: 프롬프트 반복과 버전 관리
description: 프롬프트를 실험 대상이자 관리 대상 산출물로 다루는 법 — 모델을 알아 가며 프롬프트를 고쳐 가는 반복과 모델마다 다른 특이성, 체계적으로 시험하고 전체 시스템 맥락에서 평가하라는 규율, 프롬프트를 코드에서 떼어 파일로 두는 관행과 그 네 가지 이점, 그리고 git 버전 관리의 한계에서 나온 프롬프트 카탈로그
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 프롬프트 반복과 버전 관리

- [주고받으며 고쳐 간다](#주고받으며-고쳐-간다)
- [모델마다 특이성이 있다](#모델마다-특이성이-있다)
- [체계적으로 시험한다](#체계적으로-시험한다)
- [프롬프트를 코드에서 뗀다](#프롬프트를-코드에서-뗀다)
- [프롬프트에 메타데이터를 붙인다](#프롬프트에-메타데이터를-붙인다)
- [git 버전 관리의 한계와 프롬프트 카탈로그](#git-버전-관리의-한계와-프롬프트-카탈로그)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프롬프트를 한 번 쓰고 끝나는 문자열이 아니라 계속 고쳐지고 공유되는 산출물로 다루면
무엇이 필요해지는가.**

## 주고받으며 고쳐 간다

- **프롬프트 엔지니어링은 주고받음을 요구한다. 모델을 더 잘 이해하게 되면 프롬프트를 어떻게 쓸지에
  대해 더 나은 생각을 갖게 된다. 예컨대 모델에게 최고의 비디오 게임을 고르라고 요청하면 의견이
  갈리며 어떤 비디오 게임도 절대적으로 최고라고 여겨질 수 없다고 응답할 수 있다. 이 응답을 보고 나면
  의견이 갈리더라도 게임 하나를 고르라고 요청하도록 프롬프트를 수정할 수 있다** (5장,
  p.229).[^huyen2025]

## 모델마다 특이성이 있다

- **각 모델은 자기 특이성을 갖는다. 어떤 모델은 숫자를 이해하는 데 더 나을 수 있고 다른 모델은
  롤플레잉에 더 나을 수 있다. 어떤 모델은 시스템 지시를 프롬프트의 시작에 두는 것을 선호할 수 있고
  다른 모델은 끝에 두는 것을 선호할 수 있다** (5장, p.229).[^huyen2025]
- 그래서 무엇을 하는가 — **모델을 알아 가려면 이리저리 만져 보라. 서로 다른 프롬프트를 시도하라.
  모델 개발자가 제공하는 프롬프팅 안내서가 있다면 읽어라. 온라인에서 다른 사람들의 경험을 찾아보라.
  이용 가능한 플레이그라운드가 있다면 활용하라. 같은 프롬프트를 서로 다른 모델에 써서 그 응답이
  어떻게 다른지 보라 — 이는 당신의 모델에 대한 더 나은 이해를 줄 수 있다** (5장,
  p.229).[^huyen2025]

## 체계적으로 시험한다

- 규율 — **서로 다른 프롬프트로 실험할 때 변경을 체계적으로 시험하도록 하라. 프롬프트에 버전을
  매겨라. 실험 추적 도구를 써라. 서로 다른 프롬프트의 성능을 비교할 수 있도록 평가 지표와 평가
  데이터를 표준화하라** (5장, p.230).[^huyen2025]
- 어느 범위에서 평가할 것인가 (5장, p.230):[^huyen2025]

  > Evaluate each prompt in the context of the whole system. A prompt might improve the model's
  > performance on a subtask but worsen the whole system's performance.

## 프롬프트를 코드에서 뗀다

- 관행 — **프롬프트를 코드에서 분리하는 것이 좋은 관행이다. 예컨대 프롬프트를 `prompts.py` 파일에
  두고 모델 질의를 만들 때 이 프롬프트를 참조할 수 있다** (5장, p.233).[^huyen2025] 저자가 든
  모습이다 (5장, p.233):[^huyen2025]

  ```python
  file: prompts.py
  GPT4o_ENTITY_EXTRACTION_PROMPT = [YOUR PROMPT]

  file: application.py
  from prompts import GPT4o_ENTITY_EXTRACTION_PROMPT
  def query_openai(model_name, user_prompt):
      completion = client.chat.completions.create(
      model=model_name,
      messages=[
          {"role": "system", "content": GPT4o_ENTITY_EXTRACTION_PROMPT},
          {"role": "user", "content": user_prompt}
      ]
  )
  ```

- **이 접근은 몇 가지 이점을 갖는다** (5장, pp.233–234):[^huyen2025]
  - **재사용성(reusability) — 여러 애플리케이션이 같은 프롬프트를 재사용할 수 있다.**
  - **시험 가능성(testing) — 코드와 프롬프트를 따로 시험할 수 있다. 예컨대 코드를 서로 다른
    프롬프트로 시험할 수 있다.**
  - **가독성(readability) — 프롬프트를 코드에서 분리하면 둘 다 읽기 쉬워진다.**
  - **협업(collaboration) — 이는 주제 전문가가 코드에 정신을 빼앗기지 않고 프롬프트를 고안하는 데
    협력하고 도울 수 있게 한다.**

## 프롬프트에 메타데이터를 붙인다

- 왜 — **여러 애플리케이션에 걸쳐 프롬프트가 많다면, 어떤 프롬프트가 무슨 유스케이스를 위한 것인지
  알 수 있도록 각 프롬프트에 메타데이터를 주는 것이 유용하다. 모델·애플리케이션 등으로 프롬프트를
  검색할 수 있게 프롬프트를 조직하고 싶을 수도 있다** (5장, p.234).[^huyen2025] 저자는 각 프롬프트를
  파이썬 객체로 감싸는 모습을 들었는데, pydantic의 `BaseModel`을 상속한 `Prompt` 클래스가
  `model_name: str`·`date_created: datetime`·`prompt_text: str`·`application: str`·`creator: str`
  다섯 필드를 갖는 형태다 (5장, p.234).[^huyen2025]
- 템플릿에 더 담을 것 — **당신의 프롬프트 템플릿은 프롬프트가 어떻게 쓰여야 하는지에 대한 다른
  정보도 담을 수 있다** (5장, p.234):[^huyen2025]
  - **모델 엔드포인트 URL**
  - **온도나 top-p 같은 이상적인 샘플링 변수**
  - **입력 스키마**
  - **(구조화 출력을 위한) 기대 출력 스키마**
- 파일 형식도 나왔다 — **몇몇 도구가 프롬프트를 저장하기 위한 특별한 `.prompt` 파일 형식을 제안했다.
  구글 파이어베이스의 Dotprompt·Humanloop·Continue Dev·Promptfile을 보라** (5장,
  p.234).[^huyen2025] 저자가 실은 Dotprompt 파일 예는 `---`로 감싼 머리말에 `model:
  vertexai/gemini-1.5-flash`와 입력 스키마(`theme: string`), 출력 형식(`format: json`)과 출력
  스키마(`name: string`·`price: integer`·`ingredients(array): string`)를 두고, 그 아래 본문에
  `Generate a menu item that could be found at a {{theme}} themed restaurant.`라는 프롬프트를 두는
  형태다 (5장, p.234).[^huyen2025]

## git 버전 관리의 한계와 프롬프트 카탈로그

- git에 넣으면 — **프롬프트 파일이 당신의 git 저장소의 일부라면 이 프롬프트들은 git으로 버전 관리될
  수 있다. 이 접근의 단점은 여러 애플리케이션이 같은 프롬프트를 공유하는데 이 프롬프트가 갱신되면,
  이 프롬프트에 의존하는 모든 애플리케이션이 자동으로 이 새 프롬프트로 갱신하도록 강제된다는 것이다.
  다시 말해 프롬프트를 코드와 함께 git으로 버전 관리하면, 한 팀이 자기 애플리케이션에서 옛 버전의
  프롬프트에 머무르기를 선택하기가 아주 어렵다** (5장, pp.234–235).[^huyen2025]
- 그래서 카탈로그 — **많은 팀이 각 프롬프트에 명시적으로 버전을 매기는 별도의 프롬프트
  카탈로그(prompt catalog)를 써서 서로 다른 애플리케이션이 서로 다른 프롬프트 버전을 쓸 수 있게
  한다. 프롬프트 카탈로그는 각 프롬프트에 관련 메타데이터를 제공하고 프롬프트 검색을 허용해야 한다.
  잘 구현된 프롬프트 카탈로그는 어떤 프롬프트에 의존하는 애플리케이션을 추적하고 그 프롬프트의 더 새
  버전을 애플리케이션 소유자에게 알려 주기까지 할 수 있다** (5장, p.235).[^huyen2025]

## 이어지는 페이지

- [프롬프트 엔지니어링 도구](../concepts/prompt-engineering-tools.md) — 반복 자체를 자동화하려는 도구들
- [프롬프트 분해](../concepts/prompt-decomposition.md) — 관리 대상 프롬프트가 여럿이 되는 자리
- [시스템 프롬프트와 사용자 프롬프트](../concepts/system-prompt-and-user-prompt.md) — 모델의 채팅
  템플릿과 애플리케이션의 프롬프트 템플릿을 가르는 구분
- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 프롬프트 비교에 필요한 지표와
  데이터를 세우는 자리
- [샘플링 전략](../concepts/sampling-strategies.md) — 템플릿에 함께 적는 온도와 top-p
- [프롬프팅의 기본](../concepts/prompting-fundamentals.md) — 시스템 지시를 앞에 둘지 뒤에 둘지의 문제
- [버전 관리 실천](../concepts/version-control-practice.md) — 산출물에 버전을 매기는 일반 규율

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 "Iterate on Your
    Prompts" 절(pp.229–230)과 "Organize and Version Prompts" 절(pp.233–235)을 담았다. 두 절에는
    도판이 없다. `prompts.py`/`application.py` 예는 원문 표기를 그대로 옮겼다 — 한 블록 안에 `file:`
    라벨로 두 파일이 들어 있고 들여쓰기도 원문 그대로라 그대로는 실행되지 않는다. pydantic `Prompt`
    클래스와 Dotprompt 파일 예는 필드 구성만 산문으로 옮겼다. Dotprompt·Humanloop·Continue Dev·
    Promptfile은 huyen2025를 통한 전언이다.
