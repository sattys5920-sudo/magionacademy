# 탐사 몬스터 도트 그림 → public/art/monsters.png (48px 칸 가로로 이어 붙임). 순서는 MON 목록 (index.html의 XMS와 같아야 해요)
from PIL import Image, ImageDraw
import math
O = (36, 24, 48, 255)
def C(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (255,)
def lt(c, k=40): return tuple(min(255, v + k) for v in c[:3]) + (255,)
def dk(c, k=40): return tuple(max(0, v - k) for v in c[:3]) + (255,)
W = (250, 248, 240, 255); BK = (30, 20, 40, 255)
def eyes(d, x1, x2, y, c=W, r=2, pupil=True):
    for x in (x1, x2):
        d.ellipse([x-r, y-r, x+r, y+r], fill=c)
        if pupil: d.rectangle([x, y-1, x+1, y+1], fill=BK)
def slime(d, c):
    d.ellipse([3,13,29,30], fill=c); d.ellipse([8,6,24,22], fill=c); d.ellipse([8,9,13,14], fill=lt(c,70)); d.rectangle([5,25,27,29], fill=dk(c,25)); eyes(d, 12, 20, 19); d.arc([13,21,19,26], 20, 160, fill=BK)
def rabbit(d, c):
    d.ellipse([6,14,26,30], fill=c); d.ellipse([10,6,24,19], fill=c); d.ellipse([11,0,15,12], fill=c); d.ellipse([19,0,23,12], fill=c); d.ellipse([12,2,14,9], fill=(255,170,190,255)); d.ellipse([20,2,22,9], fill=(255,170,190,255))
    d.rectangle([15,4,17,7], fill=(80,160,70,255)); eyes(d, 14, 21, 13, r=1); d.rectangle([17,16,18,17], fill=(255,120,150,255)); d.ellipse([20,24,28,30], fill=W); d.line([(10,16),(10,26)], fill=dk(c), width=1)
def bat(d, c):
    d.polygon([(16,12),(2,6),(5,14),(1,22),(10,18),(16,24)], fill=c); d.polygon([(16,12),(30,6),(27,14),(31,22),(22,18),(16,24)], fill=c)
    d.ellipse([11,10,21,24], fill=dk(c,20)); d.polygon([(11,12),(11,5),(15,10)], fill=dk(c,20)); d.polygon([(21,12),(21,5),(17,10)], fill=dk(c,20)); eyes(d, 14, 18, 16, c=(255,80,80,255), r=1, pupil=False); d.rectangle([15,20,15,21], fill=W); d.rectangle([17,20,17,21], fill=W)
def ghost(d, c):
    d.ellipse([6,3,26,22], fill=c); d.rectangle([6,12,26,26], fill=c); d.polygon([(6,26),(10,30),(14,26),(18,30),(22,26),(26,30),(26,26)], fill=c); d.ellipse([10,6,15,11], fill=lt(c,60))
    d.ellipse([10,12,14,18], fill=BK); d.ellipse([18,12,22,18], fill=BK); d.ellipse([14,19,18,23], fill=BK)
def skeleton(d, c):
    d.ellipse([9,2,23,15], fill=c); d.rectangle([12,12,20,17], fill=c); d.ellipse([11,6,14,10], fill=BK); d.ellipse([18,6,21,10], fill=BK); d.rectangle([15,10,16,12], fill=BK)
    d.rectangle([14,17,18,28], fill=c); [d.line([(9,y),(23,y)], fill=c, width=2) for y in (19,22,25)]; d.line([(7,19),(3,28)], fill=c, width=2); d.line([(25,19),(28,13)], fill=c, width=2)
    d.polygon([(28,4),(30,4),(31,16),(27,16)], fill=(190,200,220,255)); d.rectangle([26,16,32,17], fill=(150,100,50,255)); d.line([(12,28),(11,31)], fill=c, width=2); d.line([(20,28),(21,31)], fill=c, width=2)
def spider(d, c):
    for s in (-1, 1):
        for i, (dx, dy) in enumerate(((10,-6),(14,-2),(14,4),(10,9))): d.line([(16,18),(16+s*dx//2,18+dy//2-4),(16+s*dx,18+dy+2)], fill=O, width=3); d.line([(16,18),(16+s*dx//2,18+dy//2-4),(16+s*dx,18+dy+2)], fill=dk(c,10), width=1)
    d.ellipse([9,12,25,28], fill=c); d.ellipse([11,6,21,16], fill=dk(c,15)); d.ellipse([12,8,15,11], fill=(255,60,60,255)); d.ellipse([17,8,20,11], fill=(255,60,60,255)); d.polygon([(16,20),(13,24),(19,24)], fill=(220,60,60,255))
def zombie(d, c):
    d.ellipse([9,2,23,15], fill=c); d.rectangle([11,13,21,28], fill=(110,90,150,255)); d.rectangle([8,15,13,26], fill=(110,90,150,255)); d.rectangle([19,15,24,26], fill=(110,90,150,255)); d.rectangle([0,15,9,18], fill=c); d.rectangle([23,15,31,18], fill=c)
    eyes(d, 13, 19, 8, c=(255,255,150,255), r=2); d.rectangle([13,11,19,12], fill=BK); d.rectangle([12,27,15,31], fill=dk(c)); d.rectangle([17,27,20,31], fill=dk(c)); d.line([(12,22),(20,24)], fill=dk((110,90,150,255)), width=1)
def frog(d, c):
    d.ellipse([3,12,29,30], fill=c); d.ellipse([7,6,13,13], fill=c); d.ellipse([19,6,25,13], fill=c); eyes(d, 10, 22, 9, r=2); d.ellipse([8,20,24,29], fill=lt(c,50)); d.arc([8,17,24,26], 10, 170, fill=BK); d.ellipse([2,24,9,31], fill=dk(c,15)); d.ellipse([23,24,30,31], fill=dk(c,15))
def spirit(d, c):
    d.polygon([(16,2),(24,14),(26,22),(16,30),(6,22),(8,14)], fill=c); d.polygon([(16,12),(21,20),(16,28),(11,20)], fill=lt(c,70)); eyes(d, 13, 19, 20, c=BK, r=1, pupil=False)
def crab(d, c):
    d.ellipse([6,13,26,28], fill=c); d.ellipse([0,5,9,14], fill=c); d.ellipse([23,5,32,14], fill=c); d.rectangle([4,12,8,16], fill=c); d.rectangle([24,12,28,16], fill=c); d.line([(11,13),(10,7)], fill=O, width=3); d.line([(21,13),(22,7)], fill=O, width=3); eyes(d, 10, 22, 7, r=2)
    d.polygon([(0,5),(4,7),(2,10)], fill=BK); d.polygon([(32,5),(28,7),(30,10)], fill=BK); [d.line([(x,26),(x-2,31)], fill=dk(c), width=2) for x in (9,13,19,23)]; d.ellipse([10,15,15,19], fill=lt(c,60))
def mushroom(d, c):
    d.rectangle([11,16,21,28], fill=(235,225,200,255)); d.ellipse([3,3,29,20], fill=c); d.ellipse([8,7,13,12], fill=W); d.ellipse([18,5,24,11], fill=W); d.ellipse([14,12,17,15], fill=W); eyes(d, 13, 19, 21, c=BK, r=1, pupil=False); d.rectangle([14,24,18,25], fill=BK); d.ellipse([9,27,23,31], fill=dk((235,225,200,255)))
def golem(d, c):
    d.rectangle([8,10,24,26], fill=c); d.rectangle([11,2,21,11], fill=dk(c,10)); d.rectangle([2,12,8,24], fill=c); d.rectangle([24,12,30,24], fill=c); d.rectangle([9,26,14,31], fill=dk(c)); d.rectangle([18,26,23,31], fill=dk(c))
    d.rectangle([13,5,15,7], fill=(255,200,60,255)); d.rectangle([18,5,20,7], fill=(255,200,60,255)); d.rectangle([10,14,13,16], fill=lt(c,30)); d.line([(15,18),(20,22)], fill=dk(c,70), width=1); d.line([(5,15),(6,20)], fill=dk(c,70), width=1)
def wolf(d, c):
    d.ellipse([2,12,24,26], fill=c); d.polygon([(20,10),(30,14),(31,19),(22,21)], fill=c); d.polygon([(20,10),(22,3),(25,10)], fill=c); d.polygon([(24,10),(27,4),(28,12)], fill=dk(c)); d.polygon([(2,16),(0,8),(7,14)], fill=c)
    [d.rectangle([x,23,x+3,30], fill=dk(c,15)) for x in (5,10,17,21)]; d.rectangle([24,14,25,15], fill=(255,220,60,255)); d.rectangle([29,17,31,18], fill=BK); d.polygon([(25,19),(27,22),(28,19)], fill=W)
def shadow(d, c):
    d.ellipse([9,2,23,16], fill=c); d.polygon([(7,14),(25,14),(28,30),(4,30)], fill=c); d.polygon([(4,30),(8,26),(12,31),(16,26),(20,31),(24,26),(28,30)], fill=c)
    d.polygon([(11,8),(15,9),(14,11)], fill=(255,80,200,255)); d.polygon([(21,8),(17,9),(18,11)], fill=(255,80,200,255)); d.line([(2,18),(8,22)], fill=c, width=3); d.line([(30,18),(24,22)], fill=c, width=3)
def gargoyle(d, c):
    d.polygon([(16,14),(2,4),(4,16),(0,24),(10,20),(16,26)], fill=dk(c,10)); d.polygon([(16,14),(30,4),(28,16),(32,24),(22,20),(16,26)], fill=dk(c,10)); d.ellipse([9,8,23,28], fill=c); d.polygon([(10,10),(8,2),(13,8)], fill=dk(c,30)); d.polygon([(22,10),(24,2),(19,8)], fill=dk(c,30))
    d.rectangle([12,14,14,16], fill=(255,80,60,255)); d.rectangle([18,14,20,16], fill=(255,80,60,255)); d.polygon([(14,21),(16,24),(18,21)], fill=W); d.rectangle([10,26,14,31], fill=dk(c)); d.rectangle([18,26,22,31], fill=dk(c))
def statue(d, c):
    d.rectangle([9,2,23,10], fill=c); d.rectangle([7,10,25,24], fill=dk(c,10)); d.rectangle([3,12,8,27], fill=c); d.rectangle([24,12,29,27], fill=c); d.rectangle([9,24,23,31], fill=dk(c,25)); d.rectangle([12,5,14,6], fill=(90,220,255,255)); d.rectangle([18,5,20,6], fill=(90,220,255,255)); d.rectangle([14,13,18,20], fill=(90,220,255,255)); d.rectangle([14,0,18,2], fill=(230,190,70,255))
# ── 보스(48px) ──
def tree(d, c):
    d.rectangle([17,20,31,46], fill=(110,70,40,255)); d.polygon([(17,46),(9,47),(17,40)], fill=(110,70,40,255)); d.polygon([(31,46),(39,47),(31,40)], fill=(110,70,40,255))
    for x, y, r in ((10,12,10),(24,6,12),(38,12,10),(16,18,9),(32,18,9)): d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    d.ellipse([10,6,18,13], fill=lt(c,40)); d.polygon([(17,28),(21,31),(18,34)], fill=(255,210,60,255)); d.polygon([(31,28),(27,31),(30,34)], fill=(255,210,60,255)); d.polygon([(20,38),(24,41),(28,38),(24,36)], fill=BK); d.line([(17,24),(4,30)], fill=(110,70,40,255), width=3); d.line([(31,24),(44,30)], fill=(110,70,40,255), width=3)
def lich(d, c):
    d.polygon([(10,16),(38,16),(44,46),(4,46)], fill=c); d.polygon([(4,46),(10,40),(16,47),(24,40),(32,47),(38,40),(44,46)], fill=c); d.ellipse([15,3,33,22], fill=(235,235,225,255)); d.rectangle([19,18,29,24], fill=(235,235,225,255)); d.ellipse([18,9,22,14], fill=(120,255,160,255)); d.ellipse([26,9,30,14], fill=(120,255,160,255)); d.polygon([(22,15),(26,15),(24,18)], fill=BK)
    d.polygon([(13,6),(16,0),(20,5),(24,0),(28,5),(32,0),(35,6),(33,9),(15,9)], fill=(230,190,70,255)); d.line([(6,18),(6,46)], fill=(120,80,50,255), width=3); d.ellipse([2,10,10,18], fill=(150,100,255,255)); d.ellipse([4,12,7,15], fill=W)
def serpent(d, c):
    pts = [(6,40),(14,44),(24,40),(34,44),(42,36),(36,26),(26,22),(30,12)]
    for i in range(len(pts)-1): d.line([pts[i], pts[i+1]], fill=c, width=10 - i)
    d.ellipse([22,4,42,20], fill=c); d.polygon([(24,6),(20,0),(28,4)], fill=dk(c)); d.polygon([(40,6),(44,0),(36,4)], fill=dk(c)); d.ellipse([27,8,31,12], fill=(255,230,60,255)); d.ellipse([34,8,38,12], fill=(255,230,60,255)); d.rectangle([28,9,29,11], fill=BK); d.rectangle([35,9,36,11], fill=BK); d.polygon([(30,18),(32,26),(34,18)], fill=(255,90,110,255)); d.line([(8,38),(8,42)], fill=lt(c,50), width=2); d.line([(18,41),(26,41)], fill=lt(c,50), width=2)
def king(d, c):
    d.rectangle([14,12,34,32], fill=c); d.rectangle([17,2,31,14], fill=dk(c,10)); d.rectangle([4,14,13,38], fill=c); d.rectangle([35,14,44,38], fill=c); d.rectangle([14,32,34,47], fill=dk(c,20)); d.rectangle([2,38,14,44], fill=dk(c,10)); d.rectangle([34,38,46,44], fill=dk(c,10))
    d.polygon([(15,2),(18,-1),(22,2),(24,-2),(26,2),(30,-1),(33,2),(33,5),(15,5)], fill=(235,195,70,255)); d.rectangle([20,7,23,9], fill=(255,120,60,255)); d.rectangle([26,7,29,9], fill=(255,120,60,255)); d.rectangle([20,18,28,26], fill=(255,120,60,255)); d.rectangle([22,20,26,24], fill=(255,230,150,255)); d.line([(8,18),(8,32)], fill=lt(c,30), width=1)
MON = [  # id, 그림 함수, 색, 크기(48칸 안에서 배율) — 숲 4 · 묘지 4 · 동굴 4 · 신전 4 · 정예 4 · 보스 4
 ('slime', slime, '#6fcf6f', 1.0), ('pkrabbit', rabbit, '#f0903a', 1.0), ('batkid', bat, '#8a6fc0', 1.0), ('ghostkid', ghost, '#bfe3ff', 1.0),
 ('skelsol', skeleton, '#e8e4d4', 1.1), ('spider', spider, '#5a4a6a', 1.1), ('zombie', zombie, '#7fae6a', 1.1), ('gravebat', bat, '#5a6a8a', 1.1),
 ('frog', frog, '#4fae8f', 1.1), ('watersp', spirit, '#58b8ff', 1.1), ('crab', crab, '#d8645a', 1.1), ('mush', mushroom, '#b05ad0', 1.1),
 ('golem', golem, '#c8a870', 1.2), ('guardian', statue, '#9aa0b8', 1.2), ('firesp', spirit, '#ff7a3a', 1.2), ('shadow', shadow, '#4a3a7a', 1.2),
 ('oldwolf', wolf, '#8a8a98', 1.3), ('skelknight', skeleton, '#9a7ac0', 1.4), ('bigcrab', crab, '#a8403a', 1.4), ('gargoyle', gargoyle, '#7a8090', 1.4),
 ('b_tree', tree, '#4f9f4a', 1), ('b_lich', lich, '#5a3a8a', 1), ('b_serpent', serpent, '#3a9a8a', 1), ('b_king', king, '#b0a070', 1)]
def outline(im):
    a = im.load(); w, h = im.size; o = Image.new('RGBA', im.size, (0,0,0,0)); b = o.load()
    for y in range(h):
        for x in range(w):
            if a[x, y][3]: b[x, y] = a[x, y]
    for y in range(h):
        for x in range(w):
            if not a[x, y][3] and any(0 <= x+dx < w and 0 <= y+dy < h and a[x+dx, y+dy][3] for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): b[x, y] = O
    return o
sheet = Image.new('RGBA', (48 * len(MON), 48))
for i, (mid, fn, col, sc) in enumerate(MON):
    big = mid.startswith('b_'); S = 48 if big else 32
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d, C(col))
    # 모서리가 뭉개지지 않게 밝은 윗면 한 줄 + 아래 그림자
    px = im.load()
    for y in range(S - 1, 0, -1):
        for x in range(S):
            if px[x, y][3] and not px[x, y-1][3]: px[x, y-1] = (0,0,0,0)
    if sc != 1.0 and not big: n = round(S * sc); im = im.resize((n, n), Image.NEAREST); S = n
    if S > 46: im = im.resize((46, 46), Image.NEAREST); S = 46
    im = outline(im.crop((0,0,S,S)).copy().convert('RGBA'))
    sheet.alpha_composite(im, (i * 48 + (48 - im.width) // 2, 48 - im.height))
sheet.save('public/art/monsters.png', optimize=True)
big = sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST)
big.crop((0, 0, 48 * 12 * 3, 144)).save('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mon_a.png'); big.crop((48 * 12 * 3, 0, 48 * 24 * 3, 144)).save('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mon_b.png')
