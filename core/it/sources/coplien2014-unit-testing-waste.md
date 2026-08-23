---
type: report
title: "Why Most Unit Testing is Waste"
author:
  - { family: "Coplien", given: "James O." }
issued: "2014"
URL: "http://www.rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf"
custom:
  archive-url: "https://web.archive.org/web/20230923190457/https://rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf"
snapshot: /it/archive/coplien2014-unit-testing-waste/
snapshot_sha256: "0488be2e83cb3fb315cae3d6f1b5bdc36372465b4719b5da64439fc92576fd2d"
accessed: "2026-08-24"
---

# coplien2014-unit-testing-waste

- [지위 — 동료심사 없는 뉴스레터 글이다](#지위--동료심사-없는-뉴스레터-글이다)
- [원 게재처가 죽었고 아카이브가 실질 정본이다](#원-게재처가-죽었고-아카이브가-실질-정본이다)
- [판이 둘이다](#판이-둘이다)
- [참고문헌 상태 — 목록은 없고 본문 인용이 둘이다](#참고문헌-상태--목록은-없고-본문-인용이-둘이다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [대장 기재와 어긋난 것](#대장-기재와-어긋난-것)
- [반입 범위](#반입-범위)
- [이 소스가 닿을 자리](#이-소스가-닿을-자리)

**단위 테스트(unit test)의 값어치를 정면으로 낮게 매기고, 대신 시스템 테스트와 단정
(assertion)으로 무게를 옮기라고 주장하는 실무자 에세이.** 이 KB가 이것을 들이는 이유는 이
글의 결론을 받아들이기 때문이 아니라, 단위 테스트 비중을 두고 갈리는 논쟁에서 **한쪽 극의
문면이 여기에 있기** 때문이다. 반대 극은
[구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)이
소유한다.

## 지위 — 동료심사 없는 뉴스레터 글이다

- **근거 등급은 `essay`다.** 실험도 표본도 통제도 없고, 이 글에 실린 수치는 전부 저자가
  본문에서 세운 어림 계산이거나 예시다. **이 소스는 "학술 근거"로 인용되지 않는다.**
- **동료심사를 받은 흔적이 문면에 없다.** 확보본에는 학회·저널의 조판 표면(권·호·쪽수·접수
  일자·편집 이력)이 한 줄도 없다. 쪽 머리글은 제목 반복(`Why Most Unit Testing is Waste`)
  하나뿐이다.
- **글 자신이 자기 게재처를 뉴스레터로 부른다** — 말미에서 독자에게 저자 주소로 의견을 보내고
  **`copy Rex at the address at the front of this newsletter`** 하라고 적는다(§1.10). 그
  `front of this newsletter`(앞표지·머리면)는 **확보본에 들어 있지 않다.** 확보본은 이 글
  한 편만 담은 PDF이고, 뉴스레터 전체가 아니다.
  - 그러므로 **게재처 이름·호수·발행일을 이 소스의 문면으로 적을 수 없다.** 원 게재 주소가
    `rbcs-us.com`이라는 것과 본문의 `Rex`가 이 KB가 가진 전부이며, 그 둘을 이어 발행 주체를
    단정하는 것은 추론이지 문면이 아니다. `container-title`을 비워 둔 이유가 이것이다.
  - **`type: report`은 기관 보고서라는 주장이 아니다.** 이 KB의 타입 열 가운데 쪽이 매겨진
    자체 조판 PDF가 들어가는 자리가 그것이고(선례: `marick1999-coverage` — 같은 꼴의 실무자
    PDF), 진행 기록의 단위를 쪽으로 둘 수 있게 하는 것도 그 타입이다. **발행 주체에 대한
    주장은 이 필드에 없다.**
- **저자의 자기 한정이 마지막 절에 있다**(§1.10):

  > As for the Internet: it's sad, and frankly scary, that there isn't much out there.
  > There's a lot of advice, but very little of it is backed either by theory, data, or even
  > a model of why you should believe a given piece of advice. Good testing begs skepticism.
  > Be skeptical of yourself: measure, prove, retry. Be skeptical of *me* for heaven's sake.

  **이것이 확보본에 실재하는 유일한 자기 한정 문장이다.** 이 글을 인용할 때 저자의 지위
  규정으로 쓸 것은 이 문면이다.

## 원 게재처가 죽었고 아카이브가 실질 정본이다

**원 주소는 응답하지 않는다.** 이 KB의 확보본은 인터넷 아카이브(Wayback Machine)가 뜬 마지막
성공 캡처이고, 그 사실을 확보 회차가 아니라 **이 반입이 캡처 목록으로 직접 확인했다**
(2026-08-24, Wayback CDX 조회).

| 항목 | 값 |
|---|---|
| 원 주소 | `http://www.rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf` |
| 마지막 성공 캡처 | 2023-09-23 19:04:57 UTC (`20230923190457`, HTTP 200, `application/pdf`) |
| 그 뒤의 캡처 | 2025년까지 여럿 있으나 전부 301·404 (본문이 돌아오지 않는다) |
| 아카이브 주소 | `custom.archive-url` (프론트매터) |

- **확보본이 그 캡처와 바이트 동일이다.** 확보본의 SHA-1을 Wayback 캡처 목록의 다이제스트
  표기(base32)로 바꾸면 `HVRKDW6FEKZGUJFVE4OCMZEMEJFSMVBQ`이고, 2023-09-23 캡처의
  다이제스트와 **글자 하나까지 같다.** 이 KB가 가진 파일이 아카이브가 보존한 바로 그
  바이트열이라는 뜻이다.
- **같은 다이제스트가 2014-09-03 캡처부터 2023-09-23 캡처까지 이어진다.** 원 게재처는 9년
  동안 이 파일을 한 번도 바꾸지 않았다. **그래서 "아카이브본이라 판이 흔들릴 수 있다"는
  걱정이 이 소스에는 해당하지 않는다.**
- **현행판 대조는 불가능하다** — 원 주소가 죽었으므로 대조할 현행판이 존재하지 않는다.

## 판이 둘이다

**Wayback 캡처 목록에 남은 서로 다른 본문은 둘뿐이고, 확보본은 뒤엣것이다.**

| 판 | 캡처 | PDF 생성 일자(문서 메타) | 쪽수 |
|---|---|---|---|
| 앞판 | 2014-03-06 한 건 | 2014-02-27 | 19쪽 |
| **확보본** | 2014-09-03 ~ 2023-09-23 | **2014-08-05** | **21쪽** |

- **두 판의 차이는 덜어낸 것이 아니라 보탠 것이다.** 확보본에만 있는 것은 §1.9
  `"It's the process, stupid," or: Green Bar Fever` 절 전체, §1.3의 100% 커버리지 정의
  문단, 그리고 §1.5 끝의 `their hopes, stereotypes, or sometimes wishes` 구절이다. 앞판에
  있고 확보본에 없는 문단은 대조에서 나오지 않았다.
- **그러므로 확보본은 이 글의 마지막 판이다.** `issued`를 `"2014"`로만 적은 이유는 문서
  안에 발행일이 인쇄돼 있지 않고, 문서 메타의 생성 일자는 조판 시각이지 게재일이 아니기
  때문이다.
- **문서 메타의 `Company` 값이 `Gertrud&Cope`다** — 저자 본인의 회사이고, 본문에 아내
  이름 `Gertrud`가 나온다(§1.10). **저자가 직접 조판한 PDF**라는 뜻이므로, 게재처가 붙였을
  조판 표면을 이 파일에서 찾을 수 없는 것이 자연스럽다.

## 참고문헌 상태 — 목록은 없고 본문 인용이 둘이다

**참고문헌 목록(References·Bibliography)이 없다.** 확보본 전문 검색으로 확인했다. 다만
**"인용이 하나도 없다"고 적으면 그것도 틀린다** — 본문 괄호 안에 문헌 인용이 둘 있다.

| 어디 | 무엇 | 이 글이 그것을 무엇으로 쓰는가 |
|---|---|---|
| §1.6 | Perry and Kaiser, "Adequate Testing and Object-oriented Programming", *Journal of Object-Oriented Programming* 2(5), Jan. 1990, p. 13 | 프로그램 전체를 다시 시험해야 한다는 주장의 `formal proof` 근거 |
| §1.8 | Janzen and **Saledian**, "Does Test-Driven Development Really Improve Software Design Quality?", *IEEE Software* 25(2), March/April 2008, pp. 77-84 | TDD가 결합도·응집도를 개선한다는 통념을 `debunk`하는 실증 논문의 예 |

- **`Saledian`은 확보본의 표기 그대로다.** 실제 저자는 Saiedian이고, 이 오식은 두 판 모두에
  있다. 이 KB가 그 이름을 적을 때는 확보본 표기와 실제 표기를 함께 적는다.
- **웹 주소 인용이 하나 더 있다**(§1.3 자동화 논거 — computer.org의 autonomation 블로그).
  본문에 주소가 그대로 박혀 있고 저자·제목 표기는 없다.
- **이 둘은 전부 2차 경유다.** 원 논문을 이 KB가 확보하지 않았으므로, 이 글이 그 논문을
  어떻게 인용했는가까지만 쓰고 그 논문이 실제로 무엇을 보였는가는 쓰지 않는다.

## 인용할 때 지킬 것

- **수치를 실증으로 쓰지 않는다.** 이 글의 숫자는 전부 저자의 어림 계산이다 —
  `one trillionth`(§1.2, 근거로 `average object size is four words`와 `16-bit words`라는
  가정을 스스로 밝힌다), `1 in 10^12`(§1.3), `three system-affecting bugs per thousand lines
  of code`(§1.7, 출처 없음), `FIT rate of 10`(§1.6, 하드웨어 관례 설명). **어느 것도 이 글이
  잰 값이 아니다.**
- **인용 형태가 두 층이다 — 둘 다 옮긴다.** 본문 권고 상자(☞)는 권고형이고 말미
  「In summary」 불릿은 단정형이며, 같은 주장이 두 층에서 다른 세기로 적혀 있다. 한쪽만
  옮기면 이 글의 주장 세기를 잘못 전한다. 대조표는
  [단위 테스트는 대부분 낭비인가](../concepts/unit-testing-as-waste.md)의
  해당 절이 소유한다.
- **`waste`를 저자가 정의하지 않는다.** 제목의 낱말이고 본문이 린(Lean)·도요타 생산 방식을
  끌어오지만(§1.3), 무엇을 낭비로 세는지의 정의절이 없다. 이 낱말을 인용할 때 정의를 보태지
  않는다.
- **언어 모델 시대의 재검이 없다.** 2014년 글이고, 생성된 테스트에는 이 글의 논거 가운데
  유지 비용 쪽 전제(사람이 테스트를 손으로 고친다)가 그대로 서지 않는다. 이 KB는 그 재검을
  갖고 있지 않으므로 **없다고 적는다.**
- **논쟁의 한 극으로만 인용한다.** 이 글을 단독으로 인용해 "단위 테스트는 낭비다"를 이 KB의
  판정으로 만들지 않는다. `contradicts` 상대와 함께 읽는다.

## 대장 기재와 어긋난 것

- **대장(`queue.yaml`)의 `corrections`가 확보본을 "10쪽 PDF"라고 적었으나 21쪽이다.**
  앞판도 19쪽이라 10쪽인 판은 캡처 목록에 없다. 정정 후보다.
- **대장의 `verdict_note`가 저자 자인으로 인용한 "우리 중 누구도 hard data를 내놓지
  않았다"는 확보본에 없다.** 두 판 모두 `hard data`가 0회다. 저자의 자기 한정에 해당하는
  실제 문면은 위 "지위" 절에 옮긴 §1.10 문단이고, 이 KB는 그것만 쓴다. 저 문장이 어디서
  왔는지는 이 소스로 답할 수 없다 — **2차 경유 딱지를 달고 인용하지 않는다.**

## 반입 범위

이 런은 확보본 전문 21쪽(§1.1~§1.10과 말미 「In summary」 불릿 여덟)을 읽었다. 페이지로
옮긴 것은 주장의 뼈대(정보 이론 논거·계산 복잡도 논거·유지 비용 논거·심리 논거), 권고
상자와 요약 불릿의 문면과 그 두 층의 차이, 저자가 값어치를 인정한 예외 셋, 유일한 학술
인용의 용법, 그리고 이 글의 내부 모순이다.

옮기지 않은 것: 저자의 일화 서사 상당 부분(§1.10의 세르비아·케냐·펀치 카드 회고), 고객
Richard Jacobs의 편지 전문(요지만 옮겼다), 하드웨어 최악 사례 분석(WCA)의 세부다.

## 이 소스가 닿을 자리

- [단위 테스트는 대부분 낭비인가](../concepts/unit-testing-as-waste.md) — 이 소스가 세우는
  페이지
- [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)
  — `contradicts` 상대 극
