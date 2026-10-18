# 다리 Y존·세로선 검증: python3 verify_legs.py [1|2]
#   앞·뒤 모습(서기+걷기 10프레임)에서, 다리 구간(가랑이 2줄 아래 ~ 신발 바로 위, 치마는 밑단 바로 아래부터) 전체가
#   가운데 열 = 바지(다리) 그림자색 1px 선인지 (외곽선색 아님). 2번이면 신발 바로 위 3줄만 외곽선색.
import sys, json, os, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
M = json.load(open(os.path.join(HERE, '..', 'out', 'lpc_meta.json'))); FW, FH = M['fw'], M['fh']
OPT = int(sys.argv[1]) if len(sys.argv) > 1 else M.get('legline', 1)
OUT = (40, 24, 32); IMG = {}
def img(f):
    if f not in IMG: IMG[f] = np.array(Image.open(os.path.join(ROOT, 'public', f)).convert('RGBA'))
    return IMG[f]
hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def compose(av):
    body = M['bodies'][av['body']]; layers = []
    for cat in ('body', 'top', 'legs', 'feet'):
        p = M['parts'][cat][av.get(cat, 0)]
        for row, z, maps in p['L'].get(body, []): layers.append((z, p['f'], row, maps, cat))
    layers.sort(key=lambda t: t[0])
    out = np.zeros((FH, FW * M['frames'], 4), np.uint8); own = np.full((FH, FW * M['frames']), '', object); shoe = np.zeros((FH, FW * M['frames']), bool)
    for z, f, row, maps, cat in layers:
        a = img(f)[row * FH:(row + 1) * FH].copy(); m = a[..., 3] > 0
        for slot, src in maps:        # 색은 원래 팔레트 그대로 (밝기 비교만 하니까)
            pass
        out[m] = a[m]; own[m] = cat; shoe[m] = cat == 'feet' and z >= 15
    if OPT == 2:
        for k, (lc, cr) in M['leg'].items():
            x = int(k) * FW + lc; ys = [y for y in range(cr + 2, FH) if shoe[y, x]]
            if ys:
                for y in range(max(cr + 2, ys[0] - 3), ys[0]):
                    if out[y, x, 3]: out[y, x, :3] = OUT
    return out, own, shoe
def lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def check(av):
    out, own, shoe = compose(av); bad = []; rows_ok = 0
    for k, (lc, cr) in M['leg'].items():
        x = int(k) * FW + lc; ys = [y for y in range(cr + 2, FH) if shoe[y, x]]; top = ys[0] if ys else FH
        for y in range(cr + 2, top):
            if not out[y, x, 3]: continue
            o = own[y, x]
            # 치마·원피스 천이 덮은 줄은 다리 구간이 아니에요 (양옆도 같은 층이고 가운데에 선이 없음)
            if o in ('legs', 'top') and own[y, x - 1] == o and own[y, x + 1] == o and abs(lum(out[y, x]) - lum(out[y, x - 1])) < 8: continue
            c = tuple(int(v) for v in out[y, x, :3]); nb = [tuple(int(v) for v in out[y, x + d, :3]) for d in (-1, 1) if out[y, x + d, 3]]
            last3 = OPT == 2 and y >= top - 3 and top < FH
            if last3:
                ok = max(abs(c[j] - OUT[j]) for j in range(3)) <= 3
            else:
                ref = max(lum(n) for n in nb) if nb else 0
                ok = max(abs(c[j] - OUT[j]) for j in range(3)) > 3 and ref > 0 and .45 <= lum(c) / ref <= .9
            rows_ok += ok
            if not ok: bad.append((int(k), y, c))
    return rows_ok, bad
idx = lambda c, n: next(i for i, p in enumerate(M['parts'][c]) if p['n'] == n)
if __name__ == '__main__':
    tot = fail = 0
    feet = [idx('feet', n) for n in ('로퍼', '로퍼 + 무릎 양말', '운동화', '부츠')]
    for li, lp in enumerate(M['parts']['legs']):
        if 'female' not in lp['L']: continue
        for fi in feet:
            ok, bad = check(dict(body=0, top=idx('top', '티셔츠'), legs=li, feet=fi))
            tot += ok + len(bad); fail += len(bad)
            if bad: print('X', lp['n'], M['parts']['feet'][fi]['n'], bad[:3])
    print('legline', OPT, '검사한 줄', tot, '실패', fail)
