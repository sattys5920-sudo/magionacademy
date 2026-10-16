# 넓은 학교 맵 72x72 (아이소메트릭): 땅 배경 + 스프라이트 시트(반복 그림은 한 장을 여러 곳에) + 메타
import json, math, random
from PIL import Image, ImageDraw
random.seed(9)
NX, NY = 72, 72
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 170
OX, OY = NY * 8 + 20, 130
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#1C1420')
# ---------------- 땅 지도 ----------------
T = {}  # (x,y) → 'path' 'plaza' 'water' 'sand' 'soil' 'road' 'flower'
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
def ellipse(kind, cx, cy, rx, ry):
    for x in range(NX):
        for y in range(NY):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 < 1: T[(x, y)] = kind
# 호수 (북서) + 모래 둑
ellipse('sand', 13, 13, 9.2, 7.4); ellipse('water', 13, 13, 8, 6.2)
# 큰길: 정문(남쪽 끝) → 안뜰 → 본관
fill('road', 36, 30, 40, 72)
fill('plaza', 28, 22, 48, 31)          # 본관 앞 안뜰
fill('path', 14, 33, 62, 36)           # 동서 큰길
fill('path', 23, 22, 25, 33)           # 기숙사 길
fill('path', 52, 21, 54, 33)           # 온실 길
fill('path', 60, 13, 62, 33)           # 천문탑 길
fill('path', 46, 36, 48, 44); fill('path', 47, 42, 50, 44)  # 사육장 문
fill('path', 14, 36, 16, 60); fill('path', 8, 48, 36, 51)  # 상점 거리
fill('plaza', 26, 53, 34, 60)          # 마을 광장
fill('path', 20, 16, 23, 34)           # 호수 산책로
fill('path', 10, 20, 21, 22)
fill('soil', 56, 23, 66, 30)           # 텃밭
fill('flower', 41, 37, 45, 45); fill('flower', 30, 37, 34, 45)  # 꽃밭
for x in range(NX):
    for y in range(NY): T.setdefault((x, y), 'grass')
# ---------------- 땅 그리기 ----------------
GRASS = [hexc('#5E9A4A'), hexc('#548E42'), hexc('#68A452'), hexc('#4E863E')]
STONE = [hexc('#B8AE9C'), hexc('#A89E8C'), hexc('#C4BAA6'), hexc('#9E9482')]
ROAD = [hexc('#9C8E78'), hexc('#8E806A'), hexc('#A69882')]
bg = Image.new('RGBA', (W, H), hexc('#1E2A1C')); px = bg.load()
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t in ('path', 'plaza'):
            bx, by = int(fx * 3 + (int(fy * 3) % 2) * .5), int(fy * 3)
            c = STONE[(bx * 7 + by * 3) % 4]
            if (fx * 3 + (int(fy * 3) % 2) * .5) % 1 < .12 or (fy * 3) % 1 < .14: c = hexc('#7E7464')
            if t == 'plaza' and (int(fx) + int(fy)) % 2: c = shade(c, 1.05)
        elif t == 'road':
            bx, by = int(fx * 2 + (int(fy * 2) % 2) * .5), int(fy * 2)
            c = ROAD[(bx * 5 + by * 3) % 3]
            if (fx * 2 + (int(fy * 2) % 2) * .5) % 1 < .1 or (fy * 2) % 1 < .1: c = hexc('#6E6250')
        elif t == 'water':
            c = hexc('#3E7AB8') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#5A96CC')
            if random.random() < .01: c = hexc('#BFE2FF')
        elif t == 'sand':
            c = hexc('#D8C48E') if random.random() > .1 else hexc('#C8B47E')
        elif t == 'soil':
            c = hexc('#6A4A30') if (fy * 2) % 1 < .5 else hexc('#5A3E28')
        elif t == 'flower':
            c = GRASS[int(fx * 4 + fy * 4) % 4]
            if random.random() < .18: c = random.choice([hexc('#F2E27A'), hexc('#F2A0C0'), hexc('#FFFFFF'), hexc('#C08AFF'), hexc('#FF8A6A')])
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .008: c = random.choice([hexc('#F2E27A'), hexc('#F2A0C0'), hexc('#FFFFFF')])
        px[x, y] = c
# 앞쪽 두 면 흙 단면
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x1E, 0x2A, 0x1C): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2):
            px[x, y] = hexc('#6A4A30') if (y // 3) % 2 else hexc('#5A3E28')
bg.save('out/world_bg.png')
print('bg done', W, H)
# ---------------- 스프라이트 ----------------
def poly(d, pts, c): d.polygon([tuple(map(int, p)) for p in pts], fill=c)
def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200: add.append((x, y)); break
    for x, y in add: a[x, y] = c
def render(draw):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw(img)
    bb = img.getbbox(); bb = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1)
    spr = img.crop(bb); outline(spr); return spr, bb[0], bb[1]
def face(img, x0, y0, x1, y1, side, fn, v1=999):
    a = img.load()
    if side == 'L': bx, by = P(x0, y1); length = (x1 - x0) * 8; dy = .5
    else: bx, by = P(x1, y1); length = (y1 - y0) * 8; dy = -.5
    for u in range(int(length)):
        for v in range(0, int(v1)):
            c = fn(u, v)
            if c is None: continue
            X, Y = int(bx + u), int(by + u * dy - v)
            if 0 <= X < img.width and 0 <= Y < img.height: a[X, Y] = c
SPR = {}     # 그림 이름 → (그림, 기준점에서의 x, y 차이)
objs = []    # 놓인 물건
def unique(name, box, draw, door=None, solid=True, act=None):
    spr, x, y = render(draw); key = f'{name}#{len(objs)}'; SPR[key] = spr
    objs.append(dict(name=name, spr=key, box=box, x=x, y=y, door=door, solid=solid, act=act))
def shared(key, draw_at):
    """반복 그림: 기준 타일 (20,20)에 그려 두고, 놓을 때 위치만 옮겨요"""
    if key in SPR: return
    spr, x, y = render(lambda img: draw_at(img, 20, 20)); bx, by = P(20.5, 20.5)
    SPR[key] = spr; SPR[key + '@'] = (x - bx, y - by)
def place(name, key, tx, ty, w=1, d=1, solid=True, act=None):
    ox, oy = SPR[key + '@']; bx, by = P(tx + .5, ty + .5)
    objs.append(dict(name=name, spr=key, box=[tx, ty, tx + w, ty + d], x=int(bx + ox), y=int(by + oy), door=None, solid=solid, act=act))
# ---- 건물 ----
def building(x0, y0, x1, y1, h, wall, trim, roof, rh, win, doors=(), towers=()):
    def draw(img):
        d = ImageDraw.Draw(img)
        Tt, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
        def wall_fn(side, dark):
            length = ((x1 - x0) if side == 'L' else (y1 - y0)) * 8
            wins = win(side, length)
            def f(u, v):
                if v >= h: return None
                c = wall; row = v // 5
                if v % 5 == 0 or (u + (row % 2) * 6) % 12 == 0: c = shade(wall, .82)
                if v < 6: c = shade(trim, .8)
                if h - 4 <= v: c = trim
                for (wu, wv, ww, wh_) in wins:
                    uu, vv = u - wu, v - wv
                    if 0 <= uu < ww and 0 <= vv < wh_:
                        top = wh_ - ww / 2
                        if vv > top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2) ** 2: continue
                        edge = uu == 0 or uu == ww - 1 or vv == 0 or (vv > top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2 - 1.2) ** 2)
                        c = shade(trim, .6) if edge or uu == ww // 2 else (hexc('#FFD98A') if (uu + vv) % 7 else hexc('#FFF0C0'))
                for (ds, du, dw) in doors:
                    if ds != side: continue
                    uu = u - du
                    if 0 <= uu < dw and v < 24:
                        top = 24 - dw / 2
                        if v > top and (uu + .5 - dw / 2) ** 2 + (v - top) ** 2 > (dw / 2) ** 2: continue
                        c = hexc('#5A3420') if 0 < uu < dw - 1 and v > 0 else shade(trim, .55)
                        if uu == dw // 2: c = hexc('#3E2216')
                        if v == 11 and uu in (dw // 2 - 2, dw // 2 + 1): c = hexc('#E0C070')
                return shade(c, dark)
            return f
        face(img, x0, y0, x1, y1, 'L', wall_fn('L', .9)); face(img, x0, y0, x1, y1, 'R', wall_fn('R', 1.0))
        long_x = (x1 - x0) >= (y1 - y0)
        if long_x: r1, r2 = P(x0 + (y1 - y0) / 2, (y0 + y1) / 2), P(x1 - (y1 - y0) / 2, (y0 + y1) / 2)
        else: r1, r2 = P((x0 + x1) / 2, y0 + (x1 - x0) / 2), P((x0 + x1) / 2, y1 - (x1 - x0) / 2)
        R1, R2 = up(r1, h + rh), up(r2, h + rh)
        Th, Rh, Bh, Lh = up(Tt, h), up(R, h), up(B, h), up(L, h)
        dark, mid, light = shade(roof, .7), shade(roof, .85), roof
        if long_x: poly(d, [Th, Rh, R2, R1], dark); poly(d, [Th, Lh, R1], dark); poly(d, [Rh, Bh, R2], mid); poly(d, [Lh, Bh, R2, R1], light)
        else: poly(d, [Th, Lh, R1], dark); poly(d, [Th, Rh, R2, R1], dark); poly(d, [Lh, Bh, R2, R1], mid); poly(d, [Rh, Bh, R2], light)
        a = img.load()
        for yy in range(int(min(R1[1], R2[1])), int(Bh[1]) + 1, 3):
            for xx in range(int(Lh[0]), int(Rh[0]) + 1):
                if 0 <= xx < W and 0 <= yy < H and a[xx, yy][3] and a[xx, yy][:3] in (light[:3], mid[:3]): a[xx, yy] = shade(a[xx, yy], .9)
        d.line([tuple(map(int, R1)), tuple(map(int, R2))], fill=shade(trim, .9))
        for (tx, ty, th) in towers:
            cx_, cy_ = up(P(tx, ty), h + rh - 2)
            d.rectangle([cx_ - 8, cy_ - th, cx_ + 8, cy_], fill=wall); d.rectangle([cx_ - 8, cy_ - th, cx_, cy_], fill=shade(wall, .9))
            for k in range(0, th - 16, 14): d.rectangle([cx_ - 3, cy_ - th + 10 + k, cx_ + 2, cy_ - th + 18 + k], fill=hexc('#FFD98A'))
            d.polygon([(cx_ - 10, cy_ - th), (cx_, cy_ - th - 26), (cx_ + 10, cy_ - th)], fill=roof); d.polygon([(cx_ - 10, cy_ - th), (cx_, cy_ - th - 26), (cx_, cy_ - th)], fill=dark)
            d.rectangle([cx_ - 1, cy_ - th - 30, cx_, cy_ - th - 26], fill=hexc('#E0C070'))
    return draw
def wins(step=16, rows=((14, 16), (42, 14)), skip_mid=False):
    def f(side, length):
        out = []
        for u in range(10, int(length) - 8, step):
            if skip_mid and side == 'L' and abs(u + 4 - length / 2) < 14: continue
            out += [(u, v, 8, hh) for v, hh in rows]
        return out
    return f
# 본관 (크게, 탑 두 개)
unique('main', [30, 13, 46, 22], building(30, 13, 46, 22, 74, hexc('#D8CCB4'), hexc('#8A6A4A'), hexc('#4A3E6A'), 34, wins(skip_mid=True, rows=((14, 16), (40, 14), (60, 8))), doors=[('L', 60, 12)], towers=((38, 17.5, 40),)),
       door=dict(tile=[37, 22], to='lab', label='본관 · 물약 연구실', spawn=[5, 8]))
# 기숙사
dorm = building(17, 14, 25, 22, 54, hexc('#C8A888'), hexc('#6A4A3A'), hexc('#7A3A3A'), 26, wins(14, ((10, 10), (30, 12))), doors=[('R', 26, 10)])
def dorm_draw(img):
    dorm(img)
    for i, col in enumerate(['#5CCB8E', '#F08A3C', '#E8709A', '#7A66E0']):
        face(img, 17, 14, 25, 22, 'L', (lambda c, i: lambda u, v: hexc(c) if 0 <= u - (8 + i * 14) < 6 and 44 <= v < 52 and (u + v) % 2 == 0 else None)(col, i))
unique('dorm', [17, 14, 25, 22], dorm_draw, door=dict(tile=[25, 18], to=None, label='기숙사'))
# 온실
def greenhouse(img):
    x0, y0, x1, y1, h = 49, 13, 58, 21, 32
    glass, glass2, fr = hexc('#A8E0E8', 205), hexc('#D8F4F8', 225), hexc('#F2EAD8')
    def f(u, v):
        if v >= h: return None
        if u % 8 == 0 or v % 10 == 0 or v < 2: return fr
        c = glass if (u + v) % 9 else glass2
        if v < 12 and (u * 3 + v) % 7 < 3: c = hexc('#5EAE5A')
        if v < 10 and (u * 5 + v * 3) % 13 == 0: c = hexc('#F2A0C0')
        return c
    face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
    d = ImageDraw.Draw(img); Tt, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
    r1, r2 = up(P(x0, (y0 + y1) / 2), h + 20), up(P(x1, (y0 + y1) / 2), h + 20)
    poly(d, [Tt, R, r2, r1], hexc('#B8E8F0', 215)); poly(d, [L, B, r2, r1], hexc('#D0F2F6', 230)); poly(d, [R, B, r2], hexc('#C0ECF2', 220))
    for k in range(0, 10): d.line([up(P(x0 + k, y1), h), up(P(x0 + k, (y0 + y1) / 2), h + 20)], fill=fr)
    face(img, x0, y0, x1, y1, 'L', lambda u, v: hexc('#6A5A4A') if 0 <= u - 30 < 10 and v < 20 and (u - 30) not in (0, 9) else None)
unique('greenhouse', [49, 13, 58, 21], greenhouse, door=dict(tile=[53, 21], to=None, label='약초 온실'))
# 천문탑 (원통 + 돔)
def observatory(img):
    d = ImageDraw.Draw(img); cx, cy = P(61, 9.5)
    d.rectangle([cx - 18, cy - 70, cx + 18, cy], fill=hexc('#C8BCA4')); d.rectangle([cx - 18, cy - 70, cx, cy], fill=hexc('#B4A890'))
    d.ellipse([cx - 18, cy - 6, cx + 18, cy + 6], fill=hexc('#B4A890'))
    for k in range(3): d.rectangle([cx - 4, cy - 60 + k * 18, cx + 3, cy - 50 + k * 18], fill=hexc('#FFD98A'))
    d.pieslice([cx - 22, cy - 92, cx + 22, cy - 52], 180, 360, fill=hexc('#4A6A9A')); d.pieslice([cx - 22, cy - 92, cx + 22, cy - 52], 180, 270, fill=hexc('#3A5A8A'))
    d.rectangle([cx - 3, cy - 92, cx + 3, cy - 72], fill=hexc('#2A3A5A')); d.line([(cx + 2, cy - 88), (cx + 14, cy - 98)], fill=hexc('#C49446'), width=2)
    d.rectangle([cx - 20, cy - 72, cx + 20, cy - 70], fill=hexc('#8A6A4A'))
    face(img, 59, 8, 63, 11, 'L', lambda u, v: hexc('#5A3420') if 10 <= u < 18 and v < 20 else None)
unique('observatory', [59, 8, 63, 11], observatory, door=dict(tile=[61, 11], to=None, label='천문탑'))
# 헛간
unique('barn', [57, 38, 62, 43], building(57, 38, 62, 43, 32, hexc('#A84A3A'), hexc('#F2EAD8'), hexc('#6A3A2A'), 16, lambda s, l: [], doors=[('L', 14, 14)]), door=dict(tile=[58, 43], to=None, label='헛간'))
# 상점 거리 (북쪽 줄 / 남쪽 줄)
SHOPS = [('빵집', '#E8C8A0', '#C8604A'), ('마법 지팡이점', '#C8B8D8', '#4A3E6A'), ('찻집', '#D8E0C8', '#3E7A5A'), ('서점', '#E0D0B0', '#7A4A2E'), ('옷가게', '#F0D8D8', '#A84A6A'), ('잡화점', '#D0C8B8', '#5A6A8A')]
for i, (nm, wl, rf) in enumerate(SHOPS):
    if i < 3: x0, y0, x1, y1 = 17 + i * 6, 43, 22 + i * 6, 48; dside = 'L'; dt = [19 + i * 6, 48]
    else: x0, y0, x1, y1 = 17 + (i - 3) * 6, 51, 22 + (i - 3) * 6, 56; dside = 'L'; dt = [19 + (i - 3) * 6, 56]
    bd = building(x0, y0, x1, y1, 40, hexc(wl), hexc('#6A4A3A'), hexc(rf), 18, wins(18, ((14, 12),)), doors=[(dside, 14, 10)])
    def shop(img, bd=bd, x0=x0, y0=y0, x1=x1, y1=y1, rf=rf):
        bd(img); d = ImageDraw.Draw(img)
        a1, a2 = up(P(x0, y1), 26), up(P(x1, y1), 26)
        for k in range(6):
            q = [(a1[0] + (a2[0] - a1[0]) * k / 6, a1[1] + (a2[1] - a1[1]) * k / 6), (a1[0] + (a2[0] - a1[0]) * (k + 1) / 6, a1[1] + (a2[1] - a1[1]) * (k + 1) / 6)]
            poly(d, [q[0], q[1], (q[1][0] - 4, q[1][1] + 6), (q[0][0] - 4, q[0][1] + 6)], hexc(rf) if k % 2 else hexc('#F2EAD8'))
    unique('shop', [x0, y0, x1, y1], shop, door=dict(tile=dt, to=None, label=nm))
# 분수 (안뜰)
def fountain(img):
    d = ImageDraw.Draw(img); cx, cy = P(38, 26.5)
    d.ellipse([cx - 26, cy - 9, cx + 26, cy + 14], fill=hexc('#A89E8C')); d.ellipse([cx - 24, cy - 9, cx + 24, cy + 9], fill=hexc('#C4BAA6'))
    d.ellipse([cx - 21, cy - 7, cx + 21, cy + 7], fill=hexc('#5AA8D8')); d.ellipse([cx - 13, cy - 5, cx + 3, cy + 1], fill=hexc('#8ACCF0'))
    d.rectangle([cx - 3, cy - 22, cx + 3, cy], fill=hexc('#B8AE9C')); d.ellipse([cx - 9, cy - 26, cx + 9, cy - 18], fill=hexc('#C4BAA6')); d.ellipse([cx - 7, cy - 25, cx + 7, cy - 19], fill=hexc('#5AA8D8'))
    d.rectangle([cx - 2, cy - 34, cx + 1, cy - 25], fill=hexc('#B8AE9C')); d.ellipse([cx - 4, cy - 38, cx + 3, cy - 32], fill=hexc('#E0C070'))
unique('fountain', [36, 25, 40, 29], fountain, act=('동전을 던지면 소원이 이뤄진대요', '소원 빌기'))
# 마을 광장 우물 + 게시판
def well(img):
    d = ImageDraw.Draw(img); cx, cy = P(30, 56)
    d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=hexc('#8A8070')); d.rectangle([cx - 10, cy - 8, cx + 10, cy], fill=hexc('#A89E8C')); d.ellipse([cx - 10, cy - 12, cx + 10, cy - 4], fill=hexc('#B8AE9C')); d.ellipse([cx - 7, cy - 10, cx + 7, cy - 6], fill=hexc('#2A4A6A'))
    for sx in (-9, 8): d.rectangle([cx + sx, cy - 28, cx + sx + 1, cy - 6], fill=hexc('#6A4A30'))
    d.polygon([(cx - 13, cy - 26), (cx, cy - 34), (cx + 13, cy - 26)], fill=hexc('#7A3A3A'))
unique('well', [29, 55, 31, 57], well, act=('마을 우물', '물 길어 오기'))
def board(img):
    d = ImageDraw.Draw(img); cx, cy = P(33, 53.5)
    for sx in (-7, 6): d.rectangle([cx + sx, cy - 20, cx + sx + 1, cy], fill=hexc('#5A3A22'))
    d.rectangle([cx - 9, cy - 22, cx + 9, cy - 10], fill=hexc('#8A5636')); d.rectangle([cx - 7, cy - 20, cx - 1, cy - 13], fill=hexc('#F2EAD8')); d.rectangle([cx + 1, cy - 19, cx + 6, cy - 12], fill=hexc('#FFE8A0'))
unique('board', [33, 53, 34, 54], board, act=('학교 게시판', '소식 보기'))
# 선착장 (호수)
def dock(img):
    d = ImageDraw.Draw(img)
    for k in range(5):
        a, b = P(19.5 - k, 14), P(19.5 - k, 16)
        poly(d, [a, (a[0] + 8, a[1] + 4), (b[0] + 8, b[1] + 4), b], hexc('#8A5A36') if k % 2 else hexc('#7A4E2E'))
    x, y = P(15.5, 15); d.rectangle([x - 1, y - 10, x, y], fill=hexc('#5A3A22'))
    bx, by = P(13, 16.5); d.ellipse([bx - 10, by - 3, bx + 10, by + 4], fill=hexc('#7A4A2E')); d.ellipse([bx - 8, by - 3, bx + 8, by + 1], fill=hexc('#A86A44'))
unique('dock', [15, 14, 20, 16], dock, solid=False, act=('호숫가 선착장', '낚시하기'))
# ---- 반복 그림 ----
def tree_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 2, cy - 12, cx + 1, cy], fill=hexc('#6A4A30')); d.rectangle([cx - 2, cy - 12, cx - 1, cy], fill=hexc('#7E5A3A'))
        if kind == 'pine':
            for k, (wd, yy) in enumerate(((11, -12), (9, -20), (7, -28), (4, -35))):
                d.polygon([(cx - wd, cy + yy), (cx, cy + yy - 12), (cx + wd, cy + yy)], fill=hexc('#2E6A44') if k % 2 else hexc('#3A7A4E'))
            return
        r = 11 if kind == 'big' else 9
        g1, g2, g3 = (hexc('#3E7A3A'), hexc('#4E9244'), hexc('#6AAE52')) if kind != 'pink' else (hexc('#C86A8A'), hexc('#E08AA8'), hexc('#F8B8CC'))
        for dx, dy, rr in ((-6, -16, r - 3), (6, -16, r - 3), (0, -24, r - 1), (0, -14, r - 2)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
        for dx, dy, rr in ((-4, -20, r - 5), (4, -22, r - 5), (-1, -27, r - 6)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
        for dx, dy in ((-5, -24), (2, -29), (-2, -21), (5, -25)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=g3)
    return f
for k in ('round', 'big', 'pine', 'pink'): shared('tree_' + k, tree_at(k))
def lamp_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 26, cx, cy], fill=hexc('#2E3A3A')); d.rectangle([cx - 2, cy - 2, cx + 1, cy], fill=hexc('#2E3A3A'))
    d.rectangle([cx - 3, cy - 33, cx + 2, cy - 26], fill=hexc('#2E3A3A')); d.rectangle([cx - 2, cy - 32, cx + 1, cy - 27], fill=hexc('#FFE0A0'))
    d.polygon([(cx - 4, cy - 33), (cx - .5, cy - 37), (cx + 3, cy - 33)], fill=hexc('#2E3A3A'))
shared('lamp', lamp_at)
def bench_at(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x + .1, y + .35), P(x + .9, y + .35)
    poly(d, [up(a, 5), up(b, 5), up((b[0] - 3, b[1] + 2), 5), up((a[0] - 3, a[1] + 2), 5)], hexc('#9A6A44'))
    poly(d, [up(a, 6), up(b, 6), up(b, 11), up(a, 11)], hexc('#8A5A36'))
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 5, p_[0], p_[1]], fill=hexc('#3A2A20'))
shared('bench', bench_at)
def bush_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, r in ((-4, -4, 4), (3, -4, 4), (0, -7, 4)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#3E7A3A'))
    for dx, dy in ((-3, -7), (2, -9), (4, -5)): d.point((cx + dx, cy + dy), fill=hexc('#F2A0C0'))
shared('bush', bush_at)
def rock_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); d.ellipse([cx - 6, cy - 7, cx + 6, cy + 2], fill=hexc('#8A8478')); d.ellipse([cx - 5, cy - 7, cx + 2, cy - 2], fill=hexc('#A8A296'))
shared('rock', rock_at)
def crop_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for dx in (-4, 0, 4):
            d.line([(cx + dx, cy), (cx + dx, cy - 7)], fill=hexc('#3E8A3E'))
            d.ellipse([cx + dx - 2, cy - 10, cx + dx + 2, cy - 6], fill=hexc(kind))
    return f
for c in ('#E05A5A', '#F2D25A', '#C08AFF', '#FF9A4A'): shared('crop' + c, crop_at(c))
def stall_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img)
        Tt, R, B, L = P(x, y), P(x + 2, y), P(x + 2, y + 1), P(x, y + 1)
        poly(d, [L, B, up(B, 8), up(L, 8)], hexc('#7A4A2E')); poly(d, [B, R, up(R, 8), up(B, 8)], hexc('#8A5636')); poly(d, [up(Tt, 8), up(R, 8), up(B, 8), up(L, 8)], hexc('#A86A44'))
        for k, c2 in enumerate(['#E05A5A', '#5AC85A', '#F2D25A', '#C08AFF']):
            xx, yy = P(x + .4 + k * .4, y + .5); d.ellipse([xx - 2, yy - 11, xx + 2, yy - 8], fill=hexc(c2))
        for p_ in (L, B, R): d.line([tuple(map(int, up(p_, 8))), tuple(map(int, up(p_, 22)))], fill=hexc('#5A3A22'))
        a1, a2, a3, a4 = up(Tt, 22), up(R, 22), up(B, 24), up(L, 24)
        poly(d, [a1, a2, a3, a4], hexc(col))
        for k in range(4):
            q = lambda s, e, t: (s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t)
            poly(d, [q(a4, a3, k / 4), q(a4, a3, (k + .5) / 4), q(a1, a2, (k + .5) / 4), q(a1, a2, k / 4)], hexc('#F2EAD8'))
    return f
STALLS = ['#C84A4A', '#4A8AC8', '#E0A030', '#7A5AC8', '#4AA86A']
for c in STALLS: shared('stall' + c, stall_at(c))
def fence_at(r, dn):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 1, cy - 10, cx, cy], fill=hexc('#E8DCC8')); d.rectangle([cx - 1, cy - 10, cx - 1, cy], fill=hexc('#C8B8A0'))
        for dy in (-8, -4):
            if r: d.line([(cx, cy + dy), (cx + 8, cy + dy + 4)], fill=hexc('#E8DCC8'))
            if dn: d.line([(cx, cy + dy), (cx - 8, cy + dy + 4)], fill=hexc('#E8DCC8'))
    return f
for r in (0, 1):
    for dn in (0, 1): shared(f'fence{r}{dn}', fence_at(r, dn))
def sheep_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 6, cy - 8, cx + 5, cy - 1], fill=hexc('#F4F0E8')); d.ellipse([cx + 3, cy - 8, cx + 8, cy - 3], fill=hexc('#3A3040'))
    for dx in (-4, 2): d.rectangle([cx + dx, cy - 2, cx + dx, cy], fill=hexc('#3A3040'))
shared('sheep', sheep_at)
def gate_at(img, x, y):
    d = ImageDraw.Draw(img)
    for xx in (x - 1.4, x + 2.4):
        cx, cy = P(xx, y + .6); d.rectangle([cx - 3, cy - 38, cx + 3, cy], fill=hexc('#8A8070')); d.rectangle([cx - 3, cy - 38, cx, cy], fill=hexc('#A89E8C'))
    a, b = up(P(x - 1.4, y + .6), 38), up(P(x + 2.4, y + .6), 38); d.line([a, b], fill=hexc('#2E3A3A'), width=3)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 6); d.ellipse([m[0] - 6, m[1] - 6, m[0] + 6, m[1] + 6], fill=hexc('#E0C070')); d.ellipse([m[0] - 2, m[1] - 2, m[0] + 2, m[1] + 2], fill=hexc('#4A3E6A'))
shared('gate', gate_at)
# ---- 놓기 ----
occupied = set()
for o in objs:
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def can(x, y, pad=0):
    for dx in range(-pad, pad + 1):
        for dy in range(-pad, pad + 1):
            t = (x + dx, y + dy)
            if t in occupied or T.get(t, 'x') != 'grass': return False
    return True
def put(name, key, x, y, **kw):
    place(name, key, x, y, **kw); occupied.add((x, y))
# 사육장 울타리
FENCE = set()
for x in range(48, 66): FENCE |= {(x, 36), (x, 52)}
for y in range(36, 53): FENCE |= {(48, y), (66, y)}
FENCE -= {(48, 43), (48, 42)}
for (x, y) in sorted(FENCE):
    if (x, y) in occupied: continue
    put('fence', f'fence{int((x + 1, y) in FENCE)}{int((x, y + 1) in FENCE)}', x, y)
for x in range(49, 66):
    for y in range(37, 52): occupied.add((x, y)) if False else None
for (x, y) in [(52, 40), (55, 46), (60, 48), (63, 45), (51, 49)]: put('sheep', 'sheep', x, y, act=('복슬복슬한 구름양', '쓰다듬기'))
# 텃밭 작물
for x in range(56, 66):
    for y in range(23, 30):
        if (x + y) % 2 == 0 and y % 2 == 0: place('crop', 'crop' + ['#E05A5A', '#F2D25A', '#C08AFF', '#FF9A4A'][(x // 3) % 4], x, y, solid=False)
# 시장 가판대 (마을 광장)
for i, (x, y) in enumerate(((26, 54), (26, 57), (31, 58))):
    place('stall', 'stall' + STALLS[i], x, y, w=2, d=1, act=('친구들이 물건을 파는 가판대', '시장 보기')); occupied |= {(x, y), (x + 1, y)}
# 정문
place('gate', 'gate', 37, 64, solid=False)
# 가로등: 큰길·안뜰·상점 거리
LAMPS = [(35, y) for y in range(33, 66, 6)] + [(40, y) for y in range(36, 66, 6)] + [(x, 32) for x in range(18, 62, 7)] + [(x, 47) for x in range(17, 36, 6)] + [(29, 31), (47, 31), (28, 22), (48, 22)]
for (x, y) in LAMPS:
    if (x, y) not in occupied and T.get((x, y)) != 'water': put('lamp', 'lamp', x, y)
# 벤치
for (x, y) in [(34, 37), (41, 38), (29, 38), (22, 25), (21, 30), (44, 46), (12, 23), (27, 52)]:
    if can(x, y): put('bench', 'bench', x, y, act=('나무 벤치', '앉아서 쉬기'))
# 나무: 가장자리 숲(빽빽하게) + 잔디밭에 듬성듬성
for x in range(NX):
    for y in range(NY):
        edge = min(x, y, NX - 1 - x, NY - 1 - y)
        if T[(x, y)] != 'grass' or (x, y) in occupied: continue
        near_lake = ((x + .5 - 13) / 11) ** 2 + ((y + .5 - 13) / 9) ** 2 < 1
        p = .55 if edge < 3 else .2 if edge < 6 or (x < 26 and y < 26 and not near_lake) else .035
        if random.random() < p and can(x, y, 0):
            kind = 'pine' if (x < 26 and y < 26) or edge < 3 and random.random() < .6 else random.choice(['round', 'round', 'big', 'pink'] if y > 40 else ['round', 'big', 'round'])
            put('tree', 'tree_' + kind, x, y)
        elif random.random() < .02 and can(x, y, 0): put('bush', 'bush', x, y)
        elif random.random() < .006 and can(x, y, 0): put('rock', 'rock', x, y)
# ---- 시트로 묶기 ----
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/world_obj.png')
meta = []
for o in objs:
    s = SPR[o['spr']]; sx, sy = pos[o['spr']]
    meta.append(dict(name=o['name'], box=o['box'], sx=sx, sy=sy, sw=s.width, sh=s.height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']))
lights = [dict(p=P(x + .5, y + .5), dy=-30, r=34, c=[255, 210, 140], a=.6, f=1) for (x, y) in LAMPS]
for o in objs:
    if o['door']:
        x, y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(x, y), dy=-20, r=34, c=[255, 200, 120], a=.35, f=0))
lights.append(dict(p=P(53.5, 17), dy=-20, r=60, c=[150, 255, 190], a=.25, f=0))
WATER = [[x, y] for (x, y), t in T.items() if t == 'water']
AREAS = [dict(n='본관', t=[37, 22]), dict(n='기숙사', t=[25, 18]), dict(n='약초 온실', t=[53, 21]), dict(n='천문탑', t=[61, 11]), dict(n='사육장', t=[49, 43]),
         dict(n='상점 거리', t=[25, 49]), dict(n='마을 광장', t=[30, 54]), dict(n='호수', t=[21, 15]), dict(n='텃밭', t=[60, 31]), dict(n='정문', t=[38, 66])]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, water=WATER, areas=AREAS, start=[38, 67]), open('out/world.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sprites', len(keys), 'sheet', sheet.size)
