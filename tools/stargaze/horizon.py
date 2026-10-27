#!/usr/bin/env python3
"""별 보는 밤 하늘 화면 아래쪽 풍경(언덕·소나무·학교·언덕 위 학생들) 도트 그림 → public/art/stargaze_horizon_{390,720}.png
   학교는 게임 지도의 본관 그림(art/iso/hw_obj.png)을 그대로 가져와 밤빛으로 어둡게 해요. 다시 만들기: python3 tools/stargaze/horizon.py"""
import math, random, os
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OBJ = Image.open(os.path.join(ROOT, 'public/art/iso/hw_obj.png')).convert('RGBA')
SCHOOL = OBJ.crop((0, 0, 226, 197))
FAR, MID, NEAR, TREE, EDGE = (27, 33, 82), (19, 24, 62), (12, 15, 40), (8, 11, 30), (22, 28, 70)
def school(scale):
    s = SCHOOL.resize((int(226 * scale), int(197 * scale)), Image.BOX); px = s.load()
    for y in range(s.height):
        for x in range(s.width):
            r, g, b, a = px[x, y]
            if a < 128: px[x, y] = (0, 0, 0, 0); continue
            if r > 200 and g > 170 and b < 190: px[x, y] = (255, 214, 120, 255); continue     # 불 켜진 창은 그대로 밝게
            px[x, y] = (int(r * .62), int(g * .64), int(b * .8), 255)
    return s
def pine(d, x, base, h, col):
    for k in range(4):
        w = 2 + k * 2 + h // 6; y0 = base - h + k * (h // 4)
        for yy in range(y0, y0 + h // 3 + 2):
            ww = max(1, w * (yy - y0 + 2) // (h // 3 + 3)); d.line([(x - ww, yy), (x + ww, yy)], fill=col)
    d.rectangle([x - 1, base - 3, x, base], fill=col)
def gen(w, h, seed=5):
    random.seed(seed); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def hill(amp, base, col, ph, f):   # 가장자리는 같은 높이로 끝나게 해서 넓은 화면에서도 이어 붙여 칠할 수 있어요
        for x in range(w):
            e = min(1, x / 30, (w - 1 - x) / 30)
            y = int(base - e * (amp * (math.sin(x / w * f + ph) * .6 + math.sin(x / w * f * 2.3 + ph * 2) * .4)) - (1 - e) * 0)
            d.line([(x, y), (x, h)], fill=col)
    hill(14, h - 46, FAR, 1.0, 7.5); hill(10, h - 30, MID, 2.4, 9.5)
    # 먼 소나무 줄
    for x in range(6, w, 11):
        base = h - 44 + int(math.sin(x / w * 7.5 + 1) * -6 * min(1, x / 30, (w - x) / 30)) + 4; pine(d, x + random.randint(-2, 2), base, random.randint(10, 15), (16, 20, 52))
    # 학교 (오른쪽 언덕 위)
    sc = school(.5); sx, sy = int(w * .70) - sc.width // 2, h - 72 - sc.height + 14
    d.ellipse([sx - 8, h - 80, sx + sc.width + 8, h - 58], fill=MID); im.alpha_composite(sc, (sx, sy)); d = ImageDraw.Draw(im)
    hill(6, h - 38, NEAR, 4.1, 8.5)
    # 앞쪽 소나무 몇 그루
    for x in (int(w * .40), int(w * .47), int(w * .95)): pine(d, x, h - 32, random.randint(16, 22), TREE)
    # 반딧불
    for _ in range(9):
        x, y = random.randint(8, w - 8), random.randint(h - 60, h - 14); d.point([(x, y)], fill=(255, 226, 140))
    return im
for w, h in ((390, 190), (720, 190)):
    gen(w, h).save(os.path.join(ROOT, f'public/art/stargaze_horizon_{w}.png')); print('저장', w, h)
