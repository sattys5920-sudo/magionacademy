# 막대과자의 날 그림: 막대 10 맛 × 뿌리개 8 · 상자 무늬 9 × 색 8 × 리본 8 · 과자 탑 3 단계 · 책상 더미 · 막대 틀 · 가로등 장식 · 액자 · 배달 까마귀
#   python3 tools/stickday/stick_art.py → public/art/stick.png · stick.webp (게임용 한 장) + tools/stickday/out/*.png (미리보기 preview.png)
import os
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = D + '/out'; os.makedirs(O, exist_ok=True)
OL = (42, 26, 46, 255)
def hx(s, a=255): s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3],)
CHOCO = {'milk': '#8A5232', 'dark': '#4A2A1E', 'straw': '#F08AA8', 'matcha': '#7FB060', 'white': '#F4EEDC', 'ghost': '#9A6AD0',
         'caramel': '#D8963A', 'blue': '#6A7AD8', 'mint': '#8ADCC8', 'pumpkin': '#F08A3A'}
TOP = {'none': [], 'rainbow': ['#FF6A6A', '#FFD24A', '#7ACB7A', '#7FB8FF', '#C48AF0'], 'star': ['#FFE27A'], 'heart': ['#FF6A8A'],
       'pseed': ['#F2E6C0'], 'sseed': ['#5A4A3A'], 'stardust': ['#BFE8FF', '#FFFFFF'], 'gold': ['#FFD24A', '#F0B030']}
BISC = hx('#E8B868')

def stick(choco, top, seed=0):   # 막대 하나 7 × 30 (손잡이 비스킷 + 초콜릿 + 뿌리개)
    im = Image.new('RGBA', (7, 30)); p = im.load(); c = hx(CHOCO[choco])
    for y in range(30):
        for x in range(1, 6):
            edge = x in (1, 5) or y in (0, 29)
            if y < 21: col = OL if edge else (sh(c, 1.18) if x == 2 else sh(c, .82) if x == 4 else c)
            else: col = OL if edge else (sh(BISC, 1.1) if x == 2 else sh(BISC, .85) if x == 4 else BISC)
            p[x, y] = col
    for x in (2, 3, 4): p[x, 21] = sh(c, .7)   # 초콜릿 경계
    cols = TOP[top]
    if cols:
        pts = [(2, 3), (4, 6), (3, 9), (2, 12), (4, 15), (3, 18), (3, 4), (2, 8), (4, 11), (3, 14), (2, 17)]
        for i, (x, y) in enumerate(pts[:8 if top in ('rainbow', 'stardust', 'gold') else 5]):
            k = (i + seed) % len(cols); p[x, y] = hx(cols[k])
            if top in ('star', 'heart') and y + 1 < 21: p[x, y + 1] = sh(hx(cols[k]), .8)
    return im

PAT = ['plain', 'stripe', 'dot', 'check', 'heart', 'star', 'night', 'pumpkin', 'crest']
COL = {'cream': ('#F4F0E8', '#E8455A'), 'pink': ('#FFD6E4', '#F06A8A'), 'sky': ('#D6ECFF', '#5A8AD8'), 'mint': ('#D4F2E4', '#3E9A72'),
       'lemon': ('#FFF2B0', '#E8A030'), 'lilac': ('#E6DAFF', '#8A5AD0'), 'navy': ('#2E2A5A', '#FFE27A'), 'wine': ('#7A2E3A', '#F2C060')}
RIB = {'red': '#D8303A', 'pink': '#FF8EB8', 'gold': '#F2C040', 'sky': '#7FC8F0', 'purple': '#A06AE0', 'green': '#5AB060', 'white': '#F8F4EC', 'navy': '#3A4A90'}
HEART = ['.##.##.', '#######', '#######', '.#####.', '..###..', '...#...']
STAR = ['...#...', '..###..', '#######', '.#####.', '.##.##.', '#.....#']
def tops(choco, top, wob=False):   # 상자 위로 삐죽 나온 막대 끝 4 개 (26 × 12) · wob: 별 0 개면 삐뚤삐뚤
    im = Image.new('RGBA', (26, 13))
    for i in range(4):
        s = stick(choco, top, i).crop((0, 0, 7, 12)); dy = (i % 2) + (([1, -1, 2, 0][i]) if wob else 0)
        im.alpha_composite(s, (2 + i * 4 + ((1 if i == 3 else -1 if i == 0 else 0) if wob else 0), max(0, dy)))
    return im

def body(pat, col):   # 상자 몸통 26 × 25 (무늬 · 색) · 상자 그림의 9 ~ 33 줄
    W, H = 26, 25; im = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(im); a, b = hx(COL[col][0]), hx(COL[col][1])
    x0, y0, x1, y1 = 1, 0, W - 2, H - 1
    g.rectangle([x0, y0, x1, y1], fill=a, outline=OL)
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            u, v = x - x0, y - y0; on = False
            if pat == 'plain': on = False
            elif pat == 'stripe': on = (u + v) % 6 < 2
            elif pat == 'heart': on = any(0 <= u - ox < 7 and 0 <= v - oy < 6 and HEART[v - oy][u - ox] == '#' for ox, oy in ((2, 2), (12, 7), (3, 13), (13, 17)))
            elif pat == 'star': on = any(0 <= u - ox < 7 and 0 <= v - oy < 6 and STAR[v - oy][u - ox] == '#' for ox, oy in ((2, 3), (13, 9), (4, 16)))
            elif pat == 'dot': on = (u % 6 in (2, 3)) and (v % 6 in (2, 3)) or ((u + 3) % 6 in (2, 3) and (v + 3) % 6 in (2, 3))
            elif pat == 'check': on = ((u // 4) + (v // 4)) % 2 == 0
            elif pat == 'pumpkin': on = (u % 6 == 3 and 2 <= v <= 21) or ((u % 6 in (2, 4)) and v in (2, 21))
            elif pat == 'night': on = (u * 7 + v * 13) % 23 == 0 or (u, v) in ((16, 4), (17, 4), (16, 5), (17, 5), (15, 5), (16, 3))
            elif pat == 'crest': on = (abs(u - 11) <= 5 and 5 <= v <= 14 and (abs(u - 11) == 5 or v == 5)) or (v > 14 and abs(u - 11) <= 5 - (v - 14)) and abs(u - 11) >= 5 - (v - 14) - 1 or (u == 11 and 7 <= v <= 13) or (v == 9 and 9 <= u <= 13)
            if on: im.putpixel((x, y), b)
    for x in range(x0 + 1, x1): im.putpixel((x, y0 + 1), sh(a, 1.12)); im.putpixel((x, y1 - 1), sh(a, .8))
    return im

def ribbon(rib):   # 리본 띠 · 나비 매듭만 (26 × 25 · 몸통 위에 겹쳐요)
    W, H = 26, 25; im = Image.new('RGBA', (W, H)); r = hx(RIB[rib]); x0, y0, x1, y1 = 1, 0, W - 2, H - 1; cx = (x0 + x1 + 1) // 2
    for y in range(y0 + 1, y1): im.putpixel((cx - 1, y), r); im.putpixel((cx, y), sh(r, .85))   # 세로 띠
    for x in range(x0 + 1, x1): im.putpixel((x, y0 + 12), r)   # 가로 띠
    bow = [(-5, -2), (-4, -3), (-3, -3), (-2, -2), (-4, -1), (-3, -1), (-2, -1), (-5, -1), (4, -2), (3, -3), (2, -3), (1, -2), (3, -1), (2, -1), (1, -1), (4, -1), (0, -1), (-1, -1), (-1, 0), (0, 0), (-2, 1), (1, 1), (-3, 2), (2, 2)]
    for dx, dy in bow:
        x, y = cx + dx, y0 + 12 + dy
        if 0 <= x < W and 0 <= y < H: im.putpixel((x, y), r if dy < 1 or dx in (-1, 0) else sh(r, .8))
    return im

def box(pat, rib, choco='milk', top='rainbow', col='cream', wob=False):   # 상자 26 × 34 = 막대 끝 + 몸통 + 리본 (게임에서도 이 순서로 겹쳐 그려요)
    im = Image.new('RGBA', (26, 34)); im.alpha_composite(tops(choco, top, wob), (0, 0)); im.alpha_composite(body(pat, col), (0, 9)); im.alpha_composite(ribbon(rib), (0, 9))
    return im

def tower(n, k=None):   # 과자 탑: 1 단계 상자 4 · 2 단계 7 · 3 단계 10 (가구 34 × 64) · k를 주면 그 개수만 (책상 위 작은 더미)
    W, H = 34, 64; im = Image.new('RGBA', (W, H)); order = PAT[1:]; ribs = list(RIB); cols = list(COL)
    k = k or {1: 4, 2: 7, 3: 10}[n]; rows = [3, 3, 2, 1, 1]; i = 0; y = H - 1
    for row, cnt in enumerate(rows):
        if i >= k: break
        cnt = min(cnt, k - i); bw = 11; x0 = (W - cnt * bw) // 2
        for j in range(cnt):
            b = box(order[(i + row) % len(order)], ribs[(i * 3) % len(ribs)], list(CHOCO)[(i * 3) % len(CHOCO)], list(TOP)[1 + (i * 3) % 7], cols[(i * 5) % len(cols)]).resize((11, 14), Image.NEAREST)
            im.alpha_composite(b, (x0 + j * bw, y - 14)); i += 1
        y -= 12
    if n == 3:   # 꼭대기 리본 장식
        g = ImageDraw.Draw(im); t = y - 2; g.polygon([(W // 2 - 4, t), (W // 2, t - 4), (W // 2 + 4, t)], fill=hx('#FFD24A'), outline=OL)
    return im

def mold():   # 과자 교실 막대 틀: 오븐 옆 작은 나무 탁자 위 막대 틀 (32 × 30)
    im = Image.new('RGBA', (32, 30)); g = ImageDraw.Draw(im); wd, wl, wk = hx('#B07A4A'), hx('#D49A60'), hx('#8A5A2E')
    for x in (4, 26): g.rectangle([x, 17, x + 2, 29], fill=wk, outline=OL)   # 다리
    g.rectangle([1, 13, 30, 18], fill=wd, outline=OL); g.line([(2, 14), (29, 14)], fill=wl)   # 탁자 위
    g.rectangle([3, 6, 28, 13], fill=hx('#C8C8D8'), outline=OL); g.line([(4, 7), (27, 7)], fill=hx('#E8E8F4'))   # 틀
    for k in range(5): g.line([(6 + k * 5, 9), (6 + k * 5 + 3, 9)], fill=hx('#6A6A80'))   # 홈
    for k, c in enumerate(['#E8B868', '#8A5232', '#F08AA8']): g.line([(6 + k * 5, 10), (6 + k * 5 + 3, 10)], fill=hx(c)); g.point((6 + k * 5, 9), fill=OL)
    for x, c in ((9, '#F08AA8'), (13, '#7FB060'), (17, '#8A5232')):   # 막대 몇 개가 틀 위에 걸쳐 있어요
        g.line([(x, 1), (x + 3, 6)], fill=OL, width=1); g.line([(x + 1, 1), (x + 3, 5)], fill=hx(c))
    return im

def lamp_deco():   # 광장 가로등에 매다는 막대과자 장식 (14 × 20)
    im = Image.new('RGBA', (14, 20)); g = ImageDraw.Draw(im); g.line([(7, 0), (7, 4)], fill=OL)
    g.line([(2, 4), (12, 4)], fill=hx('#D8303A'), width=2)
    for i, c in enumerate(['straw', 'milk', 'matcha']):
        s = stick(c, 'rainbow', i).crop((1, 0, 6, 30)).resize((3, 15), Image.NEAREST); im.alpha_composite(s, (2 + i * 4, 5 + (i % 2)))
    return im

def frame():   # 방 가구 「완벽한 막대」 액자 (24 × 32): 금테 · 남색 바탕에 금빛 막대 하나 · 별 셋 · 받침
    im = Image.new('RGBA', (24, 32)); g = ImageDraw.Draw(im); gold, gd = hx('#E8B84A'), hx('#B07A2A')
    g.line([(5, 27), (3, 31)], fill=OL, width=2); g.line([(18, 27), (20, 31)], fill=OL, width=2); g.line([(5, 27), (4, 30)], fill=hx('#8A5A2E')); g.line([(18, 27), (19, 30)], fill=hx('#8A5A2E'))
    g.rectangle([1, 1, 22, 27], fill=gold, outline=OL); g.rectangle([2, 2, 21, 2], fill=hx('#FFE27A')); g.rectangle([2, 26, 21, 26], fill=gd)
    g.rectangle([4, 4, 19, 22], fill=hx('#2E2A5A'), outline=gd)
    st = stick('caramel', 'gold', 1).rotate(-35, expand=True, resample=Image.NEAREST); bb = st.getbbox(); st = st.crop(bb)
    st = st.resize((max(1, st.width * 2 // 3), max(1, st.height * 2 // 3)), Image.NEAREST); im.alpha_composite(st, (12 - st.width // 2, 13 - st.height // 2))
    for x, y in ((6, 6), (16, 7), (7, 19)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): im.putpixel((x + dx, y + dy), hx('#FFE27A') if (dx, dy) != (0, 0) else hx('#FFFFFF'))
    g.rectangle([8, 23, 15, 25], fill=hx('#FFF2B0'), outline=gd)   # 이름판
    return im

def crow(f):   # 배달 까마귀 (20 × 14) · 두 장 (날개 위 · 아래)
    im = Image.new('RGBA', (20, 14)); g = ImageDraw.Draw(im); bd, dk = hx('#3E3454'), hx('#2A2238')
    g.ellipse([5, 5, 14, 11], fill=bd, outline=OL); g.ellipse([12, 3, 17, 8], fill=bd, outline=OL)   # 몸 · 머리
    g.polygon([(17, 5), (20, 6), (17, 7)], fill=hx('#F2C040'), outline=OL); im.putpixel((15, 5), hx('#FFFFFF'))   # 부리 · 눈
    g.polygon([(5, 7), (1, 6), (1, 9), (5, 9)], fill=dk, outline=OL)   # 꼬리
    if f == 0: g.polygon([(7, 7), (9, 0), (12, 1), (12, 7)], fill=dk, outline=OL)   # 날개 위
    else: g.polygon([(7, 8), (9, 13), (12, 12), (12, 8)], fill=dk, outline=OL)   # 날개 아래
    g.line([(9, 11), (9, 13)], fill=hx('#F2C040')); g.line([(11, 11), (11, 13)], fill=hx('#F2C040'))   # 발
    return im

def mini_stick(choco):   # NPC가 머리 위에 드는 막대 (4 × 16)
    return stick(choco, 'rainbow', 2).crop((1, 0, 6, 30)).resize((4, 16), Image.NEAREST)

def mini_box():   # 까마귀가 무는 작은 상자 (10 × 10)
    im = Image.new('RGBA', (10, 10)); g = ImageDraw.Draw(im); g.rectangle([0, 2, 9, 9], fill=hx('#FFD6E4'), outline=OL)
    g.line([(5, 3), (5, 8)], fill=hx('#D8303A')); g.line([(1, 5), (8, 5)], fill=hx('#D8303A')); g.point([(3, 1), (4, 2), (6, 2), (7, 1)], fill=hx('#D8303A')); g.point([(3, 0), (7, 0)], fill=OL)
    return im

# 게임용 한 장 (public/art/stick.png · .webp): 칸 위치는 index.html 「막대과자의 날」의 STK_ART 와 같아요
#   y 0   몸통 무늬 9 × 색 8 (26 × 25, x = (무늬 × 8 + 색) × 26)
#   y 25  리본 8 (26 × 25) · 그 옆 x 208 부터 막대 끝 (26 × 13, x = 208 + (맛 × 8 + 뿌리개) × 26 는 너무 길어서 아래 줄)
#   y 50  막대 10 맛 × 뿌리개 8 (7 × 30, x = (맛 × 8 + 뿌리개) × 7)
#   y 80  과자 탑 3 단계 (34 × 64) · 책상 위 더미 1 ~ 3 (34 × 64) · 막대 틀 (32 × 30) · 가로등 장식 (14 × 20) · 액자 (24 × 32) · 까마귀 2 (20 × 14) · 작은 막대 10 (4 × 16) · 작은 상자 (10 × 10)
SHEET = {'body': (0, 0), 'rib': (0, 25), 'stick': (0, 50), 'tower': (0, 80), 'stack': (102, 80), 'mold': (204, 80), 'lamp': (244, 80), 'frame': (258, 80), 'crow': (282, 80), 'mini': (322, 80), 'mbox': (362, 80)}   # 막대 틀 32 × 30
def sheet():
    S = Image.new('RGBA', (len(PAT) * len(COL) * 26, 144))
    for i, p in enumerate(PAT):
        for j, c in enumerate(COL): S.alpha_composite(body(p, c), ((i * len(COL) + j) * 26, 0))
    for j, r in enumerate(RIB): S.alpha_composite(ribbon(r), (j * 26, 25))
    for i, c in enumerate(CHOCO):
        for j, t in enumerate(TOP): S.alpha_composite(stick(c, t, j), ((i * len(TOP) + j) * 7, 50))
    for n in (1, 2, 3): S.alpha_composite(tower(n), ((n - 1) * 34, 80)); S.alpha_composite(tower(1, n), (102 + (n - 1) * 34, 80))
    S.alpha_composite(mold(), SHEET['mold']); S.alpha_composite(lamp_deco(), SHEET['lamp']); S.alpha_composite(frame(), SHEET['frame'])
    for f in (0, 1): S.alpha_composite(crow(f), (SHEET['crow'][0] + f * 20, 80))
    for i, c in enumerate(CHOCO): S.alpha_composite(mini_stick(c), (SHEET['mini'][0] + i * 4, 80))
    S.alpha_composite(mini_box(), SHEET['mbox'])
    return S

if __name__ == '__main__':
    A = os.path.join(D, '..', '..', 'public', 'art'); SH = sheet(); SH.save(A + '/stick.png', optimize=True); SH.save(A + '/stick.webp', lossless=True, quality=100, method=6)
    S = Image.new('RGBA', (len(CHOCO) * len(TOP) * 8, 30))
    for i, c in enumerate(CHOCO):
        for j, t in enumerate(TOP): S.alpha_composite(stick(c, t, j), ((i * len(TOP) + j) * 8, 0))
    S.save(O + '/sticks.png')
    T = Image.new('RGBA', (3 * 36, 64))
    for n in (1, 2, 3): T.alpha_composite(tower(n), ((n - 1) * 36, 0))
    T.save(O + '/tower.png'); mold().save(O + '/mold.png'); lamp_deco().save(O + '/lamp.png')
    # 미리보기: 막대 10 맛 · 무늬 9 (색을 돌려 가며) · 상자 색 8 (같은 무늬) · 리본 8 · 탑 3 단계 · 틀 · 가로등 장식
    P = Image.new('RGBA', (300, 250), hx('#1E1830'))
    for i, c in enumerate(CHOCO): P.alpha_composite(stick(c, ['rainbow', 'star', 'gold', 'heart', 'stardust'][i % 5], i), (8 + i * 12, 6))
    cl = list(COL); rb = list(RIB); ck = list(CHOCO)
    for i, p in enumerate(PAT): P.alpha_composite(box(p, rb[i % 8], ck[i % 10], list(TOP)[1 + i % 7], cl[i % 8]), (8 + i * 31, 44))
    for i, c in enumerate(cl): P.alpha_composite(box('heart', 'gold' if c in ('navy', 'wine') else 'red', ck[(i + 3) % 10], 'rainbow', c), (8 + i * 31, 86))
    for i, r in enumerate(rb): P.alpha_composite(box('plain', r, ck[(i + 5) % 10], 'star', 'cream' if r not in ('white',) else 'sky'), (8 + i * 31, 128))
    for n in (1, 2, 3): P.alpha_composite(tower(n), (8 + (n - 1) * 40, 176))
    P.alpha_composite(mold(), (150, 210)); P.alpha_composite(lamp_deco(), (210, 206)); P.alpha_composite(frame(), (232, 196))
    for f in (0, 1): P.alpha_composite(crow(f), (262 + f * 2, 200 + f * 22))
    P.alpha_composite(mini_box(), (270, 236)); [P.alpha_composite(tower(1, k), (130 + (k - 1) * 14, 150)) for k in (1, 2, 3)]
    P.resize((P.width * 4, P.height * 4), Image.NEAREST).save(O + '/preview.png')
    print('ok')
