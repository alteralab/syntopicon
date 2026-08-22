---
type: post-weblog
title: "Test Coverage"
author:
  - { family: "Fowler", given: "Martin" }
issued: "2012-04-17"
container-title: "martinfowler.com bliki"
URL: "https://martinfowler.com/bliki/TestCoverage.html"
snapshot: /it/archive/fowler2012-test-coverage/
snapshot_sha256: "0ae9d3aeca242c2174a956d7d649380b5b226bef073d69c1fd6972af445f3a76"
accessed: "2026-08-23"
---

# fowler2012-test-coverage

**커버리지 수치를 목표로 걸지 말라는 실무자 글.** 커버리지는 테스트되지 않은 부분을
찾는 도구로 쓸모가 있고, 테스트가 얼마나 좋은지를 말하는 수치로는 쓸모가 거의 없다는
두 문장이 이 글의 전부다.

**이 소스가 이 KB에서 서는 자리는 각주 층이다.** 회의 측 논문
(`inozemtseva2014-coverage`)이 자기 5절에서 **"테스팅 공동체가 이미 이 점을 지적했다"**며
드는 두 참고문헌 중 하나이고(다른 하나가 `marick1999-coverage`), 그래서 실무자 주장과
실증의 계보를 잇는 자리다.

## 지위 — 실무자 블로그 글이지 학술 근거가 아니다

- **근거 등급은 `practitioner`다.** 측정도 표본도 통제도 없다. 이 페이지의 어떤 문장도
  학술 실증으로 인용되지 않는다.
- **이 글 자신이 남의 말에 기대어 선다.** 본문에 인용 블록 둘이 있는데 **둘 다 Brian
  Marick의 말**이다(`I expect a high level of coverage. Sometimes managers require one.
  There's a subtle difference.` · `If a part of your test suite is weak in a way that
  coverage can detect, it's likely also weak in a way coverage can't detect.`). 글 끝의
  Further Reading도 Marick의 글을 `an excellent article`로 가리킨다. **이 KB는 그 두
  문장을 이 글이 아니라 `marick1999-coverage` 원전으로 인용한다.**
- **저자가 적는 수치는 기대치다** — `a coverage percentage in the upper 80s or 90s`는
  사려 깊게 테스트했다면 그럴 것이라는 저자의 예상이고, 잰 값이 아니다. 이 KB는 이 값을
  측정값으로 인용하지 않는다.

## 판과 서지 — 살아 있는 문서다

- **날짜가 문면에 인쇄돼 있다**: `17 April 2012`.
- 이 글은 갱신될 수 있는 웹 문서다. 이 KB의 직인용은 **2026-08-23 열람본**에 대한 것이고
  그 스냅샷이 위 `snapshot_sha256`이다.
- **회의 측 논문이 이 글을 참고문헌 [13]으로 적을 때 연도를 2012로 적는다.** 문면
  날짜와 일치한다.

## 반입 범위

이 런은 확보본 전문을 읽었다. 페이지로 옮긴 것은 두 문장으로 된 이 글의 핵심 주장과,
목표로 걸면 낮은 품질의 테스트로 쉽게 도달한다는 기제, 그리고 저자가 "충분한 테스팅"의
판정 기준으로 커버리지 대신 내놓는 두 조건이다.

옮기지 않은 것: 본문의 Marick 인용 둘은 `marick1999-coverage` 원전이 담당한다. 사이트
탐색 메뉴와 Further Reading의 외부 링크(Testivus 우화 등)는 이 글의 주장이 아니다.
