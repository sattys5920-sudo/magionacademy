# 학교·마을을 둘로 나눈 뒤 옛 campus 좌표를 새 (지도, x, y)로 바꿔요 (한 번만 돌리는 이전 도구: python3 tools/split_data.py)
#   index.html의 NPC·FISH_GO 좌표, public/data/*/places.json
import json, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'iso')); import split_maps
HTML = os.path.join(os.path.dirname(__file__), '..', 'public', 'index.html')
s = open(HTML).read(); n0 = 0
def sub_npc(m):
    global n0; mp, x, y = split_maps.leg2new(int(m.group(1)), int(m.group(2))); n0 += 1
    return f"map: '{mp}', x: {x}, y: {y}"
s = re.sub(r"map: 'campus', x: (\d+), y: (\d+)", sub_npc, s)
def sub_fish(m):
    global n0; mp, x, y = split_maps.leg2new(int(m.group(2)), int(m.group(3))); n0 += 1
    return f"['{m.group(1)}', '{mp}', [{x}, {y}], {m.group(4)}]"
s = re.sub(r"\['([^']+)', 'campus', \[(\d+), (\d+)\], (\d+)\]", sub_fish, s)
open(HTML, 'w').write(s); print('index.html 바뀐 곳', n0)
for f in ('main',):   # npc places는 tools/npc_places.py가 새 좌표로 다시 만들어요
    p = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', f, 'places.json'); d = json.load(open(p)); k = 0
    for pl in d:
        if pl.get('map') != 'campus': continue
        mp, x, y = split_maps.leg2new(pl['x'], pl['y']); pl['map'], pl['x'], pl['y'] = mp, x, y
        if pl.get('bg'): pl['bg'] = list(split_maps.leg2new(pl['bg'][0], pl['bg'][1])[1:])
        k += 1
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1); print(p, '바뀐 곳', k)
