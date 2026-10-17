# 귀여운 2등신 캐릭터 조합 부품: out/avatar_parts.png + out/avatar_parts.json
# 한 칸 22×36, 한 줄 = 한 부품의 6프레임 (앞: 서기·걷기A·걷기B, 뒤: 서기·걷기A·걷기B)
# 색을 고를 수 있는 곳은 회색 열쇠색(K0 밝음 ~ K3 어두움)으로 그리고, 게임에서 고른 색으로 바꿔 칠해요.
# 회색이 아닌 색(눈 흰자, 볼터치, 리본 등)은 그대로 남아요. 바깥 테두리는 게임에서 합친 뒤에 둘러요.
import json
from PIL import Image, ImageDraw
FW, FH = 22, 36
K = [(240, 240, 240, 255), (200, 200, 200, 255), (150, 150, 150, 255), (100, 100, 100, 255)]
def hexc(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
DARK, WHITE, BLUSH, MOUTH, PINK = hexc('#2A1830'), hexc('#FFFFFC'), hexc('#FF9AB0'), hexc('#8A3048'), hexc('#F4A0B8')

class F:   # 프레임 정보
    def __init__(self, i):
        self.i, self.back, self.step = i, i >= 3, i % 3
        self.b = -1 if self.step == 1 else 0                       # 걸을 때 한 번씩 콩콩
        self.liftL, self.liftR = self.step == 1, self.step == 2    # 드는 다리
        self.footL, self.footR = 34 - self.liftL, 34 - self.liftR
        self.armL, self.armR = (1 if self.step == 2 else 0), (1 if self.step == 1 else 0)   # 팔 흔들기 (아래로 1칸)
def new(): return Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
def P(img, x, y, c):
    if 0 <= x < FW and 0 <= y < FH: img.putpixel((int(x), int(y)), c)
def R(img, x0, y0, x1, y1, c):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1): P(img, x, y, c)
def E(img, x0, y0, x1, y1, c): ImageDraw.Draw(img).ellipse([x0, y0, x1, y1], fill=c)
def G(img, pts, c): ImageDraw.Draw(img).polygon(pts, fill=c)
def mirror_x(x): return FW - 1 - x
def clear(img, x0, y0, x1, y1): R(img, x0, y0, x1, y1, (0, 0, 0, 0))

# ---------------- 몸 (피부색) ----------------
def body(f):
    u = new(); b = f.b
    # 다리
    R(u, 8, 29, 9, f.footL, K[1]); R(u, 12, 29, 13, f.footR, K[1]); R(u, 9, 29, 9, f.footL, K[2]); R(u, 13, 29, 13, f.footR, K[2])
    # 몸통·목
    R(u, 7, 22 + b, 14, 30, K[1]); R(u, 10, 20 + b, 11, 22 + b, K[2])
    # 팔 + 손
    R(u, 5, 23 + b, 6, 28 + b + f.armL, K[1]); R(u, 15, 23 + b, 16, 28 + b + f.armR, K[1])
    R(u, 5, 28 + b + f.armL, 6, 29 + b + f.armL, K[0] if not f.back else K[1]); R(u, 15, 28 + b + f.armR, 16, 29 + b + f.armR, K[0] if not f.back else K[1])
    # 머리 (큼직하게)
    E(u, 4, 7 + b, 17, 20 + b, K[1])
    R(u, 6, 19 + b, 15, 19 + b, K[2]); R(u, 4, 13 + b, 4, 15 + b, K[2]); R(u, 17, 13 + b, 17, 15 + b, K[2])
    if not f.back: E(u, 6, 9 + b, 10, 12 + b, K[0])
    R(u, 3, 13 + b, 3, 15 + b, K[2]); R(u, 18, 13 + b, 18, 15 + b, K[2])   # 귀
    return u, None

# ---------------- 눈 (눈 색) ----------------
EYES = ['동글', '반짝', '웃음', '졸린', '고양이', '별', '윙크', '송곳니']
def eyes(f, st):
    if f.back: return None, None
    o = new(); b = f.b
    def round_eye(x, hl2=False, cat=False):
        R(o, x, 13 + b, x + 1, 13 + b, DARK); R(o, x, 14 + b, x + 1, 14 + b, K[3]); R(o, x, 15 + b, x + 1, 15 + b, K[2]); R(o, x, 16 + b, x + 1, 16 + b, K[1])
        P(o, x, 14 + b, WHITE)
        if hl2: P(o, x + 1, 16 + b, WHITE)
        if cat: R(o, x + 1, 14 + b, x + 1, 16 + b, DARK); P(o, x, 14 + b, WHITE)
    def caret(x): P(o, x - 1, 15 + b, DARK); P(o, x, 14 + b, DARK); P(o, x + 1, 14 + b, DARK); P(o, x + 2, 15 + b, DARK)
    if st == 0 or st == 7: round_eye(7); round_eye(13)
    elif st == 1:
        for x in (7, 13): round_eye(x, True); P(o, x - 1, 13 + b, DARK); P(o, x + 2, 13 + b, DARK)
    elif st == 2: caret(7); caret(13)
    elif st == 3:
        for x in (7, 13): R(o, x - 1, 15 + b, x + 2, 15 + b, DARK); R(o, x, 16 + b, x + 1, 16 + b, K[2])
    elif st == 4: round_eye(7, cat=True); round_eye(13, cat=True)
    elif st == 5:
        for x in (7, 14): P(o, x, 14 + b, K[0]); R(o, x - 1, 15 + b, x + 1, 15 + b, K[1]); P(o, x, 15 + b, K[0]); P(o, x, 16 + b, K[1]); P(o, x - 1, 13 + b, DARK); P(o, x + 1, 13 + b, DARK)
    elif st == 6: round_eye(7); caret(13)
    # 볼터치
    P(o, 5, 17 + b, BLUSH); P(o, 6, 17 + b, BLUSH); P(o, 15, 17 + b, BLUSH); P(o, 16, 17 + b, BLUSH)
    # 입
    if st == 4: P(o, 9, 18 + b, MOUTH); P(o, 10, 19 + b, MOUTH); P(o, 11, 19 + b, MOUTH); P(o, 12, 18 + b, MOUTH)
    elif st == 2: R(o, 10, 18 + b, 11, 18 + b, MOUTH); R(o, 10, 19 + b, 11, 19 + b, hexc('#E0607A'))
    elif st == 7: R(o, 10, 18 + b, 11, 18 + b, MOUTH); P(o, 11, 19 + b, WHITE)
    else: P(o, 10, 18 + b, MOUTH); P(o, 11, 18 + b, MOUTH)
    return None, o

# ---------------- 머리카락 (머리 색) ----------------
HAIRS = ['단발', '긴 생머리', '양갈래', '똥머리', '짧은 머리', '삐죽 머리', '포니테일', '곱슬 머리']
def cap(o, b, bang_y=11, side_y=17, sides=True):
    E(o, 3, 5 + b, 18, 16 + b, K[1])                     # 위쪽 동그란 덮개
    clear(o, 0, bang_y + 1 + b, FW - 1, FH - 1)
    for x in range(4, 18):                                # 앞머리 끝 들쭉날쭉
        if x % 3 != 1: P(o, x, bang_y + 1 + b, K[2])
        if x % 3 == 0 and 5 < x < 16: P(o, x, bang_y + 2 + b, K[2])
    if sides:
        R(o, 3, 9 + b, 5, side_y + b, K[1]); R(o, 16, 9 + b, 18, side_y + b, K[1])
        R(o, 3, side_y - 1 + b, 3, side_y + b, K[2]); R(o, 18, side_y - 1 + b, 18, side_y + b, K[2])
    R(o, 7, 6 + b, 10, 6 + b, K[0]); R(o, 6, 7 + b, 7, 7 + b, K[0])      # 윤기
def hair(f, st):
    u, o = new(), new(); b = f.b
    if f.back:
        length = {0: 19, 1: 29, 2: 17, 3: 18, 4: 17, 5: 17, 6: 17, 7: 21}[st]
        E(o, 3, 5 + b, 18, 19 + b, K[1]); R(o, 3, 12 + b, 18, length + b, K[1]); R(o, 3, length + b, 18, length + b, K[2])
        R(o, 7, 6 + b, 12, 6 + b, K[0])
        if st == 2: E(o, 0, 11 + b, 4, 27 + b, K[1]); E(o, 17, 11 + b, 21, 27 + b, K[1]); R(o, 3, 12 + b, 4, 13 + b, hexc('#FF6A9A')); R(o, 17, 12 + b, 18, 13 + b, hexc('#FF6A9A'))
        if st == 3: E(o, 7, 1 + b, 14, 8 + b, K[1]); R(o, 9, 2 + b, 11, 2 + b, K[0])
        if st == 5:
            for x0 in (4, 8, 12, 15): G(o, [(x0, 8 + b), (x0 + 2, 2 + b), (x0 + 4, 8 + b)], K[1])
        if st == 6: R(o, 9, 14 + b, 12, 28 + b, K[1]); R(o, 10, 14 + b, 11, 14 + b, hexc('#FF6A9A')); R(o, 9, 27 + b, 12, 28 + b, K[2])
        if st == 7:
            for cx, cy in ((3, 8), (18, 8), (2, 14), (19, 14), (3, 20), (18, 20), (10, 21)): E(o, cx - 2, cy - 2 + b, cx + 2, cy + 2 + b, K[1])
        return None, o
    if st == 0: cap(o, b); E(u, 3, 8 + b, 18, 20 + b, K[2])
    elif st == 1: cap(o, b, side_y=21); R(u, 2, 10 + b, 19, 29 + b, K[2]); R(u, 2, 28 + b, 19, 29 + b, K[3])
    elif st == 2:
        cap(o, b, side_y=15); E(u, 0, 11 + b, 4, 27 + b, K[1]); E(u, 17, 11 + b, 21, 27 + b, K[1]); R(u, 1, 24 + b, 3, 26 + b, K[2]); R(u, 18, 24 + b, 20, 26 + b, K[2])
        R(o, 3, 11 + b, 4, 12 + b, hexc('#FF6A9A')); R(o, 17, 11 + b, 18, 12 + b, hexc('#FF6A9A'))
    elif st == 3: cap(o, b, side_y=15); E(o, 7, 1 + b, 14, 8 + b, K[1]); R(o, 9, 2 + b, 11, 2 + b, K[0]); R(o, 7, 7 + b, 14, 7 + b, K[2])
    elif st == 4: cap(o, b, bang_y=10, side_y=13)
    elif st == 5:
        cap(o, b, bang_y=10, side_y=13)
        for x0 in (4, 8, 12, 15): G(o, [(x0, 8 + b), (x0 + 2, 2 + b), (x0 + 4, 8 + b)], K[1])
        R(o, 9, 3 + b, 9, 4 + b, K[0])
    elif st == 6: cap(o, b, side_y=15); G(u, [(16, 8 + b), (21, 12 + b), (20, 25 + b), (17, 20 + b)], K[1]); R(o, 16, 9 + b, 17, 10 + b, hexc('#FF6A9A'))
    elif st == 7:
        for cx, cy in ((3, 8), (18, 8), (2, 14), (19, 14), (3, 20), (18, 20)): E(u, cx - 3, cy - 3 + b, cx + 3, cy + 3 + b, K[2])
        cap(o, b, side_y=18)
        for cx in (5, 9, 13, 16): E(o, cx - 2, 3 + b, cx + 2, 7 + b, K[1])
        R(o, 7, 5 + b, 9, 5 + b, K[0])
    return u, o

# ---------------- 머리 장식 ----------------
HATS = [('없음', None), ('마녀 모자', 'hat'), ('늑대 귀', 'hair'), ('고양이 귀', 'hair'), ('악마 뿔', None), ('박쥐 리본', 'hat'), ('호박 모자', None), ('유령 천', None)]
def hat(f, st):
    o = new(); b = f.b
    if st == 0: return None, None
    if st == 1:
        E(o, 0, 5 + b, 21, 10 + b, K[2]); E(o, 1, 5 + b, 20, 8 + b, K[1])
        G(o, [(6, 7 + b), (15, 7 + b), (13, 2 + b), (17, -1 + b), (10, 1 + b)], K[1]); G(o, [(12, 7 + b), (15, 7 + b), (13, 2 + b)], K[2])
        R(o, 6, 6 + b, 15, 6 + b, hexc('#E07A1E')); P(o, 10, 6 + b, hexc('#FFD86A'))
    elif st in (2, 3):
        tall = 1 if st == 2 else 3
        for x0, x1 in ((3, 8), (13, 18)):
            G(o, [(x0, 9 + b), (x1, 9 + b), ((x0 + x1) / 2 + (-1 if x0 < 10 else 1), tall + b)], K[1])
            if not f.back: G(o, [(x0 + 1.5, 8 + b), (x1 - 1.5, 8 + b), ((x0 + x1) / 2 + (-1 if x0 < 10 else 1), tall + 3 + b)], PINK)
    elif st == 4:
        for x0, s in ((5, -1), (16, 1)):
            R(o, x0, 4 + b, x0, 7 + b, hexc('#8A1E2E')); P(o, x0 + s, 3 + b, hexc('#8A1E2E')); P(o, x0 + s, 2 + b, hexc('#C83A4A')); P(o, x0, 5 + b, hexc('#C83A4A'))
    elif st == 5:
        G(o, [(12, 6 + b), (20, 2 + b), (19, 6 + b), (20, 10 + b)], K[1]); G(o, [(12, 6 + b), (5, 2 + b) if f.back else (13, 2 + b), (12, 10 + b)], K[1])
        if not f.back: G(o, [(14, 6 + b), (19, 3 + b), (19, 9 + b)], K[2])
        R(o, 12, 5 + b, 13, 7 + b, K[3])
    elif st == 6:
        for dx, w in ((-3, 3), (3, 3), (0, 4)): E(o, 11 + dx - w, 2 + b, 11 + dx + w, 8 + b, hexc('#E07A1E'))
        R(o, 9, 3 + b, 9, 7 + b, hexc('#C8601A')); R(o, 13, 3 + b, 13, 7 + b, hexc('#C8601A')); R(o, 11, 0 + b, 11, 2 + b, hexc('#4A7A2E')); P(o, 12, 0 + b, hexc('#6AAE4A'))
    elif st == 7:
        E(o, 2, 3 + b, 19, 22 + b, hexc('#F2F0FA')); R(o, 2, 14 + b, 19, 24 + b, hexc('#F2F0FA'))
        for x in range(2, 20, 3): R(o, x, 24 + b, x + 1, 25 + b, hexc('#F2F0FA'))
        R(o, 2, 18 + b, 3, 24 + b, hexc('#C8C4DC')); R(o, 18, 18 + b, 19, 24 + b, hexc('#C8C4DC'))
        if not f.back:
            E(o, 5, 10 + b, 16, 21 + b, (0, 0, 0, 0))
    return None, o

# ---------------- 윗옷 (옷 색) ----------------
TOPS = [('교복', None), ('마녀 로브', ['bottom']), ('후드티', None), ('원피스', ['bottom']), ('줄무늬 니트', None), ('뱀파이어 조끼', None)]
def sleeves(o, f, short=False, c=K[1]):
    b = f.b; yl = 24 + b if short else 27 + b
    R(o, 5, 23 + b, 6, yl + (0 if short else f.armL), c); R(o, 15, 23 + b, 16, yl + (0 if short else f.armR), c)
    R(o, 5, yl + (0 if short else f.armL), 6, yl + (0 if short else f.armL), K[2]); R(o, 15, yl + (0 if short else f.armR), 16, yl + (0 if short else f.armR), K[2])
def top(f, st):
    o = new(); b = f.b
    R(o, 7, 22 + b, 14, 29, K[1]); R(o, 7, 29, 14, 29, K[2]); R(o, 14, 23 + b, 14, 28, K[2])
    if st == 0:
        sleeves(o, f)
        if not f.back:
            G(o, [(9, 22 + b), (12, 22 + b), (10.5, 26 + b)], WHITE); R(o, 9, 23 + b, 12, 23 + b, hexc('#D8344A')); P(o, 10, 24 + b, hexc('#D8344A')); P(o, 11, 24 + b, hexc('#D8344A'))
            P(o, 10, 27 + b, K[3]); P(o, 10, 29, K[3])
        else: R(o, 8, 22 + b, 13, 23 + b, WHITE)
    elif st == 1:
        G(o, [(7, 26 + b), (14, 26 + b), (16, 33), (5, 33)], K[1]); R(o, 5, 33, 16, 33, K[2]); R(o, 14, 27, 15, 32, K[2])
        G(o, [(6, 23 + b), (4, 29 + b + f.armL), (7, 29 + b + f.armL)], K[1]); G(o, [(15, 23 + b), (17, 29 + b + f.armR), (14, 29 + b + f.armR)], K[2])
        R(o, 5, 23 + b, 6, 27 + b, K[1]); R(o, 15, 23 + b, 16, 27 + b, K[2])
        if not f.back: R(o, 10, 22 + b, 11, 33, K[2]); P(o, 10, 23 + b, hexc('#FFD86A')); P(o, 11, 23 + b, hexc('#FFD86A'))
    elif st == 2:
        sleeves(o, f)
        if not f.back: R(o, 7, 21 + b, 14, 21 + b, K[2]); R(o, 8, 26 + b, 13, 26 + b, K[2]); P(o, 9, 23 + b, WHITE); P(o, 12, 23 + b, WHITE); P(o, 9, 24 + b, WHITE); P(o, 12, 24 + b, WHITE)
        else: E(o, 6, 18 + b, 15, 24 + b, K[2]); E(o, 7, 19 + b, 14, 23 + b, K[1])
    elif st == 3:
        sleeves(o, f, short=True)
        G(o, [(7, 26 + b), (14, 26 + b), (16, 31), (5, 31)], K[1]); R(o, 5, 31, 16, 31, WHITE); R(o, 14, 27, 15, 30, K[2])
        if not f.back: R(o, 9, 22 + b, 12, 22 + b, WHITE); P(o, 10, 25 + b, hexc('#FFD86A')); P(o, 11, 25 + b, hexc('#FFD86A'))
        R(o, 7, 26 + b, 14, 26 + b, K[2])
    elif st == 4:
        sleeves(o, f)
        for y in range(22, 30):
            if (y + b) % 2 == 0: R(o, 7, y + b if y + b <= 29 else 29, 13, y + b if y + b <= 29 else 29, K[0])
        for y in range(23, 28):
            if y % 2 == 0: P(o, 5, y + b, K[0]); P(o, 16, y + b, K[0])
    elif st == 5:
        R(o, 5, 23 + b, 6, 27 + b + f.armL, WHITE); R(o, 15, 23 + b, 16, 27 + b + f.armR, WHITE)
        if not f.back:
            R(o, 9, 22 + b, 12, 29, WHITE); R(o, 9, 22 + b, 12, 23 + b, hexc('#F2EEE4')); P(o, 10, 23 + b, hexc('#B02A3A')); P(o, 11, 23 + b, hexc('#B02A3A')); P(o, 10, 24 + b, hexc('#B02A3A'))
            P(o, 8, 25 + b, hexc('#C49446')); P(o, 8, 27 + b, hexc('#C49446'))
    return None, o

# ---------------- 아래옷 ----------------
BOTTOMS = ['치마', '반바지', '긴 바지', '호박 바지']
def bottom(f, st):
    o = new()
    if st == 0:
        G(o, [(7, 28), (14, 28), (16, 31), (5, 31)], K[1]); R(o, 5, 31, 16, 31, K[2])
        for x in (7, 10, 13): R(o, x, 30, x, 31, K[2])
    elif st == 1: R(o, 7, 28, 14, 31, K[1]); clear(o, 10, 31, 11, 31); R(o, 7, 31, 9, 31, K[2]); R(o, 12, 31, 14, 31, K[2])
    elif st == 2: R(o, 7, 28, 14, 29, K[1]); R(o, 7, 30, 10, f.footL - 1, K[1]); R(o, 11, 30, 14, f.footR - 1, K[1]); R(o, 10, 30, 10, f.footL - 1, K[2]); R(o, 14, 30, 14, f.footR - 1, K[2])
    elif st == 3:
        E(o, 5, 27, 16, 33, K[1]); R(o, 6, 31, 15, 31, K[2]); clear(o, 10, 32, 11, 33); R(o, 7, 32, 9, 32, K[3]); R(o, 12, 32, 14, 32, K[3])
        for x in (8, 13): R(o, x, 28, x, 30, K[2])
    return None, o

# ---------------- 신발 ----------------
SHOES = ['단화', '부츠', '마녀 구두', '운동화']
def shoes(f, st):
    o = new()
    for (x0, x1, fy, out) in ((7, 10, f.footL, -1), (11, 14, f.footR, 1)):
        h = 3 if st == 1 else 1
        R(o, x0, fy - h, x1, fy, K[1]); R(o, x0, fy, x1, fy, K[2])
        if st == 0: R(o, x0, fy - 1, x1, fy - 1, K[3])
        if st == 1: R(o, x0, fy - 3, x1, fy - 3, K[0])
        if st == 2:
            tx = x0 - 1 if out < 0 else x1 + 1
            P(o, tx, fy, K[1]); P(o, tx + out, fy - 1, K[1]); P(o, (x0 + x1) // 2, fy - 1, hexc('#FFD86A'))
        if st == 3: R(o, x0, fy, x1, fy, WHITE); P(o, x0 + 1, fy - 1, WHITE)
    return None, o

# ---------------- 등·손 소품 ----------------
ACCS = [('없음', None), ('망토', 'acc'), ('늑대 꼬리', 'acc'), ('고양이 꼬리', 'acc'), ('박쥐 날개', 'acc'), ('호박 바구니', None), ('빗자루', None)]
def acc(f, st):
    u, o = new(), new(); b = f.b
    if st == 0: return None, None
    if st == 1:
        if f.back: G(o, [(6, 21 + b), (15, 21 + b), (17, 32), (4, 32)], K[1]); R(o, 4, 32, 17, 32, K[2]); R(o, 10, 22 + b, 11, 31, K[2]); R(o, 7, 21 + b, 14, 21 + b, hexc('#D8344A'))
        else: G(u, [(6, 21 + b), (15, 21 + b), (17, 32), (4, 32)], K[2]); R(o, 7, 22 + b, 7, 23 + b, K[1]); R(o, 14, 22 + b, 14, 23 + b, K[1]); P(o, 8, 22 + b, hexc('#D8344A')); P(o, 13, 22 + b, hexc('#D8344A'))
    elif st == 2:
        if f.back: E(o, 7, 25, 14, 34, K[1]); E(o, 9, 31, 12, 34, K[0])
        else: E(u, 14, 22, 21, 31, K[1]); E(u, 17, 22, 21, 26, K[0])
    elif st == 3:
        tgt = o if f.back else u
        pts = [(11, 29), (12, 31), (14, 31), (16, 29), (17, 26), (16, 23), (18, 21)] if f.back else [(15, 28), (17, 28), (19, 26), (19, 22), (20, 20)]
        for (x, y) in pts: R(tgt, x, y, x + 1, y + 1, K[1])
    elif st == 4:
        tgt = o if f.back else u
        flap = -1 if f.step == 1 else 0
        for s in (-1, 1):
            cx = 11 + s * 6
            G(tgt, [(11 + s * 3, 22 + b), (11 + s * 10, 16 + b + flap), (11 + s * 10, 26 + b), (11 + s * 8, 24 + b), (11 + s * 6, 27 + b), (11 + s * 4, 25 + b)], K[1])
            R(tgt, 11 + s * 9, 17 + b + flap, 11 + s * 9, 25 + b, K[2])
    elif st == 5:
        tgt = u if f.back else o
        x, y = 15, 28 + b + f.armR
        E(tgt, x, y, x + 6, y + 5, hexc('#E07A1E')); R(tgt, x + 1, y + 1, x + 5, y + 1, hexc('#C8601A')); P(tgt, x + 2, y + 3, hexc('#2A1830')); P(tgt, x + 4, y + 3, hexc('#2A1830'))
        G(tgt, [(x, y + 1), (x + 3, y - 4), (x + 6, y + 1)], (0, 0, 0, 0)); ImageDraw.Draw(tgt).arc([x, y - 4, x + 6, y + 3], 180, 360, fill=hexc('#6A4A2E'))
    elif st == 6:
        tgt = o if f.back else u
        ImageDraw.Draw(tgt).line([(2, 34), (19, 12 + b)], fill=hexc('#8A5A3A'), width=1); ImageDraw.Draw(tgt).line([(3, 34), (20, 12 + b)], fill=hexc('#6A4228'), width=1)
        G(tgt, [(1, 31), (5, 33), (3, 36), (-1, 35)], hexc('#C8A84A'))
    return u, o

# ---------------- 시트로 모으기 ----------------
rows, parts = [], {}
def add(cat, name, fn, slot, hide=None):
    us, os_ = [], []
    for i in range(6):
        u, o = fn(F(i)); us.append(u); os_.append(o)
    entry = dict(n=name, slot=slot)
    for key, imgs in (('u', us), ('o', os_)):
        if any(im is not None and im.getbbox() for im in imgs):
            row = Image.new('RGBA', (FW * 6, FH), (0, 0, 0, 0))
            for i, im in enumerate(imgs):
                if im is not None: row.paste(im, (i * FW, 0))
            entry[key] = len(rows); rows.append(row)
    if hide: entry['hide'] = hide
    parts.setdefault(cat, []).append(entry)
add('body', '몸', body, 'skin')
for i, n in enumerate(EYES): add('eyes', n, lambda f, i=i: eyes(f, i), 'eye')
for i, n in enumerate(HAIRS): add('hair', n, lambda f, i=i: hair(f, i), 'hair')
for i, (n, s) in enumerate(HATS): add('hat', n, lambda f, i=i: hat(f, i), s)
for i, (n, h) in enumerate(TOPS): add('top', n, lambda f, i=i: top(f, i), 'top', h)
for i, n in enumerate(BOTTOMS): add('bottom', n, lambda f, i=i: bottom(f, i), 'bottom')
for i, n in enumerate(SHOES): add('shoes', n, lambda f, i=i: shoes(f, i), 'shoes')
for i, (n, s) in enumerate(ACCS): add('acc', n, lambda f, i=i: acc(f, i), s)
sheet = Image.new('RGBA', (FW * 6, FH * len(rows)), (0, 0, 0, 0))
for r, im in enumerate(rows): sheet.paste(im, (0, r * FH))
sheet.save('out/avatar_parts.png')
PAL = {
  'skin': [['#FFF0E6', '#FFE0CC', '#F2C4A8', '#D8A088'], ['#FFE8D8', '#F6CCAE', '#E0A888', '#C08068'], ['#F2D0B0', '#DEAE88', '#C08A66', '#9A6A4C'],
           ['#D8A47A', '#B8845A', '#946440', '#6E482E'], ['#E8F0F8', '#C8D8EC', '#A4B8D8', '#7A90B8'], ['#D8F0C8', '#B4DCA0', '#8AC078', '#62985A'], ['#F0E0FF', '#DCC4F4', '#BCA0E0', '#9478C0']],
  'hair': [['#5A4A6A', '#3A2A4A', '#2A1E36', '#1A1224'], ['#8A5A3A', '#6A4028', '#4E2E1C', '#341E12'], ['#F2D888', '#E0B860', '#C09040', '#94682A'], ['#FF9A6A', '#E8703E', '#C0522A', '#8A361C'],
           ['#FFC8DC', '#F49AC0', '#D8709E', '#A84A78'], ['#D8C8FF', '#B49AF2', '#8E70D0', '#6648A4'], ['#B8F0E0', '#7ED8C0', '#4EB09A', '#2E8070'], ['#F4F4FA', '#D8D8E8', '#B0B0C8', '#8888A4'],
           ['#C8E8FF', '#8EC4F2', '#5E98D0', '#3C6AA0'], ['#FF8A8A', '#E04A5A', '#B02A3E', '#7A1A2A'], ['#4A4A5A', '#2E2E3A', '#1E1E28', '#121218'], ['#E8FF9A', '#C4E85A', '#94C03A', '#6A8E26']],
  'eye':  [['#A890FF', '#7A5AE0', '#5A3AB0', '#3A2470'], ['#9AD8FF', '#4AA8F0', '#2A78C0', '#1A4C80'], ['#9AF0B0', '#4AC878', '#2A9A54', '#1A6436'], ['#FFC88A', '#E8944A', '#B8682A', '#7A421A'],
           ['#FF9AB8', '#F05A8A', '#C03A64', '#80223E'], ['#FF8A7A', '#E83A3A', '#B01E2A', '#70121C'], ['#FFE88A', '#F0C040', '#C09020', '#806010'], ['#8A7A9A', '#5A4A6A', '#3A2E48', '#241A30']],
  'cloth': [['#7A6AB0', '#4E3E8A', '#3A2A6A', '#24184A'], ['#4A4A5E', '#2E2E40', '#20202E', '#14141E'], ['#FF9A5A', '#E8702A', '#C0521A', '#8A3610'], ['#9AE0A0', '#5AB86A', '#3A8A4C', '#24603A'],
            ['#FF9ABA', '#E8608A', '#C0406A', '#8A2848'], ['#E85A5A', '#B8303A', '#8A1E2A', '#5E141E'], ['#9AC8FF', '#5A94E0', '#3A6AB8', '#244A80'], ['#FFE89A', '#F0C850', '#C89A30', '#8A6A1A'],
            ['#F4F0FA', '#DCD8EA', '#B8B2CC', '#8E88A8'], ['#C8A07A', '#A07A54', '#7A5A3A', '#543C24'], ['#C8A0F0', '#A070E0', '#7A4ABA', '#56308A'], ['#8AE8E0', '#4AC4BA', '#2E968E', '#1E6A64'],
            ['#5A3A2A', '#422A1E', '#2E1C14', '#1E120C'], ['#FFF0C8', '#F2D8A0', '#D4B478', '#A88A54']],
}
json.dump(dict(fw=FW, fh=FH, parts=parts, pal=PAL, src='art/iso/avatar_parts.png'), open('out/avatar_parts.json', 'w'), ensure_ascii=False)
print('rows', len(rows), {k: len(v) for k, v in parts.items()})
