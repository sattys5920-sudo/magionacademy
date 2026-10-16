# 넓은 캠퍼스 맵 (아이소메트릭): 땅 배경 + 건물·나무·가로등 스프라이트(발판 상자 포함) + 문
import json, math, random
from PIL import Image, ImageDraw
random.seed(5)
NX, NY = 34, 34
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 150
OX, OY = NY * 8 + 20, 120
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def inv(x, y):
    a, b = (x - OX) / 8, (y - OY) / 4
    return (a + b) / 2, (b - a) / 2
OUTL = hexc('#1C1420')
# ---- 땅 종류 ----
PATH = set(); PLAZA = set(); WATER = set()
def rect(s, x0, y0, x1, y1):
    for x in range(x0, x1):
        for y in range(y0, y1): s.add((x, y))
rect(PATH, 15, 10, 18, 34)          # 정문 → 본관 큰길
rect(PATH, 4, 15, 31, 18)           # 동서 길
rect(PATH, 27, 10, 29, 15)          # 온실 가는 길
rect(PATH, 9, 21, 15, 23)           # 기숙사 가는 길
rect(PATH, 21, 23, 24, 25)          # 사육장 문 앞
rect(PLAZA, 12, 12, 21, 21)         # 분수 광장
rect(PLAZA, 11, 25, 21, 32)         # 시장 광장
GRASS = [hexc('#5E9A4A'), hexc('#548E42'), hexc('#68A452'), hexc('#4E863E')]
STONE = [hexc('#B8AE9C'), hexc('#A89E8C'), hexc('#C4BAA6'), hexc('#9E9482')]
bg = Image.new('RGBA', (W, H), hexc('#2A3A2A')); px = bg.load()
for y in range(H):
    for x in range(W):
        fx, fy = inv(x, y)
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = (int(fx), int(fy))
        if t in PATH or t in PLAZA:
            # 돌길: 작은 돌 블록
            bx, by = int(fx * 3 + (int(fy * 3) % 2) * 0.5), int(fy * 3)
            c = STONE[(bx * 7 + by * 3) % 4]
            if (fx * 3 + (int(fy * 3) % 2) * 0.5) % 1 < .12 or (fy * 3) % 1 < .14: c = hexc('#7E7464')
            if t in PLAZA and t not in PATH: c = shade(c, 1.04)
        else:
            n = (int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4
            c = GRASS[n]
            if random.random() < .012: c = random.choice([hexc('#F2E27A'), hexc('#F2A0C0'), hexc('#FFFFFF'), hexc('#A8C8FF')])
        px[x, y] = c
# 땅 가장자리 (앞쪽 두 면에 흙 단면)
for x in range(W):
    for y in range(H):
        fx, fy = inv(x, y - 0)
        if (fx >= NX or fy >= NY) and 0 <= fx < NX + .9 and 0 <= fy < NY + .9:
            gx, gy = inv(x, y - 10)
            if 0 <= gx < NX and 0 <= gy < NY and px[x, y][:3] == (0x2A, 0x3A, 0x2A):
                px[x, y] = hexc('#6A4A30') if (y // 3) % 2 else hexc('#5A3E28')
bg.save('out/campus_bg.png')
# ---- 스프라이트 ----
def poly(d, pts, c): d.polygon([tuple(map(int, p)) for p in pts], fill=c)
def up(p, k): return (p[0], p[1] - k)
def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200: add.append((x, y)); break
    for x, y in add: a[x, y] = c
def face(img, x0, y0, x1, y1, side, fn, v0=0, v1=999):
    """앞 두 면에 픽셀 칠하기. side 'L': y=y1 면(왼쪽 앞), 'R': x=x1 면(오른쪽 앞). fn(u, v) → 색"""
    a = img.load()
    if side == 'L': bx, by = P(x0, y1); length = (x1 - x0) * 8; dy = .5
    else: bx, by = P(x1, y1); length = (y1 - y0) * 8; dy = -.5
    for u in range(int(length)):
        for v in range(int(v0), int(v1)):
            c = fn(u, v)
            if c is None: continue
            X, Y = int(bx + u), int(by + u * dy - v)
            if 0 <= X < img.width and 0 <= Y < img.height: a[X, Y] = c
objs = []
def add_obj(name, box, draw, door=None, solid=True):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw(img); outline(img)
    bb = img.getbbox(); spr = img.crop(bb)
    objs.append(dict(name=name, box=box, x=bb[0], y=bb[1], img=spr, door=door, solid=solid))
def building(x0, y0, x1, y1, h, wall, trim, roof, rh, win, doors=(), tower=False):
    def draw(img):
        d = ImageDraw.Draw(img)
        T, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
        # 벽 두 면
        def wall_fn(side, dark):
            length = ((x1 - x0) if side == 'L' else (y1 - y0)) * 8
            def f(u, v):
                if v >= h: return None
                c = wall
                row = v // 5
                if v % 5 == 0 or (u + (row % 2) * 6) % 12 == 0: c = shade(wall, .82)
                if v < 6: c = shade(trim, .8)
                if h - 4 <= v: c = trim
                for (wu, wv, ww, wh_) in win(side, length):
                    uu, vv = u - wu, v - wv
                    if 0 <= uu < ww and 0 <= vv < wh_:
                        top = wh_ - ww / 2
                        if vv > top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2) ** 2: continue
                        edge = uu == 0 or uu == ww - 1 or vv == 0 or (vv > top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2 - 1.2) ** 2)
                        c = shade(trim, .6) if edge else (hexc('#FFD98A') if (uu + vv) % 7 else hexc('#FFF0C0')) if vv < wh_ * .55 or uu < ww / 2 else hexc('#F2B860')
                        if not edge and uu == ww // 2: c = shade(trim, .6)
                for (ds, du, dw) in doors:
                    if ds != side: continue
                    uu = u - du
                    if 0 <= uu < dw and v < 22:
                        top = 22 - dw / 2
                        if v > top and (uu + .5 - dw / 2) ** 2 + (v - top) ** 2 > (dw / 2) ** 2: continue
                        c = hexc('#5A3420') if 0 < uu < dw - 1 and v > 0 else shade(trim, .55)
                        if uu == dw // 2: c = hexc('#3E2216')
                        if v == 10 and uu in (dw // 2 - 2, dw // 2 + 1): c = hexc('#E0C070')
                return shade(c, dark)
            return f
        face(img, x0, y0, x1, y1, 'L', wall_fn('L', .9)); face(img, x0, y0, x1, y1, 'R', wall_fn('R', 1.0))
        # 지붕 (박공·모임지붕)
        long_x = (x1 - x0) >= (y1 - y0)
        if long_x:
            r1, r2 = P(x0 + (y1 - y0) / 2, (y0 + y1) / 2), P(x1 - (y1 - y0) / 2, (y0 + y1) / 2)
        else:
            r1, r2 = P((x0 + x1) / 2, y0 + (x1 - x0) / 2), P((x0 + x1) / 2, y1 - (x1 - x0) / 2)
        R1, R2 = up(r1, h + rh), up(r2, h + rh)
        Th, Rh, Bh, Lh = up(T, h), up(R, h), up(B, h), up(L, h)
        dark, mid, light = shade(roof, .7), shade(roof, .85), roof
        if long_x:
            poly(d, [Th, Rh, R2, R1], dark); poly(d, [Th, Lh, R1], dark)
            poly(d, [Rh, Bh, R2], mid); poly(d, [Lh, Bh, R2, R1], light)
        else:
            poly(d, [Th, Lh, R1], dark); poly(d, [Th, Rh, R2, R1], dark)
            poly(d, [Lh, Bh, R2, R1], mid); poly(d, [Rh, Bh, R2], light)
        # 지붕 기와 줄
        a = img.load()
        for yy in range(int(min(R1[1], R2[1])), int(Bh[1]) + 1, 3):
            for xx in range(int(Lh[0]), int(Rh[0]) + 1):
                if 0 <= xx < W and 0 <= yy < H and a[xx, yy][3] and a[xx, yy][:3] in (light[:3], mid[:3]): a[xx, yy] = shade(a[xx, yy], .9)
        d.line([tuple(map(int, R1)), tuple(map(int, R2))], fill=shade(trim, .9))
        if tower:
            tx, ty = tower; cx_, cy_ = up(P(tx, ty), h + rh - 6)
            d.rectangle([cx_ - 7, cy_ - 30, cx_ + 7, cy_], fill=wall); d.rectangle([cx_ - 7, cy_ - 30, cx_, cy_], fill=shade(wall, .9))
            d.rectangle([cx_ - 3, cy_ - 24, cx_ + 2, cy_ - 14], fill=hexc('#FFD98A'))
            d.polygon([(cx_ - 9, cy_ - 30), (cx_, cy_ - 52), (cx_ + 9, cy_ - 30)], fill=roof); d.polygon([(cx_ - 9, cy_ - 30), (cx_, cy_ - 52), (cx_, cy_ - 30)], fill=dark)
            d.rectangle([cx_ - 1, cy_ - 56, cx_, cy_ - 52], fill=hexc('#E0C070'))
    return draw
# 본관 (문: 왼쪽 앞면 가운데)
def main_win(side, length):
    out = []
    for u in range(10, int(length) - 8, 16):
        if side == 'L' and abs(u + 4 - length / 2) < 12: continue
        out += [(u, 14, 8, 16), (u, 40, 8, 14)]
    return out
add_obj('main', [10, 2, 22, 10], building(10, 2, 22, 10, 64, hexc('#D8CCB4'), hexc('#8A6A4A'), hexc('#4A3E6A'), 30, main_win, doors=[('L', 44, 10)], tower=(19, 6)), door=dict(tile=[16, 10], to='lab', label='본관 · 물약 연구실'))
# 온실 (유리)
def greenhouse(img):
    x0, y0, x1, y1, h = 24, 4, 31, 10, 30
    glass = hexc('#A8E0E8', 200); glass2 = hexc('#D8F4F8', 220); frame = hexc('#F2EAD8')
    def f(u, v):
        if v >= h: return None
        if u % 8 == 0 or v % 10 == 0 or v < 2: return frame
        c = glass if (u + v) % 9 else glass2
        if v < 12 and (u * 3 + v) % 7 < 3: c = hexc('#5EAE5A')
        if v < 10 and (u * 5 + v * 3) % 13 == 0: c = hexc('#F2A0C0')
        return c
    face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
    d = ImageDraw.Draw(img)
    T, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
    r1, r2 = up(P(x0, (y0 + y1) / 2), 18), up(P(x1, (y0 + y1) / 2), 18)
    poly(d, [T, R, (r2[0], r2[1]), (r1[0], r1[1])], hexc('#B8E8F0', 210)); poly(d, [L, B, r2, r1], hexc('#D0F2F6', 230)); poly(d, [R, B, r2], hexc('#C0ECF2', 220))
    for k in range(0, 8): a, b = P(x0 + k, y1), P(x0 + k, (y0 + y1) / 2); d.line([up(a, h), up(b, h + 18)], fill=frame)
    face(img, x0, y0, x1, y1, 'L', lambda u, v: hexc('#6A5A4A') if 0 <= u - 24 < 8 and v < 18 and (u - 24) not in (0, 7) else None)
add_obj('greenhouse', [24, 4, 31, 10], greenhouse, door=dict(tile=[27, 10], to=None, label='약초 온실'))
# 기숙사 (4가지 색 문)
def dorm_win(side, length):
    return [(u, 30, 7, 12) for u in range(8, int(length) - 6, 14)] + ([(u, 10, 7, 10) for u in range(8, int(length) - 6, 28)] if side == 'L' else [])
dorm_draw = building(3, 18, 9, 26, 52, hexc('#C8A888'), hexc('#6A4A3A'), hexc('#7A3A3A'), 26, dorm_win, doors=[('R', 14, 9), ('R', 34, 9)])
def dorm(img):
    dorm_draw(img)
    for i, col in enumerate(['#5CCB8E', '#F08A3C', '#E8709A', '#7A66E0']):
        face(img, 3, 18, 9, 26, 'R', (lambda c: lambda u, v: hexc(c) if 0 <= u - (10 + i * 12) < 6 and 26 <= v < 34 and (u + v) % 2 == 0 else None)(col))
add_obj('dorm', [3, 18, 9, 26], dorm, door=dict(tile=[9, 22], to=None, label='기숙사'))
# 헛간
add_obj('barn', [27, 20, 31, 24], building(27, 20, 31, 24, 30, hexc('#A84A3A'), hexc('#F2EAD8'), hexc('#6A3A2A'), 16, lambda s, l: [], doors=[('L', 12, 12)]))
# 분수
def fountain(img):
    d = ImageDraw.Draw(img); cx, cy = P(16.5, 16.5)
    d.ellipse([cx - 22, cy - 8, cx + 22, cy + 12], fill=hexc('#A89E8C')); d.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=hexc('#C4BAA6'))
    d.ellipse([cx - 17, cy - 6, cx + 17, cy + 6], fill=hexc('#5AA8D8')); d.ellipse([cx - 11, cy - 4, cx + 3, cy + 1], fill=hexc('#8ACCF0'))
    d.rectangle([cx - 3, cy - 18, cx + 3, cy], fill=hexc('#B8AE9C')); d.ellipse([cx - 8, cy - 22, cx + 8, cy - 15], fill=hexc('#C4BAA6'))
    d.ellipse([cx - 6, cy - 21, cx + 6, cy - 16], fill=hexc('#5AA8D8'))
    for dx in (-5, 0, 5): d.line([(cx + dx, cy - 22), (cx + dx * 2, cy - 28 + abs(dx))], fill=hexc('#C8EEFF'))
add_obj('fountain', [15, 15, 18, 18], fountain)
# 시장 가판대
for i, (sx, sy, col) in enumerate(((12, 26, '#C84A4A'), (15, 26, '#4A8AC8'), (18, 26, '#E0A030'), (12, 29, '#7A5AC8'), (18, 29, '#4AA86A'))):
    def stall(img, sx=sx, sy=sy, col=col):
        d = ImageDraw.Draw(img)
        T, R, B, L = P(sx, sy), P(sx + 2, sy), P(sx + 2, sy + 1), P(sx, sy + 1)
        poly(d, [L, B, up(B, 8), up(L, 8)], hexc('#7A4A2E')); poly(d, [B, R, up(R, 8), up(B, 8)], hexc('#8A5636')); poly(d, [up(T, 8), up(R, 8), up(B, 8), up(L, 8)], hexc('#A86A44'))
        for k, c2 in enumerate(['#E05A5A', '#5AC85A', '#F2D25A', '#C08AFF']):
            x, y = P(sx + .4 + k * .4, sy + .5); d.ellipse([x - 2, y - 11, x + 2, y - 8], fill=hexc(c2))
        for p_ in (L, B, R): d.line([tuple(map(int, up(p_, 8))), tuple(map(int, up(p_, 22)))], fill=hexc('#5A3A22'))
        a1, a2, a3, a4 = up(T, 22), up(R, 22), up(B, 24), up(L, 24)
        poly(d, [a1, a2, a3, a4], hexc(col))
        for k in range(4):
            q1 = (a4[0] + (a3[0] - a4[0]) * k / 4, a4[1] + (a3[1] - a4[1]) * k / 4); q2 = (a4[0] + (a3[0] - a4[0]) * (k + .5) / 4, a4[1] + (a3[1] - a4[1]) * (k + .5) / 4)
            q3 = (a1[0] + (a2[0] - a1[0]) * (k + .5) / 4, a1[1] + (a2[1] - a1[1]) * (k + .5) / 4); q4 = (a1[0] + (a2[0] - a1[0]) * k / 4, a1[1] + (a2[1] - a1[1]) * k / 4)
            poly(d, [q1, q2, q3, q4], hexc('#F2EAD8'))
    add_obj('stall', [sx, sy, sx + 2, sy + 1], stall)
# 울타리 (사육장)
FENCE = []
for x in range(22, 32): FENCE += [(x, 19), (x, 30)]
for y in range(19, 31): FENCE += [(22, y), (32, y)]
FENCE = [t for t in FENCE if not (t[0] == 22 and t[1] in (23, 24))]
def fence_post(img, t):
    d = ImageDraw.Draw(img); x, y = P(t[0] + .5, t[1] + .5)
    d.rectangle([x - 1, y - 10, x, y], fill=hexc('#E8DCC8')); d.rectangle([x - 1, y - 10, x - 1, y], fill=hexc('#C8B8A0'))
    for dy in (-8, -4):
        if (t[0] + 1, t[1]) in FENCE: d.line([(x, y + dy), (x + 8, y + dy + 4)], fill=hexc('#E8DCC8'))
        if (t[0], t[1] + 1) in FENCE: d.line([(x, y + dy), (x - 8, y + dy + 4)], fill=hexc('#E8DCC8'))
for t in FENCE: add_obj('fence', [t[0], t[1], t[0] + 1, t[1] + 1], (lambda tt: lambda img: fence_post(img, tt))(t))
# 나무
BLOCK = set(PATH) | set(PLAZA)
for o in objs: 
    b = o['box']; rect(BLOCK, b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1)
rect(BLOCK, 22, 19, 33, 31)
trees = []
for (x, y) in [(2, 3), (4, 2), (6, 5), (2, 8), (5, 10), (8, 12), (2, 13), (24, 13), (31, 12), (33, 15), (2, 28), (5, 29), (8, 31), (3, 32), (10, 33), (21, 32), (24, 33), (27, 32), (31, 32), (33, 27), (9, 7), (7, 1), (32, 2), (33, 6), (20, 11), (11, 11), (11, 22), (20, 22)]:
    if (x, y) not in BLOCK and 0 <= x < NX and 0 <= y < NY: trees.append((x, y))
def tree(img, x, y, big):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 2, cy - 12, cx + 1, cy], fill=hexc('#6A4A30')); d.rectangle([cx - 2, cy - 12, cx - 1, cy], fill=hexc('#7E5A3A'))
    r = 11 if big else 9; g1, g2, g3 = hexc('#3E7A3A'), hexc('#4E9244'), hexc('#6AAE52')
    for dx, dy, rr in ((-6, -16, r - 3), (6, -16, r - 3), (0, -24, r - 1), (0, -14, r - 2)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
    for dx, dy, rr in ((-4, -20, r - 5), (4, -22, r - 5), (-1, -27, r - 6)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
    for dx, dy in ((-5, -24), (2, -29), (-2, -21), (5, -25)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=g3)
for i, (x, y) in enumerate(trees): add_obj('tree', [x, y, x + 1, y + 1], (lambda a, b, c: lambda img: tree(img, a, b, c))(x, y, i % 3 == 0))
# 가로등
LAMPS = [(14, 11), (18, 11), (14, 22), (18, 22), (14, 33), (18, 33), (10, 14), (23, 14), (27, 18), (8, 18)]
def lamp(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 26, cx, cy], fill=hexc('#2E3A3A')); d.rectangle([cx - 2, cy - 2, cx + 1, cy], fill=hexc('#2E3A3A'))
    d.rectangle([cx - 3, cy - 33, cx + 2, cy - 26], fill=hexc('#2E3A3A')); d.rectangle([cx - 2, cy - 32, cx + 1, cy - 27], fill=hexc('#FFE0A0'))
    d.polygon([(cx - 4, cy - 33), (cx - .5, cy - 37), (cx + 3, cy - 33)], fill=hexc('#2E3A3A'))
for (x, y) in LAMPS: add_obj('lamp', [x, y, x + 1, y + 1], (lambda a, b: lambda img: lamp(img, a, b))(x, y))
# 정문 아치
def gate(img):
    d = ImageDraw.Draw(img)
    for x in (14.6, 18.4):
        cx, cy = P(x, 33.6); d.rectangle([cx - 3, cy - 34, cx + 3, cy], fill=hexc('#8A8070')); d.rectangle([cx - 3, cy - 34, cx, cy], fill=hexc('#A89E8C'))
    a, b = up(P(14.6, 33.6), 34), up(P(18.4, 33.6), 34)
    d.line([a, b], fill=hexc('#2E3A3A'), width=3)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 6); d.ellipse([m[0] - 5, m[1] - 5, m[0] + 5, m[1] + 5], fill=hexc('#E0C070')); d.ellipse([m[0] - 2, m[1] - 2, m[0] + 2, m[1] + 2], fill=hexc('#4A3E6A'))
add_obj('gate', [14, 33, 15, 34], gate, solid=False)
# 시트 저장 (줄바꿈 배치)
rowW, x, y, rowH, place = 1024, 0, 0, 0, []
for o in objs:
    w_, h_ = o['img'].size
    if x + w_ > rowW: x = 0; y += rowH + 1; rowH = 0
    place.append((x, y)); x += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, y + rowH + 1), (0, 0, 0, 0))
meta = []
for o, (sx, sy) in zip(objs, place):
    sheet.paste(o['img'], (sx, sy))
    meta.append(dict(name=o['name'], box=o['box'], sx=sx, sy=sy, sw=o['img'].width, sh=o['img'].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid']))
sheet.save('out/campus_obj.png')
lights = [dict(p=P(x + .5, y + .5), dy=-30, r=34, c=[255, 210, 140], a=.6, f=1) for x, y in LAMPS]
lights += [dict(p=up(P(16, 10), 30), dy=0, r=50, c=[255, 200, 120], a=.35, f=0), dict(p=up(P(9, 22), 26), dy=0, r=40, c=[255, 200, 120], a=.3, f=0), dict(p=up(P(27.5, 7), 15), dy=0, r=46, c=[150, 255, 190], a=.25, f=0)]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, start=[16, 31]), open('out/campus.json', 'w'))
print('objs', len(objs), 'size', W, H, 'sheet', sheet.size)
