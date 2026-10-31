# 신규 NPC 「무슈 블랑」(100년 전 학교 식당 요리장 유령)을 LPC 부품으로 조립해요 → out/blanc_lpc.png (npcs.png 한 줄과 같은 64×64 칸 20개)
#   요리사 모자는 LPC에 없어서 실크해트를 흰색으로 칠하고 위에 부푼 윗부분을 LPC 그림체로 얹어요 · 몸은 반투명 하늘빛, 다리 쪽은 흐려지며 둥실 떠요
#   python3 blanc_lpc.py <LPC 저장소 경로> [미리보기.png]
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out')
L = [(10, 'body/bodies/teen', None, N.SK('fur_white')), (100, 'head/heads/human/male', None, N.SK('fur_white')), (105, 'eyes/human/adult/default', 'blue', None),
     (20, 'legs/pants', None, N.CL('white')), (35, 'torso/clothes/longsleeve/formal', None, N.CL('white')), (40, 'torso/aprons/apron', 'white', None),
     (60, 'neck/tie/bowtie', None, N.CL('red')), (112, 'beards/mustache/handlebar', None, 'MUS'), (118, 'hair/plain', None, N.HR('gray'))]
plan = [(z, N.find(p, c, 'male'), rc) for z, p, c, rc in L]
need = sorted({f for _, f, _ in plan if not os.path.exists(os.path.join(LPC, f))})
if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
def mus(a):   # 콧수염 그림은 팔레트 밖 갈색 두 가지라 직접 칠해요 (짙은 은회색)
    o = a.copy(); rgb = a[..., :3]
    for src, dst in (((121, 65, 23), (52, 54, 68)), ((161, 96, 24), (104, 108, 126))): o[np.all(rgb == src, axis=-1) & (a[..., 3] > 0), :3] = dst
    return o
def layer(f, rc):
    if rc == 'MUS': return mus(N.strip_frames(Image.open(os.path.join(LPC, f)), False))
    return N.recolor(N.strip_frames(Image.open(os.path.join(LPC, f)), not any(w in f for w in ('/hair/', '/heads/', '/ears/', '/hat/', '/facial/', '/eyes/', '/beards/'))), rc)
row = np.zeros((64, 64 * 20, 4), np.uint8); hat = None   # hat: 머리 층 (요리사 모자를 얹을 자리)
for z, f, rc in sorted(plan, key=lambda t: t[0]):
    a = layer(f, rc)
    if '/heads/' in f: hat = a
    N.over(row, a)
# 요리사 모자: 칸마다 머리 꼭대기에 흰 띠 + 부푼 구름 모양 윗부분 (흰색 3단 음영 + 어두운 테두리)
W0, W1, W2, OL = (246, 244, 238), (214, 210, 202), (176, 170, 162), (70, 62, 66)
for i in range(20):
    cell = hat[:, i * 64:(i + 1) * 64, 3] > 0
    if not cell.any(): continue
    ys, xs = np.nonzero(cell); top, cx = ys.min(), int(round(xs.mean())); w = xs.max() - xs.min() + 1
    puff = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(puff); rx = max(6, w // 2); top += 2
    d.rectangle([cx - rx + 1, top - 3, cx + rx - 1, top + 2], fill=W1 + (255,)); d.rectangle([cx - rx + 1, top - 3, cx - rx + 3, top + 2], fill=W0 + (255,)); d.line([(cx - rx + 1, top + 2), (cx + rx - 1, top + 2)], fill=W2 + (255,))   # 띠
    for dx, dy, r in ((-rx * .5, -6, rx * .62), (rx * .5, -6, rx * .62), (0, -9, rx * .66)): d.ellipse([cx + dx - r, top + dy - r * .75, cx + dx + r, top + dy + r * .75], fill=W1 + (255,))
    for dx, dy, r in ((-rx * .55, -7, rx * .42), (-rx * .1, -10, rx * .42)): d.ellipse([cx + dx - r, top + dy - r * .65, cx + dx + r * .7, top + dy + r * .5], fill=W0 + (255,))
    for dx in (-rx * .3, rx * .3): d.line([(cx + dx, top - 4), (cx + dx, top - 8)], fill=W2 + (255,))
    p = np.array(puff); al = p[..., 3] > 0; ring = np.zeros_like(al)
    ring[1:] |= al[:-1]; ring[:-1] |= al[1:]; ring[:, 1:] |= al[:, :-1]; ring[:, :-1] |= al[:, 1:]; ring &= ~al
    cellrow = row[:, i * 64:(i + 1) * 64]; body = cellrow[..., 3] > 0
    p[ring & ~body] = OL + (255,)
    N.over(cellrow, p)
# 유령: 하늘빛을 섞고 반투명, 다리 쪽은 흐려지며 위로 떠요 (떠다니는 칸은 위아래로 흔들려요)
out = np.zeros_like(row); BOB = [0, -1, -2, -1, 0]
for i in range(20):
    c = row[:, i * 64:(i + 1) * 64].astype(float)
    on = c[..., 3] > 0; c[on, :3] = np.minimum(255, c[on, :3] * .74 + np.array([205, 228, 255]) * .26 + 10)
    fade = np.clip((60 - np.arange(64)) / 16, 0, 1)[:, None]; c[..., 3] *= np.where(np.arange(64)[:, None] < 44, .96, .96 * fade)
    dy = -4 + BOB[i % 5]; sh = np.zeros_like(c); sh[max(0, -dy):64 + min(0, -dy)] = c[max(0, dy):64 + min(0, dy)] if dy >= 0 else c[-dy:]
    if dy < 0: sh = np.zeros_like(c); sh[:64 + dy] = c[-dy:]
    gl = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse([24, 58, 40, 61], fill=(150, 190, 255, 70))   # 발밑 희미한 빛
    g = np.array(gl).astype(float); N.over(g, np.clip(sh, 0, 255).astype(np.uint8)); out[:, i * 64:(i + 1) * 64] = g.astype(np.uint8)
Image.fromarray(out).save(os.path.join(OUTD, 'blanc_lpc.png'))
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * 6, 64), (40, 30, 56, 255)); im = Image.fromarray(out)
    for j, i in enumerate((0, 2, 5, 10, 15)): pv.alpha_composite(im.crop((i * 64, 0, i * 64 + 64, 64)), (j * 64, 0))
    ref = Image.open(os.path.join(HERE, '..', '..', '..', 'public', 'art', 'npcs.png')).convert('RGBA').crop((0, 64 * 6, 64, 64 * 7)); pv.alpha_composite(ref, (5 * 64, 0))
    big = pv.resize((pv.width * 4, pv.height * 4), Image.NEAREST); face = im.crop((16, 2, 48, 34)).resize((256, 256), Image.NEAREST)
    fr = Image.new('RGBA', (big.width + 300, big.height), (40, 30, 56, 255)); fr.alpha_composite(big, (0, 0)); fr.alpha_composite(face, (big.width + 22, 0)); fr.save(sys.argv[2])
print('blanc ok')
