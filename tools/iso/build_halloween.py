# walk.html (호박달 마녀학교): hw.json + pclass.json(마녀 물약 교실) + interiors.py 방들 + halloween_tpl.html
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/walk.html'
camp = json.load(open(I + '/out/hw.json'))
camp.update(bgSrc='art/iso/hw_bg.png', objSrc='art/iso/hw_obj.png', title='호박달 마녀학교', sub='반짝이는 곳이 문이에요', fill='#140E1E')
L = json.load(open(I + '/out/pclass.json'))
L.update(indoor=True, vw=185, fill='#0C0715', bgSrc='art/iso/pclass_bg.png', objSrc='art/iso/pclass_obj.png', title='물약 교실', sub='본관 1층 · 반짝이는 곳으로 나가요')
MAPS = {'campus': {'meta': camp}, 'lab': {'meta': L}}
for k in ('candy', 'craft', 'dorm_witch', 'dorm_vamp', 'dorm_wolf', 'dorm_ghost', 'toxic'):
    MAPS[k] = {'meta': json.load(open(I + '/out/%s.json' % k))}
t = open(I + '/halloween_tpl.html').read().replace('__MAPS__', json.dumps(MAPS, ensure_ascii=False))
t = t.replace("const ACTS = {}; const ACTS_OLD = {", "const ACTS_OLD = {}; const ACTS = {")
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
