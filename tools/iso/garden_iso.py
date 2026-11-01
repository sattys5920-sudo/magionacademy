# 시안: 「손님이 찾아오는 정원」 쿼터뷰 그림 (방 가구와 같은 도구 · 같은 화풍) → ../garden_mock/gi_bg.png · gi_items.png · gi.json
#   마당 7×6 칸: 잔디 · 돌길 · 뒤쪽 생울타리와 나무 울타리 · 물건 6 (연못 · 등불 · 먹이 그루터기 · 그네 · 호박 의자 · 바람 종)
#   손님은 게임의 아기 동물 그림(art/babies.png)을 그대로 써요
import json, os, random
from PIL import Image, ImageDraw
from interiors import Room, hexc, shade
from furniture import bx, C, ell, H
from fairy_furn import glow, sparkle
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'garden_mock'); random.seed(5)
R = Room(7, 6, 26)
G = [hexc('#4E8A3E'), hexc('#5A9A46'), hexc('#46803A'), hexc('#62A24C')]
def grass(fx, fy):
    if 2.6 < fx < 4.1: return hexc('#A89878') if (int(fx * 4) + int(fy * 3)) % 5 else hexc('#968566')   # 돌길
    c = G[(int(fx * 3) * 7 + int(fy * 3) * 13) % 4]
    if random.random() < .015: return hexc('#FF9AC0') if random.random() < .5 else hexc('#FFF2A0')   # 작은 꽃
    return c
R.floor(grass)
def fence(u, v):   # 뒤쪽: 생울타리 위로 나무 울타리
    if v < 16:
        n = (u * 7 + v * 13) % 9; return shade(hexc('#2E5A2E'), .85 + n * .03) if n else hexc('#3E7A3A')
    if v < 25 and (u % 7 in (0, 1)): return hexc('#8A5A32') if u % 7 == 0 else hexc('#6A4428')
    if v in (18, 22): return hexc('#7A4E2A')
    return None
R.wall_fill('L', fence); R.wall_fill('R', fence)
for i in range(4): x, y = R.P(random.uniform(.5, 6.5), random.uniform(.5, 5.5)); R.put(x, y, hexc('#FFE070'))
items, meta = [], {}
def mk(k, draw, tile=(1, 1)):
    R.obj(k, [tile], lambda img, d: draw(img, d, tile), solid=False); o = R.objs.pop(); ax, ay = R.P(*tile)
    items.append(o['img']); meta[k] = dict(sw=o['img'].width, sh=o['img'].height, ax=round(ax - o['x']), ay=round(ay - o['y']))
def pond(img, d, t):
    x, y = C(R, t[0] + .5, t[1] + .5); ell(d, x, y, 13, 7, '#7A7A8A'); ell(d, x, y - 1, 11, 5.5, '#2E5A9A'); ell(d, x - 2, y - 2, 7, 3, '#4A7ABA'); d.line([(x - 6, y - 3), (x - 2, y - 3)], fill=H('#BFD8F4'))
    ell(d, x + 5, y, 3, 1.6, '#3A8A3A'); d.point((x + 5, y - 1), fill=H('#FF9AC0'))
    for a in ((-12, 1), (-8, 5), (6, 5), (11, -1), (-3, 6)): ell(d, x + a[0], y + a[1], 1.6, 1, '#9A9AA8')
def lamp(img, d, t):
    bx(R, img, t[0] + .4, t[1] + .4, .2, .2, 26, '#5A3A22'); x, y = C(R, t[0] + .5, t[1] + .5, 26); d = ImageDraw.Draw(img)
    d.rectangle([x - 4, y - 9, x + 4, y], fill=H('#3A2416')); d.rectangle([x - 3, y - 8, x + 3, y - 1], fill=H('#FFB848')); d.rectangle([x - 2, y - 7, x, y - 4], fill=H('#FFF0B0')); d.rectangle([x - 5, y - 11, x + 5, y - 9], fill=H('#2A1A10'))
    glow(img, x, y - 4, 16, '#FFD27A', 70)
def feeder(img, d, t):
    bx(R, img, t[0] + .25, t[1] + .25, .5, .5, 8, '#7A4E2A', top='#B8865A'); x, y = C(R, t[0] + .5, t[1] + .5, 8); d = ImageDraw.Draw(img)
    ell(d, x, y, 6, 3, '#5A3A22'); ell(d, x, y - .5, 5, 2.4, '#8A5A32')
    for a in ((-3, -1), (-1, 0), (1, -1), (3, 0), (0, -2), (2, -2)): d.point((x + a[0], y + a[1]), fill=H('#F0D070'))
def swing(img, d, t):
    for dx in (.1, .8): bx(R, img, t[0] + dx, t[1] + .45, .1, .1, 30, '#6A4428')
    a, b = C(R, t[0] + .15, t[1] + .5, 30), C(R, t[0] + .85, t[1] + .5, 30); d = ImageDraw.Draw(img); d.line([a, b], fill=H('#7A5232'), width=2)
    sa, sb = C(R, t[0] + .3, t[1] + .5, 10), C(R, t[0] + .7, t[1] + .5, 10)
    d.line([C(R, t[0] + .3, t[1] + .5, 29), sa], fill=H('#D8C8A0')); d.line([C(R, t[0] + .7, t[1] + .5, 29), sb], fill=H('#D8C8A0')); d.line([sa, sb], fill=H('#C8402A'), width=2)
def pumpkin(img, d, t):
    x, y = C(R, t[0] + .5, t[1] + .5, 6); ell(d, x, y, 9, 7, '#C85A14'); ell(d, x - 3, y - 1, 4, 6, '#E8782A'); ell(d, x + 3, y - 1, 4, 6, '#D86A1E'); d.line([(x, y - 6), (x, y + 6)], fill=H('#A84A10'))
    d.rectangle([x - 1, y - 10, x + 1, y - 7], fill=H('#3A6A2A')); d.point((x - 4, y - 3), fill=H('#FFB060'))
def bell(img, d, t):
    bx(R, img, t[0] + .42, t[1] + .42, .16, .16, 24, '#5A3A22'); x, y = C(R, t[0] + .5, t[1] + .5, 24); d = ImageDraw.Draw(img)
    d.line([(x, y), (x + 7, y - 2)], fill=H('#5A3A22'), width=2); bxx, byy = x + 7, y
    d.polygon([(bxx - 3, byy + 7), (bxx + 3, byy + 7), (bxx + 2, byy + 1), (bxx - 2, byy + 1)], fill=H('#4AA8B8')); d.line([(bxx - 1, byy + 2), (bxx - 1, byy + 6)], fill=H('#9AE0E8'))
    d.line([(bxx, byy + 8), (bxx + 1, byy + 12)], fill=H('#F0E8D0')); sparkle(d, bxx + 4, byy - 2, '#CFF4FF')
for k, f in (('pond', pond), ('lamp', lamp), ('feeder', feeder), ('swing', swing), ('pumpkin', pumpkin), ('bell', bell)): mk(k, f)
W = sum(i.width + 1 for i in items); Hh = max(i.height for i in items); sh = Image.new('RGBA', (W, Hh)); x = 0
for (k, m), im in zip(meta.items(), items): sh.alpha_composite(im, (x, Hh - im.height)); m['sx'] = x; m['ay'] += Hh - im.height; m['sh'] = Hh; x += im.width + 1
R.bg.save(os.path.join(OUT, 'gi_bg.png')); sh.save(os.path.join(OUT, 'gi_items.png'))
json.dump(dict(OX=R.OX, OY=R.OY, W=R.W, H=R.H, items=meta), open(os.path.join(OUT, 'gi.json'), 'w'))
# 미리보기: 물건을 놓고 아기 동물 몇 마리
pv = R.bg.copy(); BB = Image.open(os.path.join(HERE, '..', '..', 'public', 'art', 'babies.png')).convert('RGBA')
spots = {'pond': (1.6, 3.6), 'lamp': (1, 2), 'feeder': (5, 4), 'swing': (5, 1.4), 'pumpkin': (2, 5), 'bell': (5.6, 2.6)}
for k, (tx, ty) in spots.items():
    m = meta[k]; px, py = R.P(tx, ty); pv.alpha_composite(sh.crop((m['sx'], 0, m['sx'] + m['sw'], m['sh'])), (int(px - m['ax']), int(py - m['ay'])))
for i, (tx, ty) in ((10, (2.2, 4)), (4, (5.3, 4.5)), (6, (5.3, 1.6)), (8, (3.6, 2.4))):
    px, py = R.P(tx, ty); pv.alpha_composite(BB.crop((i * 14, 0, i * 14 + 14, 14)), (int(px - 7), int(py - 13)))
pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(os.path.join(OUT, 'gi_preview.png')); print('ok', R.W, R.H, meta)
