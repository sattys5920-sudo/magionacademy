# 사역마 12종 (시안 3): 우리 그림체(동물 NPC와 같은 LPC 음영 · 64칸)로 그린 「정령」 · 다리 없이 안개·불꽃 꼬리로 떠 있어요
#   python3 spirits_lpc.py <미리보기.png> [글꼴] → tools/iso/out/spirits_lpc.png
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beasts import Sprite, RAMP, px, hx
RAMP.update({
 'moon': ['#1A1E3A', '#343C68', '#5464A0', '#7C8EC8', '#A8B8E4', '#E0E8FF'],
 'flame': ['#3A0A06', '#7A1A0A', '#C23A12', '#E8661E', '#F8A23A', '#FFE07A'],
 'frost': ['#16304A', '#2C5478', '#4880AA', '#70AAD0', '#A4D2EE', '#E4F6FF'],
 'storm': ['#1A2030', '#30384E', '#4A546E', '#6A7690', '#94A0B8', '#C8D2E2'],
 'aqua': ['#082A3A', '#104A62', '#1A7090', '#2C98B8', '#5CC4DA', '#A8EAF4'],
 'jade': ['#0A2A1C', '#16482E', '#246A44', '#38905C', '#5CB87A', '#9CE0A8'],
 'void': ['#08060E', '#16101E', '#261C34', '#3A2C4E', '#54426C', '#76628E'],
 'ember': ['#2A0E04', '#5A2008', '#92400E', '#C86A18', '#EE9A2E', '#FFD066'],
 'astral': ['#1E0E36', '#3A1E5E', '#5A348A', '#7E52B4', '#A47ED8', '#D4BCF6'],
 'ghost': ['#3A3E58', '#5E6482', '#8890AE', '#B0B8D0', '#D4DAEA', '#F4F6FF'],
 'sun': ['#4A2A06', '#8A520C', '#C88416', '#ECAE2A', '#FAD254', '#FFF2A2'],
 'steel': ['#16181E', '#2C3038', '#484E5A', '#6A7280', '#949CAA', '#C4CAD4'],
 'antler': ['#2A1E14', '#4E3826', '#76583C', '#9A7A56', '#BEA078', '#E0C8A4'],
 'pumpkin': ['#3A1404', '#6E2A08', '#A8480E', '#D86E1C', '#F29A34', '#FFC870'],
})
def mist(cx, y0, y1, w0, bend):   # 아래로 가늘어지며 휘는 안개 꼬리 (다각형)
    L, Rr = [], []
    for k in range(13):
        t = k / 12; y = y0 + (y1 - y0) * t; w = w0 * (1 - t) ** 1.3 + .5; x = cx + bend * t * t + math.sin(t * 6) * 2 * t
        L.append((x - w, y)); Rr.append((x + w, y))
    return L + Rr[::-1]
def glowfx(a, glow, fade_from=46, sparks=()):
    a = a.copy(); h = a.shape[0]
    for y in range(fade_from, h): a[y, :, 3] = (a[y, :, 3] * max(0, 1 - (y - fade_from) / (h - fade_from) * .9)).astype(np.uint8)   # 꼬리 끝은 흐려져요
    m = a[..., 3] > 40; d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    ring = d & ~m; a[ring] = (*hx(glow), 110)
    for x, y in sparks: a[y, x] = (*hx('#FFFFFF'), 255); [a.__setitem__((y + dy, x + dx), (*hx(glow), 200)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= y + dy < 64 and 0 <= x + dx < 64]
    return a
def slit(a, x, y, c, w=3):   # 가늘게 빛나는 눈
    px(a, [(x + i, y) for i in range(w)], c); px(a, [(x + w - 1, y - 1)], '#FFFFFF')

def wolf():   # 루나울 · 달빛 늑대: 안개에서 상반신이 솟은 늑대 정령, 이마에 초승달
    S = Sprite()
    S.add('moon', lambda d: d.polygon(mist(36, 36, 63, 11, -10)), -.05)
    S.add('moon', lambda d: [d.ellipse([22, 24, 50, 48])])                                               # 가슴
    S.add('moon', lambda d: [d.ellipse([24, 8, 46, 30]), d.polygon([(27, 14), (26, 0), (34, 10)]), d.polygon([(38, 10), (44, 0), (45, 14)])])   # 머리·귀
    S.add('moon', lambda d: [d.ellipse([12, 18, 32, 29])], .1)                                           # 주둥이
    S.add('frost', lambda d: [d.polygon([(46, 26), (58, 18), (56, 30), (48, 34)]), d.polygon([(22, 30), (12, 34), (20, 38)])], .1)   # 갈기 결
    a = S.render(); slit(a, 29, 16, '#9AF0FF'); px(a, [(12, 22), (13, 22), (12, 23)], '#1A1E3A'); px(a, [(15, 26), (16, 27), (18, 27)], '#343C68')
    px(a, [(36, 9), (37, 8), (38, 8), (35, 10), (36, 11)], '#FFE9A0')
    return glowfx(a, '#A8C8FF', sparks=[(10, 40), (54, 12), (52, 44)])
def drake():   # 이그니 · 화염 도롱뇽: 불꽃 갈기, 뿔, 꼬리 대신 불길
    S = Sprite()
    S.add('flame', lambda d: d.polygon(mist(34, 38, 63, 10, 12)), .05)
    S.add('flame', lambda d: [d.polygon([(48, 20), (62, 10), (58, 24), (62, 30), (50, 30)]), d.polygon([(16, 22), (4, 12), (8, 26), (2, 32), (14, 30)])], .1)   # 불꽃 날개
    S.add('ember', lambda d: d.ellipse([20, 22, 48, 46]))
    S.add('ember', lambda d: [d.polygon([(18, 18), (34, 10), (44, 18), (40, 28), (20, 28)]), d.polygon([(14, 22), (20, 18), (22, 26), (12, 26)])])   # 머리·주둥이
    S.add('flame', lambda d: [d.polygon([(30, 12), (34, 0), (38, 10), (42, 2), (44, 16), (36, 16)])], .2)                # 불꽃 볏
    S.add('antler', lambda d: [d.polygon([(26, 12), (22, 4), (28, 10)]), d.polygon([(40, 14), (46, 6), (42, 14)])], .1)
    a = S.render(); slit(a, 24, 19, '#FFF06A'); px(a, [(13, 23), (14, 23)], '#3A0A06')
    return glowfx(a, '#FF9A40', sparks=[(8, 40), (56, 40), (50, 4)])
def fox():   # 서리 여우: 세 갈래 서리 꼬리
    S = Sprite()
    for b in (-14, 0, 14): S.add('frost', (lambda bb: (lambda d: d.polygon(mist(32 + bb * .3, 38, 62, 6, bb))))(b), .05)
    S.add('frost', lambda d: d.ellipse([22, 26, 44, 46]))
    S.add('frost', lambda d: [d.ellipse([22, 10, 44, 32]), d.polygon([(25, 16), (22, 0), (32, 10)]), d.polygon([(36, 12), (42, 0), (44, 16)]), d.polygon([(24, 20), (8, 25), (24, 30)])])
    S.add('white', lambda d: [d.polygon([(22, 30), (32, 30), (30, 40), (24, 40)])], .1)
    a = S.render(); slit(a, 26, 18, '#7AF0FF'); px(a, [(8, 25), (9, 25)], '#16304A')
    px(a, [(25, 6), (26, 8), (40, 5), (40, 7)], '#E4F6FF')
    return glowfx(a, '#BFEAFF', sparks=[(50, 20), (12, 44), (46, 6)])
def hawk():   # 폭풍 매: 펼친 날개에 번개
    S = Sprite()
    S.add('storm', lambda d: d.polygon(mist(32, 38, 63, 7, -8)), -.05)
    w = lambda s: (lambda d: d.polygon([(32, 26), (32 + s * 30, 12), (32 + s * 26, 20), (32 + s * 30, 24), (32 + s * 22, 28), (32 + s * 26, 32), (32 + s * 12, 34)]))
    S.add('storm', w(-1), .05); S.add('storm', w(1), .05)
    S.add('storm', lambda d: d.ellipse([24, 20, 40, 42]))
    S.add('storm', lambda d: d.ellipse([24, 10, 38, 24]), .1)
    S.add('yellow', lambda d: d.polygon([(24, 16), (18, 19), (24, 21)]), .1)
    a = S.render(); slit(a, 26, 15, '#FFF06A', 2)
    for (x, y) in ((8, 34), (9, 36), (8, 38), (10, 40), (54, 34), (53, 36), (55, 38), (53, 40)): px(a, [(x, y)], '#FFF06A')
    return glowfx(a, '#C8D8FF', sparks=[(32, 4), (4, 22), (60, 22)])
def serpent():   # 물뱀 정령: 지느러미 갈기, 물결 몸
    S = Sprite()
    S.add('aqua', lambda d: d.polygon(mist(30, 30, 63, 10, 18)), .0)
    S.add('aqua', lambda d: [d.ellipse([18, 20, 42, 42])])
    S.add('aqua', lambda d: [d.polygon([(16, 16), (34, 10), (42, 18), (36, 28), (18, 26)]), d.polygon([(16, 18), (6, 22), (16, 26)])])
    S.add('frost', lambda d: [d.polygon([(36, 12), (52, 4), (46, 16), (54, 20), (42, 24)]), d.polygon([(30, 10), (34, 0), (38, 10)])], .1)   # 지느러미
    a = S.render(); slit(a, 20, 17, '#E8FFF6'); px(a, [(6, 22), (7, 22)], '#082A3A')
    for x, y in ((50, 34), (52, 40), (46, 46)): px(a, [(x, y), (x + 1, y)], '#A8EAF4')
    return glowfx(a, '#7ADCF0', sparks=[(10, 36), (56, 12)])
def stag():   # 숲 사슴 정령: 잎 달린 뿔
    S = Sprite()
    S.add('jade', lambda d: d.polygon(mist(32, 38, 63, 10, -6)), -.05)
    S.add('antler', lambda d: [d.line([(28, 14), (22, 2)], 2), d.line([(24, 8), (16, 6)], 2), d.line([(36, 14), (42, 2)], 2), d.line([(40, 8), (48, 6)], 2)])
    S.add('jade', lambda d: d.ellipse([22, 26, 44, 46]))
    S.add('jade', lambda d: [d.polygon([(24, 14), (40, 14), (40, 28), (32, 34), (24, 28)]), d.polygon([(22, 16), (14, 14), (22, 22)]), d.polygon([(42, 16), (50, 14), (42, 22)])], .05)
    S.add('leaf', lambda d: [d.ellipse([14, 2, 20, 7]), d.ellipse([44, 2, 50, 7]), d.ellipse([20, 0, 25, 4])], .15)
    a = S.render(); slit(a, 26, 21, '#E8FFB0', 2); slit(a, 36, 21, '#E8FFB0', 2)
    px(a, [(31, 30), (32, 30)], '#0A2A1C')
    return glowfx(a, '#9CE0A8', sparks=[(10, 32), (54, 30), (32, 4)])
def crow():   # 그림자 까마귀: 연기 날개, 붉은 눈
    S = Sprite()
    S.add('void', lambda d: d.polygon(mist(32, 36, 63, 9, 10)), .05)
    w = lambda s: (lambda d: d.polygon([(32, 24), (32 + s * 28, 16), (32 + s * 24, 24), (32 + s * 28, 30), (32 + s * 18, 30), (32 + s * 20, 38), (32 + s * 10, 34)]))
    S.add('void', w(-1)); S.add('void', w(1))
    S.add('void', lambda d: d.ellipse([22, 18, 42, 42]), .1)
    S.add('void', lambda d: d.ellipse([24, 8, 40, 24]), .15)
    S.add('steel', lambda d: d.polygon([(24, 15), (14, 18), (24, 20)]), .1)
    a = S.render(); slit(a, 27, 14, '#FF4A5A', 2); slit(a, 34, 14, '#FF4A5A', 2)
    return glowfx(a, '#8A6AC8', sparks=[(6, 40), (58, 40)])
def pumpkin():   # 호박불 도깨비: 불타는 호박 머리, 도깨비불 꼬리
    S = Sprite()
    S.add('flame', lambda d: d.polygon(mist(32, 34, 63, 10, -10)), .1)
    S.add('pumpkin', lambda d: [d.ellipse([16, 12, 48, 40])])
    S.add('pumpkin', lambda d: [d.ellipse([24, 12, 40, 40])], .08)
    S.add('leaf', lambda d: [d.rectangle([30, 6, 33, 13]), d.ellipse([33, 4, 41, 9])], .1)
    S.add('flame', lambda d: d.polygon([(22, 12), (26, 2), (30, 10), (34, 0), (38, 10), (42, 4), (42, 14)]), .25)
    a = S.render()
    for x, y in ((22, 22), (23, 21), (24, 22), (23, 23), (38, 22), (39, 21), (40, 22), (39, 23)): px(a, [(x, y)], '#FFF06A')
    px(a, [(x, 31 + (x % 3 == 0)) for x in range(22, 42)], '#FFD040'); px(a, [(x, 32) for x in range(23, 41, 2)], '#3A1404')
    return glowfx(a, '#FFAA40', sparks=[(8, 30), (56, 24), (50, 48)])
def moth():   # 별무리 나방: 별자리 무늬 날개
    S = Sprite()
    S.add('astral', lambda d: d.polygon(mist(32, 40, 63, 5, 6)), .0)
    for s in (-1, 1):
        S.add('astral', (lambda ss: (lambda d: d.ellipse([32 + ss * 2 - (24 if ss < 0 else 0), 6, 32 + ss * 2 + (24 if ss > 0 else 0), 34])))(s), .05)
        S.add('astral', (lambda ss: (lambda d: d.ellipse([32 + ss * 4 - (16 if ss < 0 else 0), 28, 32 + ss * 4 + (16 if ss > 0 else 0), 46])))(s), -.05)
    S.add('ghost', lambda d: [d.ellipse([28, 14, 36, 44]), d.line([(30, 14), (24, 4)], 1), d.line([(34, 14), (40, 4)], 1)], .1)
    a = S.render(); slit(a, 29, 18, '#FFE9A0', 1); slit(a, 34, 18, '#FFE9A0', 1)
    for x, y in ((14, 14), (18, 22), (12, 26), (50, 14), (46, 22), (52, 26), (20, 36), (44, 36)): px(a, [(x, y)], '#FFFFFF')
    for (x0, y0), (x1, y1) in (((14, 14), (18, 22)), ((18, 22), (12, 26)), ((50, 14), (46, 22)), ((46, 22), (52, 26))):
        for t in range(1, 4): px(a, [(round(x0 + (x1 - x0) * t / 4), round(y0 + (y1 - y0) * t / 4))], '#B8A0F0')
    return glowfx(a, '#C8A0FF', sparks=[(6, 8), (58, 8), (32, 52)])
def wraith_cat():   # 유령 고양이: 반쯤 투명한 고양이 혼, 초록 눈
    S = Sprite()
    S.add('ghost', lambda d: d.polygon(mist(30, 36, 63, 11, 14)), -.05)
    S.add('ghost', lambda d: d.ellipse([20, 24, 44, 46]))
    S.add('ghost', lambda d: [d.ellipse([20, 10, 44, 32]), d.polygon([(22, 18), (20, 2), (30, 12)]), d.polygon([(42, 18), (44, 2), (34, 12)])], .05)
    S.add('ghost', lambda d: d.polygon([(44, 30), (56, 22), (58, 14), (54, 26), (46, 36)]), .1)
    a = S.render(); slit(a, 25, 20, '#7AFF9A'); slit(a, 35, 20, '#7AFF9A')
    px(a, [(31, 25), (32, 25)], '#5E6482'); px(a, [(29, 27), (30, 28), (33, 28), (34, 27)], '#5E6482')
    a[..., 3] = (a[..., 3] * .82).astype(np.uint8)
    return glowfx(a, '#B8FFD0', sparks=[(8, 20), (56, 40)])
def lion():   # 해님 사자: 햇살 갈기
    S = Sprite()
    S.add('sun', lambda d: d.polygon(mist(32, 38, 63, 10, 8)), .05)
    S.add('sun', lambda d: [d.polygon([(32 + (22 if k % 2 else 15) * math.cos(math.radians(k * 20)), 22 + (21 if k % 2 else 15) * math.sin(math.radians(k * 20))) for k in range(18)])])   # 갈기 (뾰족뾰족)
    S.add('yellow', lambda d: [d.ellipse([20, 8, 44, 34])], .1)
    S.add('belly', lambda d: d.ellipse([25, 20, 39, 33]), .1)
    a = S.render(); slit(a, 24, 17, '#FFFFFF'); slit(a, 37, 17, '#FFFFFF')
    px(a, [(31, 23), (32, 23), (31, 24), (32, 24)], '#4A2A06'); px(a, [(29, 28), (30, 29), (31, 28), (32, 28), (33, 29), (34, 28)], '#8A520C')
    return glowfx(a, '#FFD860', sparks=[(4, 44), (60, 44)])
def helm():   # 망령 기사: 떠다니는 투구 속 푸른 혼불
    S = Sprite()
    S.add('frost', lambda d: d.polygon(mist(32, 40, 63, 9, -12)), .1)
    S.add('steel', lambda d: [d.ellipse([18, 10, 46, 40]), d.rectangle([18, 26, 46, 42])])
    S.add('steel', lambda d: [d.polygon([(18, 20), (4, 6), (14, 22)]), d.polygon([(46, 20), (60, 6), (50, 22)])], .1)   # 뿔
    S.add('red', lambda d: d.polygon([(30, 10), (32, 0), (40, 2), (36, 10)]), .1)                         # 깃
    S.add('void', lambda d: [d.rectangle([22, 22, 42, 26]), d.rectangle([30, 26, 34, 36])])               # 눈구멍
    a = S.render(); slit(a, 25, 24, '#7AE0FF'); slit(a, 36, 24, '#7AE0FF')
    for y in range(28, 42, 3): px(a, [(20, y), (44, y)], '#C4CAD4')
    return glowfx(a, '#7AC8FF', sparks=[(10, 46), (54, 46)])

SP = [('루나울', '달빛 늑대 정령', wolf), ('이그니', '화염 도롱뇽 정령', drake), ('시리', '서리 여우 정령', fox), ('제피르', '폭풍 매 정령', hawk),
      ('나이아', '물뱀 정령', serpent), ('실반', '숲 사슴 정령', stag), ('녹턴', '그림자 까마귀', crow), ('잭불', '호박불 도깨비', pumpkin),
      ('스텔라리', '별무리 나방', moth), ('미스트', '유령 고양이 혼', wraith_cat), ('솔라', '해님 사자 정령', lion), ('바론', '망령 기사 투구', helm)]
if __name__ == '__main__':
    cells = [f() for _, _, f in SP]
    sheet = np.concatenate(cells, axis=1); Image.fromarray(sheet).save(os.path.join(HERE, '..', 'out', 'spirits_lpc.png'))
    if len(sys.argv) > 1:
        fnt = sys.argv[2] if len(sys.argv) > 2 else None; F = ImageFont.truetype(fnt, 15) if fnt else None; F2 = ImageFont.truetype(fnt, 12) if fnt else None
        cw, ch, cols = 230, 250, 4; pv = Image.new('RGB', (cw * cols + 20, ch * 3 + 60), (22, 16, 34)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 시안 3 · 정령 12종 (게임 그림체)', font=F, fill=(255, 233, 160))
        for i, (n, ds, _) in enumerate(SP):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 14, fill=(36, 26, 54), outline=(110, 80, 170), width=2)
            im = Image.fromarray(cells[i]).resize((192, 192), Image.NEAREST); pv.paste(im, (x + (cw - 14 - 192) // 2, y + 4), im)
            d.text((x + (cw - 14) // 2, y + 206), n, font=F, fill=(241, 233, 255), anchor='mm'); d.text((x + (cw - 14) // 2, y + 226), ds, font=F2, fill=(200, 180, 240), anchor='mm')
        pv.save(sys.argv[1])
