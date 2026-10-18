# 생성 머리(hair_feats.npz) → 게임 층. 모든 머리가 같은 민머리 바탕(까까머리에서 머리카락을 피부로 바꾼 것)을 써요
# 앞·옆: 턱 아래로 머리 바깥에 늘어진 머리카락은 몸 뒤(hairU), 나머지는 얼굴 위(hairO). 뒤: 모두 몸 위
import os, numpy as np
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
_Z = np.load(os.path.join(HERE, 'hair_feats.npz'))
HAIR_T, SK, SK_LINE = 140, 205, 70
def has(n): return f'{n}/0' in _Z.files
def g(v): return np.array([v, v, v, 255], np.uint8)
def bald_base(O12, S12, Lay):
    """민머리 피부 층: 까까머리의 머리카락 자리를 피부로, 바깥 테두리는 어두운 피부"""
    B = Lay()
    for f in range(9):
        s, o = S12.f[f], O12.f[f]; u = (s[..., 3] > 0) | (o[..., 3] > 0)
        u[33 if f >= 6 else 34:] &= s[33 if f >= 6 else 34:, :, 3] > 0     # 목 아래는 피부 층 그대로
        edge = u & ~nd.binary_erosion(u)
        b = s.copy(); m = (o[..., 3] > 0) & u
        b[m & ~edge] = g(SK); b[m & edge] = g(SK_LINE)
        B.f[f] = b
    return B
def layers(n, base, Lay):
    O, U = Lay(), Lay()
    for v in (0, 6, 3):
        a = _Z[f'{n}/{v}']; m = a[..., 3] > 0
        c = a[..., :3].astype(float); L = c[..., 0] * .3 + c[..., 1] * .59 + c[..., 2] * .11
        pink = m & (c[..., 0] > 170) & (c[..., 1] < 130) & (c[..., 2] > 110)
        hm = m & ~pink
        o = np.zeros_like(a)
        if hm.any():
            Lg = np.clip(L + (HAIR_T - np.median(L[hm & (L > 60)])) if (hm & (L > 60)).any() else L, 0, 255).astype(np.uint8)
            o[hm, 0] = o[hm, 1] = o[hm, 2] = Lg[hm]; o[hm, 3] = 255
        o[pink] = a[pink]; o[pink, 2] = np.where(o[pink, 2] > 250, o[pink, 2] - 3, o[pink, 2] + 3)   # 머리끈 색 그대로
        head = base.f[v, ..., 3] > 0
        under = np.zeros(m.shape, bool)
        if v != 3:
            chin = int(np.nonzero((base.f[v, :, 12:24, 3] > 0).any(1))[0].max()) if v == 0 else 28
            under[chin - 1:] = True; under &= ~head | (np.arange(m.shape[0])[:, None] > chin)
        for j in range(3):
            O.f[v + j][(o[..., 3] > 0) & ~under] = o[(o[..., 3] > 0) & ~under]
            U.f[v + j][(o[..., 3] > 0) & under] = o[(o[..., 3] > 0) & under]
    return O, U
