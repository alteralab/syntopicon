---
type: concept
title: 메타안정 장애의 정의와 세 상태
description: 트리거가 사라진 뒤에도 스스로 유지되는 과부하라는 실패 부류의 정의 — 안정 상태와 취약 상태와 메타안정 장애 상태의 경계, 트리거가 제거되면 낫는 장애는 왜 이 부류가 아닌가, 취약 상태가 과부하 상태가 아니며 많은 시스템이 거기서 상시 운영된다는 관찰, 근본 원인이 트리거가 아니라 지속 효과라는 판정, 그리고 부하와 용량의 비로 안정 영역의 경계를 적은 후속 논문의 형식화
generated: { by: "claude-opus-5", at: "2026-09-07T06:30:00Z" }
sources:
  - { id: bronson2021-metastable, resource: /it/sources/bronson2021-metastable.md }
  - { id: huang2022-metastable-wild, resource: /it/sources/huang2022-metastable-wild.md }
---

# 메타안정 장애의 정의와 세 상태

- [정의](#정의)
- [트리거가 제거되면 낫는 장애는 이 부류가 아니다](#트리거가-제거되면-낫는-장애는-이-부류가-아니다)
- [세 상태와 그 사이의 전이](#세-상태와-그-사이의-전이)
- [취약 상태는 과부하 상태가 아니다](#취약-상태는-과부하-상태가-아니다)
- [근본 원인은 트리거가 아니라 지속 효과다](#근본-원인은-트리거가-아니라-지속-효과다)
- [왜 대규모 시스템에서 더 심한가](#왜-대규모-시스템에서-더-심한가)
- [버그가 아니라 창발 행동이다](#버그가-아니라-창발-행동이다)
- [부하와 용량으로 다시 쓴 모델](#부하와-용량으로-다시-쓴-모델)
- [안정 영역의 경계](#안정-영역의-경계)
- [흩어져 있던 이름들](#흩어져-있던-이름들)
- [이 실패 모델이 정하지 않는 것](#이-실패-모델이-정하지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **트리거가 사라진 뒤에도 스스로 유지되는 과부하란 무엇이고, 시스템이 그
상태에 들어가기 전과 후를 어떤 상태 이름으로 갈라 부르는가.**

## 정의

- 메타안정 장애(metastable failure)의 정의는 다음 한 문장이다 (§1,
  p.221):[^bronson2021-metastable]

> Metastable failures occur in open systems with an uncontrolled source of load
> where a trigger causes the system to enter a bad state that persists even when
> the trigger is removed.

- 그 나쁜 상태 안에서 무슨 일이 벌어지는가 — **굿풋(goodput, 쓸모 있는 일의 처리량)이 쓸 수
  없을 만큼 낮고, 시스템이 그 나쁜 상태를 벗어나지 못하게 막는 지속 효과(sustaining effect)가
  있다. 지속 효과는 대개 작업 증폭(work amplification)이나 전체 효율의 저하를 동반한다** (§1,
  p.221).[^bronson2021-metastable]
- 이름은 물리학에서 왔다 — 저자들은 **물리학의 메타안정성 정의에서 따와 이 나쁜 상태를
  메타안정 장애 상태(metastable failure state)라 부른다** (§1, p.221).[^bronson2021-metastable]
- 빠져나오는 데 필요한 것 — **메타안정 장애 상태를 떠나려면 시스템 재부팅이나 부하의 극적인
  감축 같은 강한 교정력이 필요하다** (§1, p.221).[^bronson2021-metastable]
- 후속 논문은 같은 것을 더 짧게 적는다 (§1, p.73):[^huang2022-metastable-wild]

> the state of a permanent overload with an ultra-low goodput (throughput of
> useful work)

- 정의에 박힌 조건 하나가 **개방 시스템(open system)**과 **통제되지 않는 부하원**이라는 점이다
  (§1, p.221).[^bronson2021-metastable] 부하가 앞 요청의 완료로만 생기는 폐쇄 모델에서는 이
  루프가 성립하지 않는다. 그 구분의 정의는
  [개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md)에 있다.

## 트리거가 제거되면 낫는 장애는 이 부류가 아니다

- 경계를 긋는 문장은 이것이다 (§1, p.221):[^bronson2021-metastable]

> Failures that resolve when the trigger is removed, such as a denial-of-service
> attack, limplock, or livelock, are not metastable.

- 그래서 이 부류의 판별 기준은 증상의 모양이 아니라 **트리거를 없앤 뒤에도 남는가**다.
  후속 논문은 그것을 이 부류를 다른 것과 가르는 표시로 적는다 — **메타안정 장애의 구별되는
  특징은 지속 효과가 트리거가 제거된 뒤에도 시스템을 메타안정 장애 상태에 붙잡아 둔다는
  것이다** (§1, p.73).[^huang2022-metastable-wild]

## 세 상태와 그 사이의 전이

- 수명 주기는 세 국면이다 (§1, p.221).[^bronson2021-metastable]
  - **안정 상태(stable state)**에서 시작한다.
  - **부하가 어떤 문턱을 넘으면 시스템은 취약 상태(vulnerable state)에 들어간다. 그 문턱은
    암묵적이고 눈에 보이지 않는다**.
  - **취약한 시스템은 건강하지만 트리거 때문에 회복 불가능한 메타안정 상태로 떨어질 수 있다**.
- 후속 논문은 세 상태를 부하 기준으로 다시 적는다 — **안정 상태는 시스템이 일시적 과부하에서
  스스로 회복할 만큼 부하가 낮은 상태이고, 취약 상태는 부하가 높지만 일시적 과부하가 없는 한
  그 부하를 잘 처리하는 상태다** (§1, p.73).[^huang2022-metastable-wild]
- 한 예에서 세 상태의 경계가 수로 나온다. 데이터베이스가 초당 질의 수 300 아래에서는 100 ms
  안에 답하지만 그보다 높은 부하에서는 지연이 자릿수로 나빠지고, 웹 애플리케이션은 질의 하나가
  1초 안에 돌아오지 않으면 재시도를 한 번 보낸다. 이때 **부하가 초당 150 질의 아래면 안정
  상태에 머물고, 150을 넘으면 트리거가 메타안정 상태로 밀어 넣을 수 있는 취약 상태가 되며,
  회복하려면 부하를 초당 150 질의 아래로 내리거나 재시도를 초당 20 질의 미만으로 제한해야
  한다** (§2.1, pp.222–223).[^bronson2021-metastable]

## 취약 상태는 과부하 상태가 아니다

- 오해를 막는 문장 — **취약 상태는 과부하 상태가 아니다. 시스템은 부하가 전혀 늘지 않아도
  취약 상태에서 몇 달이나 몇 년을 돌다가 메타안정 상태에 갇힐 수 있다** (§1,
  p.222).[^bronson2021-metastable]
- 더 중요한 관찰 — **실제로 많은 프로덕션 시스템은 취약 상태가 안정 상태보다 훨씬 효율이
  높기 때문에 항상 취약 상태에서 돌기를 택한다** (§1, p.222).[^bronson2021-metastable]
- 후속 논문이 든 예 — **초당 300 요청을 처리하는 데이터베이스 앞에 적중률 90%의 캐시를 두면
  초당 3,000 요청까지 서비스할 수 있다. 더 효율적이지만 이제 시스템은 취약 상태에서 도는데,
  캐시 장애가 데이터베이스를 처리할 수 없는 요청 수로 압도할 수 있기 때문이다** (§1,
  p.73).[^huang2022-metastable-wild]
- 그 선택이 왜 눈감고 하는 선택인가 — **복잡한 대규모 분산 시스템에서 우리는 취약 상태에서
  운영하겠다는 이 결정의 결과를 여러 조건 아래에서 분석할 능력이 없다. 부하가 늘면 어떻게
  되는가, 하류 지연이 늘면 어떻게 되는가, 메시지 크기가 커져 직렬화와 역직렬화가 CPU를 더
  먹기 시작하면 어떻게 되는가. 그래서 정상 조건에서 "얼마나 취약한" 상태로 돌지 고르는 것은
  최선의 추측이고 언제나 옳은 선택은 아니며, 이것이 우리가 메타안정 장애를 계속 겪는
  이유다** (§1, p.73).[^huang2022-metastable-wild]

## 근본 원인은 트리거가 아니라 지속 효과다

- 이 판정이 이 실패 모델의 실무적 핵심이다 — **메타안정 장애의 근본 원인은 트리거가 아니라
  지속시키는 피드백 루프라고 본다. 같은 장애 상태로 이끄는 트리거는 여럿이므로, 지속 효과를
  다루는 쪽이 앞으로의 장애를 막을 가능성이 훨씬 높다** (§3, p.224).[^bronson2021-metastable]
- 현장에서 벌어지는 오판 — **메타안정 장애가 관련된 중단은 처음에 트리거 탓으로 돌려지는 것이
  흔하지만, 진짜 근본 원인은 지속 효과다** (§1, p.222).[^bronson2021-metastable]
- 역설 하나 — **이 장애들의 근본 원인은 흔히 시스템의 효율이나 신뢰성을 개선하는 기능들이다**
  (§1, p.221).[^bronson2021-metastable]

## 왜 대규모 시스템에서 더 심한가

- **메타안정 장애는 초대규모 분산 시스템에 불균형하게 큰 영향을 미친다. 지속 효과는 문제를
  샤드·클러스터·데이터센터 경계를 넘어 퍼뜨릴 수 있다** (§1, p.222).[^bronson2021-metastable]
- 규모가 방어를 무력화한다 — **많은 피드백 루프의 세기가 규모에 비례하므로, 견고한 테스트와
  배포 체제조차 빠져나갈 수 있다** (§1, p.222).[^bronson2021-metastable]
- 가장 심한 중단에서는 **피드백 루프가 전염성을 띠어, 트리거에 노출되지 않은 부분까지 장애
  상태로 끌어들인다** (§1, p.222).[^bronson2021-metastable]
- 복구를 늦추는 것 — **트리거와 지속 효과의 차이 때문에 올바른 대응을 찾기 어려워지고, 복구
  시간이 늘어난다. 교정 조치로 부하를 차단하는 것 자체가 사용자에게 또 다른 지장이 될 수
  있다** (§1, p.222).[^bronson2021-metastable]

## 버그가 아니라 창발 행동이다

- 결론절의 성격 규정 — **메타안정 장애는 흔한 경우의 동작을 개선하는 최적화와 정책에서
  자연스럽게 생겨난다. 논리 버그가 아니라 창발 행동(emergent behavior)이며, 그것을 일으키는
  단위 테스트나 통합 테스트를 쓸 수 없다. 그래서 드물지만 파국적 효과를 낼 수 있다** (§5,
  p.226).[^bronson2021-metastable]
- 초록의 표현으로는 **현재 메타안정 장애는 블랙 스완 사건(black swan event)으로 나타난다.
  과거의 무엇도 그 가능성을 가리키지 않기 때문에 이상치이고, 영향이 심각하며, 예측하기보다
  사후에 설명하기가 훨씬 쉽다** (Abstract, p.221).[^bronson2021-metastable]
- 후속 논문도 같은 자리를 짚는다 — **메타안정 장애의 핵심 성질은 근본 원인이 특정 하드웨어
  장애나 소프트웨어 버그가 아니라는 것이다. 그것은 시스템의 창발 행동이며 흔한 경우를 위한
  최적화에서 자연스럽게 생겨난다** (§1, p.73).[^huang2022-metastable-wild] 그래서 다른 장애
  부류와의 관계도 갈린다 — **앞의 장애들이 메타안정 장애를 촉발하지 않았다면 그것들을
  식별하고 제거하는 것으로 시스템 기능이 회복된다. 그러나 촉발했다면 그것들을 제거해도 시스템
  기능은 회복되지 않는다** (§7, p.86).[^huang2022-metastable-wild]

## 부하와 용량으로 다시 쓴 모델

후속 논문은 정의 논문의 모델을 부하와 용량이라는 두 양으로 다시 적는다 (§3.1,
p.76).[^huang2022-metastable-wild]

- **시스템의 용량 C_sys(t)(C system)는 시스템이 초당 처리할 수 있는 추상 자원 단위(resource
  unit, RU)로 표현한다. 각 요청은 시스템 예산에서 얼마간의 RU를 소비한다**. 초당 100 RU를
  처리하는 시스템은 1 RU짜리 요청 100개 또는 2 RU짜리 요청 50개를 매초 처리할 수 있다 (§3.1,
  p.76).[^huang2022-metastable-wild]
- 부하 L_sys(t)(L system)는 초당 도착하는 일의 양을 같은 RU로 잰 것이고, **시스템이 과부하가
  아니려면 L_sys(t)가 C_sys(t)보다 작아야 한다** (§3.1, p.76).[^huang2022-metastable-wild]
- 증폭이 없는 양을 따로 부른다. **유기 부하(organic load) L_org(t)는 클라이언트에서 나온
  부하이며 부하 급증 같은 일시적 효과는 포함하되 재시도 같은 부하 증폭 효과는 포함하지
  않는다. 유기 용량(organic capacity) C_org(t)는 일시적 용량 감소는 포함하되 지속되는 저하는
  포함하지 않는다** (§3.1, p.76).[^huang2022-metastable-wild]
- 이 두 쌍의 차이가 곧 증폭이다. 그래서 이 모델에서 메타안정성은 **L_sys가 L_org를 넘어서
  자라거나 C_sys가 C_org 아래로 떨어지는 것**으로 나타난다 (§3.3,
  p.78).[^huang2022-metastable-wild] 증폭 기제의 분류는
  [지속 효과와 증폭 기제](../concepts/sustaining-effects-and-amplification.md)에 있다.

## 안정 영역의 경계

- 정의 논문이 문턱이 "암묵적이고 눈에 보이지 않는다"고만 적은 자리에, 후속 논문은 경계를
  식으로 적는다. 최대 부하 증폭 계수 w_L(w L)과 최대 용량 저하 증폭 계수 w_C(w C), 정상 용량
  C_norm(C normal)에 대해 안정 용량 C_stable(C stable)은 다음과 같다 (정리 2, §3.5.1,
  p.79):[^huang2022-metastable-wild]

  ```math
  C_{stable} = \frac{C_{norm}}{w_L \cdot w_C}
  ```

- 정리 2의 주장 — **정상 부하 L_norm이 C_stable보다 작으면 시스템은 결코 메타안정 장애를
  겪지 않는다** (§3.5.1, p.79).[^huang2022-metastable-wild] 뜻은 **정상 부하가 정상 용량에
  비해 충분히 낮으면, 트리거가 시스템을 과부하시키고 최대 증폭을 일으켜도 트리거가 제거되면
  회복한다**는 것이다 (§3.5.1, p.79).[^huang2022-metastable-wild]
- 실제 사례가 이 영역에 있었다 — **CAS2 사건에서 아파치 카산드라 클러스터는 용량의 10%에서
  30% 수준의 낮은 부하로 운영되고 있었다. 매우 큰 트리거와 부하 증폭에도 불구하고 트리거가
  제거되자 클러스터는 스스로 회복했다** (§3.5.1, p.79).[^huang2022-metastable-wild]
- 취약 상태 쪽은 이분법이 아니다 — **정의 논문은 취약 상태를 일시적 과부하가 메타안정 장애로
  기울일 만큼 부하가 높은 상태로 정의한다. 그러나 우리 실험에 따르면 취약 상태는 이분법이
  아니다. 그것에는 여러 정도가 있고 그 정도를 정하는 요인도 여럿이다** (§3.5.2,
  p.79).[^huang2022-metastable-wild] 그 요인들은
  [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md)에 있다.

## 흩어져 있던 이름들

- 이 현상 자체는 새롭지 않았고, 실무자들이 서로 다른 이름을 붙여 왔다 — **지속되는
  혼잡(persistent congestion), 과부하(overload), 연쇄 장애(cascading failures), 재시도
  폭풍(retry storm), 죽음의 나선(death spiral)** 같은 이름들이다 (§1,
  p.73).[^huang2022-metastable-wild] 후속 논문은 **정의 논문이 이 서로 달라 보이는 장애들을
  같은 틀 아래 일반화한 첫 작업**이라고 적는다 (§1, p.73).[^huang2022-metastable-wild]
- 단일 기계에도 같은 패턴이 있다 — **이 논문은 분산 시스템에 초점을 맞추지만 이 패턴이 그
  영역에 한정되지는 않는다. 예컨대 락의 콘보이 현상(convoy phenomenon)은 독립 실행 시스템에서
  일어난 메타안정 장애의 이른 사례다** (§1, p.222).[^bronson2021-metastable]
- KB 안에서 이 이름이 먼저 나온 자리는
  [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md)의 메타안정 장애 절이다.
  거기 실린 재시도 폭풍 서술이 여기 정의의 한 사례에 해당한다.

## 이 실패 모델이 정하지 않는 것

- 두 논문은 실패 모델과 그 분류를 세우고, 그 모델 안에서 어떤 대처가 왜 듣는지를 논한다.
  **재시도 예산·토큰 버킷·부하 차단의 구체적 알고리즘과 임계값을 정하는 것은 이 두 소스의
  범위가 아니다.** 정의 논문이 이 자리에서 하는 일은 기존 기법들을 "알려진 메타안정 장애에
  대응해 사후에 개발된 임시방편"으로 조사하는 것이고, **알려지지 않은 메타안정 장애에 견고한
  시스템을 짓는 체계적 접근은 열린 문제로 남아 있다**고 적는다 (Abstract,
  p.221).[^bronson2021-metastable]
- 임계값을 정할 때 쓸 재료는 이 소스들이 아니라 그 자리의 측정이다. 무엇을 재야 하는지는
  [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md)에 있다.

## 이어지는 페이지

- [메타안정 장애의 트리거](../concepts/metastable-failure-triggers.md) — 무엇이 시스템을 취약
  상태에서 밀어내는가, 그리고 트리거의 크기와 지속 시간이 왜 결과를 가르는가
- [지속 효과와 증폭 기제](../concepts/sustaining-effects-and-amplification.md) — 트리거가
  사라진 뒤에도 도는 그 피드백 루프의 종류
- [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md) — 숨은 용량, 특성
  지표, 취약도의 정도
- [공개 사후 분석에서 본 메타안정 장애](../concepts/metastable-failures-in-incident-reports.md) —
  이 정의를 실제 장애 보고서 스물두 건에 적용한 결과
- [메타안정 장애에서 복구하기](../concepts/recovering-from-metastable-failures.md) — 이미
  들어갔을 때 무엇을 하는가
- [개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md) — 정의가
  전제하는 그 개방 시스템의 정의
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — KB에서 이 이름이
  먼저 등장한 자리, 그리고 연쇄 장애와의 구분
- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 이 악순환이 시작되는 그
  처리량과 응답 시간의 곡선
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 페이지가 속한 허브

[^bronson2021-metastable]: Bronson, Aghayev, Charapko & Zhu 2021, "Metastable Failures in
    Distributed Systems", HotOS '21, pp.221–227. Abstract·§1 "Introduction"(pp.221–222),
    §2.1 "Request Retries"(pp.222–223), §3 "Approaches to Handling Metastability"(p.224),
    §5 "Conclusion"(p.226). 쪽수는 ACM 게재본 인쇄 쪽 기준이며 PDF 스냅샷 1–7쪽이
    pp.221–227에 해당한다. Figure 1(상태 전이도, p.221)과 Figure 2(굿풋 곡선, p.222)는
    도해라 옮기지 않았고, 본문이 서술한 수치만 인용했다.
[^huang2022-metastable-wild]: Huang, Magnusson, Bangalore Muralikrishna, Estyak, Isaacs,
    Aghayev, Zhu & Charapko 2022, "Metastable Failures in the Wild", OSDI '22, pp.73–89.
    §1 "Introduction"(p.73), §3.1 "System Model"(p.76), §3.3 "Sustaining Effect
    Loop"(pp.77–78), §3.5.1 "Stable State"(p.79), §3.5.2 "Vulnerable State"(p.79),
    §7 "Related Work"(p.86). 쪽수는 USENIX 논문집 인쇄 쪽 기준이며 PDF 스냅샷 2–19쪽이
    pp.73–89에 해당한다(1쪽은 표지). 정리 2의 증명은 부록 A.2(p.87)에 있다.
