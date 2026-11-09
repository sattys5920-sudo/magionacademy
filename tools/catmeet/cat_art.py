# 달밤 고양이 집회 그림 시안: 게임 하얀 고양이(art/cast_animals.png 5 번 칸, 32 × 32)를 바탕으로 동네 고양이 다섯 · 아기 고양이 3 단계 · 가구 · 말풍선 · 털실 공
#   python3 tools/catmeet/cat_art.py → tools/catmeet/out/*.png + sheet.png
import os, random
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = D + '/out'; os.makedirs(O, exist_ok=True); ROOT = os.path.dirname(os.path.dirname(D))
OL = (47, 12, 24, 255)
def hx(s, a=255): s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)
BASE = Image.open(ROOT + '/public/art/cast_animals.png').convert('RGBA').crop((160, 0, 192, 32))
TONE = [(255, 252, 240), (250, 244, 226), (238, 228, 210), (218, 204, 190), (184, 166, 156), (140, 120, 118)]   # 밝음 → 그늘
EYE, HI, NOSE, CHEEK = (40, 16, 26), (255, 255, 255), (226, 110, 130), (240, 160, 160)

def recolor(ramp, eye=None):
    im = BASE.copy(); p = im.load()
    for y in range(32):
        for x in range(32):
            c = p[x, y]
            if not c[3]: continue
            if c[:3] in TONE: p[x, y] = hx(ramp[TONE.index(c[:3])])
            elif c[:3] == EYE and eye: p[x, y] = hx(eye)
    return im
def put(im, pts, c):
    for x, y in pts:
        if 0 <= x < im.width and 0 <= y < im.height and im.getpixel((x, y))[3] and im.getpixel((x, y))[:3] != OL[:3]: im.putpixel((x, y), hx(c) if isinstance(c, str) else c)
def outline(im):
    p = im.load(); W, H = im.size; out = im.copy(); q = out.load()
    for y in range(H):
        for x in range(W):
            if p[x, y][3] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and p[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): q[x, y] = OL
    return out
def widen(im, y0, k):   # 아랫몸을 옆으로 늘려요 (뚱보)
    out = im.copy(); top = im.crop((0, 0, 32, y0)); body = im.crop((0, y0, 32, 32)).resize((round(32 * k), 32 - y0), Image.NEAREST)
    out = Image.new('RGBA', (32, 32)); out.alpha_composite(top); out.alpha_composite(body.crop(((body.width - 32) // 2, 0, (body.width - 32) // 2 + 32, body.height)), (0, y0)); return out

def cheese():   # 뚱보 치즈: 주황 · 동글동글 · 졸린 눈
    im = recolor(['#FFD27A', '#FFC25A', '#F4A640', '#E08A30', '#C06A24', '#8A4A1A']); im = widen(im, 18, 1.3)
    put(im, [(x, y) for y in (9, 10) for x in range(13, 19, 2)], '#E08A30')   # 이마 줄
    put(im, [(10, 16), (11, 16), (19, 16), (20, 16)], '#C06A24'); put(im, [(10, 15), (11, 15), (19, 15), (20, 15)], '#FFD27A')   # 감은 눈 (반달)
    put(im, [(15, 25), (16, 25), (17, 25)], '#FFF4D8')   # 배
    return im
def grandpa():   # 줄무늬 할배: 회색 줄무늬 · 흰 눈썹 · 수염
    im = recolor(['#C8C4CC', '#B4AEB8', '#9C96A2', '#86808C', '#6A6470', '#4A4452'])
    for x in (13, 15, 17): put(im, [(x, 8), (x, 9), (x, 10)], '#4A4452')
    for y in (20, 23, 26): put(im, [(x, y) for x in range(12, 21)], '#6A6470')
    put(im, [(9, 13), (10, 13), (11, 12), (19, 12), (20, 13), (21, 13)], '#FFFFFF')   # 흰 눈썹
    put(im, [(9, 15), (10, 15), (11, 15), (19, 15), (20, 15), (21, 15)], '#4A4452'); put(im, [(10, 14), (20, 14)], '#B4AEB8')   # 가늘게 뜬 눈
    return im
def cloak():   # 검은 망토: 까만 고양이 · 노란 눈 · 보라 망토
    im = recolor(['#4A4058', '#3E3450', '#342A44', '#2A2238', '#221A2E', '#1A1424'], eye='#FFD040')
    for y in range(18, 29):
        put(im, [(x, y) for x in range(10, 23) if (x - 16) ** 2 * 3 < (y - 12) ** 2 * 4], '#6A3A8A' if y < 27 else '#4A2466')
    put(im, [(15, 18), (16, 18), (17, 18)], '#FFD040')   # 망토 고리
    return im
def calico():   # 방울 삼색이: 흰 바탕 · 주황 · 검정 무늬 · 빨간 목줄에 금방울
    im = recolor(['#FFFCF0', '#FAF4E2', '#EEE4D2', '#DACCBE', '#B8A69C', '#8C7876'])
    put(im, [(x, y) for y in range(7, 13) for x in range(9, 14)], '#F09A40'); put(im, [(x, y) for y in range(7, 12) for x in range(18, 22)], '#3A3040')
    put(im, [(x, y) for y in range(21, 25) for x in range(17, 21)], '#F09A40'); put(im, [(x, y) for y in range(23, 27) for x in range(12, 15)], '#3A3040')
    put(im, [(x, 22) for x in range(12, 20)], '#D8303A'); put(im, [(15, 23), (16, 23), (15, 24), (16, 24)], '#FFD040'); put(im, [(16, 23)], '#FFF4B0')
    return im
def princess():   # 하얀 공주: 새하얀 털 · 파란 눈 · 분홍 리본
    im = recolor(['#FFFFFF', '#FFFFFF', '#F4F2FA', '#E2DEEE', '#C6C0D8', '#9A92B4'], eye='#4A8AE0')
    g = ImageDraw.Draw(im); g.polygon([(19, 9), (23, 7), (23, 11)], fill=hx('#F48AB0'), outline=OL); g.polygon([(19, 9), (15, 7), (15, 11)], fill=hx('#F48AB0'), outline=OL); im.putpixel((19, 9), hx('#D85A8A'))
    return im
def baby(stage):   # 아기 고양이: 잿빛 갈색 · 작게 · 1 부스스 → 3 단정
    im = recolor(['#C8B8A8', '#B8A696', '#A69280', '#8E7A6A', '#76604E', '#5A4636'] if stage < 3 else ['#E2D2C0', '#D4C2AE', '#C2AE98', '#A8927C', '#8A725E', '#6A5442'])
    small = im.resize((24, 24), Image.NEAREST); out = Image.new('RGBA', (32, 32)); out.alpha_composite(small, (4, 8))
    p = out.load(); edge = [(x, y) for y in range(32) for x in range(32) if p[x, y][3]]
    def tuft(x, y, dx, dy):   # 몸 테두리에서 바깥으로 삐친 털 두 칸
        for k in (1, 2):
            q = (x + dx * k, y + dy * k)
            if 0 <= q[0] < 32 and 0 <= q[1] < 32 and not p[q][3]: p[q] = hx('#5A4636') if k == 2 else hx('#8E7A6A')
    side = lambda yy, left: (min if left else max)([e for e in edge if e[1] == yy], key=lambda e: e[0])
    T = [(side(18, True), (-1, -1)), (side(18, False), (1, -1)), (side(23, True), (-1, 0)), (side(24, False), (1, 0)), (side(29, True), (-1, 1)), (side(20, False), (1, -1)), (side(21, True), (-1, 0)), (side(28, False), (1, 1))]
    for (x, y), (dx, dy) in T[: {1: 8, 2: 3, 3: 0}[stage]]: tuft(x, y, dx, dy)
    if stage == 3: put(out, [(x, 24) for x in range(12, 20)], '#4A8AE0'); put(out, [(15, 25), (16, 25)], '#FFD040')   # 집회 회원 목줄
    return out

def window():   # 가구 「창가의 아기 고양이」 (28 × 30): 창틀 · 보름달 · 아기 고양이
    im = Image.new('RGBA', (28, 30)); g = ImageDraw.Draw(im)
    g.rectangle([1, 1, 26, 24], fill=hx('#1E2448'), outline=OL); g.ellipse([16, 4, 23, 11], fill=hx('#FFF2B8')); g.line([(13, 2), (13, 23)], fill=hx('#8A5A3A')); g.line([(2, 12), (25, 12)], fill=hx('#8A5A3A'))
    g.rectangle([0, 24, 27, 28], fill=hx('#B07A4A'), outline=OL)
    k = baby(3).crop((4, 6, 28, 32)).resize((16, 17), Image.NEAREST); im.alpha_composite(k, (6, 8)); return im
def window_empty():   # 아기 고양이가 놀러 오지 않은 날의 창가
    im = Image.new('RGBA', (28, 30)); g = ImageDraw.Draw(im)
    g.rectangle([1, 1, 26, 24], fill=hx('#1E2448'), outline=OL); g.ellipse([16, 4, 23, 11], fill=hx('#FFF2B8')); g.line([(13, 2), (13, 23)], fill=hx('#8A5A3A')); g.line([(2, 12), (25, 12)], fill=hx('#8A5A3A'))
    g.rectangle([0, 24, 27, 28], fill=hx('#B07A4A'), outline=OL); g.rectangle([9, 21, 18, 23], fill=hx('#E8DCC8'), outline=OL); return im   # 빈 방석
def shadow():   # 숨바꼭질 그림자 (24 × 12): 일렁이는 검은 웅덩이
    im = Image.new('RGBA', (24, 12)); g = ImageDraw.Draw(im); g.ellipse([0, 2, 23, 11], fill=(16, 10, 28, 150)); g.ellipse([4, 4, 19, 10], fill=(10, 6, 20, 200)); return im
def roof_bg():   # 끝 장면 배경 (320 × 180): 보름달 · 밤하늘 · 광장 둘레 지붕들 · 앞쪽 큰 지붕 (고양이들이 앉는 용마루)
    W, H = 320, 180; im = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(im); R = random.Random(7)
    top, bot = (14, 16, 44), (52, 40, 86)
    for y in range(H):
        t = min(1, y / 130); c = tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)); g.line([(0, y), (W, y)], fill=c + (255,))
    for y in range(0, 130):   # 띠 경계는 점점이 섞어요 (도트 느낌)
        if y % 13 == 12:
            for x in range(0, W, 2): im.putpixel(((x + (y // 13) % 2), y), im.getpixel((x, y + 1)))
    MX, MY, MR = 232, 46, 24
    for r, a in ((MR + 18, 18), (MR + 11, 30), (MR + 5, 48)):   # 달무리 (테두리만 겹겹이)
        lay = Image.new('RGBA', (W, H)); ImageDraw.Draw(lay).ellipse([MX - r, MY - r, MX + r, MY + r], fill=(255, 240, 190, a)); im.alpha_composite(lay)
    g = ImageDraw.Draw(im); g.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], fill=hx('#FFF4C8')); g.ellipse([MX - MR + 3, MY - MR + 2, MX + MR - 1, MY + MR - 2], fill=hx('#FFF8DC'))
    for cx, cy, r in ((-8, -6, 5), (7, 4, 4), (-3, 10, 3), (10, -10, 2), (-12, 6, 2)): g.ellipse([MX + cx - r, MY + cy - r, MX + cx + r, MY + cy + r], fill=hx('#F2E2AE'))
    for i in range(70):
        x, y = R.randrange(W), R.randrange(4, 100)
        if (x - MX) ** 2 + (y - MY) ** 2 < (MR + 18) ** 2: continue
        c = hx('#FFF4C8') if i % 3 else hx('#BEC8FF'); im.putpixel((x, y), c)
        if i % 9 == 0:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): im.putpixel((x + dx, y + dy), c[:3] + (150,))
    # 먼 지붕들 (실루엣 · 불 켜진 창)
    far = hx('#2A2350'); farL = hx('#4A4078')
    x = 0
    while x < W:
        w = R.randrange(26, 44); h = R.randrange(26, 48); base = 128; peak = base - h
        g.polygon([(x, base - h + 12), (x + w // 2, peak), (x + w, base - h + 12), (x + w, base), (x, base)], fill=far)
        g.line([(x + w // 2, peak), (x + w, base - h + 12)], fill=farL)
        if R.random() < .6: cx = x + R.randrange(4, w - 8); g.rectangle([cx, peak + 4, cx + 3, peak + 12], fill=far)   # 굴뚝
        for k in range(R.randrange(1, 4)):
            wx, wy = x + R.randrange(4, w - 6), R.randrange(base - h + 16, base - 6); g.rectangle([wx, wy, wx + 2, wy + 3], fill=hx('#FFC86A') if R.random() < .7 else hx('#3A3266'))
        x += w - R.randrange(0, 6)
    x = -10   # 가까운 집들 (조금 밝게 · 지붕 끝에 달빛)
    while x < W:
        w = R.randrange(34, 56); h = R.randrange(10, 22); base = 124; peak = base - h - 8
        g.polygon([(x, base - h), (x + w // 2, peak), (x + w, base - h), (x + w, base), (x, base)], fill=hx('#362C60')); g.line([(x, base - h), (x + w // 2, peak)], fill=hx('#5A4E8A')); g.line([(x + w // 2, peak), (x + w, base - h)], fill=hx('#6A5E9A'))
        for k in range(R.randrange(0, 3)):
            wx = x + R.randrange(6, w - 8); g.rectangle([wx, base - h + 4, wx + 3, base - h + 8], fill=hx('#FFD27A')); g.line([(wx, base - h + 6), (wx + 3, base - h + 6)], fill=hx('#C8884A'))
        x += w + R.randrange(-4, 8)
    # 왼쪽 시계탑
    g.rectangle([18, 52, 38, 128], fill=hx('#1E1A3C')); g.polygon([(14, 54), (28, 26), (42, 54)], fill=hx('#1E1A3C')); g.ellipse([22, 62, 34, 74], fill=hx('#FFE9A8')); g.ellipse([23, 63, 33, 73], outline=hx('#B89A5A'))
    g.line([(28, 68), (28, 64)], fill=hx('#3A2A2A')); g.line([(28, 68), (31, 68)], fill=hx('#3A2A2A'))
    # 앞쪽 큰 지붕: 용마루 y=122, 아래로 기와 줄
    RT = 122
    g.polygon([(0, RT + 4), (W, RT + 4), (W, H), (0, H)], fill=hx('#4A2E4E'))
    for i, y in enumerate(range(RT + 8, H, 7)):
        g.line([(0, y), (W, y)], fill=hx('#2F1A34'))
        for x in range((i % 2) * 6, W, 12): g.line([(x, y - 6), (x, y)], fill=hx('#3A2240'))
        g.line([(0, y + 1), (W, y + 1)], fill=hx('#6A4468'))
    g.rectangle([0, RT, W, RT + 5], fill=hx('#6A4A6A')); g.line([(0, RT), (W, RT)], fill=OL); g.line([(0, RT + 1), (W, RT + 1)], fill=hx('#8A6A8A')); g.line([(0, RT + 6), (W, RT + 6)], fill=OL)
    g.rectangle([286, 96, 302, RT + 2], fill=hx('#5A3A3A'), outline=OL); g.rectangle([284, 92, 304, 97], fill=hx('#6A4646'), outline=OL)   # 굴뚝
    for k in range(3): g.rectangle([288 + k * 5, 100, 290 + k * 5, 101], fill=hx('#4A2E2E'))
    # 달빛이 용마루에 비쳐요
    for x in range(150, 310, 3): im.putpixel((x, RT + 1), hx('#C8AAC0'))
    return im

def sheet_game():   # public/art/cat.png 한 장 (320 × 244): 고양이 8 칸 · 창가 2 · 말풍선 · 털실 공 · 그림자 · 끝 장면 배경
    S = Image.new('RGBA', (320, 244))
    for i, im in enumerate([baby(1), baby(2), baby(3), cheese(), grandpa(), cloak(), calico(), princess()]): S.alpha_composite(im, (i * 32, 0))
    S.alpha_composite(window(), (0, 32)); S.alpha_composite(window_empty(), (28, 32)); S.alpha_composite(paw_bubble(), (56, 32)); S.alpha_composite(yarn(), (82, 32)); S.alpha_composite(shadow(), (98, 32))
    S.alpha_composite(roof_bg(), (0, 64)); return S
def paw_bubble():   # 말풍선 「고양이 발자국 말풍선」 (26 × 18)
    im = Image.new('RGBA', (26, 18)); g = ImageDraw.Draw(im)
    g.rounded_rectangle([0, 0, 25, 13], radius=5, fill=hx('#FFF6EC'), outline=OL); g.polygon([(6, 13), (8, 17), (10, 13)], fill=hx('#FFF6EC'), outline=OL); g.line([(7, 13), (9, 13)], fill=hx('#FFF6EC'))
    for cx, cy in ((7, 7), (18, 6)):
        g.ellipse([cx - 2, cy, cx + 2, cy + 3], fill=hx('#F09A70'))
        for dx, dy in ((-2, -2), (0, -3), (2, -2)): im.putpixel((cx + dx, cy + dy), hx('#F09A70'))
    return im
def yarn():   # 털실 공 (16 × 16)
    im = Image.new('RGBA', (16, 16)); g = ImageDraw.Draw(im); g.ellipse([2, 3, 13, 14], fill=hx('#E86A8A'))
    for a, b in (((4, 6), (11, 12)), ((3, 9), (9, 4)), ((6, 13), (13, 7))): g.line([a, b], fill=hx('#FFB0C4'))
    g.line([(13, 12), (15, 15)], fill=hx('#E86A8A')); return outline(im)

# ---------- 다시 그린 고양이 (나비 그림 바탕): 32 칸 하얀 고양이를 바탕으로 하니 귀가 작고 둥글어 쥐처럼 보여서, 나비 정면 그림(64 칸 · 뾰족한 귀 · 긴 꼬리)의 털색만 바꿔 써요 ----------
import colorsys
NABI = Image.open(ROOT + '/public/art/npcs.png').convert('RGBA').crop((15, 21, 45, 59))   # 나비 정면 30 × 38
def _kind(p, x, y):
    h, s, v = colorsys.rgb_to_hsv(*[c / 255 for c in p[:3]]); h *= 360
    if 19 <= y <= 23 and 5 <= x <= 20 and (h >= 330 or h <= 12) and s > 0.55 and v < 0.65: return 'col', v   # 목줄
    if 21 <= y <= 23 and 11 <= x <= 14 and 12 < h < 40 and s >= 0.55: return 'bell', v                    # 방울
    if v < 0.45 and s > 0.3 and (h >= 330 or h <= 12): return 'ol', v
    if v < 0.22: return 'ol', v
    if 12 < h < 40 and s >= 0.55 and v >= 0.55: return 'pat', v
    return 'fur', v
def _mul(c, k): return tuple(max(0, min(255, int(x * k))) for x in c)
def nabi_cat(fur, pat, col=None, eye=None, extra=None, scale=32 / 38, fat=1.0):
    im = NABI.copy(); p = im.load(); F, P = hx(fur)[:3], hx(pat)[:3]
    for y in range(im.height):
        for x in range(im.width):
            q = p[x, y]
            if not q[3]: continue
            k, v = _kind(q, x, y)
            if k == 'fur': p[x, y] = _mul(F, v / 0.99) + (255,)
            elif k == 'pat': p[x, y] = _mul(P, v / 0.98) + (255,)
            elif k == 'col': p[x, y] = (_mul(hx(col)[:3], v / 0.6) + (255,)) if col else _mul(F, 0.8) + (255,)
            elif k == 'bell': p[x, y] = (hx('#FFD040') if col else _mul(F, 0.9) + (255,))
    if eye:
        for x, y in ((7, 11), (8, 11), (7, 12), (8, 12), (16, 11), (17, 11), (16, 12), (17, 12)): p[x, y] = hx(eye)   # 두 칸씩 (줄일 때 한 줄이 빠져도 보이게)
    if extra: extra(im)
    if fat != 1.0:
        top = im.crop((0, 0, im.width, 17)); body = im.crop((0, 17, im.width, im.height)); bw = round(im.width * fat)
        w = Image.new('RGBA', (bw, im.height)); w.alpha_composite(top, ((bw - im.width) // 2, 0)); w.alpha_composite(body.resize((bw, body.height), Image.NEAREST), (0, 17)); im = w
    W, H = round(im.width * scale), round(im.height * scale); W = min(W, 32)
    sm = im.resize((W, H), Image.NEAREST); out = Image.new('RGBA', (32, 32)); out.alpha_composite(sm, ((32 - W) // 2, 32 - H)); return out
def _on(im, pts, c):
    for x, y in pts:
        if 0 <= x < im.width and 0 <= y < im.height and im.getpixel((x, y))[3]: im.putpixel((x, y), hx(c))
def cheese(): return nabi_cat('#FFE2A8', '#F49A30', '#4A8AE0', fat=1.25)
def grandpa():
    def ex(im):
        for y in (25, 28, 31): _on(im, [(x, y) for x in range(6, 20) if im.getpixel((x, y))[:3] != OL[:3]], '#8A8492')
        for x in (10, 12, 14): _on(im, [(x, 4), (x, 5), (x, 6)], '#5A5462')
        _on(im, [(7, 10), (8, 10), (9, 10), (16, 10), (17, 10), (18, 10)], '#FFFFFF')   # 흰 눈썹
    return nabi_cat('#D2CED6', '#8A8492', None, extra=ex)
def cloak():
    def ex(im):
        g = ImageDraw.Draw(im); g.polygon([(7, 20), (19, 20), (23, 34), (3, 34)], fill=hx('#6A3A8A'), outline=hx('#3A1A52')); _on(im, [(12, 20), (13, 20), (14, 20)], '#FFD040')
    return nabi_cat('#4A4058', '#2E2640', None, eye='#FFD040', extra=ex)
def calico():
    def ex(im):
        _on(im, [(x, y) for y in range(2, 10) for x in range(15, 22) if im.getpixel((x, y))[:3] != OL[:3]], '#3A3040')
        _on(im, [(x, y) for y in range(26, 30) for x in range(14, 19)], '#3A3040'); _on(im, [(x, y) for y in range(28, 32) for x in range(6, 9)], '#F09A40')
    return nabi_cat('#FFFCF0', '#F09A40', '#D8303A', extra=ex)
def princess():
    def ex(im):
        g = ImageDraw.Draw(im); g.polygon([(15, 2), (11, 0), (11, 4)], fill=hx('#F48AB0'), outline=OL); g.polygon([(15, 2), (19, 0), (19, 4)], fill=hx('#F48AB0'), outline=OL); im.putpixel((15, 2), hx('#D85A8A'))
    return nabi_cat('#FFFFFF', '#ECE8F6', '#F48AB0', eye='#4A8AE0', extra=ex)
def baby(stage):
    fur, pat = (('#C8B8A8', '#8E7A6A') if stage < 3 else ('#E2D2C0', '#A8927C'))
    out = nabi_cat(fur, pat, '#4A8AE0' if stage == 3 else None, scale=21 / 38)
    if stage < 3:
        p = out.load(); edge = [(x, y) for y in range(32) for x in range(32) if p[x, y][3]]
        side = lambda yy, left: (min if left else max)([e for e in edge if e[1] == yy], key=lambda e: e[0])
        T = [(side(14, True), (-1, -1)), (side(14, False), (1, -1)), (side(22, True), (-1, 0)), (side(23, False), (1, 0)), (side(28, True), (-1, 1)), (side(18, False), (1, -1)), (side(19, True), (-1, 0)), (side(27, False), (1, 1))]
        for (x, y), (dx, dy) in T[: {1: 8, 2: 3}[stage]]:
            for k in (1, 2):
                q = (x + dx * k, y + dy * k)
                if 0 <= q[0] < 32 and 0 <= q[1] < 32 and not p[q][3]: p[q] = hx('#5A4636') if k == 2 else hx(pat)
    return out

# ---------- 제미나이가 그린 고양이 (tools/catmeet/gemini/cut.py 가 자른 것) · 작은 아이콘용 32 칸 ----------
_G32 = Image.open(D + '/gemini/cats32.png').convert('RGBA'); _GO = ['cheese', 'grandpa', 'cloak', 'calico', 'princess', 'baby1', 'baby2', 'baby3']
def _g(k): i = _GO.index(k); return _G32.crop((i * 32, 0, i * 32 + 32, 32))
def cheese(): return _g('cheese')
def grandpa(): return _g('grandpa')
def cloak(): return _g('cloak')
def calico(): return _g('calico')
def princess(): return _g('princess')
def baby(stage): return _g('baby' + str(stage))

if __name__ == '__main__':
    C = [('baby1', baby(1), '아기 (부스스)'), ('baby2', baby(2), '아기 (조금 정리)'), ('baby3', baby(3), '아기 (회원)'),
         ('cheese', cheese(), '뚱보 치즈'), ('grandpa', grandpa(), '줄무늬 할배'), ('cloak', cloak(), '검은 망토'), ('calico', calico(), '방울 삼색이'), ('princess', princess(), '하얀 공주')]
    S = Image.new('RGBA', (32 * len(C), 32))
    for i, (k, im, _) in enumerate(C): im.save(f'{O}/{k}.png'); S.alpha_composite(im, (i * 32, 0))
    _g64 = Image.open(D + '/gemini/cats64.png').convert('RGBA'); S64 = Image.new('RGBA', (64 * 8, 64))   # 장면 · 지붕 위 고양이는 64 칸 · 칸 순서는 게임(PIX)과 같게
    for i, k in enumerate(['baby1', 'baby2', 'baby3', 'cheese', 'grandpa', 'cloak', 'calico', 'princess']): j = _GO.index(k); S64.alpha_composite(_g64.crop((j * 64, 0, j * 64 + 64, 64)), (i * 64, 0))
    S64.save(ROOT + '/public/art/cat64.png'); S64.save(ROOT + '/public/art/cat64.webp', lossless=True)
    G = sheet_game(); G.save(ROOT + '/public/art/cat.png'); G.save(ROOT + '/public/art/cat.webp', lossless=True); roof_bg().save(O + '/roof_bg.png'); roof_bg().resize((960, 540), Image.NEAREST).save(O + '/roof_bg_x3.png')
    S.save(O + '/cats.png'); window().save(O + '/window.png'); paw_bubble().save(O + '/paw_bubble.png'); yarn().save(O + '/yarn.png')
    # 보기용 한 장
    from PIL import ImageFont
    F = ImageFont.truetype('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/galmuri11.ttf', 18)
    nabi = Image.open(ROOT + '/public/art/npcs.png').convert('RGBA').crop((0, 0, 64, 64))
    SC = 5; W = 32 * SC + 40; sheet = Image.new('RGB', (W * 4, (32 * SC + 50) * 3 + 20), (30, 24, 48)); d = ImageDraw.Draw(sheet)
    items = [(im, lab) for _, im, lab in C] + [(nabi.resize((32, 32), Image.NEAREST), '나비 (지금 그림)'), (window(), '창가의 아기 고양이'), (paw_bubble(), '고양이 발자국 말풍선'), (yarn(), '털실 공')]
    for i, (im, lab) in enumerate(items):
        x, y = (i % 4) * W + 20, (i // 4) * (32 * SC + 50) + 14; a = im.resize((im.width * SC, im.height * SC), Image.NEAREST)
        sheet.paste(a, (x + (32 * SC - a.width) // 2, y + 32 * SC - a.height), a); tw = d.textlength(lab, font=F); d.text((x + (32 * SC - tw) / 2, y + 32 * SC + 8), lab, font=F, fill=(232, 224, 248))
    sheet.save(O + '/sheet.png'); print('ok')
