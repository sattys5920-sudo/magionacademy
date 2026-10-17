# walk.html (호박달 마녀학교): hw.json + lab.json(마녀 물약 교실) + halloween_tpl.html
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/walk.html'
camp = json.load(open(I + '/out/hw.json')); lab = json.load(open(I + '/out/lab.json'))
camp.update(bgSrc='art/iso/hw_bg.png', objSrc='art/iso/hw_obj.png', title='호박달 마녀학교', sub='반짝이는 곳이 문이에요', fill='#140E1E')
L = dict(W=lab['W'], H=lab['H'], NX=lab['N'], NY=lab['N'], OX=lab['OX'], OY=lab['OY'], lights=lab['lights'], indoor=True, vw=200, fill='#0C0715',
         bgSrc='art/iso/lab_bg.png', objSrc='art/iso/lab_obj.png', title='물약 교실', sub='본관 지하 · 반짝이는 곳으로 나가요', objs=[])
for o in lab['objs']:
    xs = [t[0] for t in o['tiles']]; ys = [t[1] for t in o['tiles']]
    L['objs'].append(dict(name=o['name'], box=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], sx=o['sx'], sy=0, sw=o['sw'], sh=o['sh'], x=o['x'], y=o['y'], door=None, solid=True, act=None))
L['objs'].append(dict(name='exit', box=[5, 9, 6, 10], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, door=dict(tile=[5, 9], to='campus', label='호박달 마녀학교', spawn=[19, 25]), solid=False, act=None))
t = open(I + '/halloween_tpl.html').read().replace('__MAPS__', json.dumps({'campus': {'meta': camp}, 'lab': {'meta': L}}, ensure_ascii=False))
t = t.replace("const ACTS = {}; const ACTS_OLD = {", "const ACTS_OLD = {}; const ACTS = {")
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
