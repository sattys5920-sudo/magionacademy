# 옆모습 머리 구조(두개골·귀·턱·목·머리카락 정리)와 포니테일 계열 꼬리 (묶는 점 하나로 앞·옆·뒤 계산)
# 좌표는 모두 프레임 좌표(출력 시트에서 아래로 내리기 전). 기준 = face_grid의 앞 얼굴 F
import numpy as np
from scipy import ndimage
SK, SK_SH, SK_LINE, HAIR_MID, HAIR_DK, HAIR_LT, HAIR_LINE = 205, 172, 120, 140, 110, 175, 95
TIE = (224, 72, 110, 255)          # 머리끈 (포인트 색, 색 그대로)
def g(v): return np.array([v, v, v, 255], np.uint8)
# ---------- 머리 모양 데이터 ----------
# 귀 노출: visible(귀 전체, 윗부분 1칸만 머리카락) · partial(위 2칸 덮음) · hidden(귀 덮음)
EAR_VIS = {}
for n in (3, 4, 5, 6, 7, 12, 16, 20, 25, 26, 29, 32, 33, 34, 36, 39, 2, 15, 21): EAR_VIS[n] = 'visible'
for n in (0, 10, 11, 13, 14, 18, 19, 24, 27, 28, 31, 35, 38): EAR_VIS[n] = 'partial'
for n in (1, 8, 9, 17, 22, 23, 30, 37): EAR_VIS[n] = 'hidden'
EAR_EXPOSED = {'visible': 6, 'partial': 4, 'hidden': 0}     # 귀 8칸 중 보이는 칸 수
# 묶는 점: 캐릭터 기준 (u 좌우: +1 캐릭터의 왼쪽 / d 앞뒤: -1 뒤통수 / v 높이)
TAILS = {
    7: dict(kind='high'),
    29: dict(kind='side', side='L'),
    36: dict(kind='side', side='L', low=True),
    2: dict(kind='twin'),
    15: dict(kind='twin', low=True),
    21: dict(kind='twin', low=True, braid=True),
}
# ---------- 기하 ----------
def side_geom(F, dy):
    """옆 머리: 폭 = 정면 얼굴 폭 W + 2, 높이 = 정면과 같게 (옆은 dy만큼 위)"""
    T, B = F['T'] - dy, F['B'] - dy; et = F['eye_top'] - dy; Wd = F['W'] + 2
    X0 = 13; X1 = X0 + Wd - 1                    # X0 = 얼굴 앞 윤곽(테두리) 열
    third = Wd / 3
    ex0 = X0 + round(Wd * .55)                    # 귀 왼쪽 열 (귀 가운데가 55~60%)
    G = dict(T=T, B=B, H=B - T + 1, eye_top=et, mouth_row=et + 4, nose_row=et + 2, X0=X0, X1=X1, Wd=Wd,
             thirds=(X0 + third, X0 + 2 * third), ear_x=ex0, ear_y=et, ear_h=4, front=X0, eye_x=X0 + 2, mouth_x=X0 + 1,
             center=(X0 + X1) / 2, hairline=et - 3)
    G['safe'] = (et - 1, et + 2, G['eye_x'] - 1, G['eye_x'] + 2)
    return G
def jaw_back(G, y):
    """귀 아래 끝에서 앞쪽 턱 끝까지 대각선"""
    y0, x0 = G['ear_y'] + G['ear_h'], G['ear_x'] + 1; y1, x1 = G['B'], G['X0'] + 4
    if y <= y0: return x0
    return int(round(x0 + (x1 - x0) * (y - y0) / max(1, y1 - y0)))
def skull(G, FW, FH):
    """옆 두개골 실루엣 (앞 열 = 테두리)"""
    m = np.zeros((FH, FW), bool); T, B, X0, X1 = G['T'], G['B'], G['X0'], G['X1']
    for y in range(T, B + 1):
        k = y - T
        if k == 0: a, b = X0 + 4, X1 - 3
        elif k == 1: a, b = X0 + 2, X1 - 1
        elif k == 2: a, b = X0 + 1, X1
        else: a, b = X0, X1
        if y == G['nose_row']: a = X0 - 1
        if y > G['mouth_row']: a = X0 + 1 + (y == B)
        if y > G['ear_y'] + G['ear_h'] - 1: b = jaw_back(G, y)
        m[y, a:b + 1] = True
    return m
def ear_box(G): return G['ear_y'], G['ear_y'] + G['ear_h'] - 1, G['ear_x'], G['ear_x'] + 1
def side_skin(G, FW, FH):
    """옆 피부 층 1프레임: 앞·가운데 1/3은 피부(테두리 포함), 귀, 목. 뒤 1/3과 머리선 위는 머리카락 자리"""
    P = np.zeros((FH, FW, 4), np.uint8); m = skull(G, FW, FH)
    for y in range(G['T'], G['B'] + 1):
        xs = np.nonzero(m[y])[0]
        if not len(xs): continue
        a, b = xs.min(), min(xs.max(), int(G['thirds'][1]))
        P[y, a:b + 1] = g(SK)
        P[y, a] = g(SK_LINE)                                   # 앞 윤곽 테두리
        if y > G['ear_y'] + G['ear_h'] - 1: P[y, xs.max()] = g(SK_LINE)   # 턱선 테두리
    P[G['B'] + 1, G['X0'] + 3:jaw_back(G, G['B']) + 1] = g(SK_LINE)      # 턱 밑
    # 목: 머리 가로 가운데(귀 바로 아래)에서
    nc = int(round(G['center'])); top = G['ear_y'] + G['ear_h']
    for y in range(top, G['B'] + 2):
        for x in range(nc - 2, nc + 2):
            if not P[y, x, 3] or y > G['B']: P[y, x] = g(SK_SH if x == nc - 2 else SK)
    t, b, l, r = ear_box(G)
    for y in range(t, b + 1):
        P[y, l] = g(SK_SH); P[y, r] = g(SK); P[y, r + 1] = g(SK_LINE)   # 앞 열 그림자, 뒤쪽 가장자리만 테두리
    return P, m
# ---------- 꼬리 ----------
def tail_px(length, thick0, rise, dirx, drift, braid=False, delay=0):
    """꼬리 그림 (점 목록): 묶는 점 (0,0)에서 위·뒤로 rise칸 둥글게 솟았다가 아래로. 반환 [(x, y, 회색)]"""
    pts = []; cx, cy = 0, 0
    path = []
    for k in range(1, rise + 1): path.append((dirx * k, -k))
    if rise: path += [(dirx * (rise + 1), -rise), (dirx * (rise + 2), -rise + 1)]
    sx, sy = (path[-1] if path else (0, 0)); sx = sx if path else 0
    for k in range(0, length + 1):
        x = sx + (drift * min(max(0, k - delay), 8)) // 4; y = (sy + 1 if path else 1) + k   # delay: 턱 아래까지는 곧게 (얼굴을 덮지 않게)
        path.append((x, y))
    n = len(path); seen = {}
    for i, (x, y) in enumerate(path):
        t = i / max(1, n - 1)
        # 두께: 묶은 아래 thick0 → 가운데 살짝 불룩 → 끝 1~2칸 (홀수로 맞춰 가운데 정렬)
        th = thick0 if t < .45 else (thick0 - 2 if t < .8 else (3 if t < .93 else 1))
        th = max(1, th - (1 - th % 2))
        tip = n - 1 - i
        for j in range(th):
            xx = x - th // 2 + j
            if tip < 3 and th > 1 and (j + tip) % 2 == 1: continue    # 끝은 갈라진 가닥
            v = HAIR_LT if j == 0 else (HAIR_DK if j == th - 1 else HAIR_MID)
            if th >= 3 and j == th // 2 and (not braid or (y // 2) % 2): v = 122   # 결 선
            if braid and th >= 3 and (y % 3 == 0): v = HAIR_DK
            seen[(xx, y)] = v
    return [(x, y, v) for (x, y), v in seen.items()]
def paste_tail(layer_f, pts, ax, ay, tie=True, mask=None):
    FH, FW = layer_f.shape[:2]; drawn = np.zeros((FH, FW), bool)
    for x, y, v in pts:
        X, Y = ax + x, ay + y
        if 0 <= X < FW and 0 <= Y < FH and (mask is None or not mask[Y, X]):
            layer_f[Y, X] = g(v); drawn[Y, X] = True
    if tie:
        for X in (ax - 1, ax, ax + 1):
            if 0 <= X < FW: layer_f[ay, X] = TIE; drawn[ay, X] = True
    return drawn
# ---------- 머리 하나에 적용 ----------
def clean_face(fs, face):
    d = face & (fs[..., 3] > 0) & (fs[..., 0] < 150); fs[d] = g(SK); return fs
def bases(BO, BS, F, G):
    """기준(까까머리) 마스크: 앞·뒤 머리 실루엣, 앞 얼굴 피부, 옆 피부 층"""
    FH, FW = BS.f.shape[1:3]
    PS, sk = side_skin(G, FW, FH)
    fu = (BS.f[0, ..., 3] > 0) | (BO.f[0, ..., 3] > 0); bu = (BS.f[3, ..., 3] > 0) | (BO.f[3, ..., 3] > 0)
    face = np.zeros((FH, FW), bool); face[F['eye_top'] - 1:F['B'] + 1, F['L']:F['R'] + 1] = True
    face &= BS.f[0, ..., 3] > 0
    return dict(PS=PS, skull=sk, front=ndimage.binary_dilation(fu, iterations=2), back=ndimage.binary_dilation(bu, iterations=2),
                side=ndimage.binary_dilation(sk, iterations=2), face=face, back0=bu, FS=clean_face(BS.f[0].copy(), face))
def fill(o, y, x, v=HAIR_MID):
    if 0 <= y < o.shape[0] and 0 <= x < o.shape[1] and not o[y, x, 3]: o[y, x] = g(v)
def apply(n, O, U, S, F, G, BB):
    FH, FW = S.f.shape[1:3]; vis = EAR_VIS[n]
    # 앞: 얼굴 피부 안 머리카락 걷기 (눈썹은 눈 층이라 그대로)
    for j in range(3):
        o, s = O.f[j], S.f[j]; m = BB['face'] & (o[..., 3] > 0)
        o[m] = 0; s[BB['face']] = BB['FS'][BB['face']]          # 얼굴 피부는 기준 머리 것 (그림마다 남은 어두운 점 없이)
    # 옆
    et, X0, X1, T = G['eye_top'], G['X0'], G['X1'], G['T']; t, b, l, r = ear_box(G); sk = BB['skull']
    for j in range(6, 9):
        o = O.f[j]; S.f[j] = BB['PS']
        o[et - 1:, :X0] = 0                                   # 얼굴 앞 윤곽 밖 (늘어진 머리·떨어진 점)
        o[:et - 1, :X0 - 1] = 0                               # 앞머리는 이마보다 1칸까지만
        for y in range(et - 1, FH):                           # 얼굴·볼·턱 (앞·가운데 1/3) 피부 자리
            xs = np.nonzero(sk[y])[0] if y < sk.shape[0] else []
            if not len(xs): continue
            hi = min(xs.max(), int(G['thirds'][1])) if y <= b else xs.max()
            lo = X0 if y <= b else X0
            if y <= b: hi = min(hi, l - 2)                    # 귀 앞 구레나룻 열(l-1)까지는 남겨요
            o[y, lo:hi + 1] = 0
        for y in range(G['hairline'], et + 3): o[y, l - 1] = g(HAIR_DK)     # 구레나룻
        cover = {'visible': 1, 'partial': 2, 'hidden': G['ear_h']}[vis]
        for y in range(t, b + 1):
            for x in range(l, r + 2):
                o[y, x] = g(HAIR_MID) if y < t + cover else (o[y, x] if vis == 'hidden' else 0)
        if vis == 'hidden':
            for y in range(t, b + 1): o[y, l - 1] = g(HAIR_MID)               # 귀 자리에서 살짝 불룩
        for x in range(l - 1, r + 3): fill(o, t - 1, x)                        # 귀 위
        for y in range(t, b + 2): fill(o, y, r + 2)                            # 귀 뒤
        for y in range(T, b + 2):                                              # 뒤통수 1/3과 머리선 위는 머리카락
            for x in np.nonzero(sk[y])[0]:
                if x > G['thirds'][1] or y < G['hairline']: fill(o, y, x)
        for y in range(T + 2, b + 2): fill(o, y, X1 + 1, HAIR_LINE)            # 뒤통수 볼륨
        for x in range(X0 + 4, X1 - 2): fill(o, T - 1, x, HAIR_LINE)
    if n in TAILS: tails(n, O, U, F, G, BB)
def tails(n, O, U, F, G, BB):
    spec = TAILS[n]; kind = spec['kind']; low = spec.get('low'); dy = F['eye_top'] - G['eye_top']
    for frs, key in ((range(0, 3), 'front'), (range(3, 6), 'back'), (range(6, 9), 'side')):
        for j in frs:
            for L in (O, U): L.f[j][~BB[key]] = 0                     # 그림 속 꼬리는 걷고 새로 그려요
            if key == 'back':                                        # 걷고 빈 뒤통수는 머리카락으로
                e = BB['back0'] & (O.f[j][..., 3] == 0) & (U.f[j][..., 3] == 0); O.f[j][e] = g(HAIR_MID)
    T, H, L_, R_, cx = F['T'], F['H'], F['L'], F['R'], F['cx']
    rec = []                                                         # 검사용 (보기, 층, 묶는 점, 마스크)
    def put(layer, frs, pts, ax, ay, view, tie=True):
        for j in frs:
            m = paste_tail(layer.f[j], pts, ax, ay, tie)
        rec.append(dict(view=view, layer='O' if layer is O else 'U', ax=ax, ay=ay, mask=m))
    if kind == 'high':
        v = T + round(H * .2)
        for j in range(3):                                           # 앞: 정수리 뒤 볼륨만
            for x in range(cx - 2, cx + 2): fill(U.f[j], T - 1, x)
            for x in range(cx - 1, cx + 1): fill(U.f[j], T - 2, x)
        put(O, range(6, 9), tail_px(34 - v, 5, 2, 1, 1), G['X1'], v - dy, 'side')
        put(O, range(3, 6), tail_px(35 - v, 5, 0, 0, 0), cx, v, 'back')
    elif kind == 'side':
        v = F['eye_top'] + (3 if low else 1); sgn = 1 if spec['side'] == 'L' else -1   # 캐릭터의 왼쪽 = 앞에서 화면 오른쪽
        fxa = cx + sgn * 9; bxa = cx - sgn * 9
        dl = F['B'] - v + 1
        put(O, range(0, 3), tail_px(36 - v, 5, 0, 0, -sgn, delay=dl), fxa, v, 'front')
        put(O, range(3, 6), tail_px(36 - v, 5, 0, 0, sgn), bxa, v, 'back')
        if spec['side'] == 'L': put(O, range(6, 9), tail_px(36 - v, 5, 0, 0, -1, delay=dl), G['ear_x'] + 4, v - dy, 'side')
        else: put(U, range(6, 9), tail_px(36 - v, 3, 0, 0, 1), G['X1'] - 1, v - dy, 'side')
    elif kind == 'twin':
        v = F['eye_top'] + (3 if low else -1); br = spec.get('braid', False)
        for sgn in (1, -1):
            put(U, range(0, 3), tail_px(37 - v, 5, 0, 0, sgn, br), cx + sgn * 9, v, 'front')
            put(O, range(3, 6), tail_px(37 - v, 5, 0, 0, -sgn, br), cx - sgn * 9, v, 'back')
        put(O, range(6, 9), tail_px(37 - v, 5, 1, 1, 0, br), G['ear_x'] + 3, v - dy, 'side')
        put(U, range(6, 9), tail_px(37 - v, 3, 0, 0, 1, br), G['X1'], v - dy, 'side')
    TAIL_REC[n] = rec
TAIL_REC = {}
