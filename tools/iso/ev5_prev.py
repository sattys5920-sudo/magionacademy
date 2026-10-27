# 이벤트 「호박밭 같이 가꾸기」 시안: 게임 호박과 같은 도트 그림체로 5단계를 새로 찍고, 실제 호박밭 화면(2배 해상도) 위에 도트 칸 그대로 얹어요 → out/ev5_sheet.png, out/ev5_stages.png
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH = sys.argv[1]; OUTD = os.path.dirname(os.path.abspath(__file__)) + '/out'
random.seed(5)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
FP = '/usr/share/fonts/opentype/unifont/unifont.otf'; F16 = ImageFont.truetype(FP, 16)
# 게임 속 호박에서 뽑은 색
OUTL, ORA, ORAL, ORAD = c('#120A18'), c('#E07A1E'), c('#F09A3A'), c('#B85A14'); STEM, GRN, GRNL = c('#4A6A2A'), c('#4A6A2A'), c('#68923C'); YEL, YEL2 = c('#FFE07A'), c('#FFD04A'); SOIL, SOIL2 = c('#5C3C24'), c('#3E2818')
def mask(w, h, cx, cy, rx, ry):   # 정수 칸 타원 (좌우 대칭)
    return {(x, y) for y in range(h) for x in range(w) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
def ell(P, w, h, cx, cy, rx, ry, fill, outline=OUTL, shade=None, rib=None, hi=None):
    outer = mask(w, h, cx, cy, rx + .9, ry + .9); inner = mask(w, h, cx, cy, rx - .1, ry - .1)
    for p in outer - inner: P[p] = outline
    for (x, y) in inner:
        col = fill
        if shade and ((x + .5 - cx) / rx) * .6 + ((y + .5 - cy) / ry) * .8 > shade: col = ORAD if fill == ORA else fill
        P[(x, y)] = col
    if rib:
        for dx in rib:
            for (x, y) in inner:
                if abs((x - cx) - dx) < .5 and abs(y + .5 - cy) < ry * (1 - abs(dx) / (rx * 1.35)) * .92: P[(x, y)] = ORAD if fill == ORA else fill
    if hi:
        for (x, y) in hi: P[(x, y)] = ORAL
def stage(k):
    W_, H_ = (22, 14, 32, 44, 56)[k], (10, 16, 22, 34, 46)[k]; P = {}
    def rect(x0, y0, x1, y1, col):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < W_ and 0 <= y < H_: P[(x, y)] = col
    def soil(cx, rx):
        ell(P, W_, H_, cx, H_ - 4, rx, 3.2, SOIL); 
        for x in range(cx - rx + 3, cx + rx - 2, 3): P[(x, H_ - 4)] = SOIL2
    def leaf(cx, cy, rx, ry): ell(P, W_, H_, cx, cy, rx, ry, GRN); [P.__setitem__((x, cy), GRNL) for x in range(int(cx - rx + 2), int(cx + rx - 1)) if (x, cy) in P]
    def vine(pts):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            for i in range(n + 1):
                x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
                for dy in (0, 1): P[(x, y + dy)] = GRN if dy == 0 else GRNL
    def pump(cx, cy, rx, ry, green=False, face=False):
        base = c('#9ABF4A') if green else ORA
        ell(P, W_, H_, cx, cy, rx, ry, base, shade=.55, rib=None if green else (-int(rx * .5), 0, int(rx * .5)), hi=[(cx - rx // 2 - 1 + i, cy - ry // 2 + j) for i in range(2) for j in range(2)] if not green else None)
        for i in range(-rx // 3, rx // 3 + 1): P[(cx + i, cy - ry + 1)] = ORAL if not green else c('#B8D868')            # 꼭지 둘레 밝은 면
        rect(cx - 1, cy - ry - 3, cx + 1, cy - ry, STEM); P[(cx - 2, cy - ry - 3)] = OUTL; P[(cx + 2, cy - ry - 3)] = OUTL
        if face:                                                              # 잭 호박 얼굴: 파낸 구멍(어두운 테두리)에 노란 불빛이 차 있어요
            fy = cy - 3
            RIM, CORE = c('#7A3608'), c('#FFF4B8')
            def hole(cells, col=YEL, core=()):
                cs = set(cells)
                for (x, y) in cs:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        if (x + dx, y + dy) not in cs and (x + dx, y + dy) not in P.get('holes', ()): P[(x + dx, y + dy)] = RIM
                for p in cs: P[p] = col
                for p in core: P[p] = CORE
            ex, ey = cx - 0, fy - 6
            for sgn in (-1, 1):                                               # 눈: 위로 뾰족한 삼각형 + 한가운데 밝은 심
                x0 = cx + sgn * 8; cells = [(x0 + dx, ey + r_) for r_, hw in enumerate((0, 1, 2, 3, 4)) for dx in range(-hw, hw + 1)]
                hole(cells, YEL, [(x0, ey + 3), (x0 - 1, ey + 3), (x0 + 1, ey + 3), (x0, ey + 2)])
            hole([(cx + dx, fy + 1 + r_) for r_, hw in enumerate((0, 1)) for dx in range(-hw, hw + 1)], YEL2)    # 코: 작은 삼각형
            mouth = []
            for dx in range(-12, 13):                                         # 입: 활짝 웃는 곡선(가운데가 아래로, 양끝이 위로)
                yy = fy + 6 + int(5 * (1 - (dx / 12.5) ** 2) + .5)
                for t_ in range(3): mouth.append((cx + dx, yy + t_))
            hole(mouth, YEL2)
            for x_ in (cx - 6, cx - 5, cx + 5, cx + 6):                       # 이빨 두 개: 입 위쪽에 주황 칸을 남겨요
                top = min(q[1] for q in mouth if q[0] == x_)
                for t_ in range(2): P[(x_, top + t_)] = ORA
                P[(x_, top + 2)] = ORA if t_ else P[(x_, top + 2)]
    if k == 0: soil(11, 10); rect(9, 1, 12, 4, c('#D8B070')); [P.__setitem__(p, OUTL) for p in ((8, 2), (8, 3), (13, 2), (13, 3), (9, 0), (10, 0), (11, 0), (12, 0), (9, 5), (10, 5), (11, 5), (12, 5))]
    elif k == 1: soil(7, 6); rect(7, 5, 7, 11, GRN); rect(6, 5, 6, 11, GRNL); leaf(3, 6, 3, 2); leaf(11, 4, 3.5, 2)
    elif k == 2: soil(15, 13); vine([(1, H_ - 7), (7, H_ - 10), (16, H_ - 9), (28, H_ - 12)]); leaf(5, H_ - 11, 4, 2.3); leaf(26, H_ - 14, 4, 2.3); pump(15, H_ - 8, 6, 5, green=True)
    elif k == 3:
        soil(21, 19); vine([(1, H_ - 6), (8, H_ - 10), (21, H_ - 8), (34, H_ - 12), (42, H_ - 8)]); leaf(5, H_ - 13, 4.5, 2.6); leaf(34, H_ - 16, 4.5, 2.6); leaf(13, H_ - 9, 3.5, 2); pump(21, H_ - 12, 11, 9)
        ell(P, W_, H_, 36, 4, 3, 3, YEL); rect(35, 3, 36, 4, ORAL)
    else:
        soil(27, 26); vine([(1, H_ - 6), (8, H_ - 9)]); vine([(47, H_ - 9), (54, H_ - 6)]); leaf(5, H_ - 13, 4.5, 2.6); leaf(50, H_ - 13, 4.5, 2.6); leaf(12, H_ - 8, 3.5, 2); leaf(43, H_ - 8, 3.5, 2); pump(27, H_ - 19, 22, 17, face=True)
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); px = im.load()
    for (x, y), col in P.items():
        if 0 <= x < W_ and 0 <= y < H_: px[x, y] = col
    return im
ST = [stage(k) for k in range(5)]
CELL_W, CELL_H = 60, 50   # 게임용 시트: 5단계를 60×50 칸에 아래 가운데 정렬로 한 줄
_sheet = Image.new('RGBA', (CELL_W * 5, CELL_H), (0, 0, 0, 0))
for _k, _s in enumerate(ST): _sheet.alpha_composite(_s, (_k * CELL_W + (CELL_W - _s.width) // 2, CELL_H - _s.height))
_sheet.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public/art/ev5_pumpkin.png'))
def shot(n): return Image.open(f'{SH}/{n}.png').convert('RGBA')            # 780×1480 (게임 화면 2배)
def spr(base, k, cx, by, scale, glow=False):   # 좌표는 390×740 기준, 도트 한 칸 = scale×2 화면 칸
    s = ST[k].resize((ST[k].width * scale * 2, ST[k].height * scale * 2), Image.NEAREST); cx *= 2; by *= 2
    if glow:
        g = Image.new('RGBA', (s.width * 2, s.height * 2), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([g.width // 4, g.height // 4, g.width * 3 // 4, g.height * 3 // 4], fill=c('#FFB040', 70)); g = g.filter(ImageFilter.GaussianBlur(20)); base.alpha_composite(g, (int(cx - g.width / 2), int(by - s.height * .6 - g.height / 2)))
    base.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height)))
class UI:   # 390×740 기준으로 그리고 2배 도트로 키워서 얹어요
    def __init__(self, base=None): self.base = base or Image.new('RGBA', (780, 1480), c('#140E22')); self.l = Image.new('RGBA', (390, 740), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.l); self.post = []
    def text(self, xy, t, col='#FFFFFF'): self.d.text(xy, t, fill=c(col), font=F16)
    def box(self, x0, y0, x1, y1, fill='#1B1230', out='#4A3A6A'): self.d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=c(fill, 245), outline=c(out), width=2)
    def pill(self, t, x, y, col='#FF9A2E'): w = self.d.textlength(t, font=F16) + 28; self.d.rounded_rectangle([x, y, x + w, y + 32], radius=16, fill=c('#1B1230', 235), outline=c(col), width=2); self.text((x + 14, y + 7), t)
    def head(self, t, right=None):
        self.d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); self.text((12, 17), t)
        if right: self.text((390 - 12 - self.d.textlength(right, font=F16), 17), right, '#FFC23A')
    def bar(self, x, y, w, k, marks=()):
        self.d.rounded_rectangle([x, y, x + w, y + 14], radius=7, fill=c('#2A2040')); self.d.rounded_rectangle([x, y, x + max(14, int(w * k)), y + 14], radius=7, fill=c('#FF9A2E'))
        for m in marks: self.d.line([x + int(w * m), y - 3, x + int(w * m), y + 17], fill=c('#FFFFFF', 150), width=2)
    def cap(self, t): self.d.rectangle([0, 690, 390, 740], fill=c('#0B0716', 235)); self.text((14, 706), t, '#D9CFF0')
    def done(self):
        out = self.base.copy(); out.alpha_composite(self.l.resize((780, 1480), Image.NEAREST))
        for im, pos in self.post: out.alpha_composite(im, pos)
        return out
MARKS = (.2, .45, .7); S = []
# 1) 호박밭에서 자라는 호박
u = UI(shot('f1')); spr(u.base, 3, 175, 500, 2); u.pill('마법 호박 62%', 100, 62); u.box(12, 560, 378, 600); u.text((24, 571), '꽃이 피었어요! 곧 호박이 커져요'); u.cap('① 호박밭 한가운데에서 마법 호박이 자라요'); S.append(u.done())
# 2) 돌보기
u = UI(); u.head('호박밭 같이 가꾸기', '62%'); bg = shot('f1').crop((100, 640, 780, 1130)); u.base.alpha_composite(bg.resize((780, 562), Image.LANCZOS).crop((0, 0, 780, 480)), (0, 104)); spr(u.base, 3, 150, 290, 1)
u.bar(20, 330, 350, .62, MARKS); u.text((20, 352), '반 전체 성장', '#D9CFF0'); u.text((390 - 20 - u.d.textlength('372 / 600', font=F16), 352), '372 / 600')
for i, (n, sub, col, cd) in enumerate((('물 주기', '+2 · 5분마다', '#6AB8FF', '바로 가능'), ('거름 주기', '+8 · 약초 1개 · 3번', '#8A6030', '2번 남음'), ('말 걸어 주기', '+3 · 10분마다', '#FF9AC8', '7분 뒤'))):
    y = 392 + i * 74; u.box(14, y, 376, y + 64, fill='#2D2147'); u.d.ellipse([28, y + 14, 64, y + 50], fill=c(col, 220), outline=c('#FFFFFF', 120), width=2); u.text((78, y + 10), n); u.text((78, y + 36), sub, '#9A90B8')
    u.d.rounded_rectangle([280, y + 16, 366, y + 48], radius=10, fill=c('#FF9A2E') if cd == '바로 가능' else c('#3A2E50')); u.text((290, y + 24), cd, '#2A1400' if cd == '바로 가능' else '#8E86A8')
u.text((20, 620), '내가 키운 양: 36 · 오늘 한 일 11번', '#FFC23A'); u.text((20, 646), '돌본 만큼 개인 보상이 늘어요', '#8E86A8'); u.cap('② 물 · 거름 · 말 걸기로 호박을 돌봐요'); S.append(u.done())
# 3) 다 자란 순간
u = UI(shot('f1')); u.base.alpha_composite(Image.new('RGBA', (780, 1480), c('#050414', 70))); spr(u.base, 4, 175, 480, 2, glow=True)
for _ in range(30):
    a = random.random() * 6.28; r = 60 + random.random() * 130; sp = Image.new('RGBA', (8, 8), c('#FFE9A0')); u.base.alpha_composite(sp, (int(350 + math.cos(a) * r * 1.4), int(740 + math.sin(a) * r * 1.1)))
u.box(12, 560, 378, 676, out='#FF9A2E'); u.text((26, 574), '거대 호박이 활짝 자랐어요!', '#FFC23A'); u.text((26, 604), '반 친구들 모두 고마워요, 호박이 웃어요.'); u.text((26, 634), '기숙사 앞에 호박이 하나씩 놓였어요', '#9A90B8'); u.cap('③ 다 자라면 거대 호박이 웃고, 기숙사에 호박이 놓여요'); S.append(u.done())
# 4) 5단계
u = UI(); u.head('호박이 자라는 5단계'); names = (('1 씨앗', '0%'), ('2 새싹', '20%'), ('3 덩굴', '45%'), ('4 꽃', '70%'), ('5 거대 호박', '100%'))
for k in range(5):
    x, y = (k % 2) * 195 + 6, 62 + (k // 2) * 208; u.box(x, y, x + 183, y + 198, fill='#2A2040'); s = ST[k]; sc = max(1, min(6, 150 // max(s.width, s.height) * 1)); sc = max(1, 168 // max(s.width, s.height) if s.width > 30 else 6)
    s2 = s.resize((s.width * sc * 2, s.height * sc * 2), Image.NEAREST); u.post.append((s2, (int((x + 91) * 2 - s2.width / 2), int((y + 142) * 2 - s2.height)))); u.text((x + 12, y + 156), names[k][0]); u.text((x + 12, y + 176), '성장 ' + names[k][1] + ' 부터', '#9A90B8')
u.cap('④ 호박이 자라는 모습 5단계 (게임 호박과 같은 도트)'); S.append(u.done())
# 5) 기숙사 앞 호박
u = UI(shot('campus')); spr(u.base, 4, 118, 345, 1, glow=True)
for (nx, ny, col, nm) in ((300, 255, '#5CCB8E', '듀모른'), (300, 435, '#F08A3C', '엠버킬른'), (92, 525, '#E8709A', '더스크폴드'), (250, 600, '#7A66E0', '문할로우')):
    s = ST[4].resize((ST[4].width * 2 // 2 * 1, ST[4].height * 2 // 2 * 1), Image.NEAREST); u.base.alpha_composite(s.resize((s.width, s.height), Image.NEAREST), (int(nx * 2 - s.width / 2), int(ny * 2 - s.height)))
    u.d.rounded_rectangle([nx - 40, ny + 2, nx + 40, ny + 24], radius=8, fill=c(col, 230)); u.text((nx - u.d.textlength(nm, font=F16) / 2, ny + 4), nm)
u.cap('⑤ 기숙사마다 호박 장식이 하나씩 놓여요'); S.append(u.done())
# 6) 보상과 관리자
u = UI(); u.head('보상과 관리자 화면'); u.box(12, 66, 378, 292); u.text((26, 78), '반 전체 단계 보상 (모두에게)', '#FFC23A')
for i, t in enumerate(('2단계 새싹  씨앗 2개', '3단계 덩굴  마나석 2개', '4단계 꽃  골드 200', '5단계 거대 호박  (보상은 정하는 중)')): u.text((26, 112 + i * 30), t, '#D9CFF0')
u.text((26, 240), '내가 돌본 양에 따라 개인 보상도 받아요', '#9A90B8'); u.box(12, 308, 378, 520, out='#F08A3C'); u.text((26, 320), '관리자 화면', '#F08A3C'); u.text((26, 350), '성장 372/600 · 돌본 학생 14명', '#D9CFF0')
for k, t in enumerate(('이벤트 열기', '성장 속도 ×2', '처음으로', '이벤트 닫기')): x, y = 26 + (k % 2) * 172, 388 + (k // 2) * 44; u.d.rounded_rectangle([x, y, x + 160, y + 34], radius=8, fill=c('#2D2147'), outline=c('#4A3A6A')); u.text((x + 10, y + 8), t)
u.cap('⑥ 단계 보상 · 관리자 화면'); S.append(u.done())
sheet = Image.new('RGB', (780 * 3, 1480 * 2))
for k, i in enumerate(S): sheet.paste(i.convert('RGB'), ((k % 3) * 780, (k // 3) * 1480))
sheet.save(OUTD + '/ev5_sheet.png'); S[3].convert('RGB').save(OUTD + '/ev5_stages.png'); S[0].convert('RGB').save(OUTD + '/ev5_field.png'); S[2].convert('RGB').save(OUTD + '/ev5_done.png')
st = Image.new('RGBA', (5 * 140, 120), (40, 30, 60, 255))
for k in range(5): s = ST[k]; sc = max(1, 110 // max(s.width, s.height)); st.alpha_composite(s.resize((s.width * sc, s.height * sc), Image.NEAREST), (k * 140 + 6, 115 - s.height * sc))
st.save('/tmp/ev5_strip.png'); print('ok')
