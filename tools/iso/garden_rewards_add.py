# 창밖 정원 도감 보상 가구를 게임에 넣어요: 「손님 사진 액자」(10 종) · 「나무 새집」(20 종) → world.js FURN + art/iso/furn.png
#   python3 garden_rewards_add.py  (다시 돌려도 같은 칸을 새로 그려요) · 손님 그림은 ../garden_mock/gi_guests.png (garden_animals.py)
import hashlib, json, os, re
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from interiors import Room
from furniture import bx, C, ell, H
from fairy_furn import glow, sparkle
WJ = '../../public/world.js'; ATLAS = '../../public/art/iso/furn.png'
GU = Image.open('../garden_mock/gi_guests.png').convert('RGBA')
guest = lambda i, f=0: GU.crop((i * 28 + f * 14, 0, i * 28 + f * 14 + 14, 14))

def frame(R, img, d):   # 손님 사진 액자: 나무 이젤 위 초록 액자 · 안에 정원 사진(참새 · 수달)
    x, y = C(R, 1.5, 1.5); x, y = int(x), int(y); bx(R, img, 1.25, 1.25, .5, .5, 3, '#7A5232', top='#9A6A42'); d = ImageDraw.Draw(img)
    d.line([(x - 3, y - 3), (x - 6, y - 26)], fill=H('#6A4424')); d.line([(x + 3, y - 3), (x + 6, y - 26)], fill=H('#6A4424'))
    fx0, fy0, fx1, fy1 = x - 12, y - 38, x + 12, y - 15
    d.rectangle([fx0 - 1, fy0 - 1, fx1 + 1, fy1 + 1], fill=H('#2A1A10')); d.rectangle([fx0, fy0, fx1, fy1], fill=H('#5AA84A')); d.rectangle([fx0 + 1, fy0 + 1, fx1 - 1, fy1 - 1], fill=H('#8AD06A'))
    d.rectangle([fx0 + 3, fy0 + 3, fx1 - 3, fy1 - 3], fill=H('#BFE6F4'))   # 하늘
    d.rectangle([fx0 + 3, fy1 - 9, fx1 - 3, fy1 - 3], fill=H('#7AC85A')); d.line([(fx0 + 3, fy1 - 9), (fx1 - 3, fy1 - 9)], fill=H('#5AA84A'))   # 잔디
    d.rectangle([fx0 + 5, fy0 + 5, fx0 + 7, fy0 + 7], fill=H('#FFF3C8'))   # 해
    for (a, b) in ((fx1 - 6, fy1 - 10), (fx1 - 8, fy1 - 11)): d.point((a, b), fill=H('#FFD866'))
    img.alpha_composite(guest(0), (fx0 + 3, fy1 - 17)); img.alpha_composite(guest(12), (fx1 - 16, fy1 - 16))
    sparkle(d, fx1 + 3, fy0 - 2, '#FFF0B0')
    for (a, b) in ((fx0 - 1, fy0 - 1), (fx1 + 1, fy0 - 1), (fx0 - 1, fy1 + 1), (fx1 + 1, fy1 + 1)): d.point((a, b), fill=H('#FFD866'))   # 모서리 금빛 못

def house(R, img, d):   # 나무 새집: 기둥 위 빨간 지붕 새집 · 동그란 구멍 · 횃대에 파랑새 · 기둥에 작은 꽃
    x, y = C(R, 1.5, 1.5); x, y = int(x), int(y); bx(R, img, 1.3, 1.3, .4, .4, 2, '#6A4428', top='#8A5A34'); d = ImageDraw.Draw(img)
    d.rectangle([x - 1, y - 30, x + 1, y - 2], fill=H('#6A4428')); d.line([(x - 1, y - 30), (x - 1, y - 2)], fill=H('#8A5A34'))
    hx0, hy0, hx1, hy1 = x - 9, y - 48, x + 9, y - 30
    d.rectangle([hx0 - 1, hy0 - 1, hx1 + 1, hy1 + 1], fill=H('#2A1A10')); d.rectangle([hx0, hy0, hx1, hy1], fill=H('#C8884A')); d.rectangle([hx0, hy0, hx0 + 1, hy1], fill=H('#E0A060'))
    for yy in range(hy0 + 4, hy1, 4): d.line([(hx0, yy), (hx1, yy)], fill=H('#A8703A'))
    d.polygon([(hx0 - 4, hy0 + 2), (x, hy0 - 9), (hx1 + 4, hy0 + 2)], fill=H('#2A1A10')); d.polygon([(hx0 - 2, hy0 + 1), (x, hy0 - 7), (hx1 + 2, hy0 + 1)], fill=H('#C8443A')); d.line([(hx0 - 2, hy0 + 1), (x, hy0 - 7)], fill=H('#E8705A'))
    ell(d, x, hy0 + 7, 3, 3, '#2A1A10'); d.line([(x - 5, hy0 + 13), (x + 5, hy0 + 13)], fill=H('#6A4428'))   # 구멍 · 횃대
    img.alpha_composite(guest(2), (x - 1, hy0 + 1))   # 파랑새가 횃대에
    for (a, b, c) in ((x - 4, y - 8, '#FF8AB0'), (x + 3, y - 12, '#FFD866'), (x - 3, y - 16, '#B8A0FF')): d.rectangle([a, b, a + 1, b + 1], fill=H(c)); d.point((a, b + 2), fill=H('#5AA84A'))
    sparkle(d, hx1 + 4, hy0 - 4, '#FFF0B0')

s = open(WJ).read(); i = s.index('const FURN = ') + len('const FURN = '); FURN, end = json.JSONDecoder().raw_decode(s[i:])
FURN['items'] = [x for x in FURN['items'] if not x.get('garden')]
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2; atlas = atlas.crop((0, 0, x0, atlas.height))
for fid, nm, fn in (('gd_frame', '손님 사진 액자', frame), ('gd_house', '나무 새집', house)):
    R = Room(6, 6, 60); R.obj(fid, [(1, 1)], lambda img, d, fn=fn: fn(R, img, d)); o = R.objs[-1]; ax, ay = R.P(1, 1); ph = o['img']
    W = x0 + ph.width; Hh = max(atlas.height, ph.height); g = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); g.alpha_composite(atlas, (0, 0)); g.alpha_composite(ph, (x0, 0)); atlas = g
    FURN['items'].append({'id': fid, 'name': nm, 'cat': '정원', 'w': 1, 'd': 1, 'solid': 1, 'flat': 0, 'sw': ph.width, 'sh': ph.height, 'ax': round(ax - o['x']), 'ay': round(ay - o['y']), 'price': 0, 'pts': 2, 'sx': x0, 'ev': 1, 'garden': 1})
    ph.resize((ph.width * 4, ph.height * 4), Image.NEAREST).save(f'out/{fid}_preview.png'); x0 = W + 2
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]
open(WJ, 'w').write(s); print('ok', len(FURN['items']), atlas.size)
