# 사역마 시안 6: 에테르 정령불 12종 · 얼굴 없이 순수한 빛과 불꽃만 · 잡음으로 일렁이는 여러 겹 불길 + 하얀 심지 + 넓게 번지는 빛 + 흩날리는 불티
#   python3 wisp3_art.py <미리보기.png> [글꼴] → tools/iso/out/wisps3.png (64칸 × 12)
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
def hx(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
N = 64
YY, XX = np.mgrid[0:N, 0:N] + .5
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
DITH = np.tile(BAYER, (N // 4, N // 4))
FRAC = 0.   # 애니메이션 진행(0~1): 잡음을 위로 흘려 불꽃이 타오르게, 한 바퀴 돌면 처음과 이어져요
def noise(seed, s):
    r = np.random.RandomState(seed); R = N // s + 3; g = np.tile(r.rand(R, R), (3, 1))
    im = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((R * s, 3 * R * s), Image.BICUBIC)); P = R * s; y0 = P + int(round(FRAC * P)) % P
    return im[y0:y0 + N, s:s + N] / 127.5 - 1
def fbm(seed): return noise(seed, 12) * .55 + noise(seed + 1, 6) * .3 + noise(seed + 2, 3) * .15
def flame(cx, base, h, w, seed, turb=1., lean=0., curl=0., k=1.5, p=1.25, br=.35):
    """일렁이는 불꽃 하나 → 세기(0~1). 위로 갈수록 가늘어지고 잡음으로 흔들리며 끝이 갈라져요"""
    t = (base - YY) / h; nx = fbm(seed); nb = fbm(seed + 50)
    x = XX - cx - lean * np.clip(t, 0, 1) ** 2 - curl * np.sin(np.clip(t, 0, 1) * math.pi * k) - nx * turb * 5 * np.clip(t, 0, 1.2)
    wp = np.where(t > 0, w * np.clip(1 - t, 0, 1) ** p, w * np.sqrt(np.clip(1 - (t * h / w) ** 2, 0, 1)))
    v = 1 - np.abs(x) / np.maximum(wp, .01); v = np.where(wp > .3, v, 0)
    v = v - np.clip(nb, 0, 1) * br * np.clip(t, 0, 1) - np.clip(t - .75, 0, 1) * 1.2
    return np.clip(v, 0, 1)
def orb(cx, cy, r): return np.clip(1 - np.hypot(XX - cx, YY - cy) / r, 0, 1)
def render(f, ramp, glow, halo=1.):
    """세기 → 6단계 반투명 빛. 바깥은 옅고 짙은 색, 안은 밝고 핵은 하양. 단계 사이 4×4 디더"""
    R = [hx(c) for c in ramp]; A = [0, 80, 140, 200, 245, 255]
    f = np.clip(f, 0, 1) ** .6; img = np.zeros((N, N, 4)); v = np.clip(f * 5.6 + DITH - .5, 0, 5.99); lvl = v.astype(int)
    for k in range(1, 6): s = lvl == k; img[s, :3] = R[k]; img[s, 3] = A[k]
    # 넓게 번지는 빛 (흐린 덩어리를 디더로 점찍기)
    m = Image.fromarray(((f > .02) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4 * halo)); g = np.array(m) / 255 * 1.6
    s = (lvl == 0) & (g * .9 > DITH + .3); img[s, :3] = hx(glow); img[s, 3] = np.clip(g[s] * 90, 20, 80)
    return img
def stack(*layers):   # 뒤 → 앞 순서로 겹치기 (빛은 더해지는 느낌으로 밝은 쪽 우선)
    out = np.zeros((N, N, 4))
    for L in layers:
        a = L[..., 3:] / 255; out[..., :3] = out[..., :3] * (1 - a) + L[..., :3] * a; out[..., 3] = np.maximum(out[..., 3], L[..., 3])
    return out
def sparks(img, seed, n, c, cx=32, top=4, bot=40, spread=18, trail=3):
    r = np.random.RandomState(seed); C = hx(c)
    for _ in range(n):
        x, y = cx + r.randn() * spread * .5, r.uniform(top, bot); sw = r.uniform(-1, 1); y = top + (y - top - FRAC * (bot - top) * r.uniform(.6, 1.4)) % (bot - top)
        for j in range(trail):
            xi, yi = int(x + sw * j * .6), int(y + j)
            if 0 <= xi < N and 0 <= yi < N and img[yi, xi, 3] < 150: img[yi, xi, :3] = C; img[yi, xi, 3] = 255 - j * 80
    return img
def ramp(*c): return list(c)
BLUE = ramp('#04102A', '#103A8A', '#2462D0', '#4C9CF6', '#A8DAFF', '#FFFFFF')
PURP = ramp('#100428', '#3A148A', '#6A30D0', '#A066F2', '#DCB8FF', '#FFFFFF')
GREEN = ramp('#021A0C', '#0C5A2C', '#1A9A48', '#46DA72', '#B4FFB8', '#FFFFFF')
PINK = ramp('#28041A', '#7A1650', '#C8327E', '#F46AB2', '#FFC4E2', '#FFFFFF')
GOLD = ramp('#201002', '#7A4A06', '#C88410', '#F4BE30', '#FFEC9A', '#FFFFFF')
SILV = ramp('#0C1018', '#3A4660', '#6A7A9C', '#A2B4D4', '#E0EAFA', '#FFFFFF')
RED = ramp('#200202', '#7A0E06', '#C82A0E', '#F4622A', '#FFB070', '#FFFAE8')
TEAL = ramp('#02161A', '#0A5258', '#129290', '#30D0C4', '#A0FFF0', '#FFFFFF')
ORNG = ramp('#200C02', '#7A3206', '#C8600C', '#F49420', '#FFD080', '#FFFFF0')
NAVY = ramp('#020418', '#121C6A', '#2A3AAE', '#5468E0', '#A8B8FF', '#FFFFFF')
VOID = ramp('#000000', '#0A0414', '#1A0C30', '#2C1650', '#120822', '#04020A')
def w1():   # Vael · 길게 휘감겨 오르는 푸른 혼불
    f = flame(32, 46, 42, 12, 1, 1.2, 4, -6, 1.2); return sparks(render(f, BLUE, '#3A7CFF'), 101, 9, '#C8E8FF', 32, 4, 30)
def w2():   # Ixi · 나선으로 꼬이며 오르는 보라 쌍불
    a = flame(32, 46, 42, 8, 2, .8, 0, 9, 1.6); b = flame(32, 46, 38, 8, 3, .8, 0, -9, 1.6)
    return sparks(render(np.maximum(a, b), PURP, '#8A50FF'), 102, 10, '#E8D4FF', 32, 4, 34)
def w3():   # Puck · 흩어져 흐르는 초록 불덩이 무리
    f = np.maximum.reduce([flame(30, 44, 26, 9, 4, 1.4, 2), flame(16, 32, 14, 5, 5, 1.2, -2) * .9, flame(46, 26, 14, 5, 6, 1.2, 3) * .9, flame(38, 12, 8, 3, 7, 1, 1) * .8, flame(20, 14, 7, 3, 8, 1) * .7])
    return sparks(render(f, GREEN, '#30C860'), 103, 12, '#D8FFD0', 32, 6, 48, 30, 2)
def w4():   # Lotis · 꽃잎처럼 벌어지는 분홍 불꽃, 가운데서 솟는 심지
    f = np.maximum.reduce([flame(32 + dx, 48, 22 - abs(dx) * .3, 5, 10 + i, .7, dx * 1.6, 0, 1, 1.1) * .85 for i, dx in enumerate((-10, -5, 5, 10))] + [flame(32, 46, 40, 8, 9, .9, 0, 2)])
    return sparks(render(f, PINK, '#FF5AB0'), 104, 10, '#FFE0F0', 32, 2, 30)
def w5():   # Sol · 햇무리처럼 빛살을 뿜는 금빛 불
    ang = np.arctan2(YY - 32, XX - 32); r = np.hypot(XX - 32, YY - 32)
    rays = np.clip((np.cos(ang * 8 + FRAC * 2 * math.pi / 8) * .5 + .5) ** 10 * (1 - r / 26), 0, 1) * .35
    f = np.maximum.reduce([flame(32, 42, 36, 11, 20, 1, 0, 2), orb(32, 36, 12) * .8, rays])
    return sparks(render(f, GOLD, '#FFC030', 1.3), 105, 8, '#FFF6D0', 32, 2, 50, 36, 1)
def w6():   # Lune · 초승달로 휘어 흐르는 차가운 은빛 불, 아래로 흩어지는 안개
    ang = np.arctan2(YY - 32, XX - 32); r = np.hypot(XX - 32, YY - 32)
    cres = np.clip(1 - np.abs(r - 15) / (7 * np.clip(np.cos((ang + 2.4) * .8), 0, 1) + .01), 0, 1) * (np.cos((ang + 2.4) * .8) > 0)
    tng = np.clip(1 - np.abs(r - 21) / 5, 0, 1) * np.clip(np.sin(ang * 9 + fbm(33) * 3) * .6, 0, 1) * (cres > 0).astype(float)
    tng = np.maximum(tng, np.roll(cres, -3, 1) * 0)
    f = np.clip(cres * 1.2 + fbm(30) * .25 * (cres > 0), 0, 1)
    flick = np.clip(1 - np.abs(r - 20) / 4, 0, 1) * (np.cos((ang + 2.4) * .8) > .3) * np.clip(fbm(34) * 1.5, 0, 1)
    return sparks(render(np.maximum(f, flick), SILV, '#B0C8FF'), 106, 12, '#FFFFFF', 30, 6, 56, 34, 1)
def w7():   # Ignis · 사납게 갈라지며 치솟는 붉은 불길과 불티 기둥
    f = np.maximum.reduce([flame(32, 48, 44, 13, 40, 1.8, 0, 0, 1, 1.1, .8), flame(22, 48, 28, 7, 41, 1.5, -6), flame(42, 48, 30, 7, 42, 1.5, 6)])
    return sparks(render(f, RED, '#FF4818'), 107, 22, '#FFC070', 32, 0, 30, 26, 3)
def w8():   # Rill · 물결 띠가 휘감아 도는 청록 불
    core = flame(32, 46, 36, 9, 50, .8, 0, 3)
    band = np.zeros((N, N))
    for ph in (0, math.pi):
        yc = 44 - (XX - 12) * .9; xs = XX
        yb = 40 + 7 * np.sin((XX - 32) / 7 + ph) - (XX - 12) * .5
        band = np.maximum(band, np.clip(1 - np.abs(YY - yb) / 2.6, 0, 1) * np.clip(1 - np.abs(XX - 32) / 22, 0, 1) * 1.1)
    return sparks(render(np.maximum(core, band), TEAL, '#20D0C0'), 108, 10, '#E0FFFA', 32, 4, 56, 30, 1)
def w9():   # Orbi · 고리 모양으로 돌며 타는 주황 불, 가운데는 빈 하늘
    ang = np.arctan2(YY - 34, XX - 32); r = np.hypot(XX - 32, YY - 34)
    rr = np.clip(1 - np.abs(r - 13) / 4, 0, 1)
    tongues = np.clip(1 - np.abs(r - 13 - 4) / 6, 0, 1) * np.clip(np.sin(ang * 7 + fbm(60) * 2 + FRAC * 2 * math.pi) * .5 + .3, 0, 1) * (r > 13)
    f = np.clip(np.maximum(rr, tongues) + fbm(61) * .2 * (rr > 0), 0, 1)
    return sparks(render(f, ORNG, '#FF8020'), 109, 10, '#FFE8B0', 32, 6, 56, 34, 2)
def w10():   # Eon · 성운처럼 일렁이는 남색 불, 안에 별빛이 반짝
    f = np.maximum(flame(32, 46, 42, 13, 70, 1.4, 4, 3, 1.3, 1.1, .4), orb(32, 38, 9) * .5); img = render(np.minimum(f, .78) * (.85 + fbm(71) * .3), NAVY, '#5068FF')
    r = np.random.RandomState(72)
    for _ in range(14):
        x, y = r.randint(22, 42), r.randint(14, 48)
        if f[y, x] > .2: img[y, x, :3] = 255; img[y, x, 3] = 255
        if f[y, x] > .4 and r.rand() < .4:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): img[y + dy, x + dx, :3] = hx('#A8B8FF'); img[y + dy, x + dx, 3] = 230
    return sparks(img, 110, 8, '#FFFFFF', 32, 2, 56, 40, 1)
def w11():   # Nyx · 빛을 삼키는 칠흑 불, 보랏빛 테두리와 흩어지는 그림자 연기
    f = np.maximum.reduce([flame(32, 46, 42, 12, 80, 1.6, 2, 3), flame(20, 46, 24, 6, 81, 1.4, -8), flame(44, 46, 26, 6, 82, 1.4, 8)])
    img = render(f, VOID, '#7A40E0', 1.2); e = (f > .02) & (f < .2); img[e, :3] = hx('#9A60F0'); img[e, 3] = 200
    return sparks(img, 111, 12, '#5A30A0', 32, 0, 30, 30, 3)
def w12():   # Iris · 오로라처럼 색이 흐르는 무지갯불
    f = flame(32, 46, 42, 12, 90, 1.3, -3, 4); img = render(f, SILV, '#FFFFFF')
    cols = [hx(c) for c in ('#FF5A7A', '#FFA040', '#FFE060', '#60E080', '#50B0FF', '#A070FF')]
    h = ((YY - XX * .5 + fbm(91) * 10) / 5).astype(int) % 6; m = (img[..., 3] > 0) & (f < .75)
    for k in range(6): s = m & (h == k); img[s, :3] = img[s, :3] * .35 + cols[k] * .65
    return sparks(img, 112, 10, '#FFFFFF', 32, 2, 34)
WS = [('푸른 혼불', 'Vael', w1), ('보라 나선불', 'Ixi', w2), ('초록 도깨비불', 'Puck', w3), ('분홍 연꽃불', 'Lotis', w4), ('금빛 햇무리불', 'Sol', w5), ('은빛 달불', 'Lune', w6),
      ('붉은 불기둥', 'Ignis', w7), ('청록 물결불', 'Rill', w8), ('주황 고리불', 'Orbi', w9), ('남색 성운불', 'Eon', w10), ('칠흑 그림자불', 'Nyx', w11), ('오로라 무지갯불', 'Iris', w12)]
def frames(F=8):   # 12종 × F칸 애니메이션 (세로 = 정령, 가로 = 칸)
    global FRAC; rows = []
    for _, _, f in WS:
        cs = []
        for k in range(F): FRAC = k / F; cs.append(np.clip(f(), 0, 255).astype(np.uint8))
        rows.append(np.concatenate(cs, axis=1))
    FRAC = 0.; return np.concatenate(rows, axis=0)
if __name__ == '__main__':
    Image.fromarray(frames()).save(os.path.join(HERE, '..', 'out', 'wisps3_anim.png'))
    cells = [np.clip(f(), 0, 255).astype(np.uint8) for _, _, f in WS]
    Image.fromarray(np.concatenate(cells, axis=1)).save(os.path.join(HERE, '..', 'out', 'wisps3.png'))
    if len(sys.argv) > 1:
        fnt = sys.argv[2] if len(sys.argv) > 2 else None; F = ImageFont.truetype(fnt, 15) if fnt else None; F2 = ImageFont.truetype(fnt, 12) if fnt else None
        cw, ch, cols = 230, 250, 4; pv = Image.new('RGBA', (cw * cols + 20, ch * 3 + 60), (8, 6, 14, 255)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 시안 6 · 에테르 정령불 12종', font=F, fill=(220, 200, 150))
        for i, (n, nm, _) in enumerate(WS):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 10, fill=(14, 10, 22), outline=(52, 42, 72), width=2)
            im = Image.fromarray(cells[i]).resize((192, 192), Image.NEAREST); pv.alpha_composite(im, (x + (cw - 14 - 192) // 2, y + 4))
            d.text((x + (cw - 14) // 2, y + 206), nm, font=F, fill=(230, 220, 240), anchor='mm'); d.text((x + (cw - 14) // 2, y + 226), n, font=F2, fill=(150, 135, 180), anchor='mm')
        pv.convert('RGB').save(sys.argv[1])
