# 탐사 몬스터(사람 모양)를 LPC 부품으로 조립 → public/art/monsters_lpc.png (64칸 가로로 이어 붙임, 오른쪽(파티 쪽)을 보고 서 있는 모습)
#   python3 monster_lpc.py <LPC 저장소 경로> [미리보기.png]
#   NPC와 안 겹치게: 뱀파이어·프랑켄·잭·늑대 머리, 박쥐 날개·고양이 귀, 붕대, 초록 도마뱀(캇파), 마녀모자(큰 모자)는 쓰지 않아요
import sys, os, subprocess
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import find, recolor, over, LPC, ROWS
ROOT = os.path.join(HERE, '..', '..', '..')
SK = lambda dst, src='light': ('body', src, dst)
CL = lambda dst: ('cloth', 'white', dst)
HR = lambda dst: ('hair', 'orange', dst)
# 층: (z, 폴더, 색 그림 이름, 팔레트 바꾸기)
W_SWORD = (90, 'weapon/sword/longsword', 'longsword', None); W_AXE = (90, 'weapon/blunt/waraxe', 'waraxe', None); W_DAG = (90, 'weapon/sword/dagger', 'dagger', None)
MON = [  # (id, 몸 체형(g), 층들)
 ('goblin', 'teen', [(10, 'body/bodies/teen', None, SK('green')), (100, 'head/heads/goblin/adult', None, None), (20, 'legs/pants', None, CL('brown')), (35, 'torso/armour/leather/teen', None, None), (15, 'feet/boots/basic', None, CL('brown')), W_DAG]),
 ('rat', 'teen', [(10, 'body/bodies/teen', None, SK('fur_grey')), (100, 'head/heads/rat/adult', None, None), (20, 'legs/pants', None, CL('black')), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('charcoal')), (126, 'hat/cloth/hood', None, CL('black')), (15, 'feet/shoes/basic', None, CL('black')), W_DAG]),
 ('rabbit', 'teen', [(10, 'body/bodies/teen', None, SK('fur_white')), (100, 'head/heads/rabbit/adult', None, None), (20, 'legs/pants', None, CL('forest')), (35, 'torso/armour/leather/teen', None, None), (15, 'feet/boots/basic', None, CL('brown')), (90, 'weapon/polearm/spear/foreground', 'bronze', None)]),
 ('skelsol', 'male', [(10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton/adult', None, None), (126, 'hat/helmet/kettle/adult', None, None), (95, 'shield/round', 'brown', None), W_SWORD]),
 ('zombie', 'male', [(10, 'body/bodies/zombie', 'zombie', None), (100, 'head/heads/zombie/adult', None, None), (20, 'legs/pants', None, CL('brown')), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('slate')), (15, 'feet/shoes/basic', None, CL('brown'))]),
 ('mouse', 'teen', [(10, 'body/bodies/teen', None, SK('fur_tan')), (100, 'head/heads/mouse/adult', None, None), (20, 'legs/shorts/shorts', None, CL('brown')), (35, 'torso/clothes/shortsleeve/tshirt', None, CL('green')), (126, 'hat/cloth/leather_cap/adult', 'brown', None), (15, 'feet/boots/basic', None, CL('brown')), W_DAG]),
 ('boarman', 'male', [(10, 'body/bodies/muscular', None, SK('fur_brown')), (100, 'head/heads/boarman/adult', None, None), (20, 'legs/pants', None, CL('leather')), (35, 'torso/armour/plate/male', None, None), (95, 'shield/round', 'brown', None), (90, 'weapon/polearm/spear/foreground', 'bronze', None)]),
 ('alien', 'teen', [(10, 'body/bodies/teen', None, SK('lavender')), (100, 'head/heads/alien/adult', None, None), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('teal')), (20, 'legs/pants', None, CL('navy')), (15, 'feet/shoes/basic', None, CL('navy'))]),
 ('troll', 'male', [(10, 'body/bodies/muscular', None, SK('olive')), (100, 'head/heads/troll/adult', None, None), (20, 'legs/pants', None, CL('walnut')), (15, 'feet/boots/basic', None, CL('brown'))]),
 ('drake', 'male', [(10, 'body/bodies/teen', None, SK('blue')), (100, 'head/heads/lizard/male', None, SK('blue', 'green')), (20, 'legs/pants', None, CL('slate')), (35, 'torso/armour/leather/male', None, None), (90, 'weapon/polearm/spear/foreground', 'bronze', None)]),
 ('sheep', 'teen', [(10, 'body/bodies/teen', None, SK('fur_white')), (100, 'head/heads/sheep/adult', None, None), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('purple')), (20, 'legs/pants', None, CL('navy')), (126, 'hat/magic/wizard/base', None, None)]),
 ('pig', 'male', [(10, 'body/bodies/muscular', None, SK('fur_tan')), (100, 'head/heads/pig/adult', None, None), (20, 'legs/pants', None, CL('maroon')), (35, 'torso/armour/leather/male', None, None), W_AXE]),
 ('orclord', 'male', [(10, 'body/bodies/muscular', None, SK('dark_green')), (100, 'head/heads/orc/male', None, None), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/plate/male', None, None), (126, 'hat/helmet/horned/adult', None, None), W_AXE]),
 ('skelknight', 'male', [(10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton/adult', None, None), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/plate/male', None, None), (126, 'hat/helmet/greathelm/male', None, None), (95, 'shield/heater/original/paint/fg', None, None), W_SWORD]),
 ('minotaur', 'male', [(10, 'body/bodies/muscular', None, SK('fur_brown')), (100, 'head/heads/minotaur/male', None, None), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/leather/male', None, None), W_AXE]),
 ('lich', 'male', [(5, 'cape/tattered/bg', None, CL('purple')), (10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton/adult', None, None), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('purple')), (20, 'legs/pants', None, CL('charcoal')), (126, 'hat/magic/wizard/base', None, None), (110, 'cape/tattered/fg', None, CL('purple')), (90, 'weapon/magic/gnarled/universal/foreground', 'bronze', None)]),
 ('trollking', 'male', [(10, 'body/bodies/muscular', None, SK('pale_green')), (100, 'head/heads/troll/adult', None, None), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/plate/male', None, None), (126, 'hat/helmet/barbarian/adult', None, None), (95, 'shield/heater/original/paint/fg', None, None), W_AXE]),
]
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA')); y, x = ROWS['right'] * 64, 0
    return a[y:y + 64, x:x + 64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def tryfind(p, c, g):
    for pp in (p, p.replace('/foreground', ''), p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    return None
plan = []; missing = []
for mid, g, L in MON:
    ls = []
    for z, p, c, rc in L:
        f = tryfind(p, c, g)
        if f is None: missing.append((mid, p)); continue
        ls.append((z, f, rc))
    plan.append((mid, ls))
need = sorted({f for _, L in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
for i, (mid, L) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]): over(cell, recolor(frame(f), rc))
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'monsters_lpc.png'))
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(sys.argv[2])
