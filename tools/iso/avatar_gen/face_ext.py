# 눈·입 생성 시트 → 얼굴 부품 (face_feats.npz)
# 생성기에 밑그림 시트(front_sheet_base.png / side_sheet_base.png: 게임 머리 15개, 1칸 = 게임 1px)를 주고 눈·입만 그리게 했어요.
# 칸마다 머리 테두리 상자를 찾아 머리 크기(앞 19×18, 옆 18×19)로 나누고, 밑그림과 색이 달라진 피부 칸만 남겨요.
# python3 face_ext.py 앞눈.png 앞입.png 옆눈.png 옆입.png
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = {'f': (19, 18), 's': (18, 19)}          # 머리 크기 (가로, 세로) 게임 px
def heads(path):
    a = np.array(Image.open(path).convert('RGB')).astype(int); H, W = a.shape[:2]
    green = (a[..., 1] > 170) & (a[..., 0] < 140) & (a[..., 2] < 140); out = []
    for r in range(3):
        for c in range(5):
            y0, y1, x0, x1 = r * H // 3, (r + 1) * H // 3, c * W // 5, (c + 1) * W // 5
            lab, n = nd.label(~green[y0:y1, x0:x1]); i = int(np.argmax(nd.sum(np.ones_like(lab), lab, range(1, n + 1)))) + 1
            ys, xs = np.nonzero(lab == i)
            out.append(a[y0 + ys.min():y0 + ys.max() + 1, x0 + xs.min():x0 + xs.max() + 1])
    return out
def blocks(img, w, h):
    """머리 상자를 w×h 칸으로: 칸 가운데 60%의 색들 (칸마다 화소 목록)"""
    H, W = img.shape[:2]; bx, by = W / w, H / h; res = {}
    for r in range(h):
        for c in range(w):
            ya, yb = int(r * by + by * .2), int((r + 1) * by - by * .2); xa, xb = int(c * bx + bx * .2), int((c + 1) * bx - bx * .2)
            res[r, c] = img[ya:max(yb, ya + 1), xa:max(xb, xa + 1)].reshape(-1, 3)
    return res
def feats(path, base_path, view):
    w, h = HEAD[view]; base = heads(base_path)[0]; B = blocks(base, w, h); out = []
    bc = {k: np.median(v, 0) for k, v in B.items()}
    skin = {k: (v[0] > 200 and 150 < v[1] < 225 and v[2] > 120) for k, v in bc.items()}
    for img in heads(path):
        G = blocks(img, w, h); o = np.zeros((h, w, 4), np.uint8)
        for (r, c), px in G.items():
            if not skin[r, c]: continue
            d = np.abs(px - bc[r, c]).sum(1) > 70
            if d.mean() < .35: continue
            q = (px[d] // 16) * 16 + 8; vals, cnt = np.unique(q, axis=0, return_counts=True)
            o[r, c, :3] = vals[np.argmax(cnt)]; o[r, c, 3] = 255
        out.append(o)
    return out
if __name__ == '__main__':
    fb, sb = os.path.join(HERE, 'front_sheet_base.png'), os.path.join(HERE, 'side_sheet_base.png'); out = {}
    for key, p, b, v in zip(('fe', 'fm', 'se', 'sm'), sys.argv[1:5], (fb, fb, sb, sb), 'ffss'):
        for i, o in enumerate(feats(p, b, v)): out[f'{key}/{i}'] = o
    np.savez_compressed(os.path.join(HERE, 'face_feats.npz'), **out); print(len(out), 'cells')
