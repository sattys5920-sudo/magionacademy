# 시안: 뜨개 옷 4 종(목도리 · 방울 모자 · 털 귀마개 · 손모아장갑)을 입은 아바타의 앞 · 옆 · 뒤 (LPC 그대로)
#   목도리 = 게임 neck_004 를 게임 합성기로 씌운 그림에서 · 모자 · 귀마개 = 보는 방향마다 머리 모양에 맞춰 · 장갑 = LPC gloves 시트 방향별 줄
#   python3 knit_views.py <LPC 저장소> <아바타 png 폴더(av_me.png · av_me_side.png · av_me_back.png · av_me_neck*.png)> <저장 폴더>
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
LPC, AVD, OUTD = sys.argv[1:4]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
s = open(os.path.join(ROOT, 'public', 'world.js')).read(); i = s.index('const AVM = ') + 12; AVM, _ = json.JSONDecoder().raw_decode(s[i:])
hx = lambda h: tuple(int(h[k:k + 2], 16) for k in (1, 3, 5)); RAMP = {k: [hx(c) for c in v] for k, v in AVM['pal']['cloth'].items()}
YARN = {'하양': 'white', '빨강': 'red', '분홍': 'pink', '주황': 'orange', '노랑': 'p_mustard', '초록': 'green', '하늘': 'sky', '파랑': 'blue', '보라': 'purple', '갈색': 'brown'}
L = lambda c: .3 * c[0] + .59 * c[1] + .11 * c[2]
VIEWS = [('', '앞'), ('_side', '옆'), ('_back', '뒤')]
LPCROW = {'': 2, '_side': 1, '_back': 0}   # LPC walk: 위 · 왼쪽 · 아래 · 오른쪽 줄
def knit_recolor(im, pick):
    out = im.copy(); P = im.load(); Q = out.load(); px = [(x, y) for y in range(64) for x in range(64) if P[x, y][3] > 0]
    if not px: return out
    ls = [L(P[x, y][:3]) for x, y in px]; lo, hi = min(ls), max(ls)
    for x, y in px:
        r = RAMP[YARN[pick(x, y)]]; n = len(r); v = (L(P[x, y][:3]) - lo) / max(1, hi - lo); k = 0 if v < .08 else min(n - 1, 1 + int(v * (n - 1)))
        if k >= 2 and ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1 and (x + y) % 4 == 2)): k -= 1
        Q[x, y] = r[k] + (P[x, y][3],)
    return out
def lpc_fill(lay, pts, ramp, light=(-1, -1)):
    if not pts: return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2; w, h = max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)); P = lay.load()
    for x, y in pts:
        v = ((x - cx) / w * light[0] + (y - cy) / h * light[1]); k = 4 if v > .35 else 3 if v > -.1 else 2
        if ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1 and (x + y) % 4 == 2)) and k > 2: k -= 1
        P[x, y] = ramp[min(len(ramp) - 1, k)] + (255,)
    S_ = set(pts)
    for x, y in pts:
        for a_, b_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + a_, y + b_)
            if q not in S_ and 0 <= q[0] < 64 and 0 <= q[1] < 64 and not P[q][3]: P[q] = ramp[0] + (255,)
def over(base, *ls):
    o = base.copy()
    for l in ls: o.alpha_composite(l)
    return o
class View:
    def __init__(s, v):
        s.v = v; s.base = Image.open(os.path.join(AVD, f'av_me{v}.png')).convert('RGBA'); s.B = s.base.load()
        s.rows = {}
        for y in range(64):
            xs = [x for x in range(18, 47) if s.B[x, y][3]]
            if xs: s.rows[y] = (min(xs), max(xs))
        s.top = min(s.rows)
        s.tops = {}
        for x in range(18, 47):
            ys = [y for y in range(64) if s.B[x, y][3]]
            if ys: s.tops[x] = min(ys)
        # 목도리: 게임 합성기로 씌운 그림 - 안 씌운 그림
        w = Image.open(os.path.join(AVD, f'av_me_neck{v}.png')).convert('RGBA'); P = w.load(); s.neckW = w; s.neckL = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); Q = s.neckL.load()
        for y in range(64):
            for x in range(64):
                if P[x, y][3] and P[x, y] != s.B[x, y]: Q[x, y] = P[x, y]
        g = Image.open(os.path.join(LPC, 'spritesheets', 'arms', 'hands', 'gloves', 'thin', 'walk.png')).convert('RGBA'); r = LPCROW[v]; s.glove = g.crop((0, r * 64, 64, r * 64 + 64))
    def scarf(s, a, b): return over(s.neckW, knit_recolor(s.neckL, lambda x, y: a if (x // 2 + y // 3) % 2 == 0 else b))
    def hat(s, a, b):
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); BRIM = s.top + 11; dome, brim = [], []
        for y in range(s.top - 1, BRIM + 1):
            x0, x1 = s.rows.get(max(s.top, y), (30, 34)); x0 -= 1; x1 += 1
            if y == s.top - 1: x0, x1 = x0 + 4, x1 - 4
            for x in range(x0, x1 + 1): (brim if y >= BRIM - 2 else dome).append((x, y))
        lpc_fill(lay, dome, RAMP[YARN[a]]); P = lay.load(); rb = RAMP[YARN[b]]
        for x, y in brim: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
        xs = [p[0] for p in brim]
        for x in range(min(xs), max(xs) + 1): P[x, BRIM + 1] = rb[0] + (255,)
        for y in range(BRIM - 2, BRIM + 1): P[min(xs) - 1, y] = rb[0] + (255,); P[max(xs) + 1, y] = rb[0] + (255,)
        cx = (s.rows[s.top][0] + s.rows[s.top][1]) / 2 + (1 if s.v == '_side' else 0)
        pom = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 3.4) ** 2 + ((y - (s.top - 3)) / 3) ** 2 <= 1 and not P[x, y][3]]; lpc_fill(lay, pom, rb)
        return over(s.base, lay)
    def muff(s, a, b):
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); rb = RAMP[YARN[b]]; ra = RAMP[YARN[a]]; EY = s.top + 15; x0, x1 = s.rows[EY]
        if s.v == '_side':   # 옆: 귀 하나 · 띠는 머리 위로 세로로 지나가요
            ex = int(x1 - (x1 - x0) * .42); band = []
            for y in range(s.tops.get(ex, s.top) + 1, EY - 2): band += [(ex, y), (ex + 1, y)]
            for x, y in band: P[x, y] = (rb[3] if y % 2 else rb[2]) + (255,)
            puff = [(x, y) for y in range(64) for x in range(64) if ((x - ex - .5) / 2.8) ** 2 + ((y - EY) / 3.3) ** 2 <= 1]
            for q in puff: P[q] = (0, 0, 0, 0)
            lpc_fill(lay, puff, ra, light=(-1, -1)); return over(s.base, lay)
        band = []
        for x in range(x0 + 1, x1):
            y0 = s.tops.get(x, s.top) + 3; band += [(x, y0), (x, y0 + 1)]
        for x in (x0 + 1, x1 - 1):
            for y in range(s.tops.get(x, s.top) + 3, EY - 2): band += [(x, y), (x + (1 if x < 32 else -1), y)]
        for x, y in band: P[x, y] = (rb[3] if (x + y) % 2 else rb[2]) + (255,)
        for cx in (x0, x1):
            puff = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 2.6) ** 2 + ((y - EY) / 3.2) ** 2 <= 1]
            for q in puff: P[q] = (0, 0, 0, 0)
            lpc_fill(lay, puff, ra, light=(-1 if cx < 32 else 1, -1))
        return over(s.base, lay)
    def gloves(s, a, b):
        g = knit_recolor(s.glove, lambda x, y: a); P = g.load(); rb = RAMP[YARN[b]]
        for x in range(64):
            ys = [y for y in range(64) if P[x, y][3]]
            for y in ys[:3]:
                if L(P[x, y][:3]) > 30: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
        return over(s.base, g)
V = {v: View(v) for v, _ in VIEWS}
ITEMS = [('목도리', 'scarf', ('빨강', '하양')), ('방울 모자', 'hat', ('파랑', '노랑')), ('털 귀마개', 'muff', ('분홍', '하양')), ('손모아장갑', 'gloves', ('초록', '하양'))]
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
F, F2, F3 = ImageFont.truetype(FB, 16), ImageFont.truetype(FB, 13), ImageFont.truetype(FB, 22)
BG, PAN, INK, SUB, GOLD = (26, 18, 38), (37, 26, 54), (241, 233, 255), (184, 168, 216), (255, 233, 160)
img = Image.new('RGB', (1000, 1150), BG); d = ImageDraw.Draw(img)
d.text((24, 16), '뜨개 옷 4 종 · 앞 · 옆 · 뒤 (LPC)', font=F3, fill=(255, 184, 168))
for r, (nm, fn, (a, b)) in enumerate(ITEMS):
    y = 56 + r * 270; d.rounded_rectangle([16, y, 984, y + 258], 14, fill=PAN, outline=(58, 46, 88), width=2)
    d.text((32, y + 14), nm, font=F, fill=GOLD); d.text((32, y + 36), f'{a} · {b}', font=F2, fill=SUB)
    for c, (v, vn) in enumerate(VIEWS):
        im = getattr(V[v], fn)(a, b).crop((12, 2, 52, 64)).resize((140, 217), Image.NEAREST); x = 200 + c * 260; img.paste(im, (x, y + 22), im); d.text((x + 62, y + 236), vn, font=F2, fill=SUB)
os.makedirs(OUTD, exist_ok=True); img.save(os.path.join(OUTD, 'knit_views_preview.png')); print('ok')
