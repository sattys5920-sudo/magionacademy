# 탐사 직업 무기 12종 × 강화 5단계 → public/art/weapons.png (64칸, 가로 = 단계, 세로 = 직업) + index.html의 XW(손잡이 위치·끝 위치)
#   python3 weapon_lpc.py <LPC 저장소 경로> [미리보기.png]
#   LPC 무기를 왼쪽을 보고 서 있는 칸에서 떼어 내고(전투 화면에서 파티는 왼쪽을 봐요), 단계마다 금속·보석 색을 바꿔 칠해요
import sys, os, re, json, subprocess, colorsys
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import LPC, ROWS
ROOT = os.path.join(HERE, '..', '..', '..')
ORDER = ['warrior', 'black', 'thief', 'bard', 'time', 'alch', 'white', 'druid', 'cleric', 'knight', 'summon', 'gadget']
M = 'spritesheets/weapon/'
# 직업: (동작 종류 melee/bow/cast, 층 파일들 — 뒤에 깔리는 것부터)
W = {
 'warrior': ('melee', [M + 'blunt/waraxe/behind/walk/waraxe.png', M + 'blunt/waraxe/walk/waraxe.png'], None),
 'knight': ('melee', [M + 'sword/longsword/universal_behind/walk/longsword.png', M + 'sword/longsword/walk/longsword.png'], 'spritesheets/shield/round/walk.png'),
 'thief': ('melee', [M + 'sword/dagger/behind/walk/dagger.png', M + 'sword/dagger/walk/dagger.png'], None),
 'bard': ('melee', [M + 'sword/rapier/universal_behind/walk/rapier.png', M + 'sword/rapier/walk/rapier.png'], None),
 'cleric': ('melee', [M + 'blunt/mace/universal_behind/walk/mace.png', M + 'blunt/mace/walk/mace.png'], 'spritesheets/shield/round/walk.png'),
 'black': ('cast', [M + 'magic/s/universal/background/walk/s.png', M + 'magic/s/universal/foreground/walk/s.png'], None),
 'white': ('cast', [M + 'magic/simple/background/walk/simple.png', M + 'magic/simple/foreground/walk/simple.png'], None),
 'time': ('cast', [M + 'magic/loop/universal/background/walk/loop.png', M + 'magic/loop/universal/foreground/walk/loop.png'], None),
 'alch': ('cast', [M + 'magic/diamond/universal/background/walk/diamond.png', M + 'magic/diamond/universal/foreground/walk/diamond.png'], None),
 'druid': ('cast', [M + 'polearm/cane/male/walk/cane.png'], None),
 'summon': ('cast', [M + 'polearm/scythe/universal_behind/walk/scythe.png', M + 'polearm/scythe/walk/scythe.png'], None),
 'gadget': ('bow', [M + 'ranged/crossbow/background/walk/crossbow.png', M + 'ranged/crossbow/foreground/walk/crossbow.png'], None),
}
GRIP = {'warrior': .38, 'knight': .12, 'thief': .15, 'bard': .12, 'cleric': .25, 'black': .45, 'white': .45, 'time': .5, 'alch': .45, 'druid': .5, 'summon': .4, 'gadget': .5}   # 손잡이 위치: 무게 없는 끝에서 무거운 쪽으로 몇 %
SCALE = .74; SSCALE = .84     # 무기·방패 크기 (캐릭터에 비해 너무 커서 줄여요)
# 단계: 금속 색 띠(어두움→밝음), 보석 색 hue(0~1)
RAMP = [None,
 [(58, 36, 20), (122, 74, 34), (184, 122, 58), (224, 170, 102)],      # 청동
 [(44, 52, 68), (90, 106, 132), (154, 170, 196), (224, 234, 248)],    # 강철
 [(74, 52, 8), (160, 122, 24), (224, 184, 56), (255, 240, 160)],      # 황금
 [(20, 56, 80), (42, 120, 168), (90, 208, 232), (234, 252, 255)]]     # 미스릴
GEM = [None, .03, .58, .12, .5]
need = sorted({f for _, (k, L, sh) in W.items() for f in L + ([sh] if sh else []) if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS['left'] * 64
    return a[y:y + 64, 0:64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def scale_about(a, pv, sc):
    f = a.astype(np.float32); al = f[..., 3:4] / 255; pm = np.concatenate([f[..., :3] * al, f[..., 3:4]], axis=2)
    n = max(1, round(64 * sc)); chans = [np.array(Image.fromarray(np.clip(pm[..., k], 0, 255).astype(np.uint8)).resize((n, n), Image.LANCZOS)).astype(np.float32) for k in range(4)]
    out = np.stack(chans, axis=2); al2 = out[..., 3:4] / 255; rgb = np.where(al2 > .01, out[..., :3] / np.maximum(al2, .01), 0)
    res = np.zeros((64, 64, 4), np.uint8); crisp = np.where(out[..., 3] > 105, 255, 0)
    ox, oy = int(round(pv[0] - pv[0] * sc)), int(round(pv[1] - pv[1] * sc))
    for y in range(n):
        for x in range(n):
            if crisp[y, x] and 0 <= x + ox < 64 and 0 <= y + oy < 64: res[y + oy, x + ox] = (*np.clip(rgb[y, x], 0, 255).astype(np.uint8), 255)
    return res
def lerp_ramp(r, l):
    t = max(0, min(.999, l / 255)) * (len(r) - 1); i = int(t); f = t - i
    return [int(r[i][k] + (r[i + 1][k] - r[i][k]) * f) for k in range(3)]
GEMC = [None, (230, 70, 70), (90, 150, 255), (255, 214, 70), (130, 255, 240)]       # 단계 보석·빛 색
GLOW = [None, None, (200, 220, 255), (255, 214, 70), (110, 240, 255)]
def tier(a, n, tip, hilt, kind):
    if n == 0: return a.copy()
    o = a.copy(); H, Wd = a.shape[:2]
    for y in range(H):
        for x in range(Wd):
            r, g, b, al = a[y, x]
            if not al: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < .3 or (.03 < h < .16): o[y, x, :3] = lerp_ramp(RAMP[n], .299 * r + .587 * g + .114 * b)    # 금속·나무 손잡이 전부 단계 색으로
            else: o[y, x, :3] = [int(c * 255) for c in colorsys.hsv_to_rgb(GEM[n], min(1, s + .1), v)]   # 보석
    m = o[..., 3] > 0
    def ring(mask):
        d = np.zeros_like(mask)
        d[1:] |= mask[:-1]; d[:-1] |= mask[1:]; d[:, 1:] |= mask[:, :-1]; d[:, :-1] |= mask[:, 1:]
        return d & ~mask
    if n >= 2:      # 빛나는 테두리 (모양이 커 보이게)
        r1 = ring(m); c = GLOW[n]; o[r1] = (*c, 200 if n == 2 else 235)
        if n == 4: r2 = ring(m | r1); o[r2] = (*c, 90)
    gx, gy = (tip if kind == 'cast' else hilt); rad = [0, 1, 2, 2, 3][n]; gc = GEMC[n]    # 보석: 마법 지팡이는 끝에, 나머지는 손잡이 끝에
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            if abs(dx) + abs(dy) <= rad and 0 <= gx + dx < 64 and 0 <= gy + dy < 64: o[gy + dy, gx + dx] = (*gc, 255)
    if rad >= 1 and 0 <= gx - 1 < 64 and 0 <= gy - 1 < 64: o[gy - 1, gx - 1] = (255, 255, 255, 255)
    if n >= 3:      # 반짝이
        for sx, sy in ((tip[0] + 3, tip[1] - 3), (tip[0] - 3, tip[1] - 1), (tip[0] + 1, tip[1] - 5))[:n - 1]:
            if 1 <= sx < 63 and 1 <= sy < 63:
                for ddx, ddy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): o[sy + ddy, sx + ddx] = (255, 255, 255, 255 if (ddx, ddy) == (0, 0) else 170)
    return o
sheet = np.zeros((64 * 12, 64 * 10, 4), np.uint8); XW = {}; comp = {}
def merge(files):
    base = np.zeros((64, 64, 4), np.uint8)
    for f in files:
        a = frame(f); al = a[..., 3:4] / 255.0; base[..., :3] = (a[..., :3] * al + base[..., :3] * (1 - al)).astype(np.uint8); base[..., 3] = np.maximum(base[..., 3], a[..., 3])
    return base
for ji, job in enumerate(ORDER):
    kind, files, shf = W[job]; base = merge(files)
    ys, xs = np.nonzero(base[..., 3] > 0)
    if len(ys) == 0: print('무기가 안 보여요:', job); XW[job] = [32, 40, 20, 20, kind, 0]; continue
    low = ys >= np.percentile(ys, 75); px, py = int(xs[low].mean()), int(ys[low].mean())     # 손잡이(아래쪽)
    d = (xs - px) ** 2 + (ys - py) ** 2; k = int(d.argmax()); tx, ty = int(xs[k]), int(ys[k])    # 끝
    base = scale_about(base, (px, py), SCALE); tx, ty = int(round(px + (tx - px) * SCALE)), int(round(py + (ty - py) * SCALE))
    ys2, xs2 = np.nonzero(base[..., 3] > 0); pts = np.stack([xs2, ys2], 1).astype(float); cen = pts.mean(0); u_, s_, vt = np.linalg.svd(pts - cen, full_matrices=False); ax = vt[0]; pr = (pts - cen) @ ax
    e0, e1 = pts[pr.argmin()], pts[pr.argmax()]; butt, head = (e0, e1) if np.hypot(*(e0 - cen)) > np.hypot(*(e1 - cen)) else (e1, e0)
    if job in ('knight', 'thief', 'bard'): butt, head = np.array([px, py], float), np.array([tx, ty], float)   # 검: 끝(날) 반대쪽이 손잡이
    gr = butt + (head - butt) * GRIP[job]; gx, gy = int(round(gr[0])), int(round(gr[1]))
    XW[job] = [px, py, tx, ty, kind, 1 if shf else 0, gx, gy]
    sh = None
    if shf:
        sh = merge([shf]); sy_, sx_ = np.nonzero(sh[..., 3] > 0); cx, cy = int(sx_.mean()), int(sy_.mean()); sh = scale_about(sh, (cx, cy), SSCALE)
    for n in range(5):
        c = tier(base, n, (tx, ty), (px, py), kind); sheet[ji * 64:(ji + 1) * 64, n * 64:(n + 1) * 64] = c; cc = c.copy()
        if sh is not None:
            c2 = tier(sh, n, (cx, cy), (cx, cy), 'melee'); sheet[ji * 64:(ji + 1) * 64, (5 + n) * 64:(6 + n) * 64] = c2
            al = c2[..., 3:4] / 255.0; cc[..., :3] = (c2[..., :3] * al + cc[..., :3] * (1 - al)).astype(np.uint8); cc[..., 3] = np.maximum(cc[..., 3], c2[..., 3])
        comp[(ji, n)] = cc
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'weapons.png'))
big = Image.new('RGBA', (96 * 5, 96 * 12), (0, 0, 0, 0))
for ji in range(12):
    cells = [comp[(ji, n)] for n in range(5)]; ys, xs = np.nonzero(np.max([c[..., 3] for c in cells], axis=0) > 0)
    if len(ys) == 0: continue
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; k = max(1, min(96 // (y1 - y0), 96 // (x1 - x0)))
    for n, c in enumerate(cells):
        im = Image.fromarray(c[y0:y1, x0:x1]).resize(((x1 - x0) * k, (y1 - y0) * k), Image.NEAREST); big.alpha_composite(im, (n * 96 + (96 - im.width) // 2, ji * 96 + (96 - im.height) // 2))
big.save(os.path.join(ROOT, 'public', 'art', 'weapons_big.png'))
p = os.path.join(ROOT, 'public', 'index.html'); s = open(p, encoding='utf-8').read(); js = 'const XW = ' + json.dumps(XW, separators=(',', ':')) + ';'
if '/*XW*/' in s: s = re.sub(r'/\*XW\*/.*?/\*XW-END\*/', lambda m: '/*XW*/' + js + '/*XW-END*/', s, flags=re.S)
else: s = s.replace('const xRand = a =>', '/*XW*/' + js + '/*XW-END*/\nconst xRand = a =>', 1)
open(p, 'w', encoding='utf-8').write(s)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * 10, 64 * 12), (70, 80, 100, 255)); pv.alpha_composite(Image.fromarray(sheet)); pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[2])
print(XW)
