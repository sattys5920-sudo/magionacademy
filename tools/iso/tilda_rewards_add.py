# 수상한 기척(마틸다) 보상을 게임에 넣어요: 방 가구 「빛바랜 졸업 사진」(world.js FURN + art/iso/furn.png) · 모자 「마틸다의 졸업 모자」(AVM hat · art/lpc/hat_grad.png)
#   먼저 python3 ghost_rewards.py (out/ghost_photo.png 등) · python3 lpc/grad_cap.py <LPC> (out/hat_grad.png) 를 돌려 두세요
import hashlib, json, os, re, shutil
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from interiors import Room
import ghost_rewards as G
WJ = '../../public/world.js'; ATLAS = '../../public/art/iso/furn.png'
s = open(WJ).read()
# 1) 가구
i = s.index('const FURN = ') + len('const FURN = '); FURN, end = json.JSONDecoder().raw_decode(s[i:])
FURN['items'] = [x for x in FURN['items'] if not x.get('tilda')]
R = Room(6, 6, 60); R.obj('tl_photo', [(1, 1)], lambda img, d: G.photo(R, img, d)); o = R.objs[-1]; ax, ay = R.P(1, 1); ph = o['img']
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2; atlas = atlas.crop((0, 0, x0, atlas.height))
W = x0 + ph.width; H = max(atlas.height, ph.height); g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g.alpha_composite(atlas, (0, 0)); g.alpha_composite(ph, (x0, 0)); atlas = g
FURN['items'].append({'id': 'tl_photo', 'name': '빛바랜 졸업 사진', 'cat': '추억', 'w': 1, 'd': 1, 'solid': 1, 'flat': 0, 'sw': ph.width, 'sh': ph.height, 'ax': round(ax - o['x']), 'ay': round(ay - o['y']), 'price': 0, 'pts': 2, 'sx': x0, 'ev': 1, 'tilda': 1})
atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)
h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]
# 2) 모자
src = 'out/hat_grad.png'; dst = '../../public/art/lpc/hat_grad.png'; shutil.copy(src, dst); Image.open(dst).save(dst.replace('.png', '.webp'), lossless=True)
hv = hashlib.md5(open(dst, 'rb').read()).hexdigest()[:8]
i = s.index('const AVM = ') + len('const AVM = '); AVM, end = json.JSONDecoder().raw_decode(s[i:])
AVM['parts']['hat'] = [x for x in AVM['parts']['hat'] if x['id'] != 'hat_grad'] + [{'id': 'hat_grad', 'n': '마틸다의 졸업 모자', 'f': f'art/lpc/hat_grad.png?v={hv}', 'L': {'female': [[0, 130, []]], 'male': [[0, 130, []]]}, 'k': 'ev'}]
s = s[:i] + json.dumps(AVM, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]
open(WJ, 'w').write(s); print('ok', len(FURN['items']), atlas.size, hv)
