# 걷는 학생 스프라이트: 칸 14x24, 열 = [앞 서기, 앞 걷기1, 앞 걷기2, 뒤 서기, 뒤 걷기1, 뒤 걷기2], 행 = 생김새 8가지
from PIL import Image
def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (255,)
HEAD_F = ["......KK......", ".....KHHK.....", ".....KHHK.....", "....KHHHHK....", "....KHHHHK....", "...KHHHHHHK...",
          "...KHBBBBHK...", ".KKHHHHHHHHKK.", "KHHHHHHHHHHHHK", ".KKAAAAAAAAKK.", "..KAASSSSAAK..", "..KASESSESAK..",
          "..KASSSSSSAK..", "..KAPSSSSPAK..", "...KKSSSSKK..."]
HEAD_B = HEAD_F[:9] + [".KKAAAAAAAAKK.", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "..KAAAAAAAAK..", "...KKAAAAKK..."]
BODY_F = ["..KRRRWWRRRK..", ".KRRRRWWRRRRK.", ".KRRRRRRRRRRK.", ".KSRRRRRRRRSK.", ".KRRRRRRRRRRK.", "..KRRDDRRRRK..", "..KRRRRRRRRK.."]
BODY_B = ["..KRRRRRRRRK..", ".KRRRRRRRRRRK.", ".KRRRRRRRRRRK.", ".KSRRRRRRRRSK.", ".KRRRRRRRRRRK.", "..KRRRRRRRRK..", "..KRRRRRRRRK.."]
FEET = [["...KOOKKOOK...", "...KKK..KKK..."], ["..KOOK..KOOK..", "..KKK....KKK.."], ["....KOOKKOOK..", "....KKK..KKK.."]]
LOOKS = [  # 모자, 띠, 머리, 로브(기숙사 색), 신발
  ('#3A2E6A', '#C49446', '#5A3A2A', '#5E4AB0'), ('#2E5A3E', '#E0C070', '#E8C070', '#3E8A5A'),
  ('#7A3A24', '#E0C070', '#2A2030', '#C8682E'), ('#6A2E4A', '#C49446', '#C85A4A', '#C8507A'),
  ('#2A2A3A', '#8AB8FF', '#E8E0D0', '#4A4A7A'), ('#3A2E6A', '#FF9AC0', '#3A2A20', '#7A5AC8'),
  ('#2E4A3E', '#C49446', '#8A5A3A', '#4A9A6A'), ('#5A2A2A', '#E0C070', '#F0D890', '#B04A4A')]
SKIN, EYE, BLUSH, COLLAR, OUT = hexc('#F6D2B0'), hexc('#2A1830'), hexc('#F0A0A0'), hexc('#F2EAD8'), hexc('#1A0F14')
def frame(look, back, step):
    hat, band, hair, robe = map(hexc, LOOKS[look])
    rows = (HEAD_B if back else HEAD_F) + (BODY_B if back else BODY_F) + FEET[step]
    pal = {'K': OUT, 'H': hat, 'B': band, 'A': hair, 'S': SKIN, 'E': EYE, 'P': BLUSH, 'R': robe, 'W': COLLAR, 'D': tuple(max(0, v - 40) for v in robe[:3]) + (255,), 'O': hexc('#3A2418')}
    im = Image.new('RGBA', (14, 24), (0, 0, 0, 0))
    bob = 1 if step else 0
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.' and 0 <= y - (bob if y < 22 else 0) + bob < 24:
                yy = y + (0 if y >= 22 else -bob + 1) - 1 if step else y
                if 0 <= yy < 24: im.putpixel((x, yy), pal[ch])
    return im
sheet = Image.new('RGBA', (14 * 6, 24 * len(LOOKS)), (0, 0, 0, 0))
for l in range(len(LOOKS)):
    for c, (back, step) in enumerate(((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2))):
        sheet.paste(frame(l, back, step), (c * 14, l * 24))
sheet.save('out/students.png')
sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save('out/students_big.png')
