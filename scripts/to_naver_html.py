#!/usr/bin/env python3
"""초안 마크다운을 스마트에디터 붙여넣기용 HTML로 변환.
사용법: python3 scripts/to_naver_html.py posts/drafts/파일.md
결과: 같은 위치에 파일.html 생성. 브라우저로 열어 전체 선택, 복사 후 스마트에디터에 붙여넣기."""
import html
import re
import sys


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    return t


def convert(md):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    title, body = "", md
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
        body = m.group(2)
    out, in_list = [], False
    for raw in body.splitlines():
        line = raw.rstrip()
        if re.match(r"^[-*]\s+", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:].strip())}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if not line:
            out.append("<p>&nbsp;</p>")
        elif line.startswith("## "):
            out.append(f"<h3 style='font-size:19px'>{inline(line[3:])}</h3>")
        elif line.startswith("# "):
            out.append(f"<h2>{inline(line[2:])}</h2>")
        elif re.match(r"^\[사진", line):
            out.append(f"<p style='color:#0a7;text-align:center'>{inline(line)}</p>")
        elif re.match(r"^\[(경험|확인 필요)", line):
            out.append(f"<p style='color:#d33'>{inline(line)}</p>")
        else:
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return title, "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    title, content = convert(open(src, encoding="utf-8").read())
    dst = re.sub(r"\.md$", "", src) + ".html"
    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{max-width:720px;margin:24px auto;padding:0 16px;font-family:sans-serif;line-height:1.8;font-size:16px}}</style></head>
<body><p style="color:#888">제목: {html.escape(title)} (제목은 스마트에디터 제목칸에 따로 입력)</p><hr>
{content}
</body></html>"""
    open(dst, "w", encoding="utf-8").write(page)
    print(f"생성: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
