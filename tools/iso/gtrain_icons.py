# 유령 열차 이벤트 새 물건 15종 아이콘 (32x32) -> public/art/gtrain.png (480x32, 칸 i = x 32*i)
# 채집물 12종은 forage_icons.py 의 도구로 직접 그리고, 물고기 3종은 fish_rare.py 처럼 기존 물고기 그림의 색을 바꿔요
#   python3 tools/iso/gtrain_icons.py                # 시트 생성
#   python3 tools/iso/gtrain_icons.py --preview DIR  # 시트 + 4배 확대 미리보기(DIR/gtrain_prev.png)
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forage_icons as F
import fish_rare as FR
from forage_icons import H, R4, E, RE, RC, PG, LN, LEAF, Cv, WHITE, erode, ring, rot, sep, crystal, lerpc, mushroom, spot, moss_mound

ROOT = F.ROOT
OUT = os.path.join(ROOT, 'public', 'art', 'gtrain.png')
S = 32
# 칸 순서 (게임의 GT_ITEMS 순서와 같아요)
NAMES = ['별빛 민들레', '유성 솜털', '혜성 깃털', '망령 이끼', '저승 백합', '녹슨 기적 종', '거꾸로 버섯', '물구나무 도토리', '숲요정 등불',
         '동굴 수정', '메아리 돌', '빛나는 종유석', '안개 송사리', '유령 잉어', '안개 등롱어']
ICONS = {}


def icon(i):
    def deco(f):
        ICONS[i] = f
        return f
    return deco


STEMG = R4('#9ae070', '#5cb046', '#3a8240', '#25593a')


# ---------------------------------------------------------------- 0 별빛 민들레: 둥근 솜털 공 + 별빛 씨앗
@icon(0)
def _(c):
    c.fill(LN([(16, 30), (16.5, 24), (15.5, 18)], 1.6), STEMG[2])
    c.fill(LN([(16, 30), (16.5, 24)], .8), STEMG[1])
    leaf = LEAF((15.5, 29), (7, 23.5), 3.2, a=2.0, b=.6) | LEAF((16.5, 29), (25, 24.5), 3.0, a=2.0, b=.6)
    c.shade(leaf, STEMG, 'diag')
    ball = E(16, 12, 9.6, 9.2)
    PUFF = R4('#ffffff', '#eef0ff', '#c6c8f0', '#8e90c8')
    c.shade(ball, PUFF, 'sphere', th=(.8, .35, -.1))
    rr = c.rng
    for a in range(0, 360, 30):
        t = math.radians(a + 8)
        for k in (5.5, 8.2):
            x, y = 16 + math.cos(t) * k, 12 + math.sin(t) * k * .95
            c.put(x, y, H('#ffe680') if k > 7 else H('#a8aae0'))
    c.fill(E(16, 12, 2.2, 2.2), H('#ffd23a'))
    c.put(15, 11, H('#fff6c0'))
    c.halo = (H('#fff0a0'), 2.6, 110)
    c.spark(4, 5, H('#ffe890'), 1, WHITE)
    c.spark(28, 18, H('#fff0a0'), 1, WHITE)
    c.dot(27, 4, WHITE)


# ---------------------------------------------------------------- 1 유성 솜털: 꼬리를 끄는 푸른 솜털 뭉치
@icon(1)
def _(c):
    tail = PG([(18, 9), (28, 2.5), (30, 4), (22, 14), (19, 16)]) | PG([(19, 13), (29.5, 9), (30, 11), (21, 17)])
    TL = R4('#e8f6ff', '#a8d8ff', '#6ca8e8', '#3c6cb8')
    c.shade(tail, TL, 'diag', th=(.3, -.1, -.5))
    m = E(13, 19, 8.2, 7.6) | E(8.5, 15.5, 4.2, 4.0) | E(17, 14, 4.6, 4.4) | E(7.5, 22.5, 4.2, 3.8) | E(15.5, 24, 4.6, 3.6)
    FL = R4('#ffffff', '#dff0ff', '#a6c8f0', '#6a8cc8')
    c.shade(m, FL, 'sphere', box=(12, 18, 10, 9), th=(.72, .3, -.15))
    rr = c.rng
    for _ in range(26):
        q = (rr.randint(4, 22), rr.randint(11, 27))
        if q in m and c.p.get(q) in (FL[1], FL[2]):
            c.put(q[0], q[1], FL[0] if rr.random() < .6 else FL[2])
    c.fill(E(12, 18, 2.0, 2.0), H('#fff8c8'))
    c.halo = (H('#a8d8ff'), 2.6, 120)
    c.spark(26, 15, H('#cfe8ff'), 1, WHITE)
    c.spark(4, 6, WHITE, 1, WHITE)
    c.dot(24, 7, WHITE)


# ---------------------------------------------------------------- 2 혜성 깃털: 청록에서 금빛으로 물드는 깃털
@icon(2)
def _(c):
    p0, p1 = (7, 28), (25, 4)
    vane = LEAF(p0, p1, 7.0, a=2.0, b=.5, skew=-.15, bend=1.2)
    for (x, y) in vane:
        t = max(0, min(1, ((x - 7) * .55 + (28 - y) * .85) / 26))
        base = lerpc(H('#3cc8c0'), H('#ffd23a'), t)
        c.put(x, y, base)
    inner = erode(vane, 1)
    for (x, y) in vane - inner:
        c.put(x, y, lerpc(c.p[(x, y)], H('#1a1024'), .35))
    for k in range(4, 24, 3):
        a = F.lerp(p0, p1, k / 26)
        c.fill(LN([a, (a[0] + 4.5, a[1] + 1.5)], .7) & inner, H('#fff6c8'))
    c.fill(LN([(5.5, 30), p0, p1], .9), H('#fff2d0'))
    c.halo = (H('#ffe08a'), 2.8, 130)
    c.spark(27, 14, H('#fff0a0'), 1, WHITE)
    c.spark(5, 9, H('#9ff0e8'), 1, WHITE)
    c.dot(28, 3, WHITE)
    c.dot(15, 29, H('#9ff0e8'))


# ---------------------------------------------------------------- 3 망령 이끼: 푸르스름한 이끼 + 떠오르는 넋
@icon(3)
def _(c):
    MO = R4('#c8f0e8', '#7cc8bc', '#4a8a90', '#2c5068')
    m = moss_mound(c, MO, None)
    rr = c.rng
    top = [q for q in m if (q[0], q[1] - 1) not in m]
    for (x, y) in top:
        if rr.random() < .5:
            c.put(x, y - 1, MO[1] if rr.random() < .5 else MO[0])
    for _ in range(34):
        q = (rr.randint(3, 29), rr.randint(14, 27))
        if q in m:
            c.put(q[0], q[1], MO[0] if rr.random() < .5 else MO[3])
    WI = {'w': H('#e8fffa'), 'b': H('#9ee8dc'), 'e': H('#2c5068')}
    c.art(['.ww.', 'wwww', 'webw', 'wwww', '.wb.', '..b.'], WI, 8, 2)
    c.art(['.w.', 'www', 'web', '.b.'], WI, 21, 5)
    c.halo = (H('#9ee8dc'), 2.4, 100)
    c.dot(15, 6, H('#c8fff4'))
    c.dot(27, 13, H('#c8fff4'))


# ---------------------------------------------------------------- 4 저승 백합: 보랏빛 나팔 꽃잎 + 검은 줄기
@icon(4)
def _(c):
    c.fill(LN([(17, 31), (16.5, 24), (15, 17)], 1.4), H('#3a2c4e'))
    lf = LEAF((16.5, 27), (25, 20), 2.8, a=2.0, b=.6)
    c.shade(lf, R4('#8a7aa8', '#5c4e7a', '#3e3458', '#2a2240'), 'diag')
    PET = R4('#ffffff', '#e6dcff', '#a890e0', '#6a50a8')
    pets = [LEAF((15, 17), (5, 6), 5.2, a=2.0, b=.55, skew=.1), LEAF((15, 17), (25, 5), 5.2, a=2.0, b=.55, skew=-.1),
            LEAF((15, 17), (15, 2.5), 5.4, a=2.0, b=.55)]
    for pm in pets:
        sep(c, pm, PET[3])
        c.shade(erode(pm, 1), PET, 'diag', th=(.35, -.05, -.45))
    tips = [(5, 6), (25, 5), (15, 3)]
    for (x, y) in tips:
        c.put(x, y + 1, H('#c8b4ff'))
    for k in range(3):
        a = 210 + k * 60
        t = math.radians(a)
        c.fill(LN([(15, 15), (15 + math.cos(t) * 5, 15 + math.sin(t) * 5)], .6), H('#ffd23a'))
    c.halo = (H('#c8b4ff'), 2.4, 110)
    c.dot(28, 14, H('#e6dcff'))
    c.dot(4, 16, H('#e6dcff'))


# ---------------------------------------------------------------- 5 녹슨 기적 종: 녹이 슨 놋쇠 종
@icon(5)
def _(c):
    BR = R4('#ffe49a', '#d8a438', '#9a6a22', '#5e3c18')
    bell = PG([(11, 9), (21, 9), (23, 20), (26.5, 25), (5.5, 25), (9, 20)]) | E(16, 9.5, 5.2, 4.2)
    c.shade(bell, BR, 'cylv', box=(16, 17, 10.5, 9), th=(.78, .35, -.15))
    rim = E(16, 25.2, 11.2, 2.4)
    c.shade(rim, BR, 'cylh', th=(.9, .2, -.4))
    rr = c.rng
    RU = [H('#5ca88a'), H('#3e7a6a'), H('#a8582a')]
    for _ in range(30):
        q = (rr.randint(7, 25), rr.randint(8, 26))
        if q in bell | rim and rr.random() < .7:
            c.put(q[0], q[1], RU[rr.randint(0, 2)])
    c.fill(LN([(13, 3), (16, 1.5), (19, 3), (19, 5.5), (13, 5.5), (13, 3)], .9), H('#6e4824'))
    c.fill(E(16, 28.5, 2.2, 2.0), H('#7a5020'))
    c.put(15, 28, H('#c89040'))
    c.fill(LN([(11.5, 12), (10.5, 19)], .8), H('#fff2c0'))
    c.spark(27, 9, H('#fff0a0'), 1, WHITE)
    c.dot(4, 14, H('#ffe49a'))


# ---------------------------------------------------------------- 6 거꾸로 버섯: 위아래가 뒤집힌 보라 버섯 (그린 뒤 뒤집어요)
@icon(6)
def _(c):
    CAPP = R4('#e4b8ff', '#a868e0', '#6a36a8', '#3e1c70')
    STEM = R4('#f8f0ff', '#e0d4f0', '#b0a0c8', '#786890')
    cap, stem = mushroom(c, 16, 17.5, 13.2, 11.0, CAPP, STEM, 7.5, 9.5, 29.5)
    for (x, y, r) in [(9, 11, 2.2), (17, 7.5, 1.9), (22.5, 12, 2.4), (13.5, 14, 1.4), (25.5, 16, 1.2)]:
        spot(c, x, y, r, cap, H('#c8f0ff'), H('#8ab8d8'))
    c.flip = True
    c.spark(5, 4, H('#c8f0ff'), 1, WHITE)
    c.dot(27, 6, WHITE)


# ---------------------------------------------------------------- 7 물구나무 도토리: 청록 도토리를 거꾸로
@icon(7)
def _(c):
    NUT = R4('#b8f0e0', '#5cc4b0', '#2e8a84', '#1c5260')
    CAP = R4('#c8a8e8', '#8a62c0', '#5c3c8e', '#3a2460')
    F.acorn(c, NUT, CAP, CAP, H('#f0fff8'))
    c.flip = True
    c.spark(26, 6, H('#d8fff4'), 1, WHITE)
    c.dot(5, 8, WHITE)


# ---------------------------------------------------------------- 8 숲요정 등불: 잎사귀 뚜껑을 쓴 초록 등불
@icon(8)
def _(c):
    c.fill(LN([(16, 1.5), (16, 5)], .9), H('#6e4824'))
    c.fill(LN([(13, 2), (16, 1), (19, 2)], .8), H('#6e4824'))
    top = LEAF((8, 7.5), (24, 7.5), 4.2, a=2.0, b=.5) | LEAF((10, 6), (16, 3), 2.0, a=2.0, b=.5)
    c.shade(top, STEMG, 'diag')
    glass = E(16, 17, 7.5, 8.6) & RC(0, 9, 32, 27)
    GL = R4('#f6ffd8', '#c8f070', '#7cc040', '#3e7a30')
    c.shade(glass, GL, 'sphere', th=(.6, .2, -.3))
    for x in (11, 21):
        c.fill(LN([(x, 10), (x + (1 if x < 16 else -1), 25)], .8), H('#6e4824'))
    c.fill(RC(9, 25, 24, 28), H('#8a5c30'))
    c.fill(RC(10, 25, 23, 26), H('#b8844a'))
    c.fill(E(16, 17.5, 2.4, 3.2), H('#ffffff'))
    c.fill(E(16, 18.5, 1.4, 1.6), H('#fff6a0'))
    c.halo = (H('#c8f070'), 3.0, 130)
    c.spark(27, 15, H('#e8ffb0'), 1, WHITE)
    c.dot(4, 20, H('#e8ffb0'))


# ---------------------------------------------------------------- 9 동굴 수정: 푸른 수정 무리
@icon(9)
def _(c):
    CR = R4('#d8fbff', '#7cdcf0', '#3c98c8', '#245c90')
    ROCK = R4('#8a8aa0', '#606078', '#40405a', '#28283e')
    rock = (E(16, 28, 11.5, 3.6) | E(9.5, 27.2, 4.4, 3.0) | E(22.5, 27.4, 4.8, 3.2)) & RC(0, 0, 32, 31)
    c.shade(rock, ROCK, 'sphere', box=(16, 27, 13, 5))
    for (b, a, L, w) in [((10, 27.5), -30, 13, 3.0), ((22, 27.5), 28, 12, 3.0), ((16, 27), 0, 20, 4.0), ((19, 28), 12, 9, 2.2)]:
        whole, faces = crystal(c, b, a, L, w, CR)
        sep(c, whole, CR[3])
        for (m, col) in faces:
            c.fill(m, col)
    c.spark(6, 9, WHITE, 1, WHITE)
    c.spark(26, 11, H('#d8fbff'), 1, WHITE)
    c.dot(16, 4, WHITE)


# ---------------------------------------------------------------- 10 메아리 돌: 소리 물결 무늬가 새겨진 둥근 돌
@icon(10)
def _(c):
    ST = R4('#d8d4e8', '#9e98b8', '#6a6488', '#44405e')
    m = E(16, 18, 12.0, 10.5)
    c.shade(m, ST, 'sphere', th=(.8, .38, .0))
    rr = c.rng
    for q in m:
        if rr.random() < .1:
            c.put(q[0], q[1], ST[0] if rr.random() < .5 else ST[3])
    GLY = H('#8fe0ff')
    inner = erode(m, 2)
    for r in (3.4, 6.6, 9.8):
        for a in range(-55, 56, 3):
            t = math.radians(a)
            p = (int(9 + math.cos(t) * r), int(18 + math.sin(t) * r))
            if p in inner:
                c.put(p[0], p[1], GLY)
                if r < 9 and (p[0] + 1, p[1]) in inner:
                    c.put(p[0] + 1, p[1], H('#4ca8cc'))
    c.fill(E(9, 18, 1.6, 1.6), H('#e8faff'))
    c.halo = (H('#8fe0ff'), 2.2, 100)
    c.spark(28, 6, H('#c8f0ff'), 1, WHITE)
    c.dot(4, 7, H('#c8f0ff'))


# ---------------------------------------------------------------- 11 빛나는 종유석: 위에서 매달린 돌기둥 + 빛방울
@icon(11)
def _(c):
    ROCK = R4('#b8b0d0', '#807898', '#5a5474', '#3a3654')
    ceil = (E(16, 1, 15, 4.5)) & RC(0, 0, 32, 6)
    c.shade(ceil, ROCK, 'diag')
    big = PG([(10, 3), (20, 3), (15.5, 25)])
    small = PG([(4, 3), (10, 3), (7, 15)]) | PG([(21, 3), (28, 3), (24.5, 18)])
    CRY = R4('#e8fcff', '#9ae4f4', '#4ca8cc', '#2a6c98')
    for m in (small, big):
        sep(c, m, CRY[3])
        c.shade(erode(m, 1), CRY, 'cylv', th=(.7, .25, -.25))
    c.fill(LN([(13, 5), (15, 20)], .7), H('#ffffff'))
    DR = {'b': H('#bff4ff'), 'h': H('#ffffff'), 'd': H('#4ca8cc')}
    c.art(['.b.', 'bhb', 'bbd', '.d.'], DR, 14, 26)
    c.halo = (H('#9ae4f4'), 2.8, 120)
    c.spark(5, 24, H('#d8fbff'), 1, WHITE)
    c.dot(27, 25, WHITE)


def render_forage(i):
    c = Cv(i + 400)
    c.flip = False
    ICONS[i](c)
    im = c.render()
    return im.transpose(Image.FLIP_TOP_BOTTOM) if c.flip else im


# ---------------------------------------------------------------- 12~14 물고기 (기존 그림 색 바꾸기)
FR.PAL['mist'] = [(70, 64, 104), (130, 124, 170), (196, 192, 226), (246, 244, 255)]
FR.PAL['ghost'] = [(22, 70, 84), (54, 140, 150), (126, 214, 210), (226, 255, 250)]
FR.PAL['lamp'] = [(26, 40, 70), (52, 92, 130), (110, 170, 190), (220, 250, 240)]
FISH = [(2, 'mist', 'glow', (210, 206, 245)), (7, 'ghost', 'glow', (150, 240, 230)), (28, 'lamp', 'flame', (150, 240, 230))]


def render_fish(k):
    src = Image.open(os.path.join(ROOT, 'public', 'art', 'fish.png')).convert('RGBA')
    bi, pal, fx, col = FISH[k]
    cell = FR.recolor(src.crop((bi * S, 0, bi * S + S, S)), pal)
    return {'glow': FR.glow, 'spark': FR.spark, 'flame': FR.flame}[fx](cell, col)


def build():
    sheet = Image.new('RGBA', (S * len(NAMES), S), (0, 0, 0, 0))
    for i in range(12):
        sheet.paste(render_forage(i), (i * S, 0))
    for k in range(3):
        im = render_fish(k)
        sheet.paste(im, ((12 + k) * S, 0), im)
    return sheet


def preview(sheet, outdir):
    os.makedirs(outdir, exist_ok=True)
    bgc = (0x21, 0x17, 0x33, 255)
    Z, per, pad, lh = 4, 5, 8, 22
    cell = S * Z
    n = len(NAMES)
    rows = (n + per - 1) // per
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), bgc)
    d = ImageDraw.Draw(img)
    font = None
    for f in ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'):
        try:
            font = ImageFont.truetype(f, 15)
            break
        except Exception:
            pass
    for i in range(n):
        x0 = pad + (i % per) * (cell + pad)
        y0 = pad + (i // per) * (cell + lh + pad)
        t = sheet.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST)
        img.alpha_composite(t, (x0, y0))
        d.text((x0, y0 + cell + 2), NAMES[i], fill=(230, 220, 250, 255), font=font)
    img.save(os.path.join(outdir, 'gtrain_prev.png'))


if __name__ == '__main__':
    sheet = build()
    sheet.save(OUT)
    print('saved', OUT, sheet.size)
    if '--preview' in sys.argv:
        preview(sheet, sys.argv[sys.argv.index('--preview') + 1])
