# 시안: 「시련의 탑」 그림 — 몬스터 8 부류 (64 칸 · monsters_lpc 뒤에 이어 붙일 수 있게) · 10 층 보스 · 부류 아이콘 16 칸 × 8 · 탑 건물
#   python3 tools/tower/tower_art.py → tower_mon.png (64×64 × 9) · tower_icons.png (16×16 × 8) · tower_building.png (56×120) · tower_preview.png
import os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
H = lambda h, a=255: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
OL = H('#1E1428')
def outline(im):
    px = im.load(); W, Hh = im.size; add = []
    for y in range(Hh):
        for x in range(W):
            if px[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < Hh and px[x + dx, y + dy][3] > 0 and px[x + dx, y + dy][:3] != OL[:3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((x, y))
    for p in add: px[p] = OL
    return im
def R(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)
def P(d, x, y, c): d.point((x, y), fill=c)
def E(d, x0, y0, x1, y1, c): d.ellipse([x0, y0, x1, y1], fill=c)
def eye(d, x, y, c='#FFFFFF', p='#1A1020'): R(d, x, y, 2, 2, H(c)); P(d, x + 1, y + 1, H(p))
def cell(): im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
# 모두 오른쪽을 봐요 (monsters_lpc 와 같은 방향) · 발은 y=58 쯤

def armor():   # 철갑: 강철 딱정벌레 기사
    im, d = cell()
    for lx in (22, 30, 38): R(d, lx, 50, 3, 8, H('#3A4250')); R(d, lx + 1, 57, 3, 1, H('#2A303A'))
    E(d, 14, 26, 50, 54, H('#6E7A8C')); E(d, 16, 27, 46, 46, H('#9AA8BC')); E(d, 19, 29, 34, 38, H('#C8D4E4'))
    d.line([(32, 27), (32, 53)], fill=H('#4A5466'), width=1)
    for x in (22, 28, 36, 42): P(d, x, 40, H('#E8F0FA')); P(d, x, 47, H('#4A5466'))
    E(d, 44, 34, 56, 48, H('#4A5466')); E(d, 46, 36, 54, 44, H('#6E7A8C'))   # 머리
    d.polygon([(52, 34), (58, 24), (56, 35)], fill=H('#9AA8BC'))   # 뿔
    eye(d, 51, 39, '#FFD860', '#B04020')
    return outline(im)
def giant():   # 거대: 이끼 바위 거인
    im, d = cell()
    R(d, 20, 48, 9, 10, H('#6A6458')); R(d, 36, 48, 9, 10, H('#6A6458'))
    E(d, 10, 18, 54, 54, H('#8A8274')); E(d, 13, 20, 44, 44, H('#A49C8C'))
    E(d, 4, 28, 18, 50, H('#7A7264')); E(d, 46, 28, 60, 50, H('#7A7264'))   # 팔
    E(d, 6, 44, 18, 56, H('#8A8274')); E(d, 46, 44, 58, 56, H('#8A8274'))   # 주먹
    for x, y, w in ((14, 18, 14), (30, 16, 12), (40, 22, 10), (6, 28, 8)): E(d, x, y, x + w, y + 6, H('#5E9A4A')); E(d, x + 2, y, x + w - 3, y + 3, H('#86C266'))   # 이끼
    R(d, 36, 30, 4, 3, H('#2A2420')); R(d, 44, 30, 4, 3, H('#2A2420')); P(d, 37, 30, H('#B8F0A0')); P(d, 45, 30, H('#B8F0A0'))
    R(d, 38, 38, 10, 2, H('#5A5448'))
    return outline(im)
def swift(f=0):   # 날쌘: 그림자 박쥐 여우
    im, d = cell(); up = f == 1
    wy = 22 if up else 30
    d.polygon([(28, 36), (4, wy), (10, wy + 8), (6, wy + 14), (16, wy + 12), (22, 42)], fill=H('#3A2A5A'))
    d.polygon([(36, 36), (60, wy), (54, wy + 8), (58, wy + 14), (48, wy + 12), (42, 42)], fill=H('#3A2A5A'))
    d.polygon([(27, 36), (8, wy + 2), (12, wy + 8), (22, 40)], fill=H('#5A4488'))
    E(d, 22, 30, 44, 50, H('#2E2244')); E(d, 26, 36, 40, 50, H('#4A3A6A'))
    d.polygon([(25, 32), (24, 20), (31, 30)], fill=H('#2E2244')); d.polygon([(41, 32), (42, 20), (35, 30)], fill=H('#2E2244'))
    eye(d, 28, 36, '#F070FF', '#FFFFFF'); eye(d, 36, 36, '#F070FF', '#FFFFFF')
    d.polygon([(30, 50), (22, 58), (34, 52)], fill=H('#2E2244'))   # 꼬리
    for i in range(3): R(d, 6 + i * 4, 52 + i, 3, 1, H('#8A7AC0', 140))   # 잔상
    return outline(im)
def swarm():   # 무리: 꼬마 슬라임 (전투에는 셋이 나와요)
    im, d = cell()
    for (x, y, s, c, c2) in ((20, 34, 24, '#5AB8F0', '#B0E4FF'),):
        E(d, x, y, x + s, y + s * 3 // 4 + 4, H(c)); E(d, x + 3, y + 2, x + s // 2, y + s // 3 + 1, H(c2))
        eye(d, x + s // 2, y + s // 3 + 2); eye(d, x + s // 2 + 4, y + s // 3 + 2)
        R(d, x + s // 2 + 1, y + s // 3 + 6, 3, 1, H('#2A5A80'))
    return outline(im)
def regen():   # 재생: 덩굴 나무 정령
    im, d = cell()
    for x in (18, 26, 36, 44): d.line([(x, 52), (x - 4, 58)], fill=H('#6A4A2A'), width=2)
    E(d, 16, 22, 48, 56, H('#7A5A34')); E(d, 20, 26, 40, 50, H('#946E42'))
    for x, y in ((10, 10), (24, 4), (38, 8), (46, 18), (6, 22)): E(d, x, y, x + 16, y + 14, H('#3E9A4A')); E(d, x + 3, y + 2, x + 10, y + 7, H('#6ACA5E'))
    for x, y in ((14, 14), (40, 12), (28, 6)): R(d, x, y, 3, 3, H('#FF8AB0')); P(d, x + 1, y + 1, H('#FFE070'))
    R(d, 30, 34, 3, 4, H('#2A1A10')); R(d, 38, 34, 3, 4, H('#2A1A10')); P(d, 31, 34, H('#C0FFB0')); P(d, 39, 34, H('#C0FFB0'))
    d.line([(31, 43), (35, 45), (39, 43)], fill=H('#3A2414'))
    for x, y in ((52, 30), (56, 40), (8, 42)): R(d, x, y + 1, 5, 1, H('#80FF90')); R(d, x + 2, y - 1, 1, 5, H('#80FF90'))   # 회복 십자
    return outline(im)
def drain():   # 마나 먹기: 보라 도깨비불
    im, d = cell()
    d.polygon([(20, 46), (14, 18), (24, 30), (28, 10), (34, 26), (40, 8), (44, 28), (50, 16), (46, 46)], fill=H('#7A4AD0'))
    E(d, 16, 26, 48, 56, H('#7A4AD0')); E(d, 20, 30, 42, 52, H('#A070F0')); E(d, 24, 34, 36, 44, H('#D0B0FF'))
    eye(d, 28, 38, '#FFFFFF', '#3A1A70'); eye(d, 36, 38, '#FFFFFF', '#3A1A70')
    E(d, 30, 45, 37, 50, H('#2A0E50')); P(d, 32, 45, H('#FFFFFF')); P(d, 35, 45, H('#FFFFFF'))   # 입 (이빨)
    for i, (x, y) in enumerate(((56, 30), (58, 40), (54, 50))): E(d, x - 2, y - 2, x + 2, y + 2, H('#60B0FF')); d.line([(x - 3, y), (48, 40)], fill=H('#60B0FF', 120))   # 빨려 드는 마나 방울
    return outline(im)
def mirror():   # 반사: 거울 수정
    im, d = cell()
    d.polygon([(32, 6), (46, 20), (44, 50), (32, 58), (20, 50), (18, 20)], fill=H('#7AC8E8'))
    d.polygon([(32, 6), (46, 20), (32, 30), (18, 20)], fill=H('#C8F0FF'))
    d.polygon([(32, 30), (44, 50), (32, 58)], fill=H('#4A98C0'))
    d.line([(24, 22), (28, 40)], fill=H('#FFFFFF'), width=2); d.line([(36, 14), (40, 18)], fill=H('#FFFFFF'))
    for x0, y0, x1, y1 in ((6, 30, 14, 26), (8, 40, 16, 40), (50, 26, 58, 22), (50, 40, 58, 42)): d.line([(x0, y0), (x1, y1)], fill=H('#FFF2A0'), width=1)
    d.polygon([(10, 44), (16, 36), (18, 52)], fill=H('#9AD8F0')); d.polygon([(54, 44), (48, 34), (46, 52)], fill=H('#9AD8F0'))   # 작은 조각
    eye(d, 27, 34, '#1A3A5A', '#FFFFFF'); eye(d, 35, 34, '#1A3A5A', '#FFFFFF')
    return outline(im)
def rage():   # 광폭: 성난 뿔 멧돼지
    im, d = cell()
    for x in (16, 24, 36, 44): R(d, x, 48, 5, 10, H('#5A2A1E'))
    E(d, 8, 26, 50, 52, H('#8A3A2A')); E(d, 12, 28, 40, 42, H('#A84A34'))
    d.polygon([(10, 28), (14, 18), (18, 28), (22, 16), (26, 28), (30, 18), (34, 28)], fill=H('#5A2A1E'))   # 갈기
    E(d, 40, 30, 60, 48, H('#9A4230')); E(d, 52, 38, 62, 46, H('#E09A8A')); P(d, 56, 41, H('#4A1A10')); P(d, 59, 41, H('#4A1A10'))
    d.polygon([(50, 44), (56, 52), (52, 44)], fill=H('#F4ECD8')); d.polygon([(44, 32), (40, 20), (48, 30)], fill=H('#E8DCC0'))
    R(d, 46, 34, 3, 2, H('#FFE040')); P(d, 47, 35, H('#D02010'))
    for x, y in ((14, 10), (24, 6), (34, 10)): d.polygon([(x, y + 6), (x + 3, y), (x + 6, y + 6)], fill=H('#FF5A2A')); d.polygon([(x + 2, y + 6), (x + 3, y + 3), (x + 4, y + 6)], fill=H('#FFD040'))   # 화난 김
    return outline(im)
def boss():   # 10 층 보스: 탑지기 석상 (64 칸 · 크게 그려요)
    im, d = cell()
    R(d, 18, 50, 10, 8, H('#5A5A6A')); R(d, 36, 50, 10, 8, H('#5A5A6A'))
    E(d, 12, 22, 52, 54, H('#7A7A8C')); E(d, 16, 24, 44, 44, H('#9A9AAE'))
    R(d, 4, 26, 12, 22, H('#6A6A7C')); R(d, 48, 26, 12, 22, H('#6A6A7C'))
    R(d, 2, 22, 16, 6, H('#8A8A9E')); R(d, 46, 22, 16, 6, H('#8A8A9E'))   # 어깨
    E(d, 22, 4, 42, 26, H('#8A8A9E')); E(d, 24, 6, 36, 18, H('#AAAABE'))
    R(d, 26, 13, 12, 3, H('#2A2A3A')); R(d, 28, 13, 3, 3, H('#60F0FF')); R(d, 34, 13, 3, 3, H('#60F0FF'))
    d.polygon([(32, 28), (38, 36), (32, 44), (26, 36)], fill=H('#60F0FF')); d.polygon([(32, 31), (35, 36), (32, 41), (29, 36)], fill=H('#D0FFFF'))   # 가슴 보석
    d.polygon([(22, 6), (18, 0), (26, 4)], fill=H('#AAAABE')); d.polygon([(42, 6), (46, 0), (38, 4)], fill=H('#AAAABE'))
    for x, y in ((14, 46), (48, 30), (20, 30)): d.line([(x, y), (x + 3, y + 4), (x + 1, y + 7)], fill=H('#4A4A5A'))   # 금
    return outline(im)

# ---------- 부류 아이콘 16 × 16 ----------
def icons():
    out = Image.new('RGBA', (16 * 8, 16), (0, 0, 0, 0))
    def ic(i, f):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f(d); out.alpha_composite(outline(im), (i * 16, 0))
    ic(0, lambda d: (d.polygon([(8, 1), (14, 3), (13, 10), (8, 14), (3, 10), (2, 3)], fill=H('#9AA8BC')), d.polygon([(8, 3), (12, 4), (8, 12)], fill=H('#C8D4E4'))))   # 철갑: 방패
    ic(1, lambda d: (E(d, 1, 2, 14, 14, H('#E05A6A')), E(d, 3, 4, 7, 8, H('#FFA0AA')), R(d, 6, 0, 4, 3, H('#5E9A4A'))))   # 거대: 큰 하트
    ic(2, lambda d: (d.polygon([(1, 10), (8, 2), (15, 4), (9, 9), (13, 14), (4, 12)], fill=H('#8A7AC0')), R(d, 0, 13, 5, 1, H('#C8BCF0'))))   # 날쌘: 바람 깃
    ic(3, lambda d: [E(d, x, y, x + 6, y + 5, H('#6AC4F8')) for x, y in ((0, 9), (9, 9), (4, 2))])   # 무리: 셋
    ic(4, lambda d: (R(d, 6, 2, 4, 12, H('#5ADA6A')), R(d, 2, 6, 12, 4, H('#5ADA6A')), R(d, 7, 3, 2, 10, H('#B8FFB0'))))   # 재생: 십자
    ic(5, lambda d: (d.polygon([(8, 1), (13, 9), (8, 15), (3, 9)], fill=H('#60A8FF')), d.line([(4, 4), (12, 12)], fill=H('#7A4AD0'), width=2)))   # 마나 먹기: 금 간 방울
    ic(6, lambda d: (d.polygon([(8, 1), (14, 6), (12, 14), (4, 14), (2, 6)], fill=H('#7AC8E8')), d.line([(5, 5), (11, 11)], fill=H('#FFFFFF')), d.line([(1, 1), (5, 5)], fill=H('#FFF2A0'))))   # 반사: 거울
    ic(7, lambda d: (d.polygon([(8, 0), (11, 6), (15, 5), (12, 10), (14, 15), (8, 12), (2, 15), (4, 10), (1, 5), (5, 6)], fill=H('#FF5A2A')), d.polygon([(8, 4), (10, 8), (8, 11), (6, 8)], fill=H('#FFD040'))))   # 광폭: 불
    return out

# ---------- 탑 건물 (맵 위 소품 · 56 × 120) ----------
def building():
    im = Image.new('RGBA', (56, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R(d, 8, 30, 40, 84, H('#6E6488'))
    for y in range(32, 112, 8):   # 돌 줄
        d.line([(9, y), (46, y)], fill=H('#5A5274'))
        for x in range(10 + (y // 8 % 2) * 6, 46, 12): d.line([(x, y), (x, y + 7)], fill=H('#5A5274'))
    R(d, 8, 30, 6, 84, H('#827AA0')); R(d, 42, 30, 6, 84, H('#544C6C'))
    R(d, 4, 104, 48, 10, H('#5A5274')); R(d, 4, 104, 48, 2, H('#7A7298'))   # 받침
    for y in (44, 66): E(d, 22, y, 33, y + 12, H('#2A2040')); E(d, 24, y + 2, 31, y + 10, H('#FFD878'))   # 창
    E(d, 18, 86, 37, 104, H('#2A1E3A')); R(d, 18, 95, 20, 9, H('#2A1E3A')); E(d, 20, 88, 35, 104, H('#4A3A2A')); R(d, 20, 96, 16, 8, H('#4A3A2A'))   # 문
    P(d, 32, 97, H('#F2C040'))
    R(d, 4, 24, 48, 8, H('#827AA0'))
    for x in range(4, 52, 8): R(d, x, 18, 5, 7, H('#827AA0'))   # 성가퀴
    d.polygon([(10, 18), (28, 0), (46, 18)], fill=H('#4A3A7A')); d.polygon([(28, 0), (46, 18), (34, 18)], fill=H('#3A2C64'))   # 지붕
    E(d, 24, 2, 32, 10, H('#9AE8FF')); E(d, 26, 4, 29, 7, H('#FFFFFF'))   # 꼭대기 빛 구슬
    R(d, 21, 78, 14, 6, H('#3A2C54')); [P(d, x, 80, H('#F2C040')) for x in (23, 26, 29, 32)]   # 문패
    return outline(im)

if __name__ == '__main__':
    mons = [armor(), giant(), swift(), swarm(), regen(), drain(), mirror(), rage(), boss()]
    sheet = Image.new('RGBA', (64 * len(mons), 64), (0, 0, 0, 0))
    for i, m in enumerate(mons): sheet.alpha_composite(m, (i * 64, 0))
    sheet.save(os.path.join(HERE, 'tower_mon.png'))
    ic = icons(); ic.save(os.path.join(HERE, 'tower_icons.png'))
    bd = building(); bd.save(os.path.join(HERE, 'tower_building.png'))
    pv = Image.new('RGBA', (64 * 9 * 3, 64 * 3 + 16 * 4 + 120 * 3 + 20), H('#2A2F44'))
    pv.alpha_composite(sheet.resize((64 * 9 * 3, 192), Image.NEAREST), (0, 0))
    pv.alpha_composite(ic.resize((128 * 4, 64), Image.NEAREST), (0, 200))
    pv.alpha_composite(bd.resize((168, 360), Image.NEAREST), (560, 200))
    pv.save(os.path.join(HERE, 'tower_preview.png')); print('ok')
