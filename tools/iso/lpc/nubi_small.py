# 누비 인형 크기 (32×32 칸 · 조연 동물 cast_animals 와 같은 크기)
#   1 줄: 해진 4 방향 · 해진 + 리본 4 · 고쳐진 + 리본 4 (앞 · 왼쪽 · 오른쪽 · 뒤)
#   2 줄: 잿빛 1 단계 4 · 잿빛 2 단계 4 · 잿빛 2 단계 + 리본 4
#   3 줄: 잿빛 1 단계 + 리본 4 · 빛나는 눈 (0 · 1 · 2 단계 앞) · 터진 옆구리 (2 단계 + 리본 앞) · 초상화도 이 작은 그림을 작게 그대로 써요
#   python3 nubi_small.py → public/art/nubi_s.png (384×96) · tools/nubi_mock/nubi_small_prev.png
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
FRONT = """
....oooooo....
...oHLLHHHo...
..oHLHhHHhHo..
.oHLHHHHHHHHo.
.oHhSSSSSShHo.
.oHSSSSSSSSHo.
.oHSxSxSBBSHo.
.ohSSxSSBBSho.
.oHSxSxSSSSHo.
..oSSmmmmSSo..
...oSSSSSSo...
..oGGggggGGo..
.oGgGggggGgGo.
.oSgppggggkSo.
.oSgppgggggSo.
..ogggggggko..
..okgggggkko..
...oSSooSSo...
...oSdooSdo...
....oo..oo....
"""
RIGHT = """
....ooooo.....
...oHLLHHo....
..oHLHHHHHo...
.oHLHHHHHHHo..
.oHHHHHhSSSo..
.oHHHHHSSSSSo.
.oHHHHSSxSxSo.
.ohHHHSSSxSSo.
..oHHHSSxSxSo.
..oHHSSSSSmmo.
...ooSSSSSoo..
....oggGGGo...
...oggGGGGGo..
...oggSGppGo..
...oggSGppgo..
...okgggggko..
...okkgggkko..
....oSSoSSo...
....oSdoSdo...
.....oo.oo....
"""
BACK = """
....oooooo....
...oHLLHHHo...
..oHLHhHHhHo..
.oHLHHHHHHHHo.
.oHHHhHHHHHHo.
.oHHHHHHhHHHo.
.oHhHHHHHHhHo.
.ohHHHHhHHHho.
.oHHHHHHHHHHo.
..oHHhHHHHHo..
...oSSSSSSo...
..oGGggggGGo..
.oGgGgkgggGGo.
.oSgggggppgSo.
.oSgggkgppgSo.
..ogggggggko..
..okggkggkko..
...oSSooSSo...
...oSdooSdo...
....oo..oo....
"""
def grid(s): return [r for r in s.strip('\n').split('\n')]
def mirror(g): return [r[::-1] for r in g]
LEFT = mirror(grid(RIGHT))
LEFT = [r.replace('x', 'S').replace('m', 'S') for r in LEFT]
LEFT[6] = LEFT[6][:3] + 'SBB' + LEFT[6][6:]; LEFT[7] = LEFT[7][:3] + 'SBB' + LEFT[7][6:]
LEFT[9] = LEFT[9][:3] + 'mm' + LEFT[9][5:]
LEFT[13] = LEFT[13].replace('pp', 'gk'); LEFT[14] = LEFT[14].replace('pp', 'kg')
PAL = {
 False: dict(o='#231c22', H='#7d7679', h='#5e575a', L='#9c9696', S='#c6c0bb', s='#a19a9a', d='#7d7679', G='#8ea8bc', g='#6c869c', k='#4e667c', p='#b89a5a', x='#2e2228', m='#2e2228', B='#1a1020'),
 True: dict(o='#231c22', H='#9c9696', h='#7d7679', L='#bcb6b2', S='#e0dcd6', s='#c6c0bb', d='#a19a9a', G='#9cc4e4', g='#78a4cc', k='#5480a8', p='#ffe9a8', x='#1a1020', m='#7a3040', B='#1a1020'),   # 고쳐진 누비: 같은 파란 아이 · 깨끗한 헝겊
}
STAGE = {   # 잿빛 단계: 1 조금 · 2 많이 (터지기 직전)
 1: dict(H='#6a6366', h='#4e484b', L='#857e80', S='#aaa39f', s='#8d8683', d='#6d6764', G='#7e94a6', g='#5e7486', k='#44586a'),
 2: dict(H='#56504f', h='#3e3a3b', L='#6e6869', S='#8f8986', s='#76706e', d='#5a5452', G='#6c7e8e', g='#506272', k='#3a4a58'),
}
def draw(g, fixed, view, rib=False, stage=0, glow=False, burst=False):
    a = np.zeros((32, 32, 4), np.uint8); ox, oy = 9, 11
    P = dict(PAL[fixed]); P.update(STAGE.get(stage, {}))
    for y, r in enumerate(g):
        for x, ch in enumerate(r):
            if ch == '.': continue
            c = ch
            if fixed and ch == 'x': c = 'S'
            if fixed and ch == 'm': c = 'S'
            col = P[c]; a[oy + y, ox + x, :3] = [int(col[i:i + 2], 16) for i in (1, 3, 5)]; a[oy + y, ox + x, 3] = 255
    def px(pts, col):
        for x, y in pts: a[oy + y, ox + x, :3] = [int(col[i:i + 2], 16) for i in (1, 3, 5)]; a[oy + y, ox + x, 3] = 255
    if not fixed:
        if view == 'front': px([(8, 6)], '#e0dcd6'); px([(3, 4), (4, 5)], '#2e2228')                     # 단추 반짝 · 볼 바늘땀
        if view == 'left': px([(4, 6)], '#e0dcd6')
        if view in ('front', 'right', 'back'):                                                            # 덧댄 헝겊 바늘땀
            for (x, y) in {'front': [(4, 13), (5, 14)], 'right': [(8, 13), (9, 14)], 'back': [(8, 13), (9, 14)]}[view]: px([(x, y)], '#5a4422')
    else:
        B = '#1a1020'
        if view == 'front':
            px([(4, 6), (5, 6), (4, 7), (5, 7)], B); px([(4, 6), (8, 6)], '#ffffff'); px([(3, 8), (10, 8)], '#f08aa0')
            px([(6, 9), (7, 9)], '#7a3040'); px([(4, 13), (5, 13)], '#ffe9a8'); px([(4, 14), (5, 14)], '#e8c070')
        if view == 'right': px([(8, 6), (9, 6), (8, 7), (9, 7)], B); px([(8, 6)], '#ffffff'); px([(9, 8)], '#f08aa0'); px([(10, 9), (11, 9)], '#7a3040')
        if view == 'left': px([(4, 6)], '#ffffff'); px([(4, 8)], '#f08aa0'); px([(2, 9), (3, 9)], '#7a3040')
    if not fixed and stage >= 1:   # 늘어난 바늘땀
        K = '#1e181c'
        if view == 'front': px([(9, 3), (10, 4), (11, 5), (10, 3)] + [(7, 12), (8, 13), (9, 14)], K)
        if view == 'right': px([(9, 3), (10, 4), (11, 5)] + [(6, 12), (7, 13)], K)
        if view == 'left': px([(3, 3), (4, 4), (2, 4)] + [(6, 12), (7, 13)], K)
        if view == 'back': px([(4, 3), (5, 4), (6, 5), (9, 2), (10, 3)], K)
    if not fixed and stage >= 2:
        K = '#1e181c'
        if view == 'front': px([(2, 6), (2, 7), (11, 7), (11, 8)] + [(2, 13), (11, 14), (6, 15), (7, 16)], K); px([(5, 9)], K)
        if view in ('left', 'right'): px([(5, 15), (6, 16), (8, 15)] + ([(10, 7), (10, 8)] if view == 'right' else [(3, 7), (3, 8)]), K)
        if view == 'back': px([(3, 13), (4, 14), (10, 13), (9, 14), (7, 6), (8, 7)], K)
    if glow and view == 'front':   # 어둠 속에서 빛나는 단추 눈
        px([(8, 6), (9, 6), (8, 7), (9, 7)], '#ffd84a'); px([(8, 6)], '#fff6c0')
    if burst and view == 'front':   # 옆구리가 터져 솜이 비어져 나옴
        px([(10, 12), (10, 13), (10, 14)], '#1e181c'); px([(11, 12), (11, 13), (11, 14), (12, 12), (12, 13), (12, 14), (13, 13), (12, 11), (13, 12), (14, 12), (14, 13), (13, 11), (13, 14), (12, 15), (14, 11)], '#f4f2ec'); px([(14, 14), (13, 15), (11, 11), (15, 12), (11, 15)], '#d8d4ca')
        px([(13, 12)], '#ffffff')
    if rib:   # 리나가 매어 준 빛바랜 리본 (목 · 누렇게 바랜 크림색)
        L_, M_, D_ = '#f4e2a8', '#d4b868', '#6a4e20'
        if view == 'front':
            px([(x, 10) for x in range(4, 10)], M_); px([(3, 10), (4, 11), (9, 11), (10, 10)], D_); px([(4, 10), (5, 10), (8, 10), (9, 10)], L_)
            px([(6, 10), (7, 10)], D_); px([(6, 11), (7, 11)], M_); px([(5, 12), (8, 12)], D_)
        if view == 'right': px([(x, 10) for x in range(5, 10)], M_); px([(8, 10), (9, 9)], L_); px([(10, 9), (9, 10)], D_); px([(9, 11), (10, 11)], M_); px([(10, 12)], D_)
        if view == 'left': px([(x, 10) for x in range(4, 9)], M_); px([(5, 10), (4, 9)], L_); px([(3, 9), (4, 10)], D_); px([(3, 11), (4, 11)], M_); px([(3, 12)], D_)
        if view == 'back': px([(x, 10) for x in range(4, 10)], M_); px([(5, 10), (6, 10)], L_); px([(3, 10), (10, 10)], D_)
    return a
VIEWS = [('front', grid(FRONT)), ('left', LEFT), ('right', grid(RIGHT)), ('back', grid(BACK))]
if __name__ == '__main__':
    def row(specs):
        r = np.zeros((32, 32 * 12, 4), np.uint8)
        for i, sp in enumerate(specs):
            if sp is None: continue
            f, rb, st, gl, bu, vv = sp; g = dict(VIEWS)[vv]; r[:, i * 32:(i + 1) * 32] = draw(g, f, vv, rb, st, gl, bu)
        return r
    V4 = [v for v, _ in VIEWS]
    R0 = row([(False, False, 0, False, False, v) for v in V4] + [(False, True, 0, False, False, v) for v in V4] + [(True, True, 0, False, False, v) for v in V4])
    R1 = row([(False, False, 1, False, False, v) for v in V4] + [(False, False, 2, False, False, v) for v in V4] + [(False, True, 2, False, False, v) for v in V4])
    R2 = row([(False, True, 1, False, False, v) for v in V4] + [(False, False, s, True, False, 'front') for s in (0, 1, 2)] + [(False, True, 2, False, True, 'front')] + [None] * 4)
    sh = np.concatenate([R0, R1, R2], 0); Image.fromarray(sh).save(os.path.join(ROOT, 'public', 'art', 'nubi_s.png'))
    # 미리보기: 줄마다 · 빛나는 눈은 어두운 바탕
    pv = Image.new('RGBA', (32 * 12, 96), (250, 241, 226, 255))
    d = Image.new('RGBA', (32 * 3, 32), (20, 14, 30, 255)); pv.alpha_composite(d, (32 * 4, 64))
    pv.alpha_composite(Image.fromarray(sh))
    out = Image.new('RGBA', (32 * 12, 72), (250, 241, 226, 255))
    for k in range(3): out.alpha_composite(pv.crop((0, k * 32 + 8, 32 * 12, k * 32 + 32)), (0, k * 24))
    out.resize((out.width * 5, out.height * 5), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_small_prev.png'))
    print('ok')
