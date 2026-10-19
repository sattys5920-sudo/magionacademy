# 쉬기 화면 침대 (픽셀, 96×56): rest_bed.png 뒤쪽(머리판·매트리스·베개) + rest_quilt.png 앞쪽(이불)
# 캐릭터는 index.html showRest에서 둘 사이에 눕혀 그려요. python3 tools/iso/rest_art.py
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H = 96, 56
K = (34, 22, 50, 255)
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
def img(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def rect(im, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < W and 0 <= y < H: im.putpixel((x, y), c)
def outline(im):
    src = im.copy(); s = src.load(); d = im.load()
    for y in range(H):
        for x in range(W):
            if s[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and s[x + dx, y + dy][3] and s[x + dx, y + dy] != K for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): d[x, y] = K
WOOD, WOOD_D, WOOD_L, WOOD_DD = hx('#9A6A44'), hx('#7A4E30'), hx('#B8875A'), hx('#5A3A24')
# ---- 뒤쪽 ----
bed = img()
# 머리판 (둥근 위, 가운데 판자 + 호박 장식)
rect(bed, 3, 16, 12, 53, WOOD); rect(bed, 4, 14, 11, 15, WOOD); rect(bed, 5, 13, 10, 13, WOOD)
rect(bed, 3, 16, 4, 53, WOOD_D); rect(bed, 11, 16, 12, 53, WOOD_D); rect(bed, 6, 15, 9, 15, WOOD_L)
for y in (22, 30, 38): rect(bed, 5, y, 10, y, WOOD_D)
rect(bed, 6, 18, 9, 20, hx('#F08A2A')); rect(bed, 7, 17, 8, 17, hx('#5AB85A')); rect(bed, 7, 19, 7, 19, hx('#5A2A10')); rect(bed, 8, 19, 8, 19, hx('#5A2A10'))
# 발판
rect(bed, 85, 28, 91, 53, WOOD); rect(bed, 86, 27, 90, 27, WOOD); rect(bed, 85, 28, 85, 53, WOOD_L); rect(bed, 90, 28, 91, 53, WOOD_D)
for y in (34, 42): rect(bed, 86, y, 89, y, WOOD_D)
# 매트리스 (흰 시트) + 옆판
rect(bed, 13, 34, 84, 41, hx('#F2EAD8')); rect(bed, 13, 34, 84, 34, hx('#FFFFFF')); rect(bed, 13, 40, 84, 41, hx('#D8CCE0'))
rect(bed, 13, 42, 84, 49, WOOD); rect(bed, 13, 42, 84, 42, WOOD_L); rect(bed, 13, 48, 84, 49, WOOD_D)
for x in range(18, 84, 11): rect(bed, x, 44, x, 47, WOOD_D)
# 다리
rect(bed, 4, 50, 11, 55, WOOD_DD); rect(bed, 86, 50, 91, 55, WOOD_DD)
# 베개 (도톰하게, 그림자)
rect(bed, 14, 27, 31, 34, hx('#FFFFFF')); rect(bed, 13, 29, 32, 33, hx('#FFFFFF')); rect(bed, 15, 26, 30, 26, hx('#FFFFFF'))
rect(bed, 14, 32, 31, 34, hx('#DCD4EC')); rect(bed, 13, 33, 32, 33, hx('#DCD4EC')); rect(bed, 22, 28, 23, 31, hx('#E8E2F4'))
rect(bed, 15, 27, 18, 27, hx('#F6F2FF'))
outline(bed)
# ---- 앞쪽: 이불 (접힌 흰 끝단 + 보라 체크·별 무늬, 옆으로 늘어짐) ----
q = img()
QA, QB, QC, QD = hx('#7A5AC8'), hx('#6A4AB0'), hx('#9A7AE8'), hx('#5A3A98')
def quilt_px(x, y):
    c = QA if ((x // 6) + (y // 5)) % 2 == 0 else QB
    if (x % 6 == 0) or (y % 5 == 0): c = QD
    return c
for y in range(24, 48):
    # 위쪽은 몸을 따라 살짝 볼록, 아래는 침대 옆으로 늘어져요
    x0 = 30 if y < 26 else 28
    x1 = 84 if y < 42 else 83
    for x in range(x0, x1 + 1):
        if y == 24 and not (34 <= x <= 76): continue
        if y == 25 and not (31 <= x <= 80): continue
        q.putpixel((x, y), quilt_px(x, y))
# 볼록한 위쪽 밝은 면, 아래 그림자
for x in range(31, 81): q.putpixel((x, 26), QC) if q.getpixel((x, 26))[3] else None
for x in range(28, 84): q.putpixel((x, 41), QD)
for y in range(42, 48):
    for x in range(28, 84):
        if q.getpixel((x, y))[3]: q.putpixel((x, y), QB if (x // 6) % 2 else QD)
# 별 무늬
for (sx, sy) in ((40, 31), (58, 29), (72, 33), (50, 37), (66, 38)):
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): q.putpixel((sx + dx, sy + dy), hx('#FFE070'))
    q.putpixel((sx, sy), hx('#FFF6C0'))
# 접힌 흰 끝단 (머리 쪽 왼편 세로 띠)
for y in range(25, 46):
    for x in (28, 29, 30, 31):
        if y >= 26 or x >= 31: q.putpixel((x, y), hx('#F2EAD8') if x < 31 else hx('#D8CCE0'))
for y in range(25, 46, 4): q.putpixel((29, y), hx('#E0D4C8'))
# 아래 끝 술 장식
for x in range(30, 84, 3): q.putpixel((x, 48), hx('#FFE070'))
outline(q)
art = os.path.join(ROOT, 'public', 'art')
bed.save(os.path.join(art, 'rest_bed.png')); q.save(os.path.join(art, 'rest_quilt.png'))
print('ok', W, H)
