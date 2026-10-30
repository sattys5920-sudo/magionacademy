# 사역마 12종 (시안 2): 팔다리 없이 둥둥 떠다니는 정령 · 둥근 몸 + 아래로 흐르는 꼬리(불꽃·안개) + 동물 귀·뿔·날개·모자
#   python3 spirit_art.py → out/spirits.png (44×46 칸 12개) · 미리보기는 인자로 경로
import os, sys, math
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from morph_obst import Spr, rect, H as C
W, Hh = 44, 46
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
def ell(cx, cy, rx, ry): return {(x, y) for x in range(W) for y in range(Hh) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
def tri(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c; out = set()
    for x in range(W):
        for y in range(Hh):
            px, py = x + .5, y + .5
            d1 = (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2); d2 = (px - x3) * (y2 - y3) - (x2 - x3) * (py - y3); d3 = (px - x1) * (y3 - y1) - (x3 - x1) * (py - y1)
            if not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0)): out.add((x, y))
    return out
def wisp(cx, top, bot, w0, bend=6, wave=0):   # 몸 아래로 흐르는 꼬리: 점점 가늘어지며 옆으로 휘어요
    out = set()
    for y in range(int(top), int(bot)):
        t = (y - top) / (bot - top); w = w0 * (1 - t) ** 1.2 + .6; x0 = cx + bend * t * t + wave * math.sin(t * 7)
        out |= {(x, y) for x in range(W) if abs(x + .5 - x0) <= w}
    return out
def spirit(base, body=(22, 19, 10, 10), tail=(18, 42, 7, 7), tailcol=None, glow=None):
    s = Spr(W, Hh); cx, cy, rx, ry = body; b = C(base) if isinstance(base, str) else base
    tc = C(tailcol) if tailcol else b
    T = wisp(cx, cy + ry * .4, tail[1], tail[2], tail[3]); s.add(T, shade(tc, .92))
    s.add({p for p in T if (p[1] - cy) > ry * 1.4 and (p[0] + p[1]) % 5 == 0}, shade(tc, 1.15))
    B = ell(cx, cy, rx, ry); s.add(B, b)
    s.add({p for p in B if ((p[0] + .5 - cx - 3) / rx) ** 2 + ((p[1] + .5 - cy - 4) / ry) ** 2 > .75}, shade(b, .8))   # 아래·오른쪽 그늘
    s.add(ell(cx - rx * .35, cy - ry * .45, rx * .35, ry * .25), shade(b, 1.18))   # 위·왼쪽 빛
    return s, B
def face(s, cx, cy, eye='#2A1830', gap=4, big=True, blush='#FF9AB8', mouth=True):
    e = C(eye)
    for ex in (cx - gap, cx + gap - 1):
        pts = [(ex, cy), (ex + 1, cy), (ex, cy + 1), (ex + 1, cy + 1)] + ([(ex, cy + 2), (ex + 1, cy + 2)] if big else [])
        s.dot(pts, e); s.dot([(ex, cy)], C('#FFFFFF'))
    if blush: s.dot([(cx - gap - 2, cy + 3), (cx - gap - 1, cy + 3), (cx + gap + 1, cy + 3), (cx + gap + 2, cy + 3)], C(blush))
    if mouth: s.dot([(cx - 1, cy + 4), (cx, cy + 5), (cx + 1, cy + 4)], e)
def spark(s, x, y, c='#FFF6B0'): s.dot([(x, y - 1), (x - 1, y), (x, y), (x + 1, y), (x, y + 1)], C(c))
OUT = []

# 1 루나울 · 달빛 늑대: 은빛 정령 + 늑대 귀 + 이마 초승달 + 보라 나방 날개
s, B = spirit('#DCE4F6', tailcol='#B8C8F0'); cx, cy = 22, 19
for sx in (-1, 1): s.layers.insert(0, (ell(cx + sx * 13, 15, 8, 9) | ell(cx + sx * 12, 26, 5, 5), C('#B89AF0'))); s.layers.insert(1, (ell(cx + sx * 13, 15, 4, 4.5), C('#E8D8FF')))
s.add(tri((13, 13), (15, 3), (20, 10)) | tri((24, 10), (29, 3), (31, 13)), C('#DCE4F6')); s.add(tri((15, 11), (16, 6), (18, 10)) | tri((26, 10), (28, 6), (29, 11)), C('#F0B8D0'))
face(s, cx, 19); s.dot([(21, 11), (22, 11), (23, 12), (20, 12)], C('#FFE070')); spark(s, 7, 30); spark(s, 38, 8); OUT.append(('루나울', '달빛 늑대', s))
# 2 이그니 · 새끼 화염룡: 불꽃 정령 + 뾰족 불꽃 머리 + 말린 뿔 + 작은 용 날개
s, B = spirit('#F2683A', tailcol='#FFB040'); cx, cy = 22, 20
for sx in (-1, 1): s.layers.insert(0, (tri((cx + sx * 6, 16), (cx + sx * 20, 8), (cx + sx * 16, 26)), C('#C84A2E')))
s.add(tri((15, 12), (18, 2), (21, 11)) | tri((19, 11), (23, 0), (26, 11)) | tri((24, 12), (29, 4), (29, 14)), C('#FFB040')); s.add(tri((19, 11), (23, 4), (25, 11)), C('#FFE070'))
s.add({(13, 12), (12, 11), (12, 10), (13, 9)} | {(31, 12), (32, 11), (32, 10), (31, 9)}, C('#F2E6C8'))
face(s, cx, 19, blush='#FFD060'); s.dot([(10, 34), (34, 32), (30, 40)], C('#FFE070')); OUT.append(('이그니', '새끼 화염룡', s))
# 3 찍찍 박사 · 사서 생쥐: 동그란 귀 + 동그란 안경 + 기울어진 마법사 모자
s, B = spirit('#D8C4A8', tailcol='#C0A88A'); cx, cy = 22, 21
s.layers.insert(0, (ell(12, 13, 5, 5) | ell(32, 13, 5, 5), C('#D8C4A8'))); s.layers.insert(1, (ell(12, 13, 3, 3) | ell(32, 13, 3, 3), C('#F0B8C8')))
s.add(tri((15, 12), (26, 0), (30, 11)) | rect(13, 10, 31, 12), C('#5A3A8A')); s.dot([(x, 10) for x in range(14, 31)], C('#F2C450')); spark(s, 25, 3, '#FFE070')
face(s, cx, 20, blush=None, mouth=True)
gl = C('#3A2A4A'); s.dot([(x, 19) for x in range(15, 21)] + [(x, 19) for x in range(23, 29)] + [(x, 23) for x in range(15, 21)] + [(x, 23) for x in range(23, 29)] + [(15, y) for y in range(19, 24)] + [(20, y) for y in range(19, 24)] + [(23, y) for y in range(19, 24)] + [(28, y) for y in range(19, 24)] + [(21, 20), (22, 20)], gl)
s.dot([(16, 20), (24, 20)], C('#C8F0FF')); OUT.append(('찍찍 박사', '사서 생쥐', s))
# 4 코멧 · 별의 양: 뭉게구름 몸 + 금빛 말린 뿔 + 별 고리 + 요정 날개
s = Spr(W, Hh); cx, cy = 22, 20
for sx in (-1, 1): s.add(ell(cx + sx * 13, 17, 6, 9), C('#BFE8FF')); s.add(ell(cx + sx * 13, 17, 3, 5), C('#E8F8FF'))
T = wisp(20, 26, 43, 7, 6); s.add(T, C('#E8ECF8'))
Bc = ell(cx, cy, 10, 9) | ell(cx - 8, cy - 4, 5, 5) | ell(cx + 8, cy - 4, 5, 5) | ell(cx - 6, cy - 9, 5, 4) | ell(cx + 5, cy - 9, 5, 4) | ell(cx - 10, cy + 3, 4, 4) | ell(cx + 10, cy + 3, 4, 4); s.add(Bc, C('#FFFFFF'))
s.add({p for p in Bc if p[1] > cy + 4}, C('#E2E8F8')); s.add(ell(cx, cy + 1, 6, 5), C('#F6E6D0'))
s.add({(12, 14), (11, 13), (11, 12), (12, 11), (13, 12)} | {(32, 14), (33, 13), (33, 12), (32, 11), (31, 12)}, C('#F2C450'))
face(s, cx, 19); [spark(s, x, y, '#FFE070') for x, y in ((14, 3), (22, 1), (30, 3))]; OUT.append(('코멧', '별의 양', s))
# 5 녹턴 · 그림자 쥐: 검보라 정령 + 둥근 귀 + 박쥐 날개 + 별 부적 + 노란 눈
s, B = spirit('#4A3A6A', tailcol='#3A2A5A'); cx, cy = 22, 20
for sx in (-1, 1): s.layers.insert(0, (tri((cx + sx * 6, 14), (cx + sx * 21, 9), (cx + sx * 18, 25)) | tri((cx + sx * 14, 24), (cx + sx * 21, 9), (cx + sx * 22, 20)), C('#2A2040')))
s.add(ell(13, 11, 5, 5) | ell(31, 11, 5, 5), C('#4A3A6A')); s.add(ell(13, 11, 3, 3) | ell(31, 11, 3, 3), C('#8A6AB0'))
face(s, cx, 18, eye='#FFE070', blush='#8A5AA8'); s.dot([(21, 26), (22, 25), (23, 26), (22, 27), (20, 26), (24, 26), (22, 24)], C('#9AD8FF')); s.dot([(22, 26)], C('#FFFFFF'))
spark(s, 6, 32, '#C8A0FF'); spark(s, 38, 34, '#C8A0FF'); OUT.append(('녹턴', '그림자 쥐', s))
# 6 피오 · 나비 토끼: 분홍 정령 + 긴 토끼 귀 + 제왕나비 날개 + 티아라
s, B = spirit('#F8D0E0', tailcol='#F0B0C8'); cx, cy = 22, 21
for sx in (-1, 1): s.layers.insert(0, (ell(cx + sx * 13, 15, 8, 8) | ell(cx + sx * 11, 27, 6, 5), C('#E86A3A'))); s.layers.insert(1, (ell(cx + sx * 13, 15, 5, 5) | ell(cx + sx * 11, 27, 3, 3), C('#FFB060')))
s.add(ell(17, 7, 2.5, 8) | ell(27, 7, 2.5, 8), C('#F8D0E0')); s.add(ell(17, 7, 1.2, 6) | ell(27, 7, 1.2, 6), C('#FF9AB8'))
s.dot([(19, 12), (20, 11), (21, 12), (22, 10), (23, 12), (24, 11), (25, 12)], C('#F2C450')); s.dot([(22, 11)], C('#FF6A9A'))
face(s, cx, 20); OUT.append(('피오', '나비 토끼', s))
# 7 모스 · 숲지기 소: 이끼 정령 + 소뿔 + 머리 위 새싹 + 이끼 무늬
s, B = spirit('#7A9A5A', tailcol='#5A7A4A'); cx, cy = 22, 20
s.add({(11, 14), (10, 13), (9, 12), (9, 11), (10, 10)} | {(33, 14), (34, 13), (35, 12), (35, 11), (34, 10)}, C('#F2E6C8'))
s.add(rect(21, 5, 22, 10), C('#5A8A3E')); s.add(ell(19, 6, 3, 2) | ell(25, 5, 3, 2), C('#9AD06A'))
s.dot([(15, 25), (16, 26), (28, 24), (29, 25), (26, 28)], C('#5A7A3A')); s.add(ell(22, 23, 4, 2.5), C('#B8A880')); s.dot([(20, 23), (24, 23)], C('#5A4A3A'))
face(s, cx, 17, blush='#E8A0A0', mouth=False); [spark(s, x, y, '#C8F0A0') for x, y in ((8, 28), (36, 30))]; OUT.append(('모스', '숲지기 소', s))
# 8 펑 · 고블린 연금술사: 라임 정령 + 갈색 두건 + 고글 + 보글보글 거품
s, B = spirit('#9AD86A', tailcol='#7AC050'); cx, cy = 22, 21
hood = ell(cx, cy - 2, 12, 11) - ell(cx, cy + 1, 9, 9); s.add(hood, C('#8A5A3A')); s.add(tri((22, 6), (34, 2), (30, 12)), C('#8A5A3A'))
s.add(tri((9, 17), (4, 13), (10, 21)) | tri((35, 17), (40, 13), (34, 21)), C('#9AD86A'))
gg = C('#C89A3A'); s.add(ell(17, 18, 3.5, 3) | ell(27, 18, 3.5, 3), gg); s.add(ell(17, 18, 2.3, 2) | ell(27, 18, 2.3, 2), C('#9AE8FF')); s.dot([(16, 17), (26, 17)], C('#FFFFFF'))
s.dot([(21, 25), (22, 26), (23, 25)], C('#2A1830')); [s.add(ell(x, y, r, r), C('#C8F0A0')) for x, y, r in ((36, 30, 2.5), (39, 25, 1.5), (34, 36, 1.5))]
OUT.append(('펑', '고블린 연금술사', s))
# 9 셀레 · 잠자리 도마뱀: 물빛 정령 + 지느러미 귀 + 잠자리 날개 + 물방울
s, B = spirit('#7ADCC8', tailcol='#5AC0E0'); cx, cy = 22, 20
for sx in (-1, 1): s.layers.insert(0, (ell(cx + sx * 14, 13, 9, 3) | ell(cx + sx * 13, 21, 8, 2.5), C('#C8F4FF'))); s.layers.insert(1, ({(x, 13) for x in range(22 + sx * 7, 22 + sx * 22, sx)}, C('#8AD8F0')))
s.add(tri((11, 18), (6, 10), (14, 14)) | tri((33, 18), (38, 10), (30, 14)), C('#5AC0E0')); s.add(tri((19, 10), (22, 4), (25, 10)), C('#5AC0E0'))
face(s, cx, 19); [s.add(ell(x, y, 1.5, 2), C('#C8F4FF')) for x, y in ((8, 32), (36, 28), (33, 38))]; OUT.append(('셀레', '잠자리 도마뱀', s))
# 10 바론 · 멧돼지 기사: 강철빛 정령 + 뿔 달린 투구 + 엄니 + 방패 문장
s, B = spirit('#A8A0B8', tailcol='#8A84A0'); cx, cy = 22, 21
helm = ell(cx, cy - 3, 11, 9) - {(x, y) for x in range(W) for y in range(Hh) if y > cy + 1}; s.add(helm, C('#C8CCD8')); s.add(rect(12, 17, 32, 18), C('#8A90A0'))
s.dot([(x, 16) for x in range(16, 29) if x % 2 == 0], C('#3A3448')); s.add(tri((11, 13), (5, 3), (14, 10)) | tri((33, 13), (39, 3), (30, 10)), C('#F2E6C8'))
s.add(rect(21, 5, 23, 9), C('#E85A5A')); face(s, cx, 21, blush=None, mouth=False); s.dot([(18, 26), (18, 25), (26, 26), (26, 25)], C('#FFFFFF'))
s.add(tri((33, 26), (40, 26), (36.5, 34)) | rect(33, 24, 40, 26), C('#3A5AC8')); s.dot([(36, 27), (37, 27), (36, 28), (37, 28)], C('#F2C450')); OUT.append(('바론', '멧돼지 기사', s))
# 11 솔라 · 해님 늑대: 황금 정령 + 햇살 갈기 + 하얀 깃털 날개 + 왕관
s, B = spirit('#F6C050', tailcol='#F2A040'); cx, cy = 22, 20
for sx in (-1, 1): s.layers.insert(0, (ell(cx + sx * 14, 18, 8, 6) | ell(cx + sx * 17, 13, 5, 4) | ell(cx + sx * 12, 24, 6, 4), C('#FFFFFF'))); s.layers.insert(1, ({(cx + sx * k, 19 + (k % 3)) for k in range(9, 21, 3)}, C('#D8E0F0')))
for a in range(0, 360, 30): r = math.radians(a); s.layers.insert(2, (ell(cx + math.cos(r) * 12, cy + math.sin(r) * 11, 2.5, 2.5), C('#FFE070')))
s.add(tri((14, 12), (16, 4), (20, 10)) | tri((24, 10), (28, 4), (30, 12)), C('#F6C050'))
s.add(rect(17, 4, 27, 6) | tri((17, 4), (17, 0), (20, 4)) | tri((20, 4), (22, -1), (24, 4)) | tri((24, 4), (27, 0), (27, 4)), C('#F2C450')); s.dot([(22, 4)], C('#E85A5A'))
face(s, cx, 19, blush='#FF9A60'); OUT.append(('솔라', '해님 늑대', s))
# 12 뿌꾸 · 유령 돼지: 하얀 유령천 + 돼지 코 + 큰 마녀 모자 (반투명은 게임에서)
s = Spr(W, Hh); cx, cy = 22, 22
body = ell(cx, cy, 11, 10) | {(x, y) for x in range(11, 34) for y in range(cy, 40) if y < 36 + 3 * math.sin(x * .9)}; s.add(body, C('#F0F0FF'))
s.add({p for p in body if p[0] > 28 or p[1] > 34}, C('#D4D8F0')); s.add(ell(22, 25, 3.5, 2.5), C('#F8B8C8')); s.dot([(21, 25), (23, 25)], C('#C86A8A'))
s.add(rect(9, 13, 35, 15), C('#4A2A5A')); s.add(tri((13, 13), (26, -1), (31, 13)), C('#4A2A5A')); s.dot([(x, 13) for x in range(14, 31)], C('#F2C450')); s.dot([(24, 9), (25, 8)], C('#C8A0FF'))
face(s, cx, 19, mouth=False); s.dot([(21, 29), (22, 30), (23, 29)], C('#2A1830')); OUT.append(('뿌꾸', '유령 돼지', s))

if __name__ == '__main__':
    ims = [(n, d, sp.render()) for n, d, sp in OUT]
    CW = W + 2; sheet = Image.new('RGBA', (CW * len(ims), Hh + 2), (0, 0, 0, 0))
    for i, (n, d, im) in enumerate(ims): sheet.paste(im, (i * CW, 0), im)
    sheet.save('out/spirits.png'); print('spirits', sheet.size)
    if len(sys.argv) > 1:
        from PIL import ImageDraw, ImageFont
        F = ImageFont.truetype(sys.argv[2], 15) if len(sys.argv) > 2 else None; F2 = ImageFont.truetype(sys.argv[2], 12) if len(sys.argv) > 2 else None
        cw, ch, cols = 230, 250, 4; pv = Image.new('RGB', (cw * cols + 20, ch * 3 + 60), (26, 18, 40)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 시안 2 · 둥둥 떠다니는 정령 12종', font=F, fill=(255, 233, 160))
        for i, (n, ds, im) in enumerate(ims):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 14, fill=(42, 30, 64), outline=(138, 96, 208), width=2)
            big = im.resize((im.width * 4, im.height * 4), Image.NEAREST); pv.paste(big, (x + (cw - 14 - big.width) // 2, y + 4), big)
            d.text((x + (cw - 14) // 2, y + 206), n, font=F, fill=(241, 233, 255), anchor='mm'); d.text((x + (cw - 14) // 2, y + 226), ds, font=F2, fill=(200, 180, 240), anchor='mm')
        pv.save(sys.argv[1])
