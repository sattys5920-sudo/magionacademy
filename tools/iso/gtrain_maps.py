# 유령 열차 목적지 5곳 (26x20, 아이소 8:4, arena.py와 같은 그림체)
#   python3 gtrain_maps.py lake|field|grave|forest|cave  → out/gt_<id>_bg.png · _obj.png · .json
#   python3 gtrain_maps.py all                            → 다섯 곳 모두
#   서쪽 가장자리(x 1~3.6)에 유령 열차가 서 있고, 그 옆 승강장(x 3.8~5.8)에서 내려요. 채집 반짝이 자리는 json 'forage' (x, y)
import json, math, os, random, sys, importlib
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NX, NY = 26, 20
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 220
OX, OY = NY * 8 + 20, 180
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#120A18')
_src = open('world.py').read()
exec(_src[_src.index('def poly(d, pts, c)'):_src.index('# 본관 (크게, 탑 두 개)')])

TITLE = {'lake': '안개 호수', 'field': '별똥 들판', 'grave': '잊힌 묘지역', 'forest': '거꾸로 숲', 'cave': '수정 동굴역'}
PLAT = (3.8, 5.8, 6.0, 14.0)          # 승강장 x0, x1, y0, y1
SPAWN = [7, 10]


# ======================================================================= 땅
def ground(kind, T, rnd):
    bg = Image.new('RGBA', (W, H), hexc('#140E1E')); px = bg.load()
    GR = {'grass': [hexc('#3E4E3A'), hexc('#36463A'), hexc('#46563E'), hexc('#3A4436')],
          'meadow': [hexc('#46583E'), hexc('#3E5038'), hexc('#4E6244'), hexc('#42543C')],
          'moss': [hexc('#2E4440'), hexc('#28403C'), hexc('#36504A'), hexc('#2A3A38')],
          'grave': [hexc('#3A3E34'), hexc('#34382E'), hexc('#42463A')],
          'cavef': [hexc('#3A3448'), hexc('#342E42'), hexc('#40384E'), hexc('#2E2A3C')]}
    for y in range(H):
        for x in range(W):
            a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
            if not (0 <= fx < NX and 0 <= fy < NY): continue
            t = T[(int(fx), int(fy))]
            if t == 'dirt':
                c = hexc('#6A5444') if rnd.random() > .12 else hexc('#5E4A3C')
            elif t == 'stone':
                s_ = 2; bx, by = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
                c = [hexc('#5E5868'), hexc('#545060'), hexc('#68627A')][(bx * 5 + by * 3) % 3]
                if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#3A3646')
            elif t == 'water':
                c = hexc('#2E5A6A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#4A7A8A')
                if rnd.random() < .015: c = hexc('#A8E8F0')
            elif t == 'cpool':
                c = hexc('#1E4A6A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#3A7AA8')
                if rnd.random() < .02: c = hexc('#BFF4FF')
            elif t == 'dock':
                c = hexc('#7A5A3E') if int(fx * 3) % 2 else hexc('#6A4C34')
                if (fx * 3) % 1 < .1: c = hexc('#3A2A1E')
            elif t == 'plat':
                c = hexc('#6E5040') if int(fy * 2) % 2 else hexc('#5A4034')
            elif t == 'void':
                c = hexc('#1a1430') if rnd.random() > .02 else hexc('#BDB0D6')
            else:
                L = GR.get(t, GR['grass'])
                c = L[(int(fx * 4) * 13 + int(fy * 4) * 7 + rnd.randint(0, 2)) % len(L)]
                if t == 'meadow' and rnd.random() < .03: c = rnd.choice([hexc('#FFE680'), hexc('#E8E8FF'), hexc('#C8A8FF'), hexc('#FF9AC8')])
                elif t == 'grass' and rnd.random() < .004: c = rnd.choice([hexc('#C86AE8'), hexc('#E8A050'), hexc('#8AE8C8')])
                elif t == 'moss' and rnd.random() < .01: c = hexc('#9EE8DC')
                elif t == 'cavef' and rnd.random() < .006: c = rnd.choice([hexc('#7CDCF0'), hexc('#C8A8FF')])
            px[x, y] = c
    edge = hexc('#2A2236') if kind == 'cave' else hexc('#3A2A24')
    for x in range(W):
        for y in range(H):
            if px[x, y][:3] != (0x14, 0x0E, 0x1E): continue
            a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
            if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = edge if (y // 3) % 2 else shade(edge, .8)
    # 안개(호수·묘지): 바닥 위 옅은 띠
    if kind in ('lake', 'grave'):
        fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fog)
        for _ in range(26):
            cx, cy = P(rnd.uniform(3, NX - 2), rnd.uniform(3, NY - 2))
            d.ellipse([cx - 40, cy - 9, cx + 40, cy + 9], fill=(189, 176, 214, 26))
        bg.alpha_composite(fog)
    return bg


# ======================================================================= 그림
def dark_tree(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 'dead':
            d.line([(cx, cy), (cx, cy - 22)], fill=hexc('#3A2E2A'), width=3)
            for (a, b, c_, e) in ((0, -14, -9, -22), (0, -18, 8, -27), (-6, -19, -10, -26), (5, -24, 3, -31), (0, -22, -3, -32)): d.line([(cx + a, cy + b), (cx + c_, cy + e)], fill=hexc('#3A2E2A'), width=2 if b > -18 else 1)
            return
        d.rectangle([cx - 2, cy - 12, cx + 1, cy], fill=hexc('#3A2A24'))
        if kind == 'pine':
            for k, (wd, yy) in enumerate(((11, -12), (9, -20), (7, -28), (4, -35))): d.polygon([(cx - wd, cy + yy), (cx, cy + yy - 12), (cx + wd, cy + yy)], fill=hexc('#22382E') if k % 2 else hexc('#2A4434'))
            return
        g1, g2, g3 = (hexc('#2E3E36'), hexc('#3A4E40'), hexc('#4E6450')) if kind == 'round' else (hexc('#4A2E4E'), hexc('#5E3A62'), hexc('#7A4E7E')) if kind == 'purple' else (hexc('#1E4A4A'), hexc('#2A6262'), hexc('#4A8A84'))
        r = 10
        for dx, dy, rr in ((-6, -16, r - 3), (6, -16, r - 3), (0, -24, r - 1), (0, -14, r - 2)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
        for dx, dy, rr in ((-4, -20, r - 5), (4, -22, r - 5), (-1, -27, r - 6)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
        for dx, dy in ((-5, -24), (2, -29), (5, -25)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=g3)
    return f


def upside_tree(col):
    """거꾸로 나무: 잎뭉치가 땅에 닿고 뿌리가 하늘로 뻗어요"""
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        g1, g2, g3 = (hexc(c) for c in col)
        for dx, dy, rr in ((-7, -7, 7), (7, -7, 7), (0, -10, 9), (0, -4, 7)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
        for dx, dy, rr in ((-4, -10, 4), (4, -8, 4), (0, -13, 3)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
        d.rectangle([cx - 2, cy - 30, cx + 1, cy - 16], fill=hexc('#4A3A30'))
        for (a, b, c_, e) in ((0, -28, -8, -36), (0, -30, 7, -39), (-1, -26, -12, -30), (1, -27, 11, -31), (0, -31, -2, -42)):
            d.line([(cx + a, cy + b), (cx + c_, cy + e)], fill=hexc('#4A3A30'), width=2 if abs(e - b) < 9 else 1)
        for dx, dy in ((-5, -8), (3, -12), (5, -5)): d.point((cx + dx, cy + dy), fill=g3)
    return f


def lamp_at(col, hi):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 1, cy - 28, cx, cy], fill=hexc('#2A2230')); d.line([(cx, cy - 28), (cx + 6, cy - 30)], fill=hexc('#2A2230'))
        d.ellipse([cx + 3, cy - 30, cx + 10, cy - 22], fill=hexc(col)); d.ellipse([cx + 5, cy - 28, cx + 8, cy - 24], fill=hexc(hi))
    return f


def tomb_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 0:
            d.rectangle([cx - 4, cy - 10, cx + 4, cy], fill=hexc('#8A8A92')); d.ellipse([cx - 4, cy - 14, cx + 4, cy - 6], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 10, cx - 1, cy], fill=hexc('#9A9AA2'))
            d.line([(cx - 2, cy - 9), (cx + 2, cy - 9)], fill=hexc('#5A5A62')); d.line([(cx - 2, cy - 6), (cx + 2, cy - 6)], fill=hexc('#5A5A62'))
        elif kind == 1:
            d.rectangle([cx - 1, cy - 14, cx + 1, cy], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 11, cx + 4, cy - 9], fill=hexc('#8A8A92'))
        else:   # 기울어진 이끼 낀 묘비
            d.polygon([(cx - 5, cy), (cx + 3, cy), (cx + 6, cy - 11), (cx - 2, cy - 12)], fill=hexc('#7A7A84'))
            d.polygon([(cx - 5, cy), (cx - 2, cy - 12), (cx, cy - 12), (cx - 3, cy)], fill=hexc('#8E8E98'))
            d.point((cx + 2, cy - 4), fill=hexc('#5CA88A')); d.point((cx - 1, cy - 2), fill=hexc('#5CA88A'))
        d.ellipse([cx - 6, cy - 2, cx + 6, cy + 2], fill=hexc('#2E3228'))
    return f


def crystal_at(col, big):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        c1, c2, c3 = (hexc(c) for c in col)
        d.ellipse([cx - 9, cy - 3, cx + 9, cy + 3], fill=hexc('#2E2A3C'))
        spikes = ((-5, 0, 12, 3), (5, 0, 10, 3), (0, 0, 20 if big else 15, 4), (-2, 1, 8, 2), (7, 1, 6, 2))
        for (dx, dy, hgt, w) in spikes:
            bx, by = cx + dx, cy + dy
            d.polygon([(bx - w, by), (bx + w, by), (bx + w, by - hgt + w), (bx, by - hgt), (bx - w, by - hgt + w)], fill=c2)
            d.polygon([(bx - w, by), (bx, by), (bx, by - hgt), (bx - w, by - hgt + w)], fill=c1)
            d.line([(bx + w - 1, by - 1), (bx + w - 1, by - hgt + w + 1)], fill=c3)
    return f


def stalag(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.polygon([(cx - 6, cy), (cx + 6, cy), (cx + 1, cy - 26), (cx - 1, cy - 26)], fill=hexc('#5A5470'))
    d.polygon([(cx - 6, cy), (cx, cy), (cx - 1, cy - 26)], fill=hexc('#6E6886'))
    d.polygon([(cx + 7, cy + 1), (cx + 12, cy + 1), (cx + 9, cy - 12)], fill=hexc('#4E4864'))


def mush_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for dx, s_ in ((-4, 1), (3, 0), (0, 1)):
            h_ = 8 if s_ else 5
            d.rectangle([cx + dx - 1, cy - h_, cx + dx, cy], fill=hexc('#E8E0F0'))
            d.ellipse([cx + dx - 4 - s_, cy - h_ - 4, cx + dx + 3 + s_, cy - h_ + 1], fill=hexc(col))
            d.point((cx + dx - 1, cy - h_ - 2), fill=hexc('#FFFFFF'))
    return f


def star_crater(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 10, cy - 4, cx + 10, cy + 4], fill=hexc('#2E3A2C')); d.ellipse([cx - 7, cy - 3, cx + 7, cy + 2], fill=hexc('#1E2A1E'))
    d.polygon([(cx, cy - 10), (cx + 2, cy - 4), (cx + 7, cy - 4), (cx + 3, cy - 1), (cx + 4, cy + 3), (cx, cy), (cx - 4, cy + 3), (cx - 3, cy - 1), (cx - 7, cy - 4), (cx - 2, cy - 4)], fill=hexc('#FFE680'))
    d.polygon([(cx, cy - 10), (cx + 2, cy - 4), (cx, cy - 2), (cx - 2, cy - 4)], fill=hexc('#FFF6C8'))


def rock_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 2], fill=hexc('#6E6876')); d.ellipse([cx - 5, cy - 6, cx + 1, cy - 1], fill=hexc('#86808C'))


def reed(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, h_ in ((-4, 14), (-1, 18), (2, 12), (5, 16)):
        d.line([(cx + dx, cy), (cx + dx + 1, cy - h_)], fill=hexc('#4E6A3E'))
        d.rectangle([cx + dx, cy - h_ - 3, cx + dx + 1, cy - h_ + 1], fill=hexc('#6A4A2E'))


def sign_post(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 22, cx, cy], fill=hexc('#2A2230')); d.rectangle([cx + 9, cy - 17, cx + 10, cy + 3], fill=hexc('#2A2230'))
    d.polygon([(cx - 3, cy - 28), (cx + 13, cy - 23), (cx + 13, cy - 13), (cx - 3, cy - 18)], fill=hexc('#211733'))
    d.polygon([(cx - 2, cy - 26), (cx + 12, cy - 22), (cx + 12, cy - 14), (cx - 2, cy - 18)], fill=hexc('#2B1F45'))
    d.ellipse([cx + 2, cy - 25, cx + 8, cy - 17], fill=hexc('#E8FFFF'))
    d.point((cx + 4, cy - 22), fill=hexc('#211733')); d.point((cx + 6, cy - 21), fill=hexc('#211733'))


def gold_spot(img, x, y):
    """다 같이 여는 금빛 큰 반짝이 자리 (작은 받침돌)"""
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 9, cy - 4, cx + 9, cy + 4], fill=hexc('#4E4856')); d.ellipse([cx - 7, cy - 4, cx + 7, cy + 1], fill=hexc('#6E6876'))


# ======================================================================= 맵
def build(kind):
    global SPR, objs
    SPR.clear(); objs.clear()
    rnd = random.Random({'lake': 11, 'field': 22, 'grave': 33, 'forest': 44, 'cave': 55}[kind]); random.seed(rnd.random())
    base = {'lake': 'grass', 'field': 'meadow', 'grave': 'grave', 'forest': 'moss', 'cave': 'cavef'}[kind]
    T = {(x, y): base for x in range(NX) for y in range(NY)}
    def fill(k, x0, y0, x1, y1):
        for x in range(max(0, int(x0)), min(NX, int(math.ceil(x1)))):
            for y in range(max(0, int(y0)), min(NY, int(math.ceil(y1)))): T[(x, y)] = k
    def ell(k, cx, cy, rx, ry):
        for (x, y) in list(T):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: T[(x, y)] = k
    fill('void', 0, 0, 3.6, NY)                    # 열차가 서는 곳 (안개 낀 허공)
    fill('plat', PLAT[0], PLAT[2], PLAT[1], PLAT[3])
    water = []
    if kind == 'lake':
        ell('water', 16, 11, 7.5, 6.5)
        fill('dock', 9, 10, 13, 12)
        fill('dirt', 6, 9, 9, 12)
    elif kind == 'field':
        fill('dirt', 6, 9, 22, 11)
    elif kind == 'grave':
        fill('dirt', 6, 9, 24, 11); fill('dirt', 14, 3, 16, 18)
    elif kind == 'forest':
        fill('dirt', 6, 9, 12, 11); ell('dirt', 15, 10, 4, 3.5)
    elif kind == 'cave':
        fill('stone', 6, 8, 23, 12); ell('cpool', 18, 15, 4.5, 3)
    water = [[x, y] for (x, y), t in T.items() if t in ('water', 'cpool')]
    bg = ground(kind, T, rnd)
    bg.save(f'out/gt_{kind}_bg.png')

    occupied = set((x, y) for (x, y), t in T.items() if t in ('void', 'plat', 'water', 'cpool', 'dock'))
    for x in range(6, 9):
        for y in range(8, 13): occupied.add((x, y))              # 내리는 자리는 비워 둬요
    def can(x, y): return 0 <= x < NX and 0 <= y < NY and (x, y) not in occupied
    def put(name, key, x, y, **kw):
        place(name, key, x, y, **kw); occupied.add((x, y))
    for k in ('round', 'purple', 'pine', 'dead', 'teal'): shared('t_' + k, dark_tree(k))
    shared('lamp_t', lamp_at('#7AE0E0', '#E8FFFF')); shared('lamp_o', lamp_at('#FF9A3A', '#FFE08A')); shared('sign', sign_post); shared('gold', gold_spot)
    lights, forage = [], []
    def lamp(x, y, teal=True):
        if can(x, y): put('lantern', 'lamp_t' if teal else 'lamp_o', x, y); lights.append(dict(p=P(x + .5, y + .5), dy=-26, r=30, c=[122, 224, 224] if teal else [255, 160, 70], a=.6, f=1))
    # 승강장 등불·표지판
    put('sign', 'sign', 6, 7); lamp(6, 13)
    gx, gy = {'lake': (11, 15), 'field': (15, 5), 'grave': (19, 13), 'forest': (15, 10), 'cave': (13, 14)}[kind]
    put('gold', 'gold', gx, gy, solid=False)

    if kind == 'lake':
        shared('reed', reed); shared('rock', rock_at)
        for (x, y) in [(9, 6), (22, 5), (24, 15), (8, 16), (20, 18)]: lamp(x, y)
        for (x, y) in [(9, 8), (10, 14), (23, 9), (12, 17), (21, 4), (8, 13)]:
            if can(x, y): put('reed', 'reed', x, y, solid=False)
        for (x, y) in [(18, 3), (24, 12)]:
            if can(x, y): put('rock', 'rock', x, y)
        forage = [[x, y] for (x, y) in [(10, 12), (12, 9), (13, 12), (9, 15), (15, 4), (19, 4), (23, 7), (24, 14), (22, 17), (16, 18), (12, 16)]]
    elif kind == 'field':
        shared('crater', star_crater); shared('rock', rock_at)
        for (x, y) in [(10, 5), (18, 8), (21, 14), (12, 15), (17, 17), (23, 5)]:
            if can(x, y): put('crater', 'crater', x, y, solid=False); lights.append(dict(p=P(x + .5, y + .5), dy=-4, r=22, c=[255, 230, 128], a=.55, f=1))
        for (x, y) in [(8, 4), (22, 11), (9, 17), (24, 17)]: lamp(x, y, False)
        for (x, y) in [(14, 13), (20, 3)]:
            if can(x, y): put('rock', 'rock', x, y)
        forage = [[x, y] for (x, y) in [(11, 7), (13, 4), (16, 7), (19, 6), (22, 8), (12, 13), (15, 15), (19, 12), (23, 13), (20, 17), (14, 17)]]
    elif kind == 'grave':
        for k in (0, 1, 2): shared(f'tomb{k}', tomb_at(k))
        for y in (4, 6, 13, 15, 17):
            for x in range(8, 24, 2):
                if can(x, y) and rnd.random() < .7: put('tomb', f'tomb{rnd.randint(0, 2)}', x, y)
        for (x, y) in [(13, 9), (17, 12), (22, 8)]: lamp(x, y)
        forage = [[x, y] for (x, y) in [(9, 5), (13, 5), (19, 5), (23, 6), (11, 12), (17, 14), (21, 16), (9, 16), (14, 18), (22, 12), (18, 8)]]
    elif kind == 'forest':
        for c, key in ((('#4A2E6E', '#6A42A0', '#A888E0'), 'u_p'), (('#1E4A4A', '#2A6A62', '#7CC8BC'), 'u_t')): shared(key, upside_tree(c))
        shared('mush_p', mush_at('#C8A8FF')); shared('mush_t', mush_at('#7AE0E0'))
        for (x, y) in [(13, 8), (17, 12), (12, 12)]:
            if can(x, y): put('mush', 'mush_p' if x % 2 else 'mush_t', x, y, solid=False); lights.append(dict(p=P(x + .5, y + .5), dy=-8, r=18, c=[200, 168, 255], a=.5, f=1))
        forage = [[x, y] for (x, y) in [(10, 8), (11, 11), (14, 7), (16, 8), (18, 10), (17, 13), (13, 13), (19, 11), (12, 7), (15, 13), (20, 9)]]
    elif kind == 'cave':
        shared('cry_b', crystal_at(('#D8FBFF', '#7CDCF0', '#3C98C8'), True)); shared('cry_p', crystal_at(('#F0D8FF', '#B88AF0', '#6E3CB4'), False)); shared('stalag', stalag)
        for (x, y) in [(9, 5), (12, 4), (20, 6), (24, 9), (10, 15), (14, 17), (23, 17), (21, 12), (16, 6)]:
            if can(x, y): put('crystal', rnd.choice(['cry_b', 'cry_p']), x, y); lights.append(dict(p=P(x + .5, y + .5), dy=-10, r=26, c=[124, 220, 240], a=.55, f=1))
        forage = [[x, y] for (x, y) in [(10, 7), (13, 6), (17, 7), (21, 8), (11, 13), (15, 12), (19, 11), (22, 13), (12, 16), (16, 18), (24, 14)]]
    # 가장자리 나무·바위 (숲은 안쪽까지 빽빽)
    for x in range(NX):
        for y in range(NY):
            if not can(x, y) or [x, y] in forage or (T[(x, y)] in ('dirt', 'stone') and y >= 2): continue   # 길·빈터에는 나무를 안 심어요
            edge = min(NX - 1 - x, y, NY - 1 - y)
            back = y < 2                                          # 뒤쪽(화면 위) 가장자리만 빽빽하게, 앞쪽은 듬성듬성 (안이 가리지 않게)
            dens = .75 if back else (.14 if edge < 2 and kind != 'forest' else (.06 if kind == 'forest' else .0))
            if kind == 'cave' and edge < 2:
                if not back and rnd.random() < .5: continue
                if rnd.random() < .7: shared('stalag', stalag); put('stalag', 'stalag', x, y)
                continue
            if rnd.random() < dens:
                if not back and edge < 2 and kind != 'forest':
                    shared('rock', rock_at); put('rock', 'rock', x, y) if rnd.random() < .5 else put('tree', 't_dead', x, y); continue
                if kind == 'forest': put('tree', rnd.choice(['u_p', 'u_t', 'u_p']), x, y)
                elif kind == 'grave': put('tree', rnd.choice(['t_dead', 't_dead', 't_pine', 't_purple']), x, y)
                elif kind == 'field': put('tree', rnd.choice(['t_round', 't_pine', 't_round']), x, y)
                else: put('tree', rnd.choice(['t_pine', 't_dead', 't_teal', 't_round']), x, y)
    # 열차(정차 중) + 승강장 그림은 gtrain_art 로 이 지도 좌표에 맞춰 그려요
    import gtrain_art as GA
    GA.OX, GA.OY, GA.W, GA.H = OX, OY, W, H
    GA.X0, GA.X1, GA.DY = .6, 3.2, -11.5
    spr, bb = GA.train()
    key = 'train'; SPR[key] = spr
    objs.append(dict(name='gtrain', spr=key, box=[0, 3, 3, 19], x=bb[0], y=bb[1], door=None, solid=True, act=None))
    # 저장
    keys = [k for k in SPR if not k.endswith('@')]
    rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
    for k in sorted(keys, key=lambda k: -SPR[k].height):
        w_, h_ = SPR[k].size
        if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
        pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
    sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
    for k in keys: sheet.paste(SPR[k], pos[k])
    sheet.save(f'out/gt_{kind}_obj.png')
    meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
    json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, **({'water': water} if water else {}), forage=forage, gold=[gx, gy],
                   areas=[dict(n=TITLE[kind], t=[15, 10])], start=SPAWN, title=TITLE[kind]), open(f'out/gt_{kind}.json', 'w'), ensure_ascii=False)
    print(kind, 'objs', len(objs), 'sheet', sheet.size)


if __name__ == '__main__':
    ks = list(TITLE) if (len(sys.argv) < 2 or sys.argv[1] == 'all') else sys.argv[1:]
    for k in ks: build(k)
