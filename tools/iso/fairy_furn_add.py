# 요정 가구 3종(out/fairy_furn.png · .json)을 방 가구(world.js FURN + art/iso/furn.png)에 더해요. 가게에는 안 나오고(ev) 요정 시장에서 단골 선물로 받아요. 여러 번 돌려도 같은 결과
import hashlib, json, os, re
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ATLAS = '../../public/art/iso/furn.png'; WJ = '../../public/world.js'
s = open(WJ).read(); i = s.index('const FURN = ') + len('const FURN = ')
FURN, end = json.JSONDecoder().raw_decode(s[i:])
old = [x for x in FURN['items'] if 'fairy' in x]
FURN['items'] = [x for x in FURN['items'] if 'fairy' not in x]
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2
atlas = atlas.crop((0, 0, x0, atlas.height))
sh = Image.open('out/fairy_furn.png').convert('RGBA'); meta = json.load(open('out/fairy_furn.json'))
W = x0 + sh.width; H = max(atlas.height, sh.height); grown = Image.new('RGBA', (W, H), (0, 0, 0, 0)); grown.alpha_composite(atlas, (0, 0)); grown.alpha_composite(sh, (x0, 0)); atlas = grown
for m in meta:
    FURN['items'].append({**{k: m[k] for k in ('id', 'name', 'cat', 'w', 'd', 'solid', 'flat', 'sw', 'sh', 'ax', 'ay', 'fairy')}, 'price': 0, 'pts': 2, 'sx': x0 + m['sx'], 'ev': 1})
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]; open(WJ, 'w').write(s)
print('furn items', len(FURN['items']), atlas.size)
