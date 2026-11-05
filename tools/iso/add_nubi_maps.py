# 누비 이벤트: 낡은 양호실 · 따뜻한 양호실을 게임에 넣고, 물약 교실 구석 책장에 숨은 문을 달아요
#   python3 tools/iso/infirmary.py && python3 tools/iso/add_nubi_maps.py
#   물약 교실 그림은 그대로 두고, 이벤트가 열리면 index.html이 책장이 열린 그림(pclass_nubi_bg)으로 바꿔 끼워요 (World.setMapBg)
#   책장 문: 물약 교실 (0,2) · lock 'nubi' (열리기 전에는 그냥 책장) · 낡은 양호실 → 물약 교실 (1,2)
import json, os, hashlib, shutil
from PIL import Image, ImageDraw
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(I)); ART = ROOT + '/public/art/iso/'; WJ = ROOT + '/public/world.js'
def webp(p): Image.open(p).save(p[:-4] + '.webp', 'WEBP', lossless=True, quality=100, method=6)
def ver(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
for k in ('old_infirmary', 'warm_infirmary'):
    for sfx in ('_bg', '_obj'):
        p = ART + k + sfx + '.png'; shutil.copy(I + '/out/%s%s.png' % (k, sfx), p); webp(p)
# 책장이 열린 물약 교실 그림
bg = Image.open(ART + 'pclass_bg.png').convert('RGBA'); OX, OY = 180, 82
base = lambda x: OY + (OX - x) / 2; top = lambda x: 41 - (x - 152) * .5
X0, X1, HX = 152, 175, 174; src = bg.copy(); out = bg.copy()
for x in range(X0, X1):
    for y in range(int(top(x)), int(base(x)) + 1):
        depth = (y - top(x)) / max(1, base(x) - top(x))
        if x in (X0, X0 + 1, X1 - 1): c = (58, 34, 22, 255)
        else: k = int(10 + 26 * depth ** 3); c = (k // 2, k, int(k * .9), 255)
        out.putpixel((x, y), c)
d = ImageDraw.Draw(out); cx, cy = 163, int((top(163) + base(163)) / 2) - 6
d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=(70, 62, 58, 255)); d.rectangle([cx - 1, cy - 2, cx, cy + 2], fill=(120, 60, 56, 255)); d.rectangle([cx - 2, cy - 1, cx + 1, cy], fill=(120, 60, 56, 255))
for x in range(X0, X1):
    for y in range(int(top(x)), int(base(x)) + 1):
        c = src.getpixel((x, y))
        if c[3]: out.putpixel((2 * HX - x, y), (int(c[0] * .82), int(c[1] * .82), int(c[2] * .82), 255))
for y in range(int(top(X0)), int(base(X0)) + 1): out.putpixel((2 * HX - X0 + 1, y), (40, 24, 16, 255))
p = ART + 'pclass_nubi_bg.png'; out.save(p); webp(p)
s = open(WJ).read(); a = s.index('const MAPS = ') + len('const MAPS = '); b = s.index('}};\n', a) + 2
M = json.loads(s[a:b])
for k, title, sub in (('old_infirmary', '낡은 양호실', '책장 뒤에 숨어 있던 방'), ('warm_infirmary', '따뜻한 양호실', '누비가 지키는 방')):
    dd = json.load(open(I + '/out/%s.json' % k))
    for o in dd['objs']:
        if o.get('door'): o['door'].update(to='lab', label='물약 교실', spawn=[1, 2])
    dd.update(title=title, sub=sub, bgSrc='art/iso/%s_bg.png?v=%s' % (k, ver(ART + k + '_bg.png')), objSrc='art/iso/%s_obj.png?v=%s' % (k, ver(ART + k + '_obj.png')), lazy=True, indoor=True, spawnIn=[9, 11])
    if k == 'old_infirmary': dd['night'] = True
    M[k] = {'meta': dd}
L = M['lab']['meta']; L['objs'] = [o for o in L['objs'] if o['name'] != 'nubishelf']
L['objs'].append(dict(name='nubishelf', box=[0, 2, 1, 3], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, solid=False, act=None, door=dict(tile=[0, 2], to='old_infirmary', label='책장', spawn=[9, 11], lock='nubi', back=[1, 2])))
L['nubiBg'] = 'art/iso/pclass_nubi_bg.png?v=' + ver(p)
s = s[:a] + json.dumps(M, ensure_ascii=False) + s[b:]
open(WJ, 'w').write(s)
print('ok', M['old_infirmary']['meta']['bgSrc'], L['nubiBg'])
