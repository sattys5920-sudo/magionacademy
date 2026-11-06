# 막대과자의 날 그림: 막대 6 맛 × 뿌리개 · 상자 6 무늬 × 리본 4 색 · 과자 탑 3 단계 · 막대 틀 소품
#   python3 tools/stickday/stick_art.py → tools/stickday/out/*.png (+ 미리보기 preview.png)
import os
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = D + '/out'; os.makedirs(O, exist_ok=True)
OL = (42, 26, 46, 255)
def hx(s, a=255): s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3],)
CHOCO = {'milk': '#8A5232', 'dark': '#4A2A1E', 'straw': '#F08AA8', 'matcha': '#7FB060', 'white': '#F4EEDC', 'ghost': '#9A6AD0'}
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

BOX = {'stripe': ('#F4F0E8', '#E8455A'), 'dot': ('#FFE6EE', '#F06A8A'), 'check': ('#E6F2FF', '#6A9AD8'), 'pumpkin': ('#F08A3A', '#5A3A24'),
       'night': ('#2E2A5A', '#FFE27A'), 'crest': ('#7A2E3A', '#F2C060')}
RIB = {'red': '#D8303A', 'pink': '#FF8EB8', 'gold': '#F2C040', 'sky': '#7FC8F0'}
def box(pat, rib, choco='milk', top='rainbow'):   # 상자 26 × 34: 앞면 무늬 · 위쪽 창으로 막대 끝 · 리본 띠와 나비 매듭
    W, H = 26, 34; im = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(im); a, b = hx(BOX[pat][0]), hx(BOX[pat][1])
    for i in range(4):   # 막대 끝이 위로 삐죽
        s = stick(choco, top, i); im.alpha_composite(s.crop((0, 0, 7, 12)), (2 + i * 4, 0 + (i % 2)))
    x0, y0, x1, y1 = 1, 9, W - 2, H - 1
    g.rectangle([x0, y0, x1, y1], fill=a, outline=OL)
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            u, v = x - x0, y - y0; on = False
            if pat == 'stripe': on = (u + v) % 6 < 2
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
    W, H = 34, 64; im = Image.new('RGBA', (W, H)); order = list(BOX)[:]; ribs = list(RIB)
    k = {1: 4, 2: 7, 3: 10}[n]; rows = [3, 3, 2, 1, 1]; i = 0; y = H - 1
    for row, cnt in enumerate(rows):
        if i >= k: break
        cnt = min(cnt, k - i); bw = 11; x0 = (W - cnt * bw) // 2
        for j in range(cnt):
            b = box(order[(i + row) % 6], ribs[(i * 3) % 4], list(CHOCO)[(i * 5) % 6], list(TOP)[1 + (i * 3) % 7]).resize((11, 14), Image.NEAREST)
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
    sticks = Image.new('RGBA', (8 * 7 * 6, 30))
    for i, c in enumerate(CHOCO):
        for j, t in enumerate(list(TOP)[:7]): pass
    S = Image.new('RGBA', (6 * 8 * 8, 30))
    for i, c in enumerate(CHOCO):
        for j, t in enumerate(TOP): S.alpha_composite(stick(c, t, j), ((i * 8 + j) * 8, 0))
    S.save(O + '/sticks.png')
    B = Image.new('RGBA', (6 * 4 * 28, 34))
    for i, p in enumerate(BOX):
        for j, r in enumerate(RIB): B.alpha_composite(box(p, r, list(CHOCO)[(i + j) % 6], list(TOP)[1 + (i * 2 + j) % 7]), ((i * 4 + j) * 28, 0))
    B.save(O + '/boxes.png')
    T = Image.new('RGBA', (3 * 36, 64))
    for n in (1, 2, 3): T.alpha_composite(tower(n), ((n - 1) * 36, 0))
    T.save(O + '/tower.png'); mold().save(O + '/mold.png'); lamp_deco().save(O + '/lamp.png')
    # 미리보기: 막대 6 맛 (뿌리개 알록) · 상자 6 × 리본 4 · 탑 3 단계 · 틀 · 가로등 장식
    P = Image.new('RGBA', (300, 210), hx('#1E1830')); g = ImageDraw.Draw(P)
    for i, c in enumerate(CHOCO):
        for j, t in enumerate(['rainbow', 'star', 'gold']): P.alpha_composite(stick(c, t, j), (8 + i * 26 + j * 8, 8))
    for i, p in enumerate(BOX):
        for j, r in enumerate(RIB[:2] if False else ['red', 'gold']): P.alpha_composite(box(p, r, list(CHOCO)[(i + j) % 6], list(TOP)[1 + (i + j) % 7]), (8 + i * 48 + j * 22, 48) if False else (8 + (i * 2 + j) * 24, 48))
    for n in (1, 2, 3): P.alpha_composite(tower(n), (8 + (n - 1) * 40, 100))
    P.alpha_composite(mold(), (140, 140)); P.alpha_composite(lamp_deco(), (196, 136))
    P.resize((P.width * 4, P.height * 4), Image.NEAREST).save(O + '/preview.png')
    print('ok')
