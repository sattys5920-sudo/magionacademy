#!/usr/bin/env python3
# 채집물 새 25종 아이콘 (도감 확장 2차 · 늦가을~첫겨울) — forage_icons.py 와 같은 도구 상자 · 같은 화풍
# 순서는 tools/dex2_spec.json 의 "forage" 순서 (시트 칸 50..74).
#   python3 tools/iso/forage_icons75.py --preview DIR   # DIR/forage_new25.png (800x32) + DIR/forage_new25_x4_lbl.png
#   python3 tools/iso/forage_icons75.py --apply         # public/art/forage.png 앞 50칸 + 새 25칸 → 2400x32
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forage_icons as FI
from forage_icons import (S, H, R4, OL, WHITE, E, RE, RC, PG, LN, bez, bez3, LEAF, HEART, ring, erode, rot, shift, Cv,
                          lerp, lerpc, leaf_info, sep, calyx, mushroom, spot, dilate, smooth, moss_mound,
                          BROWN, GREEN, GREEN2, RED, GREY, YEL, CREAM, WOOD, PURP, BLUE, HI)

ROOT = FI.ROOT
SHEET = os.path.join(ROOT, 'public', 'art', 'forage.png')
SPEC = os.path.join(ROOT, 'tools', 'dex2_spec.json')
BASE = 50     # 기존 칸 수
N2 = 25

ICONS2 = []


def icon2(f):
    ICONS2.append(f)
    return f


# ---------------------------------------------------------------- 보조
FROST = [H('#ffffff'), H('#e4f4ff'), H('#c4e2fa')]
ICE = R4('#f4fcff', '#b8e6ff', '#6cb8ec', '#3a78c4')
TWIG = R4('#b88a62', '#8a5e3e', '#5e3e28', '#3a2418')


def star(cx, cy, r0, r1, n=5, ang=-90):
    pts = []
    for k in range(n * 2):
        r = r0 if k % 2 == 0 else r1
        a = math.radians(ang + k * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return PG(pts)


def lobed_leaf(p0, p1, w, lobes=4, depth=.32, a=2.0, b=.62):
    """LEAF 에 물결(갈래) 가장자리를 준 잎 (참나무잎 같은)"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    m = set()
    for x, y in FI._pts():
        qx, qy = x + .5 - p0[0], y + .5 - p0[1]
        t = (qx * ux + qy * uy) / L
        if t < 0 or t > 1:
            continue
        s = -qx * uy + qy * ux
        u = 2 * t - 1
        hw = w * (max(0.0, 1 - abs(u) ** a)) ** b
        hw *= 1 - depth * abs(math.sin(math.pi * t * lobes + .3)) ** 1.5
        if abs(s) <= hw:
            m.add((x, y))
    return m


def frost_edge(c, m, rate=.7, rng=None, tl_only=True):
    """잎 가장자리(특히 왼쪽 위)에 하얀 서리"""
    rr = rng or c.rng
    inner = erode(m, 1)
    for q in sorted(m - inner):
        tl = (q[0] - 1, q[1]) not in m or (q[0], q[1] - 1) not in m
        if (tl or not tl_only) and rr.random() < rate:
            c.put(q[0], q[1], FROST[0] if rr.random() < .55 else FROST[1])
            if rr.random() < .45:
                n = (q[0] + 1, q[1] + 1)
                if n in inner:
                    c.put(n[0], n[1], FROST[2])


def glow_ring(c, col, r=2.8, a=120):
    c.halo = (col, r, a)


# ======================================================================= 0 서리 낙엽
@icon2
def frostleaf(c):
    LF = R4('#d8a066', '#a86a38', '#7a4426', '#4e2a1a')
    P0, P1 = (7.5, 26.5), (27, 3.5)
    m = lobed_leaf(P0, P1, 10.6, lobes=4.5, depth=.42, b=.55)
    c.shade(m, LF, 'diag', th=(.5, -.1, -.55))
    # 잎맥
    c.fill(LN([P0, lerp(P0, P1, .92)], 1.0) & m, LF[3])
    for t in (.3, .5, .7):
        A = lerp(P0, P1, t)
        for sgn in (-1, 1):
            e = (A[0] + sgn * 6.0 + 3.0, A[1] + sgn * 5.0 - 3.6)
            e = (A[0] + (sgn * 5.2) * .77 + 2.4, A[1] + (sgn * 5.2) * .64 - 2.6)
            c.fill(LN([A, e], .8) & erode(m, 1), LF[2])
    # 벌레 먹은 점 / 얼룩
    for q in [(17, 17), (13, 14), (20, 11)]:
        if q in m:
            c.put(q[0], q[1], LF[3])
    # 서리
    frost_edge(c, m, rate=.8)
    rr = c.rng
    for _ in range(26):
        q = (rr.randint(6, 26), rr.randint(4, 26))
        if q in erode(m, 1) and (q[0] + q[1]) < 33:
            c.put(q[0], q[1], FROST[1] if rr.random() < .5 else FROST[2])
    # 잎자루
    st = LN([(8.5, 25.5), (3.5, 30.5)], 1.6)
    c.bevel(st, R4('#c08050', '#8a5432', '#5e3620', '#3a2016'))
    c.spark(26, 22, H('#e4f4ff'), 1, WHITE)
    c.dot(5, 8, H('#e4f4ff'))


# ======================================================================= 1 마른 갈대
@icon2
def reed(c):
    STK = R4('#f0dca0', '#ccae6a', '#9a7c44', '#6a522c')
    PL = R4('#fff4dc', '#e8d2a4', '#bc9c70', '#86684a')
    stalks = [
        (bez((11, 31), (11, 20), (8, 10), 14), (8, 10), (3.2, 1.0), 4.0, -1),
        (bez((16, 31), (17, 18), (19.5, 6), 14), (19.5, 6), (25, 0.6), 4.4, 1),
        (bez((21, 31), (23, 23), (27, 16), 14), (27, 16), (30.5, 11), 3.2, 1),
    ]
    for pts, top, tip, w, sgn in stalks:
        st = LN(pts, 1.5)
        c.bevel(st, STK)
    # 잎(마른 띠)
    blade = LEAF((15, 31), (4, 17.5), 1.7, a=1.6, b=.8, bend=1.5)
    c.shade(blade, STK, 'diag')
    blade2 = LEAF((18, 31), (29, 22), 1.5, a=1.6, b=.8, bend=-1.2)
    c.shade(blade2, STK, 'diag')
    rr = c.rng
    for pts, top, tip, w, sgn in stalks:
        ctrl = (top[0] + (tip[0] - top[0]) * .2 - sgn * 1.0, tip[1] - 1.5)
        curve = bez((top[0], top[1] + 3), ctrl, (tip[0] + sgn * 1.5, tip[1] + 2.5), 14)
        pl = set()
        for i, (x, y) in enumerate(curve):
            r = w * .62 * (1 - .55 * i / 14)
            pl |= E(x, y, r, r)
        c.shade(pl, PL, 'diag', th=(.4, -.15, -.6))
        # 부슬부슬 털
        for q in sorted(pl):
            r = rr.random()
            if r < .22:
                c.put(q[0], q[1], PL[0])
            elif r < .36:
                c.put(q[0], q[1], PL[2])
        for q in sorted(ring(pl)):
            if rr.random() < .28 and q not in c.p:
                c.put(q[0], q[1], PL[1])
    c.pts([(10, 23), (10, 22), (16, 22), (16, 21)], STK[0])


# ======================================================================= 2 찔레 열매
@icon2
def rosehip(c):
    HP = R4('#ff9a7a', '#e2382e', '#a41a2e', '#62122a')
    br = LN(bez3((3, 29), (8, 20), (14, 12), (28, 3)), 1.3)
    c.bevel(br, TWIG)
    for (a, b) in [((9.5, 19.5), (5, 11)), ((15, 12.5), (20, 16.5)), ((20, 8.2), (19.5, 2.5))]:
        c.fill(LN([a, b], 1.0), TWIG[2])
    # 작은 잎 하나
    GL = R4('#a8d878', '#6aa448', '#447a3c', '#2a5432')
    lf = LEAF((24, 5.4), (30, 9.2), 1.8, a=2, b=.7)
    c.shade(lf, GL, 'diag')
    hips = [((5, 11), (5.6, 3.8), 3.2), ((20, 16.5), (22.5, 27.5), 3.4), ((19.5, 2.5), (11.5, 6.0), 2.9)]
    hips = [((4.8, 10.5), 3.0, 4.6), ((20.4, 21.5), 3.2, 4.8), ((10.8, 4.8), 2.8, 4.2)]
    for k, ((cx, cy), rx, ry) in enumerate(hips):
        m = LEAF((cx, cy - ry), (cx, cy + ry), rx, a=2, b=.6, skew=0.1)
        sep(c, m, HP[3])
        c.shade(m, HP, 'sphere', box=(cx, cy, rx, ry), th=(.8, .4, .0))
        by = int(cy + ry) - 1
        c.pts([(int(cx), by), (int(cx) - 1, by), (int(cx) + 1, by)], H('#3a1a14'))
        c.put(int(cx - rx * .4), int(cy - ry * .4), H('#ffe0c8'))
        c.put(int(cx - rx * .4), int(cy - ry * .4) + 1, HP[0])
    # 열매 꼭지 연결
    c.fill(LN([(9.5, 19.5), (20.4, 16.8)], 1.0) - set(), TWIG[2])


# ======================================================================= 3 자작나무 껍질
@icon2
def birch(c):
    BK = R4('#ffffff', '#ece8f0', '#c4bcd0', '#8e86a0')
    IN = R4('#f2b884', '#d08850', '#9a5a34', '#5e3420')
    ang = -28
    cx, cy = 17, 17
    L, r = 11.5, 6.4

    def T(pts):
        return rot(pts, ang, (cx, cy))
    body = PG(T([(cx - L, cy - r), (cx + L, cy - r), (cx + L, cy + r), (cx - L, cy + r)]))
    endR = RE(*T([(cx + L, cy)])[0], 2.6, r, ang)
    endL = RE(*T([(cx - L, cy)])[0], 2.6, r, ang)
    body |= endR
    c.shade(body, BK, 'sphere', box=None)
    # 원통 음영 (축에 수직 방향)
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)
    for q in body:
        v = ((q[0] + .5 - cx) * nx + (q[1] + .5 - cy) * ny) / r
        k = 0 if v < -.55 else 1 if v < .3 else 2 if v < .75 else 3
        c.put(q[0], q[1], BK[k])
    # 검은 줄무늬(가로 껍질눈)
    ux, uy = math.cos(a), math.sin(a)
    rr = c.rng
    marks = [(-8, -3.5, 3.0), (-5, 2.5, 2.2), (-1.5, -1.0, 4.0), (2.5, 3.2, 2.6), (5.5, -3.0, 3.0), (8.5, 1.0, 2.6), (-9.5, 3.5, 1.8), (1, -4.4, 1.6)]
    for (u, v, ln) in marks:
        p = (cx + u * ux + v * nx, cy + u * uy + v * ny)
        q0 = (p[0] - nx * ln / 2, p[1] - ny * ln / 2)
        q1 = (p[0] + nx * ln / 2, p[1] + ny * ln / 2)
        mk = LN([q0, q1], 1.0) & erode(body, 1)
        mk = {q for q in mk}
        # 껍질눈은 축 방향(가로)로 짧게
        q0 = (p[0] - ux * ln / 2, p[1] - uy * ln / 2)
        q1 = (p[0] + ux * ln / 2, p[1] + uy * ln / 2)
        mk = LN([q0, q1], 1.0) & erode(body, 1)
        c.fill(mk, H('#2a2232'))
    # 돌돌 말린 끝 (왼쪽)
    endc = T([(cx - L, cy)])[0]
    em = RE(endc[0], endc[1], 3.2, r + .2, ang)
    sep(c, em, BK[3])
    c.fill(em, IN[1])
    # 나선
    for k in range(40):
        t = k / 40
        rad = (r - .3) * (1 - t * .85)
        th = t * 2.4 * 2 * math.pi
        px = endc[0] + math.cos(th) * rad * 0.42 * ux + math.sin(th) * rad * nx
        py = endc[1] + math.cos(th) * rad * 0.42 * uy + math.sin(th) * rad * ny
        q = (int(px), int(py))
        if q in em:
            c.put(q[0], q[1], BK[1] if t < .35 else IN[3])
    for q in em:
        if (q[0] - 1, q[1]) not in em and c.p[q] == IN[1]:
            c.put(q[0], q[1], IN[0])
    c.pts([(14, 9), (15, 9), (16, 8)], WHITE)


# ======================================================================= 4 산사 열매
@icon2
def hawthorn(c):
    HW = R4('#ff8a7a', '#d4243a', '#94143a', '#580c2e')
    GL = R4('#a8dc70', '#5ea844', '#3a7c3c', '#255632')
    # 잎 두 장 (갈래 잎)
    for (p0, p1, w) in [((15, 9), (5, 3.5), 3.3), ((17, 9), (27.5, 4.5), 3.3)]:
        lf = lobed_leaf(p0, p1, w, lobes=2.5, depth=.3)
        sep(c, lf, GL[3])
        c.shade(lf, GL, 'diag')
        c.fill(LN([p0, lerp(p0, p1, .85)], .8) & lf, GL[3])
    stems = [(16, 9)]
    berries = [(10.5, 16, 4.0), (21.5, 15.5, 4.0), (16, 13.5, 3.8), (7.5, 23.5, 3.9), (16.5, 21.5, 4.2), (24.5, 23, 3.9), (12, 27, 3.6), (20.5, 27.5, 3.6)]
    for (x, y, r) in berries:
        c.line((16, 9), (x, y - r + 1), TWIG[2], 1.0)
    for (x, y, r) in berries:
        m = E(x, y, r, r)
        sep(c, m, HW[3])
        c.shade(m, HW, 'sphere', th=(.82, .42, .02))
        c.put(int(x - r * .45), int(y - r * .45), H('#ffd8d0'))
        # 꽃받침 자국 (아래쪽 작은 점)
        c.put(int(x + r * .3), int(y + r * .4), H('#3a0c20'))


# ======================================================================= 5 팽이버섯
@icon2
def enoki(c):
    STM = R4('#ffffff', '#f4eedc', '#d4c8aa', '#9a8c70')
    CAP = R4('#fffcf0', '#f2e6c8', '#cdb88e', '#8e7a58')
    base = (16, 27)
    tops = [(5, 6.5), (9.5, 3.5), (14, 2.5), (18.5, 3), (23, 4.5), (27, 7.5), (7.5, 10), (12, 7), (20.5, 7.5), (25, 11), (16.5, 6)]
    sts = []
    for k, (tx, ty) in enumerate(tops):
        bx = base[0] + (tx - 16) * .18
        ctrl = ((bx + tx) / 2 + (1 if k % 2 else -1) * .8, (base[1] + ty) / 2 + 2)
        pts = bez((bx, base[1]), ctrl, (tx, ty + 1.5), 14)
        sts.append((pts, (tx, ty)))
    for pts, (tx, ty) in sts:
        st = LN(pts, 1.6)
        sep(c, st, STM[3])
        c.fill(st, STM[1])
        c.fill(LN([(x - .5, y) for x, y in pts[2:]], .6) & st, STM[0])
    for pts, (tx, ty) in sts:
        cp = E(tx, ty + .6, 2.2, 1.7)
        sep(c, cp, CAP[3])
        c.shade(cp, CAP, 'sphere', th=(.7, .2, -.3))
    # 밑동 (뭉친 뿌리)
    root = E(16, 27.8, 5.6, 3.2)
    c.shade(root, R4('#f0e0c0', '#d0b48a', '#a08460', '#6a5440'), 'sphere')
    rr = c.rng
    for q in sorted(root):
        if rr.random() < .2:
            c.put(q[0], q[1], H('#8a6c4c'))
    band = RC(11, 22, 21, 24) & dilate(set().union(*[LN(p, 1.6) for p, _ in sts]), 1)
    c.shade(band, R4('#e8c890', '#c09860', '#8e6a40', '#5e4428'), 'cylv')


# ======================================================================= 6 서리 머루
@icon2
def frostberry(c):
    GR = R4('#a48ad8', '#5a3c9a', '#3a2470', '#24164a')
    GL = R4('#b4d878', '#74a84c', '#4a7c40', '#2c5434')
    st = LN(bez((16, 8), (16, 4), (19, 1.5), 8), 1.6)
    c.bevel(st, TWIG)
    tend = LN(bez3((17, 4.5), (12, 0.5), (8, 4), (10, 7)), .9)
    c.fill(tend, GL[2])
    lf = LEAF((18, 4), (29, 6.5), 3.6, a=2, b=.65)
    lf = lobed_leaf((18, 4.5), (29.5, 7), 3.8, lobes=2.5, depth=.25)
    c.shade(lf, GL, 'diag')
    c.fill(LN([(18, 4.5), (28, 6.8)], .8) & lf, GL[3])
    grapes = [(9.5, 11.5), (16, 10.5), (22.5, 11.5), (6.8, 17.5), (12.8, 16.8), (19.2, 16.8), (25.3, 17.5),
              (9.8, 22.8), (16, 22.3), (22.2, 22.8), (13, 27.6), (19, 27.6)]
    rr = c.rng
    for (x, y) in grapes:
        m = E(x, y, 3.5, 3.5)
        sep(c, m, GR[3])
        c.shade(m, GR, 'sphere', th=(.8, .4, -.05))
        # 서리(분) — 위쪽 하얀 가루
        for q in sorted(m):
            if q[1] < y - .5 and rr.random() < .32:
                c.put(q[0], q[1], H('#c8c4ec') if rr.random() < .6 else H('#e8eaff'))
        c.put(int(x - 1.4), int(y - 1.4), WHITE)
    c.spark(27, 25, H('#e4f0ff'), 1, WHITE)
    c.dot(4, 26, H('#e4f0ff'))


# ======================================================================= 7 고드름 조각
@icon2
def icicle(c):
    y0, y1 = 3.0, 30.6

    def cxw(y):
        t = (y - y0) / (y1 - y0)
        w = 7.6 * (1 - t) ** 1.15 + .4
        w *= 1 + .09 * math.sin(t * 22)          # 물결 마디
        return 16.5 - 1.6 * t + 1.2 * math.sin(t * 3.0), w
    m = set()
    for x, y in FI._pts():
        px, py = x + .5, y + .5
        ytop = y0 + 1.6 * abs(math.sin(px * .9)) + (1.4 if 12 < px < 15 else 0)   # 부러진 윗면
        if py < ytop or py > y1:
            continue
        cx, w = cxw(py)
        if abs(px - cx) <= w:
            m.add((x, y))
    for q in m:
        cx, w = cxw(q[1] + .5)
        d = (q[0] + .5 - cx) / max(w, .6)
        k = 0 if d < -.55 else 1 if d < .1 else 2 if d < .6 else 3
        c.put(q[0], q[1], ICE[k])
    # 마디 무늬
    for yy in (9, 14, 19, 24):
        for q in m:
            if q[1] == yy and c.p[q] == ICE[1]:
                c.put(q[0], q[1], H('#9ad4f8'))
    # 윗면(부러진 단면)
    for q in m:
        if (q[0], q[1] - 1) not in m:
            c.put(q[0], q[1], WHITE if c.p[q] in (ICE[0], ICE[1]) else ICE[1])
    # 하이라이트 줄
    hl = [(cxw(y)[0] - cxw(y)[1] * .45, y) for y in (6, 12, 18, 24)]
    c.fill(LN(hl, 1.0) & erode(m, 1), WHITE)
    # 속 기포
    c.pts([(18, 10), (17, 16), (19, 13)], H('#e4f6ff'))
    c.spark(25, 14, WHITE, 2, WHITE)
    c.spark(7, 22, H('#c8ecff'), 1, WHITE)
    c.dot(22, 27, H('#c8ecff'))


# ======================================================================= 8 촛불 이끼
@icon2
def candlemoss(c):
    MOSS = R4('#b2e868', '#6cb83c', '#43873a', '#2a5a34')
    m = moss_mound(c, MOSS, None)
    rr = c.rng
    top = [q for q in m if (q[0], q[1] - 1) not in m]
    for (x, y) in sorted(top):
        if rr.random() < .5:
            c.put(x, y - 1, MOSS[1] if rr.random() < .5 else MOSS[0])
    for _ in range(36):
        q = (rr.randint(3, 29), rr.randint(14, 27))
        if q in m:
            c.put(q[0], q[1], MOSS[0] if rr.random() < .5 else MOSS[3])
    FL = R4('#fffbe0', '#ffe060', '#ffa830', '#d06a1c')
    for (x, y, h) in [(8, 13, 5), (15, 9, 6), (22, 11, 5), (26.5, 17, 4), (12, 18, 3)]:
        # 가는 줄기
        c.fill(LN([(x, y + 1), (x, y + h)], 1.0), H('#3a7a38'))
        fl = LEAF((x, y - 4.2), (x, y + 1.2), 1.9, a=1.4, b=.6, skew=.55)
        c.fill(fl, FL[1])
        c.fill(fl & RC(0, int(y), 32, 32), FL[2])
        c.fill({q for q in fl if abs(q[0] + .5 - x) < 1 and q[1] < y and q[1] > y - 3}, FL[0])
        c.dot(x - 2, y - 4, H('#fff4a0'))
    glow_ring(c, H('#ffe070'), 1.8, 90)
    c.spark(27, 6, H('#fff4a0'), 1, WHITE)


# ======================================================================= 9 부엉이 깃털
@icon2
def owlf(c):
    FL = R4('#f4dcb0', '#d0a470', '#8a5a34', '#5e3a20')
    P0, P1 = (7.5, 29.5), (24.5, 3.5)
    Pv = lerp(P0, P1, .2)
    info = leaf_info(Pv, (26, 2.5), 8.6, a=2.4, b=.5, skew=.12, bend=-.6)
    for q, (t, sn) in info.items():
        band = int(t * 8.0 + sn * 1.1) % 2
        k = (0 if sn < -.2 else 1) if band else (2 if sn < .3 else 3)
        if abs(sn) > .85 and k < 3:
            k += 1
        c.put(q[0], q[1], FL[k])
    m = set(info)
    # 솜털(밑동)
    rr = c.rng
    for q in sorted(m):
        t = info[q][0]
        if t < .15 and rr.random() < .5:
            c.put(q[0], q[1], FL[0])
    # 깃 갈라짐
    ax = (P1[0] - P0[0], P1[1] - P0[1])
    Ln = math.hypot(*ax)
    ux, uy = ax[0] / Ln, ax[1] / Ln
    nx, ny = uy, -ux
    for t, sg in ((.55, 1), (.7, -1)):
        A = lerp(P0, P1, t)
        cut = LN([(A[0] + sg * nx * 4.5, A[1] + sg * ny * 4.5), (A[0] + sg * nx * 9 + ux * 2.2, A[1] + sg * ny * 9 + uy * 2.2)], 1.0)
        c.erase(cut & m)
    c.line(Pv, lerp(P0, P1, .97), H('#f6e6c8'), 1.0)
    c.line(P0, Pv, H('#e8d4b0'), 1.3)
    c.pts([(7, 29), (8, 28)], H('#a88a68'))


# ======================================================================= 10 유자
@icon2
def yuzu(c):
    YZ = R4('#fff69a', '#ffd23c', '#e09a24', '#a8601c')
    m = E(15.5, 18.5, 11.6, 10.4) | E(15.5, 17.2, 10.8, 10.8)
    m -= E(15.5, 7.4, 2.4, 1.6)
    c.shade(m, YZ, 'sphere', box=(15.5, 18, 11.6, 11), th=(.82, .42, .02))
    # 울퉁불퉁 껍질 (작은 혹 + 기공)
    rr = c.rng
    for q in sorted(erode(m, 1)):
        r = rr.random()
        cur = c.p[q]
        k = YZ.index(cur)
        if r < .14 and k < 3:
            c.put(q[0], q[1], YZ[k + 1])
            if (q[0] - 1, q[1] - 1) in m:
                c.put(q[0] - 1, q[1] - 1, YZ[max(0, k - 1)])
    # 혹 모양 가장자리
    for (x, y) in [(5, 14), (6, 23), (25.5, 13), (26, 22), (12, 28.5), (20, 28.5)]:
        b = E(x, y, 2.0, 2.0)
        for q in b - m:
            pass
    # 꼭지와 잎
    c.fill(RC(14, 6, 17, 9), H('#6a7a2a'))
    c.pts([(14, 6), (15, 6)], H('#9ab040'))
    GL = R4('#a8e078', '#4ea444', '#2e7a3c', '#1e5232')
    lf = LEAF((16.5, 6.5), (29, 2.5), 3.6, a=2, b=.62, bend=-1.2)
    c.shade(lf, GL, 'diag')
    c.fill(LN(bez((16.5, 6.5), (22, 3.4), (28, 2.8), 8), .8) & lf, GL[3])
    c.pts([(8, 13), (9, 12), (10, 11), (8, 14)], H('#fffbd8'))


# ======================================================================= 11 설강화
@icon2
def snowdrop(c):
    LF = R4('#b4e48a', '#6cae58', '#447e48', '#2a5638')
    for (p0, p1, bd) in [((13, 31), (6, 13), -1.0), ((15, 31), (25, 16), 1.2)]:
        lf = LEAF(p0, p1, 1.9, a=1.5, b=.8, bend=bd)
        c.shade(lf, LF, 'diag')
    pts = bez3((14, 31), (13.5, 16), (15, 5), (21, 6.5), 24)
    st = LN(pts, 1.4)
    c.bevel(st, R4('#c4ecaa', '#7cbc64', '#4e8c48', '#2c5c38'))
    # 녹색 씨방
    ov = E(21.5, 8.3, 1.8, 1.6)
    c.shade(ov, LF, 'sphere')
    # 꽃잎 3장 (가운데 하나는 앞)
    PW = R4('#ffffff', '#f2f4ff', '#c8cce8', '#9294c4')
    cx, cy = 21.5, 9.5
    petals = [((cx - .5, cy), (14.5, 21), 3.0), ((cx + .5, cy), (27.5, 21.5), 3.0), ((cx, cy), (21.5, 25), 3.6)]
    for p0, p1, w in petals:
        m = LEAF(p0, p1, w, a=2, b=.55, skew=.2, bend=0)
        sep(c, m, PW[3])
        c.shade(m, PW, 'diag', th=(.4, -.2, -.6))
    # 안쪽 녹색 무늬 (가운데 꽃잎 아래 살짝)
    c.pts([(20, 23), (21, 23), (22, 23), (21, 22)], H('#7cbc64'))
    c.pts([(20, 13), (20, 14), (19, 15)], WHITE)
    c.spark(7, 5, H('#e8f0ff'), 1, WHITE)
    c.dot(27, 28, H('#e8f0ff'))


# ======================================================================= 12 안개 버섯
@icon2
def mistcap(c):
    CAPM = R4('#c8d8ee', '#8ea4c8', '#62789e', '#3e4e74')
    STEM = R4('#f4f6ff', '#d8deee', '#a4acc8', '#6c7498')
    LIP = R4('#eef0fa', '#c8cee4', '#949cbc', '#646c90')
    cap, st = mushroom(c, 16, 15.5, 12.0, 10.0, CAPM, STEM, 6.5, 8.5, 29.6, lipc=LIP)
    rr = c.rng
    for q in sorted(cap):
        if rr.random() < .12 and c.p[q] in (CAPM[1], CAPM[2]):
            c.put(q[0], q[1], CAPM[0])
    c.pts([(9, 9), (10, 8), (12, 7), (11, 7)], H('#eef4ff'))
    # 안개 띠 (윤곽선 위에 얹는 반투명 띠)
    MIST = [(232, 238, 255, 200), (210, 220, 245, 150)]
    for (pl, w, w1) in [([(0.5, 26.5), (6, 23.5), (9, 29), (12, 27.5)], 2.4, .6),
                        ([(31.5, 27.5), (26, 24.5), (23, 30), (20, 28.5)], 2.4, .6),
                        ([(31, 9), (28, 5.5), (25, 6), (23, 3.5)], 1.8, .5),
                        ([(1, 13), (3, 9), (6, 8.5), (7, 5.5)], 1.6, .5)]:
        mm = LN(bez3(pl[0], pl[1], pl[2], pl[3], 24), w, w1) - dilate(set(c.p), 1)
        for q in mm:
            if 0 <= q[0] < S and 0 <= q[1] < S:
                c.top[q] = MIST[0] if (q[0] + q[1]) % 3 else MIST[1]
    glow_ring(c, H('#c8d4f0'), 2.4, 110)
    c.dot(4, 6, H('#e4ecff'))


# ======================================================================= 13 꽈리 열매
@icon2
def lanternfruit(c):
    LH = R4('#ffd090', '#ff8a2c', '#d0561c', '#8a3218')
    # 줄기
    st = LN(bez((16, 7), (16, 3), (20, 1), 8), 1.6)
    c.bevel(st, R4('#c8b070', '#8a7a40', '#5e5228', '#3a3218'))
    # 등불 모양 껍질
    def hw(y):
        t = (y - 6.0) / (30.0 - 6.0)
        if t < 0 or t > 1:
            return 0
        return 12.2 * math.sin(math.pi * min(1, t * 1.25) ** .8) * (1 - t) ** .35 if t < .8 else 12.2 * math.sin(math.pi * 1.0 ** .8) * 0 + 12.2 * (1 - t) ** 1.0 * 1.4
    m = set()
    for x, y in FI._pts():
        t = (y + .5 - 6.0) / 24.0
        if 0 <= t <= 1:
            w = 12.0 * (math.sin(math.pi * t ** .75)) ** .8
            if abs(x + .5 - 16) <= w:
                m.add((x, y))
    c.shade(m, LH, 'sphere', box=(15, 16, 12, 12), th=(.78, .35, -.1))
    # 세로 골(맥)
    for dxs in (-7.5, -3.2, 2.5, 7.5):
        pl = []
        for k in range(21):
            t = k / 20
            y = 6.0 + t * 24
            w = (math.sin(math.pi * max(t, .001) ** .75)) ** .8
            pl.append((16 + dxs * w, y))
        c.fill(LN(pl, .9) & erode(m, 1), LH[3] if dxs > 0 else LH[2])
    # 그물(속이 비침) 창: 오른쪽 아래 구멍으로 속 열매가 보임
    win = E(19.5, 20.5, 4.2, 4.6) & erode(m, 1)
    c.fill(win, H('#fff0b0'))
    berry = E(19.5, 21, 3.0, 3.0)
    c.shade(berry, R4('#ffe08a', '#ff9a2a', '#e0601c', '#a03a18'), 'sphere')
    for q in win - berry:
        if (q[0] + q[1]) % 2 == 0:
            c.put(q[0], q[1], LH[1])
    c.pts([(9, 11), (9, 12), (10, 10), (8, 14)], H('#ffeccc'))
    glow_ring(c, H('#ffa850'), 2.4, 110)
    c.dot(4, 5, H('#ffd8a0'))
    c.spark(28, 8, H('#ffe0b0'), 1, WHITE)


# ======================================================================= 14 유령 솔잎
@icon2
def ghostpine(c):
    GP = R4('#f0fff8', '#b4f4dc', '#78d8d0', '#4aa4b8')
    NE = [H('#e0fff0'), H('#a8f0d8'), H('#80dcd8'), H('#64bcd8')]
    br = bez3((4, 29), (10, 22), (17, 14), (27, 4), 30)
    c.fill(LN(br, 1.8), H('#8ab8c8'))
    rr = c.rng
    for i in range(3, 29, 2):
        x, y = br[i]
        for sg in (-1, 1):
            ang = math.radians(-45 + sg * 62 - 10)
            dx, dy = br[min(i + 1, 30)][0] - br[i - 1][0], br[min(i + 1, 30)][1] - br[i - 1][1]
            base = math.atan2(dy, dx)
            a = base + sg * math.radians(48)
            ln = 6.5 - abs(i - 15) * .14
            e = (x + math.cos(a) * ln, y + math.sin(a) * ln)
            col = NE[(i // 2 + (sg > 0)) % 3]
            c.fill(LN([(x, y), e], 1.0), col)
    # 끝 새순
    c.fill(LN([(26, 5), (29, 1.5)], 1.2), NE[0])
    glow_ring(c, H('#8ff0e0'), 2.8, 120)
    c.spark(7, 8, H('#c8fff0'), 1, WHITE)
    c.spark(26, 22, H('#c8f4ff'), 1, WHITE)
    c.dot(15, 3, H('#d8fff4'))
    c.dot(3, 18, H('#d8fff4'))


# ======================================================================= 15 서리 결정
@icon2
def frostcrystal(c):
    C = (16, 16)
    arms = set()
    br = set()
    for k in range(6):
        a = math.radians(k * 60 - 90)
        dx, dy = math.cos(a), math.sin(a)
        arms |= LN([C, (C[0] + dx * 13.5, C[1] + dy * 13.5)], 2.2)
        for (d, ln) in ((6.5, 4.0), (10.0, 2.8)):
            p = (C[0] + dx * d, C[1] + dy * d)
            for sg in (-1, 1):
                b = a + sg * math.radians(55)
                br |= LN([p, (p[0] + math.cos(b) * ln, p[1] + math.sin(b) * ln)], 1.6)
    hexm = PG([(C[0] + 4.6 * math.cos(math.radians(k * 60)), C[1] + 4.6 * math.sin(math.radians(k * 60))) for k in range(6)])
    m = arms | br | hexm
    c.shade(m, ICE, 'diag', th=(.3, -.05, -.45), box=(16, 16, 14, 14))
    for q in m:
        if c.p[q] == ICE[3]:
            c.put(q[0], q[1], ICE[2])
    # 가운데 육각 판
    c.shade(hexm, R4('#ffffff', '#d4f0ff', '#94d0f4', '#5aa0dc'), 'diag', th=(.3, -.1, -.5))
    c.fill(PG([(C[0] + 2.2 * math.cos(math.radians(k * 60)), C[1] + 2.2 * math.sin(math.radians(k * 60))) for k in range(6)]), H('#ffffff'))
    # 팔 가운데 흰 줄
    for k in range(6):
        a = math.radians(k * 60 - 90)
        c.fill(LN([(C[0] + math.cos(a) * 5, C[1] + math.sin(a) * 5), (C[0] + math.cos(a) * 12.5, C[1] + math.sin(a) * 12.5)], .7) & m, WHITE)
    c.spark(27, 4, WHITE, 1, WHITE)
    c.dot(4, 27, H('#c8ecff'))
    c.dot(28, 26, H('#c8ecff'))


# ======================================================================= 16 겨우살이
@icon2
def mistletoe(c):
    GL = R4('#b4e07a', '#68ac48', '#3e7e3e', '#265434')
    RB = R4('#ff8a8a', '#e23a44', '#a81e3a', '#6a1430')
    # 잎 (주걱형, 쌍으로)
    leaves = [((14, 11), (4, 19), 3.0), ((18, 11), (28, 19), 3.0), ((15, 12), (8, 27), 2.9), ((17, 12), (24, 27), 2.9), ((16, 12), (16, 29), 2.6)]
    for p0, p1, w in leaves:
        lf = LEAF(p0, p1, w, a=1.6, b=.6, skew=.35)
        sep(c, lf, GL[3])
        c.shade(lf, GL, 'diag')
        c.fill(LN([lerp(p0, p1, .2), lerp(p0, p1, .8)], .7) & lf, GL[2])
    # 하얀 열매
    BW = R4('#ffffff', '#f2f4ec', '#c8ccc0', '#8e9488')
    for (x, y) in [(13.5, 15.5), (18.5, 15.5), (16, 18.5), (12, 19.5), (20, 19.8)]:
        b = E(x, y, 2.2, 2.2)
        sep(c, b, BW[3])
        c.shade(b, BW, 'sphere')
        c.put(int(x), int(y), BW[2] if False else c.p[(int(x), int(y))])
        c.put(int(x - .8), int(y - .8), WHITE)
    # 빨간 리본
    bow = [LEAF((16, 7.5), (6.5, 3.0), 3.0, a=1.4, b=.6, skew=.5), LEAF((16, 7.5), (25.5, 3.0), 3.0, a=1.4, b=.6, skew=.5)]
    tails = [LEAF((15.5, 8.5), (10.5, 14.5), 1.6, a=2, b=.8), LEAF((16.5, 8.5), (21.5, 14.5), 1.6, a=2, b=.8)]
    for m in tails + bow:
        sep(c, m, RB[3])
        c.shade(m, RB, 'diag', th=(.4, -.1, -.55))
    knot = E(16, 7.6, 2.2, 2.0)
    sep(c, knot, RB[3])
    c.shade(knot, RB, 'sphere')
    c.pts([(9, 3), (10, 3), (22, 3)], H('#ffc8c8'))


# ======================================================================= 17 달빛 나방 날개
@icon2
def moonmoth(c):
    MW = R4('#fffbe0', '#fdeea0', '#e2c870', '#a8904c')
    fr = [(16.8, 15), (17.4, 9.5), (20, 5.5), (25, 3.0), (30.6, 2.5), (29.5, 8), (27.5, 12.5), (23.5, 15.4), (18.5, 16.4)]
    hr = [(16.8, 16.2), (22, 16), (25.5, 18.5), (25, 22.5), (22, 25), (21, 30.6), (19.4, 25.5), (17.2, 21)]

    def mir(p):
        return [(32 - x, y) for x, y in p]
    parts = [PG(hr), PG(mir(hr)), PG(fr), PG(mir(fr))]
    for k, m in enumerate(parts):
        if k >= 2:
            sep(c, m, MW[3])
        c.shade(m, MW, 'diag', th=(.55, -.05, -.5), box=(16, 14, 15, 14))
        for q in m - erode(m, 1):
            if (q[0] - 1, q[1] - 1) in m and (q[0] + 1, q[1] + 1) not in m:
                c.put(q[0], q[1], MW[2])
    # 앞날개 가장자리 띠
    for sgn in (-1, 1):
        c.fill(LN([(16 + sgn * 1.5, 9.5), (16 + sgn * 4, 5.5), (16 + sgn * 9, 3.0), (16 + sgn * 14.6, 2.6)], 1.0) & (parts[2] | parts[3]), H('#c8a0d8'))
    # 은빛 달무늬 (초승달 눈무늬)
    SIL = [H('#ffffff'), H('#d8dcf0'), H('#9aa0c8')]
    for sgn in (-1, 1):
        for (ex, ey, r) in [(8.0, 9.5, 2.6), (5.8, 20.5, 2.0)]:
            x = 16 + sgn * ex
            disc = E(x, ey, r, r)
            c.fill(disc, SIL[1])
            cut = E(x + sgn * r * .55, ey - r * .3, r * .8, r * .8)
            c.fill(disc & cut, MW[1])
            c.fill(ring(disc) & (parts[0] | parts[1] | parts[2] | parts[3]), SIL[2])
            c.put(int(x - sgn * r * .5), int(ey), WHITE)
    # 털 몸통 + 깃털 더듬이
    BD = R4('#ffffff', '#ece6f4', '#b4aac8', '#7a7098')
    body = LEAF((16, 7), (16, 25), 2.6, a=2, b=.6)
    c.shade(body, BD, 'cylv')
    for y in range(10, 24, 3):
        c.put(16, y, BD[2])
    for sgn in (-1, 1):
        c.fill(LN([(16 + sgn * .8, 7), (16 + sgn * 4.5, 1.5)], .9), H('#c8b070'))
        for t in (.35, .6, .85):
            p = lerp((16 + sgn * .8, 7), (16 + sgn * 4.5, 1.5), t)
            c.put(int(p[0] + sgn), int(p[1]), H('#e2c870'))
    glow_ring(c, H('#fff0a0'), 2.4, 110)
    c.spark(3, 13, WHITE, 1, WHITE)
    c.dot(29, 15, H('#fff8d0'))
    c.dot(27, 28, H('#fff8d0'))


# ======================================================================= 18 오로라 조약돌
@icon2
def aurorastone(c):
    m = (E(16, 18, 12.4, 9.2) | E(14.5, 16.8, 10.2, 9.4)) & RC(0, 0, 32, 28)
    base = R4('#4a5aa8', '#34407e', '#262c5e', '#1a1c40')
    c.shade(m, base, 'sphere', box=(16, 17.5, 12.6, 10), th=(.85, .4, -.1))
    bands = [(H('#7cf0b0'), H('#c8ffe0'), 0), (H('#ff8ad0'), H('#ffd0f0'), 1), (H('#a87cff'), H('#dcc8ff'), 2)]
    for k, (col, lt, _) in enumerate(bands):
        off = -5 + k * 4.2
        pl = bez3((3, 19 + off), (11, 11 + off), (18, 25 + off), (30, 15 + off), 30)
        band = LN(pl, 2.4) & erode(m, 1)
        for q in band:
            cur = c.p[q]
            dark = cur in (base[2], base[3])
            c.put(q[0], q[1], lerpc(col, (40, 30, 90), .35) if dark else col)
        core = LN(pl, .8) & erode(m, 1)
        for q in core:
            if c.p[q] == col:
                c.put(q[0], q[1], lt)
    c.pts([(9, 12), (10, 11), (11, 10), (12, 10), (8, 13)], WHITE)
    c.pts([(9, 13), (10, 12)], H('#c8d4ff'))
    glow_ring(c, H('#a8f0d8'), 2.6, 110)
    c.spark(26, 7, H('#ffd0f0'), 1, WHITE)
    c.spark(5, 26, H('#c8ffe0'), 1, WHITE)
    c.dot(28, 27, H('#dcc8ff'))


# ======================================================================= 19 사탕 버섯
@icon2
def candycap(c):
    CP = R4('#ffd0e4', '#ff7aae', '#d44a84', '#8e2a5c')
    CW = R4('#ffffff', '#fff2f6', '#e8c4d4', '#b08aa0')
    STEM = R4('#ffffff', '#fff4ec', '#e4c8c8', '#a88c9c')
    cx, rim = 16, 16.5
    cap, st = mushroom(c, cx, rim, 12.8, 11.0, CP, STEM, 7, 8.5, 29.6, lipc=R4('#fff4f8', '#f4d4e0', '#c8a0b4', '#8a6a84'))
    # 소용돌이 줄무늬 (갓 꼭대기 중심)
    ctr = (14.5, 9.5)
    for q in cap:
        dx, dy = q[0] + .5 - ctr[0], (q[1] + .5 - ctr[1]) * 1.35
        r = math.hypot(dx, dy)
        th = math.atan2(dy, dx)
        ph = (th / (2 * math.pi) * 6 + r * .07) % 1.0
        k = CP.index(c.p[q])
        if ph < .5:
            c.put(q[0], q[1], CW[k])
        elif k == 0:
            c.put(q[0], q[1], CP[1])
    # 사탕 광택
    c.pts([(8, 10), (9, 9), (10, 8), (11, 7), (8, 11)], WHITE)
    c.pts([(9, 10), (10, 9)], WHITE)
    c.spark(27, 4, H('#ffe0f0'), 1, WHITE)
    c.spark(4, 22, H('#ffe0f0'), 1, WHITE)
    c.dot(28, 24, H('#ffd0e8'))
    c.dot(5, 4, H('#ffd0e8'))


# ======================================================================= 20 도깨비불 조각
@icon2
def wisp(c):
    WP = R4('#e8fffa', '#7cf0dc', '#2cc0bc', '#1a7c94')
    # 불꽃: 아래는 둥글고 위로 갈래 3개
    m = E(16, 21, 8.6, 8.0)
    m |= LEAF((16, 22), (16, 2.5), 6.0, a=1.5, b=.7, skew=-.35)
    m |= LEAF((11, 21), (7.5, 7.5), 3.6, a=1.5, b=.7, skew=-.4, bend=.8)
    m |= LEAF((21, 21), (25, 9.0), 3.4, a=1.5, b=.7, skew=-.4, bend=-.8)
    m = smooth(m, 1) | (m & RC(0, 0, 32, 12))
    for q in m:
        x, y = q[0] + .5, q[1] + .5
        d = math.hypot((x - 15.5) / 7.0, (y - 21.5) / 9.5)
        k = 0 if d < .38 else 1 if d < .72 else 2 if d < 1.0 else 3
        c.put(q[0], q[1], WP[k])
    core = E(15.5, 21.5, 3.4, 4.2)
    c.fill(core, H('#ffffff'))
    # 흔들리는 조각
    for (x, y, r) in [(25.5, 4.5, 1.4), (6.5, 3.5, 1.1)]:
        b = E(x, y, r, r)
        c.fill(b, WP[1])
    glow_ring(c, H('#5ce8d8'), 3.0, 120)
    c.spark(28, 18, H('#b4fff0'), 1, WHITE)
    c.dot(3, 15, H('#b4fff0'))
    c.dot(27, 29, H('#b4fff0'))


# ======================================================================= 21 은사시 잎
@icon2
def silverleaf(c):
    SL = R4('#ffffff', '#d8dee8', '#9ea8bc', '#626c86')
    SL2 = R4('#f0f4ff', '#bcc6da', '#8490aa', '#525a78')
    st = LN(bez((16, 30.5), (16, 25), (15, 21), 8), 1.4)
    c.bevel(st, R4('#c8c0a0', '#968a68', '#6a6048', '#423c2c'))
    lv = [((14.5, 21.5), (3.5, 6.5), 6.0, SL2, -1), ((16.5, 21), (28, 4.5), 6.6, SL, 1)]
    for p0, p1, w, ramp, sg in lv:
        m = LEAF(p0, p1, w, a=1.5, b=.55, skew=-.25)
        sep(c, m, ramp[3])
        c.shade(m, ramp, 'diag', th=(.4, -.1, -.55))
        c.fill(LN([p0, lerp(p0, p1, .9)], .9) & m, ramp[2])
        for t in (.3, .5, .7):
            A = lerp(p0, p1, t)
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            for s2 in (-1, 1):
                e = (A[0] + ux * 3 - uy * s2 * 4.5, A[1] + uy * 3 + ux * s2 * 4.5)
                c.fill(LN([A, e], .7) & erode(m, 1), ramp[2])
        # 톱니 가장자리
        for i, q in enumerate(sorted(m - erode(m, 1))):
            if i % 3 == 0:
                c.put(q[0], q[1], ramp[3])
    c.pts([(22, 9), (23, 8), (21, 10)], WHITE)
    c.pts([(7, 9), (8, 10)], WHITE)
    c.spark(24, 13, WHITE, 1, WHITE)
    c.spark(6, 22, H('#e8eeff'), 1, WHITE)
    c.spark(27, 25, H('#e8eeff'), 1, WHITE)
    c.dot(13, 3, WHITE)


# ======================================================================= 22 눈꽃새 깃털
@icon2
def snowfeather(c):
    FW = R4('#ffffff', '#eef4ff', '#c4d2f0', '#8c9cc8')
    P0, P1 = (5, 30), (27.5, 2.0)
    Pv = lerp(P0, P1, .2)
    info = leaf_info(Pv, P1, 6.2, a=2.2, b=.6, skew=-.05, bend=-.8)
    m = set(info)
    for q, (t, sn) in info.items():
        k = 0 if sn < -.35 else 1 if sn < .4 else 2
        c.put(q[0], q[1], FW[k])
    ax = (P1[0] - P0[0], P1[1] - P0[1])
    Ln = math.hypot(*ax)
    ux, uy = ax[0] / Ln, ax[1] / Ln
    nx, ny = uy, -ux
    for k in range(1, 12):
        t = .28 + k * .05
        A = lerp(P0, P1, t)
        for sg, col in ((1, FW[0]), (-1, FW[2])):
            e = (A[0] + sg * nx * 4.5 + ux * 2.5, A[1] + sg * ny * 4.5 + uy * 2.5)
            c.fill(LN([A, e], .7) & erode(m, 1), col)
    for t, sg in ((.5, -1), (.66, 1)):
        A = lerp(P0, P1, t)
        cut = LN([(A[0] + sg * nx * 3.5, A[1] + sg * ny * 3.5), (A[0] + sg * nx * 8 + ux * 2.4, A[1] + sg * ny * 8 + uy * 2.4)], 1.0)
        c.erase(cut & m)
    c.line(Pv, lerp(P0, P1, .96), H('#b8c8ec'), 1.0)
    c.line(P0, Pv, H('#a8b8e0'), 1.3)
    # 끝의 눈꽃 무늬
    sc = lerp(P0, P1, .8)
    SB = H('#6cb4f0')
    for k in range(3):
        a = math.radians(k * 60)
        dx, dy = math.cos(a) * 2.6, math.sin(a) * 2.6
        c.fill(LN([(sc[0] - dx, sc[1] - dy), (sc[0] + dx, sc[1] + dy)], .8) & m, SB)
    c.put(int(sc[0]), int(sc[1]), WHITE)
    c.halo = (H('#cfe8ff'), 2.6, 120)
    c.spark(23, 18, WHITE, 2, WHITE)
    c.spark(7, 9, H('#d8ecff'), 1, WHITE)
    c.spark(28, 26, H('#d8ecff'), 1, WHITE)
    c.dot(15, 3, H('#e8f4ff'))


# ======================================================================= 23 서리 심장
@icon2
def frostheart(c):
    HB = R4('#e4f8ff', '#7cc8ff', '#3a84e8', '#2448a8')
    m = E(10.8, 12.5, 6.4, 6.4) | E(21.2, 12.5, 6.4, 6.4) | PG([(4.8, 14.5), (27.2, 14.5), (16, 28.5)])
    m -= {(15, 6), (16, 6), (15, 7), (16, 7)}
    # 보석 면
    facets = [
        ([(4, 4), (16, 9), (11, 16), (3, 15)], HB[0]),
        ([(16, 9), (28, 4), (29, 15), (21, 16)], HB[1]),
        ([(11, 16), (16, 9), (21, 16), (16, 21)], lerpc(HB[0], HB[1], .5)),
        ([(3, 15), (11, 16), (16, 21), (16, 30)], HB[1]),
        ([(21, 16), (29, 15), (16, 30), (16, 21)], HB[2]),
    ]
    for pts, col in facets:
        c.fill(PG(pts) & m, col)
    for q in m - set(c.p):
        c.put(q[0], q[1], HB[1])
    for q in m:
        if (q[0] + 1, q[1] + 1) not in m and (q[0] + 1, q[1]) not in m or ((q[0], q[1] + 1) not in m and q[0] >= 16):
            c.put(q[0], q[1], HB[3])
    for (a, b) in [((11, 16), (16, 21)), ((16, 21), (21, 16)), ((16, 9), (11, 16)), ((16, 9), (21, 16))]:
        c.fill(LN([a, b], .7) & erode(m, 1), H('#ffffff') if a[0] < 16 or b[0] < 16 and a[1] < b[1] else H('#a8dcff'))
    # 얼음 금
    c.fill(LN([(22, 19), (19.5, 22), (20.5, 24)], .7) & erode(m, 1), H('#c8ecff'))
    c.pts([(7, 9), (8, 8), (9, 8), (7, 10)], WHITE)
    c.halo = (H('#7cd0ff'), 3.0, 120)
    c.spark(27, 4, WHITE, 2, WHITE)
    c.spark(4, 24, H('#c8ecff'), 1, WHITE)
    c.spark(27, 25, H('#c8ecff'), 1, WHITE)
    c.dot(16, 2, H('#e4f8ff'))


# ======================================================================= 24 별초
@icon2
def starcandle(c):
    GS = R4('#d8f4a8', '#94cc68', '#5e9a4c', '#3a6a3c')
    WX = R4('#fffbe8', '#f4e8c0', '#d0bc8c', '#9a8460')
    # 풀잎
    for (p0, p1, w, bd) in [((14, 31), (5, 18), 1.6, 1.0), ((18, 31), (27, 19), 1.6, -1.0), ((15, 31), (9.5, 22), 1.3, .5)]:
        lf = LEAF(p0, p1, w, a=1.6, b=.8, bend=bd)
        c.shade(lf, GS, 'diag')
    # 가는 초 모양 줄기 (두 개)
    for (x, y0, y1, w) in [(16, 11, 30.5, 3.0), (22.5, 18, 30.5, 2.2)]:
        stem = RC(x - w / 2, y0, x + w / 2 + .01, y1)
        stem = {q for q in LN([(x, y0), (x, y1)], w)}
        c.shade(stem, WX, 'cylv', th=(.6, .1, -.4))
        # 녹은 촛농 방울
        c.put(int(x - w / 2 + .5), y0 + 1, WX[0])
        # 심지
        c.fill(LN([(x, y0 - 1.5), (x, y0)], .9), H('#4a3a2a'))
    # 별빛 불꽃
    for (x, y, r0, r1) in [(16, 5.5, 5.4, 2.3), (22.5, 13.5, 3.4, 1.5)]:
        stm = star(x, y, r0, r1)
        c.fill(stm, H('#ffe060'))
        c.fill(star(x, y, r0 * .55, r1 * .6), H('#fff8c0'))
        c.put(int(x), int(y), WHITE)
        for q in stm:
            if (q[0] + 1, q[1] + 1) not in stm and (q[0] + 1, q[1]) not in stm:
                c.put(q[0], q[1], H('#f0a830'))
    c.halo = (H('#ffe070'), 2.8, 120)
    c.spark(6, 6, H('#fff4a0'), 2, WHITE)
    c.spark(27, 4, H('#fff4a0'), 1, WHITE)
    c.dot(4, 14, H('#ffe890'))
    c.dot(28, 23, H('#ffe890'))


# ======================================================================= 출력
def build_new():
    assert len(ICONS2) == N2, len(ICONS2)
    strip = Image.new('RGBA', (S * N2, S), (0, 0, 0, 0))
    for i, f in enumerate(ICONS2):
        c = Cv(BASE + i)
        f(c)
        strip.paste(c.render(), (i * S, 0))
    return strip


def names():
    try:
        return [r[1] for r in json.load(open(SPEC, encoding='utf-8'))['forage']]
    except Exception:
        return [''] * N2


def kfont(size):
    cands = []
    try:
        import subprocess
        out = subprocess.run(['fc-list', ':lang=ko', 'file'], capture_output=True, text=True, timeout=20).stdout
        cands += [l.split(':')[0].strip() for l in out.splitlines() if l.strip()]
    except Exception:
        pass
    cands += ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
              '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf']
    cands.sort(key=lambda p: (0 if 'CJK' in p or 'Nanum' in p else 1 if 'wqy' in p else 2))
    for f in cands:
        try:
            ft = ImageFont.truetype(f, size)
            if ft.getmask('가').getbbox() and ft.getmask('가').size != ft.getmask('￿').size or True:
                if ft.getbbox('가') != ft.getbbox('\U000F0000'):
                    return ft
        except Exception:
            pass
    return None


def preview(strip, outdir, extra=None):
    os.makedirs(outdir, exist_ok=True)
    strip.save(os.path.join(outdir, 'forage_new25.png'))
    bgc = (0x21, 0x17, 0x33, 255)
    Z, per, pad = 4, 5, 8
    cell = S * Z
    font = kfont(16)
    lh = 24 if font else 0
    rows = (N2 + per - 1) // per
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), bgc)
    d = ImageDraw.Draw(img)
    nm = names()
    for i in range(N2):
        x0 = pad + (i % per) * (cell + pad)
        y0 = pad + (i // per) * (cell + lh + pad)
        t = strip.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST)
        img.alpha_composite(t, (x0, y0))
        if font:
            label = '%d %s' % (BASE + i, nm[i])
            w = d.textlength(label, font=font)
            d.text((x0 + (cell - w) / 2, y0 + cell + 3), label, fill=(225, 215, 245, 255), font=font)
    img.save(os.path.join(outdir, 'forage_new25_x4_lbl.png'))
    if not font:
        print('(Korean font not found: labels skipped)')


def apply(strip):
    old = Image.open(SHEET).convert('RGBA')
    assert old.size[1] == S and old.size[0] >= S * BASE, old.size
    out = Image.new('RGBA', (S * (BASE + N2), S), (0, 0, 0, 0))
    out.paste(old.crop((0, 0, S * BASE, S)), (0, 0))
    out.paste(strip, (S * BASE, 0))
    out.save(SHEET)
    print('saved', SHEET, out.size)


if __name__ == '__main__':
    strip = build_new()
    if '--preview' in sys.argv:
        d = sys.argv[sys.argv.index('--preview') + 1]
        preview(strip, d)
        print('preview ->', d)
    if '--apply' in sys.argv:
        apply(strip)
    if '--preview' not in sys.argv and '--apply' not in sys.argv:
        print(__doc__ or 'usage: --preview DIR | --apply')
