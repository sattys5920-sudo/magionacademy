# 장난 마법 20종: 친구 머리 위·주변에 뜨는 효과 그림 (변신·아기 동물과 같은 도트 그림체) → out/prank.png + out/prank.json
#   칸마다 크기가 달라요. json: { 이름: [x, y, w, h] } · 머리 위 효과는 아래 가운데가 머리 꼭대기에 닿게 그려요
import os, json, math
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from morph_obst import Spr, rect, H as C

HI = C('#ffffff'); EYE = C('#1a1024'); BL = C('#ff9ab8')
def disc(s, cx, cy, r): return s.ell(cx, cy, r, r)
OUT = []

# 1 무지개 다리
s = Spr(24, 12)
for i, c in enumerate(['#FF6A7A', '#FFB050', '#FFE070', '#7AE6A0', '#7AB8FF', '#B48AFF']):
    s.add(s.ell(11.5, 11.5, 11.5 - i, 11 - i) - s.ell(11.5, 11.5, 10.5 - i, 10 - i), C(c))
s.add(s.ell(2, 10.5, 2.6, 1.6) | s.ell(21, 10.5, 2.6, 1.6), C('#FFFFFF')); OUT.append(('rainbow', '무지개 다리', s))
# 2 고양이 귀 (머리에 붙어요)
s = Spr(20, 8)
for ox in (0, 13): s.add({(ox + x, y) for x in range(7) for y in range(8) if y >= 7 - min(x, 6 - x) * 2.4}, C('#3A2A3A'))
s.dot([(2, 5), (3, 5), (3, 4), (4, 5), (15, 5), (16, 5), (16, 4), (17, 5)], C('#FF9AB8'))
OUT.append(('catears', '고양이 귀', s))
# 3 꽃비 (주변에 흩날려요 · 한 장면)
s = Spr(24, 18)
for (x, y, c) in ((3, 2, '#FF9AB8'), (12, 1, '#FFFFFF'), (20, 4, '#FFB0C8'), (6, 9, '#FFFFFF'), (17, 11, '#FF9AB8'), (10, 15, '#FFB0C8'), (22, 15, '#FFFFFF')):
    s.add({(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}, C(c)); s.dot([(x, y)], C('#FFE070'))
OUT.append(('petals', '꽃비', s))
# 4 비구름
s = Spr(20, 16); s.add(s.ell(6, 6, 5, 4) | s.ell(12, 5, 6, 5) | s.ell(16, 7, 4, 3.5) | rect(2, 6, 18, 9), C('#B8C4D8')); s.dot([(8, 5), (9, 5), (13, 4)], C('#E8EEF8'))
s.dot([(7, 7), (8, 7), (12, 7), (13, 7)], EYE); s.dot([(10, 9)], EYE); s.dot([(5, 9), (15, 9)], BL)
for x, y in ((4, 12), (9, 14), (14, 12), (17, 15)): s.dot([(x, y), (x, y + 1)], C('#7AB8FF'))
OUT.append(('raincloud', '꼬마 비구름', s))
# 5 하트 풍선
s = Spr(12, 22); s.add(s.ell(3.5, 4, 3.5, 3.5) | s.ell(8.5, 4, 3.5, 3.5) | {(x, y) for x in range(12) for y in range(4, 12) if abs(x - 5.5) <= (11 - y) * .85}, C('#FF5A7A'))
s.dot([(2, 2), (3, 2), (2, 3)], HI); s.add({(6, y) for y in range(12, 22)}, C('#8A8494')); OUT.append(('heartballoon', '하트 풍선', s))
# 6 별 왕관
s = Spr(18, 9); s.add(rect(1, 6, 16, 8), C('#F2C450'))
for cx in (3, 8.5, 14): s.add({(x, y) for x in range(18) for y in range(7) if abs(x + .5 - cx - .5) <= (y + 1) * .45}, C('#F2C450'))
s.dot([(8, 7), (9, 7)], C('#E8506A')); s.dot([(3, 7), (14, 7)], C('#7AB8FF')); s.dot([(3, 1), (8, 0), (9, 0), (14, 1)], C('#FFF4A0')); OUT.append(('starcrown', '반짝 왕관', s))
# 7 토끼 귀
s = Spr(14, 12); s.add(s.ell(3, 5.5, 2.4, 5.5) | s.ell(10.5, 5.5, 2.4, 5.5), C('#F6F0F6')); s.dot([(3, y) for y in range(2, 9)] + [(10, y) for y in range(2, 9)], C('#FFB0C8')); OUT.append(('bunnyears', '토끼 귀', s))
# 8 비눗방울
s = Spr(18, 20)
for (cx, cy, r) in ((5, 15, 3.5), (12, 9, 4.5), (6, 4, 2.5), (14, 17, 2)):
    s.add(s.ell(cx, cy, r, r) - s.ell(cx, cy, r - 1, r - 1), C('#9AD8F8')); s.dot([(int(cx - r / 2), int(cy - r / 2))], HI)
OUT.append(('bubbles', '비눗방울', s))
# 9 꼬마 유령 친구
s = Spr(12, 13); s.add(s.ell(6, 5, 5, 5) | rect(1, 5, 10, 10) | {(x, 11) for x in range(1, 11) if x % 3 != 2}, C('#F4F2FF')); s.dot([(4, 5), (7, 5), (4, 6), (7, 6)], EYE); s.dot([(4, 5), (7, 5)], HI); s.dot([(3, 8), (8, 8)], BL); s.dot([(2, 2)], HI); OUT.append(('ghostpal', '꼬마 유령 친구', s))
# 10 박쥐 날개 (등 뒤)
s = Spr(26, 10)
for side in (0, 1):
    pts = [(0, 1), (9, 3), (10, 8), (7, 6), (5, 9), (3, 6), (0, 8)]
    if side: pts = [(25 - x, y) for x, y in pts]
    from morph_obst import Spr as _S
    from PIL import ImageDraw
    m = set(); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for y in range(10):
        for x in range(26):
            px, py, inside, j = x + .5, y + .5, False, len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi: inside = not inside
                j = i
            if inside: m.add((x, y))
    s.add(m, C('#4A2A5A'))
s.dot([(3, 3), (22, 3)], C('#7A4A8A')); OUT.append(('batwings', '박쥐 날개', s))
# 11 호박 모자
s = Spr(16, 11); s.add(s.ell(8, 6.5, 7.5, 4.5), C('#F59A3A')); s.dot([(4, y) for y in range(4, 10)] + [(11, y) for y in range(4, 10)], C('#D8782A')); s.add(rect(7, 0, 8, 2), C('#4A7A2E')); s.dot([(9, 1), (10, 1)], C('#6EA040'))
s.dot([(5, 6), (10, 6)], EYE); s.dot([(6, 8), (7, 8), (8, 8), (9, 8)], EYE); OUT.append(('pumpkinhat', '호박 모자', s))
# 12 눈송이
s = Spr(22, 18)
for (cx, cy) in ((4, 3), (15, 2), (9, 9), (19, 11), (3, 14), (13, 16)):
    s.add({(cx, cy), (cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)}, C('#F2F8FF'))
OUT.append(('snowflakes', '눈송이', s))
# 13 반딧불이
s = Spr(22, 16)
for (x, y) in ((3, 4), (17, 2), (10, 12), (19, 13), (6, 15)): s.add({(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}, C('#FFF07A')); s.dot([(x, y)], HI)
OUT.append(('fireflies', '반딧불이', s))
# 14 음표
s = Spr(18, 16); s.add(s.ell(3, 13, 2.6, 2) | rect(5, 3, 5, 13) | rect(5, 3, 8, 4), C('#B48AFF')); s.add(s.ell(12, 10, 2.6, 2) | rect(14, 1, 14, 10) | rect(14, 1, 17, 2), C('#FF8AC8')); OUT.append(('notes', '흥얼 음표', s))
# 15 나비
s = Spr(20, 14)
for (ox, oy, c) in ((0, 0, '#FFB050'), (11, 6, '#7AB8FF')):
    s.add(s.ell(ox + 2.5, oy + 2.5, 2.5, 2.5) | s.ell(ox + 6.5, oy + 2.5, 2.5, 2.5) | s.ell(ox + 2.5, oy + 6, 2, 1.6) | s.ell(ox + 6.5, oy + 6, 2, 1.6), C(c)); s.dot([(ox + 4, oy + y) for y in range(2, 8)], C('#4A3A3A')); s.dot([(ox + 3, oy), (ox + 6, oy)], C('#4A3A3A'))
OUT.append(('butterflies', '나비 친구', s))
# 16 천사 고리
s = Spr(18, 6); s.add(s.ell(9, 3, 8.5, 2.6) - s.ell(9, 3, 6, 1.2), C('#FFE070')); s.dot([(3, 2), (4, 1)], C('#FFF8C0')); OUT.append(('halo', '천사 고리', s))
# 17 개구리 모자
s = Spr(18, 10); s.add(s.ell(9, 7, 8.5, 3.5), C('#6EC060')); s.add(disc(s, 4, 3.5, 3) | disc(s, 14, 3.5, 3), C('#6EC060')); s.add(disc(s, 4, 3.5, 1.6) | disc(s, 14, 3.5, 1.6), C('#FFFFFF'))
s.dot([(4, 3), (14, 3), (4, 4), (14, 4)], EYE); s.dot([(x, 8) for x in range(6, 13)], C('#3E8A3A')); s.dot([(3, 8), (15, 8)], BL); OUT.append(('froghat', '개구리 모자', s))
# 18 깜짝 번개구름
s = Spr(20, 18); s.add(s.ell(6, 6, 5, 4) | s.ell(12, 5, 6, 5) | s.ell(16, 7, 4, 3.5) | rect(2, 6, 18, 9), C('#6A6474')); s.dot([(7, 7), (12, 7)], EYE); s.dot([(8, 9), (9, 10), (10, 9), (11, 10)], EYE)
from morph_obst import rect as _r
s.add({(10, 11), (9, 12), (10, 12), (8, 13), (9, 13), (10, 13), (11, 13), (10, 14), (11, 14), (10, 15), (10, 16)}, C('#FFE070')); OUT.append(('zapcloud', '깜짝 번개구름', s))
# 19 사탕 비
s = Spr(22, 18)
for (x, y, c) in ((3, 2, '#FF6A7A'), (14, 1, '#7AE6A0'), (8, 9, '#7AB8FF'), (18, 10, '#FFB050'), (4, 15, '#B48AFF'), (15, 16, '#FF8AC8')):
    s.add({(x, y), (x + 1, y), (x + 2, y), (x + 1, y - 1), (x + 1, y + 1)} , C(c)); s.dot([(x - 1, y), (x + 3, y)], C('#F4F0F0')); s.dot([(x + 1, y)], HI)
OUT.append(('candyrain', '사탕 비', s))
# 20 오투모의 가호: 머리 위 꼬마 로봇 (흰 둥근 머리 · 얇은 파란 머리띠 · 노란 양쪽 뿔 · 이마 「02」 · 분홍 사선 볼 · 빨간 점 · 동그란 몸 단추 · 파란 팔다리)
s = Spr(24, 24)
s.add({(x, y) for x in range(0, 7) for y in range(1, 9) if (x - 1) + (y - 1) * .2 >= 0 and abs((x - 1.5) - (8 - y) * .55) <= 1.8 and y <= 8}, C('#F2D040'))      # 왼쪽 노란 뿔 (위로 비스듬히)
s.add({(23 - x, y) for x in range(0, 7) for y in range(1, 9) if (x - 1) + (y - 1) * .2 >= 0 and abs((x - 1.5) - (8 - y) * .55) <= 1.8 and y <= 8}, C('#F2D040'))
s.add(s.ell(12, 9.5, 8.5, 7.5), C('#FAFAFA'))                                                                     # 머리
s.dot([(x, 4) for x in range(6, 19)] + [(5, 5), (19, 5)], C('#3A5AC8'))                                            # 얇은 파란 머리띠
Z0 = ['###', '#.#', '#.#', '#.#', '###']; Z2 = ['###', '..#', '###', '#..', '###']   # 이마의 「02」
for ox, g in ((8, Z0), (12, Z2)): s.dot([(ox + i, 5 + j) for j, row in enumerate(g) for i, ch in enumerate(row) if ch == '#'], C('#3A3A5A'))
s.dot([(6, 13), (7, 12), (9, 13), (10, 12), (12, 13), (13, 12)], C('#FF8AA8'))                                    # 분홍 사선 볼
s.dot([(18, 11), (19, 11), (18, 12)], C('#E8404A'))                                                                # 빨간 점
s.add(s.ell(12, 19, 3.8, 3), C('#FAFAFA'))                                                                         # 몸
s.dot([(11, 18), (12, 18), (13, 19), (11, 20), (12, 20)], EYE)                                                    # 동그란 단추
s.add(s.ell(5.5, 17, 2.2, 1.8) | s.ell(18.5, 17, 2.2, 1.8), C('#3A5AC8'))                                       # 팔
s.add(s.ell(9, 22.5, 2.6, 1.4) | s.ell(15, 22.5, 2.6, 1.4), C('#3A5AC8'))                                        # 발
s.dot([(4, 16), (17, 16), (8, 22), (14, 22)], C('#8AAAF0'))
OUT.append(('otumo', '오투모의 가호', s))

if __name__ == '__main__':
    ims = [(k, n, sp.render()) for k, n, sp in OUT]; W = sum(im.width for *_, im in ims) + len(ims); Hh = max(im.height for *_, im in ims)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); meta = {}; x = 0
    for k, n, im in ims: sheet.alpha_composite(im, (x, 0)); meta[k] = [x, 0, im.width, im.height, n]; x += im.width + 1
    sheet.save('out/prank.png'); json.dump(meta, open('out/prank.json', 'w'), ensure_ascii=False); print('prank', sheet.size, len(meta))
