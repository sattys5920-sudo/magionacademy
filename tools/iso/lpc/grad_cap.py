# 시안: 유령 전학생 마틸다 졸업식 보상 「마틸다의 졸업 모자」 (아바타 모자 칸, 64×64 칸 20개 한 줄)
#   학사모는 LPC에 없어서 머리 꼭대기에 검은 띠 + 납작한 판 + 금색 술을 LPC 그림체(3단 음영 + 어두운 테두리)로 그려요
#   python3 grad_cap.py <LPC 저장소 경로> → ../out/hat_grad.png · ../out/hat_grad_preview.png
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC; OUTD = os.path.join(HERE, '..', 'out')
W0, W1, W2, OL = (70, 66, 90), (42, 38, 58), (26, 24, 38), (12, 10, 18); GD, GL = (224, 176, 58), (255, 224, 120)
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
    puff = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(puff); rx = max(7, w // 2); top += 4
    d.rectangle([cx - rx + 1, top - 3, cx + rx - 1, top + 2], fill=W1 + (255,)); d.line([(cx - rx + 1, top + 2), (cx + rx - 1, top + 2)], fill=W2 + (255,))   # 머리에 쓰는 띠
    bw, bh = rx + 6, 3   # 납작한 판 (앞뒤 모습은 마름모처럼, 옆모습은 얇게)
    if i < 10: d.polygon([(cx - bw, top - 4), (cx, top - 4 - bh), (cx + bw, top - 4), (cx, top - 4 + bh)], fill=W1 + (255,)); d.line([(cx - bw, top - 4), (cx, top - 4 - bh), (cx + bw, top - 4)], fill=W0 + (255,))
    else: d.rectangle([cx - bw + 2, top - 6, cx + bw - 2, top - 4], fill=W1 + (255,)); d.line([(cx - bw + 2, top - 6), (cx + bw - 2, top - 6)], fill=W0 + (255,))
    d.point((cx, top - 4 - (bh if i < 10 else 1)), fill=GL + (255,))   # 단추
    tx = cx + (bw - 2 if i not in range(10, 15) else -bw + 2)   # 금색 술은 한쪽으로 늘어져요
    d.line([(cx, top - 4), (tx, top - 3), (tx, top + 4)], fill=GD + (255,)); d.rectangle([tx - 1, top + 4, tx, top + 6], fill=GL + (255,))
    p = np.array(puff); al = p[..., 3] > 0; ring = np.zeros_like(al)
    ring[1:] |= al[:-1]; ring[:-1] |= al[1:]; ring[:, 1:] |= al[:, :-1]; ring[:, :-1] |= al[:, 1:]; ring &= ~al
    under = np.zeros_like(al); under[top + 3:top + 4, :] = True   # 띠 아래 줄은 머리카락 위에 얹히니까 테두리를 그려요
    p[ring] = OL + (255,)
    hat[:, i * 64:(i + 1) * 64] = p
Image.fromarray(hat).save(os.path.join(OUTD, 'hat_grad.png'))
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
pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(os.path.join(OUTD, 'hat_grad_preview.png')); print('ok')
