# 새 친구 넷의 ♥10 방 가구 시안: 바우의 집 · 은 등불 · 별 지도 · 낡은 소파 (art/iso/furn.png 와 같은 크기 · 그림체: 외곽선 없이 면마다 3 단계 명암)
#   python3 tools/iso/furn_new4.py <출력 폴더>  → furn_<id>.png (원래 크기) + 미리보기 preview.png (4 배, 방 바닥 위)
import os, sys
from PIL import Image, ImageDraw
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
def cv(w, h): im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def R(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)
def P(d, pts, c):
    for x, y in pts: d.point((x, y), fill=c)

def doghouse():   # 바우의 집: 나무 개집 · 빨간 지붕 · 둥근 문 · 문패 · 안에 담요 · 옆에 밥그릇
    im, d = cv(36, 34)
    W1, W2, W3 = (176, 118, 70), (148, 96, 56), (112, 70, 40)            # 나무 (밝음 · 중간 · 어둠)
    R1, R2, R3 = (196, 64, 60), (162, 46, 46), (120, 32, 36)             # 지붕
    # 몸통 앞면 (왼쪽) · 옆면 (오른쪽, 어둡게)
    d.polygon([(4, 16), (20, 22), (20, 32), (4, 26)], fill=W1)
    d.polygon([(20, 22), (31, 17), (31, 27), (20, 32)], fill=W2)
    for y in (19, 22, 25): d.line([(4, y), (20, y + 6)], fill=W2)           # 판자 줄
    for y in (21, 24): d.line([(21, y + 1), (30, y - 3)], fill=W3)
    # 지붕
    d.polygon([(2, 16), (12, 4), (21, 9), (21, 23)], fill=R1)
    d.polygon([(12, 4), (25, 0), (33, 6), (21, 9)], fill=R2)
    d.polygon([(21, 9), (33, 6), (33, 17), (21, 23)], fill=R3)
    d.line([(2, 16), (21, 23)], fill=R3); d.line([(12, 4), (21, 9)], fill=(222, 96, 86))
    # 둥근 문 (안은 어둡고 담요가 살짝)
    d.ellipse([8, 19, 16, 31], fill=(46, 28, 24)); R(d, 8, 25, 9, 5, (46, 28, 24))
    R(d, 9, 27, 7, 2, (226, 196, 120)); P(d, [(10, 27), (13, 27)], (240, 214, 150))
    # 문패 「바우」 대신 작은 뼈다귀 모양
    R(d, 17, 19, 3, 2, (236, 226, 200)); P(d, [(16, 19), (16, 20), (20, 19), (20, 20)], (236, 226, 200))
    # 지붕 위 빨간 목도리 깃발 (옛 목도리)
    d.polygon([(24, 2), (29, 4), (26, 7)], fill=(210, 60, 64)); P(d, [(28, 6), (29, 7)], (170, 40, 44))
    # 밥그릇
    d.ellipse([25, 27, 34, 32], fill=(84, 120, 176)); d.ellipse([26, 27, 33, 29], fill=(176, 120, 72)); P(d, [(28, 28), (30, 28)], (210, 160, 100))
    return im

def lantern():   # 은 등불: 은빛 테 · 따뜻한 불빛 · 손잡이 고리 · 받침
    im, d = cv(16, 32)
    S1, S2, S3 = (220, 224, 236), (168, 174, 192), (112, 116, 136)
    G1, G2, G3 = (255, 236, 160), (255, 196, 96), (232, 150, 60)
    d.ellipse([5, 0, 10, 4], outline=S2)                                  # 고리
    d.polygon([(3, 7), (8, 4), (13, 7)], fill=S1); R(d, 3, 7, 11, 2, S2)    # 뚜껑
    R(d, 4, 9, 8, 13, G2); R(d, 5, 10, 6, 11, G1); R(d, 7, 12, 2, 6, (255, 252, 230))   # 유리 · 불빛
    for x in (3, 8, 12): R(d, x, 9, 1, 13, S2)                              # 은 기둥
    R(d, 3, 9, 1, 13, S1); R(d, 12, 9, 1, 13, S3)
    R(d, 2, 22, 12, 2, S2); R(d, 3, 24, 10, 1, S3)                          # 받침
    R(d, 7, 25, 2, 4, S3); R(d, 4, 29, 8, 2, S2); R(d, 5, 31, 6, 1, S3)    # 다리
    return im

def starmap():   # 별 지도: 나무 이젤에 세운 남색 별 지도 · 별자리 선 · 귀퉁이에 작은 이름 · 아래 둘둘 만 지도
    im, d = cv(26, 36)
    W1, W2 = (150, 100, 60), (110, 70, 40)
    d.line([(4, 35), (9, 6)], fill=W2, width=2); d.line([(21, 35), (16, 6)], fill=W2, width=2); d.line([(13, 10), (13, 35)], fill=W1)   # 이젤
    R(d, 2, 4, 22, 20, (196, 160, 96)); R(d, 3, 5, 20, 18, (36, 44, 92)); R(d, 3, 5, 20, 3, (52, 62, 120))   # 액자 · 밤하늘
    stars = [(6, 9), (9, 12), (13, 10), (16, 14), (19, 11), (8, 18), (12, 16), (17, 19), (20, 7)]
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 3)]: d.line([stars[a], stars[b]], fill=(110, 130, 200))   # 별자리 선
    P(d, stars, (255, 240, 170)); P(d, [(13, 10), (16, 14)], (255, 255, 230))
    R(d, 18, 20, 4, 1, (220, 200, 140))                                     # 귀퉁이 작은 이름 (스텔라)
    R(d, 6, 25, 14, 2, W1)                                                  # 이젤 선반
    d.ellipse([5, 27, 11, 31], fill=(232, 220, 184)); R(d, 8, 27, 9, 5, (232, 220, 184)); d.ellipse([14, 27, 20, 31], fill=(210, 196, 156))   # 둘둘 만 지도
    R(d, 11, 28, 2, 3, (160, 70, 160))                                      # 보라 끈 (나비넥타이 색)
    return im

def sofa_old():   # (처음 시안): 바랜 황갈색 가죽 · 덧댄 천 조각 · 접힌 담요 · 꺼진 쿠션
    im, d = cv(34, 26)
    L1, L2, L3 = (190, 140, 92), (156, 110, 70), (118, 80, 50)
    d.polygon([(2, 10), (22, 16), (22, 24), (2, 18)], fill=L2)              # 앞 몸통
    d.polygon([(22, 16), (32, 11), (32, 19), (22, 24)], fill=L3)            # 옆 팔걸이 면
    d.polygon([(4, 3), (24, 9), (24, 16), (4, 10)], fill=L1)                # 등받이
    d.polygon([(24, 9), (30, 6), (30, 12), (24, 16)], fill=L2)
    d.polygon([(2, 8), (6, 6), (6, 15), (2, 17)], fill=L1)                  # 왼쪽 팔걸이
    d.polygon([(4, 10), (22, 16), (30, 12), (12, 7)], fill=(176, 128, 82))  # 앉는 자리
    d.line([(13, 9), (16, 14)], fill=L3)                                    # 쿠션 이음매 (꺼짐)
    R(d, 7, 5, 4, 3, (110, 140, 120)); P(d, [(7, 5), (10, 5), (7, 7), (10, 7)], (200, 200, 180))   # 덧댄 초록 천 조각 · 바느질
    d.polygon([(18, 10), (25, 12), (27, 16), (20, 14)], fill=(126, 84, 150)); d.line([(18, 10), (25, 12)], fill=(160, 120, 186))   # 접힌 보라 담요 (넥타이 색)
    R(d, 3, 18, 2, 3, L3); R(d, 20, 23, 2, 3, L3); R(d, 30, 18, 2, 3, (90, 60, 36))   # 다리
    P(d, [(9, 12), (14, 13)], (210, 166, 116))                              # 해진 반들반들한 곳
    return im

FURN_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'art', 'iso', 'furn.png')
def sofa():   # 낡은 소파: 상점 「푹신한 소파」 모양을 바랜 황갈색 가죽으로 · 덧댄 초록 천 조각 · 접힌 보라 담요
    base = Image.open(FURN_PNG).convert('RGBA').crop((35, 0, 61, 25)); px = base.load(); w, h = base.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and b > r and b > 60:   # 보라 → 황갈색 (밝기는 그대로)
                l = (r * .3 + g * .59 + b * .11) / 110; px[x, y] = (min(255, int(196 * l)), min(255, int(146 * l)), min(255, int(96 * l)), a)
    im = Image.new('RGBA', (30, 26), (0, 0, 0, 0)); im.alpha_composite(base, (2, 1)); d = ImageDraw.Draw(im)
    R(d, 7, 6, 4, 3, (104, 140, 112)); P(d, [(7, 6), (10, 6), (7, 8), (10, 8)], (210, 206, 180))   # 덧댄 천 조각 · 바느질
    d.polygon([(16, 12), (23, 15), (24, 18), (17, 15)], fill=(126, 84, 150)); d.line([(16, 12), (23, 15)], fill=(166, 126, 190))   # 접힌 담요
    return im
def outline(im, col=(42, 22, 24, 255)):   # 기존 가구처럼 1 칸 어두운 외곽선
    a = im.split()[3]; o = Image.new('RGBA', (im.width + 2, im.height + 2), (0, 0, 0, 0)); px = o.load(); src = a.load()
    for y in range(-1, im.height + 1):
        for x in range(-1, im.width + 1):
            inside = 0 <= x < im.width and 0 <= y < im.height and src[x, y] > 0
            if not inside and any(0 <= x + dx < im.width and 0 <= y + dy < im.height and src[x + dx, y + dy] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): px[x + 1, y + 1] = col
    o.alpha_composite(im, (1, 1)); return o
ITEMS = [('bau_house', '바우의 집', doghouse), ('kael_lantern', '은 등불', lantern), ('artua_starmap', '별 지도', starmap), ('grego_sofa', '낡은 소파', sofa)]
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); arts = []
    for fid, nm, f in ITEMS:
        a = f(); a = a if fid == 'grego_sofa' else outline(a); a.save(os.path.join(OUT, f'furn_{fid}.png')); arts.append(a); print(fid, nm, a.size)
    # 미리보기: 방 바닥 색 위에, 기존 가구(흔들의자 · 책장)와 나란히 4 배
    furn = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'art', 'iso', 'furn.png')).convert('RGBA')
    ref = [furn.crop((13, 0, 34, 61)), furn.crop((137, 0, 151, 61))]
    W = sum(a.width for a in arts + ref) + 12 * 7; H = 64
    pv = Image.new('RGBA', (W, H), (96, 72, 60, 255)); x = 6
    for a in ref + arts:
        bb = a.getbbox(); a2 = a.crop(bb) if bb else a; pv.alpha_composite(a2, (x, H - 4 - a2.height)); x += a2.width + 12
    pv.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, 'preview.png'))
