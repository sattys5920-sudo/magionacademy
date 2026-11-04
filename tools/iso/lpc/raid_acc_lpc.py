# 레이드 보스 기념품 아이콘 4 종을 LPC 부품에서 잘라 만들어요 (캐릭터 · 보스와 같은 화풍) → tools/raid_mock/raid_acc.png (32 칸 × 4)
#   0 얼음 왕관 (왕관) · 1 용 비늘 망토 (망토 뒷모습) · 2 그림자 모자 (마법사 모자) · 3 톱니 시계 목걸이 (사슬 + 둥근 장식)
#   python3 raid_acc_lpc.py <LPC 저장소 경로> [미리보기.png]
import sys, os, subprocess, colorsys
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import over, LPC, ROWS, FILES
ROOT = os.path.join(HERE, '..', '..', '..'); OUT = os.path.join(ROOT, 'tools', 'raid_mock', 'raid_acc.png')
OL = np.array([24, 16, 32, 255], np.uint8)
def frame(f, d='down', col=0):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS[d] * 64
    return a[y:y + 64, col * 64:col * 64 + 64]
def hueL(a, h, sat=1.0, val=1.0):
    out = a.copy()
    for y, x in zip(*np.nonzero(a[..., 3])):
        r, g, b, _ = a[y, x]; hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if vv < .16: continue
        ss = max(ss, .55)
        rr, gg, bb = colorsys.hsv_to_rgb(h, min(1, ss * sat), min(1, vv * val)); out[y, x, :3] = (int(rr * 255), int(gg * 255), int(bb * 255))
    return out
def tintL(a, c, k):
    out = a.copy().astype(float); m = a[..., 3] > 0
    lum = (out[..., 0] * .3 + out[..., 1] * .59 + out[..., 2] * .11) / 255
    for i in range(3): out[..., i] = np.where(m, out[..., i] * (1 - k) + c[i] * (.45 + lum) * k, out[..., i])
    return np.clip(out, 0, 255).astype(np.uint8)
def crop(a):
    ys, xs = np.nonzero(a[..., 3]); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def icon(a, extra=None, lim=28):
    a = crop(a); h, w = a.shape[:2]; s = max(1, min(lim // w, lim // h))
    a = np.kron(a, np.ones((s, s, 1), np.uint8)); h, w = a.shape[:2]
    c = np.zeros((32, 32, 4), np.uint8); y0, x0 = (32 - h) // 2, (32 - w) // 2; over(c[y0:y0 + h, x0:x0 + w], a)
    for y in range(32):   # 바깥 테두리 (LPC 아이템처럼)
        for x in range(32):
            if c[y, x, 3] == 0 and any(0 <= y + dy < 32 and 0 <= x + dx < 32 and c[y + dy, x + dx, 3] > 0 and not (c[y + dy, x + dx] == OL).all() for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))): c[y, x] = OL
    if extra: extra(c)
    return c
def P(c, pts, col):
    for x, y in pts:
        if 0 <= x < 32 and 0 <= y < 32: c[y, x] = col
F = {k: v for k, v in dict(
    crown='spritesheets/hat/formal/crown/adult/walk.png', cape_bg='spritesheets/cape/solid/bg/walk.png', cape_fg='spritesheets/cape/solid/fg/walk.png',
    hat='spritesheets/hat/magic/wizard/base/adult/walk.png', chain='spritesheets/neck/necklace/chain', charm='spritesheets/neck/charm/oval').items()}
def pick(p):
    if p.endswith('.png'): return p
    c = sorted(f for f in FILES if f.startswith(p + '/') and '/walk' in f and f.endswith('.png'))
    gold = [f for f in c if 'gold' in f]; return (gold or c)[0]
F = {k: pick(v) for k, v in F.items()}
need = [f for f in F.values() if not os.path.exists(os.path.join(LPC, f))]
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
# 0 얼음 왕관
cr = tintL(frame(F['crown']), (150, 215, 255), .85)
def ice_sp(c): P(c, [(6, 9), (25, 8), (27, 20)], np.array([255, 255, 255, 255], np.uint8)); P(c, [(5, 9), (7, 9), (6, 8), (6, 10)], np.array([190, 240, 255, 255], np.uint8))
I0 = icon(cr, lambda c: None, 32)
P(I0, [(3, 6), (28, 5), (29, 24), (2, 25)], np.array([255, 255, 255, 255], np.uint8))
# 1 용 비늘 망토 (뒷모습: 위쪽을 보는 칸)
cp = np.zeros((64, 64, 4), np.uint8); over(cp, frame(F['cape_bg'], 'up')); over(cp, frame(F['cape_fg'], 'up')); cp = hueL(cp, .01, 1.25, 1.05)
def scales(c):
    ys, xs = np.nonzero((c[..., 3] > 0) & ~(c == OL).all(-1))
    for y, x in zip(ys, xs):
        if (x + (y // 3) * 2) % 4 == 0 and y % 3 == 0: c[y, x, :3] = (255, 160, 110)
I1 = icon(cp, scales)
# 2 그림자 모자
I2 = icon(tintL(frame(F['hat']), (120, 70, 190), .8), lambda c: P(c, [(x, y) for x in range(12, 20) for y in (22,)], np.array([192, 138, 255, 255], np.uint8)))
# 3 톱니 시계 목걸이 (사슬 + 둥근 장식을 금빛으로, 장식에 시계 바늘)
nk = np.zeros((64, 64, 4), np.uint8); over(nk, frame(F['chain'])); over(nk, frame(F['charm'])); nk = tintL(nk, (232, 184, 88), .7)
def clockface(c):
    ys, xs = np.nonzero(c[..., 3] > 0); cx, cy = int(xs.mean()), int(ys.max()) - 5
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            d = dx * dx + dy * dy
            if d <= 20: c[cy + dy, cx + dx] = (184, 132, 46, 255) if d > 12 else (255, 244, 208, 255)
            elif d <= 26 and c[cy + dy, cx + dx, 3] == 0: c[cy + dy, cx + dx] = OL
    P(c, [(cx, cy), (cx, cy - 1), (cx, cy - 2), (cx + 1, cy), (cx + 2, cy)], np.array([60, 36, 12, 255], np.uint8))
    for a, b in ((0, -4), (4, 0), (0, 4), (-4, 0), (-3, -3), (3, -3), (3, 3), (-3, 3)):
        if a * a + b * b > 20: P(c, [(cx + a, cy + b)], np.array([232, 184, 88, 255], np.uint8))
I3 = icon(nk, clockface)
sheet = np.concatenate([I0, I1, I2, I3], axis=1); Image.fromarray(sheet).save(OUT); print('ok', OUT, F)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (128, 32), (52, 40, 76, 255)); pv.alpha_composite(Image.fromarray(sheet)); pv.resize((128 * 4, 128), Image.NEAREST).save(sys.argv[2])
