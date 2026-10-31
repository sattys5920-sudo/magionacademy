# 마법 씨앗 대회 · 호박 왕 잭: 열매 12종으로 만드는 할로윈 요리 17종 (일반 12 · 특별 4 · 만찬 1) · 아이템 아이콘 32×32 (열매와 같은 그림체)
#   python3 seed_dishes.py → out/seed_dishes.png (32×32 × 17) · out/seed_dishes.json (레시피) · out/seed_dishes_preview.png
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import seed_fruits as SF
from seed_fruits import Icon, E, PG, LN, inner_line, hx
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
FR = [f[0] for f in SF.FRUITS]   # 0 잭오랜턴 열매 · 1 박쥐 날개 꼬투리 · 2 유령 꿀방울 · 3 해골 씨주머니 · 4 거미줄 솜열매 · 5 마녀 모자 포자 · 6 눈알 열매 · 7 사탕옥수수 알 · 8 도깨비불 꽈리 · 9 검은 장미 열매 · 10 독사과 · 11 피빛 송곳니 열매
def plate(s, y=24, c='#D8D4E4'): s.shade(s.mask(E(3, y, 29, y + 7)), c, k=.5); s.fill(s.mask(E(7, y + 1.5, 25, y + 5.5)), '#ECEAF4')
def bowl(s, c='#5A4A7A', y=15):   # 사발 (위에서 비스듬히)
    s.shade(s.mask(PG([(3, y), (29, y), (26, y + 9), (21, y + 13), (11, y + 13), (6, y + 9)])), c, k=.6); return s.mask(E(3, y - 4, 29, y + 4))
def eyeball(s, x, y, r=3, iris='#3A86DC'):
    s.shade(s.mask(E(x - r, y - r, x + r, y + r)), '#F2EEE6', gloss=False); s.fill(s.mask(E(x - r * .5, y - r * .5, x + r * .5, y + r * .5)), iris); s.px(int(round(x)), int(round(y)), '#0C0C16'); s.px(int(round(x - r * .4)), int(round(y - r * .4)), '#FFFFFF')
def skull(s, x, y, r=3.4):
    s.shade(s.mask(E(x - r, y - r, x + r, y + r * .8)), '#EEE8DA', gloss=False); s.fill(s.mask(PG([(x - r * .55, y + r * .5), (x + r * .55, y + r * .5), (x + r * .45, y + r * 1.2), (x - r * .45, y + r * 1.2)])), '#DED6C4')
    s.px(int(x - r * .4), int(y), '#2A1A24'); s.px(int(x + r * .4), int(y), '#2A1A24')
def steam(s, xs, y=4, c='#C8E8D8'):
    for x in xs: s.fill(s.mask(LN([(x, y + 6), (x - 1.5, y + 3), (x + .5, y)], 1)), c)
# ---- 일반 12 ----
def d_pie(s):   # 잭오랜턴 파이
    plate(s, 22); s.shade(s.mask(E(4, 9, 28, 27)), '#B8742E', k=.6); m = s.mask(E(6.5, 11, 25.5, 24.5)); s.shade(m, '#F08A20')
    for pts in (((10, 16), (13, 13.5), (14, 17)), ((22, 16), (19, 13.5), (18, 17)), ((10, 20), (22, 20), (19.5, 22.5), (16, 21), (12.5, 22.5))): s.fill(s.mask(PG(pts)) & m, '#7A3A0A')
    for x in range(6, 27, 3): s.px(x, 10 if 9 < x < 23 else 12, '#E0A458')
    s.fill(s.mask(PG([(15, 5), (17, 5), (18.5, 9.5), (13.5, 9.5)])), '#FF9426'); s.fill(s.mask(PG([(15.4, 5), (16.6, 5), (17, 6.5), (15, 6.5)])), '#FFF2DA')
def d_rosecandy(s):   # 검은 장미 사탕
    s.fill(s.mask(LN([(16, 17), (16, 30)], 2)), '#F0ECE0'); m = s.shade(s.mask(E(6, 3, 26, 21)), '#4A2A50')
    for r, c in ((7, '#7A3A80'), (4.5, '#4A2A50'), (2.2, '#9A5AA8')): s.fill(s.mask(lambda d, k, r=r: d.arc([(16 - r) * k, (12 - r) * k, (16 + r) * k, (12 + r) * k], 0, 300, fill=255, width=int(1.4 * k))) & m, c)
    s.fill(s.mask(PG([(12, 21), (20, 21), (22, 24), (10, 24)])), '#E04878'); s.px(11, 7, '#FFFFFF'); s.px(12, 6, '#F0D8FF')
def d_rosetart(s):   # 피빛 장미 타르트
    plate(s, 23); s.shade(s.mask(PG([(5, 15), (27, 15), (25, 26), (7, 26)])), '#C8904A', k=.5)
    for x in range(6, 27, 3): s.fill(s.mask(LN([(x, 16), (x - .5, 25)], 1)), '#A8703A')
    m = s.shade(s.mask(E(5, 11, 27, 19)), '#B01E30'); s.shade(s.mask(E(11, 5, 21, 15)), '#3E2440'); s.fill(s.mask(lambda d, k: d.arc([13 * k, 7 * k, 19 * k, 13 * k], 20, 320, fill=255, width=int(1.2 * k))), '#7A4A7A')
    s.px(8, 13, '#FF7080')
def d_eyejelly(s):   # 눈알 젤리
    plate(s, 23); m = s.mask(PG([(7, 9), (25, 9), (26, 25), (6, 25)])); s.shade(m, '#6ACA3A', k=.8)
    s.fill(s.mask(PG([(7, 9), (25, 9), (23, 6), (9, 6)])), '#9AE860'); eyeball(s, 16, 17, 5, '#C83A3A')
    for x, y in ((9, 12), (10, 13)): s.px(x, y, '#E8FFC8')
def d_ghostpud(s):   # 유령 눈알 푸딩
    plate(s, 24); m = s.shade(s.mask(PG([(9, 26), (8, 13), (11, 6), (16, 4), (21, 6), (24, 13), (23, 26), (20, 23.5), (16, 26), (12, 23.5)])), '#EEF2FA')
    s.fill(s.mask(PG([(11, 6), (16, 4), (21, 6), (22, 10), (19, 8.5), (16, 11), (13, 8.5), (10, 10)])) & m, '#C88A3A')
    eyeball(s, 16, 16, 3.4, '#3A86DC'); s.fill(s.mask(E(14.5, 20.5, 17.5, 23)), '#2A2440')
def d_cotton(s):   # 유령 솜사탕
    s.fill(s.mask(LN([(16, 19), (15, 30)], 2)), '#E8C890')
    for x, y, r in ((16, 11, 8), (9, 13, 5), (23, 12, 5.5), (13, 6, 4.5), (20, 6, 4.5)): s.shade(s.mask(E(x - r, y - r, x + r, y + r)), '#DCE6FF', k=.6)
    s.px(13, 11, '#2A2440'); s.px(19, 11, '#2A2440'); s.fill(s.mask(E(14.8, 13.5, 17.2, 16)), '#2A2440'); s.px(9, 7, '#FFFFFF')
def d_webcookie(s):   # 거미줄 해골 쿠키
    m = s.shade(s.mask(E(3, 4, 29, 28)), '#8A5A32', k=.7); c = s.mask(E(6, 7, 26, 25)); s.fill(c, '#3A2418')
    for r in (3, 6, 9): s.fill(s.mask(lambda d, k, r=r: d.ellipse([(16 - r) * k, (16 - r) * k, (16 + r) * k, (16 + r) * k], outline=255, width=int(.9 * k))) & c, '#F4F0F8')
    for a in range(0, 360, 45): r_ = math.radians(a); s.fill(s.mask(LN([(16, 16), (16 + 10 * math.cos(r_), 16 + 10 * math.sin(r_))], .9)) & c, '#F4F0F8')
    skull(s, 16, 15, 3.2)
def d_batsoup(s):   # 해골 박쥐 수프
    top = bowl(s, '#4A3A5A', 16); s.fill(top, '#7A3A9A'); s.fill(s.mask(E(5, 13, 27, 19)), '#9A5ABA'); skull(s, 12, 14, 3)
    for k_ in (-1, 1): s.fill(s.mask(PG([(21, 14), (21 + k_ * 4, 10), (21 + k_ * 7, 12), (21 + k_ * 5, 15)])), '#3A2050')
    s.px(21, 14, '#3A2050'); steam(s, (9, 16, 23), 2, '#D8C0F0')
def d_batmuffin(s):   # 박쥐 모자 머핀
    s.shade(s.mask(PG([(8, 18), (24, 18), (22, 28), (10, 28)])), '#E07AA8', k=.5)
    for x in range(10, 24, 3): s.fill(s.mask(LN([(x, 19), (x - .5, 27)], 1)), '#B04A80')
    s.shade(s.mask(E(6, 11, 26, 21)), '#6A3A2A'); s.shade(s.mask(PG([(10, 14), (22, 14), (18, 6), (21, 2), (15, 5)])), '#6A3A9A')
    for k_ in (-1, 1): s.fill(s.mask(PG([(16 + k_ * 5, 13), (16 + k_ * 10, 9), (16 + k_ * 13, 12), (16 + k_ * 10, 14)])), '#3A2050')
def d_wisptea(s):   # 도깨비불 마녀 차
    s.shade(s.mask(E(3, 23, 29, 29)), '#C8C0E0', k=.5); s.shade(s.mask(PG([(6, 13), (24, 13), (22, 24), (8, 24)])), '#6A4A9A', k=.6)
    s.fill(s.mask(lambda d, k: d.arc([22 * k, 14 * k, 29 * k, 21 * k], 270, 90, fill=255, width=int(1.6 * k))), '#6A4A9A')
    s.fill(s.mask(E(6, 11, 24, 15.5)), '#6AF05A'); s.fill(s.mask(E(11, 12, 19, 14.5)), '#C8FFB0'); steam(s, (11, 16, 21), 3, '#9AFF8A')
    s.px(10, 17, '#E8B030'); s.px(19, 19, '#E8B030')
def d_cider(s):   # 도깨비불 사과 사이다
    m = s.mask(PG([(9, 7), (23, 7), (22, 28), (10, 28)])); s.fill(m, '#C8E0F0'); s.fill(s.mask(PG([(9.5, 12), (22.5, 12), (22, 28), (10, 28)])), '#7ADC4A')
    s.fill(s.mask(PG([(10, 12), (13, 12), (12.5, 28), (10, 28)])), '#A8F070')
    for x, y in ((14, 24), (18, 20), (15, 17), (19, 14)): s.fill(s.mask(E(x - 1, y - 1, x + 1, y + 1)), '#E8FFD8')
    s.shade(s.mask(E(18, 3, 27, 11)), '#86CC2E', gloss=False); s.fill(s.mask(E(20.5, 5, 24.5, 9)), '#F4F0C8'); s.fill(s.mask(LN([(14, 2), (17, 13)], 1.4)), '#F05050')
def d_applesoup(s):   # 독사과 호박 수프
    top = bowl(s, '#C86A1E', 16); s.fill(top, '#F0A030'); s.fill(s.mask(E(5, 13, 27, 19)), '#FFC050')
    for x, y in ((11, 14), (21, 15)): s.shade(s.mask(E(x - 3, y - 2, x + 3, y + 2)), '#86CC2E', gloss=False); s.px(x, y, '#F4F0C8')
    s.fill(s.mask(E(14, 11, 18, 14)), '#F4F0F8'); s.px(15, 12, '#2A2440'); s.px(17, 12, '#2A2440'); steam(s, (10, 16, 22), 2, '#FFE0B0')
# ---- 특별 4 ----
def d_cauldron(s):   # 마녀의 대솥 스튜
    s.shade(s.mask(E(4, 10, 28, 30)), '#2A2238', k=.8); s.fill(s.mask(E(3, 8, 29, 14)), '#4A4060'); s.fill(s.mask(E(5, 9, 27, 13)), '#8A3AB8')
    for x, y, r in ((10, 9, 1.8), (17, 8, 2.4), (23, 10, 1.6), (13, 5, 1.4), (20, 3, 1.2)): s.fill(s.mask(E(x - r, y - r, x + r, y + r)), '#C890FF')
    s.fill(s.mask(LN([(20, 12), (25, 5)], 1.6)), '#EEE8DA'); s.px(25, 4, '#EEE8DA'); s.px(26, 5, '#EEE8DA')
    for x in (8, 24): s.fill(s.mask(LN([(x, 28), (x - 1, 31)], 1.6)), '#1A1424')
    s.fill(s.mask(E(12, 28, 20, 31)), '#FF7A2A')
def d_trifle(s):   # 유령 파티 푸딩
    s.fill(s.mask(PG([(7, 9), (25, 9), (23, 26), (9, 26)])), '#C8D8EE'); 
    for y0, y1, c in ((19, 26, '#5A8AD8'), (14, 19, '#F4F6FF'), (10, 14, '#9AC8FF')): s.fill(s.mask(PG([(7 + (y0 - 9) * .12, y0), (25 - (y0 - 9) * .12, y0), (25 - (y1 - 9) * .12, y1), (7 + (y1 - 9) * .12, y1)])), c)
    s.shade(s.mask(E(12, 26, 20, 30)), '#B8C8E0', k=.4)
    s.shade(s.mask(PG([(12, 10), (12, 5), (14, 2), (18, 2), (20, 5), (20, 10), (18, 8.5), (16, 10), (14, 8.5)])), '#F4F6FF'); s.px(14, 5, '#2A2440'); s.px(18, 5, '#2A2440')
    s.fill(s.mask(E(21, 12, 25, 16)), '#9AFF8A'); s.px(22, 13, '#F0FFE8')
def d_vampjelly(s):   # 뱀파이어 만찬 젤리
    plate(s, 23, '#3A2A3A'); m = s.shade(s.mask(lambda d, k: (d.pieslice([5 * k, 6 * k, 27 * k, 40 * k], 180, 360, fill=255))), '#C02838')
    eyeball(s, 16, 15, 3.6, '#E0A030')
    for x in (12, 20): s.fill(s.mask(PG([(x - 1.5, 21), (x + 1.5, 21), (x, 26)])), '#FAF6F0')
    s.fill(s.mask(E(13, 3, 19, 7)), '#3E2440'); s.px(9, 10, '#FF8A9A'); s.px(10, 9, '#FFC0C8')
def d_candyapple(s):   # 잭의 사탕 사과
    s.fill(s.mask(LN([(16, 2), (16, 13)], 1.8)), '#E8C890'); s.shade(s.mask(E(5, 10, 27, 30)), '#C82838')
    s.fill(s.mask(PG([(6, 22), (26, 22), (24, 27), (8, 27)])) & s.mask(E(5, 10, 27, 30)), '#86CC2E')
    for x in (9, 15, 21): s.fill(s.mask(PG([(x, 13), (x + 2, 13), (x + 1, 16)])), '#FFF2DA'); s.fill(s.mask(PG([(x + .3, 14.2), (x + 1.7, 14.2), (x + 1, 16)])), '#FF9426')
    s.px(9, 18, '#FFFFFF'); s.px(10, 17, '#FFD0D8')
# ---- 만찬 ----
def d_feast(s):   # 열두 밤 만찬: 큰 쟁반에 호박 가운데, 둘레에 열매 열두 빛
    s.shade(s.mask(E(1, 15, 31, 30)), '#B8902E', k=.5); s.fill(s.mask(E(3, 17, 29, 28)), '#E8C060')
    s.shade(s.mask(E(9, 8, 23, 22)), '#F07A18'); s.fill(s.mask(LN([(16, 8), (16, 22)], 1)), '#B4560E'); s.fill(s.mask(E(15, 5, 17.5, 9)), '#5A7A22')
    for pts in (((11.5, 14), (14, 12), (14.5, 15)), ((20.5, 14), (18, 12), (17.5, 15)), ((11.5, 17), (20.5, 17), (18, 19.5), (14, 19.5))): s.fill(s.mask(PG(pts)), '#FFE070')
    cols = ['#F07A18', '#6A4A8A', '#E4ECF4', '#EEE8DA', '#D4D0E4', '#7A44AA', '#3A86DC', '#FF9426', '#7AFF6A', '#3E2440', '#86CC2E', '#C42838']
    for i, c in enumerate(cols): a = math.radians(i * 30); x, y = 16 + 12.5 * math.cos(a), 23 + 4.2 * math.sin(a); s.fill(s.mask(E(x - 1.6, y - 1.4, x + 1.6, y + 1.4)), c)
    for x, y in ((4, 6), (28, 5), (16, 1)): s.px(x, y, '#FFE89A')
DISHES = [   # 이름, 그림, 열매 번호들, 종류
  ('잭오랜턴 파이', d_pie, [0, 7], '일반'), ('검은 장미 사탕', d_rosecandy, [7, 9], '일반'), ('피빛 장미 타르트', d_rosetart, [9, 11], '일반'), ('눈알 젤리', d_eyejelly, [11, 6], '일반'),
  ('유령 눈알 푸딩', d_ghostpud, [6, 2], '일반'), ('유령 솜사탕', d_cotton, [2, 4], '일반'), ('거미줄 해골 쿠키', d_webcookie, [4, 3], '일반'), ('해골 박쥐 수프', d_batsoup, [3, 1], '일반'),
  ('박쥐 모자 머핀', d_batmuffin, [1, 5], '일반'), ('도깨비불 마녀 차', d_wisptea, [5, 8], '일반'), ('도깨비불 사과 사이다', d_cider, [8, 10], '일반'), ('독사과 호박 수프', d_applesoup, [10, 0], '일반'),
  ('마녀의 대솥 스튜', d_cauldron, [5, 1, 3], '특별'), ('유령 파티 푸딩', d_trifle, [2, 4, 8], '특별'), ('뱀파이어 만찬 젤리', d_vampjelly, [11, 9, 6], '특별'), ('잭의 사탕 사과', d_candyapple, [0, 7, 10], '특별'),
  ('열두 밤 만찬', d_feast, list(range(12)), '만찬')]
if __name__ == '__main__':
    icons = []
    for nm, fn, rec, kind in DISHES: s = Icon(); fn(s); icons.append(s.image())
    S = Image.new('RGBA', (32 * len(icons), 32), (0, 0, 0, 0))
    for i, c in enumerate(icons): S.alpha_composite(c, (i * 32, 0))
    S.save(os.path.join(OUT, 'seed_dishes.png'))
    json.dump([{ 'name': nm, 'kind': kind, 'fruits': [FR[i] for i in rec] } for nm, fn, rec, kind in DISHES], open(os.path.join(OUT, 'seed_dishes.json'), 'w'), ensure_ascii=False, indent=1)
    fruits = Image.open(os.path.join(OUT, 'seed_fruits.png')).convert('RGBA')
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 14) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 12) if os.path.exists(fb) else F
    cw, chh, cols = 270, 150, 4; rows = math.ceil(16 / cols)
    pv = Image.new('RGB', (cw * cols + 20, 50 + chh * rows + 40 + 190), (26, 18, 34)); d = ImageDraw.Draw(pv)
    d.text((14, 14), '할로윈 요리 17종 · 일반 12 (열매 2) · 특별 4 (열매 3) · 열두 밤 만찬 (열매 12)', font=F, fill=(255, 233, 160))
    for i, (nm, fn, rec, kind) in enumerate(DISHES[:16]):
        x, y = 10 + (i % cols) * cw, 44 + (i // cols) * chh; d.rounded_rectangle([x, y, x + cw - 10, y + chh - 10], 12, fill=(44, 32, 58) if kind == '일반' else (62, 38, 62))
        ic = icons[i].resize((96, 96), Image.NEAREST); pv.paste(ic, (x + 8, y + 10), ic)
        d.text((x + 112, y + 18), nm, font=F, fill=(255, 240, 200)); d.text((x + 112, y + 38), kind + ' 요리', font=F2, fill=(200, 170, 230) if kind == '일반' else (255, 170, 210))
        for j, fi in enumerate(rec):
            f = fruits.crop((fi * 32, 0, fi * 32 + 32, 32)).resize((40, 40), Image.NEAREST); pv.paste(f, (x + 112 + j * 46, y + 62), f)
            w = FR[fi].split(' '); l1, l2 = (' '.join(w[:-1]), w[-1]) if len(w) > 1 else (w[0], ''); F9 = ImageFont.truetype(fb, 10)
            d.text((x + 132 + j * 46, y + 110), l1, font=F9, fill=(190, 170, 220), anchor='mm'); d.text((x + 132 + j * 46, y + 123), l2, font=F9, fill=(190, 170, 220), anchor='mm')
    y = 44 + rows * chh + 10; d.rounded_rectangle([10, y, cw * cols, y + 180], 12, fill=(70, 50, 30))
    ic = icons[16].resize((128, 128), Image.NEAREST); pv.paste(ic, (24, y + 24), ic); d.text((170, y + 24), '열두 밤 만찬 (반 전체 열매 12종을 모두 모아야 해요)', font=F, fill=(255, 233, 160))
    for j in range(12):
        f = fruits.crop((j * 32, 0, j * 32 + 32, 32)).resize((48, 48), Image.NEAREST); pv.paste(f, (170 + j * 72, y + 70), f)
    pv.save(os.path.join(OUT, 'seed_dishes_preview.png')); print('dishes ok', S.size, pv.size)
