// 시안: 무슈 블랑 맛 표현 연출 — 요리 17종마다 대사·환상 배경·입자·외침이 달라요 (blanc_reactions.json)
//   목업 사이트 폴더에 blanc_lpc.png · seed_dishes.png · blanc_reactions.json이 있어야 해요
//   window.__bfGo([요리 번호...]) 차례로 맛보기 · window.__bfPeak(번호) 환상 장면만 멈춰서 보여 주기(장면 모음 찍기용)
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const SPOT = [14, 11], PLAYER = '민준';
const css = document.createElement('style'); css.textContent = `
#bfsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:320;display:none}
#bfsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid #9AC8F0;border-radius:14px;padding:12px}
#bfsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden}#bfsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}
#bfsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:#BFE0FF;margin-bottom:3px}#bfsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px}
#bfv{position:fixed;inset:0;z-index:330;pointer-events:none;opacity:0;transition:opacity .45s}#bfv.on{opacity:1}#bfv canvas{position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated}
#bfshout{position:fixed;left:14px;right:14px;top:11%;z-index:335;text-align:center;font-family:var(--f-pxb);font-size:19px;line-height:28px;color:#FFFFFF;pointer-events:none;
  text-shadow:-2px 0 #1A0A24,2px 0 #1A0A24,0 -2px #1A0A24,0 2px #1A0A24,0 0 14px rgba(255,240,200,.9);opacity:0;transform:scale(.9);transition:opacity .25s,transform .25s}#bfshout.on{opacity:1;transform:scale(1)}
#bftitle{position:fixed;left:0;right:0;top:80%;z-index:336;text-align:center;font-family:var(--f-pxb);font-size:34px;letter-spacing:2px;color:#FFE9A0;pointer-events:none;opacity:0;transform:scale(2.4);transition:opacity .35s,transform .45s cubic-bezier(.2,1.6,.4,1)}
#bftitle.on{opacity:1;transform:scale(1)}#bftitle small{display:block;font-size:13px;letter-spacing:0;color:#FFF;margin-bottom:6px}
#bftitle span{text-shadow:-3px 0 #2A0A1A,3px 0 #2A0A1A,0 -3px #2A0A1A,0 3px #2A0A1A,0 0 24px var(--g,#FF9A3A),0 0 48px var(--g,#FF9A3A)}
#bfcard{position:fixed;left:50%;top:38%;z-index:340;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 22px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #FFE8A0;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(255,232,160,.5);pointer-events:none;text-align:center;width:min(86vw,320px)}
#bfcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#bfcard .st{font-size:26px;letter-spacing:4px;color:#FFD866;text-shadow:0 0 10px #FFB020}#bfcard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}#bfcard canvas{image-rendering:pixelated}`;
document.head.appendChild(css);
const el = (id, html) => { const d = document.createElement('div'); d.id = id; if (html) d.innerHTML = html; document.body.appendChild(d); return d; };
const say = el('bfsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b>무슈 블랑</b><p></p></div></div>');
const vis = el('bfv', '<canvas></canvas>'), shout = el('bfshout'), title = el('bftitle'), card = el('bfcard');
const cv = vis.querySelector('canvas'), g = cv.getContext('2d');
const SH = new Image(); SH.src = 'blanc_lpc.png'; const DI = new Image(); DI.src = 'seed_dishes.png';
let R = null; const ready = fetch('blanc_reactions.json').then(r => r.json()).then(j => { R = j; });
const fill = t => t.replace(/\{player\}/g, PLAYER);
// ---- 무슈 블랑 (맵 위) ----
const frame = (i, a = 1) => { const c = document.createElement('canvas'); c.width = c.height = 32; const q = c.getContext('2d'); q.globalAlpha = a; q.imageSmoothingQuality = 'high'; q.drawImage(SH, i * 64, 0, 64, 64, 0, 0, 32, 32); return c; };
const place = (i, a) => { const img = frame(i, a); World.setProps('candy', [{ id: 'blanc', x: SPOT[0], y: SPOT[1], img, pxc: img.getContext('2d'), sw: 32, sh: 32, ax: 16, ay: 30, solid: true }], 'blanc'); };
let bob = null, bt = 0; const bobOn = (ms = 260) => { clearInterval(bob); bob = setInterval(() => place(1 + (bt++ % 4), 1), ms); };
const talk = async (t, hold = 1400) => { const q = say.querySelector('canvas').getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32); q.drawImage(SH, 16, 6, 32, 32, 0, 0, 32, 32);
  say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; const s = fill(t); for (let k = 1; k <= s.length; k++){ p.textContent = s.slice(0, k); await sleep(32); } await sleep(hold); say.style.display = 'none'; await sleep(140); };
const showCard = async (html, draw, ms) => { card.innerHTML = html; draw && draw(); card.classList.add('on'); await sleep(ms); card.classList.remove('on'); await sleep(420); };
// ---- 입자 그림 (점 하나 = P 픽셀) ----
const P = 4;
const px = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(Math.round(x + w * 0), Math.round(y), w * P, h * P); };
const at = (ox, oy) => (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(Math.round(ox + x * P), Math.round(oy + y * P), w * P, h * P); };
const SPR = {
  pumpkin: d => { d(1, 1, 6, 5, '#F07A18'); d(0, 2, 8, 3, '#F07A18'); d(1, 1, 2, 4, '#FF9A3A'); d(3, 0, 1, 1, '#5A7A22'); d(2, 2, 1, 1, '#FFE070'); d(5, 2, 1, 1, '#FFE070'); d(2, 4, 4, 1, '#FFE070'); },
  candy: d => { d(2, 0, 3, 2, '#FFF4E0'); d(1, 2, 5, 2, '#FF9A2A'); d(2, 4, 3, 2, '#FFD84A'); d(3, 6, 1, 1, '#FFD84A'); },
  rose: d => { d(1, 0, 4, 4, '#2A0A1A'); d(2, 1, 2, 2, '#8A1A3A'); d(0, 1, 1, 2, '#2A0A1A'); d(5, 1, 1, 2, '#2A0A1A'); d(3, 4, 1, 3, '#3A6A2A'); d(4, 5, 1, 1, '#3A6A2A'); },
  petal: d => { d(0, 1, 2, 2, '#C8143A'); d(1, 0, 2, 2, '#E83A5A'); },
  drop: d => { d(1, 0, 1, 1, '#E8143A'); d(0, 1, 3, 2, '#C8102A'); d(1, 3, 1, 1, '#A00A20'); d(0, 1, 1, 1, '#FF6A7A'); },
  eye: d => { d(1, 0, 4, 1, '#FFFFFF'); d(0, 1, 6, 3, '#FFFFFF'); d(1, 4, 4, 1, '#FFFFFF'); d(2, 1, 2, 3, '#3A9A3A'); d(2, 2, 1, 1, '#0A0A0A'); d(3, 1, 1, 1, '#FFFFFF'); },
  ghost: d => { d(1, 0, 4, 1, '#F0F4FF'); d(0, 1, 6, 5, '#F0F4FF'); d(0, 6, 1, 1, '#F0F4FF'); d(2, 6, 2, 1, '#F0F4FF'); d(5, 6, 1, 1, '#F0F4FF'); d(1, 2, 1, 2, '#1A1428'); d(4, 2, 1, 2, '#1A1428'); d(2, 4, 2, 1, '#FFA0C0'); },
  sparkle: d => { d(2, 0, 1, 5, '#FFF6C8'); d(0, 2, 5, 1, '#FFF6C8'); d(2, 2, 1, 1, '#FFFFFF'); },
  web: d => { d(0, 0, 7, 1, '#D0CCE0'); d(0, 0, 1, 7, '#D0CCE0'); for (let i = 0; i < 7; i++) d(i, i, 1, 1, '#D0CCE0'); d(3, 1, 1, 1, '#D0CCE0'); d(1, 3, 1, 1, '#D0CCE0'); d(5, 2, 1, 1, '#D0CCE0'); d(2, 5, 1, 1, '#D0CCE0'); },
  skull: d => { d(1, 0, 4, 1, '#F0EADC'); d(0, 1, 6, 3, '#F0EADC'); d(1, 4, 4, 2, '#E0D8C8'); d(1, 2, 1, 1, '#2A1A24'); d(4, 2, 1, 1, '#2A1A24'); d(2, 5, 1, 1, '#8A8272'); d(3, 5, 1, 1, '#8A8272'); },
  bat: d => { d(3, 1, 3, 3, '#5A3A7A'); d(0, 0, 3, 1, '#3A2A5A'); d(0, 1, 3, 2, '#3A2A5A'); d(6, 0, 3, 1, '#3A2A5A'); d(6, 1, 3, 2, '#3A2A5A'); d(3, 0, 1, 1, '#5A3A7A'); d(5, 0, 1, 1, '#5A3A7A'); d(4, 2, 1, 1, '#FF4A5A'); },
  hat: d => { d(0, 5, 8, 1, '#2A1440'); d(2, 3, 4, 2, '#6A3A9A'); d(3, 1, 2, 2, '#6A3A9A'); d(4, 0, 2, 1, '#6A3A9A'); d(2, 4, 4, 1, '#E8B03A'); },
  wisp: d => { d(1, 2, 3, 3, '#6AE8FF'); d(2, 0, 1, 2, '#6AE8FF'); d(2, 3, 1, 1, '#FFFFFF'); d(0, 3, 1, 1, '#3AA8E8'); d(4, 3, 1, 1, '#3AA8E8'); },
  spore: d => { d(0, 0, 2, 2, '#C8A0FF'); d(0, 0, 1, 1, '#FFFFFF'); },
  apple: d => { d(1, 1, 5, 4, '#5AC83A'); d(0, 2, 7, 2, '#5AC83A'); d(1, 2, 2, 1, '#9AF07A'); d(3, 0, 1, 1, '#5A3A1A'); d(4, 0, 1, 1, '#3A8A2A'); d(2, 5, 3, 1, '#3A8A2A'); },
  bubble: d => { d(1, 0, 3, 1, '#C8FFF0'); d(0, 1, 1, 3, '#C8FFF0'); d(4, 1, 1, 3, '#C8FFF0'); d(1, 4, 3, 1, '#C8FFF0'); d(1, 1, 1, 1, '#FFFFFF'); },
};
// ---- 환상 장면 ----
let parts = [], vt0 = 0, vRaf = 0, vD = null, shakeK = 0;
const W = () => innerWidth, H = () => innerHeight;
function spawn(D){
  parts = []; const n = D.long ? 70 : D.p.length > 2 ? 46 : 34;
  for (let i = 0; i < n; i++){ const k = D.p[i % D.p.length], a = Math.random() * Math.PI * 2;
    parts.push({ k, a, r: 20 + Math.random() * 40, sp: .4 + Math.random() * .9, x: Math.random() * W(), y: Math.random() * H(), d: Math.random() * 1.5, s: .8 + Math.random() * .7, w: Math.random() * 6 }); }
}
// ---- 환상 장면: 배경 + 블랑의 자세(날기·튜브·회전·튀기...) + 소품 · 웃기게 ----
const lg = (y0, y1, a, b) => { const q = g.createLinearGradient(0, y0, 0, y1); q.addColorStop(0, a); q.addColorStop(1, b); return q; };
const rect = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
const circ = (x, y, r, c) => { g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); };
const ell = (x, y, rx, ry, c) => { g.fillStyle = c; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill(); };
const cloud = (x, y, s, c = '#FFFFFF') => { ell(x, y, 30 * s, 14 * s, c); ell(x - 22 * s, y + 4 * s, 18 * s, 10 * s, c); ell(x + 24 * s, y + 3 * s, 20 * s, 11 * s, c); ell(x + 4 * s, y - 9 * s, 18 * s, 12 * s, c); };
// 블랑 그리기: x, y = 발 밑 가운데 · s 배율 · o = { rot, fx 좌우 뒤집기(-1~1), glasses, crown, towel, veil, clip(발 쪽 자르기 0~1), arms 만세, cart }
function blanc(x, y, s, o = {}){
  const w = 64 * s; g.save(); g.translate(x, y); g.rotate(o.rot || 0); g.scale(o.fx ?? 1, 1);
  if (o.clip){ g.beginPath(); g.rect(-w, -w * 1.2, w * 2, w * (1.2 - o.clip * .45)); g.clip(); }
  g.drawImage(SH, 0, 0, 64, 64, -w / 2, -w * .97, w, w);
  const u = s;   // 64 칸 기준 좌표 → 화면
  const P2 = (gx, gy, gw, gh, c) => rect(-w / 2 + gx * u, -w * .97 + gy * u, gw * u, gh * u, c);
  if (o.glasses){ P2(24, 23, 7, 4, '#111'); P2(33, 23, 7, 4, '#111'); P2(31, 24, 2, 1, '#111'); P2(25, 23, 2, 1, '#6AF'); P2(34, 23, 2, 1, '#6AF'); }
  if (o.crown){ P2(23, -2, 18, 5, '#FFD040'); P2(23, -5, 3, 3, '#FFD040'); P2(30, -6, 4, 4, '#FFD040'); P2(38, -5, 3, 3, '#FFD040'); P2(31, -1, 2, 2, '#E83A5A'); }
  if (o.towel){ P2(22, 0, 20, 5, '#FFFFFF'); P2(22, 4, 20, 1, '#C8C8D8'); }
  if (o.veil){ P2(20, 4, 4, 22, 'rgba(255,255,255,.75)'); P2(40, 4, 4, 22, 'rgba(255,255,255,.75)'); }
  if (o.arms){ P2(14, 18, 5, 14, '#C8CCD8'); P2(45, 18, 5, 14, '#C8CCD8'); P2(14, 14, 5, 5, '#E8ECF4'); P2(45, 14, 5, 5, '#E8ECF4'); }
  if (o.mic){ P2(44, 30, 3, 8, '#333'); P2(43, 27, 5, 4, '#999'); }
  if (o.sticks){ const a = Math.sin(o.t * 18) * .5; g.save(); g.translate(-w / 2 + 16 * u, -w * .97 + 34 * u); g.rotate(-1 + a); rect(0, 0, 3 * u, -16 * u, '#E8C890'); g.restore(); g.save(); g.translate(-w / 2 + 48 * u, -w * .97 + 34 * u); g.rotate(1 - a); rect(0, 0, 3 * u, -16 * u, '#E8C890'); g.restore(); }
  if (o.cup){ P2(44, 32, 6, 6, '#FFF'); P2(50, 33, 2, 3, '#FFF'); P2(45, 33, 4, 2, '#C88A3A'); }
  g.restore();
}
const speed = (t, c = 'rgba(255,255,255,.6)', dir = 'h') => { for (let i = 0; i < 14; i++){ const y = (i * 61 + t * 900) % H(), x = (i * 97 + t * 1300) % W(); if (dir === 'h') rect(W() - x, (i * 53) % H(), 40 + (i % 3) * 20, 2, c); else rect((i * 53) % W(), y, 2, 40 + (i % 3) * 20, c); } };
const SCENE = {
  sky(t, w, h){ g.fillStyle = lg(0, h, '#5AB8FF', '#FFE0B0'); g.fillRect(0, 0, w, h); circ(w * .82, h * .12, 34, '#FFF2A0');
    for (let i = 0; i < 6; i++) cloud(((i * 170 - t * 160) % (w + 200) + w + 200) % (w + 200) - 100, 80 + i * 70 % 300, .8 + (i % 3) * .3);
    for (let i = 0; i < 14; i++){ const x = ((i * 60 - t * 260) % (w + 80) + w + 80) % (w + 80) - 40; g.save(); g.translate(x, h * .86 + (i % 2) * 18); SPR.pumpkin(at(-12, -12)); g.restore(); } rect(0, h * .9, w, h * .1, '#3A6A2A');
    const x = w * .45 + Math.sin(t * 1.3) * 30, y = h * .5 + Math.sin(t * 2.2) * 24; g.strokeStyle = '#E83A3A'; g.lineWidth = 6; g.beginPath(); for (let k = 0; k < 8; k++) g.lineTo(x - 30 - k * 16, y - 150 + Math.sin(t * 8 + k) * 8); g.stroke();
    blanc(x, y, 3.2, { rot: -.35, arms: 1 }); speed(t); },
  beach(t, w, h){ g.fillStyle = lg(0, h * .45, '#4AC8FF', '#BFF0FF'); g.fillRect(0, 0, w, h * .45); circ(w * .2, h * .1, 30, '#FFE860');
    rect(0, h * .45, w, h * .3, '#2A8AD8'); for (let i = 0; i < 9; i++){ const y = h * .47 + i * 26, o = (t * 40 + i * 30) % 40; for (let x = -40 + o; x < w; x += 40) rect(x, y, 18, 3, 'rgba(255,255,255,.45)'); }
    rect(0, h * .75, w, h * .25, '#F0D890'); rect(w * .78, h * .5, 10, h * .27, '#8A5A2A'); for (let k = 0; k < 5; k++){ g.save(); g.translate(w * .78 + 5, h * .5); g.rotate(-1.4 + k * .7); ell(30, 0, 34, 8, '#3AA83A'); g.restore(); }
    const by = h * .6 + Math.sin(t * 2) * 10; blanc(w * .42, by + 6, 3, { glasses: 1, clip: 1, rot: Math.sin(t * 1.5) * .08, cup: 1 });
    g.strokeStyle = '#FF6A3A'; g.lineWidth = 18; g.beginPath(); g.ellipse(w * .42, by - 60, 62, 16, 0, -.1, Math.PI + .1); g.stroke(); g.strokeStyle = '#FFFFFF'; g.lineWidth = 18; g.setLineDash([16, 22]); g.beginPath(); g.ellipse(w * .42, by - 60, 62, 16, 0, -.1, Math.PI + .1); g.stroke(); g.setLineDash([]);
    for (let i = 0; i < 3; i++){ const x = (t * 60 + i * 140) % (w + 60) - 30, y = h * .15 + i * 40 + Math.sin(t * 4 + i) * 8; g.strokeStyle = '#333'; g.lineWidth = 3; g.beginPath(); g.moveTo(x - 10, y); g.lineTo(x, y + 6); g.lineTo(x + 10, y); g.stroke(); }
    const cx = (t * 50) % (w + 40) - 20; ell(cx, h * .88, 12, 8, '#E83A2A'); rect(cx - 16, h * .86, 6, 3, '#E83A2A'); rect(cx + 10, h * .86, 6, 3, '#E83A2A'); },
  space(t, w, h){ g.fillStyle = lg(0, h, '#0A0A2A', '#2A1050'); g.fillRect(0, 0, w, h); for (let i = 0; i < 70; i++){ const a = .4 + .6 * Math.abs(Math.sin(t * 2 + i)); rect((i * 73) % w, (i * 131) % h, 2, 2, `rgba(255,255,255,${a})`); }
    circ(w * .78, h * .2, 46, '#F07A18'); circ(w * .74, h * .18, 46 * .4, '#FF9A3A'); g.strokeStyle = '#FFD84A'; g.lineWidth = 5; g.beginPath(); g.ellipse(w * .78, h * .2, 80, 16, -.3, 0, 7); g.stroke(); rect(w * .78 - 3, h * .2 - 52, 6, 10, '#5A7A22');
    const x = w / 2 + Math.sin(t * .7) * 40, y = h * .62 + Math.sin(t) * 20; g.globalAlpha = .25; circ(x, y - 130, 80, '#BFE8FF'); g.globalAlpha = 1; blanc(x, y, 3, { rot: t * .5, cup: 1 }); },
  ballroom(t, w, h){ rect(0, 0, w, h, '#3A0A1E'); for (let r = 0; r < 8; r++) for (let c = 0; c < 10; c++) rect(c * w / 10, h * .6 + r * h * .05, w / 10, h * .05, (r + c) % 2 ? '#1A0A12' : '#E8D8C8');
    for (let k = 0; k < 3; k++){ const x = w * (.2 + k * .3); rect(x - 1, 0, 2, 50, '#C8A040'); circ(x, 60, 22, '#FFE8A0'); for (let j = 0; j < 6; j++) circ(x - 20 + j * 8, 76, 3, '#FFF6C8'); }
    blanc(w / 2, h * .66, 3.3, { fx: Math.cos(t * 7), rot: Math.sin(t * 7) * .1 }); },
  coaster(t, w, h){ g.fillStyle = lg(0, h, '#1A1040', '#C83A6A'); g.fillRect(0, 0, w, h); const Y = x => h * .55 + Math.sin(x / w * Math.PI * 3 - 1) * h * .18;
    g.strokeStyle = '#E8C890'; g.lineWidth = 6; g.beginPath(); for (let x = 0; x <= w; x += 6) g.lineTo(x, Y(x)); g.stroke(); for (let x = 0; x < w; x += 24){ rect(x, Y(x), 3, h - Y(x), 'rgba(232,200,144,.35)'); }
    const x = (t * 160) % (w + 100) - 50, y = Y(x), a = Math.atan2(Y(x + 4) - y, 4); g.save(); g.translate(x, y); g.rotate(a); rect(-50, -30, 100, 30, '#E83A3A'); rect(-50, -30, 100, 6, '#FFD84A'); g.restore();
    blanc(x, y - 18, 2.4, { rot: a, arms: 1 }); speed(t, 'rgba(255,255,255,.35)'); },
  bounce(t, w, h){ g.fillStyle = lg(0, h, '#6A3AB8', '#2A0A40'); g.fillRect(0, 0, w, h); const ph = (t * 1.6) % 1, hit = ph > .9, sq = hit ? 1 + Math.sin((ph - .9) * 31) * .25 : 1;
    ell(w / 2, h * .82, w * .48 * sq, 50 / sq, '#5AD84A'); ell(w / 2 - 50, h * .8, 40, 12, '#9AF07A'); circ(w / 2 - 80, h * .8, 10, '#FFF'); circ(w / 2 - 80, h * .8, 5, '#222'); circ(w / 2 + 70, h * .82, 10, '#FFF'); circ(w / 2 + 70, h * .82, 5, '#222');
    const y = h * .78 - Math.sin(ph * Math.PI) * h * .45; blanc(w / 2, y, 3, { rot: Math.sin(t * 5) * .2, arms: ph < .5 }); },
  hotspring(t, w, h){ rect(0, 0, w, h, '#14102A'); for (let i = 0; i < 40; i++) rect((i * 89) % w, (i * 41) % (h * .4), 2, 2, '#FFF6C8'); ell(w / 2, h * .66, w * .48, 90, '#6A6478'); ell(w / 2, h * .66, w * .42, 70, '#FFC8D8');
    for (let i = 0; i < 4; i++){ const r = ((t * 40 + i * 30) % 120); g.strokeStyle = `rgba(255,255,255,${1 - r / 120})`; g.lineWidth = 2; g.beginPath(); g.ellipse(w / 2, h * .66, r * 1.6, r * .4, 0, 0, 7); g.stroke(); }
    blanc(w / 2, h * .66, 3, { clip: .55, towel: 1, rot: Math.sin(t) * .05 }); ell(w / 2, h * .655, 70, 14, 'rgba(255,200,216,.85)'); const dx = w / 2 + 90 + Math.sin(t * 1.5) * 20; ell(dx, h * .66, 16, 12, '#FFD84A'); circ(dx - 10, h * .64 - 8, 8, '#FFD84A'); rect(dx - 22, h * .64 - 8, 6, 3, '#F07A18');
    for (let i = 0; i < 6; i++){ const y = h * .55 - ((t * 30 + i * 40) % 200); g.globalAlpha = Math.max(0, .5 - ((t * 30 + i * 40) % 200) / 400); cloud(w * .2 + i * 50, y, .5); g.globalAlpha = 1; } },
  cloud(t, w, h){ g.fillStyle = lg(0, h, '#FFC8E8', '#A08AE8'); g.fillRect(0, 0, w, h); for (let i = 0; i < 5; i++) cloud((i * 120 + t * 20) % (w + 120) - 60, 100 + i * 120, 1.2, '#FFF0FA');
    const y = h * .6 + Math.sin(t * 1.4) * 14; cloud(w / 2, y + 10, 2.4, '#FFFFFF'); blanc(w / 2 + 10, y - 14, 3, { rot: -1.45 }); },
  drum(t, w, h){ rect(0, 0, w, h, '#100A18'); for (let k = 0; k < 3; k++){ g.fillStyle = `hsla(${(t * 120 + k * 120) % 360},90%,60%,.25)`; g.beginPath(); g.moveTo(w * (.2 + k * .3), 0); g.lineTo(w * (.05 + k * .3), h * .8); g.lineTo(w * (.35 + k * .3), h * .8); g.fill(); }
    rect(0, h * .8, w, h * .2, '#3A2A1A'); ell(w / 2, h * .76, 60, 24, '#E8E0D0'); rect(w / 2 - 60, h * .76, 120, 30, '#C83A3A'); ell(w / 2 + 90, h * .66, 26, 8, '#FFD84A');
    blanc(w / 2, h * .72 - Math.abs(Math.sin(t * 9)) * 16, 3, { sticks: 1, t }); },
  balloon(t, w, h){ g.fillStyle = lg(0, h, '#6AC8FF', '#E8F8FF'); g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) cloud(((i * 150 + t * 30) % (w + 160)) - 80, (h - ((t * 60 + i * 200) % (h + 100))), 1);
    const k = Math.min(1.8, 1 + t * .25), y = h * .75 - Math.min(h * .4, t * 40); g.save(); g.translate(w / 2, y); g.scale(k, 1 + (k - 1) * .5); blanc(0, 0, 3, { rot: Math.sin(t * 2) * .1 }); g.restore();
    g.strokeStyle = '#FFF'; g.lineWidth = 2; g.beginPath(); g.moveTo(w / 2, y); for (let i = 1; i < 10; i++) g.lineTo(w / 2 + Math.sin(t * 3 + i) * 8, y + i * 30); g.stroke(); },
  rocket(t, w, h){ g.fillStyle = lg(0, h, '#0A0A30', '#3A6AC8'); g.fillRect(0, 0, w, h); speed(t, 'rgba(255,255,255,.6)', 'v'); for (let i = 0; i < 4; i++) cloud((i * 110) % w, ((t * 500 + i * 220) % (h + 100)) - 50, .9);
    const x = w / 2 + Math.sin(t * 30) * 3, y = h * .62; g.save(); g.translate(x, y); ell(0, 40, 40, 70, '#F07A18'); circ(0, 30, 16, '#BFE8FF'); rect(-46, 70, 20, 40, '#C83A3A'); rect(26, 70, 20, 40, '#C83A3A'); for (let i = 0; i < 6; i++) circ((Math.random() - .5) * 30, 120 + Math.random() * 60, 10 + Math.random() * 10, i % 2 ? '#FFD84A' : '#FF6A2A'); g.restore();
    blanc(x, y - 22, 2.6, { arms: 1, rot: Math.sin(t * 25) * .05 }); },
  wedding(t, w, h){ g.fillStyle = lg(0, h, '#FFE8F0', '#E8C8FF'); g.fillRect(0, 0, w, h); g.strokeStyle = '#FFFFFF'; g.lineWidth = 16; g.beginPath(); g.arc(w / 2, h * .5, w * .38, Math.PI, 0); g.stroke(); rect(0, h * .78, w, h * .22, '#C8A0D8'); rect(w / 2 - 20, h * .78, 40, h * .22, '#E83A5A');
    const sw = Math.sin(t * 6) * .3; g.save(); g.translate(w * .25, h * .2); g.rotate(sw); ell(0, 14, 16, 18, '#FFD84A'); g.restore(); g.save(); g.translate(w * .75, h * .2); g.rotate(-sw); ell(0, 14, 16, 18, '#FFD84A'); g.restore();
    g.save(); g.translate(w * .2, h * .74); SPR.pumpkin((x, y, a, b, c) => rect(x * 7 - 28, y * 7 - 42, a * 7, b * 7, c)); g.restore(); g.save(); g.translate(w * .8, h * .74); SPR.apple((x, y, a, b, c) => rect(x * 7 - 24, y * 7 - 42, a * 7, b * 7, c)); rect(-30, -50, 60, 8, 'rgba(255,255,255,.8)'); g.restore();
    blanc(w / 2, h * .7, 2.8, { veil: 0, rot: Math.sin(t * 2) * .05 }); },
  surf(t, w, h){ g.fillStyle = lg(0, h, '#1A3A1A', '#0A140A'); g.fillRect(0, 0, w, h); g.fillStyle = '#5AB83A'; g.beginPath(); g.moveTo(0, h); for (let x = 0; x <= w; x += 8) g.lineTo(x, h * .6 + Math.sin(x / 50 + t * 4) * 30 - (x / w) * h * .2); g.lineTo(w, h); g.fill();
    g.fillStyle = '#9AF07A'; for (let x = 0; x < w; x += 30) circ(x + (t * 80 % 30), h * .58 + Math.sin(x / 50 + t * 4) * 30 - (x / w) * h * .2, 6, '#C8FFB0');
    const x = w * .45 + Math.sin(t) * 40, y = h * .55 + Math.sin(x / 50 + t * 4) * 30 - (x / w) * h * .2, a = -.35 + Math.sin(t * 3) * .15; g.save(); g.translate(x, y); g.rotate(a); ell(0, 0, 70, 10, '#C8C8D8'); ell(60, -4, 24, 14, '#E8E8F0'); g.restore();
    blanc(x, y - 4, 2.8, { rot: a, arms: 1 }); },
  disco(t, w, h){ rect(0, 0, w, h, '#0A0614'); for (let r = 0; r < 5; r++) for (let c = 0; c < 6; c++) rect(c * w / 6, h * .72 + r * 50, w / 6 - 2, 48, `hsl(${(r * 60 + c * 40 + t * 300) % 360},80%,${(r + c + Math.floor(t * 6)) % 2 ? 55 : 25}%)`);
    rect(w / 2 - 1, 0, 2, 70, '#AAA'); circ(w / 2, 100, 34, '#C8C8D8'); for (let i = 0; i < 24; i++){ const a = i / 24 * Math.PI * 2 + t; rect(w / 2 + Math.cos(a) * 26 - 3, 100 + Math.sin(a) * 26 - 3, 6, 6, '#FFF'); g.fillStyle = 'rgba(255,255,255,.5)'; rect(w / 2 + Math.cos(a * 3) * w * .45, 100 + Math.abs(Math.sin(a * 2)) * h * .6, 4, 4, '#FFF'); }
    blanc(w / 2, h * .76 - Math.abs(Math.sin(t * 8)) * 12, 3, { fx: Math.sign(Math.sin(t * 4)) || 1, arms: Math.sin(t * 8) > 0, glasses: 1 }); },
  throne(t, w, h){ rect(0, 0, w, h, '#2A0A14'); for (let r = 0; r < 12; r++) for (let c = 0; c < 6; c++) rect(c * w / 6 + (r % 2) * 30, r * 50, w / 6 - 4, 46, '#3A1420'); rect(w / 2 - 50, h * .55, 100, h * .45, '#C81E3A'); rect(w / 2 - 70, h * .28, 140, 200, '#5A0A1A'); rect(w / 2 - 70, h * .28, 140, 10, '#FFD040');
    for (let k = 0; k < 2; k++){ const x = k ? w * .85 : w * .15; rect(x - 4, h * .5, 8, 60, '#F0E8D0'); circ(x, h * .5 - 8 + Math.sin(t * 12 + k) * 2, 7, '#FFB040'); }
    blanc(w / 2, h * .62, 3, { crown: 1, cup: 1, rot: Math.sin(t * 2) * .04 }); },
  parade(t, w, h){ g.fillStyle = lg(0, h, '#1A0A30', '#5A1A3A'); g.fillRect(0, 0, w, h); for (let k = 0; k < 4; k++){ const T = (t * .8 + k * .37) % 1, x = w * (.15 + k * .23), y = h * .3 - k * 20; for (let i = 0; i < 14; i++){ const a = i / 14 * Math.PI * 2; circ(x + Math.cos(a) * T * 70, y + Math.sin(a) * T * 70, 4 * (1 - T), `hsl(${k * 80 + i * 10},90%,65%)`); } }
    g.strokeStyle = '#3A2A1A'; g.lineWidth = 2; g.beginPath(); g.moveTo(0, h * .45); g.quadraticCurveTo(w / 2, h * .52, w, h * .45); g.stroke(); for (let i = 0; i < 9; i++) circ(i * w / 8, h * .46 + Math.sin(i / 8 * Math.PI) * h * .05, 8, i % 2 ? '#FF9A3A' : '#FFD84A');
    rect(0, h * .8, w, h * .2, '#4A3A5A'); const x = w / 2 + Math.sin(t * .8) * 30; rect(x - 80, h * .72, 160, 40, '#F07A18'); rect(x - 80, h * .72, 160, 8, '#FFD84A'); circ(x - 50, h * .8, 14, '#333'); circ(x + 50, h * .8, 14, '#333');
    blanc(x, h * .73, 2.8, { arms: Math.sin(t * 6) > 0 }); },
};
const MONT = ['sky', 'beach', 'space', 'disco', 'rocket', 'parade'];
const POPC = ['#FFE860', '#FF6AA0', '#6AE8FF', '#9AF07A'];
function drawVision(t){
  const D = vD, w = W(), h = H(); if (cv.width !== w * 2){ cv.width = w * 2; cv.height = h * 2; } g.setTransform(2, 0, 0, 2, 0, 0); g.imageSmoothingEnabled = false;
  const sx = shakeK ? (Math.random() - .5) * 6 * shakeK : 0, sy = shakeK ? (Math.random() - .5) * 6 * shakeK : 0; g.translate(sx, sy);
  const sc = D.scene === 'montage' ? MONT[Math.floor(t / 1.7) % MONT.length] : D.scene; (SCENE[sc] || SCENE.sky)(t, w, h);
  parts.forEach((q, i) => { if (i % 2) return; const T = t - q.d; if (T < 0) return; const x = q.x + Math.sin(T * 2 + q.w) * 14, y = -30 + ((T * 70 * q.sp + q.y) % (h + 60)); g.save(); g.translate(x, y); g.scale(q.s * .8, q.s * .8); SPR[q.k](at(-9, -9)); g.restore(); });   // 요리 재료가 조금씩 흩날려요
  (D.pop || []).forEach((p, i) => { const T = (t * .7 + i * .5) % 1.6; if (T > 1) return; const x = w * (.18 + ((i * 37) % 64) / 100), y = h * (.32 + ((i * 23) % 30) / 100) - T * 30, s = 1 + Math.min(T * 4, 1) * .6;
    g.save(); g.translate(x, y); g.rotate((i % 2 ? 1 : -1) * .18); g.scale(s, s); g.font = '22px G9, monospace'; g.textAlign = 'center'; g.lineWidth = 6; g.strokeStyle = '#1A0A24'; g.strokeText(p + '!', 0, 0); g.fillStyle = POPC[i % POPC.length]; g.fillText(p + '!', 0, 0); g.restore(); });
  g.setTransform(1, 0, 0, 1, 0, 0);
}
function visionStart(D){ vD = D; spawn(D); vt0 = performance.now(); shakeK = D.shake || 0; vis.classList.add('on'); cancelAnimationFrame(vRaf); const loop = now => { drawVision((now - vt0) / 1000); vRaf = requestAnimationFrame(loop); }; vRaf = requestAnimationFrame(loop); }
function visionStop(){ vis.classList.remove('on'); setTimeout(() => cancelAnimationFrame(vRaf), 500); }
const yell = async (t, ms = 2300) => { shout.textContent = fill(t); shout.classList.add('on'); await sleep(ms); shout.classList.remove('on'); await sleep(260); };
const dishCanvas = (i, size) => `<canvas width="32" height="32" data-bfdi="${i}" style="width:${size}px;height:${size}px"></canvas>`;
const drawDishes = () => card.querySelectorAll('canvas[data-bfdi]').forEach(c => { const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(DI, +c.dataset.bfdi * 32, 0, 32, 32, 0, 0, 32, 32); });
async function taste(i, first = true){
  const D = R.dishes[i];
  await showCard(`${dishCanvas(i, 96)}${D.name}<small>무슈 블랑에게 건넸어요${D.kind ? ` · ${D.kind} 요리` : ''}</small>`, drawDishes, 1700);
  await talk(D.sniff, 1200);
  await talk(D.bite, 700);
  clearInterval(bob); for (let k = 0; k < 6; k++){ place(k % 2 ? 0 : 2, 1); await sleep(110); }   // 들썩
  visionStart(D); await sleep(500);
  for (const v of D.vision) await yell(v, D.long ? 2800 : 2300);
  title.style.setProperty('--g', D.bg[0]); title.innerHTML = `<small>무슈 블랑의 맛 표현</small><span>「${D.title}」</span>`; title.classList.add('on'); if (D.shake){ shakeK = 2.5; setTimeout(() => shakeK = D.shake ? .6 : 0, 700); }
  await sleep(D.long ? 3000 : 2200); title.classList.remove('on'); await sleep(300); visionStop(); await sleep(600);
  bobOn();
  if (!first) await talk(R.repeat[i % R.repeat.length], 1300);
  for (const a of D.after) await talk(a, 1400);
  await showCard(`<div class="st">${'★'.repeat(D.stars)}${'☆'.repeat(3 - D.stars)}</div>무슈 블랑의 한 줄 평<small>「${D.review}」</small>`, null, 2400);
}
window.__bfGo = async (list = [0]) => {
  await ready; await sleep(1200);
  for (let k = 1; k <= 10; k++){ place(0, k / 10); await sleep(110); } bobOn();
  await talk('오, 또 왔군. 오늘은 무엇을 가져왔나.', 1200);
  for (const i of list) await taste(i);
  clearInterval(bob); await sleep(800); window.__bfDone = true;
};
window.__bfPeak = async i => {   // 장면 모음용: 환상 + 첫 외침 + 제목을 한 화면에
  await ready; const D = R.dishes[i]; visionStart(D); shakeK = 0; shout.textContent = fill(D.vision[0]); shout.classList.add('on');
  title.style.setProperty('--g', D.bg[0]); title.innerHTML = `<small>${D.name}</small><span>「${D.title}」</span>`; title.classList.add('on'); await sleep(1600); return true;
};
window.__bfClear = () => { shout.classList.remove('on'); title.classList.remove('on'); vis.classList.remove('on'); cancelAnimationFrame(vRaf); };
})();
