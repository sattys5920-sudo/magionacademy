# 겨울잠 준비 그림 시안: 굴 6 곳 × 3 단계 (휑함 · 쌓임 · 낙엽으로 덮임) · 곰 (아기 동물 그림체) · 배고픔 · Z 표시 · 가구 3 종
#   python3 tools/hibernate/hib_art.py → tools/hibernate/out/*.png + preview.png
import os, math
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = D + '/out'; os.makedirs(O, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(D))
OL = (42, 26, 46, 255)
def hx(s, a=255): s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3],)
def hs(*a):
    h = 0
    for v in a: h = (h * 131 + int(v) + 7) & 0xffffffff
    return h

BABY = Image.open(ROOT + '/public/art/babies.png').convert('RGBA')   # 14 × 14 · 12 칸 (오리 고양이 강아지 토끼 다람쥐 고슴도치 박쥐 부엉이 여우 너구리 개구리 병아리)
def baby(i): return BABY.crop((i * 14, 0, i * 14 + 14, 14))

def bear():   # 곰 20 × 18: 아기 동물과 같은 외곽선 · 두 톤 음영
    W, H = 20, 18; im = Image.new('RGBA', (W, H)); p = im.load(); B, Bd, M = hx('#8A5A3A'), hx('#6A4028'), hx('#D8B088')
    def ell(cx, cy, rx, ry, c):
        for y in range(H):
            for x in range(W):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1: p[x, y] = c
    ell(10, 12.5, 8.5, 5.5, B); ell(10, 7, 6.5, 5.2, B); ell(5, 2.8, 2.2, 2.2, B); ell(15, 2.8, 2.2, 2.2, B)
    ell(5, 2.8, 1, 1, Bd); ell(15, 2.8, 1, 1, Bd); ell(10, 9, 2.8, 2, M)
    for x in range(W):
        for y in range(H):
            if p[x, y][3] and (x > 13 and y > 9): p[x, y] = Bd   # 오른쪽 아래 그늘
    for (x, y) in ((7, 7), (13, 7)): p[x, y] = OL
    p[10, 8] = OL; p[9, 10] = OL; p[11, 10] = OL
    for (x, y) in ((6, 16), (7, 16), (13, 16), (14, 16)): p[x, y] = Bd
    out = Image.new('RGBA', (W, H)); q = out.load()
    for y in range(H):
        for x in range(W):
            if p[x, y][3]: q[x, y] = p[x, y]
            elif any(0 <= x + dx < W and 0 <= y + dy < H and p[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): q[x, y] = OL
    return out

# 굴: 48 × 36 (빛은 왼쪽 위) · kind 마다 겉모습이 달라요
KIND = {'squirrel': ('stump', '#8A5A34', '#6A4226'), 'hedgehog': ('bush', '#4E7A3A', '#3A5E2A'), 'raccoon': ('rock', '#7A7488', '#5A5468'),
        'frog': ('mud', '#6A5236', '#4E3C26'), 'bat': ('cave', '#4A4258', '#332C40'), 'bear': ('bigcave', '#5A5468', '#3E3850')}
PILE = {'squirrel': ['#C88A3A', '#8A5A2A'], 'hedgehog': ['#D8304A', '#3A4AA8'], 'raccoon': ['#7FA8C8', '#C8D8E8'], 'frog': ['#D83030', '#FFE27A'],
        'bat': ['#C8B8F0', '#FFE27A'], 'bear': ['#F2C040', '#7FA8C8']}
LEAF = ['#C86A2A', '#E8A040', '#A04A2A', '#D88A3A']
def den(kind, st):
    W, H = 48, 36; im = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(im); form, base, dark = KIND[kind]; b, d = hx(base), hx(dark)
    hole = (24, 25, 7, 6)   # 굴 입구 (가운데 x, 아래 y, 반 너비, 높이)
    if form == 'stump':
        g.rectangle([10, 8, 38, 33], fill=b, outline=OL); g.ellipse([10, 3, 38, 13], fill=hx('#C8A070'), outline=OL); g.ellipse([16, 5, 32, 11], outline=sh(hx('#C8A070'), .8))
        for x in (16, 23, 31): g.line([(x, 14), (x, 32)], fill=d)
        g.polygon([(6, 33), (12, 28), (14, 33)], fill=b, outline=OL); g.polygon([(34, 33), (37, 27), (42, 33)], fill=b, outline=OL)
    elif form == 'bush':
        for cx, cy, r in ((14, 22, 10), (34, 22, 10), (24, 15, 12), (24, 26, 13)): g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=b, outline=OL)
        for cx, cy, r in ((14, 22, 9), (34, 22, 9), (24, 15, 11), (24, 26, 12)): g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=b)
        for i in range(14): x, y = 8 + hs(i, 1) % 32, 8 + hs(i, 2) % 22; im.putpixel((x, y), sh(b, 1.25))
    elif form in ('rock', 'cave', 'bigcave'):
        pts = [(4, 34), (6, 18), (14, 8), (26, 4), (38, 9), (44, 20), (45, 34)] if form != 'rock' else [(6, 34), (8, 20), (18, 10), (30, 9), (40, 16), (43, 34)]
        g.polygon(pts, fill=b, outline=OL)
        for i in range(10): x, y = 10 + hs(i, 3, len(form)) % 28, 10 + hs(i, 4) % 20; g.line([(x, y), (x + 3, y + 1)], fill=d)
        g.polygon([(6, 34), (6, 22), (12, 14)], fill=sh(b, 1.12))
        if form != 'rock': hole = (24, 34, 11 if form == 'bigcave' else 8, 15 if form == 'bigcave' else 11)
    elif form == 'mud':
        g.ellipse([2, 14, 46, 36], fill=b, outline=OL); g.ellipse([5, 16, 43, 32], fill=sh(b, 1.1))
        for x in range(6, 42, 5): g.line([(x, 14 + abs(x - 24) // 4), (x + 2, 12 + abs(x - 24) // 4)], fill=hx('#5A8A4A'))   # 풀
        g.ellipse([34, 26, 46, 33], fill=hx('#4A6A8A'), outline=OL)   # 작은 웅덩이
    cx, by, hw, hh = hole
    g.pieslice([cx - hw, by - hh, cx + hw, by + hh], 180, 360, fill=hx('#1A1220'), outline=OL)   # 아치 모양 입구
    g.line([(cx - hw, by), (cx + hw, by)], fill=OL)
    if st >= 1:   # 입구에 먹이 · 이불감이 쌓여요
        cols = PILE[kind]; n = 5 if st == 1 else 11
        for i in range(n):
            x = cx - hw - 2 + hs(i, 9, len(kind)) % (hw * 2 + 4); y = by - 1 - (hs(i, 10) % (2 if st == 1 else 4))
            c = hx(cols[i % 2]) if i % 3 else hx(LEAF[i % 4]); g.rectangle([x, y, x + 1, y + 1], fill=c); im.putpixel((x, y), sh(c, 1.2))
    if st >= 3:   # 입구가 낙엽으로 덮여요 (아치 안을 낙엽으로 꽉)
        for y in range(by - hh, by + 1):
            for x in range(cx - hw, cx + hw + 1):
                if ((x - cx) / max(1, hw)) ** 2 + ((y - by) / max(1, hh)) ** 2 <= .92 and im.getpixel((x, y)) == hx('#1A1220'):
                    im.putpixel((x, y), sh(hx(LEAF[hs(x // 2, y // 2, len(kind)) % 4]), .85 + (hs(x, y) % 3) * .1))
        for i in range(12):
            x = cx - hw + hs(i, 13, len(kind)) % (hw * 2); y = by - 1 - hs(i, 14) % 2
            im.putpixel((x, y), hx(LEAF[i % 4]))
    return im

def zzz():   # 잠든 숨소리 Z (12 × 12)
    im = Image.new('RGBA', (12, 12)); g = ImageDraw.Draw(im)
    for (x, y, s) in ((1, 6, 4), (6, 1, 5)):
        g.line([(x, y), (x + s, y)], fill=hx('#E8F0FF'), width=1); g.line([(x + s, y), (x, y + s)], fill=hx('#E8F0FF')); g.line([(x, y + s), (x + s, y + s)], fill=hx('#E8F0FF'))
    return im

def hungry():   # 배고픔 표시: 말풍선 안 빈 접시 (14 × 12)
    im = Image.new('RGBA', (14, 12)); g = ImageDraw.Draw(im)
    g.rounded_rectangle([0, 0, 13, 9], radius=3, fill=hx('#FFFFFF'), outline=OL); g.polygon([(4, 9), (6, 11), (7, 9)], fill=hx('#FFFFFF'), outline=OL)
    g.ellipse([3, 3, 10, 7], fill=hx('#D8D0E0'), outline=OL); g.line([(5, 5), (8, 5)], fill=hx('#B8B0C0'))
    return im

def cushion():   # 가구 고슴도치 쿠션 (22 × 16)
    im = Image.new('RGBA', (22, 16)); g = ImageDraw.Draw(im)
    g.ellipse([1, 3, 21, 15], fill=hx('#8A6A4A'), outline=OL)
    for i in range(9): x = 3 + i * 2; g.line([(x, 4 + (i % 2)), (x - 1, 1 + (i % 2))], fill=hx('#5A4028'))
    g.ellipse([13, 7, 21, 14], fill=hx('#F2D8B8'), outline=OL); im.putpixel((18, 9), OL); im.putpixel((20, 11), OL)
    return im

def bear_doll():   # 가구 잠든 곰 인형 (24 × 20): 눈 감은 곰
    b = bear(); p = b.load()
    for (x, y) in ((7, 7), (13, 7)): p[x, y] = hx('#8A5A3A')
    for x in (6, 7, 8): p[x, 7] = OL
    for x in (12, 13, 14): p[x, 7] = OL
    im = Image.new('RGBA', (24, 20)); im.alpha_composite(b, (2, 2)); im.alpha_composite(zzz().crop((0, 0, 12, 12)).resize((8, 8), Image.NEAREST), (16, 0))
    return im

def frame():   # 가구 작은 굴 액자 (20 × 18)
    im = Image.new('RGBA', (20, 18)); g = ImageDraw.Draw(im)
    g.rectangle([0, 0, 19, 17], fill=hx('#B07A44'), outline=OL); g.rectangle([3, 3, 16, 14], fill=hx('#2E2A5A'), outline=OL)
    g.ellipse([5, 8, 14, 16], fill=hx('#6A5236')); g.ellipse([8, 10, 11, 13], fill=hx('#1A1220'))
    for (x, y) in ((6, 5), (12, 4), (14, 7)): im.putpixel((x, y), hx('#FFE27A'))
    return im

ANI = {'squirrel': 4, 'hedgehog': 5, 'raccoon': 9, 'frog': 10, 'bat': 6}
if __name__ == '__main__':
    kinds = list(KIND)
    sheet = Image.new('RGBA', (48 * 3, 36 * 6))
    for r, k in enumerate(kinds):
        for st in range(3): sheet.alpha_composite(den(k, [0, 1, 3][st]), (st * 48, r * 36))
    sheet.save(O + '/dens.png'); bear().save(O + '/bear.png'); zzz().save(O + '/zzz.png'); hungry().save(O + '/hungry.png')
    cushion().save(O + '/cushion.png'); bear_doll().save(O + '/bear_doll.png'); frame().save(O + '/frame.png')
    # 미리보기: 굴마다 휑함(동물 + 배고픔) · 쌓임(동물) · 덮임(Z) 한 줄씩 · 아래에 가구
    P = Image.new('RGBA', (220, 6 * 44 + 40), hx('#2A3A2E'))
    for r, k in enumerate(kinds):
        y = 4 + r * 44
        for st in range(3):
            x = 6 + st * 64; P.alpha_composite(den(k, [0, 1, 3][st]), (x, y))
            a = bear() if k == 'bear' else baby(ANI[k])
            if st < 2: P.alpha_composite(a, (x + 44, y + 36 - a.height))
            if st == 0: P.alpha_composite(hungry(), (x + 48, y + 36 - a.height - 12))
            if st == 2: P.alpha_composite(zzz(), (x + 30, y + 2))
    y = 6 * 44 + 8
    for i, f in enumerate((cushion(), bear_doll(), frame())): P.alpha_composite(f, (10 + i * 40, y))
    P.resize((P.width * 4, P.height * 4), Image.NEAREST).save(O + '/preview.png')
    print('ok')
