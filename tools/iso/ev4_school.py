# 이벤트 「유령 등불 찾기」 연출 배경: 어두운 학교와 환한 학교 (200×120) → public/art/ev4_school_dim.png · ev4_school_lit.png
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def make(lit, name):
    random.seed(21); W, H = 200, 120
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    top, bot = ((8, 8, 28), (26, 22, 58)) if not lit else ((26, 22, 70), (92, 70, 120))
    for y in range(H): k = y / H; d.line([0, y, W, y], fill=tuple(int(a + (b - a) * k) for a, b in zip(top, bot)) + (255,))
    for _ in range(50 if not lit else 30): d.point((random.randrange(W), random.randrange(60)), fill=c('#CFCFF0') if random.random() < .5 else c('#8E8EC0'))
    d.ellipse([160, 10, 180, 30], fill=c('#EDEBC8')); d.ellipse([165, 14, 172, 21], fill=c('#D4D2AE'))
    for x, h in ((4, 30), (22, 22), (170, 28), (188, 34), (150, 20)):                       # 뒤쪽 나무
        d.polygon([(x - 9, 86), (x, 86 - h), (x + 9, 86)], fill=c('#161a30' if not lit else '#2a2c58'))
    wall, roof = (c('#2a2448'), c('#1a1634')) if not lit else (c('#5a4a86'), c('#3a2e66'))
    d.rectangle([46, 52, 154, 94], fill=wall); d.polygon([(40, 52), (100, 28), (160, 52)], fill=roof)                 # 학교 본관
    d.rectangle([92, 20, 108, 52], fill=wall); d.polygon([(88, 20), (100, 2), (112, 20)], fill=roof); d.rectangle([99, 0, 101, 4], fill=roof)   # 탑
    d.rectangle([30, 64, 50, 94], fill=wall); d.polygon([(27, 64), (40, 52), (53, 64)], fill=roof); d.rectangle([150, 64, 170, 94], fill=wall); d.polygon([(147, 64), (160, 52), (173, 64)], fill=roof)
    wcol = c('#FFD87A') if lit else c('#14102a')
    for x in range(54, 150, 14):
        for y in (58, 74): d.rectangle([x, y, x + 6, y + 9], fill=wcol, outline=c('#0e0a1c'))
    d.rectangle([97, 26, 103, 36], fill=wcol, outline=c('#0e0a1c')); d.rectangle([94, 78, 106, 94], fill=c('#FFC060') if lit else c('#0e0a1c'), outline=c('#0e0a1c'))
    d.rectangle([0, 94, W, H], fill=c('#10142a') if not lit else c('#34305c'))
    for x in range(0, W, 8): d.line([x, 94, x + 4, 96], fill=c('#0b0e20') if not lit else c('#403a6e'))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    posts = [(14, 70), (58, 80), (142, 80), (186, 70)]
    for x, y in posts:                                                                       # 가로등 + 등불
        d.rectangle([x, y, x + 1, 94], fill=c('#0b0e20')); d.rectangle([x - 2, y - 6, x + 3, y], fill=c('#1f4e5f'), outline=c('#0b1f2c')); d.rectangle([x - 1, y - 5, x + 2, y - 1], fill=c('#3FE0A0') if lit else c('#223a44'))
        if lit: gd.ellipse([x - 20, y - 24, x + 22, y + 18], fill=c('#3FE0A0', 70)); gd.ellipse([x - 9, y - 13, x + 11, y + 7], fill=c('#C8FFE8', 90))
    for i in range(7):                                                                      # 처마에 매단 줄등불
        x = 48 + i * 17; y = 52 + int(4 * math.sin(i * 1.1)); d.line([x, 52, x, y + 2], fill=c('#0b0e20')); d.ellipse([x - 2, y + 2, x + 2, y + 7], fill=c('#FFC060') if lit else c('#2a2438'), outline=c('#0b0e20'))
        if lit: gd.ellipse([x - 10, y - 6, x + 12, y + 16], fill=c('#FFC060', 80))
    glow = glow.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(glow)
    im.save(f'../../public/art/{name}.png')
make(False, 'ev4_school_dim'); make(True, 'ev4_school_lit'); print('ok')
