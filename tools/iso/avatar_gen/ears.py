# 정면 귀 정리: 그림 속 귀(갈색 덩어리 안 초록·검정 점)를 피부색 2×3 + 안쪽 그림자 1칸으로
# 머리카락이 귀 자리를 덮는 머리는 그대로 둬요 (귀가 안 보이는 머리)
import numpy as np
SK, SK_SH, SK_LINE = 205, 168, 120
ROWS = (23, 25)                     # 귀 줄 (프레임 좌표, 아래로 내리기 전) — 까까머리 정면 귀 자리
EARS = ((9, 10, 'L'), (26, 27, 'R'))  # (바깥 열, 안쪽 열)
def g(v): return np.array([v, v, v, 255], np.uint8)
def covered(o, x0, x1):
    y0, y1 = ROWS; box = o[y0 - 1:y1 + 2, min(x0, x1) - 1:max(x0, x1) + 2]
    m = box[..., 3] > 0; gray = (box[..., 0] == box[..., 1]) & (box[..., 1] == box[..., 2])
    return int((m & gray & (box[..., 0] > 60)).sum()) > 3          # 진짜 머리카락(밝은 회색)이 3칸 넘게
def fix_front_ears(O, S):
    for j in range(3):
        o, s = O.f[j], S.f[j]
        for xo, xi, side in ((9, 10, 'L'), (27, 26, 'R')):
            if covered(o, xo, xi): continue
            y0, y1 = ROWS; xs = sorted((xo, xi)); out = xo - 1 if side == 'L' else xo + 1
            o[y0 - 1:y1 + 2, min(xs[0], out):max(xs[1], out) + 1] = 0
            for y in range(y0, y1 + 1):
                s[y, xo] = g(SK); s[y, xi] = g(SK_SH); s[y, out] = g(SK_LINE)
            for x in xs: s[y0 - 1, x] = g(SK_LINE); s[y1 + 1, x] = g(SK_LINE)
        # 얼굴 테두리 열의 색 섞인 어두운 점 → 회색 테두리
        for x in (11, 25):
            col = o[20:28, x]; m = (col[..., 3] > 0) & ~((col[..., 0] == col[..., 1]) & (col[..., 1] == col[..., 2])) & (col[..., :3].max(-1) < 90)
            col[m, :3] = 30
