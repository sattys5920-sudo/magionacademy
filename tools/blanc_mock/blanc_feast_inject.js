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
#bfshout{position:fixed;left:14px;right:14px;top:15%;z-index:335;text-align:center;font-family:var(--f-pxb);font-size:19px;line-height:28px;color:#FFFFFF;pointer-events:none;
  text-shadow:-2px 0 #1A0A24,2px 0 #1A0A24,0 -2px #1A0A24,0 2px #1A0A24,0 0 14px rgba(255,240,200,.9);opacity:0;transform:scale(.9);transition:opacity .25s,transform .25s}#bfshout.on{opacity:1;transform:scale(1)}
#bftitle{position:fixed;left:0;right:0;top:62%;z-index:336;text-align:center;font-family:var(--f-pxb);font-size:34px;letter-spacing:2px;color:#FFE9A0;pointer-events:none;opacity:0;transform:scale(2.4);transition:opacity .35s,transform .45s cubic-bezier(.2,1.6,.4,1)}
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
function drawVision(t){
  const D = vD, w = W(), h = H(); if (cv.width !== w * 2){ cv.width = w * 2; cv.height = h * 2; } g.setTransform(2, 0, 0, 2, 0, 0); g.imageSmoothingEnabled = false;
  const sx = shakeK ? (Math.random() - .5) * 6 * shakeK : 0, sy = shakeK ? (Math.random() - .5) * 6 * shakeK : 0; g.translate(sx, sy);
  let [c1, c2] = D.bg; if (D.long){ const hue = (t * 40) % 360; c1 = `hsl(${hue},90%,72%)`; }
  const bg = g.createLinearGradient(0, 0, 0, h); bg.addColorStop(0, c1); bg.addColorStop(1, c2); g.fillStyle = bg; g.fillRect(-10, -10, w + 20, h + 20);
  const cx = w / 2, cy = h * .44;
  // 빛줄기
  g.save(); g.translate(cx, cy); g.rotate(t * .35); for (let i = 0; i < 16; i++){ g.rotate(Math.PI / 8); g.fillStyle = i % 2 ? 'rgba(255,255,255,.10)' : 'rgba(255,240,200,.18)'; g.beginPath(); g.moveTo(0, 0); g.lineTo(-40, -Math.max(w, h)); g.lineTo(40, -Math.max(w, h)); g.fill(); } g.restore();
  // 입자
  parts.forEach((q, i) => { const T = t - q.d; if (T < 0) return; let x, y;
    if (D.m === 'burst'){ const r = (T * 160 * q.sp) % (Math.max(w, h) * .8); x = cx + Math.cos(q.a) * r; y = cy + Math.sin(q.a) * r; }
    else if (D.m === 'rise'){ x = q.x + Math.sin(T * 2 + q.w) * 14; y = h + 30 - ((T * 90 * q.sp + q.y) % (h + 60)); }
    else if (D.m === 'fall'){ x = q.x + Math.sin(T * 1.6 + q.w) * 18; y = -30 + ((T * 80 * q.sp + q.y) % (h + 60)); }
    else if (D.m === 'across'){ x = -40 + ((T * 150 * q.sp + q.x) % (w + 80)); y = q.y * .8 + Math.sin(T * 6 + q.w) * 10; }
    else if (D.m === 'swirl'){ const r = 40 + ((q.r * 4 + T * 30) % (Math.min(w, h) * .55)), a = q.a + T * (1.4 * q.sp); x = cx + Math.cos(a) * r; y = cy + Math.sin(a) * r * .8; }
    else { const r = 70 + q.r * 2.4, a = q.a + T * .8 * q.sp; x = cx + Math.cos(a) * r; y = cy + Math.sin(a) * r * .55 + Math.sin(T * 3 + i) * 6; }
    g.save(); g.translate(x, y); g.scale(q.s, q.s); SPR[q.k](at(-9, -9)); g.restore(); });
  // 가운데 블랑 (크게)
  const sc = 4.2 + Math.sin(t * 3) * .15, bw = 64 * sc;
  g.fillStyle = 'rgba(255,248,220,.35)'; g.beginPath(); g.arc(cx, cy, bw * .42, 0, 7); g.fill();
  g.drawImage(SH, 0, 0, 64, 64, cx - bw / 2, cy - bw * .62, bw, bw);
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
