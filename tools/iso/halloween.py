# 호박달 마녀학교 + 몬스터 마을 (84x72, 늘 밤)
import json, math, random
from PIL import Image, ImageDraw
random.seed(31)
NX, NY = 84, 72
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 200
OX, OY = NY * 8 + 20, 160
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#120A18')
src = open('world.py').read()
exec(src[src.index('def poly(d, pts, c)'):src.index('# 본관 (크게, 탑 두 개)')])
# ---------------- 땅 ----------------
T = {}
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
def ellipse(kind, cx, cy, rx, ry):
    for x in range(NX):
        for y in range(NY):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 < 1: T[(x, y)] = kind
fill('river', 39, 0, 45, 72)
ellipse('lake', 56, 59, 6.5, 5)
fill('bridge', 56, 53, 58, 59)           # 유령 호수 낚시 잔교
# 낚시 연못: 호수·강 말고도 낚시터가 곳곳에 (이름·낚이는 물고기는 index.html FISH_SPOT)
PONDS = [dict(id='pond_n', name='북쪽 연못', cx=26, cy=6, rx=4.5, ry=3), dict(id='pond_ne', name='북동 연못', cx=74, cy=7, rx=3.4, ry=3), dict(id='pond_se', name='남동 연못', cx=75, cy=40, rx=4, ry=3)]
for pd in PONDS: ellipse('lake', pd['cx'], pd['cy'], pd['rx'], pd['ry'])
# 학교 길
fill('stone', 14, 24, 28, 30)            # 본관 앞마당
fill('dirt', 19, 30, 22, 70)             # 학교 남북 길
fill('dirt', 2, 26, 39, 29)              # 학교 동서 길 → 다리1
fill('dirt', 2, 51, 39, 54)              # 아래 동서 길 → 다리2
fill('dirt', 6, 37, 9, 51); fill('dirt', 28, 37, 31, 51)
fill('soil', 2, 56, 15, 69)              # 호박밭
fill('dirt', 19, 63, 39, 68)             # 온실·사육장 앞 넓은 마당: 남북 길에서 두 문까지 곧장 이어져요
# 다리
fill('bridge', 39, 26, 45, 29); fill('bridge', 39, 51, 45, 54)
# 마을
fill('dirt', 45, 26, 84, 29)             # 시장 거리
fill('cobble', 53, 18, 68, 37)           # 마을 광장 · 등불 시장 거리
fill('dirt', 62, 12, 65, 21)             # 저택 가는 길
fill('dirt', 60, 34, 63, 70)             # 광장 → 남쪽
fill('dirt', 63, 46, 71, 49)             # 마녀 오두막 길
fill('dirt', 63, 58, 77, 61)             # 늑대인간 집 길
fill('dirt', 45, 51, 60, 54)             # 다리2 → 마을
fill('grave', 46, 39, 57, 50)            # 묘지
for x in range(NX):
    for y in range(NY): T.setdefault((x, y), 'grass')
GRASS = [hexc('#3E4E3A'), hexc('#36463A'), hexc('#46563E'), hexc('#3A4436')]
bg = Image.new('RGBA', (W, H), hexc('#140E1E')); px = bg.load()
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t == 'dirt':
            c = hexc('#6A5444') if random.random() > .12 else hexc('#5E4A3C')
            if random.random() < .02: c = hexc('#7E6A58')
        elif t in ('stone', 'cobble'):
            s_ = 3 if t == 'cobble' else 2
            bx, by = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
            c = [hexc('#7A7480'), hexc('#6E6876'), hexc('#86808C')][(bx * 5 + by * 3) % 3]
            if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#4E4856')
        elif t == 'river':
            c = hexc('#2A4A5A') if (int(fx * 2) + int(fy * 4)) % 5 else hexc('#3A5E6E')
            if random.random() < .01: c = hexc('#8AC8D8')
            if fx < 39.25 or fx > 44.75: c = hexc('#4A3E36')
        elif t == 'lake':
            c = hexc('#2E5A6A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#4A7A8A')
            if random.random() < .015: c = hexc('#A8E8F0')
        elif t == 'bridge':
            c = hexc('#7A5A3E') if int(fy * 3) % 2 else hexc('#6A4C34')
            if (fy * 3) % 1 < .1: c = hexc('#3A2A1E')
            if 39 <= fx < 45 and ((fy - int(fy)) < .08 and int(fy) in (26, 28) or (fy - int(fy)) > .92 and int(fy) in (26, 28)): c = hexc('#4A3424')
        elif t == 'soil':
            c = hexc('#4A3426') if (fy * 2) % 1 < .5 else hexc('#3E2C20')
        elif t == 'grave':
            c = [hexc('#3A3E34'), hexc('#34382E'), hexc('#42463A')][random.randint(0, 2)]
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .004: c = random.choice([hexc('#C86AE8'), hexc('#E8A050'), hexc('#8AE8C8')])
        px[x, y] = c
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x14, 0x0E, 0x1E): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#3A2A24') if (y // 3) % 2 else hexc('#2E221E')
bg.save('out/hw_bg.png'); print('bg', W, H)
# ---------------- 건물 ----------------
def wins_g(step=16, rows=((14, 18), (44, 14))):
    def f(side, length):
        return [(u, v, 8, hh) for u in range(10, int(length) - 8, step) for v, hh in rows]
    return f
def chimney(x, y, h, rh, col):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = up(P(x, y), h + rh - 6)
        d.rectangle([cx - 4, cy - 16, cx + 4, cy], fill=hexc(col)); d.rectangle([cx - 4, cy - 16, cx, cy], fill=shade(hexc(col), .85)); d.rectangle([cx - 5, cy - 18, cx + 5, cy - 16], fill=hexc('#3A2A2A'))
    return f
def combo(*fs):
    def f(img):
        for g in fs: g(img)
    return f
def turret(tx, ty, height, wall, roof, win='#FFC86A'):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = P(tx, ty)
        d.rectangle([cx - 8, cy - height, cx + 8, cy], fill=hexc(wall)); d.rectangle([cx - 8, cy - height, cx, cy], fill=shade(hexc(wall), .85))
        d.ellipse([cx - 8, cy - 3, cx + 8, cy + 3], fill=shade(hexc(wall), .85))
        for k in range(14, height - 8, 16): d.rectangle([cx - 2, cy - k - 8, cx + 2, cy - k], fill=hexc(win))
        d.rectangle([cx - 10, cy - height - 2, cx + 10, cy - height], fill=shade(hexc(wall), .7))
        d.polygon([(cx - 10, cy - height - 2), (cx, cy - height - 30), (cx + 10, cy - height - 2)], fill=hexc(roof)); d.polygon([(cx - 10, cy - height - 2), (cx, cy - height - 30), (cx, cy - height - 2)], fill=shade(hexc(roof), .75))
        d.rectangle([cx - 1, cy - height - 34, cx, cy - height - 30], fill=hexc('#E0C070'))
    return f
# 본관 (물약 교실)
unique('main', [12, 13, 28, 24], combo(building(12, 13, 28, 24, 72, hexc('#5E586E'), hexc('#3A3448'), hexc('#3A2A5E'), 38, wins_g(rows=((14, 18), (42, 16), (62, 6))), doors=[('L', 58, 14)]), turret(12.4, 23.6, 96, '#5E586E', '#3A2A5E'), turret(27.6, 13.4, 96, '#5E586E', '#3A2A5E')),
       door=dict(tile=[19, 24], to='lab', label='본관 · 물약 교실', spawn=[13, 18]))
unique('candy', [3, 30, 11, 37], combo(building(3, 30, 11, 37, 40, hexc('#8A5A4E'), hexc('#4A2E2A'), hexc('#C8642A'), 22, wins_g(14, ((12, 12),)), doors=[('L', 24, 12)]), chimney(9, 32, 40, 22, '#6A4A42')),
       door=dict(tile=[6, 37], to='candy', label='과자 교실', spawn=[12, 16]))
unique('craft', [26, 30, 34, 37], building(26, 30, 34, 37, 40, hexc('#6A5440'), hexc('#3A2A1E'), hexc('#4A3A5A'), 22, wins_g(14, ((12, 12),)), doors=[('L', 24, 12)]),
       door=dict(tile=[29, 37], to='craft', label='공예 교실', spawn=[12, 16]))
for i, (x0, wall, roof, nm) in enumerate(((3, '#6A5A8A', '#3A2A5E', '마녀 기숙사'), (11, '#5A3A44', '#8A2A3A', '뱀파이어 기숙사'), (19, '#6A5A48', '#4A3A2A', '늑대인간 기숙사'), (27, '#8A98A8', '#5A6A8A', '유령 기숙사'))):
    dk = ('dorm_witch', 'dorm_vamp', 'dorm_wolf', 'dorm_ghost')[i]
    unique('dorm', [x0, 42, x0 + 6, 48], building(x0, 42, x0 + 6, 48, 44, hexc(wall), hexc('#2A2230'), hexc(roof), 26, wins_g(14, ((10, 10), (28, 10))), doors=[('L', 20, 10)]),
           door=dict(tile=[x0 + 2, 48], to=dk, label=nm, spawn=[11, 14]))
def toxic_house(img):
    x0, y0, x1, y1, h = 18, 56, 26, 63, 30
    glass, glass2, fr = hexc('#4A8A6A', 200), hexc('#6AC88A', 220), hexc('#2A2A32')
    def f(u, v):
        if v >= h: return None
        if u % 8 == 0 or v % 10 == 0 or v < 2: return fr
        c = glass if (u + v) % 9 else glass2
        if v < 14 and (u * 3 + v) % 7 < 3: c = hexc('#8AE84A')
        if v < 10 and (u * 5 + v * 3) % 13 == 0: c = hexc('#C86AE8')
        return c
    face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
    d = ImageDraw.Draw(img); Tt, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
    r1, r2 = up(P(x0, (y0 + y1) / 2), h + 18), up(P(x1, (y0 + y1) / 2), h + 18)
    poly(d, [Tt, R, r2, r1], hexc('#3A6A5A', 215)); poly(d, [L, B, r2, r1], hexc('#5A9A7A', 230)); poly(d, [R, B, r2], hexc('#4A8A6A', 220))
    for k in range(0, 9): d.line([up(P(x0 + k, y1), h), up(P(x0 + k, (y0 + y1) / 2), h + 18)], fill=fr)
unique('toxic', [18, 56, 26, 63], toxic_house, door=dict(tile=[22, 63], to='toxic', label='독초 온실', spawn=[17, 21]))
# 사육장 건물: 안에 학생 12명의 우리가 있어요
unique('barn', [29, 57, 36, 63], combo(building(29, 57, 36, 63, 44, hexc('#8A4A3A'), hexc('#4A2A22'), hexc('#5A3A2E'), 26, wins_g(14, ((10, 12), (34, 12))), doors=[('L', 20, 16)])),
       door=dict(tile=[32, 63], to='barn', label='사육장', spawn=[21, 31]))
# 마을: 뱀파이어 저택
unique('manor', [57, 3, 71, 12], building(57, 3, 71, 12, 70, hexc('#3E3446'), hexc('#1E1824'), hexc('#2A1E30'), 40, lambda s, l: [(u, v, 8, 18) for u in range(10, int(l) - 8, 14) for v in (12, 42) if not (s == 'L' and abs(u - 44) < 10)],
       doors=[('L', 48, 14)]), door=dict(tile=[63, 12], to=None, label='뱀파이어 저택'))
objs[-1]['spr']; _m = objs.pop(); del SPR[_m['spr']]
unique('manor', [57, 3, 71, 12], combo(building(57, 3, 71, 12, 70, hexc('#3E3446'), hexc('#1E1824'), hexc('#2A1E30'), 40, lambda s, l: [(u, v, 8, 18) for u in range(10, int(l) - 8, 14) for v in (12, 42) if not (s == 'L' and abs(u - 44) < 10)], doors=[('L', 48, 14)]),
       turret(57.4, 11.6, 100, '#3E3446', '#2A1E30', '#FF5A4A'), turret(70.6, 3.4, 100, '#3E3446', '#2A1E30', '#FF5A4A')), door=dict(tile=[63, 12], to=None, label='뱀파이어 저택'))
# 마녀 오두막 (뾰족 원뿔 지붕)
def witch_hut(img):
    d = ImageDraw.Draw(img); cx, cy = P(73, 46.5)
    d.rectangle([cx - 16, cy - 26, cx + 16, cy], fill=hexc('#5A4A3A')); d.rectangle([cx - 16, cy - 26, cx, cy], fill=hexc('#4E3E30'))
    for k in range(0, 26, 6): d.line([(cx - 16, cy - k), (cx + 16, cy - k)], fill=hexc('#3A2C22'))
    d.rectangle([cx - 5, cy - 16, cx + 1, cy], fill=hexc('#2A1E16')); d.rectangle([cx + 6, cy - 20, cx + 12, cy - 13], fill=hexc('#FFB04A'))
    d.polygon([(cx - 22, cy - 24), (cx + 4, cy - 70), (cx + 22, cy - 24)], fill=hexc('#3A2A5E')); d.polygon([(cx - 22, cy - 24), (cx + 4, cy - 70), (cx - 2, cy - 24)], fill=hexc('#2E2050'))
    d.line([(cx + 4, cy - 70), (cx + 12, cy - 76)], fill=hexc('#3A2A5E'), width=2)
    d.ellipse([cx - 24, cy - 28, cx + 24, cy - 20], outline=hexc('#2E2050'))
unique('witchhut', [71, 45, 75, 49], witch_hut, door=dict(tile=[72, 49], to=None, label='마녀의 오두막'))
# 늑대인간 통나무집
def log_cabin(img):
    x0, y0, x1, y1, h = 76, 55, 82, 60, 28
    def f(u, v):
        if v >= h: return None
        c = hexc('#7A5232') if (v // 4) % 2 else hexc('#6A4428')
        if v % 4 == 0: c = hexc('#4A2E1A')
        return c
    face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
    face(img, x0, y0, x1, y1, 'L', lambda u, v: (hexc('#2A1A10') if v < 18 else None) if 18 <= u < 28 else (hexc('#FFB04A') if 36 <= u < 42 and 10 <= v < 18 else None))
    d = ImageDraw.Draw(img); Tt, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
    r1, r2 = up(P(x0, (y0 + y1) / 2), h + 18), up(P(x1, (y0 + y1) / 2), h + 18)
    poly(d, [Tt, R, r2, r1], hexc('#3A2E22')); poly(d, [L, B, r2, r1], hexc('#5A4632')); poly(d, [R, B, r2], hexc('#4A3A2A'))
    claw = up(P(x1, (y0 + y1) / 2), h + 6)
    for k in range(3): d.line([(claw[0] - 6 + k * 3, claw[1] - 4), (claw[0] - 4 + k * 3, claw[1] + 4)], fill=hexc('#C8B89A'))
unique('cabin', [76, 55, 82, 60], log_cabin, door=dict(tile=[78, 60], to=None, label='늑대인간 통나무집'))
# 상점 (비뚤빼뚤 집)
SHOPS = [('사탕 가게', '#C8786A', '#6A2A4A'), ('가면 가게', '#8A7AA8', '#3A2A5E'), ('호박 빵집', '#C8925A', '#8A3A2A'), ('해골 잡화점', '#9A9A8A', '#3A3A4A'), ('부엉이 우체국', '#7A8A9A', '#2A3A5A'), ('유령 찻집', '#A8B8C8', '#4A5A7A')]
for i, (nm, wl, rf) in enumerate(SHOPS):
    if i < 3: x0, y0 = [46, 68, 75][i], 19
    else: x0, y0 = [46, 68, 75][i - 3], 31
    x1, y1 = x0 + 6, y0 + 6 if i < 3 else y0 + 5
    if i >= 3: y0, y1 = 30, 35
    else: y0, y1 = 19, 25
    bd = building(x0, y0, x1, y1, 38 + (i % 2) * 8, hexc(wl), hexc('#2A2230'), hexc(rf), 24 + (i % 3) * 4, wins_g(18, ((14, 12),)), doors=[('L', 18, 10)])
    unique('shop', [x0, y0, x1, y1], bd, door=dict(tile=[x0 + 2, y1], to=None, label=nm))
# 거대 잭오랜턴 (광장)
def giant_jack(img):
    d = ImageDraw.Draw(img); cx, cy = P(61, 27.5)
    for dx, w in ((-14, 12), (14, 12), (-6, 14), (6, 14), (0, 15)): d.ellipse([cx + dx - w, cy - 34, cx + dx + w, cy + 2], fill=hexc('#E07A1E'))
    for dx in (-14, 14): d.ellipse([cx + dx - 8, cy - 30, cx + dx + 2, cy - 2], fill=hexc('#C8661A'))
    d.rectangle([cx - 2, cy - 42, cx + 3, cy - 33], fill=hexc('#4A6A2A'))
    d.polygon([(cx - 14, cy - 22), (cx - 8, cy - 28), (cx - 4, cy - 20)], fill=hexc('#FFE07A')); d.polygon([(cx + 14, cy - 22), (cx + 8, cy - 28), (cx + 4, cy - 20)], fill=hexc('#FFE07A'))
    d.polygon([(cx - 16, cy - 12), (cx - 8, cy - 8), (cx - 3, cy - 12), (cx + 3, cy - 8), (cx + 8, cy - 12), (cx + 16, cy - 10), (cx + 10, cy - 4), (cx - 10, cy - 4)], fill=hexc('#FFD04A'))
unique('giantjack', [59, 26, 63, 30], giant_jack, act=('광장의 거대 잭오랜턴', '소원 빌기'))
# 바깥 솥 (마녀 오두막 앞)
def cauldron_out(img):
    d = ImageDraw.Draw(img); cx, cy = P(69.5, 47.5)
    d.ellipse([cx - 9, cy - 10, cx + 9, cy + 4], fill=hexc('#2A2630')); d.ellipse([cx - 8, cy - 11, cx + 8, cy - 5], fill=hexc('#7AE84A')); d.ellipse([cx - 5, cy - 10, cx + 2, cy - 7], fill=hexc('#C8FF8A'))
    for dx in (-4, 0, 4): d.polygon([(cx + dx - 2, cy + 6), (cx + dx, cy + 1), (cx + dx + 2, cy + 6)], fill=hexc('#FF8A3A'))
unique('cauldron', [69, 47, 70, 48], cauldron_out, act=('부글부글 마녀의 솥', '들여다보기'))
# ---- 반복 그림 ----
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
        g1, g2, g3 = (hexc('#2E3E36'), hexc('#3A4E40'), hexc('#4E6450')) if kind == 'round' else (hexc('#4A2E4E'), hexc('#5E3A62'), hexc('#7A4E7E'))
        r = 10
        for dx, dy, rr in ((-6, -16, r - 3), (6, -16, r - 3), (0, -24, r - 1), (0, -14, r - 2)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
        for dx, dy, rr in ((-4, -20, r - 5), (4, -22, r - 5), (-1, -27, r - 6)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
        for dx, dy in ((-5, -24), (2, -29), (5, -25)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=g3)
    return f
for k in ('round', 'purple', 'pine', 'dead'): shared('t_' + k, dark_tree(k))
def pumpkin_at(lit):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for dx, w in ((-4, 4), (4, 4), (0, 5)): d.ellipse([cx + dx - w, cy - 9, cx + dx + w, cy], fill=hexc('#E07A1E'))
        d.rectangle([cx - 1, cy - 12, cx, cy - 9], fill=hexc('#4A6A2A'))
        if lit:
            d.polygon([(cx - 5, cy - 6), (cx - 3, cy - 8), (cx - 2, cy - 5)], fill=hexc('#FFE07A')); d.polygon([(cx + 5, cy - 6), (cx + 3, cy - 8), (cx + 2, cy - 5)], fill=hexc('#FFE07A'))
            d.line([(cx - 4, cy - 3), (cx + 4, cy - 3)], fill=hexc('#FFD04A'))
    return f
shared('pumpkin', pumpkin_at(False)); shared('jack', pumpkin_at(True))
def lantern_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 28, cx, cy], fill=hexc('#2A2230')); d.line([(cx, cy - 28), (cx + 6, cy - 30)], fill=hexc('#2A2230'))
    d.ellipse([cx + 3, cy - 30, cx + 10, cy - 22], fill=hexc('#FF9A3A')); d.ellipse([cx + 5, cy - 28, cx + 8, cy - 24], fill=hexc('#FFE08A'))
shared('lantern', lantern_at)
def tomb_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 0:
            d.rectangle([cx - 4, cy - 10, cx + 4, cy], fill=hexc('#8A8A92')); d.ellipse([cx - 4, cy - 14, cx + 4, cy - 6], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 10, cx - 1, cy], fill=hexc('#9A9AA2'))
            d.line([(cx - 2, cy - 9), (cx + 2, cy - 9)], fill=hexc('#5A5A62')); d.line([(cx - 2, cy - 6), (cx + 2, cy - 6)], fill=hexc('#5A5A62'))
        else:
            d.rectangle([cx - 1, cy - 14, cx + 1, cy], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 11, cx + 4, cy - 9], fill=hexc('#8A8A92'))
        d.ellipse([cx - 6, cy - 2, cx + 6, cy + 2], fill=hexc('#2E3228'))
    return f
shared('tomb0', tomb_at(0)); shared('tomb1', tomb_at(1))
def iron_at(r, dn):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 1, cy - 14, cx, cy], fill=hexc('#2A2230')); d.point((cx, cy - 15), fill=hexc('#2A2230'))
        for on, dx in ((r, 8), (dn, -8)):
            if not on: continue
            for k in range(1, 4): xx = cx + dx * k / 4; yy = cy + 4 * k / 4; d.line([(xx, yy), (xx, yy - 11)], fill=hexc('#2A2230'))
            d.line([(cx, cy - 10), (cx + dx, cy - 6)], fill=hexc('#2A2230')); d.line([(cx, cy - 3), (cx + dx, cy + 1)], fill=hexc('#2A2230'))
    return f
for r in (0, 1):
    for dn in (0, 1): shared(f'iron{r}{dn}', iron_at(r, dn))
def scarecrow_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.line([(cx, cy), (cx, cy - 24)], fill=hexc('#6A4A2A'), width=2); d.line([(cx - 9, cy - 18), (cx + 9, cy - 18)], fill=hexc('#6A4A2A'), width=2)
    d.rectangle([cx - 5, cy - 19, cx + 5, cy - 9], fill=hexc('#8A5A3A')); d.ellipse([cx - 5, cy - 30, cx + 5, cy - 20], fill=hexc('#E07A1E'))
    d.polygon([(cx - 8, cy - 28), (cx, cy - 38), (cx + 8, cy - 28)], fill=hexc('#3A2A1E')); d.point((cx - 2, cy - 26), fill=hexc('#FFE07A')); d.point((cx + 2, cy - 26), fill=hexc('#FFE07A'))
shared('scarecrow', scarecrow_at)
def mush_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, r in ((-3, 0, 3), (3, -1, 2), (0, 1, 2)):
        d.rectangle([cx + dx - 1, cy + dy - 3, cx + dx, cy + dy], fill=hexc('#E8E0D0')); d.ellipse([cx + dx - r, cy + dy - 3 - r, cx + dx + r, cy + dy - 3 + r // 2], fill=hexc('#8AE8D8'))
shared('glowmush', mush_at)
def crow_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.line([(cx, cy), (cx, cy - 14)], fill=hexc('#5A4A3A')); d.line([(cx - 5, cy - 14), (cx + 5, cy - 14)], fill=hexc('#5A4A3A'))
    d.ellipse([cx - 3, cy - 20, cx + 3, cy - 14], fill=hexc('#1E1A24')); d.ellipse([cx + 1, cy - 22, cx + 4, cy - 18], fill=hexc('#1E1A24')); d.point((cx + 5, cy - 20), fill=hexc('#E0A030'))
shared('crow', crow_at)
def blackcat_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 5, cy - 5, cx + 3, cy], fill=hexc('#1E1A24')); d.ellipse([cx + 1, cy - 8, cx + 6, cy - 3], fill=hexc('#1E1A24'))
    d.polygon([(cx + 1, cy - 7), (cx + 2, cy - 10), (cx + 3, cy - 7)], fill=hexc('#1E1A24')); d.polygon([(cx + 4, cy - 7), (cx + 5, cy - 10), (cx + 6, cy - 7)], fill=hexc('#1E1A24'))
    d.point((cx + 3, cy - 6), fill=hexc('#E8E04A')); d.point((cx + 5, cy - 6), fill=hexc('#E8E04A')); d.line([(cx - 5, cy - 3), (cx - 8, cy - 8)], fill=hexc('#1E1A24'))
shared('blackcat', blackcat_at)
def bathouse_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 20, cx, cy], fill=hexc('#5A4A3A')); d.rectangle([cx - 6, cy - 32, cx + 6, cy - 20], fill=hexc('#6A4A5A')); d.polygon([(cx - 8, cy - 32), (cx, cy - 40), (cx + 8, cy - 32)], fill=hexc('#3A2A3A'))
    d.ellipse([cx - 2, cy - 29, cx + 2, cy - 25], fill=hexc('#1A1218'))
shared('bathouse', bathouse_at)
def stall_hw(col, fish=False, veg=False):
    def f(img, x, y):
        d = ImageDraw.Draw(img); Tt, R, B, L = P(x, y), P(x + 2, y), P(x + 2, y + 1), P(x, y + 1)
        poly(d, [L, B, up(B, 8), up(L, 8)], hexc('#5A3A2A')); poly(d, [B, R, up(R, 8), up(B, 8)], hexc('#6A4632')); poly(d, [up(Tt, 8), up(R, 8), up(B, 8), up(L, 8)], hexc('#7A5238'))
        if fish:   # 생선 가게: 얼음 상자에 물고기
            ib = [up(P(x + .2, y + .2), 9), up(P(x + 1.8, y + .2), 9), up(P(x + 1.8, y + .8), 9), up(P(x + .2, y + .8), 9)]; poly(d, ib, hexc('#B8E0F0'))
            for k, c2 in enumerate(['#8AA8E0', '#F08A2A', '#C8D8F0', '#E0303A']):
                xx, yy = P(x + .45 + k * .38, y + .5); d.ellipse([xx - 3, yy - 11, xx + 1, yy - 9], fill=hexc(c2)); d.polygon([(xx + 1, yy - 10), (xx + 3, yy - 12), (xx + 3, yy - 8)], fill=hexc(c2)); d.point((xx - 2, yy - 11), fill=OUTL)
        elif veg:   # 채소 가게: 토마토·당근·양배추·비트를 두 줄로 쌓아요
            for row, (dy_, rr) in enumerate(((0, 3), (-3, 2))):
                for k, c2 in enumerate(['#E0303A', '#F08A2A', '#6AC84A', '#9A3AA8', '#E0303A']): xx, yy = P(x + .25 + k * .38, y + .5); d.ellipse([xx - rr, yy - 11 + dy_ - rr + 1, xx + rr, yy - 8 + dy_], fill=hexc(c2)); d.point((xx, yy - 12 + dy_ - rr + 1), fill=hexc('#3A7A2A'))
        else:
            for k, c2 in enumerate(['#E07A1E', '#C86AE8', '#8AE84A', '#F2E8D8']): xx, yy = P(x + .4 + k * .4, y + .5); d.ellipse([xx - 2, yy - 11, xx + 2, yy - 8], fill=hexc(c2))
        for p_ in (L, B, R): d.line([tuple(map(int, up(p_, 8))), tuple(map(int, up(p_, 22)))], fill=hexc('#3A2A1E'))
        a1, a2, a3, a4 = up(Tt, 22), up(R, 22), up(B, 24), up(L, 24); poly(d, [a1, a2, a3, a4], hexc(col))
        q = lambda s, e, t: (s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t)
        for k in range(4): poly(d, [q(a4, a3, k / 4), q(a4, a3, (k + .5) / 4), q(a1, a2, (k + .5) / 4), q(a1, a2, k / 4)], hexc('#2A1E2E'))
    return f
for c in ('#E07A1E', '#7A4AA8', '#4AA86A', '#C8486A'): shared('stall' + c, stall_hw(c))
shared('fishstall', stall_hw('#3A7AC8', True))
shared('vegstall', stall_hw('#3AA84A', False, True))
def game_board(img, x, y):   # 놀이 게시판: 기둥 둘 + 알록달록 쪽지
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx in (-9, 8): d.rectangle([cx + dx, cy - 26, cx + dx + 1, cy], fill=hexc('#3A2A1E'))
    d.rectangle([cx - 12, cy - 30, cx + 12, cy - 14], fill=OUTL); d.rectangle([cx - 11, cy - 29, cx + 11, cy - 15], fill=hexc('#7A5238'))
    for k, (c2, ox, oy) in enumerate((('#FFD866', -9, -27), ('#FF8AB8', -3, -26), ('#8CE6B0', 3, -27), ('#8AB8FF', -7, -21), ('#F2E8D8', 1, -21), ('#C08AFF', 6, -20))): d.rectangle([cx + ox, cy + oy, cx + ox + 4, cy + oy + 4], fill=hexc(c2))
    d.polygon([(cx - 14, cy - 30), (cx, cy - 37), (cx + 14, cy - 30)], fill=hexc('#C8486A')); d.line([(cx - 14, cy - 30), (cx + 14, cy - 30)], fill=OUTL)
shared('gameboard', game_board)
def bench_old(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x + .1, y + .35), P(x + .9, y + .35)
    poly(d, [up(a, 5), up(b, 5), up((b[0] - 3, b[1] + 2), 5), up((a[0] - 3, a[1] + 2), 5)], hexc('#5A4232'))
    poly(d, [up(a, 6), up(b, 6), up(b, 11), up(a, 11)], hexc('#4A3626'))
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 5, p_[0], p_[1]], fill=hexc('#2A2230'))
shared('bench', bench_old)
def bush_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, r in ((-4, -4, 4), (3, -4, 4), (0, -7, 4)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#2E3E30'))
    for dx, dy in ((-3, -7), (2, -9), (4, -5)): d.point((cx + dx, cy + dy), fill=hexc('#C86AE8'))
shared('bush', bush_at)
# 시장 거리 동쪽 끝 문 기둥 둘 (사이로 걸어가면 그림자 골목으로 넘어가요: quarter.py)
def pillar(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 7, cy - 6, cx + 7, cy + 2], fill=hexc('#4E4856')); d.rectangle([cx - 5, cy - 46, cx + 5, cy - 6], fill=hexc('#6E6876')); d.rectangle([cx - 5, cy - 46, cx, cy - 6], fill=hexc('#5E586A'))
    for k in range(-40, -8, 8): d.line([(cx - 5, cy + k), (cx + 5, cy + k)], fill=hexc('#4E4856'))
    d.rectangle([cx - 8, cy - 50, cx + 8, cy - 46], fill=hexc('#4E4856')); d.polygon([(cx - 8, cy - 50), (cx, cy - 58), (cx + 8, cy - 50)], fill=hexc('#3A2A5E'))
    d.line([(cx, cy - 46), (cx, cy - 38)], fill=hexc('#2A2230')); d.ellipse([cx - 4, cy - 38, cx + 4, cy - 28], fill=hexc('#FF9A3A')); d.ellipse([cx - 2, cy - 36, cx + 2, cy - 31], fill=hexc('#FFE08A'))
shared('pillar', pillar)
place('gate', 'pillar', 80, 25); objs[-1]['door'] = dict(tile=[80, 27], to='quarter', spawn=[8, 14], label='그림자 골목', walk=True, span=[26, 28])
place('gate', 'pillar', 80, 29)
# ---------------- 놓기 ----------------
occupied = set()
for o in objs:
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def can(x, y): return (x, y) not in occupied and T.get((x, y)) == 'grass'
def put(name, key, x, y, **kw): place(name, key, x, y, **kw); occupied.add((x, y))
# 호박밭
for x in range(2, 15):
    for y in range(56, 69):
        if (x + y) % 2 == 0 and y % 2 == 0: put('pumpkin', 'jack' if random.random() < .15 else 'pumpkin', x, y, solid=False, act=('잘 익은 호박', '수확하기'))
put('scarecrow', 'scarecrow', 8, 61)
# 사육장 (울타리 + 박쥐집·고양이·까마귀)
FN = set((x, 56) for x in range(28, 38)) | set((x, 68) for x in range(28, 38)) | set((28, y) for y in range(56, 69)) | set((37, y) for y in range(56, 69))
FN -= {(28, 61), (28, 62)}
# 울타리는 걷는 길을 막아서 없앴어요. 두 건물 앞 마당(x 17~38, y 63~69)은 나무도 심지 않아요
occupied |= set((x, y) for x in range(17, 39) for y in range(63, 70))
put('blackcat', 'blackcat', 37, 60, solid=False, act=('사육부 검은 고양이', '쓰다듬기'))
put('crow', 'crow', 37, 58, act=('사육부 까마귀', '모이 주기'))
# 묘지
GF = set((x, 39) for x in range(46, 57)) | set((x, 50) for x in range(46, 57)) | set((46, y) for y in range(39, 51)) | set((56, y) for y in range(39, 51))
GF -= {(51, 50), (52, 50)}
for (x, y) in sorted(GF):
    if (x, y) not in occupied: put('fence', f'iron{int((x + 1, y) in GF)}{int((x, y + 1) in GF)}', x, y)
for x in range(48, 56, 2):
    for y in range(41, 49, 2):
        if random.random() < .8: put('tomb', random.choice(['tomb0', 'tomb0', 'tomb1']), x, y, act=('오래된 묘비', '읽어 보기'))
for (x, y) in [(47, 44), (55, 41), (50, 48)]:
    if (x, y) not in occupied: put('tree', 't_dead', x, y)
# 등불 시장 거리: 친구 가판대 4 + 생선 가게
for i, (x, y) in enumerate(((55, 24), (55, 31), (65, 24), (65, 31))): place('stall', 'stall' + ['#E07A1E', '#7A4AA8', '#4AA86A', '#C8486A'][i], x, y, w=2, act=('등불 시장 가판대', '시장 보기')); occupied |= {(x, y), (x + 1, y)}
place('stall', 'fishstall', 58, 34, w=2, act=('생선 가게', '물고기 팔기')); occupied |= {(58, 34), (59, 34)}
place('stall', 'vegstall', 54, 34, w=2, act=('채소 가게', '채소 팔기')); occupied |= {(54, 34), (55, 34)}   # 온실 수확물을 사 주는 채소 가게
place('board', 'gameboard', 60, 21, act=('놀이 게시판', '놀이 고르기')); occupied.add((60, 21))
# 광장·거리 장식
for (x, y) in [(56, 22), (66, 22), (56, 33), (66, 33), (58, 30), (64, 24)]:
    if (x, y) not in occupied: put('jack', 'jack', x, y, solid=False)
LAMPS = [(x, 25) for x in range(4, 39, 6)] + [(x, 29) for x in range(47, 84, 6)] + [(18, y) for y in range(32, 70, 6)] + [(59, y) for y in range(36, 70, 6)] + [(x, 50) for x in range(4, 39, 7)] + [(61, 14), (61, 18), (13, 23), (28, 23)]
LAMPS = [t for t in LAMPS if t not in occupied and T.get(t) not in ('river', 'lake')]
for (x, y) in LAMPS: put('lantern', 'lantern', x, y)
for (x, y) in [(15, 29), (26, 29), (24, 38), (10, 40), (54, 23), (67, 25), (50, 54), (58, 55)]:
    if can(x, y): put('bench', 'bench', x, y, act=('낡은 벤치', '앉아서 쉬기'))
for (x, y) in [(52, 57), (60, 63), (51, 62), (57, 53), (62, 64)]:
    if can(x, y): put('glowmush', 'glowmush', x, y, solid=False)
# 숲: 가장자리 + 마을 남동쪽은 빽빽
for x in range(NX):
    for y in range(NY):
        if not can(x, y): continue
        edge = min(x, y, NX - 1 - x, NY - 1 - y)
        forest = x > 66 and y > 50
        p = .55 if edge < 3 else .3 if forest else .04
        if random.random() < p:
            kind = random.choice(['pine', 'pine', 'dead', 'round'] if (edge < 3 or forest) else ['round', 'purple', 'dead', 'round'])
            put('tree', 't_' + kind, x, y)
        elif random.random() < .015: put('bush', 'bush', x, y)
        elif random.random() < .006: put('pumpkin', 'jack', x, y, solid=False)
# ---------------- 저장 ----------------
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/hw_obj.png')
meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
lights = [dict(p=P(x + .5, y + .5), dy=-26, r=30, c=[255, 160, 70], a=.6, f=1) for (x, y) in LAMPS]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-6, r=16, c=[255, 170, 60], a=.55, f=1) for o in objs if o['spr'] == 'jack']
for o in objs:
    if o['door']: x, y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(x, y), dy=-18, r=34, c=[255, 180, 90], a=.45, f=0))
lights += [dict(p=P(61, 27.5), dy=-18, r=60, c=[255, 160, 60], a=.6, f=1), dict(p=P(69.5, 47.5), dy=-8, r=30, c=[130, 255, 90], a=.5, f=1), dict(p=P(22, 59.5), dy=-16, r=46, c=[120, 255, 140], a=.3, f=0),
           dict(p=P(56, 59), dy=0, r=70, c=[90, 200, 230], a=.25, f=0)]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-3, r=14, c=[120, 240, 220], a=.5, f=0) for o in objs if o['spr'] == 'glowmush']
lights += [dict(p=P(x + .5, y + .5), dy=-34, r=36, c=[255, 160, 70], a=.6, f=1) for (x, y) in ((80, 25), (80, 29))]
WATER = [[x, y] for (x, y), t in T.items() if t in ('river', 'lake')]
# 채집 지점 후보: 빈 풀밭·묘지 (f 숲, g 묘지, l 호숫가, p 들판)
def zone(x, y):
    if T[(x, y)] == 'grave': return 'g'
    if ((x + .5 - 56) / 9) ** 2 + ((y + .5 - 59) / 7.5) ** 2 < 1: return 'l'
    if (x > 64 and y > 48) or min(x, y, NX - 1 - x, NY - 1 - y) < 5: return 'f'
    return 'p'
FORAGE = [[x, y, zone(x, y)] for x in range(2, NX - 2) for y in range(2, NY - 2) if (x, y) not in occupied and T[(x, y)] in ('grass', 'grave') and (x * 7 + y * 3) % 4 == 0]
AREAS = [dict(n='본관 · 물약 교실', t=[19, 24]), dict(n='과자 교실', t=[6, 37]), dict(n='공예 교실', t=[29, 37]), dict(n='기숙사', t=[16, 48]), dict(n='호박밭', t=[9, 55]), dict(n='독초 온실', t=[22, 63]),
         dict(n='사육장', t=[27, 61]), dict(n='등불 시장', t=[61, 31]), dict(n='채소 가게', t=[54, 35]), dict(n='북쪽 연못', t=[26, 10]), dict(n='북동 연못', t=[74, 11]), dict(n='남동 연못', t=[75, 44]), dict(n='뱀파이어 저택', t=[63, 12]), dict(n='마녀의 오두막', t=[72, 49]), dict(n='묘지', t=[51, 51]), dict(n='유령 호수', t=[56, 53]), dict(n='늑대인간 집', t=[78, 60])]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, water=WATER, ponds=[dict(id=q['id'], name=q['name'], cx=q['cx'], cy=q['cy'], r=max(q['rx'], q['ry']) + 1.5) for q in PONDS], forage=FORAGE, areas=AREAS, start=[20, 30]), open('out/hw.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sheet', sheet.size)
