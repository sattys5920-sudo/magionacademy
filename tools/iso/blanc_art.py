# 신규 NPC 「무슈 블랑」: 100년 전 학교 식당 요리장 유령 (요리사 모자 · 콧수염 · 빨간 스카프 · 국자, 다리 대신 꼬리로 떠다녀요)
#   python3 blanc_art.py → out/blanc_map.png (64×64 칸 20개: 앞 5 · 뒤 5 · 왼쪽 5 · 오른쪽 5, npcs.png 한 줄과 같은 형식)
#                          out/blanc_portrait.png (초상화 5표정: 기본 · 웃음 · 화남 · 놀람 · 감동) · out/blanc_preview.png
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
def hx(c): return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
class Canvas:   # 모양마다 입체 음영(왼쪽 위 빛) · 테두리는 이웃 색의 어두운 톤 (열매·요리 아이콘과 같은 방식)
    def __init__(s, W, H, SS=4): s.W, s.H, s.SS = W, H, SS; s.rgb = np.zeros((H, W, 3)); s.a = np.zeros((H, W)); s.own = np.full((H, W), -1); s.cols = []
    def mask(s, fn):
        im = Image.new('L', (s.W * s.SS, s.H * s.SS), 0); d = ImageDraw.Draw(im); fn(d, s.SS); return np.array(im.resize((s.W, s.H), Image.BOX)) > 110
    def shade(s, m, c, alpha=1.0, k=1.0, gloss=True, steps=5):
        if not m.any(): return m
        base = hx(c); pal = [base * .5, base * .72, base, np.minimum(255, base * 1.1 + 24), np.minimum(255, base * 1.2 + 64)]
        d = ndimage.distance_transform_edt(m); dn = d / max(1, d.max()); YY, XX = np.mgrid[0:s.H, 0:s.W]; ys, xs = np.nonzero(m)
        pos = -((XX - xs.mean()) / (np.ptp(xs) + 1) + (YY - ys.mean()) / (np.ptp(ys) + 1))
        v = .4 * dn + .6 * pos * k + .36; tone = np.clip(np.floor(v * 4.2), 0, 3).astype(int)
        if gloss: tone[m & (dn > .4) & (pos > .3)] = 4
        for t in range(5): sel = m & (tone == t); s.rgb[sel] = pal[t] * alpha + s.rgb[sel] * (1 - alpha) * (s.a[sel, None] > 0)
        s.a[m] = np.maximum(s.a[m], alpha); s.cols.append(base); s.own[m] = len(s.cols) - 1; return m
    def fill(s, m, c, alpha=1.0): s.rgb[m] = hx(c) * alpha + s.rgb[m] * (1 - alpha); s.a[m] = np.maximum(s.a[m], alpha); s.cols.append(hx(c)); s.own[m] = len(s.cols) - 1
    def px(s, x, y, c):
        if 0 <= x < s.W and 0 <= y < s.H: s.rgb[y, x] = hx(c); s.a[y, x] = 1
    def image(s, ol=True):
        out = np.zeros((s.H, s.W, 4), np.uint8); on = s.a > 0; out[on, :3] = np.clip(s.rgb[on], 0, 255); out[on, 3] = np.clip(s.a[on] * 255, 0, 255)
        if ol:
            ring = ndimage.binary_dilation(on) & ~on
            for y, x in zip(*np.nonzero(ring)):
                for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    Y, X = y + dy, x + dx
                    if 0 <= Y < s.H and 0 <= X < s.W and on[Y, X]: c = s.cols[s.own[Y, X]] if s.own[Y, X] >= 0 else s.rgb[Y, X]; out[y, x, :3] = np.clip(c * np.array([.24, .22, .32]) + 8, 0, 255); out[y, x, 3] = 235; break
        return Image.fromarray(out)
E = lambda x0, y0, x1, y1: (lambda d, k: d.ellipse([x0 * k, y0 * k, x1 * k, y1 * k], fill=255))
PG = lambda pts: (lambda d, k: d.polygon([(x * k, y * k) for x, y in pts], fill=255))
LN = lambda pts, w: (lambda d, k: d.line([(x * k, y * k) for x, y in pts], fill=255, width=max(1, int(w * k))))
GH, HAT, SC, LAD = '#D8E6F6', '#F6F4EE', '#D83A3A', '#B8B8C8'
# ---------- 맵 캐릭터 (64×64, 발 높이 대신 꼬리 끝 ≈ y 58) ----------
def body(c, cx, top, face, t, view):   # view: down · up · side(오른쪽을 봐요) · 머리와 몸이 한 덩어리인 통통한 유령
    sway = math.sin(t * math.pi / 2) * 1.8
    blob = lambda d, k: (d.ellipse([(cx - 9) * k, (top - 1) * k, (cx + 9) * k, (top + 17) * k], fill=255), d.ellipse([(cx - 10) * k, (top + 8) * k, (cx + 10) * k, (top + 26) * k], fill=255),
                         d.polygon([(x * k, y * k) for x, y in [(cx - 9, top + 19), (cx + 9, top + 19), (cx + 6, top + 28), (cx + 2 + sway, top + 32), (cx + 3 + sway * 1.6, top + 35), (cx - 2 + sway, top + 31), (cx - 7, top + 27)]], fill=255))
    c.shade(c.mask(blob), GH, alpha=.94, k=.8)
    if view != 'up': c.fill(c.mask(PG([(cx - 6, top + 15), (cx + 6, top + 15), (cx + 7.5, top + 25), (cx - 7.5, top + 25)])), '#FFFFFF', .9)   # 앞치마
    c.shade(c.mask(lambda d, k: (d.ellipse([(cx - 8) * k, (top - 12) * k, (cx + 1) * k, (top - 2) * k], fill=255), d.ellipse([(cx - 2) * k, (top - 14) * k, (cx + 8) * k, (top - 3) * k], fill=255), d.rectangle([(cx - 6) * k, (top - 6) * k, (cx + 6) * k, (top + 1.5) * k], fill=255))), HAT, k=.7)
    c.fill(c.mask(PG([(cx - 6, top + .5), (cx + 6, top + .5), (cx + 6, top + 2), (cx - 6, top + 2)])), '#C8C4BC')
    c.shade(c.mask(PG([(cx - 7, top + 12), (cx + 7, top + 12), (cx + 2.5, top + 16.5), (cx, top + 15.5), (cx - 2.5, top + 16.5)])), SC, gloss=False)   # 스카프
    if view == 'down':
        for x in (cx - 4, cx + 3): c.px(x, top + 6, '#1E2438'); c.px(x, top + 7, '#1E2438'); c.px(x, top + 5, '#5A6488')
        c.fill(c.mask(lambda d, k: (d.ellipse([(cx - 6.5) * k, (top + 8.5) * k, (cx - .5) * k, (top + 11) * k], fill=255), d.ellipse([(cx + .5) * k, (top + 8.5) * k, (cx + 6.5) * k, (top + 11) * k], fill=255))), '#6A7088')   # 콧수염
        c.px(cx - 7, top + 8, '#6A7088'); c.px(cx + 6, top + 8, '#6A7088'); c.px(cx - 6, top + 7, '#F0B8C8'); c.px(cx + 5, top + 7, '#F0B8C8')
        c.shade(c.mask(LN([(cx + 11, top + 24 - face), (cx + 12, top + 12 - face)], 1.6)), LAD, gloss=False); c.shade(c.mask(E(cx + 9.5, top + 9 - face, cx + 14.5, top + 13.5 - face)), LAD, gloss=False)   # 국자 (오른손에 세워 들어요)
    elif view == 'side':
        c.px(cx + 4, top + 6, '#1E2438'); c.px(cx + 4, top + 7, '#1E2438'); c.px(cx + 4, top + 5, '#5A6488'); c.shade(c.mask(E(cx + 7, top + 6.5, cx + 10.5, top + 9.5)), '#E4EEFA', gloss=False)
        c.fill(c.mask(E(cx + 3, top + 9, cx + 11, top + 11.5)), '#6A7088'); c.px(cx + 11, top + 9, '#6A7088')
        c.shade(c.mask(LN([(cx + 4, top + 24 - face), (cx + 10, top + 13 - face)], 1.6)), LAD, gloss=False); c.shade(c.mask(E(cx + 8, top + 9 - face, cx + 13, top + 13.5 - face)), LAD, gloss=False)
    else:
        c.fill(c.mask(PG([(cx - 1, top + 1), (cx + 1, top + 1), (cx + 2, top + 6), (cx - 2, top + 6)])), '#C8C4BC')
def frame(view, t):
    c = Canvas(64, 64); bob = [0, -1, -2, -1][t % 4] if t else 0; top = 24 + bob
    body(c, 32, top, 0, t, view); im = c.image()
    g = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)   # 발밑 그림자 대신 희미한 빛
    gd.ellipse([25, 59, 39, 62], fill=(120, 170, 255, 45)); g.alpha_composite(im); return g
frames = [frame('down', t) for t in range(5)] + [frame('up', t) for t in range(5)]
side = [frame('side', t) for t in range(5)]
frames += [f.transpose(Image.FLIP_LEFT_RIGHT) for f in side] + side   # 왼쪽 5 · 오른쪽 5
row = Image.new('RGBA', (64 * 20, 64), (0, 0, 0, 0))
for i, f in enumerate(frames): row.alpha_composite(f, (i * 64, 0))
row.save(os.path.join(OUT, 'blanc_map.png'))
# ---------- 초상화 (가슴 위, 122×177 × 5) ----------
def portrait(expr):
    W, H = 122, 177; c = Canvas(W, H, 3); cx = 61
    c.shade(c.mask(lambda d, k: (d.ellipse([16 * k, 108 * k, 106 * k, 200 * k], fill=255))), GH, alpha=.95, k=.7)   # 어깨·몸
    c.fill(c.mask(PG([(40, 128), (82, 128), (90, 177), (32, 177)])), '#FFFFFF', .9); c.fill(c.mask(LN([(40, 128), (32, 177)], 1)), '#C8D4E4'); c.fill(c.mask(LN([(82, 128), (90, 177)], 1)), '#C8D4E4')   # 앞치마
    for y in (142, 156): c.fill(c.mask(E(57, y, 63, y + 6)), '#D8D4CC')   # 단추
    c.shade(c.mask(PG([(34, 108), (88, 108), (72, 128), (61, 122), (50, 128)])), SC, k=.8)   # 스카프
    c.shade(c.mask(PG([(56, 118), (66, 118), (70, 138), (61, 134), (52, 138)])), '#B82A2A', gloss=False)
    c.shade(c.mask(E(30, 46, 92, 116)), GH, alpha=.96)   # 얼굴
    c.shade(c.mask(lambda d, k: (d.ellipse([20 * k, 8 * k, 64 * k, 48 * k], fill=255), d.ellipse([52 * k, 2 * k, 100 * k, 46 * k], fill=255), d.ellipse([38 * k, -4 * k, 80 * k, 32 * k], fill=255), d.rectangle([32 * k, 30 * k, 90 * k, 58 * k], fill=255))), HAT, k=.7)   # 요리사 모자
    c.fill(c.mask(PG([(32, 52), (90, 52), (90, 58), (32, 58)])), '#D8D4CC')
    for x in (44, 61, 78): c.fill(c.mask(LN([(x, 20), (x + 2, 52)], 1)), '#E4E0D6')
    ey = 78; ink = '#2A3048'
    if expr == 'smile':
        for x in (46, 76): c.fill(c.mask(lambda d, k, x=x: d.arc([(x - 7) * k, (ey - 4) * k, (x + 7) * k, (ey + 6) * k], 200, 340, fill=255, width=int(2 * k))), ink)
    elif expr == 'angry':
        for x in (46, 76): c.fill(c.mask(E(x - 5, ey - 4, x + 5, ey + 5)), ink); c.fill(c.mask(E(x - 2, ey - 2, x + 1, ey + 1)), '#AAD4FF')
        c.fill(c.mask(LN([(37, 66), (53, 71)], 3)), '#5A6080'); c.fill(c.mask(LN([(85, 66), (69, 71)], 3)), '#5A6080')
        for x in (44, 78): c.fill(c.mask(E(x - 7, 86, x + 7, 92)), '#FF8A9A', .45)
    elif expr == 'surprise':
        for x in (46, 76): c.fill(c.mask(E(x - 6, ey - 7, x + 6, ey + 6)), '#FFFFFF'); c.fill(c.mask(E(x - 3, ey - 3, x + 3, ey + 3)), ink)
        c.fill(c.mask(LN([(38, 62), (52, 60)], 2.4)), '#5A6080'); c.fill(c.mask(LN([(84, 62), (70, 60)], 2.4)), '#5A6080')
    else:
        for x in (46, 76): c.fill(c.mask(E(x - 5, ey - 5, x + 5, ey + 5)), ink); c.fill(c.mask(E(x - 3, ey - 4, x, ey - 1)), '#FFFFFF')
        c.fill(c.mask(LN([(38, 66), (53, 64)], 2.4)), '#5A6080'); c.fill(c.mask(LN([(84, 66), (69, 64)], 2.4)), '#5A6080')
        if expr == 'tear':
            for x in (42, 80): c.fill(c.mask(PG([(x, 84), (x + 3, 92), (x, 98), (x - 3, 92)])), '#7AC8FF', .9); c.fill(c.mask(E(x - 1, 88, x + 1, 90)), '#FFFFFF')
            for x in (44, 78): c.fill(c.mask(E(x - 7, 86, x + 7, 92)), '#FFB0C0', .5)
    c.shade(c.mask(E(56, 83, 66, 93)), '#C8D6EC', gloss=False)   # 코
    mus = lambda d, k: [d.line([(x * k, y * k) for x, y in pts], fill=255, width=int(w * k), joint='curve') for pts, w in ((((61, 95), (52, 99), (43, 98), (36, 94), (33, 88), (36, 85)), 5), (((61, 95), (70, 99), (79, 98), (86, 94), (89, 88), (86, 85)), 5), (((58, 94), (64, 94)), 6))]
    c.shade(c.mask(mus), '#7A8098', k=.6)   # 말려 올라간 콧수염
    if expr == 'smile': c.fill(c.mask(lambda d, k: d.chord([50 * k, 98 * k, 72 * k, 112 * k], 0, 180, fill=255)), '#A84A5A')
    elif expr == 'surprise': c.fill(c.mask(E(56, 100, 66, 112)), '#5A2A3A')
    elif expr == 'angry': c.fill(c.mask(LN([(52, 106), (61, 103), (70, 106)], 2)), '#5A2A3A')
    elif expr == 'tear': c.fill(c.mask(lambda d, k: d.arc([52 * k, 100 * k, 70 * k, 110 * k], 200, 340, fill=255, width=int(2 * k))), '#5A2A3A')
    else: c.fill(c.mask(LN([(55, 104), (67, 104)], 1.6)), '#5A2A3A')
    for x, y in ((14, 40), (108, 60), (104, 24), (12, 96)): c.fill(c.mask(E(x - 1.5, y - 1.5, x + 1.5, y + 1.5)), '#C8E4FF', .7)
    return c.image()
EX = [('normal', '기본'), ('smile', '웃음'), ('angry', '화남'), ('surprise', '놀람'), ('tear', '감동')]
ports = [portrait(e) for e, _ in EX]
P = Image.new('RGBA', (122 * 5, 177), (0, 0, 0, 0))
for i, p in enumerate(ports): P.alpha_composite(p, (i * 122, 0))
P.save(os.path.join(OUT, 'blanc_portrait.png'))
# ---------- 미리보기 ----------
fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'; F = ImageFont.truetype(fb, 14); F2 = ImageFont.truetype(fb, 12)
ref = Image.open(os.path.join(HERE, '../../public/art/npcs.png')).convert('RGBA').crop((0, 64 * 7, 64 * 5, 64 * 8))   # 비교: 유령 부(Boo) 줄
pv = Image.new('RGB', (64 * 3 * 7 + 20, 60 + 177 * 2 + 80 + 64 * 3 + 40), (26, 18, 34)); d = ImageDraw.Draw(pv)
d.text((14, 14), '신규 NPC 「무슈 블랑」 · 100년 전 학교 식당 요리장 유령', font=F, fill=(255, 233, 160))
for i, p in enumerate(ports):
    b = p.resize((244, 354), Image.NEAREST); x = 14 + i * 256; pv.paste(b, (x, 44), b); d.text((x + 122, 44 + 354 + 14), EX[i][1], font=F2, fill=(241, 233, 255), anchor='mm')
y = 44 + 354 + 40; d.text((14, y), '맵 캐릭터 (3배) · 앞 · 뒤 · 왼쪽 · 오른쪽                                  비교: 유령 부', font=F2, fill=(255, 233, 160))
for j, i in enumerate((0, 2, 5, 10, 15)):
    f = row.crop((i * 64, 0, i * 64 + 64, 64)).resize((192, 192), Image.NEAREST); pv.paste(f, (14 + j * 170, y + 20), f)
r3 = ref.crop((0, 0, 64, 64)).resize((192, 192), Image.NEAREST); pv.paste(r3, (14 + 5 * 170 + 60, y + 20), r3)
pv.save(os.path.join(OUT, 'blanc_preview.png')); print('ok', row.size, P.size, pv.size)
