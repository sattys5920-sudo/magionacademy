# 표정 시트(생성기가 밑그림 expr_sheet_base.png의 대머리 머리에 얼굴을 그린 것) → 표정 층 (expr_feats.npz)
# 4×4칸: 1·3줄 정면, 2·4줄 옆(바로 위 칸과 같은 표정). 칸마다 머리 상자를 게임 머리 크기로 나눠 밑그림과 달라진 피부 칸만 1칸 = 1px로
# python3 expr_ext.py 시트A.png 시트B.png   (../out/avatar_parts.* 가 있어야 해요: 머리 자리를 거기서 재요)
import sys, os, json, numpy as np
from PIL import Image
from scipy import ndimage as nd
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'out')
def head_boxes():
    """까까머리(13번) 앞·옆 머리 상자 (프레임 좌표, 출력 시트 기준)"""
    J = json.load(open(os.path.join(OUT, 'avatar_parts.json'))); S = np.array(Image.open(os.path.join(OUT, 'avatar_parts.png')))
    FW, FH = J['fw'], J['fh']; rows = [r for r, sl, z in J['parts']['hair'][12]['L'] if z in ('hairO', 'head')]
    box = {}
    for fr in (0, 6):
        m = np.zeros((FH, FW), bool)
        for r in rows: m |= S[r * FH:(r + 1) * FH, fr * FW:(fr + 1) * FW, 3] > 0
        m[34:] = False; ys, xs = np.nonzero(m); box[fr] = (xs.min(), ys.min(), xs.max(), ys.max())
    return box, J['head']['t'] - 8, FW, FH            # 출력 시트는 아래로 dy 내려가 있어요 (head.t = CHIN-20+dy)
def cells(path):
    a = np.array(Image.open(path).convert('RGB')).astype(int); H, W = a.shape[:2]
    green = (a[..., 1] > 170) & (a[..., 0] < 140) & (a[..., 2] < 140); out = []
    for r in range(4):
        for c in range(4):
            y0, y1, x0, x1 = r * H // 4, (r + 1) * H // 4, c * W // 4, (c + 1) * W // 4
            lab, n = nd.label(~green[y0:y1, x0:x1]); i = int(np.argmax(nd.sum(np.ones_like(lab), lab, range(1, n + 1)))) + 1
            ys, xs = np.nonzero(lab == i); out.append(a[y0 + ys.min():y0 + ys.max() + 1, x0 + xs.min():x0 + xs.max() + 1])
    return out
def blocks(img, w, h):
    H, W = img.shape[:2]; bx, by = W / w, H / h; res = {}
    for r in range(h):
        for c in range(w):
            ya, yb = int(r * by + by * .25), int((r + 1) * by - by * .25); xa, xb = int(c * bx + bx * .25), int((c + 1) * bx - bx * .25)
            res[r, c] = img[ya:max(yb, ya + 1), xa:max(xb, xa + 1)].reshape(-1, 3)
    return res
if __name__ == '__main__':
    box, dy, FW, FH = head_boxes(); base = cells(os.path.join(HERE, 'expr_sheet_base.png')); out = {}
    for si, p in enumerate(sys.argv[1:3]):
        for k, img in enumerate(cells(p)):
            r, c = divmod(k, 4); fr = 0 if r % 2 == 0 else 6; e = si * 8 + (r // 2) * 4 + c
            x0, y0, x1, y1 = box[fr]; w, h = x1 - x0 + 1, y1 - y0 + 1
            B = blocks(base[k], w, h); G = blocks(img, w, h)
            o = np.zeros((FH, FW, 4), np.uint8)
            for (rr, cc), px in G.items():
                bc = np.median(B[rr, cc], 0)
                if not (bc[0] > 200 and 150 < bc[1] < 225 and bc[2] > 120): continue    # 밑그림 피부 칸만
                d = np.abs(px - bc).sum(1) > 70
                if d.mean() < .35: continue
                q = (px[d] // 16) * 16 + 8; vals, cnt = np.unique(q, axis=0, return_counts=True)
                o[y0 + rr - dy, x0 + cc, :3] = vals[np.argmax(cnt)]; o[y0 + rr - dy, x0 + cc, 3] = 255
            out[f'{e}/{fr}'] = o
    np.savez_compressed(os.path.join(HERE, 'expr_feats.npz'), **out); print(len(out), 'faces', 'dy', dy, box)
