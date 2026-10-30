# 장난 마법 「의문의 인물」: 새까만 후드를 쓴 수상한 사람 (변신·게시판과 같은 그림체) → out/shady.png (발 디딘 점: 아래 가운데)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from morph_obst import Spr, rect, H as C

s = Spr(18, 28)
cloak = {(x, y) for x in range(18) for y in range(10, 28) if abs(x - 8.5) <= 4.6 + (y - 10) * .24}
s.add(cloak, C('#1C1626'))
s.dot([(x, y) for (x, y) in cloak if y >= 26 and (x % 3 == 0)], C('#0E0A16'))                       # 너덜너덜한 밑단
s.dot([(x, y) for (x, y) in cloak if abs(x - 8.5) >= 3.6 + (y - 10) * .24 and x < 9], C('#352A48'))  # 왼쪽 가장자리 빛
s.dot([(8, y) for y in range(15, 26)] + [(9, y) for y in range(15, 26)], C('#120E1C'))               # 앞섶
hood = s.ell(8.5, 8, 6.6, 6.4) | {(x, y) for x in range(18) for y in range(0, 4) if abs(x - (10 + (3 - y) * .9)) <= .4 + y * .7}
s.add(hood, C('#221A30'))
s.dot([(x, y) for (x, y) in hood if x <= 4 and y <= 9], C('#3A2E50'))                                # 후드 빛
face = s.ell(8.5, 9, 3.8, 3.2); s.dot(face, C('#07040C'))
s.dot([(6, 8), (11, 8)], C('#FFE45A')); s.dot([(6, 7), (11, 7)], C('#FFF6B0'))                          # 빛나는 눈
s.dot([(6, 11), (7, 11), (10, 11), (11, 11), (8, 12), (9, 12)], C('#B8A8D8'))                         # 히죽 웃는 입
# 소매에서 나온 손 (입가를 가리고 쿡쿡)
s.dot([(12, 13), (13, 13), (12, 14), (13, 14), (14, 13)], C('#A898C0')); s.dot([(11, 15), (12, 15), (13, 15), (11, 16), (12, 16)], C('#2A2038'))
# 보라 마법 반짝이
s.dot([(16, 4), (15, 5), (16, 5), (17, 5), (16, 6)], C('#C890FF')); s.dot([(1, 14)], C('#C890FF')); s.dot([(2, 20)], C('#8A60D0'))

if __name__ == '__main__':
    im = s.render(); im.save('out/shady.png'); im.resize((im.width * 8, im.height * 8), 0).save('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/shady_big.png'); print(im.size)
