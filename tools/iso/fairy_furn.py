# 요정 시장 요정 가구 3종 (시안): 방 가구(furniture.py)와 같은 아이소 그림체
#   python3 fairy_furn.py → out/fairy_furn.png (한 줄) + out/fairy_furn.json + out/fairy_furn_preview.png (이름 붙인 미리보기)
import json, math, os
from interiors import Room, hexc, shade
from furniture import bx, C, ell, H
from PIL import Image, ImageDraw, ImageFont

def glow(img, x, y, r, c, a=90):   # 둥근 빛 (가운데가 진하고 바깥으로 옅게)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay); cc = hexc(c)
    for k in range(r, 0, -1): g.ellipse([x - k, y - k, x + k, y + k], fill=(cc[0], cc[1], cc[2], int(a * (1 - k / r) ** 1.6)))
    img.alpha_composite(lay)
def sparkle(d, x, y, c='#FFE070'):
    for dx, dy in ((0, -2), (0, -1), (-1, 0), (-2, 0), (0, 0), (1, 0), (2, 0), (0, 1), (0, 2)): d.point((x + dx, y + dy), fill=H(c))
    d.point((x, y), fill=H('#FFFFFF'))
def honey_lamp(R, img, d):      # 꿀단지 등불 (미엘): 나무 받침 위 호박빛 꿀단지, 뚜껑에 꽃, 옆에 꿀 국자
    x, y = C(R, 1.5, 1.5); bx(R, img, 1.2, 1.2, .6, .6, 9, '#8A5A34', top='#A8744A')
    glow(img, x, y - 20, 14, '#FFC060', 110); d = ImageDraw.Draw(img)
    ell(d, x, y - 17, 8, 7, '#C8801C'); ell(d, x, y - 18, 7, 6, '#F0A830'); ell(d, x - 2, y - 20, 3, 2.5, '#FFD878'); d.point((x - 3, y - 21), fill=H('#FFFFFF'))
    d.rectangle([x - 5, y - 25, x + 5, y - 23], fill=H('#E8D0A0')); d.line([(x - 5, y - 23), (x + 5, y - 23)], fill=H('#A88050'))   # 천 뚜껑 + 끈
    for dx, dy, c in ((-3, -27, '#FFF0F6'), (0, -28, '#FFB0D0'), (3, -27, '#FFF0F6')): ell(d, x + dx, y + dy, 1.6, 1.6, c)
    d.point((x, y - 28), fill=H('#FFE070'))
    d.line([(x - 6, y - 13), (x - 6, y - 10)], fill=H('#E8A030')); d.point((x - 6, y - 9), fill=H('#F0B040'))   # 흘러내린 꿀
    d.line([(x + 8, y - 22), (x + 11, y - 12)], fill=H('#6A4424')); ell(d, x + 11, y - 11, 2, 1.5, '#8A5A34')   # 꿀 국자
    sparkle(d, x + 6, y - 31, '#FFE070'); sparkle(d, x - 8, y - 26, '#FFF0B0')
def dew_jar(R, img, d):          # 이슬 유리병 램프 (로웬): 이끼 낀 돌 위 키 큰 유리병, 안에 떠다니는 이슬방울
    x, y = C(R, 1.5, 1.5); ell(d, x, y - 2, 9, 4.5, '#5A6070'); ell(d, x, y - 3, 8, 3.5, '#7A8090'); ell(d, x - 3, y - 4, 4, 1.5, '#5A9A60'); ell(d, x + 4, y - 3, 2.5, 1, '#4A8A50')
    glow(img, x, y - 18, 15, '#90D8FF', 120); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x - 6, y - 28, x + 6, y - 5], 4, fill=(190, 230, 250, 120), outline=H('#A8D8F0'))
    for dx, dy, r, c in ((-2, -10, 2, '#C8F0FF'), (2, -15, 1.6, '#90D8FF'), (-1, -20, 1.4, '#E0FAFF'), (3, -9, 1.2, '#B0E8FF'), (0, -24, 1, '#FFFFFF')): ell(d, x + dx, y + dy, r, r, c)
    d.line([(x - 4, y - 25), (x - 4, y - 9)], fill=(255, 255, 255, 150))
    d.rectangle([x - 4, y - 31, x + 4, y - 28], fill=H('#8A6A48'))   # 코르크
    d.polygon([(x, y - 31), (x - 8, y - 36), (x - 2, y - 33)], fill=H('#3A9A7A')); d.polygon([(x, y - 31), (x + 7, y - 37), (x + 2, y - 33)], fill=H('#5ABA94'))   # 잎사귀 모자
    d.point((x + 7, y - 37), fill=H('#C8F0FF'))
def thorn_arch(R, img, d):       # 가시 장미 아치 (시슬): 덩굴 아치에 장미와 분홍 등불 둘
    x0, y0 = C(R, 1.1, 1.9); x1, y1 = C(R, 2.9, 1.1)
    for (x, y) in ((x0, y0 - 2), (x1, y1 - 2)): d.rectangle([x - 1, y - 22, x + 1, y], fill=H('#3A5A32')); d.line([(x - 1, y - 22), (x - 1, y)], fill=H('#2A4224'))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 2
    for t in range(0, 61):
        a = t / 60 * math.pi; x = x0 + (x1 - x0) * t / 60; y = y0 + (y1 - y0) * t / 60 - 2 - 22 - 9 * math.sin(a)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=H('#3A5A32'))
        if t % 6 == 0: d.point((x + (1 if t % 12 else -1), y - 2), fill=H('#6A8A4A'))
    for t in (6, 15, 24, 33, 42, 51, 58):
        a = t / 60 * math.pi; x = x0 + (x1 - x0) * t / 60; y = y0 + (y1 - y0) * t / 60 - 2 - 22 - 9 * math.sin(a)
        c = ('#C02858', '#E04878', '#8A1A40')[t % 3]; ell(d, x, y, 2.2, 2, c); d.point((x, y - 1), fill=H('#FF90B8'))
    for (x, y) in ((x0, y0 - 2), (x1, y1 - 2)):
        for k in range(3): ell(d, x + (1 if k % 2 else -1) * 2, y - 5 - k * 6, 1.6, 1.4, '#E04878')
    for (x, y) in ((x0 + 6, y0 - 22), (x1 - 6, y1 - 22)):
        glow(img, int(x), int(y + 6), 9, '#E070C0', 110); d = ImageDraw.Draw(img)
        d.line([(x, y), (x, y + 3)], fill=H('#3A2034')); d.rectangle([x - 2, y + 3, x + 2, y + 8], fill=H('#F0A0D8')); d.point((x, y + 5), fill=H('#FFFFFF'))
    sparkle(d, int(mx), int(my - 36), '#FFB0E0')

ITEMS = [   # id, 이름, 그림, 칸(가로, 세로), 주는 요정
  ('fy_honey', '꿀단지 등불', honey_lamp, (1, 1), '미엘'), ('fy_dew', '이슬 유리병 램프', dew_jar, (1, 1), '로웬'), ('fy_arch', '가시 장미 아치', thorn_arch, (2, 1), '시슬')]

def main():
    sprites, meta = [], []
    for fid, name, draw, (w, dd), who in ITEMS:
        R = Room(6, 6, 60); R.obj(fid, [(1, 1)], lambda img, d, draw=draw: draw(R, img, d))
        o = R.objs[-1]; ax, ay = R.P(1, 1)
        sprites.append(o['img']); meta.append(dict(id=fid, name=name, cat='요정', fairy=who, w=w, d=dd, solid=1, flat=0, sw=o['img'].width, sh=o['img'].height, ax=round(ax - o['x']), ay=round(ay - o['y'])))
    W = sum(s.width + 1 for s in sprites); Hh = max(s.height for s in sprites)
    sheet = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0
    for s, m in zip(sprites, meta): sheet.paste(s, (x, Hh - s.height)); m['sx'] = x; m['ay'] += Hh - s.height; m['sh'] = Hh; x += s.width + 1
    sheet.save('out/fairy_furn.png'); json.dump(meta, open('out/fairy_furn.json', 'w'), ensure_ascii=False)
    S, CW, CH, cols = 5, 260, 330, 3
    pv = Image.new('RGB', (CW * cols, CH + 60), hexc('#2A1E3A')); dr = ImageDraw.Draw(pv)
    fb = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf'
    F = ImageFont.truetype(fb, 16) if os.path.exists(fb) else ImageFont.load_default(); F2 = ImageFont.truetype(fb, 13) if os.path.exists(fb) else F
    dr.text((20, 18), '요정 가구 시안 · 요정 시장에서만 받을 수 있어요', font=F, fill=hexc('#FFE9A0'))
    for i, (s, m) in enumerate(zip(sprites, meta)):
        cx, cy = i * CW + CW // 2, 60
        dr.rounded_rectangle([cx - CW // 2 + 8, cy + 4, cx + CW // 2 - 8, cy + CH - 8], 14, fill=hexc('#3A2C52'))
        ty = cy + 200 - (m['w'] - 1) * 20; w_, d_ = m['w'], m['d']; cx -= (w_ - d_) * 20
        dr.polygon([(cx, ty), (cx + 40 * w_, ty + 20 * w_), (cx + 40 * w_ - 40 * d_, ty + 20 * w_ + 20 * d_), (cx - 40 * d_, ty + 20 * d_)], fill=hexc('#5A4A78'))
        big = s.resize((s.width * S, s.height * S), Image.NEAREST); ax, ay = m['ax'], m['ay'] - (Hh - s.height)
        pv.paste(big, (cx - ax * S, ty - ay * S), big)
        cx = i * CW + CW // 2
        dr.text((cx, cy + CH - 44), m['name'], font=F2, fill=hexc('#F1E9FF'), anchor='mm'); dr.text((cx, cy + CH - 24), f"{m['fairy']}의 선물", font=F2, fill=hexc('#D8B4FF'), anchor='mm')
    pv.save('out/fairy_furn_preview.png'); print('fairy furn', len(meta), sheet.size, pv.size)
if __name__ == '__main__': main()
