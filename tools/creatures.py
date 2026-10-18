# 생물 10종 + 알 그림: public/art/creatures.png (화면용, 3배) · public/art/iso/creatures_w.png (세계용, 원래 크기)
# 양·도마뱀(과 이벤트용 용)은 creature_base.png에서 가져오고, 나머지는 같은 그림체로 새로 그려요.
# 재료 아이콘도 icons.png에 그려 넣어요.
import os
from PIL import Image, ImageDraw
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'art')
CW, CH = 40, 34                      # 생물 한 칸 (원래 픽셀)
OUT = (68, 44, 80, 255)
def hexc(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def outline(im):
    px = im.load(); w, h = im.size; add = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0 and any(0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy][3] > 0 and px[x + dx, y + dy] != OUT for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for x, y in add: px[x, y] = OUT
    return im
def new(): im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def P(d, x, y, c): d.point((x, y), fill=hexc(c) if isinstance(c, str) else c)

def cat():          # 검은 고양이: 앉아 있는 통통한 고양이, 노란 눈, 말린 꼬리
    im, d = new(); B, B2, B3 = '#6A5E86', '#564A72', '#8478A2'
    d.ellipse([12, 15, 30, 33], fill=hexc(B)); d.ellipse([14, 17, 22, 26], fill=hexc(B3))
    d.ellipse([10, 4, 30, 20], fill=hexc(B))
    d.polygon([(11, 9), (12, 1), (17, 6)], fill=hexc(B)); d.polygon([(29, 9), (28, 1), (23, 6)], fill=hexc(B))
    d.polygon([(12, 7), (13, 3), (15, 6)], fill=hexc('#F4A0B8')); d.polygon([(28, 7), (27, 3), (25, 6)], fill=hexc('#F4A0B8'))
    for x in (15, 24): d.rectangle([x, 10, x + 2, 13], fill=hexc('#F6D24A')); P(d, x + 1, 11, '#2A1830'); P(d, x + 1, 12, '#2A1830'); P(d, x, 10, '#FFFCE8')
    P(d, 20, 14, '#F4A0B8'); P(d, 19, 15, '#442C50'); P(d, 21, 15, '#442C50')
    d.line([(30, 30), (35, 28), (36, 23), (34, 20)], fill=hexc(B2), width=3)
    d.rectangle([14, 30, 18, 33], fill=hexc(B3)); d.rectangle([23, 30, 27, 33], fill=hexc(B3))
    for x in (13, 26): P(d, x, 15, '#F6A0B0')
    return im
def spider():       # 거미: 보송한 둥근 몸, 다리 8개, 큰 눈
    im, d = new(); B, B2, L = '#8A6A9A', '#A688B4', '#6A4E7A'
    for s in (-1, 1):
        for k, (ex, ey) in enumerate(((14, 14), (16, 21), (16, 27), (13, 32))):
            d.line([(20 + s * 6, 20), (20 + s * (6 + ex // 2), ey - 4), (20 + s * (6 + ex), ey)], fill=hexc(L), width=2)
    d.ellipse([9, 10, 31, 30], fill=hexc(B)); d.ellipse([12, 12, 22, 20], fill=hexc(B2))
    for x in (14, 23): d.ellipse([x, 15, x + 3, 20], fill=hexc('#FFFFFF')); d.ellipse([x + 1, 16, x + 3, 20], fill=hexc('#2A1830')); P(d, x + 1, 16, '#FFFFFF')
    d.line([(18, 24), (20, 25), (22, 24)], fill=hexc('#442C50'))
    for x in (11, 27): P(d, x, 22, '#FFB0C4'); P(d, x + 1, 22, '#FFB0C4')
    return im
def owl():          # 부엉이: 둥근 몸, 귀깃, 큰 눈, 배 무늬
    im, d = new(); B, B2, C = '#A87E58', '#8A6444', '#F2E2C4'
    d.ellipse([10, 6, 30, 33], fill=hexc(B)); d.ellipse([14, 16, 26, 32], fill=hexc(C))
    for y in (20, 24, 28):
        for x in range(16, 25, 3): P(d, x, y, '#C8A880'); P(d, x + 1, y + 1, '#C8A880')
    d.polygon([(11, 9), (10, 2), (16, 7)], fill=hexc(B2)); d.polygon([(29, 9), (30, 2), (24, 7)], fill=hexc(B2))
    for x in (12, 21): d.ellipse([x, 8, x + 7, 15], fill=hexc('#FFFCF0')); d.ellipse([x + 2, 10, x + 5, 14], fill=hexc('#2A1830')); P(d, x + 3, 10, '#FFFFFF')
    d.polygon([(19, 15), (21, 15), (20, 18)], fill=hexc('#F0B040'))
    d.ellipse([7, 15, 13, 28], fill=hexc(B2)); d.ellipse([27, 15, 33, 28], fill=hexc(B2))
    for x in (16, 22): d.line([(x, 33), (x + 2, 33)], fill=hexc('#F0B040'))
    return im
def rabbit():       # 토끼: 옆모습, 긴 귀, 동그란 꼬리
    im, d = new(); B, B2, B3 = '#F6F2EE', '#DCD2CC', '#FFFFFF'
    d.ellipse([9, 15, 31, 32], fill=hexc(B)); d.ellipse([24, 22, 30, 32], fill=hexc(B2))
    d.ellipse([4, 19, 11, 26], fill=hexc(B3))
    d.ellipse([22, 8, 37, 23], fill=hexc(B))
    d.ellipse([22, 0, 27, 14], fill=hexc(B)); d.ellipse([27, 0, 32, 13], fill=hexc(B2))
    d.ellipse([23, 2, 26, 11], fill=hexc('#F4B0C4'))
    d.rectangle([30, 13, 32, 16], fill=hexc('#2A1830')); P(d, 30, 13, '#FFFFFF')
    P(d, 37, 17, '#F4A0B8'); P(d, 36, 18, '#F4A0B8'); P(d, 33, 18, '#FFB0C4'); P(d, 34, 18, '#FFB0C4')
    d.rectangle([12, 30, 17, 33], fill=hexc(B2)); d.rectangle([26, 30, 30, 33], fill=hexc(B2))
    return im
def chicken():      # 닭: 통통한 몸, 빨간 볏, 노란 부리
    im, d = new(); B, B2, B3 = '#FFF8EC', '#E8DCC8', '#FFFFFF'
    d.polygon([(5, 12), (11, 16), (10, 24)], fill=hexc(B2)); d.polygon([(4, 18), (11, 18), (11, 25)], fill=hexc(B))
    d.ellipse([7, 13, 31, 31], fill=hexc(B)); d.ellipse([20, 3, 33, 18], fill=hexc(B))
    d.ellipse([11, 18, 22, 26], fill=hexc(B2)); d.line([(13, 20), (20, 24)], fill=hexc('#D0C2AC'))
    for x, y in ((23, 1), (26, 0), (29, 1)): d.ellipse([x, y, x + 3, y + 4], fill=hexc('#E8484C'))
    d.polygon([(32, 9), (37, 11), (32, 13)], fill=hexc('#F6B830'))
    d.ellipse([30, 13, 33, 18], fill=hexc('#E8484C'))
    d.rectangle([27, 8, 28, 9], fill=hexc('#2A1830')); P(d, 27, 8, '#FFFFFF')
    P(d, 25, 12, '#FFB0C4'); P(d, 26, 12, '#FFB0C4')
    for x in (16, 23): d.line([(x, 30), (x, 33)], fill=hexc('#F0A030'), width=2); d.line([(x - 1, 33), (x + 2, 33)], fill=hexc('#F0A030'))
    return im
def toad():         # 두꺼비: 납작하고 넓은 몸, 툭 튀어나온 눈, 오돌토돌 등
    im, d = new(); B, B2, C = '#8AAE5A', '#6E9244', '#E8E4B0'
    d.ellipse([5, 13, 35, 33], fill=hexc(B)); d.ellipse([11, 21, 29, 33], fill=hexc(C))
    for x in (9, 24): d.ellipse([x, 7, x + 8, 16], fill=hexc(B)); d.ellipse([x + 1, 8, x + 7, 15], fill=hexc('#F6E070')); d.rectangle([x + 2, 10, x + 6, 12], fill=hexc('#2A1830')); P(d, x + 2, 9, '#FFFFFF')
    for x, y in ((8, 19), (31, 18), (12, 16), (28, 23), (6, 25), (33, 26)): d.ellipse([x, y, x + 2, y + 2], fill=hexc(B2))
    d.line([(14, 20), (20, 22), (26, 20)], fill=hexc('#4A3050'))
    for x in (11, 27): P(d, x, 20, '#FFB0C4'); P(d, x + 1, 20, '#FFB0C4')
    d.ellipse([2, 26, 11, 33], fill=hexc(B2)); d.ellipse([29, 26, 38, 33], fill=hexc(B2))
    return im
def bee():          # 꿀벌: 줄무늬 둥근 몸, 투명한 날개, 더듬이
    im, d = new(); Y, K = '#F6C83A', '#4A3A44'
    d.ellipse([7, 3, 19, 15], fill=hexc('#E4F2FF', 230)); d.ellipse([21, 3, 33, 15], fill=hexc('#E4F2FF', 230))
    d.ellipse([9, 5, 13, 9], fill=hexc('#FFFFFF')); d.ellipse([23, 5, 27, 9], fill=hexc('#FFFFFF'))
    d.ellipse([8, 11, 32, 32], fill=hexc(Y))
    for y in (21, 26): d.rectangle([9, y, 31, y + 2], fill=hexc(K))
    d.polygon([(18, 31), (22, 31), (20, 34)], fill=hexc(K))
    d.line([(16, 12), (13, 6), (11, 5)], fill=hexc(K)); d.line([(24, 12), (27, 6), (29, 5)], fill=hexc(K))
    d.ellipse([10, 4, 12, 6], fill=hexc(K)); d.ellipse([28, 4, 30, 6], fill=hexc(K))
    for x in (14, 24): d.rectangle([x, 15, x + 2, 18], fill=hexc('#2A1830')); P(d, x, 15, '#FFFFFF')
    d.line([(18, 19), (20, 20), (22, 19)], fill=hexc('#4A3050'))
    for x in (11, 27): P(d, x, 19, '#F49A80'); P(d, x + 1, 19, '#F49A80')
    return im
def goat():         # 염소: 옆모습, 굽은 뿔, 턱수염
    im, d = new(); B, B2, B3 = '#F2EADA', '#D8CCB6', '#FFFFFF'
    d.ellipse([5, 13, 29, 28], fill=hexc(B)); d.polygon([(4, 14), (7, 12), (6, 18)], fill=hexc(B2))
    d.ellipse([8, 15, 18, 21], fill=hexc(B3))
    d.ellipse([24, 6, 36, 19], fill=hexc(B)); d.rectangle([24, 12, 29, 20], fill=hexc(B))
    d.line([(26, 7), (24, 2), (21, 1), (19, 3)], fill=hexc('#A8906C'), width=2)
    d.polygon([(23, 10), (18, 12), (23, 13)], fill=hexc(B2))
    d.rectangle([31, 10, 32, 12], fill=hexc('#2A1830')); P(d, 31, 10, '#FFFFFF')
    d.polygon([(32, 18), (35, 18), (34, 23)], fill=hexc(B2))
    P(d, 36, 14, '#B89A88'); P(d, 29, 14, '#FFB0C4'); P(d, 30, 14, '#FFB0C4')
    for x in (8, 13, 20, 25): d.rectangle([x, 26, x + 2, 33], fill=hexc(B2)); d.rectangle([x, 32, x + 2, 33], fill=hexc('#7A6A5A'))
    return im
def egg():          # 알 (색은 게임에서 생물 색으로 물들여요)
    im, d = new()
    d.ellipse([13, 9, 27, 32], fill=hexc('#F8F0DE')); d.ellipse([15, 11, 20, 17], fill=hexc('#FFFFFF'))
    d.ellipse([23, 18, 27, 30], fill=hexc('#E8DCC0'))
    for x, y in ((18, 22), (22, 14), (16, 27), (23, 26), (20, 18)): d.ellipse([x, y, x + 2, y + 2], fill=hexc('#E0B888'))
    return im

base = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creature_base.png')).convert('RGBA')
old = [base.crop((i * CW, 0, i * CW + CW, CH)) for i in range(4)]   # 0 양 · 1 (유니콘) · 2 도마뱀 · 3 (용)
# 0 양 · 1 토끼 · 2 도마뱀 · 3 닭 · 4 고양이 · 5 두꺼비 · 6 꿀벌 · 7 거미 · 8 부엉이 · 9 염소 · 10 알 · 11 용(드래곤 방문 이벤트)
L = lambda im: im.transpose(Image.FLIP_LEFT_RIGHT)   # 옆모습은 왼쪽을 보게 (양·도마뱀과 같이)
cells = [old[0], L(outline(rabbit())), old[2], L(outline(chicken())), outline(cat()), outline(toad()), outline(bee()), outline(spider()), outline(owl()), L(outline(goat())), outline(egg()), old[3]]
world = Image.new('RGBA', (CW * len(cells), CH), (0, 0, 0, 0))
for i, c in enumerate(cells): world.paste(c, (i * CW, 0))
world.save(os.path.join(R, 'iso', 'creatures_w.png'))
world.resize((world.width * 3, world.height * 3), Image.NEAREST).save(os.path.join(R, 'creatures.png'))

# ---- 재료 아이콘 (16×16을 2배로): 9번 토끼털은 덮어 그리고, 38번부터 생물 재료 ----
def icon(fn):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d); return outline(im).resize((32, 32), Image.NEAREST)
def i_rfur(d):      # 토끼털: 보송한 하얀 털뭉치
    for x, y, r in ((3, 6, 4), (8, 4, 4), (6, 9, 4), (10, 8, 3)): d.ellipse([x - 1, y - 1, x + r, y + r], fill=hexc('#FAF6F2'))
    d.ellipse([5, 5, 8, 8], fill=hexc('#FFFFFF')); d.point((11, 11), fill=hexc('#E4DAD4')); d.point((4, 11), fill=hexc('#E4DAD4'))
def i_whisker(d):
    for y, c in ((5, '#F4F0FA'), (8, '#E4E0F0'), (11, '#F4F0FA')): d.line([(2, y + 1), (8, y), (13, y + 2)], fill=hexc(c))
    d.ellipse([6, 6, 9, 10], fill=hexc('#6A5E86'))
def i_slime(d):     # 두꺼비 점액: 초록 물방울 병
    d.rectangle([6, 2, 9, 4], fill=hexc('#C8A070')); d.ellipse([3, 4, 12, 14], fill=hexc('#9ED46A')); d.ellipse([5, 6, 8, 9], fill=hexc('#E4FFC8'))
    d.point((9, 11), fill=hexc('#6EA840')); d.point((6, 12), fill=hexc('#6EA840'))
def i_honey(d):     # 벌꿀: 꿀단지
    d.ellipse([2, 5, 13, 14], fill=hexc('#F6B830')); d.rectangle([4, 3, 11, 6], fill=hexc('#E89A20')); d.rectangle([3, 2, 12, 3], fill=hexc('#C87A3A'))
    d.ellipse([4, 7, 7, 10], fill=hexc('#FFE490')); d.polygon([(9, 5), (11, 5), (10, 9)], fill=hexc('#F6C840'))
def i_silk(d):
    d.ellipse([3, 3, 13, 13], fill=hexc('#F4F2FA')); d.line([(4, 6), (12, 10)], fill=hexc('#D0CAE4')); d.line([(4, 10), (12, 6)], fill=hexc('#D0CAE4')); d.line([(8, 3), (8, 13)], fill=hexc('#D0CAE4'))
def i_feather(d):
    d.polygon([(11, 2), (13, 4), (6, 13), (3, 14), (4, 11)], fill=hexc('#C89A6C')); d.line([(12, 3), (3, 14)], fill=hexc('#F2E2C4'))
def i_milk(d):      # 염소젖: 우유병
    d.rectangle([6, 1, 9, 3], fill=hexc('#7AB0E8')); d.polygon([(6, 4), (9, 4), (12, 7), (12, 14), (3, 14), (3, 7)], fill=hexc('#FFFFFF'))
    d.rectangle([3, 9, 12, 11], fill=hexc('#BCD8F4')); d.point((5, 6), fill=hexc('#E4EEF8'))
def i_hegg(d):      # 달걀
    d.ellipse([4, 2, 12, 14], fill=hexc('#F8EAD2')); d.ellipse([5, 4, 7, 7], fill=hexc('#FFFFFF')); d.ellipse([9, 8, 11, 13], fill=hexc('#E8D4B4'))
ic_old = Image.open(os.path.join(R, 'icons.png')).convert('RGBA')
N0 = 38                                # 기존 아이콘 수 (ICONS 목록 앞부분)
new_icons = [icon(f) for f in (i_whisker, i_slime, i_honey, i_silk, i_feather, i_milk, i_hegg)]
ic_new = Image.new('RGBA', (32 * (N0 + len(new_icons)), 32), (0, 0, 0, 0)); ic_new.paste(ic_old.crop((0, 0, 32 * N0, 32)), (0, 0))
ic_new.paste((0, 0, 0, 0), (32 * 9, 0, 32 * 10, 32)); ic_new.paste(icon(i_rfur), (32 * 9, 0))
for i, im in enumerate(new_icons): ic_new.paste(im, (32 * (N0 + i), 0))
ic_new.save(os.path.join(R, 'icons.png'))
print('creatures', world.size, 'icons', ic_new.size)
