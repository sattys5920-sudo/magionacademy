# 누비 엔딩 보상 가구 「작은 누비 인형」(고쳐진 누비 + 리본 · 분홍 쿠션 위)을 방 가구(world.js FURN + art/iso/furn.png)에 더해요 · 가게에는 안 나와요 (ev)
import hashlib, json, os, re
import numpy as np
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ATLAS = '../../public/art/iso/furn.png'; WJ = '../../public/world.js'
s = open(WJ).read(); i = s.index('const FURN = ') + len('const FURN = ')
FURN, end = json.JSONDecoder().raw_decode(s[i:])
FURN['items'] = [x for x in FURN['items'] if x.get('id') != 'nubidoll']
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2
atlas = atlas.crop((0, 0, x0, atlas.height))
# 그림: 누비 (고쳐진 + 리본 앞) 를 쿠션 위에
nb = Image.open('../../public/art/nubi_s.png').convert('RGBA').crop((256 + 8, 10, 256 + 24, 32))   # 16×22
spr = Image.new('RGBA', (22, 26), (0, 0, 0, 0)); px = spr.load()
for y in range(19, 26):
    for x in range(1, 21):
        if ((x - 10.5) / 10) ** 2 + ((y - 22.5) / 3.5) ** 2 <= 1: px[x, y] = (232, 160, 176, 255) if y < 23 else (200, 120, 140, 255)
spr.alpha_composite(nb, (3, 0))
a = np.array(spr); m = a[..., 3] > 0; o = a.copy()
for y in range(a.shape[0]):
    for x in range(a.shape[1]):
        if not m[y, x] and any(0 <= y + dy < a.shape[0] and 0 <= x + dx < a.shape[1] and m[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))): o[y, x] = (42, 26, 34, 255)
spr = Image.fromarray(o)
W = x0 + spr.width; H = max(atlas.height, spr.height); grown = Image.new('RGBA', (W, H), (0, 0, 0, 0)); grown.alpha_composite(atlas, (0, 0)); grown.alpha_composite(spr, (x0, 0)); atlas = grown
FURN['items'].append({'id': 'nubidoll', 'name': '작은 누비 인형', 'cat': '인형', 'w': 1, 'd': 1, 'solid': 0, 'flat': 0, 'sw': spr.width, 'sh': spr.height, 'ax': 11, 'ay': 22, 'price': 0, 'pts': 3, 'sx': x0, 'ev': 1})
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]; open(WJ, 'w').write(s)
print('furn items', len(FURN['items']), atlas.size)
