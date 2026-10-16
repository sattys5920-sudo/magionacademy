# walk.html 만들기: campus.json + lab.json + world_tpl.html → public/walk.html
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/walk.html'
camp = json.load(open(I + '/out/campus.json')); lab = json.load(open(I + '/out/lab.json'))
camp.update(bgSrc='art/iso/campus_bg.png', objSrc='art/iso/campus_obj.png', title='별빛 아카데미', sub='반짝이는 곳이 문이에요')
for o in camp['objs']:
    if o.get('door') and o['door'].get('to') == 'lab': o['door']['spawn'] = [5, 8]
L = dict(W=lab['W'], H=lab['H'], NX=lab['N'], NY=lab['N'], OX=lab['OX'], OY=lab['OY'], lights=lab['lights'], indoor=True,
         bgSrc='art/iso/lab_bg.png', objSrc='art/iso/lab_obj.png', title='물약 연구실', sub='본관 지하 · 반짝이는 곳으로 나가요', objs=[])
for o in lab['objs']:
    xs = [t[0] for t in o['tiles']]; ys = [t[1] for t in o['tiles']]
    L['objs'].append(dict(name=o['name'], box=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], sx=o['sx'], sy=0, sw=o['sw'], sh=o['sh'], x=o['x'], y=o['y'], door=None, solid=True))
L['objs'].append(dict(name='exit', box=[5, 9, 6, 10], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[5, 9], to='campus', label='별빛 아카데미', spawn=[16, 11]), solid=False))
t = open(I + '/world_tpl.html').read().replace('__MAPS__', json.dumps({'campus': {'meta': camp}, 'lab': {'meta': L}}, ensure_ascii=False))
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
