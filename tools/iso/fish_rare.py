# 희귀 물고기 40종: 기존 물고기 그림(fish.png 앞 60칸)을 바탕으로 색을 바꾸고 빛·반짝이·불꽃을 덧그려요
# python3 tools/iso/fish_rare.py [미리보기.png]
#   → public/art/fish.png 를 63칸(물고기 60 + 쓰레기 3) 뒤에 40칸을 붙여 103칸으로 만들어요 (이미 103칸이면 앞 63칸만 쓰고 다시 만들어요)
#   칸 순서 = 게임의 RARE_FISH 순서 (index.html FISH_LIST 61~100번)
import os, sys, colorsys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 32
OUT = (26, 16, 36)
PAL = {
  'gold':    [(120, 70, 20), (200, 140, 30), (255, 206, 70), (255, 240, 170)],
  'shadow':  [(30, 20, 50), (62, 42, 96), (104, 74, 150), (176, 146, 226)],
  'frost':   [(40, 90, 150), (90, 170, 220), (170, 225, 250), (240, 252, 255)],
  'jade':    [(20, 80, 60), (40, 150, 100), (110, 210, 150), (200, 250, 210)],
  'sakura':  [(150, 60, 100), (230, 120, 160), (255, 180, 205), (255, 232, 242)],
  'abyss':   [(12, 22, 64), (32, 54, 128), (64, 116, 206), (156, 206, 255)],
  'lava':    [(110, 24, 12), (210, 72, 24), (255, 152, 44), (255, 232, 124)],
  'crimson': [(90, 12, 32), (170, 32, 52), (232, 74, 84), (255, 176, 176)],
  'pearl':   [(118, 118, 150), (190, 190, 216), (236, 236, 250), (255, 255, 255)],
}
GLOW = {'gold': (255, 214, 92), 'shadow': (170, 120, 255), 'frost': (160, 230, 255), 'jade': (120, 240, 170), 'sakura': (255, 170, 210),
        'abyss': (90, 160, 255), 'lava': (255, 130, 50), 'crimson': (255, 80, 90), 'pearl': (240, 240, 255), 'rainbow': (255, 240, 200)}
# [바탕 물고기 칸, 색, 효과]  — index.html 의 RARE 순서와 같아요
RARE = [
  (0,'gold','spark'), (1,'shadow','glow'), (5,'frost','spark'), (3,'rainbow','spark'), (4,'jade','glow'),
  (6,'frost','glow'), (7,'sakura','spark'), (8,'abyss','spark'), (9,'lava','glow'), (10,'gold','spark'),
  (11,'abyss','glow'), (12,'crimson','spark'), (13,'pearl','glow'), (14,'rainbow','glow'), (15,'crimson','glow'),
  (16,'abyss','spark'), (17,'pearl','spark'), (18,'lava','flame'), (19,'jade','spark'), (20,'shadow','spark'),
  (21,'gold','glow'), (22,'sakura','spark'), (23,'frost','glow'), (24,'lava','spark'), (25,'pearl','glow'),
  (26,'frost','spark'), (28,'shadow','glow'), (29,'gold','flame'), (30,'abyss','glow'), (31,'rainbow','spark'),
  (36,'frost','glow'), (37,'lava','spark'), (39,'pearl','spark'), (44,'rainbow','glow'), (46,'shadow','spark'),
  (48,'gold','glow'), (49,'lava','flame'), (54,'abyss','flame'), (58,'shadow','flame'), (59,'gold','flame'),
]

def lum(c): return .299 * c[0] + .587 * c[1] + .114 * c[2]

def recolor(cell, pal):
    im = cell.copy(); px = im.load()
    ys = [y for y in range(N) for x in range(N) if px[x, y][3] > 0]
    for y in range(N):
        for x in range(N):
            r, g, b, a = px[x, y]
            if a == 0: continue
            if (r, g, b) == OUT: continue
            L = lum((r, g, b)); s = max(r, g, b) - min(r, g, b)
            if L < 34 or (L > 238 and s < 20): continue          # 눈·반짝 하이라이트는 그대로
            t = min(.999, max(0, (L - 34) / 205))
            if pal == 'rainbow':
                h = (x / N * .85 + y / N * .15) % 1
                rr, gg, bb = colorsys.hls_to_rgb(h, .32 + t * .5, .75)
                px[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
            else:
                P = PAL[pal]; k = t * 3; i = min(2, int(k)); f = k - i
                c = tuple(int(P[i][j] + (P[i + 1][j] - P[i][j]) * f) for j in range(3))
                px[x, y] = c + (a,)
    return im

def body_mask(im):
    px = im.load(); return {(x, y) for y in range(N) for x in range(N) if px[x, y][3] > 0}

def glow(im, col):
    m = body_mask(im); px = im.load()
    for (x, y) in list(m):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < N and 0 <= p[1] < N and p not in m and px[p][3] == 0:
                px[p] = col + (150,)
    return im

def spark(im, col):
    m = body_mask(im); px = im.load()
    spots = [(3, 3), (28, 4), (27, 27), (4, 26), (16, 2), (29, 15)]
    n = 0
    for (x, y) in spots:
        if n >= 3: break
        if any((x + dx, y + dy) in m for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)): continue
        px[x, y] = (255, 255, 240, 255)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): px[x + dx, y + dy] = col + (230,)
        n += 1
    return im

def flame(im, col):
    im = glow(im, col); m = body_mask(im); px = im.load()
    top = {}
    for (x, y) in m: top[x] = min(top.get(x, 99), y)
    xs = sorted(top)
    for i, x in enumerate(xs[2:-2:3]):
        y0 = top[x] - 1; h = 2 + (i % 2)
        for k in range(h):
            yy = y0 - k
            if yy < 0: break
            c = (255, 236, 140) if k == 0 else col
            if px[x, yy][3] == 0: px[x, yy] = c + (255 if k == 0 else 200,)
    return im

def build():
    path = os.path.join(ROOT, 'public', 'art', 'fish.png')
    src = Image.open(path).convert('RGBA')
    base = src.crop((0, 0, 63 * N, N))
    out = Image.new('RGBA', ((63 + len(RARE)) * N, N), (0, 0, 0, 0)); out.paste(base, (0, 0))
    for k, (bi, pal, fx) in enumerate(RARE):
        cell = recolor(base.crop((bi * N, 0, bi * N + N, N)), pal)
        cell = {'glow': glow, 'spark': spark, 'flame': flame}[fx](cell, GLOW[pal])
        out.paste(cell, ((63 + k) * N, 0), cell)
    out.save(path); return out

if __name__ == '__main__':
    sh = build(); print('저장', sh.size)
    if len(sys.argv) > 1:
        per = 10; sc = 3; rows = (len(RARE) + per - 1) // per
        pv = Image.new('RGBA', (per * (N * sc + 6), rows * (N * sc + 6)), (33, 23, 51, 255))
        for k in range(len(RARE)):
            c = sh.crop(((63 + k) * N, 0, (64 + k) * N, N)).resize((N * sc, N * sc), Image.NEAREST)
            pv.paste(c, ((k % per) * (N * sc + 6) + 3, (k // per) * (N * sc + 6) + 3), c)
        pv.save(sys.argv[1])
