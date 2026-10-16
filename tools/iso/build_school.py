# walk.html (별빛고등학교): school.json + sci.json + school_tpl.html
import json, sys, os
I = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1] if len(sys.argv) > 1 else 'public/walk.html'
camp = json.load(open(I + '/out/school.json')); sci = json.load(open(I + '/out/sci.json'))
camp.update(bgSrc='art/iso/school_bg.png', objSrc='art/iso/school_obj.png', title='별빛고등학교', sub='반짝이는 곳이 문이에요', fill='#2A3A28')
sci.update(bgSrc='art/iso/sci_bg.png', objSrc='art/iso/sci_obj.png', title='과학실', sub='교실동 2층 · 반짝이는 곳으로 나가요', fill='#1E1A26', indoor=False, vw=124)
t = open(I + '/school_tpl.html').read().replace('__MAPS__', json.dumps({'campus': {'meta': camp}, 'lab': {'meta': sci}}, ensure_ascii=False))
open(OUT, 'w').write(t); print('wrote', OUT, len(t))
