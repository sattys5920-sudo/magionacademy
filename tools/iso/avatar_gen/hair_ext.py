# 머리 모양 시트(생성기가 밑그림 hair_heads_base.png의 민머리에 머리카락을 그린 것) → hair_feats.npz
# 시트 1장 = 4줄(머리 4종) × 앞·옆·뒤. 밑그림 칸 자리를 생성 그림 크기로 맞춘 뒤 얼굴(눈)로 위치를 미세 조정하고,
# 1칸 = 1px로 읽어 밑그림과 달라진 '머리카락 색' 칸만 남겨요 (얼굴·피부는 건드리지 않아요)
# python3 hair_ext.py gen_src/hair1.png ... gen_src/hair10.png
import sys, os, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
TB = 10; CW, CH = 33, 38; PADX, PADT = 5, 5; COLS, ROWS = 3, 4
FBOX = (8, 13)                 # 칸 머리 상자 왼쪽 위 = 프레임 (x, y) (출력 시트 좌표, 아래로 4 내려간 것)
DY = 4
VIEWS = (0, 6, 3)              # 칸 열 → 프레임 (앞, 옆, 뒤)
FW, FH = 36, 58
SKIP = {(6, 1): None, (6, 2): 22}   # 시트 6: 2줄에 반묶음(23번)이 그려졌어요 → 23번으로, 3줄(콘로 중복)은 버려요
def load(p): return np.array(Image.open(p).convert('RGB')).astype(int)
TPL = load(os.path.join(HERE, 'hair_heads_base.png'))
def tpl_block(cx, cy):         # 밑그림 칸 블록 색
    return TPL[cy * TB + TB // 2, cx * TB + TB // 2]
def kinds(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    green = (g > 160) & (r < 150) & (b < 150)
    skin = (r > 195) & (g > 140) & (b > 110) & (r - b > 30) & (r - b < 110)
    lum = r * .3 + g * .59 + b * .11
    brown = ~green & ~skin & (r >= g) & (g >= b - 10) & (r - b > 25) & (lum < 200)
    pink = (r > 170) & (g < 130) & (b > 110)
    dark = ~green & (lum < 75)
    return green, skin, brown, pink, dark
def read_cell(G, sx, sy, c0, r0, off):
    """칸의 블록 색 (CH×CW): 블록 가운데 60% 의 가장 흔한 색"""
    out = np.zeros((CH, CW, 3), int)
    for by in range(CH):
        for bx in range(CW):
            X0 = ((c0 + bx) * TB) * sx + off[0]; Y0 = ((r0 + by) * TB) * sy + off[1]; w = TB * sx; h = TB * sy
            xa, xb = int(X0 + w * .25), int(X0 + w * .75) + 1; ya, yb = int(Y0 + h * .25), int(Y0 + h * .75) + 1
            px = G[max(0, ya):yb, max(0, xa):xb].reshape(-1, 3)
            if not len(px): continue
            q = (px // 12) * 12 + 6; v, n = np.unique(q, axis=0, return_counts=True); out[by, bx] = v[np.argmax(n)]
    return out
def align(G, sx, sy, c0, r0):
    """눈·입(밑그림의 어두운 얼굴 칸)이 가장 잘 겹치는 미세 위치"""
    tb = np.array([[tpl_block(c0 + bx, r0 + by) for bx in range(CW)] for by in range(CH)])
    _, tskin, _, _, tdark = kinds(tb)
    ys, xs = np.nonzero(tdark | tskin)
    best = (-1, (0, 0))
    for dx in range(-6, 7, 2):
        for dy in range(-6, 7, 2):
            cs = read_cell(G, sx, sy, c0, r0, (dx, dy))
            _, s, _, _, d = kinds(cs); sc = int((s & tskin).sum() + 2 * (d & tdark).sum())
            if sc > best[0]: best = (sc, (dx, dy))
    return best[1], tb
def extract(path):
    G = load(path); sy = G.shape[0] / TPL.shape[0]; sx = G.shape[1] / TPL.shape[1]; res = {}
    for r in range(ROWS):
        off_row = None
        for c in range(COLS):
            c0, r0 = 1 + c * CW, 1 + r * CH
            if c < 2: off, tb = align(G, sx, sy, c0, r0); off_row = off if c == 0 else off_row
            else: off = off_row; tb = np.array([[tpl_block(c0 + bx, r0 + by) for bx in range(CW)] for by in range(CH)])
            cs = read_cell(G, sx, sy, c0, r0, off)
            green, skin, brown, pink, dark = kinds(cs)
            changed = np.abs(cs - tb).sum(-1) > 70
            tg, tskin, _, _, tdark = kinds(tb)
            near_brown = np.zeros_like(brown)
            for ddy in (-1, 0, 1):
                for ddx in (-1, 0, 1): near_brown |= np.roll(np.roll(brown, ddy, 0), ddx, 1)
            hair = (brown | pink | (dark & near_brown & ~tdark) | (dark & tg)) & changed & ~green
            o = np.zeros((FH, FW, 4), np.uint8)
            for by, bx in zip(*np.nonzero(hair)):
                x = FBOX[0] + bx - PADX; y = FBOX[1] + by - PADT - DY
                if 0 <= x < FW and 0 <= y < FH: o[y, x, :3] = cs[by, bx]; o[y, x, 3] = 255
            res[(r, VIEWS[c])] = o
    return res
if __name__ == '__main__':
    out = {}
    for si, p in enumerate(sys.argv[1:], 1):
        res = extract(p)
        for r in range(ROWS):
            if (si, r) in SKIP and SKIP[(si, r)] is None: continue
            n = SKIP.get((si, r), (si - 1) * 4 + r)
            for v in VIEWS: out[f'{n}/{v}'] = res[(r, v)]
        print(p, 'ok')
    np.savez_compressed(os.path.join(HERE, 'hair_feats.npz'), **out); print(len(out) // 3, 'hairs')
