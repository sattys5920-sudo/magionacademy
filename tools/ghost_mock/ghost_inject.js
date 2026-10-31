// 시안: 유령 전학생 「누리」 1 일째 — 교실에 벽을 뚫고 등장 → 첫인사 → 부탁 카드 → 학교를 걸으면 둥실둥실 따라오고, 내 이모티콘을 늦게 따라 해요
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
#ghdim{position:fixed;inset:0;z-index:300;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(160,200,255,0) 0,rgba(10,14,30,.5) 70%);opacity:0;transition:opacity 1s}`;
document.head.appendChild(css);
const el = (id, h) => { const d = document.createElement('div'); d.id = id; if (h) d.innerHTML = h; document.body.appendChild(d); return d; };
const say = el('ghsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div></div>'), card = el('ghcard'), chip = el('ghchip'), dim = el('ghdim');
const GH = new Image(); GH.src = 'ghost_lpc.png';
const talk = async (who, t, hold = 1400) => { const q = say.querySelector('canvas').getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32);
  if (who === '누리'){ say.style.setProperty('--bc', '#B8D8FF'); q.drawImage(GH, 16, 4, 32, 32, 0, 0, 32, 32); } else { say.style.setProperty('--bc', '#FFE9A0'); q.fillStyle = '#E8E0CC'; q.fillRect(9, 6, 14, 12); q.fillRect(11, 18, 10, 6); q.fillStyle = '#1A1020'; q.fillRect(12, 10, 3, 3); q.fillRect(18, 10, 3, 3); q.fillRect(15, 15, 2, 2); }
  say.querySelector('b').textContent = who; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(32); } await sleep(hold); say.style.display = 'none'; await sleep(150); };
const showCard = async (h, ms) => { card.innerHTML = h; card.classList.add('on'); await sleep(ms); card.classList.remove('on'); await sleep(450); };
// 누리 그리기 (반 크기 · 둥실) — 맵 소품으로
let gx = 0, gy = 0, gmap = '', ga = 0, gt = 0, gdir = 0;
function ghostImg(){ const c = document.createElement('canvas'); c.width = c.height = 48; const q = c.getContext('2d'); const rg = q.createRadialGradient(24, 26, 2, 24, 26, 22); rg.addColorStop(0, 'rgba(190,225,255,.55)'); rg.addColorStop(1, 'rgba(190,225,255,0)'); q.globalAlpha = ga * (.75 + .25 * Math.sin(gt / 400)); q.fillStyle = rg; q.fillRect(0, 0, 48, 48); q.globalAlpha = Math.min(1, ga * 1.1); q.imageSmoothingQuality = 'high'; q.drawImage(GH, (gdir * 5 + 1 + (Math.floor(gt / 260) % 4)) * 64, 0, 64, 64, 8, 8, 32, 32); return c; }   // 은은한 빛이 감싸서 어두운 곳에서도 보여요
function put(){ if (!gmap) return; const img = ghostImg(); World.setProps(gmap, [{ id: 'nuri', x: Math.round(gx), y: Math.round(gy), img, pxc: img.getContext('2d'), sw: 48, sh: 48, ax: 24 + Math.round((gx - Math.round(gx) - (gy - Math.round(gy))) * 8), ay: 38 + Math.round(Math.sin(gt / 300) * 1.5) - Math.round((gx - Math.round(gx) + gy - Math.round(gy)) * 4), solid: false }], 'nuri'); }   // 칸 사이도 부드럽게 (ax·ay로 남은 만큼 밀어요)
let loop = null; const startLoop = () => { clearInterval(loop); loop = setInterval(() => { gt += 60; put(); }, 60); };
// 따라오기: 내 발자국을 1.4초 늦게 밟아요
let trail = [], follow = false; setInterval(() => { const t = World.meTile && World.meTile(); if (!t) return; trail.push([t.x, t.y, performance.now()]); trail = trail.filter(p => performance.now() - p[2] < 6000);
  if (follow && trail.length){ const old = trail.find(p => performance.now() - p[2] < 1400) || trail[0], tx = old[0] - 1, ty = old[1]; const dx = tx - gx, dy = ty - gy; gdir = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 3 : 2) : (dy < 0 ? 1 : 0); gx += dx * .35; gy += dy * .35; } }, 100);
window.__ghGo = async () => {
  await sleep(1000); dim.style.opacity = 1;
  await talk('해골 선생님', '자, 다들 자리에 앉게. 오늘은 전학생을.... 아니, 돌아온 학생을 소개하지.');
  // 벽을 뚫고 스르륵
  gmap = 'classroom'; gx = 22; gy = 3; ga = 0; gdir = 2; startLoop();
  for (let k = 0; k <= 20; k++){ ga = Math.min(.95, k / 14); gx = 22 - k * .3; gy = 3 + k * .35; await sleep(90); } gdir = 0;
  World.say('me', '.......!'); await sleep(1100);
  await talk('누리', '아, 안녕하세요. 저는 누리예요. 1926 년에 입학했어요.');
  await talk('누리', '....그러니까 꽤 오래 다닌 셈이죠. 졸업을 못 해서요.');
  for (let k = 0; k <= 10; k++){ gx += (15 - gx) * .25; gy += (11 - gy) * .25; await sleep(90); }
  await talk('누리', '옆자리 비었어요? 거기 앉아도 돼요? ....아, 저는 의자를 통과하니까 그냥 서 있을게요.', 1600);
  await talk('해골 선생님', '흠흠. 누리는 앞으로 닷새 동안 자네를 따라다닐 걸세. 학교를 잘 보여 주게.', 1500);
  await showCard(`누리의 부탁 · 1 일째<small>「전학생이 왔어요」 · 학교 구경시켜 주기</small><ul><li>본관<span>☐</span></li><li>북쪽 연못<span>☐</span></li><li>시계탑<span>☐</span></li></ul>`, 3000);
  dim.style.opacity = 0;
  // 학교 밖: 따라다니기
  World.setProps('classroom', [], 'nuri'); World.teleport('campus', [44, 38]); await sleep(2200);
  gmap = 'campus'; gx = 43; gy = 38; trail = []; follow = true; chip.style.display = 'block'; chip.textContent = '누리의 부탁 0 / 3 · 본관 · 북쪽 연못 · 시계탑';
  await talk('누리', '와, 계단이 아직도 삐걱거려요. 반가워라.', 1200);
  chip.textContent = '누리의 부탁 1 / 3 · ✔ 본관 · 북쪽 연못 · 시계탑';
  World.walkToTile(50, 30); await sleep(3500);
  World.say('me', '♪'); await sleep(2000);
  await talk('누리', '(따라서) ♪ ....따라 하는 거 재밌어요.', 1100);
  World.walkToTile(55, 22); await sleep(4200);
  await talk('누리', '이 길, 옛날엔 흙길이었어요. 비 오면 장화가 쑥 빠졌어요.', 1400);
  World.walkToTile(56, 19); await sleep(2500);
  chip.textContent = '누리의 부탁 2 / 3 · ✔ 본관 · ✔ 북쪽 연못 · 시계탑';
  await talk('누리', '여기서 개구리 잡다가 선생님께 혼났어요. 100 년 전에요.', 1600);
  await sleep(1200); follow = false; window.__ghDone = true;
};
})();
