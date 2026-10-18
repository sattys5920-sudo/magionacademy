# 눈·입 생성 시트(대머리 머리 5×3) → 블록 격자 (face_blocks.npz)
# python3 face_ext.py 앞입.png 앞눈.png 옆눈.png 옆입.png   (옆 시트 2·3줄은 오른쪽을 봐서 뒤집어 왼쪽 보기로 맞춰요)
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
def cells(green):
    H, W = green.shape; out = []
    for r in range(3):
        for c in range(5):
            y0, y1, x0, x1 = r * H // 3, (r + 1) * H // 3, c * W // 5, (c + 1) * W // 5
            g = green[y0:y1, x0:x1].copy(); g[:, :3] = True; g[:, -3:] = True
            lab, n = nd.label(~g); sz = nd.sum(np.ones_like(lab), lab, range(1, n + 1)); i = int(np.argmax(sz)) + 1
            mm = lab == i; ys, xs = np.nonzero(mm)
            out.append(((slice(y0 + ys.min(), y0 + ys.max() + 1), slice(x0 + xs.min(), x0 + xs.max() + 1)), mm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]))
    return out
def grid_of(sub):
    """블록 크기와 시작점: 색이 바뀌는 자리에 가장 잘 맞는 격자"""
    d = (np.abs(np.diff(sub, axis=1)).sum(2) > 60).sum(0); e = (np.abs(np.diff(sub, axis=0)).sum(2) > 60).sum(1)
    def fit(v, b): return max((v[np.arange(ph, len(v) - 1, b).astype(int)].sum(), ph) for ph in np.arange(0, b, .5))
    b = max((fit(d, b)[0], b) for b in np.arange(10.5, 12.8, .02))[1]
    return b, fit(d, b)[1], fit(e, b)[1]
def blocks(path, flip_from=None):
    a = np.array(Image.open(path).convert('RGB')).astype(int)
    green = (a[..., 1] > 170) & (a[..., 0] < 140) & (a[..., 2] < 140); res = []
    for i, (s, m) in enumerate(cells(green)):
        sub = a[s]; b, px, py = grid_of(sub)
        xs = np.arange(px + b / 2, m.shape[1], b).astype(int); ys = np.arange(py + b / 2, m.shape[0], b).astype(int)
        rgb = sub[ys][:, xs].astype(np.uint8); mm = m[ys][:, xs]
        if flip_from is not None and i >= flip_from: rgb, mm = rgb[:, ::-1], mm[:, ::-1]
        res.append((rgb, mm))
    return res
if __name__ == '__main__':
    out = {}
    for key, p, fl in zip(('fm', 'fe', 'se', 'sm'), sys.argv[1:5], (None, None, 5, 5)):
        for i, (rgb, m) in enumerate(blocks(p, fl)): out[f'{key}/{i}/rgb'] = rgb; out[f'{key}/{i}/m'] = m
    np.savez_compressed(os.path.join(HERE, 'face_blocks.npz'), **out); print(len(out) // 2, 'cells')
