# 이벤트 「유령 등불 찾기」 그림 정리: 이미지 생성 결과(ev4_src/)에서 배경 체크무늬를 빼고 게임용 파일로 → public/art/ev4_ghost.png(초상화 5칸) · ev4_lantern.png(등불 2칸) · ev4_lamp_00~11.png(방 장식 12색)
import colorsys, os
import numpy as np
from collections import deque
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ART = '../../public/art/'
def neutral_flood(rgb, seeds, tol_chroma=10, extra=None):      # 가장자리에서 시작해 회색 체크무늬만 지워요
    H, W, _ = rgb.shape; ch = rgb.max(2) - rgb.min(2); ok = ch <= tol_chroma
    if extra is not None: ok &= extra
    seen = np.zeros((H, W), bool); q = deque()
    for (x, y) in seeds:
        if ok[y, x] and not seen[y, x]: seen[y, x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and ok[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((nx, ny))
    return seen
# ---- 1) 꼬마 유령 초상화: 5칸을 칸마다 잘라 260×266 칸에 맞춰 가로 한 줄로 ----
src = Image.open('ev4_src/ghost_portrait_src.png').convert('RGB'); a = np.array(src).astype(int)
cells = [(49, 311), (354, 617), (661, 923), (966, 1230), (1273, 1535)]; y0, y1 = 184, 484
strip = Image.new('RGBA', (1300, 266), (0, 0, 0, 0))
for i, (x0, x1) in enumerate(cells):
    sub = a[y0:y1, x0 + 2:x1 - 2]; H, W, _ = sub.shape
    seeds = [(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] + [(0, y) for y in range(H)] + [(W - 1, y) for y in range(H)]
    bg = neutral_flood(sub, seeds, 12)
    # 윤곽 안에 갇혀 남은 체크무늬 조각(밝은 칸·어두운 칸 두 색이 섞인 것)만 지워요
    from scipy import ndimage
    lumsub = sub.sum(2) / 3; neu = ((sub.max(2) - sub.min(2)) <= 14) & (lumsub > 150) & ~bg
    lab, n = ndimage.label(neu)
    for k in range(1, n + 1):
        m = lab == k
        if m.sum() < 30: continue
        lo = (lumsub[m] < 230).mean(); hi = (lumsub[m] >= 240).mean()
        if lo > .25 and hi > .25: bg |= m
    # 가장자리 정리: 체크무늬가 섞인 한 겹을 깎고, 가장자리 색은 안쪽 색으로 채우고, 알파를 살짝 부드럽게(누끼 깔끔하게)
    solid = ~bg
    ys, xs = np.nonzero(solid); x_lo, x_hi = xs.min(), xs.max(); lumsub2 = sub.sum(2) / 3; chroma = sub.max(2) - sub.min(2)
    zone = np.zeros_like(solid); zone[:, int(x_lo + (x_hi - x_lo) * .78):] = True                      # 오른쪽 가장자리(작은 등불 걸이 둘레): 남은 회색·흰 체크무늬 조각 제거
    solid &= ~(zone & (chroma <= 12) & (lumsub2 > 195))
    g_ = (sub[..., 1] - sub[..., 0] > 60) & (chroma > 70); g_ &= np.arange(solid.shape[1])[None, :] > x_lo + (x_hi - x_lo) * .6      # 작은 초록 등불 걸이(진한 초록)를 찾아
    if g_.sum() > 40:
        gy, gx = np.nonzero(g_); cx0, cx1, cy0, cy1 = gx.min() - 7, gx.max() + 7, gy.min() - 7, gy.max() + 7; mid = (gx.min() + gx.max()) // 2
        box = np.zeros_like(solid); box[max(cy0, 0):cy1, mid:cx1] = True; solid &= ~(box & (chroma <= 28) & (lumsub2 > 200) & ~g_)     # 그 오른쪽 둘레의 옅은 네모 조각을 지워요
    solid = ndimage.binary_opening(solid, iterations=1); solid = ndimage.binary_erosion(solid, iterations=1)
    lab2, n2 = ndimage.label(solid, structure=np.ones((3, 3)))
    for k in range(1, n2 + 1):                                                                         # 작고 어두운 먼지(틀 조각) 제거
        m = lab2 == k
        if m.sum() < 160 and lumsub2[m].mean() < 130: solid[m] = False
    idx = ndimage.distance_transform_edt(~solid, return_distances=False, return_indices=True); filled = sub[idx[0], idx[1]]
    alpha = np.clip(ndimage.gaussian_filter(solid.astype(float), .8) * 1.35 - .15, 0, 1) * 255
    rgba = np.dstack([filled, alpha]).astype(np.uint8); im = Image.fromarray(rgba, 'RGBA'); bb = im.getbbox()
    im = im.crop(bb); k = min(250 / im.width, 258 / im.height, 1.0); im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    strip.alpha_composite(im, (i * 260 + (260 - im.width) // 2, 262 - im.height))
strip.save(ART + 'ev4_ghost.png')
# ---- 2) 찾아야 하는 등불: 2칸 ----
src = Image.open('ev4_src/lantern_src.png').convert('RGB'); a = np.array(src).astype(int); H, W, _ = a.shape
lum = a.sum(2) / 3
seeds = [(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] + [(0, y) for y in range(H)] + [(W - 1, y) for y in range(H)]
bg = neutral_flood(a, seeds, 14, extra=(lum > 55) & (lum < 150))
rgba = np.dstack([a, np.where(bg, 0, 255)]).astype(np.uint8); L = Image.fromarray(rgba, 'RGBA')
# 은은한 땅 빛(체크무늬와 섞인 초록 점)은 따로 만든 동그란 빛으로 바꿔요: 초록이 아닌 회색 찌꺼기를 투명하게
p = np.array(L).astype(int)
mxp, mnp = p[..., :3].max(2), p[..., :3].min(2); sat = np.where(mxp > 0, (mxp - mnp) / np.maximum(mxp, 1), 0); lm = p[..., :3].sum(2) / 3
p[(sat < .42) & (lm > 60) & (lm < 165) & (p[..., 3] > 0), 3] = 0
from scipy import ndimage
lab, n = ndimage.label(p[..., 3] > 0, structure=np.ones((3, 3)))
for k in range(1, n + 1):          # 큰 덩어리(등불)와 밝은 반짝이만 남기고 먼지는 지워요
    m = lab == k; area = m.sum(); bright = (lm[m] > 185).mean() > .6 and (sat[m] > .25).mean() > .5
    if area < 600 and not (bright and area >= 6): p[m, 3] = 0
L = Image.fromarray(p.astype(np.uint8), 'RGBA')
half = W // 2; fr = []
for i in range(2):
    part = L.crop((i * half, 0, (i + 1) * half, H)); bb = part.getbbox(); fr.append(part.crop(bb) if bb else part)
fh = max(f.height for f in fr); fw = max(f.width for f in fr)
sheet = Image.new('RGBA', (fw * 2, fh), (0, 0, 0, 0))
for i, f in enumerate(fr): sheet.alpha_composite(f, (i * fw + (fw - f.width) // 2, fh - f.height))
sheet.save(ART + 'ev4_lantern.png')
# ---- 3) 유령 등불 장식: 배경색을 빼고 12색으로 ----
src = Image.open('ev4_src/lamp_src.png').convert('RGB'); a = np.array(src).astype(int); H, W, _ = a.shape; bgc = np.array([64, 50, 85])
dist = np.sqrt(((a - bgc) ** 2).sum(2)); glowish = (a[..., 1] > a[..., 2] + 5) & (dist < 100)
alpha = np.where(dist < 6, 0, np.where(glowish, np.clip(dist / 150, 0, .55) * 255, 255))
rgb = a.copy(); rgb[glowish & (dist >= 6)] = (63, 224, 160)
alpha[int(H * .88):, int(W * .8):] = 0      # 생성 그림 오른쪽 아래의 작은 별 표시 제거
lamp = Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), 'RGBA'); lamp = lamp.crop(lamp.getbbox())
def recolor(img, target_h, base_h=155.0):
    arr = np.array(img).astype(float) / 255; r, g, b, al = [arr[..., i] for i in range(4)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b); v = mx; s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    d = mx - mn + 1e-9; h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    sel = (h >= 125) & (h <= 215) & (s > .18)                      # 초록·청록 계열(유리, 불빛, 기둥, 리본)만 돌려요. 금색 뚜껑, 분홍 볼, 하얀 얼굴은 그대로
    h2 = np.where(sel, (h + (target_h - base_h)) % 360, h)
    hh = h2 / 60; c = v * s; x = c * (1 - np.abs(hh % 2 - 1)); m = v - c; z = np.zeros_like(c)
    idx = np.floor(hh).astype(int) % 6; R = np.choose(idx, [c, x, z, z, x, c]); G = np.choose(idx, [x, c, c, x, z, z]); B = np.choose(idx, [z, z, x, c, c, x])
    out = np.dstack([R + m, G + m, B + m, al]); return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA')
LAMP = [('빨강', 0), ('주황', 30), ('노랑', 60), ('연두', 90), ('초록', 120), ('민트', 150), ('하늘', 180), ('파랑', 210), ('남색', 240), ('보라', 270), ('자홍', 300), ('분홍', 330)]
import json
for i, (nm, h) in enumerate(LAMP): recolor(lamp, h).save(ART + f'ev4_lamp_{i:02d}.png')
json.dump([n for n, _ in LAMP], open('ev4_src/lamp_names.json', 'w'), ensure_ascii=False)
print('ok', strip.size, sheet.size, lamp.size)
