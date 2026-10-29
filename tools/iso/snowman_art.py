# 「눈사람」 이벤트 그림: 광장 눈더미 → 몸통 → 머리 → 장식 7가지(모자·목도리·팔·단추·눈·코·입) + 굴리는 눈뭉치
#   python3 snowman_art.py → out/snowman.png (한 줄: 단계 그림·장식 층) + out/snowman.json (칸 위치·기준점) + out/snowball.png
import json, math, os
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 1.6                  # 크기 배율 (사람 옆에 서면 사람이 작아 보이게)
W, H = round(72 * K), round(76 * K)
AX, AY = W // 2, H - 6
OUTL = (18, 10, 24, 255)
def C(h, a=255): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
SNOW, SNOW2, SNOW3, HI = C('#F2F4FF'), C('#CDD5F0'), C('#A9B3DA'), C('#FFFFFF')
def k(v): return round(v * K)

def ellmask(cx, cy, rx, ry):
    return {(x, y) for x in range(W) for y in range(H) if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1}

def snowball(img, cx, cy, rx, ry):
    """눈 덩어리: 왼쪽 위가 밝고 오른쪽 아래로 그늘 (도트 3단)"""
    P = img.load()
    for (x, y) in ellmask(cx, cy, rx, ry):
        u, v = (x + .5 - cx) / rx, (y + .5 - cy) / ry
        k = u * .55 + v * .8
        P[x, y] = HI if k < -.75 else SNOW if k < .25 else SNOW2 if k < .7 else SNOW3
    return img

def outline(img):
    P = img.load(); add = []
    for y in range(H):
        for x in range(W):
            if P[x, y][3] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and P[x + dx, y + dy][3] > 200 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for x, y in add: P[x, y] = OUTL
    return img

def ground(img, rx):
    d = ImageDraw.Draw(img); d.ellipse([AX - rx, AY - 3, AX + rx, AY + 3], fill=(40, 50, 90, 70))

def new(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))

BODY = (AX, AY - k(14), k(17), k(14))       # 몸통
HEAD = (AX, AY - k(38), k(13), k(12))       # 머리

def mound(t):
    """눈더미: t=0~1 (몸통이 600까지 차는 동안 점점 커져요)"""
    im = new(); rx = k(8 + 11 * t); ry = k(3 + 7 * t)
    snowball(im, AX, AY - ry + 1, rx, ry)
    if t > .3: snowball(im, AX - rx * .45, AY - ry * .7, rx * .45, ry * .6)
    outline(im); g = new(); ground(g, int(rx + 3)); g.alpha_composite(im); return g

def body_only():
    im = new(); snowball(im, *BODY); outline(im); g = new(); ground(g, k(20)); g.alpha_composite(im); return g

def head_mound(t):
    """몸통 위에 머리가 점점 생겨요 (t=0~1)"""
    g = body_only(); im = new(); cx, cy, rx, ry = HEAD; r = .45 + .55 * t
    snowball(im, cx, cy + (1 - r) * ry * 1.4, rx * r, ry * r); outline(im); g.alpha_composite(im); return g

def full():
    g = body_only(); im = new(); snowball(im, *HEAD); outline(im); g.alpha_composite(im); return g

# ---------- 장식 층 (같은 칸 크기, 겹쳐 그려요) ----------
def deco_hat():   # 해님 호박 모자: 주황 호박 세 쪽 + 골 + 꼭지 + 챙
    im = new(); d = ImageDraw.Draw(im); cx, cy = HEAD[0], HEAD[1] - HEAD[3] + k(2)
    d.ellipse([cx - k(11), cy - k(2), cx + k(11), cy + k(1)], fill=C('#C8642A'))
    for dx, c in ((-5, '#E88A34'), (5, '#E88A34'), (0, '#F6A848')): d.ellipse([cx + k(dx - 5), cy - k(11), cx + k(dx + 5), cy + k(1)], fill=C(c))
    for dx in (-2, 3): d.line([(cx + k(dx), cy - k(9)), (cx + k(dx), cy - k(1))], fill=C('#C8642A'), width=max(1, k(.8)))
    d.rectangle([cx - k(1), cy - k(14), cx + k(1), cy - k(11)], fill=C('#4A7A2E')); d.ellipse([cx + k(1), cy - k(14), cx + k(4), cy - k(12)], fill=C('#6EA040'))
    d.point((cx - k(6), cy - k(8)), fill=C('#FFD08A')); d.point((cx - k(6) + 1, cy - k(8)), fill=C('#FFD08A'))
    return outline(im)
def deco_scarf():   # 구름 목화 + 양털 목도리: 하늘색·흰 줄무늬, 한쪽 끝이 늘어져요
    im = new(); d = ImageDraw.Draw(im); y = HEAD[1] + HEAD[3] - k(1); st = k(3)
    for x in range(AX - k(13), AX + k(14)):
        c = C('#8FC4F0') if ((x - AX) // st) % 2 else C('#F4F8FF'); sag = abs(x - AX) * .18
        d.line([(x, y - k(1) + sag), (x, y + k(3) + sag)], fill=c)
    for j in range(k(9)): c = C('#8FC4F0') if (j // st) % 2 == 0 else C('#F4F8FF'); d.line([(AX + k(7), y + k(3) + j), (AX + k(11), y + k(3) + j)], fill=c)
    for x in range(AX + k(7), AX + k(12), 2): d.line([(x, y + k(12)), (x, y + k(13))], fill=C('#6FA4D8'))   # 술
    return outline(im)
def deco_arms():   # 빗자루 짚 팔: 양쪽으로 뻗은 지푸라기 묶음
    im = new(); d = ImageDraw.Draw(im); y = BODY[1] - k(6)
    for sd in (-1, 1):
        x0 = AX + sd * k(15); d.line([(x0, y + k(2)), (x0 + sd * k(10), y - k(6))], fill=C('#B88A3E'), width=k(2))
        for t in (-1, 0, 1): d.line([(x0 + sd * k(9), y - k(5)), (x0 + sd * k(13), y - k(9) + t * k(3))], fill=C('#D8B460'), width=max(1, k(.7)))
    return outline(im)
def deco_buttons():   # 반짝 돌 단추 3개
    im = new(); d = ImageDraw.Draw(im); r = k(2)
    for y in (BODY[1] - k(8), BODY[1] - k(2), BODY[1] + k(4)): d.ellipse([AX - r, y - r, AX + r, y + r], fill=C('#8A90A8')); d.point((AX - 1, y - 1), fill=C('#FFFFFF')); d.point((AX + 1, y + 1), fill=C('#C8D0E8'))
    return outline(im)
def deco_eyes():   # 월장석 눈: 은은한 푸른빛
    im = new(); d = ImageDraw.Draw(im); y = HEAD[1] - k(3)
    for x in (AX - k(6), AX + k(3)):
        d.rectangle([x, y, x + k(2.5), y + k(2.5)], fill=C('#2A3060')); d.rectangle([x, y, x + 1, y + 1], fill=C('#DFF4FF')); d.point((x + 2, y + 2), fill=C('#7AB8E8'))
    return im
def deco_nose():   # 당근 코
    im = new(); d = ImageDraw.Draw(im); y = HEAD[1] + k(1)
    d.polygon([(AX - 1, y - k(2)), (AX - 1, y + k(2)), (AX - k(10), y + k(1))], fill=C('#F08A30')); d.line([(AX - k(4), y - k(1)), (AX - k(4), y + k(1))], fill=C('#C8642A')); d.line([(AX - k(7), y), (AX - k(7), y + k(1))], fill=C('#C8642A'))
    return outline(im)
def deco_mouth():   # 자수정 입: 보라 알 5개 웃는 모양
    im = new(); d = ImageDraw.Draw(im); y = HEAD[1] + k(5)
    for dx, dy in ((-6, -1), (-3, 1), (0, 2), (3, 1), (6, -1)): x0, y0 = AX + k(dx), y + k(dy); d.rectangle([x0, y0, x0 + k(1.2), y0 + k(1.2)], fill=C('#7A3AB8')); d.point((x0, y0), fill=C('#C89AFF'))
    return im

DECO = [('hat', '모자', deco_hat), ('scarf', '목도리', deco_scarf), ('arms', '팔', deco_arms), ('buttons', '단추', deco_buttons), ('eyes', '눈', deco_eyes), ('nose', '코', deco_nose), ('mouth', '입', deco_mouth)]

def snowballs():
    """굴리는 눈뭉치 6단계 (크기 1~30 → 지름 4~14px)"""
    out = Image.new('RGBA', (16 * 6, 16), (0, 0, 0, 0))
    for i in range(6):
        r = 2 + i * 1.1; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); snowball(im, AX, AY - r, r, r * .9); outline(im)
        out.alpha_composite(im.crop((AX - 8, AY - 16, AX + 8, AY)), (i * 16, 0))
    return out

if __name__ == '__main__':
    frames = [('mound%d' % i, mound(t)) for i, t in enumerate((.12, .35, .6, .85))] + [('body', body_only())] + [('head%d' % i, head_mound(t)) for i, t in enumerate((.2, .6))] + [('full', full())] + [(k, f()) for k, _, f in DECO]
    sheet = Image.new('RGBA', (W * len(frames), H), (0, 0, 0, 0)); meta = {}
    for i, (k, im) in enumerate(frames): sheet.alpha_composite(im, (i * W, 0)); meta[k] = i
    sheet.save('out/snowman.png'); snowballs().save('out/snowball.png')
    json.dump({'w': W, 'h': H, 'ax': AX, 'ay': AY, 'cell': meta, 'deco': [k for k, _, _ in DECO]}, open('out/snowman.json', 'w'), ensure_ascii=False)
    print('snowman', sheet.size)
