# 낚시·채집 그림 (16×16 픽셀, 직접 그림): 물고기 40 + 쓰레기 3, 채집물 50, 낚싯대 5
# python3 tools/iso/fishing_art.py [시안.png] → public/art/fish.png, forage.png, rods.png (게임의 FISH·FORAGE·RODS 순서와 같아요)
import os, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K = (34, 22, 50)
def hx(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def pad(rows): return [r.ljust(16, '.')[:16] for r in (rows + [''] * 16)[:16]]

# ---------------- 물고기 틀 (머리가 왼쪽) ----------------
# a 몸, b 몸 그림자, c 몸 밝은 곳, d 지느러미, e 지느러미 어둠, w 흰색, x 눈, K 외곽선 그대로
FT = {
 'slim': ['', '', '', '......dd........', '....cccccc....d.', '..ccaaaaaacc.dd.', '.caxaaaaaaaaadd.', '.aaaaaaaaaaaadd.', '..bbaaaaaabb.dd.', '....bbbbbb....d.', '......e.........'],
 'round': ['', '', '......dd........', '.....dddd.......', '...cccccccc.....', '..ccaaaaaaac..dd', '.cawxaaaaaaa.ddd', '.aaaaaaaaaaaaddd', '.aaaaaaaaaaa.ddd', '..bbaaaaaaab..dd', '...bbbbbbbb.....', '.....ee.ee......'],
 'long': ['', '', '', '', '', '..cccc..........', '.cxaaacccccc....', '.aaaaaaaaaaaccdd', '..bbbbaaaaaaaadd', '......bbbbbbbbd.'],
 'flat': ['.......cc.......', '......caac......', '.....caaaac.....', '...ccaaaaaacc...', '.ccaaaxaaxaaacc.', 'caaaaaaaaaaaaaac', '.bbaaaaaaaaaabb.', '...bbaaaaaabb...', '.....baaaab.....', '......bddb......', '.......dd.......', '.......d........', '........d.......'],
 'cat': ['', '', '', '....cccccc......', '..ccaaaaaaccc...', '.cxaaaaaaaaaacdd', 'aaaaaaaaaaaaaaad', 'K.bbaaaaaaaaaadd', 'K...bbbbbbbbbbd.', 'K...............'],
 'puff': ['', '.....d..d.......', '...d.cccccc.d...', '....caaaaaac....', '..dcaaaaaaaacd..', '...awxaaaaaaa.dd', '..daaaaaaaaaaddd', '...aaaaaaaaaa.dd', '..dbccccccccbd..', '....bccccccb....', '...d.bbbbbb.d...', '.....d..d.......'],
 'jelly': ['', '.....cccccc.....', '....caaaaaac....', '...caaaaaaaac...', '...aaxaaaaxaa...', '...aaaaaaaaaa...', '...bbbbbbbbbb...', '....d.d..d.d....', '....d.d..d.d....', '...d..d..d..d...', '...d.d....d.d...', '....d......d....'],
 'shrimp': ['', '', '...e............', '..e.e...........', '....ccccc.......', '..ccaaaaacc.....', '.cxaaaaaaaac....', '.aaaaaaaaaaab...', '..bbaaaaaabb.d..', '....e.e.e.bbbdd.', '..........bdd...'],
 'cray': ['', '..dd........dd..', '.dccd......dccd.', '.dccd......dccd.', '..dd.cccccc.dd..', '....daaaaaad....', '....axaaaaxa....', '.....aaaaaa.....', '....baaaaaab....', '...e.baaaab.e...', '..e...baab...e..', '.......bb.......', '......dddd......', '.....d....d.....'],
 'shell': ['', '........cc......', '.......caac.....', '......caaaac....', '.....cadddac....', '....caddaadac...', '...cadaaaadaac..', '..caddaaaadaac..', '..cadaaddaadac..', '..caadddddaab...', '...baaaaaaabb...', '....bbbbbbbb....'],
 'horse': ['', '......ccc.......', '.....caaac......', '....cxaaaaa.....', '..aaaaaaaac.....', '......caaad.....', '.....caaaadd....', '.....aaaaadd....', '......aaaad.....', '.......aaab.....', '......baab......', '.....bab........', '.....bb.........'],
 'star': ['.......cc.......', '......caac......', '......caac......', '..ccccaaaacccc..', '.caaaaaaaaaaaac.', '..baaaxaaxaaab..', '....baaaaaab....', '....caaaaaac....', '...caab..baac...', '...cab....bac...', '...bb......bb...'],
 'turtle': ['', '', '.....dddddd.....', '...ddeddeddd....', '..ddeddeddedd...', 'cc.ddddddddddd..', 'cxaaaaaaaaaaaaa.', 'aaaa.bbbbbbbb.a.', '..aa.......aa...'],
 'whale': ['', '', '...........d.d..', '....cccccc..dd..', '..ccaaaaaacc.d..', '.caaaaaaaaaac.dd', 'caxaaaaaaaaaaadd', 'caaaaaaaaaaaaad.', '.bccccccccccab..', '..bccccccccbb...', '....bbbbbbb.....'],
 'angler': ['..d.............', '.dwd............', '..d.e...........', '....e...........', '...cccccc.......', '..caaaaaacc..dd.', '.cawxaaaaaacddd.', '.aaaaaaaaaaaaddd', '.awwwwaaaaaa.ddd', '..bbbaaaaaab..d.', '....bbbbbbb.....'],
 'boot': ['', '', '....dddddd......', '....daaaad......', '....daaaad......', '....daaaad......', '....daaaad......', '....daaaaad.....', '...daaaaaaadd...', '..daaaaaaaaaad..', '..dbbbbbbbbbbd..', '...eeeeeeeeee...'],
 'can': ['', '', '', '.....cccccc.....', '....caaaaaac....', '....awwwwwwa....', '....adddddda....', '....adwwwwda....', '....adddddda....', '....awwwwwwa....', '....baaaaaab....', '.....bbbbbb.....'],
 'weed': ['', '......a...a.....', '.....a...a......', '.....a..a...a...', '......a.a..a....', '...a..aaa.a.....', '....a.aaaa......', '.....aaaab......', '......aab.......', '.....bbbbb......', '....b.b.b.b.....'],
}
# 무늬 덧칠
def ov(g, kind, P):
    body = [(x, y) for y in range(16) for x in range(16) if g[y][x] in 'abc']
    if not body: return
    xs = [x for x, _ in body]; ys = [y for _, y in body]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for (x, y) in body:
        if kind == 'stripe' and (x - x0) % 3 == 2: g[y][x] = 'e'
        elif kind == 'band' and (x - x0) % 4 in (2, 3) and x > x0 + 2: g[y][x] = 'd'
        elif kind == 'spot' and (x * 7 + y * 5) % 9 == 0: g[y][x] = 'd'
        elif kind == 'dots' and (x + y) % 3 == 0 and (x * y) % 2 == 0: g[y][x] = 'w'
        elif kind == 'bone' and g[y][x] == 'a' and (x - x0) % 2 == 1 and x > x0 + 3: g[y][x] = 'e'
        elif kind == 'belly' and y >= (y0 + y1) // 2 + 1 and g[y][x] != 'b': g[y][x] = 'w'
        elif kind == 'rainbow': g[y][x] = 'RYGBV'[(x - x0) * 5 // max(1, x1 - x0 + 1)] if g[y][x] != 'b' else g[y][x]
        elif kind == 'speckle' and (x * 13 + y * 7) % 11 == 0: g[y][x] = 'w'
        elif kind == 'scale' and (x + (y % 2)) % 2 == 0 and g[y][x] == 'a': g[y][x] = 'c'
    if kind == 'crown':
        cx = x0 + 3; g[max(0, y0 - 2)][cx - 1] = g[max(0, y0 - 2)][cx + 1] = g[max(0, y0 - 2)][cx + 3] = 'Y'
        for dx in range(-1, 4): g[max(0, y0 - 1)][cx + dx] = 'Y'
    if kind == 'flower':
        cx, cy = x0 + 4, max(1, y0 - 1)
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)): g[cy + dy][cx + dx] = 'P'
        g[cy][cx] = 'Y'
    if kind == 'hat':   # 작은 마녀 모자
        cx, cy = x0 + 4, y0
        for dx in range(-2, 3): g[cy - 1][cx + dx] = 'H'
        g[cy - 2][cx] = g[cy - 2][cx - 1] = g[cy - 3][cx] = 'H'; g[cy - 4][cx + 1] = 'H'
    if kind == 'leaf':
        cx, cy = x0 + 5, max(1, y0 - 1); g[cy][cx] = g[cy - 1][cx + 1] = 'G'; g[cy][cx + 1] = 'G'
    if kind == 'glow':
        for (x, y) in body:
            if g[y][x] == 'c': g[y][x] = 'w'
EXTRA = {'R': hx('#FF6A7A'), 'Y': hx('#FFE066'), 'G': hx('#6AD86A'), 'B': hx('#6AB8FF'), 'V': hx('#B07AFF'), 'P': hx('#FF9AD0'), 'H': hx('#3A2A5A')}
def pal5(a, b=None, c=None, d=None, e=None):
    A = hx(a); f = lambda k: tuple(max(0, min(255, int(v * k))) for v in A)
    return {'a': A, 'b': hx(b) if b else f(.72), 'c': hx(c) if c else f(1.22), 'd': hx(d) if d else f(.85), 'e': hx(e) if e else f(.6), 'w': (255, 255, 255), 'x': K}
def draw(rows, P, ovs=(), alpha=255):
    g = [list(r) for r in pad(rows)]
    for o in ovs: ov(g, o, P)
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y in range(16):
        for x in range(16):
            c = g[y][x]
            if c == '.': continue
            col = K if c == 'K' else P.get(c) or EXTRA[c]
            px[x, y] = col + (alpha if c in 'abc' else 255,)
    # 외곽선: 칠한 칸 둘레 (K 칸 둘레는 빼요)
    out = im.copy(); op = out.load()
    for y in range(16):
        for x in range(16):
            if px[x, y][3]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 16 and 0 <= ny < 16 and px[nx, ny][3] and g[ny][nx] != 'K': op[x, y] = K + (255,); break
    return out

# 물고기 40종 (흔한 것 → 전설 순서) + 쓰레기 3: (id, 이름, 틀, 색, 무늬)
FISH = [
 ('f_minnow', '유령 피라미', 'slim', pal5('#C8D8F0', d='#9AB0D8'), ('glow',)),
 ('f_crucian', '호박 붕어', 'round', pal5('#F08A2A', d='#5A9A3A'), ('stripe',)),
 ('f_killi', '이끼 송사리', 'slim', pal5('#7AB86A', d='#4A8A4A'), ('speckle',)),
 ('f_loach', '진흙 미꾸라지', 'long', pal5('#8A6A4A', d='#6A4A30'), ('spot',)),
 ('f_smelt', '촛불 빙어', 'slim', pal5('#F0E8D0', d='#FFB040'), ('belly',)),
 ('f_carp', '버섯 잉어', 'round', pal5('#C85AA8', d='#F0E0F0'), ('dots',)),
 ('f_batcat', '박쥐 메기', 'cat', pal5('#4A3A5A', d='#2A2040'), ()),
 ('f_candy', '사탕 열대어', 'round', pal5('#FF8AB8', d='#8AE0FF'), ('band',)),
 ('f_jelly', '젤리 해파리', 'jelly', pal5('#B89AFF', d='#E0C8FF'), ('glow',)),
 ('f_cray', '거미 가재', 'cray', pal5('#C84A3A', d='#E06A4A'), ()),
 ('f_conch', '마녀 모자 소라', 'shell', pal5('#E8C8A8', d='#7A4AA8'), ()),
 ('f_trout', '달빛 송어', 'slim', pal5('#8AA8E0', d='#5A78C0'), ('speckle',)),
 ('f_puffer', '눈알 복어', 'puff', pal5('#F0D070', d='#E0A040'), ()),
 ('f_bonecat', '해골 메기', 'cat', pal5('#E8E4D8', d='#B8B4A8', e='#8A8478'), ('bone',)),
 ('f_betta', '꽃잎 베타', 'round', pal5('#E05A8A', d='#FF9AC8'), ('flower',)),
 ('f_cloudray', '구름 가오리', 'flat', pal5('#E8F0FF', d='#B8C8E8'), ('speckle',)),
 ('f_cotton', '솜사탕 넙치', 'flat', pal5('#FFB8E0', d='#B8E0FF'), ('dots',)),
 ('f_rtrout', '무지개 송어', 'slim', pal5('#A8C0D8', d='#8AA0C0'), ('rainbow',)),
 ('f_weel', '늑대 장어', 'long', pal5('#6A6A7A', d='#4A4A5A'), ('stripe',)),
 ('f_sweet', '안개 은어', 'slim', pal5('#D8E8E8', d='#A8C8C8'), ('scale',)),
 ('f_angler', '호박등 아귀', 'angler', pal5('#5A4A3A', d='#3A2E26'), ('spot',)),
 ('f_piranha', '뱀파이어 피라냐', 'angler', pal5('#A82A3A', d='#6A1A2A'), ()),
 ('f_starfish', '별사탕 불가사리', 'star', pal5('#FFC85A', d='#FF8A5A'), ('dots',)),
 ('f_goby', '부엉이 망둥이', 'round', pal5('#A8784A', d='#7A5430'), ('speckle',)),
 ('f_shrimp', '수정 새우', 'shrimp', pal5('#A8F0F0', d='#6AD0E0'), ('glow',)),
 ('f_bream', '루비 도미', 'round', pal5('#E0303A', d='#FF7080'), ('scale',)),
 ('f_seahorse', '유령 해마', 'horse', pal5('#D0E0FF', d='#A0B8F0'), ('glow',)),
 ('f_bolt', '번개 뱀장어', 'long', pal5('#FFE040', d='#5A5AC8'), ('band',)),
 ('f_gold', '황금 잉어', 'round', pal5('#FFC830', d='#FFE890'), ('scale',)),
 ('f_salmon', '오로라 연어', 'slim', pal5('#7AE0C0', d='#C07AFF'), ('rainbow',)),
 ('f_book', '마법서 넙치', 'flat', pal5('#7A4A9A', d='#FFE066'), ('band',)),
 ('f_witch', '마녀 모자 금붕어', 'round', pal5('#FF7A3A', d='#FFC07A'), ('hat',)),
 ('f_shadow', '그림자 가오리', 'flat', pal5('#2E2840', d='#4A3E6A', c='#5A4A7A'), ('speckle',)),
 ('f_moonbun', '달토끼 금붕어', 'round', pal5('#F8F0FF', d='#FFB8D8'), ('belly',)),
 ('f_turtle', '왕관 거북', 'turtle', pal5('#8AC870', d='#5A8A3A', e='#3A6A2A'), ('crown',)),
 ('f_dragon', '용 비늘 잉어', 'round', pal5('#3AB88A', d='#E0403A'), ('scale',)),
 ('f_whale', '별똥별 꼬마 고래', 'whale', pal5('#4A6AC8', d='#8AA8FF'), ('dots',)),
 ('f_mermaid', '인어의 은빛 잉어', 'slim', pal5('#C8E8F8', d='#7AC8E8'), ('scale', 'glow')),
 ('f_king', '호박달 메기왕', 'cat', pal5('#E07A1E', d='#7A4AA8'), ('stripe', 'crown')),
 ('f_lord', '호수의 주인', 'whale', pal5('#3A2A6A', d='#FFD866', c='#6A5AA8'), ('speckle', 'crown')),
 ('j_boot', '낡은 장화', 'boot', pal5('#6A5A4A', d='#3A2E26'), ()),
 ('j_can', '찌그러진 깡통', 'can', pal5('#A8A8B0', d='#C84A3A'), ()),
 ('j_weed', '물풀 뭉치', 'weed', pal5('#4A8A4A'), ()),
]

# ---------------- 채집물 틀 ----------------
# a 주색, b 그림자, c 밝은 곳, d 포인트, e 포인트 어둠, g 줄기, h 줄기 어둠, w 흰색
GT = {
 'acorn': ['', '', '.......h........', '.....dddddd.....', '....deeeeeed....', '....dddddddd....', '.....caaaaa.....', '.....caaaaab....', '.....aaaaaab....', '......aaaab.....', '.......abb......', '........b.......'],
 'cone': ['', '.......gg.......', '......aaaa......', '.....acacaa.....', '.....aabaab.....', '....acacacaa....', '....aabaabab....', '....acacacab....', '.....aabaab.....', '.....acacab.....', '......abab......', '.......bb.......'],
 'maple': ['', '.......a........', '......aaa.......', '..a...aaa...a...', '..aa.aacaa.aa...', '...aaaacaaaa....', '.aaaaaacaaaaaa..', '..aaaaacaaaaa...', '...aaaacaaaa....', '....aa.c.aa.....', '.......h........', '.......h........'],
 'fan': ['', '', '...aaaaaaaa.....', '..acaacaacaa....', '..aacaacaacb....', '...aacaccab.....', '....aaacab......', '.....aaab.......', '......ab........', '.......h........', '.......h........', '........h.......'],
 'flower': ['', '.....aa.aa......', '....acaaaca.....', '.....aadaa......', '....aadddaa.....', '....acaaaca.....', '.....aa.aa......', '.......g........', '.....g.g........', '......gg..g.....', '.......g.g......', '.......gg.......'],
 'bell': ['', '........g.......', '.......g.g......', '......g...g.....', '.....aa....g....', '....acaa...aa...', '....aaaa..acaa..', '....b.bb..aaaa..', '..........b.bb..', '.......g........', '......ggg.......', '.....hgggh......'],
 'mush': ['', '', '.....aaaaaa.....', '...aacaawaaaa...', '..acawaaaaawaa..', '..aaaaaaaaaaaa..', '..bbbbbbbbbbbb..', '......wwww......', '......wwwc......', '......wwwc......', '.....wwwwcc.....', '................'],
 'berries': ['', '........g.......', '.......gg.......', '.....g..g.g.....', '....aa.aa.......', '...acaaaca.aa...', '...aaabaab.aca..', '....bb.bb..aab..', '......aa....bb..', '.....acab.......', '.....aabb.......', '......bb........'],
 'fruit': ['', '.........h......', '........hgg.....', '.......h.ggg....', '....aaaaaaa.....', '...acaaaaaaa....', '...awaaaaaaab...', '...aaaaaaaaab...', '...aaaaaaaabb...', '....aaaaaabb....', '.....bbbbbb.....'],
 'nut': ['', '', '......dd........', '....aaaaaa......', '...acaaaaaab....', '..acaaaaaaaab...', '..aaaaaaaaaab...', '..aaaaaaaaabb...', '...aaaaaaabb....', '....bbbbbbb.....'],
 'gem': ['', '', '.....cccccc.....', '....cwwccaab....', '...cwcccaaaab...', '...aaaaaaaabb...', '....aaaaaabb....', '.....aaaabb.....', '......aabb......', '.......bb.......'],
 'crystal': ['', '.......c........', '......cwa.......', '......cwa.......', '...c..cwab..c...', '..cwa.caab.cwa..', '..cwa.caab.caa..', '..caab.ab.cab...', '...aabbabbab....', '....aaaaaaa.....', '.....bbbbb......'],
 'stone': ['', '', '', '', '......aaaa......', '....acccaaab....', '...acwcaaaabb...', '...aaaaaaaabb...', '...baaaaaabbb...', '....bbbbbbbb....'],
 'feather': ['', '..........ac....', '.........aca....', '........acab....', '.......acab.....', '......acab......', '.....acab.......', '....acab........', '....aab.........', '...hab..........', '..h.............', '.h..............'],
 'beetle': ['', '.....e....e.....', '......e..e......', '......dddd......', '.....daaaad.....', '....aacaacaa....', '....acaaacaa....', '....aaaaaaaa....', '....aaaaaaaa....', '.....aabbaa.....', '....e.....e.....'],
 'butterfly': ['', '..aaa......aaa..', '.acwaa....aawca.', '.aaaaa.ee.aaaaa.', '..aaaaaeeaaaaa..', '...aaa.ee.aaa...', '..aaaa.ee.aaaa..', '..acaa.ee.aaca..', '...aa..ee..aa...', '.......e........'],
 'snail': ['', '', '.......aaaa.....', '......acddaa....', '.....acdaada....', '.....adaacdab...', '.....addddab....', '.e....aaaabb....', '.ce.cccccccccc..', '..cccccccccccc..'],
 'seed': ['', '', '', '.....a...a......', '....aca.aca.....', '....aab.aab.....', '.....b...b......', '..a....a........', '.aca..aca.......', '.aab..aab.......', '..b....b........'],
 'fern': ['', '.......g........', '.....g.g.g......', '......ggg.......', '....g.ggg.g.....', '.....ggggg......', '...g.ggggg.g....', '....ggggggg.....', '.......g........', '.......h........', '.......h........'],
 'moss': ['', '', '', '', '.....a..a.......', '...a.ac.ac.a....', '..acaaaaaaaca...', '..aaaacaaaaaa...', '.aaacaaaacaaab..', '.abaaaaabaaabb..', '..bbbbbbbbbbb...'],
 'bottle': ['', '......hhh.......', '......wcw.......', '.......w........', '.....wwwww......', '....wddddaw.....', '....wdadaaw.....', '....waddaaw.....', '....wddaadw.....', '....waaaaaw.....', '.....wwwww......'],
 'straw': ['', '...a...a...a....', '....a..a..a.....', '....ac.a.ca.....', '.....acaca......', '.....acaca......', '.....ddddd......', '.....acaca......', '....acacaca.....', '...acac.caca....', '...aa.....aa....'],
 'eggs': ['', '', '', '.....ww.ww......', '....wcwwwcw.....', '....wwwbwwwb....', '..ww.bb.bb......', '.wcwww.ww.......', '.wwwbwwcww......', '..bb..wwwb......', '.......bb.......'],
 'fur': ['', '', '.....a..a.......', '....aca.aca.a...', '...acaacaacaa...', '..acaaaaaaaaca..', '..aaaacaaaaaab..', '..baaaaaaacabb..', '...bbaaaaaabb...', '.....bbbbbb.....'],
 'skull': ['', '.......g........', '.....aaaaa......', '....awwwwwa.....', '....wwwwwww.....', '....wKwwwKw.....', '....wwwKwww.....', '.....wKwKw......', '......www.......', '.......g........', '......ggg.......', '.....g.g.g......'],
 'firefly': ['', '...c.....c......', '....c...c.......', '.....aaaa.......', '....aaaaaa.ww...', '....aaaaaawcw...', '.....aaaaaww....', '.....dddd.......', '....ddwwdd......', '....dwwwwd......', '.....dddd.......'],
 'husk': ['', '', '.....aaaa.......', '....acccaa......', '...acaaaaab.....', '..eacaaaaabe....', '...aaaabaab.....', '..eaaabaabbe....', '...aabaabab.....', '....bbbbbb......', '...e..e..e......'],
 'sparkle': ['', '......c.........', '.....cwc........', '...ccwwwcc......', '.....cwc....a...', '......c....awa..', '.........aawwwa.', '..a.......awa...', '.awa.......a....', '..a...a.........', '.....awa........', '......a.........'],
 'clover': ['', '', '....aa..aa......', '...acaaacaa.....', '...aaaaaaaa.....', '....aaaaaa......', '..aa.aaaa.aa....', '.acaaaggaacaa...', '.aaaaagaaaaab...', '..aab.g..abb....', '......g.........', '.....g..........'],
 'wing': ['', '', '..cccc..........', '.cwwwcc.........', '.cwccwccc.......', '..cwccwwcc......', '...ccwccwcc.....', '....cccwwcc.....', '......cccccc....', '........cccc....', '..........cc....'],
}
G_ = {'g': hx('#5AB85A'), 'h': hx('#3A7A3A')}
def pal7(a, b=None, c=None, d=None, e=None, g=None, h=None):
    P = pal5(a, b, c, d, e); P['g'] = hx(g) if g else G_['g']; P['h'] = hx(h) if h else G_['h']; return P
# 채집물 50종 (흔한 것 → 전설): (id, 이름, 틀, 색, 무늬)
FORAGE = [
 ('g2_acorn', '도토리', 'acorn', pal7('#C8884A', d='#7A5430', e='#5A3E24'), ()),
 ('g2_cone', '솔방울', 'cone', pal7('#9A6A40'), ()),
 ('g2_clover3', '세잎클로버', 'clover', pal7('#5AC85A'), ()),
 ('g2_pebble', '동글 조약돌', 'stone', pal7('#9A98A8'), ()),
 ('g2_daisy', '들꽃', 'flower', pal7('#F8F0F0', d='#FFD040'), ()),
 ('g2_fern', '고사리', 'fern', pal7('#5A9A3A', g='#6AB04A', h='#3A7A2A'), ()),
 ('g2_moss', '촉촉 이끼', 'moss', pal7('#5A9A5A'), ()),
 ('g2_maple', '빨간 단풍잎', 'maple', pal7('#E0503A', h='#8A3A2A'), ()),
 ('g2_ginkgo', '노란 은행잎', 'fan', pal7('#F0C83A', h='#8A7A3A'), ()),
 ('g2_crowf', '까마귀 깃털', 'feather', pal7('#3A3A5A', h='#2A2A3A'), ()),
 ('g2_rasp', '산딸기', 'berries', pal7('#E04A5A'), ()),
 ('g2_blue', '블루베리', 'berries', pal7('#4A5AC8'), ()),
 ('g2_chest', '알밤', 'nut', pal7('#8A5A3A', d='#5AB85A'), ()),
 ('g2_walnut', '호두', 'nut', pal7('#C8A070', d='#8A6A40'), ('speckle',)),
 ('g2_catnip', '개박하', 'fern', pal7('#7AC8A0', g='#8AD8A8', h='#4A9A6A'), ()),
 ('g2_pseed', '호박씨', 'seed', pal7('#F0E0B0'), ()),
 ('g2_sseed', '해바라기씨', 'seed', pal7('#5A4A3A', c='#8A7A6A'), ('stripe',)),
 ('g2_snail', '달팽이 껍질', 'snail', pal7('#C8A070', d='#8A5A3A'), ()),
 ('g2_lady', '무당벌레', 'beetle', pal7('#E03A3A', d='#2A2030', e='#2A2030'), ('dots',)),
 ('g2_straw', '빗자루 짚', 'straw', pal7('#E0C070', d='#7A4AA8'), ()),
 ('g2_mushred', '빨간 독버섯', 'mush', pal7('#E0303A'), ()),
 ('g2_mushpine', '송이버섯', 'mush', pal7('#B88A5A'), ()),
 ('g2_bell', '은방울꽃', 'bell', pal7('#F8F8FF'), ()),
 ('g2_cicada', '매미 허물', 'husk', pal7('#C8A060', e='#8A6A3A'), ()),
 ('g2_firefly', '반딧불이', 'firefly', pal7('#4A3A5A', d='#E8FF8A'), ()),
 ('g2_batleaf', '박쥐 날개 잎', 'maple', pal7('#4A3A6A', h='#2A2040'), ()),
 ('g2_eve', '달맞이꽃', 'flower', pal7('#FFE070', d='#FFA030'), ()),
 ('g2_spider', '거미 버섯', 'mush', pal7('#6A4A8A'), ('dots',)),
 ('g2_wild', '들장미 열매', 'fruit', pal7('#E04A3A', g='#5A9A3A'), ()),
 ('g2_crab', '꽃사과', 'fruit', pal7('#FF8A7A', g='#5A9A3A'), ()),
 ('g2_poison', '독사과', 'fruit', pal7('#9A4AC8', g='#3A7A3A'), ('speckle',)),
 ('g2_bfly', '나비 날개', 'butterfly', pal7('#7AB8FF', e='#3A3A5A'), ()),
 ('g2_stag', '사슴벌레', 'beetle', pal7('#5A3A2A', d='#3A2A20', e='#2A1E16'), ()),
 ('g2_spegg', '거미 알', 'eggs', pal7('#E8E0F0', b='#B8A8C8'), ()),
 ('g2_ghostf', '유령 꽃', 'flower', pal7('#D8E8FF', d='#8AF0E0'), ('glow',)),
 ('g2_skullf', '해골 꽃', 'skull', pal7('#F0F0E8'), ()),
 ('g2_moonm', '달빛 버섯', 'mush', pal7('#7AD8F0'), ('glow',)),
 ('g2_rmoss', '무지개 이끼', 'moss', pal7('#8AD88A'), ('rainbow',)),
 ('g2_shiny', '반짝 돌', 'gem', pal7('#B8C8E0'), ()),
 ('g2_amber', '호박석', 'gem', pal7('#F0A030'), ()),
 ('g2_amethyst', '자수정', 'crystal', pal7('#B07AE8'), ()),
 ('g2_fossil', '조개 화석', 'snail', pal7('#B8B0A0', d='#8A8478'), ('speckle',)),
 ('g2_moonst', '월장석', 'crystal', pal7('#C8E0FF'), ('glow',)),
 ('g2_stardust', '별가루 병', 'bottle', pal7('#FFE070', d='#FFF4B0', h='#8A6A3A'), ()),
 ('g2_fairy', '요정 날개 가루', 'wing', pal7('#C8F0FF', c='#E8F8FF'), ()),
 ('g2_wolf', '늑대 털 뭉치', 'fur', pal7('#8A8A9A'), ()),
 ('g2_starfall', '별똥별 조각', 'sparkle', pal7('#FFD866', c='#FFE8A0'), ()),
 ('g2_gacorn', '황금 도토리', 'acorn', pal7('#FFD040', d='#E0A020', e='#B07A10'), ()),
 ('g2_unicorn', '유니콘 털', 'fur', pal7('#F8F0FF'), ('rainbow',)),
 ('g2_pumpmoon', '호박달 씨앗', 'seed', pal7('#FF8A2A', c='#FFD866'), ('glow',)),
]
# 낚싯대 5단계
def rod(col, tip, line='#E8E8F0'):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(12): x, y = 2 + i, 14 - i; d.point((x, y), fill=hx(col) + (255,)); d.point((x + 1, y), fill=K + (255,)); d.point((x - 1, y), fill=K + (255,))
    d.rectangle([2, 12, 4, 14], fill=hx('#4A3A2A') + (255,)); d.point((5, 12), fill=hx(tip) + (255,)); d.point((3, 11), fill=hx(tip) + (255,))
    d.line([(13, 2), (14, 3), (14, 10)], fill=hx(line) + (255,)); d.rectangle([13, 10, 15, 12], fill=hx('#E04A4A') + (255,)); d.point((14, 10), fill=(255, 255, 255, 255))
    return im
RODS = [('나무 낚싯대', rod('#A8784A', '#7A5430')), ('대나무 낚싯대', rod('#9AC85A', '#5A8A3A')), ('은 낚싯대', rod('#D8D8E8', '#8AA8E0')), ('달빛 낚싯대', rod('#8AA8FF', '#FFE066')), ('호박달 낚싯대', rod('#FF8A2A', '#B07AFF'))]

def sheet(items, T, maker):
    im = Image.new('RGBA', (16 * len(items), 16), (0, 0, 0, 0))
    for i, it in enumerate(items): im.alpha_composite(maker(it, T), (i * 16, 0))
    return im
mk = lambda it, T: draw(T[it[2]], it[3], it[4], 200 if 'glow' in it[4] and it[2] in ('jelly', 'horse') else 255)
if __name__ == '__main__':
    fish, forage = sheet(FISH, FT, mk), sheet(FORAGE, GT, mk)
    rods = Image.new('RGBA', (16 * len(RODS), 16), (0, 0, 0, 0))
    for i, (_, r) in enumerate(RODS): rods.alpha_composite(r, (i * 16, 0))
    art = os.path.join(ROOT, 'public', 'art')
    fish.save(os.path.join(art, 'fish.png')); forage.save(os.path.join(art, 'forage.png')); rods.save(os.path.join(art, 'rods.png'))
    if len(sys.argv) > 1:   # 시안: 크게 + 이름
        from PIL import ImageFont
        fp = [os.path.join(ROOT, 'tools', 'iso', 'fonts', f) for f in ('Galmuri11.ttf',)]
        try: fnt = ImageFont.truetype(sys.argv[2], 12)
        except Exception: fnt = ImageFont.load_default()
        k, cw, ch, cols = 4, 92, 92, 10
        groups = [('물고기 40 + 쓰레기 3', FISH, fish), ('채집물 50', FORAGE, forage), ('낚싯대 5', [(None, n) for n, _ in RODS], rods)]
        rows = sum((len(g[1]) + cols - 1) // cols for g in groups)
        S = Image.new('RGBA', (cw * cols, rows * ch + 30 * len(groups)), (250, 241, 226, 255)); d = ImageDraw.Draw(S); y = 0
        for title, lst, im in groups:
            d.text((8, y + 6), title, fill=K, font=fnt); y += 30
            for i, it in enumerate(lst):
                x, yy = (i % cols) * cw, y + (i // cols) * ch
                S.alpha_composite(im.crop((i * 16, 0, i * 16 + 16, 16)).resize((64, 64), Image.NEAREST), (x + 14, yy + 4))
                nm = it[1]; tw = d.textlength(nm, font=fnt)
                d.text((x + cw / 2 - tw / 2, yy + 72), nm, fill=K, font=fnt)
            y += ((len(lst) + cols - 1) // cols) * ch
        S.save(sys.argv[1])
