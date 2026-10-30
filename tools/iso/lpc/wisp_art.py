# 사역마 시안 4: 정령불(혼불) 12종 · 색과 모양이 조금씩 다른 둥둥 떠다니는 불꽃 · 동물 NPC와 같은 단계 음영 + 외곽선 + 은은한 빛
#   python3 wisp_art.py <미리보기.png> [글꼴] → tools/iso/out/wisps.png (64칸 × 12)
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
def hx(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])
N = 64
YY, XX = np.mgrid[0:N, 0:N] + .5
def tongue(cx, base, top, r, sway=0, p=1.6):   # 아래는 둥글고 위로 가늘어지는 불꽃 혀 하나 → 안쪽 깊이(0~1)
    out = np.zeros((N, N))
    for y in range(N):
        yc = y + .5
        if yc > base + r or yc < top: continue
        if yc >= base: w = r * math.sqrt(max(0, 1 - ((yc - base) / r) ** 2))
        else: t = (base - yc) / (base - top); w = r * (1 - t) ** p
        x0 = cx + sway * ((base - yc) / max(1, base - top)) ** 2
        if w <= .3: continue
        d = 1 - np.abs(XX[y] - x0) / w; out[y] = np.maximum(out[y], np.clip(d, 0, 1) * min(1, w / r + .3))
    return out
def ball(cx, cy, r):
    d = 1 - np.hypot(XX - cx, YY - cy) / r; return np.clip(d, 0, 1)
def paint(depth, ramp, glow, eyes=None, rim=None):
    R = [hx(c) for c in ramp]; m = depth > 0
    lvl = np.clip((depth * 5.2).astype(int) + 1, 1, 5)
    img = np.zeros((N, N, 4), np.uint8)
    for k in range(1, 6): img[(lvl == k) & m, :3] = R[k]
    img[m, 3] = 255
    # 빛: 왼쪽 위가 한 단계 밝게
    lit = m & (XX - YY * .4 < np.median(XX[m] - YY[m] * .4) - 3) & (lvl < 5); img[lit, :3] = np.array([R[min(5, l + 1)] for l in lvl[lit]])
    e = m.copy(); e[1:] &= m[:-1]; e[:-1] &= m[1:]; e[:, 1:] &= m[:, :-1]; e[:, :-1] &= m[:, 1:]
    edge = m & ~e; img[edge, :3] = R[1] if rim is None else hx(rim)
    d = m.copy(); d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    out = d & ~m; img[out, :3] = R[0]; img[out, 3] = 255
    g1 = out.copy(); g1[1:] |= out[:-1]; g1[:-1] |= out[1:]; g1[:, 1:] |= out[:, :-1]; g1[:, :-1] |= out[:, 1:]; g1 &= ~(d)
    img[g1, :3] = hx(glow); img[g1, 3] = 90
    if eyes:
        for (x, y) in eyes: img[y:y + 2, x, :3] = R[0]; img[y:y + 2, x, 3] = 255
    return img
def embers(img, pts, c):
    for x, y in pts:
        img[y, x, :3] = hx(c); img[y, x, 3] = 255
    return img
def ramp(*c): return list(c)
BLUE = ramp('#0A1A3A', '#1A3A7A', '#2A62C8', '#4A90F0', '#8AC4FF', '#E4F4FF')
PURP = ramp('#1A0A30', '#3A1A6A', '#6A34B8', '#9A5AE8', '#C89AFF', '#F2E4FF')
GREEN = ramp('#06200E', '#0E4A22', '#1E8A3A', '#3EC85A', '#8AF08A', '#E4FFE0')
PINK = ramp('#3A0A22', '#7A1A4A', '#C83A82', '#F06AAE', '#FFA8D2', '#FFE8F4')
GOLD = ramp('#3A2406', '#7A4E0A', '#C88A14', '#F2B82A', '#FFE070', '#FFFCE0')
SILV = ramp('#1E2230', '#3E4458', '#707A94', '#A4B0C8', '#D4DCEC', '#FFFFFF')
RED = ramp('#300606', '#6A0E0E', '#B42018', '#E8482A', '#FF8A5A', '#FFE0C0')
TEAL = ramp('#04262A', '#0A4A52', '#148A90', '#2EC4C0', '#7AF0E4', '#E0FFFA')
ORNG = ramp('#341404', '#6E2A06', '#B4520E', '#EE7E1E', '#FFB45A', '#FFF0C8')
NAVY = ramp('#060A24', '#121A4E', '#24308A', '#3E52C2', '#7C90EE', '#DCE4FF')
DARK = ramp('#000000', '#0C0614', '#1E1030', '#34204E', '#54387A', '#8A6AC0')
def w1():   # 푸른 혼불: 고전적인 물방울 불꽃, 끝이 살랑 휘어요
    return paint(tongue(32, 38, 8, 11, -6), BLUE, '#6AA8FF', eyes=[(28, 37), (35, 37)])
def w2():   # 보라 쌍꼬리불
    d = np.maximum(tongue(30, 38, 10, 10, -8), tongue(36, 38, 14, 8, 8)); return paint(d, PURP, '#B07AFF', eyes=[(29, 38), (35, 38)])
def w3():   # 초록 도깨비불: 작은 불꽃 셋이 흔들
    d = np.maximum.reduce([tongue(32, 40, 12, 10, 2), tongue(24, 42, 22, 6, -6), tongue(40, 42, 20, 6, 6)]); return embers(paint(d, GREEN, '#6AE87A', eyes=[(29, 40), (35, 40)]), [(16, 30), (48, 26), (20, 18)], '#C8FFB0')
def w4():   # 분홍 꽃불: 꽃잎처럼 갈라진 불꽃 머리
    d = np.maximum.reduce([ball(32, 40, 10)] + [tongue(32 + dx, 36, 14 + abs(dx), 5, dx * .6) for dx in (-9, -4.5, 0, 4.5, 9)]); return paint(d, PINK, '#FF8AC8', eyes=[(29, 40), (35, 40)])
def w5():   # 금빛 왕관불: 끝이 셋으로 반듯하게
    d = np.maximum.reduce([ball(32, 40, 13), tongue(32, 34, 8, 7, 0, 1.3), tongue(22, 36, 18, 5, -3, 1.3), tongue(42, 36, 18, 5, 3, 1.3)]); return embers(paint(d, GOLD, '#FFD860', eyes=[(29, 40), (35, 40)]), [(32, 4), (20, 8), (44, 8)], '#FFFCE0')
def w6():   # 은빛 달불: 초승달처럼 휜 불꽃
    d = np.clip(ball(32, 34, 15) - np.clip(ball(39, 29, 13) * 3, 0, 1), 0, 1); d = np.maximum(d, tongue(26, 44, 36, 5, 0) * .6); return paint(d, SILV, '#D4E0FF', eyes=[(24, 36), (29, 38)])
def w7():   # 붉은 잉걸불: 동그란 불씨 + 작은 불꽃, 튀는 불티
    d = np.maximum(ball(32, 40, 11), tongue(32, 34, 16, 6, 3)); return embers(paint(d, RED, '#FF7A4A', eyes=[(29, 40), (35, 40)]), [(18, 22), (46, 18), (50, 32), (14, 36), (40, 10)], '#FFC080')
def w8():   # 청록 물불: 아래가 넓고 둥근 물방울, 위에 작은 물결
    d = np.maximum(tongue(32, 36, 10, 13, 0, 2.2), ball(32, 40, 12)); return embers(paint(d, TEAL, '#6AE8E0', eyes=[(29, 39), (35, 39)]), [(20, 52), (44, 54)], '#E0FFFA')
def w9():   # 주황 등불: 작은 등롱 틀 안에서 타는 불
    d = tongue(32, 40, 18, 8, -3); img = paint(d, ORNG, '#FFAA50', eyes=[(29, 40), (34, 40)])
    frame = hx('#3A2A20'); hi = hx('#8A6A50')
    for y in range(14, 52): img[y, 21, :3] = frame; img[y, 43, :3] = frame; img[y, 21, 3] = img[y, 43, 3] = 255
    for x in range(20, 45): img[13, x, :3] = frame; img[52, x, :3] = frame; img[14, x, :3] = hi; img[13, x, 3] = img[52, x, 3] = img[14, x, 3] = 255
    for y in range(6, 13): img[y, 32, :3] = frame; img[y, 32, 3] = 255
    return img
def w10():   # 남색 별불: 별 모양 심지 불꽃
    img = paint(tongue(32, 38, 8, 12, 5), NAVY, '#8AA0FF', eyes=[(29, 40), (35, 40)])
    for x, y in [(32, 27), (31, 28), (32, 28), (33, 28), (30, 29), (31, 29), (32, 29), (33, 29), (34, 29), (31, 30), (32, 30), (33, 30), (31, 31), (33, 31), (30, 32), (34, 32)]: img[y, x, :3] = hx('#FFFFFF')
    return embers(img, [(12, 14), (52, 12), (50, 50), (14, 52), (46, 24)], '#FFFFFF')
def w11():   # 그림자불: 검은 불꽃, 보라 테두리, 너덜너덜한 끝
    d = np.maximum.reduce([tongue(32, 40, 8, 11, 4), tongue(24, 40, 16, 6, -10), tongue(40, 40, 18, 6, 10), tongue(30, 44, 26, 5, -14)]); img = paint(d * .55, DARK, '#9A6AE8', eyes=None, rim='#9A6AE8')
    for x, y in [(28, 36), (35, 36)]: img[y:y + 2, x:x + 2, :3] = hx('#E8D0FF')
    return img
def w12():   # 무지갯불: 겹겹이 다른 색 고리
    d = tongue(32, 40, 8, 12, -4); img = paint(d, PURP, '#FFFFFF', eyes=[(29, 40), (35, 40)])
    cols = ['#FF6A6A', '#FFB050', '#FFE070', '#7AE07A', '#6AB8FF', '#B08AFF']; m = d > 0
    for k, c in enumerate(cols):
        band = m & (d > k / 6.2) & (d <= (k + 1) / 6.2); img[band, :3] = hx(c)
    return img
WS = [('푸른 혼불', '청운', w1), ('보라 쌍꼬리불', '자운', w2), ('초록 도깨비불', '도롱', w3), ('분홍 꽃불', '연화', w4), ('금빛 왕관불', '휘황', w5), ('은빛 달불', '월영', w6),
      ('붉은 잉걸불', '단화', w7), ('청록 물불', '수련', w8), ('주황 등불', '등롱', w9), ('남색 별불', '성휘', w10), ('그림자불', '묵영', w11), ('무지갯불', '채운', w12)]
if __name__ == '__main__':
    cells = [f() for _, _, f in WS]
    Image.fromarray(np.concatenate(cells, axis=1)).save(os.path.join(HERE, '..', 'out', 'wisps.png'))
    if len(sys.argv) > 1:
        fnt = sys.argv[2] if len(sys.argv) > 2 else None; F = ImageFont.truetype(fnt, 15) if fnt else None; F2 = ImageFont.truetype(fnt, 12) if fnt else None
        cw, ch, cols = 230, 250, 4; pv = Image.new('RGB', (cw * cols + 20, ch * 3 + 60), (18, 14, 28)); d = ImageDraw.Draw(pv)
        d.text((20, 20), '사역마 시안 4 · 정령불 12종', font=F, fill=(255, 233, 160))
        for i, (n, nm, _) in enumerate(WS):
            x = (i % cols) * cw + 20; y = (i // cols) * ch + 54
            d.rounded_rectangle([x, y, x + cw - 14, y + ch - 14], 14, fill=(30, 22, 46), outline=(90, 70, 140), width=2)
            im = Image.fromarray(cells[i]).resize((192, 192), Image.NEAREST); pv.paste(im, (x + (cw - 14 - 192) // 2, y + 4), im)
            d.text((x + (cw - 14) // 2, y + 206), nm, font=F, fill=(241, 233, 255), anchor='mm'); d.text((x + (cw - 14) // 2, y + 226), n, font=F2, fill=(200, 180, 240), anchor='mm')
        pv.save(sys.argv[1])
