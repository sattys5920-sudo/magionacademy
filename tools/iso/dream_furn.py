# 꿈나라 「꿈 조각」으로 만드는 꿈 가구 15종 (시안): 방 가구(furniture.py)와 같은 아이소 그림체
#   python3 dream_furn.py → out/dream_furn.png (한 줄) + out/dream_furn.json + out/dream_furn_preview.png (이름 붙인 미리보기)
import json, math
from interiors import Room, hexc, shade, OUTL
from furniture import bx, C, ell, H
from PIL import Image, ImageDraw, ImageFont

def puff(d, x, y, rx, ry, c='#FFFFFF', s='#D4DEF8'):   # 뭉게구름 덩어리
    ell(d, x, y + 1, rx, ry, s); ell(d, x, y, rx, ry, c)
def sparkle(d, x, y, c='#FFE070'):
    for dx, dy in ((0, -2), (0, -1), (-1, 0), (-2, 0), (0, 0), (1, 0), (2, 0), (0, 1), (0, 2)): d.point((x + dx, y + dy), fill=H(c))
    d.point((x, y), fill=H('#FFFFFF'))

def cloud_sofa(R, img, d):      # 구름 소파
    x, y = C(R, 2, 1.5)
    for dx in (-10, 0, 10): puff(d, x + dx, y - 3, 8, 5)
    for dx in (-8, 4): puff(d, x + dx, y - 13, 8, 6)
    puff(d, x - 15, y - 8, 4, 5); puff(d, x + 15, y - 8, 4, 5)
    ell(d, x - 4, y - 7, 5, 2.5, '#F8C8E0'); ell(d, x + 7, y - 6, 4, 2, '#C8DCFF')   # 쿠션
def cloud_bed(R, img, d):       # 구름 침대 (달 머리판)
    x, y = C(R, 2, 1.8)
    ell(d, x - 10, y - 26, 9, 9, '#FFE9A0'); ell(d, x - 6, y - 28, 8, 8, (0, 0, 0, 0))
    for dx, dy in ((-12, -6), (-2, -4), (8, -2), (16, 0)): puff(d, x + dx, y + dy, 9, 5)
    ell(d, x + 2, y - 10, 13, 4, '#A8C0F8'); ell(d, x + 2, y - 11, 12, 3, '#C8D8FF')
    for dx, dy in ((-4, -11), (4, -10), (10, -11)): d.point((x + dx, y + dy), fill=H('#FFE070'))
    ell(d, x - 11, y - 11, 4, 2.5, '#FFFFFF')
def lolli_lamp(R, img, d):      # 막대사탕 등불
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 5, 2.2, '#E890B8'); d.rectangle([x - 1, y - 24, x, y], fill=H('#FAF2EE'))
    ell(d, x, y - 29, 8, 8, '#FF80B0'); ell(d, x, y - 29, 5.5, 5.5, '#FFB8D8'); ell(d, x, y - 29, 2.5, 2.5, '#FF80B0'); ell(d, x - 3, y - 32, 1.5, 1, '#FFFFFF')
    d.line([(x + 1, y - 21), (x + 5, y - 19)], fill=H('#7AD0F8')); d.line([(x - 1, y - 21), (x - 5, y - 19)], fill=H('#7AD0F8'))   # 리본
def upside_bowl(R, img, d):     # 거꾸로 어항: 모래·산호가 위에, 물고기가 거꾸로
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.2, 1.2, .6, .6, 8, '#8A6AB8', top='#A88AD8')
    ell(d, x, y - 20, 10, 10, '#BFE8F8'); ell(d, x, y - 19, 9, 8, '#7ACAF0')
    ell(d, x, y - 27, 8, 3, '#E8D090'); d.rectangle([x - 4, y - 26, x - 3, y - 20], fill=H('#FF7A90')); d.rectangle([x + 3, y - 26, x + 4, y - 22], fill=H('#B880F0'))
    ell(d, x + 1, y - 15, 3, 1.6, '#FFB040'); d.polygon([(x + 4, y - 15), (x + 6, y - 17), (x + 6, y - 13)], fill=H('#FFB040')); d.point((x - 1, y - 15), fill=H('#2A1830'))
    d.point((x - 5, y - 22), fill=H('#FFFFFF')); d.point((x + 6, y - 20), fill=H('#FFFFFF'))
def konpeito_pot(R, img, d):    # 별사탕 화분
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.25, 1.25, .5, .5, 7, '#E8A0C0', top='#F8C0D8')
    for dx, dy in ((0, -16), (-5, -12), (5, -13)): d.line([(x, y - 7), (x + dx, y + dy)], fill=H('#7AB850'))
    for dx, dy, c in ((0, -18, '#FFE070'), (-6, -13, '#9AD8FF'), (6, -15, '#FFB0D0'), (-2, -22, '#C8A0FF'), (4, -21, '#B8F0A0')): sparkle(d, x + dx, y + dy, c)
def moon_swing(R, img, d):      # 달 그네 (천장에서 내려와요)
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 7, 2.5, (40, 30, 70, 90))
    for dx in (-6, 6): d.line([(x + dx, y - 34), (x + dx, y - 12)], fill=H('#C8B890'))
    d.rectangle([x - 9, y - 36, x + 9, y - 35], fill=H('#8A7AB0'))
    ell(d, x, y - 10, 10, 6, '#FFE070'); ell(d, x, y - 14, 10, 6, (0, 0, 0, 0))
    d.chord([x - 10, y - 16, x + 10, y - 4], 0, 180, fill=H('#FFE070')); d.chord([x - 8, y - 14, x + 8, y - 8], 0, 180, fill=H('#FFF4B0'))
    ell(d, x - 5, y - 10, 1, 1, '#2A1830'); d.point((x - 3, y - 8), fill=H('#F0A0A0'))
    sparkle(d, x + 11, y - 30); sparkle(d, x - 12, y - 22, '#C8E0FF')
def cotton_tree(R, img, d):     # 솜사탕 나무
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.3, 1.3, .4, .4, 5, '#C8A0D8', top='#E0C0F0'); d.rectangle([x - 1, y - 18, x + 1, y - 5], fill=H('#FAF2EE'))
    puff(d, x - 5, y - 24, 7, 6, '#FFC0E0', '#F098C8'); puff(d, x + 5, y - 26, 7, 6, '#C8E0FF', '#98B8F0'); puff(d, x, y - 32, 7, 6, '#FFE8F4', '#F8C0E0')
    for dx, dy in ((-7, -26), (6, -29), (0, -34)): d.point((x + dx, y + dy), fill=H('#FFFFFF'))
def ginger_shelf(R, img, d):    # 과자 집 책장
    bx(R, img, 1.1, 1.3, .8, .6, 28, '#C88A5A', top='#FFFFFF'); x0, y0 = C(R, 1.1, 1.9)
    for row in range(3):
        d.line([(x0 + 1, y0 - 3 - row * 9), (x0 + 11, y0 - 8 - row * 9)], fill=H('#FFFFFF'))
        for k in range(4): d.rectangle([x0 + 2 + k * 2, y0 - 9 - row * 9 - k, x0 + 3 + k * 2, y0 - 4 - row * 9 - k], fill=H(['#FF80B0', '#7AD0F8', '#FFE070', '#9AE07A'][(k + row) % 4]))
    for dx, dy, c in ((3, -29, '#FF6060'), (8, -31, '#7AD0F8'), (13, -30, '#FFE070')): ell(d, x0 + dx, y0 + dy, 1.5, 1.5, c)
def dream_musicbox(R, img, d):  # 꿈 오르골 (위에서 꿈 조각이 빙글)
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.2, 1.2, .6, .6, 7, '#5A3A8A', top='#7A5AB0'); bx(R, img, 1.2, 1.2, .6, .6, 1, '#F2C450', lift=7)
    d.rectangle([x, y - 16, x, y - 10], fill=H('#F2C450'))
    pts = [(x, y - 24), (x + 2, y - 20), (x + 5, y - 19), (x + 2, y - 17), (x + 3, y - 14), (x, y - 16), (x - 3, y - 14), (x - 2, y - 17), (x - 5, y - 19), (x - 2, y - 20)]
    d.polygon(pts, fill=H('#C890FF')); d.point((x - 1, y - 20), fill=H('#F4E4FF'))
    d.line([(x + 7, y - 22), (x + 7, y - 26)], fill=H('#FFFFFF')); d.point((x + 6, y - 22), fill=H('#FFFFFF')); d.line([(x - 8, y - 18), (x - 8, y - 21)], fill=H('#FFFFFF')); d.point((x - 9, y - 18), fill=H('#FFFFFF'))
def rainbow_rug(R, img, d):     # 무지개 러그 (바닥)
    for k, c in enumerate(('#FF8A8A', '#FFC070', '#FFE88A', '#9AE0A0', '#8AC8F8', '#B8A0F0')):
        T = R.P(1 + k * .3, 1); B = R.P(1 + k * .3 + .3, 1); L = R.P(1 + k * .3, 3); Rr = R.P(1 + k * .3 + .3, 3)
        d.polygon([T, B, Rr, L], fill=H(c))
    x, y = C(R, 2, 2); puff(d, x - 10, y + 4, 4, 2); puff(d, x + 10, y - 4, 4, 2)
def whale_balloon(R, img, d):   # 둥실 고래 풍선
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 3, 1.2, '#9AA4B4'); d.line([(x, y), (x + 2, y - 10), (x, y - 18)], fill=H('#E8E0F0'))
    ell(d, x, y - 26, 11, 7, '#7A9CE8'); ell(d, x, y - 23, 9, 4, '#D8E4FF'); ell(d, x + 6, y - 28, 1, 1, '#2A1830'); d.point((x + 7, y - 25), fill=H('#F0A0B0'))
    d.polygon([(x - 10, y - 26), (x - 16, y - 32), (x - 14, y - 26), (x - 16, y - 20)], fill=H('#7A9CE8'))
    for dx, dy in ((2, -35), (0, -37), (4, -37)): d.point((x + dx, y + dy), fill=H('#C8F0FF'))
def donut_cushion(R, img, d):   # 도넛 방석
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 2, 10, 5, '#D89050'); ell(d, x, y - 4, 10, 5, '#E8A860'); ell(d, x, y - 5, 9, 4, '#FF90C0'); ell(d, x, y - 5, 3.5, 1.6, '#D89050')
    for dx, dy, c in ((-6, -6, '#FFFFFF'), (5, -7, '#7AD0F8'), (-3, -8, '#FFE070'), (6, -4, '#9AE07A'), (-7, -3, '#7AD0F8')): d.point((x + dx, y + dy), fill=H(c))
def star_mobile(R, img, d):     # 별·구름 모빌 (스탠드)
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 5, 2, '#5E4880'); d.rectangle([x, y - 36, x, y], fill=H('#8A7AB0')); d.line([(x - 12, y - 34), (x + 12, y - 36)], fill=H('#8A7AB0'))
    for dx, ln, kind in ((-11, 8, 's'), (-4, 13, 'c'), (5, 10, 's'), (11, 6, 'm')):
        d.line([(x + dx, y - 35), (x + dx, y - 35 + ln)], fill=H('#C8B8E0')); yy = y - 35 + ln
        if kind == 's': sparkle(d, x + dx, yy + 2)
        elif kind == 'c': puff(d, x + dx, yy + 2, 3, 2)
        else: ell(d, x + dx, yy + 2, 2.5, 2.5, '#FFE9A0'); ell(d, x + dx + 1, yy + 1, 2, 2, (0, 0, 0, 0))
def sleepy_clock(R, img, d):    # 졸린 괘종시계 (시계판이 흘러내려요)
    bx(R, img, 1.2, 1.3, .6, .5, 24, '#6A5AA8', top='#8A7AC8'); x, y = C(R, 1.5, 1.5)
    ell(d, x - 1, y - 24, 6, 6, '#FFF4D8'); d.polygon([(x - 7, y - 22), (x - 5, y - 15), (x - 3, y - 19)], fill=H('#FFF4D8'))
    d.line([(x - 1, y - 24), (x - 1, y - 28)], fill=H('#2A1830')); d.line([(x - 1, y - 24), (x + 2, y - 22)], fill=H('#2A1830'))
    d.line([(x - 4, y - 25), (x - 3, y - 25)], fill=H('#2A1830')); d.line([(x + 1, y - 26), (x + 2, y - 26)], fill=H('#2A1830'))   # 감은 눈
    d.line([(x - 1, y - 14), (x - 1, y - 7)], fill=H('#F2C450')); ell(d, x - 1, y - 6, 2, 2, '#F2C450')
    for (zx, zy, n) in ((x + 6, y - 32, 2), (x + 10, y - 37, 3)):
        d.line([(zx, zy), (zx + n, zy)], fill=H('#E8DCFF')); d.line([(zx + n, zy), (zx, zy + n)], fill=H('#E8DCFF')); d.line([(zx, zy + n), (zx + n, zy + n)], fill=H('#E8DCFF'))
def shard_lantern(R, img, d):   # 꿈 조각 등불
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 5, 2, '#3A2E50'); d.rectangle([x - 5, y - 18, x + 5, y - 2], fill=H('#2A2040'))
    d.rectangle([x - 4, y - 17, x + 4, y - 3], fill=H('#5A3A8A')); ell(d, x, y - 10, 4, 5, '#C890FF'); ell(d, x, y - 10, 2, 3, '#F4E4FF')
    d.polygon([(x - 6, y - 18), (x, y - 23), (x + 6, y - 18)], fill=H('#2A2040')); ell(d, x, y - 25, 2, 2, (0, 0, 0, 0)); d.arc([x - 2, y - 27, x + 2, y - 22], 180, 360, fill=H('#8A7AB0'))
    for dx, dy in ((-8, -14), (8, -8), (7, -20)): d.point((x + dx, y + dy), fill=H('#C890FF'))
def pillow_pile(R, img, d):     # 꿈 베개 더미
    x, y = C(R, 1.5, 1.5)
    for dx, dy, c in ((-5, -2, '#A8C0F8'), (6, -1, '#F8C0D8'), (0, -7, '#FFF0B0'), (-3, -12, '#C8F0D8'), (3, -16, '#E0D0FF')):
        ell(d, x + dx, y + dy, 8, 4, shade(H(c), .82)); ell(d, x + dx, y + dy - 1, 8, 3.5, c); d.point((x + dx - 6, y + dy - 1), fill=H('#FFFFFF'))
    sparkle(d, x + 3, y - 16, '#FFE070')

ITEMS = [   # id, 이름, 그림, 칸(가로, 세로), 꿈 조각
  ('dr_sofa', '구름 소파', cloud_sofa, (2, 1), 30), ('dr_bed', '구름 침대', cloud_bed, (2, 2), 60), ('dr_lolli', '막대사탕 등불', lolli_lamp, (1, 1), 20),
  ('dr_bowl', '거꾸로 어항', upside_bowl, (1, 1), 40), ('dr_konpeito', '별사탕 화분', konpeito_pot, (1, 1), 15), ('dr_swing', '달 그네', moon_swing, (1, 1), 45),
  ('dr_cotton', '솜사탕 나무', cotton_tree, (1, 1), 25), ('dr_shelf', '과자 집 책장', ginger_shelf, (1, 1), 35), ('dr_music', '꿈 오르골', dream_musicbox, (1, 1), 30),
  ('dr_rug', '무지개 러그', rainbow_rug, (2, 2), 25), ('dr_whale', '둥실 고래 풍선', whale_balloon, (1, 1), 35), ('dr_donut', '도넛 방석', donut_cushion, (1, 1), 15),
  ('dr_mobile', '별 구름 모빌', star_mobile, (1, 1), 20), ('dr_clock', '졸린 괘종시계', sleepy_clock, (1, 1), 40), ('dr_lantern', '꿈 조각 등불', shard_lantern, (1, 1), 20)]

def main():
    sprites, meta = [], []
    for fid, name, draw, (w, dd), cost in ITEMS:
        R = Room(6, 6, 60); R.obj(fid, [(1, 1)], lambda img, d, draw=draw: draw(R, img, d))
        o = R.objs[-1]; ax, ay = R.P(1, 1)
        sprites.append(o['img']); meta.append(dict(id=fid, name=name, cat='꿈', dream=cost, w=w, d=dd, solid=0 if fid == 'dr_rug' else 1, flat=1 if fid == 'dr_rug' else 0, sw=o['img'].width, sh=o['img'].height, ax=round(ax - o['x']), ay=round(ay - o['y'])))
    W = sum(s.width + 1 for s in sprites); Hh = max(s.height for s in sprites)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
    for s, m in zip(sprites, meta): sheet.paste(s, (x, Hh - s.height)); m['sx'] = x; m['ay'] += Hh - s.height; m['sh'] = Hh; x += s.width + 1
    sheet.save('out/dream_furn.png'); json.dump(meta, open('out/dream_furn.json', 'w'), ensure_ascii=False)
    # 미리보기: 5칸 × 3줄, 바닥 타일 위에 4배
    S, CW, CH, cols = 4, 200, 260, 5; rows = math.ceil(len(sprites) / cols)
    pv = Image.new('RGB', (CW * cols, CH * rows + 60), hexc('#2A1E3A')); dr = ImageDraw.Draw(pv)
    import os
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 16) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 13) if os.path.exists(fb) else F
    dr.text((20, 18), '꿈 가구 시안 · 꿈 조각으로 만들어요', font=F, fill=hexc('#FFE9A0'))
    for i, (s, m) in enumerate(zip(sprites, meta)):
        cx, cy = (i % cols) * CW + CW // 2, (i // cols) * CH + 60
        dr.rounded_rectangle([cx - CW // 2 + 8, cy + 4, cx + CW // 2 - 8, cy + CH - 8], 14, fill=hexc('#3A2C52'))
        ty = cy + 140 - (m['w'] - 1) * 16; w_, d_ = m['w'], m['d']; cx -= (w_ - d_) * 16
        dr.polygon([(cx, ty), (cx + 32 * w_, ty + 16 * w_), (cx + 32 * w_ - 32 * d_, ty + 16 * w_ + 16 * d_), (cx - 32 * d_, ty + 16 * d_)], fill=hexc('#5A4A78'))
        big = s.resize((s.width * S, s.height * S), Image.NEAREST); ax, ay = m['ax'], m['ay'] - (Hh - s.height)
        pv.paste(big, (cx - ax * S, ty - ay * S), big)
        cx = (i % cols) * CW + CW // 2
        dr.text((cx, cy + CH - 44), m['name'], font=F2, fill=hexc('#F1E9FF'), anchor='mm'); dr.text((cx, cy + CH - 24), f"꿈 조각 {m['dream']}", font=F2, fill=hexc('#D8B4FF'), anchor='mm')
    pv.save('out/dream_furn_preview.png'); print('dream furn', len(meta), sheet.size, pv.size)
if __name__ == '__main__': main()
