# 시안: 정원 손님 20 종 — 새 10 · 동물 10 (아기 동물 그림과 같은 14×14 · 진보라 테두리 · 흰 반짝 눈 · 분홍 볼) → ../garden_mock/gi_guests.png (손님마다 2 칸) · gi_guests_preview.png
#   몸 모양 틀(동그란 몸 · 귀 · 부리 · 날개 · 꼬리 · 무늬)을 조합해서 그려요. 두더지 · 거북 · 달팽이는 garden_guests.py 그림을 그대로 가져와요
import os
from PIL import Image, ImageDraw, ImageFont
import garden_guests as GG   # 두더지 · 거북 · 달팽이 칸 (그 파일을 먼저 실행해 두지 않아도 돼요)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'garden_mock')
hx = GG.hx; OL = hx('#1a1024'); W = hx('#ffffff'); PK = hx('#ff9ab8')
def blob(px, rows, c):   # rows: {y: (x0, x1)} 몸 채우기
    for y, (a, b) in rows.items():
        for x in range(a, b + 1): px[(x, y)] = c
BODY = {3: (5, 8), 4: (4, 9), 5: (3, 10), 6: (3, 10), 7: (3, 10), 8: (3, 10), 9: (3, 10), 10: (4, 9), 11: (5, 8)}   # 기본 동그란 몸
def make(o, f):
    px = {}; c = hx(o['c']); blob(px, o.get('body', BODY), c)
    up = 1 if (f and o.get('bob')) else 0
    if o.get('belly'): blob(px, {8: (5, 8), 9: (5, 8), 10: (5, 8)}, hx(o['belly']))
    if o.get('face'): blob(px, {6: (4, 9), 7: (4, 9), 8: (5, 8)}, hx(o['face']))
    ear = o.get('ear')
    if ear == 'round': [px.update({(x, y): c for x in xs for y in (1, 2)}) for xs in ((3, 4), (9, 10))]; px.update({(4, 2): hx(o.get('ein', o['c'])), (9, 2): hx(o.get('ein', o['c']))})
    if ear == 'tall': [px.update({(x, y): c for x in xs for y in (0, 1, 2)}) for xs in ((4,), (9,))]
    if ear == 'deer': px.update({(3, 2): c, (2, 1): c, (10, 2): c, (11, 1): c, (4, 0): hx('#8a5a32'), (9, 0): hx('#8a5a32'), (4, 1): hx('#8a5a32'), (9, 1): hx('#8a5a32')})
    if o.get('crest'): [px.update({p: hx(o['crest'])}) for p in ((6, 1), (7, 1), (6, 2), (7, 2), (8, 0))]
    for (x, y, col) in o.get('spots', []): px[(x, y)] = hx(col)
    if o.get('wing'):   # 날개: 양옆 · 두 번째 칸에서 위로 펄럭
        wc = hx(o['wing']); dy = -2 if f else 0
        for y in (7, 8, 9): px[(2, y + dy)] = wc; px[(11, y + dy)] = wc
        px[(1, 8 + dy)] = wc; px[(12, 8 + dy)] = wc
    if o.get('tail'):
        tc = hx(o['tail'])
        for (x, y) in o.get('tailp', [(11, 9), (12, 8), (12, 7)]): px[(x, y)] = tc
    if o.get('fan'):   # 공작 꼬리: 뒤에 부채
        for i, (x, y) in enumerate([(1, 3), (2, 1), (4, 0), (7, 0), (9, 0), (11, 1), (12, 3), (0, 5), (13, 5)]):
            px.setdefault((x, y), hx(o['fan'][i % 2]))
    # 얼굴
    ey = 6; blink = f and o.get('blink', True) and not o.get('wing')
    for x in (5, 8):
        if blink: px[(x, ey + 1)] = OL
        else: px[(x, ey)] = W; px[(x, ey + 1)] = OL
    px[(4, 8)] = PK; px[(9, 8)] = PK
    if o.get('beak'): px[(6, 8)] = hx(o['beak']); px[(7, 8)] = hx(o['beak']); px[(6, 9)] = hx(o.get('beak2', o['beak']))
    elif o.get('nose'): px[(6, 8)] = hx(o['nose']); px[(7, 8)] = hx(o['nose'])
    if o.get('legs'): [px.update({(x, y): hx(o['legs']) for y in (12, 13)}) for x in (5, 8)]
    else: px[(4, 12)] = hx(o.get('foot', '#5a3a2a')); px[(5, 12)] = hx(o.get('foot', '#5a3a2a')); px[(8, 12)] = hx(o.get('foot', '#5a3a2a')); px[(9, 12)] = hx(o.get('foot', '#5a3a2a'))
    im = Image.new('RGBA', (14, 14), (0, 0, 0, 0))
    for (x, y), col in px.items():
        yy = y - up if (x, y) not in [(4, 12), (5, 12), (8, 12), (9, 12)] else y
        if 0 <= x < 14 and 0 <= yy < 14: im.putpixel((x, yy), col)
    # 테두리 (바깥 한 줄)
    a = im.load(); add = []
    for y in range(14):
        for x in range(14):
            if a[x, y][3]: continue
            if any(0 <= x + dx < 14 and 0 <= y + dy < 14 and a[x + dx, y + dy][3] and a[x + dx, y + dy][:3] != OL[:3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for p in add: a[p] = OL
    return im
BIRDS = [
 ('sparrow', '참새', dict(c='#b8865a', face='#f0dcc0', belly='#f0dcc0', wing='#7a5232', beak='#3a2a1a', spots=[(5, 3, '#7a4a2a'), (6, 3, '#7a4a2a'), (7, 3, '#7a4a2a'), (8, 3, '#7a4a2a')])),
 ('magpie', '까치', dict(c='#2a2a3a', belly='#f4f4f8', wing='#3a5ab8', beak='#1a1a24', tail='#2a3a8a', tailp=[(11, 10), (12, 10), (13, 9)])),
 ('bluebird', '파랑새', dict(c='#4a8ae8', belly='#ffb87a', wing='#2a5ab8', beak='#3a2a1a')),
 ('woodpecker', '딱따구리', dict(c='#3a3a48', face='#f4f0e8', belly='#f4f0e8', wing='#2a2a34', beak='#c8a040', crest='#e8302a')),
 ('pigeon', '비둘기', dict(c='#9aa0b8', belly='#c8ccdc', wing='#6a7088', beak='#e8a0a8', spots=[(3, 9, '#6ac8a8'), (10, 9, '#a86ac8')])),
 ('parrot', '앵무새', dict(c='#5ac85a', face='#f8e85a', belly='#f8e85a', wing='#3a8ae8', beak='#e8603a', crest='#e83a3a')),
 ('hummingbird', '벌새', dict(c='#3ab89a', belly='#c8f0e0', wing='#a8e8f8', beak='#2a2a2a', beak2='#2a2a2a', spots=[(5, 9, '#e83a6a'), (8, 9, '#e83a6a')])),
 ('robin', '울새', dict(c='#7a5a42', face='#e86a3a', belly='#e86a3a', wing='#5a4232', beak='#e8c040')),
 ('flamingo', '홍학', dict(c='#ff8ab0', belly='#ffc8dc', wing='#e86a98', beak='#2a2a2a', beak2='#ffe0e8', legs='#e86a98')),
 ('peacock', '공작새', dict(c='#2a6ae8', face='#5ab8e8', wing='#2a9a7a', beak='#c8a040', crest='#2ab8a8', fan=['#2ac88a', '#e8c040'])),
]
ANIMALS = [
 ('mouse', '생쥐', dict(c='#b8b4c8', belly='#ece8f4', ear='round', ein='#ffb8c8', nose='#ff8ab0', tail='#ffb8c8', tailp=[(11, 10), (12, 11), (13, 10)], bob=1)),
 ('hamster', '햄스터', dict(c='#e8a858', face='#fff0dc', belly='#fff0dc', ear='round', ein='#ffc8b8', nose='#ff8ab0', bob=1)),
 ('otter', '수달', dict(c='#8a5a3a', face='#e8c8a0', belly='#e8c8a0', ear='round', nose='#3a2a1a', tail='#6a4428', tailp=[(11, 10), (12, 10), (12, 9)])),
 ('fawn', '아기 사슴', dict(c='#c8803a', belly='#f4dcb8', ear='deer', nose='#3a2a1a', spots=[(4, 4, '#f4e8d0'), (8, 3, '#f4e8d0'), (10, 5, '#f4e8d0')])),
 ('redpanda', '레서판다', dict(c='#d8602a', face='#f8f0e8', ear='round', ein='#f8f0e8', nose='#2a1a1a', belly='#5a2a1a', tail='#a8401a', tailp=[(11, 10), (12, 9), (13, 9), (12, 10)])),
 ('badger', '오소리', dict(c='#6a6a7a', face='#3a3a48', ear='round', nose='#1a1a24', belly='#9a9aaa', spots=[(6, 3, '#f4f4f8'), (7, 3, '#f4f4f8'), (6, 4, '#f4f4f8'), (7, 4, '#f4f4f8'), (6, 5, '#f4f4f8'), (7, 5, '#f4f4f8')])),
 ('lizard', '도마뱀', dict(c='#6ac85a', belly='#c8f0a8', nose='#3a8a3a', tail='#4aa83a', tailp=[(11, 10), (12, 10), (13, 11)], spots=[(5, 4, '#f8d84a'), (8, 4, '#f8d84a'), (6, 2, '#4aa83a'), (7, 2, '#4aa83a')])),
]
KEEP = [('mole', '꼬마 두더지'), ('turtle', '꼬마 거북'), ('snail', '이끼 달팽이')]   # garden_guests.py 그림
OLD = {k: (pal, rows) for k, pal, rows in GG.G}
sprites = []
for k, nm, o in BIRDS + ANIMALS: sprites.append((k, nm, make(o, 0), make(o, 1)))
for k, nm in KEEP: pal, rows = OLD[k]; sprites.append((k, nm, GG.render(rows, pal), GG.render(GG.frame2(k, rows), pal)))
sh = Image.new('RGBA', (28 * len(sprites), 14))
for i, (k, nm, a, b) in enumerate(sprites): sh.alpha_composite(a, (i * 28, 0)); sh.alpha_composite(b, (i * 28 + 14, 0))
sh.save(os.path.join(OUT, 'gi_guests.png'))
F = ImageFont.truetype('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf', 12); CW = 150
pv = Image.new('RGBA', (CW * 5, CW * 4), (40, 30, 56, 255)); d = ImageDraw.Draw(pv)
for i, (k, nm, a, b) in enumerate(sprites):
    cx, cy = (i % 5) * CW, (i // 5) * CW; d.rounded_rectangle([cx + 6, cy + 6, cx + CW - 6, cy + CW - 6], 10, fill=(58, 44, 82, 255))
    pv.alpha_composite(a.resize((56, 56), Image.NEAREST), (cx + 14, cy + 22)); pv.alpha_composite(b.resize((56, 56), Image.NEAREST), (cx + 78, cy + 22)); d.text((cx + CW // 2, cy + 112), nm, font=F, fill=(255, 243, 200, 255), anchor='mm')
pv.save(os.path.join(OUT, 'gi_guests_preview.png')); print('ok', [s[0] for s in sprites])
