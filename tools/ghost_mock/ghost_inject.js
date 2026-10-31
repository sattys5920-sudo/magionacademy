// 시안: 유령 전학생 「마틸다」 1 일째 — 밤 교정에서 수상한 기척(등불 깜빡임 · 뒤따라오는 발자국 · 속삭임) → 돌아보면 코앞에 마틸다 → 첫인사 → 부탁 카드 → 학교를 걸으면 둥실둥실 따라오고, 내 이모티콘을 늦게 따라 해요
//   목업 사이트 폴더에 ghost_lpc.png가 있어야 해요 · window.__ghGo()
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const css = document.createElement('style'); css.textContent = `
#ghsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:320;display:none}
#ghsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid var(--bc,#B8D8FF);border-radius:14px;padding:12px}
#ghsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden}#ghsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}
#ghsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:var(--bc,#CFE6FF);margin-bottom:3px}#ghsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px}
#ghcard{position:fixed;left:50%;top:38%;z-index:340;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 20px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #B8D8FF;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(184,216,255,.5);pointer-events:none;width:min(86vw,320px)}
#ghcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#ghcard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px;text-align:center}
#ghcard ul{list-style:none;margin:0;padding:0;width:100%;display:flex;flex-direction:column;gap:6px}#ghcard li{display:flex;justify-content:space-between;background:#2A2040;border-radius:10px;padding:7px 10px;font-family:var(--f-px);font-size:13px}#ghcard li.ok{color:#9AE07A}
#ghchip{position:fixed;left:50%;top:70px;transform:translateX(-50%);z-index:310;background:rgba(20,13,34,.9);border:2px solid #B8D8FF;border-radius:999px;padding:5px 12px;font-family:var(--f-px);font-size:12px;color:#E8F2FF;display:none}
#ghfog{position:fixed;inset:0;z-index:299;pointer-events:none;background:radial-gradient(circle at 50% 46%,rgba(0,0,0,0) 0,rgba(6,10,26,.55) 38%,rgba(2,4,14,.92) 75%);opacity:0;transition:opacity 2.4s}
#ghfl{position:fixed;inset:0;z-index:330;pointer-events:none;background:#000;opacity:0}#ghwh{position:fixed;inset:0;z-index:331;pointer-events:none;background:#E8F4FF;opacity:0}
#ghws{position:fixed;left:50%;top:40%;z-index:305;transform:translateX(-50%);font-family:var(--f-px);font-size:15px;color:#CFE6FF;letter-spacing:3px;text-shadow:0 0 10px #8FB8FF;opacity:0;transition:opacity 1.2s,transform 3s;pointer-events:none}
#ghbig{position:fixed;left:50%;top:44%;z-index:332;width:300px;height:300px;transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;image-rendering:pixelated;filter:drop-shadow(0 0 18px #9CC8FF) drop-shadow(0 0 40px #6A9AFF)}
#ghdim{position:fixed;inset:0;z-index:300;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(160,200,255,0) 0,rgba(10,14,30,.5) 70%);opacity:0;transition:opacity 1s}`;
document.head.appendChild(css);
const el = (id, h) => { const d = document.createElement('div'); d.id = id; if (h) d.innerHTML = h; document.body.appendChild(d); return d; };
const say = el('ghsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div></div>'), card = el('ghcard'), chip = el('ghchip'), dim = el('ghdim'), fog = el('ghfog'), fl = el('ghfl'), wh = el('ghwh'), ws = el('ghws');
const big = document.createElement('canvas'); big.id = 'ghbig'; big.width = big.height = 40; document.body.appendChild(big); const BGI = new Image(); BGI.onload = () => { const q = big.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(BGI, 12, 0, 40, 40, 0, 0, 40, 40); }; BGI.src = 'ghost_lpc.png';   // 깜짝 놀라는 순간 화면 가득 다가온 얼굴
const LOG = window.__ghLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const flick = async (n = 2) => { for (let i = 0; i < n; i++){ mark('flick'); fl.style.opacity = .85; await sleep(70 + Math.random() * 60); fl.style.opacity = 0; await sleep(90 + Math.random() * 120); } };
const shake = async () => { const st = document.body.style; for (let i = 0; i < 8; i++){ st.transform = `translate(${(i % 2 ? 1 : -1) * (8 - i)}px,${(i % 3 - 1) * (6 - i * .6)}px)`; await sleep(40); } st.transform = ''; };
// 빛나는 발자국 (내 뒤를 따라와요)
const FP = (() => { const c = document.createElement('canvas'); c.width = c.height = 24; const q = c.getContext('2d'); const rg = q.createRadialGradient(12, 14, 1, 12, 14, 10); rg.addColorStop(0, 'rgba(190,225,255,.55)'); rg.addColorStop(1, 'rgba(190,225,255,0)'); q.fillStyle = rg; q.fillRect(0, 0, 24, 24); q.fillStyle = 'rgba(220,240,255,.9)'; q.fillRect(7, 11, 3, 5); q.fillRect(14, 9, 3, 5); return c; })();
let fps = []; const fpPut = () => World.setProps('campus', fps.map(([x, y], i) => ({ id: 'fp' + i, x, y, img: FP, pxc: FP.getContext('2d'), sw: 24, sh: 24, ax: 12, ay: 16, solid: false, light: { r: 12, c: [190, 225, 255], a: .5 } })), 'fp');
const GH = new Image(); GH.src = 'ghost_lpc.png'; const SKL = new Image(); SKL.src = 'skel_lpc.png';
const talk = async (who, t, hold = 1400) => { const q = say.querySelector('canvas').getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32);
  if (who === '마틸다'){ say.style.setProperty('--bc', '#B8D8FF'); q.drawImage(GH, 16, 4, 32, 32, 0, 0, 32, 32); } else { say.style.setProperty('--bc', '#FFE9A0'); q.fillStyle = '#2A2238'; q.fillRect(0, 0, 32, 32); q.drawImage(SKL, 16, 8, 32, 32, 0, 0, 32, 32); }
  say.querySelector('b').textContent = who; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(32); } await sleep(hold); say.style.display = 'none'; await sleep(150); };
const showCard = async (h, ms) => { card.innerHTML = h; card.classList.add('on'); await sleep(ms); card.classList.remove('on'); await sleep(450); };
// 마틸다 그리기 (반 크기 · 둥실) — 맵 소품으로
let gx = 0, gy = 0, gmap = '', ga = 0, gt = 0, gdir = 0;
function ghostImg(){ const c = document.createElement('canvas'); c.width = c.height = 48; const q = c.getContext('2d'); const rg = q.createRadialGradient(24, 26, 2, 24, 26, 22); rg.addColorStop(0, 'rgba(190,225,255,.55)'); rg.addColorStop(1, 'rgba(190,225,255,0)'); q.globalAlpha = ga * (.75 + .25 * Math.sin(gt / 400)); q.fillStyle = rg; q.fillRect(0, 0, 48, 48); q.globalAlpha = Math.min(1, ga * 1.1); q.imageSmoothingQuality = 'high'; q.drawImage(GH, (gdir * 5 + 1 + (Math.floor(gt / 260) % 4)) * 64, 0, 64, 64, 8, 8, 32, 32); return c; }   // 은은한 빛이 감싸서 어두운 곳에서도 보여요
function put(){ if (!gmap) return; const img = ghostImg(); World.setProps(gmap, [{ id: 'nuri', x: Math.round(gx), y: Math.round(gy), img, pxc: img.getContext('2d'), sw: 48, sh: 48, ax: 24 + Math.round((gx - Math.round(gx) - (gy - Math.round(gy))) * 8), ay: 38 + Math.round(Math.sin(gt / 300) * 1.5) - Math.round((gx - Math.round(gx) + gy - Math.round(gy)) * 4), solid: false }], 'nuri'); }   // 칸 사이도 부드럽게 (ax·ay로 남은 만큼 밀어요)
let loop = null; const startLoop = () => { clearInterval(loop); loop = setInterval(() => { gt += 60; put(); }, 60); };
// 따라오기: 내 발자국을 1.4초 늦게 밟아요
let trail = [], follow = false; setInterval(() => { const t = World.meTile && World.meTile(); if (!t) return; trail.push([t.x, t.y, performance.now()]); trail = trail.filter(p => performance.now() - p[2] < 6000);
  if (follow && trail.length){ const old = trail.find(p => performance.now() - p[2] < 1400) || trail[0], tx = old[0] - 1, ty = old[1]; const dx = tx - gx, dy = ty - gy; gdir = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 3 : 2) : (dy < 0 ? 1 : 0); gx += dx * .35; gy += dy * .35; } }, 100);
window.__ghGo = async () => {
  // 어느 날 밤, 혼자 걷는 교정
  await sleep(800); fog.style.opacity = .55; World.walkToTile(44, 44); await sleep(1800);
  await flick(1); await sleep(700);
  World.walkToTile(44, 43); for (const y of [46, 45]){ await sleep(650); mark('step'); fps.push([44, y]); fpPut(); } await sleep(500);
  World.say('me', '....?'); await sleep(1300);
  World.faceTo(44, 47); mark('look'); fog.style.opacity = .75; await sleep(1700);   // 돌아봐도 아무도 없어요
  for (const y of [44]){ mark('step'); fps.push([44, y]); fpPut(); await sleep(600); }   // 발자국만 한 칸씩 가까이
  World.say('me', '.......'); await sleep(1400);
  fps = []; fpPut(); await flick(3); fog.style.opacity = .9;
  World.walkToTile(43, 41); await sleep(2200);
  ws.textContent = '....안녕.'; mark('whisper'); ws.style.opacity = .85; ws.style.transform = 'translateX(-50%) translateY(-14px)'; await sleep(1800); ws.style.opacity = 0; await sleep(900);
  World.say('me', '누, 누구야.......'); await sleep(1600);
  mark('heart'); await sleep(1600);
  // 천천히 돌아보면.... 코앞에
  gmap = 'campus'; gx = 43; gy = 42; ga = .95; gdir = 1; startLoop();
  World.faceTo(43, 44); mark('scare'); wh.style.transition = 'none'; wh.style.opacity = .9; big.style.transition = 'none'; big.style.opacity = 1; big.style.transform = 'translate(-50%,-50%) scale(1.15)'; shake(); World.say('me', '!'); await sleep(90); wh.style.transition = 'opacity .7s'; wh.style.opacity = 0;
  await sleep(520); big.style.transition = 'opacity .5s, transform .5s'; big.style.opacity = 0; big.style.transform = 'translate(-50%,-50%) scale(.6)';
  fog.style.transition = 'opacity 1.2s'; fog.style.opacity = .35; await sleep(1300);
  mark('reveal'); dim.style.opacity = 1;
  await talk('마틸다', '앗, 놀랐어? 미안, 미안. 말 걸 타이밍을 계속 보고 있었어.', 1300);
  await talk('마틸다', '나는 마틸다야. 1926 년에 입학했어. ....졸업은 못 했지만.', 1400);
  await talk('마틸다', '근데 너, 나 보이지? 100 년 만이야. 나 보이는 사람.', 1500);
  for (let k = 0; k <= 10; k++){ gx += (42 - gx) * .25; gy += (41 - gy) * .25; await sleep(90); } gdir = 0;
  await talk('마틸다', '그래서 말인데.... 부탁 하나만 들어줄래? 학교가 너무 바뀌어서 길을 모르겠어.', 1600);
  await showCard(`마틸다의 부탁 · 1 일째<small>「수상한 기척」 · 학교 구경시켜 주기</small><ul><li>본관<span>☐</span></li><li>북쪽 연못<span>☐</span></li><li>시계탑<span>☐</span></li></ul>`, 3000); mark('card');
  dim.style.opacity = 0; fog.style.opacity = 0;
  // 학교 밖: 따라다니기
  trail = []; follow = true; chip.style.display = 'block'; chip.textContent = '마틸다의 부탁 0 / 3 · 본관 · 북쪽 연못 · 시계탑';
  await talk('마틸다', '와, 계단이 아직도 삐걱거리네. 반가워라.', 1200);
  chip.textContent = '마틸다의 부탁 1 / 3 · ✔ 본관 · 북쪽 연못 · 시계탑';
  World.walkToTile(50, 30); await sleep(3500);
  World.say('me', '♪'); await sleep(2000);
  await talk('마틸다', '(따라서) ♪ ....따라 하는 거 재밌다.', 1100);
  World.walkToTile(55, 22); await sleep(4200);
  await talk('마틸다', '이 길, 옛날엔 흙길이었어. 비 오면 장화가 쑥 빠졌지.', 1400);
  World.walkToTile(56, 19); await sleep(2500);
  chip.textContent = '마틸다의 부탁 2 / 3 · ✔ 본관 · ✔ 북쪽 연못 · 시계탑';
  await talk('마틸다', '여기서 개구리 잡다가 선생님께 혼났어. 100 년 전에.', 1600);
  await sleep(1200); follow = false; window.__ghDone = true;
};
})();
