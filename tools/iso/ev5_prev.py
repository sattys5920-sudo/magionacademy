# 이벤트 「호박밭 같이 가꾸기」 시안: 거대 호박 5단계 도트 + 실제 게임 화면 위에 얹은 장면 → out/ev5_sheet.png, out/ev5_stages.png
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH = sys.argv[1]; OUTD = os.path.dirname(os.path.abspath(__file__)) + '/out'
random.seed(5)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
FP = '/usr/share/fonts/opentype/unifont/unifont.otf'; F16 = ImageFont.truetype(FP, 16); F32 = ImageFont.truetype(FP, 32)
OUT = c('#1A0F1F')
def shot(n): return Image.open(f'{SH}/{n}.png').convert('RGBA').resize((390, 740), Image.LANCZOS)
# ---- 호박 5단계 (48×48 도트) ----
def stage(k):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    SOIL, SOIL2 = c('#5A3A24'), c('#3E2616'); LEAF, LEAF2, LEAFD = c('#5FC24A'), c('#3E9A3A'), c('#256A2E')
    ORA, ORA2, ORA3 = c('#FFA02A'), c('#E27010'), c('#B24A08')
    def mound(w=16): d.ellipse([24 - w, 38, 24 + w, 46], fill=SOIL, outline=OUT); d.ellipse([24 - w + 3, 39, 24 + w - 3, 43], fill=SOIL2)
    def leaf(cx, cy, w, h, flip=1):
        d.ellipse([cx - w, cy - h, cx + w, cy + h], fill=LEAF, outline=OUT); d.line([cx - w + 2, cy, cx + w - 2, cy + (1 if flip > 0 else -1)], fill=LEAF2)
    def pump(cx, cy, rx, ry, green=0.0, face=False):
        col = ORA if green < .5 else c('#9ACB4A'); col2 = ORA2 if green < .5 else c('#6FA838'); col3 = ORA3 if green < .5 else c('#4A7A2A')
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col2, outline=OUT)
        d.ellipse([cx - rx + rx // 2, cy - ry + 1, cx + rx - rx // 2, cy + ry - 1], fill=col)
        d.ellipse([cx - rx // 4, cy - ry + 1, cx + rx // 4, cy + ry - 1], fill=col, outline=col3)
        d.line([cx - rx + 2, cy - ry // 3, cx - rx + 4, cy + ry // 3], fill=c('#FFD070') if green < .5 else c('#C8E88A'))
        d.rectangle([cx - 1, cy - ry - 3, cx + 1, cy - ry + 1], fill=c('#4A7A2A'), outline=OUT)
        if face:
            d.polygon([(cx - rx // 2 - 3, cy - 3), (cx - rx // 2 + 1, cy - 8), (cx - rx // 2 + 5, cy - 3)], fill=c('#3A1A00')); d.polygon([(cx + rx // 2 - 5, cy - 3), (cx + rx // 2 - 1, cy - 8), (cx + rx // 2 + 3, cy - 3)], fill=c('#3A1A00'))
            d.arc([cx - 8, cy - 1, cx + 8, cy + 9], 10, 170, fill=c('#3A1A00'), width=2); d.rectangle([cx - 3, cy + 6, cx - 2, cy + 8], fill=c('#FFF2A0'))
    if k == 0:
        mound(12); d.ellipse([21, 33, 27, 39], fill=c('#C8A060'), outline=OUT); d.line([24, 34, 24, 38], fill=c('#8A6030'))
        for x, y in ((14, 36), (34, 37), (30, 34)): d.point((x, y), fill=c('#7A5230'))
    elif k == 1:
        mound(13); d.line([24, 38, 24, 28], fill=OUT, width=3); d.line([24, 38, 24, 28], fill=LEAF2, width=1); leaf(18, 28, 6, 3, -1); leaf(31, 26, 7, 3, 1); d.ellipse([21, 22, 27, 28], fill=LEAF, outline=OUT)
    elif k == 2:
        mound(15)
        for x0, y0, x1, y1 in ((8, 40, 18, 32), (18, 32, 28, 34), (28, 34, 40, 28)): d.line([x0, y0, x1, y1], fill=OUT, width=3); d.line([x0, y0, x1, y1], fill=LEAF2, width=1)
        leaf(14, 31, 5, 3, -1); leaf(30, 30, 6, 3); leaf(38, 25, 5, 3); pump(24, 36, 8, 6, green=1)
    elif k == 3:
        mound(18)
        for x0, y0, x1, y1 in ((4, 41, 14, 31), (14, 31, 24, 33), (24, 33, 36, 27), (36, 27, 44, 33)): d.line([x0, y0, x1, y1], fill=OUT, width=3); d.line([x0, y0, x1, y1], fill=LEAF2, width=1)
        for cx, cy, w in ((10, 30, 6), (30, 29, 7), (42, 26, 5), (20, 28, 5)): leaf(cx, cy, w, 4)
        pump(24, 33, 13, 10, green=0); d.ellipse([34, 17, 40, 23], fill=c('#FFE66A'), outline=OUT); d.ellipse([36, 19, 38, 21], fill=c('#FF9A2A'))                            # 꽃
    else:
        mound(20)
        for x0, y0, x1, y1 in ((2, 43, 12, 33), (36, 33, 46, 43)): d.line([x0, y0, x1, y1], fill=OUT, width=3); d.line([x0, y0, x1, y1], fill=LEAF2, width=1)
        for cx, cy, w in ((8, 36, 6), (40, 36, 6), (12, 28, 5), (36, 28, 5)): leaf(cx, cy, w, 4)
        pump(24, 28, 19, 15, green=0, face=True)
    return im
ST = [stage(k) for k in range(5)]
glow = lambda r, col, a: Image.new('RGBA', (r * 2, r * 2), (0, 0, 0, 0))
def paste_sprite(im, k, cx, by, scale, glw=False):
    s = ST[k].resize((48 * scale, 48 * scale), Image.NEAREST)
    if glw:
        g = Image.new('RGBA', (s.width * 2, s.height * 2), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([g.width // 4, g.height // 4, g.width * 3 // 4, g.height * 3 // 4], fill=c('#FFB040', 70)); g = g.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(g, (int(cx - g.width / 2), int(by - s.height * .6 - g.height / 2)))
    im.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height)))
def pill(im, text, x, y, col='#FF9A2E'):
    d = ImageDraw.Draw(im); w = d.textlength(text, font=F16) + 28; d.rounded_rectangle([x, y, x + w, y + 32], radius=16, fill=c('#1B1230', 235), outline=c(col), width=2); d.text((x + 14, y + 7), text, fill=c('#FFFFFF'), font=F16)
def box(im, x0, y0, x1, y1, fill='#1B1230', out='#4A3A6A'): ImageDraw.Draw(im).rounded_rectangle([x0, y0, x1, y1], radius=12, fill=c(fill, 245), outline=c(out), width=2)
def caption(im, t): d = ImageDraw.Draw(im); d.rectangle([0, 690, 390, 740], fill=c('#0B0716', 235)); d.text((14, 706), t, fill=c('#D9CFF0'), font=F16)
def bar(im, x, y, w, k, col='#FF9A2E', marks=()):
    d = ImageDraw.Draw(im); d.rounded_rectangle([x, y, x + w, y + 14], radius=7, fill=c('#2A2040')); d.rounded_rectangle([x, y, x + max(14, int(w * k)), y + 14], radius=7, fill=c(col))
    for m in marks: d.line([x + int(w * m), y - 3, x + int(w * m), y + 17], fill=c('#FFFFFF', 150), width=2)
MARKS = (.2, .45, .7)
S = []
# 1) 학교 앞마당에 자라는 호박 (단계 3: 꽃)
im = shot('campus'); paste_sprite(im, 3, 130, 470, 4); pill(im, '마법 호박 62%', 100, 62); box(im, 12, 560, 378, 600, fill='#1B1230'); ImageDraw.Draw(im).text((24, 571), '꽃이 피었어요! 곧 호박이 커져요', fill=c('#FFFFFF'), font=F16); caption(im, '① 학교 뒷마당에서 마법 호박이 자라요'); S.append(im)
# 2) 돌보기 화면
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '호박밭 같이 가꾸기', fill=c('#FFFFFF'), font=F16); d.text((390 - 12 - d.textlength('62%', font=F16), 17), '62%', fill=c('#FFC23A'), font=F16)
bg = shot('campus').crop((0, 140, 390, 380)).resize((390, 240)); im.alpha_composite(bg, (0, 52)); paste_sprite(im, 3, 195, 280, 4)
bar(im, 20, 330, 350, .62, marks=MARKS); d.text((20, 352), '반 전체 성장', fill=c('#D9CFF0'), font=F16); d.text((390 - 20 - d.textlength('372 / 600', font=F16), 352), '372 / 600', fill=c('#FFFFFF'), font=F16)
for i, (n, sub, col, cd) in enumerate((('물 주기', '+2 · 5분마다', '#6AB8FF', '바로 가능'), ('거름 주기', '+8 · 약초 1개 · 3번', '#8A6030', '2번 남음'), ('말 걸어 주기', '+3 · 10분마다', '#FF9AC8', '7분 뒤'))):
    y = 392 + i * 74; box(im, 14, y, 376, y + 64, fill='#2D2147'); d.ellipse([28, y + 14, 64, y + 50], fill=c(col, 220), outline=c('#FFFFFF', 120), width=2); d.text((78, y + 10), n, fill=c('#FFFFFF'), font=F16); d.text((78, y + 36), sub, fill=c('#9A90B8'), font=F16)
    d.rounded_rectangle([280, y + 16, 366, y + 48], radius=10, fill=c('#FF9A2E') if cd == '바로 가능' else c('#3A2E50')); d.text((290, y + 24), cd, fill=c('#2A1400') if cd == '바로 가능' else c('#8E86A8'), font=F16)
d.text((20, 620), '내가 키운 양: 36 · 오늘 한 일 11번', fill=c('#FFC23A'), font=F16); d.text((20, 646), '돌본 만큼 개인 보상이 늘어요', fill=c('#8E86A8'), font=F16); caption(im, '② 물 · 거름 · 말 걸기로 호박을 돌봐요'); S.append(im)
# 3) 단계가 오른 순간
im = shot('campus'); ov = Image.new('RGBA', (390, 740), c('#050414', 90)); im.alpha_composite(ov); paste_sprite(im, 4, 195, 430, 5, glw=True)
for _ in range(30):
    a = random.random() * 6.28; r = 70 + random.random() * 120; sp = Image.new('RGBA', (8, 8), (0, 0, 0, 0)); ImageDraw.Draw(sp).rectangle([2, 2, 5, 5], fill=c('#FFE9A0')); im.alpha_composite(sp, (int(195 + math.cos(a) * r), int(330 + math.sin(a) * r * .8)))
box(im, 12, 560, 378, 676, out='#FF9A2E'); d = ImageDraw.Draw(im); d.text((26, 574), '거대 호박이 활짝 자랐어요!', fill=c('#FFC23A'), font=F16); d.text((26, 604), '반 친구들 모두 고마워요, 호박이 웃어요.', fill=c('#FFFFFF'), font=F16); d.text((26, 634), '기숙사 앞에 호박이 하나씩 놓였어요', fill=c('#9A90B8'), font=F16); caption(im, '③ 다 자라면 거대 호박이 웃고, 기숙사에 호박이 놓여요'); S.append(im)
# 4) 5단계 그림
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '호박이 자라는 5단계', fill=c('#FFFFFF'), font=F16)
names = (('1 씨앗', '0%'), ('2 새싹', '20%'), ('3 덩굴', '45%'), ('4 꽃', '70%'), ('5 거대 호박', '100%'))
for k in range(5):
    x, y = (k % 2) * 195 + 6, 62 + (k // 2) * 208; box(im, x, y, x + 183, y + 198, fill='#2A2040'); s = ST[k].resize((144, 144), Image.NEAREST); im.alpha_composite(s, (x + 20, y + 8)); d.text((x + 12, y + 160), names[k][0], fill=c('#FFFFFF'), font=F16); d.text((x + 12, y + 180), '성장 ' + names[k][1] + ' 부터', fill=c('#9A90B8'), font=F16)
caption(im, '④ 호박이 자라는 모습 5단계 (도트 그림 시안)'); S.append(im)
# 5) 완성: 기숙사 앞 호박
im = shot('campus'); paste_sprite(im, 4, 130, 330, 4, glw=True)
for (nx, ny, col, nm) in ((300, 250, '#5CCB8E', '듀모른'), (300, 430, '#F08A3C', '엠버킬른'), (90, 520, '#E8709A', '더스크폴드'), (250, 600, '#7A66E0', '문할로우')):
    sp = ST[4].resize((96, 96), Image.NEAREST); im.alpha_composite(sp, (nx - 48, ny - 90)); d = ImageDraw.Draw(im); d.rounded_rectangle([nx - 40, ny + 2, nx + 40, ny + 24], radius=8, fill=c(col, 230)); d.text((nx - d.textlength(nm, font=F16) / 2, ny + 4), nm, fill=c('#FFFFFF'), font=F16)
caption(im, '⑤ 기숙사마다 호박 장식이 하나씩 놓여요'); S.append(im)
# 6) 보상과 관리자
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '보상과 관리자 화면', fill=c('#FFFFFF'), font=F16)
box(im, 12, 66, 378, 292); d.text((26, 78), '반 전체 단계 보상 (모두에게)', fill=c('#FFC23A'), font=F16)
for i, t in enumerate(('2단계 새싹  씨앗 2개', '3단계 덩굴  마나석 2개', '4단계 꽃  골드 200', '5단계 거대 호박  호박 장식 1점')): d.text((26, 112 + i * 30), t, fill=c('#D9CFF0'), font=F16)
d.text((26, 240), '내가 돌본 양에 따라 개인 보상도 받아요', fill=c('#9A90B8'), font=F16)
box(im, 12, 308, 378, 520, out='#F08A3C'); d.text((26, 320), '관리자 화면', fill=c('#F08A3C'), font=F16); d.text((26, 350), '성장 372/600 · 돌본 학생 14명', fill=c('#D9CFF0'), font=F16)
for k, t in enumerate(('이벤트 열기', '성장 속도 ×2', '처음으로', '이벤트 닫기')): x, y = 26 + (k % 2) * 172, 388 + (k // 2) * 44; d.rounded_rectangle([x, y, x + 160, y + 34], radius=8, fill=c('#2D2147'), outline=c('#4A3A6A')); d.text((x + 10, y + 8), t, fill=c('#FFFFFF'), font=F16)
caption(im, '⑥ 단계 보상 · 관리자 화면'); S.append(im)
sheet = Image.new('RGB', (390 * 3, 740 * 2))
for k, i in enumerate(S): sheet.paste(i.convert('RGB'), ((k % 3) * 390, (k // 3) * 740))
sheet.save(OUTD + '/ev5_sheet.png'); S[3].convert('RGB').save(OUTD + '/ev5_stages.png'); print('ok')
