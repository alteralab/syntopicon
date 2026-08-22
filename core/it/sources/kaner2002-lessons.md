---
type: book
title: "Lessons Learned in Software Testing: A Context-Driven Approach"
author:
  - { family: Kaner, given: Cem }
  - { family: Bach, given: James }
  - { family: Pettichord, given: Bret }
issued: "2002"
publisher: "John Wiley & Sons"
ISBN: "9781118080559"
snapshot: /it/archive/kaner2002-lessons/
snapshot_sha256: "3dbf588e518327ce96d9df0571d918734f86465328e9221be5b30ec9695d1115"
accessed: "2026-08-22"
custom:
  locator-unit: "장 번호 + lesson 번호(1~293), 부록은 Appendix. 확보본이 Wiley 전자책
    판(EPUB)이라 인쇄 쪽 앵커가 한 개도 없다 — pagebreak 표식 0건. 그래서 쪽수는 이
    소스의 locator로 쓸 수 없다. 서문·머리말처럼 lesson 번호가 없는 자리는 §Foreword ·
    §Preface(소제목) 꼴로 적는다."
---

# Lessons Learned in Software Testing

맥락 주도 테스팅(context-driven testing) 학파가 자기 원칙을 처음으로 성문화한 책.
저자 셋의 실무 경험을 lesson 293개로 나눠 적었고, 학파의 일곱 원칙은 본문이 아니라
책 끝의 부록에 실려 있다.

**근거 등급은 실무자 선언(practitioner-manifesto)이다.** 저자들이 머리말에서 자기
기준을 직접 적는다 — lesson 채택 기준이 "우리 실제 경험에 기반할 것"이고, 이 책은
"항상 참인 lesson의 모음이 아니라 우리의 lesson"이라고 못 박는다. 측정도 통제
실험도 결과 표도 없다. 이 KB는 이 책을 학술 실증으로 인용하지 않는다.

확보본은 Wiley가 낸 전자책 판(EPUB, ISBN 9781118080559)이고 인쇄 초판은 2002년의
ISBN 0-471-08112-4다 — 판권 면이 "This title is also available in print as ISBN
0-471-08112-4"라고 적는다. 저작권 표기는 2002년 Kaner·Bach·Pettichord다.

증류 범위는 호출자 둘로 한정한다(맥락 원칙 · 버그 옹호). 재개점과 건너뛴 범위의
정본은 `it/archive/kaner2002-lessons/_progress.yaml`이다.
