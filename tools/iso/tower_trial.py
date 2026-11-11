# 시련의 탑: 학교 북쪽 강가의 「시련의 문」 + 문 너머 「시련의 언덕」 (해 질 녘 하늘 · 떠 있는 바위섬 · 검은 돌탑 · 부류 석상 여덟 · 화로)
#   python3 tower_trial.py → out/trialland_bg.png · out/trialland_obj.png · out/trialland.json · out/trial_gate.png (학교에 세우는 문 소품) · out/trial_prev.png (미리 보기)
#   게임에 넣기: python3 add_trial_map.py
import os, sys, math, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True)
from PIL import Image, ImageDraw, ImageFilter
from interiors import Room, hexc, shade, OUTL

random.seed(11)
NX, NY = 22, 22
TRAIT = ['#9AA8BC', '#5E9A4A', '#8A7AC0', '#5AB8F0', '#5ADA6A', '#7A4AD0', '#7AC8E8', '#FF5A2A']   # 철갑 · 거대 · 날쌘 · 무리 · 재생 · 마나 먹기 · 반사 · 광폭

def outline_img(im):
    a = im.load(); w, h = im.size; add = []
    for y in range(h):
        for x in range(w):
            if a[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and a[x + dx, y + dy][3] > 200 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for x, y in add: a[x, y] = OUTL
    return im

def trialland():
    R = Room(NX, NY, wall=330); R.exit_to, R.exit_label = 'campus', '호박달 마녀학교'
    px = R.px
    # ---- 하늘: 해 질 녘 (위 남보라 → 아래 주황) · 구름 띠 · 별 몇 개 ----
    for y in range(R.H):
        k = min(1, y / (R.H * .62))
        top, mid, bot = (22, 14, 48), (92, 38, 96), (236, 120, 70)
        c = tuple(int(top[i] + (mid[i] - top[i]) * k * 1.6) if k < .62 else int(mid[i] + (bot[i] - mid[i]) * (k - .62) / .38) for i in range(3))
        for x in range(R.W): px[x, y] = c + (255,)
    for _ in range(140):
        x, y = random.randrange(R.W), random.randrange(int(R.H * .28)); px[x, y] = hexc('#FFE8C8') if random.random() < .4 else hexc('#C8A8E8')
    for band, col, amp, th in ((150, (255, 170, 120), 10, 7), (190, (200, 110, 150), 14, 9), (232, (255, 200, 140), 8, 5)):
        for x in range(R.W):
            cy = band + math.sin(x / 41) * amp + math.sin(x / 11 + band) * 3
            for y in range(int(cy) - th, int(cy) + th):
                if 0 <= y < R.H:
                    a = max(0, 1 - abs(y - cy) / th) ** 1.5 * .45
                    c = px[x, y]; px[x, y] = (int(c[0] + (col[0] - c[0]) * a), int(c[1] + (col[1] - c[1]) * a), int(c[2] + (col[2] - c[2]) * a), 255)
    d = ImageDraw.Draw(R.bg)
    sx, sy = int(R.W * .78), int(R.H * .5); d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=hexc('#FFB070')); d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=hexc('#FFD49A'))   # 지는 해
    # 멀리 떠 있는 바위섬 (실루엣)
    for (cx, cy, w) in ((40, 250, 30), (R.W - 50, 200, 22), (90, 175, 14), (R.W - 120, 270, 34), (R.W // 2 - 140, 300, 18)):
        d.polygon([(cx - w, cy), (cx + w, cy), (cx + w * .6, cy + w * .5), (cx + w * .1, cy + w * 1.1), (cx - w * .5, cy + w * .6)], fill=hexc('#3A1E46'))
        d.rectangle([cx - w, cy - 3, cx + w, cy], fill=hexc('#5A3A5E'))
    # ---- 바닥: 검은 판석 · 틈에서 새는 금빛 · 탑으로 가는 계단 길 · 석상 둘레 원 ----
    def flo(fx, fy):
        tx, ty = int(fx * 1.5), int(fy * 1.5); n = (tx * 7 + ty * 13) % 5
        c = [hexc('#4A4258'), hexc('#544A64'), hexc('#3E3850'), hexc('#4E4660'), hexc('#463E58')][n]
        if (fx * 1.5) % 1 < .08 or (fy * 1.5) % 1 < .08: c = hexc('#2A2436')
        cr = math.sin(fx * 2.1 + fy * .7) + math.sin(fx * .6 - fy * 1.7) * 1.1
        if abs(cr) < .045: c = hexc('#FFB04A')                                     # 금빛 틈
        elif abs(cr) < .1: c = shade(c, 1.25)
        if abs(fx - fy) < 2 and fx + fy > 14:                                      # 탑으로 가는 길 (붉은 돌)
            c = hexc('#7A4A4A') if (int(fx * 2) + int(fy * 2)) % 2 else hexc('#6A3E44')
            if abs(abs(fx - fy) - 1.95) < .12: c = hexc('#E8B060')
        if fx < .35 or fy < .35: c = shade(c, 1.1)
        return c
    R.floor(flo)
    # 섬 낭떠러지 (앞 두 면)
    A, B, C = R.P(NX, 0), R.P(NX, NY), R.P(0, NY)
    for (p, q, col) in ((A, B, '#5A3A4E'), (B, C, '#7A4A56')):
        for t in range(0, 101):
            x = p[0] + (q[0] - p[0]) * t / 100; y = p[1] + (q[1] - p[1]) * t / 100
            depth = 26 + 10 * math.sin(t / 5) + (t * 7 % 6)
            for k in range(int(depth)):
                c = shade(hexc(col), 1 - k / depth * .5)
                if (int(x) * 3 + k) % 9 == 0: c = shade(c, .8)
                if k > depth - 7 and (int(x) + k) % 3 == 0: continue
                R.put(x, y + k, c); R.put(x + .5, y + k, c)
    # ---- 탑: 검은 돌 · 층마다 금띠 · 빛나는 창 · 꼭대기 왕관과 떠 있는 불꽃 ----
    def tower(img, d):
        cx, by = R.P(5, 5); by += 2; rx, ry, Ht = 42, 18, 214
        top_y = by - Ht
        for yy in range(int(top_y), int(by) + 1):
            t = (by - yy) / Ht; w = rx * (1 - .16 * t) + (3 if (by - yy) < 14 else 0)
            for xx in range(int(cx - w), int(cx + w) + 1):
                s = max(-1, min(1, (xx - cx) / w)); lit = (1 - s) / 2
                c = (int(58 + 70 * lit ** 1.3), int(50 + 52 * lit ** 1.3), int(74 + 64 * lit ** 1.2), 255)
                row = int((by - yy) // 10); bx = ((xx - cx) / w * 7 + (row % 2) * .5) % 1
                ell = math.sqrt(max(0, 1 - s * s)) * ry * .5
                hh = (by - yy) - ell
                if hh % 10 < 1.1 or bx < .05: c = shade(c, .72)                     # 돌 줄눈
                if hh % 42 < 3.2 and hh > 6: c = (int(200 + 50 * lit), int(150 + 40 * lit), int(60 + 20 * lit), 255)   # 층마다 금띠
                d.point((xx, yy + ell), fill=c); d.point((xx, yy + ell + 1), fill=c)
        # 창: 층마다 엇갈려 (금빛 불 · 위로 갈수록 붉게)
        for k, (dx, h) in enumerate(((-18, 30), (16, 56), (-6, 76), (20, 100), (-20, 118), (4, 142), (-14, 160), (14, 184))):
            wx, wy = int(cx + dx - 3), int(by - h - 10); col = hexc('#FFD878') if k < 4 else hexc('#FF9A5A') if k < 7 else hexc('#FF6A4A')
            for vv in range(11):
                for uu in range(7):
                    if vv < 3.5 and (uu + .5 - 3.5) ** 2 + (vv - 3.5) ** 2 > 12.25: continue
                    edge = uu in (0, 6) or vv == 10 or (vv < 3.5 and (uu + .5 - 3.5) ** 2 + (vv - 3.5) ** 2 > 6.5)
                    d.point((wx + uu, wy + vv), fill=hexc('#2A2030') if edge or uu == 3 else col)
        # 꼭대기: 톱니 왕관 · 뾰족 끝 · 떠 있는 불꽃
        tw = rx * .86
        for k in range(-5, 6):
            x0 = cx + k * tw / 5.4; hgt = 14 + (4 if k % 2 == 0 else 0)
            d.polygon([(x0 - 4, top_y + 4), (x0 - 4, top_y - hgt + 6), (x0, top_y - hgt), (x0 + 4, top_y - hgt + 6), (x0 + 4, top_y + 4)], fill=hexc('#6A5A80') if k < 0 else hexc('#4A3E5E'))
        d.rectangle([cx - tw, top_y - 2, cx + tw, top_y + 5], fill=hexc('#C8963A')); d.line([(cx - tw, top_y + 1), (cx + tw, top_y + 1)], fill=hexc('#FFD878'))
        d.polygon([(cx - 10, top_y - 6), (cx, top_y - 46), (cx + 10, top_y - 6)], fill=hexc('#4A3E5E')); d.polygon([(cx - 10, top_y - 6), (cx, top_y - 46), (cx - 1, top_y - 6)], fill=hexc('#7A6A90'))
        fy0 = top_y - 70
        for r, col in ((15, '#FF5A2A'), (11, '#FF8A3A'), (7, '#FFC85A'), (3, '#FFF4C8')): d.ellipse([cx - r, fy0 - r * 1.2, cx + r, fy0 + r], fill=hexc(col))
        for k in range(5): a = k * 1.25; d.polygon([(cx + math.cos(a) * 9, fy0 - 4 + math.sin(a) * 4), (cx + math.cos(a) * 3, fy0 - 26 - k % 2 * 6), (cx + math.cos(a + .5) * 9, fy0 - 2)], fill=hexc('#FF8A3A'))
        # 문: 큰 쇠 장식 돌문 (두 짝 · 금빛 문장)
        dw, dh = 26, 36; gx0, gy0 = int(cx - dw // 2), int(by + 9 - dh)
        for vv in range(dh):
            for uu in range(dw):
                top = dw / 2
                if vv < top and (uu + .5 - dw / 2) ** 2 + (vv - top) ** 2 > (dw / 2) ** 2: continue
                inner = 1 < uu < dw - 2 and vv > 1 and not (vv < top and (uu + .5 - dw / 2) ** 2 + (vv - top) ** 2 > (dw / 2 - 2) ** 2)
                c = hexc('#3A2A3A') if inner else hexc('#C8963A')
                if inner and vv % 8 == 5: c = hexc('#6A6070')                     # 쇠띠
                if inner and uu in (dw // 2 - 1, dw // 2): c = hexc('#1E1622')
                d.point((gx0 + uu, gy0 + vv), fill=c)
        d.ellipse([cx - 4, gy0 + 12, cx + 4, gy0 + 20], fill=hexc('#FFD878')); d.ellipse([cx - 2, gy0 + 14, cx + 2, gy0 + 18], fill=hexc('#FF6A3A'))   # 문장
        for side in (-1, 1):   # 문 옆 깃발
            fx0 = cx + side * 28
            d.rectangle([fx0 - 1, by - 70, fx0, by - 20], fill=hexc('#C8963A'))
            d.polygon([(fx0 - 7, by - 68), (fx0 + 6, by - 68), (fx0 + 6, by - 38), (fx0, by - 44), (fx0 - 7, by - 38)], fill=hexc('#8A2A3A')); d.polygon([(fx0 - 3, by - 60), (fx0 + 2, by - 60), (fx0, by - 54)], fill=hexc('#FFD878'))
    R.obj('tower', [(x, y) for x in range(3, 8) for y in range(3, 8)], tower, act=('시련의 탑', '오르기'))
    R.light(5, 5, -130, 70, [255, 150, 80], .35, 1); R.light(5, 5, -290, 40, [255, 120, 60], .7, 1); R.light(7.5, 7.5, -16, 40, [255, 200, 120], .55, 1)
    # ---- 부류 석상 여덟 (석상 둘레 원 위 · 받침 위에 부류 색 보석) ----
    def statue(tx, ty, col):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.polygon([(cx - 8, cy - 2), (cx, cy - 6), (cx + 8, cy - 2), (cx, cy + 2)], fill=hexc('#2E2838'))
            d.rectangle([cx - 6, cy - 22, cx + 5, cy - 2], fill=hexc('#6A6078')); d.rectangle([cx - 6, cy - 22, cx - 1, cy - 2], fill=hexc('#8A8098'))
            d.rectangle([cx - 8, cy - 25, cx + 7, cy - 22], fill=hexc('#9A90A8'))
            g = hexc(col); d.polygon([(cx, cy - 40), (cx + 6, cy - 31), (cx, cy - 25), (cx - 6, cy - 31)], fill=g); d.polygon([(cx, cy - 40), (cx - 6, cy - 31), (cx, cy - 29)], fill=shade(g, 1.35)); d.point((cx - 2, cy - 34), fill=hexc('#FFFFFF'))
        return f
    for k, (tx, ty) in enumerate(((7, 12), (9, 16), (5, 16), (12, 19), (12, 7), (16, 9), (16, 5), (19, 12))):   # 길 왼쪽 넷 · 오른쪽 넷
        R.obj('statue', [(tx, ty)], statue(tx, ty, TRAIT[k])); R.light(tx + .5, ty + .5, -32, 16, list(hexc(TRAIT[k])[:3]), .55, 1)
    # ---- 화로 (길 양옆) ----
    def brazier(tx, ty):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.rectangle([cx - 1, cy - 18, cx, cy], fill=hexc('#3A3040')); d.polygon([(cx - 7, cy - 22), (cx + 6, cy - 22), (cx + 3, cy - 16), (cx - 4, cy - 16)], fill=hexc('#5A4A50'))
            for r, col in ((6, '#FF5A2A'), (4, '#FF9A3A'), (2, '#FFE07A')): d.polygon([(cx - r, cy - 22), (cx, cy - 22 - r * 2.4), (cx + r, cy - 22)], fill=hexc(col))
        return f
    for (x, y) in ((11, 14), (14, 11), (15, 18), (18, 15), (19, 21), (21, 19)): R.obj('brazier', [(x, y)], brazier(x, y)); R.light(x + .5, y + .5, -30, 24, [255, 150, 70], .65, 1)
    # ---- 부서진 기둥 · 바위 ----
    def pillar(tx, ty, h):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.polygon([(cx - 8, cy - 1), (cx, cy - 5), (cx + 8, cy - 1), (cx, cy + 3)], fill=hexc('#3A3448'))
            d.rectangle([cx - 5, cy - h, cx + 4, cy - 2], fill=hexc('#7A7090')); d.rectangle([cx - 5, cy - h, cx - 1, cy - 2], fill=hexc('#9A90AE'))
            for k in range(0, h - 4, 6): d.line([(cx - 5, cy - 4 - k), (cx + 4, cy - 4 - k)], fill=hexc('#5A5470'))
            d.polygon([(cx - 6, cy - h), (cx - 1, cy - h - 5), (cx + 2, cy - h + 1), (cx + 5, cy - h - 3), (cx + 5, cy - h + 2), (cx - 6, cy - h + 2)], fill=hexc('#9A90AE'))
        return f
    def rock(tx, ty, s):
        def f(img, d):
            cx, cy = R.P(tx + .5, ty + .5)
            d.polygon([(cx - 9 * s, cy), (cx - 6 * s, cy - 8 * s), (cx + 1, cy - 11 * s), (cx + 8 * s, cy - 6 * s), (cx + 9 * s, cy)], fill=hexc('#4A4058'))
            d.polygon([(cx - 9 * s, cy), (cx - 6 * s, cy - 8 * s), (cx + 1, cy - 11 * s), (cx - 1, cy)], fill=hexc('#6A5E78'))
        return f
    for (x, y, h) in ((1, 10, 34), (10, 1, 26), (2, 18, 20), (18, 2, 30), (1, 14, 16), (14, 1, 22)): R.obj('pillar', [(x, y)], pillar(x, y, h))
    for (x, y, s) in ((3, 20, 1.1), (20, 3, 1), (6, 19, .8), (19, 6, .9), (1, 6, 1.2), (6, 1, 1)): R.obj('rock', [(x, y)], rock(x, y, s))
    # ---- 돌아가는 문 (돌 아치 · 보랏빛 소용돌이) ----
    def back_gate(img, d): gate_draw(d, *R.P(10.5, 20.5))
    R.obj('gate_back', [(10, 20)], back_gate, act=('돌아가는 문', '학교로 돌아가기'))
    R.light(10.5, 20.5, -30, 30, [190, 130, 255], .6, 1)
    R.extra = dict(night=False, indoor=False, fill='#2A1430', spawnIn=[17, 17])
    R.save('trialland', '시련의 언덕', '시련의 탑 · 혼자 오르는 50 층', [71, 13])
    m = json.load(open('out/trialland.json')); ex = [o for o in m['objs'] if o['name'] == 'exit'][0]; ex['box'] = [10, 21, 11, 22]; ex['door']['tile'] = [10, 21]; ex['door']['lock'] = 'twback'; ex['door']['label'] = '돌아가는 문'; json.dump(m, open('out/trialland.json', 'w'), ensure_ascii=False)
    return R

def gate_draw(d, cx, cy, big=1):
    s = big
    d.polygon([(cx - 16 * s, cy), (cx, cy - 7 * s), (cx + 16 * s, cy), (cx, cy + 7 * s)], fill=hexc('#3A3448'))   # 받침
    for side in (-1, 1):
        x0 = cx + side * 11 * s
        d.rectangle([x0 - 4 * s, cy - 44 * s, x0 + 4 * s, cy - 2 * s], fill=hexc('#7A7090')); d.rectangle([x0 - 4 * s, cy - 44 * s, x0 - 1 * s, cy - 2 * s], fill=hexc('#9A90AE'))
        for k in range(5): d.line([(x0 - 4 * s, cy - 8 * s - k * 8 * s), (x0 + 4 * s, cy - 8 * s - k * 8 * s)], fill=hexc('#5A5470'))
    d.pieslice([cx - 15 * s, cy - 58 * s, cx + 15 * s, cy - 30 * s], 180, 360, fill=hexc('#8A80A0')); d.pieslice([cx - 8 * s, cy - 52 * s, cx + 8 * s, cy - 36 * s], 180, 360, fill=hexc('#2A1A3A'))
    d.rectangle([cx - 7 * s, cy - 44 * s, cx + 7 * s, cy - 3 * s], fill=hexc('#5A2A8A'))   # 소용돌이 바탕
    for k in range(40):   # 소용돌이
        a = k * .5; r = k * .17 * s
        x, y = cx + math.cos(a) * r * .9, cy - 24 * s + math.sin(a) * r * 1.7
        d.point((x, y), fill=hexc('#E0B8FF') if k % 3 else hexc('#FFFFFF')); d.point((x + .5, y), fill=hexc('#B07AFF'))
    d.polygon([(cx, cy - 64 * s), (cx + 4 * s, cy - 58 * s), (cx, cy - 54 * s), (cx - 4 * s, cy - 58 * s)], fill=hexc('#FF8A3A'))   # 꼭대기 불꽃 보석

def gate_prop():   # 학교에 세우는 「시련의 문」 소품 (48 × 72)
    im = Image.new('RGBA', (48, 72), (0, 0, 0, 0)); d = ImageDraw.Draw(im); gate_draw(d, 24, 64); outline_img(im); im.save('out/trial_gate.png')

def preview(key, out, scale=2, dark=.9):
    m = json.load(open(f'out/{key}.json')); bg = Image.open(f'out/{key}_bg.png').convert('RGBA'); sh = Image.open(f'out/{key}_obj.png').convert('RGBA')
    im = bg.copy()
    for o in sorted([o for o in m['objs'] if o['sw']], key=lambda o: o['y'] + o['sh']):
        im.alpha_composite(sh.crop((o['sx'], o['sy'], o['sx'] + o['sw'], o['sy'] + o['sh'])), (o['x'], o['y']))
    im = Image.eval(im.convert('RGB'), lambda v: int(v * dark)).convert('RGBA')
    glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for L in m['lights']:
        x, y = L['p'][0], L['p'][1] + L.get('dy', 0); r = L['r']
        for k in range(r, 0, -2): gd.ellipse([x - k, y - k * .7, x + k, y + k * .7], fill=tuple(L['c']) + (int(255 * L['a'] * .16 * (1 - k / r)),))
    glow = glow.filter(ImageFilter.GaussianBlur(3)); base = im.load(); g = glow.load()
    for y in range(im.height):
        for x in range(im.width):
            a = g[x, y]
            if a[3]: c = base[x, y]; k = a[3] / 255 * 2.2; base[x, y] = (min(255, int(c[0] + a[0] * k)), min(255, int(c[1] + a[1] * k)), min(255, int(c[2] + a[2] * k)), 255)
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(out)

if __name__ == '__main__':
    trialland(); gate_prop(); preview('trialland', 'out/trial_prev.png')
    Image.open('out/trial_gate.png').resize((192, 288), Image.NEAREST).save('out/trial_gate_prev.png'); print('ok')
