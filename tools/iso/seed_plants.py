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
    def pot(s):   # LPC 질그릇 화분
        s.d.polygon([(11, 44), (29, 44), (27, 55), (13, 55)], fill=hx('#B85A30')); s.d.polygon([(11, 44), (15, 44), (16, 55), (13, 55)], fill=hx('#D87A48')); s.d.polygon([(25, 44), (29, 44), (27, 55), (25, 55)], fill=hx('#8A3E22'))
        s.d.rectangle([9, 41, 31, 45], fill=hx('#C86A3A')); s.d.line([(9, 41), (31, 41)], fill=hx('#E8945E')); s.d.line([(9, 45), (31, 45)], fill=hx('#7A3418')); s.d.line([(24, 42), (30, 42)], fill=hx('#A85030'))
        s.d.rectangle([11, 40, 29, 41], fill=hx('#4A3022')); s.px(15, 40, '#6A4632'); s.px(23, 40, '#6A4632')
        s.d.rectangle([12, 54, 28, 55], fill=hx('#6A2E16'))
    def done(s): return outline(s.im)
def base_plant(s, h=22, n=3, c='#4E9E36', sway=.8):   # 줄기 + 잎 (꽃 아래)
    s.stem(20, 40, 40 - h, sway=sway)
    for i in range(n): y = 38 - i * (h - 4) / max(1, n); s.leaf(20, y, -7 + i, -3, c); s.leaf(21, y - 1, 7 - i, -3, sh(c, 1.08))
def glint(s, x, y, c='#FFFFFF'): s.px(x, y, c); s.px(x - 1, y, sh(c, .8)); s.px(x + 1, y, sh(c, .8)); s.px(x, y - 1, sh(c, .8)); s.px(x, y + 1, sh(c, .8))
# ---- 최종 꽃 12종 ----
def f_lily(s):    # 물방울 백합
    base_plant(s, 24)
    for a in range(6): r = math.radians(a * 60 - 90); s.poly([(20, 14), (20 + 9 * math.cos(r - .4), 14 + 9 * math.sin(r - .4)), (20 + 12 * math.cos(r), 14 + 12 * math.sin(r)), (20 + 9 * math.cos(r + .4), 14 + 9 * math.sin(r + .4))], '#58B0EC' if a % 2 else '#7CC8F6')
    s.ell(20, 14, 2.5, 2.5, '#E8F8FF')
    for x, y in ((6, 8), (34, 10), (7, 24)): s.ell(x, y, 1.2, 1.6, '#A8DEFF'); s.px(x, y - 1, '#FFFFFF')
def f_sun(s):     # 햇살 왕관꽃
    base_plant(s, 26, c='#5AA236')
    for a in range(12): r = math.radians(a * 30); s.poly([(20 + 5 * math.cos(r - .32), 13 + 5 * math.sin(r - .32)), (20 + 12 * math.cos(r), 13 + 12 * math.sin(r)), (20 + 5 * math.cos(r + .32), 13 + 5 * math.sin(r + .32))], '#FFC22E' if a % 2 else '#F6A81E', lit=False)
    s.ell(20, 13, 5, 5, '#8A5A22'); s.px(18, 11, '#C08848'); s.px(21, 12, '#5A3A16')
    s.d.polygon([(15, 3), (16, 0), (18, 3), (20, 0), (22, 3), (24, 0), (25, 3), (25, 5), (15, 5)], fill=hx('#FFE070')); s.d.line([(15, 5), (25, 5)], fill=hx('#C89A30'))
def f_bell(s):    # 노래하는 종꽃
    base_plant(s, 18)
    s.line([(20, 22), (12, 10), (7, 13)], '#3E7A2E'); s.line([(20, 22), (28, 9), (33, 12)], '#3E7A2E'); s.line([(20, 22), (20, 6)], '#3E7A2E')
    for x, y in ((7, 14), (12, 11), (33, 13), (28, 10), (20, 7)):
        s.poly([(x - 3, y + 6), (x - 2, y), (x + 2, y), (x + 3, y + 6)], '#A868E8'); s.line([(x - 3, y + 6), (x + 3, y + 6)], '#D6B0FF'); s.px(x, y + 7, '#FFE070')
    for x, y in ((3, 3), (35, 2)): s.ell(x, y + 4, 1.3, 1.1, '#FFE070'); s.line([(x + 1, y + 4), (x + 1, y)], '#FFE070'); s.line([(x + 1, y), (x + 3, y + 1)], '#FFE070')
def f_rose(s):    # 달빛 장미
    base_plant(s, 22, c='#4A8E44')
    for x, y, r in ((20, 12, 6), (12, 19, 4.5), (28, 18, 4.5)):
        s.ell(x, y, r, r, '#C4CCEC'); s.d.arc([x - r + 1.5, y - r + 1.5, x + r - 1.5, y + r - 1.5], 190, 350, fill=hx('#8A92C8')); s.d.arc([x - 1.6, y - 1.6, x + 1.6, y + 1.6], 0, 280, fill=hx('#8A92C8'))
    glint(s, 5, 5); glint(s, 35, 7); s.d.ellipse([30, 0, 37, 7], fill=hx('#F2F0D2')); s.d.ellipse([32, -1, 39, 6], fill=(0, 0, 0, 0))
def f_rainbow(s): # 무지개 꽃
    base_plant(s, 24)
    cols = ['#F25468', '#FF9A3C', '#FFDC4C', '#62D266', '#52B2F0', '#7676EE', '#BC6AEE']
    for a in range(14): r = math.radians(a * 360 / 14 - 90); s.poly([(20, 14), (20 + 12 * math.cos(r - .22), 14 + 12 * math.sin(r - .22)), (20 + 12 * math.cos(r + .22), 14 + 12 * math.sin(r + .22))], cols[a % 7], lit=False)
    s.ell(20, 14, 3, 3, '#FFF4D0')
    for i, (x, y) in enumerate(((5, 6), (35, 5), (6, 26))): glint(s, x, y, cols[i * 2])
def f_tulip(s):   # 불꽃 튤립
    base_plant(s, 22, n=2, c='#4E9A30')
    for x, y, c in ((14, 16, '#F2502A'), (26, 15, '#FF7A2A'), (20, 11, '#E8381E')):
        s.poly([(x - 4, y + 5), (x - 4, y - 2), (x - 2, y - 6), (x, y - 2), (x + 2, y - 7), (x + 4, y - 2), (x + 4, y + 5)], c); s.px(x, y - 4, '#FFD060'); s.px(x - 2, y - 3, '#FFB040')
    for x, y in ((8, 6), (32, 5)): s.px(x, y, '#FFB040'); s.px(x, y + 1, '#FF7A2A')
def f_star(s):    # 별사탕 열매나무
    s.stem(20, 40, 20, sway=0); s.line([(20, 30), (13, 24)], '#6A4A2A'); s.line([(20, 27), (27, 21)], '#6A4A2A')
    s.ell(20, 14, 12, 10, '#4A9A44'); s.ell(13, 18, 6, 5, '#3E8A3A'); s.ell(28, 17, 6, 5, '#52A44A')
    for x, y, c in ((14, 11, '#FFE070'), (24, 9, '#FFB0D0'), (20, 17, '#9AD8FF'), (29, 15, '#C8A0FF'), (11, 18, '#B8F0A0')):
        for dx, dy in ((0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)): s.px(x + dx, y + dy, c)
        s.px(x, y, '#FFFFFF')
def f_ghost(s):   # 유령 난초
    base_plant(s, 20, n=2, c='#5A8A6A')
    for x, y in ((20, 12), (12, 18), (29, 17)):
        s.ell(x, y, 4.5, 4, '#E4ECF4'); s.d.polygon([(x - 4, y + 2), (x - 5, y + 8), (x - 2, y + 5), (x, y + 9), (x + 2, y + 5), (x + 5, y + 8), (x + 4, y + 2)], fill=hx('#D0DCEA'))
        s.px(x - 1, y - 1, '#2A2440'); s.px(x + 1, y - 1, '#2A2440')
    for x, y in ((6, 6), (34, 8), (20, 3)): s.px(x, y, '#B8F0E0'); s.px(x, y + 1, '#88C8B8')
def f_pumpkin(s): # 호박 덩굴꽃
    s.stem(20, 40, 24, sway=1.5)
    for x0, y0, dx in ((20, 30, -10), (21, 26, 10), (20, 22, -8)): s.line([(x0, y0), (x0 + dx * .5, y0 - 4), (x0 + dx, y0 - 1)], '#4A8A2A'); s.px(x0 + dx, y0 - 2, '#6ABA4A')
    s.leaf(20, 34, -8, -2, '#4E9A30'); s.leaf(21, 33, 8, -3, '#5AAA3A')
    s.ell(20, 18, 7, 6, '#F08A1E'); s.line([(17, 13), (17, 23)], '#C86410'); s.line([(23, 13), (23, 23)], '#C86410'); s.d.rectangle([19, 10, 21, 12], fill=hx('#5A7A22'))
    s.px(17, 17, '#3A1E0A'); s.px(23, 17, '#3A1E0A'); s.line([(18, 20), (22, 20)], '#3A1E0A')
    s.poly([(30, 9), (33, 5), (36, 9), (33, 12)], '#FFC838'); s.poly([(5, 12), (8, 8), (11, 12), (8, 15)], '#FFC838')
def f_bat(s):     # 박쥐 날개 고사리
    s.stem(20, 40, 14, sway=.5)
    for i, (y, w) in enumerate(((34, 11), (28, 13), (21, 14), (14, 10))):
        for k in (-1, 1):
            pts = [(20, y), (20 + k * w * .5, y - 5), (20 + k * w, y - 3), (20 + k * w * .85, y + 1), (20 + k * w * .6, y - 1), (20 + k * w * .4, y + 2)]
            s.poly(pts, '#5A3A7A' if i % 2 else '#6A4A8A')
    s.px(20, 12, '#FF5A6A'); s.px(19, 12, '#FF5A6A')
def f_cotton(s):  # 구름 솜꽃
    base_plant(s, 20, n=2, c='#6A9A5A')
    for x, y, r in ((20, 12, 6), (11, 17, 5), (29, 16, 5), (16, 7, 4), (25, 7, 4)):
        s.d.ellipse([x - r, y - r, x + r, y + r], fill=hx('#D8DEF0')); s.d.ellipse([x - r, y - r, x + r - 1, y + r - 1.5], fill=hx('#F4F6FF')); s.d.ellipse([x - r + 1, y - r + 1, x - 1, y - 1], fill=hx('#FFFFFF'))
    s.px(9, 3, '#C8D8FF'); s.px(33, 4, '#C8D8FF')
def f_cactus(s):  # 수정 선인장
    s.d.rounded_rectangle([16, 16, 24, 40], 4, fill=hx('#4E9A6A')); s.d.rounded_rectangle([16, 16, 19, 40], 2, fill=hx('#6ABA82')); s.d.line([(23, 18), (23, 39)], fill=hx('#3A7A52'))
    s.d.rounded_rectangle([9, 24, 14, 34], 2, fill=hx('#4E9A6A')); s.d.rectangle([13, 30, 16, 32], fill=hx('#4E9A6A')); s.d.rounded_rectangle([26, 20, 31, 30], 2, fill=hx('#56A472')); s.d.rectangle([24, 26, 27, 28], fill=hx('#56A472'))
    for x, y in ((18, 22), (21, 28), (18, 34), (11, 28), (28, 24)): s.px(x, y, '#E8F8E8')
    for x, y, c in ((20, 11, '#9AE8FF'), (12, 20, '#FF9AD8'), (28, 16, '#C8A8FF')):
        s.d.polygon([(x, y - 5), (x + 3, y), (x, y + 4), (x - 3, y)], fill=hx(c)); s.d.polygon([(x, y - 5), (x - 3, y), (x, y)], fill=sh(c, 1.25)); s.px(x - 1, y - 2, '#FFFFFF')
FINAL = [('물방울 백합', f_lily, '#7CC8F6'), ('햇살 왕관꽃', f_sun, '#FFC22E'), ('노래하는 종꽃', f_bell, '#A868E8'), ('달빛 장미', f_rose, '#C4CCEC'),
         ('무지개 꽃', f_rainbow, '#FF7AA0'), ('불꽃 튤립', f_tulip, '#F2502A'), ('별사탕 열매나무', f_star, '#FFE070'), ('유령 난초', f_ghost, '#E4ECF4'),
         ('호박 덩굴꽃', f_pumpkin, '#F08A1E'), ('박쥐 날개 고사리', f_bat, '#6A4A8A'), ('구름 솜꽃', f_cotton, '#F4F6FF'), ('수정 선인장', f_cactus, '#9AE8FF')]
cells = []
s = P(); s.pot(); s.ell(20, 37, 3, 2.4, '#8A5AB8'); glint(s, 26, 34, '#FFE8A0'); cells.append(s.done())   # 씨앗
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
K = 4; colw = CW * K + 24; pv = Image.new('RGB', (colw * 6 + 20, 60 + (CH * K + 40) * 2 + CH * 3 + 50), (42, 30, 58)); d = ImageDraw.Draw(pv)
d.text((14, 14), '자라는 단계: 씨앗 → 새싹 → 잎 → 꽃봉오리 → 최종 꽃 (12명 모두 다른 꽃)', font=F, fill=(255, 233, 160))
for i in range(3 + 4):
    c = cells[i] if i < 3 else cells[3 + (i - 3) * 3]; b = c.resize((CW * 3, CH * 3), Image.NEAREST); pv.paste(b, (14 + i * (CW * 3 + 10), 40), b)
for i, (nm, fn, c) in enumerate(FINAL):
    b = cells[15 + i].resize((CW * K, CH * K), Image.NEAREST); x = 14 + (i % 6) * colw; y = 60 + CH * 3 + 10 + (i // 6) * (CH * K + 40)
    d.rounded_rectangle([x - 4, y - 4, x + CW * K + 4, y + CH * K + 26], 10, fill=(58, 44, 82)); pv.paste(b, (x, y), b); d.text((x + CW * K / 2, y + CH * K + 12), nm, font=F2, fill=(241, 233, 255), anchor='mm')
pv.save(os.path.join(OUT, 'seed_preview.png')); print('ok', S.size, pv.size)
