---
type: concept
title: 맥락 주도 테스팅의 일곱 원칙
description: 어떤 프랙티스가 좋은가를 프랙티스가 아니라 맥락이 정한다고 못 박은 학파 선언 — 책 끝 부록에 실린 일곱 원칙 전문과 그것이 실린 자리, 원칙 1·2가 금지하는 것, 항공기 제어 소프트웨어와 웹 워드프로세서를 나란히 놓은 예시, 본문 lesson 층의 같은 조항, 그리고 이 선언에 걸린 단서 넷 — 연구 인용이 한 건도 없다는 것, 저자 한 사람이 뒤에 학파 선언을 수사적 도구라 부르고 학파의 소멸을 공표했다는 것, 반대 진영으로 지목되던 자격 제도가 맥락 의존을 자기 원칙으로 채택하고 이 책을 인용한다는 것, 그리고 학파 명단이 자기 신고라는 것
generated: { by: "claude-opus-5", at: "2026-08-22T14:00:00Z" }
sources:
  - { id: kaner2002-lessons, resource: /it/sources/kaner2002-lessons.md }
---

# 맥락 주도 테스팅의 일곱 원칙

- [이 소스의 지위 — 실무자 선언이지 학술 근거가 아니다](#이-소스의-지위--실무자-선언이지-학술-근거가-아니다)
- [원칙이 실린 자리](#원칙이-실린-자리)
- [일곱 원칙 전문](#일곱-원칙-전문)
- [원칙 1·2가 금지하는 것](#원칙-12가-금지하는-것)
- [원칙을 예시로 보인 자리](#원칙을-예시로-보인-자리)
- [본문 lesson 층의 같은 조항](#본문-lesson-층의-같은-조항)
- [이 선언에 걸린 단서 넷](#이-선언에-걸린-단서-넷)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 프랙티스가 좋은가를 무엇이 정하는가 — 프랙티스 자체인가, 그것이
놓인 맥락인가.**

## 이 소스의 지위 — 실무자 선언이지 학술 근거가 아니다

**근거 등급은 실무자 선언(practitioner-manifesto)이다.** 이 페이지의 어떤 문장도
학술 실증으로 인용되지 않는다. 지위는 저자들 자신의 규정으로 밝힌다.

- 저자들이 lesson 채택 기준을 직접 적고, 그 기준의 하나가 **자기 경험**이다
  (§Preface, "What This Book Is About").[^kaner2002-lessons]

  > The lesson must be based on our actual experience. At least one of us (preferably
  > all three of us) had to have successfully applied the advice we give.

- 저자들이 이 책이 무엇이 **아닌지**도 같은 자리에서 적는다 (§Preface, "What This
  Book Is Not").[^kaner2002-lessons]

  > This book is not a collection of lessons that are always true. These are our
  > lessons, based on our experiences. We believe these are broadly applicable, but
  > some lessons that have been useful and important in our careers may not work for
  > you. You have to use your own judgment.

- **저자들이 자기 경험의 범위 한계까지 적어 둔다** — 대중 시장용 소프트웨어와 계약
  명세 소프트웨어를 주로 다뤘고 **생명이 걸린 소프트웨어와 임베디드 소프트웨어
  경험은 제한적**이라고 같은 절에 밝힌다 (§Preface, "What This Book Is
  Not").[^kaner2002-lessons] 이 자기 한정은 아래 [원칙을 예시로 보인 자리](#원칙을-예시로-보인-자리)의
  항공기 예시를 읽을 때 함께 읽어야 한다 — **예시로 든 쪽이 저자들이 경험이 얇다고
  밝힌 쪽이다.**

## 원칙이 실린 자리

- **맥락 주도 테스팅(context-driven testing)의 일곱 원칙은 본문이 아니라 책 끝의
  부록에 있다.** 부록 제목은 "The Context-Driven Approach to Software Testing"이고,
  원칙 목록은 그 안의 소제목 "The Seven Basic
  Principles of the Context-Driven School" 아래에 있다 (§Appendix).[^kaner2002-lessons]
  머리말이 그 자리를 미리 알린다 — **"We discuss the context-driven approach at the
  end of the book"** (§Preface, "Welcome to Lessons Learned in Software
  Testing").[^kaner2002-lessons]
- **부록이 원칙의 지위를 스스로 규정한다 — 발견이 아니라 합의문이다** (§Appendix,
  도입 문단).[^kaner2002-lessons]

  > We belong to a group of people who are sometimes called the context-driven school
  > of software testing. After several years (on and off), we have finally developed a
  > statement of principles that, we believe, captures the community of views among the
  > loose collection of people who provide intellectual leadership to this school.

- **부록이 같은 문단에서 웹사이트를 만들었다고 적는다** (§Appendix, 도입
  문단).[^kaner2002-lessons]

  > Along with the book, we have created a web site, context-driven-testing.com, to
  > further the development of the school.

  - **그러므로 이 책과 그 사이트는 같은 시기의 두 자리이고, 원칙의 정본 최초 공간은
    책이라는 것이 이 KB의 판정이다.** 근거는 문면 둘이다 — 부록이 사이트를 "책과
    함께(Along with the book)" 만들었다고 적어 **책을 앞에 두고**, 사이트를 원칙의
    출처가 아니라 **합류하는 자리**("join the community")로 가리킨다. 도메인 등록일
    같은 사이트 쪽 사실은 원문 밖이라 이 페이지가 다루지 않는다.

## 일곱 원칙 전문

원칙은 번역하지 않고 부록 문면 그대로 옮긴다 (§Appendix, "The Seven Basic Principles
of the Context-Driven School").[^kaner2002-lessons]

> 1. The value of any practice depends on its context.
> 2. There are good practices in context, but there are no best practices.
> 3. People, working together, are the most important part of any project's context.
> 4. Projects unfold over time in ways that are often not predictable.
> 5. The product is a solution. If the problem isn't solved, the product doesn't work.
> 6. Good software testing is a challenging intellectual process.
> 7. Only through judgment and skill, exercised cooperatively throughout the entire
>    project, are we able to do the right things at the right times to effectively test
>    our products.

## 원칙 1·2가 금지하는 것

- **원칙 1과 2가 하는 일은 프랙티스의 순위를 매기는 축을 옮기는 것이다.** 좋고 나쁨이
  프랙티스에 붙은 성질이 아니라 프랙티스와 맥락의 **짝**에 붙는 성질이 된다. 그래서
  "이 프랙티스가 좋은가"는 원칙 1 아래에서 **답할 수 없는 질문**이 되고, 답할 수 있는
  질문은 "이 맥락에서 이 프랙티스가 좋은가"뿐이다 (§Appendix, 원칙 1·2).[^kaner2002-lessons]
- **원칙 2는 "좋은 프랙티스"를 남기고 "모범 사례"만 지운다.** 상대주의가 아니다 — 좋은
  프랙티스는 있고, 맥락과 무관한 최상급만 없다 (§Appendix, 원칙 2).[^kaner2002-lessons]
- 같은 금지를 머리말이 부록보다 먼저, 더 강한 낱말로 적는다 (§Preface, "What This
  Book Is Not").[^kaner2002-lessons]

  > This book is not a collection of best practices. In fact, we don't believe in "best
  > practices." We believe some practices are more useful than others under some
  > circumstances. We are concerned that many things sold as best practices are pushed
  > (and applied) uncritically, to situations that aren't appropriate to them.

  - **금지의 이유가 이 문장에 있다 — 최상급 자체가 아니라 그것이 유통되는 방식이다.**
    저자들이 문제 삼는 것은 모범 사례로 팔리는 것들이 **비판 없이 밀어붙여지고
    적용된다**는 것이다.

## 원칙을 예시로 보인 자리

부록이 원칙을 논증하지 않고 **대비되는 두 프로젝트**로 보인다. 결론 문장 둘이 원칙
1의 실물이다 (§Appendix, "An Example").[^kaner2002-lessons]

> Testing practices appropriate to the first project will fail in the second. Practices
> appropriate to the second project would be criminally negligent in the first.

- 첫 프로젝트는 **항공기 제어 소프트웨어**다 — "올바른 동작"이 고도로 기술적이고
  수학적인 주제이고, 규제를 따라야 하며, 한 일도 안 한 일도 **20년 뒤 소송의 증거**가
  된다고 적는다. 둘째 프로젝트는 **웹에서 쓰는 워드프로세서**다 — "올바른 동작"은
  기존 사용자를 끌어오는 무엇이든이고, 규제 요구가 없으며, **20개월 뒤면 좋든 나쁘든
  끝난다**고 적는다 (§Appendix, "An Example").[^kaner2002-lessons]
- **예시가 고르는 대비 축은 기술이 아니라 책임과 시간이다.** 두 프로젝트를 가르는 것은
  언어도 규모도 아니고 **틀렸을 때 무엇을 물어야 하는가**와 **얼마나 오래 살아 있는가**다.
  이것이 이 KB가 이 예시에서 읽는 것이고, 부록은 이 축에 이름을 붙이지 않았다.

## 본문 lesson 층의 같은 조항

부록의 원칙은 본문 lesson 293개 위에 얹힌 요약이다. 1장에서 같은 조항이 **맥락이라는
낱말 없이** 나온다 — 실제로 1장 전체에 `context`라는 낱말이 한 번도 나오지 않는다.

- **lesson 2 "Your mission drives everything you do"** — 테스트 조직의 임무가 산업·회사·
  프로젝트·팀 구성원의 성격에 따라 달라진다고 적고, 그래서 테스트 프로젝트가 자리마다
  크게 다르다고 적는다. 예로 든 것은 **테스트 계획서**다 — 어떤 조직에서는 냅킨에 써도
  효과적인 도구이고, 다른 조직에서는 형식과 내용 지침을 지켜 소프트웨어와 함께 납품하는
  산출물이다 (1장, lesson 2).[^kaner2002-lessons]
  - **이것이 원칙 1의 lesson 층 판이다.** 같은 산출물(테스트 계획서)이 맥락에 따라 전혀
    다른 것이 되므로, 그 산출물을 두고 좋다·나쁘다를 말할 자리가 없다.
- **lesson 3 "You serve many clients"** — 테스터의 성공이 **자기가 섬기는 사람들의 요구와
  최선의 이익을 얼마나 잘 채우는가**로 측정된다고 적고, 그 사람들의 요구가 서로 정렬되어
  있지 않다고 덧붙인다 (1장, lesson 3).[^kaner2002-lessons]
  - **이것이 원칙 3의 lesson 층 판이자, 맥락을 사람으로 구체화한 자리다.** 맥락이
    추상적인 환경이 아니라 **이름이 있는 이해관계자들의 어긋나는 요구**로 정의된다.

## 이 선언에 걸린 단서 넷

이 절은 원 소스의 주장이 아니라 **이 KB의 판정**이다. 아래 넷을 함께 읽지 않으면 이
페이지가 학파 선언을 정설로 오인하게 만든다.

- **하나 — 일곱 원칙에 연구 인용이 한 건도 없다.** 부록 전체를 원문에서 훑은 결과
  참고문헌 표기가 0건이고, 각주도 0건이며, 링크는 학파 가입용 메일 주소 하나뿐이다.
  이 책에는 별도의 참고문헌 부록이 있고 본문 lesson들은 그것을 인용하지만, **원칙
  일곱 개가 실린 절은 그 참고문헌을 한 번도 부르지 않는다.** 그러므로 원칙은 실증의
  요약이 아니라 **합의문**이고, 부록 자신이 그렇게 적는다(위 [원칙이 실린 자리](#원칙이-실린-자리)의
  직인용).
- **둘 — 저자 한 사람이 뒤에 학파 선언을 수사적 도구라 부르고 학파의 소멸을 공표했다.**
  Cem Kaner가 이 책 이후의 글에서 학파 선언이 **수사적 도구**였다고 적었고, **이제 그런
  학파는 없다**고 공표했다. **이 KB는 그 글의 원문을 갖고 있지 않다 — 2차 경유이고,
  그래서 문면을 직인용하지 않고 사실만 적는다.** 이 단서가 무거운 이유는 출처가 반대
  진영이 아니라 **원칙 목록에 첫 번째로 이름을 올린 저자 자신**이기 때문이다.
- **셋 — 반대 진영으로 지목되던 자격 제도가 맥락 의존을 자기 원칙으로 채택했다.**
  ISTQB의 기초 자격 요목 v4.0.1이 테스팅의 일곱 원칙 가운데 **여섯 번째로 맥락 의존**을
  두고 그 자리에서 이 책을 인용한다. **원문 미확보 — 2차 경유라 요목의 문면을
  직인용하지 않는다.** 그러나 이 사실이 참이라면 따라오는 판정이 있다 — **모순 쌍의 적대
  축(자격 제도 대 맥락 주도)이 무너졌다.** 맥락 의존은 더 이상 한 학파를 다른 진영과
  가르는 표지가 아니고, 두 진영의 다툼은 원칙의 내용이 아니라 **그 원칙에서 무엇이
  따라 나오는가**로 옮겨 갔다. 이 KB는 이 축을 대립 축으로 쓰지 않는다.
- **넷 — 학파의 명단이 자기 신고다.** 부록이 학파에 속하려면 어떻게 하는지를 적는데,
  그 절차가 **이메일을 보내는 것**이다 (§Appendix, "Members of the Context-Driven
  School").[^kaner2002-lessons] 명단에 오른 저자들은 "이 원칙에 동의한다고 스스로 밝힌
  사람들(have identified themselves as agreeing with these principles)"이라고 적힌다.
  심사도 자격도 없으므로 **명단의 길이는 원칙의 근거가 아니다.**

## LLM 시대의 지위

이 절은 원 소스의 주장이 아니라 **이 KB의 읽기**다.

- **원칙 1·2는 경험적 재검의 대상이 아니다.** 이것은 측정 결과가 아니라 판단의 형식을
  정하는 조항이므로, 새 도구가 나왔다고 참·거짓이 다시 정해지지 않는다. 낡을 수 있는
  것은 원칙이 아니라 아래에 딸린 예시와 lesson들이다.
- **오히려 이 원칙은 모델이 만든 판단을 심사하는 쪽의 근거로 선다.** 모델은 훈련
  분포에서 흔한 것을 답으로 내놓기 쉽고, 그것은 정의상 **맥락과 무관한 최상급**의 모양을
  한다. 원칙 2는 그 답이 왜 그 자리에서 성립하는지를 되묻게 만드는 조항이므로, **단일
  진리를 거부하는 심사 자체가 이 원칙에 기대어 선다.**
- #hypothesis **다만 원칙이 심사 규칙으로 쓰이면 반증 불가능해진다.** "맥락이 다르다"는
  어떤 반례에도 붙일 수 있는 답이고, 이 선언은 그 남용을 막는 조건을 적지 않았다.
  머리말이 그 자리에 놓은 것은 규칙이 아니라 **독자가 스스로 물어볼 질문 목록**이다
  (§Preface, "How to Use This Book").[^kaner2002-lessons]

## 이어지는 페이지

- [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md) — 이 원칙을 세운
  저자 둘이 십 년 뒤 자동화의 경계를 낱말로 가른 자리
- [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md) — 그
  구분에 대한 같은 학파 안의 반박. 반박이 근거로 부르는 "맥락 주도 테스팅의 전제"가 이
  페이지의 원칙 1·2다
- [버그 옹호](../concepts/bug-advocacy.md) — 같은 책의 다른 호출자. 결함 보고를 설득
  문서로 다루는 장이고, 보고의 양을 무엇이 제한하는가가 그 페이지의 물음이다
- [코코넛은 통하지 않는다](../concepts/coconuts-dont-cut-it.md) — 같은 금지가 방법론 채택
  쪽에서 되풀이되는 자리. 형식만 옮겨 오는 실패를 화물 숭배로 진단한다
- [기술 선택 기준](../concepts/technology-selection-criteria.md) — 유행이 아니라 맥락으로
  고르라는 같은 규칙이 도구 선택에 걸리는 자리
- [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md) —
  벤더 실무 문면이 "이렇게 하라"를 적는 자리. 원칙 2가 그 문면을 보편 규칙으로 읽지 말라고
  요구하는 조항이다
- [테스팅에서 자동화의 경계](../synthesis/automation-boundary-in-testing.md) — 이 갈래의 허브.
  이 원칙이 그 갈래의 헌법 자리에 놓이는 이유를 허브가 적는다

[^kaner2002-lessons]: Kaner, Bach & Pettichord 2002, *Lessons Learned in Software
    Testing*. **확보본이 Wiley 전자책 판이라 인쇄 쪽 앵커가 하나도 없다** — EPUB 전체에
    pagebreak 표식이 0건이므로 이 페이지의 locator는 **장 번호 + lesson 번호**이고,
    lesson 번호가 없는 자리는 §Preface·§Appendix 아래의 **소제목**으로 적었다. 규약의
    정본은 `it/archive/kaner2002-lessons/_progress.yaml` 머리말이다. 부록 도입 문단의
    직인용은 원문에서 첫 낱말이 장식 대문자 때문에 `W e belong`으로 분리돼 추출되는데,
    이 페이지는 그것을 `We belong`으로 되붙여 적었다 — 조판 흔적을 되돌린 것이지 문면을
    고친 것이 아니다. 일곱 원칙과 예시의 따옴표·대시는 원문 조판 그대로가 아니라
    이 KB의 문자 규약(NFC)에 맞춰 옮겼고 낱말은 한 자도 바꾸지 않았다. **이 책의 수치는
    옮기지 않는다** — 근거 등급이 실무자 선언이므로 저자들이 경험에서 추정한 값은 측정이
    아니다.
