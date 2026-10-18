# 얼굴 규칙 검사: python3 verify_face.py  (assemble.py로 만든 ../out/avatar_parts.* 를 읽어요)
import json, os, sys, numpy as np
from PIL import Image
from scipy import ndimage
import assemble as A, face_grid as FG
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'out')
J = json.load(open(os.path.join(OUT, 'avatar_parts.json'))); S = np.array(Image.open(os.path.join(OUT, 'avatar_parts.png')))
FW, FH = J['fw'], J['fh']
BO, _, BS = A.hair_layers(FG.BASE_HAIR); F, G = FG.grid(BS, BO)
dy = J['head']['t'] - (A.CHIN - 20)                  # 출력 시트는 아래로 dy 내려가 있어요
def layer(r, fr): return S[r * FH:(r + 1) * FH, fr * FW:(fr + 1) * FW]
def alpha(rows, fr):
    m = np.zeros((FH, FW), bool)
    for r in rows: m |= layer(r, fr)[..., 3] > 0
    return m
bad = []
# 1. 눈 안전 구역에 머리카락 0
for n, p in enumerate(J['parts']['hair']):
    hr = [r for r, sl, z in p['L'] if z in ('hairO', 'hairU')]
    for frs, (t, b, l, r) in ((range(0, 3), F['safe']), (range(6, 9), G['safe'])):
        for fr in frs:
            k = int(alpha(hr, fr)[t + dy:b + dy + 1, l:r + 1].sum())
            if k: bad.append(f'머리 {n + 1} {p["n"]} 프레임 {fr}: 눈 안전 구역에 머리카락 {k}px')
# 2·3·4·5. 눈·입
et = F['eye_top'] + dy
for i, p in enumerate(J['parts']['eyes']):
    er = [p['L'][0][0]]; e = alpha(er, 0)
    ys = np.nonzero(e.any(1))[0]
    if len(ys) and (ys.min() < et or ys.max() > et + 2): bad.append(f'눈 {i + 1} {p["n"]}: 눈 박스(3줄) 밖 {ys.min() - dy}~{ys.max() - dy}')
    L, R = e[:, F['lx'] - 1:F['lx'] + 2], e[:, F['rx']:F['rx'] + 3]
    if int(e.sum()) != int(L.sum() + R.sum()): bad.append(f'눈 {i + 1} {p["n"]}: 눈 박스 밖 가로 픽셀')
    lr = set(np.nonzero(L.any(1))[0]); rr = set(np.nonzero(R.any(1))[0])
    if i != 7 and (lr != rr or not np.array_equal(L, R[:, ::-1])): bad.append(f'눈 {i + 1} {p["n"]}: 정면 두 눈이 대칭이 아니에요')
    se = alpha(er, 6); nlab = ndimage.label(se, np.ones((3, 3)))[1]
    if nlab != 1: bad.append(f'눈 {i + 1} {p["n"]}: 옆모습 눈 덩어리 {nlab}개')
    for fr in range(3, 6):
        if alpha([r for r, sl, z in p['L']], fr).any(): bad.append(f'눈 {i + 1} {p["n"]}: 뒷모습에 얼굴 픽셀')
for i, p in enumerate(J['parts']['mouth']):
    m = alpha([r for r, sl, z in p['L']], 0); ys = np.nonzero(m.any(1))[0]
    if F['B'] - (ys.max() - dy) < 2: bad.append(f'입 {i + 1} {p["n"]}: 입 아래 턱 2줄 미만')
    if F['B'] - F['mouth_row'] < 2: bad.append('mouth_row: 턱 2줄 미만')
    ms = alpha([r for r, sl, z in p['L']], 6); ys = np.nonzero(ms.any(1))[0]
    if len(ys) and G['B'] - (ys.max() - dy) < 2: bad.append(f'입 {i + 1} {p["n"]}: 옆 입 아래 턱 2줄 미만')
    for fr in range(3, 6):
        if alpha([r for r, sl, z in p['L']], fr).any(): bad.append(f'입 {i + 1} {p["n"]}: 뒷모습에 입 픽셀')
print('위반', len(bad)); print('\n'.join(bad))
sys.exit(1 if bad else 0)
