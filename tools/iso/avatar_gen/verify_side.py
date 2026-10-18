# 옆 머리 구조·귀·포니테일 검사: python3 verify_side.py
import sys, numpy as np
import assemble as A, side_head as SH
C = A.face_ctx(); F, SG, BB = C['F'], C['SG'], C['BB']
bad = []; t, b, l, r = SH.ear_box(SG)
# 귀 모양·자리 (공통 옆 피부)
P = BB['PS']; ear = P[t:b + 1, l:r + 1]
w, h = r - l + 1, b - t + 1; pos = (r - SG['X0']) / SG['Wd']
if w != 2 or not 3 <= h <= 4: bad.append(f'귀 크기 {w}×{h}')
if not .55 <= pos <= .60: bad.append(f'귀 가로 위치 {pos:.2f} (55~60% 밖)')
if not (ear[..., 3] > 0).all(): bad.append('귀 피부 빈칸')
if not (P[t:b + 1, l, 0] < P[t:b + 1, r, 0]).all(): bad.append('귀 앞 열이 그림자색이 아님')
if P[t:b + 1, l - 1, 0].min() < SH.SK_SH and (P[t:b + 1, l - 1, 3] > 0).any() and (P[t:b + 1, l - 1, 0] == SH.SK_LINE).any(): bad.append('귀 앞쪽에 테두리')
if not (P[t:b + 1, r + 1, 0] == SH.SK_LINE).all(): bad.append('귀 뒤쪽 테두리 없음')
cx = F['cx']
for n in range(40):
    O, U, S = A.build_hair(n, C); name = A.HAIR_N[n]
    # 귀 노출 수
    vis = SH.EAR_VIS[n]; o = O.f[6]
    seen = int(((S.f[6, t:b + 1, l:r + 1, 3] > 0) & (o[t:b + 1, l:r + 1, 3] == 0)).sum())
    if seen != SH.EAR_EXPOSED[vis]: bad.append(f'{n + 1} {name}: 귀 노출 {seen}칸 ({vis}는 {SH.EAR_EXPOSED[vis]}칸)')
    # 얼굴 피부 안 머리카락 점 (앞)
    for j in range(3):
        k = int((BB['face'] & (O.f[j, ..., 3] > 0)).sum())
        if k: bad.append(f'{n + 1} {name}: 정면 얼굴 안 머리카락 {k}칸')
        s = S.f[j]; d = int((BB['face'] & (s[..., 3] > 0) & (s[..., 0] < 150) & (s[..., 0] == s[..., 1])).sum())
        if d: bad.append(f'{n + 1} {name}: 정면 얼굴 피부 안 어두운 점 {d}칸')
    # 옆: 얼굴(앞·가운데 1/3) 안 머리카락, 윤곽 밖 점
    et = SG['eye_top']; sk = BB['skull']
    for j in range(6, 9):
        o = O.f[j]; k = 0
        for y in range(et - 1, SG['B'] + 1):
            xs = np.nonzero(sk[y])[0]; hi = min(xs.max(), int(SG['thirds'][1])) if y <= b else xs.max()
            if y <= b: hi = min(hi, l - 2)
            k += int((o[y, SG['X0']:hi + 1, 3] > 0).sum())
        if k: bad.append(f'{n + 1} {name}: 옆 얼굴 안 머리카락 {k}칸')
        k = int((o[et - 1:, :SG['X0'], 3] > 0).sum()) + int((o[:et - 1, :SG['X0'] - 1, 3] > 0).sum())
        if k: bad.append(f'{n + 1} {name}: 옆 얼굴 윤곽 밖 머리카락 {k}칸')
    # 꼬리
    if n in SH.TAILS:
        sp = SH.TAILS[n]
        for rec in SH.TAIL_REC[n]:
            ys, xs = np.nonzero(rec['mask'])
            if ys.max() <= rec['ay']: bad.append(f'{n + 1} {name} {rec["view"]}: 꼬리 끝이 묶는 점보다 위')
            if rec['ay'] - ys.min() > 3: bad.append(f'{n + 1} {name} {rec["view"]}: 묶는 점 위로 {rec["ay"] - ys.min()}칸 솟음')
            if sp['kind'] == 'high' and rec['view'] == 'back' and abs(xs.mean() - cx) > 1: bad.append(f'{n + 1} {name}: 뒷모습 꼬리 무게중심 {xs.mean():.1f} (가운데 {cx})')
            if sp['kind'] == 'side':
                L = sp['side'] == 'L'
                if rec['view'] == 'front' and (rec['ax'] > cx) != L: bad.append(f'{n + 1} {name}: 정면 묶은 쪽 틀림')
                if rec['view'] == 'back' and (rec['ax'] < cx) != L: bad.append(f'{n + 1} {name}: 뒷모습 묶은 쪽 틀림')
                if rec['view'] == 'side' and (rec['layer'] == 'O') != L: bad.append(f'{n + 1} {name}: 옆모습 앞/뒤 층 틀림')
print('위반', len(bad)); print('\n'.join(bad)); sys.exit(1 if bad else 0)
