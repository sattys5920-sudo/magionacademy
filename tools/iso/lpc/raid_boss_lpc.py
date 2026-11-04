# 레이드 보스 4 종을 LPC 부품으로 조립해요 (탐사 몬스터 monster_lpc.py와 같은 화풍) → tools/raid_mock/raid_bosses.png
#   칸 64 × 64, 보스마다 2 칸: 0 가만히 (걷기 · 정면) · 1 기술 준비 (주문 · 팔을 든 정면)
#   LPC에 없는 것(얼음 수정 · 시계판 · 톱니)은 같은 화풍(LPC 팔레트 · 검은 테두리)으로 덧그려요
#   python3 raid_boss_lpc.py <LPC 저장소 경로> [미리보기.png]
import sys, os, json, subprocess, colorsys, math
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc
from npc_lpc import find, recolor, over, LPC, ROWS, FILES
npc_lpc.PAL['metal'] = json.load(open(os.path.join(LPC, 'palette_definitions', 'metal', 'metal_ulpc.json')))
ROOT = os.path.join(HERE, '..', '..', '..'); OUT = os.path.join(ROOT, 'tools', 'raid_mock', 'raid_bosses.png')
SK = lambda dst, src='light': ('body', src, dst)
AUTO = lambda mat, dst: (mat, 'auto', dst)
CL = lambda dst: ('cloth', 'white', dst)
HR = lambda dst: ('hair', 'orange', dst)
BOSS = [
 ('ice', 'male', [(10, 'body/bodies/muscular', None, SK('fur_white')), (100, 'head/heads/troll/adult', None, AUTO('body', 'fur_white')), (20, 'legs/armour/plate/male', None, AUTO('metal', 'silver')),
   (35, 'torso/armour/plate/male', None, AUTO('metal', 'silver')), (126, 'hat/formal/crown', None, lambda a: tintL(a, (200, 236, 255), .7))], 'ice'),
 ('dragon', 'male', [(5, 'body/wings/lizard/adult/bg', None, lambda a: hueL(a, .0, 1.35, .9)), (6, 'body/tail/lizard/adult/bg', None, lambda a: hueL(a, .02, 1.1)), (10, 'body/bodies/muscular', None, lambda a: hueL(recolor(a, SK('green')), .02, 1.1)), (100, 'head/heads/lizard/male', None, lambda a: hueL(recolor(a, SK('green', 'green')), .02, 1.1)),
   (20, 'legs/pants', None, CL('maroon')), (102, 'head/horns/curled', None, None), (110, 'body/wings/lizard/adult/fg', None, lambda a: hueL(a, .0, 1.35, .9)), (111, 'body/tail/lizard/adult/fg', None, lambda a: hueL(a, .02, 1.1))], 'fire'),
 ('witch', 'female', [(5, 'cape/tattered/bg', None, CL('black')), (10, 'body/bodies/female', None, SK('lavender')), (100, 'head/heads/human/female', None, SK('lavender')), (105, 'eyes/human/adult/default', 'purple', None),
   (35, 'torso/clothes/robe', 'black', None), (120, 'hair/long', None, HR('black')), (126, 'hat/magic/wizard/base', None, lambda a: tintL(a, (58, 30, 88), .82)), (110, 'cape/tattered/fg', None, CL('purple'))], 'shadow'),
 ('clock', 'male', [(10, 'body/bodies/muscular', None, SK('bronze')), (100, 'head/heads/human/male', None, SK('bronze')), (20, 'legs/armour/plate/male', None, AUTO('metal', 'brass')),
   (35, 'torso/armour/plate/male', None, AUTO('metal', 'brass')), (36, 'arms/armour/plate/male', None, AUTO('metal', 'brass')), (126, 'hat/helmet/greathelm/male', None, AUTO('metal', 'gold'))], 'clock'),
]
def tryfind(p, c, g):
    for pp in (p, p.replace('/foreground', ''), p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    cand = sorted(f for f in FILES if f.startswith('spritesheets/' + p + '/') and '/walk' in f and f.endswith('.png') and '/behind' not in f)
    if c: cand = [f for f in cand if c in f] or cand
    return cand[0] if cand else None
def cast_of(f):   # 걷기 그림 → 같은 부품의 주문 그림 (없으면 걷기 그대로)
    for a, b in (('/walk.png', '/spellcast.png'), ('/walk/', '/spellcast/')):
        if a in f and f.replace(a, b) in FILES: return f.replace(a, b)
    return f
def frame(f, col):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS['down'] * 64; x = col * 64
    return a[y:y + 64, x:x + 64] if y + 64 <= a.shape[0] and x + 64 <= a.shape[1] else np.zeros((64, 64, 4), np.uint8)
OL = (24, 16, 32, 255)
def px(cell, x, y, c):
    if 0 <= x < 64 and 0 <= y < 64: cell[y, x] = c
def outline_add(cell, pts, c):   # LPC처럼 바깥에 검은 테두리
    for (x, y) in pts: px(cell, x, y, c)
    for (x, y) in pts:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in pts and 0 <= x + dx < 64 and 0 <= y + dy < 64 and cell[y + dy, x + dx, 3] == 0: cell[y + dy, x + dx] = OL
def hue(cell, h_to, sat=1.0, keep=None):   # 초록 비늘 → 붉은 비늘
    out = cell.copy()
    for y in range(64):
        for x in range(64):
            r, g, b, a = cell[y, x]
            if a == 0 or (keep is not None and keep[y, x]): continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if ss < .12: continue
            hh = (hh + h_to) % 1; ss = min(1, ss * sat); rr, gg, bb = colorsys.hsv_to_rgb(hh, ss, vv); out[y, x, :3] = (int(rr * 255), int(gg * 255), int(bb * 255))
    return out
def hueL(a, h, sat=1.0, val=1.0):   # 부품 한 장의 색상을 정한 색상(h)으로 (명암은 그대로)
    out = a.copy()
    for y, x in zip(*np.nonzero(a[..., 3])):
        r, g, b, _ = a[y, x]; hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if ss < .1 or vv < .16: continue
        rr, gg, bb = colorsys.hsv_to_rgb(h, min(1, ss * sat), min(1, vv * val)); out[y, x, :3] = (int(rr * 255), int(gg * 255), int(bb * 255))
    return out
def tintL(a, c, k):
    out = a.copy().astype(float); m = a[..., 3] > 0
    lum = (out[..., 0] * .3 + out[..., 1] * .59 + out[..., 2] * .11) / 255
    for i in range(3): out[..., i] = np.where(m, out[..., i] * (1 - k) + c[i] * (.45 + lum) * k, out[..., i])
    return np.clip(out, 0, 255).astype(np.uint8)
def tint(cell, c, k, mask=None):
    out = cell.copy().astype(float)
    for y in range(64):
        for x in range(64):
            if cell[y, x, 3] and (mask is None or mask[y, x]) and tuple(cell[y, x, :3]) != OL[:3]: out[y, x, :3] = out[y, x, :3] * (1 - k) + np.array(c) * k
    return out.astype(np.uint8)
def body_box(cell):
    ys, xs = np.nonzero(cell[..., 3]); return xs.min(), ys.min(), xs.max(), ys.max()
def decorate(cell, kind, f):
    x0, y0, x1, y1 = body_box(cell); cx = (x0 + x1) // 2
    if kind == 'ice':   # 어깨 · 머리 위 얼음 수정, 몸에 서리
        cell[:] = tint(cell, (150, 210, 255), .32)
        for sx, h in ((cx - 11, 7), (cx - 8, 10), (cx + 8, 10), (cx + 11, 7)):
            sy = 30; pts = set()
            for k in range(h):
                w = max(0, 1 - k * 2 // h)
                for dx in range(-w, w + 1): pts.add((sx + dx, sy - k))
            outline_add(cell, pts, (190, 236, 255, 255))
            for k in range(1, h - 1): px(cell, sx - (1 if k < h // 2 else 0), sy - k, (255, 255, 255, 255))
        for (x, y) in ((cx - 4, 38), (cx + 3, 41), (cx - 1, 45), (cx + 5, 36)): px(cell, x, y, (235, 250, 255, 255))
        if f: [px(cell, cx + dx, 22 + dy, (127, 230, 255, 255)) for dx in (-3, -2, 2, 3) for dy in (0,)]
    if kind == 'fire':
        if f:
            for (x, y, c) in ((cx, 27, (255, 240, 150, 255)), (cx - 1, 28, (255, 180, 60, 255)), (cx + 1, 28, (255, 180, 60, 255)), (cx, 29, (255, 120, 40, 255))): px(cell, x, y, c)
    if kind == 'shadow':
        m = np.zeros((64, 64), bool); m[34:, :] = True
        cell[:] = tint(cell, (60, 20, 90), .25, m)
        for k in range(14):   # 발밑 그림자 연기
            x = x0 + 2 + k * (x1 - x0 - 4) // 13; y = 60 + (k % 3)
            if cell[y, x, 3] == 0: px(cell, x, y, (60, 30, 90, 200))
        if f: [px(cell, cx + dx, 21, (240, 190, 255, 255)) for dx in (-2, 2)]
    if kind == 'clock':   # 가슴 시계판 · 어깨 톱니
        cy = 39; pts = {(cx + dx, cy + dy) for dx in range(-5, 6) for dy in range(-5, 6) if dx * dx + dy * dy <= 26}
        outline_add(cell, pts, (242, 232, 200, 255))
        for dx, dy in [(x, y) for x in range(-5, 6) for y in range(-5, 6) if 20 <= x * x + y * y <= 26]: px(cell, cx + dx, cy + dy, (176, 132, 46, 255))
        for k in range(12):
            a = k * math.pi / 6; px(cell, cx + round(math.cos(a) * 3.6), cy + round(math.sin(a) * 3.6), (90, 60, 20, 255)) if k % 3 == 0 else None
        ha, ma = ((-math.pi / 2, math.pi / 5) if f == 0 else (math.pi * .85, -math.pi * .3))
        for t in range(3): px(cell, cx + round(math.cos(ha) * t), cy + round(math.sin(ha) * t), (40, 26, 12, 255))
        for t in range(5): px(cell, cx + round(math.cos(ma) * t), cy + round(math.sin(ma) * t), (40, 26, 12, 255))
        for gx in (cx - 12, cx + 12):
            g = {(gx + dx, 30 + dy) for dx in range(-3, 4) for dy in range(-3, 4) if dx * dx + dy * dy <= 9 or (abs(dx) == 3 and dy == 0) or (abs(dy) == 3 and dx == 0)}
            outline_add(cell, g, (184, 132, 46, 255)); px(cell, gx, 30, (74, 46, 16, 255))
            for (dx, dy) in ((-1, -2), (-2, -1)): px(cell, gx + dx, 30 + dy, (255, 232, 160, 255))
        if f:
            for dx, dy in [(x, y) for x in range(-6, 7) for y in range(-6, 7) if 30 <= x * x + y * y <= 38]:
                if cell[cy + dy, cx + dx, 3] == 0 or tuple(cell[cy + dy, cx + dx, :3]) == OL[:3]: px(cell, cx + dx, cy + dy, (255, 240, 160, 255))
plan, need, missing = [], set(), []
for bid, g, L, kind in BOSS:
    ls = []
    for z, p, c, rc in L:
        f = tryfind(p, c, g)
        if not f: missing.append((bid, p)); continue
        ls.append((z, f, cast_of(f), rc)); need |= {f, cast_of(f)}
    plan.append((bid, ls, kind))
need = sorted(f for f in need if not os.path.exists(os.path.join(LPC, f)))
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64, 64 * 2 * len(plan), 4), np.uint8)
for i, (bid, L, kind) in enumerate(plan):
    for fr in (0, 1):
        cell = np.zeros((64, 64, 4), np.uint8)
        for z, fw, fc, rc in sorted(L, key=lambda t: t[0]):
            im = frame(fc, 5) if fr else frame(fw, 0); over(cell, rc(im) if callable(rc) else recolor(im, rc))
        decorate(cell, kind, fr)
        sheet[:, (i * 2 + fr) * 64:(i * 2 + fr + 1) * 64] = cell
Image.fromarray(sheet).save(OUT)
print('없는 부품:', missing, '→', OUT)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (sheet.shape[1], 64), (52, 40, 76, 255)); pv.alpha_composite(Image.fromarray(sheet)); pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(sys.argv[2])
