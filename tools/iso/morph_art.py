# 「마녀 솥 대폭발」 변신 12종: 아기 동물(baby_animals.py)과 같은 그림체 · 15×15 도트(둘레 1칸 윤곽선 → 17×17 칸) → out/morph.png (가로 12칸)
import os
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = 15
C = S + 2
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
OL = H('#1a1024'); EYE = H('#1a1024'); HI = H('#ffffff'); BLUSH = H('#ff9ab8')
def ell(cx, cy, rx, ry): return {(x, y) for x in range(S) for y in range(S) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
def px(*p): return set(p)

class Spr:
    def __init__(s): s.layers = []; s.top = {}
    def add(s, m, c): s.layers.append((set(m), c)); return s
    def dot(s, pts, c):
        for p in pts: s.top[p] = c
        return s
    def face(s, y, a, b, blush=True, mouth=True):
        for x in (a, b): s.dot([(x, y), (x, y + 1)], EYE); s.dot([(x, y)], HI)
        if blush: s.dot([(a - 1, y + 2), (b + 1, y + 2)], BLUSH)
        if mouth: s.dot([((a + b) // 2, y + 2)], EYE)
        return s
    def render(s):
        im = Image.new('RGBA', (C, C), (0, 0, 0, 0)); P = im.load(); body = set()
        for m, c in s.layers:
            for q in m:
                if 0 <= q[0] < S and 0 <= q[1] < S: P[q[0] + 1, q[1] + 1] = c; body.add((q[0] + 1, q[1] + 1))
        for x in range(C):
            for y in range(C):
                if (x, y) not in body and any((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): P[x, y] = OL
        for q, c in s.top.items(): P[q[0] + 1, q[1] + 1] = c
        return im

F = []
# 1 호박: 데굴데굴
s = Spr().add(ell(7.5, 9.5, 7, 5), H('#F59A3A')).add(rect(7, 2, 7, 4), H('#4A7A2E')).add(px((8, 3), (9, 3), (9, 2)), H('#6EA040'))
s.dot([(4, y) for y in range(6, 14)] + [(10, y) for y in range(6, 14)], H('#D8782A')).dot([(2, 8), (2, 9)], H('#FFC070')).face(8, 5, 9); F.append(('pumpkin', '호박', s))
# 2 유령 시트: 스르륵 통과
s = Spr().add(ell(7.5, 6.5, 5.5, 5.5) | rect(2, 6, 12, 12) | {(x, 13) for x in range(2, 13) if x % 3 != 1}, H('#F4F2FF'))
s.dot([(12, y) for y in range(7, 13)], H('#D8D4EE')).dot([(4, 3), (5, 3)], HI).face(6, 5, 9); F.append(('ghost', '유령 시트', s))
# 3 젤리 슬라임: 물 위를 퐁퐁
s = Spr().add(ell(7.5, 10, 7, 4.5) | ell(7.5, 7.5, 5, 4), H('#7FD8B0')).dot([(x, 13) for x in range(2, 13)], H('#5FC090')).dot([(4, 5), (5, 5), (4, 6)], H('#C8FFE4')).dot([(11, 11)], H('#C8FFE4')).face(8, 5, 9); F.append(('slime', '젤리 슬라임', s))
# 4 양초: 어둠을 밝혀요
s = Spr().add(rect(4, 6, 10, 12), H('#F6EAD0')).add(rect(3, 13, 11, 14), H('#C8A050')).add(px((7, 4), (7, 5)), H('#3a3448')).add(px((7, 1), (6, 2), (7, 2), (8, 2), (7, 3)), H('#FFA640'))
s.dot([(7, 2)], H('#FFF0A0')).dot([(4, 7), (4, 8), (10, 7)], H('#FFFFFF')).face(8, 5, 9); F.append(('candle', '양초', s))
# 5 빗자루: 지붕 위를 날아요
s = Spr().add({(x, y) for y in range(7, 15) for x in range(5 - (y - 7) // 2, 10 + (y - 7) // 2)}, H('#D8B460')).add(rect(5, 5, 9, 6), H('#C84A3A')).add(px((10, 4), (11, 3), (12, 2), (13, 1), (14, 0)), H('#8A5A36'))
s.dot([(4, 13), (6, 14), (8, 13), (10, 14)], H('#B8903E')).face(9, 6, 8, blush=False); F.append(('broom', '빗자루', s))
# 6 찻주전자: 김으로 얼음을 녹여요
s = Spr().add(ell(7, 9.5, 5.5, 4.5), H('#8FB8E8')).add(rect(5, 4, 9, 5), H('#8FB8E8')).add(px((7, 3)), H('#C8DCF8')).add(px((0, 6), (1, 7), (2, 8)), H('#6A94C8')).add(px((13, 7), (14, 8), (14, 9), (13, 10)), H('#6A94C8'))
s.dot([(x, 12) for x in range(3, 12)], H('#F4F8FF')).dot([(4, 6)], HI).face(8, 5, 9); F.append(('teapot', '찻주전자', s))
# 7 해골: 묘지 철문을 덜그럭
s = Spr().add(ell(7.5, 6.5, 6, 5.5) | rect(4, 10, 11, 13), H('#F2EEE2'))
s.dot([(x, y) for x in (4, 5, 6) for y in (6, 7, 8)] + [(x, y) for x in (9, 10, 11) for y in (6, 7, 8)], H('#2a2030')).dot([(5, 6), (10, 6)], H('#9AE6FF')).dot([(7, 10), (8, 10)], H('#2a2030')).dot([(5, 12), (7, 12), (9, 12)], H('#B8B2A0')); F.append(('skull', '해골', s))
# 8 수정구슬: 숨은 재료를 반짝
s = Spr().add(ell(7.5, 6.5, 6, 6), H('#B8A0F0')).add(ell(7.5, 7, 4.5, 4.5), H('#D8C8FF')).add(rect(4, 12, 11, 14), H('#7A4A2E'))
s.dot([(4, 3), (5, 3), (4, 4)], HI).dot([(5, 13), (9, 13)], H('#A8744A')).face(6, 5, 9); F.append(('orb', '수정구슬', s))
# 9 마법책: 수수께끼 석판을 읽어요
s = Spr().add(rect(1, 6, 6, 12), H('#F6EED8')).add(rect(8, 6, 13, 12), H('#FFF8E8')).add(rect(0, 13, 14, 14) | rect(7, 5, 7, 14), H('#7A3AB8')).add(px((0, 12), (14, 12)), H('#7A3AB8'))
s.dot([(10, 10), (11, 10), (12, 10), (2, 11), (3, 11)], H('#C8B890')).dot([(3, 3), (11, 2)], H('#FFE070')).face(8, 4, 10, mouth=False).dot([(7, 10)], EYE); F.append(('book', '마법책', s))
# 10 버섯: 포자로 덩굴 다리
s = Spr().add(ell(7.5, 5, 7, 4.5) | rect(1, 5, 13, 6), H('#D84A6A')).add(rect(5, 7, 10, 14), H('#F4E8D0')).dot([(4, 3), (10, 2), (7, 1), (12, 5), (2, 5)], H('#FAF2E0')).dot([(x, 6) for x in range(1, 14)], H('#B03A58')).face(9, 6, 9); F.append(('mushroom', '버섯', s))
# 11 종: 석상 문지기를 깨워요
s = Spr().add({(x, y) for y in range(2, 12) for x in range(S) if abs(x + .5 - 7.5) <= 2 + (y - 2) * .5}, H('#F0C040')).add(rect(1, 12, 14, 13), H('#D8A030')).add(px((7, 14), (8, 14)), H('#8A6A20')).add(px((7, 0), (7, 1), (8, 1), (8, 0)), H('#C89030'))
s.dot([(5, y) for y in range(5, 10)], H('#FFE890')).face(6, 5, 9); F.append(('bell', '종', s))
# 12 거울: 빛으로 봉인을 풀어요
s = Spr().add(ell(7.5, 6.5, 6, 6.5), H('#C89A5A')).add(ell(7.5, 6.5, 4.5, 5), H('#BFE6FF')).add(rect(6, 13, 9, 14), H('#A8783A'))
s.dot([(5, 3), (6, 3), (5, 4), (9, 10)], HI).face(6, 5, 9); F.append(('mirror', '거울', s))
FORMS = [(k, n) for k, n, _ in F]

if __name__ == '__main__':
    sheet = Image.new('RGBA', (C * len(F), C), (0, 0, 0, 0))
    for i, (_, _, sp) in enumerate(F): sheet.alpha_composite(sp.render(), (i * C, 0))
    sheet.save('out/morph.png'); print('morph', sheet.size)
