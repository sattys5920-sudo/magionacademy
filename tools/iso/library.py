# 한밤 도서관 (26×20): 물약 교실(본관) 왼쪽 벽 문으로 들어가요. 높은 서가 · 열람 책상 · 아울라의 독서대 · 사서 책상
#   python3 library.py → out/library_bg.png · out/library_obj.png · out/library.json (public/art/iso로 복사하고 world.js MAPS에 넣어요)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade, up, planks, rug, plant_draw, float_candle, chair_draw, ImageDraw
BOOKS = ['#7A2A30', '#2E5A6E', '#7A6A2A', '#4A2E6A', '#2E6A44', '#8A4A2A', '#5A5A6A', '#6A2A4A', '#3A4A7A', '#8A6A3A']

def tall_shelf(R, side, u0, w, h=74):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 0 <= v < h): return None
        if uu < 2 or uu >= w - 2 or v >= h - 3 or v < 1: return hexc('#3A2014')
        row = (v - 1) % 12
        if row in (0, 1): return hexc('#5A3420')
        bi = (uu + (v // 12) * 5) // 3; c = hexc(BOOKS[(bi * 7 + v // 12 * 3) % len(BOOKS)])
        lv = (v - 1) % 12; tall = 6 + (bi * 5 + v // 12) % 4
        if lv < 12 - tall: return hexc('#1E120C')
        if uu % 3 == 0: return shade(c, .7)
        if lv == 12 - tall + 2 and (bi % 3 == 0): return hexc('#E0C070')
        return c
    R.wall_fill(side, f)

def ladder(R, side, u0, h=70):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < 9 and 0 <= v < h): return None
        if uu in (0, 1, 7, 8): return hexc('#8A5A34') if uu in (1, 7) else hexc('#5A3420')
        if v % 8 in (0, 1): return hexc('#A8784A')
        return None
    R.wall_fill(side, f)

def stack(R, tx, ty, w, dp, h=30):   # 서가 한 줄 (앞·옆면에 책등)
    def f(img, d):
        R.box(img, tx, ty, w, dp, h, '#5A3420', '#4A2A18', '#3A2014')
        P = R.P; L, B, Rt = P(tx, ty + dp), P(tx + w, ty + dp), P(tx + w, ty)
        rows = 3; rh = (h - 4) / rows
        for face, (a, b) in (('L', (L, B)), ('R', (B, Rt))):
            n = int(abs(b[0] - a[0]) / 2.2)
            for r in range(rows):
                lift = 2 + r * rh
                for k in range(n):
                    t0, t1 = k / n, (k + .8) / n
                    p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0); p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
                    hh = rh - 2 - ((k * 7 + r * 3) % 3)
                    c = hexc(BOOKS[(k * 3 + r * 5 + tx) % len(BOOKS)]); c = shade(c, .78) if face == 'R' else c
                    d.polygon([tuple(map(int, up(p0, lift))), tuple(map(int, up(p1, lift))), tuple(map(int, up(p1, lift + hh))), tuple(map(int, up(p0, lift + hh)))], fill=c)
                    if (k + r) % 4 == 0: d.line([tuple(map(int, up(p0, lift + hh - 2))), tuple(map(int, up(p1, lift + hh - 2)))], fill=hexc('#E0C070'))
                bl = 2 + r * rh - 1; d.line([tuple(map(int, up(a, bl))), tuple(map(int, up(b, bl)))], fill=hexc('#2A160C'), width=2)
    return f

def reading_table(R, tx, ty):
    def f(img, d):
        R.box(img, tx, ty, 2, 1, 10, '#6A4228', '#4A2E1C', '#3E2616')
        x, y = R.P(tx + 1, ty + .5); y -= 10
        d.polygon([(x - 10, y - 1), (x - 4, y - 4), (x + 1, y - 1), (x - 5, y + 2)], fill=hexc('#F2E6C8')); d.line([(x - 4, y - 4), (x - 5, y + 2)], fill=hexc('#B8A888'))
        d.rectangle([x + 5, y - 9, x + 6, y - 1], fill=hexc('#3A3020')); d.polygon([(x + 1, y - 9), (x + 10, y - 9), (x + 8, y - 13), (x + 3, y - 13)], fill=hexc('#3A8A5A')); d.ellipse([x + 3, y - 2, x + 8, y], fill=hexc('#3A3020'))
        d.rectangle([x - 1, y - 6, x + 2, y - 3], fill=hexc('#7A2A30'))
    return f

def lectern(R, tx, ty):   # 아울라의 독서대 + 횃대
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        d.rectangle([cx - 2, cy - 16, cx + 2, cy], fill=hexc('#5A3420')); d.rectangle([cx - 6, cy - 2, cx + 6, cy], fill=hexc('#3A2014'))
        d.polygon([(cx - 9, cy - 16), (cx + 9, cy - 20), (cx + 9, cy - 16), (cx - 9, cy - 12)], fill=hexc('#6A4228'))
        d.polygon([(cx - 8, cy - 17), (cx, cy - 21), (cx + 1, cy - 18), (cx - 7, cy - 14)], fill=hexc('#F2E6C8')); d.polygon([(cx + 1, cy - 18), (cx + 8, cy - 21), (cx + 8, cy - 18), (cx + 1, cy - 15)], fill=hexc('#E8DCC0'))
        d.rectangle([cx + 12, cy - 30, cx + 13, cy], fill=hexc('#5A3420')); d.rectangle([cx + 7, cy - 31, cx + 18, cy - 29], fill=hexc('#8A5A34'))
        d.ellipse([cx + 9, cy - 2, cx + 16, cy + 1], fill=hexc('#3A2014'))
    return f

def desk(R, tx, ty):   # 사서 책상: 대출 카드 · 도장 · 종
    def f(img, d):
        R.box(img, tx, ty, 3, 1, 12, '#7A4A2A', '#5A3420', '#4A2A18')
        x, y = R.P(tx + .8, ty + .5); y -= 12
        d.rectangle([x - 4, y - 3, x + 3, y], fill=hexc('#E8DCC0')); d.line([(x - 3, y - 2), (x + 2, y - 2)], fill=hexc('#B04A4A'))
        x2, y2 = R.P(tx + 1.8, ty + .5); y2 -= 12
        d.ellipse([x2 - 3, y2 - 5, x2 + 3, y2], fill=hexc('#E0C070')); d.rectangle([x2 - 1, y2 - 7, x2, y2 - 5], fill=hexc('#C8A050'))
        x3, y3 = R.P(tx + 2.6, ty + .5); y3 -= 12
        for k, c in enumerate(['#3A4A7A', '#7A2A30', '#2E6A44']): d.rectangle([x3 - 4, y3 - 2 - k * 2, x3 + 4, y3 - k * 2], fill=hexc(c))
    return f

def globe(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        d.rectangle([cx - 1, cy - 10, cx, cy], fill=hexc('#5A3420')); d.rectangle([cx - 5, cy - 1, cx + 4, cy], fill=hexc('#3A2014'))
        d.ellipse([cx - 8, cy - 26, cx + 7, cy - 11], fill=hexc('#1E2A5A')); d.arc([cx - 10, cy - 28, cx + 9, cy - 9], 200, 340, fill=hexc('#C8A050'), width=2)
        for dx, dy in ((-3, -22), (2, -18), (-4, -16), (3, -23), (0, -14)): d.point((cx + dx, cy + dy), fill=hexc('#FFE9A0'))
        d.line([(cx - 4, cy - 20), (cx - 1, cy - 18), (cx + 3, cy - 21)], fill=hexc('#9AC8F0'))
    return f

def book_pile(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        for k in range(5): c = hexc(BOOKS[(k * 3 + tx) % len(BOOKS)]); d.rectangle([cx - 6 + (k % 2), cy - 3 - k * 3, cx + 5 - (k % 2), cy - k * 3], fill=c); d.line([(cx - 6 + (k % 2), cy - 3 - k * 3), (cx + 5 - (k % 2), cy - 3 - k * 3)], fill=shade(c, 1.3))
    return f

def library_room():
    R = Room(26, 20, wall=84)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    R.floor(rug(planks(['#5A3A26', '#4E321F', '#62402A', '#563622'], '#2E1C12'), 11, 2, 15, 19, '#2A3A6A', '#C8A050', inner='#3A4E8A'))
    R.walls('#1E2448', '#262E5A', '#3A2216', trim='#C8A050')
    tall_shelf(R, 'R', 4, 40); R.window('R', 52, w=18, v0=30, h=40); tall_shelf(R, 'R', 78, 40); ladder(R, 'R', 96); R.window('R', 128, w=18, v0=30, h=40); tall_shelf(R, 'R', 154, 44)
    tall_shelf(R, 'L', 4, 36); R.window('L', 50, w=18, v0=30, h=40); tall_shelf(R, 'L', 76, 36); ladder(R, 'L', 82); tall_shelf(R, 'L', 118, 38)
    for side, u in (('R', 46), ('R', 122), ('R', 202), ('L', 44), ('L', 72), ('L', 114)): R.sconce(side, u)
    for (x, y) in ((3, 5), (3, 9), (17, 5), (17, 9)): R.obj('stack', [(x + k, y) for k in range(6)], stack(R, x, y, 6, 1, 30), act=('서가', '책 구경하기'))
    R.obj('lectern', [(12, 2), (13, 2)], lectern(R, 12, 2), act=('아울라의 독서대', '구경하기')); R.light(12.5, 2.5, -18, 34, [255, 200, 120], .55)
    for (x, y) in ((8, 13), (16, 13)):
        R.obj('table', [(x, y), (x + 1, y)], reading_table(R, x, y), act=('열람 책상', '앉아서 읽기')); R.light(x + 1.5, y, -16, 22, [140, 230, 160], .45)
        R.obj('chair', [(x, y + 1)], chair_draw(R, x, y + 1, '#2A3A6A')); R.obj('chair', [(x + 1, y + 1)], chair_draw(R, x + 1, y + 1, '#2A3A6A'))
    R.obj('desk', [(20, 16), (21, 16), (22, 16)], desk(R, 20, 16), act=('사서 책상', '대출 카드 보기'))
    R.obj('globe', [(23, 13)], globe(R, 23, 13), act=('별 지구본', '돌려 보기'))
    for (x, y) in ((1, 14), (2, 16), (24, 3), (9, 2)): R.obj('books', [(x, y)], book_pile(R, x, y))
    for (x, y) in ((0, 19), (25, 19), (0, 2)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#2E5A44', '#9A7AE8'))
    for (x, y) in ((6, 7), (20, 7), (12, 6), (6, 12), (20, 12), (12, 10), (4, 16), (22, 11)): float_candle(R, x, y)
    R.extra = dict(night=True)
    R.save('library', '한밤 도서관', '밤에 더 반짝이는 서가 · 물약 교실 문으로 나가요', [1, 14])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True); library_room()
