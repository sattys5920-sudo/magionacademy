# 이벤트 2 연출 그림: 밤 호수와 유령선, 해골 선장(해적 모자), 보물 상자 → public/art/ev2_lake.png · ev2_captain.png · ev2_chest.png
import math, os, random
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(9)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
# ---- 밤 호수와 유령선 (200×120) ----
W, H = 200, 120
im = Image.new('RGBA', (W, H)); px = im.load(); d = ImageDraw.Draw(im)
for y in range(H):
    t = y / H
    for x in range(W):
        px[x, y] = c('#0A0C24') if y < 66 else c('#0E1030')
for y in range(0, 66):                               # 하늘 그라데이션 띠
    k = y / 66; col = tuple(int(a + (b - a) * k) for a, b in zip((10, 12, 36), (34, 28, 70))); d.line([0, y, W, y], fill=col + (255,))
for _ in range(60): d.point((random.randrange(W), random.randrange(52)), fill=c('#CFCFF0') if random.random() < .5 else c('#8E8EC0'))
d.ellipse([150, 12, 176, 38], fill=c('#EDEBC8')); d.ellipse([156, 16, 166, 24], fill=c('#D4D2AE')); d.ellipse([166, 26, 172, 32], fill=c('#D4D2AE'))   # 달
for y in range(66, H):                               # 호수
    k = (y - 66) / (H - 66); col = tuple(int(a + (b - a) * k) for a, b in zip((14, 20, 54), (8, 10, 30))); d.line([0, y, W, y], fill=col + (255,))
for _ in range(120):                                 # 달빛 물결
    y = random.randrange(68, H); x = int(163 + random.gauss(0, 6 + (y - 66) * .15)); d.line([x, y, x + random.randint(2, 5), y], fill=c('#8F94C8'))
d.rectangle([0, 64, W, 66], fill=c('#1B1E48'))
# 유령선
sx, sy = 70, 78
hull = [(sx - 34, sy - 8), (sx + 36, sy - 8), (sx + 28, sy + 6), (sx - 24, sy + 6)]
d.polygon(hull, fill=c('#2B2240')); d.line([sx - 34, sy - 8, sx + 36, sy - 8], fill=c('#4A3D66'))
for i in range(-26, 30, 8): d.ellipse([sx + i - 1, sy - 3, sx + i + 1, sy - 1], fill=c('#8FE8D8'))        # 창문 빛
d.rectangle([sx - 36, sy - 12, sx - 28, sy - 8], fill=c('#2B2240'))                                       # 선미
for mx, mh, sw in ((sx - 14, 44, 13), (sx + 8, 52, 15), (sx + 26, 40, 11)):                              # 돛대와 찢어진 돛
    d.line([mx, sy - 8, mx, sy - 8 - mh], fill=c('#1A1426'), width=2)
    for r in range(3):
        top = sy - 8 - mh + 4 + r * 13; d.polygon([(mx - sw, top), (mx + sw, top), (mx + sw - 2, top + 9), (mx + sw - 5, top + 11), (mx + 1, top + 8), (mx - sw + 3, top + 12), (mx - sw, top + 8)], fill=c('#A9B4D8', 200))
d.polygon([(sx + 8, sy - 62), (sx + 20, sy - 58), (sx + 8, sy - 54)], fill=c('#1A1426')); d.ellipse([sx + 11, sy - 60, sx + 15, sy - 56], fill=c('#EDEBC8'))   # 해적 깃발
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.ellipse([sx - 50, sy - 40, sx + 50, sy + 20], fill=c('#6FD8C8', 34)); im.alpha_composite(glow)
for dy in range(8, 30, 3): d.line([sx - 30 + dy % 5, sy + 6 + dy - 4, sx + 30 - dy % 4, sy + 6 + dy - 4], fill=c('#1B1E48'))    # 배 그림자 물결
for _ in range(6):                                   # 안개
    fx, fy = random.randrange(W), random.randrange(70, 108); g2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g2).ellipse([fx - 30, fy - 4, fx + 30, fy + 4], fill=c('#B8C4E8', 26)); im.alpha_composite(g2)
im.save('../../public/art/ev2_lake.png')
# ---- 해골 선장 (64×64) ----
cap = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(cap)
BONE, BONE2, DK, OUT = c('#EEE8D2'), c('#C4BCA2'), c('#2A2438'), c('#120A18')
d.ellipse([22, 12, 42, 30], fill=BONE, outline=OUT); d.rectangle([26, 27, 38, 33], fill=BONE, outline=OUT)                 # 두개골과 턱
for x in (28, 31, 34, 37): d.line([x, 30, x, 33], fill=OUT)
d.ellipse([25, 18, 31, 24], fill=OUT); d.ellipse([33, 18, 39, 24], fill=OUT)                                               # 눈구멍
d.rectangle([27, 20, 28, 21], fill=c('#6FF0D8')); d.rectangle([35, 20, 36, 21], fill=c('#6FF0D8'))                          # 눈불
d.line([24, 17, 40, 23], fill=OUT); d.line([24, 17, 40, 23], fill=OUT)                                                    # 안대 끈
d.polygon([(32, 26), (30, 29), (34, 29)], fill=OUT)                                                                        # 코
# 해적 모자(삼각모)
d.polygon([(14, 15), (50, 15), (44, 8), (32, 2), (20, 8)], fill=c('#241A34'), outline=OUT); d.rectangle([14, 13, 50, 16], fill=c('#3A2A52'), outline=OUT)
d.line([16, 14, 48, 14], fill=c('#E0B040')); d.ellipse([29, 5, 35, 11], fill=BONE, outline=OUT); d.point((31, 8), fill=OUT); d.point((33, 8), fill=OUT)   # 모자 해골 표시
# 몸: 갈비뼈 + 낡은 외투
d.polygon([(20, 34), (44, 34), (48, 56), (16, 56)], fill=c('#6A1E2E'), outline=OUT); d.polygon([(26, 34), (38, 34), (36, 56), (28, 56)], fill=DK)
for y in (37, 41, 45, 49): d.line([27, y, 37, y], fill=BONE)
d.line([32, 34, 32, 54], fill=BONE2)
for y in (40, 46, 52): d.ellipse([18, y, 21, y + 3], fill=c('#E0B040'))                                                    # 단추
d.rectangle([14, 36, 20, 52], fill=BONE2, outline=OUT); d.rectangle([44, 36, 50, 52], fill=BONE2, outline=OUT)             # 팔뼈
d.line([48, 50, 58, 30], fill=c('#C8D0DC'), width=2); d.line([47, 51, 49, 49], fill=c('#E0B040'), width=2)                  # 휘어진 칼
d.rectangle([22, 56, 28, 62], fill=BONE, outline=OUT); d.rectangle([36, 56, 42, 62], fill=BONE, outline=OUT)
# 유령 기운(반투명 푸른 윤곽)
g = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([8, 4, 56, 62], fill=c('#6FF0D8', 36)); g.alpha_composite(cap); g.save('../../public/art/ev2_captain.png')
# ---- 보물 상자 (닫힘·열림, 32×32 두 칸) ----
ch = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(ch)
WD, WD2, GD = c('#8A5A2A'), c('#6A4220'), c('#E8B83A')
d.rectangle([3, 12, 28, 28], fill=WD, outline=OUT); d.rectangle([3, 18, 28, 20], fill=WD2); d.rectangle([14, 12, 17, 28], fill=GD, outline=OUT); d.rectangle([13, 17, 18, 22], fill=GD, outline=OUT); d.point((15, 19), fill=OUT)   # 닫힌 몸통과 자물쇠
d.pieslice([3, 4, 28, 20], 180, 360, fill=WD, outline=OUT); d.rectangle([3, 12, 28, 13], fill=WD2); d.rectangle([14, 5, 17, 13], fill=GD)
# 열린 상자
o = 32
d.rectangle([o + 3, 14, o + 28, 28], fill=WD, outline=OUT); d.rectangle([o + 3, 20, o + 28, 21], fill=WD2); d.rectangle([o + 5, 14, o + 26, 18], fill=c('#2A1A10'))
for gx, gy in ((8, 14), (13, 12), (18, 13), (22, 14), (11, 15)): d.ellipse([o + gx, gy, o + gx + 4, gy + 3], fill=GD, outline=OUT)
d.polygon([(o + 3, 14), (o + 28, 14), (o + 25, 4), (o + 6, 4)], fill=WD, outline=OUT); d.rectangle([o + 14, 5, o + 17, 13], fill=GD)
for _ in range(5): ch.putpixel((o + random.randint(6, 26), random.randint(0, 9)), c('#FFF2A0'))
ch.save('../../public/art/ev2_chest.png')
print('ok')
