---
type: article
title: "Mutation-Guided Unit Test Generation with a Large Language Model"
author:
  - { family: "Wang", given: "Guancheng" }
  - { family: "Xu", given: "Qinghua" }
  - { family: "Briand", given: "Lionel" }
  - { family: "Liu", given: "Kui" }
issued: "2025"
publisher: "arXiv"
number: "2506.02954"
version: "v8"
snapshot: /it/archive/wang2025-mutgen/
snapshot_sha256: "b8b15b1b616d79bcf76a0fa62f8f36c3c97ee20efae6e6f0736834f7817ee69b"
accessed: "2026-08-21"
---

# wang2025-mutgen

MUTGEN — 뮤테이션 피드백을 프롬프트에 넣어 LLM 테스트 생성을 이끄는 접근. 이 KB가 이
소스를 들인 이유는 도구가 아니라 **동기 진술** 하나다: 커버리지가 만점인 생성 테스트가
뮤테이션 점수는 바닥일 수 있다는 것, 곧 커버리지가 오라클의 실질성을 재지 못한다는 것.

**미심사 프리프린트다.** 확보본은 arXiv:2506.02954v8(2026-04-15 스탬프)이고 저널·학회 게재
표면이 없다. `issued: 2025`는 arXiv 식별자의 접수 시점(2025-06)에서 온 것이고, 우리가 읽은
것은 v8이다.

**이 소스에서 수치를 인용하지 않는다.** 근거 등급이 `preprint`인 데다, 초록과 §I이 내세우는
"100% 커버리지에 4% 뮤테이션 점수"는 **HumanEval-Java의 subject id_81 한 건짜리 동기
예시**이지 결과 표의 총계가 아니다(§I, 확보본 p.3). 이 KB는 방향만 쓴다.
