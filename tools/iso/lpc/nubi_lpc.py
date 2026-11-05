# 누비 (낡은 양호실의 헝겊 인형)를 LPC 부품으로 조립해요 · 게임 캐릭터와 같은 화풍 (child 몸 · child 머리)
#   한 줄 = 64×64 칸 20개 (아래·위·왼쪽·오른쪽 × 서기 + 걷기 4) · 0 줄 해진 누비 · 1 줄 고쳐진 누비
#   해진 누비: 잿빛 헝겊 살갗 · 한쪽 눈은 X 바늘땀 · 꿰맨 입 · 덧댄 헝겊 · 몸 곳곳 바늘땀
#   고쳐진 누비: 크림빛 헝겊 · 단추 눈 둘 · 분홍 볼 · 리본 · 가슴에 하트 헝겊
#   python3 nubi_lpc.py <LPC 저장소 경로> → public/art/nubi.png (1280×128) · tools/nubi_mock/nubi_prev.png
import sys, os, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..'); sys.path.insert(0, HERE)
import npc_lpc as N
LPC = N.LPC
# 헝겊 살갗 팔레트 (LPC body 팔레트와 같은 6 칸: 외곽선 → 가장 밝은 색)
N.PAL['body']['rag'] = ['#231c22', '#4e474c', '#7d7679', '#a19a9a', '#c6c0bb', '#e0dcd6']
N.PAL['body']['cream_cloth'] = ['#2a1c1c', '#8a6450', '#c4a080', '#dcbe9c', '#f2e0c4', '#fbf2e4']
N.PAL['hair']['yarn_gray'] = ['#231c22', '#3e383c', '#5e575a', '#7d7679', '#9c9696', '#bcb6b2', '#d4cfca']
def parts(fixed):
    sk = 'cream_cloth' if fixed else 'rag'
    return [(10, 'body/bodies/child', None, ('body', 'light', sk)), (100, 'head/heads/human/child', None, ('body', 'light', sk)),
            (118, 'hair/relm_short/child', None, N.HR('light_brown' if fixed else 'yarn_gray'))]
def strip(img):   # walk.png (9 칸 × 4 줄) → 20 칸 (child 몸은 날씬하게 줄이지 않아요)
    out = np.zeros((64, 64 * 20, 4), np.uint8); a = np.array(img.convert('RGBA'))
    for di, d in enumerate(N.DIRS):
        for ci, c in enumerate(N.COLS):
            y, x = N.ROWS[d] * 64, c * 64
            if y + 64 <= a.shape[0] and x + 64 <= a.shape[1]: out[:, (di * 5 + ci) * 64:(di * 5 + ci + 1) * 64] = a[y:y + 64, x:x + 64]
    return out
def build(fixed):
    plan = [(z, N.find(p, c, 'child'), rc) for z, p, c, rc in parts(fixed)]
    need = sorted({f for _, f, _ in plan if not os.path.exists(os.path.join(LPC, f))})
    if need: subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--skip-checks', *need], check=True)
    row = np.zeros((64, 64 * 20, 4), np.uint8)
    for z, f, rc in sorted(plan, key=lambda t: t[0]): N.over(row, N.recolor(strip(Image.open(os.path.join(LPC, f))), rc))
    return dress(row, fixed)
DRESS = {False: ['#1e2a36', '#34485a', '#4e667c', '#6c869c', '#8ea8bc', '#b4cad8'], True: ['#5a2a3a', '#9a4a62', '#d07a92', '#eaa0b2', '#f8c4d0', '#ffe4ea']}
def P(a, pts, c):
    for x, y in pts:
        if 0 <= x < 64 and 0 <= y < 64: a[y, x, :3] = N.hx(c); a[y, x, 3] = 255
def dress(row, fixed):
    S = [N.hx(c) for c in N.PAL['body']['cream_cloth' if fixed else 'rag']]; D = [N.hx(c) for c in DRESS[fixed]]
    for i in range(20):
        c = row[:, i * 64:(i + 1) * 64]; d = i // 5
        ys = np.nonzero(c[..., 3].any(1))[0]; dy = (ys[0] - 20) if len(ys) else 0   # 걸을 때 위아래로 흔들리는 만큼
        for y in range(39 + dy, 54 + dy):                                          # 옷: 살갗 색 단계를 그대로 옷 색으로 (LPC 음영 유지)
            for x in range(64):
                if d in (0, 1) and y >= 48 + dy and (x < 25 or x > 38): continue  # 손은 헝겊 그대로
                for k, s in enumerate(S):
                    if tuple(c[y, x, :3]) == s and c[y, x, 3]: c[y, x, :3] = D[k]; break
        for y in range(28 + dy, 38 + dy):                                          # 눈 → 검은 단추
            for x in range(64):
                r, g, b = (int(v) for v in c[y, x, :3])
                if c[y, x, 3] and b > r + 30 and y < 37 + dy: c[y, x, :3] = (26, 16, 32) if b < 200 else (90, 80, 110)
        o = lambda pts, col: P(c, [(x, y + dy) for x, y in pts], col)
        if d == 0:   # 앞모습 얼굴
            if not fixed:
                o([(26, 34), (29, 34), (27, 35), (28, 35), (26, 36), (29, 36)], '#2e2228'); o([(27, 34), (28, 34), (26, 35), (29, 35), (27, 36), (28, 36)], '#a19a9a')   # X 바늘땀 눈
                o([(34, 34)], '#ffffff')
                o([(x, 37) for x in range(29, 35)], '#2e2228'); o([(29, 38), (31, 38), (33, 38)], '#2e2228')    # 꿰맨 입
                o([(23, 29), (24, 30), (25, 31), (24, 28), (26, 30)], '#2e2228')                              # 볼 바늘땀
                o([(x, y) for x in range(27, 32) for y in range(44, 48)], '#b89a5a'); o([(27, 44), (29, 44), (31, 44), (27, 47), (29, 47), (31, 47), (27, 46), (31, 45)], '#5a4422')   # 배에 덧댄 헝겊
                o([(35, 42), (36, 43), (35, 44), (36, 45), (35, 46)], '#1e2a36')                              # 옷 꿰맨 자국
            else:
                o([(27, 34), (34, 34)], '#ffffff')
                o([(24, 36), (25, 36), (38, 36), (39, 36)], '#f08aa0'); o([(31, 37), (32, 37)], '#7a3040')     # 볼 · 입
                o([(29, 42), (30, 42), (32, 42), (33, 42), (28, 43), (29, 43), (30, 43), (31, 43), (32, 43), (33, 43), (34, 43), (29, 44), (30, 44), (31, 44), (32, 44), (33, 44), (30, 45), (31, 45), (32, 45), (31, 46)], '#fff0d8')
                o([(29, 42), (33, 42), (28, 43), (34, 43), (31, 46)], '#c4a080')                              # 하트 헝겊
        K, SK = '#2e2228', '#a19a9a'
        if not fixed and d == 2:   # 왼쪽 보기: 단추 눈 · 꿰맨 입 · 옷 꿰맨 자국
            o([(29, 34)], '#ffffff')
            o([(26, 37), (27, 37), (28, 37), (29, 37)], K); o([(27, 36), (29, 36), (28, 38)], K)
            o([(28, 42), (29, 43), (28, 44), (29, 45), (28, 46)], '#1e2a36')
        if not fixed and d == 3:   # 오른쪽 보기: X 바늘땀 눈 · 꿰맨 입 · 볼 바늘땀 · 덧댄 헝겊
            o([(33, 34), (34, 34), (33, 35), (34, 35), (33, 36), (34, 36)], SK); o([(32, 34), (34, 34), (33, 35), (32, 36), (34, 36)], K)
            o([(34, 37), (35, 37), (36, 37), (37, 37)], K); o([(34, 36), (36, 36), (35, 38)], K)
            o([(37, 28), (38, 29), (39, 30), (36, 29), (38, 31)], K)
            o([(x, y) for x in range(33, 38) for y in range(44, 48)], '#b89a5a'); o([(33, 44), (35, 44), (37, 44), (33, 47), (35, 47), (37, 47), (33, 46), (37, 45)], '#5a4422')
        if not fixed and d == 1:   # 뒷모습: 등 솔기 · 덧댄 헝겊 · 머리 바늘땀
            o([(31, y) for y in range(41, 52, 2)], '#1e2a36'); o([(30, y) for y in range(42, 52, 2)] + [(32, y) for y in range(42, 52, 2)], '#34485a')
            o([(x, y) for x in range(34, 39) for y in range(44, 48)], '#b89a5a'); o([(34, 44), (36, 44), (38, 44), (34, 47), (36, 47), (38, 47), (34, 46), (38, 45)], '#5a4422')
            o([(26, 28), (27, 29), (28, 30), (29, 31), (27, 27), (29, 29), (26, 30), (28, 32)], K)
        if fixed and d == 2:
            o([(29, 34)], '#ffffff'); o([(25, 36), (26, 36)], '#f08aa0'); o([(27, 37), (28, 37)], '#7a3040')
            o([(25, 42), (27, 42), (24, 43), (25, 43), (26, 43), (27, 43), (28, 43), (25, 44), (26, 44), (27, 44), (26, 45)], '#fff0d8')
        if fixed and d == 3:
            o([(33, 34)], '#ffffff'); o([(37, 36), (38, 36)], '#f08aa0'); o([(35, 37), (36, 37)], '#7a3040')
            o([(35, 42), (37, 42), (34, 43), (35, 43), (36, 43), (37, 43), (38, 43), (35, 44), (36, 44), (37, 44), (36, 45)], '#fff0d8')
        if fixed and d == 1: o([(36, 44), (38, 44), (35, 45), (36, 45), (37, 45), (38, 45), (39, 45), (36, 46), (37, 46), (38, 46), (37, 47)], '#fff0d8')   # 등에 작은 하트
        if fixed and d != 1:   # 리본 (머리 오른쪽 위)
            bx = {0: 37, 2: 33, 3: 36}[d] if d in (0, 2, 3) else 37
            o([(bx, 21), (bx + 1, 22), (bx, 22), (bx, 23), (bx + 4, 21), (bx + 3, 22), (bx + 4, 22), (bx + 4, 23)], '#d07a92')
            o([(bx + 1, 21), (bx + 3, 21), (bx + 1, 23), (bx + 3, 23)], '#f8c4d0'); o([(bx + 2, 22)], '#9a4a62')
        elif fixed:
            o([(22, 21), (23, 22), (22, 22), (22, 23), (26, 21), (25, 22), (26, 22), (26, 23)], '#d07a92'); o([(24, 22)], '#9a4a62')
    return row
if __name__ == '__main__':
    sheet = np.concatenate([build(False), build(True)], 0)
    Image.fromarray(sheet).save(os.path.join(ROOT, 'public', 'art', 'nubi.png'))
    if len(sys.argv) > 2:
        pv = Image.new('RGBA', (64 * 10, 64), (40, 30, 56, 255)); im = Image.fromarray(sheet)
        for j, (r, i) in enumerate(((0, 0), (0, 2), (0, 5), (0, 10), (0, 15), (1, 0), (1, 2), (1, 5), (1, 10), (1, 15))): pv.alpha_composite(im.crop((i * 64, r * 64, i * 64 + 64, r * 64 + 64)), (j * 64, 0))
        pv.resize((pv.width * 4, 256), Image.NEAREST).save(sys.argv[2])
    print('nubi ok')
