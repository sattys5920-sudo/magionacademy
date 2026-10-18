# 생물 10종 + 알 그림: public/art/creatures.png (화면용, 3배) · public/art/iso/creatures_w.png (세계용, 원래 크기)
# 기존 4종(구름양·유니콘·불도마뱀·용)은 지금 그림에서 그대로 가져오고, 6종을 같은 그림체로 새로 그려요.
# 재료 아이콘 6개도 icons.png 끝에 덧붙여요.
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
def bat():          # 박쥐: 둥근 몸, 큰 귀, 펼친 날개, 송곳니
    im, d = new(); B, W, W2 = '#7A6A96', '#5E4E7A', '#9888B4'
    for s in (-1, 1):
        cx = 20 + s * 2
        pts = [(cx, 14), (20 + s * 18, 6), (20 + s * 19, 16), (20 + s * 15, 14), (20 + s * 14, 20), (20 + s * 10, 17), (20 + s * 8, 23)]
        d.polygon(pts, fill=hexc(W)); d.line([(cx, 14), (20 + s * 18, 6)], fill=hexc(W2))
    d.ellipse([12, 9, 28, 29], fill=hexc(B)); d.ellipse([15, 18, 25, 28], fill=hexc('#B4A8CC'))
    d.polygon([(13, 12), (14, 2), (19, 9)], fill=hexc(B)); d.polygon([(27, 12), (26, 2), (21, 9)], fill=hexc(B))
    d.polygon([(14, 9), (15, 5), (17, 9)], fill=hexc('#F4A0B8')); d.polygon([(26, 9), (25, 5), (23, 9)], fill=hexc('#F4A0B8'))
    for x in (16, 23): d.rectangle([x, 13, x + 1, 15], fill=hexc('#2A1830')); P(d, x, 13, '#FFFFFF')
    P(d, 19, 18, '#FFFFFF'); P(d, 21, 18, '#FFFFFF'); P(d, 20, 17, '#442C50')
    d.rectangle([16, 29, 17, 31], fill=hexc('#5E4E7A')); d.rectangle([23, 29, 24, 31], fill=hexc('#5E4E7A'))
    return im
def ghost():        # 꼬마 유령: 하얀 천, 물결 자락, 볼터치
    im, d = new(); B, B2 = '#F6F4FC', '#D6D0EA'
    d.ellipse([10, 4, 30, 24], fill=hexc(B)); d.rectangle([10, 14, 30, 28], fill=hexc(B))
    for i, x in enumerate(range(10, 31, 5)): d.ellipse([x - 1, 25, x + 4, 31], fill=hexc(B))
    d.rectangle([27, 12, 30, 28], fill=hexc(B2)); d.ellipse([12, 6, 17, 10], fill=hexc('#FFFFFF'))
    for x in (15, 23): d.ellipse([x, 12, x + 2, 16], fill=hexc('#2A1830')); P(d, x, 12, '#FFFFFF')
    d.ellipse([18, 17, 21, 20], fill=hexc('#442C50'))
    for x in (12, 26): d.rectangle([x, 17, x + 2, 18], fill=hexc('#FFB0C4'))
    d.line([(7, 18), (10, 16)], fill=hexc(B), width=2); d.line([(33, 18), (30, 16)], fill=hexc(B), width=2)
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
def pumpkin():      # 호박 정령: 호박 몸, 잎, 웃는 얼굴, 덩굴 팔
    im, d = new(); O, O2, O3 = '#F08A30', '#D06A20', '#FFB060'
    for cx, w in ((14, 8), (26, 8), (20, 9)): d.ellipse([cx - w, 9, cx + w, 31], fill=hexc(O))
    for x in (13, 27): d.line([(x, 11), (x, 29)], fill=hexc(O2))
    d.ellipse([15, 11, 20, 16], fill=hexc(O3))
    d.rectangle([19, 4, 21, 9], fill=hexc('#4A7A2E')); d.ellipse([21, 3, 29, 8], fill=hexc('#6AAE4A'))
    d.line([(9, 6), (12, 9)], fill=hexc('#6AAE4A'))
    for x in (14, 23): d.polygon([(x, 17), (x + 3, 17), (x + 1, 14)], fill=hexc('#FFE07A'))
    d.polygon([(15, 23), (25, 23), (23, 26), (17, 26)], fill=hexc('#FFE07A')); P(d, 18, 23, O); P(d, 22, 23, O)
    d.line([(6, 22), (3, 18), (5, 15)], fill=hexc('#4A7A2E'), width=2); d.line([(34, 22), (37, 18), (35, 15)], fill=hexc('#4A7A2E'), width=2)
    d.rectangle([15, 30, 18, 33], fill=hexc(O2)); d.rectangle([22, 30, 25, 33], fill=hexc(O2))
    return im
def egg():          # 알 (색은 게임에서 생물 색으로 물들여요)
    im, d = new()
    d.ellipse([13, 9, 27, 32], fill=hexc('#F8F0DE')); d.ellipse([15, 11, 20, 17], fill=hexc('#FFFFFF'))
    d.ellipse([23, 18, 27, 30], fill=hexc('#E8DCC0'))
    for x, y in ((18, 22), (22, 14), (16, 27), (23, 26), (20, 18)): d.ellipse([x, y, x + 2, y + 2], fill=hexc('#E0B888'))
    return im

old = Image.open(os.path.join(R, 'creatures.png')).convert('RGBA')
old_n = old.resize((old.width // 3, old.height // 3), Image.NEAREST)
cells = [old_n.crop((i * CW, 0, i * CW + CW, CH)) for i in range(4)]
cells += [outline(f()) for f in (cat, bat, ghost, spider, owl, pumpkin)]
cells.append(outline(egg()))
world = Image.new('RGBA', (CW * len(cells), CH), (0, 0, 0, 0))
for i, c in enumerate(cells): world.paste(c, (i * CW, 0))
world.save(os.path.join(R, 'iso', 'creatures_w.png'))
world.resize((world.width * 3, world.height * 3), Image.NEAREST).save(os.path.join(R, 'creatures.png'))

# ---- 재료 아이콘 6개 (16×16을 2배로) ----
def icon(fn):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d); return outline(im).resize((32, 32), Image.NEAREST)
def i_whisker(d):
    for y, c in ((5, '#F4F0FA'), (8, '#E4E0F0'), (11, '#F4F0FA')): d.line([(2, y + 1), (8, y), (13, y + 2)], fill=hexc(c))
    d.ellipse([6, 6, 9, 10], fill=hexc('#6A5E86'))
def i_batdust(d):
    d.polygon([(4, 5), (11, 5), (12, 13), (3, 13)], fill=hexc('#9888B4')); d.rectangle([5, 2, 10, 5], fill=hexc('#C8A070'))
    for x, y in ((5, 8), (8, 10), (10, 7), (6, 11)): d.point((x, y), fill=hexc('#FFF0A8'))
def i_ecto(d):
    d.ellipse([3, 4, 13, 13], fill=hexc('#A8F0D8')); d.ellipse([5, 6, 8, 9], fill=hexc('#EFFFF8')); d.polygon([(3, 10), (2, 14), (6, 12)], fill=hexc('#A8F0D8'))
def i_silk(d):
    d.ellipse([3, 3, 13, 13], fill=hexc('#F4F2FA')); d.line([(4, 6), (12, 10)], fill=hexc('#D0CAE4')); d.line([(4, 10), (12, 6)], fill=hexc('#D0CAE4')); d.line([(8, 3), (8, 13)], fill=hexc('#D0CAE4'))
def i_feather(d):
    d.polygon([(11, 2), (13, 4), (6, 13), (3, 14), (4, 11)], fill=hexc('#C89A6C')); d.line([(12, 3), (3, 14)], fill=hexc('#F2E2C4'))
def i_pseed(d):
    for x, y in ((3, 4), (8, 3), (5, 9), (10, 8)): d.ellipse([x, y, x + 4, y + 5], fill=hexc('#F6E6C0')); d.point((x + 1, y + 1), fill=hexc('#FFFFFF'))
ic_old = Image.open(os.path.join(R, 'icons.png')).convert('RGBA')
N0 = 38                                # 기존 아이콘 수 (ICONS 목록 길이)
new_icons = [icon(f) for f in (i_whisker, i_batdust, i_ecto, i_silk, i_feather, i_pseed)]
ic_new = Image.new('RGBA', (32 * (N0 + len(new_icons)), 32), (0, 0, 0, 0)); ic_new.paste(ic_old.crop((0, 0, 32 * N0, 32)), (0, 0))
for i, im in enumerate(new_icons): ic_new.paste(im, (32 * (N0 + i), 0))
ic_new.save(os.path.join(R, 'icons.png'))
print('creatures', world.size, 'icons', ic_new.size)
