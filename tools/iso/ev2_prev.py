# 이벤트 2 「유령 선장의 보물 지도」 시안용 그림: 호수의 유령선, 보물섬 (게임 지도와 같은 그림 방식) → out/ev2_lake.png, out/ev2_island.png
import math, os, random
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(11)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
OUTL = hexc('#120A18')
def make(NX, NY, tiles, name, objs_fn, sky='#0C0A1C'):
    W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 160
    OX, OY = NY * 8 + 20, 120
    P = lambda tx, ty: (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
    bg = Image.new('RGBA', (W, H), hexc(sky)); px = bg.load()
    for y in range(H):
        for x in range(W):
            a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
            if not (0 <= fx < NX and 0 <= fy < NY): continue
            t = tiles(int(fx), int(fy), fx, fy); px[x, y] = t
    # 옆면
    for x in range(W):
        for y in range(H):
            if px[x, y][:3] != hexc(sky)[:3]: continue
            a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
            if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#241E34') if (y // 3) % 2 else hexc('#1C1628')
    sprites = []
    def spr(draw, tx, ty, w=300, h=300):
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); draw(img, d, *P(tx + .5, ty + .5)); sprites.append((tx + ty, tx, ty, img))
    objs_fn(spr, P)
    for _, _, _, img in sorted(sprites, key=lambda s: (s[0], s[1])):
        # 윤곽선
        bb = img.getbbox()
        if bb:
            a = img.load(); add = []
            for y in range(max(0, bb[1] - 1), min(H, bb[3] + 1)):
                for x in range(max(0, bb[0] - 1), min(W, bb[2] + 1)):
                    if a[x, y][3] == 0:
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            if 0 <= x + dx < W and 0 <= y + dy < H and a[x + dx, y + dy][3] > 200: add.append((x, y)); break
            for x, y in add: a[x, y] = OUTL
        bg.alpha_composite(img)
    bg = bg.crop((0, 40, W, H)); bg.save('out/' + name); print(name, bg.size)
def poly(d, pts, c): d.polygon([tuple(map(int, p)) for p in pts], fill=c)
# ---------- 호수의 유령선 ----------
WATER = [hexc('#1E3A58'), hexc('#22405E'), hexc('#1A3450'), hexc('#264866')]
def lake_tiles(x, y, fx, fy):
    d = math.hypot(fx - 15, fy - 12)
    if d > 14 or (fx < 2 and fy < 2): return hexc('#3E4E3A') if random.random() > .2 else hexc('#36463A')   # 호숫가 풀밭
    if d > 12.2: return hexc('#8A7A5A') if random.random() > .2 else hexc('#7A6A4A')
    c = WATER[(int(fx * 3) * 5 + int(fy * 3) * 3 + random.randint(0, 1)) % 4]
    if random.random() < .015: c = hexc('#5A8AB0')
    return c
def lake_objs(spr, P):
    def ship(img, d, cx, cy):
        # 선체
        poly(d, [(cx - 54, cy - 22), (cx + 56, cy - 30), (cx + 44, cy + 6), (cx - 40, cy + 12)], hexc('#3E2E2A'))
        poly(d, [(cx - 54, cy - 22), (cx + 56, cy - 30), (cx + 54, cy - 24), (cx - 52, cy - 16)], hexc('#5A4438'))
        for k in range(6): d.line([(cx - 48 + k * 18, cy - 20 - k * 1), (cx - 40 + k * 18, cy + 10 - k * 2)], fill=hexc('#2A1E1E'))
        poly(d, [(cx - 54, cy - 22), (cx - 70, cy - 40), (cx - 50, cy - 30)], hexc('#3E2E2A'))   # 뱃머리
        # 돛대 · 찢어진 돛
        for mx, mh in ((cx - 12, 84), (cx + 24, 74)):
            d.rectangle([mx - 2, cy - mh - 24, mx + 1, cy - 26], fill=hexc('#4A3A32'))
            poly(d, [(mx - 20, cy - mh - 14), (mx + 20, cy - mh - 14), (mx + 17, cy - 40), (mx + 8, cy - 46), (mx - 6, cy - 38), (mx - 18, cy - 44)], hexc('#B8D4D8', 200))
            for k in range(4): d.line([(mx - 14 + k * 10, cy - mh - 12), (mx - 12 + k * 10, cy - 44)], fill=hexc('#7AA0A8', 220))
        # 해골 깃발
        poly(d, [(cx - 12, cy - 112), (cx + 8, cy - 108), (cx - 12, cy - 98)], hexc('#1A1424'))
        d.ellipse([cx - 9, cy - 108, cx - 3, cy - 102], fill=hexc('#E8E4D0'))
        # 유령 등불
        for lx, ly in ((cx - 40, cy - 22), (cx + 44, cy - 26), (cx + 4, cy - 28)):
            d.rectangle([lx, ly - 8, lx + 1, ly], fill=hexc('#2A2230')); d.ellipse([lx - 4, ly - 16, lx + 6, ly - 6], fill=hexc('#6AE8E0')); d.ellipse([lx - 1, ly - 13, lx + 3, ly - 9], fill=hexc('#E8FFFF'))
    spr(ship, 14, 10)
    def dock(img, d, cx, cy):
        for k in range(5): poly(d, [(cx + k * 8 - 8, cy + k * 4), (cx + k * 8 + 8, cy + k * 4 + 4), (cx + k * 8 + 8, cy + k * 4 + 8), (cx + k * 8 - 8, cy + k * 4 + 4)], hexc('#5A4636') if k % 2 else hexc('#6A5444'))
    for i in range(5): spr(lambda img, d, cx, cy, i=i: poly(d, [(cx - 8, cy - 2), (cx + 8, cy + 2), (cx + 8, cy + 6), (cx - 8, cy + 2)], hexc('#5A4636') if i % 2 else hexc('#6A5444')), 3 + i, 20 - i * 0)
    def reeds(img, d, cx, cy):
        for dx in (-6, 0, 6): d.line([(cx + dx, cy), (cx + dx + random.randint(-2, 2), cy - random.randint(10, 18))], fill=hexc('#3E5A3A'), width=2)
    for (x, y) in [(4, 5), (3, 9), (26, 6), (27, 13), (24, 22), (6, 22), (9, 3), (22, 3)]: spr(reeds, x, y)
    def fog(img, d, cx, cy):
        fg = Image.new('RGBA', img.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
        for k in range(6): fd.ellipse([cx - 40 + k * 14, cy - 8 - (k % 2) * 6, cx + 10 + k * 14, cy + 12 - (k % 2) * 6], fill=(190, 220, 230, 42))
        img.alpha_composite(fg)
    for (x, y) in [(10, 14), (18, 16), (22, 9), (8, 8), (16, 18)]: spr(fog, x, y)
make(30, 26, lake_tiles, 'ev2_lake.png', lake_objs)
# ---------- 보물섬 ----------
def isl_tiles(x, y, fx, fy):
    d = math.hypot((fx - 15) * .9, (fy - 12) * 1.05) + math.sin(fx * .7) * .8 + math.cos(fy * .9) * .7
    if d > 11: return WATER[(int(fx * 3) * 5 + int(fy * 3) * 3 + random.randint(0, 1)) % 4]
    if d > 9.4: return hexc('#C8B488') if random.random() > .3 else hexc('#B8A478')
    if d > 7.2: return hexc('#D8C494') if random.random() > .2 else hexc('#C8B484')
    c = [hexc('#4E7A4A'), hexc('#46704A'), hexc('#58844E')][(int(fx * 4) * 7 + int(fy * 4) * 3 + random.randint(0, 2)) % 3]
    if abs(fx - 15) < 1.2 and fy > 12: c = hexc('#C8A878')   # 길
    return c
def isl_objs(spr, P):
    def palm(img, d, cx, cy):
        d.line([(cx, cy), (cx + 3, cy - 14), (cx + 1, cy - 26)], fill=hexc('#7A5A3A'), width=3)
        for a, l in ((200, 20), (240, 22), (290, 20), (330, 18), (160, 16), (20, 16)):
            ex, ey = cx + 1 + math.cos(math.radians(a)) * l, cy - 26 + math.sin(math.radians(a)) * l * .6 + 6
            poly(d, [(cx + 1, cy - 27), ((cx + ex) / 2, (cy - 30 + ey) / 2 - 5), (ex, ey)], hexc('#3E9A4A')); d.line([(cx + 1, cy - 27), (ex, ey)], fill=hexc('#2A7A3A'))
        d.ellipse([cx - 1, cy - 26, cx + 3, cy - 22], fill=hexc('#8A5A2A'))
    def rock(img, d, cx, cy):
        d.ellipse([cx - 9, cy - 10, cx + 9, cy + 2], fill=hexc('#7A7A82')); d.ellipse([cx - 6, cy - 10, cx + 2, cy - 4], fill=hexc('#A0A0AA'))
    def chest(img, d, cx, cy, open_=False):
        poly(d, [(cx - 9, cy - 10), (cx + 9, cy - 10), (cx + 9, cy + 1), (cx - 9, cy + 1)], hexc('#8A5A2A')); d.rectangle([cx - 9, cy - 14, cx + 9, cy - 9], fill=hexc('#A8702E'))
        d.rectangle([cx - 1, cy - 12, cx + 1, cy - 7], fill=hexc('#E8C050')); d.line([(cx - 9, cy - 5), (cx + 9, cy - 5)], fill=hexc('#E8C050'))
    def skull(img, d, cx, cy): d.ellipse([cx - 5, cy - 9, cx + 5, cy - 1], fill=hexc('#E8E4D0')); d.rectangle([cx - 3, cy - 6, cx - 2, cy - 5], fill=OUTL); d.rectangle([cx + 2, cy - 6, cx + 3, cy - 5], fill=OUTL)
    def xmark(img, d, cx, cy): d.line([(cx - 8, cy - 4), (cx + 8, cy + 2)], fill=hexc('#B03030'), width=3); d.line([(cx - 8, cy + 2), (cx + 8, cy - 4)], fill=hexc('#B03030'), width=3)
    def torch(img, d, cx, cy):
        d.rectangle([cx - 1, cy - 20, cx + 1, cy], fill=hexc('#5A4430')); poly(d, [(cx - 5, cy - 20), (cx, cy - 34), (cx + 5, cy - 20)], hexc('#6AE8E0')); poly(d, [(cx - 2, cy - 20), (cx, cy - 29), (cx + 2, cy - 20)], hexc('#E8FFFF'))
    def anchor(img, d, cx, cy):
        d.line([(cx, cy - 22), (cx, cy)], fill=hexc('#6A6A7A'), width=3); d.arc([cx - 12, cy - 12, cx + 12, cy + 6], 0, 180, fill=hexc('#6A6A7A'), width=3); d.line([(cx - 6, cy - 18), (cx + 6, cy - 18)], fill=hexc('#6A6A7A'), width=3)
    def boat(img, d, cx, cy): poly(d, [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx + 12, cy + 2), (cx - 12, cy + 4)], hexc('#6A4A32')); poly(d, [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx + 17, cy - 9), (cx - 16, cy - 5)], hexc('#8A6444'))
    for (x, y) in [(10, 8), (20, 8), (9, 14), (21, 15), (12, 18), (19, 18), (14, 6), (17, 20), (8, 11), (22, 11)]: spr(palm, x, y)
    for (x, y) in [(12, 10), (19, 13), (13, 16)]: spr(rock, x, y)
    for (x, y, k) in [(15, 11, 0), (11, 13, 1), (19, 10, 2)]: spr(chest, x, y); spr(xmark, x, y + 1) if False else None
    spr(skull, 16, 14); spr(skull, 13, 12); spr(anchor, 18, 17); spr(boat, 15, 21); spr(torch, 14, 19); spr(torch, 16, 19)
make(30, 26, isl_tiles, 'ev2_island.png', isl_objs)
