# 생성 이미지를 원래 픽셀 격자로 되돌리기 (칸마다 격자 크기·위치를 찾아요)
import numpy as np
from PIL import Image
def grid_fit(a):
    best = []
    for axis in (1, 0):
        d = np.abs(np.diff(a.astype(int), axis=axis)).sum(axis=2) > 90
        pos = np.nonzero(d)[axis] + 1.0
        res = []
        for p in np.arange(5.6, 6.2, 0.01):
            ph = (pos / p) % 1.0
            h, _ = np.histogram(ph, bins=24, range=(0, 1))
            k = np.argmax(h); res.append((h.max() + .5 * (h[(k - 1) % 24] + h[(k + 1) % 24]), p, (k + .5) / 24 * p))
        res.sort(reverse=True); best.append(res[0])
    return best   # [(score, p, offset) for x, for y]
def downsample(img):
    a = np.array(img.convert('RGB'))
    (sx, px, ox), (sy, py, oy) = grid_fit(a)
    nx, ny = int((a.shape[1] - ox) / px), int((a.shape[0] - oy) / py)
    out = np.zeros((ny, nx, 3), np.uint8)
    for j in range(ny):
        for i in range(nx):
            x0, y0 = ox + i * px, oy + j * py
            blk = a[int(y0 + py * .3):int(y0 + py * .7) + 1, int(x0 + px * .3):int(x0 + px * .7) + 1].reshape(-1, 3)
            out[j, i] = np.median(blk, axis=0)
    return Image.fromarray(out), (px, py)
def cells(path, cols, rows, margin=0):
    im = Image.open(path).convert('RGB'); W, H = im.size; cw, ch = W / cols, H / rows
    return [[im.crop((int(c * cw) + margin, int(r * ch) + margin, int((c + 1) * cw) - margin, int((r + 1) * ch) - margin)) for c in range(cols)] for r in range(rows)]
