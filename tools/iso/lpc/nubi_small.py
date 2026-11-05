# 누비 인형 크기 (32×32 칸 · 조연 동물 cast_animals 와 같은 크기) · nubi_lpc.py 의 색을 그대로 써요
#   칸: 0 해진 앞 · 1 해진 왼쪽 · 2 해진 오른쪽 · 3 해진 뒤 · 4~7 고쳐진 (앞 · 왼쪽 · 오른쪽 · 뒤)
#   python3 nubi_small.py → public/art/nubi_s.png (256×32) · tools/nubi_mock/nubi_small_prev.png
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
 True: dict(o='#2a1c1c', H='#a0603a', h='#7a4428', L='#c88858', S='#f2e0c4', s='#dcbe9c', d='#c4a080', G='#f8c4d0', g='#eaa0b2', k='#d07a92', p='#fff0d8', x='#1a1020', m='#7a3040', B='#1a1020'),
}
def draw(g, fixed, view):
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
            px([(6, 9), (7, 9)], '#7a3040'); px([(4, 13), (5, 13)], '#fff0d8'); px([(4, 14), (5, 14)], '#e8b8b0')
        if view == 'right': px([(8, 6), (9, 6), (8, 7), (9, 7)], B); px([(8, 6)], '#ffffff'); px([(9, 8)], '#f08aa0'); px([(10, 9), (11, 9)], '#7a3040')
        if view == 'left': px([(4, 6)], '#ffffff'); px([(4, 8)], '#f08aa0'); px([(2, 9), (3, 9)], '#7a3040')
        rb = {'front': 9, 'right': 7, 'left': 3, 'back': 2}[view]                                        # 리본
        px([(rb, 0), (rb + 3, 0), (rb, 1), (rb + 1, 1), (rb + 2, 1), (rb + 3, 1)], '#d07a92'); px([(rb + 1, 0), (rb + 2, 0)], '#f8c4d0'); px([(rb + 1, 1), (rb + 2, 1)], '#9a4a62')
        px([(rb + 1, 2), (rb + 2, 2)], '#9a4a62')
    return a
VIEWS = [('front', grid(FRONT)), ('left', LEFT), ('right', grid(RIGHT)), ('back', grid(BACK))]
if __name__ == '__main__':
    cells = [draw(g, f, v) for f in (False, True) for v, g in VIEWS]
    sh = np.concatenate(cells, 1); Image.fromarray(sh).save(os.path.join(ROOT, 'public', 'art', 'nubi_s.png'))
    # 미리보기: 학생 크기(64 칸 누비 큰 그림)와 나란히
    big = Image.open(os.path.join(ROOT, 'public', 'art', 'nubi.png')).convert('RGBA').crop((0, 0, 64, 64))
    pv = Image.new('RGBA', (64 + 32 * 8 + 16, 64), (250, 241, 226, 255)); pv.alpha_composite(big, (0, 0))
    for i, c in enumerate(cells): pv.alpha_composite(Image.fromarray(c), (80 + i * 32, 32))
    pv.resize((pv.width * 5, pv.height * 5), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_small_prev.png'))
    print('ok')
