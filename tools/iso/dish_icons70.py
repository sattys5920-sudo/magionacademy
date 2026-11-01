#!/usr/bin/env python3
# 새 요리 29종 그림 (32×32 · dish_icons.py와 같은 도구 상자 · 같은 화풍) → public/art/dishes.png 뒤에 붙여요 (기존 58칸 + 29칸 = 87칸)
#   python3 tools/iso/dish_icons70.py [--preview 폴더]
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dish_icons import *   # Cv · R · H · ell · rect · poly · bowl · plate · cookie · steam · sparkle · 공용 색
import dish_icons as DI
BASE = 58   # 기존 칸 수 (일반 41 + 할로윈 17)
def top(c, pts, col):
    for x, y in pts: c.px(x, y, col)
# ---------- 공용 틀 ----------
def t_bowl(c, food, toppings=(), band=None, rim=WHT, hot=True):
    f = R(food); im, bm = bowl(c, 15.5, 13, 13, 5, 14, rim, rim, f, band=band, bandy=(19, 22) if band else None)
    c.shade(im, [f[1], f[2], f[3]], bias=-.1)
    for x, y, col in toppings: c.px(x, y, H(col) if isinstance(col, str) else col)
    if hot: steam(c, 11, 2, 8, ph=0); steam(c, 17, 1, 8, ph=2.4)
def t_cup(c, liquid, cupc=WHT, hot=True, deco=()):
    body = rect(7, 11, 22, 25) | ell(14.5, 25, 7.5, 2.4); c.vshade(body, [cupc[1], cupc[2], cupc[3]])
    h = (ell(25, 17, 4, 4.5) - ell(25, 17, 2, 2.6)) - rect(0, 0, 22, 31); c.fill(h, cupc[2])
    lq = ell(14.5, 11, 7.5, 2.4); L = R(liquid); c.fill(lq, L[2]); c.fill({p for p in lq if p[1] <= 10}, L[1])
    c.fill(ell(14.5, 28, 11, 2.2), WHT[3]); c.fill(ell(14.5, 27.6, 10, 1.6), WHT[1])
    for x, y, col in deco: c.px(x, y, H(col))
    if hot: steam(c, 11, 1, 7, ph=0); steam(c, 17, 1, 7, ph=2.4)
def t_bottle(c, liquid, label=None, bubbles=True):
    g = R('#d8ecf8'); L = R(liquid)
    neck = rect(13, 3, 17, 9); c.vshade(neck, [g[1], g[2], g[3]]); c.fill(rect(12, 2, 18, 3), H('#a8743a'))
    body = rect(9, 10, 21, 28) | ell(15, 10, 6, 2); c.vshade(body, [L[1], L[2], L[3]])
    c.fill(rect(10, 12, 11, 25), L[0])
    if label: c.fill(rect(10, 17, 20, 22), H(label)); c.fill(rect(10, 17, 20, 17), WHITE)
    if bubbles: [c.px(x, y, WHITE) for x, y in ((13, 14), (17, 20), (14, 25), (18, 13))]
    c.fill(ell(15, 29, 8, 1.6), WHT[3])
def t_plate(c, inner=None):
    return plate(c, 15.5, 21, 14.5, 8, WHT, inner=R(inner) if inner else None)
def t_cookies(c, dough, chips=(), deco=None):
    d = R(dough); cookie(c, 13.5, 21, 12.5, 6, 3, d, chips=chips or [(7, 21), (17, 24), (12, 25), (21, 20)], cracks=[(9, 19), (19, 22)])
    cookie(c, 14.5, 13, 9, 4.6, 3, d, chips=[(11, 11), (16, 14), (8, 14)], cracks=[(12, 15)])
    if deco: deco(c)
    sparkle(c, 26, 6, True)
def t_cake(c, sponge, cream, topc, fruit=None):
    S_ = R(sponge); C_ = R(cream)
    side = rect(5, 13, 26, 26); c.vshade(side, [S_[1], S_[2], S_[3]]); c.fill(rect(5, 18, 26, 19), C_[2]); c.fill(rect(5, 24, 26, 24), S_[4])
    topm = ell(15.5, 13, 10.5, 3.6); c.fill(topm, C_[1]); c.fill({p for p in topm if p[1] >= 15}, C_[2])
    for x in range(6, 26, 3): c.px(x, 16, C_[1]); c.px(x, 17, C_[1])
    c.fill(ell(15.5, 28, 13, 2.4), WHT[3]); c.fill(ell(15.5, 27.4, 12, 1.8), WHT[1])
    if fruit: F_ = R(fruit); [c.fill(circ(x, 11, 1.8), F_[2]) or c.px(x - 1, 10, F_[0]) for x in (10, 15, 20)]
    if topc: c.pts([(15, 6), (15, 7), (16, 7), (15, 8)], H(topc))
def t_parfait(c, layers, topc):
    gl = R('#e4f0fa')
    cup = poly([(7, 6), (24, 6), (20, 22), (11, 22)]); c.fill(cup, gl[1])
    ys = [7, 11, 15, 19]
    for i, col in enumerate(layers): L = R(col); c.fill({p for p in cup if ys[i] <= p[1] < ys[i] + 4}, L[2]); c.fill({p for p in cup if p[1] == ys[i]}, L[1])
    c.fill(rect(9, 7, 10, 20) & cup, gl[0])
    c.fill(rect(14, 22, 17, 26), gl[2]); c.fill(ell(15.5, 27.5, 6, 1.6), gl[3])
    T_ = R(topc); c.fill(circ(15.5, 4, 3), T_[2]); c.px(14, 3, T_[0]); c.pts([(16, 0), (17, 0), (17, 1)], DGREEN[2])
def t_jelly(c, col, dots=None):
    J = R(col); m = ell(15.5, 17, 9, 8) | rect(7, 17, 24, 23); m = {p for p in m if p[1] >= 9}
    c.shade(m, [J[0], J[1], J[2], J[3]]); c.fill(rect(10, 12, 11, 18), WHITE)
    if dots: [c.px(x, y, H(dots)) for x, y in ((14, 14), (19, 17), (16, 20), (21, 13))]
    c.fill(ell(15.5, 25.5, 13, 2.6), WHT[3]); c.fill(ell(15.5, 25, 12, 2), WHT[1])
def t_skewer(c, pieces):
    c.fill(line(4, 28, 27, 5), H('#c8a070')); c.fill(line(4, 29, 27, 6), H('#8a6a40'))
    for i, col in enumerate(pieces):
        P_ = R(col); cx, cy = 9 + i * 5.2, 23.5 - i * 5.2; m = circ(cx, cy, 3.3); c.shade(m, [P_[1], P_[2], P_[3]]); c.px(int(cx) - 1, int(cy) - 1, P_[0])
def t_bread(c, crust, deco=None):
    B = R(crust); m = ell(15.5, 18, 12, 7.5); c.shade(m, [B[0], B[1], B[2], B[3]])
    for x0 in (9, 14, 19): c.fill(line(x0, 14, x0 + 3, 12), B[3])
    if deco: deco(c)
    c.fill(ell(15.5, 26.5, 13, 2), WHT[3])
def t_toast(c, spread, deco=None):
    T_ = R('#e8c080'); m = rect(6, 8, 25, 24) | ell(15.5, 8, 9.5, 4); c.fill(m, T_[3]); inner = rect(8, 9, 23, 22) | ell(15.5, 9, 7.5, 3); c.shade(inner, [T_[0], T_[1], T_[2]])
    S_ = R(spread); sp = ell(15.5, 15, 6.5, 5); c.shade(sp, [S_[1], S_[2], S_[3]])
    if deco: deco(c)
    c.fill(ell(15.5, 27, 13, 2), WHT[3])
def t_muffin(c, top_, paper):
    P_ = R(paper); cupm = poly([(8, 16), (23, 16), (21, 27), (10, 27)]); c.vshade(cupm, [P_[1], P_[2], P_[3]])
    for x in range(10, 22, 3): c.fill(line(x, 17, x, 26), P_[3])
    T_ = R(top_); m = ell(15.5, 13, 9, 6.5); m = {p for p in m if p[1] <= 17}; c.shade(m, [T_[0], T_[1], T_[2], T_[3]])
def t_mochi(c, col, dot):
    M = R(col)
    for cx, cy in ((10, 20), (21, 20), (15.5, 13)):
        m = ell(cx, cy, 6, 4.6); c.shade(m, [M[0], M[1], M[2], M[3]]); c.px(int(cx) - 2, int(cy) - 1, WHITE); c.px(int(cx) + 1, int(cy), H(dot))
    c.fill(ell(15.5, 27, 13, 2), WHT[3])
def t_steak(c, meat, garnish):
    t_plate(c); M = R(meat); m = ell(14, 19, 9, 5); c.shade(m, [M[1], M[2], M[3], M[4]])
    for x in (9, 13, 17): c.fill(line(x, 21, x + 3, 16), M[4])
    G = R(garnish); c.fill(circ(23, 16, 2.4), G[2]); c.px(22, 15, G[0]); c.fill(circ(24, 21, 2), DGREEN[1])
def t_pot(c, stew, bits=()):
    P_ = R('#4a4a5a'); body = below(ell(15.5, 14, 13, 12), 14); c.shade(body, [P_[1], P_[2], P_[3], P_[4]])
    rim = ell(15.5, 14, 13, 4); c.fill(rim, P_[1]); S_ = R(stew); im = ell(15.5, 14.4, 11, 2.8); c.shade(im, [S_[1], S_[2], S_[3]])
    for x, y, col in bits: c.px(x, y, H(col))
    c.fill(rect(1, 13, 3, 15), P_[3]); c.fill(rect(28, 13, 30, 15), P_[3]); steam(c, 11, 1, 8); steam(c, 18, 0, 8, ph=2)
def t_pie(c, filling, lattice='#f0d090'):
    P_ = R('#e8b870'); m = ell(15.5, 18, 13, 7); c.fill(m, P_[3]); F_ = R(filling); im = ell(15.5, 17, 11, 5.5); c.shade(im, [F_[1], F_[2], F_[3]])
    L = H(lattice); [c.fill(line(x, 12, x + 4, 22) & im, L) for x in (7, 12, 17)]; [c.fill(line(x, 22, x + 4, 12) & im, L) for x in (8, 13, 18)]
    c.fill(edge(m), P_[1]); c.fill(ell(15.5, 26, 13, 2), WHT[3])
def t_fry(c, col, n=3):
    t_plate(c, '#f4ead8'); F_ = R(col)
    for i in range(n):
        cx, cy = 9 + i * 6.5, 20 - (i % 2) * 2; m = ell(cx, cy, 4, 2.4); c.shade(m, [F_[0], F_[1], F_[2], F_[3]]); c.px(int(cx) + 3, int(cy) - 1, F_[3]); c.px(int(cx) - 1, int(cy) - 1, WHITE)
    c.fill(circ(24, 15, 1.8), YEL[1])
def t_salad(c, greens, accents):
    t_plate(c); G = R(greens)
    for i, (x, y) in enumerate(((10, 18), (14, 16), (18, 18), (13, 21), (19, 21), (16, 19))): c.fill(ell(x, y, 3.4, 2.2), G[1 + i % 3])
    for i, (x, y) in enumerate(((11, 16), (17, 15), (20, 20), (14, 22), (9, 21))): c.fill(circ(x, y, 1.3), H(accents[i % len(accents)]))
# ---------- 새 요리 29종 (DISH_LIST 뒤에 붙는 순서) ----------
NEW = [
 ('박하 소다', lambda c: t_bottle(c, '#8ae8c0', label='#3aa878')),
 ('민들레 솜털 차', lambda c: t_cup(c, '#f4d870', deco=[(9, 8, '#ffffff'), (21, 7, '#ffffff'), (15, 6, '#fff6d0')])),
 ('딸기 우유', lambda c: t_bottle(c, '#ffb8cc', label='#e8486a', bubbles=False)),
 ('당근 수프', lambda c: t_bowl(c, '#f09a3a', [(11, 13, '#ffffff'), (14, 12, '#ffffff'), (19, 13, '#5fae4a'), (18, 12, '#5fae4a')], band=ORANGE)),
 ('완두콩 죽', lambda c: t_bowl(c, '#b8d87a', [(x, y, '#6ab84a') for x, y in ((11, 13), (14, 12), (17, 14), (19, 12), (13, 15))])),
 ('해바라기씨 강정', lambda c: t_cookies(c, '#e8b858', chips=[(7, 21), (17, 24), (12, 25), (21, 20)])),
 ('카모마일 컵케이크', lambda c: (t_muffin(c, '#fff4d8', '#9ad8a8'), c.fill(circ(15.5, 8, 2.2), YEL[1]), [c.px(x, y, WHITE) for x, y in ((13, 8), (18, 8), (15, 6), (15, 10))])),
 ('호두 빵', lambda c: t_bread(c, '#b8783a', deco=lambda c: [c.fill(circ(x, y, 1.4), H('#7a4a26')) for x, y in ((11, 18), (16, 20), (20, 17))])),
 ('단풍 시럽 토스트', lambda c: t_toast(c, '#c8602a', deco=lambda c: c.pts([(14, 13), (15, 12), (16, 13), (15, 14), (13, 14), (17, 14)], H('#ff8a3a')))),
 ('대나무 통밥', lambda c: (c.vshade(rect(6, 12, 25, 25), [H('#9ad86a'), H('#6ab84a'), H('#3a8a3a')]), c.fill(rect(6, 18, 25, 18), H('#2a6a2a')), c.fill(ell(15.5, 12, 9.5, 3), H('#fff6e0')), [c.px(x, 11, H('#7ac85a')) for x in (12, 16, 19)], c.fill(ell(15.5, 27, 12, 2), WHT[3]), steam(c, 13, 2, 8), steam(c, 19, 1, 8, ph=2))),
 ('촛불 빙어 튀김', lambda c: t_fry(c, '#f0c060')),
 ('구름 게 크로켓', lambda c: (t_fry(c, '#d8904a', 3), [c.px(x, y, H('#ff9a8a')) for x, y in ((9, 19), (15, 17), (22, 19))])),
 ('라벤더 쿠키', lambda c: t_cookies(c, '#e0c8f0', chips=[(7, 21), (17, 24), (12, 25), (21, 20)], deco=lambda c: [c.px(x, y, H('#9a6ad8')) for x, y in ((11, 12), (17, 13), (14, 21))])),
 ('옥수수 버터빵', lambda c: t_bread(c, '#f0c040', deco=lambda c: (c.fill(rect(13, 13, 18, 15), H('#fff6c0')), [c.px(x, y, H('#ffe070')) for x, y in ((9, 19), (21, 19), (12, 22))]))),
 ('인삼 꿀차', lambda c: t_cup(c, '#e0a040', cupc=R('#c8a070'), deco=[(14, 9, '#fff6d0')])),
 ('튤립 꽃잎 샐러드', lambda c: t_salad(c, '#7ac85a', ['#ff7aa8', '#ffd060', '#ff5a7a'])),
 ('마법 문어 볶음', lambda c: t_pot(c, '#c84a8a', [(x, y, '#ff8ac8') for x, y in ((11, 14), (15, 13), (19, 14), (13, 15))] + [(17, 15, '#e8302a')])),
 ('등불 새우 꼬치', lambda c: (t_skewer(c, ['#ff8a5a', '#ffd060', '#ff8a5a', '#ffd060']), sparkle(c, 25, 4))),
 ('알로에 젤리', lambda c: t_jelly(c, '#b8f0c0', dots='#5ab86a')),
 ('선인장 에이드', lambda c: t_bottle(c, '#9ae86a', label='#ff7aa8')),
 ('눈송이 꽃 셔벗', lambda c: t_parfait(c, ['#f4faff', '#cfe6ff', '#f4faff', '#a8d0f8'], '#ffffff')),
 ('구름 목화 팬케이크', lambda c: (t_cake(c, '#f0c880', '#ffffff', None), c.fill(ell(15.5, 9, 5, 2), H('#ffffff')), c.fill(ell(13, 8, 3, 1.6), H('#f4f6ff')))),
 ('반딧불 꽃가루 소다', lambda c: (t_bottle(c, '#e8f070', label='#3a6a3a'), sparkle(c, 6, 8), sparkle(c, 25, 14))),
 ('오로라 연어 스테이크', lambda c: t_steak(c, '#ff9a7a', '#ffd060')),
 ('종꽃 찹쌀떡', lambda c: t_mochi(c, '#e8f0ff', '#8ab8f0')),
 ('꿈꽃 타르트', lambda c: (t_pie(c, '#b89aff', '#fff0ff'), sparkle(c, 25, 6, True))),
 ('서리 딸기 케이크', lambda c: t_cake(c, '#ffe8f0', '#ffffff', '#5fae4a', fruit='#e8304a')),
 ('별빛 청새치 스테이크', lambda c: (t_steak(c, '#5a7ac8', '#ffe070'), sparkle(c, 8, 9, True))),
 ('바다 포도 파르페', lambda c: t_parfait(c, ['#8ad8f0', '#ffffff', '#5ab8e8', '#c8f0ff'], '#3aa8a8')),
]
def build():
    old = Image.open(DI.OUT).convert('RGBA'); assert old.width >= BASE * S, old.size
    sheet = Image.new('RGBA', (S * (BASE + len(NEW)), S), (0, 0, 0, 0)); sheet.alpha_composite(old.crop((0, 0, BASE * S, S)), (0, 0))
    for i, (nm, f) in enumerate(NEW): cv = Cv(); f(cv); sheet.alpha_composite(cv.render(), ((BASE + i) * S, 0))
    return sheet
if __name__ == '__main__':
    sh = build(); sh.save(DI.OUT); print('dishes.png', sh.size)
    if '--preview' in sys.argv:
        d = sys.argv[sys.argv.index('--preview') + 1]; os.makedirs(d, exist_ok=True); Z = 4; cols = 6
        F = ImageFont.truetype('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/Galmuri11-Bold.ttf', 12)
        pv = Image.new('RGBA', (cols * 150, math.ceil(len(NEW) / cols) * 160), (0x21, 0x17, 0x33, 255)); dr = ImageDraw.Draw(pv)
        for i, (nm, f) in enumerate(NEW):
            x, y = (i % cols) * 150, (i // cols) * 160; pv.alpha_composite(sh.crop(((BASE + i) * S, 0, (BASE + i) * S + S, S)).resize((S * Z, S * Z), Image.NEAREST), (x + 11, y + 6)); dr.text((x + 75, y + 146), nm, font=F, fill=(255, 243, 200), anchor='mm')
        pv.save(os.path.join(d, 'dishes_new29.png'))
