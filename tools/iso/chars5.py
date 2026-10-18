# 귀여운 2등신 캐릭터 조합 부품 (직접 그린 픽셀): out/avatar_parts.png + out/avatar_parts.json
# 한 칸 44×60, 한 줄 = 한 층의 6프레임 (앞: 서기·걷기A·걷기B, 뒤: 서기·걷기A·걷기B)
# 색을 고를 수 있는 곳은 회색 열쇠색(240 밝음 / 200 / 150 / 100 어두움)으로 그려요.
# 게임은 그 밝기에 고른 팔레트를 입히고, 다 합친 뒤 바깥 테두리를 둘러요.
import json, math
import numpy as np
from PIL import Image, ImageDraw
FW, FH = 44, 60
K0, K1, K2, K3 = (240,) * 3, (200,) * 3, (150,) * 3, (100,) * 3
def hexc(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
DARK, WHITE, BLUSH, BLUSH2, MOUTH, TONGUE, TEAR = hexc('#2A1830'), hexc('#FFFFFC'), hexc('#FFA0B4'), hexc('#FF8AA4'), hexc('#7A2040'), hexc('#F2788E'), hexc('#8AD8FF')
X0 = 21.5                                  # 좌우 대칭 축
def mx(x): return int(round(2 * X0 - x))

class Lay:
    """한 층 = 6프레임 RGBA"""
    def __init__(self): self.f = [np.zeros((FH, FW, 4), np.uint8) for _ in range(6)]
    def put(self, fr, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < FW and 0 <= y < FH: self.f[fr][y, x] = (*c, 255)
    def mask_paint(self, fr, m, c):
        self.f[fr][m] = (*c, 255)
    def clear(self, fr, m): self.f[fr][m] = 0
    def empty(self, frs=range(6)): return all(self.f[i][..., 3].max() == 0 for i in frs)
def blank(): return np.zeros((FH, FW), bool)
def ell(x0, y0, x1, y1):
    im = Image.new('1', (FW, FH)); ImageDraw.Draw(im).ellipse([x0, y0, x1, y1], fill=1); return np.array(im)
def poly(pts):
    im = Image.new('1', (FW, FH)); ImageDraw.Draw(im).polygon(pts, fill=1); return np.array(im)
def rect(x0, y0, x1, y1):
    m = blank(); m[max(0, int(y0)):int(y1) + 1, max(0, int(x0)):int(x1) + 1] = True; return m
def sym(m): return m | m[:, ::-1]           # 좌우 대칭으로
def shift(m, dy=0, dx=0):
    o = blank(); H, W = m.shape
    ys, xs = np.nonzero(m); ys, xs = ys + dy, xs + dx; k = (ys >= 0) & (ys < H) & (xs >= 0) & (xs < W); o[ys[k], xs[k]] = True; return o
def edge_br(m):   # 아래·오른쪽 가장자리 (그림자 쪽)
    return m & ~(shift(m, -1) & shift(m, 0, -1))
def edge_tl(m):   # 위·왼쪽 가장자리 (빛 쪽)
    return m & ~(shift(m, 1) & shift(m, 0, 1))
def shade(L, fr, m, base=K1, dark=K2, light=None, rim=None):
    L.mask_paint(fr, m, base)
    L.mask_paint(fr, edge_br(m) & ~edge_tl(m), dark)
    if light: L.mask_paint(fr, edge_tl(m) & ~edge_br(m), light)
    if rim: L.mask_paint(fr, m & ~shift(m, -1), rim)

# ---------------- 기본 몸 (피부) ----------------
HEAD = ell(8, 8, 35, 35)                      # 28×28 큰 머리
HEAD_TOP, CHIN = 8, 35
EARS = sym(ell(6, 21, 9, 27))
TORSO = poly([(16, 36), (27, 36), (29, 46), (14, 46)])
ARMS = sym(poly([(16, 37), (13, 38), (11, 44), (14, 45), (16, 40)]))
HANDS = sym(ell(10, 43, 14, 47))
LEGS = sym(rect(16, 46, 20, 56))
def body_masks(back=False):
    return TORSO, ARMS, HANDS, LEGS, rect(19, 33, 24, 37)
def make_body():
    L = Lay()
    for fr in (0, 3):
        torso, arms, hands, legs, neck = body_masks(fr == 3)
        for m in (legs, torso, neck, arms, hands): shade(L, fr, m)
    return L
def make_head():
    L = Lay()
    for fr in (0, 3):
        shade(L, fr, EARS, K1, K2)
        L.mask_paint(fr, sym(ell(7, 23, 8, 25)), K2)          # 귓속
        shade(L, fr, HEAD, K1, K2)
        L.mask_paint(fr, HEAD & ~shift(HEAD, -2) & ~edge_br(HEAD), K2)   # 턱 아래 그늘 2줄
        if fr == 0:
            for x, y in ((13, 12), (14, 11), (15, 11), (12, 13)): L.put(fr, x, y, K0)   # 이마 빛
    return L
def make_blush():
    L = Lay()
    for x in (10, 11, 12, 13):
        for y in (31, 32):
            c = BLUSH if (x + y) % 2 else BLUSH2
            if (x, y) in ((10, 32), (13, 32)): continue
            L.put(0, x, y, c); L.put(0, mx(x), y, c)
    return L

# ---------------- 눈 (6×7, 왼쪽 눈 기준 / 오른쪽은 거울) ----------------
# . 없음  # 진한 선  0~3 눈동자(눈 색)  w 흰자  h 반짝이  p 분홍  b 눈물  k 진한 점
EYES = [
 ('반짝 동글', ["..###..", ".#####.", "#33333#", "#3hh33#", "#2hh22#", "#21112#", "#111h1#", ".#111#."]),
 ('큰 눈',     [".#####.", "#######", "#33333#", "#3hhw3#", "#2hw22#", "#22222#", "#11h11#", ".#####."]),
 ('졸린 눈',   [".......", ".......", ".......", "#######", "#33333#", "#2hh22#", "#11111#", ".#####."]),
 ('웃는 눈',   [".......", ".......", "..###..", ".##.##.", "##...##", "#.....#", ".......", "......."]),
 ('고양이',    ["#.....#", ".#####.", "#33#33#", "#3h#33#", "#22#22#", "#21#12#", "#11#11#", ".#####."]),
 ('별 눈',     ["..###..", ".#3#3#.", "#33333#", "#3h0h3#", "#20002#", "#22022#", "#11111#", ".#####."]),
 ('하트 눈',   ["..###..", ".#####.", "#0#3#0#", "#00000#", "#00000#", "#20002#", "#22022#", ".#####."]),
 ('윙크',      None),
 ('다짐',      ["##.....", "####...", "#33####", "#3hh33#", "#2h222#", "#21112#", ".#####.", "......."]),
 ('눈물',      [".......", ".#####.", "#33333#", "#3hh33#", "#2hh22#", "#2h112#", "#1111h#", "b#####."]),
 ('빙글빙글',  [".#####.", "#.....#", "#.###.#", "#.#.#.#", "#.#...#", "#.#####", "#......", ".#####."]),
 ('점 눈',     [".......", ".......", "..##...", ".####..", ".####..", "..##...", ".......", "......."]),
 ('뱀파이어',  [".......", "#######", "#33333.", "#3hh2#.", "#2h11#.", "#2111#.", ".####..", "......."]),
 ('순정 반짝', ["#.###.#", ".#####.", "#3hh33#", "#3hhw3#", "#2w222#", "#2h112#", "#11hh1#", ".#####."]),
 ('질끈',      [".......", "##.....", "..##...", "....##.", "..##...", "##.....", ".......", "......."]),
]
WINK_R = [".......", ".......", ".......", ".#####.", "##...##", ".......", ".......", "......."]
def make_eye(i):
    L = Lay(); name, pat = EYES[i]
    pats = (EYES[0][1], WINK_R) if pat is None else (pat, None)
    def draw(p, mirror):
        for r, row in enumerate(p):
            for c, ch in enumerate(row):
                if ch == '.': continue
                x = 11 + c; y = 22 + r
                if mirror: x = mx(x)
                col = {'#': DARK, 'k': DARK, 'w': WHITE, 'h': WHITE, 'p': BLUSH, 'b': TEAR, '0': K0, '1': K1, '2': K2, '3': K3}[ch]
                L.put(0, x, y, col)
    draw(pats[0], False)
    if pats[1] is None: draw(pats[0], True)
    else: draw(pats[1], True)
    if name == '눈물':
        for y in (30, 31, 32): L.put(0, 11, y, TEAR); L.put(0, mx(11), y, TEAR)
    return L
def make_brows(i):
    """눈썹 (머리 색). 눈 모양마다 표정이 달라요"""
    L = Lay(); name = EYES[i][0]
    shape = {'다짐': [(11, 18), (12, 18), (13, 19), (14, 19), (15, 20), (16, 20)], '뱀파이어': [(11, 18), (12, 18), (13, 19), (14, 19), (15, 19)],
             '눈물': [(12, 20), (13, 19), (14, 19), (15, 18), (16, 18)], '졸린 눈': [(12, 22), (13, 22), (14, 22), (15, 22), (16, 22)]}.get(name, [(12, 19), (13, 18), (14, 18), (15, 18), (16, 19)])
    for x, y in shape: L.put(0, x, y, K3); L.put(0, mx(x), y, K3)
    return L

# ---------------- 입 (8×4, 가운데 x 18~25) ----------------
# # 진한 선  r 입 속  t 혀  w 이  . 없음
MOUTHS = [
 ('미소',     ["........", "..#..#..", "...##...", "........"]),
 ('고양이 입', ["........", ".#..#..#", "..##.##.", "........"]),
 ('시무룩',   ["........", "...##...", "..#..#..", "........"]),
 ('송곳니',   ["........", "..####..", "..#ww#..", "...w...."]),
 ('활짝',     ["..####..", ".#rrrr#.", ".#rttr#.", "..####.."]),
 ('놀람',     ["...##...", "..#rr#..", "..#rr#..", "...##..."]),
 ('메롱',     ["........", "..####..", "...tt...", "...tt..."]),
 ('일자',     ["........", "..####..", "........", "........"]),
 ('이 보이게', [".######.", ".#wwww#.", "..####..", "........"]),
 ('오물오물', ["........", ".#.#.#..", "#.#.#.#.", "........"]),
]
def make_mouth(i):
    L = Lay(); _, pat = MOUTHS[i]
    for r, row in enumerate(pat):
        for c, ch in enumerate(row):
            if ch == '.': continue
            L.put(0, 18 + c, 31 + r, {'#': MOUTH, 'r': hexc('#A8304E'), 't': TONGUE, 'w': WHITE}[ch])
    return L

# ---------------- 머리카락 ----------------
def bangs_profile(kind):
    """x(9~34) → 앞머리 아랫끝 y"""
    def f(x):
        u = x - 9
        if kind == 'blunt': return 21 + (1 if x in (10, 33) else 0)
        if kind == 'hime': return 22
        if kind == 'swept': return int(16 + u * .32) + (1 if u % 4 == 0 else 0)
        if kind == 'swept_r': return int(16 + (25 - u) * .32) + (1 if u % 4 == 0 else 0)
        if kind == 'center': return int(15 + abs(x - X0) * .55)
        if kind == 'curtain': return int(14 + abs(x - X0) * .7) if abs(x - X0) > 1.5 else 14
        if kind == 'spiky': return 19 + [0, 2, 3, 1][u % 4]
        if kind == 'messy': return 18 + [1, 3, 0, 2, 4, 1, 2][u % 7]
        if kind == 'short': return 16 + (u % 3 == 1)
        if kind == 'side': return 15 if x < 17 else int(15 + (x - 17) * .5)
        if kind == 'eye': return int(20 + (x - 9) * .35) if x > 15 else 18
        if kind == 'none': return 13
        if kind == 'buzz': return 14
        return 20
    return f
def hair_cap(bangs, top=5, wide=6, shine=True):
    """머리 위 덮개 + 앞머리 (앞모습 위층)"""
    cap = ell(5, top, 38, 33)
    f = bangs_profile(bangs); m = cap.copy()
    for x in range(FW):
        yb = f(min(34, max(9, x))) if 9 <= x <= 34 else 30
        m[yb + 1:, x] = False
    return m
def side_locks(y_end, w=4):
    return sym(rect(6, 14, 6 + w - 1, y_end) & ~ell(-10, y_end - 3, 6, y_end + 20)) | sym(ell(5, y_end - 4, 6 + w, y_end + 1) & rect(0, y_end - 3, 43, y_end))
class Hair:
    def __init__(self): self.o, self.u, self.b = Lay(), Lay(), Lay()   # 앞 위층, 앞 아래층(몸 뒤), 뒷모습
def paint_hair(L, fr, m, top=5, shine=True, inner=None):
    """부드러운 머리 음영: 기본색 → 오른쪽·아래 그늘 → 맨 아래 진한 선 → 왼쪽 위 빛 → 천사링"""
    if not m.any(): return
    L.mask_paint(fr, m, K1)
    L.mask_paint(fr, m & ~shift(m, 0, -2), K2)                 # 오른쪽 2줄 그늘
    L.mask_paint(fr, m & ~shift(m, -2), K2)                    # 아래 2줄 그늘
    L.mask_paint(fr, m & ~shift(m, -1), K3)                    # 맨 아래 끝
    L.mask_paint(fr, m & ~shift(m, 0, 1) & ~shift(m, 1) & rect(0, 0, 21, 63), K0)   # 왼쪽 위 테두리 빛
    if inner is not None: L.mask_paint(fr, inner & m, K2)
    if shine:   # 천사링: 머리 곡선을 따라가는 반짝이 띠
        for x in range(10, 34):
            t = (x - X0) / 13.0
            y = int(round(top + 5 + 4 * t * t))
            if x % 7 in (3,): continue
            for dy in (0, 1):
                if m[y + dy, x] and m[y + dy + 2, x] and m[y + dy - 2, x]: L.put(fr, x, y + dy, K0 if (dy == 0 or x % 3) else K1)
def bang_notches(L, fr, m, f):
    """앞머리 끝 갈라짐"""
    for x in range(11, 33, 4):
        yb = f(x)
        for y in range(yb - 3, yb + 1):
            if m[y, x]: L.put(fr, x, y, K2)
def make_hair(spec):
    """spec: dict(bangs, len, extras...). len: buzz/short/bob/shoulder/long/vlong"""
    H = Hair(); bangs = spec.get('bangs', 'blunt'); ln = spec.get('len', 'bob'); ex = spec.get('ex', [])
    top = spec.get('top', 5)
    endY = {'buzz': 18, 'short': 22, 'bob': 31, 'shoulder': 38, 'long': 46, 'vlong': 56}[ln]
    for fr in (0, 3):
        back = fr == 3
        over, under = blank(), blank()
        if 'mohawk' in ex:
            strip = rect(18, 2, 25, 20) & ell(17, 1, 26, 26)
            spikes = poly([(18, 6), (19, 0), (21, 5), (22, 0), (24, 5), (25, 1), (26, 8)])
            over |= strip | spikes
            buzz = (HEAD & ~shift(HEAD, 3)) & rect(0, 0, 43, 20)
            H.o.mask_paint(fr, buzz & ~over, K2) if not back else H.b.mask_paint(fr, buzz & ~over, K2)
        elif 'cornrow' in ex:
            over |= ell(8, 7, 35, 30) & rect(0, 0, 43, 17)
        elif ln == 'buzz':
            over |= ell(8, 7, 35, 30) & rect(0, 0, 43, 15) | sym(rect(8, 12, 9, 20))
        else:
            cap = hair_cap(bangs, top)
            if back: cap = ell(5, top, 38, 36) & rect(0, 0, 43, max(endY, 30))
            over |= cap
            if ln in ('bob', 'shoulder', 'long', 'vlong'):
                sl = {'bob': 30, 'shoulder': 38, 'long': 47, 'vlong': 56}[ln]
                locks = side_locks(min(sl, 34) if ln != 'bob' else sl)
                if not back: over |= locks
                vol = ell(4, top + 1, 39, min(sl, 34) + 4) & rect(0, 0, 43, min(sl, 34))
                if ln in ('long', 'vlong', 'shoulder'):   # 끝으로 갈수록 좁아지고 끝이 갈라져요
                    w0 = 4 if ln != 'shoulder' else 5
                    vol |= poly([(w0, 18), (43 - w0, 18), (40 - w0 // 2, sl - 5), (37, sl), (33, sl - 3), (29, sl + 1), (25, sl - 2), (21.5, sl + 1), (18, sl - 2), (14, sl + 1), (10, sl - 3), (6, sl), (3 + w0 // 2, sl - 5)])
                if back: over |= vol | (ell(5, top, 38, 36) & rect(0, 0, 43, 33))
                else: under |= vol
            if ln == 'short' and back: over |= ell(6, top, 37, 33) & rect(0, 0, 43, 26)
        # 꾸밈
        if 'twin' in ex or 'twinlow' in ex:
            y0 = 12 if 'twin' in ex else 26
            t = sym(ell(0, y0, 8, y0 + 22) | ell(2, y0 - 2, 9, y0 + 4))
            under |= t
            if back: over |= t
        if 'pony' in ex:
            t = ell(30, 10, 41, 40) & ~ell(30, 30, 37, 46) if not back else ell(16, 6, 27, 46)
            if back: over |= t
            else: under |= t
        if 'sidepony' in ex:
            t = ell(32, 14, 42, 44)
            under |= t if not back else blank(); over |= t if back else blank()
        if 'lowpony' in ex:
            t = poly([(30, 30), (36, 34), (38, 48), (33, 52), (31, 40)]) if not back else poly([(19, 30), (24, 30), (26, 46), (21, 52), (18, 44)])
            (over if back else under).__ior__(t)
        if 'bun' in ex: over |= ell(15, -1, 28, 9)
        if 'buns' in ex: over |= sym(ell(5, 2, 15, 12))
        if 'starbun' in ex: over |= poly([(21.5, -1), (24, 4), (29, 4), (25, 7), (27, 12), (21.5, 9), (16, 12), (18, 7), (14, 4), (19, 4)])
        if 'topknot' in ex: over |= ell(17, 0, 26, 7)
        if 'braid' in ex:
            for k in range(6):
                bm = ell(30, 28 + k * 4, 36, 33 + k * 4)
                (over if not back else over).__ior__(bm)
        if 'braids' in ex:
            for k in range(6): over |= sym(ell(5, 30 + k * 4, 11, 35 + k * 4)) if not back else sym(ell(12, 30 + k * 4, 18, 35 + k * 4))
        if 'drill' in ex:
            for k in range(4): under |= sym(ell(0, 18 + k * 5, 8, 24 + k * 5))
            if back: over |= sym(ell(0, 18, 8, 39))
        if 'afro' in ex:
            puff = ell(1, 0, 42, 36)
            if back: over |= puff
            else: under |= puff; over |= ell(5, 2, 38, 26) & ~rect(0, 17, 43, 63)
        if 'curly' in ex:
            for cx, cy in ((9, 9), (15, 6), (22, 5), (28, 6), (34, 9), (7, 15), (36, 15)): over |= ell(cx - 4, cy - 4, cx + 4, cy + 4)
            if back:
                for cx, cy in ((8, 20), (35, 20), (14, 25), (29, 25), (21, 27)): over |= ell(cx - 5, cy - 5, cx + 5, cy + 5)
        if 'wavy' in ex:
            w = blank()
            for k in range(5): w |= sym(ell(1 + (k % 2), 16 + k * 7, 9 + (k % 2), 25 + k * 7))
            under |= w
            if back: over |= w
        if 'wild' in ex:
            w = poly([(5, 14), (1, 28), (4, 30), (2, 42), (7, 40), (7, 50), (12, 44), (15, 50), (18, 43), (25, 43), (28, 50), (31, 44), (36, 50), (36, 40), (41, 42), (39, 30), (42, 28), (38, 14)])
            under |= w
            if back: over |= w
            over |= poly([(8, 8), (5, 3), (12, 6), (14, 1), (18, 5), (22, 0), (26, 5), (30, 1), (32, 6), (38, 3), (35, 9)])
        if 'ahoge' in ex:
            for x, y in ((21, 4), (22, 3), (23, 2), (24, 2), (25, 3), (25, 4), (24, 5)): over[y, x] = True
        if 'spikes' in ex:
            over |= poly([(7, 12), (3, 6), (10, 8), (11, 1), (16, 6), (20, -1), (23, 5), (28, 0), (30, 7), (37, 3), (35, 10), (40, 12), (34, 14), (9, 14)])
        if 'mullet' in ex:
            t = rect(10, 28, 33, 40) & ~rect(14, 28, 29, 34)
            under |= t
            if back: over |= rect(10, 20, 33, 40)
        if 'eyecover' in ex and not back:
            over |= poly([(20, 12), (34, 14), (34, 31), (30, 33), (27, 26), (22, 22)])
        if 'slick' in ex: over |= ell(7, 4, 36, 22) & rect(0, 0, 43, 13)
        # 칠하기
        tgt_o = H.b if back else H.o
        if not back: paint_hair(H.u, fr, under & ~over, top, shine=False)
        paint_hair(tgt_o, fr, over, top)
        if not back and ln != 'buzz' and 'mohawk' not in ex: bang_notches(tgt_o, fr, over, bangs_profile(bangs))
        if 'cornrow' in ex:
            for x in range(11, 33, 3):
                for y in range(9, 17):
                    if over[y, x]: tgt_o.put(fr, x, y, K3)
    return H
HAIRS = [
 ('단발', dict(bangs='blunt', len='bob')),
 ('긴 생머리', dict(bangs='blunt', len='long')),
 ('양갈래', dict(bangs='blunt', len='short', ex=['twin'])),
 ('올림 똥머리', dict(bangs='swept', len='short', ex=['bun'])),
 ('숏컷', dict(bangs='short', len='short')),
 ('삐죽 숏', dict(bangs='spiky', len='short')),
 ('뾰족뾰족', dict(bangs='spiky', len='short', ex=['spikes'])),
 ('포니테일', dict(bangs='swept', len='short', ex=['pony'])),
 ('아프로', dict(bangs='short', len='short', ex=['afro'])),
 ('옆 땋은 머리', dict(bangs='side', len='short', ex=['braid'])),
 ('히메컷', dict(bangs='hime', len='long')),
 ('울프컷', dict(bangs='messy', len='shoulder')),
 ('스포츠', dict(bangs='buzz', len='buzz')),
 ('부스스', dict(bangs='messy', len='short', ex=['ahoge'])),
 ('가르마 올백', dict(bangs='side', len='short', ex=['slick'])),
 ('낮은 양갈래', dict(bangs='center', len='short', ex=['twinlow'])),
 ('양쪽 똥머리', dict(bangs='blunt', len='short', ex=['buns'])),
 ('긴 웨이브', dict(bangs='center', len='long', ex=['wavy'])),
 ('멀릿', dict(bangs='spiky', len='short', ex=['mullet'])),
 ('커튼 앞머리', dict(bangs='curtain', len='shoulder')),
 ('모히칸', dict(bangs='none', len='buzz', ex=['mohawk'])),
 ('땋은 두 갈래', dict(bangs='center', len='short', ex=['braids'])),
 ('반묶음', dict(bangs='swept_r', len='long', ex=['topknot'])),
 ('드릴 머리', dict(bangs='blunt', len='short', ex=['drill'])),
 ('곱슬 숏', dict(bangs='short', len='short', ex=['curly'])),
 ('올백', dict(bangs='none', len='short', ex=['slick'])),
 ('상투', dict(bangs='none', len='short', ex=['topknot'])),
 ('복슬복슬', dict(bangs='messy', len='bob', ex=['curly'])),
 ('옆으로 넘김', dict(bangs='swept', len='short')),
 ('옆 포니테일', dict(bangs='swept_r', len='short', ex=['sidepony'])),
 ('바닥까지 긴 머리', dict(bangs='blunt', len='vlong')),
 ('바가지', dict(bangs='blunt', len='short')),
 ('경단 머리', dict(bangs='center', len='short', ex=['buns', 'ahoge'])),
 ('콘로우', dict(bangs='none', len='buzz', ex=['cornrow'])),
 ('더듬이', dict(bangs='blunt', len='bob', ex=['ahoge'])),
 ('한쪽 눈 가림', dict(bangs='eye', len='shoulder', ex=['eyecover'])),
 ('낮은 포니테일', dict(bangs='center', len='short', ex=['lowpony'])),
 ('마녀 장발', dict(bangs='messy', len='long', ex=['wild'])),
 ('단정 앞머리', dict(bangs='hime', len='bob')),
 ('별 똥머리', dict(bangs='swept', len='short', ex=['starbun'])),
]

# ---------------- 교복 ----------------
UNIS = ['춘추복', '하복', '동복', '체육복', '생활복']
def make_uni(k):
    cloth, house, shoes = Lay(), Lay(), Lay()
    for fr in (0, 3):
        back = fr == 3
        torso = poly([(15, 35), (28, 35), (30, 47), (13, 47)])
        slv = sym(poly([(16, 36), (12, 37), (10, 43), (14, 44), (16, 39)]))
        pants = sym(rect(15, 46, 21, 54)) | rect(15, 46, 28, 48)
        sh = sym(ell(14, 53, 21, 58) | rect(15, 54, 21, 57))
        if k == 0:    # 춘추복: 블레이저 + 넥타이 + 바지
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K2, K3, light=K1)
            if not back:
                cloth.mask_paint(fr, poly([(18, 35), (25, 35), (21.5, 42)]), WHITE)
                house.mask_paint(fr, rect(21, 37, 22, 43) | rect(20, 36, 23, 37), K1); house.put(fr, 21, 44, K2); house.put(fr, 22, 44, K2)
                cloth.put(fr, 18, 43, hexc('#F0C850')); cloth.put(fr, 18, 45, hexc('#F0C850'))
                cloth.mask_paint(fr, sym(poly([(17, 35), (19, 35), (21, 41), (19, 40)])), K3)
            else: house.mask_paint(fr, rect(14, 46, 29, 46), K1)
            house.mask_paint(fr, sym(rect(10, 42, 13, 42)), K1)
        elif k == 1:  # 하복: 반팔 셔츠 + 니트 조끼 + 연한 바지
            shade(cloth, fr, pants, K1, K2); shade(cloth, fr, torso, K2, K3, light=K1)
            cloth.mask_paint(fr, sym(poly([(16, 36), (12, 37), (12, 40), (16, 39)])), WHITE); cloth.mask_paint(fr, sym(rect(12, 40, 14, 40)), hexc('#D8D4E4'))
            if not back:
                cloth.mask_paint(fr, poly([(17, 35), (26, 35), (21.5, 41)]), WHITE)
                house.mask_paint(fr, poly([(17, 36), (18, 36), (21.5, 41), (25, 36), (26, 36), (21.5, 43)]), K1)
            house.mask_paint(fr, rect(13, 46, 30, 46), K1)
        elif k == 2:  # 동복: 긴 코트 + 목도리
            coat = poly([(15, 35), (28, 35), (31, 52), (12, 52)]); shade(cloth, fr, sym(rect(15, 51, 21, 54)), K3, K3)
            shade(cloth, fr, coat | sym(poly([(16, 36), (11, 37), (9, 44), (14, 45), (16, 39)])), K1, K2, light=K0)
            if not back:
                cloth.mask_paint(fr, rect(21, 38, 22, 52), K2)
                for y in (40, 44, 48): cloth.put(fr, 19, y, hexc('#E8902A')); cloth.put(fr, 24, y, hexc('#E8902A'))
            sc = poly([(14, 33), (29, 33), (30, 37), (13, 37)])
            shade(house, fr, sc, K1, K2)
            for x in range(14, 30, 4): house.mask_paint(fr, rect(x, 33, x + 1, 37) & sc, K0)
            if not back: shade(house, fr, rect(24, 37, 27, 43), K1, K2); house.mask_paint(fr, rect(24, 43, 27, 43), K0)
        elif k == 3:  # 체육복: 지퍼 저지 + 줄무늬 트랙팬츠
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K1, K2)
            house.mask_paint(fr, sym(poly([(12, 37), (13, 37), (11, 43), (10, 43)])) | sym(rect(15, 47, 15, 54)), K1)
            if not back: cloth.mask_paint(fr, rect(21, 35, 22, 47), K2); cloth.put(fr, 21, 36, K0)
            else: house.mask_paint(fr, rect(21, 36, 22, 46), K1)
            cloth.mask_paint(fr, rect(16, 34, 27, 35), K2)
        elif k == 4:  # 생활복: 후드티 + 조거
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K1, K2, light=K0)
            cloth.mask_paint(fr, sym(rect(15, 53, 21, 54)), K3)
            if not back:
                cloth.mask_paint(fr, rect(16, 42, 27, 42), K2); cloth.mask_paint(fr, rect(16, 43, 16, 45) | rect(27, 43, 27, 45), K2)
                house.mask_paint(fr, ell(19, 37, 24, 41), K1); house.put(fr, 21, 39, K0); house.put(fr, 22, 39, K0)
                cloth.put(fr, 19, 35, WHITE); cloth.put(fr, 19, 36, WHITE); cloth.put(fr, 24, 35, WHITE); cloth.put(fr, 24, 36, WHITE)
            else:
                shade(cloth, fr, ell(15, 31, 28, 40), K1, K2); house.mask_paint(fr, ell(19, 40, 24, 44), K1)
        shade(shoes, fr, sh, K1, K2); shoes.mask_paint(fr, sh & ~shift(sh, -1), K3)
        if k == 3: shoes.mask_paint(fr, sh & ~shift(sh, -1), WHITE)
        if k in (0, 2): shoes.mask_paint(fr, sh & ~shift(sh, 1), K0)
    return dict(cloth=cloth, house=house, shoes=shoes)

# ---------------- 프레임 만들기 ----------------
LEGTOP = 47
def copy_frames(L, front=True, back=True):
    for b in (0, 3):
        for k in (1, 2): L.f[b + k] = L.f[b].copy()
def walkify(L):
    """한쪽 다리를 2칸 들고, 반대쪽 팔을 1칸 내려요"""
    for b in (0, 3):
        src = L.f[b]
        for k, side in ((1, 'L'), (2, 'R')):
            dst = src.copy()
            leg = np.zeros((FH, FW), bool); leg[LEGTOP:, :22] = side == 'L'; leg[LEGTOP:, 22:] = side == 'R'
            m = leg & (src[..., 3] > 0)
            dst[m] = 0
            ys, xs = np.nonzero(m); dst[ys - 2, xs] = src[ys, xs]
            L.f[b + k] = dst
rows, Z = [], ['hairU', 'skin', 'cloth', 'head', 'face', 'hairO']
def row_of(L):
    im = np.zeros((FH, FW * 6, 4), np.uint8)
    for i in range(6): im[:, i * FW:(i + 1) * FW] = L.f[i]
    rows.append(im); return len(rows) - 1
def front_only(L):
    for k in (3, 4, 5): L.f[k][:] = 0
    return L
body = make_body(); walkify(body)
head = make_head(); copy_frames(head)
blush = make_blush(); copy_frames(blush); front_only(blush)
base = [[row_of(body), 'skin', 'skin'], [row_of(head), 'skin', 'head'], [row_of(blush), None, 'face']]
parts = dict(hair=[], eyes=[], mouth=[], uni=[])
for n, spec in HAIRS:
    H = make_hair(spec)
    for L in (H.o, H.u, H.b): copy_frames(L)
    front_only(H.o); front_only(H.u)
    for k in (0, 1, 2): H.b.f[k][:] = 0
    Ls = [[row_of(H.o), 'hair', 'hairO'], [row_of(H.b), 'hair', 'hairO']]
    if not H.u.empty((0,)): Ls.append([row_of(H.u), 'hair', 'hairU'])
    parts['hair'].append(dict(n=n, L=Ls))
for i, (n, _) in enumerate(EYES):
    e = make_eye(i); b = make_brows(i)
    for L in (e, b): copy_frames(L); front_only(L)
    parts['eyes'].append(dict(n=n, L=[[row_of(e), 'eye', 'face'], [row_of(b), 'hair', 'face']]))
for i, (n, _) in enumerate(MOUTHS):
    m = make_mouth(i); copy_frames(m); front_only(m)
    parts['mouth'].append(dict(n=n, L=[[row_of(m), None, 'face']]))
for k, n in enumerate(UNIS):
    U = make_uni(k)
    for L in U.values(): walkify(L)
    parts['uni'].append(dict(n=n, L=[[row_of(U['cloth']), 'cloth', 'cloth'], [row_of(U['house']), 'house', 'cloth'], [row_of(U['shoes']), 'shoes', 'cloth']]))
sheet = np.concatenate(rows, axis=0)
Image.fromarray(sheet, 'RGBA').save('out/avatar_parts.png')
# ---------------- 팔레트 ----------------
import colorsys
def ramp(h, hl=.4):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    H, L_, S = colorsys.rgb_to_hls(r, g, b)
    def mk(l, s, dh=0): rr, gg, bb = colorsys.hls_to_rgb((H + dh) % 1, max(0, min(1, l)), max(0, min(1, s))); return '#%02X%02X%02X' % (round(rr * 255), round(gg * 255), round(bb * 255))
    return [mk(L_ + (1 - L_) * hl, S), h.upper(), mk(L_ * .78, min(1, S * 1.05), -.02), mk(L_ * .58, min(1, S * 1.1), -.04)]
SKIN = [['#FFF2EA', '#FFE2D2', '#F4BCA6', '#D88E80'], ['#FFE6D6', '#FBCFB2', '#E8A488', '#C47A66'], ['#F6CFAA', '#E8AE82', '#C8875E', '#9C6244'],
        ['#D8A078', '#B87C54', '#93583A', '#6A3C28'], ['#9C6A4A', '#7A4A30', '#5C3420', '#3E2216']]
EYE = [ramp(h) for h in ['#7A5AE0', '#4AA8F0', '#2E7AD0', '#4AC878', '#2A9A54', '#6AD8C8', '#E8944A', '#B8682A', '#7A4A2E', '#F05A8A', '#E83A3A', '#B01E2A',
                          '#F0C040', '#C8A040', '#A890FF', '#C060E0', '#5A4A6A', '#3A3A4A', '#8A8A9A', '#40C8E8']]
HAIR = [ramp(h, .35) for h in ['#4A3A5A', '#2E2A36', '#6A4028', '#9A6A44', '#D0A050', '#F0D888', '#F6EEDC', '#F07A40', '#C8402E', '#8A2032',
                                '#FFA8C8', '#E07AA8', '#BCA0F6', '#7058B8', '#86E0C8', '#3A9080', '#9ACCF6', '#4A78B0', '#DCDCEC', '#9494B0']]
SHOES = [ramp(h) for h in ['#3A2A3A', '#5A3A2A', '#8A5A3A', '#ECE8F4', '#C0303E', '#3A6AB8', '#3A8A4C', '#E8702A', '#7A4ABA', '#F0C850']]
CLOTH = [['#EEECF4', '#B4B0C8', '#6E6A86', '#45415A']]
HOUSE = {'dew': ramp('#4CC484'), 'ember': ramp('#F0822E'), 'dusk': ramp('#EC6A9A'), 'moon': ramp('#7A62E8')}
STOP = [240, 200, 150, 100]
meta = dict(fw=FW, fh=FH, src='art/iso/avatar_parts.png', z=Z, base=base, parts=parts, outline=True,
            stops={k: STOP for k in ('skin', 'eye', 'hair', 'cloth', 'shoes', 'house')},
            pal=dict(skin=SKIN, eye=EYE, hair=HAIR, shoes=SHOES, cloth=CLOTH, house=HOUSE), head=dict(t=4, b=40))
json.dump(meta, open('out/avatar_parts.json', 'w'), ensure_ascii=False)
print('rows', len(rows), {k: len(v) for k, v in parts.items()})
