#!/usr/bin/env python3
"""네이버 블로그 초안 자동 검수. 사용법: python3 scripts/check_post.py 파일.md [파일2.md ...]"""
import re
import sys
from collections import Counter

BANNED = ["결론적으로", "다양한", "중요합니다", "살펴보겠습니다", "알아보겠습니다", "마무리하겠습니다", "~에 대해"]


def parse(text):
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def plain(body):
    t = re.sub(r"\[(사진|경험|확인 필요)[^\]]*\]", "", body)
    t = re.sub(r"^#+\s*", "", t, flags=re.M)
    t = re.sub(r"^[-*]\s+", "", t, flags=re.M)
    t = re.sub(r"[*_`>]", "", t)
    return t


def check(path):
    text = open(path, encoding="utf-8").read()
    meta, body = parse(text)
    title = meta.get("title", "")
    kw = meta.get("keyword", "")
    pt = plain(body)
    chars = len(re.sub(r"\s", "", pt))
    photos = len(re.findall(r"\[사진", body))
    heads = len(re.findall(r"^##\s", body, re.M))
    exp_left = len(re.findall(r"\[경험", body))
    verify_left = len(re.findall(r"\[확인 필요", body))
    kw_count = pt.count(kw) if kw else 0
    paras = [p.strip() for p in pt.split("\n\n") if p.strip()]
    intro = paras[0] if paras else ""

    res = []

    def add(ok, label, detail):
        res.append(("통과" if ok else ("주의" if ok is None else "수정"), label, detail))

    add(bool(title) and 25 <= len(title) <= 35, "제목 길이", f"{len(title)}자 (25~35)")
    add(bool(kw) and title.find(kw) in range(0, 10), "제목 앞쪽 키워드", f"'{kw}' 위치 {title.find(kw)}")
    add(1500 <= chars <= 2500 if chars <= 2500 else None, "본문 글자 수", f"공백 제외 {chars}자 (1,500~2,500)")
    add(3 <= heads <= 5, "소제목", f"{heads}개 (3~5)")
    add(8 <= photos <= 15, "사진", f"{photos}장 (8~15)")
    add(3 <= kw_count <= 5 if kw_count <= 5 else None, "메인 키워드 반복", f"{kw_count}회 (3~5)")
    add(bool(kw) and kw in intro, "도입부 키워드", "첫 문단에 키워드 포함" if kw in intro else "첫 문단에 키워드 없음")
    add(exp_left == 0, "남은 [경험] 자리", f"{exp_left}곳")
    add(verify_left == 0, "남은 [확인 필요]", f"{verify_left}곳")

    hits = [w for w in BANNED if w in pt]
    add(not hits, "상투 표현", ", ".join(hits) if hits else "없음")

    sents = [s.strip() for s in re.split(r"[.!?\n]", pt) if len(s.strip()) > 8]
    dup = [s for s, c in Counter(sents).items() if c > 1]
    add(not dup, "반복 문장", f"{len(dup)}개" + (f": {dup[0][:30]}" if dup else ""))

    endings = Counter(re.findall(r"(\S{2})[.!?]", pt))
    top = endings.most_common(1)
    if top and len(sents) >= 10 and top[0][1] / len(sents) > 0.35:
        add(None, "문장 끝 반복", f"'{top[0][0]}' {top[0][1]}회, 어미를 다양하게")

    if meta.get("sponsored", "false").lower() == "true":
        add("협찬" in body[:300] or "제공" in body[:300], "협찬 표기", "상단 300자 내 표기 확인")

    print(f"\n[{path}]")
    for st, label, detail in res:
        print(f"  {st:3}  {label}: {detail}")
    fails = sum(1 for r in res if r[0] == "수정")
    print(f"  => 수정 {fails}건, 주의 {sum(1 for r in res if r[0] == '주의')}건")
    return fails


def main():
    files = [f for f in sys.argv[1:] if f.endswith(".md")]
    if not files:
        print(__doc__)
        return 0
    total = sum(check(f) for f in files)
    strict = "--strict" in sys.argv
    return 1 if (strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
