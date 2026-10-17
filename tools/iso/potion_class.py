# 넓은 마녀 물약 교실 (18x14): 바닥·벽(배경) + 솥·책상 등 스프라이트
import json, math, random
from PIL import Image, ImageDraw
random.seed(8)
NXr, NYr = 18, 14
WALL = 70
W, H = (NXr + NYr) * 8 + 40, (NXr + NYr) * 4 + WALL + 50
OX, OY = NYr * 8 + 20, WALL + 12
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#1A0F12')
bg = Image.new('RGBA', (W, H), hexc('#140D1E')); px = bg.load()
def put(x, y, c):
    if 0 <= int(x) < W and 0 <= int(y) < H: px[int(x), int(y)] = c
def inv(x, y):
    a, b = (x - OX) / 8, (y - OY) / 4; return (a + b) / 2, (b - a) / 2
# 바닥: 짙은 나무판 + 가운데 카펫 + 앞쪽 마법진
WOOD = [hexc('#6E412B'), hexc('#5F3624'), hexc('#7A4A31'), hexc('#663C28')]
for y in range(H):
    for x in range(W):
        fx, fy = inv(x, y)
        if not (0 <= fx < NXr and 0 <= fy < NYr): continue
        band = int(fy * 3); along = fx + (band % 2) * .5
        c = WOOD[(int(along * 1.5) * 3 + band * 7) % 4]
        if (fy * 3) % 1 < .12 or (along * 1.5) % 1 < .06: c = hexc('#3C2116')
        if 7.6 <= fx < 10.4 and 4 <= fy < NYr:          # 가운데 통로 카펫 (보라)
            e = min(fx - 7.6, 10.4 - fx)
            c = hexc('#C49446') if e < .15 else hexc('#5A2A6A') if e > .35 else hexc('#3E1A4A')
            if e > .35 and int(fy * 2) % 3 == 0 and abs(fx - 9) < .2: c = hexc('#C49446')
        k = .78 + .22 * min(1, (fx + fy) / (NXr + NYr) * 1.6)
        if fx < .5 or fy < .5: k *= .75
        px[x, y] = shade(c, k)
# 마법진 (교탁 앞)
for a in range(0, 360, 3):
    for rr in (1.9, 1.5):
        tx, ty = 9 + rr * math.cos(math.radians(a)), 3.2 + rr * .8 * math.sin(math.radians(a))
        put(*P(tx, ty), hexc('#7FE3B0'))
for k in range(6):
    a1, a2 = math.radians(k * 60), math.radians(k * 60 + 120)
    for t in [i / 16 for i in range(17)]:
        tx = 9 + 1.5 * ((1 - t) * math.cos(a1) + t * math.cos(a2)); ty = 3.2 + 1.2 * ((1 - t) * math.sin(a1) + t * math.sin(a2)); put(*P(tx, ty), hexc('#5CC690'))
# 벽
TOP, LEFT, RIGHT = P(0, 0), P(0, NYr), P(NXr, 0)
def wall_px(side, u, v):
    if side == 'L': return LEFT[0] + u, LEFT[1] - u / 2 - v
    return TOP[0] + u, TOP[1] + u / 2 - v
def wall_fill(side, u0, u1, v0, v1, fn):
    for u in range(int(u0), int(u1)):
        for v in range(int(v0), int(v1)):
            c = fn(u, v) if callable(fn) else fn
            if c: put(*wall_px(side, u, v), c)
WAIN, WAIN2, WAINH, MOLD, TRIM = hexc('#4C2B1C'), hexc('#3B2015'), hexc('#5F3826'), hexc('#5C3A22'), hexc('#C49446')
for side, length, dark in (('L', NYr * 8, .86), ('R', NXr * 8, 1.0)):
    def base(u, v, dark=dark):
        if v < 24:
            c = WAIN; pu = u % 16
            if pu in (0, 1) or v in (3, 21): c = WAIN2
            elif pu == 2 or v == 4: c = WAINH
            if v >= 22: c = MOLD
            if v == 23: c = TRIM
            return shade(c, dark)
        if v >= WALL - 4: return shade(MOLD if v < WALL - 1 else TRIM, dark)
        a, b = u % 12, (v - 24) % 14
        c = hexc('#2E2A4A')
        if (a - 6) ** 2 / 9 + (b - 7) ** 2 / 16 < 1 and not ((a - 6) ** 2 / 3 + (b - 7) ** 2 / 7 < 1): c = hexc('#3E3860')
        return shade(c, dark * (.8 + .2 * v / WALL))
    wall_fill(side, 0, length, 0, WALL, base)
for v in range(WALL):
    for d in (-1, 0, 1): put(TOP[0] + d, TOP[1] - v, hexc('#3A2116') if d else hexc('#6A4128'))
def window(side, u0, w=16, v0=28, h=34):
    fr, gl, gl2, gl3 = hexc('#2E1B12'), hexc('#28406E'), hexc('#3D62A0'), hexc('#7FA6E0')
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        cx = w / 2; top = h - cx
        if vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > cx ** 2: return None
        if uu < 2 or uu >= w - 2 or vv < 2 or (vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > (cx - 2) ** 2): return fr
        if uu in (w // 2 - 1, w // 2) or vv in (12, 24): return fr
        g = gl2 if (uu + vv) % 9 == 0 else gl
        if uu < w // 2 and 14 < vv < 22 and uu > 3: g = gl3 if (uu + vv) % 3 == 0 else gl2
        if (uu - 11) ** 2 + (vv - 28) ** 2 < 5: g = hexc('#F2E8B0')      # 보름달
        return g
    wall_fill(side, u0, u0 + w, v0, v0 + h, f)
# 오른쪽 벽(뒤): 창문 - 칠판 - 창문
window('R', 14); window('R', 118)
def board(u, v):
    uu, vv = u - 44, v - 30
    if not (0 <= uu < 60 and 0 <= vv < 32): return None
    if uu < 2 or uu >= 58 or vv < 2 or vv >= 30: return hexc('#6A4A2E')
    if vv in (22, 23) and 6 <= uu < 30 and uu % 3: return hexc('#E8F0E0')
    if vv in (16, 17) and 8 <= uu < 40 and (uu // 2) % 3: return hexc('#E8F0E0')
    if vv in (10, 11) and 6 <= uu < 22 and uu % 2: return hexc('#E8F0E0')
    if (uu - 46) ** 2 + (vv - 16) ** 2 < 60 and (uu - 46) ** 2 + (vv - 16) ** 2 > 40: return hexc('#F2E27A')   # 솥 그림
    if 38 <= uu < 54 and 10 <= vv < 14: return hexc('#F2E27A')
    return hexc('#24443A')
wall_fill('R', 0, NXr * 8, 0, WALL, board)
def potion_shelf(side, u0, v0, w):
    cols = ['#7FE3B0', '#FF7A8A', '#8AB8FF', '#FFD86A', '#C08AFF', '#FF9A4A']
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < 24): return None
        if vv in (0, 1, 12, 13): return hexc('#5C3A22')
        slot = uu // 4
        if uu % 4 == 3: return None
        lv = (vv - 2) if vv < 12 else (vv - 14)
        hgt = 3 + (slot * 7 + vv // 12) % 4
        if lv < 0 or lv >= 8 or lv < 8 - hgt: return None
        c = hexc(cols[(slot + vv // 12 * 2) % len(cols)])
        return shade(c, .7) if uu % 4 == 0 else c
    wall_fill(side, u0, u0 + w, v0, v0 + 24, f)
potion_shelf('R', 108 - 2, 32, 0) ; potion_shelf('R', 34, 30, 8)
# 왼쪽 벽: 책장 두 개 + 재료 서랍장 + 벽난로
BOOK = ['#7A2A30', '#2E5A6E', '#7A6A2A', '#4A2E6A', '#2E6A44', '#8A4A2A', '#5A5A6A', '#6A2A4A']
def shelf(u0, w, h):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 0 <= v < h): return None
        if uu < 2 or uu >= w - 2 or v >= h - 2 or v < 1: return hexc('#3E2216')
        row = (v - 1) % 11
        if row in (0, 1): return hexc('#55311F')
        bi = (uu + (v // 11) * 3) // 3
        c = hexc(BOOK[(bi * 5 + v // 11) % len(BOOK)])
        return shade(c, .7) if uu % 3 == 0 else c
    return f
wall_fill('L', 0, NYr * 8, 0, WALL, shelf(4, 22, 56)); wall_fill('L', 0, NYr * 8, 0, WALL, shelf(82, 22, 56))
def drawers(u, v):
    uu = u - 30
    if not (0 <= uu < 20 and 0 <= v < 40): return None
    if uu in (0, 19) or v in (0, 39) or uu % 5 == 0 or v % 6 == 0: return hexc('#3E2216')
    if uu % 5 == 2 and v % 6 == 3: return hexc('#C49446')
    return hexc('#6A4128') if (uu // 5 + v // 6) % 2 else hexc('#5E3A24')
wall_fill('L', 0, NYr * 8, 0, WALL, drawers)
def fireplace(u, v):
    uu = u - 56
    if not (0 <= uu < 22 and 0 <= v < 34): return None
    if v >= 28: return hexc('#6A6470') if v < 32 else hexc('#8A8490')
    if uu < 3 or uu >= 19: return hexc('#5A5460')
    if v < 3: return hexc('#3A3440')
    if v < 18 and 5 <= uu < 17:
        fl = (uu * 7 + v * 3) % 5
        return hexc('#7AE84A') if v < 6 + fl else hexc('#C8FF8A') if v < 9 + fl // 2 and 8 <= uu < 14 else hexc('#1A1420')
    return hexc('#1A1420')
wall_fill('L', 0, NYr * 8, 0, WALL, fireplace)
for side, u in (('L', 28), ('L', 108), ('R', 38), ('R', 108), ('R', 140)):
    wall_fill(side, u, u + 3, 36, 38, TRIM); wall_fill(side, u + 1, u + 2, 38, 43, hexc('#F2E6C8')); wall_fill(side, u + 1, u + 2, 43, 45, hexc('#FFD27A'))
for x in range(W):
    for y in range(H):
        fx, fy = inv(x, y)
        if 0 <= fx < NXr and 0 <= fy < NYr and (fx < .45 or fy < .45): px[x, y] = shade(px[x, y], .7 + .3 * min(fx, fy) / .45)
bg.save('out/pclass_bg.png')
# ---------------- 스프라이트 ----------------
def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200 for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): add.append((x, y))
    for x, y in add: a[x, y] = c
def box(img, tx, ty, w, dp, h, top, left, right, lift=0):
    d = ImageDraw.Draw(img); T_, R, B, L = P(tx, ty), P(tx + w, ty), P(tx + w, ty + dp), P(tx, ty + dp)
    pl = lambda pts, c: d.polygon([tuple(map(int, p)) for p in pts], fill=c)
    pl([up(L, lift), up(B, lift), up(B, lift + h), up(L, lift + h)], left); pl([up(B, lift), up(R, lift), up(R, lift + h), up(B, lift + h)], right)
    pl([up(T_, lift + h), up(R, lift + h), up(B, lift + h), up(L, lift + h)], top)
SPR, objs = {}, []
def obj(name, tiles, draw, act=None, solid=True, key=None):
    if key and key in SPR: spr, ox, oy = SPR[key]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw(img)
    bb = img.getbbox(); bb = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1); spr = img.crop(bb); outline(spr)
    objs.append(dict(name=name, tiles=tiles, x=bb[0], y=bb[1], img=spr, act=act, solid=solid))
def cauldron(tx, ty, brew, big=False):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = P(tx + .5, ty + .5); s = 1.5 if big else 1
        r = int(9 * s)
        d.ellipse([cx - r, cy - int(10 * s), cx + r, cy + int(4 * s)], fill=hexc('#2A2630')); d.ellipse([cx - r, cy - int(10 * s), cx + r, cy + int(1 * s)], fill=hexc('#3A3644'))
        d.ellipse([cx - r + 2, cy - int(10 * s), cx + r - 2, cy - int(5 * s)], fill=hexc('#46424F'))
        d.ellipse([cx - r + 3, cy - int(10 * s) + 1, cx + r - 3, cy - int(5 * s) - 1], fill=hexc(brew))
        d.ellipse([cx - r + 5, cy - int(10 * s) + 1, cx, cy - int(7 * s)], fill=shade(hexc(brew), 1.35))
        for dx in (-int(4 * s), 0, int(4 * s)): d.polygon([(cx + dx - 2, cy + int(6 * s)), (cx + dx, cy + int(1 * s)), (cx + dx + 2, cy + int(6 * s))], fill=hexc('#FF8A3A'))
        for dx in (-int(6 * s), int(6 * s)): d.rectangle([cx + dx - 1, cy + int(2 * s), cx + dx, cy + int(6 * s)], fill=hexc('#2A2630'))
    return f
BREWS = ['#7FE3B0', '#C08AFF', '#FF8A6A', '#8AB8FF', '#FFD86A', '#FF7AB0', '#7AE84A', '#6AE8E8', '#E8A0FF']
stations = [(x, y) for y in (6, 9, 12) for x in (4, 12, 15)] 
stations = [(4, 6), (12, 6), (15, 6), (4, 9), (12, 9), (15, 9), (4, 12), (12, 12), (15, 12)]
stations = [(3, 6), (6, 6), (12, 6), (15, 6), (3, 10), (6, 10), (12, 10), (15, 10), (6, 13)]
for i, (x, y) in enumerate(stations[:8]):
    obj('cauldron', [(x, y)], cauldron(x, y, BREWS[i]), act=('학생용 솥', '물약 끓이기'))
    # 옆에 작은 재료 탁자
    obj('stand', [(x + 1, y)], (lambda xx, yy, c: lambda img: (box(img, xx + 1.15, yy + .2, .7, .6, 9, hexc('#7A4A2E'), hexc('#4A2A1C'), hexc('#5E3826')),
        ImageDraw.Draw(img).rectangle([P(xx + 1.5, yy + .5)[0] - 2, P(xx + 1.5, yy + .5)[1] - 15, P(xx + 1.5, yy + .5)[0] + 1, P(xx + 1.5, yy + .5)[1] - 9], fill=hexc(c))))(x, y, BREWS[(i + 3) % 9]),
        act=('재료 탁자', '재료함 열기'))
# 선생님 큰 솥 + 교탁
obj('cauldron', [(8, 2), (9, 2), (8, 3), (9, 3)], cauldron(8.5, 2.5, '#5CE6A0', big=True), act=('선생님의 큰 솥', '오늘의 실습 보기'))
obj('lectern', [(12, 2)], lambda img: (box(img, 12.2, 2.2, .6, .6, 14, hexc('#7A4A2E'), hexc('#4A2A1C'), hexc('#5E3826')),
    ImageDraw.Draw(img).polygon([up(P(12.1, 2.1), 16), up(P(12.9, 2.1), 18), up(P(12.9, 2.9), 16), up(P(12.1, 2.9), 14)], fill=hexc('#EADBB0'))), act=('교탁 위 레시피 책', '레시피 노트 보기'))
# 의자 위 검은 고양이
def cat_chair(img):
    box(img, 5.2, 2.2, .7, .7, 7, hexc('#8A3A2E'), hexc('#4A2A1C'), hexc('#5E3826')); box(img, 5.75, 2.2, .15, .7, 16, hexc('#6A2E24'), hexc('#4A2A1C'), hexc('#5E3826'))
    d = ImageDraw.Draw(img); cx, cy = P(5.5, 2.5); cy -= 7
    d.ellipse([cx - 4, cy - 4, cx + 3, cy], fill=hexc('#1E1A24')); d.ellipse([cx + 1, cy - 7, cx + 5, cy - 3], fill=hexc('#1E1A24'))
    d.polygon([(cx + 1, cy - 6), (cx + 2, cy - 9), (cx + 3, cy - 6)], fill=hexc('#1E1A24')); d.polygon([(cx + 3, cy - 6), (cx + 4, cy - 9), (cx + 5, cy - 6)], fill=hexc('#1E1A24'))
    d.point((cx + 2, cy - 5), fill=hexc('#E8E04A')); d.point((cx + 4, cy - 5), fill=hexc('#E8E04A'))
obj('cat', [(5, 2)], cat_chair, act=('교실 고양이 먹물', '쓰다듬기'))
# 재료 통·화분·해골
def barrels(img):
    for tx, ty, col in ((16.3, 2.3, '#7A4A2E'), (16.4, 3.4, '#6E412B')):
        d = ImageDraw.Draw(img); cx, cy = P(tx, ty)
        d.rectangle([cx - 5, cy - 11, cx + 5, cy], fill=hexc(col)); d.ellipse([cx - 5, cy - 2, cx + 5, cy + 2], fill=hexc(col)); d.ellipse([cx - 5, cy - 13, cx + 5, cy - 9], fill=hexc('#9A6A44'))
        for yy in (-8, -3): d.line([(cx - 5, cy + yy), (cx + 5, cy + yy)], fill=hexc('#3E2216'))
        d.ellipse([cx - 3, cy - 12, cx + 3, cy - 10], fill=hexc('#7ACB7A' if ty < 3 else '#C08AFF'))
obj('barrels', [(16, 2), (16, 3)], barrels, act=('재료 통', '재료 꺼내기'))
def plant(tx, ty):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = P(tx + .5, ty + .5)
        d.polygon([(cx - 4, cy - 7), (cx + 4, cy - 7), (cx + 3, cy), (cx - 3, cy)], fill=hexc('#A8563A'))
        for dx, dy, r in ((-4, -14, 4), (3, -15, 4), (0, -19, 4), (-1, -11, 3), (4, -10, 3)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#3E6A4E'))
        for dx, dy in ((-3, -16), (2, -20)): d.point((cx + dx, cy + dy), fill=hexc('#C86AE8'))
    return f
obj('plant', [(0, 13)], plant(0, 13)); obj('plant', [(17, 13)], plant(17, 13))
def skull_stand(img):
    d = ImageDraw.Draw(img); cx, cy = P(1.5, 2.5)
    d.rectangle([cx - 1, cy - 14, cx, cy], fill=hexc('#3E2216')); d.rectangle([cx - 4, cy - 2, cx + 3, cy], fill=hexc('#3E2216'))
    d.ellipse([cx - 4, cy - 22, cx + 4, cy - 14], fill=hexc('#E8E0D0')); d.point((cx - 2, cy - 18), fill=hexc('#1A1218')); d.point((cx + 1, cy - 18), fill=hexc('#1A1218'))
obj('skull', [(1, 2)], skull_stand, act=('해골 선생님', '말 걸기'))
# 공중에 뜬 촛불 (못 지나가는 곳 아님)
FLOAT = [(4, 4), (9, 7), (14, 4), (4, 11), (14, 11), (9, 11.5)]
for (x, y) in FLOAT:
    obj('candle', [(int(x), int(y))], (lambda xx, yy: lambda img: (ImageDraw.Draw(img).rectangle([P(xx + .5, yy + .5)[0] - 1, P(xx + .5, yy + .5)[1] - 52, P(xx + .5, yy + .5)[0], P(xx + .5, yy + .5)[1] - 46], fill=hexc('#F2E6C8')),
        ImageDraw.Draw(img).rectangle([P(xx + .5, yy + .5)[0] - 1, P(xx + .5, yy + .5)[1] - 54, P(xx + .5, yy + .5)[0], P(xx + .5, yy + .5)[1] - 53], fill=hexc('#FFD27A'))))(x, y), solid=False)
sheet_w = sum(o['img'].width + 1 for o in objs); sheet_h = max(o['img'].height for o in objs)
sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0)); sx = 0; meta = []
for o in objs:
    sheet.paste(o['img'], (sx, 0)); xs = [t[0] for t in o['tiles']]; ys = [t[1] for t in o['tiles']]
    meta.append(dict(name=o['name'], box=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], sx=sx, sy=0, sw=o['img'].width, sh=o['img'].height, x=o['x'], y=o['y'], door=None, solid=o['solid'], act=o['act'])); sx += o['img'].width + 1
sheet.save('out/pclass_obj.png')
LIGHTS = [dict(p=P(x + .5, y + .5), dy=-52, r=30, c=[255, 200, 120], a=.55, f=1) for (x, y) in FLOAT]
LIGHTS += [dict(p=P(x + .5, y + .5), dy=-8, r=22, c=[int(BREWS[i][1:3], 16), int(BREWS[i][3:5], 16), int(BREWS[i][5:7], 16)], a=.45, f=1) for i, (x, y) in enumerate(stations[:8])]
LIGHTS += [dict(p=P(9, 3), dy=-14, r=50, c=[90, 255, 160], a=.55, f=1)]
LIGHTS += [dict(p=wall_px('L', 67, 10), dy=0, r=36, c=[130, 255, 90], a=.5, f=1)]
for side, u in (('L', 28), ('L', 108), ('R', 38), ('R', 108), ('R', 140)): x, y = wall_px(side, u + 1, 44); LIGHTS.append(dict(p=(x, y), dy=0, r=18, c=[255, 190, 110], a=.5, f=1))
for u in (22, 126): x, y = wall_px('R', u, 44); LIGHTS.append(dict(p=(x, y), dy=0, r=26, c=[110, 150, 255], a=.3, f=0))
meta.append(dict(name='exit', box=[9, 13, 10, 14], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[9, 13], to='campus', label='호박달 마녀학교', spawn=[19, 25]), solid=False, act=None))
json.dump(dict(W=W, H=H, NX=NXr, NY=NYr, OX=OX, OY=OY, objs=meta, lights=LIGHTS), open('out/pclass.json', 'w'), ensure_ascii=False)
print('ok', len(objs), W, H)
