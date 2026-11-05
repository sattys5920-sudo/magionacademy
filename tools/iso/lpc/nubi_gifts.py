# 누비 반짇고리 선물 (엔딩 뒤): 아이콘 32 칸 6 종 × 실 색 조합 · 선물을 단 누비 (32 칸) · 시안 미리보기
#   python3 nubi_gifts.py → public/art/nubi_gifts.png · tools/nubi_mock/nubi_gifts_prev.png
import os, sys, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c)
OUT = (42, 26, 34)
class Cv:
    def __init__(s, n=32): s.n = n; s.a = np.zeros((n, n, 4), np.uint8)
    def p(s, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < s.n and 0 <= y < s.n: s.a[y, x, :3] = c if len(c) == 3 else c[:3]; s.a[y, x, 3] = 255
    def outline(s, col=OUT):
        m = s.a[..., 3] > 0; o = s.a.copy()
        for y in range(s.n):
            for x in range(s.n):
                if m[y, x]: continue
                if any(0 <= y + dy < s.n and 0 <= x + dx < s.n and m[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))): o[y, x, :3] = col; o[y, x, 3] = 255
        s.a = o; return s
def tone(c, k):   # 0 밝게 · 1 기본 · 2 어둡게
    return sh(c, (1.18, 1.0, .74)[k])

def scarf(C):   # 줄무늬 니트 목도리 (둥글게 감긴 모양 + 늘어진 끝 + 술)
    v = Cv()
    for y in range(9, 17):
        for x in range(5, 27):
            if (x - 16) ** 2 / 121 + (y - 13) ** 2 / 20 > 1: continue
            c = C[(x // 3) % len(C)]; k = 0 if y < 11 else 2 if y > 14 else 1
            if (x + y) % 2 == 0 and 10 < y < 15: k = min(2, k + 1)   # 뜨개 무늬
            v.p(x, y, tone(c, k))
    for y in range(15, 27):
        for x in range(17, 22):
            c = C[(y // 3) % len(C)]; k = 0 if x == 17 else 2 if x == 21 else 1
            if (x + y) % 2 == 0: k = min(2, k + 1)
            v.p(x, y, tone(c, k))
    for x in (17, 19, 21): v.p(x, 27, hx('#fff4dc')); v.p(x, 28, hx('#e8d8b8'))
    return v.outline()

def button(C):   # 큰 단추 · 구멍 넷 · 다른 실로 X 꿰맴
    v = Cv(); c = C[0]
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 15.5, y - 15.5)
            if d > 11: continue
            k = 2 if d > 9.5 else 0 if (x - 12) ** 2 + (y - 11) ** 2 < 12 else 1
            if 6.5 < d < 7.5: k = 2
            v.p(x, y, tone(c, k))
    t = C[1] if len(C) > 1 else hx('#fff4dc')
    for i in range(-3, 4): v.p(15.5 + i, 15.5 + i, t); v.p(15.5 + i, 15.5 - i, t)
    for (x, y) in ((12, 12), (19, 12), (12, 19), (19, 19)): v.p(x, y, sh(c, .4))
    v.p(10, 9, hx('#ffffff')); v.p(11, 9, hx('#ffffff')); v.p(9, 10, hx('#ffffff'))
    return v.outline()

def blanket(C):   # 접힌 조각 담요 (조각마다 실 색 · 바늘땀)
    v = Cv()
    for y in range(7, 26):
        for x in range(4, 28):
            c = C[((x - 4) // 6 + (y - 7) // 6) % len(C)]
            k = 2 if y >= 22 else 1
            if (x - 4) % 6 == 0 or (y - 7) % 6 == 0: c = hx('#fff4dc'); k = 1
            v.p(x, y, tone(c, k))
    for x in range(4, 28): v.p(x, 21, hx('#c8b898'))   # 접힌 선
    for x in range(6, 27, 3): v.p(x, 23, sh(hx('#fff4dc'), .9))
    return v.outline()

def brooch(C):   # 꽃 브로치 (꽃잎 다섯 · 금빛 가운데 · 핀)
    v = Cv()
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5; cx, cy = 16 + 7 * math.cos(a), 15 + 7 * math.sin(a); c = C[i % len(C)]
        for y in range(32):
            for x in range(32):
                d = math.hypot(x - cx, y - cy)
                if d < 5: v.p(x, y, tone(c, 0 if (x - cx) + (y - cy) < -2 else 2 if d > 4 else 1))
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 16, y - 15)
            if d < 3.6: v.p(x, y, hx('#ffe070') if d < 2.4 else hx('#c89420'))
    v.p(15, 14, hx('#fff8c0'))
    for x in range(20, 29): v.p(x, 25, hx('#c8c8d0'))
    return v.outline()

def yarn(C):   # 털실 공 (감긴 실 줄 · 풀린 끝)
    v = Cv()
    for y in range(32):
        for x in range(32):
            d = math.hypot(x - 15, y - 16)
            if d > 10.5: continue
            band = int((x * .8 + y * .6 + 2 * math.sin(y * .5)) / 3)
            c = C[band % len(C)]; k = 0 if (x - 11) ** 2 + (y - 12) ** 2 < 14 else 2 if d > 9 else 1
            if (x * 2 + y) % 5 == 0: k = min(2, k + 1)
            v.p(x, y, tone(c, k))
    for i in range(10): v.p(24 + i * .6, 22 + math.sin(i * .9) * 2 + i * .4, C[0])
    return v.outline()

def pillow(C):   # 작은 베개 (네모 · 통통 · 가운데 자수 줄 · 모서리 술)
    v = Cv(); base = hx('#fff4dc')
    for y in range(9, 25):
        for x in range(4, 28):
            cx, cy = abs(x - 15.5), abs(y - 16.5)
            if cx > 11.5 - (1.5 if cy > 6 else 0) or cy > 7.5 - (1 if cx > 10 else 0): continue
            k = 0 if y < 12 or x < 7 else 2 if y > 22 or x > 25 else 1
            v.p(x, y, tone(base, k))
    for x in range(7, 25): v.p(x, 15, C[(x // 2) % len(C)]); v.p(x, 18, C[(x // 2 + 1) % len(C)])
    for x in range(7, 25, 3): v.p(x, 16, sh(C[0], .8)); v.p(x + 1, 17, sh(C[-1], .8))
    for (x, y, dx, dy) in ((3, 8, -1, -1), (28, 8, 1, -1), (3, 25, -1, 1), (28, 25, 1, 1)): v.p(x, y, C[0]); v.p(x + dx, y + dy, C[0])
    return v.outline()

GIFTS = [('scarf', '작은 목도리', scarf), ('button', '새 단추', button), ('blanket', '조각 담요', blanket), ('brooch', '꽃 브로치', brooch), ('yarn', '털실 공', yarn), ('pillow', '작은 베개', pillow)]
SETS = [[hx('#E86A6A'), hx('#6AA8E8'), hx('#F0C040')], [hx('#8AD08A'), hx('#C88AE8')], [hx('#9c9696')]]   # 세 친구 색 · 두 친구 색 · 누비 회색만

def nubi_with(gifts, C):   # 고쳐진 누비 + 리본 (앞) 위에 선물
    sheet = np.array(Image.open(os.path.join(ROOT, 'public', 'art', 'nubi_s.png')).convert('RGBA'))
    a = sheet[0:32, 256:288].copy(); ox, oy = 9, 11
    def p(x, y, c): a[oy + y, ox + x, :3] = c; a[oy + y, ox + x, 3] = 255
    if 'scarf' in gifts:
        for x in range(2, 12): p(x, 11, C[(x // 2) % len(C)]); p(x, 12, sh(C[(x // 2) % len(C)], .78))
        for y in range(12, 16): p(10, y, C[y % len(C)]); p(11, y, sh(C[y % len(C)], .78))
        p(1, 11, OUT); p(12, 11, OUT); p(12, 12, OUT); p(12, 13, OUT)
    if 'button' in gifts: p(9, 14, C[0]); p(9, 15, sh(C[0], .7))
    if 'brooch' in gifts:
        c2 = C[1 % len(C)]; p(3, 13, c2); p(2, 14, c2); p(4, 14, c2); p(3, 15, c2); p(3, 14, hx('#ffe070'))
    if 'yarn' in gifts:
        for y in range(16, 20):
            for x in range(4, 9):
                if (x - 6) ** 2 + (y - 17.6) ** 2 < 5.5: p(x, y, sh(C[(x + y) % len(C)], .85 if (x + y) % 3 else 1.1))
    return a

def doll_furn(C):   # 방에 두는 작은 누비 인형 (선물을 다 단 모습 · 쿠션 위)
    v = np.zeros((32, 32, 4), np.uint8)
    cu = Cv()
    for y in range(22, 31):
        for x in range(4, 28):
            if (x - 16) ** 2 / 144 + (y - 26) ** 2 / 16 <= 1: cu.p(x, y, tone(hx('#E8A0B0'), 0 if y < 24 else 2 if y > 28 else 1))
    cu.outline(); v = cu.a
    nb = nubi_with({'scarf', 'button', 'brooch', 'yarn'}, C)
    m = nb[..., 3] > 0; sub = np.zeros_like(v); sub[:-4] = nb[4:]; mm = sub[..., 3] > 0; v[mm] = sub[mm]
    return v

if __name__ == '__main__':
    icons = [[f(C) for _, _, f in GIFTS] for C in SETS]
    row = lambda cells: np.concatenate([c.a if isinstance(c, Cv) else c for c in cells], 1)
    sheet = np.concatenate([row(r) for r in icons], 0)
    nubis = [nubi_with({g}, SETS[0]) for g in ('scarf', 'button', 'brooch', 'yarn')] + [nubi_with({'scarf', 'button', 'brooch', 'yarn'}, SETS[0]), doll_furn(SETS[0])]
    sheet = np.concatenate([sheet, row(nubis)], 0)
    Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'nubi_gifts.png'))
    # 미리보기
    pv = Image.new('RGBA', (32 * 6, 32 * 4), (43, 31, 69, 255)); pv.alpha_composite(Image.fromarray(sheet))
    pv.resize((pv.width * 5, pv.height * 5), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_gifts_prev.png'))
    print('ok')
