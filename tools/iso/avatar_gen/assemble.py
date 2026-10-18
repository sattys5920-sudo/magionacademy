# 줄인 칸들 → 캐릭터 부품 시트 (out/avatar_parts.png + .json)
# 한 줄 = 한 층의 6프레임 (앞: 서기·걷기A·걷기B, 뒤: 서기·걷기A·걷기B)
# 색을 바꿀 층은 회색 열쇠색(240/200/150/100)으로 저장하고, 게임에서 고른 색으로 칠해요.
import numpy as np, pickle, json, colorsys
from PIL import Image
from collections import deque
D = pickle.load(open('cells.pkl', 'rb'))
KEY = [(240, 240, 240), (200, 200, 200), (150, 150, 150), (100, 100, 100)]
OUTL = (42, 24, 48)
def lv(lum, th): return 0 if lum >= th[0] else 1 if lum >= th[1] else 2 if lum >= th[2] else 3
def dil(m, n=1, diag=False):
    m = m.copy()
    for _ in range(n):
        o = m.copy(); o[1:] |= m[:-1]; o[:-1] |= m[1:]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
        if diag: o[1:, 1:] |= m[:-1, :-1]; o[:-1, :-1] |= m[1:, 1:]; o[1:, :-1] |= m[:-1, 1:]; o[:-1, 1:] |= m[1:, :-1]
        m = o
    return m
def comps(mask):
    H, W = mask.shape; seen = np.zeros_like(mask); out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            yy, xx = cy + dy, cx + dx
                            if 0 <= yy < H and 0 <= xx < W and mask[yy, xx] and not seen[yy, xx]: seen[yy, xx] = True; q.append((yy, xx))
                out.append(pts)
    return out
def is_dark(c): return c['C'] == 'dark'
# ---------- 1. 기준 머리 (얼굴 칸 13: 점 눈 → 이목구비를 지워요) ----------
def head_geom(cell):
    C, out = cell['C'], cell['out']; inner = ~out
    ys, xs = np.nonzero(inner & (C == 'skin'))
    return dict(l=xs.min(), r=xs.max(), b=ys.max(), t=np.nonzero(inner)[0].min())
F0 = D['faces'][13]
G0 = head_geom(F0)
# 피부 밝기 단계 (모든 얼굴 칸의 피부로)
# 밝기 → 4단계 경계 (히스토그램을 보고 정했어요)
SK_TH = [214, 180, 130]
HR_TH = [195, 140, 88]
EY_TH = [170, 120, 85]
UN_TH = [185, 128, 88]
MG_TH = [125, 90, 70]
print('th', HR_TH, EY_TH, UN_TH, MG_TH)
# 원본 피부색 4단계 평균 → 기본 피부 팔레트
def mean_rgb(cells, cls, th, k):
    acc = []
    for c in cells:
        m = (c['C'] == cls) & ~c['out']
        for y, x in zip(*np.nonzero(m)):
            if lv(c['lum'][y, x], th) == k: acc.append(c['rgb'][y, x])
    return '#%02X%02X%02X' % tuple(np.mean(acc, axis=0).astype(int)) if acc else None
SKIN0 = [mean_rgb(D['faces'], 'skin', SK_TH, k) for k in range(4)]
print('skin0', SKIN0)

# ---------- 프레임 좌표 ----------
# 교복 칸에서 목 위치를 찾아 머리를 얹어요
def uni_geom(cell):
    C, out = cell['C'], cell['out']; fig = ~out
    ys, xs = np.nonzero(fig); top, bot = ys.min(), ys.max()
    sk = (C == 'skin') & fig
    widths = [sk[y].sum() for y in range(C.shape[0])]
    ymax = int(np.argmax(widths[:top + 30])); neck = None
    for y in range(ymax, bot):
        if widths[y] < .45 * widths[ymax]: neck = y; break
    # 다리 사이 틈 (가운데 줄이 바깥이 되는 곳)
    cx = int(round((xs.min() + xs.max()) / 2)); legtop = bot
    for y in range(bot, neck, -1):
        if out[y, cx] or out[y, cx - 1] or out[y, cx + 1]: legtop = y
        else: break
    return dict(neck=neck, bot=bot, cx=(xs.min() + xs.max()) / 2, legtop=legtop)
UG = [uni_geom(c) for c in D['uni']]
print('uni', [(g['neck'], g['bot'], g['legtop']) for g in UG])
FW = 46
HCX = (G0['l'] + G0['r']) / 2
TOPPAD = 6
NECK = TOPPAD + (G0['b'] - G0['t']) + 1           # 머리 아래 끝 바로 다음 줄
BODYH = max(g['bot'] - g['neck'] for g in UG) + 1
FH = NECK + BODYH + 1
CX = FW // 2
print('frame', FW, FH, 'neck', NECK)
def head_xy(x, y, g):   # 머리 칸 좌표 → 프레임 좌표 (턱과 가운데를 맞춰요)
    return int(x + CX - (g['l'] + g['r']) // 2), int(y - g['b'] + (NECK - 1))

class Layer:
    def __init__(self): self.f = [np.zeros((FH, FW, 4), np.uint8) for _ in range(6)]
    def put(self, fr, x, y, c):
        if 0 <= x < FW and 0 <= y < FH: self.f[fr][y, x] = (*c, 255)
    def empty(self, frs=range(6)): return all(self.f[i][..., 3].max() == 0 for i in frs)
def walkify(L, legtop, cx=CX):
    """앞·뒤 서기(0, 3)에서 걷기 프레임을 만들어요: 한쪽 다리를 2칸 들어요"""
    for base in (0, 3):
        src = L.f[base]
        for k, side in ((1, 'L'), (2, 'R')):
            dst = np.zeros_like(src)
            for y in range(FH):
                for x in range(FW):
                    if not src[y, x, 3]: continue
                    lift = y >= legtop and ((x < cx) == (side == 'L'))
                    if not lift: dst[y, x] = src[y, x]
            for y in range(FH):
                for x in range(FW):
                    if src[y, x, 3] and y >= legtop and ((x < cx) == (side == 'L')) and y - 2 >= 0: dst[y - 2, x] = src[y, x]
            L.f[base + k] = dst
def copy_frames(L):
    for base in (0, 3):
        for k in (1, 2): L.f[base + k] = L.f[base].copy()

# ---------- 2. 머리(피부) ----------
head = Layer()
C, rgb, out, lum = F0['C'], F0['rgb'], F0['out'], F0['lum']
outline0 = (C == 'dark') & dil(out)
for y in range(C.shape[0]):
    for x in range(C.shape[1]):
        if out[y, x]: continue
        X, Y = head_xy(x, y, G0)
        if outline0[y, x]: c = OUTL
        elif C[y, x] == 'skin': c = KEY[lv(lum[y, x], SK_TH)]
        else: c = KEY[1]                    # 이목구비·볼터치 자리는 피부로 메워요
        if x < G0['l'] + 3 or x > G0['r'] - 3:     # 귀 쪽 갈색 선은 진한 피부로
            if C[y, x] not in ('skin',) and not outline0[y, x]: c = KEY[3]
        head.put(0, X, Y, c); head.put(3, X, Y, c)
copy_frames(head)
# 볼터치 (모든 얼굴에 공통, 얼굴 칸 0에서)
blush = Layer(); F = D['faces'][0]; G = head_geom(F)
for y, x in zip(*np.nonzero((F['C'] == 'blush') & ~F['out'])):
    X, Y = head_xy(x, y, G); blush.put(0, X, Y, tuple(int(v) for v in F['rgb'][y, x]))
copy_frames(blush)
for k in (3, 4, 5): blush.f[k][:] = 0

# ---------- 3. 눈·눈썹·입 ----------
EYE_PICK = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 23]
EYE_NAMES = ['반짝 동글', '큰 눈', '졸린 눈', '웃는 눈', '고양이', '별 눈', '하트 눈', '윙크', '다짐', '눈물', '빙글빙글', '점 눈', '뱀파이어', '순정 반짝', '질끈']
MOUTH_PICK = [0, 17, 10, 15, 16, 18, 20, 21, 22, 23]
MOUTH_NAMES = ['미소', '고양이 입', '시무룩', '송곳니', '활짝', '놀람', '메롱', '일자', '이 보이게', '오물오물']
def face_parts(i):
    F = D['faces'][i]; G = head_geom(F); C, out, lum, rgb = F['C'], F['out'], F['lum'], F['rgb']
    t, b = G['t'], G['b']; h = b - t; w = G['r'] - G['l']; cx = (G['l'] + G['r']) / 2
    edge = (C == 'dark') & dil(out)
    feat = ~out & ~edge & ~np.isin(C, ['skin', 'blush'])
    feat[:, :G['l'] + 4] = False; feat[:, G['r'] - 3:] = False
    eyes, brows, mouth = Layer(), Layer(), Layer()
    for pts in comps(feat):
        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]; my, mx = np.mean(ys), np.mean(xs)
        hgt = max(ys) - min(ys) + 1
        if len(pts) <= 1 and (my - t) / h > .55 and abs(mx - cx) < 2: kind = 'mouth'    # 코 점
        elif (my - t) / h >= .68 and abs(mx - cx) < .26 * w: kind = 'mouth'
        elif hgt <= 3 and (my - t) / h < .52 and all(C[y, x] in ('grey', 'other') for y, x in pts): kind = 'brow'
        else: kind = 'eye'
        for y, x in pts:
            X, Y = head_xy(x, y, G); cl = C[y, x]; col = tuple(int(v) for v in rgb[y, x])
            if kind == 'brow': brows.put(0, X, Y, KEY[min(3, lv(lum[y, x], HR_TH) + 1)])
            elif kind == 'eye':
                if cl == 'grey': eyes.put(0, X, Y, KEY[lv(lum[y, x], EY_TH)])
                elif cl == 'white': eyes.put(0, X, Y, (255, 255, 252))
                elif cl == 'dark': eyes.put(0, X, Y, OUTL)
                else: eyes.put(0, X, Y, col)
            else:
                if cl == 'grey': mouth.put(0, X, Y, (232, 106, 128) if lum[y, x] > 110 else (176, 60, 86))   # 혀
                elif cl == 'dark': mouth.put(0, X, Y, OUTL)
                elif cl == 'white': mouth.put(0, X, Y, (255, 255, 252))
                else: mouth.put(0, X, Y, col)
    for L in (eyes, brows, mouth): copy_frames(L)
    for L in (eyes, brows, mouth):
        for k in (3, 4, 5): L.f[k][:] = 0
    return eyes, brows, mouth

# ---------- 4. 머리카락 ----------
def hair_part(cell):
    C, out, lum = cell['C'], cell['out'], cell['lum']; inner = ~out
    G = head_geom(cell)
    face = inner & np.isin(C, ['skin', 'blush'])
    hairg = inner & np.isin(C, ['grey', 'white'])
    keep_dark = inner & (C == 'dark') & dil(hairg, 1, True)
    hm = hairg | keep_dark
    # 얼굴 둘레의 갈색 번짐은 버려요
    hm &= ~(inner & (C == 'other'))
    front_o, front_u, back = Layer(), Layer(), Layer()
    chinY = NECK - 1
    allpix = []
    for y, x in zip(*np.nonzero(hm)):
        X, Y = head_xy(x, y, G)
        c = OUTL if C[y, x] == 'dark' else KEY[lv(lum[y, x], HR_TH)]
        allpix.append((X, Y, c))
        if Y >= chinY - 1 and abs(X - CX) <= 10 and c != OUTL and lv(lum[y, x], HR_TH) >= 2: front_u.put(0, X, Y, c)
        elif Y >= chinY + 1 and abs(X - CX) <= 10: front_u.put(0, X, Y, c)
        else: front_o.put(0, X, Y, c)
    # 뒷모습: 머리카락 + 머리 전체를 머리카락으로 덮어요 (목덜미 4줄은 남겨요)
    hd = head.f[0][..., 3] > 0
    bm = np.zeros((FH, FW), bool); bc = {}
    for X, Y, c in allpix:
        if 0 <= X < FW and 0 <= Y < FH: bm[Y, X] = True; bc[(X, Y)] = c
    # 줄마다 머리카락이 있는 가로 범위 안만 채워요 (모히칸은 가운데 띠만, 짧은 머리는 귀 아래부터 목덜미)
    fill = np.zeros_like(bm)
    for Y in range(FH):
        xs_ = np.nonzero(bm[Y] & ~np.array([bc.get((X, Y)) == OUTL for X in range(FW)]))[0]
        if len(xs_): fill[Y, xs_.min():xs_.max() + 1] = True
    fill &= hd & ~bm
    ys = np.nonzero(hd)[0]; htop = ys.min()
    longhair = bm[chinY + 2:].any(axis=0).sum() >= 6        # 턱 아래로 내려오는 머리면 목덜미까지 덮어요
    for Y, X in zip(*np.nonzero(fill)):
        if Y >= chinY - 3 and not longhair: continue
        bm[Y, X] = True; bc[(X, Y)] = KEY[0] if (Y - htop) in (2, 3) and abs(X - CX) < 7 else KEY[1] if Y < chinY - 7 else KEY[2]
    # 안쪽 테두리 선은 지우고 새 바깥 테두리를 둘러요
    for (X, Y), c in list(bc.items()):
        if c == OUTL and all(0 <= X + dx < FW and 0 <= Y + dy < FH and bm[Y + dy, X + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): bc[(X, Y)] = KEY[2]
    ring = dil(bm) & ~bm
    for Y, X in zip(*np.nonzero(ring)):
        if Y < chinY - 3 or not hd[Y, X] or longhair: bc[(X, Y)] = OUTL
    for (X, Y), c in bc.items(): back.put(3, X, Y, c)
    for L in (front_o, front_u, back): copy_frames(L)
    # 뒤 프레임에서는 앞 머리층을 비우고, 앞 프레임에서는 뒷머리층을 비워요
    for k in (3, 4, 5): front_o.f[k][:] = 0; front_u.f[k][:] = 0
    for k in (0, 1, 2): back.f[k][:] = 0
    return front_o, front_u, back
HAIR_SRC = [('hair1', i) for i in range(24)] + [('hair2', i) for i in range(24) if i != 19]
HAIR_DROP = {('hair1', 11), ('hair1', 12), ('hair1', 15), ('hair1', 18), ('hair2', 4), ('hair2', 6), ('hair2', 10)}
HAIR_NAMES = {
 ('hair1', 0): '단발', ('hair1', 1): '긴 생머리', ('hair1', 2): '양갈래', ('hair1', 3): '올림 똥머리', ('hair1', 4): '숏컷', ('hair1', 5): '삐죽 숏', ('hair1', 6): '뾰족뾰족',
 ('hair1', 7): '포니테일', ('hair1', 8): '아프로', ('hair1', 9): '옆 땋은 머리', ('hair1', 10): '히메컷', ('hair1', 13): '울프컷', ('hair1', 14): '스포츠',
 ('hair1', 16): '부스스', ('hair1', 17): '가르마 올백', ('hair1', 18): '옆 가르마', ('hair1', 19): '낮은 양갈래', ('hair1', 20): '양쪽 똥머리', ('hair1', 21): '긴 웨이브',
 ('hair1', 22): '멀릿', ('hair1', 23): '커튼 앞머리',
 ('hair2', 0): '모히칸', ('hair2', 1): '땋은 머리', ('hair2', 2): '반묶음', ('hair2', 3): '드릴 머리', ('hair2', 7): '올백', ('hair2', 8): '상투',
 ('hair2', 9): '복슬복슬', ('hair2', 11): '옆으로 넘김', ('hair2', 12): '옆 포니테일', ('hair2', 13): '바닥까지 긴 머리', ('hair2', 14): '바가지', ('hair2', 15): '경단 머리',
 ('hair2', 16): '콘로우', ('hair2', 17): '더듬이 경단', ('hair2', 18): '한쪽 눈 가림', ('hair2', 20): '낮은 포니테일', ('hair2', 21): '마녀 장발', ('hair2', 22): '단정 앞머리', ('hair2', 23): '별 똥머리', ('hair2', 5): '곱슬 숏',
}

# ---------- 5. 교복 ----------
UNI_NAMES = ['춘추복', '하복', '동복', '체육복', '생활복']
def uni_part(k):
    Ls = dict(skin=Layer(), cloth=Layer(), house=Layer(), shoes=Layer())
    for side, idx, base in (('front', k, 0), ('back', k + 5, 3)):
        cell = D['uni'][idx]; g = UG[idx]; C, out, lum, rgb = cell['C'], cell['out'], cell['lum'], cell['rgb']
        fig = ~out
        for y, x in zip(*np.nonzero(fig)):
            if y < g['neck']: continue
            X, Y = int(x + CX - int(g['cx'])), int(y - g['neck'] + NECK)
            cl = C[y, x]
            if cl == 'skin': Ls['skin'].put(base, X, Y, KEY[lv(lum[y, x], SK_TH)])
            elif cl == 'mag': Ls['house'].put(base, X, Y, KEY[lv(lum[y, x], MG_TH)])
            elif cl == 'dark': Ls['cloth'].put(base, X, Y, OUTL)
            elif cl == 'white': Ls['cloth'].put(base, X, Y, (246, 244, 250))
            elif cl == 'grey':
                tgt = 'shoes' if y >= g['bot'] - 2 else 'cloth'
                Ls[tgt].put(base, X, Y, KEY[lv(lum[y, x], UN_TH)])
            elif cl == 'blush': Ls['skin'].put(base, X, Y, KEY[2])
            else:
                c = tuple(int(v) for v in rgb[y, x])
                if c[1] > c[0] + 8 and c[1] > c[2] + 8: continue          # 배경 초록 번짐
                Ls['cloth'].put(base, X, Y, c)
    legtop = int(UG[k]['legtop'] - UG[k]['neck'] + NECK)
    for L in Ls.values(): walkify(L, legtop)
    return Ls

# ---------- 시트로 ----------
rows = []
def row_of(L):
    im = np.zeros((FH, FW * 6, 4), np.uint8)
    for i in range(6): im[:, i * FW:(i + 1) * FW] = L.f[i]
    rows.append(im); return len(rows) - 1
Z = ['hairU', 'skin', 'cloth', 'head', 'face', 'hairO']
base = [[row_of(head), 'skin', 'head'], [row_of(blush), None, 'face']]
parts = dict(hair=[], eyes=[], mouth=[], uni=[])
for src in HAIR_SRC:
    if src in HAIR_DROP: continue
    cell = D[src[0]][src[1]]
    if src == ('hair2', 13):
        from extract_lib import classify, outside
        a, b2 = D['hair2'][13]['rgb'], D['hair2'][19]['rgb']; w = min(a.shape[1], b2.shape[1])
        rgbm = np.concatenate([a[:, :w], b2[:, :w]], axis=0); Cm, lm = classify(rgbm)
        cell = dict(rgb=rgbm, C=Cm, lum=lm, out=outside(Cm))
    o, u, bk = hair_part(cell)
    L = [[row_of(o), 'hair', 'hairO'], [row_of(bk), 'hair', 'hairO']]
    if not u.empty((0,)): L.append([row_of(u), 'hair', 'hairU'])
    parts['hair'].append(dict(n=HAIR_NAMES[src], L=L))
for n, i in zip(EYE_NAMES, EYE_PICK):
    e, b, _ = face_parts(i); L = [[row_of(e), 'eye', 'face']]
    if not b.empty((0,)): L.append([row_of(b), 'hair', 'face'])
    parts['eyes'].append(dict(n=n, L=L))
for n, i in zip(MOUTH_NAMES, MOUTH_PICK):
    _, _, m = face_parts(i); parts['mouth'].append(dict(n=n, L=[[row_of(m), None, 'face']]))
for k, n in enumerate(UNI_NAMES):
    Ls = uni_part(k)
    L = [[row_of(Ls['skin']), 'skin', 'skin'], [row_of(Ls['cloth']), 'cloth', 'cloth'], [row_of(Ls['house']), 'house', 'cloth'], [row_of(Ls['shoes']), 'shoes', 'cloth']]
    parts['uni'].append(dict(n=n, L=L))
sheet = np.concatenate(rows, axis=0)
Image.fromarray(sheet, 'RGBA').save('out/avatar_parts.png')
# ---------- 팔레트 ----------
def ramp(h, hl=.38, s2=.8, s3=.6):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    H, L_, S = colorsys.rgb_to_hls(r, g, b)
    def mk(l, s, dh=0): rr, gg, bb = colorsys.hls_to_rgb((H + dh) % 1, max(0, min(1, l)), max(0, min(1, s))); return '#%02X%02X%02X' % (int(rr * 255), int(gg * 255), int(bb * 255))
    return [mk(L_ + (1 - L_) * hl, S), h.upper(), mk(L_ * s2, min(1, S * 1.05), .015), mk(L_ * s3, min(1, S * 1.1), .03)]
def skin_like(base):   # 원본 피부의 단계별 비율을 그대로 따라가요
    s0 = [[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in SKIN0]; bb = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
    return ['#%02X%02X%02X' % tuple(max(0, min(255, int(bb[c] * s0[k][c] / s0[1][c]))) for c in range(3)) for k in range(4)]
SKIN = [SKIN0, skin_like('#FFE0CC'), skin_like('#E2A47A'), skin_like('#B07450'), skin_like('#76482E')]
EYE = [ramp(h) for h in ['#7A5AE0', '#4AA8F0', '#2E7AD0', '#4AC878', '#2A9A54', '#8AD8C8', '#E8944A', '#B8682A', '#7A4A2E', '#F05A8A', '#E83A3A', '#B01E2A',
                          '#F0C040', '#C8A040', '#A890FF', '#C060E0', '#5A4A6A', '#3A3A4A', '#8A8A9A', '#40C8E8']]
HAIR = [ramp(h, .3) for h in ['#3A2A4A', '#2A2A34', '#6A4028', '#8A5A3A', '#C09040', '#E8C870', '#F4E8C8', '#E8703E', '#C0402A', '#7A1A2A',
                               '#F49AC0', '#D8709E', '#B49AF2', '#6648A4', '#7ED8C0', '#2E8070', '#8EC4F2', '#3C6AA0', '#D8D8E8', '#8888A4']]
SHOES = [ramp(h) for h in ['#3A2A3A', '#5A3A2A', '#8A5A3A', '#E8E4F0', '#B8303A', '#3A6AB8', '#3A8A4C', '#E8702A', '#7A4ABA', '#F0C850']]
CLOTH = [['#D8D4E4', '#9C96B4', '#625C7E', '#3A3452']]
HOUSE = {'dew': ramp('#5CCB8E'), 'ember': ramp('#F08A3C'), 'dusk': ramp('#E8709A'), 'moon': ramp('#7A66E0')}
meta = dict(fw=int(FW), fh=int(FH), src='art/iso/avatar_parts.png', z=Z, base=base, parts=parts, pal=dict(skin=SKIN, eye=EYE, hair=HAIR, shoes=SHOES, cloth=CLOTH, house=HOUSE),
            head=dict(t=int(TOPPAD - 2), b=int(NECK + 1)))
json.dump(meta, open('out/avatar_parts.json', 'w'), ensure_ascii=False)
print('rows', len(rows), {k: len(v) for k, v in parts.items()}, sheet.shape)
