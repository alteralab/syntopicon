---
type: concept
title: 모델 게이트웨이
description: 조직이 여러 모델과 하나의 인터페이스로 만나게 해 주는 중간 층 — 모델 API가 바뀌어도 게이트웨이만 고치면 되는 유지보수 이득, 조직 토큰을 나눠 주지 않는 접근 제어와 비용 관리, 요금 한도와 API 실패에 대비하는 폴백 정책, 요청이 이미 지나가는 자리라서 얹히는 로드 밸런싱·로깅·캐싱·가드레일, 그리고 기성 게이트웨이 목록
generated: { by: "claude-opus-5", at: "2026-08-17T09:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 모델 게이트웨이

- [무엇인가](#무엇인가)
- [가장 단순한 형태](#가장-단순한-형태)
- [접근 제어와 비용 관리](#접근-제어와-비용-관리)
- [폴백 정책](#폴백-정책)
- [요청이 지나가는 자리라서 얹히는 것들](#요청이-지나가는-자리라서-얹히는-것들)
- [기성품과 도구 게이트웨이](#기성품과-도구-게이트웨이)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **여러 모델을 쓰는 조직이 모델과 만나는 자리를 하나로 만들면 무엇이 달라지는가.**

## 무엇인가

- 정의 — **모델 게이트웨이(model gateway)는 당신의 조직이 서로 다른 모델과 통일되고 안전한 방식으로
  접속하게 해 주는 중간 층이다. 모델 게이트웨이의 가장 기본적인 기능은 자체 호스팅 모델과 상용 API 뒤의
  모델을 포함해 서로 다른 모델에 통일된 인터페이스를 제공하는 것이다. 모델 게이트웨이는 당신의 코드를
  유지보수하기 더 쉽게 만든다. 모델 API가 바뀌면 이 API에 의존하는 모든 애플리케이션을 갱신하는 대신
  게이트웨이만 갱신하면 된다** (10장, p.458).[^huyen2025] 도판은 고객 지원 챗봇·제품 리뷰 요약·
  텍스트-투-SQL 같은 애플리케이션들이 하나의 통일 API(Unified API)를 거쳐 자체 호스팅 모델·OpenAI
  API·구글 API로 갈라지는 모습을 그린다 (10장, p.458, Figure 10-6).[^huyen2025]

## 가장 단순한 형태

- **가장 단순한 형태에서 모델 게이트웨이는 통일된 래퍼다. 다음 코드 예는 모델 게이트웨이가 어떻게 구현될
  수 있는지 감을 준다. 그것은 어떤 오류 검사나 최적화도 담고 있지 않으므로 작동하도록 의도된 것이
  아니다** (10장, p.459):[^huyen2025]

  ```python
  import google.generativeai as genai
  import openai

  def openai_model(input_data, model_name, max_tokens):
      openai.api_key = os.environ["OPENAI_API_KEY"]
      response = openai.Completion.create(
          engine=model_name,
          prompt=input_data,
          max_tokens=max_tokens
      )
      return {"response": response.choices[0].text.strip()}

  def gemini_model(input_data, model_name, max_tokens):
      genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
      model = genai.GenerativeModel(model_name=model_name)
      response = model.generate_content(input_data, max_tokens=max_tokens)
      return {"response": response["choices"][0]["message"]["content"]}

  @app.route('/model', methods=['POST'])
  def model_gateway():
      data = request.get_json()
      model_type = data.get("model_type")
          model_name = data.get("model_name")
          input_data = data.get("input_data")
          max_tokens = data.get("max_tokens")

          if model_type == "openai":
              result = openai_model(input_data, model_name, max_tokens)
          elif model_type == "gemini":
              result = gemini_model(input_data, model_name, max_tokens)
          return jsonify(result)
  ```

## 접근 제어와 비용 관리

- **모델 게이트웨이는 접근 제어와 비용 관리(access control and cost management)를 제공한다. OpenAI
  API에 접근하려는 모두에게 당신의 조직 토큰 — 쉽게 새어 나갈 수 있는 — 을 주는 대신, 사람들에게 모델
  게이트웨이에만 접근을 허용해 중앙화되고 통제된 접근 지점을 만든다. 게이트웨이는 어떤 사용자나
  애플리케이션이 어떤 모델에 접근할 수 있어야 하는지 명세하는 세밀한 접근 제어도 구현할 수 있다. 나아가
  게이트웨이는 API 호출의 사용량을 모니터링하고 제한해, 남용을 막고 비용을 효과적으로 관리할 수 있다**
  (10장, p.459).[^huyen2025]

## 폴백 정책

- **모델 게이트웨이는 요금 한도나 API 실패(후자는 불행히도 흔하다)를 극복하기 위한 폴백 정책을 구현하는
  데도 쓰일 수 있다. 주 API가 이용 불가일 때 게이트웨이는 요청을 대체 모델로 라우팅하거나, 잠깐 기다린
  뒤 재시도하거나, 다른 방식으로 실패를 우아하게 처리할 수 있다. 이는 당신의 애플리케이션이 중단 없이
  매끄럽게 작동할 수 있게 보장한다** (10장, p.459).[^huyen2025]

## 요청이 지나가는 자리라서 얹히는 것들

- **요청과 응답이 이미 게이트웨이를 통해 흐르고 있으므로, 그것은 로드 밸런싱·로깅·분석 같은 다른 기능을
  구현하기에 좋은 자리다. 어떤 게이트웨이는 캐싱과 가드레일도 제공한다** (10장, p.460).[^huyen2025]
- 오케스트레이터와 겹치는 자리 — 각주가 짚는다: **이 때문에 어떤 오케스트레이터 도구는 게이트웨이가
  되고 싶어 한다. 사실 아주 많은 도구가 모든 것을 하는 종단 간 플랫폼이 되고 싶어 하는 것으로 보인다**
  (10장, p.472 각주 6).[^huyen2025]

## 기성품과 도구 게이트웨이

- **게이트웨이가 구현하기에 비교적 직관적이라는 점을 감안하면 기성 게이트웨이가 많다. 예로는 Portkey의
  AI Gateway, MLflow AI Gateway, Wealthsimple의 LLM Gateway, TrueFoundry, Kong, Cloudflare가
  있다** (10장, p.460).[^huyen2025]
- 아키텍처에서의 자리 — **우리 아키텍처에서 게이트웨이는 이제 모델 API 상자를 대체한다** (10장,
  p.460).[^huyen2025] 도판은 모델 게이트웨이 상자에 "모델 카탈로그, 접근 토큰 관리, …"라는 부제를
  붙이고 그 안에 Routing·Generation·Scoring을 둔다 (10장, p.460, Figure 10-7).[^huyen2025]
- 다루지 않은 형제 — **도구 게이트웨이(tool gateway) 같은 비슷한 추상 층도 폭넓은 도구에 접근하는 데
  유용할 수 있다. 집필 시점 기준 그것이 흔한 패턴이 아니어서 이 책에서는 논의하지 않는다** (10장,
  p.460).[^huyen2025]

## 이어지는 페이지

- [모델 라우터](../concepts/model-router.md) — 같은 단계의 앞쪽 절반
- [AI 애플리케이션 아키텍처의 단계적 확장](../concepts/ai-application-architecture-progression.md) —
  게이트웨이가 모델 API 상자를 대체하는 자리
- [AI 애플리케이션의 가드레일](../concepts/ai-application-guardrails.md) — 게이트웨이에 얹힐 수 있는
  기능
- [정확 캐싱과 의미 캐싱](../concepts/exact-and-semantic-caching.md) — 같이 얹히는 다른 기능
- [AI 파이프라인 오케스트레이션](../concepts/ai-pipeline-orchestration.md) — 게이트웨이와 경계가
  겹치는 층
- [모델 API와 자체 호스팅](../concepts/model-api-versus-self-hosting.md) — 게이트웨이가 감추는 두
  선택지
- [로그와 트레이스](../concepts/logs-and-traces.md) — 게이트웨이가 로깅을 맡을 때 남기는 것
- [서비스 발견과 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md) — 같은 기능이
  분산 시스템 축에서 서술되는 자리

[^huyen2025]: Huyen 2025, 10장 "AI Engineering Architecture and User Feedback" (책 pp.449–496).
    이 페이지는 "Step 3. Add Model Router and Gateway" 절의 하위 절 "Gateway"(pp.458–460)를 담았고,
    오케스트레이터와의 관계는 "AI Pipeline Orchestration" 절의 각주 6(p.472)에서 왔다. 코드는
    원문 표기를 그대로 옮겼다 — `model_gateway` 함수 본문의 두 번째 줄부터 들여쓰기가 한 단 더 들어가
    인쇄돼 있고 `import os`·`from flask import ...`가 없어 그대로는 돌지 않는데, 저자 자신이 "작동하도록
    의도된 것이 아니다"라고 적었으므로 없는 줄을 보태지 않았다. Figure 10-6·10-7은 상자 이름과 배치만
    옮겼다. Portkey AI Gateway·MLflow AI Gateway·Wealthsimple LLM Gateway·TrueFoundry·Kong·
    Cloudflare는 huyen2025를 통한 전언이다.
