# 레이드 보스 4 종 도트 (정면 · 96 칸): 얼음 거인 · 불꽃 용 · 그림자 마녀 · 시계탑 골렘
#   칸마다 2 동작: 0 가만히 · 1 기술 준비 (팔을 들고 눈·가슴이 빛나요)
#   python3 raid_bosses.py [시트.png] → 기본은 tools/raid_mock/raid_bosses.png (768×96) · 미리 보기 raid_bosses_prev.png (3 배)
import sys, os, math
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.join(HERE, '..', 'raid_mock')
N = 96

def ell(cx, cy, rx, ry):
    return {(x, y) for y in range(N) for x in range(N) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}
def poly(pts):   # 아무 다각형 (짝홀 규칙)
    out = set(); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(N, int(max(ys)) + 1)):
        for x in range(max(0, int(min(xs))), min(N, int(max(xs)) + 1)):
            px, py = x + .5, y + .5; c = False; j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi: c = not c
                j = i
            if c: out.add((x, y))
    return out
def rect(x0, y0, x1, y1): return {(x, y) for y in range(max(0, y0), min(N, y1)) for x in range(max(0, x0), min(N, x1))}
def mir(m): return m | {(N - 1 - x, y) for (x, y) in m}
def line(x0, y0, x1, y1, w=1):
    out = set(); n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for i in range(n + 1):
        t = i / n; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for dx in range(-(w // 2), w - w // 2):
            for dy in range(-(w // 2), w - w // 2): out.add((int(x + dx), int(y + dy)))
    return {p for p in out if 0 <= p[0] < N and 0 <= p[1] < N}

class Spr:
    def __init__(self, ol): self.px = {}; self.ol = ol; self.flat = set()
    def add(self, mask, ramp, light=(.5, .8), flat=False, ring=None):
        if not mask: return
        xs = [p[0] for p in mask]; ys = [p[1] for p in mask]; cx = (min(xs) + max(xs)) / 2; cy = (min(ys) + max(ys)) / 2
        rx = max(1, (max(xs) - min(xs)) / 2); ry = max(1, (max(ys) - min(ys)) / 2)
        edge = {(x, y) for (x, y) in mask if (x, y) in self.px and any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))} if not flat and len(mask) > 30 else set()
        for (x, y) in mask:
            if (x, y) in edge:   # 앞에 오는 조각의 가장자리에 안쪽 선
                self.px[(x, y)] = tuple(int(v * .55) for v in ramp[-1]); continue
            if flat: c = ramp if isinstance(ramp, tuple) else ramp[min(1, len(ramp) - 1)]
            else:
                u = (x - cx) / rx; v = (y - cy) / ry; l = -(u * light[0] + v * light[1])
                k = 0 if l > .55 else 1 if l > .1 else 2 if l > -.5 else 3
                c = ramp[min(k, len(ramp) - 1)]
            self.px[(x, y)] = c
            if flat: self.flat.add((x, y))
    def dot(self, pts, c):
        for p in pts:
            if 0 <= p[0] < N and 0 <= p[1] < N: self.px[p] = c
    def img(self):
        im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); a = im.load()
        for (x, y), c in self.px.items(): a[x, y] = c + (255,) if len(c) == 3 else c
        for (x, y) in [(x, y) for y in range(N) for x in range(N) if a[x, y][3] == 0 and any(0 <= x + dx < N and 0 <= y + dy < N and a[x + dx, y + dy][3] > 0 and a[x + dx, y + dy][:3] != self.ol for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]:
            a[x, y] = self.ol + (255,)
        return im
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def ramp(*hs): return [H(h) for h in hs]

# ---------------- 1. 얼음 거인 ----------------
def ice(f):
    S = Spr(H('#14203A'))
    ICE = ramp('#E8F6FF', '#A8D4F2', '#6EA4D8', '#40709E'); DEEP = ramp('#9CC8EC', '#6496CC', '#3E6AA0', '#26466E'); CRY = ramp('#FFFFFF', '#C8F0FF', '#7FD4FF', '#3E9AD8')
    S.add(mir(rect(30, 70, 45, 90)), DEEP)                                   # 다리
    S.add(mir(ell(36, 91, 11, 5)), ICE)                                      # 발
    S.add(ell(48, 54, 27, 23), ICE)                                          # 몸
    S.add(ell(48, 62, 15, 12), DEEP, light=(.3, -.6))                         # 배 그림자
    if f == 0:
        S.add(mir(ell(19, 50, 8, 16)), DEEP); S.add(mir(ell(15, 70, 10, 9)), ICE)          # 팔 · 주먹 (아래)
    else:
        S.add(mir(poly([(14, 40), (24, 36), (18, 14), (9, 16)])), DEEP); S.add(mir(ell(13, 12, 10, 9)), ICE)   # 팔을 번쩍
    S.add(mir(ell(24, 36, 12, 9)), ICE)                                      # 어깨
    for (x, h) in ((16, 18), (22, 24), (28, 15)):                            # 어깨 수정
        S.add(mir(poly([(x - 3, 36), (x, 36 - h), (x + 3, 36)])), CRY, light=(.9, .3))
    S.add(ell(48, 25, 13, 12), ICE)                                          # 머리
    S.add(rect(37, 21, 60, 24), [H('#40709E')], flat=True)                   # 눈썹 그늘
    eye = H('#FFFFFF') if f else H('#7FE6FF')
    S.dot([(x, y) for x in (41, 42, 43, 53, 54, 55) for y in (22, 23)], eye)
    if f: S.dot([(x, 21) for x in (42, 54)] + [(x, 24) for x in (42, 54)], H('#7FE6FF'))
    for (x, l) in ((40, 14), (44, 20), (48, 24), (52, 20), (56, 14)):        # 고드름 수염
        S.add(poly([(x - 3, 32), (x + 3, 32), (x, 32 + l)]), CRY, light=(.6, -.2))
    rc = H('#BFF8FF') if f else H('#7FD4FF')                                 # 가슴 무늬
    S.dot([p for p in line(40, 46, 48, 40) | line(48, 40, 56, 46) | line(48, 40, 48, 56) | line(42, 52, 54, 52)], rc)
    if f: S.dot([p for p in ell(48, 47, 3, 3)], H('#FFFFFF'))
    return S.img()

# ---------------- 2. 불꽃 용 ----------------
def dragon(f):
    S = Spr(H('#3A0E16'))
    SC = ramp('#FF8A5A', '#E0483A', '#B02A30', '#761A28'); WG = ramp('#C8402E', '#9A2A2A', '#701C26', '#4E1420'); BL = ramp('#FFF0A8', '#FFD070', '#F0A040', '#C87030'); HO = ramp('#FFF4D8', '#E8D0A0', '#B8986A', '#7A6040')
    wy = -6 if f else 0
    for s in (0, 1):                                                         # 날개 (막 · 뼈)
        pts = [(36, 40), (4, 10 + wy), (2, 30 + wy), (8, 46 + wy), (4, 60 + wy), (22, 58), (32, 62)]
        m = poly(pts); m = m if s == 0 else {(N - 1 - x, y) for x, y in m}; S.add(m, WG, light=(.2, .8))
        for (a, b) in ((4, 10 + wy), (2, 30 + wy), (8, 46 + wy), (4, 60 + wy)):
            ln = line(36, 40, a, b, 2); ln = ln if s == 0 else {(N - 1 - x, y) for x, y in ln}; S.dot(ln, H('#E0483A'))
    S.add(poly([(62, 80), (80, 86), (90, 78), (86, 70), (80, 76), (66, 74)]), SC)          # 꼬리
    S.add(mir(ell(36, 86, 8, 7)), SC); S.dot(mir({(x, 92) for x in (31, 34, 37)}), H('#FFF4D8'))   # 발 · 발톱
    S.add(ell(48, 62, 19, 24), SC)                                           # 몸
    belly = ramp('#FFFFC8', '#FFE090', '#FFC060', '#F09040') if f else BL
    S.add(ell(48, 66, 10, 18), belly, light=(.2, .6))
    for y in range(52, 84, 5): S.dot({(x, y) for x in range(40, 57) if (x + .5 - 48) ** 2 / 100 + (y + .5 - 66) ** 2 / 324 <= 1}, H('#C87030'))
    S.add(mir(ell(31, 60, 6, 10)), SC); S.add(mir(ell(30, 70, 5, 4)), SC)                  # 팔
    S.add(ell(48, 40, 8, 10), SC)                                            # 목
    S.add(mir(poly([(38, 22), (26, 4), (30, 18), (34, 26)])), HO, light=(.8, .2))          # 뿔
    S.add(ell(48, 26, 15, 11), SC)                                           # 머리
    S.add(ell(48, 34, 10, 7 if f else 6), SC, light=(.3, .5))                 # 주둥이
    if f:
        S.add(ell(48, 37, 7, 4), [H('#FFF4A8'), H('#FFD050'), H('#FF8A30'), H('#E04A20')], light=(0, -1))   # 입 속 불
    S.dot({(44, 32), (52, 32)}, H('#3A0E16'))                                # 콧구멍
    eye = H('#FFF8A0') if f else H('#FFD040')
    S.dot({(x, y) for x in (39, 40, 41) for y in (23, 24)} | {(x, y) for x in (55, 56, 57) for y in (23, 24)}, eye); S.dot({(40, 23), (40, 24), (56, 23), (56, 24)}, H('#3A0E16'))
    S.dot(mir(line(37, 20, 43, 22)), H('#761A28'))                           # 눈썹
    S.dot({(x, 14 + abs(x - 48) // 3) for x in range(42, 55, 3)}, H('#FFD070'))   # 머리 비늘
    return S.img()

# ---------------- 3. 그림자 마녀 ----------------
def witch(f):
    S = Spr(H('#120820'))
    CL = ramp('#7A4AA8', '#5A3288', '#3E2066', '#28143E'); HT = ramp('#6A3E98', '#4A2A78', '#341C58', '#22103A'); SK = ramp('#E8DCF0', '#C8B8D8', '#A090B8', '#706088'); ORB = ramp('#FFFFFF', '#E0B0FF', '#B070F0', '#7A3AC8')
    bot = []                                                                  # 찢어진 자락
    for i in range(13):
        x = 16 + i * 64 / 12; bot.append((x, 88 + (6 if i % 2 else 0) - (3 if i in (3, 8) else 0)))
    S.add(poly([(36, 34), (60, 34), (82, 88)] + bot[::-1] + [(14, 88)]), CL, light=(.4, .5))
    S.dot({(x, y) for x in range(40, 57) for y in range(40, 88) if (x - 48) ** 2 < (y - 36) * 3.2 and (x + y) % 7 == 0}, H('#7A4AA8'))
    for k in (0, 1, 2):                                                       # 아래 그림자 연기
        S.add(ell(30 + k * 18, 92, 7, 3), [H('#3E2066')], flat=True)
    if f == 0:
        S.add(mir(poly([(34, 38), (24, 44), (16, 62), (24, 64), (32, 50)])), CL)         # 소매 (아래)
        hand = [(18, 64), (78, 64)]
    else:
        S.add(mir(poly([(34, 38), (22, 30), (12, 14), (20, 12), (32, 28)])), CL)         # 소매 (위로)
        hand = [(15, 11), (81, 11)]
    for (hx, hy) in hand:
        S.add(ell(hx, hy, 3, 3), SK)
        r = 8 if f else 6; S.add(ell(hx, hy - r - 1, r, r), ORB, light=(.6, .7))
        S.dot({(hx - 2, hy - r - 3)}, H('#FFFFFF'))
    S.add(ell(48, 30, 9, 9), SK)                                             # 얼굴
    S.add(rect(38, 24, 59, 28), [H('#28143E')], flat=True)                   # 모자 그늘
    eye = H('#FFFFFF') if f else H('#E0A0FF')
    S.dot({(x, y) for x in (43, 44) for y in (29, 30)} | {(x, y) for x in (52, 53) for y in (29, 30)}, eye)
    S.dot({(x, 35) for x in range(45, 52)}, H('#706088'))                    # 입
    S.add(mir(poly([(39, 30), (34, 40), (38, 46), (41, 34)])), ramp('#4A2A78', '#341C58', '#22103A', '#22103A'))   # 머리카락
    S.add(ell(48, 23, 26, 5), HT, light=(.3, .9))                            # 챙
    S.add(poly([(32, 22), (64, 22), (60, 14), (54, 6), (58, -2), (46, 2), (40, 12)]), HT, light=(.6, .4))   # 고깔 (끝이 휘었어요)
    S.add(rect(36, 17, 61, 20), [H('#C08AFF') if f else H('#8A5AC8')], flat=True)   # 띠
    S.dot({(47, 18), (48, 18), (48, 17), (48, 19)}, H('#FFE070'))
    return S.img()

# ---------------- 4. 시계탑 골렘 ----------------
def clock(f):
    S = Spr(H('#2A1A0C'))
    BR = ramp('#FFE8A0', '#E8B858', '#B8842E', '#7A5420'); DK = ramp('#C8964A', '#946628', '#6A4418', '#4A2E10'); FC = ramp('#FFFBEA', '#F2E8C8', '#D8C898', '#B0A070')
    def gear(cx, cy, r, rp):
        m = ell(cx, cy, r, r)
        for k in range(8):
            a = k * math.pi / 4; m |= ell(cx + math.cos(a) * r, cy + math.sin(a) * r, 2.4, 2.4)
        S.add(m, rp); S.add(ell(cx, cy, r * .35, r * .35), [H('#4A2E10')], flat=True)
    S.add(mir(rect(32, 74, 44, 90)), DK); S.add(mir(rect(29, 88, 46, 93)), BR)              # 다리
    pa = 0 if f else 5                                                          # 추 (흔들림)
    S.dot(line(48, 68, 48 + pa, 84), H('#B8842E')); S.add(ell(48 + pa, 86, 5, 5), BR)
    gear(17, 32, 9, DK); gear(79, 32, 9, DK)                                    # 어깨 톱니
    S.add(poly([(24, 30), (72, 30), (76, 72), (20, 72)]), BR, light=(.5, .6))  # 몸
    S.dot(set(line(22, 50, 74, 50)), H('#7A5420')); S.dot({(x, y) for x in (26, 70) for y in range(34, 70, 6)}, H('#FFE8A0'))   # 리벳
    if f == 0:
        S.add(mir(poly([(22, 36), (12, 40), (8, 64), (16, 66), (22, 48)])), DK); S.add(mir(rect(4, 62, 20, 74)), BR)      # 팔 · 망치 주먹
    else:
        S.add(mir(poly([(22, 34), (12, 30), (6, 10), (14, 8), (22, 26)])), DK); S.add(mir(rect(2, 0, 18, 12)), BR)
    S.add(ell(48, 48, 15, 15), FC, light=(.4, .6))                             # 시계판
    S.dot({p for p in ell(48, 48, 15, 15) if not (p in ell(48, 48, 13.5, 13.5))}, H('#7A5420'))
    for k in range(12):
        a = k * math.pi / 6; S.dot({(int(48 + math.cos(a) * 11), int(48 + math.sin(a) * 11))}, H('#4A2E10'))
    ha, ma = (-math.pi / 2, math.pi / 6) if f == 0 else (math.pi * .9, -math.pi * .4)
    S.dot(line(48, 48, 48 + math.cos(ha) * 6, 48 + math.sin(ha) * 6, 2), H('#2A1A0C')); S.dot(line(48, 48, 48 + math.cos(ma) * 10, 48 + math.sin(ma) * 10), H('#2A1A0C'))
    if f: S.dot({p for p in ell(48, 48, 13.5, 13.5) if not (p in ell(48, 48, 12.5, 12.5))}, H('#FFF4A0'))
    S.add(rect(36, 10, 61, 28), BR, light=(.5, .7))                            # 머리
    S.add(rect(39, 16, 58, 21), [H('#2A1A0C')], flat=True)
    vis = H('#FFFFFF') if f else H('#FFE070')
    S.dot({(x, y) for x in range(41, 57) for y in (18, 19) if f or x % 4 != 0}, vis)
    S.add(poly([(42, 10), (54, 10), (48, 2)]), DK); S.add(ell(48, 2, 2.5, 2.5), [H('#FFE070')], flat=True)   # 꼭대기 종
    return S.img()

BOSSES = [('ice', '얼음 거인', ice), ('dragon', '불꽃 용', dragon), ('witch', '그림자 마녀', witch), ('clock', '시계탑 골렘', clock)]
if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTD, 'raid_bosses.png')
    sheet = Image.new('RGBA', (N * 8, N), (0, 0, 0, 0))
    for i, (k, n, fn) in enumerate(BOSSES):
        for f in (0, 1): sheet.paste(fn(f), ((i * 2 + f) * N, 0))
    sheet.save(out)
    pv = Image.new('RGBA', (N * 8, N + 8), (34, 26, 52, 255)); pv.alpha_composite(sheet, (0, 4))
    pv.resize((pv.width * 3 // 2, pv.height * 3 // 2), Image.NEAREST).save(os.path.join(OUTD, 'raid_bosses_prev.png'))
    print('ok', out)
