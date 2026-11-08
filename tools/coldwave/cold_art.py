# 양호실 겨울 감기 그림 시안: 감기 물약 4 병 (지금 물약 32 × 32 그림체) · 아픈 표시 (입김 · 체온계) · 증상 4 가지 덧그림 · 진료 수첩 · 가구 2 종
#   python3 tools/coldwave/cold_art.py → tools/coldwave/out/*.png + preview.png
import os
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); O = D + '/out'; os.makedirs(O, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(D))
OL = (42, 26, 46, 255)
def hx(s, a=255): s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3],)

def outline(im):
    p = im.load(); W, H = im.size; out = im.copy(); q = out.load()
    for y in range(H):
        for x in range(W):
            if p[x, y][3] == 0 and any(0 <= x + dx < W and 0 <= y + dy < H and p[x + dx, y + dy][3] and p[x + dx, y + dy] != OL for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): q[x, y] = OL
    return out

def bottle(kind):   # 32 × 32
    im = Image.new('RGBA', (32, 32)); g = ImageDraw.Draw(im)
    cork = hx('#9A6A3A')
    if kind == 'fever':   # 열 내림: 동그란 플라스크 · 얼음빛 하늘색 · 눈송이
        c = hx('#8ADCF0'); g.ellipse([6, 11, 26, 30], fill=c); g.rectangle([13, 5, 19, 12], fill=hx('#D8F0F8')); g.rectangle([12, 2, 20, 5], fill=cork)
        for dx, dy in ((0, 0), (-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)): im.putpixel((16 + dx, 21 + dy), hx('#FFFFFF'))
        g.rectangle([9, 15, 10, 18], fill=sh(c, 1.25))
    elif kind == 'throat':   # 꿀 목: 꿀단지 모양 · 호박색 · 소용돌이
        c = hx('#F2B040'); g.rounded_rectangle([6, 10, 26, 30], radius=6, fill=c); g.rectangle([9, 6, 23, 10], fill=hx('#F8E0A0')); g.rectangle([8, 3, 24, 6], fill=cork)
        for i, (x, y) in enumerate(((16, 19), (17, 19), (18, 20), (18, 21), (17, 22), (16, 22), (15, 21), (15, 20), (14, 19), (14, 23), (15, 24), (16, 24), (17, 24), (18, 24), (19, 23))): im.putpixel((x, y), hx('#FFF2C0'))
        g.rectangle([9, 13, 10, 17], fill=sh(c, 1.2))
    elif kind == 'nose':   # 콧물 뚝: 길쭉한 병 · 연두 · 물방울에 엑스
        c = hx('#9ADC7A'); g.rounded_rectangle([10, 9, 22, 30], radius=3, fill=c); g.rectangle([13, 5, 19, 9], fill=hx('#E0F4D0')); g.rectangle([12, 2, 20, 5], fill=cork)
        g.polygon([(16, 14), (13, 19), (13, 21), (16, 23), (19, 21), (19, 19)], fill=hx('#FFFFFF'))
        for d in range(-2, 3): im.putpixel((16 + d, 19 + d), hx('#5AA040')); im.putpixel((16 + d, 19 - d), hx('#5AA040'))
        g.rectangle([12, 12, 13, 17], fill=sh(c, 1.2))
    elif kind == 'chill':   # 따끈 찜질: 세모 플라스크 · 주황 · 김
        c = hx('#F08A4A'); g.polygon([(16, 9), (5, 29), (27, 29)], fill=c); g.rectangle([13, 5, 19, 12], fill=hx('#F8D8C0')); g.rectangle([12, 2, 20, 5], fill=cork)
        for x0 in (12, 16, 20):
            for k, y in enumerate(range(17, 26)): im.putpixel((x0 + (1 if (k // 2) % 2 else 0), y), hx('#FFE8C8'))
    return outline(im)

def breath():   # 아픈 표시: 하얀 입김 (14 × 9)
    im = Image.new('RGBA', (14, 9)); g = ImageDraw.Draw(im)
    for cx, cy, r in ((3, 5, 3), (7, 4, 3), (11, 4, 2)): g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx('#F4F8FF', 220))
    return outline(im)

def thermo():   # 체온계 (7 × 14)
    im = Image.new('RGBA', (7, 14)); g = ImageDraw.Draw(im)
    g.rounded_rectangle([2, 0, 4, 10], radius=1, fill=hx('#F4F4F8')); g.ellipse([1, 9, 5, 13], fill=hx('#E8303A')); g.rectangle([3, 4, 3, 10], fill=hx('#E8303A'))
    return outline(im)

def overlay(sym):   # 증상 덧그림: 얼굴 위는 아주 살짝만 (줄 · 띠 없이)
    im = Image.new('RGBA', (20, 14)); g = ImageDraw.Draw(im)
    if sym == 'fever':   # 빨간 볼
        for x in (2, 15): g.ellipse([x, 7, x + 3, 9], fill=hx('#F07070', 170))
    elif sym == 'nose':   # 콧물 방울
        g.ellipse([10, 8, 12, 11], fill=hx('#BFE8FF', 230)); im.putpixel((11, 8), hx('#FFFFFF'))
    return im

def bubble(sym):   # 머리 위 증상 말풍선 (16 × 15): 이걸 보고 증상을 골라요
    im = Image.new('RGBA', (16, 15)); g = ImageDraw.Draw(im)
    g.rounded_rectangle([0, 0, 15, 11], radius=4, fill=hx('#FFFFFF'), outline=OL); g.polygon([(5, 11), (7, 14), (8, 11)], fill=hx('#FFFFFF'), outline=OL); g.line([(6, 11), (7, 11)], fill=hx('#FFFFFF'))
    if sym == 'fever':   # 불꽃
        g.polygon([(8, 2), (5, 7), (6, 9), (10, 9), (11, 7)], fill=hx('#F06A3A')); g.polygon([(8, 5), (7, 8), (9, 8)], fill=hx('#FFD24A'))
    elif sym == 'throat':   # 콜록 (기침 구름 세 개)
        for cx in (4, 8, 12): g.ellipse([cx - 2, 4, cx + 1, 7], fill=hx('#B8B0C8'))
    elif sym == 'nose':   # 에취 (튀는 물방울)
        for x, y in ((4, 4), (8, 3), (12, 5), (6, 7), (10, 7)): g.ellipse([x - 1, y - 1, x, y], fill=hx('#7FC8F0'))
    elif sym == 'chill':   # 눈송이
        for dx, dy in ((0, 0), (-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)): im.putpixel((8 + dx, 5 + dy), hx('#6A9AE8'))
    return im

def shiver(h):   # 오한일 때 몸 양옆 떨림 표시 (세로 h)
    im = Image.new('RGBA', (4, h))
    for y in range(2, h - 2, 4): im.putpixel((1, y), hx('#9ABCF0')); im.putpixel((2, y + 1), hx('#9ABCF0'))
    return im

def chart():   # 진료 수첩 (24 × 28)
    im = Image.new('RGBA', (24, 28)); g = ImageDraw.Draw(im)
    g.rectangle([1, 1, 22, 26], fill=hx('#F4F0E8'), outline=OL); g.rectangle([1, 1, 22, 6], fill=hx('#E8303A'), outline=OL)
    g.rectangle([10, 2, 13, 5], fill=hx('#FFFFFF')); g.rectangle([9, 3, 14, 4], fill=hx('#FFFFFF'))
    for y in (10, 14, 18, 22): g.line([(4, y), (19, y)], fill=hx('#B8B0C8')); im.putpixel((4, y - 1), hx('#5AA040'))
    return im

def cabinet():   # 가구 작은 약장 (22 × 30)
    im = Image.new('RGBA', (22, 30)); g = ImageDraw.Draw(im)
    g.rectangle([1, 1, 20, 28], fill=hx('#F2EEE8'), outline=OL); g.rectangle([3, 3, 18, 13], fill=hx('#C8E4F0'), outline=OL); g.rectangle([3, 16, 18, 26], fill=hx('#E8E2DA'), outline=OL)
    for x, c in ((5, '#8ADCF0'), (9, '#F2B040'), (13, '#9ADC7A'), (16, '#F08A4A')): g.rectangle([x, 8, x + 1, 12], fill=hx(c))
    g.rectangle([9, 0, 12, 1], fill=hx('#E8303A')); g.rectangle([10, 19, 11, 22], fill=OL)
    return im

def blanket():   # 가구 양호실 담요 (28 × 16)
    im = Image.new('RGBA', (28, 16)); g = ImageDraw.Draw(im)
    g.polygon([(2, 8), (14, 2), (26, 8), (14, 14)], fill=hx('#9AB8E8'), outline=OL)
    for k in range(3): g.line([(6 + k * 4, 6 + k * 2), (18 + k * 4, 0 + k * 2 + 6)], fill=hx('#F4F4F8'))
    g.rectangle([12, 6, 15, 9], fill=hx('#E8303A')); g.rectangle([13, 5, 14, 10], fill=hx('#E8303A'))
    return im

if __name__ == '__main__':
    K = ['fever', 'throat', 'nose', 'chill']
    S = Image.new('RGBA', (32 * 4, 32))
    for i, k in enumerate(K): S.alpha_composite(bottle(k), (i * 32, 0))
    S.save(O + '/potions.png'); breath().save(O + '/breath.png'); thermo().save(O + '/thermo.png'); chart().save(O + '/chart.png'); cabinet().save(O + '/cabinet.png'); blanket().save(O + '/blanket.png')
    npcs = Image.open(ROOT + '/public/art/npcs.png').convert('RGBA')
    P = Image.new('RGBA', (240, 150), hx('#1E1830'))
    for i, k in enumerate(K): P.alpha_composite(bottle(k), (8 + i * 40, 6))
    FACE = { 0: (13, 14, 31), 2: (20, 16, 28), 14: (21, 27, 21), 16: (16, 15, 30) }   # index.html NPC_FACE (x, y, 크기)
    for i, (row, k) in enumerate(((2, 'fever'), (14, 'throat'), (0, 'nose'), (16, 'chill'))):   # 캇파 열 · 도도 목감기 · 나비 콧물 · 본 오한
        fr = npcs.crop((0, row * 64, 64, row * 64 + 64)); x0 = 4 + i * 58; P.alpha_composite(fr, (x0, 44)); fx, fy, fs = FACE[row]
        P.alpha_composite(overlay(k), (x0 + fx + fs // 2 - 10, 44 + fy + int(fs * .35))); P.alpha_composite(breath(), (x0 + fx + fs - 2, 44 + fy + fs // 2))
        P.alpha_composite(bubble(k), (x0 + fx + fs // 2 - 8, 44 + max(0, fy - 16)))
        if k == 'chill': P.alpha_composite(shiver(20), (x0 + fx - 6, 44 + fy + fs // 2)); P.alpha_composite(shiver(20), (x0 + fx + fs + 2, 44 + fy + fs // 2))
    P.alpha_composite(chart(), (10, 114)); P.alpha_composite(cabinet(), (50, 112)); P.alpha_composite(blanket(), (90, 124))
    P.resize((P.width * 4, P.height * 4), Image.NEAREST).save(O + '/preview.png')
    print('ok')
