// 시안 2 (쿼터뷰 · 게임 화풍): 「손님이 찾아오는 정원」 — 내 방 창문 → 창밖 정원에 물건 놓기 → (게임을 끈 사이) 손님이 다녀감: 사진 + 선물 → 지금 와 있는 손님 만나기 → 손님 도감 → 친구 정원의 드문 손님
//   목업 사이트 폴더에 gi_bg.png · gi_items.png · gi.json (tools/iso/garden_iso.py) · gi_guests.png (tools/iso/garden_guests.py) · 선물은 art/forage.png · window.__gdGo() · window.__gdLog
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__gdLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const img = s => Object.assign(new Image(), { src: s }), BG = img('gi_bg.png'), IT = img('gi_items.png'), GU = img('gi_guests.png'), GF = img('art/forage.png');
let GI = null; fetch('gi.json').then(r => r.json()).then(j => { GI = j; });   // 쿼터뷰 마당 (방 가구와 같은 도구 · 같은 화풍)
const CW = 144, CH = 88, CY = 8, PP = (tx, ty) => [GI.OX + (tx - ty) * 8, GI.OY + (tx + ty) * 4 - CY];
const ITEMS = { pond: 0, lamp: 1, feeder: 2, swing: 3, pumpkin: 4, bell: 5 }, GUESTS = { snail: 0, shroom: 1, fluff: 2, moth: 3, mole: 4, jelly: 5 }, GIFTS = { shiny: 38, acorn: 0, glow: 24, star: 46 };   // 손님 = gi_guests.png (정원 전용 · 2 칸씩) · 선물 = art/forage.png 칸
const NAME = { pond: '작은 연못', lamp: '등불', feeder: '먹이 접시', swing: '그네', pumpkin: '호박 의자', bell: '바람 종' };
const css = document.createElement('style'); css.textContent = `
#gdv{position:fixed;left:50%;top:50%;transform:translate(-50%,-52%) scale(.9);opacity:0;transition:all .45s cubic-bezier(.2,1.3,.4,1);z-index:350;width:min(94vw,380px);background:rgba(20,13,34,.97);border:2px solid #9AE07A;border-radius:16px;padding:10px;box-shadow:0 0 24px rgba(154,224,122,.35);font-family:var(--f-px);color:#F1E9FF}
#gdv.on{opacity:1;transform:translate(-50%,-52%) scale(1)}#gdv .hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}#gdv .hd b{font-family:var(--f-pxb);font-size:16px;color:#CFF5B8}#gdv .hd span{font-size:12px;color:#C8B8E8}
#gdv canvas.g{width:100%;aspect-ratio:144/88;background:#140D1E;image-rendering:pixelated;border-radius:6px;display:block}
#gdv .tray{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:8px}#gdv .tray div{background:#2A2040;border-radius:10px;padding:4px 0 2px;text-align:center;font-size:10px;color:#D8CCF0;border:2px solid transparent}#gdv .tray div.hit{border-color:#FFE9A0;transform:scale(.92)}#gdv .tray canvas{width:36px;height:36px;image-rendering:pixelated;display:block;margin:0 auto}
#gdv .gtip{margin-top:8px;font-size:12px;color:#CFF5B8;min-height:18px;text-align:center}
#gdcard{position:fixed;left:50%;top:44%;z-index:360;transform:translate(-50%,-50%) rotate(-3deg) scale(.5);opacity:0;transition:all .5s cubic-bezier(.2,1.3,.4,1);pointer-events:none;background:#FBF6EA;padding:10px 10px 12px;border:3px solid #3A2C4A;box-shadow:0 6px 0 rgba(0,0,0,.25),0 0 24px rgba(255,240,200,.5);width:min(78vw,280px);text-align:center;font-family:var(--f-px);color:#3A2C4A}
#gdcard.on{opacity:1;transform:translate(-50%,-50%) rotate(-2deg) scale(1)}#gdcard canvas{width:100%;aspect-ratio:4/3;image-rendering:pixelated;border:2px solid #3A2C4A;display:block}#gdcard b{display:block;margin-top:8px;font-family:var(--f-pxb);font-size:15px}#gdcard small{display:block;margin-top:4px;font-size:12px;color:#6A5A80;line-height:18px}
#gdbook{position:fixed;left:50%;top:50%;transform:translate(-50%,-52%) scale(.9);opacity:0;transition:all .45s;z-index:355;width:min(94vw,380px);background:#FBF6EA;border:3px solid #3A2C4A;border-radius:12px;padding:12px;font-family:var(--f-px);color:#3A2C4A;box-shadow:0 0 24px rgba(0,0,0,.4)}#gdbook.on{opacity:1;transform:translate(-50%,-52%) scale(1)}
#gdbook .hd{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}#gdbook .hd b{font-family:var(--f-pxb);font-size:16px}#gdbook .hd span{font-size:12px;color:#6A5A80}
#gdbook .gr{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}#gdbook .gr div{aspect-ratio:1;border-radius:8px;background:#EDE4CE;border:2px solid #D8CCB0;display:flex;align-items:center;justify-content:center;font-family:var(--f-pxb);color:#B8A88A;font-size:18px}#gdbook .gr div.on{background:#E4F2D8;border-color:#9AC87A}#gdbook .gr div.sel{outline:3px solid #E8B84A}#gdbook .gr canvas{width:80%;height:80%;image-rendering:pixelated}
#gdbook .ht{margin-top:10px;background:#3A2C4A;color:#FFF3C8;border-radius:8px;padding:8px 10px;font-size:12px;line-height:18px;min-height:36px}
#gdtoast{position:fixed;left:50%;top:76px;transform:translateX(-50%) translateY(-10px);z-index:365;background:rgba(20,13,34,.95);border:2px solid #9AE07A;border-radius:999px;padding:7px 14px;font-family:var(--f-px);font-size:13px;color:#E8FFD8;opacity:0;transition:all .4s;white-space:nowrap}#gdtoast.on{opacity:1;transform:translateX(-50%) translateY(0)}
#gdnight{position:fixed;inset:0;z-index:370;background:#0A0818;opacity:0;transition:opacity .8s;pointer-events:none;display:flex;align-items:center;justify-content:center}#gdnight canvas{width:120px;height:120px;image-rendering:pixelated}`;
document.head.appendChild(css);
const el = (id, h = '') => { const d = document.createElement('div'); d.id = id; d.innerHTML = h; document.body.appendChild(d); return d; };
const v = el('gdv'), card = el('gdcard'), book = el('gdbook'), tst = el('gdtoast'), night = el('gdnight', '<canvas width="40" height="40"></canvas>');
const toast = async (t, ms = 2400) => { tst.textContent = t; tst.classList.add('on'); mark('toast'); await sleep(ms); tst.classList.remove('on'); await sleep(350); };
// ---------- 정원 그리기 ----------
let placed = [], visitors = [], gifts = [], prints = [], drops = [], raf = 0, title = '창밖 정원', sub = '', glow = true;
function drawGarden(c, t, opt = {}){
  const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, CW, CH); if (!GI) return; g.drawImage(BG, 0, CY, CW, CH, 0, 0, CW, CH);
  const P = opt.placed || placed, V = opt.visitors || visitors;
  (opt.prints || prints).forEach(([tx, ty]) => { const [x, y] = PP(tx, ty); g.fillStyle = 'rgba(40,24,20,.5)'; g.fillRect(x, y, 2, 1); g.fillRect(x + 2, y - 1, 1, 1); });
  const all = [...P.map(p => ({ ...p, z: p.tx + p.ty, kind: 'item' })), ...V.map(p => ({ ...p, z: p.tx + p.ty + .05, kind: 'guest' }))].sort((a, b) => a.z - b.z);
  all.forEach(o => { const [x, y] = PP(o.tx, o.ty);
    if (o.kind === 'item'){ const m = GI.items[o.k], d = drops.find(q => q.k === o.k); let dy = 0; if (d){ const k = Math.min(1, (t - d.t0) / 450); dy = -24 * (1 - k) * (1 - k); }
      g.drawImage(IT, m.sx, 0, m.sw, m.sh, Math.round(x - m.ax), Math.round(y - m.ay + dy), m.sw, m.sh); }
    else { const fl = o.k === 'moth' || o.k === 'jelly' || o.k === 'fluff', bob = Math.round(Math.abs(Math.sin(t / (o.k === 'moth' ? 160 : 420))) * (fl ? 2 : 1)), lift = o.lift || 0, fr = (GUESTS[o.k] * 2 + (Math.floor(t / (o.k === 'moth' ? 150 : 450)) % 2)) * 14; g.globalAlpha = o.a ?? 1;
      g.fillStyle = 'rgba(20,12,24,.35)'; g.beginPath(); g.ellipse(x, y, 5, 2, 0, 0, 7); g.fill();
      if (o.flip){ g.save(); g.translate(Math.round(x), 0); g.scale(-1, 1); g.drawImage(GU, fr, 0, 14, 14, -7, Math.round(y - 13 - bob - lift), 14, 14); g.restore(); }
      else g.drawImage(GU, fr, 0, 14, 14, Math.round(x - 7), Math.round(y - 13 - bob - lift), 14, 14);
      g.globalAlpha = 1;
      if (o.k === 'jelly'){ for (let i = 0; i < 5; i++){ g.fillStyle = `rgba(255,246,190,${.4 + .4 * Math.sin(t / 200 + i)})`; g.fillRect(Math.round(x - 10 + Math.sin(t / 400 + i * 2) * 9), Math.round(y - 14 + Math.cos(t / 500 + i) * 5), 1, 1); } }
      if (o.k === 'moth'){ g.fillStyle = `rgba(255,236,120,${.25 + .2 * Math.sin(t / 200)})`; g.beginPath(); g.arc(x, y - 7 - lift, 8, 0, 7); g.fill(); } } });
  (opt.gifts || gifts).forEach(gg => { const [x, y] = PP(gg.tx, gg.ty); const s = (Math.sin(t / 180 + x) + 1) / 2; g.drawImage(GF, GIFTS[gg.k] * 32, 0, 32, 32, x - 6, y - 12 + Math.round(Math.sin(t / 350)), 12, 12); g.fillStyle = `rgba(255,250,210,${.5 + s * .5})`; g.fillRect(x + 5, y - 14, 1, 3); g.fillRect(x + 4, y - 13, 3, 1); });
  for (let i = 0; i < 6; i++){ const x = (i * 29 + t / 60) % CW, y = 30 + Math.sin(t / 700 + i * 2) * 10 + i * 6; g.fillStyle = `rgba(230,255,140,${.3 + .5 * Math.abs(Math.sin(t / 300 + i))})`; g.fillRect(Math.round(x), Math.round(y), 1, 1); }
}
function openView(html){ v.innerHTML = `<div class="hd"><b>${title}</b><span>${sub}</span></div><canvas class="g" width="144" height="88"></canvas>${html || ''}`; v.classList.add('on'); const c = v.querySelector('canvas.g');
  cancelAnimationFrame(raf); const loop = now => { drawGarden(c, now); raf = requestAnimationFrame(loop); }; raf = requestAnimationFrame(loop); }
const closeView = async () => { v.classList.remove('on'); await sleep(450); cancelAnimationFrame(raf); };
const tray = () => `<div class="tray">${Object.keys(ITEMS).map(k => `<div data-k="${k}"><canvas width="24" height="24"></canvas>${NAME[k]}</div>`).join('')}</div><div class="gtip"></div>`;
const drawTray = () => v.querySelectorAll('.tray div').forEach(d => { const c = d.querySelector('canvas'), q = c.getContext('2d'), m = GI.items[d.dataset.k]; c.width = c.height = 48; q.imageSmoothingEnabled = false;
  const t = document.createElement('canvas'); t.width = m.sw; t.height = m.sh; const tq = t.getContext('2d'); tq.drawImage(IT, m.sx, 0, m.sw, m.sh, 0, 0, m.sw, m.sh); const px = tq.getImageData(0, 0, m.sw, m.sh).data; let x0 = m.sw, y0 = m.sh, x1 = 0, y1 = 0;
  for (let y = 0; y < m.sh; y++) for (let x = 0; x < m.sw; x++) if (px[(y * m.sw + x) * 4 + 3] > 20){ x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
  const w = x1 - x0 + 1, h = y1 - y0 + 1; c.width = w; c.height = h; q.imageSmoothingEnabled = false; q.drawImage(t, x0, y0, w, h, 0, 0, w, h); c.style.height = '40px'; c.style.width = Math.round(40 * w / h) + 'px'; });   // 물건 그림을 칸에 꽉 차게
async function place(k, tx, ty){ const d = v.querySelector(`.tray div[data-k="${k}"]`); d.classList.add('hit'); await sleep(220); d.classList.remove('hit'); placed.push({ k, tx, ty }); drops.push({ k, t0: performance.now() }); mark('place'); v.querySelector('.gtip').textContent = `${NAME[k]}을 놓았어요`; await sleep(900); }
// 폴라로이드 사진: 손님이 다녀간 순간
async function photo(guest, at, giftK, line){ card.innerHTML = `<canvas width="80" height="60"></canvas><b>${line}</b><small></small>`; const c = card.querySelector('canvas'), g = c.getContext('2d'); g.imageSmoothingEnabled = false;
  const tmp = document.createElement('canvas'); tmp.width = CW; tmp.height = CH; drawGarden(tmp, performance.now(), { visitors: [{ k: guest, tx: at[0], ty: at[1] }], gifts: [], prints: [] }); const [x, y] = PP(at[0], at[1]);
  g.drawImage(tmp, Math.max(0, Math.min(CW - 60, x - 30)), Math.max(0, Math.min(CH - 45, y - 30)), 60, 45, 0, 0, 80, 60); g.fillStyle = 'rgba(255,240,200,.12)'; g.fillRect(0, 0, 80, 60);
  const q = document.createElement('canvas'); q.width = q.height = 32; q.getContext('2d').drawImage(GF, GIFTS[giftK] * 32, 0, 32, 32, 0, 0, 32, 32);
  card.querySelector('small').innerHTML = `선물: <img style="width:22px;height:22px;image-rendering:pixelated;vertical-align:-6px" src="${q.toDataURL()}"> ${{ glow: '반딧불이', acorn: '도토리', shiny: '반짝 돌', star: '별똥별 조각' }[giftK]}`;
  card.classList.add('on'); mark('photo'); await sleep(3000); card.classList.remove('on'); await sleep(500); }
window.__gdGo = async () => {
  // 내 방: 창가로
  await sleep(800); World.say('me', '창밖이 좀 허전한데.......'); await sleep(2000);
  title = '창밖 정원'; sub = '손님 도감 0 / 30'; openView(tray()); drawTray(); mark('open'); await sleep(1400);
  v.querySelector('.gtip').textContent = '물건을 놓으면, 내가 없을 때 손님이 놀러 와요'; await sleep(2200);
  await place('pond', 1.6, 3.6); await place('lamp', 1, 1.6); await place('feeder', 5, 4.6); await place('swing', 5.2, 1);
  await sleep(800); await closeView();
  // 시간이 흘러 (게임을 끈 사이 · 시계만 빙글)
  night.style.opacity = 1; mark('night'); const nc = night.querySelector('canvas').getContext('2d'); nc.imageSmoothingEnabled = false; const t1 = performance.now();
  await new Promise(r => { const spin = now => { const k = (now - t1) / 2400; nc.clearRect(0, 0, 40, 40); nc.fillStyle = '#FFF3C8'; nc.beginPath(); nc.arc(20, 20, 14, 0, 7); nc.fill(); nc.fillStyle = '#3A2C4A'; nc.beginPath(); nc.arc(20, 20, 12, 0, 7); nc.fill(); nc.strokeStyle = '#FFF3C8'; nc.lineWidth = 2; nc.beginPath(); nc.moveTo(20, 20); nc.lineTo(20 + Math.sin(k * 25) * 9, 20 - Math.cos(k * 25) * 9); nc.moveTo(20, 20); nc.lineTo(20 + Math.sin(k * 2) * 6, 20 - Math.cos(k * 2) * 6); nc.stroke(); if (k < 1) requestAnimationFrame(spin); else r(); }; requestAnimationFrame(spin); });
  night.style.opacity = 0; await sleep(700);
  await toast('정원에 손님이 다녀갔어요 ★ 2');
  prints = [[0.4, 4.2], [0.9, 4], [1.4, 4.2], [4.6, 5.6], [4.9, 5.2], [5.2, 5.5]]; gifts = [{ k: 'shiny', tx: 2.6, ty: 4 }, { k: 'acorn', tx: 4.2, ty: 5.2 }];
  sub = '손님 도감 0 / 30'; openView('<div class="gtip">발자국이 남아 있어요. 반짝이는 걸 눌러 볼까요?</div>'); mark('open'); await sleep(2600);
  gifts = gifts.filter(x => x.k !== 'shiny'); await photo('snail', [2.3, 3.9], 'shiny', '이끼 달팽이가 연못가에서 쉬다 갔어요'); sub = '손님 도감 1 / 30';
  gifts = []; await photo('mole', [4.3, 5], 'acorn', '꼬마 두더지가 먹이를 먹고 갔어요'); sub = '손님 도감 2 / 30'; prints = [];
  openView('<div class="gtip">쉿....... 지금 누가 와 있어요</div>'); await sleep(600);
  // 지금 와 있는 손님: 꼬마 박쥐가 그네에
  visitors = [{ k: 'moth', tx: -2, ty: 0, lift: 30 }]; mark('fly'); for (let i = 0; i <= 30; i++){ visitors[0].tx = -2 + i * .12; visitors[0].ty = 0 + i * .073; visitors[0].lift = 30 - i * .6; await sleep(40); } await sleep(2400);
  v.querySelector('.gtip').textContent = '반딧불 나방을 만났어요! 손님 도감 3 / 30'; sub = '손님 도감 3 / 30'; mark('meet'); await sleep(1600);
  for (let i = 0; i <= 25; i++){ visitors[0].tx += .14; visitors[0].ty -= .08; visitors[0].lift += 1.2; await sleep(40); } visitors = []; gifts = [{ k: 'glow', tx: 1.4, ty: 2 }]; mark('drop'); await sleep(1600);
  await closeView(); gifts = [];
  // 손님 도감
  const B = [['snail', '이끼 달팽이', '연못 · 비 온 뒤'], ['mole', '꼬마 두더지', '먹이 그루터기 · 아침'], ['moth', '반딧불 나방', '등불 · 밤']];
  const HINT = ['??? · 바람 부는 날 · 바람 종 + 그네', '??? · 호박 의자 · 안개 낀 아침', '??? · 아주 드문 손님 · 보름달 밤의 연못'];
  book.innerHTML = `<div class="hd"><b>정원 손님 도감</b><span>3 / 30</span></div><div class="gr">${Array.from({ length: 15 }, (_, i) => `<div class="${i < 3 ? 'on' : ''}">${i < 3 ? '<canvas width="24" height="24"></canvas>' : '?'}</div>`).join('')}</div><div class="ht">이끼 달팽이 · 비 온 뒤 연못가에 와요 · 선물: 반짝 돌</div>`;
  book.querySelectorAll('.gr canvas').forEach((c, i) => { const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(GU, GUESTS[B[i][0]] * 28, 0, 14, 14, 5, 5, 14, 14); });
  book.classList.add('on'); mark('book'); await sleep(2400);
  const cells = book.querySelectorAll('.gr div'); for (const [i, h] of [[3, HINT[0]], [4, HINT[1]], [5, HINT[2]]]){ cells.forEach(x => x.classList.remove('sel')); cells[i].classList.add('sel'); book.querySelector('.ht').textContent = h; mark('pick'); await sleep(1700); }
  book.classList.remove('on'); await sleep(500);
  // 친구 정원: 드문 손님
  title = '하늘의 정원'; sub = '친구 방 창밖'; placed = [{ k: 'pumpkin', tx: 1.4, ty: 4.6 }, { k: 'lamp', tx: 1, ty: 1.4 }, { k: 'bell', tx: 5.8, ty: 2.2 }, { k: 'pond', tx: 4.4, ty: 4.4 }]; drops = []; visitors = [{ k: 'jelly', tx: 4.4, ty: 4.2, a: 0, lift: 8 }];
  World.say('me', '하늘이 정원에도 가 볼까?'); await sleep(1600); openView('<div class="gtip"></div>'); mark('open'); await sleep(900);
  for (let i = 0; i <= 20; i++){ visitors[0].a = i / 20; await sleep(60); } mark('rare'); v.querySelector('.gtip').textContent = '★ 드문 손님 「달빛 해파리」가 연못 위에 떠 있어요!'; await sleep(3000);
  await closeView(); window.__gdDone = true;
};
})();
