---
type: concept
title: 커버리지 운용의 산업 권고
status: draft
description: 커버리지가 효과성을 예측하느냐는 실증 논쟁 뒤에 한 회사가 낸 실무 합의문 — 지표를 손실 있는 간접 측정으로 규정한 자리, 값어치는 덮인 곳이 아니라 안 덮인 곳에 있다는 조문, 이상적 수치는 없고 하향식 강제를 피한다면서도 관문은 걸라는 두 권고의 병존, 회사가 적은 권고 구간이 왜 측정값이 아닌가, 커밋 단위 임계와 파이프라인 집계, 그리고 단정의 실질성은 커버리지가 아니라 뮤테이션 테스팅이 잰다는 대목
generated: { by: "claude-opus-5", at: "2026-08-23T04:00:00Z" }
sources:
  - { id: arguelles2020-coverage, resource: /it/sources/arguelles2020-coverage.md }
---

# 커버리지 운용의 산업 권고

- [이 소스의 지위](#이-소스의-지위)
- [값어치는 안 덮인 곳에 있다](#값어치는-안-덮인-곳에-있다)
- [이상적 수치는 없고 하향식 강제는 피한다](#이상적-수치는-없고-하향식-강제는-피한다)
- [그러면서도 관문은 걸라고 한다](#그러면서도-관문은-걸라고-한다)
- [회사가 적은 수치의 지위](#회사가-적은-수치의-지위)
- [단정의 실질성은 커버리지가 재지 않는다](#단정의-실질성은-커버리지가-재지-않는다)
- [단위 테스트 커버리지만으로는 부족하다](#단위-테스트-커버리지만으로는-부족하다)
- [이 KB의 읽기 — 논쟁 양극 사이 어디에 서는가](#이-kb의-읽기--논쟁-양극-사이-어디에-서는가)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **커버리지 논쟁이 갈린 채로 남았을 때, 지금 조직은 코드 커버리지
(code coverage)를 실제로 어떻게 운용하라고 권고받는가.**

## 이 소스의 지위

- **근거 등급은 `industry-norm`이다.** 측정도 표본도 통제도 없다. **규모 전제를 함께
  적는다** — 코드 리뷰에 커버리지를 심는 배선, 파이프라인 전체의 집계, 커밋 단위 관문은
  전부 그런 인프라가 이미 서 있는 조직의 그림이고, 그 인프라가 없는 조직에 이 권고를
  그대로 옮길 근거는 이 글에 없다.
- **저자들이 첫 문단에서 글의 성격을 규정한다.**[^arguelles2020-coverage]

  > We have spent several decades driving software testing initiatives in various very
  > large software companies. … The purpose of this document is to give you tools to steer
  > people on all ends of the spectrum to find common ground so that you can move forward
  > and use coverage information pragmatically.

  **재서 보인 것이 아니라 논쟁을 멈추려고 쓴 합의문이다.** 이 페이지는 이 글을 "학술
  근거"로 쓰지 않고, 저자들의 자기 규정을 인용해 지위를 밝힌다.
- **글 자신이 실증의 부재를 인정한다** (본문 불릿 2):[^arguelles2020-coverage]

  > It is an open research question whether code coverage alone reduces defects, but our
  > experience shows that efforts in increasing code coverage can often lead to culture
  > changes in engineering excellence that in the long run reduce defects.

  **뒤이어 오는 근거가 `our experience`다.** 효과의 근거로 쓸 수 없다는 것을 원문이
  먼저 적어 둔 셈이고, 이 페이지는 그 문장을 그대로 지위 표기로 쓴다.
- **지표의 성격을 스스로 좁힌다** (본문 불릿 1):[^arguelles2020-coverage] 커버리지가
  주는 것은 `a reasonable, objective, industry standard metric with actionable data`지만
  `it’s a lossy and indirect metric that compresses a lot of information into a single
  number so it should not be your only source of truth`라는 이해 위에서 다뤄야 한다.
  **손실 있는(lossy) 간접 지표**라는 자기 규정이 아래 모든 권고의 전제다.

## 값어치는 안 덮인 곳에 있다

**이 글의 뼈대 문장이다** (본문 불릿 4):[^arguelles2020-coverage]

> In fact a lot of the value of code coverage data is to highlight not what’s covered,
> but what’s not covered.

- **같은 말을 사람의 판단 쪽에서 한 번 더 적는다** (본문 불릿 8):[^arguelles2020-coverage]

  > More important than the percentage of lines covered is human judgment over the actual
  > lines of code (and behaviors) that aren’t being covered … What’s not covered is more
  > meaningful than what is covered.

- **신호가 한 방향으로만 흐른다는 규정이 따라붙는다.** 높은 수치는 테스트 품질을 보증하지
  않지만(본문 불릿 3) 낮은 수치는 큰 영역이 배포마다 자동 검증 없이 나간다는 것을
  **보증한다**(본문 불릿 4). 그래서 낮은 쪽에만 강한 결론이 붙는다.
- **배선의 형태는 코드 리뷰다** (본문 불릿 8).[^arguelles2020-coverage] 커버리지를 코드
  리뷰 절차에 심으면 리뷰가 더 빠르고 쉬워졌다고 적고, 수치뿐 아니라 **덮인 줄이 리뷰
  화면에 강조되어 보일 때** 개발자가 중요한 코드부터 덮게 된다고 쓴다. 디버그 로그 줄처럼
  덜 중요한 코드가 있다는 것이 그 근거다.

## 이상적 수치는 없고 하향식 강제는 피한다

- **보편 목표치의 부재를 조문으로 세운다** (본문 불릿 5):[^arguelles2020-coverage]

  > We cannot mandate every single team should have x% code coverage; this is a business
  > decision best made by the owners of the product with domain-specific knowledge.

  필요한 테스팅 수준은 (a) 코드의 사업 영향·중요도, (b) 얼마나 자주 손댈 것인가,
  (c) 얼마나 오래 살 것인가와 복잡도·도메인 변수의 함수라고 적는다.
- **강제를 걸 때의 조건도 같은 자리에 적는다** (본문 불릿 5).[^arguelles2020-coverage]
  x%를 요구하는 어떤 지시든 **테스팅을 쉽게 만드는 인프라 투자가 동행해야** 하고,
  엔지니어가 목표를 체크박스처럼 다뤄 **그 위로는 올리지 않게 될 수 있음**을 경계하라고
  쓴다.
- **회사 차원의 방침도 같은 방향이다** (본문 불릿 6):[^arguelles2020-coverage]

  > However we like to stay away from broad top-down mandates and encourage every team to
  > select the value that makes sense for their business needs.

## 그러면서도 관문은 걸라고 한다

**앞 절과 나란히 읽어야 하는 자리다** (본문 불릿 12):[^arguelles2020-coverage]

> We should gate deployments that do not meet our code coverage standards.

- **어떤 관문이냐는 팀이 정한다.**[^arguelles2020-coverage] 전체 코드에 걸 것인가 신규
  코드에만 걸 것인가, 고정 수치인가 이전 판 대비 변화량인가, 무시하거나 집중할 부분은
  어디인가 — 여러 기제를 두고 팀이 토론해 정하고 그것을 지키기로 약속한다. 관문을 어기는
  커버리지 하락은 체크인과 프로덕션 도달을 막아야 한다고 적는다.
- **같은 문단이 자기 단서를 단다.**[^arguelles2020-coverage] 관문이 채워야 할 체크박스로
  취급되면 역효과가 날 수 있다며 이렇게 쓴다 — `pressure to 'hit the metric' almost
  never yields the desired outcome`.
- **그래서 이 글의 권고는 "관문을 걸지 마라"가 아니라 "관문을 걸되 목표로 읽지 마라"다.**
  강제를 피하라는 절과 관문을 걸라는 절이 한 글 안에 병존하고, 원문은 그 둘을 모순으로
  적지 않는다 — 앞쪽은 **누가 수치를 정하는가**(팀), 뒤쪽은 **정해진 수치를 어떻게
  집행하는가**(하락 차단)에 걸린다.

## 회사가 적은 수치의 지위

**이 글의 수치는 전부 회사가 정한 권고이거나 경험 진술이고 측정값이 아니다.** 분모도
표본도 집계 절차도 인쇄돼 있지 않다. 아래 값은 **그 지위로만** 옮긴다.

- **권고 구간** (본문 불릿 6):[^arguelles2020-coverage]

  > Although there is no “ideal code coverage number,” at Google we offer the general
  > guidelines of 60% as “acceptable”, 75% as “commendable” and 90% as “exemplary.”

  `general guidelines`라는 자기 표기가 이 값의 격이고, 바로 다음 문장이 하향식 강제를
  피한다고 적는다. **어떤 커버리지 종류(줄·분기·조건)인지도 이 글에 적혀 있지 않다.**
- **커밋 단위 임계** (본문 불릿 10):[^arguelles2020-coverage] 프로젝트 전체 목표를 90%
  위로 두는 것은 대개 값어치가 없지만 `per-commit coverage goals of 99% are reasonable,
  and 90% is a good lower threshold`라고 적는다. 자주 바뀌는 코드를 덮게 하고 스위트가
  시간이 지나며 나빠지지 않게 하는 것이 목적이다.
- **수확 체감** (본문 불릿 7):[^arguelles2020-coverage] 90%에서 95%로 가는 데 매달리지
  말라며 `The gains of increasing code coverage beyond a certain point are logarithmic`
  이라 적고, 대신 30%에서 70%로 가는 구체적 걸음을 밟으라고 쓴다. **"어느 지점"인지도
  로그 곡선의 근거도 이 글에 없다** — 형태에 대한 저자들의 진술이다.

## 단정의 실질성은 커버리지가 재지 않는다

- **커버리지가 보증하는 것의 한계를 먼저 못 박는다** (본문 불릿 3):[^arguelles2020-coverage]

  > Code coverage does not guarantee that the covered lines or branches have been tested
  > *correctly*, it just guarantees that they have been executed by a test.

  수치를 채우려고 테스트를 복사해 붙이거나 값어치 없는 테스트를 더하는 것을 경계하라고
  같은 불릿에서 적는다.
- **그 자리에서 다른 지표를 지목한다** (본문 불릿 3):[^arguelles2020-coverage]

  > A better technique to assess whether you’re adequately exercising the lines your tests
  > cover, and adequately asserting on failures, is mutation testing.

  **뮤테이션 테스팅(mutation testing)**이 답하는 물음이 커버리지의 물음과 다르다는
  구분이다 — 줄이 실행됐는가가 아니라 그 줄에서 **단정(assertion)이 실패를 실제로
  잡는가**다. 원문은 이 낱말에 자사 논문 링크를 걸어 두고 본문에서는 더 설명하지 않는다.
- **100%를 겨냥할 때의 대가도 같은 불릿에 있다.**[^arguelles2020-coverage] 수치를 100%에
  최대한 가깝게 만드는 데 집중하면 `a false sense of security`에 이르고, 기계 시간을
  태우며 유지해야 할 저가치 테스트라는 기술 부채를 만든다고 적는다.

## 단위 테스트 커버리지만으로는 부족하다

- **집계의 단위를 파이프라인으로 올린다** (본문 불릿 11).[^arguelles2020-coverage] 단위
  테스트 커버리지는 퍼즐의 한 조각이고, 통합·시스템 테스트의 커버리지도 중요하며,
  파이프라인의 **모든 출처를 합친 관점**이 프로덕션까지 가는 동안 무엇이 한 번도 실행되지
  않는지를 보여 준다.
- **그러나 종류마다 신호의 질이 다르다고 같은 불릿이 적는다.**[^arguelles2020-coverage]
  단위 테스트는 실행된 코드와 평가된 코드의 상관이 높지만 통합·종단(end-to-end) 테스트의
  커버리지 일부는 **의도한 것이 아니라 부수적으로(incidental)** 생긴다.
- **그럼에도 통합 쪽을 집계에 넣는 이유**는 단위 테스트에서 덮지 않은 것을 통합 테스트가
  덮고 있으리라 **믿어 버리는 상황**을 피하기 위해서다.[^arguelles2020-coverage]

## 이 KB의 읽기 — 논쟁 양극 사이 어디에 서는가

**이 글은 실증 논쟁의 어느 극에도 서지 않고 양쪽의 결론을 운용 규칙으로 나눠 받는다.**
#hypothesis 아래 배치는 이 KB가 붙인 읽기이고 이 글이 주장한 것이 아니다.

- **회의 측에게서 받는 것**: 커버리지 수치를 스위트의 품질로 읽지 않는다. 높은 수치가
  보증하지 않는다는 이 글의 불릿 3이
  [커버리지 신호는 스위트 크기가 만든다](../concepts/coverage-confounded-by-suite-size.md)의
  결론과 같은 방향이다 — 다만 그 논문은 그것을 **재서** 말하고 이 글은 **경험으로** 말한다.
- **옹호 측에게서 받는 것**: 그래도 커버리지를 계속 재고 낮은 쪽에 힘을 쏟는다. 낮은
  수치에만 강한 결론을 붙이는 이 글의 비대칭이
  [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md)가 남긴
  "커버리지에 신호가 있다"는 쪽을 버리지 않는 배치다.
- **그래서 이 글이 서는 자리는 판정이 아니라 운용이다.** 논쟁이 갈린 채로 남았다는 것을
  불릿 2가 인정하고, 그 위에서 **재되 목표로 읽지 않는** 규칙을 세운다.
  [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md)가 1999년에
  세운 구분과 조문이 겹치지만 **갈리는 자리가 하나 있다** — 그쪽은 관문 수치가 사람의
  최적화 대상을 바꾼다며 관문 자체를 경계하고, 이쪽은 같은 부작용을 인정하면서도
  **관문을 걸라**고 권고한다.
- #hypothesis **생성 테스트 시대에 "무엇이 안 덮였나"는 물음이 뜻을 바꾼다.** 사람이
  테스트를 쓰던 조건에서 빠진 커버리지는 사람의 설계 실수를 가리키는 단서였지만, 모델이
  후보를 대량으로 만들고 관문이 거르는 배선에서는 **관문의 조건이 무엇을 남기느냐**가
  덮이는 곳을 정한다. 이 KB의
  [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md)이 그 실물이고,
  줄 커버리지 관문을 통과하지 못했을 테스트의 절반 가까이가 결함을 잡는다는 후속 실측이
  같은 자리에 있다. 이 글은 그 조건을 다루지 않는다.

## 이 소스의 사각

- **측정이 하나도 없다.** 커버리지를 올린 노력이 문화를 바꾸고 결함을 줄인다는 이 글의
  중심 주장에 붙은 근거가 `our experience`뿐이다.
- **권고 구간의 유래가 적혀 있지 않다.** 60·75·90이 어떻게 정해졌는지, 어떤 커버리지
  종류에 걸리는지, 어느 집계 단위인지가 전부 없다.
- **관문 권고와 강제 회피의 관계를 원문이 해소하지 않는다.** 둘을 나란히 적을 뿐, 팀이
  정한 수치가 다시 하향식 압력이 되는 경로는 다루지 않는다.
- **뮤테이션 테스팅을 이름으로만 지목한다.** 무엇을 어떻게 재는지, 비용이 얼마인지,
  어디에 걸어야 하는지가 이 글에 없다.
- **논쟁의 실증을 인용하지 않는다.** 커버리지가 효과성을 예측하는지에 대한 연구를 이
  글은 `an open research question`이라고만 적고 어느 연구도 지목하지 않는다.

## 이어지는 페이지

- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 같은
  구분을 1999년에 세운 실무자 글. 관문에 대한 결론이 이 글과 갈린다
- [커버리지 신호는 스위트 크기가 만든다](../concepts/coverage-confounded-by-suite-size.md) —
  실증 논쟁의 회의 측 극
- [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md) —
  실증 논쟁의 옹호 측 극
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 줄 커버리지를
  실제 관문의 조건으로 쓴 산업 배선과 그 관문이 버린 것
- [실용주의 스타터 킷](../concepts/pragmatic-starter-kit.md) — 같은 한계 진단에서 **재는 대상을
  상태 커버리지로 바꾸라**는 결론으로 가는 실무 규범
- [자기 테스트 코드](../concepts/self-testing-code.md) — 커버리지 분석은 테스트되지 않은 영역을
  찾는 데만 좋다는 같은 방향의 판정이 리팩터링 쪽에 적힌 자리
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) — 관문을
  다 통과해도 남는 상한

[^arguelles2020-coverage]: Arguelles, Ivanković & Bender 2020, "Code Coverage Best
    Practices", Google Testing Blog, 2026-08-23 열람본. **쪽 번호가 없는 웹 문서이므로
    locator는 본문 불릿 번호다** — 서문 두 문단 뒤로 굵은 문장으로 시작하는 불릿 열두
    개가 이어지고, 이 페이지는 그 순서를 1~12로 센다. 직인용은 원문 표기 그대로이고
    말줄임표(…)만 이 페이지가 넣었다. 게시일 `Friday, August 07, 2020`과 저자 세 사람은
    확보본 문면에서 확인했다. 옮기지 않은 것: 댓글 셋, 사이드바, 그리고 원문이 링크한
    두 논문(`research.google` 기탁본)의 내용이다.
