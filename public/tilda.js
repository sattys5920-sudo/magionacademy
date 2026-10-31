// 「수상한 기척」 연출 모음 (index.html이 필요할 때 불러요) — 등장 공포 연출 · 아침 인사 · 부탁 반응 · 일기장 조각 · 밤 이야기와 선택지 · 졸업식 · 다음 날 편지
//   마틸다는 처음부터 반말 · 해골 선생님께만 존댓말 · 말줄임: 문장 가운데 …. / 문장 끝 …….
//   window.TildaFX = { intro, morning, react, page, night, grad, letter, say, NAMES, HI, GOALS_TEXT }
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const NAMES = ['마틸다', '틸다', '틸'], HI = ['하이파이브', '새끼손가락', '이마 콩'], HI_SND = ['쉭', '띵', '콩'];
// ---------- 그림 ----------
const IMG = {}; const img = (k, src) => IMG[k] || (IMG[k] = Object.assign(new Image(), { src }));
const GH = () => img('gh', 'art/tilda.png?v=1'), SK = () => img('sk', 'art/tilda_skel.png?v=1'), DP = () => img('dp', 'art/tilda_diploma.png?v=1'), BT = () => img('bt', 'art/tilda_buttons.png?v=1'), CAP = () => img('cap', 'art/lpc/hat_grad.png?v=1'), BAT = () => img('bat', 'art/portraits/batri.png?v=1');
['gh', 'sk', 'dp', 'bt', 'cap'].forEach(k => ({ gh: GH, sk: SK, dp: DP, bt: BT, cap: CAP })[k]());
// ---------- 소리 (직접 만든 소리 · 효과음 설정을 따라요) ----------
let AC = null, A = null;
const ac = () => { try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); return AC; } catch(e){ return null; } };
const vol = () => (A && A.vol != null ? A.vol : 1);
function tone(f, d, type = 'sine', v = .2, at = 0, f2){ const C = ac(); if (!C || !(vol() > 0)) return; const t = C.currentTime + at, o = C.createOscillator(), g = C.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d); g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(v * vol(), t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(g); g.connect(C.destination); o.start(t); o.stop(t + d + .05); }
function noise(d, v = .2, at = 0, freq = 1200, type = 'lowpass'){ const C = ac(); if (!C || !(vol() > 0)) return; const t = C.currentTime + at, b = C.createBuffer(1, Math.max(1, C.sampleRate * d), C.sampleRate), a = b.getChannelData(0); for (let i = 0; i < a.length; i++) a[i] = (Math.random() * 2 - 1) * (1 - i / a.length);
  const s = C.createBufferSource(), f = C.createBiquadFilter(), g = C.createGain(); s.buffer = b; f.type = type; f.frequency.value = freq; g.gain.value = v * vol(); s.connect(f); f.connect(g); g.connect(C.destination); s.start(t); }
const SND = {
  step: () => { noise(.12, .5, 0, 500); tone(90, .15, 'sine', .25); },
  flick: () => { noise(.09, .25, 0, 3000, 'highpass'); tone(120, .08, 'square', .04); },
  whisper: () => { noise(1.6, .06, 0, 2500, 'bandpass'); tone(660, 1.4, 'sine', .03); tone(698, 1.3, 'sine', .025, .1); },
  heart: n => { for (let i = 0; i < n; i++){ const at = i * Math.max(.42, .8 - i * .08); tone(55, .18, 'sine', .5, at); tone(50, .16, 'sine', .35, at + .16); } },
  scare: () => { [311, 330, 466, 494, 698].forEach(f => tone(f, 1.3, 'triangle', .1)); noise(.5, .8, 0, 900); tone(45, 1.1, 'sine', .45); },
  drone: d => { tone(55, d, 'sine', .06); tone(58.3, d, 'sine', .04); },
  card: () => [1047, 1319, 1568].forEach((f, k) => tone(f, .5, 'triangle', .06, k * .07)),
  pick: () => tone(880, .25, 'triangle', .06),
  hi: k => k === 0 ? noise(.25, .4, 0, 4000, 'highpass') : k === 1 ? tone(1568, .5, 'sine', .08) : tone(330, .2, 'sine', .25),
  sparkle: () => [1568, 2093, 2637, 3136].forEach((f, k) => tone(f, .6, 'triangle', .07, k * .06)),
  page: () => { noise(.3, .2, 0, 3000, 'highpass'); tone(523, .3, 'triangle', .04, .1); },
  bell: () => { [[130.8, .35], [261.6, .18], [392, .08], [523, .05]].forEach(([f, v]) => tone(f, 5, 'sine', v)); },
  ascend: () => { for (let i = 0; i < 14; i++) tone(1046 * Math.pow(2, i / 12), 1.1, 'triangle', .05, i * .14); noise(3.2, .07, 0, 6000, 'bandpass'); },
  creak: () => { tone(220, .4, 'sawtooth', .04, 0, 160); },
};
// 오르골: 밤 이야기·졸업식 동안 (느리게 돌아가는 원래 가락)
const MB = [72, 76, 79, 77, 76, 72, 74, 0, 71, 74, 77, 76, 74, 71, 72, 0, 69, 72, 76, 74, 72, 69, 71, 0, 67, 71, 74, 72, 0, 0];
let mbT = null;
function musicbox(on, slow){ clearTimeout(mbT); mbT = null; if (!on) return; let i = 0; const st = slow ? 620 : 500; const nt = m => 440 * Math.pow(2, (m - 69) / 12);
  const go = () => { const m = MB[i % MB.length]; if (m){ tone(nt(m), 1.3, 'sine', .07); tone(nt(m + 12), .5, 'triangle', .02); } if (i % 4 === 0) tone(nt((i / 4) % 2 ? 43 : 48), 1.8, 'sine', .04); i++; mbT = setTimeout(go, st); }; go(); }
// ---------- 화면 부품 ----------
const css = document.createElement('style'); css.textContent = `
#tlsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:420;display:none}
#tlsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid var(--bc,#B8D8FF);border-radius:14px;padding:12px}
#tlsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden}#tlsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}#tlsay.nf .fc{display:none}
#tlsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:var(--bc,#CFE6FF);margin-bottom:3px}#tlsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px;white-space:pre-line}
#tlsay .tap{position:absolute;right:12px;bottom:6px;font-size:10px;color:#B8D8FF;animation:tlb 1s infinite}@keyframes tlb{50%{opacity:.2}}
#tlpick{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:421;display:none;flex-direction:column;gap:8px;max-width:560px;margin:0 auto}
#tlpick button{min-height:46px;border-radius:12px;border:2px solid #B8D8FF;background:rgba(30,22,52,.97);color:#F1E9FF;font-family:var(--f-px);font-size:14px;padding:8px 12px;text-align:left}
#tlcard{position:fixed;left:50%;top:40%;z-index:425;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 18px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #B8D8FF;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(184,216,255,.45);pointer-events:none;width:min(88vw,330px);text-align:center}
#tlcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#tlcard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}#tlcard canvas,#tlcard img{image-rendering:pixelated}
#tlcard ul{list-style:none;margin:0;padding:0;width:100%;display:flex;flex-direction:column;gap:6px}#tlcard li{display:flex;justify-content:space-between;gap:8px;background:#2A2040;border-radius:10px;padding:7px 10px;font-family:var(--f-px);font-size:13px;text-align:left}
#tlcard .pg{background:#F4E6C4;color:#3A2414;border-radius:6px;padding:12px;font-family:var(--f-px);font-size:14px;line-height:21px;border:3px solid #B89A62;box-shadow:inset 0 0 18px rgba(120,80,30,.35)}
#tlfog{position:fixed;inset:0;z-index:399;pointer-events:none;background:radial-gradient(circle at 50% 46%,rgba(0,0,0,0) 0,rgba(6,10,26,.55) 38%,rgba(2,4,14,.92) 75%);opacity:0;transition:opacity 2.4s}
#tldim{position:fixed;inset:0;z-index:398;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(160,200,255,0) 0,rgba(10,14,30,.5) 70%);opacity:0;transition:opacity 1s}
#tlfl{position:fixed;inset:0;z-index:430;pointer-events:none;background:#000;opacity:0}#tlwh{position:fixed;inset:0;z-index:431;pointer-events:none;background:#E8F4FF;opacity:0}
#tlws{position:fixed;left:50%;top:40%;z-index:405;transform:translateX(-50%);font-family:var(--f-px);font-size:15px;color:#CFE6FF;letter-spacing:3px;text-shadow:0 0 10px #8FB8FF;opacity:0;transition:opacity 1.2s,transform 3s;pointer-events:none}
#tlbig{position:fixed;left:50%;top:44%;z-index:432;width:300px;height:300px;transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;image-rendering:pixelated;filter:drop-shadow(0 0 18px #9CC8FF) drop-shadow(0 0 40px #6A9AFF)}
#tlttl{position:fixed;left:0;right:0;top:20%;z-index:426;text-align:center;font-family:var(--f-pxb);color:#FFE9A0;font-size:24px;text-shadow:0 0 14px #E8B84A,0 2px 0 #2A1440;opacity:0;transition:opacity .9s;pointer-events:none}#tlttl small{display:block;font-family:var(--f-px);font-size:13px;color:#E8DCFF;margin-top:6px;text-shadow:none}#tlttl.on{opacity:1}
#tlfx{position:fixed;inset:0;width:100vw;height:100vh;z-index:410;pointer-events:none;image-rendering:pixelated;opacity:0;transition:opacity .8s}#tlfx.on{opacity:1}
#tlpop{position:fixed;left:50%;top:44%;transform:translate(-50%,-50%) scale(.4);z-index:428;font-family:var(--f-pxb);font-size:42px;color:#FFF;text-shadow:0 0 18px #B8D8FF,0 0 36px #B8D8FF,-3px 0 #2A1A4A,3px 0 #2A1A4A,0 3px #2A1A4A;opacity:0;transition:all .35s cubic-bezier(.2,1.6,.4,1);pointer-events:none}#tlpop.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
#tlletter{position:fixed;inset:0;z-index:440;display:flex;align-items:center;justify-content:center;background:rgba(10,8,20,.7)}#tlletter .pp{width:min(88vw,340px);max-height:80vh;overflow:auto;background:#F4E6C4;border:4px solid #B89A62;border-radius:8px;padding:18px 16px;color:#3A2414;font-family:var(--f-px);font-size:14px;line-height:23px;box-shadow:0 0 30px rgba(0,0,0,.5);white-space:pre-line}
#tlletter button{display:block;margin:14px auto 0;min-height:40px;padding:0 22px;border-radius:10px;border:2px solid #8A6A3A;background:#E8D4A6;color:#3A2414;font-family:var(--f-pxb)}`;
document.head.appendChild(css);
const el = (id, h, tag = 'div') => { let d = document.getElementById(id); if (d) return d; d = document.createElement(tag); d.id = id; if (h) d.innerHTML = h; document.body.appendChild(d); return d; };
const UI = () => ({ say: el('tlsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div><span class="tap">▼</span></div>'), pick: el('tlpick'), card: el('tlcard'), fog: el('tlfog'), dim: el('tldim'), fl: el('tlfl'), wh: el('tlwh'), ws: el('tlws'), ttl: el('tlttl'), pop: el('tlpop') });
const cleanup = () => ['tlsay', 'tlpick', 'tlcard', 'tlfog', 'tldim', 'tlfl', 'tlwh', 'tlws', 'tlbig', 'tlttl', 'tlfx', 'tlpop'].forEach(id => document.getElementById(id)?.remove());
function face(q, who){ q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32);
  if (who === '마틸다') q.drawImage(GH(), 16, 4, 32, 32, 0, 0, 32, 32);
  else if (who === '해골 선생님'){ q.fillStyle = '#2A2238'; q.fillRect(0, 0, 32, 32); q.drawImage(SK(), 16, 8, 32, 32, 0, 0, 32, 32); }
  else if (who === '배트리'){ q.imageSmoothingEnabled = true; q.drawImage(BAT(), 0, 0, BAT().naturalWidth || 280, (BAT().naturalWidth || 280), 0, 0, 32, 32); } }
const TT = () => (A && A.t && A.t()) || {};
const rago = n => ((n.charCodeAt(n.length - 1) - 0xAC00) % 28 ? n + '이라고' : n + '라고');   // 받침에 맞춰 「틸이라고」 · 「틸다라고」
const fill = t => String(t).replace(/\{nm\}/g, NAMES[TT().nm ?? 0]).replace(/\{hi\}/g, HI[TT().hi ?? 0]).replace(/\{me\}/g, A ? A.me.nick : '').replace(/\{rago\}/g, rago(NAMES[TT().nm ?? 0]));
async function say(who, t, hold = 1400){   // 한 글자씩 · 누르면 바로 다 보이고, 한 번 더 누르면 넘어가요 (그냥 두어도 넘어가요)
  const u = UI(), s = fill(t), col = who === '마틸다' ? '#B8D8FF' : who === '나' ? '#FFD8A8' : '#FFE9A0';
  u.say.classList.toggle('nf', who === '나'); face(u.say.querySelector('canvas').getContext('2d'), who); u.say.style.setProperty('--bc', col);
  u.say.querySelector('b').textContent = who === '나' ? (A ? A.me.nick : '나') : who; u.say.style.display = 'block'; const p = u.say.querySelector('p'); p.textContent = '';
  let skip = false; u.say.onclick = () => { skip = true; };
  for (let k = 1; k <= s.length && !skip; k++){ p.textContent = s.slice(0, k); await sleep(32); } p.textContent = s;
  await new Promise(r => { let done = false; const go = () => { if (!done){ done = true; r(); } }; u.say.onclick = go; setTimeout(go, hold + s.length * 30); });
  u.say.style.display = 'none'; await sleep(140);
}
async function choose(opts){ const u = UI(); u.pick.innerHTML = opts.map((o, i) => `<button data-i="${i}">${o}</button>`).join(''); u.pick.style.display = 'flex'; SND.pick();
  const i = await new Promise(r => u.pick.querySelectorAll('button').forEach(b => b.onclick = () => r(+b.dataset.i))); u.pick.style.display = 'none'; SND.pick(); return i; }
async function card(h, ms, draw){ const u = UI(); u.card.innerHTML = h; draw && draw(u.card); u.card.classList.add('on'); SND.card(); await sleep(ms); u.card.classList.remove('on'); await sleep(450); }
const flick = async (n = 2) => { const u = UI(); for (let i = 0; i < n; i++){ SND.flick(); u.fl.style.opacity = .85; await sleep(70 + Math.random() * 60); u.fl.style.opacity = 0; await sleep(90 + Math.random() * 120); } };
const shake = async () => { if (A && A.calm) return; const st = document.body.style; for (let i = 0; i < 8; i++){ st.transform = `translate(${(i % 2 ? 1 : -1) * (8 - i)}px,${(i % 3 - 1) * (6 - i * .6)}px)`; await sleep(40); } st.transform = ''; };
// 빛나는 발자국 (내 뒤를 따라와요)
const FP = (() => { const c = document.createElement('canvas'); c.width = c.height = 24; const q = c.getContext('2d'); const rg = q.createRadialGradient(12, 14, 1, 12, 14, 10); rg.addColorStop(0, 'rgba(190,225,255,.55)'); rg.addColorStop(1, 'rgba(190,225,255,0)'); q.fillStyle = rg; q.fillRect(0, 0, 24, 24); q.fillStyle = 'rgba(220,240,255,.9)'; q.fillRect(7, 11, 3, 5); q.fillRect(14, 9, 3, 5); return c; })();
// 걸어갈 수 있는 칸 찾기 (내 자리에서 방향 d로 n칸 · 못 가면 가까운 칸)
const W = () => A.W;
function back(t, n){ const dirs = [[0, 1], [1, 0], [-1, 0], [0, -1]]; for (const [dx, dy] of dirs) if (W().isFree ? W().isFree(t.x + dx * n, t.y + dy * n) : true) return [t.x + dx * n, t.y + dy * n, dx, dy]; return [t.x, t.y + n, 0, 1]; }

// ================= 등장: 어느 날 밤, 수상한 기척 =================
async function intro(api){
  A = api; const u = UI(), t0 = W().meTile(), m = t0.m; api.bgm(true);
  try {
    u.fog.style.opacity = .55; SND.drone(14); await sleep(1400); await flick(1); await sleep(600);
    // 뒤에서 발자국이 하나씩
    const [bx, by, dx, dy] = back(t0, 1); const fps = [];
    const fpPut = () => W().setProps(m, fps.map(([x, y], i) => ({ id: 'tlfp' + i, x, y, img: FP, pxc: FP.getContext('2d'), sw: 24, sh: 24, ax: 12, ay: 16, solid: false, light: { r: 12, c: [190, 225, 255], a: .5 } })), 'tlfp');
    for (const k of [3, 2]){ SND.step(); fps.push([t0.x + dx * k, t0.y + dy * k]); fpPut(); await sleep(650); }
    W().say('me', '....?'); await sleep(1300);
    W().faceTo(t0.x + dx * 3, t0.y + dy * 3); u.fog.style.opacity = .75; await sleep(1700);   // 돌아봐도 아무도 없어요
    SND.step(); fps.push([bx, by]); fpPut(); await sleep(600);   // 발자국만 한 칸 더 가까이
    W().say('me', '.......'); await sleep(1400);
    fps.length = 0; fpPut(); await flick(3); u.fog.style.opacity = .9;
    W().faceTo(t0.x - dx * 3, t0.y - dy * 3); await sleep(900);
    u.ws.textContent = '....안녕.'; SND.whisper(); u.ws.style.opacity = .85; u.ws.style.transform = 'translateX(-50%) translateY(-14px)'; await sleep(1800); u.ws.style.opacity = 0; await sleep(900);
    W().say('me', '누, 누구야.......'); await sleep(1600);
    SND.heart(5); await sleep(1800);
    // 천천히 돌아보면.... 코앞에
    api.gh.show(m, bx, by, 1, .95); W().faceTo(bx, by); SND.scare();
    const big = el('tlbig', '', 'canvas'); big.width = big.height = 40; const q = big.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(GH(), 12, 0, 40, 40, 0, 0, 40, 40);
    if (!api.calm){ u.wh.style.transition = 'none'; u.wh.style.opacity = .9; big.style.transition = 'none'; big.style.opacity = 1; big.style.transform = 'translate(-50%,-50%) scale(1.15)'; }
    else { big.style.transition = 'opacity .6s'; big.style.opacity = .8; big.style.transform = 'translate(-50%,-50%) scale(.9)'; }
    shake(); W().say('me', '!'); await sleep(90); u.wh.style.transition = 'opacity .7s'; u.wh.style.opacity = 0;
    await sleep(520); big.style.transition = 'opacity .5s, transform .5s'; big.style.opacity = 0; big.style.transform = 'translate(-50%,-50%) scale(.6)';
    u.fog.style.transition = 'opacity 1.2s'; u.fog.style.opacity = .35; await sleep(1300); musicbox(true); u.dim.style.opacity = 1;
    await say('마틸다', '앗, 놀랐어? 미안, 미안. 말 걸 타이밍을 계속 보고 있었어.');
    await say('마틸다', '나는 마틸다야. 1926 년에 입학했어. ....졸업은 못 했지만.');
    await say('마틸다', '근데 너, 나 보이지? 100 년 만이야. 나 보이는 사람.');
    await say('마틸다', '그래서 말인데.... 부탁 하나만 들어줄래? 학교가 너무 바뀌어서 길을 모르겠어.', 1600);
    await say('마틸다', '닷새만. 딱 닷새만 같이 다녀 줘. ....싫다고 해도 따라갈 거지만. 히히.', 1600);
  } finally { musicbox(false); W().setProps(m, [], 'tlfp'); cleanup(); api.bgm(false); }
}
// ================= 아침 인사 (그날 처음 · 오늘 부탁 카드) =================
const MORNING = {
  1: ['....아직 무서워? 괜찮아, 낮에는 나도 좀 덜 무서워.'],
  2: ['좋은 아침, {nm}. 이름 불러 주는 사람이 있으니까 아침이 아침 같아.', '오늘은 100 년 만에 학생처럼 지내 보고 싶어. 맛있는 냄새도 맡고.'],
  3: ['어젯밤에 꿈을 꿨어. 유령도 꿈을 꾸나 봐. 일기장이 막 날아가는 꿈이었어.', '....진짜로 찾아볼래? 학교 여기저기에 떨어져 있을 것 같아.'],
  4: ['오늘은 부탁이 있어. 네 친구들. 나도 인사하고 싶어. 안 보여도.'],
  5: ['....오늘은 이따가 할래. 비밀 인사. 마지막에. 아껴 둘래.', '해골 선생님이 광장에서 졸업식을 열어 준대. ....같이 가 줄 거지?'],
};
async function morning(api, day, goals, skipped){
  A = api; api.bgm(true); const u = UI(); u.dim.style.opacity = 1;
  try {
    if (day > 1){ SND.hi(TT().hi ?? 0); await say('나', `(${HI[TT().hi ?? 0]}. ${HI_SND[TT().hi ?? 0]}.)`, 600); }
    if (skipped) await say('마틸다', '어제는 바빴어? 나는 계단에 앉아 있었어. 삐걱, 삐걱. ....보고 싶었어. 아, 이건 비밀.', 1600);
    if (day === 5){ const b = TT().btn; await say('마틸다', MORNING[5][0]); await say('마틸다', `(교복 매무새를 고쳐요) 어때? ${b === 0 ? (TT().dug ? '단추 달았어, 우리가 찾은 거!' : '단추는.... 결국 못 찾았네. 그래도 괜찮아.') : b === 1 ? '네 단추는 마음 주머니에 있어.' : '단추 하나 없지만 예쁘대. 누가 그랬어.'}`, 1600); await say('마틸다', MORNING[5][1]); }
    else for (const l of MORNING[day]) await say('마틸다', l);
    await card(`마틸다의 부탁 · ${day} 일째<small>${['', '수상한 기척', '100 년 만의 맛', '잃어버린 일기장', '친구 만들기', '졸업식'][day]}</small><ul>${goals.map(g => `<li><span>${g.t}</span><span>${g.n > 1 ? `0 / ${g.n}` : '☐'}</span></li>`).join('')}</ul>`, 3200);
  } finally { cleanup(); api.bgm(false); }
}
// ================= 부탁 반응 (짧게 · 화면 아래에 잠깐) =================
const REACT = {
  main_hall: '계단이 아직도 삐걱거리네. 나 이 소리 들으면서 100 년 버텼어. 친구 같은 소리야.',
  clock_tower: '시계가.... 멈춰 있네. 내가 사라진 날도 이 시간이었는데. ....아, 다음 가자! 다음!',
  library_stacks: '도서관 냄새는 그대로다. 나 여기서 맨날 졸았어. 사서 선생님이 코 고는 소리 크다고 했지.',
  ghost_lake_pier: '여기서 개구리 잡다가 선생님께 혼났어. 그때 개구리 이름이 아서였는데. 아서 3 세쯤 됐으려나.',
  cemetery: '....여기는 좀 무섭다. 유령이 무서워하는 거 웃기지? 근데 무서운 건 무서운 거야.',
  cook: ['우와, 냄새! 나 냄새만 맡을 수 있거든. ....이거 내 몫이야? 고마워. 진짜로.', '이번 건 달콤한 냄새. 100 년 전 매점 빵 냄새랑 비슷해.', '냄새만으로 배부르다. 유령인데.'],
  class: ['나 문양학 꼴찌였어. 근데 옆에서 보니까 쉽네. 100 년 동안 복습했나 봐.', '아니면 옆자리가 좋아서인가. ....방금 그 말은 못 들은 걸로 해.'],
  brew: ['와, 한 번에! 우리 때는 세 번에 한 번은 쾅이었어.', '색이 예쁘다. 우리 때 물약은 다 갈색이었는데.', '세 병째! 너 진짜 마녀 같다.'],
  fail: '쾅! 경을 칠 노릇이네! ....아, 이거 옛날 말이야. 「큰일 났다」라는 뜻.',
  failq: '경을 칠!',
  hi: ['안녕! ....안 보이는 거 알아. 그래도 네 친구니까 내 친구 같아서.', '얘도 착하게 생겼다. 나 손 흔들었어. 못 봤겠지만.', '친구 많네. 부럽다. ....아니, 이제 나도 있으니까 안 부러워.'],
  room: '남의 방은 처음이야. 100 년 전엔 기숙사가 다 한 방이었거든. 코 고는 소리가 대단했어. ....그립다, 그 시끄러운 거.',
  emo: '(2 초 늦게 따라 해요) 나 이제 이모티콘 장인이야. 졸업 시험에 이모티콘 과목 있으면 1 등이야.',
  dig: '이, 이거.... 내 거야. 무늬가 같아. 100 년 동안 여기 있었구나. 나처럼.',
  idle: ['밤이 유령의 낮이야.', '{nm}, 오늘 무슨 생각 해?', '나 비 좋아해. 맞아도 안 젖거든.', '혼자 쓰는 방! 부르주아다.', '저기 블랑 아저씨 닮은 사람 지나갔어. 맨날 빵 훔쳐 먹던.... 아, 모르겠구나.'],
};
async function react(api, key, i){ A = api; let t = REACT[key]; if (Array.isArray(t)) t = t[Math.min(i || 0, t.length - 1)]; if (!t) return;
  if (key === 'fail' && TT().quip === 0){ await say('마틸다', REACT.failq, 500); A.W.say('me', '노릇이네!'); return; }
  await say('마틸다', t, 1100); }
// ================= 일기장 조각 (3 일째) =================
const PAGES = [
  ['졸업식 날 입을 교복을 다렸다. 단추가 하나 없지만 괜찮다.', '아, 이 단추. 아직도 하나 없어. 보여? 여기.'],
  ['오늘 아서를 연못에 놓아주었다. 졸업하면 못 보니까. 잘 살아, 아서.', '....아서한테 작별 인사도 했었구나. 나 기억력 좋다.'],
  ['열이 난다. 선생님은 졸업식까지는 낫는다고 했다. 엄마가 보내 준 털실 장갑을 꼈다.', '....엄마 장갑. 그건 어디 갔을까.'],
  ['밤에 창밖이 너무 조용하다. 다들 짐 싸는 소리만 난다. 나도 싸야지. 내일.', '그날 밤 진짜 조용했어. 지금처럼.'],
  ['내일이 졸업식이다. 꼭 가야지. 꼭. 졸업하면 바다에 가서, 엄마한테 편지를 쓸 거다.', '.......'],
];
async function page(api, i, n){ A = api; api.bgm(true);
  try { SND.page(); await card(`일기장 조각 · ${n} / 5<div class="pg">「${PAGES[i][0]}」</div>`, 3600); await say('마틸다', PAGES[i][1], 1300); }
  finally { cleanup(); api.bgm(false); } }
// ================= 밤 이야기 (부탁을 다 하면 · 그날 장소에서) =================
async function night(api, day){
  A = api; api.bgm(true); const u = UI(), T = TT(), r = {}; u.dim.style.opacity = 1; musicbox(true);
  try {
    if (day === 1){
      await say('마틸다', '오늘 고마웠어. 나 사실 100 년 동안 말 건 사람이 없었어. 다들 내가 안 보이니까.');
      await say('마틸다', '그래서 오늘 말을 너무 많이 했나 봐. 목이 쉰 것 같아. 유령인데.');
      await say('마틸다', '저기, 혹시.... 나 이름 말고 다르게 불러 줄래? 친구끼리는 다르게 부르잖아.');
      r.nm = await choose(['「마틸다. 예쁜 이름인데 그대로 부를래.」', '「틸다 어때?」', '「틸. 짧고 좋잖아.」']);
      await say('마틸다', ['그대로? ....좋아. 엄마가 지어 준 이름이거든. 100 년 만에 제대로 불렸네.', '틸다! 엄마만 그렇게 불렀어. ....좋아, 아주 좋아.', '틸? 푸하하, 무슨 강아지 이름 같아. ....근데 맘에 들어. 아무도 안 쓴 이름이라서. 너만 쓰는 이름.'][r.nm], 1600);
      await say('마틸다', '그리고 하나 더. 친구 인사 정하자. 100 년 전엔 다들 그런 거 하나씩 있었어.');
      r.hi = await choose(['하이파이브', '새끼손가락 걸기', '이마 콩']); SND.hi(r.hi);
      await say('마틸다', ['앗. ....괜찮아, 소리는 났어. 쉭. 이게 우리 인사야.', '손가락은 못 잡지만.... 이렇게 가까이 대면 걸린 거야. 약속도 이걸로 하자.', '이마 콩! 아, 통과했다. 머릿속까지 들어갔어. 이제 내 생각 다 들켰어.'][r.hi], 1500);
      await say('마틸다', '내일 아침부터 이걸로 인사할 거야. 까먹으면 안 돼.');
    } else if (day === 2){
      await say('마틸다', '오늘은 진짜 학생 같았어. 100 년 동안 학교에 있었는데, 오늘 처음 학교에 다닌 것 같아.');
      await say('마틸다', '그때는 빨리 졸업하고 싶었어. 졸업하면 바다에 가려고 했거든. 활동사진에서만 봤어. 파도가 하얗게 부서지는 거.', 1700);
      r.sea = await choose(['「언젠가 내가 바다 보여 줄게.」', '「바다 사진 찍어서 보여 줄게.」', '「바다는 생각보다 짜고 축축해.」']);
      await say('마틸다', ['진짜? ....새끼손가락. 아니, {hi}로 약속하자.', '사진! 그럼 나 사진 속 바다에 들어가 볼래. 유령은 그런 것도 될지 몰라.', '푸하하. 그럼 나는 안 젖으니까 이득이네. 짠맛도 모르고. ....조금 부럽다, 짠맛.'][r.sea], 1500);
      await say('마틸다', '아, 그리고 아까 그 말. 「경을 칠 노릇이네」. 100 년 전엔 다들 썼는데.');
      r.quip = await choose(['「경을 칠 노릇이네, 나도 써야지.」', '「그건 좀 할머니 같아.」']);
      await say('마틸다', ['진짜? 100 년 만에 이 말 쓰는 사람이 둘이 됐어.', '할머니 맞아. 나이로는. 히히.'][r.quip]);
    } else if (day === 3){
      await say('마틸다', '....그날 나는 결국 못 갔어. 눈을 떴더니 학교에 아무도 없었어.');
      await say('마틸다', '다들 졸업하고 떠났더라. 나만 빼고. 엄마한테 편지도 못 썼어.');
      await say('마틸다', '그래서 기다렸어. 누가 「졸업 축하해」라고 말해 줄 때까지. 그 말을 들어야 갈 수 있을 것 같아서.', 1700);
      await say('마틸다', '....앗, 분위기가 너무 무거워졌다. 미안. 유령이라 무거운 건 잘 못 들어. 히히.');
      r.btn = await choose(['「없어진 단추, 같이 찾아보자.」', '「내 단추 하나 줄게.」', '「단추 하나 없어도 예뻐.」']);
      if (r.btn === 1) await say('나', '(내 옷 단추를 하나 떼어 건네요. 마틸다 손을 통과해서 바닥에 떨어져요)', 900);
      await say('마틸다', ['100 년 전 단추를? ....찾으면 졸업식 때 달고 갈래. 내일 호숫가에 같이 가 줘.', '....못 잡네. 그래도 받은 거야. 내 마음 주머니에 넣었어.', '....그 말, 100 년 전에 듣고 싶었어. 지금 들어서 더 좋아.'][r.btn], 1600);
    } else if (day === 4){
      await say('마틸다', '오늘 정말 좋았어. 친구가 많아진 기분이야.');
      await say('마틸다', '근데, 친구가 생기니까.... 무서운 게 하나 생겼어.');
      await say('마틸다', '헤어지는 거. 100 년 동안 혼자일 땐 하나도 안 무서웠는데.');
      await say('마틸다', '내일이 마지막 날이래. 해골 선생님이 졸업식을 열어 준대. 그러면 나는.......', 1600);
      r.fear = await choose(['「나도 무서워.」', '「안 무서워. 우린 또 만날 거야.」', '「에이, 졸업하면 좋은 거지!」']);
      await say('마틸다', ['....둘 다 무서우면, 반씩 나눠 들자. 그럼 반만 무섭잖아.', '또? ....그 말, 믿을래. 유령은 믿는 거 잘해. 100 년 동안 기다린 것도 믿어서였으니까.', '맞아, 좋은 거야. ....좋은 건데 왜 이렇게 코끝이 찡하지. 유령도 코가 있나.'][r.fear], 1700);
      await say('마틸다', '저기, 오늘 밤은 조금만 더 같이 있어도 돼? 별 하나만 더 보고.');
      SND.sparkle(); await say('마틸다', '앗, 별똥별! 소원 빌었어? ....나는 빌었어. 비밀이야.', 1500);
    }
  } finally { musicbox(false); cleanup(); api.bgm(false); }
  return r;
}
// ================= 졸업식 (5 일째 · 광장 · 혼자 보는 연출) =================
const MEM_LINE = ['시계탑에서 {rago} 처음 불러 줬던 날.', '냄새만 맡았는데 제일 맛있었던 저녁.', '무거운 얘기 해도 안 도망갔던 밤.', '별똥별. 그때 빈 소원, 지금 말해 줄까? ....「이 친구랑 하루만 더」였어. 근데 벌써 들어줬어. 닷새나 줬어.'];
async function grad(api){
  A = api; api.bgm(true); const u = UI(), T = TT(), t0 = W().meTile(), m = t0.m, SP = [t0.x + 1, t0.y - 1];
  const fx = el('tlfx', '', 'canvas'); let raf = 0, fT0 = 0, capY = null, result = {};
  try {
    api.gh.show(m, SP[0], SP[1], 0, .95);
    // 해골 선생님이 옆에
    const skc = document.createElement('canvas'); skc.width = skc.height = 48; const sq = skc.getContext('2d'); sq.imageSmoothingQuality = 'high'; sq.drawImage(SK(), 0, 0, 64, 64, 8, 8, 32, 32);
    W().setProps(m, [{ id: 'tlskel', x: t0.x + 2, y: t0.y, img: skc, pxc: sq, sw: 48, sh: 48, ax: 24, ay: 40, solid: false, light: { r: 20, c: [255, 230, 190], a: .45 } }], 'tlskel');
    u.dim.style.opacity = 1; musicbox(true); u.ttl.innerHTML = '졸업식<small>1926 년 입학생 · 마틸다</small>'; u.ttl.classList.add('on'); await sleep(2600); u.ttl.classList.remove('on'); await sleep(600);
    await say('해골 선생님', '지금부터 1926 년 입학생, 마틸다의 졸업식을 시작하겠네.');
    await say('해골 선생님', '마틸다. 100 년 동안 결석 없이 학교를 지켰으니.... 개근상도 같이 주지.');
    if (T.quip === 0){ await say('마틸다', '개, 개근상이요? ....푸하하. 경을 칠 노릇이네!', 900); W().say('me', '노릇이네!'); await sleep(1300); }
    else await say('마틸다', '개, 개근상이요? ....푸하하. 100 년 동안 학교에 붙어 있긴 했죠.', 1200);
    await card(`<img src="art/tilda_diploma.png?v=1" style="width:240px;height:168px;filter:drop-shadow(0 0 10px rgba(232,216,160,.5))">졸업장<small>「위 학생은 호박달 마녀학교의 모든 과정을 마치고<br>100 년 개근하였기에 이 졸업장을 줍니다.」</small>`, 2600);
    await say('마틸다', '(손이 졸업장을 통과한다) ....앗.', 600); await say('해골 선생님', '쯧, 내가 들고 있지.', 900);
    // 추억 되돌아보기: 그날그날 찍어 둔 사진
    u.ttl.innerHTML = '추억 되돌아보기'; u.ttl.classList.add('on'); await sleep(1800); u.ttl.classList.remove('on'); musicbox(true, true);
    for (let i = 0; i < 4; i++){ const src = await api.mem(i + 1); if (!src) continue;
      u.card.innerHTML = `<img src="${src}" style="width:288px;height:192px;border-radius:4px;border:6px solid #F4ECDC;box-shadow:0 2px 0 #B8A88A;filter:sepia(.45) saturate(.85)"><small>추억 조각 ${i + 1} / 4</small>`; u.card.classList.add('on'); SND.card(); await sleep(900);
      await say('마틸다', MEM_LINE[i], 1500); u.card.classList.remove('on'); await sleep(500); }
    // 마지막 말
    await say('마틸다', '이제 진짜 가야 하나 봐. 「졸업 축하해」, 말해 줄래? 그 말 들으면 갈 수 있어.', 1300);
    let last = await choose([`「졸업 축하해, ${NAMES[T.nm ?? 0]}.」`, '「아직 말 안 할래. 하루만 더 있어.」', '「축하해. 그리고 고마워. 친구가 돼 줘서.」']);
    if (last === 1){ await say('마틸다', '....치사해. 그럼 나 계속 기다릴 거야. (조금 웃다가) 아니야. 그러면 네가 계속 마음 쓰잖아. 말해 줘. 괜찮아.', 1600); await choose(['「졸업 축하해.」']); }
    result.last = last;
    u.pop.textContent = '졸업 축하해!'; u.pop.classList.add('on'); SND.sparkle(); await sleep(1300); u.pop.classList.remove('on');
    await say('마틸다', last === 2 ? '그건 내 대사인데. ....친구가 돼 줘서 고마워. 100 년 동안 기다린 게 하나도 안 아까워.' : `....고마워. 이 말 들으려고 100 년 기다렸나 봐. 근데 듣고 나니까, 조금 더 기다릴 걸 그랬어. 너랑 조금 더.`, 1700);
    await say('마틸다', ['바다 약속, 잊지 마. 네가 바다에 가면, 하얀 파도 하나는 나야.', '바다 사진, 꼭 찍어. 나 그 사진 속에서 기다릴게.', '짠맛, 대신 맛봐 줘. 나는 안 젖는 쪽 할게.'][T.sea ?? 0], 1500);
    await say('마틸다', ['무서운 거 반씩 나눴잖아. 그러니까 지금 반만 슬픈 거야. 반만.', '또 만날 거라고 했지. 믿어. 약속이야.', '졸업은 좋은 거라고 했지. 맞아. 웃으면서 갈게. 너도 웃어 줘.'][T.fear ?? 0], 1600);
    await say('마틸다', '이제 아껴 둔 거 할게.', 900);
    SND.hi(T.hi ?? 0); u.pop.textContent = HI_SND[T.hi ?? 0] + '!'; u.pop.classList.add('on'); u.wh.style.transition = 'opacity .25s'; u.wh.style.opacity = .5; setTimeout(() => { u.wh.style.transition = 'opacity 1.2s'; u.wh.style.opacity = 0; }, 260); SND.sparkle(); await sleep(1500); u.pop.classList.remove('on');
    await say('마틸다', '....닿았다. 마지막에 닿았네.', 1500);
    // 빛이 되어 시계탑 쪽으로
    api.gh.hide(); musicbox(false); SND.ascend(); fT0 = performance.now(); fx.classList.add('on');
    const GHI = GH(), draw = now => { const t = (now - fT0) / 1000, w = innerWidth, h = innerHeight, L = 3; fx.width = Math.ceil(w / L); fx.height = Math.ceil(h / L); fx.style.width = w + 'px'; fx.style.height = h + 'px'; const g = fx.getContext('2d'); g.imageSmoothingEnabled = false; const Wd = fx.width, Hd = fx.height;
      for (let i = 0; i < 8; i++){ g.fillStyle = `rgb(${18 + i * 8},${14 + i * 6},${42 + i * 7})`; g.fillRect(0, i * Hd / 8, Wd, Hd / 8 + 1); }
      for (let i = 0; i < 40; i++){ g.fillStyle = `rgba(255,246,200,${.3 + .5 * Math.abs(Math.sin(t * 2 + i))})`; g.fillRect((i * 37) % Wd, (i * 23) % (Hd * .6), 1, 1); }
      const cx = Wd / 2, pw = 26 + Math.sin(t * 2) * 2; g.fillStyle = 'rgba(255,240,190,.16)'; g.fillRect(cx - pw, 0, pw * 2, Hd); g.fillStyle = 'rgba(255,248,220,.26)'; g.fillRect(cx - pw * .5, 0, pw, Hd); g.fillStyle = 'rgba(255,255,240,.34)'; g.fillRect(cx - pw * .18, 0, pw * .36, Hd);
      g.fillStyle = '#3A2E5A'; g.fillRect(cx - 12, 8, 24, 60); g.fillStyle = '#2A1E44'; g.fillRect(cx - 15, 4, 30, 6); g.fillStyle = '#E8D8A0'; g.beginPath(); g.arc(cx, 26, 8, 0, 7); g.fill(); const ang = t > 4.2 ? (t - 4.2) * 1.4 : 0; g.strokeStyle = '#3A2A1A'; g.beginPath(); g.moveTo(cx, 26); g.lineTo(cx + Math.sin(ang) * 6, 26 - Math.cos(ang) * 6); g.moveTo(cx, 26); g.lineTo(cx + 4, 26); g.stroke();
      for (let i = 0; i < 26; i++){ const y = Hd - ((t * 26 + i * 19) % (Hd + 20)), x = cx + Math.sin(t * 2 + i) * pw * .9; g.fillStyle = '#FFF6C8'; g.fillRect(x, y, 1, 1); if (i % 4 === 0){ g.fillRect(x - 1, y, 3, 1); g.fillRect(x, y - 1, 1, 3); } }
      const gy0 = Hd * .74 - Math.max(0, t - .8) * 18, ga0 = Math.max(0, Math.min(1, 1 - (t - 3.4) / 1.4)); g.globalAlpha = ga0; const rg = g.createRadialGradient(cx, gy0 - 14, 1, cx, gy0 - 14, 18); rg.addColorStop(0, 'rgba(200,230,255,.7)'); rg.addColorStop(1, 'rgba(200,230,255,0)'); g.fillStyle = rg; g.fillRect(cx - 20, gy0 - 34, 40, 40);
      const fr = t > 2 && t < 2.9 ? 5 : 0; g.drawImage(GHI, (fr + 1 + Math.floor(t * 4) % 4) * 64, 0, 64, 64, cx - 16, gy0 - 32, 32, 32); g.globalAlpha = 1;
      if (t > 2 && t < 2.9){ g.fillStyle = '#C8D8E8'; g.fillRect(cx + 9, gy0 - 22 - Math.round(Math.sin(t * 20) * 2), 2, 4); }
      if (capY !== null){ const cy = Math.min(Hd * .82, capY + (t - 5) * 14), sway = Math.sin(t * 3) * 6; g.fillStyle = '#2A2438'; g.fillRect(cx - 6 + sway, cy, 12, 2); g.fillRect(cx - 3 + sway, cy + 2, 6, 3); g.fillStyle = '#E0B03A'; g.fillRect(cx + 5 + sway, cy + 1, 1, 4); }
      raf = requestAnimationFrame(draw); };
    raf = requestAnimationFrame(draw); await sleep(4300); SND.bell(); await sleep(900); capY = -10; await sleep(3600);
    fx.classList.remove('on'); await sleep(900); cancelAnimationFrame(raf);
    W().setProps(m, [], 'tlskel');
    await card(`<canvas id="tlcap" width="64" height="64" style="width:160px;height:160px"></canvas>마틸다의 졸업 모자<small>하늘에서 천천히 내려와 내 앞에 놓였어요</small>`, 2600, c => { const g = c.querySelector('#tlcap').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(CAP(), 0, 0, 64, 64, 0, 0, 64, 64); });
    const rw = api.grant(result.last);
    await card(rw, 3800, c => { const b = c.querySelector('#tlbtn'); if (b){ const g = b.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BT(), 32 * (T.btn ?? 2), 0, 32, 32, 0, 0, 32, 32); } });
  } finally { cancelAnimationFrame(raf); musicbox(false); W().setProps(m, [], 'tlskel'); cleanup(); api.bgm(false); }
  return result;
}
// ================= 다음 날 편지 (배트리가 배달) =================
function letterText(T, nick){
  return [`${nick}에게.`, '', '졸업식 날 하루 늦게 편지를 써. 100 년 늦은 것보다는 낫지?', '',
    `${rago(NAMES[T.nm ?? 0])} 불러 줘서 고마워. 그 이름, 나 거기 가서도 쓸 거야.`,
    ['쉭. 하이파이브 소리 들려?', '새끼손가락 대고 쓰는 중이야.', '이마 콩. 생각 다 보낼게.'][T.hi ?? 0],
    ['바다 가면 첫 파도 보고 내 생각 해 줘.', '사진 기다릴게. 나 사진발 좋아.', '짠맛 어땠는지 나중에 알려 줘.'][T.sea ?? 0],
    T.btn === 0 ? (T.dug ? '단추 달고 졸업했어. 우리가 찾은 단추.' : '단추는 못 찾았지만, 같이 찾아 준 게 더 좋았어.') : T.btn === 1 ? '네 단추, 아직 마음 주머니에 있어.' : '단추 없어도 예쁘다는 말, 제일 좋은 졸업 선물이었어.',
    '', '계단이 삐걱거리면 내가 인사하는 거야. 모른 척하지 마.', '', '100 년 만에 사귄 친구. 마틸다가.', '', '추신. 엄마한테 쓸 편지, 이제 쓰러 갈게.'].join('\n');
}
async function letter(api){
  A = api; api.bgm(true); const u = UI(); u.dim.style.opacity = 1;
  try {
    await say('배트리', '학생님! 편지 왔어요. 보낸 사람이.... 어, 이상하다. 1926 년 학생이래요.');
    await say('배트리', '이번엔 제대로 배달했어요. 학생님 집, 끝에서 두 번째.');
    SND.page(); const v = el('tlletter', `<div class="pp">${letterText(TT(), api.me.nick).replace(/</g, '&lt;')}<button>닫기</button></div>`);
    await new Promise(r => { v.querySelector('button').onclick = r; }); v.remove();
  } finally { document.getElementById('tlletter')?.remove(); cleanup(); api.bgm(false); }
}
window.TildaFX = { intro, morning, react, page, night, grad, letter, say: (api, who, t, h) => { A = api; return say(who, t, h).finally(() => { if (!document.getElementById('tlcard')?.classList.contains('on')) document.getElementById('tlsay')?.remove(); }); }, letterText, NAMES, HI, PAGES, REACT, SND, setApi: a => { A = a; } };
})();
