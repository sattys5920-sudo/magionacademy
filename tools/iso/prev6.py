# chars5 미리보기: 게임과 같은 방식(밝기→팔레트, 바깥 테두리)으로 합쳐 봐요
import json, random, sys
from PIL import Image
M = json.load(open('out/avatar_parts.json')); S = Image.open('out/avatar_parts.png').convert('RGBA')
FW, FH = M['fw'], M['fh']
hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def lut(slot, ramp):
    st = M['stops'][slot]; cs = [hx(h) for h in ramp]; T = []
    for v in range(256):
        if v >= st[0]: k = (v - st[0]) / max(1, 255 - st[0]) * .6; c = [a + (255 - a) * k for a in cs[0]]
        elif v <= st[3]: k = v / max(1, st[3]); c = [a * (.55 + .45 * k) for a in cs[3]]
        else:
            i = next(i for i in range(3) if st[i + 1] <= v <= st[i]); k = (st[i] - v) / max(1, st[i] - st[i + 1]); c = [a + (b - a) * k for a, b in zip(cs[i], cs[i + 1])]
        T.append(tuple(int(round(x)) for x in c) + (255,))
    return T
def compose(av, fr):
    P = M['pal']; R = dict(skin=lut('skin', P['skin'][av['skinC']]), eye=lut('eye', P['eye'][av['eyeC']]), hair=lut('hair', P['hair'][av['hairC']]), shoes=lut('shoes', P['shoes'][av['shoeC']]), cloth=lut('cloth', P['cloth'][0]), house=lut('house', P['house'][av['house']]))
    L = list(M['base'])
    for c in ('hair', 'eyes', 'mouth', 'uni'): L += M['parts'][c][av[c]]['L']
    L.sort(key=lambda l: M['z'].index(l[2]))
    out = Image.new('RGBA', (FW, FH))
    for row, slot, z in L:
        im = S.crop((fr * FW, row * FH, fr * FW + FW, row * FH + FH)); px = im.load()
        if slot:
            for y in range(FH):
                for x in range(FW):
                    r, g, b, a = px[x, y]
                    if a and r == g == b: px[x, y] = R[slot][r]
        out.alpha_composite(im)
    if M.get('outline'):
        px = out.load(); add = []
        for y in range(FH):
            for x in range(FW):
                if px[x, y][3] == 0 and any(0 <= x + dx < FW and 0 <= y + dy < FH and px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
        for x, y in add: px[x, y] = (42, 24, 48, 255)
    return out
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'rand'
    if mode == 'hair':
        n = len(M['parts']['hair']); sh = Image.new('RGBA', ((FW + 1) * 30, (FH // 2 + 22) * 4), (70, 54, 96, 255))
        for i in range(n):
            for k, f in enumerate((0, 6, 3)):
                av = dict(hair=i, eyes=0, mouth=0, uni=0, skinC=1, eyeC=1, hairC=(i * 3) % 20, shoeC=0, house='moon')
                sh.alpha_composite(compose(av, f).crop((0, 0, FW, FH // 2 + 20)), (((i % 10) * 3 + k) * (FW + 1), (i // 10) * (FH // 2 + 22)))
        sh.resize((sh.width * 2, sh.height * 2), Image.NEAREST).save('out/prev_hair.png')
    elif mode == 'face':
        sh = Image.new('RGBA', ((FW + 1) * 15, 46 * 2), (70, 54, 96, 255))
        for i in range(15): sh.alpha_composite(compose(dict(hair=4, eyes=i, mouth=0, uni=0, skinC=1, eyeC=i, hairC=2, shoeC=0, house='moon'), 0).crop((0, 0, FW, 44)), (i * (FW + 1), 0))
        for i in range(10): sh.alpha_composite(compose(dict(hair=4, eyes=0, mouth=i, uni=0, skinC=i % 5, eyeC=1, hairC=2, shoeC=0, house='moon'), 0).crop((0, 0, FW, 44)), (i * (FW + 1), 46))
        sh.resize((sh.width * 3, sh.height * 3), Image.NEAREST).save('out/prev_face.png')
    else:
        random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1); N = 5
        sh = Image.new('RGBA', ((FW + 2) * 9, (FH + 2) * N), (70, 54, 96, 255))
        for n in range(N):
            av = dict(hair=random.randrange(40), eyes=random.randrange(15), mouth=random.randrange(10), uni=n, skinC=random.randrange(5), eyeC=random.randrange(20), hairC=random.randrange(20), shoeC=random.randrange(10), house=['dew', 'ember', 'dusk', 'moon', 'moon'][n])
            if n == 0: av.update(hair=0, eyes=0, mouth=0, skinC=1)
            for f in range(9): sh.alpha_composite(compose(av, f), (f * (FW + 2) + 1, n * (FH + 2) + 1))
        sh.resize((sh.width * 3, sh.height * 3), Image.NEAREST).save('out/prev_rand.png')
