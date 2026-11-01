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
    def __init__(s, v, who='me', body='thin'):
        s.v = v; s.who = who; s.base = Image.open(os.path.join(AVD, f'av_{who}{v}.png')).convert('RGBA'); s.B = s.base.load()
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
        np_ = os.path.join(AVD, f'av_{who}_neck{v}.png'); s.neckW = s.neckL = None
        if os.path.exists(np_):
            w = Image.open(np_).convert('RGBA'); P = w.load(); s.neckW = w; s.neckL = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); Q = s.neckL.load()
            for y in range(64):
                for x in range(64):
                    if P[x, y][3] and P[x, y] != s.B[x, y]: Q[x, y] = P[x, y]
        s.glove = None
        if body:
            g = Image.open(os.path.join(LPC, 'spritesheets', 'arms', 'hands', 'gloves', body, 'walk.png')).convert('RGBA'); r = LPCROW[v]; s.glove = g.crop((0, r * 64, 64, r * 64 + 64))
        bb = s.base.getbbox(); s.bb = bb; s.brim = 11 if body else 7; s.eyo = 15 if body else 10   # 그림 NPC(귀 달린 동물)는 모자를 덜 깊게
    def scarf(s, a, b, neck=None):
        if s.neckW is not None: return over(s.neckW, knit_recolor(s.neckL, lambda x, y: a if (x // 2 + y // 3) % 2 == 0 else b))
        # 그림 NPC: 머리와 몸 사이 줄에 목도리 띠 + 앞에서는 한쪽으로 늘어진 끝
        x0, y0, x1, y1 = s.bb; ny = neck if neck else y0 + int((y1 - y0) * .46); lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); ra, rb = RAMP[YARN[a]], RAMP[YARN[b]]
        band = []
        for y in range(ny - 1, ny + 2):
            mid = (x0 + x1) // 2; xs = [x for x in range(mid - 8, mid + 9) if s.B[x, y][3]]   # 날개 · 꼬리는 빼고 몸통 가운데만
            if xs: band += [(x, y) for x in range(min(xs), max(xs) + 1)]
        tail = []
        if s.v == '':
            xs = [x for x, y in band]; tx = max(xs) - 4 if xs else 34; tail = [(x, y) for y in range(ny + 2, ny + 8) for x in range(tx, tx + 3)]
        if s.v == '_back':
            xs = [x for x, y in band]; tx = (min(xs) + max(xs)) // 2 - 1 if xs else 31; tail = [(x, y) for y in range(ny + 2, ny + 7) for x in range(tx, tx + 3)]
        pts = band + tail; lpc_fill(lay, pts, ra)
        for x, y in pts:
            if (x // 2 + y // 3) % 2: P[x, y] = rb[2 + ((x + y) % 2)] + (255,)
        return over(s.base, lay)
    def hat(s, a, b):
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); BRIM = s.top + s.brim; dome, brim = [], []
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
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); rb = RAMP[YARN[b]]; ra = RAMP[YARN[a]]; EY = s.top + s.eyo; x0, x1 = s.rows[EY]
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
        if s.glove is None: return None
        g = knit_recolor(s.glove, lambda x, y: a); P = g.load(); rb = RAMP[YARN[b]]
        for x in range(64):
            ys = [y for y in range(64) if P[x, y][3]]
            for y in ys[:3]:
                if L(P[x, y][:3]) > 30: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
        return over(s.base, g)
# 그림 NPC(동물 등): 앞 · 옆 · 뒤마다 직접 잡은 자리 — 모자(dome x0, x1, 꼭대기 y, 챙 y) · 귀마개(솜방울 자리들) · 목(y, x0, x1) · 손(자리들)
SP_ = {
 'npc0': {'': dict(hat=(21, 36, 23, 30), muff=[(20, 25), (37, 25)], neck=(40, 23, 34), hands=[(25, 55), (31, 55)]),            # 나비: 귀는 모자 밖으로 · 귀마개는 귀에
          '_side': dict(hat=(19, 33, 23, 30), muff=[(30, 25)], neck=(42, 22, 30), hands=[(24, 55)]),
          '_back': dict(hat=(25, 42, 21, 29), muff=[(23, 23), (43, 23)], neck=(36, 28, 40), hands=[])},
 'npc1': {'': dict(hat=(27, 38, 22, 28), muff=[(25, 21), (39, 21)], neck=(38, 26, 39), hands=[(17, 32), (48, 32)]),            # 배트리: 손 = 날개 끝 발톱
          '_side': dict(hat=(24, 35, 22, 28), muff=[(33, 21)], neck=(37, 24, 34), hands=[]),
          '_back': dict(hat=(27, 40, 20, 27), muff=[(25, 18), (42, 18)], neck=(37, 27, 41), hands=[])},
 'npc2': {'': dict(hat=(25, 43, 18, 27), muff=[(24, 33), (44, 33)], neck=(39, 27, 41), hands=[(25, 45), (43, 45)]),            # 캇파: 접시 위로 · 손은 양옆
          '_side': dict(hat=(26, 44, 18, 27), muff=[(38, 32)], neck=(39, 28, 42), hands=[(28, 45)]),
          '_back': dict(hat=(26, 44, 18, 26), muff=[(25, 32), (45, 32)], neck=(38, 28, 42), hands=[(26, 46), (44, 46)])},
 'npc3': {'': dict(hat=(24, 39, 24, 30), muff=[(21, 27), (42, 27)], neck=(41, 24, 39), hands=[(24, 46), (38, 46)]),            # 아울라: 손 = 책 든 날개 끝
          '_side': dict(hat=(23, 40, 24, 30), muff=[(36, 28)], neck=(41, 25, 37), hands=[(24, 46)]),
          '_back': dict(hat=(22, 41, 23, 29), muff=[(20, 27), (43, 27)], neck=(40, 22, 41), hands=[])},
 'npc4': {'': dict(hat=(27, 43, 36, 43), muff=[(27, 41), (43, 41)], neck=(52, 27, 43), hands=[(26, 52), (44, 52)], leaves=True),   # 맨디: 잎은 모자 위로 쏙
          '_side': dict(hat=(25, 41, 36, 43), muff=[(37, 41)], neck=(52, 25, 41), hands=[(24, 52)], leaves=True),
          '_back': dict(hat=(27, 44, 36, 43), muff=[(27, 41), (44, 41)], neck=(51, 27, 43), hands=[(26, 52), (44, 52)], leaves=True)},
 'npc5': {'': dict(hat=(24, 40, 22, 31), muff=[(24, 33), (40, 33)], neck=(40, 26, 38), hands=[(18, 49), (45, 49)], strip=31, mufftop=14),   # 스트로: 밀짚모자 벗고 털모자
          '_side': dict(hat=(25, 39, 22, 31), muff=[(35, 33)], neck=(40, 27, 37), hands=[(26, 49)], strip=31, mufftop=15),
          '_back': dict(hat=(24, 40, 22, 31), muff=[(24, 33), (40, 33)], neck=(40, 26, 38), hands=[(19, 48), (45, 48)], strip=31, mufftop=14)},
}
class SpriteView:
    def __init__(s, v, who):
        s.v = v; s.who = who; s.p = SP_[who][v]; s.base = Image.open(os.path.join(AVD, f'av_{who}{v}.png')).convert('RGBA'); s.orig = s.base.copy(); s.bare = None
        if 'strip' in s.p:
            s.base = s.base.copy()   # 스트로: 밀짚모자(챙 아래 줄까지)를 지우고, 그 자리에 자루 천 머리를 그려 둬요 (털모자가 덮어요)
            P = s.base.load(); x0, x1, top, brim = s.p['hat']
            for y in range(0, brim + 1):   # 챙 줄까지: 얼굴 폭 밖(챙 끝)은 지우고, 위쪽은 다 지워요 (털모자가 덮어요 · 얼굴은 그대로)
                for x in range(64):
                    if y < brim - 2 or x < x0 - 1 or x > x1 + 1: P[x, y] = (0, 0, 0, 0)
            # 모자 없이(귀마개만) 쓸 때 보일 자루 천 머리 윗부분
            bare = s.base.copy(); d = ImageDraw.Draw(bare); cxh = (x0 + x1) / 2
            d.ellipse([x0 - 1, top + 2, x1 + 1, brim + 10], fill=(58, 36, 28, 255)); d.ellipse([x0, top + 3, x1, brim + 9], fill=(196, 156, 100, 255)); d.ellipse([x0 + 2, top + 4, cxh, brim], fill=(218, 182, 124, 255))
            for xx in range(x0 + 2, x1 - 1, 3): d.point((xx, brim - 1), fill=(150, 110, 70, 255))
            bare.alpha_composite(s.base); s.bare = bare
            s.stripped = s.base; s.base = s.orig
        s.B = s.base.load()
    def _hat_pts(s):
        x0, x1, top, brim = s.p['hat']; cx = (x0 + x1) / 2; rx = (x1 - x0) / 2 + .5; dome, band = [], []
        for y in range(top, brim + 1):
            if y >= brim - 2: band += [(x, y) for x in range(x0 - 1, x1 + 2)]
            else:
                t = (brim - 2 - y) / max(1, brim - 2 - top); w = rx * (1 - t * t) ** .5 if t < 1 else 2
                dome += [(x, y) for x in range(int(cx - w), int(cx + w) + 1)]
        return dome, band, cx, top
    def hat(s, a, b):
        base0 = s.base
        if s.bare is not None and s.base is s.orig: s.base = s.stripped
        try: return s._hat(a, b)
        finally: s.base = base0
    def _hat(s, a, b):
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); dome, band, cx, top = s._hat_pts(); lpc_fill(lay, dome, RAMP[YARN[a]]); P = lay.load(); rb = RAMP[YARN[b]]
        for x, y in band: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
        xs = [p[0] for p in band]; by = max(p[1] for p in band)
        for x in range(min(xs), max(xs) + 1): P[x, by + 1] = rb[0] + (255,)
        if s.p.get('leaves'):   # 잎이 모자를 뚫고 나와요: 원래 잎 픽셀을 모자 위에 다시
            out = over(s.base, lay); O = out.load()
            for y in range(0, top + 3):
                for x in range(64):
                    c = s.B[x, y]
                    if c[3] and c[1] > c[0] + 20: O[x, y] = c
            return out
        pom = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 3) ** 2 + ((y - (top - 2)) / 2.6) ** 2 <= 1 and not P[x, y][3]]; lpc_fill(lay, pom, rb)
        return over(s.base, lay)
    def muff(s, a, b):
        base0 = s.base
        try: return s._muff(a, b)
        finally: s.base = base0
    def _muff(s, a, b):
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); ra, rb = RAMP[YARN[a]], RAMP[YARN[b]]; pts = s.p['muff']
        if len(pts) == 2:   # 두 솜방울을 머리 위로 잇는 띠
            (ax_, ay_), (bx_, by_) = pts; _, _, top, _ = s.p['hat']; topy = s.p.get('mufftop', top - 1)
            for i in range(41):
                t = i / 40; x = round(ax_ + (bx_ - ax_) * t); y = round((1 - t) ** 2 * ay_ + 2 * (1 - t) * t * (topy - 2) + t * t * by_)
                for dy in (0, 1): P[x, y + dy] = (rb[3] if (x + y) % 2 else rb[2]) + (255,)
        else:
            (ax_, ay_), = pts; _, _, top, _ = s.p['hat']
            for y in range(s.p.get('mufftop', top - 1), ay_ - 2):
                for dx in (0, 1): P[ax_ + dx, y] = (rb[3] if y % 2 else rb[2]) + (255,)
        for (cx, cy) in pts:
            puff = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 2.6) ** 2 + ((y - cy) / 3) ** 2 <= 1]
            for q in puff: P[q] = (0, 0, 0, 0)
            lpc_fill(lay, puff, ra, light=(-1 if cx < 32 else 1, -1))
        return over(s.base, lay)
    def scarf(s, a, b, neck=None):
        """몸 윤곽에 맞춰 감은 목도리: 띠는 몸이 있는 칸 + 양 끝 1 칸 두께 · 가운데가 1 칸 처져요 · 끝자락은 앞(앞모습 한쪽 · 옆모습 가슴 쪽)에만"""
        y0, x0, x1 = s.p['neck']; lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); ra, rb = RAMP[YARN[a]], RAMP[YARN[b]]; B = s.B
        band = []; mid = (x0 + x1) / 2; half = max(1, (x1 - x0) / 2)
        for x in range(x0 - 1, x1 + 2):
            sag = 1 if abs(x - mid) < half * .45 and s.v != '_side' else 0
            for y in range(y0 - 1 + sag, y0 + 2 + sag):
                inside = B[x, y][3] > 0 or B[max(0, x - 1), y][3] > 0 or B[min(63, x + 1), y][3] > 0
                if inside: band.append((x, y))
        tail = []
        if s.v == '': tail = [(x, y) for y in range(y0 + 2, y0 + 8) for x in range(x1 - 4, x1 - 1)]
        if s.v == '_side': tail = [(x, y) for y in range(y0 + 2, y0 + 7) for x in range(x0 + 1, x0 + 4)]   # 왼쪽을 보고 있어서 가슴 쪽 = 왼쪽
        pts = band + tail; lpc_fill(lay, pts, ra)
        for x, y in pts:
            if (x // 2 + y // 3) % 2 and P[x, y][:3] != ra[0]: P[x, y] = rb[2 + ((x + y) % 2)] + (255,)
        if tail:   # 술
            tx0 = min(x for x, _ in tail); ty = max(y for _, y in tail) + 1
            for x in range(tx0, tx0 + 3, 2): P[x, ty] = rb[2] + (255,); P[x, ty + 1] = rb[3] + (255,)
        return over(s.base, lay)
    def gloves(s, a, b):
        if not s.p['hands']: return over(s.base)
        lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); ra, rb = RAMP[YARN[a]], RAMP[YARN[b]]
        for cx, cy in s.p['hands']:
            m = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 2.3) ** 2 + ((y - cy) / 2.3) ** 2 <= 1]; lpc_fill(lay, m, ra)
            for x in range(cx - 2, cx + 3): P[x, cy - 3] = rb[2 + (x % 2)] + (255,)   # 손목 고무단
        return over(s.base, lay)
CAST = [('레오', 'leo', 'thin'), ('세라 선생님', 'sera', 'male'), ('마들렌', 'madeleine', 'male'), ('스텔라', 'stella', 'thin'), ('나비', 'npc0', None), ('배트리', 'npc1', None), ('캇파', 'npc2', None), ('아울라', 'npc3', None), ('맨디', 'npc4', None), ('스트로', 'npc5', None)]
NECK = {'npc0': 41, 'npc1': 41, 'npc2': 39, 'npc3': 42, 'npc4': 44, 'npc5': 37}   # 그림 NPC 목 높이 (앞)
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
F, F2, F3 = ImageFont.truetype(FB, 15), ImageFont.truetype(FB, 12), ImageFont.truetype(FB, 22)
BG, PAN, INK, SUB, GOLD = (26, 18, 38), (37, 26, 54), (241, 233, 255), (184, 168, 216), (255, 233, 160)
COLS = [('목도리', 'scarf', ('빨강', '하양')), ('방울 모자', 'hat', ('파랑', '노랑')), ('털 귀마개', 'muff', ('분홍', '하양')), ('손모아장갑', 'gloves', ('초록', '하양'))]
CW, RH = 120, 150; W_ = 150 + CW * 7 + 20; img = Image.new('RGB', (W_, 70 + RH * len(CAST) + 20), BG); d = ImageDraw.Draw(img)
d.text((20, 14), 'NPC가 선물받은 뜨개 옷 (내 화면에서만 · 모자 칸은 방울 모자나 귀마개 하나 · 여러 개면 매일 바꿔 써요)', font=F2, fill=(255, 184, 168))
for c, (nm, _, _) in enumerate(COLS): d.text((150 + c * CW + 20, 48), nm, font=F2, fill=GOLD)
for c, nm in enumerate(['다 같이 · 앞', '옆', '뒤']): d.text((150 + (4 + c) * CW + 24, 48), nm, font=F2, fill=GOLD)
def cell(im, c, r):
    if im is None: d.text((150 + c * CW + 30, 70 + r * RH + 60), '손 없음', font=F2, fill=(110, 96, 140)); return
    bb = im.getbbox(); crop = im.crop((max(0, bb[0] - 2), max(0, bb[1] - 2), min(64, bb[2] + 2), min(64, bb[3] + 2))); k = min((CW - 10) / crop.size[0], (RH - 14) / crop.size[1], 3)
    t = crop.resize((int(crop.size[0] * k), int(crop.size[1] * k)), Image.NEAREST); img.paste(t, (150 + c * CW + (CW - t.size[0]) // 2, 70 + r * RH + (RH - t.size[1]) - 6), t)
for r, (nm, who, body) in enumerate(CAST):
    y = 70 + r * RH; d.rounded_rectangle([12, y + 2, W_ - 12, y + RH - 4], 12, fill=PAN); d.text((22, y + RH // 2 - 10), nm, font=F, fill=INK)
    VV = {v: (View(v, who, body) if body else SpriteView(v, who)) for v, _ in VIEWS}
    for c, (_, fn, (a, b)) in enumerate(COLS):
        im = getattr(VV[''], fn)(a, b); cell(im, c, r)
    for c, (v, _) in enumerate(VIEWS):   # 다 같이: 목도리 + 모자 칸 하나(방울 모자) + 장갑
        V_ = VV[v]; keep = V_.base
        if isinstance(V_, View):
            V_.base = V_.scarf('빨강', '하양'); V_.B = V_.base.load(); V_.neckW = V_.base; V_.neckL = Image.new('RGBA', (64, 64))
            V_.base = V_.hat('파랑', '노랑'); V_.B = V_.base.load()
        else:   # 그림 NPC: 모자 먼저(스트로는 밀짚모자 벗고) → 목도리
            hb = V_.hat('파랑', '노랑'); V_.orig_keep = V_.orig; V_.base = hb; V_.B = hb.load(); V_.bare = None
            V_.base = V_.scarf('빨강', '하양'); V_.B = V_.base.load()
        g = V_.gloves('초록', '하양')
        cell(g if g is not None else V_.base, 4 + c, r); V_.base = keep; V_.B = keep.load()
os.makedirs(OUTD, exist_ok=True); img.save(os.path.join(OUTD, 'knit_npc_preview.png')); print('ok')
