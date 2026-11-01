# 겨울 뜨개질 시안 영상 소리: python3 knit_audio.py <knit_log.json> <영상 길이> <짝 json | 시각 차이> <출력.wav>
#   직접 만든 오르골 가락 · 벽난로 타닥 · 물레 윙윙 · 바늘 딸깍 · 완벽 반짝 · 완성 · 선물 · 나무 뜨개 옷
import sys, json, wave, numpy as np
R = 44100; L = json.load(open(sys.argv[1])); D = float(sys.argv[2]); OFF = sys.argv[3]; N = int(R * (D + 1)); out = np.zeros(N)
if OFF.endswith('.json'):
    MP = json.load(open(OFF)); fx = lambda t: float(np.interp(t, [a for a, b in MP], [b for a, b in MP], left=None, right=None) if MP[0][0] <= t <= MP[-1][0] else MP[0][1] + (t - MP[0][0]) * (MP[-1][1] - MP[0][1]) / (MP[-1][0] - MP[0][0]))
else: fx = lambda t, o=float(OFF): t + o
ev = {}
for t, k in L: ev.setdefault(k, []).append(fx(t))
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
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
# 벽난로 타닥
for k in range(int(D * 5)):
    t = k / 5 + np.random.rand() * .15
    if np.random.rand() < .5: noise(t, .015 + np.random.rand() * .02, .05 + np.random.rand() * .05, True)
# 오르골 가락 (느긋한 3 박자 · 겨울)
M = [72, 76, 79, 77, 76, 74, 72, 0, 74, 77, 81, 79, 77, 76, 74, 0, 76, 79, 84, 83, 81, 79, 77, 76, 74, 72, 74, 76, 72, 0, 0, 0]
B = [48, 55, 53, 50]
t = .5; i = 0
while t < D - .5:
    m = M[i % len(M)]
    if m: tone(t, nt(m), 1.4, .07, 'sine', 2.5); tone(t, nt(m) * 2, .6, .015, 'sine', 5)
    if i % 8 == 0: tone(t, nt(B[(i // 8) % 4]), 2.6, .05, 'tri', 1.2)
    t += .36; i += 1
for s in ev.get('toast', []): [tone(s + k * .08, f, .6, .04, 'tri', 4) for k, f in enumerate((1047, 1319, 1568))]
for s in ev.get('line', []): [tone(s + k * .09, 260 + (k % 3) * 30, .05, .018, 'square', 40) for k in range(4)]
for s in ev.get('open', []): noise(s, .25, .06, True); tone(s + .05, 784, .3, .04, 'tri', 6)
for s in ev.get('pick', []): tone(s, 1318, .2, .05, 'tri', 8)
for s in ev.get('spin', []):
    n = int(.5 * R); tt = np.arange(n) / R; add(s, np.sin(2 * np.pi * (180 + 40 * np.sin(tt * 30)) * tt) * np.hanning(n) * .05)
for s in ev.get('perfect', []): tone(s, 1568, .25, .025, 'tri', 10)
for s in ev.get('good', []): tone(s, 1175, .2, .02, 'tri', 10)
for s in ev.get('miss', []): tone(s, 180, .2, .1, 'square', 12)
for s in ev.get('click', []): tone(s, 3000, .02, .05, 'square', 120); tone(s + .015, 2200, .02, .04, 'square', 120)   # 코가 바늘로 넘어가는 딸깍
for s in ev.get('flip', []): noise(s, .25, .07); tone(s + .1, 523, .2, .03, 'tri', 8)
for s in ev.get('tie', []): [tone(s + k * .06, f, .3, .04, 'tri', 6) for k, f in enumerate((659, 784))]
for s in ev.get('learn', []): [tone(s + k * .08, f, .7, .05, 'tri', 3) for k, f in enumerate((784, 988, 1175, 1568))]
for s in ev.get('insert', []): tone(s, 900, .06, .05, 'square', 40); tone(s + .03, 1400, .05, .04, 'square', 40)
for s in ev.get('wrap', []): [tone(s + k * .05, 600 + k * 60, .1, .03, 'sine', 12) for k in range(5)]
for s in ev.get('pull', []): tone(s, 520, .12, .05, 'tri', 10)
for s in ev.get('slip', []): tone(s, 3000, .03, .05, 'square', 100); tone(s + .02, 2200, .03, .04, 'square', 100)
for s in ev.get('card', []): [tone(s + k * .08, f, .7, .05, 'tri', 3) for k, f in enumerate((784, 988, 1175, 1568))]
for s in ev.get('done', []): [tone(s + k * .1, f, 1.2, .06, 'tri', 2.5) for k, f in enumerate((523, 659, 784, 1047, 1319))]
for s in ev.get('wear', []): noise(s, .4, .06); [tone(s + .2 + k * .07, f, .8, .04, 'sine', 3) for k, f in enumerate((880, 1109, 1319))]
for s in ev.get('gift', []): [tone(s + k * .08, f, .7, .05, 'tri', 3) for k, f in enumerate((784, 988, 1175, 1568))]
for s in ev.get('sparkle', []): [tone(s + k * .06, 1568 * 2 ** (k / 6), .5, .04, 'sine', 5) for k in range(6)]
for s in ev.get('stack', []): tone(s, 220, .15, .12, 'sine', 15); noise(s, .08, .08)
for s in ev.get('fin', []): [tone(s + k * .12, f, 1.6, .06, 'tri', 1.8) for k, f in enumerate((523, 659, 784, 1047, 784, 1047, 1319, 1568))]
out = out / np.max(np.abs(out)) * .85
w = wave.open(sys.argv[4], 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
