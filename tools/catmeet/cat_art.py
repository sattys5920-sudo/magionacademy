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

if __name__ == '__main__':
    C = [('baby1', baby(1), '아기 (부스스)'), ('baby2', baby(2), '아기 (조금 정리)'), ('baby3', baby(3), '아기 (회원)'),
         ('cheese', cheese(), '뚱보 치즈'), ('grandpa', grandpa(), '줄무늬 할배'), ('cloak', cloak(), '검은 망토'), ('calico', calico(), '방울 삼색이'), ('princess', princess(), '하얀 공주')]
    S = Image.new('RGBA', (32 * len(C), 32))
    for i, (k, im, _) in enumerate(C): im.save(f'{O}/{k}.png'); S.alpha_composite(im, (i * 32, 0))
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
