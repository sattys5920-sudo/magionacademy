# 학교 + 마을 한 장짜리 지도(84x72)를 둘로 나눠 더 넓게 펴요: halloween.py 끝에서 run(globals())로 불러요
#   campus = 학교 (강 서쪽), town = 마을·시장 (강 동쪽). 건물·길 사이를 가로 SX배, 세로 SY배로 벌리고 건물 크기는 그대로예요.
#   길(좁은 흙길)은 폭을 그대로 두고 문 앞까지 길을 새로 이어요. 나무·울타리·가로등·호박밭·묘비는 새 땅에 다시 심어요.
#   index.html·데이터의 옛 좌표는 leg2new()로 새 (지도, x, y)로 바꿔요 (tools/split_data.py)
import json, math, random
from collections import deque
from PIL import Image, ImageDraw

SX, SY, M = 2.0, 1.4, 4            # 가로·세로 벌림, 가장자리 여백
CUT = 42                           # 옛 지도에서 강 가운데: 이보다 서쪽은 학교, 동쪽은 마을
LNX, LNY = 84, 72
SPECS = {'campus': dict(lo=0, hi=CUT), 'town': dict(lo=CUT, hi=LNX)}
for k, s in SPECS.items():
    s['NX'] = int(round(SX * (s['hi'] - s['lo']))) + 2 * M; s['NY'] = int(round(SY * LNY)) + 2 * M
    s['OX'] = s['NY'] * 8 + 20; s['OY'] = 160; s['W'] = (s['NX'] + s['NY']) * 8 + 40; s['H'] = (s['NX'] + s['NY']) * 4 + 200

def which(lx): return 'campus' if lx < CUT else 'town'
def tf(mapid, lx, ly):
    s = SPECS[mapid]; return SX * (lx - s['lo']) + M, SY * ly + M
def leg2new(lx, ly):
    """옛 좌표 → (지도, x, y) (칸 중심 기준, 반올림)"""
    m = which(lx); x, y = tf(m, lx, ly); return m, int(round(x)), int(round(y))

def hexc(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
GRASS = [hexc('#3E4E3A'), hexc('#36463A'), hexc('#46563E'), hexc('#3A4436')]
ROAD = ('dirt', 'cobble', 'stone', 'bridge')
FILLS = [   # (종류, x0, y0, x1, y1) 옛 좌표
    ('river', 39, 0, 45, 72), ('bridge', 56, 53, 58, 59),
    ('stone', 14, 24, 28, 30), ('dirt', 19, 30, 22, 70), ('dirt', 2, 26, 39, 29), ('dirt', 2, 51, 39, 54), ('dirt', 6, 37, 9, 51), ('dirt', 28, 37, 31, 51),
    ('soil', 2, 56, 15, 69), ('dirt', 19, 63, 39, 68), ('bridge', 39, 26, 45, 29), ('bridge', 39, 51, 45, 54),
    ('dirt', 45, 26, 84, 29), ('cobble', 53, 18, 68, 37), ('dirt', 62, 12, 65, 21), ('dirt', 60, 34, 63, 70), ('dirt', 63, 46, 71, 49), ('dirt', 63, 58, 77, 61), ('dirt', 45, 51, 60, 54),
    ('grave', 46, 39, 57, 50),
]

def run(g):
    SPR, pos, P_old, OXo, OYo = g['SPR'], g['pos'], g['P'], g['OX'], g['OY']
    legacy, PONDS, EXPL, LAMPS_L, FORAGEZONE = g['objs'], g['PONDS'], g['EXPL'], g['LAMPS_ALL'], g['zone']
    AREAS_L = g['AREAS_LEG']
    out_meta = {}
    DOOR_MAP = {}     # 옛 문 칸 → (지도, 새 문 칸)
    for mapid in ('campus', 'town'):
        S = SPECS[mapid]; NX, NY, OX, OY, W, H = S['NX'], S['NY'], S['OX'], S['OY'], S['W'], S['H']
        random.seed(51 if mapid == 'campus' else 52)
        P = lambda tx, ty: (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
        T = {}
        def fill(kind, x0, y0, x1, y1):
            for x in range(max(0, x0), min(NX, x1)):
                for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
        def ellipse(kind, cx, cy, rx, ry):
            for x in range(NX):
                for y in range(NY):
                    if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 < 1: T[(x, y)] = kind
        # ---------- 땅 ----------
        rivers, bridges = [], []
        def rect(kind, x0, y0, x1, y1):
            cx0, cx1 = max(x0, S['lo']), min(x1, S['hi'])
            if cx1 <= cx0: return None
            nx0, ny0 = tf(mapid, cx0, y0); nx1, ny1 = tf(mapid, cx1, y1)
            if kind == 'dirt':   # 좁은 흙길은 폭을 그대로
                if x1 - x0 <= 4: c = (nx0 + nx1) / 2; nx0, nx1 = c - (x1 - x0) / 2, c + (x1 - x0) / 2
                if y1 - y0 <= 4: c = (ny0 + ny1) / 2; ny0, ny1 = c - (y1 - y0) / 2, c + (y1 - y0) / 2
            a = (int(round(nx0)), int(round(ny0)), int(round(nx1)), int(round(ny1)))
            if cx0 == S['lo'] and S['lo'] > 0 and kind in ('river', 'bridge', 'dirt'): a = (0,) + a[1:]            # 강 서쪽 끝은 지도 가장자리까지
            if cx1 == S['hi'] and S['hi'] < LNX and kind in ('river', 'bridge'): a = a[:2] + (NX,) + a[3:]       # 강 동쪽도 가장자리까지
            return a
        for kind, x0, y0, x1, y1 in FILLS:
            a = rect(kind, x0, y0, x1, y1)
            if not a: continue
            fill(kind, *a)
            if kind == 'river': rivers.append(a)
            if kind == 'bridge': bridges.append(a)
        # 연못·호수
        ponds = []
        for lk in [dict(id='lake', name='유령 호수', cx=56, cy=59, rx=6.5, ry=5)] + PONDS:
            if which(lk['cx']) != mapid: continue
            nx, ny = tf(mapid, lk['cx'], lk['cy']); ellipse('lake', nx, ny, lk['rx'] * SX, lk['ry'] * SY)
            if lk['id'] != 'lake': ponds.append(dict(id=lk['id'], name=lk['name'], cx=nx, cy=ny, r=max(lk['rx'] * SX, lk['ry'] * SY) + 1.5))
        # 호수 잔교는 호수 위에 다시
        for kind, x0, y0, x1, y1 in FILLS:
            if kind == 'bridge' and x1 - x0 == 2:
                a = rect(kind, x0, y0, x1, y1)
                if a: fill('bridge', *a)
        # ---------- 건물·물건 옮기기 ----------
        fixed_drop = {'tree', 'bush', 'fence', 'tomb', 'lantern', 'pumpkin', 'jack', 'gate'}
        objs = []
        for o in legacy:
            if o['name'] in fixed_drop: continue
            b = o['box']; w, d = b[2] - b[0], b[3] - b[1]; cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            if which(cx) != mapid: continue
            ncx, ncy = tf(mapid, cx, cy); x0, y0 = int(round(ncx - w / 2)), int(round(ncy - d / 2))
            dx, dy = x0 - b[0], y0 - b[1]
            n = dict(o); n['box'] = [x0, y0, x0 + w, y0 + d]
            n['x'] = o['x'] + (OX + (x0 - y0) * 8) - (OXo + (b[0] - b[1]) * 8); n['y'] = o['y'] + (OY + (x0 + y0) * 4) - (OYo + (b[0] + b[1]) * 4)
            if o['door']:
                dr = json.loads(json.dumps(o['door'])); ot = list(dr['tile']); dr['tile'] = [ot[0] + dx, ot[1] + dy]
                if 'span' in dr: dr['span'] = [dr['span'][0] + dy, dr['span'][1] + dy]
                if 'spanX' in dr: dr['spanX'] = [dr['spanX'][0] + dx, dr['spanX'][1] + dx]
                n['door'] = dr; DOOR_MAP[tuple(ot)] = (mapid, dr['tile'][0], dr['tile'][1])
            objs.append(n)
        def solid_tiles():
            s = set()
            for o in objs:
                if o['solid']:
                    b = o['box']
                    for x in range(b[0], b[2]):
                        for y in range(b[1], b[3]): s.add((x, y))
            return s
        # ---------- 문 앞 길 이어 주기 ----------
        sol = solid_tiles(); WATER = ('river', 'lake')
        for o in objs:
            dr = o['door']
            if not dr or dr.get('walk') or o['name'] in ('exit',): continue
            st = tuple(dr['tile'])
            if T.get(st) in ROAD: continue
            seen = {st: None}; q = deque([st]); hit = None
            while q and hit is None:
                c = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (c[0] + dx, c[1] + dy)
                    if n in seen or not (1 <= n[0] < NX - 1 and 1 <= n[1] < NY - 1) or n in sol or T.get(n) in WATER: continue
                    seen[n] = c
                    if T.get(n) in ROAD: hit = n; break
                    q.append(n)
            if hit is None: continue
            c = seen[hit]
            while c is not None:
                T[c] = 'dirt'
                for nb in ((c[0] + 1, c[1]), (c[0], c[1] + 1)):
                    if nb not in sol and T.get(nb) not in WATER + ('bridge',) and nb[0] < NX - 1 and nb[1] < NY - 1 and T.get(nb) != 'soil': T[nb] = 'dirt'
                c = seen[c]
        for (x, y) in list(T): pass
        for x in range(NX):
            for y in range(NY): T.setdefault((x, y), 'grass')
        # ---------- 탐사장 문 (남·서·북·동) ----------
        gates = []   # (지역 번호, 기둥 둘, 문)
        def road_row(ly0, ly1):   # 옛 길 가로줄 → 새 줄
            return int(round(tf(mapid, S['lo'], ly0)[1])), int(round(tf(mapid, S['lo'], ly1)[1]))
        def add_gate(e, pa, pb, door, back, corridor):
            fill('dirt', *corridor)
            key = e[3]
            ox, oy = SPR[key + '@']
            for (px_, py_) in (pa, pb):
                b = P(px_ + .5, py_ + .5); objs.append(dict(name='gate', spr=key, box=[px_, py_, px_ + 1, py_ + 1], x=int(b[0] + ox), y=int(b[1] + oy), door=None, solid=True, act=None))
            objs[-2]['door'] = dict(to=None, label=f'{e[2]}쪽 길 · {e[1]}', walk=True, explore=e[0], back=back, **door)
            gates.append((e, pa, pb))
        by = {e[2]: e for e in EXPL}
        if mapid == 'campus':
            # 서쪽: 학교 동서 길 서쪽 끝
            r0, r1 = road_row(26, 29); yc = (r0 + r1) // 2
            add_gate(by['서'], (M, yc - 3), (M, yc + 3), dict(tile=[M, yc], span=[yc - 2, yc + 2]), [M + 4, yc], (0, yc - 2, M + 6, yc + 3))
        if mapid == 'town':
            # 남쪽: 광장 남쪽 길 끝, 북쪽: 광장 위 길, 동쪽: 광장에서 동쪽
            sx_c = int(round(tf('town', 61.5, 0)[0]))
            add_gate(by['남'], (sx_c - 4, NY - M - 1), (sx_c + 3, NY - M - 1), dict(tile=[sx_c, NY - M - 1], spanX=[sx_c - 2, sx_c + 1]), [sx_c, NY - M - 5], (sx_c - 2, NY - M - 6, sx_c + 2, NY))
            nx_c = int(round(tf('town', 51, 0)[0]))
            top = int(round(tf('town', 0, 18)[1]))
            add_gate(by['북'], (nx_c - 4, M + 1), (nx_c + 3, M + 1), dict(tile=[nx_c, M + 1], spanX=[nx_c - 2, nx_c + 1]), [nx_c, M + 5], (nx_c - 2, 0, nx_c + 2, top + 1))
            ey = int(round(tf('town', 0, 36)[1]))
            add_gate(by['동'], (NX - M - 1, ey - 3), (NX - M - 1, ey + 3), dict(tile=[NX - M - 1, ey], span=[ey - 2, ey + 2]), [NX - M - 6, ey], (int(round(tf('town', 68, 0)[0])) - 1, ey - 2, NX, ey + 3))
            # 그림자 골목 문: 시장 거리 동쪽 끝
            r0, r1 = road_row(26, 29); yc = (r0 + r1) // 2
            e0 = ('x', '그림자 골목', '', 'pillar')
            key = 'pillar'; ox, oy = SPR[key + '@']
            for (px_, py_) in ((NX - M - 2, yc - 3), (NX - M - 2, yc + 3)):
                b = P(px_ + .5, py_ + .5); objs.append(dict(name='gate', spr=key, box=[px_, py_, px_ + 1, py_ + 1], x=int(b[0] + ox), y=int(b[1] + oy), door=None, solid=True, act=None))
            objs[-2]['door'] = dict(tile=[NX - M - 2, yc], to='quarter', spawn=[8, 14], label='그림자 골목', walk=True, span=[yc - 2, yc + 2])
            fill('dirt', NX - M - 6, yc - 2, NX, yc + 3)
            gates.append((None, (NX - M - 2, yc - 3), (NX - M - 2, yc + 3)))
        # ---------- 학교 ↔ 마을 (다리 끝을 걸으면 넘어가요) ----------
        cross = []
        for (kind, x0, y0, x1, y1) in FILLS:
            if kind == 'bridge' and x1 - x0 == 6:
                r = rect(kind, x0, y0, x1, y1)
                if r: cross.append((r[1], r[3]))
        other = 'town' if mapid == 'campus' else 'campus'
        for (ya, yb) in cross:
            yc = (ya + yb) // 2
            if mapid == 'campus': tx = NX - 2; sp = [3, yc]
            else: tx = 1; sp = [SPECS['campus']['NX'] - 4, yc]
            lab = '마을·시장으로' if mapid == 'campus' else '학교로'
            objs.append(dict(name='exit', box=[tx, yc, tx + 1, yc + 1], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[tx, yc], to=other, spawn=sp, label=lab, walk=True, span=[ya, yb - 1]), solid=False, act=None))
        # ---------- 다시 심기 ----------
        sol = solid_tiles()
        occupied = set(sol)
        for (e, pa, pb) in gates:
            occupied |= {(x, y) for x in range(min(pa[0], pb[0]) - 3, max(pa[0], pb[0]) + 4) for y in range(min(pa[1], pb[1]) - 3, max(pa[1], pb[1]) + 4)}
        for (ya, yb) in cross:
            for x in (list(range(NX - 8, NX)) if mapid == 'campus' else list(range(0, 8))):
                for y in range(ya - 2, yb + 2): occupied.add((x, y))
        ox_, oy_ = {}, {}
        def pl(name, key, tx, ty, w=1, d=1, solid=True, act=None):
            ox, oy = SPR[key + '@']; b = P(tx + .5, ty + .5)
            objs.append(dict(name=name, spr=key, box=[tx, ty, tx + w, ty + d], x=int(b[0] + ox), y=int(b[1] + oy), door=None, solid=solid, act=act)); occupied.add((tx, ty))
        def can(x, y): return 0 <= x < NX and 0 <= y < NY and (x, y) not in occupied and T.get((x, y)) == 'grass'
        # 호박밭 (옛 soil 칸에 격자로)
        soils = [t for t, k in T.items() if k == 'soil']
        for (x, y) in sorted(soils):
            if x % 3 == 0 and y % 2 == 0 and (x, y) not in occupied: pl('pumpkin', 'jack' if random.random() < .15 else 'pumpkin', x, y, solid=False, act=('잘 익은 호박', '수확하기'))
        # 묘지: 울타리 + 묘비
        gr = [t for t, k in T.items() if k == 'grave']
        if gr:
            gx0, gx1, gy0, gy1 = min(t[0] for t in gr), max(t[0] for t in gr), min(t[1] for t in gr), max(t[1] for t in gr)
            GF = {(x, gy0 - 1) for x in range(gx0 - 1, gx1 + 2)} | {(x, gy1 + 1) for x in range(gx0 - 1, gx1 + 2)} | {(gx0 - 1, y) for y in range(gy0 - 1, gy1 + 2)} | {(gx1 + 1, y) for y in range(gy0 - 1, gy1 + 2)}
            mid = (gx0 + gx1) // 2; GF -= {(mid, gy1 + 1), (mid + 1, gy1 + 1)}
            for (x, y) in sorted(GF):
                if (x, y) not in occupied and 0 <= x < NX and 0 <= y < NY: pl('fence', f'iron{int((x + 1, y) in GF)}{int((x, y + 1) in GF)}', x, y)
            for x in range(gx0 + 1, gx1, 3):
                for y in range(gy0 + 1, gy1, 3):
                    if random.random() < .8 and (x, y) not in occupied: pl('tomb', random.choice(['tomb0', 'tomb0', 'tomb1']), x, y, act=('오래된 묘비', '읽어 보기'))
            for t in ((gx0 + 1, gy0 + 3), (gx1 - 1, gy0 + 1), (mid, gy1 - 1)):
                if t not in occupied: pl('tree', 't_dead', *t)
            for x in range(gx0 - 2, gx1 + 3):
                for y in range(gy0 - 2, gy1 + 3): occupied.add((x, y))
        # 가로등: 옛 자리 → 새 자리
        lamps = []
        for (lx, ly) in LAMPS_L:
            if which(lx) != mapid: continue
            nx, ny = tf(mapid, lx + .5, ly + .5); t = (int(round(nx - .5)), int(round(ny - .5)))
            if t not in occupied and T.get(t) not in WATER and 1 <= t[0] < NX - 1 and 1 <= t[1] < NY - 1: lamps.append(t)
        # 길을 따라 가로등 더 (큰길 양쪽 끝에서 끝까지 8칸마다)
        for y in range(2, NY - 2):
            for x in range(2, NX - 2):
                if T.get((x, y)) == 'dirt' and T.get((x, y + 1)) == 'grass' and (x * 5 + y * 3) % 17 == 0 and (x, y + 1) not in occupied: lamps.append((x, y + 1))
        lamp_set = []
        for t in lamps:
            if all(abs(t[0] - u[0]) + abs(t[1] - u[1]) >= 7 for u in lamp_set) and t not in occupied: lamp_set.append(t)
        for t in lamp_set: pl('lantern', 'lantern', *t)
        # 숲: 가장자리 + 마을 남동쪽
        for x in range(NX):
            for y in range(NY):
                if not can(x, y): continue
                lx, ly = (x - M) / SX + S['lo'], (y - M) / SY
                edge = min(x, y, NX - 1 - x, NY - 1 - y)
                forest = mapid == 'town' and lx > 66 and ly > 50
                p = .55 if edge < 3 else .3 if forest else .035
                if random.random() < p:
                    kind = random.choice(['pine', 'pine', 'dead', 'round'] if (edge < 3 or forest) else ['round', 'purple', 'dead', 'round'])
                    pl('tree', 't_' + kind, x, y)
                elif random.random() < .012: pl('bush', 'bush', x, y)
                elif random.random() < .005: pl('jack', 'jack', x, y, solid=False)
        # ---------- 땅 그림 ----------
        bg = Image.new('RGBA', (W, H), hexc('#140E1E')); px = bg.load()
        rv = rivers[0] if rivers else None
        for yy in range(H):
            for xx in range(W):
                a, b = (xx - OX) / 8, (yy - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
                if not (0 <= fx < NX and 0 <= fy < NY): continue
                t = T[(int(fx), int(fy))]
                if t == 'dirt':
                    c = hexc('#6A5444') if random.random() > .12 else hexc('#5E4A3C')
                    if random.random() < .02: c = hexc('#7E6A58')
                elif t in ('stone', 'cobble'):
                    s_ = 3 if t == 'cobble' else 2
                    bx, by_ = int(fx * s_ + (int(fy * s_) % 2) * .5), int(fy * s_)
                    c = [hexc('#7A7480'), hexc('#6E6876'), hexc('#86808C')][(bx * 5 + by_ * 3) % 3]
                    if (fx * s_ + (int(fy * s_) % 2) * .5) % 1 < .1 or (fy * s_) % 1 < .12: c = hexc('#4E4856')
                elif t == 'river':
                    c = hexc('#2A4A5A') if (int(fx * 2) + int(fy * 4)) % 5 else hexc('#3A5E6E')
                    if random.random() < .01: c = hexc('#8AC8D8')
                    if rv and (fx < rv[0] + .25 or fx > rv[2] - .25) and 0 < rv[0] + .25 < NX and not (rv[0] == 0 and fx < 1) and not (rv[2] == NX and fx > NX - 1): c = hexc('#4A3E36')
                elif t == 'lake':
                    c = hexc('#2E5A6A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#4A7A8A')
                    if random.random() < .015: c = hexc('#A8E8F0')
                elif t == 'bridge':
                    c = hexc('#7A5A3E') if int(fy * 3) % 2 else hexc('#6A4C34')
                    if (fy * 3) % 1 < .1: c = hexc('#3A2A1E')
                    for (bx0, by0, bx1, by1) in bridges:
                        if bx1 - bx0 > 4 and bx0 <= fx < bx1 and ((fy - int(fy)) < .08 and int(fy) in (by0, by1 - 1) or (fy - int(fy)) > .92 and int(fy) in (by0, by1 - 1)): c = hexc('#4A3424')
                elif t == 'soil':
                    c = hexc('#4A3426') if (fy * 2) % 1 < .5 else hexc('#3E2C20')
                elif t == 'grave':
                    c = [hexc('#3A3E34'), hexc('#34382E'), hexc('#42463A')][random.randint(0, 2)]
                else:
                    c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
                    if random.random() < .004: c = random.choice([hexc('#C86AE8'), hexc('#E8A050'), hexc('#8AE8C8')])
                px[xx, yy] = c
        for xx in range(W):
            for yy in range(H):
                if px[xx, yy][:3] != (0x14, 0x0E, 0x1E): continue
                a, b = (xx - OX) / 8, (yy - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
                if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[xx, yy] = hexc('#3A2A24') if (yy // 3) % 2 else hexc('#2E221E')
        bgname = 'hw_bg.png' if mapid == 'campus' else 'town_bg.png'
        bg.save('out/' + bgname); print(mapid, 'bg', W, H, 'objs', len(objs))
        # ---------- 저장 ----------
        meta = []
        for o in objs:
            if 'sx' in o: meta.append(o); continue
            meta.append(dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']))
        lights = [dict(p=P(x + .5, y + .5), dy=-26, r=30, c=[255, 160, 70], a=.6, f=1) for (x, y) in lamp_set]
        lights += [dict(p=P(o['box'][0] + .5, o['box'][1] + .5), dy=-6, r=16, c=[255, 170, 60], a=.55, f=1) for o in objs if o.get('spr') == 'jack']
        for o in objs:
            if o['door'] and not o['door'].get('explore') and o['name'] not in ('gate', 'exit'):
                x, y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(x, y), dy=-18, r=34, c=[255, 180, 90], a=.45, f=0))
        def lpix(lx, ly, dy, r, c, a, f):
            nx, ny = tf(mapid, lx, ly)
            if 0 <= nx < NX and 0 <= ny < NY and which(lx) == mapid: lights.append(dict(p=P(nx, ny), dy=dy, r=r, c=c, a=a, f=f))
        lpix(61, 27.5, -18, 60, [255, 160, 60], .6, 1); lpix(69.5, 47.5, -8, 30, [130, 255, 90], .5, 1); lpix(22, 59.5, -16, 46, [120, 255, 140], .3, 0); lpix(56, 59, 0, 70, [90, 200, 230], .25, 0)
        for (e, pa, pb) in gates:
            col = e[9] if e else [255, 160, 70]
            for q in (pa, pb): lights.append(dict(p=P(q[0] + .5, q[1] + .5), dy=-34, r=36, c=col, a=.6, f=1))
        WATERL = [[x, y] for (x, y), t in T.items() if t in ('river', 'lake')]
        FOR = []
        for x in range(2, NX - 2):
            for y in range(2, NY - 2):
                if (x, y) in occupied or T[(x, y)] not in ('grass', 'grave') or (x * 7 + y * 3) % 5: continue
                lx, ly = (x - M) / SX + S['lo'], (y - M) / SY
                FOR.append([x, y, 'g' if T[(x, y)] == 'grave' else FORAGEZONE(int(max(0, min(LNX - 1, lx))), int(max(0, min(LNY - 1, ly))))])   # 묘지 칸은 묘지 채집 (옛 좌표로 구역을 찾으면 묘지가 빠져요)
        areas = []
        for a in AREAS_L:
            ax, ay = a['t']
            if which(ax) == mapid: _, nx, ny = leg2new(ax, ay); areas.append(dict(n=a['n'], t=[nx, ny]))
        for (e, pa, pb) in gates:
            if e: areas.insert(0, dict(n=f'{e[2]}쪽 길 · {e[1]}', t=[(pa[0] + pb[0]) // 2, (pa[1] + pb[1]) // 2]))
        _, sx0, sy0 = leg2new(20, 30)
        out_meta[mapid] = dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, water=WATERL, ponds=ponds, forage=FOR, areas=areas, start=[sx0, sy0], cross=cross, river=(list(rivers[0]) if rivers else None))
        json.dump(out_meta[mapid], open('out/hw.json' if mapid == 'campus' else 'out/town.json', 'w'), ensure_ascii=False)
    # 옛 문 칸 → 새 문 칸 (인테리어에서 돌아 나올 때 쓰는 대응표)
    json.dump({f'{k[0]},{k[1]}': v for k, v in DOOR_MAP.items()}, open('out/door_map.json', 'w'))
    print('split done', {k: (v['NX'], v['NY']) for k, v in out_meta.items()})
