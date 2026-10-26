# 유령 등불 장식 12색을 방 가구(world.js FURN + art/iso/furn.png)에 더해요. 여러 번 돌려도 같은 결과(이미 있으면 건너뜀)
import hashlib, json, os, re
import numpy as np
from scipy import ndimage
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ATLAS = '../../public/art/iso/furn.png'; WJ = '../../public/world.js'; ART = '../../public/art/'
names = json.load(open('ev4_src/lamp_names.json'))
s = open(WJ).read(); i = s.index('const FURN = ') + len('const FURN = ')
FURN, end = json.JSONDecoder().raw_decode(s[i:])
have = {x['id'] for x in FURN['items']}
SW, SH = 24, 30
atlas = Image.open(ATLAS).convert('RGBA'); x0 = max(x['sx'] + x['sw'] for x in FURN['items']) + 2
new = [(k, n) for k, n in enumerate(names) if f'ghostlamp{k}' not in have]
if new:
    W = max(atlas.width, x0 + len(new) * (SW + 2)); grown = Image.new('RGBA', (W, max(atlas.height, SH)), (0, 0, 0, 0)); grown.alpha_composite(atlas, (0, 0)); atlas = grown
    for j, (k, n) in enumerate(new):
        im = Image.open(ART + f'ev4_lamp_{k:02d}.png').convert('RGBA'); a = np.array(im); a[a[..., 3] < 200, 3] = 0       # 바닥 빛과 흐린 가장자리를 빼요
        mx_, mn_ = a[..., :3].max(2).astype(int), a[..., :3].min(2).astype(int); sat_ = (mx_ - mn_) / np.maximum(mx_, 1); rows_ = np.arange(a.shape[0])[:, None] >= int(a.shape[0] * .74); a[rows_ & (sat_ < .38), 3] = 0   # 바닥 빛 점선 무늬 제거
        lab, nlab = ndimage.label(a[..., 3] > 0); big = 1 + int(np.argmax(ndimage.sum(a[..., 3] > 0, lab, range(1, nlab + 1)))); a[lab != big, 3] = 0   # 몸통만 남겨요(작은 반짝이 제외)
        im = Image.fromarray(a, 'RGBA'); im = im.crop(im.getbbox())
        k_ = min(SW / im.width, SH / im.height); im = im.resize((max(1, round(im.width * k_)), max(1, round(im.height * k_))), Image.BOX)
        b = np.array(im); b[..., 3] = np.where(b[..., 3] > 110, 255, 0); q = Image.fromarray(b[..., :3]).quantize(14, dither=Image.NONE).convert('RGB'); b[..., :3] = np.array(q); im = Image.fromarray(b, 'RGBA')   # 도트답게 색을 줄여요
        sx = x0 + j * (SW + 2); atlas.alpha_composite(im, (sx + (SW - im.width) // 2, SH - im.height))
        FURN['items'].append({'id': f'ghostlamp{k}', 'name': f'유령 등불 ({n})', 'cat': '이벤트', 'price': 0, 'pts': 3, 'w': 1, 'd': 1, 'solid': 1, 'flat': 0, 'sw': SW, 'sh': SH, 'ax': SW // 2, 'ay': SH - 5, 'sx': sx, 'ev': 1})
    atlas.save(ATLAS); atlas.save(ATLAS.replace('.png', '.webp'), lossless=True)   # 게임은 웹피 그림을 먼저 써요
    h = hashlib.md5(open(ATLAS, 'rb').read()).hexdigest()[:8]; FURN['src'] = re.sub(r'\?v=\w+', '?v=' + h, FURN['src'])
    s = s[:i] + json.dumps(FURN, ensure_ascii=False, separators=(', ', ': ')) + s[i + end:]; open(WJ, 'w').write(s)
print('furn items', len(FURN['items']), 'added', len(new))
