# 생성 시트의 눈·입(face_blocks.npz) → 게임 얼굴 크기의 선명한 픽셀
# 생성 머리는 게임 머리보다 커서(눈 6~7칸) 눈은 0.6배, 입은 가로 0.6배로 줄여요.
# 줄일 때 섞지 않고 칸마다 한 색을 골라요: 테두리·흰 반짝·특별한 색(하트·눈물·별·뱀파이어)을 먼저 살려요
import os, numpy as np
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
_Z = np.load(os.path.join(HERE, 'face_blocks.npz'))
def cellk(key, i): return _Z[f'{key}/{i}/rgb'].astype(int), _Z[f'{key}/{i}/m']
LINE = (42, 24, 48, 255)                      # 눈 테두리 (기존 L)
MLINE = (96, 38, 58, 255)                     # 입 선
SPECIAL_EYES = {5, 6, 9, 12}                  # 별·하트·눈물·뱀파이어: 색 그대로
def lum(a): return a[..., 0] * .3 + a[..., 1] * .59 + a[..., 2] * .11
def feature_mask(rgb, m):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    skin = (r > 185) & (g > 115) & (g < 228) & (b > 85) & (b < 205) & (r - b > 38) & (r - g > 12) & (r - g < 80)
    f = nd.binary_erosion(m, iterations=1) & ~skin
    ring = m & ~nd.binary_erosion(m, iterations=2)
    lab, n = nd.label(f, structure=np.ones((3, 3))); keep = np.zeros_like(f)
    for i in range(1, n + 1):
        cm = lab == i
        if (cm & ring).sum() > cm.sum() * .5: continue
        keep |= cm
    return keep
def classify(rgb, f, special):
    """칸 종류: 0 피부/없음, 1 테두리, 2 흰색, 3 칠할 회색(눈 색), 4 색 그대로"""
    L = lum(rgb); r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    sat = (np.max(rgb, 2) - np.min(rgb, 2))
    c = np.zeros(f.shape, int)
    c[f] = 3
    c[f & special & (sat > 70) & (L > 60)] = 4
    c[f & (L < 52)] = 1
    c[f & (L > 215) & (sat < 45)] = 2
    return c
def quant(rgb, c):
    """칸마다 게임 색 하나로: 테두리 / 흰색 / 회색 3단(눈 색으로 칠함) / 특별한 색"""
    o = np.zeros(c.shape + (4,), np.uint8)
    o[c == 1] = LINE; o[c == 2] = (255, 255, 250, 255)
    g = c == 3; L = lum(rgb.astype(float))
    lv = np.where(L < 95, 70, np.where(L < 150, 130, 195))
    o[g, 0] = o[g, 1] = o[g, 2] = lv[g]; o[g, 3] = 255
    s = c == 4; q = (rgb // 24 * 24 + 12).clip(0, 255); o[s, :3] = q[s]; o[s, 3] = 255
    return o
def shrink(o, tw, th):
    """픽셀을 섞지 않고 줄·칸을 빼서 줄여요: 이웃과 가장 비슷한(겹치는) 줄부터 빼요"""
    def key(v): return [tuple(p) for p in v]
    def drop(o, axis, n):
        for _ in range(n):
            a = o if axis == 0 else o.transpose(1, 0, 2)
            if a.shape[0] <= 1: break
            def cost(i):
                cur = a[i]; nb = [a[j] for j in (i - 1, i + 1) if 0 <= j < len(a)]
                d = min((np.any(cur != x, axis=1)).sum() for x in nb)
                return d * 10 + (cur[:, 3] > 0).sum() * .5 + (0 if 0 < i < len(a) - 1 else 3)
            i = min(range(len(a)), key=cost); a = np.delete(a, i, 0)
            o = a if axis == 0 else a.transpose(1, 0, 2)
        return o
    o = drop(o, 1, max(0, o.shape[1] - tw)); o = drop(o, 0, max(0, o.shape[0] - th)); return o
def crop(a):
    ys, xs = np.nonzero(a[..., 3])
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else a[:0, :0]
def split_lr(f):
    """두 눈 나누기: 가운데쯤 가장 긴 빈 세로줄"""
    cols = f.any(0); xs = np.nonzero(cols)[0]; best = None; x = xs[0]
    while x <= xs[-1]:
        if not cols[x]:
            s = x
            while not cols[x]: x += 1
            if best is None or x - s > best[1] - best[0]: best = (s, x)
        x += 1
    return (best[0] + best[1]) // 2 if best else (xs[0] + xs[-1]) // 2
# 생성 머리 → 게임 머리: 0.77배. 앞: 머리 가운데 = NECKX, 머리 아래 끝(턱 테두리) = 턱+1. 옆: 얼굴 앞 윤곽 = x 10
K = .77
def _groups(key, i, roi_rows, side):
    rgb, m = cellk(key, i); f = feature_mask(rgb, m); h, w = f.shape
    roi = np.zeros_like(f); roi[roi_rows[0]:roi_rows[1], (1 if side else 3):(16 if side else w - 4)] = True; f &= roi
    if side: f[15:, :3] = False
    ys, xs = np.nonzero(m)
    return rgb, f, ys.max(), (xs.min() + xs.max()) / 2
def _place(rgb, c, x0, x1, y0, y1, bot, cx, side, neckx, chin):
    sub = c[y0:y1 + 1, x0:x1 + 1]; sr = rgb[y0:y1 + 1, x0:x1 + 1]
    tw, th = max(1, round(sub.shape[1] * K)), max(1, round(sub.shape[0] * K))
    o = crop(shrink(quant(sr, sub), tw, th))
    fx = 10 + x0 * K if side else neckx + (x0 - cx) * K
    fy = chin + 1 - (bot - y0) * K
    return o, int(np.floor(fx + .5)), int(np.floor(fy + .5))
def eyes(i, side, neckx, chin):
    """[(그림, x, y)]: 앞이면 (왼눈, 오른눈), 옆이면 (먼 눈, 가까운 눈)"""
    rgb, f, bot, cx = _groups('se' if side else 'fe', i, (4, 16 if side else 15), side)
    c = classify(rgb, f, np.full(f.shape, i in SPECIAL_EYES))
    if i == 4: c[c == 4] = 3                  # 고양이 눈: 노랑 대신 고른 눈 색
    mid = split_lr(c > 0); out = []
    for part in (slice(0, mid), slice(mid, c.shape[1])):
        cc = np.zeros_like(c); cc[:, part] = c[:, part]; ys, xs = np.nonzero(cc)
        if len(ys): out.append(_place(rgb, cc, xs.min(), xs.max(), ys.min(), ys.max(), bot, cx, side, neckx, chin))
    return out
SIDE_MOUTH = [0, 1, 2, 3, 4, 5, 7, 8, 9, 14]   # 옆 입 시트는 7번째에 작은 o가 더 들어가 있고 울먹은 맨 끝
def mouth(i, side, neckx, chin):
    rgb, f, bot, cx = _groups('sm' if side else 'fm', SIDE_MOUTH[i] if side else i, (12, 19), side)
    lab, n = nd.label(f, structure=np.ones((3, 3)))
    for k in range(1, n + 1):                 # 감은 눈 곡선(활짝 웃는 입 위)은 빼요
        ys, _ = np.nonzero(lab == k)
        if ys.max() < 13: f[lab == k] = False
    c = classify(rgb, f, np.ones(f.shape, bool)); c[c == 3] = 4
    ys, xs = np.nonzero(c)
    o, x, y = _place(rgb, c, xs.min(), xs.max(), ys.min(), ys.max(), bot, cx, side, neckx, chin)
    o[(o[..., 3] > 0) & (lum(o[..., :3].astype(float)) < 70)] = MLINE
    return [(o, x, y)]
