# 걸어 다니는 세계: hw.json(학교+마을) + pclass.json(물약 교실) + interiors.py·dorms.py 방들 + furniture.py 가구 + world_tpl.js → public/world.js
# 게임 화면은 public/index.html에 있고, 세계와는 window.World로 이어져요.
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/world.js'
camp = json.load(open(I + '/out/hw.json'))
camp.update(bgSrc='art/iso/hw_bg.png', objSrc='art/iso/hw_obj.png', title='호박달 마녀학교', sub='반짝이는 곳이 문이에요', fill='#140E1E')
L = json.load(open(I + '/out/pclass.json'))
L.update(indoor=True, spawnIn=[9, 12], vw=185, fill='#0C0715', bgSrc='art/iso/pclass_bg.png', objSrc='art/iso/pclass_obj.png', title='물약 교실', sub='본관 1층 · 반짝이는 곳으로 나가요')
Q = json.load(open(I + '/out/quarter.json'))   # quarter.py: 시장 거리 동쪽 끝에서 이어지는 의뢰인 마을 (들어갈 때 불러와요)
Q.update(bgSrc='art/iso/quarter_bg.png', objSrc='art/iso/quarter_obj.png', title='그림자 골목', sub='의뢰인들이 사는 마을 · 서쪽 문으로 시장에 돌아가요', fill='#140E1E', lazy=True)
A = json.load(open(I + '/out/arena.json'))     # arena.py: 놀이(호박 줍기 …)를 하는 전용 맵 (게임이 시작되면 이리로 와요)
A.update(bgSrc='art/iso/arena_bg.png', objSrc='art/iso/arena_obj.png', title='놀이 마당', sub='놀이가 끝나면 원래 자리로 돌아가요', fill='#140E1E', lazy=True)
town = json.load(open(I + '/out/town.json'))    # split_maps.py: 강 동쪽 마을·시장 (학교와 다리로 이어져요)
town.update(bgSrc='art/iso/town_bg.png', objSrc='art/iso/hw_obj.png', title='등불 마을', sub='반짝이는 곳이 문이에요 · 서쪽 다리로 학교에 가요', fill='#140E1E', lazy=True)
camp.update(sub='반짝이는 곳이 문이에요 · 동쪽 다리로 마을·시장에 가요')
QROOMS = {'vamp_manor': 'main_01_dracula', 'museum': 'main_05_mummy', 'lab_tower': 'main_06_frankenstein', 'witch_hut': 'main_03_witch', 'wolf_cabin': 'main_04_werewolf', 'jack_hut': 'main_07_jack'}   # quarter_rooms.py: 의뢰인 집 안
MAPS = {'campus': {'meta': camp}, 'town': {'meta': town}, 'lab': {'meta': L}, 'quarter': {'meta': Q}, 'arena': {'meta': A}}
DOORMAP = {tuple(map(int, k.split(','))): v for k, v in json.load(open(I + '/out/door_map.json')).items()}
ALLO, ALLA = camp['objs'] + town['objs'], camp['areas'] + town['areas']
for k in QROOMS: MAPS[k] = {'meta': dict(json.load(open(I + '/out/%s.json' % k)), lazy=True)}
for k in ('candy', 'craft', 'classroom', 'toxic', 'barn', 'pen'):
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
    for o in ALLO:
        if o['door'] and o['door']['to'] == k: o['door']['label'] = name
for o in ALLO:                          # 마을 '가면 가게' = 옷 가게 (index.html World.onLockedDoor)
    if o['door'] and o['door']['label'] == '가면 가게': o['door']['label'] = '옷 가게'
    if o['door'] and o['door']['label'] == '해골 잡화점': o['door']['label'] = '낚시 도구점'   # index.html World.onLockedDoor
OLDHOME = {'뱀파이어 저택': '뱀파이어 저택 별채', '마녀의 오두막': '마녀의 작은 오두막', '늑대인간 통나무집': '늑대인간 사냥 오두막'}
for o in ALLO:                          # 시장 쪽 옛 집들은 별채예요: 진짜 집은 그림자 골목 (quarter.py)
    if o['door'] and o['door']['label'] in OLDHOME: o['door']['note'] = '이곳은 별채예요. 진짜 집은 시장 동쪽 끝 「그림자 골목」에 있어요'; o['door']['label'] = OLDHOME[o['door']['label']]
for a in ALLA:
    if a['n'] in OLDHOME: a['n'] = OLDHOME[a['n']]
    if a['n'] == '늑대인간 집': a['n'] = '늑대인간 사냥 오두막'
    if a['n'] == '기숙사': a['n'] = '기숙사 네 동'
sys.path.insert(0, I); import split_maps
for m in MAPS.values():   # 안에서 학교·시장으로 나오는 문: 옛 좌표 → 새 (지도, 좌표)
    for o in m['meta'].get('objs', []):
        d = o.get('door')
        if not d or d.get('to') != 'campus' or not d.get('spawn') or m['meta'] is camp or m['meta'] is town: continue
        sx, sy = d['spawn']; hit = DOORMAP.get((sx, sy - 1))
        if hit: d['to'], d['spawn'] = hit[0], [hit[1], hit[2] + 1]
        else: mp, nx, ny = split_maps.leg2new(sx, sy); d['to'], d['spawn'] = mp, [nx, ny]
AV = json.load(open(I + '/out/lpc_meta.json'))   # lpc/build_lpc.py (LPC 캐릭터 부품)
# png는 1년 동안 캐시돼요 → 내용이 바뀌면 주소도 바뀌게 ?v=해시 를 붙여요
import hashlib
def ver(src): return src + '?v=' + hashlib.md5(open(I + '/out/' + src.split('/')[-1], 'rb').read()).hexdigest()[:8]
for m in MAPS.values():   # 침대: 하루 넘기기 대신 30분 쉬기 (index.html rest)
    for o in m['meta'].get('objs', []):
        if o.get('act') and o['act'][1] == '잠자고 내일로': o['act'] = [o['act'][0], '쉬기']
        if o.get('act') and o['act'][1] == '카라멜 젓기': o['act'] = ['요리 솥', '요리하기']   # 과자 교실 = 요리 (index.html renderCook)
        if o.get('act') and o['act'][1] == '과자 만들기': o['act'] = ['요리 조리대', '요리책 보기']
        if o.get('act') and o['act'][1] in ('솜사탕 만들기', '핼러윈 용품 만들기'): o['act'] = None   # 아직 없는 기능은 눌러도 반응이 없는 장식으로 둬요
for m in MAPS.values(): m['meta']['bgSrc'] = ver(m['meta']['bgSrc']); m['meta']['objSrc'] = ver(m['meta']['objSrc'])
_PUBD = os.path.join(I, '..', '..', 'public')
for ps in AV['parts'].values():                 # LPC 부품 그림 (public/art/lpc)
    for q in ps:
        if q.get('f'): q['f'] += '?v=' + hashlib.md5(open(os.path.join(_PUBD, q['f']), 'rb').read()).hexdigest()[:8]
FURN = dict(src=ver('art/iso/furn.png'), items=json.load(open(I + '/out/furn.json')))   # furniture.py
PUB = os.path.dirname(os.path.abspath(OUT))
CR = 'art/iso/creatures_w.png'; CR += '?v=' + hashlib.md5(open(os.path.join(PUB, CR), 'rb').read()).hexdigest()[:8]
t = open(I + '/world_tpl.js').read().replace('__MAPS__', json.dumps(MAPS, ensure_ascii=False)).replace('__AVATAR__', json.dumps(AV, ensure_ascii=False)).replace('__CRSRC__', json.dumps(CR)).replace('__FURN__', json.dumps(FURN, ensure_ascii=False))
open(OUT, 'w').write(t); print('wrote', OUT, len(t))

# 지도 그림(png + 무손실 webp)을 public/art/iso에 복사해요
from PIL import Image
for nm in ['hw_bg', 'town_bg', 'hw_obj', 'quarter_bg', 'quarter_obj'] + [k + sfx for k in QROOMS for sfx in ('_bg', '_obj')]:
    im = Image.open(I + '/out/%s.png' % nm); d = os.path.join(_PUBD, 'art', 'iso')
    im.save(os.path.join(d, nm + '.png')); im.save(os.path.join(d, nm + '.webp'), lossless=True)
