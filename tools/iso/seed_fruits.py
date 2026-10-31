# 마법 씨앗 대회: 할로윈 식물 12종에서만 나오는 열매 12종 (아이템 아이콘 32×32)
#   게임 아이콘 그림체: 모양마다 입체 음영 5단(왼쪽 위 빛) · 반짝 · 테두리는 그 색의 아주 어두운 톤
#   python3 seed_fruits.py → out/seed_fruits.png (32×32 × 12) · out/seed_fruits_preview.png
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
N, SS = 32, 4
def hx(c): return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
class Icon:
    def __init__(s): s.rgb = np.zeros((N, N, 3)); s.a = np.zeros((N, N), bool); s.own = np.full((N, N), -1); s.cols = []
    def mask(s, fn):   # 4배로 그려서 줄이면 둥근 모양이 매끈해요
        im = Image.new('L', (N * SS, N * SS), 0); d = ImageDraw.Draw(im); fn(d, SS)
        return np.array(im.resize((N, N), Image.BOX)) > 110
    def shade(s, m, c, gloss=True, flat=False, k=1.0):   # 입체 음영 5단
        if not m.any(): return m
        base = hx(c); pal = [base * .5, base * .72, base, np.minimum(255, base * 1.12 + 22), np.minimum(255, base * 1.25 + 60)]
        if flat: tone = np.full((N, N), 2)
        else:
            d = ndimage.distance_transform_edt(m); dn = d / max(1, d.max()); g = ndimage.gaussian_filter(d, 1.0); gy, gx = np.gradient(g)
            lt = -(gx + gy) / (np.hypot(gx, gy) + 1e-6); YY, XX = np.mgrid[0:N, 0:N]; ys, xs = np.nonzero(m)
            pos = -((XX - xs.mean()) / (np.ptp(xs) + 1) + (YY - ys.mean()) / (np.ptp(ys) + 1))   # 왼쪽 위가 밝게
            v = .42 * dn + .22 * lt * (1 - dn) + .55 * pos * k + .32; tone = np.clip(np.floor(v * 4.2), 0, 3).astype(int)
            if gloss:
                hp = (m & (dn > .35) & (pos > .28)); tone[hp] = 4
        for t in range(5): sel = m & (tone == t); s.rgb[sel] = pal[t]
        s.a |= m; s.cols.append(base); s.own[m] = len(s.cols) - 1; return m
    def fill(s, m, c): s.rgb[m] = hx(c); s.a |= m; s.cols.append(hx(c)); s.own[m] = len(s.cols) - 1
    def px(s, x, y, c): s.rgb[y, x] = hx(c); s.a[y, x] = True; s.cols.append(hx(c)); s.own[y, x] = len(s.cols) - 1
    def image(s):   # 바깥 테두리: 이웃한 색을 아주 어둡게
        out = np.zeros((N, N, 4), np.uint8); out[s.a, :3] = np.clip(s.rgb[s.a], 0, 255); out[s.a, 3] = 255
        ring = ndimage.binary_dilation(s.a) & ~s.a
        for y, x in zip(*np.nonzero(ring)):
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                Y, X = y + dy, x + dx
                if 0 <= Y < N and 0 <= X < N and s.a[Y, X]:
                    c = s.cols[s.own[Y, X]] if s.own[Y, X] >= 0 else s.rgb[Y, X]; out[y, x, :3] = np.clip(c * np.array([.26, .22, .3]) + 6, 0, 255); out[y, x, 3] = 255; break
        return Image.fromarray(out)
E = lambda x0, y0, x1, y1: (lambda d, k: d.ellipse([x0 * k, y0 * k, x1 * k, y1 * k], fill=255))
PG = lambda pts: (lambda d, k: d.polygon([(x * k, y * k) for x, y in pts], fill=255))
LN = lambda pts, w: (lambda d, k: d.line([(x * k, y * k) for x, y in pts], fill=255, width=int(w * k)))
def inner_line(s, m_base, pts, c, w=1):   # 모양 안쪽 선 (호박 골 같은 것)
    m = s.mask(LN(pts, w)) & m_base; s.rgb[m] = hx(c)
def jack(s):
    m = s.shade(s.mask(E(5, 9, 27, 28)), '#F07A18')
    for pts in (((11, 10), (9.5, 18), (11, 27)), ((21, 10), (22.5, 18), (21, 27)), ((16, 9.5), (16, 28))): inner_line(s, m, pts, '#B4560E')
    s.shade(s.mask(LN([(16, 10), (16.5, 6), (19, 3.5)], 2.6)), '#5A7A22', gloss=False)
    for pts, c in ((((8, 17), (12, 13), (13.5, 18)), '#FFC23A'), (((24, 17), (20, 13), (18.5, 18)), '#FFC23A'), (((8, 21), (24, 21), (21, 25.5), (18.5, 23), (16, 26), (13.5, 23), (11, 25.5)), '#FFC23A')):
        mm = s.mask(PG(pts)) & m; s.rgb[mm] = hx(c); core = ndimage.binary_erosion(mm); s.rgb[core] = hx('#FFF2A0')
def bat(s):
    for k in (-1, 1):
        w = s.shade(s.mask(PG([(16, 15), (16 + k * 6, 8), (16 + k * 14, 10), (16 + k * 13, 15), (16 + k * 10, 13.5), (16 + k * 8.5, 18), (16 + k * 6, 15.5)])), '#5A3A7A', k=.6)
        inner_line(s, w, [(16, 15), (16 + k * 12.5, 10.5)], '#3A2050'); inner_line(s, w, [(16 + k * 6, 9), (16 + k * 8.5, 17)], '#3A2050')
    s.shade(s.mask(E(11, 11, 21, 27)), '#7A5A9A')
    for x in (13.5, 18.5): s.px(int(x), 17, '#FF4A5A')
    s.px(14, 22, '#F4F0F0'); s.px(17, 22, '#F4F0F0'); s.fill(s.mask(LN([(16, 11), (16, 7)], 1.6)), '#4A6A22')
def ghostdrop(s):
    m = s.shade(s.mask(PG([(16, 2), (20, 9), (25, 17), (25.5, 22), (22, 27), (16, 29), (10, 27), (6.5, 22), (7, 17), (12, 9)])), '#CFDCF0', k=1.1)
    for x in (12, 19): s.fill(s.mask(E(x - 1.4, 16.5, x + 1.4, 20.5)) & m, '#1E1830')
    s.fill(s.mask(E(14.3, 21.5, 17.7, 25)) & m, '#1E1830'); s.px(12, 17, '#7A88B8'); s.px(19, 17, '#7A88B8')
    for x, y in ((4, 8), (27, 6), (28, 26)): s.px(x, y, '#A8F4DA')
def skull(s):
    head = s.shade(s.mask(E(6, 4, 26, 23)), '#EEE8DA'); jaw = s.shade(s.mask(PG([(10, 19), (22, 19), (21, 27), (11, 27)])), '#DED6C4', k=.7)
    for x in (11, 21): s.fill(s.mask(E(x - 3.4, 11, x + 3.4, 18)) & head, '#2A1A24'); s.px(int(x) - 1, 13, '#E8485A')
    s.fill(s.mask(PG([(14.5, 19), (17.5, 19), (16, 21.5)])) & head, '#2A1A24')
    for x in (12.5, 15.5, 18.5): inner_line(s, jaw, [(x, 22.5), (x, 26)], '#9A9282')
    s.shade(s.mask(PG([(16, 5), (21, 1), (24, 2.5), (19, 6)])), '#5A9A3A', gloss=False)
def web(s):
    m = s.shade(s.mask(E(5, 6, 27, 29)), '#E6E4F0')
    for y in (11, 15, 19, 23): inner_line(s, m, [(4, y - 1), (16, y + 1), (28, y - 1)], '#A8A0C4')
    inner_line(s, m, [(16, 5), (16, 30)], '#A8A0C4'); inner_line(s, m, [(9, 7), (12, 29)], '#B8B0D0'); inner_line(s, m, [(23, 7), (20, 29)], '#B8B0D0')
    s.fill(s.mask(LN([(16, 1), (16, 6)], 1)), '#C8C0DC'); s.fill(s.mask(LN([(24, 1), (24, 5)], 1)), '#C8C0DC')
    sp = s.shade(s.mask(E(21.5, 4.5, 26.5, 9.5)), '#3A2A44', gloss=False)
    for dx, dy in ((-3.5, -1.5), (3.5, -1.5), (-3.5, 2), (3.5, 2)): s.fill(s.mask(LN([(24, 7), (24 + dx, 7 + dy)], 1)), '#3A2A44')
    s.px(23, 6, '#FF5A6A')
def hat(s):
    s.shade(s.mask(E(2, 20, 30, 29)), '#4A2A6A', k=.5)
    m = s.shade(s.mask(PG([(6, 24), (26, 24), (21, 13), (25, 4), (27, 2), (19, 6), (14, 11)])), '#7A44AA')
    s.fill(s.mask(PG([(8, 20), (24, 20), (25, 23.5), (7, 23.5)])) & m, '#2A1440'); s.fill(s.mask(PG([(13.5, 20), (18.5, 20), (18.5, 23.5), (13.5, 23.5)])), '#E8B030'); s.px(15, 21, '#FFE89A')
    for x, y in ((28, 9), (4, 12)): s.px(x, y, '#E6B8FF')
def eye(s):
    m = s.shade(s.mask(E(4, 5, 28, 29)), '#F2EEE6')
    for pts in (((5, 14), (9, 16), (11, 15)), ((27, 21), (23, 20)), ((8, 25), (12, 22)), ((25, 10), (22, 12))): inner_line(s, m, pts, '#D85050')
    s.shade(s.mask(E(9.5, 10, 22.5, 23)) & m, '#3A86DC'); s.fill(s.mask(E(13.5, 14, 18.5, 19)) & m, '#0C0C16'); s.fill(s.mask(E(11.5, 12, 14.5, 15)) & m, '#FFFFFF')
    s.shade(s.mask(PG([(15, 6), (19, 1), (21, 2), (17, 6)])), '#4A8A3A', gloss=False)
def candy(s):
    m = s.mask(PG([(16, 2.5), (18, 4), (26, 24), (25, 27), (7, 27), (6, 24), (14, 4)]))
    s.shade(m & s.mask(PG([(0, 0), (32, 0), (32, 13), (0, 13)])), '#FFF2DA'); s.shade(m & s.mask(PG([(0, 13), (32, 13), (32, 21), (0, 21)])), '#FF9426'); s.shade(m & s.mask(PG([(0, 21), (32, 21), (32, 32), (0, 32)])), '#FFCC34')
    for x, y in ((14, 7), (14, 8), (13, 10)): s.px(x, y, '#FFFFFF')
def wisp(s):
    m = s.shade(s.mask(PG([(16, 4), (22, 8), (26.5, 15), (25, 23), (20, 28), (16, 29.5), (12, 28), (7, 23), (5.5, 15), (10, 8)])), '#E85A1E')
    for x in (9.5, 13, 16, 19, 22.5): inner_line(s, m, [(16, 5), (x, 18), (16, 29)], '#A83A0E')
    g = s.mask(E(11.5, 13, 20.5, 24)) & m; s.fill(g, '#6AF05A'); s.fill(s.mask(E(13.5, 15, 18.5, 22)) & m, '#B8FFA8'); s.fill(s.mask(E(15, 16.5, 17, 19)) & m, '#F4FFEE')
    s.shade(s.mask(LN([(16, 5), (17, 1.5)], 2)), '#4A6A22', gloss=False)
    for x, y in ((3, 9), (29, 11), (27, 28)): s.px(x, y, '#9AFF8A')
def rosehip(s):
    s.shade(s.mask(E(6, 9, 26, 29)), '#3E2440')
    for a in range(5): r = math.radians(a * 72 - 90); s.shade(s.mask(PG([(16, 9), (16 + 7 * math.cos(r - .35), 7 + 5 * math.sin(r - .35)), (16 + 7 * math.cos(r + .35), 7 + 5 * math.sin(r + .35))])), '#2E5A2A', gloss=False)
    for x, y in ((11, 14), (12, 13), (27, 7), (5, 25)): s.px(x, y, '#D8A8FF')
def apple(s):
    m = s.shade(s.mask(lambda d, k: (d.ellipse([4 * k, 8 * k, 18 * k, 29 * k], fill=255), d.ellipse([14 * k, 8 * k, 28 * k, 29 * k], fill=255))), '#86CC2E')
    s.fill(s.mask(E(13, 7, 19, 11)) & m, '#5E9A1E'); s.shade(s.mask(LN([(16, 10), (17, 3)], 2)), '#5A4232', gloss=False); s.shade(s.mask(PG([(17, 5), (25, 1.5), (22, 7)])), '#3E8A2E', gloss=False)
    for x in (12.5, 19.5): s.fill(s.mask(E(x - 2, 15, x + 2, 19.5)) & m, '#1C2C0C')
    s.fill(s.mask(PG([(15, 20), (17, 20), (16, 22)])) & m, '#1C2C0C')
    for x in (12, 14, 16, 18, 20): s.px(x, 24, '#1C2C0C')
    s.px(27, 26, '#C0FF70'); s.px(27, 27, '#86CC2E')
def fang(s):
    m = s.shade(s.mask(E(5, 5, 27, 26)), '#C42838')
    s.fill(s.mask(PG([(9, 19), (23, 19), (22, 21.5), (10, 21.5)])) & m, '#6A0E1C')
    for x in (11.5, 20.5): s.shade(s.mask(PG([(x - 2, 20), (x + 2, 20), (x, 29)])), '#FAF6F0', k=.4)
    s.shade(s.mask(LN([(16, 6), (17, 1.5)], 2)), '#3E7A2E', gloss=False); s.px(25, 27, '#FF4A5A'); s.px(25, 28, '#A01E2E')
FRUITS = [('잭오랜턴 열매', jack, '잭오랜턴 호박꽃'), ('박쥐 날개 꼬투리', bat, '박쥐 날개 고사리'), ('유령 꿀방울', ghostdrop, '유령 난초'), ('해골 씨주머니', skull, '해골 양귀비'),
          ('거미줄 솜열매', web, '거미줄 백합'), ('마녀 모자 포자', hat, '마녀 모자 버섯'), ('눈알 열매', eye, '눈알 열매덩굴'), ('사탕옥수수 알', candy, '사탕옥수수 튤립'),
          ('도깨비불 꽈리', wisp, '도깨비불 등불초'), ('검은 장미 열매', rosehip, '검은 장미'), ('독사과', apple, '독사과 나무'), ('피빛 송곳니 열매', fang, '뱀파이어 송곳니 끈끈이')]
if __name__ == '__main__':
    icons = []
    for nm, fn, _ in FRUITS: s = Icon(); fn(s); icons.append(s.image())
    S = Image.new('RGBA', (32 * len(icons), 32), (0, 0, 0, 0))
    for i, c in enumerate(icons): S.alpha_composite(c, (i * 32, 0))
    S.save(os.path.join(OUT, 'seed_fruits.png'))
    plants = Image.open(os.path.join(OUT, 'seed_plants.png')).convert('RGBA'); ref = Image.open(os.path.join(HERE, '../../public/art/forage.png')).convert('RGBA').crop((0, 0, 32 * 6, 32))
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 14) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 12) if os.path.exists(fb) else F
    cw, chh = 180, 230; pv = Image.new('RGB', (cw * 6 + 20, 130 + chh * 2), (26, 18, 34)); d = ImageDraw.Draw(pv)
    d.text((14, 14), '식물마다 그 식물에서만 나오는 열매 (3배 크기) · 아래 줄은 게임에 있는 채집물 아이콘(비교용)', font=F, fill=(255, 233, 160))
    r3 = ref.resize((ref.width * 3, 96), Image.NEAREST); pv.paste(r3, (14, 34), r3)
    for i, (nm, fn, pn) in enumerate(FRUITS):
        x, y = 10 + (i % 6) * cw, 140 + (i // 6) * chh; d.rounded_rectangle([x, y, x + cw - 10, y + chh - 10], 12, fill=(44, 32, 58))
        p = plants.crop(((15 + i) * 40, 0, (16 + i) * 40, 56)).resize((60, 84), Image.NEAREST); pv.paste(p, (x + 6, y + 30), p)
        f = icons[i].resize((96, 96), Image.NEAREST); pv.paste(f, (x + 70, y + 18), f)
        d.text((x + (cw - 10) / 2, y + 150), nm, font=F, fill=(255, 240, 200), anchor='mm'); d.text((x + (cw - 10) / 2, y + 172), pn, font=F2, fill=(190, 170, 220), anchor='mm')
        s1 = icons[i]; pv.paste(s1, (x + (cw - 10) // 2 - 16, y + 184), s1)
    pv.save(os.path.join(OUT, 'seed_fruits_preview.png')); print('fruits ok')
