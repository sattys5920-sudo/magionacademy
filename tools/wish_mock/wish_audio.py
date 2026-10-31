# 첫눈의 소원 영상 소리: python3 wish_audio.py <wish_log.json> <영상 길이> <로그→영상 시각 차이> <출력.wav>
#   눈 오는 밤 오르골(직접 만든 가락) · 쪽지 떨어지는 방울 · 펼치는 종이 · 응원 별 · 글씨 쓰는 소리 · 날려 보내기 · 별자리
import sys, json, wave, numpy as np
R = 44100; L = json.load(open(sys.argv[1])); D = float(sys.argv[2]); OFF = float(sys.argv[3]); N = int(R * (D + 1)); out = np.zeros(N)
ev = {}
for t, k in L: ev.setdefault(k, []).append(t + OFF)
def add(t0, s):
    i = int(max(0, t0) * R); j = min(N, i + len(s)); out[i:j] += s[:j - i]
def env(n, a=.01, r=3): t = np.arange(n) / R; return np.minimum(1, t / a) * np.exp(-t * r)
def tone(t0, f, d, v=.2, kind='sine', dec=3):
    n = int(d * R); t = np.arange(n) / R; w = np.sin(2 * np.pi * f * t) if kind == 'sine' else (2 * np.abs(2 * ((f * t) % 1) - 1) - 1); add(t0, w * env(n, r=dec) * v)
def noise(t0, d, v=.2, hp=False):
    n = int(d * R); x = np.random.randn(n)
    if hp: x = x - np.concatenate([[0], x[:-1]])
    add(t0, x * np.hanning(n) * v)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t_sky = ev['sky'][0]
# 오르골 (직접 만든 겨울 가락 · 별자리부터는 느리고 낮게)
M = [76, 79, 81, 79, 76, 74, 76, 0, 72, 74, 76, 79, 77, 76, 74, 0, 74, 77, 79, 77, 74, 72, 74, 0, 71, 72, 74, 76, 72, 0, 0, 0]
t = .5; i = 0
while t < D - .5:
    st = .46 if t < t_sky else .6; m = M[i % len(M)]
    if m: tone(t, nt(m), 1.4, .08, 'sine', 2.2); tone(t, nt(m + 12), .5, .02, 'tri', 5)
    if i % 4 == 0: tone(t, nt(52 if (i // 4) % 2 == 0 else 48), 2, .04, 'sine', 1.2)
    t += st; i += 1
for s in ev.get('fall', []): [tone(s + k * .35, 2093 + k * 220, .8, .03, 'sine', 3) for k in range(6)]
for s in ev.get('land', []): [tone(s + k * .12, f, .5, .05, 'tri', 5) for k, f in enumerate((1568, 1976, 2349))]
for s in ev.get('pick', []): tone(s, 1318, .3, .05, 'tri', 7)
for s in ev.get('open', []): noise(s, .35, .08, True); tone(s + .1, 659, .4, .04, 'tri', 5)
for s in ev.get('cheer', []): [tone(s + k * .05, 1046 * 2 ** (k / 12), .6, .05, 'tri', 3) for k in range(10)]
for s in ev.get('toast', []): tone(s, 1568, .5, .05, 'sine', 4); tone(s + .08, 2093, .5, .04, 'sine', 4)
for s in ev.get('type', []): noise(s, .04, .05, True)
for s in ev.get('write', []): noise(s, .3, .06, True)
for s in ev.get('send', []): noise(s, 2.4, .05, True); [tone(s + .3 + k * .14, 880 * 2 ** (k / 12), 1, .04, 'tri', 2) for k in range(14)]
for s in ev.get('starborn', []): [tone(s + k * .06, f, .8, .06, 'tri', 3) for k, f in enumerate((1568, 2093, 2637, 3136))]
for s in ev.get('sky', []): [tone(s, f, 6, v, 'sine', .5) for f, v in ((130.8, .08), (196, .05), (261.6, .04))]
for k in range(14): tone(t_sky + .8 + k * .18, 1046 * 2 ** ([0, 4, 7, 12, 7, 4, 0, 2, 5, 9, 12, 9, 5, 2][k] / 12), .9, .04, 'tri', 3)
for s in ev.get('link', []): [tone(s + k * .15, 1568 + (k % 3) * 200, .4, .03, 'sine', 5) for k in range(13)]
for s in ev.get('title', []): [tone(s, f, 3, .06, 'sine', 1) for f in (261.6, 329.6, 392, 523.3)]
for s in ev.get('reward', []): [tone(s + k * .07, f, .6, .06, 'tri', 4) for k, f in enumerate((1047, 1319, 1568, 2093))]
out = out / np.max(np.abs(out)) * .85
w = wave.open(sys.argv[4], 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
