# 그림자 골목 집 안 다섯 곳 (뱀파이어 저택 · 학교 박물관 · 낡은 연구 탑 · 마녀 오두막 · 늑대인간 통나무집)
#   python3 quarter_rooms.py → out/vamp_manor·museum·lab_tower·witch_hut·wolf_cabin (_bg.png _obj.png .json)
#   의뢰인이 사는 집이에요: 이야기가 꽤 진행되면(그 사람의 의뢰 3단계부터) 들어갈 수 있고, 안에서 의뢰인을 만나요 (index.html QHOME · World.canEnter)
import json, math, random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade, up, checker, planks, rug, table_draw, chair_draw, plant_draw, float_candle, bookshelf, cauldron_draw, crates, chalkboard
random.seed(404)
NX, NY = 22, 16
def common(R, floor, paper, paper2, wain, trim):
    R.floor(floor); R.walls(paper, paper2, wain, trim=trim)
    R.extra = dict(vw=200)
def wall_frame(R, side, u0, w, h, v0, border, inner, fn=None):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h): return None
        if uu < 2 or uu >= w - 2 or vv < 2 or vv >= h - 2: return hexc(border)
        return fn(uu, vv) if fn else hexc(inner)
    R.wall_fill(side, f)
def portrait(R, side, u0, face='#C8B8A8', hair='#2A1A22', bg='#2E1E30'):
    def fn(uu, vv):
        if (uu - 8) ** 2 / 20 + (vv - 17) ** 2 / 34 < 1: return hexc(face)
        if (uu - 8) ** 2 / 34 + (vv - 17) ** 2 / 60 < 1 and vv > 16: return hexc(hair)
        if vv < 8: return shade(hexc(bg), 1.3)
        return hexc(bg)
    wall_frame(R, side, u0, 17, 28, 30, '#C49446', bg, fn)
def tiles(x, y, w, d): return [(a, b) for a in range(x, x + w) for b in range(y, y + d)]
def fireplace(R, side, u0, w=40, h=46):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 0 <= v < h): return None
        if uu < 5 or uu >= w - 5 or v >= h - 5: return hexc('#6A6270') if (uu + v // 4) % 5 else hexc('#524A5A')
        if v < 3: return hexc('#2A2030')
        fl = (math.sin(uu * .6) + 1) * 6
        if v < 16 + fl and 6 < uu < w - 6: return hexc('#FF8A2A') if (uu * 3 + v) % 4 else hexc('#FFC84A')
        return hexc('#1A1018')
    R.wall_fill(side, f)
    x, y = R.wall_px(side, u0 + w / 2, 12); R.lights.append(dict(p=(x, y), dy=0, r=46, c=[255, 150, 70], a=.65, f=1))
def glass_case(R, tx, ty, w, inner):
    def f(img, d):
        R.box(img, tx, ty, w, .9, 9, '#5A4A38', '#3E3024', '#4A3A2C'); R.box(img, tx + .05, ty + .05, w - .1, .8, 12, (200, 230, 255, 120), (190, 220, 250, 110), (190, 220, 250, 110), lift=9)
        for k in range(int(w)):
            x, y = R.P(tx + .5 + k, ty + .5); inner(d, x, y - 12, k)
    return f
def finish(R, key, title, sub, back):
    R.exit_label = '그림자 골목'; R.exit_to = 'quarter'; R.save(key, title, sub, back)
# ============ 1. 뱀파이어 저택 (블라디) ============
def vamp_manor():
    R = Room(NX, NY)
    common(R, rug(checker('#2A2230', '#3A2E40'), 6.5, 4.5, 15.5, 14.5, '#6A1E2E', border='#C49446', inner='#8A2A3E'), '#4A1E2A', '#5E2A38', '#241A22', '#C49446')
    for u in (22, 62, 112, 150): R.window('R', u, 16, 28, 36, glass=('#241848', '#4A3A8A', '#8A7AE0'))
    for u in (30, 94): R.window('L', u, 16, 28, 36, glass=('#241848', '#4A3A8A', '#8A7AE0'))
    portrait(R, 'R', 44, '#D8C8B8', '#1A1018'); portrait(R, 'R', 84, '#C8B098', '#6A2A22'); portrait(R, 'R', 128, '#B8B0C8', '#2A2A3A'); portrait(R, 'L', 58, '#D0C0B0', '#3A2A2A')
    for side, u in (('R', 38), ('R', 78), ('R', 124), ('R', 164), ('L', 16), ('L', 50), ('L', 80), ('L', 112)): R.sconce(side, u)
    bookshelf(R, 'L', 100, 24)
    for x in range(8, 14): R.obj('table', [(x, 8)], table_draw(R, x, 8, '#3A1E1E', (('cup',), ('book',), ('cup', 'cake'), ('pumpkin',))[x % 4]), act=('긴 식탁', '살펴보기'))
    for x in range(8, 14): R.obj('chair', [(x, 7)], chair_draw(R, x, 7, '#6A1E2E')); R.obj('chair', [(x, 9)], chair_draw(R, x, 9, '#6A1E2E'))
    R.obj('chair', [(7, 8)], chair_draw(R, 7, 8, '#8A2A3E')); R.obj('chair', [(14, 8)], chair_draw(R, 14, 8, '#8A2A3E'))
    for (x, y) in ((5, 5), (16, 5), (3, 10), (18, 10), (9, 4), (12, 4), (6, 13), (15, 13)): float_candle(R, x, y)
    def coffin(img, d):
        R.box(img, 1, 11, 3, 1.6, 8, '#2A1A1E', '#3A2228', '#4A2A32'); R.box(img, 1.1, 11.1, 2.8, 1.4, 11, '#4A2A32', '#3A2228', '#4A2A32')
        x, y = R.P(2.5, 11.9); d.line([(x - 8, y - 14), (x + 8, y - 10)], fill=hexc('#C49446'), width=1)
    R.obj('coffin', tiles(1, 11, 3, 2), coffin, act=('낡은 관', '들여다보기'))
    def organ(img, d):
        R.box(img, 17, 2, 3, 1.2, 14, '#2A1E24', '#1E161C', '#2E2228'); R.box(img, 17.1, 3.2, 2.8, .5, 8, '#E8E0D0', '#1E161C', '#C8C0B0', lift=6)
        for k in range(6): x, y = R.P(17.4 + k * .45, 3.4); d.line([(x, y - 11), (x, y - 7)], fill=hexc('#1A1018'))
    R.obj('organ', tiles(17, 2, 3, 2), organ, act=('낡은 오르간', '건반 눌러 보기'))
    def clock(img, d):
        R.box(img, 1, 2, 1, 1, 46, '#4A2E1E', '#3A2216', '#5A3826'); x, y = R.P(1.5, 2.5)
        d.ellipse([x - 5, y - 40, x + 5, y - 30], fill=hexc('#E8DCC0')); d.line([(x, y - 35), (x, y - 39)], fill=hexc('#2A1A12')); d.line([(x, y - 35), (x + 3, y - 34)], fill=hexc('#2A1A12'))
    R.obj('clock', [(1, 2)], clock, act=('멈춘 시계', '들여다보기'))
    for (x, y) in ((1, 14), (20, 14), (20, 7)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4A3A4A', '#C83A4A'))
    R.light(11, 8, -40, 120, [255, 180, 120], .25, 1)
    finish(R, 'vamp_manor', '뱀파이어 저택', '블라디의 집 · 촛불이 둥둥 떠다녀요', [12, 14])
# ============ 2. 학교 박물관 (네페르) ============
def museum():
    R = Room(NX, NY)
    common(R, rug(checker('#D8CCB0', '#B8AC90'), 7.5, 5, 14.5, 14, '#8A3A2E', border='#C49446', inner='#B8864E'), '#C8B286', '#B8A276', '#6A5438', '#C49446')
    for u in (24, 70, 118, 160): R.window('R', u, 16, 28, 36, glass=('#4A5A8A', '#7A8AC0', '#C0D0F0'))
    R.window('L', 30, 16, 28, 36, glass=('#4A5A8A', '#7A8AC0', '#C0D0F0'))
    def glyph(uu, vv):
        if (uu // 6 + vv // 6) % 3 == 0 and uu % 6 in (1, 2, 3) and vv % 6 in (2, 3): return hexc('#2E5A8A')
        if (uu // 6 + vv // 8) % 4 == 1 and uu % 6 in (2, 3) and vv % 8 in (2, 4, 5): return hexc('#8A2A22')
        return hexc('#D8C494')
    wall_frame(R, 'R', 44, 62, 36, 30, '#8A7448', '#D8C494', glyph); wall_frame(R, 'R', 122, 36, 36, 30, '#8A7448', '#D8C494', glyph)
    for side, u in (('R', 38), ('R', 110), ('R', 164), ('L', 16), ('L', 80), ('L', 112)): R.sconce(side, u)
    R.shelf('L', 96, 24, 56, ['#8A7448', '#B8A276', '#6A5438', '#C8B286'])
    def sarc(img, d):
        R.box(img, 9, 6, 3, 1.5, 9, '#7A5A2A', '#5A4020', '#6A4A26'); R.box(img, 9.1, 6.1, 2.8, 1.3, 14, '#E0B84A', '#B8902E', '#C8A03A')
        x, y = R.P(10.5, 6.8); d.ellipse([x - 8, y - 22, x - 2, y - 14], fill=hexc('#E8C85A')); d.line([(x - 5, y - 14), (x + 8, y - 11)], fill=hexc('#2E5A8A'))
    R.obj('sarcophagus', tiles(9, 6, 3, 2), sarc, act=('금빛 석관', '들여다보기'))
    inner_a = lambda d, x, y, k: d.ellipse([x - 3, y - 4, x + 3, y], fill=hexc(['#C84A2E', '#2E8A8A', '#E0B84A'][k % 3]))
    def inner_b(d, x, y, k): d.rectangle([x - 3, y - 4, x + 3, y], fill=hexc('#B8A276')); d.line([(x - 3, y - 2), (x + 3, y - 2)], fill=hexc('#6A5438'))
    R.obj('case', tiles(2, 2, 4, 1), glass_case(R, 2, 2, 4, inner_a), act=('유리 진열장', '구경하기')); R.obj('case', tiles(16, 2, 4, 1), glass_case(R, 16, 2, 4, inner_b), act=('유리 진열장', '구경하기'))
    R.obj('case', tiles(2, 13, 4, 1), glass_case(R, 2, 13, 4, inner_b), act=('유리 진열장', '구경하기')); R.obj('case', tiles(16, 13, 4, 1), glass_case(R, 16, 13, 4, inner_a), act=('유리 진열장', '구경하기'))
    def statue(tx, ty, col):
        def f(img, d):
            R.box(img, tx + .1, ty + .1, .8, .8, 7, '#8A7448', '#6A5438', '#7A6440'); x, y = R.P(tx + .5, ty + .5)
            d.rectangle([x - 4, y - 24, x + 4, y - 8], fill=hexc(col)); d.rectangle([x - 4, y - 24, x, y - 8], fill=shade(hexc(col), .85)); d.ellipse([x - 4, y - 32, x + 4, y - 24], fill=hexc(col))
            d.polygon([(x - 5, y - 30), (x, y - 36), (x + 5, y - 30)], fill=hexc('#2E5A8A'))
        return f
    for (x, y) in ((6, 5), (15, 5), (6, 11), (15, 11)): R.obj('statue', [(x, y)], statue(x, y, '#C8B898'), act=('고대 조각상', '올려다보기'))
    def pedestal(tx, ty):
        def f(img, d):
            R.box(img, tx + .15, ty + .15, .7, .7, 8, '#E8E0D0', '#B8B0A0', '#C8C0B0'); x, y = R.P(tx + .5, ty + .5)
            d.polygon([(x - 3, y - 10), (x + 3, y - 10), (x + 4, y - 15), (x + 1, y - 18), (x - 1, y - 18), (x - 4, y - 15)], fill=hexc('#B85A3A')); d.line([(x - 3, y - 13), (x + 3, y - 13)], fill=hexc('#E8C85A'))
        return f
    for (x, y) in ((12, 11), (9, 11), (18, 8), (3, 8)): R.obj('vase', [(x, y)], pedestal(x, y), act=('유물 받침대', '살펴보기'))
    for (x, y) in ((1, 14), (20, 14)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#6A8A4A', '#E0B84A'))
    for (x, y) in ((5, 8), (17, 5), (12, 4), (10, 14)): float_candle(R, x, y)
    R.light(11, 8, -30, 110, [255, 230, 170], .22, 0)
    finish(R, 'museum', '학교 박물관', '네페르가 지키는 유물 방', [31, 14])
# ============ 3. 낡은 연구 탑 (피스) ============
def lab_tower():
    R = Room(NX, NY)
    common(R, checker('#3A3C4A', '#2E303E', 1), '#2E3E44', '#3A4E54', '#20242C', '#8A9AAA')
    for u in (24, 64, 112, 152): R.window('R', u, 16, 26, 40, glass=('#1E2A3E', '#3A5A7A', '#B8E8FF'))
    R.window('L', 36, 16, 26, 40, glass=('#1E2A3E', '#3A5A7A', '#B8E8FF'))
    chalkboard(R, 40, 40, 'R'); chalkboard(R, 112, 34, 'R')
    for side, u in (('R', 36), ('R', 100), ('R', 164), ('L', 16), ('L', 70), ('L', 112)): R.sconce(side, u)
    def coil(tx, ty):
        def f(img, d):
            R.box(img, tx + .1, ty + .1, .8, .8, 6, '#5A5A6A', '#3A3A4A', '#4A4A5A'); x, y = R.P(tx + .5, ty + .5)
            d.rectangle([x - 2, y - 40, x + 2, y - 6], fill=hexc('#8A8A9A')); d.ellipse([x - 6, y - 52, x + 6, y - 40], fill=hexc('#C8E8FF')); d.ellipse([x - 3, y - 49, x + 3, y - 43], fill=hexc('#FFFFFF'))
            for k in range(3): d.line([(x - 5, y - 36 + k * 8), (x + 5, y - 34 + k * 8)], fill=hexc('#E0A83A'))
        return f
    for (x, y) in ((3, 4), (18, 4)): R.obj('coil', [(x, y)], coil(x, y), act=('번개 코일', '쳐다보기')); R.light(x + .5, y + .5, -46, 36, [150, 220, 255], .6, 1)
    def slab(img, d):
        R.box(img, 9, 6, 3, 1.6, 9, '#8A9AAA', '#5A6270', '#6A7280'); R.box(img, 9.1, 6.1, 2.8, 1.4, 12, '#D8E4EC', '#8A9AAA', '#A8B6C2')
        x, y = R.P(10.5, 6.8); d.line([(x - 7, y - 14), (x + 7, y - 10)], fill=hexc('#8A5A3A'))
    R.obj('slab', tiles(9, 6, 3, 2), slab, act=('수술대', '살펴보기'))
    def bench(tx, ty, w):
        def f(img, d):
            R.box(img, tx, ty, w, 1, 11, '#6A6A78', '#3E3E4A', '#4E4E5A')
            for k in range(int(w)):
                x, y = R.P(tx + .5 + k, ty + .5); c = ['#6AE88A', '#FF6A8A', '#6AB8FF', '#E0C84A'][(k + int(tx)) % 4]
                d.rectangle([x - 2, y - 17, x + 2, y - 12], fill=hexc(c)); d.rectangle([x - 1, y - 20, x + 1, y - 17], fill=hexc('#C8D8E0'))
        return f
    for (x, y, w) in ((2, 9, 4), (16, 9, 4), (7, 12, 3), (12, 12, 3)): R.obj('bench', tiles(x, y, w, 1), bench(x, y, w), act=('실험대', '살펴보기'))
    def generator(img, d):
        R.box(img, 19, 12, 2, 1.4, 16, '#4E5A62', '#323A42', '#3E4850'); x, y = R.P(20, 12.7)
        d.ellipse([x - 5, y - 22, x + 5, y - 14], fill=hexc('#E0C84A')); d.line([(x, y - 18), (x + 3, y - 20)], fill=hexc('#2A2A2A'))
    R.obj('generator', tiles(19, 12, 2, 2), generator, act=('낡은 발전기', '살펴보기'))
    for (x, y) in ((1, 5), (20, 7), (1, 14)): R.obj('crate', [(x, y)], crates(R, x, y, 2))
    for (x, y) in ((6, 4), (15, 4), (11, 10), (5, 14)): float_candle(R, x, y)
    R.light(11, 7, -20, 120, [150, 200, 255], .25, 1)
    finish(R, 'lab_tower', '낡은 연구 탑', '피스의 작업실 · 번개 맞은 흔적', [44, 14])
# ============ 4. 마녀 오두막 (베아트릭스) ============
def witch_hut():
    R = Room(NX, NY)
    common(R, rug(planks(['#6A4A32', '#5E4128', '#745338']), 7, 5, 15, 13, '#5A3A8A', border='#C49446', inner='#7A5ABA'), '#3A2E4A', '#4A3E5E', '#3A2418', '#B88A4A')
    for u in (30, 100): R.window('R', u, 16, 28, 36, glass=('#241848', '#4A3A8A', '#8A7AE0'))
    R.window('L', 54, 16, 28, 36, glass=('#241848', '#4A3A8A', '#8A7AE0'))
    R.shelf('R', 56, 26, 58, ['#6AE88A', '#C86AE8', '#E8C84A', '#6AB8FF', '#FF6A8A']); R.shelf('R', 134, 26, 58, ['#6AE88A', '#C86AE8', '#E8C84A', '#6AB8FF', '#FF6A8A'])
    def herbs(u0):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < 12 and 40 <= v < 66): return None
            if v >= 62 and uu in (5, 6): return hexc('#8A6A3A')
            if v < 62 and (uu - 6) ** 2 / 25 + ((v - 50) / 11) ** 2 < 1: return hexc(['#4E8A4E', '#6AAA5A', '#8A5ABA'][(uu + v) % 3])
            return None
        R.wall_fill('R', f)
    for u in (24, 92, 118, 170): herbs(u)
    for side, u in (('R', 50), ('R', 124), ('L', 20), ('L', 90)): R.sconce(side, u)
    R.obj('cauldron', [(5, 4), (6, 4)], cauldron_draw(R, 5, 4, '#6AE88A', 1.7), act=('커다란 마녀의 솥', '들여다보기')); R.light(5.5, 4.5, -12, 46, [120, 255, 150], .6, 1)
    def bed(img, d):
        R.box(img, 17, 11, 3, 2, 8, '#5A3A8A', '#4A2E70', '#5A3A8A'); R.box(img, 17.1, 11.1, 2.8, .8, 12, '#E8E0F0', '#8A7AA8', '#A89AC0')
    R.obj('bed', tiles(17, 11, 3, 2), bed, act=('마녀의 침대', '살펴보기'))
    def ball(img, d):
        R.box(img, 11, 7, 1, 1, 9, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(11.5, 7.5)
        d.ellipse([x - 5, y - 20, x + 5, y - 10], fill=hexc('#B8A8F0')); d.ellipse([x - 3, y - 18, x + 1, y - 14], fill=hexc('#F0E8FF'))
    R.obj('crystal', [(11, 7)], ball, act=('수정 구슬', '들여다보기')); R.light(11.5, 7.5, -16, 40, [190, 170, 255], .5, 1)
    def book(img, d):
        R.box(img, 14, 3, 1, 1, 12, '#3E2616', '#2A1A10', '#3A2216'); x, y = R.P(14.5, 3.5)
        d.polygon([(x - 6, y - 16), (x, y - 20), (x + 6, y - 16), (x, y - 12)], fill=hexc('#7A2A5A')); d.line([(x, y - 20), (x, y - 12)], fill=hexc('#E0C84A'))
    R.obj('spellbook', [(14, 3)], book, act=('낡은 마법서', '펼쳐 보기'))
    def broom(img, d):
        x, y = R.P(2.5, 12.5); d.line([(x - 6, y - 24), (x + 4, y - 2)], fill=hexc('#8A6A3A'), width=2); d.polygon([(x + 2, y - 5), (x + 9, y - 2), (x + 4, y + 3), (x - 1, y)], fill=hexc('#C8A04A'))
    R.obj('broom', [(2, 12)], broom, act=('기대어 둔 빗자루', '살펴보기'))
    R.obj('table', [(9, 11)], table_draw(R, 9, 11, '#5A3A22', ('cup', 'book')), act=('작은 탁자', '살펴보기')); R.obj('chair', [(8, 11)], chair_draw(R, 8, 11, '#5A3A8A')); R.obj('chair', [(10, 11)], chair_draw(R, 10, 11, '#5A3A8A'))
    R.obj('crate', [(19, 4)], crates(R, 19, 4, 2)); R.obj('crate', [(20, 5)], crates(R, 20, 5, 1))
    for (x, y) in ((1, 2), (20, 14), (1, 8)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E8A4E', '#C86AE8'))
    for (x, y) in ((8, 3), (16, 8), (4, 9), (12, 14), (18, 3)): float_candle(R, x, y)
    R.light(11, 8, -30, 110, [190, 160, 255], .2, 0)
    finish(R, 'witch_hut', '마녀 오두막', '베아트릭스의 집 · 솥이 부글부글', [9, 30])
# ============ 5. 늑대인간 통나무집 (우르) ============
def wolf_cabin():
    R = Room(NX, NY)
    common(R, rug(planks(['#7A5232', '#6A4428', '#865C3A']), 7.5, 5.5, 14.5, 12.5, '#5A3220', border='#3A2216', inner='#4A2A1A'), '#7A5232', '#6A4428', '#4A2E1A', '#3A2216')
    R.window('R', 26, 16, 26, 34, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0')); R.window('R', 140, 16, 26, 34, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0')); R.window('L', 60, 16, 26, 34, glass=('#1E2A4E', '#3A5A8A', '#B8D0F0'))
    fireplace(R, 'R', 70, 50)
    def antlers(u0):
        def f(u, v):
            uu = u - u0
            if not (0 <= uu < 30 and 40 <= v < 66): return None
            c = hexc('#E8DCC0')
            if abs(uu - 15) <= 1 and v < 52: return c
            if v < 62 and abs(uu - 15) in (v - 40 + 2, v - 40 + 3) and 3 < uu < 27: return c
            if 52 <= v < 54 and abs(uu - 15) < 10: return c
            return None
        R.wall_fill('R', f)
    antlers(24); antlers(136)
    for side, u in (('R', 54), ('R', 128), ('L', 20), ('L', 100)): R.sconce(side, u)
    def bunk(img, d):
        R.box(img, 18, 2, 3, 2, 8, '#5A3A22', '#3E2616', '#4A2E1C'); R.box(img, 18.1, 2.1, 2.8, 1.8, 11, '#8A4A3A', '#6A3228', '#7A3E30'); R.box(img, 18.1, 2.1, 2.8, 1.8, 11, '#8A4A3A', '#6A3228', '#7A3E30', lift=14)
    R.obj('bunk', tiles(18, 2, 3, 2), bunk, act=('이층 침상', '살펴보기'))
    def bearrug(img, d):
        x, y = R.P(11, 8.5); d.ellipse([x - 22, y - 8, x + 22, y + 8], fill=hexc('#3E2A22')); d.ellipse([x - 20, y - 7, x + 20, y + 6], fill=hexc('#5A3E30')); d.ellipse([x - 28, y - 8, x - 20, y - 2], fill=hexc('#5A3E30'))
    R.obj('bearrug', [(10, 8)], bearrug, solid=False)
    def rack(img, d):
        R.box(img, 2, 5, 1, 2, 6, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(2.5, 6)
        d.line([(x - 4, y - 8), (x + 4, y - 24)], fill=hexc('#8A8A92'), width=1); d.arc([x - 4, y - 28, x + 8, y - 6], 100, 260, fill=hexc('#A8824E'), width=2); d.line([(x + 6, y - 10), (x + 10, y - 22)], fill=hexc('#6A4428'), width=2)
    R.obj('rack', tiles(2, 5, 1, 2), rack, act=('사냥 도구 걸이', '살펴보기'))
    def wood(img, d):
        for k in range(3): R.box(img, 1 + k * .05, 12, .9, 1, 5, '#8A6A3E', '#5A3E24', '#6A4A2E', lift=k * 5)
    R.obj('woodpile', tiles(1, 12, 1, 1), wood, act=('장작더미', '살펴보기'))
    def pot(img, d):
        R.box(img, 3, 3, 1.2, 1.2, 8, '#5A3A22', '#3E2616', '#4A2E1C'); x, y = R.P(3.6, 3.6); d.ellipse([x - 7, y - 20, x + 7, y - 10], fill=hexc('#4A4A52')); d.ellipse([x - 5, y - 19, x + 5, y - 13], fill=hexc('#C8864A'))
    R.obj('pot', tiles(3, 3, 1, 1), pot, act=('스튜 냄비', '냄새 맡기')); R.light(3.6, 3.6, -14, 26, [255, 170, 80], .4, 1)
    R.obj('table', [(12, 11)], table_draw(R, 12, 11, '#6A4428', ('cup', 'cake')), act=('통나무 식탁', '살펴보기')); R.obj('chair', [(11, 11)], chair_draw(R, 11, 11, '#8A4A2E')); R.obj('chair', [(13, 11)], chair_draw(R, 13, 11, '#8A4A2E'))
    R.obj('crate', [(20, 8)], crates(R, 20, 8, 2)); R.obj('crate', [(20, 14)], crates(R, 20, 14, 1))
    for (x, y) in ((1, 2), (20, 12)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E7A3E', '#E8A050'))
    for (x, y) in ((6, 9), (16, 7), (10, 14), (8, 3)): float_candle(R, x, y)
    R.light(11, 8, -30, 110, [255, 180, 110], .22, 0)
    finish(R, 'wolf_cabin', '늑대인간 통나무집', '우르의 집 · 벽난로가 따뜻해요', [28, 30])
if __name__ == '__main__':
    for fn in (vamp_manor, museum, lab_tower, witch_hut, wolf_cabin): fn()
