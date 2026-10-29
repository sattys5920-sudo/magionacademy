# 오늘의 운세 카드: 메이저 아르카나 22장 + 카드 뒷면 · 변신(morph_art.py)·아기 동물과 같은 도트 그림체 (물체마다 1칸 윤곽선)
#   카드 48×72 (금테 · 위에 로마 숫자 · 가운데 그림 40×52) → out/tarot.png (가로 23칸: 0~21, 뒷면)
import os, math
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 48, 72            # 카드
IX, IY, IW, IH = 4, 11, 40, 52   # 그림 칸
def C(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
OL = C('#1a1024'); HI = C('#ffffff'); EYE = C('#1a1024'); BLUSH = C('#ff9ab8'); SKIN = C('#F6D2B4'); SKIN2 = C('#E8B898')
GOLD, GOLD2, GOLD3 = C('#F2C450'), C('#B8862E'), C('#FFE9A0')

def ell(cx, cy, rx, ry): return {(x, y) for x in range(int(cx - rx - 1), int(cx + rx + 2)) for y in range(int(cy - ry - 1), int(cy + ry + 2)) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
def poly(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; out = set()
    for y in range(int(min(ys)) - 1, int(max(ys)) + 2):
        for x in range(int(min(xs)) - 1, int(max(xs)) + 2):
            px, py, inside, j = x + .5, y + .5, False, len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi: inside = not inside
                j = i
            if inside: out.add((x, y))
    return out
def line(x0, y0, x1, y1, w=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1; out = set()
    for i in range(n + 1):
        t = i / max(1, n); x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for dx in range(w):
            for dy in range(w): out.add((round(x - w / 2 + .5) + dx, round(y - w / 2 + .5) + dy))
    return out
def star(cx, cy, r, r2=None, n=5, rot=-90):
    r2 = r2 or r * .45; pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n); rr = r if i % 2 == 0 else r2; pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return poly(pts)

class Art:   # 그림 칸 (IW×IH): bg 칠 → 물체(윤곽선) 차례로 → 점
    def __init__(s, top, bot=None):
        s.px = {}; s.solid = set()
        for y in range(IH):
            t = y / (IH - 1); a, b = C(top), C(bot or top)
            s.px.update({(x, y): tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,) for x in range(IW)})
    def bg(s, m, c):
        for p in m:
            if 0 <= p[0] < IW and 0 <= p[1] < IH: s.px[p] = C(c) if isinstance(c, str) else c
        return s
    def obj(s, m, c, ol=True, shade=True):   # 윤곽선 + 아래·오른쪽 그늘 + 위·왼쪽 빛 (작은 건 그늘 없이)
        m = {p for p in m if 0 <= p[0] < IW and 0 <= p[1] < IH}; c = C(c) if isinstance(c, str) else c
        if ol:
            for (x, y) in m:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + dx, y + dy)
                    if q not in m and 0 <= q[0] < IW and 0 <= q[1] < IH: s.px[q] = OL
        dk = tuple(round(v * .78) for v in c[:3]) + (255,); lt = tuple(min(255, round(v + (255 - v) * .35)) for v in c[:3]) + (255,)
        big = shade and len(m) >= 18
        for (x, y) in m:
            if big and ((x + 1, y) not in m or (x, y + 1) not in m): s.px[(x, y)] = dk
            elif big and (x - 1, y) not in m and (x, y - 1) not in m: s.px[(x, y)] = lt
            else: s.px[(x, y)] = c
        return s
    def dot(s, pts, c):
        for p in pts:
            if 0 <= p[0] < IW and 0 <= p[1] < IH: s.px[p] = C(c) if isinstance(c, str) else c
        return s
    def stars(s, pts, c='#FFF4C8'): return s.dot(pts, c)
    def face(s, x, y, gap=3, blush=True, mouth=True, closed=False):   # x: 왼쪽 눈
        for ex in (x, x + gap):
            if closed: s.dot([(ex, y + 1)], EYE)
            else: s.dot([(ex, y), (ex, y + 1)], EYE); s.dot([(ex, y)], HI)
        if blush: s.dot([(x - 1, y + 2), (x + gap + 1, y + 2)], BLUSH)
        if mouth: s.dot([(x + gap // 2 + (gap % 2) * 0, y + 2)], EYE)
        return s
    def person(s, cx, top, robe, hair='#5A3A2A', hat=None, arms='down', skin=SKIN, robe2=None, hood=False, h=1.0, closed=False):
        # 귀여운 큰 머리 꼬마: 머리(가로 13) + 동글 몸통. cx: 가운데, top: 머리 맨 위
        hy = top + 6; by0 = hy + 5; bh = max(5, round(9 * h)); by1 = by0 + bh
        body = ell(cx + .5, by0 + bh * .6, 5.2, bh * .62) | rect(cx - 4, by0, cx + 5, by0 + 2)
        if arms == 'up': s.obj(line(cx - 3, by0 + 2, cx - 7, by0 - 3, 2) | line(cx + 4, by0 + 2, cx + 8, by0 - 3, 2), robe, shade=False); s.obj(ell(cx - 7, by0 - 4, 1.6, 1.6) | ell(cx + 8, by0 - 4, 1.6, 1.6), skin, shade=False)
        if arms == 'side': s.obj(ell(cx - 5, by0 + 3, 2, 2.4) | ell(cx + 6, by0 + 3, 2, 2.4), robe, shade=False)
        s.obj(body, robe)
        if robe2: s.dot([(x, y) for (x, y) in body if by0 + 1 <= y <= by0 + 2 and abs(x - cx - .5) <= 3] + [(cx, by0 + 3), (cx + 1, by0 + 3)], robe2)   # 옷깃
        s.dot([(cx - 2, by1), (cx - 1, by1), (cx + 2, by1), (cx + 3, by1)], '#3A2A3A')
        if arms == 'front': s.obj(ell(cx - 1, by0 + 4, 1.6, 1.4) | ell(cx + 2, by0 + 4, 1.6, 1.4), skin, shade=False)
        if arms == 'side': s.dot([(cx - 6, by0 + 5), (cx + 7, by0 + 5)], skin)
        hb = ell(cx + .5, hy - .2, 6.6, 6.2) | rect(cx - 6, hy, cx - 5, hy + 4 if not hood else hy + 5) | rect(cx + 6, hy, cx + 7, hy + 4 if not hood else hy + 5)
        s.obj(hb, robe if hood else hair)
        win = ell(cx + .5, hy + 1.6, 5.1, 4.1); s.obj(win, skin, ol=False, shade=False)
        if not hood: s.dot([(x, y) for (x, y) in win if y <= hy - 2 or (y == hy - 1 and (x - cx) % 3 == 0)], hair)
        if hat == 'witch': s.obj(poly([(cx - 9, hy - 3), (cx + 10, hy - 3), (cx + 5, hy - 6), (cx + 3, hy - 15), (cx - 4, hy - 6)]), '#3A2A63'); s.dot([(x, hy - 5) for x in range(cx - 4, cx + 6)], GOLD)
        elif hat == 'crown': s.obj(poly([(cx - 5, hy - 5), (cx + 6, hy - 5), (cx + 6, hy - 10), (cx + 3, hy - 7), (cx + .5, hy - 11), (cx - 2, hy - 7), (cx - 5, hy - 10)]), GOLD); s.dot([(cx, hy - 7), (cx + 1, hy - 7)], '#E8506A')
        elif hat == 'tiara': s.obj(rect(cx - 4, hy - 7, cx + 5, hy - 6) | {(cx, hy - 8), (cx + 1, hy - 8), (cx, hy - 9), (cx + 1, hy - 9)}, GOLD, shade=False)
        ey = hy + 1
        for ex in (cx - 3, cx + 3):
            if closed: s.dot([(ex, ey + 1), (ex + 1, ey + 1)], EYE)
            else: s.dot([(ex, ey), (ex + 1, ey), (ex, ey + 1), (ex + 1, ey + 1)], EYE); s.dot([(ex, ey)], HI)
        s.dot([(cx - 4, ey + 2), (cx + 5, ey + 2)], BLUSH); s.dot([(cx, ey + 3), (cx + 1, ey + 3)], C('#C0506A'))
        return s
    def render(s):
        im = Image.new('RGBA', (IW, IH)); P = im.load()
        for p, c in s.px.items(): P[p] = c
        return im

ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']
FONT = { 'I': ['1', '1', '1', '1', '1'], 'V': ['101', '101', '101', '101', '010'], 'X': ['101', '101', '010', '101', '101'], '0': ['111', '101', '101', '101', '111'] }
def card(art, num):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); P = im.load()
    for x in range(W):
        for y in range(H):
            edge = x in (0, W - 1) or y in (0, H - 1)
            corner = (x in (0, W - 1) and y in (0, H - 1))
            if corner: continue
            P[x, y] = OL if edge else GOLD2 if x in (1, W - 2) or y in (1, H - 2) else GOLD if x in (2, W - 3) or y in (2, H - 3) else C('#2A1840')
    for x in range(3, W - 3): P[x, 3] = GOLD3   # 금테 위쪽 빛
    im.alpha_composite(art.render(), (IX, IY))
    for x in range(IX - 1, IX + IW + 1): P[x, IY - 1] = OL; P[x, IY + IH] = OL
    for y in range(IY - 1, IY + IH + 1): P[IX - 1, y] = OL; P[IX + IW, y] = OL
    # 로마 숫자 (위 띠 가운데)
    glyphs = [FONT[ch] for ch in num]; tw = sum(len(g[0]) for g in glyphs) + len(glyphs) - 1; x0 = (W - max(0, tw)) // 2
    for g in glyphs:
        for j, row in enumerate(g):
            for i, b in enumerate(row):
                if b == '1': P[x0 + i, 4 + j] = GOLD3
        x0 += len(g[0]) + 1
    # 아래 띠: 작은 장식 (이름은 화면에서 글자로)
    for x in range(10, W - 10): P[x, H - 6] = GOLD2
    for (dx, dy) in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)): P[W // 2 + dx, H - 6 + dy] = GOLD3
    return im

ARTS = []
NIGHT, NIGHT2 = '#1E1638', '#3A2A63'
DUSK, DUSK2 = '#3A2A63', '#B4608A'
DAY, DAY2 = '#7FB8E0', '#CDE8F4'
def ground(a, y, c, c2=None, ol=True): a.obj(rect(0, y, IW - 1, IH - 1), c, ol); c2 and a.dot([(x, y + 1) for x in range(0, IW, 3)], c2); return a

# 0 바보: 보따리를 메고 낭떠러지 끝을 걸어요 · 흰 꽃 · 강아지
a = Art(DAY, DAY2); a.obj(ell(32, 9, 5, 5), '#FFE070'); a.dot([(31, 7)], HI)
a.obj(poly([(0, 40), (26, 40), (30, 51), (0, 51)]), '#7FB06A'); a.dot([(x, 41) for x in range(0, 25, 2)], '#A8D488')
a.obj(line(9, 22, 4, 13, 1), '#8A5A36'); a.obj(ell(3.5, 12.5, 3, 2.5), '#E8506A')
a.person(14, 16, '#F2E8C8', hair='#E8A040', arms='side', robe2='#7FB8E0'); a.obj(ell(20.5, 31.5, 1.5, 1.5) | ell(21.5, 29, 1, 1), '#FFFFFF')
a.obj(ell(26, 37, 3, 2) | ell(28, 34, 2, 2), '#F6F0E6'); a.dot([(28, 34)], EYE); a.dot([(29, 35)], EYE); ARTS.append(a)
# 1 마법사: 고깔모자 · 지팡이를 높이 · 탁자 위 잔·검·별동전
a = Art(NIGHT, NIGHT2); a.stars([(4, 5), (33, 4), (36, 15), (7, 20), (25, 3)])
a.obj(line(27, 21, 31, 6, 1), '#8A5A36'); a.obj(star(31.5, 5.5, 3.5, 1.6), '#FFE070')
a.person(20, 16, '#7A3AB8', hair='#2A1840', hat='witch', arms='up', robe2='#C890FF')
a.obj(rect(4, 38, 35, 41), '#8A5A36'); a.obj(rect(6, 42, 8, 50) | rect(31, 42, 33, 50), '#6A4A34')
a.obj(rect(8, 34, 10, 37) | {(7, 33), (11, 33), (8, 33), (9, 33), (10, 33)}, GOLD); a.obj(line(15, 37, 19, 31, 1), '#C8D8E8'); a.obj(ell(25.5, 36.5, 2.5, 1.5), GOLD); a.dot([(25, 36)], GOLD3); a.obj(rect(29, 33, 31, 37), '#5A3A8A')
ground(a, 51, '#2A1840', ol=False); ARTS.append(a)
# 2 여사제: 검은 기둥 · 흰 기둥 사이 · 초승달 · 두루마리
a = Art(NIGHT, '#2A3A63'); a.stars([(20, 3), (8, 7), (31, 9)])
a.obj(rect(2, 8, 7, 50), '#2A2030'); a.obj(rect(32, 8, 37, 50), '#F2EEE2'); a.dot([(4, 10)], '#F2EEE2'); a.dot([(34, 10)], '#2A2030')
a.obj(ell(20, 8, 4.5, 4.5) - ell(22, 7, 4, 4), '#F2EEE2')
a.person(19, 16, '#4A6AB8', hair='#2A1840', hat='tiara', arms='front', robe2='#F2EEE2'); a.obj(rect(17, 29, 22, 32), '#F6EED8'); ARTS.append(a)
# 3 여황제: 별관 · 밀밭 · 하트 방패
a = Art('#E8A0B0', '#F6D8C8'); a.obj(rect(0, 40, IW - 1, IH - 1), '#D8B460')
for x in range(1, IW, 4): a.obj(line(x, 50, x + 1, 41, 1), '#B8903E', ol=False)
a.person(20, 16, '#E8506A', hair='#E8A040', hat='crown', arms='front', robe2='#FFD060', h=1.1)
a.obj(ell(31, 30, 3.5, 3) | poly([(27.5, 30), (34.5, 30), (31, 35)]), '#FF9AB8'); a.stars([(5, 5), (34, 6), (8, 14)], '#FFFFFF'); ARTS.append(a)
# 4 황제: 돌 왕좌 · 붉은 망토 · 왕관 · 수염
a = Art('#E87A3A', '#F6C060'); a.obj(rect(0, 44, IW - 1, IH - 1), '#8A5A36')
a.obj(rect(9, 14, 30, 46) | rect(7, 10, 11, 18) | rect(28, 10, 32, 18), '#8A8494'); a.dot([(8, 11), (9, 11), (29, 11), (30, 11)], '#C8C2D4')
a.person(20, 16, '#C83A3A', hair='#8A8A8A', hat='crown', arms='side', robe2='#FFD060'); a.obj(poly([(17, 25), (24, 25), (20.5, 30)]), '#D8D8D8')
a.face(18, 21, gap=4, mouth=False); ARTS.append(a)
# 5 교황: 세 겹 관 · 손 들고 · 두 열쇠
a = Art('#6A3A2A', '#B4783E'); a.obj(rect(3, 6, 8, 50) | rect(31, 6, 36, 50), '#8A8494')
a.person(20, 18, '#F2EEE2', hair='#8A8A8A', arms='up', robe2='#C83A3A')
a.obj(poly([(16, 18), (25, 18), (24, 12), (20.5, 6), (17, 12)]), GOLD); a.dot([(x, 16) for x in range(17, 25)] + [(x, 12) for x in range(18, 24)], GOLD2)
a.obj(line(12, 46, 17, 41, 1) | {(11, 46), (11, 47), (12, 47)}, GOLD); a.obj(line(29, 46, 24, 41, 1) | {(30, 46), (30, 47), (29, 47)}, '#C8C2D4'); ARTS.append(a)
# 6 연인: 두 사람 · 위에 큰 하트와 날개 해
a = Art('#9AD0F0', '#F6E0F0'); a.obj(ell(20, 10, 6, 5) | ell(12, 10, 4, 3) | ell(28, 10, 4, 3), '#FFFFFF'); a.obj(ell(17.5, 9, 3, 3) | ell(22.5, 9, 3, 3) | poly([(14.5, 10), (25.5, 10), (20, 16)]), '#E8506A'); a.dot([(16, 8)], HI)
ground(a, 45, '#7FB06A', '#A8D488'); a.person(11, 24, '#4A8AD8', hair='#5A3A2A', arms='side'); a.person(28, 24, '#E880A8', hair='#E8A040', arms='side'); ARTS.append(a)
# 7 전차: 별 지붕 수레 · 흑백 스핑크스 고양이
a = Art(NIGHT, NIGHT2); a.stars([(3, 4), (36, 5), (20, 2)])
a.obj(rect(8, 12, 31, 14), '#3A6AB8'); a.dot([(12, 13), (19, 13), (26, 13)], '#FFE070'); a.obj(rect(9, 15, 10, 30) | rect(29, 15, 30, 30), GOLD2)
a.obj(rect(7, 28, 32, 37), '#8A8494'); a.person(20, 12, '#C8D8E8', hair='#2A1840', hat='crown', arms='down')
a.obj(rect(7, 28, 32, 37), '#8A8494'); a.dot([(x, 32) for x in range(9, 31, 3)], '#C8C2D4')
for cx, col, c2 in ((10, '#2A2030', '#5A4A6A'), (29, '#F2EEE2', '#C8C2D4')):
    a.obj(ell(cx, 44, 5, 4) | ell(cx, 39, 3.5, 3.5) | {(cx - 3, 35), (cx - 2, 36), (cx + 3, 35), (cx + 2, 36)}, col); a.face(cx - 2, 38, gap=4, blush=False)
ground(a, 49, '#2A1840', ol=False); ARTS.append(a)
# 8 힘: 꽃관 소녀가 사자를 쓰다듬어요 · 무한 기호
a = Art('#F6D070', '#F6EED8'); a.obj((ell(17, 6, 3, 2) - ell(17, 6, 1.5, .8)) | (ell(23, 6, 3, 2) - ell(23, 6, 1.5, .8)), GOLD2)
ground(a, 46, '#A8D488'); a.person(12, 15, '#F2EEE2', hair='#E8A040', arms='side', robe2='#E8506A'); a.dot([(9, 15), (11, 14), (14, 14), (16, 15)], '#E8506A')
a.obj(ell(27, 38, 9, 6) | ell(30, 30, 7, 7), '#E8A040'); a.obj(ell(30, 31, 5, 4.5), '#F6C060'); a.face(28, 30, gap=4); a.dot([(36, 44), (20, 44)], '#C88030'); ARTS.append(a)
# 9 은둔자: 눈 덮인 봉우리 · 두건 · 별 등불
a = Art('#1A1430', '#2A3A63'); a.stars([(5, 4), (30, 8), (16, 2), (36, 20)])
a.obj(poly([(-2, 51), (14, 26), (28, 51)]), '#5A6A8A'); a.obj(poly([(10, 51), (30, 22), (44, 51)]), '#6A7A9A'); a.obj(poly([(26.5, 27), (30, 22), (33.5, 27)]), '#F2F4FF')
a.person(16, 20, '#6A6474', arms='down', hood=True, robe2='#4A4454'); a.obj(line(24, 26, 24, 44, 1), '#8A5A36'); a.obj(rect(25, 26, 28, 30), GOLD); a.obj(star(26.5, 28, 2, 1), '#FFF4C8', ol=False); ARTS.append(a)
# 10 운명의 수레바퀴: 큰 바퀴 · 구름 · 고양이가 꼭대기
a = Art('#4A8AD8', '#9AD0F0'); a.obj(ell(6, 46, 7, 4) | ell(34, 47, 7, 4), '#FFFFFF')
a.obj(ell(20, 28, 14, 14), GOLD); a.obj(ell(20, 28, 11, 11), '#E87A3A'); a.obj(ell(20, 28, 4, 4), GOLD)
for k in range(8):
    an = k * math.pi / 4; a.dot(line(20 + math.cos(an) * 4.5, 28 + math.sin(an) * 4.5, 20 + math.cos(an) * 10.5, 28 + math.sin(an) * 10.5, 1), GOLD2)
a.obj(ell(20, 11, 4, 3) | {(17, 8), (17, 7), (23, 8), (23, 7)}, '#2A2030'); a.dot([(18, 10), (22, 10)], '#FFE070'); ARTS.append(a)
# 11 정의: 저울과 칼 · 붉은 옷
a = Art('#7A3AB8', '#C890FF'); a.obj(rect(3, 4, 8, 50) | rect(31, 4, 36, 50), '#8A8494')
a.person(20, 18, '#C83A3A', hair='#2A1840', hat='crown', arms='side', robe2='#FFD060')
a.obj(line(29, 25, 29, 9, 1) | rect(27, 24, 31, 24), '#C8D8E8'); a.obj(line(5, 23, 13, 23, 1) | line(9, 18, 9, 23, 1), GOLD); a.obj(ell(5, 26, 2.5, 1.5) | ell(13, 26, 2.5, 1.5), GOLD); ARTS.append(a)
# 12 매달린 사람: 나무에 거꾸로 · 머리 뒤 후광 · 편안한 얼굴
a = Art('#4A6A5A', '#9AC8A8'); a.obj(rect(3, 2, 36, 5), '#6A4A34'); a.obj(rect(4, 6, 6, 50) | rect(33, 6, 35, 50), '#6A4A34'); a.dot([(8, 4), (14, 3), (27, 4)], '#7FB06A')
a.obj(line(20, 6, 20, 13, 1), '#D8B460')
body = poly([(17, 13), (24, 13), (23, 30), (18, 30)]); a.obj(body, '#4A6AB8'); a.obj(line(20, 13, 25, 18, 2), '#C83A3A')
a.obj(ell(20.5, 36, 6.5, 6.5), '#FFE070', ol=False); a.obj(ell(20.5, 36, 5, 5), SKIN); a.dot([(x, y) for (x, y) in ell(20.5, 36, 5, 5) if y >= 39], '#E8A040'); a.face(18, 34, gap=4, closed=True); ARTS.append(a)
# 13 죽음: 귀여운 해골 기사 · 흰 장미 깃발 · 해가 떠요
a = Art('#2A2040', '#B4608A'); a.obj(ell(32, 40, 7, 7) - rect(0, 41, IW, IH), '#FFB070', ol=False)
ground(a, 41, '#3A2A4A'); a.obj(line(9, 44, 9, 10, 1), '#8A5A36'); a.obj(rect(10, 10, 21, 18), '#2A2030'); a.obj(ell(15.5, 14, 2.5, 2.5), '#F2EEE2'); a.dot([(15, 14)], '#E8506A')
a.obj(poly([(19, 26), (26, 26), (29, 44), (16, 44)]), '#2A2030'); a.obj(ell(22.5, 21.5, 5.5, 5), '#F2EEE2'); a.dot([(20, 21), (21, 21), (24, 21), (25, 21), (20, 22), (25, 22)], '#2A2030'); a.dot([(22, 24), (23, 24)], '#B8B2A0'); ARTS.append(a)
# 14 절제: 날개 천사가 두 잔 사이로 물을 옮겨요 · 한 발은 물에
a = Art('#9AD0F0', '#F6F0E0'); a.obj(ell(7, 18, 6, 10) | ell(33, 18, 6, 10), '#FFFFFF'); a.dot([(5, 14), (35, 14), (6, 20), (34, 20)], '#D8E8F4')
a.obj(rect(0, 44, 18, IH - 1), '#4A8AD8', ol=False); a.obj(rect(19, 44, IW - 1, IH - 1), '#7FB06A')
a.person(20, 12, '#F2EEE2', hair='#E8A040', arms='side', robe2='#FFD060'); a.obj(ell(20.5, 15.5, 7, 7) - ell(20.5, 15.5, 5.6, 5.6), '#FFE070', ol=False)
a.obj(rect(9, 26, 12, 30), GOLD); a.obj(rect(28, 30, 31, 34), GOLD); a.obj(line(12, 29, 28, 32, 1), '#7FD8F0', ol=False); ARTS.append(a)
# 15 악마: 뿔 달린 장난꾸러기 · 쇠사슬 두 꼬마 · 거꾸로 별
a = Art('#2A1020', '#6A2A3A'); a.obj(star(20, 7, 4, 1.8, rot=90), '#FFE070')
a.obj(ell(6, 22, 6, 7) | ell(34, 22, 6, 7), '#4A2A4A'); a.person(20, 14, '#8A2A3A', hair='#2A1020', arms='side', skin=C('#E8706A'))
a.obj({(15, 15), (14, 14), (14, 13), (26, 15), (27, 14), (27, 13)}, '#F2EEE2')
a.obj(rect(13, 38, 28, 41), '#4A4454'); a.person(9, 34, '#6A6474', hair='#5A3A2A', h=.7); a.person(31, 34, '#6A6474', hair='#E8A040', h=.7)
a.obj(line(13, 43, 20, 40, 1) | line(27, 43, 20, 40, 1), '#8A8494', ol=False); ARTS.append(a)
# 16 탑: 번개 맞은 탑 · 왕관이 떨어져요 · 불꽃
a = Art('#1A1028', '#3A2A4A'); a.obj(rect(13, 14, 27, 51), '#8A8494'); a.obj(rect(11, 10, 29, 14), '#9A94A6'); a.dot([(x, 10) for x in range(11, 30, 3)], '#1A1028')
a.obj(rect(18, 20, 22, 25) | rect(18, 32, 22, 37), '#FFB040'); a.obj(poly([(24, 0), (19, 7), (23, 7), (17, 13), (27, 5), (23, 5), (28, 0)]), '#FFF4A0')
a.obj(poly([(9, 8), (14, 8), (14, 4), (12, 6), (11.5, 3), (11, 6), (9, 4)]), GOLD); a.obj(ell(31, 12, 2.5, 3), '#FF7A3A'); a.obj(ell(10, 18, 2, 2.5), '#FF7A3A'); a.dot([(31, 11), (10, 17)], '#FFE070'); ARTS.append(a)
# 17 별: 큰 별 하나와 작은 별 일곱 · 물을 붓는 소녀
a = Art('#1E1638', '#3A4A8A'); a.obj(star(20, 9, 7, 3, n=8), '#FFE070'); a.dot([(20, 9)], HI)
for (x, y) in ((5, 5), (35, 4), (8, 16), (32, 15), (4, 26), (36, 27), (14, 3)): a.obj(star(x, y, 2, .9, n=4), '#FFF4C8', ol=False)
a.obj(rect(0, 42, IW - 1, IH - 1), '#3A6AB8', ol=False); a.dot([(x, 45) for x in range(1, IW, 4)] + [(x + 2, 48) for x in range(0, IW, 4)], '#6A9AE0')
a.person(18, 22, '#B8D8F8', hair='#E8D8A0', arms='side'); a.obj(rect(8, 33, 10, 36) | rect(26, 33, 28, 36), '#E8A040'); a.obj(line(9, 37, 7, 43, 1) | line(27, 37, 29, 43, 1), '#9AE6FF', ol=False); ARTS.append(a)
# 18 달: 얼굴 있는 달 · 두 탑 · 늑대와 강아지 · 물가 가재
a = Art('#1A1430', '#3A3A6A'); a.obj(ell(20, 11, 7, 7), '#F6F0D0'); a.obj(ell(23, 10, 6, 6), '#3A2E5A', ol=False); a.obj(ell(20, 11, 7, 7) - ell(23.5, 10, 6, 6), '#F6F0D0'); a.face(14, 10, gap=2, blush=True, mouth=False)
a.obj(rect(1, 18, 6, 40) | rect(33, 18, 38, 40), '#5A5464'); a.dot([(3, 22), (35, 22)], '#FFD060')
ground(a, 38, '#3A4A3A'); a.obj(rect(14, 46, 26, IH - 1), '#3A6AB8', ol=False)
a.obj(ell(9, 35, 4, 3) | {(6, 31), (7, 32), (11, 31), (11, 32)}, '#8A8494'); a.face(7, 34, gap=3, blush=False)
a.obj(ell(31, 35, 4, 3) | {(28, 32), (34, 32)}, '#E8C090'); a.face(29, 34, gap=3)
a.obj(ell(20, 48, 2.5, 1.5) | {(17, 47), (23, 47)}, '#E8506A'); ARTS.append(a)
# 19 태양: 웃는 해 · 해바라기 · 하얀 조랑말 탄 아이
a = Art('#7FC8F0', '#F6F0C0'); a.obj(ell(20, 12, 8, 8), '#FFD040')
for k in range(12):
    an = k * math.pi / 6; a.obj(line(20 + math.cos(an) * 9.5, 12 + math.sin(an) * 9.5, 20 + math.cos(an) * 12, 12 + math.sin(an) * 12, 1), '#FFB030', ol=False)
a.face(17, 11, gap=5); a.obj(rect(0, 29, IW - 1, 34), '#B8A07A'); a.dot([(x, 29) for x in range(0, IW, 4)], '#D8C09A')
for x in (4, 34): a.obj(line(x, 34, x, 28, 1), '#4A8A3A', ol=False); a.obj(ell(x, 27, 2.5, 2.5), '#FFD040'); a.dot([(x, 27)], '#8A5A36')
ground(a, 46, '#7FB06A'); a.obj(ell(20, 41, 8, 4.5) | rect(13, 43, 14, 47) | rect(26, 43, 27, 47) | ell(27, 36, 3, 3), '#F6F0E6'); a.dot([(28, 35)], EYE); a.person(18, 26, '#E8506A', hair='#E8A040', arms='up', h=.65); ARTS.append(a)
# 20 심판: 구름 위 천사의 나팔 · 깨어나 손 드는 사람들
a = Art('#6A8AC8', '#E8C0D8'); a.obj(ell(20, 12, 13, 5) | ell(10, 10, 6, 4) | ell(30, 10, 6, 4), '#FFFFFF')
a.obj(ell(14, 6, 4, 4), SKIN); a.dot([(x, y) for (x, y) in ell(14, 6, 4, 4) if y <= 4], '#E8A040'); a.face(12, 5, gap=3); a.obj(ell(8, 7, 3, 4) | ell(20, 7, 3, 4), '#F2EEE2')
a.obj(line(17, 9, 28, 14, 1) | ell(29, 15, 2, 2), GOLD); a.obj(rect(0, 42, IW - 1, IH - 1), '#4A8AD8', ol=False)
for cx, col in ((9, '#C8C2D4'), (20, '#E8C8A8'), (31, '#C8C2D4')): a.person(cx, 28, '#F2EEE2', hair='#5A3A2A', arms='up', h=.7); a.obj(rect(cx - 6, 40, cx + 7, 44), '#8A8494')
ARTS.append(a)
# 21 세계: 별 화환 · 가운데 춤추는 사람 · 네 귀퉁이 날개 친구
a = Art('#2A3A8A', '#6A4AB8'); a.stars([(3, 3), (36, 3), (3, 48), (36, 48), (20, 2)])
a.obj(ell(20, 26, 13, 19) - ell(20, 26, 10, 16), '#5FA84A'); a.dot([(x, y) for (x, y) in (ell(20, 26, 13, 19) - ell(20, 26, 10, 16)) if (x * 3 + y) % 7 == 0], '#E8506A')
a.person(20, 15, '#C890FF', hair='#2A1840', arms='up', robe2='#FFE070'); a.obj(line(9, 30, 31, 26, 1), '#E880A8', ol=False)
for (x, y) in ((4, 9), (36, 9), (4, 44), (36, 44)): a.obj(ell(x, y, 2.5, 2.5), '#FFE070'); a.dot([(x - 1, y), (x + 1, y)], EYE)
ARTS.append(a)

def back():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); P = im.load(); base = card(Art('#2A1840'), ''); im.alpha_composite(base)
    a = Art('#2A1840', '#3A2A63')
    a.obj(ell(20, 26, 11, 11), '#3A2A63'); a.obj(ell(20, 26, 8, 8) - ell(23, 24, 7, 7), '#FFE070'); a.obj(star(27, 30, 3, 1.3), '#FFF4C8')
    for (x, y) in ((4, 4), (35, 4), (4, 47), (35, 47), (20, 4), (20, 47), (4, 26), (35, 26)): a.obj(star(x, y, 2, .9, n=4), GOLD, ol=False)
    a.dot([(x, y) for (x, y) in ell(20, 26, 15, 15) - ell(20, 26, 14, 14) if (x + y) % 2 == 0], GOLD2)
    im.alpha_composite(a.render(), (IX, IY))
    for x in range(18, 30):
        for y in range(4, 9): P[x, y] = C('#2A1840') if not (x in (18, 29) or y in (4, 8)) else P[x, y]
    for (dx, dy) in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)): P[24 + dx, 6 + dy] = GOLD3
    return im

NAMES = ['바보', '마법사', '여사제', '여황제', '황제', '교황', '연인', '전차', '힘', '은둔자', '운명의 수레바퀴', '정의', '매달린 사람', '죽음', '절제', '악마', '탑', '별', '달', '태양', '심판', '세계']
if __name__ == '__main__':
    sheet = Image.new('RGBA', (W * 23, H), (0, 0, 0, 0))
    for i, a in enumerate(ARTS): sheet.alpha_composite(card(a, ROMAN[i]), (i * W, 0))
    sheet.alpha_composite(back(), (22 * W, 0)); sheet.save('out/tarot.png'); print('tarot', sheet.size, len(ARTS))
