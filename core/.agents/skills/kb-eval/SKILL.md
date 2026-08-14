---
name: kb-eval
description: syntopicon 지식 베이스의 검색 품질을 잰다. kb-query가 잘 찾는지 의심될 때, 승급 뒤 회귀가 걱정될 때, 임베딩이나 검색 설정을 바꾸기 전후 비교가 필요할 때 쓴다. 질문지(qrels)를 레그별로 돌려 R@5와 MRR을 내고 지난 실측과 추세를 비교한다. 측정만 하고 튜닝 판단은 사람이 한다.
compatibility: 어느 프로젝트에서든 호출 가능(본문 '저장소 위치 확정' 절이 core를 찾는다). uv와 qmd 필요.
---

# kb-eval

**측정은 품질을 보장하지 않고 회귀를 검출한다.** 수치가 떨어졌으면 원인 후보를
갈라 보고하는 것까지가 이 스킬이고, 튜닝(임계·레그 구성·질문지 개정)은 사람이
정한다.

## 저장소 위치 확정 (cwd 독립 — 최초 1회)

```sh
cd "$(dirname "$(dirname "$(dirname "$(realpath "${CLAUDE_SKILL_DIR:-$HOME/.claude/skills/kb-eval}")")")")"
```

## 실행

```
uv run --group index evals/retrieval/runner.py --legs fast    # 결정적 3레그, 분 단위
uv run --group index evals/retrieval/runner.py --legs all     # hybrid 포함, 질의당 ~10초
```

- `--legs fast`(bm25·vector·morph)는 결정적이라 **단발 실행이 유효**하다.
  promote 사슬이 승급마다 자동으로 돌리는 것과 같은 측정이다.
- `--legs all`은 hybrid(qmd query) 레그를 더한다 — LLM 질의 확장이 껴서 느리고
  **비결정적**이다. 단발 점수 차이로 판단하지 마라: 변경 전후 비교는 반복 실행으로
  분포를 만들고 유의성을 봐야 한다(LLMOps 3장 실측, 원장 2026-08-14). 같은 설정을
  두 번 돌려 차이가 크면 그 차이가 노이즈 바닥이다.
- 결과 파일은 `evals/runs/retrieval-<날짜>.json`(git 밖), 집계는 stats.sqlite
  `retrieval_eval` 이벤트로 남는다.

## 추세 읽기 (지난 실측과 비교)

```sh
uv run python -c "
import json, sqlite3
db = sqlite3.connect('stats.sqlite'); db.row_factory = sqlite3.Row
for r in db.execute(\"SELECT at, payload FROM events WHERE kind='retrieval_eval' ORDER BY id DESC LIMIT 5\"):
    p = json.loads(r['payload'])
    legs = {k.split('(')[0]: v['R@5'] for k, v in p['summary'].items()}
    print(r['at'][:16], p['n_queries'], '문항', legs, '경보:', list(p['breaches']) or '없음')"
```

읽는 법:
- **문항 수가 함께 변했으면 점수 등락은 회귀가 아닐 수 있다** — 질문지가 자라면
  (신규 소스 문항 추가) 분모가 바뀐다. 클래스별 표(러너 stdout)로 갈라 본다.
- 경보(바닥 밑 R@5)가 떴으면: ① 질문지 추가 직후라면 신규 문항의 정답 경로 오타
  먼저 ② 승급 직후라면 개명·병합으로 정답 경로가 이동했는지(`git log --diff-filter=R`)
  ③ 둘 다 아니면 진짜 회귀 — 재색인 신선도(`tools/reindex.py`)부터.
- bm25 레그의 낮은 전체 점수는 결함이 아니라 분업이다(영문 원어·부분토큰 전담 —
  alias 클래스만 본다).

## 질문지 공백 점검

qrels 조각이 없는 소스는 측정 사각지대다. 대조:

```sh
git log --format="%(trailers:key=Ingest-Source,valueonly)" | grep -v '^$' | sort -u
ls evals/retrieval/qrels/
```

공백 소스는 목록으로 보고만 한다 — 문항 추가는 ingest 리뷰 절차(승급 후 확인)의
일이고, 소급 작성은 사람이 시킬 때 한다.
