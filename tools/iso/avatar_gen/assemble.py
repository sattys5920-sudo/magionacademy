# 생성 그림(이미지 생성기로 뽑은 시트) → 아바타 부품 (게임 형식: 한 줄 = 한 층의 9프레임, 회색은 고른 색으로 칠해요)
# 프레임: 0~2 앞(서기·걷기A·걷기B), 3~5 뒤, 6~8 옆(왼쪽 보기)
# 칸 그림은 cells.npz (extract.py가 생성 이미지 시트에서 뽑아요). python3 assemble.py → ../out/avatar_parts.png + .json
import json, os, numpy as np
from PIL import Image
from scipy import ndimage
from reduce import reduce
from picks import FRONT, BACK, SIDE
import face
HERE = os.path.dirname(os.path.abspath(__file__))
_Z = np.load(os.path.join(HERE, 'cells.npz')); D = {}
for key in _Z.files:
    n, i = key.split('/'); D.setdefault(n, {})[int(i)] = dict(rgb=_Z[key])
D = {n: [v[i] for i in sorted(v)] for n, v in D.items()}
FW, FH, NF = 36, 58, 9
SKIN_T, HAIR_T = 205, 140   # 피부·머리카락 중간 밝기
CHIN = 28            # 모든 머리의 턱 줄 (프레임 안 y)
NECKX = FW // 2      # 목 가운데 x

# ---------- 픽셀 종류 ----------
def kinds(rgb):
    r, g, b = [rgb[..., i].astype(int) for i in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    lum = (r * 3 + g * 6 + b) / 10
    bg = (g > r + 45) & (g > b + 45)
    skin = ~bg & (r > 140) & (r > g + 12) & (g > b) & (r - b > 35)
    gray = ~bg & ~skin & (mx - mn < 26)
    mag = ~bg & (r > 110) & (b > 90) & (g < .6 * np.minimum(r, b))
    return dict(bg=bg, skin=skin, gray=gray, mag=mag, lum=lum)
def rgba_of(rgb):
    k = kinds(rgb); a = np.zeros(rgb.shape[:2] + (4,), np.uint8); a[..., :3] = rgb; a[..., 3] = np.where(k['bg'], 0, 255); return a
def keep_main(a):
    """가장 큰 덩어리와 그 근처만 남겨요 (옆 칸에서 묻어온 점 지우기)"""
    m = a[..., 3] > 0; lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n <= 1: return a
    sizes = ndimage.sum(m, lab, range(1, n + 1)); big = np.argmax(sizes) + 1
    keep = lab == big
    for i in range(1, n + 1):
        if i != big and sizes[i - 1] >= 6 and ndimage.binary_dilation(keep, iterations=2)[lab == i].any(): keep |= lab == i
    a = a.copy(); a[~keep, 3] = 0; return a
def split_wide(cells):
    """두 그림이 붙은 칸은 반으로"""
    med = np.median([c['rgb'].shape[1] for c in cells]); out = []
    for c in cells:
        a = c['rgb']
        if a.shape[1] > 1.6 * med:
            k = kinds(a)['bg']; col = k.mean(0); mid = a.shape[1] // 2; rng = range(int(mid * .6), int(mid * 1.4))
            x = max(rng, key=lambda i: col[i]); out += [dict(rgb=a[:, :x]), dict(rgb=a[:, x:])]
        else: out.append(c)
    return out
def split_tall(a):
    """위아래로 붙은 두 그림 → [위, 아래]"""
    k = kinds(a)['bg']; row = k.mean(1); mid = a.shape[0] // 2; rng = range(int(mid * .7), int(mid * 1.3))
    y = max(rng, key=lambda i: row[i]); return a[:y], a[y:]
# ---------- 머리 기준점: 턱 줄과 목 가운데 ----------
def chin_neck(a):
    k = kinds(a[..., :3]); sk = k['skin'] & (a[..., 3] > 0)
    w = sk.sum(1); ys = np.nonzero(w)[0]
    if not len(ys): return None
    top = ys.min(); ymax = top + int(np.argmax(w[top:top + 22])); wm = w[ymax]; chin = None
    for y in range(ymax, a.shape[0]):
        if w[y] < .55 * wm: chin = y - 1; break
    if chin is None: chin = ys.max()
    # 목: 턱 바로 아래 피부 칸들의 가운데 (없으면 얼굴 가운데)
    for y in (chin + 2, chin + 1, chin):
        xs = np.nonzero(sk[min(y, a.shape[0] - 1)])[0]
        if len(xs) and (y > chin or True): return chin, (xs.min() + xs.max()) / 2
    return chin, a.shape[1] / 2
# ---------- 피부 띠 지우기 (생성 그림의 빈 눈 자리) ----------
def fix_band(a):
    a = a.copy(); k = kinds(a[..., :3]); sk = k['skin'] & (a[..., 3] > 0)
    if not sk.any(): return a
    r, g = a[..., 0].astype(int), a[..., 1].astype(int)
    base = np.median(a[sk & (r - g < 55)][:, :3], 0) if (sk & (r - g < 55)).any() else None
    if base is None: return a
    band = sk & (r - g >= 55)
    # 띠는 얼굴 가운데 가로줄: 가장자리 음영(테두리 옆)은 남겨요
    edge = ndimage.binary_dilation(~sk & (a[..., 3] > 0), iterations=1)
    a[band & ~edge, :3] = base.astype(np.uint8); return a
# ---------- 층 그리기 판 ----------
class Lay:
    def __init__(self): self.f = np.zeros((NF, FH, FW, 4), np.uint8)
    def paste(self, fr, a, ox, oy, mask=None):
        h, w = a.shape[:2]
        for y in range(h):
            yy = y + oy
            if not 0 <= yy < FH: continue
            for x in range(w):
                xx = x + ox
                if 0 <= xx < FW and a[y, x, 3] and (mask is None or mask[y, x]): self.f[fr, yy, xx] = a[y, x]
    def row(self): return np.concatenate(list(self.f), axis=1)
def to_gray(a, m, target=None):
    """칠할 층: 밝기만 남긴 회색 (게임이 고른 색으로 칠해요). target: 중간 밝기를 이 값에 맞춰요 (시트마다 다른 밝기 고르기)"""
    o = np.zeros_like(a); k = kinds(a[..., :3]); L = k['lum'].copy()
    mm = m & (a[..., 3] > 0) & (L > 40)
    if target is not None and mm.any(): L = np.where(L > 40, L + (target - np.median(L[mm])), L)
    L = np.clip(L, 0, 255).astype(np.uint8)
    o[..., 0] = o[..., 1] = o[..., 2] = L; o[..., 3] = np.where(m & (a[..., 3] > 0), 255, 0); return o
def keep_color(a, m):
    o = a.copy(); o[..., 3] = np.where(m & (a[..., 3] > 0), 255, 0)
    gr = (o[..., 0] == o[..., 1]) & (o[..., 1] == o[..., 2]) & (o[..., 3] > 0)
    o[gr, 2] = np.where(o[gr, 2] > 250, o[gr, 2] - 3, o[gr, 2] + 3)   # 회색이면 게임이 칠해 버려서 살짝 비틀어요
    return o
def outline_of(a):
    k = kinds(a[..., :3]); r, g, b = [a[..., i].astype(int) for i in range(3)]
    return (a[..., 3] > 0) & (k['lum'] < 75) & ~k['gray'] | ((a[..., 3] > 0) & (k['lum'] < 45))
# ---------- 걷기: 다리 한쪽을 1px 올려요 ----------
def walk(fr_a, legtop, which):
    o = fr_a.copy(); h = o.shape[0]; mid = FW // 2
    side = slice(0, mid) if which == 0 else slice(mid, FW)
    o[legtop:h - 1, side] = fr_a[legtop + 1:h, side]; o[h - 1, side] = 0
    return o
# ---------- 교복(몸) ----------
UNI = [  # (이름, 앞, 뒤, 옆) 칸: (시트, 번호, 위/아래 반쪽)
    ('춘추복', ('u2', 8, None), ('u2', 11, 0), ('u2', 12, 0)),
    ('하복', ('u4', 0, None), ('u4', 10, None), ('u4', 17, None)),
    ('동복', ('u5', 0, None), ('u5', 10, None), ('u5', 17, None)),
    ('체육복', ('u3', 0, None), ('u3', 7, None), ('u3', 11, None)),
    ('생활복', ('u1', 0, None), ('u1', 10, None), ('u1', 17, None)),
]
SIDE_FLIP = {}   # 옆모습이 오른쪽을 보면 뒤집어요 (아래에서 귀 위치로 판단)
def cell(src):
    s, i, half = src; a = D[s][i]['rgb']
    if half is not None: a = split_tall(a)[half]
    a = keep_main(rgba_of(a))
    ys, xs = np.nonzero(a[..., 3]); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return a
def faces_right(a):
    """옆모습 머리의 귀가 왼쪽에 있으면 얼굴은 오른쪽을 봐요"""
    k = kinds(a[..., :3]); sk = k['skin'] & (a[..., 3] > 0); ch = chin_neck(a)[0]
    head = sk[:ch]; xs = np.nonzero(head)[1]
    if not len(xs): return False
    cx = (xs.min() + xs.max()) / 2
    dark_in = outline_of(a)[:ch] & ndimage.binary_erosion(ndimage.binary_fill_holes(a[:ch, :, 3] > 0), iterations=2)
    ys2, xs2 = np.nonzero(dark_in)
    return len(xs2) > 0 and xs2.mean() < cx
def body_layers():
    out = []
    for name, *views in UNI:
        L = dict(cloth=Lay(), house=Lay(), shoes=Lay(), skin=Lay())
        for vi, src in enumerate(views):
            a = cell(src)
            if a.shape[0] > 43: o, b, _ = reduce(a[..., :3], 41 / a.shape[0], bg_th=.5); a = np.dstack([o, np.where(b, 0, 255).astype(np.uint8)])
            if vi == 2 and faces_right(a): a = a[:, ::-1]
            ch, nx = chin_neck(a); body = a.copy(); body[:ch + 1, :, 3] = 0           # 머리는 버리고 목부터
            k = kinds(body[..., :3]); h = body.shape[0]
            ox, oy = int(round(NECKX - nx)), CHIN - ch
            feet = np.zeros(body.shape[:2], bool); feet[h - 3:] = True
            masks = dict(skin=k['skin'], house=k['mag'], shoes=k['gray'] & feet, cloth=~k['skin'] & ~k['mag'] & ~(k['gray'] & feet))
            # 다리 시작: 가운데 줄이 처음으로 비는 곳 (옆모습은 아래 6줄)
            col = body[:, int(round(nx)), 3] == 0; legtop = h - 6
            for y in range(h - 1, ch, -1):
                if col[y]: legtop = y
                else: break
            for kk, m in masks.items():
                lay = to_gray(body, m, SKIN_T if kk == 'skin' else None) if kk != 'cloth' else None
                if kk == 'cloth':   # 옷: 회색은 칠하고, 테두리·색 있는 점은 그대로
                    g = to_gray(body, m & k['gray']); c = keep_color(body, m & ~k['gray']); lay = np.where(c[..., 3:] > 0, c, g)
                fr0 = np.zeros((FH, FW, 4), np.uint8); tmp = Lay(); tmp.paste(0, lay, ox, oy); fr0 = tmp.f[0]
                lt = legtop + oy
                for j, fr in enumerate((fr0, walk(fr0, lt, 0), walk(fr0, lt, 1))): L[kk].f[vi * 3 + j] = fr
        out.append((name, L))
    return out
# ---------- 머리 ----------
def head_cell(src, reduce_f=None, flip=False, band=False):
    s, i = src; a = D[s][i]['rgb']
    if reduce_f: o, b, _ = reduce(a, reduce_f); a = np.dstack([o, np.where(b, 0, 255).astype(np.uint8)])
    else: a = rgba_of(a)
    a = keep_main(a)
    if flip: a = a[:, ::-1]
    if band: a = fix_band(a)
    return a
def synth_back(a):
    """앞모습으로 뒷모습 만들기: 턱 위 얼굴(피부)을 머리카락으로 채워요"""
    a = a.copy(); ch, nx = chin_neck(a); k = kinds(a[..., :3]); sk = k['skin'] & (a[..., 3] > 0)
    hair = k['gray'] & (a[..., 3] > 0); hl = k['lum'][hair]
    if not len(hl): return a
    lo, mid, hi = np.percentile(hl, 20), np.percentile(hl, 50), np.percentile(hl, 85)
    face = sk.copy(); face[ch + 1:] = False
    ys, xs = np.nonzero(face)
    # 턱 아래: 양옆에 머리카락이 있는 줄의 피부·어두운 안쪽은 머리카락으로 (긴 머리는 목을 덮어요)
    for y in range(ch + 1, a.shape[0]):
        row = hair[y]; hx = np.nonzero(row)[0]
        if len(hx) >= 2 and hx.min() < nx - 3 and hx.max() > nx + 3:
            seg = np.zeros_like(row); seg[hx.min():hx.max() + 1] = True
            face[y] |= seg & (a[y, :, 3] > 0) & ~outline_of(a)[y]
            face[y] |= seg & hair[y] & (k['lum'][y] < mid)
    # 안쪽 테두리(앞머리 선)도 머리카락으로
    inner = outline_of(a) & ndimage.binary_erosion(a[..., 3] > 0, iterations=2); inner[ch - 1:] = False
    fill = face | inner
    for y, x in zip(*np.nonzero(fill)):
        if y <= ch: t = min(1, max(0, (y - ys.min()) / max(1, ch - ys.min()))) if len(ys) else .5; v = hi - (hi - mid) * t
        else: v = mid - (mid - lo) * .35 * min(1, (y - ch) / 12)   # 턱 아래 늘어진 머리: 중간 밝기
        if (x + y // 3) % 4 == 0: v = (v + lo) / 2      # 머리카락 결
        a[y, x, :3] = int(np.clip(v, 0, 255))
    return a
def place_head(lay, fr, a, chin=None, nx=None):
    if chin is None: chin, nx = chin_neck(a)
    lay.paste(fr, a, int(round(NECKX - nx)), CHIN - chin)
    return int(round(NECKX - nx)), CHIN - chin
def hair_layers(n):
    O, U, S = Lay(), Lay(), Lay()
    views = []
    f = head_cell(FRONT[n]); views.append(f)
    b = head_cell(BACK[n]) if n in BACK and n not in (20, 28, 29) else synth_back(f); views.append(b)
    # 옆 시트는 오른쪽을 봐요 → 뒤집어 왼쪽으로. 7번은 원래 왼쪽을 봐요.
    # 8번 옆모습은 거의 뒷모습이라 얼굴이 안 보여서, 3/4로 돌아간 앞모습 칸을 뒤집어 써요
    if n == 7: s = head_cell(FRONT[n])[:, ::-1]
    else:
        s = head_cell(SIDE[n], reduce_f=.55, band=True)
        if n not in SIDE_KEEP: s = s[:, ::-1]
    views.append(s)
    fch, fnx = chin_neck(f); fys, fxs = np.nonzero(f[..., 3]); ftop = fys.min()
    for vi, a in enumerate(views):
        cn = chin_neck(a) if vi != 1 or not (n in BACK and n not in (20, 28, 29)) else None
        if cn is None:   # 뒷모습(피부가 안 보임): 앞모습의 머리 위→턱 높이, 가로는 가운데
            ys, xs = np.nonzero(a[..., 3]); cn = (ys.min() + (fch - ftop), (xs.min() + xs.max()) / 2)
        ch, nx = cn; k = kinds(a[..., :3])
        if vi == 2: nx += SIDE_SHIFT.get(n, 0)   # 옆얼굴 위치 맞추기
        head = a.copy(); head[ch + 2:, :, 3] = 0                   # 목은 몸 것을 써요
        skin_m = k['skin']; hair_m = ~k['skin']
        under = np.zeros(a.shape[:2], bool); under[ch + 1:] = True    # 턱 아래 머리카락은 몸 뒤로 (앞모습만)
        sk = to_gray(head, skin_m, SKIN_T)
        hg = to_gray(a, hair_m & k['gray'], HAIR_T); hl = np.where(hg[..., 3:] > 0, hg, keep_color(a, hair_m & ~k['gray']))
        hO, hU = hl.copy(), hl.copy()
        if vi == 0: hO[under, 3] = 0; hU[~under, 3] = 0
        else: hU[..., 3] = 0
        for j in range(3):
            fr = vi * 3 + j
            place_head(S, fr, sk, ch, nx); place_head(O, fr, hO, ch, nx); place_head(U, fr, hU, ch, nx)
    return O, U, S
# ---------- 눈·입 (앞 얼굴 기준) ----------
SIDE_SHIFT = {9: 4, 7: 1, 33: 1, 3: 2, 25: 2, 26: 2, 38: 2, 36: 2, 0: 1}   # 옆얼굴 위치 맞추기 (눈이 얼굴 밖으로 나가지 않게)
SIDE_KEEP = {6}            # 이미 왼쪽을 보는 옆모습 (7번)
SIDE_DX, SIDE_IN = -2, 1   # 옆모습 눈: 왼쪽으로 옮김, 먼 눈은 안쪽으로
# ---------- 눈·코·입: 선명한 픽셀로, 생성 그림 얼굴 비율에 맞춰 같은 자리에 ----------
# 얼굴 기준(앞모습): 가운데 x = NECKX, 턱 = CHIN. 눈은 턱 위 8~5줄, 코는 4줄 위 1점, 입은 3~1줄 위
# 비율 기준 = 생성 그림 얼굴의 빈 눈 자리(연한 띠)와 입 위치
# 글자: L 속눈썹·선(자주) · D/I/J 눈동자 어둠/중간/밝음 (고른 눈 색) · W 흰 반짝 · P 동공 · K 하트 분홍 · T 눈물 · V 뱀파이어 빨강
# 왼쪽 눈(첫 칸이 바깥쪽), 오른쪽 눈은 좌우로 뒤집어요
EYE_PIX = [
    ['LLL', 'WDD', 'DDI', 'DIJ'],          # 반짝 동글
    ['LLLL', '.WDD', '.DDI', '.DIJ'],      # 큰 애니 (바깥 속눈썹)
    ['...', 'LLL', 'DDI', '.I.'],          # 졸린 눈
    ['...', '.L.', 'L.L', '...'],          # 웃는 눈 ^ ^
    ['LLL', 'JPJ', 'IPI', '.I.'],          # 고양이 눈
    ['LLL', 'DWD', 'WWW', 'DWD'],          # 별 눈동자
    ['LLL', 'KDK', 'KKK', '.K.'],          # 하트 눈동자
    ['LLL', 'WDD', 'DDI', 'DIJ'],          # 윙크 (오른쪽은 감은 눈)
    ['LL.', '.LL', 'DDI', 'DIJ'],          # 단호한 눈
    ['LLL', 'WDD', 'DDI', 'TTT'],          # 눈물 그렁
    ['LLL', '..L', 'L.L', 'LLL'],          # 빙글빙글
    ['...', '.L.', '.L.', '...'],          # 점 눈
    ['LL.', '.LL', 'VVP', 'VVV'],          # 뱀파이어 눈
    ['LLLL', '.WDW', '.DDI', '.WIJ'],      # 순정 반짝
    ['...', 'L..', '.LL', 'L..'],          # 질끈 감은 눈 > <
]
EYE_WINK_R = ['...', '.L.', 'L.L', '...']
# 입 (가운데 정렬, 홀수 너비): M 선 · R 입속 · N 혀 · W 이
MOUTH_PIX = [
    ['M.M', '.M.'],                        # 미소
    ['M.M.M', '.M.M.'],                    # 고양이 입
    ['.M.', 'M.M'],                        # 시무룩
    ['MMM', 'W.W'],                        # 송곳니 미소
    ['MMM', '.R.'],                        # 활짝 웃음
    ['MM', 'MM'],                          # 놀란 입 (작은 o)
    ['MMM', '.N.'],                        # 메롱
    ['MMM'],                               # 일자 입
    ['MMMMM', 'MWWWM'],                    # 이 드러낸 웃음
    ['.M.M.', 'M.M.M'],                    # 울먹
]
FACE_COL = dict(L=(42, 24, 48, 255), D=(70, 70, 70, 255), I=(145, 145, 145, 255), J=(205, 205, 205, 255), W=(255, 255, 250, 255),
                P=(24, 12, 30, 255), K=(255, 118, 160, 255), T=(160, 214, 255, 255), V=(206, 40, 64, 255),
                M=(120, 46, 66, 255), R=(196, 64, 86, 255), N=(244, 130, 156, 255))
EYE_ROW = CHIN - 7          # 눈 맨 윗줄 (앞머리에 가리지 않게)
EYE_IN = 2                  # 눈 안쪽 끝이 가운데에서 떨어진 칸 (두 눈 사이 = 2*EYE_IN - 1)
MOUTH_ROW = CHIN - 2
NOSE = (0, CHIN - 3)        # 가운데에서 x, y
def pix(rows):
    h, w = len(rows), max(len(r) for r in rows); a = np.zeros((h, w, 4), np.uint8)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': a[y, x] = FACE_COL[ch]
    return a
def eye_layers(i, cells=None):
    """눈: 생성 시트(face.py)에서 뽑아 게임 얼굴 크기로"""
    E, B = Lay(), Lay()
    for side, base in ((False, 0), (True, 6)):
        for g, x, y in face.eyes(i, side, NECKX, CHIN):
            for j in range(3): E.paste(base + j, g, x, y)
    return E, B
def mouth_layer(i):
    M = Lay()
    for side, base in ((False, 0), (True, 6)):
        for g, x, y in face.mouth(i, side, NECKX, CHIN):
            for j in range(3): M.paste(base + j, g, x, y)
    return M
def nose_layer():
    N = Lay(); n = np.array([[[0, 0, 0, 0]]], np.uint8); n[0, 0] = (186, 186, 186, 255)   # 피부색으로 칠해지는 옅은 그림자 (코)
    for j in range(3): N.paste(j, n, NECKX + NOSE[0], NOSE[1]); N.paste(6 + j, n, NECKX + NOSE[0] + SIDE_DX - 1, NOSE[1])
    return N

HAIR_N = ['단발', '긴 생머리', '높은 양갈래', '올림머리', '짧은 머리', '삐죽 짧은 머리', '소년 만화', '높은 포니테일', '아프로', '옆 땋은 머리',
          '히메컷', '울프컷', '까까머리', '부스스', '옆 가르마', '낮은 양갈래', '양쪽 똥머리', '긴 웨이브', '멀릿', '커튼 앞머리',
          '모히칸', '두 갈래 땋기', '반묶음', '드릴 컬', '짧은 곱슬', '올백', '정수리 묶음', '복슬 짧은 머리', '옆으로 넘김', '옆 포니테일',
          '바닥까지 긴 머리', '바가지 머리', '양쪽 경단', '콘로', '더듬이와 경단', '한쪽 눈 가림', '낮은 옆 포니테일', '마녀 산발', '단정한 앞머리', '별 모양 경단']
EYE_N = ['반짝 동글', '큰 애니', '졸린 눈', '웃는 눈', '고양이 눈', '별 눈동자', '하트 눈동자', '윙크', '단호한 눈', '눈물 그렁', '빙글빙글', '점 눈', '뱀파이어 눈', '순정 반짝', '질끈 감은 눈']
MOUTH_N = ['미소', '고양이 입', '시무룩', '송곳니 미소', '활짝 웃음', '놀란 입', '메롱', '일자 입', '이 드러낸 웃음', '울먹']
if __name__ == '__main__':
    rows, parts = [], dict(hair=[], eyes=[], mouth=[], uni=[])
    def add(lay): rows.append(lay.row()); return len(rows) - 1
    for name, L in body_layers():
        parts['uni'].append(dict(n=name, L=[[add(L['skin']), 'skin', 'skin'], [add(L['cloth']), 'cloth', 'cloth'], [add(L['house']), 'house', 'cloth'], [add(L['shoes']), 'shoes', 'cloth']]))
    for n in range(40):
        O, U, S = hair_layers(n)
        parts['hair'].append(dict(n=HAIR_N[n], L=[[add(O), 'hair', 'hairO'], [add(U), 'hair', 'hairU'], [add(S), 'skin', 'head']]))
    for i in range(15):
        E, B = eye_layers(i); parts['eyes'].append(dict(n=EYE_N[i], L=[[add(E), 'eye', 'face'], [add(B), None, 'face']]))
    for i in range(10): parts['mouth'].append(dict(n=MOUTH_N[i], L=[[add(mouth_layer(i)), None, 'face']]))
    nose_row = add(nose_layer())
    # 발이 그림 아래 끝에 닿게: 교복 층에서 가장 아래 줄을 찾아 전부 내려요 (위가 잘리지 않을 만큼)
    feet = max(int(np.nonzero(rows[r][..., 3].any(1))[0].max()) for p in parts['uni'] for r, sl, z in p['L'])
    top = min(int(np.nonzero(rw[..., 3].any(1))[0].min()) for rw in rows if rw[..., 3].any())
    dy = max(0, min(FH - 1 - feet, top)); rows = [np.concatenate([np.zeros((dy,) + rw.shape[1:], np.uint8), rw[:FH - dy]]) for rw in rows]
    print('shift', dy, 'feet', feet, 'top', top)
    sheet = np.concatenate(rows, axis=0); OUT = os.path.join(HERE, '..', 'out'); Image.fromarray(sheet).save(os.path.join(OUT, 'avatar_parts.png'))
    # 칠할 색의 밝기 기준(stops): 층마다 회색 밝기 분포에서. 피부는 음영이 살게 넓게 고정
    def stops_of(slot):
        vals = [sheet[r * FH:(r + 1) * FH][..., 0][(sheet[r * FH:(r + 1) * FH][..., 3] > 0) & (sheet[r * FH:(r + 1) * FH][..., 0] == sheet[r * FH:(r + 1) * FH][..., 1]) & (sheet[r * FH:(r + 1) * FH][..., 1] == sheet[r * FH:(r + 1) * FH][..., 2])]
                for cat in parts.values() for p in cat for r, sl, z in p['L'] if sl == slot]
        v = np.concatenate(vals) if vals else np.array([200]); v = v[(v > 40) & (v < 236)]
        return [int(np.percentile(v, q)) for q in (90, 62, 35, 10)]
    stops = {s: stops_of(s) for s in ('hair', 'cloth', 'shoes', 'house')}; stops['eye'] = [205, 150, 105, 70]; stops['skin'] = [228, 206, 180, 146]; stops['house'] = [140, 116, 96, 74]
    pal = json.load(open(os.path.join(HERE, 'palette.json')))
    json.dump(dict(fw=FW, fh=FH, frames=NF, src='art/iso/avatar_parts.png', z=['hairU', 'skin', 'cloth', 'head', 'face', 'hairO'], base=[[nose_row, 'skin', 'face']], parts=parts, outline=False,
                   stops=stops, pal=pal, head=dict(t=CHIN - 20 + dy, b=CHIN + 2 + dy), scale=.75), open(os.path.join(OUT, 'avatar_parts.json'), 'w'), ensure_ascii=False)
    print('rows', len(rows), sheet.shape)
