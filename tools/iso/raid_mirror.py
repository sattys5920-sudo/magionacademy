# 레이드 시안: 한밤 도서관 안쪽 벽의 「이상한 거울」 + 거울 너머 구역 (얼어붙은 탑 · 모이는 곳 두 군데)
#   python3 raid_mirror.py → out/library_m_bg.png (거울이 꺼진 도서관) · out/library_mg_bg.png (빛나는 거울) · out/mirrorland_* · out/raid_prev_*.png (미리 보기)
#   시안이라 world.js에는 아직 안 넣어요
import os, sys, math, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True)
from PIL import Image, ImageDraw, ImageFilter
import interiors
from interiors import Room, hexc, shade, up

# ---------------- 이상한 거울 (벽 그림) ----------------
MU, MW, MV, MH = 124, 26, 6, 72          # 오른쪽 벽 u 124~150 (창문 자리) · 바닥에서 6 위로 · 높이 72
CRACK = [(5, 58), (9, 50), (8, 44), (13, 36), (12, 28), (17, 20)]
def crack_d(x, y):
    best = 9
    for (a, b), (c, d) in zip(CRACK, CRACK[1:]):
        dx, dy = c - a, d - b; t = max(0, min(1, ((x - a) * dx + (y - b) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(x - a - t * dx, y - b - t * dy))
    return best
def mirror_fn(glow):
    fr1, fr2, fr3 = hexc('#E4EEF8'), hexc('#9AAAC4'), hexc('#5A6684')
    def f(u, v):
        uu, vv = u - MU, v - MV
        if not (-3 <= uu < MW + 3 and -3 <= vv < MH + 9): return None
        cx = MW / 2; top = MH - cx
        # 위 장식 (작은 왕관 · 가운데 보석)
        if vv >= MH - 1:
            k = vv - (MH - 1)
            if abs(uu + .5 - cx) < 5 - k * .5 and k < 8:
                if abs(uu + .5 - cx) < 1.5 and 2 <= k <= 4: return hexc('#7FE6FF') if glow else hexc('#6A7AA8')
                return fr1 if k % 3 else fr2
            if k < 3 and abs(uu + .5 - cx) < 8: return fr2
        # 받침
        if -3 <= vv < 0: return (fr3 if vv == -3 else fr2) if -2 <= uu < MW + 2 else None
        if uu < -1 or uu >= MW + 1: return None
        r = math.hypot(uu + .5 - cx, vv - top) if vv > top else abs(uu + .5 - cx)
        if r > cx + 1: return None
        if r > cx - 1.5 or vv < 1.5:                  # 바깥 테두리 (은빛)
            return fr1 if (uu + vv) % 5 else fr2
        if r > cx - 3 or vv < 3: return fr3 if (vv // 3) % 2 else fr2
        # 유리
        gx, gy = uu - 3, vv - 3
        if glow:
            d = math.hypot(uu + .5 - cx, vv - MH * .45)
            ring = (d * 1.1 - math.atan2(vv - MH * .45, uu + .5 - cx) * 2.2) % 6
            c = hexc('#BFF4FF') if ring < 1.2 else hexc('#6FD8FF') if ring < 3 else hexc('#3AA8E8')
            if d < 4: c = hexc('#F4FFFF')
        else:
            k = vv / MH; c = (int(26 + 18 * k), int(34 + 22 * k), int(58 + 30 * k), 255)
            if 0 <= (gx * .8 - gy * .5 + 30) % 22 < 2.2: c = shade(c, 1.45)      # 비친 빛 줄
        cd = crack_d(uu, vv)
        if cd < .7: return hexc('#EAF4FF') if not glow else hexc('#FFFFFF')
        if cd < 1.4 and not glow: return shade(c, .7)
        return c
    return f

def library_variant(glow, key):
    orig_win, orig_save = Room.window, Room.save
    def win(self, side, u0, *a, **k):
        if side == 'R' and u0 == 128: return            # 이 창문 자리에 거울을 걸어요
        return orig_win(self, side, u0, *a, **k)
    def save(self, k_, title, sub, back):
        self.wall_fill('R', mirror_fn(glow))
        x, y = self.wall_px('R', MU + MW / 2, MV + MH / 2)
        if glow:
            self.lights.append(dict(p=(x, y), dy=0, r=70, c=[110, 220, 255], a=.7, f=1))
            self.lights.append(dict(p=self.P(17, 1.5), dy=0, r=46, c=[110, 220, 255], a=.45, f=1))
            # 바닥에 번지는 빛
            for yy in range(self.H):
                for xx in range(self.W):
                    fx, fy = self.inv(xx, yy)
                    if 0 <= fx < self.NX and 0 <= fy < self.NY:
                        d = math.hypot((fx - 17.2) / 2.6, (fy - .4) / 1.6)
                        if d < 1:
                            c = self.px[xx, yy]; k = (1 - d) * .55
                            self.px[xx, yy] = (int(c[0] + (150 - c[0]) * k), int(c[1] + (235 - c[1]) * k), int(c[2] + (255 - c[2]) * k), 255)
        self.doors.append(dict(tile=[17, 0], to='mirrorland', label='이상한 거울', spawn=[12, 17], lock='raid', back=[17, 1]))
        return orig_save(self, key, title, sub, back)
    Room.window, Room.save = win, save
    import library; library.library_room()
    Room.window, Room.save = orig_win, orig_save

# ---------------- 거울 너머 (얼음 섬 · 얼어붙은 탑) ----------------
random.seed(7)
NX, NY = 22, 22
def mirrorland():
    R = Room(NX, NY, wall=250); R.exit_to, R.exit_label = 'library', '한밤 도서관'
    px = R.px
    # 하늘: 밤 · 오로라 · 별 · 먼 얼음 산
    for y in range(R.H):
        k = y / R.H; base = (int(14 + 20 * k), int(18 + 30 * k), int(44 + 50 * k), 255)
        for x in range(R.W): px[x, y] = base
    for x in range(R.W):
        for band, col, amp in ((70, (90, 255, 200), 18), (96, (140, 160, 255), 14)):
            cy = band + math.sin(x / 37) * amp + math.sin(x / 13) * 4
            for y in range(int(cy) - 14, int(cy) + 14):
                if 0 <= y < R.H:
                    a = max(0, 1 - abs(y - cy) / 14) ** 2 * .32 * (.6 + .4 * math.sin(x / 9))
                    c = px[x, y]; px[x, y] = (int(c[0] + (col[0] - c[0]) * a), int(c[1] + (col[1] - c[1]) * a), int(c[2] + (col[2] - c[2]) * a), 255)
    for _ in range(260):
        x, y = random.randrange(R.W), random.randrange(int(R.H * .7)); px[x, y] = hexc('#FFFFFF') if random.random() < .3 else hexc('#9AB4E8')
    d = ImageDraw.Draw(R.bg)
    for layer, col, base, amp in ((0, '#2A3E6E', 168, 46), (1, '#3A5488', 196, 30)):
        pts = [(0, R.H)]
        for x in range(0, R.W + 12, 12):
            h = amp * (.5 + .5 * math.sin(x / (40 + layer * 17) + layer * 2)) + (x * 37 % 23 if (x // 12) % 2 else 0)
            pts.append((x, base - h))
        pts.append((R.W, R.H)); d.polygon(pts, fill=hexc(col))
        for x in range(0, R.W, 12):   # 산꼭대기 눈
            pass
    # 바닥 (얼음 · 눈 · 거울 길)
    def flo(fx, fy):
        n = math.sin(fx * 1.3 + fy * .7) + math.sin(fx * .4 - fy * 1.1) * 1.2 + math.sin(fx * 2.3 + fy * 1.9) * .4
        c = hexc('#E6F2FC') if n > .9 else hexc('#A8CCEA') if n > -.6 else hexc('#8CB6DE')
        if abs(fx - fy) < 2.2 and fx + fy > 12:                               # 탑으로 가는 거울 길 (화면 가운데로 곧게)
            c = hexc('#C4E4FA') if (int(fx * 2) + int(fy * 2)) % 2 else hexc('#94C4EC')
            if abs(abs(fx - fy) - 2.1) < .14: c = hexc('#F4FAFF')
        for (cx, cy, col) in ((9, 16.5, '#5FD0FF'), (16.5, 9, '#C08AFF')):    # 모이는 곳: 왼쪽(파랑) · 오른쪽(보라)
            r = math.hypot(fx - cx, fy - cy)
            if r < 2.6:
                ang = math.atan2(fy - cy, fx - cx)
                if 2.25 < r < 2.55 or 1.55 < r < 1.7: c = hexc(col)
                elif r < 1.55 and abs(math.sin(ang * 3)) * r > 1.25: c = shade(hexc(col), .8)
                elif r < .35: c = hexc('#FFFFFF')
                else: c = (int(c[0] * .8 + int(col[1:3], 16) * .2), int(c[1] * .8 + int(col[3:5], 16) * .2), int(c[2] * .8 + int(col[5:7], 16) * .2), 255)
                for k in range(6):                                            # 여섯 자리
                    a = k * math.pi / 3 + .5; sx, sy = cx + math.cos(a) * 1.95, cy + math.sin(a) * 1.95
                    if math.hypot(fx - sx, fy - sy) < .22: c = hexc('#FFFFFF')
        if fx < .35 or fy < .35: c = shade(c, 1.08)
        return c
    R.floor(flo)
    # 얼음 섬 낭떠러지 (앞 두 면)
    A, B, C = R.P(NX, 0), R.P(NX, NY), R.P(0, NY)
    for (p, q, col) in ((A, B, '#5A86B8'), (B, C, '#7AA6D4')):
        for t in range(0, 101):
            x = p[0] + (q[0] - p[0]) * t / 100; y = p[1] + (q[1] - p[1]) * t / 100
            depth = 22 + 8 * math.sin(t / 6) + (t * 7 % 5)
            for k in range(int(depth)):
                c = shade(hexc(col), 1 - k / depth * .45)
                if k > depth - 6 and (int(x) + k) % 3 == 0: continue
                R.put(x, y + k, c); R.put(x + .5, y + k, c)
    # 고드름 끝
    # ---- 물건 ----
    def tower(img, d):
        cx, by = R.P(5, 5); by += 2; rx, ry, Ht = 40, 18, 176
        top_y = by - Ht
        for yy in range(int(top_y), int(by) + 1):
            t = (by - yy) / Ht; w = rx * (1 - .18 * t)
            if yy > by - ry * .0: pass
            for xx in range(int(cx - w), int(cx + w) + 1):
                s = max(-1, min(1, (xx - cx) / w))
                base = (1 - s) / 2
                c = (int(110 + 110 * (1 - base) ** 1.4), int(150 + 90 * (1 - base) ** 1.4), int(200 + 50 * (1 - base)), 255)
                row = int((by - yy) // 12); bx = ((xx - cx) / w * 6 + (row % 2) * .5) % 1
                ell = math.sqrt(max(0, 1 - s * s)) * ry * .5
                if ((by - yy) - ell) % 12 < 1.2 or bx < .06: c = shade(c, .78)
                d.point((xx, yy + ell), fill=c); d.point((xx, yy + ell + 1), fill=c)
        # 꼭대기 (톱니 · 뾰족 지붕 · 떠 있는 수정)
        tw = rx * .82
        for k in range(-4, 5):
            x0 = cx + k * tw / 4.5
            d.rectangle([x0 - 4, top_y - 10 + abs(k) * .8, x0 + 3, top_y + 4], fill=hexc('#D8EEFA') if k < 0 else hexc('#9CC0E4'))
        d.polygon([(cx - tw * .7, top_y - 4), (cx, top_y - 70), (cx + tw * .7, top_y - 4)], fill=hexc('#7FB0E0'))
        d.polygon([(cx - tw * .7, top_y - 4), (cx, top_y - 70), (cx - 2, top_y - 4)], fill=hexc('#B8DCF6'))
        for yy in range(int(top_y - 66), int(top_y - 4), 8): d.line([(cx - (top_y - 4 - yy) * .0 - (yy - (top_y - 70)) * tw * .7 / 66, yy), (cx + (yy - (top_y - 70)) * tw * .7 / 66, yy)], fill=hexc('#6A9ACC'))
        gy = top_y - 92
        d.polygon([(cx, gy - 14), (cx + 8, gy), (cx, gy + 14), (cx - 8, gy)], fill=hexc('#7FE6FF')); d.polygon([(cx, gy - 14), (cx - 8, gy), (cx, gy + 14)], fill=hexc('#C8F6FF')); d.line([(cx, gy - 10), (cx, gy + 10)], fill=hexc('#FFFFFF'))
        # 창문: 게임 건물 창문과 같은 모양 (둥근 윗부분 · 테두리 · 가운데 창살) · 얼음빛
        TRIM = hexc('#5A7AA8')
        for (dx, h) in ((-20, 64), (14, 64), (-4, 104), (16, 132), (-18, 140)):
            wx, wy, ww, wh = int(cx + dx - 3), int(by - h - 12), 7, 12
            for vv in range(wh):
                for uu in range(ww):
                    top = ww / 2
                    if vv < top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2) ** 2: continue
                    edge = uu == 0 or uu == ww - 1 or vv == wh - 1 or (vv < top and (uu + .5 - ww / 2) ** 2 + (vv - top) ** 2 > (ww / 2 - 1.2) ** 2)
                    c = shade(TRIM, .6) if edge or uu == ww // 2 else (hexc('#BFEFFF') if (uu + vv) % 7 else hexc('#F0FCFF'))
                    d.point((wx + uu, wy + vv), fill=c)
        # 문: 게임 건물 문과 같은 모양 (둥근 아치 나무 문 · 테두리 · 가운데 줄 · 금빛 손잡이) · 길 한가운데에 맞춰요
        dw, dh = 22, 30; gx0, gy0 = int(cx - dw // 2), int(by + 9 - dh)
        for vv in range(dh):
            for uu in range(dw):
                top = dw / 2
                if vv < top and (uu + .5 - dw / 2) ** 2 + (vv - top) ** 2 > (dw / 2) ** 2: continue
                inner = 1 < uu < dw - 2 and vv > 1 and not (vv < top and (uu + .5 - dw / 2) ** 2 + (vv - top) ** 2 > (dw / 2 - 2) ** 2)
                c = hexc('#5A3420') if inner else shade(TRIM, .55)
                if inner and uu % 4 == 1: c = hexc('#4A2A18')           # 나무 판자 줄
                if inner and uu in (dw // 2 - 1, dw // 2): c = hexc('#3E2216')   # 가운데 (두 짝 문)
                if vv == dh - 13 and uu in (dw // 2 - 3, dw // 2 + 2): c = hexc('#E0C070')   # 손잡이
                d.point((gx0 + uu, gy0 + vv), fill=c)
        for k in range(-2, 3): d.point((cx + k * 5, gy0 - 2 + abs(k)), fill=hexc('#E8F6FF'))   # 문 위 얼음 장식
        # 고드름 (꼭대기 아래)
        for k in range(-9, 10):
            x0 = cx + k * 3.6; L = 4 + (k * 7 % 6)
            d.polygon([(x0 - 1.5, top_y + 4), (x0 + 1.5, top_y + 4), (x0, top_y + 4 + L)], fill=hexc('#E8F6FF'))
    R.obj('tower', [(x, y) for x in range(3, 8) for y in range(3, 8)], tower, act=('거울 탑', '올라가기'))
    R.light(5, 5, -110, 60, [110, 220, 255], .4, 1); R.light(7.5, 7.5, -10, 40, [110, 220, 255], .55, 1)
    def crystal(tx, ty, s):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            for (dx, h, w) in ((-5 * s, 14 * s, 3 * s), (0, 22 * s, 4 * s), (5 * s, 12 * s, 3 * s), (2 * s, 8 * s, 2 * s)):
                d.polygon([(cx + dx - w, cy), (cx + dx - w, cy - h + w), (cx + dx, cy - h - w), (cx + dx + w, cy - h + w), (cx + dx + w, cy)], fill=hexc('#7FC8F4'))
                d.polygon([(cx + dx - w, cy), (cx + dx - w, cy - h + w), (cx + dx, cy - h - w), (cx + dx, cy)], fill=hexc('#C8EEFF'))
        return f
    def tree(tx, ty):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.rectangle([cx - 2, cy - 8, cx + 1, cy], fill=hexc('#6A7A9A'))
            for k, (w, y0) in enumerate(((13, 8), (10, 18), (7, 27))):
                d.polygon([(cx - w, cy - y0), (cx, cy - y0 - 16), (cx + w, cy - y0)], fill=hexc('#9ACCEA'))
                d.polygon([(cx - w, cy - y0), (cx, cy - y0 - 16), (cx, cy - y0)], fill=hexc('#E4F4FF'))
        return f
    def lantern(tx, ty):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.rectangle([cx - 1, cy - 26, cx, cy], fill=hexc('#C8D8EC')); d.rectangle([cx - 4, cy - 34, cx + 3, cy - 26], fill=hexc('#E4EEF8')); d.rectangle([cx - 3, cy - 33, cx + 2, cy - 27], fill=hexc('#7FE6FF'))
            d.polygon([(cx - 5, cy - 34), (cx, cy - 39), (cx + 4, cy - 34)], fill=hexc('#9AAAC4'))
        return f
    def back_mirror(img, d):   # 돌아가는 거울 (서 있는 틀)
        cx, cy = R.P(19.5, 19.5)
        d.rectangle([cx - 10, cy - 4, cx + 9, cy], fill=hexc('#5A6684'))
        d.rectangle([cx - 9, cy - 44, cx + 8, cy - 4], fill=hexc('#E4EEF8')); d.ellipse([cx - 9, cy - 54, cx + 8, cy - 36], fill=hexc('#E4EEF8'))
        d.rectangle([cx - 7, cy - 44, cx + 6, cy - 6], fill=hexc('#3A2A20')); d.ellipse([cx - 7, cy - 52, cx + 6, cy - 38], fill=hexc('#3A2A20'))
        for k in range(5): d.rectangle([cx - 6, cy - 44 + k * 8, cx + 5, cy - 41 + k * 8], fill=hexc('#7A4A2A' if k % 2 else '#5A3420'))   # 비친 도서관 서가
        d.line([(cx - 4, cy - 46), (cx + 3, cy - 30)], fill=hexc('#FFFFFF'))
    R.obj('mirror_back', [(19, 19)], back_mirror, act=('돌아가는 거울', '도서관으로 돌아가기'))
    R.light(19.5, 19.5, -28, 26, [255, 210, 150], .5, 1)
    for (x, y, s) in ((1, 10, 1.2), (10, 1, 1.4), (2, 19, 1), (19, 2, 1.1), (12, 4, .8), (4, 12, .8), (15, 20, .9), (20, 15, 1)): R.obj('crystal', [(x, y)], crystal(x, y, s))
    for (x, y) in ((1, 4), (4, 1), (1, 14), (14, 1), (3, 17), (17, 3), (6, 20), (20, 6), (12, 1), (1, 12)): R.obj('tree', [(x, y)], tree(x, y))
    for (x, y) in ((11, 14), (14, 11), (15, 18), (18, 15)): R.obj('lantern', [(x, y)], lantern(x, y)); R.light(x + .5, y + .5, -30, 22, [127, 230, 255], .6, 1)
    R.extra = dict(night=True, indoor=False, fill='#0E1430', spawnIn=[18, 18])
    R.save('mirrorland', '거울 너머', '거울 탑 1 ~ 4 층 · 친구들과 같이 올라가요', [17, 1])
    m = json.load(open('out/mirrorland.json')); ex = [o for o in m['objs'] if o['name'] == 'exit'][0]; ex['box'] = [20, 21, 21, 22]; ex['door']['tile'] = [20, 21]; ex['door']['lock'] = 'raidback'; ex['door']['label'] = '돌아가는 거울'; json.dump(m, open('out/mirrorland.json', 'w'), ensure_ascii=False)   # 나가는 곳: 앞 모서리 (돌아가는 거울 옆)
    return R

def preview(key, out, scale=2, dark=.62):
    m = json.load(open(f'out/{key}.json')); bg = Image.open(f'out/{key}_bg.png').convert('RGBA'); sh = Image.open(f'out/{key}_obj.png').convert('RGBA')
    im = bg.copy()
    for o in sorted([o for o in m['objs'] if o['sw']], key=lambda o: o['y'] + o['sh']):
        im.alpha_composite(sh.crop((o['sx'], o['sy'], o['sx'] + o['sw'], o['sy'] + o['sh'])), (o['x'], o['y']))
    im = Image.eval(im.convert('RGB'), lambda v: int(v * dark)).convert('RGBA')        # 밤
    glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for L in m['lights']:
        x, y = L['p'][0], L['p'][1] + L.get('dy', 0); r = L['r']
        for k in range(r, 0, -2): gd.ellipse([x - k, y - k * .7, x + k, y + k * .7], fill=tuple(L['c']) + (int(255 * L['a'] * .16 * (1 - k / r)),))
    glow = glow.filter(ImageFilter.GaussianBlur(3))
    base = im.load(); g = glow.load()
    for y in range(im.height):
        for x in range(im.width):
            a = g[x, y]
            if a[3]: c = base[x, y]; k = a[3] / 255 * 2.2; base[x, y] = (min(255, int(c[0] + a[0] * k)), min(255, int(c[1] + a[1] * k)), min(255, int(c[2] + a[2] * k)), 255)
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(out)

if __name__ == '__main__':
    library_variant(False, 'library_m'); library_variant(True, 'library_mg'); mirrorland()
    preview('library_m', 'out/raid_prev_lib_off.png'); preview('library_mg', 'out/raid_prev_lib_on.png'); preview('mirrorland', 'out/raid_prev_land.png', dark=.8)
    print('ok')
