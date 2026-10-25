# 채집물 50종 아이콘 (32x32, 직접 그림) -> public/art/forage.png (1600x32, 칸 i = x 32*i)
# 순서는 index.html 의 FORAGE_LIST 순서(idx 0..49).
#   python3 tools/iso/forage_icons.py                 # 시트 생성
#   python3 tools/iso/forage_icons.py --preview DIR   # 시트 + 4배 확대 미리보기(DIR/forage_prev.png, forage_prev_lbl.png)
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.environ.get('FORAGE_OUT') or os.path.join(ROOT, 'public', 'art', 'forage.png')
S = 32
N = 50
NAMES = ['도토리', '솔방울', '세잎클로버', '동글 조약돌', '들꽃', '고사리', '촉촉 이끼', '빨간 단풍잎', '노란 은행잎', '까마귀 깃털',
         '산딸기', '블루베리', '알밤', '호두', '개박하', '호박씨', '해바라기씨', '달팽이 껍질', '무당벌레', '빗자루 짚',
         '빨간 독버섯', '송이버섯', '은방울꽃', '매미 허물', '반딧불이', '박쥐 날개 잎', '달맞이꽃', '거미 버섯', '들장미 열매', '꽃사과',
         '독사과', '나비 날개', '사슴벌레', '거미 알', '유령 꽃', '해골 꽃', '달빛 버섯', '무지개 이끼', '반짝 돌', '호박석',
         '자수정', '조개 화석', '월장석', '별가루 병', '요정 날개 가루', '늑대 털 뭉치', '별똥별 조각', '황금 도토리', '유니콘 털', '호박달 씨앗']


def H(s):
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


OL = H('#1a1024')          # 겉 윤곽선
WHITE = H('#ffffff')


def R4(a, b, c, d):        # 램프: 밝음, 기본, 어두움, 가장 어두움
    return (H(a), H(b), H(c), H(d))


# ---------------------------------------------------------------- 마스크(좌표 집합) 도형
def _pts():
    for y in range(S):
        for x in range(S):
            yield x, y


def E(cx, cy, rx, ry):
    return {(x, y) for x, y in _pts() if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}


def RE(cx, cy, rx, ry, ang):
    """회전 타원 (ang: 도, 시계방향)"""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    m = set()
    for x, y in _pts():
        dx, dy = x + .5 - cx, y + .5 - cy
        u = dx * ca + dy * sa
        v = -dx * sa + dy * ca
        if (u / rx) ** 2 + (v / ry) ** 2 <= 1:
            m.add((x, y))
    return m


def RC(x0, y0, x1, y1):
    return {(x, y) for x in range(int(x0), int(x1)) for y in range(int(y0), int(y1)) if 0 <= x < S and 0 <= y < S}


def PG(pts):
    """다각형 (짝홀 규칙, 픽셀 중심 기준)"""
    m = set()
    n = len(pts)
    for x, y in _pts():
        px, py = x + .5, y + .5
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = pts[i]
            xj, yj = pts[j]
            if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi + 1e-12) + xi:
                inside = not inside
            j = i
        if inside:
            m.add((x, y))
    return m


def _segd(px, py, x0, y0, x1, y1):
    vx, vy = x1 - x0, y1 - y0
    l2 = vx * vx + vy * vy
    t = 0 if l2 == 0 else max(0, min(1, ((px - x0) * vx + (py - y0) * vy) / l2))
    qx, qy = x0 + t * vx, y0 + t * vy
    return math.hypot(px - qx, py - qy), t


def LN(pts, w=1.0, w1=None):
    """굵은 폴리라인. w1 이 있으면 처음 w → 끝 w1 으로 가늘어짐"""
    if w1 is None:
        w1 = w
    segs = list(zip(pts[:-1], pts[1:]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens) or 1
    m = set()
    for x, y in _pts():
        px, py = x + .5, y + .5
        acc = 0
        for (a, b), l in zip(segs, lens):
            d, t = _segd(px, py, a[0], a[1], b[0], b[1])
            ww = w + (w1 - w) * (acc + t * l) / tot
            if d <= ww / 2:
                m.add((x, y))
                break
            acc += l
    return m


def bez(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def bez3(p0, p1, p2, p3, n=20):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def LEAF(p0, p1, w, a=2.0, b=0.7, skew=0.0, bend=0.0):
    """p0→p1 축을 따라 폭 w 인 잎/씨앗 모양. a,b: 끝 뾰족함, skew>0 이면 p1쪽이 더 넓음, bend: 휘어짐(px)"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    m = set()
    for x, y in _pts():
        qx, qy = x + .5 - p0[0], y + .5 - p0[1]
        t = (qx * ux + qy * uy) / L
        if t < 0 or t > 1:
            continue
        s = -qx * uy + qy * ux - bend * math.sin(math.pi * t)
        u = 2 * t - 1
        hw = w * (max(0.0, 1 - abs(u) ** a)) ** b * (1 + skew * u)
        if abs(s) <= hw:
            m.add((x, y))
    return m


def HEART(tip, ang, length, r, a=None):
    """tip 에서 ang(도) 방향으로 뻗은 하트(끝이 오목). 클로버/꽃잎용"""
    if a is None:
        a = 0.8 * r
    t = math.radians(ang)
    dx, dy = math.cos(t), math.sin(t)

    def G(u, v):
        return (tip[0] + u * dx - v * dy, tip[1] + u * dy + v * dx)
    u0 = length - r
    m = set()
    for v in (-a, a):
        c = G(u0, v)
        m |= E(c[0], c[1], r, r)
    m |= PG([G(0, 0), G(u0, -(a + r * .75)), G(u0, a + r * .75)])
    return m


def ring(mask):
    """mask 바깥 4방향 이웃"""
    out = set()
    for x, y in mask:
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + d[0], y + d[1])
            if q not in mask:
                out.add(q)
    return out


def erode(mask, n=1):
    m = set(mask)
    for _ in range(n):
        m = {(x, y) for x, y in m if all((x + dx, y + dy) in m for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    return m


def rot(pts, ang, c=(16, 16)):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def shift(m, dx, dy):
    return {(x + dx, y + dy) for x, y in m}


# ---------------------------------------------------------------- 캔버스
class Cv:
    def __init__(s, idx=0):
        s.p = {}          # (x,y) -> rgba  (윤곽선 전)
        s.top = {}        # 윤곽선 후에 덮는 것(반짝이/광채)
        s.halo = None     # (색, 반경, 알파)
        s.rng = random.Random(idx * 7919 + 13)
        s.noline = set()  # 윤곽선을 그리지 않을 칸(바깥 윤곽 제외 대상)

    # --- 기본
    def put(s, x, y, col):
        x, y = int(x), int(y)
        if 0 <= x < S and 0 <= y < S:
            s.p[(x, y)] = col

    def pts(s, pl, col):
        for x, y in pl:
            s.put(x, y, col)

    def fill(s, m, col):
        for x, y in m:
            s.p[(x, y)] = col

    def line(s, a, b, col, w=1.0):
        s.fill(LN([a, b], w), col)

    def poly(s, pts, col, w=1.0):
        s.fill(LN(pts, w), col)

    def move(s, dx, dy):
        s.p = {(x + dx, y + dy): v for (x, y), v in s.p.items() if 0 <= x + dx < S and 0 <= y + dy < S}
        s.top = {(x + dx, y + dy): v for (x, y), v in s.top.items() if 0 <= x + dx < S and 0 <= y + dy < S}

    def erase(s, m):
        for q in m:
            s.p.pop(q, None)

    # --- 음영
    def shade(s, m, ramp, mode='sphere', th=None, box=None, light=(-.5, -.6, .62)):
        if not m:
            return
        xs = [x for x, y in m]
        ys = [y for x, y in m]
        if box is None:
            cx, cy = (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2
            rx, ry = (max(xs) - min(xs) + 1) / 2, (max(ys) - min(ys) + 1) / 2
        else:
            cx, cy, rx, ry = box
        ln = math.sqrt(sum(v * v for v in light))
        lx, ly, lz = (v / ln for v in light)
        if th is None:
            th = (.86, .5, .15) if mode in ('sphere', 'cylv', 'cylh') else (.55, -.1, -.55)
        for (x, y) in m:
            nx, ny = (x + .5 - cx) / max(rx, .5), (y + .5 - cy) / max(ry, .5)
            if mode == 'sphere':
                nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                d = nx * lx + ny * ly + nz * lz
            elif mode == 'cylv':     # 세로 원통
                nz = math.sqrt(max(0.0, 1 - nx * nx))
                d = nx * lx + nz * lz
            elif mode == 'cylh':     # 가로 원통
                nz = math.sqrt(max(0.0, 1 - ny * ny))
                d = ny * ly + nz * lz
            else:                    # diag: 왼쪽 위가 밝음
                d = -(nx + ny) / 2
            k = 0 if d >= th[0] else 1 if d >= th[1] else 2 if d >= th[2] else 3
            s.p[(x, y)] = ramp[k]

    def bevel(s, m, ramp):
        for (x, y) in m:
            tl = (x - 1, y) not in m or (x, y - 1) not in m
            br = (x + 1, y) not in m or (x, y + 1) not in m
            s.p[(x, y)] = ramp[0] if (tl and not br) else ramp[2] if (br and not tl) else ramp[1]

    def art(s, rows, pal, ox=0, oy=0):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.' and ch != ' ':
                    s.put(ox + i, oy + j, pal[ch])

    def spark(s, x, y, col=WHITE, size=1, core=None):
        """윤곽선 후에 올리는 별 모양 반짝이"""
        x, y = int(x), int(y)
        core = core or col
        s.top[(x, y)] = core
        for k in range(1, size + 1):
            for d in ((k, 0), (-k, 0), (0, k), (0, -k)):
                s.top[(x + d[0], y + d[1])] = col

    def dot(s, x, y, col):
        s.top[(int(x), int(y))] = col

    # --- 마무리
    def render(s):
        img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        px = img.load()
        body = set(s.p)
        edge = ring(body)
        if s.halo:
            col, r, a = s.halo
            near = body | edge
            for x, y in _pts():
                if (x, y) in near:
                    continue
                d = min((math.hypot(x - bx, y - by) for bx, by in edge if abs(x - bx) <= r + 1 and abs(y - by) <= r + 1),
                        default=99)
                if d <= r:
                    if d <= 1.6:
                        ok = (x + y) % 2 == 0
                    else:
                        ok = x % 2 == 0 and y % 2 == 0
                    if ok:
                        px[x, y] = (col[0], col[1], col[2], a)
        for q, c in s.p.items():
            px[q] = c
        for (x, y) in edge:
            if 0 <= x < S and 0 <= y < S:
                px[x, y] = OL
        for q, c in s.top.items():
            if 0 <= q[0] < S and 0 <= q[1] < S:
                px[q] = c
        return img


ICONS = {}


def icon(i):
    def deco(f):
        ICONS[i] = f
        return f
    return deco


def build():
    sheet = Image.new('RGBA', (S * N, S), (0, 0, 0, 0))
    for i in range(N):
        if i in ICONS:
            c = Cv(i)
            ICONS[i](c)
            sheet.paste(c.render(), (i * S, 0))
    return sheet


# ======================================================================= 아이콘들
# ---------------------------------------------------------------- 공용 팔레트/보조
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def lerpc(c1, c2, t):
    return tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)) + (255,)


BROWN = R4('#e2a860', '#b97a34', '#8a5224', '#5c3419')
CAPB = R4('#b8855a', '#8a5c36', '#63401f', '#3f2814')
GOLD = R4('#fff0a0', '#ffd23a', '#d9981c', '#9a5e18')
GOLDCAP = R4('#f2c04a', '#d49a28', '#a8701c', '#6e4616')
GREEN = R4('#9ae070', '#5cb046', '#3a8240', '#25593a')
GREEN2 = R4('#b4e86a', '#74c04a', '#4a9040', '#2e6238')
RED = R4('#ff8a62', '#e43c34', '#a8223c', '#701838')
GREY = R4('#d6d2e6', '#a8a2c0', '#7a7498', '#4e486e')
YEL = R4('#fff59a', '#ffd94a', '#e8a82a', '#b86e1c')
CREAM = R4('#fff8e0', '#f0e0b8', '#c8b080', '#8c7650')
WOOD = R4('#c8935a', '#9a6a3a', '#6e4824', '#46301a')
PURP = R4('#d8a8ff', '#a068e8', '#6a38b0', '#44247a')
BLUE = R4('#bfe8ff', '#6cb4f0', '#3c78c8', '#26489a')
HI = H('#fff6dc')


# ---------------------------------------------------------------- 0 도토리 / 47 황금 도토리
def acorn(c, nut, cap, stem, hi, gold=False):
    body = LEAF((16, 9), (16, 29.6), 7.9, a=2.0, b=0.55, skew=-0.28)
    c.shade(body, nut, 'sphere', box=(15, 19, 8, 10))
    capm = (E(16, 16.5, 9.6, 9.6) & RC(0, 0, 32, 17)) | E(16, 16.6, 9.6, 1.9)
    c.shade(capm, cap, 'sphere', box=(15, 15, 10, 10))
    # 모자 비늘 무늬
    for (x, y) in capm:
        if y < 16 and ((x + (y // 2 % 2) * 2) % 4 == 0 and y % 2 == 0) and c.p[(x, y)] in (cap[1], cap[2]):
            c.put(x, y, cap[3] if c.p[(x, y)] == cap[2] else cap[2])
    # 모자 아랫단 그림자
    for (x, y) in capm:
        if y >= 17 or (y == 16 and (x + 1, y + 1) not in capm):
            c.put(x, y, cap[3])
    c.fill(RC(15, 3, 18, 8) - {(17, 7), (17, 6)}, stem[1])
    c.pts([(15, 3), (16, 3), (15, 4), (15, 5)], stem[0])
    c.pts([(17, 5), (17, 6), (16, 7)], stem[2])
    c.pts([(11, 20), (11, 21), (12, 19), (11, 22)], hi)
    c.pts([(12, 9), (13, 8), (11, 10)], cap[0])
    if gold:
        c.pts([(12, 9), (13, 8), (11, 10), (14, 8), (12, 10)], hi)
        c.pts([(11, 20), (11, 21), (12, 19), (11, 22), (12, 20)], WHITE)


@icon(0)
def _(c):
    acorn(c, BROWN, CAPB, R4('#b8855a', '#8a5c36', '#63401f', '#3f2814'), HI)


# ---------------------------------------------------------------- 1 솔방울
@icon(1)
def _(c):
    CONE = R4('#ecc080', '#b8804a', '#7e4c2a', '#3e2418')
    cx = 16
    y0, y1 = 5.0, 30.2

    def hw(y):
        t = (y - y0) / (y1 - y0)
        if t < 0 or t > 1:
            return 0
        return 8.8 * math.sqrt(max(0, 1 - ((t - 0.40) / 0.60) ** 2))
    body = {(x, y) for x, y in _pts() if abs(x + .5 - cx) <= hw(y + .5)}
    c.fill(body, CONE[3])
    rows = []
    y = 6.2
    while y < 29.5:
        rows.append(y)
        y += 3.15
    for r in reversed(range(len(rows))):
        y = rows[r]
        w = hw(y + 1.5)
        n = max(1, int(round(w * 2 / 4.6)))
        sp = 2 * w / max(n, 1)
        xs = [cx + (k - (n - 1) / 2) * sp + ((r % 2) - .5) * sp * 0.55 for k in range(n + 1)] if r % 2 else \
             [cx + (k - (n - 1) / 2) * sp for k in range(n)]
        for x in xs:
            if abs(x - cx) > w + 1.0:
                continue
            sw = min(3.1, max(2.2, sp * .62))
            sc = PG([(x - sw, y - 1.9), (x + sw, y - 1.9), (x + sw + .2, y + .6), (x, y + 3.5), (x - sw - .2, y + .6)])
            tone = 0 if r < 2 else 0
            for (px, py) in sc:
                c.put(px, py, CONE[1])
            for (px, py) in sc:
                tl = (px - 1, py) not in sc or (px, py - 1) not in sc
                bot = (px, py + 1) not in sc or (px + 1, py + 1) not in sc and (px + 1, py) not in sc
                if bot:
                    c.put(px, py, CONE[2])
                    q = (px, py + 1)
                    if q in c.p and q not in sc:
                        c.put(px, py + 1, CONE[3])
                elif tl and px <= x + 1:
                    c.put(px, py, CONE[0])
                elif px >= x + sw - 1.2:
                    c.put(px, py, CONE[2])
    c.fill(RC(14, 1, 18, 6), CONE[2])
    c.pts([(14, 1), (15, 1), (14, 2), (14, 3)], CONE[0])
    c.pts([(17, 3), (17, 4), (16, 5)], CONE[3])


# ---------------------------------------------------------------- 2 세잎클로버
@icon(2)
def _(c):
    C = (16, 19)
    # 줄기
    st = LN(bez((16, 19), (17, 25), (14.5, 29.6), 12), 1.6)
    c.bevel(st, R4('#8fd070', '#4e9a48', '#2f6c3c', '#25593a'))
    leaves = [(-90, 12.6, 4.2), (152, 12.6, 4.2), (28, 12.6, 4.2)]
    order = [(150), (30), (-90)]
    ms = {}
    for ang, ln, r in leaves:
        ms[ang] = HEART(C, ang, ln, r, a=3.5)
    for ang in (152, 28, -90):
        m = ms[ang]
        c.shade(m, GREEN, 'diag', th=(.5, -.1, -.6))
        # 중앙 맥 + 연한 V 무늬
        t = math.radians(ang)
        dx, dy = math.cos(t), math.sin(t)
        c.fill(LN([(C[0] + dx * 1.5, C[1] + dy * 1.5), (C[0] + dx * 9.0, C[1] + dy * 9.0)], 1.0) & m, GREEN[3])
        mid = (C[0] + dx * 6.2, C[1] + dy * 6.2)
        for sgn in (-1, 1):
            e = (mid[0] + dx * 1.5 - sgn * dy * 3.0, mid[1] + dy * 1.5 + sgn * dx * 3.0)
            s0 = (mid[0] - dx * 0.5, mid[1] - dy * 0.5)
            c.fill(LN([s0, e], 0.9) & m, GREEN[0])


# ---------------------------------------------------------------- 3 동글 조약돌
@icon(3)
def _(c):
    m = (E(16, 18.5, 11.2, 8.4) | E(14, 17, 9.2, 8.8)) & RC(0, 0, 32, 27)
    c.shade(m, GREY, 'sphere', box=(16, 17.5, 12, 10), th=(.85, .45, .0))
    # 하얀 줄무늬 결
    band = LN(bez((7, 22), (14, 15), (25, 19), 14), 1.2)
    for q in band & m:
        c.put(q[0], q[1], GREY[0] if c.p[q] != GREY[3] else GREY[1])
    # 잔 점
    rr = c.rng
    for _ in range(9):
        q = (rr.randint(7, 25), rr.randint(12, 25))
        if q in m and c.p[q] in (GREY[1], GREY[2]):
            c.put(q[0], q[1], GREY[3] if rr.random() < .6 else GREY[0])
    c.pts([(10, 14), (11, 13), (12, 12), (13, 12), (9, 15)], WHITE)
    c.pts([(10, 15), (11, 14)], GREY[0])


# ---------------------------------------------------------------- 4 들꽃(데이지)
@icon(4)
def _(c):
    # 줄기와 잎
    st = LN(bez((16, 19), (15.5, 25), (16.5, 30), 12), 1.7)
    c.bevel(st, GREEN2)
    lf1 = LEAF((16, 27), (7, 21), 2.6, a=2, b=.7)
    lf2 = LEAF((16.5, 25), (25, 20), 2.4, a=2, b=.7)
    for lf in (lf1, lf2):
        c.shade(lf, GREEN, 'diag')
    c.line((15.5, 26.5), (8.5, 22), GREEN[3], 1)
    c.line((17, 24.8), (24, 21), GREEN[3], 1)
    cx, cy = 16, 11
    PET = R4('#ffffff', '#f4efff', '#cdbfe8', '#9a8cc4')
    for k in range(10):
        a = math.radians(k * 36 - 90)
        d = (math.cos(a), math.sin(a))
        m = LEAF((cx + d[0] * 2.5, cy + d[1] * 2.5), (cx + d[0] * 10, cy + d[1] * 10), 2.5, a=2, b=.55)
        c.shade(m, PET, 'diag', th=(.4, -.2, -.6))
        tip = (cx + d[0] * 9.5, cy + d[1] * 9.5)
    ce = E(cx, cy, 3.6, 3.6)
    c.shade(ce, R4('#fff08a', '#ffd23a', '#e29a1c', '#a8621a'), 'sphere')
    c.pts([(14, 9), (13, 10), (15, 8)], H('#fffbd0'))
    for q in [(17, 11), (15, 13), (18, 13), (16, 11)]:
        c.put(q[0], q[1], H('#c0701c'))


# ---------------------------------------------------------------- 5 고사리
@icon(5)
def _(c):
    Cc = (14.0, 12.0)
    pts = bez((21.5, 30.0), (22.5, 24), (21.0, 17.6), 14)
    turns = 1.5
    n = 60
    for i in range(1, n + 1):
        f = i / n
        ph = f * turns * 360
        th = math.radians(34 - ph)
        r = 8.8 - (8.8 - 2.2) * (f ** 0.85)
        pts.append((Cc[0] + r * math.cos(th), Cc[1] + r * math.sin(th)))
    m = LN(pts, 5.6, 2.8)
    c.bevel(m, GREEN2)
    for q in list(m):
        x, y = q
        if c.p[q] == GREEN2[1] and (x - 2, y - 2) not in m:
            c.put(x, y, GREEN2[0])
    rr = c.rng
    for _ in range(30):
        q = (rr.randint(4, 28), rr.randint(2, 30))
        if q in m and c.p[q] in (GREEN2[1], GREEN2[2]):
            c.put(q[0], q[1], H('#c49a58') if rr.random() < .6 else H('#e0c080'))
    # 아래 줄기 갈색 솜털 띠
    for y in range(24, 30):
        for x in range(18, 25):
            if (x, y) in m and (x + y) % 3 == 0 and c.p[(x, y)] == GREEN2[1]:
                c.put(x, y, H('#d0a860'))
    c.move(0, -1)


# ---------------------------------------------------------------- 6 촉촉 이끼
def moss_mound(c, ramp, seed_hi):
    lumps = [(8.5, 21.5, 5.6), (14, 18.5, 6.8), (21.5, 19.5, 6.6), (26, 23.5, 4.6), (5, 25, 3.6), (17, 23, 6.5)]
    m = set()
    for (x, y, r) in lumps:
        m |= E(x, y, r, r * .92)
    m &= RC(0, 0, 32, 28)
    c.shade(m, ramp, 'sphere', box=(16, 21, 14, 8.5), th=(.82, .45, .08))
    return m


@icon(6)
def _(c):
    MOSS = R4('#b2e868', '#6cb83c', '#43873a', '#2a5a34')
    m = moss_mound(c, MOSS, None)
    rr = c.rng
    top = [q for q in m if (q[0], q[1] - 1) not in m]
    # 솜털 풀잎
    for (x, y) in top:
        if rr.random() < .55:
            c.put(x, y - 1, MOSS[1] if rr.random() < .5 else MOSS[0])
            if rr.random() < .3:
                c.put(x, y - 2, MOSS[0])
    for _ in range(40):
        q = (rr.randint(3, 29), rr.randint(14, 27))
        if q in m:
            c.put(q[0], q[1], MOSS[0] if rr.random() < .5 else MOSS[3])
    DR = {'b': H('#8fe0ff'), 'h': H('#f4feff'), 'd': H('#4aa8e0')}
    drop = ['.b.', 'bhb', 'bbd', '.d.']
    for (x, y) in [(10, 16), (20, 21), (24, 15), (14, 24)]:
        for yy in range(4):
            pass
        c.art(drop, DR, x, y)


# ---------------------------------------------------------------- 7 빨간 단풍잎
@icon(7)
def _(c):
    right = [(16, 3.5), (17.6, 8), (20.2, 6.2), (20.2, 11.6), (25.5, 9.4), (24, 15.2), (29.2, 16.6), (23.6, 20.4), (24.4, 23.4),
             (18.2, 22), (16.8, 25)]
    pts = right + [(32 - x, y) for x, y in reversed(right[1:])]
    m = PG(pts)
    c.shade(m, RED, 'diag', th=(.45, -.05, -.55))
    # 잎맥
    for (tx, ty) in [(16, 5.5), (8.2, 10.4), (23.8, 10.4), (4.8, 16.6), (27.2, 16.6), (9, 22), (23, 22)]:
        c.fill(LN([(16, 24), (tx, ty)], 0.9) & m, RED[3])
    # 밝은 가장자리
    for q in m:
        if (q[0] - 1, q[1] - 1) not in m and c.p[q] != RED[3]:
            c.put(q[0], q[1], RED[0])
    st = LN([(16, 24), (16.5, 30)], 1.7)
    c.bevel(st, R4('#c8503c', '#9a2c3c', '#701838', '#4a1230'))
    c.pts([(12, 9), (11, 10), (7, 13), (6, 14)], H('#ffc8a0'))


# ---------------------------------------------------------------- 8 노란 은행잎
@icon(8)
def _(c):
    ox, oy = 16, 25
    m = set()
    vein = set()
    for x, y in _pts():
        dx, dy = (x + .5 - ox) * 1.1, y + .5 - oy
        r = math.hypot(dx, dy)
        if r < 1:
            continue
        ang = math.degrees(math.atan2(dx, -dy))
        aa = abs(ang)
        R = 19.0 - 3.0 * (aa / 80) ** 2 - 0.8 * math.cos(math.radians(aa * 9))
        maxang = min(80, 26 + (r - 3) * 9)
        if aa > maxang or r > R or r < 2.5:
            continue
        if aa < 40 and r > 15 and abs(dx) <= (r - 15) * 0.2 + 0.05:
            continue
        m.add((x, y))
        k = round(ang / 8.0)
        if r > 5 and abs(r * math.sin(math.radians(ang - k * 8))) <= 0.5:
            vein.add((x, y))
    c.shade(m, YEL, 'diag', th=(.5, -.1, -.55), box=(16, 17, 14, 12))
    for q in vein:
        if c.p[q] != YEL[0]:
            c.put(q[0], q[1], YEL[2] if c.p[q] != YEL[2] else YEL[3])
    for q in m:
        if q[1] <= 21 and (q[0], q[1] - 1) not in m:
            pass
    st = LN([(16, 24), (16.5, 30.5)], 2.0)
    c.bevel(st, R4('#c8c060', '#a89440', '#7a6a30', '#56481e'))
    c.pts([(8, 15), (9, 14), (10, 13), (7, 17)], H('#fffbd0'))
    c.move(0, -1)


# ---------------------------------------------------------------- 9 까마귀 깃털
@icon(9)
def _(c):
    P0, P1 = (5.5, 29), (26.5, 3.2)
    Pv = lerp(P0, P1, .26)
    ax = (P1[0] - P0[0], P1[1] - P0[1])
    Ln = math.hypot(*ax)
    ux, uy = ax[0] / Ln, ax[1] / Ln
    nx, ny = -uy, ux   # 왼쪽(위쪽) 법선 (y아래 좌표에서 위쪽-왼쪽)
    nx, ny = uy, -ux
    if nx > 0:
        nx, ny = -nx, -ny
    vane = LEAF(Pv, P1, 7.2, a=1.9, b=.75, skew=-0.1, bend=-0.8)
    FL = R4('#8886c0', '#4c4a7c', '#35305e', '#26224a')
    for q in vane:
        s = (q[0] + .5 - P0[0]) * nx + (q[1] + .5 - P0[1]) * ny
        c.put(q[0], q[1], FL[1] if s > 0.5 else FL[2])
    # 깃가지 결
    for k in range(1, 15):
        t = 0.30 + k * 0.05
        A = lerp(P0, P1, t)
        for sgn, col in ((1, FL[0]), (-1, FL[3])):
            e = (A[0] + sgn * nx * 5.2 + ux * 3.0, A[1] + sgn * ny * 5.2 + uy * 3.0)
            c.fill(LN([A, e], .8) & vane, col)
    # 깃 갈라짐(홈)
    for t in (.52, .72):
        A = lerp(P0, P1, t)
        cut = LN([(A[0] - nx * 2, A[1] - ny * 2), (A[0] - nx * 7 + ux * 2.5, A[1] - ny * 7 + uy * 2.5)], 1.0)
        c.erase(cut & vane)
    # 가운데 대와 깃촉
    c.line(Pv, lerp(P0, P1, .98), H('#c8c0e8'), 1.0)
    c.line(P0, Pv, H('#b8b0d8'), 1.3)
    c.pts([(6, 28), (5, 29)], H('#7a7298'))
    c.pts([(Pv[0] - 1, Pv[1] - 1)], H('#e8e0ff'))


# ---------------------------------------------------------------- 보조 (b)
def leaf_info(p0, p1, w, a=2.0, b=0.7, skew=0.0, bend=0.0):
    """LEAF 와 같지만 각 칸의 (t, s/hw) 를 돌려줌 (줄무늬용)"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    out = {}
    for x, y in _pts():
        qx, qy = x + .5 - p0[0], y + .5 - p0[1]
        t = (qx * ux + qy * uy) / L
        if t < 0 or t > 1:
            continue
        s = -qx * uy + qy * ux - bend * math.sin(math.pi * t)
        u = 2 * t - 1
        hw = w * (max(0.0, 1 - abs(u) ** a)) ** b * (1 + skew * u)
        if hw > 0 and abs(s) <= hw:
            out[(x, y)] = (t, s / hw)
    return out


def sep(c, m, col):
    """m 의 바깥 테두리 중 이미 그려진 칸을 col 로 (겹친 열매 구분선)"""
    for q in ring(m):
        if q in c.p:
            c.p[q] = col


def calyx(c, top, ramp, n=5, ln=4.4, spread=70, w=1.3, base=-90):
    for k in range(n):
        ang = math.radians(base + (k - (n - 1) / 2) * spread / max(1, (n - 1)) * 2)
        e = (top[0] + ln * math.cos(ang), top[1] + ln * math.sin(ang) * 0.8 + 0.6)
        lf = LEAF(top, e, w, a=2, b=.7)
        c.shade(lf, ramp, 'diag')


# ---------------------------------------------------------------- 10 산딸기
def raspberry(c, cx, cy, rx, ry, RAS):
    body = LEAF((cx, cy - ry), (cx, cy + ry), rx, a=2.0, b=0.62, skew=-0.2)
    c.fill(body, RAS[3])
    ys = []
    y = cy - ry + 1.6
    r = 0
    while y < cy + ry:
        x = cx - rx - 2 + (r % 2) * 1.6
        while x < cx + rx + 2:
            if (int(x), int(y)) in body:
                ys.append((x, y))
            x += 3.2
        y += 2.8
        r += 1
    for (x, y) in ys:
        d = E(x, y, 1.75, 1.75) & body
        c.shade(d, RAS, 'sphere', box=(x, y, 1.75, 1.75), th=(.8, .35, -.2))
    return body


@icon(10)
def _(c):
    LEAFG = R4('#a0e070', '#5cb046', '#3a8240', '#25593a')
    RAS = R4('#ff8496', '#e22c52', '#a21844', '#60103a')
    lf = LEAF((14, 11), (29, 6), 4.2, a=2, b=.7, bend=-1.5)
    c.shade(lf, LEAFG, 'diag')
    c.fill(LN([(15, 10.5), (27, 6.8)], 0.9) & lf, LEAFG[3])
    mA = raspberry(c, 12, 17.5, 7.6, 8.8, RAS)
    mB = raspberry(c, 22.5, 21, 6.3, 7.2, RAS)
    sep(c, mB, RAS[3])
    calyx(c, (12, 9.8), LEAFG, ln=5.0, spread=75)
    calyx(c, (22.5, 14.4), LEAFG, ln=4.2, spread=70)
    c.fill(LN([(12, 9.5), (13.5, 4.5)], 1.4), LEAFG[2])
    c.fill(LN([(22.5, 14), (21, 11)], 1.2), LEAFG[2])
    c.pts([(13, 4)], LEAFG[0])
    c.pts([(8, 12), (9, 12)], H('#ffd0d8'))
    c.pts([(19, 17), (20, 17)], H('#ffd0d8'))


# ---------------------------------------------------------------- 11 블루베리
@icon(11)
def _(c):
    BB = R4('#a4b4ff', '#5c6ad2', '#3c409c', '#242668')
    LG = R4('#a0e070', '#5cb046', '#3a8240', '#25593a')
    lf = LEAF((16, 11), (30, 4), 4.0, a=2, b=.7, bend=-1.2)
    c.shade(lf, LG, 'diag')
    c.fill(LN([(17, 10), (28, 5)], 0.9) & lf, LG[3])
    berries = [(11.5, 17.5, 7.0), (22, 15, 6.4), (17.5, 24.2, 7.0)]
    for (x, y, r) in berries:
        m = E(x, y, r, r)
        sep(c, m, BB[3])
        c.shade(m, BB, 'sphere', box=(x, y, r, r), th=(.8, .42, .02))
        # 껍질 분(허연 막): 왼쪽 위 쪽에 약간
        for q in m:
            if (q[0] - x) + (q[1] - y) < -r * 0.9 and c.p[q] == BB[1] and (q[0] + q[1]) % 2 == 0:
                c.put(q[0], q[1], BB[0])
        # 왕관(별 모양)
        cx, cy = int(x + 1), int(y - 1)
        c.pts([(cx, cy), (cx - 1, cy - 1), (cx + 1, cy - 1), (cx - 1, cy + 1), (cx + 1, cy + 1)], BB[3])
        c.pts([(cx, cy - 1), (cx - 1, cy), (cx + 1, cy), (cx, cy + 1)], BB[2])
        c.pts([(int(x - r * .45), int(y - r * .55)), (int(x - r * .45) - 1, int(y - r * .55) + 1)], H('#e6ecff'))
        c.pts([(int(x - r * .45) + 1, int(y - r * .55) - 1)], WHITE)


# ---------------------------------------------------------------- 12 알밤
@icon(12)
def _(c):
    BU = R4('#dcdc80', '#aaa842', '#787c2c', '#4a5020')
    CH = R4('#c87c4c', '#8e4626', '#5e2814', '#3a1810')
    # 밤송이(뒤)
    bc = (11, 12.5)
    c.shade(E(bc[0], bc[1], 6.4, 6.4), BU, 'sphere')
    for k in range(12):
        a = math.radians(k * 360 / 12 + 8)
        p1 = (bc[0] + 9.2 * math.cos(a), bc[1] + 9.2 * math.sin(a))
        sp = LN([(bc[0] + 3 * math.cos(a), bc[1] + 3 * math.sin(a)), p1], 3.0, 0.6)
        c.bevel(sp, BU)
        tip = (int(bc[0] + 8.8 * math.cos(a)), int(bc[1] + 8.8 * math.sin(a)))
        c.pts([tip], H('#f0eca0'))
    # 밤(앞)
    body = LEAF((18.5, 9.5), (18.5, 29.6), 9.4, a=2.2, b=.62, skew=0.35)
    c.shade(body, CH, 'sphere', box=(17.5, 20, 10, 10.5), th=(.84, .45, .08))
    # 결 줄무늬
    for (x0, y0, x1, y1) in [(18, 12, 17, 20), (14, 14, 12, 21), (22, 14, 24, 21), (11, 18, 9.5, 23)]:
        for q in LN([(x0, y0), (x1, y1)], 0.8) & body:
            if c.p[q] in (CH[1], CH[2]):
                c.put(q[0], q[1], CH[3] if c.p[q] == CH[2] else CH[2])
    # 배꼽(아래 밝은 면)
    hil = E(18.5, 27.4, 6.0, 3.0) & body
    for (x, y) in hil:
        col = H('#e8c88c') if (x - 18) + (y - 26) < 3 else H('#b8884c')
        c.put(x, y, col)
    for x in range(14, 24):
        if (x, 24) in body and x % 2 == 0:
            c.put(x, 24, H('#c8a060'))
        if (x, 25) in body and x % 2 == 1:
            c.put(x, 25, H('#d8b070'))
    c.pts([(12, 17), (12, 18), (13, 16), (12, 19)], H('#ffd8b0'))
    c.pts([(17, 10), (18, 10)], CH[0])


# ---------------------------------------------------------------- 13 호두
@icon(13)
def _(c):
    WAL = R4('#e6bc7c', '#b8844a', '#8a5a2c', '#58381c')
    body = (E(16, 16, 11.6, 10.6) | PG([(11.5, 22.5), (20.5, 22.5), (17.2, 28.6), (14.8, 28.6)])) & RC(0, 0, 32, 29)
    c.shade(body, WAL, 'sphere', box=(16, 16.5, 12, 12), th=(.84, .46, .1))
    # 주름 (양각)
    left = [[(7, 11), (9, 13), (8, 17)], [(11, 7), (12, 10), (10.5, 14)], [(8.5, 20), (11, 22.5)], [(12, 15), (13.5, 19), (12, 23)], [(10, 24.5), (12, 26.5)]]
    right = [[(24.5, 11), (22.5, 14), (24, 18)], [(20, 7), (19.5, 10), (21, 13)], [(22.5, 21), (20, 23)], [(19, 15), (18.5, 19), (20.5, 23)], [(21, 25), (19, 27)]]
    for pl in left + right:
        dk = LN([(x + 1, y + 1) for x, y in pl], 1.0) & body
        c.fill(dk, WAL[3])
    for pl in left + right:
        li = LN(pl, 1.0) & body
        for q in li:
            c.put(q[0], q[1], WAL[0] if q[0] < 16 else WAL[1])
    # 봉합선
    seam = bez3((16, 4.5), (13.5, 10), (18.5, 20), (16, 28.5), 24)
    sm = LN(seam, 1.5)
    c.fill(sm & body, WAL[3])
    lite = LN([(x - 1.2, y) for x, y in seam], 1.0)
    for q in lite & body:
        if q not in sm:
            c.put(q[0], q[1], WAL[0])
    c.pts([(10, 11), (11, 10), (12, 9)], H('#fff0cc'))


# ---------------------------------------------------------------- 14 개박하
@icon(14)
def _(c):
    SG = R4('#c8e8b8', '#8abc94', '#5c8e70', '#34584c')
    st = LN(bez((16, 30.5), (15.5, 20), (16, 3), 20), 1.8)
    c.bevel(st, R4('#a8d4a0', '#78a888', '#4e7a64', '#34584c'))
    for (y, ln, w, up) in [(27.5, 11.5, 4.1, 4.6), (20.5, 10.5, 3.8, 4.6), (13.5, 8.5, 3.0, 4.2)]:
        for sgn in (-1, 1):
            p0 = (16, y)
            p1 = (16 + sgn * ln, y - up)
            lf = LEAF(p0, p1, w, a=1.8, b=.62, skew=0.3)
            sep(c, lf, SG[3])
            c.shade(lf, SG, 'diag', th=(.5, -.05, -.5))
            c.fill(LN([p0, lerp(p0, p1, .86)], 0.9) & lf, SG[0] if sgn < 0 else SG[3])
    FL = R4('#f8f0ff', '#c6a0f4', '#8a64cc', '#5a3c98')
    for (x, y) in [(13, 7), (17, 7), (12, 4), (18, 4), (13, 1), (17, 1)]:
        c.pts([(x, y), (x + 1, y)], FL[0])
        c.pts([(x, y + 1), (x + 1, y + 1)], FL[1])
        c.pts([(x + 1, y + 1)], FL[2])
    c.pts([(15, 6), (16, 6), (15, 3), (16, 4)], FL[3])


# ---------------------------------------------------------------- 15 호박씨 / 16 해바라기씨
def pseed(c, p0, p1, w, ramp, rim):
    info = leaf_info(p0, p1, w, a=2.0, b=.58, skew=-0.3)
    m = set(info)
    inner = erode(m, 1)
    for q in m:
        c.put(q[0], q[1], rim)
    c.shade(inner, ramp, 'diag', th=(.35, -.25, -.7))
    # 가운데 홈
    for q in LN([lerp(p0, p1, .25), lerp(p0, p1, .75)], 0.8) & inner:
        c.put(q[0], q[1], ramp[2] if c.p[q] != ramp[2] else ramp[3])
    # 뾰족 끝
    return m


@icon(15)
def _(c):
    PS = R4('#fffbe0', '#f0e6b0', '#cbbe7c', '#9a8e52')
    rim = H('#8e9a52')
    rim2 = H('#a8a860')
    s1 = pseed(c, (3, 17), (19, 3.5), 5.6, PS, rim)
    s2 = pseed(c, (9.5, 28.5), (29, 17), 5.6, PS, rim)
    sep(c, s2, H('#6c7440'))
    s3 = pseed(c, (3.5, 27), (21, 22.5), 5.0, PS, rim2)
    sep(c, s3, H('#6c7440'))
    c.pts([(7, 12), (8, 11), (9, 10)], WHITE)
    c.pts([(14, 26), (15, 25), (16, 24)], WHITE)


@icon(16)
def _(c):
    DK = R4('#6a6078', '#443a52', '#2c2438', '#1a1424')
    LT = H('#f2eee0')
    LT2 = H('#bfb8aa')
    seeds = [((3, 15), (18, 3.5), 4.7), ((9.5, 28), (29, 17.5), 4.7), ((3, 26), (21, 21.5), 4.4)]
    prev = None
    for (p0, p1, w) in seeds:
        info = leaf_info(p0, p1, w, a=2.0, b=.58, skew=-0.3)
        m = set(info)
        for q, (t, s) in info.items():
            col = DK[1]
            if s > 0.2:
                col = DK[2]
            if 0.18 < t < 0.9 and (0.26 < abs(s) < 0.66):
                col = LT if s < 0 else LT2
            elif t > 0.88 or t < 0.1:
                col = H('#6a4a3a') if t > .88 else DK[3]
            c.put(q[0], q[1], col)
        if prev is not None:
            sep(c, m, DK[3])
        prev = m
    c.pts([(6, 11), (7, 10)], LT)


# ---------------------------------------------------------------- 17 달팽이 껍질
@icon(17)
def _(c):
    SH = R4('#ffe6ae', '#e29c4e', '#a8602c', '#5a2e18')
    cc = (14.5, 14.5)
    lip = RE(23.4, 21.6, 5.4, 4.0, 42)
    shell = E(cc[0], cc[1], 12.5, 12) | lip
    c.shade(shell - lip, SH, 'sphere', box=(cc[0] - .5, cc[1] - .5, 12.5, 12), th=(.84, .45, .1))
    g = 2.2
    for q in shell - lip:
        dx, dy = q[0] + .5 - cc[0] - 1.5, q[1] + .5 - cc[1] + 1.5
        r = math.hypot(dx, dy)
        if r < 1.2:
            continue
        th = math.atan2(dy, dx)
        ph = (th / (2 * math.pi) - math.log(r) / math.log(g)) % 1.0
        k = SH.index(c.p[q])
        if ph < 0.2:
            c.p[q] = SH[3]
        elif ph < 0.58:
            c.p[q] = SH[max(0, k - 1)]
        else:
            c.p[q] = SH[min(3, k + 1)]
    c.shade(lip, R4('#fff4dc', '#f4c28c', '#d08a60', '#8a4e30'), 'diag', th=(.4, -.1, -.5))
    hole = RE(24.0, 22.4, 3.3, 2.4, 42)
    c.fill(hole, H('#4a1c30'))
    c.fill(hole & RC(0, 23, 32, 32), H('#8a3c50'))
    c.pts([(20, 19), (21, 18)], WHITE)
    c.pts([(7, 8), (8, 7), (9, 6)], H('#fff4d8'))


# ---------------------------------------------------------------- 18 무당벌레
@icon(18)
def _(c):
    BK = R4('#5a4a6a', '#2e2438', '#221a2c', '#140e1c')
    LG = (3.0, 12.0)
    # 다리
    for (x0, y0, x1, y1) in [(7, 14, 2.5, 12), (6.2, 19, 1.8, 19.5), (7.4, 24, 3.2, 28)]:
        for sgn in (-1, 1):
            xa = 16 + sgn * (16 - x0)
            xb = 16 + sgn * (16 - x1)
            c.line((xa, y0), (xb, y1), BK[1], 1.5)
    # 더듬이
    c.line((14, 5.5), (11, 2), BK[1], 1.1)
    c.line((18, 5.5), (21, 2), BK[1], 1.1)
    # 머리
    head = E(16, 8.6, 5.4, 3.8)
    c.shade(head, BK, 'sphere')
    c.pts([(13, 8), (14, 8), (18, 8), (19, 8)], WHITE)
    c.pts([(13, 9), (19, 9)], H('#c8c0d8'))
    # 몸
    body = E(16, 18.6, 10.4, 10.0)
    c.shade(body, RED, 'sphere', box=(15, 17.5, 11, 10.5), th=(.84, .45, .05))
    # 가운데 선 + 점
    for q in LN([(16, 10.5), (16, 28.5)], 1.2) & body:
        c.put(q[0], q[1], BK[2])
    for (x, y, r) in [(10.8, 15.5, 2.5), (21.2, 15.5, 2.5), (9.6, 22.4, 2.2), (22.4, 22.4, 2.2), (12.6, 26.2, 1.5), (19.4, 26.2, 1.5)]:
        sp = E(x, y, r, r) & body
        c.fill(sp, BK[1])
        c.pts([(int(x - r * .5), int(y - r * .5))], BK[0])
    # 하이라이트
    c.pts([(8, 12), (9, 11), (10, 10.5), (11, 10), (7, 13)], H('#ffd8c8'))
    c.pts([(9, 12), (10, 11)], WHITE)


# ---------------------------------------------------------------- 19 빗자루 짚
@icon(19)
def _(c):
    ANG = 16
    cols = [R4('#fff0a8', '#f0d070', '#c89a3c', '#7c5a20'),
            R4('#ffe890', '#e4b850', '#b88430', '#6e4c1c'),
            R4('#f8e07c', '#d8a840', '#a87828', '#684418')]
    n = 9
    order = sorted(range(n), key=lambda i: -abs(i - 4))
    allm = set()
    for i in order:
        a = (i - 4) / 4.0
        pts = [(16 + a * 11, 2.5 + abs(a) * 2.0), (16 + a * 7.5, 8), (16 + a * 4.6, 16), (16 + a * 6.6, 24), (16 + a * 9.5, 29.4 - abs(a) * 1.4)]
        pts = [(x, 16 + (y - 16) * .88) for x, y in pts]
        pts = rot(pts, ANG)
        mk = LN(pts, 3.2)
        cc = cols[i % 3]
        c.fill(mk, cc[3])
        c.fill(LN(pts, 2.0), cc[1])
        c.fill(LN([(x - .6, y - .3) for x, y in pts], 0.9) & mk, cc[0])
        allm |= mk
    # 끈
    band = PG(rot([(5, 14.2), (27, 14.2), (27, 19.4), (5, 19.4)], ANG)) & allm
    for (x, y) in band:
        c.put(x, y, H('#c4603c') if (x + y) % 3 else H('#e08a52'))
    for (x, y) in band:
        pass
    top = PG(rot([(5, 14.2), (27, 14.2), (27, 15.2), (5, 15.2)], ANG)) & band
    bot = PG(rot([(5, 18.4), (27, 18.4), (27, 19.4), (5, 19.4)], ANG)) & band
    c.fill(top, H('#8a3c2c'))
    c.fill(bot, H('#7a3228'))
    kn = rot([(22, 17)], ANG)[0]
    c.fill(E(kn[0], kn[1], 2.2, 2.2), H('#c4603c'))
    c.pts([(int(kn[0]) - 1, int(kn[1]) - 1)], H('#f0a070'))
    t1 = rot([(22, 17), (23.5, 22.5)], ANG)
    t2 = rot([(22, 17), (26, 21)], ANG)
    c.line(t1[0], t1[1], H('#a8482e'), 1.4)
    c.line(t2[0], t2[1], H('#a8482e'), 1.4)


# ---------------------------------------------------------------- 보조 (c): 버섯
def mushroom(c, cx, rim_y, rx, ry, CAP, STEM, stem_top, stem_bot, stem_end, lipc=None, ring_y=None, lean=0.0, spots=(), spotcol=None,
             stemx_off=0.0, flat=0.0):
    # 줄기
    sx0 = cx + stemx_off
    pts = [(sx0 - stem_top / 2, rim_y - 2), (sx0 + stem_top / 2, rim_y - 2), (sx0 + stem_bot / 2 + lean, stem_end - 1.5),
           (sx0 + stem_bot / 2 + lean - 1, stem_end), (sx0 - stem_bot / 2 + lean + 1, stem_end), (sx0 - stem_bot / 2 + lean, stem_end - 1.5)]
    stem = PG(pts)
    c.shade(stem, STEM, 'cylv', th=(.75, .3, -.2))
    # 갓 아래 주름
    lip = (E(cx, rim_y, rx * .96, 2.8) & RC(0, int(rim_y), 32, 32))
    lc = lipc or R4('#f6e6c8', '#dcc4a0', '#a88c70', '#6e5848')
    c.shade(lip, lc, 'cylh', th=(.9, .2, -.4))
    for (x, y) in lip:
        if (x % 2 == 0) and c.p[(x, y)] == lc[1]:
            c.put(x, y, lc[2])
    # 갓
    cap = E(cx, rim_y, rx, ry) & RC(0, 0, 32, int(rim_y))
    c.shade(cap, CAP, 'sphere', box=(cx - 1, rim_y + 1, rx, ry + 1), th=(.82, .42, .05))
    return cap, stem


def spot(c, x, y, r, cap, col=None, shade=None):
    m = E(x, y, r, r) & cap
    col = col or H('#fdf8ff')
    shade = shade or H('#d4c6e6')
    c.fill(m, col)
    for q in m:
        if (q[0] + 1, q[1] + 1) not in m and (q[0] + 1, q[1]) not in m or ((q[0], q[1] + 1) not in m and (q[0] + 1, q[1] + 1) not in m):
            c.put(q[0], q[1], shade)


# ---------------------------------------------------------------- 20 빨간 독버섯
@icon(20)
def _(c):
    CAPR = R4('#ff8c70', '#e83c38', '#a8203c', '#62123a')
    STEM = R4('#fffaf0', '#f0e4d4', '#c8b4b4', '#8a7490')
    cx, rim = 16, 17.5
    cap, stem = mushroom(c, cx, rim, 13.6, 11.6, CAPR, STEM, 8, 10, 29.5)
    # 치마(고리)
    sk = E(cx, 22, 6.8, 2.6)
    c.shade(sk, R4('#fffaf0', '#ecdcd0', '#bca8ac', '#7e6a88'), 'cylh', th=(.9, .3, -.3))
    c.fill(sk & RC(0, 23, 32, 32), H('#b4a0a8'))
    c.pts([(x, 22) for x in range(10, 22, 2)], H('#d8c8c8'))
    for (x, y, r) in [(9, 10, 2.5), (17.5, 7.2, 2.1), (23, 11.5, 2.7), (15, 13.2, 1.7), (7, 14.8, 1.3), (26, 15.8, 1.3), (11.5, 15.8, 1.2), (20.5, 15.2, 1.3), (13, 7, 1.2)]:
        spot(c, x, y, r, cap)
    c.pts([(7, 9), (8, 8), (10, 7), (9, 7)], H('#ffd8c0'))


# ---------------------------------------------------------------- 21 송이버섯
@icon(21)
def _(c):
    CAPB = R4('#dcb080', '#a87a4a', '#7a5232', '#4c3020')
    STEM = R4('#fff6e4', '#ecd8b4', '#c0a47c', '#86694a')
    cx, rim = 16, 14.2
    cap, stem = mushroom(c, cx, rim, 12.4, 9.0, CAPB, STEM, 10, 8, 29.6, lean=1.0)
    rr = c.rng
    for q in cap:
        if rr.random() < .2 and c.p[q] in (CAPB[1], CAPB[0]):
            c.put(q[0], q[1], CAPB[2])
    for q in cap:
        if rr.random() < .1 and c.p[q] in (CAPB[1], CAPB[2]):
            c.put(q[0], q[1], CAPB[0])
    # 줄기 섬유 무늬
    sm = {q for q in stem if q[1] >= 20}
    for y in range(20, 29):
        for x in range(10, 24):
            if (x, y) in sm and ((x * 3 + y * 5) % 7 == 0 or (x + 2 * y) % 9 == 0) and c.p[(x, y)] in (STEM[1], STEM[2], STEM[0]):
                c.put(x, y, H('#b88a58') if (x + y) % 2 else H('#d4a870'))
    # 고리
    sk = E(cx + .6, 18.6, 6.4, 2.2)
    sk &= RC(0, 0, 32, 32)
    c.shade(sk, R4('#fff8ea', '#f0dcc0', '#c0a47c', '#86694a'), 'cylh', th=(.9, .3, -.3))
    c.fill(sk & RC(0, 19, 32, 32), H('#a88a64'))
    c.pts([(9, 9), (10, 8), (12, 7), (11, 7)], H('#f4d8b0'))


# ---------------------------------------------------------------- 22 은방울꽃
@icon(22)
def _(c):
    LF = R4('#a8e078', '#62b04a', '#3c8440', '#26593a')
    l1 = LEAF((13, 30.5), (3.5, 15), 4.2, a=2, b=.62, bend=-1.5)
    l2 = LEAF((14, 30.5), (25.5, 17.5), 4.0, a=2, b=.62, bend=1.2)
    for lf in (l1, l2):
        c.shade(lf, LF, 'diag', th=(.5, -.05, -.5))
    c.fill(LN(bez((13, 30), (7.5, 25), (4.5, 16), 10), 0.9) & l1, LF[3])
    c.fill(LN(bez((14, 30), (20, 26), (25, 18.5), 10), 0.9) & l2, LF[3])
    pts = bez3((13.5, 30), (12, 14), (14, 2), (26.5, 6.5), 30)
    st = LN(pts, 1.5)
    c.bevel(st, R4('#bce890', '#7cc060', '#4e9444', '#2c6038'))
    BW = R4('#ffffff', '#f4f2ff', '#cfc6ea', '#9a8ec4')
    PED = H('#6cac58')

    def bell(x, y, s):
        x = int(x)
        y = int(y)
        dome = E(x, y + 1.7 * s, 2.6 * s, 2.4 * s)
        flare = PG([(x - 2.2 * s, y + 2.8 * s), (x + 2.2 * s, y + 2.8 * s), (x + 3.3 * s, y + 5.0 * s), (x - 3.3 * s, y + 5.0 * s)])
        m = dome | flare
        yb = max(b for (a, b) in m)
        m = {(a, b) for (a, b) in m if not (b == yb and (a - x) % 2 == 1)}
        sep(c, m, BW[3])
        c.shade(m, BW, 'diag', th=(.4, -.2, -.6))
        c.pts([(a, yb) for (a, b) in m if b == yb], BW[3])
    for (t, drop, s) in [(.45, 4, 1.15), (.6, 6, 1.15), (.76, 4, 1.05), (.92, 6, 0.95)]:
        px, py = pts[int(t * 30)]
        c.line((px, py), (px, py + drop - 0.5), PED, 1.0)
        bell(px, py + drop - 1.5, s)


# ---------------------------------------------------------------- 23 매미 허물
@icon(23)
def _(c):
    AM = R4('#fae4a0', '#dcb060', '#a8743a', '#654322')
    legs = [[(11, 9.5), (5.5, 8.5), (3.2, 14), (6.5, 18.5)], [(10.5, 13), (4.2, 15.5), (3.2, 21.5), (4.5, 25.5)], [(11, 16.5), (6, 22), (6.5, 28.5)]]
    for pl in legs:
        for sgn in (-1, 1):
            pp = [(16 + sgn * (16 - x), y) for x, y in pl]
            m = LN(pp, 2.4, 1.4)
            c.bevel(m, AM)
    ab = LEAF((16, 14.5), (16, 29.8), 5.7, a=2.0, b=.62, skew=-0.2)
    c.shade(ab, AM, 'cylv', th=(.7, .15, -.4))
    for y in range(17, 29, 2):
        for x in range(8, 24):
            if (x, y) in ab and c.p[(x, y)] != AM[3]:
                c.put(x, y, AM[2] if (x + y) % 3 else AM[3])
    th = E(16, 12.2, 6.6, 5.2)
    c.shade(th, AM, 'sphere', box=(16, 12, 6.6, 5.2), th=(.82, .4, .0))
    hd = E(16, 6.8, 5.6, 3.5)
    c.shade(hd, AM, 'sphere')
    for ex in (12.2, 19.8):
        eye = E(ex, 6.2, 2.1, 2.4)
        c.shade(eye, R4('#c88a4a', '#9a6030', '#6e4020', '#40260f'), 'sphere')
    c.fill(LN([(16, 9), (16, 16)], 1.0), AM[3])
    c.pts([(13, 10), (14, 9)], AM[0])
    c.pts([(13, 4), (12, 5)], H('#fff2c8'))
    c.pts([(14, 18), (13, 18), (14, 17)], H('#fff2c8'))


# ---------------------------------------------------------------- 24 반딧불이
@icon(24)
def _(c):
    WG = R4('#f4fcff', '#cde6f6', '#9cc0e0', '#6a90b8')
    for sgn in (-1, 1):
        w = LEAF((16 + sgn * 3, 12.5), (16 + sgn * 14.5, 5.5), 3.6, a=2, b=.7, bend=-sgn * 1.2)
        c.shade(w, WG, 'diag', th=(.5, -.15, -.6))
        c.fill(LN([(16 + sgn * 3.5, 12.2), (16 + sgn * 13.5, 6.0)], 0.8) & w, WG[2])
    for sgn in (-1, 1):
        for (y0, x1, y1) in [(12, 9.5, 17), (15, 8.5, 21), (18, 9.5, 25.5)]:
            c.line((16 + sgn * 4, y0), (16 + sgn * (16 - x1), y1), H('#4a3040'), 1.0)
    c.line((15, 5), (12, 1.5), H('#3a2434'), 1.0)
    c.line((17, 5), (20, 1.5), H('#3a2434'), 1.0)
    el = LEAF((16, 11), (16, 25.5), 5.6, a=2, b=.6)
    c.shade(el, R4('#9a7060', '#5a3a3a', '#3c2430', '#241420'), 'cylv', th=(.6, .0, -.5))
    c.fill(LN([(16, 12.5), (16, 24)], 0.9), H('#241420'))
    pn = E(16, 10, 5.4, 3.5)
    c.shade(pn, R4('#ffc0a0', '#f27c64', '#b84c54', '#703040'), 'sphere')
    c.fill(RC(15, 8, 17, 12) & pn, H('#8a3448'))
    c.fill(E(16, 5.8, 2.7, 2.2), H('#3a2434'))
    c.pts([(14, 5), (15, 4)], H('#7a5a6a'))
    gl = E(16, 26.2, 4.8, 3.8)
    c.shade(gl, R4('#fdffd8', '#e4ff6a', '#b4e834', '#6cb41e'), 'sphere', th=(.5, .1, -.4), box=(16, 26, 4.8, 3.8))
    c.pts([(15, 25), (16, 25), (15, 26)], WHITE)
    c.halo = (H('#d8ff50'), 3.0, 120)
    c.spark(5, 26, H('#f0ffa0'), 1, WHITE)
    c.dot(27, 22, H('#f0ffa0'))
    c.dot(26, 29, H('#d8ff70'))


# ---------------------------------------------------------------- 25 박쥐 날개 잎
@icon(25)
def _(c):
    WGP = R4('#a888e0', '#6e4cb0', '#48306e', '#2c1c4c')
    rw = [(16.8, 12), (21, 7), (26, 4.5), (31, 8.5), (27.8, 12.5), (29.4, 21), (24.8, 17.5), (24.4, 27), (19.8, 21.5), (16.8, 26)]
    lw = [(32 - x, y) for x, y in reversed(rw)]
    wing = PG(rw + lw)
    c.shade(wing, WGP, 'diag', th=(.55, -.1, -.6), box=(16, 15, 15, 11))
    VE = H('#b4f080')
    VE2 = H('#74c850')
    for tip in [(30.4, 8.8), (28.6, 20.6), (23.8, 26.2)]:
        for sgn in (-1, 1):
            tx = 16 + sgn * (tip[0] - 16)
            c.fill(LN([(16 + sgn * 1.2, 12), (16 + sgn * 9.5, 7.5), (tx, tip[1])] if tip[1] < 12 else [(16 + sgn * 1.2, 12.5), (tx, tip[1])], 0.9) & wing,
                   VE if sgn < 0 else VE2)
    c.fill(LN([(16 + 1.2, 12), (16 + 10, 7.2), (16 + 14, 5.8)], 0.9) & wing, H('#74c850'))
    body = LEAF((16, 7), (16, 27.5), 3.2, a=2, b=.62)
    c.shade(body, R4('#7ad89a', '#3ea074', '#2a7058', '#1c4640'), 'cylv', th=(.6, .0, -.5))
    c.fill(LN([(16, 9), (16, 26)], 0.9), H('#9af0b0'))
    for sgn in (-1, 1):
        ear = PG([(16 + sgn * 0.6, 7.5), (16 + sgn * 3.0, 2.5), (16 + sgn * 3.6, 8.5)])
        c.shade(ear, R4('#7ad89a', '#3ea074', '#2a7058', '#1c4640'), 'diag')
    c.fill(LN([(16, 26.5), (16.5, 30.6)], 1.4), H('#4a7a58'))
    c.pts([(14, 9), (18, 9)], H('#ffe070'))


# ---------------------------------------------------------------- 26 달맞이꽃
@icon(26)
def _(c):
    YL = R4('#fffbb0', '#ffe44e', '#ebb42c', '#b87a18')
    LG = R4('#b0e480', '#68b04c', '#3e8640', '#27593a')
    st = LN(bez((16, 20), (16, 25.5), (15, 30.6), 12), 1.8)
    c.bevel(st, R4('#b0e480', '#78b850', '#4a8a44', '#2c6038'))
    for (p0, p1) in [((15.5, 29), (6.5, 23.5)), ((16, 26.5), (25.5, 21.5))]:
        lf = LEAF(p0, p1, 2.7, a=2, b=.7)
        c.shade(lf, LG, 'diag')
        c.fill(LN([p0, lerp(p0, p1, .85)], 0.8) & lf, LG[3])
    C = (16, 12.8)
    for ang in (-72, 18, 108, 198):
        pm = HEART(C, ang, 11.0, 4.1, a=3.3)
        sep(c, pm, YL[3])
        c.shade(pm, YL, 'diag', th=(.55, -.05, -.6))
        t = math.radians(ang)
        dx, dy = math.cos(t), math.sin(t)
        c.fill(LN([(C[0] + dx * 3.5, C[1] + dy * 3.5), (C[0] + dx * 9, C[1] + dy * 9)], 0.8) & pm, YL[2])
    c.fill(E(16, 12.8, 2.8, 2.8), H('#9ac040'))
    c.shade(E(16, 12.8, 2.4, 2.4), R4('#e4f080', '#b0cc3c', '#7a9c28', '#4c6c1c'), 'sphere')
    for (dx, dy) in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        c.pts([(16 + dx * 2 - (1 if dx > 0 else 0), 12 + dy * 2 - (1 if dy > 0 else 0) + 1)], H('#c07818'))
    c.pts([(9, 5), (8, 6), (10, 4)], H('#fffff0'))
    c.spark(27, 5, H('#fff6a0'), 1, WHITE)
    c.dot(4, 20, H('#fff6a0'))


# ---------------------------------------------------------------- 27 거미 버섯
@icon(27)
def _(c):
    CAPP = R4('#9684d0', '#6454a4', '#413672', '#271d48')
    STEM = R4('#f8f0ff', '#dcd2f2', '#aaa0cc', '#6c6296')
    cx, rim = 16, 17.5
    cap, stem = mushroom(c, cx, rim, 12.6, 10.2, CAPP, STEM, 7, 8.5, 29.5, lipc=R4('#efe6ff', '#cbbfe6', '#9488b8', '#5e5486'))
    WEB = H('#f6f0ff')
    ctr = (16, 8.0)
    for a in (-78, -52, -26, 0, 26, 52, 78):
        t = math.radians(a)
        end = (ctr[0] + math.sin(t) * 16, ctr[1] + math.cos(t) * 16)
        c.fill(LN([ctr, end], 0.9) & cap, WEB)
    for rr_ in (4.0, 7.4, 10.8):
        ringm = E(ctr[0], ctr[1], rr_ + .5, (rr_ + .5) * .95) - E(ctr[0], ctr[1], rr_ - .6, (rr_ - .6) * .95)
        for q in ringm & cap:
            if q[1] >= ctr[1] - 0.5:
                c.put(q[0], q[1], WEB)
    c.pts([(15, 7), (16, 7), (15, 8), (16, 8)], WEB)
    # 거미 (실에 매달림)
    SPC = H('#2a1a3a')
    sx = 24.5
    c.line((sx, 17.5), (sx, 23.6), H('#d8ccf8'), 0.9)
    c.fill(E(sx, 26.0, 2.5, 2.7), SPC)
    c.fill(E(sx, 23.8, 1.5, 1.2), SPC)
    c.pts([(int(sx) - 2, 25), (int(sx) - 2, 24)], H('#7a6aa0'))
    c.pts([(int(sx), 27), (int(sx) + 1, 27)], H('#ff4a6a'))
    for (dy, ex, ey) in [(24.6, 4.8, -2.0), (25.8, 5.4, -0.2), (27.0, 5.0, 1.8), (27.9, 3.8, 2.4)]:
        for sgn in (-1, 1):
            c.fill(LN([(sx + sgn * 1.8, dy), (sx + sgn * ex * .6, dy + ey * .4 - 0.8), (sx + sgn * ex, dy + ey)], 0.9), SPC)


# ---------------------------------------------------------------- 28 들장미 열매
@icon(28)
def _(c):
    HP = R4('#ff9a78', '#e03a2c', '#a01c2c', '#601428')
    GL = R4('#a8e478', '#5cb046', '#3a8240', '#25593a')
    BR = R4('#c89868', '#946040', '#64402a', '#3c2418')
    br = LN(bez3((1.5, 7.5), (8, 1.5), (18, 1.5), (24.5, 5.5)), 1.9)
    c.bevel(br, BR)
    for (p1, w) in [((30.5, 2.5), 2.6), ((30.5, 10.5), 2.7), ((22, 11), 2.4)]:
        lf = LEAF((24, 5.5), p1, w, a=2, b=.7)
        sep(c, lf, GL[3])
        c.shade(lf, GL, 'diag')
        c.fill(LN([(24, 5.5), lerp((24, 5.5), p1, .85)], 0.8) & lf, GL[3])
    c.pts([(7, 2), (7, 1)], BR[1])
    for (x0, y0, x1, y1) in [(9, 4, 9, 12), (14.5, 2.6, 15, 19), (20, 3.8, 20.5, 10)]:
        c.line((x0, y0), (x1, y1), BR[2], 1.1)
    hips = [(9, 17, 5.4, 6.7), (21, 15.5, 5.2, 6.4), (15.2, 24.2, 5.4, 6.0)]
    for k, (cx, cy, rx, ry) in enumerate(hips):
        m = LEAF((cx, cy - ry), (cx, cy + ry), rx, a=2, b=.58, skew=0.12)
        if k == 2:
            sep(c, m, HP[3])
        c.shade(m, HP, 'sphere', box=(cx, cy, rx, ry), th=(.82, .42, .05))
        by = int(cy + ry) - 1
        c.pts([(int(cx) - 1, by), (int(cx) + 1, by), (int(cx), by), (int(cx), by - 1)], H('#4a2418'))
        c.pts([(int(cx) - 2, by - 1), (int(cx) + 2, by - 1)], H('#7a3a20'))
        ty = int(cy - ry) + 1
        c.pts([(int(cx), ty), (int(cx) - 1, ty), (int(cx) + 1, ty)], GL[2])
        c.pts([(int(cx - rx * .5), int(cy - ry * .45)), (int(cx - rx * .5), int(cy - ry * .45) + 1)], H('#fff0d0'))


# ---------------------------------------------------------------- 29 꽃사과
def apple(c, cx, cy, r, ramp, dimple=True, ry=None, hi=True):
    ry = ry or r * .94
    m = E(cx, cy, r, ry)
    if dimple:
        m -= E(cx, cy - ry + 0.3, 1.9, 1.3)
    c.shade(m, ramp, 'sphere', box=(cx, cy, r, ry), th=(.82, .45, .08))
    return m


@icon(29)
def _(c):
    CR = R4('#ffb0b4', '#ee5262', '#b42c54', '#70194a')
    GL = R4('#a8e478', '#5cb046', '#3a8240', '#25593a')
    TW = R4('#b88860', '#8a5a3a', '#5e3a24', '#3c2418')
    # 가지/잎
    lf = LEAF((21, 7), (30.5, 2.5), 3.0, a=2, b=.7, bend=-1)
    c.shade(lf, GL, 'diag')
    c.fill(LN([(21.5, 6.6), (29, 3)], 0.8) & lf, GL[3])
    c.fill(LN(bez((12.5, 5.5), (17, 2.5), (21, 6.5)), 1.4), TW[1])
    mB = apple(c, 23.3, 17.5, 6.8, CR)
    c.line((23, 10.8), (21, 5.5), TW[1], 1.3)
    mA = apple(c, 11.5, 20, 8.7, CR)
    sep(c, mA, CR[3])
    c.line((11.5, 12), (12.8, 5), TW[1], 1.4)
    c.pts([(12, 5), (13, 5)], TW[0])
    # 노란 기운 (위쪽)
    for (cx, cy, r) in ((11.5, 20, 8.7), (23.3, 17.5, 6.8)):
        for q in E(cx, cy, r, r):
            if q[1] < cy - r * .45 and (q[0] + q[1]) % 2 == 0 and c.p.get(q) in (CR[1], CR[0]):
                c.put(q[0], q[1], H('#ff9a58') if c.p[q] == CR[1] else H('#ffd090'))
    # 꽃받침(아래)
    for (cx, cy, r) in ((11.5, 20, 8.7), (23.3, 17.5, 6.8)):
        by = int(cy + r * .94) - 1
        c.pts([(int(cx), by), (int(cx) - 1, by), (int(cx) + 1, by), (int(cx), by - 1)], H('#5a2a2a'))
    c.pts([(7, 17), (7, 16), (8, 15), (9, 14)], WHITE)
    c.pts([(7, 18)], H('#ffd8dc'))
    c.pts([(21, 14), (21, 13)], WHITE)


# ---------------------------------------------------------------- 30 독사과
@icon(30)
def _(c):
    PG_ = R4('#d4f87c', '#86cc3c', '#4a9434', '#2a5a30')
    BONE = R4('#ffffff', '#f4f2dc', '#c8c8a8', '#80806c')
    m = (E(11.8, 16.6, 8.8, 8.6) | E(20.2, 16.6, 8.8, 8.6) | E(16, 21.6, 9.6, 6.8)) & RC(0, 0, 32, 29)
    m -= E(16, 8.6, 2.4, 1.5)
    c.shade(m, PG_, 'sphere', box=(16, 18, 12, 11), th=(.84, .45, .08))
    # 독 번짐(보라 방울)
    for q in LN([(8.4, 11), (8.4, 15.5)], 1.3) & m:
        c.put(q[0], q[1], H('#7a3aa8'))
    c.pts([(8, 16), (9, 16), (8, 17)], H('#7a3aa8'))
    c.pts([(8, 11)], H('#b080e0'))
    for q in LN([(24.6, 12), (24.6, 14)], 1.2) & m:
        c.put(q[0], q[1], H('#7a3aa8'))
    c.pts([(24, 15), (25, 15)], H('#7a3aa8'))
    # 해골
    cr = E(16, 16, 5.8, 5.2)
    jaw = PG([(12.8, 18), (19.2, 18), (18.2, 22.4), (13.8, 22.4)])
    sk = cr | jaw
    sep(c, sk, PG_[3])
    c.shade(sk, BONE, 'sphere', box=(16, 17, 6, 6), th=(.84, .5, .0))
    for ex in (13.4, 18.6):
        c.fill(E(ex, 16.2, 1.7, 2.0), H('#241038'))
    c.pts([(13, 15)], H('#7a3aa8'))
    c.pts([(15, 18.5), (16, 18.5)], H('#241038'))
    for x in (14, 16, 18):
        c.pts([(x - (0 if x != 18 else 0), 21)], H('#3a2a50'))
    c.pts([(15, 20), (17, 20)], H('#3a2a50'))
    c.pts([(14, 20), (18, 20)], BONE[2])
    c.fill(LN([(16, 8.5), (17.6, 3.2)], 1.5), H('#5a3a52'))
    c.pts([(16, 3), (17, 3)], H('#8a6280'))
    lf = LEAF((17, 5.6), (27, 3.4), 2.8, a=2, b=.7, bend=-1)
    c.shade(lf, R4('#a888e0', '#6e4cb0', '#48306e', '#2c1c4c'), 'diag')
    c.pts([(10, 11), (9, 12), (11, 10)], WHITE)
    c.dot(3, 8, H('#c8ff90'))
    c.dot(29, 24, H('#c8ff90'))


# ---------------------------------------------------------------- 31 나비 날개
@icon(31)
def _(c):
    BL = R4('#b8ecff', '#4c9ef2', '#2c64c8', '#1c3a8c')
    NAVY = H('#1c1850')
    fr = [(17, 15.8), (17.6, 10), (20, 5.8), (24, 3), (28, 2.6), (30.6, 4.6), (30.8, 8.4), (29, 12.4), (25.5, 15.4), (21, 17), (17.6, 17)]
    hr = [(17, 17), (22, 16.8), (26, 18.5), (28.2, 22), (27, 26), (23.6, 28.6), (20, 28.4), (17.6, 25), (17, 21)]

    def mir(p):
        return [(32 - x, y) for x, y in p]
    parts = [PG(hr), PG(mir(hr)), PG(fr), PG(mir(fr))]
    for k, m in enumerate(parts):
        if k >= 2:
            sep(c, m, NAVY)
        inner = erode(m, 2)
        c.shade(m, BL, 'diag', th=(.5, -.1, -.5), box=(16, 14, 15, 14))
        for q in m - inner:
            c.put(q[0], q[1], NAVY)
        # 가장자리 흰 점
        edge1 = [q for q in (m - inner) if q in erode(m, 1)]
        for i, q in enumerate(sorted(edge1)):
            if i % 4 == 0 and q[0] < 30 and q[0] > 2:
                c.put(q[0], q[1], H('#e8f4ff'))
    # 날개맥
    for sgn in (-1, 1):
        for (ex, ey) in [(29, 5), (27.5, 11), (23, 15), (26, 21), (22, 26)]:
            x0 = 16 + sgn * 1.5
            tx = 16 + sgn * (ex - 16)
            ln = LN([(x0, 16.5), (tx, ey)], 0.8)
            for q in ln:
                if q in erode(parts[2] | parts[3] | parts[0] | parts[1], 2) and c.p.get(q) not in (NAVY,):
                    c.put(q[0], q[1], BL[2] if sgn > 0 else BL[0])
    # 눈동자 무늬
    for sgn in (-1, 1):
        ex = 16 + sgn * 9.5
        c.fill(E(ex, 22.6, 2.4, 2.4), H('#ffb040'))
        c.fill(E(ex, 22.6, 1.3, 1.3), NAVY)
        c.pts([(int(ex) - (1 if sgn < 0 else 0), 21)], WHITE)
    # 몸, 더듬이
    c.fill(LN([(16, 8.5), (16, 25)], 2.2, 1.4), H('#2a1a3a'))
    c.fill(E(16, 7.2, 1.8, 1.8), H('#2a1a3a'))
    c.line((15.3, 6), (12.5, 1.5), H('#2a1a3a'), 0.9)
    c.line((16.7, 6), (19.5, 1.5), H('#2a1a3a'), 0.9)
    c.pts([(12, 1), (12, 2), (20, 1), (20, 2)], H('#2a1a3a'))
    c.spark(5, 9, WHITE, 1)


# ---------------------------------------------------------------- 32 사슴벌레
@icon(32)
def _(c):
    EL = R4('#c8785a', '#85402e', '#552626', '#321618')
    TH = R4('#9a6450', '#63382f', '#3f2326', '#261316')
    LEG = H('#3a2024')
    for sgn in (-1, 1):
        for (x0, y0, x1, y1) in [(9, 16.5, 2.6, 14.5), (8.4, 21, 2.0, 22.5), (10, 25.5, 4.4, 29.5)]:
            xa = 16 + sgn * (16 - x0)
            xb = 16 + sgn * (16 - x1)
            c.line((xa, y0), (xb, y1), LEG, 1.8)
    el = E(16, 21, 8.6, 9.6)
    c.shade(el, EL, 'sphere', box=(15, 20, 9, 10), th=(.84, .46, .08))
    c.fill(LN([(16, 12), (16, 30)], 1.0) & el, EL[3])
    th = E(16, 12.8, 7.6, 3.9)
    c.shade(th, TH, 'sphere')
    hd = E(16, 8.6, 4.6, 3.2)
    c.shade(hd, TH, 'sphere')
    for sgn in (-1, 1):
        pts = [(16 + sgn * 3.0, 9.0), (16 + sgn * 7.4, 7.6), (16 + sgn * 9.2, 4.4), (16 + sgn * 6.4, 1.2)]
        m = LN(pts, 3.4, 1.2)
        sep(c, m, H('#2e1416'))
        c.bevel(m, R4('#d08060', '#954a34', '#5e2c28', '#321618'))
        tooth = PG([(16 + sgn * 7.6, 6.6), (16 + sgn * 4.6, 5.6), (16 + sgn * 6.6, 4.2)])
        c.fill(tooth, H('#954a34'))
        c.pts([(int(16 + sgn * 5.0 - (1 if sgn < 0 else 0)), 5)], H('#5e2c28'))
    c.pts([(8, 15), (9, 14)], H('#c89a80'))
    c.pts([(10, 16), (10, 17), (11, 15), (10, 18)], H('#f0b898'))
    c.pts([(13, 7), (14, 7)], H('#b88068'))


# ---------------------------------------------------------------- 33 거미 알
@icon(33)
def _(c):
    SC = R4('#ffffff', '#ece6f8', '#bfb4dc', '#8478b0')
    sac = E(16, 16.5, 11.2, 10.8)
    c.shade(sac, SC, 'sphere', box=(15, 15.5, 11.5, 11), th=(.86, .5, .1))
    # 비단 감긴 결
    for pl in [bez((6, 11), (15, 15), (26, 11), 14), bez((5, 19), (16, 23), (27, 19), 14), bez((10, 6), (14, 16), (10, 27), 14), bez((22, 6), (18, 16), (22, 27), 14)]:
        for q in LN(pl, 0.9) & sac:
            k = SC.index(c.p[q])
            c.put(q[0], q[1], SC[min(3, k + 1)] if (q[0] + q[1]) % 2 == 0 else c.p[q])
    # 알이 비치는 창
    win = E(16, 17.4, 7.4, 6.4)
    for q in win:
        c.put(q[0], q[1], H('#b4a8da') if (q[0] - 16) + (q[1] - 17) > 1 else H('#d0c6ec'))
    for (x, y) in [(13.5, 14.2), (18.5, 14.2), (11, 17.8), (16, 17.6), (21, 17.8), (13.5, 21), (18.5, 21)]:
        e = E(x, y, 1.7, 1.7)
        c.fill(e, H('#fff0a8'))
        c.pts([(int(x) + 1, int(y) + 1)], H('#d8a850'))
        c.pts([(int(x), int(y) + 1)], H('#e8c878'))
        c.pts([(int(x) - 1, int(y) - 1)], WHITE)
    c.pts([(7, 9), (8, 8), (9, 7), (10, 6)], WHITE)
    # 실 (윤곽선 없이)
    th = H('#c4badc')
    for (a, b) in [((8, 9), (1, 2)), ((24, 9), (30, 2)), ((5, 22), (1, 29)), ((27, 22), (31, 29)), ((16, 6), (16, 1))]:
        for q in LN([a, b], 0.8):
            c.top[q] = th
    c.halo = None


# ---------------------------------------------------------------- 34 유령 꽃
@icon(34)
def _(c):
    GH = R4('#ffffff', '#e8efff', '#b8c6ee', '#8294cc')
    st = LN(bez((16, 20), (15, 25), (16.5, 30.6), 12), 1.7)
    c.bevel(st, R4('#d4eee4', '#a4d0c4', '#6c9c94', '#486c70'))
    for (p0, p1) in [((15.8, 28), (8, 24.5)), ((16.2, 26), (24.5, 22.5))]:
        lf = LEAF(p0, p1, 2.3, a=2, b=.7)
        c.shade(lf, R4('#d4eee4', '#a4d0c4', '#6c9c94', '#486c70'), 'diag')
    C = (16, 13.2)
    for k in range(6):
        ang = k * 60 - 90 + 0
        t = math.radians(ang)
        dx, dy = math.cos(t), math.sin(t)
        m = LEAF((C[0] + dx * 2, C[1] + dy * 2), (C[0] + dx * 11.2, C[1] + dy * 11.2), 3.6, a=2, b=.55, bend=(1.4 if k % 2 else -1.4))
        sep(c, m, GH[3])
        c.shade(m, GH, 'diag', th=(.45, -.2, -.65))
        c.fill(LN([(C[0] + dx * 4, C[1] + dy * 4), (C[0] + dx * 10, C[1] + dy * 10)], 0.7) & m, GH[2])
    orb = E(C[0], C[1], 4.0, 4.0)
    c.shade(orb, R4('#ffffff', '#d8f6ff', '#9cd0f0', '#5c98d0'), 'sphere')
    for ex in (14, 17.5):
        c.pts([(ex, 12), (ex, 13)], H('#2a2658'))
    c.pts([(15, 15), (16, 15)], H('#2a2658'))
    c.halo = (H('#bfe8ff'), 2.6, 120)
    c.spark(4, 7, H('#dff4ff'), 1, WHITE)
    c.dot(28, 18, H('#dff4ff'))
    c.dot(5, 22, H('#dff4ff'))


# ---------------------------------------------------------------- 35 해골 꽃
@icon(35)
def _(c):
    PT = R4('#e280f0', '#a844c8', '#6c2a94', '#3e1a5c')
    BONE = R4('#ffffff', '#f4eeda', '#c8c0a8', '#8a8070')
    LG = R4('#a0d070', '#5ca048', '#3a7040', '#274a38')
    st = LN(bez((16, 24), (16, 27), (17, 30.6), 10), 1.8)
    c.bevel(st, R4('#98c870', '#5a9a48', '#386c3c', '#254a36'))
    lf = LEAF((16.5, 29), (26, 25), 2.4, a=2, b=.7)
    c.shade(lf, LG, 'diag')
    C = (16, 13.4)
    for k in range(6):
        ang = k * 60 - 90 + 30
        t = math.radians(ang)
        dx, dy = math.cos(t), math.sin(t)
        m = LEAF((C[0] + dx * 1, C[1] + dy * 1), (C[0] + dx * 13, C[1] + dy * 13), 4.6, a=2, b=.6)
        sep(c, m, PT[3])
        c.shade(m, PT, 'diag', th=(.5, -.1, -.6))
        c.fill(LN([(C[0] + dx * 5, C[1] + dy * 5), (C[0] + dx * 11, C[1] + dy * 11)], 0.8) & m, PT[2])
    cr = E(16, 12.6, 5.6, 5.0)
    jaw = PG([(12.8, 15.5), (19.2, 15.5), (18.2, 19.4), (13.8, 19.4)])
    sk = cr | jaw
    sep(c, sk, PT[3])
    c.shade(sk, BONE, 'sphere', box=(16, 14, 6, 6.2), th=(.84, .5, .0))
    for ex in (13.4, 18.6):
        c.fill(E(ex, 13, 1.7, 2.0), H('#241038'))
    c.pts([(15, 15.5), (16, 15.5)], H('#241038'))
    c.pts([(15, 17.5), (17, 17.5), (15, 18.5), (17, 18.5)], H('#3a2a50'))
    c.pts([(12, 9), (13, 8), (14, 8)], WHITE)
    c.dot(3, 5, H('#f0b0ff'))
    c.dot(29, 24, H('#f0b0ff'))


# ---------------------------------------------------------------- 36 달빛 버섯
@icon(36)
def _(c):
    CAPB = R4('#c8f6ff', '#58c4ff', '#3a82e0', '#2650b0')
    STEM = R4('#f0ffff', '#c0e8ff', '#88b8e8', '#5a80c0')
    LIPB = R4('#e8fcff', '#a8e0ff', '#6aa8e0', '#4070b8')
    cap2, st2 = mushroom(c, 24.8, 25.4, 6.2, 4.8, CAPB, STEM, 3.6, 4.4, 29.6, lipc=LIPB)
    spot(c, 22.5, 22, 1.0, cap2, H('#e8ffff'), H('#a8e0ff'))
    spot(c, 26, 22.5, .9, cap2, H('#e8ffff'), H('#a8e0ff'))
    cap, st = mushroom(c, 12.5, 18.8, 11.4, 9.4, CAPB, STEM, 5.4, 6.6, 29.6, lipc=LIPB)
    for (x, y, r) in [(8.5, 11.5, 2.0), (15, 8.5, 1.7), (17.8, 13, 1.5), (11.5, 15, 1.2), (6.5, 15.5, 1.0), (20.5, 16.5, 1.0)]:
        spot(c, x, y, r, cap, H('#e8ffff'), H('#9ad8ff'))
    c.pts([(6, 11), (7, 10), (9, 8), (8, 9)], H('#ffffff'))
    c.halo = (H('#7fd8ff'), 3.0, 120)
    c.spark(27, 7, H('#c8f4ff'), 1, WHITE)
    c.dot(2, 4, H('#c8f4ff'))
    c.dot(29, 15, H('#c8f4ff'))


# ---------------------------------------------------------------- 37 무지개 이끼
@icon(37)
def _(c):
    bands = [H('#ee4a5c'), H('#fa9a3a'), H('#f8e050'), H('#6cd05a'), H('#4aa8f0'), H('#9a68e0')]
    edges = [14.6, 12.5, 10.4, 8.3, 6.2, 4.1, 2.0]
    cc = (16, 26.5)
    rr = c.rng
    allm = set()
    for k in range(6):
        col = bands[k]
        ro, ri = edges[k], edges[k + 1]
        for q in _pts():
            dx, dy = q[0] + .5 - cc[0], q[1] + .5 - cc[1]
            r = math.hypot(dx, dy)
            if ri <= r < ro and q[1] <= 28:
                f = (ro - r) / (ro - ri)
                cl = col
                if f < .3:
                    cl = lerpc(col, (255, 255, 255), .35)
                elif f > .72:
                    cl = lerpc(col, (40, 20, 60), .3)
                # 솜털 질감
                if rr.random() < .12:
                    cl = lerpc(cl, (255, 255, 255), .25)
                elif rr.random() < .1:
                    cl = lerpc(cl, (30, 10, 50), .2)
                c.put(q[0], q[1], cl)
                allm.add(q)
    # 바깥 솜털
    for q in sorted(ring(allm)):
        if q[1] <= 27 and 1 <= q[0] <= 30 and rr.random() < .3:
            dx, dy = q[0] + .5 - cc[0], q[1] + .5 - cc[1]
            if math.hypot(dx, dy) > 12:
                c.put(q[0], q[1], lerpc(bands[0], (255, 255, 255), .2))
    # 양쪽 이끼 덩이
    MS = R4('#b2e868', '#6cb83c', '#43873a', '#2a5a34')
    for (x, y, r) in [(4.6, 26.5, 3.6), (27.4, 26.5, 3.6), (7.6, 28.4, 3.0), (24.4, 28.4, 3.0)]:
        m = E(x, y, r, r * .9) & RC(0, 0, 32, 30)
        c.shade(m, MS, 'sphere')
        for q in m:
            if rr.random() < .25:
                c.put(q[0], q[1], MS[0] if rr.random() < .6 else MS[3])
    c.spark(16, 8, H('#fff8c0'), 1, WHITE)
    c.spark(5, 12, H('#d8f0ff'), 1, WHITE)
    c.dot(27, 11, H('#ffe0f0'))


# ---------------------------------------------------------------- 38 반짝 돌
@icon(38)
def _(c):
    outline = [(6, 17), (9, 10), (15, 6), (22, 8), (27, 13), (26.5, 21), (20, 26.5), (11, 26.5), (6.5, 22)]
    m = PG(outline)
    facets = [
        ([(9, 10), (15, 6), (17, 14.5), (6, 17.5)], H('#d8dcf8')),
        ([(15, 6), (22, 8), (27, 13), (17, 14.5)], H('#aab2e8')),
        ([(6, 17.5), (17, 14.5), (14.5, 26.5), (6.5, 22)], H('#8e98d4')),
        ([(17, 14.5), (27, 13), (26.5, 21), (20, 26.5), (14.5, 26.5)], H('#6c76b8')),
        ([(14.5, 26.5), (20, 26.5), (26.5, 21), (22, 20)], H('#4e5894')),
    ]
    for pts, col in facets:
        c.fill(PG(pts) & m, col)
    # 면 사이 밝은 모서리
    for (a, b) in [((9, 10), (6, 17.5)), ((15, 6), (22, 8)), ((9, 10), (15, 6))]:
        c.fill(LN([a, b], 0.9) & m, H('#f4f6ff'))
    for (a, b) in [((17, 14.5), (14.5, 26.5)), ((17, 14.5), (27, 13))]:
        c.fill(LN([a, b], 0.8) & m, H('#5a64a4'))
    rr = c.rng
    for _ in range(26):
        q = (rr.randint(7, 26), rr.randint(8, 26))
        if q in m:
            c.put(q[0], q[1], rr.choice([H('#ffffff'), H('#8ae8ff'), H('#ffe890'), H('#c8b8ff')]))
    c.spark(22, 11, WHITE, 2, WHITE)
    c.spark(10, 21, H('#9aeaff'), 1, WHITE)
    c.spark(25, 24, H('#ffe890'), 1, WHITE)
    c.dot(5, 8, H('#ffffff'))
    c.dot(28, 5, H('#ffffff'))


# ---------------------------------------------------------------- 39 호박석 (벌레가 들어 있는 호박)
@icon(39)
def _(c):
    AMB = R4('#fff2a8', '#fcc444', '#dc841c', '#8e4418')
    poly = PG([(5.5, 14), (8, 8), (14, 4.8), (21.5, 5.5), (27, 10), (27.5, 18), (24, 24.5), (17, 27.5), (9.5, 26), (5.5, 20.5)])
    m = dilate(erode(poly, 2), 2) & dilate(poly, 1)
    cc = (16, 16)
    for q in m:
        d = math.hypot((q[0] + .5 - cc[0]) / 12.0, (q[1] + .5 - cc[1]) / 11.0)
        ang = (q[0] - cc[0]) * -0.4 + (q[1] - cc[1]) * -0.5
        v = d - 0.12 * (ang / 8)
        k = 0 if v < .34 else 1 if v < .64 else 2 if v < .86 else 3
        c.put(q[0], q[1], AMB[k])
    # 안쪽 가장자리 빛 (반투명 느낌)
    for q in m:
        if (q[0] + 1, q[1] + 1) not in m and c.p[q] != AMB[0]:
            pass
    for q in erode(m, 1) - erode(m, 2):
        if q[0] + q[1] > 28 and c.p[q] == AMB[3]:
            c.put(q[0], q[1], AMB[2])
    INS = H('#3a1e0c')
    # 날개
    for sgn in (-1, 1):
        w = LEAF((16 + sgn * 1.4, 14.2), (16 + sgn * 9.4, 8.6), 2.6, a=2, b=.7)
        for q in ring(w):
            if q in m:
                c.put(q[0], q[1], H('#9a5a1c'))
        for q in w:
            c.put(q[0], q[1], H('#fff4c4'))
        c.fill(LN([(16 + sgn * 2, 13.8), (16 + sgn * 8.2, 9.2)], 0.7) & w, H('#e0a850'))
    # 다리
    for sgn in (-1, 1):
        for (y, ex, ey) in [(15.0, 5.4, -2.2), (16.6, 6.0, 0.6), (18.2, 5.0, 3.6)]:
            c.fill(LN([(16 + sgn * 1.6, y), (16 + sgn * ex * .55, y + ey * .4 + 0.6), (16 + sgn * ex, y + ey)], 0.9) & m, INS)
    c.fill(LEAF((16, 16), (16, 25), 2.0, a=2, b=.7), INS)
    c.fill(E(16, 14.8, 2.1, 2.1), INS)
    c.fill(E(16, 11.8, 1.6, 1.6), INS)
    c.line((15.2, 10.5), (13.6, 8.4), INS, 0.9)
    c.line((16.8, 10.5), (18.4, 8.4), INS, 0.9)
    for y in (19, 21.5):
        c.pts([(15, int(y)), (16, int(y))], H('#8a5a24'))
    # 윤기
    c.pts([(8, 11), (9, 10), (10, 9), (11, 8), (8, 12)], H('#fffbe0'))
    c.pts([(9, 10), (10, 9)], WHITE)
    c.pts([(24, 21), (23, 22)], H('#ffd870'))
    c.spark(27, 5, H('#fff0a0'), 1, WHITE)
    c.dot(3, 26, H('#ffe890'))


# ---------------------------------------------------------------- 보조 (e)
def dilate(m, n=1):
    m = set(m)
    for _ in range(n):
        m = m | ring(m)
    return {q for q in m if 0 <= q[0] < S and 0 <= q[1] < S}


def smooth(m, n=2):
    return dilate(erode(m, n), n)


def crystal(c, base, ang, L, w, CR):
    ty = -(L - w * 1.5)

    def T(pts):
        return PG(rot([(base[0] + x, base[1] + y) for x, y in pts], ang, base))
    left = T([(-w, 0), (-w * .25, 0), (-w * .25, ty), (-w, ty)])
    mid = T([(-w * .25, 0), (w * .35, 0), (w * .35, ty), (-w * .25, ty)])
    right = T([(w * .35, 0), (w, 0), (w, ty), (w * .35, ty)])
    tl = T([(-w, ty), (-w * .25, ty), (0, -L), ])
    tm = T([(-w * .25, ty), (w * .35, ty), (0, -L)])
    tr = T([(w * .35, ty), (w, ty), (0, -L)])
    whole = left | mid | right | tl | tm | tr
    return whole, [(left, CR[1]), (mid, CR[0]), (right, CR[2]), (tl, CR[0]), (tm, lerpc(CR[0], CR[1], .5)), (tr, CR[1])]


# ---------------------------------------------------------------- 40 자수정
@icon(40)
def _(c):
    CR = R4('#e4baff', '#a86cec', '#6e3cb4', '#46267c')
    ROCK = R4('#9a8aa8', '#6e6080', '#4a3f5e', '#2e2640')
    rock = (E(16, 28, 12.5, 4.0) | E(9.5, 27, 4.6, 3.2) | E(22.5, 27.4, 5.0, 3.4)) & RC(0, 0, 32, 31)
    c.shade(rock, ROCK, 'sphere', box=(16, 27, 14, 5))
    rr = c.rng
    for q in rock:
        if rr.random() < .15:
            c.put(q[0], q[1], ROCK[0] if rr.random() < .5 else ROCK[3])
    cl = [((8.6, 28), -48, 9.5, 2.5), ((23.6, 28), 48, 10, 2.6), ((10.5, 27), -27, 17, 3.4), ((21.5, 27), 25, 16, 3.4),
          ((16, 27), 0, 24, 4.4), ((13.8, 28), -10, 10, 2.5)]
    for (b, a, L, w) in cl:
        whole, faces = crystal(c, b, a, L, w, CR)
        sep(c, whole, CR[3])
        for (m, col) in faces:
            c.fill(m, col)
        # 모서리 하이라이트
        edge = [rot([(b[0] - w * .25, b[1] - 1), (b[0] - w * .25, b[1] - (L - w * 1.5))], a, b)][0]
        c.fill(LN(edge, 0.8) & whole, H('#f4dcff'))
    c.spark(7, 6, H('#f4dcff'), 1, WHITE)
    c.spark(25, 8, WHITE, 1, WHITE)
    c.dot(16, 2, WHITE)
    c.dot(29, 18, H('#e4baff'))


# ---------------------------------------------------------------- 41 조개 화석 (암모나이트)
@icon(41)
def _(c):
    MX = R4('#e6dcc4', '#c0b294', '#8e8068', '#5c5240')
    AM = R4('#fbd896', '#d49c54', '#966034', '#53321e')
    disc = (E(16, 16, 13.4, 12.8) | E(17, 17, 12.6, 13)) & RC(0, 1, 32, 31)
    cc = (15.0, 15.6)
    c.shade(disc, MX, 'sphere', box=(16, 16, 13.4, 12.8), th=(.82, .45, .08))
    g = 2.3
    for q in disc:
        dx, dy = q[0] + .5 - cc[0], q[1] + .5 - cc[1]
        r = math.hypot(dx, dy)
        k = MX.index(c.p[q])
        if r > 12.0:
            continue
        th = math.atan2(dy, dx)
        ph = (th / (2 * math.pi) - math.log(max(r, .3)) / math.log(g)) % 1.0
        rib = (th / (2 * math.pi) * (9 + r * 0.7)) % 1.0
        if r < 1.4:
            c.p[q] = AM[3]
        elif ph < 0.17:
            c.p[q] = AM[3]
        else:
            u = (ph - 0.17) / 0.83
            kk = 0 if u < .28 else 1 if u < .62 else 2
            if rib < 0.4 and kk < 2:
                kk += 1
            c.p[q] = AM[kk]
    rr = c.rng
    for q in disc:
        r = math.hypot(q[0] + .5 - cc[0], q[1] + .5 - cc[1])
        if r > 12.2 and rr.random() < .22:
            c.put(q[0], q[1], MX[2] if rr.random() < .6 else MX[0])
    c.pts([(7, 8), (8, 7), (9, 6)], H('#fff8e8'))
    c.dot(28, 5, H('#fff0d0'))


# ---------------------------------------------------------------- 42 월장석
@icon(42)
def _(c):
    MS = R4('#ffffff', '#e6eeff', '#b8c4ee', '#8890c4')
    m = E(16, 16.2, 10.8, 12.8)
    c.shade(m, MS, 'sphere', box=(16, 16, 10.8, 12.8), th=(.85, .5, .1))
    sheen = E(13, 12.5, 6.8, 8.6) - E(16.2, 15.4, 6.6, 8.6)
    for q in sheen & m:
        c.put(q[0], q[1], H('#9ccaff') if (q[0] + q[1]) % 3 else H('#bfdcff'))
    inner = E(14.5, 14, 4.2, 5.6) & m
    for q in inner:
        c.put(q[0], q[1], H('#f4f8ff'))
    # 달 문양 (옅은 초승달)
    cres = E(17.5, 19.5, 4.2, 4.2) - E(19.4, 18.2, 3.8, 3.8)
    for q in cres & m:
        c.put(q[0], q[1], H('#fff0b8') if (q[0] + q[1]) % 2 == 0 else H('#ffe090'))
    c.pts([(9, 10), (9, 11), (10, 8), (10, 9), (11, 7)], WHITE)
    c.pts([(21, 24), (22, 23)], MS[3])
    c.spark(26, 6, H('#dce8ff'), 2, WHITE)
    c.spark(5, 24, H('#dce8ff'), 1, WHITE)
    c.dot(27, 27, H('#dce8ff'))


# ---------------------------------------------------------------- 43 별가루 병
@icon(43)
def _(c):
    glass = PG([(9.5, 14), (22.5, 14), (25, 17), (25, 26), (22, 29.6), (10, 29.6), (7, 26), (7, 17)]) | RC(12.5, 8, 19.5, 14) | RC(11.5, 7, 20.5, 9)
    inner = erode(glass, 1)
    c.fill(glass, H('#bfe0ff'))
    EMPTY = (190, 216, 255, 70)
    for q in inner:
        c.p[q] = EMPTY
    # 별가루(차있는 부분)
    top_y = 17
    dust = {q for q in inner if q[1] >= top_y}
    for q in dust:
        t = (q[1] - top_y) / 12.0
        c.p[q] = lerpc(H('#3a2a8c'), H('#24185a'), t)
    for q in dust:
        if q[1] == top_y:
            c.p[q] = H('#8a7ae0')
    rr = c.rng
    for q in dust:
        if rr.random() < .1:
            c.p[q] = H('#5a48b8')
    for (x, y) in [(12, 21), (18, 19), (14, 26), (20, 24), (10, 27)]:
        c.pts([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], H('#ffe36a'))
        c.pts([(x, y)], H('#fff8c0'))
    for (x, y) in [(15, 22), (21, 28), (11, 23), (17, 27), (23, 20)]:
        c.pts([(x, y)], H('#ffffff'))
    for (x, y) in [(13, 18), (22, 26)]:
        c.pts([(x, y)], H('#ff9ad0'))
    for (x, y) in [(16, 20), (9, 25), (19, 22)]:
        c.pts([(x, y)], H('#8af0ff'))
    # 병 하이라이트
    for y in range(18, 27):
        c.put(9, y, H('#e8f6ff'))
    c.pts([(9, 16), (10, 15), (10, 17), (14, 10), (14, 11), (14, 12)], WHITE)
    # 코르크
    cork = RC(13, 2, 19, 8)
    c.shade(cork, R4('#e4b078', '#bc844a', '#8a5a2c', '#5a3818'), 'cylv')
    for q in [(15, 4), (17, 6), (14, 6), (16, 3)]:
        c.put(q[0], q[1], H('#8a5a2c'))
    c.fill(RC(11, 7, 21, 8), H('#9cb8e0'))
    c.spark(27, 8, H('#fff0a0'), 1, WHITE)
    c.spark(4, 20, H('#c8b8ff'), 1, WHITE)
    c.dot(28, 22, H('#8af0ff'))
    c.dot(3, 8, H('#ffffff'))


# ---------------------------------------------------------------- 44 요정 날개 가루
@icon(44)
def _(c):
    PO = R4('#f8d4fc', '#d08ce8', '#9254bc', '#5e3088')
    body = E(16, 21, 10.6, 8.8) | PG([(11, 9.5), (21, 9.5), (19.5, 14), (12.5, 14)]) | E(16, 14, 5.2, 3)
    body &= RC(0, 0, 32, 30)
    c.shade(body, PO, 'sphere', box=(16, 20, 11, 10), th=(.84, .45, .08))
    # 입구 주름(윗단)
    fr = PG([(10.2, 8), (21.8, 8), (20.6, 12.2), (11.4, 12.2)])
    c.shade(fr, PO, 'cylh', th=(.8, .1, -.4))
    for x in range(11, 22, 2):
        c.pts([(x, 9), (x, 10)], PO[2])
    # 금색 끈
    c.fill(LN([(11, 13), (21, 13)], 1.7), H('#ffd23a'))
    c.fill(LN([(11, 14.2), (21, 14.2)], 0.9), H('#c88a1c'))
    c.pts([(12, 12), (13, 12)], H('#fff4a0'))
    c.fill(E(22, 14.5, 2.2, 1.7), H('#ffd23a'))
    c.line((21.5, 15.5), (23.5, 20), H('#e0a828'), 1.2)
    c.line((22.5, 15.5), (26, 19), H('#e0a828'), 1.2)
    c.pts([(24, 20), (26, 19)], H('#ffe27a'))
    # 날개 문양
    WN = R4('#e8fffc', '#9ceaf0', '#52b8d0', '#2e7aa0')
    for sgn in (-1, 1):
        w1 = LEAF((16 + sgn * 0.8, 21.4), (16 + sgn * 6.0, 17.2), 2.0, a=2, b=.65)
        w2 = LEAF((16 + sgn * 0.8, 22), (16 + sgn * 4.6, 25.8), 1.6, a=2, b=.65)
        for w in (w2, w1):
            for q in ring(w):
                if q in c.p:
                    c.p[q] = WN[3]
            c.shade(w, WN, 'diag')
    c.fill(LN([(16, 19), (16, 24)], 1.3), H('#6a3a98'))
    # 반짝이 가루
    glit = [H('#ff9ad8'), H('#8af0ff'), H('#fff08a'), H('#ffffff'), H('#c8a8ff')]
    for (x, y) in [(13, 6), (16, 3), (19, 5), (11, 3), (21, 2), (15, 7), (18, 8), (24, 7), (8, 6), (5, 12)]:
        c.dot(x, y, glit[(x * 3 + y) % 5])
    c.spark(16, 4, H('#fff0a0'), 2, WHITE)
    c.spark(7, 9, H('#8af0ff'), 1, WHITE)
    c.spark(26, 10, H('#ff9ad8'), 1, WHITE)
    c.top[(13, 6)] = H('#ffffff')


# ---------------------------------------------------------------- 45 늑대 털 뭉치
@icon(45)
def _(c):
    FUR = [R4('#f4f2fa', '#d0cee0', '#a4a2bc', '#70708e'), R4('#dcdaea', '#b4b2ca', '#8a88a4', '#5c5a78'),
           R4('#b4b2c8', '#8a88a2', '#625f7c', '#413f58'), R4('#8c8aa4', '#66647e', '#464360', '#2e2c44')]
    base = (16, 28)
    strands = [(3, 14, 3), (30, 15, 3), (6, 7, 2), (26, 6, 2), (10, 3, 1), (22, 3, 1), (16, 1.5, 0), (13, 5, 0), (19, 6, 1),
               (4, 21, 3), (28, 22, 2), (8, 11, 1), (24, 11, 1), (11, 8, 0), (21, 9, 0), (15, 10, 1), (17, 12, 0)]
    for k, (tx, ty, ci) in enumerate(strands):
        bx = base[0] + (tx - 16) * 0.16
        p0 = (bx, base[1])
        mid = lerp(p0, (tx, ty), .55)
        nx_, ny_ = -(ty - base[1]), (tx - bx)
        nl = math.hypot(nx_, ny_)
        off = 3.2 * (1 if k % 2 else -1)
        ctrl = (mid[0] + nx_ / nl * off, mid[1] + ny_ / nl * off)
        pts = bez(p0, ctrl, (tx, ty), 14)
        m = LN(pts, 4.2, 0.6)
        F = FUR[ci]
        sep(c, m, F[3])
        c.fill(m, F[1])
        lit = LN([(x - .8, y - .5) for x, y in pts], 1.4, 0.4) & m
        c.fill(lit, F[0])
        dk = LN([(x + 1.0, y + .7) for x, y in pts], 1.2, 0.3) & m
        c.fill(dk - lit, F[2])
    mass = E(16, 27.5, 5.6, 2.8)
    c.shade(mass, FUR[2], 'sphere')
    c.pts([(12, 26), (13, 25), (14, 25)], FUR[0][0])


# ---------------------------------------------------------------- 46 별똥별 조각
@icon(46)
def _(c):
    RK = R4('#a498c8', '#6a5e94', '#443c6c', '#2a2448')
    outline = [(13, 15.5), (18, 12), (24, 12.5), (28.5, 17), (28, 24), (22.5, 29), (15, 27.8), (11.5, 22)]
    rock = PG(outline)
    c.shade(rock, RK, 'sphere', box=(20, 20, 9.5, 9.5), th=(.84, .46, .08))
    # 구덩이
    for (x, y, r) in [(20, 17, 2.2), (25, 21, 1.8), (18, 24, 2.0), (23, 26, 1.2)]:
        cr = E(x, y, r, r) & rock
        c.fill(cr, RK[3])
        for q in cr:
            if (q[0] - 1, q[1] - 1) not in cr:
                pass
        for q in (shift(cr, 1, 1) - cr) & rock:
            c.put(q[0], q[1], RK[0])
    # 달궈진 가장자리 / 균열
    for q in rock:
        if (q[0] - 1, q[1] - 1) not in rock or (q[0] - 1, q[1]) not in rock and (q[0], q[1] - 1) not in rock:
            c.put(q[0], q[1], H('#ff9a3a'))
    for pl in [[(21, 13), (22, 17), (20, 20)], [(26, 15), (25, 19), (27, 22)], [(15, 20), (18, 21), (19, 25)]]:
        m = LN(pl, 0.9) & rock
        c.fill(m, H('#ff7a2a'))
    c.pts([(22, 14), (22, 15), (21, 19)], H('#ffd060'))
    c.pts([(25, 18), (26, 21)], H('#ffd060'))
    c.pts([(16, 20), (18, 21)], H('#ffd060'))
    # 꼬리 (윤곽선 없이 위에 얹음)
    keep = rock | ring(rock)
    tail_o = LN([(14, 17), (2.5, 2.5)], 9.0, 0.6)
    tail_m = LN([(14, 17), (3.5, 3.5)], 5.8, 0.4)
    tail_c = LN([(14, 17), (4.5, 4.5)], 3.0, 0.3)
    for q in tail_o - keep:
        c.top[q] = H('#ff8a2a')
    for q in tail_m - keep:
        c.top[q] = H('#ffc84a')
    for q in tail_c - keep:
        c.top[q] = H('#fff6c8')
    rr = c.rng
    for _ in range(14):
        t = rr.random()
        x = 12 - t * 9 + rr.uniform(-3, 3)
        y = 15 - t * 12 + rr.uniform(-3, 3)
        q = (int(x), int(y))
        if q not in keep and q not in c.top and 0 <= q[0] < 32 and 0 <= q[1] < 32:
            c.top[q] = H('#ffb040') if rr.random() < .6 else H('#fff0a0')
    c.spark(6, 22, H('#fff0a0'), 1, WHITE)
    c.spark(24, 5, H('#ffd8a0'), 1, WHITE)
    c.dot(2, 12, H('#ffe080'))


# ---------------------------------------------------------------- 47 황금 도토리
@icon(47)
def _(c):
    acorn(c, GOLD, GOLDCAP, R4('#f6d070', '#c8962c', '#8e5e1c', '#5a3a14'), H('#fffbe0'), gold=True)
    c.halo = (H('#ffe070'), 2.8, 120)
    c.spark(6, 9, H('#fff4a0'), 2, WHITE)
    c.spark(26, 14, H('#fff4a0'), 1, WHITE)
    c.spark(25, 27, H('#ffe890'), 1, WHITE)
    c.dot(5, 24, H('#fff4a0'))


# ---------------------------------------------------------------- 48 유니콘 털
@icon(48)
def _(c):
    grad = [H('#ffa8d4'), H('#e8a8ff'), H('#a8b8ff'), H('#90e4ff'), H('#a8ffd8')]

    def gcol(t):
        f = max(0.0, min(1.0, t)) * (len(grad) - 1)
        i = min(len(grad) - 2, int(f))
        return lerpc(grad[i], grad[i + 1], f - i)

    def lock(path, w0, w1, tshift):
        m = LN(path, w0, w1)
        n = len(path)
        for q in m:
            px, py = q[0] + .5, q[1] + .5
            best = (99, 0)
            for i, (x, y) in enumerate(path):
                d = math.hypot(px - x, py - y)
                if d < best[0]:
                    best = (d, i)
            d, i = best
            j = min(n - 1, i + 1)
            j0 = max(0, i - 1)
            tx, ty = path[j][0] - path[j0][0], path[j][1] - path[j0][1]
            tl = math.hypot(tx, ty) or 1
            nx_, ny_ = -ty / tl, tx / tl
            s = (px - path[i][0]) * nx_ + (py - path[i][1]) * ny_
            if nx_ + ny_ > 0:
                s = -s
            col = gcol(i / (n - 1) + tshift)
            hw = (w0 * (1 - i / (n - 1)) + w1 * (i / (n - 1))) / 2
            f = s / max(hw, .8)
            if f > 0.3:
                col = lerpc(col, (255, 255, 255), .5)
            elif f < -0.4:
                col = lerpc(col, (80, 40, 140), .38)
            if abs(abs(s) - hw * .42) < .5 and hw > 1.7:
                col = lerpc(col, (255, 255, 255), .32) if s > 0 else lerpc(col, (80, 40, 140), .24)
            c.put(q[0], q[1], col)
        return m
    back = bez3((17, 6), (3, 12), (20, 21), (5, 28), 40)
    m2 = lock(back, 6.0, 1.2, 0.25)
    front = bez3((22, 3), (7, 9), (28, 19), (14, 29), 40)
    sep(c, LN(front, 9.2, 1.8), H('#5a2c88'))
    m1 = lock(front, 9.2, 1.8, 0.0)
    band = LN([(19.4, 1.8), (24.8, 6.6)], 3.4) & m1
    c.fill(band, H('#ffd23a'))
    c.pts([(20, 2), (21, 3), (20, 3)], H('#fff4a0'))
    c.fill(shift(band, 1, 1) - band & m1, H('#c88a1c'))
    c.spark(5, 6, H('#ffd8f4'), 2, WHITE)
    c.spark(27, 15, H('#c8f0ff'), 1, WHITE)
    c.spark(5, 20, H('#d8ffe8'), 1, WHITE)
    c.spark(24, 27, H('#fff0a0'), 1, WHITE)
    c.dot(29, 25, H('#ffd8f4'))
    c.dot(11, 3, H('#ffd8f4'))
    c.move(0, 1)


# ---------------------------------------------------------------- 49 호박달 씨앗
@icon(49)
def _(c):
    cres = E(15.5, 16.5, 13.8, 13.8) - E(20.5, 12, 12.6, 12.6)
    cres &= RC(0, 0, 32, 31)
    CM = R4('#fffbd0', '#ffe98a', '#f0b83c', '#b87a20')
    c.shade(cres, CM, 'diag', th=(.55, 0.0, -.5), box=(8, 22, 10, 10))
    seed = LEAF((8.5, 25.5), (24.5, 6.5), 6.3, a=2.0, b=.58, skew=-0.28)
    sep(c, seed, H('#7a3a14'))
    inner = erode(seed, 1)
    OR = R4('#ffe49a', '#ffa032', '#d86a18', '#8e3a14')
    for q in seed:
        c.put(q[0], q[1], H('#c8641c'))
    c.shade(inner, OR, 'diag', th=(.4, -.2, -.65))
    for q in LN([lerp((8.5, 25.5), (24.5, 6.5), .25), lerp((8.5, 25.5), (24.5, 6.5), .75)], 0.8) & inner:
        c.put(q[0], q[1], OR[2])
    c.pts([(12, 18), (13, 17), (14, 15), (13, 16)], H('#fff2c0'))
    c.halo = (H('#ffc060'), 2.8, 120)
    c.spark(27, 24, H('#fff0a0'), 1, WHITE)
    c.spark(4, 6, H('#ffe890'), 1, WHITE)
    c.dot(28, 8, H('#fff0a0'))
    c.dot(3, 28, H('#ffe890'))
# ==== ICONS-END (아래는 미리보기/메인)


def preview(sheet, outdir):
    os.makedirs(outdir, exist_ok=True)
    bgc = (0x21, 0x17, 0x33, 255)
    Z = 4
    per = 10
    rows = (N + per - 1) // per
    cell = S * Z
    pad = 6
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + pad) + pad), bgc)
    for i in range(N):
        t = sheet.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST)
        img.alpha_composite(t, (pad + (i % per) * (cell + pad), pad + (i // per) * (cell + pad)))
    img.save(os.path.join(outdir, 'forage_prev.png'))
    # 라벨판
    font = None
    for f in ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/opentype/unifont/unifont.otf'):
        try:
            font = ImageFont.truetype(f, 14)
            break
        except Exception:
            pass
    lh = 34
    img2 = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), bgc)
    d = ImageDraw.Draw(img2)
    for i in range(N):
        x0 = pad + (i % per) * (cell + pad)
        y0 = pad + (i // per) * (cell + lh + pad)
        t = sheet.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST)
        img2.alpha_composite(t, (x0, y0))
        d.text((x0, y0 + cell + 2), '%d' % i, fill=(255, 220, 120, 255), font=font)
        d.text((x0, y0 + cell + 17), NAMES[i], fill=(220, 210, 240, 255), font=font)
    img2.save(os.path.join(outdir, 'forage_prev_lbl.png'))


if __name__ == '__main__':
    sheet = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT)
    print('saved', OUT, sheet.size, len(ICONS), 'icons')
    if '--preview' in sys.argv:
        preview(sheet, sys.argv[sys.argv.index('--preview') + 1])
