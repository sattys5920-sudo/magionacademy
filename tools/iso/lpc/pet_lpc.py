# 소환수 14종(정령 같은 동물)을 LPC 부품으로 조립 → public/art/pets.png (64칸, 왼쪽(적 쪽)을 보고 서 있는 모습)
#   LPC 꼬마 몸(맨몸) 전체를 털 색으로 칠하고 + 동물 머리 + 꼬리 + 날개. 속성 색 빛·반투명. 옷·무기 없음
#   python3 pet_lpc.py <LPC 저장소 경로> [미리보기.png]   순서는 index.html의 XPETI와 같아요
import sys, os, subprocess
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import find, recolor, over, LPC, ROWS, FILES
ROOT = os.path.join(HERE, '..', '..', '..')
CH = 'body/bodies/child'
FUR = {'fur_copper': (232, 120, 46), 'blue': (120, 170, 240), 'fur_white': (240, 244, 250), 'fur_brown': (138, 106, 72), 'fur_grey': (140, 146, 160), 'fur_tan': (184, 152, 104), 'bright_green': (100, 200, 100), 'fur_black': (66, 62, 72)}   # 털 색 (몸 전체를 이 색으로)
def animal(head, fur, glow, tail=None, tcol='gray', extra=(), alpha=.88, hair=None):
    L = [(10, CH, None, ('TINT', FUR[fur])), (100, 'head/heads/' + head, None, ('TINT', FUR[fur]))] + list(extra)
    if tail: L += [(5, tail + '/bg', tcol, ('TINT', FUR[fur])), (125, tail + '/fg', tcol, ('TINT', FUR[fur]))]
    return (L, glow, alpha)
WOLF, CAT, FLUF, LIZ = 'body/tail/wolf/child', 'body/tail/cat/child', 'body/tail/fluffy/child', 'body/tail/lizard/child'
PETS = [
 ('불 정령', animal('wolf/child', 'fur_copper', (255, 110, 50), WOLF, 'ginger')), ('물 정령', animal('rabbit/child', 'blue', (90, 210, 255), FLUF, 'blue')),
 ('바람 정령', animal('sheep/child', 'fur_white', (225, 240, 255), FLUF, 'white', alpha=.8)), ('대지 정령', animal('boarman/child', 'fur_brown', (200, 160, 90), CAT, 'dark_brown')),
 ('정령왕', animal('wolf/child', 'fur_white', (255, 214, 90), WOLF, 'white', extra=[(126, 'hat/formal/crown', None, None)])), ('늑대', animal('wolf/child', 'fur_grey', (200, 215, 255), WOLF, 'gray')),
 ('곰', animal('minotaur/child', 'fur_brown', (170, 115, 70), CAT, 'dark_brown')),
 ('독수리', animal('lizard/child', 'fur_tan', (240, 232, 190), None, extra=[(5, 'body/wings/feathered/adult/bg', 'brown', None), (105.5, 'body/wings/feathered/adult/fg', 'brown', None)])),
 ('호박 유령', animal('rabbit/child', 'fur_copper', (255, 150, 40), FLUF, 'orange', alpha=.6)),
 ('용', animal('lizard/child', 'blue', (255, 80, 60), None, extra=[(5, 'body/wings/lizard/adult', None, None), (5.5, LIZ + '/bg', None, ('TINT', FUR['blue'])), (125, LIZ + '/fg', None, ('TINT', FUR['blue']))])),
 ('번개 쥐', animal('mouse/child', 'fur_grey', (90, 230, 255), CAT, 'gray')), ('수호 쥐', animal('rat/child', 'fur_black', (120, 255, 150), CAT, 'black')),
 ('광선 도마뱀', animal('lizard/child', 'bright_green', (255, 100, 170), None, extra=[(5.5, LIZ + '/bg', None, ('TINT', FUR['bright_green'])), (125, LIZ + '/fg', None, ('TINT', FUR['bright_green']))])), ('철갑 멧돼지', animal('boarman/child', 'fur_grey', (170, 190, 210), CAT, 'gray')),
]
def tint(a, rgb):   # 몸 그림의 밝기는 살리고 색을 털 색으로
    o = a.copy(); lum = (a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114); mean = lum[a[..., 3] > 0].mean() if (a[..., 3] > 0).any() else 150; k = np.clip(.95 + (lum - mean) / 110, .5, 1.3)[..., None]   # 이 조각 자신의 평균 밝기 기준 (머리·몸 색조가 같아져요)
    o[..., :3] = np.clip(np.array(rgb)[None, None, :] * k, 0, 255).astype(np.uint8); return o
def layer(f, rc):
    a = frame(f); return tint(a, rc[1]) if rc and rc[0] == 'TINT' else recolor(a, rc)
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS['left'] * 64
    return a[y:y + 64, 0:64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def tryfind(p, c, g='child'):
    for pp in (p, p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    cand = sorted(f for f in FILES if f.startswith('spritesheets/' + p + '/') and '/walk' in f and f.endswith('.png') and '/behind' not in f)
    if c: cand = [f for f in cand if c in f] or cand
    return cand[0] if cand else None
plan = []; missing = []
for name, (L, glow, al) in PETS:
    ls = []
    for z, p, c, rc in L:
        f = tryfind(p, c)
        if f is None: missing.append((name, p)); continue
        ls.append((z, f, rc))
    plan.append((name, ls, glow, al))
need = sorted({f for _, L, _, _ in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
def dil(m):
    d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]; return d
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
for i, (name, L, glow, al) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]): over(cell, layer(f, rc))
    m = cell[..., 3] > 0; r1 = dil(m) & ~m; r2 = dil(m | r1) & ~(m | r1)
    cell[..., :3] = (cell[..., :3] * .82 + np.array(glow) * .18).astype(np.uint8); cell[..., 3] = (cell[..., 3] * al).astype(np.uint8); cell[r1] = (*glow, 190); cell[r2] = (*glow, 70)
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'pets.png'))
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[2])
