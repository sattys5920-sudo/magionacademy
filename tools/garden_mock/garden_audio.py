# 손님이 찾아오는 정원 영상 소리: python3 garden_audio.py <garden_log.json> <영상 길이> <로그→영상 시각 차이> <출력.wav>
#   저녁 풀벌레 · 느긋한 기타풍 가락(직접 만든 것) · 물건 놓는 소리 · 시계 · 선물 반짝 · 사진 찰칵 · 박쥐 날갯짓 · 도감 · 드문 손님
import sys, json, wave, numpy as np
R = 44100; L = json.load(open(sys.argv[1])); D = float(sys.argv[2]); OFF = float(sys.argv[3]); N = int(R * (D + 1)); out = np.zeros(N)
ev = {}
for t, k in L: ev.setdefault(k, []).append(t + OFF)
def add(t0, s):
    i = int(max(0, t0) * R); j = min(N, i + len(s)); out[i:j] += s[:j - i]
def env(n, a=.005, r=3): t = np.arange(n) / R; return np.minimum(1, t / a) * np.exp(-t * r)
def tone(t0, f, d, v=.2, kind='sine', dec=3):
    n = int(d * R); t = np.arange(n) / R
    w = np.sin(2 * np.pi * f * t) if kind == 'sine' else (2 * np.abs(2 * ((f * t) % 1) - 1) - 1) if kind == 'tri' else np.sign(np.sin(2 * np.pi * f * t)) * .5
    add(t0, w * env(n, r=dec) * v)
def noise(t0, d, v=.2, hp=False):
    n = int(d * R); x = np.random.randn(n)
    if hp: x = x - np.concatenate([[0], x[:-1]])
    add(t0, x * np.hanning(n) * v)
def pluck(t0, f, v=.1):   # 기타 줄 튕기는 소리 (간단한 카플러스-스트롱)
    n = int(1.4 * R); p = max(2, int(R / f)); buf = np.random.uniform(-1, 1, p); o = np.zeros(n)
    for i in range(n): o[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    add(t0, o * v)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t_night = ev.get('night', [-99])[0]
# 풀벌레 (밤 장면 빼고 내내)
for k in range(int(D * 3)):
    t = k / 3 + np.random.rand() * .2
    if t_night - .2 < t < t_night + 3.2: continue
    for j in range(3): tone(t + j * .045, 4200 + np.random.rand() * 300, .03, .012, 'sine', 60)
# 가락: 느긋하게 (밤 장면엔 멈춤)
M = [64, 67, 71, 69, 67, 64, 62, 64, 0, 60, 64, 67, 69, 67, 64, 0, 62, 66, 69, 67, 66, 62, 64, 0, 59, 62, 66, 64, 62, 59, 60, 0]
t = .4; i = 0
while t < D - .4:
    if not (t_night - .3 < t < t_night + 3.2):
        m = M[i % len(M)]
        if m: pluck(t, nt(m), .09)
        if i % 4 == 0: pluck(t, nt(40 if (i // 4) % 2 == 0 else 45), .06)
    t += .42; i += 1
for s in ev.get('open', []): [tone(s + k * .06, f, .4, .05, 'tri', 5) for k, f in enumerate((784, 988, 1175))]
for s in ev.get('place', []): tone(s + .35, 140, .18, .25, 'sine', 18); noise(s + .35, .12, .15)
if t_night > 0:
  for k in range(10): tone(t_night + .3 + k * .24, 1800 if k % 2 else 1500, .05, .06, 'square', 40)   # 째깍
for s in ev.get('toast', []): [tone(s + k * .08, f, .6, .05, 'tri', 4) for k, f in enumerate((1047, 1319, 1568))]
for s in ev.get('photo', []): noise(s, .08, .5, True); tone(s + .05, 2400, .05, .05, 'square', 50); [tone(s + .4 + k * .07, f, .6, .05, 'tri', 4) for k, f in enumerate((1568, 2093, 2637))]
for s in ev.get('fly', []):
    for k in range(16): noise(s + k * .18, .07, .12)
for s in ev.get('meet', []): [tone(s + k * .07, f, .7, .06, 'tri', 3) for k, f in enumerate((1047, 1319, 1568, 2093))]
for s in ev.get('drop', []): tone(s, 2093, .3, .05, 'tri', 6)
for s in ev.get('book', []): noise(s, .3, .08, True)
for s in ev.get('pick', []): tone(s, 1318, .25, .04, 'tri', 7)
for s in ev.get('rare', []): [tone(s + k * .1, 1046 * 2 ** (k / 12 * 2), 1.2, .05, 'sine', 2) for k in range(8)]
for s in ev.get('tab', []): noise(s, .12, .1, True); tone(s + .02, 880, .15, .04, 'tri', 10)
for s in ev.get('reward', []): [tone(s + k * .09, f, .9, .06, 'tri', 3) for k, f in enumerate((784, 988, 1175, 1568, 1976))]
out = out / np.max(np.abs(out)) * .85
w = wave.open(sys.argv[4], 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
