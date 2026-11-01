// 시안: 「겨울 뜨개질」 — 첫 추위 밤 레오가 양털을 나눠 줘요 → 물레로 털실(채집물로 물들이기) → 도안 고르기 → 뜨개 미니게임(박자 맞춰 누르기) → 두르기 / 선물하기(NPC가 진짜로 하고 다님) → 반 전체 목표: 광장 큰 나무 뜨개 옷
//   window.__knGo() · window.__knLog · window.__knDone
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__knLog = [], T0 = performance.now();
const mark = k => { LOG.push([(performance.now() - T0) / 1000, k]); const d = document.getElementById('vmk'); if (d) d.style.background = LOG.length % 2 ? '#FF0000' : '#0000FF'; };
if (!document.getElementById('vmk')) document.body.insertAdjacentHTML('beforeend', '<div id="vmk" style="position:fixed;left:0;top:0;width:6px;height:6px;z-index:99999;background:#00FF00;pointer-events:none"></div>');
const css = document.createElement('style'); css.textContent = `
#kndim{position:fixed;inset:0;background:rgba(10,8,24,.45);opacity:0;transition:opacity .6s;z-index:300;pointer-events:none}
#knsay{position:fixed;left:10px;right:10px;bottom:150px;z-index:340;display:none}#knsay .bx{max-width:370px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.97);border:2px solid #C8B8E8;border-radius:14px;padding:10px 12px}
#knsay .fc{width:54px;height:54px;flex:none;border-radius:10px;background:#3A2E58;overflow:hidden}#knsay .fc img{width:100%;height:100%;image-rendering:pixelated}#knsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:#FFD8A8;margin-bottom:2px}#knsay p{margin:0;font-family:var(--f-px);font-size:14px;line-height:21px;color:#F1E9FF}
#knv{position:fixed;left:50%;top:44%;transform:translate(-50%,-50%) scale(.9);opacity:0;transition:all .4s cubic-bezier(.2,1.3,.4,1);z-index:330;width:min(94vw,370px);background:rgba(20,13,34,.97);border:2px solid #FFB8A8;border-radius:16px;padding:12px;font-family:var(--f-px);color:#F1E9FF;box-shadow:0 0 24px rgba(255,184,168,.3);text-align:center}
#knv.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#knv h3{margin:0 0 8px;font-family:var(--f-pxb);font-size:16px;color:#FFE0C8}#knv canvas.st{width:100%;image-rendering:pixelated;border-radius:8px;background:#2A1E3A;display:block}
#knv .row{display:flex;gap:6px;justify-content:center;margin-top:8px;flex-wrap:wrap}#knv .row span{padding:6px 9px;border-radius:10px;background:#2A2040;border:2px solid #3A2E58;font-size:12px;display:flex;align-items:center;gap:5px}#knv .row span.on{border-color:#FFE9A0;background:#3A2E50}#knv .row span.hit{transform:scale(.92)}#knv .row i{display:inline-block;width:12px;height:12px;border-radius:6px;border:1px solid #1a1024}
#knv .gr{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:4px}#knv .gr div{background:#2A2040;border:2px solid #3A2E58;border-radius:10px;padding:6px 2px;font-size:12px}#knv .gr div.on{border-color:#FFE9A0;background:#3A2E50}#knv .gr div.lk{opacity:.45}#knv .gr canvas{width:48px;height:48px;image-rendering:pixelated;display:block;margin:0 auto 2px}#knv .gr small{display:block;font-size:10px;color:#B8A8D8}
#knv .bar{position:relative;height:22px;border-radius:11px;background:#2A2040;margin-top:10px;overflow:hidden}#knv .bar .z{position:absolute;top:0;bottom:0;left:42%;width:16%;background:rgba(154,224,122,.45)}#knv .bar .z2{position:absolute;top:0;bottom:0;left:47%;width:6%;background:rgba(255,233,160,.7)}#knv .bar .m{position:absolute;top:2px;bottom:2px;width:6px;border-radius:3px;background:#fff;box-shadow:0 0 6px #fff}
#knv .jd{height:24px;margin-top:6px;font-family:var(--f-pxb);font-size:18px;color:#FFE9A0}#knv .btns{display:flex;gap:8px;justify-content:center;margin-top:10px}#knv .btns span{padding:9px 16px;border-radius:12px;background:#2A2040;border:2px solid #6A5A90;font-family:var(--f-pxb);font-size:14px}#knv .btns span.go{background:#FFB8A8;border-color:#FFB8A8;color:#3A1A14}#knv .btns span.hit{transform:scale(.93)}
#knv .pb{height:8px;border-radius:4px;background:#2A2040;margin-top:8px;overflow:hidden}#knv .pb i{display:block;height:100%;width:0;background:linear-gradient(90deg,#FF8A8A,#FFE9A0);transition:width .4s}#knv small.s{display:block;margin-top:6px;font-size:12px;color:#D8C8F0;line-height:18px}
#kntoast{position:fixed;left:50%;top:76px;transform:translate(-50%,-10px);z-index:345;background:rgba(20,13,34,.95);border:2px solid #FFB8A8;border-radius:12px;padding:8px 14px;font-family:var(--f-px);font-size:13px;color:#F1E9FF;opacity:0;transition:all .3s;white-space:nowrap}#kntoast.on{opacity:1;transform:translate(-50%,0)}`;
document.head.appendChild(css);
const el = (id, h = '') => { const d = document.createElement('div'); d.id = id; d.innerHTML = h; document.body.appendChild(d); return d; };
const dim = el('kndim'), say = el('knsay', '<div class="bx"><div class="fc"><img></div><div><b></b><p></p></div></div>'), v = el('knv'), tst = el('kntoast');
const A = World.Avatar, LEO = A.fromLook(5), NECK = A.meta.parts.neck.findIndex(p => p.id === 'neck_4'), HAT = A.meta.parts.hat.findIndex(p => p.id === 'hat_1');
const leoFace = () => A.head(LEO) || '';
async function line(t, hold = 1400, who = '레오'){ say.querySelector('img').src = leoFace(); say.querySelector('b').textContent = who; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; mark('line');
  for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(32); } await sleep(hold + t.length * 22); say.style.display = 'none'; await sleep(140); }
const toast = async (t, ms = 2400) => { tst.textContent = t; tst.classList.add('on'); mark('toast'); await sleep(ms); tst.classList.remove('on'); await sleep(300); };
const show = h => { v.innerHTML = h; v.classList.add('on'); }, hide = async () => { v.classList.remove('on'); await sleep(420); };
const YC = { 하양: '#F4F0E8', 빨강: '#E0505A', 파랑: '#5A8AE0', 노랑: '#F0C850', 초록: '#6AB85A' };
// 그림: 털실 뭉치 · 목도리 · 모자 · 장갑 · 양말 · 숄 · 인형
const R = (g, x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
function ball(g, cx, cy, r, col){ g.fillStyle = '#1a1024'; g.beginPath(); g.arc(cx, cy, r + 1, 0, 7); g.fill(); g.fillStyle = col; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill(); g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 1; for (let k = -r + 2; k < r; k += 3){ g.beginPath(); g.moveTo(cx - r * .8, cy + k * .6 - 2); g.quadraticCurveTo(cx, cy + k, cx + r * .8, cy + k * .6 + 2); g.stroke(); } R(g, cx - r * .4, cy - r * .5, 2, 2, 'rgba(255,255,255,.6)'); }
function icon(c, k, cols){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 24, 24); const [a, b] = cols;
  if (k === 'scarf'){ R(g, 3, 4, 18, 6, '#1a1024'); for (let i = 0; i < 4; i++) R(g, 4 + i * 4, 5, 4, 4, i % 2 ? b : a); R(g, 14, 9, 6, 12, '#1a1024'); for (let i = 0; i < 3; i++) R(g, 15, 10 + i * 3, 4, 3, i % 2 ? b : a); [15, 17].forEach(x => R(g, x, 21, 1, 2, a)); }
  if (k === 'hat'){ R(g, 5, 9, 14, 11, '#1a1024'); R(g, 6, 10, 12, 9, a); R(g, 5, 16, 14, 4, '#1a1024'); R(g, 6, 16, 12, 3, b); for (let x = 7; x < 18; x += 2) R(g, x, 17, 1, 1, 'rgba(0,0,0,.2)'); R(g, 10, 4, 5, 5, '#1a1024'); R(g, 11, 5, 3, 3, b); }
  if (k === 'mit'){ R(g, 6, 5, 11, 15, '#1a1024'); R(g, 7, 6, 9, 13, a); R(g, 3, 9, 5, 6, '#1a1024'); R(g, 4, 10, 3, 4, a); R(g, 6, 17, 11, 4, '#1a1024'); R(g, 7, 17, 9, 3, b); }
  if (k === 'sock'){ R(g, 8, 3, 8, 14, '#1a1024'); R(g, 9, 4, 6, 12, a); R(g, 8, 14, 12, 7, '#1a1024'); R(g, 9, 15, 10, 5, a); R(g, 9, 4, 6, 3, b); R(g, 16, 15, 3, 5, b); }
  if (k === 'shawl'){ g.fillStyle = '#1a1024'; g.beginPath(); g.moveTo(2, 5); g.lineTo(22, 5); g.lineTo(12, 21); g.fill(); g.fillStyle = a; g.beginPath(); g.moveTo(4, 6); g.lineTo(20, 6); g.lineTo(12, 19); g.fill(); R(g, 6, 8, 12, 1, b); R(g, 9, 12, 6, 1, b); }
  if (k === 'doll'){ R(g, 6, 4, 12, 10, '#1a1024'); R(g, 7, 5, 10, 8, a); R(g, 5, 3, 4, 4, '#1a1024'); R(g, 15, 3, 4, 4, '#1a1024'); R(g, 6, 4, 2, 2, a); R(g, 16, 4, 2, 2, a); R(g, 9, 8, 1, 1, '#1a1024'); R(g, 14, 8, 1, 1, '#1a1024'); R(g, 7, 13, 10, 8, '#1a1024'); R(g, 8, 14, 8, 6, b); } }
// 물레 장면
function wheel(c, t, col, k){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 160, 90); R(g, 0, 70, 160, 20, '#3A2A1E'); R(g, 0, 70, 160, 1, '#5A4030');
  const cx = 58, cy = 42, r = 26; g.strokeStyle = '#1a1024'; g.lineWidth = 4; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.stroke(); g.strokeStyle = '#B8804A'; g.lineWidth = 2; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.stroke();
  for (let i = 0; i < 8; i++){ const a = t * 6 + i * Math.PI / 4; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); g.stroke(); } R(g, cx - 3, cy - 3, 6, 6, '#7A5232'); R(g, cx - 2, cy + 2, 4, 30, '#7A5232'); R(g, cx - 14, 68, 28, 4, '#6A4428');
  // 양털 → 실
  ball(g, 22, 58, 9, '#F4F0E8'); g.strokeStyle = col; g.lineWidth = 1.5; g.beginPath(); g.moveTo(cx + 4, cy - 8); g.quadraticCurveTo(100, 20 + Math.sin(t * 8) * 3, 120, 50); g.stroke();
  ball(g, 124, 56, 4 + k * 10, col); }
// 뜨개: 바늘 두 개가 엇갈리고, 목도리가 아래로 자라요
function knit(c, rows, t, cols){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 160, 100); const W = 60, x0 = 50;
  for (let r = 0; r < rows; r++){ const y = 30 + r * 5, col = Math.floor(r / 3) % 2 ? cols[1] : cols[0]; R(g, x0 - 1, y - 1, W + 2, 6, '#1a1024'); for (let s = 0; s < W; s += 5){ R(g, x0 + s, y, 5, 5, col); R(g, x0 + s + 2, y, 1, 3, 'rgba(0,0,0,.18)'); R(g, x0 + s + 1, y + 3, 3, 1, 'rgba(255,255,255,.25)'); } }
  const sw = Math.sin(t * 10) * 4; g.save(); g.translate(80, 26); g.rotate(-.5 + sw * .02); R(g, -40, -2, 80, 4, '#1a1024'); R(g, -39, -1, 78, 2, '#D8C8A0'); R(g, 38, -3, 5, 6, '#B8804A'); g.restore();
  g.save(); g.translate(80, 26); g.rotate(.5 - sw * .02); R(g, -40, -2, 80, 4, '#1a1024'); R(g, -39, -1, 78, 2, '#D8C8A0'); R(g, -43, -3, 5, 6, '#B8804A'); g.restore();
  g.strokeStyle = cols[Math.floor(rows / 3) % 2]; g.lineWidth = 1.5; g.beginPath(); g.moveTo(112, 26); g.quadraticCurveTo(135, 50, 140, 85); g.stroke(); ball(g, 142, 88, 8, cols[Math.floor(rows / 3) % 2]); }
// 반 전체 목표: 광장 큰 나무 뜨개 옷
function tree(c, n, t){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 160, 100); R(g, 0, 86, 160, 14, '#E8F0F8'); R(g, 0, 86, 160, 1, '#C8D8E8');
  const br = (x0, y0, x1, y1, w) => { g.strokeStyle = '#1a1024'; g.lineWidth = w + 2; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.strokeStyle = '#7A5232'; g.lineWidth = w; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.fillStyle = '#FFFFFF'; g.fillRect(Math.round(x1) - 2, Math.round(y1) - 2, 4, 2); };
  br(80, 40, 50, 18, 5); br(80, 34, 112, 14, 5); br(62, 28, 52, 8, 3); br(98, 24, 108, 4, 3); br(80, 30, 82, 6, 4); br(56, 22, 36, 20, 3); br(104, 20, 126, 22, 3);
  R(g, 69, 34, 22, 54, '#1a1024'); R(g, 71, 34, 18, 54, '#7A5232'); R(g, 73, 34, 3, 54, '#9A6A42');
  const C = Object.values(YC); for (let i = 0; i < Math.min(n, 12); i++){ const y = 82 - i * 4; R(g, 69, y, 22, 4, '#1a1024'); R(g, 70, y, 20, 3, C[i % C.length]); for (let x = 71; x < 89; x += 3) R(g, x, y + 1, 1, 1, 'rgba(0,0,0,.2)'); }
  if (n >= 12){ [[50, 18], [112, 14], [82, 6]].forEach(([x, y], j) => { R(g, x - 4, y + 2, 8, 4, '#1a1024'); R(g, x - 3, y + 3, 6, 2, C[(j + 2) % C.length]); }); R(g, 78, 30, 4, 6, '#E0505A'); R(g, 76, 28, 8, 3, '#E0505A'); }
  for (let i = 0; i < 18; i++){ const x = (i * 29 + t * 20) % 160, y = (i * 17 + t * 30) % 86; R(g, Math.round(x), Math.round(y), 2, 2, '#FFFFFF'); } }
// 레오를 내 옆에 세우기 (아바타 정면)
let leoSc = false; function leoProp(on){ const t = World.meTile(); if (!on){ World.setProps(t.m, [], 'knleo'); return; } const S = A.compose(leoSc ? { ...LEO, neck: NECK } : LEO); if (!S) return; const HB = A.meta.head, fx = Math.floor(HB.x / A.FW) * A.FW, fy = Math.floor(HB.y / A.FH) * A.FH;
  const K = .68, W = Math.round(A.FW * K), H = Math.round(A.FH * K), c = document.createElement('canvas'); c.width = W; c.height = H; const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(S, fx, fy, A.FW, A.FH, 0, 0, W, H);
  World.setProps(t.m, [{ id: 'knleo', x: t.x + 1, y: t.y - 1, img: c, pxc: q, sw: W, sh: H, ax: W / 2, ay: H - 3, solid: false }], 'knleo'); }
let raf = 0; const loop = fn => { cancelAnimationFrame(raf); const f = now => { fn(now / 1000); raf = requestAnimationFrame(f); }; raf = requestAnimationFrame(f); };
window.__knGo = async () => {
  try { World.setWeather('snow'); } catch(e){}
  await sleep(600); await toast('오늘 밤은 유난히 추워요.......', 2200);
  leoProp(true); setInterval(() => leoProp(true), 1000); dim.style.opacity = 1; await sleep(500);
  await line('....추운데 왜 나와 있어.');
  await line('양들이 겨울 털을 잔뜩 줬어. 버리긴 아깝고.... 혼자 뜨기엔 너무 많아.', 1500);
  await line('뜨개질, 해 볼래. ....가르쳐 주는 거 아니다. 그냥 같이 하는 거야.', 1400);
  // 1) 물레: 양털 3 + 산딸기 → 빨간 털실
  show(`<h3>물레 · 털실 만들기</h3><canvas class="st" width="160" height="90"></canvas><div class="row">${Object.entries(YC).map(([n, c]) => `<span data-c="${n}"><i style="background:${c}"></i>${n}</span>`).join('')}</div><small class="s">양털 3 개 → 털실 1 뭉치 · 채집물로 물들여요 (산딸기 빨강 · 블루베리 파랑 · 노란 은행잎 노랑 · 촉촉 이끼 초록)</small><div class="pb"><i></i></div>`); mark('open');
  let col = YC.하양, k = 0; const cv = v.querySelector('canvas'); loop(t => wheel(cv, t, col, k)); await sleep(1400);
  const pickC = async n => { const s = v.querySelector(`[data-c="${n}"]`); v.querySelectorAll('[data-c]').forEach(x => x.classList.remove('on')); s.classList.add('on', 'hit'); await sleep(150); s.classList.remove('hit'); col = YC[n]; mark('pick'); };
  await pickC('빨강'); for (let i = 0; i <= 20; i++){ k = i / 20; v.querySelector('.pb i').style.width = (i * 5) + '%'; if (i % 5 === 0) mark('spin'); await sleep(90); } await toast('빨간 털실 1 뭉치를 만들었어요', 1600);
  await pickC('하양'); k = 0; for (let i = 0; i <= 20; i++){ k = i / 20; v.querySelector('.pb i').style.width = (i * 5) + '%'; if (i % 5 === 0) mark('spin'); await sleep(60); } await hide();
  // 2) 도안
  const D = [['scarf', '줄무늬 목도리', '털실 2', 0], ['hat', '방울 털모자', '털실 2', 0], ['mit', '손모아장갑', '털실 2', 0], ['sock', '털양말', '털실 2', 1], ['shawl', '포근 숄', '털실 4', 1], ['doll', '털실 양 인형', '털실 3', 1]];
  show(`<h3>뜨개 도안</h3><div class="gr">${D.map(([kk, n, need, lk]) => `<div data-d="${kk}" class="${lk ? 'lk' : ''}"><canvas width="24" height="24" data-ic="${kk}"></canvas>${n}<small>${lk ? '레오와 더 친해지면' : need}</small></div>`).join('')}</div><small class="s">빨강 · 하양 털실로 떠요</small>`); mark('open');
  v.querySelectorAll('[data-ic]').forEach(c => icon(c, c.dataset.ic, [YC.빨강, YC.하양])); await sleep(1600); const ds = v.querySelector('[data-d="scarf"]'); ds.classList.add('on'); mark('pick'); await sleep(900); await hide();
  // 3) 진짜 뜨개질: 코 잡기 → 한 코마다 찔러 넣기 · 실 감기 · 빼내기 · 넘기기 → 한 줄 끝나면 뒤집기 → 실 바꾸기 → 코 막음 → 술 달기
  const COLX = c => 48 + c * 13, NC = 8, cols2 = [YC.빨강, YC.하양];
  const K = { rows: [], j: NC, cast: 0, cur: cols2[0], tipDX: 0, tipDY: 0, wrap: null, newLoop: 0, drop: null, flip: 1, bind: -1, fringe: 0, step: '' };
  const dk = c => { const n = parseInt(c.slice(1), 16), f = .62; return `rgb(${(n >> 16 & 255) * f | 0},${(n >> 8 & 255) * f | 0},${(n & 255) * f | 0})`; };
  function vSt(g, x, y, col){ const D = dk(col);   // 겉뜨기 한 코 = 통통한 V (두 다리가 가운데서 만나요)
    for (let i = 0; i < 5; i++){ R(g, x - 6 + i, y + i, 4, 2, col); R(g, x + 3 - i, y + i, 4, 2, col); R(g, x - 6 + i, y + i + 1, 1, 1, D); R(g, x + 6 - i, y + i + 1, 1, 1, D); R(g, x - 3 + i, y + i, 1, 1, '#FFFFFF33'); } R(g, x, y + 5, 1, 1, D); }
  function rowBg(g, y, col){ R(g, COLX(0) - 7, y - 1, NC * 13 + 1, 7, dk(col)); }
  // 고리: 바늘이 고리 가운데를 꿰뚫어요 (뒤쪽 위 반 → 바늘 → 앞쪽 아래 반)
  function lpBack(g, x, y, col, a = 1){ g.globalAlpha = a; R(g, x - 3, y - 7, 7, 2, '#1a1024'); R(g, x - 2, y - 6, 5, 1, dk(col)); g.globalAlpha = 1; }
  function lp(g, x, y, col, a = 1){ g.globalAlpha = a; R(g, x - 4, y - 6, 2, 11, '#1a1024'); R(g, x + 3, y - 6, 2, 11, '#1a1024'); R(g, x - 3, y + 3, 7, 3, '#1a1024');
    R(g, x - 3, y - 5, 1, 9, col); R(g, x + 3, y - 5, 1, 9, col); R(g, x - 2, y + 3, 5, 2, col); R(g, x - 2, y + 4, 5, 1, dk(col)); R(g, x - 3, y - 5, 1, 2, '#FFFFFF66'); g.globalAlpha = 1; }
  function needle(g, x0, y0, x1, y1){ g.strokeStyle = '#1a1024'; g.lineWidth = 5; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.strokeStyle = '#D8C8A0'; g.lineWidth = 3; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); g.strokeStyle = '#F4ECD8'; g.lineWidth = 1; g.beginPath(); g.moveTo(x0, y0 - 1); g.lineTo(x1, y1 - 1); g.stroke(); R(g, x0 - 4, y0 - 4, 8, 8, '#1a1024'); R(g, x0 - 3, y0 - 3, 6, 6, '#B8804A'); }
  function kDraw(c, t){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 192, 128); R(g, 0, 0, 192, 128, '#2A1E3A');
    g.setTransform(K.flip, 0, 0, 1, K.flip < 0 ? 192 : 96 * (1 - K.flip), 0);
    // 떠 놓은 천 (아래로 자라요 · 위가 최근 줄)
    K.rows.forEach((col, k) => { const y = 38 + (K.rows.length - 1 - k) * 5; if (y > 112) return; rowBg(g, y, col); for (let cc = 0; cc < NC; cc++) vSt(g, COLX(cc), y, col); });
    for (let cc = K.j; cc < NC && K.bind < 0 && !K.casting; cc++) vSt(g, COLX(cc), 32, K.cur);   // 이번 줄에 뜬 코
    if (K.fringe) for (let cc = 0; cc < Math.min(NC, K.fringe); cc++){ const x = COLX(cc), y = 38 + K.rows.length * 5; [-2, 2].forEach(d => { R(g, x + d - 1, y, 3, 10, '#1a1024'); R(g, x + d, y, 1, 9, cols2[cc % 2]); }); }
    if (K.bind >= 0){ for (let cc = 0; cc < NC; cc++) if (cc < K.bind){ R(g, COLX(cc) - 6, 33, 13, 4, '#1a1024'); R(g, COLX(cc) - 5, 34, 11, 2, K.cur); } }
    // 왼쪽 바늘 (아직 안 뜬 코) · 오른쪽 바늘 (뜬 코)
    const tipL = K.j > 0 ? COLX(K.j - 1) + 8 : 30, tipR = (K.j < NC ? COLX(K.j) - 7 : COLX(NC - 1) + 14) + K.tipDX;
    if (K.bind < NC){ const n0 = Math.max(0, K.bind), n1 = K.cast ? K.cast : K.j; for (let cc = n0; cc < n1; cc++) if (!(K.drop && K.drop.c === cc)) lpBack(g, COLX(cc), 30, K.cur); needle(g, 4, 34, K.bind >= 0 || K.casting ? COLX(NC - 1) + 8 : tipL, 29); for (let cc = n0; cc < n1; cc++){ if (K.drop && K.drop.c === cc) continue; lp(g, COLX(cc), 30, K.cur); } }
    if (K.bind < 0 && !K.casting){ for (let cc = K.j; cc < NC && !K.casting; cc++) lpBack(g, COLX(cc), 25, K.cur); needle(g, 188, 22, tipR, 27 + K.tipDY); for (let cc = K.j; cc < NC && !K.casting; cc++) lp(g, COLX(cc), 25, K.cur); }
    if (K.newLoop) lp(g, tipR + 4, 26 + K.tipDY, K.cur, K.newLoop);
    if (K.drop){ const cc = K.drop.c, p = K.drop.p; lp(g, COLX(cc), 30 + p * 6, K.cur, 1 - p * .7); }
    // 실: 일하는 곳 → 털실 뭉치
    const wx = K.wrap != null ? tipR + 2 + Math.cos(K.wrap) * 5 : tipR + 6, wy = K.wrap != null ? 27 + K.tipDY + Math.sin(K.wrap) * 5 : 30;
    g.setTransform(1, 0, 0, 1, 0, 0); const sx = K.flip < 0 ? 192 - wx : wx;
    g.strokeStyle = K.cur; g.lineWidth = 2; g.beginPath(); g.moveTo(sx, wy); g.quadraticCurveTo(170, 70 + Math.sin(t * 2) * 3, 176, 106); g.stroke(); ball(g, 178, 112, 10, K.cur); }
  // 손가락 길잡이 (아래 칸): 점선 길 + 손가락 · 따라 그으면 한 동작
  const PATH = { stab: [[150, 24], [96, 14]], wrap: 'c', pull: [[96, 14], [150, 30]], slip: [[52, 20], [150, 20]], swipe: [[40, 26], [100, 10], [120, 30], [160, 16]], tap: [[100, 20]], fringe: [[100, 12], [100, 30]], flip: [[150, 20], [50, 20]] };
  const NAME = { stab: '↖ 찔러 넣기', wrap: '⟳ 실 감기', pull: '↘ 빼내기', slip: '→ 넘기기', swipe: '쓱 · 한 코', tap: '톡 · 코 잡기', fringe: '↓ 술 달기', flip: '← 뒤집기' };
  function pad(c, k, p){ const g = c.getContext('2d'); g.clearRect(0, 0, 192, 40); g.fillStyle = 'rgba(255,255,255,.06)'; g.fillRect(0, 0, 192, 40); const P = PATH[k]; let fx, fy; g.strokeStyle = 'rgba(255,233,160,.5)'; g.setLineDash([3, 3]); g.lineWidth = 2; g.beginPath();
    if (P === 'c'){ g.arc(96, 20, 12, 0, 7); fx = 96 + Math.cos(p * 6.28 - 1.57) * 12; fy = 20 + Math.sin(p * 6.28 - 1.57) * 12; } else { P.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); const n = P.length - 1, s = Math.min(n - 1e-6, p * n), i = Math.floor(s), f = s - i; [fx, fy] = n ? [P[i][0] + (P[i + 1][0] - P[i][0]) * f, P[i][1] + (P[i + 1][1] - P[i][1]) * f] : P[0]; }
    g.stroke(); g.setLineDash([]); g.fillStyle = 'rgba(255,255,255,.35)'; g.beginPath(); g.arc(fx, fy, 8, 0, 7); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(fx, fy, 4, 0, 7); g.fill(); }
  show(`<h3>줄무늬 목도리 뜨는 중</h3><canvas class="st" width="192" height="128"></canvas><div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;font-family:var(--f-pxb);font-size:14px"><span class="nm">코 잡기</span><span class="jd2" style="color:#FFE9A0"></span></div><canvas class="st pad" width="192" height="40" style="margin-top:4px;background:#1a1228"></canvas><div class="pb"><i></i></div><small class="s ks">바늘에 코 8 개를 잡아요</small>`); mark('open');
  const kc = v.querySelector('canvas'), pc = v.querySelector('.pad'), nm = v.querySelector('.nm'), jd2 = v.querySelector('.jd2'), ks = v.querySelector('.ks'), pbi = v.querySelector('.pb i'); loop(t => kDraw(kc, t));
  const score = []; let fast = false;
  async function gest(k, ms, onP){ nm.textContent = NAME[k]; const t1 = performance.now(); while (true){ const p = Math.min(1, (performance.now() - t1) / ms); pad(pc, k, p); onP && onP(p); if (p >= 1) break; await sleep(16); }
    const r = Math.random(), j = r < .72 ? ['완벽!', 2, 'perfect'] : r < .95 ? ['좋아요', 1, 'good'] : ['삐끗.......', 0, 'miss']; jd2.textContent = j[0]; score.push(j[1]); mark(j[2]); await sleep(fast ? 60 : 160); jd2.textContent = ''; }
  const TOTAL = 6; const prog = () => { pbi.style.width = Math.min(100, (K.rows.length + (NC - K.j) / NC) / TOTAL * 100) + '%'; };
  // 코 잡기: 톡 누를 때마다 바늘에 고리 하나
  K.casting = 1; K.cast = 0; K.j = 0; for (let i = 0; i < NC; i++){ await gest('tap', 260, null); K.cast = i + 1; } K.cast = 0; K.casting = 0; K.j = NC; ks.textContent = '한 코마다 진짜 뜨개질처럼 네 동작: 찔러 넣기 → 실 감기 → 빼내기 → 넘기기';
  async function stitch(){ const c = K.j - 1;
    if (!fast){
      await gest('stab', 700, p => { K.tipDX = -(COLX(K.j) - 7 - COLX(c)) * p; K.tipDY = 4 * p; });
      await gest('wrap', 800, p => { K.wrap = -1.57 + p * 6.28; }); K.wrap = null;
      await gest('pull', 650, p => { K.tipDX = -(COLX(K.j) - 7 - COLX(c)) * (1 - p); K.tipDY = 4 * (1 - p); K.newLoop = p; });
      await gest('slip', 600, p => { K.drop = { c, p }; }); }
    else await gest('swipe', 340, p => { K.tipDX = -(COLX(K.j) - 7 - COLX(c)) * Math.sin(p * 3.14); K.tipDY = 4 * Math.sin(p * 3.14); K.wrap = p > .3 && p < .7 ? -1.57 + (p - .3) / .4 * 6.28 : null; K.newLoop = p > .5 ? 1 : 0; K.drop = p > .7 ? { c, p: (p - .7) / .3 } : null; });
    K.drop = null; K.newLoop = 0; K.tipDX = 0; K.tipDY = 0; K.wrap = null; K.j--; mark('click'); prog(); }
  async function flipRow(){ await gest('flip', 420, p => { K.flip = Math.cos(p * Math.PI); }); K.flip = 1; K.rows.push(K.cur); K.j = NC; mark('flip'); prog(); }
  for (let i = 0; i < 3; i++) await stitch();
  ks.textContent = '손에 익었어요! 이제 쓱 한 번에 한 코'; mark('learn'); fast = true; await sleep(700);
  for (let r = 0; r < TOTAL; r++){ while (K.j > (r === 0 ? 0 : 0)) await stitch(); await flipRow(); if (r === 1 || r === 3){ K.cur = K.cur === cols2[0] ? cols2[1] : cols2[0]; ks.textContent = '실 바꾸기: 새 색 실을 묶어요'; mark('tie'); await sleep(500); } else ks.textContent = `${K.rows.length} 줄 · 다 뜨면 바늘을 뒤집어요`; if (r === 4) { /* 중간 */ } }
  // 코 막음: 고리를 하나씩 넘겨 씌워 바늘에서 빼요 → 술 달기
  ks.textContent = '코 막음: 앞 고리를 뒤 고리에 씌워서 빼요'; NAME.slip = '→ 코 막음'; K.bind = 0; K.j = NC; for (let i = 0; i < NC; i++){ await gest('slip', 220, null); K.bind = i + 1; mark('click'); }
  K.rows.push(K.cur); K.bind = 99; ks.textContent = '술 달기: 끝에 실 술을 매달아요'; for (let i = 0; i < NC; i++){ await gest('fringe', 220, null); K.fringe = i + 1; }
  await sleep(900); cancelAnimationFrame(raf); await hide();
  // 4) 완성
  const st = score.filter(s => s === 2).length >= 8 ? 3 : 2;
  show(`<h3>완성!</h3><canvas width="24" height="24" data-ic="scarf" style="width:120px;height:120px;image-rendering:pixelated"></canvas><div style="font-family:var(--f-pxb);font-size:16px;margin-top:4px">빨강 · 하양 줄무늬 목도리 <span style="color:#FFD866">${'★'.repeat(st)}</span></div><small class="s">완벽 ${score.filter(s => s === 2).length} · 좋아요 ${score.filter(s => s === 1).length} · 삐끗 ${score.filter(s => s === 0).length}</small><div class="btns"><span class="go" data-b="wear">두르기</span><span data-b="gift">선물하기</span></div>`); mark('done');
  icon(v.querySelector('[data-ic]'), 'scarf', [YC.빨강, YC.하양]); await sleep(2600); const bw = v.querySelector('[data-b="wear"]'); bw.classList.add('hit'); mark('pick'); await sleep(200); await hide();
  // 5) 두르기: 내 아바타에 목도리
  const M = window.__T && __T.me ? __T.me() : null; if (M){ M.av = { ...M.av, neck: NECK }; World.setPlayer(M.nick, { ...M.av }); }
  mark('wear'); World.say('me', '따뜻하다.......'); await sleep(2200);
  // 다시 하나 더 떠서 레오에게 (목도리를 한 레오)
  await line('....그거, 꽤 잘 떴네.', 1100);
  show(`<h3>레오에게 선물하기</h3><canvas width="64" height="64" id="knleo" style="width:150px;height:150px;image-rendering:pixelated;background:#3A2E58;border-radius:12px"></canvas><small class="s">파랑 · 하양 줄무늬 목도리를 레오에게 줬어요 · 호감도 +30</small>`); mark('gift');
  const drawLeo = withScarf => { const S = A.compose(withScarf ? { ...LEO, neck: NECK } : LEO), HB = A.meta.head || { x: 0, y: 0 }, FW = A.FW, FH = A.FH, fx = Math.floor((HB.x || 0) / FW) * FW, fy = Math.floor((HB.y || 0) / FH) * FH, q = v.querySelector('#knleo').getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, 64, 64); if (S) q.drawImage(S, fx, fy, FW, FH, 0, 0, 64, 64); };
  drawLeo(false); await sleep(900); drawLeo(true); leoSc = true; mark('sparkle'); await sleep(1400); await hide(); dim.style.opacity = 0;
  await line('....이거, 나 주는 거야.', 900); await line('따뜻하네. ....고맙다. 내일부터 하고 다닐게.', 1400);
  // 6) 반 전체 목표
  dim.style.opacity = 1; show(`<h3>반 전체 목표 · 광장 큰 나무 뜨개 옷</h3><canvas class="st" width="160" height="100"></canvas><div class="pb"><i style="width:77%"></i></div><small class="s">반 전체가 뜬 뜨개 23 / 30 개 · 다 모이면 광장 큰 나무가 알록달록 뜨개 옷을 입어요</small>`); mark('open');
  let n = 9; const tc = v.querySelector('canvas'); loop(t => tree(tc, n, t)); for (let i = 0; i < 3; i++){ await sleep(700); n++; mark('stack'); } await sleep(1600);
  n = 12; v.querySelector('h3').textContent = '광장 큰 나무가 뜨개 옷을 입었어요!'; v.querySelector('.pb i').style.width = '100%'; v.querySelector('small.s').textContent = '30 / 30 · 모두에게 「뜨개 바구니」 가구 · 이름표 「털실 이름표」'; mark('fin'); await sleep(3200);
  cancelAnimationFrame(raf); await hide(); dim.style.opacity = 0; await sleep(600); window.__knDone = true;
};
})();
