# 몬스터 학생: 마녀·뱀파이어·늑대인간·유령 (칸 14x24, 6열 x 8행)
from PIL import Image
exec(open('chars2.py').read().split("# (머리색")[0])   # FRONT, BACK, FEET, hexc 재사용
SKIN, EYE, BLUSH, SHIRT, OUT, SHOE = hexc('#F6D2B0'), hexc('#2A1830'), hexc('#F0A0A0'), hexc('#F4F2EC'), hexc('#1A0F14'), hexc('#2A1E1A')
BLAZER, TIE, SKIRT = hexc('#2A2236'), hexc('#E07A1E'), hexc('#4A2E5A')
HAT = ["......K.......", ".....KHK......", ".....KHHK.....", "....KHHHK.....", "....KHHHHK....", "...KHBBBBHK...", ".KKHHHHHHHHKK.", "KHHHHHHHHHHHHK"]
# (종족, 머리색, 특징색)
LOOKS = [('witch', '#5A3A2A', '#5A3A9A'), ('witch', '#E8C070', '#2E6A4E'),
         ('vamp', '#1E1A24', '#B02A3A'), ('vamp', '#D8D8E0', '#7A1A2A'),
         ('wolf', '#7A5232', '#7A5232'), ('wolf', '#8A8A92', '#6A6A72'),
         ('ghost', '#F2F6FF', '#C8D8FF'), ('ghost', '#E0D0FF', '#B8A8F0')]
def frame(look, back, step):
    kind, hair, feat = LOOKS[look]
    rows = [list(r) for r in (BACK if back else FRONT)[:19]] + [list(r) for r in FEET[step]]
    skin = SKIN
    pal = {'K': OUT, 'A': hexc(hair), 'S': skin, 'E': EYE, 'P': BLUSH, 'W': SHIRT, 'N': BLAZER, 'R': TIE, 'B': SKIRT, 'L': SKIN, 'O': SHOE, 'H': hexc(feat), 'C': hexc('#E0C070')}
    if kind == 'witch':       # 뾰족 모자를 머리 위에 (머리는 아래로 밀어요)
        rows = [list(r) for r in HAT] + rows[4:]
        rows = rows[:19] + [list(r) for r in FEET[step]]
        for y, r in enumerate(rows[:8]):
            rows[y] = [('C' if ch == 'B' else ch) for ch in r]
    elif kind == 'vamp':      # 창백한 피부, 빨간 눈, 망토(양옆 + 높은 깃)
        pal['S'] = hexc('#E8E2F0'); pal['L'] = hexc('#E8E2F0'); pal['E'] = hexc('#C8203A'); pal['P'] = hexc('#E8E2F0')
        for y in range(10, 19):
            rows[y][0] = 'K'; rows[y][1] = 'H' if not back else 'K'; rows[y][12] = 'H' if not back else 'K'; rows[y][13] = 'K'
            if back:
                for x in range(2, 12): rows[y][x] = 'K' if x in (2, 11) else 'D'
        pal['D'] = hexc('#1E1824')
        rows[9][2] = 'H'; rows[9][11] = 'H'
    elif kind == 'wolf':      # 늑대 귀 + 꼬리
        rows[0] = list("..K.KKKKKK.K..") ; rows[1] = list(".KAKAAAAAAKAK."); rows[2] = list(".KAAAAAAAAAAK.")
        for y in (15, 16, 17): rows[y][13] = 'A'
        rows[14][13] = 'K'; rows[18][13] = 'K'
    im = Image.new('RGBA', (14, 24), (0, 0, 0, 0))
    bob = 1 if step else 0
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '.': continue
            yy = y + (bob if y < 19 else 0) + 1
            if kind == 'ghost' and y >= 19: continue
            if 0 <= yy < 24: im.putpixel((x, yy), pal[ch])
    if kind == 'ghost':       # 반투명, 다리 대신 물결 꼬리, 동동
        g = Image.new('RGBA', (14, 24), (0, 0, 0, 0))
        for y in range(24):
            for x in range(14):
                c = im.getpixel((x, y))
                if c[3]:
                    l = (c[0] + c[1] + c[2]) // 3
                    if c[:3] == EYE[:3]: nc = (50, 50, 120, 240)
                    elif c[:3] == OUT[:3]: nc = (120, 130, 220, 230)
                    elif c[:3] == BLUSH[:3]: nc = (240, 180, 220, 200)
                    else: nc = (min(255, l // 3 + 170), min(255, l // 3 + 180), 255, 185)
                    g.putpixel((x, max(0, y - 2)), nc)
        for x in range(3, 11):
            yy = 18 + (1 if (x + step) % 3 == 0 else 0)
            g.putpixel((x, yy), (200, 215, 255, 170))
        im = g
    return im
sheet = Image.new('RGBA', (14 * 6, 24 * len(LOOKS)), (0, 0, 0, 0))
for l in range(len(LOOKS)):
    for c, (back, step) in enumerate(((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2))):
        sheet.paste(frame(l, back, step), (c * 14, l * 24))
sheet.save('out/students3.png'); sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save('out/students3_big.png')
