#!/usr/bin/env python3
# 시안: 겨울 뜨개질 아이템 그림 (요리 아이콘과 같은 32×32 도구 상자 · 같은 화풍)
#   목도리 · 방울 모자 · 손모아장갑 · 포근 숄 (두 색 조합) + 아바타가 입은 모습 + NPC 뜨개 인형 10 종
#   python3 tools/iso/knit_items.py <아바타 정면 png> <저장 폴더>
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dish_icons import Cv, R, H, ell, circ, rect, poly, line, edge, below, above, left, right, shift, mirror, sparkle, OL, WHITE
AV, OUTD = sys.argv[1], sys.argv[2]
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
YC = {'빨강': '#E0505A', '하양': '#F4F0E8', '파랑': '#5A8AE0', '노랑': '#F0C850', '초록': '#6AB85A', '보라': '#9A6AD8', '갈색': '#A8703A'}
def knit(c, m, col, light=True):
    """뜨개 결: 둥근 빛 + V 모양 코 무늬 (두 칸마다 어두운 V)"""
    r = R(col); c.shade(m, [r[1], r[2], r[3]] if light else [r[2], r[3], r[3]])
    for x, y in m:
        if (x % 3 == 0 and y % 2 == 0) or (x % 3 == 1 and y % 2 == 1): c.px(x, y, r[3] if (x + y) % 5 else r[4])
        elif x % 3 == 2 and y % 2 == 0: c.px(x, y, r[1])
def stripes(c, m, cols, h=3, ax='y'):
    groups = {}
    for x, y in m: groups.setdefault(((y if ax == 'y' else x) // h) % len(cols), set()).add((x, y))
    for i, g in groups.items(): knit(c, g, YC.get(cols[i], cols[i]))
# ---------- 아이콘 ----------
def scarf(c, a, b):
    loop_ = (ell(15.5, 10, 10, 5.5) - ell(15.5, 9, 6, 2.6))   # 목에 두르는 고리
    stripes(c, loop_, [a, b], 2, 'x')
    tail = poly([(17, 11), (23, 11), (24, 26), (18, 26)]); stripes(c, tail, [a, b, a], 3)
    tail2 = poly([(10, 12), (15, 12), (14, 23), (9, 23)]); stripes(c, tail2, [b, a], 3)
    for x in range(18, 25, 2): c.fill(line(x, 27, x, 30), H(YC[b] if x % 4 else YC[a]))   # 술
    for x in range(9, 15, 2): c.fill(line(x, 24, x, 27), H(YC[a]))
    sparkle(c, 27, 5)
def beanie(c, a, b):
    dome = ell(15.5, 18, 11, 10) & above(set((x, y) for x in range(32) for y in range(32)), 21); knit(c, dome, YC[a])
    brim = rect(4, 20, 27, 25); rb = R(YC[b]); c.fill(brim, rb[2]); [c.fill(rect(x, 20, x, 25), rb[3]) for x in range(5, 27, 2)]; c.fill(rect(4, 20, 27, 20), rb[1])
    pom = circ(15.5, 6, 4.2); knit(c, pom, YC[b]); [c.px(x, y, H('#ffffff')) for x, y in ((14, 4), (13, 6))]
    sparkle(c, 26, 7)
def mittens(c, a, b):
    for dx, flip in ((0, False), (13, True)):
        body = ell(9.5 + dx, 14, 5.5, 7.5) | rect(4 + dx, 14, 15 + dx, 22); th = ell((4 if not flip else 15) + dx, 15, 2.6, 3.4)
        knit(c, body | th, YC[a]); cuff = rect(4 + dx, 22, 15 + dx, 27); rb = R(YC[b]); c.fill(cuff, rb[2]); [c.fill(rect(x, 22, x, 27), rb[3]) for x in range(5 + dx, 15 + dx, 2)]
        c.fill(rect(6 + dx, 12, 13 + dx, 13), R(YC[b])[2])   # 줄무늬 한 줄
    c.fill(line(10, 28, 22, 29), H('#d8c8a0'))   # 두 짝 잇는 끈
def shawl(c, a, b):
    tri = poly([(2, 7), (30, 7), (16, 27)]); stripes(c, tri, [a, a, b], 2)
    c.fill(rect(2, 6, 30, 7), R(YC[b])[2])
    for i in range(0, 15, 2):   # 가장자리 술
        c.fill(line(2 + i, 8 + int(i * 1.35), 1 + i, 11 + int(i * 1.35)), H(YC[b])); c.fill(line(30 - i, 8 + int(i * 1.35), 31 - i, 11 + int(i * 1.35)), H(YC[b]))
    c.fill(circ(16, 13, 2.2), H('#ffd860')); c.px(15, 12, H('#fff6c0'))   # 브로치
ICONS = [('목도리', scarf), ('방울 모자', beanie), ('손모아장갑', mittens), ('포근 숄', shawl)]
# ---------- NPC 뜨개 인형 (머리 크고 몸 작은 아미구루미) ----------
def eyes(c, y=15, x0=12, x1=19, col='#2a1c38'):
    for x in (x0, x1): c.fill(rect(x, y, x, y + 1), H(col))
    c.px(x0 - 1, y + 2, H('#ff9ab0')); c.px(x1 + 1, y + 2, H('#ff9ab0'))
def head(c, skin, cx=15.5, cy=14, r=8): knit(c, ell(cx, cy, r, r - .5), skin)
def body(c, col, y0=20, w=6): knit(c, ell(15.5, y0 + 5, w, 5.5) | rect(int(15.5 - w + 1), y0, int(15.5 + w - 1), y0 + 5), col)
def arms(c, col, y=22): [knit(c, ell(x, y, 2, 3), col) for x in (8.5, 22.5)]
def feet(c, col): [knit(c, ell(x, 29, 2.6, 1.8), col) for x in (12.5, 18.5)]
def doll_leo(c):
    feet(c, '#3a3050'); body(c, '#2a3a6a'); arms(c, '#2a3a6a'); head(c, '#7a4a2a'); knit(c, ell(15.5, 8, 8, 4) | rect(8, 8, 23, 10), '#f0f0f8'); eyes(c, 15, col='#f8f0e0'); c.fill(rect(14, 18, 17, 18), H('#3a2414'))
def doll_sera(c):
    feet(c, '#f0f0f8'); body(c, '#f8f4f0'); arms(c, '#f8f4f0'); c.fill(rect(14, 22, 17, 22) | rect(15, 21, 16, 23), H('#e0505a')); head(c, '#f4d0b0'); knit(c, (ell(15.5, 10, 9, 6) - ell(15.5, 14, 6, 4)) | ell(7.5, 15, 2.2, 5) | ell(23.5, 15, 2.2, 5), '#e0402a'); eyes(c)
def doll_madeleine(c):
    feet(c, '#6a4a3a'); body(c, '#d8d0c8'); knit(c, rect(11, 21, 20, 28), '#f8f4f0'); arms(c, '#d8d0c8'); head(c, '#f0c8a8'); knit(c, ell(15.5, 9, 8, 4.5), '#a8a8b0'); knit(c, ell(15.5, 4, 5, 3.4) | rect(11, 4, 20, 7), '#ffffff'); eyes(c)
def doll_stella(c):
    feet(c, '#2a1a4a'); body(c, '#5a3a9a'); arms(c, '#5a3a9a'); head(c, '#c8885a'); knit(c, (ell(15.5, 10, 9, 6) - ell(15.5, 15, 6, 4)) | ell(7, 17, 2.4, 7) | ell(24, 17, 2.4, 7), '#f070b8'); eyes(c)
    c.fill(poly([(22, 3), (24, 7), (28, 7), (25, 10), (26, 14), (22, 11), (18, 14), (19, 10), (16, 7), (20, 7)]) & set((x, y) for x in range(32) for y in range(32)), H('#ffd860'))
def doll_nabi(c):
    feet(c, '#f8f0e0'); body(c, '#f8f0e0', w=7); head(c, '#f0a050', r=9); knit(c, ell(15.5, 17, 5, 3.4), '#f8f0e0')
    for p in (poly([(8, 9), (9, 2), (13, 7)]), poly([(23, 9), (22, 2), (18, 7)])): knit(c, p, '#f0a050')
    eyes(c, 13, 12, 19); c.px(15, 16, H('#ff7090')); c.px(16, 16, H('#ff7090')); c.fill(circ(15.5, 21, 1.5), H('#ffd040'))
def doll_batri(c):
    for side in (1, -1):
        w = poly([(15.5 + side * 4, 16), (15.5 + side * 14, 10), (15.5 + side * 13, 20), (15.5 + side * 9, 18), (15.5 + side * 6, 22)]); knit(c, w, '#5a3a8a', False)
    body(c, '#8a6ac8', 19, 5); head(c, '#9a7ad8', cy=13, r=7.5)
    for p in (poly([(10, 9), (10, 2), (14, 7)]), poly([(21, 9), (21, 2), (17, 7)])): knit(c, p, '#9a7ad8')
    eyes(c, 12, 12, 19, '#ffe060'); c.px(14, 16, WHITE); c.px(17, 16, WHITE)
def doll_kappa(c):
    feet(c, '#5aa84a'); knit(c, ell(15.5, 24, 7.5, 6), '#8a6a3a'); body(c, '#6ac85a', 20, 5); arms(c, '#6ac85a'); head(c, '#6ac85a')
    c.fill(ell(15.5, 7, 5, 2), H('#d8e8f0')); c.fill(ell(15.5, 7, 3.5, 1), H('#a8c8e0')); eyes(c); c.fill(rect(13, 18, 18, 19), H('#f0c040'))
def doll_aula(c):
    feet(c, '#f0c040'); body(c, '#8a5a3a', 18, 7); knit(c, ell(15.5, 24, 4.5, 4), '#e8d0a8'); head(c, '#8a5a3a', r=8.5)
    for p in (poly([(8, 8), (9, 3), (12, 7)]), poly([(23, 8), (22, 3), (19, 7)])): knit(c, p, '#6a4028')
    for x in (12, 19): c.fill(circ(x, 13, 3), H('#f8f0e0')); c.fill(circ(x, 13, 1.2), H('#2a1c38'))
    c.fill(poly([(14, 16), (17, 16), (15.5, 19)]), H('#f0a030')); knit(c, rect(19, 22, 25, 27), '#3a5aa8')   # 책
def doll_mandi(c):
    feet(c, '#c8945a'); knit(c, ell(15.5, 20, 7.5, 9), '#e0b07a'); arms(c, '#e0b07a', 21)
    for p in (ell(10, 7, 4.5, 3), ell(21, 7, 4.5, 3), ell(15.5, 4.5, 3.6, 4)): knit(c, p, '#5ab84a')
    eyes(c, 17, 12, 19); c.fill(rect(15, 20, 16, 20), H('#8a4a2a'))
def doll_stro(c):
    feet(c, '#6a4a2a'); body(c, '#c84a3a'); arms(c, '#e8c060'); head(c, '#e8d0a0')
    hat = ell(15.5, 8, 12, 2.6) | (ell(15.5, 6, 6.5, 4.5) & above(set((x, y) for x in range(32) for y in range(32)), 7)); knit(c, hat, '#e8b850'); c.fill(rect(9, 7, 22, 7), H('#c84a3a'))
    eyes(c, 14); c.fill(line(12, 18, 19, 18), H('#6a4a2a')); [c.px(x, 19, H('#6a4a2a')) for x in (13, 15, 17)]
DOLLS = [('레오', doll_leo), ('세라 선생님', doll_sera), ('마들렌', doll_madeleine), ('스텔라', doll_stella), ('나비', doll_nabi), ('배트리', doll_batri), ('캇파', doll_kappa), ('아울라', doll_aula), ('맨디', doll_mandi), ('스트로', doll_stro)]
def icon(fn, *a):
    c = Cv(); fn(c, *a); return c.render()
# ---------- 아바타가 입은 모습 (64×64 정면 서기 · LPC) ----------
def outline_layer(lay):
    P = lay.load(); W, H_ = lay.size; o = lay.copy(); Q = o.load()
    for y in range(H_):
        for x in range(W):
            if P[x, y][3]: continue
            if any(0 <= x + a < W and 0 <= y + b < H_ and P[x + a, y + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): Q[x, y] = OL + (255,)
    return o
def paint(lay, pts, col):
    P = lay.load()
    for x, y in pts:
        if 0 <= x < 64 and 0 <= y < 64: P[x, y] = col + (255,)
def kpaint(lay, pts, colhex):
    r = R(colhex); P = lay.load()
    for x, y in pts:
        if not (0 <= x < 64 and 0 <= y < 64): continue
        c = r[3] if ((x % 3 == 0 and y % 2 == 0) or (x % 3 == 1 and y % 2 == 1)) else r[1] if (x % 3 == 2 and y % 2 == 0) else r[2]
        P[x, y] = c + (255,)
A64 = lambda pts: {(x, y) for x, y in pts}
def e64(cx, cy, rx, ry): return {(x, y) for y in range(64) for x in range(64) if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1}
def r64(x0, y0, x1, y1): return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
def worn(base, kind, a, b):
    lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if kind in ('scarf', 'all'):
        band = r64(25, 34, 39, 37); kpaint(lay, {p for p in band if (p[0] // 2) % 2}, YC[a]); kpaint(lay, {p for p in band if not (p[0] // 2) % 2}, YC[b])
        tail = r64(35, 37, 38, 46); kpaint(lay, {p for p in tail if (p[1] // 3) % 2}, YC[a]); kpaint(lay, {p for p in tail if not (p[1] // 3) % 2}, YC[b])
        paint(lay, {(x, y) for x in (35, 37) for y in range(47, 50)}, H(YC[a])); paint(lay, {(x, y) for x in (36, 38) for y in range(47, 49)}, H(YC[b]))
    if kind in ('beanie', 'all'):
        dome = {p for p in e64(32, 22, 11.5, 11) if p[1] <= 21}; kpaint(lay, dome, YC[a]); brim = r64(20, 19, 44, 23); rb = R(YC[b]); paint(lay, brim, rb[2]); paint(lay, {(x, y) for x in range(21, 44, 2) for y in range(19, 24)}, rb[3]); paint(lay, r64(20, 19, 44, 19), rb[1])
        kpaint(lay, e64(32, 9.5, 3.6, 3.4), YC[b]); paint(lay, {(31, 8)}, (255, 255, 255))
    if kind in ('mitten', 'all'):
        for x0 in (18, 41):
            m = r64(x0, 44, x0 + 5, 49) | e64(x0 + 2.5, 49, 3, 1.6); kpaint(lay, m, YC[a]); paint(lay, r64(x0, 43, x0 + 5, 44), R(YC[b])[2])
    if kind in ('shawl', 'all'):
        tri = {(x, y) for y in range(36, 52) for x in range(64) if abs(x - 32) <= (51 - y) * 0.75 + .5}; kpaint(lay, {p for p in tri if (p[1] // 2) % 3 != 2}, YC[a]); kpaint(lay, {p for p in tri if (p[1] // 2) % 3 == 2}, YC[b])
        paint(lay, r64(21, 36, 43, 36), R(YC[b])[2]); paint(lay, {(32, 39), (31, 39), (32, 40), (31, 40)}, H('#ffd860'))
        if kind == 'all': pass
    out = base.copy(); out.alpha_composite(outline_layer(lay)); return out
# ---------- 미리보기 한 장 ----------
os.makedirs(OUTD, exist_ok=True)
base = Image.open(AV).convert('RGBA')
F = ImageFont.truetype(FB, 16); F2 = ImageFont.truetype(FB, 13); F3 = ImageFont.truetype(FB, 22)
BG, PAN, INK, SUB, GOLD = (26, 18, 38), (37, 26, 54), (241, 233, 255), (184, 168, 216), (255, 233, 160)
Wd = 1040; img = Image.new('RGB', (Wd, 1220), BG); d = ImageDraw.Draw(img)
def panel(x, y, w, h): d.rounded_rectangle([x, y, x + w, y + h], 14, fill=PAN, outline=(58, 46, 88), width=2)
d.text((24, 18), '겨울 뜨개질 · 아이템 시안 (게임 화풍 32 × 32 · 아바타 LPC)', font=F3, fill=(255, 184, 168))
# 1) 아이콘 2 색 조합
y = 60; panel(16, y, Wd - 32, 300); d.text((32, y + 12), '뜨개 옷 · 털실 10 뭉치 (숄 15 뭉치)', font=F, fill=GOLD)
combos = [('빨강', '하양'), ('파랑', '노랑')]
for i, (nm, fn) in enumerate(ICONS):
    x = 40 + i * 245
    for j, (a, b) in enumerate(combos):
        im = icon(fn, a, b).resize((96, 96), Image.NEAREST); img.paste(im, (x + j * 108, y + 50), im)
    d.text((x, y + 160), nm, font=F, fill=INK); d.text((x, y + 184), f"털실 {15 if nm == '포근 숄' else 10} 뭉치", font=F2, fill=SUB)
    d.text((x, y + 204), {'목도리': '목 칸 · 두 색 줄무늬 · 끝에 술', '방울 모자': '모자 칸 · 고무단 · 방울', '손모아장갑': '손 · 고무단 · 끈으로 이은 한 쌍', '포근 숄': '망토 칸 · 술 · 금빛 브로치'}[nm], font=F2, fill=SUB)
    d.text((x, y + 224), '빨강 · 하양 / 파랑 · 노랑', font=F2, fill=(140, 124, 170))
d.text((40, y + 262), '색은 털실 만들 때 물들인 색 (빨강 · 하양 · 파랑 · 노랑 · 초록) 두 개를 골라요', font=F2, fill=SUB)
# 2) 입은 모습
y = 376; panel(16, y, Wd - 32, 330); d.text((32, y + 12), '입은 모습 (내 아바타)', font=F, fill=GOLD)
for i, (k, nm) in enumerate([('scarf', '목도리'), ('beanie', '방울 모자'), ('mitten', '손모아장갑'), ('shawl', '포근 숄'), ('all', '다 같이')]):
    a, b = combos[0] if i % 2 == 0 else combos[1]
    if k == 'all': a, b = '빨강', '하양'
    im = worn(base, k, a, b).crop((12, 4, 52, 64)).resize((160, 240), Image.NEAREST); x = 40 + i * 196; img.paste(im, (x, y + 44), im); d.text((x + 40, y + 292), nm, font=F, fill=INK)
# 3) 인형
y = 722; panel(16, y, Wd - 32, 480); d.text((32, y + 12), 'NPC 뜨개 인형 10 종 · 털실 20 뭉치 · 방 가구', font=F, fill=GOLD)
for i, (nm, fn) in enumerate(DOLLS):
    im = icon(fn).resize((128, 128), Image.NEAREST); x = 44 + (i % 5) * 196; yy = y + 50 + (i // 5) * 210; img.paste(im, (x + 20, yy), im); d.text((x + 84 - d.textlength(nm, font=F) / 2, yy + 140), nm, font=F, fill=INK)
d.text((40, y + 456), '레오 호감도가 오르면 도안이 하나씩 열려요 · 선물받은 NPC 인형은 그 NPC가 받으면 아주 좋아해요', font=F2, fill=SUB)
img.save(os.path.join(OUTD, 'knit_items_preview.png'))
# 낱장 그림
sheet = Image.new('RGBA', (32 * 8, 32), (0, 0, 0, 0))
for i, (nm, fn) in enumerate(ICONS):
    for j, (a, b) in enumerate(combos): sheet.paste(icon(fn, a, b), ((i * 2 + j) * 32, 0))
sheet.save(os.path.join(OUTD, 'knit_icons.png'))
dsheet = Image.new('RGBA', (32 * 10, 32), (0, 0, 0, 0))
for i, (nm, fn) in enumerate(DOLLS): dsheet.paste(icon(fn), (i * 32, 0))
dsheet.save(os.path.join(OUTD, 'knit_dolls.png'))
print('ok')
