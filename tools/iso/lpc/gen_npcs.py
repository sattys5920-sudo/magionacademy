# 생성형으로 뽑은 NPC 시트(tools/iso/npc_src/*.png, 5칸 × 4줄: 아래·왼쪽·오른쪽·위 × [서기, 걷기 4])를 게임 칸으로
#   - 가짜 체크무늬·마젠타 배경: 칸 테두리에서부터 무채색·마젠타를 채워서 지워요 (캐릭터 외곽선에서 멈춰요)
#   - 오른쪽 아래 칸은 생성기 표시(✦)가 있어서 안 써요 (뒷모습 걷기는 다른 칸으로)
#   - 시트마다 한 배율로 줄여서 64×64 칸에 (캐릭터와 같은 픽셀 크기), 색 수 줄이고 외곽선 정리
#   npc_lpc.py가 불러서 public/art/npcs.png의 해당 줄을 덮어써요
import os
import numpy as np
from PIL import Image
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'npc_src')
# 이름: (npcs.png 줄, 서 있을 때 키(px), 발 높이 y, 뒷모습 줄에 쓸 칸 [서기, 걷기 4])
GEN = {
 'nabi':   (0, 36, 58, [0, 1, 2, 3, 1]),
 'batri':  (1, 34, 52, [0, 1, 2, 3, 2]),
 'kappa':  (2, 40, 58, [0, 1, 2, 3, 1]),
 'aula':   (3, 34, 58, [1, 1, 1, 1, 1]),   # 부엉이 뒷줄은 2번 칸만 진짜 뒷모습
 'mandi':  (4, 34, 58, [0, 1, 2, 3, 1]),
 'jipsin': (5, 42, 58, [0, 1, 2, 3, 1]),
}
GROW = {'down': 0, 'left': 1, 'right': 2, 'up': 3}   # 생성 시트의 줄
DIRS = ['down', 'up', 'left', 'right']              # 게임 칸 순서
def cells(a):
    H, W = a.shape[:2]; ch, cw = H / 4, W / 5
    return [[a[int(r * ch) + 2:int((r + 1) * ch) - 2, int(c * cw) + 2:int((c + 1) * cw) - 2] for c in range(5)] for r in range(4)]
def cut_bg(c):
    rgb = c[..., :3].astype(int); mx, mn = rgb.max(-1), rgb.min(-1)
    r_, g_, b_ = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    bg = ((mx - mn <= 24) & (mx >= 45)) | ((r_ > 170) & (b_ > 150) & (g_ < 130)) | ((r_ - g_ > 25) & (b_ - g_ > 20) & (np.abs(r_ - b_) < 40) & (g_ > 90))   # 무채색 · 마젠타 · 마젠타가 번진 체크무늬
    reg = np.zeros_like(bg); reg[0, :] = bg[0, :]; reg[-1, :] = bg[-1, :]; reg[:, 0] = bg[:, 0]; reg[:, -1] = bg[:, -1]
    while True:   # 테두리에서 이어진 배경만
        n = reg.copy()
        n[1:] |= reg[:-1]; n[:-1] |= reg[1:]; n[:, 1:] |= reg[:, :-1]; n[:, :-1] |= reg[:, 1:]
        n &= bg
        if (n == reg).all(): break
        reg = n
    out = c.copy(); out[..., 3] = np.where(reg, 0, 255)
    # 배경과 맞닿은 밝은 무채색 테두리 찌꺼기 한 겹 더
    m = out[..., 3] > 0; edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    out[edge & bg, 3] = 0
    return out
def bbox(c):
    ys, xs = np.nonzero(c[..., 3] > 0)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(ys) else None
def shrink(c, k):
    """RGBA를 k배로 줄여요: 색은 불투명 칸끼리만 평균, 반 넘게 차면 칸으로"""
    h, w = c.shape[:2]; H, W = max(1, round(h * k)), max(1, round(w * k))
    a = c[..., 3:4].astype(float) / 255; pm = (c[..., :3] * a).astype(np.float32)
    P = np.array(Image.fromarray(np.concatenate([pm, a * 255], -1).astype(np.uint8), 'RGBA').resize((W, H), Image.BOX)).astype(float)
    al = P[..., 3:4] / 255; col = np.where(al > 0, P[..., :3] / np.maximum(al, 1e-3), 0)
    out = np.zeros((H, W, 4), np.uint8); out[..., :3] = np.clip(col, 0, 255); out[..., 3] = np.where(al[..., 0] >= .45, 255, 0)
    return out
def outline(f):
    m = f[..., 3] > 0; o = f.copy()
    for y in range(64):
        for x in range(64):
            if m[y, x]: continue
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < 64 and 0 <= xx < 64 and m[yy, xx]:
                    c = f[yy, xx, :3].astype(int)
                    if c.max() > 70: o[y, x, :3] = (c * .3).astype(np.uint8); o[y, x, 3] = 255
                    break
    return o
def build(name):
    row, height, foot, upcols = GEN[name]
    a = np.array(Image.open(os.path.join(SRC, name + '.png')).convert('RGBA'))
    C = [[cut_bg(c) for c in r] for r in cells(a)]
    b = bbox(C[0][0]); k = height / (b[3] - b[1])
    frames = []
    for d in DIRS:
        r = GROW[d]; idx = upcols if d == 'up' else [0, 1, 2, 3, 4]
        for ci in idx:
            src = C[r][ci]; bb = bbox(src)
            s = shrink(src[bb[1]:bb[3], bb[0]:bb[2]], k)
            f = np.zeros((64, 64, 4), np.uint8); h, w = s.shape[:2]
            x0 = 32 - w // 2; y0 = foot - h
            ys, xs = slice(max(0, y0), min(64, y0 + h)), slice(max(0, x0), min(64, x0 + w))
            f[ys, xs] = s[max(0, -y0):max(0, -y0) + (ys.stop - ys.start), max(0, -x0):max(0, -x0) + (xs.stop - xs.start)]
            frames.append(f)
    # 옆모습 정리: 왼쪽 서기 칸을 기준으로, 반대로 선 칸은 뒤집고 앞모습 칸은 이웃 칸으로. 오른쪽은 왼쪽을 뒤집어요
    iou = lambda p, q: ((p[..., 3] > 0) & (q[..., 3] > 0)).sum() / max(1, ((p[..., 3] > 0) | (q[..., 3] > 0)).sum())
    L0, D0 = frames[10], frames[0]; left = [L0]
    for f in frames[11:15]:
        fl = f[:, ::-1]; a_, b_, c_ = iou(f, L0), iou(fl, L0), iou(f, D0)
        if c_ > max(a_, b_) + .05: f = left[-1]
        elif b_ > a_: f = fl
        left.append(f)
    frames[10:15] = left; frames[15:20] = [f[:, ::-1].copy() for f in left]
    strip = np.concatenate(frames, 1)
    # 색 수 줄이기 (시트 하나에 32색)
    rgb = Image.fromarray(strip[..., :3]).quantize(32, method=Image.Quantize.MEDIANCUT).convert('RGB')
    strip[..., :3] = np.array(rgb)
    return row, np.concatenate([outline(strip[:, i * 64:(i + 1) * 64]) for i in range(20)], 1)
def all_gen():
    return [build(n) for n in GEN if os.path.exists(os.path.join(SRC, n + '.png'))]
if __name__ == '__main__':
    import sys
    rows = all_gen(); pv = Image.new('RGBA', (64 * 20, 64 * len(rows)), (250, 241, 226, 255))
    for i, (r, s) in enumerate(rows): pv.alpha_composite(Image.fromarray(s), (0, i * 64))
    pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[1])
