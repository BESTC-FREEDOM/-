---
description: 키워드로 블로그 초안 작성
argument-hint: 메인키워드
---
메인 키워드: $ARGUMENTS

1. CLAUDE.md 글쓰기 규칙과 templates/post-template.md 를 따른다.
2. 제목 후보 3개를 만들고 가장 좋은 것을 title 에 넣는다.
3. 도입 3~4줄에 검색자가 원하는 답을 바로 준다.
4. 사실 정보는 정확하게 쓰고, 불확실한 수치는 [확인 필요] 로 표시한다.
5. 경험은 절대 지어내지 않는다. [경험: 적을 내용 안내] 로 비워 둔다.
6. [사진: 무엇을 찍을지] 를 8~15개 배치한다.
7. posts/drafts/오늘날짜-키워드.md 로 저장하고 python3 scripts/check_post.py 로 검사한다.
8. keywords.csv 상태를 초안으로 바꾸고, 사용자가 채워야 할 [경험] 목록을 보고한다.
