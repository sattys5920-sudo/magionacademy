# 제미나이 아기 고양이 걷기 그림 (1696 × 624 · 3 줄 × 8 칸 · 가짜 체크무늬 배경) → 64 칸 · 3 × 8 (public/art/catbaby64.png)
#   칸: 0 · 1 정면 걷기 / 2 · 3 뒤 걷기 / 4 · 5 · 6 옆(오른쪽) 걷기 / 7 정면 앉기 · 줄: 1 단계 부스스 · 2 단계 조금 정리 · 3 단계 회원
from collections import deque
from PIL import Image
D = __file__.rsplit('/', 1)[0]; ROOT = D.rsplit('/tools/', 1)[0]
src = Image.open(D + '/baby_walk_source.webp').convert('RGB'); W, H = src.size; p = src.load()
def bgish(c): return max(c) - min(c) < 22 and min(c) > 175
bg = [[False] * H for _ in range(W)]
CW, CH = W / 8, H / 3
def flood(seeds):
    q = deque(seeds)
    while q:
        x, y = q.popleft()
        if bg[x][y] or not bgish(p[x, y]): continue
        bg[x][y] = True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and not bg[nx][ny]: q.append((nx, ny))
flood([(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)] + [(int(c * CW), y) for c in range(9) for y in range(H) if int(c * CW) < W] + [(x, int(r * CH)) for r in range(4) for x in range(W) if int(r * CH) < H])
# 다리 · 꼬리 사이에 갇힌 체크무늬 (밝은 회색과 흰색이 섞인 덩어리)
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
        if len(comp) > 30 and grey > len(comp) * .2 and white > len(comp) * .2:
            for x, y in comp: bg[x][y] = True
rgba = Image.new('RGBA', (W, H)); r = rgba.load()
for x in range(W):
    for y in range(H):
        if not bg[x][y]: r[x, y] = p[x, y] + (255,)
cells = [[rgba.crop((round(c * CW), round(rw * CH), round((c + 1) * CW), round((rw + 1) * CH))) for c in range(8)] for rw in range(3)]
cells = [[cl.crop(cl.getbbox()) if cl.getbbox() else cl for cl in row] for row in cells]
# 크기: 지금 게임의 아기 고양이(회원 · 앉은 모습) 키에 3 단계 앉기 칸을 맞춰요
cur = Image.open(ROOT + '/public/art/cat64.png').convert('RGBA').crop((2 * 64, 0, 3 * 64, 64)); curH = cur.getbbox()[3] - cur.getbbox()[1]
k = curH / cells[2][7].height
out = Image.new('RGBA', (64 * 8, 64 * 3))
for rw in range(3):
    for c in range(8):
        cl = cells[rw][c]; w, h = max(1, round(cl.width * k)), max(1, round(cl.height * k))
        s = cl.resize((w, h), Image.BOX); a = s.split()[3].point(lambda v: 255 if v > 110 else 0); s.putalpha(a)
        s = s.convert('RGB').quantize(colors=16, method=Image.MEDIANCUT).convert('RGBA'); s.putalpha(a)
        out.alpha_composite(s, (c * 64 + (64 - w) // 2, rw * 64 + 64 - 2 - h))
out.save(ROOT + '/public/art/catbaby64.png'); out.save(ROOT + '/public/art/catbaby64.webp', lossless=True); out.save(D + '/baby_walk64.png')
big = Image.new('RGBA', out.size, (40, 32, 60, 255)); big.alpha_composite(out); big.resize((out.width * 4, out.height * 4), Image.NEAREST).save(D + '/baby_walk64_x4.png')
print('k', round(k, 3), 'curH', curH)
