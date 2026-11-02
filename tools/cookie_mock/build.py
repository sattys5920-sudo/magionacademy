import sys
S, D = sys.argv[1], sys.argv[2]
r = lambda p: open(p).read().strip()
t = r(D + '/cookie_play.tpl.html').replace('__INTRO__', r(D + '/intro.js')).replace('__GIFT__', r(D + '/gift.js'))
for k, f in [('__G11B__', 'g11b.b64'), ('__G11__', 'g11.b64'), ('__SHEET__', 'mini_b64.txt'), ('__CANDY__', 'map_candy_b64.txt'), ('__ICONS__', 'ck_icons_b64.txt')]:
    t = t.replace(k, r(S + '/' + f))
open(D + '/cookie_play.html', 'w').write(t)
print(len(t))
