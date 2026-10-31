# 무슈 블랑 특별 요리 보상 가구 4종 (시안): 방 가구(furniture.py)·요정 가구와 같은 아이소 그림체
#   python3 blanc_furn.py → out/blanc_furn.png (한 줄) + out/blanc_furn.json + out/blanc_furn_preview.png (이름 붙인 미리보기)
import json, math, os
from interiors import Room, hexc, shade
from furniture import bx, C, ell, H
from fairy_furn import glow, sparkle
from PIL import Image, ImageDraw, ImageFont

def cauldron_counter(R, img, d):   # 블랑의 대솥 조리대 (마녀의 대솥 스튜): 돌 조리대 위 큰 무쇠 솥, 초록 스튜가 보글보글, 국자, 김
    bx(R, img, 1.05, 1.1, 1.9, .8, 9, '#6A5A54', top='#8A7A70'); d = ImageDraw.Draw(img)
    x0, y0 = C(R, 1.05, 1.9); x1, y1 = C(R, 2.95, 1.1)
    for k in (3, 6): d.line([(x0 + 1, y0 - k), (x0 + 15, y0 - k - 7)], fill=H('#54463F'))   # 벽돌 줄
    for (x, y) in ((x0 + 5, y0 - 2), (x0 + 11, y0 - 5)): d.line([(x, y), (x, y - 3)], fill=H('#54463F'))
    d.rectangle([x0 + 5, y0 - 8, x0 + 9, y0 - 5], fill=H('#E07028')); d.point((x0 + 7, y0 - 7), fill=H('#FFD060'))   # 불 구멍
    x, y = C(R, 2, 1.5, 9); glow(img, x, y - 8, 10, '#9AF07A', 70); d = ImageDraw.Draw(img)
    ell(d, x, y - 4, 7, 5, '#1E1A22'); ell(d, x - 2, y - 5, 3, 2, '#3A3440'); ell(d, x, y - 8, 6.5, 2.4, '#2A2430'); ell(d, x, y - 8, 5.6, 1.9, '#5AC83A'); ell(d, x - 2, y - 8.5, 2, .8, '#9AF07A')
    for dx, dy in ((-3, -8), (2, -9)): d.point((x + dx, y + dy), fill=H('#C8FFB0'))
    d.line([(x + 3, y - 8), (x + 7, y - 16)], fill=H('#8A5A34')); ell(d, x + 7, y - 17, 1.2, 1, '#A8744A')   # 국자
    for k, (dx, dy) in enumerate(((-3, -13), (-1, -16), (-3, -19))): ell(d, x + dx, y + dy, 2 - k * .3, 1.6 - k * .3, '#E8F0E8')   # 김
    for dx in (-5, 5): d.point((x + dx, y), fill=H('#1E1A22'))   # 솥 다리
    sparkle(d, x - 8, y - 19, '#C8FFB0')
def mirror_ball(R, img, d):        # 유령 파티 미러볼 (유령 파티 푸딩): 검은 받침대에 매달린 미러볼, 바닥에 빛 조각, 꼬마 유령
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 1, 6, 3, '#2A2434'); ell(d, x, y - 2, 5, 2.4, '#4A4458')
    d.line([(x, y - 2), (x, y - 34)], fill=H('#3A3448')); d.line([(x + 1, y - 2), (x + 1, y - 34)], fill=H('#5A5468')); d.line([(x, y - 34), (x + 7, y - 34)], fill=H('#3A3448')); d.line([(x + 7, y - 34), (x + 7, y - 30)], fill=H('#8A8498'))
    bxc, byc = x + 7, y - 25; glow(img, bxc, byc, 13, '#FFFFFF', 70); d = ImageDraw.Draw(img)
    ell(d, bxc, byc, 6, 6, '#6A6A80'); ell(d, bxc, byc, 5, 5, '#B8B8CC')
    for gy in range(-4, 5, 2):
        for gx in range(-4, 5, 2):
            if gx * gx + gy * gy <= 20: d.point((bxc + gx, byc + gy), fill=H(('#FFFFFF', '#8A8AA0', '#E0E0F0')[(gx + gy) % 3]))
    d.point((bxc - 2, byc - 3), fill=H('#FFFFFF')); d.point((bxc - 3, byc - 2), fill=H('#FFFFFF'))
    for dx, dy, c in ((-9, 0, '#FF6AA0'), (8, 2, '#6AE8FF'), (-4, 4, '#FFE860'), (11, -2, '#9AF07A'), (2, 5, '#C88AFF')): d.rectangle([x + dx, y + dy - 1, x + dx + 1, y + dy], fill=H(c))   # 바닥 빛 조각
    gx, gy = x - 7, y - 12; ell(d, gx, gy, 3.5, 4, '#F0F4FF'); d.rectangle([gx - 3, gy, gx + 3, gy + 4], fill=H('#F0F4FF')); d.point((gx - 1, gy - 1), fill=H('#1A1428')); d.point((gx + 1, gy - 1), fill=H('#1A1428')); d.point((gx, gy + 1), fill=H('#FFA0C0'))
    sparkle(d, bxc + 8, byc - 6, '#FFFFFF')
def red_candelabra(R, img, d):     # 백작의 붉은 촛대 (뱀파이어 만찬 젤리): 붉은 벨벳 받침, 금빛 세 갈래 촛대, 촛불 셋, 꼭대기 박쥐 장식
    bx(R, img, 1.2, 1.2, .6, .6, 5, '#8A1A2A', top='#B02A3A'); d = ImageDraw.Draw(img)
    x, y = C(R, 1.5, 1.5, 5); d.line([(x, y), (x, y - 18)], fill=H('#C8902A')); d.line([(x + 1, y), (x + 1, y - 18)], fill=H('#FFD060')); ell(d, x, y - 2, 3, 1.5, '#C8902A')
    d.line([(x - 7, y - 14), (x + 8, y - 14)], fill=H('#C8902A')); d.line([(x - 7, y - 14), (x - 7, y - 18)], fill=H('#C8902A')); d.line([(x + 8, y - 14), (x + 8, y - 18)], fill=H('#C8902A'))
    for cx, top in ((x - 7, y - 23), (x + 1, y - 27), (x + 8, y - 23)):
        glow(img, cx, top - 3, 8, '#FFB040', 100); d = ImageDraw.Draw(img)
        d.rectangle([cx - 1, top, cx + 1, top + 5], fill=H('#F4ECD8')); d.point((cx - 1, top), fill=H('#FFFFFF')); d.point((cx + 1, top + 4), fill=H('#C8C0A8'))
        d.point((cx, top - 1), fill=H('#3A2A20')); ell(d, cx, top - 3, 1.2, 2, '#FF9A2A'); d.point((cx, top - 3), fill=H('#FFF0A0'))
    bxx, byy = x + 1, y - 32; d.line([(bxx, byy + 2), (bxx, byy + 4)], fill=H('#C8902A'))
    for k in (-1, 1): d.polygon([(bxx + k, byy - 1), (bxx + k * 6, byy - 3), (bxx + k * 5, byy), (bxx + k * 4, byy - 1), (bxx + k * 3, byy + 1)], fill=H('#3A2A5A'))
    ell(d, bxx, byy, 1.5, 1.5, '#5A3A7A'); d.point((bxx - 1, byy - 2), fill=H('#5A3A7A')); d.point((bxx + 1, byy - 2), fill=H('#5A3A7A')); d.point((bxx, byy), fill=H('#FF4A5A'))
def apple_cart(R, img, d):         # 사탕 사과 수레 (잭의 사탕 사과): 나무 수레, 줄무늬 차양, 막대 꽂은 사탕 사과
    bx(R, img, 1.15, 1.2, 1.7, .6, 7, '#9A6A3A', top='#B88450', lift=3); d = ImageDraw.Draw(img)
    for tx, ty in ((1.3, 1.8), (2.7, 1.1)):
        x, y = C(R, tx, ty); ell(d, x, y - 2, 3.5, 3.5, '#4A2E18'); ell(d, x, y - 2, 2.5, 2.5, '#8A5A30'); d.point((x, y - 2), fill=H('#2A1A0C'))
    x0, y0 = C(R, 1.15, 1.8, 10); x1, y1 = C(R, 2.85, 1.2, 10)
    for (x, y) in ((x0 + 1, y0), (x1 - 1, y1)): d.line([(x, y), (x, y - 16)], fill=H('#6A4424'))
    for k in range(6):   # 줄무늬 차양 (위로 볼록)
        t0, t1 = k / 6, (k + 1) / 6; ax0, ay0 = x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0 - 17; ax1, ay1 = x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1 - 17
        d.polygon([(ax0, ay0), (ax1, ay1), (ax1, ay1 - 6), (ax0, ay0 - 6)], fill=H('#FF7A2A' if k % 2 else '#FFF4E0'))
        d.polygon([(ax0, ay0), (ax1, ay1), ((ax0 + ax1) / 2, (ay0 + ay1) / 2 + 3)], fill=H('#E8601A' if k % 2 else '#E8DCC8'))
    d.line([(x0, y0 - 23), (x1, y1 - 23)], fill=H('#8A3A10'))
    for i, (tx, ty, c) in enumerate(((1.45, 1.55, '#D8202A'), (1.85, 1.45, '#5AC83A'), (2.25, 1.35, '#D8202A'), (2.65, 1.25, '#5AC83A'), (1.65, 1.75, '#5AC83A'), (2.05, 1.65, '#D8202A'))):
        x, y = C(R, tx, ty, 11); d.line([(x, y - 3), (x, y - 7)], fill=H('#E8D0A0')); ell(d, x, y, 2.6, 2.4, shade(hexc(c), .7)); ell(d, x - .4, y - .4, 2.1, 1.9, c); d.point((x - 1, y - 1), fill=H('#FFFFFF'))
    sparkle(d, int(x1) - 2, int(y1) - 30, '#FFE070')

ITEMS = [   # id, 이름, 그림, 칸(가로, 세로), 받는 요리
  ('bl_cauldron', '블랑의 대솥 조리대', cauldron_counter, (2, 1), '마녀의 대솥 스튜'), ('bl_mirror', '유령 파티 미러볼', mirror_ball, (1, 1), '유령 파티 푸딩'),
  ('bl_candle', '백작의 붉은 촛대', red_candelabra, (1, 1), '뱀파이어 만찬 젤리'), ('bl_cart', '사탕 사과 수레', apple_cart, (2, 1), '잭의 사탕 사과')]

def main():
    sprites, meta = [], []
    for fid, name, draw, (w, dd), dish in ITEMS:
        R = Room(6, 6, 60); R.obj(fid, [(1, 1)], lambda img, d, draw=draw: draw(R, img, d))
        o = R.objs[-1]; ax, ay = R.P(1, 1)
        sprites.append(o['img']); meta.append(dict(id=fid, name=name, cat='블랑', dish=dish, w=w, d=dd, solid=1, flat=0, sw=o['img'].width, sh=o['img'].height, ax=round(ax - o['x']), ay=round(ay - o['y'])))
    W = sum(s.width + 1 for s in sprites); Hh = max(s.height for s in sprites)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
    for s, m in zip(sprites, meta): sheet.paste(s, (x, Hh - s.height)); m['sx'] = x; m['ay'] += Hh - s.height; m['sh'] = Hh; x += s.width + 1
    sheet.save('out/blanc_furn.png'); json.dump(meta, open('out/blanc_furn.json', 'w'), ensure_ascii=False)
    S, CW, CH, cols = 5, 260, 330, 4
    pv = Image.new('RGB', (CW * cols, CH + 60), hexc('#2A1E3A')); dr = ImageDraw.Draw(pv)
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 16); F2 = ImageFont.truetype(fb, 13)
    dr.text((20, 18), '무슈 블랑 보상 가구 시안 · 특별 요리를 처음 가져다주면 받아요', font=F, fill=hexc('#FFE9A0'))
    for i, (s, m) in enumerate(zip(sprites, meta)):
        cx, cy = i * CW + CW // 2, 60
        dr.rounded_rectangle([cx - CW // 2 + 8, cy + 4, cx + CW // 2 - 8, cy + CH - 8], 14, fill=hexc('#3A2C52'))
        ty = cy + 200 - (m['w'] - 1) * 20; w_, d_ = m['w'], m['d']; cx -= (w_ - d_) * 20
        dr.polygon([(cx, ty), (cx + 40 * w_, ty + 20 * w_), (cx + 40 * w_ - 40 * d_, ty + 20 * w_ + 20 * d_), (cx - 40 * d_, ty + 20 * d_)], fill=hexc('#5A4A78'))
        big = s.resize((s.width * S, s.height * S), Image.NEAREST); ax, ay = m['ax'], m['ay'] - (Hh - s.height)
        pv.paste(big, (cx - ax * S, ty - ay * S), big)
        cx = i * CW + CW // 2
        dr.text((cx, cy + CH - 44), m['name'], font=F2, fill=hexc('#F1E9FF'), anchor='mm'); dr.text((cx, cy + CH - 24), f"「{m['dish']}」", font=F2, fill=hexc('#D8B4FF'), anchor='mm')
    pv.save('out/blanc_furn_preview.png'); print('blanc furn', len(meta), sheet.size, pv.size)
if __name__ == '__main__': main()
