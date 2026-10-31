// 시안: 마틸다 졸업식 (5 일째) — 단상 · 개근상 · 추억 조각 4 장 · 「졸업 축하해」 선택 · 아껴 둔 비밀 인사 · 빛이 되어 떠남 · 졸업 모자 · 보상
//   목업 사이트 폴더에 ghost_lpc.png · ghost_photo.png · ghost_buttons.png · hat_grad.png · diploma.png · skel_lpc.png · mem0~3.png가 있어야 해요 · window.__grGo()
//   예시 선택: 부르는 이름 「틸다」 · 비밀 인사 하이파이브 · 바다 약속 함께 가기 · 단추 같이 찾기 · 무서운 것 나눔
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__ghLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const css = document.createElement('style'); css.textContent = `
#grsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:350;display:none}
#grsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid var(--bc,#B8D8FF);border-radius:14px;padding:12px}
#grsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden}#grsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}
#grsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:var(--bc,#CFE6FF);margin-bottom:3px}#grsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px}
#grcard{position:fixed;left:50%;top:40%;z-index:360;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .6s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 18px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #E8D8A0;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(232,216,160,.45);pointer-events:none;width:min(88vw,330px);text-align:center}
#grcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#grcard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}#grcard canvas,#grcard img{image-rendering:pixelated}
#grttl{position:fixed;left:0;right:0;top:20%;z-index:355;text-align:center;font-family:var(--f-pxb);color:#FFE9A0;font-size:24px;text-shadow:0 0 14px #E8B84A,0 2px 0 #2A1440;opacity:0;transition:opacity .9s;pointer-events:none}#grttl small{display:block;font-family:var(--f-px);font-size:13px;color:#E8DCFF;margin-top:6px;text-shadow:none}#grttl.on{opacity:1}
#grpick{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:352;display:none;flex-direction:column;gap:8px;max-width:560px;margin:0 auto}#grpick button{min-height:46px;border-radius:12px;border:2px solid #B8D8FF;background:rgba(30,22,52,.97);color:#F1E9FF;font-family:var(--f-px);font-size:14px}#grpick button.on{background:#B8D8FF;color:#1A1030}
#grdim{position:fixed;inset:0;z-index:300;pointer-events:none;background:radial-gradient(circle at 50% 42%,rgba(255,240,200,0) 0,rgba(10,10,28,.62) 75%);opacity:0;transition:opacity 1.2s}
#grfx{position:fixed;inset:0;width:100vw;height:100vh;z-index:340;pointer-events:none;image-rendering:pixelated;opacity:0;transition:opacity .8s}#grfx.on{opacity:1}
#grpop{position:fixed;left:50%;top:44%;transform:translate(-50%,-50%) scale(.4);z-index:358;font-family:var(--f-pxb);font-size:42px;color:#FFFFFF;text-shadow:0 0 18px #B8D8FF,0 0 36px #B8D8FF,-3px 0 #2A1A4A,3px 0 #2A1A4A,0 3px #2A1A4A;opacity:0;transition:all .35s cubic-bezier(.2,1.6,.4,1);pointer-events:none}#grpop.on{opacity:1;transform:translate(-50%,-50%) scale(1)}`;
document.head.appendChild(css);
const el = (id, h, tag = 'div') => { const d = document.createElement(tag); d.id = id; if (h) d.innerHTML = h; document.body.appendChild(d); return d; };
const say = el('grsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div></div>'), card = el('grcard'), ttl = el('grttl'), pick = el('grpick'), dim = el('grdim'), pop = el('grpop'), fx = el('grfx', '', 'canvas');
const GH = new Image(); GH.src = 'ghost_lpc.png'; const PH = new Image(); PH.src = 'ghost_photo.png'; const BT = new Image(); BT.src = 'ghost_buttons.png'; const CAP = new Image(); CAP.src = 'hat_grad.png'; const SK = new Image(); SK.src = 'skel_lpc.png'; const MEM = [0, 1, 2, 3].map(i => { const m = new Image(); m.src = `mem${i}.png`; return m; });
const face = (q, who) => { q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32); if (who === '마틸다'){ q.drawImage(GH, 16, 4, 32, 32, 0, 0, 32, 32); } else { q.fillStyle = '#2A2238'; q.fillRect(0, 0, 32, 32); q.drawImage(SK, 16, 8, 32, 32, 0, 0, 32, 32); } };
const talk = async (who, t, hold = 1500) => { const q = say.querySelector('canvas').getContext('2d'); face(q, who); say.style.setProperty('--bc', who === '마틸다' ? '#B8D8FF' : '#FFE9A0');
  say.querySelector('b').textContent = who; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; mark('say'); for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(34); } await sleep(hold); say.style.display = 'none'; await sleep(160); };
const showCard = async (h, draw, ms) => { card.innerHTML = h; draw && draw(); card.classList.add('on'); mark('card'); await sleep(ms); card.classList.remove('on'); await sleep(500); };
// 마틸다 · 다른 학생들의 마틸다(흐릿하게) · 블랑 — 맵 소품
let gt = 0, ga = 1, gy = 0, gmap = 'campus', ghostOn = true; const SPOT = [43, 40];
const gImg = (a, glowK = 1) => { const c = document.createElement('canvas'); c.width = c.height = 48; const q = c.getContext('2d'); const rg = q.createRadialGradient(24, 26, 2, 24, 26, 22); rg.addColorStop(0, `rgba(200,230,255,${.55 * glowK})`); rg.addColorStop(1, 'rgba(200,230,255,0)'); q.globalAlpha = a; q.fillStyle = rg; q.fillRect(0, 0, 48, 48); q.imageSmoothingQuality = 'high'; q.drawImage(GH, (1 + (Math.floor(gt / 280) % 4)) * 64, 0, 64, 64, 8, 8, 32, 32); q.globalCompositeOperation = 'lighter'; q.globalAlpha = a * .35; q.drawImage(GH, (1 + (Math.floor(gt / 280) % 4)) * 64, 0, 64, 64, 8, 8, 32, 32); return c; };   // 한 번 더 밝게 겹쳐 밤에도 보여요
function put(){ const list = []; if (ghostOn){ const im = gImg(ga); list.push({ id: 'tilda', x: SPOT[0], y: SPOT[1], img: im, pxc: im.getContext('2d'), sw: 48, sh: 48, ax: 24, ay: 38 + Math.round(Math.sin(gt / 300) * 1.5) + gy, solid: false, light: { r: 34, c: [190, 225, 255], a: .75 } }); }
  [[40, 42], [42, 44], [45, 43], [47, 42], [38, 41]].forEach(([x, y], i) => { const im = gImg(.35, .5); list.push({ id: 'g' + i, x, y, img: im, pxc: im.getContext('2d'), sw: 48, sh: 48, ax: 24, ay: 38 + Math.round(Math.sin(gt / 300 + i) * 1.5), solid: false, light: { r: 22, c: [190, 225, 255], a: .4 } }); });
  if (SK.complete && SK.naturalWidth){ const t = document.createElement('canvas'); t.width = t.height = 48; const tq = t.getContext('2d'); tq.imageSmoothingQuality = 'high'; tq.drawImage(SK, 0, 0, 64, 64, 8, 8, 32, 32); list.push({ id: 'skel', x: SPOT[0] + 2, y: SPOT[1] - 1, img: t, pxc: tq, sw: 48, sh: 48, ax: 24, ay: 40, solid: false, light: { r: 20, c: [255, 230, 190], a: .45 } }); }
  World.setProps(gmap, list, 'tilda'); }
const loop = setInterval(() => { gt += 70; put(); }, 70); window.__grImg = gImg; window.__grDbg = () => { const c = gImg(1); const d = c.getContext('2d').getImageData(0, 0, 48, 48).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 20) n++; return [n, GH.complete, GH.naturalWidth]; };
// 추억 조각: 그날 실제 게임 화면을 찍어 둔 사진 (내 아바타 그대로 · mem_shots.js) + 별똥별은 위에 그려요
function memo(i){ const c = document.createElement('canvas'); c.width = 480; c.height = 320; const g = c.getContext('2d'); g.drawImage(MEM[i], 0, 0, 480, 320);
  if (i === 3){ const gr = g.createLinearGradient(400, 20, 300, 90); gr.addColorStop(0, 'rgba(255,255,240,1)'); gr.addColorStop(1, 'rgba(255,246,200,0)'); g.strokeStyle = gr; g.lineWidth = 4; g.beginPath(); g.moveTo(400, 20); g.lineTo(300, 90); g.stroke(); g.fillStyle = '#FFFFFF'; g.fillRect(396, 16, 8, 8); }
  const v = g.createRadialGradient(240, 160, 120, 240, 160, 300); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(30,18,10,.55)'); g.fillStyle = v; g.fillRect(0, 0, 480, 320);
  return c; }
async function memCard(i, line){ card.innerHTML = `<canvas id="grm" width="480" height="320" style="width:288px;height:192px;border-radius:4px;border:6px solid #F4ECDC;box-shadow:0 2px 0 #B8A88A;filter:sepia(.45) saturate(.85)"></canvas><small>추억 조각 ${i + 1} / 4</small>`; card.querySelector('#grm').getContext('2d').drawImage(memo(i), 0, 0); card.classList.add('on'); mark('memo'); await sleep(900); await talk('마틸다', line, 1500); card.classList.remove('on'); await sleep(500); }
// 빛이 되어 떠나는 장면 (화면 전체 · 1/3 크기로 그려 픽셀 확대)
let fxRaf = 0, fxT0 = 0, capY = null;
function drawFx(now){ const t = (now - fxT0) / 1000, w = innerWidth, h = innerHeight, L = 3; fx.width = Math.ceil(w / L); fx.height = Math.ceil(h / L); fx.style.width = w + 'px'; fx.style.height = h + 'px'; const g = fx.getContext('2d'); g.imageSmoothingEnabled = false;
  const W = fx.width, H = fx.height; for (let i = 0; i < 8; i++){ g.fillStyle = `rgb(${18 + i * 8},${14 + i * 6},${42 + i * 7})`; g.fillRect(0, i * H / 8, W, H / 8 + 1); }
  for (let i = 0; i < 40; i++){ g.fillStyle = `rgba(255,246,200,${.3 + .5 * Math.abs(Math.sin(t * 2 + i))})`; g.fillRect((i * 37) % W, (i * 23) % (H * .6), 1, 1); }
  const cx = W / 2, pw = 26 + Math.sin(t * 2) * 2; g.fillStyle = 'rgba(255,240,190,.16)'; g.fillRect(cx - pw, 0, pw * 2, H); g.fillStyle = 'rgba(255,248,220,.26)'; g.fillRect(cx - pw * .5, 0, pw, H); g.fillStyle = 'rgba(255,255,240,.34)'; g.fillRect(cx - pw * .18, 0, pw * .36, H);
  // 시계탑 (위쪽)
  g.fillStyle = '#3A2E5A'; g.fillRect(cx - 12, 8, 24, 60); g.fillStyle = '#2A1E44'; g.fillRect(cx - 15, 4, 30, 6); g.fillStyle = '#E8D8A0'; g.beginPath(); g.arc(cx, 26, 8, 0, 7); g.fill(); const ang = t > 4.2 ? (t - 4.2) * 1.4 : 0; g.strokeStyle = '#3A2A1A'; g.beginPath(); g.moveTo(cx, 26); g.lineTo(cx + Math.sin(ang) * 6, 26 - Math.cos(ang) * 6); g.moveTo(cx, 26); g.lineTo(cx + 4, 26); g.stroke();
  for (let i = 0; i < 26; i++){ const y = H - ((t * 26 + i * 19) % (H + 20)), x = cx + Math.sin(t * 2 + i) * pw * .9; g.fillStyle = '#FFF6C8'; g.fillRect(x, y, 1, 1); if (i % 4 === 0){ g.fillRect(x - 1, y, 3, 1); g.fillRect(x, y - 1, 1, 3); } }
  const gy0 = H * .74 - Math.max(0, t - .8) * 18, ga0 = Math.max(0, Math.min(1, 1 - (t - 3.4) / 1.4)); g.globalAlpha = ga0; const rg = g.createRadialGradient(cx, gy0 - 14, 1, cx, gy0 - 14, 18); rg.addColorStop(0, 'rgba(200,230,255,.7)'); rg.addColorStop(1, 'rgba(200,230,255,0)'); g.fillStyle = rg; g.fillRect(cx - 20, gy0 - 34, 40, 40);
  const fr = t > 2 && t < 2.9 ? 5 : 0; g.drawImage(GH, (fr + 1 + Math.floor(t * 4) % 4) * 64, 0, 64, 64, cx - 16, gy0 - 32, 32, 32); g.globalAlpha = 1;   // 날아가다 한 번 뒤돌아봐요
  if (t > 2 && t < 2.9){ g.fillStyle = '#C8D8E8'; g.fillRect(cx + 9, gy0 - 22 - Math.round(Math.sin(t * 20) * 2), 2, 4); }   // 손 흔들기
  if (capY !== null){ const cy = Math.min(H * .82, capY + (t - 5) * 14), sway = Math.sin(t * 3) * 6; g.fillStyle = '#2A2438'; g.fillRect(cx - 6 + sway, cy, 12, 2); g.fillRect(cx - 3 + sway, cy + 2, 6, 3); g.fillStyle = '#E0B03A'; g.fillRect(cx + 5 + sway, cy + 1, 1, 4); }
  fxRaf = requestAnimationFrame(drawFx); }
window.__grGo = async () => {
  await sleep(800); dim.style.opacity = 1; ttl.innerHTML = '졸업식<small>1926 년 입학생 · 마틸다</small>'; ttl.classList.add('on'); mark('open'); await sleep(2600); ttl.classList.remove('on'); await sleep(600);
  await talk('해골 선생님', '지금부터 1926 년 입학생, 마틸다의 졸업식을 시작하겠네.');
  await talk('해골 선생님', '마틸다. 100 년 동안 결석 없이 학교를 지켰으니.... 개근상도 같이 주지.');
  await talk('마틸다', '개, 개근상이요? ....푸하하. 경을 칠 노릇이네!', 900); World.say('me', '노릇이네!'); mark('quip'); await sleep(1500);
  await showCard(`<img src="diploma.png" style="width:240px;height:168px;image-rendering:pixelated;filter:drop-shadow(0 0 10px rgba(232,216,160,.5))">졸업장<small>「위 학생은 호박달 마녀학교의 모든 과정을 마치고<br>100 년 개근하였기에 이 졸업장을 줍니다.」</small>`, null, 2600);
  await talk('마틸다', '(손이 졸업장을 통과한다) ....앗.', 600); await talk('해골 선생님', '쯧, 내가 들고 있지.', 900);
  ttl.innerHTML = '추억 되돌아보기'; ttl.classList.add('on'); await sleep(1400); ttl.classList.remove('on');
  await memCard(0, '시계탑에서 틸다라고 처음 불러 줬던 날.');
  await memCard(1, '냄새만 맡았는데 제일 맛있었던 저녁.');
  await memCard(2, '무거운 얘기 해도 안 도망갔던 밤.');
  await memCard(3, '별똥별. 그때 빈 소원, 지금 말해 줄까? ....「이 친구랑 하루만 더」였어. 근데 벌써 들어줬어. 닷새나 줬어.');
  await talk('마틸다', '이제 진짜 가야 하나 봐. 「졸업 축하해」, 말해 줄래? 그 말 들으면 갈 수 있어.', 1300);
  pick.innerHTML = ['졸업 축하해, 틸다.', '아직 말 안 할래. 하루만 더 있어.', '축하해. 그리고 고마워. 친구가 돼 줘서.'].map((t, i) => `<button data-i="${i}">${t}</button>`).join(''); pick.style.display = 'flex'; mark('pick'); await sleep(2600);
  pick.querySelector('[data-i="0"]').classList.add('on'); await sleep(600); pick.style.display = 'none';
  await talk('마틸다', '....고마워. 이 말 들으려고 100 년 기다렸나 봐. 근데 듣고 나니까, 조금 더 기다릴 걸 그랬어. 너랑 조금 더.', 1700);
  await talk('마틸다', '바다 약속, 잊지 마. 네가 바다에 가면, 하얀 파도 하나는 나야.', 1500);
  await talk('마틸다', '무서운 거 반씩 나눴잖아. 그러니까 지금 반만 슬픈 거야. 반만.', 1600);
  await talk('마틸다', '이제 아껴 둔 거 할게.', 900);
  World.say('me', '✋'); mark('hi'); await sleep(500); pop.textContent = '쉭!'; pop.classList.add('on'); for (let k = 0; k < 6; k++){ ga = k % 2 ? 1 : .55; await sleep(110); } ga = 1; await sleep(500); pop.classList.remove('on');
  await talk('마틸다', '....닿았다. 마지막에 닿았네.', 1500);
  // 떠나요
  ghostOn = false; put(); fx.classList.add('on'); fxT0 = performance.now(); mark('ascend'); fxRaf = requestAnimationFrame(drawFx);
  await sleep(4300); mark('bell'); pop.textContent = '뎅.......'; pop.style.fontSize = '30px'; pop.classList.add('on'); await sleep(1400); pop.classList.remove('on');
  capY = 10; await sleep(3200); fx.classList.remove('on'); await sleep(900); cancelAnimationFrame(fxRaf); dim.style.opacity = 0;
  await showCard(`<canvas id="grc" width="64" height="64" style="width:160px;height:160px"></canvas>마틸다의 졸업 모자<small>하늘에서 천천히 내려와 내 앞에 놓였어요</small>`, () => { const g = document.querySelector('#grc').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(CAP, 0, 0, 64, 64, 0, 0, 64, 64); }, 2600);
  await showCard(`<div style="display:flex;gap:14px;align-items:flex-end"><img src="ghost_photo.png" style="width:93px;height:135px"><canvas id="grb" width="32" height="32" style="width:64px;height:64px"></canvas></div>보상<small>방 가구 「빛바랜 졸업 사진」 · 「마틸다의 녹슨 단추」<br>개근상 이름표 · 졸업 모자</small>`, () => { const g = document.querySelector('#grb').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BT, 0, 0, 32, 32, 0, 0, 32, 32); }, 3400);
  await sleep(600); clearInterval(loop); World.setProps(gmap, [], 'tilda'); window.__grDone = true;
};
})();
