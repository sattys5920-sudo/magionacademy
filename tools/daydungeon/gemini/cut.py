# 제미나이 요일 보스 그림 (회색 배경 한 장) → 배경 지우기 · 열 칸 자르기 · 64 칸으로 줄이기 (레이드 보스와 같은 틀)
#   python3 tools/daydungeon/gemini/cut.py   → bosses64.png (640 × 64) · bosses64_x4.png · public/art/day_bosses.png
#   칸: [바위등 서기, 바위등 기술, 송곳니 서기, 송곳니 기술, 독버섯 할멈 서기, 기술, 낮과 밤 서기, 기술, 태엽공 서기, 기술]
import shutil
from collections import Counter, deque
from PIL import Image
D = __file__.rsplit('/', 1)[0]; ROOT = D.rsplit('/tools/', 1)[0]
src = Image.open(D + '/source.webp').convert('RGB'); W, H = src.size; p = src.load()
bgc = Counter(src.get_flattened_data() if hasattr(src, 'get_flattened_data') else src.getdata()).most_common(1)[0][0]
def near_bg(c): return sum(abs(c[i] - bgc[i]) for i in range(3)) < 36
bg = [[False] * H for _ in range(W)]; q = deque([(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)])
while q:
    x, y = q.popleft()
    if bg[x][y] or not near_bg(p[x, y]): continue
    bg[x][y] = True
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H and not bg[nx][ny]: q.append((nx, ny))
rgba = Image.new('RGBA', (W, H)); r = rgba.load()
for x in range(W):
    for y in range(H):
        if not bg[x][y]: r[x, y] = p[x, y] + (255,)
cols = [sum(1 for y in range(H) if r[x, y][3]) for x in range(W)]
segs = []; x = 0
while x < W:
    if cols[x] > 2:
        s = x
        while x < W and cols[x] > 2: x += 1
        if x - s > 12: segs.append((s, x))
    else: x += 1
print('segments', len(segs), segs)
while len(segs) < 10:   # 붙어 있는 두 칸: 가장 넓은 덩어리를 가운데쯤 가장 얇은 세로줄에서 나눠요
    i = max(range(len(segs)), key=lambda j: segs[j][1] - segs[j][0]); a0, b0 = segs[i]; lo, hi = a0 + (b0 - a0) * 3 // 10, a0 + (b0 - a0) * 7 // 10
    cut = min(range(lo, hi), key=lambda x: cols[x]); segs[i:i + 1] = [(a0, cut), (cut, b0)]; print('split', a0, b0, 'at', cut)
crops = []
for a, b in segs:
    c = rgba.crop((a, 0, b, H)); bb = c.getbbox(); crops.append(c.crop(bb) if bb else c)
k = min(62 / max(c.height for c in crops), 64 / max(c.width for c in crops))
out = Image.new('RGBA', (640, 64))
for i, c in enumerate(crops):
    w, h = max(1, round(c.width * k)), max(1, round(c.height * k))
    s = c.resize((w, h), Image.BOX); a = s.split()[3].point(lambda v: 255 if v > 110 else 0); s.putalpha(a)
    s = s.convert('RGB').quantize(colors=24, method=Image.MEDIANCUT).convert('RGBA'); s.putalpha(a)
    out.alpha_composite(s, (i * 64 + (64 - w) // 2, 63 - h))
out.save(D + '/bosses64.png'); out.save(ROOT + '/public/art/day_bosses.png'); out.save(ROOT + '/public/art/day_bosses.webp', lossless=True)
big = Image.new('RGBA', out.size, (40, 32, 60, 255)); big.alpha_composite(out); big.resize((out.width * 3, out.height * 3), Image.NEAREST).save(D + '/bosses64_x3.png')
print('k', round(k, 3))
