# 「길 잃은 아기 동물」 12마리 (16x16 도트, 왼쪽을 봐요) → out/babies.png (192x16, 칸 i = x 16*i)
#   python3 baby_animals.py [--preview DIR]   # DIR/babies_prev.png (8배 확대 + 이름)
import os, sys
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = 16
def H(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
BASE = {'o': H('#1a1024'), 'h': H('#ffffff'), 'e': H('#1a1024'), 'p': H('#ff9ac8'), 'w': H('#f6f0ff')}
NAMES = ['아기 오리', '아기 고양이', '아기 강아지', '아기 토끼', '아기 다람쥐', '아기 고슴도치', '아기 박쥐', '아기 부엉이', '아기 여우', '아기 너구리', '아기 개구리', '아기 병아리']
A = []   # (그림 줄, 색)

A.append(([   # 1 아기 오리: 노란 솜털 · 넓적한 주황 부리 · 꽁지
"................",
"................",
".....oooo.......",
"....oyyyyo......",
"...oyyyyyyo.....",
"...oyhyyyyo.....",
"..ooyeyyyyo.....",
".obbbyypyyo.....",
".obbbyyyyyoooo..",
"..oooyyyyyyyyyo.",
"...oyyyyyysyyso.",
"...oyyyyyssyyo..",
"....oyysssyyo...",
".....oooooooo...",
"......ob.ob.....",
"......oo.oo.....",
], {'y': H('#ffe04a'), 's': H('#e8b02a'), 'b': H('#ff8a2a')}))

A.append(([   # 2 아기 고양이: 까만 털 · 하얀 양말 · 꼬리를 세움
"................",
"............oo..",
"..o....o...oko..",
".opo..opo..oko..",
".okkooookko.ok..",
".okkkkkkkko.ok..",
".okgkkkkgko.ok..",
".okekkkkeko.ok..",
".okkkppkkko.ok..",
"..okkkkkkooook..",
"...okkkkkkkkko..",
"...okkkkkkkkko..",
"...okkkkkkkkko..",
"...owwooooowwo..",
"...oo......oo...",
"................",
], {'k': H('#3e3454'), 'g': H('#ffd866')}))

A.append(([   # 3 아기 강아지: 갈색 · 축 처진 귀 · 하얀 주둥이 · 꼬리 살랑
"................",
"................",
"...oooooooo.....",
"..oddddddddo....",
".oedddddddddo...",
".oedhdddhddeo...",
".oededddedeeo...",
"..oddwwwwddo..o.",
"..odwwkwwwdo.odo",
"...oowwwwooooddo",
"....oddddddddo..",
"....oddddddddo..",
"....oddssddsdo..",
"....owoo.oowoo..",
"....oo.....oo...",
"................",
], {'d': H('#c8935a'), 's': H('#9a6a3a'), 'e': H('#6e4824'), 'k': H('#1a1024')}))

A.append(([   # 4 아기 토끼: 하얀 털 · 한쪽 귀만 접힘 · 동그란 꼬리
"................",
"...oo...........",
"..owpo..oooo....",
"..owpo.owppwo...",
"..owpo.oooowo...",
"..owwoooo..oo...",
".owwwwwwwo......",
".owhwwwwwwo.....",
".owewwwwwwo.....",
".opwwwwwwwoooo..",
"..owwwwwwwwwwwo.",
"...owwwwwwwwcwwo",
"...owwwwwwwwwwo.",
"....owcwwwwcwo..",
".....ooooooooo..",
"................",
], {'c': H('#c8c0e0')}))

A.append(([   # 5 아기 다람쥐: 큰 줄무늬 꼬리 · 볼에 도토리
"...........ooo..",
"..o..o....orrro.",
".oro.oro.orllrro",
".orrrrrro.orllro",
".orhrrrrro.orlro",
".orerrrrro.orlro",
".oappgrrro.orlro",
".oaaorrrroorlro.",
"..oooorrrrrrlro.",
"....orllrrrrro..",
"....orllrrrrro..",
"....orrrrrrro...",
"....oorooroo....",
".....oo.oo......",
"................",
"................",
], {'r': H('#d8803a'), 'l': H('#f6d098'), 'a': H('#9a6a3a'), 'g': H('#6e4824')}))

A.append(([   # 6 아기 고슴도치: 동글동글 가시 · 등에 낙엽 하나
"................",
"................",
"........oo......",
".....ooofo......",
"....osssooo.....",
"...ossssssso....",
"..osssssssssoo..",
".offfssssssssso.",
"offhfssssssssso.",
"offefssssssssso.",
"ofkffssssssssso.",
".offffsssssssso.",
"..offfooooooooo.",
"...ooo.oo..oo...",
"................",
"................",
], {'s': H('#6e5040'), 'f': H('#f0d8b0'), 'k': H('#1a1024'), 'l': H('#ff8a2a')}))
A[-1][0][2] = "........oo......"
A[-1][0][3] = ".....ooolo......"

A.append(([   # 7 아기 박쥐: 작은 날개 · 분홍 귀 · 송곳니
"................",
"................",
"......o..o......",
".....opoopo.....",
"..o..obbbbo..o..",
".owo.obhbho.owo.",
".owwoobebeoowwo.",
".owwwobbbbowwwo.",
".owwwoobfboowwo.",
"..owo.obbbo.owo.",
"...o..obbbo..o..",
"......oo.oo.....",
"................",
"................",
"................",
"................",
], {'b': H('#7a5ea8'), 'w': H('#4a3870'), 'f': H('#ffffff')}))

A.append(([   # 8 아기 부엉이: 커다란 눈 · 솜뭉치 몸 · 작은 부리
"................",
"...o.......o....",
"...ooooooooo....",
"...occcccccco...",
"..ocwwccwwcco...",
"..owhkwwhkwco...",
"..owkkwwkkwco...",
"..ocwwbbwwcco...",
"..occccbcccco...",
"..occllllccco...",
"..oclllllllco...",
"..occllllllco...",
"...occccccco....",
"....oyoooyo.....",
"....oo...oo.....",
"................",
], {'c': H('#b8a088'), 'l': H('#efe2c8'), 'k': H('#1a1024'), 'b': H('#ffb04a'), 'y': H('#ffb04a')}))

A.append(([   # 9 아기 여우: 주황 털 · 꼬리 끝만 하얌
"................",
"..o....o........",
".ofo..ofo.......",
".offooooffo.....",
".offffffffo.....",
".ofhfffffffo....",
".ofeffffffffo...",
"owwfffffffffo...",
"okwwwffffffo..oo",
".oowwwoffffooowo",
"....offfffffffwo",
"....owwffffffffo",
"....owwfffffffo.",
"....oeooooooeo..",
"....oo......oo..",
"................",
], {'f': H('#ff9a3c'), 'k': H('#1a1024'), 'e': H('#4a2e24')}))

A.append(([   # 10 아기 너구리: 눈가 까만 줄 · 줄무늬 꼬리
"................",
"..o....o........",
".ogo..ogo.......",
".oggooooggo.....",
".oggggggggo.....",
".ommmmmmmmo.....",
".omhmmmmhmo.....",
".omemmmmemo.....",
"..owwwkwwwo..ooo",
"...owwwwwo..ogmo",
"...oggggggooogmo",
"...oggggggggggo.",
"...oggggggggggo.",
"...ommooooommo..",
"...oo......oo...",
"................",
], {'g': H('#9a94aa'), 'm': H('#3a3448'), 'k': H('#1a1024')}))
A[-1][0][5] = ".ogmmmmmmgo....."
A[-1][0][6] = ".omhmggmhmo....."
A[-1][0][7] = ".omemggmemo....."

A.append(([   # 11 아기 개구리: 연두색 · 빨간 볼 · 툭 튀어나온 눈
"................",
"................",
"................",
"...ooo....ooo...",
"..ohwgo..ohwgo..",
"..oeggoooeggo...",
"..ogggggggggo...",
".oggggggggggo...",
".orggggggggrgo..",
".oggoooooooggo..",
"..ogllllllllgo..",
"..oglllllllggo..",
".oggogggggoggo..",
".oo.oo...oo.oo..",
"................",
"................",
], {'g': H('#7cd06a'), 'l': H('#c8f0a0'), 'r': H('#ff7a8a')}))

A.append(([   # 12 아기 병아리: 노란 공 · 머리에 깃털 하나 · 짧은 부리
"................",
"................",
".......oo.......",
"......oyo.......",
".....ooyoo......",
"....oyyyyyo.....",
"...oyyyyyyyo....",
"..oyhyyyyyhyo...",
"..oyeyybyyeyo...",
"..opyyybyyypo...",
"..oyyyyyyyyyo...",
"..osyyyyyyyso...",
"...osyyyyyso....",
"....ooooooo.....",
".....ob.bo......",
".....oo.oo......",
], {'y': H('#fff07a'), 's': H('#e8c43a'), 'b': H('#ff8a2a')}))


def render(rows, pal):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load()
    P = {**BASE, **pal}
    for y, r in enumerate(rows):
        r = r.ljust(S, '.')[:S]
        for x, ch in enumerate(r):
            if ch != '.': px[x, y] = P[ch]
    return im


def build():
    sheet = Image.new('RGBA', (S * len(A), S), (0, 0, 0, 0))
    for i, (rows, pal) in enumerate(A): sheet.paste(render(rows, pal), (i * S, 0))
    return sheet


def preview(sheet, outdir):
    os.makedirs(outdir, exist_ok=True); Z, per, pad, lh = 8, 6, 10, 26
    cell = S * Z; rows = (len(A) + per - 1) // per
    img = Image.new('RGBA', (per * (cell + pad) + pad, rows * (cell + lh + pad) + pad), (0x21, 0x17, 0x33, 255)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 16)
    for i in range(len(A)):
        x0, y0 = pad + (i % per) * (cell + pad), pad + (i // per) * (cell + lh + pad)
        img.alpha_composite(sheet.crop((i * S, 0, i * S + S, S)).resize((cell, cell), Image.NEAREST), (x0, y0))
        d.text((x0 + 4, y0 + cell + 2), NAMES[i], fill=(230, 220, 250, 255), font=font)
    img.save(os.path.join(outdir, 'babies_prev.png'))


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    sh = build(); sh.save('out/babies.png'); print('saved', sh.size)
    if '--preview' in sys.argv: preview(sh, sys.argv[sys.argv.index('--preview') + 1])
