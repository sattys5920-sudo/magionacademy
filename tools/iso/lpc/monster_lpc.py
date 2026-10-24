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
 ('trollking', 'male', [(10, 'body/bodies/muscular', None, SK('pale_green')), (100, 'head/heads/troll/adult', None, None), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/plate/male', None, None), (126, 'hat/formal/crown', None, None), (95, 'shield/heater/original/paint/fg', None, None), W_AXE]),
 ('fairy', 'child', [(5, 'body/wings/pixie/solid', None, None), (10, 'body/bodies/child', None, SK('pale_green')), (100, 'head/heads/human/child', None, SK('pale_green')), (105, 'eyes/human/child/default', 'green', None), (35, 'torso/clothes/shirt/child', None, CL('forest')), (20, 'legs/pants', None, CL('green')), (120, 'hair/messy1', None, HR('green')), (110, 'head/ears/elven/child', None, SK('pale_green'))]),
 ('hare', 'child', [(10, 'body/bodies/child', None, SK('fur_tan')), (100, 'head/heads/rabbit/child', None, None), (35, 'torso/clothes/shirt/child', None, CL('rose')), (20, 'legs/pants', None, CL('brown'))]),
 ('dragonfly', 'child', [(5, 'body/wings/dragonfly/solid', None, None), (10, 'body/bodies/child', None, SK('green')), (100, 'head/heads/goblin/child', None, None), (35, 'torso/clothes/shirt/child', None, CL('teal')), (20, 'legs/pants', None, CL('navy'))]),
 ('piglet', 'child', [(10, 'body/bodies/child', None, SK('fur_tan')), (100, 'head/heads/boarman/child', None, None), (35, 'torso/clothes/shirt/child', None, CL('orange')), (20, 'legs/pants', None, CL('leather'))]),
 ('goblinking', 'male', [(5, 'cape/solid/bg', None, CL('maroon')), (10, 'body/bodies/muscular', None, SK('green')), (100, 'head/heads/goblin/adult', None, None), (20, 'legs/pants', None, CL('leather')), (35, 'torso/armour/leather/male', None, None), (126, 'hat/formal/crown', None, None), (110, 'cape/solid/fg', None, CL('maroon')), W_SWORD]),
 ('skelarcher', 'male', [(10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton/adult', None, None), (126, 'hat/cloth/hood', None, CL('forest')), (35, 'torso/clothes/sleeveless/sleeveless', None, CL('forest')), (8, 'spritesheets/weapon/ranged/bow/normal/walk/background/normal.png', None, None), (90, 'spritesheets/weapon/ranged/bow/normal/walk/foreground/normal.png', None, None)]),
 ('wraith', 'male', [(10, 'body/bodies/skeleton', None, None), (100, 'head/heads/skeleton/adult', None, None), (35, 'torso/clothes/robe/female', 'white', None), (126, 'hat/cloth/hood', None, CL('white')), ('alpha', .62)]),
 ('moonfairy', 'child', [(5, 'body/wings/lunar/bg', None, None), (10, 'body/bodies/child', None, SK('lavender')), (100, 'head/heads/human/child', None, SK('lavender')), (105, 'eyes/human/child/default', 'blue', None), (35, 'torso/clothes/shirt/child', None, CL('navy')), (20, 'legs/pants', None, CL('navy')), (120, 'hair/messy1', None, HR('platinum')), (110, 'body/wings/lunar/fg', None, None)]),
 ('lizard', 'male', [(10, 'body/bodies/teen', None, SK('blue')), (100, 'head/heads/lizard/male', None, SK('blue', 'green')), (20, 'legs/shorts/shorts', None, CL('tan')), (35, 'torso/clothes/sleeveless/sleeveless', None, CL('navy')), (90, 'weapon/polearm/trident', None, None)]),
 ('babytroll', 'child', [(10, 'body/bodies/child', None, SK('olive')), (100, 'head/heads/troll/child', None, None), (20, 'legs/pants', None, CL('walnut'))]),
 ('butterfly', 'child', [(5, 'body/wings/monarch/base', None, None), (10, 'body/bodies/child', None, SK('fur_tan')), (100, 'head/heads/mouse/child', None, None), (35, 'torso/clothes/shirt/child', None, CL('orange')), (20, 'legs/pants', None, CL('brown'))]),
 ('lizardking', 'male', [(5, 'body/wings/lizard/adult', None, None), (10, 'body/bodies/muscular', None, SK('blue')), (100, 'head/heads/lizard/male', None, SK('blue', 'green')), (20, 'legs/pants', None, CL('slate')), (35, 'torso/armour/plate/male', None, None), (126, 'hat/formal/crown', None, None), (90, 'weapon/polearm/trident', None, None)]),
 ('bronze', 'male', [(10, 'body/bodies/muscular', None, SK('bronze')), (100, 'head/heads/human/male', None, SK('bronze')), (20, 'legs/armour/plate/male', None, None), (35, 'torso/armour/legion/male', None, None), (126, 'hat/helmet/legion/adult', None, None), (95, 'shield/round', 'gold', None), (90, 'weapon/polearm/spear/foreground', 'bronze', None)]),
 ('shadowman', 'male', [(10, 'body/bodies/teen', None, SK('black')), (100, 'head/heads/human/male', None, SK('black')), (126, 'hat/cloth/hood', None, CL('charcoal')), (35, 'torso/jacket/trench', None, CL('black')), (20, 'legs/pants', None, CL('black')), W_DAG]),
 ('firepriest', 'female', [(10, 'body/bodies/teen', None, SK('amber')), (100, 'head/heads/human/female', None, SK('amber')), (105, 'eyes/human/adult/default', 'orange', None), (35, 'torso/clothes/robe', 'maroon', None), (126, 'hat/magic/celestial/adult', None, None), (90, 'weapon/magic/gnarled/universal/foreground', 'bronze', None)]),
]
CROWN_DY = {'goblinking': 4, 'lizardking': 4}
def frame(f):
    a = np.array(Image.open(os.path.join(LPC, f)).convert('RGBA'))
    if a.shape[0] == 512:   # 큰 무기(활)는 128칸 — 가운데 64칸만 잘라 써요
        y = ROWS['right'] * 128; return a[y + 32:y + 96, 32:96]
    y, x = ROWS['right'] * 64, 0
    return a[y:y + 64, x:x + 64] if y + 64 <= a.shape[0] else np.zeros((64, 64, 4), np.uint8)
def tryfind(p, c, g):
    for pp in (p, p.replace('/foreground', ''), p + '/foreground', p + '/universal'):
        try: return find(pp, c, g)
        except SystemExit: pass
    from npc_lpc import FILES
    cand = sorted(f for f in FILES if f.startswith('spritesheets/' + p + '/') and '/walk' in f and f.endswith('.png') and '/behind' not in f and '/background' not in f)
    if c: cand = [f for f in cand if c in f] or cand
    return cand[0] if cand else None
plan = []; missing = []
for mid, g, L in MON:
    ls = []
    for t in L:
        if t[0] == 'alpha': ls.append((t[0], t[1], None)); continue
        z, p, c, rc = t
        f = p if p.startswith('spritesheets/') else tryfind(p, c, g)
        if f is None: missing.append((mid, p)); continue
        ls.append((z, f, rc))
    plan.append((mid, ls))
need = sorted({f for _, L in plan for z, f, _ in L if z != 'alpha' and not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64, 64 * len(plan), 4), np.uint8)
for i, (mid, L) in enumerate(plan):
    cell = np.zeros((64, 64, 4), np.uint8)
    al = next((t[1] for t in L if t[0] == 'alpha'), 1)
    for z, f, rc in sorted((t for t in L if t[0] != 'alpha'), key=lambda t: t[0]):
        fr = recolor(frame(f), rc)
        if 'formal/crown' in f and mid in CROWN_DY: fr = np.roll(fr, CROWN_DY[mid], axis=0)   # 머리가 낮은 왕은 왕관을 내려 써요
        over(cell, fr)
    cell[..., 3] = (cell[..., 3] * al).astype(np.uint8)
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'monsters_lpc.png'))
print('없는 부품:', missing)
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(plan), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(sys.argv[2])
