// 「겨울 뜨개질」 두 손 뜨개 화면 (index.html이 필요할 때 불러요) — 화면 왼쪽 = 왼손(바늘 잡기 · 밀기) · 오른쪽 = 오른손(바늘 끝이 손가락을 따라와요)
//   KnitFX.play(host, { a 첫째 색, b 둘째 색(줄무늬), rows 줄 수, fringe 술 달기(목도리), lesson 레오와 배우기(코 미리 잡고 한 줄), vol }) → { result: Promise({ score [삐끗, 좋아요, 완벽], rows }) · stop() }
(function(){
function play(host, O){
const YC = { A: O.a, B: O.b || O.a };
const NC = 8, ROWS = O.rows || 6, TIE = O.b && O.b !== O.a ? (O.tie || [2, 4]) : [], LEARN = O.lesson ? 99 : 3, W = 240, H = 230;
host.innerHTML = `<canvas id="kn_view" width="240" height="230"></canvas><div class="knbar"><span id="kn_step"></span><span id="kn_judge"></span></div><div id="kn_tip"></div><div class="knprog"><i id="kn_pg"></i></div><div class="knstats"><span>뜬 코 <b id="kn_sn">0</b></span><span>완벽 <b id="kn_s2">0</b></span><span>좋아요 <b id="kn_s1">0</b></span><span>삐끗 <b id="kn_s0">0</b></span><span id="kn_mouseHint" hidden>마우스: 왼손은 스페이스바 · 밀기는 ← 키</span></div>`;
const $ = id => host.querySelector('#kn_' + id), V = $('view'), g = V.getContext('2d');
let colA = 'A', colB = 'B', done = false, resolve; const result = new Promise(r => resolve = r);
// ---------- 소리 ----------
let AC = null; const ac = () => { try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); } catch(e){} return AC; };
function tone(f, d, type = 'triangle', v = .06, at = 0){ const C = ac(); if (!C || !(O.vol > 0)) return; v *= O.vol; const t = C.currentTime + at, o = C.createOscillator(), gn = C.createGain(); o.type = type; o.frequency.value = f; gn.gain.setValueAtTime(v, t); gn.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(gn); gn.connect(C.destination); o.start(t); o.stop(t + d); }
const buzz = ms => { try { navigator.vibrate && navigator.vibrate(ms); } catch(e){} };
const SND = { tick: () => { tone(2600, .03, 'square', .025); }, insert: () => { tone(900, .06, 'square', .03); tone(1400, .05, 'square', .02, .03); buzz(15); }, wrap: () => tone(700, .12, 'sine', .04), wrapped: () => [880, 1175].forEach((f, k) => tone(f, .2, 'triangle', .05, k * .05)),
  pull: () => tone(520, .1, 'triangle', .05), slip: () => { tone(3000, .03, 'square', .03); tone(2200, .03, 'square', .025, .02); buzz(25); }, perfect: () => tone(1568, .3), good: () => tone(1175, .25), miss: () => tone(200, .2, 'square', .05),
  warn: () => tone(240, .12, 'square', .04), flip: () => tone(523, .3, 'triangle', .05), tie: () => [659, 784].forEach((f, k) => tone(f, .3, 'triangle', .05, k * .06)), learn: () => [784, 988, 1175, 1568].forEach((f, k) => tone(f, .6, 'triangle', .05, k * .08)), done: () => [523, 659, 784, 1047, 1319].forEach((f, k) => tone(f, 1.2, 'triangle', .06, k * .1)) };
// ---------- 바늘 모양 (1 인칭: 아래 양쪽에서 두 손이 바늘을 쥐고 있어요) ----------
const LB = [14, 236], LT0 = [126, 104], RB = [226, 236], RT0 = [152, 100];
const sub2 = (a, b) => [a[0] - b[0], a[1] - b[1]], add2 = (a, b) => [a[0] + b[0], a[1] + b[1]], mul = (a, k) => [a[0] * k, a[1] * k], len = a => Math.hypot(a[0], a[1]), nrm = a => mul(a, 1 / (len(a) || 1));
const UL = nrm(sub2(LT0, LB)), UR = nrm(sub2(RT0, RB));   // 바늘 방향 (손 → 끝)
const dk = c => { const n = parseInt(c.slice(1), 16), f = .62; return `rgb(${(n >> 16 & 255) * f | 0},${(n >> 8 & 255) * f | 0},${(n & 255) * f | 0})`; };
const R = (c, x, y, w, h, col) => { c.fillStyle = col; c.fillRect(x, y, w, h); };
function needle(b, t){ const d = nrm(sub2(t, b)), side = [-d[1], d[0]];
  [[7, '#1a1024'], [5, '#C8B890'], [3, '#E8DCC0']].forEach(([w, c]) => { g.strokeStyle = c; g.lineWidth = w; g.lineCap = 'round'; g.beginPath(); g.moveTo(...b); g.lineTo(...sub2(t, mul(d, 6))); g.stroke(); });
  g.fillStyle = '#1a1024'; g.beginPath(); g.moveTo(...add2(sub2(t, mul(d, 7)), mul(side, 3.5))); g.lineTo(...add2(t, mul(d, 1))); g.lineTo(...sub2(sub2(t, mul(d, 7)), mul(side, 3.5))); g.fill();
  g.fillStyle = '#E8DCC0'; g.beginPath(); g.moveTo(...add2(sub2(t, mul(d, 6)), mul(side, 2))); g.lineTo(...t); g.lineTo(...sub2(sub2(t, mul(d, 6)), mul(side, 2))); g.fill();
  g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 1; g.beginPath(); g.moveTo(...add2(b, mul(side, -1))); g.lineTo(...add2(sub2(t, mul(d, 8)), mul(side, -1))); g.stroke(); }
// 고리: 바늘을 감싼 동그라미 (뒤쪽 반 → 바늘 → 앞쪽 반)
function loopArc(p, u, col, front, a = 1, s = 1){ const ang = Math.atan2(u[1], u[0]); g.save(); g.globalAlpha = a; g.translate(...p); g.rotate(ang);
  const st = front ? 0 : Math.PI, en = front ? Math.PI : 2 * Math.PI; [[4.5, '#1a1024'], [2.5, front ? col : dk(col)]].forEach(([w, c]) => { g.strokeStyle = c; g.lineWidth = w; g.beginPath(); g.ellipse(0, 0, 3.2 * s, 7 * s, 0, st, en); g.stroke(); }); g.restore(); }
function hand(x, y, flip, grip){ g.save(); g.translate(x, y); g.scale(flip ? -1 : 1, 1);
  g.fillStyle = '#1a1024'; g.beginPath(); g.ellipse(0, 0, 22, 16, -.6, 0, 7); g.fill(); g.fillStyle = grip ? '#F4C8A0' : '#E0B890'; g.beginPath(); g.ellipse(0, 0, 20, 14, -.6, 0, 7); g.fill();
  g.fillStyle = grip ? '#FFD8B8' : '#E8C4A0'; g.beginPath(); g.ellipse(8, -10, 8, 5, -.9, 0, 7); g.fill(); g.strokeStyle = 'rgba(120,70,50,.5)'; g.lineWidth = 1; [[-6, -2], [-1, 2], [4, 6]].forEach(([a, b]) => { g.beginPath(); g.moveTo(a, b - 6); g.lineTo(a + 6, b - 3); g.stroke(); });
  g.fillStyle = '#7A4AB8'; g.fillRect(-20, 6, 18, 12); g.fillStyle = '#5A3A90'; g.fillRect(-20, 6, 18, 3); g.restore(); }   // 소매
function vSt(x, y, col, q){ const D = dk(col), o = q === 0 ? 1 : 0;
  for (let i = 0; i < 5; i++){ R(g, x - 6 + i + o, y + i, 4, 2, col); R(g, x + 3 - i + o, y + i + o, 4, 2, col); R(g, x - 6 + i + o, y + i + 1, 1, 1, D); R(g, x + 6 - i + o, y + i + 1, 1, 1, D); R(g, x - 3 + i, y + i, 1, 1, 'rgba(255,255,255,.2)'); } R(g, x, y + 5, 1, 1, D); }
function ball(cx, cy, r, col){ g.fillStyle = '#1a1024'; g.beginPath(); g.arc(cx, cy, r + 1, 0, 7); g.fill(); g.fillStyle = col; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill(); g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 1; for (let k = -r + 2; k < r; k += 3){ g.beginPath(); g.moveTo(cx - r * .8, cy + k * .6 - 2); g.quadraticCurveTo(cx, cy + k, cx + r * .8, cy + k * .6 + 2); g.stroke(); } }
// ---------- 상태 ----------
// st: insert(찔러 넣기) → wrap(실 감기) → pull(빼내기) → slip(헌 고리 빼기)
let K, score, phase, st, busy, rowQ, stitchT, wobble, msg, msgT, learnDone;
const hands = { L: null, R: null };   // 누르고 있는 손가락 { id, x0, y0, x, y }
let keyGrip = false, mouseMode = false;
const gripL = () => !!hands.L || keyGrip;
function reset(){ K = { rows: [], j: 0, cast: 0, cur: YC[colA], flip: 1, bind: -1, fringe: 0, rt: RT0.slice(), lpull: 0, wrapA: 0, newLoop: 0, drop: null, inserted: false, castA: 0 };
  score = [0, 0, 0]; phase = O.lesson ? 'knit' : 'cast'; if (O.lesson){ K.j = NC; } st = 'insert'; busy = false; rowQ = []; wobble = 0; msg = ''; learnDone = false;
  const R0 = O.resume; if (R0){ K.rows = R0.rows.map(r => ({ col: r.col, q: r.q.slice() })); K.j = R0.j; K.cast = R0.cast; K.cur = R0.cur; K.bind = R0.bind; K.fringe = R0.fringe; phase = R0.phase; rowQ = R0.rowQ.slice(); score = R0.score.slice(); learnDone = !!R0.learnDone; msg = '멈춘 데서 이어 떠요'; msgT = performance.now() + 2000; }
  ui(); }
// 이어 뜨기용: 지금까지 뜬 것 (뜨던 코는 처음부터)
const snap = () => ({ rows: K.rows.map(r => ({ col: r.col, q: r.q.slice() })), j: K.j, cast: K.cast, cur: K.cur, bind: K.bind, fringe: K.fringe, phase: phase === 'done' ? 'fringe' : phase, rowQ: rowQ.slice(), score: score.slice(), learnDone });
const saveNow = () => { if (O.onSave && !done) try { O.onSave(snap()); } catch(e){} };
const leftTip = () => sub2(LT0, mul(UL, K.lpull));   // 왼손으로 밀면 끝이 손 쪽으로 물러나요
const leftLoopPos = i => sub2(leftTip(), mul(UL, 9 + i * 10));
const rightLoopPos = (rt, i) => sub2(rt, mul(UR, 9 + i * 10));
function draw(t){ g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H); R(g, 0, 0, W, H, '#2A1E3A');
  // 벽난로 빛
  const gr = g.createRadialGradient(40, 20, 4, 40, 20, 140); gr.addColorStop(0, 'rgba(255,170,90,.18)'); gr.addColorStop(1, 'rgba(255,170,90,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  g.setTransform(K.flip, 0, 0, 1, (W / 2) * (1 - K.flip), 0);
  const wob = wobble ? [Math.sin(t * 40) * wobble * 2, Math.cos(t * 33) * wobble] : [0, 0];
  // 천 (가운데 아래로 늘어져요)
  const fx = c => 120 - (NC - 1) * 6.5 + c * 13;
  K.rows.forEach((r, k) => { const y = 132 + (K.rows.length - 1 - k) * 5; if (y > 214) return; R(g, fx(0) - 7, y - 1, NC * 13 + 1, 7, dk(r.col)); for (let c = 0; c < NC; c++) vSt(fx(c), y, r.col, r.q[c]); });
  if (phase !== 'cast' && K.bind < 0) for (let c = K.j; c < NC; c++) vSt(fx(c), 126, K.cur, rowQ[c]);
  if (K.fringe) for (let c = 0; c < K.fringe; c++){ const x = fx(c), y = Math.min(132 + K.rows.length * 5, 214); [-2, 2].forEach(d => { R(g, x + d - 1, y, 3, 10, '#1a1024'); R(g, x + d, y, 1, 9, c % 2 ? YC[colB] : YC[colA]); }); }
  // 왼쪽 바늘 + 고리
  const lt = add2(leftTip(), wob), lb = add2(LB, wob), nL = phase === 'cast' ? K.cast : K.bind >= 0 ? Math.max(0, NC - K.bind) : K.j;
  if (K.bind < 99){ for (let i = 0; i < nL; i++) if (!(K.drop && i === 0)) loopArc(add2(leftLoopPos(i), wob), UL, K.cur, false);
    // 오른쪽 바늘이 첫 고리에 들어가 있으면 고리 뒤로 지나가요
    if (K.inserted && phase === 'knit') drawRight(t);
    needle(lb, lt); for (let i = 0; i < nL; i++) if (!(K.drop && i === 0)) loopArc(add2(leftLoopPos(i), wob), UL, K.cur, true); }
  if (K.drop){ const p = K.drop; loopArc(add2(leftLoopPos(0), [0, p * 10]), UL, K.cur, true, 1 - p, 1 - p * .3); }
  if (!(K.inserted && phase === 'knit') && phase !== 'cast' && K.bind < 99) drawRight(t);
  // 실: 일하는 곳 → 털실 뭉치 (오른손 아래)
  const wk = phase === 'cast' ? leftLoopPos(Math.max(0, K.cast)) : K.wrapA && K.inserted ? add2(K.rt, [Math.cos(K.wrapA) * 6, Math.sin(K.wrapA) * 6]) : add2(K.rt, mul(UR, -10));
  g.setTransform(1, 0, 0, 1, 0, 0); const wx = W / 2 + (wk[0] - W / 2) * K.flip;
  g.strokeStyle = K.cur; g.lineWidth = 2; g.beginPath(); g.moveTo(wx, wk[1]); g.quadraticCurveTo(220, 150 + Math.sin(t * 2) * 3, 214, 196); g.stroke(); ball(214, 200, 11, K.cur);
  // 손
  g.setTransform(K.flip, 0, 0, 1, (W / 2) * (1 - K.flip), 0);
  hand(lb[0] + 26, lb[1] - 30, false, gripL()); const rb = add2(RB, sub2(K.rt, RT0)); if (phase !== 'cast') hand(rb[0] - 26, rb[1] - 30, true, !!hands.R); else hand(206, 196, true, !!hands.R);
  g.setTransform(1, 0, 0, 1, 0, 0);
  // 손가락 표시
  [['L', '#9AE07A'], ['R', '#FFE9A0']].forEach(([k, c]) => { const h = hands[k]; if (!h) return; g.strokeStyle = c; g.globalAlpha = .7; g.lineWidth = 2; g.beginPath(); g.arc(h.cx, h.cy, 10, 0, 7); g.stroke(); g.globalAlpha = 1; });
  // 다음에 할 일 표시 (반짝)
  const blink = (Math.sin(t * 6) + 1) / 2;
  if (phase === 'knit' && st === 'insert' && K.j > 0){ const p = leftLoopPos(0), x = W / 2 + (p[0] - W / 2) * K.flip; g.strokeStyle = `rgba(255,233,160,${.3 + blink * .6})`; g.lineWidth = 1; g.beginPath(); g.arc(x, p[1], 11, 0, 7); g.stroke(); } }
function drawRight(t){ const rt = K.rt, rb = add2(RB, sub2(rt, RT0)), n = NC - K.j;
  if (phase === 'bind'){ needle(rb, rt); return; }
  for (let i = 0; i < n; i++) loopArc(rightLoopPos(rt, i + (K.newLoop ? 1 : 0)), UR, K.cur, false); needle(rb, rt); for (let i = 0; i < n; i++) loopArc(rightLoopPos(rt, i + (K.newLoop ? 1 : 0)), UR, K.cur, true);
  if (K.newLoop) loopArc(rightLoopPos(rt, 0), UR, K.cur, true, K.newLoop, .8); }
// ---------- 손가락 ----------
const scale = () => V.getBoundingClientRect().width / W;
const cpos = e => { const r = V.getBoundingClientRect(); return [(e.clientX - r.left) / r.width * W, (e.clientY - r.top) / r.height * H]; };
V.addEventListener('pointerdown', e => { ac(); if (e.pointerType === 'mouse'){ mouseMode = true; $('mouseHint').hidden = false; } const [x, y] = cpos(e), side = mouseMode ? 'R' : (x < W / 2 ? 'L' : 'R');
  if (hands[side]) return; V.setPointerCapture(e.pointerId); hands[side] = { id: e.pointerId, x0: x, y0: y, x, y, cx: x, cy: y, lastA: null, turn: 0, rt0: K.rt.slice(), pts: [[x, y]] }; onDown(side); });
V.addEventListener('pointermove', e => { const side = hands.L && hands.L.id === e.pointerId ? 'L' : hands.R && hands.R.id === e.pointerId ? 'R' : null; if (!side) return; const h = hands[side], [x, y] = cpos(e), dx = x - h.x, dy = y - h.y;
  if (Math.hypot(dx, dy) > .6){ const a = Math.atan2(dy, dx); if (h.lastA != null){ let d = a - h.lastA; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; if (Math.abs(d) < 1.6) h.turn += d; } h.lastA = a; }
  h.x = x; h.y = y; h.cx = x; h.cy = y; h.pts.push([x, y]); onMove(side, h); });
const end = e => { ['L', 'R'].forEach(s => { if (hands[s] && hands[s].id === e.pointerId){ const h = hands[s]; hands[s] = null; onUp(s, h); } }); };
V.addEventListener('pointerup', end); V.addEventListener('pointercancel', end);
const kd = e => { if (e.code === 'Space'){ e.preventDefault(); if (!keyGrip){ keyGrip = true; onDown('L'); } } if (e.code === 'ArrowLeft' && gripL()){ e.preventDefault(); keySlip(); } }; addEventListener('keydown', kd);
const ku = e => { if (e.code === 'Space'){ keyGrip = false; onUp('L', null); } }; addEventListener('keyup', ku);
// ---------- 뜨개 규칙 ----------
const say = (m, ms = 1600) => { msg = m; msgT = performance.now() + ms; ui(); };
let jT = 0; function showJudge(r){ const J = $('judge'); J.textContent = r === 2 ? '완벽!' : r === 1 ? '좋아요' : '삐끗.......'; J.style.color = r === 2 ? 'var(--gold)' : r === 1 ? 'var(--ok)' : 'var(--bad)'; jT = performance.now(); }
let bothT = 0;
let rtTw = 0;
function onDown(side){ if (side === 'R'){ rtTw++; if (hands.R) hands.R.rt0 = K.rt.slice(); } if (busy) return;
  if (phase === 'flip' && gripL() && hands.R){ doFlip(); return; }
  if (phase === 'tie' && side === 'R'){ K.cur = curRowColor(); SND.tie(); phase = 'knit'; st = 'insert'; say('새 색 실을 묶었어요'); }
  if (phase === 'fringe' && side === 'R'){ /* 아래로 그으면 */ }
  if (phase === 'knit' && st === 'insert' && side === 'R') stitchT = stitchT || performance.now();
  ui(); }
function onMove(side, h){ if (busy) return;
  if (side === 'R' && phase === 'cast'){ if (!gripL()){ nag(); return; } if (Math.abs(h.turn) >= Math.PI * 1.75){ h.turn = 0; K.cast++; SND.tick(); if (K.cast >= NC){ phase = 'knit'; K.j = NC; st = 'insert'; say('코 8 개를 잡았어요. 이제 한 코씩 떠요', 2000); } ui(); } K.castA = h.turn; return; }
  if (side === 'R' && (phase === 'knit' || phase === 'bind')){
    if (K.inserted && st === 'wrap'){ K.wrapA = h.turn; if (Math.abs(h.turn) >= Math.PI * 1.7){ st = 'pull'; K.newLoop = .4; SND.wrapped(); h.x0 = h.x; h.y0 = h.y; ui(); } else if (Math.abs(h.turn) > .5 && Math.random() < .05) SND.wrap(); if (!gripL()) slipOut(); return; }
    if (K.inserted && st === 'pull'){ const d = [h.x - h.x0, h.y - h.y0]; const pin = leftLoopPos(0); K.rt = add2(add2(pin, [-1, 1]), [Math.max(0, d[0]) * .9, Math.max(0, d[1]) * .9]); K.newLoop = Math.min(1, .4 + Math.max(0, d[0] + d[1]) / 40);
      if (!gripL()){ slipOut(); return; } if (d[0] + d[1] > 22){ K.inserted = false; st = 'slip'; K.newLoop = 1; SND.pull(); ui(); } return; }
    if (!K.inserted){ K.rt = clampRt(add2(h.rt0, [h.x - h.x0, h.y - h.y0]));
      if (phase === 'knit' && st === 'insert' && K.j > 0){ const p = leftLoopPos(0), d = sub2(K.rt, p); if (len(d) < 11 && K.rt[0] < p[0] + 4){ if (!gripL()){ nag(); return; } K.inserted = true; st = 'wrap'; K.rt = add2(p, [-1, 1]); h.turn = 0; K.wrapA = 0; SND.insert(); ui(); } } } }
  if (side === 'L' && hands.L){ const d = [h.x - h.x0, h.y - h.y0], push = Math.max(0, -(d[0] * UL[0] + d[1] * UL[1]));   // 손 쪽(아래 왼쪽)으로 미는 만큼
    K.lpull = Math.min(14, push * .8);
    if (phase === 'knit' && st === 'slip' && push > 14) finishStitch();
    if (phase === 'bind' && push > 14 && hands.R && !busy){ bindOne(); h.x0 = h.x; h.y0 = h.y; } }
  if (side === 'R' && phase === 'fringe' && h.y - h.y0 > 20){ h.y0 = h.y; K.fringe++; SND.tick(); if (K.fringe >= NC){ phase = 'done'; setTimeout(finish, 600); } ui(); } }
function onUp(side, h){ if (side === 'L'){ K.lpull = 0; if (K.inserted) slipOut(); }
  if (side === 'R' && !K.inserted && st !== 'pull'){ /* 오른쪽 바늘은 손을 떼면 제자리로 */ const from = K.rt.slice(), id = ++rtTw; tween(180, p => { if (id === rtTw) K.rt = add2(from, mul(sub2(RT0, from), p)); }); }
  if (side === 'R' && phase === 'fringe' && h && h.pts.length < 4 ){ K.fringe++; SND.tick(); if (K.fringe >= NC){ phase = 'done'; setTimeout(finish, 600); } ui(); } }
const clampRt = p => [Math.max(70, Math.min(214, p[0])), Math.max(60, Math.min(170, p[1]))];
let nagT = 0; function nag(){ if (performance.now() - nagT < 900) return; nagT = performance.now(); wobble = 1; SND.warn(); say('왼손으로 바늘을 꽉 잡아요 (화면 왼쪽을 누른 채)'); setTimeout(() => { wobble = 0; }, 500); }
function slipOut(){ K.inserted = false; st = 'insert'; K.newLoop = 0; K.wrapA = 0; wobble = 1; setTimeout(() => { wobble = 0; }, 500); K.missed = true; SND.warn(); say('왼손을 놓쳐서 바늘이 빠졌어요. 다시 찔러 넣어요'); ui(); }
const tween = (ms, fn) => new Promise(res => { const t0 = performance.now(); const f = now => { const p = Math.min(1, (now - t0) / ms); fn(p); if (p < 1) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); });
async function finishStitch(){ if (busy) return; busy = true; SND.slip(); if (hands.R){ hands.R.rt0 = K.rt.slice(); hands.R.x0 = hands.R.x; hands.R.y0 = hands.R.y; } await tween(220, p => { K.drop = p; }); K.drop = null; K.newLoop = 0; K.wrapA = 0;
  const secs = (performance.now() - (stitchT || performance.now())) / 1000, q = K.missed ? 0 : secs < (learnDone ? 3.2 : 6) ? 2 : 1; stitchT = 0; K.missed = false;
  score[q]++; SND[q === 2 ? 'perfect' : q === 1 ? 'good' : 'miss'](); showJudge(q); rowQ[K.j - 1] = q; K.j--; st = 'insert';
  const doneSt = K.rows.length * NC + (NC - K.j); if (!learnDone && doneSt >= LEARN){ learnDone = true; SND.learn(); say('손에 익었어요! 이제 리듬 있게: 쏙 · 빙글 · 쭉 · 툭', 2400); }
  if (K.j === 0 && O.lesson){ K.rows.push({ col: K.cur, q: rowQ.slice() }); phase = 'done'; say('한 줄 완성!', 2000); setTimeout(finish, 900); }
  else if (K.j === 0){ phase = 'flip'; setTimeout(saveNow, 0); say('한 줄 끝! 두 손을 떼었다가 양손으로 동시에 다시 쥐면 바늘을 바꿔 쥐어요', 2600); }
  busy = false; ui(); }
async function doFlip(){ busy = true; SND.flip(); await tween(420, p => { K.flip = Math.cos(p * Math.PI); }); K.flip = 1; K.rows.push({ col: K.cur, q: rowQ.slice() }); rowQ = []; K.rt = RT0.slice();
  if (K.rows.length >= ROWS && O.lesson){ phase = 'done'; setTimeout(finish, 400); }
  else if (K.rows.length >= ROWS){ phase = 'bind'; K.bind = 0; K.j = NC; say('코 막음: 양손으로 쥐고 왼손을 아래로 밀 때마다 고리가 하나씩 빠져요', 2600); }
  else if (TIE.includes(K.rows.length)){ phase = 'tie'; K.j = NC; say('줄무늬 차례예요. 오른손으로 톡 눌러 새 색 실을 묶어요', 2400); } else { phase = 'knit'; K.j = NC; st = 'insert'; }
  ['L', 'R'].forEach(s => { if (hands[s]){ hands[s].x0 = hands[s].x; hands[s].y0 = hands[s].y; hands[s].rt0 = K.rt.slice(); } }); busy = false; ui(); saveNow(); }
async function bindOne(){ busy = true; SND.slip(); await tween(160, p => { K.drop = p; }); K.drop = null; K.bind++; if (K.bind >= NC){ K.bind = 99; if (O.fringe === false){ phase = 'done'; setTimeout(finish, 500); } else phase = 'fringe'; K.rows.push({ col: K.cur, q: Array(NC).fill(2) }); say('술 달기: 오른손으로 아래로 그을 때마다 실 술이 하나씩', 2400); } busy = false; ui(); }
function keySlip(){ if (phase === 'knit' && st === 'slip') finishStitch(); else if (phase === 'bind') bindOne(); }
const curRowColor = () => (TIE.filter(r => r <= K.rows.length).length % 2 ? YC[colB] : YC[colA]);
// ---------- 안내 ----------
const STEP0 = { insert: ['쏙 · 찔러 넣기', '왼손으로 잡은 채, 오른손을 움직여 오른쪽 바늘 끝을 반짝이는 첫 고리에 넣어요'], wrap: ['빙글 · 실 감기', '오른손을 동그랗게 한 바퀴 돌려서 실을 바늘에 감아요'], pull: ['쭉 · 빼내기', '오른손을 오른쪽 아래로 당겨서 감은 실을 고리 사이로 빼내요'], slip: ['툭 · 헌 고리 빼기', '왼손을 아래로 밀어서 왼쪽 바늘의 헌 고리를 빼요'] };
const STEP = O.lesson ? { insert: ['쏙 · 찔러 넣기', '레오: 끝을 고리에 넣어. 앞에서 뒤로. (왼손은 화면 왼쪽을 누른 채)'], wrap: ['빙글 · 실 감기', '레오: 실 한 바퀴 감고.'], pull: ['쭉 · 빼내기', '레오: 빼내고....'], slip: ['툭 · 헌 고리 빼기', '레오: 헌 고리는 왼손으로 밀어서 빼.'] } : STEP0;
function ui(){ if (done) return; let n = '', tp = '';
  if (phase === 'cast'){ n = '코 잡기'; tp = `왼손으로 바늘을 잡고, 오른손을 동그랗게 돌릴 때마다 고리가 하나씩 생겨요 (${K.cast} / ${NC})`; }
  else if (phase === 'knit'){ [n, tp] = STEP[st]; if (learnDone && !O.lesson) tp = ''; }
  else if (phase === 'flip'){ n = '바늘 바꿔 쥐기'; tp = '두 손을 다 떼었다가 양쪽을 동시에 다시 눌러요'; }
  else if (phase === 'tie'){ n = '실 바꾸기'; tp = '오른손으로 톡'; }
  else if (phase === 'bind'){ n = '코 막음'; tp = `양손으로 쥐고 왼손을 아래로 밀어요 (${Math.max(0, K.bind)} / ${NC})`; }
  else if (phase === 'fringe'){ n = '술 달기'; tp = `오른손으로 아래로 긋거나 톡 (${K.fringe} / ${NC})`; }
  else n = '완성!';
  $('step').textContent = n; $('tip').textContent = msg && performance.now() < msgT ? msg : tp;
  const total = NC + ROWS * NC + NC * 2, prog = (phase === 'cast' ? K.cast : NC) + K.rows.length * NC + (phase === 'knit' || phase === 'flip' ? NC - K.j : 0) + (phase === 'fringe' || phase === 'done' ? NC - NC : Math.max(0, Math.min(NC, K.bind))) + K.fringe;
  $('pg').style.width = Math.min(100, prog / total * 100) + '%'; $('sn').textContent = score[0] + score[1] + score[2]; ['s0', 's1', 's2'].forEach((id, i) => $(id).textContent = score[i]); }
// ---------- 끝 ----------
function finish(){ if (done) return; done = true; SND.done(); cancelAnimationFrame(raf); removeEventListener('keydown', kd); removeEventListener('keyup', ku); resolve({ score: score.slice(), rows: K.rows.map(r => ({ col: r.col, q: r.q.slice() })) }); }
let raf = 0; const loop = now => { if (done) return; draw(now / 1000); if (performance.now() - jT > 800 && $('judge').textContent) $('judge').textContent = ''; if (msg && performance.now() > msgT){ msg = ''; ui(); } raf = requestAnimationFrame(loop); };
reset(); raf = requestAnimationFrame(loop);
return { result, snap, stop: () => { if (done) return; done = true; cancelAnimationFrame(raf); removeEventListener('keydown', kd); removeEventListener('keyup', ku); resolve(null); } };
}
window.KnitFX = { play };
})();
