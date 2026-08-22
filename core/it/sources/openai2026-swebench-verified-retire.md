---
type: webpage
title: "Why SWE-bench Verified no longer measures frontier coding capabilities"
author:
  - { literal: "OpenAI" }
issued: "2026-02-23"
URL: "https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/"
custom: {archive-url: "https://web.archive.org/web/20260811105804id_/https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/"}
snapshot: /it/archive/openai2026-swebench-verified-retire/
snapshot_sha256: "0a2084fded4b8783babde2c003f8da96f294d4ac38c538e01c552c2e739d796f"
accessed: "2026-08-22"
---

# openai2026-swebench-verified-retire

자기가 2024년에 만든 벤치마크 부분집합을 2026년에 **더는 쓰지 않겠다고 밝히고 그 근거를
공개한 벤더 문서**다. 이 KB에서는 [원전](jimenez2024-swebench.md)과 한 페이지에 묶어
**한 벤치마크의 채택과 철회**를 보이는 데 쓴다.

## 지위 — 산업 보고(industry report), 벤더의 자기 보고

- **학술 근거가 아니다.** 심사도 재현 자료도 없고, 저자는 평가 대상 모델을 파는 회사다.
  이 문서의 수치는 전부 **OpenAI가 스스로 잰 값**이고, 이 KB는 그것을 그렇게 표기해서만
  인용한다.
- **이해가 걸린 자리가 둘이다.** 이 회사는 (1) 철회 대상인 SWE-bench Verified를
  **자기가 만들었고**, (2) 대안으로 권하는 SWE-bench Pro의 점수로 자기 모델을 보고한다.
  감사의 근거 자체를 무르게 만들지는 않지만, 권고를 읽을 때 적어 둘 조건이다.
- **살아있는 문서**다. 언제든 개정되며 이 소스가 보증하는 것은 아래 캡처 시점의 문면
  하나뿐이다.

## 확보 경로 — 라이브 403, Wayback 경유 사본

| 시점 | 무엇 |
|---|---|
| 2026-02-23 | 게시일. 문서 상단에 `February 23, 2026`으로 인쇄돼 있다 |
| 2026-08-11 | Wayback 캡처 시각 `20260811105804`(UTC). 이 KB의 스냅샷 원본 |
| 2026-08-22 | 이 KB의 열람·반입일 |

라이브 URL은 브라우저 UA를 붙인 `curl`과 WebFetch 양쪽에서 **403**이다. 그래서
Wayback Machine의 `id_` 모드(툴바 주입 없는 원본 바이트)로 받았다. 확보 경위는
스냅샷의 `_acquisition-note.txt`에 있다(밑줄 접두 = 우리가 만든 파일이라 다이제스트
밖이다).

**"2차 경유" 딱지는 붙지 않는다.** 사본의 경로가 아카이브일 뿐 문면은 원문이고,
`<link rel="canonical">`이 정본 URL을 가리키며 제목·게시일·절 구성·인용할 수치가
모두 스냅샷 안에 실재한다. 다만 **캡처가 게시 약 5.5개월 뒤**이므로, 이 사본이
보증하는 것은 그 시점의 문면이다.

## 인용 규칙

- **본문 절의 수치만 옮긴다.** 이 문서는 목차 위에 요약(lede)을 두고 같은 값을 본문
  절에서 다시 적는다. 요약에만 있는 값은 쓰지 않는다.

  | 요약이 적는 값 | 본문 절이 적는 값 | 처리 |
  |---|---|---|
  | `at least 59.4%` of the audited problems | `59.4% of the 138 problems` (Too narrow and too wide tests 절) | 본문 값을 쓴다 |
  | `27.6% subset` of the dataset | 감사 대상 `138`문항(같은 절) · Verified `500`문항(Background 절) | 두 본문 값을 쓰고 비율은 적지 않는다 |
  | `74.9%` → `80.9%` in the last 6 months | 없다 | **쓰지 않는다**(아래) |

- **`74.9% → 80.9%`는 제3자 수치다.** 요약의 `improving`이라는 낱말에 걸린 링크가
  `llm-stats.com/benchmarks/swe-bench-verified`, 곧 외부 리더보드 집계다. OpenAI가
  잰 값이 아니고 이 KB는 그 리더보드를 원전으로 확인하지 않았으므로 **옮기지 않는다.**
- **감사의 분모는 무작위 표본이 아니다.** 138문항은 `OpenAI o3가 64회 독립 실행에서
  일관되게 풀지 못한` 문항이다. 곧 어려운 쪽으로 치우친 표본이고, `59.4%`를 "Verified
  500문항의 59.4%가 결함"으로 읽으면 원문이 하지 않은 주장이 된다.
- **오염 탐침의 대상 모델에는 저자 자신의 단서가 붙는다** — 추론 모델을 빼려고 고른
  구성이고, 세 모델 사이에 무시할 수 없는 역량 차가 있을 것이라고 문서가 스스로 적는다.
- **`SWE-bench Pro`·`GDPval`은 이름만 옮긴다.** 이 문서 안에 그 벤치마크의 수치가 없고,
  이 KB는 그 원문을 확보하지 않았다.

## 이 소스가 닿을 자리

- [벤치마크의 수명과 철회](../concepts/benchmark-lifespan-and-retirement.md) — 이 소스가
  세우는 페이지의 뒤쪽 절반(무엇이 드러났고 무엇을 권고했나)
