# 누비 (낡은 양호실의 헝겊 인형) · 동물 NPC 와 같은 그림체 (lpc/beasts.py 의 Sprite: 부위마다 6 단계 색 · 왼쪽 위 빛 · 부위 색 외곽선)
#   64 칸 × 8: 0~3 해진 누비 (가만히 · 빛나는 눈 · 훌쩍 · 놀람) · 4~7 고쳐진 누비 (가만히 · 웃음 · 눈 감음 · 수줍음)
#   해진 누비: 잿빛 헝겊 · 단추 눈 하나 없음(X 바늘땀) · 꿰맨 입 · 덧댄 헝겊 · 찢어진 팔에서 솜
#   고쳐진 누비: 크림빛 헝겊 · 단추 눈 둘 · 분홍 볼 · 리본 · 가슴에 하트 헝겊
#   python3 nubi_art.py → public/art/nubi.png (512×64) · tools/nubi_mock/nubi_prev.png (다른 NPC 와 나란히)
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, 'lpc'))
from beasts import Sprite, RAMP, px, hx, cat, owl, mandrake
RAMP['ash'] = ['#3A3438', '#5E565A', '#857C7E', '#A8A0A0', '#C8C2BE', '#E2DED8']
RAMP['patch'] = ['#1E2A36', '#34485A', '#4E667C', '#6C869C', '#8EA8BC', '#B4CAD8']
RAMP['stuff'] = ['#8A8478', '#B8B2A6', '#D8D4CA', '#ECE8E0', '#F8F6F0', '#FFFFFF']
def nubi(fixed, face, bob=0):
    cl = 'cream' if fixed else 'ash'
    y = bob
    S = Sprite()
    S.add(cl, lambda d: [d.ellipse([22, 52 + y, 31, 63]), d.ellipse([33, 52 + y, 42, 63])], -.05)                     # 다리
    S.add(cl, lambda d: d.ellipse([20, 36 + y, 44, 60 + y]))                                                         # 몸
    if not fixed: S.add('patch', lambda d: d.rectangle([24, 46 + y, 31, 53 + y]), .05)                               # 배에 덧댄 헝겊
    else: S.add('pink', lambda d: [d.ellipse([27, 43 + y, 32, 48 + y]), d.ellipse([31, 43 + y, 36, 48 + y]), d.polygon([(27, 46 + y), (36, 46 + y), (31.5, 53 + y)])], .1)   # 하트 헝겊
    S.add(cl, lambda d: d.ellipse([41, 38 + y, 50, 52 + y]), -.05)                                                   # 오른팔
    if fixed: S.add(cl, lambda d: d.ellipse([14, 38 + y, 23, 52 + y]), -.05)                                         # 왼팔
    else: S.add(cl, lambda d: d.ellipse([15, 38 + y, 23, 47 + y]), -.05)                                             # 찢어져 짧은 왼팔
    if not fixed: S.add('stuff', lambda d: [d.ellipse([14, 45 + y, 20, 50 + y]), d.ellipse([18, 47 + y, 22, 51 + y])], .15)   # 삐져나온 솜
    S.add(cl, lambda d: [d.ellipse([12, 4 + y, 21, 13 + y]), d.ellipse([43, 4 + y, 52, 13 + y])])                    # 묶은 귀 끝
    S.add(cl, lambda d: d.ellipse([14, 6 + y, 50, 40 + y]))                                                          # 머리
    if not fixed: S.add('patch', lambda d: d.ellipse([36, 9 + y, 46, 18 + y]), .05)                                  # 머리에 덧댄 헝겊
    else: S.add('pink', lambda d: [d.polygon([(32, 8 + y), (22, 2 + y), (22, 13 + y)]), d.polygon([(32, 8 + y), (42, 2 + y), (42, 13 + y)]), d.ellipse([29, 5 + y, 35, 11 + y])], .05)   # 리본
    a = S.render()
    R = RAMP[cl]; seam = R[1]
    # 귀 끝을 묶은 실
    px(a, [(19, 13 + y), (20, 12 + y), (44, 12 + y), (45, 13 + y)], seam)
    if not fixed:
        st = '#2E2228'
        for (x, yy) in ((24, 46), (31, 46), (24, 53), (31, 53), (27, 46), (28, 53), (24, 49), (31, 50)): px(a, [(x, yy + y)], st)   # 덧댄 헝겊 바늘땀
        for (x, yy) in ((37, 9), (41, 8), (45, 11), (46, 15), (36, 14)): px(a, [(x, yy + y)], st)
        for k in range(5): px(a, [(22 + k, 20 + k + y)], st if k % 2 == 0 else seam)                                  # 이마 바늘땀
        for (x, yy) in ((21, 21), (23, 19), (25, 23), (27, 21)): px(a, [(x, yy + y)], st)
        for k in range(4): px(a, [(37 + k, 40 + k + y), (38 + k, 39 + k + y)], st if k % 2 == 0 else seam)           # 몸 바늘땀
        px(a, [(22, 44 + y), (21, 46 + y), (23, 46 + y)], st)                                                         # 찢어진 팔 끝
    else:
        px(a, [(27, 47 + y), (31, 49 + y), (35, 47 + y)], '#9A4A62')                                                  # 하트 바늘땀
        px(a, [(31, 7 + y), (32, 7 + y)], '#FFE4EA')
    # 얼굴
    ex1, ex2, ey = 24, 37, 22 + y
    def button(x, yy, glow=False):   # 단추 눈 4×4 · 구멍 둘
        c0, c1 = ('#C88A10', '#FFE070') if glow else ('#1A1020', '#3E3250')
        px(a, [(x + i, yy + j) for i in range(5) for j in range(5) if (i - 2) ** 2 + (j - 2) ** 2 <= 5], c0)
        px(a, [(x + 1, yy + 2), (x + 3, yy + 2)], c1)
        if glow: px(a, [(x + 1, yy + 1)], '#FFFBE0')
        else: px(a, [(x + 1, yy + 1), (x + 1, yy)], '#FFFFFF')
    def xmark(x, yy):
        for k in range(5): px(a, [(x + k, yy + k), (x + 4 - k, yy + k)], '#2E2228')
    if face == 'closed':
        px(a, [(ex1, ey + 2), (ex1 + 1, ey + 3), (ex1 + 2, ey + 3), (ex1 + 3, ey + 2), (ex2, ey + 2), (ex2 + 1, ey + 3), (ex2 + 2, ey + 3), (ex2 + 3, ey + 2)], '#2A1A20')
    elif face == 'shy':
        px(a, [(ex1, ey + 3), (ex1 + 1, ey + 2), (ex1 + 2, ey + 2), (ex1 + 3, ey + 3), (ex2, ey + 3), (ex2 + 1, ey + 2), (ex2 + 2, ey + 2), (ex2 + 3, ey + 3)], '#2A1A20')
    elif fixed: button(ex1, ey); button(ex2, ey)
    else: xmark(ex1, ey); button(ex2, ey, glow=face == 'glow')
    if face == 'sad': px(a, [(ex2 + 1, ey + 4), (ex2 + 1, ey + 5), (ex2 + 2, ey + 6)], '#9ACAEE')                     # 눈물
    if fixed:
        px(a, [(20, 29 + y), (21, 29 + y), (22, 29 + y), (41, 29 + y), (42, 29 + y), (43, 29 + y)], '#F8A0B4')     # 분홍 볼
        if face == 'shy': px(a, [(20, 30 + y), (21, 30 + y), (42, 30 + y), (43, 30 + y)], '#F08AA0')
        if face == 'smile': px(a, [(29, 30 + y), (30, 31 + y), (31, 31 + y), (32, 31 + y), (33, 31 + y), (34, 30 + y), (31, 32 + y), (32, 32 + y)], '#7A3040')
        else: px(a, [(30, 30 + y), (31, 31 + y), (32, 31 + y), (33, 30 + y)], '#7A3040')
    elif face == 'surprise':
        px(a, [(31, 30 + y), (32, 30 + y), (30, 31 + y), (33, 31 + y), (31, 32 + y), (32, 32 + y)], '#2A1A20')
    else:                                                                                                            # 꿰맨 입
        px(a, [(x, 31 + y) for x in range(28, 36)], '#2E2228')
        px(a, [(x, 30 + y) for x in (28, 30, 32, 34)] + [(x, 32 + y) for x in (29, 31, 33, 35)], '#2E2228')
    return a
FR = [(False, 'idle', 0), (False, 'glow', -1), (False, 'sad', 1), (False, 'surprise', -1), (True, 'idle', 0), (True, 'smile', -1), (True, 'closed', 0), (True, 'shy', 0)]
if __name__ == '__main__':
    sh = np.zeros((64, 64 * len(FR), 4), np.uint8)
    for i, (fx, fc, b) in enumerate(FR): sh[:, i * 64:(i + 1) * 64] = nubi(fx, fc, b)
    Image.fromarray(sh).save(os.path.join(ROOT, 'public', 'art', 'nubi.png'))
    # 미리보기: 나비 · 아울라 · 맨디 옆에 누비 8 장
    ref = [cat(), owl(), mandrake()]
    row = np.zeros((64, 64 * (len(ref) + len(FR)), 4), np.uint8)
    for i, r in enumerate(ref): row[:, i * 64:(i + 1) * 64] = r
    row[:, len(ref) * 64:] = sh
    bg = Image.new('RGBA', (row.shape[1], 64), (250, 241, 226, 255)); bg.alpha_composite(Image.fromarray(row))
    os.makedirs(os.path.join(ROOT, 'tools', 'nubi_mock'), exist_ok=True)
    bg.resize((bg.width * 4, 256), Image.NEAREST).save(os.path.join(ROOT, 'tools', 'nubi_mock', 'nubi_prev.png'))
    print('ok')
