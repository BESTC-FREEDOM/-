---
description: 초안 검수와 개선
argument-hint: 파일경로
---
대상: $ARGUMENTS

1. python3 scripts/check_post.py $ARGUMENTS 를 실행한다.
2. templates/review-checklist.md 기준으로 사람 눈 검수를 한다: 도입부 답변, 경험 밀도, AI 티 나는 문장, 반복, 사실 오류.
3. 고칠 점을 우선순위 순으로 제시하고, 사용자가 원하면 바로 수정한다.
4. 통과하면 python3 scripts/to_naver_html.py $ARGUMENTS 로 붙여넣기용 HTML을 만든다.
