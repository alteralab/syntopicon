---
type: concept
title: 지시 따르기 역량
description: 모델이 내가 준 지시를 얼마나 잘 따르는가를 재는 자리 — 지시를 못 따르면 지시가 아무리 좋아도 소용없다는 규정과 도메인 역량과 뒤섞이는 정의의 어려움, 자동 검증 가능한 지시로 좁힌 IFEval과 예/아니오 기준 목록으로 넓힌 INFOBench, 벤치마크가 놓치는 지시와 자기 벤치마크를 만들라는 조언, 그리고 실세계 지시의 큰 갈래인 롤플레잉과 그 평가
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 지시 따르기 역량

- [지시가 좋아도 못 따르면 소용없다](#지시가-좋아도-못-따르면-소용없다)
- [도메인 역량과 지시 따르기를 가르는 예](#도메인-역량과-지시-따르기를-가르는-예)
- [구조화 출력이 걸려 있다](#구조화-출력이-걸려-있다)
- [정의도 측정도 간단하지 않다](#정의도-측정도-간단하지-않다)
- [IFEval: 자동 검증 가능한 지시](#ifeval-자동-검증-가능한-지시)
- [INFOBench: 예·아니오 기준 목록](#infobench-예아니오-기준-목록)
- [벤치마크가 놓치는 지시](#벤치마크가-놓치는-지시)
- [롤플레잉](#롤플레잉)
- [롤플레잉을 어떻게 평가하는가](#롤플레잉을-어떻게-평가하는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델이 내가 준 지시를 따르는 능력을 그 자체로 어떻게 떼어 재는가.**

## 지시가 좋아도 못 따르면 소용없다

- 규정 — **지시 따르기 측정은 이 질문을 묻는다: 이 모델은 당신이 주는 지시를 따르는 데 얼마나 좋은가?
  모델이 지시를 따르는 데 나쁘면 당신의 지시가 아무리 좋아도 출력은 나쁠 것이다** (4장,
  p.172).[^huyen2025]
- 5장이 프롬프팅 쪽에서 같은 것을 전제로 세운다 — **프롬프팅이 통하려면 모델이 지시를 따를 수 있어야
  한다** (5장, pp.212–213).[^huyen2025] 그 자리는
  [프롬프팅의 기본](../concepts/prompting-fundamentals.md)이고, 같은 절이 견고성을 지시 따르기 역량과
  나란히 놓는다 — **모델의 견고성은 그 전반적 역량과 강하게 상관된다** (5장, p.213).[^huyen2025]
- 핵심 요건이다 — **지시를 따를 수 있는 것은 파운데이션 모델의 핵심 요건이며 대부분의 파운데이션 모델이
  그렇게 하도록 훈련된다. ChatGPT의 전신 InstructGPT는 지시를 따르도록 파인 튜닝되었기 때문에 그렇게
  이름 붙었다. 더 강력한 모델은 일반적으로 지시를 따르는 데 더 낫다. GPT-4는 대부분의 지시를 따르는 데
  GPT-3.5보다 낫고, 마찬가지로 Claude-v2는 대부분의 지시를 따르는 데 Claude-v1보다 낫다** (4장,
  p.172).[^huyen2025]

## 도메인 역량과 지시 따르기를 가르는 예

- 저자가 든 실물 — **모델에게 트윗의 감정을 탐지해 NEGATIVE·POSITIVE·NEUTRAL을 출력하라고 요청한다고
  하자. 모델은 각 트윗의 감정을 이해하는 것 같은데 HAPPY와 ANGRY 같은 기대하지 않은 출력을 생성한다.
  이는 모델이 트윗에 대해 감정 분석을 할 도메인 특화 역량은 갖고 있지만 그 지시 따르기 역량이 형편없다는
  뜻이다** (4장, p.172).[^huyen2025]

## 구조화 출력이 걸려 있다

- **지시 따르기 역량은 JSON 형식이나 정규 표현식 일치처럼 구조화 출력을 요구하는 애플리케이션에
  필수적이다. 예컨대 모델에게 입력을 A·B·C로 분류하라고 요청했는데 모델이 "That's correct"를 출력하면
  이 출력은 그다지 유용하지 않고 A·B·C만 기대하는 다운스트림 애플리케이션을 깨뜨릴 가능성이 높다** (4장,
  p.172).[^huyen2025]
  - 각주 — **구조화 출력은 2장에서 깊이 논의된다** (4장, p.172 각주 6).[^huyen2025]
- 구조화 출력이 전부는 아니다 — **그러나 지시 따르기 역량은 구조화 출력을 생성하는 것 이상이다. 모델에게
  최대 네 글자인 낱말만 쓰라고 요청하면 모델의 출력이 구조화될 필요는 없지만 최대 네 글자인 낱말만 담으라는
  지시는 여전히 따라야 한다. 아이들이 더 잘 읽게 돕는 스타트업 Ello는 아이가 이해할 수 있는 낱말만 써서
  이야기를 자동으로 생성하는 시스템을 만들고자 한다. 그들이 쓰는 모델은 제한된 낱말 풀로 작업하라는 지시를
  따를 능력이 필요하다** (4장, p.172).[^huyen2025]

## 정의도 측정도 간단하지 않다

- 뒤섞인다 — **지시 따르기 역량은 정의하거나 측정하기가 간단하지 않은데, 도메인 특화 역량이나 생성
  역량과 쉽게 뒤섞일 수 있기 때문이다. 모델에게 베트남 시 형식인 룩밧(lục bát)을 쓰라고 요청한다고
  상상해 보라. 모델이 그렇게 하는 데 실패하면 그것은 모델이 룩밧을 쓸 줄 몰라서일 수도 있고, 자기가
  무엇을 해야 하는지 이해하지 못해서일 수도 있다** (4장, p.173).[^huyen2025]
- 저자의 경고 상자 — **모델이 얼마나 잘 수행하는지는 그 지시의 품질에 달려 있고, 이는 AI 모델을 평가하기
  어렵게 만든다. 모델이 형편없이 수행할 때 그것은 모델이 나빠서일 수도 있고 지시가 나빠서일 수도
  있다** (4장, p.173).[^huyen2025]

## IFEval: 자동 검증 가능한 지시

- 두 벤치마크의 자리 — **서로 다른 벤치마크는 지시 따르기 역량이 무엇을 포괄하는지에 대해 서로 다른
  관념을 갖는다. 여기서 논의하는 두 벤치마크 IFEval과 INFOBench는 넓은 범위의 지시를 따르는 모델의
  역량을 재는데, 이는 당신의 지시를 따르는 모델의 능력을 어떻게 평가할지에 대한 아이디어를 줄 수 있다:
  어떤 기준을 쓸지, 평가 집합에 어떤 지시를 넣을지, 어떤 평가 방법이 적절한지** (4장,
  p.173).[^huyen2025]
- IFEval — **구글의 벤치마크 IFEval(Instruction-Following Evaluation)은 모델이 기대되는 형식을 따르는
  출력을 생산할 수 있는지에 초점을 맞춘다. Zhou et al.(2023)은 키워드 포함·길이 제약·불릿 개수·JSON
  형식처럼 자동으로 검증될 수 있는 25가지 유형의 지시를 식별했다. 모델에게 "ephemeral"이라는 낱말을 쓰는
  문장을 쓰라고 요청하면 출력이 이 낱말을 담는지 확인하는 프로그램을 쓸 수 있다. 따라서 이 지시는 자동으로
  검증 가능하다. 점수는 전체 지시 중 올바르게 따라진 지시의 비율이다** (4장, p.173).[^huyen2025]
- Zhou et al.이 제안한 자동 검증 가능한 지시들이다 (4장, pp.173–174, Table 4-2, IFEval 논문에서 가져온
  표로 CC BY 4.0 라이선스):[^huyen2025]

  | Instruction group | Instruction | Description |
  |---|---|---|
  | Keywords | Include keywords | Include keywords {keyword1}, {keyword2} in your response. |
  | Keywords | Keyword frequency | In your response, the word {word} should appear {N} times. |
  | Keywords | Forbidden words | Do not include keywords {forbidden words} in the response. |
  | Keywords | Letter frequency | In your response, the letter {letter} should appear {N} times. |
  | Language | Response language | Your ENTIRE response should be in {language}; no other language is allowed. |
  | Length constraints | Number paragraphs | Your response should contain {N} paragraphs. You separate paragraphs using the markdown divider: *** |
  | Length constraints | Number words | Answer with at least/around/at most {N} words. |
  | Length constraints | Number sentences | Answer with at least/around/at most {N} sentences. |
  | Length constraints | Number paragraphs + first word in i-th paragraph | There should be {N} paragraphs. Paragraphs and only paragraphs are separated from each other by two line breaks. The {i}-th paragraph must start with word {first_word}. |
  | Detectable content | Postscript | At the end of your response, please explicitly add a postscript starting with {postscript marker}. |
  | Detectable content | Number placeholder | The response must contain at least {N} placeholders represented by square brackets, such as {address}. |
  | Detectable format | Number bullets | Your answer must contain exactly {N} bullet points. Use the markdown bullet points such as: * This is a point. |
  | Detectable format | Title | Your answer must contain a title, wrapped in double angular brackets, such as <<poem of joy>>. |
  | Detectable format | Choose from | Answer with one of the following options: {options}. |
  | Detectable format | Minimum number highlighted section | Highlight at least {N} sections in your answer with markdown, i.e. *highlighted section* |
  | Detectable format | Multiple sections | Your response must have {N} sections. Mark the beginning of each section with {section_splitter} X. |
  | Detectable format | JSON format | Entire output should be wrapped in JSON format. |

## INFOBench: 예·아니오 기준 목록

- 더 넓은 관념 — **Qin et al.(2024)이 만든 INFOBench는 지시 따르기가 무엇을 뜻하는지에 대해 훨씬 넓은
  관점을 취한다. IFEval처럼 기대 형식을 따르는 모델의 능력을 평가하는 것에 더해, INFOBench는 내용
  제약("기후 변화만 논의하라" 같은)·언어 지침("빅토리아 시대 영어를 쓰라" 같은)·문체 규칙("정중한 어조를
  쓰라" 같은)을 따르는 모델의 능력도 평가한다. 그러나 이 확장된 지시 유형의 검증은 쉽게 자동화될 수 없다.
  모델에게 "젊은 청중에게 적합한 언어를 쓰라"고 지시하면 그 출력이 정말로 젊은 청중에게 적합한지를 어떻게
  자동으로 검증하겠는가?** (4장, p.174).[^huyen2025]
- 검증 방식 — **검증을 위해 INFOBench 저자들은 각 지시에 대한 기준 목록을 만들었고, 각 기준은 예/아니오
  질문으로 틀 지워졌다. 예컨대 "호텔 손님이 호텔 후기를 쓰는 것을 돕는 설문지를 만들라"는 지시에 대한
  출력은 세 개의 예/아니오 질문으로 검증될 수 있다** (4장, p.174):[^huyen2025]
  1. **생성된 텍스트가 설문지인가?**
  2. **생성된 설문지가 호텔 손님을 위해 설계되었는가?**
  3. **생성된 설문지가 호텔 손님이 호텔 후기를 쓰는 데 도움이 되는가?**
- 채점 — **모델의 출력이 그 지시에 대한 모든 기준을 충족하면 그 모델이 지시를 성공적으로 따랐다고 본다.
  이 예/아니오 질문 각각은 사람이나 AI 평가자가 답할 수 있다. 지시가 세 기준을 갖고 평가자가 모델의
  출력이 그중 둘을 충족한다고 판정하면 이 지시에 대한 모델의 점수는 2/3다. 이 벤치마크에서 모델의 최종
  점수는 모델이 맞힌 기준의 수를 모든 지시에 대한 기준의 총수로 나눈 것이다** (4장, p.175).[^huyen2025]
- 판정자에 대한 실험 결과 — **INFOBench 저자들은 자기 실험에서 GPT-4가 꽤 신뢰할 만하고 비용 효율적인
  평가자임을 발견했다. GPT-4는 인간 전문가만큼 정확하지는 않지만 Amazon Mechanical Turk로 모집한
  주석자보다는 더 정확하다. 그들은 자기 벤치마크가 AI 판정자로 자동 검증될 수 있다고 결론지었다** (4장,
  p.175).[^huyen2025]

## 벤치마크가 놓치는 지시

- 한계 — **IFEval과 INFOBench 같은 벤치마크는 서로 다른 모델이 지시를 따르는 데 얼마나 좋은지에 대한
  감을 주는 데 도움이 된다. 둘 다 실세계 지시를 대표하는 지시를 넣으려고 노력했지만 그들이 평가하는
  지시 집합은 서로 다르고, 흔히 쓰이는 많은 지시를 의심할 여지 없이 놓친다. 이 벤치마크에서 잘 수행하는
  모델이 당신의 지시에서도 반드시 잘 수행하지는 않을 수 있다** (4장, p.175).[^huyen2025]
  - 각주가 밝히는 공백 — **사람들이 파운데이션 모델을 어떤 지시에 쓰고 있는지의 분포에 대한 포괄적 연구는
    아직 많지 않다. LMSYS는 Chatbot Arena의 대화 100만 건에 대한 연구를 발표했지만 이 대화들은 실세계
    애플리케이션에 근거하지 않는다. 저자는 모델 제공자와 API 제공자의 연구를 기다리고 있다** (4장,
    p.175 각주 7).[^huyen2025]
- 저자의 조언 상자 — **당신 자신의 기준을 써서 당신의 지시를 따르는 모델의 역량을 평가할 자기 벤치마크를
  큐레이션해야 한다. 모델이 YAML을 출력해야 한다면 벤치마크에 YAML 지시를 넣어라. 모델이 "언어 모델로서"
  같은 말을 하지 않기를 원한다면 이 지시로 모델을 평가하라** (4장, p.175).[^huyen2025]

## 롤플레잉

- 두 목적 — **실세계 지시의 가장 흔한 유형 중 하나가 롤플레잉이다 — 모델에게 허구의 인물이나 페르소나를
  맡으라고 요청하는 것. 롤플레잉은 두 목적에 쓰일 수 있다: 사용자가 상호작용할 인물을 연기하는 것(대개
  게임이나 인터랙티브 스토리텔링 같은 오락용), 그리고 모델 출력의 품질을 개선하는 프롬프트 엔지니어링
  기법으로서의 롤플레잉이다** (4장, p.175).[^huyen2025]
- 얼마나 흔한가 — **LMSYS가 자기 Vicuna 데모와 Chatbot Arena의 대화 100만 건을 분석한 것(Zheng et
  al., 2023)은 롤플레잉이 여덟째로 흔한 유스케이스임을 보인다. 롤플레잉은 게임의 AI 기반
  NPC(non-playable characters)·AI 동반자·글쓰기 조수에 특히 중요하다** (4장, p.176, Figure
  4-4).[^huyen2025] 도판이 표시한 상위 10개 지시 유형과 그 비율이다 (4장, p.176, Figure
  4-4):[^huyen2025]

  | 순위 | 클러스터 | 비율 |
  |---|---|---|
  | 1 | Discussing software errors and solutions | 10.43% |
  | 2 | Inquiries about AI tools, software design, and programming | 7.29% |
  | 3 | Geography, travel, and global cultural inquiries | 6.96% |
  | 4 | Requests for summarizing and elaborating texts | 6.83% |
  | 5 | Creating and improving business strategies and products | 6.38% |
  | 6 | Requests for Python coding assistance and examples | 6.14% |
  | 7 | Requests for text summarizing, rewriting, and summarization | 6.06% |
  | 8 | Role-playing various characters in conversations | 5.83% |
  | 9 | Requests for explicit and erotic storytelling | 5.71% |
  | 10 | Answering questions based on passages | 5.59% |

## 롤플레잉을 어떻게 평가하는가

- 자동화가 어렵다 — **롤플레잉 역량 평가는 자동화하기 어렵다. 롤플레잉 역량을 평가하는 벤치마크에는
  RoleLLM(Wang et al., 2023)과 CharacterEval(Tu et al., 2024)이 있다. CharacterEval은 인간 주석자를
  쓰고 각 롤플레잉 측면을 5점 척도로 평가하도록 보상 모델을 훈련했다. RoleLLM은 유사도 점수(생성된 출력이
  기대 출력과 얼마나 비슷한가)와 AI 판정자를 모두 써서 페르소나를 흉내 내는 모델의 능력을 평가한다** (4장,
  p.176).[^huyen2025]
- 무엇을 확인해야 하는가 — **당신의 애플리케이션에서 AI가 어떤 역할을 맡기로 되어 있다면 당신의 모델이
  그 인물을 유지하는지 반드시 평가하라. 역할에 따라서는 모델의 출력을 평가할 휴리스틱을 만들 수 있다.
  예컨대 그 역할이 말수가 적은 사람이라면 휴리스틱은 모델 출력의 평균 길이일 수 있다. 그 외에 가장 쉬운
  자동 평가 접근은 AI 판정자다. 롤플레잉 AI는 문체와 지식 양쪽에서 평가해야 한다. 예컨대 모델이 성룡처럼
  말하기로 되어 있다면 그 출력은 성룡의 문체를 담아야 하고 성룡의 지식에 근거해 생성되어야 한다** (4장,
  p.176).[^huyen2025]
  - 각주가 붙이는 까다로운 부분 — **지식 부분이 까다로운데, 롤플레잉 모델이 성룡이 모르는 것을 말해서는
    안 되기 때문이다. 예컨대 성룡이 베트남어를 못 한다면 롤플레잉 모델이 베트남어를 하지 않는지 확인해야
    한다. 이 "부정 지식" 검사는 게임에 아주 중요하다. NPC가 실수로 플레이어에게 스포일러를 흘리는 것을
    원하지 않을 것이다** (4장, p.176 각주 8).[^huyen2025]
- 역할마다 프롬프트가 다르다 — **서로 다른 역할에 대한 AI 판정자는 서로 다른 프롬프트를 필요로 한다**
  (4장, p.176).[^huyen2025] 특정 역할을 연기하는 능력으로 모델의 순위를 매기려고 RoleLLM AI 판정자가
  쓰는 프롬프트의 앞부분이다 (4장, p.177):[^huyen2025]

  ```text
  System Instruction:
  You are a role-playing performance comparison assistant. You should rank
  the models based on the role characteristics and text quality of their
  responses. The rankings are then output using Python dictionaries and
  lists.

  User Prompt:
  The models below are to play the role of ``{role_name}''. The role
  description of ``{role_name}'' is ``{role_description_and_catchphra
  ses}''. I need to rank the following models based on the two criteria
  below.
  1. Which one has more pronounced role speaking style, and speaks more in
  line with the role description. The more distinctive the speaking style,
  the better.
  2. Which one's output contains more knowledge and memories related to the
  role; the richer, the better. (If the question contains reference
  answers, then the role-specific knowledge and memories are based on the
  reference answer.)
  ```

## 이어지는 페이지

- [평가 주도 개발](../concepts/evaluation-driven-development.md) — 이 갈래가 놓인 네 갈래의 틀
- [구조화 출력](../concepts/structured-outputs.md) — 지시 따르기가 형식으로 나타나는 쪽과 그 기법들
- [도메인 특화 역량 평가](../concepts/domain-specific-capability-evaluation.md) — 지시 따르기와
  뒤섞이는 쪽
- [AI 판정자](../concepts/ai-as-a-judge.md) — INFOBench와 RoleLLM이 기대는 판정 접근
- [참조 데이터 대비 유사도 측정](../concepts/similarity-measurements-against-reference-data.md) —
  RoleLLM이 판정자와 함께 쓰는 유사도 점수
- [공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md) — IFEval이 2024년
  리더보드 개편에 들어가는 자리
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — InstructGPT가 지시를 따르도록 훈련되는 쪽
- [비교 평가](../concepts/comparative-evaluation.md) — Chatbot Arena 대화가 나오는 자리
- [프롬프팅의 기본](../concepts/prompting-fundamentals.md) — 이 역량이 프롬프팅의 전제로 놓이는 자리
- [탈옥과 프롬프트 주입](../concepts/jailbreaking-and-prompt-injection.md) — 이 역량이 그대로 공격
  표면이 되는 자리

[^huyen2025]: Huyen 2025, 4장 "Evaluate AI Systems" (책 pp.159–210). 이 페이지는 "Evaluation
    Criteria" 절의 하위 절 "Instruction-Following Capability"(pp.172–177)와 그 아래
    "Instruction-following criteria"·"Roleplaying"을 담았다. Table 4-2는 원문 표기를 그대로 옮겼다
    (원문 각주: IFEval 논문에서 가져온 표이며 CC BY 4.0 라이선스). RoleLLM 판정자 프롬프트는 원문에
    실린 것을 그대로 옮겼고, 원문 조판의 줄바꿈(`catchphra ses`로 갈라진 것 포함)과 이중 백틱·이중
    작은따옴표 인용 부호도 그대로다. Figure 4-4(LMSYS 100만 대화의 상위 10개 클러스터 막대,
    p.176)는 막대에 비율이 인쇄돼 있어 라벨과 값을 표로 옮겼다. IFEval(Zhou et al., 2023)·
    INFOBench(Qin et al., 2024)·RoleLLM(Wang et al., 2023)·CharacterEval(Tu et al., 2024)·
    LMSYS(Zheng et al., 2023)·Ello는 huyen2025를 통한 전언이다. 프롬프팅 쪽 전제 두 줄은 5장
    "Prompt Engineering"의 "Introduction to Prompting"(책 pp.212–213)에서 왔다.
