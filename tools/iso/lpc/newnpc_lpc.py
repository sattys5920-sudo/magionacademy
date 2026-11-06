# 시안: 새 NPC 셋 (셀린 · 도도 · 본)을 LPC 부품으로 조립해요 → out/newnpc_lpc.png (한 줄 = 한 명, 64×64 칸 20개) + 미리보기
#   python3 newnpc_lpc.py <LPC 저장소 경로> [미리보기.png]
#   셀린: 사람 재봉사 (검은 드레스 · 보라 앞치마 · 거미 목걸이 · 올림머리)
#   도도: 도도새 경매사 (회색 깃털 날개 · 실크해트 · 외알 안경 · 크라바트 · 흰 머리)
#   본: 해골 음유시인 (해골 몸 · 깃털 모자 · 알록달록 셔츠 · 해진 망토)
import sys, os, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out'); SK, HR, CL = N.SK, N.HR, N.CL
NPC = [
 ('셀린', 'female', [(10, 'body/bodies/teen', None, SK('light')), (100, 'head/heads/human/female', None, SK('light')), (105, 'eyes/human/adult/default', 'purple', None),
   (20, 'legs/skirts/straight', None, CL('black')), (35, 'torso/clothes/blouse_longsleeve', None, CL('black')), (40, 'torso/aprons/apron_half', None, CL('purple')),
   (60, 'neck/amulet/spider', None, None), (15, 'feet/shoes/basic', None, CL('black')), (120, 'hair/bangs_bun', None, HR('black'))]),
 ('도도', 'male', [(5, 'body/wings/feathered/adult/bg', 'gray', None), (10, 'body/bodies/teen', None, SK('light')), (100, 'head/heads/human/male', None, SK('light')), (105, 'eyes/human/adult/default', 'blue', None),
   (20, 'legs/pants', None, CL('tan')), (35, 'torso/clothes/longsleeve/formal', None, CL('white')), (40, 'torso/jacket/collared', 'navy', None), (60, 'neck/cravat', None, CL('white')),
   (15, 'feet/shoes/basic', None, CL('brown')), (120, 'hair/plain', None, HR('white')), (126, 'hat/formal/tophat', None, CL('gray')), (130, 'facial/monocle/left', None, None), (105.5, 'body/wings/feathered/adult/fg', 'gray', None)]),
 ('본', 'male', [(5, 'cape/tattered/bg', None, CL('maroon')), (10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton', None, None),
   (20, 'legs/pants', None, CL('red')), (35, 'torso/clothes/longsleeve/laced', None, CL('yellow')), (15, 'feet/boots/basic', None, CL('brown')),
   (110, 'cape/tattered/fg', None, CL('maroon')), (126, 'hat/cloth/leather_cap', None, CL('green')), (127, 'hat/cloth/leather_cap/feather', None, CL('red'))]),
]
plan = []
for nm, g, L in NPC:
    ps = []
    for z, p, c, rc in L:
        try: ps.append((z, N.find(p, c, g), rc))
        except SystemExit as e: print('빠짐', nm, e)
    plan.append((nm, ps))
need = sorted({f for _, L in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64 * len(plan), 64 * 20, 4), np.uint8)
for r, (nm, L) in enumerate(plan):
    row = np.zeros((64, 64 * 20, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]):
        keep = any(w in f for w in ('/hair/', '/heads/', '/ears/', '/hat/', '/facial/', '/eyes/'))
        a = N.strip_frames(Image.open(os.path.join(LPC, f)), not keep) if 'skeleton' not in f else N.strip_frames(Image.open(os.path.join(LPC, f)), False)
        N.over(row, N.recolor(a, rc))
    sheet[r * 64:(r + 1) * 64] = row
    print(nm, [f for _, f, _ in L])
im = Image.fromarray(sheet); im.save(os.path.join(OUTD, 'newnpc_lpc.png'))
if len(sys.argv) > 2:   # 미리보기: 사람마다 아래 · 왼쪽 · 위 · 오른쪽 + 걷기 한 칸 (4 배)
    pv = Image.new('RGBA', (64 * 5, 66 * len(plan)), (40, 30, 56, 255))
    for r in range(len(plan)):
        for j, i in enumerate((0, 10, 5, 15, 2)): pv.alpha_composite(im.crop((i * 64, r * 64, i * 64 + 64, r * 64 + 64)), (j * 64, r * 66 + 1))
    pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(sys.argv[2])
