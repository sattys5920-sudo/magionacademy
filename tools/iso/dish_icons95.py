#!/usr/bin/env python3
# 늦가을·첫겨울 새 요리 25종 그림 (32×32 · dish_icons.py / dish_icons70.py 와 같은 도구 상자 · 같은 화풍)
#   python3 tools/iso/dish_icons95.py --preview DIR   시안만 DIR에 저장 (dish_new25.png 800×32, dish_new25_x4_lbl.png, dish_cmp_x4.png)
#   python3 tools/iso/dish_icons95.py --apply         public/art/dishes.png 앞 87칸 + 새 25칸 = 112칸(3584×32)으로 저장
# 순서 = tools/dex2_spec.json 의 "dish" 순서
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dish_icons import *      # Cv · R · H · ell · rect · poly · bowl · plate · cookie · steam · sparkle · 공용 색
from dish_icons70 import t_bowl, t_cup, t_bottle, t_plate, t_cookies, t_cake, t_parfait, t_jelly, t_skewer, t_bread, t_muffin, t_steak, t_pot, t_pie, t_fry, t_salad
import dish_icons as DI
BASE = 87   # 기존 칸 수 (일반 41 + 할로윈 17 + 봄여름 29)

# ---------- 작은 부품 ----------
def yuzu_slice(c, x, y, r=2.6):
    m = circ(x, y, r); c.fill(m, H('#f0b818')); c.fill(circ(x, y, r - 1), H('#ffe878'))
    c.px(round(x), round(y), H('#fff6c8')); c.pts([(round(x) - 1, round(y)), (round(x) + 1, round(y)), (round(x), round(y) - 1), (round(x), round(y) + 1)], H('#ffd040'))
def chestnut(c, x, y):
    c.fill(ell(x, y, 2.4, 2), H('#7a3e1e')); c.fill(ell(x, y + .4, 1.6, 1.2), H('#f0c868')); c.px(int(x) - 1, int(y) - 1, H('#b8703a'))
def lantern(c, x, y, r=2.2):
    """꽈리 한 알 (주황 열매 + 얇은 갈색 꽃받침)"""
    b = circ(x, y, r); c.shade(b, [H('#ffb860'), H('#ff8a1a'), H('#d85a10')], lx=.5, ly=.6); c.px(round(x) - 1, round(y) - 1, H('#fff0c0'))
    c.pts([(round(x) - 1, round(y - r) - 1), (round(x), round(y - r)), (round(x) + 1, round(y - r) - 1)], H('#c8a060'))
def snowdrop(c, x, y):
    """설강화: 고개 숙인 흰 종꽃"""
    c.px(x, y - 2, H('#5fae4a')); c.px(x + 1, y - 2, H('#5fae4a'))
    c.pts([(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y)], WHITE); c.px(x, y + 1, H('#cfe6c8')); c.px(x + 1, y, H('#d8d4ec'))
def crystal(c, x, y, col='#9ad8ff', fx=False):
    """얼음 결정 (작은 십자 별)"""
    put = c.fxp if fx else c.px
    put(x, y, WHITE)
    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)): put(x + a, y + b, H(col))
    for a, b in ((2, 0), (-2, 0), (0, 2), (0, -2)): put(x + a, y + b, H('#5aa8e8'))
def marsh(c, x, y, col='#ffb0d0'):
    m = rect(x, y, x + 2, y + 1); c.fill(m, H(col)); c.px(x, y, H('#fff0f6'))
def scallion(c, x, y): c.px(x, y, H('#7ac85a')); c.px(x + 1, y, H('#3f8a3a'))
def glass_cup(c, x0, y0, x1, y1, liquid, ly):
    """속이 비치는 큰 유리잔. ly 아래가 음료"""
    g = R('#e4f0fa'); L = R(liquid)
    body = rect(x0, y0, x1, y1); c.fill(body, g[1])
    lq = rect(x0 + 1, ly, x1 - 1, y1 - 1); c.vshade(lq, [L[1], L[2], L[3]]); c.fill(rect(x0 + 1, ly, x1 - 1, ly), L[0])
    c.fill(rect(x0 + 1, y0 + 1, x0 + 1, y1 - 2), WHITE)
    c.fill(rect(x0, y1, x1, y1), g[2])
    c.fill(ell((x0 + x1) / 2, y1 + 2, (x1 - x0) / 2 + 3, 1.6), WHT[3])

# ---------- 25종 ----------
def d_rosehiptea(c):
    t_cup(c, '#c8302a', deco=[(12, 10, '#ff8a6a'), (17, 11, '#ff8a6a')])
    for x, y in ((4, 25), (7, 26)):
        b = ell(x, y, 1.8, 1.6); c.shade(b, [H('#ff6a4a'), H('#d8302a'), H('#9a1a2a')]); c.px(x - 1, y - 1, H('#ffc0a8'))
    c.pts([(5, 23), (6, 22)], DGREEN[1])

def d_hawthorncandy(c):
    t_skewer(c, ['#e8202a', '#e8202a', '#e8202a', '#e8202a'])
    for i in range(4):
        cx, cy = int(9 + i * 5.2), int(23.5 - i * 5.2)
        c.px(cx - 2, cy - 1, WHITE); c.px(cx + 1, cy + 2, H('#ff8a8a')); c.px(cx + 2, cy - 2, H('#ffd0d0'))
    sparkle(c, 24, 25); sparkle(c, 6, 9); c.fxp(28, 16, H('#fff6c0'))

def d_leafloachsoup(c):
    t_bowl(c, '#e0782a', [(15, 15, '#5fae4a'), (16, 15, '#5fae4a'), (9, 14, '#5fae4a'), (13, 11, '#e8302a'), (20, 15, '#e8302a')],
           band=R('#e8a050'), rim=R('#8a5a3a'))
    # 미꾸라지 두 마리 (가늘고 길게)
    for pts in (((9, 12), (10, 12), (11, 13), (12, 13), (13, 13), (14, 12)), ((15, 14), (16, 13), (17, 13), (18, 13), (19, 14), (20, 14))):
        c.pts(pts, H('#5a3a1e')); c.px(pts[-1][0], pts[-1][1] - 1, H('#8a6a3a')); c.px(pts[0][0], pts[0][1] - 1, H('#8a6a3a'))
    # 단풍잎 한 장
    c.art(19, 9, ['..r..', 'r.r.r', 'rrRrr', '.rrr.', '..d..'], {'r': H('#ff4a1a'), 'R': H('#ffa040'), 'd': H('#a83a1a')})

def d_frostcarpstew(c):
    t_plate(c, '#e8d8b8')
    fish(c, 15, 19.5, 20, 7, R('#a8b8cc'), belly=R('#e8eef6'), fin=R('#8a9ab8'), d=1)
    for x, y in ((10, 18), (13, 17), (17, 18)): c.px(x, y, H('#ff7a4a'))
    for x, y in ((8, 23), (22, 23), (12, 24)): c.px(x, y, H('#d8502a'))
    c.pts([(19, 16), (20, 16)], H('#5fae4a')); c.pts([(11, 16), (12, 16)], H('#f0d070'))
    crystal(c, 26, 12, fx=True); steam(c, 12, 4, 11, ph=0); steam(c, 18, 3, 11, ph=2.4)

def d_yuzutea(c):
    t_cup(c, '#f4c020', cupc=R('#d8ecc8'), deco=[(11, 11, '#ffe878'), (12, 11, '#ffe878'), (17, 10, '#e89a10'), (18, 11, '#e89a10')])
    yuzu_slice(c, 4, 24, 2.6)

def d_frostberrymuffin(c):
    t_muffin(c, '#e8b868', '#b8a0e0')
    for x, y in ((11, 11), (15, 9), (19, 12), (13, 14), (18, 15), (10, 15), (21, 14), (16, 12)):
        c.px(x, y, H('#6a2a9a')); c.px(x + 1, y, H('#9a5ad0'))
    for x, y in ((13, 8), (17, 8), (12, 10), (20, 10)): c.px(x, y, WHITE)
    sparkle(c, 26, 6)

def d_crabchestsoup(c):
    t_bowl(c, '#f0dcae', [(11, 12, '#e8503a'), (12, 12, '#e8503a'), (18, 14, '#e8503a'), (19, 14, '#ff8a6a'), (15, 11, '#5fae4a'), (14, 15, '#5fae4a')], band=R('#c8602a'))
    chestnut(c, 11, 14); chestnut(c, 21, 15)
    # 게 집게발 하나
    c.art(15, 8, ['.rr.r', 'rRr.r', 'rRRrr', '.rRr.', '..rr.'], {'r': H('#d8302a'), 'R': H('#ff7a5a')})

def d_mistsmeltfry(c):
    # 대바구니 + 종이 + 가느다란 빙어 튀김 세 마리
    B = R('#c8904a'); bm = ell(15.5, 21, 14, 7.5); c.fill(below(ell(15.5, 22, 14, 7.5), 21), B[3]); c.fill(bm, B[2])
    for x, y in bm:
        if (x + y * 2) % 4 == 0: c.px(x, y, B[3])
    c.fill(edge(bm), B[1]); paper = poly([(5, 18), (26, 15), (25, 24), (7, 26)]); c.fill(paper & ell(15.5, 21, 12.5, 6.5), H('#f8f0dc'))
    F = R('#f0b850')
    for i, (y, x0) in enumerate(((16, 8), (20, 10), (24, 9))):
        m = ell(x0 + 6.5, y + .3, 7, 1.9); c.fill(shift(m, 0, 1) - m, F[4]); c.shade(m, [F[0], F[1], F[2], F[3]])
        c.pts([(x0 - 1, y), (x0 - 2, y - 1), (x0 - 3, y - 2), (x0 - 2, y + 1), (x0 - 3, y + 2)], H('#7a4a1a'))
        c.fill(rect(x0 + 10, y - 1, x0 + 10, y + 1), F[3]); c.px(x0 + 12, y, BLACK); c.px(x0 + 4, y - 1, WHITE); c.px(x0 + 7, y - 1, F[0])
    c.fill(ell(24, 23, 2.4, 1.8), YEL[1]); c.px(23, 22, YEL[0])
    steam(c, 6, 4, 10, amp=1, ph=1); steam(c, 25, 3, 10, amp=1, ph=3)

def d_icicleade(c):
    glass_cup(c, 9, 7, 22, 26, '#8ad0f4', 10)
    for x, y in ((11, 13), (16, 16), (12, 20), (17, 22)): c.fill(rect(x, y, x + 3, y + 2), H('#e8f8ff')); c.px(x + 3, y + 2, H('#a8d8f0'))
    for x, y in ((19, 12), (14, 24), (19, 19)): c.px(x, y, WHITE)
    # 고드름 빨대 + 박하잎
    c.fill(line(19, 1, 17, 11), H('#ffffff')); c.fill(line(20, 1, 18, 11), H('#a8d8f0'))
    c.pts([(10, 8), (11, 7), (12, 7), (11, 8), (12, 8), (13, 8)], H('#5fc86a')); c.px(13, 7, H('#2f8a3a'))
    sparkle(c, 25, 5)

def d_killiroll(c):
    t_plate(c)
    fill = ['#ffd040', '#5fae4a', '#ff8a3a', '#ff8ab0']
    for k, (x, y) in enumerate(((9.5, 19), (15.5, 17), (21.5, 19), (12.5, 23), (18.5, 23))):
        c.fill(circ(x, y, 3.2), H('#1e2a22')); c.fill(circ(x, y, 2.3), H('#fffaf0'))
        xi, yi = round(x), round(y)
        c.px(xi, yi, H(fill[k % 4])); c.px(xi - 1, yi, H(fill[(k + 1) % 4])); c.px(xi, yi - 1, H(fill[(k + 2) % 4])); c.px(xi + 1, yi, H(fill[(k + 3) % 4]))
        c.px(xi - 2, yi - 1, H('#e8e0d0'))
    # 목도리 줄무늬 리본
    c.pts([(25, 13), (26, 13), (27, 14), (26, 15)], H('#e8403a')); c.pts([(26, 14), (25, 14)], H('#fff0f0'))

def d_lanterntart(c):
    P = R('#e0a860'); sh = ell(15.5, 20, 13, 6.5); c.fill(below(ell(15.5, 22, 13, 6.5), 20), P[3])
    for x in range(4, 28, 2): c.fill(rect(x, 21, x, 26) & below(ell(15.5, 22, 13, 6.5), 20), P[4])
    c.fill(sh, P[1]); cream = ell(15.5, 19.6, 10.5, 4.6); c.shade(cream, [H('#fff8e0'), H('#fff0c0'), H('#f0d890')])
    for x, y in edge(sh):
        if x % 2 == 0: c.px(x, y, P[0])
    for x, y in ((10, 19), (15, 17), (21, 19), (13, 21), (18, 21)): lantern(c, x, y, 2.1)
    c.pts([(15, 12), (16, 12)], H('#5fae4a')); sparkle(c, 26, 9)

def d_yuzupuffsoup(c):
    t_bowl(c, '#f4ecc8', [(12, 13, '#ffffff'), (13, 13, '#ffffff'), (13, 14, '#e8e0d0'), (18, 15, '#ffffff'), (19, 15, '#e8e0d0'),
                           (16, 12, '#5fae4a'), (17, 12, '#7ac85a'), (10, 15, '#5fae4a'), (21, 12, '#5fae4a')],
           band=R('#5aa890'), rim=R('#c8e8d8'))
    yuzu_slice(c, 17, 14, 2.2)

def d_cocoaeel(c):
    t_plate(c)
    E = R('#9a5226')
    for k, (x0, y0) in enumerate(((5, 16), (8, 20), (7, 24))):
        m = poly([(x0, y0), (x0 + 17, y0 - 2), (x0 + 18, y0 + 2), (x0 + 1, y0 + 3)])
        c.fill(shift(m, 0, 1) - m, H('#4a2010')); c.shade(m, [E[0], E[1], E[2], E[3]])
        for t in (5, 10, 14): c.fill(line(x0 + t, y0 + 2, x0 + t + 1, y0 - 1) & m, E[4])
        c.fill(line(x0 + 1, y0 + 1, x0 + 16, y0 - 1) & m, H('#d8945a')); c.px(x0 + 3, y0, WHITE)
    for x, y in ((9, 17), (15, 19), (20, 18), (13, 23), (19, 22)): c.px(x, y, H('#fff0d0'))
    c.pts([(24, 25), (25, 25), (25, 24)], H('#ffa8b8')); c.pts([(23, 26), (24, 26)], H('#f08aa0'))
    steam(c, 12, 4, 11, ph=1); steam(c, 19, 3, 11, ph=3)

def d_snowflatbutter(c):
    t_plate(c, '#f4ead8')
    F = R('#e0a050'); body = ell(14, 20, 9, 5.5); fr = ell(14, 20, 10.5, 6.8)
    c.fill(fr, F[3])
    for x, y in edge(fr):
        if (x + y) % 2: c.px(x, y, F[2])
    c.shade(body, [F[0], F[1], F[2], F[3]])
    c.fill(poly([(23, 20), (27, 16), (28, 18), (27, 22), (28, 24), (27, 25)]), F[3])
    for x in (10, 13, 16): c.fill(line(x, 23, x + 3, 17) & body, F[3])
    c.px(9, 18, BLACK); c.px(10, 17, BLACK)
    # 버터 한 조각 + 허브
    c.fill(rect(13, 15, 17, 18), H('#fff0a0')); c.fill(rect(13, 15, 17, 15), H('#fffadc')); c.fill(rect(17, 16, 17, 18), H('#e8c860')); c.px(12, 19, H('#ffe080')); c.px(18, 19, H('#ffe080'))
    c.pts([(20, 18), (21, 17), (21, 18)], H('#5fae4a')); c.pts([(8, 21), (8, 22)], H('#5fae4a'))
    for x, y in ((6, 9), (25, 8), (15, 6)): c.fxp(x, y, WHITE)
    steam(c, 12, 3, 10, amp=1, ph=1)

def d_mistcappie(c):
    P = R('#e8b060'); m = ell(15.5, 19, 13, 7.5); c.fill(below(ell(15.5, 21, 13, 7.5), 19), P[3])
    c.shade(m, [P[0], P[1], P[2], P[3]])
    for x, y in edge(m):
        if (x + y) % 2 == 0: c.px(x, y, P[3])
    for x0 in (8, 21): c.fill(line(x0, 18, x0 + 2, 21), P[3])
    # 반죽 버섯 장식 (안개 버섯 = 청회색 갓)
    cap = above(ell(15.5, 16, 5.5, 4), 16); c.fill(ring(cap), H('#3a3050')); c.shade(cap, [H('#d8d8f0'), H('#a8a8d0'), H('#7a78a8')], lx=.5, ly=.7)
    c.fill(rect(14, 17, 17, 20), H('#f4e8d0')); c.fill(rect(17, 17, 17, 20), H('#d0b890')); c.px(14, 13, WHITE); c.px(17, 14, WHITE)
    for x, y in ((8, 22), (23, 21), (12, 24)): c.px(x, y, P[0])
    c.fill(ell(15.5, 28, 13, 1.8), WHT[3])
    steam(c, 7, 5, 12, amp=1, ph=0); steam(c, 23, 4, 12, amp=1, ph=2.4)

def d_frostshrimppasta(c):
    t_plate(c)
    P = R('#f4e0a0'); nest = ell(15.5, 20, 10, 5.5); c.shade(nest, [P[0], P[1], P[2], P[3]])
    for k in range(3):
        c.fill(ell(15.5, 20, 8 - k * 2.4, 4.3 - k * 1.3) - ell(15.5, 20, 7 - k * 2.4, 3.3 - k * 1.3), P[3])
    def shrimp(x, y, fl=1):
        S_ = R('#ff8a6a'); m = (circ(x, y, 2.6) - circ(x + fl, y - 1, 1.3)); c.shade(m, [S_[0], S_[1], S_[2], S_[3]]); c.px(x - fl * 2, y + 1, H('#e8402a'))
    shrimp(10, 18); shrimp(20, 18, -1); shrimp(15, 23)
    for x, y in ((13, 17), (18, 21), (11, 22), (21, 22)): c.px(x, y, H('#3f8a3a'))
    for x, y in ((14, 19), (17, 18)): c.px(x, y, H('#2a1c38'))
    crystal(c, 26, 12, fx=True); steam(c, 12, 4, 11, ph=0); steam(c, 18, 3, 11, ph=2.4)

def d_snowdropsalad(c):
    G = R('#6ab84a'); im, bm = bowl(c, 15.5, 15, 13, 5, 12, R('#c8a070'), R('#d8b080'), G)
    c.shade(im, [G[1], G[2], G[3]])
    for i, (x, y) in enumerate(((9, 13), (13, 11), (18, 11), (22, 13), (11, 15), (16, 14), (20, 15), (15, 9))):
        c.fill(ell(x, y, 3.2, 2.2), [G[0], G[1], G[2], DGREEN[1]][i % 4])
    for x, y in ((10, 12), (16, 9), (21, 12), (13, 15)): snowdrop(c, x, y)
    for x, y in ((18, 14), (8, 15), (23, 15)): c.fill(circ(x, y, 1.2), H('#6a3aa8')); c.px(x, y - 1, H('#c8a0ff'))

def d_candlerayskewer(c):
    t_skewer(c, ['#c87a3a', '#d89048', '#c87a3a', '#d89048'])
    for i in range(4):
        cx, cy = int(9 + i * 5.2), int(23.5 - i * 5.2)
        c.px(cx - 1, cy + 1, H('#5a2a14')); c.px(cx, cy, H('#5a2a14')); c.px(cx + 1, cy - 1, H('#5a2a14')); c.px(cx + 1, cy + 2, H('#e8302a'))
    # 촛불 불꽃 (끝에)
    c.fxp(28, 3, H('#ffd860')); c.fxp(28, 2, H('#fff6c0')); c.fxp(27, 4, H('#ff8a2a')); c.fxp(29, 4, H('#ff8a2a')); c.fxp(28, 4, H('#ffd860')); c.fxp(28, 1, H('#ff8a2a'))
    steam(c, 6, 4, 11, amp=1, ph=1); steam(c, 14, 2, 8, amp=1, ph=3); sparkle(c, 25, 24)

def d_squidsundae(c):
    # 나무 도마 위 썬 오징어 순대 + 초장
    W = R('#c89060'); bd = rect(3, 15, 28, 26); c.fill(rect(3, 27, 28, 27), W[4]); c.hshade(bd, [W[1], W[2], W[3]])
    for y in (18, 22): c.fill(rect(4, y, 27, y), W[3])
    for x, y in ((7.5, 19), (13, 20), (18.5, 21), (24, 20)):
        o = ell(x, y, 3.6, 4.2); c.fill(o, H('#f8e8f0')); c.fill({p for p in o if p[0] > x + 1}, H('#e0c0d8'))
        inn = ell(x, y, 2.4, 3); c.fill(inn, H('#e86a3a'))
        xi, yi = round(x), round(y)
        c.px(xi - 1, yi - 1, H('#fff6e0')); c.px(xi + 1, yi, H('#5fae4a')); c.px(xi, yi + 1, H('#fff6e0')); c.px(xi, yi - 2, H('#ffb040'))
    for x, y in ((8, 11), (12, 12)): b = circ(x, y, 2); c.shade(b, [H('#ffb860'), H('#ff8a1a'), H('#d85a10')]); c.px(x - 1, y - 1, H('#fff0c0'))
    c.pts([(9, 8), (10, 8), (10, 9), (11, 9)], DGREEN[1]); c.pts([(10, 10), (10, 9)], H('#c8a060'))
    d = ell(23, 11, 4, 2.2); c.fill(d, WHT[1]); c.fill(ell(23, 11, 2.6, 1.2), H('#e8302a'))

def d_owlcatstew(c):
    t_pot(c, '#b87838', [(10, 14, '#e8a060'), (20, 14, '#ff8a3a'), (14, 15, '#5fae4a'), (19, 15, '#5fae4a')])
    for x, y in ((12, 14), (17, 14)):
        cap = above(ell(x, y, 3, 2.4), y); c.fill(ring(cap), H('#3a1a0a')); c.shade(cap, [H('#d89a5a'), H('#a8683a'), H('#7a4422')]); c.px(x - 1, y - 1, H('#f0c890')); c.pts([(x, y + 1), (x - 1, y + 1)], H('#f0e8d0'))
    c.pts([(14, 13), (15, 13)], H('#d8c8a8'))
    # 부엉이 귀 손잡이
    for x0 in (1, 28): c.pts([(x0, 12), (x0 + 2, 12)], H('#6a6a7a')); c.px(x0 + (0 if x0 < 10 else 2), 11, H('#6a6a7a'))

def d_candycocoa(c):
    t_cup(c, '#7a4022', cupc=R('#e86a8a'), hot=True)
    c.fill(ell(14.5, 10, 6, 2.4), H('#fff6f0'))
    marsh(c, 10, 8); marsh(c, 15, 7, '#ff9ac0'); marsh(c, 18, 9); marsh(c, 13, 10, '#fff0f6')
    for x in (9, 14, 19): c.px(x, 18, H('#fff0f6')); c.px(x + 1, 17, H('#fff0f6'))

def d_frostbingsu(c):
    g = R('#c8e4f8')
    cup = poly([(5, 16), (27, 16), (23, 24), (9, 24)]); c.vshade(cup, [g[0], g[1], g[2], g[3]])
    c.fill(rect(13, 24, 18, 26), g[2]); c.fill(ell(15.5, 27, 7, 1.6), g[3])
    ice = above(ell(15.5, 16, 10.5, 11), 16); I = R('#f4faff')
    c.shade(ice, [WHITE, I[1], H('#d8ecfa'), H('#b8d8f0')], lx=.6, ly=.6)
    for x, y in ice:
        if (x * 3 + y * 5) % 7 == 0: c.px(x, y, H('#e8f4ff'))
    for x, y in ((9, 12), (11, 11), (13, 12), (16, 10), (18, 11), (20, 12), (22, 13)): c.px(x, y, H('#fff4c8'))
    crystal(c, 15, 5); crystal(c, 21, 9); c.px(10, 9, H('#9ad8ff')); c.px(11, 8, H('#5aa8e8'))
    c.fill(rect(6, 17, 26, 17) & cup, H('#ffe8a0'))
    sparkle(c, 26, 5); sparkle(c, 5, 10)

def d_stormoctobowl(c):
    im, bm = bowl(c, 15.5, 13, 13, 5, 14, R('#3a4a7a'), R('#5a6aa0'), R('#fffaf0'), band=R('#8ab8e8'), bandy=(19, 21))
    c.shade(im, [H('#fffaf0'), H('#f0ece0'), H('#d8d0c0')])
    for x, y in ((9, 13), (14, 11), (19, 12), (22, 14)): c.px(x, y, WHITE)
    O = R('#c8507a')
    for x, y in ((11, 12), (16, 13), (20, 11)):
        m = ell(x, y, 2.6, 1.8); c.shade(m, [O[0], O[1], O[2], O[3]]); c.px(x, y, H('#ffd0e0')); c.px(x - 1, y + 1, H('#ffd0e0'))
    for x, y in ((13, 15), (18, 15), (8, 13), (22, 12)): scallion(c, x, y)
    c.px(14, 13, H('#e8302a')); c.px(19, 14, H('#e8302a'))
    # 빗줄기 무늬 띠
    for x in range(8, 24, 3): c.px(x, 20, H('#e8f4ff')); c.px(x + 1, 21, H('#e8f4ff'))
    steam(c, 11, 2, 8, ph=0); steam(c, 17, 1, 8, ph=2.4)

def d_wintermarlin(c):
    pl = R('#3a4a78'); c.fill(ell(15.5, 22, 15, 8), pl[4]); o = ell(15.5, 21, 15, 8); c.fill(o, pl[1]); c.fill(edge(o), H('#c8e4ff'))
    inn = ell(15.5, 21, 12.5, 6); c.shade(inn, [pl[1], pl[2], pl[3]], bias=.2)
    M = R('#d87a5a'); st = poly([(6, 19), (12, 14), (22, 15), (25, 20), (19, 25), (9, 24)]); c.fill(ring(st), H('#5a2a1a'))
    c.shade(st, [M[0], M[1], M[2], M[3]])
    c.fill(rect(7, 23, 23, 25) & st, M[4])
    for k in range(4): c.fill(line(9 + k * 4, 22, 13 + k * 4, 15) & st, H('#6a2a1a'))
    for k in range(3): c.fill(line(9, 17 + k * 3, 23, 19 + k * 3) & st & rect(0, 0, 31, 22), H('#8a3a22'))
    crystal(c, 24, 13); crystal(c, 7, 13); c.px(26, 23, H('#9ad8ff')); c.px(27, 22, WHITE)
    c.fill(circ(26, 19, 1.6), H('#5fae4a'))
    sparkle(c, 27, 5, True); sparkle(c, 4, 6, True); sparkle(c, 15, 6)

def d_winterfeast(c):
    gd = R('#f2c13a')
    c.fill(ell(15.5, 23, 15.8, 8), gd[4]); o = ell(15.5, 22, 15.8, 8); c.shade(o, [gd[0], gd[1], gd[2], gd[3]], lx=.5, ly=.7)
    for x, y in edge(o):
        if (x + y) % 2 == 0: c.px(x, y, H('#fff0a0'))
    inn = ell(15.5, 22, 13, 5.8); c.shade(inn, [H('#a8c8f0'), H('#7aa0d8'), H('#5a7ab8')], bias=.2); c.fill(edge(inn), H('#ffe070'))
    fish(c, 14, 20.5, 20, 8, R('#f0a030'), belly=R('#fff0b0'), fin=R('#e8602a'), d=1, scales=True)
    crown(c, 12, 12, 7)
    yuzu_slice(c, 25, 24, 2.2); yuzu_slice(c, 6, 24, 2)
    cap = above(ell(23, 18, 2.4, 1.8), 18); c.fill(ring(cap), H('#3a3050')); c.fill(cap, H('#b8b8e0')); c.px(23, 19, H('#f0e8d0'))
    st = STAR5(6, 15, 3.2, 1.4); c.fill(ring(st), H('#7a4a0a')); c.fill(st, H('#ffe060')); c.px(6, 14, WHITE)
    sparkle(c, 4, 6, True); sparkle(c, 27, 7, True); sparkle(c, 21, 4); sparkle(c, 29, 15)

NEW = [
 ('찔레 열매 차', d_rosehiptea), ('산사 탕후루', d_hawthorncandy), ('낙엽 미꾸라지탕', d_leafloachsoup), ('서리 붕어찜', d_frostcarpstew),
 ('유자차', d_yuzutea), ('서리 머루 머핀', d_frostberrymuffin), ('군밤 게 수프', d_crabchestsoup), ('안개 빙어 튀김', d_mistsmeltfry),
 ('고드름 에이드', d_icicleade), ('목도리 송사리 김밥', d_killiroll), ('꽈리 타르트', d_lanterntart), ('유자 복어 맑은탕', d_yuzupuffsoup),
 ('코코아 장어구이', d_cocoaeel), ('눈송이 가자미 버터구이', d_snowflatbutter), ('안개 버섯 파이', d_mistcappie), ('서리 새우 크림 파스타', d_frostshrimppasta),
 ('설강화 샐러드', d_snowdropsalad), ('촛불 가오리 꼬치', d_candlerayskewer), ('꽈리 오징어 순대', d_squidsundae), ('부엉이 메기 스튜', d_owlcatstew),
 ('사탕 버섯 코코아', d_candycocoa), ('서리 결정 빙수', d_frostbingsu), ('빗줄기 문어 덮밥', d_stormoctobowl), ('겨울 청새치 스테이크', d_wintermarlin),
 ('겨울 잉어왕 정찬', d_winterfeast),
]

def strip():
    sh = Image.new('RGBA', (S * len(NEW), S), (0, 0, 0, 0))
    for i, (nm, f) in enumerate(NEW): cv = Cv(); f(cv); sh.alpha_composite(cv.render(), (i * S, 0))
    return sh
def cjk_font(size):
    try:
        out = subprocess.run(['fc-list', ':lang=ko', 'file'], capture_output=True, text=True).stdout
        fs = [l.split(':')[0].strip() for l in out.splitlines() if l.strip()]
        fs.sort(key=lambda p: ('unifont' in p.lower(), p))
        for p in fs:
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    except Exception: pass
    return None
def preview(d):
    os.makedirs(d, exist_ok=True); sh = strip(); sh.save(os.path.join(d, 'dish_new25.png'))
    Z, cols, cw, chh = 4, 5, 160, 156; F = cjk_font(12); bg = (0x21, 0x17, 0x33, 255)
    pv = Image.new('RGBA', (cols * cw, math.ceil(len(NEW) / cols) * chh), bg); dr = ImageDraw.Draw(pv)
    for i, (nm, f) in enumerate(NEW):
        x, y = (i % cols) * cw, (i // cols) * chh
        pv.alpha_composite(sh.crop((i * S, 0, i * S + S, S)).resize((S * Z, S * Z), Image.NEAREST), (x + 16, y + 4))
        if F: dr.text((x + cw // 2, y + 144), '%d %s' % (i + 1, nm), font=F, fill=(255, 243, 200), anchor='mm')
    pv.save(os.path.join(d, 'dish_new25_x4_lbl.png'))
    # 비교: 기존 요리 몇 개 + 새 요리
    old = Image.open(DI.OUT).convert('RGBA'); pick = [0, 11, 15, 22, 34, 38, 61, 66, 74, 81, 85]
    row = [old.crop((i * S, 0, i * S + S, S)) for i in pick if (i + 1) * S <= old.width] + [sh.crop((i * S, 0, i * S + S, S)) for i in range(len(NEW))]
    n = 12; cmp_ = Image.new('RGBA', (n * S, math.ceil(len(row) / n) * S), bg)
    for k, cell in enumerate(row): cmp_.alpha_composite(cell, ((k % n) * S, (k // n) * S))
    cmp_.resize((cmp_.width * 3, cmp_.height * 3), Image.NEAREST).save(os.path.join(d, 'dish_cmp_x3.png'))
def apply():
    old = Image.open(DI.OUT).convert('RGBA'); assert old.width >= BASE * S, old.size
    sh = strip(); out = Image.new('RGBA', (S * (BASE + len(NEW)), S), (0, 0, 0, 0))
    out.alpha_composite(old.crop((0, 0, BASE * S, S)), (0, 0)); out.alpha_composite(sh, (BASE * S, 0)); out.save(DI.OUT); print('dishes.png', out.size)

if __name__ == '__main__':
    if '--preview' in sys.argv: preview(sys.argv[sys.argv.index('--preview') + 1])
    if '--apply' in sys.argv: apply()
    if '--preview' not in sys.argv and '--apply' not in sys.argv: print(__doc__ or 'usage: --preview DIR | --apply')
