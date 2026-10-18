# 표정 층: expr_feats.npz(생성기가 그린 얼굴, 프레임 좌표 1칸 = 1px) → 게임 색 규칙
# 눈동자(남색 계열)는 회색으로 바꿔 고른 눈 색으로 칠하고, 테두리·흰 반짝은 고정, 입·볼터치·하트·별·눈물·눈썹은 그림 색 그대로
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_Z = np.load(os.path.join(HERE, 'expr_feats.npz'))
NAMES = ['미소', '활짝 웃음', '윙크', '깜짝', '시무룩', '화남', '졸림', '수줍음',
         '하트 눈', '별 눈', '눈물 그렁', '메롱', '고양이 입', '빙글빙글', '자신만만', '질끈',
         '반짝반짝', '멍', '식은땀', '뿌루퉁']
N = len(NAMES)
LINE, WHITE = (42, 24, 48, 255), (255, 255, 250, 255)
MOUTH_TOP = {0: 25, 6: 22}          # 이 줄부터는 입 (색 그대로)
SIDE_MAX_X = 25                      # 옆: 이보다 뒤(귀 자리)는 밑그림과 귀 모양 차이라 빼요
def lum(c): return c[..., 0] * .3 + c[..., 1] * .59 + c[..., 2] * .11
def face(e, fr):
    a = _Z[f'{e}/{fr}'].copy()
    if fr == 6: a[:, SIDE_MAX_X + 1:] = 0
    a[:, :12] = 0                                            # 귀 자리 (밑그림 귀와 생성 귀 차이)
    if fr == 0: a[:, 25:] = 0
    m = a[..., 3] > 0; c = a[..., :3].astype(float); L = lum(c); sat = c.max(2) - c.min(2)
    yy = np.arange(a.shape[0])[:, None] * np.ones(a.shape[:2])
    mouth = m & (yy >= MOUTH_TOP[fr])
    dark = m & ~mouth & (L < 45)
    white = m & ~mouth & (c.min(2) > 195) & (sat < 45)
    navy = (L < 115) & (c[..., 2] >= c[..., 0])               # 눈동자 (남색·보라)
    keep = m & ~mouth & ~dark & ~white & (sat > 60) & ~navy    # 볼터치·하트·별·눈물·눈썹
    gray = m & ~mouth & ~dark & ~white & ~keep
    if e == 15: dark |= gray; gray &= False                 # 질끈(> <)은 눈동자가 없어요: 생성기 반짝이 표시가 섞인 칸은 선으로
    o = np.zeros_like(a)
    o[dark] = LINE; o[white] = WHITE; o[keep] = a[keep]; o[mouth] = a[mouth]
    gv = np.clip(70 + (L - 45) * 1.6, 70, 205).astype(np.uint8); o[gray, 0] = o[gray, 1] = o[gray, 2] = gv[gray]; o[gray, 3] = 255
    if fr == 6: narrow_far(o, MOUTH_TOP[fr])
    fix = (keep | mouth) & (o[..., 0] == o[..., 1]) & (o[..., 1] == o[..., 2])   # 색 그대로 둘 칸이 회색이면 살짝 비틀어요
    o[fix, 2] = np.where(o[fix, 2] > 250, o[fix, 2] - 3, o[fix, 2] + 3)
    return o

def eye_groups(o, top):
    cols = (o[:top, :, 3] > 0).any(0); xs = np.nonzero(cols)[0]; gs = []; cur = []
    for x in xs:
        if cur and x > cur[-1] + 1: gs.append(cur); cur = []
        cur.append(x)
    if cur: gs.append(cur)
    return gs
def narrow_far(o, top):
    """옆(3/4): 먼 쪽 눈(앞 윤곽 쪽, 왼쪽)은 가까운 눈보다 1칸 좁게 — 바깥 열부터 빼요"""
    gs = [g for g in eye_groups(o, top) if len(g) >= 1]
    if len(gs) < 2: return
    far, near = gs[0], gs[-1]
    cut = len(far) - (len(near) - 1)
    for x in far[:max(0, cut)]: o[:top, x] = 0
