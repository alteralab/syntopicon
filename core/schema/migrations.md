# 스키마 변경 로그

append-only. `schema/*.yaml`이 **현재** 스키마이고, 이 파일이 **해석**을 제공한다.
파일마다 `schema_version`을 적지 않는 이유가 여기 있다 — 콘텐츠 파일은 재작성되지
않으므로 그 필드는 시간이 지나면 거짓말을 한다. 대신 git 커밋 날짜 + 이 로그가
"이 파일이 쓰이던 시점의 스키마"를 복원한다(PLAN §2.7).

## 호환 정책 — BACKWARD_TRANSITIVE

1. **additive만.** 새 optional 필드는 안전하다. 의미론 변경은 O(N)이므로 금지.
2. **in-place 개명 금지.** 새 키를 추가하고, 아래 로그에 구→신 매핑을 남기고,
   필요하면 backfill한다. 기존 키를 조용히 바꾸지 않는다.
3. **은퇴 키 이름은 영구 결번.** 재사용하면 과거 파일의 같은 이름이 다른 의미가 된다.
4. **변경 전 `tools/affected` 실행**(PLAN §6 운영 캘린더 "수시"). 영향 범위는 기억이
   아니라 조회가 답한다.

집행: `tools/validate`가 아래 결번 대장을 읽어 현재 스키마와 신규 파일에 결번 키가
등장하지 않는지 대조한다. 산문 규칙이 지켜진다고 가정하지 않는다.

## 결번 대장

`tools/validate`가 파싱하는 표다(markdown-it-py AST — 열 순서 고정). 비어 있어도 표는 남긴다.

| 결번 키 | 은퇴일 | 대체 | 사유 |
|---|---|---|---|

## 로그

### 2026-08-05 — 초기 스키마

첫 파일 작성 전 동결 코어(PLAN §2.7)를 기계화했다. 구→신 매핑 없음(선행 상태 없음).

- `layout.yaml` — 저장소 경계 정본: 공유 자산 화이트리스트 / KB 골격·디렉터리↔type
  정합 / 색인 포함·제외 패턴.
- `common.yaml` — 공유 `$defs`. 크로스 파일 `$ref`는 상대 `$id`로 해결(jsonschema
  4.26.0 + referencing 0.37.0 실측).
- `concept.yaml` · `synthesis.yaml` · `redirect.yaml` · `guide.yaml` · `source.yaml` —
  계층(=PLAN §2.3 "파일 종류")당 스키마 1개.
- `vocabulary.yaml` — 본문 epistemic 폐쇄 어휘. JSON Schema 아님, 소비자는 lint.
- `user-dict.yaml` — Kiwi 사용자 사전. 항목은 비어 있다(파편화 검출이 채운다).

기록해 둘 판단 3가지:

1. **소스 계층을 CSL 타입 10개 파일로 쪼개지 않았다.** CSL 공식 `csl-data.json`이
   45개 타입을 단일 스키마 + `type` enum으로 다루고 타입별 required 차등을 선언하지
   않는다(전역 `required: [type, id]`). PLAN §2.2가 enum을 차용한 출처의 관행을 따랐다.
2. **`issued`를 스칼라 문자열로 고정했다.** CSL 원형은 `{date-parts: [[2017]]}` 객체다.
   PLAN §2.1의 "날짜 값은 따옴표 문자열" 규약과 한 표현으로 맞췄고, CSL 스펙 설명문
   자체가 EDTF 문자열을 preferred로 명시한다. Zotero/pandoc 상호운용 시 변환이 필요하다
   — 다만 `snapshot`·`snapshot_sha256` 확장 필드가 이미 CSL 밖이라 변환은 어차피 발생한다.
3. **`number`를 문자열 전용으로 좁혔다.** CSL은 `string|number`지만 따옴표 없는 arXiv ID
   `2405.14831`이 YAML에서 float로 파싱돼 식별자가 조용히 손상된다. 스키마가 그 실수를
   fail-loud로 잡게 했다.
