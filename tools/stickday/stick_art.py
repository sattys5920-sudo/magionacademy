# 막대과자의 날 그림: 막대 6 맛 × 뿌리개 · 상자 6 무늬 × 리본 4 색 · 과자 탑 3 단계 · 막대 틀 소품
#   python3 tools/stickday/stick_art.py → tools/stickday/out/*.png (+ 미리보기 preview.png)
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
def box(pat, rib, choco='milk', top='rainbow', col='cream'):   # 상자 26 × 34: 앞면 무늬 · 위쪽 창으로 막대 끝 · 리본 띠와 나비 매듭
    W, H = 26, 34; im = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(im); a, b = hx(COL[col][0]), hx(COL[col][1])
    for i in range(4):   # 막대 끝이 위로 삐죽
        s = stick(choco, top, i); im.alpha_composite(s.crop((0, 0, 7, 12)), (2 + i * 4, 0 + (i % 2)))
    x0, y0, x1, y1 = 1, 9, W - 2, H - 1
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
    r = hx(RIB[rib]); cx = (x0 + x1 + 1) // 2
    for y in range(y0 + 1, y1): im.putpixel((cx - 1, y), r); im.putpixel((cx, y), sh(r, .85))   # 세로 띠
    for x in range(x0 + 1, x1): im.putpixel((x, y0 + 12), r)   # 가로 띠
    bow = [(-5, -2), (-4, -3), (-3, -3), (-2, -2), (-4, -1), (-3, -1), (-2, -1), (-5, -1), (4, -2), (3, -3), (2, -3), (1, -2), (3, -1), (2, -1), (1, -1), (4, -1), (0, -1), (-1, -1), (-1, 0), (0, 0), (-2, 1), (1, 1), (-3, 2), (2, 2)]
    for dx, dy in bow:
        x, y = cx + dx, y0 + 12 + dy
        if 0 <= x < W and 0 <= y < H: im.putpixel((x, y), r if dy < 1 or dx in (-1, 0) else sh(r, .8))
    for dx, dy in bow:   # 매듭 외곽선
        for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = cx + dx + ex, y0 + 12 + dy + ey
            if 0 <= x < W and 0 <= y < H and (dx + ex, dy + ey) not in bow and im.getpixel((x, y))[3] and im.getpixel((x, y)) not in (r, sh(r, .8)): pass
    return im

def tower(n):   # 과자 탑: 1 단계 상자 4 · 2 단계 7 · 3 단계 10 (책상 위 가구 32 × 60)
    W, H = 34, 64; im = Image.new('RGBA', (W, H)); order = PAT[1:]; ribs = list(RIB); cols = list(COL)
    k = {1: 4, 2: 7, 3: 10}[n]; rows = [3, 3, 2, 1, 1]; i = 0; y = H - 1
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

def mold():   # 과자 교실 막대 틀 (오븐 옆 탁자 위 소품 40 × 24)
    im = Image.new('RGBA', (40, 24)); g = ImageDraw.Draw(im)
    g.polygon([(2, 12), (20, 3), (38, 12), (20, 21)], fill=hx('#B8B8C8'), outline=OL)
    for k in range(5):
        x = 9 + k * 5; y = 8 + k * 2 - 2
        g.line([(x, y), (x + 9, y + 4)], fill=hx('#6A6A80'), width=2)
        if k < 3: g.line([(x, y - 1), (x + 8, y + 3)], fill=hx(['#E8B868', '#8A5232', '#F08AA8'][k]), width=1)
    g.polygon([(2, 12), (20, 21), (20, 23), (2, 14)], fill=hx('#7A7A90'), outline=OL); g.polygon([(20, 21), (38, 12), (38, 14), (20, 23)], fill=hx('#9A9AB0'), outline=OL)
    return im

def lamp_deco():   # 광장 가로등에 매다는 막대과자 장식 (14 × 20)
    im = Image.new('RGBA', (14, 20)); g = ImageDraw.Draw(im); g.line([(7, 0), (7, 4)], fill=OL)
    g.line([(2, 4), (12, 4)], fill=hx('#D8303A'), width=2)
    for i, c in enumerate(['straw', 'milk', 'matcha']):
        s = stick(c, 'rainbow', i).crop((1, 0, 6, 30)).resize((3, 15), Image.NEAREST); im.alpha_composite(s, (2 + i * 4, 5 + (i % 2)))
    return im

if __name__ == '__main__':
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
    P.alpha_composite(mold(), (150, 210)); P.alpha_composite(lamp_deco(), (210, 206))
    P.resize((P.width * 4, P.height * 4), Image.NEAREST).save(O + '/preview.png')
    print('ok')
