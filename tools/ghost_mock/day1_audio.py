# 1 일째 영상 소리: python3 day1_audio.py <ghost_log.json> <영상 길이(초)> <로그→영상 시각 차이(초)> <출력.wav>
#   으스스한 바닥 소리 · 발자국 · 등불 지직 · 속삭임 · 심장 소리 · 깜짝 소리 → 마틸다가 말하면 오르골 가락
import sys, json, wave, numpy as np
R = 44100; L = json.load(open(sys.argv[1])); D = float(sys.argv[2]); OFF = float(sys.argv[3]); N = int(R * (D + 1)); out = np.zeros(N)
ev = {}
for t, k in L: ev.setdefault(k, []).append(t + OFF)
def add(t0, s):
    i = int(max(0, t0) * R); j = min(N, i + len(s)); out[i:j] += s[:j - i]
def env(n, a=.01, r=3): t = np.arange(n) / R; return np.minimum(1, t / a) * np.exp(-t * r)
def tone(t0, f, dur, v=.2, kind='sine', dec=3):
    n = int(dur * R); t = np.arange(n) / R; w = np.sin(2 * np.pi * f * t) if kind == 'sine' else (2 * np.abs(2 * ((f * t) % 1) - 1) - 1); add(t0, w * env(n, r=dec) * v)
def noise(t0, dur, v=.2, lp=.3, shape=None):
    n = int(dur * R); x = np.random.randn(n); y = np.zeros(n); a = 0
    for k in range(n): a = a * (1 - lp) + x[k] * lp; y[k] = a
    add(t0, y * (shape if shape is not None else np.hanning(n)) * v)
nt = lambda m: 440 * 2 ** ((m - 69) / 12)
t_rev = ev['reveal'][0]; t_sc = ev['scare'][0]
# 바닥에 깔리는 낮은 웅웅 (깜짝 소리까지 점점 커져요)
n = int(t_sc * R); t = np.arange(n) / R; dr = (np.sin(2 * np.pi * 55 * t) + .6 * np.sin(2 * np.pi * 58.3 * t) + .3 * np.sin(2 * np.pi * 82.4 * t)) * (.04 + .08 * t / t_sc) * np.minimum(1, t / 2); add(0, dr)
noise(0, t_sc, .05, .02, np.minimum(1, np.arange(int(t_sc * R)) / R / 3))   # 밤바람
for s in ev.get('step', []):   # 뒤에서 들리는 발자국 (나무 바닥 같은 둔탁한 소리)
    noise(s, .12, .55, .25, np.exp(-np.arange(int(.12 * R)) / R * 40)); tone(s, 90, .15, .2, 'sine', 30)
for s in ev.get('flick', []):   # 등불 지직
    noise(s, .1, .25, .9, np.ones(int(.1 * R)) * (np.random.rand(int(.1 * R)) > .5)); tone(s, 120, .1, .05, 'tri', 10)
for s in ev.get('whisper', []):   # 속삭임: 숨소리 같은 높은 바람 + 흔들리는 음
    n = int(1.6 * R); x = np.random.randn(n); y = x - np.concatenate([[0], x[:-1]]); add(s, y * np.hanning(n) * .05)
    tone(s, 660, 1.5, .03, 'sine', 1.5); tone(s + .1, 698, 1.4, .025, 'sine', 1.5)
th = ev['heart'][0]   # 심장 소리: 점점 빨라져요
k = 0; t0 = th
while t0 < t_sc - .1: tone(t0, 55, .18, .45, 'sine', 18); tone(t0 + .16, 50, .16, .32, 'sine', 18); t0 += max(.42, .8 - k * .08); k += 1
# 깜짝 소리: 불협화음 + 쾅
for f in (311, 330, 466, 494, 698): tone(t_sc, f, 1.4, .12, 'tri', 2.5)
noise(t_sc, .5, .9, .6, np.exp(-np.arange(int(.5 * R)) / R * 9)); tone(t_sc, 45, 1.2, .5, 'sine', 3)
# 마틸다가 말하기 시작하면 오르골 (졸업식과 같은 가락을 밝은 조로)
M = [72, 76, 79, 77, 76, 72, 74, 0, 71, 74, 77, 76, 74, 71, 72, 0, 69, 72, 76, 74, 72, 69, 71, 0, 67, 71, 74, 72, 0, 0]
t0 = t_rev + .8; i = 0
while t0 < D - .5:
    m = M[i % len(M)]
    if m: tone(t0, nt(m + 2), 1.3, .09, 'sine', 2.4); tone(t0, nt(m + 14), .5, .025, 'tri', 5)
    if i % 4 == 0: tone(t0, nt(50 if (i // 4) % 2 == 0 else 45), 1.8, .045, 'sine', 1.3)
    t0 += .48; i += 1
for c in ev.get('card', []): [tone(c - 3 + k * .07, f, .5, .06, 'tri', 5) for k, f in enumerate((1047, 1319, 1568))]
out = out / np.max(np.abs(out)) * .85
w = wave.open(sys.argv[4], 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(R); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
