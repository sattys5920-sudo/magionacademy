# 생성 그림(이미지 생성기로 뽑은 시트) → 아바타 부품 (게임 형식: 한 줄 = 한 층의 9프레임, 회색은 고른 색으로 칠해요)
# 프레임: 0~2 앞(서기·걷기A·걷기B), 3~5 뒤, 6~8 옆(왼쪽 보기)
# 칸 그림은 cells.npz (extract.py가 생성 이미지 시트에서 뽑아요). python3 assemble.py → ../out/avatar_parts.png + .json
import json, os, numpy as np
from PIL import Image
from scipy import ndimage
from reduce import reduce
from picks import FRONT, BACK, SIDE
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
    open_face(O, S, (0, 1, 2), NECKX, FACE_RX); open_face(O, S, (6, 7, 8), SIDE_C, SIDE_RX)
    return O, U, S
# ---------- 얼굴 비율 (모든 머리·표정이 같은 자리) ----------
# 턱 = CHIN, 앞모습 얼굴 가운데 = NECKX. 얼굴은 둥글고 가로가 조금 더 넓어요 (너비 15 · 앞머리 아래~턱 11)
#   이마  CHIN-10 ~ CHIN-9 : 늘 피부 (앞머리는 CHIN-11 까지만, 눈을 절대 가리지 않아요)
#   눈    CHIN-8 ~ CHIN-6  : 3칸 너비, 두 눈 사이 5칸 (눈 너비의 약 1.7배), 같은 줄
#   코    CHIN-5           : 옅은 점 하나
#   입    CHIN-3           : 1줄 (벌린 입은 CHIN-4 ~ CHIN-3), 보통 2칸 · 크게 웃어도 4칸
#   턱    CHIN-2 ~ CHIN-1 피부, CHIN 테두리
# 옆(3/4, 왼쪽 보기): 얼굴 가운데가 SIDE_C, 먼 눈은 2칸으로 얼굴 왼쪽 끝 가까이
EYE_TOP, EYE_W, EYE_GAP = CHIN - 8, 3, 5
FACE_RX, FACE_CY, FACE_TOP = 7.5, CHIN - 7, CHIN - 10
SIDE_C, SIDE_RX = NECKX - 2, 6.5
MOUTH_ROW = CHIN - 3
NOSE_ROW = CHIN - 5
SKIN_FILL = 210
OUTL = (42, 24, 48, 255)
SIDE_SHIFT = {9: 4, 7: 1, 33: 1, 3: 1, 25: 2, 26: 1, 38: 1}   # 옆얼굴 위치 맞추기 (얼굴이 오른쪽에 치우친 그림들)
SIDE_KEEP = {6}            # 이미 왼쪽을 보는 옆모습 (7번)
def dil4(m):
    o = m.copy(); o[1:] |= m[:-1]; o[:-1] |= m[1:]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]; return o
def open_face(O, S, frames, cx, rx):
    """얼굴 자리(둥근 영역)의 앞머리·옆머리를 걷어 내고 피부로 채운 다음 테두리를 다시 그어요"""
    yy, xx = np.mgrid[0:FH, 0:FW]
    reg = (((xx - cx) / rx) ** 2 + ((yy - FACE_CY) / 7.5) ** 2 <= 1) & (yy >= FACE_TOP) & (yy <= CHIN - 1)
    for fr in frames:
        o, sk = O.f[fr], S.f[fr]
        head = (o[..., 3] > 0) | (sk[..., 3] > 0)
        fill = reg & head
        o[fill, 3] = 0
        sk[fill] = (SKIN_FILL, SKIN_FILL, SKIN_FILL, 255)                 # 얼굴은 고른 피부 한 톤 (머리카락 그림자 자국 없이)
        # 남은 머리카락이 얼굴과 닿는 곳은 어두운 선으로 (앞머리 끝·옆머리 안쪽)
        edge_h = dil4(fill) & (o[..., 3] > 0) & ~fill
        g = edge_h & (o[..., 0] == o[..., 1]) & (o[..., 1] == o[..., 2])
        o[g, :3] = np.minimum(o[g, :3], 70)
        # 얼굴 바깥이 빈 곳이면 자주 테두리
        anyp = (o[..., 3] > 0) | (sk[..., 3] > 0)
        edge_f = fill & dil4(~anyp)
        o[edge_f] = OUTL; sk[edge_f, 3] = 0
        # 둥근 느낌: 테두리·머리카락과 닿는 얼굴 가장자리 한 칸만 살짝 어둡게
        fill2 = fill & ~edge_f; anyo = o[..., 3] > 0
        rim = fill2 & dil4(anyo | ~((o[..., 3] > 0) | (sk[..., 3] > 0)))
        sk[rim, :3] = SKIN_FILL - 14
# 눈 (왼쪽 눈, 첫 칸이 바깥쪽. 오른쪽 눈은 좌우 뒤집기) — 모두 3×3
# L 선(자주) · D/I/J 눈동자 어둠/중간/밝음(고른 눈 색) · W 흰 반짝 · P 동공 · K 하트 · T 눈물 · V 뱀파이어 빨강
EYE_PIX = [
    ['LLL', 'WDD', 'DDJ'],      # 반짝 동글
    ['LLL', 'WDD', 'DIJ'],      # 큰 애니
    ['...', 'LLL', 'DDI'],      # 졸린 눈
    ['.L.', 'L.L', '...'],      # 웃는 눈 ^ ^
    ['LLL', 'JPJ', 'IPI'],      # 고양이 눈
    ['LWL', 'WWW', 'LWL'],      # 별 눈동자
    ['KLK', 'KKK', '.K.'],      # 하트 눈동자
    ['LLL', 'WDD', 'DDJ'],      # 윙크 (오른쪽은 감은 눈)
    ['L..', 'LLL', 'DDJ'],      # 단호한 눈
    ['LLL', 'WDD', 'TDT'],      # 눈물 그렁
    ['LLL', '..L', 'LLL'],      # 빙글빙글
    ['...', '.L.', '.L.'],      # 점 눈
    ['LL.', 'VPV', '.VV'],      # 뱀파이어 눈
    ['LWL', 'WDD', 'DIJ'],      # 순정 반짝
    ['L..', '.L.', 'L..'],      # 질끈 감은 눈 > <
]
EYE_WINK_R = ['...', 'LLL', '...']
# 입 (가운데 정렬): M 선 · R 입속 · N 혀 · W 이(1~2점). 2줄짜리는 위로 (CHIN-4 ~ CHIN-3)
MOUTH_PIX = [
    ['M..M', '.MM.'],           # 미소
    ['M.M', '.M.'],             # 고양이 입
    ['.MM.', 'M..M'],           # 시무룩
    ['MMM', 'W.W'],             # 송곳니 미소
    ['MMMM', '.RR.'],           # 활짝 웃음
    ['MM', 'MM'],               # 놀란 입
    ['MMM', '.N.'],             # 메롱
    ['MM'],                     # 일자 입
    ['MMMM', 'MWWM'],           # 이 드러낸 웃음
    ['M.M.', '.M.M'],           # 울먹
]
FACE_COL = dict(L=(42, 24, 48, 255), D=(70, 70, 70, 255), I=(145, 145, 145, 255), J=(205, 205, 205, 255), W=(255, 255, 250, 255),
                P=(24, 12, 30, 255), K=(255, 118, 160, 255), T=(160, 214, 255, 255), V=(206, 40, 64, 255),
                M=(120, 46, 66, 255), R=(196, 64, 86, 255), N=(244, 130, 156, 255))
def pix(rows):
    h, w = len(rows), max(len(r) for r in rows); a = np.zeros((h, w, 4), np.uint8)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': a[y, x] = FACE_COL[ch]
    return a
def eye_layers(i, cells=None):
    E, B = Lay(), Lay()
    gl = pix(EYE_PIX[i]); gr = pix(EYE_WINK_R) if i == 7 else gl[:, ::-1]
    lx = NECKX - EYE_GAP // 2 - EYE_W; rx = NECKX + EYE_GAP // 2 + 1          # 두 눈 사이 EYE_GAP칸, 가운데 NECKX
    slx = SIDE_C - EYE_GAP // 2 - 2; srx = SIDE_C + EYE_GAP // 2              # 옆: 먼 눈 2칸, 가까운 눈 3칸
    for j in range(3):
        E.paste(j, gl, lx, EYE_TOP); E.paste(j, gr, rx, EYE_TOP)
        E.paste(6 + j, gl[:, -2:], slx, EYE_TOP); E.paste(6 + j, gr, srx, EYE_TOP)
    return E, B
def mouth_layer(i):
    M = Lay(); g = pix(MOUTH_PIX[i]); h, w = g.shape[:2]; y0 = MOUTH_ROW - (h - 1)
    for j in range(3):
        M.paste(j, g, NECKX - w // 2, y0); M.paste(6 + j, g, SIDE_C - 1 - w // 2, y0)
    return M
def nose_layer():
    N = Lay(); n = np.zeros((1, 1, 4), np.uint8); n[0, 0] = (186, 186, 186, 255)   # 피부색으로 칠해지는 옅은 그림자
    for j in range(3): N.paste(j, n, NECKX, NOSE_ROW); N.paste(6 + j, n, SIDE_C - 3, NOSE_ROW)
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
