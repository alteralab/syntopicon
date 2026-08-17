---
type: webpage
title: "A Philosophy of Software Design vs Clean Code"
author: [{family: Ousterhout, given: John}, {family: Martin, given: Robert C.}]
issued: "2024-09-04"
container-title: "GitHub"
URL: "https://github.com/johnousterhout/aposd-vs-clean-code"
snapshot: /it/archive/ousterhout2024-aposd/
snapshot_sha256: "37109a6804172e75a49f4b29d82c64fa95e217b7ee70b01a8bd60ee8c330f51f"
accessed: "2026-08-17"
---

# A Philosophy of Software Design vs Clean Code

**이 논쟁의 1차 사료다.** 이 KB의 `contradicts` 두 자리에 걸린 두 저자가 직접 맞붙은
유일한 공개 문서이고, 문서 스스로 그 성격을 밝힌다 — **이 문서는 2024년 9월과 2025년
2월 사이에 로버트 "엉클 밥" 마틴과 존 오스터하우트 사이에서 열린 일련의 논의(일부는
온라인, 일부는 대면)의 결과다**(머리말).

- 형식은 **번갈아 가는 대담**이다. 발언자가 `**JOHN:**`과 `**UB:**`로 표시되고, 각
  주제 끝에 오스터하우트가 합의·불합의 목록을 요약하면 마틴이 그 요약이 공정한지
  확인한다. **양보 지점이 그 요약 절에 몰려 있다.**
- 주제는 셋이다 — 메서드 길이(Method Length), 주석(Comments), 테스트 주도 개발
  (Test-Driven Development). 그 사이에 두 저자가 각자 `PrimeGenerator`를 다시 쓴
  절이 둘 있다.
- **이 소스가 이 KB에 특히 중요한 이유**: [Clean Code](martin2008.md)와
  [A Philosophy of Software Design](ousterhout2021.md)의 대립을 이 KB는 두 책의 문장만
  대조해 세웠는데, 이 문서는 **두 저자 본인이 그 대립을 어디까지 인정하고 어디서
  물러서는지**를 직접 적는다. 판정의 근거가 추론에서 1차 진술로 바뀐다.
- **판본에 관한 새 사실이 여기서 나온다.** 마틴이 대담 중과 맺음말에서 *Clean Code*
  **2판**을 언급하며 이 대담의 내용을 반영했다고 적는다. 이 KB의 martin2008 반입분은
  **초판**이므로 그 페이지들의 주장에는 판본 조건이 붙는다 — 조문은
  [클린 코드](../synthesis/clean-code.md) 허브가 갖는다.

## 스냅샷 취득 경로 — `--url`이 아니다

**GitHub raw가 이 반입 시점에 비인증 요청을 429로 막았다**(curl과 `snapshot.py --url`
모두 실패). 그래서 인증된 `gh api`로 README 원문을 먼저 받아 파일로 스냅샷했다 —
kb-ingest 1단계가 Medium에 대해 규정한 경로와 같은 모양이다(취득이 막히면 먼저 확보한 뒤
로컬 파일로 넘긴다).

- 받은 바이트는 `repos/johnousterhout/aposd-vs-clean-code/contents/README.md`를
  `Accept: application/vnd.github.raw`로 요청한 것이고, 크기는 GitHub API가 보고한
  114599바이트와 일치한다.
- **그러므로 `snapshot_sha256`은 그 시점 `main` 브랜치 README의 다이제스트다.** 저장소가
  갱신되면 달라진다 — 이 문서는 정적 글이 아니라 저장소이므로 그 점이 다른 웹 소스와
  다르다. 절차와 실측은 `it/archive/ousterhout2024-aposd/_progress.yaml` 머리말이 정본이다.

## locator

**절 제목이 잘 붙어 있어 그대로 쓴다** — `§"Method Length"`, `§"Comments Summary"` 등.
대담이므로 **발언자를 함께 적는다**(`§"Method Length", UB 발언`). 발언자를 빼면 누구의
주장인지 사라져 claim이 무의미해지기 때문이다.
