# 시안: 마틸다 졸업식 「졸업장」 그림 (120×84 · 게임 그림체: 짙은 갈색 테두리선 · 양피지 결 · 금빛 겹테두리 · 호박 모서리 · 붉은 밀랍 봉인과 리본)
#   python3 diploma.py → out/diploma.png
import os, random
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
H = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
W, HH = 120, 84; img = Image.new('RGBA', (W, HH), (0, 0, 0, 0)); d = ImageDraw.Draw(img); random.seed(7)
OL, P0, P1, P2, P3 = H('#3A2414'), H('#F4E6C4'), H('#E8D4A6'), H('#D6BC86'), H('#B89A62')
GD, GL, GS = H('#C8902A'), H('#F0C860'), H('#8A5A1A')
# 위아래 말린 두루마리 + 가운데 종이
x0, x1, y0, y1 = 8, 111, 9, 72
d.rectangle([x0, y0, x1, y1], fill=P1, outline=OL)
for yy in range(y0 + 1, y1):   # 양피지 결: 가장자리 어둡게 · 점 무늬
    for xx in range(x0 + 1, x1):
        e = min(xx - x0, x1 - xx, yy - y0, y1 - yy)
        c = P0 if e > 6 else P1 if e > 2 else P2
        r = random.random(); c = P2 if r < .035 else P0 if r < .07 and e > 3 else c
        img.putpixel((xx, yy), c)
def roll(y, top):   # 말린 두루마리 원통
    d.rectangle([x0 - 4, y - 4, x1 + 4, y + 4], fill=P2, outline=OL)
    d.line([(x0 - 3, y - 3 if top else y - 3), (x1 + 3, y - 3)], fill=P0); d.line([(x0 - 3, y - 1), (x1 + 3, y - 1)], fill=P1)
    d.line([(x0 - 3, y + 2), (x1 + 3, y + 2)], fill=P3); d.line([(x0 - 3, y + 3), (x1 + 3, y + 3)], fill=H('#9A7A48'))
    for ex in (x0 - 4, x1 + 4):   # 원통 끝 나무 손잡이
        d.rectangle([ex - 3, y - 3, ex + 3, y + 3], fill=H('#7A4A22'), outline=OL); d.point((ex - 1, y - 2), fill=H('#B07A40')); d.point((ex, y - 2), fill=H('#B07A40'))
roll(y0, True); roll(y1, False)
# 금빛 겹테두리
for i, c in ((0, GS), (1, GD), (3, GD)): d.rectangle([x0 + 4 + i, y0 + 7 + i, x1 - 4 - i, y1 - 7 - i], outline=c)
d.rectangle([x0 + 5, y0 + 8, x1 - 5, y1 - 8], outline=GL)
def pump(cx, cy):   # 모서리 작은 호박
    d.rectangle([cx - 2, cy - 1, cx + 2, cy + 2], fill=H('#E07A18'), outline=OL); d.point((cx, cy - 2), fill=H('#3A6A2A')); d.point((cx - 1, cy), fill=H('#F8A848')); d.point((cx + 1, cy + 1), fill=H('#B05A10'))
for cx, cy in ((x0 + 7, y0 + 10), (x1 - 7, y0 + 10), (x0 + 7, y1 - 10), (x1 - 7, y1 - 10)): pump(cx, cy)
# 제목 · 글줄
d.fontmode = '1'; f = ImageFont.truetype(FB, 12); t = '졸업장'; tw = d.textlength(t, font=f); tx = (W - tw) / 2
d.text((tx + 1, y0 + 11), t, font=f, fill=H('#E8C88A')); d.text((tx, y0 + 10), t, font=f, fill=H('#5A2A12'))
d.line([(38, y0 + 25), (82, y0 + 25)], fill=GD); d.point((37, y0 + 25), fill=GS); d.point((83, y0 + 25), fill=GS); d.point((60, y0 + 24), fill=GL)
for k, (a, b) in enumerate(((24, 96), (22, 98), (28, 78))):   # 흐린 글씨 줄 (손글씨처럼 끊겨요)
    yy = y0 + 30 + k * 5; xx = a
    while xx < b:
        ln = random.randint(3, 8); d.line([(xx, yy), (min(b, xx + ln), yy)], fill=H('#8A6A4A')); xx += ln + random.randint(1, 3)
# 서명 줄 + 이름 (해골 선생님 서명처럼 꼬불꼬불)
d.line([(70, y1 - 13), (98, y1 - 13)], fill=H('#8A6A4A'))
pts = [(72, y1 - 15), (75, y1 - 18), (77, y1 - 14), (80, y1 - 17), (83, y1 - 15), (86, y1 - 18), (90, y1 - 15), (95, y1 - 16)]; d.line(pts, fill=H('#3A2A5A'))
# 붉은 밀랍 봉인 + 리본 두 가닥
sx, sy = 36, y1 - 14
for dx, c in ((-4, H('#8A1A2A')), (2, H('#B02A3A'))):
    d.polygon([(sx + dx, sy + 2), (sx + dx + 4, sy + 2), (sx + dx + 5 + (dx > 0) * 2, sy + 14), (sx + dx + 2, sy + 11), (sx + dx - 1 - (dx < 0) * 2, sy + 14)], fill=c, outline=OL)
d.ellipse([sx - 8, sy - 7, sx + 8, sy + 7], fill=H('#C02A30'), outline=OL)
d.ellipse([sx - 6, sy - 5, sx + 6, sy + 5], outline=H('#8A1420'))
for p in ((sx - 5, sy - 6), (sx + 6, sy - 3), (sx - 7, sy + 3), (sx + 4, sy + 6)): d.point(p, fill=H('#C02A30'))   # 울퉁불퉁 가장자리
d.rectangle([sx - 3, sy - 2, sx + 3, sy + 3], fill=H('#E04A40')); d.point((sx, sy - 3), fill=H('#7A1018'))   # 봉인 속 호박 무늬
d.line([(sx - 1, sy - 2), (sx - 1, sy + 3)], fill=H('#A01A22')); d.line([(sx + 1, sy - 2), (sx + 1, sy + 3)], fill=H('#A01A22'))
d.point((sx - 4, sy - 4), fill=H('#FF8A80')); d.point((sx - 3, sy - 5), fill=H('#FF8A80'))   # 반짝 하이라이트
img.save(os.path.join(OUT, 'diploma.png'))
img.resize((W * 4, HH * 4), Image.NEAREST).save(os.path.join(OUT, 'diploma_preview.png')); print('ok')
