#!/bin/sh
# README 다이어그램 재생성 — .d2 소스가 정본, SVG는 커밋되는 파생물(GitHub <picture> 소비용).
# 수정 절차: .d2 편집 → ./build.sh → 커밋. 렌더링을 로컬에서 하므로 결과가 결정적이다.
cd "$(dirname "$0")" || exit 1
for f in *.d2; do
  b="${f%.d2}"
  d2 --theme=0 "$f" "$b-light.svg" || exit 1
  d2 --theme=200 "$f" "$b-dark.svg" || exit 1
done
