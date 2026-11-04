# 선배 학년 방 두 곳 (시안)
#   3학년 휴게실 lounge3 (22×18): 보라·호박빛 아늑한 휴게실. 벽난로 · 큰 소파 · 선배의 책장 · 3학년 게시판 · 3학년 깃발
#   시계탑 옥상 관측실 observatory (22×18): 4학년의 밤 옥상. 탑의 큰 시계판 · 놋쇠 망원경 · 날씨 점 수정구 · 마법 연구대 · 마을이 보이는 난간
#   python3 senior_rooms.py → out/lounge3_bg.png·_obj.png·.json, out/observatory_bg.png·_obj.png·.json (아직 게임에 안 넣었어요: public/art/iso로 복사하고 world.js MAPS에 넣어요)
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade, up, planks, rug, plant_draw, float_candle, chair_draw, ImageDraw
from library import stack, book_pile, BOOKS

def tiles(x, y, w, d): return [(a, b) for a in range(x, x + w) for b in range(y, y + d)]
def hsh(*a):   # 작은 정수 해시 (무늬가 늘 같게)
    h = 2166136261
    for v in a: h = ((h ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h

def wall_sprite(R, side, u0, u1, v0, v1, fn):   # 벽에 붙은 물건을 물건 그림(obj)으로: 눌러서 쓸 수 있게
    def f(img, d):
        px = img.load(); W, H = img.size
        for u in range(u0, u1):
            for v in range(v0, v1):
                c = fn(u - u0, v - v0)
                if c:
                    x, y = R.wall_px(side, u, v)
                    if 0 <= int(x) < W and 0 <= int(y) < H: px[int(x), int(y)] = c
    return f

def fireplace(R, side, u0, w=44, h=50, stone=('#6A5A6E', '#54465A'), fire=('#FF9A3A', '#FFD27A')):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w + 8 and 0 <= v < h + 6): return None
        if v >= h:   # 벽난로 선반 (조금 더 넓게)
            if v >= h + 4: return None
            return hexc('#8A5A34') if v < h + 3 else hexc('#B07A48')
        if uu < 4 or uu >= w + 4: return None
        uu -= 4
        if uu < 5 or uu >= w - 5 or v >= h - 6: return hexc(stone[0]) if (uu // 6 + v // 5) % 3 else hexc(stone[1])
        if v < 3: return hexc('#2A1E26')
        top = h - 6 - 6
        if v > top and (uu - w / 2) ** 2 + (v - top) ** 2 > (w / 2 - 6) ** 2: return hexc(stone[0])
        fl = (math.sin(uu * .55) + 1) * 5 + (uu * 7 % 3)
        if v < 4 + 2: return hexc('#5A2A1A') if uu % 5 else hexc('#3A1A12')   # 장작
        if v < 12 + fl and 7 < uu < w - 7: return hexc(fire[1]) if (v < 8 + fl * .5 and 12 < uu < w - 12) else hexc(fire[0])
        return hexc('#1A1018')
    R.wall_fill(side, f)
    x, y = R.wall_px(side, u0 + 4 + w / 2, 12); R.lights.append(dict(p=(x, y), dy=0, r=56, c=[255, 160, 80], a=.7, f=1))

# ======================= 3학년 휴게실 =======================
def senior_shelf(R, tx, ty, w):   # 선배의 책장: 키 큰 책장 + 위에 트로피·화분
    base = stack(R, tx, ty, w, 1, 46)
    def f(img, d):
        base(img, d)
        for k in range(w):
            x, y = R.P(tx + k + .5, ty + .5); y -= 46
            it = k % 3
            if it == 0:   # 트로피
                d.polygon([(x - 4, y - 9), (x + 4, y - 9), (x + 2, y - 4), (x - 2, y - 4)], fill=hexc('#E0B050')); d.rectangle([x - 1, y - 4, x, y - 2], fill=hexc('#C08A30')); d.rectangle([x - 3, y - 2, x + 2, y], fill=hexc('#7A4A2A'))
                d.point((x - 2, y - 8), fill=hexc('#FFF0B0'))
            elif it == 1:   # 눕힌 책
                for j, c in enumerate(('#6A2A4A', '#3A4A7A', '#7A6A2A')): d.rectangle([x - 5 + j, y - 2 - j * 2, x + 4 - j, y - j * 2], fill=hexc(c))
            else:   # 작은 유리병
                d.rectangle([x - 2, y - 7, x + 1, y], fill=hexc('#C08AFF')); d.rectangle([x - 1, y - 9, x, y - 7], fill=hexc('#C8B8A0'))
    return f

def big_sofa(R, tx, ty, w, col='#6A3A8A', pil=('#E0A040', '#C86A9A', '#F2D890')):   # 벽을 등진 큰 소파 (앞을 봐요)
    c = hexc(col)
    def f(img, d):
        R.box(img, tx + .05, ty + .1, w - .1, .9, 8, shade(c, 1.05), shade(c, .62), shade(c, .78))   # 앉는 곳
        R.box(img, tx + .05, ty + .05, w - .1, .35, 22, shade(c, .92), shade(c, .58), shade(c, .72))  # 등받이
        for k in range(w):   # 방석 줄
            a, b = R.P(tx + k + .1, ty + .95), R.P(tx + k + .1, ty + .4); d.line([tuple(map(int, up(a, 8))), tuple(map(int, up(b, 8)))], fill=shade(c, .75))
            a, b = R.P(tx + k + .1, ty + .4), R.P(tx + k + .1, ty + .1); d.line([tuple(map(int, up(a, 21))), tuple(map(int, up(a, 9)))], fill=shade(c, .7))
        a, b = R.P(tx + .05, ty + .05), R.P(tx + w - .05, ty + .05); d.line([tuple(map(int, up(a, 22))), tuple(map(int, up(b, 22)))], fill=hexc('#E0A040'))   # 금색 테두리
        a, b = R.P(tx + .05, ty + .4), R.P(tx + w - .05, ty + .4); d.line([tuple(map(int, up(a, 22))), tuple(map(int, up(b, 22)))], fill=hexc('#E0A040'))
        for xx in (-.12, w - .2):   # 팔걸이
            R.box(img, tx + xx, ty + .05, .32, .95, 14, shade(c, 1.15), shade(c, .6), shade(c, .76))
        for k, (px_, col2) in enumerate(((.55, pil[0]), (w / 2, pil[1]), (w - .55, pil[2]))):   # 쿠션
            x, y = R.P(tx + px_, ty + .5); y -= 9
            d.polygon([(x - 4, y - 8), (x + 3, y - 10), (x + 4, y - 4), (x - 3, y - 2)], fill=hexc(col2)); d.line([(x - 3, y - 7), (x + 2, y - 9)], fill=shade(hexc(col2), 1.2))
        x, y = R.P(tx + w - 1.1, ty + .9); y -= 8   # 걸쳐 둔 담요
        d.polygon([(x - 1, y - 3), (x + 6, y - 6), (x + 7, y + 4), (x, y + 7)], fill=hexc('#E8C878')); d.line([(x, y + 1), (x + 6, y - 2)], fill=hexc('#B07A3A')); d.line([(x, y + 4), (x + 7, y + 1)], fill=hexc('#B07A3A'))
    return f

def tea_table(R, tx, ty, w=2.2):
    def f(img, d):
        for a, b in ((.15, .12), (w - .2, .12), (.15, .55), (w - .2, .55)): R.box(img, tx + a, ty + b, .08, .08, 7, '#3A2014', '#3A2014', '#2A160C')
        R.box(img, tx, ty, w, .7, 2, '#8A5A34', '#5A3420', '#4A2A18', lift=7)
        x, y = R.P(tx + w / 2, ty + .35); y -= 9
        d.ellipse([x - 5, y - 8, x + 5, y], fill=hexc('#E8DCC8')); d.ellipse([x - 3, y - 10, x + 3, y - 7], fill=hexc('#C8B8A0')); d.line([(x + 5, y - 6), (x + 9, y - 9)], fill=hexc('#E8DCC8'), width=2)   # 찻주전자
        d.arc([x - 9, y - 7, x - 4, y - 2], 90, 270, fill=hexc('#E8DCC8'))
        for dx, cc in ((-12, '#C86A9A'), (12, '#7AB8E8')):   # 찻잔 + 받침
            d.ellipse([x + dx - 4, y - 1, x + dx + 4, y + 2], fill=hexc('#F2E8D8')); d.rectangle([x + dx - 2, y - 5, x + dx + 2, y], fill=hexc(cc)); d.rectangle([x + dx - 1, y - 5, x + dx + 1, y - 4], fill=hexc('#7A4A2A'))
        d.ellipse([x + 3, y + 1, x + 11, y + 4], fill=hexc('#F2E8D8'))   # 과자 접시
        for dx in (5, 8): d.ellipse([x + dx - 1, y, x + dx + 2, y + 2], fill=hexc('#D89A4A'))
    return f

def armchair(R, tx, ty, col='#8A4A2A', back='far'):
    c = hexc(col)
    def f(img, d):
        R.box(img, tx + .1, ty + .1, .8, .8, 7, shade(c, 1.05), shade(c, .62), shade(c, .78))
        if back == 'far': R.box(img, tx + .1, ty + .1, .8, .25, 18, shade(c, .9), shade(c, .58), shade(c, .72))
        else: R.box(img, tx + .1, ty + .1, .25, .8, 18, shade(c, .9), shade(c, .58), shade(c, .72))
        for a, b, ww, dd in ((( .05, .1, .2, .8), (.75, .1, .2, .8)) if back == 'far' else ((.1, .05, .8, .2), (.1, .75, .8, .2))):
            R.box(img, tx + a, ty + b, ww, dd, 11, shade(c, 1.15), shade(c, .6), shade(c, .76))
    return f

def floor_lamp(R, tx, ty, shade_col='#E0A040'):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 4, y - 2, x + 4, y + 1], fill=hexc('#5A3A24')); d.rectangle([x - 1, y - 34, x, y - 1], fill=hexc('#7A5A34'))
        d.polygon([(x - 4, y - 44), (x + 4, y - 44), (x + 7, y - 34), (x - 7, y - 34)], fill=hexc(shade_col)); d.line([(x - 7, y - 34), (x + 7, y - 34)], fill=hexc('#FFE8A0'))
        d.polygon([(x - 3, y - 43), (x - 1, y - 43), (x - 3, y - 35), (x - 5, y - 35)], fill=shade(hexc(shade_col), 1.2))
    R.obj('lamp', [(tx, ty)], f); R.light(tx + .5, ty + .5, -38, 36, [255, 190, 100], .6, 1)

def side_table(R, tx, ty, item='book'):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.rectangle([x - 1, y - 10, x, y], fill=hexc('#3E2216')); d.ellipse([x - 4, y - 1, x + 3, y + 1], fill=hexc('#3E2216'))
        d.ellipse([x - 7, y - 13, x + 7, y - 8], fill=hexc('#8A5A34')); d.ellipse([x - 7, y - 14, x + 7, y - 9], fill=hexc('#A06A40'))
        if item == 'book': d.rectangle([x - 4, y - 15, x + 2, y - 12], fill=hexc('#4A2E6A')); d.line([(x - 4, y - 15), (x + 2, y - 15)], fill=hexc('#E0C070'))
        else: d.rectangle([x - 1, y - 20, x, y - 13], fill=hexc('#F2E6C8')); d.rectangle([x - 1, y - 22, x, y - 21], fill=hexc('#FFD27A')); d.ellipse([x - 3, y - 14, x + 2, y - 12], fill=hexc('#C8A050'))
    return f

def pouf(R, tx, ty, col):   # 둥근 방석 의자
    c = hexc(col)
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.rectangle([x - 6, y - 7, x + 6, y - 1], fill=shade(c, .75)); d.ellipse([x - 6, y - 4, x + 6, y + 1], fill=shade(c, .75))
        d.ellipse([x - 6, y - 10, x + 6, y - 4], fill=c); d.ellipse([x - 3, y - 9, x + 1, y - 7], fill=shade(c, 1.2)); d.point((x, y - 7), fill=shade(c, .6))
    return f

def chess_table(R, tx, ty):   # 마법 체스판 (말이 혼자 움직여요)
    def f(img, d):
        R.box(img, tx + .35, ty + .35, .3, .3, 8, '#5A3420', '#3A2014', '#4A2A18')
        R.box(img, tx + .05, ty + .05, .9, .9, 2, '#6A4228', '#4A2E1C', '#3E2616', lift=8)
        px = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                fx, fy = R.inv(x, y + 10)
                if tx + .15 <= fx < tx + .85 and ty + .15 <= fy < ty + .85:
                    i, j = int((fx - tx - .15) / .175), int((fy - ty - .15) / .175); px[x, y] = hexc('#E8DCC0') if (i + j) % 2 else hexc('#3A2A3A')
        for (a, b, c, o) in ((.3, .3, '#F2E8D8', '#8A7A6A'), (.7, .4, '#2A1E2A', '#C86AE8'), (.45, .7, '#F2E8D8', '#8A7A6A'), (.65, .7, '#2A1E2A', '#C86AE8')):
            x, y = R.P(tx + a, ty + b); y -= 10; d.rectangle([x - 1, y - 5, x + 1, y], fill=hexc(c)); d.rectangle([x - 1, y - 7, x + 1, y - 6], fill=hexc(o)); d.point((x, y - 8), fill=hexc(c))
    return f

def notice_board(R, side, u0, w=34, h=30, v0=28):   # 3학년 게시판 (코르크판 + 의뢰 쪽지)
    notes = [(3, 4, 9, 9, '#F2E6C8'), (14, 3, 8, 10, '#FFE08A'), (24, 5, 7, 8, '#BFE0F2'), (5, 15, 10, 8, '#F2C8D8'), (17, 15, 7, 9, '#F2E6C8'), (26, 15, 5, 7, '#C8F0C0')]
    def fn(uu, vv):
        if uu < 2 or uu >= w - 2 or vv < 2 or vv >= h - 2: return hexc('#6A4228') if (uu + vv) % 7 else hexc('#7A5030')
        if vv >= h - 7 and 9 <= uu < w - 9:   # 위쪽 이름표 (금색)
            return hexc('#E0B050') if vv in (h - 7, h - 3) or uu in (9, w - 10) else hexc('#4A2A5A')
        for k, (a, b, ww, hh, c) in enumerate(notes):
            if a <= uu < a + ww and b <= vv < b + hh:
                if vv == b + hh - 2 and uu == a + ww // 2: return hexc(['#D84A4A', '#4A8AD8', '#E0B050'][k % 3])   # 압정
                if (vv - b) % 2 == 0 and a + 1 <= uu < a + ww - 1 - (vv * 3 + k) % 3 and vv < b + hh - 3: return hexc('#8A7A6A')
                return hexc(c)
        return hexc('#B8875A') if hsh(uu, vv) % 7 else hexc('#9A6E46')
    return wall_sprite(R, side, u0, u0 + w, v0, v0 + h, fn)

def pennant3(R, side, u0, v0=36, w=22, h=40):   # 3학년 깃발: 보라 천에 금색 3
    D3 = ['01110', '11011', '00011', '00110', '00011', '11011', '01110']
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < w and 0 <= vv < h + 2): return None
        if vv >= h: return hexc('#8A5A34') if -2 <= uu < w + 2 else None   # 막대
        tip = (h - vv)   # 아래가 V 모양
        if vv < 10 and abs(uu - w / 2 + .5) > (vv / 10) * (w / 2): return None
        if uu < 1 or uu >= w - 1 or (vv < 11 and abs(uu - w / 2 + .5) > (vv / 10) * (w / 2) - 1.2): return hexc('#E0A040')
        gx, gy = (uu - (w // 2 - 5)) // 2, (h - 8 - vv) // 2
        if 0 <= gx < 5 and 0 <= gy < 7 and D3[gy][gx] == '1': return hexc('#F2C860')
        if vv in (h - 4, h - 3): return hexc('#E0A040')
        return hexc('#5A2A7A') if (uu + vv) % 9 else hexc('#4E2470')
    R.wall_fill(side, f)

def flag_string(R, side, u0, u1, v=74, cols=('#7A4AA8', '#E0A040', '#C86A9A')):
    def f(u, vv):
        if not (u0 <= u < u1): return None
        sag = int(5 * math.sin((u - u0) / (u1 - u0) * math.pi))
        if vv == v - sag: return hexc('#3A2A20')
        k = (u - u0) // 8; uu = (u - u0) % 8
        if v - sag - 7 + abs(uu - 3.5) <= vv < v - sag and uu < 7: return hexc(cols[k % len(cols)])
        return None
    R.wall_fill(side, f)

def lounge3_room():
    R = Room(22, 18, wall=84)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    def flo(fx, fy):
        c = planks(['#6A4028', '#5E3822', '#74482E', '#643C26'], '#34200F')(fx, fy)
        if 10 <= fx < 12 and fy >= 16.6:   # 문 앞 발판
            e = min(fx - 10, 12 - fx, fy - 16.6, 18 - fy)
            return hexc('#E0A040') if e < .12 else hexc('#8A3A2A') if int((fx - 10) * 4) % 2 else hexc('#7A3224')
        return rug(lambda a, b: c, 5, 3.5, 17, 13.5, '#5A2E7A', '#E0A040', inner='#7A4AA8')(fx, fy)
    R.floor(flo)
    # 둥근 깔개 무늬 (가운데 별)
    for a in range(0, 360, 2):
        for rr in (2.3, 2.0):
            R.put(*R.P(11 + rr * math.cos(math.radians(a)), 8.5 + rr * .9 * math.sin(math.radians(a))), hexc('#E0A040'))
    for k in range(8):   # 반짝 별 (긴 빛 4 + 짧은 빛 4)
        a = math.radians(k * 45); L = 1.75 if k % 2 == 0 else 1.0
        for sgn in (-1, 1):
            b = a + sgn * math.radians(90)
            for t in [i / 30 for i in range(31)]:
                p0 = (math.cos(b) * .32, math.sin(b) * .32); p1 = (math.cos(a) * L, math.sin(a) * L)
                R.put(*R.P(11 + p0[0] + (p1[0] - p0[0]) * t, 8.5 + (p0[1] + (p1[1] - p0[1]) * t) * .9), hexc('#C88A3A'))
    R.walls('#3E2456', '#4E2E68', '#4A2A1A', trim='#E0A040')
    # 오른쪽 벽 (x 쪽): 책장 · 창 · 깃발 · 소파 · 창 · 트로피 선반
    R.window('R', 44, w=16, v0=30, h=36)
    pennant3(R, 'R', 70, v0=28)
    R.window('R', 108, w=16, v0=30, h=36)
    R.shelf('R', 140, 30, 50, ['#E0B050', '#7A2A30', '#4A2E6A', '#C8A050', '#2E5A6E', '#7A6A2A'])
    flag_string(R, 'R', 2, 176, 76)
    # 왼쪽 벽 (y 쪽): 게시판 · 벽난로 · 창
    fireplace(R, 'L', 58, w=44, h=48)
    R.wall_fill('L', lambda u, v: hexc('#F2E6C8') if (u in (66, 67, 96, 97) and 54 <= v < 61) else hexc('#FFD27A') if (u in (66, 97) and 61 <= v < 63) else None)   # 선반 위 초
    def frame(u, v):   # 선반 위 액자 (3학년 단체 사진)
        uu, vv = u - 74, v - 54
        if not (0 <= uu < 16 and 0 <= vv < 12): return None
        if uu < 2 or uu >= 14 or vv < 2 or vv >= 10: return hexc('#C8A050')
        if vv < 5: return hexc('#5A4A6A')
        return hexc('#F2D8B0') if (uu % 3 == 1 and vv in (5, 6)) else hexc('#3A2A5A') if vv < 7 else hexc('#8AA8D8')
    R.wall_fill('L', frame)
    R.window('L', 118, w=16, v0=30, h=36)
    flag_string(R, 'L', 4, 56, 76); flag_string(R, 'L', 106, 142, 76)
    for side, u in (('R', 36), ('R', 64), ('R', 98), ('R', 130), ('L', 112), ('L', 136), ('L', 14)): R.sconce(side, u)
    # 물건
    R.obj('shelf', tiles(1, 0, 4, 1), senior_shelf(R, 1, 0, 4), act=('선배의 책장', '책 읽기'))
    R.obj('sofa', tiles(8, 0, 3, 1), big_sofa(R, 8, 0, 3, '#8A2E5E'), act=('휴게실 소파', '쉬기'))
    R.obj('teatable', tiles(8, 3, 3, 1), tea_table(R, 8.4, 3.15), act=('찻상', '차 마시기'))
    R.obj('board', [(0, y) for y in range(12, 16)], notice_board(R, 'L', 18, 34, 30, 28), act=('3 학년 게시판', '선배 의뢰 보기'))
    R.obj('arm', [(3, 5)], armchair(R, 3, 5, '#9A3A5A', 'far'), act=('안락의자', '불 쬐기'))
    R.obj('arm', [(3, 9)], armchair(R, 3, 9, '#9A3A5A', 'near'), act=('안락의자', '불 쬐기'))
    R.obj('side', [(3, 7)], side_table(R, 3, 7, 'candle')); R.light(3.5, 7.5, -20, 18, [255, 200, 120], .45, 1)
    R.obj('chess', [(15, 9)], chess_table(R, 15, 9), act=('마법 체스판', '한 판 두기'))
    R.obj('chair', [(16, 9)], chair_draw(R, 16, 9, '#9A5AC0')); R.obj('chair', [(15, 10)], chair_draw(R, 15, 10, '#9A5AC0'))
    for (x, y, c) in ((8, 6, '#E0A040'), (13, 6, '#C86A9A')): R.obj('pouf', [(x, y)], pouf(R, x, y, c), act=('방석 의자', '앉아서 수다 떨기'))
    floor_lamp(R, 6, 1); floor_lamp(R, 12, 0); floor_lamp(R, 20, 8)
    R.obj('side', [(18, 1)], side_table(R, 18, 1, 'book'))
    R.obj('books', [(19, 1)], book_pile(R, 19, 1)); R.obj('books', [(1, 2)], book_pile(R, 1, 2))
    for (x, y) in ((0, 17), (21, 17), (21, 0), (0, 10)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#3E6A4E', '#E0A040'))
    R.obj('plant', [(7, 0)], plant_draw(R, 7, 0, '#2E5A44', '#C86AE8'))
    for (x, y) in ((6, 5), (16, 5), (11, 5), (7, 12), (15, 12), (11, 11), (19, 13), (3, 14)): float_candle(R, x, y)
    R.extra = dict(night=True)
    R.save('lounge3', '3학년 휴게실', '선배들의 아늑한 쉼터 · 물약 교실 문으로 나가요', [1, 14])

# ======================= 시계탑 옥상 관측실 =======================
SKY_TOP, SKY_BOT = hexc('#0A0C26'), hexc('#2A2458')
def sky_col(t, k):   # t: 0(위)~1(아래)
    c = tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3)) + (255,)
    h = hsh(*k) % 1000
    if h < 9: return hexc('#FFF4D0')
    if h < 22: return hexc('#9AA8E8')
    if h < 30: return shade(c, 1.5)
    return c

def night_sky_bg(R):   # 벽 위 빈 곳을 밤하늘로: 별 + 은하수
    fill = R.bg.getpixel((0, 0)); TOP, LEFT, RIGHT = R.P(0, 0), R.P(0, R.NY), R.P(R.NX, 0)
    for x in range(LEFT[0], RIGHT[0] + 1):
        yb = LEFT[1] - (x - LEFT[0]) / 2 if x <= TOP[0] else TOP[1] + (x - TOP[0]) / 2
        for y in range(0, int(yb) - R.WALL + 2):
            if R.px[x, y] != fill: continue
            t = y / max(1, yb - R.WALL); c = sky_col(min(1, t) * .5, (x, y))
            band = abs((y - 70) + (x - R.W / 2) * .35)
            if band < 14 and hsh(x, y, 3) % 4 == 0: c = shade(c, 1.25)
            R.px[x, y] = c
    for (x, y) in ((70, 30), (250, 14), (300, 48), (140, 8), (40, 70)):   # 반짝이는 큰 별
        if 0 <= x < R.W and R.px[x, y] != fill:
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): R.put(x + dx, y + dy, hexc('#FFF4D0') if dx == dy == 0 else hexc('#C8C8F0'))
        R.lights.append(dict(p=(x, y), dy=0, r=8, c=[220, 220, 255], a=.4, f=1))

def tower_wall(R, cu, cv, rad):   # 오른쪽 벽: 시계탑 돌벽 + 큰 시계판
    hh, mm = 11, 56
    ah, am = math.radians(90 - (hh + mm / 60) * 30), math.radians(90 - mm * 6)
    def seg(du, dv, a, L, wdt):
        ex, ey = math.cos(a) * L, math.sin(a) * L
        t = max(0, min(1, (du * ex + dv * ey) / (L * L))); return math.hypot(du - ex * t, dv - ey * t) < wdt
    def f(u, v):
        if v >= R.WALL - 6:   # 처마 돌
            return hexc('#8A8098') if v >= R.WALL - 2 else hexc('#6A6078') if (u // 10) % 2 else hexc('#5E5470')
        du, dv = u - cu, v - cv; r = math.hypot(du, dv)
        if r < rad:
            if r >= rad - 3: return hexc('#E0B050') if r < rad - 1.5 else hexc('#9A7030')
            if r >= rad - 5: return hexc('#2A2236')
            if seg(du, dv, am, rad - 9, 1.3): return hexc('#2A1E2A')
            if seg(du, dv, ah, rad - 16, 1.8): return hexc('#2A1E2A')
            if r < 2.5: return hexc('#C8A050')
            ang = math.degrees(math.atan2(dv, du)) % 360
            for k in range(12):
                da = abs((ang - k * 30 + 180) % 360 - 180)
                if rad - 11 < r < rad - 6 and da < (5 if k % 3 == 0 else 2.6) * 30 / r: return hexc('#3A2A3A')
            if rad - 13 < r < rad - 12: return hexc('#C8B890')
            return hexc('#EADDB4') if (u + v) % 13 else hexc('#DDCFA4')
        if rad <= r < rad + 4: return hexc('#4A4258') if (int(math.degrees(math.atan2(dv, du))) // 15) % 2 else hexc('#3E3850')   # 둘레 돌
        row = v // 8; off = (row % 2) * 7; col = (u + off) // 14
        if v % 8 == 0 or (u + off) % 14 == 0: return hexc('#2A2638')
        c = ['#4A4560', '#454058', '#504A66', '#423D56'][hsh(row, col) % 4]
        return shade(hexc(c), .8 + .2 * v / R.WALL)
    R.wall_fill('R', f)
    x, y = R.wall_px('R', cu, cv); R.lights.append(dict(p=(x, y), dy=0, r=46, c=[255, 230, 170], a=.35, f=0))

def parapet_view(R):   # 왼쪽: 낮은 돌 난간 너머로 마을 지붕과 밤하늘
    NU = R.NY * 8
    def bldg(u):
        b = u // 9; h = 8 + hsh(b, 7) % 16
        if hsh(b, 11) % 6 == 0: h += 10 - abs(u % 9 - 4) * 2   # 뾰족 지붕
        return h
    def f(u, v):
        if v < 20:
            if v >= 16: return hexc('#8A8298') if v >= 18 else hexc('#6E6680')
            row = v // 5; off = (row % 2) * 6
            if v % 5 == 0 or (u + off) % 12 == 0: return hexc('#2E2A3C')
            return hexc(['#5A5470', '#544E68', '#605A76'][hsh(row, (u + off) // 12) % 3])
        h = 20 + bldg(u)
        if v < h:
            b = u // 9
            if v == h - 1: return hexc('#4A4070')   # 지붕선 달빛
            if (u % 9) in (2, 3, 5, 6) and (v - 20) % 6 in (2, 3) and hsh(b, v // 6, u % 9 // 3) % 3 == 0: return hexc('#FFD27A')
            return hexc('#2A2448') if hsh(b) % 2 else hexc('#322A54')
        if (u - 100) ** 2 + (v - 76) ** 2 < 64 and (u - 104) ** 2 + (v - 79) ** 2 >= 49:   # 초승달
            return hexc('#FFF4C8') if (u - 100) ** 2 + (v - 76) ** 2 < 40 else hexc('#E8DCA8')
        return sky_col(1 - (v - 20) / (R.WALL - 20), (u, v, 5))
    R.wall_fill('L', f)
    for u in (24, 64, 94, 128):   # 마을 창 불빛
        x, y = R.wall_px('L', u, 26); R.lights.append(dict(p=(x, y), dy=0, r=10, c=[255, 200, 110], a=.35, f=1))
    x, y = R.wall_px('L', 100, 76); R.lights.append(dict(p=(x, y), dy=0, r=22, c=[230, 230, 255], a=.4, f=0))

def star_charts(R, side, u0, v0=36):
    def f(u, v):
        uu, vv = u - u0, v - v0
        for a, b, w, h, c in ((0, 0, 20, 24, '#E8DCB8'), (24, 6, 16, 18, '#D8E0F0')):
            if a <= uu < a + w and b <= vv < b + h:
                q, r_ = uu - a, vv - b
                if q in (0, w - 1) or r_ in (0, h - 1): return shade(hexc(c), .75)
                if hsh(q, r_, a) % 23 == 0: return hexc('#2A3A7A')
                if (q - w / 2) ** 2 + (r_ - h / 2) ** 2 < (w / 2.6) ** 2 and abs(math.hypot(q - w / 2, r_ - h / 2) - w / 2.8) < .6: return hexc('#7A6A9A')
                if abs(r_ - h / 2 - (q - w / 2) * .6) < .5 and 3 < q < w - 3: return hexc('#C8A050')
                return hexc(c)
        if vv == 25 and uu in (10, 32): return hexc('#C8A050')
        return None
    R.wall_fill(side, f)

def telescope(R, tx, ty):   # 2×2 놋쇠 망원경 (왼쪽 위 하늘을 봐요)
    def f(img, d):
        cx, cy = R.P(tx + 1, ty + 1)
        R.box(img, tx + .55, ty + .55, .9, .9, 4, '#4A4458', '#34303E', '#3E3A4A')   # 받침돌
        hub = (cx, cy - 26)
        for fx_, fy_ in ((-13, 2), (12, 1), (1, 7)): d.line([(cx + fx_, cy + fy_ - 3), hub], fill=hexc('#5A3420'), width=3); d.line([(cx + fx_ + 1, cy + fy_ - 3), hub], fill=hexc('#7A4A2A'))
        d.ellipse([hub[0] - 4, hub[1] - 3, hub[0] + 4, hub[1] + 3], fill=hexc('#9A7030'))
        ax, ay, bx, by = hub[0] + 14, hub[1] + 2, hub[0] - 24, hub[1] - 26
        L = math.hypot(bx - ax, by - ay); nx, ny = -(by - ay) / L, (bx - ax) / L
        def tube(t0, t1, w0, w1, c):
            p0 = (ax + (bx - ax) * t0, ay + (by - ay) * t0); p1 = (ax + (bx - ax) * t1, ay + (by - ay) * t1)
            d.polygon([(p0[0] + nx * w0, p0[1] + ny * w0), (p1[0] + nx * w1, p1[1] + ny * w1), (p1[0] - nx * w1, p1[1] - ny * w1), (p0[0] - nx * w0, p0[1] - ny * w0)], fill=c)
        tube(0, 1, 3.2, 6.2, hexc('#C8962E')); tube(0, 1, 1.2, 2.6, hexc('#E8C060'))
        tube(.6, 1, -1, -4.5, hexc('#9A6E24'))
        for t in (.12, .45, .78, .97): tube(t, t + .035, 3.6 + 3 * t, 3.6 + 3 * t, hexc('#7A5420'))
        tube(-.12, .02, 1.6, 2.2, hexc('#5A3A1A'))   # 접안렌즈
        ex, ey = bx, by; d.ellipse([ex - 4, ey - 6, ex + 4, ey + 6], fill=hexc('#3A4A8A')); d.ellipse([ex - 2, ey - 4, ex + 1, ey], fill=hexc('#9AB8FF'))
        sx, sy = ax + (bx - ax) * .4 + nx * 7, ay + (by - ay) * .4 + ny * 7   # 파인더
        d.line([(sx, sy), (sx + (bx - ax) * .25, sy + (by - ay) * .25)], fill=hexc('#9A7030'), width=2)
    return f

def crystal_ball(R, tx, ty):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.polygon([(x - 6, y), (x + 6, y), (x + 3, y - 4), (x - 3, y - 4)], fill=hexc('#3A3448'))
        d.rectangle([x - 2, y - 16, x + 1, y - 4], fill=hexc('#5A4A6A')); d.rectangle([x - 2, y - 16, x - 1, y - 4], fill=hexc('#6E5E80'))
        d.polygon([(x - 6, y - 16), (x + 6, y - 16), (x + 4, y - 19), (x - 4, y - 19)], fill=hexc('#C8A050'))
        d.ellipse([x - 8, y - 34, x + 8, y - 18], fill=hexc('#5A4AB8')); d.ellipse([x - 7, y - 33, x + 6, y - 20], fill=hexc('#7A6AE0'))
        d.ellipse([x - 4, y - 28, x + 3, y - 24], fill=hexc('#E8F0FF')); d.ellipse([x - 1, y - 30, x + 5, y - 26], fill=hexc('#D0DCFF'))   # 구름
        d.line([(x - 5, y - 22), (x - 1, y - 21)], fill=hexc('#9AD8FF')); d.point((x + 3, y - 23), fill=hexc('#FFE890'))
        d.ellipse([x - 5, y - 32, x - 2, y - 29], fill=hexc('#F2F4FF'))
    return f

def research_desk(R, tx, ty, w=3):
    def f(img, d):
        R.box(img, tx, ty + .05, w, .9, 13, '#9A7450', '#5A3E2C', '#4A3424')
        for k in range(1, w): a, b = R.P(tx + k - .5, ty + .95); d.rectangle([a - 2, b - 9, a + 1, b - 8], fill=hexc('#C8A050'))
        x, y = R.P(tx + .7, ty + .5); y -= 13
        d.polygon([(x - 7, y - 1), (x + 1, y - 4), (x + 6, y - 1), (x - 2, y + 2)], fill=hexc('#EADDB4')); d.line([(x - 4, y - 1), (x + 2, y - 2)], fill=hexc('#6A5A8A')); d.line([(x - 2, y + 1), (x + 3, y - 1)], fill=hexc('#6A5A8A'))
        d.line([(x + 3, y - 3), (x + 7, y - 11)], fill=hexc('#F2F0E8')); d.point((x + 7, y - 12), fill=hexc('#3A2A3A'))   # 깃펜
        x, y = R.P(tx + 1.6, ty + .4); y -= 13
        for dx, c, hgt in ((-6, '#7AF0C0', 10), (0, '#C08AFF', 14), (6, '#FFD86A', 8)):   # 빛나는 플라스크
            d.ellipse([x + dx - 3, y - 6, x + dx + 3, y], fill=hexc(c)); d.rectangle([x + dx - 1, y - hgt, x + dx, y - 5], fill=hexc('#D8E8F0')); d.point((x + dx - 1, y - 4), fill=hexc('#FFFFFF'))
        x, y = R.P(tx + 2.55, ty + .45); y -= 13
        d.ellipse([x - 7, y - 5, x + 7, y + 3], outline=hexc('#C8A050')); d.ellipse([x - 3, y - 15, x + 3, y - 9], outline=hexc('#C8A050'))   # 작은 혼천의
        d.line([(x, y - 1), (x, y - 9)], fill=hexc('#9A7030')); d.ellipse([x - 2, y - 7, x + 2, y - 3], fill=hexc('#FFD86A'))
    return f

def railing(R, x0, y0, x1, y1, h=12):   # 쇠 난간 한 토막 (앞 가장자리)
    def f(img, d):
        a, b = R.P(x0, y0), R.P(x1, y1); n = max(1, int(round(math.hypot(x1 - x0, y1 - y0))))
        for k in range(n * 2 + 1):
            t = k / (n * 2); p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            d.line([tuple(map(int, p)), tuple(map(int, up(p, h)))], fill=hexc('#3A3448') if k % 2 else hexc('#4A4458'))
        for hh, c in ((h, '#8A7A9A'), (h - 1, '#5A5068'), (5, '#4A4458')): d.line([tuple(map(int, up(a, hh))), tuple(map(int, up(b, hh)))], fill=hexc(c))
        for t in (0, 1):
            p = a if t == 0 else b; d.rectangle([int(p[0]) - 1, int(p[1]) - h - 3, int(p[0]) + 1, int(p[1])], fill=hexc('#5A5068')); d.rectangle([int(p[0]) - 1, int(p[1]) - h - 4, int(p[0]) + 1, int(p[1]) - h - 3], fill=hexc('#C8A050'))
    return f

def view_scope(R, tx, ty):   # 난간 망원 쌍안경 (난간 앞 자리)
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 4, y - 2, x + 4, y + 1], fill=hexc('#3A3448')); d.rectangle([x - 1, y - 20, x + 1, y - 1], fill=hexc('#5A5068'))
        d.rectangle([x - 6, y - 27, x + 4, y - 20], fill=hexc('#2E7A6A')); d.rectangle([x - 6, y - 27, x + 4, y - 26], fill=hexc('#4AA890'))
        for dx in (-7, 0): d.rectangle([x + dx - 2, y - 26, x + dx + 1, y - 21], fill=hexc('#C8A050')); d.point((x + dx - 1, y - 24), fill=hexc('#9AB8FF'))
        d.rectangle([x + 5, y - 18, x + 8, y - 15], fill=hexc('#C8A050'))   # 동전 넣는 곳
    return f

def lantern_post(R, tx, ty, h=30):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 4, y - 2, x + 4, y + 1], fill=hexc('#3A3448')); d.rectangle([x - 1, y - h, x, y - 1], fill=hexc('#2E2A38'))
        d.line([(x, y - h), (x + 5, y - h)], fill=hexc('#2E2A38')); d.rectangle([x + 3, y - h + 1, x + 8, y - h + 9], fill=hexc('#FFD27A')); d.rectangle([x + 3, y - h + 1, x + 8, y - h + 1], fill=hexc('#2E2A38'))
        d.polygon([(x + 2, y - h + 1), (x + 9, y - h + 1), (x + 5, y - h - 3)], fill=hexc('#2E2A38')); d.line([(x + 5, y - h + 2), (x + 5, y - h + 8)], fill=hexc('#C88A3A'))
    R.obj('lantern', [(tx, ty)], f); R.light(tx + .5, ty + .5, -h + 4, 38, [255, 190, 110], .65, 1)

def stone_bench(R, tx, ty, w=2):
    def f(img, d):
        for a in (.2, w - .5): R.box(img, tx + a, ty + .25, .3, .5, 6, '#5A5470', '#3E3850', '#4A4460')
        R.box(img, tx, ty + .15, w, .7, 3, '#7A7290', '#4E4864', '#5E5876', lift=6)
        x, y = R.P(tx + .5, ty + .5); y -= 9   # 놓고 간 담요·책
        d.polygon([(x - 5, y), (x + 4, y - 3), (x + 6, y + 1), (x - 3, y + 4)], fill=hexc('#3A4A8A')); d.line([(x - 4, y + 1), (x + 5, y - 2)], fill=hexc('#6A7AC8'))
    return f

def night_flower(R, tx, ty, flower='#9AE8FF'):
    p = plant_draw(R, tx, ty, '#2E4A5A', flower)
    def f(img, d):
        p(img, d); cx, cy = R.P(tx + .5, ty + .5)
        for dx, dy in ((-4, -15), (3, -17), (0, -21), (-6, -11), (5, -12)): d.ellipse([cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1], fill=hexc(flower))
    R.obj('plant', [(tx, ty)], f); R.light(tx + .5, ty + .5, -16, 14, [140, 220, 255], .35, 1)

def chart_easel(R, tx, ty):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        for a, b in ((-6, 0), (6, 0), (0, -2)): d.line([(x + a, y + b), (x, y - 36)], fill=hexc('#5A3420'), width=2)
        d.polygon([(x - 10, y - 34), (x + 10, y - 38), (x + 10, y - 14), (x - 10, y - 10)], fill=hexc('#1E2450'))
        d.polygon([(x - 10, y - 34), (x + 10, y - 38), (x + 10, y - 37), (x - 10, y - 33)], fill=hexc('#C8A050'))
        for (a, b) in ((-6, -27), (-2, -30), (3, -25), (6, -31), (-4, -19), (4, -18)): d.point((x + a, y + b), fill=hexc('#FFF4D0'))
        d.line([(x - 6, y - 27), (x - 2, y - 30), (x + 3, y - 25), (x + 6, y - 31)], fill=hexc('#7A8AD8')); d.line([(x - 4, y - 19), (x + 4, y - 18)], fill=hexc('#7A8AD8'))
        d.rectangle([x - 11, y - 11, x + 11, y - 9], fill=hexc('#5A3420'))
    return f

def scroll_pile(R, tx, ty):
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        for k, (dx, dy) in enumerate(((-4, -2), (3, -1), (0, -5), (-2, -8))):
            d.rectangle([x + dx - 5, y + dy - 3, x + dx + 5, y + dy], fill=hexc('#E8DCB8' if k % 2 else '#D8C8A0')); d.ellipse([x + dx + 4, y + dy - 3, x + dx + 6, y + dy], fill=hexc('#B8A880'))
            d.line([(x + dx - 1, y + dy - 3), (x + dx - 1, y + dy)], fill=hexc('#8A2A30'))
    return f

def observatory_room():
    R = Room(22, 18, wall=100)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    CX, CY = 8, 9
    def flo(fx, fy):
        i, j = int(fx), int(fy); a, b = fx - i, fy - j
        c = hexc(['#3E4260', '#383C58', '#444866', '#3A3E5C'][hsh(i, j) % 4])
        if a < .06 or b < .06: c = hexc('#22243A')
        elif hsh(i, j, 2) % 5 == 0 and abs(a - b) < .05: c = shade(c, .85)   # 금
        r = math.hypot(fx - CX, (fy - CY))
        if abs(r - 3.6) < .08 or abs(r - 2.9) < .06: c = hexc('#C8A050')
        elif 2.9 < r < 3.6:
            ang = math.degrees(math.atan2(fy - CY, fx - CX)) % 30
            c = hexc('#C8A050') if ang < 1.2 else hexc('#2E2A50')
            if 13 < ang < 17 and abs(r - 3.25) < .12: c = hexc('#E8D090')
        elif r < 2.9 and abs(r - 1.6) < .05: c = hexc('#8A7A50')
        if 10 <= fx < 13 and fy >= 16.4:   # 아래층 계단 (나가는 곳)
            st = min(3, int((fy - 16.4) / .4))
            c = hexc(['#7A7294', '#5A5474', '#3E3A56', '#2A2640'][st]) if (fy - 16.4) % .4 > .1 else hexc('#0E0A16')
            if (fy - 16.4) % .4 > .34: c = hexc('#9A90B4')   # 계단 모서리
            if fx < 10.15 or fx > 12.85: c = hexc('#C8A050')
        return c
    R.floor(flo)
    tower_wall(R, 96, 52, 34)
    star_charts(R, 'R', 136, 36)
    parapet_view(R)
    TOP = R.P(0, 0)
    for v in range(R.WALL):   # 탑 모서리 기둥
        for dd in (-1, 0, 1): R.put(TOP[0] + dd, TOP[1] - v, hexc('#3A3448') if dd else hexc('#5A5068'))
    night_sky_bg(R)
    for side, u in (('R', 30), ('R', 58), ('R', 168)): R.sconce(side, u)
    # 물건
    R.obj('telescope', tiles(CX - 1, CY - 1, 2, 2), telescope(R, CX - 1, CY - 1), act=('별 관측 망원경', '들여다보기'))
    R.obj('crystal', [(16, 9)], crystal_ball(R, 16, 9), act=('날씨 점 수정구', '내일 날씨 보기')); R.light(16.5, 9.5, -26, 30, [150, 130, 255], .6, 1)
    R.obj('desk', tiles(16, 0, 3, 1), research_desk(R, 16, 0), act=('마법 연구대', '연구하기')); R.light(17.6, .4, -18, 26, [140, 255, 200], .5, 1)
    R.obj('chair', [(17, 1)], chair_draw(R, 17, 1, '#3A4A8A'))
    R.obj('scope', [(0, 6)], view_scope(R, 0, 6), act=('시계탑 난간', '마을 내려다보기'))
    R.obj('easel', [(4, 3)], chart_easel(R, 4, 3), act=('별자리 지도', '구경하기'))
    R.obj('books', [(20, 1)], book_pile(R, 20, 1)); R.obj('books', [(3, 0)], book_pile(R, 3, 0))
    R.obj('bench', tiles(3, 14, 2, 1), stone_bench(R, 3, 14), act=('돌 벤치', '앉아서 별 보기'))
    R.obj('bench', tiles(14, 14, 2, 1), stone_bench(R, 14, 14), act=('돌 벤치', '앉아서 별 보기'))
    for (x, y) in ((0, 1), (0, 12), (6, 0), (20, 12), (8, 16), (14, 16)): lantern_post(R, x, y)
    for (x, y) in ((1, 16), (2, 16), (20, 16), (0, 3), (21, 6), (13, 6)): night_flower(R, x, y, '#9AE8FF' if (x + y) % 2 else '#E8A0FF')
    # 앞 가장자리 쇠 난간 (가운데는 내려가는 계단 자리)
    for (a, b) in ((0, 5), (5, 10), (13, 17), (17, 22)):
        R.obj('rail', [(k, 17) for k in range(a, b)], railing(R, a, 18, b, 18))
    for (a, b) in ((0, 6), (6, 12), (12, 17)):
        R.obj('rail', [(21, k) for k in range(a, b)], railing(R, 22, a, 22, 18 if b == 17 else b))
    R.extra = dict(night=True)
    R.save('observatory', '시계탑 옥상 관측실', '4학년의 별 보는 옥상 · 계단으로 내려가요', [1, 14])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True); lounge3_room(); observatory_room()
