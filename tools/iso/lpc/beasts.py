# 동물 NPC 그림 (64×64, 캐릭터와 같은 픽셀 크기 · 세계에선 절반 크기로 그려요)
# LPC 느낌: 부위마다 6단계 색, 왼쪽 위 빛으로 둥글게 음영, 검정 대신 그 부위의 가장 어두운 색으로 외곽선
#   0 나비(고양이) 1 배트리(박쥐 우체부) 2 캇파(갓파) 3 아울라(부엉이 사서) 4 맨디(맨드레이크)
import numpy as np
from PIL import Image, ImageDraw
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
RAMP = {   # 어두운 → 밝은 (0번은 외곽선)
 'cream': ['#4A3428', '#7A604A', '#B49478', '#D8C0A0', '#F0E2CA', '#FFF8EA'],
 'orange': ['#4A1E12', '#80381A', '#B85E2A', '#DC8840', '#F2AE68', '#FFD49A'],
 'pink': ['#5A2A3A', '#9A4A62', '#D07A92', '#EAA0B2', '#F8C4D0', '#FFE4EA'],
 'gold': ['#4A3008', '#8A6010', '#C89420', '#E8B838', '#F8D860', '#FFF09A'],
 'red': ['#3A0A14', '#6A1424', '#A02234', '#C83848', '#E05A62', '#F08A8A'],
 'purple': ['#1A1028', '#33244E', '#4E3A72', '#6A5294', '#8A72B4', '#B09ED4'],
 'membrane': ['#140C20', '#281A3C', '#3C2A54', '#54406E', '#6E5888', '#8C78A4'],
 'leather': ['#2A1A0E', '#4E3220', '#76503A', '#9A7052', '#BC9070', '#DAB494'],
 'paper': ['#5A5048', '#8A8070', '#B8AE9C', '#DAD2C0', '#F0EAD8', '#FFFFF6'],
 'green': ['#0E2A16', '#22502C', '#3A7A3E', '#58A050', '#80C06A', '#B0E094'],
 'shell': ['#2A1A0A', '#4E3218', '#7A5228', '#A07038', '#C49450', '#E2BA78'],
 'water': ['#1A3A5A', '#2A5A8A', '#4A82B8', '#72A8D8', '#9ACAEE', '#D0EEFF'],
 'yellow': ['#4A3410', '#8A6420', '#C49030', '#E8B848', '#F8D870', '#FFF0A8'],
 'brown': ['#24160C', '#4A301C', '#704A2C', '#946640', '#B8885A', '#D8AE80'],
 'belly': ['#4A3A2A', '#7A684E', '#AA9874', '#CEBE98', '#E8DCBE', '#FAF4E2'],
 'root': ['#3A2414', '#664424', '#966C40', '#BC9462', '#DCBC8A', '#F4DEB4'],
 'leaf': ['#0C2A12', '#1E4E22', '#347A34', '#4EA048', '#76C462', '#A8E28C'],
 'denim': ['#141E3A', '#24365E', '#385084', '#5070A8', '#7092C8', '#9CBAE2'],
 'dark': ['#0A0610', '#1C1426', '#2C2238', '#3E3250', '#544668', '#6E6084'],
 'white': ['#5A5A6A', '#8A8A9A', '#B8B8C8', '#D8D8E4', '#EEEEF6', '#FFFFFF'],
}
class _Fill:   # 모양은 모두 채워서 그려요
    def __init__(s, d): s.d = d
    def ellipse(s, b): s.d.ellipse(b, fill=255)
    def rectangle(s, b): s.d.rectangle(b, fill=255)
    def polygon(s, p): s.d.polygon(p, fill=255)
    def line(s, p, width=1): s.d.line(p, fill=255, width=width)
class Sprite:
    def __init__(s): s.parts = []
    def add(s, ramp, draw, light=0.0):   # draw(d): ImageDraw에 흰색으로 모양을 그려요
        m = Image.new('L', (64, 64), 0); draw(_Fill(ImageDraw.Draw(m))); s.parts.append((ramp, np.array(m) > 0, light)); return s
    def render(s):
        col = np.zeros((64, 64, 4), np.uint8); owner = -np.ones((64, 64), int); dark = {}
        for pi, (ramp, m, lb) in enumerate(s.parts):
            R = [hx(c) for c in RAMP[ramp]]
            # 테두리까지 거리 (최대 6)
            dist = np.zeros((64, 64), int); cur = m.copy()
            for k in range(1, 7):
                er = cur.copy()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)): er &= np.roll(np.roll(cur, dy, 0), dx, 1)
                dist[cur & ~er] = k - 1; cur = er
                if not cur.any(): break
            dist[cur] = 6
            ys, xs = np.nonzero(m)
            if not len(ys): continue
            cy, cx = ys.mean(), xs.mean(); r = max(3.0, np.sqrt(len(ys) / np.pi))
            for y, x in zip(ys, xs):
                o = ((x - cx) / r, (y - cy) / r)                       # 빛: 왼쪽 위
                v = .5 + .22 * min(1, dist[y, x] / max(1.5, r * .45)) - .32 * (o[0] * .6 + o[1] * .8) + lb
                i = 1 + int(round(max(0, min(1, v)) * 4))
                if dist[y, x] == 0: i = max(1, i - 1)                 # 가장자리는 한 단계 어둡게
                col[y, x, :3] = R[i]; col[y, x, 3] = 255; owner[y, x] = pi
            dark[pi] = R[0]
        out = col.copy()   # 외곽선: 바깥쪽은 맞닿은 부위의 가장 어두운 색
        for y in range(64):
            for x in range(64):
                if col[y, x, 3]: continue
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < 64 and 0 <= xx < 64 and col[yy, xx, 3]: out[y, x, :3] = dark[owner[yy, xx]]; out[y, x, 3] = 255; break
        # 부위끼리 겹친 경계: 위에 그린 부위 테두리를 그 부위의 2번 색으로 (선이 살짝 보여요)
        for y in range(1, 63):
            for x in range(1, 63):
                o = owner[y, x]
                if o < 0: continue
                if any(owner[y + dy, x + dx] >= 0 and owner[y + dy, x + dx] < o for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))) and (owner[y + 1, x] < o or owner[y, x + 1] < o):
                    out[y, x, :3] = [hx(c) for c in RAMP[s.parts[o][0]]][1]
        return out
def px(a, pts, c):
    for x, y in pts: a[y, x, :3] = hx(c); a[y, x, 3] = 255
def eye(a, x, y, iris='#3A8A4A', h=3):   # 반짝이는 눈 (2칸 폭)
    for yy in range(y, y + h):
        a[yy, x, :3] = hx('#1A1020'); a[yy, x + 1, :3] = hx(iris); a[yy, x, 3] = a[yy, x + 1, 3] = 255
    px(a, [(x, y)], '#FFFFFF')
def cat():   # 나비: 앉아 있는 크림·주황 얼룩 고양이, 빨간 목줄에 금방울
    S = Sprite()
    S.add('orange', lambda d: [d.ellipse([39, 44, 50, 52]), d.rectangle([45, 32, 49, 48]), d.ellipse([43, 28, 50, 35])], .05)   # 꼬리
    S.add('cream', lambda d: [d.ellipse([20, 34, 44, 62]), d.rectangle([23, 50, 41, 62])])                                       # 몸
    S.add('cream', lambda d: [d.ellipse([24, 52, 31, 63]), d.ellipse([33, 52, 40, 63])], .1)                                     # 앞발
    S.add('cream', lambda d: [d.ellipse([18, 14, 46, 38]), d.polygon([(19, 24), (20, 8), (29, 16)]), d.polygon([(45, 24), (44, 8), (35, 16)])])   # 머리·귀
    S.add('orange', lambda d: [d.ellipse([17, 13, 32, 30]), d.polygon([(19, 22), (20, 8), (29, 16)])], .05)                     # 얼룩
    S.add('orange', lambda d: d.ellipse([34, 40, 43, 50]), .0)
    S.add('red', lambda d: d.rectangle([24, 35, 40, 37]))
    S.add('gold', lambda d: d.ellipse([29, 36, 35, 42]), .1)
    a = S.render()
    px(a, [(22, 13), (22, 14), (23, 15), (41, 13), (41, 14), (40, 15)], '#F4A8BC')   # 귀 안쪽
    eye(a, 25, 24, '#5AB85A'); eye(a, 36, 24, '#5AB85A')
    px(a, [(31, 29), (32, 29)], '#E8889C'); px(a, [(30, 31), (33, 31), (31, 32), (32, 32)], '#5A3428')   # 코·입
    px(a, [(22, 29), (23, 29), (40, 29), (41, 29)], '#F4A8BC')                          # 볼
    for x0, x1 in ((15, 22), (42, 49)): px(a, [(x, 28 + (x % 2)) for x in range(x0, x1)], '#D8C8B8')   # 수염
    px(a, [(32, 40)], '#5A3A08')
    return a
def bat():   # 배트리: 날개 편 보라 박쥐, 우편 가방 + 편지
    S = Sprite()
    wing = lambda s: (lambda d: d.polygon([(32, 30), (32 + s * 28, 14), (32 + s * 30, 30), (32 + s * 24, 28), (32 + s * 22, 38), (32 + s * 16, 34), (32 + s * 12, 42)]))
    S.add('membrane', wing(-1), -.05); S.add('membrane', wing(1), -.05)
    S.add('purple', lambda d: [d.ellipse([20, 22, 44, 50]), d.polygon([(22, 28), (21, 10), (30, 22)]), d.polygon([(42, 28), (43, 10), (34, 22)])])
    S.add('pink', lambda d: d.ellipse([26, 34, 38, 48]), .05)
    S.add('purple', lambda d: [d.rectangle([26, 49, 29, 54]), d.rectangle([35, 49, 38, 54])], -.1)
    S.add('leather', lambda d: [d.line([(21, 30), (44, 46)], width=2), d.rectangle([38, 42, 50, 52])])
    S.add('paper', lambda d: d.rectangle([40, 38, 48, 43]), .1)
    a = S.render()
    eye(a, 26, 30, '#E8D040'); eye(a, 36, 30, '#E8D040')
    px(a, [(30, 36), (31, 37), (32, 37), (33, 36)], '#2A1830'); px(a, [(31, 38), (33, 38)], '#FFFFFF')
    px(a, [(41, 39), (44, 41), (47, 39), (42, 40), (46, 40)], '#C8486A')
    px(a, [(24, 34), (25, 34), (39, 34), (40, 34)], '#E8A0C0')
    return a
def kappa():   # 캇파: 초록 갓파, 등딱지, 머리 접시에 물, 노란 부리, 낚싯대
    S = Sprite()
    S.add('brown', lambda d: d.line([(46, 60), (56, 8)], width=2), .1)
    S.add('shell', lambda d: d.ellipse([16, 34, 48, 62]), .0)
    S.add('green', lambda d: [d.rectangle([22, 40, 42, 60]), d.ellipse([22, 36, 42, 48])])
    S.add('yellow', lambda d: d.ellipse([25, 42, 39, 58]), .1)
    S.add('green', lambda d: [d.rectangle([24, 58, 30, 63]), d.rectangle([34, 58, 40, 63])], -.05)
    S.add('green', lambda d: d.ellipse([16, 12, 48, 42]))
    S.add('dark', lambda d: [d.polygon([(16, 22), (18, 12), (24, 18), (28, 10), (32, 16), (36, 10), (40, 18), (46, 12), (48, 22), (44, 18), (20, 18)])], .1)
    S.add('white', lambda d: d.ellipse([20, 8, 44, 18]), .1)
    S.add('water', lambda d: d.ellipse([23, 9, 41, 15]), .15)
    S.add('yellow', lambda d: d.polygon([(28, 31), (36, 31), (32, 37)]), .1)
    S.add('green', lambda d: d.ellipse([41, 44, 47, 50]), .05)
    a = S.render()
    eye(a, 24, 24, '#2A1830', 4); eye(a, 38, 24, '#2A1830', 4)
    px(a, [(56, 8), (57, 9), (57, 10), (57, 11), (57, 12), (57, 13), (57, 14)], '#E8E8F0'); px(a, [(56, 15), (57, 15), (58, 15), (57, 16)], '#E04A4A')
    px(a, [(26, 11), (27, 11), (28, 10)], '#FFFFFF')
    return a
def owl():   # 아울라: 갈색 부엉이, 귀깃, 동그란 금테 안경, 펼친 책
    S = Sprite()
    S.add('brown', lambda d: [d.ellipse([16, 18, 48, 62]), d.polygon([(18, 22), (19, 6), (28, 16)]), d.polygon([(46, 22), (45, 6), (36, 16)])])
    S.add('brown', lambda d: [d.ellipse([12, 30, 22, 56]), d.ellipse([42, 30, 52, 56])], -.1)   # 날개
    S.add('belly', lambda d: d.ellipse([22, 34, 42, 60]), .05)
    S.add('belly', lambda d: [d.ellipse([19, 17, 32, 30]), d.ellipse([32, 17, 45, 30])], .1)   # 얼굴 원반
    S.add('denim', lambda d: d.rectangle([20, 44, 44, 54]), .05)                              # 책 표지
    S.add('paper', lambda d: [d.rectangle([21, 45, 31, 53]), d.rectangle([33, 45, 43, 53])], .15)
    S.add('gold', lambda d: [d.rectangle([24, 60, 28, 63]), d.rectangle([36, 60, 40, 63])])
    a = S.render()
    for cx_ in (25, 38):   # 안경 + 큰 눈
        im = Image.fromarray(a); dd = ImageDraw.Draw(im); dd.ellipse([cx_ - 5, 18, cx_ + 5, 28], outline=hx('#C89420')); a = np.array(im)
        eye(a, cx_ - 1, 21, '#E8A020', 4)
    px(a, [(31, 23), (32, 23), (33, 23)], '#C89420')
    px(a, [(31, 28), (32, 28), (31, 29), (32, 30)], '#E8A020')
    for y in range(46, 53, 2): px(a, [(x, y) for x in range(23, 30)] + [(x, y) for x in range(35, 42)], '#B8AE9C')
    px(a, [(32, y) for y in range(44, 55)], '#24365E')
    return a
def mandrake():   # 맨디: 뿌리 몸, 머리 위 큰 잎, 수줍게 볼 빨간
    S = Sprite()
    S.add('leaf', lambda d: [d.ellipse([12, 2, 30, 26]), d.ellipse([34, 2, 52, 26])], .0)
    S.add('leaf', lambda d: d.ellipse([24, 0, 40, 22]), .1)
    S.add('root', lambda d: [d.polygon([(26, 52), (22, 63), (29, 56)]), d.polygon([(38, 52), (42, 63), (35, 56)])], -.05)
    S.add('root', lambda d: [d.polygon([(22, 38), (10, 46), (12, 48), (22, 44)]), d.polygon([(42, 38), (54, 46), (52, 48), (42, 44)])], -.05)
    S.add('root', lambda d: d.ellipse([20, 20, 44, 56]))
    a = S.render()
    for x0, y0 in ((24, 44), (30, 47), (36, 44)): px(a, [(x0, y0), (x0 + 1, y0 + 1), (x0 + 1, y0 + 2)], '#966C40')
    eye(a, 26, 32); eye(a, 36, 32)
    px(a, [(30, 39), (31, 39), (32, 39), (33, 39), (31, 40), (32, 40)], '#7A3040')
    px(a, [(23, 37), (24, 37), (39, 37), (40, 37), (23, 38), (40, 38)], '#F08AA0')
    for x in (22, 24, 26): px(a, [(x + 10, 6 + (x % 3)), (x + 11, 7 + (x % 3))], '#1E4E22')
    return a
BEASTS = [cat, bat, kappa, owl, mandrake]
if __name__ == '__main__':
    import sys
    sh = np.zeros((64, 64 * len(BEASTS), 4), np.uint8)
    for i, f in enumerate(BEASTS): sh[:, i * 64:(i + 1) * 64] = f()
    bg = Image.new('RGBA', (sh.shape[1], 64), (250, 241, 226, 255)); bg.alpha_composite(Image.fromarray(sh)); bg.resize((bg.width * 5, 320), Image.NEAREST).save(sys.argv[1])
