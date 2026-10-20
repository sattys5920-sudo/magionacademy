# 놀이 마당 (34x28): 놀이(호박 줍기·빗자루 경주 …)를 하는 전용 맵. 눌러서 뜨는 물건이 하나도 없는 넓은 풀밭이에요
#   python3 arena.py → out/arena_bg.png, out/arena_obj.png, out/arena.json (build_halloween.py가 불러가요)
#   게임이 시작되면 모두 이리로 오고, 끝나면 원래 있던 곳으로 돌아가요 (index.html gameStart·gameReturn). 남쪽 문 기둥 사이로 나가면 시장 광장이에요
import json, math, os, random
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(53)
NX, NY = 34, 28
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 200
OX, OY = NY * 8 + 20, 160
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#120A18')
src = open('world.py').read()
exec(src[src.index('def poly(d, pts, c)'):src.index('# 본관 (크게, 탑 두 개)')])
# ---------------- 땅 ----------------
T = {}
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
fill('dirt', 4, 4, 30, 24)             # 바깥 달리기 길
fill('grass', 6, 6, 28, 22)            # 안쪽 풀밭 (놀이 판)
fill('dirt', 15, 24, 19, 28)           # 남쪽 출구 길
fill('cobble', 13, 20, 21, 24)         # 출구 앞 돌바닥
for x in range(NX):
    for y in range(NY): T.setdefault((x, y), 'grass')
GRASS = [hexc('#3E4E3A'), hexc('#36463A'), hexc('#46563E'), hexc('#3A4436')]
bg = Image.new('RGBA', (W, H), hexc('#140E1E')); px = bg.load()
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t == 'dirt':
            c = hexc('#6A5444') if random.random() > .12 else hexc('#5E4A3C')
            if random.random() < .02: c = hexc('#7E6A58')
        elif t == 'cobble':
            s_ = 3; bx, by = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
            c = [hexc('#7A7480'), hexc('#6E6876'), hexc('#86808C')][(bx * 5 + by * 3) % 3]
            if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#4E4856')
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .004: c = random.choice([hexc('#C86AE8'), hexc('#E8A050'), hexc('#8AE8C8')])
        px[x, y] = c
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x14, 0x0E, 0x1E): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#3A2A24') if (y // 3) % 2 else hexc('#2E221E')
bg.save('out/arena_bg.png'); print('bg', W, H)
# ---------------- 그림 (quarter.py와 같아요) ----------------
def dark_tree(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 'dead':
            d.line([(cx, cy), (cx, cy - 22)], fill=hexc('#3A2E2A'), width=3)
            for (a, b, c_, e) in ((0, -14, -9, -22), (0, -18, 8, -27), (-6, -19, -10, -26), (5, -24, 3, -31), (0, -22, -3, -32)): d.line([(cx + a, cy + b), (cx + c_, cy + e)], fill=hexc('#3A2E2A'), width=2 if b > -18 else 1)
            return
        d.rectangle([cx - 2, cy - 12, cx + 1, cy], fill=hexc('#3A2A24'))
        if kind == 'pine':
            for k, (wd, yy) in enumerate(((11, -12), (9, -20), (7, -28), (4, -35))): d.polygon([(cx - wd, cy + yy), (cx, cy + yy - 12), (cx + wd, cy + yy)], fill=hexc('#22382E') if k % 2 else hexc('#2A4434'))
            return
        g1, g2, g3 = (hexc('#2E3E36'), hexc('#3A4E40'), hexc('#4E6450')) if kind == 'round' else (hexc('#4A2E4E'), hexc('#5E3A62'), hexc('#7A4E7E'))
        r = 10
        for dx, dy, rr in ((-6, -16, r - 3), (6, -16, r - 3), (0, -24, r - 1), (0, -14, r - 2)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g1)
        for dx, dy, rr in ((-4, -20, r - 5), (4, -22, r - 5), (-1, -27, r - 6)): d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=g2)
        for dx, dy in ((-5, -24), (2, -29), (5, -25)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=g3)
    return f
for k in ('round', 'purple', 'pine', 'dead'): shared('t_' + k, dark_tree(k))
def pumpkin_at(lit):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for dx, w in ((-4, 4), (4, 4), (0, 5)): d.ellipse([cx + dx - w, cy - 9, cx + dx + w, cy], fill=hexc('#E07A1E'))
        d.rectangle([cx - 1, cy - 12, cx, cy - 9], fill=hexc('#4A6A2A'))
        if lit:
            d.polygon([(cx - 5, cy - 6), (cx - 3, cy - 8), (cx - 2, cy - 5)], fill=hexc('#FFE07A')); d.polygon([(cx + 5, cy - 6), (cx + 3, cy - 8), (cx + 2, cy - 5)], fill=hexc('#FFE07A'))
            d.line([(cx - 4, cy - 3), (cx + 4, cy - 3)], fill=hexc('#FFD04A'))
    return f
shared('jack', pumpkin_at(True))
def lantern_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 28, cx, cy], fill=hexc('#2A2230')); d.line([(cx, cy - 28), (cx + 6, cy - 30)], fill=hexc('#2A2230'))
    d.ellipse([cx + 3, cy - 30, cx + 10, cy - 22], fill=hexc('#FF9A3A')); d.ellipse([cx + 5, cy - 28, cx + 8, cy - 24], fill=hexc('#FFE08A'))
shared('lantern', lantern_at)
def iron_at(r, dn):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 1, cy - 14, cx, cy], fill=hexc('#2A2230')); d.point((cx, cy - 15), fill=hexc('#2A2230'))
        for on, dx in ((r, 8), (dn, -8)):
            if not on: continue
            for k in range(1, 4): xx = cx + dx * k / 4; yy = cy + 4 * k / 4; d.line([(xx, yy), (xx, yy - 11)], fill=hexc('#2A2230'))
            d.line([(cx, cy - 10), (cx + dx, cy - 6)], fill=hexc('#2A2230')); d.line([(cx, cy - 3), (cx + dx, cy + 1)], fill=hexc('#2A2230'))
    return f
for r in (0, 1):
    for dn in (0, 1): shared(f'iron{r}{dn}', iron_at(r, dn))
def pillar(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 7, cy - 6, cx + 7, cy + 2], fill=hexc('#4E4856')); d.rectangle([cx - 5, cy - 46, cx + 5, cy - 6], fill=hexc('#6E6876')); d.rectangle([cx - 5, cy - 46, cx, cy - 6], fill=hexc('#5E586A'))
    for k in range(-40, -8, 8): d.line([(cx - 5, cy + k), (cx + 5, cy + k)], fill=hexc('#4E4856'))
    d.rectangle([cx - 8, cy - 50, cx + 8, cy - 46], fill=hexc('#4E4856')); d.polygon([(cx - 8, cy - 50), (cx, cy - 58), (cx + 8, cy - 50)], fill=hexc('#3A2A5E'))
    d.line([(cx, cy - 46), (cx, cy - 38)], fill=hexc('#2A2230')); d.ellipse([cx - 4, cy - 38, cx + 4, cy - 28], fill=hexc('#FF9A3A')); d.ellipse([cx - 2, cy - 36, cx + 2, cy - 31], fill=hexc('#FFE08A'))
shared('pillar', pillar)
def flag_at(col):   # 모서리 깃발 (꾸밈)
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.rectangle([cx - 1, cy - 40, cx, cy], fill=hexc('#2A2230')); d.polygon([(cx + 1, cy - 40), (cx + 16, cy - 35), (cx + 1, cy - 28)], fill=hexc(col)); d.ellipse([cx - 2, cy - 43, cx + 2, cy - 39], fill=hexc('#E0C070'))
    return f
for c in ('#E07A1E', '#7A4AA8', '#4AA86A', '#C8486A'): shared('flag' + c, flag_at(c))
# ---------------- 놓기 (아무 동작도 안 붙여요: act 없음) ----------------
occupied = set()
def can(x, y): return (x, y) not in occupied and T.get((x, y)) == 'grass'
def put(name, key, x, y, **kw): place(name, key, x, y, **kw); occupied.add((x, y))
# 울타리: 남쪽 가운데(15·16·17·18)는 비워 둬요
FN = set((x, 2) for x in range(2, 32)) | set((x, 25) for x in range(2, 32)) | set((2, y) for y in range(2, 26)) | set((31, y) for y in range(2, 26))
FN -= {(x, 25) for x in range(15, 19)}
for (x, y) in sorted(FN): put('fence', f'iron{int((x + 1, y) in FN)}{int((x, y + 1) in FN)}', x, y)
# 출구 문 기둥 (사이로 걸어 나가면 시장 광장)
put('gate', 'pillar', 14, 26); objs[-1]['door'] = dict(tile=[16, 27], to='campus', spawn=[61, 32], label='등불 시장', walk=True, spanX=[15, 18]); put('gate', 'pillar', 19, 26)
# 모서리 깃발·가로등 (꾸밈만)
for i, (x, y) in enumerate(((3, 3), (30, 3), (3, 24), (30, 24))): put('flag', 'flag' + ['#E07A1E', '#7A4AA8', '#4AA86A', '#C8486A'][i], x, y)
for (x, y) in [(10, 3), (16, 3), (22, 3), (3, 12), (30, 12), (10, 24), (22, 24)]: put('lantern', 'lantern', x, y)
for (x, y) in [(4, 8), (4, 17), (29, 8), (29, 17), (9, 4), (24, 4), (9, 23), (24, 23)]: put('jack', 'jack', x, y, solid=False)
# 바깥 숲
for x in range(NX):
    for y in range(NY):
        if not can(x, y): continue
        if 2 <= x <= 31 and 2 <= y <= 25: continue
        edge = min(x, y, NX - 1 - x, NY - 1 - y)
        if random.random() < (.75 if edge < 2 else .5):
            put('tree', 't_' + random.choice(['pine', 'pine', 'dead', 'round', 'purple']), x, y)
# ---------------- 저장 ----------------
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/arena_obj.png')
meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
lights = [dict(p=P(x + .5, y + .5), dy=-26, r=32, c=[255, 160, 70], a=.6, f=1) for (x, y) in [(10, 3), (16, 3), (22, 3), (3, 12), (30, 12), (10, 24), (22, 24)]]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-6, r=18, c=[255, 170, 60], a=.55, f=1) for o in objs if o['spr'] == 'jack']
lights += [dict(p=P(x + .5, y + .5), dy=-34, r=36, c=[255, 160, 70], a=.6, f=1) for (x, y) in ((14, 26), (19, 26))]
lights += [dict(p=P(x + .5, y + .5), dy=-38, r=28, c=[255, 190, 100], a=.5, f=1) for (x, y) in ((3, 3), (30, 3), (3, 24), (30, 24))]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, areas=[dict(n='놀이 마당', t=[16, 13])], start=[16, 21]), open('out/arena.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sheet', sheet.size)
