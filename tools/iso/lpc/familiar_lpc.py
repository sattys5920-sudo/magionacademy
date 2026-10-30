# 사역마 12종 (시안): LPC 부품으로 조립 → tools/iso/out/familiars_lpc.png (64칸 가로로 이어 붙임, 앞을 보고 선 모습)
#   꼬마 몸 + 동물 머리를 한 색으로 칠하고, 날개·꼬리·뿔·모자·망토·지팡이로 「마법사의 짝꿍」 느낌 · 소환수(pet_lpc.py)와 겹치지 않게 장식을 더해요
#   python3 familiar_lpc.py <LPC 저장소 경로> [미리보기.png]
import sys, os, subprocess
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import find, recolor, over, LPC, ROWS, FILES
OUT = os.path.join(HERE, '..', 'out', 'familiars_lpc.png')
CH = 'body/bodies/child'
def fam(head, rgb, glow, extra=(), alpha=1.0):
    return ([(10, CH, None, ('TINT', rgb)), (100, 'head/heads/' + head + '/child', None, ('TINT', rgb))] + list(extra), glow, alpha)
WPATH = {'lunar': 'lunar', 'pixie': 'pixie/solid', 'monarch': 'monarch/base', 'dragonfly': 'dragonfly/solid', 'feathered': 'feathered/adult'}
def wings(kind, col=None, tint=None): return [(5, f'body/wings/{WPATH[kind]}/bg', col, tint), (105.5, f'body/wings/{WPATH[kind]}/fg', col, tint)]
def wing1(kind, col=None, tint=None): return [(5, f'body/wings/{kind}/adult', col, tint)]
def tail(kind, rgb): return [(5, f'body/tail/{kind}/child/bg', None, ('TINT', rgb)), (125, f'body/tail/{kind}/child/fg', None, ('TINT', rgb))]
FAM = [
 ('루나울 · 달빛 늑대', fam('wolf', (210, 220, 240), (170, 200, 255), wings('lunar', 'lavender') + tail('wolf', (210, 220, 240)))),
 ('이그니 · 새끼 화염룡', fam('lizard', (220, 80, 60), (255, 140, 50), wing1('lizard') + tail('lizard', (220, 80, 60)) + [(110, 'head/horns/curled/child', None, None)])),
 ('찍찍 박사 · 사서 생쥐', fam('mouse', (190, 170, 150), (200, 160, 255), [(120, 'facial/glasses/round', None, None), (126, 'hat/magic/wizard', None, None)] + tail('cat', (190, 170, 150)))),
 ('코멧 · 별의 양', fam('sheep', (245, 245, 255), (255, 220, 110), wings('pixie', 'sky') + [(126, 'hat/magic/celestial', None, None)])),
 ('녹턴 · 그림자 쥐', fam('rat', (60, 50, 80), (180, 120, 255), wing1('bat') + tail('cat', (60, 50, 80)) + [(115, 'neck/amulet/star', None, None)])),
 ('피오 · 나비 토끼', fam('rabbit', (250, 200, 220), (255, 150, 200), wings('monarch', 'pink') + [(126, 'hat/formal/tiara', None, None)] + tail('fluffy', (250, 200, 220)))),
 ('모스 · 숲지기 소', fam('minotaur', (120, 100, 70), (130, 220, 110), [(5, 'cape/tattered/bg', 'forest', None), (110, 'cape/tattered/fg', 'forest', None)])),
 ('펑 · 고블린 연금술사', fam('goblin', (120, 190, 90), (190, 255, 120), [(126, 'hat/cloth/hood', 'brown', None), (120, 'facial/glasses/nerd', None, None)])),
 ('셀레 · 잠자리 도마뱀', fam('lizard', (90, 210, 170), (120, 240, 255), wings('dragonfly', 'teal') + tail('lizard', (90, 210, 170)))),
 ('바론 · 멧돼지 기사', fam('boarman', (150, 120, 100), (230, 200, 120), [(126, 'hat/helmet/horned', None, None)])),
 ('솔라 · 해님 늑대', fam('wolf', (240, 170, 70), (255, 220, 90), wings('feathered', 'white') + tail('wolf', (240, 170, 70)) + [(126, 'hat/formal/crown', None, None)])),
 ('뿌꾸 · 유령 돼지', fam('pig', (235, 235, 255), (220, 230, 255), [(126, 'hat/magic/large', None, None)], alpha=.72)),
]
def tint(a, rgb):
    o = a.copy(); lum = (a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114); mean = lum[a[..., 3] > 0].mean() if (a[..., 3] > 0).any() else 150; k = np.clip(.95 + (lum - mean) / 110, .5, 1.3)[..., None]
    o[..., :3] = np.clip(np.array(rgb)[None, None, :] * k, 0, 255).astype(np.uint8); return o
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y = ROWS['down'] * 64
    return a[y:y + 64, 0:64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def layer(f, rc): a = frame(f); return tint(a, rc[1]) if rc and rc[0] == 'TINT' else recolor(a, rc)
def tryfind(p, c, g='child'):
    for pp in (p, p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    cand = sorted(f for f in FILES if f.startswith('spritesheets/' + p + '/') and '/walk' in f and f.endswith('.png') and '/behind' not in f)
    if c: cand = [f for f in cand if c in f] or cand
    return cand[0] if cand else None
plan, missing = [], []
for name, (L, glow, al) in FAM:
    ls = []
    for z, p, c, rc in L:
        f = tryfind(p, c)
        if f is None: missing.append((name, p)); continue
        ls.append((z, f, rc))
    plan.append((name, ls, glow, al))
need = sorted({f for _, L, _, _ in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=False)
def dil(m):
    d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]; return d
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
for i, (name, L, glow, al) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]):
        if os.path.exists(os.path.join(LPC, f)): over(cell, layer(f, rc))
        else: missing.append((name, f))
    m = cell[..., 3] > 0; r1 = dil(m) & ~m
    cell[..., :3] = (cell[..., :3] * .9 + np.array(glow) * .1).astype(np.uint8); cell[..., 3] = (cell[..., 3] * al).astype(np.uint8); cell[r1] = (*glow, 150)
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(OUT)
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (40, 30, 64, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(sys.argv[2])
