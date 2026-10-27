# 이벤트 「호박밭 같이 가꾸기」 시안: 거대 호박 5단계 도트 + 실제 게임 화면 위에 얹은 장면 → out/ev5_sheet.png, out/ev5_stages.png
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH = sys.argv[1]; OUTD = os.path.dirname(os.path.abspath(__file__)) + '/out'
random.seed(5)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
FP = '/usr/share/fonts/opentype/unifont/unifont.otf'; F16 = ImageFont.truetype(FP, 16); F32 = ImageFont.truetype(FP, 32)
OUT = c('#1A0F1F')
def shot(n): return Image.open(f'{SH}/{n}.png').convert('RGBA').resize((390, 740), Image.LANCZOS)
# ---- 호박 5단계: 게임 속 호박과 같은 그림체(평평한 주황 + 검은 윤곽선 + 초록 꼭지, 잭 호박은 노란 얼굴) ----
ORA, ORAL, OUTL = c('#E07A1E'), c('#F09A3A'), c('#120A18'); STEM, GREEN, GREENL = c('#4A6A2A'), c('#4A6A2A'), c('#68923C'); YEL, YEL2 = c('#FFE07A'), c('#FFD04A'); SOIL, SOIL2 = c('#5C3C24'), c('#3E2818')
def stage(k):
    W_, H_ = (24, 14, 34, 46, 62)[k], (12, 20, 24, 36, 50)[k]; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def soil(cx, rx): d.ellipse([cx - rx, H_ - 8, cx + rx, H_ - 1], fill=SOIL, outline=OUTL); d.ellipse([cx - rx + 2, H_ - 6, cx + rx - 2, H_ - 3], fill=SOIL2)
    def leaf(cx, cy, w, h): d.ellipse([cx - w, cy - h, cx + w, cy + h], fill=GREEN, outline=OUTL); d.line([cx - w + 1, cy, cx + w - 1, cy], fill=GREENL)
    def vine(pts):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]): d.line([x0, y0, x1, y1], fill=GREEN, width=2)
    def pump(cx, cy, rx, ry, green=False, face=False):
        body = c('#9ABF4A') if green else ORA; mid = c('#B8D868') if green else ORAL
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=body, outline=OUTL)
        d.ellipse([cx - rx // 3, cy - ry + 2, cx + rx // 3, cy - 1], fill=mid)                                              # 꼭지 둘레 밝은 면
        d.rectangle([cx - 1, cy - ry - 3, cx + 1, cy - ry + 1], fill=STEM, outline=OUTL)
        if face:
            ex = max(5, rx // 3)
            for sgn in (-1, 1): d.polygon([(cx + sgn * ex - 5, cy + 2), (cx + sgn * ex + 5, cy + 2), (cx + sgn * ex, cy - 6)], fill=YEL, outline=None)
            d.rectangle([cx - rx // 2, cy + 6, cx + rx // 2, cy + 8], fill=YEL2); d.rectangle([cx - 1, cy - 2, cx + 1, cy + 1], fill=ORAL)
    if k == 0: soil(12, 11); d.ellipse([10, 1, 14, 5], fill=c('#D8B070'), outline=OUTL)
    elif k == 1: soil(7, 6); d.line([7, H_ - 8, 7, 6], fill=GREEN, width=2); leaf(3, 8, 3, 2); leaf(11, 6, 4, 2)
    elif k == 2: soil(17, 15); vine([(2, H_ - 6), (9, H_ - 11), (19, H_ - 9), (31, H_ - 12)]); leaf(7, H_ - 12, 4, 2); leaf(27, H_ - 14, 4, 2); pump(17, H_ - 9, 7, 5, green=True)
    elif k == 3:
        soil(23, 21); vine([(2, H_ - 6), (10, H_ - 12), (23, H_ - 9), (36, H_ - 14), (44, H_ - 8)]); leaf(7, H_ - 14, 5, 3); leaf(37, H_ - 17, 5, 3); leaf(16, H_ - 10, 4, 2); pump(23, H_ - 14, 13, 10)
        d.ellipse([34, 3, 41, 10], fill=YEL, outline=OUTL); d.ellipse([36, 5, 39, 8], fill=ORAL)
    else:
        soil(31, 29); vine([(2, H_ - 6), (10, H_ - 10)]); vine([(52, H_ - 10), (60, H_ - 6)]); leaf(6, H_ - 14, 5, 3); leaf(56, H_ - 14, 5, 3); leaf(14, H_ - 9, 4, 2); leaf(48, H_ - 9, 4, 2); pump(31, H_ - 21, 26, 19, face=True)
    return im
ST = [stage(k) for k in range(5)]
glow = lambda r, col, a: Image.new('RGBA', (r * 2, r * 2), (0, 0, 0, 0))
def paste_sprite(im, k, cx, by, scale, glw=False):
    s = ST[k].resize((ST[k].width * scale, ST[k].height * scale), Image.NEAREST)
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
im = shot('f1'); paste_sprite(im, 3, 175, 500, 2); pill(im, '마법 호박 62%', 100, 62); box(im, 12, 560, 378, 600, fill='#1B1230'); ImageDraw.Draw(im).text((24, 571), '꽃이 피었어요! 곧 호박이 커져요', fill=c('#FFFFFF'), font=F16); caption(im, '① 호박밭 한가운데에서 마법 호박이 자라요'); S.append(im)
# 2) 돌보기 화면
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '호박밭 같이 가꾸기', fill=c('#FFFFFF'), font=F16); d.text((390 - 12 - d.textlength('62%', font=F16), 17), '62%', fill=c('#FFC23A'), font=F16)
bg = shot('f1').crop((60, 330, 390, 570)).resize((390, 283), Image.LANCZOS).crop((0, 0, 390, 240)); im.alpha_composite(bg, (0, 52)); paste_sprite(im, 3, 150, 290, 2)
bar(im, 20, 330, 350, .62, marks=MARKS); d.text((20, 352), '반 전체 성장', fill=c('#D9CFF0'), font=F16); d.text((390 - 20 - d.textlength('372 / 600', font=F16), 352), '372 / 600', fill=c('#FFFFFF'), font=F16)
for i, (n, sub, col, cd) in enumerate((('물 주기', '+2 · 5분마다', '#6AB8FF', '바로 가능'), ('거름 주기', '+8 · 약초 1개 · 3번', '#8A6030', '2번 남음'), ('말 걸어 주기', '+3 · 10분마다', '#FF9AC8', '7분 뒤'))):
    y = 392 + i * 74; box(im, 14, y, 376, y + 64, fill='#2D2147'); d.ellipse([28, y + 14, 64, y + 50], fill=c(col, 220), outline=c('#FFFFFF', 120), width=2); d.text((78, y + 10), n, fill=c('#FFFFFF'), font=F16); d.text((78, y + 36), sub, fill=c('#9A90B8'), font=F16)
    d.rounded_rectangle([280, y + 16, 366, y + 48], radius=10, fill=c('#FF9A2E') if cd == '바로 가능' else c('#3A2E50')); d.text((290, y + 24), cd, fill=c('#2A1400') if cd == '바로 가능' else c('#8E86A8'), font=F16)
d.text((20, 620), '내가 키운 양: 36 · 오늘 한 일 11번', fill=c('#FFC23A'), font=F16); d.text((20, 646), '돌본 만큼 개인 보상이 늘어요', fill=c('#8E86A8'), font=F16); caption(im, '② 물 · 거름 · 말 걸기로 호박을 돌봐요'); S.append(im)
# 3) 단계가 오른 순간
im = shot('f1'); ov = Image.new('RGBA', (390, 740), c('#050414', 70)); im.alpha_composite(ov); paste_sprite(im, 4, 175, 470, 2, glw=True)
for _ in range(30):
    a = random.random() * 6.28; r = 50 + random.random() * 110; sp = Image.new('RGBA', (8, 8), (0, 0, 0, 0)); ImageDraw.Draw(sp).rectangle([2, 2, 5, 5], fill=c('#FFE9A0')); im.alpha_composite(sp, (int(175 + math.cos(a) * r), int(410 + math.sin(a) * r * .8)))
box(im, 12, 560, 378, 676, out='#FF9A2E'); d = ImageDraw.Draw(im); d.text((26, 574), '거대 호박이 활짝 자랐어요!', fill=c('#FFC23A'), font=F16); d.text((26, 604), '반 친구들 모두 고마워요, 호박이 웃어요.', fill=c('#FFFFFF'), font=F16); d.text((26, 634), '기숙사 앞에 호박이 하나씩 놓였어요', fill=c('#9A90B8'), font=F16); caption(im, '③ 다 자라면 거대 호박이 웃고, 기숙사에 호박이 놓여요'); S.append(im)
# 4) 5단계 그림
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '호박이 자라는 5단계', fill=c('#FFFFFF'), font=F16)
names = (('1 씨앗', '0%'), ('2 새싹', '20%'), ('3 덩굴', '45%'), ('4 꽃', '70%'), ('5 거대 호박', '100%'))
for k in range(5):
    x, y = (k % 2) * 195 + 6, 62 + (k // 2) * 208; box(im, x, y, x + 183, y + 198, fill='#2A2040'); s = ST[k]; sc = max(1, min(4, 140 // max(s.width, s.height))); s = s.resize((s.width * sc, s.height * sc), Image.NEAREST); im.alpha_composite(s, (x + (183 - s.width) // 2, y + 140 - s.height)); d.text((x + 12, y + 160), names[k][0], fill=c('#FFFFFF'), font=F16); d.text((x + 12, y + 180), '성장 ' + names[k][1] + ' 부터', fill=c('#9A90B8'), font=F16)
caption(im, '④ 호박이 자라는 모습 5단계 (도트 그림 시안)'); S.append(im)
# 5) 완성: 기숙사 앞 호박
im = shot('campus'); paste_sprite(im, 4, 120, 340, 1, glw=True)
for (nx, ny, col, nm) in ((300, 250, '#5CCB8E', '듀모른'), (300, 430, '#F08A3C', '엠버킬른'), (90, 520, '#E8709A', '더스크폴드'), (250, 600, '#7A66E0', '문할로우')):
    sp = ST[4].resize((ST[4].width * 2 // 3, ST[4].height * 2 // 3), Image.NEAREST); im.alpha_composite(sp, (nx - sp.width // 2, ny - sp.height)); d = ImageDraw.Draw(im); d.rounded_rectangle([nx - 40, ny + 2, nx + 40, ny + 24], radius=8, fill=c(col, 230)); d.text((nx - d.textlength(nm, font=F16) / 2, ny + 4), nm, fill=c('#FFFFFF'), font=F16)
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
