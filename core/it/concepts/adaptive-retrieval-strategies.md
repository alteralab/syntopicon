---
type: concept
title: 적응형 검색 전략
description: 검색을 탈지, 언제 탈지를 누가 정하는가 — 질의 복잡도로 생성 전에 고르는 사전 라우팅(Adaptive-RAG), 생성 도중 문장마다 정하는 능동 검색(FLARE·DRAGIN), 모델 자신이 특수 토큰으로 정하는 내장 판단(Self-RAG)의 세 갈래와, 훈련 데이터·반복 호출·모델 훈련이라는 서로 다른 자리에 붙는 대가
generated: { by: "claude-fable-5", at: "2026-08-17T18:30:00Z" }
sources:
  - { id: jeong2024-adaptiverag, resource: /it/sources/jeong2024-adaptiverag.md }
  - { id: jiang2023-flare, resource: /it/sources/jiang2023-flare.md }
  - { id: su2024-dragin, resource: /it/sources/su2024-dragin.md }
  - { id: asai2024-selfrag, resource: /it/sources/asai2024-selfrag.md }
---

# 적응형 검색 전략

- [검색을 언제 탈지 정하는 세 갈래](#검색을-언제-탈지-정하는-세-갈래)
- [사전 라우팅 — 질의 복잡도로 미리 고르기](#사전-라우팅--질의-복잡도로-미리-고르기)
- [생성 중 결정 — FLARE와 DRAGIN](#생성-중-결정--flare와-dragin)
- [세 갈래의 대가는 서로 다른 자리에 붙는다](#세-갈래의-대가는-서로-다른-자리에-붙는다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **검색을 탈지, 언제 탈지를 누가 어떻게 정하는가.**

## 검색을 언제 탈지 정하는 세 갈래

- [검색 증강 생성](../concepts/retrieval-augmented-generation.md)이 담은 Self-RAG는 **그 결정을 훈련으로
  모델 안에 넣은** 갈래다. 결정을 모델 밖으로 빼는 갈래가 둘
  더 있고, 셋은 **결정이 내려지는 시점**이 다르다 — 질의를 보고 생성 전에 정하는 사전
  라우팅(Adaptive-RAG), 생성하는 도중 문장마다 정하는 능동 검색(FLARE·DRAGIN), 그리고 모델 자신이
  특수 토큰으로 정하는 내장 판단(Self-RAG).
- 사전 라우팅 쪽은 내장 판단 쪽을 명시적으로 겨눈다 — **하나의 모델에 기대는 적응형 검색 방법들은
  다양한 복잡도의 질의를 다루는 데 차선일 수 있다. 모든 입력 질의에 대해 지나치게 단순하거나 지나치게
  복잡한 쪽으로 기울기 때문이며, 이는 질의 복잡도에 맞춰 검색 증강 LLM의 가장 알맞은 전략을 고를 수
  있는 새 접근을 요구한다** (2절, p.3).[^jeong2024-adaptiverag] 저자들은 Self-RAG를 자기 작업과
  동시대(concurrent)로 분류한다 (2절, p.3).[^jeong2024-adaptiverag]
- 능동 검색 쪽은 다른 결을 겨눈다 — **대부분의 기존 검색 증강 LM은 입력에 근거해 한 번만 검색하는
  retrieve-and-generate 구성을 쓴다. 그러나 이는 긴 텍스트를 생성하는 더 일반적인 상황에서 제약이
  되는데, 그런 상황에서는 생성 과정 내내 정보를 계속 모으는 것이 필수적이기 때문이다** (초록,
  p.1).[^jiang2023-flare] 곧 사전 라우팅이 "이 질의에 검색이 몇 번 필요한가"를 묻는다면 능동 검색은
  "이 문장을 쓰는 지금 검색이 필요한가"를 묻는다. 두 축(**언제** 검색하고 **무엇으로** 검색하는가)이
  아래에서 따로 다뤄진다.

## 사전 라우팅 — 질의 복잡도로 미리 고르기

- 진단 — **다양한 복잡도의 질의를 다루는 여러 접근이 있지만, 그것들은 단순한 질의를 불필요한 계산
  부담으로 처리하거나 복잡한 다단계 질의를 충분히 다루지 못한다. 그런데 모든 사용자 요청이 단순이나
  복잡 한쪽에만 떨어지는 것은 아니다** (초록, p.1).[^jeong2024-adaptiverag]
- 이 갈래의 정의다. 원문 표기를 그대로 옮겼다 (초록, p.1):[^jeong2024-adaptiverag]

  > we propose a novel adaptive QA framework that can dynamically select the most suitable strategy
  > for (retrieval-augmented) LLMs from the simplest to the most sophisticated ones based on the
  > query complexity.
- 3단 라우팅 — **분류기는 세 부류를 낸다. 'A'는 질의가 직설적이어서 `LLM(q)` 자체로 답할 수 있음을,
  'B'는 적어도 단발 접근 `LLM(q, d)`가 필요한 중간 복잡도임을, 'C'는 가장 광범위한 해법
  `LLM(q, d, c)`를 요구하는 복잡한 질의임을 가리킨다** (3.2절, p.5).[^jeong2024-adaptiverag]
  분류기는 **질의 복잡도를 예측하도록 훈련된 더 작은 언어 모델**이며 실험에서는 T5-Large를 썼다
  (3.2절, p.5; 4.4절, p.6).[^jeong2024-adaptiverag]
- 라벨을 사람이 달지 않는다 — **질의–복잡도 쌍의 주석 데이터셋이 없으므로 두 전략으로 훈련 데이터를
  자동 구성한다. ⑴ 세 전략의 실제 예측 결과로 라벨을 붙이되, 동점은 더 단순한 모델에 우선권을 준다
  ⑵ 세 접근이 모두 실패해 라벨이 붙지 않은 질의에는 데이터셋의 귀납 편향을 쓴다 — 단일홉 데이터셋의
  질의에 'B'를, 다중홉 데이터셋의 질의에 'C'를 준다** (3.2절, p.5).[^jeong2024-adaptiverag]
  - 저자들이 스스로 좁힌 범위 — **이 라벨링 과정은 질의 복잡도를 라벨링하는 하나의 특정 사례이며,
    효과적이긴 하나 질의를 잘못 라벨링할 가능성이 있다** (Limitations, p.9).[^jeong2024-adaptiverag]
- 비용이 실측된다. 라우팅이 사는 근거가 이 표다. 원문 표기를 그대로 옮겼다 (5절, p.8,
  Table 3):[^jeong2024-adaptiverag]

  | Labels | Time/Query (Sec.) | Percentage (%) |
  |---|---|---|
  | No (A) | 0.35 | 8.60 |
  | One (B) | 3.08 | 53.33 |
  | Multi (C) | 27.18 | 38.07 |

  - 읽는 법 — 가장 비싼 갈래가 가장 싼 갈래의 **약 78배**이고 질의의 38%만 그리로 간다. 곧 이 설계가
    아끼는 것은 평균이 아니라 **꼬리**다.
  - 라우터는 작아도 된다 — **다양한 크기의 분류기 사이에 유의미한 성능 차이가 관측되지 않으며, 더
    작은 분류기의 줄어든 복잡도와 적은 파라미터에서도 그렇다** (5절, p.8; Table 6은
    p.9).[^jeong2024-adaptiverag] 실제로 Small(60M)의 F1 45.83과 Large(770M)의 46.94 사이가 그 폭이다.

## 생성 중 결정 — FLARE와 DRAGIN

- 이 갈래의 정의다. 원문 표기를 그대로 옮겼다 (초록, p.1):[^jiang2023-flare]

  > In this work, we provide a generalized view of *active retrieval augmented generation*, methods
  > that actively decide when and what to retrieve across the course of the generation.

- FLARE의 기제 — **단계 `t`에서 먼저 검색된 문서에 근거하지 않은 임시 다음 문장을 생성한다. LM이 그
  문장에 확신이 있으면 검색 없이 받아들이고, 아니면 그 문장으로 검색 질의를 만들어 문서를 가져온 뒤
  다음 문장을 다시 생성한다. LM이 잘 보정되어 있어 낮은 확률·확신이 흔히 지식의 부재를 가리킨다는
  점에 기대어, 임시 문장의 어떤 토큰이든 확률이 문턱 `θ`보다 낮으면 검색을 발동한다. `θ = 0`은 검색이
  결코 발동되지 않음을, `θ = 1`은 문장마다 발동됨을 뜻한다** (3.2.1절, p.4).[^jiang2023-flare]
  - 왜 **다음** 문장인가 — **검색 질의는 미래 생성의 의도를 반영해야 한다** (3절, p.3)는 것이 전제이고,
    직전 문장으로 검색하는 것과의 정면 비교에서 2WikiMultihopQA EM이 39.0 대 48.8로 갈린다 (6.2절,
    p.8, Table 3).[^jiang2023-flare] 다만 그 문장을 질의로 **그대로** 쓰지는 않는다 — 저확신 토큰을
    가리거나 그 자리를 겨냥한 질문을 생성한다 (3.2.2절, pp.4–5).[^jiang2023-flare] 질의를 만드는
    쪽의 세 방법은 [쿼리 재작성](../concepts/query-rewriting.md)이 담는다.
- 얼마나 자주 발동해야 하는가 — **2WikiMultihopQA에서는 검색 비율이 60%를 넘으면 성능이 평평해지고,
  StrategyQA에서는 50%를 넘으면 오히려 떨어진다 — 불필요한 검색이 잡음을 들여와 원래 생성 과정을
  방해할 수 있음을 가리킨다. 과제·데이터셋을 가로질러 문장의 40–80%에서 검색을 발동하는 것이 통상
  좋은 성능으로 이어진다** (6.2절, p.8, Figure 5).[^jiang2023-flare] Self-RAG의 문턱 실험이 낸
  "최적점은 과제마다 다르다"와 같은 결론이 다른 기전에서 반복된다.[^asai2024-selfrag]
- DRAGIN이 고쳐 잡는 것 — **검색 증강의 필요성은 생성 확신에만 달린 것이 아니라 토큰의 중요도,
  토큰의 의미, 그리고 각 토큰이 뒤따르는 토큰에 미치는 영향에도 달려 있다** (3.1절,
  p.3).[^su2024-dragin] 그래서 발동 점수를 셋의 곱으로 둔다 — **`S_RIND(t_i) = H_i · a_max(i) · s_i`**
  로, `H_i`는 어휘 전체에 걸친 확률 분포의 엔트로피(entropy), `a_max(i)`는 뒤따르는 모든 토큰에서
  오는 최대 어텐션 값, `s_i`는 불용어를 걸러 내는 이진 의미 지시자다 (3.1절, 식 (1)–(5),
  pp.3–4).[^su2024-dragin] 질의 쪽도 직전 문장이 아니라 **앞선 전체 맥락에 대한 자기 어텐션**에서
  뽑는다 (3.2절, p.4).[^su2024-dragin]
- **두 축을 갈라 재면 FLARE의 몫이 어디인지가 드러난다** — 질의 형성을 직전 문장으로 고정하고 발동
  시점만 바꾸면 IIRC EM이 FLARE 0.128, FL-RAG 0.155, FS-RAG 0.171, DRAGIN 0.187이고 (5.3절, p.8,
  Table 4), 발동을 RIND로 고정하고 질의 형성만 바꾸면 HotpotQA EM이 FLARE 0.262로 베이스라인 중
  가장 높다 (5.4절, p.8, Table 6).[^su2024-dragin] 저자들의 읽기는 **FLARE의 질의 형성 전략은 다른
  베이스라인보다 유의미하게 낫지만 전체 성능은 그렇지 않으며, 이는 FLARE의 검색 증강 시점이 완벽과는
  거리가 멀다는 것을 가리킨다**는 것이다 (5.1절, p.7).[^su2024-dragin]

## 세 갈래의 대가는 서로 다른 자리에 붙는다

- 비용을 내는 자리가 다르다 — 사전 라우팅은 **분류기의 훈련 데이터**(와 그 라벨링이 틀릴
  여지)에,[^jeong2024-adaptiverag] 생성 중 결정은 **생성 도중의 반복 호출**에(순진한 구현은 검색마다
  LM을 다시 깨우고 캐싱이 없으면 이전 활성을 다시 계산한다 — 9 Limitations,
  p.9),[^jiang2023-flare] 모델 내장 판단은 **모델 자신의 훈련**(비평 모델·반성 토큰
  코퍼스)에[^asai2024-selfrag] 낸다. 어느 것이 옳은가는 상황이 고르는 선택이지 사실의 충돌이 아니다.
- 적용 가능성도 다르다 — FLARE는 **추가 훈련 없이 추론 시점에 어떤 기존 LM에도 적용 가능**하고
  (1절, p.2),[^jiang2023-flare] DRAGIN도 추가 훈련을 요구하지 않지만 **RIND와 QFS 양쪽이 자기 어텐션
  기전에 의존하므로 자기 어텐션 점수에 접근을 주지 않는 API에는 적용할 수 없다** (7 Limitations,
  p.9).[^su2024-dragin] 곧 갈래의 선택은 성능만이 아니라 **모델을 어떻게 부르는가**에도 묶인다.
- 세 원전이 공통으로 재확인하는 것 하나 — **검색을 더 하는 것이 늘 좋지는 않다.** 고정 규칙 기반
  검색이 단발 검색을 늘 이기지는 않으며, **잘못된 위치에서 수행된 검색 증강은 LLM 출력의 품질을
  개선하는 데 도움이 되지 않을 수 있다** (5.1절, p.7).[^su2024-dragin] 같은 결론이 Self-RAG의
  절제 실험과[^asai2024-selfrag] FLARE의 문턱 곡선에서도[^jiang2023-flare] 나온다.


## 이어지는 페이지

- [검색 증강 생성](../concepts/retrieval-augmented-generation.md) — 이 결정이 붙는 패턴의 본체와
  내장 판단(Self-RAG)의 상세
- [쿼리 재작성](../concepts/query-rewriting.md) — 능동 검색이 임시 문장을 질의로 바꾸는 세 방법
- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 세 갈래가 공통으로 BM25를 검색기로 쓰는 자리
- [모델 라우터](../concepts/model-router.md) — 질의를 보고 경로를 고르는 같은 형태의 부품

[^jeong2024-adaptiverag]: Jeong et al. 2024, "Adaptive-RAG: Learning to Adapt Retrieval-Augmented
    Large Language Models through Question Complexity", NAACL 2024 (인쇄 쪽 7036–7050). 쪽 번호는
    스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.7036). 이 페이지는 초록·1절 Introduction·2절 Related
    Work의 Adaptive Retrieval 항목·3.2절 Adaptive-RAG(질의 복잡도 평가·훈련 전략)·4.4절
    Implementation Details·5절 Experimental Results and Analyses·Limitations를 담았다. Table 3은
    원문 표기를 그대로 옮겼다. Table 1(전 데이터셋 평균)·Table 2(데이터셋별)·Table 4(주석 전략
    절제)·Table 5(사례 연구)·Table 7–8(부록)은 옮기지 않았다 — 추출본에서 열이 서로 섞여 안전하게
    읽히지 않았고, 본문이 서술한 우열과 Table 3·Table 6의 읽히는 수치만 담았다. Figure 1(성능 대
    시간, p.1)·Figure 2(세 접근 도식, p.2)·Figure 3(분류기 성능과 혼동 행렬, p.7)은 옮기지 않았고
    본문이 서술한 것만 담았다. 3.1절 Preliminaries의 형식화는 3단 라우팅 서술에 필요한 만큼만 담았다.
    Self-RAG(Asai et al., 2024)·FLARE(Jiang et al., 2023)·DPR(Karpukhin et al., 2020)·
    BM25(Robertson et al., 1994)는 이 KB에 원전이 있다. FLAN-T5(Chung et al., 2022)·
    T5(Raffel et al., 2020)·IRCoT(Trivedi et al., 2023)·Mallen et al.(2023)·MuSiQue·HotpotQA·
    2WikiMultiHopQA·SQuAD·Natural Questions·TriviaQA는 jeong2024-adaptiverag를 통한 전언이다.

[^jiang2023-flare]: Jiang et al. 2023, "Active Retrieval Augmented Generation", EMNLP 2023
    (인쇄 쪽 7969–7992). 쪽 번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.7969). 이 페이지는
    초록·1절 Introduction·2절 Retrieval Augmented Generation·3절 FLARE(3.1–3.3)·4절 Multi-time
    Retrieval Baselines·6절 Experimental Results(6.1–6.2)·8절 Conclusion·9절 Limitations를 담았다.
    Table 1(2WikiMultihopQA 베이스라인 비교)·Table 3(직전 문장 대 다음 문장)·Table 5(마스킹 문턱)는
    본문이 서술한 수치만 담았고 표 자체는 옮기지 않았다. Table 2·4·6과 Figure 1–5, 부록 A–D의
    프롬프트는 옮기지 않았다. 5절 Experimental Setup의 데이터셋·지표 세부는 담지 않았다.
    Self-RAG(Asai et al., 2024)와의 대비는 이 페이지의 서술이며 FLARE 원문은 Self-RAG를 인용하지
    않는다. BM25(Robertson and Zaragoza, 2009)는 이 KB에 원전이 있다. Toolformer(Schick et al.,
    2023)·RETRO(Borgeaud et al., 2022)·IC-RALM(Ram et al., 2023)·KNN-LM(Khandelwal et al., 2020)·
    IRCoT(Trivedi et al., 2022)·self-ask(Press et al., 2022)·Kadavath et al.(2022)·
    text-davinci-003·Bing 검색은 jiang2023-flare를 통한 전언이다.

[^su2024-dragin]: Su et al. 2024, "DRAGIN: Dynamic Retrieval Augmented Generation based on the
    Real-time Information Needs of Large Language Models", ACL 2024 (인쇄 쪽 12991–13013). 쪽
    번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.12991). **표제 표기 차이** — 스냅샷한 PDF의
    표제는 "based on the Information Needs of"로 인쇄돼 있고 "Real-time"이 빠져 있다. 소스 메타의
    제목은 ACL Anthology·DOI 등록 제목("Real-time" 포함)을 따랐다. 이 페이지는 초록·1절
    Introduction·2절 Related Work·3절 Methodology(3.1–3.3)·4절 Experimental Setup(4.3–4.5)·5절
    Experimental Results(5.1–5.5)·6절 Conclusions·7절 Limitations를 담았다. Table 2(전체 결과)·
    Table 3(검색 호출 횟수)·Table 5(RIND 문턱)·Table 7(BM25 대 SGPT)은 본문이 서술한 것과
    [어휘 기반 검색](../concepts/term-based-retrieval.md)이 담은 것만 옮겼다. Table 1(베이스라인
    개관)과 Figure 1(전체 도식, p.3), 부록 A–F의 프롬프트 템플릿은 옮기지 않았다. 식 (1)–(6)은
    원문의 수학 표기를 인라인 코드로 옮긴 것이며 식 (2)의 어텐션 정의와 식 (6)의 절단은 서술로만
    담았다. FLARE(Jiang et al., 2023)는 이 KB에 원전이 있다. LLaMA-2(Touvron et al., 2023b)·
    Vicuna(Chiang et al., 2023)·SGPT(Muennighoff, 2022)·IRCoT(Trivedi et al., 2022)·
    RETRO(Borgeaud et al., 2022)·IC-RALM(Ram et al., 2023)·spaCy는 su2024-dragin을 통한 전언이다.

[^asai2024-selfrag]: Asai et al. 2024, "Self-RAG: Learning to Retrieve, Generate, and Critique
    through Self-Reflection", ICLR 2024 (oral). 스냅샷은 arXiv:2310.11511 v1(프리프린트 —
    카메라 레디와 자구가 다를 수 있음). 이 페이지는 문턱 실험·절제 결론의 비교 인용만 담으며,
    Self-RAG의 본체는 [검색 증강 생성](../concepts/retrieval-augmented-generation.md)이 담는다.
