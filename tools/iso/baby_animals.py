# 「길 잃은 아기 동물」 12마리 (12x12 도트) → out/babies.png (168x14, 칸 i = x 14*i, 둘레 1칸은 윤곽선)
#   모두 같은 아기 몸틀(큰 둥근 머리 + 작은 몸 + 짧은 발)에 귀·꼬리·무늬만 달라요 → 머리와 몸 비율이 일정해요
#   python3 baby_animals.py [--preview DIR]   # DIR/babies_prev.png (11배 확대 + 이름)
import os, sys
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = 12
C = S + 2   # 칸 크기 (윤곽선 포함 14x14)
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
OL = H('#1a1024'); EYE = H('#1a1024'); HI = H('#ffffff'); BLUSH = H('#ff9ab8')
NAMES = ['아기 오리', '아기 고양이', '아기 강아지', '아기 토끼', '아기 다람쥐', '아기 고슴도치', '아기 박쥐', '아기 부엉이', '아기 여우', '아기 너구리', '아기 개구리', '아기 병아리']


def ell(cx, cy, rx, ry):
    return {(x, y) for x in range(S) for y in range(S) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}


def px(*pts): return set(pts)


def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


HEAD = ell(6, 4.9, 4.2, 3.7)      # 머리: 몸보다 커요 (아기 비율)
BODY = ell(6, 9.2, 3, 2.2)
FEET = rect(3, 11, 4, 11) | rect(7, 11, 8, 11)


class Baby:
    def __init__(s):
        s.layers = []; s.top = {}
    def add(s, mask, col): s.layers.append((set(mask), col)); return s
    def dot(s, pts, col):
        for p in pts: s.top[p] = col
        return s
    def face(s, y=5, a=4, b=7, blush=True, mouth=True):
        for x in (a, b): s.dot([(x, y), (x, y + 1)], EYE); s.dot([(x, y)], HI)
        if blush: s.dot([(a - 1, y + 2), (b + 1, y + 2)], BLUSH)
        if mouth: s.dot([((a + b) // 2, y + 2)], EYE)
        return s
    def render(s):
        im = Image.new('RGBA', (C, C), (0, 0, 0, 0)); P = im.load(); body = set()   # 그림은 12칸, 둘레 1칸은 윤곽선 자리
        for m, c in s.layers:
            for q in m:
                if 0 <= q[0] < S and 0 <= q[1] < S: P[q[0] + 1, q[1] + 1] = c; body.add((q[0] + 1, q[1] + 1))
        for x in range(C):
            for y in range(C):
                if (x, y) in body: continue
                if any((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): P[x, y] = OL
        for q, c in s.top.items(): P[q[0] + 1, q[1] + 1] = c
        return im


def shade(c, k=.78): return tuple(int(v * k) for v in c[:3]) + (255,)


def base(c, belly=None, feet=None, b=None):
    b = b or Baby(); b.add(BODY, c)
    if belly: b.add(ell(6, 9.6, 1.7, 1.3), belly)
    b.add(FEET, feet or shade(c)); b.add(HEAD, c); return b


B = []
# 1 아기 오리: 하얀 솜털 · 작은 주황 부리 · 꽁지 깃털
Y = H('#f6f0ff'); OR = H('#ff8a2a'); b = Baby(); b.add(px((10, 8), (10, 9)), H('#d8d0ec')); base(Y, H('#ffffff'), OR, b)
b.add(px((6, 0), (6, 1), (7, 0)), Y).face(mouth=False).dot([(5, 7), (6, 7)], OR).dot([(5, 8), (6, 8)], H('#d86a18')); B.append(b)
# 2 아기 고양이: 까만 털 · 뾰족 귀 · 하얀 발 · 말린 꼬리
K = H('#4a3e62'); b = Baby(); b.add(px((10, 10), (11, 9), (11, 8), (10, 7)), K); base(K, H('#6e6088'), H('#f6f0ff'), b)
b.add(px((2, 0), (2, 1), (3, 1)), K).add(px((9, 0), (9, 1), (8, 1)), K).dot([(2, 1), (9, 1)], H('#ff9ab8')).face(mouth=False).dot([(5, 7), (6, 7)], H('#ff9ab8')); B.append(b)
# 3 아기 강아지: 갈색 · 축 처진 귀 · 하얀 주둥이 · 살랑 꼬리
D = H('#d8a068'); b = Baby(); b.add(px((10, 8), (11, 7)), D); base(D, H('#f4dcb8'), H('#a8743c'), b)
EAR = H('#8a5a30'); b.add(rect(1, 3, 1, 6), EAR).add(rect(10, 3, 10, 6), EAR)
b.add(ell(6, 7.4, 1.8, 1.1), H('#fff4e4')).face(mouth=False).dot([(5, 7), (6, 7)], EYE).dot([(5, 8)], H('#ff7a9a')); B.append(b)
# 4 아기 토끼: 하얀 털 · 머리를 낮추고 위로 쫑긋 선 긴 귀(분홍 속) · 분홍 코와 앞니 · 솜뭉치 꼬리
Wt = H('#f6f0ff'); PK = H('#ffb0cc'); b = Baby(); b.add(ell(9.6, 10.3, 1.2, 1.1), Wt).add(ell(6, 10.2, 2.7, 1.4), Wt).add(FEET, H('#d8d0ec')).add(ell(6, 7.2, 3.9, 2.9), Wt)
b.add(rect(3, 0, 4, 4), Wt).add(rect(7, 0, 8, 4), Wt).dot([(4, 1), (4, 2), (4, 3), (7, 1), (7, 2), (7, 3)], PK)
b.face(y=7, mouth=False, blush=False).dot([(5, 9), (6, 9)], PK).dot([(5, 10), (6, 10)], H('#ffffff')).dot([(2, 9), (9, 9)], BLUSH); B.append(b)
# 5 아기 다람쥐: 주황 · 크게 말린 줄무늬 꼬리 · 도토리를 안음
R = H('#e08a42'); b = Baby(); b.add(ell(10.2, 7.3, 1.8, 3.6), R).add(ell(10.4, 7.1, .8, 2.4), H('#f6d098')); base(R, H('#f6d098'), H('#a85e28'), b)
b.add(px((3, 1), (2, 1)), R).add(px((8, 1), (9, 1)), R).face().dot([(5, 9), (6, 9)], H('#a8743c')).dot([(5, 8), (6, 8)], H('#6e4824')); B.append(b)
# 6 아기 고슴도치: 뾰족뾰족 등 · 동그란 얼굴 · 등에 낙엽 하나
SP = H('#7a5a48'); b = Baby(); b.add(ell(6, 5, 4.8, 4.2) | ell(6, 8.8, 3.8, 2.6), SP).add(ell(5.6, 6.4, 2.8, 2.3), H('#f6dcc0')).add(FEET, H('#c8a888'))
b.add(px((0, 3), (0, 6), (11, 3), (11, 6), (2, 0), (9, 0), (6, 0)), SP).face(y=5).dot([(8, 1), (9, 1), (9, 2)], H('#ff8a2a')); B.append(b)
# 7 아기 박쥐: 보라 · 펼친 작은 날개 · 뾰족 귀 · 송곳니
V = H('#8a6ec0'); WG = H('#5a4488'); b = Baby()
b.add(px((0, 7), (1, 6), (1, 7), (1, 8), (2, 7), (2, 8), (0, 9), (1, 9)), WG).add(px((11, 7), (10, 6), (10, 7), (10, 8), (9, 7), (9, 8), (11, 9), (10, 9)), WG)
base(V, H('#b8a0e0'), WG, b); b.add(px((2, 0), (2, 1), (3, 1)), V).add(px((9, 0), (9, 1), (8, 1)), V).face(mouth=False).dot([(5, 7), (6, 7)], HI); B.append(b)
# 8 아기 부엉이: 솜뭉치 · 귀깃 · 동그란 큰 눈 · 작은 부리
O = H('#c0a888'); b = base(O, H('#f2e6cc'), H('#ffb04a')); b.add(px((2, 0), (2, 1), (9, 0), (9, 1)), O)
b.add(ell(4, 5, 1.6, 1.6) | ell(8, 5, 1.6, 1.6), H('#fff8ec')).dot([(3, 4), (3, 5), (8, 4), (8, 5)], EYE).dot([(3, 4), (8, 4)], HI).dot([(5, 6), (6, 6)], H('#ffb04a')).dot([(2, 7), (9, 7)], BLUSH); B.append(b)
# 9 아기 여우: 주황 · 큰 뾰족 귀 · 하얀 볼 · 꼬리 끝 하양
X = H('#ff9a3c'); Wf = H('#fff4e4'); b = Baby(); b.add(ell(10.2, 9, 1.5, 1.8), X).add(px((11, 10), (10, 10)), Wf); base(X, Wf, H('#5a3424'), b)
b.add(px((2, 0), (2, 1), (3, 1), (2, 2), (3, 2)), X).add(px((9, 0), (9, 1), (8, 1), (9, 2), (8, 2)), X).dot([(2, 1), (9, 1)], H('#5a3424'))
b.add(ell(6, 7.3, 2.6, 1.3), Wf).face(mouth=False).dot([(5, 7), (6, 7)], EYE); B.append(b)
# 10 아기 너구리: 회색 · 눈가 까만 가면 · 줄무늬 꼬리
G = H('#a8a0b8'); M = H('#3a3448'); b = Baby(); b.add(ell(10.2, 8.6, 1.4, 2.1), G).add(px((9, 8), (10, 8), (11, 8), (9, 10), (10, 10), (11, 10)), H('#4a4458')); base(G, H('#e4e0ec'), H('#4a4458'), b)
b.add(ell(2.6, 1.8, 1, 1) | ell(9.4, 1.8, 1, 1), G).add(rect(2, 4, 9, 6) - {(2, 6), (9, 6), (5, 6), (6, 6), (5, 4), (6, 4)}, M)
b.add(ell(6, 7.4, 1.6, 1), H('#f6f2fa')).face(mouth=False).dot([(5, 7), (6, 7)], EYE); B.append(b)
# 11 아기 개구리: 연두 · 머리 위로 튀어나온 눈 · 빨간 볼 · 활짝 웃음
Gn = H('#86d66e'); b = Baby(); b.add(ell(6, 9, 3.3, 2.2), Gn).add(ell(6, 9.6, 2, 1.3), H('#d4f4b0')).add(FEET, H('#5aa84a'))
b.add(ell(6, 5.6, 4.3, 2.8), Gn).add(ell(3.4, 2.8, 1.5, 1.5) | ell(8.6, 2.8, 1.5, 1.5), Gn)
b.dot([(3, 2), (3, 3), (8, 2), (8, 3)], EYE).dot([(3, 2), (8, 2)], HI).dot([(2, 6), (9, 6)], H('#ff7a8a')).dot([(4, 6), (5, 7), (6, 7), (7, 6)], EYE); B.append(b)
# 12 아기 병아리: 머리·몸이 하나인 노란 공 · 머리 깃털 · 짧은 부리
Yc = H('#fff07a'); b = Baby(); b.add(ell(6, 7, 4.4, 4.1), Yc).add(ell(6, 8.8, 2.6, 1.7), H('#fff8c0')).add(px((4, 11), (7, 11)), OR)
b.add(px((5, 2), (6, 2), (6, 1), (7, 0)), Yc).face(y=5, mouth=False).dot([(5, 7), (6, 7)], OR); B.append(b)


def build():
    sheet = Image.new('RGBA', (C * len(B), C), (0, 0, 0, 0))
    for i, b in enumerate(B): sheet.paste(b.render(), (i * C, 0))
    return sheet


def preview(sheet, outdir):
    os.makedirs(outdir, exist_ok=True); Z, per, pad, lh = 11, 6, 10, 26
    cell = C * Z; rows = (len(B) + per - 1) // per
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), (0x21, 0x17, 0x33, 255)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 16)
    for i in range(len(B)):
        x0, y0 = pad + (i % per) * (cell + pad), pad + (i // per) * (cell + lh + pad)
        img.alpha_composite(sheet.crop((i * C, 0, i * C + C, C)).resize((cell, cell), Image.NEAREST), (x0, y0))
        d.text((x0 + 4, y0 + cell + 2), NAMES[i], fill=(230, 220, 250, 255), font=font)
    img.save(os.path.join(outdir, 'babies_prev.png'))


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    sh = build(); sh.save('out/babies.png'); print('saved', sh.size)
    if '--preview' in sys.argv: preview(sh, sys.argv[sys.argv.index('--preview') + 1])
