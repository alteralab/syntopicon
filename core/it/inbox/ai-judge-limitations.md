---
type: concept
title: AI 판정자의 한계
description: AI로 AI를 평가하는 접근이 신뢰를 얻지 못하는 네 가지 이유 — 같은 판정자가 같은 입력에 다른 점수를 내는 비일관성과 일관성이 정확성이 아니라는 단서, 도구마다 뜻이 다른 faithfulness가 보여 주는 기준 모호성과 판정자가 바뀌면 지표가 무너진다는 문제, API 호출이 배로 느는 비용과 응답 전 판정이 더하는 지연, 그리고 자기 편향·첫 위치 편향·장황함 편향과 자기 편향이 자기인식에서 온다는 기제 쪽 설명
status: draft
generated: { by: "claude-opus-5", at: "2026-08-21T21:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: es2024-ragas, resource: /it/sources/es2024-ragas.md }
  - { id: kim2025-error-correlation, resource: /it/sources/kim2025-error-correlation.md }
  - { id: panickssery2024, resource: /it/sources/panickssery2024.md }
---

# AI 판정자의 한계

- [왜 주저하는가](#왜-주저하는가)
- [비일관성](#비일관성)
- [기준 모호성](#기준-모호성)
- [판정자가 바뀌면 지표가 무너진다](#판정자가-바뀌면-지표가-무너진다)
- [늘어난 비용과 지연](#늘어난-비용과-지연)
- [편향 셋](#편향-셋)
- [그럼에도 저자의 결론](#그럼에도-저자의-결론)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **AI 판정자의 점수를 벤치마크로 삼으려 할 때 무엇이 그것을 신뢰할 수 없게
만드는가.**

## 왜 주저하는가

- 네 가지 이유가 한 문단에 있다 — **AI 판정자의 많은 이점에도 많은 팀이 이 접근을 채택하기를
  주저한다. AI를 써서 AI를 평가하는 것은 동어반복처럼 보인다. AI의 확률적 성격은 그것이 평가자 노릇을
  하기에 너무 믿을 수 없어 보이게 만든다. AI 판정자는 애플리케이션에 사소하지 않은 비용과 지연을
  들일 수 있다. 이 한계들 때문에 어떤 팀은 AI 판정자를, 특히 프로덕션에서, 자기 시스템을 평가할 다른
  방법이 아무것도 없을 때의 대비책으로 본다** (3장, p.141).[^huyen2025]

## 비일관성

- 요구 조건과 그 위반 — **어떤 평가 방법이 믿을 만하려면 그 결과가 일관되어야 한다. 그러나 AI
  판정자는 모든 AI 애플리케이션과 마찬가지로 확률적이다. 같은 판정자가 같은 입력에 대해 다르게
  프롬프트되면 다른 점수를 낼 수 있다. 같은 판정자가 같은 지시로 프롬프트되었더라도 두 번 돌리면 다른
  점수를 낼 수 있다. 이 비일관성은 평가 결과를 재현하거나 신뢰하기 어렵게 만든다** (3장,
  p.142).[^huyen2025]
- 완화와 그 대가 — **AI 판정자를 더 일관되게 만드는 것은 가능하다. 2장이 샘플링 변수로 그렇게 하는
  법을 논의한다. Zheng et al.(2023)은 프롬프트에 평가 예시를 포함하는 것이 GPT-4의 일관성을 65%에서
  77.5%로 높일 수 있음을 보였다. 그러나 그들은 높은 일관성이 높은 정확성을 뜻하지는 않을 수 있음을
  인정했다 — 판정자가 일관되게 같은 실수를 저지를 수도 있다. 게다가 예시를 더 많이 포함하면 프롬프트가
  길어지고, 긴 프롬프트는 더 높은 추론 비용을 뜻한다. Zheng et al.의 실험에서 프롬프트에 더 많은 예시를
  포함한 것이 그들의 GPT-4 지출을 네 배로 만들었다** (3장, p.142).[^huyen2025]
- 위 표에 실린 도구 중 하나의 원전이 같은 문제를 자기 절로 인정한다 — **(큰) 언어 모델로 재현 가능한
  결과를 얻는 것은 어렵다. 그래서 프롬프트를 쓰는 신뢰할 만한 소프트웨어는 환각뿐 아니라, 같은
  실험을 같은 설정으로 여러 번 돌려도 다른 결과가 나올 수 있다는 사실도 고려해야 한다 — 예컨대
  밑에 깔린 API의 문서화되지 않은 변경 때문에, 또는 신경망에 내재한 무작위성 때문에** (5.1절,
  p.154).[^es2024-ragas]
  - 저자들이 쓴 완화책과 그 검증 — **우리는 LLM이 구조화된 JSON 형식으로 출력을 생성하도록
    요구한다. JSON 형식화의 효과를 재려고 JSON 형식화가 있을 때와 없을 때 연속 두 실행의 RAGAS
    점수 사이 상관을 측정했고, JSON 형식화 출력을 쓸 때 점수가 더 일관됨을 보았다** (5.1절,
    pp.154–155, Figure 1).[^es2024-ragas] 곧 비일관성의 완화책은 예시 추가만이 아니다 — 출력
    **형식**을 고정하는 것도 같은 축의 손잡이이며, 이쪽은 프롬프트를 길게 만들지 않는다.
    다만 원전은 상관의 수치를 본문에 적지 않고 도판으로만 보인다.

## 기준 모호성

- 표준이 없다 — **사람이 설계한 많은 지표와 달리 AI 판정자 지표는 표준화되어 있지 않아 오해하고
  오용하기 쉽다. 집필 시점 기준 오픈 소스 도구 MLflow·Ragas·LlamaIndex 모두 생성된 출력이 주어진 맥락에
  얼마나 충실한지를 재는 내장 기준 faithfulness를 갖고 있지만, 그 지시와 채점 체계는 모두 다르다.
  MLflow는 1에서 5까지의 채점 체계를 쓰고, Ragas는 0과 1을 쓰며, LlamaIndex의 프롬프트는 판정자에게
  YES와 NO를 출력하라고 요청한다** (3장, p.142).[^huyen2025]
- 같은 기준 이름에 붙은 서로 다른 기본 프롬프트다. 간결함을 위해 원문이 일부를 생략한 채 실었다
  (3장, pp.142–143, Table 3-4):[^huyen2025]

  | 도구 | 프롬프트(일부 생략) | 채점 체계 |
  |---|---|---|
  | MLflow | `Faithfulness is only evaluated with the provided output and provided context. please ignore the provided input entirely when scoring faithfulness. Faithfulness assesses how much of the provided output is factually consistent with the provided context.…` / `Faithfulness: Below are the details for different scores:` / `- Score 1: None of the claims in the output can be inferred from the provided context.` / `- Score 2: …` | 1–5 |
  | Ragas | `Your task is to judge the faithfulness of a series of statements based on a given context. For each statement you must return verdict as 1 if the statement can be verified based on the context or 0 if the statement can not be verified based on the context.` | 0 and 1 |
  | LlamaIndex | `Please tell if a given piece of information is supported by the context.` / `You need to answer with either YES or NO.` / `Answer YES if any of the context supports the information, even if most of the context is unrelated. Some examples are provided below.` / `Information: Apple pie is generally double-crusted.` / `Context: An apple pie is a fruit pie… It is generally double-crusted, with pastry both above and below the filling ...` / `Answer: YES` | YES and NO |

- 그래서 비교가 불가능하다 — **이 세 도구가 출력하는 faithfulness 점수는 비교될 수 없다. (맥락, 답)
  쌍이 주어졌을 때 MLflow가 faithfulness 점수 3을 주고, Ragas가 1을 출력하고, LlamaIndex가 NO를
  출력한다면 어느 점수를 쓰겠는가?** (3장, p.143).[^huyen2025]
- 표의 Ragas 행이 "0과 1"인 이유가 그 원전에 있다 — **각 진술 `s_i`에 대해 LLM이 그것이 맥락에서
  추론될 수 있는지 판정하고**, 최종 충실성 점수는 **지지된 진술 수를 전체 진술 수로 나눈 값**이다
  (3절, p.152).[^es2024-ragas] 곧 Ragas의 0/1은 **답 전체의 등급이 아니라 답을 쪼갠 진술 하나의
  판정**이고, 사용자가 보는 점수는 그 비율이다. 표의 세 도구는 채점 체계만 다른 것이 아니라 **무엇
  하나를 채점 단위로 삼는가**가 다르다 — MLflow는 출력 전체를 1–5로, LlamaIndex는 정보 하나를
  YES/NO로, Ragas는 진술마다 Yes/No를 받아 비율을 낸다.
  - 프롬프트 문구도 갈린다. 원전이 실은 검증 프롬프트는 **verdict (Yes/No)**를 요구하지만 (3절,
    p.152),[^es2024-ragas] huyen2025의 표에 실린 라이브러리 프롬프트는 **1 또는 0**을 요구한다
    (3장, p.142, Table 3-4).[^huyen2025] 논문의 프롬프트와 배포된 도구의 프롬프트가 같지 않다는
    뜻이며, 이것이 이 절의 문제를 한 겹 더한다 — 같은 이름의 지표가 도구마다 다를 뿐 아니라 **한
    도구 안에서도 논문과 코드가 다를 수 있다.**
  - 그 원전의 표기가 "Faithfulness"에 붙이는 정의다 (3절, p.152):[^es2024-ragas]

    > Faithfulness refers to the idea that the answer should be grounded in the given context.

## 판정자가 바뀌면 지표가 무너진다

- 지표의 존재 이유가 깨진다 — **애플리케이션은 시간에 따라 진화하지만 그것이 평가되는 방식은 이상적으로는
  고정되어야 한다. 그래야 평가 지표를 애플리케이션의 변화를 감시하는 데 쓸 수 있다. 그러나 AI 판정자도
  AI 애플리케이션이고, 이는 그것들도 시간에 따라 바뀔 수 있다는 뜻이다** (3장, p.143).[^huyen2025]
- 저자가 든 상황 — **지난달 애플리케이션의 일관성(coherence) 점수가 90%였고 이번 달 이 점수가 92%라고
  상상해 보라. 이는 애플리케이션의 일관성이 개선되었다는 뜻인가? 두 경우에 쓰인 AI 판정자가 정확히 같다는
  것을 확실히 알지 못하는 한 이 질문에 답하기 어렵다. 이번 달 판정자의 프롬프트가 지난달과 다르다면?
  살짝 더 잘 수행하는 프롬프트로 바꿨거나 동료가 지난달 프롬프트의 오타를 고쳤을 수 있고, 그래서 이번
  달 판정자가 더 관대할 수 있다** (3장, p.143).[^huyen2025]
- 팀이 나뉘면 더 나빠진다 — **애플리케이션과 AI 판정자를 서로 다른 팀이 관리하면 이는 특히 혼란스러워질
  수 있다. AI 판정자 팀이 애플리케이션 팀에 알리지 않고 판정자를 바꿀 수 있다. 그 결과 애플리케이션 팀은
  평가 결과의 변화를 판정자의 변화가 아니라 애플리케이션의 변화로 잘못 귀속시킬 수 있다** (3장,
  p.143).[^huyen2025]
- 저자의 조언 상자 (3장, p.143):[^huyen2025]

  > Do not trust any AI judge if you can't see the model and the prompt used for the judge.

- 시간이 필요한 문제 — **평가 방법이 표준화되는 데는 시간이 걸린다. 분야가 진화하고 더 많은 가드레일이
  도입되면서 미래의 AI 판정자가 훨씬 더 표준화되고 믿을 만해지기를 저자는 바란다** (3장,
  p.144).[^huyen2025]

## 늘어난 비용과 지연

- 어디에 쓰이는가 — **AI 판정자는 실험 중에도 프로덕션에서도 애플리케이션을 평가하는 데 쓸 수 있다. 많은
  팀이 위험을 줄이려고 AI 판정자를 프로덕션의 가드레일로 쓰며, AI 판정자가 좋다고 판단한 생성 응답만
  사용자에게 보여 준다** (3장, p.144).[^huyen2025]
- 비용의 배수 — **강력한 모델로 응답을 평가하는 것은 비쌀 수 있다. GPT-4를 응답 생성과 평가 양쪽에
  쓴다면 GPT-4 호출을 두 배로 하게 되어 API 비용이 대략 두 배가 된다. 전체 응답 품질·사실 일관성·독성이라는
  세 기준을 평가하고 싶어 평가 프롬프트가 셋이라면 API 호출 수가 네 배로 는다** (3장,
  p.144).[^huyen2025]
  - 각주 — **어떤 경우에는 평가가 예산의 대부분을, 응답 생성보다도 더 많이 차지할 수 있다** (3장,
    p.144 각주 17).[^huyen2025]
- 줄이는 두 방법 — **더 약한 모델을 판정자로 써서 비용을 줄일 수 있다. 스폿 체크(spot-checking),
  곧 응답의 부분집합만 평가하는 것으로도 비용을 줄일 수 있다. 스폿 체크는 어떤 실패를 잡지 못할 수도
  있다는 뜻이다. 평가하는 표본의 비율이 클수록 평가 결과에 대한 확신이 커지지만 비용도 높아진다. 비용과
  확신 사이의 올바른 균형을 찾는 데는 시행착오가 필요할 수 있다** (3장, p.144).[^huyen2025]
  - 각주 — **스폿 체크는 샘플링과 같다** (3장, p.144 각주 18).[^huyen2025]
  - **모든 것을 감안하면 AI 판정자는 사람 평가자보다 훨씬 싸다** (3장, p.144).[^huyen2025]
- 지연 — **프로덕션 파이프라인에 AI 판정자를 구현하면 지연이 더해질 수 있다. 응답을 사용자에게 돌려주기
  전에 평가한다면 트레이드오프에 맞닥뜨린다: 줄어든 위험과 늘어난 지연. 더해진 지연은 엄격한 지연 요구가
  있는 애플리케이션에서는 이 선택지를 아예 성립하지 않게 만들 수 있다** (3장, p.144).[^huyen2025]

## 편향 셋

- 전제 — **사람 평가자에게 편향이 있듯 AI 판정자에게도 있다. 서로 다른 AI 판정자는 서로 다른 편향을
  갖는다. 자기 AI 판정자의 편향을 인식하는 것은 그 점수를 올바르게 해석하고 나아가 그 편향을 완화하는
  데 도움이 된다** (3장, p.144).[^huyen2025]
- 자기 편향 — **AI 판정자는 자기 편향(self-bias)을 갖는 경향이 있는데, 모델이 다른 모델이 생성한 응답보다
  자기 응답을 선호하는 것이다. 모델이 생성할 가장 그럴듯한 응답을 계산하도록 돕는 바로 그 기제가 이
  응답에 높은 점수도 준다. Zheng et al.의 2023년 실험에서 GPT-4는 자기 자신을 10% 높은 승률로,
  Claude-v1은 자기 자신을 25% 높은 승률로 선호한다** (3장, pp.144–145).[^huyen2025]
- **자기 편향의 기제를 실험으로 파고든 원전이 따로 있다** — 자기 출력을 알아보는 능력
  (self-recognition)을 파인튜닝으로 올리면 자기 출력을 선호하는 정도(self-preference)가
  같은 선 위를 따라 함께 오른다. 저자들은 역인과와 교란 변수를 각각 배제하는 실험을
  덧붙이지만, 그것을 인과의 **초기 증거**라고만 부르고 확정하지 않는다 (§3·§5.3).[^panickssery2024]
  - **자기 편향이 실제 품질 차이보다 크다는 것도 같은 원전이 사람 주석으로 쟀다** —
    같은 모델 쌍을 사람이 판정했을 때의 격차보다 판정자가 자기에게 준 선호가 더
    컸다 (§2.5).[^panickssery2024] 곧 위 huyen2025의 "사람 주석자는 동등한 품질로
    판단하는데"라는 전제가 이 원전에서 측정으로 확인된 셈이다.
  - 위 huyen2025의 설명("가장 그럴듯한 응답을 계산하는 바로 그 기제가 높은 점수도
    준다")과 이 원전의 가설은 **같은 것이 아니다.** 앞은 생성 확률이 곧 점수라는
    설명이고, 뒤는 자기 것임을 **알아보는 것**이 선호를 낳는다는 설명이다. 뒤쪽이
    맞다면 처방이 달라진다 — 원전이 조건부로 권하는 대응은 판정자 교체가 아니라
    **저자 은닉(authorship obfuscation)**이다 (§5.1).[^panickssery2024]
  - 측정 설계와 수치, 그리고 저자들이 넘지 않은 선은
    [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md)에 있다.
    그 페이지의 값은 2024년의 모델 세대와 뉴스 요약 과제에 묶여 있다.
- **자기 편향은 같은 벤더의 다른 모델에까지 걸린다** — 판정자를 근거 진리 대신 써서 다른 모델을
  채점시키면, 판정자는 자기보다 정확도가 낮은 모델의 정확도를 체계적으로 부풀리고 자기보다 정확한
  모델의 정확도는 깎는다. 기제는 관대함이 아니라 **오류 상관(correlated errors)**이다 — 판정자와
  대상이 같은 오답을 고르면 그 문항이 정답으로 집계되고, 반대로 판정자가 틀린 문항에서는 대상이
  맞혀도 점수를 줄 수 없다. 그리고 부풀림은 **같은 벤더·같은 계열의 모델에서 더 크다**. 저자들은
  이것을 자기 선호(self-preferencing)가 같은 계열의 다른 모델 사이에서도 일어날 수 있다는 뜻으로
  읽는다 (§4, Figure 2·8).[^kim2025-error-correlation]
  - 처방 — 판정자를 바꿔서 푸는 문제가 아니라 **모델과 판정자의 쌍마다 근거 진리 자료로 오류
    지표를 보정해야 하는** 문제다 (§4).[^kim2025-error-correlation]
- 첫 위치 편향 — **많은 AI 모델이 첫 위치 편향(first-position bias)을 갖는다. AI 판정자는 쌍 비교에서
  첫 번째 답을, 또는 선택지 목록에서 첫 번째 것을 선호할 수 있다. 이는 서로 다른 순서로 같은 테스트를
  여러 번 반복하거나 정성껏 만든 프롬프트로 완화할 수 있다. AI의 위치 편향은 사람의 그것과 반대다.
  사람은 마지막에 본 답을 선호하는 경향이 있고 이를 최신 편향(recency bias)이라 부른다** (3장,
  p.145).[^huyen2025]
- 장황함 편향 — **어떤 AI 판정자는 장황함 편향(verbosity bias)을 갖는데, 품질과 무관하게 더 긴 답을
  선호하는 것이다. Wu와 Aji(2023)는 GPT-4와 Claude-1 둘 다 짧고 올바른 응답(낱말 약 50개)보다 사실
  오류가 있는 더 긴 응답(낱말 약 100개)을 선호한다는 것을 발견했다. Saito et al.(2023)은 창의적 과제에
  대해 이 편향을 연구해, 길이 차이가 충분히 클 때(예컨대 한 응답이 다른 응답의 두 배 길이일 때) 판정자가
  거의 언제나 더 긴 쪽을 선호한다는 것을 발견했다** (3장, p.145).[^huyen2025]
  - 각주 — **Saito et al.(2023)은 사람도 더 긴 응답을 선호하는 경향이 있지만 그 정도는 훨씬 덜하다는
    것을 발견했다** (3장, p.145 각주 19).[^huyen2025]
  - 사라질 수도 있다 — **그러나 Zheng et al.(2023)과 Saito et al.(2023) 둘 다 GPT-4가 GPT-3.5보다 이
    편향에 덜 취약함을 발견했는데, 이는 모델이 강해지면서 이 편향이 사라질 수도 있음을 시사한다** (3장,
    p.145).[^huyen2025]
- 편향 밖의 한계 — **이 모든 편향에 더해 AI 판정자는 프라이버시와 지식 재산권을 포함해 모든 AI
  애플리케이션과 같은 한계를 갖는다. 독점 모델을 판정자로 쓴다면 자기 데이터를 이 모델에 보내야 한다.
  모델 제공자가 자기 훈련 데이터를 공개하지 않으면 그 판정자가 상업적으로 안전하게 쓸 수 있는지 확실히
  알 수 없다** (3장, p.145).[^huyen2025]

## 그럼에도 저자의 결론

- **AI 판정자 접근의 한계에도 그 많은 이점 때문에 저자는 그 채택이 계속 늘 것이라고 믿는다. 그러나 AI
  판정자는 정확 평가 방법이나 사람 평가로, 또는 둘 다로 보완되어야 한다** (3장, p.145).[^huyen2025]

## 이어지는 페이지

- [AI 판정자](../concepts/ai-as-a-judge.md) — 이 한계가 붙는 접근 자체와 "판정자 = 모델 + 프롬프트"라는
  규정
- [판정자 모델 고르기](../concepts/ai-judge-selection.md) — 비용을 줄이려 약한 판정자를 쓰는 선택과
  자기 편향이 자기 평가에 걸리는 자리
- [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md) — 위 자기 편향이
  왜 생기는가의 기제 쪽. 자기 출력을 알아보는 능력을 손잡이로 써서 인과를 세우려 한 설계와,
  저자들이 인과를 확정하지 않고 남긴 선
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md) — 위 자기 편향이 같은
  벤더의 다른 모델로 번지는 기제와 그 실측
- [비교 평가](../concepts/comparative-evaluation.md) — 첫 위치 편향이 실제로 쌍 비교에서 작동하는 자리
- [기능적 정확성](../concepts/functional-correctness.md) — AI 판정자를 보완할 정확 평가 쪽
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 비일관성의 출처와 그 완화책
- [샘플링 전략](../concepts/sampling-strategies.md) — 판정자를 더 일관되게 만드는 변수들
- [파운데이션 모델 평가의 난제](../concepts/evaluating-foundation-models-challenges.md) — 평가 방법이
  표준화되지 않은 배경
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — Ragas의 세 지표가 정의되는 자리

[^es2024-ragas]: Es et al. 2024, "RAGAs: Automated Evaluation of Retrieval Augmented Generation",
    EACL 2024 **System Demonstrations**, pp.150–158. 본 학회 트랙이 아니라 시연 트랙이므로
    심사가 가볍다 — 이 페이지의 claim은 그 조건에서 읽는다. 쪽 번호는 학회 논문집 인쇄 쪽이다.
    이 페이지는 3절 Evaluation Strategies의 충실성 정의·계산과 5.1절 Reproducibility만 담았다 —
    지표 전체와 실험은 [검색 품질 평가](../concepts/retrieval-evaluation.md)가 담는다.
    Figure 1(JSON 형식 유무별 점수 일관성 산점도, p.155)은 옮기지 않았고 본문이 서술한 결론만
    담았다 — 원문이 상관 계수를 본문에 적지 않아 수치는 옮길 것이 없다.

[^huyen2025]: Huyen 2025, 3장 "Evaluation Methodology" (책 pp.113–158). 이 페이지는 "AI as a Judge"
    절의 하위 절 "Limitations of AI as a Judge"(pp.141–145)를 담았다. Table 3-4의 프롬프트는 원문이
    "partially omitted for brevity"라고 밝힌 발췌를 그대로 옮겼다. Zheng et al.(2023)·Wu와
    Aji(2023)·Saito et al.(2023)·MLflow·LlamaIndex는 huyen2025를 통한 전언이다. Ragas에 대한
    전언은 위 원전 각주로 이중화했다.

[^kim2025-error-correlation]: Kim, Garg, Peng & Garg 2025, "Correlated Errors in Large
    Language Models", ICML 2025 본회의(PMLR 267). 이 페이지는 §4의 판정자 사례 연구와 그
    바탕이 되는 §3.2의 방향만 담았다 — 오류 상관 자체의 수치와 분모·표 위치는
    [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md)에 있다.

[^panickssery2024]: Panickssery, Bowman & Feng 2024, "LLM Evaluators Recognize and Favor
    Their Own Generations", NeurIPS 2024 본회의(게재본 1쪽 푸터가 문면 근거). 이 페이지는
    그 소스에서 수치를 옮기지 않고 방향과 설계만 옮겼다 — 수치와 그것에 붙는 모델·과제
    조건은 [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md)에
    있고, 프리프린트와 게재본이 갈리는 자리는
    [소스 메타](../sources/panickssery2024.md)에 있다.
