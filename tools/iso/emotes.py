# 말풍선 픽셀 이모티콘 12종 (16×16, 직접 그림). python3 tools/iso/emotes.py → public/art/emo.png
from PIL import Image, ImageDraw, ImageFont
import os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # tools/
PAL = {
 'K': (42, 26, 64), 'F': (255, 216, 102), 'S': (232, 168, 60), 'L': (255, 241, 186), 'W': (255, 255, 255),
 'R': (255, 143, 168), 'M': (176, 48, 80), 'T': (255, 104, 128), 'B': (127, 208, 255), 'b': (64, 150, 230),
 'H': (255, 79, 110), 'h': (200, 40, 80), 'O': (255, 150, 40), 'o': (210, 100, 20), 'G': (110, 190, 90), 'g': (60, 130, 60),
 'Y': (255, 236, 140), 'P': (236, 228, 255), 'p': (180, 166, 220), 'A': (255, 90, 70), 'a': (200, 50, 50),
 'C': (250, 210, 170), 'c': (220, 160, 120),
}
CIRCLE = [
 '.....KKKKKK.....',
 '...KKFFFFFFKK...',
 '..KFFFFFFFFFFK..',
 '.KFFFFFFFFFFFFK.',
 '.KFFFFFFFFFFFFK.',
 'KFFFFFFFFFFFFFFK',
 'KFFFFFFFFFFFFFFK',
 'KFFFFFFFFFFFFFFK',
 'KFFFFFFFFFFFFFFK',
 'KFFFFFFFFFFFFFSK',
 'KFFFFFFFFFFFFFSK',
 '.KFFFFFFFFFFFSK.',
 '.KFFFFFFFFFFSSK.',
 '..KSFFFFFFSSSK..',
 '...KKSSSSSSKK...',
 '.....KKKKKK.....',
]
def face(col='F', sh='S'):
    g = [[{'F': col, 'S': sh}.get(c, c) for c in r] for r in CIRCLE]
    g[2][4] = g[2][5] = g[3][3] = g[3][4] = 'L'
    return g
def over(g, rows):
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.': g[y][x] = c
    return g
def grid(rows): return [list(r.ljust(16, '.')) for r in rows]
E = {}
E['웃음'] = over(face(), [
 '', '', '', '', '',
 '................',
 '.....K....K.....',
 '....K.K..K.K....',
 '................',
 '...RR......RR...',
 '.....K....K.....',
 '......KKKK......',
])
E['깔깔'] = over(face(), [
 '', '', '', '', '',
 '....K......K....',
 '.....K....K.....',
 '....K......K....',
 '..B..........B..',
 '..B.KKKKKKKK.B..',
 '.BB.KWWWWWWK.BB.',
 '.B..KMMMMMMK..B.',
 '.....KTTTTK.....',
 '......KKKK......',
])
E['하트눈'] = over(face(), [
 '', '', '', '',
 '................',
 '...HH.HH.HH.HH..',
 '...HHHHH.HHHHH..',
 '....HHH...HHH...',
 '.....H.....H....',
 '................',
 '.....K....K.....',
 '......KKKK......',
])
E['놀람'] = over(face(), [
 '', '', '', '',
 '....K......K....',
 '...KWK....KWK...',
 '...KKK....KKK...',
 '................',
 '................',
 '.......KK.......',
 '......KMMK......',
 '......KMMK......',
 '.......KK.......',
])
E['눈물'] = over(face(), [
 '', '', '', '',
 '...KK......KK...',
 '................',
 '....KK....KK....',
 '....B......B....',
 '....B......B....',
 '...BB..KK..BB...',
 '...BB.K..K.BB...',
 '...B........B...',
])
E['화남'] = over(face('A', 'a'), [
 '', '', '',
 '................',
 '...K........K...',
 '....KK....KK....',
 '.....K....K.....',
 '....KK....KK....',
 '................',
 '................',
 '......KKKK......',
 '.....K....K.....',
])
E['화남'][2][4] = E['화남'][2][5] = E['화남'][3][3] = E['화남'][3][4] = 'T'
E['손인사'] = grid([
 '................',
 '....KK.KK.......',
 '...KCCKCCK.KK...',
 '...KCCKCCKKCCK..',
 '...KCCKCCKCCK.b.',
 '.KKKCCKCCKCCK.b.',
 'KCCKCCKCCKCCK...',
 'KCCKCCCCCCCCKb..',
 '.KCCKCCCCCCCK.b.',
 '..KCCCCCCCCcK...',
 '..KCCCCCCCccK...',
 '...KCCCCCCccK...',
 '...KCCCCCcccK...',
 '....KcccccccK...',
 '.....KKKKKKK....',
 '',
])
E['하트'] = grid([
 '',
 '..KKKK..KKKK....',
 '.KHHHHKKHHHHK...',
 'KHWWHHHHHHHHHK..',
 'KHWHHHHHHHHHHK..',
 'KHHHHHHHHHHHHK..',
 'KHHHHHHHHHHHhK..',
 '.KHHHHHHHHHhK...',
 '..KHHHHHHHhK....',
 '...KHHHHHhK.....',
 '....KHHHhK......',
 '.....KHhK.......',
 '......KK........',
 '',
])
for r in E['하트']: r.insert(0, '.'); r.pop()
E['엄지척'] = grid([
 '',
 '......KK........',
 '.....KCCK.......',
 '.....KCCK.......',
 '.....KCCK.......',
 '....KCCCK.......',
 '.KKKCCCCKKKKK...',
 '.KbKCCCCCCCCCK..',
 '.KbKCCCKKKKKK...',
 '.KbKCCCCCCCCCK..',
 '.KbKCCCKKKKKK...',
 '.KbKCCCCCCCCK...',
 '.KbKCCCKKKKK....',
 '.KbKCCCCcccK....',
 '.KKKKKKKKKK.....',
 '',
])
E['반짝'] = grid([
 '.....K..........',
 '....KYK.........',
 '....KYK.........',
 '..KKYWYKK.......',
 '.KYYWWWYYK......',
 '..KKYWYKK...K...',
 '....KYK....KYK..',
 '....KYK..KKYWYKK',
 '.....K...KYWWWYK',
 '..........KKYWYK',
 '...K.......KYK..',
 '..KYK.......K...',
 '.KYWYK..........',
 '..KYK...........',
 '...K............',
 '',
])
E['호박'] = grid([
 '.......KK.......',
 '......KgK.......',
 '...KKKKgKKKKK...',
 '..KOOOoKoOOOOK..',
 '.KOOOOoOoOOOOOK.',
 '.KOKKOoOoOKKOOK.',
 'KOOKYKoOoKYKOOoK',
 'KOOOOOoOoOOOOOoK',
 'KOOOOOoKoOOOOOoK',
 'KOOKOOoOoOOOKOoK',
 'KOOKYKKKKKKYKOoK',
 '.KOOKYKYYKYKOooK',
 '.KOOOKKKKKKOooK.',
 '..KoOOOoKoOooK..',
 '...KKKKKKKKKK...',
 '',
])
E['유령'] = grid([
 '.....KKKKK......',
 '....KPPPPPK.....',
 '...KPWPPPPPK....',
 '..KPWPPPPPPPK...',
 '..KPPKKPPKKPK...',
 '..KPPKKPPKKPK...',
 '..KPPPPPPPPPK...',
 '..KPRPPKKPRPK...',
 '..KPPPPKKPPPKK..',
 '.KKPPPPPPPPPPPK.',
 'KPKPPPPPPPPPKK..',
 '.KKPPPPPPPPpK...',
 '..KPPPPPPPppK...',
 '..KPpPPpPppK....',
 '..KKpKKpKKK.....',
 '...K.K..........',
])
ORDER = ['손인사', '웃음', '깔깔', '하트눈', '놀람', '눈물', '화남', '하트', '엄지척', '반짝', '호박', '유령']
def img(g, k=1):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            c = g[y][x] if y < len(g) and x < len(g[y]) else '.'
            if c != '.': im.putpixel((x, y), PAL[c] + (255,))
    return im.resize((16 * k, 16 * k), Image.NEAREST)
if __name__ == '__main__':
    # 게임용 한 줄 시트: 16×16 × 12칸 → public/art/emo.png (순서 = ORDER, 게임의 EMOS와 같아요)
    out = Image.new('RGBA', (16 * len(ORDER), 16), (0, 0, 0, 0))
    for i, n in enumerate(ORDER): out.alpha_composite(img(E[n]), (i * 16, 0))
    out.save(os.path.join(os.path.dirname(D), 'public', 'art', 'emo.png') if len(sys.argv) < 2 else sys.argv[1])
    print(' '.join(ORDER))
