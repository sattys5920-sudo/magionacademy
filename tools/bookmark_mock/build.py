import sys, json
S, D = sys.argv[1], sys.argv[2]
r = lambda p: open(p).read().strip()
body = r(D + '/book.md').split('\n---\n', 1)[1].strip()
t = r(D + '/words.tpl.html').replace('__BASECSS__', r(S + '/bm_css_all.css')).replace('__BOOK__', json.dumps(body, ensure_ascii=False))
for k, f in [('__G11B__', 'g11b.b64'), ('__G11__', 'g11.b64'), ('__SHEET__', 'mini_b64.txt')]:
    t = t.replace(k, r(S + '/' + f))
open(D + '/words.html', 'w').write(t); print(len(t))
