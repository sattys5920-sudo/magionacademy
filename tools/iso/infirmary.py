# 낡은 양호실 (누비) · 물약 교실 구석 책장 문 뒤에 숨은 방 · 마지막 날 따뜻한 양호실
#   (sera_room 은 쓰지 않는 예전 시안이에요)
#   python3 infirmary.py → out/infirmary_* · out/old_infirmary_* · tools/nubi_mock/infirmary_prev.png
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiors import Room, hexc, shade, up, checker, planks, plant_draw, chair_draw, ImageDraw
from dorms import curtains
from PIL import Image
NX, NY = 18, 14
OLD_U = 112   # 오른쪽 벽 낡은 문 자리 (x=14)

def cross_sign(R, side, u0, v0=56, faded=False, tilt=0):   # 빨간 십자 팻말
    bg, cr = (hexc('#D8D0C0'), hexc('#B86A62')) if faded else (hexc('#FFFFFF'), hexc('#E04848'))
    def f(u, v):
        uu, vv = u - u0, v - v0 - (uu_t(u) if tilt else 0)
        if not (0 <= uu < 14 and 0 <= vv < 12): return None
        if uu in (0, 13) or vv in (0, 11): return shade(bg, .7)
        if 5 <= uu <= 8 or 4 <= vv <= 7: return cr if (4 <= vv <= 7 and 2 <= uu <= 11) or (5 <= uu <= 8 and 2 <= vv <= 9) else bg
        return bg
    uu_t = lambda u: int((u - u0) * tilt)
    R.wall_fill(side, f)

def height_chart(R, side, u0):   # 키 재는 자
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < 8 and 6 <= v < 64): return None
        if uu in (0, 7): return hexc('#C8B890')
        if v % 6 == 0: return hexc('#5A4A3A') if uu < 5 else hexc('#F4ECD8')
        return hexc('#F4ECD8') if (v // 12) % 2 else hexc('#E8F4EE')
    R.wall_fill(side, f)

def med_cabinet(R, side, u0, broken=False):   # 벽 약장: 유리 칸에 약병
    BOT = ['#E04848', '#4AA8E0', '#5AC88A', '#F0C040', '#B07AE0', '#FFFFFF']
    def f(u, v):
        uu, vv = u - u0, v - 26
        if not (0 <= uu < 28 and 0 <= vv < 40): return None
        if uu < 2 or uu >= 26 or vv < 2 or vv >= 38: return hexc('#8A9A98') if not broken else hexc('#5A5450')
        if vv % 12 in (0, 1): return hexc('#C8D4D0') if not broken else hexc('#6A6460')
        k = (uu // 4 + vv // 12 * 3)
        if broken:
            if (uu * 3 + vv * 5) % 17 == 0 or abs((uu - 8) - (vv - 14) * .6) < .6 or abs((uu - 18) + (vv - 26) * .5) < .6: return hexc('#C8D0D8')   # 금 간 유리
            if k % 4 == 0 and uu % 4 in (1, 2) and vv % 12 > 6: return shade(hexc(BOT[k % len(BOT)]), .45)
            return hexc('#2A2630')
        if uu % 4 in (1, 2) and vv % 12 > 4: c = hexc(BOT[k % len(BOT)]); return shade(c, 1.2) if uu % 4 == 1 and vv % 12 == 6 else c
        return hexc('#DCEAF0')
    R.wall_fill(side, f)

def old_door(R, side, u0, ribbon=True):   # 페인트 벗겨진 낡은 나무문 · 녹슨 자물쇠 · 빛바랜 리본
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < 18 and 0 <= v < 50): return None
        top = 50 - 9
        if v > top and (uu + .5 - 9) ** 2 + (v - top) ** 2 > 81: return None
        if uu < 2 or uu >= 16 or (v > top and (uu + .5 - 9) ** 2 + (v - top) ** 2 > 49): return hexc('#3A2A20')
        c = hexc('#7A6E62') if (uu // 4) % 2 else hexc('#6E6258')
        if uu % 4 == 0: c = hexc('#4A3E36')
        if (uu * 7 + v * 3) % 23 < 3 or (v in range(18, 26) and uu in range(4, 9)): c = hexc('#8A5A3A')   # 벗겨진 칠 속 나무
        if v in (12, 36) : c = hexc('#3A2E28')
        return c
    R.wall_fill(side, f)
    R.wall_fill(side, hexc('#8A4A2A'), u0 + 11, u0 + 14, 22, 27); R.wall_fill(side, hexc('#B86A3A'), u0 + 12, u0 + 13, 23, 26)   # 녹슨 자물쇠
    R.wall_fill(side, hexc('#3A2A20'), u0 + 12, u0 + 13, 27, 30)
    if ribbon: R.wall_fill(side, hexc('#E8DCB0'), u0 + 13, u0 + 15, 18, 22); R.wall_fill(side, hexc('#C8B888'), u0 + 14, u0 + 15, 14, 19)

def bed(R, tx, ty, frame='#F4F4F0', blanket='#9AD8C8', sheet='#FFFFFF', bare=False, mess=False, head='N'):   # 철제 침대 · head='N' 머리가 뒷벽(오른쪽 벽) 쪽 · 'W' 머리가 왼쪽 벽 쪽
    fr = hexc(frame); W, D = (1.3, 2.2) if head == 'N' else (2.2, 1.3)
    def B(img, x, y, w, dp, h, top, l, r, lift=0): R.box(img, tx + x, ty + y, w, dp, h, top, l, r, lift)
    def f(img, d):
        hd = ((0, 0), (W - .1, 0)) if head == 'N' else ((0, 0), (0, D - .1))
        for (ox, oy) in ((0, 0), (W - .1, 0), (0, D - .1), (W - .1, D - .1)): B(img, ox, oy, .1, .1, 18 if (ox, oy) in hd else 11, fr, shade(fr, .6), shade(fr, .8))
        B(img, 0, 0, W, D, 2, shade(fr, .9), shade(fr, .6), shade(fr, .75), lift=5)
        if not bare:
            sh = hexc(sheet); bl = hexc(blanket)
            B(img, .05, .05, W - .1, D - .1, 3, sh, shade(sh, .75), shade(sh, .88), lift=7)
            if head == 'N':
                B(img, .05, .8 if not mess else 1.0, W - .1, D - .85 if not mess else D - 1.05, 2, bl, shade(bl, .6), shade(bl, .8), lift=10)
                B(img, .2, .12, W - .4, .45, 2, '#FFFFFF', '#C8C8C8', '#E0E0E0', lift=10)
            else:
                B(img, .8 if not mess else 1.0, .05, W - .85 if not mess else W - 1.05, D - .1, 2, bl, shade(bl, .6), shade(bl, .8), lift=10)
                B(img, .12, .2, .45, D - .4, 2, '#FFFFFF', '#C8C8C8', '#E0E0E0', lift=10)
            if mess: B(img, .4, .3, .5, .5, 1, shade(bl, 1.1), shade(bl, .6), shade(bl, .8), lift=11)
        if head == 'N': B(img, 0, -.05, W, .1, 12, fr, shade(fr, .6), shade(fr, .8), lift=6); B(img, 0, D - .05, W, .1, 4, fr, shade(fr, .6), shade(fr, .8), lift=7)
        else: B(img, -.05, 0, .1, D, 12, fr, shade(fr, .6), shade(fr, .8), lift=6); B(img, W - .05, 0, .1, D, 4, fr, shade(fr, .6), shade(fr, .8), lift=7)
    return f

def screen(R, tx, ty, col='#BFE2EE', torn=False, along='y', n=2):   # 칸막이 커튼 (침대 사이)
    c = hexc(col)
    def f(img, d):
        P = R.P
        if along == 'y': a, b = P(tx, ty), P(tx, ty + n)
        else: a, b = P(tx, ty), P(tx + n, ty)
        m = 9
        for k in range(m):
            t0, t1 = k / m, (k + 1) / m
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0); p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            cc = shade(c, .8 if k % 2 else 1.0); hh = 20 - (((k * 5) % 7) if torn else 0)
            d.polygon([tuple(map(int, up(p0, 2))), tuple(map(int, up(p1, 2))), tuple(map(int, up(p1, hh))), tuple(map(int, up(p0, hh)))], fill=cc)
        d.line([tuple(map(int, up(a, 22))), tuple(map(int, up(b, 22)))], fill=hexc('#8A9A98'), width=2)
        for q in (a, b): d.line([tuple(map(int, q)), tuple(map(int, up(q, 22)))], fill=hexc('#8A9A98'))
    return f

def desk(R, tx, ty):   # 세라 선생님 책상: 서류 · 진료 기록 · 따뜻한 차 · 체온계
    def f(img, d):
        R.box(img, tx, ty, 2, 1, 12, '#C8A07A', '#8A6A4A', '#A8825E')
        x, y = R.P(tx + .6, ty + .5); y -= 12
        d.polygon([(x - 6, y - 1), (x, y - 4), (x + 4, y - 2), (x - 2, y + 1)], fill=hexc('#FFFFFF')); d.line([(x - 3, y - 1), (x + 1, y - 3)], fill=hexc('#9AB8C8'))
        x2, y2 = R.P(tx + 1.4, ty + .5); y2 -= 12
        d.rectangle([x2 - 2, y2 - 5, x2 + 2, y2], fill=hexc('#F4ECD8')); d.line([(x2 - 1, y2 - 8), (x2, y2 - 6)], fill=hexc('#E8E8F0'))
        d.rectangle([x2 + 4, y2 - 2, x2 + 9, y2 - 1], fill=hexc('#E04848'))
    return f

def scale(R, tx, ty):
    def f(img, d):
        R.box(img, tx + .2, ty + .2, .6, .6, 2, '#E8E8E8', '#A8A8A8', '#C8C8C8')
        R.box(img, tx + .45, ty + .25, .1, .1, 22, '#C8C8C8', '#8A8A8A', '#A8A8A8')
        x, y = R.P(tx + .5, ty + .3); d.ellipse([x - 4, y - 30, x + 4, y - 22], fill=hexc('#FFFFFF')); d.line([(x, y - 26), (x + 2, y - 28)], fill=hexc('#E04848'))
    return f

def sink(R, tx, ty, old=False):
    def f(img, d):
        R.box(img, tx + .1, ty + .1, .8, .8, 12, '#E8E8E8' if not old else '#A8A098', '#B8B8B8' if not old else '#787068', '#D0D0D0' if not old else '#8A8278')
        x, y = R.P(tx + .5, ty + .5); d.ellipse([x - 5, y - 15, x + 5, y - 10], fill=hexc('#9AC8E0' if not old else '#4A4440'))
        d.line([(x + 3, y - 22), (x + 3, y - 14)], fill=hexc('#A8A8B0'))
    return f

def stool(R, tx, ty, fallen=False):
    def f(img, d):
        if fallen:
            x, y = R.P(tx + .5, ty + .5); d.ellipse([x - 6, y - 4, x + 6, y + 1], fill=hexc('#6A5240')); d.line([(x - 4, y - 2), (x - 12, y - 6)], fill=hexc('#4A3828'), width=2); d.line([(x + 2, y - 3), (x - 6, y - 9)], fill=hexc('#4A3828'), width=2)
        else: R.box(img, tx + .25, ty + .25, .5, .5, 8, '#C8A07A', '#8A6A4A', '#A8825E')
    return f

def clutter(R, tx, ty):   # 낡은 방 바닥: 붕대 뭉치 · 깨진 약병 · 먼지
    def f(img, d):
        x, y = R.P(tx + .5, ty + .5)
        d.ellipse([x - 4, y - 3, x + 3, y + 1], fill=hexc('#D8D0B8')); d.line([(x + 3, y - 1), (x + 10, y + 2)], fill=hexc('#D8D0B8'), width=2)
        d.rectangle([x - 12, y - 2, x - 8, y + 1], fill=hexc('#4A6A5A')); d.point((x - 6, y), fill=hexc('#8AB8A8')); d.point((x - 5, y + 1), fill=hexc('#8AB8A8'))
    return f

def cobweb(R, side, u0, v0):
    def f(u, v):
        uu, vv = u - u0, v - v0
        if not (0 <= uu < 22 and 0 <= vv < 22): return None
        r = math.hypot(uu, 22 - vv)
        if r > 22: return None
        a = math.atan2(22 - vv, uu)
        if abs((a * 6 / math.pi) % 1) < .08 or abs(r % 6) < .5: return hexc('#C8C8D0', 160)
    R.wall_fill(side, f)

def peel(R, side):   # 벽지가 군데군데 벗겨져 회벽이 보여요
    def f(u, v):
        if v < 26 or v > R.WALL - 6: return None
        n = math.sin(u * .31) + math.sin(v * .23 + u * .07) + math.sin((u + v) * .11)
        if n > 1.75: return hexc('#8A8478')
        if n > 1.55: return hexc('#5A5650')
    R.wall_fill(side, f)

def curtain_torn(R, side, u0, w=18):
    def f(u, v):
        uu = u - u0
        if R.WALL - 9 <= v < R.WALL - 6 and -6 <= uu < w + 6: return hexc('#6A5A48')
        if 20 <= v < R.WALL - 9 and (-6 <= uu < 0 or w <= uu < w + 6):
            if v < 24 + ((uu * 5) % 7) * 3: return None
            return hexc('#B8A880') if (uu % 3) else hexc('#988A68')
    R.wall_fill(side, f)

def sera_room():
    R = Room(NX, NY, wall=80)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    R.floor(checker('#E8F4EE', '#CFE6DC', 1))
    R.walls('#E4F2EE', '#CFE8E0', '#F4F0E6', trim='#7AB8A8')
    R.window('R', 14, w=18, glass=('#9ACCE8', '#BCE0F4', '#E8F6FF'), frame='#E8E8E8', moon=False)
    med_cabinet(R, 'R', 40); cross_sign(R, 'R', 76)
    R.window('R', 92, w=18, glass=('#9ACCE8', '#BCE0F4', '#E8F6FF'), frame='#E8E8E8', moon=False)
    old_door(R, 'R', OLD_U)
    height_chart(R, 'L', 12); R.window('L', 30, w=18, glass=('#9ACCE8', '#BCE0F4', '#E8F6FF'), frame='#E8E8E8', moon=False); R.window('L', 66, w=18, glass=('#9ACCE8', '#BCE0F4', '#E8F6FF'), frame='#E8E8E8', moon=False)
    for i, y in enumerate((3, 6.5, 10)):
        R.obj('bed', [(0, int(y)), (1, int(y))], bed(R, .2, y, blanket=['#9AD8C8', '#F8C4D0', '#BCD8F4'][i], head='W'), act=('양호실 침대', '누워서 쉬기'))
        if i < 2: R.obj('screen', [(0, int(y) + 2), (1, int(y) + 2)], screen(R, .1, y + 1.85, along='x', n=2.4), solid=False)
    R.obj('desk', [(9, 3), (10, 3)], desk(R, 9, 3), act=('세라 선생님 책상', '진료 기록 보기')); R.obj('chair', [(10, 4)], chair_draw(R, 10, 4, '#7AB8A8'))
    R.obj('scale', [(4, 1)], scale(R, 4, 1), act=('키 · 몸무게 재기', '재 보기'))
    R.obj('sink', [(8, 0)], sink(R, 8, 0), act=('세면대', '손 씻기'))
    for (x, y) in ((17, 13), (6, 13)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E8A5E', '#F8C4D0'))
    R.light(9.5, 3.5, -30, 40, [255, 250, 230], .35, 0)
    R.doors.append(dict(tile=[14, 0], to='old_infirmary', label='낡은 문', spawn=[9, 12], lock='nubi', back=[14, 1]))
    R.save('infirmary', '양호실', '세라 선생님의 양호실 · 물약 교실 문으로 나가요', [12, 1])
    return R

def old_room():
    R = Room(NX, NY, wall=80)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    R.floor(planks(['#5E5448', '#544A40', '#665A4C', '#5A5044'], '#2E2822'))
    R.walls('#5A6A64', '#4E5C56', '#4A3E34', trim='#6A5A48', dark=(.8, .92))
    peel(R, 'L'); peel(R, 'R')
    R.window('L', 40, w=18, glass=('#1A2238', '#26304E', '#4A5878')); curtain_torn(R, 'L', 40)
    med_cabinet(R, 'R', 24, broken=True); cross_sign(R, 'R', 62, faded=True, tilt=.25)
    R.window('R', 88, w=18, glass=('#1A2238', '#26304E', '#4A5878')); curtain_torn(R, 'R', 88)
    cobweb(R, 'R', 0, R.WALL - 22); cobweb(R, 'L', R.NY * 8 - 22, R.WALL - 22)
    for i, x in enumerate((3.5, 7.8, 12.1)):
        R.obj('bed', [(int(x), 1), (int(x), 2)], bed(R, x, .4, frame='#8A8A88', blanket='#B8A880', sheet='#D8D0B8', bare=(i == 2), mess=(i == 0)),
              act=('낡은 침대', '구경하기') if i != 1 else ('가운데 침대', '살펴보기'))
    R.obj('screen', [(6, 3), (6, 4)], screen(R, 6.3, .5, col='#A8A090', torn=True, along='y', n=2.2), solid=False)
    R.obj('sink', [(16, 1)], sink(R, 16, 1, old=True))
    R.obj('stool', [(9, 6)], stool(R, 9, 6, fallen=True), solid=False)
    for (x, y) in ((3, 8), (13, 7), (6, 10)): R.obj('clutter', [(x, y)], clutter(R, x, y), solid=False)
    R.light(8.5, 2, -24, 30, [180, 200, 255], .3, 1)
    R.extra = dict(night=True)
    R.save('old_infirmary', '낡은 양호실', '100 년 동안 닫혀 있던 방', [14, 1])
    return R


def gift_shelf(R, side, u0):   # 누비 선반: 학생들이 준 선물 (목도리 · 단추 · 담요 · 브로치 · 털실 공 · 베개)
    COL = ['#E86A6A', '#6AA8E8', '#F0C040', '#8AD08A', '#C88AE8', '#F4A0C0', '#7AD8D8', '#F0A060']
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < 40 and 26 <= v < 64): return None
        if v in (26, 27, 44, 45) : return hexc('#8A5A34')
        if uu in (0, 1, 38, 39): return hexc('#6A4228')
        row = 0 if v < 44 else 1; k = uu // 6 + row * 7; vv = (v - 28) if row == 0 else (v - 46)
        if uu % 6 in (1, 2, 3, 4) and 2 <= vv <= 12:
            c = hexc(COL[k % len(COL)])
            kind = k % 6
            if kind == 0 and vv > 6: return c                                   # 목도리 (아래 늘어짐)
            if kind == 1 and (uu % 6 - 2.5) ** 2 + (vv - 9) ** 2 < 4: return c   # 단추
            if kind == 2 and vv > 5: return shade(c, .8 if (uu + vv) % 2 else 1)  # 조각 담요
            if kind == 3 and (uu % 6 - 2.5) ** 2 + (vv - 8) ** 2 < 3: return c   # 브로치
            if kind == 4 and (uu % 6 - 2.5) ** 2 + (vv - 9) ** 2 < 5: return c   # 털실 공
            if kind == 5 and vv > 7: return hexc('#FFFFFF') if vv == 8 else c    # 베개
        return None
    R.wall_fill(side, f)
    R.wall_fill(side, hexc('#F4E8C8'), u0 + 12, u0 + 28, 66, 72); R.wall_fill(side, hexc('#8A5A34'), u0 + 13, u0 + 27, 68, 70)   # 이름표 판

def warm_room():
    R = Room(NX, NY, wall=80)
    R.exit_to, R.exit_label = 'lab', '물약 교실'
    R.floor(planks(['#B8865A', '#AC7C52', '#C08E60', '#B28256'], '#7A5234'))
    R.walls('#F4E2CC', '#EAD2B8', '#A8784E', trim='#E8B880')
    R.window('L', 40, w=18, glass=('#F0B060', '#F8D088', '#FFF0C8'), frame='#8A5A34', moon=False); curtains(R, 'L', 40, w=18, col='#E8A0B0')
    med_cabinet(R, 'R', 24); cross_sign(R, 'R', 66)
    R.window('R', 88, w=18, glass=('#F0B060', '#F8D088', '#FFF0C8'), frame='#8A5A34', moon=False); curtains(R, 'R', 88, w=18, col='#E8A0B0')
    for i, x in enumerate((3.5, 7.8, 12.1)):
        R.obj('bed', [(int(x), 1), (int(x), 2)], bed(R, x, .4, frame='#F4F0E8', blanket=['#F0A0A8', '#9AC8E8', '#F4D088'][i], sheet='#FFFFFF'),
              act=('따뜻한 침대', '누워서 쉬기') if i != 1 else ('누비 침대', '누비 옆에 앉기'))
    R.obj('sink', [(16, 1)], sink(R, 16, 1))
    R.obj('stool', [(9, 6)], stool(R, 9, 6))
    for (x, y) in ((1, 12), (16, 12)): R.obj('plant', [(x, y)], plant_draw(R, x, y, '#4E8A5E', '#F8C4D0'))
    R.light(8.5, 2, -24, 44, [255, 200, 140], .45, 1); R.light(4, 9, -30, 30, [255, 190, 120], .3, 1)
    R.save('warm_infirmary', '따뜻한 양호실', '누비가 지키는 방', [14, 1])
    return R

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('out', exist_ok=True)
    rooms = [('old_infirmary', old_room()), ('warm_infirmary', warm_room())]
    ims = []
    for key, R in rooms:
        bg = Image.open('out/%s_bg.png' % key).convert('RGBA'); sh = Image.open('out/%s_obj.png' % key).convert('RGBA')
        import json; meta = json.load(open('out/%s.json' % key))
        for o in sorted(meta['objs'], key=lambda o: o['box'][1] + o['box'][0]):
            if o['sw']: bg.alpha_composite(sh.crop((o['sx'], o['sy'], o['sx'] + o['sw'], o['sy'] + o['sh'])), (o['x'], o['y']))
        if key in ('old_infirmary', 'warm_infirmary'):   # 가운데 침대 위 누비
            fr = 0 if key == 'old_infirmary' else 8
            nb = Image.open('../../public/art/nubi_s.png').convert('RGBA').crop((fr * 32, 0, fr * 32 + 32, 32)); x, y = R.P(8.45, 1.6); bg.alpha_composite(nb, (int(x) - 16, int(y) - 41))
            if key == 'old_infirmary': bg.alpha_composite(Image.new('RGBA', bg.size, (10, 6, 24, 90)))
        ims.append(bg)
    W = sum(i.width for i in ims); H = max(i.height for i in ims); pv = Image.new('RGBA', (W, H), hexc('#140D1E')); x = 0
    for i in ims: pv.alpha_composite(i, (x, 0)); x += i.width
    pv.resize((W * 2, H * 2), Image.NEAREST).save('../nubi_mock/infirmary_prev.png'); print('prev ok')
