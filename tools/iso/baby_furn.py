# 「길 잃은 아기 동물」 방 가구 12종: 동물마다 하나, 그 위(spot)에서 아기 동물이 놀아요
#   python3 baby_furn.py → out/baby_furn.png (한 줄) + out/baby_furn.json (이름·크기·그림 위치·동물 자리 spot)
import json, math
from interiors import Room, hexc, shade, OUTL
from furniture import bx, C, ell, H
from PIL import Image, ImageDraw

def basin(R, img, d):        # 오리: 나무 물 대야
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 3, 11, 6, '#7A4A2E'); ell(d, x, y - 5, 11, 6, '#9A643E'); ell(d, x, y - 5, 9, 4.5, '#5AA8D8'); ell(d, x - 2, y - 6, 4, 1.5, '#9AD8F2')
    for k in (-7, 7): d.line([(x + k, y - 9), (x + k, y - 1)], fill=H('#6E4428'))
    d.line([(x + 8, y - 6), (x + 9, y - 13)], fill=H('#5E8A3E')); d.line([(x + 10, y - 5), (x + 11, y - 11)], fill=H('#5E8A3E')); ell(d, x + 9, y - 13, 1, 2, '#8A5A36')
def basket(R, img, d):       # 고양이: 털실 바구니
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 3, 10, 5.5, '#B07A40'); d.rectangle([x - 10, y - 8, x + 10, y - 3], fill=H('#B07A40'))
    for k in range(-9, 10, 3): d.line([(x + k, y - 8), (x + k, y - 1)], fill=H('#8A5A2E'))
    ell(d, x, y - 8, 10, 5, '#C88A4A'); ell(d, x, y - 8, 8, 3.8, '#D86A8A'); ell(d, x + 9, y - 1, 3, 3, '#7A9AE0'); d.arc([x + 6, y - 4, x + 12, y + 2], 200, 340, fill=H('#5A7AC0'))
def doghouse(R, img, d):     # 강아지: 빨간 지붕 개집
    x, y = C(R, 1.5, 1.5); d.polygon([(x - 10, y - 13), (x, y - 8), (x, y + 4), (x - 10, y - 1)], fill=H('#B8864E')); d.polygon([(x, y - 8), (x + 10, y - 13), (x + 10, y - 1), (x, y + 4)], fill=H('#D8A86A'))
    L, Rr, T = (x - 11, y - 13), (x + 11, y - 13), (x, y - 23); d.polygon([L, T, (x, y - 9)], fill=H('#C8443A')); d.polygon([Rr, T, (x, y - 9)], fill=H('#A8342C'))
    d.polygon([(x - 7, y - 7), (x - 3, y - 5), (x - 3, y + 1), (x - 7, y - 1)], fill=H('#3A2418')); ell(d, x + 8, y + 1, 3, 1.5, '#9AA4B4'); ell(d, x + 8, y, 2, .8, '#E8C27A')
def haymound(R, img, d):     # 토끼: 건초 굴
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 6, 11, 8, '#D8B860'); ell(d, x - 2, y - 9, 7, 5, '#E8CC7A')
    for k in (-8, -3, 2, 7): d.line([(x + k, y - 12), (x + k + 2, y - 4)], fill=H('#B8983E'))
    ell(d, x + 3, y - 3, 3.5, 3, '#4A3420'); d.polygon([(x - 9, y + 1), (x - 4, y - 1), (x - 8, y - 2)], fill=H('#F08A30')); d.line([(x - 9, y - 2), (x - 10, y - 4)], fill=H('#5E9A3E'))
def stump(R, img, d):        # 다람쥐: 도토리 그루터기
    bx(R, img, 1.2, 1.2, .6, .6, 9, '#8A5A36', top='#C89A6A'); x, y = C(R, 1.5, 1.5)
    ell(d, x, y - 10, 2.5, 1.2, '#A8744A'); ell(d, x + 1, y - 5, 2, 2.5, '#3A2418')
    for k, (dx, dy) in enumerate(((-9, 1), (-6, 3), (8, 2))): ell(d, x + dx, y + dy, 2, 2, '#B07838'); d.rectangle([x + dx - 2, y + dy - 3, x + dx + 2, y + dy - 2], fill=H('#6E4428'))
def leafbed(R, img, d):      # 고슴도치: 낙엽 이불
    x, y = C(R, 1.5, 1.5)
    for k, (dx, dy, c) in enumerate(((-6, -3, '#C8603A'), (5, -4, '#E0A040'), (0, -1, '#B84A2E'), (-2, -6, '#E8C060'), (7, 0, '#A86A30'), (-8, 1, '#D8803A'))): ell(d, x + dx, y + dy, 5, 2.5, c)
    ell(d, x + 10, y - 7, 2.5, 3, '#E8D8B8'); ell(d, x + 10, y - 9, 2.5, 1, '#C84A3A')     # 도토리 컵
def perch_bat(R, img, d):    # 박쥐: 거꾸로 매달리는 횃대
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 26, x + 1, y], fill=H('#6E4428')); d.rectangle([x - 9, y - 27, x + 9, y - 25], fill=H('#8A5A36')); ell(d, x, y, 6, 2.5, '#5E3826')
    ell(d, x + 7, y - 31, 2.5, 2.5, '#F2E2A0'); d.line([(x + 7, y - 27), (x + 7, y - 28)], fill=H('#6E4428'))
def perch_owl(R, img, d):    # 부엉이: 나뭇가지 횃대 + 둥지 상자
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 18, x + 1, y], fill=H('#6E4428')); d.line([(x - 9, y - 18), (x + 9, y - 19)], fill=H('#8A5A36'), width=2); ell(d, x, y, 6, 2.5, '#5E3826')
    d.rectangle([x + 4, y - 30, x + 12, y - 21], fill=H('#A8744A')); ell(d, x + 8, y - 26, 2, 2, '#3A2418'); d.polygon([(x + 3, y - 30), (x + 8, y - 34), (x + 13, y - 30)], fill=H('#5E8A3E')); d.line([(x - 6, y - 19), (x - 7, y - 21)], fill=H('#7AAA4E'))
def burrow(R, img, d):       # 여우: 담요 굴
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 7, 11, 9, '#8A6A4E'); ell(d, x, y - 9, 9, 7, '#A8866A'); ell(d, x, y - 3, 7, 4, '#3A2418'); ell(d, x - 3, y + 1, 8, 2.5, '#D86A4A'); d.line([(x - 10, y + 1), (x + 4, y + 1)], fill=H('#F2E2C4'))
def washlog(R, img, d):      # 너구리: 통나무 + 손 씻는 물그릇
    x, y = C(R, 1.5, 1.5); d.polygon([(x - 13, y - 6), (x + 1, y - 13), (x + 5, y - 7), (x - 9, y)], fill=H('#8A5A36')); d.line([(x - 12, y - 4), (x + 2, y - 11)], fill=H('#6E4428'))
    ell(d, x - 11, y - 3, 3, 3.5, '#C89A6A'); ell(d, x - 11, y - 3, 1.5, 2, '#A8744A'); d.line([(x - 4, y - 9), (x - 3, y - 13)], fill=H('#5E8A3E')); ell(d, x - 3, y - 13, 1.5, 1, '#7AAA4E')
    ell(d, x + 7, y + 1, 5, 2.5, '#9AA4B4'); ell(d, x + 7, y, 4, 1.6, '#5AA8D8')
def lilybowl(R, img, d):     # 개구리: 연잎 어항
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 7, 10, 9, '#BFE4F2'); ell(d, x, y - 4, 9, 5, '#5AA8D8'); ell(d, x, y - 6, 9, 3, '#7AC0E2'); ell(d, x - 1, y - 7, 5, 2, '#5E9A3E'); d.polygon([(x - 1, y - 7), (x + 3, y - 9), (x + 4, y - 7)], fill=H('#7AC0E2'))
    ell(d, x + 5, y - 8, 1.5, 1.5, '#F0A0C0'); d.point((x - 6, y - 12), fill=H('#FFFFFF'))
def strawnest(R, img, d):    # 병아리: 짚 둥지 + 따뜻한 등
    x, y = C(R, 1.5, 1.5); ell(d, x - 2, y - 2, 9, 4.5, '#C8A050'); ell(d, x - 2, y - 4, 7, 3, '#E8CC7A')
    for k in (-9, -5, 1, 5): d.line([(x + k, y - 5), (x + k + 3, y - 1)], fill=H('#B08838'))
    d.rectangle([x + 8, y - 22, x + 9, y + 1], fill=H('#3A3448')); d.line([(x + 9, y - 22), (x + 4, y - 20)], fill=H('#3A3448')); d.polygon([(x + 1, y - 20), (x + 7, y - 20), (x + 6, y - 16), (x + 2, y - 16)], fill=H('#F0B040')); ell(d, x + 4, y - 15, 2, 1, '#FFE08A')


# ---------- 동물마다 두 개 더: 밥그릇 + 놀이·쉼 가구 ----------
def bowl(col, food):
    def f(R, img, d):
        x, y = C(R, 1.5, 1.5); x += 5; ell(d, x, y - 1, 7, 3.5, shade(H(col), .7)); d.rectangle([x - 7, y - 4, x + 7, y - 1], fill=H(col)); ell(d, x, y - 4, 7, 3.5, shade(H(col), 1.15)); ell(d, x, y - 4, 5.5, 2.5, '#3A2A30'); food(d, x, y - 4)
    return f
def f_grain(d, x, y): [d.point((x + dx, y + dy), fill=H(c)) for dx, dy, c in ((-3, 0, '#E8D070'), (-1, -1, '#F2E08A'), (1, 0, '#E8D070'), (3, -1, '#D8C060'), (0, 1, '#F2E08A'), (2, 1, '#E8D070'), (-2, 1, '#D8C060'))]
def f_milk(d, x, y): ell(d, x, y, 5, 2, '#FAF6EE')
def f_bone(d, x, y): d.line([(x - 3, y), (x + 3, y)], fill=H('#F2EAD8'), width=2); [ell(d, x + k, y + j, 1, 1, '#F2EAD8') for k in (-4, 4) for j in (-1, 1)]
def f_carrot(d, x, y): d.polygon([(x - 4, y + 1), (x + 3, y - 1), (x + 2, y + 1)], fill=H('#F08A30')); d.line([(x + 3, y - 1), (x + 5, y - 3)], fill=H('#5E9A3E'))
def f_acorn(d, x, y): [(ell(d, x + k, y, 1.5, 1.5, '#B07838'), d.line([(x + k - 1, y - 1), (x + k + 1, y - 1)], fill=H('#6E4428'))) for k in (-3, 0, 3)]
def f_berry(d, x, y): [ell(d, x + k, y + j, 1.3, 1.3, '#D83A5A') for k, j in ((-3, 0), (0, -1), (3, 0), (-1, 1), (2, 1))]
def f_fruit(d, x, y): ell(d, x - 2, y, 2, 1.8, '#E85A4A'); ell(d, x + 2, y, 2, 1.8, '#F0B040'); d.point((x, y - 2), fill=H('#5E9A3E'))
def f_fish(d, x, y): d.polygon([(x - 4, y), (x + 2, y - 1), (x + 2, y + 1)], fill=H('#9AB4D0')); d.polygon([(x + 2, y), (x + 5, y - 2), (x + 5, y + 2)], fill=H('#7A94B0'))
def f_egg(d, x, y): ell(d, x - 2, y, 2, 1.6, '#FAF2E0'); ell(d, x + 2, y, 2, 1.6, '#F2E2C4')
def f_bug(d, x, y): ell(d, x, y, 2, 1.6, '#D83A3A'); d.point((x - 1, y - 1), fill=H('#2A1830')); d.point((x + 1, y), fill=H('#2A1830'))
def f_seed(d, x, y): [d.point((x + dx, y + dy), fill=H(c)) for dx, dy, c in ((-3, 0, '#F2E2A0'), (-1, -1, '#E8C870'), (1, 0, '#F2E2A0'), (3, -1, '#E8C870'), (0, 1, '#D8B060'), (2, 1, '#F2E2A0'))]

def reednest(R, img, d):     # 오리: 갈대 둥지
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 2, 10, 5, '#8A7A4A'); ell(d, x, y - 4, 8, 3.5, '#B8A86A'); ell(d, x, y - 4, 6, 2.2, '#6E5E38')
    for k in (-9, -6, 7, 10): d.line([(x + k, y - 3), (x + k + (1 if k > 0 else -1), y - 15)], fill=H('#7A9A4E')); ell(d, x + k + (1 if k > 0 else -1), y - 15, 1, 2, '#8A5A36')
def scratcher(R, img, d):    # 고양이: 스크래처 기둥
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 1, 9, 4.5, '#C86A8A'); d.rectangle([x - 2, y - 22, x + 2, y - 2], fill=H('#D8B47A'))
    for k in range(-20, -2, 3): d.line([(x - 2, y + k), (x + 2, y + k + 1)], fill=H('#B08A50'))
    ell(d, x, y - 22, 6, 3, '#C86A8A'); d.line([(x + 4, y - 21), (x + 7, y - 14)], fill=H('#F2E2A0')); ell(d, x + 7, y - 13, 1.5, 1.5, '#F0B040')
def dogbed(R, img, d):       # 강아지: 방석 + 공
    x, y = C(R, 1.5, 1.5); ell(d, x - 1, y - 2, 11, 5.5, '#4A7AB8'); ell(d, x - 1, y - 3, 9, 4, '#6A9AD8'); ell(d, x - 1, y - 3, 6, 2.5, '#E8D8B8'); ell(d, x + 10, y + 1, 2.5, 2.5, '#E85A4A'); d.line([(x + 8, y + 1), (x + 12, y + 1)], fill=H('#FAF2E0'))
def logtunnel(R, img, d):    # 토끼: 통나무 굴
    x, y = C(R, 1.5, 1.5); d.polygon([(x - 12, y - 4), (x + 4, y - 12), (x + 9, y - 5), (x - 7, y + 3)], fill=H('#9A6A3E')); ell(d, x - 10, y, 4.5, 5, '#C89A6A'); ell(d, x - 10, y, 3, 3.6, '#3A2418'); d.line([(x - 6, y - 6), (x + 5, y - 11)], fill=H('#7A4A2E')); ell(d, x + 2, y - 10, 2, 1, '#7AAA4E')
def wheel(R, img, d):        # 다람쥐: 쳇바퀴
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 1, y - 9, x + 1, y], fill=H('#6E4428')); ell(d, x, y, 6, 2.5, '#5E3826')
    d.ellipse([x - 10, y - 21, x + 10, y - 1], outline=H('#B07838'), width=2); d.ellipse([x - 7, y - 18, x + 7, y - 4], outline=H('#D8A86A'))
    for a in range(0, 360, 45): t = math.radians(a); d.line([(x, y - 11), (x + math.cos(t) * 9, y - 11 + math.sin(t) * 9)], fill=H('#8A5A36'))
def mushhouse(R, img, d):    # 고슴도치: 버섯 집
    x, y = C(R, 1.5, 1.5); d.rectangle([x - 5, y - 10, x + 5, y], fill=H('#F2E2C4')); ell(d, x, y, 5, 2, '#E8D2A8'); d.rectangle([x - 2, y - 6, x + 1, y], fill=H('#6E4428'))
    ell(d, x, y - 12, 11, 6, '#D83A3A'); d.rectangle([x - 11, y - 12, x + 11, y - 10], fill=H('#B82A2A')); [ell(d, x + k, y - 14 + j, 1.5, 1, '#FAF2E0') for k, j in ((-6, 0), (0, -3), (5, 0), (-2, 2))]
def moonmobile(R, img, d):   # 박쥐: 달 모빌 (매달려요)
    x, y = C(R, 1.5, 1.5); ell(d, x, y, 6, 2.5, '#5E3826'); d.rectangle([x + 8, y - 30, x + 9, y], fill=H('#6E4428')); d.rectangle([x - 8, y - 31, x + 9, y - 30], fill=H('#6E4428'))
    d.line([(x - 6, y - 30), (x - 6, y - 25)], fill=H('#C8B890')); ell(d, x - 6, y - 21, 4, 4, '#F2E08A'); ell(d, x - 4, y - 22, 3.5, 3.5, (0, 0, 0, 0)); d.line([(x + 3, y - 30), (x + 3, y - 22)], fill=H('#C8B890')); d.polygon([(x + 3, y - 22), (x + 5, y - 19), (x + 3, y - 16), (x + 1, y - 19)], fill=H('#F2E08A'))
def bookstack(R, img, d):    # 부엉이: 책 더미
    x, y = C(R, 1.5, 1.5)
    for k, (c, dx) in enumerate((('#7A4AA8', 0), ('#3A7A6A', 1), ('#C8603A', -1), ('#3A5AA8', 0))): bx(R, img, 1.2 + dx * .04, 1.25, .6, .5, 3, c, lift=k * 3)
    d.line([(x + 7, y - 10), (x + 9, y - 6)], fill=H('#F2E2A0'))
def leafcushion(R, img, d):  # 여우: 단풍 방석
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 2, 11, 5.5, '#B84A2E'); ell(d, x, y - 3, 9, 4, '#D8703A')
    for k, (dx, dy) in enumerate(((-5, -3), (4, -4), (0, -2), (6, -1), (-7, -1))): d.polygon([(x + dx, y + dy - 2), (x + dx + 2, y + dy), (x + dx, y + dy + 1), (x + dx - 2, y + dy)], fill=H(('#F0B040', '#E8603A', '#F2D060')[k % 3]))
def treasure(R, img, d):     # 너구리: 반짝이 보물 상자
    bx(R, img, 1.2, 1.25, .6, .5, 6, '#9A643E'); x, y = C(R, 1.5, 1.5); d.polygon([(x - 5, y - 8), (x + 5, y - 10), (x + 5, y - 15), (x - 5, y - 13)], fill=H('#B07840')); d.rectangle([x - 1, y - 7, x + 1, y - 5], fill=H('#F0C040'))
    for dx, dy, c in ((-2, -9, '#F2E08A'), (1, -10, '#9AD8F2'), (3, -9, '#F0A0C0'), (8, 0, '#F2E08A'), (-9, 1, '#9AD8F2')): d.point((x + dx, y + dy), fill=H(c))
def mushstool(R, img, d):    # 개구리: 버섯 의자 + 연잎
    x, y = C(R, 1.5, 1.5); ell(d, x - 3, y + 1, 8, 3, '#5E9A3E'); d.polygon([(x - 3, y + 1), (x + 2, y - 1), (x + 3, y + 1)], fill=H('#4A7A2E'))
    d.rectangle([x + 2, y - 8, x + 5, y], fill=H('#F2E2C4')); ell(d, x + 3.5, y - 9, 6, 3, '#E8A040'); ell(d, x + 3.5, y - 10, 6, 2.5, '#F2C060'); d.point((x + 1, y - 11), fill=H('#FAF2E0')); d.point((x + 6, y - 10), fill=H('#FAF2E0'))
def eggbed(R, img, d):       # 병아리: 달걀 껍질 침대
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 3, 9, 6, '#FAF2E0'); d.rectangle([x - 9, y - 9, x + 9, y - 4], fill=(0, 0, 0, 0))
    d.polygon([(x - 9, y - 4), (x - 7, y - 7), (x - 4, y - 4), (x - 1, y - 7), (x + 2, y - 4), (x + 5, y - 7), (x + 7, y - 4), (x + 9, y - 4), (x + 9, y - 2), (x - 9, y - 2)], fill=H('#FAF2E0')); ell(d, x, y - 4, 7, 2.5, '#F0D070')

# id, 이름, 그림, 동물 자리(기준 칸 꼭짓점에서 px), 동물 모습(normal·float·flip·peek)
ITEMS = [
  ('bf_duck', '오리 물 대야', basin, (0, -6), 'float'), ('bf_cat', '고양이 털실 바구니', basket, (0, -9), 'normal'), ('bf_dog', '강아지 개집', doghouse, (-6, 3), 'normal'),
  ('bf_rabbit', '토끼 건초 굴', haymound, (3, -2), 'peek'), ('bf_squirrel', '다람쥐 그루터기', stump, (0, -14), 'normal'), ('bf_hedgehog', '고슴도치 낙엽 이불', leafbed, (0, -3), 'normal'),
  ('bf_bat', '박쥐 횃대', perch_bat, (-5, -25), 'flip'), ('bf_owl', '부엉이 횃대', perch_owl, (-3, -19), 'normal'), ('bf_fox', '여우 담요 굴', burrow, (0, -2), 'normal'),
  ('bf_raccoon', '너구리 통나무', washlog, (6, -1), 'normal'), ('bf_frog', '개구리 연잎 어항', lilybowl, (-1, -7), 'normal'), ('bf_chick', '병아리 짚 둥지', strawnest, (-2, -4), 'normal')]

ITEMS += [
  ('bf_duck2', '오리 모이 그릇', bowl('#7A9AC8', f_grain), (-5, 0), 'normal'), ('bf_duck3', '오리 갈대 둥지', reednest, (0, -4), 'normal'),
  ('bf_cat2', '고양이 우유 접시', bowl('#E890A8', f_milk), (-5, 0), 'normal'), ('bf_cat3', '고양이 스크래처', scratcher, (0, -24), 'normal'),
  ('bf_dog2', '강아지 뼈다귀 그릇', bowl('#C84A3A', f_bone), (-5, 0), 'normal'), ('bf_dog3', '강아지 방석', dogbed, (-1, -3), 'normal'),
  ('bf_rabbit2', '토끼 당근 그릇', bowl('#E8B060', f_carrot), (-5, 0), 'normal'), ('bf_rabbit3', '토끼 통나무 굴', logtunnel, (-10, 1), 'peek'),
  ('bf_squirrel2', '다람쥐 도토리 접시', bowl('#9A7A5A', f_acorn), (-5, 0), 'normal'), ('bf_squirrel3', '다람쥐 쳇바퀴', wheel, (0, -4), 'normal'),
  ('bf_hedgehog2', '고슴도치 산딸기 그릇', bowl('#7AAA6A', f_berry), (-5, 0), 'normal'), ('bf_hedgehog3', '고슴도치 버섯 집', mushhouse, (-6, 2), 'normal'),
  ('bf_bat2', '박쥐 과일 접시', bowl('#8A6AB8', f_fruit), (-5, 0), 'normal'), ('bf_bat3', '박쥐 달 모빌', moonmobile, (0, -30), 'flip'),
  ('bf_owl2', '부엉이 물고기 접시', bowl('#6A8AB8', f_fish), (-5, 0), 'normal'), ('bf_owl3', '부엉이 책 더미', bookstack, (0, -15), 'normal'),
  ('bf_fox2', '여우 달걀 그릇', bowl('#E07A40', f_egg), (-5, 0), 'normal'), ('bf_fox3', '여우 단풍 방석', leafcushion, (0, -3), 'normal'),
  ('bf_raccoon2', '너구리 생선 접시', bowl('#8A9AA8', f_fish), (-5, 0), 'normal'), ('bf_raccoon3', '너구리 보물 상자', treasure, (-8, 2), 'normal'),
  ('bf_frog2', '개구리 무당벌레 접시', bowl('#5EAA7A', f_bug), (-5, 0), 'normal'), ('bf_frog3', '개구리 버섯 의자', mushstool, (3, -11), 'normal'),
  ('bf_chick2', '병아리 모이통', bowl('#E8C050', f_seed), (-5, 0), 'normal'), ('bf_chick3', '병아리 달걀 껍질 침대', eggbed, (0, -4), 'normal')]

PRICE = {'bf_duck': 180, 'bf_cat': 160, 'bf_dog': 260, 'bf_rabbit': 170, 'bf_squirrel': 150, 'bf_hedgehog': 120, 'bf_bat': 160, 'bf_owl': 200, 'bf_fox': 200, 'bf_raccoon': 150, 'bf_frog': 220, 'bf_chick': 170, 'bf_duck3': 140, 'bf_cat3': 220, 'bf_dog3': 150, 'bf_rabbit3': 190, 'bf_squirrel3': 240, 'bf_hedgehog3': 230, 'bf_bat3': 210, 'bf_owl3': 180, 'bf_fox3': 140, 'bf_raccoon3': 250, 'bf_frog3': 160, 'bf_chick3': 150}   # 밥그릇(…2)은 모두 60G

def main():
    sprites, meta = [], []
    for k, (fid, name, draw, spot, pose) in enumerate(ITEMS):
        R = Room(6, 6, 60); R.obj(fid, [(1, 1)], lambda img, d, draw=draw: draw(R, img, d))
        o = R.objs[-1]; ax, ay = R.P(1, 1)   # 놓은 칸의 위 꼭짓점 (spot은 칸 가운데 기준)
        sprites.append(o['img']); meta.append(dict(id=fid, name=name, cat='아기 동물', price=PRICE.get(fid, 60), pts=2, w=1, d=1, solid=1, flat=0, sw=o['img'].width, sh=o['img'].height, ax=round(ax - o['x']), ay=round(ay - o['y']), baby=k if k < 12 else (k - 12) // 2, spot=list(spot), pose=pose))
    W = sum(s.width + 1 for s in sprites); Hh = max(s.height for s in sprites)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
    for s, m in zip(sprites, meta): sheet.paste(s, (x, Hh - s.height)); m['sx'] = x; m['ay'] += Hh - s.height; m['sh'] = Hh; x += s.width + 1
    sheet.save('out/baby_furn.png'); json.dump(meta, open('out/baby_furn.json', 'w'), ensure_ascii=False)
    print('baby furn', len(meta), sheet.size)
if __name__ == '__main__': main()
