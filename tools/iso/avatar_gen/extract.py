# 생성 이미지 시트 → 원래 픽셀 크기의 칸들 (cells.npz). 원본 시트는 저장소에 넣지 않았어요 (크기가 커서)
# 시트에서 그림 덩어리(칸)를 찾아 번호를 붙여요
import numpy as np, sys, json
from PIL import Image, ImageDraw
from scipy import ndimage
def fg_mask(a):
    r, g, b = [a[..., i].astype(int) for i in range(3)]
    bg = (g > r + 45) & (g > b + 45) & (g > 120)
    return ~bg
ROWS = {'side1': 2, 'side2': 2, 'side3': 2, 'side4': 2, 'mouth': 2, 'base': 3}
def blobs(path, min_area=1500, close=2, nrows=None):
    import os; nrows = nrows or ROWS.get(os.path.basename(path)[:-4])
    a = np.array(Image.open(path).convert('RGB')); m = fg_mask(a)
    m2 = ndimage.binary_closing(m, iterations=close)
    lab, n = ndimage.label(m2)
    objs = ndimage.find_objects(lab); out = []
    for i, sl in enumerate(objs):
        area = (lab[sl] == i + 1).sum()
        if area < min_area: continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        out.append(dict(box=[x0, y0, x1, y1], area=int(area), lab=i + 1))
    # 줄(위→아래) 다음 칸(왼→오) 순서: 줄 수를 알면 가운데 높이의 큰 틈으로 나눠요
    out.sort(key=lambda o: (o['box'][1] + o['box'][3]) / 2)
    cy = [(o['box'][1] + o['box'][3]) / 2 for o in out]
    if nrows and len(out) >= nrows:
        gaps = sorted(range(1, len(out)), key=lambda i: cy[i] - cy[i - 1], reverse=True)[:nrows - 1]
        cuts = [0] + sorted(gaps) + [len(out)]; rows = [out[cuts[k]:cuts[k + 1]] for k in range(nrows)]
    else:
        rows, cur = [], []
        for o, c in zip(out, cy):
            if cur and c - np.mean([(x['box'][1] + x['box'][3]) / 2 for x in cur]) > 40: rows.append(cur); cur = []
            cur.append(o)
        if cur: rows.append(cur)
    res = []
    for r in rows: res += sorted(r, key=lambda o: o['box'][0])
    return a, m, lab, res
if False:
    for name in sys.argv[1:]:
        a, m, lab, res = blobs(f'src/{name}.png')
        im = Image.fromarray(a); d = ImageDraw.Draw(im)
        for k, o in enumerate(res):
            d.rectangle(o['box'], outline=(255, 0, 0), width=2); d.text((o['box'][0] + 2, o['box'][1] + 2), str(k), fill=(255, 255, 0))
        im.save(f'lab_{name}.png'); json.dump([o['box'] for o in res], open(f'box_{name}.json', 'w'))
        print(name, len(res))

# 시트 → 원래 픽셀 크기 (시트마다 픽셀 블록 크기를 찾아서 블록 가운데 색을 써요)
import numpy as np, json, sys, pickle
from PIL import Image
def block_size(a):
    res = {}
    for axis in (1, 0):
        d = np.abs(np.diff(a.astype(int), axis=axis)).sum(axis=2) > 80
        pos = np.nonzero(d)[axis] + 1.0
        best = None
        for p in np.arange(4.5, 10, 0.01):
            ph = (pos / p) % 1.0; h, _ = np.histogram(ph, bins=30, range=(0, 1)); k = np.argmax(h)
            sc = h.max() + .5 * (h[(k - 1) % 30] + h[(k + 1) % 30]) - h.mean() * 3
            if best is None or sc > best[0]: best = (sc, p, (k + .5) / 30 * p)
        res[axis] = best
    return res
def sample(a, x0, y0, px, py, nx, ny):
    out = np.zeros((ny, nx, 3), np.uint8)
    for j in range(ny):
        for i in range(nx):
            xa, ya = x0 + i * px, y0 + j * py
            blk = a[int(ya + py * .3):int(ya + py * .7) + 1, int(xa + px * .3):int(xa + px * .7) + 1].reshape(-1, 3)
            out[j, i] = np.median(blk, axis=0) if len(blk) else (0, 255, 0)
    return out
def cells_of(name):
    a, m, lab, res = blobs(f'src/{name}.png')
    out = []
    for o in res:
        x0, y0, x1, y1 = o['box']; pad = 8
        sub = a[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
        bs = block_size(sub); px, ox = bs[1][1], bs[1][2]; py, oy = bs[0][1], bs[0][2]
        nx, ny = int((sub.shape[1] - ox) / px), int((sub.shape[0] - oy) / py)
        out.append(dict(rgb=sample(sub, ox, oy, px, py, nx, ny), p=(px, py), box=o['box']))
    return out
if __name__ == '__main__':
    # 사용법: src/ 에 시트를 넣고 python3 extract.py base hairA hairB hairC hairD u1 u2 u3 u4 u5 side1 side2 side3 side4 mouth
    D = {}
    for name in sys.argv[1:]:
        D[name] = cells_of(name)
        ps = [c['p'] for c in D[name]]
        print(name, len(ps), 'block px', np.round(np.median([p[0] for p in ps]), 2), np.round(np.median([p[1] for p in ps]), 2), 'spread', np.round(np.std([p[0] for p in ps]), 2))
    arrs = {f'{n}/{i}': c['rgb'] for n, cs in D.items() for i, c in enumerate(cs)}
    # 눈 시트는 7×5 격자로 잘라요 (머리끼리 붙어 있어서)
    a = np.array(Image.open('src/eyes.png').convert('RGB')); H, W = a.shape[:2]; cw, ch = W / 7, H / 5
    EYE_PICK = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (1, 0), (1, 1), (1, 2), (1, 4), (1, 5), (2, 0), (2, 1), (2, 3), (2, 4), (2, 5)]
    for i, (r, c) in enumerate(EYE_PICK):
        sub = a[int(r * ch):int((r + 1) * ch), int(c * cw):int((c + 1) * cw)]
        bs = block_size(sub); px, ox = bs[1][1], bs[1][2]; py, oy = bs[0][1], bs[0][2]
        arrs[f'eyecell/{i}'] = sample(sub, ox, oy, px, py, int((sub.shape[1] - ox) / px), int((sub.shape[0] - oy) / py))
    np.savez_compressed('cells.npz', **arrs)
