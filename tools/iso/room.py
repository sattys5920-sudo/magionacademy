# 아이소메트릭 물약 연구실 시안: 바닥·벽(배경), 가구(깊이 정렬용 스프라이트), 캐릭터 시트
import json, math, random
from PIL import Image, ImageDraw
random.seed(3)
W, H = 195, 184
N = 10                       # 방 크기 (타일)
OX, OY = 97, 66              # 타일 (0,0) 윗꼭짓점
WALL = 62                    # 벽 높이
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def mix(c, d, t): return tuple(int(c[i] + (d[i] - c[i]) * t) for i in range(3)) + (255,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
OUT = hexc('#140D1E'); OUTL = hexc('#1A0F12')
bg = Image.new('RGBA', (W, H), OUT); px = bg.load()
def put(img, x, y, c):
    x, y = int(x), int(y)
    if 0 <= x < img.width and 0 <= y < img.height: img.load()[x, y] = c
# ---------- 바닥: 헤링본 느낌 나무판 ----------
WOOD = [hexc('#6E412B'), hexc('#5F3624'), hexc('#7A4A31'), hexc('#663C28')]
SEAM = hexc('#3C2116')
for y in range(H):
    for x in range(W):
        fx = ((x - OX) / 8 + (y - OY) / 4) / 2; fy = ((y - OY) / 4 - (x - OX) / 8) / 2
        if 0 <= fx < N and 0 <= fy < N:
            band = int(fy * 3); along = fx + (band % 2) * 0.5
            plank = int(along * 1.5)
            c = WOOD[(plank * 3 + band * 7) % 4]
            if (fy * 3) % 1 < 0.12 or (along * 1.5) % 1 < 0.06: c = SEAM
            # 멀수록 어둡게
            k = 0.78 + 0.22 * min(1, (fx + fy) / (2 * N) * 1.6)
            if random.random() < .06: k *= .93
            px[x, y] = shade(c, k)
# 러그
RUG, RUG2, RUGB, RUGG = hexc('#7C2633'), hexc('#5E1A27'), hexc('#3E1018'), hexc('#C79A4B')
for y in range(H):
    for x in range(W):
        fx = ((x - OX) / 8 + (y - OY) / 4) / 2; fy = ((y - OY) / 4 - (x - OX) / 8) / 2
        if 3 <= fx < 8 and 3.5 <= fy < 8.5:
            ex, ey = min(fx - 3, 8 - fx), min(fy - 3.5, 8.5 - fy)
            e = min(ex, ey)
            if e < .12: c = RUGB
            elif e < .3: c = RUGG if int((fx + fy) * 4) % 2 else hexc('#A87A36')
            elif e < .42: c = RUG2
            else:
                cx, cy = fx - 5.5, fy - 6
                r = abs(cx) + abs(cy)
                c = RUGG if abs(r - 1.2) < .1 else RUG2 if abs(r - 0.6) < .12 or r < .18 else RUG
                if int((fx * 2 + fy * 2)) % 3 == 0 and r > 1.4 and int(fy * 8) % 4 == 0: c = hexc('#9A3640')
            px[x, y] = shade(c, 0.85 + 0.15 * min(1, (fx + fy) / 14))
# 바닥 마법진 (러그 위 왼쪽 앞)
mc = hexc('#7FE3B0')
for a in range(0, 360, 4):
    for rr, step in ((1.15, 1), (0.85, 2)):
        if (a // 4) % step: continue
        tx = 2.0 + rr * math.cos(math.radians(a)); ty = 7.6 + rr * math.sin(math.radians(a))
        x, y = P(tx, ty); put(bg, x, y, mc)
for k in range(5):
    a1 = math.radians(k * 144 - 90); a2 = math.radians((k + 2) * 144 - 90)
    for t in [i / 14 for i in range(15)]:
        tx = 2.0 + 0.85 * ((1 - t) * math.cos(a1) + t * math.cos(a2)); ty = 7.6 + 0.85 * ((1 - t) * math.sin(a1) + t * math.sin(a2))
        x, y = P(tx, ty); put(bg, x, y, hexc('#5CC690'))
# ---------- 벽 ----------
TOP, LEFT, RIGHT = P(0, 0), P(0, N), P(N, 0)
WAIN, WAIN2, WAINH = hexc('#4C2B1C'), hexc('#3B2015'), hexc('#5F3826')
PAPER, PAPER2, PAPERD = hexc('#2D4A3B'), hexc('#3A5E4A'), hexc('#223A2E')
TRIM, MOLD = hexc('#C49446'), hexc('#5C3A22')
def wall_px(side, u, v):          # u: 벽을 따라 x 픽셀, v: 높이 픽셀
    if side == 'L': return LEFT[0] + u, LEFT[1] - u / 2 - v
    return TOP[0] + u, TOP[1] + u / 2 - v
WL = N * 8
def wall_fill(side, u0, u1, v0, v1, fn):
    for u in range(int(u0), int(u1)):
        for v in range(int(v0), int(v1)):
            x, y = wall_px(side, u, v)
            c = fn(u, v) if callable(fn) else fn
            if c: put(bg, x, y, c)
for side in ('L', 'R'):
    dark = 0.86 if side == 'L' else 1.0
    def base(u, v, side=side, dark=dark):
        if v < 22:   # 징두리 판벽
            pu = u % 16
            c = WAIN
            if pu in (0, 1) or v in (3, 19): c = WAIN2
            elif pu == 2 or v == 4: c = WAINH
            if v >= 20: c = MOLD
            if v == 21: c = TRIM
            return shade(c, dark)
        if v >= WALL - 4: return shade(MOLD if v < WALL - 1 else TRIM, dark)
        # 다마스크 무늬 벽지
        c = PAPER
        a, b = u % 12, (v - 22) % 14
        if (a - 6) ** 2 / 9 + (b - 7) ** 2 / 16 < 1 and not ((a - 6) ** 2 / 3 + (b - 7) ** 2 / 7 < 1): c = PAPER2
        if a in (0,) and b % 2 == 0: c = PAPERD
        return shade(c, dark * (0.8 + 0.2 * v / WALL))
    wall_fill(side, 0, WL, 0, WALL, base)
# 벽 모서리 기둥
for v in range(WALL):
    for d in (-1, 0, 1):
        put(bg, TOP[0] + d, TOP[1] - v, hexc('#3A2116') if d else hexc('#6A4128'))
# 창문 (아치형, 달빛)
def window(side, u0, w=16, v0=26, h=30):
    fr, gl, gl2, gl3 = hexc('#2E1B12'), hexc('#28406E'), hexc('#3D62A0'), hexc('#7FA6E0')
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        cx = w / 2; top = h - cx
        if vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > cx ** 2: return None
        edge = uu < 2 or uu >= w - 2 or vv < 2 or (vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > (cx - 2) ** 2)
        if edge: return fr
        if uu in (w // 2 - 1, w // 2) or vv in (12, 22): return fr
        g = gl
        if (uu + vv) % 9 == 0 or (uu - vv) % 11 == 0: g = gl2
        if uu < w // 2 and 14 < vv < 21 and uu > 3: g = gl3 if (uu + vv) % 3 == 0 else gl2
        return g
    wall_fill(side, u0, u0 + w, v0, v0 + h, f)
    # 창틀 아래 선반
    wall_fill(side, u0 - 1, u0 + w + 1, v0 - 2, v0, hexc('#6A4128'))
window('R', 44); window('L', 50)
# 그림 액자
def frame_pic(side, u0, v0, w, h, inner):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        if uu < 2 or vv < 2 or uu >= w - 2 or vv >= h - 2: return TRIM if (uu + vv) % 2 else hexc('#8E6A2E')
        return inner(uu, vv)
    wall_fill(side, u0, u0 + w, v0, v0 + h, f)
frame_pic('R', 18, 30, 14, 18, lambda u, v: hexc('#3A2A4A') if v > 8 else hexc('#1E2A44') if (u - 7) ** 2 + (v - 5) ** 2 > 6 else hexc('#E8D8A0'))
frame_pic('L', 26, 34, 12, 14, lambda u, v: hexc('#52331E') if v < 4 else hexc('#7A5A3A') if (u - 6) ** 2 + (v - 8) ** 2 < 10 else hexc('#2C3A30'))
# 벽에 붙은 책장 (왼쪽 벽 앞쪽 끝) - 벽에 붙어 있어 캐릭터가 뒤로 못 가니 배경에 그려요
BOOK = ['#7A2A30', '#2E5A6E', '#7A6A2A', '#4A2E6A', '#2E6A44', '#8A4A2A', '#5A5A6A', '#6A2A4A']
def shelf(side, u0, w, h):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 0 <= v < h): return None
        if uu < 2 or uu >= w - 2 or v >= h - 2 or v < 1: return hexc('#3E2216')
        row = (v - 1) % 11
        if row in (0, 1): return hexc('#55311F')
        bi = (uu + (v // 11) * 3) // 3
        c = hexc(BOOK[(bi * 5 + v // 11) % len(BOOK)])
        if (uu % 3) == 0: c = shade(c, .7)
        if row == 2 and bi % 4 == 0: return hexc('#2A1810')
        if row == 7 and (uu % 3) == 1: c = hexc('#C49446')
        return shade(c, .95)
    wall_fill(side, u0, u0 + w, 0, h, f)
shelf('L', 4, 22, 48); shelf('R', 2, 12, 40)
# 오른쪽 벽: 물약 선반
def potion_shelf(side, u0, v0, w):
    cols = ['#7FE3B0', '#FF7A8A', '#8AB8FF', '#FFD86A', '#C08AFF', '#FF9A4A']
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < 22): return None
        if vv in (0, 1, 11, 12): return hexc('#5C3A22')
        slot = uu // 4
        if uu % 4 == 3: return None
        top = 6 if vv < 11 else 17
        if vv >= top + 4 or vv < 2: return None
        hgt = 3 + (slot * 7 + vv // 11) % 3
        lv = (vv - 2) if vv < 11 else (vv - 13)
        if lv < 7 - hgt: return None
        c = hexc(cols[(slot + vv // 11 * 2) % len(cols)])
        if uu % 4 == 0: c = shade(c, .7)
        return c
    wall_fill(side, u0, u0 + w, v0, v0 + 22, f)
potion_shelf('R', 64, 28, 14)
# 벽 촛대 (빛은 화면에서 따로 그려요)
def sconce(side, u):
    wall_fill(side, u, u + 3, 30, 32, hexc('#C49446'))
    wall_fill(side, u + 1, u + 2, 32, 37, hexc('#F2E6C8'))
    wall_fill(side, u + 1, u + 2, 37, 39, hexc('#FFD27A'))
sconce('L', 44); sconce('L', 70); sconce('R', 38); sconce('R', 62)
# 바닥-벽 경계 그림자
for x in range(W):
    for y in range(H):
        fx = ((x - OX) / 8 + (y - OY) / 4) / 2; fy = ((y - OY) / 4 - (x - OX) / 8) / 2
        if 0 <= fx < N and 0 <= fy < N and (fx < .45 or fy < .45):
            px[x, y] = shade(px[x, y], .7 + .3 * min(fx, fy) / .45)
bg.save('out/lab_bg.png')

# ---------- 가구 스프라이트 ----------
def poly(d, pts, c): d.polygon([tuple(map(int, p)) for p in pts], fill=c)
def box(img, tx, ty, w, dpt, h, top, left, right, lift=0):
    d = ImageDraw.Draw(img)
    T, R, B, L = P(tx, ty), P(tx + w, ty), P(tx + w, ty + dpt), P(tx, ty + dpt)
    up = lambda p, k: (p[0], p[1] - k)
    poly(d, [up(L, lift), up(B, lift), up(B, lift + h), up(L, lift + h)], left)
    poly(d, [up(B, lift), up(R, lift), up(R, lift + h), up(B, lift + h)], right)
    poly(d, [up(T, lift + h), up(R, lift + h), up(B, lift + h), up(L, lift + h)], top)
def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 0 for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                add.append((x, y))
    for x, y in add: a[x, y] = c
objs = []
def obj(name, tiles, draw, key=None):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw(img); outline(img)
    bb = img.getbbox(); spr = img.crop(bb)
    objs.append(dict(name=name, tiles=tiles, x=bb[0], y=bb[1], w=spr.width, h=spr.height, key=key if key is not None else max(a + b for a, b in tiles), img=spr))
# 솥 (2x2, 뒤쪽 가운데)
def cauldron(img):
    d = ImageDraw.Draw(img); cx, cy = P(5, 3)
    cy += 2
    d.ellipse([cx - 13, cy - 14, cx + 13, cy + 6], fill=hexc('#2A2630'))
    d.ellipse([cx - 13, cy - 14, cx + 13, cy + 2], fill=hexc('#3A3644'))
    d.ellipse([cx - 11, cy - 14, cx + 11, cy - 6], fill=hexc('#46424F'))
    d.ellipse([cx - 9, cy - 13, cx + 9, cy - 7], fill=hexc('#5CE6A0'))
    d.ellipse([cx - 6, cy - 12, cx + 4, cy - 9], fill=hexc('#A8FFD0'))
    for i, (dx, dy) in enumerate(((-8, 4), (7, 4), (0, 6))): d.rectangle([cx + dx - 1, cy + dy, cx + dx + 1, cy + dy + 3], fill=hexc('#2A2630'))
    for dx in (-5, -1, 3): d.polygon([(cx + dx, cy + 9), (cx + dx + 2, cy + 3), (cx + dx + 4, cy + 9)], fill=hexc('#FF8A3A'))
    d.polygon([(cx - 1, cy + 9), (cx + 1, cy + 5), (cx + 3, cy + 9)], fill=hexc('#FFE07A'))
    for bx, by in ((-3, -18), (2, -22), (-1, -27), (4, -16)): d.ellipse([cx + bx, cy + by, cx + bx + 2, cy + by + 2], fill=hexc('#8AF5C0'))
obj('cauldron', [(4, 2), (5, 2), (4, 3), (5, 3)], cauldron)
# 책상 (왼쪽, 2x1) + 책·촛불·두루마리
def desk(img):
    box(img, 1, 4, 1, 2, 9, hexc('#7A4A2E'), hexc('#4A2A1C'), hexc('#5E3826'))
    d = ImageDraw.Draw(img); x, y = P(1.5, 4.6); y -= 9
    d.rectangle([x - 3, y - 4, x + 3, y - 1], fill=hexc('#7A2A30')); d.rectangle([x - 3, y - 6, x + 2, y - 4], fill=hexc('#2E5A6E'))
    x2, y2 = P(1.5, 5.6); y2 -= 9
    d.polygon([(x2 - 5, y2), (x2, y2 - 2), (x2 + 5, y2), (x2, y2 + 2)], fill=hexc('#EADBB0'))
    d.line([(x2 - 3, y2), (x2 + 2, y2 - 1)], fill=hexc('#6A5A3A'))
    x3, y3 = P(1.3, 5.0); y3 -= 9
    d.rectangle([x3 - 1, y3 - 7, x3, y3 - 1], fill=hexc('#F2E6C8')); d.rectangle([x3 - 1, y3 - 9, x3, y3 - 8], fill=hexc('#FFD27A'))
obj('desk', [(1, 4), (1, 5)], desk)
# 의자 (책상 앞)
obj('chair', [(2, 5)], lambda img: (box(img, 2.15, 4.95, .7, .7, 6, hexc('#8A3A2E'), hexc('#4A2A1C'), hexc('#5E3826')), box(img, 2.75, 4.95, .15, .7, 14, hexc('#6A2E24'), hexc('#4A2A1C'), hexc('#5E3826'))))
# 둥근 탁자 + 수정구 (오른쪽)
def table(img):
    d = ImageDraw.Draw(img); cx, cy = P(8, 5.5)
    d.rectangle([cx - 1, cy - 9, cx + 1, cy], fill=hexc('#3E2216')); d.ellipse([cx - 4, cy - 1, cx + 4, cy + 2], fill=hexc('#3E2216'))
    d.ellipse([cx - 9, cy - 13, cx + 9, cy - 7], fill=hexc('#6E412B')); d.ellipse([cx - 9, cy - 14, cx + 9, cy - 9], fill=hexc('#8A5636'))
    d.ellipse([cx - 4, cy - 21, cx + 4, cy - 13], fill=hexc('#8FB8FF')); d.ellipse([cx - 3, cy - 20, cx, cy - 17], fill=hexc('#E0F0FF'))
    d.rectangle([cx - 3, cy - 13, cx + 3, cy - 11], fill=hexc('#C49446'))
obj('table', [(7, 5), (8, 5)], table)
# 안락의자 (앞 오른쪽)
obj('armchair', [(7, 8)], lambda img: (box(img, 7.05, 7.9, .9, 1, 7, hexc('#3E6A4E'), hexc('#24402E'), hexc('#2E5A3E')), box(img, 7.05, 7.9, .25, 1, 15, hexc('#4A7A5A'), hexc('#24402E'), hexc('#2E5A3E')), box(img, 7.05, 7.9, .9, .2, 11, hexc('#4A7A5A'), hexc('#24402E'), hexc('#2E5A3E'))))
# 스탠드 등 (오른쪽 뒤)
def lamp(img):
    d = ImageDraw.Draw(img); cx, cy = P(8.5, 1.5)
    d.ellipse([cx - 3, cy - 1, cx + 3, cy + 2], fill=hexc('#2A1810')); d.rectangle([cx, cy - 22, cx + 1, cy], fill=hexc('#3E2216'))
    d.polygon([(cx - 5, cy - 22), (cx - 3, cy - 30), (cx + 4, cy - 30), (cx + 6, cy - 22)], fill=hexc('#3E6A9A'))
    d.line([(cx - 5, cy - 22), (cx + 6, cy - 22)], fill=hexc('#C49446'))
obj('lamp', [(8, 1)], lamp)
# 화분 (앞 왼쪽)
def plant(img):
    d = ImageDraw.Draw(img); cx, cy = P(0.6, 8.4)
    d.polygon([(cx - 4, cy - 7), (cx + 4, cy - 7), (cx + 3, cy), (cx - 3, cy)], fill=hexc('#A8563A'))
    for dx, dy, r in ((-4, -14, 4), (3, -15, 4), (0, -19, 4), (-1, -11, 3), (4, -10, 3)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#3E8A4E'))
    for dx, dy in ((-3, -16), (2, -20), (4, -12)): d.point((cx + dx, cy + dy), fill=hexc('#7ACB7A'))
obj('plant', [(0, 8)], plant)
# 재료 통 (오른쪽 앞)
def barrels(img):
    for tx, ty, col in ((9.2, 7.2, '#7A4A2E'), (9.3, 8.4, '#6E412B')):
        d = ImageDraw.Draw(img); cx, cy = P(tx, ty)
        d.rectangle([cx - 5, cy - 11, cx + 5, cy], fill=hexc(col)); d.ellipse([cx - 5, cy - 2, cx + 5, cy + 2], fill=hexc(col))
        d.ellipse([cx - 5, cy - 13, cx + 5, cy - 9], fill=hexc('#9A6A44'))
        for yy in (-8, -3): d.line([(cx - 5, cy + yy), (cx + 5, cy + yy)], fill=hexc('#3E2216'))
        d.ellipse([cx - 3, cy - 12, cx + 3, cy - 10], fill=hexc('#7ACB7A' if ty < 8 else '#C08AFF'))
obj('barrels', [(9, 7), (9, 8)], barrels)
# 책 더미 (뒤 왼쪽 바닥)
def books(img):
    d = ImageDraw.Draw(img); cx, cy = P(1.5, 1.5)
    for i, c in enumerate(['#7A2A30', '#2E5A6E', '#7A6A2A', '#4A2E6A']):
        d.rectangle([cx - 5 + (i % 2), cy - 3 - i * 3, cx + 4 - (i % 2), cy - i * 3], fill=hexc(c))
obj('books', [(1, 1)], books)
# 시트로 합치기
sheet_w = sum(o['w'] + 1 for o in objs); sheet_h = max(o['h'] for o in objs)
sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0)); sx = 0
meta = []
for o in objs:
    sheet.paste(o['img'], (sx, 0))
    meta.append(dict(name=o['name'], tiles=o['tiles'], sx=sx, sw=o['w'], sh=o['h'], x=o['x'], y=o['y'], key=o['key'])); sx += o['w'] + 1
sheet.save('out/lab_obj.png')
LIGHTS = [  # x, y(화면), 반지름, 색
    dict(p=P(5, 3), dy=-8, r=46, c=[90, 255, 160], a=.55, f=1),
    dict(p=P(8.5, 1.5), dy=-26, r=34, c=[255, 200, 120], a=.5, f=0),
    dict(p=P(1.3, 5.0), dy=-18, r=22, c=[255, 190, 100], a=.55, f=1),
    dict(p=P(8, 5.5), dy=-17, r=18, c=[140, 180, 255], a=.45, f=0),
]
for side, u in (('L', 44), ('L', 70), ('R', 38), ('R', 62)):
    x, y = wall_px(side, u + 1, 38); LIGHTS.append(dict(p=(x, y), dy=0, r=20, c=[255, 190, 110], a=.5, f=1))
for side, u in (('R', 52), ('L', 58)):
    x, y = wall_px(side, u, 40); LIGHTS.append(dict(p=(x, y), dy=0, r=26, c=[110, 150, 255], a=.28, f=0))
json.dump(dict(W=W, H=H, N=N, OX=OX, OY=OY, objs=meta, lights=LIGHTS), open('out/lab.json', 'w'))
print('ok', len(objs))
