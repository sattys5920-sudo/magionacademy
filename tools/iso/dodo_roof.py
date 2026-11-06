# 시계탑 꼭대기 방 (도도의 경매장) · 교정 시계탑에 기댄 사다리로 올라와요 · 사방 돌벽에 창문
#   관측실(senior_rooms.py)의 시계판 · 난간 · 등불을 그대로 쓰고, 하늘은 낮 하늘 (별 · 달 없음)
#   python3 dodo_roof.py → out/clock_roof_bg.png · _obj.png · .json
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade
import senior_rooms as S
SKY_T, SKY_B = hexc('#5C8FD8'), hexc('#BFD9F2')
def day_sky(t, k):
    c = tuple(int(SKY_T[i] + (SKY_B[i] - SKY_T[i]) * t) for i in range(3)) + (255,)
    return c
def day_sky_bg(R):   # 벽 위 빈 곳: 낮 하늘 + 구름 몇 점
    fill = R.bg.getpixel((0, 0)); TOP, LEFT, RIGHT = R.P(0, 0), R.P(0, R.NY), R.P(R.NX, 0)
    for x in range(LEFT[0], RIGHT[0] + 1):
        yb = LEFT[1] - (x - LEFT[0]) / 2 if x <= TOP[0] else TOP[1] + (x - TOP[0]) / 2
        for y in range(0, int(yb) - R.WALL + 2):
            if R.px[x, y] != fill: continue
            c = day_sky(min(1, y / max(1, yb - R.WALL)) * .6, (x, y))
            for cx, cy, rw in ((60, 26, 22), (200, 14, 18), (250, 40, 14)):
                if ((x - cx) / rw) ** 2 + ((y - cy) / (rw * .35)) ** 2 < 1: c = hexc('#F4F8FF') if y < cy + 2 else hexc('#DCE6F4')
            R.px[x, y] = c
def roof_view(R):   # 왼쪽: 낮은 돌 난간 너머로 낮 마을 지붕
    def bldg(u):
        b = u // 9; h = 8 + S.hsh(b, 7) % 16
        if S.hsh(b, 11) % 6 == 0: h += 10 - abs(u % 9 - 4) * 2
        return h
    def f(u, v):
        if v < 20:
            if v >= 16: return hexc('#A8A0B4') if v >= 18 else hexc('#8A8298')
            row = v // 5; off = (row % 2) * 6
            if v % 5 == 0 or (u + off) % 12 == 0: return hexc('#4E4A5C')
            return hexc(['#7A7490', '#746E88', '#807A96'][S.hsh(row, (u + off) // 12) % 3])
        h = 20 + bldg(u)
        if v < h:
            b = u // 9
            if v == h - 1: return hexc('#C86A4A')
            if (u % 9) in (2, 3, 5, 6) and (v - 20) % 6 in (2, 3) and S.hsh(b, v // 6, u % 9 // 3) % 3 == 0: return hexc('#3A3A5A')
            return hexc(['#B85A3E', '#9A6A8A', '#6A7AAA', '#C8945A'][S.hsh(b) % 4])
        return day_sky(1 - (v - 20) / (R.WALL - 20), (u, v))
    R.wall_fill('L', f)
def stone_walls(R, wins):   # 양쪽 벽 모두 시계탑 돌벽 · 아치 창문 너머로 낮 하늘과 마을 지붕
    def bldg(u):
        b = u // 7; return 4 + S.hsh(b, 7) % 9
    for side, dk in (('L', .86), ('R', 1.0)):
        def f(u, v, side=side, dk=dk):
            for (u0, w) in wins[side]:
                v0, h = 30, 46
                uu, vv = u - u0, v - v0
                if not (0 <= uu < w and 0 <= vv < h): continue
                cx = w / 2; top = h - cx; out = (uu + .5 - cx) ** 2 + (vv - top) ** 2
                if vv > top and out > cx ** 2: continue
                if uu < 2 or uu >= w - 2 or vv < 2 or (vv > top and out > (cx - 2) ** 2): return hexc('#2A2236')
                if uu in (w // 2 - 1, w // 2) or vv == 22: return hexc('#3A3046')   # 창살
                gu = u + (0 if side == 'L' else 300); hb = bldg(gu)
                if vv - 2 < hb:
                    if vv - 2 == hb - 1: return hexc('#C86A4A')
                    return hexc(['#B85A3E', '#9A6A8A', '#6A7AAA', '#C8945A'][S.hsh(gu // 7) % 4])
                c = day_sky(1 - vv / h, (u, v))
                for ccx, ccy, rw in ((u0 + w * .35, v0 + h - 12, 6),):
                    if ((u - ccx) / rw) ** 2 + ((v - ccy) / (rw * .4)) ** 2 < 1: c = hexc('#F4F8FF')
                return c
            if v >= R.WALL - 6:   # 처마 돌
                return hexc('#8A8098') if v >= R.WALL - 2 else hexc('#6A6078') if (u // 10) % 2 else hexc('#5E5470')
            if v < 4: return shade(hexc('#3A344A'), dk)   # 굽돌
            row = v // 8; off = (row % 2) * 7; col = (u + off) // 14
            if v % 8 == 0 or (u + off) % 14 == 0: return shade(hexc('#2A2638'), dk)
            c = ['#4A4560', '#454058', '#504A66', '#423D56'][S.hsh(row, col, side == 'L') % 4]
            return shade(hexc(c), dk * (.8 + .2 * v / R.WALL))
        R.wall_fill(side, f)
        for (u0, w) in wins[side]:   # 창으로 드는 햇빛
            x, y = R.wall_px(side, u0 + w / 2, 50); R.lights.append(dict(p=(x, y), dy=0, r=30, c=[255, 240, 200], a=.3, f=0))
def crate_jars(R, tx, ty):   # 사과 상자 위 내기 단지 셋 (호박씨 · 도토리 · 사탕)
    def f(img, d):
        R.box(img, tx + .05, ty + .05, .9, .9, 12, '#B07A44', '#7A4E28', '#8E5E32')
        x, y = R.P(tx + .5, ty + .5); y -= 12
        for dx, fill in ((-8, '#F2C060'), (0, '#8A5A34'), (8, '#E86A8A')):
            d.rectangle([x + dx - 3, y - 9, x + dx + 3, y], fill=hexc('#D8ECF4')); d.rectangle([x + dx - 3, y - 5, x + dx + 3, y], fill=hexc(fill))
            d.rectangle([x + dx - 3, y - 11, x + dx + 3, y - 9], fill=hexc('#7A5A3A'))
        d.rectangle([x - 6, y + 4, x + 6, y + 7], fill=hexc('#F2E6C8')); d.line([(x - 5, y + 5), (x + 5, y + 5)], fill=hexc('#5A3A24'))   # 내기 쪽지
    return f
def podium(R, tx, ty):   # 작은 경매대 + 망치
    def f(img, d):
        R.box(img, tx + .15, ty + .15, .7, .7, 16, '#8A4A2A', '#5A2E18', '#6E3A20')
        R.box(img, tx + .05, ty + .05, .9, .9, 3, '#A86A3A', '#6A3A20', '#7E4A28', lift=16)
        x, y = R.P(tx + .5, ty + .5); y -= 21
        d.rectangle([x - 1, y - 6, x + 6, y - 4], fill=hexc('#7A4A28')); d.rectangle([x + 4, y - 9, x + 8, y - 1], fill=hexc('#A06A3A'))   # 망치
        d.rectangle([x - 6, y - 2, x - 1, y], fill=hexc('#C8302E'))   # 빨간 천
    return f
def ladder_hole(fx, fy, ex, NY):   # 앞 가운데: 내려가는 사다리 구멍
    if ex <= fx < ex + 1 and fy >= NY - 1.1:
        if fx - ex < .12 or fx - ex > .88: return hexc('#7A5A34')
        return hexc('#8E6A3E') if (fy - (NY - 1.1)) % .28 < .07 else hexc('#1A1220')
    return None
def roof():
    R = Room(12, 10, wall=100)
    R.exit_to, R.exit_label = 'campus', '교정 (사다리)'
    ex = R.NX // 2
    def flo(fx, fy):
        h = ladder_hole(fx, fy, ex, R.NY)
        if h: return h
        i, j = int(fx), int(fy); a, b = fx - i, fy - j
        c = hexc(['#7A6E86', '#746880', '#80748C', '#6E6280'][S.hsh(i, j) % 4])
        if a < .06 or b < .06: c = hexc('#4A4058')
        if (j % 2 == 0 and abs(a - .5) < .04): c = hexc('#4A4058')   # 슬레이트 엇갈림
        return c
    R.floor(flo)
    stone_walls(R, {'L': [(12, 22), (46, 22)], 'R': [(10, 22), (38, 22), (66, 22)]})
    TOP = R.P(0, 0)
    for v in range(R.WALL):
        for dd in (-1, 0, 1): R.put(TOP[0] + dd, TOP[1] - v, hexc('#2A2638') if dd else hexc('#3E3850'))
    R.obj('jars', [(9, 1)], crate_jars(R, 9, 1), act=('내기 단지', '들여다보기'))
    R.obj('podium', [(3, 2)], podium(R, 3, 2), act=('작은 경매대', '구경하기'))
    R.obj('ledger', [(10, 4)], S.scroll_pile(R, 10, 4))
    for (x, y) in ((0, 0), (0, 8), (11, 7)): S.lantern_post(R, x, y)
    R.obj('bench', [(1, 5), (2, 5)], S.stone_bench(R, 1, 5), act=('돌 벤치', '앉아서 마을 보기'))
    for (a, b) in ((0, ex - 1), (ex + 2, 12)):
        R.obj('rail', [(k, 9) for k in range(a, b)], S.railing(R, a, 10, b, 10))
        R.extra = dict(night=False)
    R.save('clock_roof', '시계탑 꼭대기', '도도의 경매장 · 사다리로 내려가요', [41, 38])
if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True); roof()
