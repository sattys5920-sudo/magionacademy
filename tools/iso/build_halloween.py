# 걸어 다니는 세계: hw.json(학교+마을) + pclass.json(물약 교실) + interiors.py·dorms.py 방들 + furniture.py 가구 + world_tpl.js → public/world.js
# 게임 화면은 public/index.html에 있고, 세계와는 window.World로 이어져요.
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/world.js'
camp = json.load(open(I + '/out/hw.json'))
camp.update(bgSrc='art/iso/hw_bg.png', objSrc='art/iso/hw_obj.png', title='호박달 마녀학교', sub='반짝이는 곳이 문이에요', fill='#140E1E')
L = json.load(open(I + '/out/pclass.json'))
L.update(indoor=True, spawnIn=[9, 12], vw=185, fill='#0C0715', bgSrc='art/iso/pclass_bg.png', objSrc='art/iso/pclass_obj.png', title='물약 교실', sub='본관 1층 · 반짝이는 곳으로 나가요')
MAPS = {'campus': {'meta': camp}, 'lab': {'meta': L}}
for k in ('candy', 'craft', 'toxic', 'barn', 'pen'):
    MAPS[k] = {'meta': json.load(open(I + '/out/%s.json' % k))}
# 기숙사 휴게실 (dorms.py): 4곳 × 6단계, 개인 방·복도 4개씩. 들어갈 때 불러와요 (lazy)
DK = ('witch', 'vamp', 'wolf', 'ghost')
for kd in DK:
    for n in range(1, 7): MAPS['dorm_%s_%d' % (kd, n)] = {'meta': dict(json.load(open(I + '/out/dorm_%s_%d.json' % (kd, n))), lazy=True)}
    for pre in ('myroom_', 'hall_'): MAPS[pre + kd] = {'meta': dict(json.load(open(I + '/out/%s%s.json' % (pre, kd))), lazy=True)}
# 기숙사 건물 = 게임의 네 기숙사 (마녀관 Emberkiln, 뱀파이어관 Moonhollow, 늑대관 Duskfold, 유령관 Dewmorn)
DORM = {'dorm_witch': ('ember', 'Emberkiln 기숙사', '마녀관'), 'dorm_vamp': ('moon', 'Moonhollow 기숙사', '뱀파이어관'),
        'dorm_wolf': ('dusk', 'Duskfold 기숙사', '늑대관'), 'dorm_ghost': ('dew', 'Dewmorn 기숙사', '유령관')}
for k, (house, name, hall) in DORM.items():
    for n in range(1, 7): MAPS['%s_%d' % (k, n)]['meta'].update(title=name.replace('기숙사', '휴게실'), sub='%s · %d단계 · 게시판에서 함께 꾸며요' % (hall, n))
    for o in camp['objs']:
        if o['door'] and o['door']['to'] == k: o['door']['label'] = name
for a in camp['areas']:
    if a['n'] == '기숙사': a['n'] = '기숙사 네 동'
AV = json.load(open(I + '/out/avatar_parts.json'))   # chars4.py
# png는 1년 동안 캐시돼요 → 내용이 바뀌면 주소도 바뀌게 ?v=해시 를 붙여요
import hashlib
def ver(src): return src + '?v=' + hashlib.md5(open(I + '/out/' + src.split('/')[-1], 'rb').read()).hexdigest()[:8]
for m in MAPS.values(): m['meta']['bgSrc'] = ver(m['meta']['bgSrc']); m['meta']['objSrc'] = ver(m['meta']['objSrc'])
AV['src'] = ver(AV['src'])
FURN = dict(src=ver('art/iso/furn.png'), items=json.load(open(I + '/out/furn.json')))   # furniture.py
PUB = os.path.dirname(os.path.abspath(OUT))
CR = 'art/iso/creatures_w.png'; CR += '?v=' + hashlib.md5(open(os.path.join(PUB, CR), 'rb').read()).hexdigest()[:8]
t = open(I + '/world_tpl.js').read().replace('__MAPS__', json.dumps(MAPS, ensure_ascii=False)).replace('__AVATAR__', json.dumps(AV, ensure_ascii=False)).replace('__CRSRC__', json.dumps(CR)).replace('__FURN__', json.dumps(FURN, ensure_ascii=False))
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
