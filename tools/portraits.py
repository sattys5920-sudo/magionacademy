# 메인 주인공 초상화: tools/portraits_src/<id>_<표정>.webp (생성형, 흰 배경) → public/art/portraits/<id>.png
#   흰 배경을 가장자리부터 지우고(flood fill), 생성기 표시(✦)가 있는 오른쪽 아래 구석은 비우고,
#   원래 픽셀 크기로 줄여서(한 픽셀 = 블록의 가운데 색) 5칸 가로 시트로: neutral, happy, angry, surprised, shy
import os, sys
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(D, 'portraits_src'); OUT = os.path.join(D, '..', 'public', 'art', 'portraits')
FACES = ['neutral', 'happy', 'angry', 'surprised', 'shy']
def block_size(a):
    # 가로 줄에서 색이 바뀌는 간격의 최빈값 → 원래 픽셀 하나의 크기
    g = a[..., :3].astype(int).sum(-1); runs = []
    for y in range(0, a.shape[0], 37):
        row = g[y]; ch = np.nonzero(np.abs(np.diff(row)) > 40)[0]
        runs += list(np.diff(ch))
    runs = [r for r in runs if 3 <= r <= 16]
    return max(set(runs), key=runs.count) if runs else 8
def cut(a):
    rgb = a[..., :3].astype(int); white = (rgb.min(-1) > 225) & (rgb.max(-1) - rgb.min(-1) < 25)
    reg = np.zeros_like(white); reg[0, :] = white[0, :]; reg[-1, :] = white[-1, :]; reg[:, 0] = white[:, 0]; reg[:, -1] = white[:, -1]
    while True:
        n = reg.copy(); n[1:] |= reg[:-1]; n[:-1] |= reg[1:]; n[:, 1:] |= reg[:, :-1]; n[:, :-1] |= reg[:, 1:]; n &= white
        if (n == reg).all(): break
        reg = n
    out = np.dstack([a[..., :3], np.where(reg, 0, 255).astype(np.uint8)])
    return out
def build(pid):
    imgs = []
    for f in FACES:
        p = os.path.join(SRC, f'{pid}_{f}.webp')
        if not os.path.exists(p): return None
        imgs.append(np.array(Image.open(p).convert('RGB')))
    k = block_size(imgs[0]); H, W = imgs[0].shape[:2]; h, w = H // k, W // k
    cells = []
    for a in imgs:
        a = cut(a)
        # 오른쪽 아래 생성기 표시 지우기 (몸통 바깥 투명한 곳만이 아니라 표시 크기만큼)
        small = a[k // 2::k, k // 2::k][:h, :w].copy()
        for _ in range(3):   # 외곽의 흰 찌꺼기(배경과 맞닿은 밝은 점) 지우기
            al = small[..., 3] > 0; rgb = small[..., :3].astype(int)
            edge = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
            light = (rgb.min(-1) > 200) & (rgb.max(-1) - rgb.min(-1) < 40)
            small[edge & light, 3] = 0
        # 생성기 표시(✦): 오른쪽 아래 구석의 회백색 작은 점들
        cy, cx = int(h * .82), int(w * .78); blk = small[cy:, cx:]; rgb = blk[..., :3].astype(int)
        mark = (rgb.min(-1) > 150) & (rgb.max(-1) - rgb.min(-1) < 30)
        if 0 < mark.sum() < 60:   # 몸통 색으로 채워요 (이웃 평균)
            ys, xs = np.nonzero(mark)
            for y, x in zip(ys, xs):
                nb = [blk[yy, xx, :3] for yy, xx in ((y, x - 3), (y, x + 3), (y - 3, x), (y + 3, x)) if 0 <= yy < blk.shape[0] and 0 <= xx < blk.shape[1] and not mark[yy, xx] and blk[yy, xx, 3]]
                if nb: blk[y, x, :3] = np.mean(nb, 0)
        cells.append(small)
    sheet = np.concatenate(cells, 1)
    Image.fromarray(sheet, 'RGBA').save(os.path.join(OUT, f'{pid}.png'))
    return k, w, h
if __name__ == '__main__':
    for pid in sys.argv[1:] or ['lucian', 'boo', 'hazel', 'wolfgang', 'mirabel', 'frankie', 'jack']:
        r = build(pid); print(pid, r)
