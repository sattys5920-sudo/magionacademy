# 유령 열차 그림: 등불 마을 강 위에 떠서 오는 열차 + 강가 승강장 (아이소 8:4, world.py 그림체)
#   python3 gtrain_art.py → out/gtrain_train.png · out/gtrain_platform.png · out/gtrain.json (소품 기준점)
#   열차는 강(x 0~10) 위 x 3.6~6.2, y 45~61 에 떠 있어요 (다리 남쪽). 승강장은 강가 x 9.2~11.4, y 51.5~57.5 앞(기관차)이 남서쪽(y 큰 쪽)
import json, math, os
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
OX, OY = 892, 160          # 등불 마을(town) 지도의 원점
W, H = 1648, 1004
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#120A18')

BODY = hexc('#3A2A55'); BODY_R = hexc('#463466'); BODY_L = hexc('#2E2246')
ROOF = hexc('#2B1F45'); ROOF_HI = hexc('#9B7BFF'); TRIM = hexc('#E0C070')
WIN = hexc('#7AE0E0'); WIN_HI = hexc('#E8FFFF'); WIN_DK = hexc('#3C98A8')
X0, X1 = 3.6, 6.2
Z = 12                      # 떠 있는 높이(px)
DY = 30                     # 다리 남쪽 강가 (집·나무에 가리지 않는 빈 강가)


def poly(d, pts, c): d.polygon([tuple(map(round, p)) for p in pts], fill=c)


def outline(img, c=OUTL):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200: add.append((x, y)); break
    for x, y in add: a[x, y] = c


def glow_edge(img, col, alpha=110):
    a = img.load(); w, h = img.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][:3] == OUTL[:3] and a[x + dx, y + dy][3] == 255: add.append((x, y)); break
    for x, y in add: a[x, y] = col[:3] + (alpha,)


def rf(x1, y, v):           # 남동쪽 면(x = x1) 위의 점: y 칸, 높이 v
    return up(P(x1, y), v + Z)


def lf(x, y1, v):           # 남서쪽 면(y = y1) 위의 점
    return up(P(x, y1), v + Z)


def box(d, x0, y0, x1, y1, h, top, left, right, z0=0):
    T, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
    k = Z + z0
    poly(d, [up(L, k), up(B, k), up(B, k + h), up(L, k + h)], left)
    poly(d, [up(R, k), up(B, k), up(B, k + h), up(R, k + h)], right)
    poly(d, [up(T, k + h), up(R, k + h), up(B, k + h), up(L, k + h)], top)


def quad_r(d, x1, ya, yb, v0, v1, c):
    poly(d, [rf(x1, ya, v0), rf(x1, yb, v0), rf(x1, yb, v1), rf(x1, ya, v1)], c)


SEATED = [0]                # 창문마다 그림자 승객을 그릴지 (탑승 중 그림): 남은 수만큼 앞 창부터 채워요


def window_r(d, x1, ya, yb, v0, v1, seat=True):
    quad_r(d, x1, ya, yb, v0, v1, WIN_DK)
    quad_r(d, x1, ya + .08, yb - .08, v0 + 1, v1 - 1, WIN)
    quad_r(d, x1, ya + .12, ya + .32, v1 - 4, v1 - 1, WIN_HI)
    if seat and SEATED[0] > 0:
        SEATED[0] -= 1
        m = (ya + yb) / 2
        cx, cy = rf(x1, m, v0 + 5)
        sil = hexc('#2A1E40')
        d.ellipse([cx - 2.5, cy - 3, cx + 2.5, cy + 2], fill=sil)
        poly(d, [rf(x1, m - .22, v0 + 1), rf(x1, m + .22, v0 + 1), rf(x1, m + .14, v0 + 3), rf(x1, m - .14, v0 + 3)], sil)


def wheel(d, x1, y, r=3.2):
    cx, cy = rf(x1, y, -1)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexc('#140D1E'))
    d.ellipse([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], outline=hexc('#7AE0E0'))
    d.point((round(cx), round(cy)), fill=hexc('#7AE0E0'))


def carriage(d, ya, yb, seats=4):
    h = 18
    box(d, X0, ya, X1, yb, h, ROOF, BODY_L, BODY_R)
    # 지붕: 가운데가 조금 높은 둥근 지붕
    box(d, X0 + .35, ya + .2, X1 - .35, yb - .2, 3, shade(ROOF, 1.15), shade(ROOF, .8), shade(ROOF, .95), z0=h)
    d.line([tuple(map(round, up(P(X0 + .35, yb - .2), Z + h + 3))), tuple(map(round, up(P(X1 - .35, yb - .2), Z + h + 3)))], fill=ROOF_HI)
    d.line([tuple(map(round, up(P(X1 - .35, ya + .2), Z + h + 3))), tuple(map(round, up(P(X1 - .35, yb - .2), Z + h + 3)))], fill=ROOF_HI)
    # 금빛 띠 + 아랫단
    quad_r(d, X1, ya, yb, 4, 5, TRIM)
    quad_r(d, X1, ya, yb, 0, 2, shade(BODY_R, .7))
    # 창문
    L = yb - ya; step = L / seats
    for k in range(seats):
        a = ya + step * k + step * .2
        window_r(d, X1, a, a + step * .6, 7, 15)
    # 끝면 창 하나
    c0, c1 = lf(X0 + .7, yb, 8), lf(X1 - .7, yb, 8)
    poly(d, [c0, c1, lf(X1 - .7, yb, 14), lf(X0 + .7, yb, 14)], WIN_DK)
    for y in (ya + .7, yb - .7): wheel(d, X1, y)


def engine(d, ya, yb):
    # 운전실 (뒤쪽, 높아요)
    cab_b = ya + 2.0
    box(d, X0, ya, X1, cab_b, 22, ROOF, BODY_L, BODY_R)
    box(d, X0 - .15, ya - .15, X1 + .15, cab_b + .15, 2, shade(ROOF, 1.2), shade(ROOF, .8), shade(ROOF, .95), z0=22)
    window_r(d, X1, ya + .35, cab_b - .35, 10, 18, seat=False)
    quad_r(d, X1, ya, cab_b, 4, 5, TRIM)
    # 보일러 (앞쪽 원통 느낌: 좁은 상자 + 띠)
    bx0, bx1 = X0 + .3, X1 - .3
    box(d, bx0, cab_b, bx1, yb, 14, shade(BODY, 1.1), BODY_L, BODY_R)
    for y in (cab_b + 1.0, cab_b + 2.2, cab_b + 3.4):
        quad_r(d, bx1, y, y + .18, 0, 14, TRIM)
    # 굴뚝 + 유령 연기
    cx, cy = up(P((bx0 + bx1) / 2, yb - 1.1), Z + 14)
    d.rectangle([cx - 3, cy - 11, cx + 3, cy], fill=hexc('#2B1F45'))
    d.rectangle([cx - 3, cy - 11, cx - 1, cy], fill=hexc('#3A2A55'))
    d.rectangle([cx - 5, cy - 14, cx + 5, cy - 11], fill=hexc('#4E3C72'))
    # 앞면: 등불(헤드라이트)
    hx, hy = lf((bx0 + bx1) / 2, yb, 8)
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=hexc('#FFD866'))
    d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=hexc('#FFF6C8'))
    # 배장기(앞 아래 쇠 날개)
    a, b = lf(X0 + .2, yb + .5, -2), lf(X1 - .2, yb + .5, -2)
    poly(d, [lf(X0 + .3, yb, 3), lf(X1 - .3, yb, 3), b, a], hexc('#4E3C72'))
    for y in (cab_b + .6, yb - 1.6, yb - .6): wheel(d, bx1, y, 3.6 if y < yb - 1 else 3.0)
    return (cx, cy - 14)


def smoke(img, at):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x, y = at
    for i, (dx, dy, r) in enumerate([(0, -4, 5), (5, -11, 6), (12, -17, 7), (21, -21, 6), (29, -24, 4)]):
        a = 170 - i * 28
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(206, 196, 232, a))
        d.ellipse([x + dx - r + 2, y + dy - r + 1, x + dx + 1, y + dy - 1], fill=(240, 236, 255, a))
    return lay


def mist(size):
    lay = Image.new('RGBA', size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(17):
        y = 14.6 + k + DY
        cx, cy = P((X0 + X1) / 2, y)
        rx, ry = 20 + (k % 3) * 4, 6 + (k % 2) * 2
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(189, 176, 214, 46))
    for k in range(9):
        cx, cy = P((X0 + X1) / 2 + .2, 15.5 + k * 2 + DY)
        d.ellipse([cx - 11, cy - 3, cx + 11, cy + 3], fill=(225, 220, 245, 60))
    return lay


def train(seated=0):
    SEATED[0] = seated
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    carriage(d, 15.0 + DY, 19.6 + DY)
    # 연결 고리
    for y in (19.6 + DY, 24.8 + DY):
        poly(d, [rf(X1 - .6, y, 6), rf(X1 - .6, y + .6, 6), rf(X1 - .6, y + .6, 9), rf(X1 - .6, y, 9)], hexc('#140D1E'))
    carriage(d, 20.2 + DY, 24.8 + DY)
    top = engine(d, 25.4 + DY, 31.0 + DY)
    outline(img)
    glow_edge(img, hexc('#7AE0E0'), 120)
    base = mist(img.size)
    base.alpha_composite(img)
    base.alpha_composite(smoke(img, top))
    bb = base.getbbox()
    return base.crop(bb), bb


def platform():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x0, x1, y0, y1, h = 9.2, 11.4, 21.5 + DY, 27.5 + DY, 4
    T, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
    WD = hexc('#6E5040'); WD2 = hexc('#5A4034'); WD3 = hexc('#82604C')
    poly(d, [L, B, up(B, h), up(L, h)], WD2)
    poly(d, [R, B, up(B, h), up(R, h)], shade(WD, .9))
    poly(d, [up(T, h), up(R, h), up(B, h), up(L, h)], WD)
    k = y0 + .5
    while k < y1:
        d.line([tuple(map(round, up(P(x0, k), h))), tuple(map(round, up(P(x1, k), h)))], fill=WD2)
        k += .5
    d.line([tuple(map(round, up(P(x0, y1), h))), tuple(map(round, up(P(x1, y1), h)))], fill=WD3)
    # 기둥 + 청록 등불
    for y in (y0 + .7, y1 - .7):
        cx, cy = up(P(x1 - .3, y), h)
        d.rectangle([cx - 1, cy - 26, cx, cy], fill=hexc('#2A2230'))
        d.line([(cx, cy - 26), (cx - 5, cy - 28)], fill=hexc('#2A2230'))
        d.ellipse([cx - 10, cy - 30, cx - 3, cy - 22], fill=hexc('#7AE0E0')); d.ellipse([cx - 8, cy - 28, cx - 5, cy - 24], fill=hexc('#E8FFFF'))
    # 표지판 (유령 얼굴 문양)
    cx, cy = up(P(x1 - .2, (y0 + y1) / 2), h)
    d.rectangle([cx - 1, cy - 18, cx, cy], fill=hexc('#2A2230')); d.rectangle([cx + 9, cy - 13, cx + 10, cy + 4], fill=hexc('#2A2230'))
    poly(d, [(cx - 3, cy - 24), (cx + 13, cy - 19), (cx + 13, cy - 9), (cx - 3, cy - 14)], hexc('#211733'))
    poly(d, [(cx - 2, cy - 22), (cx + 12, cy - 18), (cx + 12, cy - 10), (cx - 2, cy - 14)], hexc('#2B1F45'))
    d.ellipse([cx + 2, cy - 21, cx + 8, cy - 13], fill=hexc('#E8FFFF'))
    d.point((cx + 4, cy - 18), fill=hexc('#211733')); d.point((cx + 6, cy - 17), fill=hexc('#211733'))
    outline(img)
    bb = img.getbbox()
    return img.crop(bb), bb


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    meta = {}
    for name, fn, tile in (('train', train, (5, 31 + DY)), ('train_in', lambda: train(6), (5, 31 + DY)), ('platform', platform, (11, 27 + DY))):
        spr, bb = fn()
        spr.save(f'out/gtrain_{name}.png')
        ax, ay = P(tile[0] + .5, tile[1] + .5)
        meta[name] = dict(x=tile[0], y=tile[1], sw=spr.width, sh=spr.height, ax=round(ax - bb[0]), ay=round(ay - bb[1]), bx=bb[0], by=bb[1])
        print(name, spr.size, meta[name])
    json.dump(meta, open('out/gtrain.json', 'w'))
