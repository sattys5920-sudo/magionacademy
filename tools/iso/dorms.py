# 기숙사 휴게실: 기숙사마다 분위기가 다른 공용 휴게실 6단계 (dorm_{kind}_{n}) + 개인 방 (myroom_{kind})
# 기숙사생이 함께 재료를 모으면 단계가 올라가며 방이 넓어지고 꾸며져요. 게임에서 단계에 맞는 방을 골라 보여 줘요.
# python3 interiors.py 가 끝에 dorms.main()을 불러요 (따로: python3 -c "import dorms; dorms.main()")
import math
from interiors import *
SIZES = [(10, 8, 62), (12, 9, 66), (14, 10, 70), (16, 12, 74), (19, 14, 78), (22, 16, 84)]
KIND = {'ember': 'witch', 'moon': 'vamp', 'dusk': 'wolf', 'dew': 'ghost'}   # 기숙사 → 지도 이름
# ---------- 벽 ----------
def walls_style(R, T, dull):
    paper, paper2, wain, trim = (T['dull'] if dull else (T['paper'], T['paper2'], T['wain'], T['trim']))
    st = 'paper' if dull else T['wall']
    if st == 'paper': return R.walls(paper, paper2, wain, trim=trim)
    R.walls(paper, paper2, wain, trim=trim)
    for side, dk in (('L', .86), ('R', 1.0)):
        def f(u, v, dk=dk):
            if v < 24 or v >= R.WALL - 4: return None
            if st == 'logs':      # 통나무 벽
                k, r = (v - 24) // 8, (v - 24) % 8
                c = hexc(paper if k % 2 else paper2)
                c = shade(c, [.62, .85, 1.08, 1.12, 1.05, .98, .88, .7][r])
                if (u + k * 37) % 53 in (0, 1) and 2 < r < 6: c = hexc('#C8A070')
                return shade(c, dk)
            if st == 'stone':     # 돌 블록 벽
                row = (v - 24) // 9; off = (row % 2) * 7
                if (v - 24) % 9 == 0 or (u + off) % 14 == 0: return shade(hexc(paper2), dk * .7)
                return shade(hexc(paper), dk * (.9 + .1 * (((u + off) // 14 + row) % 3) / 2))
            if st == 'damask':    # 붉은 다마스크
                a, b = u % 16, (v - 24) % 18
                c = hexc(paper)
                if abs(a - 8) + abs(b - 9) in (6, 7) or (abs(a - 8) < 2 and abs(b - 9) < 3): c = hexc(paper2)
                if a == 0: c = shade(hexc(paper), .8)
                return shade(c, dk * (.82 + .18 * v / R.WALL))
        R.wall_fill(side, f)

# ---------- 공통 소품 ----------
def banner(R, side, u0, col, emb='#F2D27A', w=14):
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < w and 30 <= v < 64): return None
        if v < 32: return hexc('#C49446')
        if v < 30 + abs(uu - w / 2 + .5) * .9 + 2: return None
        if (uu - w / 2 + .5) ** 2 + (v - 48) ** 2 < 12: return hexc(emb)
        return shade(hexc(col), .8 if uu < 2 else 1)
    R.wall_fill(side, f)
def crest(R, side, u0, col, v0=50, big=False):
    rr = 11 if big else 8
    def f(u, v):
        d2 = (u - u0) ** 2 + (v - v0) ** 2
        if d2 < rr * rr:
            if d2 > (rr - 2) ** 2: return hexc('#E8C060')
            if abs(u - u0) < 2 and abs(v - v0) < rr - 4 or abs(v - v0 - 2) < 1.5 and abs(u - u0) < rr - 5: return hexc('#F6E6A8')
            return hexc(col)
    R.wall_fill(side, f)
def hearth(R, T, u0, big=False):
    W_, H_ = (40, 50) if big else (28, 40); f1, f2, lc = T['fire']; stone = T['hearth']
    def f(u, v):
        uu = u - u0
        if not (0 <= uu < W_ and 0 <= v < H_): return None
        if v >= H_ - 6: return hexc('#E8C060') if big and v == H_ - 1 else shade(hexc(stone), .85) if v < H_ - 2 else shade(hexc(stone), 1.1)
        if uu < 3 or uu >= W_ - 3: return shade(hexc(stone), .75 + .1 * ((v // 6 + uu) % 2))
        if v < 3: return shade(hexc(stone), .55)
        if v < H_ // 2 and 5 <= uu < W_ - 5:
            fl = (uu * 7 + v * 3) % 5
            return hexc(f1) if v < 6 + fl else hexc(f2) if v < 9 + fl // 2 and W_ // 3 <= uu < W_ * 2 // 3 else hexc('#1A1420')
        return hexc('#1A1420')
    R.wall_fill('R', f); x, y = R.wall_px('R', u0 + W_ / 2, 10); R.lights.append(dict(p=(x, y), dy=0, r=48 if big else 38, c=lc, a=.6, f=1))
    return u0 + W_
def web(R, side, u0):
    def f(u, v):
        uu, vv = u - u0, R.WALL - 4 - v
        if 0 <= uu < 12 and 0 <= vv < 12 and (uu == vv or uu == 0 or vv == 0 or (uu + vv) in (6, 11)): return hexc('#B8B0C8')
    R.wall_fill(side, f)
def curtains(R, side, u0, w=16, col='#8A1E2E'):
    def f(u, v):
        uu = u - u0
        if 24 <= v < R.WALL - 6 and (-6 <= uu < -1 or w + 1 <= uu < w + 6):
            return shade(hexc(col), .75 if (uu % 3 == 0) else 1.0)
        if R.WALL - 9 <= v < R.WALL - 5 and -6 <= uu < w + 6: return hexc('#C49446')
    R.wall_fill(side, f)
def vines(R, side, u0, u1):
    def f(u, v):
        if not (u0 <= u < u1 and v > R.WALL - 20): return None
        h = 6 + int(8 * (1 + math.sin(u * .7)) / 2) + (u * 13 % 7)
        if R.WALL - 4 - v < h and (u * 7 + v) % 3: return hexc('#5E9A5A') if (u + v) % 5 else hexc('#E8F0FF')
    R.wall_fill(side, f)
def sofa(R, tx, ty, n, col):
    rd = hexc(col)
    def f(img, d):
        R.box(img, tx, ty + .2, n, .8, 6, rd, shade(rd, .6), shade(rd, .8)); R.box(img, tx, ty + .75, n, .25, 13, shade(rd, 1.1), shade(rd, .6), shade(rd, .8))
    R.obj('sofa', [(tx + i, ty) for i in range(n)], f)
def armchair(R, tx, ty, col):
    rd = hexc(col)
    def f(img, d):
        R.box(img, tx, ty + .2, 1, .8, 6, rd, shade(rd, .6), shade(rd, .8)); R.box(img, tx, ty + .75, 1, .25, 14, shade(rd, 1.1), shade(rd, .6), shade(rd, .8))
        for xx in (-.05, .9): R.box(img, tx + xx, ty + .2, .15, .8, 9, shade(rd, .9), shade(rd, .55), shade(rd, .7))
    R.obj('arm', [(tx, ty)], f)
def statue(R, tx, ty, body='#B4AEC0'):
    def f(img, d):
        R.box(img, tx + .1, ty + .1, .8, .8, 8, '#8A8494', '#5E5868', '#74707E')
        cx, cy = R.P(tx + .5, ty + .5); cy -= 8
        d.polygon([(cx - 5, cy), (cx + 5, cy), (cx + 3, cy - 14), (cx - 3, cy - 14)], fill=hexc(body))
        d.ellipse([cx - 4, cy - 21, cx + 4, cy - 13], fill=shade(hexc(body), 1.08)); d.polygon([(cx - 6, cy - 19), (cx + 6, cy - 19), (cx, cy - 32)], fill=shade(hexc(body), .85))
    R.obj('statue', [(tx, ty)], f)
def chandelier(R, tx, ty, metal='#E8C060', glow=(255, 200, 140), crystal=False):
    def f(img, d):
        cx, cy = R.P(tx, ty); cy -= 70
        d.line([(cx, cy - 30), (cx, cy)], fill=hexc('#C49446'))
        d.ellipse([cx - 16, cy - 3, cx + 16, cy + 5], outline=hexc(metal), width=2)
        for dx in (-14, -7, 0, 7, 14):
            if crystal: d.polygon([(cx + dx, cy + 3), (cx + dx - 2, cy + 8), (cx + dx, cy + 12), (cx + dx + 2, cy + 8)], fill=hexc('#C8F0FF'))
            d.rectangle([cx + dx - 1, cy - 7, cx + dx, cy - 1], fill=hexc('#F2E6C8')); d.point((cx + dx, cy - 8), fill=hexc('#FFE07A'))
    R.obj('chand', [(int(tx), int(ty))], f, solid=False); R.lights.append(dict(p=R.P(tx, ty), dy=-70, r=70, c=list(glow), a=.5, f=1))
def lantern(R, tx, ty, col=(255, 190, 110), glass='#FFD27A', h=40):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); cy -= h
        d.rectangle([cx - 3, cy - 5, cx + 3, cy + 4], fill=hexc('#2A2030')); d.rectangle([cx - 2, cy - 4, cx + 2, cy + 3], fill=hexc(glass)); d.polygon([(cx - 4, cy - 5), (cx + 4, cy - 5), (cx, cy - 9)], fill=hexc('#2A2030'))
    R.obj('lantern', [(tx, ty)], f, solid=False); R.lights.append(dict(p=R.P(tx + .5, ty + .5), dy=-h, r=26, c=list(col), a=.55, f=1))
def potion_shelf(R, side, u0, w=26):
    R.shelf(side, u0, w, 40, ['#C86AE8', '#6AD8A8', '#FF7A5C', '#5AA8FF', '#FFE07A', '#3E2216'])
def cauldron(R, tx, ty, brew, big=False):
    R.obj('cauldron', [(tx, ty)], cauldron_draw(R, tx, ty, brew, 1.4 if big else 1.0)); R.light(tx + .5, ty + .5, -10, 30 if big else 22, list(hexc(brew)[:3]), .5)
def broom_rack(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); d.rectangle([cx - 10, cy - 30, cx + 10, cy - 28], fill=hexc('#5E3826'))
        for k in range(3):
            x = cx - 7 + k * 7; d.line([(x, cy - 30), (x, cy - 8)], fill=hexc('#8A5A3A'), width=2); d.polygon([(x - 3, cy - 10), (x + 3, cy - 10), (x + 4, cy), (x - 4, cy)], fill=hexc('#C8A84A'))
    R.obj('brooms', [(tx, ty)], f)
def crystal_ball(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); R.box(img, tx + .2, ty + .2, .6, .6, 8, '#5E3826', '#3E2216', '#4A2A1C')
        d.ellipse([cx - 5, cy - 22, cx + 5, cy - 12], fill=hexc('#B88AFF')); d.ellipse([cx - 3, cy - 20, cx, cy - 17], fill=hexc('#F2E8FF'))
    R.obj('ball', [(tx, ty)], f); R.light(tx + .5, ty + .5, -17, 22, [190, 140, 255], .5)
def kiln(R, tx, ty):   # 엠버킬른의 가마
    def f(img, d):
        R.box(img, tx, ty, 2, 1.4, 20, '#7A5A50', '#5A3E36', '#6A4A42'); R.box(img, tx + .6, ty - .1, .8, .6, 34, '#6A4A42', '#4A302A', '#5A3E36', lift=0)
        x, y = R.P(tx + 1, ty + 1.4); d.ellipse([x - 6, y - 14, x + 6, y - 4], fill=hexc('#2A1410')); d.ellipse([x - 4, y - 11, x + 4, y - 5], fill=hexc('#FF8A3A')); d.ellipse([x - 2, y - 9, x + 2, y - 6], fill=hexc('#FFE07A'))
    R.obj('kiln', [(tx, ty), (tx + 1, ty)], f); R.light(tx + 1, ty + 1.4, -9, 34, [255, 140, 60], .6)
def worktable(R, tx, ty):
    def f(img, d):
        R.box(img, tx, ty + .1, 2, .8, 10, '#7A4A2E', '#4A2A1C', '#5E3826')
        for k, c in enumerate(('#C86AE8', '#6AD8A8', '#FF7A5C', '#5AA8FF')):
            x, y = R.P(tx + .3 + k * .45, ty + .5); y -= 10; d.rectangle([x - 1, y - 6, x + 1, y], fill=hexc(c)); d.point((x, y - 7), fill=hexc('#F2E6C8'))
    R.obj('work', [(tx, ty), (tx + 1, ty)], f)
def coffin(R, tx, ty, polished=False):
    def f(img, d):
        R.box(img, tx + .1, ty, .9, 2.2, 8, '#5A1E2E' if polished else '#3A2A2E', '#2A1218', '#341820')
        cx, cy = R.P(tx + .55, ty + 1.1); cy -= 8; c = '#E8C060' if polished else '#8A7A6A'
        d.line([(cx, cy - 4), (cx, cy + 3)], fill=hexc(c)); d.line([(cx - 2, cy - 1), (cx + 2, cy - 1)], fill=hexc(c))
    R.obj('coffin', [(tx, ty), (tx, ty + 1)], f)
def candelabra(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); d.rectangle([cx - 1, cy - 18, cx, cy], fill=hexc('#C49446')); d.line([(cx - 5, cy - 18), (cx + 5, cy - 18)], fill=hexc('#C49446'))
        for dx in (-5, 0, 5): d.rectangle([cx + dx - 1, cy - 24, cx + dx, cy - 18], fill=hexc('#F2E6C8')); d.point((cx + dx, cy - 25), fill=hexc('#FFD27A'))
    R.obj('candelabra', [(tx, ty)], f); R.light(tx + .5, ty + .5, -24, 26, [255, 170, 100], .55)
def roses(R, tx, ty):
    def f(img, d):
        R.box(img, tx + .1, ty + .1, .8, .8, 9, '#3A1E2A', '#2A1218', '#341820'); cx, cy = R.P(tx + .5, ty + .5); cy -= 9
        d.rectangle([cx - 2, cy - 7, cx + 1, cy], fill=hexc('#C8D8E8'))
        for dx, dy in ((-3, -10), (2, -11), (0, -14), (-1, -9)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=hexc('#D02040'))
    R.obj('roses', [(tx, ty)], f)
def chest(R, tx, ty, gold=False):
    def f(img, d):
        R.box(img, tx + .1, ty + .2, .9, .7, 8, '#7A4A2E', '#4A2A1C', '#5E3826'); R.box(img, tx + .1, ty + .2, .9, .7, 2, '#C49446', '#8A6A2E', '#A8823A', lift=8)
        if gold: x, y = R.P(tx + .5, ty + .3); d.ellipse([x - 4, y - 14, x + 4, y - 9], fill=hexc('#F6D24A'))
    R.obj('chest', [(tx, ty)], f)
def piano(R, tx, ty):
    def f(img, d):
        R.box(img, tx, ty, 2, 1, 12, '#2A1C2A', '#1A1018', '#24161E'); R.box(img, tx, ty + .7, 2, .3, 13, '#F2EEE4', '#C8C4BC', '#E0DCD4'); R.box(img, tx, ty, 2, .25, 22, '#2A1C2A', '#1A1018', '#24161E')
    R.obj('piano', [(tx, ty), (tx + 1, ty)], f)
def throne(R, tx, ty):
    def f(img, d):
        R.box(img, tx, ty + .2, 1, .8, 7, '#8A1E2E', '#5A1018', '#6E1622'); R.box(img, tx, ty + .75, 1, .25, 26, '#8A1E2E', '#5A1018', '#6E1622')
        x, y = R.P(tx + .5, ty + .9); d.ellipse([x - 3, y - 30, x + 3, y - 25], fill=hexc('#E8C060'))
    R.obj('throne', [(tx, ty)], f)
def logs(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        for k in range(3): d.ellipse([cx - 8 + k * 5, cy - 6 - (k == 1) * 4, cx - 2 + k * 5, cy - (k == 1) * 4], fill=hexc('#7A5232')); d.ellipse([cx - 6 + k * 5, cy - 5 - (k == 1) * 4, cx - 4 + k * 5, cy - 2 - (k == 1) * 4], fill=hexc('#C8A878'))
    R.obj('logs', [(tx, ty)], f)
def hay(R, tx, ty): R.obj('hay', [(tx, ty)], lambda img, d: R.box(img, tx + .1, ty + .1, .8, .8, 7, '#D8B85A', '#A8883A', '#C0A04A'))
def stump(R, tx, ty):
    def f(img, d):
        R.box(img, tx + .25, ty + .25, .5, .5, 7, '#C8A878', '#6A4428', '#7A5232')
    R.obj('stump', [(tx, ty)], f)
def log_table(R, tx, ty):
    def f(img, d): R.box(img, tx, ty + .1, 1.6, .9, 9, '#A8784A', '#5E3E22', '#7A5232'); x, y = R.P(tx + .8, ty + .5); d.ellipse([x - 3, y - 13, x + 2, y - 10], fill=hexc('#F2EEE4'))
    R.obj('ltable', [(tx, ty), (tx + 1, ty)], f)
def pet_bed(R, tx, ty, col='#C86A4A'):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); d.ellipse([cx - 9, cy - 5, cx + 9, cy + 4], fill=hexc(col)); d.ellipse([cx - 6, cy - 3, cx + 6, cy + 2], fill=hexc('#F2E2C4'))
        d.line([(cx - 3, cy - 1), (cx + 3, cy - 1)], fill=hexc('#FFFFFF'), width=2)
    R.obj('petbed', [(tx, ty)], f, solid=False)
def fur_rug(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + 1, ty + 1); d.ellipse([cx - 18, cy - 8, cx + 18, cy + 8], fill=hexc('#B8A890')); d.ellipse([cx - 14, cy - 5, cx + 14, cy + 5], fill=hexc('#D8CAB0'))
    R.obj('fur', [(tx, ty)], f, solid=False)
def herbs_hang(R, side, u0, u1):
    def f(u, v):
        if u0 <= u < u1:
            if v == R.WALL - 10: return hexc('#5E3826')
            k = (u - u0) % 8
            if k in (3, 4) and R.WALL - 20 < v < R.WALL - 10: return hexc(['#6AAE5A', '#C8A84A', '#A86AE8'][(u - u0) // 8 % 3])
    R.wall_fill(side, f)
def big_moon_window(R, side, u0):
    R.window(side, u0, w=26, h=38, glass=('#2A3A5E', '#3A4E78', '#F2E8B0'))
def antlers(R, side, u0):
    def f(u, v):
        uu, vv = u - u0, v - 52
        if abs(uu) < 4 and -4 < vv < 3: return hexc('#7A5232')
        for s in (-1, 1):
            if 0 < s * uu < 14 and abs(vv - (s * uu) * .5) < 1.2: return hexc('#E8DCC0')
            if s * uu in (5, 10) and 0 <= vv - s * uu * .5 < 6: return hexc('#E8DCC0')
    R.wall_fill(side, f)
def chains(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5)
        for j in range(6): d.ellipse([cx - 2 + (j % 2), cy - 56 + j * 4, cx + 1 + (j % 2), cy - 52 + j * 4], outline=hexc('#B8C8E8'))
    R.obj('chains', [(tx, ty)], f, solid=False)
def mirror(R, tx, ty, clean=False):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); d.rectangle([cx - 6, cy - 26, cx + 6, cy], fill=hexc('#C49446' if clean else '#7A6A5A')); d.rectangle([cx - 4, cy - 24, cx + 4, cy - 2], fill=hexc('#A8C8E8' if clean else '#6A7A8A'))
        d.line([(cx - 2, cy - 20), (cx + 2, cy - 16)], fill=hexc('#E8F4FF'))
    R.obj('mirror', [(tx, ty)], f)
def wisp(R, tx, ty, h=34):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); cy -= h; d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=hexc('#C8F0FF')); d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=hexc('#FFFFFF'))
    R.obj('wisp', [(tx, ty)], f, solid=False); R.lights.append(dict(p=R.P(tx + .5, ty + .5), dy=-h, r=24, c=[140, 210, 255], a=.6, f=1))
def fountain(R, tx, ty):
    def f(img, d):
        R.box(img, tx, ty, 2, 2, 6, '#9AB0C0', '#6A8090', '#7A90A0'); R.box(img, tx + .2, ty + .2, 1.6, 1.6, 1, '#6AB8E8', '#4A88B8', '#5A98C8', lift=5)
        R.box(img, tx + .8, ty + .8, .4, .4, 18, '#B0C4D0', '#7A90A0', '#8AA0B0')
        x, y = R.P(tx + 1, ty + 1); y -= 20
        for dx in (-6, -3, 3, 6): d.line([(x, y), (x + dx, y + 10)], fill=hexc('#C8F0FF'))
    R.obj('fountain', [(tx, ty), (tx + 1, ty), (tx, ty + 1), (tx + 1, ty + 1)], f); R.light(tx + 1, ty + 1, -10, 30, [140, 210, 255], .4)
def can(R, tx, ty):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); d.rectangle([cx - 4, cy - 7, cx + 3, cy], fill=hexc('#6A9AB8')); d.line([(cx + 3, cy - 5), (cx + 8, cy - 9)], fill=hexc('#6A9AB8'), width=2); d.arc([cx - 3, cy - 12, cx + 2, cy - 4], 180, 360, fill=hexc('#4A7A98'))
    R.obj('can', [(tx, ty)], f, solid=False)
def tree(R, tx, ty, leaf='#4E8A4A', leaf2='#6AAE5A', glow=None):
    def f(img, d):
        cx, cy = R.P(tx + .5, ty + .5); R.box(img, tx + .1, ty + .1, .8, .8, 6, '#8A8494', '#5E5868', '#74707E')
        d.rectangle([cx - 2, cy - 26, cx + 1, cy - 6], fill=hexc('#6A4428'))
        for dx, dy, r in ((-8, -34, 9), (7, -35, 9), (0, -44, 10), (-2, -28, 8)): d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=hexc(leaf))
        for dx, dy in ((-6, -38), (4, -46), (8, -30)): d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=hexc(glow or leaf2))
    R.obj('tree', [(tx, ty)], f)

# ---------- 기숙사 4곳 ----------
TH = {
  'ember': dict(title='Emberkiln · 마녀관', mood='실험광들의 보랏빛 실험 휴게실 — 솥, 물약 선반, 불타는 가마', HC='#F08A3C', wall='paper',
                paper='#3A2A5E', paper2='#4A3A72', wain='#4C2B1C', trim='#C49446', dull=('#3A3040', '#3E3446', '#3E2A20', '#6A5A4A'),
                floor=lambda n: planks(['#6E412B', '#5F3624', '#7A4A31', '#663C28']) if n < 4 else checker('#6E412B', '#4A2E40'),
                rug='#5A3A9A', rug2='#F08A3C', sofa='#6A3AA8', fire=('#C86AE8', '#F2B8FF', [200, 120, 255]), hearth='#6A6470', glass=('#28406E', '#3D62A0', '#7FA6E0')),
  'moon':  dict(title='Moonhollow · 뱀파이어관', mood='밤의 장사꾼들의 붉은 고딕 살롱 — 벨벳, 관, 촛대, 피아노, 금화 상자', HC='#B0203A', wall='damask',
                paper='#4A1E2A', paper2='#6A2A3A', wain='#2A1E24', trim='#C49446', dull=('#3A2A30', '#3E2E34', '#2A1E24', '#5A4A4A'),
                floor=lambda n: checker('#3A2E36', '#2A2028') if n < 4 else checker('#4A3A44', '#1E161C'),
                rug='#8A1E2E', rug2='#E8C060', sofa='#8A1E2E', fire=('#FF6A3A', '#FFC07A', [255, 120, 70]), hearth='#4A3E48', glass=('#5A1E2E', '#8A2A3A', '#E8A0B0')),
  'dusk':  dict(title='Duskfold · 늑대관', mood='돌봄이들의 숲속 오두막 — 통나무 벽, 돌 벽난로, 털 러그, 반려동물 방석', HC='#5E8A3A', wall='logs',
                paper='#7A5232', paper2='#8A6040', wain='#5A3A24', trim='#A8784A', dull=('#4A3A2E', '#4E3E32', '#4A3220', '#6A5A4A'),
                floor=lambda n: planks(['#A8784A', '#98683E', '#B08050', '#9E7044'], '#5E3E22'),
                rug='#6A8A4A', rug2='#E8709A', sofa='#7A5A3A', fire=('#FF8A3A', '#FFE07A', [255, 150, 60]), hearth='#7A7480', glass=('#2A3A5E', '#3A4E78', '#9AB8E0')),
  'dew':   dict(title='Dewmorn · 유령관', mood='정원사들의 안개 낀 유리 정원 — 푸른 도깨비불, 화분과 덩굴, 분수', HC='#4AA8A0', wall='stone',
                paper='#5A7A8A', paper2='#3E5A68', wain='#4A5A6A', trim='#A8C8D8', dull=('#4A5A66', '#4E5E6A', '#3E4A56', '#6A7A86'),
                floor=lambda n: checker('#6A808E', '#5E7482') if n < 4 else checker('#7A92A0', '#5A7080'),
                rug='#8AB8C8', rug2='#5CCB8E', sofa='#5A8AA0', fire=('#6AB8FF', '#C8E8FF', [120, 180, 255]), hearth='#8A98A8', glass=('#3E6A7A', '#5A8E9E', '#C8F0FF')),
}
NAMES = {
  'ember': ['먼지 쌓인 창고', '불 붙은 벽난로', '물약 선반', '수정구와 빗자루', '불타는 가마', '전설의 실험실'],
  'moon':  ['낡은 관이 있는 방', '붉은 커튼', '벨벳 살롱', '금화 상자', '달빛 피아노', '밤의 왕좌'],
  'dusk':  ['장작 창고', '돌 벽난로', '숲 냄새 나는 방', '반려동물 방석', '큰 달 창문', '전설의 오두막'],
  'dew':   ['쇠사슬 소리', '푸른 도깨비불', '첫 화분', '떠다니는 도깨비불', '안개 분수', '전설의 유리 정원'],
}
def build(key, n):
    """휴게실 한 단계를 그려서 Room으로 돌려줘요"""
    T = TH[key]; NX, NY, WALL = SIZES[n - 1]; R = Room(NX, NY, WALL)
    # 바닥과 벽
    fl = T['floor'](n) if n > 1 else planks(['#5A3A2A', '#4E3224', '#604030', '#553626'])
    if key == 'dew' and n == 1: fl = checker('#5A6A76', '#52626E')
    if key == 'moon' and n == 1: fl = checker('#3A2E36', '#32282E')
    if n >= 2:
        rx0, ry0, rx1, ry1 = 3, max(3, NY // 2 - 2 + (n < 3)), NX - 4, NY - 2
        fl = rug(fl, rx0, ry0, rx1, ry1, T['rug'], border='#E8C060' if n == 6 else '#C49446', inner=T['rug2'] if n >= 4 else None)
    R.floor(fl); walls_style(R, T, n == 1)
    RW, LW = NX * 8, NY * 8
    # 창문
    glass = T['glass']
    R.window('R', 14, glass=glass)
    if n >= 3: R.window('R', RW - 24, glass=glass)
    if n >= 5: R.window('R', 34, glass=glass)
    # 벽난로 (2단계부터)
    hu = 40 if n < 4 else 54 if n < 6 else 70
    if n >= 2:
        hend = hearth(R, T, hu, big=n == 6)
        if n == 6: crest(R, 'R', hu + 20, T['HC'], v0=62, big=True)
    else: web(R, 'R', 0); web(R, 'L', LW - 12)
    # 벽 촛대
    R.sconce('L', 14 if n > 1 else 30)
    if n >= 2: R.sconce('R', hu - 8)
    if n >= 4: R.sconce('L', LW - 20)
    # 깃발과 문장 (4단계부터)
    if n >= 4:
        banner(R, 'R', (hend + 6) if n < 6 else 54, T['HC']); crest(R, 'L', LW // 2, T['HC'])
    if n >= 5: banner(R, 'R', RW - 46, T['HC'])
    if n == 6: banner(R, 'R', hend + 6, T['HC'])
    if n >= 3: garland(R, 'R', hu - 2, hu + 32, WALL - 4, (T['HC'], '#E07A1E', '#2A2030'))
    # 자리 (2단계 작은 소파 → 6단계 소파 둘 + 안락의자)
    if n >= 2: sofa(R, 4, NY - 1, 2 if n == 2 else 3, T['sofa'])
    if n >= 5: sofa(R, NX - 7, NY - 1, 2 if n == 5 else 3, T['sofa'])
    if n >= 4: armchair(R, 2, NY - 5, T['HC']); armchair(R, NX - 4, NY - 5, T['HC'])
    if n >= 3:
        if key == 'dusk': log_table(R, NX // 2 - 1, NY // 2 + 1); stump(R, NX // 2 - 2, NY // 2 + 1); stump(R, NX // 2 + 1, NY // 2 + 1)
        else:
            R.obj('table', [(NX // 2 - 1, NY // 2 + 1)], table_draw(R, NX // 2 - 1, NY // 2 + 1, '#8A5636', ('cup', 'cake')))
            R.obj('chair', [(NX // 2 - 3, NY // 2 + 1)], chair_draw(R, NX // 2 - 3, NY // 2 + 1, T['sofa'])); R.obj('chair', [(NX // 2 + 1, NY // 2 + 1)], chair_draw(R, NX // 2 + 1, NY // 2 + 1, T['sofa']))
    if n >= 5: chandelier(R, NX // 2 - 1, NY // 2, **({'crystal': True, 'glow': (170, 220, 255), 'metal': '#C8E0F0'} if key == 'dew' else {}))
    if n == 6: chandelier(R, NX // 2 + 4, NY // 2, **({'crystal': True, 'glow': (170, 220, 255), 'metal': '#C8E0F0'} if key == 'dew' else {}))
    # ---- 기숙사마다 다른 것 ----
    if key == 'ember':
        if n == 1: R.obj('crates', [(1, 1)], crates(R, 1, 1, 3)); R.obj('crates', [(NX - 3, NY - 3)], crates(R, NX - 3, NY - 3, 1)); cauldron(R, 1, 4, '#5A5060')
        else: cauldron(R, 1, 4, '#C08AFF', big=n >= 5)
        if n >= 3: potion_shelf(R, 'L', 30); bookshelf(R, 'L', 4)
        if n >= 4: crystal_ball(R, NX - 2, 2); broom_rack(R, 1, 1)
        if n >= 5: kiln(R, NX - 5, 1); worktable(R, 1, NY - 3)
        if n == 6: potion_shelf(R, 'L', 60); cauldron(R, NX - 2, NY - 7, '#6AD8A8'); statue(R, NX - 2, NY - 3, '#B4A8D8')
        for (x, y) in [(4, 4), (NX - 5, 5), (NX // 2, 3)][: max(0, n - 2)]: float_candle(R, x, y)
    elif key == 'moon':
        coffin(R, 1, 2, polished=n >= 4)
        if n == 1: web(R, 'L', 20)
        if n >= 2: curtains(R, 'R', 14, col='#8A1E2E'); candelabra(R, 1, NY - 3)
        if n >= 3: bookshelf(R, 'L', 30); roses(R, NX - 2, 2); curtains(R, 'R', RW - 24, col='#8A1E2E')
        if n >= 4: chest(R, 1, 6, gold=True); chest(R, NX - 2, 4, gold=True); candelabra(R, NX - 2, NY - 3)
        if n >= 5: piano(R, NX - 6, 1); curtains(R, 'R', 34, col='#8A1E2E'); R.window('L', LW // 2 - 30, w=20, h=36, glass=('#5A1E2E', '#C8A0D8', '#F2E8B0'))
        if n == 6: throne(R, NX // 2 + 2, 1); statue(R, 1, NY - 6, '#6A6070'); statue(R, NX - 2, NY - 7, '#6A6070'); roses(R, 3, 1)
    elif key == 'dusk':
        logs(R, 1, 1); hay(R, 2, 1)
        if n == 1: logs(R, NX - 2, NY - 3)
        if n >= 2: fur_rug(R, NX // 2 - 1, NY - 4)
        if n >= 3:
            for (x, y) in ((NX - 1, NY - 1), (0, NY - 1)): R.obj('plant', [(x, y)], plant_draw(R, x, y, leaf='#4E8A3A', flower='#E8709A'))
            lantern(R, 1, NY // 2, h=30); herbs_hang(R, 'L', 20, 60)
        if n >= 4: pet_bed(R, NX - 3, 3); pet_bed(R, 4, 3, '#6A8A4A'); antlers(R, 'L', LW // 2 + 26)
        if n >= 5: big_moon_window(R, 'L', LW // 2 - 40); lantern(R, NX - 2, NY // 2, h=30); logs(R, NX - 2, 1)
        if n == 6: tree(R, 1, NY - 6); tree(R, NX - 2, NY - 8, leaf='#3E7A3A'); pet_bed(R, NX // 2 + 3, 2, '#E8709A'); herbs_hang(R, 'R', RW - 60, RW - 30)
    elif key == 'dew':
        chains(R, 2, 2); mirror(R, 1, 1, clean=n >= 3)
        if n >= 3:
            for (x, y) in ((NX - 1, NY - 1), (0, NY - 1), (NX - 1, 2)): R.obj('plant', [(x, y)], plant_draw(R, x, y, leaf='#4E8A6A', flower='#C8F0FF'))
            can(R, 2, NY - 2); vines(R, 'L', 0, 40)
        if n >= 4:
            for (x, y) in ((4, 4), (NX - 4, 3), (NX // 2, NY - 4)): wisp(R, x, y)
            vines(R, 'R', 0, 12); vines(R, 'R', RW - 30, RW)
        if n >= 5: fountain(R, NX - 4, 2); R.window('L', LW // 2 - 30, w=24, h=40, glass=glass)
        if n == 6: tree(R, 1, NY - 7, leaf='#4E8A6A', glow='#C8F0FF'); statue(R, NX - 2, NY - 7, '#C8D8E8'); wisp(R, NX // 2 - 3, 4); wisp(R, NX - 3, NY - 3)
    return R

# 눌러서 쓰는 것들
ACTMAP = {'sofa': ('푹신한 소파', '앉아서 쉬기'), 'arm': ('안락의자', '앉아서 쉬기'), 'table': ('티 테이블', '차 마시기'), 'ltable': ('통나무 테이블', '차 마시기'),
          'cauldron': ('기숙사 솥', '들여다보기'), 'ball': ('수정구', '미래 엿보기'), 'brooms': ('빗자루 걸이', '타 보기'), 'kiln': ('불타는 가마', '구경하기'), 'work': ('실험대', '구경하기'),
          'coffin': ('관', '들어가 보기'), 'candelabra': ('촛대', '불 켜기'), 'roses': ('장미 화병', '구경하기'), 'chest': ('금화 상자', '구경하기'), 'piano': ('피아노', '구경하기'), 'throne': ('밤의 왕좌', '앉아서 쉬기'),
          'logs': ('장작더미', '장작 넣기'), 'petbed': ('반려동물 방석', '뒹굴기'), 'stump': ('그루터기 의자', '앉아서 쉬기'), 'mirror': ('거울', '들여다보기'), 'fountain': ('안개 분수', '구경하기'),
          'statue': ('석상', '구경하기'), 'board': ('휴게실 게시판', '휴게실 꾸미기')}
def noticeboard(R, tx, ty, col):
    def f(img, d):
        R.box(img, tx + .35, ty + .35, .3, .3, 12, '#5E3826', '#3E2216', '#4A2A1C')
        R.box(img, tx + .1, ty + .45, .8, .1, 14, '#B88A5A', '#7A5232', '#A07040', lift=12)
        x, y = R.P(tx + .5, ty + .5)
        for k, c in enumerate(('#F2E6C8', '#FFD0DA', col)): d.rectangle([x - 6 + k * 4, y - 23 + (k % 2) * 3, x - 3 + k * 4, y - 19 + (k % 2) * 3], fill=hexc(c))
    R.obj('board', [(tx, ty)], f)
def common_room(key, n):
    T = TH[key]; kind = KIND[key]; R = build(key, n); NX, NY = R.NX, R.NY
    noticeboard(R, NX - 1, NY - 3, T['HC'])
    for o in R.objs:
        if not o['act'] and o['name'] in ACTMAP: o['act'] = ACTMAP[o['name']]
    R.doors.append(dict(tile=[1, NY - 1], to='myroom_' + kind, label='내 방', spawn=[6, 8], house=key))
    if key == 'dew':   # 유령관: 바닥에 옅은 안개
        for y in range(R.H):
            for x in range(R.W):
                fx, fy = R.inv(x, y)
                if 0 <= fx < NX and 0 <= fy < NY:
                    m = max(0, min(1, ((fx + fy) / (NX + NY) - .35) * 1.6)) * (.08 + .025 * n) * (.75 + .25 * math.sin(x / 9 + y / 13))
                    c = R.px[x, y]; R.px[x, y] = tuple(int(c[i] * (1 - m) + (190, 220, 235)[i] * m) for i in range(3)) + (255,)
    R.extra = dict(vw=170 + n * 12, house=key, stage=n)
    R.save(f'dorm_{kind}_{n}', T['title'].split(' · ')[0] + ' 휴게실', f'{n}단계 · {NAMES[key][n - 1]}', DORMS[kind]['spawn'])
def my_room(key):
    """개인 방: 기숙사 분위기의 벽과 바닥, 침대 하나. 가구는 게임에서 놓아요 (furn)"""
    T = TH[key]; kind = KIND[key]; R = Room(12, 10, 70)
    R.floor(T['floor'](4) if key != 'dusk' else T['floor'](1)); walls_style(R, T, False)
    R.window('R', 14, glass=T['glass']); R.window('R', 66, glass=T['glass']); R.window('L', 30, glass=T['glass'])
    R.sconce('R', 40); R.sconce('L', 14); R.sconce('L', 56)
    rd = hexc(T['rug'])
    def bed(img, d):   # 나무 침대: 머리판, 매트리스, 이불, 베개
        R.box(img, 9.9, .9, 1.8, 2.2, 5, '#8A5636', '#5E3826', '#7A4A2E')
        R.box(img, 10, 1, 1.6, 2, 3, '#F2EEE4', '#C8C4BC', '#E0DCD4', lift=5)
        R.box(img, 10, 1.7, 1.6, 1.3, 2, rd, shade(rd, .6), shade(rd, .8), lift=7)
        R.box(img, 10.15, 1.1, 1.3, .5, 3, '#FFFFFF', '#D8D4CC', '#ECE8E0', lift=7)
        R.box(img, 9.9, .85, 1.8, .15, 20, '#8A5636', '#5E3826', '#7A4A2E')
        x, y = R.P(10.8, .9); d.ellipse([x - 3, y - 18, x + 3, y - 14], fill=hexc('#E8C060'))
    R.obj('bed', [(10, 1), (11, 1), (10, 2), (11, 2)], bed, act=('내 침대', '잠자고 내일로'))
    R.exit_to, R.exit_label = '@back', '휴게실'
    R.extra = dict(vw=180, house=key, furn=True, spawnIn=[6, 8])
    R.save('myroom_' + kind, '내 방', '침대에서 자요 · 가구를 놓아 꾸며요', [0, 0])
def main():
    for key in TH:
        for n in range(1, 7): common_room(key, n)
        my_room(key)
if __name__ == '__main__': main()
