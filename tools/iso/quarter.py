# 그림자 골목 (72x48): 시장 거리 동쪽 끝에서 이어지는 의뢰인 마을. 큰길 두 줄에 집들이 늘어서요
#   python3 quarter.py → out/quarter_bg.png, out/quarter_obj.png, out/quarter.json (build_halloween.py가 불러가요)
import json, math, os, random
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(77)
NX, NY = 72, 42
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
fill('cobble', 2, 12, 10, 18)            # 문 앞 돌바닥
fill('dirt', 2, 13, NX - 1, 17)          # 큰길 A (집 앞길)
fill('dirt', 2, 29, NX - 1, 33)          # 큰길 B
fill('dirt', 34, 17, 38, 29)             # 두 큰길을 잇는 골목
fill('dirt', 60, 17, 64, 29)
fill('cobble', 54, 2, 70, 13)            # 일곱 등불 광장
fill('stone', 6, 13, 20, 14)             # 저택 앞마당 돌
for i in range(0, 4): fill('dirt', 11 + i // 2, 13, 13, 14)
fill('grave', 54, 22, 67, 29)            # 작은 묘지
POND = dict(id='pond_q', name='골목 연못', cx=20, cy=23, rx=5, ry=3.5)   # 낚시 연못
for x in range(NX):
    for y in range(NY):
        if ((x + .5 - POND['cx']) / POND['rx']) ** 2 + ((y + .5 - POND['cy']) / POND['ry']) ** 2 < 1: T[(x, y)] = 'lake'
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
        elif t in ('stone', 'cobble'):
            s_ = 3 if t == 'cobble' else 2
            bx, by = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
            c = [hexc('#7A7480'), hexc('#6E6876'), hexc('#86808C')][(bx * 5 + by * 3) % 3]
            if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#4E4856')
        elif t == 'grave':
            c = [hexc('#3A3E34'), hexc('#34382E'), hexc('#42463A')][random.randint(0, 2)]
        elif t == 'lake':
            c = hexc('#2E5A6A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#4A7A8A')
            if random.random() < .015: c = hexc('#A8E8F0')
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .004: c = random.choice([hexc('#C86AE8'), hexc('#E8A050'), hexc('#8AE8C8')])
        px[x, y] = c
for x in range(W):
    for y in range(H):
        if px[x, y][:3] != (0x14, 0x0E, 0x1E): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#3A2A24') if (y // 3) % 2 else hexc('#2E221E')
bg.save('out/quarter_bg.png'); print('bg', W, H)
# ---------------- 그림 도구 (halloween.py와 같은 모양) ----------------
def wins_g(step=16, rows=((14, 18), (44, 14))):
    def f(side, length): return [(u, v, 8, hh) for u in range(10, int(length) - 8, step) for v, hh in rows]
    return f
def combo(*fs):
    def f(img):
        for g in fs: g(img)
    return f
def turret(tx, ty, height, wall, roof, win='#FFC86A'):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = P(tx, ty)
        d.rectangle([cx - 8, cy - height, cx + 8, cy], fill=hexc(wall)); d.rectangle([cx - 8, cy - height, cx, cy], fill=shade(hexc(wall), .85))
        d.ellipse([cx - 8, cy - 3, cx + 8, cy + 3], fill=shade(hexc(wall), .85))
        for k in range(14, height - 8, 16): d.rectangle([cx - 2, cy - k - 8, cx + 2, cy - k], fill=hexc(win))
        d.rectangle([cx - 10, cy - height - 2, cx + 10, cy - height], fill=shade(hexc(wall), .7))
        d.polygon([(cx - 10, cy - height - 2), (cx, cy - height - 30), (cx + 10, cy - height - 2)], fill=hexc(roof)); d.polygon([(cx - 10, cy - height - 2), (cx, cy - height - 30), (cx, cy - height - 2)], fill=shade(hexc(roof), .75))
        d.rectangle([cx - 1, cy - height - 34, cx, cy - height - 30], fill=hexc('#E0C070'))
    return f
def columns(x0, y0, x1, y1, h, col):   # 박물관 앞 기둥
    def fn(u, v):
        if 6 < v < h - 6 and (u % 20) in (6, 7, 8, 9, 10): return shade(hexc(col), .8 if (u % 20) < 8 else 1.0)
        return None
    return lambda img: face(img, x0, y0, x1, y1, 'L', fn)
def rod(x0, y0, x1, y1, top):   # 번개 탑 꼭대기 피뢰침
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = up(P((x0 + x1) / 2, (y0 + y1) / 2), top)
        d.line([(cx, cy), (cx, cy - 26)], fill=hexc('#2A2230'), width=2); d.ellipse([cx - 3, cy - 31, cx + 3, cy - 25], fill=hexc('#9AF0C8'))
        for k in (-8, 8): d.line([(cx, cy - 12), (cx + k, cy - 18)], fill=hexc('#2A2230'))
    return f
def witch_hut(cx0, cy0):
    def f(img):
        d = ImageDraw.Draw(img); cx, cy = P(cx0, cy0)
        d.rectangle([cx - 16, cy - 26, cx + 16, cy], fill=hexc('#5A4A3A')); d.rectangle([cx - 16, cy - 26, cx, cy], fill=hexc('#4E3E30'))
        for k in range(0, 26, 6): d.line([(cx - 16, cy - k), (cx + 16, cy - k)], fill=hexc('#3A2C22'))
        d.rectangle([cx - 5, cy - 16, cx + 1, cy], fill=hexc('#2A1E16')); d.rectangle([cx + 6, cy - 20, cx + 12, cy - 13], fill=hexc('#FFB04A'))
        d.polygon([(cx - 22, cy - 24), (cx + 4, cy - 70), (cx + 22, cy - 24)], fill=hexc('#3A2A5E')); d.polygon([(cx - 22, cy - 24), (cx + 4, cy - 70), (cx - 2, cy - 24)], fill=hexc('#2E2050'))
        d.line([(cx + 4, cy - 70), (cx + 12, cy - 76)], fill=hexc('#3A2A5E'), width=2)
        d.ellipse([cx - 24, cy - 28, cx + 24, cy - 20], outline=hexc('#2E2050'))
    return f
def log_cabin(x0, y0, x1, y1, h=28):
    def f(img):
        def fn(u, v):
            if v >= h: return None
            c = hexc('#7A5232') if (v // 4) % 2 else hexc('#6A4428')
            if v % 4 == 0: c = hexc('#4A2E1A')
            return c
        face(img, x0, y0, x1, y1, 'L', fn); face(img, x0, y0, x1, y1, 'R', fn)
        face(img, x0, y0, x1, y1, 'L', lambda u, v: (hexc('#2A1A10') if v < 18 else None) if 18 <= u < 28 else (hexc('#FFB04A') if 36 <= u < 42 and 10 <= v < 18 else None))
        d = ImageDraw.Draw(img); Tt, R, B, L = [up(p, h) for p in (P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1))]
        r1, r2 = up(P(x0, (y0 + y1) / 2), h + 18), up(P(x1, (y0 + y1) / 2), h + 18)
        poly(d, [Tt, R, r2, r1], hexc('#3A2E22')); poly(d, [L, B, r2, r1], hexc('#5A4632')); poly(d, [R, B, r2], hexc('#4A3A2A'))
        claw = up(P(x1, (y0 + y1) / 2), h + 6)
        for k in range(3): d.line([(claw[0] - 6 + k * 3, claw[1] - 4), (claw[0] - 4 + k * 3, claw[1] + 4)], fill=hexc('#C8B89A'))
    return f
# ---------------- 건물 ----------------
# 뱀파이어 저택 (큰길 A 북쪽, 문 (12,13))
unique('manor', [6, 4, 20, 13], combo(building(6, 4, 20, 13, 70, hexc('#3E3446'), hexc('#1E1824'), hexc('#2A1E30'), 40, lambda s, l: [(u, v, 8, 18) for u in range(10, int(l) - 8, 14) for v in (12, 42) if not (s == 'L' and abs(u - 44) < 10)], doors=[('L', 48, 14)]),
       turret(6.4, 12.6, 100, '#3E3446', '#2A1E30', '#FF5A4A'), turret(19.6, 4.4, 100, '#3E3446', '#2A1E30', '#FF5A4A')),
       door=dict(tile=[12, 13], to=None, label='뱀파이어 저택', note='집사 박쥐가 마당에서 기다려요. 안은 손님이 들어가기엔 아직 어수선해요'))
# 학교 박물관 (문 (31,13))
unique('museum', [26, 6, 38, 13], combo(building(26, 6, 38, 13, 46, hexc('#B8A276'), hexc('#D8C494'), hexc('#8A7448'), 14, wins_g(16, ((18, 14),)), doors=[('L', 40, 14)]), columns(26, 6, 38, 13, 46, '#E0CFA0')),
       door=dict(tile=[31, 13], to=None, label='학교 박물관', note='창가 관 옆에서 서기가 지켜보고 있어요. 안으로는 아직 못 들어가요'))
# 번개 탑 (낡은 연구 탑, 문 (45,13))
unique('labtower', [42, 5, 48, 13], combo(building(42, 5, 48, 13, 84, hexc('#585868'), hexc('#34344A'), hexc('#2E3E44'), 20, wins_g(14, ((14, 14), (42, 14), (66, 10))), doors=[('L', 20, 12)]), rod(42, 5, 48, 13, 84 + 20)),
       door=dict(tile=[44, 13], to=None, label='낡은 연구 탑', note='번개 맞은 자국이 선명해요. 문은 오래전에 잠겼어요'))
# 마녀 오두막 (큰길 B 북쪽, 문 (9,29)) · 늑대인간 통나무집 (문 (28,29))
unique('witchhut', [8, 25, 12, 29], witch_hut(10, 26.5), door=dict(tile=[9, 29], to=None, label='마녀의 오두막', note='초록 연기가 굴뚝에서 피어올라요. 주인은 지금 바빠요'))
unique('cabin', [26, 24, 32, 29], log_cabin(26, 24, 32, 29), door=dict(tile=[28, 29], to=None, label='늑대인간 통나무집', note='문틈으로 장작 타는 냄새가 나요. 지하실 문은 이제 열려 있대요'))
# 일곱 등불 광장 가운데 기둥, 비어 있는 등불대, 바깥 솥
def sevenpost(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 12, cy - 4, cx + 12, cy + 4], fill=hexc('#4E4856')); d.rectangle([cx - 8, cy - 9, cx + 8, cy - 1], fill=hexc('#6E6876'))
    d.rectangle([cx - 2, cy - 52, cx + 1, cy - 8], fill=hexc('#2A2230')); d.ellipse([cx - 14, cy - 56, cx + 14, cy - 46], outline=hexc('#2A2230'))
    for k in range(7):
        a = k / 7 * 6.2832; lx = cx + 13 * math.cos(a); ly = cy - 51 + 4 * math.sin(a)
        d.line([(lx, ly), (lx, ly + 4)], fill=hexc('#2A2230')); d.ellipse([lx - 3, ly + 3, lx + 3, ly + 10], fill=hexc('#FF9A3A')); d.ellipse([lx - 1, ly + 5, lx + 1, ly + 8], fill=hexc('#FFE08A'))
    d.ellipse([cx - 4, cy - 60, cx + 4, cy - 52], fill=hexc('#FFE08A'))
shared('sevenpost', sevenpost)
def emptylamp(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 40, cx, cy], fill=hexc('#2A2230')); d.line([(cx, cy - 40), (cx + 9, cy - 43)], fill=hexc('#2A2230'), width=2)
    d.rectangle([cx + 6, cy - 42, cx + 13, cy - 31], fill=hexc('#6E6A78')); d.rectangle([cx + 7, cy - 41, cx + 12, cy - 32], fill=hexc('#3A3844')); d.polygon([(cx + 5, cy - 42), (cx + 9, cy - 47), (cx + 14, cy - 42)], fill=hexc('#2A2230'))
shared('emptylamp', emptylamp)
def cauldron_out(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 9, cy - 10, cx + 9, cy + 4], fill=hexc('#2A2630')); d.ellipse([cx - 8, cy - 11, cx + 8, cy - 5], fill=hexc('#7AE84A')); d.ellipse([cx - 5, cy - 10, cx + 2, cy - 7], fill=hexc('#C8FF8A'))
    for dx in (-4, 0, 4): d.polygon([(cx + dx - 2, cy + 6), (cx + dx, cy + 1), (cx + dx + 2, cy + 6)], fill=hexc('#FF8A3A'))
shared('cauldron', cauldron_out)
# 문 기둥 (양쪽 길 끝에서 다음 지역으로 넘어가는 곳)
def pillar(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 7, cy - 6, cx + 7, cy + 2], fill=hexc('#4E4856')); d.rectangle([cx - 5, cy - 46, cx + 5, cy - 6], fill=hexc('#6E6876')); d.rectangle([cx - 5, cy - 46, cx, cy - 6], fill=hexc('#5E586A'))
    for k in range(-40, -8, 8): d.line([(cx - 5, cy + k), (cx + 5, cy + k)], fill=hexc('#4E4856'))
    d.rectangle([cx - 8, cy - 50, cx + 8, cy - 46], fill=hexc('#4E4856')); d.polygon([(cx - 8, cy - 50), (cx, cy - 58), (cx + 8, cy - 50)], fill=hexc('#3A2A5E'))
    d.line([(cx, cy - 46), (cx, cy - 38)], fill=hexc('#2A2230')); d.ellipse([cx - 4, cy - 38, cx + 4, cy - 28], fill=hexc('#FF9A3A')); d.ellipse([cx - 2, cy - 36, cx + 2, cy - 31], fill=hexc('#FFE08A'))
shared('pillar', pillar)
# ---- 반복 그림 (halloween.py와 같아요) ----
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
shared('pumpkin', pumpkin_at(False)); shared('jack', pumpkin_at(True))
def lantern_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 28, cx, cy], fill=hexc('#2A2230')); d.line([(cx, cy - 28), (cx + 6, cy - 30)], fill=hexc('#2A2230'))
    d.ellipse([cx + 3, cy - 30, cx + 10, cy - 22], fill=hexc('#FF9A3A')); d.ellipse([cx + 5, cy - 28, cx + 8, cy - 24], fill=hexc('#FFE08A'))
shared('lantern', lantern_at)
def tomb_at(kind):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if kind == 0:
            d.rectangle([cx - 4, cy - 10, cx + 4, cy], fill=hexc('#8A8A92')); d.ellipse([cx - 4, cy - 14, cx + 4, cy - 6], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 10, cx - 1, cy], fill=hexc('#9A9AA2'))
            d.line([(cx - 2, cy - 9), (cx + 2, cy - 9)], fill=hexc('#5A5A62')); d.line([(cx - 2, cy - 6), (cx + 2, cy - 6)], fill=hexc('#5A5A62'))
        else:
            d.rectangle([cx - 1, cy - 14, cx + 1, cy], fill=hexc('#8A8A92')); d.rectangle([cx - 4, cy - 11, cx + 4, cy - 9], fill=hexc('#8A8A92'))
        d.ellipse([cx - 6, cy - 2, cx + 6, cy + 2], fill=hexc('#2E3228'))
    return f
shared('tomb0', tomb_at(0)); shared('tomb1', tomb_at(1))
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
def mush_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, r in ((-3, 0, 3), (3, -1, 2), (0, 1, 2)):
        d.rectangle([cx + dx - 1, cy + dy - 3, cx + dx, cy + dy], fill=hexc('#E8E0D0')); d.ellipse([cx + dx - r, cy + dy - 3 - r, cx + dx + r, cy + dy - 3 + r // 2], fill=hexc('#8AE8D8'))
shared('glowmush', mush_at)
def bench_old(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x + .1, y + .35), P(x + .9, y + .35)
    poly(d, [up(a, 5), up(b, 5), up((b[0] - 3, b[1] + 2), 5), up((a[0] - 3, a[1] + 2), 5)], hexc('#5A4232'))
    poly(d, [up(a, 6), up(b, 6), up(b, 11), up(a, 11)], hexc('#4A3626'))
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 5, p_[0], p_[1]], fill=hexc('#2A2230'))
shared('bench', bench_old)
def bush_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx, dy, r in ((-4, -4, 4), (3, -4, 4), (0, -7, 4)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#2E3E30'))
    for dx, dy in ((-3, -7), (2, -9), (4, -5)): d.point((cx + dx, cy + dy), fill=hexc('#C86AE8'))
shared('bush', bush_at)
def crow_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.line([(cx, cy), (cx, cy - 14)], fill=hexc('#5A4A3A')); d.line([(cx - 5, cy - 14), (cx + 5, cy - 14)], fill=hexc('#5A4A3A'))
    d.ellipse([cx - 3, cy - 20, cx + 3, cy - 14], fill=hexc('#1E1A24')); d.ellipse([cx + 1, cy - 22, cx + 4, cy - 18], fill=hexc('#1E1A24')); d.point((cx + 5, cy - 20), fill=hexc('#E0A030'))
shared('crow', crow_at)
# ---------------- 놓기 ----------------
def doorize(o_idx, **dr): objs[o_idx]['door'] = dr
occupied = set()
for o in objs:
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def can(x, y): return (x, y) not in occupied and T.get((x, y)) == 'grass'
def put(name, key, x, y, **kw): place(name, key, x, y, **kw); occupied.add((x, y))
# 학교·시장 쪽으로 돌아가는 문: 큰길 A 서쪽 끝 (기둥 둘, 사이가 길)
put('gate', 'pillar', 3, 12); doorize(len(objs) - 1, tile=[3, 14], to='campus', spawn=[77, 27], label='등불 시장', walk=True, span=[13, 16])
put('gate', 'pillar', 3, 17)
# 일곱 등불 광장
put('sevenpost', 'sevenpost', 62, 7, act=('일곱 등불 기둥', '올려다보기'))
for (x, y) in [(58, 10), (66, 10), (58, 4), (66, 4)]: put('bench', 'bench', x, y, act=('낡은 벤치', '앉아서 쉬기'))
for (x, y) in [(55, 3), (69, 3), (55, 12), (69, 12), (62, 12), (62, 3)]: put('lantern', 'lantern', x, y)
for (x, y) in [(57, 7), (67, 7), (60, 11), (64, 11)]: put('jack', 'jack', x, y, solid=False)
# 비어 있는 등불대 (큰길 B 가운데)
put('emptylamp', 'emptylamp', 46, 27, act=('비어 있는 등불대', '바라보기')); put('bench', 'bench', 47, 27, act=('낡은 벤치', '앉아서 쉬기'))
# 마녀 오두막 옆 솥
put('cauldron', 'cauldron', 13, 28, act=('부글부글 마녀의 솥', '들여다보기'))
# 작은 묘지
GF = set((x, 22) for x in range(54, 67)) | set((x, 28) for x in range(54, 67)) | set((54, y) for y in range(22, 29)) | set((66, y) for y in range(22, 29))
GF -= {(60, 28), (61, 28), (62, 28), (63, 28)}
for (x, y) in sorted(GF):
    if (x, y) not in occupied: put('fence', f'iron{int((x + 1, y) in GF)}{int((x, y + 1) in GF)}', x, y)
for x in range(56, 65, 2):
    for y in range(24, 28, 2):
        if random.random() < .85: put('tomb', random.choice(['tomb0', 'tomb0', 'tomb1']), x, y, act=('오래된 묘비', '읽어 보기'))
# 길가 가로등
LAMPS = [(x, 17) for x in range(6, NX - 2, 6)] + [(x, 33) for x in range(6, NX - 2, 6)] + [(36, y) for y in range(20, 29, 4)] + [(62, y) for y in range(19, 22, 3)]
LAMPS = [t for t in LAMPS if t not in occupied and T.get(t) == 'grass']
for (x, y) in LAMPS: put('lantern', 'lantern', x, y)
for (x, y) in [(23, 18), (41, 18), (50, 18), (17, 34), (40, 34), (57, 34)]:
    if can(x, y): put('bench', 'bench', x, y, act=('낡은 벤치', '앉아서 쉬기'))
for (x, y) in [(14, 35), (30, 36), (44, 37), (52, 36), (60, 38), (22, 40)]:
    if can(x, y): put('glowmush', 'glowmush', x, y, solid=False)
# 숲: 가장자리와 아래쪽은 빽빽, 집 사이 빈 풀밭엔 드문드문
for x in range(NX):
    for y in range(NY):
        if not can(x, y): continue
        edge = min(x, y, NX - 1 - x, NY - 1 - y)
        south = y > 35
        p = .6 if edge < 3 else .4 if south else .05
        if random.random() < p:
            kind = random.choice(['pine', 'pine', 'dead', 'round'] if (edge < 3 or south) else ['round', 'purple', 'dead', 'round'])
            put('tree', 't_' + kind, x, y)
        elif random.random() < .02: put('bush', 'bush', x, y)
        elif random.random() < .008: put('pumpkin', 'jack', x, y, solid=False)
# ---------------- 저장 ----------------
keys = [k for k in SPR if not k.endswith('@')]
rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
for k in sorted(keys, key=lambda k: -SPR[k].height):
    w_, h_ = SPR[k].size
    if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
    pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
for k in keys: sheet.paste(SPR[k], pos[k])
sheet.save('out/quarter_obj.png')
meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
lights = [dict(p=P(x + .5, y + .5), dy=-26, r=30, c=[255, 160, 70], a=.6, f=1) for (x, y) in LAMPS]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-6, r=16, c=[255, 170, 60], a=.55, f=1) for o in objs if o['spr'] == 'jack']
for o in objs:
    if o['door'] and o['name'] != 'gate': x, y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(x, y), dy=-18, r=34, c=[255, 180, 90], a=.45, f=0))
    if o['name'] == 'gate': x, y = P(o['box'][0] + .5, o['box'][1] + .5); lights.append(dict(p=(x, y), dy=-34, r=36, c=[255, 160, 70], a=.6, f=1))
lights += [dict(p=P(62.5, 7.5), dy=-46, r=70, c=[255, 160, 60], a=.65, f=1), dict(p=P(13.5, 28.5), dy=-8, r=30, c=[130, 255, 90], a=.5, f=1), dict(p=P(45, 9), dy=-30, r=50, c=[120, 255, 190], a=.35, f=0),
           dict(p=P(46.5, 27.5), dy=-40, r=26, c=[255, 190, 90], a=.25, f=0)]
lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-3, r=14, c=[120, 240, 220], a=.5, f=0) for o in objs if o['spr'] == 'glowmush']
AREAS = [dict(n='뱀파이어 저택', t=[12, 13]), dict(n='학교 박물관', t=[31, 13]), dict(n='낡은 연구 탑', t=[44, 13]), dict(n='일곱 등불 광장', t=[62, 9]), dict(n='마녀의 오두막', t=[9, 29]),
         dict(n='늑대인간 통나무집', t=[28, 29]), dict(n='비어 있는 등불대', t=[46, 28]), dict(n='작은 묘지', t=[60, 29]), dict(n='등불 시장 쪽 문', t=[4, 14])]
json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, areas=AREAS, water=[[x, y] for (x, y), t in T.items() if t == 'lake'], ponds=[dict(id=POND['id'], name=POND['name'], cx=POND['cx'], cy=POND['cy'], r=max(POND['rx'], POND['ry']) + 1.5)], start=[8, 14]), open('out/quarter.json', 'w'), ensure_ascii=False)
print('objs', len(objs), 'sheet', sheet.size)
