---
type: paper-conference
title: "Correlated Errors in Large Language Models"
author:
  - { family: "Kim", given: "Elliot" }
  - { family: "Garg", given: "Avi" }
  - { family: "Peng", given: "Kenny" }
  - { family: "Garg", given: "Nikhil" }
issued: "2025"
event-title: "42nd International Conference on Machine Learning (ICML 2025)"
container-title: "Proceedings of the 42nd International Conference on Machine Learning"
collection-title: "Proceedings of Machine Learning Research"
snapshot: /it/archive/kim2025-error-correlation/
snapshot_sha256: "aff0dcf6f2636b561529a1217a1cc399bc94c0bd9f0e1616924c76dd36f36ed2"
accessed: "2026-08-21"
---

# kim2025-error-correlation

서로 다른 언어 모델이 서로 다르게 틀리는지를 세 자료로 실측한 논문이다. 이 KB에서는
`knight1986-nversion`이 프로그램 판본 층에서 잰 것과 **같은 물음의 모델 층 대응물**로
쓴다 — 독립적으로 만들어진 것들이 독립적으로 틀리는가.

**게재 지위는 확보본 문면에서 확인했다.** 1쪽 하단이 "Proceedings of the 42nd
International Conference on Machine Learning, Vancouver, Canada. PMLR 267, 2025"라 인쇄돼
있고, PDF 메타데이터의 Subject가 "Proceedings of the International Conference on Machine
Learning 2025", Keywords가 "Machine Learning, ICML"이다. **워크숍이 아니라 PMLR
proceedings 권에 실린 본회의 논문**이므로 이 KB에서 `peer-reviewed`로 취급한다. 다만
그 등급이 여는 것은 **이 논문이 스스로 잰 값**뿐이다.

**쪽수는 확보본 문면이 아니다.** 확보본은 1–29쪽으로 자체 페이지를 매긴 camera-ready이고,
PMLR v267 pp.30038–30066이라는 쪽 범위는 반입 대장의 리포지토리 레코드가 근거다.
그래서 이 KB의 locator는 **절 번호와 표·그림 번호**로만 단다.

저자는 4인이다 — Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg. 1쪽 각주가 앞의 두 명을
동등 기여로 표시하고, 소속은 Cornell University(1)와 Independent(2)이며, 교신 저자는
Kenny Peng과 Nikhil Garg다.

**문항 수가 논문 안에서 어긋난다 — 인용할 때 주의한다.** 같은 두 값이 세 자리에서
서로 다르게 배정돼 있다.

| 어디 | HUGGINGFACE | HELM |
|---|---|---|
| §1 서론 | 14,402 문항 | 12,032 문항 |
| Table 1(§3.2) | 14,042 응답/모델 | 12,032 응답/모델 |
| Appendix A.1 | 12,032 문항·91개 MMLU 데이터셋·14개 범주·대부분 10지선다 | 14,042 문항·57개 범주·4지선다 한정 |

모델 수(349 대 71)는 세 자리 모두 일치하고, 선택지 수 서술도 본문 §3.2와 Appendix A.1이
일치한다(HELM은 오답 선택지 3개라 우연 일치율 1/3, HUGGINGFACE는 3~10지선다에 80% 이상이
10지선다라 0.127). **어긋나는 것은 문항 수의 배정뿐이다.** 이 KB는 데이터셋 성격 서술이
붙어 있는 Appendix A.1 쪽을 채택하고, 그 사실을 페이지 본문에 적었다.

각주 항목의 원문은 확보하지 않았다. 이 논문이 §2와 §6에서 언급하는 Goel et al. 2025
(CAPA 계열 유사도 지표, arXiv:2502.04313), Wenger & Kenett 2025, Wu et al. 2024,
Peng & Garg 2024a는 전부 미확보이므로 이 KB의 그것들에 대한 서술은 **이 논문을 통한
2차 전언**이고 수치는 옮기지 않는다.

**측정 시점이 이 소스의 유통기한이다.** Appendix D의 HELM 모델 표에서 가장 새 모델이
claude-3-5-sonnet-20241022 · gpt-4o-2024-08-06 · gemini-1.5-pro-002 · llama-3.1/3.2 ·
qwen2.5이고, RESUMES 표의 최신 모델도 같은 세대다. 곧 이 논문의 자료는 **2024년 말까지
공개된 모델 집합의 스냅샷**이다.
