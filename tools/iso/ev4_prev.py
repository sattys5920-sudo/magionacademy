# 이벤트 「유령 등불 찾기」 시안: 실제 게임 화면 위에 등불·표시를 얹어서 → out/ev4_sheet.png (스크린샷은 인자로 받은 폴더)
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SH = sys.argv[1]; OUTD = os.path.dirname(os.path.abspath(__file__)) + '/out'
random.seed(4)
def c(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
FP = '/usr/share/fonts/opentype/unifont/unifont.otf'; F16 = ImageFont.truetype(FP, 16); F32 = ImageFont.truetype(FP, 32)
def shot(n): return Image.open(f'{SH}/{n}.png').convert('RGBA').resize((390, 740), Image.LANCZOS)
def lantern(sz=3, glow=True):
    L = Image.new('RGBA', (16, 22), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    OUT, TEAL, GL, FL = c('#0B1F2C'), c('#1F4E5F'), c('#3FE0A0'), c('#C8FFE8')
    d.rectangle([6, 0, 9, 2], fill=TEAL, outline=OUT); d.line([7, 3, 8, 3], fill=OUT); d.rectangle([3, 3, 12, 5], fill=TEAL, outline=OUT)
    d.rectangle([3, 6, 12, 17], fill=GL, outline=OUT); d.rectangle([5, 8, 10, 15], fill=c('#8FFFD0')); d.rectangle([6, 10, 9, 14], fill=FL)
    d.line([6, 6, 6, 17], fill=OUT); d.line([9, 6, 9, 17], fill=OUT) if False else None
    d.rectangle([3, 18, 12, 20], fill=TEAL, outline=OUT); d.point((7, 21), fill=OUT)
    L = L.resize((16 * sz, 22 * sz), Image.NEAREST)
    if not glow: return L
    G = Image.new('RGBA', (L.width + 80 * sz // 3 * 2, L.height + 80 * sz // 3 * 2), (0, 0, 0, 0)); gd = ImageDraw.Draw(G); cx, cy = G.width // 2, G.height // 2
    for r, a in ((G.width // 2, 26), (G.width // 3, 44), (G.width // 5, 70)): gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c('#3FE0A0', a))
    G = G.filter(ImageFilter.GaussianBlur(6)); G.alpha_composite(L, ((G.width - L.width) // 2, (G.height - L.height) // 2)); return G
def put(im, spr, x, y): im.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height / 2)))
def pill(im, text, x, y, col='#3FE0A0'):
    d = ImageDraw.Draw(im); w = d.textlength(text, font=F16) + 28; d.rounded_rectangle([x, y, x + w, y + 32], radius=16, fill=c('#0B1F2C', 230), outline=c(col), width=2); d.text((x + 14, y + 7), text, fill=c('#FFFFFF'), font=F16); return w
def bubble(im, text, x, y, w=300, who=None, col='#FFC23A'):
    d = ImageDraw.Draw(im); lines = text.split('\n'); h = 22 * len(lines) + 20 + (22 if who else 0)
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=c('#1B1230', 240), outline=c(col), width=2)
    yy = y + 10
    if who: d.text((x + 12, yy), who, fill=c(col), font=F16); yy += 22
    for l in lines: d.text((x + 12, yy), l, fill=c('#FFFFFF'), font=F16); yy += 22
def caption(im, text):
    d = ImageDraw.Draw(im); d.rectangle([0, 690, 390, 740], fill=c('#0B0716', 235)); d.text((14, 706), text, fill=c('#D9CFF0'), font=F16)
def hud_counter(im, n): pill(im, f'유령 등불 {n} / 30', 90, 62)
S = []
# 1) 찾기: 학교 앞마당, 나무 뒤에 숨은 등불
im = shot('campus'); hud_counter(im, 12); L = lantern(3); put(im, L, 252, 226)
d = ImageDraw.Draw(im); d.ellipse([222, 196, 282, 256], outline=c('#FFFFFF', 150), width=2)
bubble(im, '반짝이는 걸 눌러서 주워요', 70, 300, 250, col='#3FE0A0'); caption(im, '① 지도 곳곳에 숨은 등불을 눌러서 찾아요'); S.append(im)
# 2) 힌트: 마을 + 아울라
im = shot('town'); hud_counter(im, 17); put(im, lantern(3), 108, 330)
bubble(im, '시장 왼쪽 가판대 뒤에서\n초록 불빛을 봤어요, 호!', 24, 446, 340, who='아울라', col='#FFC23A'); caption(im, '② NPC에게 말 걸면 힌트를 줘요'); S.append(im)
# 3) 찾은 순간
im = shot('quarter'); hud_counter(im, 18)
for k in range(10):
    a = random.random() * 6.28; r = 30 + random.random() * 38; sp = Image.new('RGBA', (8, 8), (0, 0, 0, 0)); ImageDraw.Draw(sp).rectangle([2, 2, 5, 5], fill=c('#C8FFE8')); put(im, sp, 300 + math.cos(a) * r, 320 + math.sin(a) * r)
put(im, lantern(4), 300, 320); ImageDraw.Draw(im).line([300, 360, 300, 420], fill=c('#3FE0A0', 80), width=4)
bubble(im, '유령 등불을 찾았어요! (18/30)\n마나석 1개를 얻었어요', 24, 470, 342, col='#3FE0A0'); caption(im, '③ 찾으면 반 전체 숫자가 올라가요'); S.append(im)
# 4) 단계 연출: 꼬마 유령
im = Image.new('RGBA', (390, 740), c('#0A0618')); lake = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/../../public/art/ev2_lake.png').convert('RGBA').resize((390, 234), Image.NEAREST); im.alpha_composite(lake, (0, 0))
g = Image.new('RGBA', (28, 32), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([2, 2, 25, 24], fill=c('#EDEBFF')); gd.rectangle([2, 14, 25, 28], fill=c('#EDEBFF')); 
for x in (2, 8, 14, 20): gd.polygon([(x, 28), (x + 3, 31), (x + 6, 28)], fill=c('#EDEBFF'))
gd.ellipse([8, 11, 12, 16], fill=c('#120A18')); gd.ellipse([16, 11, 20, 16], fill=c('#120A18')); gd.ellipse([12, 18, 16, 21], fill=c('#120A18')); gd.ellipse([3, 15, 7, 18], fill=c('#FFB0C8', 170)); gd.ellipse([21, 15, 25, 18], fill=c('#FFB0C8', 170))
gs = g.resize((28 * 6, 32 * 6), Image.NEAREST); put(im, lantern(3), 120, 150); put(im, lantern(3), 280, 130); put(im, gs, 195, 150)
hud_counter(im, 20)
d = ImageDraw.Draw(im); d.rounded_rectangle([12, 330, 378, 520], radius=12, fill=c('#1B1230'), outline=c('#FFC23A'), width=2)
d.text((26, 344), '꼬마 유령', fill=c('#FFC23A'), font=F16); d.text((26, 376), '와아, 등불이 스무 개나 돌아왔어!', fill=c('#FFFFFF'), font=F16); d.text((26, 402), '조금만 더 찾아 주면 우리 다 같이', fill=c('#FFFFFF'), font=F16); d.text((26, 428), '하늘로 갈 수 있어....', fill=c('#FFFFFF'), font=F16)
d.rounded_rectangle([26, 466, 364, 504], radius=10, fill=c('#2D2147'), outline=c('#4A3A6A')); d.text((40, 477), '20개 달성 보상: 모두에게 골드 200', fill=c('#6FD08C'), font=F16); caption(im, '④ 10 · 20 · 30개마다 꼬마 유령 등장'); S.append(im)
# 5) 엔딩: 등불이 하늘로
im = shot('campus').convert('RGBA'); ov = Image.new('RGBA', (390, 740), c('#050414', 150)); im.alpha_composite(ov)
for k in range(26):
    x, y = random.randrange(20, 370), random.randrange(80, 640); sz = random.choice((1, 1, 2, 2, 3)); put(im, lantern(sz), x, y)
d = ImageDraw.Draw(im); d.rounded_rectangle([12, 600, 378, 676], radius=12, fill=c('#1B1230', 240), outline=c('#3FE0A0'), width=2); d.text((26, 614), '30 / 30  유령 등불을 모두 찾았어요!', fill=c('#FFFFFF'), font=F16); d.text((26, 642), '유령들이 등불과 함께 하늘로 올라가요.', fill=c('#9A90B8'), font=F16)
caption(im, '⑤ 다 모으면 학교 위로 등불이 떠오르는 연출'); S.append(im)
# 6) 현황 + 보상 + 관리자
im = Image.new('RGBA', (390, 740), c('#140E22')); d = ImageDraw.Draw(im); d.rectangle([0, 0, 390, 52], fill=c('#1B1230')); d.text((12, 17), '유령 등불 찾기', fill=c('#FFFFFF'), font=F16); d.text((390 - 12 - d.textlength('18 / 30', font=F16), 17), '18 / 30', fill=c('#FFC23A'), font=F16)
d.text((14, 70), '장소별로 찾은 등불', fill=c('#FFC23A'), font=F16)
rows = (('호박달 마녀학교', 5, 7), ('등불 마을 (시장)', 3, 6), ('그림자 골목', 4, 5), ('독초 온실', 2, 4), ('과자 교실', 2, 4), ('호수·묘지 쪽', 2, 4))
for i, (n, a, b) in enumerate(rows):
    y = 100 + i * 46; d.text((14, y), n, fill=c('#D9CFF0'), font=F16); d.text((390 - 14 - d.textlength(f'{a}/{b}', font=F16), y), f'{a}/{b}', fill=c('#FFFFFF'), font=F16)
    d.rounded_rectangle([14, y + 24, 376, y + 36], radius=6, fill=c('#2A2040')); d.rounded_rectangle([14, y + 24, 14 + int(362 * a / b), y + 36], radius=6, fill=c('#3FE0A0'))
y = 100 + 6 * 46 + 4; d.rounded_rectangle([12, y, 378, y + 118], radius=12, fill=c('#1B1230'), outline=c('#4A3A6A'), width=2)
d.text((26, y + 12), '단계 보상 (모두에게)', fill=c('#FFC23A'), font=F16); d.text((26, y + 40), '10개  마나석 3개', fill=c('#D9CFF0'), font=F16); d.text((26, y + 64), '20개  골드 200', fill=c('#D9CFF0'), font=F16); d.text((26, y + 88), '30개  유령 등불 장식 1점', fill=c('#D9CFF0'), font=F16)
y += 126; d.rounded_rectangle([12, y, 378, y + 150], radius=12, fill=c('#1B1230'), outline=c('#F08A3C'), width=2); d.text((26, y + 12), '관리자 화면', fill=c('#F08A3C'), font=F16)
d.text((26, y + 40), '찾은 등불 18/30 · 찾은 학생 14명', fill=c('#D9CFF0'), font=F16)
for k, t in enumerate(('이벤트 열기', '힌트 공개', '등불 다시 섞기', '이벤트 닫기')): d.rounded_rectangle([26 + (k % 2) * 172, y + 74 + (k // 2) * 34, 26 + (k % 2) * 172 + 160, y + 74 + (k // 2) * 34 + 28], radius=8, fill=c('#2D2147'), outline=c('#4A3A6A')); d.text((36 + (k % 2) * 172, y + 79 + (k // 2) * 34), t, fill=c('#FFFFFF'), font=F16)
caption(im, '⑥ 장소별 현황 · 단계 보상 · 관리자 화면'); S.append(im)
sheet = Image.new('RGB', (390 * 3, 740 * 2))
for k, i in enumerate(S): sheet.paste(i.convert('RGB'), ((k % 3) * 390, (k // 3) * 740))
sheet.save(OUTD + '/ev4_sheet.png'); print('ok')
