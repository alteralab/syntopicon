---
type: post-weblog
title: "Code Coverage Best Practices"
author:
  - { family: "Arguelles", given: "Carlos" }
  - { family: "Ivanković", given: "Marko" }
  - { family: "Bender", given: "Adam" }
issued: "2020-08-07"
container-title: "Google Testing Blog"
URL: "https://testing.googleblog.com/2020/08/code-coverage-best-practices.html"
snapshot: /it/archive/arguelles2020-coverage/
snapshot_sha256: "0d497f51044a056d17d6b36c813bdb6a4aecf750ffdcc6376b25c0c60d4629ad"
accessed: "2026-08-23"
---

# arguelles2020-coverage

**커버리지를 어떻게 운용할 것인가를 한 회사가 사내 합의문 형태로 낸 글.** 커버리지가
효과성을 예측하느냐는 실증 논쟁 뒤에 나와, 그 논쟁을 판정하지 않고 **"그래서 실무에서는
이렇게 한다"**를 열두 개 남짓한 굵은 문장으로 적는다.

## 지위 — 산업 규범이지 실증이 아니다

- **근거 등급은 `industry-norm`이다.** 측정도 표본도 통제도 없다. 이 글에 실린 수치는
  전부 회사가 권고로 정한 값이거나 저자들의 경험 진술이고, **분모도 집계 절차도 인쇄돼
  있지 않다.** 이 KB의 어떤 페이지도 이 글의 수치를 측정값으로 인용하지 않는다.
- **저자들이 스스로 규정하는 자리가 첫 문단이다** — `We have spent several decades
  driving software testing initiatives in various very large software companies` 그리고
  `The purpose of this document is to give you tools to steer people on all ends of the
  spectrum to find common ground`. **재서 보인 것이 아니라 논쟁을 멈추려고 쓴 합의문이다.**
- **이 글 자신이 실증의 부재를 인정한다** — `It is an open research question whether code
  coverage alone reduces defects, but our experience shows…`. 뒤이어 오는 근거가
  `our experience`이므로, **효과의 근거로 쓸 수 없다는 것을 원문이 먼저 적어 둔 셈이다.**
- **규모 전제를 떼면 옮겨지지 않는다.** 코드 리뷰에 커버리지를 심는 배선, 파이프라인
  전체의 집계 커버리지, 커밋 단위 관문은 전부 그런 인프라가 이미 있는 조직의 그림이다.

## 판과 서지 — 살아 있는 웹 문서다

- **게시일이 문면에 인쇄돼 있다**: `Friday, August 07, 2020` (`itemprop='datePublished'`).
- **저자 세 사람이 문면에 인쇄돼 있다**: `By Carlos Arguelles, Marko Ivanković, and Adam
  Bender`. 글 아래 라벨도 같은 세 이름이다.
- **살아 있는 페이지이므로 열람일 스탬프를 단다.** 이 KB의 직인용은 **2026-08-23
  열람본**에 대한 것이다.

| 시점 | 무엇 | 아카이브 안의 파일 |
|---|---|---|
| 2026-08-20 | 확보(`verify-ingest`)한 최초 스냅샷 | `google-coverage2020.html` |
| 2026-08-23 | 반입 시점 재열람·재취득 | `code-coverage-best-practices--refetch-2026-08-23.html` |

**두 판의 렌더 본문은 완전히 같다.** 태그를 벗겨 낸 텍스트가 16,660자로 한 글자도
다르지 않았고, 직인용한 구절도 두 파일 모두에 있다. 원본 HTML의 바이트는 다르지만
(블로그 플랫폼이 매 요청마다 넣는 동적 조각) **본문에는 판본 함정이 없다.** 다만 없었다는
사실은 이 두 시점에서만 참이다.

- **댓글이 페이지에 붙어 있다**(2020~2021년 셋). 저자의 글이 아니므로 이 KB는 옮기지
  않는다. `New comments are not allowed.`가 인쇄돼 있어 더 늘지 않는다.

## 인용할 때 지킬 것

- **60/75/90%는 측정값이 아니라 회사가 정한 권고 구간이다.** 원문이 그 값을
  `general guidelines`라 부르고 바로 다음 문장에서 하향식 강제를 피한다고 적는다.
  이 값을 인용할 때는 **분모가 없다는 사실과 규모 전제를 함께 적는다.**
- **이 글이 링크하는 두 논문의 내용을 이 글 경유로 옮기지 않는다** — 뮤테이션 권고에
  걸린 `research.google/pubs/pub46584`와 마지막 줄의 `"Coverage at Google"`
  (`research.google/pubs/pub48413`)이다. 원전으로 가서 읽는다.
- **이 글은 생성 테스트를 다루지 않는다.** 2020년의 실무 문면이고, 생성 시대의 함의는
  이 KB의 읽기이지 이 글의 주장이 아니다.

## 반입 범위

이 런은 확보본 전문(본문 열두 개 남짓한 굵은 문장 전부와 서문 두 문단)을 읽었다.
페이지로 옮긴 것은 지표의 성격 규정, 안 덮인 곳을 읽으라는 조문, 이상적 수치의 부재와
하향식 강제 회피, 권고 구간과 커밋 단위 임계, 코드 리뷰 배선, 통합·파이프라인 집계,
관문 권고와 그 자기 단서, 그리고 단언 실질성에 뮤테이션을 권고하는 대목이다.

옮기지 않은 것: 댓글 셋, 블로그 사이드바(라벨·아카이브 목록), 그리고 두 논문 링크의
내용이다.
