#!/usr/bin/env python3
# 요리 40종 그림 (32×32 픽셀, 코드로 그림) → public/art/dishes.png (1280×32, 칸 i = x 32*i, DISH_LIST 순서)
#   python3 tools/iso/dish_icons.py                 시트만 다시 만들기
#   python3 tools/iso/dish_icons.py --preview DIR   + 4배 확대 시안(dishes_x4.png, dishes_x4_label.png)을 DIR에 저장
# 도구 상자: 마스크(ell/poly/rect/line) → fill/shade(밝기 3~5톤, 빛은 왼쪽 위) → 외곽선 한 번(OL) → 김·반짝이(fx)는 외곽선 뒤에
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'public', 'art', 'dishes.png')
S = 32
OL = (0x1a, 0x10, 0x24)

def H(s):
    s = s.lstrip('#'); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
WARM, COOL, DEEP = (255, 244, 206), (110, 70, 140), (50, 24, 80)
def R(c, n=5):
    """색 하나 → 밝음→어둠 5톤 [하이라이트, 밝음, 기본, 그림자, 어둠] (밝은 쪽은 따뜻하게, 그늘은 보라 쪽으로)"""
    if isinstance(c, str): c = H(c)
    return [mix(c, WARM, .5), mix(c, WARM, .22), c, mix(c, COOL, .25), mix(c, DEEP, .5)]

# ---------- 마스크 (좌표 집합) ----------
def ell(cx, cy, rx, ry):
    return {(x, y) for y in range(S) for x in range(S) if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0}
def circ(cx, cy, r): return ell(cx, cy, r, r)
def rect(x0, y0, x1, y1): return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if 0 <= x < S and 0 <= y < S}
def poly(pts):
    m = set(); n = len(pts)
    for y in range(S):
        for x in range(S):
            ins = False; j = n - 1
            for i in range(n):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: ins = not ins
                j = i
            if ins: m.add((x, y))
    return m
def line(x0, y0, x1, y1, w=1):
    m = set(); dx, dy = x1 - x0, y1 - y0; n = max(abs(dx), abs(dy), 1)
    for i in range(n + 1):
        x = round(x0 + dx * i / n); y = round(y0 + dy * i / n)
        for a in range(w):
            for b in range(w): m.add((x + a, y + b))
    return {p for p in m if 0 <= p[0] < S and 0 <= p[1] < S}
def below(m, y): return {p for p in m if p[1] >= y}
def above(m, y): return {p for p in m if p[1] <= y}
def left(m, x): return {p for p in m if p[0] <= x}
def right(m, x): return {p for p in m if p[0] >= x}
def shift(m, dx, dy): return {(x + dx, y + dy) for x, y in m}
def edge(m): return {(x, y) for x, y in m if any((x + a, y + b) not in m for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
def ring(m): return {(x + a, y + b) for x, y in m for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))} - m
def mirror(m, cx2): return {(cx2 - x, y) for x, y in m}   # x -> cx2-x

class Cv:
    def __init__(s): s.p = {}; s.fx = {}
    def px(s, x, y, c):
        if 0 <= x < S and 0 <= y < S and c is not None: s.p[(x, y)] = c
    def fxp(s, x, y, c):
        if 0 <= x < S and 0 <= y < S and c is not None: s.fx[(x, y)] = c
    def fill(s, m, c):
        for x, y in m: s.px(x, y, c)
    def pts(s, pl, c):
        for x, y in pl: s.px(x, y, c)
    def shade(s, m, ramp, lx=.5, ly=.8, cuts=None, bias=0.0):
        """둥근 빛: 왼쪽 위가 밝고 오른쪽 아래가 어두움. ramp 길이 2~5"""
        if not m: return
        xs = [p[0] for p in m]; ys = [p[1] for p in m]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cx, cy, hw, hh = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0 + 1) / 2, (y1 - y0 + 1) / 2
        n = len(ramp)
        if cuts is None: cuts = {2: [.1], 3: [-.3, .35], 4: [-.5, 0, .5], 5: [-.62, -.2, .3, .68]}[n]
        nr = math.hypot(lx, ly)
        for x, y in m:
            v = (lx * (x - cx) / hw + ly * (y - cy) / hh) / nr + bias
            s.px(x, y, ramp[sum(1 for c in cuts if v > c)])
    def vshade(s, m, ramp, cuts=None):
        """세로 줄무늬 빛(원통): 왼쪽 밝음"""
        xs = [p[0] for p in m]; x0, x1 = min(xs), max(xs); w = max(1, x1 - x0 + 1); n = len(ramp)
        if cuts is None: cuts = {2: [.55], 3: [.3, .7], 4: [.22, .55, .82]}[n]
        for x, y in m: s.px(x, y, ramp[sum(1 for c in cuts if (x - x0 + .5) / w > c)])
    def hshade(s, m, ramp, cuts=None):
        """가로 줄무늬 빛: 위가 밝음"""
        ys = [p[1] for p in m]; y0, y1 = min(ys), max(ys); h = max(1, y1 - y0 + 1); n = len(ramp)
        if cuts is None: cuts = {2: [.55], 3: [.3, .7], 4: [.22, .55, .82]}[n]
        for x, y in m: s.px(x, y, ramp[sum(1 for c in cuts if (y - y0 + .5) / h > c)])
    def art(s, x0, y0, rows, pal):
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in pal and pal[ch] is not None: s.px(x0 + i, y0 + j, pal[ch])
    def render(s):
        im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); P = im.load()
        for (x, y), c in s.p.items(): P[x, y] = c + (255,)
        for (x, y) in list(s.p):
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + a, y + b)
                if q not in s.p and 0 <= q[0] < S and 0 <= q[1] < S: P[q] = OL + (255,)
        for (x, y), c in s.fx.items(): P[x, y] = c + (255,)
        return im

# ---------- 공용 색 ----------
WHT = R('#f2ecf8')          # 하얀 도자기
LAV = R('#b9a6dc')
STEAM = (H('#f4eefc'), H('#cbbfe6'))
GOLD = R('#f2c13a'); GOLDD = H('#a8741a')
GREEN = R('#5fae4a'); LEAF = R('#7fc45a'); DGREEN = R('#2f6a3a')
RED = R('#d8403a'); ORANGE = R('#ee8a2a'); YEL = R('#f7d65a')
BROWN = R('#a8693a'); WOOD = R('#b98350'); PURP = R('#8a58c0'); PINK = R('#f08ab4'); BLUE = R('#5a8ae0')
WHITE = H('#fffaf0'); BLACK = H('#2a1c38')

# ---------- 공용 부품 ----------
def steam(cv, x, y0, y1, amp=1.5, ph=0.0, per=7.0):
    """김: 두 칸 굵기의 부드러운 S자(꼭대기는 한 칸·옅게)"""
    for y in range(y0, y1 + 1):
        xx = x + round(math.sin((y - y0) / per * 2 * math.pi + ph) * amp)
        if y == y0: cv.fxp(xx, y, STEAM[1]); continue
        cv.fxp(xx, y, STEAM[0]); cv.fxp(xx + 1, y, STEAM[1])
def sparkle(cv, x, y, big=False, c=H('#fff6c0'), c2=H('#ffd860')):
    cv.fxp(x, y, WHITE)
    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)): cv.fxp(x + a, y + b, c)
    if big:
        for a, b in ((2, 0), (-2, 0), (0, 2), (0, -2)): cv.fxp(x + a, y + b, c2)
def dot_sp(cv, x, y, c=H('#fff6c0')): cv.fxp(x, y, c)
STAR5 = lambda cx, cy, ro, ri, rot=-90: poly([(cx + (ro if i % 2 == 0 else ri) * math.cos(math.radians(rot + i * 36)),
                                               cy + (ro if i % 2 == 0 else ri) * math.sin(math.radians(rot + i * 36))) for i in range(10)])

def bowl(cv, cx, ty, rx, ry, depth, body, rim=None, food=None, foot=True, band=None, bandy=None):
    """그릇(옆에서 약간 위로 본 모양). 반환: (속 마스크, 몸통 마스크)"""
    rim = rim or body
    bm = below(ell(cx, ty, rx, depth), ty)
    cv.shade(bm, body[1:] if len(body) == 5 else body, lx=.75, ly=.45)
    if foot:
        f = rect(int(cx - rx * .45), int(ty + depth - 2), int(cx + rx * .45), int(ty + depth + 1))
        cv.fill(f - bm, body[3]); cv.fill(rect(int(cx - rx * .45), int(ty + depth + 1), int(cx + rx * .45), int(ty + depth + 1)), body[4])
    if band:
        cv.fill({p for p in bm if bandy[0] <= p[1] <= bandy[1]}, band[2])
        cv.fill({p for p in bm if p[1] == bandy[0]}, band[1])
        cv.fill({p for p in bm if p[1] == bandy[1] and p[0] > cx}, band[3])
    rm = ell(cx, ty, rx, ry); cv.fill(rm, rim[1])
    cv.fill({p for p in rm if p[1] >= ty + ry - 1 and p[0] >= cx}, rim[2])
    cv.fill({p for p in rm if p[1] == ty - int(ry) and p[0] < cx}, rim[0])
    im = ell(cx, ty + .6, rx - 1.6, ry - 1.4)
    cv.fill(im, (food or R('#d8a040'))[2])
    return im, bm

def plate(cv, cx, cy, rx, ry, ramp=None, inner=None, thick=1):
    ramp = ramp or WHT
    for k in range(thick, 0, -1): cv.fill(ell(cx, cy + k, rx, ry), ramp[3])
    cv.fill(ell(cx, cy, rx, ry), ramp[1])
    cv.fill({p for p in ell(cx, cy, rx, ry) if p[1] >= cy + ry - 1.2 and p[0] > cx - rx * .3}, ramp[2])
    im = ell(cx, cy + .3, rx - 2.2, ry - 1.5); cv.fill(im, (inner or ramp)[2] if inner else ramp[0])
    cv.shade(im, [(inner or ramp)[1], (inner or ramp)[2], (inner or ramp)[3]] if inner else [ramp[0], ramp[1], ramp[2]], bias=.1)
    return im

def fish(cv, cx, cy, L, Hh, base, belly=None, fin=None, d=1, tail=0.5, eye=True, dorsal=True, bars=None, spots=None, scales=False, mouth=False, teeth=False, tailw=1.0, rim=True):
    """옆에서 본 물고기. 머리가 d=1이면 오른쪽. 반환: 몸통 마스크"""
    def hh(t):
        if t < .4: return Hh / 2 * (.2 + .8 * math.sin(math.pi / 2 * t / .4) ** 1.1)
        return Hh / 2 * max(0.0, 1 - ((t - .4) / .6) ** 2) ** .5
    x_tail = cx - d * L / 2 * .72; x_head = cx + d * L / 2 * .62 + d * 1
    body = set()
    n = int(abs(x_head - x_tail)) + 1
    for i in range(n + 1):
        t = i / n; x = round(x_tail + d * i * (abs(x_head - x_tail)) / n); h = hh(t)
        for y in range(S):
            if abs(y - cy) <= h + .01: body.add((x, y))
    tl = L * .3
    tx = x_tail - d * tl; th = Hh * .56 * tailw
    h0 = hh(0)
    tm = poly([(x_tail + d * .5, cy - h0), (tx, cy - th), (tx + d * tl * .4, cy), (tx, cy + th), (x_tail + d * .5, cy + h0)])
    tm -= body
    xm = round(cx + d * L * .02); hm = hh(.45)
    fm = set()
    if dorsal: fm |= poly([(xm - d * L * .22, cy - hm + 1), (xm - d * L * .14, cy - hm - Hh * .38), (xm + d * L * .1, cy - hm + 1)]) - body
    fm |= poly([(xm - d * 1, cy + hm - 1), (xm - d * 3, cy + hm + Hh * .26), (xm - d * 6, cy + hm - 1)]) - body
    fc = fin or base
    if rim:
        allm = body | tm | fm
        cv.fill(ring(allm), mix(base[4], OL, .45))
    cv.fill(tm, fc[2]); cv.fill({p for p in tm if p[1] > cy}, fc[3]); cv.fill({p for p in tm if p[1] < cy - th * .5}, fc[1])
    cv.fill(fm, fc[2]); cv.fill({p for p in fm if p[1] < cy}, fc[1])
    cv.shade(body, [base[1], base[2], base[3]], lx=.35, ly=.9, cuts=[-.2, .45])
    if belly:
        lo = {p for p in body if p[1] > cy + Hh * .12}
        cv.fill(lo, belly[1]); cv.fill({p for p in lo if p[1] == max(q[1] for q in body if q[0] == p[0])}, belly[2])
    if scales:
        for (x, y) in body:
            if (x + y * 2) % 4 == 0 and (x - x_tail) * d > 3 and (x - x_head) * d < -5 and y > cy - Hh * .3 and y < cy + Hh * .25: cv.px(x, y, base[3])
    if bars:
        for (x, y) in body:
            if ((x - x_tail) * d) % bars[1] == 0 and (x - x_tail) * d > 3 and (x - x_head) * d < -5: cv.px(x, y, bars[0])
    if spots:
        for (x, y) in body:
            if (x * 7 + y * 13) % 9 == 0 and (x - x_tail) * d > 2 and (x - x_head) * d < -5 and cy - Hh * .45 < y < cy + Hh * .1: cv.px(x, y, spots)
    gx = round(x_head - d * L * .24)
    for y in range(int(cy - hh(.68) + 2), int(cy + hh(.68) - 1)):
        if (gx, y) in body: cv.px(gx, y, base[4])
    # 가슴지느러미
    px0 = round(x_head - d * L * .32); py0 = round(cy + Hh * .08)
    cv.pts([(px0, py0), (px0 - d, py0 + 1), (px0 - 2 * d, py0 + 1)], fc[3])
    if eye:
        ex = round(x_head - d * L * .15); ey = round(cy - Hh * .12)
        if L >= 15:
            cv.px(ex, ey, WHITE); cv.px(ex + d, ey, BLACK); cv.px(ex, ey - 1, WHITE) if Hh > 7 else None
        else: cv.px(ex, ey, BLACK)
    if teeth:
        mx = round(x_head - d * 1); my = round(cy + Hh * .14)
        cv.px(mx, my, WHITE); cv.px(mx - 2 * d, my, WHITE)
    return body

REG = {}
def dish(i):
    def deco(f): REG[i] = f; return f
    return deco

# ======================= 요리 그림 =======================
def shrink(m, n=1):
    for _ in range(n): m = m - edge(m)
    return m
def seed(c, x, y, f=0):
    """호박씨 4×2"""
    L, G, g = H('#d9ec9a'), H('#82b84e'), H('#3f7a3a')
    c.pts([(x + 1, y), (x + 2, y)], L); c.pts([(x, y + 1), (x + 1, y + 1), (x + 2, y + 1)], G); c.px(x + 3, y + 1, g); c.px(x, y, g) if f else None
def leaf(c, x, y, ramp=LEAF):
    c.pts([(x, y), (x + 1, y), (x + 1, y - 1), (x + 2, y - 1)], ramp[2]); c.pts([(x + 1, y), (x + 2, y)], ramp[1]); c.px(x, y + 1, ramp[3])
def ghost(c, x, y, eyes=True):
    """작은 유령 7×8"""
    P = {'W': H('#f4f2ff'), 'w': H('#c9c6ec'), 'k': BLACK}
    c.art(x, y, ['..WWW..', '.WWWWW.', 'WWWWWWw', 'WkWWkWw', 'WkWWkWw', 'WWWWWWw', 'WWWWWWw', 'WW.WW.w'], P)

@dish(0)
def d0(c):
    food = R('#e8dca0')
    im, bm = bowl(c, 15.5, 13, 13, 5, 14, WHT, WHT, food, band=ORANGE, bandy=(19, 22))
    c.shade(im, [food[1], food[2], food[3]], bias=-.1)
    for (x, y) in [(10, 14), (11, 13), (13, 12), (15, 12), (17, 13), (18, 14), (17, 15), (15, 15), (14, 14)]: c.px(x, y, WHITE)
    c.pts([(12, 15), (11, 15), (10, 15)], H('#fff3c8'))
    for (x, y, f) in [(8, 14, 0), (20, 12, 1), (21, 15, 0), (13, 16, 1), (16, 10 + 3, 0)]: seed(c, x, y, f)
    leaf(c, 18, 17); leaf(c, 11, 11, GREEN)
    # 주황 띠 위의 씨앗 무늬
    for x in range(8, 24, 4): c.pts([(x, 20), (x + 1, 20)], H('#fff0c0')); c.px(x + 2, 21, H('#fff0c0'))
    steam(c, 10, 2, 8, ph=0); steam(c, 16, 1, 8, ph=2); steam(c, 22, 2, 8, ph=4)

def cookie(c, cx, cy, rx, ry, th, ramp, chips=(), bits=(), cracks=()):
    c.fill(ell(cx, cy + th, rx, ry), ramp[3]); c.fill(below(ell(cx, cy + th, rx, ry), cy + th), ramp[3])
    c.fill({p for p in ell(cx, cy + th, rx, ry) if p[1] > cy + ry}, ramp[4])
    top = ell(cx, cy, rx, ry); c.shade(top, [ramp[1], ramp[2], ramp[3]], bias=-.05)
    c.fill(edge(top) & {p for p in top if p[0] < cx - rx * .3 or p[1] < cy - ry * .6}, ramp[1])
    for x, y in cracks: c.px(x, y, ramp[3])
    for x, y in bits: c.pts([(x, y), (x + 1, y)], H('#f0d09a')); c.px(x, y + 1, H('#c89a5a'))
    for x, y in chips: c.pts([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], H('#4a2a1c')); c.px(x, y, H('#7a4a30'))
def acorn(c, cx, cy):
    nut = ell(cx, cy + 2.5, 3.9, 5.2); c.fill(ring(nut), H('#5a3a22')); c.shade(nut, [H('#f0c078'), H('#d49a52'), H('#a8683a')], lx=.7, ly=.4)
    c.pts([(cx - 2, cy + 2), (cx - 2, cy + 3), (cx - 2, cy + 4)], H('#fbe4b0')); c.px(cx, cy + 7, H('#5a3a22'))
    cap = ell(cx, cy - 1, 5, 2.8); c.fill(ring(cap), H('#3a2214')); c.shade(cap, [H('#a06a3e'), H('#7a4a2a'), H('#5a3220')], lx=.6, ly=.6)
    for (x, y) in [(cx - 3, cy - 1), (cx - 1, cy - 2), (cx + 1, cy - 1), (cx + 3, cy - 2), (cx - 2, cy), (cx + 2, cy), (cx, cy - 1)]: c.px(int(x), int(y), H('#3e2414'))
    c.pts([(cx, cy - 4), (cx, cy - 5), (cx + 1, cy - 5)], H('#5a3a22'))

@dish(1)
def d1(c):
    dough = R('#dca052')
    cookie(c, 13.5, 21, 12.5, 6, 3, dough, chips=[(6, 21), (17, 24), (11, 25), (22, 20), (4, 24)], bits=[(9, 22), (20, 25), (14, 21)], cracks=[(8, 19), (9, 19), (19, 22), (13, 23)])
    cookie(c, 12.5, 13, 9, 4.6, 3, dough, chips=[(9, 11), (15, 14), (6, 14), (17, 11)], bits=[(12, 12), (16, 15), (7, 11)], cracks=[(11, 15), (12, 15), (14, 10)])
    acorn(c, 24, 17)
    sparkle(c, 25, 5, True); sparkle(c, 4, 5)

@dish(2)
def d2(c):
    plate(c, 15.5, 21, 14.5, 8, WHT, inner=R('#eadff5'))
    gold = R('#e8a838'); fin = R('#cf8a2c')
    for (x, y, d) in [(12, 18, 1), (18, 24, -1)]:
        b = fish(c, x, y, 19, 8, gold, belly=R('#f6d27a'), fin=fin, d=d, dorsal=True)
        for (px_, py_) in b:
            if (px_ * 5 + py_ * 3) % 7 == 0 and py_ < y + 1: c.px(px_, py_, H('#fbe29a'))
    # 레몬 조각과 파슬리
    lem = below(ell(26, 17, 3.8, 3.8), 17) | ell(26, 17, 3.8, 1.2)
    c.fill(ring(lem), H('#9a7a20')); c.fill(lem, H('#f6dc4a')); c.fill(shrink(lem, 1), H('#fff2a8')); c.pts([(26, 18), (26, 19), (24, 19), (28, 19)], H('#f6dc4a'))
    leaf(c, 4, 23, GREEN); leaf(c, 5, 26, LEAF); leaf(c, 7, 27)
    ghost(c, 22, 3)
    sparkle(c, 8, 7)

@dish(3)
def d3(c):
    # 대각선 꼬치 두 줄
    def skewer(x0, y0, x1, y1, kinds):
        n = len(kinds)
        c.fill(line(x0 - 1, y0 + 1, x1 + 2, y1 - 2, 1), WOOD[3])
        c.fill(line(x0, y0, x1, y1, 1), WOOD[1])
        for i, k in enumerate(kinds):
            t = .18 + .64 * i / (n - 1); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            if k == 'm':      # 갈색 버섯 갓
                m = ell(x, y, 4.4, 3.8); c.shade(m, R('#a8603a')[1:], lx=.6, ly=.6)
                c.pts([(round(x) - 2, round(y) - 2), (round(x) - 1, round(y) - 2)], H('#e0a070'))
                for (a, b) in [(1, 1), (-2, 1), (2, -1)]: c.px(round(x + a), round(y + b), H('#4a2a1c'))
            elif k == 'w':    # 흰 버섯 단면
                m = ell(x, y, 4.2, 3.6); c.shade(m, R('#f1e4cf')[1:4], lx=.6, ly=.6)
                c.fill({p for p in m if p[1] > y + 1}, H('#c9a88a')); c.px(round(x) - 2, round(y) - 1, WHITE)
                c.pts([(round(x) - 1, round(y)), (round(x) + 1, round(y) + 1)], H('#8a6a4a'))
            elif k == 'g':    # 파
                m = ell(x, y, 3.3, 3.3); c.shade(m, R('#6cc04a')[1:4], lx=.6, ly=.6); c.px(round(x), round(y), H('#d8f0a0'))
            else:             # 붉은 피망
                m = ell(x, y, 3.6, 3.4); c.shade(m, R('#e04a3a')[1:4], lx=.6, ly=.6); c.px(round(x) - 1, round(y) - 1, H('#ffb09a'))
        c.fill(line(x1 - 1, y1 + 1, x1 + 2, y1 - 2, 1), WOOD[2])
    skewer(2, 22, 24, 3, ['m', 'g', 'w', 'r', 'm'])
    skewer(8, 29, 30, 10, ['w', 'm', 'g', 'm', 'r'])
    sparkle(c, 4, 7, True); steam(c, 26, 1, 4, amp=.5)

@dish(4)
def d4(c):
    plate(c, 15.5, 25, 14.5, 5, WHT, inner=R('#eadff5'))
    bread = rect(6, 9, 25, 23) | ell(10.5, 10, 5.2, 3.8) | ell(20.5, 10, 5.2, 3.8)
    bread -= {(x, y) for (x, y) in bread if y > 22 and (x < 7 or x > 24)}
    c.fill(bread, H('#a8602c')); c.fill(bread & below(bread, 21), R('#a8602c')[3])
    c.fill({p for p in bread if p[1] < 12 and (p in edge(bread))}, H('#c88040'))
    crumb = shrink(bread, 2); c.shade(crumb, [H('#fbe3a0'), H('#f1c97a'), H('#dca85a')], bias=.1)
    jam = (ell(15.5, 16, 7.8, 5.6) | ell(11, 13.5, 3.6, 2.6) | ell(20.5, 17.5, 3.6, 3)) & crumb
    c.shade(jam, [H('#e8405a'), H('#c42848'), H('#8e1a38')], lx=.5, ly=.7)
    c.fill(edge(jam) & {p for p in jam if p[0] < 16}, H('#f06a7a'))
    c.pts([(9, 12), (10, 11), (11, 11)], H('#ffa0aa'))
    # 꿀 한 줄
    c.pts([(9, 17), (10, 18), (11, 17), (12, 18), (13, 17), (14, 18), (15, 17), (16, 18), (17, 17), (18, 18), (19, 17), (20, 18)], H('#f7c438'))
    c.pts([(10, 17), (12, 17), (14, 17), (16, 17), (18, 17)], H('#ffe488'))
    # 산딸기 3알
    for (x, y) in [(14, 12), (19, 14), (10, 19)]:
        b = ell(x, y, 3.1, 2.9); c.shade(b, [H('#ff7a8a'), H('#f04458'), H('#c42848')], lx=.5, ly=.6)
        c.fill(edge(b) & {p for p in b if p[0] > x or p[1] > y}, H('#9a1c3a'))
        c.pts([(x - 1, y - 1), (x, y - 1), (x - 1, y)], H('#ffc0c8')); c.px(x + 1, y + 1, H('#8a1830')); c.px(x - 1, y + 1, H('#b02240')); c.px(x + 1, y - 1, H('#b02240'))
    leaf(c, 16, 9, GREEN); leaf(c, 12, 22, GREEN)
    sparkle(c, 27, 6)

@dish(5)
def d5(c):
    # 종이컵
    cup = poly([(8, 19), (23, 19), (21, 28), (10, 28)])
    c.fill(cup, H('#e6c690'))
    for x in range(8, 24):
        if (x - 8) % 3 == 0: c.fill({p for p in cup if p[0] == x}, H('#c89a5a'))
        elif (x - 8) % 3 == 1: c.fill({p for p in cup if p[0] == x}, H('#f4dcae'))
    c.fill({p for p in cup if p[1] == 28}, H('#9a6a3a'))
    dome = above(ell(15.5, 19.5, 12.8, 8), 20); c.shade(dome, R('#c97b36')[1:], lx=.6, ly=.7)
    c.fill({p for p in dome if p[1] == 19 and (p[0] < 5 or p[0] > 26)}, R('#c97b36')[3])
    for (x, y) in [(7, 17), (11, 15), (20, 16), (24, 18), (14, 18), (18, 13)]: c.pts([(x, y), (x + 1, y)], H('#f0902a'))
    for (x, y) in [(9, 18), (22, 14), (16, 16)]: c.px(x, y, H('#5a2a2a'))
    # 크림치즈 프로스팅
    for (cx, cy, rx, ry) in [(15.5, 12, 8.5, 3.2), (15.5, 9, 6.2, 2.8), (15.5, 6.3, 3.8, 2.4)]:
        m = ell(cx, cy, rx, ry); c.shade(m, [H('#ffffff'), H('#fdf3e2'), H('#e8d2c0')], lx=.4, ly=.8)
    c.fill({p for p in ell(15.5, 12, 8.5, 3.2) if p[1] >= 14 and p[0] > 14}, H('#d9c2b4'))
    # 당근 장식
    carrot = poly([(15, 2), (18, 2), (17, 8), (16.5, 9)]) ; carrot = poly([(14.5, 4.5), (18.5, 4.5), (16.5, 10)])
    c.fill(carrot, ORANGE[2]); c.px(15, 5, ORANGE[1]); c.px(16, 6, ORANGE[3]); c.px(17, 8, ORANGE[3])
    c.pts([(16, 3), (17, 3), (16, 2), (17, 1), (15, 2)], GREEN[2]); c.px(16, 1, GREEN[1])

@dish(6)
def d6(c):
    # 받침 접시
    c.fill(ell(15.5, 26, 14.5, 4), WHT[3]); sa = ell(15.5, 25, 14.5, 4); c.fill(sa, WHT[1]); c.fill({p for p in sa if p[1] >= 27}, WHT[2])
    c.fill(ell(14, 25, 9, 2), WHT[2])
    # 손잡이
    hd = ell(24, 19, 4, 4.2) - ell(24, 19, 2, 2.4); c.fill(hd, WHT[2]); c.fill({p for p in hd if p[0] < 24 and p[1] < 19}, WHT[1]); c.fill({p for p in hd if p[0] > 24 and p[1] > 19}, WHT[3])
    body = below(ell(14, 14, 11, 12), 14) - below(ell(14, 14, 11, 12), 28)
    c.vshade(body, [WHT[1], WHT[2], WHT[3], WHT[3]], cuts=[.2, .6, .85])
    c.fill({p for p in body if 17 <= p[1] <= 18}, H('#7fc45a')); c.fill({p for p in body if p[1] == 17 and p[0] < 12}, H('#b4e08a')); c.fill({p for p in body if p[1] == 18 and p[0] > 17}, H('#4f9a3c'))
    rm = ell(14, 14, 11, 3.6); c.fill(rm, WHT[0]); c.fill({p for p in rm if p[1] >= 16 and p[0] > 14}, WHT[2])
    tea = ell(14, 14.4, 9.3, 2.6); c.shade(tea, [H('#c0e07a'), H('#9ccf5a'), H('#78b040')], bias=.1)
    # 세잎클로버
    for (x, y) in [(12, 13), (15.5, 13), (13.8, 15)]: 
        l = ell(x, y, 1.9, 1.5); c.shade(l, GREEN[1:4], lx=.5, ly=.5)
    c.pts([(15, 16), (16, 17)], DGREEN[2]); c.px(14, 14, H('#d8f0a0'))
    # 받침의 작은 클로버 + 찻잎
    for (x, y) in [(5, 25), (7, 25), (6, 27)]: c.pts([(x, y), (x + 1, y), (x, y + 1)], LEAF[2])
    c.px(6, 26, DGREEN[2])
    steam(c, 10, 2, 9, ph=0); steam(c, 15, 1, 9, ph=2); steam(c, 20, 3, 9, ph=4)

@dish(7)
def d7(c):
    glass = poly([(7, 8), (24, 8), (22, 29), (9, 29)])
    inner = poly([(8, 11), (23, 11), (21, 27), (10, 27)])
    c.fill(glass, H('#cfe0f6')); c.fill({p for p in glass if p[0] > 18}, H('#9db6dc'))
    c.fill(inner, RED[2])
    c.vshade(inner, [H('#ee5a4a'), H('#d4302e'), H('#a21e2e'), H('#7a1428')], cuts=[.15, .5, .85])
    c.fill({p for p in inner if p[1] < 13}, H('#f06a5a'))
    c.pts([(9, 14), (9, 15), (9, 16), (9, 17)], H('#ff9a88')); c.pts([(10, 21), (10, 22), (10, 23)], H('#ff9a88'))
    c.fill({p for p in glass if p[1] >= 28}, H('#e8f2ff'))
    rim = ell(15.5, 8, 8.5, 2.2); c.fill(rim, H('#eaf4ff')); c.fill(ell(15.5, 8.4, 7, 1.4), H('#c02a2e')); c.fill({p for p in rim if p[1] >= 9 and p[0] > 16}, H('#a9bde0'))
    # 얼음
    for (x, y) in [(12, 12), (18, 14)]: c.fill(rect(x, y, x + 3, y + 3), H('#f4a49a')); c.pts([(x, y), (x + 1, y), (x, y + 1)], H('#ffe0da'))
    # 빨대 (줄무늬)
    for i in range(14):
        x = 17 + i * .45; y = 13 - i * .85; col = WHITE if (i // 2) % 2 == 0 else H('#e8404a')
        c.px(round(x), round(y), col); c.px(round(x) + 1, round(y), col)
    # 토마토 조각
    tm = ell(7, 7, 4.3, 4.3); c.shade(tm, RED[1:4], lx=.5, ly=.6); c.fill(shrink(tm, 1), H('#f2604e'))
    for (x, y) in [(6, 5), (8, 6), (5, 8), (7, 9)]: c.px(x, y, H('#fbe49a'))
    c.fill(ell(7, 7, 1.2, 1.2), H('#ffb8a8')); c.px(6, 5, H('#fff0c8'))
    # 흘러내리는 피
    for (x, y0, y1) in [(21, 9, 14), (19, 9, 12), (23, 9, 11)]:
        for y in range(y0, y1): c.px(x, y, H('#b0202e'))
        c.px(x, y1, H('#d4302e'))
    sparkle(c, 27, 22)

@dish(8)
def d8(c):
    dish_ = ell(15.5, 20, 15, 9); c.fill(ell(15.5, 21.5, 15, 9), H('#5a3a52'))
    c.shade(dish_, R('#8a5a6a')[1:], lx=.6, ly=.7)
    inn = ell(15.5, 19.5, 12.8, 7.2); c.fill(inn, H('#3a2236'))
    sauce = ell(15.5, 19.8, 12, 6.6); c.shade(sauce, [H('#7a3c26'), H('#5a2c22'), H('#3e1c20')], lx=.5, ly=.6)
    # 호박 조각
    for (x, y) in [(6, 21), (25, 24)]:
        p = poly([(x - 3, y - 2), (x + 3, y - 2), (x + 4, y + 2), (x - 4, y + 2)]); c.fill(p, ORANGE[2]); c.fill({q for q in p if q[1] <= y - 1}, ORANGE[1]); c.fill({q for q in p if q[1] == y + 2}, H('#7a8a2a')); c.px(x - 2, y - 2, H('#ffd08a'))
        c.pts([(x - 1, y), (x + 1, y)], ORANGE[3])
    # 붕어
    b = fish(c, 15.5, 19, 22, 10, R('#e08a32'), belly=R('#f6c878'), fin=R('#c0642a'), d=1, scales=True)
    c.pts([(20, 14), (19, 14), (18, 14), (14, 14), (13, 14)], H('#ffd890'))
    # 버섯, 산딸기, 파
    m1 = ell(10, 25.5, 3.2, 2.2); c.shade(m1, R('#e0b080')[1:4], lx=.6, ly=.6); c.pts([(9, 24), (11, 26)], H('#8a5a3a'))
    for (x, y) in [(20, 26), (24, 19)]:
        r = ell(x, y, 2, 2); c.shade(r, R('#f04a62')[1:4]); c.px(x - 1, y - 1, H('#ffb0b8'))
    for (x, y) in [(5, 17), (26, 17), (14, 27), (18, 26)]: c.pts([(x, y), (x + 1, y)], H('#8fd05a')); c.px(x, y, H('#d0f0a0'))
    steam(c, 9, 2, 9, ph=1); steam(c, 16, 1, 9, ph=3); steam(c, 22, 2, 9, ph=5)

@dish(9)
def d9(c):
    wing = poly([(13, 13), (9, 5), (0, 8), (3, 12), (1, 19), (6, 16), (7, 24), (11, 19), (13, 26)])
    wr = mirror(wing, 31)
    c.shade(wing, [H('#8fd05a'), H('#5fae4a'), H('#3f8a3e')], lx=.3, ly=.9, bias=-.1)
    c.shade(wr, [H('#8fd05a'), H('#5fae4a'), H('#3f8a3e')], lx=-.3, ly=.9, bias=-.1)
    for (x1, y1) in [(1, 9), (2, 17), (7, 22), (6, 14)]:
        for (x, y) in line(13, 15, x1 + 1, y1):
            if (x, y) in wing: c.px(x, y, DGREEN[2]); c.px(31 - x, y, DGREEN[2])
    body = ell(15.5, 19, 6, 8.5); c.shade(body, R('#8a5a8a')[1:], lx=.6, ly=.6)
    c.shade(shrink(body, 1) & above(body, 25), [H('#f4e6c0'), H('#e2c892'), H('#c8a070')], lx=.5, ly=.7)
    for (x, y) in [(13, 22), (14, 23), (15, 24), (17, 21), (18, 22)]: c.px(x, y, H('#e0402e'))
    c.pts([(13, 21), (14, 21), (17, 23), (18, 23)], H('#c82a2a')); c.pts([(16, 21), (16, 22), (15, 20)], H('#7fc45a'))
    head = ell(15.5, 12.5, 4.6, 4); c.shade(head, R('#5a3a70')[1:], lx=.6, ly=.7)
    c.fill(poly([(11, 11), (11, 5), (14, 9)]), H('#4a2e60')); c.fill(poly([(20, 11), (20, 5), (17, 9)]), H('#4a2e60'))
    c.px(12, 8, H('#ff9ac0')); c.px(19, 8, H('#ff9ac0'))
    c.pts([(13, 12), (14, 12), (17, 12), (18, 12)], H('#ff4a5a')); c.px(14, 12, H('#ffd0c0')); c.px(17, 12, H('#ffd0c0'))
    c.px(14, 15, WHITE); c.px(17, 15, WHITE)
    sparkle(c, 27, 27)

def berry(c, x, y, r=2.2, ramp=None):
    """블루베리 한 알"""
    ramp = ramp or [H('#7a8af0'), H('#4a5ad0'), H('#2f3a9a')]
    b = ell(x, y, r, r); c.fill(ring(b), H('#1e2260')); c.shade(b, ramp, lx=.5, ly=.6)
    c.px(round(x) - 1, round(y) - 1, H('#c8d0ff')); c.px(round(x) + 1, round(y), H('#1e2260'))

@dish(10)
def d10(c):
    sh = R('#b284e8'); fill = R('#fff0cf')
    top = above(ell(15.5, 13, 12.8, 8), 13); bot = below(ell(15.5, 18, 12.8, 8), 18)
    fl = rect(5, 14, 26, 17) - {(5, 14), (26, 14), (5, 17), (26, 17)}
    c.fill(fl, fill[1]); c.fill({p for p in fl if p[1] >= 16}, fill[2]); c.fill({p for p in fl if p[1] == 14}, fill[0])
    c.shade(bot, [sh[1], sh[2], sh[3]], lx=.5, ly=.4, bias=.1); c.shade(top, [sh[0], sh[1], sh[2], sh[3]], lx=.6, ly=.8)
    for x in range(4, 28):
        if (x, 13) in top: c.px(x, 13, sh[0] if x % 2 == 0 else sh[2])
        if (x, 18) in bot: c.px(x, 18, sh[1] if x % 2 == 0 else sh[3])
    # 버섯 반점
    for (x, y) in [(8, 10), (23, 10), (20, 7), (6, 13)]:
        c.pts([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], H('#fff4fa')); c.px(x + 1, y + 1, H('#e8d4f4'))
    # 거미
    P = {'k': BLACK, 'g': H('#5a4a78'), 'r': H('#ff4a5a')}
    sp = ['k...k.k...k', '.k..kkk..k.', '..kkkkkkk..', 'kkkkkkkkkkk', '..kkrkrkk..', '.kk.kkk.kk.', 'k...k.k...k']
    c.art(10, 5, [r[1:10] for r in sp] if False else sp, P)
    # 딸기 조각 + 꿀
    sb = ell(25.5, 24.5, 3.6, 3.4); c.fill(ring(sb), H('#6a1a2a')); c.shade(sb, [H('#ff6a7a'), H('#e0304a'), H('#a8203a')], lx=.5, ly=.6)
    c.pts([(24, 23), (25, 24), (26, 23), (27, 25), (25, 26)], H('#ffd0c8')); c.pts([(25, 20), (26, 20), (27, 21)], GREEN[2])
    for (x, y) in [(5, 26), (6, 27)]: c.px(x, y, H('#f7c438'))
    c.pts([(7, 19), (7, 20), (7, 21)], H('#f7c438'))
    sparkle(c, 5, 4, True)

@dish(11)
def d11(c):
    c.fill(ell(15.5, 21, 15, 9.5), H('#6a4a30'))
    outer = ell(15.5, 19.5, 15, 9.5); c.shade(outer, [H('#f0c070'), H('#d99c48'), H('#a8683a')], lx=.5, ly=.7, bias=-.1)
    for (x, y) in edge(outer):
        if (x + y) % 3 == 0: c.px(x, y, H('#fbe0a0'))
        elif (x + y) % 3 == 1: c.px(x, y, H('#b87838'))
    inn = ell(15.5, 19, 12, 7.4); c.shade(inn, [H('#6a6ae0'), H('#4a4ac0'), H('#34328e')], lx=.5, ly=.7, bias=-.1)
    for (x, y) in inn:
        if ((x + y) % 6 in (0, 1) and y < 22 and x < 24) or ((x - y) % 6 in (0, 1) and y < 22 and x < 24):
            c.px(x, y, H('#f2c070') if (x + y) % 2 == 0 else H('#dc9c4a'))
    # 잘려나간 한 조각
    wedge = poly([(15.5, 19), (21, 30), (31, 25), (30, 17)]) & outer
    c.fill(wedge, H('#2e2a58'))
    cut = wedge - ring(inn) & ell(15.5, 20.5, 12.5, 8)
    c.fill(wedge & ell(15.5, 19.8, 12.5, 7.8), H('#3e3aa8')); c.fill({p for p in wedge & ell(15.5, 19.8, 12.5, 7.8) if p[1] > 23}, H('#2a2878'))
    c.fill({p for p in wedge if p[0] > 15 and p[1] > 26}, H('#8a5a2e'))
    for (x, y) in [(20, 22), (22, 24), (24, 22), (26, 21), (23, 20)]: c.px(x, y, H('#8a8aff'))
    # 생크림 + 블루베리
    cr = ell(22, 25, 3.2, 2); c.fill(ring(cr), H('#6a5a7a')); c.shade(cr, [H('#ffffff'), H('#f4ecfa'), H('#c8bcdc')])
    berry(c, 8, 18); berry(c, 12, 22); berry(c, 22, 24, 2)
    steam(c, 9, 2, 9, ph=0); steam(c, 16, 1, 9, ph=2); steam(c, 22, 3, 9, ph=4)

@dish(12)
def d12(c):
    plate(c, 15.5, 22, 14.5, 7.5, WHT, inner=R('#eadff5'))
    om = ell(15.5, 20.5, 11.5, 5.8) | ell(12, 22, 6, 4)
    c.fill(ring(om), H('#b8781e')); c.shade(om, [H('#ffe880'), H('#f8d444'), H('#e0aa28'), H('#b8801e')], lx=.4, ly=.8)
    for (x, y) in om:
        if y == 22 and 8 <= x <= 22 and x % 2 == 0: c.px(x, y, H('#c8901e'))
    for x in range(7, 24): c.px(x, 20 + (1 if 11 < x < 19 else 0), H('#d8a028'))
    c.pts([(10, 19), (11, 19), (20, 18), (21, 18), (13, 24), (14, 24)], H('#c88a24'))
    # 이끼(허브)
    for (x, y) in [(8, 20), (9, 21), (12, 19), (18, 22), (21, 21), (16, 24), (22, 19), (10, 23)]: c.pts([(x, y), (x + 1, y)], H('#4f9a3c')); c.px(x, y - 1, H('#9fd870'))
    # 송사리
    fish(c, 17, 14.5, 14, 5.5, R('#8fb0d8'), belly=R('#eef2fa'), fin=R('#6a8ac0'), d=1, dorsal=True)
    c.pts([(14, 14), (15, 14), (16, 14), (17, 14), (18, 14)], H('#4a6ab8'))
    ghost_ = None
    steam(c, 9, 3, 10, amp=1.0, ph=1)
    sparkle(c, 27, 8)

@dish(13)
def d13(c):
    # 꿀 웅덩이와 꼬치
    pud = ell(18, 27.8, 11, 2.8); c.fill(ring(pud), H('#a8741a')); c.shade(pud, [H('#ffe27a'), H('#f7c438'), H('#d99a22')])
    c.fill(line(9, 30, 22, 2, 1), WOOD[3]); c.fill(line(10, 30, 23, 2, 1), WOOD[1])
    chest = [(13, 24.5), (16.5, 18), (15.5, 11.5), (19, 5.5)]
    for i, (x, y) in enumerate(chest):
        m = ell(x, y, 4.8, 3.2); c.fill(ring(m), H('#3a2012')); c.shade(m, [H('#c4803e'), H('#8a4a26'), H('#5a2e1e')], lx=.5, ly=.7)
        c.fill(ell(x - 1.4, y - 1.2, 2.6, 1.2), H('#f0b860')); c.pts([(round(x) - 3, round(y) - 1), (round(x) - 2, round(y) - 2)], H('#fff0b0'))
        c.pts([(round(x) + 2, round(y) + 1), (round(x) + 3, round(y)), (round(x) + 1, round(y))], H('#f4dc8a'))   # 칼집
        c.pts([(round(x) + 3, round(y) + 3), (round(x) + 3, round(y) + 4)], H('#f7c438')) if i in (0, 1) else None
    for (x, y0, y1) in [(9, 24, 27), (21, 20, 24), (21, 13, 16)]:
        for y in range(y0, y1): c.px(x, y, H('#f7c438'))
        c.pts([(x, y1), (x, y1 + 1)], H('#e8a828')); c.px(x - 1, y0 + 1, H('#ffe27a'))
    # 낱개 밤
    m = ell(26, 22, 3.8, 3.2); c.fill(ring(m), H('#3a2012')); c.shade(m, [H('#c4803e'), H('#8a4a26'), H('#5a2e1e')]); c.pts([(25, 20), (26, 20)], H('#f0b860')); c.pts([(27, 23), (28, 22)], H('#f4dc8a'))
    sparkle(c, 5, 8, True); sparkle(c, 27, 6)

def ghost_mask(cx, yt, w, yb, wave=1):
    top = above(ell(cx, yt + w / 2, w / 2, w / 2), yt + w // 2)
    body = rect(int(cx - w / 2 + .5), yt + w // 2, int(cx + w / 2 - .5), yb)
    m = top | body
    # 아래쪽 물결
    xs = [p[0] for p in m]; x0 = min(xs)
    out = set()
    for (x, y) in m:
        ph = (x - x0) % 6
        cut = yb - (0 if ph in (1, 2, 3) else 2 + wave)
        if y <= cut: out.add((x, y))
    return out

@dish(14)
def d14(c):
    # 그레이엄 크래커
    cr = rect(3, 25, 28, 29); c.fill(ring(cr), H('#6a4a22')); c.shade(cr, [H('#e8c488'), H('#d8a860'), H('#b88040')], lx=.3, ly=.9)
    for x in range(5, 27, 4): c.px(x, 27, H('#9a6a30'))
    c.pts([(5, 26), (6, 26), (14, 26), (15, 26), (22, 26)], H('#f8e0b0'))
    g = ghost_mask(13.5, 2, 18, 27, 1) 
    arms = ell(5.5, 17, 2.4, 3.2) | ell(21.5, 18, 2.4, 3.2); g |= arms
    c.fill(ring(g), H('#6a5a9a')); c.shade(g, [H('#ffffff'), H('#f0ecff'), H('#d4ccf2'), H('#a89cd8')], lx=.5, ly=.8)
    # 마시멜로의 소용돌이 결
    for (x, y) in [(9, 8), (10, 7), (11, 6), (16, 5), (17, 5), (18, 6), (8, 20), (9, 21), (10, 22), (17, 21), (18, 22), (19, 23)]: c.px(x, y, H('#d4ccf2'))
    # 얼굴
    c.pts([(10, 12), (10, 13), (10, 14), (11, 12), (11, 13), (11, 14)], BLACK); c.pts([(16, 12), (16, 13), (16, 14), (17, 12), (17, 13), (17, 14)], BLACK)
    c.px(10, 12, WHITE); c.px(16, 12, WHITE)
    c.pts([(13, 16), (14, 16), (13, 17), (14, 17)], H('#5a2a48')); c.pts([(8, 16), (9, 16), (18, 16), (19, 16)], H('#ffb0c8'))
    # 작은 유령
    g2 = ghost_mask(25, 14, 8, 24, 0); c.fill(ring(g2), H('#6a5a9a')); c.shade(g2, [H('#ffffff'), H('#ece8ff'), H('#c4bce8')], lx=.5, ly=.8)
    c.pts([(23, 18), (23, 19), (26, 18), (26, 19)], BLACK); c.px(24, 21, H('#5a2a48')); c.px(25, 21, H('#5a2a48'))
    # 꿀
    for (x, y) in [(10, 3), (11, 3), (12, 4), (13, 3), (14, 4), (15, 3)]: c.px(x, y, H('#f7c438'))
    sparkle(c, 4, 6, True); sparkle(c, 28, 8)

@dish(15)
def d15(c):
    pot = R('#6a4030'); food = R('#8a7a3a')
    # 손잡이(양쪽 귀)
    for x0 in (1, 27):
        h = rect(x0, 15, x0 + 3, 18); c.fill(ring(h), OL); c.fill(h, pot[2]); c.fill({p for p in h if p[1] == 15}, pot[1])
    im, bm = bowl(c, 15.5, 14, 13, 5, 13, pot, R('#8a5a44'), food, band=R('#3a2418'), bandy=(20, 21))
    c.shade(im, [H('#9a8a40'), H('#7a6a34'), H('#5a4a2a')], bias=.2)
    c.fill({p for p in bm if p[1] == 20 and p[0] < 14}, H('#5a3a2a'))
    # 파, 깻잎, 생강, 추어 조각
    for (x, y) in [(9, 13), (13, 11), (18, 13), (21, 15), (11, 16), (16, 16)]:
        r = ell(x, y, 1.6, 1.3); c.fill(r, H('#6cc04a')); c.px(x, y, H('#d4f0a0')); c.px(x + 1, y, H('#3f8a3e'))
    for (x, y) in [(14, 14), (20, 12)]: c.pts([(x, y), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y)], H('#d8b878'))
    c.pts([(10, 14), (11, 14), (12, 15), (13, 15)], H('#4a3a28')); c.pts([(17, 11), (18, 11), (19, 12)], H('#4a3a28'))
    c.pts([(19, 16), (20, 16)], H('#e0402e')); c.px(12, 18, H('#b8a060')); c.px(15, 17, H('#b8a060')); c.px(7, 15, H('#b8a060'))
    steam(c, 9, 2, 8, ph=1); steam(c, 15, 1, 8, ph=3); steam(c, 21, 2, 8, ph=0)

@dish(16)
def d16(c):
    # 막대기
    c.fill(rect(14, 22, 16, 30), WOOD[2]); c.fill(rect(14, 22, 14, 30), WOOD[1]); c.fill(rect(16, 22, 16, 30), WOOD[3])
    ap = ell(12.5, 14, 7, 8.5) | ell(19, 14, 7, 8.5) | ell(15.5, 16, 9.5, 8)
    ap -= poly([(14, 4), (17, 4), (15.5, 7)])
    c.fill(ring(ap), H('#3a1456')); c.shade(ap, [H('#c06ae8'), H('#9a3ad0'), H('#6a22a8'), H('#431a7c')], lx=.55, ly=.75, cuts=[-.45, .1, .6])
    # 독약 초록 코팅과 줄줄
    cap = {p for p in ap if p[1] <= 9 + (1 if p[0] % 5 in (1, 2) else 0) + (3 if p[0] in (8, 9, 19, 20) else 0) + (5 if p[0] in (12, 13) else 0)}
    c.fill(cap, H('#5ee04a')); c.shade(cap, [H('#b8ff7a'), H('#5ee04a'), H('#2fa83a')], lx=.5, ly=.8)
    c.fill({p for p in cap if p[1] > 9 and p[0] in (12, 13)}, H('#3cc43c'))
    # 하이라이트와 해골
    c.pts([(8, 11), (8, 12), (9, 13), (8, 14)], H('#f0d0ff')); c.pts([(9, 10), (10, 10)], H('#f0d0ff'))
    sk = ['.WWW.', 'WWWWW', 'WkWkW', '.WWW.', '.W.W.']
    c.art(14, 16, sk, {'W': H('#f6f0ff'), 'k': H('#2a1048')})
    # 줄기와 잎
    c.pts([(15, 3), (15, 4), (16, 2), (16, 1)], H('#5a3a22')); leaf(c, 17, 3, GREEN)
    # 리본
    c.fill(poly([(10, 24), (15, 26), (10, 28)]), H('#5ee04a')); c.fill(poly([(21, 24), (16, 26), (21, 28)]), H('#2fa83a')); c.fill(rect(14, 25, 16, 27), H('#8aff6a'))
    # 독 거품
    for (x, y) in [(4, 8), (27, 6), (26, 13), (5, 17)]: c.fxp(x, y, H('#8aff6a')); c.fxp(x + 1, y, H('#4ad84a')); c.fxp(x, y + 1, H('#4ad84a'))
    sparkle(c, 27, 22)

@dish(17)
def d17(c):
    blue = R('#7aa6e0'); food = R('#f2b840')
    im, bm = bowl(c, 15.5, 14, 12.5, 5, 13, blue, R('#f6ecc0'), food, band=R('#f2d060'), bandy=(19, 19))
    c.shade(im, [H('#ffd860'), H('#f2b840'), H('#d89a30')], bias=.1)
    # 초승달 크림
    cres = ell(14, 14.2, 5.6, 3.4) - ell(16.4, 13.2, 4.6, 2.9); c.fill(cres, H('#fffdf4')); c.fill({p for p in cres if p[1] >= 16 or p[0] < 10}, H('#f0e4c8'))
    # 옥수수 낟알
    for (x, y) in [(8, 14), (10, 17), (18, 17), (21, 14), (20, 11), (12, 11), (23, 13)]: c.pts([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], H('#ffe040')); c.px(x, y, H('#fff6a0')); c.px(x + 1, y + 1, H('#c88a18'))
    for (x, y) in [(15, 11), (11, 15)]: c.px(x, y, H('#2fa83a')); c.px(x + 1, y, H('#6cc04a'))
    for (x, y) in [(8, 22), (12, 24), (19, 22), (23, 24)]: c.px(x, y, H('#f6ecc0')); c.px(x + 1, y, H('#f6ecc0')); c.px(x, y + 1, H('#f6ecc0'))
    c.pts([(15, 21), (16, 21), (14, 22), (14, 23), (15, 24), (16, 24)], H('#f6ecc0'))
    steam(c, 10, 2, 9, ph=0); steam(c, 16, 1, 9, ph=2); steam(c, 22, 2, 9, ph=4)
    sparkle(c, 27, 4, True)

@dish(18)
def d18(c):
    # 유리 접시
    gl = ell(15.5, 26.5, 14, 4); c.fill(ring(gl), H('#5a7aa0')); c.shade(gl, [H('#e8f6ff'), H('#c4e0f4'), H('#8ab4d8')], lx=.4, ly=.8)
    c.fill(ell(15.5, 26, 11.5, 2.4), H('#a8d0ec'))
    # 촉수
    for (x, ph) in [(6, 0), (9, 1), (12, 2), (15, 0), (18, 2), (21, 1), (24, 0)]:
        for y in range(18, 27):
            xx = x + round(math.sin(y / 1.6 + ph) * 1.3)
            c.px(xx, y, H('#f0e0ff')); c.px(xx + 1, y, H('#b890f0'))
    dome = above(ell(15.5, 18, 12, 11), 18)
    c.fill(ring(dome), H('#4a2a7a')); c.shade(dome, [H('#f0e0ff'), H('#d4b4ff'), H('#b088f0'), H('#8a62d0')], lx=.55, ly=.85)
    c.fill({p for p in dome if p[1] == 18}, H('#8a62d0'))
    for (x, y) in [(9, 14), (12, 11), (19, 12), (22, 15), (16, 15)]: c.pts([(x, y), (x + 1, y)], H('#8a62d0')); c.px(x, y - 1, H('#fff4ff'))
    c.pts([(8, 12), (9, 10), (11, 8), (14, 7)], H('#ffffff')); c.px(7, 14, H('#ffffff'))
    sb = ell(15.5, 5.5, 3.4, 3); c.fill(ring(sb), H('#6a1a2a')); c.shade(sb, [H('#ff6a7a'), H('#e0304a'), H('#a8203a')]); c.pts([(14, 4), (16, 5), (15, 7)], H('#ffd8c8'))
    c.pts([(14, 2), (15, 2), (16, 2), (15, 3)], GREEN[2])
    for (x, y0, y1) in [(12, 9, 12), (19, 10, 13)]:
        for y in range(y0, y1): c.px(x, y, H('#f7c438'))
        c.px(x, y1, H('#ffe27a'))
    for (x, y) in [(4, 15), (27, 12)]: c.fxp(x, y, H('#e8f6ff')); c.fxp(x, y + 1, H('#c4e0f4'))
    sparkle(c, 4, 6, True); sparkle(c, 27, 20)

@dish(19)
def d19(c):
    # 대나무 찜기
    bk = R('#d8b070')
    body = poly([(2, 20), (29, 20), (28, 29), (3, 29)])
    c.fill(ring(body), H('#4a3018')); c.vshade(body, [bk[0], bk[1], bk[2], bk[3]], cuts=[.12, .5, .85])
    for y in (23, 26): c.fill({p for p in body if p[1] == y}, H('#9a6a30'))
    for x in range(5, 27, 3): c.px(x, 21, H('#9a6a30')); c.px(x + 1, 24, H('#9a6a30')); c.px(x, 27, H('#9a6a30'))
    c.fill({p for p in body if p[1] == 29}, bk[4])
    rim = ell(15.5, 20, 14, 3.4); c.fill(ring(rim), H('#4a3018')); c.fill(rim, bk[1]); c.fill({p for p in rim if p[1] >= 22}, bk[2]); c.fill(ell(15.5, 20, 12, 2.2), H('#6a4a28'))
    # 가재
    rc = R('#e8402c'); dr = R('#c42a24')
    for sgn in (1, -1):
        def X(x): return x if sgn == 1 else 31 - x
        for (x, y) in line(14, 14, 9, 9, 2): c.px(X(x), y, dr[2])
        # 집게
        cl = ell(7, 6, 3.6, 3.1); 
        c.fill({(X(x), y) for x, y in ring(cl)}, H('#4a1018')); c.fill({(X(x), y) for x, y in cl}, rc[2])
        c.fill({(X(x), y) for x, y in cl if y < 6}, rc[1]); c.fill({(X(x), y) for x, y in cl if y > 7}, rc[3])
        c.pts([(X(5), 3), (X(4), 2)], dr[3]); c.pts([(X(8), 3), (X(9), 2)], rc[1])
        # 다리
        for (x0, y0, x1, y1) in [(13, 16, 8, 18), (13, 17, 9, 21), (14, 18, 11, 22)]:
            for (x, y) in line(x0, y0, x1, y1): c.px(X(x), y, dr[3])
        # 더듬이
        for (x, y) in line(14, 9, 11, 2): c.px(X(x), y, H('#a8281e'))
    car = ell(15.5, 12.5, 5, 4.5); c.fill(ring(car), H('#4a1018')); c.shade(car, [rc[1], rc[2], rc[3]], lx=.5, ly=.7)
    c.pts([(14, 8), (14, 9), (17, 8), (17, 9)], BLACK); c.px(14, 8, WHITE); c.px(17, 8, WHITE)
    for k, (cy, rx) in enumerate([(17.5, 4.2), (20.3, 4), (22.8, 3.6)]):
        sg = ell(15.5, cy, rx, 1.9); c.fill(ring(sg), H('#4a1018')); c.shade(sg, [rc[1], rc[2], rc[3]], lx=.3, ly=.9)
    fan = poly([(12.5, 23), (18.5, 23), (20, 27), (15.5, 26), (11, 27)]); c.fill(ring(fan), H('#4a1018')); c.fill(fan, rc[3]); c.pts([(15, 24), (16, 24), (14, 26), (17, 26)], dr[2])
    c.pts([(14, 11), (15, 11), (14, 12)], H('#ff9a80')); c.px(13, 10, H('#ffb8a0'))
    # 옥수수 토막과 고추
    cb = ell(5, 25, 3.2, 3.2); c.fill(ring(cb), H('#6a4a10')); c.fill(cb, H('#ffd848')); c.pts([(4, 24), (6, 24), (5, 26), (3, 26), (7, 26)], H('#f0a820')); c.px(4, 24, H('#fff6a0'))
    for (x, y, f) in [(23, 25, 1), (26, 23, 0)]:
        pp = line(x, y, x + 3, y + (3 if f else -3), 2); c.fill(ring(pp), H('#5a0a14')); c.fill(pp, H('#e0242a')); c.px(x, y, H('#ff8a7a'))
    steam(c, 14, 0, 4, amp=.6, ph=0)

def skull_small(c, x, y, col=H('#f6f0ff'), hole=H('#2a1048')):
    c.art(x, y, ['.WWW.', 'WWWWW', 'WkWkW', '.WWW.', '.W.W.'], {'W': col, 'k': hole})
def mush_cap(c, x, y, r=3, cap=None, spots=True):
    cap = cap or R('#e04a4a')
    m = above(ell(x, y, r, r * .8), y); c.fill(ring(m), H('#3a1020')); c.shade(m, [cap[1], cap[2], cap[3]], lx=.5, ly=.7)
    c.fill(rect(int(x - r * .45), y + 1, int(x + r * .45), y + 2), H('#f0e0c8'))
    if spots: c.px(round(x) - 1, y - 1, WHITE); c.px(round(x) + 1, y - 2, WHITE)

@dish(20)
def d20(c):
    navy = R('#4a4680'); food = R('#f6f0e0')
    im, bm = bowl(c, 15.5, 14, 13, 5, 13, navy, R('#6a66a0'), food)
    c.shade(im, [H('#fffaf0'), H('#f6f0e0'), H('#e0d6c0')], bias=.2)
    skull_small(c, 13, 20)
    # 물고기 뼈(메기)
    bone = H('#fffaf0'); bs = H('#bfae92')
    for (x, y) in line(9, 14, 19, 14): c.px(x, y, bs); c.px(x, y - 1, bone)
    for x in (11, 13, 15, 17): c.pts([(x, 12), (x, 13), (x, 15), (x, 16)], bone); c.px(x, 17, bs) if False else None
    c.pts([(x, 15) for x in (11, 13, 15, 17)], bs)
    sk = ell(8, 14, 2.6, 2.4); c.fill(ring(sk), bs); c.fill(sk, bone); c.px(7, 13, BLACK); c.px(9, 13, BLACK)
    for (x, y) in [(5, 12), (4, 11), (5, 16), (4, 17)]: c.px(x, y, bs)
    c.pts([(20, 12), (21, 11), (20, 16), (21, 17), (19, 14), (20, 14)], bone)
    # 사골 뼈
    for (x, y) in line(14, 10, 25, 3, 3): c.px(x, y, H('#fffaf0'))
    for (x, y) in line(14, 11, 25, 4, 1): c.px(x, y, H('#d4cab4'))
    for (cx_, cy_) in [(25, 3), (26, 5), (13, 9), (14, 11)]:
        k = circ(cx_, cy_, 1.8); c.fill(ring(k), H('#8a7a62')); c.fill(k, bone)
    c.pts([(25, 4), (26, 6), (13, 10), (14, 12)], H('#d4cab4'))
    # 대파·후추
    for (x, y) in [(16, 11), (20, 15), (12, 17), (9, 17), (22, 12)]: c.pts([(x, y), (x + 1, y)], H('#6cc04a')); c.px(x, y, H('#d4f0a0'))
    for (x, y) in [(18, 17), (14, 12), (21, 17)]: c.px(x, y, H('#3a3040'))
    steam(c, 9, 2, 8, ph=0); steam(c, 17, 1, 7, ph=2)

@dish(21)
def d21(c):
    pl = ell(15.5, 27.5, 14, 3.4); c.fill(ring(pl), H('#6a5a8a')); c.shade(pl, [H('#fbf4ff'), H('#e8dcf4'), H('#c0aedc')], lx=.4, ly=.8)
    pud = poly([(8, 25), (23, 25), (21, 14), (10, 14)]) | ell(15.5, 25, 7.5, 2.4)
    c.fill(ring(pud), H('#7a4a1e')); c.vshade(pud, [H('#fff0a8'), H('#f7d878'), H('#e8b850'), H('#c8943a')], cuts=[.2, .55, .85])
    c.fill({p for p in pud if p[1] >= 24}, H('#c8943a'))
    cap = above(ell(15.5, 15, 6.4, 2.6), 15) | {(x, y) for (x, y) in pud if y <= 17 and abs(x - 15.5) <= 5.8 + (y - 14) * .1}
    c.fill(cap, H('#a8581e')); c.shade(cap, [H('#d8883a'), H('#a8581e'), H('#7a3c18')], lx=.5, ly=.8)
    for (x, y0, y1) in [(10, 17, 21), (13, 17, 19), (17, 17, 22), (20, 17, 20)]:
        for y in range(y0, y1): c.px(x, y, H('#a8581e'))
        c.px(x, y1, H('#7a3c18'))
    # 솜사탕 구름
    blobs = [(9.5, 9, 4.2, 0), (15, 6, 5, 0), (21, 9, 4.4, 1), (13, 10, 4.2, 0), (18, 10.5, 3.8, 1), (15.5, 3.8, 3.2, 0)]
    for (x, y, r, b) in blobs:
        m = ell(x, y, r, r * .9); c.fill(ring(m), H('#8a4a8a'))
    for (x, y, r, b) in blobs:
        m = ell(x, y, r, r * .9)
        c.shade(m, [H('#fff0f8'), H('#ffc4e4'), H('#ff9ccc')] if not b else [H('#f0fbff'), H('#b8e4ff'), H('#8cc4f4')], lx=.5, ly=.7)
    for (x, y) in [(10, 8), (14, 5), (20, 8), (13, 9), (17, 10)]: c.pts([(x, y), (x + 1, y)], H('#ffffff'))
    # 넙치 쿠키
    f = ell(26.5, 23, 3.8, 3) | poly([(29, 23), (31, 21), (31, 25)]); f &= rect(0, 0, 31, 31)
    c.fill(ring(f), H('#5a3a1e')); c.shade(f, [H('#e8c488'), H('#d0a060'), H('#a8743a')], lx=.5, ly=.6)
    c.pts([(25, 21), (27, 21)], WHITE); c.px(25, 21, BLACK); c.px(27, 21, BLACK); c.px(26, 24, H('#8a5a2a'))
    sparkle(c, 4, 4, True); sparkle(c, 27, 9)

@dish(22)
def d22(c):
    pl = R('#4a5a8a')
    c.fill(ell(15.5, 22, 15, 8.5), pl[4]); o = ell(15.5, 21, 15, 8.5); c.shade(o, [pl[1], pl[2], pl[3]], lx=.5, ly=.7)
    inn = ell(15.5, 21, 12.5, 6.4); c.shade(inn, [H('#6a7aa8'), H('#566698'), H('#44547e')], bias=.2)
    tr = R('#c8924c')
    b = fish(c, 17, 20.5, 23, 11, tr, belly=R('#f0d498'), fin=R('#a8683a'), d=1)
    # 구이 자국(비스듬한 줄)
    for (x, y) in b:
        if 11 <= x <= 22 and (x - y) % 5 == 0 and 15 <= y <= 25: c.px(x, y, H('#5a3a28'))
    for (x, y) in b:
        if y <= 17 and 8 < x < 23 and (x + y) % 3 == 0: c.px(x, y, H('#7a90b0'))
    for (x, y) in b:
        if (x * 7 + y * 13) % 11 == 0 and 10 < x < 21 and 18 < y < 24: c.px(x, y, H('#3a2a2a'))
    # 라벤더와 레몬
    for (x, y) in line(24, 28, 20, 21): c.px(x, y, H('#5a8a4a'))
    for (x, y) in [(20, 22), (21, 23), (20, 24), (22, 25), (21, 26), (23, 23), (19, 25)]: c.pts([(x, y), (x + 1, y)], H('#b07ae8')); c.px(x, y, H('#d8b0ff'))
    lem = ell(6.5, 26, 3.2, 2.2); c.fill(ring(lem), H('#9a7a20')); c.fill(lem, H('#f6dc4a')); c.fill(ell(6.5, 26, 1.6, 1), H('#fff2a8'))
    cres = ell(26, 6, 3.6, 3.6) - ell(27.8, 5.2, 3.2, 3.2)
    for (x, y) in cres: c.fxp(x, y, H('#fff3b0'))
    sparkle(c, 5, 7, True); sparkle(c, 21, 4)

@dish(23)
def d23(c):
    tl = R('#2e6a72')
    c.fill(ell(15.5, 23, 15, 7.5), tl[4]); o = ell(15.5, 22, 15, 7.5); c.shade(o, [tl[1], tl[2], tl[3]], lx=.5, ly=.7)
    c.fill(edge(o) & {p for p in o if p[1] < 22}, H('#f2c13a'))
    inn = ell(15.5, 22, 12.4, 5.4); c.fill(inn, tl[3])
    mound = above(ell(15.5, 23, 11, 10), 23); c.fill(ring(mound), H('#6a5a3a')); c.shade(mound, [H('#fffbe8'), H('#fbf0c8'), H('#e8d6a0'), H('#c8b078')], lx=.5, ly=.8)
    for (x, y) in mound:
        if (x * 3 + y * 5) % 7 == 0: c.pts([(x, y), (x + 1, y)], H('#ffffff'))
        elif (x * 5 + y * 3) % 11 == 0: c.px(x, y, H('#c8aa70'))
    # 달버섯 조각
    for (x, y) in [(6, 24), (25, 24), (15, 27)]:
        m = ell(x, y, 3, 1.9); c.fill(ring(m), H('#3a4a7a')); c.shade(m, [H('#e8f4ff'), H('#b8d4f4'), H('#8aa8d8')]); c.pts([(x - 1, y), (x + 1, y)], H('#6a82c0'))
    for (x, y) in [(10, 26), (21, 27), (12, 18), (22, 20)]: c.pts([(x, y), (x + 1, y)], H('#6cc04a')); c.px(x, y, H('#d4f0a0'))
    # 반딧불이
    wing = ell(14, 9, 5.2, 2.3); c.fill(ring(wing), H('#6a82c0')); c.shade(wing, [H('#f4fcff'), H('#d4ecff'), H('#a8c8f0')], lx=.4, ly=.8)
    ab = circ(11, 14, 3.4); c.fill(ring(ab), H('#5a6a10')); c.shade(ab, [H('#fbffb0'), H('#e8ff5a'), H('#b8e020')], lx=.5, ly=.6)
    c.pts([(12, 13), (12, 14), (12, 15)], H('#8aa818')) if False else None
    th = ell(16, 13.6, 3.2, 2.6); c.fill(ring(th), H('#1a1228')); c.shade(th, [H('#5a4a78'), H('#3a3050'), H('#2a2040')])
    hd = circ(20, 14.2, 2.2); c.fill(ring(hd), H('#1a1228')); c.fill(hd, H('#3a3050')); c.px(21, 13, WHITE)
    for (x, y) in [(21, 11), (22, 10), (23, 10)]: c.px(x, y, H('#3a3050'))
    for (x, y) in [(19, 11), (18, 10), (17, 10)]: c.px(x, y, H('#3a3050'))
    # 빛 번짐
    for (x, y) in [(6, 10), (7, 9), (6, 18), (12, 8), (15, 4), (5, 14)]: c.fxp(x, y, H('#f4ff80'))
    for (x, y) in [(5, 14), (17, 5)]:
        for a, b_ in ((1, 0), (-1, 0), (0, 1), (0, -1)): c.fxp(x + a, y + b_, H('#b8e848'))
    for (x, y) in [(25, 9), (28, 14), (4, 5), (24, 4)]:
        c.fxp(x, y, H('#f4ff80'))
        for a, b_ in ((1, 0), (-1, 0), (0, 1), (0, -1)): c.fxp(x + a, y + b_, H('#a8e040'))

@dish(24)
def d24(c):
    bd = rect(2, 25, 29, 29); c.fill(ring(bd), H('#3a2214')); c.shade(bd, [H('#d8a870'), H('#b88050'), H('#8a5a38')], lx=.3, ly=.9)
    c.pts([(5, 27), (6, 27), (7, 27), (15, 28), (16, 28), (23, 27), (24, 27), (25, 27)], H('#8a5a38'))
    cr = ell(15.5, 12.5, 11, 10) | rect(10, 17, 21, 24)
    jaw = rect(10, 17, 21, 24) - {(10, 24), (21, 24)}
    cr = ell(15.5, 12.5, 11, 10) | jaw
    cr = {p for p in cr if p[1] <= 24}
    c.fill(ring(cr), H('#5a3414')); c.shade(cr, [H('#f4c880'), H('#dca458'), H('#b8783a'), H('#8a5428')], lx=.55, ly=.75, cuts=[-.5, 0, .55])
    # 눈구멍·코
    for ex in (11.5, 19.5):
        e = ell(ex, 13, 3, 3.3); c.fill(e, H('#3a1e10')); c.fill({p for p in e if p[1] >= 14}, H('#5a3018')); c.px(round(ex) - 1, 11, H('#7a4a28'))
    c.fill(poly([(14, 17), (17, 17), (15.5, 20)]), H('#3a1e10'))
    # 이빨(칼집)
    for x in (12, 14, 16, 18): 
        for y in range(21, 25): c.px(x, y, H('#8a5428') if y < 24 else H('#5a3414'))
    c.pts([(11, 21), (20, 21)], H('#a8683a'))
    for (x, y) in [(8, 7), (23, 9), (13, 5), (6, 12), (24, 14)]: c.px(x, y, H('#fff0d8')); 
    c.pts([(14, 6), (15, 6), (16, 6)], H('#fbe0a8'))
    # 꽃
    fx_, fy_ = 25, 7
    for (dx, dy) in [(0, -2.6), (2.5, -.8), (1.6, 2.2), (-1.6, 2.2), (-2.5, -.8)]:
        p = circ(fx_ + dx, fy_ + dy, 1.7); c.fill(ring(p), H('#8a2a5a')); 
    for (dx, dy) in [(0, -2.6), (2.5, -.8), (1.6, 2.2), (-1.6, 2.2), (-2.5, -.8)]:
        p = circ(fx_ + dx, fy_ + dy, 1.7); c.shade(p, [H('#ffd0e8'), H('#ff9ac8'), H('#e0629a')], lx=.5, ly=.6)
    c.fill(circ(fx_, fy_, 1.4), H('#ffd84a')); c.px(fx_, fy_, H('#fff6a0'))
    c.pts([(26, 11), (27, 12), (27, 13)], GREEN[2]); leaf(c, 27, 12)
    sparkle(c, 4, 4)

@dish(25)
def d25(c):
    # 불꽃
    for (x, h) in [(5, 5), (8, 7), (22, 7), (26, 5), (12, 4), (19, 4)]:
        fl = poly([(x - 2, 31), (x + 2, 31), (x + 1, 31 - h), (x, 31 - h - 2), (x - 1, 31 - h + 1)]); c.fill(fl, H('#ff8a2a'))
        c.fill(poly([(x - 1, 31), (x + 1, 31), (x, 31 - h + 2)]), H('#ffd84a'))
    # 다리
    for x in (6, 14, 23): c.fill(rect(x, 25, x + 2, 28), H('#2a2438'))
    iron = R('#4a4468')
    body = below(ell(15.5, 13, 13.5, 13), 13) & rect(0, 0, 31, 27)
    c.fill(ring(body), OL); c.shade(body, [iron[0], iron[1], iron[2], iron[3]], lx=.7, ly=.5, cuts=[-.45, 0, .5])
    c.pts([(5, 17), (5, 18), (6, 19), (6, 20), (8, 22)], H('#9a94b8'))
    # 손잡이 고리
    for x0 in (0, 29):
        r = ell(x0 + 1, 15, 1.8, 2.4) - ell(x0 + 1, 15, .5, 1); c.fill(r, iron[3])
    rim = ell(15.5, 13, 13.5, 3.8); c.fill(ring(rim), OL); c.fill(rim, iron[1]); c.fill({p for p in rim if p[1] >= 15}, iron[2])
    st = ell(15.5, 12.8, 12, 2.9); c.shade(st, [H('#b8ff7a'), H('#6ee04a'), H('#3ca83a')], bias=.1)
    # 글씨 대신 해골 표시
    skull_small(c, 13, 18, H('#b8b0d8'), iron[4])
    # 거품 방울
    for (x, y, r) in [(9, 10, 2.2), (14, 8, 2.8), (21, 9, 2.3), (18, 12, 1.6), (25, 12, 1.3), (6, 13, 1.3)]:
        b = circ(x, y, r); c.fill(ring(b), H('#2a7a30')); c.shade(b, [H('#e8ffc0'), H('#9aff6a'), H('#5ae04a')], lx=.5, ly=.6); c.px(round(x) - 1, round(y) - 1, WHITE)
    # 건더기: 붉은 버섯, 고둥, 고사리
    mush_cap(c, 22, 8, 3.2, R('#e04a4a'))
    c.fill(ring(circ(8, 7, 2.5)), H('#6a2a4a')); c.shade(circ(8, 7, 2.5), [H('#ffe0f0'), H('#ffa8cc'), H('#d86a9a')]); c.pts([(8, 6), (9, 7), (8, 8), (7, 7)], H('#9a3a6a'))
    for (x, y) in [(16, 5), (17, 4), (18, 4), (19, 5), (19, 6)]: c.px(x, y, H('#2f8a3a'))
    # 보라 연기
    for (x, ph) in [(10, 0), (17, 2), (23, 4)]: steam(c, x, 0, 3, amp=.6, ph=ph)

@dish(26)
def d26(c):
    # 게타(나무 받침)
    bd = rect(1, 21, 30, 26); c.fill(ring(bd), H('#3a2214')); c.shade(bd, [H('#e0b078'), H('#c08a58'), H('#946034')], lx=.3, ly=.9)
    for x in range(3, 29, 5): c.px(x, 23, H('#a8723e')); c.px(x + 1, 24, H('#a8723e'))
    for x0 in (5, 22): c.fill(rect(x0, 27, x0 + 3, 28), H('#6a4020'))
    rain = [[H('#ff7a9a'), H('#ffb070'), H('#ffe080')], [H('#b8a0ff'), H('#7ac8ff'), H('#8affd0')], [H('#ff9ac8'), H('#ffcf8a'), H('#fff0a0')]]
    for k, x0 in enumerate((2, 12, 22)):
        rice = ell(x0 + 4, 20, 4.6, 3.4); c.fill(ring(rice), H('#6a5a8a')); c.shade(rice, [H('#ffffff'), H('#f4eefa'), H('#d0c4e4')], lx=.5, ly=.7)
        for (dx, dy) in [(1, 20), (3, 21), (6, 20), (7, 21)]: c.px(x0 + dx, dy, H('#d0c4e4'))
        fil = ell(x0 + 4.5, 14.8, 5.4, 4.4) | rect(x0 - 1, 16, x0 + 9, 18)
        c.fill(ring(fil), H('#6a2a3a'))
        for (x, y) in fil:
            band = ((x - x0) + (y - 11) * 1 + k) // 3 % 3
            c.px(x, y, rain[k][band])
        c.pts([(x0 + 1, 13), (x0 + 2, 12), (x0 + 3, 12)], H('#ffffff'))
        c.fill({p for p in fil if p[1] >= 18}, mix(rain[k][2], DEEP, .35))
        if k == 1:
            nori = rect(x0 + 3, 11, x0 + 5, 21); c.fill(nori, H('#2a4a3a')); c.pts([(x0 + 3, 12), (x0 + 3, 13)], H('#4a7a5a'))
    # 와사비
    wb = ell(16.5, 28.8, 2.2, 1.2) if False else None
    sparkle(c, 29, 6); sparkle(c, 3, 8, True); sparkle(c, 16, 6)

@dish(27)
def d27(c):
    star = STAR5(15.5, 16.5, 15, 7)
    c.fill(ring(star), H('#5a3414')); c.shade(star, [H('#f6c878'), H('#dca050'), H('#b8743a'), H('#8a5028')], lx=.6, ly=.7)
    ic = STAR5(15.5, 16.8, 10.5, 4.6); c.shade(ic, [H('#fffbe8'), H('#fff0b8'), H('#f4d878')], lx=.5, ly=.7)
    # 별 모양 스프링클
    sp = [(15, 9, '#7ac8ff'), (10, 15, '#ff9ac8'), (21, 15, '#b8a0ff'), (13, 21, '#8affd0'), (18, 20, '#ff9ac8'), (16, 14, '#ffd84a'), (8, 11, '#fffbe8')]
    for (x, y, col) in sp:
        c.px(x, y, H(col)); c.px(x + 1, y, H(col)); c.px(x, y + 1, H(col)); c.px(x - 1, y, H(col)); c.px(x, y - 1, H(col))
    for (x, y) in [(12, 12), (19, 17), (14, 18), (17, 11), (11, 18), (21, 12)]: c.px(x, y, H('#ffffff'))
    # 꿀 줄
    c.pts([(6, 20), (7, 21), (8, 20), (9, 21)], H('#f7c438')) if False else None
    sparkle(c, 3, 4, True); sparkle(c, 29, 8); sparkle(c, 27, 27, True); sparkle(c, 4, 28)

@dish(28)
def d28(c):
    pl = R('#3a3050')
    c.fill(ell(15.5, 23, 15.2, 8), pl[4]); o = ell(15.5, 22, 15.2, 8); c.shade(o, [pl[1], pl[2], pl[3]], lx=.5, ly=.7)
    c.fill(edge(o), H('#a8202e'))
    inn = ell(15.5, 22, 12.8, 5.8); c.shade(inn, [H('#4a4066'), H('#3a3050'), H('#2a2240')], bias=.2)
    # 소스(피)
    sc = ell(15, 23.4, 11.5, 3.6); c.fill(sc, H('#a8101e')); c.shade(sc, [H('#e0303a'), H('#b01424'), H('#7a0e1e')], lx=.5, ly=.7)
    # 피라냐 (뭉툭한 머리, 커다란 이빨)
    L_, cx_, cy_ = 22, 14, 17
    b = fish(c, cx_, cy_, L_, 12, R('#6a7ca0'), belly=R('#f0583a'), fin=R('#c0302a'), d=1, eye=False)
    xh = round(cx_ + L_ / 2 * .62 + 1)
    # 벌어진 입
    mouth = {(x, y) for x in range(xh - 5, xh + 1) for y in range(cy_ + 1, cy_ + 5) if (x, y) in b and y - cy_ - 1 <= (xh - x) * .0 + 3}
    c.fill({(x, y) for (x, y) in mouth if y <= cy_ + 3 and x >= xh - 5}, H('#4a0a16'))
    for x in range(xh - 4, xh + 1, 2): c.px(x, cy_ + 1, WHITE)
    for x in range(xh - 3, xh + 1, 2): c.px(x, cy_ + 4, WHITE)
    c.px(xh - 5, cy_ + 2, H('#e0303a'))
    # 눈과 반짝이는 비늘
    ex = xh - 6; c.pts([(ex, cy_ - 2), (ex + 1, cy_ - 2), (ex, cy_ - 1), (ex + 1, cy_ - 1)], H('#ffd84a')); c.px(ex + 1, cy_ - 2, BLACK); c.px(ex + 1, cy_ - 1, BLACK)
    for (x, y) in b:
        if y < cy_ and (x * 5 + y * 3) % 7 == 0 and 8 < x < xh - 7: c.px(x, y, H('#c8d4f0'))
    # 구이 자국
    for x in (10, 13, 16):
        for y in range(cy_ - 3, cy_ + 3):
            if (x + y) % 3 == 0 and (x, y) in b: c.px(x, y, H('#3a3050'))
    # 방울토마토와 허브
    for (x, y) in [(4, 25), (27, 25)]:
        t = circ(x, y, 2.6); c.fill(ring(t), H('#5a0a14')); c.shade(t, [H('#ff7a6a'), H('#e0302a'), H('#a81a24')], lx=.5, ly=.6); c.px(x - 1, y - 1, H('#ffd0c0')); c.pts([(x, y - 3), (x + 1, y - 3)], GREEN[2])
    for (x, y) in [(10, 27), (18, 28)]: c.pts([(x, y), (x + 1, y), (x + 2, y)], H('#6cc04a')); c.px(x, y, H('#d4f0a0'))
    # 송곳니 피가 뚝뚝
    c.pts([(xh - 4, cy_ + 5), (xh - 4, cy_ + 6)], H('#e0303a')) 
    sparkle(c, 6, 6); sparkle(c, 27, 8)

@dish(29)
def d29(c):
    iron = R('#4a4468')
    for x0 in (0, 28):
        h = rect(x0, 18, x0 + 3, 20); c.fill(ring(h), OL); c.fill(h, iron[3]); c.fill({p for p in h if p[1] == 18}, iron[1])
    pot = below(ell(15.5, 17, 14.5, 11), 17) & rect(0, 0, 31, 28)
    c.fill(ring(pot), OL); c.shade(pot, [iron[0], iron[1], iron[2], iron[3]], lx=.7, ly=.5, cuts=[-.45, 0, .5])
    c.fill({p for p in pot if p[1] >= 27}, iron[4])
    rim = ell(15.5, 17, 14.5, 5); c.fill(ring(rim), OL); c.fill(rim, H('#d8a850')); c.fill({p for p in rim if p[1] >= 20 and p[0] > 15}, H('#a8782a'))
    br = ell(15.5, 17.4, 12.8, 3.8); c.shade(br, [H('#ff9a4a'), H('#e8502a'), H('#b8281e')], bias=.2)
    # 건더기: 파, 표고, 호박씨, 두부
    for (x, y) in [(19, 15), (22, 17), (25, 18)]: seed(c, x, y, 0)
    tf = rect(17, 18, 20, 20); c.fill(ring(tf), H('#6a3a1a')); c.fill(tf, H('#fff0d0')); c.px(17, 18, WHITE)
    mush_cap(c, 24, 15, 2.4, R('#a8683a'), False)
    for (x, y) in [(16, 14), (21, 19), (14, 19), (25, 20)]: c.pts([(x, y), (x + 1, y)], H('#6cc04a')); c.px(x, y, H('#d4f0a0'))
    # 아귀 머리
    hd = ell(9.5, 16.5, 7, 5.6); c.fill(ring(hd), H('#1a1020')); c.shade(hd, [H('#9a7a98'), H('#6a4a68'), H('#442a42'), H('#32202f')], lx=.5, ly=.7)
    c.fill({(x, y) for (x, y) in hd if 18 <= y <= 20 and x < 14}, H('#4a0a16'))
    for x in range(4, 15, 2): c.px(x, 18, WHITE)
    for x in range(5, 14, 2): c.px(x, 20, WHITE)
    c.pts([(10, 14), (11, 14), (10, 13), (11, 13)], H('#ffd84a')); c.px(11, 14, BLACK); c.px(10, 13, H('#fff6a0'))
    for (x, y) in [(7, 15), (6, 16), (8, 17)]: c.px(x, y, H('#8a6a88'))
    # 낚싯대와 호박등
    for (x, y) in [(8, 12), (8, 10), (9, 8), (11, 6), (13, 4), (16, 3), (18, 3)]: c.px(x, y, H('#5a3a58')); c.px(x, y + 1, H('#3a2038'))
    c.pts([(8, 11), (8, 12)], H('#5a3a58'))
    pm = ell(22, 5.5, 4, 3.6); c.fill(ring(pm), H('#7a2a0a')); c.shade(pm, [H('#ffd05a'), H('#ffa82a'), H('#e8701a')], lx=.5, ly=.6)
    c.pts([(20, 4), (20, 5), (24, 4), (24, 5)], H('#7a2a0a')); c.pts([(21, 7), (22, 7), (23, 7)], H('#7a2a0a')); c.pts([(22, 1), (22, 2)], GREEN[2])
    c.fill(rect(10, 28, 21, 30), H('#2a2438'))
    for (x, y) in [(17, 5), (27, 5), (22, 9)]: c.fxp(x, y, H('#ffe888'))
    sparkle(c, 28, 3, True)
    steam(c, 4, 4, 10, amp=1.0, ph=0)

def gem(c, x, y, r=3, col='#f0a020'):
    g = poly([(x, y - r), (x + r * .8, y - r * .3), (x + r * .6, y + r * .8), (x - r * .6, y + r * .8), (x - r * .8, y - r * .3)])
    k = R(col); c.fill(ring(g), mix(k[4], OL, .5)); c.shade(g, [k[0], k[1], k[2], k[3]], lx=.6, ly=.6)
    c.px(round(x) - 1, round(y) - 1, WHITE)
def crown(c, x, y, w=7):
    pl = [(x, y + 2), (x + w - 1, y + 2), (x + w - 1, y), (x + w - 2, y + 1), (x + w // 2 + 1, y - 1), (x + w // 2, y + 1), (x + w // 2 - 1, y - 1), (x + 2, y + 1), (x + 1, y)]
    cr = poly([(x, y + 3), (x + w - 1, y + 3), (x + w - 1, y), (x + w - 3, y + 2), (x + w // 2, y - 1), (x + 2, y + 2), (x, y)])
    c.fill(ring(cr), H('#7a4a0a')); c.fill(cr, H('#ffd84a')); c.fill({p for p in cr if p[1] == y + 3}, H('#d99a22')); c.px(x + w // 2, y + 1, H('#e0304a')); c.px(x + 1, y, WHITE)

@dish(30)
def d30(c):
    pl = R('#2e6a72')
    c.fill(ell(15.5, 22, 15.5, 8.5), pl[4]); o = ell(15.5, 21, 15.5, 8.5); c.shade(o, [pl[1], pl[2], pl[3]], lx=.5, ly=.7)
    c.fill(edge(o), H('#f2c13a')); c.fill({p for p in edge(o) if p[1] > 21}, H('#c08a22'))
    inn = ell(15.5, 21, 13, 6.4); c.shade(inn, [H('#3f8a92'), H('#2e6a72'), H('#245560')], bias=.2)
    br = R('#e8505a')
    b = fish(c, 17, 20, 22, 12, br, belly=R('#ffc0b0'), fin=R('#c0303a'), d=1, scales=True)
    # 호박색 꿀 글레이즈
    for (x, y) in b:
        if y <= 18 and (x * 3 + y * 7) % 5 == 0: c.px(x, y, H('#ffb040'))
        if (x - 12) ** 2 / 36 + (y - 17) ** 2 / 9 < 1 and (x + y) % 2 == 0: c.px(x, y, H('#f4a030')) if False else None
    c.pts([(10, 17), (11, 16), (12, 16), (13, 16)], H('#ffe090')); c.pts([(17, 15), (18, 15), (19, 15)], H('#ffe090'))
    # 꿀 줄
    for (x, y0, y1) in [(12, 24, 28), (19, 25, 28)]:
        for y in range(y0, y1): c.px(x, y, H('#f7c438'))
        c.px(x, y1, H('#ffe27a'))
    gem(c, 5, 24, 3, '#f0a020'); gem(c, 26, 15, 3, '#f0a020'); gem(c, 25, 26, 2.4, '#ffbe3a')
    for (x, y) in [(22, 11), (23, 10), (21, 10)]: c.pts([(x, y), (x, y + 1)], H('#8fd05a'))
    sparkle(c, 5, 8, True); sparkle(c, 27, 6); sparkle(c, 15, 4)

@dish(31)
def d31(c):
    # 날개
    wg = poly([(12, 12), (6, 3), (1, 1), (0, 7), (4, 11), (10, 14)])
    for w, sg in ((wg, 1), (mirror(wg, 31), -1)):
        c.fill(ring(w), H('#5a6ab0')); c.shade(w, [H('#f4fcff'), H('#c8f0ff'), H('#a8d0ff'), H('#c8b0ff')], lx=.3 * sg, ly=.8)
        for (x1, y1) in [(2, 2), (1, 6), (5, 10)]:
            for (x, y) in line(12, 12, x1, y1):
                if (x, y) in wg: c.px(x if sg == 1 else 31 - x, y, H('#ff9ad0'))
    # 케이크 받침
    c.fill(ell(15.5, 29, 13, 1.8), H('#c4b0e0')); c.fill(ring(ell(15.5, 29, 13, 1.8)), OL) if False else None
    c.fill(rect(14, 26, 17, 29), H('#b8a4d8'))
    plt = ell(15.5, 26, 14, 2.6); c.fill(ring(plt), H('#5a4a7a')); c.shade(plt, [H('#fbf4ff'), H('#e8dcf4'), H('#c0aedc')])
    # 층
    bot = rect(5, 19, 26, 25) - {(5, 25), (26, 25)}; top = rect(8, 12, 23, 18) - {(8, 12), (23, 12)}
    for m in (bot, top): c.fill(ring(m), H('#7a3a5a'))
    c.shade(bot, [H('#ffc0d8'), H('#f8a0c4'), H('#e07aa4')], lx=.7, ly=.5); c.shade(top, [H('#ffc0d8'), H('#f8a0c4'), H('#e07aa4')], lx=.7, ly=.5)
    c.fill(rect(5, 21, 26, 22), H('#fffaf4')); c.fill(rect(8, 16, 23, 16), H('#fffaf4')) if False else None
    c.fill({p for p in bot if p[1] == 21 or p[1] == 22}, H('#fffaf4')); c.fill({p for p in bot if p[1] == 22 and p[0] > 14}, H('#e8dcf0'))
    c.fill({p for p in top if p[1] == 16 or p[1] == 17}, H('#fffaf4')); c.fill({p for p in top if p[1] == 17 and p[0] > 14}, H('#e8dcf0'))
    # 윗면 크림과 흘러내림
    fr = ell(15.5, 12.5, 8.4, 2.6); c.fill(ring(fr), H('#7a3a5a')); c.shade(fr, [H('#ffffff'), H('#fffaf4'), H('#e8dcf0')])
    # 구름 크림 방울
    for (x, y) in [(6, 18), (11, 25), (16, 25), (21, 25), (25, 18)]: pass
    for x in (7, 11, 15, 19, 23):
        d_ = ell(x, 19.3, 1.8, 1.4); c.fill(d_, H('#fffaf4'))
    # 딸기 장식
    for (x, y) in [(12, 10), (19, 10)]:
        sb = ell(x, y, 2.6, 2.4); c.fill(ring(sb), H('#6a1a2a')); c.shade(sb, [H('#ff7a8a'), H('#e0304a'), H('#a8203a')]); c.px(x - 1, y - 1, H('#ffd0c8')); c.px(x, y - 3, GREEN[2])
    c.pts([(15, 9), (16, 9), (15, 10), (16, 10)], H('#ffd84a')); c.px(15, 9, WHITE)
    sparkle(c, 4, 15, True); sparkle(c, 27, 14); sparkle(c, 15, 3, True) if False else None

SEAHORSE = [
 '....wWw.....',
 '...wWWWw.w..',
 '..wWWWWWWw..',
 '.wWWkWWWWw..',
 'wWWWWWWWw...',
 'wWWWwwWWw...',
 '.www.wWWWw..',
 '.....wWWWWw.',
 '....wWWWWWw.',
 '....wWWWWWw.',
 '....wWWWWw..',
 '.....wWWWw..',
 '.....wWWWw..',
 '....wWWWw...',
 '...wWWWw....',
 '..wWWWw.....',
 '..wWWw.ww...',
 '..wWWwwWWw..',
 '...wWWWWw...',
 '....wwww....',
]
@dish(32)
def d32(c):
    # 유령 해마 (찻주전자에서 피어오름)
    P = {'W': H('#e8f8ff'), 'w': H('#8ab4e8'), 'k': H('#2a2048')}
    c.art(13, 0, SEAHORSE, P)
    for (x, y) in [(18, 8), (19, 9), (19, 10), (20, 11)]: c.px(x, y, H('#ffffff'))
    lav = R('#b8a6e8')
    sp = poly([(5, 22), (9, 25), (9, 28), (4, 24)]); c.fill(ring(sp), OL); c.shade(sp, [lav[1], lav[2], lav[3]], lx=.3, ly=.9)
    hd = ell(25.5, 24, 3.6, 3.8) - ell(25.5, 24, 1.8, 2.2); c.fill(ring(ell(25.5, 24, 3.6, 3.8)), OL); c.fill(hd, lav[3]); c.fill({p for p in hd if p[0] < 25 and p[1] < 24}, lav[1])
    body = ell(15, 24, 10.5, 6.6); c.fill(ring(body), OL); c.shade(body, [lav[0], lav[1], lav[2], lav[3]], lx=.6, ly=.7, cuts=[-.5, 0, .5])
    cres = ell(12.5, 24.5, 3, 3) - ell(14, 24, 2.7, 2.7); c.fill(cres, H('#fff3b0'))
    for (x, y) in [(18, 22), (20, 26), (9, 27)]: c.px(x, y, H('#fff3b0'))
    lid = above(ell(15, 18.5, 6, 3), 18); c.fill(ring(lid), OL); c.shade(lid, [lav[1], lav[2], lav[3]], lx=.5, ly=.8)
    c.fill(rect(14, 15, 16, 16), lav[1]); c.px(15, 14, H('#fff3b0')); c.fill(rect(10, 18, 20, 18), H('#f2c13a'))
    for (dx, dy) in [(0, -2), (2, 0), (-2, 0), (1, 2), (-1, 2)]:
        p = ell(26.5 + dx * .8, 28.5 + dy * .5, 1.7, 1.1); c.fill(p, H('#ffffff'))
    c.px(26, 28, H('#ffd84a'))
    sparkle(c, 4, 6, True); sparkle(c, 28, 8)

@dish(33)
def d33(c):
    pl = ell(15.5, 28, 14.5, 3); c.fill(ring(pl), H('#4a3a7a')); c.shade(pl, [H('#c8d8ff'), H('#a8bcf0'), H('#7a8ad0')], lx=.4, ly=.8)
    # 귀
    for (ex, tilt) in [(11.5, -1), (19.5, 1)]:
        e = ell(ex + tilt * .8, 8, 3, 7.4); c.fill(ring(e), H('#7a6a9a')); c.shade(e, [H('#ffffff'), H('#f4eefa'), H('#d0c4e4')], lx=.5, ly=.4)
        i = ell(ex + tilt * .8, 8.5, 1.3, 5); c.shade(i, [H('#ffd0e4'), H('#ff9ac4'), H('#e07aa8')], lx=.3, ly=.8)
    body = ell(15.5, 21, 11, 8) ; c.fill(ring(body), H('#7a6a9a')); c.shade(body, [H('#ffffff'), H('#f8f2fc'), H('#d8cce8'), H('#b4a4d4')], lx=.6, ly=.7, cuts=[-.5, .1, .6])
    # 얼굴
    c.pts([(11, 20), (11, 21), (20, 20), (20, 21)], H('#3a2a4a')); c.px(11, 20, WHITE); c.px(20, 20, WHITE)
    c.pts([(8, 23), (9, 23), (22, 23), (23, 23)], H('#ff9ac4')); c.px(15, 22, H('#ff9ac4')); c.px(16, 22, H('#ff9ac4'))
    c.pts([(14, 24), (15, 24)], H('#7a4a6a')) if False else None
    c.pts([(15, 23), (16, 23)], H('#7a4a6a')); c.px(14, 24, H('#7a4a6a')); c.px(17, 24, H('#7a4a6a'))
    # 쌀가루
    for (x, y) in [(9, 17), (13, 15), (19, 16), (22, 19), (7, 22), (24, 24), (12, 27), (20, 27)]: c.px(x, y, H('#ffffff'))
    c.pts([(10, 14), (11, 13)], H('#ffffff'))
    # 달
    cres = ell(27, 6, 3.4, 3.4) - ell(28.8, 5.2, 3, 3)
    for (x, y) in cres: c.fxp(x, y, H('#fff3b0'))
    sparkle(c, 4, 7, True); sparkle(c, 27, 16)

@dish(34)
def d34(c):
    red = R('#b02a32')
    im, bm = bowl(c, 15.5, 18, 13.5, 5, 11, red, R('#2a1a2a'), R('#f4eefa'), band=R('#f2c13a'), bandy=(23, 24))
    c.fill({p for p in bm if p[1] == 26 and (p[0] // 3) % 2 == 0}, H('#f2c13a'))
    # 밥 둔덕
    rice = above(ell(15.5, 18.5, 12, 9), 18); c.fill(ring(rice), H('#5a4a7a')); c.shade(rice, [H('#ffffff'), H('#f8f2fc'), H('#d8cce8'), H('#b4a4d4')], lx=.5, ly=.8, cuts=[-.5, 0, .5])
    for (x, y) in rice:
        if (x * 5 + y * 3) % 9 == 0: c.px(x, y, H('#d0c4e4'))
    # 황금 잉어
    gl = R('#f6b830')
    b = fish(c, 15.5, 11.5, 23, 9, gl, belly=R('#ffe898'), fin=R('#e0881e'), d=1, scales=True)
    for (x, y) in b:
        if (x * 3 + y * 5) % 11 == 0: c.px(x, y, H('#fff6c0'))
    # 인삼 / 옥수수 / 파
    gs = poly([(22, 15), (25, 15), (26, 20), (24, 18), (23, 20), (22, 18)]) if False else None
    for (x, y) in [(5, 17), (7, 15), (23, 17), (25, 16)]: c.pts([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], H('#ffe040')); c.px(x, y, H('#fff6a0'))
    gs = rect(8, 16, 10, 18) | {(7, 18), (11, 18), (9, 19), (8, 19)}
    c.fill(ring(gs), H('#5a3a1a')); c.fill(gs, H('#e8d0a0')); c.pts([(8, 16), (8, 17)], H('#fff0d0')); c.pts([(9, 18), (10, 17)], H('#b8986a'))
    c.pts([(9, 14), (9, 15)], GREEN[2])
    for (x, y) in [(20, 17), (22, 18), (13, 18)]: c.pts([(x, y), (x + 1, y)], H('#6cc04a')); c.px(x, y, H('#d4f0a0'))
    sparkle(c, 4, 6, True); sparkle(c, 27, 5, True); sparkle(c, 15, 2)
    steam(c, 25, 1, 5, amp=.5, ph=2) if False else None

@dish(35)
def d35(c):
    cup = poly([(6, 5), (25, 5), (24, 10), (20, 19), (11, 19), (7, 10)])
    c.fill(ring(cup), H('#5a6a9a')); c.fill(cup, H('#dff0ff'))
    inner = poly([(7, 7), (24, 7), (23, 10), (19.5, 18), (11.5, 18), (8, 10)])
    layers = [(7, 10, '#8aff9a', '#5ae07a'), (11, 13, '#5ae8d8', '#34c0c0'), (14, 16, '#ff9ad0', '#e070b0'), (17, 19, '#a078f0', '#7a52d0')]
    for (y0, y1, ca, cb) in layers:
        m = {p for p in inner if y0 <= p[1] <= y1}
        c.vshade(m, [H(ca), H(ca), H(cb)], cuts=[.25, .75])
        c.fill({p for p in m if p[1] == y0}, mix(H(ca), WHITE, .45))
    c.pts([(8, 8), (8, 9), (9, 11), (10, 13), (10, 14), (11, 16)], H('#ffffff'))
    # 별사탕 비
    for (x, y, col) in [(12, 9, '#ffd84a'), (19, 12, '#ffffff'), (14, 15, '#ffd84a'), (17, 17, '#ffffff')]: c.px(x, y, H(col))
    # 받침
    c.fill(rect(14, 19, 17, 26), H('#cfe0f4')); c.fill(rect(14, 19, 14, 26), H('#f4faff')); c.fill(rect(17, 19, 17, 26), H('#9ab4d8'))
    ft = ell(15.5, 27.5, 8, 2.2); c.fill(ring(ft), H('#5a6a9a')); c.shade(ft, [H('#f4faff'), H('#dff0ff'), H('#9ab4d8')])
    # 소프트크림과 체리
    for (x, y, rx, ry) in [(15.5, 5, 9, 2.4), (15.5, 3, 6.4, 2.2), (15.5, 1.2, 3.6, 1.6)]:
        m = ell(x, y, rx, ry); c.fill(ring(m), H('#7a6a9a')); c.shade(m, [H('#ffffff'), H('#fff6fc'), H('#ecd8f4')], lx=.4, ly=.8)
    # 웨하스
    for (x, y) in line(20, 6, 28, -1, 3): c.px(x, y, H('#e8c488'))
    for (x, y) in line(20, 8, 28, 1, 1): c.px(x, y, H('#b88040'))
    for (x, y) in line(19, 5, 27, -2, 1): c.px(x, y, H('#f8e0b0'))
    # 별똥별 장식
    st = STAR5(26.5, 15, 3.4, 1.5); c.fill(ring(st), H('#7a4a0a')); c.fill(st, H('#ffd84a'))
    st2 = STAR5(5, 18, 2.8, 1.2); c.fill(ring(st2), H('#7a4a0a')); c.fill(st2, H('#ffe888'))
    for (x, y) in [(29, 12), (28, 9)]: c.fxp(x, y, H('#ffd84a'))
    sparkle(c, 4, 6, True); sparkle(c, 27, 24, True)

@dish(36)
def d36(c):
    sl = R('#3a3050')
    c.fill(ell(15.5, 24, 15.5, 7), sl[4]); o = ell(15.5, 23, 15.5, 7); c.shade(o, [sl[1], sl[2], sl[3]], lx=.5, ly=.7)
    c.fill(edge(o), H('#a8282a'))
    sc = [H('#ff5a2a'), H('#ffb040'), H('#e0301a')]
    def piece(cx, cy):
        r = 6.2
        side = circ(cx, cy + 2, r); c.fill(ring(side), OL); c.fill(side, H('#8a1a1a'))
        d_ = circ(cx, cy, r); c.fill(ring(d_), OL)
        for (x, y) in d_:
            ang = math.atan2(y - cy, x - cx); i = int((ang + math.pi) / (2 * math.pi) * 10)
            c.px(x, y, sc[0] if i % 2 == 0 else sc[1])
        c.fill({p for p in d_ if p[1] < cy - 3}, sc[1]) if False else None
        nori = circ(cx, cy, 4.1); c.fill(nori, H('#243a2c')); rice = circ(cx, cy, 3.4); c.shade(rice, [H('#ffffff'), H('#f4eefa'), H('#d0c4e4')], lx=.5, ly=.6)
        c.fill(circ(cx, cy, 1.4), H('#e0402a')); c.px(round(cx) - 1, round(cy) - 1, H('#ff9a6a')); c.px(round(cx) + 1, round(cy) + 1, H('#6aae4a'))
        c.pts([(round(cx) - 5, round(cy) - 3), (round(cx) - 4, round(cy) - 4)], H('#ffe0a0'))
    piece(15.5, 11.5); piece(8.5, 20); piece(22.5, 20)
    # 고추
    pp = line(2, 27, 9, 25, 2); c.fill(ring(pp), H('#5a0a14')); c.fill(pp, H('#e0242a')); c.px(3, 26, H('#ff8a7a')); c.pts([(1, 27), (1, 28)], GREEN[2])
    # 불꽃
    for (x, h) in [(11, 5), (16, 7), (21, 5)]:
        pass
    for (x0, y0, h) in [(10, 3, 4), (15, 1, 5), (21, 3, 4)]:
        fl = poly([(x0 - 1.5, y0 + h), (x0 + 1.5, y0 + h), (x0 + 1, y0 + 1), (x0, y0 - 1), (x0 - 1, y0 + 1)])
        for (x, y) in fl: c.fxp(x, y, H('#ff7a2a') if y > y0 + 1 else H('#ffb040'))
        c.fxp(x0, y0 + h - 1, H('#ffe880')); c.fxp(x0, y0 + h - 2, H('#ffe880'))
    sparkle(c, 28, 8)

@dish(37)
def d37(c):
    navy = R('#2a3a8a'); food = R('#4a5ac8')
    im, bm = bowl(c, 15.5, 16, 14, 5.4, 12, navy, R('#e8c050'), food, band=R('#e8c050'), bandy=(22, 22))
    c.shade(im, [H('#6a7ae0'), H('#4a5ac8'), H('#3a44a0')], bias=.2)
    for (x, y) in [(5, 24), (9, 25), (14, 24), (19, 25), (24, 24)]: c.px(x, y, H('#ffd84a')); c.px(x + 1, y, H('#ffd84a')); c.px(x, y + 1, H('#ffd84a')); c.px(x - 1, y, H('#ffd84a')); c.px(x, y - 1, H('#ffd84a'))
    wh = R('#6aa8f0')
    body = {p for p in (ell(13.5, 13, 8.5, 6.2) | ell(7.5, 12.5, 3.5, 3.2)) if p[1] <= 17}
    stalk = poly([(7, 12), (4, 9), (3, 6), (5, 6), (6, 9), (9, 11)])
    flu = poly([(0, 4), (3, 6), (4, 2), (5, 6), (8, 4), (6, 8), (2, 8)])
    for m in (stalk | flu,): c.fill(ring(m), H('#1a2a6a'))
    c.fill(stalk | flu, wh[2]); c.fill({p for p in flu if p[1] <= 5}, wh[1]); c.fill({p for p in stalk if p[0] > 5}, wh[3])
    c.fill(ring(body), H('#1a2a6a')); c.shade(body, [wh[0], wh[1], wh[2], wh[3]], lx=.5, ly=.8)
    belly = {p for p in body if p[1] >= 15 and 10 <= p[0] <= 21}; c.fill(belly, H('#dff0ff'))
    for x in range(11, 21, 2):
        for y in (15, 16): 
            if (x, y) in body: c.px(x, y, H('#9ac4f0'))
    c.pts([(17, 11), (18, 11)], BLACK); c.px(17, 10, WHITE); c.px(19, 14, H('#2a3a8a')); c.pts([(20, 14), (21, 14)], H('#2a3a8a'))
    c.pts([(13, 14), (12, 15), (13, 15)], wh[3])
    for (x, y) in [(16, 6), (16, 7), (16, 8), (15, 5), (17, 5), (14, 6), (18, 6), (13, 7), (19, 7), (16, 4)]: c.fxp(x, y, H('#dff4ff'))
    c.fxp(16, 3, H('#ffffff')); c.fxp(14, 4, H('#a8d8ff')); c.fxp(18, 4, H('#a8d8ff'))
    for (x, y) in line(23, 12, 30, 4, 1): c.fxp(x, y, H('#ffe888'))
    for (x, y) in line(23, 13, 30, 6, 1): c.fxp(x, y, H('#ffb040'))
    for (x, y) in circ(22.5, 12.5, 2.3): c.fxp(x, y, H('#ffd84a'))
    c.fxp(22, 12, WHITE); c.fxp(21, 12, H('#fff3b0')); c.fxp(22, 11, H('#fff3b0'))
    sparkle(c, 4, 20) if False else None; sparkle(c, 26, 18, True)

@dish(38)
def d38(c):
    gd = R('#f2c13a')
    c.fill(ell(15.5, 22, 15.8, 9), gd[4]); o = ell(15.5, 21, 15.8, 9); c.shade(o, [gd[0], gd[1], gd[2], gd[3]], lx=.5, ly=.7)
    for (x, y) in edge(o):
        if (x + y) % 2 == 0: c.px(x, y, H('#fff0a0'))
    inn = ell(15.5, 21, 13, 6.6); c.shade(inn, [H('#7a3a8a'), H('#5a2a78'), H('#431e60')], bias=.2)
    c.fill(edge(inn), H('#f2c13a'))
    # 메기왕
    ct = R('#7a6a58')
    b = fish(c, 13, 19.5, 21, 9, ct, belly=R('#d8c8a8'), fin=R('#5a4a40'), d=1, dorsal=True)
    # 수염
    for (x, y) in [(23, 19), (24, 20), (25, 21), (26, 22), (27, 22)]: c.px(x, y, H('#5a4a40'))
    for (x, y) in [(23, 18), (24, 17), (25, 16), (26, 16), (27, 15)]: c.px(x, y, H('#5a4a40'))
    for (x, y) in [(22, 21), (22, 22), (23, 23), (23, 24)]: c.px(x, y, H('#8a7a68'))
    crown(c, 16, 12, 7)
    # 호박(달)과 도토리, 보석
    pm = ell(25.5, 24, 4.4, 3.8); c.fill(ring(pm), H('#7a2a0a')); c.shade(pm, [H('#ffd05a'), H('#ffa82a'), H('#e8701a'), H('#b84a10')], lx=.5, ly=.6)
    c.pts([(25, 21), (25, 22), (25, 26), (25, 27)], H('#b84a10')); c.pts([(25, 20), (26, 20)], GREEN[2])
    cres = ell(6.5, 25, 3.2, 3.2) - ell(8, 24.2, 2.8, 2.8); c.fill(ring(cres), H('#7a2a0a')); c.fill(cres, H('#ffa82a'))
    ac = ell(8, 14, 2.4, 2.9); c.fill(ring(ac), H('#6a4a0a')); c.shade(ac, [H('#ffe888'), H('#f2c13a'), H('#c8921e')]); c.fill(above(ell(8, 12.5, 3, 1.8), 12), H('#c8921e')); c.px(8, 11, H('#6a4a0a'))
    sparkle(c, 4, 6, True); sparkle(c, 28, 8, True); sparkle(c, 15, 4); steam(c, 21, 3, 8, amp=.8, ph=1) if False else None

@dish(39)
def d39(c):
    gd = R('#e8b030')
    c.fill(ell(15.5, 25, 15.8, 6.4), gd[4]); o = ell(15.5, 24, 15.8, 6.4); c.shade(o, [gd[0], gd[1], gd[2], gd[3]], lx=.5, ly=.7)
    for (x, y) in edge(o):
        if (x * 2 + y) % 3 == 0: c.px(x, y, H('#fff6c0'))
    inn = ell(15.5, 24, 13.2, 4.6); c.shade(inn, [H('#4a3a9a'), H('#352a7a'), H('#28205e')], bias=.2)
    # 호수의 주인(푸른 금빛 물고기)
    bl = R('#4a8ae0')
    b = fish(c, 13, 20, 24, 11, bl, belly=R('#ffe8a0'), fin=R('#f2c13a'), d=1, scales=True, tailw=1.15)
    for (x, y) in b:
        if (x * 3 + y * 5) % 13 == 0 and y < 22: c.px(x, y, H('#a8d4ff'))
    crown(c, 18, 12, 7)
    # 달호박(빛나는)
    pm = ell(27, 20.5, 3.6, 3.6)
    # 소울 불꽃 (푸른 도깨비불)
    def flame(x, y, h):
        fl = poly([(x - 2, y + h), (x + 2, y + h), (x + 1.4, y + h * .4), (x, y - 1), (x - 1.4, y + h * .35)]); c.fill(ring(fl), H('#2a3a8a')); c.shade(fl, [H('#e8f8ff'), H('#8ad8ff'), H('#4a8af0')], lx=.2, ly=.9)
        c.px(x, y + h - 1, WHITE)
    flame(5, 8, 6); flame(10, 3, 5)
    # 소원의 별
    st = STAR5(22.5, 5, 4.2, 1.9); c.fill(ring(st), H('#7a4a0a')); c.shade(st, [H('#fff6c0'), H('#ffd84a'), H('#e0a020')], lx=.5, ly=.7)
    # 달 호박
    p = ell(26.5, 20, 3.6, 3.4); c.fill(ring(p), H('#7a2a0a')); c.shade(p, [H('#ffd05a'), H('#ffa82a'), H('#e8701a')], lx=.5, ly=.6)
    cr = ell(26.5, 20, 1.8, 1.8) - ell(27.5, 19.6, 1.6, 1.6)
    c.fill(cr, H('#fff3b0')); c.pts([(26, 16), (27, 16)], GREEN[2])
    for (x, y) in [(3, 14), (28, 28), (6, 28)]: sparkle(c, x, y)
    sparkle(c, 15, 6, True); sparkle(c, 28, 5, True); sparkle(c, 3, 22, True)

# ---------- 시트 만들기 ----------
NAMES = None
def names():
    global NAMES
    if NAMES is None:
        NAMES = ['호박씨 크림수프', '도토리 쿠키', '유령 피라미 튀김', '버섯 꼬치구이', '산딸기 잼 토스트', '당근 머핀', '세잎클로버 차', '피처럼 붉은 토마토주스', '호박 붕어 버섯 조림', '박쥐 날개 잎 쌈',
                 '거미 버섯 마카롱', '블루베리 파이', '이끼 송사리 오믈렛', '꿀 군밤 꼬치', '유령 마시멜로', '늪지 추어탕', '독사과 캔디', '옥수수 달빛수프', '젤리 해파리 젤리', '거미 가재 매운찜',
                 '해골 메기 사골탕', '솜사탕 넙치 푸딩', '달빛 송어 구이', '반딧불이 리소토', '해골 꽃 빵', '마녀 솥 스튜', '무지개 송어 초밥', '별가루 쿠키', '뱀파이어 피라냐 스테이크', '호박등 아귀 전골',
                 '호박석 꿀 도미 조림', '요정 날개 케이크', '유령 해마 차', '달토끼 찹쌀떡', '황금 잉어 덮밥', '오로라 파르페', '화룡 용비늘 롤', '별똥별 고래 수프', '호박달 메기왕 정찬', '호수의 주인 만찬']
    return NAMES

def build():
    sheet = Image.new('RGBA', (S * 40, S), (0, 0, 0, 0))
    for i in range(40):
        if i in REG:
            cv = Cv(); REG[i](cv); sheet.alpha_composite(cv.render(), (i * S, 0))
    return sheet

def preview(sheet, d):
    os.makedirs(d, exist_ok=True)
    bg = (0x21, 0x17, 0x33, 255); Z = 4
    big = Image.new('RGBA', (10 * S * Z, 4 * S * Z), bg)
    lab_h = 22
    lab = Image.new('RGBA', (10 * S * Z, 4 * (S * Z + lab_h)), bg)
    fnt = None
    for p in ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/opentype/unifont/unifont.otf'):
        try: fnt = ImageFont.truetype(p, 11); break
        except Exception: pass
    dr = ImageDraw.Draw(lab); nm = names()
    for i in range(40):
        cell = sheet.crop((i * S, 0, i * S + S, S)).resize((S * Z, S * Z), Image.NEAREST)
        x, y = (i % 10) * S * Z, (i // 10) * S * Z
        big.alpha_composite(cell, (x, y))
        ly = (i // 10) * (S * Z + lab_h)
        lab.alpha_composite(cell, (x, ly))
        t = '%d %s' % (i, nm[i])
        dr.text((x + 2, ly + S * Z + 3), t, fill=(230, 220, 250), font=fnt)
    big.save(os.path.join(d, 'dishes_x4.png')); lab.save(os.path.join(d, 'dishes_x4_label.png'))

if __name__ == '__main__':
    sh = build(); sh.save(OUT)
    if '--preview' in sys.argv: preview(sh, sys.argv[sys.argv.index('--preview') + 1])
    print('dishes.png', sh.size, len(REG), 'icons')
