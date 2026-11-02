import sys
S, D = sys.argv[1], sys.argv[2]
r = lambda p: open(p).read().strip()
t = r(D + '/bookmarks.tpl.html').replace('__BASECSS__', r(S + '/bm_css_all.css')).replace('__NAMES__', r(S + '/bk_names.json'))
for k, f in [('__G11B__', 'g11b.b64'), ('__G11__', 'g11.b64'), ('__SHEET__', 'mini_b64.txt'), ('__ICONS__', 'bk_icons_b64.txt')]:
    t = t.replace(k, r(S + '/' + f))
open(D + '/bookmarks.html', 'w').write(t); print(len(t))
