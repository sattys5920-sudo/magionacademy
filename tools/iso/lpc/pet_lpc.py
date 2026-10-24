# 소환수·포탑을 LPC 부품으로 조립 → public/art/pets.png (64칸 14개, 왼쪽(적 쪽)을 보고 서 있는 모습)
#   python3 pet_lpc.py <LPC 저장소 경로> [미리보기.png]   순서는 index.html의 XPETI(이름 → 칸)와 같아요
import sys, os, subprocess
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import find, recolor, over, LPC, ROWS, FILES
ROOT = os.path.join(HERE, '..', '..', '..')
SK = lambda dst, src='light': ('body', src, dst)
CL = lambda dst: ('cloth', 'white', dst)
HR = lambda dst: ('hair', 'orange', dst)
CH = 'body/bodies/child'; SHIRT = 'torso/clothes/shirt/child'
def spirit(skin, cloth, hair, wing, hat=None):
    L = [(5, 'body/wings/pixie/solid', wing, None), (10, CH, None, SK(skin)), (100, 'head/heads/human/child', None, SK(skin)), (35, SHIRT, None, CL(cloth)), (120, 'hair/messy1', None, HR(hair)), (110, 'head/ears/elven/child', None, SK(skin))]
    if hat: L.append((126, hat, None, None))
    return L
PETS = [  # 이름, 몸 체형, 층들, 알파
 ('불 정령', 'child', spirit('amber', 'red', 'red', 'red'), 1), ('물 정령', 'child', spirit('blue', 'sky', 'blue', 'blue'), 1),
 ('바람 정령', 'child', spirit('lavender', 'white', 'platinum', 'white'), 1), ('대지 정령', 'child', spirit('brown', 'forest', 'dark_brown', 'green'), 1),
 ('정령왕', 'child', spirit('bronze', 'yellow', 'gold', 'yellow', 'hat/formal/crown'), 1),
 ('늑대', 'child', [(5, 'body/tail/wolf/child', 'gray', None), (10, CH, None, SK('fur_grey')), (100, 'head/heads/wolf/child', None, None), (125, 'body/tail/wolf/child', 'gray', None)], 1),
 ('곰', 'child', [(10, CH, None, SK('fur_brown')), (100, 'head/heads/minotaur/child', None, None), (35, SHIRT, None, CL('brown'))], 1),
 ('독수리', 'child', [(5, 'body/wings/feathered/adult/bg', 'brown', None), (10, CH, None, SK('fur_tan')), (100, 'head/heads/goblin/child', None, None), (35, SHIRT, None, CL('tan')), (105.5, 'body/wings/feathered/adult/fg', 'brown', None)], 1),
 ('호박 유령', 'child', [(10, CH, None, SK('fur_white')), (100, 'head/heads/human/child', None, SK('fur_white')), (126, 'hat/cloth/hood', None, CL('orange'))], .62),
 ('용', 'child', [(5, 'body/wings/lizard/adult', None, None), (5.5, 'body/tail/lizard/child', None, None), (10, CH, None, SK('blue')), (100, 'head/heads/lizard/child', None, SK('blue', 'green')), (35, SHIRT, None, CL('maroon'))], 1),
 ('소형 포탑', 'male', [(10, 'weapon/ranged/crossbow/walk/crossbow.png', 'RAW', None), (9, 'weapon/ranged/crossbow/background/walk/crossbow.png', 'RAW', None), (11, 'weapon/ranged/crossbow/foreground/walk/crossbow.png', 'RAW', None)], 1),
 ('보조 포탑', 'male', [(10, 'shield/round/walk.png', 'RAWF', None)], 1),
 ('레이저 포탑', 'male', [(9, 'weapon/magic/diamond/universal/background/walk/diamond.png', 'RAW', None), (10, 'weapon/magic/diamond/universal/foreground/walk/diamond.png', 'RAW', None)], 1),
 ('요새 포대', 'male', [(10, 'weapon/blunt/mace/walk/mace.png', 'RAW', None), (9, 'weapon/blunt/mace/universal_behind/walk/mace.png', 'RAW', None), (11, 'weapon/ranged/crossbow/foreground/walk/crossbow.png', 'RAW', None)], 1),
]
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS['left'] * 64
    return a[y:y + 64, 0:64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def tryfind(p, c, g):
    for pp in (p, p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    cand = sorted(f for f in FILES if f.startswith('spritesheets/' + p + '/') and '/walk' in f and f.endswith('.png') and '/behind' not in f and '/background' not in f)
    if c: cand = [f for f in cand if c in f] or cand
    return cand[0] if cand else None
plan = []; missing = []
for name, g, L, al in PETS:
    ls = []
    for z, p, c, rc in L:
        if c in ('RAW', 'RAWF'): f = 'spritesheets/' + p
        else: f = tryfind(p, c, g)
        if f is None or f not in FILES: missing.append((name, p)); continue
        ls.append((z, f, rc))
    plan.append((name, ls, al))
need = sorted({f for _, L, _ in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
for i, (name, L, al) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]): over(cell, recolor(frame(f), rc))
    cell[..., 3] = (cell[..., 3] * al).astype(np.uint8); sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'pets.png'))
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[2])
