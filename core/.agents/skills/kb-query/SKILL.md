---
name: kb-query
description: syntopicon 지식 베이스를 조회해 답하고, 새로 알아낸 것만 골라 저장한다. KB에 쌓인 개념·소스·판단을 찾을 때, 답에 출처 라벨이 필요할 때, 웹에서 찾은 것을 KB에 남길지 판단할 때 쓴다. 검색 결과를 링크 이웃으로 확장하고 검색 공백을 계측한다.
compatibility: 어느 프로젝트에서든 호출 가능 — 아래 ⓪이 core 저장소를 찾는다. qmd(선택)와 uv가 있으면 검색 레그가 늘어난다.
---

# kb-query

**기억에서 답하지 말 것.** 모델이 이미 아는 주제여도 KB에는 사용자가 축적해 온
판단·정오표·조건이 붙어 있다. 그것이 이 KB의 존재 이유다.

아래는 체크리스트다. ⓪·①은 세션 최초 1회, ②–⑥은 매 질문, ⑦은 답한 뒤.

## ⓪ 저장소 위치 확정 (최초 1회 — cwd 독립)

이 스킬의 `uv run tools/…` 명령은 전부 core 저장소 루트 기준이다. cwd가 core가
아니면(다른 프로젝트에서 호출) 먼저:

```sh
cd "$(dirname "$(dirname "$(dirname "$(realpath "${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/kb-query}")")")")"
```

(스킬 심링크의 실경로 `core/.agents/skills/kb-query`에서 3단계 위 = core 루트.)

## ① 방향 잡기 (최초 1회)

루트 `overview.md`(KB 라우터) → 관련 `<kb>/overview.md`의 `## Hubs`.
**전체 카탈로그는 없다.** 파일 목록을 훑지 말고 라우터·허브·검색을 쓴다.

## ② 횡단 검색

읽기는 **KB 횡단이 기본**이다. `--kb`로 좁히는 것은 사용자가 요구할 때만.

```
qmd query "<질의>"                       # 하이브리드 (있으면 1순위)
uv run --group index tools/ksearch.py "<질의>"   # 한국어 형태소 레그
rg -n "<영문 부분문자열>"                  # 영문 substring 폴백
```

한국어 질의는 확장 없이 그대로 던진다 — 질의 확장은 영어 쪽으로 기운다.
형태소 레그가 조사 변형·활용형을, qmd 음절 레그가 부분 일치를 맡는다.

**벤더 기술 문서 질의는 KB가 아니라 docs-mirror가 담당한다** — "dbt의 이 설정",
"Spark 이 버전의 동작"처럼 답의 정본이 벤더 문서인 질문은 docs-query 스킬
(라우팅→rg→정독, `~/.claude/skills/docs-query`)로 라우팅한다. KB는 그 위에 쌓인
사용자의 판단·조건·경험만 답한다. docs-mirror에서 가져온 내용의 출처는
`[웹]`이 아니라 upstream 정식 인용(URL+버전)으로 단다.

## ③ 이웃 확장

히트한 **섹션 → 페이지 → 링크 이웃** 순으로 넓힌다. 한 페이지에서 답이 안 나오면
멈추지 말고 이웃을 본다 — 이 KB의 주제 조직은 태그가 아니라 링크다.

```
uv run tools/edges.py neighbors <경로> --depth 2
uv run tools/edges.py backlinks <경로>
```

탐색 기본 스코프는 **KB 내부**다. 크로스 KB 엣지는 있다고 표시만 하고, 사용자가
명시로 요구할 때만 따라간다.

## ④ 공백 평가

KB가 답하지 못하면 **그렇다고 말한다.** 없는 것을 있는 것처럼 내놓는 순간
출처 라벨 전체가 무의미해진다. 공백은 이벤트로 남긴다 — 계측되지 않는 공백은
영영 메워지지 않는다.

```
uv run python -c "
import sys; sys.path.insert(0,'tools')
from syntopicon import stats
with stats.connect() as db:
    db.execute('INSERT INTO search_miss VALUES (?,?,?)', (stats.now(), '<kb>', '<질의>'))
"
```

## ⑤ 웹은 공백에 한해

KB가 답한 부분은 웹으로 보강하지 않는다. 웹으로 간 부분은 ⑦의 판단 대상이 된다.

## ⑥ 출처 라벨

문장마다가 아니라 **출처가 바뀌는 지점마다** 라벨을 단다.

호출에 `--plain` 옵션이 있으면 답변 글을 kb-plain 규칙(기호 최소, 쉬운 낱말 —
정본은 `../kb-plain/SKILL.md`)으로 쓴다. 옵션이 없으면 평소대로 쓴다.

| 라벨 | 뜻 |
|---|---|
| `[<kb>]` | 그 KB의 검토된 페이지 |
| `[unreviewed]` | `<kb>/inbox/`의 미검토 초안 — 그대로 믿지 말 것 |
| `[웹]` | 이번에 웹에서 가져온 것 |
| 무표기 | 모델 지식 — KB 문장과 섞지 말 것 |

기계가 쓴 claim을 이번에 실제로 확인했다면 승급시킨다(review-on-read):

```
uv run tools/verify.py <페이지 경로>              # 사용자가 확인한 경우 (기본 human:me)
uv run tools/verify.py <페이지 경로> --by <모델id>  # 에이전트가 원문 대조로 확인한 경우
```

frontmatter를 손으로 고치지 않는다 — 스탬프 형식(따옴표 datetime·빈 리스트 금지)은
도구가 책임진다. **확인하지 않았다면 손대지 않는다** — 거짓 스탬프가 사다리 전체를
무의미하게 만든다.

## ⑦ 저장 판단 3문

**전부 예일 때만** 저장한다. 하나라도 아니오면 저장하지 않고, 왜 안 하는지 한 줄로 말한다.

1. 이 세션 맥락 **밖에서도** 재사용되는가?
2. 기존 페이지의 재조합이 아닌 **신규**인가? (교차 발견·공백 메움)
3. claim마다 **각주 가능한 출처**가 있는가? (웹 출처면 ①부터 다시 — ingest 경로다)

사용자가 "쓸 만하면 남겨줘"라고 해도 3문은 그대로 적용한다. 과잉 저장의 비용은
몇 달 뒤 중복 페이지와 inbox 파산으로 청구된다.

저장한다면 **`--kb` 명시로 `<kb>/inbox/` 경유**다. `concepts/`·`synthesis/`에
직접 쓰지 않는다. 기존 페이지 보강이 맞다면 새 페이지 대신 그것을 제안한다.

저장 후:

```
uv run tools/validate.py            # 통과할 때까지
uv run tools/reindex.py
```

## 오판은 구조가 흡수한다

과잉 저장은 inbox 격리·overlap lint·P90 경보가, 과소 저장은 search-miss가 잡는다.
완벽한 판단이 아니라 **판단을 명시적으로 하는 것**이 요점이다.
