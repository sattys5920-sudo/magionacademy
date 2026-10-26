# 이벤트 2 「유령 선장의 보물 지도」: 50조각 직소 퍼즐 지도 그림과 시안 화면 → out/ev2_map.png, out/ev2_puzzle_board.png
import math, os, random
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(5)
COLS, ROWS, PW, PH = 10, 5, 20, 24          # 조각 10×5 = 50, 조각 하나는 20×24 칸
W, H = COLS * PW, ROWS * PH                  # 지도 200×120 칸
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def make_map():
    im = Image.new('RGBA', (W, H), c('#E8D3A0')); px = im.load(); d = ImageDraw.Draw(im)
    for y in range(H):                        # 양피지 얼룩
        for x in range(W):
            n = random.random()
            if n < .08: px[x, y] = c('#DCC490')
            elif n < .12: px[x, y] = c('#F0DEB0')
    cx, cy = 104, 62                          # 바다 파도와 섬
    for y in range(8, H - 8):
        for x in range(8, W - 8):
            dx, dy = (x - cx) / 62, (y - cy) / 36
            r = dx * dx + dy * dy + .12 * math.sin(x * .35) + .1 * math.sin(y * .5 + 1)
            if r > 1.7 and (x + y) % 9 == 0: px[x, y] = c('#B79B66')    # 바다 물결 점
            if r < .95: px[x, y] = c('#6FA34A')
            if .8 < r < .95: px[x, y] = c('#E6CF86')   # 해변
    for x in range(8, W - 8):                  # 산
        pass
    def tri(x, y, w, h, col, sh):
        d.polygon([(x, y), (x - w, y + h), (x + w, y + h)], fill=c(col)); d.polygon([(x, y), (x, y + h), (x + w, y + h)], fill=c(sh))
    tri(98, 38, 11, 16, '#8A8A92', '#66666E'); tri(112, 44, 8, 11, '#8A8A92', '#66666E')
    for tx, ty in ((78, 70), (84, 78), (126, 74), (132, 66), (118, 84), (90, 60)):   # 야자수
        d.rectangle([tx, ty, tx, ty + 5], fill=c('#6B4A2A'))
        for ax, ay in ((-3, -1), (3, -1), (-2, -3), (2, -3), (0, -4)): d.line([tx, ty, tx + ax, ty + ay], fill=c('#2E7A3A'))
    for x in range(6):                         # 점선 길
        pass
    pts = [(46, 100), (62, 92), (74, 88), (92, 78), (104, 72), (112, 66)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(math.hypot(x1 - x0, y1 - y0) / 3)
        for i in range(n + 1):
            t = i / max(1, n)
            if i % 2 == 0: d.point((int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)), fill=c('#9A2A22'))
    X = (116, 62); d.line([X[0] - 4, X[1] - 4, X[0] + 4, X[1] + 4], fill=c('#C0281E'), width=2); d.line([X[0] - 4, X[1] + 4, X[0] + 4, X[1] - 4], fill=c('#C0281E'), width=2)
    # 유령선
    sx, sy = 38, 96
    d.polygon([(sx - 9, sy), (sx + 9, sy), (sx + 6, sy + 5), (sx - 6, sy + 5)], fill=c('#4A3A5A')); d.line([sx, sy, sx, sy - 14], fill=c('#2A2030'))
    d.polygon([(sx, sy - 13), (sx + 8, sy - 6), (sx, sy - 3)], fill=c('#D9D9F0')); d.polygon([(sx, sy - 11), (sx - 6, sy - 6), (sx, sy - 3)], fill=c('#BFBFE0'))
    # 나침반
    kx, ky = 176, 28
    d.ellipse([kx - 9, ky - 9, kx + 9, ky + 9], outline=c('#6B4A2A')); d.polygon([(kx, ky - 11), (kx - 2, ky), (kx + 2, ky)], fill=c('#C0281E')); d.polygon([(kx, ky + 11), (kx - 2, ky), (kx + 2, ky)], fill=c('#4A3A2A'))
    d.line([kx - 11, ky, kx + 11, ky], fill=c('#4A3A2A'))
    # 바다 괴물 꼬리
    mx, my = 160, 98
    for i in range(5): d.ellipse([mx + i * 5 - 3, my - int(4 * math.sin(i * 1.3)) - 3, mx + i * 5 + 3, my - int(4 * math.sin(i * 1.3)) + 3], fill=c('#3B6E8A'), outline=c('#244A60'))
    d.rectangle([2, 2, W - 3, H - 3], outline=c('#8A6A3A'))          # 가장자리
    d.rectangle([4, 4, W - 5, H - 5], outline=c('#B08E56'))
    return im
M = make_map(); M.save('out/ev2_map_native.png')
# 직소 조각: 가로/세로 이웃 모서리마다 볼록·오목을 정해요
hs = [[random.choice((-1, 1)) for _ in range(COLS)] for _ in range(ROWS - 1)]   # 가로선(위아래 이웃)
vs = [[random.choice((-1, 1)) for _ in range(COLS - 1)] for _ in range(ROWS)]   # 세로선(좌우 이웃)
S = 4                                                                               # 조각 마스크 해상도 배율
def piece_mask(r, cc):
    m = Image.new('L', ((PW + 12) * S, (PH + 12) * S), 0); d = ImageDraw.Draw(m); ox, oy = 6 * S, 6 * S
    d.rectangle([ox, oy, ox + PW * S - 1, oy + PH * S - 1], fill=255)
    def knob(cx, cy, sign, horiz):                     # sign>0 바깥으로 볼록
        rad = 3.4 * S; nk = 2.2 * S
        dx, dy = (0, sign) if horiz else (sign, 0)
        bx, by = cx + dx * (nk), cy + dy * (nk)
        fill = 255 if sign > 0 else 0
        d.rectangle([cx - 1.4 * S - (0 if horiz else 0), cy - 1.4 * S, cx + 1.4 * S, cy + 1.4 * S], fill=255 if sign > 0 else fill)
        d.ellipse([bx - rad, by - rad, bx + rad, by + rad], fill=fill)
    if r > 0: knob(ox + PW * S / 2, oy, -hs[r - 1][cc], True)               # 위
    if r < ROWS - 1: knob(ox + PW * S / 2, oy + PH * S, hs[r][cc], True)     # 아래
    if cc > 0: knob(ox, oy + PH * S / 2, -vs[r][cc - 1], False)              # 왼
    if cc < COLS - 1: knob(ox + PW * S, oy + PH * S / 2, vs[r][cc], False)   # 오른
    return m.resize((PW + 12, PH + 12), Image.LANCZOS).point(lambda v: 255 if v > 127 else 0)
def piece_img(r, cc):
    m = piece_mask(r, cc); canvas = Image.new('RGBA', (PW + 12, PH + 12), (0, 0, 0, 0))
    src = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); src.paste(M, (6 - cc * PW, 6 - r * PH))
    canvas.paste(src, (0, 0), m)
    a = canvas.load(); o = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); oa = o.load(); mm = m.load()
    for y in range(canvas.size[1]):
        for x in range(canvas.size[0]):
            if mm[x, y] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < canvas.size[0] and 0 <= ny < canvas.size[1] and mm[nx, ny]: oa[x, y] = c('#3A2A18'); break
    canvas.alpha_composite(o); return canvas
P = {(r, cc): piece_img(r, cc) for r in range(ROWS) for cc in range(COLS)}
# ---- 시안 화면 (폰 390×740, 도트 ×3) ----
Z = 3
BW = 390; frame = Image.new('RGBA', (BW, 740), c('#140E22')); fd = ImageDraw.Draw(frame)
F = ImageFont.truetype('/usr/share/fonts/opentype/unifont/unifont.otf', 16); FS = ImageFont.truetype('/usr/share/fonts/opentype/unifont/unifont.otf', 16)
fd.rectangle([0, 0, BW, 52], fill=c('#1B1230')); fd.text((12, 16), '유령 선장의 보물 지도', fill=c('#FFFFFF'), font=F); fd.text((226, 16), '맞춘 조각 31 / 50', fill=c('#FFC23A'), font=FS)
bx, by = 15, 70; bw, bh = W * Z // 2 * 1, H * Z // 2   # 보드 (도트 1.5배 → 300×180)
BZ = 1.9; bw, bh = int(W * BZ), int(H * BZ); bx = (BW - bw) // 2
fd.rectangle([bx - 4, by - 4, bx + bw + 3, by + bh + 3], fill=c('#3A2A18'))
board = Image.new('RGBA', (W, H), c('#2A2036'))
bd = ImageDraw.Draw(board)
for r in range(ROWS):
    for cc in range(COLS): bd.rectangle([cc * PW, r * PH, cc * PW + PW - 1, r * PH + PH - 1], outline=c('#3A2E4A'))
placed = set(random.sample([(r, cc) for r in range(ROWS) for cc in range(COLS)], 31))
# 가운데가 더 많이 채워지게 (섬 중심)
for (r, cc) in sorted(placed): board.alpha_composite(P[(r, cc)], (cc * PW - 6, r * PH - 6))
board = board.resize((bw, bh), Image.NEAREST); frame.alpha_composite(board, (bx, by))
# 내가 가진 조각
ty = by + bh + 24
fd.text((15, ty - 6), '내 조각 (눌러서 보드에 놓아요)', fill=c('#D9CFF0'), font=FS)
mine = random.sample([k for k in P if k not in placed], 6)
for i, k in enumerate(mine):
    im = P[k].resize(((PW + 12) * 3, (PH + 12) * 3), Image.NEAREST); x = 4 + (i % 4) * 96; y = ty + 18 + (i // 4) * 112
    fd.rounded_rectangle([x - 2, y - 2, x + im.size[0] + 1, y + im.size[1] + 1], radius=8, fill=c('#2D2147'), outline=c('#FF9A2E') if i == 1 else c('#4A3A6A'), width=2 if i == 1 else 1)
    frame.alpha_composite(im, (x, y))
fd.text((15, 700), '낚시·채집·탐사에서 조각이 나와요', fill=c('#9A90B8'), font=FS)
frame.convert('RGB').save('out/ev2_puzzle_board.png')
M.resize((W * 3, H * 3), Image.NEAREST).convert('RGB').save('out/ev2_map.png')
# 조각 모양 확대
sheet = Image.new('RGBA', (COLS * (PW + 12) * 2, 2 * (PH + 12) * 2), c('#2A2036'))
for r in range(2):
    for cc in range(COLS): sheet.alpha_composite(P[(r + 1, cc)].resize(((PW + 12) * 2, (PH + 12) * 2), Image.NEAREST), (cc * (PW + 12) * 2, r * (PH + 12) * 2))
sheet.convert('RGB').save('out/ev2_pieces.png')
print('ok', len(P))
# ---- 게임용 그림: 조각 모음(10×5칸, 칸 32×36)과 완성 지도 ----
full = Image.new('RGBA', (COLS * (PW + 12), ROWS * (PH + 12)), (0, 0, 0, 0))
for (r, cc), im in P.items(): full.alpha_composite(im, (cc * (PW + 12), r * (PH + 12)))
full.save('../../public/art/ev2_pieces.png'); M.save('../../public/art/ev2_map.png')
