# 사역마 만남 연출 컷 배경: 깊은 숲속 빈터, 덩굴에 감긴 옛 제단 (320×180, 이벤트 무대 EV 크기)
#   우리 맵처럼 둥근 나무·단계 음영·디더, 밤빛 · 제단 불빛은 연출에서 따로 그려요
#   python3 familiar_altar.py → tools/iso/out/familiar_altar.png (+ 4배 미리보기 out/familiar_altar_x4.png)
import os, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
W, H = 320, 180
R = np.random.RandomState(7)
def hx(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
img = np.zeros((H, W, 3))
YY, XX = np.mgrid[0:H, 0:W]
B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
D = np.tile(B4, (H // 4 + 1, W // 4 + 1))[:H, :W]
def ramp_fill(mask, val, ramp):   # val 0~1 → 램프 단계 (디더)
    R_ = [hx(c) for c in ramp]; n = len(R_); v = np.clip(val * (n - 1) + D - .5, 0, n - 1).astype(int)
    for k in range(n): s = mask & (v == k); img[s] = R_[k]
def blob(cx, cy, rx, ry): return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1
# 하늘: 위는 짙은 남색, 아래로 보랏빛
ramp_fill(np.ones((H, W), bool), 1 - YY / 110, ['#120C26', '#16102E', '#1C1438', '#221A44'])
for _ in range(70):
    x, y = R.randint(0, W), R.randint(0, 70); img[y, x] = hx('#C8C0F0') * (.5 + R.rand() * .5)
# 달 (나무 뒤로 반쯤)
m = blob(236, 34, 15, 15); ramp_fill(m, 1 - np.hypot(XX - 232, YY - 30) / 22, ['#B8B0A0', '#D8D0B8', '#F0EACC', '#FFF8E0'])
halo = (np.hypot(XX - 236, YY - 34) < 30) & ~m & (D < .25); img[halo] = img[halo] * .6 + hx('#6A6290') * .4
# 먼 숲 실루엣 (두 겹)
def far_trees(base, h, col, seed, step):
    r = np.random.RandomState(seed)
    for x in range(-10, W + 10, step):
        cy = base - r.randint(int(h * .6), h); rr = r.randint(step - 2, step + 6)
        img[blob(x + r.randint(-3, 3), cy, rr, rr * 1.1)] = hx(col)
    img[YY > base - 4] = np.where((YY > base - 4)[..., None], hx(col), img)[YY > base - 4]
far_trees(92, 40, '#1A1A34', 3, 14)
far_trees(104, 34, '#18223A', 5, 12)
# 빛줄기 (달 쪽에서 비스듬히)
for k, (x0, w) in enumerate([(150, 16), (182, 10), (210, 20)]):
    shaft = (np.abs((XX - x0) - (YY - 20) * -.45) < w / 2) & (YY > 20) & (YY < 160)
    a = .10 * (1 - (YY - 20) / 160); sel = shaft & (D < a * 6)
    img[sel] = img[sel] * .7 + hx('#8A90C8') * .3
# 땅: 이끼 낀 빈터
ground = YY >= 112
ramp_fill(ground, np.clip((YY - 112) / 70, 0, 1) * .5 + .2 - .25 * np.exp(-((XX - 160) / 70) ** 2 - ((YY - 140) / 22) ** 2), ['#0E1A16', '#14261E', '#1C3426', '#26422E', '#2E5034'])
lit = ground & (np.hypot((XX - 160) / 1.8, YY - 132) < 46)
ramp_fill(lit, 1 - np.hypot((XX - 160) / 1.8, YY - 132) / 46, ['#1C3426', '#26422E', '#30543A', '#3A6444'])
# 풀 포기 · 작은 꽃 · 돌
for _ in range(160):
    x, y = R.randint(0, W), R.randint(116, H - 2); c = hx(R.choice(['#2E5034', '#3A6444', '#44704A']))
    for d in range(R.randint(2, 4)): img[y - d, min(W - 1, x + (d % 2) * (1 if R.rand() < .5 else -1))] = c
for _ in range(18):
    x, y = R.randint(10, W - 10), R.randint(125, H - 4); img[y, x] = hx(R.choice(['#C8A0FF', '#8AC4FF', '#FFE0A0'])); img[y + 1, x] = hx('#2E5034')
def stone(cx, cy, rx, ry):
    m = blob(cx, cy, rx, ry); ramp_fill(m, np.clip(1 - (XX - cx + rx) / (2 * rx) * .6 - (YY - cy + ry) / (2 * ry) * .4, 0, 1), ['#2A2838', '#3A3850', '#4E4C66', '#666480'])
for s in [(52, 160, 7, 4), (276, 150, 9, 5), (98, 168, 5, 3), (230, 170, 6, 3)]: stone(*s)
# 앞쪽 큰 나무 (양옆 틀): 둥근 덩어리 잎 + 굵은 줄기, 우리 맵 나무처럼 단계 음영
LEAF = ['#0C1A14', '#12261C', '#1A3424', '#22442E', '#2C5638']
def tree(cx, base, tw, th, crown):
    trunk = (np.abs(XX - cx) < tw) & (YY > base - th) & (YY <= base)
    ramp_fill(trunk, np.clip(.7 - (XX - cx + tw) / (2 * tw) * .7, 0, 1), ['#140E10', '#22181A', '#322426', '#423234'])
    for (dx, dy, r) in crown:
        m = blob(cx + dx, base - th + dy, r, r * .9); v = 1 - np.hypot(XX - (cx + dx - r * .35), YY - (base - th + dy - r * .35)) / (r * 1.4)
        ramp_fill(m, np.clip(v, 0, 1), LEAF)
tree(18, 150, 7, 110, [(-10, 0, 30), (16, -10, 26), (4, -30, 24), (26, 14, 20)])
tree(302, 156, 8, 112, [(10, 0, 30), (-16, -8, 26), (-2, -30, 24), (-26, 16, 22)])
tree(70, 118, 4, 60, [(-4, 0, 18), (10, -6, 15)])
tree(258, 120, 4, 62, [(4, 0, 18), (-10, -6, 15)])
# 늘어진 덩굴 (위 나뭇가지에서)
def vine(x0, y0, length, sway, col='#2C5638', leaf='#3A6A44'):
    for t in range(length):
        x = int(x0 + sway * math.sin(t / 7)); y = y0 + t
        if 0 <= x < W and 0 <= y < H: img[y, x] = hx(col)
        if t % 5 == 2 and 0 <= x + 1 < W and y < H: img[y, x + 1] = hx(leaf); img[y, x - 1] = hx(leaf) * .8
for (x0, y0, L, s) in [(40, 30, 50, 2), (52, 20, 38, 1.5), (280, 28, 54, 2), (266, 24, 36, 1.5), (300, 40, 60, 2.5)]: vine(x0, y0, L, s)
# 제단 (가운데): 계단 두 단 · 기둥 받침 · 윗판 · 얕은 그릇 · 룬
STONE = ['#24222E', '#34324A', '#46445E', '#5A5874', '#706E8A']
def box(x0, y0, x1, y1, shade_top=True):
    m = (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)
    v = np.clip(.85 - (XX - x0) / max(1, x1 - x0) * .55 - (YY - y0) / max(1, y1 - y0) * .25, 0, 1); ramp_fill(m, v, STONE)
    img[(YY == y0) & (XX >= x0) & (XX < x1)] = hx(STONE[4]); img[(YY == y1 - 1) & (XX >= x0) & (XX < x1)] = hx(STONE[0])
    img[(XX == x1 - 1) & (YY >= y0) & (YY < y1)] = hx(STONE[1])
box(118, 134, 202, 142)   # 아래 계단
box(126, 126, 194, 134)
box(142, 96, 178, 126)    # 기둥
box(132, 88, 188, 96)     # 윗판
box(140, 84, 180, 88)     # 그릇 테
img[(YY >= 85) & (YY < 87) & (XX > 142) & (XX < 178)] = hx('#18161F')   # 그릇 안
# 금 간 자국 · 이끼
for (x, y) in [(150, 100), (151, 101), (151, 102), (152, 103), (170, 110), (169, 111), (169, 112), (130, 138), (131, 139)]: img[y, x] = hx(STONE[0])
for _ in range(60):
    x, y = R.randint(118, 202), R.randint(86, 142)
    if img[y, x].sum() > 90 and img[y, x].sum() < 400 and R.rand() < .6: img[y, x] = hx(R.choice(['#2C5638', '#3A6A44', '#264A30']))
# 룬 (기둥 앞면, 희미한 하늘빛)
RUNE = hx('#5A80C8')
for gx, pts in [(148, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 1)]), (157, [(1, 0), (0, 1), (2, 1), (1, 2), (1, 3)]), (166, [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2), (1, 3)])]:
    for (dx, dy) in pts: img[106 + dy * 2, gx + dx * 2] = RUNE; img[107 + dy * 2, gx + dx * 2] = RUNE * .7
# 제단을 감은 덩굴: 기둥을 비스듬히 휘감고 윗판에서 늘어져요
VC, VL = hx('#2E5A36'), hx('#4A8050')
for t in range(0, 140):
    a = t / 140; x = int(142 + 36 * (.5 + .5 * math.sin(a * math.pi * 3.2))); y = int(126 - a * 40)
    img[y, x] = VC; img[y, min(W - 1, x + 1)] = VC * .8
    if t % 9 == 0: img[y - 1, x] = VL; img[y - 1, x + 1] = VL; img[y, x + 2] = VL * .85
for (x0, L) in [(134, 14), (139, 9), (183, 16), (187, 10), (176, 7)]:
    for t in range(L): x = x0 + (1 if t % 6 < 3 else 0); img[96 + t, x] = VC
    img[96 + L, x0] = VL; img[96 + L - 1, x0 + 1] = VL
for t in range(0, 90):   # 계단을 기어가는 덩굴
    x = 118 + t; y = int(141 - 2 * abs(math.sin(t / 6))); img[y, x] = VC
    if t % 7 == 0: img[y - 1, x] = VL
# 선돌 둘 (양옆, 덩굴)
for (x0, x1, top) in [(96, 108, 92), (212, 224, 98)]:
    box(x0, top, x1, 138)
    img[top + 6: top + 30: 3, x0 + 5] = RUNE * .8
    for t in range(0, 44, 2): img[top + t, x0 + int(5 + 5 * math.sin(t / 5))] = VC
# 안개 띠 (아래)
fog = (YY > 150) & (D < np.clip((YY - 150) / 40, 0, 1) * .45); img[fog] = img[fog] * .7 + hx('#5A6890') * .3
# 반딧불
for _ in range(24):
    x, y = R.randint(20, W - 20), R.randint(60, 160); img[y, x] = hx('#E0FFB0')
    if R.rand() < .4: img[y, x + 1] = hx('#90C870')
# 가장자리 어둡게 (비네트)
v = np.clip(np.hypot((XX - 160) / 180, (YY - 110) / 120) - .55, 0, 1); dark = D < v * 1.6; img[dark] = img[dark] * .55
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
im.save(os.path.join(OUT, 'familiar_altar.png')); im.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, 'familiar_altar_x4.png'))
print('ok')
