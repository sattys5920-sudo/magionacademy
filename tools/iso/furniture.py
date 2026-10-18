# 개인 방 가구 50종: out/furn.png (한 줄 그림) + out/furn.json (이름·값·크기·그림 위치)
# 각 가구는 타일 (1,1)을 기준으로 그려서, 게임에서 놓은 타일의 위 꼭짓점에 ax, ay를 맞춰 그려요.
import json
from interiors import Room, hexc, shade, OUTL
from PIL import Image, ImageDraw

def H(c): return hexc(c) if isinstance(c, str) else c
def bx(R, img, tx, ty, w, dp, h, c, lift=0, top=None):
    c = H(c); R.box(img, tx, ty, w, dp, h, H(top) if top else shade(c, 1.08), shade(c, .62), shade(c, .82), lift)
def C(R, tx, ty, dy=0): x, y = R.P(tx, ty); return x, y - dy
def ell(d, x, y, rx, ry, c): d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=H(c))
def face(d, x, y, eye='#2A1830', blush='#FFB0C4', w=3):
    d.point((x - w, y), fill=H(eye)); d.point((x + w, y), fill=H(eye)); d.point((x - w - 1, y + 1), fill=H(blush)); d.point((x + w + 1, y + 1), fill=H(blush))

# ---------- 인형 ----------
def doll(kind, body, belly=None, scale=1.0):
    def f(R, img, d):
        x, y = C(R, 1.5, 1.5); s = scale
        if kind == 'bat': d.polygon([(x - 13 * s, y - 14 * s), (x - 4 * s, y - 10 * s), (x - 5 * s, y - 4 * s)], fill=H(shade(H(body), .8))); d.polygon([(x + 13 * s, y - 14 * s), (x + 4 * s, y - 10 * s), (x + 5 * s, y - 4 * s)], fill=H(shade(H(body), .8)))
        ell(d, x, y - 5 * s, 6 * s, 5 * s, body)                         # 몸
        if belly: ell(d, x, y - 4 * s, 3.5 * s, 3 * s, belly)
        hy = y - 14 * s; ell(d, x, hy, 7 * s, 6 * s, body)                 # 머리
        if kind == 'bear': ell(d, x - 6 * s, hy - 5 * s, 2.5 * s, 2.5 * s, body); ell(d, x + 6 * s, hy - 5 * s, 2.5 * s, 2.5 * s, body); ell(d, x, hy + 2 * s, 2.5 * s, 1.6 * s, belly or '#F2E2C4')
        if kind == 'cat': d.polygon([(x - 7 * s, hy - 2 * s), (x - 6 * s, hy - 9 * s), (x - 2 * s, hy - 5 * s)], fill=H(body)); d.polygon([(x + 7 * s, hy - 2 * s), (x + 6 * s, hy - 9 * s), (x + 2 * s, hy - 5 * s)], fill=H(body))
        if kind == 'bunny': ell(d, x - 3 * s, hy - 9 * s, 1.6 * s, 5 * s, body); ell(d, x + 3 * s, hy - 9 * s, 1.6 * s, 5 * s, body); ell(d, x - 3 * s, hy - 9 * s, .7 * s, 3.5 * s, '#FFB0C4')
        if kind == 'bat': d.polygon([(x - 6 * s, hy - 3 * s), (x - 5 * s, hy - 10 * s), (x - 2 * s, hy - 5 * s)], fill=H(body)); d.polygon([(x + 6 * s, hy - 3 * s), (x + 5 * s, hy - 10 * s), (x + 2 * s, hy - 5 * s)], fill=H(body))
        if kind == 'ghost': d.rectangle([x - 7 * s, hy, x + 7 * s, y - 2 * s], fill=H(body)); [ell(d, x + k * s, y - 2 * s, 2.4 * s, 2 * s, body) for k in (-5, 0, 5)]
        if kind == 'pumpkin': [ell(d, x + k * s, hy, 4 * s, 6 * s, body) for k in (-4, 4)]; ell(d, x, hy, 4 * s, 6 * s, body); d.rectangle([x - 1, hy - 8 * s, x, hy - 6 * s], fill=H('#4A7A2E'))
        if kind == 'witch': d.polygon([(x - 9 * s, hy - 3 * s), (x + 9 * s, hy - 3 * s), (x + 2 * s, hy - 7 * s)], fill=H('#3A2A5E')); d.polygon([(x - 4 * s, hy - 5 * s), (x + 4 * s, hy - 5 * s), (x + 3 * s, hy - 15 * s)], fill=H('#3A2A5E')); ell(d, x, hy + 1 * s, 5 * s, 4 * s, '#F2C6A0'); d.rectangle([x - 6 * s, hy - 3 * s, x - 4 * s, hy + 3 * s], fill=H('#C86A3A')); d.rectangle([x + 4 * s, hy - 3 * s, x + 6 * s, hy + 3 * s], fill=H('#C86A3A'))
        if kind == 'dragon': d.polygon([(x - 7 * s, y - 8 * s), (x - 14 * s, y - 14 * s), (x - 9 * s, y - 4 * s)], fill=H(shade(H(body), .8))); d.polygon([(x + 7 * s, y - 8 * s), (x + 14 * s, y - 14 * s), (x + 9 * s, y - 4 * s)], fill=H(shade(H(body), .8))); [d.polygon([(x + k * s - 1, hy - 5 * s), (x + k * s + 1, hy - 5 * s), (x + k * s, hy - 9 * s)], fill=H('#F2E2A0')) for k in (-3, 3)]
        if kind == 'owl': d.polygon([(x - 7 * s, hy - 2 * s), (x - 7 * s, hy - 8 * s), (x - 3 * s, hy - 5 * s)], fill=H(body)); d.polygon([(x + 7 * s, hy - 2 * s), (x + 7 * s, hy - 8 * s), (x + 3 * s, hy - 5 * s)], fill=H(body)); ell(d, x - 3 * s, hy, 2.5 * s, 2.5 * s, '#FFFCF0'); ell(d, x + 3 * s, hy, 2.5 * s, 2.5 * s, '#FFFCF0'); d.point((x, hy + 2 * s), fill=H('#F0B040'))
        if kind == 'pumpkin': face(d, x, int(hy), eye='#3A2010', blush='#FFD27A')
        elif kind != 'witch': face(d, x, int(hy + (1 if kind == 'owl' else 0)), w=max(2, int(3 * s)))
        else: face(d, x, int(hy + 1 * s), w=2)
    return f

# ---------- 가구 ----------
def chair(col):
    def f(R, img, d): bx(R, img, 1.2, 1.2, .6, .6, 7, '#8A5636'); bx(R, img, 1.2, 1.2, .6, .6, 2, col, lift=7); bx(R, img, 1.2, 1.2, .12, .6, 14, '#7A4A2E', lift=0)
    return f
def rocking(R, img, d):
    x, y = C(R, 1.5, 1.5); d.arc([x - 10, y - 6, x + 10, y + 4], 20, 160, fill=H('#5E3826'), width=2)
    bx(R, img, 1.2, 1.2, .6, .6, 3, '#C86A8A', lift=6); bx(R, img, 1.15, 1.2, .12, .6, 13, '#8A5636', lift=6)
def sofa2(col):
    def f(R, img, d):
        c = H(col); bx(R, img, 1, 1.2, 2, .8, 6, c); bx(R, img, 1, 1.75, 2, .25, 13, shade(c, 1.1))
        for xx in (.95, 2.9): bx(R, img, xx, 1.2, .15, .8, 9, shade(c, .9))
    return f
def cushions(R, img, d):
    x, y = C(R, 1.5, 1.5)
    for (dx, dy, c) in ((-6, 0, '#C86A8A'), (5, -1, '#6A8AD8'), (0, -5, '#F6C83A')): ell(d, x + dx, y + dy - 2, 6, 3, c); ell(d, x + dx, y + dy - 3, 4, 1.5, shade(H(c), 1.2))
def tea_table(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 9, x, y], fill=H('#5E3826')); ell(d, x, y - 10, 9, 4, '#8A5636'); ell(d, x, y - 11, 8, 3, '#A86A42')
    d.rectangle([x - 4, y - 15, x - 1, y - 12], fill=H('#F2EEE4')); d.rectangle([x + 2, y - 14, x + 5, y - 12], fill=H('#FFD0DA'))
def desk(R, img, d):
    bx(R, img, 1, 1.2, 2, .7, 11, '#7A4A2E'); x, y = C(R, 1.6, 1.5, 11)
    d.rectangle([x - 3, y - 3, x + 2, y - 1], fill=H('#E8DCC8')); d.rectangle([x + 6, y - 6, x + 7, y - 1], fill=H('#F2E6C8')); d.point((x + 6, y - 7), fill=H('#FFD27A'))
def bookcase(R, img, d):
    bx(R, img, 1.1, 1.3, .8, .6, 30, '#5E3826'); x0, y0 = C(R, 1.1, 1.9)
    for row in range(3):
        for k in range(5): d.rectangle([x0 + 1 + k * 2, y0 - 8 - row * 9 - k % 2, x0 + 2 + k * 2, y0 - 3 - row * 9 - (k // 2) % 2 - (k * 0)], fill=H(['#C86A3A', '#5A8AD8', '#6AAE5A', '#E8C060', '#A86AE8'][(k + row) % 5]))
def wardrobe(R, img, d):
    bx(R, img, 1.1, 1.2, .8, .7, 32, '#8A5A3A'); x, y = C(R, 1.1, 1.9)
    d.line([(x + 3, y - 30), (x + 3, y - 2)], fill=H('#4A2A1C')); d.point((x + 2, y - 16), fill=H('#E8C060')); d.point((x + 4, y - 15), fill=H('#E8C060'))
def vanity(R, img, d):
    bx(R, img, 1.1, 1.3, .8, .6, 11, '#F2E2EC'); x, y = C(R, 1.5, 1.4, 11)
    ell(d, x, y - 8, 5, 7, '#C49446'); ell(d, x, y - 8, 4, 6, '#A8C8E8'); d.line([(x - 2, y - 11), (x + 1, y - 8)], fill=H('#E8F4FF'))
def chest(R, img, d):
    bx(R, img, 1.15, 1.25, .7, .55, 7, '#7A4A2E'); bx(R, img, 1.15, 1.25, .7, .55, 3, '#C49446', lift=7)
    x, y = C(R, 1.5, 1.5, 9); ell(d, x, y - 3, 3, 2, '#F6D24A'); d.point((x + 2, y - 5), fill=H('#FFFFFF'))
def books(R, img, d):
    for k, c in enumerate(('#C86A3A', '#5A8AD8', '#6AAE5A', '#A86AE8')): bx(R, img, 1.25 + k * .03, 1.25 - k * .02, .5, .4, 2, c, lift=k * 2)
def candlestand(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 16, x, y], fill=H('#C49446')); ell(d, x, y, 4, 1.5, '#A8823A'); d.rectangle([x - 2, y - 22, x + 1, y - 16], fill=H('#F2E6C8')); d.point((x - 1, y - 23), fill=H('#FFD27A')); d.point((x - 1, y - 24), fill=H('#FF8A3A'))
def jacklantern(R, img, d):
    x, y = C(R, 1.5, 1.5)
    for k in (-4, 4): ell(d, x + k, y - 6, 4, 6, '#F08A30')
    ell(d, x, y - 6, 4, 6, '#F08A30'); d.rectangle([x - 1, y - 14, x, y - 11], fill=H('#4A7A2E'))
    for k in (-3, 2): d.polygon([(x + k, y - 7), (x + k + 2, y - 7), (x + k + 1, y - 9)], fill=H('#FFE07A'))
    d.line([(x - 3, y - 4), (x + 3, y - 4)], fill=H('#FFE07A'))
def mushlamp(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 12, x + 1, y], fill=H('#F2E6C8')); ell(d, x, y - 14, 8, 4, '#C86AE8'); ell(d, x - 3, y - 15, 1.5, 1, '#FFE8FF'); ell(d, x + 3, y - 14, 1, 1, '#FFE8FF')
def stove(R, img, d):
    bx(R, img, 1.2, 1.2, .6, .6, 12, '#3A3440'); x, y = C(R, 1.5, 1.8); ell(d, x - 1, y - 6, 3, 2, '#FF8A3A'); d.rectangle([x + 1, y - 30, x + 3, y - 12], fill=H('#3A3440'))
def plant(leaf, pot='#B86A3A', flower=None, tall=1.0):
    def f(R, img, d):
        x, y = C(R, 1.5, 1.5); d.polygon([(x - 4, y - 7), (x + 4, y - 7), (x + 3, y), (x - 3, y)], fill=H(pot))
        for dx, dy, r in ((-4, -12, 4), (4, -13, 4), (0, -17, 5), (-1, -10, 3)): ell(d, x + dx, y + dy * tall, r, r, leaf)
        if flower: [d.point((x + a, y + b * tall), fill=H(flower)) for a, b in ((-4, -14), (3, -16), (0, -20), (5, -11))]
    return f
def cactus(R, img, d):
    x, y = C(R, 1.5, 1.5); d.polygon([(x - 4, y - 6), (x + 4, y - 6), (x + 3, y), (x - 3, y)], fill=H('#C86A3A'))
    d.rectangle([x - 2, y - 18, x + 1, y - 6], fill=H('#5E9A4A')); d.rectangle([x - 6, y - 14, x - 4, y - 9], fill=H('#5E9A4A')); d.rectangle([x - 4, y - 10, x - 2, y - 9], fill=H('#5E9A4A')); d.point((x - 1, y - 19), fill=H('#FF9ACA'))
def vase(R, img, d):
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 4, 3, 4, '#6A8AD8'); d.rectangle([x - 1, y - 9, x, y - 6], fill=H('#6A8AD8'))
    for dx, dy, c in ((-3, -13, '#FF7A9A'), (2, -14, '#FFE07A'), (0, -16, '#C86AE8')): ell(d, x + dx, y + dy, 2, 2, c); d.line([(x, y - 8), (x + dx, y + dy)], fill=H('#4E8A4A'))
def tree(R, img, d):
    x, y = C(R, 1.5, 1.5); d.polygon([(x - 5, y - 6), (x + 5, y - 6), (x + 4, y), (x - 4, y)], fill=H('#8A8494')); d.rectangle([x - 1, y - 20, x, y - 6], fill=H('#6A4428'))
    for dx, dy, r in ((-6, -24, 6), (5, -25, 6), (0, -31, 7)): ell(d, x + dx, y + dy, r, r, '#4E8A4A')
    for dx, dy in ((-5, -27), (3, -32), (6, -22)): d.point((x + dx, y + dy), fill=H('#FF9A4A'))
def crystal(R, img, d):
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.3, 1.3, .4, .4, 6, '#5E3826'); ell(d, x, y - 12, 5, 5, '#B88AFF'); ell(d, x - 2, y - 14, 1.5, 1.5, '#F2E8FF')
def cauldron(R, img, d):
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 4, 8, 6, '#2A2430'); ell(d, x, y - 8, 7, 2.5, '#6AD8A8'); d.point((x - 2, y - 10), fill=H('#C8FFE8')); d.point((x + 3, y - 11), fill=H('#C8FFE8'))
def brooms(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 9, y - 26, x + 9, y - 24], fill=H('#5E3826'))
    for k in range(3): xx = x - 6 + k * 6; d.line([(xx, y - 26), (xx, y - 7)], fill=H('#8A5A3A'), width=2); d.polygon([(xx - 3, y - 9), (xx + 3, y - 9), (xx + 4, y), (xx - 4, y)], fill=H('#C8A84A'))
def potion_case(R, img, d):
    bx(R, img, 1.1, 1.3, .8, .6, 26, '#4A2A3A'); x, y = C(R, 1.1, 1.9)
    for row in range(3):
        for k in range(3): xx, yy = x + 1 + k * 2, y - 6 - row * 8 - k; d.rectangle([xx, yy - 3, xx + 1, yy], fill=H(['#C86AE8', '#6AD8A8', '#FF7A5C', '#5AA8FF', '#FFE07A'][(k + row * 2) % 5]))
def telescope(R, img, d):
    x, y = C(R, 1.5, 1.5)
    for dx in (-5, 0, 5): d.line([(x, y - 10), (x + dx, y)], fill=H('#5E3826'))
    d.line([(x - 6, y - 8), (x + 7, y - 18)], fill=H('#C49446'), width=3); d.point((x + 8, y - 19), fill=H('#A8C8E8'))
def globe(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 6, x, y], fill=H('#5E3826')); ell(d, x, y, 4, 1.5, '#5E3826'); ell(d, x, y - 12, 6, 6, '#4A8AD8')
    d.arc([x - 7, y - 19, x + 7, y - 5], 200, 340, fill=H('#C49446')); ell(d, x - 2, y - 13, 2, 2, '#6AAE5A'); ell(d, x + 3, y - 10, 1.5, 1, '#6AAE5A')
def clock(R, img, d):
    bx(R, img, 1.25, 1.3, .5, .4, 32, '#6A3E26'); x, y = C(R, 1.25, 1.7); ell(d, x + 3, y - 24, 3, 3, '#F2E6C8'); d.line([(x + 3, y - 24), (x + 3, y - 26)], fill=H('#2A1830')); d.line([(x + 3, y - 24), (x + 4, y - 24)], fill=H('#2A1830'))
    d.line([(x + 3, y - 18), (x + 3, y - 10)], fill=H('#C49446')); ell(d, x + 3, y - 9, 1.5, 1.5, '#E8C060')
def gramophone(R, img, d):
    bx(R, img, 1.2, 1.3, .6, .5, 7, '#7A4A2E'); x, y = C(R, 1.5, 1.5, 7); d.line([(x, y - 2), (x + 2, y - 9)], fill=H('#C49446'))
    d.polygon([(x + 1, y - 9), (x + 9, y - 18), (x + 12, y - 12)], fill=H('#E8C060')); ell(d, x + 10, y - 15, 2, 3, '#A8823A')
def piano(R, img, d):
    bx(R, img, 1, 1.2, 2, .8, 12, '#2A1C2A'); bx(R, img, 1, 1.75, 2, .25, 13, '#F2EEE4', top='#F2EEE4'); bx(R, img, 1, 1.2, 2, .25, 22, '#2A1C2A')
def easel(R, img, d):
    x, y = C(R, 1.5, 1.5); d.line([(x - 5, y), (x, y - 22)], fill=H('#8A5A3A'), width=2); d.line([(x + 5, y), (x, y - 22)], fill=H('#8A5A3A'), width=2)
    d.rectangle([x - 7, y - 20, x + 6, y - 9], fill=H('#F2EEE4')); ell(d, x - 2, y - 15, 3, 2, '#5AA8FF'); ell(d, x + 2, y - 13, 2, 2, '#FFB0C4'); d.point((x + 3, y - 17), fill=H('#F6C83A'))
def rug(shape, c1, c2, w=2, dp=2):
    def f(R, img, d):
        pts = [R.P(1, 1), R.P(1 + w, 1), R.P(1 + w, 1 + dp), R.P(1, 1 + dp)]
        if shape == 'round':
            x, y = C(R, 1 + w / 2, 1 + dp / 2); ell(d, x, y, w * 7, dp * 3.5, c1); ell(d, x, y, w * 5, dp * 2.4, c2); ell(d, x, y, w * 2.5, dp * 1.2, c1)
        elif shape == 'star':
            x, y = C(R, 1 + w / 2, 1 + dp / 2); d.polygon(pts, fill=H(c1)); import math
            st = [(x + (9 if k % 2 == 0 else 4) * math.cos(-math.pi / 2 + k * math.pi / 5) * 1.6, y + (9 if k % 2 == 0 else 4) * math.sin(-math.pi / 2 + k * math.pi / 5) * .8) for k in range(10)]
            d.polygon(st, fill=H(c2))
        elif shape == 'check':
            for i in range(w * 2):
                for j in range(dp * 2):
                    q = [R.P(1 + i / 2, 1 + j / 2), R.P(1 + (i + 1) / 2, 1 + j / 2), R.P(1 + (i + 1) / 2, 1 + (j + 1) / 2), R.P(1 + i / 2, 1 + (j + 1) / 2)]
                    d.polygon(q, fill=H(c1 if (i + j) % 2 else c2))
        elif shape == 'pumpkin':
            x, y = C(R, 1 + w / 2, 1 + dp / 2)
            for k in (-6, 6): ell(d, x + k, y, 8, 5, c1)
            ell(d, x, y, 9, 6, c1); ell(d, x, y, 5, 3, c2)
    return f
def skull(R, img, d):
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.3, 1.3, .4, .4, 5, '#5E3826'); ell(d, x, y - 10, 5, 4.5, '#F2EEE4'); d.rectangle([x - 3, y - 7, x + 2, y - 5], fill=H('#F2EEE4'))
    ell(d, x - 2, y - 10, 1.2, 1.4, '#2A1830'); ell(d, x + 2, y - 10, 1.2, 1.4, '#2A1830'); d.point((x + 4, y - 12), fill=H('#FF9ACA'))
def balloons(R, img, d):
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 1, 3, 1.5, '#5E3826')
    for dx, dy, c in ((-5, -26, '#FF7A9A'), (4, -28, '#6AB8FF'), (0, -33, '#F6C83A'), (6, -21, '#A86AE8')): d.line([(x, y - 1), (x + dx, y + dy + 4)], fill=H('#E8E0F0')); ell(d, x + dx, y + dy, 3.5, 4.5, c); d.point((x + dx - 1, y + dy - 2), fill=H('#FFFFFF'))
def candy_jar(R, img, d):
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 6, 6, 6, '#E8F4FF'); d.rectangle([x - 4, y - 14, x + 3, y - 11], fill=H('#C86A8A'))
    for dx, dy, c in ((-2, -6, '#FF7A9A'), (2, -4, '#6AD8A8'), (0, -8, '#F6C83A'), (3, -8, '#A86AE8'), (-3, -3, '#5AA8FF')): ell(d, x + dx, y + dy, 1.5, 1.5, c)
def cake(R, img, d):
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 6, x, y], fill=H('#C49446')); ell(d, x, y - 6, 7, 2.5, '#E8C060')
    d.rectangle([x - 5, y - 13, x + 4, y - 7], fill=H('#FFD0DA')); ell(d, x, y - 13, 5, 2, '#FFF0F4'); d.point((x, y - 16), fill=H('#E8484C')); d.rectangle([x - 5, y - 10, x + 4, y - 10], fill=H('#FFFFFF'))
def fishbowl(R, img, d):
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.3, 1.3, .4, .4, 6, '#5E3826'); ell(d, x, y - 13, 6, 6, '#C8E8FF'); ell(d, x, y - 11, 5, 3.5, '#6AB8E8')
    ell(d, x - 1, y - 11, 2, 1, '#FF8A3A'); d.point((x + 1, y - 11), fill=H('#FF8A3A')); d.point((x - 3, y - 16), fill=H('#FFFFFF'))
def cattower(R, img, d):
    bx(R, img, 1.2, 1.2, .6, .6, 4, '#C8A878'); x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 20, x + 1, y - 4], fill=H('#D8C8A8'))
    bx(R, img, 1.15, 1.15, .7, .7, 3, '#C86A8A', lift=20); ell(d, x + 3, y - 26, 3, 2, '#6A5E86'); d.polygon([(x + 1, y - 28), (x + 2, y - 31), (x + 3, y - 28)], fill=H('#6A5E86'))
def coffin_sofa(R, img, d):
    bx(R, img, 1, 1.2, 2, .8, 6, '#3A1E2A'); bx(R, img, 1, 1.75, 2, .25, 15, '#4A1E2A'); x, y = C(R, 2, 2, 12)
    d.line([(x, y - 3), (x, y + 2)], fill=H('#C49446')); d.line([(x - 2, y - 1), (x + 2, y - 1)], fill=H('#C49446'))
# (id, 이름, 분류, 값, 아늑함, 가로, 세로, 막힘, 바닥에 깔림, 그리기)
ITEMS = [
  ('chair', '나무 의자', '가구', 40, 1, 1, 1, 1, 0, chair('#C86A8A')),
  ('rocking', '흔들의자', '가구', 180, 2, 1, 1, 1, 0, rocking),
  ('sofa', '푹신한 소파', '가구', 320, 3, 2, 1, 1, 0, sofa2('#8A5AD8')),
  ('cushions', '쿠션 더미', '가구', 90, 2, 1, 1, 0, 0, cushions),
  ('teatable', '둥근 티 테이블', '가구', 120, 2, 1, 1, 1, 0, tea_table),
  ('desk', '공부 책상', '가구', 200, 2, 2, 1, 1, 0, desk),
  ('bookcase', '책장', '가구', 220, 2, 1, 1, 1, 0, bookcase),
  ('wardrobe', '옷장', '가구', 260, 2, 1, 1, 1, 0, wardrobe),
  ('vanity', '화장대', '가구', 240, 2, 1, 1, 1, 0, vanity),
  ('chest', '보물 상자', '가구', 300, 2, 1, 1, 1, 0, chest),
  ('books', '마법서 더미', '마법', 60, 1, 1, 1, 0, 0, books),
  ('candle', '촛대', '조명', 30, 1, 1, 1, 1, 0, candlestand),
  ('jack', '호박 랜턴', '조명', 70, 1, 1, 1, 1, 0, jacklantern),
  ('mushlamp', '버섯 스탠드', '조명', 160, 2, 1, 1, 1, 0, mushlamp),
  ('stove', '작은 난로', '조명', 280, 3, 1, 1, 1, 0, stove),
  ('monstera', '몬스테라 화분', '식물', 80, 1, 1, 1, 1, 0, plant('#4E8A4A')),
  ('cactus', '선인장 화분', '식물', 50, 1, 1, 1, 1, 0, cactus),
  ('vase', '꽃병', '식물', 60, 1, 1, 1, 1, 0, vase),
  ('tree', '작은 귤나무', '식물', 350, 3, 1, 1, 1, 0, tree),
  ('crystal', '수정구', '마법', 400, 3, 1, 1, 1, 0, crystal),
  ('cauldron', '작은 솥', '마법', 250, 2, 1, 1, 1, 0, cauldron),
  ('brooms', '빗자루 걸이', '마법', 140, 1, 1, 1, 1, 0, brooms),
  ('potions', '물약 진열장', '마법', 380, 3, 1, 1, 1, 0, potion_case),
  ('telescope', '별 망원경', '마법', 420, 3, 1, 1, 1, 0, telescope),
  ('globe', '지구본', '장식', 180, 2, 1, 1, 1, 0, globe),
  ('clock', '괘종시계', '장식', 360, 2, 1, 1, 1, 0, clock),
  ('gramophone', '축음기', '장식', 450, 3, 1, 1, 1, 0, gramophone),
  ('piano', '작은 피아노', '가구', 800, 5, 2, 1, 1, 0, piano),
  ('easel', '그림 이젤', '장식', 170, 2, 1, 1, 1, 0, easel),
  ('bear', '곰 인형', '인형', 100, 2, 1, 1, 0, 0, doll('bear', '#B8845A', '#E8C8A0')),
  ('catdoll', '고양이 인형', '인형', 100, 2, 1, 1, 0, 0, doll('cat', '#6A5E86', '#8478A2')),
  ('batdoll', '박쥐 인형', '인형', 110, 2, 1, 1, 0, 0, doll('bat', '#7A6A96', '#B4A8CC')),
  ('ghostdoll', '유령 인형', '인형', 110, 2, 1, 1, 0, 0, doll('ghost', '#F6F4FC')),
  ('pumpdoll', '호박 인형', '인형', 90, 2, 1, 1, 0, 0, doll('pumpkin', '#F08A30')),
  ('bunny', '토끼 인형', '인형', 100, 2, 1, 1, 0, 0, doll('bunny', '#F6F2EE', '#FFE0E8')),
  ('bigbear', '커다란 곰 인형', '인형', 500, 4, 1, 1, 1, 0, doll('bear', '#C8945A', '#F2D8B0', 1.7)),
  ('witchdoll', '마녀 인형', '인형', 150, 2, 1, 1, 0, 0, doll('witch', '#5A3A9A', '#7A5AB8')),
  ('dragondoll', '아기 용 인형', '인형', 260, 3, 1, 1, 0, 0, doll('dragon', '#6AC88A', '#D8F2C8')),
  ('owldoll', '부엉이 인형', '인형', 120, 2, 1, 1, 0, 0, doll('owl', '#A87E58', '#F2E2C4')),
  ('rug_round', '둥근 러그', '러그', 120, 2, 2, 2, 0, 1, rug('round', '#C86A8A', '#F2D0DA')),
  ('rug_star', '별자리 러그', '러그', 300, 3, 2, 2, 0, 1, rug('star', '#3A3A7A', '#F6D24A')),
  ('rug_check', '체크 러그', '러그', 180, 2, 2, 2, 0, 1, rug('check', '#6A8A4A', '#A8C878')),
  ('rug_pump', '호박 러그', '러그', 160, 2, 2, 2, 0, 1, rug('pumpkin', '#F08A30', '#FFC070')),
  ('skull', '귀여운 해골', '장식', 80, 1, 1, 1, 1, 0, skull),
  ('balloons', '풍선 다발', '장식', 60, 1, 1, 1, 0, 0, balloons),
  ('candyjar', '사탕 항아리', '장식', 90, 1, 1, 1, 1, 0, candy_jar),
  ('cake', '케이크 스탠드', '장식', 140, 2, 1, 1, 1, 0, cake),
  ('fishbowl', '어항', '장식', 200, 2, 1, 1, 1, 0, fishbowl),
  ('cattower', '캣타워', '가구', 230, 2, 1, 1, 1, 0, cattower),
  ('coffinsofa', '관 소파', '가구', 420, 3, 2, 1, 1, 0, coffin_sofa),
]

def main():
    sprites, meta = [], []
    for (fid, name, cat, price, pts, w, dp, solid, flat, draw) in ITEMS:
        R = Room(6, 6, 60)
        R.obj(fid, [(1, 1)], lambda img, d, draw=draw: draw(R, img, d))
        o = R.objs[-1]; ax, ay = R.P(1, 1)
        sprites.append(o['img']); meta.append(dict(id=fid, name=name, cat=cat, price=price, pts=pts, w=w, d=dp, solid=solid, flat=flat, sw=o['img'].width, sh=o['img'].height, ax=ax - o['x'], ay=ay - o['y']))
    W = sum(s.width + 1 for s in sprites); Hh = max(s.height for s in sprites)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
    for s, m in zip(sprites, meta): sheet.paste(s, (x, 0)); m['sx'] = x; x += s.width + 1
    sheet.save('out/furn.png'); json.dump(meta, open('out/furn.json', 'w'), ensure_ascii=False)
    print('furniture', len(meta), sheet.size)
if __name__ == '__main__': main()
