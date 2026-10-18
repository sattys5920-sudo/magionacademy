import json, random, sys
from PIL import Image
M = json.load(open('out/avatar_parts.json')); S = Image.open('out/avatar_parts.png').convert('RGBA')
FW, FH = M['fw'], M['fh']; KEYS = {240: 0, 200: 1, 150: 2, 100: 3}
hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
def compose(av, fr):
    pal = M['pal']; R = dict(skin=pal['skin'][av['skinC']], eye=pal['eye'][av['eyeC']], hair=pal['hair'][av['hairC']], shoes=pal['shoes'][av['shoeC']], cloth=pal['cloth'][0], house=pal['house'][av['house']])
    L = list(M['base'])
    for c in ('hair', 'eyes', 'mouth', 'uni'): L += M['parts'][c][av[c]]['L']
    L.sort(key=lambda l: M['z'].index(l[2]))
    out = Image.new('RGBA', (FW, FH))
    for row, slot, z in L:
        im = S.crop((fr * FW, row * FH, fr * FW + FW, row * FH + FH)); px = im.load()
        for y in range(FH):
            for x in range(FW):
                r, g, b, a = px[x, y]
                if a and slot and r == g == b and r in KEYS: px[x, y] = hx(R[slot][KEYS[r]])
        out.alpha_composite(im)
    return out
if __name__ == '__main__':
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    sheet = Image.new('RGBA', ((FW + 2) * 6, (FH + 2) * N), (70, 54, 96, 255))
    for n in range(N):
        av = dict(hair=random.randrange(len(M['parts']['hair'])), eyes=random.randrange(15), mouth=random.randrange(10), uni=n % 5, skinC=random.randrange(5), eyeC=random.randrange(20), hairC=random.randrange(20), shoeC=random.randrange(10), house=random.choice(list(M['pal']['house'])))
        if n == 0: av.update(skinC=0, hair=0, eyes=0, mouth=0)
        for f in range(6): sheet.alpha_composite(compose(av, f), (f * (FW + 2) + 1, n * (FH + 2) + 1))
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save('out/prev.png'); print(sheet.size)
