# 사역마 시안 5: 고대 정령불 12종 · 장난감 같은 외곽선·점눈 대신 반투명 빛, 하얗게 타는 심지, 흩날리는 불티, 룬 고리, 가면·결정·균열 같은 신비한 핵
#   python3 wisp2_art.py <미리보기.png> [글꼴] → tools/iso/out/wisps2.png (64칸 × 12)
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
def hx(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])
N = 64
YY, XX = np.mgrid[0:N, 0:N] + .5
def noise(seed, s=6):   # 부드러운 값 잡음(-1~1): 가장자리를 너울너울하게
    r = np.random.RandomState(seed); g = r.rand(N // s + 2, N // s + 2)
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((N + 2 * s, N + 2 * s), Image.BICUBIC)
    return np.array(im)[s:s + N, s:s + N] / 127.5 - 1
def tongue(cx, base, top, r, sway=0, p=1.6, curl=0):
    out = np.zeros((N, N))
    for y in range(N):
        yc = y + .5
        if yc > base + r or yc < top: continue
        if yc >= base: w = r * math.sqrt(max(0, 1 - ((yc - base) / r) ** 2)); t = 0
        else: t = (base - yc) / (base - top); w = r * (1 - t) ** p
        x0 = cx + sway * t ** 2 + curl * math.sin(t * math.pi * 1.5) * t
        if w <= .3: continue
        d = 1 - np.abs(XX[y] - x0) / w; out[y] = np.maximum(out[y], np.clip(d, 0, 1) * min(1, w / r + .25))
    return out
def ball(cx, cy, r): return np.clip(1 - np.hypot(XX - cx, YY - cy) / r, 0, 1)
def ring(cx, cy, rx, ry, w=.9): return np.abs(np.hypot((XX - cx) / rx, (YY - cy) / ry) - 1) * min(rx, ry) < w
BAYER = np.array([[0, 2], [3, 1]]) / 4
DITH = np.tile(BAYER, (N // 2, N // 2))
def spirit(d, ramp, glow, seed, rag=.18):
    """깊이 → 반투명 정령 몸: 가장자리는 짙은 색에 반투명, 안으로 갈수록 밝고 핵은 하얗게, 단계 사이는 바이어 디더"""
    d = np.clip(d + noise(seed) * rag * (d > 0) * (1 - d), 0, 1)
    R = [hx(c) for c in ramp]; img = np.zeros((N, N, 4), np.float64)
    v = d * 5.4 + DITH * .9; lvl = np.clip(v.astype(int), 0, 5); m = d > .04
    for k in range(6): sel = m & (lvl == k); img[sel, :3] = R[k]
    img[m, 3] = np.clip(120 + d[m] * 400, 0, 255)
    # 빛 번짐: 몸 바깥 3겹
    prev = m
    for a in (110, 55, 24):
        g = prev.copy(); g[1:] |= prev[:-1]; g[:-1] |= prev[1:]; g[:, 1:] |= prev[:, :-1]; g[:, :-1] |= prev[:, 1:]
        sel = g & ~prev; img[sel, :3] = hx(glow); img[sel, 3] = np.maximum(img[sel, 3], a * DITH[sel] * 1.3 + a * .5); prev = g
    return img
def put(img, pts, c, a=255):
    for x, y in pts:
        if 0 <= x < N and 0 <= y < N: img[y, x, :3] = hx(c); img[y, x, 3] = a
def mask_on(img, sel, c, a=255): img[sel, :3] = hx(c); img[sel, 3] = a
def motes(img, seed, n, c, box=(6, 58, 4, 50)):
    r = np.random.RandomState(seed)
    for _ in range(n):
        x, y = r.randint(box[0], box[1]), r.randint(box[2], box[3])
        if img[y, x, 3] < 60: put(img, [(x, y)], c, int(r.choice([140, 200, 255])))
def runes(img, cx, cy, rx, ry, c, glyph, seed):   # 기울어진 룬 고리 + 고리 위 글자 조각
    sel = ring(cx, cy, rx, ry, .7) & (img[..., 3] < 200); img[sel, :3] = hx(c); img[sel, 3] = 120
    r = np.random.RandomState(seed)
    for k in range(6):
        a = k / 6 * 2 * math.pi + r.rand() * .3; x = int(cx + rx * math.cos(a)); y = int(cy + ry * math.sin(a))
        for dx, dy in glyph[k % len(glyph)]: put(img, [(x + dx, y + dy)], glyph and c, 230)
G = [[(0, -1), (0, 0), (0, 1), (1, -1)], [(-1, 0), (0, 0), (1, 0), (0, -1)], [(0, -1), (-1, 0), (1, 0), (0, 1)], [(-1, -1), (0, 0), (1, 1)]]
def ramp(*c): return list(c)
BLUE = ramp('#06102A', '#0E2A64', '#1E56B4', '#3E8CEA', '#9ACCFF', '#F4FBFF')
PURP = ramp('#12062A', '#2E1260', '#5A28AA', '#8C52E2', '#C8A0FF', '#FAF0FF')
GREEN = ramp('#041A0E', '#0A3E22', '#16763C', '#34B85A', '#9AF0A0', '#F2FFEC')
PINK = ramp('#2A0618', '#601440', '#A82E74', '#E05CA4', '#FFB0D8', '#FFF2F8')
GOLD = ramp('#241604', '#5A3A08', '#A06E10', '#E0A824', '#FFE48A', '#FFFFF0')
SILV = ramp('#10141E', '#2A3044', '#566078', '#8E9AB4', '#D2DCEE', '#FFFFFF')
RED = ramp('#200404', '#560A0A', '#9C1A12', '#DE4424', '#FF9A60', '#FFF0D8')
TEAL = ramp('#02181C', '#063A40', '#0E7478', '#28B2AE', '#86F2E6', '#F0FFFC')
ORNG = ramp('#241004', '#5A2406', '#A0480C', '#E8781C', '#FFC070', '#FFF8E0')
NAVY = ramp('#04061C', '#0A1244', '#18267E', '#3046B8', '#8CA0F0', '#F0F4FF')
DARK = ramp('#000000', '#06030C', '#120A20', '#22143A', '#3A2660', '#6A50A0')
def w1():   # 청운 · 푸른 혼불: 둥근 머리에서 길게 휘어 오르는 꼬리, 하얀 핵에 비스듬한 빈 눈
    d = np.maximum(tongue(30, 40, 4, 11, 10, 1.8, -5), ball(30, 41, 10) * .9); img = spirit(d, BLUE, '#5A9CFF', 1)
    put(img, [(25, 41), (26, 42), (34, 41), (33, 42)], '#0E2A64'); motes(img, 11, 9, '#BFE0FF'); return img
def w2():   # 자운 · 보라 쌍둥이불: 서로를 휘감아 도는 두 불, 가운데는 비어 있음
    d = np.maximum(tongue(24, 36, 6, 8, 16, 1.5), tongue(40, 42, 12, 8, -16, 1.5)); img = spirit(d * .95, PURP, '#A070FF', 2)
    mask_on(img, ball(24, 37, 2.6) > 0, '#FFFFFF'); mask_on(img, ball(40, 43, 2.6) > 0, '#FFFFFF'); motes(img, 12, 8, '#E0C8FF'); return img
def w3():   # 도롱 · 초록 도깨비불: 떨어져 떠도는 불덩이 셋, 가운데 하나만 바늘구멍 눈
    d = np.maximum.reduce([tongue(32, 40, 16, 9, 3), tongue(16, 30, 18, 5, -3) * .8, tongue(48, 24, 10, 5, 4) * .8]); img = spirit(d, GREEN, '#4ADC6A', 3, .25)
    put(img, [(29, 39), (35, 39)], '#0A3E22'); motes(img, 13, 14, '#C8FFB8'); return img
def w4():   # 연화 · 분홍 연꽃불: 가라앉은 꽃잎 불 위로 떠오른 심지, 감은 눈
    d = np.maximum.reduce([tongue(32 + dx, 46, 30 + abs(dx) * .6, 5, dx * .9) * .8 for dx in (-12, -6, 6, 12)] + [tongue(32, 40, 8, 8, 0, 1.4)])
    img = spirit(d, PINK, '#FF7AC0', 4); put(img, [(28, 37), (29, 38), (30, 38), (31, 37), (33, 37), (34, 38), (35, 38), (36, 37)], '#601440')
    runes(img, 32, 50, 18, 4, '#FFB0D8', G, 4); return img
def w5():   # 휘황 · 금빛 왕관불: 이마에 세로 셋째 눈, 머리 위로 떠 있는 후광
    d = np.maximum.reduce([tongue(32, 40, 10, 11, 0, 1.4), tongue(22, 42, 22, 5, -6), tongue(42, 42, 22, 5, 6)]); img = spirit(d, GOLD, '#FFD050', 5)
    sel = ring(32, 9, 10, 3, .6); img[sel, :3] = hx('#FFF2A0'); img[sel, 3] = 220
    put(img, [(32, 33), (31, 34), (33, 34), (31, 35), (33, 35), (32, 36)], '#5A3A08'); put(img, [(32, 34), (32, 35)], '#E0A824'); motes(img, 15, 8, '#FFF6C0'); return img
def w6():   # 월영 · 은빛 달불: 초승달 몸에서 늘어지는 면사포 꼬리, 감은 눈
    d = np.clip(ball(30, 30, 15) - np.clip(ball(37, 25, 12) * 3, 0, 1), 0, 1); d = np.maximum(d, tongue(24, 22, 54, 4, 0) * 0)
    veil = np.zeros((N, N))
    for y in range(40, 60): t = (y - 40) / 20; veil[y] = np.clip(1 - np.abs(XX[y] - (22 + 6 * math.sin(t * 4))) / (4 * (1 - t) + .5), 0, 1) * .5 * (1 - t)
    img = spirit(np.maximum(d, veil), SILV, '#C8D8FF', 6, .1); put(img, [(20, 30), (21, 31), (22, 31), (23, 30)], '#2A3044')
    motes(img, 16, 10, '#FFFFFF'); return img
def w7():   # 단화 · 붉은 잉걸불: 갈라진 흑요석 덩이 틈으로 새어 나오는 불, 위로 솟는 불길
    img = spirit(np.maximum(tongue(32, 34, 4, 10, -4, 1.5, 3), ball(32, 34, 9) * .7), RED, '#FF5A2A', 7, .25)
    rock = ball(32, 42, 11) > 0; img[rock, :3] = hx('#1A1018'); img[rock, 3] = 255
    lit = rock & (XX + YY < 32 + 42 - 4) & (ball(32, 42, 11) < .35); img[lit, :3] = hx('#3A2430')
    crack = [(32, 32), (32, 33), (31, 34), (31, 35), (32, 36), (33, 37), (33, 38), (32, 39), (31, 40), (30, 41), (29, 42), (34, 39), (35, 40), (36, 41), (37, 42), (38, 43), (30, 44), (31, 45), (32, 46), (32, 47), (26, 40), (27, 41), (28, 42)]
    put(img, crack, '#FFB060'); put(img, [(31, 41), (32, 40), (33, 40), (32, 41)], '#FFF0D8'); motes(img, 17, 12, '#FF9A50', (8, 56, 2, 30)); return img
def w8():   # 수련 · 청록 물불: 거꾸로 맺힌 물방울처럼 흘러내리는 불, 떨어지는 물방울
    d = np.zeros((N, N))
    for y in range(N):
        yc = y + .5
        if 12 <= yc <= 54: t = (yc - 12) / 42; w = 12 * math.sin(min(1, t * 1.25) * math.pi * .5) * (1 - max(0, t - .7) * 2.6) if t < 1 else 0
        else: continue
        if w > .3: d[y] = np.clip(1 - np.abs(XX[y] - 32 - 3 * math.sin(t * 6)) / w, 0, 1)
    d = np.maximum(d, ball(32, 18, 9)); img = spirit(d, TEAL, '#40D8D0', 8, .12)
    put(img, [(28, 22), (35, 22)], '#063A40'); put(img, [(31, 58), (32, 59), (32, 58), (40, 56), (24, 60)], '#86F2E6'); motes(img, 18, 6, '#F0FFFC'); return img
def w9():   # 등롱 · 녹슨 옛 등롱에 갇힌 불, 불 속 외눈
    img = spirit(tongue(32, 40, 18, 8, -3, 1.5), ORNG, '#FFA040', 9)
    fr, hi, rust = hx('#2A1E1A'), hx('#6A5040'), hx('#5A3A28')
    for y in range(15, 51):
        for x in (20, 44): img[y, x, :3] = fr if y % 7 else rust; img[y, x, 3] = 255
    for x in range(18, 47):
        for y in (14, 51): img[y, x, :3] = fr; img[y, x, 3] = 255
        img[13, x, :3] = hi if 20 < x < 44 else fr; img[13, x, 3] = 255
    for x in range(22, 43, 2): img[52, x, :3] = rust; img[52, x, 3] = 255
    for y in range(2, 13): img[y, 32, :3] = hi if y % 2 else fr; img[y, 32, 3] = 255
    mask_on(img, ball(32, 38, 3.2) > 0, '#FFF8E0'); put(img, [(32, 37), (32, 38), (32, 39)], '#241004'); return img
def w10():   # 성휘 · 남색 별자리불: 몸 안에 별자리가 비치는 밤하늘 불, 기울어진 룬 고리
    d = tongue(32, 38, 6, 12, 6, 1.6); img = spirit(np.minimum(d, .62), NAVY, '#7088FF', 10, .1)
    stars = [(28, 30), (32, 26), (36, 33), (30, 40), (35, 42), (33, 18), (26, 36)]
    for (a, b) in [(0, 1), (1, 2), (0, 6), (6, 3), (3, 4), (1, 5)]:
        (x0, y0), (x1, y1) = stars[a], stars[b]
        for t in np.linspace(0, 1, 8): put(img, [(int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t))], '#5A70D0', 230)
    put(img, stars, '#FFFFFF'); runes(img, 32, 40, 21, 6, '#8CA0F0', G, 10); motes(img, 20, 8, '#FFFFFF'); return img
def w11():   # 묵영 · 그림자불: 칠흑 불꽃에 걸린 하얀 옛 가면
    d = np.maximum.reduce([tongue(32, 42, 4, 12, 4, 1.5, 3), tongue(22, 42, 14, 6, -12), tongue(42, 42, 16, 6, 12), tongue(28, 48, 28, 5, -16)]); img = spirit(d, DARK, '#8A5AE0', 11, .3)
    mk = (np.hypot((XX - 32) / 7, (YY - 36) / 9) < 1); img[mk, :3] = hx('#E8E0D4'); img[mk, 3] = 255
    sh = mk & (XX > 33) & (np.hypot((XX - 32) / 7, (YY - 36) / 9) > .6); img[sh, :3] = hx('#B0A898')
    put(img, [(29, 34), (30, 34), (28, 35), (29, 35), (34, 34), (35, 34), (35, 35), (36, 35), (31, 41), (32, 41), (33, 41), (32, 31), (32, 30)], '#0A0610')
    put(img, [(32, 30), (32, 31)], '#C02040'); put(img, [(29, 35), (35, 35)], '#C8A0FF'); motes(img, 21, 10, '#8A5AE0'); return img
def w12():   # 채운 · 무지갯불: 떠 있는 결정 조각 속에서 타는 빛, 겹겹의 무지개 빛
    d = tongue(32, 42, 6, 11, -5, 1.6); img = spirit(d, SILV, '#FFFFFF', 12, .15)
    cols = ['#FF6A6A', '#FFB050', '#FFE070', '#7AE07A', '#6AB8FF', '#B08AFF']; m = img[..., 3] > 100
    for k, c in enumerate(cols): band = m & (np.abs((XX - 32) - (YY - 30) * .6) // 3 % 6 == k); img[band, :3] = img[band, :3] * .45 + hx(c) * .55
    cr = (np.abs(XX - 32) / 5 + np.abs(YY - 38) / 9) < 1; img[cr, :3] = hx('#E8F4FF'); img[cr, 3] = 255
    img[cr & (XX < 32), :3] = hx('#FFFFFF'); img[cr & (XX > 33), :3] = hx('#A8C0E8')
    for (x, y, s) in [(18, 22, 3), (46, 18, 2), (44, 46, 2)]:
        c = (np.abs(XX - x) / s + np.abs(YY - y) / (s * 2)) < 1; img[c, :3] = hx('#D8E8FF'); img[c, 3] = 220
    return img
WS = [('푸른 혼불', '청운', w1), ('보라 쌍둥이불', '자운', w2), ('초록 도깨비불', '도롱', w3), ('분홍 연꽃불', '연화', w4), ('금빛 셋째눈불', '휘황', w5), ('은빛 달불', '월영', w6),
      ('흑요석 잉걸불', '단화', w7), ('청록 물불', '수련', w8), ('녹슨 등롱불', '등롱', w9), ('남색 별자리불', '성휘', w10), ('가면 그림자불', '묵영', w11), ('결정 무지갯불', '채운', w12)]
if __name__ == '__main__':
    cells = [np.clip(f(), 0, 255).astype(np.uint8) for _, _, f in WS]
    Image.fromarray(np.concatenate(cells, axis=1)).save(os.path.join(HERE, '..', 'out', 'wisps2.png'))
    if len(sys.argv) > 1:
        fnt = sys.argv[2] if len(sys.argv) > 2 else None; F = ImageFont.truetype(fnt, 15) if fnt else None; F2 = ImageFont.truetype(fnt, 12) if fnt else None
        cw, ch, cols = 230, 250, 4; pv = Image.new('RGBA', (cw * cols + 20, ch * 3 + 60), (10, 8, 16, 255)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 시안 5 · 고대 정령불 12종', font=F, fill=(220, 200, 150))
        for i, (n, nm, _) in enumerate(WS):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 10, fill=(16, 12, 24), outline=(60, 48, 80), width=2)
            im = Image.fromarray(cells[i]).resize((192, 192), Image.NEAREST); pv.alpha_composite(im, (x + (cw - 14 - 192) // 2, y + 4))
            d.text((x + (cw - 14) // 2, y + 206), nm, font=F, fill=(230, 220, 240), anchor='mm'); d.text((x + (cw - 14) // 2, y + 226), n, font=F2, fill=(150, 135, 180), anchor='mm')
        pv.convert('RGB').save(sys.argv[1])
