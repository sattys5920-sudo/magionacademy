# 요정 시장 연출 컷 배경: 보름달 아래 숲 가장자리 빈터, 버섯 고리와 작은 노점 셋 (320×180)
#   왼쪽 꿀 요정(호박빛 등불·벌집 상자) · 가운데 이슬 요정(큰 잎 차양·유리병) · 오른쪽 가시 요정(장미 덩굴 아치)
#   python3 fairy_market.py → tools/iso/out/fairy_market.png (+ out/fairy_market_x4.png)
import os, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
W, H = 320, 180
R = np.random.RandomState(11)
def hx(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
img = np.zeros((H, W, 3))
YY, XX = np.mgrid[0:H, 0:W]
B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
D = np.tile(B4, (H // 4 + 1, W // 4 + 1))[:H, :W]
def ramp_fill(mask, val, ramp):
    R_ = [hx(c) for c in ramp]; n = len(R_); v = np.clip(val * (n - 1) + D - .5, 0, n - 1).astype(int)
    for k in range(n): s = mask & (v == k); img[s] = R_[k]
def blob(cx, cy, rx, ry): return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1
# 하늘 · 별
ramp_fill(np.ones((H, W), bool), 1 - YY / 115, ['#0E0A22', '#140E2C', '#1A1438', '#22183F', '#2A1E4A'])
for _ in range(90):
    x, y = R.randint(0, W), R.randint(0, 80); img[y, x] = hx('#D8D0FF') * (.45 + R.rand() * .55)
# 큰 보름달 (가운데 위) + 달무리
glow = np.hypot(XX - 160, YY - 34)
halo = (glow < 46) & (D < np.clip((46 - glow) / 46, 0, 1) * .6); img[halo] = img[halo] * .55 + hx('#7A70B8') * .45
m = glow < 22; ramp_fill(m, 1 - np.hypot(XX - 155, YY - 29) / 30, ['#C8C0A8', '#E0D8C0', '#F4EED6', '#FFFBEA'])
for (x, y, r) in [(152, 28, 4), (166, 38, 3), (160, 22, 2), (147, 40, 2)]:
    c = blob(x, y, r, r) & m; img[c] = img[c] * .9
# 먼 숲 실루엣 두 겹
def far_trees(base, h, col, seed, step):
    r = np.random.RandomState(seed)
    for x in range(-10, W + 10, step):
        cy = base - r.randint(int(h * .6), h); rr = r.randint(step - 2, step + 6)
        img[blob(x + r.randint(-3, 3), cy, rr, rr * 1.15)] = hx(col)
    sel = YY > base - 4; img[sel] = hx(col)
far_trees(96, 42, '#1A1838', 4, 14)
far_trees(108, 34, '#172238', 9, 12)
# 땅: 이끼 빈터, 가운데가 달빛에 밝아요
ground = YY >= 112
ramp_fill(ground, np.clip((YY - 112) / 70, 0, 1) * .45 + .2, ['#0E1A16', '#14261E', '#1C3426', '#26422E', '#2E5034'])
lit = ground & (np.hypot((XX - 160) / 2.2, YY - 140) < 40)
ramp_fill(lit, 1 - np.hypot((XX - 160) / 2.2, YY - 140) / 40, ['#1C3426', '#26422E', '#30543A', '#3A6444'])
for _ in range(170):
    x, y = R.randint(0, W), R.randint(116, H - 2); c = hx(R.choice(['#2E5034', '#3A6444', '#44704A']))
    for d in range(R.randint(2, 4)): img[y - d, min(W - 1, x + (d % 2))] = c
# 양옆 큰 나무 틀
LEAF = ['#0C1A14', '#12261C', '#1A3424', '#22442E', '#2C5638']
def tree(cx, base, tw, th, crown):
    trunk = (np.abs(XX - cx) < tw) & (YY > base - th) & (YY <= base)
    ramp_fill(trunk, np.clip(.7 - (XX - cx + tw) / (2 * tw) * .7, 0, 1), ['#140E10', '#22181A', '#322426', '#423234'])
    for (dx, dy, r) in crown:
        mm = blob(cx + dx, base - th + dy, r, r * .9); v = 1 - np.hypot(XX - (cx + dx - r * .35), YY - (base - th + dy - r * .35)) / (r * 1.4)
        ramp_fill(mm, np.clip(v, 0, 1), LEAF)
tree(10, 150, 7, 112, [(-8, 0, 30), (18, -10, 26), (4, -30, 24), (24, 16, 20)])
tree(310, 154, 8, 114, [(8, 0, 30), (-18, -8, 26), (-2, -30, 24), (-24, 18, 22)])
# 버섯 고리 (가운데 땅, 타원으로 늘어선 빛나는 버섯)
def mush(x, y, s, cap, glowc):
    gg = np.hypot(XX - x, YY - y + s) < s * 3.2; sel = gg & (D < .22); img[sel] = img[sel] * .6 + hx(glowc) * .4
    img[(XX >= x - max(1, s // 3)) & (XX <= x + max(0, s // 3)) & (YY > y - s) & (YY <= y)] = hx('#E8E0D0')
    cp = blob(x, y - s, s * 1.4, s * .8) & (YY <= y - s + 1); ramp_fill(cp, np.clip(1 - (YY - (y - s * 1.8)) / (s * 1.6), 0, 1), [cap, glowc, '#FFFFFF'])
for i in range(14):
    a = i / 14 * 2 * math.pi; x = int(160 + 62 * math.cos(a)); y = int(146 + 13 * math.sin(a))
    if 140 < y or abs(x - 160) > 30: mush(x, y, 2 + (i % 3 == 0), R.choice(['#7A3AA8', '#3A68B8', '#B83A6A']), R.choice(['#C890FF', '#90C8FF', '#FF90C0']))
# 노점 공통: 나무 판자 진열대
def counter(x0, x1, y0, col='#5A3A28', top='#7A5236'):
    img[(XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y0 + 10)] = hx(col)
    img[(XX >= x0 - 1) & (XX < x1 + 1) & (YY >= y0) & (YY < y0 + 2)] = hx(top)
    for x in range(x0 + 3, x1, 7): img[y0 + 3:y0 + 10, x] = hx('#3E2618')
    img[y0 + 10:y0 + 16, x0 + 1:x0 + 3] = hx('#3E2618'); img[y0 + 10:y0 + 16, x1 - 3:x1 - 1] = hx('#3E2618')
def lantern(x, y, col):
    gg = np.hypot(XX - x, YY - y) < 12; sel = gg & (D < np.clip((12 - np.hypot(XX - x, YY - y)) / 12, 0, 1) * .55); img[sel] = img[sel] * .55 + hx(col) * .45
    img[y - 2:y + 3, x - 1:x + 2] = hx(col); img[y - 1:y + 2, x] = hx('#FFFFFF'); img[y - 4:y - 2, x] = hx('#3E2618')
# 1) 꿀 요정 노점 (왼쪽): 꽃잎 차양 + 벌집 상자
cx = 72
for t in range(-22, 23):
    y = int(98 + (t / 22) ** 2 * 6); img[y:y + 3, cx + t] = hx('#E8A040' if (t // 4) % 2 else '#F4C870')
img[100:122, cx - 20] = hx('#5A3A28'); img[100:122, cx + 20] = hx('#5A3A28')
counter(cx - 22, cx + 23, 122)
for (x, y) in [(cx - 15, 116), (cx - 4, 116), (cx + 8, 117)]:
    hc = blob(x, y, 4, 3); ramp_fill(hc, np.clip(1 - (YY - y + 3) / 6, 0, 1), ['#A06A18', '#D49A2A', '#F4C860'])
    img[y - 1, x - 2:x + 3:2] = hx('#7A4A10')
lantern(cx - 20, 104, '#FFC060'); lantern(cx + 20, 104, '#FFC060')
# 2) 이슬 요정 노점 (가운데): 큰 잎 차양 + 유리병
cx = 160
lf = blob(cx, 100, 30, 9) & (YY < 104); ramp_fill(lf, np.clip(1 - (YY - 91) / 13, 0, 1), ['#1E5A4A', '#2A7A62', '#3A9A7A', '#5ABA94'])
for t in range(-28, 29, 2): img[int(100 - 7 * (1 - (t / 28) ** 2)), cx + t] = hx('#2A7A62')
img[100:122, cx - 2:cx + 1] = hx('#3E2618')
counter(cx - 24, cx + 25, 122, '#3A4A5A', '#5A6A7A')
for i, (x, c) in enumerate([(cx - 17, '#90D8FF'), (cx - 8, '#B0A0FF'), (cx + 2, '#90FFD8'), (cx + 12, '#FFB0E0')]):
    img[114:122, x - 2:x + 3] = hx(c) * .8; img[112:114, x - 1:x + 2] = hx('#C8D8E8'); img[115:117, x - 1] = hx('#FFFFFF')
    gg = np.hypot(XX - x, YY - 118) < 6; sel = gg & (D < .3); img[sel] = img[sel] * .6 + hx(c) * .4
lantern(cx - 26, 106, '#90D8FF'); lantern(cx + 26, 106, '#90D8FF')
# 3) 가시 요정 노점 (오른쪽): 장미 덩굴 아치
cx = 248
for t in range(0, 180):
    a = t / 180 * math.pi; x = int(cx - 22 * math.cos(a)); y = int(122 - 28 * math.sin(a))
    img[y, x] = hx('#2E4A2A'); img[y, min(W - 1, x + 1)] = hx('#22381E')
    if t % 14 == 0: rb = blob(x, y, 2, 2); img[rb] = hx(R.choice(['#C02858', '#E04878', '#8A1A40']))
counter(cx - 22, cx + 23, 122, '#3A2034', '#5A3050')
for (x, y) in [(cx - 14, 117), (cx - 2, 116), (cx + 10, 117)]:
    img[y:y + 5, x - 2:x + 3] = hx('#4A2A44'); img[y - 2:y, x - 1:x + 2] = hx('#E04878')
lantern(cx - 22, 104, '#E070C0'); lantern(cx + 22, 104, '#E070C0')
# 작은 나무 표지판 (왼쪽 앞): 「요정 시장」 대신 별·달 문양
img[134:150, 26:28] = hx('#3E2618'); img[128:136, 18:36] = hx('#6A4A2E'); img[128, 18:36] = hx('#8A6A44')
for (x, y) in [(22, 131), (23, 132), (22, 133), (30, 130), (31, 131), (29, 131), (30, 132), (31, 133)]: img[y, x] = hx('#FFE8A0')
# 반딧불 · 안개 · 비네트
for _ in range(30):
    x, y = R.randint(20, W - 20), R.randint(60, 165); img[y, x] = hx(R.choice(['#E0FFB0', '#FFE0F0', '#C0E0FF']))
fog = (YY > 152) & (D < np.clip((YY - 152) / 36, 0, 1) * .45); img[fog] = img[fog] * .7 + hx('#5A6890') * .3
v = np.clip(np.hypot((XX - 160) / 180, (YY - 105) / 120) - .55, 0, 1); dark = D < v * 1.6; img[dark] = img[dark] * .55
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
im.save(os.path.join(OUT, 'fairy_market.png')); im.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, 'fairy_market_x4.png'))
print('ok')
