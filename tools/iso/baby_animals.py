# 「길 잃은 아기 동물」 12마리 (16x16 도트) → out/babies.png (192x16, 칸 i = x 16*i)
#   모두 같은 아기 몸틀(큰 둥근 머리 + 작은 몸 + 짧은 발)에 귀·꼬리·무늬만 달라요 → 머리와 몸 비율이 일정해요
#   python3 baby_animals.py [--preview DIR]   # DIR/babies_prev.png (8배 확대 + 이름)
import os, sys
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = 16
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
OL = H('#1a1024'); EYE = H('#1a1024'); HI = H('#ffffff'); BLUSH = H('#ff9ab8')
NAMES = ['아기 오리', '아기 고양이', '아기 강아지', '아기 토끼', '아기 다람쥐', '아기 고슴도치', '아기 박쥐', '아기 부엉이', '아기 여우', '아기 너구리', '아기 개구리', '아기 병아리']


def ell(cx, cy, rx, ry):
    return {(x, y) for x in range(S) for y in range(S) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}


def px(*pts): return set(pts)


def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


HEAD = ell(8, 6.6, 5.4, 4.7)      # 머리: 몸보다 커요 (아기 비율)
BODY = ell(8, 12.2, 3.9, 2.9)
FEET = rect(5, 14, 6, 14) | rect(9, 14, 10, 14)


class Baby:
    def __init__(s):
        s.layers = []; s.top = {}
    def add(s, mask, col): s.layers.append((set(mask), col)); return s
    def dot(s, pts, col):
        for p in pts: s.top[p] = col
        return s
    def face(s, y=7, gap=4, blush=True, mouth='w', x0=None):
        a = x0 if x0 is not None else 8 - gap // 2 - 1; b = a + gap + 1
        for x in (a, b): s.dot([(x, y), (x, y + 1)], EYE); s.dot([(x, y)], HI)
        if blush: s.dot([(a - 1, y + 2), (b + 1, y + 2)], BLUSH)
        if mouth == 'w': s.dot([((a + b) // 2, y + 2)], EYE)
        return s
    def render(s):
        im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); P = im.load(); body = set()
        for m, c in s.layers:
            for q in m:
                if 0 <= q[0] < S and 0 <= q[1] < S: P[q] = c; body.add(q)
        for x in range(S):
            for y in range(S):
                if (x, y) in body: continue
                if any((x + dx, y + dy) in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): P[x, y] = OL
        for q, c in s.top.items(): P[q] = c
        return im


def base(c, belly=None, feet=None, b=None):
    b = b or Baby(); b.add(BODY, c)
    if belly: b.add(ell(8, 12.6, 2.2, 1.8), belly)
    b.add(FEET, feet or shade(c)); b.add(HEAD, c); return b


def shade(c, k=.78): return tuple(int(v * k) for v in c[:3]) + (255,)


B = []
# 1 아기 오리: 노란 솜털 · 넓적한 주황 부리 · 꽁지 깃털
Y = H('#ffe04a'); b = Baby(); b.add(px((13, 11), (13, 10), (12, 10)), shade(Y)); base(Y, H('#fff4a8'), H('#ff8a2a'), b)
b.add(px((8, 1), (9, 1), (8, 2)), Y).face(y=6).dot([(7, 9), (8, 9), (9, 9), (7, 10), (8, 10), (9, 10)], H('#ff8a2a')).dot([(8, 10)], H('#d86a18'))
b.top.pop((8, 8), None); B.append(b)
# 2 아기 고양이: 까만 털 · 뾰족 귀(분홍 속) · 하얀 발 · 동그랗게 만 꼬리
K = H('#4a3e62'); b = Baby(); b.add(px((12, 12), (13, 12), (13, 11), (13, 10), (12, 9)), K); base(K, H('#6e6088'), H('#f6f0ff'), b)
b.add(px((3, 1), (3, 2), (4, 2), (3, 3), (4, 3), (5, 3)), K).add(px((12, 1), (12, 2), (11, 2), (12, 3), (11, 3), (10, 3)), K)
b.dot([(4, 3), (11, 3)], H('#ff9ab8')).face(y=6).dot([(7, 9), (8, 9)], H('#ff9ab8')); b.top.pop((7, 8), None); B.append(b)
# 3 아기 강아지: 갈색 · 축 처진 귀 · 하얀 주둥이 · 살랑 꼬리
D = H('#d8a068'); b = Baby(); b.add(px((13, 11), (13, 10), (14, 9)), D); base(D, H('#f4dcb8'), H('#a8743c'), b)
EAR = H('#8a5a30'); b.add(rect(2, 4, 3, 9) - {(2, 9)}, EAR).add(rect(12, 4, 13, 9) - {(13, 9)}, EAR)
b.add(ell(8, 9.3, 2.4, 1.6), H('#fff4e4')).face(y=6, mouth='').dot([(7, 8), (8, 8)], EYE).dot([(7, 10), (8, 10)], H('#ff7a9a')); B.append(b)
# 4 아기 토끼: 하얀 털 · 긴 귀(한쪽 접힘) · 솜뭉치 꼬리
Wt = H('#f6f0ff'); b = Baby(); b.add(ell(13, 12, 1.6, 1.4), Wt); base(Wt, None, H('#d8d0ec'), b)
b.add(rect(5, 0, 6, 3), Wt).add(px((9, 2), (10, 2), (11, 2), (12, 2), (12, 3), (9, 3), (10, 3)), Wt).dot([(5, 1), (5, 2), (10, 2), (11, 2)], H('#ffb0cc'))
b.face(y=7); B.append(b)
# 5 아기 다람쥐: 주황 · 크게 말린 줄무늬 꼬리 · 도토리를 안음
R = H('#e08a42'); b = Baby(); TL = H('#f6d098')
b.add(ell(13.2, 9.5, 2.3, 4.8), R).add(ell(13.4, 9.2, 1, 3.2), TL); base(R, H('#f6d098'), H('#a85e28'), b)
b.add(px((4, 2), (4, 3), (5, 3)), R).add(px((11, 2), (11, 3), (10, 3)), R).face(y=6)
b.dot([(7, 12), (8, 12), (7, 13), (8, 13)], H('#a8743c')).dot([(7, 11), (8, 11)], H('#6e4824')); B.append(b)
# 6 아기 고슴도치: 뾰족뾰족 등 · 동그란 얼굴 · 등에 낙엽 하나
SP = H('#7a5a48'); F = H('#f6dcc0'); b = Baby()
b.add(ell(8, 6.4, 6.2, 5.4) | ell(8, 11.5, 5, 3.5), SP); b.add(ell(7.4, 8.3, 3.6, 3.2), F); b.add(FEET, H('#c8a888'))
b.add(px((1, 4), (0, 6), (1, 9), (15, 6), (14, 3), (15, 9), (3, 1), (12, 1), (8, 0)), SP)
b.face(y=7, gap=3, x0=5).dot([(7, 10)], EYE).dot([(11, 2), (12, 2), (12, 3)], H('#ff8a2a')); B.append(b)
# 7 아기 박쥐: 보라 · 펼친 작은 날개 · 뾰족 귀 · 송곳니
V = H('#8a6ec0'); WG = H('#5a4488'); b = Baby()
b.add(px((1, 9), (2, 8), (2, 9), (2, 10), (3, 9), (3, 10), (3, 11), (1, 11), (2, 11)), WG).add(px((14, 9), (13, 8), (13, 9), (13, 10), (12, 9), (12, 10), (12, 11), (14, 11), (13, 11)), WG)
base(V, H('#b8a0e0'), H('#5a4488'), b); b.add(px((3, 1), (3, 2), (4, 2)), V).add(px((12, 1), (12, 2), (11, 2)), V)
b.face(y=6).dot([(7, 9), (9, 9)], HI); b.top.pop((8, 8), None); B.append(b)
# 8 아기 부엉이: 솜뭉치 · 귀깃 · 동그란 큰 눈 · 작은 부리
O = H('#c0a888'); b = base(O, H('#f2e6cc'), H('#ffb04a'))
b.add(px((3, 1), (3, 2), (12, 1), (12, 2)), O)
for cx in (5.5, 10.5): b.add(ell(cx, 6.8, 2.2, 2.2), H('#fff8ec'))
b.dot([(5, 6), (5, 7), (10, 6), (10, 7)], EYE).dot([(5, 6), (10, 6)], HI).dot([(8, 8), (7, 8), (8, 9)], H('#ffb04a')).dot([(3, 9), (12, 9)], BLUSH); B.append(b)
# 9 아기 여우: 주황 · 큰 뾰족 귀 · 하얀 볼 · 꼬리 끝 하양
X = H('#ff9a3c'); b = Baby(); b.add(ell(13, 11.5, 2, 2.6), X).add(px((13, 13), (14, 13), (14, 12)), H('#fff4e4')); base(X, H('#fff4e4'), H('#5a3424'), b)
b.add(px((3, 0), (3, 1), (4, 1), (3, 2), (4, 2), (5, 2), (3, 3), (4, 3)), X).add(px((12, 0), (12, 1), (11, 1), (12, 2), (11, 2), (10, 2), (12, 3), (11, 3)), X)
b.dot([(4, 2), (11, 2)], H('#5a3424')).add(ell(8, 9.4, 3.2, 1.7), H('#fff4e4')).face(y=6, mouth='').dot([(7, 9), (8, 9)], EYE); B.append(b)
# 10 아기 너구리: 회색 · 눈가 까만 가면 · 줄무늬 꼬리
G = H('#a8a0b8'); b = Baby(); b.add(ell(13, 11, 1.8, 2.8), G).add(px((12, 10), (13, 10), (14, 10), (12, 12), (13, 12), (14, 12)), H('#4a4458')); base(G, H('#e4e0ec'), H('#4a4458'), b)
b.add(ell(4, 2.6, 1.4, 1.4) | ell(12, 2.6, 1.4, 1.4), G).add(rect(3, 6, 12, 8) - {(3, 8), (12, 8), (7, 8), (8, 8)}, H('#3a3448'))
b.add(ell(8, 9.6, 2.2, 1.3), H('#f6f2fa')).face(y=6, blush=True, mouth='').dot([(7, 9), (8, 9)], EYE); B.append(b)
# 11 아기 개구리: 연두 · 머리 위로 튀어나온 눈 · 빨간 볼 · 활짝 웃음
Gn = H('#86d66e'); b = Baby(); b.add(ell(8, 12, 4.4, 3), Gn).add(ell(8, 12.8, 2.6, 1.8), H('#d4f4b0')).add(FEET, H('#5aa84a'))
b.add(ell(8, 7.4, 5.6, 3.8), Gn).add(ell(4.6, 3.6, 2, 2) | ell(11.4, 3.6, 2, 2), Gn)
b.dot([(4, 3), (4, 4), (11, 3), (11, 4)], EYE).dot([(4, 3), (11, 3)], HI).dot([(3, 8), (12, 8)], H('#ff7a8a')).dot([(5, 8), (6, 9), (7, 9), (8, 9), (9, 9), (10, 8)], EYE); B.append(b)
# 12 아기 병아리: 머리·몸이 하나인 노란 공 · 머리 깃털 · 짧은 부리
Yc = H('#fff07a'); b = Baby(); b.add(ell(8, 9.4, 5.8, 5.4), Yc).add(ell(8, 11.6, 3.4, 2.4), H('#fff8c0')).add(FEET - rect(5, 14, 5, 14) - rect(10, 14, 10, 14) | px((6, 15), (9, 15)), H('#ff8a2a'))
b.add(px((7, 2), (8, 2), (8, 3), (9, 1)), Yc).face(y=8).dot([(7, 10), (8, 10), (7, 11)], H('#ff8a2a')); b.top.pop((7, 10), None); b.dot([(7, 10), (8, 10)], H('#ff8a2a')); B.append(b)


def build():
    sheet = Image.new('RGBA', (S * len(B), S), (0, 0, 0, 0))
    for i, b in enumerate(B): sheet.paste(b.render(), (i * S, 0))
    return sheet


def preview(sheet, outdir):
    os.makedirs(outdir, exist_ok=True); Z, per, pad, lh = 8, 6, 10, 26
    cell = S * Z; rows = (len(B) + per - 1) // per
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), (0x21, 0x17, 0x33, 255)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 16)
    for i in range(len(B)):
        x0, y0 = pad + (i % per) * (cell + pad), pad + (i // per) * (cell + lh + pad)
        img.alpha_composite(sheet.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST), (x0, y0))
        d.text((x0 + 4, y0 + cell + 2), NAMES[i], fill=(230, 220, 250, 255), font=font)
    img.save(os.path.join(outdir, 'babies_prev.png'))


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    sh = build(); sh.save('out/babies.png'); print('saved', sh.size)
    if '--preview' in sys.argv: preview(sh, sys.argv[sys.argv.index('--preview') + 1])
