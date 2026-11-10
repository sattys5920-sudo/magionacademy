# 새 직업 12 종 상징을 public/art/jobs.png 오른쪽에 붙여요 (기존 12 칸은 그대로) → 32px × 24 칸
#   python3 tools/job_icons.py 로 기존 12 칸을 다시 만든 뒤에 돌려도 돼요 (앞 12 칸만 잘라 써요)
from PIL import Image, ImageDraw
import math
O = (43, 27, 58, 255)
JOBS = [('paladin', (200, 165, 70), (255, 250, 230)), ('guardian', (60, 110, 170), (230, 235, 245)), ('darkknight', (90, 45, 110), (200, 140, 255)),
        ('dancer', (205, 85, 145), (255, 225, 160)), ('sage', (55, 145, 185), (240, 250, 255)), ('shaman', (85, 140, 75), (200, 120, 70)),
        ('miko', (195, 70, 70), (255, 248, 232)), ('archer', (115, 145, 60), (235, 220, 170)), ('gunner', (170, 110, 50), (220, 225, 235)),
        ('elemental', (70, 115, 180), (255, 255, 255)), ('fighter', (190, 90, 50), (255, 220, 180)), ('bladedancer', (105, 95, 165), (230, 230, 245))]
S = 32
def badge(d, bg):
    d.ellipse([1, 1, 30, 30], fill=O); d.ellipse([3, 3, 28, 28], fill=bg)
    d.ellipse([5, 5, 26, 26], outline=tuple(min(255, c + 30) for c in bg[:3]) + (255,))
def icon(k, bg, fg):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); badge(d, bg + (255,)); fg += (255,)
    def poly(p, f=fg): d.polygon(p, fill=f, outline=O)
    if k == 'paladin':      # 금빛 방패 + 흰 십자
        poly([(8, 7), (24, 7), (24, 17), (16, 27), (8, 17)], (255, 214, 102, 255)); d.rectangle([14, 9, 17, 22], fill=fg, outline=O); d.rectangle([10, 12, 21, 15], fill=fg, outline=O)
    elif k == 'guardian':   # 창 (세로)
        d.line([(16, 26), (16, 10)], fill=O, width=4); d.line([(16, 26), (16, 10)], fill=(150, 100, 60, 255), width=2); poly([(16, 4), (20, 11), (16, 13), (12, 11)]); d.rectangle([12, 13, 20, 14], fill=(255, 214, 102, 255), outline=O)
    elif k == 'darkknight': # 어둠의 투구
        poly([(9, 24), (9, 12), (16, 6), (23, 12), (23, 24), (19, 24), (19, 17), (13, 17), (13, 24)], (70, 60, 90, 255)); d.rectangle([11, 13, 21, 15], fill=fg, outline=O); d.line([(16, 6), (16, 3)], fill=fg, width=2)
    elif k == 'dancer':     # 부채
        for a in range(-60, 61, 20):
            r = math.radians(a - 90); d.line([(16, 24), (16 + 12 * math.cos(r), 24 + 12 * math.sin(r))], fill=O, width=3)
        d.pieslice([4, 12, 28, 36], 210, 330, fill=fg, outline=O); [d.line([(16, 24), (16 + 11 * math.cos(math.radians(a - 90)), 24 + 11 * math.sin(math.radians(a - 90)))], fill=(230, 110, 150, 255)) for a in (-40, 0, 40)]; d.ellipse([14, 22, 18, 26], fill=O)
    elif k == 'sage':       # 펼친 책 + 룬
        poly([(5, 10), (15, 8), (16, 24), (5, 25)]); poly([(27, 10), (17, 8), (16, 24), (27, 25)]); d.line([(8, 14), (13, 13)], fill=(55, 145, 185, 255)); d.line([(8, 18), (13, 17)], fill=(55, 145, 185, 255)); d.ellipse([19, 13, 24, 18], outline=(55, 145, 185, 255))
    elif k == 'shaman':     # 토템 얼굴
        d.rectangle([11, 6, 21, 26], fill=fg, outline=O); d.rectangle([12, 10, 14, 12], fill=O); d.rectangle([18, 10, 20, 12], fill=O); d.rectangle([13, 16, 19, 17], fill=O); poly([(5, 8), (11, 10), (11, 13)], (255, 214, 102, 255)); poly([(27, 8), (21, 10), (21, 13)], (255, 214, 102, 255)); d.rectangle([11, 20, 21, 21], fill=(85, 140, 75, 255))
    elif k == 'miko':       # 부적
        d.rectangle([11, 5, 21, 27], fill=fg, outline=O); d.rectangle([12, 6, 20, 8], fill=(195, 50, 50, 255)); d.rectangle([15, 10, 17, 22], fill=(195, 50, 50, 255)); d.rectangle([13, 13, 19, 14], fill=(195, 50, 50, 255)); d.rectangle([13, 18, 19, 19], fill=(195, 50, 50, 255))
    elif k == 'archer':     # 활 + 화살
        d.arc([5, 5, 23, 27], 270, 90, fill=O, width=4); d.arc([5, 5, 23, 27], 270, 90, fill=(150, 100, 60, 255), width=2); d.line([(14, 6), (14, 26)], fill=fg, width=1)
        d.line([(8, 16), (26, 16)], fill=O, width=3); d.line([(8, 16), (26, 16)], fill=fg, width=1); poly([(27, 16), (23, 13), (23, 19)])
    elif k == 'gunner':     # 권총
        poly([(6, 11), (26, 11), (26, 16), (14, 16), (12, 25), (7, 25), (8, 16), (6, 16)]); d.rectangle([22, 9, 24, 11], fill=O); d.rectangle([9, 18, 11, 22], fill=(170, 110, 50, 255))
    elif k == 'elemental':  # 불 · 물 · 바람 구슬
        for (x, y), c in zip([(16, 9), (9, 21), (23, 21)], [(255, 120, 60), (90, 170, 255), (190, 255, 230)]):
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=c + (255,), outline=O); d.rectangle([x - 2, y - 3, x - 1, y - 2], fill=fg)
    elif k == 'fighter':    # 주먹
        d.rounded_rectangle([8, 10, 24, 24], 4, fill=fg, outline=O); [d.line([(x, 10), (x, 16)], fill=O) for x in (12, 16, 20)]; d.rectangle([8, 22, 24, 26], fill=(220, 60, 50, 255), outline=O)
    elif k == 'bladedancer':  # 엇갈린 쌍검
        for s in (1, -1):
            x0, x1 = (16 - 10 * s, 16 + 9 * s); d.line([(x0, 25), (x1, 6)], fill=O, width=4); d.line([(x0, 25), (x1, 6)], fill=fg, width=2)
            d.line([(16 - 8 * s, 19), (16 - 4 * s, 23)], fill=(255, 214, 102, 255), width=3)
    return im
old = Image.open('public/art/jobs.png').convert('RGBA'); base = old.crop((0, 0, 64 * 12, 64))
sheet = Image.new('RGBA', (64 * 24, 64)); sheet.paste(base, (0, 0))
for i, (k, bg, fg) in enumerate(JOBS): sheet.paste(icon(k, bg, fg).resize((64, 64), Image.NEAREST), ((12 + i) * 64, 0))
sheet.save('public/art/jobs.png', optimize=True)
sheet.resize((64 * 24 * 2 // 2, 64), Image.NEAREST).crop((64 * 12, 0, 64 * 24, 64)).resize((64 * 12 * 2, 128), Image.NEAREST).save('tools/newjobs/job_icons_new.png')
print('ok', sheet.size)
