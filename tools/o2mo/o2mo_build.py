# 오투모 그림 만들기: 제미나이 그림(바둑판이 그려진 PNG) → 게임 NPC 한 줄(1280 × 64) + 초상화 5 표정(320 × 64)
#   python3 tools/o2mo/o2mo_build.py   (tools/o2mo/gemini_source.png · gemini_face_source.png → o2mo_sheet.png · o2mo_face.png)
import os
from collections import deque
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
OUTLINE = (26, 16, 36, 255)
def isbg(c):   # 바둑판(흰색 · 밝은 회색, 색이 거의 없음)
    r, g, b, a = c; mx, mn = max(r, g, b), min(r, g, b); return mn >= 165 and mx - mn <= 14
def fringe(c):   # 가장자리에 남은 밝은 회색 번짐 (원래 그림 가장자리는 진한 테두리라서 밝으면 번짐이에요)
    r, g, b, a = c; mx, mn = max(r, g, b), min(r, g, b); return a and mn >= 120 and mx - mn <= 40
def cut(c, from_bottom=True):
    P = c.load(); w, h = c.size; q = deque([(x, 0) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)] + ([(x, h - 1) for x in range(w)] if from_bottom else [(x, h - 1) for x in range(w) if isbg(P[x, h - 1])]))
    seen = set()
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h): continue
        seen.add((x, y))
        if not isbg(P[x, y]): continue
        P[x, y] = (0, 0, 0, 0); q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    for _ in range(4):   # 번짐 깎기: 투명과 맞닿은 밝은 회색을 네 겹까지
        rm = [(x, y) for y in range(h) for x in range(w) if fringe(P[x, y]) and any(0 <= x + a < w and 0 <= y + b < h and P[x + a, y + b][3] == 0 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        if not rm: break
        for p in rm: P[p] = (0, 0, 0, 0)
    return c
def tidy(im, cell=64):   # 작은 티 지우기 + 바깥 진한 테두리 한 겹
    W, H = im.size; P = im.load(); seen = set()
    for y in range(H):
        for x in range(W):
            if not P[x, y][3] or (x, y) in seen: continue
            comp = []; st = [(x, y)]; seen.add((x, y))
            while st:
                a, b = st.pop(); comp.append((a, b))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        q = (a + dx, b + dy)
                        if 0 <= q[0] < W and 0 <= q[1] < H and q not in seen and P[q][3] and q[0] // cell == x // cell: seen.add(q); st.append(q)
            if len(comp) < 8:
                for p in comp: P[p] = (0, 0, 0, 0)
    A = lambda x, y: 0 <= x < W and 0 <= y < H and P[x, y][3] > 0
    for y in range(H):   # 가장자리 칸이 밝은 회색이면 테두리 색으로
        for x in range(W):
            if A(x, y) and fringe(P[x, y]) and any(not A(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): P[x, y] = OUTLINE
    out = [(x, y) for y in range(H) for x in range(W) if not A(x, y) and x % cell not in (0, cell - 1) and any(A(x + a, y + b) and sum(P[x + a, y + b][:3]) > 220 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for p in out: P[p] = OUTLINE
    return im
# ---------- 걷기 시트 (5 칸 × 4 줄: 앞 · 뒤 · 오른쪽 · 왼쪽 → 게임: 앞 · 뒤 · 왼쪽 · 오른쪽) ----------
src = Image.open(os.path.join(D, 'gemini_source.png')).convert('RGBA'); W, H = src.size; cw, ch = W / 5, H / 4
cells = [[cut(src.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))) for c in range(5)] for r in range(4)]
k = 50 / max(cells[r][c].getbbox()[3] - cells[r][c].getbbox()[1] for r in range(4) for c in range(5))
sheet = Image.new('RGBA', (64 * 20, 64))
for d, row in enumerate((0, 1, 3, 2)):
    fr = [cells[row][c] for c in range(5)]
    if row in (2, 3): fr = [fr[1]] + fr[1:]   # 옆모습 서 있기 칸은 몸이 앞을 봐서 걷기 첫 칸으로
    for i, f in enumerate(fr):
        bb = f.getbbox(); cr = f.crop(bb); sm = cr.resize((max(1, round(cr.width * k)), max(1, round(cr.height * k))), Image.NEAREST); w, h = sm.size
        hb = sm.crop((0, 0, w, int(h * .55))).getbbox(); cx = (hb[0] + hb[2]) / 2 if hb else w / 2
        sheet.alpha_composite(sm, (d * 320 + i * 64 + round(32 - cx), 62 - h))
tidy(sheet).save(os.path.join(D, 'o2mo_sheet.png'))
# ---------- 초상화 (5 칸 × 2 줄 중 위 줄: 기본 · 웃음 · 놀람 · 슬픔 · 당황) ----------
fs = Image.open(os.path.join(D, 'gemini_face_source.png')).convert('RGBA'); W, H = fs.size; cw, ch = W / 5, H / 2
fc = [cut(fs.crop((int(c * cw), 0, int((c + 1) * cw), int(ch))), from_bottom=False) for c in range(5)]
k = 62 / max(c.getbbox()[2] - c.getbbox()[0] for c in fc)
face = Image.new('RGBA', (320, 64))
for i, c in enumerate(fc):
    b = c.getbbox(); cr = c.crop((b[0], b[1], b[2], c.size[1])); sm = cr.resize((round(cr.width * k), round(cr.height * k)), Image.NEAREST)
    face.alpha_composite(sm, (i * 64 + (64 - sm.width) // 2, max(0, 64 - sm.height)))
tidy(face).save(os.path.join(D, 'o2mo_face.png'))
print('ok')
# ---------- 게임에 넣기: NPC 그림(art/npcs.png · webp) 14 번째 줄(spr 13) · 초상화(art/portraits/otumo.png, 게임 표정 순서: 기본 · 웃음 · 화남 · 놀람 · 부끄러움) ----------
#   tools/iso/npc_art.py로 npcs.png를 다시 만들면 이 줄이 빠져요 → 그 뒤에 이 파일을 한 번 더 돌려요
ROOT = os.path.join(D, '..', '..', 'public', 'art')
npcs = Image.open(os.path.join(ROOT, 'npcs.png')).convert('RGBA'); ROW = 13
big = Image.new('RGBA', (1280, max(npcs.height, (ROW + 1) * 64))); big.alpha_composite(npcs.crop((0, 0, 1280, min(npcs.height, ROW * 64))), (0, 0)); big.alpha_composite(sheet, (0, ROW * 64))
big.save(os.path.join(ROOT, 'npcs.png')); big.save(os.path.join(ROOT, 'npcs.webp'), lossless=True, method=6, quality=100)
port = Image.new('RGBA', (320, 64))
for slot, src_i in enumerate((0, 1, 4, 2, 3)):   # 기본 · 웃음 · 화남(당황 > <) · 놀람 · 부끄러움(슬픔 · 미안할 때)
    port.alpha_composite(face.crop((src_i * 64, 0, src_i * 64 + 64, 64)), (slot * 64, 0))
port.save(os.path.join(ROOT, 'portraits', 'otumo.png')); print('game art ok', big.size)
