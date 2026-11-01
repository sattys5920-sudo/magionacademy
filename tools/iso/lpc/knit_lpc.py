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
def mk_shawl(a, b):
    bb = mantal.getbbox(); y1 = bb[3]; sh = knit_recolor(mantal, lambda x, y: b if y >= y1 - 2 or (y // 2) % 3 == 2 else a)
    d = ImageDraw.Draw(sh); P = sh.load()   # 아래 가장자리에 술
    for x in range(bb[0] + 1, bb[2] - 1, 2):
        ys = [y for y in range(64) if P[x, y][3]]
        if ys: yb = max(ys); r = RAMP[YARN[b]]; d.point((x, yb + 1), fill=r[2] + (255,)); d.point((x, yb + 2), fill=r[3] + (255,))
    return sh
def mk_sweater(a, b):
    bb = sweater.getbbox(); y0, y1 = bb[1], bb[3]; mid = y0 + 6
    def pk(x, y):
        if y >= y1 - 2: return b                              # 밑단 고무단
        if mid <= y <= mid + 2: return b if (x + (y - mid)) % 3 else a   # 가슴 무늬 띠 (페어아일 느낌)
        return a
    sw = knit_recolor(sweater, pk); P = sw.load(); r = RAMP[YARN[b]]
    for y in range(64):   # 소매 끝 고무단: 양쪽 가장 바깥 아래
        for x in range(64):
            if P[x, y][3] and y >= y1 - 9 and (x <= bb[0] + 3 or x >= bb[2] - 4): P[x, y] = r[2 + (x % 2)] + (255,)
    return sw
def mk_muff(a, b):
    o = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if band is not None: o = knit_recolor(band, lambda x, y: b)
    d = ImageDraw.Draw(o); r = RAMP[YARN[a]]
    for cx in (21, 42):   # 귀 솜방울 (LPC처럼 테두리 + 3 단 음영)
        d.ellipse([cx - 4, 22, cx + 4, 31], fill=r[0] + (255,)); d.ellipse([cx - 3, 23, cx + 3, 30], fill=r[2] + (255,)); d.ellipse([cx - 3, 23, cx + 1, 27], fill=r[3] + (255,)); d.point((cx - 2, 24), fill=(255, 255, 255, 255))
        for yy in range(24, 30, 2): d.point((cx + 1 + (yy % 4 == 0), yy), fill=r[1] + (255,))
    return o
ITEMS = [('목도리', '털실 10', mk_scarf), ('방울 모자', '털실 10', mk_hat), ('포근 숄', '털실 15', mk_shawl), ('니트 스웨터', '털실 15', mk_sweater), ('털 귀마개', '털실 10', mk_muff)]
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
Wd = 1060; img = Image.new('RGB', (Wd, 1340), BG); d = ImageDraw.Draw(img)
panel = lambda x, y, w, h: d.rounded_rectangle([x, y, x + w, y + h], 14, fill=PAN, outline=(58, 46, 88), width=2)
d.text((24, 16), '겨울 뜨개질 · LPC 아이템 시안', font=F3, fill=(255, 184, 168))
y = 56; panel(16, y, Wd - 32, 760); d.text((32, y + 12), '내 아바타가 입은 모습 (LPC 부품을 털실 색 · 뜨개 결로 다시 칠함)', font=F, fill=GOLD)
for i, (nm, cost, fn) in enumerate(ITEMS):
    x = 36 + i * 204; d.text((x + 6, y + 42), nm, font=F, fill=INK); d.text((x + 6, y + 62), cost + ' 뭉치', font=F2, fill=SUB)
    for j, (a, b) in enumerate(COMBOS):
        r_ = fn(a, b); im = over(r_[1], r_[2]) if isinstance(r_, tuple) else over(base, r_); im = im.crop((12, 2, 52, 64)).resize((120, 186), Image.NEAREST); img.paste(im, (x + 20, y + 86 + j * 222), im)
        d.text((x + 30, y + 274 + j * 222), f'{a} · {b}', font=F2, fill=(140, 124, 170))
y = 832; panel(16, y, Wd - 32, 492); d.text((32, y + 12), 'NPC 뜨개 인형 10 종 · 털실 20 뭉치 · 방 가구 (각 NPC의 LPC 그림을 뜨개 인형 비율로)', font=F, fill=GOLD)
for i, (nm, k) in enumerate(DOLLS):
    p = os.path.join(NPCD, f'av_{k}.png')
    if not os.path.exists(p): continue
    dl = dollify(Image.open(p)); bb = dl.getbbox(); dl = dl.crop(bb); k = min(150 / dl.size[0], 150 / dl.size[1], 5); im = dl.resize((int(dl.size[0] * k), int(dl.size[1] * k)), Image.NEAREST); x = 44 + (i % 5) * 198; yy = y + 44 + (i // 5) * 222; img.paste(im, (x + 84 - im.size[0] // 2, yy + 156 - im.size[1]), im); d.text((x + 84 - d.textlength(nm, font=F) / 2, yy + 166), nm, font=F, fill=INK)
os.makedirs(OUTD, exist_ok=True); img.save(os.path.join(OUTD, 'knit_lpc_preview.png')); print('ok')
