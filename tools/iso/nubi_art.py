# 누비 (낡은 양호실의 헝겊 인형) 도트 · 64 칸 × 8: 0~3 해진 누비 (가만히 · 고개 듦(빛나는 눈) · 훌쩍 · 놀람) · 4~7 고쳐진 누비 (가만히 · 웃음 · 눈 감음 · 수줍음)
#   해진 누비: 잿빛 헝겊 · 단추 눈 하나 없음(X 바늘땀) · 꿰맨 입 · 온몸 바늘땀 · 찢어진 왼팔에서 솜이 삐져나옴
#   고쳐진 누비: 크림빛 헝겊 · 단추 눈 둘 · 분홍 볼 · 리본 · 바늘땀은 하트 모양 하나만 남아요
#   python3 nubi_art.py → public/art/nubi.png (512×64) · tools/nubi_mock/nubi_prev.png (3 배)
import os, math
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
N = 64
OL = (34, 22, 30)
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
class C:
    def __init__(s): s.p = {}
    def put(s, x, y, c):
        if 0 <= x < N and 0 <= y < N: s.p[(int(x), int(y))] = c
    def ell(s, cx, cy, rx, ry, ramp, light=(-.25, -.95)):
        for y in range(N):
            for x in range(N):
                u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
                if u * u + v * v <= 1:
                    l = -(u * light[0] + v * light[1]) * -1
                    k = 0 if l > .55 else 1 if l > -.35 else 2 if l > -.8 else 3
                    s.p[(x, y)] = ramp[min(k, len(ramp) - 1)]
    def img(s):
        im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); a = im.load()
        for (x, y), c in s.p.items(): a[x, y] = c + (255,)
        for y in range(N):
            for x in range(N):
                if a[x, y][3] == 0 and any(0 <= x + dx < N and 0 <= y + dy < N and a[x + dx, y + dy][3] and a[x + dx, y + dy][:3] != OL for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): a[x, y] = OL + (255,)
        return im
def nubi(fixed, face, bob=0):
    c = C(); y0 = 30 + bob
    cloth = [H(h) for h in (('#fff4e2', '#f2dcc0', '#d8bc98', '#b89870') if fixed else ('#c8c0b8', '#a8a098', '#878078', '#686058'))]
    patch = [H(h) for h in (('#ffb8c8', '#f090a8', '#d07090', '#a85070') if fixed else ('#8a9aa8', '#6e7e8c', '#566270', '#3e4852'))]
    stitch = H('#d06080') if fixed else H('#2e2228')
    # 다리 · 몸 · 팔
    c.ell(25, y0 + 22, 4, 4, cloth); c.ell(38, y0 + 22, 4, 4, cloth)
    c.ell(31.5, y0 + 13, 10, 10, cloth)
    if not fixed: c.ell(28, y0 + 14, 4.5, 5, patch)                                   # 배 헝겊 조각
    c.ell(21, y0 + 11, 3.5, 6, cloth); c.ell(42, y0 + 11, 3.5, 6, cloth)
    # 머리 (크고 둥글게) · 귀처럼 묶은 헝겊 끝
    c.ell(18.5, y0 - 18, 4, 4, cloth); c.ell(44.5, y0 - 18, 4, 4, cloth)
    c.ell(31.5, y0 - 8, 14, 12.5, cloth)
    if not fixed:
        c.ell(40, y0 - 14, 4.5, 4, patch)                               # 머리 헝겊 덧댄 자국
        for (x, y) in ((19, y0 + 4), (20, y0 + 6), (18, y0 + 7), (21, y0 + 3)): c.put(x, y, H('#f4f0e8'))   # 찢어진 팔에서 솜
        c.put(17, y0 + 5, H('#ffffff')); c.put(19, y0 + 8, H('#ffffff'))
        for (x0, y0_, x1, y1) in ((24, y0 - 17, 30, y0 - 14), (35, y0 + 6, 39, y0 + 10), (25, y0 + 15, 29, y0 + 19), (34, y0 - 2, 38, y0)):   # 몸 곳곳 바늘땀
            n = 4
            for k in range(n + 1):
                x = x0 + (x1 - x0) * k / n; y = y0_ + (y1 - y0_) * k / n; c.put(x, y, stitch)
                if k % 2 == 0: c.put(x - 1, y + 1, stitch); c.put(x + 1, y - 1, stitch)
    else:
        c.ell(31.5, y0 - 21, 5, 2.5, patch); c.ell(25, y0 - 21, 3.5, 3, patch); c.ell(38, y0 - 21, 3.5, 3, patch)   # 리본
        c.put(31, y0 - 21, H('#fff0f4')); c.put(32, y0 - 21, H('#fff0f4'))
        HEART = ['.##.##.', '#######', '#######', '.#####.', '..###..', '...#...']   # 가슴의 하트 헝겊
        for yy, row in enumerate(HEART):
            for xx, ch in enumerate(row):
                if ch == '#': c.put(28 + xx, y0 + 9 + yy, patch[1] if (xx + yy) % 3 else patch[0])
        for (dx, dy) in ((0, 1), (6, 1), (1, 3), (5, 3), (3, 5)): c.put(28 + dx, y0 + 9 + dy, stitch)
        c.put(23, y0 - 5, H('#ffa8b8')); c.put(24, y0 - 5, H('#ffa8b8')); c.put(39, y0 - 5, H('#ffa8b8')); c.put(40, y0 - 5, H('#ffa8b8'))   # 분홍 볼
    # 얼굴
    ex1, ex2, ey = 26, 37, y0 - 9
    btn = H('#2a2030'); hi = H('#ffffff')
    def button(x, y, glow=False):   # 단추 눈: 지름 5 · 구멍 둘 · 반짝
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx * dx + dy * dy <= 5: c.put(x + dx, y + dy, H('#ffe070') if glow else btn)
        if not glow: c.put(x - 1, y, H('#5a4a60')); c.put(x + 1, y, H('#5a4a60')); c.put(x - 1, y - 2, hi); c.put(x - 2, y - 1, hi)
        else: c.put(x, y, H('#fffbe0'))
    def xmark(x, y):
        for k in (-2, -1, 0, 1, 2): c.put(x + k, y + k, stitch); c.put(x + k, y - k, stitch)
    if face == 'closed':
        for k in (-1, 0, 1): c.put(ex1 + k, ey, btn); c.put(ex2 + k, ey, btn)
    elif face == 'shy':
        for k in (-1, 0, 1): c.put(ex1 + k, ey - abs(k) + 1, btn); c.put(ex2 + k, ey - abs(k) + 1, btn)
    else:
        if fixed: button(ex1, ey); button(ex2, ey)
        else: xmark(ex1, ey); button(ex2, ey, glow=face == 'glow')
    if face == 'sad' and not fixed: c.put(ex2, ey + 3, H('#9fd8ff')); c.put(ex2, ey + 4, H('#9fd8ff'))   # 눈물
    if face == 'surprise':
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)): c.put(31 + dx, y0 - 2 + dy, btn)
    elif fixed and face in ('smile', 'closed', 'shy', 'idle'):
        for (dx, dy) in ((-2, 0), (-1, 1), (0, 1), (1, 1), (2, 0)): c.put(31.5 + dx, y0 - 3 + dy, H('#a04060'))
    elif not fixed:                                                       # 꿰맨 입
        for k in range(-3, 4): c.put(31 + k, y0 - 2, stitch)
        for k in (-3, -1, 1, 3): c.put(31 + k, y0 - 3, stitch); c.put(31 + k, y0 - 1, stitch)
    return c.img()
FR = [(False, 'idle', 0), (False, 'glow', -1), (False, 'sad', 1), (False, 'surprise', -1), (True, 'idle', 0), (True, 'smile', -1), (True, 'closed', 0), (True, 'shy', 0)]
if __name__ == '__main__':
    sheet = Image.new('RGBA', (N * len(FR), N), (0, 0, 0, 0))
    for i, (fx, fc, b) in enumerate(FR): sheet.paste(nubi(fx, fc, b), (i * N, 0))
    sheet.save(os.path.join(ROOT, 'public', 'art', 'nubi.png'))
    os.makedirs(os.path.join(ROOT, 'tools', 'nubi_mock'), exist_ok=True)
    pv = Image.new('RGBA', sheet.size, (42, 32, 56, 255)); pv.alpha_composite(sheet); pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_prev.png'))
    print('ok')
