# 걸어 다니는 세계: hw.json(학교+마을) + pclass.json(물약 교실) + interiors.py 방들 + world_tpl.js → public/world.js
# 게임 화면은 public/index.html에 있고, 세계와는 window.World로 이어져요.
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/world.js'
camp = json.load(open(I + '/out/hw.json'))
camp.update(bgSrc='art/iso/hw_bg.png', objSrc='art/iso/hw_obj.png', title='호박달 마녀학교', sub='반짝이는 곳이 문이에요', fill='#140E1E')
L = json.load(open(I + '/out/pclass.json'))
L.update(indoor=True, spawnIn=[9, 12], vw=185, fill='#0C0715', bgSrc='art/iso/pclass_bg.png', objSrc='art/iso/pclass_obj.png', title='물약 교실', sub='본관 1층 · 반짝이는 곳으로 나가요')
MAPS = {'campus': {'meta': camp}, 'lab': {'meta': L}}
for k in ('candy', 'craft', 'dorm_witch', 'dorm_vamp', 'dorm_wolf', 'dorm_ghost', 'toxic'):
    MAPS[k] = {'meta': json.load(open(I + '/out/%s.json' % k))}
# 기숙사 건물 = 게임의 네 기숙사 (마녀관 Emberkiln, 뱀파이어관 Moonhollow, 늑대관 Duskfold, 유령관 Dewmorn)
DORM = {'dorm_witch': ('ember', 'Emberkiln 기숙사', '마녀관'), 'dorm_vamp': ('moon', 'Moonhollow 기숙사', '뱀파이어관'),
        'dorm_wolf': ('dusk', 'Duskfold 기숙사', '늑대관'), 'dorm_ghost': ('dew', 'Dewmorn 기숙사', '유령관')}
for k, (house, name, hall) in DORM.items():
    MAPS[k]['meta'].update(title=name, sub=hall + ' · 침대에서 자고 내일로', house=house)
    for o in MAPS[k]['meta']['objs']:
        if o['act'] and o['act'][1] == '잠자고 내일로': o['act'][0] = '기숙사 침대'
    for o in camp['objs']:
        if o['door'] and o['door']['to'] == k: o['door']['label'] = name
for a in camp['areas']:
    if a['n'] == '기숙사': a['n'] = '기숙사 네 동'
t = open(I + '/world_tpl.js').read().replace('__MAPS__', json.dumps(MAPS, ensure_ascii=False))
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
