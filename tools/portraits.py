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
# 가장자리에서 안 닿는 갇힌 배경(볼트와 목 사이 등): 그 안의 한 점을 (가로, 세로) 비율로 적어 두면 거기서도 지워요
HOLES = {'frankie': [(.324, .576), (.675, .576)]}
# 한 표정만 확대돼서 뽑혔을 때: 그 표정을 (배율, 왼쪽, 위)로 줄여 옮기고, 모든 표정을 같이 잘라요 (왼, 위, 오른, 아래)
FIT = {'boo': {'happy': (.83, 59, 71)}}
CROP = {'boo': (66, 0, 798, 1062)}
def fit(a, t):
    s, dx, dy = t; H, W = a.shape[:2]
    im = Image.fromarray(a).resize((round(W * s), round(H * s)), Image.NEAREST)
    c = Image.new('RGB', (W, H), (255, 255, 255)); c.paste(im, (dx, dy)); return np.array(c)
def cut(a, pid=None):
    rgb = a[..., :3].astype(int); white = (rgb.min(-1) > 225) & (rgb.max(-1) - rgb.min(-1) < 25)
    reg = np.zeros_like(white); reg[0, :] = white[0, :]; reg[-1, :] = white[-1, :]; reg[:, 0] = white[:, 0]; reg[:, -1] = white[:, -1]
    for fx, fy in HOLES.get(pid, []):
        y, x = int(fy * a.shape[0]), int(fx * a.shape[1]); reg[y, x] = white[y, x]
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
        a = np.array(Image.open(p).convert('RGB'))
        if f in FIT.get(pid, {}): a = fit(a, FIT[pid][f])
        if pid in CROP: x0, y0, x1, y1 = CROP[pid]; a = a[y0:y1, x0:x1]
        imgs.append(a)
    k = block_size(imgs[0]); H, W = imgs[0].shape[:2]; h, w = H // k, W // k
    cells = []
    for a in imgs:
        a = cut(a, pid)
        # 오른쪽 아래 생성기 표시 지우기 (몸통 바깥 투명한 곳만이 아니라 표시 크기만큼)
        small = a[k // 2::k, k // 2::k][:h, :w].copy()
        for _ in range(3):   # 외곽의 흰 찌꺼기(배경과 맞닿은 밝은 점) 지우기
            al = small[..., 3] > 0; rgb = small[..., :3].astype(int); pa = np.pad(al, 1, constant_values=True)   # 그림 밖은 막힌 것으로 (잘린 몸통 아래쪽을 지우지 않게)
            edge = al & ~(pa[:-2, 1:-1] & pa[2:, 1:-1] & pa[1:-1, :-2] & pa[1:-1, 2:])
            light = (rgb.min(-1) > 200) & (rgb.max(-1) - rgb.min(-1) < 40)
            small[edge & light, 3] = 0
        for _ in range(2):   # 외곽선 밖의 회색 번짐 점: 둘레에 비슷한 회색이 거의 없는 무채색 점
            al = small[..., 3] > 0; rgb = small[..., :3].astype(int); lum = rgb.mean(-1); sat = rgb.max(-1) - rgb.min(-1)
            pa = np.pad(al, 1, constant_values=True); edge = al & ~(pa[:-2, 1:-1] & pa[2:, 1:-1] & pa[1:-1, :-2] & pa[1:-1, 2:])
            gray = al & (sat < 14) & (lum > 110); sim = np.zeros(al.shape, int)
            pl, pg = np.pad(lum, 1), np.pad(gray, 1)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy or dx:
                        nl = pl[1 + dy:pl.shape[0] - 1 + dy, 1 + dx:pl.shape[1] - 1 + dx]; ng = pg[1 + dy:pg.shape[0] - 1 + dy, 1 + dx:pg.shape[1] - 1 + dx]
                        sim += ng & (np.abs(nl - lum) < 30)
            small[edge & gray & (sim < 2), 3] = 0
        # 생성기 표시(✦, 오른쪽 아래 어두운 옷 위의 회색 별): 둘레보다 밝은 점을 둘레 색으로
        y0, y1, x0, x1 = int(h * .855), int(h * .945), int(w * .82), int(w * .91)
        box = small[y0:y1, x0:x1]; lum = box[..., :3].astype(int).mean(-1); med = np.median(lum[box[..., 3] > 0]) if (box[..., 3] > 0).any() else 255
        if med < 90:
            fill = np.median(box[..., :3][(box[..., 3] > 0) & (lum <= med + 15)], 0)
            box[(lum > med + 25) & (box[..., 3] > 0), :3] = fill
        elif med >= 150 and (np.abs(lum - med) <= 3).mean() > .6:   # 밝고 고른 옷 위의 흰 별
            fill = np.median(box[..., :3][(box[..., 3] > 0) & (np.abs(lum - med) <= 3)], 0)
            box[(lum > med + 8) & (box[..., 3] > 0), :3] = fill
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
