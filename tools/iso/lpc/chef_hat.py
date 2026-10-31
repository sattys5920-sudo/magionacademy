# 무슈 블랑 「열두 밤 만찬」 보상: 학생용 요리사 모자 (아바타 모자 칸, 64×64 칸 20개 한 줄)
#   요리사 모자는 LPC에 없어서 블랑 모자와 같은 방법으로 머리 꼭대기에 흰 띠 + 부푼 윗부분을 LPC 그림체(3단 흰색 + 어두운 테두리)로 그려요
#   python3 chef_hat.py <LPC 저장소 경로> → ../out/hat_chef.png · ../out/hat_chef_preview.png (학생 둘에게 씌운 미리보기)
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out')
W0, W1, W2, OL = (246, 244, 238), (214, 210, 202), (176, 170, 162), (70, 62, 66)
def sheet(p, rc=None, g='male', neck=False):
    f = N.find(p, None, g)
    if not os.path.exists(os.path.join(LPC, f)): subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', f], check=True)
    a = N.strip_frames(Image.open(os.path.join(LPC, f)), neck); return N.recolor(a, rc) if rc else a
head = sheet('head/heads/human/male')
hat = np.zeros((64, 64 * 20, 4), np.uint8)
for i in range(20):
    cell = head[:, i * 64:(i + 1) * 64, 3] > 0
    if not cell.any(): continue
    ys, xs = np.nonzero(cell); top, cx = ys.min(), int(round(xs.mean())); w = xs.max() - xs.min() + 1
    side = i >= 10   # 옆모습은 모자를 뒤로 살짝
    puff = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(puff); rx = max(7, w // 2); top += 5   # 띠가 이마 위 머리카락을 덮게
    d.rectangle([cx - rx, top - 2, cx + rx, top + 2], fill=W1 + (255,)); d.rectangle([cx - rx, top - 2, cx - rx + 2, top + 2], fill=W0 + (255,)); d.line([(cx - rx, top + 2), (cx + rx, top + 2)], fill=W2 + (255,))   # 띠
    sh = (-1 if i < 15 else 1) * 2 if side else 0
    for dx, dy, r in ((-rx * .42, -5, rx * .52), (rx * .42, -5, rx * .52), (0, -8, rx * .58)): d.ellipse([cx + sh + dx - r, top + dy - r * .72, cx + sh + dx + r, top + dy + r * .72], fill=W1 + (255,))   # 부푼 윗부분을 낮고 작게
    for dx, dy, r in ((-rx * .45, -6, rx * .36), (-rx * .05, -9, rx * .36)): d.ellipse([cx + sh + dx - r, top + dy - r * .6, cx + sh + dx + r * .7, top + dy + r * .45], fill=W0 + (255,))
    for dx in (-rx * .3, rx * .3): d.line([(cx + sh + dx, top - 4), (cx + sh + dx, top - 6)], fill=W2 + (255,))
    p = np.array(puff); al = p[..., 3] > 0; ring = np.zeros_like(al)
    ring[1:] |= al[:-1]; ring[:-1] |= al[1:]; ring[:, 1:] |= al[:, :-1]; ring[:, :-1] |= al[:, 1:]; ring &= ~al
    under = np.zeros_like(al); under[top + 3:top + 4, :] = True   # 띠 아래 줄은 머리카락 위에 얹히니까 테두리를 그려요
    p[ring] = OL + (255,)
    if i in range(5, 10): p[(np.arange(64)[:, None] > top + 2) & al] = 0   # 뒷모습은 띠 아래를 비워요
    hat[:, i * 64:(i + 1) * 64] = p
Image.fromarray(hat).save(os.path.join(OUTD, 'hat_chef.png'))
# 미리보기: 학생 두 명 (갈색 단발 여학생 · 검은 머리 남학생)에게 씌워요
studs = []
for g, hair, hc, top in (('female', 'hair/bob', 'brown', 'torso/clothes/longsleeve/formal'), ('male', 'hair/plain', 'black', 'torso/clothes/longsleeve/formal')):
    row = np.zeros((64, 64 * 20, 4), np.uint8)
    for p, rc, nk in (('body/bodies/teen', None, True), ('head/heads/human/' + g, None, False), ('eyes/human/adult/default', None, False), ('legs/pants', N.CL('navy'), True), (top, N.CL('maroon'), True), (hair, N.HR(hc), False)):
        try: N.over(row, sheet(p, rc, g, nk))
        except Exception as e: print('skip', p, e)
    N.over(row, hat); studs.append(row)
pv = Image.new('RGBA', (64 * 8, 64 * 2), (52, 40, 72, 255))
for r, row in enumerate(studs):
    im = Image.fromarray(row)
    for j, i in enumerate((0, 2, 5, 7, 10, 12, 15, 17)): pv.alpha_composite(im.crop((i * 64, 0, i * 64 + 64, 64)), (j * 64, r * 64))
pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(os.path.join(OUTD, 'hat_chef_preview.png')); print('ok')
