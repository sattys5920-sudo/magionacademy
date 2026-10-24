# 소환수(정령 같은 동물)를 LPC 부품으로 조립 → public/art/pets.png (64칸 14개, 왼쪽(적 쪽)을 보고 서 있는 모습)
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
# 소환수는 모두 정령 같은 동물: 동물 머리 + 꼬마 몸(맨몸) + 속성 색 빛(번짐·반투명). 무기·옷 없음
AU = lambda dst: ('body', 'auto', dst)
def animal(head, skin, glow, extra=(), alpha=.86, tail=None):
    L = [(10, CH, None, AU(skin)), (100, 'head/heads/' + head, None, None)] + list(extra)
    if tail: L = [(5, tail, 'gray', None), (125, tail, 'gray', None)] + L
    return (L, glow, alpha)
CH = 'body/bodies/child'
PETS = [  # 이름, 몸 체형, (층들, 빛 색, 투명도)
 ('불 정령', 'child', animal('wolf/child', 'fur_copper', (255, 110, 50), tail='body/tail/wolf/child')),
 ('물 정령', 'child', animal('rabbit/child', 'blue', (90, 210, 255))),
 ('바람 정령', 'child', animal('sheep/child', 'fur_white', (225, 240, 255), alpha=.8)),
 ('대지 정령', 'child', animal('boarman/child', 'fur_brown', (200, 160, 90))),
 ('정령왕', 'child', animal('wolf/child', 'fur_white', (255, 214, 90), extra=[(126, 'hat/formal/crown', None, None)], tail='body/tail/wolf/child')),
 ('늑대', 'child', animal('wolf/child', 'fur_grey', (200, 215, 255), tail='body/tail/wolf/child')),
 ('곰', 'child', animal('minotaur/child', 'fur_brown', (170, 115, 70))),
 ('독수리', 'child', animal('lizard/child', 'fur_tan', (240, 232, 190), extra=[(5, 'body/wings/feathered/adult/bg', 'brown', None), (105.5, 'body/wings/feathered/adult/fg', 'brown', None)])),
 ('호박 유령', 'child', animal('rabbit/child', 'fur_copper', (255, 150, 40), alpha=.6)),
 ('용', 'child', animal('lizard/child', 'blue', (255, 80, 60), extra=[(5, 'body/wings/lizard/adult', None, None), (5.5, 'body/tail/lizard/child', None, None)])),
 ('소형 포탑', 'child', animal('mouse/child', 'fur_grey', (90, 230, 255))),
 ('보조 포탑', 'child', animal('rat/child', 'fur_black', (120, 255, 150))),
 ('레이저 포탑', 'child', animal('goblin/child', 'bright_green', (255, 100, 170))),
 ('요새 포대', 'child', animal('troll/child', 'fur_grey', (170, 190, 210))),
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
for name, g, (L, glow, al) in PETS:
    ls = []
    for z, p, c, rc in L:
        if c in ('RAW', 'RAWF'): f = 'spritesheets/' + p
        else: f = tryfind(p, c, g)
        if f is None or f not in FILES: missing.append((name, p)); continue
        ls.append((z, f, rc))
    plan.append((name, ls, al, glow))
need = sorted({f for _, L, _, _ in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
def dil(m):
    d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]; return d
for i, (name, L, al, glow) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]): over(cell, recolor(frame(f), rc))
    m = cell[..., 3] > 0; r1 = dil(m) & ~m; r2 = dil(m | r1) & ~(m | r1)
    cell[..., :3] = (cell[..., :3] * .82 + np.array(glow) * .18).astype(np.uint8)    # 속성 색을 살짝 입혀서 정령 느낌
    cell[..., 3] = (cell[..., 3] * al).astype(np.uint8)
    cell[r1] = (*glow, 190); cell[r2] = (*glow, 70)    # 빛 번짐
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'pets.png'))
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[2])
