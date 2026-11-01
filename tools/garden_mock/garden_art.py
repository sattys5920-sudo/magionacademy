# 시안: 「손님이 찾아오는 정원」 그림 — 창밖 마당 배경 · 놓는 물건 6 · 손님 생물 6 (2 칸씩) · 선물 6
#   python3 garden_art.py → garden_bg.png (160×112) · garden_items.png (24×24 × 6) · garden_guests.png (24×24 × 2칸 × 6) · garden_gifts.png (16×16 × 6) · garden_preview.png
import os, random
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); random.seed(3)
H = lambda h, a=255: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
OL = H('#1E1428')
def outline(im):   # 그림 바깥에 진한 테두리 한 줄
    px = im.load(); W, Hh = im.size; add = []
    for y in range(Hh):
        for x in range(W):
            if px[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < Hh and px[x + dx, y + dy][3] > 0 and px[x + dx, y + dy][:3] != OL[:3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for p in add: px[p] = OL
    return im
def R(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)
# ---------- 배경: 창틀 너머 저녁 마당 ----------
bg = Image.new('RGBA', (160, 112), H('#2A2450')); d = ImageDraw.Draw(bg)
for i, c in enumerate(['#3A2E6A', '#4A3A7A', '#5A4688', '#6A5090']): R(d, 0, i * 6, 160, 6, H(c))   # 저녁 하늘
for i in range(18): d.point((random.randint(2, 157), random.randint(1, 18)), fill=H('#FFF3C8'))
R(d, 120, 4, 9, 9, H('#FFE9A0')); R(d, 121, 5, 7, 7, H('#FFF6D0')); R(d, 118, 6, 2, 5, H('#3A2E6A'))   # 달
for x in range(0, 160, 14): d.ellipse([x - 6, 18, x + 12, 34], fill=H('#2A3A30'))   # 먼 나무
R(d, 0, 28, 160, 84, H('#3A6A3A'))   # 잔디
for i in range(260):
    x, y = random.randint(0, 159), random.randint(30, 111); d.point((x, y), fill=H(random.choice(['#4A7A42', '#2E5A30', '#5A8A4A'])))
for x in range(2, 160, 9): R(d, x, 30, 3, 10, H('#7A5232')); R(d, x, 30, 3, 1, H('#9A6A42'))   # 울타리
R(d, 0, 33, 160, 2, H('#6A4428')); R(d, 0, 37, 160, 2, H('#6A4428'))
d.polygon([(66, 112), (94, 112), (86, 40), (74, 40)], fill=H('#8A7A5A')); d.polygon([(68, 112), (92, 112), (85, 42), (75, 42)], fill=H('#A08E68'))   # 돌길
for y in range(46, 112, 8): R(d, 76 - (y - 40) // 8, y, 8 + (y - 40) // 5, 1, H('#7A6A4A'))
for bx, by in ((8, 44), (140, 50), (14, 96), (146, 94)): d.ellipse([bx - 9, by - 7, bx + 9, by + 7], fill=H('#2E5A2E')); d.ellipse([bx - 7, by - 6, bx + 5, by + 3], fill=H('#3E7A3A')); d.point((bx - 3, by - 3), fill=H('#FF8AB0'))
# 창틀 (방 안에서 내다보는 느낌)
R(d, 0, 0, 160, 3, H('#5A3A22')); R(d, 0, 0, 3, 112, H('#5A3A22')); R(d, 157, 0, 3, 112, H('#5A3A22')); R(d, 0, 109, 160, 3, H('#5A3A22')); R(d, 3, 3, 154, 1, H('#7A5232'))
bg.save(os.path.join(HERE, 'garden_bg.png'))
# ---------- 놓는 물건 (24×24) ----------
def item(k):
    im = Image.new('RGBA', (24, 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if k == 'pond':   # 작은 연못: 돌 테두리 · 물 · 연잎
        d.ellipse([1, 9, 22, 22], fill=H('#8A8A9A')); d.ellipse([3, 11, 20, 20], fill=H('#3A6AB8')); d.ellipse([5, 12, 15, 17], fill=H('#5A8AD8')); R(d, 7, 13, 3, 1, H('#CFE4FF'))
        d.ellipse([14, 14, 19, 18], fill=H('#3A8A3A')); d.point((16, 15), fill=H('#6AC85A'))
    elif k == 'lamp':   # 등불: 나무 기둥 · 호박색 등
        R(d, 11, 9, 2, 14, H('#6A4428')); R(d, 8, 21, 8, 2, H('#5A3A22')); R(d, 8, 3, 8, 8, H('#E8902A')); R(d, 9, 4, 6, 6, H('#FFC85A')); R(d, 10, 5, 2, 2, H('#FFF6C0')); R(d, 7, 2, 10, 2, H('#3A2A1A'))
    elif k == 'feeder':   # 먹이 접시: 나무 접시에 씨앗
        d.ellipse([3, 13, 20, 21], fill=H('#7A4A22')); d.ellipse([4, 13, 19, 18], fill=H('#9A6A3A'))
        for p in ((7, 15), (10, 14), (13, 15), (16, 14), (9, 16), (14, 16)): d.point(p, fill=H('#F0D070')); d.point((p[0] + 1, p[1]), fill=H('#C8902A'))
    elif k == 'swing':   # 작은 그네
        R(d, 3, 3, 2, 20, H('#6A4428')); R(d, 19, 3, 2, 20, H('#6A4428')); R(d, 3, 2, 18, 2, H('#7A5232')); d.line([(8, 4), (8, 15)], fill=H('#C8B890')); d.line([(16, 4), (16, 15)], fill=H('#C8B890')); R(d, 7, 15, 11, 2, H('#C8402A'))
    elif k == 'pumpkin':   # 호박 의자
        d.ellipse([3, 9, 20, 22], fill=H('#D86A18')); d.ellipse([5, 10, 13, 20], fill=H('#F0882A')); d.line([(11, 10), (11, 21)], fill=H('#B05010')); R(d, 10, 6, 3, 4, H('#3A6A2A')); R(d, 6, 12, 2, 3, H('#FFB060'))
    elif k == 'bell':   # 바람 종
        R(d, 11, 1, 2, 4, H('#6A4428')); d.polygon([(7, 14), (17, 14), (15, 5), (9, 5)], fill=H('#5AB8C8')); R(d, 10, 6, 2, 6, H('#9AE0E8')); R(d, 11, 15, 2, 3, H('#E8D070')); d.line([(12, 18), (14, 22)], fill=H('#F0E8D0'))
    return outline(im)
ITEMS = ['pond', 'lamp', 'feeder', 'swing', 'pumpkin', 'bell']
sh = Image.new('RGBA', (24 * len(ITEMS), 24)); [sh.alpha_composite(item(k), (i * 24, 0)) for i, k in enumerate(ITEMS)]; sh.save(os.path.join(HERE, 'garden_items.png'))
# ---------- 손님 생물 (24×24 · 2칸) ----------
def guest(k, f):
    im = Image.new('RGBA', (24, 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im); b = f   # f: 1이면 살짝 들썩
    if k == 'frog':   # 반딧불 개구리: 연두 몸 · 엉덩이에 빛
        d.ellipse([5, 11 - b, 18, 21], fill=H('#5AA83A')); d.ellipse([6, 12 - b, 14, 18], fill=H('#7AC85A')); R(d, 7, 9 - b, 3, 3, H('#5AA83A')); R(d, 13, 9 - b, 3, 3, H('#5AA83A')); R(d, 8, 10 - b, 1, 1, OL); R(d, 14, 10 - b, 1, 1, OL)
        d.ellipse([15, 14 - b, 20, 19 - b], fill=H('#FFF27A' if f else '#E8D84A')); R(d, 5, 20, 4, 2, H('#4A8A2A')); R(d, 15, 20, 4, 2, H('#4A8A2A'))
    elif k == 'bat':   # 꼬마 박쥐: 보라 · 날개 접었다 폈다
        d.ellipse([8, 8, 15, 16], fill=H('#5A3A7A')); R(d, 9, 6, 2, 3, H('#5A3A7A')); R(d, 13, 6, 2, 3, H('#5A3A7A')); R(d, 10, 10, 1, 1, H('#FFE070')); R(d, 13, 10, 1, 1, H('#FFE070'))
        if f: d.polygon([(8, 11), (1, 7), (3, 14)], fill=H('#7A5A9A')); d.polygon([(15, 11), (22, 7), (20, 14)], fill=H('#7A5A9A'))
        else: d.polygon([(8, 11), (4, 13), (8, 16)], fill=H('#7A5A9A')); d.polygon([(15, 11), (19, 13), (15, 16)], fill=H('#7A5A9A'))
    elif k == 'squirrel':   # 도토리 다람쥐: 큰 꼬리
        d.ellipse([12, 6 - b, 22, 20 - b], fill=H('#C87A3A')); d.ellipse([14, 8 - b, 20, 16 - b], fill=H('#E89A5A')); d.ellipse([4, 11, 13, 21], fill=H('#B86A2A')); d.ellipse([5, 7, 11, 13], fill=H('#B86A2A')); R(d, 7, 9, 1, 1, OL); R(d, 6, 6, 2, 2, H('#B86A2A')); R(d, 6, 15, 3, 3, H('#8A5A2A'))
    elif k == 'cat':   # 유령 고양이: 반투명 하늘빛
        d.ellipse([5, 9 - b, 18, 21], fill=H('#CFE4F8', 200)); R(d, 6, 6 - b, 3, 4, H('#CFE4F8', 200)); R(d, 14, 6 - b, 3, 4, H('#CFE4F8', 200)); R(d, 8, 12 - b, 2, 2, H('#3A5A8A')); R(d, 13, 12 - b, 2, 2, H('#3A5A8A')); R(d, 11, 15 - b, 1, 1, H('#FF9AB8'))
        d.polygon([(17, 17), (22, 12 + b), (21, 18)], fill=H('#CFE4F8', 200))
    elif k == 'owl':   # 아기 부엉이
        d.ellipse([6, 6, 18, 21], fill=H('#8A6A4A')); d.ellipse([8, 11, 16, 20], fill=H('#C8A87A')); d.ellipse([7, 8, 11, 12], fill=H('#FFF6D0')); d.ellipse([13, 8, 17, 12], fill=H('#FFF6D0'))
        R(d, 9, 9 + b, 1, 2, OL); R(d, 15, 9 + b, 1, 2, OL); R(d, 11, 12, 2, 2, H('#E8A030')); R(d, 7, 5, 2, 2, H('#8A6A4A')); R(d, 15, 5, 2, 2, H('#8A6A4A'))
    elif k == 'fox':   # 달빛 여우 (드문 손님): 은빛 · 꼬리 끝 빛
        d.ellipse([3, 11, 15, 20], fill=H('#D8DCF0')); d.polygon([(12, 6), (20, 9), (17, 15), (11, 13)], fill=H('#E8ECFA')); R(d, 13, 4, 2, 4, H('#D8DCF0')); R(d, 17, 5, 2, 4, H('#D8DCF0')); R(d, 16, 10, 1, 1, OL)
        d.polygon([(4, 14), (0, 8 - b), (2, 16)], fill=H('#E8ECFA')); d.point((0, 8 - b), fill=H('#FFF6A0')); d.point((1, 9 - b), fill=H('#FFF6A0'))
    return outline(im)
GUESTS = ['frog', 'bat', 'squirrel', 'cat', 'owl', 'fox']
gs = Image.new('RGBA', (48 * len(GUESTS), 24)); [gs.alpha_composite(guest(k, f), (i * 48 + f * 24, 0)) for i, k in enumerate(GUESTS) for f in (0, 1)]; gs.save(os.path.join(HERE, 'garden_guests.png'))
# ---------- 선물 (16×16) ----------
def gift(k):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if k == 'glow': d.ellipse([4, 4, 11, 11], fill=H('#E8D84A')); d.ellipse([5, 5, 9, 9], fill=H('#FFF6A0'))   # 반딧불 조각
    elif k == 'feather': d.polygon([(4, 13), (11, 2), (12, 5), (6, 13)], fill=H('#7A5A9A')); d.line([(4, 13), (11, 3)], fill=H('#C8B0E8'))   # 박쥐 깃털
    elif k == 'acorn': d.ellipse([4, 6, 11, 13], fill=H('#B8742A')); R(d, 4, 4, 8, 3, H('#6A4428')); R(d, 7, 2, 2, 2, H('#6A4428')); R(d, 5, 7, 2, 2, H('#E09A4A'))   # 도토리
    elif k == 'bell': R(d, 5, 3, 6, 7, H('#CFE4F8')); R(d, 4, 10, 8, 2, H('#CFE4F8')); R(d, 7, 12, 2, 2, H('#9AB8E8')); R(d, 6, 4, 1, 4, H('#FFFFFF'))   # 유령 방울
    elif k == 'quill': d.polygon([(3, 13), (10, 3), (12, 4), (5, 13)], fill=H('#C8A87A')); d.line([(3, 13), (11, 3)], fill=H('#FFF6D0'))   # 부엉이 깃
    elif k == 'moon': d.ellipse([3, 3, 12, 12], fill=H('#FFF6C0')); d.ellipse([6, 2, 14, 10], fill=(0, 0, 0, 0))   # 달빛 조각
    return outline(im)
GIFTS = ['glow', 'feather', 'acorn', 'bell', 'quill', 'moon']
gf = Image.new('RGBA', (16 * len(GIFTS), 16)); [gf.alpha_composite(gift(k), (i * 16, 0)) for i, k in enumerate(GIFTS)]; gf.save(os.path.join(HERE, 'garden_gifts.png'))
# ---------- 미리보기 ----------
pv = bg.copy(); [pv.alpha_composite(item(k), (8 + i * 25, 52)) for i, k in enumerate(ITEMS)]; [pv.alpha_composite(guest(k, 0), (8 + i * 25, 78)) for i, k in enumerate(GUESTS)]
pv.resize((640, 448), Image.NEAREST).save(os.path.join(HERE, 'garden_preview.png')); print('ok')
