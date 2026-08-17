---
type: book
title: "Fluent Python: Clear, Concise, and Effective Programming"
author: [{family: Ramalho, given: Luciano}]
issued: "2022"
publisher: "O'Reilly Media"
ISBN: "9781492056355"
edition: 2
snapshot: /it/archive/ramalho2022/
snapshot_sha256: "5fe4c4f87418e594e1b420e60e496d1466ffef3ad622e0187092a59b42a2ca58"
accessed: "2026-08-18"
---

# Fluent Python, Second Edition

파이썬의 관용 표현(idiom)을 언어의 내부 규약에서부터 설명하는 참조서. 24개 장이
특수 메서드·자료 구조·일급 함수·클래스와 프로토콜·제어 흐름·메타프로그래밍을 훑는다.

이 KB에서 이 소스의 지위는 **1차 — 파이썬 관용 참조**다. 원전이 아니다. 코드 품질 축의
원리는 [Ousterhout](ousterhout2021.md)·[Fowler](fowler2018.md)·[Beck](beck2023.md)이
말하고, 그 원리의 파이썬 실물은 [Percival & Gregory](percival2020.md)가 보인다. 이 책은
그 실물이 쓰는 **언어 기능 자체의 정본 근거**를 댄다 — `dataclass`가 무엇을 생성하는지,
`typing.Protocol`과 추상 기반 클래스가 어떻게 갈리는지 같은 것들이다.

- **스냅샷은 정식 출간본 PDF다** — 판권장이 "April 2022: Second Edition",
  "Revision History for the Second Edition: 2022-03-31 First Release", "Copyright ©
  2022"이고 표지가 "Covers Python 3.10"이다. 1011쪽, 텍스트 레이어 신뢰 가능
  (OCR 필요 0쪽).
- **⚠ 2026-08-18에 스냅샷을 교체했다.** 그 전날 반입된 첫 런(2026-08-17, 1·5·13장)은
  **Early Release(사전 공개판) 12차 릴리스(2021-07-27, 25개 장, 파이썬 3.9 기준)**를 보고
  있었다. 판정 근거와 두 판본의 실측 차이는
  `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 그 런의 산출물은 이 교체와
  함께 최종판 기준으로 전면 재정합했으므로, **현재 코퍼스에 Early Release를 가리키는
  각주는 없다.**
- **인쇄판 쪽 앵커가 있다.** locator는 `N장 §"절 제목", p.NN` 꼴이고, 쪽은 **PDF 쪽에서
  30을 뺀 인쇄판 쪽**이다(1장 시작 = PDF 33쪽 = 인쇄판 3쪽). 오프셋은 색인까지 일정하다 —
  실측 절차는 `_progress.yaml` 머리말이 정본이다.
- **정식판의 장 구성은 24개 장·5개 부다.** 1~16장은 Early Release와 번호가 같고,
  17장 이후가 다르다(사전 공개판의 17장과 19장이 정식판 17장으로 합쳐졌다). 부 구성도
  다르다 — 사전 공개판의 "I부 Prologue"가 없어지고 1장이 "I부 Data Structures"에 들어간다.
- **표지가 "Covers Python 3.10"이라 적지만 본문의 여러 자리가 파이썬 3.9 시점에서
  쓰였다.** 5장이 Mypy 0.910을 실측하고 저자가 그 절에서 "나는 파이썬 3.9를 쓰고 있다"고
  적는다. 그래서 3.10이 `@dataclass`에 더한 `slots`·`kw_only`·`match_args`는 **책 전체에
  한 번도 나오지 않는다**(전문 검색 실측 0건). 해당 자리에 버전 조건을 달아 두었다.
- 본문의 그림(Figure)은 전부 이미지로 조판돼 있어 산문 서술로만 옮겼다. 특히 13장의
  Typing Map(Figure 13-1)은 이 장 전체의 뼈대인데 이미지라 네 사분면의 축을 그림 설명
  캡션에서 판독해 옮겼다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.
- 반입 재개점의 정본은 `it/archive/ramalho2022/_progress.yaml`이다.
