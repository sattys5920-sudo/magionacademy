// 「낡은 양호실의 누비」 연출 모음 (index.html이 필요할 때 불러요) — 장면 · 대사 · 꿰매기 · 바늘땀 풀기
//   누비 말투: 1~6 일째 한두 낱말 · 소리 나는 대로 · 다정한 말 없음 → 7~9 일째 길게 → 마지막에 입이 풀리면 맞춤법대로
//   말줄임: 문장 가운데 .... / 문장 끝 ....... · 숫자와 단위 띄어 쓰기
//   window.NubiFX = { say, choose, intro, d1, walkLine, d2end, d3dish, d3end, sew, d4end, night5, d6, burst7, reveal7, d8, unpick, finale, gyeobi, evening, card }
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
let A = null;
const SHEET = Object.assign(new Image(), { src: 'art/nubi_s.png?v=e37a79d4' }), FRIEND = Object.assign(new Image(), { src: 'art/nubi_friend.png?v=1' });
// ---------- 소리 ----------
let AC = null;
const ac = () => { try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); return AC; } catch(e){ return null; } };
const vol = () => (A && A.vol != null ? A.vol : 1);
function tone(f, d, type = 'sine', v = .2, at = 0, f2){ const C = ac(); if (!C || !(vol() > 0)) return; const t = C.currentTime + at, o = C.createOscillator(), g = C.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d); g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(v * vol(), t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(g); g.connect(C.destination); o.start(t); o.stop(t + d + .05); }
function noise(d, v = .2, at = 0, freq = 1200, type = 'lowpass'){ const C = ac(); if (!C || !(vol() > 0)) return; const t = C.currentTime + at, b = C.createBuffer(1, Math.max(1, C.sampleRate * d), C.sampleRate), a = b.getChannelData(0); for (let i = 0; i < a.length; i++) a[i] = (Math.random() * 2 - 1) * (1 - i / a.length);
  const s = C.createBufferSource(), f = C.createBiquadFilter(), g = C.createGain(); s.buffer = b; f.type = type; f.frequency.value = freq; g.gain.value = v * vol(); s.connect(f); f.connect(g); g.connect(C.destination); s.start(t); }
const SND = {
  flick: () => { noise(.09, .25, 0, 3000, 'highpass'); tone(120, .08, 'square', .04); },
  creak: () => tone(220, .5, 'sawtooth', .04, 0, 150),
  drone: d => { tone(55, d, 'sine', .06); tone(58.3, d, 'sine', .04); },
  scare: () => { [311, 330, 466, 494].forEach(f => tone(f, 1.1, 'triangle', .08)); noise(.4, .6, 0, 900); tone(45, 1, 'sine', .4); },
  sew: () => { noise(.06, .25, 0, 5000, 'highpass'); tone(1400, .04, 'square', .02); },
  pick: () => tone(880, .2, 'triangle', .06),
  card: () => [1047, 1319, 1568].forEach((f, k) => tone(f, .5, 'triangle', .06, k * .07)),
  rip: () => { noise(.5, .7, 0, 2200, 'bandpass'); tone(90, .4, 'sawtooth', .1, 0, 50); },
  sparkle: () => [1568, 2093, 2637, 3136].forEach((f, k) => tone(f, .6, 'triangle', .07, k * .06)),
  whisper: () => { noise(1.4, .05, 0, 2500, 'bandpass'); tone(330, 1.2, 'sine', .02); },
  warm: () => [523, 659, 784, 1047].forEach((f, k) => tone(f, 1.6, 'sine', .06, k * .18)),
};
// ---------- 화면 부품 ----------
const css = document.createElement('style'); css.textContent = `
#nbsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:420;display:none}
#nbsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid var(--bc,#C8C0B8);border-radius:14px;padding:12px}
#nbsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#3A2E5A;overflow:hidden;display:flex;align-items:center;justify-content:center}#nbsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}#nbsay .fc img{width:60px;height:60px;image-rendering:pixelated}#nbsay.nf .fc{display:none}
#nbsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:var(--bc,#E0DCD6);margin-bottom:3px}#nbsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px;white-space:pre-line}
#nbsay .tap{position:absolute;right:12px;bottom:6px;font-size:10px;color:#C8C0B8;animation:nbb 1s infinite}@keyframes nbb{50%{opacity:.2}}
#nbpick{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:421;display:none;flex-direction:column;gap:8px;max-width:560px;margin:0 auto}
#nbpick button{min-height:46px;border-radius:12px;border:2px solid #C8C0B8;background:rgba(30,22,52,.97);color:#F1E9FF;font-family:var(--f-px);font-size:14px;padding:8px 12px;text-align:left}
#nbcard{position:fixed;left:50%;top:40%;z-index:425;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;width:min(86vw,320px);padding:14px 16px;border-radius:10px;background:#efe6d2;color:#3a2c26;box-shadow:0 0 0 3px #b8a888,0 10px 30px rgba(0,0,0,.6);pointer-events:none}
#nbcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#nbcard h3{margin:0 0 8px;font:16px var(--f-pxb);color:#5a3a2a}#nbcard li{list-style:none;font-family:var(--f-px);font-size:14px;line-height:1.9;border-bottom:1px dashed #c8b898}#nbcard ul{margin:0;padding:0}#nbcard p{margin:0;font-family:var(--f-px);font-size:14px;line-height:1.7}
#nbfog{position:fixed;inset:0;z-index:399;pointer-events:none;background:radial-gradient(circle at 50% 46%,rgba(0,0,0,0) 0,rgba(6,4,14,.6) 38%,rgba(2,2,8,.94) 75%);opacity:0;transition:opacity 2s}
#nbfl{position:fixed;inset:0;z-index:430;pointer-events:none;background:#000;opacity:0}
#nbbig{position:fixed;left:50%;top:42%;z-index:432;width:min(56vw,240px);height:min(56vw,240px);transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;image-rendering:pixelated;transition:opacity .5s,transform .5s}
#nbstars{position:fixed;inset:0;z-index:409;pointer-events:none;width:100vw;height:100vh}
#nbmini{position:fixed;inset:0;z-index:440;display:flex;align-items:center;justify-content:center;background:rgba(10,8,20,.82)}
#nbmini .bx{width:min(92vw,360px);background:#211733;border:1px solid #4E3C72;border-radius:16px;padding:12px;display:flex;flex-direction:column;gap:8px}
#nbmini .hd{display:flex;justify-content:space-between;font:16px var(--f-pxb);color:#F6F0FF}#nbmini .hd span{color:#FFD866;font-size:13px}
#nbmini canvas{width:100%;aspect-ratio:1/1;border-radius:10px;touch-action:none;image-rendering:pixelated;background:#857e7c}
#nbmini .tip{font-family:var(--f-px);font-size:13px;color:#BDB0D6;text-align:center;min-height:18px}`;
document.head.appendChild(css);
const el = (id, h, tag = 'div') => { let d = document.getElementById(id); if (d) return d; d = document.createElement(tag); d.id = id; if (h) d.innerHTML = h; document.body.appendChild(d); return d; };
const UI = () => ({ say: el('nbsay', '<div class="bx"><div class="fc"></div><div><b></b><p></p></div><span class="tap">▼</span></div>'), pick: el('nbpick'), card: el('nbcard'), fog: el('nbfog'), fl: el('nbfl') });
const cleanup = () => ['nbsay', 'nbpick', 'nbcard', 'nbfog', 'nbfl', 'nbbig', 'nbstars', 'nbmini'].forEach(id => document.getElementById(id)?.remove());
// 누비 칸 (그림 384×96 · 32 칸): [줄, 칸]
const FR = { t0: [0, 0], rib0: [0, 4], fix: [0, 8], s1: [1, 0], s2: [1, 4], s2r: [1, 8], s1r: [2, 0], g0: [2, 4], g1: [2, 5], g2: [2, 6], burst: [2, 7] };
// 초상화: 인형이 액자 정중앙에 오게 (인형은 칸 안 x 9~23 · y 11~31 → 가운데 16 · 21)
function drawNubi(q, fk, size){ q.imageSmoothingEnabled = false; q.clearRect(0, 0, size, size); const [r, c] = FR[fk] || FR.t0; q.drawImage(SHEET, c * 32 + 4, r * 32 + 9, 24, 24, 0, 0, size, size); }
function face(fc, who){
  fc.innerHTML = '';
  if (who === '누비'){ const cv = document.createElement('canvas'); cv.width = cv.height = 48; fc.appendChild(cv); drawNubi(cv.getContext('2d'), (A && A.frame && A.frame()) || 't0', 48); }
  else if (A && A.faceHTML){ fc.innerHTML = A.faceHTML(who) || ''; }
}
const nm = () => (A && A.me && A.me.nick) || '나';
const fill = t => String(t).replace(/\{나\}/g, nm());
async function say(who, t, hold = 1400){
  const u = UI(), s = fill(t), col = who === '누비' ? '#C8C0B8' : who === '나' ? '#FFD8A8' : who === '' ? '#BDB0D6' : '#9CC4E4';
  u.say.classList.toggle('nf', who === '나' || who === ''); face(u.say.querySelector('.fc'), who); u.say.style.setProperty('--bc', col);
  u.say.querySelector('b').textContent = who === '나' ? nm() : who; u.say.style.display = 'block'; const p = u.say.querySelector('p'); p.textContent = '';
  let skip = false; u.say.onclick = () => { skip = true; };
  for (let k = 1; k <= s.length && !skip; k++){ p.textContent = s.slice(0, k); await sleep(who === '누비' && A && A.mumble ? 55 : 32); } p.textContent = s;
  await new Promise(r => { let done = false; const go = () => { if (!done){ done = true; r(); } }; u.say.onclick = go; setTimeout(go, hold + s.length * 30); });
  u.say.style.display = 'none'; await sleep(140);
}
const nar = (t, hold = 1200) => say('', t, hold);
async function choose(opts){ const u = UI(); u.pick.innerHTML = opts.map((o, i) => `<button data-i="${i}">${fill(o)}</button>`).join(''); u.pick.style.display = 'flex'; SND.pick();
  const i = await new Promise(r => u.pick.querySelectorAll('button').forEach(b => b.onclick = () => r(+b.dataset.i))); u.pick.style.display = 'none'; SND.pick(); return i; }
async function card(h, ms){ const u = UI(); u.card.innerHTML = h; u.card.classList.add('on'); SND.card(); await sleep(ms); u.card.classList.remove('on'); await sleep(450); }
const flick = async (n = 2) => { const u = UI(); for (let i = 0; i < n; i++){ SND.flick(); u.fl.style.opacity = .85; await sleep(70 + Math.random() * 60); u.fl.style.opacity = 0; await sleep(90 + Math.random() * 120); } };
const shake = async () => { if (A && A.calm) return; const st = document.body.style; for (let i = 0; i < 8; i++){ st.transform = `translate(${(i % 2 ? 1 : -1) * (8 - i)}px,${(i % 3 - 1) * (6 - i * .6)}px)`; await sleep(40); } st.transform = ''; };
async function big(fk, ms = 900){ const b = el('nbbig', '', 'canvas'); b.width = b.height = 24; drawNubi(b.getContext('2d'), fk, 24); b.style.opacity = 1; b.style.transform = 'translate(-50%,-50%) scale(1.1)'; await sleep(ms); b.style.opacity = 0; b.style.transform = 'translate(-50%,-50%) scale(.6)'; await sleep(500); }
function stars(on){ let c = document.getElementById('nbstars'); if (!on){ c && c.remove(); return; } c = el('nbstars', '', 'canvas'); c.width = innerWidth; c.height = innerHeight; const q = c.getContext('2d'); const P = Array.from({ length: 90 }, () => ({ x: Math.random() * c.width, y: c.height + Math.random() * 200, v: 40 + Math.random() * 90, s: 1 + Math.random() * 3 }));
  let last = performance.now(); const go = now => { if (!document.getElementById('nbstars')) return; const dt = Math.min(.05, (now - last) / 1000); last = now; q.clearRect(0, 0, c.width, c.height); P.forEach(p => { p.y -= p.v * dt; if (p.y < -10){ p.y = c.height + 10; p.x = Math.random() * c.width; } q.fillStyle = Math.random() < .5 ? '#ffe9a8' : '#ffffff'; q.globalAlpha = .7; q.fillRect(p.x, p.y, p.s * 2, p.s * 2); }); requestAnimationFrame(go); }; requestAnimationFrame(go); }
const frameSet = fk => { if (A) A.frameOver = fk; };
async function run(api, fn){ A = api; api.bgm && api.bgm(true); try { return await fn(); } finally { frameSet(null); cleanup(); api.bgm && api.bgm(false); } }

// ================= 처음 (관리자가 연 날 · 낡은 양호실에 처음 들어가면) =================
const intro = api => run(api, async () => {
  const u = UI(); A.mumble = true; u.fog.style.opacity = .7; SND.drone(10); await sleep(900); await flick(2);
  await nar('먼지 냄새. 오래된 소독약 냄새.');
  u.fl.style.opacity = 1; frameSet('g0'); await sleep(900); await nar('어둠 속에 노란 점 하나가 떠 있다. 무언가가 이쪽을 보고 있다.', 1400); u.fl.style.opacity = 0;
  await flick(1); SND.creak(); await nar('인형 고개가 끼익, 천천히 이쪽으로 꺾인다.'); frameSet('t0');
  SND.scare(); shake(); await big('g0', 700);
  await say('누비', '....너.'); await say('누비', '이르믄.');
  let i = await choose(['이름을 말한다', '....넌 뭐야?']);
  if (i === 1){ await say('누비', '누비.'); await nar('인형은 빤히 본다. 오래.', 1400); await say('누비', '너느 니르믄.'); await choose(['이름을 말한다']); }
  await say('나', '....{나}.'); const n = nm();
  await say('누비', `${n}. ${n}. ....${n}.`, 1600); await nar('인형 고개가 반대쪽으로 천천히 꺾인다.'); await say('누비', '....기어캐써.');
  u.fog.style.opacity = .4; await nar('등 뒤에서 아주 작은 목소리가 들린다.'); await say('누비', '....또 와.');
});
// ================= 1 일째 · 실 한 가닥 =================
const d1 = api => run(api, async () => {
  A.mumble = true; frameSet('t0'); await nar('단추를 X 바늘땀 위에 대고 꿰맨다. 실이 지나갈 때마다 인형이 움찔한다.');
  await nar('두 눈이 동시에 이쪽을 본다. 아무 말이 없다. 오래.', 1600);
  await say('누비', '....이제.'); await say('누비', '다 보여.');
  await say('누비', '시를.'); await say('누비', '한 가닥.'); await say('누비', '....줘.');
  let i = await choose(['줄게', '뭐 하려고?']);
  if (i === 1){ await nar('인형은 대답하지 않고 빤히 본다.'); i = await choose(['....안 줄래', '알았어, 줄게']); if (i === 0){ await nar('돌아서는 순간 소매에서 실 한 가닥이 스르륵 빠져 인형 손으로 날아간다.', 1600); await say('누비', '....이미.'); await say('누비', '가져써.'); return { thr: 0 }; } }
  await nar('소매 끝 실을 한 가닥 뽑아 건넨다. 인형이 실을 품속에 넣는다. 아무 말도 안 한다.', 1600); return { thr: 1 };
});
// ================= 2 일째 · 산책 =================
const WALK = { town: '....마나. 이르미. 마나.', toxic: '....여기. 다 사라 이써.', barn: '....아라.', library: '....책. 다 이르미 이써.', classroom: '....매일. 여기. 다 아자?' };
const walkLine = (api, m) => run(api, async () => { A.mumble = true; if (m === 'barn') await nar('동물들이 일제히 누비 쪽을 본다.'); await say('누비', WALK[m] || '....'); if (m === 'barn') await nar('동물들이 조용해진다.'); });
const d2end = api => run(api, async () => { A.mumble = true; await nar('인형 몸에 아침에는 없던 바늘땀이 생겨 있다. 가까이 보면 작은 글씨 같은 무늬가 있다.', 1600); await say('누비', '보지 마.'); await say('누비', '....아직.'); });
// ================= 3 일째 =================
const d3dish = (api, dish) => run(api, async () => { A.mumble = true; await nar('인형은 먹지 않는다. 그릇 앞에 앉아 피어오르는 김만 본다.', 1500); await say('누비', '....다들.'); await say('누비', '추워.'); await say('나', '다들?'); await nar('대답이 없다.'); });
const d3end = api => run(api, async () => { A.mumble = true; await nar('먼지를 털자 방이 조금 밝아졌다.'); await say('누비', '....추워.'); });
// ================= 손가락으로 선 따라 긋기 (꿰매기 · 바늘땀 풀기) =================
function trace(opt){
  return new Promise(res => {
    const m = el('nbmini', `<div class="bx"><div class="hd"><b>${opt.title}</b><span>${opt.sub || ''}</span></div><canvas width="320" height="320"></canvas><div class="tip">${opt.tip || ''}</div></div>`);
    const cv = m.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
    const S = 4, W = 80, path = [];
    for (let i = 0; i <= opt.n; i++) path.push([10 + i * (60 / opt.n), 40 + (i % 2 ? -10 : 10)]);
    const pts = opt.back ? path.slice().reverse() : path; let k = 0, sp = [];
    const px = (x, y, c) => { g.fillStyle = c; g.fillRect(Math.round(x) * S, Math.round(y) * S, S, S); };
    const draw = () => {
      for (let y = 0; y < W; y++) for (let x = 0; x < W; x++){ const n = (x * 7 + y * 13) % 5; px(x, y, (x + y) % 2 ? ['#8d8683', '#857e7c', '#918a87'][n % 3] : ['#7d7674', '#878080', '#827b79'][n % 3]); }
      for (let i = 0; i < pts.length - 1; i++){
        const [x0, y0] = pts[i], [x1, y1] = pts[i + 1], dn = i < k;
        for (let t = 0; t <= 10; t++){ const x = x0 + (x1 - x0) * t / 10, y = y0 + (y1 - y0) * t / 10;
          if (opt.back){ if (!dn){ px(x, y, '#1e181c'); if (t % 3 === 0) px(x, y - 1, '#4e484b'); } else if (t === 0 || t === 10) px(x, y, '#3a3436'); }
          else { if (dn){ px(x, y, '#2e2228'); if (t % 3 === 0) px(x, y - 1, '#5a4a4a'); } else if (t % 2 === 0) px(x, y, '#f4ead8'); } }
      }
      if (k < pts.length){ const [x, y] = pts[k]; g.strokeStyle = 'rgba(255,233,168,.95)'; g.lineWidth = 3; g.beginPath(); g.arc(x * S + S / 2, y * S + S / 2, 14, 0, 7); g.stroke(); }
      sp = sp.filter(s => (s.t += 1) < 18); sp.forEach(s => { g.fillStyle = s.t % 2 ? '#ffe9a8' : '#ffffff'; g.fillRect(s.x + s.vx * s.t, s.y + s.vy * s.t, 4, 4); });
    };
    let raf = 0; const loop = () => { draw(); if (document.getElementById('nbmini')) raf = requestAnimationFrame(loop); }; loop();
    const at = e => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / r.width * 320, (e.clientY - r.top) / r.height * 320]; };
    let down = false;
    const mv = e => { if (!down || k >= pts.length) return; const [x, y] = at(e), [tx, ty] = pts[k]; if (Math.hypot(x - (tx * S + 2), y - (ty * S + 2)) < 26){ k++; SND.sew(); for (let i = 0; i < 4; i++) sp.push({ x: tx * S, y: ty * S, vx: (Math.random() - .5) * 5, vy: -Math.random() * 4, t: 0 });
      if (k >= pts.length){ SND.sparkle(); setTimeout(() => { cancelAnimationFrame(raf); m.remove(); res(true); }, 700); } } };
    cv.addEventListener('pointerdown', e => { down = true; cv.setPointerCapture && cv.setPointerCapture(e.pointerId); mv(e); });
    cv.addEventListener('pointermove', mv); cv.addEventListener('pointerup', () => { down = false; });
    if (A && A.autoTrace){ (async () => { for (const [x, y] of pts){ await sleep(60); const r = cv.getBoundingClientRect(); down = true; mv({ clientX: r.left + (x * S + 2) / 320 * r.width, clientY: r.top + (y * S + 2) / 320 * r.height }); } })(); }
  });
}
// ================= 4 일째 · 꿰매기 · 시침핀 =================
const sew = api => run(api, async () => { A.mumble = true; await say('누비', '꿰매.'); await say('누비', '....빨리.'); await trace({ title: '찢어진 팔 꿰매기', n: 8, tip: '' }); });
const d4end = api => run(api, async () => {
  A.mumble = true; await nar('꿰매다 보니 인형 몸 곳곳에 시침핀이 꽂혀 있다. 열 개가 넘는다.', 1600);
  await nar('핀마다 옆에 아주 작은 글씨가 수놓여 있다. 이름이다.', 1500); await nar(`....그리고.`);
  await say('나', '....이거, 내 이름이잖아.'); SND.scare(); shake(); await big('g1', 600);
  await say('누비', '빼지 마.'); await say('누비', '....빼면.'); await say('누비', '도라가.');
  await say('나', '뭐가 돌아가는데?'); await nar('대답이 없다. 인형 고개가 원래대로 돌아간다.');
  await say('누비', '....됐어.');
  await card('<h3>찢긴 쪽지</h3><p>그 인형에 이름이 새겨지면....</p><p style="color:#8a7a68">(뒤는 찢겨 나갔어요)</p>', 2600);
});
// ================= 5 일째 · 한밤의 이름 =================
const night5 = (api, names) => run(api, async () => {
  const u = UI(); A.mumble = true; u.fog.style.opacity = .85; SND.drone(12); await sleep(800);
  await nar('책장 틈으로 낮고 뭉개진 목소리가 새어 나온다.', 1500);
  for (const n of names.slice(0, 4)){ SND.whisper(); await nar(`「${n}.」`, 700); await nar('....', 500); }
  SND.whisper(); await nar(`「....${nm()}.」`, 1000); await nar('내 이름이다.', 1200);
  await nar('불 꺼진 방. 인형이 핀 하나하나를 쓰다듬고 있다. 이름을 부를 때마다 핀을 꾹 누른다.', 1800);
  frameSet('g2'); await nar('몸은 그대로, 고개만 천천히 돌아간다.'); await big('g2', 700);
  await say('누비', '....봐써.'); await say('누비', '가.');
});
// ================= 6 일째 · 문을 연 사람 =================
const sera6 = api => run(api, async () => {
  await say('세라 선생님', '....학생도 소문 들었구나.'); await say('세라 선생님', '....그 책장, 제가 열었어요.');
  const i = await choose(['선생님이요?', '왜 혼자 두면 안 되는데요?']);
  if (i === 0){
    await say('세라 선생님', '양호 선생님들끼리 대대로 전해 온 말이 있어요.'); await say('세라 선생님', '책장 뒤 그 방 아이를 혼자 두지 말 것. 함께 있어 줄 아이들이 올 때까지는 문을 잠가 둘 것.', 1800);
    await say('세라 선생님', '저도 선배 선생님한테 열쇠를 받았어요. 한 번도 안 열어 봤고요.'); await say('세라 선생님', '근데 이번 학생들은.... 서로 문을 두드려 주더라고요. 아픈 친구 데리고 오고, 물약 나눠 주고.', 1800);
    await say('세라 선생님', '그래서 열어 봤어요. 이 아이들이라면 함께 있어 줄 것 같아서.');
  } else { await say('세라 선생님', '....저도 몰라요. 찢긴 쪽지 뒷부분은 아무도 못 봤대요.'); await say('세라 선생님', '그건 그 아이가 말해 줄 때까지 기다려요.'); }
  await say('세라 선생님', '이 리본은 그 책장 열쇠에 늘 매여 있던 거예요. 이제 열쇠는 필요 없으니까.'); await say('세라 선생님', '바늘은.... 언젠가 필요할 거예요. 왜인지는 저도 몰라요. 그렇게 전해 왔어요.', 1600);
});
const d6 = api => run(api, async () => {
  A.mumble = true; await nar('인형이 문간에 서 있다. 처음으로 침대에서 내려와 있다.');
  await say('누비', '....저주.'); await say('누비', '인형.'); await say('누비', '누비가.'); await say('누비', '해써?'); await nar('아니라고 하지 않는다. 묻고 있다.');
  const i = await choose(['아니라고 믿어', '....솔직히 무서워', '그럼 이름은 왜 모았어?']);
  if (i === 0){ await nar('인형이 한참 말이 없다가 고개를 숙인다. 리본을 인형 목에 매어 준다.', 1600); }
  else if (i === 1){ await say('누비', '....응.'); await say('누비', '누비도.'); await say('누비', '누비가. 무서워.'); await nar('그날 저녁, 세라 선생님이 대신 인형 목에 리본을 매어 주었다.', 1600); }
  else { await say('누비', '....내일.'); await nar('리본을 인형 목에 매어 준다. 인형이 리본 끝을 오래 만지작거린다.', 1600); }
  return { a6: i };
});
// ================= 7 일째 · 터진 날 =================
const burst7 = api => run(api, async () => {
  A.mumble = true; SND.rip(); shake(); await nar('인형 옆구리가 크게 터져 있다. 솜이 방 안 가득, 창문 밖까지 흩어졌다.', 1700);
  await nar('인형은 침대에 쓰러진 채 움직이지 않는다.'); await say('누비', '....솜.......', 1600);
  await card('<h3>솜 줍기</h3><p>학교 어딘가에 떨어진 솜뭉치 하나를 주워 와요. 한 사람 한 개.</p>', 2600);
});
const reveal7 = (api, lines, a6) => run(api, async () => {
  A.mumble = false; frameSet('burst');
  await nar('모은 솜을 터진 자리에 채워 넣으려다 손이 멈춘다.'); await nar('터진 틈 사이로 안쪽이 보인다. 이름이 수놓인 바늘땀들. 그 위를 누르고 있는 핀들.', 1800);
  await nar('그중 하나에 내 이름이 있다.', 1300);
  await card(`<h3>${nm()}의 바늘땀</h3><ul>${(lines.length ? lines : ['그냥 조금 지친 날']).map(l => `<li>${l}</li>`).join('')}</ul>`, 3200 + lines.length * 500);
  await say('나', '....그날 이상하게 금방 괜찮아졌던 게.......', 1600);
  A.mumble = true; await say('누비', '....들켰다.......');
  await say('누비', '누비가 이르킨 거 아니야. 나쁘 니른 그냥 생겨.'); await say('누비', '누비는.... 그 아프믈 조금씩 가져온 것뿌니야.');
  await say('누비', '실 한 가다기 이써야 이어져. 이르미 이써야 다믈 자리가 생겨. 피늘 꼬자야 다시 너한테 안 도라가.', 2000);
  await say('누비', '바메 부른 건 주무 나니야. 이름 뒤에.... 괜차나, 해써. 너무 작아서 안 드려써.......', 2000);
  await say('누비', '다 들고 이쓰려고 했는데.... 누비가 못 버텨써. 미안해.');
  await say('누비', ['어제. 믿는다고 해 줘찌. ....그 말 붙잡고 버텨써.', '무섭다고 해 줘서 고마워써. 거짓마 란 해 줘서.', '어제 무러본 거. 이게 대다비야. ....화나써?'][a6 ?? 0], 1800);
  const i = await choose(['왜 말 안 했어', '바보야']);
  if (i === 0){ await say('누비', '말하면.... 다들 도로 가져가려고 할 거자나.'); await say('누비', '누비는 그게 시러써. 다들 웃는 게 조아써.'); }
  else { await say('누비', '....응.'); await say('누비', '누비, 바보야.'); }
  await nar('솜을 채우고 터진 자리를 임시로 여며 준다.');
});
// ================= 8 일째 · 찢긴 쪽지의 뒷부분 · 짝 정하기 =================
const d8note = api => run(api, async () => {
  A.mumble = true; await nar('어제 채운 솜 사이에서 누렇게 바랜 종이 반쪽이 삐져나와 있다.'); await say('누비', '....그거. 누비가 가지고 이써써. 아주 오래.');
  await card('<h3>쪽지</h3><p>그 인형에 이름이 새겨지면, 그 아이는 그 이름의 아픔을 대신 짊어진다.</p><p>혼자 두지 말 것.</p><p>자기 바늘땀은 자기가 풀 수 없으니, 함께 풀어 줄 이들이 있어야 한다.</p>', 5200);
  await say('누비', '....누비는 이 종이를 찌저써. 아무도 못 보게.'); await say('누비', '다들 아라 버리면.... 누비는 아무것도 아닌 인형이 되니까.');
});
const sera8 = api => run(api, async () => { await say('세라 선생님', '....그랬구나.'); await say('세라 선생님', '그래서 혼자 두면 안 된다고 했던 거네요. 혼자 두면 남의 아픔을 다 가져가 버리니까.', 1800); await say('세라 선생님', '그 바늘, 이제 쓸 때가 됐나 봐요.'); });
const d8 = api => run(api, async () => {
  A.mumble = true; await nar('은바늘을 꺼내자 인형이 한참 바늘을 본다.');
  await say('누비', '....풀면. 누비 몸. 텅 비어.'); await say('누비', '아무것도 안 든 인형이 돼.'); await say('누비', '그래도.... 와 줄 거야?');
  await nar('대답 대신 고개를 끄덕인다.');
  await say('누비', '....그럼.'); await say('누비', '한 땀씩. 누비가 정할게. 누가 누구 걸 풀지.'); await say('누비', '누구 건지는.... 풀어 보면 아라.');
  await say('누비', '그리고.... 이제 안 가져올게. 새로 아픈 거.'); await say('누비', '약속.');
});
// ================= 9 일째 · 바늘땀 풀기 =================
const unpick = (api, who, lines) => run(api, async () => {
  A.mumble = true; await say('누비', '....네 꺼는. 여기.');
  await trace({ title: '바늘땀 풀기', sub: '???의 바늘땀', n: 10, back: true });
  await nar(`${who}의 바늘땀.`, 1300);
  await card(`<h3>${who}의 바늘땀</h3><ul>${(lines.length ? lines : ['그냥 조금 지친 날']).map(l => `<li>${l}</li>`).join('')}</ul>`, 3000 + lines.length * 400);
  await say('누비', `${who}. 그날 마니 아파써.`);
  const MSG = ['나도 그날 힘들었어', '다음엔 같이 가자', '고생했어'];
  const i = await choose(MSG); await nar(`손에 실 한 가닥이 남는다. ${who}의 색이다.`); return MSG[i];
});
// ================= 10 일째 · 100 % =================
const finale = (api, late) => run(api, async () => {
  const u = UI(); A.mumble = false; frameSet('s1r'); stars(true); SND.sparkle();
  if (late){ await nar('화면이 밝아진다. 책장 문이 활짝 열려 있다.'); }
  else { await nar('남은 핀들이 하나씩 톡, 톡 빠져 바닥에 떨어진다.'); await nar('별가루가 한꺼번에 날아올라 창문 밖으로 흩어진다.'); }
  frameSet('fix'); await nar('인형 얼굴의 잿빛이 걷힌다. 그리고 꿰매져 있던 입의 실이, 스르륵 풀린다.', 1800); SND.warm();
  if (late){ await say('누비', `${nm()}. 왔구나.`); await say('누비', '누비 목소리, 처음 듣지? ....이렇게 생겼어.'); }
  else { await say('누비', '....아.'); await say('누비', '아, 아.'); await say('누비', '누비.'); await say('누비', '....말이, 똑바로 나와.'); }
  await nar('인형이 침대에서 내려와 방을 둘러본다. 빈 침대 둘, 활짝 열린 책장 문, 와 준 얼굴들.', 1800);
  await say('누비', '누비, 이제 아무것도 안 들고 있는데....'); await say('누비', '....다들 그래도 와 주네.');
  await say('누비', '아울라가 그랬어. 얇은 천도 겹쳐서 꿰매면 따뜻해진대. 누비 이름이 그런 뜻이래.', 1800);
  await say('누비', '누비는 혼자 다 드는 인형인 줄 알았어.'); await say('누비', '....아니었네. 같이 겹쳐 있어야 따뜻한 거였어.', 1600);
  await say('누비', '고마워.'); await say('누비', '진짜, 진짜 고마워.', 1600);
  await say('세라 선생님', '....열길 잘했네요.');
  stars(false); await card('<h3>받았어요</h3><ul><li>누비의 하트 헝겊 · 갖고 있으면 최대 체력 +10 %</li><li>작은 누비 인형 · 방에 둘 수 있어요</li></ul>', 3200);
});
// ================= 엔딩 뒤 · 겹이 =================
const seraThr = (api, first) => run(api, async () => {
  if (first){ await say('세라 선생님', '학생, 그 실 아직 갖고 있죠? 친구 바늘땀에서 나온 거요.'); await say('세라 선생님', '선생님한테 모아 줄래요? 누비한테 줄 게 있어서요. ....비밀이에요.', 1600); }
  const i = await choose(['실 주기', '나중에']); if (i) return false;
  await nar('손에 남아 있던 실을 선생님 손바닥에 올린다.'); await say('세라 선생님', '소중히 쓸게요.'); return true;
});
const gyeobi = (api, names) => run(api, async () => {
  A.mumble = false; frameSet('fix'); SND.warm();
  await nar('세라 선생님이 따뜻한 양호실 빈 침대에 앉아 실 가닥들을 무릎에 펼친다.', 1600);
  await say('세라 선생님', '양호 선생님은요, 바느질을 잘해야 해요. 붕대도 감고, 찢어진 가운도 꿰매고.'); await say('세라 선생님', '오늘은 그 솜씨를 조금 다르게 써 볼게요.');
  for (let i = 0; i < 6; i++){ SND.sew(); await sleep(260); }
  await nar('작은 몸통. 작은 팔. 단추 눈 두 개. 조각마다 다른 색이다. 우리 반의 색.', 1800);
  await say('누비', '선생님, 뭐 만들어?'); await say('세라 선생님', '....다 됐다.');
  await say('세라 선생님', '누비 거예요. 이 반 학생들이 준 실로 만들었어요.'); await say('세라 선생님', '누비는 늘 남 옆에 있어 줬잖아요. 이제 누비 옆에도 누가 있어야죠.', 1800);
  await nar('누비가 인형을 한참 바라보다가, 두 팔로 꼭 안는다.');
  await say('누비', '....따뜻해.'); await say('누비', `이 색, ${names[0] || ''} 색이다. 이건 ${names[1] || ''} 색. ....다 있어. 우리 반이 다 있어.`, 1800);
  await say('누비', '이름은.... 겹이. 겹쳐 있으면 따뜻하니까.'); await say('누비', '고마워. 이번엔 누비가.... 선물을 받았네.');
  await say('세라 선생님', '대대로 전해 온 말에 한 줄 더 보태야겠네요. 「혼자 두지 말 것. 이제는 아무도.」', 2000);
});
// ================= 저녁 한마디 · 평소 한마디 =================
const evening = (api, line, mumble = true) => run(api, async () => { A.mumble = mumble; await say('누비', line, 1600); });

window.NubiFX = { say, choose, card, intro, d1, walkLine, d2end, d3dish, d3end, sew, d4end, night5, sera6, d6, burst7, reveal7, d8note, sera8, d8, unpick, finale, seraThr, gyeobi, evening, FR, drawNubi, SHEET, FRIEND };
})();
