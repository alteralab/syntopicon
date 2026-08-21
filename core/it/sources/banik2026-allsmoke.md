---
type: article
title: "All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code"
author:
  - { family: "Banik", given: "Dipayan" }
  - { family: "Chowdhury", given: "Kowshik" }
  - { family: "Shamim", given: "Shazibul Islam" }
issued: "2026"
publisher: "arXiv"
number: "2606.18168"
version: "v1"
snapshot: /it/archive/banik2026-allsmoke/
snapshot_sha256: "d7b28555fc5593e3d403bd85967f72a1a48098651757affaea0a57e727e1e084"
accessed: "2026-08-21"
---

# banik2026-allsmoke

코딩 에이전트 다섯이 GitHub 풀 리퀘스트로 실제로 올린 테스트 파일 패치를 대량으로 긁어
그 안에 단언이 있는지를 구문 분류로 센 저장소 마이닝 연구. `yuan2024-chatgpt-tests`가
**실험실에서 생성시킨** 테스트를 잰다면 이쪽은 **현장에 실제로 올라간** 테스트를 잰다 —
이 KB에서는 그 대비를 위해서만 쓴다.

**미심사 프리프린트다.** 확보본은 arXiv:2606.18168v1(2026-06-16 스탬프)이고 4쪽이며 게재
표면이 없다. 그래서 이 소스의 수치는 어느 페이지에도 박지 않고 방향만 쓰며, 인용하는
자리마다 "미심사" 딱지를 붙인다.

**측정 대상이 다르다는 점도 함께 읽어야 한다.** 이 연구가 세는 것은 실행 결과가 아니라
**패치 텍스트에 나타난 단언 구문의 등급**이다(구문 분류기). 통과율이나 결함 검출력이 아니라
"오라클처럼 생긴 줄이 있는가"를 재는 대리 지표이고, 논문 자신도 분류기와 사람 라벨의
일치율을 함께 보고한다.
