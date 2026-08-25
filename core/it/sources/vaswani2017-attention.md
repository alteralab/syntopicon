---
type: paper-conference
title: "Attention Is All You Need"
author:
  - { family: "Vaswani", given: "Ashish" }
  - { family: "Shazeer", given: "Noam" }
  - { family: "Parmar", given: "Niki" }
  - { family: "Uszkoreit", given: "Jakob" }
  - { family: "Jones", given: "Llion" }
  - { family: "Gomez", given: "Aidan N." }
  - { family: "Kaiser", given: "Łukasz" }
  - { family: "Polosukhin", given: "Illia" }
issued: "2017"
event-title: "31st Conference on Neural Information Processing Systems (NIPS 2017)"
container-title: "Advances in Neural Information Processing Systems 30"
URL: "https://papers.nips.cc/paper/7181-attention-is-all-you-need"
snapshot: /it/archive/vaswani2017-attention/
snapshot_sha256: "dd83901c41a8d3a3de5f8902c9f00bd0c183544466746ed9f79f1c17c5dbd139"
accessed: "2026-08-25"
---

# vaswani2017-attention

트랜스포머 구조의 원전(NIPS 2017 심사 논문). 저자 여덟 명 전원이 "Equal contribution"
각주를 달았고 게재 순서는 무작위라고 그 각주가 밝힌다.

## 정본 판과 다른 판

스냅샷에 **두 판**이 들어 있다. 정본은 논문집 판이다.

| 파일 | 판 | 쪽 | 지위 |
|---|---|---|---|
| `vaswani2017-attention--nips2017-proceedings.pdf` | NIPS 2017 논문집 판 | 11쪽 | **정본**. 심사를 통과한 게재본 |
| `vaswani2017-attention--arxiv-1706.03762v7.pdf` | arXiv:1706.03762v7 (2023-08-02) | 15쪽 | 후속 개정본. 심사 밖 |

**정본을 논문집 판으로 정한 근거**: 이 KB가 이 소스에 매기는 등급은 `peer-reviewed`이고
그 등급이 여는 것은 심사를 통과한 문면뿐이다. arXiv v7이 더한 것(6.3절·부록·수치 하나)은
게재 뒤에 붙은 것이라 같은 심사를 받지 않았다. 또 논문집 판은 EN-FR 수치가 초록·6.1절·표 2
세 자리에서 모두 41.0으로 일치하는데, arXiv v7은 초록과 표 2만 41.8로 고치고 6.1절 본문은
41.0으로 남겨 두어 **판 안에서 어긋난다**(아래 대조표).

두 판의 문면 대조(2026-08-25, 렌더 이미지와 `pdftotext -layout` 양쪽으로 확인):

| 자리 | 논문집 판 | arXiv v7 |
|---|---|---|
| 1쪽 머리 | 없음 | Google의 표·그림 복제 허가 문구가 붙어 있다 |
| 초록 EN-FR BLEU | 41.0 | **41.8** |
| 초록 마지막 문장 | 없음 | 영어 구구조 구문 분석으로의 일반화를 주장하는 한 문장이 더 있다 |
| 표 2 Transformer (big) EN-FR | 41.0 | **41.8** |
| 6.1절 본문 EN-FR | 41.0 | 41.0 (초록·표 2와 어긋난다) |
| 6.3절 English Constituency Parsing + 표 4 | **없다** | 있다 |
| 부록(어텐션 시각화, Figure 3~5) | **없다** | 있다 |
| 4절의 "in the appendix" 문구 | 있다 (가리킬 부록이 없다) | 있다 (부록이 실재한다) |
| 저자·소속·"Equal contribution" 각주 | 동일 | 동일 |
| 표 1·표 3·식 (1)(2)(3)·3절 전체 | 동일 | 동일 |
| 참고문헌 | 32건 | 40건 (번호가 밀린다) |

**두 판의 수치가 다르다는 사실 자체를 개념 페이지에 적었다** —
`concepts/attention-is-all-you-need.md`의 "판 대조" 절.

## 서지의 근거

논문 문면이 인쇄하는 게재 정보는 1쪽 아래의 한 줄뿐이다:
"31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA."
**권·쪽수(Advances in Neural Information Processing Systems 30, pp.5998–6008)는 문면이 아니라
논문집 레코드가 근거다.** 그래서 이 KB의 로케이터는 권 쪽수가 아니라 **논문집 판 PDF에 인쇄된
쪽 번호(1~11)와 절 번호**를 쓴다.

## 대상 페이지

- `concepts/attention-is-all-you-need.md` (신규, 원전 페이지)
- `concepts/transformer-architecture.md` (보강 — Vaswani 2차 경유 딱지 해소)
- `concepts/kv-cache-and-attention-optimization.md` (보강 — 원전 링크)
