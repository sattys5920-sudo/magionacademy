# 실내 방들: 과자 교실, 공예 교실, 기숙사 휴게실 4종, 독초 온실
import json, math, random
from PIL import Image, ImageDraw
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#1A0F12')
class Room:
    def __init__(self, NX, NY, wall=70):
        self.NX, self.NY, self.WALL = NX, NY, wall
        self.W, self.H = (NX + NY) * 8 + 40, (NX + NY) * 4 + wall + 50
        self.OX, self.OY = NY * 8 + 20, wall + 12
        self.bg = Image.new('RGBA', (self.W, self.H), hexc('#140D1E')); self.px = self.bg.load()
        self.objs, self.lights = [], []
    def P(self, tx, ty): return (self.OX + (tx - ty) * 8, self.OY + (tx + ty) * 4)
    def inv(self, x, y):
        a, b = (x - self.OX) / 8, (y - self.OY) / 4; return (a + b) / 2, (b - a) / 2
    def put(self, x, y, c):
        if 0 <= int(x) < self.W and 0 <= int(y) < self.H: self.px[int(x), int(y)] = c
    def floor(self, fn):
        for y in range(self.H):
            for x in range(self.W):
                fx, fy = self.inv(x, y)
                if 0 <= fx < self.NX and 0 <= fy < self.NY:
                    c = fn(fx, fy); k = .8 + .2 * min(1, (fx + fy) / (self.NX + self.NY) * 1.6)
                    if fx < .5 or fy < .5: k *= .75
                    self.px[x, y] = shade(c, k)
    def wall_px(self, side, u, v):
        TOP, LEFT = self.P(0, 0), self.P(0, self.NY)
        if side == 'L': return LEFT[0] + u, LEFT[1] - u / 2 - v
        return TOP[0] + u, TOP[1] + u / 2 - v
    def wall_fill(self, side, fn, u0=0, u1=None, v0=0, v1=None):
        u1 = u1 if u1 is not None else (self.NY if side == 'L' else self.NX) * 8; v1 = v1 if v1 is not None else self.WALL
        for u in range(int(u0), int(u1)):
            for v in range(int(v0), int(v1)):
                c = fn(u, v) if callable(fn) else fn
                if c: self.put(*self.wall_px(side, u, v), c)
    def walls(self, paper, paper2, wain, trim='#C49446', dark=(.86, 1.0)):
        for side, dk in (('L', dark[0]), ('R', dark[1])):
            def f(u, v, dk=dk):
                if v < 24:
                    c = hexc(wain); pu = u % 16
                    if pu in (0, 1) or v in (3, 21): c = shade(hexc(wain), .78)
                    elif pu == 2 or v == 4: c = shade(hexc(wain), 1.15)
                    if v >= 22: c = shade(hexc(wain), .7)
                    if v == 23: c = hexc(trim)
                    return shade(c, dk)
                if v >= self.WALL - 4: return shade(hexc(trim) if v == self.WALL - 1 else shade(hexc(wain), .8), dk)
                a, b = u % 12, (v - 24) % 14
                c = hexc(paper)
                if (a - 6) ** 2 / 9 + (b - 7) ** 2 / 16 < 1 and not ((a - 6) ** 2 / 3 + (b - 7) ** 2 / 7 < 1): c = hexc(paper2)
                return shade(c, dk * (.82 + .18 * v / self.WALL))
            self.wall_fill(side, f)
        TOP = self.P(0, 0)
        for v in range(self.WALL):
            for d in (-1, 0, 1): self.put(TOP[0] + d, TOP[1] - v, hexc('#3A2116') if d else hexc('#6A4128'))
    def edge_shadow(self):
        for x in range(self.W):
            for y in range(self.H):
                fx, fy = self.inv(x, y)
                if 0 <= fx < self.NX and 0 <= fy < self.NY and (fx < .45 or fy < .45): self.px[x, y] = shade(self.px[x, y], .7 + .3 * min(fx, fy) / .45)
    def window(self, side, u0, w=16, v0=28, h=34, glass=('#28406E', '#3D62A0', '#7FA6E0'), frame='#2E1B12', moon=True):
        fr, gl, gl2, gl3 = hexc(frame), hexc(glass[0]), hexc(glass[1]), hexc(glass[2])
        def f(u, v):
            uu, vv = u - u0, v - v0
            if not (0 <= uu < w and 0 <= vv < h): return None
            cx = w / 2; top = h - cx
            if vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > cx ** 2: return None
            if uu < 2 or uu >= w - 2 or vv < 2 or (vv > top and (uu + .5 - cx) ** 2 + (vv - top) ** 2 > (cx - 2) ** 2): return fr
            if uu in (w // 2 - 1, w // 2) or vv in (12, 24): return fr
            g = gl2 if (uu + vv) % 9 == 0 else gl
            if uu < w // 2 and 14 < vv < 22 and uu > 3: g = gl3 if (uu + vv) % 3 == 0 else gl2
            if moon and (uu - 11) ** 2 + (vv - 28) ** 2 < 5: g = hexc('#F2E8B0')
            return g
        self.wall_fill(side, f)
        x, y = self.wall_px(side, u0 + w / 2, v0 + h / 2); self.lights.append(dict(p=(x, y), dy=0, r=26, c=[110, 150, 255], a=.25, f=0))
    def sconce(self, side, u):
        self.wall_fill(side, hexc('#C49446'), u, u + 3, 36, 38); self.wall_fill(side, hexc('#F2E6C8'), u + 1, u + 2, 38, 43); self.wall_fill(side, hexc('#FFD27A'), u + 1, u + 2, 43, 45)
        x, y = self.wall_px(side, u + 1, 44); self.lights.append(dict(p=(x, y), dy=0, r=18, c=[255, 190, 110], a=.5, f=1))
    def shelf(self, side, u0, w, h, items):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < w and 0 <= v < h): return None
            if uu < 2 or uu >= w - 2 or v >= h - 2 or v < 1: return hexc('#3E2216')
            row = (v - 1) % 11
            if row in (0, 1): return hexc('#55311F')
            bi = (uu + (v // 11) * 3) // 3
            c = hexc(items[(bi * 5 + v // 11) % len(items)])
            return shade(c, .7) if uu % 3 == 0 else c
        self.wall_fill(side, f)
    def box(self, img, tx, ty, w, dp, h, top, left, right, lift=0):
        d = ImageDraw.Draw(img); P = self.P
        T_, R, B, L = P(tx, ty), P(tx + w, ty), P(tx + w, ty + dp), P(tx, ty + dp)
        pl = lambda pts, c: d.polygon([tuple(map(int, p)) for p in pts], fill=c)
        pl([up(L, lift), up(B, lift), up(B, lift + h), up(L, lift + h)], hexc(left) if isinstance(left, str) else left)
        pl([up(B, lift), up(R, lift), up(R, lift + h), up(B, lift + h)], hexc(right) if isinstance(right, str) else right)
        pl([up(T_, lift + h), up(R, lift + h), up(B, lift + h), up(L, lift + h)], hexc(top) if isinstance(top, str) else top)
    def obj(self, name, tiles, draw, act=None, solid=True):
        img = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0)); draw(img, ImageDraw.Draw(img))
        bb = img.getbbox(); bb = (bb[0] - 1, bb[1] - 1, bb[2] + 1, bb[3] + 1); spr = img.crop(bb)
        a = spr.load(); w, h = spr.size; add = []
        for y in range(h):
            for x in range(w):
                if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200 for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): add.append((x, y))
        for x, y in add: a[x, y] = OUTL
        self.objs.append(dict(name=name, tiles=tiles, x=bb[0], y=bb[1], img=spr, act=act, solid=solid))
    def light(self, tx, ty, dy, r, c, a=.5, f=1):
        self.lights.append(dict(p=self.P(tx, ty), dy=dy, r=r, c=c, a=a, f=f))
    def save(self, key, title, sub, back_spawn):
        self.edge_shadow(); self.bg.save(f'out/{key}_bg.png')
        sw = sum(o['img'].width + 1 for o in self.objs); sh = max(o['img'].height for o in self.objs)
        sheet = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); sx = 0; meta = []
        for o in self.objs:
            sheet.paste(o['img'], (sx, 0)); xs = [t[0] for t in o['tiles']]; ys = [t[1] for t in o['tiles']]
            meta.append(dict(name=o['name'], box=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], sx=sx, sy=0, sw=o['img'].width, sh=o['img'].height, x=o['x'], y=o['y'], door=None, solid=o['solid'], act=o['act'])); sx += o['img'].width + 1
        sheet.save(f'out/{key}_obj.png')
        ex = self.NX // 2
        meta.append(dict(name='exit', box=[ex, self.NY - 1, ex + 1, self.NY], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[ex, self.NY - 1], to='campus', label='호박달 마녀학교', spawn=back_spawn), solid=False, act=None))
        json.dump(dict(W=self.W, H=self.H, NX=self.NX, NY=self.NY, OX=self.OX, OY=self.OY, objs=meta, lights=self.lights, title=title, sub=sub,
                       bgSrc=f'art/iso/{key}_bg.png', objSrc=f'art/iso/{key}_obj.png', indoor=True, vw=185, fill='#0C0715', spawnIn=[ex, self.NY - 2]), open(f'out/{key}.json', 'w'), ensure_ascii=False)
        print(key, self.W, self.H, len(self.objs))
def checker(c1, c2, s=1):
    def f(fx, fy):
        c = hexc(c1) if (int(fx * s) + int(fy * s)) % 2 else hexc(c2)
        if (fx * s) % 1 < .05 or (fy * s) % 1 < .05: c = shade(c, .85)
        return c
    return f
def planks(cols, seam='#3C2116'):
    def f(fx, fy):
        band = int(fy * 3); along = fx + (band % 2) * .5
        c = hexc(cols[(int(along * 1.5) * 3 + band * 7) % len(cols)])
        if (fy * 3) % 1 < .12 or (along * 1.5) % 1 < .06: c = hexc(seam)
        return c
    return f
def rug(base, x0, y0, x1, y1, col, border='#C49446', inner=None):
    def f(fx, fy):
        if x0 <= fx < x1 and y0 <= fy < y1:
            e = min(fx - x0, x1 - fx, fy - y0, y1 - fy)
            if e < .15: return hexc(border)
            if e < .3: return shade(hexc(col), .7)
            if inner and abs((fx - (x0 + x1) / 2)) + abs(fy - (y0 + y1) / 2) < 1: return hexc(inner)
            return hexc(col)
        return base(fx, fy)
    return f
# 공용 소품 그리기
def cauldron_draw(R, tx, ty, brew, s=1.0):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); r = int(9 * s)
        d.ellipse([cx - r, cy - int(10 * s), cx + r, cy + int(4 * s)], fill=hexc('#2A2630')); d.ellipse([cx - r, cy - int(10 * s), cx + r, cy + int(1 * s)], fill=hexc('#3A3644'))
        d.ellipse([cx - r + 3, cy - int(10 * s) + 1, cx + r - 3, cy - int(5 * s) - 1], fill=hexc(brew)); d.ellipse([cx - r + 5, cy - int(10 * s) + 1, cx, cy - int(7 * s)], fill=shade(hexc(brew), 1.3))
        for dx in (-int(4 * s), 0, int(4 * s)): d.polygon([(cx + dx - 2, cy + int(6 * s)), (cx + dx, cy + int(1 * s)), (cx + dx + 2, cy + int(6 * s))], fill=hexc('#FF8A3A'))
    return f
def plant_draw(R, tx, ty, leaf='#3E6A4E', flower='#C86AE8'):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        d.polygon([(cx - 4, cy - 7), (cx + 4, cy - 7), (cx + 3, cy), (cx - 3, cy)], fill=hexc('#A8563A'))
        for dx, dy, r in ((-4, -14, 4), (3, -15, 4), (0, -19, 4), (-1, -11, 3), (4, -10, 3)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc(leaf))
        for dx, dy in ((-3, -16), (2, -20)): d.point((cx + dx, cy + dy), fill=hexc(flower))
    return f
def float_candle(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        d.rectangle([cx - 1, cy - 52, cx, cy - 46], fill=hexc('#F2E6C8')); d.rectangle([cx - 1, cy - 54, cx, cy - 53], fill=hexc('#FFD27A'))
    R.obj('candle', [(int(tx), int(ty))], f, solid=False); R.light(tx + .5, ty + .5, -52, 30, [255, 200, 120], .5, 1)
# ================= 과자 교실 =================
def candy_room():
    R = Room(16, 12)
    R.floor(rug(checker('#E8D8C0', '#B88A6A'), 6, 5, 10, 11, '#C84A6A', inner='#F2C84A'))
    R.walls('#E89A7A', '#F2B898', '#F2EEE4', trim='#C86A4A')
    # 뒤 벽: 벽돌 오븐 2개 + 메뉴 칠판
    def oven(u0):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < 26 and 0 <= v < 46): return None
            if v >= 42: return hexc('#8A3A2A')
            c = hexc('#A84A3A') if ((v // 4) + (uu // 6 if (v // 4) % 2 else (uu + 3) // 6)) % 2 else hexc('#B85A44')
            if v % 4 == 0 or (uu + ((v // 4) % 2) * 3) % 6 == 0: c = hexc('#7A3426')
            if 6 <= uu < 20 and 8 <= v < 24:
                top = 24 - 7
                if v > top and (uu - 13) ** 2 + (v - top) ** 2 > 49: return c
                return hexc('#FF9A3A') if v < 12 else hexc('#FFD27A') if v < 15 and 9 < uu < 17 else hexc('#3A1A10')
            return c
        R.wall_fill('R', f); x, y = R.wall_px('R', u0 + 13, 14); R.lights.append(dict(p=(x, y), dy=0, r=34, c=[255, 160, 70], a=.55, f=1))
    oven(10); oven(92)
    def menu(u, v):
        uu, vv = u - 46, v - 30
        if not (0 <= uu < 36 and 0 <= vv < 28): return None
        if uu < 2 or uu >= 34 or vv < 2 or vv >= 26: return hexc('#6A4A2E')
        if vv in (20, 21) and 4 <= uu < 24 and uu % 3: return hexc('#F2E8D0')
        if vv in (14, 15) and 4 <= uu < 30 and (uu // 2) % 3: return hexc('#FF9ACA')
        if vv in (8, 9) and 4 <= uu < 18 and uu % 2: return hexc('#F2E8D0')
        if (uu - 27) ** 2 + (vv - 8) ** 2 < 10: return hexc('#E07A1E')
        return hexc('#2A3A34')
    R.wall_fill('R', menu)
    # 옆 벽: 사탕 병 선반 + 창문
    def jars(u, v):
        uu = u - 6
        if not (0 <= uu < 40 and 0 <= v < 48): return None
        if v % 12 < 2: return hexc('#8A5A3A')
        slot, lv = uu // 6, v % 12
        if uu % 6 == 5 or lv > 10: return None
        c = ['#FF6A9A', '#7AE8C8', '#FFD86A', '#C08AFF', '#FF9A4A', '#8AC8FF'][(slot + v // 12) % 6]
        if lv > 8: return hexc('#E8E0D8')
        return hexc(c) if (uu + lv) % 3 else hexc('#F8F4F0')
    R.wall_fill('L', jars); R.window('L', 62)
    R.sconce('R', 40); R.sconce('R', 86); R.sconce('L', 54)
    # 조리대 (반죽 그릇·쿠키 판·사탕 냄비)
    def counter(tx, ty, items):
        def f(img, d):
            R.box(img, tx, ty, 2, 1, 12, '#F2EEE4', '#B88A6A', '#C89A7A')
            for k, it in enumerate(items):
                x, y = R.P(tx + .5 + k, ty + .5); y -= 12
                if it == 'bowl': d.ellipse([x - 4, y - 4, x + 4, y + 1], fill=hexc('#E8E0D8')); d.ellipse([x - 3, y - 4, x + 3, y - 1], fill=hexc('#F2D8A8'))
                elif it == 'tray': d.polygon([(x - 6, y - 1), (x, y - 4), (x + 6, y - 1), (x, y + 2)], fill=hexc('#8A8A92')); [d.ellipse([x + dx - 1, y - 2 + dy, x + dx + 1, y + dy], fill=hexc('#C88A4A')) for dx, dy in ((-3, 0), (0, -1), (3, 0), (0, 1))]
                elif it == 'pot': d.ellipse([x - 4, y - 6, x + 4, y], fill=hexc('#5A5A62')); d.ellipse([x - 3, y - 6, x + 3, y - 3], fill=hexc('#E0904A'))
                elif it == 'pie': d.ellipse([x - 5, y - 3, x + 5, y + 1], fill=hexc('#C8864A')); d.ellipse([x - 4, y - 3, x + 4, y], fill=hexc('#E07A1E'))
        return f
    for (x, y, it) in ((3, 4, ['bowl', 'tray']), (11, 4, ['pot', 'bowl']), (3, 8, ['pie', 'tray']), (11, 8, ['bowl', 'pie'])):
        R.obj('counter', [(x, y), (x + 1, y)], counter(x, y, it), act=('과자 조리대', '과자 만들기'))
    R.obj('cauldron', [(7, 2)], cauldron_draw(R, 7, 2, '#C8864A', 1.3), act=('카라멜 솥', '카라멜 젓기')); R.light(7.5, 2.5, -10, 30, [255, 170, 80], .5)
    def cotton(img, d):
        cx, cy = R.P(14.5, 2.5)
        R.box(img, 14.1, 2.1, .8, .8, 10, '#F2EEE4', '#C84A6A', '#E06A8A')
        for dx, dy, r in ((-3, -16, 5), (3, -17, 5), (0, -21, 5)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#FFB8DA'))
    R.obj('cotton', [(14, 2)], cotton, act=('솜사탕 기계', '솜사탕 만들기'))
    def lolli(img, d):
        cx, cy = R.P(1.5, 10.5)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy], fill=hexc('#8A5A3A'))
        for k, (dx, c) in enumerate(((-3, '#FF6A9A'), (0, '#7AE8C8'), (3, '#FFD86A'))):
            d.line([(cx + dx, cy - 4), (cx + dx, cy - 14 - k * 2)], fill=hexc('#F2EEE4')); d.ellipse([cx + dx - 3, cy - 20 - k * 2, cx + dx + 3, cy - 14 - k * 2], fill=hexc(c))
    R.obj('lolli', [(1, 10)], lolli, act=('막대사탕 진열대', '구경하기'))
    R.obj('plant', [(15, 11)], plant_draw(R, 15, 11, '#4E8A4E', '#FF9ACA'))
    for (x, y) in ((5, 6), (12, 6), (8, 9)): float_candle(R, x, y)
    R.save('candy', '과자 교실', '캔디·쿠키·젤리를 만들어요', [6, 38])
# ================= 공예 교실 =================
def craft_room():
    R = Room(16, 12)
    R.floor(planks(['#B8925E', '#A8824E', '#C49E6A', '#AE8854'], '#7A5A3A'))
    R.walls('#2E4A3A', '#3A5E4A', '#5A3A24')
    def peg(u, v):       # 공구 걸이판
        uu, vv = u - 8, v - 28
        if not (0 <= uu < 44 and 0 <= vv < 28): return None
        if uu < 2 or uu >= 42 or vv < 2 or vv >= 26: return hexc('#5A3A24')
        c = hexc('#C8A878') if (uu % 4 or vv % 4) else hexc('#8A6A48')
        if 6 <= uu < 8 and 6 <= vv < 20: c = hexc('#8A8A92')
        if 14 <= uu < 20 and 14 <= vv < 18: c = hexc('#5A5A62')
        if 26 <= uu < 28 and 4 <= vv < 22: c = hexc('#6A4A2E')
        if (uu - 35) ** 2 + (vv - 12) ** 2 < 12: c = hexc('#E0C070')
        return c
    R.wall_fill('R', peg)
    def masks(u, v):      # 가면 진열
        for k, (u0, col) in enumerate(((64, '#F2EEE4'), (82, '#C84A6A'), (100, '#7A4AA8'))):
            uu, vv = u - u0, v - 34
            if (uu - 6) ** 2 / 36 + (vv - 8) ** 2 / 49 < 1:
                if (uu - 3) ** 2 + (vv - 9) ** 2 < 3 or (uu - 9) ** 2 + (vv - 9) ** 2 < 3: return hexc('#1A1218')
                if vv == 4 and 3 <= uu <= 9 and k == 0: return hexc('#1A1218')
                return hexc(col)
        return None
    R.wall_fill('R', masks); R.window('R', 112)
    def brooms(u, v):
        uu = u - 10
        if not (0 <= uu < 40 and 0 <= v < 56): return None
        if v in (50, 51): return hexc('#5A3A24')
        k = uu // 8
        if uu % 8 == 3 and 14 <= v < 50: return hexc('#8A5A3A')
        if uu % 8 in (1, 2, 3, 4, 5) and 2 <= v < 14 + (uu % 8 == 3) * 2: return hexc('#C8A84A') if (uu + v) % 2 else hexc('#A8883A')
        return None
    R.wall_fill('L', brooms); R.window('L', 58)
    R.sconce('R', 56); R.sconce('L', 50); R.sconce('L', 82)
    def bench(tx, ty, items):
        def f(img, d):
            R.box(img, tx, ty, 2, 1, 11, '#8A6A48', '#5A3A24', '#6A4A2E')
            for k, it in enumerate(items):
                x, y = R.P(tx + .5 + k, ty + .5); y -= 11
                if it == 'pumpkin':
                    for dx, w in ((-3, 3), (3, 3), (0, 4)): d.ellipse([x + dx - w, y - 7, x + dx + w, y], fill=hexc('#E07A1E'))
                    d.polygon([(x - 3, y - 5), (x - 1, y - 6), (x - 1, y - 4)], fill=hexc('#FFE07A')); d.polygon([(x + 3, y - 5), (x + 1, y - 6), (x + 1, y - 4)], fill=hexc('#FFE07A'))
                elif it == 'wax': d.ellipse([x - 4, y - 5, x + 4, y], fill=hexc('#5A5A62')); d.ellipse([x - 3, y - 5, x + 3, y - 2], fill=hexc('#F2E0C0')); d.rectangle([x + 5, y - 6, x + 6, y], fill=hexc('#F2E6C8'))
                elif it == 'paint': [d.rectangle([x - 5 + j * 3, y - 4, x - 3 + j * 3, y], fill=hexc(c)) for j, c in enumerate(['#E05A5A', '#4A8AE0', '#8AE84A', '#E8C84A'])]
                elif it == 'cloth': d.polygon([(x - 6, y - 1), (x, y - 4), (x + 6, y - 1), (x, y + 2)], fill=hexc('#7A4AA8'))
        return f
    for (x, y, it) in ((3, 4, ['pumpkin', 'wax']), (11, 4, ['paint', 'pumpkin']), (3, 8, ['cloth', 'paint']), (11, 8, ['wax', 'pumpkin'])):
        R.obj('bench', [(x, y), (x + 1, y)], bench(x, y, it), act=('공예 작업대', '할로윈 용품 만들기'))
    def mannequin(img, d):
        cx, cy = R.P(14.5, 2.5)
        d.rectangle([cx - 1, cy - 8, cx, cy], fill=hexc('#5A3A24')); d.rectangle([cx - 4, cy - 1, cx + 3, cy], fill=hexc('#5A3A24'))
        d.polygon([(cx - 6, cy - 8), (cx - 4, cy - 24), (cx + 4, cy - 24), (cx + 6, cy - 8)], fill=hexc('#2A1E30')); d.polygon([(cx - 4, cy - 24), (cx, cy - 18), (cx + 4, cy - 24)], fill=hexc('#B02A3A'))
        d.ellipse([cx - 3, cy - 30, cx + 3, cy - 24], fill=hexc('#E8DCC8')); d.polygon([(cx - 6, cy - 29), (cx, cy - 40), (cx + 6, cy - 29)], fill=hexc('#3A2A5E'))
    R.obj('mannequin', [(14, 2)], mannequin, act=('코스튬 마네킹', '옷 입어 보기'))
    def lanterns(img, d):
        for (tx, ty) in ((7.5, 2.5),):
            cx, cy = R.P(tx, ty)
            R.box(img, tx - .6, ty - .6, 1.2, 1.2, 10, '#6A4A2E', '#3E2A1C', '#4E3424')
            for k, dx in enumerate((-5, 0, 5)):
                for ddx, w in ((-2, 2), (2, 2), (0, 3)): d.ellipse([cx + dx + ddx - w, cy - 17 - (k == 1) * 3, cx + dx + ddx + w, cy - 10 - (k == 1) * 3], fill=hexc('#E07A1E'))
                d.point((cx + dx - 1, cy - 14 - (k == 1) * 3), fill=hexc('#FFE07A')); d.point((cx + dx + 1, cy - 14 - (k == 1) * 3), fill=hexc('#FFE07A'))
    R.obj('lanterns', [(7, 2)], lanterns, act=('완성된 잭오랜턴', '구경하기')); R.light(7.5, 2.5, -14, 30, [255, 160, 60], .55)
    R.obj('plant', [(0, 11)], plant_draw(R, 0, 11))
    for (x, y) in ((6, 6), (12, 7), (4, 10)): float_candle(R, x, y)
    R.save('craft', '공예 교실', '잭오랜턴·양초·가면을 만들어요', [29, 38])
# ================= 기숙사 휴게실 =================
DORMS = {
  'witch': dict(name='마녀 기숙사', paper='#3A2A5E', paper2='#4A3A72', wain='#4C2B1C', rug='#5A3A9A', spawn=[5, 49]),
  'vamp':  dict(name='뱀파이어 기숙사', paper='#4A1E2A', paper2='#5E2A38', wain='#2A1E24', rug='#8A1E2E', spawn=[13, 49]),
  'wolf':  dict(name='늑대인간 기숙사', paper='#3A4A2E', paper2='#4A5E3A', wain='#5A3A24', rug='#7A5232', spawn=[21, 49]),
  'ghost': dict(name='유령 기숙사', paper='#5A6A8A', paper2='#6E80A0', wain='#4A5A6A', rug='#8AA0C8', spawn=[29, 49]),
}
def dorm_room(kind):
    D = DORMS[kind]; R = Room(14, 12)
    R.floor(rug(planks(['#6E412B', '#5F3624', '#7A4A31', '#663C28']), 4, 4, 10, 9, D['rug']))
    R.walls(D['paper'], D['paper2'], D['wain'])
    def fireplace(u, v):
        uu = u - 44
        if not (0 <= uu < 24 and 0 <= v < 36): return None
        if v >= 30: return hexc('#6A6470') if v < 34 else hexc('#8A8490')
        if uu < 3 or uu >= 21: return hexc('#5A5460')
        if v < 3: return hexc('#3A3440')
        if v < 18 and 5 <= uu < 19:
            fl = (uu * 7 + v * 3) % 5; fire = {'ghost': ('#6AB8FF', '#C8E8FF'), 'witch': ('#C86AE8', '#F2B8FF')}.get(kind, ('#FF8A3A', '#FFE07A'))
            return hexc(fire[0]) if v < 6 + fl else hexc(fire[1]) if v < 9 + fl // 2 and 8 <= uu < 16 else hexc('#1A1420')
        return hexc('#1A1420')
    R.wall_fill('R', fireplace); x, y = R.wall_px('R', 56, 10); R.lights.append(dict(p=(x, y), dy=0, r=38, c={'ghost': [120, 180, 255], 'witch': [200, 120, 255]}.get(kind, [255, 150, 60]), a=.55, f=1))
    R.window('R', 14, moon=True); R.window('R', 88)
    R.shelf('L', 6, 22, 52, ['#7A2A30', '#2E5A6E', '#7A6A2A', '#4A2E6A', '#2E6A44', '#8A4A2A'])
    if kind == 'wolf': R.window('L', 50, w=26, h=38, glass=('#2A3A5E', '#3A4E78', '#F2E8B0'))
    else: R.window('L', 54)
    R.sconce('R', 40); R.sconce('R', 76); R.sconce('L', 36)
    def bed(tx, ty, sheet):
        def f(img, d):
            R.box(img, tx, ty, 1, 2, 7, sheet, '#4A2A1C', '#5E3826'); R.box(img, tx, ty, 1, .5, 9, '#F2EEE4', '#C8C4BC', '#E0DCD4')
            R.box(img, tx - .05, ty - .05, .15, 2.1, 16, '#5E3826', '#4A2A1C', '#5E3826')
        return f
    for i, (x, y) in enumerate(((12, 1), (12, 4), (12, 7))):
        R.obj('bed', [(x, y), (x, y + 1)], bed(x, y, D['rug']), act=('내 침대', '잠자고 내일로'))
    def sofa(img, d):
        R.box(img, 5, 9.2, 3, .8, 6, D['rug'], shade(hexc(D['rug']), .6), shade(hexc(D['rug']), .8)); R.box(img, 5, 9.75, 3, .25, 13, shade(hexc(D['rug']), 1.1), shade(hexc(D['rug']), .6), shade(hexc(D['rug']), .8))
    R.obj('sofa', [(5, 9), (6, 9), (7, 9)], sofa, act=('푹신한 소파', '앉아서 쉬기'))
    def table(img, d):
        cx, cy = R.P(6.5, 6.5)
        d.rectangle([cx - 1, cy - 8, cx, cy], fill=hexc('#3E2216')); d.ellipse([cx - 8, cy - 12, cx + 8, cy - 6], fill=hexc('#8A5636'))
        d.rectangle([cx - 3, cy - 15, cx + 2, cy - 11], fill=hexc('#E8DCC8')); d.rectangle([cx + 3, cy - 13, cx + 5, cy - 10], fill=hexc('#E07A1E'))
    R.obj('table', [(6, 6)], table, act=('티 테이블', '차 마시기'))
    # 종족별 소품
    if kind == 'witch':
        def ball(img, d):
            cx, cy = R.P(2.5, 2.5); d.rectangle([cx - 4, cy - 4, cx + 4, cy], fill=hexc('#3E2216')); d.ellipse([cx - 5, cy - 14, cx + 5, cy - 4], fill=hexc('#B88AFF')); d.ellipse([cx - 3, cy - 12, cx, cy - 9], fill=hexc('#F2E8FF'))
        R.obj('ball', [(2, 2)], ball, act=('수정구', '미래 엿보기')); R.light(2.5, 2.5, -9, 22, [190, 140, 255], .5)
        def broom(img, d):
            cx, cy = R.P(1.5, 6.5); d.line([(cx - 6, cy - 20), (cx + 2, cy - 2)], fill=hexc('#8A5A3A'), width=2); d.polygon([(cx, cy - 6), (cx + 6, cy + 1), (cx + 1, cy + 2), (cx - 3, cy - 3)], fill=hexc('#C8A84A'))
        R.obj('broom', [(1, 6)], broom, act=('빗자루', '타 보기'))
    elif kind == 'vamp':
        def coffin(img, d):
            R.box(img, 1.2, 2, .9, 2.2, 8, '#3A1E2A', '#2A1218', '#341820')
            cx, cy = R.P(1.65, 3.1); cy -= 8; d.line([(cx, cy - 4), (cx, cy + 3)], fill=hexc('#C49446')); d.line([(cx - 2, cy - 1), (cx + 2, cy - 1)], fill=hexc('#C49446'))
        R.obj('coffin', [(1, 2), (1, 3), (1, 4)], coffin, act=('관 침대', '들어가 보기'))
        def candelabra(img, d):
            cx, cy = R.P(2.5, 7.5); d.rectangle([cx - 1, cy - 18, cx, cy], fill=hexc('#C49446')); d.line([(cx - 5, cy - 18), (cx + 5, cy - 18)], fill=hexc('#C49446'))
            for dx in (-5, 0, 5): d.rectangle([cx + dx - 1, cy - 24, cx + dx, cy - 18], fill=hexc('#F2E6C8')); d.point((cx + dx, cy - 25), fill=hexc('#FFD27A'))
        R.obj('candelabra', [(2, 7)], candelabra, act=('촛대', '불 켜기')); R.light(2.5, 7.5, -24, 26, [255, 180, 100], .55)
    elif kind == 'wolf':
        def bone(img, d):
            cx, cy = R.P(2.5, 3.5); d.ellipse([cx - 8, cy - 5, cx + 8, cy + 3], fill=hexc('#7A5232'))
            d.line([(cx - 4, cy - 2), (cx + 4, cy - 2)], fill=hexc('#F2EEE4'), width=2); [d.ellipse([cx + dx - 2, cy - 4, cx + dx, cy - 1], fill=hexc('#F2EEE4')) for dx in (-5, 5)]
        R.obj('bone', [(2, 3)], bone, act=('늑대 방석과 뼈다귀', '뒹굴기'))
        def logpile(img, d):
            for k in range(3): cx, cy = R.P(1.5, 7.5); d.ellipse([cx - 8 + k * 5, cy - 6 - (k == 1) * 4, cx - 2 + k * 5, cy - (k == 1) * 4], fill=hexc('#7A5232')); d.ellipse([cx - 6 + k * 5, cy - 5 - (k == 1) * 4, cx - 4 + k * 5, cy - 2 - (k == 1) * 4], fill=hexc('#C8A878'))
        R.obj('logs', [(1, 7)], logpile, act=('장작더미', '장작 넣기'))
    else:
        def mirror(img, d):
            cx, cy = R.P(1.5, 3.5); d.rectangle([cx - 6, cy - 26, cx + 6, cy], fill=hexc('#C49446')); d.rectangle([cx - 4, cy - 24, cx + 4, cy - 2], fill=hexc('#A8C8E8')); d.line([(cx - 2, cy - 20), (cx + 2, cy - 16)], fill=hexc('#E8F4FF'))
        R.obj('mirror', [(1, 3)], mirror, act=('거울 (아무도 안 비쳐요)', '들여다보기'))
        def chains(img, d):
            for k, (tx, ty) in enumerate(((4, 3), (9, 3))):
                cx, cy = R.P(tx + .5, ty + .5)
                for j in range(5): d.ellipse([cx - 2 + (j % 2), cy - 50 + j * 4, cx + 1 + (j % 2), cy - 46 + j * 4], outline=hexc('#B8C8E8'))
        R.obj('chains', [(4, 3)], chains, solid=False)
        R.light(6.5, 6.5, -20, 50, [140, 190, 255], .3, 0)
    R.obj('plant', [(0, 11)], plant_draw(R, 0, 11))
    for (x, y) in ((4, 5), (9, 8)): float_candle(R, x, y)
    R.save('dorm_' + kind, D['name'], '종족 휴게실 · 침대에서 자요', D['spawn'])
# ================= 독초 온실 =================
def toxic_room():
    R = Room(16, 12, wall=60)
    def flo(fx, fy):
        if 2 <= fx < 14 and fy >= 3 and (int(fy) % 3 != 2) and not (7 <= fx < 9):
            return hexc('#3E2C20') if (fy * 2) % 1 < .5 else hexc('#4A3426')
        return checker('#6A7470', '#5A6460')(fx, fy)
    R.floor(flo)
    for side, dk in (('L', .86), ('R', 1.0)):
        def g(u, v, dk=dk):
            if v < 10: return shade(hexc('#4A5450'), dk)
            if u % 16 in (0, 1) or v % 16 in (0, 1) or v >= R.WALL - 2: return shade(hexc('#2A2A32'), dk)
            c = hexc('#3A6A5A') if (u + v) % 11 else hexc('#5A9A7A')
            if v < 30 and (u * 3 + v) % 13 < 3: c = hexc('#4A8A4A')
            return shade(c, dk)
        R.wall_fill(side, g)
    def bed_row(y):
        def f(img, d):
            for x in range(2, 14):
                if 7 <= x < 9: continue
                cx, cy = R.P(x + .5, y + .5)
                kind = (x * 7 + y) % 4
                if kind == 0:
                    for dx, dy in ((-3, -6), (0, -9), (3, -6)): d.line([(cx, cy), (cx + dx, cy + dy)], fill=hexc('#5AAE4A'))
                    d.ellipse([cx - 2, cy - 12, cx + 2, cy - 8], fill=hexc('#C86AE8'))
                elif kind == 1:
                    d.ellipse([cx - 3, cy - 5, cx + 3, cy], fill=hexc('#C8A878')); d.point((cx - 1, cy - 3), fill=hexc('#1A1218')); d.point((cx + 1, cy - 3), fill=hexc('#1A1218'))
                    for dx in (-2, 0, 2): d.line([(cx + dx, cy - 5), (cx + dx * 2, cy - 11)], fill=hexc('#4A9A3A'))
                elif kind == 2:
                    for dx, dy, r in ((-2, -4, 2), (2, -5, 2), (0, -7, 2)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc('#8AE8D8'))
                else:
                    d.line([(cx, cy), (cx, cy - 8)], fill=hexc('#4A9A3A')); d.ellipse([cx - 3, cy - 12, cx + 3, cy - 7], fill=hexc('#E8E04A'))
        return f
    for y in (3, 6, 9):
        R.obj('bed', [(x, y) for x in range(2, 14) if not 7 <= x < 9] + [(x, y + 1) for x in range(2, 14) if not 7 <= x < 9], bed_row(y), act=('독초 화단', '독초 돌보기'))
        R.obj('bed2', [(2, y + 1)], bed_row(y + 1), solid=False)
        R.light(4.5, y + 1, -6, 30, [120, 255, 160], .25, 0); R.light(11.5, y + 1, -6, 30, [120, 255, 160], .25, 0)
    def flytrap(img, d):
        cx, cy = R.P(14.5, 1.5)
        d.polygon([(cx - 6, cy - 7), (cx + 6, cy - 7), (cx + 5, cy), (cx - 5, cy)], fill=hexc('#6A5A6A'))
        d.line([(cx, cy - 7), (cx - 2, cy - 22)], fill=hexc('#3E8A3E'), width=2)
        d.pieslice([cx - 12, cy - 34, cx + 6, cy - 16], 180, 360, fill=hexc('#5AAE4A')); d.pieslice([cx - 12, cy - 26, cx + 6, cy - 10], 0, 180, fill=hexc('#4A9A3A'))
        d.chord([cx - 10, cy - 28, cx + 4, cy - 18], 0, 360, fill=hexc('#C83A4A'))
        for k in range(5): d.point((cx - 9 + k * 3, cy - 25), fill=hexc('#F2EEE4'))
    R.obj('flytrap', [(14, 1)], flytrap, act=('식충식물 쩝쩝이', '먹이 주기'))
    def cans(img, d):
        cx, cy = R.P(1.5, 1.5)
        d.rectangle([cx - 5, cy - 8, cx + 1, cy], fill=hexc('#5A8AB0')); d.line([(cx + 1, cy - 6), (cx + 6, cy - 9)], fill=hexc('#5A8AB0'), width=2); d.rectangle([cx - 4, cy - 10, cx, cy - 8], fill=hexc('#4A7AA0'))
    R.obj('cans', [(1, 1)], cans, act=('물뿌리개', '물 주기'))
    R.save('toxic', '독초 온실', '빛나는 독초를 길러요', [22, 64])
candy_room(); craft_room()
for k in DORMS: dorm_room(k)
toxic_room()
