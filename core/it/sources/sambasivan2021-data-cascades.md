---
type: paper-conference
title: "'Everyone wants to do the model work, not the data work': Data Cascades in High-Stakes AI"
author:
  - { family: "Sambasivan", given: "Nithya" }
  - { family: "Kapania", given: "Shivani" }
  - { family: "Highfill", given: "Hannah" }
  - { family: "Akrong", given: "Diana" }
  - { family: "Paritosh", given: "Praveen" }
  - { family: "Aroyo", given: "Lora" }
issued: "2021"
event-title: "CHI Conference on Human Factors in Computing Systems (CHI '21)"
event-place: "Yokohama, Japan"
publisher: "ACM"
publisher-place: "New York, NY, USA"
DOI: "10.1145/3411764.3445518"
ISBN: "978-1-4503-8096-6"
number-of-pages: "15"
snapshot: /it/archive/sambasivan2021-data-cascades/
snapshot_sha256: "2f54477a1decbc45f0f0059363814ae9f688e25e2c1a7f77e9984a2c829584d2"
accessed: "2026-08-25"
---

# sambasivan2021-data-cascades

**데이터 품질 문제가 고위험(high-stakes) AI 현장에서 어떻게 하류로 번지는가**를
인도·동서 아프리카·미국의 AI 실무자 53명 인터뷰로 답한 질적 연구. 답은 **데이터
캐스케이드(data cascades)** — 상류에서 촉발돼 하류에서 늦게, 불투명하게, 겹쳐서
나타나는 사건의 연쇄이며, 이 논문은 그것을 정의하고 유형 넷으로 가른다.

**이 소스가 이 KB에서 서는 자리는 데이터 검증 축의 사회기술적 근거다.** 상류에 검증을
두라는 처방을 기술 쪽에서 낸 소스들(Breck·Schelter)이 동기로만 말하고 재지 않은 것 —
검증이 없을 때 오염이 하류에서 실제로 무엇을 하는가 — 을 현장 증언으로 채운다.

## 지위 — 심사 학회 논문이되 정량 실험이 아니다

- **근거 등급은 `peer-reviewed`다**(대장 미기재 → 이 런의 판정). 1쪽에 ACM 참조 형식과
  DOI가 인쇄돼 있다 — `In CHI Conference on Human Factors in Computing Systems (CHI '21),
  May 8–13, 2021, Yokohama, Japan. ACM, New York, NY, USA, 15 pages.
  https://doi.org/10.1145/3411764.3445518`. ISBN `978-1-4503-8096-6/21/05`도 같은 자리에
  있다. CHI 전체 논문 트랙은 심사 트랙이다.
- **그러나 이 등급이 여는 것은 "정량 실증"이 아니다.** 이 논문은 **반구조화 인터뷰
  기반 질적 연구**이고, 실린 백분율은 **인터뷰 전사를 코딩해 센 자기 보고 빈도**다.
  통제군도, 실험 조작도, 측정 장치도 없다. 이 KB가 이 소스를 인용할 때 "실증"이라는
  낱말은 **현장 증언의 체계적 수집**을 뜻하지 정량 측정을 뜻하지 않는다.
- **권·호·논문 번호·쪽 범위는 확보본 문면에 없다.** 확보본에 인쇄된 쪽 번호도 없어
  이 KB의 locator는 **확보본 PDF 쪽(1~15)**과 절·표·그림 번호다. ACM DL 레코드의
  논문 번호를 페이지에 적지 않는다.
- **이 등급이 여는 것은 이 논문이 스스로 코딩한 값뿐이다.** 1절이 동기로 옮기는 제3자
  수치(IBM 암 치료 AI 정확도 저하, Google Flu Trends의 `missing the flu peak by 140%`
  등, PDF p.1)는 경유 값이고 동기 절의 수치라 이 KB는 옮기지 않는다.

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **표본**: 2020년 5~7월, 고위험 AI 응용에 종사하는 **AI 실무자 53명**과의 반구조화
  인터뷰. 1인당 약 75분 (§3, PDF p.4).
- **지역 분포(분모의 정본, Table 1, PDF p.5)**: 인도 23 · 미국 16 · 나이지리아 10 ·
  케냐 2 · 가나 1 · 우간다 1. 논문은 뒤 셋+나이지리아를 `East and West African
  countries` 14로 묶는다. 성별은 남 45 · 여 8. 소속은 스타트업 28 · 대기업 16 · 학계 9.
- **모집**: 개발자 커뮤니티·배포 목록·직업 네트워크·개인 연줄을 통한 **눈덩이 표집과
  의도적 표집**(snowball and purposive sampling)이며 포화까지 반복했다 (§3, PDF p.4).
  **무작위 표본이 아니므로 백분율은 모집단 추정치가 아니다.**
- **백분율의 정의가 §3에 명시돼 있다** (PDF p.4):

  > Numbers reported throughout the paper represent the percentage of participants who
  > self-reported a trigger, impact, or signal of data challenges in the interviews.
  > Percentages are derived from coding each transcript for each individual’s experiences
  > of cascades.

- **평정자 간 신뢰도를 재지 않았다** — `Since codes are our process, not product [80],
  IRR was not used` (§3, PDF p.4). 분석은 연구자 둘이 독립적으로 전 단위를 반복해 읽고
  포화까지 범주를 세운 뒤 그룹 토의로 다듬는 절차다.
- **분모는 전체 53이고, Table 2의 지역별 값만 하위 분모(23/14/16)를 쓴다.** 백분율이
  53분모와 정확히 맞는다는 산술 대조는 개념 페이지에 관측으로 적었다.
- **한계는 저자가 적는다** (§3 Limitations, PDF p.4): COVID-19로 전부 화상·전화로
  진행해 **작업 관찰(shadowing)과 맥락적 조사를 넣지 못했다**. 성비 편중도 표집 한계로
  스스로 밝힌다.

## 이 논문이 스스로 그은 경계

- **범위 한정**: `While our analysis is limited to high-stakes AI projects, we believe
  these challenges may exist in more or less amplified forms in all of AI development`
  (§5, PDF p.10). 뒷절은 **믿음**(believe)이지 측정이 아니다.
- **개인의 실천으로 풀리지 않는다고 못 박는다**: `Individuals can attempt to avoid data
  cascades in their model development, but a broader, systemic approach is needed for
  structural, sustainable shifts in how data is viewed in AI praxis` (§5, PDF p.10).
- **"best practices"가 아니다** — 보고된 개입·실천·작업 방식은 전부 참여자 **자기
  경험**으로 보고된 것이지 모범 사례로 제시된 것이 아니라고 §3이 명시한다 (PDF p.4).

## 반입 범위

이 런은 확보본 15쪽 전부를 읽었다. 페이지로 옮긴 것은 4절(캐스케이드의 정의·성질·
유형 넷과 Table 2), 3절(방법·표본·분석 절차·한계), 5절 중 goodness-of-data와 "AI 데이터
수명 주기의 가시성" 대목이다.

옮기지 않은 것: 2절 관련 연구가 경유해 전하는 제3자 수치와 문헌 지도, 1절 동기 절의
수치, 5절의 HCI 연구 의제·AI 교육 과정·글로벌 사우스 데이터 형평 논의(이 KB의 축 밖),
Figure 1 도해(구조는 산문으로만 옮겼다), 참고문헌 130여 항.

**추출 도구 주의**: 직전 두 런에서 `tools/pdftext.py`가 수식·기호를 오식한 실측이 있어
이 런은 본문을 `pdftotext -layout`으로 뽑고, **수치가 실린 pp.5·6·7·8을 150dpi 렌더
이미지로 다시 대조**했다. Table 1·Table 2의 모든 수치와 92%·45.3%·74%·75%를 렌더에서
육안 확인했고 어긋남은 없다.

**철자 주의**: 논문은 영국식 `-isation` 계열을 쓴다(`organisational`·`standardised`).
단 Figure 1 범례만 `Poor cross-organizational documentation`으로 `z`를 쓰고 Table 2는
`cross-organisational`이다. 직인용 시 그 자리의 표기를 그대로 옮긴다.
