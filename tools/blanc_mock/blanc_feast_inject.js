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
const cv = vis.querySelector('canvas'), G0 = cv.getContext('2d'); let g = G0;
// 우리 그림체: 환상 장면은 1/3 크기 캔버스에 그리고 픽셀 그대로 3배로 키워요 (블랑 스프라이트가 원래 도트 크기로 맞아요)
const LO = 3, lo = document.createElement('canvas'), LG = lo.getContext('2d');
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
const P = 3;   // 입자 점 하나 = 작은 캔버스 1 픽셀
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
const hx2 = c => { const m = /^#([0-9a-f]{6})$/i.exec(c); return m ? [0, 2, 4].map(i => parseInt(m[1].slice(i, i + 2), 16)) : null; };
const shade = (c, k) => { const v = hx2(c); if (!v) return c; return '#' + v.map(x => Math.max(0, Math.min(255, Math.round(k > 1 ? x + (255 - x) * (k - 1) : x * k))).toString(16).padStart(2, '0')).join(''); };
const mix = (a, b, t) => { const A = hx2(a), B = hx2(b); if (!A || !B) return a; return '#' + A.map((x, i) => Math.round(x + (B[i] - x) * t).toString(16).padStart(2, '0')).join(''); };
const lg = (y0, y1, a, b, n = 7) => { const q = g.createLinearGradient(0, y0, 0, y1); for (let i = 0; i < n; i++){ const c = mix(a, b, i / (n - 1)); q.addColorStop(i / n, c); q.addColorStop((i + 1) / n - .0001, c); } return q; };   // 띠처럼 끊어진 그러데이션 (도트 느낌)
const rect = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
const flat = (x, y, rx, ry, c) => { g.fillStyle = c; g.beginPath(); g.ellipse(x, y, Math.max(.5, rx), Math.max(.5, ry), 0, 0, 7); g.fill(); };
// 동그란 소품: 진한 테두리 → 어두운 면(오른쪽 아래) → 기본색 → 밝은 점(왼쪽 위) · 색이 #RRGGBB가 아니면 그냥 칠해요
const blob = (x, y, rx, ry, c) => { if (!hx2(c) || rx < 4) return flat(x, y, rx, ry, c); const o = LO;
  flat(x, y, rx + o, ry + o, shade(c, .3)); flat(x, y, rx, ry, shade(c, .72)); flat(x - o * .7, y - o * .7, rx - o, ry - o, c); flat(x - rx * .35, y - ry * .38, rx * .32, ry * .28, shade(c, 1.35)); };
const circ = (x, y, r, c) => blob(x, y, r, r, c);
const ell = (x, y, rx, ry, c) => blob(x, y, rx, ry, c);
const CLP = s => [[0, 0, 30, 14], [-22, 4, 18, 10], [24, 3, 20, 11], [4, -9, 18, 12]].map(([a, b, c, d]) => [a * s, b * s, c * s, d * s]);
const cloud = (x, y, s, c = '#FFFFFF') => { const L = CLP(s), o = LO; L.forEach(([a, b, rx, ry]) => flat(x + a, y + b, rx + o, ry + o, hx2(c) ? mix(c, '#3A2A5A', .55) : c)); L.forEach(([a, b, rx, ry]) => flat(x + a, y + b + o, rx, ry, hx2(c) ? mix(c, '#8A7AB8', .35) : c)); L.forEach(([a, b, rx, ry]) => flat(x + a, y + b - o * .4, rx - o, ry - o, c)); };
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
    const x = w * .45 + Math.sin(t * 1.3) * 30, y = h * .5 + Math.sin(t * 2.2) * 24; g.strokeStyle = '#4A0A10'; g.lineWidth = 12; g.beginPath(); for (let k = 0; k < 8; k++) g.lineTo(x - 30 - k * 16, y - 150 + Math.sin(t * 8 + k) * 8); g.stroke(); g.strokeStyle = '#E83A3A'; g.lineWidth = 6; g.beginPath(); for (let k = 0; k < 8; k++) g.lineTo(x - 30 - k * 16, y - 150 + Math.sin(t * 8 + k) * 8); g.stroke();
    blanc(x, y, 3.2, { rot: -.35, arms: 1 }); speed(t); },
  beach(t, w, h){ g.fillStyle = lg(0, h * .45, '#4AC8FF', '#BFF0FF'); g.fillRect(0, 0, w, h * .45); circ(w * .2, h * .1, 30, '#FFE860');
    rect(0, h * .45, w, h * .3, '#2A8AD8'); for (let i = 0; i < 9; i++){ const y = h * .47 + i * 26, o = (t * 40 + i * 30) % 40; for (let x = -40 + o; x < w; x += 40) rect(x, y, 18, 3, 'rgba(255,255,255,.45)'); }
    rect(0, h * .75, w, h * .25, '#F0D890'); rect(w * .78, h * .5, 10, h * .27, '#8A5A2A'); for (let k = 0; k < 5; k++){ g.save(); g.translate(w * .78 + 5, h * .5); g.rotate(-1.4 + k * .7); ell(30, 0, 34, 8, '#3AA83A'); g.restore(); }
    const by = h * .6 + Math.sin(t * 2) * 10; blanc(w * .42, by + 6, 3, { glasses: 1, clip: 1, rot: Math.sin(t * 1.5) * .08, cup: 1 });
    g.strokeStyle = '#4A1408'; g.lineWidth = 26; g.beginPath(); g.ellipse(w * .42, by - 60, 62, 16, 0, -.1, Math.PI + .1); g.stroke(); g.strokeStyle = '#FF6A3A'; g.lineWidth = 18; g.beginPath(); g.ellipse(w * .42, by - 60, 62, 16, 0, -.1, Math.PI + .1); g.stroke(); g.strokeStyle = '#FFB08A'; g.lineWidth = 4; g.beginPath(); g.ellipse(w * .42, by - 64, 58, 12, 0, .3, Math.PI - .3); g.stroke(); g.strokeStyle = '#FFFFFF'; g.lineWidth = 18; g.setLineDash([16, 22]); g.beginPath(); g.ellipse(w * .42, by - 60, 62, 16, 0, -.1, Math.PI + .1); g.stroke(); g.setLineDash([]);
    for (let i = 0; i < 3; i++){ const x = (t * 60 + i * 140) % (w + 60) - 30, y = h * .15 + i * 40 + Math.sin(t * 4 + i) * 8; g.strokeStyle = '#333'; g.lineWidth = 3; g.beginPath(); g.moveTo(x - 10, y); g.lineTo(x, y + 6); g.lineTo(x + 10, y); g.stroke(); }
    const cx = (t * 50) % (w + 40) - 20; ell(cx, h * .88, 12, 8, '#E83A2A'); rect(cx - 16, h * .86, 6, 3, '#E83A2A'); rect(cx + 10, h * .86, 6, 3, '#E83A2A'); },
  space(t, w, h){ g.fillStyle = lg(0, h, '#0A0A2A', '#2A1050'); g.fillRect(0, 0, w, h); for (let i = 0; i < 70; i++){ const a = .4 + .6 * Math.abs(Math.sin(t * 2 + i)); rect((i * 73) % w, (i * 131) % h, 2, 2, `rgba(255,255,255,${a})`); }
    circ(w * .78, h * .2, 46, '#F07A18'); circ(w * .74, h * .18, 46 * .4, '#FF9A3A'); g.strokeStyle = '#FFD84A'; g.lineWidth = 5; g.beginPath(); g.ellipse(w * .78, h * .2, 80, 16, -.3, 0, 7); g.stroke(); rect(w * .78 - 3, h * .2 - 52, 6, 10, '#5A7A22');
    const x = w / 2 + Math.sin(t * .7) * 40, y = h * .62 + Math.sin(t) * 20; g.globalAlpha = .25; circ(x, y - 130, 80, '#BFE8FF'); g.globalAlpha = 1; blanc(x, y, 3, { rot: t * .5, cup: 1 }); },
  ballroom(t, w, h){ rect(0, 0, w, h, '#3A0A1E'); for (let r = 0; r < 8; r++) for (let c = 0; c < 10; c++) rect(c * w / 10, h * .6 + r * h * .05, w / 10, h * .05, (r + c) % 2 ? '#1A0A12' : '#E8D8C8');
    for (let k = 0; k < 3; k++){ const x = w * (.2 + k * .3); rect(x - 1, 0, 2, 50, '#C8A040'); circ(x, 60, 22, '#FFE8A0'); for (let j = 0; j < 6; j++) circ(x - 20 + j * 8, 76, 3, '#FFF6C8'); }
    blanc(w / 2, h * .66, 3.3, { fx: Math.cos(t * 7), rot: Math.sin(t * 7) * .1 }); },
  coaster(t, w, h){ g.fillStyle = lg(0, h, '#1A1040', '#C83A6A'); g.fillRect(0, 0, w, h); const Y = x => h * .55 + Math.sin(x / w * Math.PI * 3 - 1) * h * .18;
    g.strokeStyle = '#3A2410'; g.lineWidth = 12; g.beginPath(); for (let x = 0; x <= w; x += 6) g.lineTo(x, Y(x)); g.stroke(); g.strokeStyle = '#E8C890'; g.lineWidth = 6; g.beginPath(); for (let x = 0; x <= w; x += 6) g.lineTo(x, Y(x)); g.stroke(); for (let x = 0; x < w; x += 24){ rect(x, Y(x), 3, h - Y(x), 'rgba(232,200,144,.35)'); }
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
SCENE.ascend = (t, w, h) => {   // 마지막 인사: 빛기둥 속으로 둥실 떠오르며 사라져요
  g.fillStyle = lg(0, h, '#2A1E4A', '#120A24'); g.fillRect(0, 0, w, h); for (let i = 0; i < 50; i++) rect((i * 73) % w, (i * 131) % h, 2, 2, `rgba(255,246,200,${.3 + .5 * Math.abs(Math.sin(t * 2 + i))})`);
  const pw = 90 + Math.sin(t * 2) * 6; g.fillStyle = 'rgba(255,240,190,.18)'; g.fillRect(w / 2 - pw, 0, pw * 2, h); g.fillStyle = 'rgba(255,248,220,.28)'; g.fillRect(w / 2 - pw * .55, 0, pw * 1.1, h); g.fillStyle = 'rgba(255,255,240,.35)'; g.fillRect(w / 2 - pw * .2, 0, pw * .4, h);
  for (let i = 0; i < 24; i++){ const y = h - ((t * 70 + i * 47) % (h + 40)), x = w / 2 + Math.sin(t * 2 + i) * pw * .9; rect(x, y, 3, 3, '#FFF6C8'); if (i % 3 === 0){ rect(x - 3, y + 1, 9, 1, '#FFF6C8'); rect(x + 1, y - 3, 1, 9, '#FFF6C8'); } }
  const y = h * .72 - Math.max(0, t - 1) * 55, a = Math.max(0, Math.min(1, 1 - (t - 3.2) / 1.6)); g.globalAlpha = a; blanc(w / 2, y, 3.2, { rot: Math.sin(t * 2) * .06, arms: t > 1.4 }); g.globalAlpha = 1;
  if (t > 3.6){ const hy = y - 220 + Math.min(1, (t - 3.6) / 1.4) * 260; g.globalAlpha = Math.min(1, (t - 3.6) * 2) * .9; ell(w / 2 + Math.sin(t * 3) * 20, hy, 26, 10, '#F4F0E6'); ell(w / 2 + Math.sin(t * 3) * 20, hy - 14, 20, 16, '#FFFFFF'); g.globalAlpha = 1; }   // 모자만 살랑살랑 내려와요
};
const MONT = ['sky', 'beach', 'space', 'disco', 'rocket', 'parade'];
const POPC = ['#FFE860', '#FF6AA0', '#6AE8FF', '#9AF07A'];
function drawVision(t){
  const D = vD, w = W(), h = H(); if (cv.width !== w * 2){ cv.width = w * 2; cv.height = h * 2; } const lw = Math.ceil(w / LO), lh = Math.ceil(h / LO); if (lo.width !== lw){ lo.width = lw; lo.height = lh; }
  g = LG; g.setTransform(1 / LO, 0, 0, 1 / LO, 0, 0); g.imageSmoothingEnabled = false; g.clearRect(0, 0, w, h);
  const sc = D.scene === 'montage' ? MONT[Math.floor(t / 1.7) % MONT.length] : D.scene; (SCENE[sc] || SCENE.sky)(t, w, h);
  parts.forEach((q, i) => { if (i % 2) return; const T = t - q.d; if (T < 0) return; const x = q.x + Math.sin(T * 2 + q.w) * 14, y = -30 + ((T * 70 * q.sp + q.y) % (h + 60)); g.save(); g.translate(Math.round(x / LO) * LO, Math.round(y / LO) * LO); SPR[q.k](at(-9, -9)); g.restore(); });   // 요리 재료가 조금씩 흩날려요
  g = G0; g.setTransform(1, 0, 0, 1, 0, 0); g.imageSmoothingEnabled = false; g.clearRect(0, 0, cv.width, cv.height);
  const sx = shakeK ? Math.round((Math.random() - .5) * 4 * shakeK) * LO * 2 : 0, sy = shakeK ? Math.round((Math.random() - .5) * 4 * shakeK) * LO * 2 : 0;
  g.drawImage(lo, 0, 0, lw, lh, sx - 6, sy - 6, lw * LO * 2 + 12, lh * LO * 2 + 12);
  g.setTransform(2, 0, 0, 2, 0, 0);
  (D.pop || []).forEach((p, i) => { const T = (t * .7 + i * .5) % 1.6; if (T > 1) return; const x = w * (.18 + ((i * 37) % 64) / 100), y = h * (.32 + ((i * 23) % 30) / 100) - T * 30, s = 1 + Math.min(T * 4, 1) * .6;
    g.save(); g.translate(x, y); g.rotate((i % 2 ? 1 : -1) * .18); g.scale(s, s); g.font = '22px G9, monospace'; g.textAlign = 'center'; g.lineWidth = 6; g.strokeStyle = '#1A0A24'; g.strokeText(p + '!', 0, 0); g.fillStyle = POPC[i % POPC.length]; g.fillText(p + '!', 0, 0); g.restore(); });
  g.setTransform(1, 0, 0, 1, 0, 0);
}
function visionStart(D){ vD = D; spawn(D); vt0 = performance.now(); shakeK = D.shake || 0; vis.classList.add('on'); cancelAnimationFrame(vRaf); const loop = now => { drawVision((now - vt0) / 1000); vRaf = requestAnimationFrame(loop); }; vRaf = requestAnimationFrame(loop); }
function visionStop(){ vis.classList.remove('on'); setTimeout(() => cancelAnimationFrame(vRaf), 500); }
const yell = async (t, ms = 2300) => { shout.textContent = fill(t); shout.classList.add('on'); await sleep(ms); shout.classList.remove('on'); await sleep(260); };
const dishCanvas = (i, size) => `<canvas width="32" height="32" data-bfdi="${i}" style="width:${size}px;height:${size}px"></canvas>`;
const drawDishes = () => card.querySelectorAll('canvas[data-bfdi]').forEach(c => { const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(DI, +c.dataset.bfdi * 32, 0, 32, 32, 0, 0, 32, 32); });
// ---- 소리: 환상이 나오는 동안은 배경 음악을 잠깐 끄고, 장면마다 어울리는 효과음·짧은 음악을 합성해요 ----
//   게임에서는 BGM.hold('blanc') / BGM.release('blanc') + 이 합성기 · 시안 영상에서는 같은 합성기를 OfflineAudioContext로 다시 그려 영상에 붙여요
const SND = (() => {
  let AC = null, T0 = 0; const log = [];
  const mk = (C, D) => {
    const tone = (f, at, d, type = 'triangle', v = .4, f2) => { const o = C.createOscillator(), gn = C.createGain(); o.type = type; o.frequency.setValueAtTime(f, at); if (f2) o.frequency.exponentialRampToValueAtTime(f2, at + d);
      gn.gain.setValueAtTime(.0001, at); gn.gain.exponentialRampToValueAtTime(v, at + .015); gn.gain.exponentialRampToValueAtTime(.0001, at + d); o.connect(gn); gn.connect(D); o.start(at); o.stop(at + d + .05); };
    let NB = null; const nbuf = () => { if (NB && NB.sampleRate === C.sampleRate) return NB; NB = C.createBuffer(1, C.sampleRate * 2, C.sampleRate); const a = NB.getChannelData(0); for (let i = 0; i < a.length; i++) a[i] = Math.random() * 2 - 1; return NB; };
    const noise = (at, d, v = .3, f = 1500, kind = 'lowpass', f2, atk = .02) => { const s = C.createBufferSource(); s.buffer = nbuf(); s.loop = true; const fl = C.createBiquadFilter(); fl.type = kind; fl.frequency.setValueAtTime(f, at); if (f2) fl.frequency.exponentialRampToValueAtTime(f2, at + d);
      const gn = C.createGain(); gn.gain.setValueAtTime(.0001, at); gn.gain.exponentialRampToValueAtTime(v, at + atk); gn.gain.exponentialRampToValueAtTime(.0001, at + d); s.connect(fl); fl.connect(gn); gn.connect(D); s.start(at); s.stop(at + d + .05); };
    const notes = (seq, at, step, type = 'triangle', v = .3, len = .9) => seq.forEach((n, i) => { if (n) tone(440 * Math.pow(2, (n - 69) / 12), at + i * step, step * len * 1.6, type, v); });
    const kick = at => tone(130, at, .18, 'sine', .7, 45), snare = at => noise(at, .12, .35, 3500, 'highpass'), hat = at => noise(at, .04, .12, 8000, 'highpass');
    const SC = {
      sky(a, d){ for (let k = 0; k < d; k += 1.6) noise(a + k, 1.8, .18, 700, 'bandpass', 1400, .5); for (let k = .3; k < d; k += 2.2) noise(a + k, .5, .3, 3000, 'bandpass', 600, .05); },
      beach(a, d){ for (let k = 0; k < d; k += 2.4) noise(a + k, 2.4, .32, 500, 'lowpass', 1600, 1.1); for (let k = .8; k < d; k += 1.9) { tone(1700, a + k, .22, 'sine', .14, 2300); tone(2100, a + k + .25, .3, 'sine', .12, 1500); } },
      space(a, d){ tone(110, a, d, 'sine', .14); tone(165, a + .1, d, 'sine', .08); for (let k = 0; k < d; k += .45) tone(1500 + Math.random() * 1500, a + k, .5, 'sine', .07); },
      ballroom(a, d){ for (let k = 0; k < d; k += .55){ noise(a + k, .35, .16, 900, 'bandpass', 2600, .12); tone(1900, a + k + .2, .04, 'square', .07); tone(1500, a + k + .35, .04, 'square', .06); } for (let k = 2.6; k < d; k += 2.8) for (let c = 0; c < 18; c++) noise(a + k + c * .05 + Math.random() * .03, .05, .12, 2500, 'bandpass'); },   // 치맛자락 휘익 · 구두 또각 · 박수
      coaster(a, d){ for (let k = 0; k < Math.min(1.6, d); k += .1) tone(900, a + k, .03, 'square', .08); tone(400, a + 1.6, 1.4, 'sawtooth', .12, 1400); noise(a + 1.6, 2, .35, 800, 'bandpass', 3000, .3); for (let k = 3.2; k < d; k += 2.6){ noise(a + k, 1.6, .3, 600, 'bandpass', 2600, .2); tone(500, a + k, 1, 'sawtooth', .08, 1600); } },
      bounce(a, d){ for (let k = .55; k < d; k += 1 / 1.6) tone(160, a + k, .35, 'sine', .45, 520); for (let k = .1; k < d; k += 1.25) tone(620, a + k, .12, 'square', .06); },
      hotspring(a, d){ for (let k = 0; k < d; k += .22) tone(300 + Math.random() * 500, a + k, .08, 'sine', .1, 900); noise(a + .3, 1.6, .16, 400, 'lowpass', 200, .4); for (let k = 1.5; k < d; k += 1.7) tone(1800, a + k, .15, 'sine', .12, 900); },
      cloud(a, d){ for (let k = 0; k < d; k += 1.6) notes([60, 64, 67, 72, 76, 79], a + k, .12, 'triangle', .1); tone(98, a, d, 'sine', .08); },
      drum(a, d){ for (let k = 0; k < d; k += .18 + Math.random() * .3) tone(700 + Math.random() * 900, a + k, .05, 'square', .09); for (let k = .4; k < d; k += 2.1) noise(a + k, 1.4, .22, 1000, 'bandpass', 1600, .3); for (let k = 1; k < d; k += 1.7) noise(a + k, .3, .3, 2200, 'highpass'); },   // 해골 뼈 따닥따닥 · 관객 와아 · 심벌 챙
      balloon(a, d){ tone(200, a, Math.min(3.5, d), 'square', .08, 900); for (let k = 0; k < Math.min(3.5, d); k += .35) noise(a + k, .2, .1, 2500, 'bandpass'); for (let k = 3.6; k < d; k += 1.1) tone(900, a + k, .5, 'sine', .1, 600); },
      rocket(a, d){ [0, .6, 1.2].forEach((k, i) => tone(i < 2 ? 660 : 990, a + k, .2, 'square', .12)); noise(a + 1.5, d - 1.5, .5, 300, 'lowpass', 2500, .3); tone(80, a + 1.5, d - 1.5, 'sawtooth', .15, 240); },
      wedding(a, d){   // 축하곡(직접 만든 가락): 땡그랑 종 + 밝은 3박자 가락 + 화음 + 박수
        const B = .5, MEL = [72, 76, 79, 77, 76, 74, 76, 72, 74, 76, 74, 71, 72, 0, 79, 81, 79, 77, 76, 74, 72, 76, 74, 72], CH = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]];
        for (let k = 0, i = 0; k < d; k += B, i++){ const t = a + k, n = MEL[i % MEL.length];
          if (n){ tone(440 * Math.pow(2, (n - 69) / 12), t, B * 1.1, 'triangle', .16); tone(440 * Math.pow(2, (n - 57) / 12), t, B * .6, 'sine', .05); }
          if (i % 3 === 0) CH[(i / 3 | 0) % 4].forEach(c => tone(440 * Math.pow(2, (c - 69) / 12), t, B * 2.8, 'sine', .06)); }
        for (let k = 0; k < d; k += 2) { tone(1046, a + k, 1.4, 'triangle', .14); tone(1568, a + k + .04, 1.1, 'triangle', .08); }
        for (let k = d - 2.4; k < d; k += .06) noise(a + k + Math.random() * .03, .05, .1, 2500, 'bandpass'); },
      surf(a, d){ for (let k = 0; k < d; k += 1.8) noise(a + k, 1.8, .4, 400, 'lowpass', 2400, .6); for (let k = 0; k < d; k += .3) tone(250 + Math.random() * 300, a + k, .07, 'sine', .08, 700); },
      disco(a, d){   // 요란한 EDM: 짧은 빌드업 → 드롭(쿵쿵 킥 · 넓은 화음 · 펌핑 베이스 · 하이햇)
        const B = .47, up = Math.min(2.8, d * .25);
        noise(a, up, .35, 400, 'bandpass', 7000, up * .9); for (let k = 0, s2 = .5; k < up; k += s2, s2 = Math.max(.07, s2 * .78)) snare(a + k);
        tone(220, a, up, 'sawtooth', .12, 1760); tone(70, a + up - .05, .5, 'sine', .8, 35); noise(a + up, .6, .5, 6000, 'highpass');
        const CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], st = a + up;
        for (let k = 0, i = 0; st + k < a + d; k += B, i++){ const t = st + k; kick(t); kick(t);   // 두 번 겹쳐 더 세게
          hat(t + B / 2); hat(t + B * .75); if (i % 2) { snare(t); noise(t, .1, .25, 1800, 'bandpass'); }
          const c = CH[Math.floor(i / 4) % 4]; c.forEach(n => [-.06, 0, .06].forEach(dt => { const f = 440 * Math.pow(2, (n - 57 + dt) / 12) * 2; tone(f, t + .1, B * .8, 'sawtooth', .045); }));   // 쿵 뒤에 화음이 부풀어요(펌핑)
          tone(440 * Math.pow(2, (c[0] - 69) / 12), t + .1, B * .8, 'sawtooth', .16);
          if (i % 8 === 7) [0, .12, .24].forEach(x => tone(1760, t + x, .1, 'square', .08)); }
      },
      throne(a, d){ tone(2600, a + 2.2, .6, 'triangle', .14); tone(3100, a + 2.25, .5, 'triangle', .1); tone(196, a + .5, d, 'triangle', .06); },
      parade(a, d){   // 행진곡(직접 만든 가락): 둥 짝 둥 짝 북 + 금관 가락 + 화음, 사이사이 폭죽과 환호
        const B = .42, MEL = [67, 0, 72, 72, 74, 72, 71, 72, 76, 0, 74, 72, 71, 69, 67, 0, 69, 71, 72, 69, 67, 72, 76, 79, 77, 76, 74, 71, 72, 0, 72, 0], BAS = [48, 55, 48, 55, 53, 57, 55, 50];
        for (let k = 0, i = 0; k < d; k += B / 2, i++){ const t = a + k; if (i % 2 === 0) kick(t); else snare(t); if (i % 4 === 3) noise(t + B / 4, .05, .2, 3500, 'highpass');
          const n = MEL[i % MEL.length]; if (n){ tone(440 * Math.pow(2, (n - 69) / 12), t, B * .45, 'sawtooth', .09); tone(440 * Math.pow(2, (n - 69) / 12) * 2, t, B * .3, 'square', .03); }
          if (i % 2 === 0) tone(440 * Math.pow(2, (BAS[(i / 2 | 0) % 8] - 69) / 12), t, B * .4, 'triangle', .16); }
        for (let k = 1.2; k < d; k += 2.3){ tone(300, a + k, .4, 'sine', .07, 1200); noise(a + k + .4, .6, .3, 2500, 'lowpass', 400, .01); }
        noise(a, d, .06, 900, 'bandpass'); },
    };
    const CUE = {
      appear: a => noise(a, 1.2, .2, 500, 'bandpass', 2000, .5),
      cut: a => { tone(440, a, .45, 'sawtooth', .18, 60); noise(a + .05, .6, .35, 300, 'bandpass', 4000, .2); },   // 음악이 끊기는 순간: 테이프가 멈추듯 뚝 + 휘익
      card: a => [1047, 1319, 1568].forEach((f, i) => tone(f, a + i * .07, .3, 'triangle', .14)),
      sniff: a => [0, .25].forEach(k => noise(a + k, .14, .25, 1800, 'bandpass', 3500, .03)),
      bite: a => { noise(a, .08, .5, 3000, 'highpass'); noise(a + .12, .07, .4, 2500, 'highpass'); },
      jump: a => tone(300, a, .25, 'square', .12, 900),
      title: a => { tone(70, a, .7, 'sine', .7, 40); noise(a, .5, .5, 800, 'lowpass', 120, .005); [1568, 2093, 2637].forEach((f, i) => tone(f, a + .2 + i * .06, .5, 'triangle', .12)); },
      star: (a, n) => { for (let i = 0; i < n; i++) tone(1047 + i * 262, a + i * .18, .3, 'triangle', .16); },
      reward: a => [784, 988, 1175, 1568].forEach((f, i) => tone(f, a + i * .08, .35, 'triangle', .14)),
      farewell: (a, d) => { const M = [72, 76, 79, 77, 76, 72, 74, 0, 71, 74, 77, 76, 74, 71, 72, 0, 69, 72, 76, 74, 72, 69, 71, 0, 67, 71, 74, 72, 0, 0];   // 마지막 인사: 오르골 가락(직접 만든) — 0.42초 간격
        for (let k = 0, i = 0; k < d; k += .42, i++){ const n = M[i % M.length]; if (n){ tone(440 * Math.pow(2, (n - 57) / 12), a + k, 1.2, 'sine', .14); tone(440 * Math.pow(2, (n - 45) / 12), a + k, .8, 'triangle', .04); } if (i % 4 === 0) tone(440 * Math.pow(2, (48 - 69) / 12), a + k, 1.6, 'sine', .06); } },
      ascend: a => { for (let i = 0; i < 12; i++) tone(1046 * Math.pow(2, i / 12), a + i * .12, .6, 'triangle', .08); noise(a, 2.6, .12, 2000, 'bandpass', 6000, 1.2); },
    };
    return { SC, CUE };
  };
  const now = () => (performance.now() - T0) / 1000;
  return {
    start(){ T0 = performance.now(); log.length = 0; },
    ctx(){ try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); return AC; } catch(e){ return null; } },
    scene(k, dur){ log.push({ t: now(), k, dur, s: 1 }); const C = this.ctx(); if (C) mk(C, C.destination).SC[k]?.(C.currentTime + .02, dur); },
    cue(k, n){ log.push({ t: now(), k, n }); const C = this.ctx(); if (C) mk(C, C.destination).CUE[k]?.(C.currentTime + .02, n); },
    bgm(on){ log.push({ t: now(), k: on ? 'bgm_on' : 'bgm_off' }); },
    log: () => log.slice(),
    async render(total, bgmUrl, onlyBgm){   // 영상용: 같은 합성을 처음부터 다시 그려서 WAV(base64)로
      const R = 44100, C = new OfflineAudioContext(2, Math.ceil(R * total), R), M = C.createGain(); M.gain.value = .9; M.connect(C.destination); const S = mk(C, M);
      if (bgmUrl){ try { const buf = await C.decodeAudioData(await (await fetch(bgmUrl)).arrayBuffer()); const src = C.createBufferSource(); src.buffer = buf; src.loop = true; const gn = C.createGain(); gn.gain.setValueAtTime(.32, 0);
        log.filter(e => e.k === 'bgm_off' || e.k === 'bgm_on').forEach(e => { gn.gain.setValueAtTime(gn.gain.value, e.t); if (e.k === 'bgm_off') gn.gain.linearRampToValueAtTime(.0001, e.t + .4); else { gn.gain.setValueAtTime(.0001, e.t); gn.gain.linearRampToValueAtTime(.32, e.t + 1.6); } });
        src.connect(gn); gn.connect(M); src.start(0); } catch(e){} }
      if (!onlyBgm) log.forEach(e => { if (e.s) S.SC[e.k]?.(e.t + .02, e.dur); else S.CUE[e.k]?.(e.t + .02, e.n); });
      const out = await C.startRendering(), L = out.getChannelData(0), Rr = out.getChannelData(1), n = L.length, b = new DataView(new ArrayBuffer(44 + n * 4));
      const ws = (o, s) => [...s].forEach((c, i) => b.setUint8(o + i, c.charCodeAt(0))); ws(0, 'RIFF'); b.setUint32(4, 36 + n * 4, true); ws(8, 'WAVEfmt '); b.setUint32(16, 16, true); b.setUint16(20, 1, true); b.setUint16(22, 2, true); b.setUint32(24, R, true); b.setUint32(28, R * 4, true); b.setUint16(32, 4, true); b.setUint16(34, 16, true); ws(36, 'data'); b.setUint32(40, n * 4, true);
      for (let i = 0; i < n; i++){ b.setInt16(44 + i * 4, Math.max(-1, Math.min(1, L[i])) * 32767, true); b.setInt16(46 + i * 4, Math.max(-1, Math.min(1, Rr[i])) * 32767, true); }
      let s = ''; const u = new Uint8Array(b.buffer); for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s);
    },
  };
})();
window.__bfSnd = SND;
const REWARD = ['호박 이름표', '사탕 말풍선', '묘비 말풍선', '물약 이름표', '유령 말풍선', '사탕옥수수 이름표', '거미줄 이름표', '해골 이름표', '박쥐 이름표', '마녀 말풍선', '물약 말풍선', '잭오랜턴 말풍선',
  '가구 「블랑의 대솥 조리대」', '가구 「유령 파티 미러볼」', '가구 「백작의 붉은 촛대」', '가구 「사탕 사과 수레」', '옷 「블랑의 요리사 모자」 + 1000 G'];
async function taste(i, first = true){
  const D = R.dishes[i];
  SND.cue('card'); await showCard(`${dishCanvas(i, 96)}${D.name}<small>무슈 블랑에게 건넸어요${D.kind ? ` · ${D.kind} 요리` : ''}</small>`, drawDishes, 1700);
  SND.cue('sniff'); await talk(D.sniff, 1200);
  SND.cue('bite'); await talk(D.bite, 700);
  SND.cue('jump'); clearInterval(bob); for (let k = 0; k < 6; k++){ place(k % 2 ? 0 : 2, 1); await sleep(110); }   // 들썩
  const yellMs = D.long ? 2800 : 2300, titleMs = D.long ? 3000 : 2200, vdur = .5 + D.vision.length * (yellMs + 260) / 1000 + titleMs / 1000 + .3;
  SND.bgm(false); SND.cue('cut'); visionStart(D);   // 환상 동안 배경 음악은 잠깐 꺼요
  if (D.scene === 'montage') MONT.forEach((k, j) => setTimeout(() => SND.scene(k, 1.75), j * 1700)), setTimeout(() => SND.scene(MONT[0], vdur - 10.2), 10200);
  else SND.scene(D.scene, vdur);
  await sleep(500);
  for (const v of D.vision) await yell(v, yellMs);
  title.style.setProperty('--g', D.bg[0]); title.innerHTML = `<small>무슈 블랑의 맛 표현</small><span>「${D.title}」</span>`; title.classList.add('on'); SND.cue('title'); if (D.shake){ shakeK = 2.5; setTimeout(() => shakeK = D.shake ? .6 : 0, 700); }
  await sleep(titleMs); title.classList.remove('on'); await sleep(300); visionStop(); SND.bgm(true); await sleep(600);
  bobOn();
  if (!first) await talk(R.repeat[i % R.repeat.length], 1300);
  for (const a of D.after) await talk(a, 1400);
  SND.cue('star', D.stars); await showCard(`<div class="st">${'★'.repeat(D.stars)}${'☆'.repeat(3 - D.stars)}</div>무슈 블랑의 한 줄 평<small>「${D.review}」</small>`, null, 2400);
  SND.cue('reward'); await showCard(first ? `처음 맛본 요리 보상<div class="st" style="font-size:18px;letter-spacing:0">${REWARD[i]}</div><small>무슈 블랑이 맛본 요리 ${i + 1} / 17</small>` : `다시 가져온 요리<div class="st" style="font-size:20px;letter-spacing:0">${[0, 30, 60, 100][D.stars]} G</div>`, null, 2400);
}
window.__bfGo = async (list = [0]) => {
  await ready; SND.start(); await sleep(1200);
  SND.cue('appear'); for (let k = 1; k <= 10; k++){ place(0, k / 10); await sleep(110); } bobOn();
  await talk('오, 또 왔군. 오늘은 무엇을 가져왔나.', 1200);
  for (const i of list) await taste(i);
  clearInterval(bob); await sleep(800); window.__bfDone = true;
};
// 요리 17가지를 다 맛본 뒤: 잘 먹었다고 인사하고, 빛이 되어 돌아가요 (배경 음악 대신 오르골)
window.__bfFinale = async () => {
  await ready; SND.start(); await sleep(1000);
  SND.cue('appear'); for (let k = 1; k <= 10; k++){ place(0, k / 10); await sleep(110); } bobOn(420);
  SND.cue('reward'); await showCard(`<div class="st" style="font-size:20px;letter-spacing:0">열일곱 가지 모두</div>무슈 블랑이 맛본 요리 17 / 17<small>열두 밤 만찬까지 다 가져다줬어요</small>`, null, 2400);
  SND.bgm(false); SND.cue('farewell', 30);   // 배경 음악은 잠깐 끄고 오르골 (게임에선 BGM.hold('blanc'))
  const L = ['....열일곱 가지. 정말로 다 먹었군.', '백 년 동안 아무 맛도 못 느꼈는데, 그대 덕분에 열일곱 번이나 놀라고, 울고, 춤췄네.', '{player}. 잘 먹었네. 진심으로.', '이제.... 돌아갈 시간이야. 걱정 말게. 슬퍼서 가는 게 아니라, 배가 불러서 가는 거니까.', '식당 문은 열어 두겠네. 내 생각이 나면, 오늘 만든 요리를 누군가에게 대접해 주게.', '그럼 이만. 봉 아페티.......'];
  for (const t of L) await talk(t, 1500);
  clearInterval(bob); World.setProps('candy', [], 'blanc'); SND.cue('ascend');
  visionStart({ scene: 'ascend', bg: ['#FFF6D8', '#3A2A5A'], p: ['sparkle'], m: 'rise', pop: [] }); shakeK = 0; await sleep(1200);
  await yell('잘 먹었네, {player}. 정말로 맛있었어.......', 2600); await yell('봉 아페티.......', 2000);
  await sleep(1000); visionStop(); await sleep(700);
  await showCard(`<canvas width="32" height="32" data-bfdi="16" style="width:72px;height:72px"></canvas>「블랑의 레시피 노트」<small>조리대에 노트 한 권이 남아 있어요<br>펼치면 블랑이 맛본 장면 17개를 다시 볼 수 있어요</small>`, drawDishes, 3200);
  SND.cue('star', 3); await showCard(`무슈 블랑이 편히 돌아갔어요<small>레시피 노트는 아래 메뉴 「일지」에서 언제든 펼칠 수 있어요</small>`, null, 2600);
  SND.bgm(true); await sleep(1500); window.__bfDone = true;
};
window.__bfPeak = async i => {   // 장면 모음용: 환상 + 첫 외침 + 제목을 한 화면에
  await ready; const D = R.dishes[i]; visionStart(D); shakeK = 0; shout.textContent = fill(D.vision[0]); shout.classList.add('on');
  title.style.setProperty('--g', D.bg[0]); title.innerHTML = `<small>${D.name}</small><span>「${D.title}」</span>`; title.classList.add('on'); await sleep(1600); return true;
};
window.__bfClear = () => { shout.classList.remove('on'); title.classList.remove('on'); vis.classList.remove('on'); cancelAnimationFrame(vRaf); };
})();
