# 무슈 블랑 보상 시안: 할로윈 꾸미기 (이름표 테두리 6종 · 말풍선 6종)
#   python3 halloween_deco.py <게임 화면 캡처(2배, 이름표가 x 356~424 · y 845~879 근처)> → out/hw_deco_preview.png · out/hw_tags.png · out/hw_bubbles.png · out/hw_emo.png
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
FB = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
F11 = ImageFont.truetype(FB, 11); F14 = ImageFont.truetype(FB, 14); F12 = ImageFont.truetype(FB, 12)
def H(c, a=255): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
def tw(t, f=F11): return int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(t, font=f))
# ---------- 이름표 (1배로 그려서 게임처럼 2배로 키워요) ----------
def pumpkin_ico(d, x, y):   # 7×6 작은 호박
    d.ellipse([x, y + 1, x + 6, y + 6], fill=H('#F07A18')); d.ellipse([x, y + 1, x + 3, y + 5], fill=H('#FF9A3A')); d.line([(x + 3, y + 1), (x + 3, y + 6)], fill=H('#B4560E'))
    d.point((x + 3, y), fill=H('#5A7A22')); d.point((x + 2, y + 3), fill=H('#FFE070')); d.point((x + 4, y + 3), fill=H('#FFE070'))
def tag(style, name):
    w = tw(name); pad = 5; W = w + pad * 2; Hh = 15; ex = 8   # 양옆 장식 자리
    im = Image.new('RGBA', (W + ex * 2, Hh + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0, y0 = ex, 5
    if style == 'pumpkin':
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=H('#2A140A', 220), outline=H('#F07A18'))
        d.line([(x0 + 3, y0 + Hh - 1), (x0 + W - 4, y0 + Hh - 1)], fill=H('#B4560E'))
        pumpkin_ico(d, x0 - 6, y0 + 4); pumpkin_ico(d, x0 + W - 1, y0 + 4); col = '#FFC23A'
    elif style == 'bat':
        for k, xx in ((-1, x0 + 1), (1, x0 + W - 2)):
            pts = [(xx, y0 + 3), (xx + k * 4, y0), (xx + k * 8, y0 + 2), (xx + k * 7, y0 + 6), (xx + k * 5, y0 + 5), (xx + k * 4, y0 + 8), (xx + k * 2, y0 + 6)]
            d.polygon(pts, fill=H('#5A3A7A')); d.line([pts[0], pts[2]], fill=H('#7A5A9A'))
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=H('#1A1028', 225), outline=H('#9A6ACA'))
        d.point((x0 + W // 2 - 1, y0 + Hh), fill=H('#9A6ACA')); d.point((x0 + W // 2 + 1, y0 + Hh), fill=H('#9A6ACA')); col = '#E0C0FF'
    elif style == 'candy':   # 사탕옥수수 줄무늬 테두리 + 양옆 포장 사탕
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=H('#2A1424', 225), outline=H('#FFF4E0'))
        for i in range(2, W - 2, 4): d.line([(x0 + i, y0), (x0 + i + 1, y0)], fill=H('#FF9A2A')); d.line([(x0 + i + 2, y0), (x0 + i + 2, y0)], fill=H('#FFE04A'))
        for i in range(2, W - 2, 4): d.line([(x0 + i, y0 + Hh - 1), (x0 + i + 1, y0 + Hh - 1)], fill=H('#FF9A2A')); d.point((x0 + i + 2, y0 + Hh - 1), fill=H('#FFE04A'))
        for xx in (x0 - 6, x0 + W - 1):
            d.ellipse([xx + 1, y0 + 4, xx + 5, y0 + 8], fill=H('#FF5A8A')); d.point((xx + 2, y0 + 5), fill=H('#FFFFFF'))
            d.polygon([(xx + 1, y0 + 6), (xx - 1, y0 + 4), (xx - 1, y0 + 8)], fill=H('#FF9AC0')); d.polygon([(xx + 5, y0 + 6), (xx + 7, y0 + 4), (xx + 7, y0 + 8)], fill=H('#FF9AC0'))
        col = '#FFD8E8'
    elif style == 'bone':   # 뼈 테두리 + 양옆 해골
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 3, fill=H('#1E1A16', 225), outline=H('#E8DEC8'))
        for (xx, yy) in ((x0, y0), (x0 + W - 1, y0), (x0, y0 + Hh - 1), (x0 + W - 1, y0 + Hh - 1)):
            d.ellipse([xx - 2, yy - 2, xx, yy], fill=H('#F4ECDA')); d.ellipse([xx, yy - 2, xx + 2, yy], fill=H('#F4ECDA'))
        for xx in (x0 - 7, x0 + W):
            d.ellipse([xx, y0 + 3, xx + 6, y0 + 9], fill=H('#F0EADC')); d.rectangle([xx + 2, y0 + 9, xx + 4, y0 + 10], fill=H('#E0D8C8'))
            d.point((xx + 2, y0 + 6), fill=H('#2A1A24')); d.point((xx + 4, y0 + 6), fill=H('#2A1A24')); d.point((xx + 3, y0 + 8), fill=H('#9A9282'))
        col = '#F4ECDA'
    elif style == 'slime':   # 초록 물약이 흘러내리는 테두리
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=H('#10201A', 225), outline=H('#6AE05A'))
        for i, ln in zip(range(4, W - 3, 7), [3, 5, 2, 4, 6, 3, 2, 5, 4, 3]):
            d.line([(x0 + i, y0 + Hh - 1), (x0 + i, y0 + Hh - 1 + ln)], fill=H('#6AE05A')); d.point((x0 + i, y0 + Hh + ln), fill=H('#9AFF8A'))
        for xx in (x0 - 6, x0 + W):   # 작은 물약병
            d.rectangle([xx + 2, y0 + 2, xx + 3, y0 + 4], fill=H('#C8B8A0')); d.ellipse([xx, y0 + 4, xx + 5, y0 + 10], fill=H('#3A9A3A')); d.ellipse([xx, y0 + 4, xx + 5, y0 + 7], fill=H('#7AFF6A')); d.point((xx + 1, y0 + 6), fill=H('#FFFFFF'))
        col = '#C8FFB8'
    else:   # web
        d.rounded_rectangle([x0, y0, x0 + W - 1, y0 + Hh - 1], 4, fill=H('#16141E', 225), outline=H('#B8B4C8'))
        for r in (3, 6): d.arc([x0 - r, y0 - r, x0 + r, y0 + r], 0, 90, fill=H('#D0CCE0'))
        d.line([(x0, y0), (x0 + 7, y0 + 7)], fill=H('#D0CCE0')); d.line([(x0, y0), (x0 + 8, y0 + 2)], fill=H('#D0CCE0')); d.line([(x0, y0), (x0 + 2, y0 + 8)], fill=H('#D0CCE0'))
        sx = x0 + W + 2; d.line([(sx, y0), (sx, y0 + 9)], fill=H('#C8C4D8')); d.ellipse([sx - 2, y0 + 9, sx + 2, y0 + 13], fill=H('#2A1E30'))
        for dx, dy in ((-3, 9), (3, 9), (-3, 13), (3, 13)): d.point((sx + dx, y0 + dy), fill=H('#2A1E30'))
        d.point((sx - 1, y0 + 10), fill=H('#FF4A5A')); col = '#E8E6F4'
    d.text((x0 + pad, y0 + 2), name, font=F11, fill=H(col)); return im
# ---------- 말풍선 ----------
def bubble(style, text):
    w = tw(text); W = w + 14; Hh = 19; im = Image.new('RGBA', (W + 12, Hh + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0, y0 = 6, 14
    if style == 'ghost':
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 7, fill=H('#EEF4FF'), outline=H('#5A6A9A'))
        for i in range(0, W, 6): d.ellipse([x0 + i, y0 + Hh - 3, x0 + i + 6, y0 + Hh + 3], fill=H('#EEF4FF'), outline=H('#5A6A9A'))
        d.rectangle([x0 + 1, y0 + Hh - 3, x0 + W - 1, y0 + Hh], fill=H('#EEF4FF'))
        d.point((x0 + W - 8, y0 - 2), fill=H('#2A2440')); d.point((x0 + W - 5, y0 - 2), fill=H('#2A2440')); d.arc([x0 + W - 11, y0 - 6, x0 + W - 2, y0 + 3], 180, 360, fill=H('#5A6A9A'))
        col = '#3A3A6A'; tail = '#5A6A9A'
    elif style == 'jack':
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 8, fill=H('#FF9A3A'), outline=H('#7A3408'))
        for xx in (x0 + W // 3, x0 + 2 * W // 3): d.line([(xx, y0 + 2), (xx, y0 + Hh - 2)], fill=H('#F07A18'))
        d.rectangle([x0 + W // 2 - 1, y0 - 4, x0 + W // 2 + 1, y0], fill=H('#5A7A22')); d.line([(x0 + W // 2 + 1, y0 - 4), (x0 + W // 2 + 4, y0 - 6)], fill=H('#5A7A22'))
        col = '#3A1404'; tail = '#7A3408'
    elif style == 'slime':   # 끈적한 물약 말풍선
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 7, fill=H('#7AE86A'), outline=H('#1E5A1E'))
        for i, ln in zip(range(5, W - 4, 8), [3, 5, 2, 4, 6, 3, 4, 2, 5, 3, 4]):
            d.rectangle([x0 + i, y0 + Hh, x0 + i + 1, y0 + Hh + ln], fill=H('#7AE86A')); d.point((x0 + i, y0 + Hh + ln + 1), fill=H('#1E5A1E')); d.point((x0 + i + 1, y0 + Hh + ln + 1), fill=H('#1E5A1E'))
        for x, y in ((x0 + 4, y0 + 3), (x0 + W - 6, y0 + 4)): d.ellipse([x, y, x + 2, y + 2], fill=H('#C8FFB8'))
        col = '#0E3A0E'; tail = '#1E5A1E'
    elif style == 'tomb':   # 묘비 돌 말풍선
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 3, fill=H('#9A96A8'), outline=H('#3A3648'))
        cx0 = x0 + W // 2; d.pieslice([cx0 - 9, y0 - 7, cx0 + 9, y0 + 9], 180, 360, fill=H('#9A96A8'), outline=H('#3A3648')); d.line([(cx0 - 8, y0), (cx0 + 8, y0)], fill=H('#9A96A8'))
        d.line([(cx0, y0 - 5), (cx0, y0 - 1)], fill=H('#3A3648')); d.line([(cx0 - 2, y0 - 4), (cx0 + 2, y0 - 4)], fill=H('#3A3648'))
        d.line([(x0 + 1, y0 + 1), (x0 + W - 1, y0 + 1)], fill=H('#C0BCCC')); d.line([(x0 + 3, y0 + 3), (x0 + 5, y0 + 5)], fill=H('#5A566A'))
        for x in range(x0 + 3, x0 + W - 3, 9): d.point((x, y0 + Hh - 2), fill=H('#6A8A4A')); d.point((x + 1, y0 + Hh - 3), fill=H('#6A8A4A'))
        col = '#1E1A2A'; tail = '#3A3648'
    elif style == 'candy':   # 줄무늬 사탕 말풍선
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 9, fill=H('#FFE8F0'), outline=H('#C83A6A'))
        for i in range(3, W - 2, 6): d.line([(x0 + i, y0 + 1), (x0 + i + 3, y0 + 1)], fill=H('#FF5A8A')); d.line([(x0 + i, y0 + Hh - 1), (x0 + i + 3, y0 + Hh - 1)], fill=H('#FF5A8A'))
        d.polygon([(x0, y0 + Hh // 2), (x0 - 5, y0 + 3), (x0 - 5, y0 + Hh - 3)], fill=H('#FF9AC0'), outline=H('#C83A6A'))
        d.polygon([(x0 + W, y0 + Hh // 2), (x0 + W + 5, y0 + 3), (x0 + W + 5, y0 + Hh - 3)], fill=H('#FF9AC0'), outline=H('#C83A6A'))
        col = '#7A1A3A'; tail = '#C83A6A'
    else:   # witch
        d.rounded_rectangle([x0, y0, x0 + W, y0 + Hh], 4, fill=H('#3A1E5A'), outline=H('#C8A0FF'))
        d.polygon([(x0 - 3, y0 + 2), (x0 + 11, y0 + 2), (x0 + 6, y0 - 5), (x0 + 9, y0 - 9)], fill=H('#6A3A9A')); d.rectangle([x0 - 3, y0 + 1, x0 + 11, y0 + 2], fill=H('#2A1440')); d.point((x0 + 4, y0 + 1), fill=H('#E8B030'))
        for x, y in ((x0 + W - 4, y0 + 3), (x0 + W - 9, y0 + Hh - 4)): d.point((x, y), fill=H('#FFE89A'))
        col = '#F4E8FF'; tail = '#C8A0FF'
    cx = x0 + W // 2; d.polygon([(cx - 3, y0 + Hh), (cx + 3, y0 + Hh), (cx, y0 + Hh + 4)], fill=H(tail))
    d.text((x0 + 7, y0 + 4), text, font=F11, fill=H(col)); return im
# ---------- 이모티콘 16×16 (게임에선 48px로 보여요) ----------
def emo(kind):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'jack':
        d.ellipse([1, 3, 14, 15], fill=H('#F07A18')); d.ellipse([1, 3, 8, 12], fill=H('#FF9A3A')); d.line([(7, 3), (7, 15)], fill=H('#B4560E')); d.rectangle([7, 0, 8, 3], fill=H('#5A7A22'))
        d.polygon([(3, 8), (5, 6), (6, 9)], fill=H('#FFE070')); d.polygon([(12, 8), (10, 6), (9, 9)], fill=H('#FFE070')); d.polygon([(3, 11), (12, 11), (10, 13), (7, 12), (5, 13)], fill=H('#FFE070'))
    elif kind == 'boo':
        d.polygon([(3, 6), (8, 1), (13, 6), (13, 14), (11, 12), (9, 14), (7, 12), (5, 14), (3, 12)], fill=H('#EEF2FA')); d.ellipse([3, 1, 13, 10], fill=H('#EEF2FA'))
        for x in (5, 6, 10, 11): d.point((x, 5), fill=H('#1A1428')); d.point((x, 6), fill=H('#1A1428'))
        d.rectangle([7, 8, 9, 10], fill=H('#1A1428')); d.point((7, 8), fill=H('#EEF2FA')); d.point((9, 8), fill=H('#EEF2FA')); d.point((4, 3), fill=H('#FFFFFF'))
    elif kind == 'bat':
        d.polygon([(8, 7), (4, 3), (0, 6), (2, 9), (4, 8), (5, 11)], fill=H('#5A3A7A')); d.polygon([(8, 7), (12, 3), (16, 6), (14, 9), (12, 8), (11, 11)], fill=H('#5A3A7A'))
        d.ellipse([5, 5, 11, 12], fill=H('#7A5A9A')); d.point((7, 7), fill=H('#FF4A5A')); d.point((9, 7), fill=H('#FF4A5A')); d.point((6, 4), fill=H('#7A5A9A')); d.point((10, 4), fill=H('#7A5A9A'))
    elif kind == 'skull':
        d.ellipse([2, 1, 13, 11], fill=H('#F0EADC')); d.rectangle([5, 10, 10, 14], fill=H('#E0D8C8')); d.rectangle([4, 5, 6, 7], fill=H('#2A1A24')); d.rectangle([9, 5, 11, 7], fill=H('#2A1A24')); d.point((5, 6), fill=H('#E8485A')); d.point((10, 6), fill=H('#E8485A'))
        d.point((7, 9), fill=H('#2A1A24')); d.point((6, 12), fill=H('#9A9282')); d.point((9, 12), fill=H('#9A9282'))
    elif kind == 'candy':
        d.ellipse([4, 4, 11, 11], fill=H('#FF5A8A')); d.arc([5, 5, 10, 10], 0, 270, fill=H('#FFFFFF')); d.polygon([(4, 7), (0, 4), (0, 11)], fill=H('#FF9AC0')); d.polygon([(11, 7), (15, 4), (15, 11)], fill=H('#FF9AC0'))
    else:   # cauldron
        d.ellipse([2, 6, 13, 15], fill=H('#2A2238')); d.ellipse([2, 6, 9, 12], fill=H('#3A3250')); d.ellipse([3, 5, 12, 8], fill=H('#7AFF6A'))
        for x, y, r in ((5, 3, 1), (9, 1, 1.5), (11, 4, 1)): d.ellipse([x - r, y - r, x + r, y + r], fill=H('#9AFF8A'))
    return im
def outline(im):   # 이모티콘 테두리
    import numpy as np
    a = np.array(im); al = a[..., 3] > 0; o = a.copy()
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if al[y, x]: continue
            if any(0 <= y + dy < a.shape[0] and 0 <= x + dx < a.shape[1] and al[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): o[y, x] = [30, 18, 40, 255]
    return Image.fromarray(o)
TAGS = [('pumpkin', '호박 이름표'), ('bat', '박쥐 이름표'), ('web', '거미줄 이름표'), ('candy', '사탕옥수수 이름표'), ('bone', '해골 이름표'), ('slime', '물약 이름표')]
BUBS = [('ghost', '유령 말풍선', '안녕! 오늘 무서운 날이야.'), ('jack', '잭오랜턴 말풍선', '사탕 안 주면 장난칠 거야!'), ('witch', '마녀 말풍선', '비밀 물약 레시피 알아?'),
        ('slime', '물약 말풍선', '으앗, 손이 끈적끈적해!'), ('tomb', '묘비 말풍선', '여기 잠들다.... 숙제와 함께.'), ('candy', '사탕 말풍선', '사탕 하나 줄까?')]
EMOS = [('jack', '씩 웃는 호박'), ('boo', '깜짝 유령'), ('bat', '박쥐'), ('skull', '해골'), ('candy', '사탕'), ('cauldron', '보글보글 솥')]
if __name__ == '__main__':
    shot = Image.open(sys.argv[1]).convert('RGBA'); bg = shot.crop((210, 660, 570, 930))   # 내 캐릭터 둘레 (이름표 가운데 ≈ (180, 202))
    up = lambda im, k=2: im.resize((im.width * k, im.height * k), Image.NEAREST)
    cards = []
    for st, nm in TAGS:
        c = bg.copy(); t = up(tag(st, '민준')); c.alpha_composite(t, (182 - t.width // 2, 167 - t.height // 2 + 4)); cards.append((c, nm))
    for st, nm, tx in BUBS:
        c = bg.copy(); t = up(tag('pumpkin', '민준')) if False else None; b = up(bubble(st, tx)); c.alpha_composite(b, (182 - b.width // 2, 74 - b.height // 2)); cards.append((c, nm))
    cw, ch = bg.width, bg.height; rows = (len(cards) + 2) // 3; pv = Image.new('RGB', (cw * 3 + 40, 60 + (ch + 40) * rows), (26, 18, 34)); d = ImageDraw.Draw(pv)
    d.text((14, 16), '무슈 블랑 보상 · 할로윈 이름표 6 · 말풍선 6 (게임 화면 크기 그대로)', font=F14, fill=H('#FFE9A0'))
    for i, (c, nm) in enumerate(cards):
        x = 10 + (i % 3) * (cw + 10); y = 50 + (i // 3) * (ch + 40); pv.paste(c, (x, y)); d.text((x + cw // 2, y + ch + 16), nm, font=F12, fill=H('#F1E9FF'), anchor='mm')
    pv.save(os.path.join(OUT, 'hw_deco_preview.png'))
    for nm, items in (('hw_tags.png', [tag(s, '이름') for s, _ in TAGS]), ('hw_bubbles.png', [bubble(s, t) for s, _, t in BUBS])):
        W = sum(i.width + 2 for i in items); Hh = max(i.height for i in items); sh = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
        for i in items: sh.alpha_composite(i, (x, 0)); x += i.width + 2
        sh.save(os.path.join(OUT, nm))
    print('ok', pv.size)
