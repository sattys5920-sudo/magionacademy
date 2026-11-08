# 감기 이벤트 시안: NPC 14 명 모두 아픈 모습 + 물약 분류표 (게임에서 꺼낸 사람 NPC 그림은 인자로 받은 폴더의 av_*.png)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import cold_art as A
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
avdir, font = sys.argv[1], sys.argv[2]
F = ImageFont.truetype(font, 12); FS = ImageFont.truetype(font, 11)
npcs = Image.open(ROOT + '/public/art/npcs.png').convert('RGBA')
FACE = {0: (13, 14, 31), 1: (18, 12, 29), 2: (20, 16, 28), 3: (17, 18, 31), 4: (19, 23, 32), 5: (12, 9, 39), 13: (14, 20, 35), 14: (21, 27, 21), 15: (18, 15, 27), 16: (16, 15, 30)}
L = [('nabi', '나비', 0), ('batri', '배트리', 1), ('kappa', '캇파', 2), ('aula', '아울라', 3), ('mandi', '맨디', 4), ('jipsin', '스트로', 5), ('sera', '세라', None), ('madeleine', '마들렌', None), ('stella', '스텔라', None), ('leo', '레오', None), ('otumo', '오투모', 13), ('dodo', '도도', 14), ('selin', '셀린', 15), ('bone', '본', 16)]
SYM = ['fever', 'throat', 'nose', 'chill']; KO = {'fever': '열', 'throat': '목감기', 'nose': '콧물', 'chill': '오한'}
W, H = 7 * 70 + 10, 2 * 100 + 20
P = Image.new('RGBA', (W, H), A.hx('#1E1830')); g = ImageDraw.Draw(P)
for i, (id, ko, row) in enumerate(L):
    x0, y0 = 6 + (i % 7) * 70, 14 + (i // 7) * 100; k = SYM[i % 4]
    if row is None: fr = Image.open(f'{avdir}/av_{id}.png').convert('RGBA'); fx, fy, fs = 22, 15, 20
    else: fr = npcs.crop((0, row * 64, 64, row * 64 + 64)); fx, fy, fs = FACE[row]
    P.alpha_composite(fr, (x0, y0 + 10))
    P.alpha_composite(A.overlay(k), (x0 + fx + fs // 2 - 10, y0 + 10 + fy + int(fs * .35)))
    P.alpha_composite(A.breath(), (x0 + fx + fs - 2, y0 + 10 + fy + fs // 2))
    P.alpha_composite(A.bubble(k), (x0 + fx + fs // 2 - 8, y0 + 10 + max(0, fy - 16)))
    if k == 'chill': P.alpha_composite(A.shiver(20), (x0 + fx - 6, y0 + 10 + fy + fs // 2)); P.alpha_composite(A.shiver(20), (x0 + fx + fs + 2, y0 + 10 + fy + fs // 2))
    g.text((x0 + 32, y0 + 78), ko, font=F, fill=(240, 236, 250), anchor='mm'); g.text((x0 + 32, y0 + 91), KO[k], font=FS, fill=(255, 210, 120), anchor='mm')
P.resize((W * 3, H * 3), Image.NEAREST).save(D + '/out/all_npcs.png')
# 물약 분류표
T = Image.new('RGBA', (360, 4 * 44 + 30), A.hx('#1E1830')); g = ImageDraw.Draw(T)
g.text((10, 8), '증상 말풍선  →  감기 물약  ·  재료', font=F, fill=(255, 216, 102))
ROWS = [('fever', '열 내림 물약', '촉촉 이끼 · 고사리 · 달맞이꽃'), ('throat', '꿀 목 물약', '벌꿀 · 산딸기 · 은방울꽃'), ('nose', '콧물 뚝 물약', '블루베리 · 개박하 · 들꽃'), ('chill', '따끈 찜질 물약', '호박씨 · 서리 낙엽 · 해바라기씨')]
for i, (k, pn, mats) in enumerate(ROWS):
    y = 30 + i * 44; T.alpha_composite(A.bubble(k).resize((32, 30), Image.NEAREST), (10, y)); g.text((50, y + 8), KO[k], font=F, fill=(240, 236, 250))
    g.text((100, y + 8), '→', font=F, fill=(180, 170, 200)); T.alpha_composite(A.bottle(k), (120, y)); g.text((158, y + 2), pn, font=F, fill=(240, 236, 250)); g.text((158, y + 18), mats, font=FS, fill=(190, 182, 210))
T.resize((T.width * 3, T.height * 3), Image.NEAREST).save(D + '/out/potion_table.png')
print('ok')
