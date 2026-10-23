# 탐사 직업 12종 상징 → public/art/jobs.png (32px × 12칸 가로 스프라이트)
from PIL import Image, ImageDraw
import math
O = (43, 27, 58, 255)      # 외곽선(앱 진보라)
JOBS = [  # id, 배경색, 밝은 색
    ('warrior', (196, 74, 74), (245, 245, 250)), ('black', (110, 66, 170), (255, 150, 60)),
    ('thief', (70, 80, 110), (220, 225, 235)), ('bard', (214, 130, 60), (255, 236, 160)),
    ('time', (60, 140, 160), (255, 226, 130)), ('alch', (90, 160, 90), (190, 120, 230)),
    ('white', (230, 190, 90), (255, 255, 255)), ('druid', (70, 130, 70), (170, 235, 120)),
    ('cleric', (150, 160, 200), (255, 240, 150)), ('knight', (80, 110, 190), (230, 230, 240)),
    ('summon', (150, 70, 140), (255, 160, 220)), ('gadget', (140, 110, 80), (230, 200, 120))]
S = 32
def badge(d, bg):
    d.ellipse([1, 1, 30, 30], fill=O); d.ellipse([3, 3, 28, 28], fill=bg)
    d.ellipse([5, 5, 26, 26], outline=tuple(min(255, c + 30) for c in bg[:3]) + (255,))
def icon(i):
    k, bg, fg = JOBS[i]; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); badge(d, bg + (255,)); fg += (255,)
    def poly(p, f=fg): d.polygon(p, fill=f, outline=O)
    if k == 'warrior':   # 도끼
        d.line([(12, 25), (20, 8)], fill=O, width=4); d.line([(12, 25), (20, 8)], fill=(150, 100, 60, 255), width=2)
        poly([(17, 7), (25, 9), (24, 16), (19, 14)])
    elif k == 'black':   # 불꽃
        poly([(16, 6), (22, 14), (24, 20), (16, 26), (8, 20), (10, 13), (14, 16)]); poly([(16, 14), (19, 20), (16, 24), (13, 20)], (255, 230, 120, 255))
    elif k == 'thief':   # 단검
        poly([(16, 5), (19, 18), (16, 20), (13, 18)]); d.rectangle([11, 19, 20, 21], fill=(210, 160, 70, 255), outline=O); d.rectangle([15, 22, 17, 26], fill=O)
    elif k == 'bard':    # 음표
        d.ellipse([9, 18, 15, 24], fill=fg, outline=O); d.ellipse([18, 16, 24, 22], fill=fg, outline=O)
        d.rectangle([14, 8, 15, 21], fill=O); d.rectangle([23, 6, 24, 19], fill=O); d.rectangle([14, 7, 24, 10], fill=fg, outline=O)
    elif k == 'time':    # 모래시계
        poly([(10, 7), (22, 7), (17, 16), (22, 25), (10, 25), (15, 16)]); poly([(13, 21), (19, 21), (19, 24), (13, 24)], (230, 170, 60, 255)); d.rectangle([9, 5, 23, 7], fill=O); d.rectangle([9, 25, 23, 27], fill=O)
    elif k == 'alch':    # 플라스크
        poly([(14, 6), (18, 6), (18, 13), (24, 24), (22, 26), (10, 26), (8, 24), (14, 13)]); poly([(11, 20), (21, 20), (23, 24), (21, 25), (11, 25), (9, 24)], fg[:3] and (190, 90, 230, 255)); d.rectangle([13, 4, 19, 6], fill=O)
    elif k == 'white':   # 반짝 별
        poly([(16, 5), (19, 13), (27, 16), (19, 19), (16, 27), (13, 19), (5, 16), (13, 13)])
    elif k == 'druid':   # 잎
        poly([(8, 24), (9, 12), (17, 6), (24, 8), (24, 17), (16, 24)]); d.line([(10, 23), (21, 11)], fill=O, width=1)
    elif k == 'cleric':  # 종
        poly([(16, 6), (21, 12), (22, 20), (25, 23), (7, 23), (10, 20), (11, 12)]); d.ellipse([14, 24, 18, 27], fill=O)
    elif k == 'knight':  # 방패
        poly([(8, 8), (24, 8), (24, 17), (16, 27), (8, 17)]); poly([(12, 11), (20, 11), (20, 16), (16, 22), (12, 16)], (190, 60, 60, 255))
    elif k == 'summon':  # 마법진 별
        d.ellipse([7, 7, 25, 25], outline=O, width=3)
        pts = [(16 + 8 * math.sin(math.radians(a * 144)), 16 - 8 * math.cos(math.radians(a * 144))) for a in range(5)]
        d.line(pts + [pts[0]], fill=fg, width=2)
    elif k == 'gadget':  # 톱니
        for a in range(8):
            x, y = 16 + 9 * math.cos(a * math.pi / 4), 16 + 9 * math.sin(a * math.pi / 4); d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=fg, outline=O)
        d.ellipse([8, 8, 24, 24], fill=fg, outline=O); d.ellipse([13, 13, 19, 19], fill=bg + (255,), outline=O)
    return im
sheet = Image.new('RGBA', (S * 12, S))
for i in range(12): sheet.paste(icon(i), (i * S, 0))
sheet = sheet.resize((S * 12 * 2, S * 2), Image.NEAREST)
sheet.save('public/art/jobs.png', optimize=True)
