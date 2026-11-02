# 맨디의 꽃말 수첩 · 꽃말 쪽지 그림 (게임 그림체: 진한 보라 테두리 · 위 밝게 · 아래 그늘)
from PIL import Image
OL = (42, 26, 46, 255)
def img(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))
def rect(im, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): im.putpixel((x, y), c)
def outline(im):
    w, h = im.size; src = im.copy()
    for y in range(h):
        for x in range(w):
            if src.getpixel((x, y))[3]: continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X, Y = x + dx, y + dy
                if 0 <= X < w and 0 <= Y < h and src.getpixel((X, Y))[3] and src.getpixel((X, Y)) != OL:
                    im.putpixel((x, y), OL); break
def px(im, pts, c):
    for x, y in pts: im.putpixel((x, y), c)
G1, G2, G3, G4 = (120, 186, 104, 255), (94, 154, 82, 255), (66, 116, 62, 255), (46, 84, 48, 255)
CR1, CR2, CR3 = (255, 248, 230, 255), (240, 226, 196, 255), (214, 194, 156, 255)
PK1, PK2 = (255, 143, 175, 255), (214, 92, 128, 255)
YL = (255, 216, 102, 255); BR = (150, 106, 70, 255)

# 1) 수첩 아이콘 32 × 32
nb = img(32, 32)
rect(nb, 7, 5, 25, 27, CR2); rect(nb, 24, 6, 25, 26, CR3)                    # 종이 옆면
rect(nb, 5, 4, 23, 27, G2); rect(nb, 5, 4, 7, 27, G4)                         # 겉표지 · 책등
rect(nb, 8, 4, 23, 5, G1); rect(nb, 8, 26, 23, 27, G3)                        # 위 밝게 · 아래 그늘
for y in range(7, 26, 3): px(nb, [(6, y)], G3)                                # 책등 실밥
for y in range(6, 26):                                                        # 표지 명암: 왼쪽 위 밝게
    for x in range(8, 23):
        if x + y < 20: nb.putpixel((x, y), G1)
        elif x + y > 44 and (x + y) % 2 == 0: nb.putpixel((x, y), G3)
for x in range(9, 23, 2): px(nb, [(x, 7), (x, 24)], G1)                       # 바느질 점선
SK, SK2 = (238, 214, 170, 255), (206, 176, 128, 255)                          # 맨디 얼굴 스티커
for y in range(10, 20):
    for x in range(10, 21):
        if (x - 15) ** 2 + (y - 15) ** 2 <= 22: nb.putpixel((x, y), SK)
        if (x - 15) ** 2 + (y - 15) ** 2 <= 22 and y >= 18: nb.putpixel((x, y), SK2)
px(nb, [(13, 15), (17, 15)], OL); px(nb, [(14, 17), (15, 17), (16, 17)], (150, 90, 80, 255)); px(nb, [(12, 16), (18, 16)], PK1)
px(nb, [(15, 9), (14, 8), (16, 8), (13, 7), (17, 7), (15, 8)], G1); px(nb, [(14, 7), (16, 7)], G1)   # 머리 잎
rect(nb, 12, 20, 18, 20, G4); rect(nb, 12, 22, 16, 22, G3)                    # 글씨 줄
rect(nb, 20, 2, 21, 8, PK1); px(nb, [(20, 9), (21, 10)], PK1); px(nb, [(21, 2), (21, 3)], PK2)  # 책갈피 리본
px(nb, [(9, 24), (10, 24), (9, 25)], PK1)                                     # 꽃잎 하나 끼워 둠
outline(nb); nb.save('art/note_icon.png')

# 2) 꽃말 쪽지 아이콘 32 × 32 (찢어진 종이 · 눌린 꽃 · 접힌 귀퉁이)
pg = img(32, 32)
for y in range(6, 27):
    l = 7 + (1 if y % 5 == 0 else 0); r = 24 - (1 if y % 4 == 1 else 0)          # 찢긴 가장자리
    for x in range(l, r + 1): pg.putpixel((x, y), CR1)
for x in range(7, 25): pg.putpixel((x, 26), CR3); pg.putpixel((x, 25), CR2)
for y in range(6, 11):
    for x in range(20 + (y - 6), 25): pg.putpixel((x, y), (0, 0, 0, 0))
px(pg, [(20, 6), (20, 7), (21, 7), (20, 8), (21, 8), (22, 8), (20, 9), (21, 9), (22, 9), (23, 9), (20, 10), (21, 10), (22, 10), (23, 10), (24, 10)], CR3)  # 접힌 귀
px(pg, [(13, 10), (12, 11), (14, 11), (13, 12), (11, 12), (15, 12), (12, 13), (14, 13)], PK1); px(pg, [(13, 11), (13, 13)], YL)  # 눌린 꽃
px(pg, [(13, 14), (13, 15), (13, 16), (14, 15)], G2)
for y, w in ((19, 12), (21, 10), (23, 8)): rect(pg, 10, y, 10 + w, y, (176, 150, 120, 255))  # 글씨 줄
TP = (200, 230, 210, 200)                                                     # 위에 붙인 테이프
rect(pg, 12, 4, 18, 7, TP)
px(pg, [(9, 22), (10, 21), (11, 22), (10, 23)], G2)                           # 맨디 잎 도장
for y in range(7, 26):                                                        # 종이 그늘 (아래 오른쪽)
    for x in range(8, 24):
        c = pg.getpixel((x, y))
        if c == CR1 and x + y > 40 and (x + y) % 2: pg.putpixel((x, y), CR2)
outline(pg); pg.save('art/page_icon.png')

# 3) 펼친 수첩 112 × 72 (왼쪽: 꽃 칸 · 오른쪽: 맨디 글씨)
op = img(112, 72)
rect(op, 2, 4, 109, 69, G2); rect(op, 2, 4, 109, 6, G1); rect(op, 2, 67, 109, 69, G3)   # 겉표지
rect(op, 6, 8, 54, 65, CR1); rect(op, 57, 8, 105, 65, CR1)                    # 두 쪽
rect(op, 52, 8, 54, 65, CR2); rect(op, 57, 8, 59, 65, CR2); rect(op, 55, 6, 56, 67, G4)  # 가운데 접힘
rect(op, 6, 63, 54, 65, CR2); rect(op, 57, 63, 105, 65, CR2)
rect(op, 14, 14, 45, 45, CR2); rect(op, 15, 15, 44, 44, (250, 240, 216, 255))  # 꽃 붙이는 칸
for x in range(14, 46, 2): op.putpixel((x, 14), CR3); op.putpixel((x, 45), CR3)
blank = op.copy()                                                              # 글씨 줄 없는 판 (화면에서 글씨를 얹어요)
rect(op, 12, 50, 40, 51, G4); rect(op, 12, 55, 32, 55, G3)                    # 이름 · 꽃말 줄
for i, w in enumerate((38, 34, 40, 30, 36, 22)): rect(op, 63, 14 + i * 7, 63 + w, 14 + i * 7, (176, 150, 120, 255))
px(op, [(98, 54), (97, 55), (99, 55), (98, 56), (98, 57), (98, 58), (97, 57)], G2)        # 맨디 서명 새싹
rect(op, 92, 0, 95, 12, PK1); px(op, [(92, 13), (95, 13), (93, 12), (94, 12)], PK2)       # 책갈피
outline(op); op.save('art/note_open.png')
for im_ in (blank,):
    px(im_, [(98, 54), (97, 55), (99, 55), (98, 56), (98, 57), (98, 58), (97, 57)], G2); rect(im_, 92, 0, 95, 12, PK1); px(im_, [(92, 13), (95, 13), (93, 12), (94, 12)], PK2); outline(im_); im_.save('art/note_open_blank.png')

# 미리 보기 (4 배)
bg = Image.new('RGBA', (32 * 4 * 2 + 112 * 4 + 48, 72 * 4 + 16), (43, 31, 69, 255))
bg.alpha_composite(nb.resize((128, 128), Image.NEAREST), (8, 8))
bg.alpha_composite(pg.resize((128, 128), Image.NEAREST), (8 + 128 + 16, 8))
bg.alpha_composite(op.resize((448, 288), Image.NEAREST), (8 + 128 * 2 + 32, 8))
bg.save('art/preview_art.png')
