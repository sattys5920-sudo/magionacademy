# 이벤트 3 「호박 축제 대결」 미니게임 시안 → out/ev3_*.png (폰 화면 390×740)
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(3)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
FP = '/usr/share/fonts/opentype/unifont/unifont.otf'
F16, F32 = ImageFont.truetype(FP, 16), ImageFont.truetype(FP, 32)
HOUSE = [('듀모른', '#5CCB8E'), ('엠버킬른', '#F08A3C'), ('더스크폴드', '#E8709A'), ('문할로우', '#7A66E0')]
BG, PANEL = c('#140E22'), c('#1B1230')
def screen(title, sub=None):
    im = Image.new('RGBA', (390, 740), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 390, 52], fill=PANEL); d.text((12, 17), title, fill=c('#FFFFFF'), font=F16)
    if sub: d.text((390 - 12 - d.textlength(sub, font=F16), 17), sub, fill=c('#FFC23A'), font=F16)
    return im, d
def art(im, fn, h=110, y=52):                       # 도트 그림 영역: 130×h 칸을 3배로
    a = Image.new('RGBA', (130, h), c('#0A0618')); ad = ImageDraw.Draw(a); fn(a, ad); im.alpha_composite(a.resize((390, h * 3), Image.NEAREST), (0, y))
def txt(d, x, y, s, f=F16, col='#D9CFF0'): d.text((x, y), s, fill=c(col), font=f)
def box(d, x0, y0, x1, y1, fill='#2D2147', out='#4A3A6A', r=10): d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=c(fill), outline=c(out), width=2)
def stars(ad, n=40, hmax=60):
    for _ in range(n): ad.point((random.randrange(130), random.randrange(hmax)), fill=c('#CFCFF0') if random.random() < .5 else c('#8E8EC0'))
def pumpkin(ad, cx, cy, rx, ry, face=True, glow=False):
    if glow: ad.ellipse([cx - rx - 6, cy - ry - 6, cx + rx + 6, cy + ry + 6], fill=c('#FF9A2E', 40))
    ad.rectangle([cx - 2, cy - ry - 5, cx + 2, cy - ry + 1], fill=c('#5A8A2E'))
    for k, col in ((-1, '#E26A10'), (1, '#E26A10'), (0, '#F08A1C')):
        ad.ellipse([cx - rx + k * rx * .42 - (0 if k == 0 else 0), cy - ry, cx + rx + k * rx * .42 - rx * .5, cy + ry], fill=c(col), outline=c('#7A3A08'))
    ad.ellipse([cx - rx * .55, cy - ry, cx + rx * .55, cy + ry], fill=c('#F59A28'), outline=c('#7A3A08'))
HW = 130
# ---- 1) 점수판 ----
def s_board():
    im, d = screen('호박 축제 대결', '2 / 4 라운드')
    def f(a, ad):
        stars(ad); 
        for i in range(8): ad.rectangle([i * 17 + 2, 60 + (i % 3) * 3, i * 17 + 12, 66], fill=c('#2A2040'))
        pumpkin(ad, 22, 40, 11, 9, glow=True); pumpkin(ad, 108, 44, 9, 7, glow=True)
        ad.rectangle([40, 30, 90, 50], fill=c('#3A1E10')); ad.polygon([(36, 30), (65, 12), (94, 30)], fill=c('#4A2A18')); ad.rectangle([58, 36, 72, 50], fill=c('#FFC23A'))
    art(im, f, 80)
    y0 = 52 + 240 + 14; txt(d, 14, y0, '기숙사 점수 (한 사람 평균으로 겨뤄요)', col='#FFC23A')
    sc = [38, 51, 44, 29]; mx = 60
    for i, (n, col) in enumerate(HOUSE):
        y = y0 + 34 + i * 62; txt(d, 14, y, n, col=col); d.rounded_rectangle([14, y + 22, 376, y + 40], radius=6, fill=c('#2A2040'))
        d.rounded_rectangle([14, y + 22, 14 + int(362 * sc[i] / mx), y + 40], radius=6, fill=c(col)); txt(d, 340, y, str(sc[i]), col='#FFFFFF')
    yy = y0 + 34 + 4 * 62 + 4
    box(d, 12, yy, 378, yy + 112, fill='#1B1230')
    for k, (nm, st) in enumerate((('호박 조각하기', '끝'), ('사탕 던지기', '끝'), ('귀신의 집 탈출', '진행 중'), ('유령 뿅망치', '대기'))):
        txt(d, 24, yy + 10 + k * 24, f'{k + 1}. {nm}', col='#D9CFF0'); txt(d, 300, yy + 10 + k * 24, st, col='#6FD08C' if st == '끝' else '#FFC23A' if st == '진행 중' else '#8E86A8')
    return im
# ---- 2) 호박 조각하기 ----
def s_carve():
    im, d = screen('호박 조각하기', '남은 시간 18초')
    def f(a, ad):
        ad.rectangle([0, 0, 130, 130], fill=c('#120C24')); stars(ad, 30, 40)
        pumpkin(ad, 65, 62, 44, 36, glow=True)
        pts = [(46, 52), (52, 44), (58, 52)]; pts2 = [(72, 52), (78, 44), (84, 52)]
        for p in (pts, pts2):
            for (x0, y0), (x1, y1) in zip(p + [p[0]], p[1:] + [p[0]]):
                n = int(math.hypot(x1 - x0, y1 - y0)); 
                for i in range(n + 1):
                    t = i / max(1, n); X, Y = int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)
                    ad.point((X, Y), fill=c('#FFF2A0') if i % 2 == 0 else c('#7A3A08'))
        mouth = [(44, 72), (50, 78), (56, 72), (62, 78), (68, 72), (74, 78), (80, 72), (86, 78)]
        for k, ((x0, y0), (x1, y1)) in enumerate(zip(mouth, mouth[1:])):
            n = int(math.hypot(x1 - x0, y1 - y0))
            for i in range(n + 1):
                t = i / max(1, n); X, Y = int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)
                ad.point((X, Y), fill=c('#3A1A00') if k < 4 else (c('#FFF2A0') if i % 2 == 0 else c('#7A3A08')))
        for p in (pts, pts2):                       # 이미 잘라 낸 눈
            ad.polygon(p, fill=c('#2A1000'), outline=c('#FFC23A'))
        ad.line([73, 92, 63, 82], fill=c('#C8D0DC'), width=2); ad.line([74, 93, 77, 96], fill=c('#6B4A2A'), width=2)   # 칼
    art(im, f, 110)
    y = 52 + 330 + 14
    box(d, 12, y, 378, y + 150, fill='#1B1230'); txt(d, 24, y + 12, '점선을 손가락으로 따라 그어요', col='#FFFFFF'); txt(d, 24, y + 36, '선에서 벗어나면 감점 · 빨리 끝내면 보너스', col='#9A90B8')
    d.rounded_rectangle([24, y + 74, 366, y + 92], radius=6, fill=c('#2A2040')); d.rounded_rectangle([24, y + 74, 24 + int(342 * .62), y + 92], radius=6, fill=c('#FF9A2E')); txt(d, 24, y + 100, '완성 62%'); txt(d, 250, y + 100, '정확도 94%', col='#6FD08C')
    txt(d, 24, y + 124, '점수 = 정확도 × 60 + 남은 시간 × 2', col='#8E86A8')
    return im
# ---- 3) 사탕 던지기 ----
def s_candy():
    im, d = screen('사탕 던지기', '남은 사탕 7 / 10')
    def f(a, ad):
        ad.rectangle([0, 0, 130, 130], fill=c('#120C24')); stars(ad, 30, 50)
        for i, (x, pts, col) in enumerate(((28, 1, '#8CE6B0'), (65, 5, '#FF6A8A'), (102, 3, '#FFD866'))):
            ad.rectangle([x - 14, 20, x + 14, 22], fill=c('#6B4A2A')); pumpkin(ad, x, 36, 12, 10); ad.ellipse([x - 7, 33, x + 7, 41], fill=c('#2A1000'))  # 바구니 구멍
            ad.text((x - 3, 54), str(pts), fill=c(col))
        ad.line([65, 22, 65, 6], fill=c('#6B4A2A')); ad.line([28, 22, 28, 12], fill=c('#6B4A2A')); ad.line([102, 22, 102, 8], fill=c('#6B4A2A'))
        for k in range(6): ad.ellipse([60 + k * 2, 100 - k * 12, 67 + k * 2, 107 - k * 12], outline=c('#FFFFFF', 60))   # 던지는 궤적
        ad.ellipse([60, 100, 70, 110], fill=c('#FF6AA8'), outline=c('#FFFFFF')); ad.polygon([(60, 105), (54, 100), (54, 110)], fill=c('#FF6AA8')); ad.polygon([(70, 105), (76, 100), (76, 110)], fill=c('#FF6AA8'))
        for x in (14, 24, 100, 110, 118): ad.ellipse([x, 108, x + 6, 114], fill=c(random.choice(['#6AB8FF', '#FFD866', '#8CE6B0'])))
    art(im, f, 110)
    y = 52 + 330 + 14; box(d, 12, y, 378, y + 150, fill='#1B1230')
    txt(d, 24, y + 12, '사탕을 위로 밀어 던져요', col='#FFFFFF'); txt(d, 24, y + 36, '가운데 5점 · 양끝 1점 · 바구니는 움직여요', col='#9A90B8')
    txt(d, 24, y + 70, '지금 점수 21점', col='#FFC23A'); txt(d, 24, y + 96, '연속으로 넣으면 콤보 +1', col='#8E86A8'); txt(d, 24, y + 120, '시간 40초 · 사탕 10개', col='#8E86A8')
    return im
# ---- 4) 귀신의 집 탈출 (기숙사 팀) ----
def s_escape():
    im, d = screen('귀신의 집 탈출 · 엠버킬른 팀', '남은 시간 2:10')
    def f(a, ad):
        ad.rectangle([0, 0, 130, 130], fill=c('#0E0A1E'))
        ad.rectangle([0, 62, 130, 110], fill=c('#2A1E34')); 
        for i in range(0, 130, 10): ad.line([i, 62, i + 6, 110], fill=c('#1E1628'))
        ad.rectangle([40, 14, 90, 70], fill=c('#4A2E22'), outline=c('#120A18')); ad.rectangle([46, 20, 84, 70], fill=c('#6A4230'), outline=c('#120A18')); ad.ellipse([76, 44, 80, 48], fill=c('#E8B83A'))
        ad.rectangle([55, 30, 75, 42], fill=c('#1A1A28'), outline=c('#8E86A8'))
        for i in range(4): ad.rectangle([57 + i * 5, 33, 60 + i * 5, 39], fill=c('#6FF0D8') if i < 2 else c('#2A2A3A'))
        ad.ellipse([8, 20, 28, 48], fill=c('#EDEBFF', 150)); ad.ellipse([12, 28, 16, 33], fill=c('#120A18')); ad.ellipse([20, 28, 24, 33], fill=c('#120A18')); ad.ellipse([14, 38, 22, 44], fill=c('#120A18'))   # 유령
        ad.rectangle([100, 30, 122, 60], fill=c('#3A2A18'), outline=c('#120A18')); ad.ellipse([104, 34, 118, 56], fill=c('#241810'))                                          # 그림 액자
        ad.polygon([(10, 80), (20, 96), (6, 96)], fill=c('#8A5AE0'))
    art(im, f, 110)
    y = 52 + 330 + 8
    box(d, 12, y, 378, y + 74, fill='#3A2A18', out='#FFC23A'); txt(d, 24, y + 8, '나만 보이는 단서 (팀원은 못 봐요)', col='#FFC23A'); txt(d, 24, y + 34, '“박쥐는 모두 세 마리였다.”', col='#FFFFFF', f=F16)
    txt(d, 14, y + 90, '자물쇠: 3 ? ? ?   (팀원이 말로 맞춰 봐요)', col='#FFFFFF')
    yy = y + 118
    for i, (nm, st) in enumerate((('하나', '단서 확인'), ('지우', '단서 확인'), ('도윤', '읽는 중'), ('서연', '단서 확인'), ('나', '단서 확인'))):
        x = 14 + (i % 3) * 124; yb = yy + (i // 3) * 38; box(d, x, yb, x + 116, yb + 32, fill='#1B1230', r=8); txt(d, x + 8, yb + 8, nm + ' ' + ('●' if st != '읽는 중' else '○'), col='#6FD08C' if st != '읽는 중' else '#8E86A8')
    box(d, 12, yy + 84, 378, yy + 128, fill='#1B1230'); txt(d, 24, yy + 98, '번호를 입력해요 [  3  ][  ?  ][  ?  ][  ?  ]', col='#D9CFF0')
    txt(d, 14, yy + 138, '방 3개를 열면 끝 · 빠를수록 높은 점수', col='#8E86A8')
    return im
# ---- 5) 유령 뿅망치 (이미 있는 놀이) ----
def s_whack():
    im, d = screen('유령 뿅망치', '남은 시간 22초')
    def f(a, ad):
        ad.rectangle([0, 0, 130, 130], fill=c('#0F0B20')); stars(ad, 24, 22)
        for r in range(3):
            for q in range(3):
                x, y = 24 + q * 40, 34 + r * 28
                ad.ellipse([x - 12, y + 6, x + 12, y + 14], fill=c('#2A2038')); ad.rectangle([x - 8, y - 2, x + 8, y + 10], fill=c('#5A5870'), outline=c('#120A18'))
                if (r, q) in ((0, 1), (1, 2), (2, 0)): ad.ellipse([x - 8, y - 14, x + 8, y + 4], fill=c('#EDEBFF')); ad.ellipse([x - 4, y - 8, x - 1, y - 4], fill=c('#120A18')); ad.ellipse([x + 1, y - 8, x + 4, y - 4], fill=c('#120A18'))
                if (r, q) == (1, 0): ad.polygon([(x - 8, y - 4), (x, y - 14), (x + 8, y - 4)], fill=c('#3A2A60'))
    art(im, f, 110)
    y = 52 + 330 + 14; box(d, 12, y, 378, y + 150, fill='#1B1230'); txt(d, 24, y + 12, '올라온 유령을 눌러요', col='#FFFFFF'); txt(d, 24, y + 36, '유령 +3점 · 박쥐는 -1점과 기절', col='#9A90B8'); txt(d, 24, y + 76, '지금 점수 27점', col='#FFC23A')
    txt(d, 24, y + 110, '이미 있는 놀이를 그대로 써요', col='#8E86A8')
    return im
# ---- 6) 시상 ----
def s_win():
    im, d = screen('호박 축제 시상식')
    def f(a, ad):
        ad.rectangle([0, 0, 130, 130], fill=c('#120C28')); stars(ad, 40, 70)
        for i, (x, h, col) in enumerate(((22, 20, '#E8709A'), (65, 34, '#F08A3C'), (108, 12, '#7A66E0'))):
            ad.rectangle([x - 16, 100 - h, x + 16, 100], fill=c('#3A2E4A'), outline=c('#120A18')); ad.rectangle([x - 14, 100 - h - 22, x + 14, 100 - h], fill=c(col), outline=c('#120A18'))
        pumpkin(ad, 65, 40, 10, 8, glow=True); ad.polygon([(58, 30), (60, 24), (63, 29), (65, 22), (67, 29), (70, 24), (72, 30)], fill=c('#FFD866'))
        for _ in range(26): ad.ellipse([(x := random.randrange(130)), (y := random.randrange(70)), x + 3, y + 3], fill=c(random.choice(['#FF6AA8', '#FFD866', '#6AB8FF', '#8CE6B0'])))
    art(im, f, 110)
    y = 52 + 330 + 16; txt(d, 14, y, '우승 · 엠버킬른', f=F32, col='#F08A3C'); txt(d, 14, y + 46, '평균 점수 51점', col='#FFC23A')
    box(d, 12, y + 82, 378, y + 262, fill='#1B1230')
    for i, (n, col) in enumerate((('1등 엠버킬른', '#F08A3C'), ('2등 더스크폴드', '#E8709A'), ('3등 듀모른', '#5CCB8E'), ('4등 문할로우', '#7A66E0'))): txt(d, 24, y + 94 + i * 24, n, col=col)
    txt(d, 24, y + 196, '보상: 모두 사탕 5개 · 우승 기숙사 칭호', col='#FFFFFF'); txt(d, 24, y + 220, '우승 기숙사는 호박 장식 한 점 더', col='#9A90B8')
    return im
S = [s_board(), s_carve(), s_candy(), s_escape(), s_whack(), s_win()]
names = ['board', 'carve', 'candy', 'escape', 'whack', 'win']
for n, im in zip(names, S): im.convert('RGB').save(f'out/ev3_{n}.png')
sheet = Image.new('RGB', (390 * 3, 740 * 2), (0, 0, 0))
for k, im in enumerate(S): sheet.paste(im.convert('RGB'), ((k % 3) * 390, (k // 3) * 740))
sheet.save('out/ev3_sheet.png'); print('ok')
