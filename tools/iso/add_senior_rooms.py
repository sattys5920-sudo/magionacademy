# 3학년 휴게실 · 4학년 시계탑 옥상 관측실을 게임에 넣어요 (senior_rooms.py 그림 → public/art/iso, world.js MAPS · 물약 교실 벽에 문 두 개)
#   python3 tools/iso/senior_rooms.py && python3 tools/iso/add_senior_rooms.py
#   물약 교실(lab) 문: 왼쪽 벽 (0,18) → 3학년 휴게실 · 오른쪽 벽 (23,0) → 시계탑 계단(관측실). 문 그림은 도서관 문을 본떠 pclass_bg에 그려요 (이미 그렸으면 다시 안 그려요)
#   잠금: door.lock = 'gr3' / 'gr4' (index.html World.canEnter)
import json, os, hashlib, shutil
from PIL import Image
I = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(I)); ART = ROOT + '/public/art/iso/'; WJ = ROOT + '/public/world.js'

def webp(p): Image.open(p).save(p[:-4] + '.webp', 'WEBP', lossless=True, quality=100, method=6)
def ver(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]

# 1) 문 그림: 도서관 문(왼쪽 벽 y=14)을 왼쪽 벽 y=18 · (좌우 뒤집어) 오른쪽 벽 x=23 으로
bgp = ART + 'pclass_bg.png'; bg = Image.open(bgp).convert('RGBA'); OX, OY = 180, 82
mark = bg.getpixel((36, 120))
src = bg.crop((50, 70, 81, 149)); W, H = src.size
def base_left(x): return OY + (OX - x) / 2          # 왼쪽 벽 밑선
def tint(c, k):
    r, g, b, a = c
    if k == 'purple': return (min(255, int(r * .85 + 30)), int(g * .7), min(255, int(b * .9 + 40)), a)
    return (int(r * .75), min(255, int(g * .85 + 10)), min(255, int(b * .95 + 40)), a)
def door_pixel(x, y, c):   # 문짝·장식만 (벽 무늬는 그대로 두려고 나무색·금색·유리만 옮겨요)
    r, g, b, a = c
    return a > 0 and (r > g + 18 or (r > 150 and g > 120 and b < 120) or (b > r + 40 and b > 120))
done = os.path.exists(I + '/out/.senior_doors')
if not done:
    for (kind, dx, dy, flip) in (('purple', -32, 16, False), ('blue', 0, 0, True)):
        for yy in range(H):
            for xx in range(W):
                sx, sy = 50 + xx, 70 + yy
                if sy > base_left(sx): continue
                c = src.getpixel((xx, yy))
                if not door_pixel(sx, sy, c): continue
                if not flip: tx, ty = sx + dx, sy + dy
                else: tx, ty = 2 * OX - sx + 72, sy + 36          # 오른쪽 벽: 거울 (x=14 자리) → 9칸 안쪽으로
                if 0 <= tx < bg.width and 0 <= ty < bg.height: bg.putpixel((tx, ty), tint(c, kind))
    bg.save(bgp); webp(bgp); open(I + '/out/.senior_doors', 'w').write('1')

# 2) 방 그림 복사
for k in ('lounge3', 'observatory'):
    for sfx in ('_bg', '_obj'):
        p = ART + k + sfx + '.png'; shutil.copy(I + '/out/%s%s.png' % (k, sfx), p); webp(p)

# 3) world.js MAPS
s = open(WJ).read(); a = s.index('const MAPS = ') + len('const MAPS = '); b = s.index('}};\n', a) + 2
M = json.loads(s[a:b])
SUB = {'lounge3': ('3학년 휴게실', '3학년부터 들어올 수 있어요 · 문으로 물약 교실에 나가요', [1, 18]), 'observatory': ('시계탑 옥상 관측실', '4학년부터 올라올 수 있어요 · 계단으로 물약 교실에 내려가요', [23, 1])}
for k, (t, sub, back) in SUB.items():
    d = json.load(open(I + '/out/%s.json' % k))
    for o in d['objs']:
        if o.get('door'): o['door']['spawn'] = back
    d.update(title=t, sub=sub, bgSrc='art/iso/%s_bg.png?v=%s' % (k, ver(ART + k + '_bg.png')), objSrc='art/iso/%s_obj.png?v=%s' % (k, ver(ART + k + '_obj.png')), lazy=True)
    M[k] = {'meta': d}
L = M['lab']['meta']; L['objs'] = [o for o in L['objs'] if o['name'] not in ('g3door', 'g4door')]
L['objs'] += [dict(name='g3door', box=[0, 18, 1, 19], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, solid=False, act=None, door=dict(tile=[0, 18], to='lounge3', label='3학년 휴게실', spawn=[11, 16], lock='gr3', back=[1, 18])),
              dict(name='g4door', box=[23, 0, 24, 1], sx=0, sy=0, sw=0, sh=0, x=-99, y=-99, solid=False, act=None, door=dict(tile=[23, 0], to='observatory', label='시계탑 계단', spawn=[11, 16], lock='gr4', back=[23, 1]))]
L['bgSrc'] = 'art/iso/pclass_bg.png?v=' + ver(bgp)
s = s[:a] + json.dumps(M, ensure_ascii=False) + s[b:]
open(WJ, 'w').write(s)
print('ok', M['lounge3']['meta']['bgSrc'], M['observatory']['meta']['bgSrc'], L['bgSrc'])
