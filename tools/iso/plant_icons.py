# 온실 수확물 60종 그림 (32×32 픽셀, 직접 그림) → public/art/plants.png  (320×192 = 10열 × 6행, 칸 idx = 열 k%10, 행 k//10)
# python3 tools/iso/plant_icons.py [미리보기폴더]   → 시트를 다시 만들고, 미리보기(4배, 이름 붙은 것)를 폴더에 저장
# idx 0·1·2·9 (약초·이슬·버섯·마나석)는 게임이 따로 쓰는 그림이 있어서 비워 둬요.
# 그리는 방식: 마스크(bool 32×32)를 만들고 → shade()로 왼쪽 위 빛 3~4톤 칠 → outline()으로 1px 어두운 테두리 → 반짝임은 맨 위에.
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

N = 32
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUTLINE = (0x1a, 0x10, 0x24)
NAMES = ["약초", "달빛 이슬", "보라 버섯", "민들레 솜털", "네잎클로버", "박하 잎", "딸기", "당근", "카모마일", "마나석", "라벤더", "들장미 꽃잎", "해바라기 씨", "이끼", "블루베리", "생강", "밀 이삭", "완두콩", "목화솜", "대나무 잎", "솔잎", "단풍잎", "도토리", "토마토", "고추", "옥수수", "은방울꽃", "연꽃 씨", "선인장 즙", "알로에", "튤립 구근", "나팔꽃", "인삼", "광대버섯", "반딧불 꽃가루", "눈송이 꽃", "구름 목화", "달맞이꽃", "요정 버섯", "노래하는 종꽃", "속삭임 덩굴", "유리 열매", "별사과", "화룡초", "꿈꽃", "거울 잎", "그림자 버섯", "번개 콩", "서리 딸기", "바다 포도", "오로라 꽃잎", "혜성 씨앗", "월하향", "해님 호박", "황금 버섯", "수정 장미", "무지개 콩", "시간의 꽃", "영혼 연꽃", "소원 민들레"]

# ---------------------------------------------------------------- 색
def hx(s):
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))

def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

WARM = (255, 244, 200)
SHADE = (58, 30, 96)
def ramp(base, hi=None, lo=None, dk=None):
    """기준색 하나 → (밝음, 기본, 어둠, 더 어둠) 4톤. 그림자는 보라 쪽으로, 빛은 따뜻한 쪽으로."""
    b = hx(base) if isinstance(base, str) else base
    h = hx(hi) if hi else mix(b, WARM, 0.42)
    l = hx(lo) if lo else mix(b, SHADE, 0.38)
    d = hx(dk) if dk else mix(b, (28, 14, 44), 0.66)
    return (h, b, l, d)

def P(*cols):
    return tuple(hx(c) if isinstance(c, str) else c for c in cols)

# ---------------------------------------------------------------- 마스크
YY, XX = np.mgrid[0:N, 0:N]
PX = XX + 0.5
PY = YY + 0.5
def empty():
    return np.zeros((N, N), bool)

def ell(cx, cy, rx, ry=None, ang=0.0):
    ry = rx if ry is None else ry
    dx, dy = PX - cx, PY - cy
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    u, v = dx * c + dy * s, -dx * s + dy * c
    return (u / rx) ** 2 + (v / ry) ** 2 <= 1.0

def rect(x0, y0, x1, y1):
    return (PX >= x0) & (PX <= x1) & (PY >= y0) & (PY <= y1)

def poly(pts):
    im = Image.new('L', (N, N), 0)
    ImageDraw.Draw(im).polygon([(x - 0.5, y - 0.5) for x, y in pts], fill=1)
    return np.array(im, bool)

def line(pts, w=1):
    im = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(im)
    p = [(x - 0.5, y - 0.5) for x, y in pts]
    d.line(p, fill=1, width=w)
    if w == 1:
        pass
    return np.array(im, bool)

def taper(p0, p1, r0, r1, cap=True):
    """p0→p1 로 굵기가 r0→r1 로 변하는 막대(캡슐). 당근·뿌리·줄기용."""
    x0, y0 = p0; x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    t = ((PX - x0) * dx + (PY - y0) * dy) / L2
    tc = np.clip(t, 0, 1)
    qx, qy = x0 + tc * dx, y0 + tc * dy
    d = np.hypot(PX - qx, PY - qy)
    r = r0 + (r1 - r0) * tc
    m = d <= r
    if not cap:
        m &= (t >= 0) & (t <= 1)
    return m

def leaf(p0, p1, w, skew=0.0, pw=0.8, side=1.0):
    """p0(줄기쪽)→p1(끝) 뾰족한 잎. w=최대 반폭, pw 작을수록 둥글다, skew -1..1 은 가장 넓은 곳 위치."""
    x0, y0 = p0; x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    L = math.sqrt(L2)
    t = ((PX - x0) * dx + (PY - y0) * dy) / L2
    s = ((PX - x0) * (-dy) + (PY - y0) * dx) / L
    tt = np.clip(t, 0, 1)
    k = 0.5 + 0.25 * skew
    tw = np.where(tt < k, tt / k, (1 - tt) / (1 - k)) * math.pi / 2
    prof = w * np.sin(tw) ** pw
    return (t >= 0) & (t <= 1) & (np.abs(s) <= prof + 0.0)

def heart(cx, cy, s, ang=0.0):
    """하트 (끝이 아래). ang 만큼 시계로 돌림. s=크기."""
    dx, dy = PX - cx, PY - cy
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    u, v = dx * c + dy * sn, -dx * sn + dy * c
    x = u / s
    y = -v / s - 0.1
    return (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0

def star(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180.0 / n)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts)

def polar(cx, cy, r, ang):
    a = math.radians(ang)
    return (cx + r * math.cos(a), cy + r * math.sin(a))

def shift(m, dx, dy):
    r = np.zeros_like(m)
    ys = slice(max(dy, 0), N + min(dy, 0)); yd = slice(max(-dy, 0), N + min(-dy, 0))
    xs = slice(max(dx, 0), N + min(dx, 0)); xd = slice(max(-dx, 0), N + min(-dx, 0))
    r[ys, xs] = m[yd, xd]
    return r

def grow(m, n=1):
    for _ in range(n):
        m = m | shift(m, 1, 0) | shift(m, -1, 0) | shift(m, 0, 1) | shift(m, 0, -1)
    return m

def erode(m, n=1):
    for _ in range(n):
        m = m & shift(m, 1, 0) & shift(m, -1, 0) & shift(m, 0, 1) & shift(m, 0, -1)
    return m


def bez(p0, p1, p2, p3=None, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        if p3 is None:
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        else:
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out

def tube(path, r0, r1):
    """곡선 경로를 따라 굵기가 r0→r1 로 변하는 관."""
    m = empty()
    n = len(path)
    for i, (x, y) in enumerate(path):
        r = r0 + (r1 - r0) * i / (n - 1)
        m |= ell(x, y, r, r)
    return m

def mirror(pts, cx=16):
    return [(2 * cx - x, y) for x, y in pts]

def mask_of(c):
    return c.body[:, :, 3] > 0


def prof(cx, y0, y1, fn):
    """위에서 아래로 반폭 fn(t) (t=0..1)인 좌우대칭 모양."""
    m = empty()
    for y in range(N):
        t = (y + 0.5 - y0) / (y1 - y0)
        if 0 <= t <= 1:
            w = fn(t)
            m[y] = np.abs(PX[y] - cx) <= w
    return m

def mushroom(c, cx, by, cw, ch, sw, sh, cap, stem_pal, spots=(), spot_col=(255, 255, 255), lean=0.0):
    """버섯 하나. by=밑동 y, cw=갓 반폭, ch=갓 높이, sw=줄기 반폭, sh=줄기 높이."""
    top = by - sh
    st = rect(cx - sw, top - 1, cx + sw, by) | ell(cx, by - 0.6, sw + 0.9, 1.4)
    c.shade(st, stem_pal, R=max(1.6, sw), soft=0)
    capm = ell(cx, top + 0.5, cw, ch) & rect(0, 0, 32, top + 0.5)
    c.shade(capm, cap, R=max(2.0, ch * 0.9), soft=1)
    for (dx, dy, r) in spots:
        c.flat(ell(cx + dx, top + dy, r), spot_col)
    return capm


def flame(cx, by, w, h, lean=0.0, wob=0.0):
    """불꽃 모양: 밑동(by)에서 위로 h, 최대 반폭 w, lean 만큼 끝이 기울고 wob 만큼 출렁."""
    m = empty()
    for y in range(N):
        t = (by - (y + 0.5)) / h   # 0 밑동 → 1 끝
        if 0 <= t <= 1:
            ww = w * (math.sin(math.pi * min(1, t * 0.9 + 0.05) ** 0.7) ** 0.9) * (1 - t * 0.15)
            if t > 0.95:
                ww = 0
            ccx = cx + lean * t ** 2 + wob * math.sin(t * 6.0)
            m[y] = np.abs(PX[y] - ccx) <= ww
    return m

def blend(a, b, t):
    return mix(a, b, t)

def stops(*cols):
    cs = [hx(c) for c in cols]
    def f(t):
        t = min(max(t, 0), 0.9999) * (len(cs) - 1)
        i = int(t)
        return mix(cs[i], cs[i + 1], t - i)
    return f

# ---------------------------------------------------------------- 그림판
LIGHT = np.array([-0.5, -0.6, 0.62]); LIGHT /= np.linalg.norm(LIGHT)

def depth_map(mask):
    ins = np.argwhere(mask)
    pad = np.pad(mask, 1)
    outs = np.argwhere(~pad) - 1
    d = np.zeros((N, N))
    if len(ins) == 0:
        return d
    dist = np.sqrt(((ins[:, None, :] - outs[None, :, :]) ** 2).sum(-1)).min(1)
    for (y, x), v in zip(ins, dist):
        d[y, x] = v - 0.5
    return d

class Cv:
    def __init__(self):
        self.body = np.zeros((N, N, 4), np.uint8)
        self.back = np.zeros((N, N, 4), np.uint8)   # 테두리 뒤(빛무리)
        self.front = np.zeros((N, N, 4), np.uint8)  # 테두리 앞(반짝임·글자)
        self.nooutline = empty()

    # --- 기본 칠
    def flat(self, mask, col, a=255, layer=None):
        L = self.body if layer is None else layer
        L[mask] = (*col, a)

    def px(self, x, y, col, a=255, layer=None):
        L = self.body if layer is None else layer
        if 0 <= x < N and 0 <= y < N:
            L[int(y), int(x)] = (*col, a)

    def pts(self, lst, col, layer=None):
        for x, y in lst:
            self.px(x, y, col, layer=layer)

    def art(self, rows, pal, ox=0, oy=0, layer=None):
        """글자 지도. pal = {'a': color,...}, '.'/' ' 투명."""
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in '. ':
                    continue
                self.px(ox + i, oy + j, pal[ch], layer=layer)

    def shade_idx(self, mask, R=None, soft=1, bias=0.0, light=None):
        d = depth_map(mask)
        if R is None:
            R = max(1.5, min(d.max(), 7.0))
        t = np.clip(d / R, 0, 1)
        h = R * np.sqrt(1 - (1 - t) ** 2)
        h[~mask] = 0
        for _ in range(soft):
            hp = np.pad(h, 1, mode='edge')
            hs = (hp[1:-1, 1:-1] * 4 + hp[:-2, 1:-1] + hp[2:, 1:-1] + hp[1:-1, :-2] + hp[1:-1, 2:]) / 8
            h = np.where(mask, hs, 0)
        gy, gx = np.gradient(h)
        nrm = np.sqrt(gx ** 2 + gy ** 2 + 1)
        Lv = LIGHT if light is None else np.array(light) / np.linalg.norm(light)
        v = (-gx * Lv[0] - gy * Lv[1] + Lv[2]) / nrm + bias
        idx = np.full((N, N), 1)
        idx[v >= 0.86] = 0
        idx[v < 0.5] = 2
        idx[v < 0.22] = 3
        return idx

    def shade(self, mask, pal, R=None, soft=1, bias=0.0, light=None):
        """마스크를 왼쪽 위 빛으로 3~4톤 칠. pal=(밝음,기본,어둠,더어둠). R=둥근 정도(픽셀)."""
        if not mask.any():
            return
        idx = self.shade_idx(mask, R, soft, bias, light)
        for y, x in np.argwhere(mask):
            k = idx[y, x]
            if len(pal) <= 3 and k == 3:
                k = 2
            self.body[y, x] = (*pal[k], 255)

    def shade_grad(self, mask, colfn, R=None, soft=1, bias=0.0):
        """위치마다 기준색이 다른 칠 (오로라·무지개). colfn(x,y) → (r,g,b) 기준색."""
        if not mask.any():
            return
        idx = self.shade_idx(mask, R, soft, bias)
        cache = {}
        for y, x in np.argwhere(mask):
            b = colfn(x, y)
            if b not in cache:
                cache[b] = ramp(b)
            self.body[y, x] = (*cache[b][idx[y, x]], 255)

    def outline(self, col=OUTLINE):
        a = self.body[:, :, 3] > 0
        near = shift(a, 1, 0) | shift(a, -1, 0) | shift(a, 0, 1) | shift(a, 0, -1)
        o = near & ~a & ~self.nooutline
        self.body[o] = (*col, 255)

    # --- 빛무리·반짝임
    def glow(self, cx, cy, r, col, a0=70, rings=3, mask=None):
        """뒤쪽 은은한 빛: 반지름 r 안쪽부터 바깥으로 점점 옅게."""
        dist = np.hypot(PX - cx, PY - cy)
        for k in range(rings):
            ring = (dist <= r + k * 1.6) & (dist > -1)
            al = int(a0 * (1 - k / (rings + 0.3)))
            sel = ring & (self.back[:, :, 3] < al)
            self.back[sel] = (*col, al)

    def glow_mask(self, mask, col, a0=64, rings=3):
        m = mask
        for k in range(rings):
            m2 = grow(m, 1)
            al = int(a0 * (1 - k / (rings + 0.3)))
            ring = m2 & ~m if k else m2
            sel = ring & (self.back[:, :, 3] < al)
            self.back[sel] = (*col, al)
            m = m2

    def spark(self, x, y, col=(255, 255, 255), big=False):
        L = self.front
        L[int(y), int(x)] = (*col, 255)
        arms = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in arms:
            xx, yy = int(x) + dx, int(y) + dy
            if 0 <= xx < N and 0 <= yy < N:
                L[yy, xx] = (*col, 255 if big else 190)
        if big:
            for dx, dy in arms:
                xx, yy = int(x) + dx * 2, int(y) + dy * 2
                if 0 <= xx < N and 0 <= yy < N:
                    L[yy, xx] = (*col, 150)

    def dot(self, x, y, col, a=255):
        if 0 <= x < N and 0 <= y < N:
            self.front[int(y), int(x)] = (*col, a)

    def image(self):
        im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
        for L in (self.back, self.body, self.front):
            im.alpha_composite(Image.fromarray(L, 'RGBA'))
        return im

def px_line(c, p0, p1, col, layer=None):
    """1px 선(브레젠험)."""
    x0, y0 = int(round(p0[0] - 0.5)), int(round(p0[1] - 0.5))
    x1, y1 = int(round(p1[0] - 0.5)), int(round(p1[1] - 0.5))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        c.px(x0, y0, col, layer=layer)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy: err += dy; x0 += sx
        if e2 <= dx: err += dx; y0 += sy

def vein(c, p0, p1, col, mask=None):
    """마스크 안쪽에서만 그리는 잎맥."""
    tmp = Cv()
    px_line(tmp, p0, p1, col)
    sel = tmp.body[:, :, 3] > 0
    if mask is not None:
        sel &= mask
    c.body[sel] = tmp.body[sel]

# ---------------------------------------------------------------- 그림 목록
ICONS = {}
def icon(idx):
    def deco(f):
        ICONS[idx] = f
        return f
    return deco

# 자주 쓰는 색
GREEN = ramp('#5cc04a', hi='#b8ec78', lo='#2f8a46', dk='#1c5a3c')
LEAFG = ramp('#4aa84a', hi='#a8e070', lo='#2a7a44', dk='#1a4a38')
STEM = ramp('#4a9a3c', hi='#90d060', lo='#2c6a3a', dk='#1c4430')
WHITE = P('#ffffff', '#efe9fa', '#c4b8e0', '#8a7cb4')
CREAM = P('#fffbe8', '#f4ead0', '#d0bfa0', '#9a8670')

def stem(c, pts, w=2, pal=STEM):
    m = line(pts, w)
    c.shade(m, pal, R=1.4, soft=0)
    return m

# === ICONS ===

def petal_ring(c, cx, cy, n, r0, r1, w, pal, a0=0.0, R=1.8, pw=0.55, skew=0.3):
    for i in range(n):
        a = a0 + i * 360.0 / n
        p0 = polar(cx, cy, r0, a); p1 = polar(cx, cy, r1, a)
        m = leaf(p0, p1, w, skew=skew, pw=pw)
        c.shade(m, pal, R=R, soft=0)

@icon(3)  # 민들레 솜털
def _(c):
    stem(c, [(16, 20), (15, 25), (16, 30)], 2)
    cx, cy = 16, 12.5
    head = ell(cx, cy, 8.2)
    pal = P('#ffffff', '#ece8f8', '#bfb8dc', '#8a82b0')
    c.shade(head, pal, R=7, soft=1)
    for i in range(16):
        a = i * 22.5 + 5
        col = pal[0] if i % 2 == 0 else pal[2]
        px_line(c, polar(cx, cy, 2.2, a), polar(cx, cy, 8.4, a), col)
        c.px(*[int(v) for v in polar(cx, cy, 9.6, a)], pal[1] if i % 2 else pal[0])
    c.flat(ell(cx, cy, 1.6), P('#d8d0a0')[0])
    c.px(15, 11, hx('#fff6c0'))

@icon(4)  # 네잎클로버
def _(c):
    cx, cy = 16, 14
    stem(c, [(16, 15), (17, 21), (14.5, 26), (13, 30)], 2)
    for ang in (225, 315, 135, 45):
        a = math.radians(ang)
        d = 5.6
        lx, ly = cx + d * math.cos(a), cy + d * math.sin(a)
        # 끝이 가운데로 향하는 하트: 하트 +y(끝쪽)을 가운데로 돌림
        m = heart(lx, ly, 4.9, ang=ang + 90)
        c.shade(m, GREEN, R=4, soft=1)
        px_line(c, (cx + 1.2 * math.cos(a), cy + 1.2 * math.sin(a)), (lx + 3.2 * math.cos(a), ly + 3.2 * math.sin(a)), GREEN[0])
    c.flat(ell(cx, cy, 1.4), GREEN[2])

@icon(5)  # 박하 잎
def _(c):
    MINT = ramp('#4ccf8c', hi='#c0ffd0', lo='#27956c', dk='#17584a')
    stem(c, [(15.5, 30), (15, 22), (16, 14), (16, 6)], 2, pal=ramp('#3a9a60', hi='#7ad090', lo='#25704c', dk='#17483a'))
    specs = [((15, 23), (7, 19.5), 3.5), ((15.5, 22), (24, 17.5), 3.5),
             ((15.5, 15), (8, 10.5), 3.2), ((16, 14.5), (24, 9.5), 3.2),
             ((16, 9), (16.5, 2), 2.6)]
    for p0, p1, w in specs:
        m = leaf(p0, p1, w, skew=0.2, pw=0.7)
        c.shade(m, MINT, R=2.8, soft=0)
        px_line(c, p0, ((p0[0] * 0.25 + p1[0] * 0.75), (p0[1] * 0.25 + p1[1] * 0.75)), MINT[0])
    c.px(7, 20, MINT[0]); 

@icon(6)  # 딸기
def _(c):
    RED = ramp('#e83a4a', hi='#ff8f90', lo='#b01c44', dk='#6a1038')
    body = ell(16, 14.5, 9.6, 8) | taper((16, 15), (16, 26), 9.2, 2.4)
    c.shade(body, RED, R=7, soft=1)
    inner = erode(body, 2)
    k = 0
    for y in range(11, 26, 3):
        for x in range(8 + (k % 2) * 2, 26, 4):
            if inner[y, x]:
                c.px(x, y, hx('#ffe27a')); c.px(x, y + 1, hx('#9a1c40'))
        k += 1
    # 꼭지
    for p1 in [(6, 11), (10, 15.5), (22, 15.5), (26, 11), (16, 16.5)]:
        m = leaf((16, 8.5), p1, 2.4, skew=0.3, pw=0.7)
        c.shade(m, GREEN, R=2, soft=0)
    c.flat(taper((16, 9), (17.5, 3), 1.3, 1.0), STEM[2])
    c.px(16, 7, STEM[0])
    c.px(10, 14, hx('#ffc0c0')); c.px(11, 13, hx('#ffd8d8'))

@icon(7)  # 당근
def _(c):
    OR = ramp('#f08a22', hi='#ffc070', lo='#c4561c', dk='#7a2c20')
    p0, p1 = (21, 12), (6, 27.5)
    body = taper(p0, p1, 6.2, 0.7)
    c.shade(body, OR, R=5, soft=1)
    for t in (0.3, 0.52, 0.72):
        x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
        vein(c, (x - 4, y - 4.4), (x - 1.5, y - 1.9), OR[2], body)
        vein(c, (x + 1, y + 1), (x + 3, y + 3), OR[3], body)
    for p, w in [(((22.5, 9), (20, 1.2)), 2.0), (((22.5, 9), (27, 2)), 2.0), (((23, 9.5), (30, 7)), 1.8), (((21.5, 9.5), (14.5, 4.5)), 1.7)]:
        m = leaf(p[0], p[1], w, skew=0.2, pw=0.7)
        c.shade(m, GREEN, R=1.8, soft=0)
        vein(c, p[0], p[1], GREEN[0], m)

@icon(8)  # 카모마일
def _(c):
    stem(c, [(16, 22), (16, 30)], 2)
    c.shade(leaf((16, 28), (24, 24), 2.4, pw=0.7), GREEN, R=2, soft=0)
    petal_ring(c, 16, 12.5, 12, 2.5, 11.6, 2.5, WHITE, a0=-90, R=1.8, pw=0.5)
    YEL = ramp('#ffd23c', hi='#fff290', lo='#e0961c', dk='#a05a1c')
    c.shade(ell(16, 12.5, 4.3), YEL, R=4, soft=1)
    c.px(14, 11, hx('#fffbc0'))

@icon(10)  # 라벤더
def _(c):
    LAV = ramp('#9a6ee0', hi='#d6b8ff', lo='#6a46b8', dk='#40286e')
    LAV2 = ramp('#b48af0', hi='#e8d4ff', lo='#7c58c8', dk='#4a2c80')
    stem(c, [(16, 30), (16.5, 21), (17, 14)], 2)
    c.shade(leaf((16, 29), (8.5, 23.5), 2, pw=0.7), GREEN, R=1.6, soft=0)
    c.shade(leaf((16, 28), (24, 22.5), 2, pw=0.7), GREEN, R=1.6, soft=0)
    # 꽃송이: 위로 갈수록 작고 좁게, 좌우 번갈아
    rows = [(21, 3.4), (19, 3.2), (17, 3.0), (15, 2.8), (13, 2.5), (11, 2.2), (9, 1.9), (7, 1.5), (5, 1.1), (3.5, 0.0)]
    for k, (y, w) in enumerate(rows):
        x0 = 17.0 - (21 - y) * 0.10
        r = 2.2 if w > 1.6 else 1.8
        pal = LAV if k % 2 == 0 else LAV2
        if w == 0:
            c.shade(ell(x0, y, 1.6, 1.8), LAV2, R=1.6, soft=0)
            continue
        for sgn in (-1, 1):
            yy = y + (0.6 if sgn > 0 else -0.5)
            c.shade(ell(x0 + sgn * w * 0.62, yy, r, r * 0.9), pal if sgn < 0 else LAV, R=2, soft=0)
    c.shade(ell(17.1, 14.5, 1.9, 1.6), LAV, R=1.6, soft=0)

@icon(11)  # 들장미 꽃잎 (들장미 꽃: 하트 모양 꽃잎 5장)
def _(c):
    ROSE = ramp('#f06a92', hi='#ffc0d0', lo='#c4386c', dk='#7a1c4c')
    for k in range(5):
        ang = -90 + k * 72
        a = math.radians(ang)
        lx, ly = 16 + 6.6 * math.cos(a), 15 + 6.6 * math.sin(a)
        m = heart(lx, ly, 5.3, ang=ang + 90) & ~ell(*polar(16, 15, 12.6, ang), 1.5, 1.5)
        c.shade(m, ROSE, R=4.2, soft=1)
        vein(c, polar(16, 15, 3, ang), polar(16, 15, 9.5, ang), ROSE[2], m)
    c.shade(ell(16, 15, 3.4), P('#fff6c8', '#ffe27a', '#e0a030', '#9a6020'), R=3, soft=0)
    for dx, dy in [(-1, -2), (1, -2), (-2, 0), (2, 0), (0, 1), (-1, 2), (1, 2)]:
        c.px(15 + dx + (1 if dx >= 0 else 0), 14 + dy, hx('#b8641c') if (dx + dy) % 2 else hx('#fff0a0'))

@icon(12)  # 해바라기 씨
def _(c):
    SF = ramp('#ffc61c', hi='#fff070', lo='#e08a10', dk='#a05010')
    BR = ramp('#6a3c1c', hi='#b0743a', lo='#3e2214', dk='#24120c')
    stem(c, [(16, 24), (16, 30)], 2)
    petal_ring(c, 16, 13.5, 16, 4, 13, 2.2, SF, a0=-90, R=1.7, pw=0.55, skew=0.1)
    c.shade(ell(16, 13.5, 6.4), BR, R=5, soft=1)
    inner = erode(ell(16, 13.5, 6.4), 1)
    for k, (dx, dy) in enumerate([(-3, -3), (0, -4), (3, -3), (-4, 0), (-1.5, -1), (1.5, -1), (4, 0), (-3, 2.5), (0, 2), (3, 2.5), (-1.5, 4.5), (1.5, 4.5)]):
        x, y = int(16 + dx), int(13 + dy)
        if inner[y, x]:
            c.px(x, y, BR[0] if k % 2 == 0 else BR[2])


@icon(13)  # 이끼
def _(c):
    MOSS = ramp('#6aa83c', hi='#c4ec74', lo='#3e7a3a', dk='#24503a')
    # 포자 줄기
    for (x0, x1, y1) in [(11, 9, 5), (16, 17, 3), (21, 24, 6)]:
        px_line(c, (x0, 16), (x1, y1), hx('#8a6a3c'))
        c.px(x1 - 0, y1 - 1, hx('#c8903c')); c.px(x1, y1 - 2 if y1 > 3 else y1 - 1, hx('#e8b858')) if False else None
        c.flat(ell(x1 + 0.5, y1 - 0.3, 1.5, 1.8), hx('#c8903c'))
        c.px(x1 - 1, y1 - 1, hx('#f0d080'))
    base = (ell(9, 22.5, 6.2, 5) | ell(16, 19.5, 8, 7) | ell(23.5, 22.5, 6.2, 5) | ell(16, 25, 13, 4.2)) & rect(0, 0, 32, 29)
    c.shade(base, MOSS, R=6, soft=1)
    inner = erode(base, 1)
    import random
    rnd = random.Random(13)
    for _i in range(34):
        x, y = rnd.randint(4, 27), rnd.randint(14, 27)
        if inner[y, x]:
            c.px(x, y, MOSS[0] if rnd.random() < 0.5 else MOSS[3])
    for x, y in [(11, 17), (12, 18), (19, 15), (20, 16), (7, 21), (24, 21)]:
        c.px(x, y, MOSS[0])

@icon(14)  # 블루베리
def _(c):
    BL = ramp('#4a62d0', hi='#a8bcff', lo='#2e3a9a', dk='#1c2064')
    LEAFP = GREEN
    c.shade(leaf((17, 6), (27, 3), 2.2, pw=0.7), LEAFP, R=1.8, soft=0)
    def berry(cx, cy, r):
        c.shade(ell(cx, cy, r), BL, R=r, soft=1)
        # 꼭지(왕관)
        crown = [(0, -r * 0.35), (-1, -r * 0.35 - 1), (1, -r * 0.35 - 1), (-2, -r * 0.35), (2, -r * 0.35), (0, -r * 0.35 + 1)]
        for dx, dy in crown[:1]:
            pass
        x, y = int(cx), int(cy - r * 0.3)
        c.px(x, y, BL[3]); c.px(x - 1, y - 1, BL[3]); c.px(x + 1, y - 1, BL[3]); c.px(x - 1, y + 1, BL[3]); c.px(x + 1, y + 1, BL[3])
        c.px(x, y - 1, hx('#7a8ae0')); c.px(x - 1, y, hx('#7a8ae0')); c.px(x + 1, y, hx('#7a8ae0')); c.px(x, y + 1, hx('#7a8ae0'))
        c.px(int(cx - r * 0.5), int(cy - r * 0.2) + 0, BL[0])
        c.px(int(cx - r * 0.5) - 0, int(cy - r * 0.2) + 1, BL[0])
    berry(15.5, 11.5, 6.3)
    berry(9.5, 20.5, 6.3)
    berry(21, 20.5, 6.8)

@icon(15)  # 생강
def _(c):
    G = ramp('#d8a860', hi='#f6dc9a', lo='#a8743c', dk='#6a4224')
    m = empty()
    m |= taper((9, 21.5), (24, 19), 5, 4.6)
    m |= taper((12, 20), (10.5, 9.5), 3.4, 2.8)
    m |= taper((18, 19), (20.5, 7.5), 3.6, 2.8)
    m |= taper((24, 19.5), (28, 12.5), 3.2, 2.6)
    m |= taper((9, 22), (4, 27), 3.4, 2.6)
    m |= taper((15, 23), (17, 28), 3, 2.4)
    c.shade(m, G, R=4.5, soft=1)
    # 마디 줄무늬
    for (x0, y0, x1, y1) in [(7.5, 11, 12.5, 11.8), (8.5, 14.5, 13.5, 15), (17, 11, 22, 11.2), (17, 14.5, 22.5, 14.5), (26, 15, 29.5, 16), (13, 25, 17, 26)]:
        vein(c, (x0, y0), (x1, y1), G[2], m)
    for (x0, y0, x1, y1) in [(9, 15.5, 12, 15.8), (18, 16, 21, 16)]:
        vein(c, (x0, y0), (x1, y1), G[0], m)
    # 분홍 새싹 끝
    for (x, y) in [(10, 8), (11, 8), (20, 6), (21, 6), (28, 11), (29, 12)]:
        c.px(x, y, hx('#f0a0a0') if (x + y) % 2 == 0 else hx('#d8707c'))
    # 단면
    c.flat(ell(4.8, 26.3, 1.6, 1.3, ang=-40), hx('#f6e08a'))

@icon(16)  # 밀 이삭
def _(c):
    W = ramp('#e8b840', hi='#fff58a', lo='#b07a20', dk='#6a4418')
    STK = ramp('#c8b050', hi='#ece080', lo='#8a7c30', dk='#5a4c24')
    c.shade(tube(bez((16.5, 30), (15, 26.5), (16.2, 21)), 1.1, 1.0), STK, R=1.2, soft=0)
    c.shade(leaf((15.5, 30), (5, 22), 2.2, pw=0.7), P('#b8e060', '#8cc84c', '#5a9a40', '#2c5a34'), R=1.6, soft=0)
    ax = 16.2
    # 까끄라기: 위쪽 낟알에서 길게
    for (x0, y0, x1, y1, col) in [(ax - 2, 7.5, ax - 6.5, 1.5, '#f0cc6c'), (ax - 0.5, 4, ax - 1.5, 0, '#f0cc6c'), (ax + 2, 7.5, ax + 6.5, 1.5, '#c8962c'), (ax + 1, 4.2, ax + 3.5, 0.2, '#c8962c')]:
        px_line(c, (x0, y0), (x1, y1), hx(col))
    for i in range(6):
        y = 21.5 - i * 2.9
        c.shade(ell(ax - 2.3, y + 0.9, 1.9, 2.9, ang=-20), W, R=1.8, soft=0)
        c.shade(ell(ax + 2.3, y - 0.5, 1.9, 2.9, ang=20), W, R=1.8, soft=0)
    c.shade(ell(ax, 4.6, 1.8, 2.8), W, R=1.7, soft=0)

@icon(17)  # 완두콩
def _(c):
    POD = ramp('#3c9a3c', hi='#88d058', lo='#26703c', dk='#164832')
    INN = ramp('#f6fcc8', hi='#ffffee', lo='#d8ec98', dk='#7c9c50')
    PEA = ramp('#7ee04c', hi='#eaffa4', lo='#38a83c', dk='#1e6a38')
    p0, p1 = (4.5, 25.5), (28, 7)
    pod = leaf(p0, p1, 7.4, skew=0.0, pw=0.65)
    c.shade(pod, POD, R=4, soft=1)
    inn = leaf((6.8, 23.2), (25.8, 8.8), 5.6, skew=0.0, pw=0.7)
    c.flat(inn, INN[1])
    c.flat(inn & ~shift(inn, 1, 1), INN[3])
    c.flat(inn & ~shift(inn, 1, 0) & ~(inn & ~shift(inn, 1, 1)), INN[2])
    for t in (0.2, 0.4, 0.6, 0.8):
        tt = t * 0.8 + 0.1
        x = p0[0] + (p1[0] - p0[0]) * tt - 0.7
        y = p0[1] + (p1[1] - p0[1]) * tt - 0.9
        c.flat(ell(x + 0.6, y + 0.8, 3.3), INN[3])
        c.shade(ell(x, y, 3.0), PEA, R=3.0, soft=0)
        c.px(int(x - 1), int(y - 1), PEA[0]); c.px(int(x - 1), int(y - 2), hx('#f0ffc0'))
    c.flat(taper((5, 26), (2, 29), 1.3, 0.9), STEM[1])
    px_line(c, (3, 29), (5, 30.5), STEM[1])
    c.shade(leaf((5.5, 24.5), (9.5, 29.5), 2, pw=0.7), GREEN, R=1.5, soft=0)

@icon(18)  # 목화솜
def _(c):
    CT = P('#ffffff', '#f4f0fc', '#cdc2e6', '#968ac0')
    HK = ramp('#8a5a38', hi='#c08a5c', lo='#5c3a28', dk='#38222a')
    for (x, y, r) in [(16, 15.5, 7.2), (7.5, 17.5, 4.4), (24.5, 17.5, 4.4), (9.5, 11, 4.8), (22.5, 11, 4.8), (16, 6.8, 5.2)]:
        c.flat(ell(x, y, r + 0.9), CT[2])
        c.shade(ell(x, y, r), CT, R=r, soft=0)
    for p1, w in [((3.5, 14.5), 3.2), ((28.5, 14.5), 3.2), ((8, 24), 3.0), ((24, 24), 3.0)]:
        m = leaf((16, 29.5), p1, w, skew=0.1, pw=0.95)
        c.shade(m, HK, R=2.6, soft=0)
    m = leaf((16, 30), (16, 21.5), 3.0, skew=0.1, pw=0.9)
    c.shade(m, HK, R=2.6, soft=0)
    c.px(12, 24, HK[0]); c.px(20, 25, HK[2])

@icon(19)  # 대나무 잎
def _(c):
    BM = ramp('#7ac050', hi='#d0f58a', lo='#3a8a44', dk='#205a3a')
    BS = ramp('#4aa06a', hi='#a8e8a0', lo='#2a7050', dk='#184838')
    culm = taper((3.5, 31), (10.5, 20), 2.6, 2.3)
    c.shade(culm, BS, R=2.4, soft=0)
    for (x, y) in [(5.6, 27.5), (8.6, 23)]:   # 마디
        c.flat(ell(x, y, 3.4, 1.2, ang=-58), BS[3]); c.px(int(x) - 1, int(y) - 1, BS[0]); c.px(int(x), int(y) - 2, BS[0])
    branch = tube(bez((10, 20.5), (14, 17), (22, 14), (27, 8)), 1.0, 0.7)
    c.shade(branch, BS, R=1.0, soft=0)
    for (t, big) in [(0.20, 1.0), (0.50, 0.95), (0.85, 0.8)]:
        pth = bez((10, 20.5), (14, 17), (22, 14), (27, 8))
        x, y = pth[int(t * 40)]
        ang = -48 + (t * 20)
        for sgn in (-1, 1):
            p1 = polar(x, y, 12.5 * big, ang + sgn * 38)
            m = leaf((x, y), p1, 2.0, skew=-0.1, pw=0.9)
            c.shade(m, BM, R=2, soft=0)
            vein(c, (x, y), p1, BM[0], m)
    m = leaf((26.5, 8.5), (29.5, 1.5), 1.7, skew=0, pw=0.9)
    c.shade(m, BM, R=1.7, soft=0)

@icon(20)  # 솔잎
def _(c):
    PN = ramp('#3a9a5a', hi='#8ae08a', lo='#25704a', dk='#164a3a')
    TW = ramp('#9a6a3c', hi='#d09a5c', lo='#6a4428', dk='#3e2624')
    c.shade(tube(bez((3, 30), (11, 27), (19, 17), (25, 13.5)), 1.7, 1.0), TW, R=1.5, soft=0)
    tufts = [(8.5, 28, -135, 10), (14.5, 24, -115, 11), (20, 18.5, -95, 11), (25, 13.5, -68, 10)]
    for (x, y, base, L) in tufts:
        n = 7
        for i in range(n):
            a = base + (i - (n - 1) / 2) * 12
            LL = L - abs(i - (n - 1) / 2) * 0.8
            p1 = polar(x, y, LL, a)
            px_line(c, (x + 1, y + 1), (p1[0] + 1, p1[1] + 1), PN[2])
        for i in range(n):
            a = base + (i - (n - 1) / 2) * 12
            LL = L - abs(i - (n - 1) / 2) * 0.8
            p1 = polar(x, y, LL, a)
            px_line(c, (x, y), p1, PN[0] if i % 2 == 0 else PN[1])
        c.flat(ell(x, y, 1.5, 1.5), TW[1]); c.px(int(x), int(y), TW[3]); c.px(int(x) - 1, int(y) - 1, TW[0])

@icon(21)  # 단풍잎
def _(c):
    MP = P('#ffc84a', '#f0802a', '#cc3a22', '#7a1c2c')
    R = [(16, 2), (18.2, 6.5), (21, 5), (20.5, 10.5), (26, 8.5), (24.5, 13.5), (29.5, 15.5), (23.5, 18.8), (24.5, 23), (17.5, 21.5)]
    pts = R + [(16, 23.5)] + mirror(R[::-1])
    m = poly(pts) | taper((16, 22), (16.5, 30), 1.2, 1.0)
    c.shade(m, MP, R=7, soft=1)
    for tip in [(16, 4), (21, 7), (26, 10), (27, 15), (23, 22), (11, 7), (6, 10), (5, 15), (9, 22)]:
        vein(c, (16, 22), tip, MP[2], m)
    vein(c, (16, 22), (16, 30), MP[3], m)
    c.px(14, 6, MP[0]); c.px(13, 9, MP[0])

@icon(22)  # 도토리
def _(c):
    NUT = ramp('#c8883a', hi='#f4c878', lo='#8a5224', dk='#4e2c1c')
    CAP = ramp('#8a5a30', hi='#c8905a', lo='#5a3622', dk='#34201c')
    nut = (ell(16, 19.5, 7.2, 8) | taper((16, 20), (16, 28), 6.2, 1.0)) & rect(0, 12, 32, 32)
    c.shade(nut, NUT, R=6, soft=1)
    cap = ell(16, 13.5, 9.3, 6.4) & rect(0, 0, 32, 16.5)
    c.shade(cap, CAP, R=5, soft=1)
    for y in range(8, 16):
        for x in range(6, 27):
            if cap[y, x] and (x + y) % 3 == 0 and erode(cap, 1)[y, x]:
                c.px(x, y, CAP[2] if (y % 2) else CAP[0])
    c.flat(taper((16, 8), (17.5, 3.5), 1.5, 1.2), CAP[1]); c.px(16, 5, CAP[0]); c.px(18, 3, CAP[3])
    c.px(12, 21, NUT[0]); c.px(12, 22, NUT[0]); c.px(13, 19, NUT[0])
    c.px(21, 22, NUT[3])

@icon(23)  # 토마토
def _(c):
    T = ramp('#e8301c', hi='#ff9070', lo='#b01a30', dk='#6a1034')
    body = ell(16, 18, 11.2, 9.6) | ell(10.5, 16, 6, 8) | ell(21.5, 16, 6, 8)
    body &= ~ell(16, 8.5, 2.2, 1.5)
    c.shade(body, T, R=8, soft=1)
    # 꼭지 (별 모양 꽃받침)
    for p1 in [(7.5, 12), (11, 15.5), (21, 15.5), (24.5, 12), (16, 16)]:
        m = leaf((16, 9.5), p1, 2.2, skew=0.3, pw=0.7)
        c.shade(m, GREEN, R=1.8, soft=0)
    c.flat(taper((16, 9.5), (17, 4.5), 1.3, 1.1), STEM[2]); c.px(16, 6, STEM[0])
    c.px(8, 17, hx('#ffc0a8')); c.px(8, 18, hx('#ffb090')); c.px(9, 15, hx('#ffc0a8'))

@icon(24)  # 고추
def _(c):
    R_ = ramp('#e02828', hi='#ff8a68', lo='#a01438', dk='#5a1030')
    path = bez((22.5, 8.5), (25, 17), (14, 24), (4.5, 28.5))
    body = tube(path, 5.0, 0.7)
    c.shade(body, R_, R=4, soft=1)
    # 윤기
    for (x, y) in [(22, 11), (22.4, 13), (21.4, 15.6)]:
        c.px(x, y, hx('#ffd0b8'))
    cap = ell(22.5, 7.2, 6.0, 2.6) | ell(22.5, 8, 4.6, 2.6)
    c.shade(cap, GREEN, R=2.4, soft=0)
    c.flat(taper((22.5, 6.5), (26, 1.8), 1.7, 1.3), STEM[2])
    c.px(22, 7, GREEN[0]); c.px(21, 8, GREEN[0]); c.px(26, 2, STEM[0])

@icon(25)  # 옥수수
def _(c):
    CN = ramp('#ffd23c', hi='#fff4a0', lo='#e09a20', dk='#a0601c')
    cob = tube(bez((17, 6.5), (17, 14), (16.5, 20)), 5.3, 6.6)
    c.shade(cob, CN, R=6, soft=1)
    inner = erode(cob, 1)
    for x in (11, 14, 17, 20, 23):
        for y in range(6, 24):
            if inner[y, x]:
                c.px(x, y, CN[2] if (x + y) % 2 == 0 else CN[1])
    for y in range(9, 24, 3):
        for x in range(9, 25):
            if inner[y, x]:
                c.px(x, y, CN[2])
    for y in range(8, 24, 3):
        for x in (12, 15, 18, 21):
            if inner[y, x]:
                c.px(x, y, CN[0])
    # 수염
    for (x0, y0, x1, y1) in [(16, 7.5, 14, 3.5), (17, 7, 17.5, 2.5), (18, 7.5, 20.5, 3.8)]:
        px_line(c, (x0, y0), (x1, y1), hx('#c8903c'))
    # 껍질
    for p1, w in [((6.5, 14), 4.6), ((26, 13), 4.6)]:
        m = leaf((16, 30.5), p1, w, skew=0.2, pw=0.75)
        c.shade(m, GREEN, R=3.2, soft=0)
        vein(c, (16, 30), p1, GREEN[2], m)
    m = leaf((16, 31), (16.5, 17.5), 3.8, skew=0.1, pw=0.8)
    c.shade(m, ramp('#6ccc54', hi='#c0f488', lo='#34964a', dk='#1c5a3c'), R=3, soft=0)
    vein(c, (16, 30), (16.5, 19), GREEN[2], m)

@icon(26)  # 은방울꽃
def _(c):
    path = bez((11, 29), (9, -2), (29, -3), (28, 16), n=40)
    c.shade(tube(path, 1.0, 0.8), STEM, R=1.0, soft=0)
    L1 = leaf((14, 30.5), (2.5, 16), 5.0, skew=0.2, pw=0.9)
    L2 = leaf((14.5, 30.5), (28.5, 24), 4.4, skew=0.2, pw=0.9)
    c.shade(L1, GREEN, R=3.6, soft=0)
    c.shade(L2, ramp('#58b84a', hi='#b0ec78', lo='#2c8446', dk='#1a5238'), R=3.4, soft=0)
    vein(c, (14, 29), (5, 18), GREEN[2], L1); vein(c, (15, 29), (27, 24), GREEN[2], L2)
    for (i, bx, by, r) in [(14, 16.8, 12.8, 2.6), (20, 20.3, 9.6, 2.5), (30, 24.2, 12.2, 2.4), (37, 24.6, 18.6, 2.3)]:
        sx, sy = path[i]
        px_line(c, (sx, sy + 0.5), (bx, by - 1.5), STEM[1])
        bell = ell(bx, by, r, r + 0.3) | ell(bx, by + 1.8, r + 0.8, 1.4)
        c.shade(bell, WHITE, R=2.4, soft=0)
        c.px(int(bx - 1), int(by - 1), hx('#ffffff'))
        c.px(int(bx), int(by + 3), WHITE[3])

@icon(27)  # 연꽃 씨
def _(c):
    POD = ramp('#a8d050', hi='#e4f488', lo='#68a040', dk='#386038')
    c.shade(tube(bez((16, 25), (16.5, 28), (19, 30.5)), 1.4, 1.2), STEM, R=1.3, soft=0)
    body = taper((16, 14), (16, 26.5), 8.6, 2.6)
    c.shade(body, ramp('#78b048', hi='#bce070', lo='#427c3c', dk='#244c34'), R=6, soft=1)
    top = ell(16, 11.5, 11.8, 5.8)
    c.shade(top, POD, R=5, soft=1)
    for (x, y) in [(11, 9.4), (16, 8.9), (21, 9.4), (7.6, 12), (24.4, 12), (12.2, 14.3), (19.8, 14.3)]:
        c.flat(ell(x, y, 2.3, 2.0), POD[3])
        c.flat(ell(x - 0.1, y + 0.2, 1.7, 1.5), hx('#dcc47a'))
        c.px(int(x) - 1, int(y) - 1, hx('#fff0b0'))
        c.px(int(x), int(y) + 1, hx('#a88a48'))

@icon(28)  # 선인장 즙
def _(c):
    CAC = ramp('#4aa860', hi='#98e08a', lo='#2c7a50', dk='#1a4a3c')
    m = taper((13.5, 27), (13.5, 8), 5.2, 4.8)
    m |= taper((9, 18.5), (5.5, 18.5), 2.6, 2.6) | taper((5.5, 18.5), (5.5, 12), 2.6, 2.4)
    m |= taper((18, 15), (21.5, 15), 2.6, 2.6) | taper((21.5, 15), (21.5, 8.5), 2.6, 2.4)
    m &= rect(0, 0, 32, 28.5)
    c.shade(m, CAC, R=4, soft=1)
    for x in (11.5, 13.5, 15.5):
        vein(c, (x, 10), (x, 27), CAC[2] if x != 13.5 else CAC[3], taper((13.5, 27), (13.5, 8), 5.2, 4.8))
    vein(c, (5.5, 14), (5.5, 18), CAC[2], m); vein(c, (21.5, 10), (21.5, 14), CAC[2], m)
    for (x, y) in [(10, 10), (12, 14), (16, 12), (17, 19), (11, 22), (15, 24), (5, 14), (21, 11), (9, 16), (14, 17)]:
        c.px(x, y, hx('#fff2c0'))
    # 꽃
    c.shade(ell(13.5, 4.7, 2.3, 1.9), ramp('#ff5a9a', hi='#ffb0d0', lo='#c82c70', dk='#7a1c50'), R=1.8, soft=0)
    c.px(13, 4, hx('#ffe08a'))
    # 모래
    c.shade(ell(14, 28, 11.5, 2.4), ramp('#e0b878', hi='#f8e0a0', lo='#b08850', dk='#6a4c34'), R=2.2, soft=0)
    # 즙 방울
    DR = ramp('#4ad8d0', hi='#d0fff4', lo='#209aa8', dk='#145a78')
    drop = poly([(25.5, 12), (29.2, 19.5), (29, 22), (27.8, 24.5), (25.5, 25.3), (23.2, 24.5), (22, 22), (21.8, 19.5)]) | ell(25.5, 21.8, 3.9, 3.7)
    c.shade(drop, DR, R=3.6, soft=1)
    c.px(24, 19, hx('#ffffff')); c.px(24, 20, hx('#ffffff')); c.px(25, 18, hx('#d0fff4'))

@icon(29)  # 알로에
def _(c):
    AL = ramp('#56b87a', hi='#a8f0b8', lo='#2e8a64', dk='#1a5446')
    AL2 = ramp('#46a86e', hi='#98e4a8', lo='#277a5c', dk='#164a42')
    layers = [((16, 28.5), (3, 14), 3.6, AL2), ((16, 28.5), (29, 14.5), 3.6, AL2),
              ((16, 28.5), (8, 6), 3.8, AL), ((16, 28.5), (24, 5.5), 3.8, AL),
              ((16, 28.5), (16, 2), 4.2, AL), ]
    for p0, p1, w, pal in layers:
        m = leaf(p0, p1, w, skew=-0.35, pw=0.9)
        c.shade(m, pal, R=3, soft=1)
        vein(c, p0, p1, pal[2], m)
        # 가시 이빨
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        for tt in (0.45, 0.6, 0.75):
            for sgn in (-1, 1):
                x = p0[0] + ux * L * tt - uy * sgn * w * 0.7 * (1 - abs(tt - 0.5)) 
                y = p0[1] + uy * L * tt + ux * sgn * w * 0.7 * (1 - abs(tt - 0.5))
                if m[int(y), int(x)] if 0 <= int(x) < N and 0 <= int(y) < N else False:
                    c.px(int(x), int(y), hx('#f2ffd8'))
    for (x, y) in [(15, 20), (17, 23), (14, 24), (18, 17)]:
        c.px(x, y, AL[0])
    m = leaf((16, 29.5), (16, 14), 3.5, skew=-0.2, pw=0.9)
    c.shade(m, ramp('#5cc080', hi='#b0f4c0', lo='#30906a', dk='#1a5848'), R=3, soft=1)
    vein(c, (16, 29), (16, 16), AL[2], m)

@icon(30)  # 튤립 구근
def _(c):
    TL = ramp('#ee4a78', hi='#ffa0b8', lo='#b82458', dk='#6a1848')
    BU = ramp('#d8b070', hi='#f8e0a8', lo='#a07848', dk='#5e4030')
    stem(c, [(16, 16), (16, 22)], 2)
    c.shade(leaf((16, 23), (5, 17), 2.8, skew=0.2, pw=0.8), GREEN, R=2, soft=0)
    c.shade(leaf((16, 23), (27, 17), 2.8, skew=0.2, pw=0.8), GREEN, R=2, soft=0)
    c.shade(leaf((16, 17), (9, 3.5), 4.2, skew=0.2, pw=0.85), TL, R=3, soft=1)
    c.shade(leaf((16, 17), (23, 3.5), 4.2, skew=0.2, pw=0.85), TL, R=3, soft=1)
    c.shade(leaf((16, 18.5), (16, 1.5), 5.0, skew=0.1, pw=0.6), ramp('#f85a86', hi='#ffb0c4', lo='#c42c60', dk='#721c4c'), R=4, soft=1)
    # 구근
    bulb = ell(16, 26.3, 6.4, 4.3) | taper((16, 26), (16, 21.5), 4.2, 1.2)
    c.shade(bulb, BU, R=5, soft=1)
    for x in (12.5, 15, 17.5, 20):
        vein(c, (x, 22.5), (x - 1.2 + (x - 16) * 0.3, 29), BU[2], bulb)
    for (x, y) in [(13, 30.5), (15, 31), (17.5, 30.8), (19.5, 30.2)]:
        c.px(x, y, hx('#8a6a4c'))
    c.px(13, 25, BU[0]); c.px(12, 26, BU[0])

@icon(31)  # 나팔꽃
def _(c):
    MG = ramp('#5a7cf0', hi='#b0c8ff', lo='#3a48c0', dk='#24246a')
    # 잎·덩굴
    c.shade(heart(6.8, 26.5, 4.0, ang=-111), GREEN, R=3, soft=0)
    c.shade(heart(25.2, 27, 3.8, ang=115), GREEN, R=3, soft=0)
    rim = empty()
    for y in range(N):
        for x in range(N):
            dx, dy = x + 0.5 - 16, y + 0.5 - 14
            a = math.atan2(dy, dx)
            r = 10.3 + 1.3 * math.cos(5 * (a + math.pi / 2))
            if math.hypot(dx, dy) <= r:
                rim[y, x] = True
    c.shade(rim, MG, R=8, soft=1)
    for k in range(5):
        ang = -90 + k * 72
        vein(c, polar(16, 14, 4, ang), polar(16, 14, 12, ang), MG[0], rim)
        vein(c, polar(16, 14, 4, ang + 36), polar(16, 14, 11, ang + 36), MG[2], rim)
    c.shade(star(16, 14, 6.4, 3.0, n=5), ramp('#ffffff', hi='#ffffff', lo='#d8d0f8', dk='#8878c8'), R=2.5, soft=0)
    c.flat(ell(16, 14, 1.6), hx('#ffe27a')); c.px(15, 13, hx('#fff6c0'))

@icon(32)  # 인삼
def _(c):
    GS = ramp('#e8d0a0', hi='#fff2d0', lo='#b89868', dk='#6a5238')
    m = taper((16, 11), (16, 19), 3.6, 3.9)
    m |= ell(16, 17, 4.6, 4)
    m |= taper((14, 20), (10.5, 29.5), 2.6, 0.9) | taper((18, 20), (21.5, 29), 2.6, 0.9)
    m |= taper((13, 14), (6.5, 19.5), 2.0, 0.8) | taper((19, 14), (25.5, 18), 1.9, 0.8)
    m |= taper((14.5, 13), (12, 12), 1.0, 1.0)
    c.shade(m, GS, R=3.8, soft=1)
    for (y, x0, x1) in [(14, 13, 15), (16, 12.5, 14.5), (18.5, 12, 14), (13, 17, 19), (17, 18, 20)]:
        vein(c, (x0, y), (x1, y), GS[2], m)
    for (x, y) in [(10, 30.5), (21.5, 30), (6, 20.5), (25.5, 19), (8.5, 29), (23, 28.5), (12, 29)]:
        c.px(x, y, GS[3])
    # 머리 + 새싹
    c.shade(taper((16, 12), (16, 6.5), 1.6, 1.3), ramp('#7ab850', hi='#c0f088', lo='#46904a', dk='#285a38'), R=1.4, soft=0)
    for p1 in [(9.5, 4.5), (22.5, 4.5), (16, 1)]:
        c.shade(leaf((16, 7), p1, 2.0, pw=0.8), GREEN, R=1.8, soft=0)
    c.px(16, 6, hx('#ff5a5a'))

@icon(33)  # 광대버섯
def _(c):
    RD = ramp('#e83a3a', hi='#ff9a80', lo='#b01c3c', dk='#6a1038')
    SW = P('#ffffff', '#f4eefa', '#cdc2e0', '#9488b8')
    stem = prof(16, 16, 28, lambda t: 3.7 + 1.5 * t ** 2.2) | ell(16, 27.2, 6.4, 2.6)
    c.shade(stem, SW, R=4.5, soft=1)
    ring = ell(16, 21.2, 7.2, 2.2)
    c.shade(ring, P('#ffffff', '#f4eefa', '#cdc2e0', '#9488b8'), R=2, soft=0)
    c.flat(ring & ~shift(ring, 0, 1), SW[2])
    c.flat(ring & ~shift(ring, 0, -1), SW[2]) if False else None
    cap = ell(16, 12.5, 12.5, 9.5) & rect(0, 0, 32, 17.5)
    gill = ell(16, 17.2, 11.4, 2.6) & rect(0, 16, 32, 20)
    c.shade(gill, P('#fff0e0', '#efd0c0', '#b8909a', '#7a5a7a'), R=2, soft=0)
    cap &= ~(gill & rect(0, 16.5, 32, 20))
    cap = ell(16, 12.5, 12.5, 9.5) & rect(0, 0, 32, 16.6)
    c.shade(cap, RD, R=8, soft=1)
    for (x, y, r) in [(10, 8.5, 1.6), (17, 5.5, 1.7), (22.5, 10, 1.7), (13.5, 12.5, 1.4), (19.5, 13.6, 1.3), (6.5, 13, 1.1), (26, 14, 1.0), (9, 14.5, 0.9), (23, 6.5, 0.9)]:
        c.flat(ell(x, y, r), SW[0]); 
        if r > 1.3:
            c.px(int(x + 0.5), int(y + 0.5), SW[2])

@icon(34)  # 반딧불 꽃가루
def _(c):
    YL = (244, 255, 112)
    c.glow(16, 13, 12, hx('#d8ff60'), a0=46, rings=3)
    stem(c, [(16, 21), (15.5, 26), (16, 31)], 2)
    c.shade(leaf((15.8, 28), (7, 23), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    TLP = ramp('#2f9a8a', hi='#80e8c0', lo='#1c6a7a', dk='#103c58')
    petal_ring(c, 16, 13.5, 6, 3, 9.6, 3.0, TLP, a0=-90, R=2.4, pw=0.6, skew=0.1)
    c.shade(ell(16, 13.5, 3.8), ramp('#f4ff70', hi='#ffffd0', lo='#c8d838', dk='#8a9a28'), R=3.5, soft=1)
    c.px(14, 12, hx('#ffffff'))
    for (x, y) in [(5, 5), (26, 7), (28, 21), (4, 21), (21, 2), (10, 28)]:
        c.glow(x + 0.5, y + 0.5, 2.2, hx('#e8ff60'), a0=90, rings=2)
        c.flat(rect(x, y, x + 1, y + 1), YL, layer=c.front)
        c.dot(x, y, hx('#ffffff'))

@icon(35)  # 눈송이 꽃
def _(c):
    ICE = ramp('#d8f0ff', hi='#ffffff', lo='#8cb8e8', dk='#4c78b8')
    c.glow(16, 16, 12, hx('#a8e0ff'), a0=46, rings=3)
    cx, cy = 16, 16
    for k in range(6):
        ang = -90 + k * 60
        m = leaf(polar(cx, cy, 2, ang), polar(cx, cy, 13, ang), 2.5, skew=0.2, pw=0.8)
        c.shade(m, ICE, R=2.2, soft=0)
        for (rr, ln, w) in [(6.5, 5.2, 1.5), (9.3, 4.0, 1.2)]:
            for sgn in (-1, 1):
                b0 = polar(cx, cy, rr, ang)
                b1 = polar(b0[0], b0[1], ln, ang + sgn * 50)
                c.shade(leaf(b0, b1, w, pw=0.8), ICE, R=1.4, soft=0)
    c.shade(ell(cx, cy, 3.4), ramp('#fff4c0', hi='#ffffff', lo='#e8c870', dk='#a88a50'), R=3, soft=0)
    c.px(15, 15, hx('#ffffff'))
    c.spark(5, 4, hx('#ffffff')); c.spark(27, 27, hx('#d8f4ff'))

@icon(36)  # 구름 목화
def _(c):
    CL = P('#ffffff', '#e8f0ff', '#b8c4ee', '#8090c8')
    HK = ramp('#8a5a38', hi='#c08a5c', lo='#5c3a28', dk='#38222a')
    c.glow(16, 14, 13, hx('#b8d0ff'), a0=40, rings=3)
    for p1, w in [((9, 20.5), 2.8), ((23, 20.5), 2.8)]:
        pass
    puffs = [(16, 17, 8, 5.6), (7, 17.5, 4.6, 4), (25, 17.5, 4.6, 4), (10.5, 12, 5.2, 5), (21.5, 12.5, 5.2, 5), (16, 8.5, 5.6, 5.4)]
    for (x, y, rx, ry) in puffs:
        c.flat(ell(x, y, rx + 0.9, ry + 0.9), CL[2])
        c.shade(ell(x, y, rx, ry), CL, R=min(rx, ry), soft=0)
    # 꼬투리
    for p1, w in [((9, 23), 2.6), ((23, 23), 2.6)]:
        c.shade(leaf((16, 29.5), p1, w, skew=0.1, pw=0.95), HK, R=2.2, soft=0)
    c.shade(leaf((16, 30), (16, 22), 2.6, pw=0.9), HK, R=2.2, soft=0)
    c.spark(26, 6, hx('#ffffff')); c.spark(5, 10, hx('#d8e4ff'))

@icon(37)  # 달맞이꽃
def _(c):
    PR = ramp('#ffe45a', hi='#fffbb0', lo='#e0a826', dk='#a0661c')
    c.glow(14, 16, 12, hx('#ffe888'), a0=40, rings=3)
    stem(c, [(14, 23), (13.5, 27.5), (14, 31)], 2)
    c.shade(leaf((13.8, 28.5), (23, 25), 2.3, pw=0.7), GREEN, R=1.8, soft=0)
    for k in range(4):
        ang = k * 90
        a = math.radians(ang)
        lx, ly = 14 + 5.8 * math.cos(a), 16.5 + 5.8 * math.sin(a)
        m = heart(lx, ly, 5.2, ang=ang + 90) & ~ell(*polar(14, 16.5, 11.8, ang), 1.4, 1.4)
        c.shade(m, PR, R=3.8, soft=1)
        vein(c, polar(14, 16.5, 2.5, ang), polar(14, 16.5, 9, ang), PR[2], m)
    c.shade(ell(14, 16.5, 2.6), ramp('#d89a2c', hi='#ffe27a', lo='#a8641c', dk='#6a3c1c'), R=2.4, soft=0)
    c.px(13, 15, hx('#fff0a0'))
    # 초승달
    moon = ell(27, 5.2, 4.0) & ~ell(28.6, 4.2, 3.5)
    c.shade(moon, ramp('#fff4b0', hi='#ffffff', lo='#e0c060', dk='#a08840'), R=1.6, soft=0)
    c.spark(5, 4, hx('#fff4c0'))

@icon(38)  # 요정 버섯 (둥글게 난 버섯 고리)
def _(c):
    c.glow(16, 20, 12, hx('#f0a0ff'), a0=40, rings=3)
    ring = ell(16, 24, 14, 6.4)
    c.shade(ring, ramp('#5ab84a', hi='#a8e870', lo='#2e8a44', dk='#1a5638'), R=3, soft=0)
    caps = [ramp('#f070b8', hi='#ffb8e0', lo='#b8388a', dk='#70206a'), ramp('#a88af0', hi='#d8c8ff', lo='#7058c0', dk='#40308a')]
    stem_p = P('#ffffff', '#f4eefa', '#cdc2e0', '#9488b8')
    # 뒤→앞 순서
    items = [(16, 17, 3.8, 3.0, 0, 1.2, 3.6), (6.5, 21.5, 4.2, 3.3, 1, 1.3, 3.8), (25.5, 21.5, 4.2, 3.3, 0, 1.3, 3.8), (11, 28.5, 5.2, 4.2, 0, 1.6, 4.4), (22, 28.5, 5.2, 4.2, 1, 1.6, 4.4)]
    for (x, y, cw, ch, k, sw, sh) in items:
        mushroom(c, x, y, cw, ch, sw, sh, caps[k], stem_p, spots=[(-1.3, -1.2, 0.8), (1.5, -0.4, 0.7)] if cw < 5 else [(-1.8, -1.6, 1.0), (1.8, -0.5, 0.9), (0, -2.6, 0.6)], spot_col=(255, 255, 255))
    c.spark(16, 7, hx('#ffffff'), big=True)
    c.spark(6, 11, hx('#ffd0f4')); c.spark(26, 10, hx('#d8c8ff'))

@icon(39)  # 노래하는 종꽃
def _(c):
    BL = ramp('#6a7cf0', hi='#c0d0ff', lo='#4a46c0', dk='#2c2a76')
    c.glow(13, 15, 11, hx('#a0b0ff'), a0=40, rings=3)
    stm = tube(bez((12.5, 31), (10, 15), (10, 3), (14, 4.5)), 1.0, 0.8)
    c.shade(stm, STEM, R=1, soft=0)
    c.shade(leaf((12, 29.5), (4, 24), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    c.shade(leaf((12, 27), (21, 23), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    bell = ell(14.5, 8.8, 4.8, 4.6) | prof(14.5, 8.8, 21, lambda t: 4.8 + 5.2 * (t ** 1.4))
    bell &= rect(0, 0, 32, 21.5)
    c.shade(bell, BL, R=6, soft=1)
    for x in (8.5, 11.5, 14.5, 17.5, 20.5):
        vein(c, (14.5 + (x - 14.5) * 0.35, 9), (x + (x - 14.5) * 0.15, 20.5), BL[2], bell)
    lip = ell(14.5, 21.5, 9.0, 3.0)
    c.shade(lip, ramp('#8a9aff', hi='#d0dcff', lo='#5a5ad0', dk='#34328a'), R=2.4, soft=0)
    c.flat(ell(14.5, 22.0, 7.4, 1.7), hx('#2e2070'))
    c.flat(rect(14, 22.5, 15, 24.6), hx('#ffe27a')); c.px(14, 25, hx('#fff6b0')); c.px(15, 25, hx('#e0a830'))
    c.px(10, 9, BL[0]); c.px(11, 8, BL[0]); c.px(9, 11, BL[0]); c.px(9, 12, BL[0])
    NOTE = hx('#ffe27a')
    for (x, y) in [(25, 17), (26, 17), (24, 18), (25, 18), (26, 18), (24, 19), (25, 19)]:
        c.px(x, y, NOTE, layer=c.front)
    for y in range(8, 18):
        c.px(27, y, NOTE, layer=c.front)
    for (x, y) in [(28, 9), (29, 10), (29, 11), (28, 12)]:
        c.px(x, y, NOTE, layer=c.front)
    c.spark(23, 5, hx('#ffffff'))

@icon(40)  # 속삭임 덩굴
def _(c):
    VN = ramp('#7ad8b0', hi='#d0ffe8', lo='#3a9a88', dk='#1c5a5e')
    c.glow(17, 16, 12, hx('#a8f0d8'), a0=34, rings=3)
    pts = bez((7, 31), (6, 20), (16, 22), (18, 16), n=30)
    # 소용돌이
    cx, cy = 20, 11
    spiral = []
    for i in range(46):
        t = i / 45
        a = math.radians(60 + t * 560)
        r = 7.2 * (1 - t) + 0.8
        spiral.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    path = pts + spiral[::1]
    c.shade(tube(path, 1.5, 0.8), VN, R=1.4, soft=0)
    # 곁덩굴
    side = bez((11, 26), (4, 24), (3, 17), (7, 15), n=14)
    c.shade(tube(side, 1.0, 0.6), VN, R=1.0, soft=0)
    for (x, y, ang, s) in [(8.5, 27, 200, 3.4), (12.5, 22.5, 20, 3.2), (6, 17.5, 235, 3.0), (26, 18, 40, 3.0)]:
        c.shade(heart(x, y, s, ang=ang - 90 + 180), VN, R=2.6, soft=0)
    c.px(25, 5, hx('#ffffff'), layer=c.front)
    c.spark(27, 5, hx('#d8fff0')); c.spark(5, 7, hx('#d8c8ff'))
    c.dot(11, 12, hx('#d8fff0')); c.dot(28, 14, hx('#d8fff0')); c.dot(14, 4, hx('#d8fff0'))

@icon(41)  # 유리 열매
def _(c):
    GL = P('#e8ffff', '#86dcf4', '#5aa4e8', '#3a60b4')
    c.glow(16, 16, 13, hx('#a0f0ff'), a0=40, rings=3)
    c.shade(leaf((17, 6), (27, 3), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    def berry(cx, cy, r):
        m = ell(cx, cy, r)
        c.shade(m, GL, R=r, soft=1)
        # 안쪽 반사광(오른쪽 아래) — 투명한 느낌
        c.flat(ell(cx + r * 0.25, cy + r * 0.3, r * 0.6) & m & ~erode(m, 2) if False else (m & shift(m, -1, -1) & ~shift(m, -2, -2) & ~ell(cx - r * 0.3, cy - r * 0.3, r * 0.9)), hx('#d8f8ff'))
        c.px(int(cx - r * 0.5), int(cy - r * 0.5), hx('#ffffff')); c.px(int(cx - r * 0.5) + 1, int(cy - r * 0.5) - 1, hx('#ffffff'))
        c.px(int(cx - r * 0.5), int(cy - r * 0.5) + 1, hx('#ffffff'))
        c.px(int(cx + r * 0.45), int(cy + r * 0.5), hx('#ffffff'))
        x, y = int(cx), int(cy - r * 0.15)
        c.px(x, y, GL[3]); c.px(x - 1, y, GL[2]); c.px(x + 1, y, GL[2]); c.px(x, y - 1, GL[2]); c.px(x, y + 1, GL[2])
    berry(15.5, 11.5, 6.3)
    berry(9.5, 20.5, 6.3)
    berry(21.5, 20.5, 6.8)
    c.spark(27, 9, hx('#ffffff')); c.spark(4, 10, hx('#d8f8ff'))

@icon(42)  # 별사과
def _(c):
    AP = ramp('#f05a3c', hi='#ffb878', lo='#b82c4a', dk='#6a1a44')
    c.glow(16, 17, 13, hx('#ffd060'), a0=44, rings=3)
    body = poly([polar(16, 17.5, (13.2 if i % 2 == 0 else 7.6), -54 + i * 36) for i in range(10)])
    body = grow(erode(body, 1), 1) | erode(body, 1)
    c.shade(body, AP, R=6, soft=2)
    # 별 무늬(금빛)
    c.shade(star(16.5, 18.5, 5.0, 2.3, n=5, rot=-90), ramp('#ffd84a', hi='#fff8b0', lo='#e0982a', dk='#a05a24'), R=2, soft=0)
    c.px(15, 17, hx('#ffffff'))
    # 꼭지·잎
    c.shade(taper((16, 9), (17, 3.5), 1.2, 1.0), ramp('#8a5a30', hi='#c08a50', lo='#5a3622', dk='#34201c'), R=1.2, soft=0)
    c.shade(leaf((17, 5.5), (25, 2.5), 2.4, pw=0.7), GREEN, R=1.8, soft=0)
    c.px(8, 12, hx('#ffd8b0')); c.px(9, 11, hx('#ffd8b0'))
    c.spark(27, 24, hx('#fff4b0')); c.spark(4, 6, hx('#fff4b0'))

@icon(43)  # 화룡초
def _(c):
    FR = ramp('#e8301c', hi='#ff8a3a', lo='#b01c28', dk='#6a1038')
    FO = ramp('#ff8a1c', hi='#ffc850', lo='#e0501c', dk='#a02c20')
    FY = ramp('#ffd83a', hi='#fffbc0', lo='#ffa82c', dk='#e0701c')
    c.glow(16, 14, 13, hx('#ff8a30'), a0=46, rings=3)
    # 줄기·잎
    c.shade(tube(bez((16, 31), (15, 26), (16, 22)), 1.4, 1.2), ramp('#6a8a3c', hi='#a8c860', lo='#46663a', dk='#2a4430'), R=1.3, soft=0)
    c.shade(leaf((15.5, 29), (6, 25), 2.4, pw=0.7), ramp('#5a9a3c', hi='#a8d860', lo='#38703a', dk='#224a30'), R=2, soft=0)
    c.shade(leaf((16, 27.5), (26, 24), 2.4, pw=0.7), ramp('#5a9a3c', hi='#a8d860', lo='#38703a', dk='#224a30'), R=2, soft=0)
    # 불꽃 잎
    fl = [(9.5, 23, 4.2, 14, -3, 0.8, FR), (22.5, 23, 4.2, 15, 3, -0.8, FR), (16, 24, 5.6, 22, 1.5, 1.0, FR)]
    for (x, by, w, h, lean, wob, pal) in fl:
        m = flame(x, by, w, h, lean, wob)
        c.shade(m, pal, R=3.0, soft=1)
    for (x, by, w, h, lean, wob) in [(16, 23.5, 3.4, 14, 1.0, 0.7), (9.7, 22.5, 2.2, 8, -2, 0.5), (22.3, 22.5, 2.2, 9, 2, -0.5)]:
        m = flame(x, by, w, h, lean, wob)
        c.shade(m, FO, R=2.2, soft=1)
    for (x, by, w, h, lean, wob) in [(16, 23, 1.8, 7.5, 0.6, 0.4)]:
        c.shade(flame(x, by, w, h, lean, wob), FY, R=1.8, soft=0)
    c.spark(5, 8, hx('#ffd060')); c.spark(27, 9, hx('#ffb040'))
    c.dot(24, 3, hx('#ffd060')); c.dot(8, 3, hx('#ff9030')); c.dot(12, 1, hx('#ffe080'))

@icon(44)  # 꿈꽃
def _(c):
    DR = ramp('#b890f8', hi='#f0d8ff', lo='#8058d0', dk='#44308a')
    DP = ramp('#f0a0e8', hi='#ffe0fa', lo='#c070c8', dk='#783c88')
    c.glow(16, 15, 13, hx('#c8a0ff'), a0=44, rings=3)
    stem(c, [(16, 25), (16, 31)], 2)
    c.shade(leaf((16, 29), (7, 25.5), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    c.shade(leaf((16, 29), (25, 25.5), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    for k in range(8):
        ang = -90 + k * 45
        m = ell(*polar(16, 14.5, 8.2, ang), 4.0, 3.4, ang=ang)
        c.shade(m, DR if k % 2 == 0 else DP, R=2.8, soft=0)
    c.shade(ell(16, 14.5, 6.2), ramp('#3a2a9a', hi='#6a58d0', lo='#22186a', dk='#120c40'), R=5, soft=1)
    moon = ell(15.2, 14.5, 4.2) & ~ell(17.4, 13.3, 3.6)
    c.shade(moon, ramp('#ffe88a', hi='#fffbd0', lo='#e8b84a', dk='#a07a30'), R=1.6, soft=0)
    c.px(20, 12, hx('#ffffff')); c.px(19, 17, hx('#cfc0ff'))
    c.spark(4, 5, hx('#ffffff')); c.spark(28, 6, hx('#ffe0fa')); c.spark(27, 27, hx('#d8c8ff'))

@icon(45)  # 거울 잎
def _(c):
    MR = ramp('#b8c8e0', hi='#ffffff', lo='#7888b0', dk='#485080')
    MR2 = ramp('#a0b4d4', hi='#f0f8ff', lo='#6878a8', dk='#40487a')
    c.glow(16, 16, 13, hx('#c8e0ff'), a0=40, rings=3)
    c.shade(tube(bez((8, 31), (9, 27), (12, 24)), 1.2, 1.0), ramp('#7a8aa0', hi='#c0ccdc', lo='#506078', dk='#34405a'), R=1.2, soft=0)
    l2 = leaf((11, 27), (3, 12), 4.2, skew=0.1, pw=0.95)
    c.shade(l2, MR2, R=3.2, soft=1)
    vein(c, (11, 26), (4, 14), MR2[2], l2)
    lf = leaf((10, 28), (27, 4), 8.2, skew=0.1, pw=0.95)
    c.shade(lf, MR, R=6, soft=1)
    vein(c, (11, 27), (26, 5), MR[2], lf)
    for (x0, y0, x1, y1) in [(14, 21, 11, 17), (17, 18, 13, 13), (20, 14, 17, 8), (14, 22, 19, 22), (18, 18, 23, 19), (21, 13, 25, 13)]:
        vein(c, (x0, y0), (x1, y1), MR[2], lf)
    for (x0, y0, x1, y1, col) in [(10, 18, 16, 10, '#ffffff'), (12, 21, 19, 13, '#e8f4ff')]:
        vein(c, (x0, y0), (x1, y1), hx(col), lf)
    for (x, y) in [(22, 20), (20, 22), (24, 17), (17, 24)]:
        if lf[y, x]:
            c.px(x, y, hx('#9ac8f0'))
    c.spark(6, 5, hx('#ffffff'), big=True); c.spark(27, 26, hx('#e0f0ff'))

@icon(46)  # 그림자 버섯
def _(c):
    SH = ramp('#6a48b8', hi='#b8a0f0', lo='#44308a', dk='#261a52')
    SS = ramp('#5a4a88', hi='#9a88c8', lo='#3a2e68', dk='#20183e')
    c.glow(16, 17, 13, hx('#8a50ff'), a0=52, rings=3)
    # 그림자 연기
    for (x, y) in [(9, 6), (22, 4), (24, 8), (6, 11)]:
        c.flat(ell(x, y, 1.5, 1.2), hx('#3a2468'), layer=c.back)
    mushroom(c, 10, 29, 3.8, 3.0, 1.1, 4.5, SH, SS, spots=[(-1, -1.0, 0.7)], spot_col=hx('#d0b8ff'))
    mushroom(c, 17.5, 29.5, 8.4, 7.2, 2.4, 12, SH, SS, spots=[(-3.5, -3.2, 1.3), (2.5, -4.6, 1.5), (4.8, -1.8, 1.0), (-1, -1.4, 0.8), (-5.5, -1.0, 0.8)], spot_col=hx('#d0b8ff'))
    for (x, y) in [(14, 13), (20, 11), (22, 14)]:
        c.px(x, y, hx('#ffffff'))
    c.px(15, 22, hx('#5ae8ff'), layer=c.front); c.px(19, 22, hx('#5ae8ff'), layer=c.front)
    c.spark(5, 18, hx('#c0a0ff')); c.spark(27, 20, hx('#c0a0ff'))

@icon(47)  # 번개 콩
def _(c):
    BN = ramp('#4a5ae0', hi='#a0b0ff', lo='#2c34a8', dk='#161a64')
    c.glow(16, 16, 13, hx('#ffe650'), a0=44, rings=3)
    bean = ell(16, 16, 12.2, 9, ang=-40) & ~ell(22, 23.5, 4.2, 3.2)
    c.shade(bean, BN, R=6, soft=1)
    # 번개
    bolt = poly([(19, 3), (11, 15), (16, 15), (12, 28), (24, 12), (18.5, 12), (22, 3)])
    c.flat(bolt, hx('#e8a800'), layer=c.front)
    bolt2 = poly([(19.5, 4), (12.5, 14.4), (17.5, 14.4), (13.5, 26), (22.5, 12.6), (17.5, 12.6), (20.6, 4)])
    c.flat(bolt2, hx('#ffe83a'), layer=c.front)
    c.flat(poly([(19.5, 4), (15.8, 9), (17.4, 9)]), hx('#fffbc0'), layer=c.front)
    c.px(8, 13, hx('#c8d0ff')); c.px(8, 14, hx('#c8d0ff')); c.px(9, 12, hx('#c8d0ff'))
    c.spark(5, 4, hx('#fff070')); c.spark(27, 26, hx('#fff070'))

@icon(48)  # 서리 딸기
def _(c):
    FB = ramp('#4a7ae8', hi='#a0c8ff', lo='#2c46b0', dk='#182070')
    FW = P('#ffffff', '#e8f6ff', '#b0d4f4', '#78a0d8')
    c.glow(16, 17, 13, hx('#a0e0ff'), a0=44, rings=3)
    body = ell(16, 15.5, 10.4, 8.6) | taper((16, 16), (16, 27), 9.8, 2.6)
    c.shade(body, FB, R=7, soft=1)
    # 서리 덮개 (위쪽, 고드름처럼 삐죽)
    cap = ell(16, 11.5, 10.6, 4.8) & body
    for x, ln in [(7, 1), (10, 3), (13, 1), (16, 4), (19, 2), (22, 3), (25, 1)]:
        cap |= rect(x - 1.3, 11, x + 1.3, 14 + ln) & body
    c.shade(cap, FW, R=3, soft=1)
    k = 0
    for y in range(17, 26, 3):
        for x in range(9 + (k % 2) * 2, 24, 4):
            if erode(body, 2)[y, x] and not cap[y, x]:
                c.px(x, y, hx('#e8f6ff')); c.px(x, y + 1, hx('#18309a'))
        k += 1
    # 얼음 꼭지
    for p1 in [(5.5, 10), (10, 5), (22, 5), (26.5, 10)]:
        c.shade(leaf((16, 10.5), p1, 2.6, skew=0.2, pw=0.7), ramp('#38b8a8', hi='#a0f0e0', lo='#208898', dk='#145068'), R=1.8, soft=0)
    c.flat(taper((16, 10), (16.5, 4), 1.2, 1.0), hx('#208898'))
    c.spark(5, 20, hx('#ffffff')); c.spark(27, 6, hx('#d8f4ff'), big=True)

@icon(49)  # 바다 포도
def _(c):
    SG = ramp('#30c8c0', hi='#b8fff0', lo='#1c8aa0', dk='#104a6a')
    c.glow(16, 16, 13, hx('#60f0e0'), a0=40, rings=3)
    c.shade(leaf((15, 6.5), (6, 2.5), 2.2, pw=0.7), ramp('#58c8a0', hi='#a8f0c8', lo='#2c906c', dk='#185a4a'), R=1.8, soft=0)
    c.shade(leaf((17, 6.5), (26, 3), 2.2, pw=0.7), ramp('#58c8a0', hi='#a8f0c8', lo='#2c906c', dk='#185a4a'), R=1.8, soft=0)
    c.flat(taper((16, 8), (16, 3), 1.2, 1.0), hx('#58c8a0'))
    rows = [(8.5, [11, 16, 21]), (13, [8.5, 13.5, 18.5, 23.5]), (17.5, [11, 16, 21]), (22, [13.5, 18.5]), (26.5, [16])]
    for (y, xs) in rows[::-1]:
        for x in xs:
            pass
    for (y, xs) in rows:
        for x in xs:
            c.shade(ell(x + (0.4 if y % 2 else 0), y, 3.3), SG, R=3.2, soft=0)
            c.px(int(x - 1), int(y - 1), hx('#ffffff'))
    c.spark(4, 24, hx('#d8fff8')); c.spark(28, 24, hx('#d8fff8')); c.dot(27, 11, hx('#d8fff8')); c.dot(5, 9, hx('#d8fff8'))

@icon(50)  # 오로라 꽃잎
def _(c):
    c.glow(16, 14, 13, hx('#70f0d0'), a0=44, rings=3)
    grad = stops('#3ce890', '#38d0e8', '#6a8cf8', '#c070f0', '#ff78d8')
    def col(x, y):
        t = (30 - y) / 27.0
        return grad(t)
    base = (16, 30)
    mask = empty()
    petals = []
    for ang, L, w in [(-90 - 52, 20, 5.4), (-90 + 52, 20, 5.4), (-90 - 26, 24, 6.0), (-90 + 26, 24, 6.0), (-90, 27, 6.4)]:
        m = leaf(base, polar(base[0], base[1], L, ang), w, skew=0.25, pw=0.7)
        petals.append(m)
    for m in petals:
        # 이미 칠한 곳 위에 덮어 씀 (앞 꽃잎이 위)
        c.shade_grad(m, col, R=4, soft=1)
        vein(c, base, polar(*base, 17, -90), (0, 0, 0), None) if False else None
    for ang, L in [(-142, 17), (-116, 21), (-90, 24), (-64, 21), (-38, 17)]:
        p1 = polar(base[0], base[1], L, ang)
        tmp = Cv()
        px_line(tmp, polar(*base, 6, ang), p1, (255, 255, 255))
        sel = tmp.body[:, :, 3] > 0
        for y, x in np.argwhere(sel):
            if c.body[y, x, 3]:
                r, g, b = col(x, y)
                c.body[y, x] = (min(255, r + 70), min(255, g + 70), min(255, b + 70), 255)
    c.spark(5, 6, hx('#ffffff')); c.spark(27, 5, hx('#ffd8f8'), big=True); c.spark(28, 22, hx('#d8fff0'))

@icon(51)  # 혜성 씨앗
def _(c):
    # 꼬리 (뒤쪽 반투명 줄무늬)
    tail = [((17, 17), (1.5, 1.5), 7.4, (110, 100, 255), 200), ((16, 19), (0.5, 10), 4.2, (80, 200, 255), 225), ((19, 16), (10, 0.5), 4.2, (214, 120, 255), 225), ((17, 17), (3, 3), 2.6, (255, 255, 255), 255)]
    for (p0, p1, w, col, a) in tail:
        m = taper(p0, p1, w, 0.4, cap=False)
        for y, x in np.argwhere(m):
            t = math.hypot(x + 0.5 - p0[0], y + 0.5 - p0[1]) / math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            al = int(a * (1 - t * 0.7))
            if t > 0.55 and (x + y) % 2 == 0:
                continue
            c.back[y, x] = (*col, max(al, int(c.back[y, x, 3])))
    c.glow(22, 22, 8, hx('#ffe080'), a0=60, rings=2)
    SD = ramp('#d8a04a', hi='#fff0a0', lo='#a06a2c', dk='#5a3622')
    seed = leaf((13.5, 13), (28, 27.5), 6.2, skew=0.55, pw=0.8)
    c.shade(seed, SD, R=4.5, soft=1)
    vein(c, (16, 16), (26, 26), SD[2], seed)
    c.px(20, 19, hx('#ffffff')); c.px(21, 18, hx('#fff8d0')); c.px(19, 20, hx('#fff8d0')); c.px(21, 19, hx('#fff8d0'))
    c.spark(8, 22, hx('#ffffff')); c.spark(27, 6, hx('#d8c8ff'), big=True); c.spark(22, 5, hx('#a8e0ff'))
    c.dot(4, 16, hx('#c8d8ff')); c.dot(12, 6, hx('#e8d0ff')); c.dot(27, 14, hx('#ffffff'))

@icon(52)  # 월하향
def _(c):
    WH = ramp('#f4f0ff', hi='#ffffff', lo='#c4b8f0', dk='#8070c0')
    c.glow(17, 14, 13, hx('#d8e8ff'), a0=44, rings=3)
    moon = ell(8, 8, 6.0) & ~ell(11, 6.6, 5.2)
    c.shade(moon, ramp('#fff4b0', hi='#ffffff', lo='#e0c060', dk='#a08840'), R=2.2, soft=0)
    c.shade(tube(bez((17, 21), (17, 26), (14, 29)), 1.4, 1.0), STEM, R=1.3, soft=0)
    c.shade(leaf((15.5, 29), (5, 27), 2.4, pw=0.7), GREEN, R=1.8, soft=0)
    c.shade(leaf((16.5, 27), (28, 24), 2.4, pw=0.7), GREEN, R=1.8, soft=0)
    # 꽃통
    c.shade(taper((17, 18), (17, 24), 3.4, 1.8), ramp('#e8f4d8', hi='#ffffff', lo='#a8c898', dk='#688868'), R=2, soft=0)
    for k in range(5):
        ang = -90 + k * 72
        m = leaf(polar(17, 14.5, 2, ang), polar(17, 14.5, 11.8, ang), 3.6, skew=0.1, pw=0.8)
        c.shade(m, WH, R=2.8, soft=0)
        vein(c, polar(17, 14.5, 3, ang), polar(17, 14.5, 9, ang), WH[2], m)
    c.shade(ell(17, 14.5, 3.0), ramp('#fff4a8', hi='#ffffff', lo='#e8c868', dk='#a08840'), R=2.6, soft=0)
    c.px(16, 13, hx('#ffffff'))
    c.spark(27, 7, hx('#ffffff'), big=True); c.spark(5, 20, hx('#d8e4ff'))
    for (x, y) in [(28, 12), (27, 14), (28, 16)]:
        c.dot(x, y, hx('#d8e8ff'))

@icon(53)  # 해님 호박
def _(c):
    PK = ramp('#ffc02c', hi='#fff08a', lo='#e0801c', dk='#a0481c')
    c.glow(16, 18, 14, hx('#ffe060'), a0=50, rings=3)
    # 줄기
    c.shade(taper((16, 9), (18, 3.5), 1.8, 1.5), ramp('#7a8a3c', hi='#b8c860', lo='#4e663a', dk='#2c4230'), R=1.6, soft=0)
    px_line(c, (19, 5), (23, 3), STEM[1]); px_line(c, (23, 3), (25, 5), STEM[1]); c.px(25, 6, STEM[2])
    # 호박 마디 (바깥 → 안)
    for (x, rx, ry, cy) in [(5.8, 5.0, 8.2, 19), (26.2, 5.0, 8.2, 19), (10, 6.0, 10.2, 18.5), (22, 6.0, 10.2, 18.5), (16, 6.6, 10.8, 18.5)]:
        c.shade(ell(x, cy, rx, ry), PK, R=4.5, soft=1)
    for x in (10.5, 21.5):
        vein(c, (x, 9), (x + (1 if x > 16 else -1) * 0.5, 28), PK[2], mask_of(c))
    # 얼굴
    BR = hx('#4e1e0c')
    for (x, y) in [(10, 17), (11, 16), (12, 16), (13, 17)] + [(19, 17), (20, 16), (21, 16), (22, 17)]:
        c.px(x, y, BR)
    for (x, y) in [(13, 22), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 22)]:
        c.px(x, y, BR)
    c.px(12, 21, hx('#ff9a50')); c.px(11, 21, hx('#ff9a50')); c.px(20, 21, hx('#ff9a50')); c.px(21, 21, hx('#ff9a50'))
    c.px(14, 12, PK[0]); c.px(13, 13, PK[0]); c.px(8, 14, PK[0])
    c.spark(4, 6, hx('#fff4a0'), big=True); c.spark(28, 8, hx('#fff4a0')); c.spark(27, 28, hx('#fff4a0'))

@icon(54)  # 황금 버섯
def _(c):
    GD = ramp('#ffd23c', hi='#fff7b0', lo='#d89018', dk='#8a5418')
    GS = ramp('#f0d890', hi='#fff8d0', lo='#c8a458', dk='#8a6a38')
    c.glow(16, 17, 14, hx('#ffe060'), a0=52, rings=3)
    mushroom(c, 16, 29.5, 12.2, 9.6, 4.6, 10, GD, GS, spots=[(-4, -3.8, 1.4), (3, -5.6, 1.6), (6.5, -2, 1.1), (-7.5, -1.6, 1.0), (0, -1.6, 0.9)], spot_col=hx('#fffbd0'))
    c.px(9, 12, hx('#ffffff')); c.px(10, 11, hx('#ffffff')); c.px(8, 13, hx('#ffffff'))
    c.spark(5, 6, hx('#fff8c0'), big=True); c.spark(27, 7, hx('#fff8c0')); c.spark(26, 26, hx('#ffe888')); c.spark(5, 25, hx('#ffe888'))

@icon(55)  # 수정 장미
def _(c):
    CR = ramp('#e8489c', hi='#ffb8e4', lo='#a82478', dk='#5a1450')
    CR2 = ramp('#ff74c0', hi='#ffe0f6', lo='#d046a0', dk='#7a2068')
    CR3 = ramp('#ffa8dc', hi='#ffffff', lo='#f06cc0', dk='#a83888')
    LF = ramp('#58c8b8', hi='#b0fff0', lo='#2c8a98', dk='#185068')
    c.glow(16, 14, 14, hx('#ff90e0'), a0=44, rings=3)
    c.shade(tube(bez((16, 22), (15, 27), (16, 31)), 1.3, 1.0), LF, R=1.2, soft=0)
    c.shade(leaf((15.5, 29.5), (4.5, 27), 2.5, pw=0.8), LF, R=2, soft=0)
    c.shade(leaf((16, 28.5), (27.5, 26), 2.5, pw=0.8), LF, R=2, soft=0)
    cx, cy = 16, 12.5
    for k in range(7):
        ang = -90 + k * 360 / 7
        m = leaf(polar(cx, cy, 1.5, ang), polar(cx, cy, 12.0, ang), 4.8, skew=0.15, pw=0.7)
        c.flat(grow(m), CR[3])
        c.shade(m, CR, R=3.4, soft=0)
    for k in range(6):
        ang = -60 + k * 60
        m = leaf(polar(cx, cy, 1, ang), polar(cx, cy, 8.6, ang), 3.6, skew=0.1, pw=0.62)
        c.flat(grow(m), CR[2])
        c.shade(m, CR2, R=2.8, soft=0)
    for k in range(5):
        ang = -90 + k * 72
        m = leaf(polar(cx, cy, 0.5, ang), polar(cx, cy, 5.4, ang), 2.6, skew=0.1, pw=0.65)
        c.flat(grow(m), CR2[2])
        c.shade(m, CR3, R=2.2, soft=0)
    c.flat(ell(cx, cy, 1.6), CR[2]); c.px(15, 13, hx('#ffffff'))
    c.px(9, 8, hx('#ffffff')); c.px(10, 7, hx('#ffffff')); c.px(8, 9, hx('#ffe0f6'))
    c.px(23, 11, hx('#9ae8ff')); c.px(19, 21, hx('#9ae8ff')); c.px(8, 17, hx('#9ae8ff'))
    c.spark(4, 5, hx('#ffffff'), big=True); c.spark(28, 8, hx('#ffd8f4')); c.spark(27, 27, hx('#e8f8ff'))

@icon(56)  # 무지개 콩
def _(c):
    c.glow(16, 16, 13, hx('#ffc0f0'), a0=38, rings=3)
    rb = stops('#ff4a5a', '#ff9a3a', '#ffe23a', '#58e060', '#3ac8f0', '#7a6af8', '#d068f0')
    def col(x, y):
        return rb(((x + y) - 12) / 28.0)
    bean = ell(16, 16, 12.2, 9, ang=-40) & ~ell(22, 23.5, 4.2, 3.2)
    c.shade_grad(bean, col, R=6, soft=1)
    c.px(9, 15, hx('#ffffff')); c.px(10, 14, hx('#ffffff')); c.px(9, 16, hx('#ffffff')); c.px(11, 13, hx('#ffffff'))
    c.spark(5, 5, hx('#ffffff'), big=True); c.spark(27, 5, hx('#ffe0f8')); c.spark(26, 27, hx('#d8f0ff'))

@icon(57)  # 시간의 꽃
def _(c):
    TP = ramp('#8a6af0', hi='#d0c0ff', lo='#5a40c0', dk='#2e2478')
    TP2 = ramp('#a888ff', hi='#e8dcff', lo='#7058d8', dk='#3a2a90')
    c.glow(16, 14, 14, hx('#b8a0ff'), a0=44, rings=3)
    stem(c, [(16, 25), (16, 31)], 2)
    c.shade(leaf((16, 29), (7, 25.5), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    c.shade(leaf((16, 29), (25, 25.5), 2.2, pw=0.7), GREEN, R=1.8, soft=0)
    for k in range(10):
        ang = -90 + k * 36
        m = leaf(polar(16, 14, 5, ang), polar(16, 14, 13.4, ang), 3.2, skew=0.15, pw=0.7)
        c.shade(m, TP if k % 2 == 0 else TP2, R=2.4, soft=0)
    GO = ramp('#ffd24a', hi='#fff4a8', lo='#d8901c', dk='#8a5418')
    c.shade(ell(16, 14, 7.4), GO, R=3, soft=0)
    c.flat(ell(16, 14, 5.6), hx('#fff8e0'))
    c.flat(ell(16, 14, 5.6) & ~shift(ell(16, 14, 5.6), 1, 1), hx('#d8c8a8'))
    for k in range(12):
        a = k * 30 - 90
        x, y = polar(16, 14, 4.6, a)
        c.px(int(x), int(y), hx('#6a4a2c'))
    dk = hx('#3a2a50')
    px_line(c, (16, 14), (16, 9.6), dk)
    px_line(c, (16, 14), (19.3, 15.8), dk)
    c.px(16, 14, hx('#c02a3a'))
    c.spark(4, 5, hx('#ffffff')); c.spark(28, 6, hx('#e0d0ff'), big=True); c.spark(27, 27, hx('#fff4a8'))

@icon(58)  # 영혼 연꽃
def _(c):
    GH = ramp('#a8e0f8', hi='#ffffff', lo='#6a9ae0', dk='#4a4aa8')
    GH2 = ramp('#c8ecff', hi='#ffffff', lo='#88aef0', dk='#5a5ab8')
    c.glow(16, 14, 14, hx('#a0d8ff'), a0=50, rings=3)
    for (rx, y, col) in [(13.5, 28, '#6aa8e8'), (9, 30, '#8ac0f0')]:
        c.flat(ell(16, y, rx, 1.6) & ~ell(16, y, rx - 1.6, 0.5), hx(col), layer=c.back)
    PAD = ramp('#58b8c8', hi='#b0f0f0', lo='#3a80b0', dk='#24508a')
    pad = ell(16, 27.6, 13.5, 3.4)
    c.shade(pad, PAD, R=3, soft=0)
    vein(c, (16, 28), (6, 27), PAD[2], pad); vein(c, (16, 28), (26, 27.5), PAD[2], pad)
    base = (16, 26.6)
    order = [(-90 - 72, 12.5, 3.4, 0), (-90 + 72, 12.5, 3.4, 0), (-90 - 46, 17.5, 4.0, 1), (-90 + 46, 17.5, 4.0, 1), (-90 - 22, 21.5, 4.2, 1), (-90 + 22, 21.5, 4.2, 1), (-90, 23.5, 4.2, 2)]
    for (ang, L, w, kind) in order:
        m = leaf(base, polar(base[0], base[1], L, ang), w, skew=0.3, pw=0.78)
        if kind:
            c.flat(grow(m), GH[3])
        c.shade(m, GH2 if kind == 2 else GH, R=2.8, soft=1)
        vein(c, polar(*base, 5, ang), polar(*base, L * 0.72, ang), GH[2], m)
    c.shade(flame(16, 4.2, 2.0, 4.0, 0.8, 0.4), ramp('#d8f8ff', hi='#ffffff', lo='#98c8f8', dk='#6a7ad0'), R=1.6, soft=0)
    c.spark(5, 8, hx('#ffffff')); c.spark(27, 9, hx('#d8f0ff'), big=True); c.spark(27, 24, hx('#e8e0ff'))
    c.dot(5, 17, hx('#d8f0ff')); c.dot(28, 16, hx('#d8f0ff'))

@icon(59)  # 소원 민들레
def _(c):
    WH = P('#ffffff', '#fff2d8', '#e8c8a8', '#b09078')
    c.glow(12, 19, 13, hx('#fff0b0'), a0=40, rings=3)
    stem(c, [(12, 24), (11.5, 28), (12, 31)], 2)
    cx, cy = 12, 19
    head = ell(cx, cy, 7.4)
    c.shade(head, WH, R=6.5, soft=1)
    for i in range(16):
        a = i * 22.5 + 8
        col = WH[0] if i % 2 == 0 else WH[2]
        px_line(c, polar(cx, cy, 2, a), polar(cx, cy, 7.4, a), col)
        c.px(*[int(v) for v in polar(cx, cy, 8.6, a)], WH[0] if i % 2 == 0 else WH[1])
    c.flat(ell(cx, cy, 1.4), hx('#ffd060'))
    # 날아가는 씨앗 (낙하산)
    def seed(x, y, big=False):
        W_, G_ = hx('#ffffff'), hx('#ffe9b0')
        L = c.front
        c.px(x - 2, y - 2, G_, layer=L); c.px(x, y - 2, W_, layer=L); c.px(x + 2, y - 2, G_, layer=L)
        for dx in (-1, 0, 1):
            c.px(x + dx, y - 1, W_ if dx == 0 else G_, layer=L)
        c.px(x, y, W_, layer=L)
        c.px(x, y + 1, hx('#d89a30'), layer=L)
    seed(21, 12, True); seed(26.5, 7, True); seed(27, 18); seed(18, 5); seed(12, 6)
    c.glow(21.5, 11, 3.5, hx('#fff0a0'), a0=70, rings=2)
    c.glow(27, 6, 3.5, hx('#fff0a0'), a0=70, rings=2)
    c.spark(28, 12, hx('#ffe888'), big=True); c.spark(4, 6, hx('#fff4c0'))

# === MAIN ===
def build(preview_dir=None):
    sheet = Image.new('RGBA', (320, 192), (0, 0, 0, 0))
    for idx in range(60):
        if idx in (0, 1, 2, 9):
            continue
        f = ICONS.get(idx)
        if not f:
            continue
        c = Cv()
        f(c)
        c.outline()
        sheet.alpha_composite(c.image(), ((idx % 10) * N, (idx // 10) * N))
    out = os.path.join(ROOT, 'public', 'art', 'plants.png')
    sheet.save(out)
    print('saved', out, 'icons', len([i for i in ICONS if i in range(60)]))
    if preview_dir:
        preview(sheet, preview_dir)

def preview(sheet, d):
    os.makedirs(d, exist_ok=True)
    bg = Image.new('RGBA', sheet.size, (0x21, 0x17, 0x33, 255))
    bg.alpha_composite(sheet)
    bg.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(os.path.join(d, 'plants_x4.png'))
    names = NAMES
    S = 4
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 12)
    except Exception:
        font = ImageFont.load_default()
    big = bg.resize((sheet.width * S, sheet.height * S), Image.NEAREST)
    cell = N * S
    lab = Image.new('RGBA', (big.width, big.height + 6 * 18), (0x21, 0x17, 0x33, 255))
    # 각 행 아래에 이름 줄
    full = Image.new('RGBA', (big.width, 6 * (cell + 16)), (0x21, 0x17, 0x33, 255))
    dr = ImageDraw.Draw(full)
    for r in range(6):
        full.paste(big.crop((0, r * cell, big.width, (r + 1) * cell)), (0, r * (cell + 16)))
        for k in range(10):
            idx = r * 10 + k
            dr.text((k * cell + 2, r * (cell + 16) + cell + 1), '%d %s' % (idx, names[idx]), font=font, fill=(220, 210, 240, 255))
    full.save(os.path.join(d, 'plants_labeled.png'))
    # 행별 큰 미리보기(6배)
    for part in range(3):
        sub = bg.crop((0, part * 64, 320, part * 64 + 64)).resize((320 * 3, 64 * 3), Image.NEAREST)
        sub.save(os.path.join(d, 'rows_%d.png' % part))

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
