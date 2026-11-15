# 시안: 새 NPC 셋 (뭉치 · 루시안 · 테오)을 LPC 부품으로 조립해요 → out/newnpc2_lpc.png (한 줄 = 한 명, 64×64 칸 20개) + 미리보기
#   python3 newnpc2_lpc.py <LPC 저장소 경로> [미리보기.png]
#   뭉치: 떠돌이 강아지 (꼬마 몸 전체를 누런 털 색으로 · 늑대 꼬마 머리 · 늑대 꼬리 · 해진 빨간 목도리)
#   루시안: 그림자 골목 거울 수리공 (잿빛 은발 긴 머리 · 검은 프록코트 · 흰 셔츠 · 장갑 · 은 목걸이)
#   테오: 별 지도를 그리는 떠돌이 지도 제작자 (갈색 곱슬머리 · 동그란 안경 · 남색 목도리 · 베이지 재킷 · 가방 끈)
import sys, os, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out'); SK, HR, CL = N.SK, N.HR, N.CL
FUR = (196, 150, 92)   # 누런 털
def tint(a, rgb):   # 그림의 밝기는 살리고 색만 털 색으로 (pet_lpc.py 와 같은 식)
    o = a.copy(); lum = (a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114); on = a[..., 3] > 0; mean = lum[on].mean() if on.any() else 150
    k = np.clip(.95 + (lum - mean) / 110, .5, 1.3)[..., None]; o[..., :3] = np.clip(np.array(rgb)[None, None, :] * k, 0, 255).astype(np.uint8); return o
T = ('TINT', FUR)
NPC = [
 ('뭉치', 'child', [(5, 'body/tail/wolf/child/bg', 'light', T), (10, 'body/bodies/child', None, T), (100, 'head/heads/wolf/child', None, T),
   (60, 'neck/scarf', None, CL('red')), (125, 'body/tail/wolf/child/fg', 'light', T)]),
 ('루시안', 'male', [(10, 'body/bodies/male', None, SK('light')), (100, 'head/heads/human/male', None, SK('light')), (105, 'eyes/human/adult/default', 'gray', None),
   (20, 'legs/pants', None, CL('black')), (35, 'torso/clothes/longsleeve/formal', None, CL('white')), (40, 'torso/jacket/frock', 'black', None),
   (60, 'neck/necklace/chain', None, None), (15, 'feet/boots/basic', None, CL('black')), (45, 'arms/hands/gloves', None, CL('black')), (120, 'hair/curtains_long', None, HR('white'))]),
 ('테오', 'male', [(10, 'body/bodies/male', None, SK('light')), (100, 'head/heads/human/male', None, SK('light')), (105, 'eyes/human/adult/default', 'brown', None),
   (20, 'legs/pants', None, CL('brown')), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('white')), (40, 'torso/jacket/collared', 'tan', None),
   (60, 'neck/scarf', None, CL('navy')), (15, 'feet/boots/basic', None, CL('brown')), (8, 'backpack/straps', None, CL('brown')), (120, 'hair/curly_short', None, HR('dark_brown')),
   (130, 'facial/glasses/round', None, None)]),
]
plan = []
for nm, g, L in NPC:
    ps = []
    for z, p, c, rc in L:
        try: ps.append((z, N.find(p, c, g), rc))
        except SystemExit as e: print('빠짐', nm, p, e)
    plan.append((nm, ps))
need = sorted({f for _, L in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
sheet = np.zeros((64 * len(plan), 64 * 20, 4), np.uint8)
for r, (nm, L) in enumerate(plan):
    row = np.zeros((64, 64 * 20, 4), np.uint8)
    for z, f, rc in sorted(L, key=lambda t: t[0]):
        keep = any(w in f for w in ('/hair/', '/heads/', '/ears/', '/hat/', '/facial/', '/eyes/'))
        a = N.strip_frames(Image.open(os.path.join(LPC, f)), not keep)
        N.over(row, tint(a, rc[1]) if rc and rc[0] == 'TINT' else N.recolor(a, rc))
    sheet[r * 64:(r + 1) * 64] = row
    print(nm, [f.split('spritesheets/')[-1] for _, f, _ in L])
os.makedirs(OUTD, exist_ok=True)
im = Image.fromarray(sheet); im.save(os.path.join(OUTD, 'newnpc2_lpc.png'))
if len(sys.argv) > 2:   # 미리보기: 사람마다 아래 · 왼쪽 · 위 · 오른쪽 + 걷기 한 칸 (4 배)
    pv = Image.new('RGBA', (64 * 5, 66 * len(plan)), (40, 30, 56, 255))
    for r in range(len(plan)):
        for j, i in enumerate((0, 10, 5, 15, 2)): pv.alpha_composite(im.crop((i * 64, r * 64, i * 64 + 64, r * 64 + 64)), (j * 64, r * 66 + 1))
    pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(sys.argv[2])
