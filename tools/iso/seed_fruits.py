# 마법 씨앗 대회: 할로윈 식물 12종에서만 나오는 열매 12종 (아이템 아이콘 32×32, 게임 아이콘과 같은 LPC 그림체)
#   python3 seed_fruits.py → out/seed_fruits.png (32×32 × 12) · out/seed_fruits_preview.png
import os, math
from PIL import Image, ImageDraw, ImageFont
import seed_plants as SP   # 테두리·음영 손잡이 (import 하면 식물 그림도 다시 만들어요)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
hx, sh, ramp, outline = SP.hx, SP.sh, SP.ramp, SP.outline
class I:
    def __init__(s): s.im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def ball(s, x, y, rx, ry, c):   # 둥근 열매 4단 음영 + 반짝
        d0, m, l = ramp(c); s.d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=d0); s.d.ellipse([x - rx, y - ry, x + rx - 2, y + ry - 2], fill=m)
        if rx > 4 and ry > 4: s.d.ellipse([x - rx + 2, y - ry + 2, x - 1, y - 1], fill=l); s.d.ellipse([x - rx * .55 - 1, y - ry * .55 - 1, x - rx * .55 + 1, y - ry * .55 + 1], fill=(255, 255, 255, 230))
    def px(s, x, y, c): s.d.point((x, y), fill=hx(c) if isinstance(c, str) else c)
    def poly(s, pts, c): s.d.polygon(pts, fill=hx(c) if isinstance(c, str) else c)
    def line(s, pts, c, w=1): s.d.line(pts, fill=hx(c) if isinstance(c, str) else c, width=w)
    def stem(s, x, y, c='#4A6A22'): s.line([(x, y), (x + 1, y - 4)], c, 2); s.poly([(x + 1, y - 3), (x + 7, y - 6), (x + 3, y - 1)], '#5A9A2E')
    def done(s): return outline(s.im)
def jack(s):   # 잭오랜턴 열매
    s.ball(16, 18, 11, 9, '#F07A18'); s.line([(11, 10), (11, 26)], '#B85A0E'); s.line([(21, 10), (21, 26)], '#B85A0E'); s.d.rectangle([15, 6, 17, 9], fill=hx('#4A6A1E'))
    s.poly([(9, 16), (13, 12), (14, 17)], '#FFE070'); s.poly([(23, 16), (19, 12), (18, 17)], '#FFE070'); s.poly([(9, 21), (23, 21), (20, 25), (16, 22), (12, 25)], '#FFE070')
def bat(s):    # 박쥐 날개 꼬투리
    for k in (-1, 1): s.poly([(16, 14), (16 + k * 7, 8), (16 + k * 14, 11), (16 + k * 12, 16), (16 + k * 9, 14), (16 + k * 7, 18)], '#5A3A7A')
    for k in (-1, 1): s.line([(16, 14), (16 + k * 12, 11)], '#3A2052')
    s.ball(16, 18, 5, 7, '#6A4A8A'); s.px(14, 16, '#FF3A4A'); s.px(18, 16, '#FF3A4A'); s.px(15, 21, '#F0F0F0'); s.px(17, 21, '#F0F0F0')
def ghostdrop(s):   # 유령 꿀방울
    s.poly([(16, 3), (24, 16), (24, 22), (20, 28), (12, 28), (8, 22), (8, 16)], '#D8E4F4'); s.poly([(16, 3), (12, 12), (11, 22), (13, 27), (8, 22), (8, 16)], '#F0F6FF')
    s.poly([(20, 14), (24, 16), (24, 22), (20, 28), (18, 26)], '#AEBEDA'); s.px(13, 18, '#1A1428'); s.px(19, 18, '#1A1428'); s.d.ellipse([14, 21, 18, 24], fill=hx('#1A1428'))
    s.px(11, 11, '#FFFFFF'); s.px(25, 8, '#9AF0D0'); s.px(5, 12, '#9AF0D0')
def skull(s):  # 해골 씨주머니
    s.ball(16, 14, 10, 9, '#ECE6D8'); s.d.rectangle([11, 20, 21, 26], fill=hx('#D8D2C2')); s.d.rectangle([11, 20, 13, 26], fill=hx('#ECE6D8'))
    s.d.ellipse([9, 11, 14, 17], fill=hx('#2A1A22')); s.d.ellipse([18, 11, 23, 17], fill=hx('#2A1A22')); s.px(11, 13, '#E04050'); s.px(20, 13, '#E04050')
    s.poly([(15, 18), (17, 18), (16, 20)], '#2A1A22'); [s.px(x, 24, '#7A7266') for x in (13, 16, 19)]
    s.line([(16, 5), (17, 1)], '#3E6E2E', 2)
def web(s):    # 거미줄 솜열매
    s.ball(16, 17, 10, 11, '#ECEAF4')
    for y in (11, 15, 19, 23): s.line([(8, y), (24, y + 1)], (170, 160, 195, 200))
    s.line([(16, 6), (16, 28)], (170, 160, 195, 200)); s.line([(16, 2), (16, 6)], '#C8C0D8')
    s.ball(23, 8, 2.6, 2.4, '#2A1E30'); s.px(22, 8, '#FF4A5A'); [s.px(23 + dx, 8 + dy, '#2A1E30') for dx, dy in ((-3, -2), (3, -2), (-3, 2), (3, 2))]
def hat(s):    # 마녀 모자 포자
    s.poly([(5, 24), (27, 24), (20, 12), (24, 3), (14, 10)], '#6A3A9A'); s.poly([(14, 10), (20, 12), (17, 22), (9, 22)], '#8A5ABA')
    s.d.ellipse([3, 21, 29, 28], fill=hx('#4A2A6A')); s.d.ellipse([3, 21, 27, 26], fill=hx('#5A3A82'))
    s.d.rectangle([10, 19, 22, 22], fill=hx('#2A1440')); s.d.rectangle([14, 19, 18, 22], fill=hx('#E8B030')); s.px(15, 20, '#FFE080')
    s.px(26, 6, '#E0B0FF'); s.px(5, 10, '#E0B0FF')
def eye(s):    # 눈알 열매
    s.ball(16, 17, 11, 11, '#F4F0E8'); s.d.arc([5, 6, 27, 28], 20, 160, fill=hx('#C8C0B0'))
    for pts in (((6, 12), (10, 14)), ((26, 20), (22, 19)), ((9, 24), (12, 21))): s.line(list(pts), '#E05050')
    s.d.ellipse([10, 11, 22, 23], fill=hx('#3A8AE0')); s.d.ellipse([12, 13, 20, 21], fill=hx('#5AA8F0')); s.d.ellipse([14, 15, 18, 19], fill=hx('#0A0A14')); s.d.ellipse([12, 13, 15, 16], fill=(255, 255, 255, 240))
    s.line([(16, 6), (18, 1)], '#3E7A3A', 2)
def candy(s):  # 사탕옥수수 알
    s.poly([(16, 3), (25, 26), (7, 26)], '#FFF4E0'); s.poly([(11, 15), (21, 15), (25, 26), (7, 26)], '#FF9A28'); s.poly([(8.5, 22), (23.5, 22), (25, 26), (7, 26)], '#FFD038')
    s.poly([(16, 3), (13, 11), (12, 15), (11, 15)], '#FFFFFF'); s.line([(21, 15), (25, 26)], '#C86A10'); s.px(14, 8, '#FFFFFF')
def wisp(s):   # 도깨비불 꽈리
    s.poly([(16, 4), (26, 15), (24, 24), (16, 29), (8, 24), (6, 15)], '#E85A1E'); s.poly([(16, 4), (12, 14), (11, 24), (8, 24), (6, 15)], '#FF7A3A')
    for x in (12, 16, 20): s.line([(16, 5), (x, 28)], '#A8380E')
    s.ball(16, 18, 3.5, 4.5, '#7AFF6A'); s.px(16, 16, '#F0FFE8'); s.line([(16, 4), (17, 1)], '#4A6A22', 2)
    s.px(4, 8, '#9AFF8A'); s.px(28, 10, '#9AFF8A')
def rosehip(s):   # 검은 장미 열매
    s.ball(16, 18, 9, 10, '#3A2238'); s.d.ellipse([8, 9, 24, 27], outline=(150, 80, 200, 160))
    for k in range(5): a = math.radians(k * 72 - 90); s.poly([(16, 8), (16 + 6 * math.cos(a - .3), 8 + 4 * math.sin(a - .3) - 2), (16 + 6 * math.cos(a + .3), 8 + 4 * math.sin(a + .3) - 2)], '#2E4A26')
    s.px(12, 14, '#C890FF'); s.px(13, 13, '#E8C8FF'); s.px(26, 6, '#C890FF')
def apple(s):  # 독사과
    s.ball(16, 18, 11, 10, '#8AD030'); s.d.ellipse([13, 7, 19, 11], fill=hx('#6AA020')); s.line([(16, 9), (17, 3)], '#4A3A2E', 2); s.poly([(17, 5), (24, 2), (21, 7)], '#3E7A2E')
    s.d.ellipse([12, 15, 15, 18], fill=hx('#1A2A0A')); s.d.ellipse([17, 15, 20, 18], fill=hx('#1A2A0A')); s.poly([(15, 19), (17, 19), (16, 21)], '#1A2A0A')
    for x in (13, 16, 19): s.px(x, 23, '#1A2A0A')
    s.px(26, 22, '#B8FF6A'); s.px(27, 24, '#9AE03A')
def fang(s):   # 피빛 송곳니 열매
    s.ball(16, 16, 10, 10, '#C02A3A'); s.poly([(11, 22), (13, 22), (12, 29)], '#FFFFFF'); s.poly([(19, 22), (21, 22), (20, 29)], '#FFFFFF')
    s.line([(12, 22), (12, 27)], '#D8D8E0'); s.line([(20, 22), (20, 27)], '#D8D8E0'); s.d.rectangle([10, 21, 22, 22], fill=hx('#7A1020'))
    s.line([(16, 6), (17, 1)], '#3E7A2E', 2); s.px(23, 26, '#FF5060'); s.px(23, 27, '#C02A3A')
FRUITS = [('잭오랜턴 열매', jack, '잭오랜턴 호박꽃'), ('박쥐 날개 꼬투리', bat, '박쥐 날개 고사리'), ('유령 꿀방울', ghostdrop, '유령 난초'), ('해골 씨주머니', skull, '해골 양귀비'),
          ('거미줄 솜열매', web, '거미줄 백합'), ('마녀 모자 포자', hat, '마녀 모자 버섯'), ('눈알 열매', eye, '눈알 열매덩굴'), ('사탕옥수수 알', candy, '사탕옥수수 튤립'),
          ('도깨비불 꽈리', wisp, '도깨비불 등불초'), ('검은 장미 열매', rosehip, '검은 장미'), ('독사과', apple, '독사과 나무'), ('피빛 송곳니 열매', fang, '뱀파이어 송곳니 끈끈이')]
if __name__ == '__main__':
    icons = []
    for nm, fn, _ in FRUITS: s = I(); fn(s); icons.append(s.done())
    S = Image.new('RGBA', (32 * len(icons), 32), (0, 0, 0, 0))
    for i, c in enumerate(icons): S.alpha_composite(c, (i * 32, 0))
    S.save(os.path.join(OUT, 'seed_fruits.png'))
    plants = Image.open(os.path.join(OUT, 'seed_plants.png')).convert('RGBA')
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 14) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 12) if os.path.exists(fb) else F
    cw, chh = 180, 220; pv = Image.new('RGB', (cw * 6 + 20, 50 + chh * 2), (26, 18, 34)); d = ImageDraw.Draw(pv)
    d.text((14, 14), '식물마다 그 식물에서만 나오는 열매 (하루 한 번 수확)', font=F, fill=(255, 233, 160))
    for i, (nm, fn, pn) in enumerate(FRUITS):
        x, y = 10 + (i % 6) * cw, 44 + (i // 6) * chh; d.rounded_rectangle([x, y, x + cw - 10, y + chh - 10], 12, fill=(44, 32, 58))
        p = plants.crop(((15 + i) * 40, 0, (16 + i) * 40, 56)).resize((80, 112), Image.NEAREST); pv.paste(p, (x + 8, y + 16), p)
        f = icons[i].resize((64, 64), Image.NEAREST); pv.paste(f, (x + 98, y + 50), f); d.text((x + 86, y + 80), '→', font=F, fill=(200, 180, 230), anchor='mm')
        d.text((x + (cw - 10) / 2, y + 150), nm, font=F, fill=(255, 240, 200), anchor='mm'); d.text((x + (cw - 10) / 2, y + 172), pn, font=F2, fill=(190, 170, 220), anchor='mm')
    pv.save(os.path.join(OUT, 'seed_fruits_preview.png')); print('fruits ok')
