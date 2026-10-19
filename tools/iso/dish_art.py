# 요리 40종 그림 (16×16 픽셀, 직접 그림) → public/art/dishes.png (index.html DISH_LIST 순서)
# python3 tools/iso/dish_art.py [시안.png 글꼴.ttf]
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fishing_art import draw, pal7, hx, K, ROOT
# 틀: a 주색 b 그림자 c 밝은 곳 d 포인트 e 포인트 어둠 g 초록 h 초록 어둠 w 흰색 (그릇·접시는 w/x 고정색으로)
T = {
 'bowl': ['', '', '', '....c.c..c......', '.....c..c.......', '..aaaaaaaaaaaa..', '.acaadaaaadaaab.', '.wwwwwwwwwwwwwww', '..wwwwwwwwwwww..', '...wwwwwwwwww...', '....wwwwwwww....', '.....ewwwwwe....'],
 'plate': ['', '', '', '', '....aaaaaaa.....', '...acccaaaaad...', '..aaaaaaaaaaddd.', '...bbbbbbbbb.d..', '.wwwwwwwwwwwwww.', 'wwwwwwwwwwwwwwww', '.eeeeeeeeeeeeee.'],
 'skewer': ['', '..............e.', '.............e..', '..........aaae..', '.........acab...', '.......ddde.....', '......dcdd......', '.....aaae.......', '....acab........', '...ddde.........', '..dcdd..........', '.e..............', 'e...............'],
 'cookie': ['', '', '...aaaaaaaa.....', '..acaadaaaaa....', '.acaaaaaaadab...', '.aaadaaaaaaab...', '.aaaaaaadaaab...', '.aadaaaaaaabb...', '..aaaadaaabb....', '...bbbbbbbb.....'],
 'pie': ['', '', '..........cc....', '........ccaac...', '......ccaaaab...', '....ccaaaaabb...', '..ccdddddddbb...', '.cdddedddeddb...', '.wwwwwwwwwwwb...', '.bbbbbbbbbbbb...'],
 'cake': ['', '......d.........', '......e.........', '...ddddddddd....', '..dcwwwwwwwwd...', '..aaaaaaaaaaab..', '..ccccccccccab..', '..aaaaaaaaaaab..', '..aaaaaaaaaaab..', '.wwwwwwwwwwwwww.', '..eeeeeeeeeeee..'],
 'cup': ['', '.....c..c.......', '......c..c......', '.....c..c.......', '..wwwwwwwwww....', '..waaaaaaaaww...', '..wcaaaaaaaw.w..', '..waaaaaaaaw.w..', '...waaaaaaww....', '....wwwwww......', '.eeeeeeeeeeee...'],
 'bottle': ['', '......ee........', '......ww........', '.....wwww.......', '.....waaw.......', '....waaaaw......', '....wcaaaw......', '....waddaw......', '....waddaw......', '....waaaaw......', '....waaaaw......', '.....wwww.......'],
 'jelly': ['', '', '.....cccccc.....', '....caaaaaac....', '....awaaaaaa....', '...aawaaaaaaa...', '...aaaaaaaaab...', '...bbbbbbbbbb...', '.wwwwwwwwwwwwww.', '..eeeeeeeeeeee..'],
 'macaron': ['', '', '', '....aaaaaaa.....', '...acaaaaaaa....', '...bbbbbbbbb....', '...ddddddddd....', '...aaaaaaaaa....', '...acaaaaaab....', '....bbbbbbb.....'],
 'bread': ['', '', '', '....aaaaaa......', '..aacaaaaaaa....', '.acaawaaawaab...', '.aaaaaaaaaaab...', '.aaaaaaaaaaab...', '..bbbbbbbbbb....'],
 'sushi': ['', '', '', '', '...aaa...aaa....', '..acaab.acaab...', '..dddd..dddd....', '..wwwwh.wwwwh...', '..wwwwh.wwwwh...', '.eeeeeeeeeeeee..'],
 'parfait': ['', '.....dd.........', '....dcdd........', '...wwwwwww......', '...wcccccw......', '...waaaaaw......', '...wdddddw......', '....waaaw.......', '.....www........', '......w.........', '....wwwww.......'],
 'steak': ['', '', '', '', '...aaaaaaaa.....', '..aceaeaeaab.g..', '..aaaaaaaaab.gg.', '...bbbbbbbb.dd..', '.wwwwwwwwwwwwww.', 'wwwwwwwwwwwwwwww', '.eeeeeeeeeeeeee.'],
 'pot': ['', '..c..c..c.......', '...c..c..c......', '..aaaaaaaaaa....', '.eaddadaadaae...', '.eeeeeeeeeeee...', 'eewwwwwwwwwwee..', '..wwwwwwwwww....', '..wwwwwwwwww....', '...bbbbbbbb.....'],
 'roll': ['', '', '', '..dd..dd..dd....', '.daad.daad.daad.', '.dacd.dacd.dacd.', '.daad.daad.daad.', '..hh..hh..hh....', '.wwwwwwwwwwwwww.', '..eeeeeeeeeeee..'],
 'toast': ['', '', '..bbbbbbbbb.....', '.bcccccccccb....', '.bcaaaaaaacb....', '.bcadaadaacb....', '.bcaaaaadacb....', '.bcadaaaaacb....', '.bcaaaaaaacb....', '.bbbbbbbbbbb....'],
 'muffin': ['', '', '.....aaaa.......', '...aacaaada.....', '..acadaaaaaa....', '..aaaaaadaab....', '...dededede.....', '...deddeded.....', '....dededd......', '....eeeeee......'],
 'candy': ['', '.......h........', '......hhg.......', '.......h........', '....aaaaaaa.....', '...acaaaaaaa....', '...awaaaaaaab...', '...aaaaaaaab....', '....aaaaaab.....', '.....ddddd......', '...dddddddd.....'],
 'mochi': ['', '', '', '.....cccc.......', '...ccaaaacc.....', '..caaaaaaaac....', '..aadaaaadaa....', '..aaaaaaaaab....', '...bbbbbbbb.....', '.wwwwwwwwwwww...', '..eeeeeeeeee....'],
 'feast': ['', '...d..d..d......', '..ddddddddd.....', '..dcwwwwwwd.....', '.aaaaaaaaaaa....', '.acaaaaaaaaab.g.', '.aaaaaaaaaaab.gg', '..bbbbbbbbbb.d..', 'wwwwwwwwwwwwwwww', '.eeeeeeeeeeeeee.'],
}
W_, E_ = hx('#F4ECF8'), hx('#B8A8D0')
def P(a, **k):
    p = pal7(a, **k); p['w'] = k.get('w') and hx(k['w']) or W_
    if 'e' not in k: p['e'] = E_
    return p
# 요리 40종 (흔한 것 → 전설): (id, 이름, 틀, 색, 무늬)
DISH = [
 ('d_pseedsoup', '호박씨 크림수프', 'bowl', P('#F0B860', d='#F08A2A', c='#FFE0A0'), ()),
 ('d_acorncookie', '도토리 쿠키', 'cookie', P('#C8884A', d='#5A3E24'), ()),
 ('d_minnowfry', '유령 피라미 튀김', 'plate', P('#E8C070', d='#C8D8F0'), ('speckle',)),
 ('d_mushskewer', '버섯 꼬치구이', 'skewer', P('#C85AA8', d='#B88A5A', e='#6A4A30'), ()),
 ('d_jamtoast', '산딸기 잼 토스트', 'toast', P('#E04A5A', b='#B8875A', c='#E8C890', d='#FF8A9A'), ()),
 ('d_carrotmuffin', '당근 머핀', 'muffin', P('#E8A050', d='#F08A2A', e='#B85A2A'), ()),
 ('d_clovertea', '세잎클로버 차', 'cup', P('#7AC86A', c='#E8F8E0'), ()),
 ('d_tomatojuice', '피처럼 붉은 토마토주스', 'bottle', P('#C8202A', d='#FF5A5A'), ()),
 ('d_crucianstew', '호박 붕어 버섯 조림', 'plate', P('#F08A2A', d='#B88A5A'), ('stripe',)),
 ('d_batwrap', '박쥐 날개 잎 쌈', 'roll', P('#5A8A3A', d='#4A3A6A'), ()),
 ('d_spidermac', '거미 버섯 마카롱', 'macaron', P('#8A5AB8', d='#F0E0F0'), ()),
 ('d_bluepie', '블루베리 파이', 'pie', P('#E8C080', d='#4A5AC8', e='#2A3A8A'), ()),
 ('d_killiomelet', '이끼 송사리 오믈렛', 'plate', P('#FFE070', d='#7AB86A'), ()),
 ('d_chestnut', '꿀 군밤 꼬치', 'skewer', P('#8A5A3A', d='#E0A040', e='#6A4A30'), ()),
 ('d_ghostmallow', '유령 마시멜로', 'jelly', P('#F0F4FF', c='#FFFFFF', b='#C8D0E8'), ()),
 ('d_loachsoup', '늪지 추어탕', 'bowl', P('#8A6A3A', d='#5A9A3A', c='#B8A070'), ()),
 ('d_poisoncandy', '독사과 캔디', 'candy', P('#9A4AC8', d='#E0C8FF'), ()),
 ('d_cornsoup', '옥수수 달빛수프', 'bowl', P('#FFD860', d='#8AE0F0', c='#FFF0A0'), ()),
 ('d_jellyjelly', '젤리 해파리 젤리', 'jelly', P('#B89AFF', c='#E8D8FF'), ('dots',)),
 ('d_crayboil', '거미 가재 매운찜', 'pot', P('#E0402A', d='#C82020', e='#3A3448'), ()),
 ('d_bonesoup', '해골 메기 사골탕', 'bowl', P('#F0ECE0', d='#B8B4A8', c='#FFFFFF'), ()),
 ('d_cottonpudding', '솜사탕 넙치 푸딩', 'jelly', P('#FFB8E0', c='#FFE0F0', b='#E08AB8'), ()),
 ('d_moontrout', '달빛 송어 구이', 'plate', P('#8AA8E0', d='#E8D070'), ('speckle',)),
 ('d_fireflyrisotto', '반딧불이 리소토', 'bowl', P('#F0E8C0', d='#E8FF8A', c='#FFFFFF'), ('dots',)),
 ('d_skullbread', '해골 꽃 빵', 'bread', P('#E0B070', d='#F0F0E8'), ()),
 ('d_witchstew', '마녀 솥 스튜', 'pot', P('#5AA84A', d='#C86AE8', e='#2A2230'), ()),
 ('d_rainbowsushi', '무지개 송어 초밥', 'sushi', P('#FF8A6A', d='#2A3A2A', h='#3A5A3A'), ('rainbow',)),
 ('d_starcookie', '별가루 쿠키', 'cookie', P('#FFD860', d='#FFF4B0'), ('dots',)),
 ('d_vampsteak', '뱀파이어 피라냐 스테이크', 'steak', P('#A82A3A', e='#5A1A2A', d='#E0402A'), ()),
 ('d_anglerpot', '호박등 아귀 전골', 'pot', P('#E08A3A', d='#FFE070', e='#3A3448'), ()),
 ('d_amberbream', '호박석 꿀 도미 조림', 'plate', P('#E0303A', d='#F0A030'), ('scale',)),
 ('d_fairycake', '요정 날개 케이크', 'cake', P('#C8F0FF', c='#FFFFFF', d='#FF9AD0', e='#B07AFF'), ()),
 ('d_seahorsetea', '유령 해마 차', 'cup', P('#A8D8F0', c='#E0F4FF'), ('glow',)),
 ('d_moonmochi', '달토끼 찹쌀떡', 'mochi', P('#F8F0FF', c='#FFFFFF', d='#FFB8D8'), ()),
 ('d_goldcarpbowl', '황금 잉어 덮밥', 'bowl', P('#FFC830', d='#FF8A2A', c='#FFE890'), ('scale',)),
 ('d_auroraparfait', '오로라 파르페', 'parfait', P('#8AE0C0', d='#C07AFF', c='#FFFFFF'), ('rainbow',)),
 ('d_dragonroll', '화룡 용비늘 롤', 'roll', P('#3AB88A', d='#E0403A', h='#2A2230'), ()),
 ('d_whalesoup', '별똥별 고래 수프', 'bowl', P('#4A6AC8', d='#FFE070', c='#8AA8FF'), ('dots',)),
 ('d_kingfeast', '호박달 메기왕 정찬', 'feast', P('#E07A1E', d='#FFD040', e='#B07A10'), ('stripe',)),
 ('d_lordbanquet', '호수의 주인 만찬', 'feast', P('#3A2A6A', d='#FFD866', c='#6A5AA8', e='#E0A020'), ('speckle', 'crown')),
]
if __name__ == '__main__':
    im = Image.new('RGBA', (16 * len(DISH), 16), (0, 0, 0, 0))
    for i, (_, _, t, p, ov) in enumerate(DISH): im.alpha_composite(draw(T[t], p, ov), (i * 16, 0))
    im.save(os.path.join(ROOT, 'public', 'art', 'dishes.png'))
    if len(sys.argv) > 1:
        from PIL import ImageFont
        fnt = ImageFont.truetype(sys.argv[2], 12); cols, cw, ch = 8, 112, 96
        S = Image.new('RGBA', (cw * cols, ch * 5), (250, 241, 226, 255)); d = ImageDraw.Draw(S)
        for i, (_, nm, *_r) in enumerate(DISH):
            x, y = (i % cols) * cw, (i // cols) * ch
            S.alpha_composite(im.crop((i * 16, 0, i * 16 + 16, 16)).resize((64, 64), Image.NEAREST), (x + 24, y + 4))
            for j, line in enumerate([nm[:8], nm[8:]] if len(nm) > 8 else [nm]): tw = d.textlength(line, font=fnt); d.text((x + cw / 2 - tw / 2, y + 70 + j * 13), line, fill=K, font=fnt)
        S.save(sys.argv[1])
    print(len(DISH))
