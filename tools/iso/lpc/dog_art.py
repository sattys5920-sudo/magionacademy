# 시안: 떠돌이 강아지 「뭉치」 — beasts.py(나비 · 배트리 …)와 같은 그림 방식 (64×64 칸, 부위마다 6단계 색, 외곽선)
#   누렁이 털 · 축 처진 귀 (한쪽만 뒤집혀 있어요) · 혀를 내민 멍한 얼굴 · 해진 빨간 목도리 · 털에 묻은 얼룩 · 흔드는 꼬리
#   python3 dog_art.py <미리보기.png>  → 앉기 · 꼬리 흔들기 · 고개 갸웃 · 걷기 2 칸 (앞모습)
import sys
import numpy as np
from PIL import Image
from beasts import Sprite, px, eye

def dog(tail=0, tilt=0, step=0):
    S = Sprite(); t = tail; dy = 1 if step else 0
    S.add('root', lambda d: [d.ellipse([42 + t, 40 - abs(t), 52 + t, 50 - abs(t)]), d.ellipse([46 + t, 34 - abs(t), 53 + t, 42 - abs(t)])], .05)   # 꼬리 (흔들면 좌우로)
    S.add('root', lambda d: [d.ellipse([19, 36 + dy, 45, 63]), d.rectangle([22, 52, 42, 63])])                                                   # 몸
    S.add('belly', lambda d: d.ellipse([25, 42 + dy, 39, 62]), .05)                                                                           # 배
    S.add('root', lambda d: [d.ellipse([22 - step, 53, 30 - step, 63]), d.ellipse([34 + step, 53, 42 + step, 63])], .1)                         # 앞발
    hx0 = 17 + tilt
    S.add('root', lambda d: [d.ellipse([hx0, 12, hx0 + 30, 40])])                                                                             # 머리
    S.add('belly', lambda d: d.ellipse([hx0 + 8, 26, hx0 + 22, 39]), .08)                                                                     # 주둥이
    S.add('brown', lambda d: [d.polygon([(hx0 + 2, 16), (hx0 - 3, 32), (hx0 + 3, 34), (hx0 + 9, 18)])], -.05)                                 # 왼귀 (축 처짐)
    S.add('brown', lambda d: [d.polygon([(hx0 + 21, 16), (hx0 + 31, 8), (hx0 + 33, 14), (hx0 + 27, 20)])], -.05)                               # 오른귀 (뒤집혀 위로)
    S.add('brown', lambda d: d.ellipse([hx0 + 18, 14, hx0 + 27, 23]), -.1)                                                                    # 눈가 얼룩
    S.add('red', lambda d: [d.polygon([(21, 38), (43, 38), (42, 42), (22, 42)]), d.polygon([(36, 41), (41, 41), (39, 50), (34, 48)])])        # 해진 목도리
    a = S.render()
    eye(a, hx0 + 8, 22, '#3A2414', 4); eye(a, hx0 + 19, 22, '#3A2414', 4)                                                                     # 동그란 눈
    px(a, [(hx0 + 14, 28), (hx0 + 15, 28), (hx0 + 16, 28), (hx0 + 14, 29), (hx0 + 15, 29), (hx0 + 16, 29)], '#2A1810')                       # 코
    px(a, [(hx0 + 15, 30), (hx0 + 13, 31), (hx0 + 17, 31)], '#5A3428')                                                                        # 입
    px(a, [(hx0 + 15, 32), (hx0 + 16, 32), (hx0 + 15, 33), (hx0 + 16, 33), (hx0 + 16, 34)], '#F07890')                                       # 내민 혀
    px(a, [(hx0 + 5, 29), (hx0 + 6, 29), (hx0 + 24, 29), (hx0 + 25, 29)], '#F4A8BC')                                                          # 볼
    px(a, [(26, 56), (27, 57), (37, 47), (38, 48)], '#8A6A48')                                                                                # 털 얼룩 (떠돌이)
    px(a, [(41, 40), (42, 43), (40, 44)], '#6A1424')                                                                                          # 목도리 해진 자리
    return a

if __name__ == '__main__':
    frames = [dog(), dog(tail=-3), dog(tail=3), dog(tilt=-3), dog(step=1)]
    sh = np.zeros((64, 64 * len(frames), 4), np.uint8)
    for i, f in enumerate(frames): sh[:, i * 64:(i + 1) * 64] = f
    bg = Image.new('RGBA', (sh.shape[1], 64), (40, 30, 56, 255)); bg.alpha_composite(Image.fromarray(sh)); bg.resize((bg.width * 4, 256), Image.NEAREST).save(sys.argv[1])
    Image.fromarray(sh).save(sys.argv[1].replace('.png', '_raw.png'))
