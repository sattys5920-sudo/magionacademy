# 데이터의 「변수 + 고정 조사」를 {var|받침O/받침X} 표기로 바꿔요 (한 번만 돌리면 돼요)
import json, glob, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from josa import RUN
PAT = re.compile(r'\{([a-z_]+(?:\.[a-z_]+)?)\}([가-힣]*)(.?)')
def fix(t):
    def r(m):
        k, run, nx = m.group(1), m.group(2), m.group(3)
        if run == '야' or run == '아': return '{%s|%s}%s' % (k, '아/야' if nx in (',', '!', '…', '~') or run == '아' else '이야/야', nx)
        if run in RUN: a, b, rest = RUN[run]; return '{%s|%s/%s}%s%s' % (k, a, b, rest, nx)
        return m.group(0)
    return PAT.sub(r, t)
n = 0
def walk(o):
    global n
    if isinstance(o, str):
        f = fix(o); n += f != o; return f
    if isinstance(o, list): return [walk(v) for v in o]
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    return o
for f in glob.glob('public/data/npc/**/*.json', recursive=True):
    d = json.load(open(f)); d2 = walk(d)
    if d2 != d: json.dump(d2, open(f, 'w'), ensure_ascii=False, indent=1)
print('바뀐 문장', n)
