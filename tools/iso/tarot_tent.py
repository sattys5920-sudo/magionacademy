# 광장 점술 천막 (오늘의 운세 카드): 게시판(morph_obst.py)과 같은 그림체 → out/tarot_tent.png (발 디딘 점: 아래 가운데)
import os, math
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from morph_obst import Spr, rect, H as C

s = Spr(40, 44)
# 천막 몸: 줄무늬 (보라 · 남색)
body = {(x, y) for x in range(40) for y in range(14, 44) if abs(x - 19.5) <= 12 + (y - 14) * .25}
s.add(body, C('#5A3496'))
s.dot([(x, y) for (x, y) in body if (x // 3) % 2 == 0], C('#3A2A63'))
# 지붕: 둥근 꼭대기
roof = {(x, y) for x in range(40) for y in range(2, 16) if abs(x - 19.5) <= (y - 2) * 1.05 + .5}
s.add(roof, C('#7A48C8')); s.dot([(x, y) for (x, y) in roof if ((x - 19.5) // 3) % 2 == 0], C('#5A3496'))
s.dot([(x, y) for (x, y) in roof if abs(x - 19.5) >= (y - 2) * 1.05 - .5], C('#B890F0'))   # 지붕 가장자리 빛
# 술 장식 띠 (물결)
for x in range(4, 36):
    y = 15 + (1 if x % 4 in (1, 2) else 0); s.dot([(x, y), (x, y + 1)], C('#F2C450'))
    if x % 4 == 2: s.dot([(x, y + 2)], C('#F2C450'))
# 입구: 걷어 올린 휘장 사이로 안쪽
door = {(x, y) for x in range(40) for y in range(20, 44) if abs(x - 19.5) <= 3 + (y - 20) * .42}
s.dot(door, C('#1E1638'))
s.dot([(x, y) for (x, y) in door if abs(x - 19.5) > 2 + (y - 20) * .42], C('#2A1E4A'))
s.dot([(int(19.5 - 3 - (y - 20) * .42), y) for y in range(20, 44)] + [(int(19.5 + 3 + (y - 20) * .42) + 1, y) for y in range(20, 44)], C('#F2C450'))   # 휘장 끈
# 탁자 + 수정구슬
s.dot([(x, y) for x in range(14, 26) for y in range(36, 41)], C('#B4608A')); s.dot([(x, 36) for x in range(14, 26)], C('#E880A8')); s.dot([(x, 40) for x in range(14, 26) if x % 2 == 0], C('#F2C450'))
ball = {(x, y) for x in range(15, 25) for y in range(28, 37) if (x + .5 - 19.5) ** 2 + (y + .5 - 32.5) ** 2 <= 13}
s.dot(ball, C('#8FD8F8')); s.dot([(18, 30), (18, 31), (19, 30)], C('#FFFFFF')); s.dot([(21, 34), (22, 33)], C('#C8F0FF'))
# 꼭대기 별 깃대
s.add(rect(19, 0, 20, 3), C('#B8862E'))
s.dot([(19, 0), (20, 0)], C('#FFE070'))
# 옆에 걸린 등불
s.add(rect(3, 22, 6, 26), C('#2A1E3A')); s.dot([(4, 23), (5, 23), (4, 24), (5, 24), (4, 25), (5, 25)], C('#FFB040')); s.dot([(4, 23)], C('#FFF0A0'))
s.add(rect(33, 22, 36, 26), C('#2A1E3A')); s.dot([(34, 23), (35, 23), (34, 24), (35, 24), (34, 25), (35, 25)], C('#FFB040')); s.dot([(34, 23)], C('#FFF0A0'))
# 별 간판
s.dot([(31, 31), (30, 32), (31, 32), (32, 32), (31, 33)], C('#FFE070'))

if __name__ == '__main__':
    im = s.render(); im.save('out/tarot_tent.png'); print('tent', im.size)
