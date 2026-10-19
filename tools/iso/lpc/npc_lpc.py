# 이야기 NPC(사람이 아닌 13명)를 LPC 부품으로 조립해요 → public/art/npcs.png
#   한 줄 = NPC 하나, 64×64 칸 20개 (아래·위·왼쪽·오른쪽 × 서기 + 걷기 4) — 게임 캐릭터(public/art/lpc)와 같은 칸 배치·같은 화풍
#   python3 npc_lpc.py <LPC 저장소 경로> [미리보기.png]
#   몸은 캐릭터와 같은 teen 체형을 같은 방식으로 날씬하게 (SLIM)
#   0 나비 1 배트리 2 캇파 3 아울라 4 맨디 (이 다섯은 beasts.py의 동물 그림으로 덮어요) 5 짚신 / 6 루시안 7 부우 8 헤이즐 9 울프강 10 미라벨 11 프랭키 12 잭
import sys, os, json, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
LPC = sys.argv[1]; FILES = set(l.strip() for l in open(os.path.join(LPC, '..', 'lpc_files.txt')))
PAL = {m: json.load(open(os.path.join(LPC, 'palette_definitions', m, f'{m}_ulpc.json'))) for m in ('body', 'hair', 'eye', 'cloth')}
ROWS = {'down': 2, 'up': 0, 'left': 1, 'right': 3}; DIRS = ['down', 'up', 'left', 'right']; COLS = [0, 1, 3, 5, 7]
def find(p, color=None, g='teen'):
    """부품 폴더 → 실제 walk 그림 (색 이름이 있으면 그 색 그림, 없으면 기본 그림을 팔레트로)"""
    p = 'spritesheets/' + p.strip('/')
    for sub in ('', '/' + g, '/adult', '/teen', '/female', '/male', '/thin'):
        for f in ([f'{p}{sub}/walk/{color}.png', f"{p}{sub}/walk/{color.replace(' ', '_')}.png"] if color else []) + [f'{p}{sub}/walk.png']:
            if f in FILES: return f
    for sub in ('', '/' + g, '/adult', '/teen', '/female', '/male', '/thin'):   # 색 그림만 있으면 흰색(팔레트로 바꿔 칠해요)
        for c in ('white', 'gray', 'light_gray'):
            if f'{p}{sub}/walk/{c}.png' in FILES: return f'{p}{sub}/walk/{c}.png'
    raise SystemExit('없어요: ' + p + ' ' + str(color))
# 층: (z, 폴더, 색 그림 이름 또는 None, 팔레트 바꾸기 (재질, 원래, 바꿀 색) 또는 None)
SK = lambda dst, src='light': ('body', src, dst)
HR = lambda dst: ('hair', 'orange', dst)
CL = lambda dst: ('cloth', 'white', dst)
NPC = [
 ('나비', 'female', [(5, 'body/tail/cat/adult/bg', 'ginger', None), (10, 'body/bodies/teen', None, SK('light')), (100, 'head/heads/human/female', None, SK('light')), (105, 'eyes/human/adult/default', 'green', None),
   (8, 'head/ears/cat/adult/bg', 'ginger', None), (20, 'legs/skirts/plain', None, CL('maroon')), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('white')), (40, 'torso/aprons/apron', 'brown', None),
   (15, 'feet/shoes/basic', None, CL('brown')), (120, 'hair/bob', None, HR('ginger')), (125, 'body/tail/cat/adult/fg', 'ginger', None), (130, 'head/ears/cat/adult/fg', 'ginger', None)]),
 ('배트리', 'male', [(5, 'body/wings/bat/adult/bg', 'dark gray', None), (10, 'body/bodies/teen', None, SK('lavender')), (100, 'head/heads/human/male', None, SK('lavender')), (105, 'eyes/human/adult/default', 'purple', None),
   (20, 'legs/pants', None, CL('charcoal')), (35, 'torso/clothes/longsleeve/longsleeve', None, CL('lavender')), (15, 'feet/shoes/basic', None, CL('black')), (120, 'hair/spiked', None, HR('black')),
   (126, 'hat/cloth/leather_cap', None, CL('navy')), (105.5, 'body/wings/bat/adult/fg', 'dark gray', None)]),
 ('캇파', 'male', [(10, 'body/bodies/teen', None, SK('green')), (100, 'head/heads/lizard/male', None, SK('green', 'green')), (20, 'legs/shorts/shorts', None, CL('tan')),
   (35, 'torso/clothes/shortsleeve/tshirt', None, CL('sky')), (40, 'torso/aprons/overalls', 'blue', None), (15, 'feet/sandals', None, CL('brown')), (126, 'hat/formal/bowler', None, CL('tan'))]),
 ('아울라', 'female', [(5, 'body/wings/feathered/adult/bg', 'dark brown', None), (10, 'body/bodies/teen', None, SK('amber')), (100, 'head/heads/human/female', None, SK('amber')), (105, 'eyes/human/adult/default', 'orange', None),
   (20, 'legs/skirts/plain', None, CL('brown')), (35, 'torso/clothes/robe', 'brown', None), (15, 'feet/shoes/basic', None, CL('brown')), (120, 'hair/bunches/adult/bg', None, HR('light brown')),
   (121, 'hair/bunches/adult/fg', None, HR('light brown')), (110, 'head/ears/avyon', None, SK('fur_brown', 'fur_brown')), (130, 'facial/glasses/glasses', None, CL('gold'))]),
 ('맨디', 'female', [(10, 'body/bodies/teen', None, SK('pale_green')), (100, 'head/heads/human/female', None, SK('pale_green')), (105, 'eyes/human/adult/default', 'brown', None),
   (20, 'legs/skirts/plain', None, CL('forest')), (35, 'torso/clothes/sleeveless/sleeveless', None, CL('green')), (15, 'feet/slippers', None, CL('brown')), (120, 'hair/pixie', None, HR('green'))]),
 ('짚신', 'male', [(10, 'body/bodies/teen', None, SK('taupe')), (100, 'head/heads/human/male', None, SK('taupe')), (105, 'eyes/human/adult/default', 'brown', None), (20, 'legs/pants', None, CL('blue')),
   (35, 'torso/clothes/longsleeve/longsleeve', None, CL('red')), (40, 'torso/aprons/suspenders', 'brown', None), (15, 'feet/boots/basic', None, CL('brown')), (120, 'hair/messy1', None, HR('blonde')),
   (126, 'hat/cloth/bandana', None, CL('yellow'))]),
 ('루시안', 'male', [(5, 'cape/solid/bg', None, CL('red')), (10, 'body/bodies/teen', None, SK('lavender')), (100, 'head/heads/vampire', None, None), (105, 'eyes/human/adult/default', 'red', None),
   (20, 'legs/formal', None, CL('black')), (35, 'torso/clothes/longsleeve/formal', None, CL('white')), (40, 'torso/jacket/collared', 'black', None), (15, 'feet/shoes/basic', None, CL('black')),
   (120, 'hair/parted', None, HR('black')), (60, 'neck/tie/bowtie', None, CL('red')), (110, 'cape/solid/fg', None, CL('black'))]),
 ('부우', 'female', [(10, 'body/bodies/teen', None, SK('fur_white', 'light')), (100, 'head/heads/human/female', None, SK('fur_white')), (105, 'eyes/human/adult/default', 'blue', None),
   (35, 'torso/clothes/robe', 'white', None), (126, 'hat/cloth/hood', None, CL('white'))]),
 ('헤이즐', 'female', [(10, 'body/bodies/teen', None, SK('light')), (100, 'head/heads/human/female', None, SK('light')), (105, 'eyes/human/adult/default', 'green', None),
   (35, 'torso/clothes/robe', 'purple', None), (15, 'feet/boots/basic', None, CL('black')), (120, 'hair/long', None, HR('redhead')), (126, 'hat/magic/large', 'brown', ('cloth', 'auto', 'purple'))]),
 ('울프강', 'male', [(5, 'body/tail/wolf/adult/bg', 'gray', None), (10, 'body/bodies/teen', None, SK('fur_grey')), (100, 'head/heads/wolf/male', None, SK('fur_grey', 'fur_brown')),
   (20, 'legs/pants', None, CL('brown')), (35, 'torso/clothes/sleeveless/sleeveless', None, CL('slate')), (125, 'body/tail/wolf/adult/fg', 'gray', None)]),
 ('미라벨', 'female', [(10, 'body/bodies/teen', None, SK('taupe')), (100, 'head/heads/human/female', None, SK('taupe')), (105, 'eyes/human/adult/default', 'orange', None),
   (35, 'torso/bandage', 'white', None), (20, 'legs/leggings', None, CL('white')), (15, 'feet/slippers', None, CL('white')), (126, 'hat/cloth/bandana', None, CL('white')), (130, 'hat/headband/hairtie', None, CL('pink'))]),
 ('프랭키', 'male', [(10, 'body/bodies/teen', None, SK('zombie_green')), (100, 'head/heads/frankenstein', None, SK('zombie_green')), (20, 'legs/pants', None, CL('charcoal')),
   (35, 'torso/clothes/longsleeve/longsleeve', None, CL('gray')), (40, 'torso/jacket/collared', 'black', None), (15, 'feet/boots/basic', None, CL('black'))]),
 ('잭', 'male', [(5, 'cape/tattered/bg', None, CL('brown')), (10, 'body/bodies/teen', None, SK('taupe')), (100, 'head/heads/jack', 'jack', None), (20, 'legs/pants', None, CL('brown')),
   (35, 'torso/clothes/longsleeve/longsleeve', None, CL('orange')), (40, 'torso/aprons/suspenders', 'black', None), (15, 'feet/boots/basic', None, CL('brown')), (110, 'cape/tattered/fg', None, CL('brown'))]),
]
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def recolor(a, rc):
    if not rc: return a
    mat, src, dst = rc
    if src == 'auto':   # 원래 색을 몰라요 → 그림 픽셀과 가장 많이 맞는 팔레트
        px_ = a[a[..., 3] > 0][:, :3].astype(int)
        src = max(PAL[mat], key=lambda k: sum(int((np.abs(px_ - np.array(hx(c))).max(1) <= 2).sum()) for c in PAL[mat][k]))
    S = [hx(c) for c in PAL[mat].get(src, [])]; D = [hx(c) for c in PAL[mat].get(dst, [])]
    if not S or not D: return a
    out = a.copy(); rgb = a[..., :3]
    for i, s in enumerate(S):
        m = np.all(rgb == s, axis=-1) & (a[..., 3] > 0); out[m, :3] = D[min(i, len(D) - 1)]
    return out
# 캐릭터와 같은 날씬한 몸: build_lpc.py의 PRESET 'legs4'와 같은 세로줄을 빼서 몸통·다리를 안으로 당겨요
SLIM = [(33, 51, {'down': {21, 28, 35, 42}, 'up': {21, 28, 35, 42}, 'left': {28, 31, 34, 37}, 'right': {26, 29, 32, 35}}),
        (51, 64, {'down': {28, 31, 32, 35}, 'up': {28, 31, 32, 35}, 'left': {29, 32, 35}, 'right': {28, 31, 34}})]
def slim(cell, d, neck=True):
    o = cell.copy()
    for y0, y1, cols in SLIM:
        if not neck: y0 = max(y0, 36)        # 머리카락·머리: 어깨 줄은 그대로
        C = cols[d]; keep = [x for x in range(64) if x not in C]; nl = sum(1 for c in C if c < 32)
        b = cell[y0:y1][:, keep]; o[y0:y1] = 0; o[y0:y1, nl:nl + len(keep)] = b
    return o
def strip_frames(img, neck=True):
    """walk.png (9칸 × 4줄) → 20칸 (방향 4 × [서기, 걷기 4]), 날씬하게"""
    out = np.zeros((64, 64 * 20, 4), np.uint8); a = np.array(img.convert('RGBA'))
    for di, d in enumerate(DIRS):
        for ci, c in enumerate(COLS):
            y, x = ROWS[d] * 64, c * 64
            if y + 64 <= a.shape[0] and x + 64 <= a.shape[1]: out[:, (di * 5 + ci) * 64:(di * 5 + ci + 1) * 64] = slim(a[y:y + 64, x:x + 64], d, neck)
    return out
def over(dst, src):
    al = src[..., 3:4] / 255.0; dst[..., :3] = (src[..., :3] * al + dst[..., :3] * (1 - al)).astype(np.uint8); dst[..., 3] = np.maximum(dst[..., 3], src[..., 3])
if __name__ == '__main__':
    plan = [(name, g, [(z, find(p, c, g), rc) for z, p, c, rc in L]) for name, g, L in NPC]
    need = sorted({f for _, _, L in plan for _, f, _ in L if not os.path.exists(os.path.join(LPC, f))})
    if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
    sheet = np.zeros((64 * len(plan), 64 * 20, 4), np.uint8)
    for r, (name, g, L) in enumerate(plan):
        row = np.zeros((64, 64 * 20, 4), np.uint8)
        for z, f, rc in sorted(L, key=lambda t: t[0]): over(row, recolor(strip_frames(Image.open(os.path.join(LPC, f)), not any(w in f for w in ('/hair/', '/heads/', '/ears/', '/hat/', '/facial/', '/eyes/'))), rc))
        sheet[r * 64:(r + 1) * 64] = row
    # 동물 NPC(0 나비 고양이 · 1 배트리 박쥐 · 2 캇파 · 3 아울라 부엉이 · 4 맨디 맨드레이크)는 진짜 동물 그림으로 (beasts.py, 같은 칸 크기)
    sys.path.insert(0, HERE); from beasts import BEASTS
    for r, f in enumerate(BEASTS):
        b = f(); sheet[r * 64:(r + 1) * 64] = np.tile(b, (1, 20, 1))
    # 생성형으로 뽑은 시트가 있으면 그걸로 (4방향 걷기까지): gen_npcs.py · tools/iso/npc_src/
    from gen_npcs import all_gen
    for r, strip in all_gen(): sheet[r * 64:(r + 1) * 64] = strip
    Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'npcs.png'))
    if len(sys.argv) > 2:   # 미리보기: 앞모습만 크게
        pv = Image.new('RGBA', (64 * len(plan), 64), (250, 241, 226, 255))
        for r in range(len(plan)): pv.alpha_composite(Image.fromarray(sheet[r * 64:(r + 1) * 64, 0:64]), (r * 64, 0))
        pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST).save(sys.argv[2])
    print('npcs', len(plan))
