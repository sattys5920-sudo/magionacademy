# 소환수 14종 → public/art/pets.png (64칸, 왼쪽(적 쪽)을 보고 서 있는 모습)
#   정령 동물 10: 몸은 네발·날개 달린 동물로 직접 그리고(beasts.py와 같은 6단계 음영·색 외곽선), 얼굴은 LPC 동물 머리를 붙여요. 속성 색 빛·반투명
#   기공사 소환수 4(번개 쥐·수호 쥐·광선 도마뱀·철갑 멧돼지)도 같은 방식
#   python3 pet_lpc.py <LPC 저장소 경로> [미리보기.png]   순서는 index.html의 XPETI와 같아요
import sys, os, subprocess
sys.argv = sys.argv[:3]
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from npc_lpc import find, recolor, over, LPC, ROWS, FILES
import beasts
from beasts import Sprite, RAMP, px, hx
ROOT = os.path.join(HERE, '..', '..', '..')
def ramp(c):   # 기준색 하나로 6단계(외곽선 → 밝은색)
    r = hx(c); f = lambda k: '#%02X%02X%02X' % tuple(max(0, min(255, int(v * k + (255 * (k - 1) * .25 if k > 1 else 0)))) for v in r)
    return [f(.28), f(.5), f(.75), f(1), f(1.22), f(1.5)]
for n, c in {'wolfg': '#8A8F9C', 'wolfo': '#E8782E', 'wolfw': '#E8ECF4', 'rabb': '#7AB8F0', 'rabo': '#F0902E', 'wool': '#F2F4FA', 'boar': '#8A6A48', 'bear': '#7A5230', 'eagle': '#B89868', 'feather': '#E8E0C0', 'drag': '#4A78C8', 'wing': '#C84A3A', 'steel': '#8C96A6', 'steel2': '#5C6676', 'lens': '#FF5AA0', 'dome': '#5AD0FF', 'ember': '#FF6A3A'}.items(): RAMP[n] = ramp(c)
def head(name, skin, ax, ay, sc=1.0):   # LPC 동물 머리(왼쪽을 봄)를 따서 (ax, ay)가 머리 가운데가 되게 붙일 그림을 돌려줘요
    f = find('head/heads/' + name, None, 'child'); need = os.path.join(LPC, f)
    if not os.path.exists(need): subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', f], check=True)
    a = np.array(Image.open(need).convert('RGBA')); y = ROWS['left'] * 64; cell = a[y:y + 64, 0:64]
    if skin: cell = recolor(cell, ('body', 'auto', skin))
    ys, xs = np.nonzero(cell[..., 3] > 0); crop = cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(crop)
    if sc != 1: im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.NEAREST)
    out = np.zeros((64, 64, 4), np.uint8); h, w = im.height, im.width; x0, y0 = ax - w // 2, ay - h // 2; arr = np.array(im)
    for yy in range(h):
        for xx in range(w):
            if 0 <= y0 + yy < 64 and 0 <= x0 + xx < 64 and arr[yy, xx, 3]: out[y0 + yy, x0 + xx] = arr[yy, xx]
    return out
def legs(S, r, xs, y0=48, y1=62, light=-.08, w=5):
    for x in xs: S.add(r, lambda d, x=x: d.rectangle([x, y0, x + w, y1]), light)
def wolf(r, hd, skin, crown=False):
    S = Sprite(); S.add(r, lambda d: [d.ellipse([44, 30, 60, 48]), d.polygon([(46, 40), (62, 34), (58, 50)])], .08)
    S.add(r, lambda d: d.ellipse([14, 34, 49, 55])); legs(S, r, [17, 25, 36, 44]); S.add(r, lambda d: d.ellipse([20, 38, 36, 52]), .12)
    a = S.render(); over(a, head(hd, skin, 14, 34)); return a
def rabbit(r, hd, skin, tail='#FFFFFF'):
    S = Sprite(); S.add(r, lambda d: d.ellipse([22, 32, 48, 61])); S.add(r, lambda d: d.ellipse([34, 48, 54, 62]), -.08); S.add(r, lambda d: d.ellipse([18, 53, 28, 63]), .05)
    S.add('white', lambda d: d.ellipse([46, 44, 56, 54]), .15); a = S.render(); over(a, head(hd, skin, 22, 28, 1.1)); return a
def sheep(r, hd, skin):
    S = Sprite(); S.add('dark', lambda d: legs_d(d)); [S.add(r, lambda d, b=b: d.ellipse(b), .05 * i) for i, b in enumerate([[14, 30, 34, 52], [26, 26, 46, 50], [34, 32, 54, 54], [22, 38, 44, 58]])]
    a = S.render(); over(a, head(hd, skin, 13, 40)); return a
def legs_d(d): d.rectangle([20, 52, 24, 62]); d.rectangle([40, 52, 44, 62])
def boar(r, hd, skin):
    S = Sprite(); S.add(r, lambda d: d.ellipse([14, 32, 50, 55])); legs(S, r, [18, 26, 36, 44], 50, 62); S.add(r, lambda d: [d.ellipse([48, 36, 58, 44]), d.rectangle([54, 38, 58, 41])], .0); S.add('dark', lambda d: d.polygon([(30, 32), (34, 26), (38, 32)]), .0)
    a = S.render(); over(a, head(hd, skin, 13, 40)); return a
def bear(r, hd, skin):
    S = Sprite(); S.add(r, lambda d: d.ellipse([14, 28, 53, 57])); legs(S, r, [16, 25, 37, 46], 50, 62, w=7); S.add(r, lambda d: d.ellipse([46, 38, 58, 50]), .08)
    a = S.render(); over(a, head(hd, skin, 15, 34, 1.15)); return a
def eagle(r, hd, skin):
    S = Sprite(); S.add('feather', lambda d: d.polygon([(42, 44), (58, 60), (46, 58)]), -.05); S.add(r, lambda d: d.ellipse([20, 24, 45, 52]))
    S.add('feather', lambda d: d.ellipse([26, 28, 52, 50]), -.05); S.add('feather', lambda d: d.ellipse([28, 30, 56, 40]), .1); S.add('yellow', lambda d: [d.rectangle([28, 50, 30, 60]), d.rectangle([36, 50, 38, 60]), d.rectangle([24, 59, 31, 61]), d.rectangle([32, 59, 39, 61])])
    S.add('white', lambda d: d.ellipse([14, 14, 30, 30]), .12); S.add('yellow', lambda d: d.polygon([(15, 21), (5, 25), (15, 28)]), .1)
    a = S.render(); px(a, [(19, 21), (20, 21)], '#1A1020'); return a
def dragon(r, hd, skin):
    S = Sprite(); S.add('wing', lambda d: [d.polygon([(34, 36), (48, 8), (56, 30)]), d.polygon([(38, 38), (60, 24), (58, 42)])], -.05); S.add(r, lambda d: [d.ellipse([46, 42, 62, 52]), d.polygon([(46, 44), (62, 56), (50, 52)])], .05)
    S.add(r, lambda d: d.ellipse([18, 32, 48, 54])); legs(S, r, [22, 36], 50, 62, w=6); S.add('yellow', lambda d: d.ellipse([22, 38, 38, 52]), .1)
    a = S.render(); over(a, head(hd, skin, 16, 32)); return a
def crown_px(a, x, y):
    px(a, [(x + i, y + 4) for i in range(8)] + [(x, y + 3), (x, y + 2), (x + 3, y + 3), (x + 3, y + 1), (x + 7, y + 3), (x + 7, y + 2)], '#FFD84A')
def rodent(r, hd, skin, tail='#E8A8B8'):   # 쥐: 작은 네발 몸 + 가는 꼬리
    S = Sprite(); S.add('rabo' if False else r, lambda d: [d.line([(46, 52), (56, 46), (62, 50)], width=2)], -.1); S.add(r, lambda d: d.ellipse([16, 38, 48, 58])); legs(S, r, [20, 28, 36, 42], 54, 62, w=4); S.add(r, lambda d: d.ellipse([20, 42, 36, 56]), .12)
    a = S.render(); over(a, head(hd, skin, 15, 42, 1.0)); return a
def lizard(r, hd, skin):   # 도마뱀: 길쭉한 네발 몸 + 긴 꼬리
    S = Sprite(); S.add(r, lambda d: [d.polygon([(44, 44), (62, 56), (50, 54)]), d.ellipse([40, 42, 56, 52])], .05); S.add(r, lambda d: d.ellipse([14, 38, 48, 56])); legs(S, r, [18, 26, 36, 43], 52, 62, w=4); S.add('yellow', lambda d: d.ellipse([20, 44, 38, 55]), .12)
    a = S.render(); over(a, head(hd, skin, 14, 40)); return a
def armor_boar(r, hd, skin):   # 철갑 멧돼지: 멧돼지 + 철판
    a = boar(r, hd, skin); S = Sprite(); S.add('steel', lambda d: [d.rectangle([22, 32, 42, 38]), d.rectangle([28, 34, 36, 44])], .1); over(a, S.render()); return a
# 포탑 4종 (기계: 받침·몸통·포신·렌즈) — 지금은 쓰지 않아요

def turret_s():
    S = Sprite(); S.add('steel2', lambda d: [d.polygon([(18, 62), (24, 44), (40, 44), (46, 62)]), d.rectangle([28, 40, 36, 52])]); S.add('steel', lambda d: d.rectangle([14, 30, 44, 44])); S.add('steel2', lambda d: d.rectangle([4, 34, 18, 39]), -.05)
    S.add('steel', lambda d: d.rectangle([2, 33, 8, 40]), .1); S.add('ember', lambda d: d.ellipse([34, 33, 41, 40]), .15); a = S.render(); px(a, [(5, 36), (6, 36)], '#1A1020'); return a
def turret_h():
    S = Sprite(); S.add('steel2', lambda d: d.rectangle([14, 52, 50, 62])); S.add('steel', lambda d: d.rectangle([20, 44, 44, 54])); S.add('dome', lambda d: d.ellipse([16, 22, 48, 54]), .1); S.add('steel2', lambda d: d.rectangle([30, 8, 33, 26]))
    S.add('ember', lambda d: d.ellipse([28, 5, 36, 13]), .2); S.add('white', lambda d: d.ellipse([22, 28, 30, 36]), .3); return S.render()
def turret_l():
    S = Sprite(); S.add('steel2', lambda d: [d.rectangle([24, 44, 40, 62]), d.rectangle([16, 56, 48, 62])]); S.add('steel', lambda d: [d.polygon([(10, 36), (26, 30), (26, 50), (10, 44)]), d.rectangle([24, 30, 44, 50])])
    S.add('lens', lambda d: d.ellipse([4, 34, 16, 46]), .2); S.add('steel2', lambda d: [d.polygon([(40, 30), (52, 22), (52, 34)]), d.polygon([(40, 50), (52, 58), (52, 46)])]); S.add('white', lambda d: d.ellipse([7, 37, 11, 41]), .4); return S.render()
def turret_f():
    S = Sprite(); S.add('steel2', lambda d: [d.rectangle([8, 54, 58, 62]), d.polygon([(14, 54), (22, 40), (50, 40), (56, 54)])]); S.add('steel', lambda d: d.rectangle([20, 26, 50, 44])); S.add('steel2', lambda d: d.rectangle([0, 28, 24, 40]), -.05)
    S.add('steel', lambda d: d.rectangle([0, 25, 8, 43]), .1); S.add('ember', lambda d: [d.ellipse([30, 30, 38, 38]), d.rectangle([40, 30, 48, 33])], .1); S.add('steel', lambda d: d.rectangle([22, 18, 34, 28]), .05); return S.render()
PETS = [  # 이름, 그리는 함수, 빛 색(없으면 기계), 투명도
 ('불 정령', lambda: wolf('wolfo', 'wolf/child', 'fur_copper'), (255, 110, 50), .88), ('물 정령', lambda: rabbit('rabb', 'rabbit/child', 'blue'), (90, 210, 255), .86),
 ('바람 정령', lambda: sheep('wool', 'sheep/child', 'fur_white'), (225, 240, 255), .8), ('대지 정령', lambda: boar('boar', 'boarman/child', 'fur_brown'), (200, 160, 90), .9),
 ('정령왕', lambda: (lambda a: (crown_px(a, 6, 14), a)[1])(wolf('wolfw', 'wolf/child', 'fur_white')), (255, 214, 90), .9), ('늑대', lambda: wolf('wolfg', 'wolf/child', 'fur_grey'), (200, 215, 255), .9),
 ('곰', lambda: bear('bear', 'minotaur/child', 'fur_brown'), (170, 115, 70), .92), ('독수리', lambda: eagle('eagle', None, None), (240, 232, 190), .9),
 ('호박 유령', lambda: rabbit('rabo', 'rabbit/child', 'fur_copper'), (255, 150, 40), .6), ('용', lambda: dragon('drag', 'lizard/child', 'blue'), (255, 80, 60), .9),
 ('번개 쥐', lambda: rodent('wolfg', 'mouse/child', 'fur_grey'), (90, 230, 255), .88), ('수호 쥐', lambda: rodent('boar', 'rat/child', 'fur_black'), (120, 255, 150), .88),
 ('광선 도마뱀', lambda: lizard('drag', 'lizard/child', 'bright_green'), (255, 100, 170), .88), ('철갑 멧돼지', lambda: armor_boar('wolfg', 'boarman/child', 'fur_grey'), (170, 190, 210), .9)]
def dil(m):
    d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]; return d
sheet = np.zeros((64, 64 * len(PETS), 4), np.uint8)
for i, (name, fn, glow, al) in enumerate(PETS):
    cell = fn()
    if glow:
        m = cell[..., 3] > 0; r1 = dil(m) & ~m; r2 = dil(m | r1) & ~(m | r1)
        cell[..., :3] = (cell[..., :3] * .82 + np.array(glow) * .18).astype(np.uint8); cell[..., 3] = (cell[..., 3] * al).astype(np.uint8); cell[r1] = (*glow, 190); cell[r2] = (*glow, 70)
    sheet[:, i * 64:(i + 1) * 64] = cell
Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'pets.png'))
if len(sys.argv) > 2:
    pv = Image.new('RGBA', (64 * len(PETS), 64), (60, 70, 90, 255)); pv.alpha_composite(Image.fromarray(sheet), (0, 0)); pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(sys.argv[2])
print('ok')
