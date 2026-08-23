---
type: webpage
title: "Test Desiderata"
author: [{family: Beck, given: Kent}]
issued: "2019"
container-title: "testdesiderata.com"
URL: "https://testdesiderata.com/"
snapshot: /it/archive/beck2019-test-desiderata/
snapshot_sha256: "3a058bde81bf0bab9eff8c810e5c7585306e999987310fe1760024399c14ad40"
accessed: "2026-08-20"
---

# Test Desiderata

**테스트가 갖출 만한 성질 열둘을 한 줄 정의로 나열하고, 그 성질들이 서로 지지하거나
간섭한다고 적은 한 쪽짜리 공개 문면.** 이 KB가 이 소스를 들이는 이유는 목록 자체가 아니라
**성질을 하나의 이상이 아니라 서로 당기는 여럿으로 놓는 형식**이다. 같은 형식을 네 속성으로
세운 [khorikov2020-unit-testing](khorikov2020-unit-testing.md)과 셋으로 세운
[wacker2015-e2e](wacker2015-e2e.md)가 이미 이 KB에 있고, 이 문서는 그 둘보다 넓은
열둘을 **논증 없이** 늘어놓는다.

## 지위 — 실무자의 목록이고 측정도 논증도 없다

- **근거 등급 표기는 `practitioner-norm`이다.** 이 문서에는 실험도 표본도 측정도 없고,
  인용할 수 있는 수치가 하나도 없다. 성질마다 붙은 것은 한 줄 정의뿐이고 근거 절도 참고문헌도
  없다. **대장(queue.yaml)에는 `evidence_grade:`가 기재돼 있지 않아 이 등급은 이 반입이
  문면을 보고 붙인 것이다** — 아래 "인용할 때 지킬 것" 참조.
- **자기 규정은 문서의 부제 한 줄이 전부다**: `Optimize the value of your tests by choosing
  how to tradeoff among various valuable properties.` 목록을 규범이 아니라 **고르는
  사람의 교환 재료**로 규정한다. 이 문장은 `<title>`·`og:description`·`<h2 id="project_tagline">`
  세 자리에 같은 문면으로 놓여 있다.
- **성질 사이의 우선순위가 없다.** 어느 성질을 먼저 포기하라는 말도, 어떤 조건에서 어느
  쪽으로 기울라는 말도 없다. 지지·간섭·겉보기 간섭 세 문장이 관계에 관해 이 문서가 적은
  전부다.

## 판과 서지 — 문면에 인쇄된 것과 인쇄되지 않은 것

- **저자 표시(byline)가 없다.** 확보본 어디에도 `by …` 줄이 없고, 저자를 가리키는 문면은
  둘뿐이다. ① 목록을 소개하는 문장의 `describing each property with Kent Beck and Kelly
  Sutton`, ② 말미의 원글 링크 주소 `medium.com/@kentbeck_7670/…`. **`author`에 Beck을 적은
  근거는 이 둘이고 저자 표기 줄이 아니다.**
- **발행 연도가 인쇄돼 있지 않다.** 게시일·갱신일·저작권 줄이 확보본에 없다. `issued: "2019"`는
  **대장 기재(`Beck, Test Desiderata (2019)`)와 원글이 2019년 Medium 글이라는 외부 근거**이지
  이 문면에서 읽은 값이 아니다. citekey의 `2019`도 같은 지위다.
- **원글은 대조하지 않았다.** 말미가 `The original Test Desiderata papers are here and here`로
  Medium 글 둘(`test-desiderata-94150638a4b3` · `programmer-test-principles-d01c064d7934`)을
  가리키는데, **이 반입은 Medium 판을 받지 않았다**(확보 회차 기록: Medium 403). 이 KB가
  문면으로 보증하는 것은 testdesiderata.com 스냅샷 한 장뿐이고, **원글과의 이동(문구 변경·
  성질 추가·삭제)은 미대조다.**
- **현행판 재취득 대조도 하지 않았다.** 살아 있는 페이지이므로 열람일 스탬프를 단다 —
  이 KB의 직인용은 **2026-08-20 확보본**에 대한 것이다.
- **확보본은 HTML 한 장 5,493바이트다.** Jekyll v3.10.0이 찍었고 푸터가
  `Published with GitHub Pages`다. 사이트 껍데기와 Fathom 분석 스크립트 태그가 함께 들어 있다.

## 인용할 때 지킬 것

- **학술 근거로 쓰지 않는다.** 실무자가 자기 경험으로 고른 목록이고, 목록의 완전성도
  성질의 독립성도 검증되지 않았다. 조항에 쓸 때는 저자의 자기 규정(교환 재료)을 함께 옮긴다.
- **등급을 이 반입이 붙였다는 사실을 지운 채 인용하지 않는다.** 대장에 `evidence_grade:`가
  없으므로, 다음 세션이 이 등급을 대장 판정으로 오인하면 안 된다. 판단 근거는 문면에
  측정·표본·참고문헌이 하나도 없다는 사실이다.
- **다섯 분 비디오는 이 KB가 갖고 있지 않다.** 성질마다 유튜브 주소가 걸려 있고 소개 문장이
  `links lead to 5-minute videos`라고 적지만, **이 반입은 어느 영상도 열지 않았다.** 성질의
  뜻을 더 좁히는 서술이 영상 안에 있을 수 있고, 이 KB는 그것을 모른다. 영상에서 온 것처럼
  적힌 서술이 페이지에 있으면 그것은 오류다.
- **마인드맵 그림은 확보되지 않았다.** 본문에 `<img src="/Desiderata-map.jpg" alt="Mindmap" />`가
  있으나 확보본은 HTML 한 장이라 그림 파일이 없다. **그림 안에 성질 사이의 관계가 그려져
  있을 수 있고, 이 KB는 그것을 읽지 못했다** — 성질 간 관계에 관해 이 KB가 아는 것은
  산문 세 문장뿐이다.
- **역어는 이 KB가 지은 것이다.** 열두 성질의 이름은 한국어 확립 역어가 없다. 채택한 역어와
  그 근거는 [테스트의 바람직한 성질 열둘](../concepts/test-desiderata.md)의 역어 절이
  정본이고, **원어를 함께 적지 않은 인용은 이 소스에 귀속시키지 않는다.**

## 옮기지 않은 것

사이트 껍데기(헤더·푸터·스타일시트 링크), Jekyll SEO 태그 블록, Fathom 분석 스크립트,
그리고 열두 성질에 걸린 유튜브 주소 열두 개다. 주소는 페이지에 옮기지 않았고 **영상은
열지 않았다**.
