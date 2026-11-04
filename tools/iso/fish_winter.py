# 늦가을·첫겨울 물고기 20종: 기존 물고기 그림(fish.png 앞 60칸)을 바탕으로 색을 바꾸고 계절 장식을 덧그려요
# python3 tools/iso/fish_winter.py --preview DIR   → DIR/fish_new20.png · fish_new20_x4_lbl.png · fish_new20_cmp.png
# python3 tools/iso/fish_winter.py --apply         → public/art/fish.png 앞 103칸 + 새 20칸 = 123칸 (3936×32)
#   칸 순서 = tools/dex2_spec.json 의 "fish" 순서
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fish_rare import recolor, glow, body_mask, PAL, N, OUT, lum   # fish_rare 는 import 만으로는 아무것도 저장하지 않아요

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = os.path.join(ROOT, 'public', 'art', 'fish.png')
KEEP = 103

PAL.update({
  'autumn':   [(90, 30, 14), (176, 70, 24), (236, 130, 40), (255, 206, 110)],
  'mist':     [(104, 112, 130), (158, 166, 182), (206, 212, 224), (242, 246, 252)],
  'chestnut': [(58, 28, 16), (108, 56, 28), (156, 90, 46), (204, 144, 90)],
  'killi':    [(40, 70, 100), (80, 130, 160), (150, 195, 215), (225, 242, 250)],
  'yuzu':     [(140, 96, 10), (222, 168, 20), (255, 218, 60), (255, 246, 170)],
  'cocoa':    [(48, 24, 16), (94, 52, 32), (142, 90, 58), (192, 142, 104)],
  'lantern':  [(130, 38, 10), (222, 88, 20), (255, 148, 48), (255, 222, 140)],
  'snow':     [(104, 136, 180), (176, 204, 232), (226, 238, 252), (255, 255, 255)],
  'owl':      [(64, 40, 24), (124, 82, 46), (186, 138, 84), (236, 208, 160)],
  'cream':    [(138, 98, 68), (206, 168, 118), (244, 222, 178), (255, 248, 226)],
  'ice':      [(48, 108, 160), (108, 188, 230), (184, 234, 250), (240, 253, 255)],
  'mistviolet': [(88, 78, 120), (138, 128, 170), (188, 180, 214), (234, 230, 248)],
  'storm':    [(14, 20, 52), (28, 44, 100), (54, 84, 156), (112, 154, 214)],
  'silverblue': [(38, 54, 96), (88, 114, 164), (158, 184, 222), (230, 240, 252)],
  'whitesky': [(78, 128, 190), (138, 190, 236), (204, 232, 252), (255, 255, 255)],
  'fog':      [(66, 86, 120), (124, 150, 182), (192, 212, 234), (246, 252, 255)],
  'wisp':     [(8, 16, 30), (18, 40, 66), (36, 74, 106), (82, 132, 164)],
  'silver':   [(88, 98, 128), (158, 168, 196), (216, 224, 240), (255, 255, 255)],
})

WHITE = (255, 255, 255)

# ── 작은 그리기 도구 ─────────────────────────────────────────
def inb(x, y): return 0 <= x < N and 0 <= y < N

def put(px, x, y, c, a=255):
    if inb(x, y): px[x, y] = tuple(c[:3]) + (a,)

def blend(px, x, y, c, a):
    """(x,y) 위에 색 c 를 불투명도 a(0~255)로 얹어요"""
    if not inb(x, y): return
    r, g, b, A = px[x, y]
    if A == 0: px[x, y] = tuple(c) + (a,); return
    t = a / 255
    px[x, y] = (int(r + (c[0] - r) * t), int(g + (c[1] - g) * t), int(b + (c[2] - b) * t), max(A, a))

def is_out(c): return c[3] > 0 and (lum(c) < 40)

def interior(im):
    """몸통 안쪽(윤곽선·눈 아닌 칸, 네 이웃이 모두 몸통)"""
    px = im.load(); m = body_mask(im); s = set()
    for (x, y) in m:
        if is_out(px[x, y]): continue
        if all((x + dx, y + dy) in m and not is_out(px[x + dx, y + dy]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            s.add((x, y))
    return s

def shape(im, pts, outline=True):
    """pts = {(x,y): 색} 을 칠하고, 비어 있는 이웃에 윤곽선을 둘러요"""
    px = im.load()
    for (x, y), c in pts.items(): put(px, x, y, c)
    if outline:
        for (x, y) in pts:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p not in pts and inb(*p) and px[p][3] == 0: put(px, p[0], p[1], OUT)

def grid(rows, x0, y0, cmap):
    pts = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in cmap: pts[(x0 + i, y0 + j)] = cmap[ch]
    return pts

def erase(im, x0, y0, x1, y1):
    px = im.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if inb(x, y): px[x, y] = (0, 0, 0, 0)

def strip_small(im, maxn=12):
    """몸통과 떨어진 작은 조각(반짝이 등)을 지워요"""
    px = im.load(); m = body_mask(im); seen = set()
    for p in list(m):
        if p in seen: continue
        comp = [p]; seen.add(p); st = [p]
        while st:
            x, y = st.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (x + dx, y + dy)
                    if q in m and q not in seen: seen.add(q); comp.append(q); st.append(q)
        if len(comp) <= maxn:
            for q in comp: px[q] = (0, 0, 0, 0)
    return im

def keep_main(im, minsize=30):
    """윤곽선 아닌 칸끼리(4방향) 이어진 덩어리 중 큰 것만 남기고, 그 덩어리에 붙은 윤곽선만 남겨요
    (몸통에서 떨어진 별가루·기운·반짝이를 지울 때)"""
    px = im.load(); m = body_mask(im)
    fill = {p for p in m if not is_out(px[p])}; seen = set(); keep = set()
    for p in fill:
        if p in seen: continue
        comp = [p]; seen.add(p); st = [p]
        while st:
            x, y = st.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q in fill and q not in seen: seen.add(q); comp.append(q); st.append(q)
        if len(comp) >= minsize: keep.update(comp)
    for p in m:
        if p in keep: continue
        if is_out(px[p]) and any((p[0] + dx, p[1] + dy) in keep for dx in (-1, 0, 1) for dy in (-1, 0, 1)): continue
        px[p] = (0, 0, 0, 0)
    return im

def soft_glow(im, col, a=110, ring2=True):
    """윤곽 바깥으로 1~2칸 부드러운 빛"""
    m = body_mask(im); px = im.load(); ring = set()
    for (x, y) in m:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if inb(*p) and p not in m: ring.add(p)
    for p in ring: put(px, p[0], p[1], col, a)
    if ring2:
        ring2s = set()
        for (x, y) in ring:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if inb(*p) and p not in m and p not in ring: ring2s.add(p)
        for p in ring2s: put(px, p[0], p[1], col, a // 3)
    return im

def empty_near(im, x, y, r=1):
    px = im.load()
    return all(not inb(x + dx, y + dy) or px[x + dx, y + dy][3] == 0 for dx in range(-r, r + 1) for dy in range(-r, r + 1))

def plus_spark(im, x, y, core=WHITE, arm=(170, 225, 250), force=False):
    px = im.load()
    if not force and not empty_near(im, x, y, 1): return False
    put(px, x, y, core)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): put(px, x + dx, y + dy, arm, 230)
    return True

def snowflake(im, x, y, c=WHITE, c2=(170, 215, 250)):
    """5×5 눈꽃: 가운데 + 네 팔 + 대각 끝"""
    px = im.load()
    put(px, x, y, c)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): put(px, x + dx, y + dy, c2)
    for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)): put(px, x + dx, y + dy, c, 230)
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)): put(px, x + dx, y + dy, c2, 150)

def translucent(im, a=205):
    px = im.load()
    for (x, y) in interior(im):
        r, g, b, A = px[x, y]
        if A == 255: px[x, y] = (r, g, b, a)

def top_rim(im, col=WHITE, a=220):
    """윗면 가장자리(바로 위가 윤곽선/빈칸)를 서리처럼 밝혀요"""
    px = im.load(); inn = interior(im) | {p for p in body_mask(im) if not is_out(px[p])}
    for (x, y) in inn:
        if y > 0 and (px[x, y - 1][3] == 0 or is_out(px[x, y - 1])) and lum(px[x, y]) > 40:
            blend(px, x, y, col, a)

def fog_wisp(im, x0, y, length, col=(232, 238, 246), a=150, over=True):
    """옆으로 흐르는 안개 한 줄기 (가운데 진하고 끝은 옅게)"""
    px = im.load()
    for i in range(length):
        x = x0 + i; yy = y + (1 if (i // 3) % 2 else 0)
        if not inb(x, yy): continue
        k = min(i, length - 1 - i)
        aa = a if k >= 2 else int(a * (0.45 + 0.27 * k))
        if px[x, yy][3] == 0: put(px, x, yy, col, aa)
        elif over: blend(px, x, yy, col, aa // 2)

def dots(im, pts, col, only_inside=True):
    px = im.load(); inn = interior(im)
    for p in pts:
        if not only_inside or p in inn: put(px, p[0], p[1], col)

# ── 20종 ────────────────────────────────────────────────────
def f_frostcarp(c):        # 서리 붕어 (base 1) — 서리 하늘색, 잎은 얼음 잎, 서리 알갱이
    c = recolor(c, 'frost')
    dots(c, [(12, 12), (17, 10), (21, 13), (14, 17), (19, 19), (10, 21), (23, 18)], WHITE)
    top_rim(c, WHITE, 140)
    plus_spark(c, 28, 4); plus_spark(c, 3, 27)
    return c

def f_leafloach(c):        # 낙엽 미꾸라지 (base 4) — 단풍 주황-갈색 + 잎 무늬
    c = recolor(c, 'autumn'); px = c.load()
    R, Y, V = (196, 40, 24), (255, 200, 60), (120, 24, 14)
    inn = interior(c)
    for (x, y) in [(8, 13), (14, 13), (19, 17), (24, 21)]:     # 몸통 위 작은 잎 (빨간 잎 + 노란 잎맥)
        for dx, dy, col in ((0, -1, R), (-1, 0, R), (1, 0, R), (0, 1, V), (0, 0, Y)):
            if (x + dx, y + dy) in inn: put(px, x + dx, y + dy, col)
    # 위쪽 빈 곳에 떨어지는 단풍잎 하나 (세 갈래 잎 + 꼭지)
    leaf = grid(["...r...",
                 "r.rRr.r",
                 "RrrYrrR",
                 ".rrYrr.",
                 "rr.Y.rr",
                 "...b..."], 21, 1, {'r': (222, 70, 30), 'R': (255, 130, 50), 'Y': (255, 196, 70), 'b': (120, 60, 30)})
    shape(c, leaf)
    return c

def f_mistsmelt(c):        # 안개 빙어 (base 5) — 촛불 떼고 회백색 반투명 + 등뼈 + 안개
    erase(c, 7, 0, 16, 13)
    px = c.load()
    for x in range(8, 15): put(px, x, 14, OUT)
    c = recolor(c, 'mist'); px = c.load()
    inn = interior(c)
    for x in range(9, 24):                                # 비치는 등뼈
        if (x, 18) in inn: put(px, x, 18, (150, 158, 176))
        if x % 2 == 0:
            for y in (17, 19):
                if (x, y) in inn: put(px, x, y, (176, 184, 200))
    translucent(c, 200)
    fog_wisp(c, 0, 10, 12, a=140); fog_wisp(c, 14, 8, 10, a=120)
    fog_wisp(c, 4, 25, 14, a=150); fog_wisp(c, 18, 27, 12, a=120)
    return c

def f_chestcrab(c):        # 군밤 게 (base 6) — 밤색 + 등에 X자 칼집, 노란 속살
    c = recolor(c, 'chestnut'); px = c.load()
    Y, Y2, D = (255, 214, 90), (232, 168, 50), (60, 30, 14)
    cx, cy = 17, 15
    for d in range(-3, 4):
        for (x, y) in ((cx + d, cy + d), (cx + d, cy - d)):
            put(px, x, y, Y if abs(d) < 2 else Y2)
    put(px, cx, cy, (255, 240, 160))
    for (x, y) in ((cx - 4, cy - 3), (cx + 4, cy - 3), (cx - 4, cy + 3), (cx + 4, cy + 3)): put(px, x, y, D)
    # 밤 아랫부분 밝은 베이지 띠
    inn = interior(c)
    for x in range(8, 28):
        for y in (21, 22):
            if (x, y) in inn: blend(px, x, y, (226, 186, 128), 170)
    # 따끈한 김
    for (x, y, a) in ((15, 3, 150), (16, 2, 110), (19, 4, 140), (20, 3, 100)): put(px, x, y, (240, 240, 240), a)
    return c

def f_mufflerkilli(c):     # 목도리 송사리 (base 3) — 은청색 + 빨간 줄무늬 목도리
    c = recolor(c, 'killi'); px = c.load()
    R, R2, W = (214, 40, 46), (150, 22, 34), (250, 240, 228)
    pts = {}
    for y in range(11, 22):                              # 목에 감긴 띠: 빨강 바탕 + 흰 가로 줄
        stripe = W if y % 3 == 1 else R
        for x in (9, 10, 11):
            col = stripe
            if x == 11: col = R2 if stripe == R else (214, 196, 196)
            if x == 9 and stripe == R: col = (240, 80, 80)
            pts[(x, y)] = col
    # 배 아래로 늘어진 끝자락 (뒤로 살짝 휘날림)
    end = [(11, 22), (12, 22), (12, 23), (13, 23), (13, 24), (14, 24), (14, 25), (15, 25)]
    for p in end: pts[p] = W if (p[1] % 3 == 1) else (R2 if p[0] - p[1] == -10 else R)
    for p in ((14, 26), (16, 25), (16, 26)): pts[p] = (250, 220, 210)     # 술
    shape(c, pts)
    for x in (9, 10, 11):                                # 등 위 윤곽 정리
        if px[x, 10][3] == 0 or not is_out(px[x, 10]): put(px, x, 10, OUT)
    return c

def f_yuzupuff(c):         # 유자 복어 (base 16) — 유자 노랑 + 귤껍질 점 + 꼭지 잎
    c = recolor(c, 'yuzu'); px = c.load()
    dots(c, [(9, 9), (13, 6), (19, 7), (22, 11), (8, 14), (11, 20), (16, 22), (21, 19), (23, 15), (14, 12)], (214, 150, 20))
    leaf = grid(["..gG",
                 ".gGG",
                 "bgg."], 16, 0, {'g': (70, 150, 50), 'G': (130, 200, 80), 'b': (110, 80, 30)})
    shape(c, leaf)
    return c

def f_cocoaeel(c):         # 코코아 뱀장어 (base 21) — 코코아 갈색 + 크림(마시멜로) 점 + 김
    c = recolor(c, 'cocoa'); px = c.load()
    inn = interior(c)
    for (x, y) in sorted(inn):                           # 고르게 흩뿌린 크림 점
        if (x * 3 + y * 5) % 9 == 0 and lum(px[x, y]) < 150 and x > 6:
            put(px, x, y, (252, 240, 216))
    for (x, y, a) in ((10, 6, 140), (11, 5, 170), (10, 4, 120), (11, 3, 90), (19, 4, 150), (18, 3, 120), (19, 2, 90)):
        put(px, x, y, (245, 240, 236), a)
    return c

def f_lanternsquid(c):     # 꽈리 오징어 (base 17) — 주황 꽈리 등불 + 세로 골 + 꼭지 + 은은한 빛
    c = recolor(c, 'lantern'); px = c.load()
    inn = interior(c)
    for x in (11, 19):                                   # 꽈리 골(세로 줄)
        for y in range(3, 14):
            if (x, y) in inn: put(px, x, y, (196, 70, 18))
    for y in range(5, 12):                               # 속 불빛
        for x in range(13, 18):
            if (x, y) in inn: blend(px, x, y, (255, 246, 190), 120 if x in (13, 17) else 200)
    for p in ((15, 1), (14, 2), (15, 2), (16, 2)): put(px, *p, (100, 140, 50))
    soft_glow(c, (255, 160, 60), 90)
    return c

def f_snowflat(c):         # 눈송이 가자미 (base 27) — 흰 바탕 + 눈송이 점, 버섯은 눈더미
    c = recolor(c, 'snow'); px = c.load()
    for y in range(8, 14):                               # 버섯 갓 → 소복한 눈
        for x in range(9, 22):
            if px[x, y][3] and not is_out(px[x, y]):
                px[x, y] = (255, 255, 255, 255) if y < 11 else (220, 236, 252, 255)
    B = (120, 170, 226)
    for (x, y) in [(10, 19), (16, 21), (22, 18), (13, 24), (25, 23), (19, 17)]:
        inn = interior(c)
        if (x, y) in inn:
            put(px, x, y, WHITE)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (x + dx, y + dy) in inn: put(px, x + dx, y + dy, B)
    snowflake(c, 4, 4); snowflake(c, 28, 7)
    return c

def f_owlcat(c):           # 부엉이 메기 (base 8) — 갈색 깃털 무늬 + 큰 눈
    c = recolor(c, 'owl'); px = c.load()
    inn = interior(c); D, L = (88, 54, 30), (236, 210, 164)
    for (x0, y0) in [(14, 18), (19, 17), (24, 18), (16, 21), (21, 21), (18, 10), (23, 8)]:   # V 깃털
        for (dx, dy) in ((-1, -1), (0, 0), (1, -1)):
            if (x0 + dx, y0 + dy) in inn: put(px, x0 + dx, y0 + dy, D)
        if (x0, y0 - 1) in inn: put(px, x0, y0 - 1, L)
    for (x, y) in inn:                                   # 가슴 쪽 밝은 솜털
        if y >= 19 and x < 20 and (x + y) % 2 == 0: blend(px, x, y, L, 120)
    eye = grid([".OOO.",
                "OYYYO",
                "OYkYO",
                "OYYwO",
                ".OOO."], 6, 13, {'O': OUT, 'Y': (255, 196, 40), 'k': (20, 10, 10), 'w': WHITE})
    for p, col in eye.items(): put(px, p[0], p[1], col)
    put(px, 8, 14, (255, 236, 120))
    return c

def f_frostshrimp(c):      # 서리 새우 (base 14) — 서리 하늘색 + 얼음 고드름 + 반짝
    c = recolor(c, 'frost'); px = c.load()
    for y in range(1, 6):                                # 등불 구슬 → 얼음 결정
        for x in range(1, 7):
            if px[x, y][3] and not is_out(px[x, y]):
                px[x, y] = (255, 255, 255, 255) if (x + y) % 3 else (150, 220, 250, 255)
    for (x, y, h) in ((8, 24, 2), (11, 24, 3), (14, 24, 2)):   # 다리 끝 고드름
        for k in range(h):
            if px[x, y + k][3] == 0: put(px, x, y + k, (200, 240, 255) if k < h - 1 else WHITE, 230)
    dots(c, [(19, 9), (23, 12), (24, 18), (20, 21), (12, 10)], WHITE)
    plus_spark(c, 28, 4); plus_spark(c, 27, 27)
    return c

def f_candleray(c):        # 촛불 가오리 (base 20) — 크림색 + 꼬리 끝 촛불
    c = recolor(c, 'cream'); px = c.load()
    candle = grid(["..f..",
                   ".fFf.",
                   ".fYf.",
                   "..k..",
                   ".wW..",
                   ".wW..",
                   ".wW.."], 27, 7, {'f': (255, 140, 40), 'F': (255, 236, 140), 'Y': (255, 210, 80),
                                      'k': (60, 40, 30), 'w': (255, 250, 236), 'W': (226, 204, 170)})
    flame = {p: col for p, col in candle.items() if p[1] < 10}
    stick = {p: col for p, col in candle.items() if p[1] >= 10}
    shape(c, stick)
    for p, col in flame.items(): put(px, p[0], p[1], col)
    for p in ((29, 6), (28, 7), (30, 7), (27, 8), (31, 8), (27, 9), (31, 9)):   # 불빛 번짐
        if px[p][3] == 0: put(px, p[0], p[1], (255, 190, 90), 110)
    # 몸에 비친 따뜻한 불빛
    inn = interior(c)
    for (x, y) in inn:
        if x > 18 and y < 18: blend(px, x, y, (255, 200, 120), 60)
    return c

def f_icehorse(c):         # 얼음 해마 (base 36) — 얼음 투명 하늘색 + 결정 면 + 반짝
    c = recolor(c, 'ice'); px = c.load()
    inn = interior(c)
    for (x, y) in inn:                                   # 사선 결정 면
        if (x + y) % 6 == 0: blend(px, x, y, WHITE, 190)
        elif (x + y) % 6 == 1: blend(px, x, y, (210, 245, 255), 110)
    translucent(c, 190)
    for (x, y) in body_mask(c):                          # 윤곽선도 얼음빛(짙은 청록)으로 — 유리처럼
        if px[x, y][:3] == OUT: px[x, y] = (34, 74, 120, 255)
    for (x, y) in ((13, 0), (17, 1), (21, 3)):           # 머리·등의 얼음 가시
        if px[x, y][3] == 0: put(px, x, y, (220, 248, 255))
    plus_spark(c, 28, 16); plus_spark(c, 4, 4, force=False)
    return c

def f_mistjelly(c):        # 안개 해파리 (base 11) — 희뿌연 보라-회색 + 안개
    c = recolor(c, 'mistviolet')
    translucent(c, 200)
    fog_wisp(c, 0, 23, 13, a=150); fog_wisp(c, 16, 26, 15, a=150)
    fog_wisp(c, 6, 29, 14, a=120); fog_wisp(c, 20, 20, 12, a=110)
    return c

def f_stormocto(c):        # 빗줄기 문어 (base 30) — 짙은 남색 + 빗방울 무늬 + 빗줄기
    c = recolor(c, 'storm'); px = c.load()
    D, D2, D3 = (120, 190, 250), (230, 246, 255), (80, 140, 220)
    for (x, y) in [(11, 8), (20, 7), (15, 4), (9, 20), (24, 19), (17, 22)]:
        for dx, dy, col in ((0, 0, D), (-1, 1, D), (0, 1, D2), (1, 1, D), (-1, 2, D3), (0, 2, D), (1, 2, D3)):
            put(px, x + dx, y + dy, col)
    for (x, y) in [(4, 2), (8, 1), (2, 10), (29, 17), (27, 26), (2, 24)]:   # 사선 빗줄기
        for k in range(3):
            if inb(x - k, y + k) and px[x - k, y + k][3] == 0: put(px, x - k, y + k, (170, 210, 250), 220 - k * 60)
    return c

def f_wintermarlin(c):     # 겨울 청새치 (base 44) — 은청색 + 서리 테두리 + 반짝
    c = strip_small(c, 6)
    c = recolor(c, 'silverblue')
    top_rim(c, (240, 250, 255), 220)
    dots(c, [(12, 14), (17, 11), (20, 15), (24, 12), (15, 17)], WHITE)
    snowflake(c, 4, 4); plus_spark(c, 5, 26); plus_spark(c, 20, 28)
    return c

def f_frostwhale(c):       # 서리 꼬마 고래 (base 51) — 흰-하늘 + 눈꽃 반짝 + 빛
    c = keep_main(c, 30)                                  # 별 지팡이·별가루 떼기
    c = recolor(c, 'whitesky')
    top_rim(c, WHITE, 180)
    soft_glow(c, (190, 235, 255), 130, ring2=False)
    snowflake(c, 5, 5); plus_spark(c, 13, 3, force=True); plus_spark(c, 28, 28, force=True)
    return c

def f_mistlord(c):         # 안개 호수의 정령 (base 58) — 안개빛 + 빛남, 체크무늬 기운은 안개로
    c = keep_main(c, 30)                                  # 체크무늬 기운·빛줄기 떼고 몸만
    px = c.load(); gold = {p for p in body_mask(c) if px[p][0] > 190 and px[p][2] < 130}
    c = recolor(c, 'fog'); px = c.load(); aura = set()
    for p in gold: px[p] = (255, 250, 214, 255) if lum(px[p]) > 200 else (214, 232, 255, 255)   # 왕관은 진줏빛
    for (x, y) in interior(c):
        if (x, y) not in aura and px[x, y][3] == 255: px[x, y] = px[x, y][:3] + (225,)
    soft_glow(c, (220, 236, 255), 130, ring2=False)
    fog_wisp(c, 0, 27, 13, a=160); fog_wisp(c, 17, 29, 14, a=150); fog_wisp(c, 20, 2, 11, a=130); fog_wisp(c, 0, 4, 9, a=120)
    return c

def f_wispshark(c):        # 도깨비불 상어 (base 54) — 검푸른 + 청록 불꽃 + 도깨비불 구슬
    c = strip_small(c, 8)
    c = recolor(c, 'wisp'); px = c.load()
    T, T2, T3 = (60, 230, 200), (150, 255, 230), (230, 255, 248)
    m = body_mask(c); top = {}
    for (x, y) in m: top[x] = min(top.get(x, 99), y)
    for i, x in enumerate(sorted(top)[3:-3:4]):          # 등 위 청록 불꽃
        y0 = top[x] - 1
        for k in range(2 + i % 2):
            put(px, x, y0 - k, T3 if k == 0 else T, 255 if k == 0 else 210)
    soft_glow(c, (60, 220, 200), 100)
    for (x, y) in ((4, 4), (3, 27), (28, 28)):           # 도깨비불 구슬
        put(px, x, y, T3); put(px, x + 1, y, T2); put(px, x, y + 1, T2); put(px, x + 1, y + 1, T)
        put(px, x, y - 1, T, 200); put(px, x + 1, y - 2, T, 140)
    return c

def f_winterking(c):       # 겨울 잉어왕 (base 59) — 은백색 + 금빛 왕관 + 반짝
    erase(c, 3, 0, 9, 8)
    px = c.load()
    for x in range(3, 9):
        if px[x, 9][3] and not is_out(px[x, 9]): put(px, x, 9, OUT)
    px = c.load(); spots = set()
    for (x, y) in body_mask(c):                         # 주황 무늬 자리 → 얼음 파랑 무늬
        r, g, b, a = px[x, y]
        if r > 180 and b < 120 and r - b > 90: spots.add((x, y))
    c = recolor(c, 'silver'); px = c.load()
    for (x, y) in spots:
        L = lum(px[x, y]); px[x, y] = ((96, 150, 226, 255) if L < 200 else (150, 196, 246, 255))
    crown = grid(["y..y..y",
                  "yY.yY.y",
                  "GYGYGYG",
                  "GrGbGrG",
                  "ggggggg"], 3, 4, {'y': (255, 240, 150), 'Y': (255, 210, 70), 'G': (232, 170, 40),
                                     'g': (170, 110, 26), 'r': (220, 40, 60), 'b': (70, 140, 240)})
    shape(c, crown)
    soft_glow(c, (255, 232, 150), 120, ring2=False)
    return c

FUNCS = [f_frostcarp, f_leafloach, f_mistsmelt, f_chestcrab, f_mufflerkilli, f_yuzupuff, f_cocoaeel, f_lanternsquid,
         f_snowflat, f_owlcat, f_frostshrimp, f_candleray, f_icehorse, f_mistjelly, f_stormocto, f_wintermarlin,
         f_frostwhale, f_mistlord, f_wispshark, f_winterking]

def load_spec():
    with open(os.path.join(ROOT, 'tools', 'dex2_spec.json'), encoding='utf-8') as f: rows = json.load(f)['fish']
    out = []
    for r in rows:
        b = int(r[6].split('base', 1)[1].strip().split()[0])
        out.append((r[0], r[1], b))
    return out

def make_cells():
    src = Image.open(SHEET).convert('RGBA')
    spec = load_spec()
    assert len(spec) == len(FUNCS), (len(spec), len(FUNCS))
    cells = []
    for (fid, name, b), fn in zip(spec, FUNCS):
        assert fn.__name__ == fid, (fn.__name__, fid)
        cells.append(fn(src.crop((b * N, 0, b * N + N, N)).copy()))
    return src, spec, cells

def find_font():
    try:
        out = subprocess.run(['fc-list', ':lang=ko', 'file'], capture_output=True, text=True).stdout
        files = [l.split(':')[0].strip() for l in out.splitlines() if l.strip()]
        files.sort(key=lambda f: (0 if ('Nanum' in f or 'Noto' in f or 'wqy' in f) else 1, 'unifont' in f))
        return files[0] if files else None
    except Exception:
        return None

def preview(d):
    os.makedirs(d, exist_ok=True)
    src, spec, cells = make_cells()
    strip = Image.new('RGBA', (len(cells) * N, N), (0, 0, 0, 0))
    for k, c in enumerate(cells): strip.paste(c, (k * N, 0))
    strip.save(os.path.join(d, 'fish_new20.png'))
    fp = find_font(); font = ImageFont.truetype(fp, 14) if fp else None
    per, sc, lab = 10, 4, (20 if font else 0)
    W, H = N * sc + 8, N * sc + 8 + lab
    rows = (len(cells) + per - 1) // per
    big = Image.new('RGBA', (per * W, rows * H), (46, 38, 66, 255)); dr = ImageDraw.Draw(big)
    for k, c in enumerate(cells):
        x0, y0 = (k % per) * W + 4, (k // per) * H + 4
        u = c.resize((N * sc, N * sc), Image.NEAREST); big.paste(u, (x0, y0), u)
        if font:
            t = f'{k} {spec[k][1]}'
            tw = dr.textlength(t, font=font)
            dr.text((x0 + (N * sc - tw) / 2, y0 + N * sc + 2), t, font=font, fill=(240, 236, 250))
    big.save(os.path.join(d, 'fish_new20_x4_lbl.png'))
    # 비교: [바탕 | 새 물고기] 짝, 한 줄에 5쌍
    per, sc = 5, 4; PW = 2 * N * sc + 24; PH = N * sc + 8 + lab
    cmp_ = Image.new('RGBA', (per * PW, ((len(cells) + per - 1) // per) * PH), (46, 38, 66, 255)); dr = ImageDraw.Draw(cmp_)
    for k, c in enumerate(cells):
        b = spec[k][2]; x0, y0 = (k % per) * PW + 4, (k // per) * PH + 4
        bc = src.crop((b * N, 0, b * N + N, N)).resize((N * sc, N * sc), Image.NEAREST)
        cmp_.paste(bc, (x0, y0), bc)
        u = c.resize((N * sc, N * sc), Image.NEAREST); cmp_.paste(u, (x0 + N * sc + 8, y0), u)
        if font:
            dr.text((x0, y0 + N * sc + 2), f'b{b} → {spec[k][1]}', font=font, fill=(240, 236, 250))
    cmp_.save(os.path.join(d, 'fish_new20_cmp.png'))
    # 시트에 붙인 모습(바탕 60 + 희귀 끝 몇 칸 + 새 20칸) 확인용
    ctx = Image.new('RGBA', (30 * N * 2, N * 2), (60, 70, 90, 255))
    ctx_cells = [src.crop((i * N, 0, i * N + N, N)) for i in range(93, 103)] + cells
    for k, c in enumerate(ctx_cells):
        u = c.resize((N * 2, N * 2), Image.NEAREST); ctx.paste(u, (k * N * 2, 0), u)
    ctx.save(os.path.join(d, 'fish_new20_ctx.png'))
    print('미리보기 저장:', d)

def apply():
    src, spec, cells = make_cells()
    if src.width < KEEP * N: raise SystemExit(f'fish.png 가 {src.width // N}칸이에요 (103칸 이상이어야 해요)')
    out = Image.new('RGBA', ((KEEP + len(cells)) * N, N), (0, 0, 0, 0))
    out.paste(src.crop((0, 0, KEEP * N, N)), (0, 0))
    for k, c in enumerate(cells): out.paste(c, ((KEEP + k) * N, 0))
    out.save(SHEET); print('저장', SHEET, out.size)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--preview' in a:
        preview(a[a.index('--preview') + 1])
    elif '--apply' in a:
        apply()
    else:
        print('usage: fish_winter.py --preview DIR | --apply')
