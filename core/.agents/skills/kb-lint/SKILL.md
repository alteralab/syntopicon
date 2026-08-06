---
name: kb-lint
description: syntopicon 지식 베이스의 전수 점검 리포트를 돌리고 읽는다. 주간 점검, 깨진 링크·만료 페이지·고아 페이지·모순 쌍·스냅샷 변조·inbox 적체를 확인할 때, lint 리포트를 어디부터 손댈지 판단할 때 쓴다. 검출만 하고 수정은 사람이 한다.
compatibility: syntopicon 저장소 안에서 uv와 함께 실행한다. tools/reindex.py를 먼저 돌려야 한다.
---

# kb-lint

**lint는 검출만 한다.** 수정 커밋은 사람이 한다 — 자동 수정은 이 KB에서 금지된
동작(모순 자동 해소·페이지 자동 병합)과 구분되지 않고, 조용히 판단을 대신한다.

커밋을 막는 것은 `validate`다. lint의 종료 코드는 항상 0이다.

## 실행

```
uv run tools/reindex.py                    # 파생 인덱스 먼저
uv run tools/lint.py                       # 전수
uv run tools/lint.py --incremental         # 직전 실행 이후 바뀐 페이지만 (주간)
uv run tools/lint.py --kb <kb> --quiet     # info 숨김
uv run tools/lint.py --overlap-full        # overlap 전쌍 — 부트스트랩·분기 전수용
```

주간은 `--incremental`(overlap도 바뀐 페이지 × 전체만 본다), 분기 전수 검사와
부트스트랩만 전수다.
결과는 사람이 읽는 리포트와 `stats.sqlite`(경보·큐)에 이원 기록된다.

## 등급이 곧 우선순위는 아니다

| 등급 | 뜻 | 다루는 법 |
|---|---|---|
| error | 무결성이 깨졌거나 임계를 넘었다 | 종류를 갈라서 본다(아래) |
| warn | 부패 진행 중 | 이번 세션 또는 다음 세션 |
| info | 큐 | 지금 할 일이 아니다 |

같은 error 안에서도 **일의 종류가 다르다**:

- `broken-link`, `snapshot-mismatch` → 지금 고치는 일. 파일 수정.
- `inbox-p90`, `contradiction-one-sided` → **정책·연구 과제**. 파일 수정으로 안 끝난다.

리포트를 그대로 되읽어 주는 것은 분류가 아니다. 무엇이 5분짜리이고 무엇이
결정을 요구하는지 갈라 준다.

## 검사별 판단 기준

**broken-link / redirect-hop** — 링크를 고친다. redirect 경유는 스텁의
`superseded_by` 대상으로 직접 건다. 개명은 반드시 `tools/rename.py` 경유.

**cross-kb-link** — KB 자립성 위반이고 저장소 분리 시 파손 예고다. 대개 KB 경계를
잘못 그은 신호이므로 링크만 지우지 말고 왜 생겼는지 본다.

**stale** — 재검토 큐. 내용을 확인했으면 `stale_after`를 옮기고, 낡았으면
`status: deprecated` + `superseded_by`(둘은 함께 간다).

**orphan** — 허브나 관련 페이지에서 링크를 건다. 페이지를 지우는 것이 답인 경우는 드물다.

**hub-candidate** — `<kb>/overview.md`의 `## Hubs` 갱신 후보. **자동으로 넣지 않는다** —
목록 자동화는 생존하지만 큐레이션 자동화는 실패한다. 사람이 고른다. 상한은 10–30개.

**hub-split-hint** — 링크 40개 초과 허브. 분할은 부모–자식 패턴(옛 허브가 자식들을
가리키는 부모로 남아 링크 불파손). 새 허브 이름은 **현재 내용 범위만큼만 좁게** —
넓은 이름은 description을 미래에 거짓으로 만든다(SCHEMA.md §5).

**claim-unfootnoted / source-uncited** — 각주는 출처 귀속 전용 채널이다. 선언한
소스가 인용되지 않았다면 죽은 항목이거나, 각주 정의가 빠져 본문에 `[^…]`가
평문으로 남아 있는 것이다(후자는 validate가 못 본다).

**contradiction / contradiction-one-sided** — 한쪽만 적힌 것은 오류이니 상호 기록으로
맞춘다. 양쪽 다 적힌 모순은 **연구 과제 큐**다: 자동 해소 금지, 최신성 단독 판단 금지.
해소한다면 해소 날짜·결정 근거·대체된 주장을 페이지에 남긴다. 두 주장이 실은
조건이 다른 것일 수도 있다 — 그건 병합이 아니라 조건 명시로 풀린다.

**snapshot-missing / snapshot-mismatch** — mismatch는 변조 증거다. `snapshot_sha256`은
write-once이므로 **기록을 새 값으로 덮지 않는다.** 무엇이 왜 바뀌었는지부터 본다.

**page-too-long / toc-missing / heading-\*** — 500줄은 백스톱이지 분할 기준이 아니다.
1차 완화책은 분할이 아니라 TOC + 섹션 앵커다. 분할은 "한 페이지 = 하나의 질문"이
깨졌을 때만.

**morph-fragmentation** — `schema/user-dict.yaml` 후보. 넣으면 재색인이 필요하다.
여러 페이지에서 반복되는 것만 넣는다.

**field-unused** — 소비자 없는 필드가 쌓이고 있다는 신호. 스키마에서 은퇴시키려면
`tools/affected.py`로 영향을 조회하고 `schema/migrations.md` 결번 대장에 적는다.

**ingest-trailer** — 소스를 들인 커밋에 트레일러가 없다. 과거 커밋은 고치지 않고,
다음 ingest부터 지킨다.

## 임계 경보 (tripwire)

경보는 **주기 작업의 우선순위 지시**이지 신규 구축 트리거가 아니다.

| 경보 | 대응 |
|---|---|
| inbox 나이 P90 > 30일 | **자동 머지 범위 확대**(저위험 diff의 N일 자동 머지). 리뷰 시간 증액이 아니다 — 예산 2–3주당 30–45분은 고정 전제다 |
| lint 오류 > 50건 | 유지보수 세션을 잡는다 |
| search-miss 20회 중 4회 초과 | 검색 설정 점검(형태소 사전·융합 가중치) |

1인 운영에서 리뷰 공급은 1이고 백로그가 정상 상태가 되는 것은 알려진 성질이다.
P90은 파산 시점의 계측이지 더 열심히 하라는 신호가 아니다.

**overlap / overlap-skipped** — qmd 벡터로 페이지 쌍 유사도(청크 최대 코사인)를
재서 compaction 후보를 낸다. 병합 판단은 사람. 능력의 경계를 알고 읽을 것(전부 실측):
근사 복제(1.00)와 **같은 용어의 재생성 중복(0.92 — 두 번째 소스가 같은 개념 페이지를
새로 만든 상황, 주 사용례)은 잡는다.** 어휘가 전혀 다른 재서술은 못 잡는다(0.54로
관련-상이 쌍 대역 0.65~0.77보다 오히려 낮음 — 임계로 분리 불가). 그 사각은 inbox
리뷰의 3문 ⑵와 저장 전 검색이 담당한다. 벡터가 없으면 경고로 크게 건너뛴다 —
`qmd update && qmd embed` 후 재실행.
