# 시련의 언덕 지도를 게임에 넣어요 (tower_trial.py 그림 → public/art/iso, world.js MAPS) · 학교 문 소품 → public/art/tower_gate.png
#   python3 tower_trial.py && python3 add_trial_map.py
#   학교 쪽 문은 지도에 박지 않고 index.html 이 탑이 열렸을 때만 소품(World.setProps)으로 세워요 (북쪽 강가 71, 10)
import json, os, hashlib, shutil
from PIL import Image
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(I)); ART = ROOT + '/public/art/iso/'; WJ = ROOT + '/public/world.js'
def webp(p): Image.open(p).save(p[:-4] + '.webp', 'WEBP', lossless=True, quality=100, method=6)
def ver(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
for k in ('trialland_bg', 'trialland_obj'):
    p = ART + k + '.png'; shutil.copy(I + '/out/%s.png' % k, p); webp(p)
shutil.copy(I + '/out/trial_gate.png', ROOT + '/public/art/tower_gate.png')
s = open(WJ).read(); a = s.index('const MAPS = ') + len('const MAPS = '); b = s.index('}};\n', a) + 2
M = json.loads(s[a:b]); d = json.load(open(I + '/out/trialland.json'))
d.update(bgSrc='art/iso/trialland_bg.png?v=' + ver(ART + 'trialland_bg.png'), objSrc='art/iso/trialland_obj.png?v=' + ver(ART + 'trialland_obj.png'), lazy=True, indoor=True, night=False, spawnIn=[17, 17])
M['trialland'] = {'meta': d}
s = s[:a] + json.dumps(M, ensure_ascii=False) + s[b:]
open(WJ, 'w').write(s); print('ok', d['bgSrc'], len(d['objs']))
