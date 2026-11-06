# 시계탑 꼭대기 방(도도의 경매장)을 게임에 넣어요: 그림 → public/art/iso, world.js MAPS.clock_roof, 교정 시계탑 사다리 문
#   python3 tools/iso/dodo_roof.py && python3 tools/iso/clock_ladder.py && python3 tools/iso/add_clock_roof.py
#   교정: 시계탑(본관 왼쪽 끝 뾰족탑) 앞 (37,36)에 사다리 그림 (index.html clockLadder) · 문 칸 (37,37) → 꼭대기 방 (6,8)
#   꼭대기 방: 앞 가운데 사다리 구멍 (6,9) → 교정 (37,38)
import json, os, hashlib, shutil
from PIL import Image
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(I)); ART = ROOT + '/public/art/iso/'; WJ = ROOT + '/public/world.js'
def webp(p): Image.open(p).save(p[:-4] + '.webp', 'WEBP', lossless=True, quality=100, method=6)
def ver(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
for sfx in ('_bg', '_obj'):
    p = ART + 'clock_roof' + sfx + '.png'; shutil.copy(I + '/out/clock_roof%s.png' % sfx, p); webp(p)
p = ROOT + '/public/art/clock_ladder.png'; shutil.copy(I + '/out/clock_ladder_long.png', p); webp(p)
s = open(WJ).read(); a = s.index('const MAPS = ') + len('const MAPS = '); b = s.index('}};\n', a) + 2
M = json.loads(s[a:b])
d = json.load(open(I + '/out/clock_roof.json'))
for o in d['objs']:
    if o.get('door'): o['door'].update(spawn=[37, 38], label='사다리로 내려가기')
d.update(bgSrc='art/iso/clock_roof_bg.png?v=' + ver(ART + 'clock_roof_bg.png'), objSrc='art/iso/clock_roof_obj.png?v=' + ver(ART + 'clock_roof_obj.png'), lazy=True)
M['clock_roof'] = {'meta': d}
C = M['campus']['meta']; C['objs'] = [o for o in C['objs'] if o['name'] != 'clockladder']
C['objs'].append(dict(name='clockladder', box=[37, 37, 38, 38], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, solid=False, act=None,
                      door=dict(tile=[37, 37], to='clock_roof', label='시계탑 사다리', spawn=[6, 8])))
s = s[:a] + json.dumps(M, ensure_ascii=False) + s[b:]
open(WJ, 'w').write(s)
print('ok', d['bgSrc'])
