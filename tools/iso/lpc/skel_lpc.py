# 시안: 유령 전학생 이야기의 「해골 선생님」을 LPC 부품으로 조립해요 → out/skel_lpc.png (64×64 칸 20개) + 초상 out/skel_face.png
#   해골 몸·해골 머리 + 짙은 보라 망토 · 단정한 정장 · 반달 안경 · 마법사 모자 (어른 체형이라 날씬하게 줄이지 않아요)
#   python3 skel_lpc.py <LPC 저장소 경로> [미리보기.png]
import sys, os, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
N.slim = lambda cell, d, neck=True: cell.copy()
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out')
L = [(5, 'cape/solid/bg', None, N.CL('purple')), (10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton', None, None),
     (20, 'legs/pants', None, N.CL('charcoal')), (15, 'feet/boots/basic', None, N.CL('black')), (35, 'torso/clothes/longsleeve/formal', None, N.CL('white')),
     (40, 'torso/jacket/collared', 'black', None), (60, 'neck/tie/bowtie', None, N.CL('purple')), (110, 'cape/solid/fg', None, N.CL('purple')),
     ] + ([] if os.environ.get('NOGL', '1') == '1' else [(130, 'facial/glasses/halfmoon', 'gold', None)]) + ([(140, os.environ.get('HAT', 'hat/magic/wizard/base'), None, None)] if os.environ.get('HAT', 'hat/magic/wizard/base') else [])
plan = [(z, N.find(p, c, 'male'), rc) for z, p, c, rc in L]
need = sorted({f for _, f, _ in plan if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
row = np.zeros((64, 64 * 20, 4), np.uint8); HATC = (96, 52, 140)
def tint(a, col):   # 모자: 밝기만 살리고 색을 입혀요
    o = a.copy().astype(float); lum = (a[..., :3].astype(float) @ [.3, .59, .11]) / 255; o[..., :3] = np.clip(lum[..., None] * 1.5 * np.array(col), 0, 255); return o.astype(np.uint8)
def up(a, d):   # 해골 머리는 눈이 높아서 모자를 조금 올려 써요
    o = np.zeros_like(a); o[:-d] = a[d:]; return o
for z, f, rc in sorted(plan, key=lambda t: t[0]):
    a = N.strip_frames(Image.open(os.path.join(LPC, f)))
    if '/hat/' in f: a = up(tint(a, HATC), int(os.environ.get('HUP', 4)))
    else: a = N.recolor(a, rc)
    N.over(row, a)
im = Image.fromarray(row); im.save(os.path.join(OUTD, 'skel_lpc.png'))
for f in plan: print(f[1])
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * 5 + 140, 70), (40, 30, 56, 255))
    for j, i in enumerate((0, 5, 10, 15, 2)): pv.alpha_composite(im.crop((i * 64, 0, i * 64 + 64, 64)), (j * 64, 3))
    pv = pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST); pv.alpha_composite(im.crop((14, 0, 50, 36)).resize((280, 280), Image.NEAREST), (64 * 5 * 4 + 0, 0)); pv.save(sys.argv[2])
