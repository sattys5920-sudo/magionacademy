# 용의 동굴 (32x26): 이벤트 「용의 알 지키기」에서 지켜 낸 용들이 사는 곳. 학교 북쪽 문(build_halloween.py)으로 들어와요
#   python3 dcave.py → out/dcave_bg.png, out/dcave_obj.png, out/dcave.json (build_halloween.py가 불러가요)
#   용 세 마리(불·물·숲)는 둥지 둘레에 서 있고, 알이 깨졌던 자리에는 깨진 알껍데기가 놓여요 (req: alive:N / dead:N — index.html World.reqOk)
import json, math, os, random
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(77)
NX, NY = 32, 26
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 200
OX, OY = NY * 8 + 20, 160
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
OUTL = hexc('#120A18')
src = open('world.py').read()
exec(src[src.index('def poly(d, pts, c)'):src.index('# 본관 (크게, 탑 두 개)')])
DR = Image.open('../../public/art/dragons.png').convert('RGBA')
# ---------------- 땅 ----------------
T = {}
for x in range(NX):
    for y in range(NY): T[(x, y)] = 'rock'
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
fill('path', 14, 12, 18, 26)           # 입구에서 둥지까지 닿는 길
NEST = (16, 9)
for x in range(NX):
    for y in range(NY):
        if math.hypot(x - NEST[0], (y - NEST[1]) * 1.3) <= 6.6: T[(x, y)] = 'nest'
ROCK = [hexc('#3C3240'), hexc('#443A48'), hexc('#382E3C'), hexc('#40363E')]
bg = Image.new('RGBA', (W, H), hexc('#0C0715')); px = bg.load()
cracks = set()
for k in range(40):
    x, y = random.random() * NX, random.random() * NY
    if T[(int(x), int(y))] != 'rock': continue
    for t in range(random.randint(4, 9)):
        cracks.add((int(x * 8), int(y * 8))); x += random.choice([-.12, 0, .12]); y += random.choice([-.12, 0, .12])
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t == 'path':
            s_ = 3; bx, by = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
            c = [hexc('#6A5E66'), hexc('#5E5460'), hexc('#746870')][(bx * 5 + by * 3) % 3]
            if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#3E3440')
        elif t == 'nest':
            d = math.hypot(fx - NEST[0], (fy - NEST[1]) * 1.3)
            c = hexc('#8A6A38') if random.random() > .25 else hexc('#7A5A2E')
            if random.random() < .08: c = hexc('#B08A48')
            if d > 5.8: c = hexc('#5A4430') if random.random() > .3 else hexc('#4A3828')
        else:
            c = ROCK[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .03: c = hexc('#4E4254')
            if (int(fx * 8), int(fy * 8)) in cracks: c = hexc('#FF8A3A') if random.random() < .5 else hexc('#C8582A')
        px[x, y] = c
# 땅 아래 옆면 (그림자 색)
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x0C, 0x07, 0x15): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#2A2030') if (y // 3) % 2 else hexc('#221A28')
bg.save('out/dcave_bg.png'); print('bg', W, H)
# ---------------- 그림 ----------------
def stalag(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        w, h = {'s': (6, 14), 'm': (9, 24), 'l': (12, 36)}[kind]
        poly(d, [(cx - w, cy + 2), (cx - w * .3, cy - h), (cx + w * .2, cy - h * .8), (cx + w, cy + 2)], hexc('#4A3E50'))
        poly(d, [(cx - w, cy + 2), (cx - w * .3, cy - h), (cx - w * .1, cy - h * .3), (cx - w * .2, cy + 2)], hexc('#6A5E70'))
        poly(d, [(cx + w * .3, cy + 2), (cx + w * .2, cy - h * .8), (cx + w, cy + 2)], hexc('#382C3E'))
    return f
for k in ('s', 'm', 'l'): shared('sg_' + k, stalag(k))
def crystal(col):
    base, lite, dark = hexc(col), shade(hexc(col), 1.35), shade(hexc(col), .6)
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for dx, h, w in ((-5, 14, 4), (1, 22, 5), (7, 11, 3)):
            poly(d, [(cx + dx - w, cy), (cx + dx - w + 1, cy - h + 4), (cx + dx, cy - h), (cx + dx + w - 1, cy - h + 4), (cx + dx + w, cy)], base)
            poly(d, [(cx + dx, cy - h), (cx + dx - w + 1, cy - h + 4), (cx + dx - w, cy), (cx + dx - 1, cy)], lite)
            poly(d, [(cx + dx, cy - h), (cx + dx + w - 1, cy - h + 4), (cx + dx + w, cy), (cx + dx + 1, cy)], dark)
    return f
for nm, c in (('r', '#E8503A'), ('o', '#F0A030'), ('p', '#B060E8')): shared('cr_' + nm, crystal(c))
def gold(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, w in ((-5, 0, 8), (5, 1, 7), (0, -3, 8), (-2, -6, 5)): d.ellipse([cx + dx - w, cy + dy - w // 2 - 3, cx + dx + w, cy + dy + w // 2], fill=hexc('#E8B030'))
    for dx, dy, w in ((-4, -2, 5), (3, -4, 5), (0, -7, 3)): d.ellipse([cx + dx - w, cy + dy - 3, cx + dx + w, cy + dy + 1], fill=hexc('#FFE070'))
    for dx, dy in ((-7, 1), (6, 2), (1, -5)): d.rectangle([cx + dx, cy + dy, cx + dx + 1, cy + dy + 1], fill=random.choice([hexc('#FF5A6A'), hexc('#6AD8FF'), hexc('#8AF08A')]))
shared('gold', gold)
def bones(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); c = hexc('#E8DCC0')
    d.line([(cx - 8, cy), (cx + 6, cy - 3)], fill=c, width=2); d.ellipse([cx - 10, cy - 2, cx - 6, cy + 2], fill=c); d.ellipse([cx + 5, cy - 6, cx + 9, cy - 2], fill=c)
    d.ellipse([cx - 3, cy - 12, cx + 5, cy - 5], fill=c); d.rectangle([cx - 1, cy - 8, cx, cy - 7], fill=OUTL); d.rectangle([cx + 2, cy - 8, cx + 3, cy - 7], fill=OUTL)
shared('bones', bones)
def torch(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 26, cx + 1, cy], fill=hexc('#4A3828')); d.rectangle([cx - 4, cy - 30, cx + 4, cy - 25], fill=hexc('#2A2230'))
    poly(d, [(cx - 4, cy - 30), (cx, cy - 44), (cx + 4, cy - 30)], hexc('#FF8A2A')); poly(d, [(cx - 2, cy - 30), (cx, cy - 39), (cx + 2, cy - 30)], hexc('#FFE070'))
shared('torch', torch)
def wallrock(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); h = 30 + kind * 8
        poly(d, [(cx - 16, cy + 4), (cx - 12, cy - h * .6), (cx - 4, cy - h), (cx + 6, cy - h * .85), (cx + 14, cy - h * .5), (cx + 16, cy + 4)], hexc('#2E2434'))
        poly(d, [(cx - 16, cy + 4), (cx - 12, cy - h * .6), (cx - 4, cy - h), (cx - 5, cy - h * .5), (cx - 6, cy + 4)], hexc('#4A3E50'))
        poly(d, [(cx + 6, cy - h * .85), (cx + 14, cy - h * .5), (cx + 16, cy + 4), (cx + 4, cy + 4)], hexc('#241C2A'))
    return f
for k in range(3): shared('wr%d' % k, wallrock(k))
def pillar_g(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    poly(d, [(cx - 9, cy + 3), (cx - 7, cy - 40), (cx + 7, cy - 40), (cx + 9, cy + 3)], hexc('#4A3E50')); poly(d, [(cx - 9, cy + 3), (cx - 7, cy - 40), (cx - 2, cy - 40), (cx - 3, cy + 3)], hexc('#6A5E70'))
    d.ellipse([cx - 5, cy - 34, cx + 5, cy - 24], fill=hexc('#FF8A2A')); d.ellipse([cx - 2, cy - 31, cx + 2, cy - 27], fill=hexc('#FFE08A'))
shared('pillar_g', pillar_g)
def nest_rim(img, x, y):   # 둥지 가장자리의 짚·나뭇가지 한 뭉치
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for a in range(-8, 9, 4): d.line([(cx + a, cy), (cx + a * 1.6, cy - 8 - abs(a) % 5)], fill=hexc('#6A4A28'), width=2)
    for a in range(-6, 7, 4): d.line([(cx + a, cy), (cx + a * 1.2, cy - 6)], fill=hexc('#B08A48'), width=1)
shared('nestrim', nest_rim)
def dragon_at(row, frame=0, sc=1):
    def f(img, x, y):
        cx, cy = P(x + .5, y + .5); s = DR.crop((frame * 32, row * 32, frame * 32 + 32, row * 32 + 32)).resize((32 * sc, 32 * sc), Image.NEAREST)
        sh = ImageDraw.Draw(img); sh.ellipse([cx - 14, cy - 3, cx + 14, cy + 5], fill=(0, 0, 0, 90))
        img.alpha_composite(s, (int(cx - 16 * sc), int(cy - 30 * sc + 6)))
    return f
for r, nm in enumerate(('fire', 'water', 'forest')): shared('dragon_' + nm, dragon_at(r))
def shell(r):
    cols = ['#F0A07A', '#9ACCF0', '#A0DC96']
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); c = hexc(cols[r]); dk = shade(c, .6)
        for dx, dy, w in ((-6, 0, 7), (5, 1, 6)): poly(d, [(cx + dx - w, cy + dy), (cx + dx - w + 2, cy + dy - 7), (cx + dx - 1, cy + dy - 4), (cx + dx + 2, cy + dy - 8), (cx + dx + w, cy + dy)], c)
        d.line([(cx - 9, cy), (cx + 8, cy + 2)], fill=dk, width=1)
        d.ellipse([cx - 2, cy - 14, cx + 2, cy - 10], fill=hexc('#FFE070'))   # 아직 남은 따뜻한 불씨
    return f
for r in range(3): shared('shell%d' % r, shell(r))
# ---------------- 놓기 ----------------
occupied = set()
def can(x, y): return (x, y) not in occupied and T.get((x, y)) == 'rock' and 2 <= x <= NX - 3 and 2 <= y <= NY - 3
def put(name, key, x, y, **kw): place(name, key, x, y, **kw); occupied.add((x, y))
# 가장자리 바위 벽 (아래 가운데 입구는 비워 둬요)
GAP = {(x, y) for x in range(14, 18) for y in range(NY - 3, NY)}
for x in range(NX):
    for y in range(NY):
        if (x, y) in GAP: continue
        if x < 1 or y < 1 or x >= NX - 1 or y >= NY - 1:
            put('wall', 'wr%d' % ((x * 7 + y * 3) % 3), x, y)
# 입구 기둥과 문 (사이로 걸어 나가면 학교 북쪽 길)
put('gate', 'pillar_g', 13, NY - 3); put('gate', 'pillar_g', 18, NY - 3)
objs[-2]['door'] = dict(tile=[16, NY - 1], to='campus', spawn=[30, 16], label='학교 북쪽 길', walk=True, spanX=[14, 17])
# 둥지: 가장자리 짚
for a in range(0, 360, 24):
    x, y = int(round(NEST[0] + math.cos(math.radians(a)) * 6.0)), int(round(NEST[1] + math.sin(math.radians(a)) * 4.6))
    if (x, y) not in occupied: put('nestrim', 'nestrim', x, y, solid=False)
# 용 세 마리 (살아 있으면 용, 알이 깨졌으면 깨진 알껍데기) — req 는 게임이 정해요
SPOTS = [(12, 11), (16, 7), (20, 11)]
for i, (nm, (x, y)) in enumerate(zip(('fire', 'water', 'forest'), SPOTS)):
    put('dragon%d' % i, 'dragon_' + nm, x, y, act=['용', '용 만나기']); objs[-1]['req'] = 'alive:%d' % i
    place('shell%d' % i, 'shell%d' % i, x, y, solid=False); objs[-1]['req'] = 'dead:%d' % i
# 보물 더미 · 뼈 · 수정 · 종유석 · 횃불
for (x, y) in [(6, 6), (7, 9), (26, 7), (25, 10), (6, 14), (26, 15)]: put('gold', 'gold', x, y, solid=False)
for (x, y) in [(10, 14), (22, 15), (12, 19), (20, 20)]: put('bones', 'bones', x, y, solid=False)
for i, (x, y) in enumerate([(5, 6), (26, 6), (6, 16), (25, 18), (10, 4), (22, 4), (4, 20), (27, 21)]): put('crystal', 'cr_' + 'rop'[i % 3], x, y)
for _ in range(34):
    x, y = random.randint(2, NX - 3), random.randint(2, NY - 3)
    if not can(x, y) or abs(x - 16) < 3 and y > 6: continue
    put('stalag', 'sg_' + random.choice('ssmml'), x, y)
TORCH = [(12, 21), (19, 21), (5, 10), (26, 10), (11, 3), (21, 3), (3, 17), (28, 17)]
for (x, y) in TORCH: put('torch', 'torch', x, y)
# ---------------- 저장 ----------------
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/dcave_obj.png')
meta = []
for o in objs:
    m = dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act'])
    if o.get('req'): m['req'] = o['req']
    meta.append(m)
lights = [dict(p=P(x + .5, y + .5), dy=-36, r=46, c=[255, 150, 60], a=.65, f=1) for (x, y) in TORCH]
lights += [dict(p=P(NEST[0] + .5, NEST[1] + .5), dy=-6, r=70, c=[255, 190, 90], a=.5, f=1)]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-12, r=28, c=[255, 120, 80] if o['spr'] == 'cr_r' else [255, 190, 90] if o['spr'] == 'cr_o' else [190, 120, 255], a=.55, f=1) for o in objs if o['spr'] in ('cr_r', 'cr_o', 'cr_p')]
lights += [dict(p=P(x + .5, y + .5), dy=-30, r=34, c=[255, 160, 70], a=.6, f=1) for (x, y) in ((13, NY - 3), (18, NY - 3))]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, areas=[dict(n='용의 동굴', t=[16, 14])], start=[16, NY - 4]), open('out/dcave.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sheet', sheet.size)
