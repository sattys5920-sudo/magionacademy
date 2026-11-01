# 시안: 겨울 뜨개질 아이템을 LPC 그대로 (게임 아바타 부품 · LPC 원본 시트를 털실 색 + 뜨개 결로 다시 칠하기)
#   목도리(게임 neck_004) · 방울 모자(게임 hat_001) · 포근 숄(LPC shoulders/mantal) · 니트 스웨터(LPC longsleeve2) · 털 귀마개(LPC headband/thick + 귀 솜방울)
#   NPC 뜨개 인형: 각 NPC의 LPC 정면 그림을 머리 크게 · 몸 작게 줄이고 뜨개 결을 입혀요
#   python3 knit_lpc.py <LPC 저장소> <아바타 정면 png> <NPC 정면 png 폴더> <저장 폴더>
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
LPC, AVP, NPCD, OUTD = sys.argv[1:5]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
s = open(os.path.join(ROOT, 'public', 'world.js')).read(); i = s.index('const AVM = ') + 12; AVM, _ = json.JSONDecoder().raw_decode(s[i:])
CL = AVM['pal']['cloth']; hx = lambda h: tuple(int(h[k:k + 2], 16) for k in (1, 3, 5))
RAMP = {k: [hx(c) for c in v] for k, v in CL.items()}
YARN = {'빨강': 'red', '하양': 'white', '파랑': 'blue', '노랑': 'p_mustard', '초록': 'green', '분홍': 'p_pink', '남색': 'navy'}
def L(c): return .3 * c[0] + .59 * c[1] + .11 * c[2]
def frame(path, row=0, col=0, lpc=False):
    im = Image.open(path).convert('RGBA')
    if lpc: return im.crop((0, 128, 64, 192))   # LPC walk: 아래 보기 줄(3 번째) 첫 칸
    return im.crop((col * 64, row * 64, col * 64 + 64, row * 64 + 64))
def knit_recolor(im, pick, texture=True):
    """밝기 순서대로 털실 색 단계에 맞춰 칠하고 (LPC 음영 단계 유지), V 모양 코 결을 한 단계 어둡게 넣어요. pick(x, y) → 색 이름"""
    out = im.copy(); P = im.load(); Q = out.load(); px = [(x, y) for y in range(64) for x in range(64) if P[x, y][3] > 0]
    if not px: return out
    ls = sorted(set(round(L(P[x, y][:3])) for x, y in px)); lo, hi = ls[0], ls[-1]
    for x, y in px:
        r = RAMP[YARN[pick(x, y)]]; n = len(r); v = (L(P[x, y][:3]) - lo) / max(1, hi - lo)
        k = 0 if v < .08 else min(n - 1, 1 + int(v * (n - 1)))   # 제일 어두운 건 테두리
        if texture and k >= 2 and ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1 and (x + y) % 4 == 2)): k -= 1
        Q[x, y] = r[k] + (P[x, y][3],)
    return out
def over(base, *layers):
    o = base.copy()
    for l in layers: o.alpha_composite(l)
    return o
base = Image.open(AVP).convert('RGBA')
ART = os.path.join(ROOT, 'public', 'art', 'lpc')
SP = os.path.join(LPC, 'spritesheets')
# 부품 (정면 한 칸)
scarf = frame(os.path.join(ART, 'neck_004.png'))
hatb, hatp = frame(os.path.join(ART, 'hat_001.png'), 0), frame(os.path.join(ART, 'hat_001.png'), 1)
mantal = frame(os.path.join(SP, 'shoulders', 'mantal', 'thin', 'walk.png'), lpc=True)
sweater = frame(os.path.join(SP, 'torso', 'clothes', 'longsleeve', 'longsleeve2', 'female', 'walk.png'), lpc=True)
band = frame(os.path.join(SP, 'hat', 'headband', 'thick', 'adult', 'walk.png'), lpc=True) if os.path.exists(os.path.join(SP, 'hat', 'headband', 'thick', 'adult', 'walk.png')) else None
def bbox_y(im):
    b = im.getbbox(); return b
def part_from(withp, neutral=True):
    """게임 합성기로 부품을 씌운 그림 - 안 씌운 그림 = 부품 픽셀 (무채색만: 머리카락 · 피부는 빼요)"""
    w = Image.open(withp).convert('RGBA'); P, B = w.load(), base.load(); o = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); Q = o.load()
    for y in range(64):
        for x in range(64):
            c, d0 = P[x, y], B[x, y]
            if c[3] and c != d0 and (not neutral or max(c[:3]) - min(c[:3]) < 26): Q[x, y] = c
    return w, o
HAT_W, HAT_L = part_from(os.path.join(NPCD, 'av_me_hat.png')); NECK_W, NECK_L = part_from(os.path.join(NPCD, 'av_me_neck.png'), False)
def mk_scarf(a, b): return ('full', NECK_W, knit_recolor(NECK_L, lambda x, y: a if (x // 2 + y // 3) % 2 == 0 else b))
def mk_hat(a, b):
    bb = HAT_L.getbbox(); return ('full', HAT_W, knit_recolor(HAT_L, lambda x, y: b if y >= bb[3] - 2 or y <= bb[1] + 2 else a))
gloves = frame(os.path.join(SP, 'arms', 'hands', 'gloves', 'thin', 'walk.png'), lpc=True)
BA = base.load()
def head_rows():
    """머리(머리카락 포함) 윗부분의 줄마다 왼쪽 · 오른쪽 끝 (양 갈래 머리는 빼고 x 20 ~ 44 안에서)"""
    rows = {}
    for y in range(64):
        xs = [x for x in range(20, 45) if BA[x, y][3]]
        if xs: rows[y] = (min(xs), max(xs))
    return rows
HR_ = head_rows(); TOP = min(HR_)
def lpc_fill(lay, pts, ramp, light=(-1, -1)):
    """LPC처럼: 덩어리 안에서 왼쪽 위가 밝고 오른쪽 아래가 어둡게 3 단 + 뜨개 결 + 둘레 진한 테두리"""
    if not pts: return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2; w, h = max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)); P = lay.load()
    for x, y in pts:
        v = ((x - cx) / w * light[0] + (y - cy) / h * light[1])   # 클수록 밝음
        k = 4 if v > .35 else 3 if v > -.1 else 2
        if ((x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1 and (x + y) % 4 == 2)) and k > 2: k -= 1
        P[x, y] = ramp[min(len(ramp) - 1, k)] + (255,)
    S_ = set(pts)
    for x, y in pts:
        for a_, b_ in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + a_, y + b_)
            if q not in S_ and 0 <= q[0] < 64 and 0 <= q[1] < 64 and not P[q][3]: P[q] = ramp[0] + (255,)
def mk_hat(a, b):
    """머리 모양에 맞춰 푹 눌러 쓴 비니: 머리카락 윗부분을 덮고 눈썹 위까지 · 고무단 · 방울"""
    lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); BRIM = TOP + 11; dome, brim = [], []
    for y in range(TOP - 1, BRIM + 1):
        x0, x1 = HR_.get(max(TOP, y), (30, 34)); x0 -= 1; x1 += 1
        if y == TOP - 1: x0, x1 = x0 + 4, x1 - 4
        for x in range(x0, x1 + 1): (brim if y >= BRIM - 2 else dome).append((x, y))
    lpc_fill(lay, dome, RAMP[YARN[a]]); P = lay.load(); rb = RAMP[YARN[b]]
    for x, y in brim: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
    for x, y in brim:
        if (x, y + 1) not in set(brim) and y == BRIM: pass
    lpc_fill(lay, [(x, y) for x, y in brim if not P[x, y][3] or True][:0], rb)
    xs = [p[0] for p in brim]; [P.__setitem__((x, BRIM + 1), rb[0] + (255,)) for x in range(min(xs), max(xs) + 1)]; [P.__setitem__((min(xs) - 1, y), rb[0] + (255,)) for y in range(BRIM - 2, BRIM + 1)]; [P.__setitem__((max(xs) + 1, y), rb[0] + (255,)) for y in range(BRIM - 2, BRIM + 1)]
    pom = [(x, y) for y in range(64) for x in range(64) if ((x - 32) / 3.4) ** 2 + ((y - (TOP - 3)) / 3) ** 2 <= 1 and not P[x, y][3]]; lpc_fill(lay, pom, rb)
    return lay
def mk_muff(a, b):
    """머리 꼭대기를 지나는 얇은 띠 + 귀 옆 작은 솜방울"""
    lay = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); P = lay.load(); rb = RAMP[YARN[b]]; ra = RAMP[YARN[a]]
    tops = {}
    for x in range(20, 45):
        ys = [y for y in range(64) if BA[x, y][3]]
        if ys: tops[x] = min(ys)
    EY = TOP + 15   # 귀 높이
    lx, rx = HR_[EY][0], HR_[EY][1]
    band = []
    for x in range(lx + 1, rx):
        y0 = tops.get(x, TOP) + 3
        band += [(x, y0), (x, y0 + 1)]
    for x in (lx + 1, rx - 1):
        for y in range(tops.get(x, TOP) + 3, EY - 2): band += [(x, y), (x + (1 if x < 32 else -1), y)]
    for x, y in band: P[x, y] = (rb[3] if (x + y) % 2 else rb[2]) + (255,)
    for cx in (lx, rx):
        puff = [(x, y) for y in range(64) for x in range(64) if ((x - cx) / 2.6) ** 2 + ((y - EY) / 3.2) ** 2 <= 1]
        for q in puff: P[q] = (0, 0, 0, 0)
        lpc_fill(lay, puff, ra, light=(-1 if cx < 32 else 1, -1))
    return lay
def mk_gloves(a, b):
    g = knit_recolor(gloves, lambda x, y: a); P = g.load(); bb = gloves.getbbox(); rb = RAMP[YARN[b]]
    for x in range(64):   # 손목 쪽 고무단 (장갑 덩어리마다 맨 위 2 줄)
        ys = [y for y in range(64) if P[x, y][3]]
        if not ys: continue
        for y in ys[:3]:
            if L(P[x, y][:3]) > 30: P[x, y] = (rb[3] if x % 2 else rb[2]) + (255,)
    return g
ITEMS = [('목도리', '털실 10', mk_scarf), ('방울 모자', '털실 10', mk_hat), ('털 귀마개', '털실 10', mk_muff), ('벙어리장갑', '털실 10', mk_gloves)]
COMBOS = [('빨강', '하양'), ('파랑', '노랑'), ('초록', '하양')]
# ---------- NPC 뜨개 인형: 정면 LPC 그림 → 머리 크게 · 몸 줄이기 · 뜨개 결 ----------
def dollify(im):
    im = im.convert('RGBA'); bb = im.getbbox(); x0, y0, x1, y1 = bb; hh = int((y1 - y0) * .44); neck = y0 + hh
    head = im.crop((x0, y0, x1, neck)); body = im.crop((x0, neck, x1, y1)); bw, bh = body.size; body = body.resize((max(1, int(bw * .9)), max(1, int(bh * .55))), Image.NEAREST)
    W = x1 - x0; Hh = head.size[1] + body.size[1]; o = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); ox = (64 - W) // 2; oy = 64 - Hh - 4
    o.alpha_composite(body, (ox + (W - body.size[0]) // 2, oy + head.size[1] - 1)); o.alpha_composite(head, (ox, oy))
    P = o.load()
    for y in range(64):
        for x in range(64):
            c = P[x, y]
            if not c[3]: continue
            l = L(c[:3])
            if l < 40: P[x, y] = (58, 36, 52, 255); continue   # 테두리는 진한 털실색
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1 and (x + y) % 4 == 2): P[x, y] = (int(c[0] * .9), int(c[1] * .9), int(c[2] * .92), 255)
    d = ImageDraw.Draw(o); d.ellipse([20, 58, 44, 63], fill=(0, 0, 0, 70))   # 그림자
    return o
DOLLS = [('레오', 'leo'), ('세라 선생님', 'sera'), ('마들렌', 'madeleine'), ('스텔라', 'stella'), ('나비', 'npc0'), ('배트리', 'npc1'), ('캇파', 'npc2'), ('아울라', 'npc3'), ('맨디', 'npc4'), ('스트로', 'npc5')]
# ---------- 미리보기 ----------
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
F, F2, F3 = ImageFont.truetype(FB, 16), ImageFont.truetype(FB, 13), ImageFont.truetype(FB, 22)
BG, PAN, INK, SUB, GOLD = (26, 18, 38), (37, 26, 54), (241, 233, 255), (184, 168, 216), (255, 233, 160)
Wd = 1000; img = Image.new('RGB', (Wd, 840), BG); d = ImageDraw.Draw(img)
panel = lambda x, y, w, h: d.rounded_rectangle([x, y, x + w, y + h], 14, fill=PAN, outline=(58, 46, 88), width=2)
d.text((24, 16), '겨울 뜨개질 · LPC 아이템 시안', font=F3, fill=(255, 184, 168))
y = 56; panel(16, y, Wd - 32, 760); d.text((32, y + 12), '내 아바타가 입은 모습 (LPC 부품을 털실 색 · 뜨개 결로 다시 칠함)', font=F, fill=GOLD)
for i, (nm, cost, fn) in enumerate(ITEMS):
    x = 40 + i * 240; d.text((x + 6, y + 42), nm, font=F, fill=INK); d.text((x + 6, y + 62), cost + ' 뭉치', font=F2, fill=SUB)
    for j, (a, b) in enumerate(COMBOS):
        r_ = fn(a, b); im = over(r_[1], r_[2]) if isinstance(r_, tuple) else over(base, r_); im = im.crop((12, 2, 52, 64)).resize((120, 186), Image.NEAREST); img.paste(im, (x + 20, y + 86 + j * 222), im)
        d.text((x + 30, y + 274 + j * 222), f'{a} · {b}', font=F2, fill=(140, 124, 170))
os.makedirs(OUTD, exist_ok=True); img.save(os.path.join(OUTD, 'knit_lpc_preview.png')); print('ok')
