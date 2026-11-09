# 제미나이가 그린 고양이 여덟 (가짜 체크무늬 배경 · 2000 × 240) → 배경 지우기 · 한 마리씩 자르기 · 32 칸으로 줄이기
#   python3 tools/catmeet/gemini/cut.py [칸 크기 32]
import sys
from collections import deque
from PIL import Image
D = __file__.rsplit('/', 1)[0]; N = int(sys.argv[1]) if len(sys.argv) > 1 else 32; TH = int(sys.argv[2]) if len(sys.argv) > 2 else N - 2   # TH: 가장 큰 어른 고양이 키 (나비와 같은 픽셀 크기면 64 칸에 44)
OL = (47, 12, 24, 255)
src = Image.open(D + '/source.webp').convert('RGB'); W, H = src.size; p = src.load()
def bgish(c): r, g, b = c; return max(c) - min(c) < 22 and min(c) > 175
bg = [[False] * H for _ in range(W)]; q = deque()
for x in range(W):
    for y in (0, H - 1): q.append((x, y))
for y in range(H):
    for x in (0, W - 1): q.append((x, y))
while q:
    x, y = q.popleft()
    if bg[x][y] or not bgish(p[x, y]): continue
    bg[x][y] = True
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H and not bg[nx][ny]: q.append((nx, ny))
# 꼬리 고리처럼 고양이에 둘러싸인 체크무늬: 밝은 회색(200 ~ 220)과 흰색이 섞인 덩어리면 배경이에요
seen = [[False] * H for _ in range(W)]
for sx in range(W):
    for sy in range(H):
        if bg[sx][sy] or seen[sx][sy] or not bgish(p[sx, sy]): continue
        comp = []; q = deque([(sx, sy)]); seen[sx][sy] = True
        while q:
            x, y = q.popleft(); comp.append((x, y))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and not seen[nx][ny] and not bg[nx][ny] and bgish(p[nx, ny]): seen[nx][ny] = True; q.append((nx, ny))
        grey = sum(1 for x, y in comp if 198 <= p[x, y][0] <= 222); white = sum(1 for x, y in comp if p[x, y][0] >= 245)
        if len(comp) > 30 and grey > len(comp) * .25 and white > len(comp) * .25 and all(860 <= x <= 1090 for x, y in comp):   # 삼색이 꼬리 고리만 (할배 흰 눈썹이 지워지지 않게)
            for x, y in comp: bg[x][y] = True
rgba = Image.new('RGBA', (W, H)); r = rgba.load()
for x in range(W):
    for y in range(H):
        if not bg[x][y]: r[x, y] = p[x, y] + (255,)
cols = [any(r[x, y][3] for y in range(H)) for x in range(W)]
segs = []; x = 0
while x < W:
    if cols[x]:
        s = x
        while x < W and cols[x]: x += 1
        if x - s > 20: segs.append((s, x))
    else: x += 1
print('segments', len(segs), segs)
crops = [rgba.crop((a, 0, b, H)) for a, b in segs]; crops = [c.crop(c.getbbox()) for c in crops]
tallest = max(c.height for c in crops[:5]); widest = max(c.width for c in crops)
k = min(TH / tallest, N / widest)   # 어른 고양이 중 가장 큰 고양이가 칸 높이에 맞게 · 아기는 같은 배율이라 작아요
out = []
for ci, c in enumerate(crops):
    kk = k * (.78 if ci >= 5 else 1)   # 아기 고양이 셋은 더 작게
    w, h = max(1, round(c.width * kk)), max(1, round(c.height * kk))
    s = c.resize((w, h), Image.BOX)
    a = s.split()[3].point(lambda v: 255 if v > 110 else 0); s.putalpha(a)
    s = s.convert('RGB').quantize(colors=20 if N >= 48 else 14, method=Image.MEDIANCUT).convert('RGBA'); s.putalpha(a)
    cell = Image.new('RGBA', (N, N)); cell.alpha_composite(s, ((N - w) // 2, N - h)); out.append(cell)
    rgba_c = c
sheet = Image.new('RGBA', (N * len(out), N))
for i, c in enumerate(out): sheet.alpha_composite(c, (i * N, 0))
sheet.save(f'{D}/cats{N}.png'); rgba.save(D + '/source_cut.png')
big = Image.new('RGB', (sheet.width * 6, sheet.height * 6), (40, 32, 60)); big.paste(sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST), (0, 0), sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST)); big.save(f'{D}/cats{N}_x6.png')
