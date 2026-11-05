# 친구 인형 「겹이」: 우리 반 열두 색 조각보 인형 (누비와 같은 32 칸 · 같은 틀) · 짜이는 단계 3 칸 (실 공 → 반쯤 → 다 짜임)
#   python3 nubi_friend.py → public/art/nubi_friend.png (96×32) · tools/nubi_mock/nubi_friend_prev.png
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..'); sys.path.insert(0, HERE)
from nubi_small import FRONT, grid
COL = ['#E86A6A', '#F0A060', '#F0C040', '#B8D860', '#8AD08A', '#5AC8B0', '#6AA8E8', '#7A86E0', '#C88AE8', '#F08AC0', '#D8B890', '#9C9696']
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c)
OUT = hx('#2a1a22')
def doll(rows=None):
    g = grid(FRONT); a = np.zeros((32, 32, 4), np.uint8); ox, oy = 9, 11
    for y, r in enumerate(g):
        if rows is not None and y < rows: continue        # 아래부터 짜여 올라와요
        for x, ch in enumerate(r):
            if ch == '.': continue
            if ch == 'o': c = OUT
            elif ch in 'Ssxm' and y <= 10: c = hx('#f4ead8') if ch != 's' else hx('#dccfb8')   # 얼굴은 크림색 무명
            else:
                k = (x // 3 + (y // 3) * 3) % 12; c = hx(COL[k])               # 3 칸 조각마다 다른 친구 색
                if ch in 'hdk': c = sh(c, .78)
                elif ch in 'LG': c = sh(c, 1.12)
                if (x % 3 == 0 or y % 3 == 0) and ch not in 'o': c = sh(c, .9)  # 조각 사이 바늘땀 선
            a[oy + y, ox + x, :3] = c; a[oy + y, ox + x, 3] = 255
    if rows is None or rows <= 6:
        for (x, y) in ((4, 6), (5, 6), (4, 7), (5, 7), (8, 6), (9, 6), (8, 7), (9, 7)): a[oy + y, ox + x, :3] = hx('#1a1020')
        for (x, y) in ((4, 6), (8, 6)): a[oy + y, ox + x, :3] = hx('#ffffff')
        for (x, y) in ((6, 9), (7, 9)): a[oy + y, ox + x, :3] = hx('#7a3040')
        for (x, y) in ((3, 8), (10, 8)): a[oy + y, ox + x, :3] = hx('#f08aa0')
    return a
def yarn_ball():
    a = np.zeros((32, 32, 4), np.uint8)
    for y in range(32):
        for x in range(32):
            d = ((x - 16) ** 2 + (y - 24) ** 2) ** .5
            if d <= 6.5: a[y, x, :3] = sh(hx(COL[int((x + y * .7) / 2) % 12]), .85 if d > 5.5 else 1); a[y, x, 3] = 255
            elif d <= 7.5: a[y, x, :3] = OUT; a[y, x, 3] = 255
    return a
if __name__ == '__main__':
    cells = [yarn_ball(), doll(rows=10), doll()]
    sh_ = np.concatenate(cells, 1); Image.fromarray(sh_).save(os.path.join(ROOT, 'public', 'art', 'nubi_friend.png'))
    nb = np.array(Image.open(os.path.join(ROOT, 'public', 'art', 'nubi_s.png')).convert('RGBA'))[0:32, 256:288]
    pv = Image.new('RGBA', (32 * 5 + 8, 32), (43, 31, 69, 255))
    for i, c in enumerate(cells): pv.alpha_composite(Image.fromarray(c), (i * 32, 0))
    pv.alpha_composite(Image.fromarray(nb), (3 * 32 + 4, 0)); pv.alpha_composite(Image.fromarray(cells[2]), (3 * 32 + 22, 0))
    pv.crop((0, 8, pv.width, 32)).resize(((pv.width) * 6, 24 * 6), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_friend_prev.png'))
    print('ok')
