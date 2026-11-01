# 겨울 뜨개질을 게임에 넣어요: 뜨개 목도리 아바타 부품(neck_knit · 두 색 줄무늬 · 뜨개 결) + 방 가구 「뜨개 바구니」 + NPC 뜨개 인형 10 종(그림은 게임이 저장한 생김새로 그때그때 만들어요)
#   python3 tools/iso/knit_add.py   (다시 돌려도 같은 결과)
import hashlib, json, os, re
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from interiors import Room
from furniture import bx, C, ell, H
from fairy_furn import sparkle
WJ = '../../public/world.js'; LPC = '../../public/art/lpc'; ATLAS = '../../public/art/iso/furn.png'
s = open(WJ).read()
i = s.index('const AVM = ') + 12; AVM, end = json.JSONDecoder().raw_decode(s[i:])
WHITE = [tuple(int(h[k:k + 2], 16) for k in (1, 3, 5)) for h in AVM['pal']['cloth']['white']]
# 1) 뜨개 목도리: 게임 목도리(neck_004)를 줄무늬 두 층으로 나눠요 (0 줄 = 첫째 색 · 1 줄 = 둘째 색) · 흰색 단계 안에서 V 모양 뜨개 결
src = Image.open(os.path.join(LPC, 'neck_004.png')).convert('RGBA'); W, Hh = src.size
out = Image.new('RGBA', (W, Hh * 2), (0, 0, 0, 0)); P = src.load(); Q = out.load()
for y in range(Hh):
    for x in range(W):
        c = P[x, y]
        if not c[3]: continue
        rgb = c[:3]; k = min(range(len(WHITE)), key=lambda j: sum((rgb[t] - WHITE[j][t]) ** 2 for t in range(3)))
        lx = x % 64
        if k >= 2 and ((lx % 2 == 0 and y % 2 == 0) or (lx % 2 == 1 and y % 2 == 1 and (lx + y) % 4 == 2)): k -= 1
        col = WHITE[k] + (c[3],); row = 0 if (lx // 2 + y // 3) % 2 == 0 or k == 0 else 1
        Q[x, y + row * Hh] = col
        if k == 0: Q[x, y + Hh] = col   # 테두리는 두 층 다
out.save(os.path.join(LPC, 'neck_knit.png')); out.save(os.path.join(LPC, 'neck_knit.webp'), lossless=True)
hv = hashlib.md5(open(os.path.join(LPC, 'neck_knit.png'), 'rb').read()).hexdigest()[:8]
AVM['parts']['neck'] = [x for x in AVM['parts']['neck'] if x['id'] != 'neck_knit'] + [{'id': 'neck_knit', 'n': '뜨개 목도리', 'f': f'art/lpc/neck_knit.png?v={hv}', 'L': {b: [[0, 90, [['neck', 'white']]], [1, 90, [['neck2', 'white']]]] for b in ('female', 'male')}, 'k': 'ev', 'p': 0}]
s = s[:i] + json.dumps(AVM, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]
# 2) 가구: 뜨개 바구니 + 인형 10 종(빈 칸 · 게임이 그림을 넣어요)
i = s.index('const FURN = ') + len('const FURN = '); FURN, end = json.JSONDecoder().raw_decode(s[i:])
FURN['items'] = [x for x in FURN['items'] if not x.get('knit')]
def basket(R, img, d):   # 등나무 바구니 · 털실 뭉치 셋 · 꽂힌 바늘 두 개 · 늘어진 실
    x, y = C(R, 1.5, 1.5); x, y = int(x), int(y); d = ImageDraw.Draw(img)
    d.ellipse([x - 11, y - 9, x + 11, y + 3], fill=H('#2A1A10')); d.rectangle([x - 11, y - 14, x + 11, y - 3], fill=H('#2A1A10'))
    d.ellipse([x - 10, y - 8, x + 10, y + 2], fill=H('#9A6A3A')); d.rectangle([x - 10, y - 13, x + 10, y - 3], fill=H('#B8844A'))
    for xx in range(x - 9, x + 10, 3): d.line([(xx, y - 13), (xx, y - 2)], fill=H('#8A5A2E'))
    for yy in range(y - 12, y - 3, 3): d.line([(x - 10, yy), (x + 10, yy)], fill=H('#C89A5A'))
    d.ellipse([x - 10, y - 17, x + 10, y - 9], fill=H('#2A1A10')); d.ellipse([x - 9, y - 16, x + 9, y - 10], fill=H('#6A4424'))
    for (cx, cy, c1, c2) in ((x - 4, y - 16, '#E0505A', '#F08A8A'), (x + 4, y - 17, '#F4F0E8', '#FFFFFF'), (x, y - 20, '#5A8AE0', '#8AB0F0')):
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=H('#1a1024')); d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=H(c1)); d.arc([cx - 3, cy - 3, cx + 3, cy + 3], 200, 320, fill=H(c2))
    d.line([(x + 2, y - 30), (x + 7, y - 14)], fill=H('#1a1024'), width=3); d.line([(x + 2, y - 30), (x + 7, y - 14)], fill=H('#E8DCC0'), width=1)
    d.line([(x + 8, y - 29), (x + 5, y - 14)], fill=H('#1a1024'), width=3); d.line([(x + 8, y - 29), (x + 5, y - 14)], fill=H('#E8DCC0'), width=1)
    d.line([(x - 4, y - 12), (x - 12, y - 4), (x - 14, y + 2)], fill=H('#E0505A'), width=1)
    sparkle(d, x + 12, y - 24, '#FFF0B0')
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2; atlas = atlas.crop((0, 0, x0, atlas.height))
R = Room(6, 6, 60); R.obj('kn_basket', [(1, 1)], lambda img, d: basket(R, img, d)); o = R.objs[-1]; ax, ay = R.P(1, 1); ph = o['img']
blank = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
W2 = x0 + ph.width + 2 + 40; H2 = max(atlas.height, ph.height, 40); g = Image.new('RGBA', (W2, H2), (0, 0, 0, 0)); g.alpha_composite(atlas, (0, 0)); g.alpha_composite(ph, (x0, 0)); atlas = g
FURN['items'].append({'id': 'kn_basket', 'name': '뜨개 바구니', 'cat': '뜨개', 'w': 1, 'd': 1, 'solid': 1, 'flat': 0, 'sw': ph.width, 'sh': ph.height, 'ax': round(ax - o['x']), 'ay': round(ay - o['y']), 'price': 0, 'pts': 2, 'sx': x0, 'ev': 1, 'knit': 1})
bx0 = x0 + ph.width + 2
DOLLS = [('leo', '레오'), ('sera', '세라 선생님'), ('madeleine', '마들렌'), ('stella', '스텔라'), ('nabi', '나비'), ('batri', '배트리'), ('kappa', '캇파'), ('aula', '아울라'), ('mandi', '맨디'), ('jipsin', '스트로'), ('otumo', '오투모')]
for nid, nm in DOLLS:
    FURN['items'].append({'id': 'kn_doll_' + nid, 'name': nm + ' 뜨개 인형', 'cat': '뜨개', 'w': 1, 'd': 1, 'solid': 1, 'flat': 0, 'sw': 40, 'sh': 40, 'ax': 20, 'ay': 36, 'price': 0, 'pts': 2, 'sx': bx0, 'ev': 1, 'knit': 1, 'dyn': nid})
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]
open(WJ, 'w').write(s); ph.resize((ph.width * 4, ph.height * 4), Image.NEAREST).save('out/kn_basket_preview.png'); print('ok', hv, len(FURN['items']))
