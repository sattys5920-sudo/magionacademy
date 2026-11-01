// 시안: 「손님이 찾아오는 정원」 — 내 방 창문 → 창밖 정원에 물건 놓기 → (게임을 끈 사이) 손님이 다녀감: 사진 + 선물 → 지금 와 있는 손님 만나기 → 손님 도감 → 친구 정원의 드문 손님
//   목업 사이트 폴더에 garden_bg.png · garden_items.png · garden_guests.png · garden_gifts.png · window.__gdGo() · window.__gdLog
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__gdLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const img = s => Object.assign(new Image(), { src: s }), BG = img('garden_bg.png'), IT = img('garden_items.png'), GU = img('garden_guests.png'), GF = img('garden_gifts.png');
const ITEMS = { pond: 0, lamp: 1, feeder: 2, swing: 3, pumpkin: 4, bell: 5 }, GUESTS = { frog: 0, bat: 1, squirrel: 2, cat: 3, owl: 4, fox: 5 }, GIFTS = { glow: 0, feather: 1, acorn: 2, bell: 3, quill: 4, moon: 5 };
const NAME = { pond: '작은 연못', lamp: '등불', feeder: '먹이 접시', swing: '그네', pumpkin: '호박 의자', bell: '바람 종' };
const css = document.createElement('style'); css.textContent = `
#gdv{position:fixed;left:50%;top:50%;transform:translate(-50%,-52%) scale(.9);opacity:0;transition:all .45s cubic-bezier(.2,1.3,.4,1);z-index:350;width:min(94vw,380px);background:rgba(20,13,34,.97);border:2px solid #9AE07A;border-radius:16px;padding:10px;box-shadow:0 0 24px rgba(154,224,122,.35);font-family:var(--f-px);color:#F1E9FF}
#gdv.on{opacity:1;transform:translate(-50%,-52%) scale(1)}#gdv .hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}#gdv .hd b{font-family:var(--f-pxb);font-size:16px;color:#CFF5B8}#gdv .hd span{font-size:12px;color:#C8B8E8}
#gdv canvas.g{width:100%;aspect-ratio:160/112;image-rendering:pixelated;border-radius:6px;display:block}
#gdv .tray{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:8px}#gdv .tray div{background:#2A2040;border-radius:10px;padding:4px 0 2px;text-align:center;font-size:10px;color:#D8CCF0;border:2px solid transparent}#gdv .tray div.hit{border-color:#FFE9A0;transform:scale(.92)}#gdv .tray canvas{width:36px;height:36px;image-rendering:pixelated;display:block;margin:0 auto}
#gdv .tip{margin-top:8px;font-size:12px;color:#CFF5B8;min-height:18px;text-align:center}
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
  const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 160, 112); g.drawImage(BG, 0, 0);
  const P = opt.placed || placed, V = opt.visitors || visitors;
  (opt.prints || prints).forEach(([x, y]) => { g.fillStyle = 'rgba(30,20,40,.45)'; g.fillRect(x, y, 2, 1); g.fillRect(x + 3, y - 1, 2, 1); });
  const all = [...P.map(p => ({ ...p, z: p.y, kind: 'item' })), ...V.map(p => ({ ...p, z: p.y + .1, kind: 'guest' }))].sort((a, b) => a.z - b.z);
  all.forEach(o => {
    if (o.kind === 'item'){ const d = drops.find(x => x.k === o.k); let dy = 0; if (d){ const k = Math.min(1, (t - d.t0) / 450); dy = -30 * (1 - k) * (1 - k) + (k >= 1 ? 0 : Math.sin(k * Math.PI) * -2); }
      g.drawImage(IT, ITEMS[o.k] * 24, 0, 24, 24, o.x - 12, o.y - 22 + dy, 24, 24);
      if (o.k === 'lamp' && glow){ const rg = g.createRadialGradient(o.x, o.y - 16, 1, o.x, o.y - 16, 22); rg.addColorStop(0, 'rgba(255,210,120,.35)'); rg.addColorStop(1, 'rgba(255,210,120,0)'); g.fillStyle = rg; g.fillRect(o.x - 22, o.y - 38, 44, 44); } }
    else { const f = Math.floor(t / (o.k === 'bat' ? 180 : 420)) % 2, bob = o.k === 'bat' || o.k === 'cat' || o.k === 'fox' ? Math.round(Math.sin(t / 300) * 1.5) : 0, a = o.a ?? 1;
      g.globalAlpha = a; g.drawImage(GU, GUESTS[o.k] * 48 + f * 24, 0, 24, 24, Math.round(o.x - 12), Math.round(o.y - 22 + bob), 24, 24); g.globalAlpha = 1;
      if (o.k === 'frog' && f){ g.fillStyle = 'rgba(255,240,120,.35)'; g.beginPath(); g.arc(o.x + 6, o.y - 7, 5, 0, 7); g.fill(); }
      if (o.k === 'fox'){ for (let i = 0; i < 4; i++){ g.fillStyle = `rgba(255,246,190,${.4 + .4 * Math.sin(t / 200 + i)})`; g.fillRect(o.x - 14 + Math.sin(t / 400 + i * 2) * 10, o.y - 18 + Math.cos(t / 500 + i) * 6, 1, 1); } } }
  });
  (opt.gifts || gifts).forEach(gg => { g.drawImage(GF, GIFTS[gg.k] * 16, 0, 16, 16, gg.x - 8, gg.y - 12 + Math.round(Math.sin(t / 350) * 1), 16, 16); const s = (Math.sin(t / 180 + gg.x) + 1) / 2; g.fillStyle = `rgba(255,250,210,${.5 + s * .5})`; g.fillRect(gg.x + 5, gg.y - 14, 1, 3); g.fillRect(gg.x + 4, gg.y - 13, 3, 1); });
  // 반딧불 몇 마리 (저녁)
  for (let i = 0; i < 6; i++){ const x = (i * 29 + t / 60) % 160, y = 50 + Math.sin(t / 700 + i * 2) * 14 + i * 6; g.fillStyle = `rgba(230,255,140,${.3 + .5 * Math.abs(Math.sin(t / 300 + i))})`; g.fillRect(Math.round(x), Math.round(y), 1, 1); }
}
function openView(html){ v.innerHTML = `<div class="hd"><b>${title}</b><span>${sub}</span></div><canvas class="g" width="160" height="112"></canvas>${html || ''}`; v.classList.add('on'); const c = v.querySelector('canvas.g');
  cancelAnimationFrame(raf); const loop = now => { drawGarden(c, now); raf = requestAnimationFrame(loop); }; raf = requestAnimationFrame(loop); }
const closeView = async () => { v.classList.remove('on'); await sleep(450); cancelAnimationFrame(raf); };
const tray = () => `<div class="tray">${Object.keys(ITEMS).map(k => `<div data-k="${k}"><canvas width="24" height="24"></canvas>${NAME[k]}</div>`).join('')}</div><div class="tip"></div>`;
const drawTray = () => v.querySelectorAll('.tray div').forEach(d => { const q = d.querySelector('canvas').getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(IT, ITEMS[d.dataset.k] * 24, 0, 24, 24, 0, 0, 24, 24); });
async function place(k, x, y){ const d = v.querySelector(`.tray div[data-k="${k}"]`); d.classList.add('hit'); await sleep(220); d.classList.remove('hit'); placed.push({ k, x, y }); drops.push({ k, t0: performance.now() }); mark('place'); v.querySelector('.tip').textContent = `${NAME[k]}을 놓았어요`; await sleep(900); }
// 폴라로이드 사진: 손님이 다녀간 순간
async function photo(guest, at, giftK, line){ card.innerHTML = `<canvas width="80" height="60"></canvas><b>${line}</b><small>선물을 두고 갔어요</small>`; const c = card.querySelector('canvas'), g = c.getContext('2d'); g.imageSmoothingEnabled = false;
  const tmp = document.createElement('canvas'); tmp.width = 160; tmp.height = 112; drawGarden(tmp, performance.now(), { visitors: [{ k: guest, x: at[0], y: at[1] }], gifts: [], prints: [] });
  g.drawImage(tmp, at[0] - 40, at[1] - 44, 80, 60, 0, 0, 80, 60); g.fillStyle = 'rgba(255,240,200,.12)'; g.fillRect(0, 0, 80, 60);
  card.querySelector('small').innerHTML = `선물: <img style="width:20px;height:20px;image-rendering:pixelated;vertical-align:-5px" src="${(() => { const q = document.createElement('canvas'); q.width = q.height = 16; q.getContext('2d').drawImage(GF, GIFTS[giftK] * 16, 0, 16, 16, 0, 0, 16, 16); return q.toDataURL(); })()}"> ${{ glow: '반딧불 조각', acorn: '반짝 도토리', feather: '박쥐 깃털', moon: '달빛 조각' }[giftK]}`;
  card.classList.add('on'); mark('photo'); await sleep(3000); card.classList.remove('on'); await sleep(500); }
window.__gdGo = async () => {
  // 내 방: 창가로
  await sleep(800); World.say('me', '창밖이 좀 허전한데.......'); await sleep(2000);
  title = '창밖 정원'; sub = '손님 도감 0 / 30'; openView(tray()); drawTray(); mark('open'); await sleep(1400);
  v.querySelector('.tip').textContent = '물건을 놓으면, 내가 없을 때 손님이 놀러 와요'; await sleep(2200);
  await place('pond', 38, 78); await place('lamp', 56, 66); await place('feeder', 108, 84); await place('swing', 124, 62);
  await sleep(800); await closeView();
  // 시간이 흘러 (게임을 끈 사이 · 시계만 빙글)
  night.style.opacity = 1; mark('night'); const nc = night.querySelector('canvas').getContext('2d'); nc.imageSmoothingEnabled = false; const t1 = performance.now();
  await new Promise(r => { const spin = now => { const k = (now - t1) / 2400; nc.clearRect(0, 0, 40, 40); nc.fillStyle = '#FFF3C8'; nc.beginPath(); nc.arc(20, 20, 14, 0, 7); nc.fill(); nc.fillStyle = '#3A2C4A'; nc.beginPath(); nc.arc(20, 20, 12, 0, 7); nc.fill(); nc.strokeStyle = '#FFF3C8'; nc.lineWidth = 2; nc.beginPath(); nc.moveTo(20, 20); nc.lineTo(20 + Math.sin(k * 25) * 9, 20 - Math.cos(k * 25) * 9); nc.moveTo(20, 20); nc.lineTo(20 + Math.sin(k * 2) * 6, 20 - Math.cos(k * 2) * 6); nc.stroke(); if (k < 1) requestAnimationFrame(spin); else r(); }; requestAnimationFrame(spin); });
  night.style.opacity = 0; await sleep(700);
  await toast('정원에 손님이 다녀갔어요 ★ 2');
  prints = [[30, 92], [34, 88], [38, 86], [100, 100], [104, 96], [108, 93]]; gifts = [{ k: 'glow', x: 46, y: 86 }, { k: 'acorn', x: 98, y: 92 }];
  sub = '손님 도감 0 / 30'; openView('<div class="tip">발자국이 남아 있어요. 반짝이는 걸 눌러 볼까요?</div>'); mark('open'); await sleep(2600);
  gifts = gifts.filter(x => x.k !== 'glow'); await photo('frog', [38, 76], 'glow', '반딧불 개구리가 연못에서 놀다 갔어요'); sub = '손님 도감 1 / 30';
  gifts = []; await photo('squirrel', [108, 82], 'acorn', '도토리 다람쥐가 먹이를 먹고 갔어요'); sub = '손님 도감 2 / 30'; prints = [];
  openView('<div class="tip">쉿....... 지금 누가 와 있어요</div>'); await sleep(600);
  // 지금 와 있는 손님: 꼬마 박쥐가 그네에
  visitors = [{ k: 'bat', x: 170, y: 40 }]; mark('fly'); for (let i = 0; i <= 30; i++){ visitors[0].x = 170 - i * 1.53; visitors[0].y = 40 + i * .45; await sleep(40); } await sleep(2400);
  v.querySelector('.tip').textContent = '꼬마 박쥐를 만났어요! 손님 도감 3 / 30'; sub = '손님 도감 3 / 30'; mark('meet'); await sleep(1600);
  for (let i = 0; i <= 25; i++){ visitors[0].x += 2.4; visitors[0].y -= 1.6; await sleep(40); } visitors = []; gifts = [{ k: 'feather', x: 124, y: 62 }]; mark('drop'); await sleep(1600);
  await closeView(); gifts = [];
  // 손님 도감
  const B = [['frog', '반딧불 개구리', '연못 + 등불 · 저녁'], ['squirrel', '도토리 다람쥐', '먹이 접시 · 아침'], ['bat', '꼬마 박쥐', '그네 · 밤']];
  const HINT = ['??? · 비 오는 밤 · 연못 + 바람 종', '??? · 호박 의자 + 등불 · 보름달', '??? · 아주 드문 손님 · 조용한 새벽'];
  book.innerHTML = `<div class="hd"><b>정원 손님 도감</b><span>3 / 30</span></div><div class="gr">${Array.from({ length: 15 }, (_, i) => `<div class="${i < 3 ? 'on' : ''}">${i < 3 ? '<canvas width="24" height="24"></canvas>' : '?'}</div>`).join('')}</div><div class="ht">반딧불 개구리 · 연못 + 등불이 있는 저녁에 와요 · 선물: 반딧불 조각</div>`;
  book.querySelectorAll('.gr canvas').forEach((c, i) => { const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(GU, GUESTS[B[i][0]] * 48, 0, 24, 24, 0, 0, 24, 24); });
  book.classList.add('on'); mark('book'); await sleep(2400);
  const cells = book.querySelectorAll('.gr div'); for (const [i, h] of [[3, HINT[0]], [4, HINT[1]], [5, HINT[2]]]){ cells.forEach(x => x.classList.remove('sel')); cells[i].classList.add('sel'); book.querySelector('.ht').textContent = h; mark('pick'); await sleep(1700); }
  book.classList.remove('on'); await sleep(500);
  // 친구 정원: 드문 손님
  title = '하늘의 정원'; sub = '친구 방 창밖'; placed = [{ k: 'pumpkin', x: 40, y: 80 }, { k: 'lamp', x: 60, y: 70 }, { k: 'bell', x: 118, y: 60 }, { k: 'pond', x: 112, y: 92 }]; drops = []; visitors = [{ k: 'fox', x: 82, y: 84, a: 0 }];
  World.say('me', '하늘이 정원에도 가 볼까?'); await sleep(1600); openView('<div class="tip"></div>'); mark('open'); await sleep(900);
  for (let i = 0; i <= 20; i++){ visitors[0].a = i / 20; await sleep(60); } mark('rare'); v.querySelector('.tip').textContent = '★ 드문 손님 「달빛 여우」가 와 있어요!'; await sleep(3000);
  await closeView(); window.__gdDone = true;
};
})();
