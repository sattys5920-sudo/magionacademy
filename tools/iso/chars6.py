# 귀여운 2등신 캐릭터 조합 부품 (직접 그린 픽셀, 앞·뒤·옆): out/avatar_parts.png + out/avatar_parts.json
# 한 칸 44×60, 한 줄 = 한 층의 9프레임 (앞: 서기·걷기A·걷기B, 뒤: 같은 3개, 옆(왼쪽 보기): 같은 3개)
# 오른쪽 옆은 게임이 옆모습을 뒤집어 그려요.
# 색을 고를 수 있는 곳은 회색 열쇠색(240 밝음 / 200 / 150 / 100 어두움)으로 그리고, 게임이 팔레트를 입혀요.
# 다 합친 뒤 바깥 테두리는 게임이 둘러요.
import json, math, colorsys
import numpy as np
from PIL import Image, ImageDraw
FW, FH, NF = 44, 60, 9
FRONT, BACK, SIDE = 0, 3, 6
K0, K1, K2, K3 = (240,) * 3, (200,) * 3, (150,) * 3, (100,) * 3
def hexc(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
DARK, WHITE, BLUSH, BLUSH2, MOUTH, TONGUE, TEAR = hexc('#2A1830'), hexc('#FFFFFC'), hexc('#FFA0B4'), hexc('#FF8AA4'), hexc('#7A2040'), hexc('#F2788E'), hexc('#8AD8FF')
X0 = 21.5
def mx(x): return int(round(2 * X0 - x))

class Lay:
    def __init__(self): self.f = [np.zeros((FH, FW, 4), np.uint8) for _ in range(NF)]
    def put(self, fr, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < FW and 0 <= y < FH: self.f[fr][y, x] = (*c, 255)
    def get(self, fr, x, y): return 0 <= x < FW and 0 <= y < FH and self.f[fr][y, x, 3] > 0
    def paint(self, fr, m, c): self.f[fr][m] = (*c, 255)
    def empty(self, frs=range(NF)): return all(self.f[i][..., 3].max() == 0 for i in frs)
def blank(): return np.zeros((FH, FW), bool)
def ell(x0, y0, x1, y1):
    im = Image.new('1', (FW, FH)); ImageDraw.Draw(im).ellipse([x0, y0, x1, y1], fill=1); return np.array(im)
def poly(pts):
    im = Image.new('1', (FW, FH)); ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=1); return np.array(im)
def rect(x0, y0, x1, y1):
    m = blank(); m[max(0, int(y0)):max(0, int(y1) + 1), max(0, int(x0)):max(0, int(x1) + 1)] = True; return m
def rows_le(y): m = blank(); m[:max(0, int(y) + 1)] = True; return m
def sym(m): return m | m[:, ::-1]
def shift(m, dy=0, dx=0):
    o = blank(); ys, xs = np.nonzero(m); ys, xs = ys + dy, xs + dx; k = (ys >= 0) & (ys < FH) & (xs >= 0) & (xs < FW); o[ys[k], xs[k]] = True; return o
def edge_br(m): return m & ~(shift(m, -1) & shift(m, 0, -1))
def edge_tl(m): return m & ~(shift(m, 1) & shift(m, 0, 1))
def shade(L, fr, m, base=K1, dark=K2, light=None):
    L.paint(fr, m, base); L.paint(fr, edge_br(m) & ~edge_tl(m), dark)
    if light: L.paint(fr, edge_tl(m) & ~edge_br(m), light)
def line(L, fr, pts, c, mask=None, gap=0):
    """점들을 잇는 1픽셀 선 (mask 안에서만)"""
    k = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(1, n - 1); x, y = int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t)); k += 1
            if gap and k % gap == 0: continue
            if mask is None or (0 <= y < FH and 0 <= x < FW and mask[y, x]): L.put(fr, x, y, c)

# ================= 몸 =================
HEAD_F = ell(8, 8, 35, 35)
HEAD_S = ell(9, 8, 34, 35) | ell(8, 16, 26, 35)
EARS_F = sym(ell(6, 21, 9, 27))
EAR_S = ell(22, 20, 26, 27)
def pose_front():
    return dict(torso=poly([(16, 36), (27, 36), (29, 46), (14, 46)]), arms=sym(poly([(16, 37), (13, 38), (11, 44), (14, 45), (16, 40)])),
                hands=sym(ell(10, 43, 14, 47)), legs=sym(rect(16, 46, 20, 56)), neck=rect(19, 33, 24, 37))
def pose_side(k):
    """옆(왼쪽 보기) 자세: k=0 서기, 1 앞발 내딛기, 2 반대"""
    legF = {0: poly([(17, 46), (20, 46), (20, 56), (17, 56)]), 1: poly([(17, 46), (20, 46), (18, 56), (14, 56)]), 2: poly([(17, 46), (20, 46), (23, 56), (19, 56)])}[k]
    legB = {0: poly([(21, 46), (24, 46), (24, 56), (21, 56)]), 1: poly([(21, 46), (24, 46), (27, 56), (23, 56)]), 2: poly([(21, 46), (24, 46), (21, 56), (17, 56)])}[k]
    footF = {0: 17, 1: 14, 2: 19}[k]; footB = {0: 21, 1: 23, 2: 17}[k]
    hx = {0: 20, 1: 22, 2: 17}[k]
    arm = poly([(19, 37), (23, 37), (hx + 3, 44), (hx, 44)])
    return dict(torso=poly([(17, 35), (26, 35), (27, 46), (16, 46)]), arm=arm, hand=ell(hx - 1, 42, hx + 3, 46), legF=legF, legB=legB,
                footF=footF, footB=footB, neck=rect(19, 33, 23, 37))
def make_body():
    L = Lay(); P = pose_front()
    for fr in (FRONT, BACK):
        for m in (P['legs'], P['torso'], P['neck'], P['arms'], P['hands']): shade(L, fr, m)
    for k in range(3):
        S = pose_side(k); fr = SIDE + k
        shade(L, fr, S['legB'], K2, K3); shade(L, fr, S['legF']); shade(L, fr, S['torso']); shade(L, fr, S['neck'])
        shade(L, fr, S['arm']); shade(L, fr, S['hand'])
    return L
def make_head():
    L = Lay()
    for fr in (FRONT, BACK):
        shade(L, fr, EARS_F, K1, K2); L.paint(fr, sym(ell(7, 23, 8, 25)), K2)
        shade(L, fr, HEAD_F, K1, K2); L.paint(fr, HEAD_F & ~shift(HEAD_F, -2) & ~edge_br(HEAD_F), K2)
        if fr == FRONT:
            for x, y in ((13, 12), (14, 11), (15, 11), (12, 13)): L.put(fr, x, y, K0)
    fr = SIDE
    shade(L, fr, HEAD_S, K1, K2); L.paint(fr, HEAD_S & ~shift(HEAD_S, -2) & ~edge_br(HEAD_S), K2)
    shade(L, fr, EAR_S, K1, K2); L.paint(fr, ell(23, 22, 24, 25), K2)
    for x, y in ((11, 13), (12, 12), (13, 12)): L.put(fr, x, y, K0)
    copy_side(L)
    return L
def make_blush():
    L = Lay()
    for x in (10, 11, 12, 13):
        for y in (31, 32):
            if (x, y) in ((10, 32), (13, 32)): continue
            c = BLUSH if (x + y) % 2 else BLUSH2
            L.put(FRONT, x, y, c); L.put(FRONT, mx(x), y, c)
    for x, y in ((12, 30), (13, 30), (14, 30), (12, 31), (13, 31), (14, 31), (15, 31)): L.put(SIDE, x, y, BLUSH if (x + y) % 2 else BLUSH2)
    return L

# ================= 눈·입 =================
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
EYE_COL = {'#': DARK, 'k': DARK, 'w': WHITE, 'h': WHITE, 'p': BLUSH, 'b': TEAR, '0': K0, '1': K1, '2': K2, '3': K3}
def make_eye(i):
    L = Lay(); name, pat = EYES[i]
    pl, pr = (EYES[0][1], WINK_R) if pat is None else (pat, pat)
    for p, mirror in ((pl, False), (pr, True)):
        for r, row in enumerate(p):
            for c, ch in enumerate(row):
                if ch != '.': L.put(FRONT, mx(11 + c) if mirror else 11 + c, 22 + r, EYE_COL[ch])
    # 옆: 앞쪽 눈 하나를 좁게 (가운데 열 하나 빼기)
    ps = pat or EYES[0][1]
    for r, row in enumerate(ps):
        for j, c in enumerate((0, 1, 2, 4, 5, 6)):
            ch = row[c]
            if ch != '.' and j < 5: L.put(SIDE, 10 + j, 22 + r, EYE_COL[ch])
    if name == '눈물':
        for y in (30, 31, 32): L.put(FRONT, 11, y, TEAR); L.put(FRONT, mx(11), y, TEAR); L.put(SIDE, 10, y, TEAR)
    copy_side(L)
    return L
def make_brows(i):
    L = Lay(); name = EYES[i][0]
    shape = {'다짐': [(11, 18), (12, 18), (13, 19), (14, 19), (15, 20), (16, 20)], '뱀파이어': [(11, 18), (12, 18), (13, 19), (14, 19), (15, 19)],
             '눈물': [(12, 20), (13, 19), (14, 19), (15, 18), (16, 18)], '졸린 눈': [(12, 22), (13, 22), (14, 22), (15, 22), (16, 22)]}.get(name, [(12, 19), (13, 18), (14, 18), (15, 18), (16, 19)])
    for x, y in shape: L.put(FRONT, x, y, K3); L.put(FRONT, mx(x), y, K3); L.put(SIDE, x - 2, y, K3)
    copy_side(L)
    return L
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
MCOL = {'#': MOUTH, 'r': hexc('#A8304E'), 't': TONGUE, 'w': WHITE}
def make_mouth(i):
    L = Lay(); _, pat = MOUTHS[i]
    for r, row in enumerate(pat):
        for c, ch in enumerate(row):
            if ch != '.': L.put(FRONT, 18 + c, 31 + r, MCOL[ch])
            if ch != '.' and 1 <= c <= 4: L.put(SIDE, 9 + c, 31 + r, MCOL[ch])
    copy_side(L)
    return L

# ================= 머리카락 =================
def bang_locks(kind, view):
    """앞머리 가닥들: (왼쪽 x, 오른쪽 x, 끝 x, 끝 y). 옆모습은 이마 앞쪽만"""
    L = []
    if view == 'side':
        tips = {'blunt': 21, 'hime': 22, 'swept': 19, 'swept_r': 22, 'center': 19, 'curtain': 20, 'spiky': 21, 'messy': 21, 'short': 16, 'side': 17, 'eye': 23}.get(kind)
        if tips is None: return []
        for i, x in enumerate(range(8, 21, 4)):
            ty = tips + (1 if i % 2 else 0) - (1 if kind in ('spiky', 'messy') and i % 2 else 0) + (2 if kind == 'curtain' and i == 0 else 0)
            L.append((x, x + 4, x - 1 if kind != 'swept_r' else x + 1, ty))
        return L
    if kind in ('none', 'buzz'): return []
    xs = list(range(9, 35, 4)) if kind not in ('spiky', 'messy') else [9, 14, 18, 23, 27, 31]
    for i, x in enumerate(xs):
        xr = (xs[i + 1] if i + 1 < len(xs) else 35); cx = (x + xr) / 2
        if kind == 'blunt': L.append((x, xr, cx, 21 + (i % 2)))
        elif kind == 'hime': L.append((x, xr, cx, 22))
        elif kind == 'swept': L.append((x, xr, x - 1, int(16 + (cx - 9) * .3)))
        elif kind == 'swept_r': L.append((x, xr, xr + 1, int(16 + (34 - cx) * .3)))
        elif kind == 'center': L.append((x, xr, cx + (-2 if cx < X0 else 2), int(15 + abs(cx - X0) * .55)))
        elif kind == 'curtain': L.append((x, xr, cx + (-3 if cx < X0 else 3), int(13 + abs(cx - X0) * .75)))
        elif kind == 'spiky': L.append((x, xr, cx, 19 + [0, 3, 1, 4, 0, 2][i % 6]))
        elif kind == 'messy': L.append((x, xr, cx + [-1, 1, 0, -1, 1, 0][i % 6], 18 + [2, 4, 1, 3, 0, 3][i % 6]))
        elif kind == 'short': L.append((x, xr, cx, 16 + (i % 2)))
        elif kind == 'side': L.append((x, xr, x - 1, 15 if cx < 17 else int(15 + (cx - 17) * .5)))
        elif kind == 'eye': L.append((x, xr, cx - 1, 18 if cx < 17 else int(20 + (cx - 17) * .7)))
    return L
def lock_poly(x0, x1, tx, ty, top=10):
    return poly([(x0, top), (x1, top), (x1, ty - 3), (tx + .5, ty + .5), (x0, ty - 3)])
class Hair:
    def __init__(self): self.o, self.u, self.sh = Lay(), Lay(), Lay()   # 위층, 아래층(몸 뒤), 이마 그림자(피부)
def paint_mass(L, fr, m, top, crown, view, back=False, dim=False):
    """머리 덩어리 음영: 기본 → 그늘 → 끝선 → 빛 → 천사링 → 머리결"""
    if not m.any(): return
    base, dark, deep = (K2, K3, K3) if dim else (K1, K2, K3)
    L.paint(fr, m, base)
    # 세로 그러데이션: 각 줄기 아래쪽 30%는 그늘
    for x in range(FW):
        ys = np.nonzero(m[:, x])[0]
        if len(ys) < 3: continue
        y0, y1 = ys.min(), ys.max(); cut = y0 + (y1 - y0) * (.62 if not back else .7)
        for y in ys:
            if y > cut: L.put(fr, x, y, dark)
    L.paint(fr, m & ~shift(m, 0, -2), dark)                    # 오른쪽 그늘
    L.paint(fr, m & ~shift(m, -1), deep)                       # 맨 아래 끝
    if not dim:
        L.paint(fr, m & ~shift(m, 0, 1) & ~shift(m, 1) & rows_le(top + 16), K0)   # 왼쪽 위 빛
        # 천사링 (끊어진 반짝이 띠)
        cx = crown[0]
        for x in range(4, 40):
            t = (x - cx) / 13.0; y = int(round(top + 5 + 4 * t * t))
            if x % 7 == 3: continue
            if m[y, x] and m[min(FH - 1, y + 2), x] and m[max(0, y - 2), x]:
                L.put(fr, x, y, K0)
                if x % 3 and m[y + 1, x]: L.put(fr, x, y + 1, K0 if x % 2 else K1)
        # 머리결: 정수리에서 퍼지는 곡선 (짧게 끊어서)
        for a in ((-55, -30, -10, 12, 34, 58) if view != 'side' else (-20, 10, 40, 70, 100)):
            ang = math.radians(a + 90); pts = []
            for r in range(6, 40, 2):
                bend = .012 * r * r * (1 if a > 0 else -1)
                pts.append((crown[0] + math.cos(ang) * r * 1.05 + bend, crown[1] + math.sin(ang) * r))
            line(L, fr, pts[2:], dark, mask=m & ~shift(m, -2) & ~rows_le(top + 7) if True else m, gap=4)
def paint_locks(L, fr, locks, mask_clip=None, top=10, dim=False):
    """앞머리 가닥: 가닥마다 빛·그늘, 사이 갈라짐"""
    allm = blank(); ms = []
    for (x0, x1, tx, ty) in locks:
        m = lock_poly(x0, x1, tx, ty, top)
        if mask_clip is not None: m &= mask_clip
        ms.append((m, x0, x1, tx, ty)); allm |= m
    for m, x0, x1, tx, ty in ms:
        L.paint(fr, m, K2 if dim else K1)
        L.paint(fr, m & ~shift(m, 0, -1), K2)                                  # 오른쪽 끝
        L.paint(fr, m & ~shift(m, 0, 1) & rows_le(ty - 4) & ~rows_le(top + 3), K0 if not dim else K1)   # 왼쪽 빛
        L.paint(fr, m & ~shift(m, -1), K3 if dim else K2)                       # 끝
    for m, x0, x1, tx, ty in ms:   # 가닥 사이 갈라짐
        for y in range(max(top + 4, ty - 6), ty):
            if 0 <= x1 < FW and allm[y, x1] and allm[y, x1 - 1]: L.put(fr, x1, y, K3)
    return allm
def make_hair(spec):
    H = Hair(); bangs = spec.get('bangs', 'blunt'); ln = spec.get('len', 'bob'); ex = spec.get('ex', []); top = spec.get('top', 5)
    sl = {'buzz': 18, 'short': 22, 'bob': 30, 'shoulder': 38, 'long': 47, 'vlong': 56}[ln]
    def long_vol(view):
        """어깨 아래로 내려오는 머리 (끝이 갈라진 모양)"""
        if ln not in ('shoulder', 'long', 'vlong'): return blank()
        if view == 'side':
            pts = [(24, 14), (38, 14), (39, sl - 5), (37, sl), (34, sl - 3), (31, sl + 1), (28, sl - 2), (25, sl - 4)]
            return poly(pts)
        w0 = 4 if ln != 'shoulder' else 5
        return poly([(w0, 18), (43 - w0, 18), (40 - w0 // 2, sl - 5), (37, sl), (33, sl - 3), (29, sl + 1), (25, sl - 2), (21.5, sl + 1), (18, sl - 2), (14, sl + 1), (10, sl - 3), (6, sl), (3 + w0 // 2, sl - 5)])
    def tip_lines(L, fr, m, dim=False):
        """긴 머리 끝 가닥 나눔"""
        ys = np.nonzero(m)[0]
        if not len(ys): return
        yb = ys.max()
        for x in range(7, 40, 5):
            for y in range(yb - 7, yb + 1):
                if m[y, x] and m[y, x - 1] and m[y, min(FW - 1, x + 1)]: L.put(fr, x, y, K3 if y > yb - 3 else K2)
    for view, frs in (('front', FRONT), ('back', BACK), ('side', SIDE)):
        fr = frs; back = view == 'back'; side = view == 'side'
        over, under, mass = blank(), blank(), blank()
        crown = (21.5, top + 2) if not side else (27, top + 3)
        # ---- 기본 덩어리 ----
        if 'mohawk' in ex:
            if side: crest = poly([(10, 10), (12, 3), (16, 6), (18, -1), (22, 4), (25, -1), (28, 4), (31, 1), (34, 8), (35, 14), (30, 10), (12, 13)])
            else: crest = (rect(18, 2, 25, 20) & ell(17, 1, 26, 26)) | poly([(18, 6), (19, 0), (21, 5), (22, 0), (24, 5), (25, 1), (26, 8)])
            buzz = ((HEAD_S if side else HEAD_F) & ~shift(HEAD_S if side else HEAD_F, 3)) & rows_le(20)
            (H.o).paint(fr, buzz & ~crest, K2)
            mass |= crest
        elif 'cornrow' in ex or ln == 'buzz':
            cap = (ell(9, 7, 35, 32) if side else ell(8, 7, 35, 30)) & rows_le(16 if 'cornrow' in ex else 14)
            if side: cap |= ell(14, 7, 36, 32) & rows_le(26) & ~ell(0, 15, 23, 40)
            elif back: cap = ell(8, 7, 35, 32) & rows_le(26 if ln != 'buzz' else 24)
            mass |= cap
        else:
            if back:
                mass |= ell(5, top, 38, 36) & rows_le(max(sl, 31))
                mass |= long_vol('back') if ln in ('shoulder', 'long', 'vlong') else blank()
            elif side:
                face = poly([(-2, 15), (14, 14), (20, 16), (23, 20), (24, 26), (26, 31), (28, 36), (-2, 44)])   # 앞머리선에서 귀 뒤로 둥글게
                mass |= ell(7, top, 39, 34) & rows_le(min(sl, 31) if ln != 'short' else 28) & ~face
                if ln in ('bob', 'shoulder', 'long', 'vlong'):   # 귀를 덮는 옆머리 (끝이 둥글게)
                    e = min(sl, 33)
                    mass |= poly([(17, 15), (27, 14), (30, e - 4), (28, e), (24, e - 1), (21, e - 3), (19, 22)])
                over |= long_vol('side')
                if ln == 'short' and 'slick' not in ex: pass
            else:
                mass |= ell(5, top, 38, 33) & rows_le(16)
                if ln in ('bob', 'shoulder', 'long', 'vlong'):
                    lk = min(sl, 34) if ln != 'bob' else 30
                    mass |= sym(poly([(5, 12), (10, 12), (11, lk - 4), (9, lk), (6, lk - 1)]))
                    under |= ell(4, top + 1, 39, min(sl, 34) + 4) & rows_le(min(sl, 34))
                    under |= long_vol('front')
                else:
                    mass |= sym(poly([(6, 12), (10, 12), (10, 22), (7, 21)]))          # 짧은 옆머리
        # ---- 꾸밈 ----
        if 'twin' in ex or 'twinlow' in ex:
            y0 = 12 if 'twin' in ex else 26
            t = sym(ell(0, y0, 8, y0 + 22) | ell(2, y0 - 2, 9, y0 + 4))
            if side: over |= ell(22, y0 - 2, 31, y0 + 24) | ell(23, y0 - 3, 29, y0 + 2)
            elif back: over |= t
            else: under |= t
        if 'pony' in ex:
            if side: over |= poly([(33, 8), (40, 9), (42, 22), (40, 38), (36, 42), (37, 26), (34, 16)])
            elif back: over |= ell(16, 6, 27, 46)
            else: under |= ell(30, 10, 41, 40) & ~ell(30, 30, 37, 46)
        if 'sidepony' in ex:
            if side: under |= ell(30, 14, 40, 42)
            elif back: over |= ell(2, 14, 12, 44)
            else: under |= ell(32, 14, 42, 44)
        if 'lowpony' in ex:
            if side: over |= poly([(30, 26), (36, 28), (38, 44), (33, 50), (31, 40)])
            elif back: over |= poly([(19, 30), (24, 30), (26, 46), (21, 52), (18, 44)])
            else: under |= poly([(30, 30), (36, 34), (38, 48), (33, 52), (31, 40)])
        if 'bun' in ex: over |= ell(24, -1, 35, 9) if side else ell(15, -1, 28, 9)
        if 'buns' in ex: over |= ell(17, 0, 28, 11) if side else sym(ell(5, 2, 15, 12))
        if 'starbun' in ex:
            cx = 27 if side else 21.5
            over |= poly([(cx, -1), (cx + 2.5, 4), (cx + 7.5, 4), (cx + 3.5, 7), (cx + 5.5, 12), (cx, 9), (cx - 5.5, 12), (cx - 3.5, 7), (cx - 7.5, 4), (cx - 2.5, 4)])
        if 'topknot' in ex: over |= ell(22, 0, 30, 7) if side else ell(17, 0, 26, 7)
        if 'braid' in ex:
            for k in range(6): over |= (ell(26, 28 + k * 4, 32, 33 + k * 4) if side else ell(30, 28 + k * 4, 36, 33 + k * 4))
        if 'braids' in ex:
            for k in range(6):
                if side: over |= ell(22, 30 + k * 4, 28, 35 + k * 4)
                elif back: over |= sym(ell(12, 30 + k * 4, 18, 35 + k * 4))
                else: over |= sym(ell(5, 30 + k * 4, 11, 35 + k * 4))
        if 'drill' in ex:
            for k in range(4):
                if side: over |= ell(22, 18 + k * 5, 30, 24 + k * 5)
                else: (over if back else under).__ior__(sym(ell(0, 18 + k * 5, 8, 24 + k * 5)))
        if 'afro' in ex:
            puff = ell(1, 0, 42, 36) if not side else ell(4, 0, 43, 36)
            if back or side: mass |= puff & ~(ell(0, 14, 22, 44) if side else blank())
            else: under |= puff; mass |= ell(5, 2, 38, 26) & rows_le(16)
        if 'curly' in ex:
            bumps = ((9, 9), (15, 6), (22, 5), (28, 6), (34, 9), (7, 15), (36, 15)) if not side else ((10, 9), (16, 5), (23, 4), (30, 6), (36, 10), (38, 17), (36, 24))
            for cx, cy in bumps: mass |= ell(cx - 4, cy - 4, cx + 4, cy + 4)
            if back:
                for cx, cy in ((8, 20), (35, 20), (14, 25), (29, 25), (21, 27)): mass |= ell(cx - 5, cy - 5, cx + 5, cy + 5)
        if 'wavy' in ex:
            w = blank()
            for k in range(5):
                if side: w |= ell(29 + (k % 2), 16 + k * 7, 38 + (k % 2), 25 + k * 7)
                else: w |= sym(ell(1 + (k % 2), 16 + k * 7, 9 + (k % 2), 25 + k * 7))
            (over if back or side else under).__ior__(w)
        if 'wild' in ex:
            if side: w = poly([(24, 12), (40, 10), (43, 24), (40, 26), (42, 40), (37, 38), (37, 48), (33, 42), (30, 48), (28, 40), (24, 36)])
            else: w = poly([(5, 14), (1, 28), (4, 30), (2, 42), (7, 40), (7, 50), (12, 44), (15, 50), (18, 43), (25, 43), (28, 50), (31, 44), (36, 50), (36, 40), (41, 42), (39, 30), (42, 28), (38, 14)])
            (over if back or side else under).__ior__(w)
            mass |= poly([(8, 8), (5, 3), (12, 6), (14, 1), (18, 5), (22, 0), (26, 5), (30, 1), (32, 6), (38, 3), (35, 9)]) if not side else poly([(10, 8), (12, 2), (17, 5), (21, 0), (25, 4), (30, 1), (33, 6), (39, 4), (37, 11)])
        if 'ahoge' in ex:
            for x, y in ((21, 4), (22, 3), (23, 2), (24, 2), (25, 3), (25, 4), (24, 5)): over[y, x - (4 if side else 0)] = True
        if 'spikes' in ex:
            mass |= poly([(7, 12), (3, 6), (10, 8), (11, 1), (16, 6), (20, -1), (23, 5), (28, 0), (30, 7), (37, 3), (35, 10), (40, 12), (34, 14), (9, 14)]) if not side else poly([(9, 12), (10, 4), (15, 7), (18, 0), (23, 5), (28, 1), (31, 7), (38, 4), (36, 11), (42, 14), (36, 18), (12, 14)])
        if 'mullet' in ex:
            if side: over |= poly([(28, 22), (36, 20), (38, 40), (34, 42), (30, 38), (28, 30)])
            elif back: mass |= rect(10, 20, 33, 40)
            else: under |= rect(10, 28, 33, 40) & ~rect(14, 28, 29, 34)
        if 'eyecover' in ex and view == 'front': mass |= poly([(20, 12), (34, 14), (34, 31), (30, 33), (27, 26), (22, 22)])
        if 'slick' in ex:
            mass |= (ell(7, 4, 36, 22) & rows_le(13)) if not side else (ell(8, 4, 38, 24) & rows_le(14))
        # ---- 칠하기 ----
        tgt = H.o
        if not back and not side: paint_mass(H.u, fr, under & ~mass, top, crown, view, dim=True)
        if side and under.any(): paint_mass(H.u, fr, under & ~mass, top, crown, view, dim=True)
        paint_mass(tgt, fr, over & ~mass, top, crown, view, back=back)
        tip_lines(tgt, fr, over & ~mass)
        paint_mass(tgt, fr, mass, top, crown, view, back=back)
        if back: tip_lines(tgt, fr, mass)
        if not back:
            locks = bang_locks(bangs, view) if not ('slick' in ex or 'mohawk' in ex or 'cornrow' in ex or ln == 'buzz') else []
            if locks:
                lm = paint_locks(tgt, fr, locks, top=top + 5)
                # 이마 그림자: 앞머리 끝 바로 아래 한 줄 (피부색)
                head = HEAD_S if side else HEAD_F
                shad = shift(lm, 1) & ~lm & head & ~(mass | over)
                H.sh.paint(fr, shad, K2)
        if 'cornrow' in ex:
            for k in range(4):
                if side: line(tgt, fr, [(10, 9 + k * 2), (22, 7 + k * 2), (34, 12 + k * 3)], K3, mask=mass)
                else:
                    for x in range(11, 33, 3):
                        for y in range(9, 17):
                            if mass[y, x]: tgt.put(fr, x, y, K3)
    for L in (H.o, H.u, H.sh): copy_all(L)
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
 ('상투', dict(bangs='none', len='short', ex=['topknot', 'slick'])),
 ('복슬복슬', dict(bangs='messy', len='bob', ex=['curly'])),
 ('옆으로 넘김', dict(bangs='swept', len='short')),
 ('옆 포니테일', dict(bangs='swept_r', len='short', ex=['sidepony'])),
 ('바닥까지 긴 머리', dict(bangs='blunt', len='vlong')),
 ('바가지', dict(bangs='hime', len='short')),
 ('경단 머리', dict(bangs='center', len='short', ex=['buns', 'ahoge'])),
 ('콘로우', dict(bangs='none', len='buzz', ex=['cornrow'])),
 ('더듬이', dict(bangs='blunt', len='bob', ex=['ahoge'])),
 ('한쪽 눈 가림', dict(bangs='eye', len='shoulder', ex=['eyecover'])),
 ('낮은 포니테일', dict(bangs='center', len='short', ex=['lowpony'])),
 ('마녀 장발', dict(bangs='messy', len='long', ex=['wild'])),
 ('단정 앞머리', dict(bangs='hime', len='bob')),
 ('별 똥머리', dict(bangs='swept', len='short', ex=['starbun'])),
]

# ================= 교복 =================
UNIS = ['춘추복', '하복', '동복', '체육복', '생활복']
GOLD, ORANGE, SHIRT2 = hexc('#F0C850'), hexc('#E8902A'), hexc('#D8D4E4')
def make_uni(k):
    cloth, house, shoes = Lay(), Lay(), Lay()
    # ---- 앞·뒤 ----
    for fr in (FRONT, BACK):
        back = fr == BACK
        torso = poly([(15, 35), (28, 35), (30, 47), (13, 47)])
        slv = sym(poly([(16, 36), (12, 37), (10, 43), (14, 44), (16, 39)]))
        pants = sym(rect(15, 46, 21, 54)) | rect(15, 46, 28, 48)
        sh = sym(ell(14, 53, 21, 58) | rect(15, 54, 21, 57))
        if k == 0:
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K2, K3, light=K1)
            if not back:
                cloth.paint(fr, poly([(18, 35), (25, 35), (21.5, 42)]), WHITE)
                house.paint(fr, rect(21, 37, 22, 43) | rect(20, 36, 23, 37), K1); house.put(fr, 21, 44, K2); house.put(fr, 22, 44, K2)
                cloth.put(fr, 18, 43, GOLD); cloth.put(fr, 18, 45, GOLD)
                cloth.paint(fr, sym(poly([(17, 35), (19, 35), (21, 41), (19, 40)])), K3)
            else: house.paint(fr, rect(14, 46, 29, 46), K1)
            house.paint(fr, sym(rect(10, 42, 13, 42)), K1)
        elif k == 1:
            shade(cloth, fr, pants, K1, K2); shade(cloth, fr, torso, K2, K3, light=K1)
            cloth.paint(fr, sym(poly([(16, 36), (12, 37), (12, 40), (16, 39)])), WHITE); cloth.paint(fr, sym(rect(12, 40, 14, 40)), SHIRT2)
            if not back:
                cloth.paint(fr, poly([(17, 35), (26, 35), (21.5, 41)]), WHITE)
                house.paint(fr, poly([(17, 36), (18, 36), (21.5, 41), (25, 36), (26, 36), (21.5, 43)]), K1)
            house.paint(fr, rect(13, 46, 30, 46), K1)
        elif k == 2:
            coat = poly([(15, 35), (28, 35), (31, 52), (12, 52)]); shade(cloth, fr, sym(rect(15, 51, 21, 54)), K3, K3)
            shade(cloth, fr, coat | sym(poly([(16, 36), (11, 37), (9, 44), (14, 45), (16, 39)])), K1, K2, light=K0)
            if not back:
                cloth.paint(fr, rect(21, 38, 22, 52), K2)
                for y in (40, 44, 48): cloth.put(fr, 19, y, ORANGE); cloth.put(fr, 24, y, ORANGE)
            sc = poly([(14, 33), (29, 33), (30, 37), (13, 37)]); shade(house, fr, sc, K1, K2)
            for x in range(14, 30, 4): house.paint(fr, rect(x, 33, x + 1, 37) & sc, K0)
            if not back: shade(house, fr, rect(24, 37, 27, 43), K1, K2); house.paint(fr, rect(24, 43, 27, 43), K0)
        elif k == 3:
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K1, K2)
            house.paint(fr, sym(poly([(12, 37), (13, 37), (11, 43), (10, 43)])) | sym(rect(15, 47, 15, 54)), K1)
            if not back: cloth.paint(fr, rect(21, 35, 22, 47), K2); cloth.put(fr, 21, 36, K0)
            else: house.paint(fr, rect(21, 36, 22, 46), K1)
            cloth.paint(fr, rect(16, 34, 27, 35), K2)
        elif k == 4:
            shade(cloth, fr, pants, K2, K3); shade(cloth, fr, torso | slv, K1, K2, light=K0)
            cloth.paint(fr, sym(rect(15, 53, 21, 54)), K3)
            if not back:
                cloth.paint(fr, rect(16, 42, 27, 42), K2); cloth.paint(fr, rect(16, 43, 16, 45) | rect(27, 43, 27, 45), K2)
                house.paint(fr, ell(19, 37, 24, 41), K1); house.put(fr, 21, 39, K0); house.put(fr, 22, 39, K0)
                for x, y in ((19, 35), (19, 36), (24, 35), (24, 36)): cloth.put(fr, x, y, WHITE)
            else: shade(cloth, fr, ell(15, 31, 28, 40), K1, K2); house.paint(fr, ell(19, 40, 24, 44), K1)
        shade(shoes, fr, sh, K1, K2); shoes.paint(fr, sh & ~shift(sh, -1), WHITE if k == 3 else K3)
        if k in (0, 2): shoes.paint(fr, sh & ~shift(sh, 1), K0)
    walkify(cloth); walkify(house); walkify(shoes)
    # ---- 옆 (왼쪽 보기) ----
    for j in range(3):
        S = pose_side(j); fr = SIDE + j
        torso = S['torso'] | poly([(16, 35), (27, 35), (28, 47), (15, 47)])
        slv = S['arm'] & rows_le(44 if k != 1 else 39)
        legF = S['legF'] & rows_le(54); legB = S['legB'] & rows_le(54)
        def shoe(fx): return ell(fx - 3, 53, fx + 3, 58) | rect(fx - 1, 54, fx + 3, 57)
        shB, shF = shoe(S['footB']), shoe(S['footF'])
        pb, pf = (K3, K2) if k != 1 else (K2, K1)
        if k == 2: legF |= rect(15, 46, 28, 52) & torso; legB = legB
        shade(cloth, fr, legB, pb, K3); shade(cloth, fr, legF | (rect(15, 46, 27, 48)), pf, K3)
        if k == 2:
            coat = poly([(16, 35), (27, 35), (29, 52), (14, 52)]); shade(cloth, fr, coat, K1, K2, light=K0)
            for y in (40, 44, 48): cloth.put(fr, 15, y, ORANGE)
            sc = poly([(15, 33), (28, 33), (28, 37), (15, 37)]); shade(house, fr, sc, K1, K2)
            for x in range(15, 29, 4): house.paint(fr, rect(x, 33, x + 1, 37) & sc, K0)
            shade(house, fr, rect(13, 36, 16, 43), K1, K2)
            shade(cloth, fr, slv | (S['arm'] & rows_le(45)), K1, K2, light=K0)
        else:
            tb = {0: K2, 1: K2, 3: K1, 4: K1}[k]
            shade(cloth, fr, torso, tb, K3 if tb == K2 else K2, light=K1 if tb == K2 else K0)
            if k == 0:
                cloth.paint(fr, poly([(16, 35), (19, 35), (16, 41)]), WHITE); house.paint(fr, rect(16, 37, 17, 43), K1)
                cloth.put(fr, 17, 44, GOLD)
            if k == 1:
                cloth.paint(fr, poly([(16, 35), (18, 35), (16, 39)]), WHITE); house.paint(fr, rect(15, 46, 28, 46), K1)
                cloth.paint(fr, S['arm'] & rows_le(39), WHITE)
            if k == 3:
                house.paint(fr, line_mask([(21, 47), (S['footF'] + 1, 54)]) | line_mask([(25, 36), (27, 46)]), K1)
                cloth.paint(fr, rect(16, 34, 24, 35), K2)
            if k == 4:
                shade(cloth, fr, ell(22, 31, 30, 40), K1, K2)          # 후드
                cloth.put(fr, 17, 36, WHITE); cloth.put(fr, 17, 37, WHITE)
                cloth.paint(fr, rect(16, 42, 24, 42), K2)
            if k != 1: shade(cloth, fr, slv, tb if k != 0 else K2, K3 if k == 0 else K2, light=K1)
            if k == 0: house.paint(fr, slv & ~shift(slv, -1), K1)
            if k == 3: house.paint(fr, line_mask([(21, 37), (S['hand'].nonzero()[1].mean(), 44)]) & slv, K1)
        for shm in (shB, shF):
            shade(shoes, fr, shm, K1 if shm is shF else K2, K2 if shm is shF else K3); shoes.paint(fr, shm & ~shift(shm, -1), WHITE if k == 3 else K3)
    return dict(cloth=cloth, house=house, shoes=shoes)
def line_mask(pts):
    im = Image.new('1', (FW, FH)); ImageDraw.Draw(im).line([(float(x), float(y)) for x, y in pts], fill=1, width=1); return np.array(im)

# ================= 프레임 =================
LEGTOP = 47
def copy_all(L):
    for b in (FRONT, BACK, SIDE):
        for k in (1, 2): L.f[b + k] = L.f[b].copy()
def copy_side(L):
    copy_all(L)
def walkify(L):
    """앞·뒤: 한쪽 다리를 2칸 들어요"""
    for b in (FRONT, BACK):
        src = L.f[b]
        for k, side in ((1, 'L'), (2, 'R')):
            dst = src.copy()
            leg = np.zeros((FH, FW), bool); leg[LEGTOP:, :22] = side == 'L'; leg[LEGTOP:, 22:] = side == 'R'
            m = leg & (src[..., 3] > 0); dst[m] = 0; ys, xs = np.nonzero(m); dst[ys - 2, xs] = src[ys, xs]
            L.f[b + k] = dst
def only(L, views):
    for b in (FRONT, BACK, SIDE):
        if b not in views:
            for k in range(3): L.f[b + k][:] = 0
    return L
rows, Z = [], ['hairU', 'skin', 'cloth', 'head', 'face', 'hairO']
def row_of(L):
    im = np.zeros((FH, FW * NF, 4), np.uint8)
    for i in range(NF): im[:, i * FW:(i + 1) * FW] = L.f[i]
    rows.append(im); return len(rows) - 1
body = make_body(); walkify(body)
head = make_head()
blush = make_blush(); copy_all(blush); only(blush, (FRONT, SIDE))
base = [[row_of(body), 'skin', 'skin'], [row_of(head), 'skin', 'head'], [row_of(blush), None, 'face']]
parts = dict(hair=[], eyes=[], mouth=[], uni=[])
for n, spec in HAIRS:
    H = make_hair(spec)
    Ls = [[row_of(H.o), 'hair', 'hairO']]
    if not H.u.empty(): Ls.append([row_of(H.u), 'hair', 'hairU'])
    if not H.sh.empty(): Ls.append([row_of(H.sh), 'skin', 'face'])
    parts['hair'].append(dict(n=n, L=Ls))
for i, (n, _) in enumerate(EYES):
    e = only(make_eye(i), (FRONT, SIDE)); b = only(make_brows(i), (FRONT, SIDE))
    parts['eyes'].append(dict(n=n, L=[[row_of(e), 'eye', 'face'], [row_of(b), 'hair', 'face']]))
for i, (n, _) in enumerate(MOUTHS):
    parts['mouth'].append(dict(n=n, L=[[row_of(only(make_mouth(i), (FRONT, SIDE))), None, 'face']]))
for k, n in enumerate(UNIS):
    U = make_uni(k)
    parts['uni'].append(dict(n=n, L=[[row_of(U['cloth']), 'cloth', 'cloth'], [row_of(U['house']), 'house', 'cloth'], [row_of(U['shoes']), 'shoes', 'cloth']]))
import os; os.makedirs('out', exist_ok=True)
Image.fromarray(np.concatenate(rows, axis=0), 'RGBA').save('out/avatar_parts.png')
# ================= 팔레트 =================
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
meta = dict(fw=FW, fh=FH, frames=NF, src='art/iso/avatar_parts.png', z=Z, base=base, parts=parts, outline=True,
            stops={k: STOP for k in ('skin', 'eye', 'hair', 'cloth', 'shoes', 'house')},
            pal=dict(skin=SKIN, eye=EYE, hair=HAIR, shoes=SHOES, cloth=CLOTH, house=HOUSE), head=dict(t=4, b=40))
json.dump(meta, open('out/avatar_parts.json', 'w'), ensure_ascii=False)
print('rows', len(rows), {k: len(v) for k, v in parts.items()})
