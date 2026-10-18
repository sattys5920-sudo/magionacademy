# 얼굴 그리드 (모든 머리·표정이 같은 좌표를 써요). 기준 = 까까머리(13번) 머리의 피부·머리 윤곽
# 앞: T(정수리)·B(턱)·L/R(얼굴 좌우)·cx 에서 눈·입·볼·눈썹 자리를 계산. 옆: 왼쪽을 보는 옆얼굴을 새로 그려요(눈 1개, 코끝, 귀)
import numpy as np
BASE_HAIR = 12
def box(S, O, fr):
    s = S.f[fr, ..., 3] > 0; u = s | (O.f[fr, ..., 3] > 0)
    T = int(np.nonzero(u.any(1))[0].min()); B = int(np.nonzero(s.any(1))[0].max()); H = B - T + 1
    y = T + round(H * .52); c = (np.nonzero(s[y])[0].min() + np.nonzero(s[y])[0].max()) // 2   # 눈 높이 줄에서
    L = R = c                                                     # 가운데에서 이어진 피부 끝까지 (귀는 테두리로 떨어져 있어서 빠져요)
    while L > 0 and s[y, L - 1]: L -= 1
    while R < s.shape[1] - 1 and s[y, R + 1]: R += 1
    return dict(T=T, B=B, H=H, L=int(L), R=int(R), u=u, s=s)
def grid(S, O):
    f = box(S, O, 0); W = f['R'] - f['L'] + 1; cx = (f['L'] + f['R']) // 2
    et = f['T'] + round(f['H'] * .52); gap = max(4, round(W * .22)); ew = 2
    F = dict(T=f['T'], B=f['B'], H=f['H'], L=f['L'], R=f['R'], W=W, cx=cx, eye_top=et, eye_h=3, eye_w=ew, eye_gap=gap,
             brow_row=et - 2, blush_row=et + 3, mouth_row=et + 4, lx=cx - gap // 2 - ew, rx=cx + gap // 2)
    F['safe'] = (et - 1, et + 2, F['lx'] - 1, F['rx'] + ew)     # 행 위·아래, 열 왼·오른 (포함)
    s = box(S, O, 6); ets = s['T'] + round(s['H'] * .52)
    # 옆 얼굴 앞 윤곽: 이마 줄들에서 피부가 시작하는 x - 1 (테두리 자리)
    fx = int(np.median([np.nonzero(s['s'][y])[0].min() for y in range(ets - 4, ets)])) - 1
    xs = np.nonzero(s['u'].any(0))[0]; hc = (xs.min() + xs.max()) / 2
    G = dict(T=s['T'], B=s['B'], H=s['H'], eye_top=ets, mouth_row=ets + 4, front=fx, eye_x=fx + 2, mouth_x=fx + 1,
             ear_x=int(np.floor(hc)) + 1, u=s['u'], s=s['s'])
    G['safe'] = (ets - 1, ets + 2, G['eye_x'] - 1, G['eye_x'] + 2)
    assert F['B'] - F['mouth_row'] >= 2 and G['B'] - G['mouth_row'] >= 2
    return F, G
def report(F, G):
    k = lambda d: {a: b for a, b in d.items() if not isinstance(b, np.ndarray)}
    print('FRONT', k(F)); print('SIDE ', k(G))

# ---------- 픽셀맵 ----------
# K 속눈썹 · W 흰 반짝 · I 홍채 · i 홍채 밝은색 · D 홍채 어두운색 (I/i/D는 고른 눈 색) · P 동공 · H 하트 · Y 별 · T 눈물 · V 뱀파이어
# 앞 왼쪽 눈: 3칸 = [바깥 속눈썹 1칸 | 눈 박스 2칸], 3줄. 오른쪽 눈은 좌우 반전
COL = dict(K=(42, 24, 48, 255), W=(255, 255, 250, 255), I=(130, 130, 130, 255), i=(205, 205, 205, 255), D=(70, 70, 70, 255),
           P=(24, 12, 30, 255), H=(236, 72, 110, 255), Y=(255, 214, 90, 255), T=(160, 214, 255, 255), V=(206, 40, 64, 255),
           M=(120, 46, 66, 255), R=(196, 64, 86, 255), E=(255, 255, 250, 255))   # E = 입 속 흰 이
EYES = [
    ['KKK', '.WI', '.Ii'],   # 반짝 동글
    ['KKK', '.WD', '.Di'],   # 큰 애니 (진한 눈동자)
    ['...', '.KK', '.Ii'],   # 졸린 눈 (눈꺼풀이 내려옴)
    ['...', 'KKK', '...'],   # 웃는 눈 ^ ^ (행1에 3칸)
    ['KKK', '.iP', '.iP'],   # 고양이 눈 (세로 동공)
    ['KKK', '.YI', '.IY'],   # 별 눈동자
    ['...', '.HH', '.H.'],   # 하트 눈동자
    ['KKK', '.WI', '.Ii'],   # 윙크 (오른쪽은 감은 눈)
    ['.KK', '.WI', '.Ii'],   # 단호한 눈 (안쪽으로 내려온 속눈썹)
    ['KKK', '.WI', '.TT'],   # 눈물 그렁
    ['KKK', '.KK', '.K.'],   # 빙글빙글
    ['...', '..K', '...'],   # 점 눈
    ['KKK', '.VP', '.VV'],   # 뱀파이어 눈
    ['KKK', '.Wi', '.iW'],   # 순정 반짝
    ['.K.', '..K', '.K.'],   # 질끈 감은 눈 > <
]
WINK_R = ['...', 'KKK', '...']
# 옆 눈: 2칸 3줄 (왼쪽 = 얼굴 앞). 기본은 규칙 그대로, 나머지는 앞 왼쪽 눈 박스를 좌우로 뒤집어서
SIDE_EYE0 = ['KK', 'IW', 'Ii']
def side_eye(i):
    if i in (0, 7): return SIDE_EYE0
    r = [row[1:][::-1] for row in EYES[i]]
    if EYES[i][0][0] == 'K': r[0] = 'KK'
    return r
# 입: 짝수 너비(눈 사이 가운데에 맞춰요), 4칸·2줄까지. 고양이 입·혀·3칸 넘는 이는 쓰지 않아요
MOUTHS = [
    (['M..M', '.MM.'], '미소'),
    (['MM'], '기본 입'),
    (['.MM.', 'M..M'], '시무룩'),
    (['MMMM', '..E.'], '송곳니 미소'),
    (['MMMM', '.EE.'], '활짝 웃음'),
    (['MM', 'MM'], '놀란 입'),
    (['MMMM', '.RR.'], '헤벌쭉'),
    (['MMMM'], '일자 입'),
    (['MMMM', 'MEEM'], '이 드러낸 웃음'),
    (['M.M.', '.M.M'], '울먹'),
    (['...M', 'MMM.'], '씩 웃음'),
    (['M.', '.M'], '뽀뽀'),
    (['.MM.', 'MRRM'], '깜짝 O'),
    (['.MMM', 'M...'], '삐죽'),
    (['M..M', '.RR.'], '방긋'),
]
def side_mouth(i):
    m = MOUTHS[i][0]; return [row[:2] for row in m]
BLUSH = (236, 112, 124, 102)       # 분홍 40% (게임이 피부 위에 섞어요)
SK, SK_SH, SK_LINE, HAIR_TIP = 205, 172, 120, 0.7   # 피부 회색, 그림자, 테두리, 앞머리 끝 어둡게
def pix(rows):
    h, w = len(rows), max(len(r) for r in rows); a = np.zeros((h, w, 4), np.uint8)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': a[y, x] = COL[ch]
    return a
def g(v): return np.array([v, v, v, 255], np.uint8)

# ---------- 층 만들기 ----------
def eye_layers(i, F, G, Lay):
    E, Br, Bl = Lay(), Lay(), Lay()
    gl = pix(EYES[i]); gr = pix(WINK_R)[:, ::-1] if i == 7 else gl[:, ::-1]
    se = pix(side_eye(i)); dot = np.array([[[0, 0, 0, 0]] * 2], np.uint8); dot[0, :] = BLUSH
    brow = np.array([[g(80)] * 2], np.uint8)
    for j in range(3):
        E.paste(j, gl, F['lx'] - 1, F['eye_top']); E.paste(j, gr, F['rx'], F['eye_top'])
        Br.paste(j, brow, F['lx'], F['brow_row']); Br.paste(j, brow, F['rx'], F['brow_row'])
        Bl.paste(j, dot, F['lx'] - 1, F['blush_row']); Bl.paste(j, dot, F['rx'] + 1, F['blush_row'])
        f = 6 + j
        E.paste(f, se, G['eye_x'], G['eye_top']); Br.paste(f, brow, G['eye_x'], G['eye_top'] - 2)
        Bl.paste(f, dot[:, :1], G['eye_x'] + 1, G['eye_top'] + 3)
    return E, Br, Bl
def mouth_layer(i, F, G, Lay):
    M = Lay(); m = pix(MOUTHS[i][0]); w = m.shape[1]; x0 = (F['lx'] + F['eye_w'] + F['rx']) // 2 - w // 2
    sm = pix(side_mouth(i))
    for j in range(3): M.paste(j, m, x0, F['mouth_row']); M.paste(6 + j, sm, G['mouth_x'], G['mouth_row'])
    return M
def ear_layer(G, Lay):
    """옆 귀: 머리 가로 가운데보다 1칸 뒤, 눈 줄부터 3줄. 피부 2칸 + 안쪽 그림자 1칸 + 테두리"""
    A = Lay(); x, y = G['ear_x'], G['eye_top']; a = np.zeros((5, 4, 4), np.uint8)
    for yy in range(1, 4):
        a[yy, 0] = a[yy, 3] = g(SK_LINE); a[yy, 1] = a[yy, 2] = g(SK)
    a[0, 1] = a[0, 2] = a[4, 1] = a[4, 2] = g(SK_LINE); a[2, 1] = g(SK_SH)
    for j in range(6, 9): A.paste(j, a, x - 1, y - 1)
    return A
def profile_skin(BS, BO, G):
    """옆얼굴 피부 (모든 머리 공통): 까까머리 옆 피부에서 앞 윤곽만 규칙대로 다시. 이마 수직, 코끝 1칸, 입 아래 턱 1칸 들어감"""
    P = BS.f[6].copy(); et, mr, B, fx = G['eye_top'], G['mouth_row'], G['B'], G['front']
    top = int(np.nonzero((P[..., 3] > 0).any(1))[0].min())
    ear = np.zeros(P.shape[:2], bool)
    for y in range(top, B + 1):
        xs = np.nonzero(P[y, :, 3])[0]
        if not len(xs): continue
        if y <= et + 1: xf = fx + 1
        elif y == et + 2: xf = fx          # 코끝
        elif y <= mr: xf = fx + 1
        elif y < B: xf = fx + 2            # 턱 아래로 들어감
        else: xf = max(fx + 3, xs.min())
        right = xs.max()
        P[y, :xf] = 0
        for x in range(xf, right + 1):
            if not P[y, x, 3]: P[y, x] = g(SK)
        if y >= top + 1: P[y, xf - 1] = g(SK_LINE)
        if y <= et + 4: ear[y, G['ear_x'] + 3:] = P[y, G['ear_x'] + 3:, 3] > 0   # 그림 속 옛 귀 자리 → 뒷머리로
    P[ear] = 0
    return P, ear
def apply_face(n, O, S, F, G, PS, ear):
    """머리 n: 옆 피부를 공통 옆얼굴로, 눈 안전 구역의 머리카락은 걷고 끝 1칸은 그림자색"""
    t, b, l, r = F['safe']
    for j in range(3):
        o, s = O.f[j], S.f[j]
        for x in range(l, r + 1):
            hit = o[t:b + 1, x, 3].any()
            o[t:b + 1, x] = 0
            for y in range(t, b + 1):
                if not s[y, x, 3]: s[y, x] = g(SK)
            if hit and o[t - 1, x, 3]: o[t - 1, x, :3] = (o[t - 1, x, :3] * HAIR_TIP).astype(np.uint8)
    t, b, l, r = G['safe']
    for j in range(6, 9):
        o = O.f[j]; S.f[j] = PS
        o[G['eye_top'] + 2, G['front']] = 0   # 코끝 자리
        for x in range(l, r + 1):
            hit = o[t:b + 1, x, 3].any(); o[t:b + 1, x] = 0
            if hit and o[t - 1, x, 3]: o[t - 1, x, :3] = (o[t - 1, x, :3] * HAIR_TIP).astype(np.uint8)
        # 옛 귀 자리에 머리카락이 없으면 뒷머리 색으로
        m = ear & ~(o[..., 3] > 0); o[m] = g(140)
