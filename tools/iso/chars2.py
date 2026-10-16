# 교복 학생 걷기 그림: 칸 14x24, 열 = [앞 서기, 앞 걷기1, 앞 걷기2, 뒤 서기, 뒤 걷기1, 뒤 걷기2], 행 = 생김새 8가지
from PIL import Image
def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (255,)
FRONT = ["....KKKKKK....", "...KAAAAAAK...", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAASAAASAK..", "..KASSSSSSAK..",
         "..KASESSESAK..", "..KASSSSSSAK..", "..KAPSSSSPAK..", "...KKSSSSKK...", "....KWWWWK....", "..KNNWRRWNNK..",
         ".KNNNWRRWNNNK.", ".KNNNNRRNNNNK.", ".KSNNNNNNNNSK.", ".KKNNNNNNNNKK.", "..KBBBBBBBBK..", "..KBBBBBBBBK..",
         "..KBBBBBBBBK..", "...KLLKKLLK..."]
BACK = ["....KKKKKK....", "...KAAAAAAK...", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAAAAAAAAK..",
        "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "...KKAAAAKK...", "....KNNNNK....", "..KNNNNNNNNK..",
        ".KNNNNNNNNNNK.", ".KNNNNNNNNNNK.", ".KSNNNNNNNNSK.", ".KKNNNNNNNNKK.", "..KBBBBBBBBK..", "..KBBBBBBBBK..",
        "..KBBBBBBBBK..", "...KLLKKLLK..."]
FEET = [["...KLLKKLLK...", "...KOOKKOOK...", "...KKKKKKKK...", ".............."],
        ["..KLLK..KLLK..", "..KOOK..KOOK..", "..KKKK..KKKK..", ".............."],
        ["....KLLKKLLK..", "....KOOKKOOK..", "....KKKKKKKK..", ".............."]]
# (머리색, 긴머리, 아래(치마/바지 색), 다리(피부/바지), 넥타이=기숙사 색)
LOOKS = [('#3A2A24', 1, '#4A4A6A', 'S', '#5CCB8E'), ('#E8C070', 0, '#3A3A52', 'B', '#F08A3C'),
         ('#1E1A24', 1, '#5A3A4A', 'S', '#E8709A'), ('#C85A3A', 0, '#3A3A52', 'B', '#7A66E0'),
         ('#6A4A3A', 0, '#4A4A6A', 'S', '#5CCB8E'), ('#2A2030', 1, '#3A3A52', 'B', '#7A66E0'),
         ('#A8784A', 1, '#5A3A4A', 'S', '#F08A3C'), ('#4A3A6A', 0, '#3A3A52', 'B', '#E8709A')]
SKIN, EYE, BLUSH, SHIRT, BLAZER, OUT, SHOE = hexc('#F6D2B0'), hexc('#2A1830'), hexc('#F0A0A0'), hexc('#F4F2EC'), hexc('#2E3A5E'), hexc('#1A0F14'), hexc('#3A2418')
def frame(look, back, step):
    hair, long_, bottom, leg, tie = LOOKS[look]
    rows = [list(r) for r in (BACK if back else FRONT)[:19]] + [list(r) for r in FEET[step]]
    if long_:   # 긴 머리: 어깨까지 양옆으로
        for y in range(9, 14):
            rows[y][2] = 'A'; rows[y][11] = 'A'
            if back:
                for x in range(3, 11): rows[y][x] = 'A' if y < 13 else rows[y][x]
    pal = {'K': OUT, 'A': hexc(hair), 'S': SKIN, 'E': EYE, 'P': BLUSH, 'W': SHIRT, 'N': BLAZER, 'R': hexc(tie), 'B': hexc(bottom),
           'L': SKIN if leg == 'S' else hexc(bottom), 'O': SHOE}
    im = Image.new('RGBA', (14, 24), (0, 0, 0, 0))
    bob = 1 if step else 0
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '.': continue
            yy = y + (bob if y < 19 else 0) + 1
            if 0 <= yy < 24: im.putpixel((x, yy), pal[ch])
    return im
sheet = Image.new('RGBA', (14 * 6, 24 * len(LOOKS)), (0, 0, 0, 0))
for l in range(len(LOOKS)):
    for c, (back, step) in enumerate(((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2))):
        sheet.paste(frame(l, back, step), (c * 14, l * 24))
sheet.save('out/students2.png'); sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save('out/students2_big.png')
