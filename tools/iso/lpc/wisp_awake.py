# 사역마 각성 시안: 12종 정령불의 「각성한 모습」 (wisp3_art 의 불꽃·빛 그리기를 그대로 써요)
#   python3 wisp_awake.py <비교 미리보기.png> [글꼴] → tools/iso/out/wisps_awake.png (64칸 × 12), wisps_awake_anim.png (12줄 × 8칸)
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wisp3_art as W
from wisp3_art import flame, orb, render, sparks, fbm, hx, N, XX, YY, DITH
HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda: W.FRAC
def ring(img, cx, cy, rx, ry, col, a=200, w=.8, gap=None):   # 기울어진 빛 고리 (gap: 끊긴 룬 고리)
    d = np.abs(np.hypot((XX - cx) / rx, (YY - cy) / ry) - 1) * min(rx, ry); m = d < w
    if gap: ang = np.arctan2(YY - cy, XX - cx); m &= (np.sin(ang * gap + F() * 2 * math.pi) > -.3)
    m &= img[..., 3] < 230; img[m, :3] = hx(col); img[m, 3] = a; return img
def motes(img, cx, cy, r, n, col, speed=1, ry=None):   # 둘레를 도는 빛 알갱이
    for i in range(n):
        a = i / n * 2 * math.pi + F() * 2 * math.pi * speed; x, y = int(cx + r * math.cos(a)), int(cy + (ry or r * .45) * math.sin(a))
        if 0 <= x < N - 1 and 0 <= y < N - 1: img[y:y + 2, x:x + 2, :3] = hx(col); img[y:y + 2, x:x + 2, 3] = 255
    return img
def wings(cx, cy, span, h, seed, lift=0):   # 좌우로 펼친 빛 날개 (불꽃 혀 여러 개를 비스듬히)
    f = np.zeros((N, N))
    for s in (-1, 1):
        for j, (dx, hh) in enumerate([(7, h), (11, h * .82), (15, h * .62)]):
            if dx > span: break
            f = np.maximum(f, flame(cx + s * dx, cy + 6, hh, 4.6 - j * .7, seed + j + (s > 0) * 5, .7, s * (16 + j * 7), 0, 1, 1.15, .25))
    return f
def base(k, sz=1.0):   # 원래 모습 불꽃 세기 (조금 크게)
    return [lambda: flame(32, 48, 44 * sz, 13 * sz, 1, 1.2, 4, -6, 1.2)][0]()
def a1():   # Vael: 안개 면사포 날개 + 끊긴 룬 고리
    f = np.maximum(flame(32, 46, 42, 13, 1, 1.2, 4, -6, 1.2), wings(32, 38, 21, 30, 101) * .8); img = render(f, W.BLUE, '#3A7CFF', 1.3)
    return motes(ring(img, 32, 50, 22, 6, '#8AC4FF', 190, .7, 7), 32, 50, 22, 6, '#E4F4FF')
def a2():   # Ixi: 별 왕관을 쓴 쌍나선 + 둘레를 도는 쌍둥이 구슬
    a = flame(32, 46, 44, 9, 2, .8, 0, 9, 1.6); b = flame(32, 46, 40, 9, 3, .8, 0, -9, 1.6); img = render(np.maximum(np.maximum(a, b), orb(32, 12, 5) * .7), W.PURP, '#8A50FF', 1.3)
    for i in range(5): ang = -math.pi / 2 + (i - 2) * .45; x, y = int(32 + 13 * math.cos(ang)), int(14 + 13 * math.sin(ang)); img[y - 1:y + 2, x, :3] = 255; img[y, x - 1:x + 2, :3] = 255; img[y - 1:y + 2, x, 3] = img[y, x - 1:x + 2, 3] = 255
    t = F() * 2 * math.pi
    for s in (0, math.pi): x, y = int(32 + 20 * math.cos(t + s)), int(36 + 8 * math.sin(t + s)); img[y - 1:y + 2, x - 1:x + 2, :3] = hx('#E8D4FF'); img[y - 1:y + 2, x - 1:x + 2, 3] = 255
    return img
def a3():   # Puck: 도깨비불 다섯이 둘레를 돌고, 가운데 불은 등롱 왕관
    t = F() * 2 * math.pi; f = flame(32, 44, 36, 11, 4, 1.4, 2)
    for i in range(5): a = t + i / 5 * 2 * math.pi; f = np.maximum(f, flame(32 + 21 * math.cos(a), 44 + 9 * math.sin(a), 17, 5.5, 10 + i, 1.1))
    img = render(f, W.GREEN, '#30C860', 1.3); return ring(img, 32, 42, 22, 9, '#9AF0A0', 110, .5)
def a4():   # Lotis: 겹겹이 핀 큰 연꽃불 + 물결 고리
    f = np.maximum.reduce([flame(32 + dx, 50, 26 - abs(dx) * .25, 5.5, 10 + i, .6, dx * 1.8, 0, 1, 1.1) * .9 for i, dx in enumerate((-15, -10, -5, 5, 10, 15))] + [flame(32 + dx, 50, 18, 4, 20 + i, .5, dx * 2.4, 0, 1, 1) * .8 for i, dx in enumerate((-20, 20))] + [flame(32, 46, 44, 9, 9, .9, 0, 2)])
    img = render(f, W.PINK, '#FF5AB0', 1.3); return motes(ring(img, 32, 54, 24, 5, '#FFC4E2', 170, .7), 32, 54, 24, 8, '#FFF2F8', .5, 5)
def a5():   # Sol: 햇무리 빛살 + 불꽃 왕관
    ang = np.arctan2(YY - 30, XX - 32); r = np.hypot(XX - 32, YY - 30)
    rays = np.clip((np.cos(ang * 12 + F() * 2 * math.pi / 12) * .5 + .5) ** 8 * (1 - r / 31), 0, 1) * .55
    crown = np.maximum.reduce([flame(32 + dx, 18, 9 - abs(dx) * .2, 2.5, 30 + i, .4) for i, dx in enumerate((-8, -4, 0, 4, 8))])
    f = np.maximum.reduce([flame(32, 46, 38, 12, 20, 1, 0, 2), orb(32, 34, 13) * .85, rays, crown * .9]); img = render(f, W.GOLD, '#FFC030', 1.5)
    return ring(img, 32, 30, 25, 25, '#FFEC9A', 120, .6, 12)
def a6():   # Lune: 등 뒤 보름달 + 초승달 불 + 별가루 고리
    f0 = orb(32, 28, 19); moon = np.clip(f0 * .9, 0, .32)
    ang = np.arctan2(YY - 32, XX - 32); r = np.hypot(XX - 32, YY - 32); cres = np.clip(1 - np.abs(r - 15) / (7 * np.clip(np.cos((ang + 2.4) * .8), 0, 1) + .01), 0, 1) * (np.cos((ang + 2.4) * .8) > 0)
    img = render(np.maximum(moon, np.clip(cres * 1.25, 0, 1)), W.SILV, '#B0C8FF', 1.5); return motes(img, 32, 32, 26, 10, '#FFFFFF', .4, 10)
def a7():   # Ignis: 불사조 날개
    f = np.maximum.reduce([flame(32, 48, 46, 13, 40, 1.8, 0, 0, 1, 1.1, .7), wings(32, 40, 21, 34, 140)]); img = render(f, W.RED, '#FF4818', 1.4)
    return sparks(img, 207, 26, '#FFC070', 32, 0, 34, 36, 3)
def a8():   # Rill: 소용돌이치는 물 고리 두 겹
    core = flame(32, 46, 38, 10, 50, .8, 0, 3); band = np.zeros((N, N))
    for ph, amp in ((0, 8), (math.pi, 8), (math.pi / 2, 5)):
        yb = 38 + amp * np.sin((XX - 32) / 6.5 + ph + F() * 2 * math.pi) - (XX - 12) * .35
        band = np.maximum(band, np.clip(1 - np.abs(YY - yb) / 2.4, 0, 1) * np.clip(1 - np.abs(XX - 32) / 26, 0, 1) * 1.1)
    img = render(np.maximum(core, band), W.TEAL, '#20D0C0', 1.3); return motes(img, 32, 40, 24, 7, '#E0FFFA', .6, 8)
def a9():   # Orbi: 겹친 고리 셋이 서로 다르게 도는 혼천의
    ang = np.arctan2(YY - 34, XX - 32); r = np.hypot(XX - 32, YY - 34); t = F() * 2 * math.pi
    rr = np.clip(1 - np.abs(r - 11) / 3.5, 0, 1); f = np.clip(rr + fbm(61) * .2 * (rr > 0), 0, 1); f = np.maximum(f, orb(32, 34, 6))
    img = render(f, W.ORNG, '#FF8020', 1.3)
    ring(img, 32, 34, 22, 7 + 4 * math.sin(t), '#FFD080', 210, .7); ring(img, 32, 34, 7 + 4 * math.cos(t), 22, '#FFB060', 190, .7); ring(img, 32, 34, 18, 18, '#FFF0C8', 120, .5, 8)
    return img
def a10():   # Eon: 은하 소용돌이 + 별빛
    r = np.hypot(XX - 32, YY - 34); ang = np.arctan2(YY - 34, XX - 32)
    spiral = np.clip((np.cos(ang * 2 - r * .35 + F() * 2 * math.pi) * .5 + .5) ** 2 * np.clip(1 - r / 28, 0, 1) * 1.1, 0, 1)
    f = np.maximum(spiral * .7, flame(32, 44, 38, 10, 70, 1.2, 4, 3, 1.3, 1.1, .4)); img = render(np.minimum(f, .85), W.NAVY, '#5068FF', 1.4)
    rs = np.random.RandomState(72)
    for _ in range(20):
        x, y = rs.randint(8, 56), rs.randint(8, 58)
        if f[y, x] > .1: img[y, x, :3] = 255; img[y, x, 3] = 255
    return img
def a11():   # Nyx: 그림자 날개 + 가시 왕관, 보랏빛 테두리
    f = np.maximum.reduce([flame(32, 46, 44, 12, 80, 1.6, 2, 3), wings(32, 40, 21, 32, 180)])
    thorn = np.maximum.reduce([flame(32 + dx, 14, 8, 1.8, 90 + i, .3, dx * .3) for i, dx in enumerate((-9, -5, 0, 5, 9))])
    img = render(np.maximum(f, thorn), W.VOID, '#7A40E0', 1.5); e = (np.maximum(f, thorn) > .02) & (np.maximum(f, thorn) < .2); img[e, :3] = hx('#B080FF'); img[e, 3] = 220
    return sparks(img, 211, 14, '#5A30A0', 32, 0, 34, 34, 3)
def a12():   # Iris: 오로라 날개 + 무지갯빛 고리
    f = np.maximum(flame(32, 46, 44, 12, 90, 1.3, -3, 4), wings(32, 38, 21, 32, 190) * .9); img = render(f, W.SILV, '#FFFFFF', 1.4)
    cols = [hx(c) for c in ('#FF5A7A', '#FFA040', '#FFE060', '#60E080', '#50B0FF', '#A070FF')]
    h = ((YY - XX * .5 + fbm(91) * 10 + F() * 30) / 5).astype(int) % 6; m = (img[..., 3] > 0) & (f < .75)
    for k in range(6): s = m & (h == k); img[s, :3] = img[s, :3] * .3 + cols[k] * .7
    return motes(img, 32, 40, 24, 12, '#FFFFFF', .7, 8)
AW = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]
TITLE = ['안개 날개의 혼불', '별 왕관 쌍둥이', '도깨비불 행렬', '만개한 연꽃불', '태양 왕관', '보름달의 혼불', '불사조', '소용돌이 물불', '혼천의 고리', '은하의 현자', '그림자 날개', '오로라 날개']
def frames(F_=8):
    rows = []
    for f in AW:
        cs = []
        for k in range(F_): W.FRAC = k / F_; cs.append(np.clip(f(), 0, 255).astype(np.uint8))
        rows.append(np.concatenate(cs, axis=1))
    W.FRAC = 0.; return np.concatenate(rows, axis=0)
if __name__ == '__main__':
    out = os.path.join(HERE, '..', 'out'); an = frames(); Image.fromarray(an).save(os.path.join(out, 'wisps_awake_anim.png'))
    cells = [an[i * 64:(i + 1) * 64, 0:64] for i in range(12)]; Image.fromarray(np.concatenate(cells, axis=1)).save(os.path.join(out, 'wisps_awake.png'))
    if len(sys.argv) > 1:
        before = np.array(Image.open(os.path.join(out, 'wisps3.png')).convert('RGBA'))
        fnt = sys.argv[2] if len(sys.argv) > 2 else None; FT = ImageFont.truetype(fnt, 15) if fnt else None; F2 = ImageFont.truetype(fnt, 12) if fnt else None
        cw, ch, cols = 300, 210, 4; pv = Image.new('RGBA', (cw * cols + 20, ch * 3 + 60), (8, 6, 14, 255)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 각성 시안 · 지금 모습 → 각성한 모습', font=FT, fill=(220, 200, 150))
        for i in range(12):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 10, fill=(14, 10, 22), outline=(52, 42, 72), width=2)
            b = Image.fromarray(before[:, i * 64:(i + 1) * 64]).resize((112, 112), Image.NEAREST); a = Image.fromarray(cells[i]).resize((144, 144), Image.NEAREST)
            pv.alpha_composite(b, (x + 8, y + 30)); pv.alpha_composite(a, (x + 130, y + 6)); d.text((x + 120, y + 86), '→', font=FT, fill=(160, 140, 200), anchor='mm')
            d.text((x + 64, y + 160), W.WS[i][1], font=FT, fill=(230, 220, 240), anchor='mm'); d.text((x + 202, y + 160), W.WS[i][1] + ' (각성)', font=F2, fill=(200, 180, 240), anchor='mm')
        pv.convert('RGB').save(sys.argv[1])
    print('ok')
