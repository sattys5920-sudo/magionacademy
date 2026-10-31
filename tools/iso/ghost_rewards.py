# 시안: 유령 전학생 마틸다 졸업식 보상 그림 — 방 가구 「빛바랜 졸업 사진」 · 단추 3종(32×32) · 「개근상 이름표」 · 졸업 모자(lpc/grad_cap.py)를 한 장에
#   python3 ghost_rewards.py → out/ghost_photo.png · out/ghost_buttons.png · out/ghost_rewards_preview.png
import os, math
from PIL import Image, ImageDraw, ImageFont
from interiors import Room, hexc, shade
from furniture import bx, C, ell, H
from fairy_furn import glow, sparkle
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
GH = Image.open(os.path.join(OUT, 'ghost_lpc.png')).convert('RGBA')
def photo(R, img, d):   # 빛바랜 졸업 사진: 나무 받침대 위 금빛 액자, 안에 세피아 사진(나 · 마틸다 · 졸업 모자)
    x, y = C(R, 1.5, 1.5); x, y = int(x), int(y); bx(R, img, 1.25, 1.25, .5, .5, 3, '#7A5232', top='#9A6A42'); d = ImageDraw.Draw(img)
    d.line([(x - 3, y - 3), (x - 5, y - 26)], fill=H('#6A4424')); d.line([(x + 3, y - 3), (x + 5, y - 26)], fill=H('#6A4424'))   # 이젤 다리
    fx0, fy0, fx1, fy1 = x - 11, y - 36, x + 11, y - 14
    d.rectangle([fx0 - 1, fy0 - 1, fx1 + 1, fy1 + 1], fill=H('#5A3A12')); d.rectangle([fx0, fy0, fx1, fy1], fill=H('#C8902A')); d.rectangle([fx0 + 1, fy0 + 1, fx1 - 1, fy1 - 1], fill=H('#E8B84A'))
    d.rectangle([fx0 + 3, fy0 + 3, fx1 - 3, fy1 - 3], fill=H('#D8C49A'))   # 세피아 사진
    for yy in range(fy0 + 3, fy1 - 2, 3): d.line([(fx0 + 3, yy), (fx1 - 3, yy)], fill=H('#CDB78A'))
    # 사진 속 두 사람: 왼쪽 나(갈색 실루엣), 오른쪽 마틸다(옅은 하늘빛) · 둘 다 손을 들어 비밀 인사
    sep = lambda c: tuple(int(v) for v in (c[0] * .5 + 120, c[1] * .42 + 92, c[2] * .3 + 60))
    def fig(px, py, hair, body, ghost=False):   # 사진 속 작은 사람 (머리 · 얼굴 · 몸 · 비밀 인사로 든 손)
        hc, bc, sk = sep(hexc(hair)), sep(hexc(body)), sep(hexc('#F0C8A0'))
        if ghost: hc, bc, sk = (196, 208, 214), (176, 196, 210), (222, 228, 232)
        d.rectangle([px - 2, py - 1, px + 2, py + 2], fill=hc); d.rectangle([px - 1, py + 1, px + 1, py + 3], fill=sk); d.point((px - 1, py + 2), fill=(70, 50, 40)); d.point((px + 1, py + 2), fill=(70, 50, 40))
        d.rectangle([px - 2, py + 4, px + 2, py + 9], fill=bc); d.rectangle([px - 1, py + 10, px + 1, py + 12], fill=bc if not ghost else (190, 204, 214))
    fig(x - 4, fy0 + 5, '#6A3A1A', '#8A2A2A'); fig(x + 4, fy0 + 5, '#2A2A3A', '#2A3A6A', True)
    d.line([(x - 2, fy0 + 9), (x, fy0 + 6)], fill=(150, 110, 80)); d.line([(x + 2, fy0 + 9), (x, fy0 + 6)], fill=(200, 212, 222))
    d.point((x, fy0 + 5), fill=H('#FFF6D0'))   # 손이 닿은 곳 반짝
    d.line([(x + 1, fy0 + 3), (x + 7, fy0 + 3)], fill=(60, 52, 48)); d.point((x + 7, fy0 + 4), fill=H('#C8902A'))   # 마틸다의 졸업 모자
    d.point((fx1 - 4, fy0 + 4), fill=H('#B8A47A')); d.point((fx0 + 4, fy1 - 4), fill=H('#B8A47A'))
    glow(img, x + 4, fy0 + 10, 6, '#C8E4FF', 45); d = ImageDraw.Draw(img); sparkle(d, fx1 + 3, fy0 - 2, '#FFF0B0')
def button(kind):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'rust':   # 마틸다의 녹슨 단추 (100 년 묵은 놋쇠 · 무늬 같음)
        ell(d, 16, 16, 10, 10, '#3A2414'); ell(d, 16, 16, 9, 9, '#8A6A2A'); ell(d, 15, 15, 7, 7, '#B08A3A'); ell(d, 13, 13, 3, 2, '#D8B860')
        for (a, b) in ((13, 13), (19, 13), (13, 19), (19, 19)): ell(d, a, b, 1.2, 1.2, '#3A2414')
        for (a, b) in ((21, 22), (10, 20), (22, 10)): d.point((a, b), fill=H('#5A8A6A')); d.point((a + 1, b), fill=H('#4A7A5A'))   # 녹
        d.arc([8, 8, 24, 24], 200, 250, fill=H('#E8D090'))
    elif kind == 'mine':   # 되돌아온 내 단추 (반짝이는 교복 단추 · 작은 하트 빛)
        ell(d, 16, 16, 10, 10, '#2A1E44'); ell(d, 16, 16, 9, 9, '#C8C8D8'); ell(d, 15, 15, 7, 7, '#E8E8F4'); ell(d, 13, 13, 3, 2, '#FFFFFF')
        d.line([(16, 12), (16, 20)], fill=H('#9A8AC8')); d.line([(12, 16), (20, 16)], fill=H('#9A8AC8')); d.point((16, 16), fill=H('#FFFFFF'))
        for (a, b) in ((14, 15), (18, 15), (14, 19), (18, 19)): d.point((a, b), fill=H('#6A6A8A'))
        d.polygon([(25, 6), (27, 4), (29, 6), (27, 9)], fill=H('#FF8AB0'))
    else:   # 단추 없는 단춧구멍 브로치 (리본 + 빈 고리)
        d.polygon([(16, 14), (6, 8), (7, 20)], fill=H('#3A6AB8')); d.polygon([(16, 14), (26, 8), (25, 20)], fill=H('#3A6AB8')); d.polygon([(16, 14), (8, 10), (8, 18)], fill=H('#5A8AD8'))
        d.polygon([(14, 16), (10, 28), (13, 27), (15, 25)], fill=H('#2A5A9A')); d.polygon([(18, 16), (22, 28), (19, 27), (17, 25)], fill=H('#2A5A9A'))
        ell(d, 16, 14, 4, 4, '#C8902A'); ell(d, 16, 14, 2, 2, (0, 0, 0, 0)); d.point((14, 12), fill=H('#FFE070'))
    # 테두리
    import numpy as np
    a = np.array(im); al = a[..., 3] > 0; o = a.copy()
    for yy in range(32):
        for xx in range(32):
            if al[yy, xx]: continue
            if any(0 <= yy + dy < 32 and 0 <= xx + dx < 32 and al[yy + dy, xx + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): o[yy, xx] = [24, 16, 32, 255]
    return Image.fromarray(o)
def tag(name):   # 개근상 이름표: 금빛 테두리, 양옆 별, 위에 작은 리본 「개근」
    F = ImageFont.truetype(FB, 11); w = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(name, font=F)); W = w + 10; Hh = 15
    im = Image.new('RGBA', (W + 20, Hh + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0, y0 = 10, 9
    d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=(40, 28, 12, 235), outline=H('#E8B84A')); d.line([(x0 + 3, y0 + 1), (x0 + W - 4, y0 + 1)], fill=H('#FFE9A0'))
    for sx in (x0 - 6, x0 + W + 1):
        d.polygon([(sx + 2, y0 + 3), (sx + 3, y0 + 6), (sx + 6, y0 + 6), (sx + 3.5, y0 + 8), (sx + 4.5, y0 + 11), (sx + 2, y0 + 9), (sx - .5, y0 + 11), (sx + .5, y0 + 8), (sx - 2, y0 + 6), (sx + 1, y0 + 6)], fill=H('#FFD040'))
    cx = x0 + W // 2; d.rectangle([cx - 9, 1, cx + 9, 8], fill=H('#C83A3A')); d.polygon([(cx - 9, 1), (cx - 12, 4), (cx - 9, 8)], fill=H('#A02A2A')); d.polygon([(cx + 9, 1), (cx + 12, 4), (cx + 9, 8)], fill=H('#A02A2A'))
    d.text((cx, 5), '개근', font=ImageFont.truetype(FB, 8), fill=H('#FFF0C0'), anchor='mm')
    d.text((x0 + 5, y0 + 2), name, font=F, fill=H('#FFE9A0')); return im
if __name__ == '__main__':
    R = Room(6, 6, 60); R.obj('photo', [(1, 1)], lambda img, d: photo(R, img, d)); o = R.objs[-1]; ph = o['img']; ph.save(os.path.join(OUT, 'ghost_photo.png'))
    btns = [button(k) for k in ('rust', 'mine', 'brooch')]; S = Image.new('RGBA', (96, 32)); [S.alpha_composite(b, (i * 32, 0)) for i, b in enumerate(btns)]; S.save(os.path.join(OUT, 'ghost_buttons.png'))
    F = ImageFont.truetype(FB, 16); F2 = ImageFont.truetype(FB, 13)
    pv = Image.new('RGB', (1160, 470), hexc('#2A1E3A')); d = ImageDraw.Draw(pv); d.text((20, 16), '유령 전학생 마틸다 · 졸업식 보상 시안', font=F, fill=hexc('#FFE9A0'))
    def card(x, w, title, sub): d.rounded_rectangle([x, 50, x + w, 450], 14, fill=hexc('#3A2C52')); d.text((x + w // 2, 405), title, font=F2, fill=hexc('#F1E9FF'), anchor='mm'); d.text((x + w // 2, 428), sub, font=ImageFont.truetype(FB, 11), fill=hexc('#D8B4FF'), anchor='mm')
    card(20, 250, '빛바랜 졸업 사진', '방 가구 · 나와 마틸다, 비밀 인사 자세'); big = ph.resize((ph.width * 5, ph.height * 5), Image.NEAREST); pv.paste(big, (145 - big.width // 2, 330 - big.height), big)
    card(290, 300, '마틸다의 졸업 모자', '옷(모자) · 4방향'); cap = Image.open(os.path.join(OUT, 'hat_grad_preview.png')).convert('RGBA'); c2 = cap.crop((0, 0, cap.width // 4, cap.height // 2)); c2 = c2.resize((280, int(c2.height * 280 / c2.width)), Image.NEAREST); pv.paste(c2, (300, 90), c2)
    card(610, 300, '단추 (3 일째 고른 것에 따라 하나)', '녹슨 단추 · 되돌아온 내 단추 · 단춧구멍 브로치')
    for i, b in enumerate(btns): bb = b.resize((80, 80), Image.NEAREST); pv.paste(bb, (630 + i * 92, 170), bb)
    for i, nm in enumerate(('함께 찾은 단추', '내가 준 단추', '없어도 예뻐')): d.text((670 + i * 92, 265), nm, font=ImageFont.truetype(FB, 10), fill=hexc('#E0D4F4'), anchor='mm')
    card(930, 210, '개근상 이름표', '할로윈 이름표처럼 끼워요'); t = tag('민준'); tb = t.resize((t.width * 3, t.height * 3), Image.NEAREST); pv.paste(tb, (1035 - tb.width // 2, 200), tb)
    pv.save(os.path.join(OUT, 'ghost_rewards_preview.png')); print('ok')
