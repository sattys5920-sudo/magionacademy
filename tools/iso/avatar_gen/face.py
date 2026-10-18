# 눈·입 (face_feats.npz: face_ext.py가 생성 시트에서 뽑은 머리 기준 칸, 1칸 = 게임 1px) → 게임 프레임 자리
# 밑그림 머리의 왼쪽 위가 프레임에서 어디인지만 알면 그대로 붙여요 (줄이지 않아요)
import os, numpy as np
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
_Z = np.load(os.path.join(HERE, 'face_feats.npz'))
ORIGIN = {False: (9, 12), True: (8, 11)}       # 밑그림 머리 왼쪽 위 → 프레임 (x, y), 턱 = 28 기준 (앞, 옆)
MOUTH_TOP = {False: 13, True: 12}              # 입 시트에 같이 그려진 눈은 이 줄 위라 빼요
LINE = (42, 24, 48, 255); WHITE = (255, 255, 250, 255)
def lum(c): return c[..., 0] * .3 + c[..., 1] * .59 + c[..., 2] * .11
def not_gray(o):
    """색 그대로 둘 칸이 회색이면 게임이 칠해 버려서 살짝 비틀어요"""
    g = (o[..., 3] > 0) & (o[..., 0] == o[..., 1]) & (o[..., 1] == o[..., 2]); o[g, 2] = np.where(o[g, 2] > 250, o[g, 2] - 3, o[g, 2] + 3); return o
def eye_colors(a, i):
    """눈동자는 회색(고른 눈 색으로 칠해짐), 테두리·흰 반짝은 고정. 하트·눈물·뱀파이어는 색 그대로, 별은 노란 별만 그대로"""
    o = np.zeros_like(a); m = a[..., 3] > 0; c = a[..., :3].astype(float); L = lum(c)
    sat = c.max(2) - c.min(2)
    dark = m & (L < 34); white = m & (c.min(2) > 195) & (sat < 45)
    keep = np.zeros_like(m)
    if i in (6, 9, 12): keep = m & ~dark & ~white
    if i == 5: keep = m & (c[..., 0] > 170) & (c[..., 1] > 140) & (c[..., 2] < 120)
    gray = m & ~dark & ~white & ~keep
    o[dark] = LINE; o[white] = WHITE; o[keep] = a[keep]
    gv = np.clip(70 + (L - 35) * 2.2, 70, 205).astype(np.uint8); o[gray, 0] = o[gray, 1] = o[gray, 2] = gv[gray]; o[gray, 3] = 255
    o[keep] = not_gray(o[keep][None])[0] if keep.any() else o[keep]
    return o
def clean(a, cell):
    if cell == 14:   # 마지막 칸 오른쪽 위에 생성기 반짝이 표시가 있어요: 어두운 칸과 안 닿은 밝은 덩어리는 빼요
        m = a[..., 3] > 0; lab, n = nd.label(m, structure=np.ones((3, 3)))
        for k in range(1, n + 1):
            if not (lum(a[lab == k][:, :3].astype(float)) < 90).any(): a[lab == k] = 0
    return a
def eyes(i, side):
    a = clean(_Z[f'{"se" if side else "fe"}/{i}'].copy(), i)
    x, y = ORIGIN[side]; return [(eye_colors(a, i), x, y)]
SIDE_MOUTH = list(range(15))
def mouth(i, side):
    a = clean(_Z[f'{"sm" if side else "fm"}/{i}'].copy(), i); a[:MOUTH_TOP[side]] = 0
    x, y = ORIGIN[side]; return [(not_gray(a), x, y)]
