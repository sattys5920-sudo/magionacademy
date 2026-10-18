# 큰 픽셀 그림을 작은 픽셀 그림으로: 칸마다 덮는 원본 픽셀을 종류별로 세어 정해요 (테두리·어두운 점은 살려요)
import numpy as np
def classes(a):
    r, g, b = [a[..., i].astype(int) for i in range(3)]
    lum = (r * 3 + g * 6 + b) / 10
    bg = (g > r + 45) & (g > b + 45)
    dark = (lum < 70) & ~bg
    return bg, dark, lum
def reduce(a, f, dark_th=.28, bg_th=.5):
    H, W = a.shape[:2]; nh, nw = max(1, int(round(H * f))), max(1, int(round(W * f)))
    bg, dark, lum = classes(a)
    out = np.zeros((nh, nw, 3), np.uint8); ob = np.zeros((nh, nw), bool); od = np.zeros((nh, nw), bool)
    for j in range(nh):
        y0, y1 = j / f, (j + 1) / f
        for i in range(nw):
            x0, x1 = i / f, (i + 1) / f
            ys = np.arange(int(y0), min(H, int(np.ceil(y1)))); xs = np.arange(int(x0), min(W, int(np.ceil(x1))))
            if not len(ys) or not len(xs): ob[j, i] = True; continue
            wy = np.minimum(ys + 1, y1) - np.maximum(ys, y0); wx = np.minimum(xs + 1, x1) - np.maximum(xs, x0)
            w = np.outer(wy, wx); w /= w.sum()
            B, Dk = bg[np.ix_(ys, xs)], dark[np.ix_(ys, xs)]; C = a[np.ix_(ys, xs)].reshape(-1, 3)
            if (w * B).sum() > bg_th: ob[j, i] = True; continue
            if (w * Dk).sum() >= dark_th:
                m = (Dk & ~B).ravel(); out[j, i] = np.median(C[m], 0) if m.any() else (42, 24, 48); od[j, i] = True; continue
            m = (~Dk & ~B).ravel(); ww = w.ravel()[m]; cc = C[m]
            # 가장 많이 덮은 색 무리의 중간값 (색이 섞여 흐려지지 않게)
            keys = (cc // 24).astype(int); kk = keys[:, 0] * 10000 + keys[:, 1] * 100 + keys[:, 2]
            best = max(set(kk.tolist()), key=lambda k: ww[kk == k].sum())
            out[j, i] = np.median(cc[kk == best], 0)
    return out, ob, od
def to_rgba(out, ob):
    a = np.zeros(out.shape[:2] + (4,), np.uint8); a[..., :3] = out; a[..., 3] = np.where(ob, 0, 255); return a
def bg_rgba(rgb):
    bg, dark, lum = classes(rgb); a = np.zeros(rgb.shape[:2] + (4,), np.uint8); a[..., :3] = rgb; a[..., 3] = np.where(bg, 0, 255); return a
