# 마법 씨앗 대회: 화분 식물 그림 (LPC 그림체: 색마다 어두운 테두리 · 3단 음영 · 왼쪽 위 빛)
#   python3 seed_plants.py → out/seed_plants.png (40×56 칸 한 줄: 0 씨앗 · 1 새싹 · 2 잎 · 3~14 꽃봉오리 12종 · 15~26 최종 꽃 12종)
#                            out/seed_bg.png (온실 320×180) · out/seed_preview.png (이름 붙인 미리보기)
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
CW, CH = 40, 56
def hx(c, a=255): return tuple(c[:3]) + (a,) if not isinstance(c, str) else tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def sh(c, k): c = hx(c) if isinstance(c, str) else c; return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
def ramp(c): return sh(c, .72), hx(c), sh(c, 1.22)   # 어두움 · 기본 · 밝음
def outline(im):   # 빈칸 중 옆에 그림이 있으면 그 색을 아주 어둡게 (LPC 테두리)
    a = np.array(im); al = a[..., 3] > 0; out = a.copy(); H, W = al.shape
    for y in range(H):
        for x in range(W):
            if al[y, x]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                X, Y = x + dx, y + dy
                if 0 <= X < W and 0 <= Y < H and al[Y, X]:
                    c = a[Y, X]; out[y, x] = [int(c[0] * .32), int(c[1] * .3), int(c[2] * .36), 255]; break
    return Image.fromarray(out)
class P:   # 한 칸 그리기
    def __init__(s): s.im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def ell(s, x, y, rx, ry, c):   # 3단 음영 타원
        d0, m, l = ramp(c); s.d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=d0)
        s.d.ellipse([x - rx, y - ry, x + rx - max(1, rx * .3), y + ry - max(1, ry * .3)], fill=m)
        if rx > 1.5 and ry > 1.5: s.d.ellipse([x - rx * .6, y - ry * .7, x - rx * .1, y - ry * .2], fill=l)
    def poly(s, pts, c, lit=True):
        d0, m, l = ramp(c); s.d.polygon(pts, fill=m)
        if lit and len(pts) >= 3:
            cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
            s.d.polygon([(cx + (px - cx) * .55 - 1, cy + (py - cy) * .55 - 1) for px, py in pts], fill=l)
            s.d.line([pts[i] for i in range(len(pts)) if pts[i][0] >= cx or pts[i][1] >= cy][:2] or pts[:2], fill=d0)
    def px(s, x, y, c): s.d.point((x, y), fill=hx(c) if isinstance(c, str) else c)
    def line(s, pts, c, w=1): s.d.line(pts, fill=hx(c) if isinstance(c, str) else c, width=w)
    def leaf(s, x, y, dx, dy, c='#5AAA3A', w=2.6):
        n = 8; L = [(x + dx * t / n + (-dy) * math.sin(t / n * math.pi) * w / 6, y + dy * t / n + dx * math.sin(t / n * math.pi) * w / 6) for t in range(n + 1)]
        R = [(x + dx * t / n - (-dy) * math.sin(t / n * math.pi) * w / 6, y + dy * t / n - dx * math.sin(t / n * math.pi) * w / 6) for t in range(n, -1, -1)]
        d0, m, l = ramp(c); s.d.polygon(L + R, fill=m); s.d.polygon(L, fill=l) if False else s.d.line(L, fill=l); s.d.line(R[1:-1], fill=d0); s.d.line([(x, y), (x + dx * .85, y + dy * .85)], fill=d0)
    def stem(s, x, y0, y1, c='#3E7A2E', sway=0):
        for y in range(int(y1), int(y0) + 1): xx = round(x + sway * math.sin((y0 - y) / 7)); s.px(xx, y, c); s.px(xx + 1, y, sh(c, .75))
    def pot(s):   # 할로윈 화분: 검보라 돌 화분 + 주황 띠 + 박쥐 무늬
        s.d.polygon([(11, 44), (29, 44), (27, 55), (13, 55)], fill=hx('#3A2E4A')); s.d.polygon([(11, 44), (15, 44), (16, 55), (13, 55)], fill=hx('#54446A')); s.d.polygon([(25, 44), (29, 44), (27, 55), (25, 55)], fill=hx('#261E32'))
        s.d.rectangle([12, 48, 28, 50], fill=hx('#E87A1E')); s.d.line([(12, 48), (28, 48)], fill=hx('#FFA040')); s.d.line([(12, 50), (28, 50)], fill=hx('#A84E10'))
        for x, y in ((18, 52), (19, 53), (20, 52), (21, 53), (22, 52), (17, 53), (23, 53)): s.px(x, y, '#120C1A')   # 박쥐
        s.d.rectangle([9, 41, 31, 45], fill=hx('#4A3C5E')); s.d.line([(9, 41), (31, 41)], fill=hx('#6A5A82')); s.d.line([(9, 45), (31, 45)], fill=hx('#1E1828')); s.d.line([(24, 42), (30, 42)], fill=hx('#3A2E4A'))
        s.d.rectangle([11, 40, 29, 41], fill=hx('#1E1612')); s.px(15, 40, '#3A2A22'); s.px(23, 40, '#3A2A22')
        s.d.rectangle([12, 54, 28, 55], fill=hx('#18121F'))
    def done(s): return outline(s.im)
def base_plant(s, h=22, n=3, c='#4E9E36', sway=.8):   # 줄기 + 잎 (꽃 아래)
    s.stem(20, 40, 40 - h, sway=sway)
    for i in range(n): y = 38 - i * (h - 4) / max(1, n); s.leaf(20, y, -7 + i, -3, c); s.leaf(21, y - 1, 7 - i, -3, sh(c, 1.08))
def glint(s, x, y, c='#FFFFFF'): s.px(x, y, c); s.px(x - 1, y, sh(c, .8)); s.px(x + 1, y, sh(c, .8)); s.px(x, y - 1, sh(c, .8)); s.px(x, y + 1, sh(c, .8))
# ---- 최종 꽃 12종 (할로윈) ----
def f_jack(s):    # 잭오랜턴 호박꽃: 꽃 대신 빛나는 작은 호박 얼굴
    base_plant(s, 22, n=2, c='#4A8A2E')
    s.line([(20, 20), (12, 15)], '#4A7A22'); s.px(11, 14, '#6AAA3A'); s.line([(21, 19), (29, 13)], '#4A7A22'); s.px(30, 12, '#6AAA3A')
    s.ell(20, 13, 8, 7, '#F07A18'); s.line([(16, 7), (16, 19)], '#B85A0E'); s.line([(24, 7), (24, 19)], '#B85A0E'); s.d.rectangle([19, 4, 21, 6], fill=hx('#4A6A1E'))
    for pts in (((15, 11), (18, 9), (18, 12)), ((25, 11), (22, 9), (22, 12))): s.d.polygon(pts, fill=hx('#FFE070'))
    s.d.polygon([(15, 15), (25, 15), (23, 18), (21, 16), (19, 18), (17, 16)], fill=hx('#FFE070'))
def f_bat(s):     # 박쥐 날개 고사리
    s.stem(20, 40, 14, sway=.5)
    for i, (y, w) in enumerate(((34, 11), (28, 13), (21, 14), (14, 10))):
        for k in (-1, 1): s.poly([(20, y), (20 + k * w * .5, y - 5), (20 + k * w, y - 3), (20 + k * w * .85, y + 1), (20 + k * w * .6, y - 1), (20 + k * w * .4, y + 2)], '#5A3A7A' if i % 2 else '#6A4A8A')
    s.px(19, 12, '#FF3A4A'); s.px(21, 12, '#FF3A4A')
def f_ghost(s):   # 유령 난초: 꽃잎 끝이 유령 꼬리처럼
    base_plant(s, 20, n=2, c='#4A7A5A')
    for x, y in ((20, 11), (12, 18), (29, 17)):
        s.ell(x, y, 4.5, 4, '#E4ECF4'); s.d.polygon([(x - 4, y + 2), (x - 5, y + 8), (x - 2, y + 5), (x, y + 9), (x + 2, y + 5), (x + 5, y + 8), (x + 4, y + 2)], fill=hx('#C8D6E8'))
        s.px(x - 2, y - 1, '#1A1428'); s.px(x + 1, y - 1, '#1A1428'); s.px(x, y + 2, '#1A1428')
    for x, y in ((6, 6), (34, 7), (20, 2)): s.px(x, y, '#9AF0D0'); s.px(x, y + 1, '#5AA890')
def f_skull(s):   # 해골 양귀비: 하얀 해골 모양 꽃, 붉은 꽃술
    base_plant(s, 22, n=3, c='#3E6E2E')
    for a in range(5): r = math.radians(a * 72 - 90); s.poly([(20, 14), (20 + 11 * math.cos(r - .5), 14 + 11 * math.sin(r - .5)), (20 + 11 * math.cos(r + .5), 14 + 11 * math.sin(r + .5))], '#B01E30', lit=False)
    s.ell(20, 13, 5.5, 5, '#F0ECE0'); s.d.rectangle([17, 17, 23, 19], fill=hx('#E0DCD0'))
    s.d.ellipse([16, 11, 19, 14], fill=hx('#1A1218')); s.d.ellipse([21, 11, 24, 14], fill=hx('#1A1218')); s.px(20, 15, '#1A1218')
    for x in (18, 20, 22): s.px(x, 18, '#8A847A')
def f_web(s):     # 거미줄 백합: 흰 꽃잎에 거미줄, 작은 거미
    base_plant(s, 24, c='#4A8040')
    for a in range(6): r = math.radians(a * 60 - 90); s.poly([(20, 14), (20 + 9 * math.cos(r - .35), 14 + 9 * math.sin(r - .35)), (20 + 12 * math.cos(r), 14 + 12 * math.sin(r)), (20 + 9 * math.cos(r + .35), 14 + 9 * math.sin(r + .35))], '#E8E4F0' if a % 2 else '#D4D0E4')
    for rr in (4, 7, 10): s.d.ellipse([20 - rr, 14 - rr, 20 + rr, 14 + rr], outline=(150, 140, 175, 200))
    for a in range(6): r = math.radians(a * 60); s.line([(20, 14), (20 + 11 * math.cos(r), 14 + 11 * math.sin(r))], (150, 140, 175, 200))
    s.line([(31, 4), (31, 9)], '#C8C0D8'); s.ell(31, 10, 1.6, 1.4, '#2A1E30'); s.px(30, 10, '#FF4A5A')
    for dx in (-2, 2): s.px(31 + dx, 9, '#2A1E30'); s.px(31 + dx, 11, '#2A1E30')
def f_hat(s):     # 마녀 모자 버섯: 보랏빛 뾰족 모자 버섯 셋
    for x, h, c in ((12, 14, '#6A3A9A'), (28, 12, '#7A4AAA'), (20, 20, '#5A2A8A')):
        s.d.rectangle([x - 1, 40 - h // 2, x + 1, 40], fill=hx('#E8DCC8')); s.px(x + 1, 40 - h // 3, '#B8AC98')
        top = 40 - h // 2 - h; s.poly([(x - 7, 40 - h // 2), (x + 7, 40 - h // 2), (x + 2, top + 3), (x + 5, top)], c)
        s.d.rectangle([x - 7, 40 - h // 2 - 1, x + 7, 40 - h // 2], fill=hx('#3A1A5A')); s.d.rectangle([x - 4, 40 - h // 2 - 3, x + 3, 40 - h // 2 - 2], fill=hx('#E8B030'))
    for x, y in ((6, 10), (34, 14), (20, 4)): glint(s, x, y, '#E0B0FF')
def f_eye(s):     # 눈알 열매덩굴
    s.stem(20, 40, 12, sway=1.6)
    for y, dx in ((34, -8), (30, 8), (24, -7), (18, 7)): s.leaf(20, y, dx, -3, '#3E7A3A')
    for x, y, r, k in ((12, 22, 3.5, '#3A8AE0'), (28, 18, 3.5, '#5ABA3A'), (19, 9, 4.5, '#C83A3A'), (27, 30, 2.6, '#E0A030'), (11, 32, 2.6, '#8A4AE0')):
        s.d.ellipse([x - r, y - r, x + r, y + r], fill=hx('#F4F0E8')); s.d.arc([x - r, y - r, x + r, y + r], 30, 150, fill=hx('#C8C0B0'))
        s.d.ellipse([x - r * .5, y - r * .5, x + r * .5, y + r * .5], fill=hx(k)); s.px(round(x), round(y), '#0A0A10'); s.px(round(x - r * .3), round(y - r * .3), '#FFFFFF')
        s.px(round(x + r * .6), round(y - r * .2), '#E05050')
def f_candy(s):   # 사탕옥수수 튤립: 노랑·주황·흰 줄무늬 꽃잎
    base_plant(s, 22, n=2, c='#4E8A30')
    for x, y in ((14, 17), (26, 16), (20, 11)):
        for k, c in enumerate(('#FFF4E0', '#FF9A28', '#FFD038')):
            yy = y - 6 + k * 3; w = 2 + k * 1.3; s.d.polygon([(x - w, yy + 3), (x - w + 1, yy), (x, yy - (2 if k == 0 else 0)), (x + w - 1, yy), (x + w, yy + 3)], fill=hx(c))
        s.d.line([(x - 4, y + 3), (x + 4, y + 3)], fill=hx('#C86A10'))
def f_wisp(s):    # 도깨비불 등불초: 꽈리 등불 안에 초록 불꽃
    s.stem(20, 40, 10, sway=1.2)
    for y, dx in ((36, -8), (31, 8), (26, -7)): s.leaf(20, y, dx, -3, '#4A7A30')
    for x, y in ((12, 22), (28, 18), (19, 10)):
        s.line([(20, y - 6), (x, y - 5)], '#4A6A22'); s.poly([(x, y - 5), (x - 5, y + 1), (x - 3, y + 5), (x, y + 6), (x + 3, y + 5), (x + 5, y + 1)], '#E85A1E')
        s.line([(x, y - 4), (x, y + 5)], '#A8380E'); s.ell(x, y + 1, 1.8, 2.4, '#9AFF8A'); s.px(x, y, '#E8FFE0')
    for x, y in ((6, 8), (34, 6)): s.px(x, y, '#9AFF8A'); s.px(x, y + 1, '#4ACA5A')
def f_black(s):   # 검은 장미: 가시 줄기, 보랏빛 그림자
    s.stem(20, 40, 16, c='#2E4A26', sway=.6)
    for y in (34, 28, 22): s.px(22, y, '#A8A8A8'); s.px(18, y + 3, '#A8A8A8')
    s.leaf(20, 32, -7, -3, '#2E5A2A'); s.leaf(21, 26, 7, -3, '#34622E')
    for x, y, r in ((20, 11, 6.5), (12, 19, 4), (28, 18, 4)):
        s.d.ellipse([x - r - 1, y - r - 1, x + r + 1, y + r + 1], fill=(120, 60, 180, 90))
        s.ell(x, y, r, r, '#3A2238'); s.d.arc([x - r + 1.5, y - r + 1.5, x + r - 1.5, y + r - 1.5], 190, 350, fill=hx('#6A3A68')); s.d.arc([x - 1.6, y - 1.6, x + 1.6, y + 1.6], 0, 280, fill=hx('#7A4A7A'))
    for x, y in ((6, 6), (34, 8)): glint(s, x, y, '#C890FF')
def f_apple(s):   # 독사과 나무: 해골 무늬 초록 사과
    s.d.rectangle([19, 22, 21, 40], fill=hx('#4A3A2E')); s.d.line([(19, 22), (19, 40)], fill=hx('#6A5444')); s.line([(20, 28), (13, 23)], '#4A3A2E'); s.line([(20, 25), (27, 20)], '#4A3A2E')
    s.ell(20, 13, 12, 10, '#2E5A3A'); s.ell(12, 18, 6, 5, '#264E32'); s.ell(28, 17, 6, 5, '#346440')
    for x, y in ((13, 11), (25, 9), (20, 17), (29, 16)):
        s.ell(x, y, 2.6, 2.4, '#9AE03A'); s.px(x, y - 3, '#4A3A2E'); s.px(x - 1, y, '#1A2A0A'); s.px(x + 1, y, '#1A2A0A')
    for x, y in ((8, 26), (32, 27)): s.px(x, y, '#9AE03A'); s.px(x, y + 1, '#5AA020')
def f_fang(s):    # 뱀파이어 송곳니 끈끈이: 붉은 덫 잎에 하얀 송곳니
    s.stem(20, 40, 22, sway=.4)
    s.leaf(20, 36, -8, -2, '#3E7A2E'); s.leaf(21, 35, 8, -3, '#4A8A36')
    for x, y, f in ((20, 13, 1), (11, 23, .7), (29, 22, .7)):
        w, h = 8 * f, 5 * f
        s.poly([(x - w, y), (x, y - h), (x + w, y)], '#C02A3A'); s.poly([(x - w, y + 1), (x, y + h + 1), (x + w, y + 1)], '#A01E30')
        for k in range(-2, 3): xx = round(x + k * w / 2.6); s.px(xx, y - 1, '#FFFFFF'); s.px(xx, y + 2, '#F0F0F0')
        s.px(round(x - w * .35), round(y - h * .5), '#FFD040')
FINAL = [('잭오랜턴 호박꽃', f_jack, '#F07A18'), ('박쥐 날개 고사리', f_bat, '#6A4A8A'), ('유령 난초', f_ghost, '#E4ECF4'), ('해골 양귀비', f_skull, '#B01E30'),
         ('거미줄 백합', f_web, '#E8E4F0'), ('마녀 모자 버섯', f_hat, '#6A3A9A'), ('눈알 열매덩굴', f_eye, '#F4F0E8'), ('사탕옥수수 튤립', f_candy, '#FF9A28'),
         ('도깨비불 등불초', f_wisp, '#E85A1E'), ('검은 장미', f_black, '#3A2238'), ('독사과 나무', f_apple, '#9AE03A'), ('뱀파이어 송곳니 끈끈이', f_fang, '#C02A3A')]
cells = []
s = P(); s.pot(); s.ell(20, 37, 3, 2.4, '#3A1A4A'); s.px(19, 36, '#9A5AE0'); glint(s, 26, 34, '#9AFF8A'); cells.append(s.done())   # 씨앗 (검보라, 초록 빛)
s = P(); s.pot(); s.stem(20, 40, 32); s.leaf(20, 33, -5, -3, '#62C24A'); s.leaf(21, 33, 5, -3, '#72D25A'); cells.append(s.done())   # 새싹
s = P(); s.pot(); s.stem(20, 40, 24, sway=.8)
for y, dx in ((36, -7), (36, 7), (30, -6), (30, 6)): s.leaf(20, y, dx, -4, '#56B044' if dx < 0 else '#64BE50')
glint(s, 20, 22, '#C8FFB0'); cells.append(s.done())   # 잎
for nm, fn, c in FINAL:   # 꽃봉오리: 꽃 색이 살짝 보여요
    s = P(); s.pot(); base_plant(s, 24, n=3)
    s.ell(20, 14, 4.5, 6, c); s.d.polygon([(15, 17), (20, 21), (25, 17), (20, 15)], fill=hx('#4E9E36')); s.d.line([(17, 17), (20, 12)], fill=hx('#3E7A2E')); cells.append(s.done())
for nm, fn, c in FINAL: s = P(); s.pot(); fn(s); cells.append(s.done())
S = Image.new('RGBA', (CW * len(cells), CH), (0, 0, 0, 0))
for i, c in enumerate(cells): S.alpha_composite(c, (i * CW, 0))
S.save(os.path.join(OUT, 'seed_plants.png'))
# 미리보기: 최종 꽃 12종 4배 + 이름, 위에 자라는 단계
fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
F = ImageFont.truetype(fb, 14) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 12) if os.path.exists(fb) else F
K = 4; colw = CW * K + 24; pv = Image.new('RGB', (colw * 6 + 20, 60 + (CH * K + 40) * 2 + CH * 3 + 50), (26, 18, 34)); d = ImageDraw.Draw(pv)
d.text((14, 14), '할로윈 씨앗: 씨앗 → 새싹 → 잎 → 꽃봉오리 → 최종 꽃 (12명 모두 다른 꽃)', font=F, fill=(255, 233, 160))
for i in range(3 + 4):
    c = cells[i] if i < 3 else cells[3 + (i - 3) * 3]; b = c.resize((CW * 3, CH * 3), Image.NEAREST); pv.paste(b, (14 + i * (CW * 3 + 10), 40), b)
for i, (nm, fn, c) in enumerate(FINAL):
    b = cells[15 + i].resize((CW * K, CH * K), Image.NEAREST); x = 14 + (i % 6) * colw; y = 60 + CH * 3 + 10 + (i // 6) * (CH * K + 40)
    d.rounded_rectangle([x - 4, y - 4, x + CW * K + 4, y + CH * K + 26], 10, fill=(44, 32, 58)); pv.paste(b, (x, y), b); d.text((x + CW * K / 2, y + CH * K + 12), nm, font=F2, fill=(241, 233, 255), anchor='mm')
pv.save(os.path.join(OUT, 'seed_preview.png')); print('ok', S.size, pv.size)
# ---- 할로윈 온실 배경 320×180: 밤, 유리창 너머 보름달, 거미줄, 잭오랜턴, 보랏빛 ----
W, H = 320, 180; bg = Image.new('RGBA', (W, H), hx('#140E20')); d = ImageDraw.Draw(bg); random.seed(5)
for y in range(0, 120): t = y / 120; d.line([(0, y), (W, y)], fill=(int(24 + 30 * t), int(16 + 14 * t), int(48 + 30 * t), 255))
for _ in range(60): d.point((random.randint(0, W - 1), random.randint(0, 80)), fill=(220, 210, 255, random.randint(120, 255)))
d.ellipse([226, 14, 258, 46], fill=hx('#F4ECC8')); d.ellipse([232, 20, 238, 26], fill=hx('#DCD2AC')); d.ellipse([244, 30, 249, 35], fill=hx('#DCD2AC'))
for x in range(-20, W, 30): d.polygon([(x, 120), (x + 10, 84 - random.randint(0, 14)), (x + 20, 120)], fill=hx('#1A1A30'))   # 먼 뾰족 나무
for x, y in ((60, 40), (150, 22), (196, 50)): d.line([(x - 3, y), (x, y + 1), (x + 3, y)], fill=hx('#0A0812')); d.point((x, y), fill=hx('#0A0812'))   # 박쥐
for x in range(0, W + 1, 40): d.rectangle([x - 2, 0, x + 1, 120], fill=hx('#3A3248')); d.line([(x - 2, 0), (x - 2, 120)], fill=hx('#56506A'))   # 창틀
for y in (30, 75): d.rectangle([0, y - 1, W, y + 1], fill=hx('#3A3248'))
for x in range(0, W, 40): d.line([(x + 6, 6), (x + 14, 20)], fill=(200, 190, 255, 70))
for cx, cy, k in ((0, 0, 1), (W, 0, -1)):   # 구석 거미줄
    for r in (12, 22, 32): d.arc([cx - r, cy - r, cx + r, cy + r], 0 if k > 0 else 90, 90 if k > 0 else 180, fill=(200, 196, 220, 150))
    for a in range(0, 91, 22): rr = math.radians(a if k > 0 else 180 - a); d.line([(cx, cy), (cx + 36 * math.cos(rr), cy + 36 * math.sin(rr))], fill=(200, 196, 220, 150))
d.rectangle([0, 120, W, H], fill=hx('#2A1E2A'))
for x in range(0, W, 16): d.rectangle([x, 120, x + 15, H], fill=hx('#34262E' if (x // 16) % 2 else '#2E2028')); d.line([(x, 120), (x, H)], fill=hx('#1A1218'))
d.line([(0, 120), (W, 120)], fill=hx('#4A3640'))
for x in (34, 286):   # 양옆 잭오랜턴
    d.ellipse([x - 13, 102, x + 13, 124], fill=hx('#E06A10')); d.ellipse([x - 13, 102, x + 4, 120], fill=hx('#F08A28')); d.rectangle([x - 1, 98, x + 1, 103], fill=hx('#4A6A1E'))
    d.polygon([(x - 8, 110), (x - 4, 106), (x - 3, 111)], fill=hx('#FFE070')); d.polygon([(x + 8, 110), (x + 4, 106), (x + 3, 111)], fill=hx('#FFE070')); d.polygon([(x - 7, 115), (x + 7, 115), (x + 4, 119), (x, 116), (x - 4, 119)], fill=hx('#FFE070'))
for x, c in ((70, '#5A3A7A'), (250, '#3A5A3A')):   # 시든 화분
    d.polygon([(x - 9, 112), (x + 9, 112), (x + 6, 124), (x - 6, 124)], fill=hx('#3A2E4A')); d.line([(x, 112), (x - 5, 96), (x - 9, 98)], fill=hx(c)); d.line([(x, 112), (x + 4, 100), (x + 8, 101)], fill=hx(c))
d.rectangle([128, 120, 192, 126], fill=hx('#4A3640')); d.rectangle([132, 126, 188, 150], fill=hx('#3A2A32')); d.line([(128, 120), (192, 120)], fill=hx('#6A5260')); d.rectangle([136, 130, 184, 146], outline=hx('#2A1E24'))   # 가운데 받침대
for x, y in ((150, 140), (170, 136)): d.point((x, y), fill=hx('#E8B030'))
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
for k in range(60, 0, -4): g.ellipse([160 - k, 110 - k * .6, 160 + k, 110 + k * .6], fill=(150, 90, 220, int(30 * (1 - k / 60))))   # 받침대 위 보랏빛
bg.alpha_composite(lay); bg.save(os.path.join(OUT, 'seed_bg.png')); print('bg ok')
