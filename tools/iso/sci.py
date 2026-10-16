# 과학실 (밝은 현대 교실): 바닥·벽(배경) + 실험대 등 스프라이트
import json, math, random
from PIL import Image, ImageDraw
random.seed(4)
W, H = 211, 196
N = 11
OX, OY = 105, 72
WALL = 64
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#2A2230')
bg = Image.new('RGBA', (W, H), hexc('#1E1A26')); px = bg.load()
def put(x, y, c):
    if 0 <= int(x) < W and 0 <= int(y) < H: px[int(x), int(y)] = c
# 바닥: 밝은 리놀륨 타일
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if 0 <= fx < N and 0 <= fy < N:
            c = hexc('#D8D4C8') if (int(fx) + int(fy)) % 2 else hexc('#C8C4B8')
            if fx % 1 < .05 or fy % 1 < .05: c = hexc('#B0ACA0')
            if fx < .4 or fy < .4: c = shade(c, .85)
            px[x, y] = c
TOP, LEFT = P(0, 0), P(0, N)
def wall_px(side, u, v):
    if side == 'L': return LEFT[0] + u, LEFT[1] - u / 2 - v
    return TOP[0] + u, TOP[1] + u / 2 - v
def wall_fill(side, u0, u1, v0, v1, fn):
    for u in range(int(u0), int(u1)):
        for v in range(int(v0), int(v1)):
            c = fn(u, v) if callable(fn) else fn
            if c: put(*wall_px(side, u, v), c)
for side, dark in (('L', .9), ('R', 1.0)):
    def base(u, v, dark=dark):
        if v < 18: c = hexc('#9AC4A8') if v < 16 else hexc('#6A9A7A')      # 아래 연두 판벽
        elif v >= WALL - 3: c = hexc('#E8E4DC')
        else: c = hexc('#F4F0E6')
        return shade(c, dark)
    wall_fill(side, 0, N * 8, 0, WALL, base)
for v in range(WALL): put(TOP[0], TOP[1] - v, hexc('#C8C4BC'))
# 왼쪽 벽: 칠판
def board(u, v):
    if 22 <= v < 52 and 10 <= u < 70:
        if v < 24 or v >= 50 or u < 12 or u >= 68: return hexc('#8A6A4A')
        c = hexc('#2E5A44')
        # 분필 글씨
        if v in (44, 45) and 16 <= u < 40 and u % 3: return hexc('#E8F0E0')
        if v in (38, 39) and 18 <= u < 50 and (u // 2) % 3: return hexc('#E8F0E0')
        if 26 <= v < 34 and abs((u - 56) ** 2 / 16 + (v - 30) ** 2 / 9 - 1) < .35: return hexc('#F2E27A')   # 원자 그림
        if 26 <= v < 34 and abs((u - 56) ** 2 / 4 + (v - 30) ** 2 / 16 - 1) < .4: return hexc('#F2E27A')
        return c
    if 20 <= v < 22 and 12 <= u < 68: return hexc('#A8A49C')    # 분필 받침
    return None
wall_fill('L', 0, N * 8, 0, WALL, board)
# 왼쪽 벽: 주기율표
def ptable(u, v):
    if 26 <= v < 46 and 74 <= u < 86:
        if v in (26, 45) or u in (74, 85): return hexc('#8A8A92')
        return [hexc('#F2A0A0'), hexc('#A0C8F2'), hexc('#F2E27A'), hexc('#A8E0A8')][((u - 74) // 2 + (v - 26) // 3) % 4] if (u + v) % 2 else hexc('#F8F6EE')
    return None
wall_fill('L', 0, N * 8, 0, WALL, ptable)
# 오른쪽 벽: 큰 창문 (밝은 하늘)
def window(u, v):
    for u0 in (12, 40, 68):
        uu, vv = u - u0, v - 22
        if 0 <= uu < 20 and 0 <= vv < 34:
            if uu in (0, 19, 10) or vv in (0, 33, 16): return hexc('#E8E8E4')
            c = hexc('#A8D4F0') if vv > 8 else hexc('#C8E6F8')
            if (uu + vv) % 11 == 0: c = hexc('#E0F2FF')
            if vv < 6 and 3 < uu < 9: c = hexc('#FFFFFF')
            return c
    return None
wall_fill('R', 0, N * 8, 0, WALL, window)
# 오른쪽 벽 위: 시계
def clock(u, v):
    if (u - 60) ** 2 + (v - 59) ** 2 < 9: return hexc('#F8F6EE') if (u - 60) ** 2 + (v - 59) ** 2 < 5 else hexc('#3A3A42')
    return None
wall_fill('L', 0, N * 8, 0, WALL, lambda u, v: clock(u - 30, v) if 0 else None)
wall_fill('R', 0, N * 8, 0, WALL, lambda u, v: hexc('#F8F6EE') if (u - 6) ** 2 + (v - 58) ** 2 < 6 else hexc('#3A3A42') if (u - 6) ** 2 + (v - 58) ** 2 < 10 else None)
# 벽 쪽 선반 (비커 진열) - 왼쪽 벽 끝
def shelf(u, v):
    if 0 <= u - 2 < 6 and v < 46:
        if v % 12 < 2 or u - 2 in (0, 5): return hexc('#9A7A5A')
        k = (v // 12 + u) % 3
        if v % 12 > 6: return [hexc('#7FE3B0'), hexc('#8AB8FF'), hexc('#FF9AA8')][k]
        return hexc('#E8F4F8') if (u + v) % 2 else None
    return None
wall_fill('R', 0, N * 8, 0, WALL, lambda u, v: shelf(u - 84, v) if 0 else None)
bg.save('out/sci_bg.png')
# ---------------- 스프라이트 ----------------
def poly(d, pts, c): d.polygon([tuple(map(int, p)) for p in pts], fill=c)
def box(img, tx, ty, w, dp, h, top, left, right, lift=0):
    d = ImageDraw.Draw(img)
    Tt, R, B, L = P(tx, ty), P(tx + w, ty), P(tx + w, ty + dp), P(tx, ty + dp)
    poly(d, [up(L, lift), up(B, lift), up(B, lift + h), up(L, lift + h)], left)
    poly(d, [up(B, lift), up(R, lift), up(R, lift + h), up(B, lift + h)], right)
    poly(d, [up(Tt, lift + h), up(R, lift + h), up(B, lift + h), up(L, lift + h)], top)
def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200 for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): add.append((x, y))
    for x, y in add: a[x, y] = c
objs = []
def obj(name, tiles, draw, act=None):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw(img)
    bb = img.getbbox(); bb = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1); spr = img.crop(bb); outline(spr)
    objs.append(dict(name=name, tiles=tiles, x=bb[0], y=bb[1], w=spr.width, h=spr.height, img=spr, act=act))
def bench(tx, ty, items):
    def draw(img):
        box(img, tx, ty, 2, 1, 12, hexc('#2E2E36'), hexc('#B8946A'), hexc('#C8A47A'))
        d = ImageDraw.Draw(img)
        for k, it in enumerate(items):
            x, y = P(tx + .5 + k * .9, ty + .5); y -= 12
            if it == 'beaker': d.rectangle([x - 2, y - 6, x + 2, y], fill=hexc('#D8F0F8')); d.rectangle([x - 2, y - 3, x + 2, y], fill=hexc('#7FE3B0'))
            elif it == 'flask': d.polygon([(x - 3, y), (x - 1, y - 5), (x - 1, y - 8), (x + 1, y - 8), (x + 1, y - 5), (x + 3, y)], fill=hexc('#E8F4F8')); d.polygon([(x - 3, y), (x - 2, y - 2), (x + 2, y - 2), (x + 3, y)], fill=hexc('#FF8AA0'))
            elif it == 'burner': d.rectangle([x - 1, y - 4, x + 1, y], fill=hexc('#5A5A62')); d.polygon([(x - 1, y - 4), (x, y - 8), (x + 1, y - 4)], fill=hexc('#6AB8FF'))
            elif it == 'scope': d.rectangle([x - 2, y - 2, x + 2, y], fill=hexc('#3A3A42')); d.line([(x, y - 2), (x + 1, y - 9)], fill=hexc('#3A3A42'), width=2); d.rectangle([x - 1, y - 11, x + 2, y - 9], fill=hexc('#5A5A62'))
            elif it == 'book': d.rectangle([x - 3, y - 2, x + 3, y], fill=hexc('#4A7AC8')); d.rectangle([x - 3, y - 4, x + 2, y - 2], fill=hexc('#E05A5A'))
    return draw
obj('bench', [(3, 3), (4, 3)], bench(3, 3, ['beaker', 'burner']), act=('실험대', '실험하기'))
obj('bench', [(7, 3), (8, 3)], bench(7, 3, ['flask', 'scope']), act=('실험대', '현미경 보기'))
obj('bench', [(3, 6), (4, 6)], bench(3, 6, ['book', 'beaker']), act=('실험대', '실험하기'))
obj('bench', [(7, 6), (8, 6)], bench(7, 6, ['burner', 'flask']), act=('실험대', '실험하기'))
# 선생님 책상 (칠판 앞)
obj('tdesk', [(1, 4), (1, 5)], lambda img: (box(img, 1, 4, 1, 2, 11, hexc('#A88A6A'), hexc('#7A5A3E'), hexc('#8A6A4A')),
    ImageDraw.Draw(img).rectangle([P(1.5, 4.8)[0] - 3, P(1.5, 4.8)[1] - 15, P(1.5, 4.8)[0] + 3, P(1.5, 4.8)[1] - 11], fill=hexc('#E8E4DC'))), act=('선생님 책상', '레시피 노트 보기'))
# 개수대
def sink(img):
    box(img, 9.6, .2, 1.2, 1.6, 12, hexc('#C8C8CC'), hexc('#9A9AA2'), hexc('#B0B0B8'))
    d = ImageDraw.Draw(img); x, y = P(10.2, 1); y -= 12
    d.ellipse([x - 4, y - 2, x + 4, y + 2], fill=hexc('#8A8A92')); d.line([(x + 2, y - 2), (x + 2, y - 8), (x - 1, y - 8)], fill=hexc('#E8E8EC'), width=1)
obj('sink', [(10, 0), (10, 1)], sink, act=('개수대', '손 씻기'))
# 비커 진열장 (오른쪽 벽 끝)
def cabinet(img):
    box(img, .1, 9, .9, 2, 34, hexc('#B8946A'), hexc('#9A7A5A'), hexc('#A88A6A'))
    d = ImageDraw.Draw(img)
    for k in range(3):
        for j in range(3):
            x, y = P(1, 9.4 + j * .6); y -= 8 + k * 9
            d.rectangle([x - 1, y - 4, x + 1, y], fill=[hexc('#7FE3B0'), hexc('#8AB8FF'), hexc('#FF9AA8')][(k + j) % 3])
obj('cabinet', [(0, 9), (0, 10)], cabinet, act=('약품 진열장', '재료함 열기'))
# 인체 모형 + 화분
def skeleton(img):
    d = ImageDraw.Draw(img); x, y = P(10.5, 9.5)
    d.rectangle([x - 4, y - 2, x + 4, y], fill=hexc('#5A5A62')); d.line([(x, y - 2), (x, y - 26)], fill=hexc('#F2EEE4'))
    d.ellipse([x - 3, y - 32, x + 3, y - 26], fill=hexc('#F2EEE4'))
    for k in range(4): d.line([(x - 4, y - 22 + k * 2), (x + 4, y - 22 + k * 2)], fill=hexc('#F2EEE4'))
    d.line([(x, y - 14), (x - 3, y - 6)], fill=hexc('#F2EEE4')); d.line([(x, y - 14), (x + 3, y - 6)], fill=hexc('#F2EEE4'))
obj('skeleton', [(10, 9)], skeleton, act=('인체 모형 뼈다귀 씨', '말 걸기'))
def plant(img):
    d = ImageDraw.Draw(img); x, y = P(10.5, 4.5)
    d.polygon([(x - 3, y - 6), (x + 3, y - 6), (x + 2, y), (x - 2, y)], fill=hexc('#E08A5A'))
    for dx, dy, r in ((-3, -11, 3), (3, -12, 3), (0, -15, 3)): d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=hexc('#4E9A4E'))
obj('plant', [(10, 4)], plant)
sheet_w = sum(o['w'] + 1 for o in objs); sheet_h = max(o['h'] for o in objs)
sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0)); sx = 0; meta = []
for o in objs:
    sheet.paste(o['img'], (sx, 0))
    xs = [t[0] for t in o['tiles']]; ys = [t[1] for t in o['tiles']]
    meta.append(dict(name=o['name'], box=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], sx=sx, sy=0, sw=o['w'], sh=o['h'], x=o['x'], y=o['y'], door=None, solid=True, act=o['act'])); sx += o['w'] + 1
sheet.save('out/sci_obj.png')
LIGHTS = [dict(p=P(x, y), dy=-50, r=40, c=[255, 250, 230], a=.45, f=0) for x, y in ((3, 3), (8, 3), (3, 8), (8, 8))]
meta.append(dict(name='exit', box=[4, 10, 5, 11], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[4, 10], to='campus', label='별빛고등학교', spawn=[37, 49]), solid=False, act=None))
json.dump(dict(W=W, H=H, NX=N, NY=N, OX=OX, OY=OY, objs=meta, lights=LIGHTS), open('out/sci.json', 'w'), ensure_ascii=False)
print('ok', len(objs))
