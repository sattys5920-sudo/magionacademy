# 누비 인형 크기 (32×32 칸 · 조연 동물 cast_animals 와 같은 크기)
#   칸: 0~3 해진 (앞 · 왼쪽 · 오른쪽 · 뒤) · 4~7 해진 + 리나의 리본 (6 일째부터) · 8~11 고쳐진 + 리본 (같은 파란 옷) · 초상화도 이 작은 그림을 작게 그대로 써요
#   python3 nubi_small.py → public/art/nubi_s.png (384×32) · tools/nubi_mock/nubi_small_prev.png
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
def draw(g, fixed, view, rib=False):
    a = np.zeros((32, 32, 4), np.uint8); ox, oy = 9, 11
    P = PAL[fixed]
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
    cells = [draw(g, f, v, r) for f, r in ((False, False), (False, True), (True, True)) for v, g in VIEWS]
    sh = np.concatenate(cells, 1); Image.fromarray(sh).save(os.path.join(ROOT, 'public', 'art', 'nubi_s.png'))
    # 미리보기: 학생(캐릭터 한 칸)과 나란히
    big = Image.open(os.path.join(ROOT, 'public', 'art', 'npcs.png')).convert('RGBA').crop((0, 64 * 10, 64, 64 * 11))
    pv = Image.new('RGBA', (64 + 32 * 12 + 16, 64), (250, 241, 226, 255)); pv.alpha_composite(big, (0, 0))
    for i, c in enumerate(cells): pv.alpha_composite(Image.fromarray(c), (80 + i * 32, 32))
    pv.resize((pv.width * 5, pv.height * 5), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_small_prev.png'))
    print('ok')
