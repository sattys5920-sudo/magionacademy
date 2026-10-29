# 아기 동물 가구 36종(out/baby_furn.png · .json)을 방 가구(world.js FURN + art/iso/furn.png)에 더하고, 아기 동물·수레 그림을 art/로 옮겨요. 여러 번 돌려도 같은 결과
import hashlib, json, os, re, shutil
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ATLAS = '../../public/art/iso/furn.png'; WJ = '../../public/world.js'; ART = '../../public/art/'
s = open(WJ).read(); i = s.index('const FURN = ') + len('const FURN = ')
FURN, end = json.JSONDecoder().raw_decode(s[i:])
FURN['items'] = [x for x in FURN['items'] if 'baby' not in x]          # 다시 돌리면 새로 그려요
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2
atlas = atlas.crop((0, 0, x0, atlas.height))
sh = Image.open('out/baby_furn.png').convert('RGBA'); meta = json.load(open('out/baby_furn.json'))
W = x0 + sh.width; H = max(atlas.height, sh.height); grown = Image.new('RGBA', (W, H), (0, 0, 0, 0)); grown.alpha_composite(atlas, (0, H - atlas.height if False else 0)); grown.alpha_composite(sh, (x0, 0)); atlas = grown
for m in meta:
    FURN['items'].append({**{k: m[k] for k in ('id', 'name', 'cat', 'price', 'pts', 'w', 'd', 'solid', 'flat', 'sw', 'sh', 'ax', 'ay', 'baby', 'spot', 'pose')}, 'sx': x0 + m['sx'], 'ev': 0})
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]; open(WJ, 'w').write(s)
for f in ('babies', 'cart_up', 'cart_tilt', 'cart_fall', 'cart_tarp', 'cart_puff', 'cart_shadows'): shutil.copy(f'out/{f}.png', ART + f + '.png')
shutil.copy('out/cart.json', ART + 'cart.json')
print('furn items', len(FURN['items']), atlas.size)
