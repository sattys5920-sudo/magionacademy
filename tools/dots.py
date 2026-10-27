#!/usr/bin/env python3
"""말줄임표 통일: 말 중간은 점 4개 ("...."), 말 끝은 점 7개 (".......").
   「…」 「……」 「...」 같은 옛 표기를 모두 바꿔요. 여러 번 돌려도 같은 결과예요.
   사용: python3 tools/dots.py [--check] 파일...   (--check: 바꿀 곳이 있으면 목록만 보여 주고 끝)"""
import re, sys
MID, END = '....', '.......'
CLOSE = '」』)]”’'
def is_end(rest):
    r = rest
    for _ in range(3):
        r = r.lstrip(' \t')
        r = re.sub('^[' + re.escape(CLOSE) + ']*[?!]*[' + re.escape(CLOSE) + ']*', '', r)
    r = r.lstrip(' \t')
    return r == '' or r[0] in '\n\r\'"`<' or r.startswith('\\n') or r.startswith('\\"') or r.startswith("\\'") or r.startswith('\\r')
PAT = re.compile(r'[….]*…[….]*|(?<!\.)\.{3,}(?!\.)')   # …와 점이 섞인 것도 한 덩어리
def fix(text):
    out, last = [], 0
    for m in PAT.finditer(text):
        s = m.group(0)
        if s in (MID, END) and '…' not in s: continue           # 이미 새 표기
        if s[0] == '.' and text[m.start() - 1:m.start()] in ('(', '[', '{', ',') : continue   # 코드의 펼침 연산(...x)
        if s == '...' and re.match(r'[\w$(\[{]', text[m.end():m.end() + 1] or ' '): continue    # ...args
        rep = END if is_end(text[m.end():]) else MID
        out.append(text[last:m.start()]); out.append(rep); last = m.end()
    out.append(text[last:]); return ''.join(out)
if __name__ == '__main__':
    chk = '--check' in sys.argv; n = 0
    for f in [a for a in sys.argv[1:] if a != '--check']:
        t = open(f, encoding='utf-8').read(); u = fix(t)
        if u != t:
            n += 1
            if chk: print('바꿀 곳 있음:', f)
            else: open(f, 'w', encoding='utf-8').write(u)
    sys.exit(1 if chk and n else 0)
