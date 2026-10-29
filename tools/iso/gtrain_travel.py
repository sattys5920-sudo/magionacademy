# 유령 열차 이동 연출 시안 (8초): 열차가 몽환적인 곳 네 군데를 지나가요 → out/gtrain_travel.gif
#   별빛 강(0~2초) · 등불 구름(2~4초) · 거대한 달과 떠 있는 섬(4~6초) · 오로라(6~8초)
#   열차는 가운데에 떠 있고(살짝 출렁), 배경이 뒤쪽(오른쪽 위)으로 흘러가요. 게임에 넣을 때는 같은 그림을 캔버스로 그려요
import math, os, random
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SW, SH = 200, 260               # 1배 크기 (게임 화면 비율)
FPS, SEC = 12, 8
N = FPS * SEC
K = 3                           # 확대
TRAIN = Image.open('out/gtrain_train_in.png').convert('RGBA')
FONT = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 15 * K // 2)
rnd = random.Random(7)
STARS = [(rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.choice([1, 1, 1, 2]), rnd.uniform(.3, 1)) for _ in range(140)]
LANT = [(rnd.uniform(-.2, 1.2), rnd.uniform(0, 1.2), rnd.uniform(.6, 1.4)) for _ in range(26)]
ISLE = [(rnd.uniform(0, 1.3), rnd.uniform(.1, .9), rnd.uniform(.7, 1.3)) for _ in range(6)]
DIR = (2.0, -1.0)               # 배경이 흘러가는 방향 (오른쪽 위 = 아이소 뒤쪽)


def seg_alpha(t, a, b, fade=.45):
    if t < a - fade or t > b + fade: return 0.0
    if t < a: return (t - (a - fade)) / fade
    if t > b: return 1 - (t - b) / fade
    return 1.0


def flow(x, y, t, speed, wrapw=1.0, wraph=1.0):
    nx = (x + DIR[0] * speed * t / 100) % wrapw
    ny = (y + DIR[1] * speed * t / 100) % wraph
    return nx, ny


def frame(i):
    t = i / FPS
    img = Image.new('RGB', (SW, SH), (16, 11, 34)); d = ImageDraw.Draw(img, 'RGBA')   # RGB 바탕이어야 반투명이 섞여요
    # 하늘 띠 (도트 느낌으로 몇 줄만)
    for k, c in enumerate([(20, 14, 42), (24, 17, 50), (28, 20, 58), (32, 22, 66)]):
        d.rectangle([0, SH * k / 4 + SH * .1, SW, SH], fill=c + (255,))
    # 별 (먼 층, 느리게)
    for (x, y, s, b) in STARS:
        nx, ny = flow(x, y, t, 1.2)
        tw = .6 + .4 * math.sin(t * 3 + x * 40)
        c = (int(230 * b * tw), int(230 * b * tw), 255, 255)
        X, Y = int(nx * SW), int(ny * SH)
        d.rectangle([X, Y, X + s - 1, Y + s - 1], fill=c)
    # 1 별빛 강: 아래쪽에 흐르는 빛의 강
    a1 = seg_alpha(t, 0, 2)
    if a1:
        for k in range(60):
            x0 = ((k * 37) % 200) / 200; y0 = ((k * 53) % 100) / 100
            nx, ny = flow(x0, y0, t, 9)
            px, py = nx * SW * 1.2 - 20, SH * .62 + ny * SH * .3 - nx * SW * .25
            d.rectangle([px, py, px + 2 + k % 3, py], fill=(122, 224, 224, int(200 * a1)))
        d.polygon([(0, SH * .74), (SW, SH * .52), (SW, SH * .62), (0, SH * .86)], fill=(60, 120, 150, int(70 * a1)))
    # 2 등불 구름: 떠오르는 주황 등불 (가까운 건 크고 빠르게)
    a2 = seg_alpha(t, 2, 4)
    if a2:
        for (x, y, s) in LANT:
            nx, ny = flow(x, y, t - 2, 14 * s, 1.4, 1.3)
            px, py = nx * SW - 20, ny * SH - 20
            r = 2 + s * 2
            d.ellipse([px - r * 3, py - r * 3, px + r * 3, py + r * 3], fill=(255, 160, 70, int(30 * a2)))
            d.rectangle([px - r, py - r * 1.4, px + r, py + r], fill=(255, 154, 58, int(255 * a2)))
            d.rectangle([px - r + 1, py - r * 1.4 + 1, px + r - 1, py - r * .2], fill=(255, 224, 138, int(255 * a2)))
    # 3 거대한 달 + 떠 있는 섬
    a3 = seg_alpha(t, 4, 6)
    if a3:
        mx, my = SW * .62 - (t - 4) * 4, SH * .26 + (t - 4) * 2
        for rr, al in ((52, 30), (44, 60)):
            d.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=(255, 216, 102, int(al * a3)))
        d.ellipse([mx - 38, my - 38, mx + 38, my + 38], fill=(255, 230, 150, int(255 * a3)))
        d.ellipse([mx - 20, my - 14, mx - 8, my - 4], fill=(232, 200, 120, int(255 * a3)))
        d.ellipse([mx + 6, my + 8, mx + 20, my + 18], fill=(232, 200, 120, int(255 * a3)))
        for (x, y, s) in ISLE:
            nx, ny = flow(x, y, t - 4, 7 * s, 1.4, 1.0)
            px, py = nx * SW - 30, ny * SH
            w = 12 * s
            d.polygon([(px - w, py), (px + w, py), (px, py + w * 1.1)], fill=(42, 30, 70, int(255 * a3)))
            d.rectangle([px - w, py - 2, px + w, py], fill=(62, 78, 58, int(255 * a3)))
            d.rectangle([px - 1, py - 8 * s, px, py - 2], fill=(58, 42, 36, int(255 * a3)))
            d.ellipse([px - 4 * s, py - 13 * s, px + 4 * s, py - 6 * s], fill=(46, 62, 54, int(255 * a3)))
    # 4 오로라: 물결치는 빛의 띠
    a4 = seg_alpha(t, 6, 8.5)
    if a4:
        for band, (col, yb, amp) in enumerate([((111, 230, 170), .18, 10), ((176, 132, 255), .28, 14), ((122, 224, 224), .36, 8)]):
            for x in range(0, SW, 2):
                y = SH * yb + math.sin(x / 18 + t * 2 + band) * amp
                d.rectangle([x, y, x + 1, y + 26], fill=col + (int(46 * a4),))
                d.rectangle([x, y, x + 1, y + 3], fill=col + (int(140 * a4),))
    # 빠르게 지나가는 빛줄기 (속도감)
    for k in range(10):
        x0 = (k * .137) % 1; y0 = (k * .291) % 1
        nx, ny = flow(x0, y0, t, 30)
        px, py = nx * SW, ny * SH
        d.line([(px, py), (px + 10, py - 5)], fill=(200, 240, 255, 90))
    # 열차 (가운데, 살짝 출렁)
    bob = round(math.sin(t * 2.4) * 2)
    tx, ty = (SW - TRAIN.width) // 2 + 6, SH // 2 - TRAIN.height // 2 + bob
    img.paste(TRAIN, (tx, ty), TRAIN)
    # 열차 밑 안개 꼬리
    fog = Image.new('RGBA', (SW, SH), (0, 0, 0, 0)); f = ImageDraw.Draw(fog)
    for k in range(7):
        ox = (t * 14 + k * 9) % 70
        f.ellipse([tx + 30 + ox * 1.6, ty + 80 - ox * .8, tx + 70 + ox * 1.6, ty + 92 - ox * .8], fill=(210, 200, 240, max(0, 70 - int(ox))))
    img.paste(fog, (0, 0), fog)
    # 시작·끝 페이드
    fade = max(0.0, 1 - t / .4, (t - (SEC - .5)) / .5)
    if fade > 0: img = Image.blend(img, Image.new('RGB', (SW, SH), (10, 6, 22)), min(1, fade))
    big = img.resize((SW * K, SH * K), Image.NEAREST)
    bd = ImageDraw.Draw(big, 'RGBA')
    txt = '열차가 이동하고 있어요'
    tw = bd.textlength(txt, font=FONT)
    bx, by = (SW * K - tw) / 2 - 18, SH * K - 64
    bd.rounded_rectangle([bx, by, bx + tw + 36, by + 40], radius=12, fill=(20, 13, 30, 235), outline=(122, 224, 224, 255), width=2)
    dots = '.' * (1 + int(t * 2) % 3)
    bd.text((bx + 18, by + 8), txt, font=FONT, fill=(246, 240, 255, 255))
    bd.text((bx + 18 + tw, by + 8), dots, font=FONT, fill=(122, 224, 224, 255))
    return big


if __name__ == '__main__':
    frames = [frame(i) for i in range(N)]
    frames[0].save('out/gtrain_travel.gif', save_all=True, append_images=frames[1:], duration=int(1000 / FPS), loop=0, optimize=True)
    for s in (1, 3, 5, 7):
        frames[int(s * FPS)].save(f'out/gtrain_travel_{s}s.png')
    print('saved', len(frames), 'frames')
