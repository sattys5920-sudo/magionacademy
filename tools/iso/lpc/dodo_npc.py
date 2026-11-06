# 도도 (새 NPC 시안): 생성 시트 tools/iso/npc_src/dodo.png → 64×64 칸 20개 (아래 · 위 · 왼쪽 · 오른쪽 × 서기 + 걷기 4)
#   생성 시트가 칸마다 보는 방향이 뒤섞여 있어서 쓸 칸을 직접 골라요: 앞 = 1줄 1·2칸 · 오른쪽 = 3줄 · 뒤 = 4줄 1·2칸 (5칸은 생성기 표시) · 왼쪽 = 오른쪽을 뒤집어요
#   키는 배트리 · 아울라(34)보다 작게 28
#   python3 dodo_npc.py <출력.png> [미리보기.png]
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_npcs as G
HEIGHT, FOOT = 28, 58
PICK = {'down': [(0, 0), (0, 1), (0, 0), (0, 1), (0, 0)], 'up': [(3, 0), (3, 1), (3, 0), (3, 1), (3, 0)], 'right': [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]}
a = np.array(Image.open(os.path.join(G.SRC, 'dodo.png')).convert('RGBA'))
def cut(c):   # 체크무늬 두 회색(약 122 · 180)만 배경으로 (도도 몸 회청색 · 검은 모자 · 흰 외알 안경은 남겨요)
    rgb = c[..., :3].astype(int); mx, mn = rgb.max(-1), rgb.min(-1)
    bg = (mx - mn <= 14) & (mx >= 95) & (mx <= 205)
    reg = np.zeros_like(bg); reg[0, :] = bg[0, :]; reg[-1, :] = bg[-1, :]; reg[:, 0] = bg[:, 0]; reg[:, -1] = bg[:, -1]
    while True:
        n = reg.copy(); n[1:] |= reg[:-1]; n[:-1] |= reg[1:]; n[:, 1:] |= reg[:, :-1]; n[:, :-1] |= reg[:, 1:]; n &= bg
        if (n == reg).all(): break
        reg = n
    out = c.copy(); out[..., 3] = np.where(reg, 0, 255); return out
C = [[cut(c) for c in r] for r in G.cells(a)]
b = G.bbox(C[0][0]); k = HEIGHT / (b[3] - b[1])
def place(src):
    bb = G.bbox(src); s = G.shrink(src[bb[1]:bb[3], bb[0]:bb[2]], k)
    f = np.zeros((64, 64, 4), np.uint8); h, w = s.shape[:2]; x0 = 32 - w // 2; y0 = FOOT - h
    f[y0:y0 + h, x0:x0 + w] = s; return f
F = {d: [place(C[r][c]) for r, c in L] for d, L in PICK.items()}
F['left'] = [f[:, ::-1].copy() for f in F['right']]
frames = [f for d in G.DIRS for f in F[d]]
strip = np.concatenate(frames, 1)
strip[..., :3] = np.array(Image.fromarray(strip[..., :3]).quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB'))
strip = np.concatenate([G.outline(strip[:, i * 64:(i + 1) * 64]) for i in range(20)], 1)
Image.fromarray(strip).save(sys.argv[1])
if len(sys.argv) > 2:   # 미리보기: 도도 옆에 배트리 · 아울라 (같은 배율)
    npcs = Image.open(os.path.join(HERE, '..', '..', '..', 'public', 'art', 'npcs.png'))
    pv = Image.new('RGBA', (64 * 7, 64), (60, 50, 80, 255)); im = Image.fromarray(strip)
    for j, i in enumerate((0, 10, 5, 15, 2)): pv.alpha_composite(im.crop((i * 64, 0, i * 64 + 64, 64)), (j * 64, 0))
    pv.alpha_composite(npcs.crop((0, 64, 64, 128)), (5 * 64, 0)); pv.alpha_composite(npcs.crop((0, 192, 64, 256)), (6 * 64, 0))
    pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(sys.argv[2])
