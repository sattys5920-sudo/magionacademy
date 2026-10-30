# 사역마 12종 (시안): 따라다니며 말을 거는 마법 동반자 · 변신·게시판과 같은 그림체 → out/familiars.png (24×24 칸 12개) + 미리보기
import os
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from morph_obst import Spr, rect, H as C
EYE = C('#2A1830'); HI = C('#FFFFFF')
def eyes(s, pts, hi=True):
    s.dot(pts, EYE)
    if hi: s.dot([(x, y - 1) for x, y in pts[::2]], HI) if False else None
def blush(s, pts): s.dot(pts, C('#FF9AB8'))
OUT = []

# 1 심지: 촛불 도깨비불 (불)
s = Spr(22, 22); s.add(rect(7, 15, 14, 21), C('#F2E6C8')).add(rect(7, 15, 14, 15), C('#FFF6DE'))
s.add(s.ell(11, 10, 6.5, 6.5) | {(x, y) for x in range(22) for y in range(0, 6) if abs(x - 11) <= (y) * .9}, C('#FF8A3A')).add(s.ell(11, 11, 4.5, 4.5), C('#FFD060'))
s.dot([(9, 11), (13, 11)], EYE); s.dot([(10, 13), (11, 13), (12, 13)], C('#C84A2E')); blush(s, [(8, 12), (14, 12)]); s.dot([(16, 17), (17, 17)], C('#F2C450'))
OUT.append(('simji', '심지', s))
# 2 먹방울: 잉크 박쥐
s = Spr(24, 18); s.add(s.ell(12, 9, 5.5, 5.5), C('#2A2440'))
s.add({(x, y) for x in range(0, 8) for y in range(4, 12) if y - 4 >= (7 - x) * .6 and y <= 10 - (x % 3 == 0)}, C('#3A3460')).add({(x, y) for x in range(16, 24) for y in range(4, 12) if y - 4 >= (x - 16) * .6 and y <= 10 - (x % 3 == 2)}, C('#3A3460'))
s.add({(9, 3), (9, 2), (10, 3)} | {(15, 3), (15, 2), (14, 3)}, C('#2A2440')); s.dot([(10, 8), (14, 8)], C('#FFE070')); s.dot([(12, 11)], C('#FF9AB8')); s.dot([(12, 15), (12, 16), (11, 16)], C('#3A6AE8'))
OUT.append(('meok', '먹방울', s))
# 3 홍차: 찻잔 유령
s = Spr(22, 22); s.add(s.ell(11, 8, 6, 6) | rect(5, 8, 16, 14), C('#F4F0FF')); s.dot([(5, 14), (7, 15), (9, 14), (11, 15), (13, 14), (15, 15)], C('#F4F0FF'))
s.add(rect(4, 14, 17, 19) | s.ell(10.5, 19, 7, 2), C('#E890A8')).add(rect(17, 15, 19, 17), C('#E890A8')).add(rect(4, 14, 17, 14), C('#F8B8C8'))
s.dot([(8, 8), (13, 8)], EYE); blush(s, [(7, 10), (14, 10)]); s.dot([(10, 10), (11, 10)], C('#B87AA8')); s.dot([(x, 17) for x in range(6, 16, 3)], C('#FFFFFF'))
OUT.append(('hongcha', '홍차', s))
# 4 유성: 별똥 여우
s = Spr(24, 20); s.add(s.ell(11, 12, 6, 5), C('#6A5AC8')).add(s.ell(8, 7, 4.5, 4), C('#6A5AC8'))
s.add({(4, 2), (4, 3), (5, 3), (5, 4)} | {(10, 2), (10, 3), (9, 3), (9, 4)}, C('#6A5AC8')).add({(x, y) for x in range(16, 24) for y in range(4, 16) if abs(y - 10 + (x - 16) * .5) <= 2.6 - (x - 16) * .2}, C('#8A7AE8'))
s.dot([(22, 6), (23, 5), (21, 5), (22, 4)], C('#FFE070')); s.dot([(7, 7), (10, 7)], C('#FFE070')); s.dot([(8, 9)], EYE); s.dot([(7, 14), (12, 15), (15, 13)], C('#FFF6B0'))
OUT.append(('yuseong', '유성', s))
# 5 잭: 호박등 꼬마
s = Spr(22, 22); s.add(s.ell(11, 11, 8.5, 7), C('#F28A2A')).add(rect(10, 1, 12, 4), C('#5E8A3E'))
s.dot([(x, y) for x in (7, 11, 15) for y in range(6, 17)], C('#D8701E')); s.dot([(7, 9), (8, 9), (8, 8), (14, 9), (15, 9), (14, 8)], C('#FFE070')); s.dot([(8, 13), (9, 14), (10, 13), (11, 14), (12, 13), (13, 14), (14, 13)], C('#FFE070'))
s.add(rect(7, 18, 9, 21) | rect(13, 18, 15, 21), C('#3A2A4A')); s.dot([(13, 2), (14, 1)], C('#7AAA4E'))
OUT.append(('jack', '잭', s))
# 6 루나: 달빛 나방
s = Spr(24, 20); s.add(s.ell(6, 9, 6, 7) | s.ell(18, 9, 6, 7), C('#C8D8FF')).add(s.ell(6, 9, 3, 3.5) | s.ell(18, 9, 3, 3.5), C('#8AA0E8'))
s.add(s.ell(12, 10, 3, 6), C('#F4F0E8')).add({(10, 2), (9, 1), (14, 2), (15, 1)}, C('#F4F0E8')); s.dot([(11, 8), (13, 8)], EYE); s.dot([(6, 9), (18, 9)], C('#FFF6B0')); s.dot([(12, 12), (12, 14)], C('#D8C8A8'))
OUT.append(('luna', '루나', s))
# 7 포실: 버섯 요정
s = Spr(22, 22); s.add(s.ell(11, 8, 9, 6) - {(x, y) for x in range(22) for y in range(9, 22)}, C('#E85A6A')).add(rect(3, 8, 19, 9), C('#F27A88'))
s.dot([(6, 4), (7, 4), (12, 3), (15, 5), (16, 5), (9, 6)], C('#FFF6EE')); s.add(rect(6, 10, 16, 19) | s.ell(11, 19, 5, 2), C('#F6E6D0'))
s.dot([(9, 13), (13, 13)], EYE); blush(s, [(8, 15), (14, 15)]); s.dot([(10, 16), (11, 16), (12, 16)], C('#C86A6A'))
OUT.append(('posil', '포실', s))
# 8 까악: 해골 까마귀
s = Spr(22, 22); s.add(s.ell(11, 12, 7, 7), C('#2A2A3A')).add({(x, y) for x in range(2, 7) for y in range(10, 16) if x + (15 - y) * .5 > 3}, C('#3A3A4E'))
s.add(s.ell(12, 8, 4.5, 4), C('#F2EEE4')); s.dot([(10, 8), (14, 8)], EYE); s.add(rect(16, 9, 19, 10), C('#F2C450')).add({(19, 10), (20, 10)}, C('#F2C450'))
s.dot([(9, 19), (13, 19)], C('#F2C450')); s.dot([(11, 2), (12, 3), (10, 3)], C('#2A2A3A')); s.dot([(15, 15)], C('#F2C450'))
OUT.append(('kkak', '까악', s))
# 9 몽글: 거품 해파리
s = Spr(22, 24); s.add(s.ell(11, 8, 8, 7) - {(x, y) for x in range(22) for y in range(10, 24)}, C('#9AD8F8')).add(rect(3, 8, 19, 10), C('#B8E8FF'))
for x in (5, 8, 11, 14, 17): s.add({(x, y) for y in range(11, 20 + (x % 2) * 2)}, C('#7AC0F0'))
s.dot([(8, 6), (14, 6)], EYE); blush(s, [(7, 8), (15, 8)]); s.dot([(5, 3), (6, 3)], HI); s.dot([(18, 1), (20, 3)], C('#DFF6FF'))
OUT.append(('monggeul', '몽글', s))
# 10 책벌레: 마법책 미믹
s = Spr(24, 20); s.add({(x, y) for x in range(2, 22) for y in range(4, 18) if y >= 4 + abs(x - 12) * .25}, C('#7A3A5A')).add(rect(2, 15, 21, 17), C('#5A2A44'))
s.add({(x, y) for x in range(4, 20) for y in range(5, 12) if y >= 5 + abs(x - 12) * .25}, C('#F6EAD2')); s.dot([(12, y) for y in range(6, 12)], C('#C8B08A'))
s.dot([(8, 8), (16, 8)], EYE); s.add(rect(10, 12, 14, 15), C('#E85A7A')); s.dot([(9, 12), (11, 13), (13, 13), (15, 12)], C('#FFFFFF')); s.dot([(3, 14), (20, 14)], C('#F2C450'))
OUT.append(('bookworm', '책벌레', s))
# 11 솜바람: 구름 고양이
s = Spr(24, 20); s.add(s.ell(12, 12, 9, 5.5) | s.ell(8, 9, 4.5, 4) | s.ell(15, 8, 5, 4.5), C('#FFFFFF'))
s.add({(9, 3), (9, 4), (10, 4), (15, 3), (15, 4), (14, 4)}, C('#FFFFFF')); s.dot([(x, 17) for x in range(5, 20)], C('#D4DEF8'))
s.dot([(10, 9), (15, 9)], EYE); blush(s, [(9, 11), (16, 11)]); s.dot([(12, 11), (13, 11)], C('#F4A0A0')); s.dot([(21, 10), (22, 9), (23, 8)], C('#C8D8FF'))
OUT.append(('sombaram', '솜바람', s))
# 12 철컥: 자물쇠 골렘
s = Spr(22, 22); s.add(s.ell(11, 6, 6, 6) - s.ell(11, 6, 3.5, 3.5) - {(x, y) for x in range(22) for y in range(8, 22)}, C('#9AA4B4'))
s.add(rect(4, 8, 17, 18), C('#F2C450')).add(rect(4, 8, 17, 9), C('#FFE08A')).add(rect(4, 17, 17, 18), C('#C89A3A'))
s.dot([(8, 12), (13, 12)], EYE); s.add({(10, 14), (11, 14), (10, 15), (11, 15), (10, 16)}, C('#3A2A4A')); s.add(rect(5, 19, 7, 21) | rect(14, 19, 16, 21), C('#9AA4B4'))
OUT.append(('cheolkeok', '철컥', s))

if __name__ == '__main__':
    ims = [(k, n, sp.render()) for k, n, sp in OUT]
    S = 26; sheet = Image.new('RGBA', (S * len(ims), S), (0, 0, 0, 0))
    for i, (k, n, im) in enumerate(ims): sheet.paste(im, (i * S + (S - im.width) // 2, S - im.height), im)
    sheet.save('out/familiars.png'); print('familiars', sheet.size, [k for k, _, _ in ims])
