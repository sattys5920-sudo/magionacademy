# 시안: 정원 손님 6 종 (아기 동물과 같은 14×14 · 진보라 테두리 · 흰 반짝 눈 · 분홍 볼) → ../garden_mock/gi_guests.png (14×14 · 손님마다 2 칸)
#   0 이끼 달팽이 · 1 버섯 꼬마 · 2 솜뭉치 정령 · 3 반딧불 나방 · 4 꼬마 두더지 · 5 달빛 해파리(드문 손님)
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'garden_mock')
def hx(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
COMMON = {'O': hx('#1a1024'), 'K': hx('#1a1024'), 'W': hx('#ffffff'), 'P': hx('#ff9ab8')}
G = [
 ('snail', {'B': hx('#f2dca6'), 'b': hx('#d8b878'), 'G': hx('#7ab85a'), 'H': hx('#a8da7a'), 'g': hx('#5a9a42')}, [
  '..............',
  '.......OOOOO..',
  '......OGGHGGO.',
  '.....OGHGGGgGO',
  '.....OGGgOGGGO',
  '.O.O.OGgOOgGGO',
  'OBOBOOGGGGGgO.',
  'OBBBBOOGGGGO..',
  'OBWBBBOOOOOO..',
  'OBKBPBBBBBBBO.',
  '.OBBBBBBBBBBBO',
  '..ObbbbbbbbbO.',
  '...OOOOOOOOO..',
  '..............']),
 ('shroom', {'R': hx('#e0584a'), 'r': hx('#b03a32'), 'C': hx('#f6e2be'), 'c': hx('#d8b88a'), 'D': hx('#a85a3a')}, [
  '..............',
  '....OOOOOO....',
  '..OORRWRRROO..',
  '.ORRWRRRRWRRO.',
  '.ORRRRRWRRRRO.',
  '.OrrrrrrrrrrO.',
  '..OOOOOOOOOO..',
  '...OCCCCCCO...',
  '...OCWCCWCO...',
  '...OCKCCKCO...',
  '...OPCDDCPO...',
  '....OccccO....',
  '...OOO..OOO...',
  '..............']),
 ('fluff', {'F': hx('#f4f0ff'), 'S': hx('#d4cbef'), 'L': hx('#b8acdc')}, [
  '..............',
  '.....O..O.....',
  '...OOFOOFOO...',
  '..OFFFFFFFFO..',
  '.OFFFFFFFFFFO.',
  'OFFFWFFFFWFFFO',
  'OFFFKFFFFKFFFO',
  'OFFPFFFFFFPFFO',
  'OSFFFFFFFFFFSO',
  '.OSSFFFFFFSSO.',
  '..OLSOSSOSLO..',
  '...O.O..O.O...',
  '..............',
  '..............']),
 ('moth', {'Y': hx('#ffd84a'), 'L': hx('#fff6b8'), 'F': hx('#ecdcc4'), 'f': hx('#c8b090'), 'A': hx('#8a6a4a')}, [
  '..............',
  '...A......A...',
  '....A....A....',
  '.OO..OOOO..OO.',
  'OYYO.OFFO.OYYO',
  'OYLYOFFFFOYLYO',
  'OYYYOFWWFOYYYO',
  'OYLYOFKKFOYLYO',
  '.OYYOFPPFOYYO.',
  '..OOOFffFOOO..',
  '.....OFFO.....',
  '......OO......',
  '..............',
  '..............']),
 ('mole', {'M': hx('#9a6a4a'), 'm': hx('#7a5034'), 'N': hx('#ff8ab0'), 'E': hx('#6a4a2a'), 'e': hx('#8a6a3e')}, [
  '..............',
  '..............',
  '....OOOOOO....',
  '...OMMMMMMO...',
  '..OMMMMMMMMO..',
  '..OMWMMMMWMO..',
  '..OMKMMMMKMO..',
  '..OPMMNNMMPO..',
  '..OMmMNNMmMO..',
  '.OOOMMMMMMOOO.',
  'OeEeOOOOOOeEeO',
  'OEEEeEEEEeEEEO',
  '.OOOOOOOOOOOO.',
  '..............']),
 ('jelly', {'J': hx('#cfc4ff', 215), 'L': hx('#ffffff', 230), 'j': hx('#a898e8', 215), 'T': hx('#b8acf8', 180)}, [
  '..............',
  '....OOOOOO....',
  '..OOJJJJJJOO..',
  '.OJJLJJJJJJJO.',
  '.OJLJJJJJJJJO.',
  '.OJJJWJJWJJJO.',
  '.OJJJKJJKJJJO.',
  '.OjjPjjjjPjjO.',
  '..OOjOjjOjOO..',
  '...T..T..T....',
  '..T...T...T...',
  '...T..T..T....',
  '....T..T..T...',
  '..............']),
]
def render(rows, pal):
    im = Image.new('RGBA', (14, 14), (0, 0, 0, 0)); P = {**COMMON, **pal}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r[:14]):
            if ch != '.': im.putpixel((x, y), P[ch])
    return im
def frame2(k, rows):   # 두 번째 칸: 눈 깜빡 · 둥실 · 날개 반짝 · 촉수 흔들
    if k in ('fluff', 'jelly'): rows = rows[1:] + ['..............']
    if k == 'jelly': rows = rows[:8] + [r[1:] + '.' if i % 2 == 0 else '.' + r[:-1] for i, r in enumerate(rows[8:])]
    if k == 'moth': rows = [r.replace('L', 'Y') for r in rows]
    if k in ('snail', 'shroom', 'mole'): rows = [r.replace('W', 'K') if i in (8, 5) else r for i, r in enumerate(rows)]
    if k == 'mole': rows = ['..............'] + rows[:-1]
    return rows
sh = Image.new('RGBA', (14 * 2 * len(G), 14))
for i, (k, pal, rows) in enumerate(G):
    sh.alpha_composite(render(rows, pal), (i * 28, 0)); sh.alpha_composite(render(frame2(k, rows), pal), (i * 28 + 14, 0))
sh.save(os.path.join(OUT, 'gi_guests.png'))
pv = Image.new('RGBA', (sh.width, 14), (40, 30, 56, 255)); pv.alpha_composite(sh, (0, 0)); pv.resize((sh.width * 8, 112), Image.NEAREST).save(os.path.join(OUT, 'gi_guests_preview.png')); print('ok')
