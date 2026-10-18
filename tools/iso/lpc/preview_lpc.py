# LPC 부품 미리보기 (게임과 같은 규칙: 팔레트 바꿔 칠하기, z 순서)
import json, os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
M = json.load(open(os.path.join(HERE, '..', 'out', 'lpc_meta.json'))); FW, FH, NF = M['fw'], M['fh'], M['frames']
IMG = {}
def img(f):
    if f not in IMG: IMG[f] = np.array(Image.open(os.path.join(ROOT, 'public', f)).convert('RGBA'))
    return IMG[f]
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
MAT = {'skin': 'skin', 'eye': 'eye', 'hair': 'hair', 'top': 'cloth', 'legs': 'cloth', 'feet': 'cloth', 'hat': 'cloth', 'neck': 'cloth'}
def compose(av):
    body = M['bodies'][av.get('body', 0)]; layers = []
    for cat in ('body', 'face', 'hair', 'top', 'legs', 'feet', 'hat', 'cape', 'neck'):
        p = M['parts'][cat][av.get(cat, 0) % len(M['parts'][cat])]
        for row, z, maps in p['L'].get(body, []): layers.append((z, p['f'], row, maps))
    layers.sort(key=lambda t: t[0]); out = np.zeros((FH, FW * NF, 4), np.uint8)
    for z, f, row, maps in layers:
        a = img(f)[row * FH:(row + 1) * FH].copy(); m = a[..., 3] > 0
        for slot, src in maps:
            pal = M['pal'][MAT[slot]]; tgt = pal[av.get(slot + 'C', src)] if isinstance(av.get(slot + 'C'), str) else pal[src]
            for s, t in zip(pal[src], tgt):
                sc = hx(s); hit = m & (np.abs(a[..., :3].astype(int) - sc).max(-1) <= 1); a[hit, :3] = hx(t)
        out[m] = a[m]
    return out
if __name__ == '__main__':
    import random; random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    k = 3; rows = []
    for i in range(8):
        av = dict(body=i % 2, hair=random.randrange(89), face=random.randrange(len(M['parts']['face'])), top=random.randrange(40), legs=random.randrange(14), feet=random.randrange(10),
                  hat=random.choice([0, 0, 1, 2, 3, 4]), cape=random.choice([0, 0, 1]), neck=random.choice([0, 0, 1, 5]),
                  skinC=random.choice(list(M['pal']['skin'])[:7]), hairC=random.choice(list(M['pal']['hair'])), eyeC=random.choice(list(M['pal']['eye'])),
                  topC=random.choice(['purple', 'red', 'navy', 'forest', 'black']), legsC='charcoal', feetC='brown', hatC='black', neckC='red')
        im = compose(av); fr = [im[:, d * FW:(d + 1) * FW] for d in (0, 10, 5, 15)]
        rows.append(np.concatenate(fr, 1))
    can = np.concatenate([np.concatenate(rows[:4], 0), np.concatenate(rows[4:], 0)], 1)
    bg = Image.new('RGBA', (can.shape[1], can.shape[0]), (70, 58, 92, 255)); bg.alpha_composite(Image.fromarray(can))
    bg.resize((bg.width * k, bg.height * k), Image.NEAREST).save(sys.argv[2] if len(sys.argv) > 2 else 'prev.png')
