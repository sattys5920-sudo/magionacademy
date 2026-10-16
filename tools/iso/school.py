# 별빛고등학교 캠퍼스 72x72 (현대 기숙 고등학교)
import json, math, random
from PIL import Image, ImageDraw
random.seed(21)
NX, NY = 72, 72
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 190
OX, OY = NY * 8 + 20, 150
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#1C1420')
src = open('world.py').read()
exec(src[src.index('def poly(d, pts, c)'):src.index('# 본관 (크게, 탑 두 개)')])   # 그리기 도구 재사용 (render, face, unique, shared, place, building, wins)
# ---------------- 땅 ----------------
T = {}
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
def ellipse(kind, cx, cy, rx, ry):
    for x in range(NX):
        for y in range(NY):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 < 1: T[(x, y)] = kind
fill('asphalt', 0, 66, 72, 72)              # 학교 앞 찻길
fill('brick', 30, 50, 47, 65)               # 앞마당
fill('walk', 36, 30, 41, 50)                # 교실동 뒤 → 식당
fill('walk', 4, 30, 68, 33)                 # 뒤쪽 동서 길
fill('walk', 20, 18, 23, 30); fill('walk', 6, 17, 31, 19)   # 기숙사 길
fill('walk', 52, 33, 55, 50); fill('walk', 47, 49, 66, 51)  # 체육관·농구장 길
fill('walk', 56, 18, 59, 30)                # 온실 길
fill('walk', 27, 50, 30, 60); fill('walk', 47, 57, 52, 60)
fill('court', 55, 52, 66, 61)               # 농구장
ellipse('water', 47, 12, 4.2, 3.4)          # 오리 연못
fill('soil', 60, 20, 70, 28)                # 원예부 텃밭
# 운동장: 트랙(타원) + 잔디
for x in range(NX):
    for y in range(NY):
        cx, cy = 15, 46; dx, dy = abs(x + .5 - cx), abs(y + .5 - cy)
        a, r = 6, 9    # 직선 길이 반, 반지름
        d = math.hypot(dx, max(0, dy - a))
        if d < r: T[(x, y)] = 'track' if d > r - 2.2 else 'field'
for x in range(NX):
    for y in range(NY): T.setdefault((x, y), 'grass')
GRASS = [hexc('#6AA852'), hexc('#5E9C48'), hexc('#74B25A'), hexc('#58943F')]
bg = Image.new('RGBA', (W, H), hexc('#2A3A28')); px = bg.load()
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t == 'walk':     # 보도블록 (밝은 회색 네모)
            c = hexc('#D4D0C8') if (int(fx * 2) + int(fy * 2)) % 2 else hexc('#C4C0B8')
            if (fx * 2) % 1 < .08 or (fy * 2) % 1 < .08: c = hexc('#A8A49C')
        elif t == 'brick':  # 붉은 벽돌 마당
            bx, by = int(fx * 3 + (int(fy * 3) % 2) * .5), int(fy * 3)
            c = [hexc('#B86A52'), hexc('#A85E48'), hexc('#C47860')][(bx * 5 + by * 3) % 3]
            if (fx * 3 + (int(fy * 3) % 2) * .5) % 1 < .1 or (fy * 3) % 1 < .12: c = hexc('#8A4E3E')
        elif t == 'asphalt':
            c = hexc('#4A4A52') if random.random() > .05 else hexc('#56565E')
            if 68.8 < fy < 69.2 and int(fx) % 3: c = hexc('#F2E27A')
            if fy < 66.4: c = hexc('#B8B4AC')
        elif t == 'track':
            c = hexc('#C4664E') if random.random() > .06 else hexc('#B45A44')
            cx, cy = 15, 46; d = math.hypot(abs(fx - cx), max(0, abs(fy - cy) - 6))
            if abs(d - 8.0) < .05 or abs(d - 7.3) < .05: c = hexc('#F2EEE6')
        elif t == 'field':
            c = hexc('#5AAE4E') if (int((fy - 37) * 1.2)) % 2 else hexc('#66BA58')
            if abs(fy - 46) < .06 or (abs(fx - 15) < .05 and abs(fy - 46) < 6.5): c = hexc('#F2EEE6')
            if abs(math.hypot(fx - 15, fy - 46) - 2) < .06: c = hexc('#F2EEE6')
        elif t == 'court':
            c = hexc('#3E8A9A'); 
            if 56 <= fx < 65 and 53 <= fy < 60 and not (56.15 < fx < 64.85 and 53.15 < fy < 59.85): c = hexc('#F2EEE6')
            if abs(fy - 56.5) < .08 and 56 <= fx < 65: c = hexc('#F2EEE6')
            if abs(math.hypot(fx - 60.5, fy - 56.5) - 1.5) < .07: c = hexc('#F2EEE6')
        elif t == 'water':
            c = hexc('#4A8AC0') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#66A2D2')
        elif t == 'soil':
            c = hexc('#6A4A30') if (fy * 2) % 1 < .5 else hexc('#5A3E28')
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .006: c = random.choice([hexc('#F2E27A'), hexc('#FFFFFF'), hexc('#F2A0C0')])
        px[x, y] = c
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x2A, 0x3A, 0x28): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#7A7A82') if (y // 3) % 2 else hexc('#6A6A72')
bg.save('out/school_bg.png'); print('bg', W, H)
# ---------------- 현대식 건물 (평평한 지붕) ----------------
def modern(x0, y0, x1, y1, h, wall, band, glass, floors, door=None, roofc='#9A9AA2', clock=False, extras=None, sign=None):
    def draw(img):
        d = ImageDraw.Draw(img)
        fh = h / floors
        def wall_fn(side, dark):
            length = ((x1 - x0) if side == 'L' else (y1 - y0)) * 8
            def f(u, v):
                if v >= h + 3: return None
                c = wall
                fl = int(v // fh); fv = v - fl * fh
                if v >= h: c = shade(band, 1.1)                     # 옥상 난간
                elif fv < 2: c = band                               # 층마다 띠
                elif 5 <= fv < fh - 3 and 4 <= (u % 14) < 12 and 6 < u < length - 6:   # 창문
                    uu = u % 14
                    lit = (u // 14 + fl * 3) % 5 == 0
                    c = hexc('#FFE6A0') if lit else glass
                    if uu in (4, 11) or fv in (5,) : c = hexc('#F2F2EE')
                    elif uu == 8: c = hexc('#E8E8E4')
                    elif not lit and (uu + int(fv)) % 6 == 0: c = shade(glass, 1.25)
                if door and side == door[0]:
                    du, dw = door[1], door[2]
                    if du <= u < du + dw and v < 24:
                        c = hexc('#8AB8D8') if 2 <= u - du < dw - 2 and v < 22 else hexc('#5A6A7A')
                        if u - du == dw // 2: c = hexc('#5A6A7A')
                    if du - 4 <= u < du + dw + 4 and 24 <= v < 28: c = hexc('#E8E4DC')   # 차양
                return shade(c, dark)
            return f
        face(img, x0, y0, x1, y1, 'L', wall_fn('L', .92)); face(img, x0, y0, x1, y1, 'R', wall_fn('R', 1.0))
        Tt, R, B, L = [up(p, h + 3) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
        poly(d, [Tt, R, B, L], hexc(roofc))
        Ti, Ri, Bi, Li = [up(p, h + 1) for p in (P(x0 + .3, y0 + .3), P(x1 - .3, y0 + .3), P(x1 - .3, y1 - .3), P(x0 + .3, y1 - .3))]
        poly(d, [Ti, Ri, Bi, Li], shade(hexc(roofc), .85))
        if extras: extras(img, d, h)
        if clock:
            cx_, cy_ = up(P((x0 + x1) / 2, y1), h + 14)
            d.rectangle([cx_ - 12, cy_ - 14, cx_ + 12, cy_ + 16], fill=wall); d.rectangle([cx_ - 12, cy_ - 14, cx_ - 1, cy_ + 16], fill=shade(wall, .92))
            d.rectangle([cx_ - 12, cy_ - 16, cx_ + 12, cy_ - 14], fill=band)
            d.ellipse([cx_ - 8, cy_ - 8, cx_ + 8, cy_ + 8], fill=hexc('#F8F6EE')); d.ellipse([cx_ - 8, cy_ - 8, cx_ + 8, cy_ + 8], outline=band)
            d.line([(cx_, cy_), (cx_, cy_ - 6)], fill=hexc('#2A2A3A')); d.line([(cx_, cy_), (cx_ + 4, cy_ + 1)], fill=hexc('#2A2A3A'))
        if sign:
            sx_, sy_ = up(P(sign[0], y1), sign[1])
            d.rectangle([sx_ - 18, sy_ - 4, sx_ + 18, sy_ + 4], fill=hexc(sign[2])); d.rectangle([sx_ - 16, sy_ - 2, sx_ + 16, sy_ + 2], fill=hexc('#F8F6EE'))
    return draw
def rooftop(units):
    def f(img, d, h):
        for (tx, ty, kind) in units:
            cx_, cy_ = up(P(tx, ty), h + 1)
            if kind == 'tank':
                d.rectangle([cx_ - 5, cy_ - 14, cx_ + 5, cy_], fill=hexc('#5A8AB0')); d.ellipse([cx_ - 5, cy_ - 17, cx_ + 5, cy_ - 11], fill=hexc('#7AA8CC'))
                for k in (-4, 3): d.line([(cx_ + k, cy_), (cx_ + k, cy_ + 3)], fill=hexc('#3A3A42'))
            else:
                d.rectangle([cx_ - 6, cy_ - 7, cx_ + 6, cy_], fill=hexc('#C8C8CC')); d.ellipse([cx_ - 3, cy_ - 6, cx_ + 3, cy_ - 1], fill=hexc('#8A8A92'))
    return f
# 교실동 (4층, 시계, 정문)
unique('main', [26, 38, 50, 48], modern(26, 38, 50, 48, 76, hexc('#F2EEE4'), hexc('#5A7AB0'), hexc('#7AA8D8'), 4, door=('L', 88, 16), clock=True,
       extras=rooftop([(30, 41, 'tank'), (45, 41, 'unit'), (47, 44, 'unit')])), door=dict(tile=[37, 48], to='lab', label='교실동 · 과학실', spawn=[4, 7]))
# 체육관 (둥근 지붕)
def gym(img):
    x0, y0, x1, y1, h, rh = 55, 35, 67, 47, 30, 16
    def f(side, dark):
        def g(u, v):
            if v >= h: return None
            c = hexc('#D8D4CC') if v > 6 else hexc('#A8A49C')
            if 12 <= v < 22 and u % 12 < 8 and 4 < u: c = hexc('#9AC4E0')
            if side == 'L' and 40 <= u < 56 and v < 22: c = hexc('#6A7A8A') if (u - 40) not in (0, 15) else hexc('#4A5A6A')
            return shade(c, dark)
        return g
    face(img, x0, y0, x1, y1, 'L', f('L', .92)); face(img, x0, y0, x1, y1, 'R', f('R', 1))
    d = ImageDraw.Draw(img); n = 16
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        ya, yb = y0 + (y1 - y0) * t0, y0 + (y1 - y0) * t1
        za, zb = h + rh * math.sin(math.pi * t0), h + rh * math.sin(math.pi * t1)
        col = shade(hexc('#4A8A9A'), .75 + .35 * t1 if t1 > .5 else .75)
        poly(d, [up(P(x0, ya), za), up(P(x1, ya), za), up(P(x1, yb), zb), up(P(x0, yb), zb)], col)
        if k % 2 == 0: d.line([tuple(map(int, up(P(x0, yb), zb))), tuple(map(int, up(P(x1, yb), zb)))], fill=shade(hexc('#4A8A9A'), .6))
    # 옆면(반원) 채우기
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        ya, yb = y0 + (y1 - y0) * t0, y0 + (y1 - y0) * t1
        poly(d, [up(P(x1, ya), h), up(P(x1, ya), h + rh * math.sin(math.pi * t0)), up(P(x1, yb), h + rh * math.sin(math.pi * t1)), up(P(x1, yb), h)], hexc('#E4E0D8'))
unique('gym', [55, 35, 67, 47], gym, door=dict(tile=[61, 47], to=None, label='체육관'))
# 기숙사 A동, B동 (벽돌, 5층)
for i, (x0, nm) in enumerate(((5, '기숙사 A동'), (21, '기숙사 B동'))):
    unique('dorm', [x0, 6, x0 + 9, 16], modern(x0, 6, x0 + 9, 16, 80, hexc('#B8705A'), hexc('#E8E0D4'), hexc('#8AB0D0'), 5, door=('L', 28, 14), roofc='#8A8A92',
           extras=rooftop([(x0 + 2, 8, 'tank')])), door=dict(tile=[x0 + 4, 16], to=None, label=nm))
# 학생식당·매점
unique('cafe', [33, 21, 45, 29], modern(33, 21, 45, 29, 34, hexc('#F4E8D0'), hexc('#E0904A'), hexc('#9AC8E0'), 2, door=('L', 40, 16), roofc='#A8A8AE', sign=(39, 30, '#E0904A')), door=dict(tile=[38, 29], to=None, label='학생식당 · 매점'))
# 원예부 온실 (유리)
def greenhouse(img):
    x0, y0, x1, y1, h = 52, 8, 60, 16, 30
    glass, glass2, fr = hexc('#A8E0E8', 205), hexc('#D8F4F8', 225), hexc('#F2F2EE')
    def f(u, v):
        if v >= h: return None
        if u % 8 == 0 or v % 10 == 0 or v < 2: return fr
        c = glass if (u + v) % 9 else glass2
        if v < 12 and (u * 3 + v) % 7 < 3: c = hexc('#5EAE5A')
        if v < 10 and (u * 5 + v * 3) % 13 == 0: c = hexc('#F2A0C0')
        return c
    face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
    d = ImageDraw.Draw(img); Tt, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
    r1, r2 = up(P(x0, (y0 + y1) / 2), h + 18), up(P(x1, (y0 + y1) / 2), h + 18)
    poly(d, [Tt, R, r2, r1], hexc('#B8E8F0', 215)); poly(d, [L, B, r2, r1], hexc('#D0F2F6', 230)); poly(d, [R, B, r2], hexc('#C0ECF2', 220))
    for k in range(0, 9): d.line([up(P(x0 + k, y1), h), up(P(x0 + k, (y0 + y1) / 2), h + 18)], fill=fr)
    face(img, x0, y0, x1, y1, 'L', lambda u, v: hexc('#7A8A7A') if 0 <= u - 28 < 10 and v < 20 and (u - 28) not in (0, 9) else None)
unique('greenhouse', [52, 8, 60, 16], greenhouse, door=dict(tile=[56, 16], to=None, label='원예부 온실'))
# 사육부: 토끼장 + 닭장 (나무 우리, 철망)
def hutch(x0, y0, x1, y1, roof):
    def draw(img):
        d = ImageDraw.Draw(img)
        def f(u, v):
            if v >= 16: return None
            if v < 3 or v >= 14 or u % 10 < 2: return hexc('#9A6A44')
            return hexc('#C8C8C0') if (u + v) % 3 == 0 else None
        face(img, x0, y0, x1, y1, 'L', f); face(img, x0, y0, x1, y1, 'R', f)
        Tt, R, B, L = [up(p, 16) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
        r1, r2 = up(P(x0, (y0 + y1) / 2), 24), up(P(x1, (y0 + y1) / 2), 24)
        poly(d, [Tt, R, r2, r1], shade(hexc(roof), .75)); poly(d, [L, B, r2, r1], hexc(roof)); poly(d, [R, B, r2], shade(hexc(roof), .88))
    return draw
unique('hutch', [62, 9, 67, 13], hutch(62, 9, 67, 13, '#C85A3A'), act=('토끼장', '토끼 돌보기'))
unique('coop', [62, 15, 66, 18], hutch(62, 15, 66, 18, '#5A7AB0'), act=('닭장', '달걀 꺼내기'))
# ---- 반복 그림 ----
src2 = src[src.index('def tree_at(kind):'):src.index("shared('lamp', lamp_at)")]
exec(src2)
for k in ('round', 'big', 'pine', 'pink'): shared('tree_' + k, tree_at(k))
def lamp_at(img, x, y):   # 현대식 가로등
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 30, cx, cy], fill=hexc('#5A5A62')); d.rectangle([cx - 2, cy - 2, cx + 1, cy], fill=hexc('#5A5A62'))
    d.rectangle([cx, cy - 31, cx + 6, cy - 29], fill=hexc('#5A5A62')); d.rectangle([cx + 3, cy - 29, cx + 7, cy - 28], fill=hexc('#FFF2C0'))
shared('lamp', lamp_at)
exec(src[src.index('def bench_at(img, x, y):'):src.index("def crop_at(kind):")])
exec(src[src.index('def crop_at(kind):'):src.index("def stall_at(col):")])
def vend_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 5, cy - 22, cx + 5, cy], fill=hexc(col)); d.rectangle([cx - 5, cy - 22, cx, cy], fill=shade(hexc(col), .85))
        d.rectangle([cx - 3, cy - 19, cx + 3, cy - 9], fill=hexc('#E8F4FF'))
        for k in range(3): d.rectangle([cx - 3 + k * 2, cy - 18, cx - 2 + k * 2, cy - 15], fill=hexc(['#E05A5A', '#5AC85A', '#F2D25A'][k]))
        d.rectangle([cx - 3, cy - 6, cx + 3, cy - 3], fill=hexc('#3A3A42'))
    return f
shared('vend_r', vend_at('#D84A4A')); shared('vend_b', vend_at('#4A7AC8'))
def bike_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for k, col in enumerate(['#4A8AC8', '#E05A5A', '#4AA86A']):
        bx = cx - 6 + k * 5; d.ellipse([bx - 3, cy - 5 - k, bx, cy - 2 - k], outline=hexc('#2A2A2A')); d.ellipse([bx + 2, cy - 4 - k, bx + 5, cy - 1 - k], outline=hexc('#2A2A2A'))
        d.line([(bx - 1, cy - 4 - k), (bx + 3, cy - 3 - k)], fill=hexc(col))
shared('bikes', bike_at)
def flag_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 4, cy - 2, cx + 3, cy + 1], fill=hexc('#B8B4AC')); d.rectangle([cx - 1, cy - 50, cx, cy], fill=hexc('#C8C8CC'))
    d.rectangle([cx + 1, cy - 50, cx + 14, cy - 42], fill=hexc('#F8F6EE')); d.ellipse([cx + 5, cy - 48, cx + 10, cy - 44], fill=hexc('#5A7AB0'))
shared('flag', flag_at)
def stone_at(img, x, y):   # 학교 표지석
    d = ImageDraw.Draw(img); cx, cy = P(x + 1, y + .5)
    d.polygon([(cx - 14, cy), (cx - 12, cy - 16), (cx + 10, cy - 18), (cx + 14, cy - 2)], fill=hexc('#9A968C'))
    d.polygon([(cx - 12, cy - 16), (cx + 10, cy - 18), (cx + 8, cy - 20), (cx - 10, cy - 19)], fill=hexc('#B8B4AC'))
    d.rectangle([cx - 8, cy - 13, cx + 7, cy - 6], fill=hexc('#5A5A62')); d.line([(cx - 6, cy - 10), (cx + 5, cy - 10)], fill=hexc('#E0C070'))
shared('stone', stone_at)
def goal_at(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x, y + .5), P(x + 3, y + .5)
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 14, p_[0], p_[1]], fill=hexc('#F2F2EE'))
    d.line([up(a, 14), up(b, 14)], fill=hexc('#F2F2EE'))
    for k in range(1, 6): q = (a[0] + (b[0] - a[0]) * k / 6, a[1] + (b[1] - a[1]) * k / 6); d.line([up(q, 14), (q[0] - 3, q[1] - 2)], fill=hexc('#D8D8D8'))
shared('goal', goal_at)
def hoop_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 30, cx, cy], fill=hexc('#5A5A62')); d.rectangle([cx - 7, cy - 38, cx + 7, cy - 28], fill=hexc('#F2F2EE')); d.rectangle([cx - 3, cy - 35, cx + 3, cy - 31], outline=hexc('#E05A3A'))
    d.ellipse([cx - 4, cy - 29, cx + 4, cy - 26], outline=hexc('#E05A3A'))
shared('hoop', hoop_at)
def busstop_at(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x, y + .3), P(x + 3, y + .3)
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 24, p_[0], p_[1]], fill=hexc('#5A5A62'))
    poly(d, [up(a, 24), up(b, 24), up((b[0] - 6, b[1] + 3), 22), up((a[0] - 6, a[1] + 3), 22)], hexc('#4A7AC8'))
    poly(d, [up(a, 4), up(b, 4), up(b, 20), up(a, 20)], hexc('#BFE2F0', 160))
    d.rectangle([b[0] + 3, b[1] - 30, b[0] + 9, b[1] - 24], fill=hexc('#4A7AC8')); d.rectangle([b[0] + 5, b[1] - 24, b[0] + 6, b[1]], fill=hexc('#5A5A62'))
shared('busstop', busstop_at)
def wall_at(r, dn):     # 학교 담장 (낮은 벽 + 철망)
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for (on, dx, dy) in ((r, 8, 4), (dn, -8, 4)):
            if not on: continue
            poly(d, [(cx, cy), (cx + dx, cy + dy), (cx + dx, cy + dy - 6), (cx, cy - 6)], hexc('#C8C4BC'))
            poly(d, [(cx, cy - 6), (cx + dx, cy + dy - 6), (cx + dx, cy + dy - 7), (cx, cy - 7)], hexc('#E0DCD4'))
            for k in range(0, 9, 2): d.line([(cx + dx * k / 8, cy + dy * k / 8 - 7), (cx + dx * k / 8, cy + dy * k / 8 - 14)], fill=hexc('#5A6A5A'))
            d.line([(cx, cy - 14), (cx + dx, cy + dy - 14)], fill=hexc('#5A6A5A'))
        d.rectangle([cx - 1, cy - 9, cx + 1, cy], fill=hexc('#B8B4AC'))
    return f
for r in (0, 1):
    for dn in (0, 1): shared(f'wall{r}{dn}', wall_at(r, dn))
def gatepost_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 4, cy - 26, cx + 4, cy], fill=hexc('#B8B4AC')); d.rectangle([cx - 4, cy - 26, cx, cy], fill=hexc('#C8C4BC')); d.rectangle([cx - 5, cy - 28, cx + 5, cy - 26], fill=hexc('#8A867E'))
    d.rectangle([cx - 2, cy - 22, cx + 2, cy - 14], fill=hexc('#E0C070'))
shared('gatepost', gatepost_at)
def animal_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 'rabbit':
            d.ellipse([cx - 4, cy - 5, cx + 3, cy], fill=hexc('#F4F0E8')); d.ellipse([cx + 1, cy - 7, cx + 5, cy - 3], fill=hexc('#F4F0E8'))
            d.line([(cx + 2, cy - 10), (cx + 2, cy - 7)], fill=hexc('#F4F0E8')); d.line([(cx + 4, cy - 10), (cx + 4, cy - 7)], fill=hexc('#F4F0E8')); d.point((cx + 4, cy - 5), fill=hexc('#2A2030'))
        elif kind == 'chick':
            d.ellipse([cx - 4, cy - 6, cx + 3, cy], fill=hexc('#F8F4EC')); d.ellipse([cx + 1, cy - 9, cx + 5, cy - 5], fill=hexc('#F8F4EC')); d.point((cx + 5, cy - 7), fill=hexc('#F2A030')); d.point((cx + 3, cy - 10), fill=hexc('#E04A3A'))
        elif kind == 'duck':
            d.ellipse([cx - 5, cy - 4, cx + 3, cy + 1], fill=hexc('#F8F4EC')); d.ellipse([cx + 1, cy - 7, cx + 5, cy - 3], fill=hexc('#3E8A4E')); d.point((cx + 6, cy - 5), fill=hexc('#F2A030'))
        else:  # 학교 고양이
            d.ellipse([cx - 5, cy - 5, cx + 3, cy], fill=hexc('#E8A050')); d.ellipse([cx + 1, cy - 8, cx + 6, cy - 3], fill=hexc('#E8A050'))
            d.polygon([(cx + 1, cy - 7), (cx + 2, cy - 10), (cx + 3, cy - 7)], fill=hexc('#E8A050')); d.polygon([(cx + 4, cy - 7), (cx + 5, cy - 10), (cx + 6, cy - 7)], fill=hexc('#E8A050'))
            d.line([(cx - 5, cy - 3), (cx - 8, cy - 7)], fill=hexc('#E8A050'))
    return f
for k in ('rabbit', 'chick', 'duck', 'cat'): shared(k, animal_at(k))
def table_at(img, x, y):   # 야외 테이블 + 파라솔
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 7, cy - 9, cx + 7, cy - 5], fill=hexc('#F2F2EE')); d.rectangle([cx - 1, cy - 8, cx, cy], fill=hexc('#8A8A92'))
    d.rectangle([cx, cy - 28, cx + 1, cy - 8], fill=hexc('#8A8A92')); d.polygon([(cx - 12, cy - 22), (cx, cy - 30), (cx + 13, cy - 22)], fill=hexc('#E0904A'))
    d.polygon([(cx - 4, cy - 23), (cx, cy - 30), (cx + 4, cy - 23)], fill=hexc('#F8F6EE'))
shared('ptable', table_at)
def planter_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    poly(d, [(cx - 8, cy - 4), (cx, cy - 8), (cx + 8, cy - 4), (cx, cy)], hexc('#5E9C48'))
    poly(d, [(cx - 8, cy - 4), (cx, cy), (cx, cy + 4), (cx - 8, cy)], hexc('#A8A49C')); poly(d, [(cx, cy), (cx + 8, cy - 4), (cx + 8, cy), (cx, cy + 4)], hexc('#C4C0B8'))
    for dx, dy, c in ((-4, -6, '#F2A0C0'), (1, -8, '#F2E27A'), (4, -5, '#E05A5A'), (-1, -4, '#FFFFFF')): d.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=hexc(c))
shared('planter', planter_at)
# ---------------- 놓기 ----------------
occupied = set()
for o in objs:
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def can(x, y):
    return (x, y) not in occupied and T.get((x, y)) == 'grass'
def put(name, key, x, y, **kw):
    place(name, key, x, y, **kw); occupied.add((x, y))
# 담장: 앞쪽(y=64)과 양옆, 정문 틈
WALL = set((x, 64) for x in range(0, 72) if not 35 <= x <= 41) | set((0, y) for y in range(20, 65)) | set((71, y) for y in range(20, 65))
for (x, y) in sorted(WALL):
    if (x, y) in occupied: continue
    put('wall', f'wall{int((x + 1, y) in WALL)}{int((x, y + 1) in WALL)}', x, y)
put('gatepost', 'gatepost', 34, 64); put('gatepost', 'gatepost', 42, 64)
place('busstop', 'busstop', 45, 66, w=3, solid=False, act=('버스 정류장', '시내로 가기'))
put('stone', 'stone', 31, 61, act=('별빛고등학교', '학교 소개 보기'))
put('flag', 'flag', 44, 53)
for (x, y) in [(36, 52), (40, 52), (36, 56), (40, 56), (36, 60), (40, 60), (31, 52), (45, 52), (31, 57), (45, 58)]:
    if (x, y) not in occupied: put('planter', 'planter', x, y)
for (x, y) in [(35, 50), (41, 50), (35, 54), (41, 54), (35, 58), (41, 58), (35, 62), (41, 62)]:
    if (x, y) not in occupied: put('tree', 'tree_pink', x, y)
put('vend', 'vend_r', 47, 30, act=('자판기', '음료 뽑기')); put('vend', 'vend_b', 48, 30, act=('자판기', '음료 뽑기'))
put('bikes', 'bikes', 24, 50); put('bikes', 'bikes', 24, 52)
for (x, y) in [(40, 31), (34, 31), (31, 33), (29, 33)]: pass
for (x, y) in [(34, 30), (43, 30), (46, 31)]:
    if (x, y) not in occupied: put('ptable', 'ptable', x, y, act=('야외 테이블', '앉아서 쉬기'))
put('goal', 'goal', 13, 36, w=3, solid=False); put('goal', 'goal', 13, 55, w=3, solid=False)
put('hoop', 'hoop', 60, 52); put('hoop', 'hoop', 60, 60)
for (x, y, k) in [(63, 11, 'rabbit'), (65, 10, 'rabbit'), (63, 16, 'chick'), (64, 17, 'chick'), (46, 11, 'duck'), (48, 13, 'duck'), (44, 52, 'cat')]:
    place(k, k, x, y, solid=False, act={'rabbit': ('사육부 토끼', '쓰다듬기'), 'chick': ('사육부 닭', '모이 주기'), 'duck': ('연못 오리', '빵 던져 주기'), 'cat': ('학교 고양이 치즈', '쓰다듬기')}[k])
for x in range(60, 70):
    for y in range(20, 28):
        if (x + y) % 2 == 0 and y % 2 == 0: place('crop', 'crop' + ['#E05A5A', '#F2D25A', '#C08AFF', '#FF9A4A'][(x // 3) % 4], x, y, solid=False)
LAMPS = [(34, y) for y in range(51, 64, 4)] + [(42, y) for y in range(51, 64, 4)] + [(x, 29) for x in range(8, 68, 8)] + [(51, y) for y in range(34, 50, 5)] + [(x, 19) for x in range(8, 32, 8)]
LAMPS = [t for t in LAMPS if t not in occupied]
for (x, y) in LAMPS: put('lamp', 'lamp', x, y)
for (x, y) in [(28, 34), (44, 34), (25, 22), (14, 20), (50, 20), (29, 50), (46, 46), (8, 32), (26, 44)]:
    if can(x, y): put('bench', 'bench', x, y, act=('벤치', '앉아서 쉬기'))
for x in range(NX):
    for y in range(NY):
        if not can(x, y): continue
        edge = min(x, y, NX - 1 - x)
        p = .5 if edge < 3 and y < 64 else .025 if y < 64 else 0
        if y >= 64: continue
        if random.random() < p: put('tree', 'tree_' + random.choice(['round', 'big', 'round', 'pine'] if edge < 3 else ['round', 'big', 'pink']), x, y)
        elif random.random() < .015: put('bush', 'bush', x, y)
# ---------------- 저장 ----------------
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/school_obj.png')
meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
lights = [dict(p=P(x + .5, y + .5), dy=-29, r=34, c=[255, 236, 190], a=.55, f=0) for (x, y) in LAMPS]
for o in objs:
    if o['door']: x, y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(x, y), dy=-18, r=36, c=[255, 220, 160], a=.4, f=0))
WATER = [[x, y] for (x, y), t in T.items() if t == 'water']
AREAS = [dict(n='교실동', t=[37, 48]), dict(n='기숙사 A동', t=[9, 16]), dict(n='기숙사 B동', t=[25, 16]), dict(n='학생식당', t=[38, 29]), dict(n='체육관', t=[61, 47]),
         dict(n='운동장', t=[15, 46]), dict(n='농구장', t=[56, 51]), dict(n='원예부 온실', t=[56, 16]), dict(n='사육장', t=[61, 13]), dict(n='연못', t=[47, 16]), dict(n='정문', t=[38, 65])]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, water=WATER, areas=AREAS, start=[38, 67]), open('out/school.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sheet', sheet.size)
