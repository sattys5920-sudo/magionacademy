# 새 직업 12 종 무기 × 강화 5 단계 (시안) → tools/newjobs/weapons_new.png · weapons_new_big.png · xw_new.json
#   python3 tools/newjobs/weapon_new.py <LPC 저장소 경로>
#   tools/iso/lpc/weapon_lpc.py 와 같은 방법(LPC 무기를 왼쪽 보는 칸에서 떼어 와 줄이고, 단계마다 금속 · 보석 색)으로 만들어요 · 총과 격투 장갑은 LPC 에 없어서 직접 찍어요
import sys, os, json, math, re
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); LPC = sys.argv[1]
src = open(os.path.join(ROOT, 'tools', 'iso', 'lpc', 'weapon_lpc.py'), encoding='utf-8').read()
# 원래 스크립트의 도구(frame · scale_about · fit_to · tier · 색 띠)만 가져와요
ns = {'np': np, 'Image': Image, 'os': os, 'colorsys': __import__('colorsys'), 'LPC': LPC, 'ROWS': {'down': 2, 'up': 0, 'left': 1, 'right': 3}}
exec(src[src.index('SCALE = .62'):src.index('\nneed = ')], ns); exec(re.search(r'^GEMC = .*$', src, re.M).group(0), ns); exec(re.search(r'^GLOW = .*$', src, re.M).group(0), ns)
for fn in ['frame', 'scale_about', 'fit_to', 'lerp_ramp', 'tier']:
    m = re.search(r'^def ' + fn + r'\(.*?(?=^\S)', src, re.S | re.M); exec(m.group(0), ns)
frame, scale_about, fit_to, tier, SCALE = ns['frame'], ns['scale_about'], ns['fit_to'], ns['tier'], ns['SCALE']
#   지금 직업 무기(도끼 · 단검 · 레이피어 · 롱소드 · 철퇴 · 둥근 방패 · 석궁 · 낫 · 지팡이 다섯 종)와 겹치지 않게 골랐어요
ORDER = ['paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer']
M = 'spritesheets/weapon/'; S_ = 'spritesheets/shield/'
W = {   # 직업: (동작 melee · bow · cast, 무기 층 파일 (없으면 직접 그림), 방패, 색 바꾸기)
 'paladin': ('melee', [M + 'blunt/flail/behind/walk/flail.png', M + 'blunt/flail/walk/flail.png'], S_ + 'crusader/fg/male/walk/crusader.png', None),   # 사슬철퇴 + 십자 방패
 'guardian': ('melee', [M + 'polearm/spear/background/walk/spear.png', M + 'polearm/spear/foreground/walk/spear.png'], S_ + 'kite/male/walk/kite.png', None),
 'darkknight': ('melee', [M + 'polearm/halberd/behind/walk/halberd.png', M + 'polearm/halberd/walk/halberd.png'], None, 'dark'),   # 검은 미늘창
 'dancer': ('cast', None, None, None),   # 부채 (직접)
 'sage': ('cast', [M + 'magic/gnarled/universal/background/walk/gnarled.png', M + 'magic/gnarled/universal/foreground/walk/gnarled.png'], None, None),
 'shaman': ('cast', None, None, None),   # 토템 지팡이 (직접)
 'miko': ('cast', [M + 'magic/crystal/universal/background/walk/crystal.png', M + 'magic/crystal/universal/foreground/walk/crystal.png'], None, 'red'),
 'archer': ('bow', [M + 'ranged/bow/recurve/walk/background/recurve.png', M + 'ranged/bow/recurve/walk/foreground/recurve.png'], None, None),
 'gunner': ('bow', None, None, None),
 'elemental': ('cast', [M + 'polearm/trident/background/walk/trident.png', M + 'polearm/trident/foreground/walk/trident.png'], None, None),
 'fighter': ('melee', None, None, None),
 'bladedancer': ('melee', [M + 'sword/saber/universal_behind/walk/saber.png', M + 'sword/saber/walk/saber.png'], None, None),
}
def find(f):   # 파일 이름이 저장소마다 조금씩 달라서, 없으면 같은 폴더의 첫 그림
    if os.path.exists(os.path.join(LPC, f)): return f
    d = os.path.dirname(f); fs = sorted(x for x in os.listdir(os.path.join(LPC, d)) if x.endswith('.png')) if os.path.isdir(os.path.join(LPC, d)) else []
    pref = [x for x in fs if x in ('foreground.png', 'background.png', 'steel.png', 'iron.png', 'brown.png', 'light.png')] or fs
    return os.path.join(d, pref[0]) if pref else None
def merge(files):
    base = np.zeros((64, 64, 4), np.uint8)
    for f in files:
        f = find(f)
        if not f: continue
        a = frame(f); al = a[..., 3:4] / 255.0; base[..., :3] = (a[..., :3] * al + base[..., :3] * (1 - al)).astype(np.uint8); base[..., 3] = np.maximum(base[..., 3], a[..., 3])
    return base
def recolor(a, mode):
    if not mode: return a
    import colorsys; o = a.copy(); H = {'dark': .78, 'pink': .92, 'green': .33, 'red': .0}[mode]
    for y in range(64):
        for x in range(64):
            r, g, b, al = a[y, x]
            if not al: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if mode == 'dark': v = v * .75
            o[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(H, max(s, .45), v)]
    return o
def px_draw(cells):   # 직접 찍는 무기: [(x, y, 색)]
    a = np.zeros((64, 64, 4), np.uint8)
    for x, y, c in cells: a[y, x] = (*c, 255)
    return a
def gun():   # 총잡이: 왼쪽을 겨누는 짧은 총 (손잡이는 오른쪽 아래)
    K, D, B, G = (34, 30, 40), (70, 66, 80), (120, 116, 130), (130, 86, 44); c = []
    for x in range(14, 31): c += [(x, 46, K), (x, 47, D if x > 16 else K), (x, 48, K)]
    for x in range(15, 30): c.append((x, 47, B if x % 3 else D))
    for x in range(26, 33): c += [(x, 49, K), (x, 50, G)]
    c += [(31, 51, K), (32, 51, G), (31, 52, K), (32, 52, G), (33, 52, K), (31, 53, K), (32, 53, K), (13, 46, K), (13, 47, K), (13, 48, K), (28, 45, K), (29, 45, B)]
    return px_draw(c)
def glove():   # 격투가: 손등 쇠붙이가 달린 장갑
    K, L, R, S = (40, 26, 18), (150, 80, 40), (190, 112, 56), (200, 204, 214); c = []
    for y in range(46, 53):
        for x in range(20, 27): c.append((x, y, K if x in (20, 26) or y in (46, 52) else (R if (x + y) % 3 else L)))
    for x in range(19, 25): c.append((x, 45, S))
    c += [(18, 46, S), (18, 47, S), (25, 54, K), (26, 54, K)]
    return px_draw(c)
def fan():   # 무희: 펼친 부채 (분홍 · 금빛 살)
    K, P, Q, G = (60, 24, 44), (240, 120, 170), (255, 178, 210), (230, 190, 90); c = []
    cx, cy = 26, 50
    for r in range(3, 11):
        for a in range(-60, 61, 6):
            t = math.radians(a + 150); x, y = int(round(cx + r * math.cos(t))), int(round(cy - r * math.sin(t) * .9))
            c.append((x, y, K if r == 10 else (G if a % 30 == 0 else (Q if r < 7 else P))))
    c += [(cx, cy, G), (cx + 1, cy, G), (cx + 1, cy + 1, K), (cx + 2, cy + 2, (200, 60, 90)), (cx + 2, cy + 3, (200, 60, 90))]
    return px_draw(c)
def totem():   # 주술사: 위에 새 얼굴 장식이 달린 나무 토템 지팡이
    K, W1, W2, R, Gr, Y = (40, 26, 18), (120, 80, 44), (160, 110, 60), (200, 60, 50), (80, 170, 90), (240, 200, 80); c = []
    for y in range(24, 58): c += [(24, y, K), (25, y, W1 if y % 4 else W2), (26, y, W2), (27, y, K)]
    for y in range(18, 26):
        for x in range(21, 31): c.append((x, y, K if x in (21, 30) or y in (18, 25) else (R if y < 21 else Gr if y < 23 else Y)))
    c += [(23, 20, (255, 255, 255)), (28, 20, (255, 255, 255)), (19, 21, (255, 220, 120)), (20, 22, (255, 220, 120)), (31, 22, (120, 200, 255)), (32, 21, (120, 200, 255)), (25, 26, Y), (26, 27, Y)]
    return px_draw(c)
def flail():   # 성기사: 손잡이 + 사슬 + 금빛 가시 철퇴알 (철퇴와 다른 모양)
    K, H1, H2, C, G1, G2, Wt = (40, 26, 18), (130, 86, 44), (176, 120, 62), (160, 164, 176), (200, 150, 40), (250, 214, 100), (255, 250, 220); c = []
    for i in range(12): x, y = 28 - i // 3, 54 - i; c += [(x, y, K), (x + 1, y, H1 if i % 2 else H2)]
    for i in range(6): c.append((24 - i // 2, 42 - i, C if i % 2 else K))
    for y in range(28, 36):
        for x in range(17, 25):
            d = (x - 20.5) ** 2 + (y - 31.5) ** 2
            if d <= 13: c.append((x, y, K if d > 9 else (G2 if (x + y) % 3 == 0 else G1)))
    c += [(20, 26, K), (20, 27, G2), (15, 31, K), (16, 31, G2), (25, 31, G2), (26, 31, K), (20, 36, G2), (20, 37, K), (19, 30, Wt), (20, 29, Wt)]
    return px_draw(c)
def bow():   # 궁수: 세로로 긴 활과 시위
    K, Wd, Wl, St = (40, 26, 18), (120, 76, 40), (176, 122, 66), (230, 230, 220); c = []
    for i in range(-14, 15):
        x = 22 - int(round(5 * math.cos(i / 14 * math.pi / 2))) ; y = 46 + i
        c += [(x, y, K), (x + 1, y, Wl if abs(i) < 10 else Wd)]
        c.append((24, y, St))
    c += [(23, 44, (90, 60, 30)), (23, 45, (90, 60, 30)), (23, 46, (90, 60, 30)), (23, 47, (90, 60, 30)), (23, 48, (90, 60, 30))]
    return px_draw(c)
def gohei():   # 무녀: 막대 끝에 하얀 종이 술 · 방울
    K, Wd, Wp, Gd = (40, 26, 18), (190, 70, 60), (255, 255, 250), (240, 200, 80); c = []
    for y in range(26, 56): c += [(24, y, K), (25, y, Wd)]
    for j, (x0, y0) in enumerate([(20, 24), (27, 24), (19, 30), (28, 30)]):
        for k in range(5): c.append((x0 + (k % 2) * (1 if j % 2 else -1), y0 + k, Wp if k % 2 == 0 else (220, 220, 230)))
    c += [(23, 22, Gd), (24, 21, Gd), (25, 21, Gd), (26, 22, Gd), (24, 22, K), (25, 23, Gd), (24, 23, Gd), (22, 34, Gd), (27, 34, Gd)]
    return px_draw(c)
def glove2():   # 격투가: 주먹 모양 장갑 · 손등 쇠붙이
    K, R1, R2, S1, S2 = (40, 22, 16), (176, 60, 44), (220, 96, 70), (180, 186, 200), (236, 240, 250); c = []
    rows = {44: (21, 27), 45: (20, 28), 46: (19, 28), 47: (19, 28), 48: (19, 28), 49: (20, 28), 50: (21, 27), 51: (22, 27), 52: (22, 27)}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1): c.append((x, y, K if x in (a, b) or y in (44, 52) else (R2 if (x + y) % 4 == 0 else R1)))
    for x in range(20, 28): c.append((x, 45, S2 if x % 2 else S1))
    c += [(19, 45, K), (28, 46, K), (21, 46, S1), (23, 46, S1), (25, 46, S1)]
    return px_draw(c)
def saber():   # 검무사: 살짝 휜 쌍칼 (레이피어 · 단검과 다른 모양)
    K, B1, B2, Hd, Gd = (40, 30, 40), (200, 210, 226), (246, 250, 255), (90, 50, 110), (230, 190, 80); c = []
    for i in range(18):
        x = 26 - i; y = 50 - i // 3 - int(round((i / 17) ** 2 * 4))
        c += [(x, y - 1, K), (x, y, B2 if i % 3 else B1), (x, y + 1, B1), (x, y + 2, K)]
    c += [(27, 48, Gd), (27, 49, Gd), (27, 50, Gd), (27, 51, Gd), (28, 49, Hd), (29, 50, Hd), (30, 51, Hd), (31, 52, K), (26, 48, K), (26, 52, K)]
    return px_draw(c)
sheet = np.zeros((64 * 12, 64 * 10, 4), np.uint8); XW = {}; comp = {}
for ji, job in enumerate(ORDER):
    kind, files, shf, rc = W[job]
    DR = { 'gunner': gun, 'fighter': glove2, 'dancer': fan, 'shaman': totem, 'paladin': flail, 'archer': bow, 'miko': gohei, 'bladedancer': saber }
    base = DR[job]() if job in DR else recolor(merge(files), rc)
    ys, xs = np.nonzero(base[..., 3] > 0)
    if len(ys) == 0: print('무기가 안 보여요:', job); continue
    low = ys >= np.percentile(ys, 75); px, py = int(xs[low].mean()), int(ys[low].mean())
    d = (xs - px) ** 2 + (ys - py) ** 2; k = int(d.argmax()); tx, ty = int(xs[k]), int(ys[k])
    DRAWN = { 'gunner': ((31, 52), (13, 47)), 'fighter': ((24, 50), (19, 45)), 'dancer': ((27, 51), (20, 41)), 'shaman': ((25, 56), (26, 18)), 'paladin': ((28, 54), (20, 31)), 'archer': ((23, 46), (17, 32)), 'miko': ((25, 55), (24, 21)), 'bladedancer': ((30, 51), (9, 41)) }   # 직접 그린 것: 손잡이 · 끝
    if job not in DRAWN: base = scale_about(base, (px, py), SCALE); tx, ty = int(round(px + (tx - px) * SCALE)), int(round(py + (ty - py) * SCALE))
    else: (px, py), (tx, ty) = DRAWN[job]
    ys2, xs2 = np.nonzero(base[..., 3] > 0); pts = np.stack([xs2, ys2], 1).astype(float); cen = pts.mean(0); _u, _s, vt = np.linalg.svd(pts - cen, full_matrices=False); pr = (pts - cen) @ vt[0]
    e0, e1 = pts[pr.argmin()], pts[pr.argmax()]; butt, head = (e0, e1) if np.hypot(*(e0 - cen)) > np.hypot(*(e1 - cen)) else (e1, e0)
    if job in ('bladedancer', 'gunner', 'fighter', 'dancer', 'shaman', 'paladin', 'archer', 'miko'): butt, head = np.array([px, py], float), np.array([tx, ty], float)
    grip = .5 if job == 'archer' else .05 if job in ('gunner', 'fighter', 'dancer') else .18
    gr = butt + (head - butt) * grip; gx, gy = int(round(gr[0])), int(round(gr[1])); phi0 = round(math.degrees(math.atan2(-(head[0] - gr[0]), -(head[1] - gr[1]))), 1)
    XW[job] = [px, py, tx, ty, kind, 1 if shf else 0, gx, gy, phi0]
    sh = None
    if shf:
        sh = fit_to(merge([shf]), 32, 38, 11); sy_, sx_ = np.nonzero(sh[..., 3] > 0); cx, cy = int(sx_.mean()), int(sy_.mean())
    for n in range(5):
        c = tier(base, n, (tx, ty), (px, py), kind); sheet[ji * 64:(ji + 1) * 64, n * 64:(n + 1) * 64] = c; cc = c.copy()
        if sh is not None:
            c2 = tier(sh, n, (cx, cy), (cx, cy), 'melee'); sheet[ji * 64:(ji + 1) * 64, (5 + n) * 64:(6 + n) * 64] = c2
            al = c2[..., 3:4] / 255.0; cc[..., :3] = (c2[..., :3] * al + cc[..., :3] * (1 - al)).astype(np.uint8); cc[..., 3] = np.maximum(cc[..., 3], c2[..., 3])
        comp[(ji, n)] = cc
Image.fromarray(sheet).save(os.path.join(HERE, 'weapons_new.png'))
big = Image.new('RGBA', (96 * 5, 96 * 12), (60, 70, 92, 255))
for ji in range(12):
    cells = [comp[(ji, n)] for n in range(5) if (ji, n) in comp]
    if not cells: continue
    ys, xs = np.nonzero(np.max([c[..., 3] for c in cells], axis=0) > 0); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; k = max(1, min(96 // (y1 - y0), 96 // (x1 - x0)))
    for n, c in enumerate(cells):
        im = Image.fromarray(c[y0:y1, x0:x1]).resize(((x1 - x0) * k, (y1 - y0) * k), Image.NEAREST); big.alpha_composite(im, (n * 96 + (96 - im.width) // 2, ji * 96 + (96 - im.height) // 2))
big.save(os.path.join(HERE, 'weapons_new_big.png'))
json.dump(XW, open(os.path.join(HERE, 'xw_new.json'), 'w')); print(json.dumps(XW))
