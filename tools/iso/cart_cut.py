# 「길 잃은 아기 동물」 첫 장면: 천을 덮은 수레가 밤길에 덜컹 → 기울고 → 옆으로 넘어져요 (아이소 8:4, world.py 그림체)
#   python3 cart_cut.py → out/cart_up.png · cart_tilt.png · cart_fall.png · cart_tarp.png · cart_puff.png · cart_shadows.png + out/cart.json (기준점)
#   수레는 길(y 방향)을 따라 북쪽(화면 오른쪽 위)으로 가요. 기준 칸 (0, 0) 기준으로 그리고, 게임에서 칸만 옮겨요
import json, math, os
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 160, 140
OX, OY = 80, 80
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
OUTL = hexc('#120A18')
WOOD = hexc('#8a5a38'); WOOD2 = hexc('#6e4628'); WOOD3 = hexc('#a8744a'); PLANK = hexc('#5a3820')
CLOTH = hexc('#5e4e7a'); CLOTH2 = hexc('#4a3c64'); CLOTH3 = hexc('#7a6a98'); ROPE = hexc('#c8a870')
IRON = hexc('#3a3448')


def poly(d, pts, c): d.polygon([tuple(map(round, p)) for p in pts], fill=c)


def outline(img):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for x, y in add: a[x, y] = OUTL


def up(p, k): return (p[0], p[1] - k)


def prism(d, x0, y0, x1, y1, hc, z, top, left, right):
    """상자: 네 모서리 높이(hc: T R B L 순, 바닥에서 위로 px)가 달라도 돼요 → 기울어진 상자"""
    T, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
    zt, zr, zb, zl = z
    ht, hr, hb, hl = hc
    poly(d, [up(L, zl), up(B, zb), up(B, zb + hb), up(L, zl + hl)], left)
    poly(d, [up(R, zr), up(B, zb), up(B, zb + hb), up(R, zr + hr)], right)
    poly(d, [up(T, zt + ht), up(R, zr + hr), up(B, zb + hb), up(L, zl + hl)], top)


def wheel(d, cx, cy, r=4.5):
    d.ellipse([cx - r, cy - r * 1.05, cx + r, cy + r * 1.05], fill=WOOD2)
    d.ellipse([cx - r + 1.5, cy - r + 1.5, cx + r - 1.5, cy + r - 1.5], fill=WOOD3)
    for a in range(0, 180, 45):
        t = math.radians(a); d.line([(cx - math.cos(t) * (r - 1), cy - math.sin(t) * (r - 1)), (cx + math.cos(t) * (r - 1), cy + math.sin(t) * (r - 1))], fill=WOOD2)
    d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=IRON)


X0, X1, Y0, Y1, BH, ZW = -.7, .7, -1.2, 1.2, 9, 5     # 수레 몸통: 폭 1.4칸 · 길이 2.4칸 · 높이 9px · 바퀴 위로 5px


def lantern(d, tilt=0):
    bx, by = up(P(.0, Y0 - .5), ZW + BH + 6 + tilt)
    d.line([tuple(map(round, up(P(0, Y0), ZW + BH + 2 + tilt))), (round(bx), round(by))], fill=IRON)
    d.rectangle([bx - 2, by, bx + 2, by + 5], fill=hexc('#FF9A3A')); d.rectangle([bx - 1, by + 1, bx + 1, by + 3], fill=hexc('#FFE08A'))


def cart_up():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # 뒤 바퀴(가려진 쪽)
    for y in (Y0 + .5, Y1 - .5): wheel(d, *up(P(X0, y), ZW - 1))
    # 끌채 두 개 (앞, 위쪽)
    for x in (X0 + .2, X1 - .2): d.line([tuple(map(round, up(P(x, Y0), ZW + 2))), tuple(map(round, up(P(x, Y0 - 1.3), 3)))], fill=WOOD2, width=2)
    z = (ZW,) * 4
    prism(d, X0, Y0, X1, Y1, (BH,) * 4, z, WOOD3, WOOD2, WOOD)
    for k in (3, 6): d.line([tuple(map(round, up(P(X1, Y0), ZW + k))), tuple(map(round, up(P(X1, Y1), ZW + k)))], fill=PLANK)
    # 덮개 천: 둥근 지붕 (세 겹)
    for i, (dx, hh, c) in enumerate(((0, 4, CLOTH2), (.18, 4, CLOTH), (.38, 3, CLOTH3))):
        prism(d, X0 + dx, Y0 - .05, X1 - dx, Y1 + .05, (hh,) * 4, (ZW + BH + i * 4,) * 4, c, shade(c, .8), shade(c, .92))
    # 밧줄
    for y in (Y0 + .5, 0, Y1 - .5):
        d.line([tuple(map(round, up(P(X1 + .02, y), ZW + BH - 1))), tuple(map(round, up(P(X1 - .38, y), ZW + BH + 11)))], fill=ROPE)
    # 앞 바퀴(보이는 쪽)
    for y in (Y0 + .5, Y1 - .5): wheel(d, *up(P(X1, y), ZW - 1))
    lantern(d)
    outline(img); return img


def cart_tilt():
    """보이는 쪽(남동)으로 기울어요: 먼 쪽(x0) 바퀴가 들려요"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lift = 7
    for y in (Y0 + .5, Y1 - .5): wheel(d, *up(P(X0 + .1, y), ZW - 1 + lift + 3))
    z = (ZW + lift, ZW, ZW, ZW + lift)     # T R B L: x0 쪽(T·L)이 들려요
    prism(d, X0, Y0, X1, Y1, (BH,) * 4, z, WOOD3, WOOD2, WOOD)
    for i, (dx, hh, c) in enumerate(((0, 4, CLOTH2), (.18, 4, CLOTH), (.38, 3, CLOTH3))):
        zz = tuple(v + BH + i * 4 - (i * 2 if j in (1, 2) else 0) for j, v in enumerate(z))
        prism(d, X0 + dx + .15, Y0 - .05, X1 - dx + .15, Y1 + .05, (hh,) * 4, zz, c, shade(c, .8), shade(c, .92))
    for y in (Y0 + .5, Y1 - .5): wheel(d, *up(P(X1, y), ZW - 1))
    outline(img); return img


def cart_fall():
    """옆으로 쓰러짐: 열린 짐칸이 이쪽을 보고(어둡게 빈 속), 바퀴는 위로 · 지푸라기가 흩어져요"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # 흩어진 지푸라기 (땅)
    for (x, y) in ((1.4, -.6), (1.9, .3), (1.5, 1.0), (2.2, -1.1), (1.1, 1.6), (2.4, .9)):
        cx, cy = P(x, y); d.line([(cx - 3, cy), (cx + 3, cy - 1)], fill=hexc('#d8b860')); d.line([(cx - 1, cy + 1), (cx + 3, cy + 1)], fill=hexc('#b8983e'))
    xa, xb = X0 + .5, X1 + 1.0       # 쓰러진 몸통: 높이 11px (원래 폭)
    prism(d, xa, Y0, xb, Y1, (11,) * 4, (0,) * 4, WOOD2, WOOD, WOOD3)
    # 열린 쪽(남동 면) = 짐칸 속: 어두운 빈 칸
    R0, B0 = P(xb, Y0 + .2), P(xb, Y1 - .2)
    poly(d, [up(R0, 2), up(B0, 2), up(B0, 9), up(R0, 9)], hexc('#1e1424'))
    for k in range(3): cx, cy = up(P(xb, -0.6 + k * .6), 3); d.line([(cx - 2, cy), (cx + 2, cy - 1)], fill=hexc('#d8b860'))
    # 위로 들린 바퀴 두 개 (윗면 먼 쪽)
    for y in (Y0 + .5, Y1 - .5):
        cx, cy = up(P(xa + .15, y), 15); wheel(d, cx, cy, 4)
    # 부러진 끌채
    d.line([tuple(map(round, up(P(xa + .6, Y0), 6))), tuple(map(round, up(P(xa + 1.4, Y0 - 1.2), 1)))], fill=WOOD2, width=2)
    outline(img); return img


def tarp():
    img = Image.new('RGBA', (40, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    poly(d, [(3, 18), (14, 6), (30, 4), (37, 12), (26, 22), (10, 25)], CLOTH)
    poly(d, [(14, 6), (30, 4), (37, 12), (24, 12)], CLOTH3)
    d.line([(8, 20), (20, 9)], fill=ROPE); d.line([(18, 21), (30, 10)], fill=ROPE)
    outline(img); return img


def puffs():
    img = Image.new('RGBA', (48 * 3, 28), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for f, (n, r0, a) in enumerate(((5, 4, 200), (7, 6, 150), (8, 8, 90))):
        ox = f * 48 + 24
        for k in range(n):
            t = k / n * 6.283; x, y = ox + math.cos(t) * r0 * 1.6, 16 + math.sin(t) * r0 * .5 - k % 2 * 2
            rr = 3 + f
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(200, 188, 168, a))
    return img


def shadows():
    """먼지 뭉치 그림자 8개: 누군지 모르게 동글동글 털뭉치 + 노랗게 빛나는 두 눈 (크기·모양이 조금씩 달라요)"""
    import random
    out = Image.new('RGBA', (14 * 8, 14), (0, 0, 0, 0)); o = out.load()
    for i in range(8):
        rnd = random.Random(i * 31 + 7); r = 3.6 + (i % 3) * .7; cx, cy = 7 + i * 14, 9.2 - (i % 3) * .4
        for y in range(14):
            for x in range(i * 14, i * 14 + 14):
                d = math.hypot((x + .5 - cx) / r, (y + .5 - cy) / (r * .9))
                if d <= 1 or (d <= 1.35 and rnd.random() < .45):   # 가장자리가 보송보송 삐죽
                    o[x, y] = (16, 10, 26, 235) if d <= 1 else (30, 20, 44, 190)
        ey = int(cy - r * .25); ex = int(cx) - 2 + (i % 2)
        for x in (ex, ex + 3 - (i % 3 == 2)): o[x, ey] = (255, 230, 120, 255)
    return out


if __name__ == '__main__':
    meta = {}
    for name, fn in (('up', cart_up), ('tilt', cart_tilt), ('fall', cart_fall)):
        im = fn(); bb = im.getbbox(); im = im.crop(bb); im.save(f'out/cart_{name}.png')
        ax, ay = P(.5, .5)
        meta[name] = dict(sw=im.width, sh=im.height, ax=round(ax - bb[0]), ay=round(ay - bb[1]))
    tarp().save('out/cart_tarp.png'); puffs().save('out/cart_puff.png'); shadows().save('out/cart_shadows.png')
    json.dump(meta, open('out/cart.json', 'w')); print(meta)
