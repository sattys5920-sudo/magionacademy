# 그림자 골목 집 안 다섯 곳 (뱀파이어 저택 · 학교 박물관 · 낡은 연구 탑 · 마녀 오두막 · 늑대인간 통나무집)
#   python3 quarter_rooms.py → out/vamp_manor·museum·lab_tower·witch_hut·wolf_cabin (_bg.png _obj.png .json)
#   의뢰인이 사는 집이에요: 이야기가 꽤 진행되면(그 사람의 의뢰 3단계부터) 들어갈 수 있고, 안에서 의뢰인을 만나요 (index.html QHOME · World.canEnter)
#   크기: 저택 36×26(천장 높게) · 박물관 30×22 · 연구 탑 28×20 · 마녀 오두막 26×18 · 통나무집 26×18
import json, math, random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade, up, checker, planks, rug, table_draw, chair_draw, plant_draw, float_candle, bookshelf, cauldron_draw, crates, chalkboard
from PIL import ImageDraw
random.seed(404)
def common(R, floor, paper, paper2, wain, trim, vw=240):
    R.floor(floor); R.walls(paper, paper2, wain, trim=trim); R.extra = dict(vw=vw)
def tiles(x, y, w, d): return [(a, b) for a in range(x, x + w) for b in range(y, y + d)]
def wall_frame(R, side, u0, w, h, v0, border, inner, fn=None):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        if uu < 2 or uu >= w - 2 or vv < 2 or vv >= h - 2: return hexc(border)
        return fn(uu, vv) if fn else hexc(inner)
    R.wall_fill(side, f)
def portrait(R, side, u0, face='#C8B8A8', hair='#2A1A22', bg='#2E1E30', v0=34, big=False):
    s = 1.3 if big else 1
    def fn(uu, vv):
        if (uu - 8 * s) ** 2 / (20 * s * s) + (vv - 17 * s) ** 2 / (34 * s * s) < 1: return hexc(face)
        if (uu - 8 * s) ** 2 / (34 * s * s) + (vv - 17 * s) ** 2 / (60 * s * s) < 1 and vv > 16 * s: return hexc(hair)
        return shade(hexc(bg), 1.3) if vv < 8 else hexc(bg)
    wall_frame(R, side, u0, int(17 * s), int(28 * s), v0, '#C49446', bg, fn)
def tapestry(R, side, u0, w, h, col, v0=22, emblem='#E8C85A'):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        if vv < 4 and 0 <= uu < w: return hexc('#C49446')
        tip = (w // 2 - abs(uu - w // 2)) * .8
        if vv < 12 + tip * 0 and False: return None
        if vv > h - 8 + (abs(uu - w // 2) * .5) and vv > 8: return None
        c = hexc(col); k = 0
        if uu < 2 or uu >= w - 2: c = shade(c, .75)
        if abs(uu - w // 2) + abs(vv - h // 2) < 7 and abs(abs(uu - w // 2) - abs(vv - h // 2)) < 2: c = hexc(emblem)
        if abs(uu - w // 2) < 2 and abs(vv - h // 2) < 8: c = hexc(emblem)
        return c
    R.wall_fill(side, f)
def mirror(R, side, u0, w=22, h=40, v0=28):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        cx, cy = w / 2, h / 2
        r = ((uu + .5 - cx) / cx) ** 2 + ((vv + .5 - cy) / cy) ** 2
        if r > 1: return None
        if r > .72: return hexc('#C49446')
        return hexc('#6A6A86') if (uu + vv) % 11 else hexc('#8A8AA8')
    R.wall_fill(side, f)
def fireplace(R, side, u0, w=40, h=46, stone=('#6A6270', '#524A5A'), fire=('#FF8A2A', '#FFC84A')):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 0 <= v < h): return None
        if uu < 5 or uu >= w - 5 or v >= h - 5: return hexc(stone[0]) if (uu + v // 4) % 5 else hexc(stone[1])
        if v < 3: return hexc('#2A2030')
        fl = (math.sin(uu * .6) + 1) * 6
        if v < 16 + fl and 6 < uu < w - 6: return hexc(fire[0]) if (uu * 3 + v) % 4 else hexc(fire[1])
        return hexc('#1A1018')
    R.wall_fill(side, f)
    x, y = R.wall_px(side, u0 + w / 2, 12); R.lights.append(dict(p=(x, y), dy=0, r=50, c=[255, 150, 70], a=.65, f=1))
def column(R, tx, ty, h=64, col='#D8D0E0'):
    def f(img, d):
        R.box(img, tx + .05, ty + .05, .9, .9, 6, shade(hexc(col), .85), shade(hexc(col), .7), shade(hexc(col), .6))
        x, y = R.P(tx + .5, ty + .5)
        d.rectangle([x - 5, y - h, x + 5, y - 6], fill=hexc(col)); d.rectangle([x - 5, y - h, x - 1, y - 6], fill=shade(hexc(col), .85))
        for k in range(-h + 8, -6, 8): d.line([(x - 5, y + k), (x + 5, y + k)], fill=shade(hexc(col), .8))
        d.rectangle([x - 7, y - h - 4, x + 7, y - h], fill=shade(hexc(col), 1.05)); d.rectangle([x - 6, y - h - 7, x + 6, y - h - 4], fill=hexc(col))
    R.obj('column', [(tx, ty)], f)
def chandelier(R, tx, ty, h=82, col='#C49446', n=6, light=(255, 200, 130)):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.line([(x, y - h - 30), (x, y - h)], fill=hexc('#3A3040')); d.ellipse([x - 16, y - h - 4, x + 16, y - h + 6], outline=hexc(col), width=2); d.ellipse([x - 9, y - h - 1, x + 9, y - h + 4], outline=hexc(col))
        for k in range(n):
            a = k * 2 * math.pi / n; px, py = x + math.cos(a) * 14, y - h + 1 + math.sin(a) * 4
            d.rectangle([px - 1, py - 7, px + 1, py], fill=hexc('#F2E6C8')); d.rectangle([px - 1, py - 9, px, py - 7], fill=hexc('#FFD27A'))
        d.polygon([(x - 3, y - h + 6), (x + 3, y - h + 6), (x, y - h + 14)], fill=hexc(col))
    R.obj('chandelier', [(tx, ty)], f, solid=False); R.light(tx + .5, ty + .5, -h + 4, 64, list(light), .6, 1)
def candelabra(R, tx, ty, h=34):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 5, y - 3, x + 5, y + 2], fill=hexc('#9A7430')); d.rectangle([x - 1, y - h, x, y - 3], fill=hexc('#C49446')); d.line([(x - 8, y - h + 6), (x + 8, y - h + 6)], fill=hexc('#C49446'))
        for dx in (-8, 0, 8): d.rectangle([x + dx - 1, y - h - 4 + (6 if dx else 0), x + dx, y - h + (6 if dx else 2)], fill=hexc('#F2E6C8')); d.point((x + dx, y - h - 6 + (6 if dx else 0)), fill=hexc('#FFD27A'))
    R.obj('candelabra', [(tx, ty)], f); R.light(tx + .5, ty + .5, -h, 28, [255, 200, 120], .5, 1)
def armor(R, tx, ty, col='#9AA0AA'):
    def f(img, d):
        R.box(img, tx + .15, ty + .15, .7, .7, 5, '#4E4856', '#3A3444', '#443E50'); x, y = R.P(tx + .5, ty + .5)
        d.rectangle([x - 5, y - 24, x + 5, y - 9], fill=hexc(col)); d.rectangle([x - 5, y - 24, x - 1, y - 9], fill=shade(hexc(col), .8)); d.rectangle([x - 4, y - 9, x - 1, y - 5], fill=hexc(col)); d.rectangle([x + 1, y - 9, x + 4, y - 5], fill=hexc(col))
        d.ellipse([x - 4, y - 34, x + 4, y - 24], fill=hexc(col)); d.rectangle([x - 3, y - 31, x + 3, y - 29], fill=hexc('#2A2630')); d.polygon([(x - 1, y - 34), (x + 1, y - 34), (x, y - 40)], fill=hexc('#A81E2E'))
        d.line([(x + 7, y - 6), (x + 7, y - 32)], fill=hexc('#6A4A2E')); d.polygon([(x + 5, y - 32), (x + 9, y - 32), (x + 7, y - 38)], fill=hexc('#C8CCD4'))
    R.obj('armor', [(tx, ty)], f, act=('빈 갑옷', '살펴보기'))
def throne(R, tx, ty, col='#7A1E2E'):
    def f(img, d):
        R.box(img, tx, ty, 2, 1.2, 10, col, shade(hexc(col), .7), shade(hexc(col), .85)); R.box(img, tx + .1, ty, 1.8, .3, 36, shade(hexc(col), 1.1), shade(hexc(col), .7), shade(hexc(col), .85), lift=10)
        x, y = R.P(tx + 1, ty + .3); d.polygon([(x - 14, y - 46), (x - 8, y - 56), (x - 4, y - 48), (x, y - 58), (x + 4, y - 48), (x + 8, y - 56), (x + 14, y - 46)], fill=hexc('#C49446')); d.rectangle([x - 14, y - 46, x + 14, y - 44], fill=hexc('#C49446'))
    R.obj('throne', tiles(tx, ty, 2, 1), f, act=('높은 등받이 의자', '앉아 보기'))
def dais(R, x0, y0, w, d_, lift=6, col='#5A1E2A'):
    def f(img, d):
        R.box(img, x0, y0, w, d_, lift, col, shade(hexc(col), .6), shade(hexc(col), .75)); R.box(img, x0 + .4, y0 + .3, w - .8, d_ - .5, lift, shade(hexc(col), 1.1), shade(hexc(col), .6), shade(hexc(col), .75), lift=lift)
    R.obj('dais', tiles(x0, y0, w, d_), f, solid=False)
def couch(R, tx, ty, w=2, col='#6A1E2E', facing='down'):
    def f(img, d):
        R.box(img, tx, ty, w, 1, 7, col, shade(hexc(col), .65), shade(hexc(col), .8)); R.box(img, tx, ty, w, .35, 16, shade(hexc(col), .9), shade(hexc(col), .6), shade(hexc(col), .75))
        R.box(img, tx - .1, ty, .3, 1, 12, shade(hexc(col), 1.1), shade(hexc(col), .65), shade(hexc(col), .8)); R.box(img, tx + w - .2, ty, .3, 1, 12, shade(hexc(col), 1.1), shade(hexc(col), .65), shade(hexc(col), .8))
    R.obj('couch', tiles(tx, ty, w, 1), f, act=('푹신한 소파', '앉아서 쉬기'))
def rosevase(R, tx, ty, col='#D8283A'):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.polygon([(x - 4, y - 2), (x + 4, y - 2), (x + 3, y - 10), (x - 3, y - 10)], fill=hexc('#E8E0F0')); d.ellipse([x - 5, y - 3, x + 5, y + 1], fill=hexc('#C8C0D8'))
        for dx, dy in ((-3, -16), (3, -17), (0, -20), (-4, -12), (4, -13)): d.line([(x, y - 10), (x + dx, y + dy)], fill=hexc('#2E5A32')); d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=hexc(col))
    R.obj('rosevase', [(tx, ty)], f)
def globe(R, tx, ty):
    def f(img, d):
        R.box(img, tx + .2, ty + .2, .6, .6, 8, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 7, y - 24, x + 7, y - 10], fill=hexc('#3A6A8A')); d.ellipse([x - 5, y - 21, x - 1, y - 16], fill=hexc('#6A9A4A')); d.arc([x - 9, y - 26, x + 9, y - 8], 60, 300, fill=hexc('#C49446'))
    R.obj('globe', [(tx, ty)], f, act=('낡은 지구본', '돌려 보기'))
def winerack(R, tx, ty, w=3):
    def f(img, d):
        R.box(img, tx, ty, w, .9, 24, '#4A2E1A', '#3A2216', '#523520')
        for k in range(int(w)):
            x, y = R.P(tx + .5 + k, ty + .9)
            for r in range(3):
                for c in range(2): d.ellipse([x - 7 + c * 8, y - 20 + r * 7 - 2, x - 3 + c * 8, y - 16 + r * 7 + 2], fill=hexc(['#3A1E2A', '#2E3A22', '#4A2A1E'][(k + r + c) % 3]))
    R.obj('winerack', tiles(tx, ty, w, 1), f, act=('포도주 선반', '살펴보기'))
def glass_case(R, tx, ty, w, inner, d_=.9):
    def f(img, d):
        R.box(img, tx, ty, w, d_, 9, '#5A4A38', '#3E3024', '#4A3A2C'); R.box(img, tx + .05, ty + .05, w - .1, d_ - .1, 12, (200, 230, 255, 120), (190, 220, 250, 110), (190, 220, 250, 110), lift=9)
        for k in range(int(w)):
            x, y = R.P(tx + .5 + k, ty + .5); inner(d, x, y - 12, k)
    R.obj('case', tiles(tx, ty, int(w), 1), f, act=('유리 진열장', '구경하기'))
def finish(R, key, title, sub, back):
    R.exit_label = '그림자 골목'; R.exit_to = 'quarter'; R.save(key, title, sub, back)
def tall_windows(R, side, us, glass, w=18, h=44, v0=26):
    for u in us: R.window(side, u, w, v0, h, glass=glass)
def sconces(R, side, us):
    for u in us: R.sconce(side, u)
# ============ 1. 뱀파이어 저택 (블라디) · 36×26 ============
def vamp_manor():
    NX, NY = 36, 26
    R = Room(NX, NY, 92)
    def floor(fx, fy):
        c = checker('#26202E', '#D8D0E0', 1)(fx, fy) if False else (hexc('#D0C8D8') if (int(fx) + int(fy)) % 2 else hexc('#2A2432'))
        if (fx * 1) % 1 < .05 or (fy * 1) % 1 < .05: c = shade(c, .85)
        cx = 18.0
        if 15 <= fx < 21 and fy >= 4:
            e = min(fx - 15, 21 - fx)
            c = hexc('#C49446') if e < .22 else hexc('#5A1020') if e < .55 else hexc('#7A1428')
            if abs(fx - cx) < .12 and int(fy * 3) % 2 == 0: c = hexc('#9A2438')
        if ((fx - cx) ** 2 + ((fy - 13.5) * .8) ** 2) < 7.5:
            r = math.hypot(fx - cx, (fy - 13.5) * .8)
            c = hexc('#C49446') if abs(r - 2.5) < .18 or abs(r - 1.6) < .1 else (hexc('#3A0A18') if r > 1.6 else hexc('#8A1A30'))
        if 3 <= fx < 12 and 17 <= fy < 24:
            e = min(fx - 3, 12 - fx, fy - 17, 24 - fy); c = hexc('#C49446') if e < .18 else (hexc('#3A2A5E') if e < .5 else hexc('#4A3A78'))
        if 24 <= fx < 33 and 17 <= fy < 24:
            e = min(fx - 24, 33 - fx, fy - 17, 24 - fy); c = hexc('#C49446') if e < .18 else (hexc('#5A1020') if e < .5 else hexc('#6A1A2A'))
        return c
    common(R, floor, '#4A1E2A', '#6A2A3C', '#241A22', '#C49446', vw=300)
    tall_windows(R, 'R', (16, 70, 118, 182, 230), ('#241848', '#4A3A8A', '#8A7AE0'), 20, 56, 26)
    tall_windows(R, 'L', (22, 70, 122, 160), ('#241848', '#4A3A8A', '#8A7AE0'), 20, 56, 26)
    tapestry(R, 'R', 46, 18, 54, '#7A1428', 30); tapestry(R, 'R', 96, 18, 54, '#7A1428', 30); tapestry(R, 'R', 150, 18, 54, '#7A1428', 30); tapestry(R, 'R', 206, 18, 54, '#7A1428', 30)
    portrait(R, 'R', 270 - 40 if False else 262, '#D8C8B8', '#1A1018', big=True)
    portrait(R, 'L', 46, '#D0C0B0', '#3A2A2A', big=True); portrait(R, 'L', 94, '#B8B0C8', '#2A2A3A', big=True); portrait(R, 'L', 140, '#C8B098', '#6A2A22', big=True)
    mirror(R, 'L', 8, 22, 44, 30)
    sconces(R, 'R', (36, 62, 88, 134, 142, 196, 220, 252)); sconces(R, 'L', (14, 58, 110, 132, 166))
    fireplace(R, 'L', 172, 40, 50, ('#6A6270', '#524A5A'))
    # 무대·옥좌
    dais(R, 13, 1, 10, 3, 6, '#5A1E2A'); dais(R, 14, 1, 8, 2, 12, '#6A2434')
    throne(R, 17, 2, '#8A1428'); candelabra(R, 14, 3); candelabra(R, 21, 3); R.obj('rosevase', [(13, 3)], lambda i, d: None, solid=False) if False else None
    # 기둥과 샹들리에
    for y in (7, 11, 15, 19):
        column(R, 11, y); column(R, 24, y)
    for (x, y) in ((18, 8), (18, 16), (7, 13), (29, 13)): chandelier(R, x, y, 90, n=8)
    # 입구 갑옷
    armor(R, 15, 23); armor(R, 21, 23)
    for (x, y) in ((13, 22), (23, 22), (13, 6), (23, 6)): candelabra(R, x, y)
    # 왼쪽: 식당 구역
    for x in range(3, 9): R.obj('table', [(x, 20)], table_draw(R, x, 20, '#3A1E1E', (('cup', 'cake'), ('book',), ('cup',), ('pumpkin',), ('cup', 'cake'), ('cup',))[x - 3]), act=('긴 식탁', '살펴보기'))
    for x in range(3, 9): R.obj('chair', [(x, 19)], chair_draw(R, x, 19, '#6A1E2E')); R.obj('chair', [(x, 21)], chair_draw(R, x, 21, '#6A1E2E'))
    R.obj('chair', [(2, 20)], chair_draw(R, 2, 20, '#8A2A3E')); R.obj('chair', [(9, 20)], chair_draw(R, 9, 20, '#8A2A3E'))
    winerack(R, 2, 24, 4); rosevase(R, 7, 24); rosevase(R, 9, 24)
    couch(R, 3, 8, 3, '#4A1E5E'); couch(R, 3, 12, 3, '#4A1E5E')
    R.obj('table', [(7, 10)], table_draw(R, 7, 10, '#3A1E1E', ('cup',)), act=('작은 탁자', '살펴보기')); rosevase(R, 7, 9)
    # 오른쪽: 오르간·서재
    def organ(img, d):
        R.box(img, 26, 2, 4, 1.4, 16, '#2A1E24', '#1E161C', '#2E2228'); R.box(img, 26.1, 3.4, 3.8, .5, 8, '#E8E0D0', '#1E161C', '#C8C0B0', lift=6)
        for k in range(10): x, y = R.P(26.4 + k * .38, 3.6); d.line([(x, y - 12), (x, y - 8)], fill=hexc('#1A1018'))
        for k in range(5): x, y = R.P(27.5 + k * .55, 2.3); d.rectangle([x - 2, y - 34, x + 2, y - 16], fill=hexc('#C49446')); d.rectangle([x - 1, y - 36, x + 1, y - 34], fill=hexc('#E8D88A'))
    R.obj('organ', tiles(26, 2, 4, 2), organ, act=('커다란 오르간', '건반 눌러 보기'))
    bookshelf(R, 'R', 236, 36)
    for x in range(29, 33): R.obj('table', [(x, 9)], table_draw(R, x, 9, '#3A2A1E', (('book',), ('cup',), ('book', 'cup'), ('book',))[x - 29]), act=('서재 책상', '살펴보기'))
    globe(R, 28, 8); R.obj('chair', [(30, 10)], chair_draw(R, 30, 10, '#4A1E5E')); R.obj('chair', [(31, 10)], chair_draw(R, 31, 10, '#4A1E5E'))
    couch(R, 26, 13, 3, '#6A1428'); couch(R, 30, 13, 3, '#6A1428')
    def coffin(img, d):
        R.box(img, 26, 19, 4, 2, 9, '#2A1A1E', '#3A2228', '#4A2A32'); R.box(img, 26.1, 19.1, 3.8, 1.8, 13, '#4A2A32', '#3A2228', '#4A2A32')
        x, y = R.P(28, 20); d.line([(x - 12, y - 17), (x + 12, y - 11)], fill=hexc('#C49446'), width=1); d.ellipse([x - 3, y - 17, x + 3, y - 13], fill=hexc('#C49446'))
    R.obj('coffin', tiles(26, 19, 4, 2), coffin, act=('블라디의 관', '들여다보기')); candelabra(R, 25, 19); candelabra(R, 30, 19); rosevase(R, 31, 22); rosevase(R, 25, 22)
    def clock(img, d):
        R.box(img, 33, 6, 1, 1, 56, '#4A2E1E', '#3A2216', '#5A3826'); x, y = R.P(33.5, 6.5)
        d.ellipse([x - 6, y - 50, x + 6, y - 38], fill=hexc('#E8DCC0')); d.line([(x, y - 44), (x, y - 49)], fill=hexc('#2A1A12')); d.line([(x, y - 44), (x + 4, y - 42)], fill=hexc('#2A1A12')); d.rectangle([x - 4, y - 32, x + 4, y - 14], fill=hexc('#2A1A12')); d.line([(x, y - 30), (x, y - 16)], fill=hexc('#C49446'))
    R.obj('clock', [(33, 6)], clock, act=('멈춘 시계', '들여다보기'))
    for (x, y) in ((1, 1), (1, 24), (34, 24), (34, 1), (1, 14), (34, 17)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4A3A4A', '#C83A4A'))
    R.light(18, 13, -40, 160, [255, 190, 130], .22, 1)
    finish(R, 'vamp_manor', '뱀파이어 저택', '블라디의 집 · 촛불이 둥둥 떠다녀요', [12, 14])
    return (NX, NY)
# ============ 2. 학교 박물관 (네페르) · 30×22 ============
def museum():
    NX, NY = 30, 22
    R = Room(NX, NY, 84)
    def floor(fx, fy):
        c = hexc('#D8CCB0') if (int(fx) + int(fy)) % 2 else hexc('#B8AC90')
        if (fx % 1 < .05) or (fy % 1 < .05): c = shade(c, .85)
        if 10 <= fx < 20 and 4 <= fy < 16:
            e = min(fx - 10, 20 - fx, fy - 4, 16 - fy); c = hexc('#C49446') if e < .2 else hexc('#2E5A8A') if e < .5 else hexc('#8A3A2E')
            if e >= .5 and abs(fx - 15) < .15: c = hexc('#C49446')
        return c
    common(R, floor, '#C8B286', '#B8A276', '#6A5438', '#C49446', vw=270)
    tall_windows(R, 'R', (20, 62, 110, 156, 198), ('#4A5A8A', '#7A8AC0', '#C0D0F0'), 18, 46, 26); tall_windows(R, 'L', (24, 80, 130), ('#4A5A8A', '#7A8AC0', '#C0D0F0'), 18, 46, 26)
    def glyph(uu, vv):
        if (uu // 6 + vv // 6) % 3 == 0 and uu % 6 in (1, 2, 3) and vv % 6 in (2, 3): return hexc('#2E5A8A')
        if (uu // 6 + vv // 8) % 4 == 1 and uu % 6 in (2, 3) and vv % 8 in (2, 4, 5): return hexc('#8A2A22')
        return hexc('#D8C494')
    wall_frame(R, 'R', 42, 48, 40, 30, '#8A7448', '#D8C494', glyph); wall_frame(R, 'R', 118, 32, 40, 30, '#8A7448', '#D8C494', glyph); wall_frame(R, 'R', 164, 28, 40, 30, '#8A7448', '#D8C494', glyph)
    wall_frame(R, 'L', 40, 36, 40, 30, '#8A7448', '#D8C494', glyph); wall_frame(R, 'L', 108, 36, 40, 30, '#8A7448', '#D8C494', glyph)
    sconces(R, 'R', (34, 104, 150, 192, 232)); sconces(R, 'L', (16, 70, 100, 150))
    R.shelf('L', 160, 30, 62, ['#8A7448', '#B8A276', '#6A5438', '#C8B286'])
    def sarc(img, d):
        R.box(img, 13, 7, 4, 2, 10, '#7A5A2A', '#5A4020', '#6A4A26'); R.box(img, 13.1, 7.1, 3.8, 1.8, 16, '#E0B84A', '#B8902E', '#C8A03A')
        x, y = R.P(15, 8); d.ellipse([x - 10, y - 28, x - 2, y - 18], fill=hexc('#E8C85A')); d.rectangle([x - 9, y - 22, x - 3, y - 20], fill=hexc('#2E5A8A')); d.line([(x - 4, y - 18), (x + 12, y - 13)], fill=hexc('#2E5A8A'), width=2); d.line([(x - 2, y - 22), (x + 12, y - 17)], fill=hexc('#8A2A22'))
    R.obj('sarcophagus', tiles(13, 7, 4, 2), sarc, act=('금빛 석관', '들여다보기'))
    inner_a = lambda d, x, y, k: d.ellipse([x - 3, y - 4, x + 3, y], fill=hexc(['#C84A2E', '#2E8A8A', '#E0B84A'][k % 3]))
    def inner_b(d, x, y, k): d.rectangle([x - 3, y - 4, x + 3, y], fill=hexc('#B8A276')); d.line([(x - 3, y - 2), (x + 3, y - 2)], fill=hexc('#6A5438'))
    for (x, y, f_) in ((2, 2, inner_a), (8, 2, inner_b), (20, 2, inner_a), (25, 2, inner_b), (2, 19, inner_b), (8, 19, inner_a), (20, 19, inner_b), (25, 19, inner_a)): glass_case(R, x, y, 4, f_)
    for (x, y, f_) in ((2, 8, inner_a), (2, 12, inner_b)): glass_case(R, x, y, 1, f_)
    for (x, y, f_) in ((27, 8, inner_b), (27, 12, inner_a)): glass_case(R, x, y, 1, f_)
    def statue(tx, ty, col):
        def f(img, d):
            R.box(img, tx + .1, ty + .1, .8, .8, 7, '#8A7448', '#6A5438', '#7A6440'); x, y = R.P(tx + .5, ty + .5)
            d.rectangle([x - 4, y - 24, x + 4, y - 8], fill=hexc(col)); d.rectangle([x - 4, y - 24, x, y - 8], fill=shade(hexc(col), .85)); d.ellipse([x - 4, y - 32, x + 4, y - 24], fill=hexc(col))
            d.polygon([(x - 5, y - 30), (x, y - 36), (x + 5, y - 30)], fill=hexc('#2E5A8A'))
        R.obj('statue', [(tx, ty)], f, act=('고대 조각상', '올려다보기'))
    for (x, y) in ((8, 6), (21, 6), (8, 15), (21, 15), (5, 10), (24, 10)): statue(x, y, '#C8B898')
    for (x, y) in ((6, 4), (23, 4), (6, 17), (23, 17)): column(R, x, y, 56, '#E0D0A8')
    def pedestal(tx, ty):
        def f(img, d):
            R.box(img, tx + .15, ty + .15, .7, .7, 8, '#E8E0D0', '#B8B0A0', '#C8C0B0'); x, y = R.P(tx + .5, ty + .5)
            d.polygon([(x - 3, y - 10), (x + 3, y - 10), (x + 4, y - 15), (x + 1, y - 18), (x - 1, y - 18), (x - 4, y - 15)], fill=hexc('#B85A3A')); d.line([(x - 3, y - 13), (x + 3, y - 13)], fill=hexc('#E8C85A'))
        R.obj('vase', [(tx, ty)], f, act=('유물 받침대', '살펴보기'))
    for (x, y) in ((13, 12), (16, 12), (12, 4), (17, 4), (4, 6), (25, 6), (4, 15), (25, 15)): pedestal(x, y)
    def mapt(img, d):
        R.box(img, 12, 17, 6, 1.6, 10, '#6A4A2E', '#4A3220', '#5A3E28'); R.box(img, 12.1, 17.1, 5.8, 1.4, 11, '#E8D8A8', '#8A6A3A', '#A8864A')
        x, y = R.P(15, 17.8); d.line([(x - 18, y - 13), (x + 12, y - 15)], fill=hexc('#8A2A22')); d.ellipse([x + 2, y - 15, x + 6, y - 11], fill=hexc('#2E5A8A'))
    R.obj('maptable', tiles(12, 17, 6, 2), mapt, act=('유적 지도 탁자', '살펴보기'))
    def mummycase(img, d):
        R.box(img, 26, 15, 2, 2, 8, '#6A4A2E', '#4A3220', '#5A3E28'); R.box(img, 26.15, 15.15, 1.7, 1.7, 40, (200, 230, 255, 70), (190, 220, 250, 60), (190, 220, 250, 60), lift=8)
        x, y = R.P(27, 16); d.rectangle([x - 4, y - 36, x + 4, y - 12], fill=hexc('#E8E0C8')); d.ellipse([x - 4, y - 44, x + 4, y - 36], fill=hexc('#E8E0C8')); [d.line([(x - 4, y - 34 + k * 4), (x + 4, y - 32 + k * 4)], fill=hexc('#B8B098')) for k in range(5)]
    R.obj('mummycase', tiles(26, 15, 2, 2), mummycase, act=('붕대 감은 전시물', '구경하기'))
    for (x, y) in ((1, 20), (28, 20), (1, 1), (28, 1)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#6A8A4A', '#E0B84A'))
    for (x, y) in ((8, 10), (21, 10), (15, 3), (15, 14), (4, 13), (25, 13)): float_candle(R, x, y)
    R.light(15, 11, -30, 150, [255, 230, 170], .22, 0)
    finish(R, 'museum', '학교 박물관', '네페르가 지키는 유물 방', [31, 14])
    return (NX, NY)
# ============ 3. 낡은 연구 탑 (피스) · 28×20 ============
def lab_tower():
    NX, NY = 28, 20
    R = Room(NX, NY, 86)
    def floor(fx, fy):
        c = hexc('#3A3C4A') if (int(fx) + int(fy)) % 2 else hexc('#2E303E')
        if fx % 1 < .05 or fy % 1 < .05: c = shade(c, .8)
        if 9 <= fx < 17 and 4 <= fy < 11:
            e = min(fx - 9, 17 - fx, fy - 4, 11 - fy); c = hexc('#E0A83A') if int(fx + fy) % 2 == 0 and e < .4 else (hexc('#4A4A5A') if e > .4 else hexc('#2A2A36'))
        return c
    common(R, floor, '#2E3E44', '#3A4E54', '#20242C', '#8A9AAA', vw=260)
    tall_windows(R, 'R', (14, 56, 100, 150, 196), ('#1E2A3E', '#3A5A7A', '#B8E8FF'), 18, 50, 26); R.window('L', 36, 18, 26, 46, glass=('#1E2A3E', '#3A5A7A', '#B8E8FF')); R.window('L', 96, 18, 26, 46, glass=('#1E2A3E', '#3A5A7A', '#B8E8FF'))
    chalkboard(R, 40, 44, 'R'); chalkboard(R, 106, 40, 'R'); chalkboard(R, 150, 30, 'R', v0=36)
    sconces(R, 'R', (30, 94, 146, 192)); sconces(R, 'L', (16, 70, 120, 140))
    bookshelf(R, 'L', 20, 12) if False else None
    R.shelf('L', 140, 20, 56, ['#5A6A7A', '#7A8A9A', '#3A4A5A', '#E0A83A'])
    def coil(tx, ty, big=False):
        def f(img, d):
            R.box(img, tx + .1, ty + .1, .8, .8, 6, '#5A5A6A', '#3A3A4A', '#4A4A5A'); x, y = R.P(tx + .5, ty + .5)
            H = 52 if big else 40
            d.rectangle([x - 2, y - H, x + 2, y - 6], fill=hexc('#8A8A9A')); d.ellipse([x - 7, y - H - 12, x + 7, y - H + 2], fill=hexc('#C8E8FF')); d.ellipse([x - 3, y - H - 8, x + 3, y - H - 2], fill=hexc('#FFFFFF'))
            for k in range(4): d.line([(x - 5, y - H + 6 + k * 8), (x + 5, y - H + 8 + k * 8)], fill=hexc('#E0A83A'))
        R.obj('coil', [(tx, ty)], f, act=('번개 코일', '쳐다보기')); R.light(tx + .5, ty + .5, -50, 40, [150, 220, 255], .6, 1)
    for (x, y) in ((2, 3), (25, 3), (2, 16), (25, 16)): coil(x, y)
    coil(8, 7, True); coil(18, 7, True)
    def slab(img, d):
        R.box(img, 11, 6, 4, 2, 10, '#8A9AAA', '#5A6270', '#6A7280'); R.box(img, 11.1, 6.1, 3.8, 1.8, 14, '#D8E4EC', '#8A9AAA', '#A8B6C2')
        x, y = R.P(13, 7); d.line([(x - 9, y - 16), (x + 9, y - 12)], fill=hexc('#8A5A3A'), width=2); d.line([(x - 3, y - 17), (x - 1, y - 11)], fill=hexc('#6A4A2A')); d.line([(x + 4, y - 15), (x + 6, y - 9)], fill=hexc('#6A4A2A'))
        R.obj('slab', tiles(11, 6, 4, 2), lambda *_: None) if False else None
    R.obj('slab', tiles(11, 6, 4, 2), slab, act=('수술대', '살펴보기'))
    def bench(tx, ty, w):
        def f(img, d):
            R.box(img, tx, ty, w, 1, 11, '#6A6A78', '#3E3E4A', '#4E4E5A')
            for k in range(int(w)):
                x, y = R.P(tx + .5 + k, ty + .5); c = ['#6AE88A', '#FF6A8A', '#6AB8FF', '#E0C84A'][(k + int(tx)) % 4]
                d.rectangle([x - 2, y - 17, x + 2, y - 12], fill=hexc(c)); d.rectangle([x - 1, y - 20, x + 1, y - 17], fill=hexc('#C8D8E0'))
        R.obj('bench', tiles(tx, ty, w, 1), f, act=('실험대', '살펴보기'))
    for (x, y, w) in ((3, 8, 4), (21, 8, 4), (3, 12, 4), (21, 12, 4), (10, 14, 3), (15, 14, 3)): bench(x, y, w)
    def generator(img, d):
        R.box(img, 23, 15, 3, 2, 18, '#4E5A62', '#323A42', '#3E4850'); x, y = R.P(24.5, 16)
        d.ellipse([x - 6, y - 26, x + 6, y - 16], fill=hexc('#E0C84A')); d.line([(x, y - 21), (x + 4, y - 24)], fill=hexc('#2A2A2A'))
        d.rectangle([x + 8, y - 22, x + 11, y - 8], fill=hexc('#6A6A78')); d.rectangle([x - 14, y - 22, x - 10, y - 8], fill=hexc('#6A6A78'))
    R.obj('generator', tiles(23, 15, 3, 2), generator, act=('낡은 발전기', '살펴보기'))
    def cabinet(tx, ty):
        def f(img, d):
            R.box(img, tx, ty, 1, 1, 28, '#6A6A78', '#3E3E4A', '#4E4E5A'); x, y = R.P(tx + .5, ty + .5)
            for k in range(3): d.rectangle([x - 4, y - 24 + k * 8, x + 2, y - 20 + k * 8], fill=hexc('#2E3036')); d.point((x + 1, y - 22 + k * 8), fill=hexc('#E0C84A'))
        R.obj('cabinet', [(tx, ty)], f, act=('서류 보관함', '살펴보기'))
    for (x, y) in ((6, 2), (7, 2), (20, 2), (21, 2)): cabinet(x, y)
    for (x, y) in ((1, 6), (26, 6), (1, 11), (26, 11)): R.obj('crate', [(x, y)], crates(R, x, y, 2))
    for (x, y) in ((7, 5), (19, 5), (13, 11), (6, 17), (21, 17)): float_candle(R, x, y)
    R.light(13, 8, -20, 150, [150, 200, 255], .25, 1)
    finish(R, 'lab_tower', '낡은 연구 탑', '피스의 작업실 · 번개 맞은 흔적', [44, 14])
    return (NX, NY)
# ============ 4. 마녀 오두막 (베아트릭스) · 26×18 ============
def witch_hut():
    NX, NY = 26, 18
    R = Room(NX, NY, 80)
    def floor(fx, fy):
        c = planks(['#6A4A32', '#5E4128', '#745338'])(fx, fy)
        if 8 <= fx < 18 and 5 <= fy < 14:
            e = min(fx - 8, 18 - fx, fy - 5, 14 - fy); c = hexc('#C49446') if e < .2 else hexc('#5A3A8A') if e < .6 else hexc('#7A5ABA')
            r = math.hypot(fx - 13, (fy - 9.5) * 1.1)
            if abs(r - 2) < .12 or abs(r - 3) < .1: c = hexc('#E0C84A')
        return c
    common(R, floor, '#3A2E4A', '#4A3E5E', '#3A2418', '#B88A4A', vw=250)
    tall_windows(R, 'R', (28, 120), ('#241848', '#4A3A8A', '#8A7AE0'), 20, 40, 28); R.window('L', 58, 20, 28, 40, glass=('#241848', '#4A3A8A', '#8A7AE0'))
    R.shelf('R', 60, 30, 56, ['#6AE88A', '#C86AE8', '#E8C84A', '#6AB8FF', '#FF6A8A']); R.shelf('R', 150, 30, 56, ['#6AE88A', '#C86AE8', '#E8C84A', '#6AB8FF', '#FF6A8A']); R.shelf('L', 100, 30, 56, ['#8A5ABA', '#C86AE8', '#E8C84A', '#6AE88A'])
    def herbs(u0, side='R'):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < 12 and 38 <= v < 64): return None
            if v >= 60 and uu in (5, 6): return hexc('#8A6A3A')
            if v < 60 and (uu - 6) ** 2 / 25 + ((v - 48) / 11) ** 2 < 1: return hexc(['#4E8A4E', '#6AAA5A', '#8A5ABA'][(uu + v) % 3])
            return None
        R.wall_fill(side, f)
    for u in (22, 98, 124, 138, 180): herbs(u)
    for u in (26, 70, 112): herbs(u, 'L')
    sconces(R, 'R', (50, 108, 144)); sconces(R, 'L', (16, 44, 90, 118))
    R.obj('cauldron', [(4, 4), (5, 4), (4, 5), (5, 5)], cauldron_draw(R, 4, 4, '#6AE88A', 2.2), act=('커다란 마녀의 솥', '들여다보기')); R.light(5, 5, -14, 60, [120, 255, 150], .6, 1)
    def bed(img, d):
        R.box(img, 20, 12, 4, 3, 8, '#5A3A8A', '#4A2E70', '#5A3A8A'); R.box(img, 20.1, 12.1, 3.8, 1.2, 12, '#E8E0F0', '#8A7AA8', '#A89AC0'); R.box(img, 20.1, 13.4, 3.8, 1.5, 10, '#7A5ABA', '#4A2E70', '#5A3A8A', lift=0)
    R.obj('bed', tiles(20, 12, 4, 3), bed, act=('마녀의 침대', '살펴보기'))
    def ball(img, d):
        R.box(img, 12, 8, 2, 2, 9, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(13, 9)
        d.ellipse([x - 7, y - 24, x + 7, y - 10], fill=hexc('#B8A8F0')); d.ellipse([x - 4, y - 21, x + 1, y - 16], fill=hexc('#F0E8FF')); d.polygon([(x - 6, y - 10), (x + 6, y - 10), (x + 4, y - 8), (x - 4, y - 8)], fill=hexc('#C49446'))
    R.obj('crystal', tiles(12, 8, 2, 2), ball, act=('수정 구슬', '들여다보기')); R.light(13, 9, -18, 50, [190, 170, 255], .5, 1)
    def book(img, d):
        R.box(img, 16, 3, 1, 1, 14, '#3E2616', '#2A1A10', '#3A2216'); x, y = R.P(16.5, 3.5)
        d.polygon([(x - 7, y - 18), (x, y - 22), (x + 7, y - 18), (x, y - 14)], fill=hexc('#7A2A5A')); d.line([(x, y - 22), (x, y - 14)], fill=hexc('#E0C84A'))
    R.obj('spellbook', [(16, 3)], book, act=('낡은 마법서', '펼쳐 보기'))
    def broom(img, d):
        x, y = R.P(2.5, 14.5); d.line([(x - 7, y - 28), (x + 5, y - 2)], fill=hexc('#8A6A3A'), width=2); d.polygon([(x + 2, y - 5), (x + 10, y - 2), (x + 5, y + 4), (x - 1, y)], fill=hexc('#C8A04A'))
    R.obj('broom', [(2, 14)], broom, act=('기대어 둔 빗자루', '살펴보기'))
    R.obj('table', [(9, 14)], table_draw(R, 9, 14, '#5A3A22', ('cup', 'book')), act=('작은 탁자', '살펴보기')); R.obj('chair', [(8, 14)], chair_draw(R, 8, 14, '#5A3A8A')); R.obj('chair', [(10, 14)], chair_draw(R, 10, 14, '#5A3A8A'))
    R.obj('table', [(2, 8)], table_draw(R, 2, 8, '#5A3A22', ('cup',)), act=('약초 작업대', '살펴보기')); R.obj('table', [(2, 9)], table_draw(R, 2, 9, '#5A3A22', ('book', 'cup')), act=('약초 작업대', '살펴보기'))
    R.obj('crate', [(21, 3)], crates(R, 21, 3, 2)); R.obj('crate', [(22, 4)], crates(R, 22, 4, 1)); R.obj('crate', [(23, 3)], crates(R, 23, 3, 1))
    def cat(img, d):
        x, y = R.P(18.5, 15.5); d.ellipse([x - 5, y - 7, x + 5, y], fill=hexc('#1E1824')); d.ellipse([x - 3, y - 12, x + 3, y - 6], fill=hexc('#1E1824')); d.polygon([(x - 3, y - 11), (x - 2, y - 15), (x, y - 11)], fill=hexc('#1E1824')); d.polygon([(x + 3, y - 11), (x + 2, y - 15), (x, y - 11)], fill=hexc('#1E1824')); d.point((x - 1, y - 9), fill=hexc('#E0C84A')); d.point((x + 1, y - 9), fill=hexc('#E0C84A'))
    R.obj('cat', [(18, 15)], cat, act=('검은 고양이', '쓰다듬기'))
    for (x, y) in ((1, 2), (24, 16), (1, 12), (24, 8)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E8A4E', '#C86AE8'))
    for (x, y) in ((8, 3), (18, 8), (4, 10), (12, 16), (21, 5), (6, 14), (15, 4)): float_candle(R, x, y)
    R.light(13, 9, -30, 140, [190, 160, 255], .2, 0)
    finish(R, 'witch_hut', '마녀 오두막', '베아트릭스의 집 · 솥이 부글부글', [9, 30])
    return (NX, NY)
# ============ 5. 늑대인간 통나무집 (우르) · 26×18 ============
def wolf_cabin():
    NX, NY = 26, 18
    R = Room(NX, NY, 80)
    def floor(fx, fy):
        c = planks(['#7A5232', '#6A4428', '#865C3A'])(fx, fy)
        if 8 <= fx < 18 and 5 <= fy < 13:
            e = min(fx - 8, 18 - fx, fy - 5, 13 - fy); c = hexc('#3A2216') if e < .25 else hexc('#5A3220') if e < .6 else hexc('#4A2A1A')
        return c
    common(R, floor, '#7A5232', '#6A4428', '#4A2E1A', '#3A2216', vw=250)
    R.window('R', 24, 20, 28, 36, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0')); R.window('R', 150, 20, 28, 36, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0')); R.window('L', 54, 20, 28, 36, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0')); R.window('L', 100, 20, 28, 36, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0'))
    fireplace(R, 'R', 66, 56, 52, ('#7A6E66', '#5A504A'), ('#FF8A2A', '#FFC84A'))
    def antlers(u0, side='R'):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < 30 and 42 <= v < 68): return None
            c = hexc('#E8DCC0')
            if abs(uu - 15) <= 1 and v < 54: return c
            if v < 64 and abs(uu - 15) in (v - 42 + 2, v - 42 + 3) and 3 < uu < 27: return c
            if 54 <= v < 56 and abs(uu - 15) < 10: return c
            return None
        R.wall_fill(side, f)
    antlers(18); antlers(134); antlers(166); antlers(40, 'L'); antlers(96, 'L')
    def pelt(u0, w, col, side='R'):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < w and 34 <= v < 62): return None
            r = ((uu - w / 2) / (w / 2)) ** 2 + ((v - 48) / 14) ** 2
            if r > 1: return None
            return hexc(col) if (uu + v) % 7 else shade(hexc(col), .8)
        R.wall_fill(side, f)
    pelt(126, 20, '#5A4A3A'); pelt(188, 20, '#7A6A5A')
    sconces(R, 'R', (50, 128, 176)); sconces(R, 'L', (20, 76, 120))
    def bunk(tx, ty):
        def f(img, d):
            R.box(img, tx, ty, 3, 2, 8, '#5A3A22', '#3E2616', '#4A2E1C'); R.box(img, tx + .1, ty + .1, 2.8, 1.8, 11, '#8A4A3A', '#6A3228', '#7A3E30'); R.box(img, tx + .1, ty + .1, 2.8, 1.8, 11, '#8A4A3A', '#6A3228', '#7A3E30', lift=14)
        R.obj('bunk', tiles(tx, ty, 3, 2), f, act=('이층 침상', '살펴보기'))
    bunk(21, 2); bunk(21, 6)
    def bearrug(img, d):
        x, y = R.P(13, 9); d.ellipse([x - 30, y - 10, x + 30, y + 10], fill=hexc('#3E2A22')); d.ellipse([x - 28, y - 9, x + 28, y + 8], fill=hexc('#5A3E30')); d.ellipse([x - 38, y - 10, x - 26, y - 2], fill=hexc('#5A3E30')); d.point((x - 36, y - 6), fill=hexc('#1A1018')); d.point((x - 32, y - 6), fill=hexc('#1A1018'))
    R.obj('bearrug', [(12, 8)], bearrug, solid=False)
    def rack(img, d):
        R.box(img, 2, 6, 1, 3, 6, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(2.5, 7.5)
        d.line([(x - 4, y - 8), (x + 4, y - 26)], fill=hexc('#8A8A92'), width=1); d.arc([x - 4, y - 30, x + 8, y - 6], 100, 260, fill=hexc('#A8824E'), width=2); d.line([(x + 6, y - 10), (x + 10, y - 24)], fill=hexc('#6A4428'), width=2); d.polygon([(x + 8, y - 26), (x + 14, y - 22), (x + 10, y - 20)], fill=hexc('#9AA0A8'))
    R.obj('rack', tiles(2, 6, 1, 3), rack, act=('사냥 도구 걸이', '살펴보기'))
    def wood(img, d):
        for k in range(4): R.box(img, 1 + k * .03, 13, 1.1, 1.4, 5, '#8A6A3E', '#5A3E24', '#6A4A2E', lift=k * 5)
    R.obj('woodpile', tiles(1, 13, 2, 2), wood, act=('장작더미', '살펴보기'))
    def pot(img, d):
        R.box(img, 3, 3, 1.4, 1.4, 8, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(3.7, 3.7); d.ellipse([x - 8, y - 22, x + 8, y - 10], fill=hexc('#4A4A52')); d.ellipse([x - 6, y - 21, x + 6, y - 13], fill=hexc('#C8864A')); d.line([(x + 2, y - 18), (x + 10, y - 28)], fill=hexc('#8A6A3E'), width=2)
    R.obj('pot', tiles(3, 3, 1, 1), pot, act=('스튜 냄비', '냄새 맡기')); R.light(3.7, 3.7, -16, 30, [255, 170, 80], .4, 1)
    for x in range(11, 15): R.obj('table', [(x, 14)], table_draw(R, x, 14, '#6A4428', (('cup', 'cake'), ('cup',), ('book',), ('cup', 'cake'))[x - 11]), act=('통나무 식탁', '살펴보기'))
    for x in range(11, 15): R.obj('chair', [(x, 13)], chair_draw(R, x, 13, '#8A4A2E')); R.obj('chair', [(x, 15)], chair_draw(R, x, 15, '#8A4A2E'))
    def stool(tx, ty):
        R.obj('stool', [(tx, ty)], lambda img, d: R.box(img, tx + .2, ty + .2, .6, .6, 8, '#8A6240', '#5A3E24', '#6A4A2E'))
    for (x, y) in ((19, 10), (20, 11), (5, 11)): stool(x, y)
    R.obj('crate', [(23, 13)], crates(R, 23, 13, 2)); R.obj('crate', [(24, 14)], crates(R, 24, 14, 1)); R.obj('crate', [(23, 15)], crates(R, 23, 15, 1))
    for (x, y) in ((1, 2), (24, 10), (1, 16)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E7A3E', '#E8A050'))
    for (x, y) in ((6, 9), (18, 7), (10, 16), (8, 3), (16, 14), (4, 5)): float_candle(R, x, y)
    R.light(13, 9, -30, 140, [255, 180, 110], .22, 0)
    finish(R, 'wolf_cabin', '늑대인간 통나무집', '우르의 집 · 벽난로가 따뜻해요', [28, 30])
    return (NX, NY)
if __name__ == '__main__':
    for fn in (vamp_manor, museum, lab_tower, witch_hut, wolf_cabin): fn()
