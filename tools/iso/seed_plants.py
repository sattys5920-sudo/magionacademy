# 마법 씨앗 대회 시안: 화분 하나가 5일 동안 자라는 단계 그림 + 최종 꽃 5종 + 온실 배경
#   python3 seed_plants.py → out/seed_plants.png (48×64 칸: 0 씨앗 · 1 새싹 · 2 떡잎 · 3 꽃봉오리(물·해·노래·달·무지개 5색) · 4 최종 꽃 5종) · out/seed_bg.png (320×180) · out/seed_preview.png
import os, math, random
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
CW, CH = 48, 64
def hx(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
def cell(): im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def pot(d):   # 테라코타 화분 (아래 가운데)
    d.polygon([(14, 50), (34, 50), (31, 62), (17, 62)], fill=hx('#C8683C')); d.polygon([(14, 50), (18, 50), (19, 62), (17, 62)], fill=hx('#E08850'))
    d.polygon([(29, 50), (34, 50), (31, 62), (30, 62)], fill=hx('#A04E2C'))
    d.rectangle([12, 47, 35, 51], fill=hx('#D87848')); d.line([(12, 47), (35, 47)], fill=hx('#F0A070')); d.line([(12, 51), (35, 51)], fill=hx('#8A4024'))
    d.rectangle([14, 46, 33, 47], fill=hx('#4A3024')); d.point((18, 46), fill=hx('#6A4834')); d.point((27, 46), fill=hx('#6A4834'))
    for x, y in ((22, 56), (24, 57), (26, 56)): d.point((x, y), fill=hx('#F0C060'))   # 별 무늬
def leaf(d, x, y, dx, dy, c, w=2):
    pts = [(x + dx * t / 6 + (-dy) * math.sin(t / 6 * math.pi) * w / 6, y + dy * t / 6 + dx * math.sin(t / 6 * math.pi) * w / 6) for t in range(7)]
    pts2 = [(x + dx * t / 6 - (-dy) * math.sin(t / 6 * math.pi) * w / 6, y + dy * t / 6 - dx * math.sin(t / 6 * math.pi) * w / 6) for t in range(6, -1, -1)]
    d.polygon(pts + pts2, fill=hx(c)); d.line([(x, y), (x + dx * .8, y + dy * .8)], fill=shade(hx(c), .75))
def stem(d, x, y0, y1, c='#4A8A3A', sway=0):
    for y in range(y1, y0 + 1): d.point((round(x + sway * math.sin((y0 - y) / 8)), y), fill=hx(c))
def glowdot(d, x, y, c): d.point((x, y), fill=hx(c)); [d.point((x + a, y + b), fill=shade(hx(c), .7)) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
CARE = [('물', '#5AB8F0'), ('햇빛', '#FFC838'), ('노래', '#B070F0'), ('달빛', '#D8E0FF'), ('무지개', '#FF70A0')]
sheet = []
# 0 씨앗: 흙 위에 반짝이는 씨앗
im, d = cell(); pot(d); d.ellipse([21, 42, 27, 47], fill=hx('#8A5AB8')); d.point((23, 43), fill=hx('#E8C8FF')); glowdot(d, 30, 40, '#FFE8A0'); sheet.append(im)
# 1 새싹
im, d = cell(); pot(d); stem(d, 24, 46, 38); leaf(d, 24, 39, -5, -3, '#6ACA4A'); leaf(d, 24, 39, 5, -3, '#7ADA5A'); sheet.append(im)
# 2 떡잎·잎 넷
im, d = cell(); pot(d); stem(d, 24, 46, 28, sway=1)
for (y, dx) in ((40, -7), (40, 7), (33, -6), (33, 6)): leaf(d, 24, y, dx, -4, '#5ABA4A' if dx < 0 else '#6ACA5A', 3)
glowdot(d, 24, 27, '#C8FFB0'); sheet.append(im)
# 3 꽃봉오리 5색
for nm, c in CARE:
    im, d = cell(); pot(d); stem(d, 24, 46, 22, sway=1.2)
    for (y, dx) in ((41, -8), (41, 8), (35, -7), (35, 7), (29, -5), (29, 5)): leaf(d, 24, y, dx, -4, '#4AAA3A' if dx < 0 else '#5ABA4A', 3)
    if nm == '무지개':
        for i, cc in enumerate(['#FF70A0', '#FFC838', '#6ADA6A', '#5AB8F0', '#B070F0']): d.pieslice([19, 13, 29, 25], -90 + i * 72 - 36, -90 + i * 72 + 36, fill=hx(cc))
    else: d.ellipse([19, 13, 29, 25], fill=hx(c)); d.ellipse([21, 15, 25, 19], fill=shade(hx(c), 1.25))
    d.polygon([(19, 22), (24, 26), (29, 22), (24, 21)], fill=hx('#4AAA3A')); sheet.append(im)
# 4 최종 꽃 5종
def final(nm):
    im, d = cell(); pot(d); stem(d, 24, 46, 20, sway=1)
    for (y, dx) in ((42, -9), (42, 9), (36, -8), (36, 8), (30, -6), (30, 6)): leaf(d, 24, y, dx, -4, '#3A9A3A' if dx < 0 else '#4AAA4A', 3)
    if nm == '물':   # 물방울 백합: 파란 투명 꽃잎 + 물방울
        for a in range(6): r = math.radians(a * 60 - 90); d.polygon([(24, 16), (24 + 12 * math.cos(r - .35), 16 + 12 * math.sin(r - .35)), (24 + 15 * math.cos(r), 16 + 15 * math.sin(r)), (24 + 12 * math.cos(r + .35), 16 + 12 * math.sin(r + .35))], fill=hx('#7AC8F8' if a % 2 else '#5AB0F0'))
        d.ellipse([21, 13, 27, 19], fill=hx('#E8F8FF'))
        for x, y in ((8, 10), (40, 14), (12, 28), (37, 30)): d.ellipse([x - 1, y - 2, x + 1, y + 1], fill=hx('#A8E0FF')); d.point((x, y - 1), fill=hx('#FFFFFF'))
    elif nm == '햇빛':   # 햇살 왕관꽃: 큰 금빛 꽃 + 왕관 꽃잎
        for a in range(12): r = math.radians(a * 30); d.polygon([(24 + 6 * math.cos(r - .3), 16 + 6 * math.sin(r - .3)), (24 + 15 * math.cos(r), 16 + 15 * math.sin(r)), (24 + 6 * math.cos(r + .3), 16 + 6 * math.sin(r + .3))], fill=hx('#FFC838' if a % 2 else '#FFB020'))
        d.ellipse([18, 10, 30, 22], fill=hx('#8A5A20')); d.ellipse([20, 12, 28, 20], fill=hx('#A87030'))
        d.polygon([(19, 4), (21, 0), (23, 4), (25, 0), (27, 4), (29, 0), (29, 6), (19, 6)], fill=hx('#FFE070'))
    elif nm == '노래':   # 노래하는 종꽃: 늘어진 보라 종 + 음표
        d.line([(24, 20), (14, 10), (8, 14)], fill=hx('#4A8A3A')); d.line([(24, 20), (34, 9), (40, 13)], fill=hx('#4A8A3A')); d.line([(24, 20), (24, 6)], fill=hx('#4A8A3A'))
        for x, y in ((8, 16), (14, 12), (40, 15), (34, 11), (24, 8), (19, 9), (29, 8)):
            d.polygon([(x - 3, y + 5), (x - 2, y), (x + 2, y), (x + 3, y + 5)], fill=hx('#B070F0')); d.line([(x - 3, y + 5), (x + 3, y + 5)], fill=hx('#D8A8FF')); d.point((x, y + 6), fill=hx('#FFE070'))
        for x, y in ((4, 4), (42, 3)): d.ellipse([x, y + 3, x + 2, y + 5], fill=hx('#FFE070')); d.line([(x + 2, y + 4), (x + 2, y)], fill=hx('#FFE070')); d.line([(x + 2, y), (x + 4, y + 1)], fill=hx('#FFE070'))
    elif nm == '달빛':   # 달빛 장미: 은빛 장미 셋 + 빛
        for x, y, s in ((24, 12, 7), (14, 20, 5), (34, 19, 5)):
            d.ellipse([x - s, y - s, x + s, y + s], fill=hx('#C8D0F0')); d.ellipse([x - s + 2, y - s + 2, x + s - 2, y + s - 2], fill=hx('#E8ECFF'))
            d.arc([x - s + 1, y - s + 1, x + s - 1, y + s - 1], 200, 340, fill=hx('#A0A8D8')); d.arc([x - 2, y - 2, x + 2, y + 2], 0, 270, fill=hx('#A0A8D8'))
        for x, y in ((6, 6), (42, 8), (24, 2)): glowdot(d, x, y, '#FFFFFF')
        d.ellipse([36, 0, 44, 8], fill=hx('#F0F0D0')); d.ellipse([38, -1, 46, 7], fill=(0, 0, 0, 0))
    else:   # 무지개 꽃: 일곱 빛깔 꽃잎
        cols = ['#FF5A70', '#FF9A40', '#FFE050', '#6ADA6A', '#5AB8F0', '#7A7AF0', '#C070F0']
        for a in range(14): r = math.radians(a * 360 / 14 - 90); d.polygon([(24, 16), (24 + 15 * math.cos(r - .22), 16 + 15 * math.sin(r - .22)), (24 + 15 * math.cos(r + .22), 16 + 15 * math.sin(r + .22))], fill=hx(cols[a % 7]))
        d.ellipse([20, 12, 28, 20], fill=hx('#FFFFFF')); d.ellipse([22, 14, 26, 18], fill=hx('#FFE8A0'))
        for x, y in ((6, 8), (42, 6), (8, 30), (40, 28)): glowdot(d, x, y, cols[(x + y) % 7])
    return im
for nm, _ in CARE: sheet.append(final(nm))
S = Image.new('RGBA', (CW * len(sheet), CH), (0, 0, 0, 0))
for i, c in enumerate(sheet): S.alpha_composite(c, (i * CW, 0))
S.save(os.path.join(OUT, 'seed_plants.png'))
# 온실 배경 320×180: 유리 온실 안, 가운데 작은 받침대, 창밖 낮 하늘
W, H = 320, 180; bg = Image.new('RGBA', (W, H), hx('#2A4A3A')); d = ImageDraw.Draw(bg)
for y in range(0, 120): c = (int(150 + y * .5), int(200 + y * .2), int(235 - y * .1), 255); d.line([(0, y), (W, y)], fill=c)
random.seed(3)
for x in range(-20, W, 34): d.ellipse([x, 70 + random.randint(-8, 8), x + 60, 120], fill=hx('#7AB87A'))   # 먼 덤불
for x in range(0, W + 1, 40): d.rectangle([x - 2, 0, x + 1, 120], fill=hx('#E8F0E8')); d.line([(x - 2, 0), (x - 2, 120)], fill=hx('#B8C8B8'))   # 온실 창틀
for y in (30, 75): d.rectangle([0, y - 1, W, y + 1], fill=hx('#E8F0E8'))
for x in range(0, W, 40): d.line([(x + 6, 6), (x + 14, 20)], fill=(255, 255, 255, 160)); d.line([(x + 10, 6), (x + 16, 16)], fill=(255, 255, 255, 120))   # 유리 반짝
d.rectangle([0, 120, W, H], fill=hx('#6A4A34'))
for x in range(0, W, 16): d.rectangle([x, 120, x + 15, H], fill=hx('#7A5A3E' if (x // 16) % 2 else '#6E5038')); d.line([(x, 120), (x, H)], fill=hx('#4A3424'))
d.line([(0, 120), (W, 120)], fill=hx('#9A7A58'))
for x, c in ((30, '#C8683C'), (70, '#A86A9A'), (250, '#C8683C'), (290, '#6A9AB8')):   # 양옆 화분들
    d.polygon([(x - 10, 112), (x + 10, 112), (x + 7, 124), (x - 7, 124)], fill=hx(c))
    for k in range(5): d.ellipse([x - 9 + k * 3, 96 + (k % 2) * 4, x - 3 + k * 3, 106 + (k % 2) * 4], fill=hx('#4AAA4A' if k % 2 else '#3A9A3A'))
d.rectangle([128, 120, 192, 126], fill=hx('#B8906A')); d.rectangle([132, 126, 188, 150], fill=hx('#9A7450')); d.line([(128, 120), (192, 120)], fill=hx('#D8B088'))   # 가운데 받침대
d.rectangle([136, 130, 184, 146], outline=hx('#7A5A3A'))
bg.save(os.path.join(OUT, 'seed_bg.png'))
# 미리보기
big = S.resize((S.width * 3, S.height * 3), Image.NEAREST); pv = Image.new('RGB', (big.width + 20, big.height + 70), (42, 30, 58)); pv.paste(big, (10, 50), big)
fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'; F = ImageFont.truetype(fb, 14) if os.path.exists(fb) else ImageFont.load_default()
dd = ImageDraw.Draw(pv); dd.text((10, 14), '씨앗 → 새싹 → 잎 → 꽃봉오리(5색) → 최종 꽃(물방울 백합 · 햇살 왕관꽃 · 노래하는 종꽃 · 달빛 장미 · 무지개 꽃)', font=F, fill=(255, 233, 160))
pv.save(os.path.join(OUT, 'seed_preview.png')); print('ok', S.size)
