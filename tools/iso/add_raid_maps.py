# 레이드: 한밤 도서관의 이상한 거울 · 거울 너머 구역을 게임에 넣어요 (raid_mirror.py 그림 → public/art/iso, world.js MAPS)
#   python3 tools/iso/raid_mirror.py && python3 tools/iso/add_raid_maps.py
#   도서관 그림은 그대로 두고, 레이드가 열리면 index.html이 빛나는 거울 그림(library_mg_bg)으로 바꿔 끼워요 (World.setMapBg)
#   도서관 거울 문: (17,0) · lock 'raid' (열리기 전에는 아무 일도 없어요) / 거울 너머 나가는 곳: (20,21) · lock 'raidback' (거울 통과 연출)
import json, os, hashlib, shutil
from PIL import Image
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(I)); ART = ROOT + '/public/art/iso/'; WJ = ROOT + '/public/world.js'
def webp(p): Image.open(p).save(p[:-4] + '.webp', 'WEBP', lossless=True, quality=100, method=6)
def ver(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
for src, dst in (('library_mg_bg', 'library_mg_bg'), ('mirrorland_bg', 'mirrorland_bg'), ('mirrorland_obj', 'mirrorland_obj')):
    p = ART + dst + '.png'; shutil.copy(I + '/out/%s.png' % src, p); webp(p)
s = open(WJ).read(); a = s.index('const MAPS = ') + len('const MAPS = '); b = s.index('}};\n', a) + 2
M = json.loads(s[a:b])
d = json.load(open(I + '/out/mirrorland.json'))
for o in d['objs']:
    if o.get('door'): o['door']['spawn'] = [17, 1]
d.update(bgSrc='art/iso/mirrorland_bg.png?v=' + ver(ART + 'mirrorland_bg.png'), objSrc='art/iso/mirrorland_obj.png?v=' + ver(ART + 'mirrorland_obj.png'), lazy=True, indoor=True, night=True, spawnIn=[20, 20])
M['mirrorland'] = {'meta': d}
L = M['library']['meta']; L['objs'] = [o for o in L['objs'] if o['name'] != 'raidmirror']
L['objs'].append(dict(name='raidmirror', box=[17, 0, 18, 1], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, solid=False, act=None, door=dict(tile=[17, 0], to='mirrorland', label='이상한 거울', spawn=[20, 20], lock='raid', back=[17, 1])))
L['raidBg'] = 'art/iso/library_mg_bg.png?v=' + ver(ART + 'library_mg_bg.png')
s = s[:a] + json.dumps(M, ensure_ascii=False) + s[b:]
open(WJ, 'w').write(s)
print('ok', d['bgSrc'], L['raidBg'], len(d['objs']))
