# 「마녀 솥 대폭발」 장애물 12종 · 해독 재료 병 12색 · 광장 게시판: 변신(morph_art.py)과 같은 그림체 → out/morph_obst.png + out/morph_obst.json
#   칸마다 크기가 달라요. json: { 이름: [x, y, w, h, ax, ay] } (ax, ay = 발 디딘 점)
import os, json
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
OL = H('#1a1024'); HI = H('#ffffff'); EYE = H('#1a1024')

class Spr:
    def __init__(s, w, h): s.w, s.h = w, h; s.layers = []; s.top = {}
    def ell(s, cx, cy, rx, ry): return {(x, y) for x in range(s.w) for y in range(s.h) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
    def add(s, m, c): s.layers.append((set(m), c)); return s
    def dot(s, pts, c):
        for p in pts: s.top[p] = c
        return s
    def render(s):
        W, Hh = s.w + 2, s.h + 2; im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); P = im.load(); body = set()
        for m, c in s.layers:
            for q in m:
                if 0 <= q[0] < s.w and 0 <= q[1] < s.h: P[q[0] + 1, q[1] + 1] = c; body.add((q[0] + 1, q[1] + 1))
        for x in range(W):
            for y in range(Hh):
                if (x, y) not in body and any((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): P[x, y] = OL
        for q, c in s.top.items(): P[q[0] + 1, q[1] + 1] = c
        return im
def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}

OUT = []   # (이름, 그림)
# 1 호박 → 바위 무더기 (굴러서 밀어내요)
s = Spr(22, 16); s.add(s.ell(7, 10, 7, 5.5), H('#8A8494')).add(s.ell(15, 11, 6, 4.5), H('#9A94A6')).add(s.ell(11, 5.5, 5, 4), H('#A8A2B4'))
s.dot([(9, 3), (10, 3), (9, 4), (4, 7), (5, 7), (14, 8), (15, 8)], H('#C8C2D4')).dot([(x, 14) for x in range(2, 19)], H('#6A6474')).dot([(11, 9), (12, 10), (6, 12)], H('#6A6474')); OUT.append(('o_pumpkin', s))
# 2 유령 → 가시덤불 (스르륵 통과)
s = Spr(22, 18); s.add(s.ell(11, 11, 10.5, 6.5) | s.ell(7, 7, 5, 4) | s.ell(15, 6.5, 5, 4.5), H('#4A6A3A'))
s.dot([(3, 8), (7, 3), (12, 2), (18, 4), (20, 10), (1, 12), (10, 6), (15, 9)], H('#C8B8E0')).dot([(5, 10), (9, 12), (14, 13), (17, 11), (12, 8)], H('#2E4A26')).dot([(6, 6), (14, 5), (8, 13), (16, 13)], H('#B04A7A')); OUT.append(('o_ghost', s))
# 3 슬라임 → 물 위 연잎 (물 칸에 놓여요)
s = Spr(20, 10); s.add(s.ell(10, 5, 9.5, 4.5) - {(x, y) for x in range(9, 12) for y in range(0, 5) if abs(x - 10) <= (5 - y) * .4}, H('#5FA84A'))
s.dot([(5, 4), (6, 4), (14, 6), (15, 6)], H('#8AD06A')).dot([(x, 8) for x in range(4, 16)], H('#3E7A30')); OUT.append(('o_slime', s))
# 4 양초 → 짙은 어둠 덩어리 (밝혀서 걷어내요)
s = Spr(22, 16); s.add(s.ell(11, 9, 10.5, 6.5) | s.ell(6, 6, 5, 4.5) | s.ell(16, 5.5, 5, 4.5), H('#241838'))
s.dot([(5, 4), (6, 4), (15, 3), (17, 4), (10, 7), (3, 10), (19, 10)], H('#3E2A5A')).dot([(8, 9), (13, 9)], H('#B89AFF')); OUT.append(('o_candle', s))
# 5 빗자루 → 높은 마른 나무 위 둥지
s = Spr(22, 38); s.add(rect(9, 10, 12, 37) | {(x, 36 - abs(x - 10)) for x in range(5, 17)}, H('#6A4A34'))
for (x0, y0, dx) in ((8, 20, -1), (13, 16, 1), (8, 12, -1), (13, 25, 1)): s.add({(x0 + i * dx, y0 - i) for i in range(5)}, H('#6A4A34'))
s.add(s.ell(11, 7, 7, 3.5), H('#A8804A')).add(s.ell(11, 5, 3, 2), H('#7FD8E8'))
s.dot([(10, 12 + i * 4) for i in range(6)], H('#4A3424')).dot([(6, 7), (9, 8), (13, 8), (16, 7)], H('#7A5A30')).dot([(10, 4)], HI); OUT.append(('o_broom', s))
# 6 찻주전자 → 얼음 덩어리 (안에 병이 비쳐요)
s = Spr(18, 18); s.add({(x, y) for x in range(18) for y in range(18) if abs(x - 8.5) + abs(y - 8.5) * 1.15 <= 9.5}, H('#B8E4F4'))
s.add(rect(7, 6, 10, 12), H('#8AC8E4')).dot([(8, 5), (9, 5)], H('#7AB4D0')).dot([(4, 6), (5, 5), (5, 6), (12, 3)], HI).dot([(x, 15) for x in range(6, 12)], H('#8AC8E4')); OUT.append(('o_teapot', s))
# 7 해골 → 녹슨 철창문
s = Spr(22, 22); s.add(rect(0, 4, 2, 21) | rect(19, 4, 21, 21), H('#5A5464')).add(s.ell(11, 4, 9, 4) - s.ell(11, 5, 7, 3.2), H('#4A4454'))
s.add(rect(1, 19, 20, 20), H('#4A4454')).add({(x, y) for x in (5, 8, 11, 14, 17) for y in range(5, 20)}, H('#4A4454')).add(rect(1, 11, 20, 11), H('#4A4454'))
s.dot([(0, 3), (2, 3), (19, 3), (21, 3)], H('#7A7484')).dot([(11, 11), (10, 12), (11, 12)], H('#C88A3A')).dot([(5, 14), (14, 7), (17, 16)], H('#8A5A3A')); OUT.append(('o_skull', s))
# 8 수정구슬 → 흐릿한 마법진 (바닥)
s = Spr(24, 12); ring = s.ell(12, 6, 11.5, 5.5) - s.ell(12, 6, 9.5, 4.2); s.add(ring, H('#6A5A9A')).add({(12, 6), (11, 6), (12, 5), (12, 7), (13, 6)}, H('#8A7ABA'))
s.dot([(4, 3), (20, 3), (4, 9), (20, 9), (12, 1), (12, 11)], H('#C8B8FF')); OUT.append(('o_orb', s))
# 9 마법책 → 수수께끼 석판
s = Spr(18, 24); s.add(s.ell(9, 5, 8, 5) | rect(1, 5, 16, 21), H('#8A8494')).add(rect(0, 21, 17, 23), H('#6A6474'))
s.dot([(x, y) for (x, y) in ((5, 6), (6, 6), (5, 7), (9, 6), (10, 7), (12, 6), (5, 11), (7, 11), (8, 12), (11, 11), (12, 12), (6, 16), (9, 16), (10, 15), (12, 16))], H('#C8A0FF')).dot([(3, 4), (4, 3)], H('#B8B2C4')); OUT.append(('o_book', s))
# 10 버섯 → 시든 덩굴 무더기
s = Spr(22, 16); s.add(s.ell(11, 10, 10.5, 5.5), H('#6A5A3A'))
for (x, y) in ((2, 9), (5, 6), (9, 4), (14, 5), (18, 7), (20, 11)): s.add({(x, y), (x, y + 1), (x + 1, y + 1)}, H('#6A5A3A'))
s.dot([(4, 10), (6, 8), (8, 11), (10, 9), (12, 12), (14, 9), (16, 11), (18, 9)], H('#4A3E28')).dot([(7, 7), (13, 7), (17, 12)], H('#8A7A4A')).dot([(10, 6)], H('#A86A8A')); OUT.append(('o_mushroom', s))
# 11 종 → 잠든 돌 문지기 석상
s = Spr(20, 28); s.add(rect(1, 23, 18, 27), H('#6A6474')).add(s.ell(10, 16, 7, 7.5), H('#8A8494')).add(s.ell(10, 7, 6, 5.5), H('#9A94A6'))
s.add({(3, 2), (4, 3), (4, 2), (16, 2), (15, 3), (15, 2)}, H('#9A94A6')).add({(1, 12), (2, 11), (3, 11), (18, 12), (17, 11), (16, 11)}, H('#7A7484'))
s.dot([(7, 7), (8, 7), (12, 7), (13, 7)], EYE).dot([(10, 10)], H('#6A6474')).dot([(15, 4), (17, 3)], H('#E0E8FF')).dot([(18, 1)], H('#E0E8FF')).dot([(6, 17), (14, 17)], H('#6A6474')); OUT.append(('o_bell', s))
# 12 거울 → 봉인된 상자 (빛 문양 자물쇠)
s = Spr(20, 16); s.add(rect(1, 5, 18, 15), H('#7A4A2E')).add(s.ell(10, 5, 9, 4) & {(x, y) for x in range(20) for y in range(6)}, H('#8A5A36'))
s.add(rect(1, 8, 18, 8) | rect(4, 2, 4, 15) | rect(15, 2, 15, 15), H('#C8A050')).add(rect(8, 7, 11, 11), H('#4A3A6A'))
s.dot([(9, 8), (10, 8), (9, 9), (10, 10), (9, 10)], H('#9AF0FF')).dot([(6, 11), (12, 13)], H('#5A3420')); OUT.append(('o_mirror', s))

# 해독 재료 병: 변신 12종 색
COLS = ['#F59A3A', '#E8E4FF', '#7FD8B0', '#FFD060', '#D8B460', '#8FB8E8', '#F2EEE2', '#B8A0F0', '#C890FF', '#D84A6A', '#F0C040', '#BFE6FF']
for i, c in enumerate(COLS):
    s = Spr(9, 12); s.add(rect(3, 0, 5, 1), H('#8A5A36')).add(rect(3, 2, 5, 3), H('#D8E8F0')).add(s.ell(4.5, 8, 4.5, 4), H('#D8E8F0')).add(s.ell(4.5, 8.5, 3.5, 3), H(c))
    s.dot([(2, 6), (2, 7)], HI); OUT.append((f'f{i}', s))

# 광장 게시판
s = Spr(30, 30); s.add(rect(3, 14, 4, 29) | rect(25, 14, 26, 29), H('#6A4A34')).add(rect(0, 0, 29, 18), H('#8A5A36')).add(rect(2, 2, 27, 16), H('#C89A62'))
s.add(rect(0, 0, 29, 1), H('#6A4A34')).dot([(x, 9) for x in range(2, 28) if x % 6 == 1], H('#B0844E'))
for (x0, y0, x1, y1, c) in ((4, 4, 12, 13, '#FFF8E8'), (15, 3, 25, 9, '#F6EED8'), (16, 11, 24, 15, '#FFF0F0')):
    s.add(rect(x0, y0, x1, y1), H(c))
s.dot([(x, y) for y in (6, 8, 10) for x in range(5, 12) if (x + y) % 5]  + [(x, y) for y in (5, 7) for x in range(16, 25) if (x * 3 + y) % 4] + [(x, 13) for x in range(17, 24) if x % 3], H('#9A8A7A'))
s.dot([(8, 4), (20, 3), (20, 11)], H('#E84A5A')).dot([(1, 0), (28, 0)], H('#A8784A')); OUT.append(('board', s))

if __name__ == '__main__':
    ims = [(k, sp.render()) for k, sp in OUT]; W = sum(im.width for _, im in ims) + len(ims); Hh = max(im.height for _, im in ims)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); meta = {}; x = 0
    for k, im in ims:
        sheet.alpha_composite(im, (x, 0)); meta[k] = [x, 0, im.width, im.height, im.width // 2, im.height - 1]; x += im.width + 1
    sheet.save('out/morph_obst.png'); json.dump(meta, open('out/morph_obst.json', 'w')); print('obst', sheet.size, len(meta))
