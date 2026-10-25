# 낚시 물고기 그림 (32×32 픽셀, 코드로 그림): 물고기 60 + 쓰레기 3 → public/art/fish.png (63칸 × 32px = 2016×32)
# python3 tools/iso/fish_icons.py [미리보기.png]   → 시트를 다시 만들어요 (칸 순서 = 게임의 FISH 순서)
# 물고기는 모두 머리가 왼쪽. 도구: 타원·다각형·관(튜브)·몸통 곡선 → 면 칠하기(왼쪽 위 빛) → 무늬 덧칠 → 바깥 1px 테두리.
import os, sys, math
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 32
OUT = (26, 16, 36)          # #1a1024 바깥 테두리


# ---------------------------------------------------------------- 색
def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def mul(a, f):
    return tuple(max(0, min(255, int(round(c * f)))) for c in a)

def R(base, dk=None, lt=None, hi=None):
    """색 4단: [어둠, 기본, 밝음, 하이라이트]. 어둠은 보랏빛으로, 밝음은 따뜻하게."""
    b = hx(base) if isinstance(base, str) else base
    d = hx(dk) if isinstance(dk, str) else (dk or mix(mul(b, .66), (46, 22, 84), .30))
    l = hx(lt) if isinstance(lt, str) else (lt or mix(b, (255, 244, 226), .38))
    h = hx(hi) if isinstance(hi, str) else (hi or mix(b, (255, 255, 255), .74))
    return [d, b, l, h]

def edge_col(r):
    return mix(r[0], OUT, .45)


# ---------------------------------------------------------------- 모양 (점 집합). 좌표는 칸 가운데가 정수.
def E(cx, cy, rx, ry, k=1.0):
    s = set()
    for y in range(N):
        for x in range(N):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= k:
                s.add((x, y))
    return s

def EL(cx, cy, rx, ry, ang=0, k=1.0):
    """기울어진 타원 (ang: 도, 0 = 오른쪽, 90 = 아래쪽 방향이 rx 축)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    s = set()
    for y in range(N):
        for x in range(N):
            u = (x - cx) * ca + (y - cy) * sa
            v = -(x - cx) * sa + (y - cy) * ca
            if (u / rx) ** 2 + (v / ry) ** 2 <= k:
                s.add((x, y))
    return s

def petal(bx, by, ang, ln, wd):
    """기준점에서 ang 방향으로 길이 ln, 폭 wd 인 꽃잎 모양."""
    a = math.radians(ang)
    return EL(bx + math.cos(a) * ln / 2, by + math.sin(a) * ln / 2, ln / 2, wd / 2, ang)

def PG(pts):
    im = Image.new('L', (N, N), 0)
    ImageDraw.Draw(im).polygon([(int(round(x)), int(round(y))) for x, y in pts], fill=1)
    px = im.load()
    return {(x, y) for y in range(N) for x in range(N) if px[x, y]}

def RC(x0, y0, x1, y1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}

def sh(S, dx, dy):
    return {(x + dx, y + dy) for x, y in S}

def clip(S):
    return {(x, y) for x, y in S if 0 <= x < N and 0 <= y < N}

def chk(S, ph=0):
    return {(x, y) for x, y in S if (x + y) % 2 == ph}

def spline(pts, n=10):
    """Catmull-Rom 곡선 위의 점들."""
    if len(pts) < 3:
        return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                  + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out

def tube(pts, r0, r1=None, smooth=True, step=.25):
    """점들을 지나는 굵은 선. 반지름이 r0에서 r1로 줄어들어요."""
    if r1 is None:
        r1 = r0
    path = spline(pts) if (smooth and len(pts) > 2) else list(pts)
    # 길이에 따라 고르게 다시 뽑기
    segs = []
    for i in range(len(path) - 1):
        (ax, ay), (bx, by) = path[i], path[i + 1]
        L = math.hypot(bx - ax, by - ay)
        m = max(1, int(L / step))
        for k in range(m):
            t = k / m
            segs.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    segs.append(path[-1])
    s = set()
    T = len(segs) - 1 or 1
    for i, (cx, cy) in enumerate(segs):
        r = r0 + (r1 - r0) * i / T
        rr = r + .02
        for y in range(int(cy - rr) - 1, int(cy + rr) + 2):
            for x in range(int(cx - rr) - 1, int(cx + rr) + 2):
                if (x - cx) ** 2 + (y - cy) ** 2 <= rr * rr:
                    s.add((x, y))
    return clip(s)

def LN(a, b, r=.5):
    return tube([a, b], r, r, smooth=False)

def prof(pts):
    """몸통 곡선: [(x, 위, 아래), …] 를 부드럽게 이어 한 칸씩 채워요."""
    xs = [p[0] for p in pts]
    def tang(arr, i):
        if i == 0:
            return (arr[1] - arr[0]) / (xs[1] - xs[0])
        if i == len(arr) - 1:
            return (arr[-1] - arr[-2]) / (xs[-1] - xs[-2])
        return (arr[i + 1] - arr[i - 1]) / (xs[i + 1] - xs[i - 1])
    def interp(col, x):
        arr = [p[col] for p in pts]
        for i in range(len(xs) - 1):
            if xs[i] <= x <= xs[i + 1]:
                h = xs[i + 1] - xs[i]
                t = (x - xs[i]) / h
                m0, m1 = tang(arr, i) * h, tang(arr, i + 1) * h
                t2, t3 = t * t, t * t * t
                return (2 * t3 - 3 * t2 + 1) * arr[i] + (t3 - 2 * t2 + t) * m0 + (-2 * t3 + 3 * t2) * arr[i + 1] + (t3 - t2) * m1
        return None
    s = set()
    for x in range(int(math.ceil(xs[0])), int(math.floor(xs[-1])) + 1):
        t, b = interp(1, x), interp(2, x)
        if t is None:
            continue
        for y in range(int(math.ceil(t - .01)), int(math.floor(b + .01)) + 1):
            s.add((x, y))
    return clip(s)

def edge_of(S):
    return {(x, y) for x, y in S if any((x + dx, y + dy) not in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


# ---------------------------------------------------------------- 칠하기 도구
class Cv:
    def __init__(s):
        s.p = {}
        s.t = {}

    def tones(s, M, light=(-1, -1), rad=4.2, t1=.62, t2=1.55, t0=-.55):
        lx, ly = light
        L = math.hypot(lx, ly)
        lx, ly = lx / L, ly / L
        ir = int(rad) + 1
        res = {}
        for (x, y) in M:
            sx = sy = n = 0
            for yy in range(y - ir, y + ir + 1):
                for xx in range(x - ir, x + ir + 1):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= rad * rad and (xx, yy) in M:
                        sx += xx; sy += yy; n += 1
            vx, vy = x - sx / n, y - sy / n
            d = vx * lx + vy * ly
            res[(x, y)] = 3 if d > t2 else 2 if d > t1 else 0 if d < t0 else 1
        return res

    def add(s, M, rmp, shade=True, edge=None, hi=True, ec=None, **kw):
        """면 하나를 칠해요. edge='out' 이미 칠한 이웃 쪽 가장자리를 어둡게, 'in' 이 면의 가장자리를 어둡게."""
        M = clip(M)
        if isinstance(rmp[0], int):
            rmp = [rmp] * 4
            shade = False
        if shade:
            tn = s.tones(M, **kw)
        else:
            tn = {p: 1 for p in M}
        prior = set(s.p)
        ec = ec or edge_col(rmp)
        if edge == 'out':
            for (x, y) in M:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + dx, y + dy)
                    if q not in M and q in prior:
                        s.p[q] = ec
        for q in M:
            t = tn[q]
            if t == 3 and not hi:
                t = 2
            s.p[q] = rmp[t]
            s.t[q] = t
        if edge == 'in':
            for (x, y) in M:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + dx, y + dy)
                    if q not in M and q in prior:
                        s.p[(x, y)] = ec
                        break
        return M

    def pat(s, S, rmp, keep_tone=True):
        """이미 칠한 곳 위에 무늬 색을 덧칠 (밝기 단계는 그대로)."""
        for q in S:
            if q in s.p:
                s.p[q] = rmp[s.t.get(q, 1) if keep_tone else 1]

    def col(s, S, c):
        for q in S:
            if q in s.p:
                s.p[q] = c

    def darken(s, S, f=.78):
        for q in S:
            if q in s.p:
                s.p[q] = mix(mul(s.p[q], f), (40, 20, 70), .08)

    def lighten(s, S, t=.3):
        for q in S:
            if q in s.p:
                s.p[q] = mix(s.p[q], (255, 250, 235), t)

    def dot(s, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            s.p[(x, y)] = c

    def put(s, S, c):
        for q in clip(S):
            s.p[q] = c

    def erase(s, S):
        for q in S:
            s.p.pop(q, None)

    def eye(s, x, y, size=2, ring=None, white=(255, 255, 255), pupil=None):
        """눈 (x,y = 왼쪽 위 칸). 2: 어두운 2×2 / 3: 둥근 3×3 / 4: 둥근 4×4. ring 색을 주면 흰자 + 왼쪽 눈동자."""
        K = pupil or OUT
        if size == 1:
            s.dot(x, y, K); return
        if size == 2:
            for dx in (0, 1):
                for dy in (0, 1):
                    s.dot(x + dx, y + dy, K)
            s.dot(x, y, white)
            return
        if size == 3:
            px = [(dx, dy) for dx in range(3) for dy in range(3) if (dx, dy) != (2, 2)]
            cut = [(2, 2)]
            hl = (0, 0)
            pp = [(0, 1), (1, 1), (0, 2), (1, 2)]
        else:
            px = [(dx, dy) for dx in range(4) for dy in range(4) if (dx, dy) not in ((0, 0), (3, 0), (0, 3), (3, 3))]
            cut = []
            hl = (1, 1)
            pp = [(0, 1), (1, 1), (0, 2), (1, 2)]
        if ring is None:
            for dx, dy in px:
                s.dot(x + dx, y + dy, K)
            s.dot(x + hl[0], y + hl[1], white)
        else:
            for dx, dy in px + cut:
                s.dot(x + dx, y + dy, ring)
            if size == 3:
                s.dot(x + 2, y + 2, ring)
            for dx, dy in ([(0, 1), (1, 1), (0, 2), (1, 2)] if size == 3 else [(1, 1), (2, 1), (1, 2), (2, 2)]):
                s.dot(x + dx, y + dy, K)
            s.dot(x + (0 if size == 3 else 1), y + (1 if size == 3 else 1), white)

    def rays(s, M, origin, angles, f=.8):
        """부채꼴 지느러미 살: 기준점에서 각도(도) 방향으로 선을 그어 살짝 어둡게."""
        ox, oy = origin
        hit = set()
        for a in angles:
            ex = ox + math.cos(math.radians(a)) * 40
            ey = oy + math.sin(math.radians(a)) * 40
            hit |= LN((ox, oy), (ex, ey), .5) & M
        s.darken(hit, f)

    def fit(s, lim=30):
        """그림이 칸(0~31)을 꽉 채우면 바깥 테두리가 잘려요. 몸이 lim칸보다 크면 가장 닮은 줄을 빼서 줄이고, 1~30 안으로 옮겨요."""
        for axis in (0, 1):
            while True:
                vals = [q[axis] for q in s.p]
                lo, hi = min(vals), max(vals)
                if hi - lo + 1 <= lim:
                    break
                best = None
                for k in range(lo + 3, hi - 2):
                    a = {q[1 - axis]: col for q, col in s.p.items() if q[axis] == k}
                    b = {q[1 - axis]: col for q, col in s.p.items() if q[axis] == k - 1}
                    cost = sum(1 for t in set(a) | set(b) if a.get(t) != b.get(t))
                    if best is None or cost < best[0]:
                        best = (cost, k)
                k = best[1]
                new_p, new_t = {}, {}
                for q, col in s.p.items():
                    v = q[axis]
                    if v == k:
                        continue
                    nq = (q[0] - (1 if axis == 0 and v > k else 0), q[1] - (1 if axis == 1 and v > k else 0))
                    new_p[nq] = col
                    new_t[nq] = s.t.get(q, 1)
                s.p, s.t = new_p, new_t
        for axis in (0, 1):
            vals = [q[axis] for q in s.p]
            d = 0
            if min(vals) < 1:
                d = 1 - min(vals)
            elif max(vals) > 30:
                d = 30 - max(vals)
            if d:
                s.p = {((q[0] + d, q[1]) if axis == 0 else (q[0], q[1] + d)): col for q, col in s.p.items()}

    def image(s):
        s.fit()
        full = set(s.p)
        o = set()
        for (x, y) in full:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in full and 0 <= q[0] < N and 0 <= q[1] < N:
                    o.add(q)
        im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
        px = im.load()
        for q in o:
            px[q] = OUT + (255,)
        for (x, y), c in s.p.items():
            px[x, y] = c + (255,)
        return im


FISH = {}        # 번호 → (id, 한글 이름, 그리는 함수)
def fish(i, fid, name):
    def deco(fn):
        FISH[i] = (fid, name, fn)
        return fn
    return deco


def fade(S, x0, ph=0):
    """x0 오른쪽부터는 바둑판으로 듬성듬성 (반투명한 유령 느낌)."""
    return {q for q in S if q[0] < x0 or (q[0] + q[1]) % 2 == ph}

def rim(c, S, col):
    """면의 가장자리 한 줄을 색칠."""
    c.put(edge_of(S) & set(c.p), col)


# ================================================================= 물고기
@fish(0, 'f_minnow', '유령 피라미')
def _(c):
    r = R('#d4e2ff', dk='#8190d6', lt='#f0f5ff')
    fn = R('#aebdf2', dk='#6f7cc4', lt='#dbe4ff')
    tail = PG([(21, 15), (30, 8), (27, 13), (25, 16), (27, 19), (30, 24), (21, 17)])
    c.add(fade(tail, 27), fn)
    c.add(PG([(11, 12), (14, 7), (18, 12)]), fn)
    c.add(PG([(14, 20), (16, 24), (19, 20)]), fn)
    body = prof([(3, 15, 18), (4, 13, 19.5), (8, 11, 21), (13, 11, 21), (18, 12.5, 19.5), (22, 14, 18)])
    c.add(body, r, edge='out')
    c.lighten({(x, y) for x, y in body if 16 <= y <= 17 and 10 <= x <= 21}, .5)
    c.add(PG([(9, 17), (13, 20), (14, 17)]), fn, edge='in')
    c.darken({(8, y) for y in range(13, 20)} & body, .85)
    c.eye(5, 13, 3, ring=(255, 255, 255))
    c.dot(3, 17, hx('#5a4a90'))


@fish(1, 'f_crucian', '호박 붕어')
def _(c):
    o = R('#f08a24', dk='#b4511c', lt='#ffb13e')
    d = R('#d96d1a', dk='#90401a', lt='#f79a2a')
    g = R('#5fae3a', dk='#2f6d2c', lt='#92d65a')
    c.add(PG([(24, 14), (30, 9), (31, 15), (31, 17), (30, 23), (24, 18)]), d)
    c.add(PG([(9, 9), (11, 5), (17, 4), (22, 7), (22, 12)]), d)
    c.add(PG([(14, 23), (17, 27), (21, 24), (19, 21)]), d)
    body = prof([(3, 15, 18), (5, 11.5, 21.5), (9, 9, 24), (14, 8.5, 24.5), (19, 10.5, 22.5), (23, 13.5, 19.5), (25, 14.5, 18.5)])
    c.add(body, o, edge='out')
    # 호박 갈비선
    for x in (8, 12, 16, 20):
        top = min(y for (xx, y) in body if xx == x)
        bot = max(y for (xx, y) in body if xx == x)
        c.pat(tube([(x, top + 1), (x - 1.5, 16.5), (x, bot - 1)], .5) & body, d)
    c.add(PG([(10, 18), (14, 21), (15, 17)]), d, edge='in')
    # 꼭지
    c.add(RC(8, 3, 10, 9) & set(), g)
    c.add(PG([(8, 9), (8, 3), (11, 2), (11, 4), (10, 9)]), g, edge='out')
    c.add(tube([(11, 3), (14, 1), (16, 2), (15, 3)], .5, smooth=True), g)
    c.eye(5, 13, 3)
    c.dot(3, 17, hx('#7a2d12')); c.dot(4, 17, hx('#7a2d12'))


@fish(2, 'f_seedbit', '호박씨 송사리')
def _(c):
    r = R('#f3e2a6', dk='#c0a566', lt='#fff5cf')
    gr = R('#8ea84e', dk='#4f6b2f', lt='#b4cd6e')
    fn = R('#e6efd0', dk='#9aae78', lt='#f6fae6')
    c.add(PG([(23, 14), (29, 11), (29, 21), (23, 18)]), fn)
    c.add(PG([(17, 12), (20, 8), (23, 13)]), fn)
    c.add(PG([(9, 21), (13, 25), (21, 24), (20, 19)]), fn)
    body = PG([(3, 16), (5, 13), (9, 11), (14, 10), (19, 11), (23, 14), (24, 16), (23, 18), (19, 21), (14, 22), (9, 21), (5, 19)])
    c.add(body, r, edge='out')
    c.pat(edge_of(body) & body, gr, keep_tone=False)
    c.col(edge_of(body) & body & {q for q in body if q[0] < 5}, hx('#6a8a3a'))
    c.pat({(x, 16) for x in range(8, 22)} & body, gr)
    for x in (10, 14, 18):
        c.pat({(x, 14), (x, 18)} & body, gr)
    c.add(PG([(8, 17), (12, 20), (12, 17)]), fn, edge='in')
    c.eye(5, 14, 3)


@fish(3, 'f_killi', '이끼 송사리')
def _(c):
    r = R('#58b39a', dk='#2d6e6e', lt='#8fdcb8')
    m = R('#4c9a3a', dk='#24602c', lt='#86cf50')
    fn = R('#7fd0c0', dk='#3e8a8c', lt='#b7efe0')
    c.add(PG([(22, 15), (27, 11), (30, 13), (30, 20), (27, 22), (22, 18)]), fn)
    c.add(PG([(14, 19), (16, 23), (21, 22), (22, 18)]), fn)
    body = prof([(3, 15.5, 18.5), (5, 13, 20), (9, 12, 21), (15, 12.5, 20.5), (20, 14, 19), (23, 15, 18)])
    c.add(body, r, edge='out')
    # 이끼 덩이 (등에 난 보송한 털)
    blob = E(10, 12.4, 3.2, 1.8) | E(15, 12.4, 3.4, 1.7) | E(19.5, 14, 2.6, 1.4)
    c.add(blob, m, edge='out')
    for q in ((9, 10), (11, 10), (14, 10), (16, 10), (18, 12), (20, 12), (7, 12), (12, 9), (15, 9)):
        c.dot(q[0], q[1], m[1] if q[1] == 10 else m[2])
    c.add(tube([(21, 14), (24, 14), (26, 15), (28, 14)], .8, .5), m)
    c.add(tube([(10, 14), (9, 18), (10, 20)], .5), m, shade=False) if False else None
    for q in ((12, 17), (16, 18), (19, 17), (9, 18)):
        c.pat({q}, R('#bff3ff'))
    c.add(PG([(8, 18), (12, 21), (12, 18)]), fn, edge='in')
    c.eye(5, 14, 3, ring=hx('#ffd25a'))


@fish(4, 'f_loach', '진흙 미꾸라지')
def _(c):
    r = R('#b9a066', dk='#74603a', lt='#e0cc90')
    mud = R('#7a5232', dk='#43291c', lt='#a77a4c')
    fn = R('#d2bb80', dk='#8a7444', lt='#efe0b0')
    # 진흙 더미
    path = [(6, 14), (10, 11), (15, 13), (20, 19), (25, 21), (29, 18)]
    body = tube(path, 3.7, 1.4)
    c.add(PG([(27, 19), (31, 14), (31, 22), (27, 21)]), fn)
    c.add(PG([(12, 8), (16, 8), (20, 13), (22, 15), (17, 13)]), fn)
    c.add(body, r, edge='out')
    belly = {q for q in body if q[1] >= 14 and q[0] < 12}
    for (x, y, rx, ry) in ((13, 11, 2, 1.4), (19, 17, 1.8, 1.4), (24, 19, 1.6, 1.2), (9, 9.5, 1.5, 1.1), (16, 15.5, 1.2, 1)):
        c.pat(E(x, y, rx, ry) & body, mud)
    c.lighten({q for q in body if q[1] >= 15 and q[0] < 10}, .3)
    # 수염
    for a_, b_ in (((3, 12), (0, 10)), ((3, 14), (0, 14)), ((3, 13), (0, 12))):
        c.put(LN(a_, b_, .5), hx('#efe4c8'))
    c.eye(5, 11, 2)
    c.dot(3, 15, hx('#7a6038'))

@fish(5, 'f_smelt', '촛불 빙어')
def _(c):
    r = R('#dff5ff', dk='#8fb4d8', lt='#f6fdff')
    fn = R('#c4e6f8', dk='#82a6d0', lt='#eaf8ff')
    wax = R('#fff1c8', dk='#d8b878', lt='#ffffff')
    fl = R('#ffae2a', dk='#e0521a', lt='#ffe45e', hi='#fffbe0')
    c.add(PG([(22, 17), (30, 11), (27, 17), (30, 23), (22, 19)]), fn)
    c.add(PG([(12, 21), (15, 25), (19, 21)]), fn)
    c.add(PG([(18, 14), (20, 11), (22, 14)]), fn)
    body = prof([(3, 17, 19.5), (4, 15, 21), (8, 14, 22), (13, 14.5, 22), (18, 15.5, 21), (23, 17, 20)])
    c.add(body, r, edge='out')
    # 비치는 등뼈
    c.pat({(x, 18) for x in range(9, 22)} & body, R('#b2cbe8'))
    for x in (11, 13, 15, 17, 19):
        c.pat({(x, 17), (x, 19)} & body, R('#c3d9ee'))
    c.add(PG([(9, 20), (12, 22), (13, 20)]), fn, edge='in')
    c.eye(5, 15, 3, ring=(255, 255, 255))
    # 초 + 촛불
    c.add(RC(11, 8, 13, 14), wax, edge='out')
    c.dot(10, 14, wax[0]); c.dot(14, 14, wax[0])
    c.dot(13, 10, wax[0]); c.dot(13, 12, wax[0]); c.dot(14, 11, wax[0])
    c.put({(12, 7)}, OUT)
    c.add(PG([(12, 3), (13, 5), (13, 6), (11, 6), (11, 5)]), fl, hi=True)
    c.put({(12, 6), (12, 5)}, fl[3])
    c.dot(12, 4, fl[2])


@fish(6, 'f_cloudcrab', '구름 게')
def _(c):
    b = R('#e9ecff', dk='#9aa2d8', lt='#ffffff')
    cl = R('#9aaeee', dk='#5e6cc0', lt='#c4d2ff')
    pk = R('#ffc0d4', dk='#d77c9c', lt='#ffe4ee')
    # 다리
    for a in (-1, 1):
        for (sy, ey, ex) in ((20, 28, 5), (22, 29, 7), (24, 30, 10)):
            pass
    legs = set()
    for sgn in (1, -1):
        cx = 15.5
        for (y0, x1, y1) in ((19, 5, 24), (21, 4, 28), (23, 7, 30)):
            xs = cx + sgn * 8
            xe = cx + sgn * (cx - x1) if True else 0
            legs |= tube([(xs, y0), (cx + sgn * 12.5, y0 - 1 + (y1 - y0) * .3), (cx + sgn * (cx - x1 + 1), y1)], .9, .6)
    c.add(legs, cl, shade=False, edge='out')
    # 집게팔
    for sgn in (1, -1):
        cx = 15.5
        arm = tube([(cx + sgn * 7, 17), (cx + sgn * 11, 13), (cx + sgn * 12, 10)], 1.4, 1.4)
        c.add(arm, cl, shade=False, edge='out')
        claw = E(cx + sgn * 12, 6.2, 3.8, 4.4) - PG([(cx + sgn * 12, 6), (cx + sgn * 14.5, 0), (cx + sgn * 10.5, 0)]) \
            - PG([(cx + sgn * 12, 5), (cx + sgn * 13, 1), (cx + sgn * 11, 1)])
        c.add(claw, pk, edge='out')
    # 구름 등딱지
    shell = E(15.5, 19, 9.5, 5.6) | E(9.5, 16, 3.6, 3.4) | E(14.5, 14, 4.2, 3.8) | E(20.5, 15.5, 3.8, 3.4) | E(22, 19, 5, 4.4) | E(9, 20, 4, 3.6)
    c.add(shell, b, edge='out')
    c.pat({(x, y) for x, y in shell if y >= 22} & shell, cl, keep_tone=True)
    # 눈자루 + 눈
    for ex in (12, 19):
        c.add(LN((ex + .5, 13), (ex + .5, 10), .6), b, shade=False, edge=None)
    c.eye(11, 7, 3)
    c.eye(18, 7, 3)
    c.put({(13, 20), (14, 20), (17, 20), (18, 20)}, cl[1])
    c.dot(15, 22, hx('#8a5a9a'))
    c.dot(16, 22, hx('#8a5a9a'))


@fish(7, 'f_carp', '버섯 잉어')
def _(c):
    r = R('#cfa44a', dk='#85602a', lt='#f0cd78')
    fn = R('#c0782e', dk='#7c4426', lt='#e49a48')
    cap = R('#e0382e', dk='#8e1c3a', lt='#ff6a48')
    stem = R('#f4e8cc', dk='#b49c80', lt='#ffffff')
    c.add(PG([(23, 15), (30, 8), (28, 14), (27, 17), (28, 20), (30, 26), (23, 19)]), fn)
    c.add(PG([(15, 10), (17, 8), (22, 10), (23, 15), (17, 13)]), fn)
    c.add(PG([(14, 24), (17, 27), (21, 24), (19, 22)]), fn)
    body = prof([(3, 16, 19), (5, 13, 22), (9, 11, 24), (14, 10.5, 24.5), (19, 12, 22.5), (23, 14.5, 19.5)])
    c.add(body, r, edge='out')
    # 비늘
    for (x, y) in ((10, 16), (13, 15), (16, 16), (19, 17), (11, 20), (14, 20), (17, 21)):
        c.pat({(x - 1, y), (x, y + 1), (x + 1, y)} & body, fn)
    c.lighten({(x, y) for x, y in body if y >= 22 and x < 18}, .25)
    c.add(PG([(9, 19), (13, 22), (14, 18)]), fn, edge='in')
    c.eye(5, 14, 3)
    # 수염
    c.put(LN((3, 18), (1, 21), .5) | LN((4, 19), (2, 23), .5), hx('#e8c870'))
    # 버섯
    c.add(RC(11, 6, 13, 11), stem, edge='out')
    c.add(E(12, 6, 7, 4.6) & {(x, y) for x in range(N) for y in range(0, 8)}, cap, edge='out')
    c.pat({(9, 4), (10, 5), (13, 3), (14, 5), (12, 6), (6, 6), (16, 6)} & set(c.p), R('#fff3e0', dk='#e8c8c0', lt='#ffffff'))


@fish(8, 'f_batcat', '박쥐 메기')
def _(c):
    r = R('#7a6a9c', dk='#42365e', lt='#a698c8')
    w = R('#8a5ccc', dk='#3a2278', lt='#b890f0')
    c.add(PG([(22, 15), (27, 12), (30, 15), (30, 19), (27, 21), (22, 18)]), w)
    c.add(PG([(14, 20), (16, 23), (22, 23), (23, 19)]), w)
    # 박쥐 날개 (펼친 모습)
    wing = PG([(13, 13), (14, 6), (19, 0), (21, 7), (27, 3), (25, 10), (31, 10), (27, 13), (22, 13)])
    c.add(wing, w, edge=None, rad=3.2)
    c.put(tube([(14, 6), (19, 0)], .5, smooth=False) | tube([(14, 6), (27, 3)], .5, smooth=False) | tube([(14, 6), (31, 10)], .5, smooth=False), w[0])
    c.put(tube([(13, 13), (14, 6)], .5, smooth=False), w[3])
    body = prof([(3, 15, 20), (5, 12.5, 21.5), (9, 12, 22), (14, 12.5, 21), (19, 13.5, 20), (23, 15, 19)])
    c.add(body, r, edge='out')
    c.lighten({(x, y) for x, y in body if y >= 19 and 5 < x < 20}, .22)
    # 박쥐 귀
    c.add(PG([(4, 12), (4, 6), (8, 11)]), r, edge='out')
    c.add(PG([(8, 11), (9, 6), (12, 12)]), r, edge='out')
    c.dot(5, 9, hx('#e89ab8')); c.dot(9, 9, hx('#e89ab8'))
    # 입 + 송곳니 + 수염
    c.put({(x, 18) for x in range(3, 9)}, OUT)
    c.dot(4, 19, (255, 255, 255)); c.dot(7, 19, (255, 255, 255))
    for a_, b_ in (((3, 16), (0, 15)), ((4, 20), (1, 25)), ((3, 18), (0, 21)), ((5, 20), (4, 27))):
        c.put(LN(a_, b_, .5), r[2])
    c.eye(6, 13, 3, ring=hx('#ffe35a'))


@fish(9, 'f_candy', '사탕 열대어')
def _(c):
    pk = R('#ff5a8c', dk='#b82a62', lt='#ff8cb0')
    wh = R('#fff4f8', dk='#e6a8c4', lt='#ffffff')
    wr = R('#9fe0ff', dk='#4e9ad8', lt='#d6f4ff')
    body = E(14, 16, 10.5, 9.8)
    c.add(PG([(23, 14), (30, 8), (31, 15), (31, 17), (30, 24), (23, 18)]), wr)
    c.add(PG([(10, 8), (13, 3), (18, 6), (19, 9)]), pk)
    c.add(PG([(12, 24), (16, 29), (20, 24)]), pk)
    c.add(body, wh, edge='out')
    stripes = {(x, y) for (x, y) in body if ((x + y * 1 + (x // 4)) // 3) % 2 == 0 and True}
    # 소용돌이 줄무늬 (사탕처럼)
    sw = set()
    for (x, y) in body:
        d = math.hypot(x - 14, y - 16)
        a = math.atan2(y - 16, x - 14)
        if int(d / 3.0 + a / (2 * math.pi) * 3) % 2 == 0:
            sw.add((x, y))
    c.pat(sw, pk)
    c.add(PG([(14, 18), (20, 22), (19, 16)]), pk, edge='in')
    c.rays(c.p and {q for q in c.p if q[0] >= 24}, (23, 16), [-25, -10, 10, 25], .75)
    c.dot(30, 12, (255, 255, 255)); c.dot(29, 20, (255, 255, 255))
    c.eye(6, 13, 3)
    c.put({(3, 18), (4, 19)}, hx('#8a1a4a'))


@fish(10, 'f_tadpole', '진흙 개구리')
def _(c):
    r = R('#86a040', dk='#3e5a2a', lt='#b4cc5c')
    mud = R('#8a6438', dk='#4e321c', lt='#b48a52')
    belly = R('#d8e08c', dk='#9ea85a', lt='#f4f4b8')
    # 뒷다리
    c.add(PG([(22, 27), (31, 28), (31, 30), (22, 30)]), r, edge=None)
    c.add(E(21, 23, 5.2, 5), r, edge='out')
    # 몸 + 머리
    body = E(16, 20, 10.5, 7.5) | E(9, 19, 6.5, 5)
    c.add(body, r, edge='out')
    c.lighten({(x, y) for (x, y) in body if y >= 24 and x < 19}, .0)
    c.pat({(x, y) for (x, y) in body if y >= 23 and x < 19 and y <= 26}, belly)
    c.pat({(x, y) for (x, y) in E(21, 23, 5.2, 5) if x >= 17 and y >= 20} & set(), r)
    # 뒷다리 안쪽 선
    c.put(tube([(19, 20), (25, 21), (27, 26)], .5) & E(21, 23, 5.2, 5), r[0])
    # 앞다리
    c.add(tube([(11, 23), (9, 27)], 2.2, 1.6), r, edge='out')
    c.add(PG([(5, 28), (11, 28), (11, 30), (5, 30)]), r, edge='out')
    c.put({(7, 29), (9, 29)}, r[0])
    # 눈
    c.add(E(9, 13, 3.8, 3.6), r, edge='out')
    c.eye(7, 11, 4, ring=hx('#fff0a0'))
    # 입, 콧구멍
    c.put(tube([(1, 21), (6, 22), (11, 22), (13, 20)], .5), OUT)
    c.dot(3, 18, OUT)
    # 진흙 얼룩과 방울
    for (x, y, rx, ry) in ((16, 15, 3, 2), (21, 17, 2.2, 1.6), (13, 19, 1.4, 1.2), (26, 24, 1.4, 1.2), (24, 21, 1.2, 1)):
        c.pat(E(x, y, rx, ry) & body, mud)
    c.add(E(16, 15, 2.2, 1.5) & set(), mud)
    c.put({(5, 23), (4, 25), (4, 26)}, mud[1])


@fish(11, 'f_jelly', '젤리 해파리')
def _(c):
    bl = R('#ff7cc4', dk='#b83a96', lt='#ffb0e0', hi='#ffeaf8')
    ar = R('#c88cff', dk='#7c4cc0', lt='#e4c0ff')
    # 촉수/구강완
    for x, ph in ((8, 0), (11, 1), (21, 0), (24, 1)):
        pts = [(x, 14), (x + (1 if ph else -1), 18), (x + (-1 if ph else 1), 22), (x + (1 if ph else -1), 27), (x, 30)]
        c.add(tube(pts, .55, .5), ar, shade=False)
    for x, ph in ((13, 0), (16, 1), (19, 0)):
        pts = [(x, 15), (x + (2 if ph else -2), 19), (x + (-2 if ph else 2), 23), (x + (2 if ph else -2), 27)]
        c.add(tube(pts, 1.8, .7), ar, edge='out')
    dome = E(15.5, 14, 11.5, 11) & {(x, y) for x in range(N) for y in range(0, 15)}
    skirt = set()
    for cx in (6, 10, 15.5, 21, 25):
        skirt |= E(cx, 14.5, 2.9, 1.9)
    bell = dome | skirt | RC(5, 12, 26, 14)
    c.add(bell, bl, edge='out')
    # 속 무늬 (네잎 고리)
    for (x, y) in ((12, 8), (19, 8), (12, 11), (19, 11)):
        c.pat(E(x, y, 1.4, 1.3) & bell, R('#ffd0ec', dk='#e88ac8', lt='#fff0fa'))
    c.pat(E(7, 6, 1.4, 1) & bell | {(6, 7), (5, 8)}, R('#fff4fb'))
    c.pat({(x, 13) for x in range(6, 26)} & bell, bl, keep_tone=False) if False else None
    c.pat({(x, 13) for x in range(5, 27)} & bell, R('#d84aa8', dk='#8a2a78', lt='#f06cc0'))
    c.eye(12, 15, 2) if False else None


@fish(12, 'f_cray', '거미 가재')
def _(c):
    r = R('#7a2e5e', dk='#3c1840', lt='#a8467a')
    cl = R('#9a3a6a', dk='#4a1c48', lt='#c8588c')
    mk = R('#ff9a2a', dk='#d0561a', lt='#ffd05a')
    cx = 15.5
    # 거미 같은 다리
    legs = set()
    for sgn in (-1, 1):
        for (y0, kx, ky, ex, ey) in ((12, 8, 9, 3, 14), (15, 7.5, 13, 2, 20), (18, 8, 17, 3, 26), (21, 9, 22, 6, 30)):
            legs |= tube([(cx + sgn * 3.5, y0), (cx + sgn * kx, ky), (cx + sgn * (cx - ex), ey)], .6, .6, smooth=False)
    c.add(legs, r, shade=False)
    # 꼬리 부채
    fan = PG([(13, 27), (11, 31), (14, 31), (15, 29), (16, 31), (17, 29), (18, 31), (21, 31), (18, 27)])
    c.add(fan, cl, edge='out')
    c.rays(fan, (cx, 26), [70, 90, 110], .75)
    # 배 마디
    for i, (y, hw) in enumerate(((20, 4.2), (22, 4), (24, 3.6), (26, 3.2))):
        c.add(E(cx, y + .5, hw, 1.7), r, edge='out')
    # 집게
    for sgn in (-1, 1):
        arm = tube([(cx + sgn * 4, 12), (cx + sgn * 8, 9), (cx + sgn * 10, 6)], 1.5, 1.5)
        c.add(arm, cl, edge='out')
        claw = EL(cx + sgn * 11.5, 3.5, 4.8, 2.9, -90 if True else 0) | set()
        claw = E(cx + sgn * 10.5, 3.3, 3.4, 3.8) - PG([(cx + sgn * 10.5, 4), (cx + sgn * 11.5, -1), (cx + sgn * 9.5, -1)])
        c.add(claw, cl, edge='out')
    # 머리가슴
    thorax = E(cx, 14, 5.2, 7.2)
    c.add(thorax, r, edge='out')
    c.add(PG([(cx - 2, 7), (cx, 2), (cx + 2, 7)]), r, edge='out')
    # 모래시계 무늬
    c.pat(PG([(13, 12), (18, 12), (16, 15), (18, 18), (13, 18), (15, 15)]) & thorax, mk, keep_tone=False)
    # 눈 + 더듬이
    c.put(LN((cx - 2, 4), (cx - 5, 0), .5) | LN((cx + 2, 4), (cx + 5, 0), .5), cl[2])
    c.eye(11, 6, 2)
    c.eye(19, 6, 2)
    for q in ((14, 8), (17, 8), (15, 9), (16, 9)):
        c.dot(q[0], q[1], hx('#ff4a5a'))


@fish(13, 'f_conch', '마녀 모자 소라')
def _(c):
    sh_ = R('#f4cdb4', dk='#b8788a', lt='#fff0e0')
    pk = R('#e2607e', dk='#8e2a58', lt='#ff9aa8')
    hat = R('#6a3aa8', dk='#321a62', lt='#9468d8')
    gold = R('#ffd24a', dk='#c88a1a', lt='#fff09a')
    ec = hx('#5a2440')
    band = R('#e09468', dk='#a0504a', lt='#f8c090')
    W = [E(14, 23, 12.5, 7.2), E(16, 16.5, 8.6, 4.8), E(17.6, 11.4, 6, 3.6), E(18.6, 7.6, 4, 2.8)]
    # 아래 껍질부터 차례로 쌓아 올려 마디 선이 생겨요
    for i, w in enumerate(W):
        c.add(w, sh_, edge='out', ec=ec)
        c.pat(tube([(min(x for x, y in w) + 1, 0), ], .5) & set(), band) if False else None
    # 어깨 가시
    for (x, y, k) in ((4, 21, -1), (24, 21, 1), (8, 15, -1), (24, 15, 1), (12, 10, -1), (23, 10, 1)):
        c.add(PG([(x, y + 2), (x + k * 3, y - 1), (x - k * 1, y - 1)]), sh_, edge='out', ec=ec)
    # 마디마다 갈색 띠
    c.pat(tube([(8, 21), (14, 19), (22, 21)], .6) & set(c.p) - {(x, y) for (x, y) in E(16, 16.5, 8.6, 4.8)}, band)
    c.pat(tube([(10, 16), (16, 14.5), (23, 16)], .6) & E(16, 16.5, 8.6, 4.8), band)
    c.pat(tube([(13, 11), (18, 9.8), (22, 11)], .5) & E(17.6, 11.4, 6, 3.6), band)
    c.pat(tube([(10, 27), (17, 28), (24, 26)], .6) & E(14, 23, 12.5, 7.2), band)
    # 입구 (분홍 속살 + 하얀 입술)
    c.add(E(9, 25, 6.4, 4.6), sh_, edge='out', ec=ec)
    c.add(E(9, 25.4, 4.6, 3.2), pk, edge='out')
    c.pat({(x, y) for x in range(5, 9) for y in range(23, 26)} & set(c.p), R('#ff9aa8', dk='#c8587a', lt='#ffd0d4'))
    # 마녀 모자
    c.add(E(18.6, 5.2, 6, 1.6), hat, edge='out')
    c.add(PG([(15, 5), (17, 1), (19, 0), (21, 0), (22, 2), (22, 5)]), hat, edge='out')
    c.pat({(x, 4) for x in range(15, 23)} & set(c.p), gold, keep_tone=False)
    c.dot(18, 4, hat[0]); c.dot(19, 4, hat[0])
    c.dot(22, 0, hat[1]); c.dot(23, 1, hat[2]); c.dot(23, 2, hat[1])


@fish(14, 'f_lampshrimp', '등불 새우')
def _(c):
    r = R('#ffb27c', dk='#c8582e', lt='#ffd6a8')
    d = R('#ff8a5a', dk='#a8402e', lt='#ffb088')
    glow = R('#ffe45e', dk='#ffae2a', lt='#fff6b0', hi='#ffffff')
    # 더듬이 + 등불
    c.put(tube([(7, 10), (5, 6), (4, 3)], .5), r[0])
    c.put(tube([(9, 9), (9, 5), (12, 2), (15, 2)], .5), r[0])
    c.add(E(4, 3, 2.3, 2.6), glow, edge='out')
    c.put({(4, 2), (3, 2)}, glow[3])
    # 꼬리 부채
    fan = PG([(18, 23), (14, 26), (13, 30), (16, 30), (18, 28), (21, 29), (22, 25)])
    c.add(fan, d, edge='out')
    c.rays(fan, (20, 23), [110, 135, 160], .75)
    # 배 (아치형)
    abd = tube([(13, 11), (18, 9), (23, 12), (24, 18), (20, 23)], 4.8, 2.6)
    c.add(abd, r, edge='out')
    # 마디선
    for (x0, y0, x1, y1) in ((16, 5, 15, 13), (20, 6, 19, 14), (24, 9, 21, 16)):
        c.pat(LN((x0, y0), (x1, y1), .5) & abd, d)
    # 머리가슴
    head = E(10, 14, 6, 5.2)
    c.add(head, r, edge='out')
    c.add(PG([(5, 12), (2, 9), (6, 9), (9, 10)]), r, edge='out')
    # 다리
    for x in (7, 9, 11, 13):
        c.add(LN((x, 18), (x - 1, 22), .5), d, shade=False)
    for x in (18, 21):
        c.add(LN((x, 23), (x + 1, 26), .5), d, shade=False)
    c.eye(6, 12, 2)
    # 등불 점 (배 쪽 발광)
    for (x, y) in ((8, 17), (11, 18), (14, 16), (19, 15), (22, 18), (22, 14), (14, 12)):
        c.dot(x, y, glow[1])
    for (x, y) in ((8, 17), (14, 16), (22, 18)):
        c.dot(x, y, glow[3])


@fish(15, 'f_trout', '달빛 송어')
def _(c):
    r = R('#a6bde6', dk='#566aa8', lt='#d0def8')
    bk = R('#5a6cb0', dk='#2e3a78', lt='#7e92d4')
    fn = R('#8ea4d8', dk='#4a5a9c', lt='#b8caf0')
    mo = R('#ffe98a', dk='#e0b040', lt='#fff8c8')
    c.add(PG([(25, 14), (30, 9), (29, 14), (30, 18), (30, 23), (25, 19)]), fn)
    c.add(PG([(11, 11), (14, 7), (19, 11)]), fn)
    c.add(PG([(21, 11), (22, 9), (24, 12)]), bk)
    c.add(PG([(15, 21), (18, 24), (21, 20)]), fn)
    body = prof([(2, 15, 18.5), (4, 12.5, 20), (8, 11, 21.5), (14, 10.5, 22), (20, 12.5, 21), (25, 14.5, 19)])
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y <= 13 + (0 if x < 8 else 0)}, bk)
    c.pat({(x, 16) for x in range(11, 25)} & body, R('#f0a8c8', dk='#c0708e', lt='#ffd0e0'))
    c.pat({(x, 17) for x in range(11, 25)} & body, R('#f0a8c8', dk='#c0708e', lt='#ffd0e0'))
    for q in ((10, 12), (13, 13), (16, 12), (19, 13), (22, 14), (12, 14), (17, 14), (9, 14)):
        c.dot(q[0], q[1], OUT)
    c.add(PG([(8, 18), (12, 21), (13, 18)]), fn, edge='in')
    # 아가미 위 초승달
    cres = {(10, 12), (9, 12), (8, 13), (7, 14), (7, 15), (7, 16), (7, 17), (8, 18), (9, 19), (10, 19), (9, 13), (8, 14), (9, 18)}
    c.put(cres & body, mo[2])
    c.put({(8, 15), (8, 16), (9, 15), (9, 16), (9, 14), (9, 17), (10, 14), (10, 17), (10, 15), (10, 16)} & body, r[1])
    c.put({(7, 16), (7, 15), (8, 14), (8, 18)} & body, mo[1])
    c.eye(4, 14, 3)
    c.dot(2, 17, OUT)
    c.put({(24, 6), (27, 5), (4, 8)}, hx('#fff2a0'))


@fish(16, 'f_puffer', '눈알 복어')
def _(c):
    r = R('#d6e068', dk='#7a9a3a', lt='#f2f6a0')
    fn = R('#bcd05a', dk='#6a8a3a', lt='#e2eb86')
    cr = R('#fff6d0', dk='#d8c890', lt='#ffffff')
    cx, cy = 15, 16
    body = E(cx, cy, 11, 10.5)
    # 가시
    spikes = set()
    for a in range(0, 360, 30):
        rad = math.radians(a)
        ux, uy = math.cos(rad), math.sin(rad)
        px_, py_ = -uy, ux
        bx, by = cx + ux * 9.5 * 1.04, cy + uy * 9.0
        spikes |= PG([(bx + px_ * 1.6, by + py_ * 1.6), (cx + ux * 14.2, cy + uy * 13.6), (bx - px_ * 1.6, by - py_ * 1.6)])
    c.add(PG([(25, 14), (31, 11), (31, 21), (25, 18)]), fn)
    c.add(spikes, cr, edge=None, shade=True)
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y >= 19 and x > 4}, cr)
    c.pat(E(9, 22, 6, 2) & body, cr)
    # 앞지느러미
    c.add(E(17, 19, 2, 2.6), fn, edge='out')
    # 눈알들 (충혈된)
    def ball(x, y, big=False):
        if big:
            c.put(E(x, y, 3.2, 3.2), (255, 255, 255))
            c.put(E(x, y, 3.2, 3.2) & {(a, b) for a in range(N) for b in range(N) if (a == x - 3 or b == y + 3 or (a, b) == (x - 2, y + 2))}, hx('#e8a0a8'))
            c.put({(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)}, hx('#d83a4a'))
            c.put({(x - 1, y), (x, y)}, OUT)
            c.dot(x - 1, y - 1, (255, 255, 255))
        else:
            c.put(E(x, y, 2.2, 2.2, 1.0), (255, 255, 255))
            c.put({(x - 1, y), (x, y), (x - 1, y + 1)}, hx('#c0306a'))
            c.dot(x - 1, y, OUT)
    ball(7, 13, True)
    ball(15, 10)
    ball(20, 17)
    ball(11, 20)
    # 입 + 앞니
    c.put({(2, 18), (3, 19), (4, 19)}, OUT)
    c.put({(3, 20), (4, 20)}, (255, 255, 255))


@fish(17, 'f_ghostsquid', '유령 오징어')
def _(c):
    r = R('#e2eaff', dk='#8e9ce0', lt='#f8fbff')
    ar = R('#c6d4ff', dk='#7a88d0', lt='#eaf0ff')
    # 팔 (아래로 흐르는 유령 자락)
    for (x, ph) in ((10, 0), (13, 1), (16, 0), (19, 1), (22, 0)):
        s = 1 if ph else -1
        pts = [(x, 22), (x + s, 25), (x - s, 28), (x + s, 31)]
        c.add(fade(tube(pts, 1.4, .7), 99), ar, shade=False, edge=None) if False else None
        c.add(tube(pts, 1.5, .6), ar, shade=True, edge='out')
    c.add(fade(tube([(8, 21), (5, 25), (6, 29)], 1.2, .5), 99), ar) if False else c.add(tube([(8, 21), (5, 25), (6, 29)], 1.2, .5), ar, edge='out')
    c.add(tube([(24, 21), (27, 25), (26, 29)], 1.2, .5), ar, edge='out')
    # 지느러미
    c.add(PG([(16, 1), (25, 8), (22, 12), (17, 8)]), ar, edge='out')
    c.add(PG([(15, 1), (6, 8), (9, 12), (14, 8)]), ar, edge='out')
    mantle = PG([(15, 0), (20, 4), (22, 11), (21, 18), (19, 23), (12, 23), (10, 18), (9, 11), (11, 4)])
    c.add(mantle, r, edge='out')
    # 외투 가운데 선과 점
    c.pat({(15, y) for y in range(3, 12)}, ar)
    c.add(RC(8, 19, 23, 23) & mantle & set(), r)
    # 얼굴: 유령처럼 텅 빈 눈 + 입
    c.eye(10, 14, 4, ring=(255, 255, 255))
    c.eye(18, 14, 4, ring=(255, 255, 255))
    c.put({(15, 19), (16, 19), (15, 20), (16, 20)}, hx('#5a4a90'))


@fish(18, 'f_bonecat', '해골 메기')
def _(c):
    r = R('#eee0c0', dk='#9a8672', lt='#fff8e4')
    bn = R('#5c4a44', dk='#2c2024', lt='#8a7468')
    fn = R('#d8c8a4', dk='#8a7660', lt='#f4e8cc')
    c.add(PG([(25, 14), (30, 11), (30, 22), (25, 19)]), fn)
    c.add(PG([(11, 14), (13, 9), (17, 13)]), fn)
    c.add(PG([(13, 20), (15, 24), (24, 22), (25, 19)]), fn)
    body = prof([(3, 14, 20), (5, 12, 21), (10, 12, 21), (16, 13, 20), (21, 14.5, 19), (25, 15.5, 18.5)])
    c.add(body, r, edge='out')
    # 갈비뼈 + 척추
    c.pat({(x, 16) for x in range(11, 25)} & body, bn)
    for x in (12, 14, 16, 18, 20, 22):
        k = 0 if x < 17 else 1
        c.pat({(x, 14 + k), (x, 15), (x, 17), (x, 18 - k)} & body, bn)
    # 해골 얼굴
    c.pat(RC(3, 13, 9, 19) & body, R('#f8f0d8', dk='#b8a488', lt='#ffffff'))
    c.pat(E(6, 15, 2.7, 2.5) & body, bn, keep_tone=False)
    c.dot(5, 15, hx('#ff9a2a')); c.dot(6, 15, hx('#ffd05a')) if False else None
    c.put({(5, 14), (5, 15), (6, 15), (6, 14)}, hx('#241820'))
    c.dot(6, 15, hx('#ffb02a')); c.dot(5, 14, (255, 255, 255))
    c.dot(3, 16, bn[0])
    for x in range(3, 10):
        c.dot(x, 19, bn[0] if x % 2 else (255, 255, 255))
    for a_, b_ in (((3, 15), (0, 12)), ((4, 20), (0, 25)), ((3, 18), (0, 20)), ((6, 21), (3, 28))):
        c.put(LN(a_, b_, .5), r[1])
    c.put({(0, 12), (0, 25)}, fn[1]) if False else None
    c.add(PG([(14, 20), (16, 23), (20, 21)]), fn, edge='in') if False else None


@fish(19, 'f_betta', '꽃잎 베타')
def _(c):
    p1 = R('#ff7ab4', dk='#c03a86', lt='#ffa8d0', hi='#ffe0f0')
    p2 = R('#ff9a6a', dk='#d0503a', lt='#ffc090')
    body = R('#d0408c', dk='#7a2a6a', lt='#f070b8')
    # 꼬리 꽃잎들
    for ang, ln, wd, col in ((-52, 13, 6, p1), (-22, 15, 7, p2), (8, 15, 7, p1), (36, 14, 7, p2), (62, 11, 6, p1)):
        c.add(petal(19, 16, ang, ln, wd), col, edge='out')
    # 등/배 지느러미 꽃잎
    for ang, ln, wd, col in ((-112, 8, 5, p2), (-80, 9, 5, p1), (95, 9, 5, p1), (122, 8, 5, p2), (72, 9, 5, p2)):
        bx, by = (12, 11) if ang < 0 else (12, 20)
        c.add(petal(bx, by, ang, ln, wd), col, edge='out')
    b = prof([(3, 15, 18), (5, 12.5, 20), (9, 11.5, 21.5), (14, 12.5, 20.5), (19, 14.5, 18.5)])
    c.add(b, body, edge='out')
    c.pat({(x, y) for (x, y) in b if x % 3 == 0 and y % 3 == 0}, p1)
    c.add(petal(10, 18, 40, 6, 4), p1, edge='in')
    c.eye(5, 14, 3)
    c.dot(3, 17, hx('#5a1a4a'))


@fish(20, 'f_cloudray', '구름 가오리')
def _(c):
    r = R('#c4d8fc', dk='#6a84d4', lt='#eaf2ff', hi='#ffffff')
    cl = R('#ffffff', dk='#b8c6f0', lt='#ffffff')
    c.add(tube([(23, 16), (27, 16), (31, 15)], 1.3, .5, smooth=False), r, edge='out', shade=False)
    body = PG([(2, 16), (10, 8), (19, 2), (21, 8), (24, 12), (25, 16), (24, 20), (21, 24), (19, 30), (10, 24)])
    c.add(body, r, edge='out')
    # 몽실몽실 구름 무늬 (윤곽은 그대로, 안쪽에만)
    for puff in (E(11, 16, 2.6, 2.4) | E(15, 14, 3.4, 3) | E(19, 16, 3, 2.6) | E(15, 18, 5.4, 1.8),
                 E(15, 8.6, 3, 1.6) | E(12, 10, 2, 1.2) | E(19, 7, 1.6, 1.2), E(15, 23.4, 3, 1.6) | E(12, 22, 2, 1.2) | E(19, 25, 1.6, 1.2)):
        c.add(puff & body, cl, edge='out', ec=hx('#8aa0e4'), shade=True)
    c.pat({(x, y) for (x, y) in body if y >= 22 and x >= 12 and not (x, y) in set()}, R('#a8bcf0', dk='#6a84d4', lt='#c4d4fa')) if False else None
    c.eye(4, 11, 2)
    c.eye(4, 19, 2)
    c.dot(6, 14, hx('#ff9ac0')); c.dot(6, 18, hx('#ff9ac0'))


@fish(21, 'f_candleeel', '촛농 뱀장어')
def _(c):
    r = R('#f4a868', dk='#b0602e', lt='#ffd098')
    wx = R('#fffaf0', dk='#e6cfa0', lt='#ffffff')
    fl = R('#ffae2a', dk='#e0521a', lt='#ffe45e', hi='#fffbe0')
    fin = R('#e08a54', dk='#a04c34', lt='#f0a876')
    path = [(4, 17), (9, 12), (15, 11), (21, 16), (26, 21), (30, 19)]
    body = tube(path, 3.3, 1.5)
    c.add(tube([(8, 8), (13, 7), (19, 9), (25, 14), (29, 17)], 1.0, .8), fin, shade=False)
    c.add(tube([(15, 15), (20, 19), (25, 25), (29, 24)], 1.0, .8), fin, shade=False)
    c.add(body, r, edge='out')
    c.eye(4, 15, 2)
    c.put({(2, 19), (3, 19), (4, 19)}, hx('#9a5a2a'))
    # 등에서 녹아내려 몸을 타고 흐르는 촛농
    cap = {(x, y) for (x, y) in body if y <= min(yy for (xx, yy) in body if xx == x) + 1 and 7 <= x <= 22}
    c.pat(cap, wx)
    for (x, ln) in ((9, 4), (13, 5), (17, 4), (21, 3)):
        top = min(y for (xx, y) in body if xx == x)
        d = {(x, top + k) for k in range(ln)} | {(x + 1, top + k) for k in range(max(0, ln - 2))}
        c.pat(d & body, wx)
        c.dot(x, top + ln, wx[2])
    c.add(PG([(28, 18), (30, 11), (31, 15), (31, 20), (29, 21)]), fl)
    c.put({(30, 17), (30, 16), (30, 18)}, fl[3])
    c.dot(30, 13, fl[2])


@fish(22, 'f_cotton', '솜사탕 넙치')
def _(c):
    pk = R('#ff9ed0', dk='#d66aa8', lt='#ffd0e8', hi='#fff0f8')
    bl = R('#9ad8ff', dk='#5a9ee0', lt='#d0eeff')
    pu = R('#d0a8ff', dk='#9068d8', lt='#eadcff')
    cone = R('#fff4e8', dk='#d8b89a', lt='#ffffff')
    red = R('#ff6a8a', dk='#c03a62', lt='#ff9ab0')
    wh = R('#ffffff', dk='#fbe8ff', lt='#ffffff')
    # 종이 콘 꼬리
    cn = PG([(23, 14), (31, 9), (31, 23), (23, 18)])
    c.add(cn, cone, edge='out')
    for x in (26, 30):
        c.pat({(x, y) for y in range(6, 26)} & cn, red)
    # 솜사탕 몸통 (납작한 몽실 덩어리, 위아래 가장자리가 지느러미 술)
    puff = E(13, 16, 11, 7) | E(5.5, 15, 3.5, 4) | E(9, 10, 4, 3.4) | E(15, 9.5, 4.4, 3.4) | E(20.5, 12, 3.6, 3.4)         | E(8, 22, 4, 3.2) | E(14, 23, 4.4, 3.4) | E(20, 20, 3.8, 3.2)
    c.add(puff, pk, edge='out')
    c.pat({(x, y) for (x, y) in puff if x + y >= 29 and y >= 16}, bl)
    c.pat({(x, y) for (x, y) in puff if x + y >= 35}, pu)
    c.pat({(x, y) for (x, y) in puff if (x * 3 + y * 5) % 7 == 0 and y > 11 and x > 9}, wh)
    # 넙치 눈 두 개 (한쪽에 모여), 입
    c.eye(3, 12, 2)
    c.eye(6, 10, 2)
    c.put({(1, 18), (2, 19), (3, 19)}, hx('#a8407a'))


@fish(23, 'f_rtrout', '무지개 송어')
def _(c):
    cols = ['#ff4a5a', '#ff9a2a', '#ffe24a', '#58d05a', '#3aa8ff', '#8a5aff']
    base = R('#e6f0ff', dk='#8a96c8', lt='#ffffff')
    fn = R('#8ad0ff', dk='#4a88d0', lt='#c0ecff')
    c.add(PG([(25, 14), (30, 8), (28, 15), (30, 22), (25, 18)]), fn)
    c.add(PG([(10, 10), (13, 6), (18, 6), (21, 11)]), fn)
    c.add(PG([(20, 20), (24, 24), (21, 20)]), fn) if False else None
    c.add(PG([(14, 21), (17, 25), (21, 20)]), fn)
    body = prof([(3, 15, 19), (5, 11.5, 21), (9, 8.5, 23.5), (14, 8, 24), (19, 10.5, 22), (24, 14, 19)])
    c.add(body, base, edge='out')
    # 가로 무지개 띠 (몸 중간)
    for i, h in enumerate(cols):
        y = 11 + i * 2
        c.pat({(x, yy) for (x, yy) in body if yy in (y, y + 1) and x >= 8 and yy >= 10}, R(h))
    c.pat({(x, y) for (x, y) in body if x < 8 and 12 <= y <= 19 and False}, base)
    c.pat({(x, y) for (x, y) in body if y <= 11 and x >= 6}, R('#6a82c8', dk='#3a4a88', lt='#8ea4e4'))
    c.add(PG([(8, 19), (12, 22), (13, 19)]), fn, edge='in')
    c.pat({(25, 11), (27, 10), (26, 13)} & set(c.p), R('#ff9a2a'))
    c.eye(4, 13, 3)
    c.dot(2, 17, OUT)
    c.dot(7, 11, hx('#ffffff'))


@fish(24, 'f_maplebass', '단풍 쏘가리')
def _(c):
    r = R('#e9a43a', dk='#a05a22', lt='#ffd070')
    rd = R('#c8362a', dk='#7a1c2a', lt='#e86a3a')
    fn = R('#d86a2a', dk='#8a3a22', lt='#f09a40')
    # 단풍잎 꼬리
    leaf = PG([(23, 16), (24, 12), (22, 9), (26, 10), (27, 5), (29, 9), (31, 8), (30, 12), (31, 16), (30, 18), (31, 23), (28, 21), (28, 25), (26, 21), (23, 22), (24, 18)])
    c.add(leaf, rd, edge='out')
    c.put(LN((23, 16), (30, 16), .5) | LN((26, 16), (27, 7), .5) | LN((26, 16), (29, 22), .5) | LN((25, 16), (28, 11), .5), rd[2])
    # 가시 등지느러미
    spikes = set()
    for x in range(9, 22, 2):
        top = 6 + abs(x - 14) * 0.45
        spikes |= PG([(x - 1, 11), (x, top), (x + 1, 11)])
    c.add(spikes, fn, edge='out')
    c.add(PG([(15, 21), (17, 24), (21, 21)]), fn)
    body = prof([(2, 16, 19), (4, 12, 21), (8, 10, 23), (14, 10, 23), (19, 12, 21.5), (23, 14.5, 19)])
    c.add(body, r, edge='out')
    # 표범 무늬 단풍 얼룩
    for q in ((10, 13), (11, 13), (10, 14), (14, 16), (15, 16), (15, 17), (17, 13), (18, 13), (17, 12), (12, 19), (13, 19), (12, 20), (19, 17), (20, 17), (19, 18), (8, 17), (9, 18), (7, 12), (21, 14)):
        c.pat({q} & body, rd)
    # 커다란 입
    c.put({(x, 18) for x in range(2, 8)} | {(7, 17), (8, 16)}, OUT)
    c.put({(3, 19), (5, 19)}, (255, 255, 255))
    c.add(PG([(8, 19), (12, 22), (13, 19)]), fn, edge='in')
    c.eye(5, 13, 3)


@fish(25, 'f_weel', '늑대 장어')
def _(c):
    r = R('#8a90b8', dk='#464c78', lt='#b8bede')
    fin = R('#6a7098', dk='#383e66', lt='#9aa0c8')
    path = [(11, 14), (15, 17), (20, 22), (25, 22), (30, 18)]
    body = tube(path, 3.4, 1.4)
    c.add(tube([(12, 10), (17, 12), (22, 17), (27, 17), (30, 15)], 1.0, .8), fin, shade=False)
    c.add(tube([(15, 21), (20, 26), (25, 27), (29, 23)], 1.0, .8), fin, shade=False)
    c.add(body, r, edge='out')
    c.pat(tube([(12, 16), (17, 20), (22, 23)], .5) & body, fin)
    # 늑대 머리
    head = E(8, 13, 5.2, 4.8)
    snout = PG([(1, 15), (4, 12), (8, 13), (9, 18), (2, 18)])
    c.add(head | snout, r, edge='out')
    c.add(PG([(4, 10), (4, 4), (8, 9)]), r, edge='out')
    c.add(PG([(9, 9), (12, 4), (13, 11)]), r, edge='out')
    c.dot(5, 8, hx('#e89ab8')); c.dot(11, 8, hx('#e89ab8'))
    c.put({(1, 17), (2, 17)}, OUT)
    c.put({(x, 17) for x in range(2, 9)}, OUT)
    c.put({(3, 18), (6, 18)}, (255, 255, 255))
    c.dot(1, 15, OUT)
    c.eye(6, 11, 2)
    c.dot(7, 11, hx('#ffe35a')) if False else None
    c.lighten({(7, 12), (7, 13)}, 0) if False else None


@fish(26, 'f_sweet', '안개 은어')
def _(c):
    r = R('#a6cdc0', dk='#4e7a86', lt='#d4eee0')
    fn = R('#8ab6b0', dk='#487480', lt='#bce0d4')
    mist = R('#f4f8ff', dk='#c0cce4', lt='#ffffff')
    c.add(PG([(23, 15), (30, 9), (27, 16), (30, 23), (23, 17)]), fn)
    c.add(PG([(10, 12), (13, 8), (17, 12)]), fn)
    c.add(PG([(18, 13), (20, 11), (22, 14)]), fn)
    c.add(PG([(13, 20), (16, 23), (20, 19)]), fn)
    body = prof([(2, 16, 18), (4, 13.5, 19.5), (8, 12, 20.5), (14, 12, 20.5), (19, 13.5, 19), (23, 15, 18)])
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y <= 14 and x >= 6}, R('#6a9890', dk='#386068', lt='#8cb8ae'))
    c.pat({(5, 15), (6, 15), (5, 16), (6, 16), (7, 16)} & body, R('#ffe070', dk='#d09a30', lt='#fff4b0'))
    c.add(PG([(8, 18), (11, 20), (12, 18)]), fn, edge='in')
    c.eye(3, 14, 3)
    # 안개 (몽글몽글 구름 조각)
    for (x, y, k) in ((7, 25, 1.0), (15, 26.5, 1.2), (24, 25, 1.0), (27, 5, .8), (5, 7, .9)):
        cloud = E(x, y, 3.2 * k, 2.2 * k) | E(x + 3 * k, y + .5, 2.6 * k, 1.8 * k) | E(x - 3 * k, y + .6, 2.4 * k, 1.6 * k)
        cloud = {(qx, qy) for (qx, qy) in cloud if qy >= y - 1 or (qx + qy) % 2 == 0}
        c.add(cloud, mist, edge=None)
    c.eye(3, 14, 3)


@fish(27, 'f_mushflat', '버섯 가자미')
def _(c):
    r = R('#c4a070', dk='#76563a', lt='#e6cc9c')
    fn = R('#a88050', dk='#664a32', lt='#cca878')
    cap = R('#e0382e', dk='#8e1c3a', lt='#ff6a48')
    cap2 = R('#b0703a', dk='#6a3e22', lt='#d89a5c')
    stem = R('#f4e8cc', dk='#b49c80', lt='#ffffff')
    outer = PG([(1, 21), (6, 15), (14, 12), (22, 13), (26, 18), (27, 24), (22, 29), (13, 30), (6, 28)])
    c.add(outer, fn, edge='out')
    c.add(PG([(26, 19), (31, 17), (31, 27), (26, 25)]), fn, edge='out')
    ringfin = outer - PG([(3, 21), (8, 17), (14, 14), (21, 15), (24, 19), (25, 24), (21, 27), (13, 28), (8, 26)])
    for k in range(0, 360, 16):
        ang = math.radians(k)
        c.pat(LN((14 + math.cos(ang) * 8, 21 + math.sin(ang) * 6), (14 + math.cos(ang) * 16, 21 + math.sin(ang) * 11), .5) & ringfin, R('#7a5636', dk='#4a3422', lt='#8a6a44'), keep_tone=False)
    inner = PG([(3, 21), (8, 17), (14, 14), (21, 15), (24, 19), (25, 24), (21, 27), (13, 28), (8, 26)])
    c.add(inner, r, edge='out')
    for q in ((8, 23), (11, 26), (16, 24), (21, 24), (13, 21), (19, 20), (24, 22), (9, 19), (17, 27)):
        c.pat({q, (q[0] + 1, q[1])} & set(c.p), fn)
    c.pat({(15, 20), (16, 20), (22, 18), (12, 24), (20, 26)} & set(c.p), R('#e8d4a8', dk='#b09468', lt='#fff0c8'))
    c.eye(3, 19, 2)
    c.eye(6, 17, 2)
    c.put({(1, 23), (2, 24), (3, 24)}, OUT)
    # 버섯 두 개
    c.add(RC(12, 11, 14, 17), stem, edge='out')
    c.add(E(13, 11, 6.5, 4.4) & {(x, y) for x in range(N) for y in range(0, 12)}, cap, edge='out')
    c.pat({(9, 8), (11, 6), (13, 9), (15, 7), (17, 10), (12, 10)} & set(c.p), R('#fff3e0', dk='#e8c8c0', lt='#ffffff'))
    c.add(RC(21, 14, 22, 18), stem, edge='out')
    c.add(E(21.5, 14, 4, 3) & {(x, y) for x in range(N) for y in range(0, 15)}, cap2, edge='out')
    c.dot(20, 12, stem[2])


@fish(28, 'f_angler', '호박등 아귀')
def _(c):
    r = R('#5a4890', dk='#2c2058', lt='#8670c0')
    fn = R('#483a7c', dk='#241a4c', lt='#6a58a4')
    pk = R('#ff8a1e', dk='#c4521a', lt='#ffb43a', hi='#ffe28a')
    gl = R('#ffe85a', dk='#ffb82a', lt='#fff8b0')
    tooth = R('#ffffff', dk='#d8d0e8')
    c.add(PG([(25, 15), (31, 11), (31, 23), (25, 20)]), fn)
    c.add(PG([(14, 11), (16, 8), (22, 11)]), fn)
    c.add(PG([(14, 26), (18, 30), (22, 25)]), fn)
    body = E(16, 19, 11.5, 8.5) | E(8, 19, 6, 6)
    c.add(body, r, edge='out')
    # 큰 입 + 이빨
    c.put({(x, 21) for x in range(1, 12)}, OUT)
    c.put({(x, 22) for x in range(1, 6)}, OUT)
    for x in (2, 4, 6, 8, 10):
        c.add(PG([(x, 20), (x + 1, 20), (x, 17 if x % 4 else 18)]) if False else {(x, 20), (x, 19)}, tooth, shade=False)
    for x in (3, 5, 7, 9):
        c.dot(x, 22, tooth[0])
    c.put({(1, 20), (2, 20)}, OUT) if False else None
    c.add(PG([(14, 18), (18, 22), (19, 17)]), fn, edge='in')
    c.eye(8, 14, 3, ring=hx('#ffe85a'))
    # 낚싯대 + 호박등
    c.put(tube([(11, 11), (9, 5), (7, 3), (5, 5)], .6), OUT)
    c.put(tube([(11, 11), (9, 5), (7, 3), (5, 5)], .5) , hx('#c8a0ff'))
    c.add(E(4.5, 7, 4, 3.4), pk, edge='out')
    c.pat({(x, y) for (x, y) in E(4.5, 7, 4, 3.4) if x in (3, 6)}, R('#d96a14', dk='#a44412'))
    c.add(RC(4, 3, 5, 3), R('#4a9a3a'), edge=None, shade=False)
    # 잭오랜턴 얼굴
    c.put({(3, 6), (6, 6), (4, 6) if False else (3, 6), (4, 8), (5, 8), (3, 8), (6, 8)}, gl[0]) if False else None
    c.put({(3, 6), (6, 6)}, gl[2]); c.put({(4, 8), (5, 8), (3, 7), (6, 7)}, gl[1])
    c.dot(4, 7, gl[2]); c.dot(5, 7, gl[2])


@fish(29, 'f_piranha', '뱀파이어 피라냐')
def _(c):
    r = R('#8e9ab8', dk='#464e78', lt='#c0cae0')
    rd = R('#d02a4a', dk='#7a1438', lt='#ff5a6a')
    cape = R('#3a2058', dk='#1c1030', lt='#5a3a8a')
    fn = R('#6a5a98', dk='#342a5a', lt='#8a7ab8')
    c.add(PG([(24, 14), (31, 9), (29, 16), (31, 23), (24, 19)]), fn)
    c.add(PG([(12, 10), (14, 7), (20, 10), (22, 14)]), fn)
    # 망토 깃 (머리 뒤로 높이 솟은 깃)
    c.add(PG([(9, 5), (11, 12), (13, 24), (6, 28), (9, 19), (4, 15)]) & set() | PG([(10, 4), (13, 12), (14, 26), (8, 26), (10, 18)]), cape, edge='out')
    c.add(PG([(12, 6), (14, 13), (15, 25), (11, 25), (12, 18)]), rd, edge='out') if False else None
    body = prof([(2, 16, 21), (4, 11.5, 24), (8, 9.5, 25.5), (13, 9, 26), (18, 10.5, 24.5), (22, 13.5, 20)])
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y >= 21}, rd)
    c.add(PG([(10, 5), (13, 11), (14, 26), (16, 26), (16, 8), (13, 3)]) & set(), cape)
    # 깃 안쪽 붉은 안감
    collar = PG([(13, 3), (17, 9), (17, 12), (13, 10)])
    c.add(PG([(9, 3), (13, 10), (12, 13), (8, 10)]), cape, edge='out')
    c.add(PG([(14, 4), (17, 10), (16, 13), (13, 10)]), cape, edge='out')
    c.pat({(10, 6), (11, 8), (14, 6), (15, 8), (14, 9)} & set(c.p), rd)
    # 아래턱 + 이빨 + 송곳니
    c.put({(x, 20) for x in range(2, 11)}, OUT)
    for x in range(3, 10, 2):
        c.add({(x, 19), (x, 18)}, R('#ffffff', dk='#d8d0e8'), shade=False)
    c.add({(3, 21), (3, 22), (3, 23)} | {(8, 21), (8, 22), (8, 23)}, R('#ffffff', dk='#d8d0e8'), shade=False)
    c.eye(5, 13, 3, ring=hx('#ff6a7a'))
    c.add(PG([(13, 18), (17, 22), (18, 17)]), fn, edge='in')


@fish(30, 'f_octopus', '마법 문어')
def _(c):
    r = R('#a468e8', dk='#5a2ea0', lt='#ce9cff')
    gl = R('#ffe45e', dk='#ffae2a', lt='#fff6b0')
    # 여덟 다리 (둥글게 말린 모습)
    arms = [
        [(9, 15), (5, 19), (3, 24), (6, 28), (9, 26)],
        [(11, 17), (8, 22), (8, 27), (11, 30)],
        [(14, 18), (12, 24), (14, 30)],
        [(17, 18), (19, 24), (17, 30)],
        [(20, 17), (23, 22), (23, 27), (20, 30)],
        [(22, 15), (26, 19), (28, 24), (25, 28), (22, 26)],
    ]
    for pts in arms:
        c.add(tube(pts, 2.6, .8), r, edge='out')
    c.put({(5, 22), (4, 24), (9, 25), (8, 28), (13, 25), (18, 25), (22, 24), (23, 27), (27, 22)}, hx('#e6c8ff'))
    # 마법봉을 든 팔
    c.add(tube([(23, 12), (27, 9), (28, 5)], 1.8, .9), r, edge='out')
    c.add(LN((28, 5), (30, 1), .55), hx('#c8a050'))
    for q in ((30, 0), (29, 1), (31, 1), (30, 2), (31, 0)):
        c.dot(q[0], q[1], gl[1])
    # 머리 (큰 둥근 머리)
    head = E(15.5, 10, 9, 8.8)
    c.add(head, r, edge='out')
    # 별 무늬
    def star(x, y):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & head, gl[1])
        c.dot(x, y, gl[2])
    star(15, 4); star(20, 8); star(11, 10); star(18, 14)
    c.dot(9, 5, gl[1]); c.dot(22, 4, gl[1])
    c.eye(8, 12, 4, ring=(255, 255, 255))
    c.eye(16, 12, 4, ring=(255, 255, 255))
    c.dot(12, 16, hx('#6a2ea0')); c.dot(13, 16, hx('#6a2ea0'))
    c.dot(6, 15, hx('#ff9ac0')); c.dot(21, 15, hx('#ff9ac0'))


@fish(31, 'f_starfish', '별사탕 불가사리')
def _(c):
    cols = [R('#ff8ab8', dk='#c04a86', lt='#ffbcd8'), R('#ffe070', dk='#d89a2a', lt='#fff4b0'), R('#7ad8f8', dk='#3a8cd0', lt='#bcecff'),
            R('#8ae088', dk='#3a9a58', lt='#c0f4b8'), R('#c8a0ff', dk='#8458d0', lt='#e6d4ff')]
    cx, cy = 16, 17.5
    tips = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        tips.append((cx + math.cos(a) * 14, cy + math.sin(a) * 14))
    arms = []
    for i, (tx, ty) in enumerate(tips):
        m = tube([(cx, cy), (tx, ty)], 4.2, .9, smooth=False)
        arms.append(m)
    # 팔마다 색을 다르게 (콘페이토처럼)
    for i in (0, 1, 2, 3, 4):
        c.add(arms[i], cols[i], edge='out')
    c.add(E(cx, cy, 5.2, 5.2), cols[0], edge=None)
    c.pat(E(cx, cy, 5.2, 5.2), R('#ff9cc4', dk='#d0609a', lt='#ffd0e4'))
    # 설탕 알갱이
    for i, (tx, ty) in enumerate(tips):
        for t in (.45, .7):
            x = int(round(cx + (tx - cx) * t)); y = int(round(cy + (ty - cy) * t))
            c.dot(x, y, (255, 255, 255))
    for q in ((14, 15), (18, 15), (16, 20), (13, 19), (19, 19)):
        c.dot(q[0], q[1], (255, 255, 255))
    c.eye(13, 16, 2)
    c.eye(17, 16, 2)
    c.put({(15, 19), (16, 19)}, hx('#b04a7a'))


@fish(32, 'f_goby', '부엉이 망둥이')
def _(c):
    r = R('#b89868', dk='#6e5238', lt='#dcc490')
    fn = R('#a07c4e', dk='#5e422c', lt='#c4a070')
    fc = R('#f2e4c0', dk='#b09c78', lt='#fff8e0')
    yl = R('#ffd23a', dk='#d89a1a', lt='#fff08a')
    c.add(PG([(23, 15), (30, 11), (31, 14), (31, 20), (30, 22), (23, 19)]), fn)
    c.add(PG([(13, 12), (15, 8), (21, 9), (23, 14)]), fn)
    body = prof([(3, 13, 21), (5, 9, 24), (9, 8, 25.5), (14, 10.5, 25), (19, 13, 22), (24, 15, 19.5)])
    c.add(body, r, edge='out')
    # 깃털 무늬 (V자)
    for (x, y) in ((14, 16), (18, 17), (12, 20), (16, 21), (20, 19)):
        c.pat({(x - 1, y - 1), (x, y), (x + 1, y - 1)} & body, fn)
    c.lighten({(x, y) for (x, y) in body if y >= 22 and x < 16}, .25)
    # 부엉이 얼굴판 + 깃귀
    c.add(PG([(3, 10), (4, 5), (8, 9)]), fn, edge='out')
    c.add(PG([(9, 9), (12, 4), (14, 10)]), fn, edge='out')
    face = E(7.5, 15, 6, 5.8)
    c.add(face, fc, edge='out')
    c.eye(3, 12, 4, ring=yl[1])
    c.eye(8, 12, 4, ring=yl[1])
    # 부리
    c.add(PG([(1, 18), (4, 16), (5, 20)]), yl, edge='out')
    c.add(PG([(6, 19), (10, 22), (12, 19)]), fn, edge='in')
    c.add(PG([(12, 20), (16, 25), (18, 21)]), fn, edge='in') if False else None


@fish(33, 'f_shrimp', '수정 새우')
def _(c):
    r = R('#9ae0ff', dk='#4a88d8', lt='#d4f4ff', hi='#ffffff')
    pk = R('#ffa8e0', dk='#c860b0', lt='#ffd6f2')
    # 더듬이
    c.put(tube([(5, 13), (3, 8), (1, 4)], .5), r[2])
    c.put(tube([(7, 12), (7, 6), (10, 2), (15, 1)], .5), r[2])
    # 꼬리 부채
    fan = PG([(24, 19), (27, 17), (31, 19), (31, 25), (28, 26), (25, 24)])
    c.add(fan, pk, edge='out')
    c.rays(fan, (24, 21), [10, 35, 60], .78)
    # 배 마디 (곧게 뻗다 아래로 굽음)
    abd = tube([(11, 14), (17, 14), (22, 16), (25, 21)], 4.4, 2.6)
    c.add(abd, r, edge='out')
    for (x0, y0, x1, y1) in ((14, 9, 14, 19), (18, 9, 18, 19), (22, 12, 21, 20)):
        c.pat(LN((x0, y0), (x1, y1), .5) & abd, pk)
    # 머리가슴 + 톱니 뿔
    head = E(8, 15, 6, 5)
    c.add(head, r, edge='out')
    c.add(PG([(4, 12), (0, 9), (5, 9), (8, 10)]), pk, edge='out')
    # 다리
    for x in (6, 8, 10, 12):
        c.add(LN((x, 19), (x - 1, 23), .5), pk, shade=False)
    for x in (15, 19):
        c.add(LN((x, 18), (x, 22), .5), pk, shade=False)
    c.eye(4, 13, 2)
    # 수정 면
    c.pat(PG([(10, 11), (15, 11), (12, 16)]) & set(c.p), pk) if False else None
    c.put({(11, 12), (12, 13), (13, 12), (12, 12)} & set(c.p), r[3])
    c.put({(19, 11), (20, 12), (18, 12)} & set(c.p), r[3])
    for (x, y) in ((24, 7), (28, 12), (3, 22)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(34, 'f_ribbonmoray', '리본 곰치')
def _(c):
    r = R('#d86a3a', dk='#843018', lt='#f89a58')
    yl = R('#ffd25a', dk='#d89a2a', lt='#fff0a0')
    rb = R('#ff5aa0', dk='#b02a70', lt='#ff9ac8')
    fin = R('#a84a2a', dk='#602a1a', lt='#c8683a')
    path = [(6, 16), (11, 13), (17, 15), (22, 20), (27, 20), (30, 16)]
    body = tube(path, 4.6, 1.8)
    c.add(tube([(10, 9), (16, 10), (22, 15), (27, 15), (30, 13)], 1.1, .8), fin, shade=False)
    c.add(tube([(16, 20), (21, 25), (27, 26)], 1.1, .8), fin, shade=False)
    c.add(body, r, edge='out')
    # 노란 점무늬
    for q in ((13, 12), (16, 11), (18, 15), (21, 18), (24, 19), (26, 18), (15, 17), (19, 12), (11, 17)):
        c.pat({q, (q[0] + 1, q[1])} & body, yl)
    # 머리: 큰 입
    head = E(6, 15, 5.5, 5)
    c.add(head, r, edge='out')
    c.put(tube([(1, 16), (6, 18), (11, 17)], .5), OUT)
    for x in (2, 4, 6, 8):
        c.dot(x, 17, (255, 255, 255))
    c.dot(3, 19, (255, 255, 255)); c.dot(6, 19, (255, 255, 255))
    c.dot(1, 14, OUT)
    c.put({(2, 12), (2, 11)}, r[2])
    c.eye(5, 12, 2)
    # 리본 (목에 묶은 나비매듭)
    band = {(x, y) for (x, y) in body | head if 11 <= x <= 12}
    c.add(band, rb, edge='out')
    lo = PG([(11, 18), (6, 15), (7, 21), (11, 20)])
    ro = PG([(12, 18), (17, 15), (17, 21), (12, 20)])
    c.add(lo, rb, edge='out')
    c.add(ro, rb, edge='out')
    c.add(E(11.5, 19, 1.6, 1.6), rb, edge='out')
    c.add(PG([(10, 20), (8, 25), (11, 23)]) | PG([(13, 20), (15, 25), (12, 23)]), rb, edge='out')


@fish(35, 'f_bream', '루비 도미')
def _(c):
    r = R('#dc2a44', dk='#7a1034', lt='#ff6a74', hi='#ffc8cc')
    fn = R('#b81c3c', dk='#6a0c2e', lt='#e04a58')
    # 긴 가시 등지느러미 + 꼬리
    c.add(PG([(24, 14), (31, 8), (29, 15), (31, 23), (24, 19)]), fn)
    sp = set()
    for x in range(8, 22, 2):
        sp |= PG([(x - 1, 9), (x, 3 + abs(x - 14) // 2), (x + 1, 9)])
    sp |= PG([(7, 10), (22, 10), (22, 12), (7, 12)])
    c.add(sp, fn, edge='out')
    c.add(PG([(14, 24), (16, 28), (21, 24), (20, 22)]), fn)
    body = prof([(2, 15, 18.5), (4, 11.5, 21), (7, 8.5, 24.5), (12, 7.5, 26), (17, 9, 25), (21, 11.5, 22), (24, 14, 19)])
    c.add(body, r, edge='out')
    # 보석 면 (마름모 분할선)
    fac = R('#ff9aa4', dk='#c8344c', lt='#ffd6d8')
    for pts in (((7, 16), (12, 10), (17, 16), (12, 23)), ((12, 16), (17, 11), (22, 16), (17, 22))):
        for i in range(4):
            a_, b_ = pts[i], pts[(i + 1) % 4]
            c.pat(LN(a_, b_, .5) & body, fac)
    c.pat({(12, 10), (11, 12), (12, 12), (10, 13), (17, 11), (16, 13)} & body, R('#ffe4e4', dk='#ffa8b0', lt='#ffffff'))
    c.add(PG([(10, 19), (14, 24), (15, 20)]), fn, edge='in')
    c.eye(4, 13, 3)
    c.put({(2, 17), (3, 18)}, hx('#5a0a2a'))
    c.dot(9, 14, (255, 255, 255))


@fish(36, 'f_seahorse', '유령 해마')
def _(c):
    r = R('#dde6ff', dk='#8494d8', lt='#f6f9ff')
    fn = R('#bccaf8', dk='#7080d0', lt='#e4ecff')
    # 등지느러미 (부채)
    fin = PG([(16, 12), (22, 14), (22, 20), (17, 20)])
    c.add(fade(fin, 21), fn)
    c.rays(fin, (16, 16), [-10, 10, 30], .8)
    # 꼬리 (돌돌 말림)
    tail = tube([(15, 21), (15, 25), (11, 28), (7, 26), (8, 22), (11, 22), (11, 24)], 2.8, 1.0)
    c.add(tail, r, edge='out')
    # 몸통 (배가 불룩)
    body = tube([(12, 8), (15, 12), (16, 17), (15, 22)], 3.0, 3.2) | E(14.5, 16.5, 4.8, 5.4)
    c.add(body, r, edge='out')
    # 머리 + 긴 주둥이 + 갈기
    head = E(10, 8, 4.2, 3.8)
    c.add(head, r, edge='out')
    c.add(tube([(7, 9), (1, 10)], 1.4, 1.1, smooth=False), r, edge='out')
    c.add(PG([(8, 5), (9, 1), (11, 5)]) | PG([(11, 5), (13, 2), (14, 6)]) | PG([(13, 7), (17, 5), (15, 10)]), fn, edge='out')
    # 마디 무늬
    for y in (13, 15, 17, 19, 21):
        c.pat({(x, y) for (x, y) in body if x >= 12} - {(12, y)}, fn) if False else None
    for y in (14, 17, 20):
        c.pat({(x, y) for (x, y) in body}, R('#b6c4f4', dk='#6c7cd0', lt='#d8e2ff'))
    c.eye(9, 6, 3, ring=(255, 255, 255))
    c.dot(1, 10, hx('#5a4a90'))
    # 배 주머니 빛
    for (x, y) in ((24, 5), (27, 9), (4, 20), (3, 26)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(37, 'f_pumpray', '호박 쥐가오리')
def _(c):
    r = R('#f6902a', dk='#b0521c', lt='#ffbc4a', hi='#ffe08a')
    d = R('#d96a1a', dk='#8e3a1a', lt='#f79a2a')
    g = R('#5fae3a', dk='#2f6d2c', lt='#92d65a')
    c.add(tube([(21, 16), (26, 17), (31, 20)], 1.2, .5, smooth=False), d, edge='out', shade=False)
    wings = PG([(4, 16), (10, 11), (17, 5), (25, 1), (23, 8), (21, 13), (23, 16), (21, 19), (23, 24), (25, 31), (17, 27), (10, 21)])
    c.add(wings, d, edge='out')
    # 머리 지느러미 (뿔 두 개)
    c.add(PG([(0, 11), (6, 12), (6, 15), (2, 14)]), d, edge='out')
    c.add(PG([(0, 21), (6, 20), (6, 17), (2, 18)]), d, edge='out')
    # 호박 몸통
    pk = E(14, 16, 9.5, 9.5)
    c.add(pk, r, edge='out')
    for x, h in ((8, 4), (11, 7), (14, 9), (17, 7), (20, 4)):
        c.pat(tube([(x, 16 - h), (x - 1.5 if x < 14 else x + 1.5 if x > 14 else x, 16), (x, 16 + h)], .5) & pk, d)
    # 꼭지
    c.add(PG([(13, 8), (13, 5), (16, 4), (16, 9)]), g, edge='out')
    c.add(tube([(16, 5), (19, 3), (19, 6)], .5), g[1], shade=False)
    c.eye(5, 11, 2)
    c.eye(5, 19, 2)
    c.put({(7, 15), (7, 17)}, hx('#7a2a10'))


@fish(38, 'f_bolt', '번개 뱀장어')
def _(c):
    r = R('#3a5ad0', dk='#1c2a78', lt='#6a8af0')
    fin = R('#58c8f8', dk='#2a78c8', lt='#a0e8ff')
    yl = R('#ffe83a', dk='#e0a81a', lt='#fff8a0', hi='#ffffff')
    path = [(4, 15), (9, 9), (15, 12), (20, 20), (25, 21), (30, 14)]
    body = tube(path, 3.2, 1.3)
    c.add(tube([(8, 5), (14, 8), (19, 16), (25, 17), (30, 11)], .9, .7), fin, shade=False)
    c.add(tube([(10, 14), (14, 17), (18, 25), (24, 26)], .9, .7), fin, shade=False)
    c.add(body, r, edge='out')
    # 노란 번개 지그재그 줄무늬
    pts = spline(path, 10)
    zig = []
    for i in range(0, len(pts), 4):
        px_, py_ = pts[i]
        nx, ny = (pts[min(i + 1, len(pts) - 1)][0] - px_, pts[min(i + 1, len(pts) - 1)][1] - py_)
        L = math.hypot(nx, ny) or 1
        off = 1.2 if (i // 4) % 2 == 0 else -1.2
        zig.append((px_ - ny / L * off, py_ + nx / L * off))
    zz = set()
    for i in range(1, len(zig) - 1):
        zz |= LN(zig[i - 1], zig[i], .5)
    c.pat(zz & body, yl, keep_tone=False)
    c.eye(4, 12, 2)
    c.put({(2, 16), (3, 16)}, hx('#101a58'))
    # 스파크
    for (x, y) in ((1, 5), (8, 2), (28, 5), (24, 28)):
        c.put({(x, y), (x + 1, y + 1), (x + 1, y + 2), (x + 2, y + 3)} | {(x + 2, y + 1)}, yl[1])
        c.dot(x, y, yl[3])


@fish(39, 'f_gold', '황금 잉어')
def _(c):
    r = R('#ffc928', dk='#c47a14', lt='#ffe870', hi='#fffbd0')
    fn = R('#f08a1c', dk='#a04a14', lt='#ffc048')
    sc = R('#ffb020', dk='#b86a14', lt='#ffd860')
    # 너울거리는 꼬리 (두 갈래 베일)
    t1 = PG([(23, 15), (28, 6), (31, 8), (31, 14), (29, 17), (26, 17)])
    t2 = PG([(23, 17), (26, 17), (29, 17), (31, 20), (31, 26), (28, 28), (23, 19)])
    c.add(t1, fn, edge='out')
    c.add(t2, fn, edge='out')
    c.rays(t1, (23, 16), [-60, -40, -20, 0], .78)
    c.rays(t2, (23, 17), [60, 40, 20, 0], .78)
    c.add(PG([(10, 11), (12, 7), (18, 7), (22, 10), (22, 14), (14, 13)]), fn, edge='out')
    c.add(PG([(14, 22), (17, 26), (21, 22)]), fn)
    body = prof([(3, 15, 19), (5, 12.5, 21.5), (9, 10.5, 23.5), (14, 10, 24), (19, 11.5, 22.5), (23, 14.5, 19.5)])
    c.add(body, r, edge='out')
    # 금화 비늘
    for (x, y) in ((10, 15), (13, 14), (16, 15), (19, 16), (11, 19), (14, 19), (17, 20), (20, 19)):
        c.pat({(x - 1, y), (x, y + 1), (x + 1, y)} & body, sc)
        c.pat({(x, y)} & body, R('#ffe060', dk='#e0a020', lt='#fff4a0'))
    c.add(PG([(10, 20), (14, 23), (15, 19)]), fn, edge='in')
    c.eye(5, 14, 3)
    c.put(LN((3, 18), (0, 21), .5) | LN((4, 19), (1, 24), .5), hx('#ffe070'))
    for (x, y) in ((5, 7), (20, 3), (28, 22)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(40, 'f_marshpuff', '마시멜로 복어')
def _(c):
    r = R('#fff4f6', dk='#e6b4cc', lt='#ffffff')
    br = R('#e0a050', dk='#8a5230', lt='#f8c878')
    fn = R('#ffd6e4', dk='#e096b4', lt='#fff0f6')
    # 꼬리
    c.add(PG([(25, 14), (31, 12), (31, 21), (25, 18)]), fn, edge='out')
    # 말랑한 통통 몸 (둥근 네모)
    body = RC(5, 7, 24, 24) - {(5, 7), (6, 7), (5, 8), (24, 7), (23, 7), (24, 8), (5, 24), (6, 24), (5, 23), (24, 24), (23, 24), (24, 23)}
    body |= E(15, 15.5, 11, 9.2)
    c.add(body, r, edge='out')
    # 구운 갈색 윗면
    c.pat({(x, y) for (x, y) in body if y <= 9 + (1 if (x // 3) % 2 else 0) and 7 <= x <= 22}, br)
    c.pat({(x, y) for (x, y) in body if y <= 11 and x in (9, 10, 15, 16, 19) and False}, br)
    c.pat({(x, y) for (x, y) in body if (x, y) in {(8, 11), (9, 11), (14, 11), (15, 11), (20, 10), (21, 11)}}, br)
    # 작은 몽글 가시
    for (x, y) in ((8, 6), (13, 5), (18, 6), (23, 9), (4, 11), (4, 18), (8, 25), (14, 26), (20, 25), (24, 21)):
        c.add(E(x, y, 1.3, 1.3), fn, edge='out', shade=False)
    c.add(E(16, 18, 2.6, 2.4), fn, edge='out')
    # 얼굴
    c.eye(7, 13, 3)
    c.dot(5, 18, hx('#ff9ac0')); c.dot(6, 18, hx('#ff9ac0')); c.dot(10, 18, hx('#ff9ac0'))
    c.put({(6, 20), (7, 21), (8, 21), (9, 20)}, hx('#c0608a'))
    c.dot(2, 3, (255, 255, 255)) if False else None


@fish(41, 'f_salmon', '오로라 연어')
def _(c):
    r = R('#5ae8b8', dk='#2a8a98', lt='#a8ffd8')
    fn = R('#6ab8e8', dk='#3a62b0', lt='#a8dcff')
    ramp = [R('#58f0a0', dk='#28986a', lt='#a0ffd0'), R('#38d8d8', dk='#1c8898', lt='#88f0f0'), R('#5a9aff', dk='#2c52b8', lt='#9cc4ff'),
            R('#a070f0', dk='#5a34b0', lt='#c8a4ff'), R('#ff7ad0', dk='#b43a8e', lt='#ffa8e4')]
    c.add(PG([(24, 14), (31, 7), (28, 16), (31, 25), (24, 19)]), fn, edge='out')
    c.rays(PG([(24, 14), (31, 7), (28, 16), (31, 25), (24, 19)]), (24, 16), [-40, -20, 20, 40], .78)
    c.add(PG([(12, 10), (15, 6), (20, 8), (21, 12)]), fn, edge='out')
    c.add(PG([(21, 11), (23, 9), (24, 13)]), fn)
    c.add(PG([(13, 22), (16, 26), (21, 22)]), fn)
    body = prof([(2, 16, 19.5), (4, 12, 22), (8, 9.5, 24.5), (14, 9, 25), (20, 11, 23), (24, 14, 19.5)])
    c.add(body, r, edge='out')
    # 오로라 띠 (비스듬한 색 띠)
    for (x, y) in body:
        k = ((x * 3 + y * 2) // 8) % 5
        c.pat({(x, y)}, ramp[k])
    c.pat({(x, y) for (x, y) in body if y >= 22 and x >= 5}, R('#e8fff4', dk='#9ac8c4', lt='#ffffff'))
    c.add(PG([(8, 20), (12, 24), (14, 20)]), fn, edge='in')
    c.eye(4, 13, 3)
    # 갈고리 턱 + 이빨
    c.put({(x, 19) for x in range(2, 9)}, OUT)
    c.add(PG([(1, 19), (3, 21), (6, 20)]), r, edge='out')
    c.dot(4, 20, (255, 255, 255))
    for (x, y) in ((22, 4), (28, 3), (4, 27), (29, 29), (10, 3)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(42, 'f_book', '마법서 넙치')
def _(c):
    cv = R('#7a3a6a', dk='#3e1a46', lt='#a85a90')
    pg = R('#fff0cc', dk='#c8a878', lt='#ffffff')
    gd = R('#ffd24a', dk='#c88a1a', lt='#fff09a')
    fn = R('#a8506e', dk='#5a2440', lt='#d07a92')
    # 꼬리 (책등 쪽에서 삐죽)
    c.add(PG([(26, 14), (31, 11), (31, 22), (26, 19)]), fn, edge='out')
    # 가장자리 지느러미 술
    for x in range(6, 26, 3):
        c.add(PG([(x, 9), (x + 1, 6), (x + 2, 9)]), fn, edge=None)
        c.add(PG([(x, 25), (x + 1, 28), (x + 2, 25)]), fn, edge=None)
    # 책 표지
    c.add(PG([(2, 11), (13, 9), (16, 11), (28, 9), (28, 24), (16, 27), (13, 25), (2, 25)]) | RC(2, 10, 28, 25), cv, edge='out')
    # 쪽
    c.add(PG([(4, 12), (14, 11), (15, 22), (4, 23)]), pg, edge='out')
    c.add(PG([(16, 11), (26, 12), (26, 23), (16, 22)]), pg, edge='out')
    c.put({(15, y) for y in range(11, 24)}, pg[0])
    # 왼쪽 쪽: 넙치 얼굴 (눈 두 개, 입)
    c.eye(5, 13, 2)
    c.eye(9, 13, 2)
    c.put({(6, 20), (7, 20), (8, 20), (9, 19)}, hx('#a84a6a'))
    c.put({(x, 16) for x in range(5, 14)} - {(9, 16)}, pg[0]) if False else None
    # 오른쪽 쪽: 마법진
    ring = E(21, 17, 3.8, 3.8) - E(21, 17, 2.4, 2.4)
    c.put(ring, hx('#8a5ae0'))
    c.put({(21, 14), (21, 20), (18, 17), (24, 17), (21, 17)}, hx('#b48aff'))
    c.put({(19, 15), (23, 15), (19, 19), (23, 19)}, hx('#8a5ae0'))
    c.put({(20, 17), (22, 17), (21, 16), (21, 18)}, gd[1])
    # 금박 모서리
    for (x, y) in ((2, 10), (28, 10), (2, 25), (28, 25)):
        c.put({(x, y), (x + (1 if x < 10 else -1), y), (x, y + (1 if y < 15 else -1))}, gd[1])
    c.put({(x, 10) for x in range(3, 28, 2)}, gd[0]) if False else None


@fish(43, 'f_witch', '마녀 모자 금붕어')
def _(c):
    r = R('#ff8a2a', dk='#c04a1c', lt='#ffb44a')
    fn = R('#ffa040', dk='#d0602a', lt='#ffd078')
    hat = R('#6a3aa8', dk='#321a62', lt='#9468d8')
    gold = R('#ffd24a', dk='#c88a1a', lt='#fff09a')
    # 부채꼴 꼬리 (너울)
    t = PG([(21, 17), (27, 8), (31, 10), (31, 17), (31, 25), (27, 27), (21, 21)])
    c.add(fade(t, 28, 1) if False else t, fn, edge='out')
    c.rays(t, (21, 19), [-50, -30, -10, 10, 30, 50], .78)
    c.add(PG([(13, 12), (16, 9), (21, 12), (20, 16)]), fn, edge='out')
    c.add(PG([(13, 26), (15, 30), (19, 26)]), fn)
    body = E(12.5, 20, 10.5, 8) | E(8, 19.5, 6, 6)
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y >= 24}, R('#ffd8a0', dk='#e0a070', lt='#fff0d0'))
    for (x, y) in ((11, 16), (14, 15), (17, 18), (10, 21), (14, 21)):
        c.pat({(x, y), (x + 1, y)} & body, fn)
    c.add(E(14, 22, 3, 2.2), fn, edge='in')
    c.eye(5, 17, 3)
    c.put({(1, 21), (2, 22)}, hx('#7a2d12'))
    # 마녀 모자
    c.add(E(8.5, 12.5, 7, 2.2), hat, edge='out')
    c.add(PG([(5, 11), (8, 3), (10, 0), (12, 2), (12, 11)]), hat, edge='out')
    c.put({(x, 10) for x in range(5, 13)} & set(c.p), gold[1])
    c.dot(9, 10, hat[0]); c.dot(8, 10, hat[0])
    c.dot(11, 0, hat[1]); c.dot(12, 1, hat[2]); c.dot(13, 2, hat[1])


@fish(44, 'f_starmarlin', '별빛 청새치')
def _(c):
    r = R('#3a5eb8', dk='#1c2e78', lt='#6a8ee0')
    bl = R('#d6e4fa', dk='#8ea4d8', lt='#ffffff')
    fn = R('#2c4aa0', dk='#16286a', lt='#5a7ad0')
    yl = R('#ffe45e', dk='#ffae2a', lt='#fff6b0')
    # 초승달 꼬리
    c.add(PG([(25, 16), (30, 5), (31, 6), (28, 16), (31, 26), (30, 27)]) | PG([(24, 14), (28, 13), (28, 19), (24, 18)]) | PG([(26, 14), (31, 4), (28, 14)]) | PG([(26, 18), (31, 28), (28, 18)]), fn, edge='out')
    # 큰 돛 등지느러미
    sail = PG([(12, 13), (13, 8), (16, 6), (22, 7), (24, 13)])
    c.add(sail, fn, edge='out')
    c.rays(sail, (18, 14), [-100, -80, -60, -45], .8)
    c.add(PG([(14, 19), (13, 25), (18, 21)]), fn)
    c.add(PG([(19, 20), (22, 25), (23, 20)]), fn)
    body = prof([(8, 15.5, 18), (11, 13, 20.5), (16, 12.5, 21), (21, 13.5, 20), (25, 15, 18.5)])
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y >= 18}, bl)
    # 긴 창 주둥이
    c.add(tube([(10, 16.5), (1, 16.5)], 1.4, .5, smooth=False), bl, edge='out')
    c.eye(9, 14, 2)
    # 별빛 무늬 (등지느러미와 몸)
    def star(x, y, k=1):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} if k else {(x, y)}, yl[1])
        c.dot(x, y, yl[2])
    star(17, 6); star(21, 9)
    c.put({(13, 17), (18, 16), (22, 16)}, yl[1])
    c.pat({(14, 14), (17, 13), (20, 14)} & body, R('#8ab4ff'))
    c.put({(4, 8), (3, 24), (28, 22)}, (255, 255, 255))


@fish(45, 'f_shadow', '그림자 가오리')
def _(c):
    r = R('#5a3e8c', dk='#281a50', lt='#8062b4')
    d = R('#3c2a68', dk='#1c1238', lt='#5a428c')
    gl = R('#ff6ad0', dk='#c8349a', lt='#ffb4ec', hi='#ffffff')
    # 길고 가시 돋친 꼬리
    c.add(tube([(20, 16), (26, 16), (31, 14)], 1.3, .5, smooth=False), d, edge='out', shade=False)
    c.add(PG([(24, 14), (26, 11), (27, 15)]) | PG([(24, 18), (26, 21), (27, 17)]), d, edge='out', shade=False)
    # 박쥐 같은 뾰족 날개 (뒷가장자리가 톱니)
    top = [(2, 16), (8, 11), (15, 5), (24, 0), (21, 5), (27, 5), (21, 9), (25, 12), (19, 13), (21, 16)]
    bot = [(x, 32 - y) for (x, y) in reversed(top)]
    body = PG(top + bot)
    c.add(body, r, edge='out')
    # 날개맥과 가운데 능선
    c.pat((LN((8, 15), (24, 1), .5) | LN((9, 14), (26, 5), .5) | LN((10, 16), (20, 13), .5)) & body, d)
    c.pat((LN((8, 17), (24, 31), .5) | LN((9, 18), (26, 27), .5) | LN((10, 16), (20, 19), .5)) & body, d)
    c.pat(E(9, 16, 5, 3), R('#7a5cb0', dk='#3a2a68', lt='#9a7ccc'))
    # 반짝이는 눈
    c.eye(3, 12, 2, white=gl[3], pupil=gl[1])
    c.eye(3, 18, 2, white=gl[3], pupil=gl[1])
    c.dot(5, 15, d[0]); c.dot(5, 17, d[0])
    for (x, y) in ((29, 6), (4, 28)):
        c.put({(x, y), (x - 1, y), (x + 1, y)}, hx('#a888e0'))


@fish(46, 'f_moonbun', '달토끼 금붕어')
def _(c):
    r = R('#fff6ee', dk='#d8b8c4', lt='#ffffff')
    fn = R('#ffe6ee', dk='#e0a8c0', lt='#fff6fa')
    pk = R('#ff9ec0', dk='#d0608c', lt='#ffc8dc')
    mo = R('#ffe27a', dk='#e0aa30', lt='#fff4b0')
    # 길게 너울거리는 리본 꼬리
    t = PG([(19, 17), (24, 9), (31, 7), (28, 14), (31, 20), (26, 26), (19, 20)])
    c.add(fade(t, 28), fn, edge='out')
    c.rays(t, (19, 18), [-45, -25, -5, 15, 35], .82)
    c.add(PG([(12, 22), (13, 28), (18, 23)]), fn)
    body = E(11, 19, 9.5, 7) | E(7, 18.5, 6, 5.5)
    c.add(body, r, edge='out')
    # 토끼 귀 (길게 솟은)
    c.add(EL(6.5, 8, 7.5, 2.4, 100), r, edge='out')
    c.add(EL(12.5, 8, 7, 2.4, 80), r, edge='out')
    c.pat(EL(6.4, 8, 5, 1, 100) | EL(12.6, 8, 4.5, 1, 80), pk)
    c.pat({(x, y) for (x, y) in body if y >= 23}, pk) if False else None
    # 초승달 이마 무늬
    c.pat({(8, 14), (9, 14), (7, 15), (7, 16), (8, 17), (9, 17)} & body, mo, keep_tone=False)
    c.put({(9, 15), (9, 16)} & body, r[1])
    c.eye(4, 17, 3)
    c.put({(1, 21)}, pk[1]); c.put({(2, 20), (1, 20), (1, 19)}, pk[0] if False else pk[1])
    c.dot(2, 21, pk[0])
    c.add(E(14, 22, 2.6, 2), fn, edge='in')
    # 솜꼬리 + 별빛
    c.add(E(20, 20, 2.4, 2.4), (255, 255, 255), edge='out') if False else None
    for (x, y) in ((26, 3), (3, 4), (29, 28)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, mo[1])


@fish(47, 'f_jellyqueen', '등불 해파리 여왕')
def _(c):
    lt_ = R('#ffb02a', dk='#d0561a', lt='#ffd860', hi='#fff4b8')
    rib = R('#e07a1a', dk='#a03a14', lt='#ff9a2a')
    gold = R('#ffe05a', dk='#d89a1a', lt='#fff6b0')
    ar = R('#ffcf70', dk='#e08a3a', lt='#fff0b0')
    # 긴 촉수 + 끝의 작은 등불
    for x, ph in ((7, 0), (11, 1), (21, 0), (25, 1)):
        s_ = 1 if ph else -1
        pts = [(x, 18), (x + s_, 22), (x - s_, 26), (x + s_, 29)]
        c.add(tube(pts, .6, .5), ar, shade=False)
        c.dot(x + s_, 30, gold[2]); c.dot(x + s_, 31, gold[1])
    for x, ph in ((13, 0), (16, 1), (19, 0)):
        s_ = 2 if ph else -2
        c.add(tube([(x, 17), (x + s_, 21), (x - s_, 25), (x + s_, 29)], 1.7, .7), ar, edge='out')
    # 등불 모양 종 (둥근 타원 + 세로 갈비)
    bell = E(15.5, 12, 10.5, 8.2)
    c.add(bell, lt_, edge='out')
    for dx in (-6.5, -3.4, 0, 3.4, 6.5):
        c.pat(tube([(15.5 + dx * .5, 4.5), (15.5 + dx, 12), (15.5 + dx * .5, 19.5)], .5) & bell, rib)
    # 윗뚜껑 + 아랫 술
    c.add(E(15.5, 17.5, 8, 1.4), rib, edge='out')
    c.pat(E(13, 9, 3, 2) | {(11, 12), (10, 13)}, R('#fff4c0', dk='#ffd860', lt='#ffffff'))
    # 왕관
    crown = PG([(9, 5), (9, 0), (12, 3), (15, 0), (16, 0), (19, 3), (22, 0), (22, 5)])
    c.add(crown, gold, edge='out')
    c.put({(12, 3), (16, 2), (20, 3)}, hx('#ff4a6a'))
    c.dot(11, 1, hx('#ffffff')) if False else None
    c.eye(11, 12, 2)
    c.eye(18, 12, 2)
    c.put({(15, 15), (16, 15)}, hx('#a03a14'))


@fish(48, 'f_turtle', '왕관 거북')
def _(c):
    sh_ = R('#4ea860', dk='#1e5a3c', lt='#86d880')
    sk = R('#9ac86a', dk='#4e7e3c', lt='#c8ec94')
    gold = R('#ffd24a', dk='#c88a1a', lt='#fff09a')
    # 꼬리, 뒷발
    c.add(PG([(26, 21), (31, 23), (26, 24)]), sk, edge='out')
    c.add(E(22, 26, 4.5, 3), sk, edge='out')
    # 머리와 목
    c.add(tube([(10, 19), (6, 19)], 3, 3, smooth=False) | E(5, 18, 4.2, 3.8), sk, edge='out')
    # 앞발
    c.add(EL(11.5, 25, 4.6, 2.6, 25), sk, edge='out')
    # 배딱지
    c.add(E(16.5, 23, 12, 2.6), R('#f2e4a8', dk='#b09858', lt='#fff6d0'), edge='out')
    # 등딱지
    shell = E(16.5, 16, 11.5, 8.5) & {(x, y) for x in range(N) for y in range(0, 22)}
    c.add(shell, sh_, edge='out')
    hexs = R('#8ee08a', dk='#3a8a58', lt='#c4f8b0')
    for (x, y) in ((16, 13), (11, 17), (22, 17), (16, 19) if False else (16, 18), (8, 14) if False else (13, 21) if False else (12, 12), (21, 12)):
        pass
    # 육각 무늬
    c.pat(LN((10, 21), (13, 11), .5) | LN((16, 8), (16, 22), .5) | LN((22, 21), (19, 11), .5) | LN((9, 14), (24, 14), .5) | LN((9, 19), (24, 19), .5), sh_ and R('#2a7048', dk='#14402c', lt='#3a8858')) if False else None
    for pts in (((11, 21), (13, 15), (19, 15), (21, 21)), ((13, 15), (14, 9)), ((19, 15), (18, 9)), ((13, 15), (9, 14)), ((19, 15), (24, 14))):
        for i in range(len(pts) - 1):
            c.pat(LN(pts[i], pts[i + 1], .5) & shell, R('#2e7a4a', dk='#164a30', lt='#48986a'))
    c.pat(E(16, 18, 2, 1.4) & shell, hexs)
    # 왕관 (머리 위)
    crown = PG([(2, 13), (2, 8), (4, 11), (6, 7), (8, 11), (10, 8), (10, 13)])
    c.add(crown, gold, edge='out')
    c.put({(4, 12), (7, 12)}, hx('#ff4a6a'))
    c.eye(3, 16, 2)
    c.put({(1, 20), (2, 20), (3, 21)}, OUT)
    c.dot(2, 17, (255, 255, 255)) if False else None


@fish(49, 'f_dragon', '용 비늘 잉어')
def _(c):
    r = R('#d8322a', dk='#7a1430', lt='#ff6a48')
    gd = R('#ffcc3a', dk='#c88a1a', lt='#fff09a')
    fn = R('#ff9a2a', dk='#b0521c', lt='#ffd05a')
    # 불꽃 같은 긴 꼬리
    t = PG([(23, 15), (27, 8), (31, 2), (29, 11), (31, 15), (31, 20), (29, 25), (31, 30), (25, 25), (23, 19)])
    c.add(t, fn, edge='out')
    c.rays(t, (23, 17), [-70, -45, -20, 5, 30, 55, 80], .78)
    # 용의 갈기 (등지느러미 가시)
    sp = set()
    for x in range(8, 23, 3):
        sp |= PG([(x - 1, 11), (x, 5 + (x % 4)), (x + 2, 11)])
    c.add(sp, fn, edge='out')
    c.add(PG([(14, 23), (16, 28), (21, 24)]), fn)
    body = prof([(4, 14, 20), (6, 11, 23), (10, 9.5, 25), (15, 9.5, 25), (20, 11.5, 23), (23, 14.5, 20)])
    c.add(body, r, edge='out')
    # 금빛 용 비늘 (물결 호)
    for (x, y) in ((9, 14), (13, 13), (17, 14), (20, 17), (11, 18), (15, 18), (19, 20), (13, 22), (17, 23)):
        c.pat({(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)} & body, gd)
    c.pat({(x, y) for (x, y) in body if y >= 23}, R('#ffd070', dk='#d89a3a', lt='#fff0b0'))
    # 뿔 + 수염
    c.add(PG([(6, 11), (4, 5), (9, 10)]), gd, edge='out')
    c.add(PG([(9, 10), (9, 4), (13, 10)]), gd, edge='out')
    c.put(tube([(4, 18), (1, 20), (1, 24), (4, 26)], .5), gd[2])
    c.put(tube([(5, 19), (2, 23), (3, 28)], .5), gd[2])
    c.add(PG([(10, 19), (14, 24), (15, 20)]), fn, edge='in')
    c.eye(6, 13, 3, ring=hx('#ffe35a'))
    c.dot(5, 18, OUT)


@fish(50, 'f_crystalcrab', '수정 왕게')
def _(c):
    b = R('#8ad4ff', dk='#3a78d0', lt='#d0f0ff', hi='#ffffff')
    pk = R('#ffa8e0', dk='#c85cb4', lt='#ffd4f2')
    cx = 15.5
    legs = set()
    for sgn in (-1, 1):
        for (y0, kx, ky, ex, ey) in ((18, 11, 14, 4, 20), (20, 11.5, 18, 3, 27), (22, 10, 22, 4, 30)):
            legs |= tube([(cx + sgn * 7, y0), (cx + sgn * kx, ky), (cx + sgn * (cx - ex), ey)], .9, .6, smooth=False)
    c.add(legs, pk, shade=False, edge='out')
    for sgn in (-1, 1):
        arm = tube([(cx + sgn * 6, 17), (cx + sgn * 10, 12), (cx + sgn * 11, 9)], 1.7, 1.7)
        c.add(arm, b, edge='out')
        claw = E(cx + sgn * 11, 5.2, 4.2, 4.6) - PG([(cx + sgn * 11, 5), (cx + sgn * 14, -1), (cx + sgn * 8, -1)]) - PG([(cx + sgn * 11, 4), (cx + sgn * 12.5, 0), (cx + sgn * 9.5, 0)])
        c.add(claw, pk, edge='out')
    shell = PG([(cx, 8), (cx + 8, 13), (cx + 9, 21), (cx + 4, 26), (cx - 4, 26), (cx - 9, 21), (cx - 8, 13)])
    c.add(shell, b, edge='out')
    # 뾰족뾰족 수정 가시
    for (x, y, h) in ((cx - 7, 13, 3), (cx + 7, 13, 3), (cx - 9, 20, 3), (cx + 9, 20, 3)):
        c.add(PG([(x - 1, y + 1), (x + (-3 if x < cx else 3), y - 1), (x + (0), y + 3)]), pk, edge='out')
    # 면 나누기
    fac = R('#dff6ff', dk='#78b4f0', lt='#ffffff')
    for pts in (((cx, 8), (cx, 26)), ((cx - 8, 13), (cx + 8, 21)), ((cx + 8, 13), (cx - 8, 21)), ((cx - 9, 21), (cx + 9, 21))):
        c.pat(LN(pts[0], pts[1], .5) & shell, fac)
    # 왕관 수정
    c.add(PG([(cx - 3, 11), (cx - 3, 6), (cx - 1, 9), (cx, 4), (cx + 1, 9), (cx + 3, 6), (cx + 3, 11)]), pk, edge='out')
    c.put({(int(cx) , 8), (int(cx), 7)}, (255, 255, 255))
    c.eye(10, 14, 2)
    c.eye(19, 14, 2)
    c.put({(14, 22), (15, 22), (16, 22), (17, 22)}, pk[0]) if False else None


@fish(51, 'f_whale', '별똥별 꼬마 고래')
def _(c):
    r = R('#4a8ee8', dk='#223a98', lt='#82bcff')
    bl = R('#e8f2ff', dk='#9cb4e8', lt='#ffffff')
    yl = R('#ffe45e', dk='#ffae2a', lt='#fff6b0', hi='#ffffff')
    fn = R('#3a70c8', dk='#1c2e84', lt='#6a9ae8')
    # 꼬리 지느러미 (위로 들어 올림)
    c.add(tube([(21, 17), (25, 14), (27, 10)], 3.0, 1.6), r, edge='out')
    c.add(PG([(27, 11), (23, 6), (23, 3), (27, 6), (28, 3), (31, 5), (31, 8), (27, 12)]), fn, edge='out')
    body = prof([(2, 14, 22), (4, 11, 25), (8, 9.5, 26.5), (14, 11, 26), (19, 15, 23), (22, 18, 21)])
    c.add(body, r, edge='out')
    # 흰 배 + 주름
    c.pat({(x, y) for (x, y) in body if y >= 21 and x < 19}, bl)
    for x in (8, 10, 12, 14):
        c.pat({(x, 23), (x, 24)} & body, R('#c8d8f4', dk='#8aa4e0', lt='#e4eefc'))
    c.add(EL(14, 24, 4, 2, 30), fn, edge='out')
    c.eye(5, 15, 3)
    c.dot(4, 19, hx('#ff9ac0')); c.dot(5, 19, hx('#ff9ac0'))
    c.put({(2, 20), (3, 21), (4, 21)}, hx('#16286a'))
    # 별똥별: 큰 별 + 꼬리 줄
    c.put({(9, 6), (8, 6), (10, 6), (9, 5), (9, 7), (9, 4), (9, 8)} , yl[1])
    c.put({(8, 5), (10, 5), (8, 7), (10, 7)}, yl[2])
    c.dot(9, 6, yl[3])
    for i in range(1, 7):
        c.dot(9 + i * 2, 6 + i // 2 - 0, yl[1] if i % 2 else yl[0])
    c.dot(11, 4, (255, 255, 255)); c.dot(3, 8, (255, 255, 255))
    c.dot(20, 3, yl[2]); c.dot(28, 14, yl[2])


@fish(52, 'f_cauldronangler', '가마솥 아귀')
def _(c):
    ir = R('#4a4a62', dk='#1e1e30', lt='#7a7a96')
    gr = R('#7aff5a', dk='#2aa83a', lt='#c8ffa8', hi='#f0ffe0')
    fn = R('#3a3a54', dk='#18182a', lt='#5a5a78')
    tooth = R('#ffffff', dk='#d0d0e0')
    # 꼬리
    c.add(PG([(25, 18), (31, 14), (31, 26), (25, 23)]), fn, edge='out')
    # 다리
    c.add(RC(7, 27, 10, 30) | RC(21, 27, 24, 30), fn, edge='out')
    # 솥 몸통
    body = E(15.5, 20, 11.5, 8.5)
    c.add(body, ir, edge='out')
    # 솥 귀(손잡이)
    c.add(E(4, 15, 2.2, 2.2) - E(4, 15, 1, 1), fn, edge='out')
    # 솥 입구 테두리
    c.add(E(15.5, 12.5, 9.5, 2.2), ir, edge='out')
    # 보글보글 초록 물약
    c.add(E(15.5, 12, 7.8, 1.5), gr, edge=None)
    for (x, y, rr) in ((11, 9, 1.8), (16, 7, 2.4), (21, 9.5, 1.6), (14, 4, 1.2), (19, 3, 1)):
        c.add(E(x, y, rr, rr), gr, edge='out')
    c.dot(15, 6, gr[3]); c.dot(10, 8, gr[3])
    # 얼굴 (아귀 입 + 이빨)
    c.put({(x, 21) for x in range(6, 25)} , OUT)
    for x in range(7, 24, 3):
        c.add({(x, 20), (x, 19), (x + 1, 20)}, tooth, shade=False)
    for x in (8, 11, 14, 17, 20, 23):
        c.dot(x, 22, tooth[0])
    c.eye(9, 15, 3, ring=gr[1])
    c.eye(18, 15, 3, ring=gr[1])
    # 낚싯대 (불꽃 등불)
    c.put(tube([(25, 14), (28, 8), (28, 3)], .5), hx('#c8a0ff'))
    c.add(PG([(28, 0), (30, 3), (28, 5), (26, 3)]), gr, edge='out')


@fish(53, 'f_mermaid', '인어의 은빛 잉어')
def _(c):
    r = R('#cfe0ee', dk='#6a86b0', lt='#f4faff', hi='#ffffff')
    fl = R('#9adcd8', dk='#4a8cb0', lt='#d0f6ee')
    pk = R('#ffb8d8', dk='#d070a8', lt='#ffe0f0')
    # 인어 꼬리 같은 큰 부채 지느러미 (아래로 살짝 굽음)
    t1 = PG([(20, 15), (25, 9), (30, 6), (31, 10), (28, 13), (31, 17), (27, 19), (22, 18)])
    t2 = PG([(21, 18), (26, 19), (30, 22), (31, 27), (27, 26), (28, 30), (23, 25)])
    c.add(t1, fl, edge='out')
    c.add(t2, fl, edge='out')
    c.rays(t1, (20, 17), [-30, -10, 10], .8)
    c.rays(t2, (21, 19), [20, 40, 60], .8)
    c.pat({(x, y) for (x, y) in set(c.p) if x >= 27 and y >= 20}, pk) if False else None
    body = prof([(2, 14, 18), (4, 11.5, 20.5), (8, 10.5, 22), (13, 11.5, 22), (17, 13.5, 21), (21, 15, 19.5)])
    c.add(PG([(11, 10), (14, 6), (19, 9), (19, 13)]), fl, edge='out')
    c.add(body, r, edge='out')
    # 비늘 호
    for (x, y) in ((8, 13), (11, 13), (14, 14), (17, 15), (7, 17), (10, 17), (13, 18), (16, 18), (9, 20), (12, 21), (15, 21)):
        c.pat({(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)} & body, R('#b0c8e0', dk='#6a86b0', lt='#d8e8f6'))
    c.pat({(x, y) for (x, y) in body if x >= 14 and y >= 18} | {(x, y) for (x, y) in body if x >= 17}, R('#a8e8e0', dk='#4a98b0', lt='#d4faf4'))
    c.add(PG([(8, 19), (11, 22), (13, 19)]), fl, edge='in')
    c.eye(4, 13, 3)
    # 진주 목걸이 + 조개 머리핀
    for q in ((7, 14), (8, 16), (8, 18), (7, 20)):
        c.dot(q[0], q[1], (255, 255, 255))
    c.add(PG([(7, 9), (9, 7), (11, 9), (10, 11), (8, 11)]), pk, edge='out')
    c.put({(9, 8), (9, 10)}, pk[0])
    c.put({(2, 16), (3, 17)}, hx('#6a4a90'))
    c.put({(3, 5), (27, 3), (24, 29)}, (255, 255, 255))


@fish(54, 'f_ghostshark', '유령 상어')
def _(c):
    r = R('#d0dcf8', dk='#7488d0', lt='#f2f6ff')
    bl = R('#f8faff', dk='#bccaec', lt='#ffffff')
    fn = R('#aab8ec', dk='#6678c8', lt='#d4defc')
    # 초승달 꼬리 (위 날개가 더 긺, 끝은 듬성듬성)
    tail = PG([(24, 15), (27, 8), (31, 2), (30, 11), (28, 16), (30, 20), (29, 25), (24, 19)])
    c.add(fade(tail, 28), fn, edge='out')
    # 큰 등지느러미 (삼각)
    c.add(PG([(11, 12), (15, 3), (20, 11)]), fn, edge='out')
    c.add(PG([(21, 14), (23, 11), (24, 15)]), fn)
    c.add(PG([(19, 20), (22, 25), (23, 19)]), fn)
    body = prof([(1, 18, 20), (4, 15, 21.5), (9, 12, 23), (15, 11.5, 23), (21, 13.5, 21), (25, 15.5, 19)])
    c.add(body, r, edge='out')
    c.pat({(x, y) for (x, y) in body if y >= 20 and x > 3}, bl)
    # 가슴지느러미 (낫 모양)
    c.add(PG([(9, 20), (7, 28), (14, 22), (15, 19)]), fn, edge='out')
    # 아가미 줄, 입, 이빨
    for x in (11, 12, 13):
        c.pat({(x, y) for y in range(15, 19)} & body, R('#9aaae0', dk='#6678c8', lt='#bccaf0')) if x != 12 else None
    c.put({(x, 21) for x in range(2, 9)}, hx('#5a4a90'))
    for x in (3, 5, 7):
        c.dot(x, 22, (255, 255, 255))
    # 텅 빈 유령 눈
    c.eye(5, 16, 3, ring=(255, 255, 255), pupil=hx('#2a2060'))
    c.put({(1, 19), (2, 20)}, r[1]) if False else None
    for (x, y) in ((4, 5), (28, 28), (2, 28)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(55, 'f_king', '호박달 메기왕')
def _(c):
    r = R('#e8802a', dk='#9c4218', lt='#ffb04a')
    d = R('#c4601c', dk='#7a3414', lt='#e88a34')
    gold = R('#ffd24a', dk='#c88a1a', lt='#fff09a')
    mo = R('#fff2a0', dk='#e0b83a', lt='#ffffff')
    c.add(PG([(24, 15), (28, 12), (31, 15), (31, 21), (28, 24), (24, 21)]), d, edge='out')
    c.add(PG([(15, 11), (17, 8), (22, 12), (22, 16)]), d, edge='out')
    c.add(PG([(14, 25), (16, 28), (23, 26), (24, 22)]), d, edge='out')
    body = prof([(3, 15, 25), (5, 11.5, 26), (9, 11, 26.5), (14, 11.5, 26), (19, 13, 24), (24, 15, 21)])
    c.add(body, r, edge='out')
    # 호박 갈비
    for x in (11, 15, 19):
        c.pat(tube([(x, 13), (x - 1, 19), (x, 25)], .5) & body, d)
    c.pat({(x, y) for (x, y) in body if y >= 24 and x > 8}, R('#f8c070', dk='#d08840', lt='#ffe0a0'))
    # 이마의 달 (초승달 무늬)
    c.pat({(7, 12), (8, 12), (6, 13), (6, 14), (7, 15), (8, 15)} & body, mo, keep_tone=False)
    # 큰 입 + 이빨
    c.put({(x, 21) for x in range(3, 12)}, OUT)
    c.put({(4, 22), (6, 22), (8, 22), (10, 22)}, (255, 255, 255))
    # 길고 구불구불한 수염 (여섯 가닥)
    for pts in (((3, 17), (1, 15), (0, 12)), ((4, 18), (1, 19), (0, 22)), ((3, 20), (0, 25), (2, 29)), ((5, 22), (3, 27), (6, 30)),
                ((9, 12), (11, 9), (14, 8)) if False else ((4, 12), (2, 9), (3, 5))):
        c.put(tube(list(pts), .5), hx('#ffc060'))
    # 왕관
    crown = PG([(8, 11), (8, 5), (10, 8), (12, 4), (14, 8), (16, 5), (16, 11)])
    c.add(crown, gold, edge='out')
    c.put({(10, 9), (14, 9)}, hx('#ff4a6a'))
    c.dot(12, 8, hx('#6ae0ff'))
    c.eye(5, 15, 3, ring=hx('#ffe35a'))


@fish(56, 'f_auroracachalot', '오로라 향유고래')
def _(c):
    r = R('#4a4a9c', dk='#22206a', lt='#7a78c8')
    bl = R('#c8c8f0', dk='#8888cc', lt='#e8e8ff')
    fn = R('#3a3a84', dk='#1a1858', lt='#5a58a8')
    ramp = [R('#58f0a0', dk='#28986a', lt='#a0ffd0'), R('#38d8d8', dk='#1c8898', lt='#88f0f0'),
            R('#a070f0', dk='#5a34b0', lt='#c8a4ff'), R('#ff7ad0', dk='#b43a8e', lt='#ffa8e4')]
    # 꼬리 자루 + 꼬리 지느러미 (위로)
    c.add(tube([(20, 16), (25, 15), (28, 11)], 4.2, 2.0), r, edge='out')
    c.add(PG([(28, 12), (24, 7), (22, 3), (27, 6), (29, 2), (31, 7), (31, 10), (29, 12)]), fn, edge='out')
    # 네모난 큰 머리 + 몸
    body = RC(2, 6, 14, 24) | E(13, 15, 11, 9) | RC(8, 8, 20, 22)
    body = PG([(1, 7), (7, 5), (15, 6), (21, 10), (24, 15), (22, 20), (17, 24), (9, 26), (4, 24), (1, 20)])
    c.add(body, r, edge='out')
    # 아래턱 + 이빨
    c.add(PG([(4, 22), (14, 23), (15, 26), (6, 27)]), bl, edge='out')
    for x in (6, 8, 10, 12):
        c.dot(x, 22, (255, 255, 255))
    # 오로라 띠가 등에 걸친 모습
    for (x, y) in body:
        if y <= 16:
            k = ((x + y * 2) // 4) % 4
            if (x - 2) / 22 + (y - 6) / 14 * .4 < 1.1 and y <= 14 - (x - 14) * .5 if x > 14 else y <= 14:
                c.pat({(x, y)}, ramp[k])
    c.pat({(x, y) for (x, y) in body if y >= 19 and y <= 21 and x > 14}, bl)
    # 주름 + 지느러미
    for x in (7, 10, 13):
        c.pat({(x, y) for y in range(15, 20)} & body, fn)
    c.add(EL(15, 22, 4.5, 2, 35), fn, edge='out')
    c.eye(4, 15, 2)
    c.dot(2, 10, hx('#101050'))  # 분수공
    for (x, y) in ((5, 2), (14, 1), (28, 22), (3, 29), (19, 29)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, (255, 255, 255))


@fish(57, 'f_dragonsea', '용머리 바다거북')
def _(c):
    sh_ = R('#2e9a8a', dk='#124a5a', lt='#5ad0b0')
    sk = R('#4ab8a0', dk='#1c6a74', lt='#88e8c8')
    gd = R('#ffcc3a', dk='#c88a1a', lt='#fff09a')
    rd = R('#ff6a3a', dk='#b02a1a', lt='#ffa05a')
    # 뒷지느러미 + 꼬리
    c.add(EL(23, 24, 4.6, 2.4, 55), sk, edge='out')
    c.add(EL(23, 8, 4.6, 2.4, -55), sk, edge='out')
    c.add(tube([(24, 16), (28, 16), (31, 15)], 1.5, .6, smooth=False), sk, edge='out')
    # 앞지느러미 (크고 넓게)
    c.add(EL(12, 27, 8, 2.8, -25) | E(7, 29, 2, 1.5), sk, edge='out')
    c.add(EL(12, 5, 8, 2.8, 25) | E(7, 3, 2, 1.5), sk, edge='out')
    # 등딱지
    shell = E(17, 16, 10, 8.6)
    c.add(shell, sh_, edge='out')
    # 용 비늘 무늬
    sc = R('#8ae8c0', dk='#2a7a84', lt='#c4fce0')
    for (x, y) in ((13, 12), (17, 12), (21, 12), (11, 16), (15, 16), (19, 16), (23, 16), (13, 20), (17, 20), (21, 20)):
        c.pat({(x - 1, y), (x, y + 1), (x + 1, y)} & shell, sc)
    c.pat(LN((8, 16), (26, 16), .5) & shell, R('#1e6a74', dk='#0e3a4a', lt='#2e8a90'))
    # 불꽃 갈기 + 용머리 (뿔, 수염)
    c.add(PG([(10, 11), (7, 6), (11, 9), (11, 5), (14, 9)]), rd, edge='out')
    c.add(PG([(10, 21), (7, 26), (11, 23), (11, 27), (14, 23)]), rd, edge='out')
    head = E(5, 16, 4.6, 4.2) | RC(2, 15, 7, 19)
    c.add(head, sk, edge='out')
    c.add(PG([(4, 12), (2, 6), (7, 11)]), gd, edge='out')
    c.add(PG([(7, 12), (8, 6), (10, 12)]), gd, edge='out')
    c.put({(x, 18) for x in range(1, 6)}, OUT)
    c.dot(2, 19, (255, 255, 255))
    c.put(tube([(1, 17), (0, 21)], .5) | tube([(4, 20), (3, 25)], .5), gd[2])
    c.eye(5, 14, 2, white=(255, 255, 255), pupil=hx('#d02a1a'))
    c.dot(1, 16, OUT)


@fish(58, 'f_lord', '호수의 주인')
def _(c):
    # 달무리 (뒤)
    for rr, col in ((15.2, '#3a3a78'), (13.4, '#58589c')):
        ring = E(15.5, 15.5, rr, rr) - E(15.5, 15.5, rr - 1.2, rr - 1.2)
        c.put(chk(ring, 0), hx(col))
    r = R('#4a8ea8', dk='#1c3e68', lt='#86ccd8')
    gd = R('#ffd86a', dk='#c88a2a', lt='#fff4b0')
    fn = R('#2e6a98', dk='#142e5a', lt='#5a9ac8')
    # 거대한 꼬리
    t = PG([(23, 15), (28, 8), (31, 6), (30, 12), (28, 16), (30, 20), (31, 26), (28, 24), (23, 19)])
    c.add(t, fn, edge='out')
    c.rays(t, (23, 17), [-50, -30, -10, 10, 30, 50], .78)
    c.add(PG([(9, 10), (11, 5), (16, 3), (22, 8), (22, 13)]), fn, edge='out')
    c.add(PG([(12, 24), (15, 29), (20, 25), (19, 22)]), fn, edge='out')
    body = prof([(2, 14, 20), (4, 10, 23), (8, 8, 25.5), (14, 7.5, 26), (19, 10, 24), (23, 14, 20)])
    c.add(body, r, edge='out')
    # 황금 비늘 (고대의 위엄)
    for (x, y) in ((9, 12), (13, 11), (17, 12), (21, 15), (11, 16), (15, 16), (19, 18), (9, 20), (13, 21), (17, 22)):
        c.pat({(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y)} & body, R('#86c8c8', dk='#2e6a88', lt='#b8ece0'))
    c.pat({(x, y) for (x, y) in body if y >= 23}, R('#d8f4e0', dk='#88c4c0', lt='#ffffff'))
    c.add(PG([(8, 20), (12, 25), (14, 20)]), fn, edge='in')
    # 이마 왕관 지느러미 + 보름달 이마
    c.add(PG([(5, 9), (5, 4), (8, 7), (10, 3), (12, 8), (13, 9)]), gd, edge='out')
    c.put(E(6, 13, 1.5, 1.5) & body, gd[1])
    # 긴 수염 두 쌍
    for pts in (((3, 18), (0, 21), (0, 25), (3, 28)), ((4, 19), (1, 24), (3, 30)), ((3, 16), (0, 14), (0, 10))):
        c.put(tube(list(pts), .5), gd[2])
    c.put({(x, 21) for x in range(2, 7)}, OUT)
    c.eye(5, 15, 3, ring=hx('#ffe35a'))


@fish(59, 'f_moonkoi', '달잉어 신령')
def _(c):
    wh = R('#fffaf0', dk='#c8bcd8', lt='#ffffff')
    og = R('#ff8a2a', dk='#c04a1c', lt='#ffb44a')
    fn = R('#fff0f6', dk='#d8a8c8', lt='#ffffff')
    bl = R('#8ad0ff', dk='#4a88d8', lt='#d0f0ff')
    mo = R('#ffe27a', dk='#e0aa30', lt='#fff6c0')
    # 우아한 S자 몸통
    path = [(3, 15), (8, 13), (14, 15), (20, 19), (25, 18), (29, 12)]
    body = tube(path, 4.4, 1.6)
    # 길게 너울대는 꼬리
    t = PG([(26, 17), (28, 10), (31, 5), (31, 11), (30, 15), (31, 19), (28, 21)])
    c.add(fade(t, 29), fn, edge='out')
    c.add(tube([(9, 9), (14, 8), (19, 12), (24, 15)], 1.4, .8), fn, edge='out')
    c.add(tube([(12, 19), (16, 24), (22, 26)], 1.6, .8), fn, edge='out')
    c.add(body, wh, edge='out')
    # 주황 무늬
    for (x, y, rx, ry) in ((11, 12, 3, 2), (16, 15, 2.4, 2.6), (21, 19, 2, 1.8), (6, 12, 1.4, 1.4)):
        c.pat(E(x, y, rx, ry) & body, og)
    # 이마의 초승달
    c.pat({(4, 11), (5, 10), (6, 10), (4, 12) if False else (4, 13)} & body, mo, keep_tone=False)
    c.put({(5, 11), (5, 12)} & body, wh[1])
    # 수염
    c.put(tube([(1, 17), (0, 20), (2, 23)], .5), og[2])
    c.put(tube([(3, 18), (2, 22), (4, 26)], .5), og[2])
    c.eye(4, 13, 3)
    c.put({(1, 17), (2, 17)}, OUT) if False else None
    # 푸른 도깨비불 (영혼 불꽃)
    for (x, y) in ((8, 5), (16, 3), (26, 26), (5, 27)):
        c.add(PG([(x, y + 3), (x - 1, y + 1), (x, y - 2), (x + 1, y + 1)]) | {(x, y + 2)}, bl, edge='out')
        c.dot(x, y + 1, (255, 255, 255))
    for (x, y) in ((22, 5), (29, 28)):
        c.put({(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}, mo[1])


# ================================================================= 쓰레기
@fish(60, 'j_boot', '낡은 장화')
def _(c):
    r = R('#8a5a34', dk='#4a2c1c', lt='#b88050')
    sole = R('#4a3a38', dk='#241a1e', lt='#6e5a56')
    gr = R('#4ea04a', dk='#24602c', lt='#86d070')
    # 장화 목 + 발등
    shaft = PG([(15, 4), (26, 4), (27, 20), (25, 25), (13, 25), (13, 14)])
    foot = PG([(2, 18), (5, 15), (11, 14), (16, 16), (26, 20), (27, 26), (2, 26)])
    c.add(foot | shaft, r, edge=None)
    c.add(foot | shaft, r, edge='out')
    # 밑창 + 굽
    c.add(PG([(1, 24), (27, 24), (28, 29), (1, 29)]) | RC(21, 24, 29, 30), sole, edge='out')
    c.pat({(x, 24) for x in range(2, 28)}, R('#c8b8a8', dk='#8a7a70', lt='#e8dcd0'), keep_tone=False)
    # 접힌 윗단
    c.add(RC(14, 3, 27, 7), R('#a87444', dk='#5a381e', lt='#d09c64'), edge='out')
    # 끈 구멍 + 끈
    for (x, y) in ((15, 12), (15, 15)):
        pass
    c.put({(13, 11), (14, 12), (13, 13), (14, 14)}, hx('#e8d8b0'))
    c.put({(14, 11), (13, 12), (14, 13), (13, 14)}, hx('#c8b080'))
    # 기운 천 조각과 박음질
    patch = RC(19, 12, 24, 16)
    c.add(patch, R('#6a6e48', dk='#363a24', lt='#8e9468'), edge='out')
    c.put({(20, 12), (22, 12), (20, 16), (22, 16), (19, 14), (24, 14)}, hx('#d8c898'))
    # 앞코 구멍
    c.put(E(5, 21, 2.4, 1.8), OUT)
    c.put({(4, 22), (5, 22), (6, 22)}, hx('#c88a6a'))
    # 물풀과 물방울
    c.add(tube([(26, 5), (29, 9), (28, 14), (30, 18)], .9, .6), gr, edge='out')
    c.add(tube([(22, 5), (24, 0), (22, -2)], .7, .5) & set(), gr)
    c.add(tube([(16, 5), (13, 1)], .8, .6, smooth=False), gr, edge='out')
    c.put({(9, 31) if False else (4, 28), (10, 30) if False else (6, 29)} & set(), hx('#9ad8ff'))
    c.put({(15, 30), (16, 31), (15, 31)} & set(), hx('#9ad8ff'))
    c.dot(2, 30 if False else 28, hx('#9ad8ff'))


@fish(61, 'j_can', '찌그러진 깡통')
def _(c):
    sv = R('#b8c0d0', dk='#5a6480', lt='#e8eef8', hi='#ffffff')
    lb = R('#d8c8b0', dk='#8a7a68', lt='#f4e8d4')
    rd = R('#c8403a', dk='#7a1c2a', lt='#e86a5a')
    rs = R('#b0642a', dk='#6a3418', lt='#d88a44')
    # 통 (오른쪽이 푹 들어간 모양)
    body = RC(7, 9, 24, 27) - {(24, 14), (24, 15), (24, 16), (23, 15), (24, 21), (24, 22), (24, 23), (23, 22), (23, 21)} - {(7, 27), (24, 27), (23, 27)}
    body |= E(15.5, 27, 8.8, 2.2)
    c.add(body, sv, edge='out')
    # 상표 띠
    lab = {(x, y) for (x, y) in body if 14 <= y <= 22}
    c.pat(lab, lb)
    c.pat({(x, y) for (x, y) in lab if 16 <= y <= 19}, rd)
    c.pat({(x, y) for (x, y) in lab if y == 17 and 10 <= x <= 20 and x % 3 != 0}, R('#fff4e0', dk='#e8c8b0', lt='#ffffff'), keep_tone=False)
    # 찌그러짐 그림자 (움푹)
    c.darken({(x, y) for (x, y) in body if (x - 17) ** 2 / 9 + (y - 18) ** 2 / 20 <= 1 and x > 19}, .72)
    c.darken(tube([(8, 24), (12, 21), (11, 25)], .8) & body, .8)
    c.lighten({(9, y) for y in range(10, 14)} | {(9, y) for y in range(23, 26)}, .35)
    # 녹
    for q in ((20, 11), (21, 12), (9, 20), (10, 21), (13, 25), (14, 25), (19, 26), (22, 18)):
        c.pat({q} & body, rs, keep_tone=False)
    # 찌그러진 윗면 + 비뚤게 열린 뚜껑
    c.add(E(15.5, 9, 9, 2.8), R('#d8dff0', dk='#7a86a8', lt='#f4f8ff'), edge='out')
    c.add(E(15.5, 9, 6.4, 1.6), R('#6a7490', dk='#2e344e', lt='#8a94b0'), edge=None, shade=False)
    c.add(PG([(18, 8), (24, 3), (27, 5), (22, 10)]), sv, edge='out')
    c.put({(25, 4), (24, 5)}, sv[3])
    c.put({(15, 5)}, OUT) if False else None


@fish(62, 'j_weed', '물풀 뭉치')
def _(c):
    g1 = R('#4ea04a', dk='#1e5a2c', lt='#86d070')
    g2 = R('#6ab84a', dk='#2e7432', lt='#a8e070')
    g3 = R('#3a8a52', dk='#164a34', lt='#62b878')
    mud = R('#7a5232', dk='#43291c', lt='#a77a4c')
    # 뿌리 진흙 덩이
    c.add(E(15.5, 28, 9, 3), mud, edge='out')
    blades = [
        ([(9, 28), (6, 22), (8, 16), (5, 10), (8, 5)], 2.2, g3),
        ([(22, 28), (26, 22), (23, 15), (27, 9), (24, 3)], 2.2, g3),
        ([(12, 28), (10, 21), (13, 14), (10, 8), (13, 2)], 2.4, g1),
        ([(19, 28), (21, 21), (18, 14), (21, 8), (19, 2)], 2.4, g1),
        ([(15.5, 28), (15, 21), (17, 14), (15, 8), (16, 1)], 2.6, g2),
        ([(15, 28), (9, 25), (4, 26), (2, 23)], 1.8, g2),
        ([(16, 28), (23, 25), (28, 26), (30, 22)], 1.8, g2),
    ]
    for pts, w, col in blades:
        c.add(tube(pts, w, .6), col, edge='out')
    # 둥근 잎과 공기주머니
    c.add(E(4, 13, 2.2, 1.6), g2, edge='out')
    c.add(E(27, 14, 2.2, 1.6), g2, edge='out')
    for q in ((13, 9), (17, 6), (11, 16), (20, 16), (16, 18)):
        c.add(E(q[0], q[1], 1.1, 1.1), R('#d8f4a0', dk='#88c050', lt='#f4ffd0'), edge=None, shade=False)
    c.put({(16, 8)}, hx('#ffffff')) if False else None
    c.dot(2, 28, hx('#9ad8ff')); c.dot(29, 29, hx('#9ad8ff'))


# ================================================================= 시트 만들기
def build():
    sheet = Image.new('RGBA', (N * 63, N), (0, 0, 0, 0))
    for i in range(63):
        c = Cv()
        FISH[i][2](c)
        sheet.alpha_composite(c.image(), (i * N, 0))
    return sheet


def preview(sheet, path, scale=4, per=10):
    """확인용 확대 그림 (#211733 바탕, 번호·이름 표시)."""
    font = None
    for f in ('/usr/share/fonts/opentype/unifont/unifont.otf', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'):
        try:
            font = ImageFont.truetype(f, 14); break
        except Exception:
            pass
    cw, ch = N * scale + 8, N * scale + 26
    rows = (63 + per - 1) // per
    im = Image.new('RGB', (cw * per, ch * rows), (33, 23, 51))
    d = ImageDraw.Draw(im)
    for i in range(63):
        ic = sheet.crop((i * N, 0, i * N + N, N)).resize((N * scale, N * scale), Image.NEAREST)
        x, y = (i % per) * cw + 4, (i // per) * ch
        im.paste(ic, (x, y), ic)
        d.text((x, y + N * scale + 3), '%d %s' % (i, FISH[i][1]), font=font, fill=(220, 210, 240))
    im.save(path)


def main():
    out = os.path.join(ROOT, 'public', 'art', 'fish.png')
    sheet = build()
    sheet.save(out)
    print('저장:', out, sheet.size)
    if len(sys.argv) > 1:
        preview(sheet, sys.argv[1])
        print('미리보기:', sys.argv[1])


if __name__ == '__main__':
    main()
