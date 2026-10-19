# 이야기 NPC 동물 6명 (48×48 한 칸, 앞모습) → public/art/npcs.png  (index.html NPC_DEF의 spr 번호 순서)
# 0 나비(고양이) 1 배트리(박쥐 우체부) 2 캇파(갓파) 3 아울라(부엉이 사서) 4 맨디(맨드레이크) 5 짚신(꼬마 허수아비)
import os, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K = (34, 22, 50, 255)
def hx(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def cell():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def outline(im):
    s = im.copy(); sp = s.load(); dp = im.load()
    for y in range(48):
        for x in range(48):
            if sp[x, y][3]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 48 and 0 <= ny < 48 and sp[nx, ny][3] and sp[nx, ny][:3] != K[:3]: dp[x, y] = K; break
    return im
def px(d, pts, c):
    for p in pts: d.point(p, fill=c)
def eyes(d, x1, x2, y, big=False, col=K):
    for x in (x1, x2):
        d.rectangle([x, y, x + 1, y + (2 if big else 1)], fill=col); d.point((x, y), fill=hx('#FFFFFF'))
def blush(d, x1, x2, y): d.rectangle([x1, y, x1 + 1, y], fill=hx('#FF9AB8')); d.rectangle([x2, y, x2 + 1, y], fill=hx('#FF9AB8'))

def cat():   # 나비: 크림색 + 주황 얼룩, 목에 방울, 앉은 자세
    im, d = cell(); C, O, Cd = hx('#F4E8D0'), hx('#F0A050'), hx('#D8C8A8')
    d.ellipse([15, 30, 33, 46], fill=C); d.rectangle([17, 40, 31, 46], fill=C)            # 몸
    d.ellipse([28, 38, 38, 44], fill=O); d.rectangle([34, 30, 37, 40], fill=O); d.ellipse([33, 27, 38, 32], fill=O)   # 꼬리
    d.ellipse([13, 16, 35, 34], fill=C)                                                     # 머리
    d.polygon([(14, 22), (15, 11), (21, 17)], fill=C); d.polygon([(34, 22), (33, 11), (27, 17)], fill=C)   # 귀
    d.polygon([(16, 19), (16, 14), (19, 17)], fill=hx('#FFB8C8')); d.polygon([(32, 19), (32, 14), (29, 17)], fill=hx('#FFB8C8'))
    d.ellipse([13, 16, 23, 25], fill=O)                                                     # 얼룩
    d.rectangle([18, 43, 21, 46], fill=Cd); d.rectangle([26, 43, 29, 46], fill=Cd)          # 앞발
    eyes(d, 19, 27, 24, True, hx('#3A8A4A')); px(d, [(23, 28), (24, 28)], hx('#FF8AA0')); px(d, [(22, 29), (25, 29)], K)
    blush(d, 16, 30, 28)
    d.rectangle([18, 33, 30, 34], fill=hx('#C8486A')); d.ellipse([22, 34, 26, 38], fill=hx('#FFD040')); d.point((24, 37), fill=K)   # 방울
    return outline(im)
def bat():   # 배트리: 보라 박쥐, 우편 가방 + 편지
    im, d = cell(); B, Bd, W = hx('#7A5AA8'), hx('#5A3E88'), hx('#4A3470')
    d.polygon([(4, 20), (12, 14), (18, 22), (16, 30), (12, 26), (8, 30), (6, 25)], fill=W); d.polygon([(44, 20), (36, 14), (30, 22), (32, 30), (36, 26), (40, 30), (42, 25)], fill=W)   # 날개
    d.ellipse([15, 16, 33, 38], fill=B); d.ellipse([18, 26, 30, 38], fill=hx('#9A7AC8'))    # 몸·배
    d.polygon([(17, 18), (16, 8), (22, 15)], fill=B); d.polygon([(31, 18), (32, 8), (26, 15)], fill=B)
    eyes(d, 19, 27, 21, True); px(d, [(22, 26), (25, 26)], hx('#FFFFFF')); d.line([(22, 25), (25, 25)], fill=K); blush(d, 17, 29, 24)
    d.line([(16, 24), (33, 34)], fill=hx('#8A5A30'), width=2); d.rectangle([28, 31, 37, 38], fill=hx('#B8875A')); d.rectangle([28, 31, 37, 32], fill=hx('#8A5A30'))   # 가방
    d.rectangle([30, 28, 36, 32], fill=hx('#F2EAD8')); d.line([(30, 28), (33, 30), (36, 28)], fill=hx('#C8486A'))    # 편지
    d.rectangle([20, 38, 22, 41], fill=Bd); d.rectangle([26, 38, 28, 41], fill=Bd)
    return outline(im)
def kappa():   # 캇파: 초록, 등딱지, 머리 접시(물), 낚싯대
    im, d = cell(); G, Gd, Y = hx('#6AB86A'), hx('#4A8A4A'), hx('#F0D070')
    d.ellipse([12, 24, 36, 44], fill=hx('#8A6A3A')); d.ellipse([14, 26, 34, 42], fill=hx('#A8844A'))   # 등딱지 (뒤)
    d.rectangle([17, 30, 31, 44], fill=G); d.ellipse([17, 26, 31, 36], fill=G); d.rectangle([19, 34, 29, 42], fill=Y)   # 몸·배
    d.rectangle([18, 44, 22, 46], fill=Gd); d.rectangle([26, 44, 30, 46], fill=Gd)
    d.ellipse([12, 8, 36, 30], fill=G)                                                      # 머리
    d.ellipse([15, 6, 33, 13], fill=hx('#E8F0F8')); d.ellipse([17, 7, 31, 11], fill=hx('#8AC8F0'))   # 접시 + 물
    for x in range(12, 37, 3): d.polygon([(x, 12), (x + 2, 12), (x + 1, 16)], fill=hx('#3A6A3A'))      # 머리카락
    eyes(d, 18, 28, 18, True); d.polygon([(21, 23), (27, 23), (24, 27)], fill=hx('#F0B040'))           # 부리
    d.line([(34, 44), (42, 6)], fill=hx('#9AC85A'), width=1); d.line([(42, 6), (44, 22)], fill=hx('#E8E8F0')); d.rectangle([43, 22, 45, 24], fill=hx('#E04A4A'))   # 낚싯대
    d.ellipse([32, 33, 36, 37], fill=G)
    return outline(im)
def owl():   # 아울라: 갈색 부엉이, 동그란 안경, 책
    im, d = cell(); Br, Bl, Bd = hx('#9A6A44'), hx('#E8D0A8'), hx('#6A4428')
    d.ellipse([12, 14, 36, 46], fill=Br); d.ellipse([16, 26, 32, 44], fill=Bl)
    for y in range(30, 43, 4):
        for x in range(18, 31, 4): d.point((x + (y // 4) % 2 * 2, y), fill=hx('#C8A878'))
    d.polygon([(13, 18), (14, 8), (20, 15)], fill=Br); d.polygon([(35, 18), (34, 8), (28, 15)], fill=Br)   # 귀깃
    d.ellipse([15, 15, 24, 24], fill=Bl); d.ellipse([24, 15, 33, 24], fill=Bl)
    d.ellipse([15, 15, 24, 24], outline=hx('#3A3A4A')); d.ellipse([24, 15, 33, 24], outline=hx('#3A3A4A')); d.line([(23, 19), (25, 19)], fill=hx('#3A3A4A'))   # 안경
    d.ellipse([18, 18, 21, 21], fill=K); d.ellipse([27, 18, 30, 21], fill=K); px(d, [(19, 18), (28, 18)], hx('#FFFFFF'))
    d.polygon([(23, 23), (25, 23), (24, 27)], fill=hx('#F0A030'))
    d.rectangle([16, 34, 32, 42], fill=hx('#3A6AA8')); d.rectangle([24, 34, 24, 42], fill=hx('#22183F')); d.rectangle([17, 35, 23, 41], fill=hx('#F2EAD8')); d.rectangle([25, 35, 31, 41], fill=hx('#F2EAD8'))   # 책
    d.rectangle([18, 44, 21, 46], fill=hx('#F0A030')); d.rectangle([27, 44, 30, 46], fill=hx('#F0A030'))
    return outline(im)
def mandrake():   # 맨디: 뿌리 몸, 머리 위 잎, 볼 빨간 부끄럼쟁이
    im, d = cell(); R, Rd = hx('#E8C898'), hx('#C8A070')
    d.ellipse([15, 20, 33, 40], fill=R); d.polygon([(19, 38), (16, 46), (21, 41)], fill=R); d.polygon([(29, 38), (32, 46), (27, 41)], fill=R)   # 몸·다리
    d.polygon([(16, 28), (9, 32), (16, 32)], fill=R); d.polygon([(32, 28), (39, 32), (32, 32)], fill=R)   # 팔
    for i in range(3): d.line([(20 + i * 3, 34 + i), (21 + i * 3, 37)], fill=Rd)
    G, Gd = hx('#5AB85A'), hx('#3A8A3A')
    d.ellipse([12, 4, 22, 18], fill=G); d.ellipse([26, 4, 36, 18], fill=G); d.ellipse([19, 2, 29, 16], fill=hx('#6AC86A'))
    d.line([(17, 6), (21, 15)], fill=Gd); d.line([(31, 6), (27, 15)], fill=Gd); d.line([(24, 4), (24, 17)], fill=Gd)
    eyes(d, 19, 27, 26); d.ellipse([22, 30, 26, 33], fill=hx('#8A3A4A')); blush(d, 16, 30, 29); blush(d, 16, 30, 30)
    return outline(im)
def scarecrow():   # 짚신: 밀짚모자, 자루 얼굴(바느질 웃음), 체크 셔츠, 막대 팔
    im, d = cell(); S, Sd = hx('#D8B878'), hx('#B89858')
    d.rectangle([23, 30, 25, 47], fill=hx('#8A5A30'))                                          # 막대
    d.line([(6, 28), (42, 28)], fill=hx('#8A5A30'), width=2)                                   # 팔 막대
    d.rectangle([15, 25, 33, 40], fill=hx('#C84A4A'))
    for x in range(15, 34, 4): d.line([(x, 25), (x, 40)], fill=hx('#E87A6A'))
    for y in range(27, 41, 4): d.line([(15, y), (33, y)], fill=hx('#A83A3A'))
    d.rectangle([22, 32, 26, 38], fill=hx('#4A6AC8'))                                          # 덧댄 천
    for x in (8, 11, 37, 40): d.line([(x, 27), (x - 1, 31)], fill=hx('#E8C870'))               # 손 짚
    d.ellipse([15, 9, 33, 27], fill=S)                                                          # 자루 얼굴
    d.ellipse([10, 9, 38, 14], fill=hx('#E8C870')); d.ellipse([16, 2, 32, 12], fill=hx('#E8C870')); d.rectangle([16, 9, 32, 10], fill=hx('#C84A4A'))   # 모자
    d.rectangle([19, 16, 21, 18], fill=K); d.rectangle([27, 16, 29, 18], fill=K)                # 단추 눈
    d.line([(19, 22), (29, 22)], fill=K); px(d, [(20, 21), (20, 23), (23, 21), (23, 23), (26, 21), (26, 23), (29, 21), (29, 23)], K)   # 바느질 웃음
    blush(d, 16, 30, 20)
    return outline(im)
SPR = [('나비', cat), ('배트리', bat), ('캇파', kappa), ('아울라', owl), ('맨디', mandrake), ('짚신', scarecrow)]
if __name__ == '__main__':
    sheet = Image.new('RGBA', (48 * len(SPR), 48), (0, 0, 0, 0))
    for i, (_, f) in enumerate(SPR): sheet.alpha_composite(f(), (i * 48, 0))
    sheet.save(os.path.join(ROOT, 'public', 'art', 'npcs.png'))
    if len(sys.argv) > 1:
        bg = Image.new('RGBA', sheet.size, (250, 241, 226, 255)); bg.alpha_composite(sheet); bg.resize((sheet.width * 5, sheet.height * 5), Image.NEAREST).save(sys.argv[1])
    print(len(SPR))
