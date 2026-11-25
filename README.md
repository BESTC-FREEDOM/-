# 네이버 블로그 종합운영

Claude Code 클라우드 세션에서 네이버 블로그 기획, 키워드, 초안, 검수, 통계 점검을 한 저장소로 운영하는 작업 공간.

## 구조

| 경로 | 용도 |
|---|---|
| CLAUDE.md | Claude가 따르는 운영 원칙과 글쓰기 규칙 |
| blog/profile.md | 블로그 정체성, 주제, 카테고리, 독자 |
| keywords/keywords.csv | 키워드 풀과 진행 상태 |
| calendar/ | 월별 발행 캘린더 |
| posts/drafts/ | 작성 중인 초안 (마크다운) |
| posts/published/ | 발행 완료 글 보관 (URL, 발행일 기록) |
| templates/ | 글 템플릿, 검수 체크리스트 |
| scripts/ | 초안 자동 검수, 스마트에디터 붙여넣기용 HTML 변환 |
| stats/weekly-log.md | 주간 통계 기록과 개선 메모 |
| images/ | 글별 사진 메모 (원본 사진은 휴대폰에 두고 목록만 기록 권장) |

## 슬래시 명령

Claude Code에서 아래처럼 입력하면 된다.

- /keyword 주제 : 롱테일 키워드 후보 발굴, keywords.csv에 추가
- /plan 2026-12 : 한 달 발행 캘린더 작성
- /draft 키워드 : 템플릿에 맞춰 초안 작성 (경험 자리는 비워 둠)
- /review 파일경로 : 자동 검수 + 품질 피드백
- /weekly : 주간 통계 점검과 다음 주 계획

## 기본 흐름

1. blog/profile.md 를 먼저 채운다.
2. /keyword 로 키워드 풀을 만든다.
3. /plan 으로 한 달 캘린더를 잡는다.
4. /draft 로 초안을 만들고, [경험] 표시된 자리를 직접 채운다.
5. /review 로 점검 후 아래 명령으로 HTML을 만든다.

```bash
python3 scripts/to_naver_html.py posts/drafts/파일명.md
```

6. 생성된 HTML을 브라우저로 열어 전체 복사 후 스마트에디터에 붙여넣고, 사진을 [사진] 위치에 넣어 발행한다.
7. 발행 후 파일을 posts/published/ 로 옮기고 상단에 URL과 발행일을 적는다.

## 자동 검수

```bash
python3 scripts/check_post.py posts/drafts/파일명.md
```

글자 수, 사진 수, 소제목 수, 제목과 본문의 키워드 배치, 반복 문장, 금지 표현을 점검한다. GitHub에 올리면 drafts 변경 시 Actions에서도 같은 검사가 돈다.
