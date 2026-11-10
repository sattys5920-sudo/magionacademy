# 시안: 「반이 같이 품는 거대 알」 그림 — 알 5 단계(금 0~4) · 아기 4 종 × 2 칸 (불새 · 구름 고래 · 별 여우 · 무지개 용)
#   python3 tools/egg_mock/egg_art.py → egg_stages.png (32×40 × 5) · egg_babies.png (32×32 × 2칸 × 4) · egg_preview.png (4 배)
import os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
H = lambda h, a=255: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
OL = H('#1E1428')
def outline(im):
    px = im.load(); W, Hh = im.size; add = []
    for y in range(Hh):
        for x in range(W):
            if px[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < Hh and px[x + dx, y + dy][3] > 0 and px[x + dx, y + dy][:3] != OL[:3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for p in add: px[p] = OL
    return im
def R(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)
def P(d, x, y, c): d.point((x, y), fill=c)
# ---------- 알 (금 0 ~ 4) ----------
def egg(stage):
    im = Image.new('RGBA', (32, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([3, 3, 28, 38], fill=H('#F2E6CC'))           # 몸통
    d.ellipse([5, 5, 22, 30], fill=H('#FBF5E6'))           # 밝은 면
    d.ellipse([18, 14, 28, 38], fill=H('#DCCDB0'))          # 그늘
    d.ellipse([9, 8, 13, 13], fill=H('#FFFFFF'))            # 반짝
    for x, y, c in ((15, 10, '#C9A9E8'), (21, 18, '#9FC8F0'), (10, 22, '#F0B0A8'), (18, 29, '#C9A9E8'), (24, 25, '#F0D080'), (12, 32, '#9FC8F0'), (7, 15, '#F0D080')):   # 별 무늬 점
        P(d, x, y, H(c)); P(d, x + 1, y, H(c)); P(d, x, y + 1, H(c))
    cr = H('#5A4A3A')
    paths = [[(16, 4), (14, 8), (17, 11), (15, 14)], [(26, 17), (22, 19), (24, 22), (20, 24)], [(5, 24), (9, 25), (8, 28), (12, 29), (11, 32)], [(15, 14), (12, 17), (14, 20), (11, 22), (13, 25)]]
    for i in range(min(stage, 4)): d.line(paths[i], fill=cr, width=1)
    if stage >= 4:   # 금 사이로 빛
        for (x0, y0), (x1, y1) in zip(paths[3], paths[3][1:]): d.line([(x0 + 1, y0), (x1 + 1, y1)], fill=H('#FFF6B0'), width=1)
    return outline(im)
# ---------- 아기 4 종 ----------
def firebird(f):   # 아기 불새: 동그란 병아리 몸 · 불꽃 볏 · 불꽃 꼬리
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im); up = f == 1
    for i, (x, h, c) in enumerate(((12, 7, '#FF7A2A'), (15, 9, '#FFB040'), (18, 7, '#FF7A2A'))): d.polygon([(x - 2, 11), (x, 11 - h - (1 if up and i == 1 else 0)), (x + 2, 11)], fill=H(c))   # 볏
    d.polygon([(3, 20), (0, 16 - up), (2, 23), (6, 24)], fill=H('#FF9A3A')); d.polygon([(4, 21), (2, 18), (5, 24)], fill=H('#FFE07A'))   # 꼬리 불꽃
    d.ellipse([6, 10, 26, 29], fill=H('#F05A3A')); d.ellipse([9, 16, 23, 29], fill=H('#FFB070'))   # 몸 · 배
    wy = 15 if up else 18; d.ellipse([21, wy, 28, wy + 7], fill=H('#D8402A')); d.ellipse([4, wy, 11, wy + 7], fill=H('#D8402A'))   # 날개
    R(d, 13, 15, 2, 3, H('#2A1A1A')); R(d, 19, 15, 2, 3, H('#2A1A1A')); P(d, 13, 15, H('#FFFFFF')); P(d, 19, 15, H('#FFFFFF'))   # 눈
    d.polygon([(15, 18), (18, 18), (16, 21)], fill=H('#FFD040'))   # 부리
    P(d, 11, 19, H('#FF8A9A')); P(d, 22, 19, H('#FF8A9A'))   # 볼
    R(d, 13, 29, 2, 2, H('#E09030')); R(d, 18, 29, 2, 2, H('#E09030'))   # 발
    return outline(im)
def cloudwhale(f):   # 아기 구름 고래: 몽실한 구름 몸 · 작은 꼬리 · 숨구멍 구름
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if f == 1: d.ellipse([12, 1, 17, 6], fill=H('#FFFFFF')); d.ellipse([16, 0, 22, 5], fill=H('#EAF6FF'))   # 뿜는 구름
    else: d.ellipse([14, 4, 18, 8], fill=H('#FFFFFF'))
    R(d, 15, 7, 2, 3, H('#CFE8FF'))
    d.polygon([(25, 18), (31, 13 - f), (30, 20), (31, 25 + f), (25, 22)], fill=H('#BFE0FA'))   # 꼬리
    for cx, cy, r in ((9, 19, 7), (15, 16, 8), (21, 19, 7), (14, 22, 7), (20, 23, 6)): d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=H('#EAF6FF'))   # 구름 몸
    d.ellipse([5, 21, 25, 29], fill=H('#BFE0FA')); d.ellipse([6, 20, 24, 26], fill=H('#EAF6FF'))   # 아랫배
    for x in range(8, 23, 3): P(d, x, 25, H('#9CCBF0'))
    R(d, 9, 17, 2, 3, H('#2A2A4A')); R(d, 16, 17, 2, 3, H('#2A2A4A')); P(d, 9, 17, H('#FFFFFF')); P(d, 16, 17, H('#FFFFFF'))
    P(d, 7, 21, H('#FFAAC0')); P(d, 18, 21, H('#FFAAC0')); d.line([(12, 21), (13, 22), (14, 21)], fill=H('#2A2A4A'))
    return outline(im)
def starfox(f):   # 아기 별 여우: 남보라 털 · 큰 귀 · 이마 별 · 끝에 별이 달린 꼬리
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im); sw = 1 if f else 0
    d.polygon([(19, 24), (27, 14 - sw), (30, 18 - sw), (24, 27)], fill=H('#4A3A8A')); d.polygon([(26, 15 - sw), (29, 12 - sw), (30, 17 - sw)], fill=H('#FFE27A'))   # 꼬리 · 별
    P(d, 29, 11 - sw, H('#FFFFFF'))
    d.ellipse([8, 16, 24, 30], fill=H('#5A4AA0')); d.ellipse([11, 21, 21, 30], fill=H('#E8E0FF'))   # 몸 · 가슴
    d.polygon([(6, 6), (11, 12), (7, 14)], fill=H('#5A4AA0')); d.polygon([(22, 6), (17, 12), (21, 14)], fill=H('#5A4AA0'))   # 귀
    d.polygon([(7, 8), (10, 12), (8, 13)], fill=H('#C9A9E8')); d.polygon([(21, 8), (18, 12), (20, 13)], fill=H('#C9A9E8'))
    d.ellipse([6, 9, 22, 22], fill=H('#6A5AB0')); d.polygon([(10, 17), (18, 17), (14, 22)], fill=H('#E8E0FF'))   # 얼굴 · 주둥이
    P(d, 14, 11, H('#FFE27A')); P(d, 13, 12, H('#FFE27A')); P(d, 15, 12, H('#FFE27A')); P(d, 14, 13, H('#FFE27A')); P(d, 14, 12, H('#FFFFFF'))   # 이마 별
    R(d, 10, 14, 2, 3, H('#1A1030')); R(d, 16, 14, 2, 3, H('#1A1030')); P(d, 10, 14, H('#FFFFFF')); P(d, 16, 14, H('#FFFFFF'))
    R(d, 13, 18, 2, 1, H('#1A1030'))
    R(d, 11, 29, 3, 2, H('#4A3A8A')); R(d, 18, 29, 3, 2, H('#4A3A8A'))
    return outline(im)
def rainbowdragon(f):   # 아기 무지개 용: 하얀 몸 · 무지개 갈기 · 작은 날개
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    RB = ['#FF6A6A', '#FFB040', '#FFE27A', '#7AEF6A', '#6AC8FF', '#B07AFF']
    up = f == 1; d.polygon([(22, 16), (30, 8 - up), (29, 18)], fill=H('#F0E6FF')); d.polygon([(23, 16), (28, 11 - up), (28, 17)], fill=H('#FFC0E0'))   # 날개
    d.polygon([(4, 24), (0, 27), (3, 28), (8, 26)], fill=H('#F8F4FF'))   # 꼬리
    d.ellipse([6, 16, 24, 30], fill=H('#F8F4FF')); d.ellipse([10, 21, 20, 30], fill=H('#FFF6D8'))   # 몸 · 배
    for i, c in enumerate(RB): d.ellipse([7 + i * 2, 4 + (i % 2), 11 + i * 2, 9 + (i % 2)], fill=H(c))   # 무지개 갈기
    d.ellipse([7, 7, 23, 21], fill=H('#F8F4FF'))   # 머리
    d.polygon([(10, 7), (11, 3), (13, 7)], fill=H('#FFE27A')); d.polygon([(18, 7), (19, 3), (21, 7)], fill=H('#FFE27A'))   # 뿔
    R(d, 11, 12, 2, 3, H('#2A1A3A')); R(d, 17, 12, 2, 3, H('#2A1A3A')); P(d, 11, 12, H('#FFFFFF')); P(d, 17, 12, H('#FFFFFF'))
    P(d, 9, 16, H('#FFAAC0')); P(d, 20, 16, H('#FFAAC0')); d.line([(13, 17), (14, 18), (15, 17), (16, 18)], fill=H('#2A1A3A'))
    R(d, 11, 29, 2, 2, H('#D8D0F0')); R(d, 17, 29, 2, 2, H('#D8D0F0'))
    return outline(im)
st = Image.new('RGBA', (32 * 5, 40)); [st.paste(egg(i), (i * 32, 0)) for i in range(5)]; st.save(os.path.join(HERE, 'egg_stages.png'))
KINDS = [firebird, cloudwhale, starfox, rainbowdragon]
bb = Image.new('RGBA', (64, 32 * 4)); [bb.paste(fn(f), (f * 32, k * 32)) for k, fn in enumerate(KINDS) for f in (0, 1)]; bb.save(os.path.join(HERE, 'egg_babies.png'))
pv = Image.new('RGBA', (32 * 5 + 8 + 32 * 4, 40), H('#2A2450')); pv.paste(st, (0, 0), st)
for k, fn in enumerate(KINDS): im = fn(0); pv.paste(im, (32 * 5 + 8 + k * 32, 6), im)
pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(os.path.join(HERE, 'egg_preview.png')); print('ok')
