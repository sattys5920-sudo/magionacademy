# 「마녀 솥 대폭발」 변신 12종 (도트 · 한 칸 24×30, 귀여운 얼굴) → out/morph.png (가로 12칸) · 걸을 때 콩콩 뛰어요
import math, os
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 24, 30
OUTL = (18, 10, 24, 255)
def C(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def new(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def outline(im):
    P = im.load(); add = []
    for y in range(H):
        for x in range(W):
            if P[x, y][3] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and P[x + dx, y + dy][3] > 200 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for x, y in add: P[x, y] = OUTL
    return im
def face(d, cx, y, gap=3, col='#1a1024', blush=True):
    for x in (cx - gap, cx + gap - 1): d.rectangle([x, y, x, y + 1], fill=C(col)); d.point((x, y), fill=C('#ffffff'))
    if blush: d.point((cx - gap - 1, y + 2), fill=C('#ff9ab8')); d.point((cx + gap, y + 2), fill=C('#ff9ab8'))
    d.point((cx - 1, y + 2), fill=C(col)); d.point((cx, y + 2), fill=C(col))

def pumpkin(d):   # 1 호박: 데굴데굴 빨라요
    for dx, c in ((-5, '#E07A2A'), (5, '#E07A2A'), (0, '#F59A3A')): d.ellipse([12 + dx - 6, 13, 12 + dx + 6, 27], fill=C(c))
    d.line([(9, 15), (9, 26)], fill=C('#C8601E')); d.line([(15, 15), (15, 26)], fill=C('#C8601E')); d.rectangle([11, 9, 12, 13], fill=C('#4A7A2E')); d.ellipse([13, 9, 17, 12], fill=C('#6EA040'))
    face(d, 12, 18)
def ghost(d):     # 2 유령 시트: 담장·덤불 통과
    d.ellipse([4, 6, 20, 22], fill=C('#F4F2FF')); d.rectangle([4, 14, 20, 25], fill=C('#F4F2FF'))
    for k in range(4): d.ellipse([4 + k * 4, 23, 8 + k * 4, 28], fill=C('#F4F2FF'))
    d.ellipse([6, 8, 11, 12], fill=C('#FFFFFF')); face(d, 12, 14)
def slime(d):     # 3 젤리 슬라임: 물 위를 퐁퐁
    d.ellipse([3, 12, 21, 28], fill=C('#7FD8B0')); d.rectangle([3, 21, 21, 27], fill=C('#7FD8B0')); d.ellipse([3, 24, 21, 29], fill=C('#5FC090'))
    d.ellipse([6, 14, 11, 18], fill=C('#C8FFE4')); d.point((17, 23), fill=C('#C8FFE4')); face(d, 12, 19)
def candle(d):    # 4 양초: 어두운 곳을 밝혀요
    d.rectangle([7, 12, 16, 27], fill=C('#F6EAD0')); d.ellipse([7, 10, 16, 14], fill=C('#FFF6E4')); d.ellipse([5, 25, 18, 29], fill=C('#C8A050'))
    d.line([(9, 14), (9, 19)], fill=C('#FFF6E4')); d.line([(11, 6), (11, 10)], fill=C('#3a3448'))
    d.polygon([(11, 1), (14, 6), (11, 9), (8, 6)], fill=C('#FFB040')); d.polygon([(11, 4), (12, 6), (11, 8), (10, 6)], fill=C('#FFF0A0')); face(d, 12, 17)
def broom(d):     # 5 빗자루: 지붕 위를 날아요
    d.line([(17, 3), (10, 17)], fill=C('#8A5A36'), width=2); d.polygon([(6, 16), (13, 15), (17, 27), (3, 27)], fill=C('#D8B460'))
    for x in (5, 8, 11, 14): d.line([(x + 1, 18), (x, 27)], fill=C('#B8903E')); d.rectangle([7, 15, 13, 17], fill=C('#C84A3A')); face(d, 10, 20, blush=False)
def teapot(d):    # 6 찻주전자: 김으로 얼음을 녹여요
    d.ellipse([4, 12, 20, 27], fill=C('#8FB8E8')); d.rectangle([9, 9, 15, 13], fill=C('#8FB8E8')); d.ellipse([10, 6, 14, 10], fill=C('#C8DCF8'))
    d.arc([17, 14, 23, 22], 270, 90, fill=C('#6A94C8'), width=2); d.polygon([(5, 17), (0, 13), (1, 12), (6, 15)], fill=C('#6A94C8'))
    d.line([(6, 22), (18, 22)], fill=C('#F4F8FF')); d.ellipse([1, 8, 3, 10], fill=C('#FFFFFF', 200)); face(d, 12, 16)
def skull(d):     # 7 해골: 묘지 철문을 덜그럭 지나가요
    d.ellipse([4, 5, 20, 20], fill=C('#F2EEE2')); d.rectangle([7, 17, 17, 23], fill=C('#F2EEE2')); d.ellipse([6, 25, 18, 29], fill=C('#D8D2C0'))
    for x in (9, 12, 15): d.line([(x, 20), (x, 23)], fill=C('#B8B2A0'))
    d.ellipse([6, 10, 10, 14], fill=C('#2a2030')); d.ellipse([14, 10, 18, 14], fill=C('#2a2030')); d.point((7, 11), fill=C('#9AE6FF')); d.point((15, 11), fill=C('#9AE6FF')); d.polygon([(12, 15), (11, 17), (13, 17)], fill=C('#2a2030'))
def orb(d):       # 8 수정구슬: 근처 숨은 재료를 반짝 보여 줘요
    d.polygon([(5, 25), (19, 25), (17, 29), (7, 29)], fill=C('#7A4A2E')); d.ellipse([3, 6, 21, 25], fill=C('#B8A0F0')); d.ellipse([6, 9, 18, 22], fill=C('#D8C8FF'))
    d.ellipse([6, 8, 10, 12], fill=C('#FFFFFF')); d.point((16, 19), fill=C('#FFFFFF')); face(d, 12, 14)
def book(d):      # 9 마법책: 수수께끼 석판을 읽어요
    d.polygon([(2, 12), (12, 15), (12, 28), (2, 25)], fill=C('#7A3AB8')); d.polygon([(22, 12), (12, 15), (12, 28), (22, 25)], fill=C('#8A4AC8'))
    d.polygon([(4, 12), (12, 14), (12, 26), (4, 23)], fill=C('#F6EED8')); d.polygon([(20, 12), (12, 14), (12, 26), (20, 23)], fill=C('#FFF8E8'))
    for y in (17, 20): d.line([(14, y), (18, y - 1)], fill=C('#C8B890'))
    d.point((7, 9), fill=C('#FFE070')); d.point((17, 8), fill=C('#FFE070')); face(d, 8, 16, gap=2, blush=False)
def mushroom(d):  # 10 버섯: 가만히 있으면 숨고, 포자로 덩굴 길을 만들어요
    d.rectangle([8, 17, 16, 28], fill=C('#F4E8D0')); d.ellipse([7, 25, 17, 29], fill=C('#E8D8B8'))
    d.ellipse([2, 6, 22, 20], fill=C('#C84A6A')); d.rectangle([2, 14, 22, 17], fill=C('#A83A58'))
    for x, y in ((7, 9), (14, 8), (18, 13), (5, 14)): d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=C('#FAF2E0')); face(d, 12, 20)
def bell(d):      # 11 종: 울려서 잠든 석상 문지기를 깨워요
    d.polygon([(12, 5), (19, 12), (21, 24), (3, 24), (5, 12)], fill=C('#F0C040')); d.ellipse([3, 21, 21, 27], fill=C('#D8A030')); d.ellipse([10, 25, 14, 29], fill=C('#8A6A20'))
    d.rectangle([10, 2, 13, 5], fill=C('#C89030')); d.line([(7, 12), (6, 20)], fill=C('#FFE890')); face(d, 12, 15)
def mirror(d):    # 12 거울: 빛을 반사해 봉인을 풀어요
    d.ellipse([4, 3, 20, 24], fill=C('#C89A5A')); d.ellipse([6, 5, 18, 22], fill=C('#BFE6FF')); d.line([(8, 8), (11, 6)], fill=C('#FFFFFF')); d.line([(8, 11), (14, 6)], fill=C('#FFFFFF'))
    d.rectangle([10, 23, 13, 26], fill=C('#A8783A')); d.ellipse([6, 25, 17, 29], fill=C('#A8783A')); face(d, 12, 13)

FORMS = [('pumpkin', '호박', pumpkin), ('ghost', '유령 시트', ghost), ('slime', '젤리 슬라임', slime), ('candle', '양초', candle), ('broom', '빗자루', broom), ('teapot', '찻주전자', teapot),
         ('skull', '해골', skull), ('orb', '수정구슬', orb), ('book', '마법책', book), ('mushroom', '버섯', mushroom), ('bell', '종', bell), ('mirror', '거울', mirror)]
if __name__ == '__main__':
    sheet = Image.new('RGBA', (W * len(FORMS), H), (0, 0, 0, 0))
    for i, (_, _, f) in enumerate(FORMS): im = new(); f(ImageDraw.Draw(im)); outline(im); sheet.alpha_composite(im, (i * W, 0))
    sheet.save('out/morph.png'); print('morph', sheet.size)
