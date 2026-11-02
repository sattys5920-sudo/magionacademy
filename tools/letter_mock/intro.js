// ===== 시작 연출: 학교 앞 마당 · 배트리가 날다가 돌풍에 꽈당 → 편지가 날아가며 봉투가 다 벗겨짐 → 난처한 얼굴로 와서 부탁 =====
const PLAZA = { img: Object.assign(new Image(), { src: 'data:image/png;base64,__PLAZA__' }), OX: 252, OY: -168 };
const IZ = 3;
let IC = null;
const isleep = ms => new Promise(r => setTimeout(r, ms));
const itp = (x, y) => [PLAZA.OX + (x - y) * 8, PLAZA.OY + (x + y) * 4];
function introStart(){
  const o = document.getElementById('cine'); o.hidden = false;
  const cw = document.querySelector('.cwrap'), cc = document.getElementById('ccv'); cc.width = cw.clientWidth; cc.height = cw.clientHeight;
  IC = { t0: performance.now(), me: { x: 44, y: 49.4, dir: 5 }, bat: { x: 33, y: 44, h: 46, dir: 15, fly: true, face: 0, sweat: 0 }, wind: 0, papers: [], envs: [], bang: null, shake: 0, bub: null };
  requestAnimationFrame(introLoop);
}
function introLoop(now){
  if (!IC) return; requestAnimationFrame(introLoop);
  const c = document.getElementById('ccv'), q = c.getContext('2d'); q.imageSmoothingEnabled = false; const t = (now - IC.t0) / 1000;
  const [fx, fy] = itp(45.5, 48), sh = IC.shake > 0 ? Math.random() * 4 - 2 : 0; IC.shake = Math.max(0, IC.shake - 16);
  const ox = fx - c.width / IZ / 2 + sh, oy = fy - c.height / IZ * .48;
  const W2 = (x, y) => { const [px, py] = itp(x, y); return [(px - ox) * IZ, (py - oy) * IZ]; };
  q.fillStyle = '#140E1E'; q.fillRect(0, 0, c.width, c.height);
  if (PLAZA.img.complete) q.drawImage(PLAZA.img, -ox * IZ, -oy * IZ, PLAZA.img.width * IZ, PLAZA.img.height * IZ);
  // 바람 줄기
  if (IC.wind > 0){ q.globalAlpha = Math.min(1, IC.wind) * .6; q.fillStyle = '#E8F0FF'; for (let i = 0; i < 14; i++){ const y = (i * 53) % c.height, x = ((t * 900 * (1 + i % 3 * .4)) + i * 140) % (c.width + 200) - 100; q.fillRect(x, y, 60 + (i % 4) * 30, 2); } q.globalAlpha = 1; }
  // 바닥에 흩어진 편지 (봉투 없이 접힌 종이)
  IC.papers.forEach(p => { const k = Math.min(1, (t - p.t0) / p.dur), x = p.x0 + (p.x1 - p.x0) * k, y = p.y0 + (p.y1 - p.y0) * k, lift = Math.sin(k * Math.PI) * p.hop, [px, py] = W2(x, y), rot = (1 - k) * Math.sin(t * 9 + p.s) * .9;
    q.save(); q.translate(px, py - lift * IZ); q.rotate(rot); q.fillStyle = '#2A1A2E'; q.fillRect(-9, -6, 18, 12); q.fillStyle = '#FFF8EC'; q.fillRect(-8, -5, 16, 10); q.fillStyle = '#C8B8A0'; q.fillRect(-5, -2, 10, 1); q.fillRect(-5, 1, 7, 1); q.restore(); });
  // 날아가는 봉투 (벗겨진 껍데기)
  IC.envs.forEach(e => { const k = (t - e.t0) / 2.4; if (k > 1) return; const x = e.x + k * c.width * 1.1, y = e.y - k * 120 + Math.sin(t * 7 + e.s) * 16;
    q.save(); q.translate(x, y); q.rotate(t * 5 + e.s); q.fillStyle = '#2A1A2E'; q.fillRect(-11, -8, 22, 16); q.fillStyle = e.col; q.fillRect(-10, -7, 20, 14); q.fillStyle = 'rgba(0,0,0,.15)'; q.beginPath(); q.moveTo(-10, -7); q.lineTo(0, 1); q.lineTo(10, -7); q.fill(); q.restore(); });
  // 사람들 (y 순서)
  const L = [IC.me, IC.bat].sort((a, b) => (a.x + a.y) - (b.x + b.y));
  L.forEach(a => { const [px, py] = W2(a.x, a.y), lift = a.h ? a.h * IZ : 0;
    q.fillStyle = 'rgba(0,0,0,.25)'; q.beginPath(); q.ellipse(px, py, (a.h ? 4 : 6) * IZ, 2.2 * IZ, 0, 0, 7); q.fill();
    const row = a === IC.me ? 11 : 1, col = a.flat ? 10 : a.walk ? a.dir + 1 + (Math.floor(t * 8) % 4) : a.fly ? a.dir + 1 + (Math.floor(t * 10) % 4) : a.dir;
    q.save(); q.translate(px, py - lift); if (a.flat){ q.rotate(-Math.PI / 2); q.translate(10 * IZ, 0); }
    if (SHEET.complete) q.drawImage(SHEET, col * 64, row * 64, 64, 64, Math.round(-16 * IZ + (a.wob ? Math.sin(t * 30) * 4 : 0)), Math.round(-28 * IZ), 32 * IZ, 32 * IZ);
    q.restore();
    if (a.sweat){ q.fillStyle = '#9AD4F0'; const dy = (t * 20) % 10; q.fillRect(px + 9 * IZ, py - 26 * IZ + dy, 2 * IZ, 3 * IZ); }
    if (a.stars){ for (let i = 0; i < 3; i++){ const an = t * 4 + i * 2.1; q.fillStyle = '#FFE9A0'; q.fillRect(px + Math.cos(an) * 30 - 3, py - 20 * IZ + Math.sin(an) * 8 - 30, 6, 6); } }
  });
  if (IC.bang){ const [px, py] = W2(IC.bat.x, IC.bat.y); q.font = `${10 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 6; q.strokeStyle = '#3A2414'; q.strokeText(IC.bang, px, py - 34 * IZ); q.fillStyle = '#FFE9A0'; q.fillText(IC.bang, px, py - 34 * IZ); q.textAlign = 'left'; }
  if (IC.bub && now < IC.bub.until){ const [px, py] = W2(IC.bub.a.x, IC.bub.a.y); q.font = '14px G11, sans-serif'; const w = Math.ceil(q.measureText(IC.bub.text).width) + 16, bx = Math.max(4, Math.min(c.width - w - 4, px - w / 2)), by = py - 34 * IZ;
    q.fillStyle = '#22183F'; q.fillRect(bx - 2, by - 2, w + 4, 26); q.fillStyle = '#FFFFFF'; q.fillRect(bx, by, w, 22); q.fillStyle = '#22183F'; q.fillRect(px - 3, by + 24, 6, 2); q.fillText(IC.bub.text, bx + 8, by + 16); }
}
async function iwalk(a, x, y, ms){ const x0 = a.x, y0 = a.y, t0 = performance.now(), dx = x - x0, dy = y - y0, sx = (dx - dy) * 8, sy = (dx + dy) * 4; a.dir = Math.abs(sx) > Math.abs(sy) ? (sx > 0 ? 15 : 10) : (sy > 0 ? 0 : 5); a.walk = true;
  await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / ms); a.x = x0 + dx * k; a.y = y0 + dy * k; if (k < 1) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); a.walk = false; }
function itoast(t){ const el = document.getElementById('ctoast'); el.textContent = t; el.classList.add('on'); clearTimeout(itoast.t); itoast.t = setTimeout(() => el.classList.remove('on'), 2400); }
async function isay(t, hold = 1500){
  const v = document.getElementById('blsay'), p = v.querySelector('p'), g = v.querySelector('canvas').getContext('2d'); g.imageSmoothingEnabled = false; g.fillStyle = '#1E2A44'; g.fillRect(0, 0, 32, 32); if (SHEET.complete) g.drawImage(SHEET, 16, 1 * 64 + 10, 32, 32, 0, 0, 32, 32);
  v.style.display = 'block'; p.textContent = ''; let skip = false; v.onclick = () => { skip = true; };
  for (let k = 1; k <= t.length && !skip; k++){ p.textContent = t.slice(0, k); await isleep(30); } p.textContent = t;
  await new Promise(r => { let done = false; const go = () => { if (done) return; done = true; r(); }; v.onclick = go; setTimeout(go, hold + t.length * 45); });
  v.style.display = 'none'; await isleep(120);
}
async function playIntro(){
  introStart(); const B = IC.bat, ME = IC.me;
  await isleep(700);
  // 배트리가 가방을 메고 날아와요
  await iwalk(B, 40, 46, 1800); B.fly = true;
  itoast('휘이이잉....... 갑자기 거센 바람이 불어요'); IC.wind = .4; await isleep(400); IC.wind = 1.2; B.wob = true; await iwalk(B, 43, 46.5, 900);
  // 꽈당
  for (let k = 0; k <= 10; k++){ B.h = 46 * (1 - k / 10); B.x += .25; await isleep(28); } B.h = 0; B.flat = true; B.wob = false; B.fly = false;
  IC.bang = '꽈당!'; IC.shake = 400; await isleep(150);
  const t = (performance.now() - IC.t0) / 1000, [bx, by] = [B.x, B.y], c = document.getElementById('ccv');
  for (let i = 0; i < 14; i++){ const a = i / 14 * 6.283 + Math.random() * .3, r = 2 + Math.random() * 4.5; IC.papers.push({ t0: t, dur: .9 + Math.random() * .6, x0: bx, y0: by, x1: bx + Math.cos(a) * r, y1: by + Math.sin(a) * r * .8, hop: 18 + Math.random() * 20, s: i }); }
  const [ex, ey] = (() => { const o = itp(bx, by); return [c.width / 2, c.height * .45]; })();
  for (let i = 0; i < 12; i++) IC.envs.push({ t0: t + i * .05, x: ex - 40 + Math.random() * 80, y: ey - 20 + Math.random() * 60, s: i * 1.7, col: ['#F4EAD8', '#EAF0F8', '#F6E8EE', '#EEF4E6'][i % 4] });
  await isleep(900); IC.bang = null; itoast('편지가 사방으로 흩어지고, 봉투만 바람에 날아가 버렸어요'); await isleep(1600); IC.wind = .3;
  B.stars = true; await isleep(1200); B.stars = false; B.flat = false; B.dir = 0; await isleep(400); IC.wind = 0;
  B.sweat = 1; await iwalk(B, 45.2, 48.2, 1200); B.dir = 10;
  await isay('으으.... 아파.......');
  await isay('바람이 갑자기 확 불어서.... 꽈당 넘어졌어. 가방에 있던 편지가 전부 날아가 버렸어.');
  await isay('봉투까지 다 벗겨져서 누가 보낸 건지도 모르겠어. 받는 사람 이름은.... 편지 첫 줄에 적혀 있을 거야.', 1700);
  await isay('그래서 말인데.... 혹시라도 주우면, 주인 좀 찾아 줄래? 그 친구 방에 살짝 놓아 주기만 하면 돼.', 1700);
  IC.bub = { a: ME, text: '응, 찾아 줄게!', until: performance.now() + 1500 }; await isleep(1500);
  B.sweat = 0; await isay('고마워.... 진짜 고마워. 나도 열심히 찾아볼게. 날개 펴고!');
  await isleep(300); document.getElementById('cine').hidden = true; IC = null;
}
