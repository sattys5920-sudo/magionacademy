# 아기 용 3종(불·물·숲)을 도트로 그려요 → public/art/dragons.png  (32칸 × 4동작 × 3종: 가만히 · 가만히2(날개) · 폴짝 · 신남)
#   python3 dragons.py [미리보기.png]
import sys, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', '..', 'public', 'art', 'dragons.png')
N = 32
PAL = {   # 불 · 물 · 숲: 밝은 빛·빛·바탕·그림자·테두리·배·날개·뿔
 'fire':   dict(hi=(255, 178, 138), li=(255, 128, 92), ba=(236, 88, 64), da=(178, 54, 56), ol=(88, 26, 42), be=(255, 218, 150), be2=(244, 178, 112), wi=(255, 156, 66), wd=(210, 98, 48), ho=(255, 238, 176), bl=(255, 150, 140)),
 'water':  dict(hi=(176, 230, 255), li=(116, 192, 255), ba=(72, 152, 232), da=(44, 102, 184), ol=(20, 46, 98), be=(220, 246, 255), be2=(170, 214, 244), wi=(124, 214, 255), wd=(74, 164, 226), ho=(240, 252, 255), bl=(255, 170, 190)),
 'forest': dict(hi=(188, 242, 144), li=(132, 216, 104), ba=(86, 178, 86), da=(52, 128, 72), ol=(22, 64, 42), be=(238, 234, 164), be2=(206, 200, 120), wi=(158, 224, 112), wd=(104, 174, 82), ho=(248, 238, 190), bl=(255, 170, 150)),
}
def ell(cx, cy, rx, ry):
    return {(x, y) for y in range(N) for x in range(N) if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1}
def poly(pts):   # 아주 단순한 채움 (볼록 다각형)
    def inside(x, y):
        s = None
        for i in range(len(pts)):
            ax, ay = pts[i]; bx, by = pts[(i + 1) % len(pts)]
            c = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
            if c != 0:
                if s is None: s = c > 0
                elif s != (c > 0): return False
        return True
    return {(x, y) for y in range(N) for x in range(N) if inside(x + .5, y + .5)}
def shade(mask, c, pal, light=(-.55, -.8)):
    xs = [p[0] for p in mask]; ys = [p[1] for p in mask]; cx = (min(xs) + max(xs)) / 2; cy = (min(ys) + max(ys)) / 2; rx = max(1, (max(xs) - min(xs)) / 2); ry = max(1, (max(ys) - min(ys)) / 2)
    out = {}
    for (x, y) in mask:
        u = (x - cx) / rx; v = (y - cy) / ry; l = -(u * -light[0] * -1 + 0) if False else -(u * .55 + v * .8)
        out[(x, y)] = pal['hi'] if l > .62 else pal['li'] if l > .2 else pal['ba'] if l > -.45 else pal['da']
    return out
def frame(sp, pose):
    pal = PAL[sp]; px = {}
    dy = pose.get('dy', 0); wing = pose.get('wing', 0); mouth = pose.get('mouth', 0); blink = pose.get('blink', 0)
    def put(layer, shift=(0, 0)):
        for (x, y), c in layer.items(): px[(x + shift[0], y + shift[1] + dy)] = c
    # 꼬리 (뒤쪽 오른쪽으로 말려요)
    tail = {}
    for i, (x, y) in enumerate([(22, 25), (24, 25), (26, 24), (27, 22), (27, 20), (26, 19)]):
        for (a, b) in [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)] if i < 3 else [(x, y), (x + 1, y)]: tail[(a, b)] = pal['ba'] if (a + b) % 5 else pal['da']
    tail[(26, 18)] = pal['wi']; tail[(27, 18)] = pal['wi']; tail[(26, 17)] = pal['ho']
    put(tail)
    # 날개 (작은 박쥐 날개, 몸 뒤)
    for sgn, cx in ((-1, 8), (1, 24)):
        up = -3 if wing else 0
        w = poly([(cx, 18), (cx + sgn * 5, 13 + up), (cx + sgn * 6, 18 + up), (cx + sgn * 3, 21), (cx + sgn * 1, 21)])
        lay = {p: pal['wi'] for p in w}
        for (x, y) in list(w):   # 날개 막 줄무늬
            if (x - cx) * sgn >= 3 and (y + x) % 4 == 0: lay[(x, y)] = pal['wd']
        put(lay)
    # 몸통 · 배
    body = ell(16, 22, 8, 7); put(shade(body, 0, pal))
    belly = ell(16, 24, 5, 5); put({p: (pal['be'] if p[1] < 26 else pal['be2']) for p in belly if p in body})
    for yy in (22, 24, 26):   # 배 줄무늬
        for xx in range(13, 20):
            if (xx, yy) in belly and (xx + yy) % 2 == 0: px[(xx, yy + dy)] = pal['be2']
    # 발
    ft = pose.get('feet', 0)
    for fx in (11, 19): put({p: pal['da'] for p in ell(fx + 1, 29 - ft, 3, 2)}); put({p: pal['ba'] for p in ell(fx + 1, 28 - ft, 3, 1.6)})
    # 머리
    head = ell(16, 13, 8, 7); put(shade(head, 0, pal))
    # 귀 지느러미 · 뿔
    for sgn in (-1, 1):
        put({p: pal['wi'] for p in poly([(16 + sgn * 8, 11), (16 + sgn * 12, 8), (16 + sgn * 11, 13), (16 + sgn * 8, 15)])})
        put({p: pal['ho'] for p in poly([(16 + sgn * 4, 7), (16 + sgn * 5, 2), (16 + sgn * 6.5, 7)])})
    # 머리 위 작은 볏
    for xx in (15, 16, 17): px[(xx, 6 + dy)] = pal['li']
    # 얼굴: 큰 눈 · 볼 · 콧구멍 · 입
    for ex in (10, 19):
        if blink:
            for k in range(3): px[(ex + k, 14 + dy)] = pal['ol']
        else:
            for yy in range(11, 16):
                for xx in range(ex, ex + 3): px[(xx, yy + dy)] = pal['ol']
            px[(ex, 12 + dy)] = (255, 255, 255); px[(ex + 1, 12 + dy)] = (255, 255, 255); px[(ex, 13 + dy)] = (255, 255, 255)
            px[(ex + 2, 15 + dy)] = (180, 190, 230)
    for bx in (8, 22):
        for k in range(2): px[(bx + k, 16 + dy)] = pal['bl']
    px[(15, 16 + dy)] = pal['ol']; px[(17, 16 + dy)] = pal['ol']
    if mouth:
        for xx in range(14, 19): px[(xx, 18 + dy)] = pal['ol']
        for xx in (15, 16, 17): px[(xx, 19 + dy)] = (236, 90, 110)
    else:
        for xx in (15, 16, 17): px[(xx, 18 + dy)] = pal['ol']
    # 테두리 (겉모양 한 칸 바깥)
    keys = set(px)
    for (x, y) in keys:
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + ax, y + ay)
            if q not in px and 0 <= q[0] < N and 0 <= q[1] < N: px[q] = ('ol',)
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for (x, y), c in px.items():
        if 0 <= x < N and 0 <= y < N: im.putpixel((x, y), (*pal['ol'], 255) if c == ('ol',) else (*c, 255))
    return im
POSES = [dict(), dict(dy=1, wing=1, blink=1), dict(dy=-3, feet=2, wing=1), dict(dy=0, wing=1, mouth=1)]
sheet = Image.new('RGBA', (N * 4, N * 3), (0, 0, 0, 0))
for r, sp in enumerate(PAL):
    for c, po in enumerate(POSES): sheet.alpha_composite(frame(sp, po), (c * N, r * N))
sheet.save(OUT)
if len(sys.argv) > 1:
    pv = Image.new('RGBA', (N * 4 * 5, N * 3 * 5), (96, 140, 92, 255)); pv.alpha_composite(sheet.resize((N * 4 * 5, N * 3 * 5), Image.NEAREST)); pv.save(sys.argv[1])
print('ok', OUT)
