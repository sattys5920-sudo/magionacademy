// ===== 선물 연출: 상자를 건넴 → NPC가 받아서 열어 봄 → NPC마다 다른 기뻐하는 동작 → 냠냠 → 대사
// 게임에서는 NPC가 서 있는 그 자리 맵 위에서 나와요. 시안은 과자 교실 맵으로 보여 줘요.
const GZ = 3;
let GC = null;
// 도트 무늬 (1 = 테두리, 2 = 색, 3 = 밝은 색)
const BMP = {
  heart: ['0110110', '1221221', '1222221', '0122210', '0012100', '0001000'],
  star: ['0001000', '0012100', '1122211', '0122210', '0121210', '0100010'],
  note: ['0011110', '0012210', '0010010', '0110110', '1210121', '0100010'],
  flower: ['0011100', '0132310', '1323231', '0132310', '0011100'],
  drop: ['00100', '01210', '12221', '12221', '01110'],
  feather: ['0001', '0012', '0122', '1220', '1200', '1000'],
  crow: ['1100011', '0111110', '0012100', '0001000'],
  bunny: ['01010', '01010', '12221', '12321', '12221', '01110'],
  spark: ['0010', '0110', '1111', '0110', '0100'],
  sweat: ['010', '121', '121', '010'],
  bat: ['1000001', '1101011', '1122211', '0112110', '0001000'],
  crown: ['1010101', '1212121', '1222221', '1111111'],
};
const FXC = { heart: ['#FF6B8A', '#FFB0C4'], star: ['#FFD866', '#FFF4B8'], note: ['#9AC8F0', '#D8ECFF'], flower: ['#FF9EC0', '#FFE27A'], drop: ['#7CC8F0', '#D8F0FF'], feather: ['#C8A878', '#F0DCB8'], crow: ['#2A1A2E', '#2A1A2E'], bunny: ['#FFFFFF', '#FFC8D8'], spark: ['#FFE860', '#FFFFFF'], sweat: ['#9AD4F0', '#E0F4FF'], bat: ['#6A4A9A', '#9A7AC8'], crown: ['#FFD24A', '#FFF0A0'] };
function bmp(q, k, x, y, s, a = 1){ const B = BMP[k], C = FXC[k]; q.globalAlpha = a; B.forEach((row, j) => [...row].forEach((v, i) => { if (v === '0') return; q.fillStyle = v === '1' ? (k === 'crow' || k === 'bunny' && false ? C[0] : '#2A1A2E') : v === '2' ? C[0] : C[1]; if (k === 'crow') q.fillStyle = '#2A1A2E'; q.fillRect(Math.round(x + (i - row.length / 2) * s), Math.round(y + (j - B.length / 2) * s), s, s); })); q.globalAlpha = 1; }
// NPC마다 다른 반응: act = 몸 동작, fx = 튀어나오는 것, emo = 머리 위 글자
const REACT = {
  nabi: { act: 'roll', fx: 'heart', emo: '냥!', say: '골골골.......' },
  batri: { act: 'fly', fx: 'bat', emo: '와!', say: '빙글빙글!' },
  kappa: { act: 'head', fx: 'drop', emo: '오.', say: '....균형 잡는 중이다.' },
  aula: { act: 'tilt', fx: 'feather', emo: '어머.', say: '부엉.......' },
  mandi: { act: 'blush', fx: 'flower', emo: '♥', say: '헤헤.......' },
  jipsin: { act: 'shoo', fx: 'crow', emo: '!', say: '저리 가라, 내 쿠키다.' },
  sera: { act: 'stamp', fx: 'heart', emo: '어머', say: '진찰 결과.... 합격!', stamp: '건강 합격' },
  madeleine: { act: 'stamp', fx: 'crown', emo: '오!', say: '심사 결과.......', stamp: '합격!' },
  stella: { act: 'spin', fx: 'star', emo: '☆', say: '별이 반짝반짝.......' },
  leo: { act: 'bunny', fx: 'bunny', emo: '하하!', say: '얘들아, 이거 봐라!' },
  otumo: { act: 'zap', fx: 'spark', emo: '삐빅!', say: '기쁨 회로 과열.......' },
};
const gtp = (x, y) => [164 + (x - y) * 8, 82 + (x + y) * 4];
function giftCine(n, B, tier, ck, line){
  return new Promise(done => {
    const o = $('#cine'); o.hidden = false; o.querySelector('.cnm').textContent = n.n.replace(' 선생님', '') + '에게 선물';
    const cw = document.querySelector('.cwrap'), cc = $('#ccv'); cc.width = cw.clientWidth; cc.height = cw.clientHeight;
    const R = REACT[n.id];
    GC = { t0: performance.now(), me: { x: 9.6, y: 12.4, dir: 15, row: 11 }, np: { x: 13.2, y: 9.2, dir: 10, row: n.row }, box: { st: 'held', k: 0 }, fx: [], emo: null, bub: null, stamp: null, R, tier, ck, B, shake: 0, cookie: null, bites: 0, crumbs: [], spin: 0, rot: 0, lift: 0, blush: 0, onHead: false };
    requestAnimationFrame(giftLoop);
    const run = ++giftRun, ok = () => run === giftRun && GC;
    $('#cskip').onclick = () => { giftRun++; GC = null; o.hidden = true; $('#blsay').style.display = 'none'; done(); };
    giftScript(n, line, ok).then(() => { if (run !== giftRun) return; o.hidden = true; GC = null; done(); });
  });
}
let giftRun = 0;
function boxImg(B, open){ const c = document.createElement('canvas'); c.width = open ? 120 : 60; c.height = open ? 96 : 48; const g = c.getContext('2d'); if (open) drawBoxOpen(g, B); else drawBoxClosed(g, B); return c; }
function giftLoop(now){
  if (!GC) return; requestAnimationFrame(giftLoop);
  const c = $('#ccv'), q = c.getContext('2d'); q.imageSmoothingEnabled = false; const t = (now - GC.t0) / 1000;
  const sh = GC.shake > 0 ? Math.random() * 6 - 3 : 0; GC.shake = Math.max(0, GC.shake - 16);
  const [fx, fy] = gtp(11.4, 10.8), ox = fx - c.width / GZ / 2 + sh, oy = fy - c.height / GZ * .55;
  const S = (px, py) => [(px - ox) * GZ, (py - oy) * GZ], W2 = (x, y) => S(...gtp(x, y));
  q.fillStyle = '#120C18'; q.fillRect(0, 0, c.width, c.height);
  if (CANDY.complete) q.drawImage(CANDY, -ox * GZ, -oy * GZ, CANDY.width * GZ, CANDY.height * GZ);
  q.fillStyle = 'rgba(20,10,30,.25)'; q.fillRect(0, 0, c.width, c.height);
  const [npx, npy] = W2(GC.np.x, GC.np.y), [mpx, mpy] = W2(GC.me.x, GC.me.y);
  // 깡총 토끼 · 까마귀 같은 땅 위 효과는 사람보다 먼저
  GC.fx.filter(f => f.ground).forEach(f => drawFx(q, f, t, npx, npy));
  [GC.me, GC.np].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(a => {
    const [px, py] = W2(a.x, a.y), isN = a === GC.np;
    const hop = a.jump ? Math.abs(Math.sin(t * 12)) * 4 * GZ : 0, lift = isN ? GC.lift * GZ : 0;
    q.fillStyle = 'rgba(0,0,0,.25)'; q.beginPath(); q.ellipse(px, py, (lift ? 4 : 6) * GZ, 2.2 * GZ, 0, 0, 7); q.fill();
    const col = a.walk ? a.dir + 1 + (Math.floor(t * 8) % 4) : (isN && GC.flap) ? a.dir + 1 + (Math.floor(t * 12) % 4) : a.dir;
    q.save(); q.translate(px, py - hop - lift - 14 * GZ); if (isN && GC.rot) q.rotate(GC.rot);
    if (SHEET.complete) q.drawImage(SHEET, col * 64, a.row * 64, 64, 64, -16 * GZ, -14 * GZ, 32 * GZ, 32 * GZ);
    if (isN && GC.blush){ q.fillStyle = `rgba(255,120,150,${GC.blush * .8})`; q.fillRect(-7 * GZ, -1 * GZ, 3 * GZ, 2 * GZ); q.fillRect(4 * GZ, -1 * GZ, 3 * GZ, 2 * GZ); }
    q.restore();
    if (isN && a.sweat){ bmp(q, 'sweat', px + 10 * GZ, py - 26 * GZ - lift + (t * 10 % 4), GZ); }
    // 상자: 플레이어 손 / NPC 손 / 머리 위
    const b = GC.box;
    if ((b.st === 'held' && !isN) || (b.st === 'npc' && isN)){ const img = boxImg(GC.B, false); const bob = a.walk ? Math.abs(Math.sin(t * 16)) * GZ * .6 : b.st === 'npc' ? Math.sin(t * 5) * GZ * .4 : 0, face = a.dir === 15 ? 1 : a.dir === 10 ? -1 : 0; q.drawImage(img, px - 24 + face * 3 * GZ, py - 9 * GZ - 19 - hop - lift + bob, 48, 38); }
    if (isN && GC.onHead){ const img = boxImg(GC.B, false), sway = Math.sin(t * 5) * 6 * GZ; q.save(); q.translate(px + sway * .3, py - 30 * GZ - lift); q.rotate(Math.sin(t * 5) * .25); q.drawImage(img, -30, -48, 60, 48); q.restore(); }
  });
  const b = GC.box;
  if (b.st === 'fly'){ const k = Math.min(1, (now - b.t) / 600), x = mpx + (npx - mpx) * k, y = mpy + (npy - mpy) * k - 9 * GZ - Math.sin(k * Math.PI) * 6 * GZ; q.drawImage(boxImg(GC.B, false), x - 24 + (1 - 2 * k) * 3 * GZ, y - 19, 48, 38); }
  if (b.st === 'open'){ const img = boxImg(GC.B, true); q.drawImage(img, npx - 36 - 2 * GZ, npy - 26, 72, 58); }
  // 떠오르는 쿠키
  if (GC.cookie){ const k = Math.min(1, (now - GC.cookie.t) / 500), cy = npy - 30 * GZ - k * 8 * GZ, cx = npx - 18 * GZ; GC.cpos = [cx, cy]; const tmp = document.createElement('canvas'); tmp.width = 24; tmp.height = 24; const g = tmp.getContext('2d'); drawCookie(g, GC.ck, 0, 0, 1);
    if (GC.bites){ g.globalCompositeOperation = 'destination-out'; for (let i = 0; i < GC.bites; i++){ g.beginPath(); g.arc(22 - i * 2, 4 + i * 5, 4 + i, 0, 7); g.fill(); } g.globalCompositeOperation = 'source-over'; }
    if (GC.bites < 4){ q.fillStyle = 'rgba(255,240,180,.35)'; q.beginPath(); q.arc(cx, cy, 20 * GZ * .9, 0, 7); q.fill(); q.drawImage(tmp, cx - 24 * GZ / 2 * .9, cy - 24 * GZ / 2 * .9, 24 * GZ * .9, 24 * GZ * .9); } }
  GC.crumbs = GC.crumbs.filter(f => now - f.t < 700); GC.crumbs.forEach(f => { const a = (now - f.t) / 1000; q.fillStyle = f.c; q.fillRect(f.x + f.vx * a * 60, f.y + f.vy * a * 60 + 300 * a * a, GZ * 1.5, GZ * 1.5); });
  GC.fx.filter(f => !f.ground).forEach(f => drawFx(q, f, t, npx, npy));
  GC.fx = GC.fx.filter(f => t - f.t0 < f.life);
  if (GC.stamp){ const k = Math.min(1, (now - GC.stamp.at) / 200), s = 2.2 - k * 1.2; q.save(); q.translate(npx, npy - 44 * GZ); q.rotate(-.18); q.scale(s, s); q.font = `${9 * GZ}px G11B, sans-serif`; q.textAlign = 'center'; const w = q.measureText(GC.stamp.tx).width + 10 * GZ; q.strokeStyle = '#E8455A'; q.lineWidth = GZ * 1.2; q.strokeRect(-w / 2, -8 * GZ, w, 11 * GZ); q.fillStyle = '#E8455A'; q.fillText(GC.stamp.tx, 0, 0); q.restore(); q.textAlign = 'left'; }
  if (GC.emo && now < GC.emo.until){ q.font = `${9 * GZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 5; q.strokeStyle = '#3A2414'; const yy = npy - 34 * GZ - GC.lift * GZ; q.strokeText(GC.emo.t, npx, yy); q.fillStyle = GC.emo.c || '#FFE9A0'; q.fillText(GC.emo.t, npx, yy); q.textAlign = 'left'; }
  if (GC.bub && now < GC.bub.until){ const a = GC.bub.a, [px, py] = W2(a.x, a.y); q.font = '14px G11, sans-serif'; const w = Math.ceil(q.measureText(GC.bub.text).width) + 16, bx = Math.max(4, Math.min(c.width - w - 4, px - w / 2)), by = py - 40 * GZ - 10 - (a === GC.np ? GC.lift * GZ : 0);
    q.fillStyle = '#22183F'; q.fillRect(bx - 2, by - 2, w + 4, 26); q.fillStyle = '#FFFFFF'; q.fillRect(bx, by, w, 22); q.fillStyle = '#22183F'; q.fillRect(px - 3, by + 24, 6, 2); q.fillText(GC.bub.text, bx + 8, by + 16); }
}
function drawFx(q, f, t, npx, npy){
  const a = t - f.t0; if (a < 0) return; const k = a / f.life, s = GZ;
  if (f.kind === 'orbit'){ const an = f.a0 + a * f.sp, x = npx + Math.cos(an) * f.r * s, y = npy - 18 * s + Math.sin(an) * f.r * .45 * s - a * 6 * s; bmp(q, f.k, x, y, s, Math.min(1, (1 - k) * 2)); return; }
  if (f.kind === 'walk'){ const x = npx + (f.x0 + (f.x1 - f.x0) * k) * s, hop = Math.abs(Math.sin(a * 10)) * 5 * s; bmp(q, f.k, x, npy - 3 * s - hop, s); return; }
  if (f.kind === 'flyby'){ const x = npx + (f.x0 + (f.x1 - f.x0) * k) * s, y = npy + (f.y0 + (f.y1 - f.y0) * k) * s + Math.sin(a * 14) * 2 * s; bmp(q, f.k, x, y, s); return; }
  const x = npx + (f.x + f.vx * a) * s, y = npy + (f.y + f.vy * a + (f.g || 0) * a * a) * s; bmp(q, f.k, x, y, s, Math.min(1, (1 - k) * 2.5));
}
const gsleep = ms => new Promise(r => setTimeout(r, ms));
async function gwalk(a, x, y, ms){ const x0 = a.x, y0 = a.y, t0 = performance.now(); a.walk = true; await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / ms); a.x = x0 + (x - x0) * k; a.y = y0 + (y - y0) * k; if (k < 1 && GC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); a.walk = false; }
function burst(k, n, opt = {}){ const t = (performance.now() - GC.t0) / 1000; for (let i = 0; i < n; i++) GC.fx.push({ k, t0: t + i * (opt.gap || .08), life: opt.life || 1.6, x: (Math.random() - .5) * 16, y: -22 - Math.random() * 6, vx: (Math.random() - .5) * 26, vy: -14 - Math.random() * 14, g: opt.g ?? 6 }); }
function orbit(k, n, opt = {}){ const t = (performance.now() - GC.t0) / 1000; for (let i = 0; i < n; i++) GC.fx.push({ kind: 'orbit', k, t0: t, life: opt.life || 2.2, a0: i / n * 6.283, sp: opt.sp || 4, r: opt.r || 16 }); }
async function giftScript(n, line, ok){
  const R = GC.R, NP = GC.np, ME = GC.me, tier = GC.tier, big = tier === 0, mid = tier === 1;
  await gsleep(400); if (!ok()) return;
  await gwalk(ME, 11.6, 10.4, 1300); ME.dir = 15; if (!ok()) return;
  GC.bub = { a: ME, text: '이거, 내가 구운 쿠키야!', until: performance.now() + 1500 }; await gsleep(1500); if (!ok()) return;
  GC.box = { st: 'fly', t: performance.now() }; await gsleep(620); GC.box = { st: 'npc' }; if (!ok()) return;
  GC.emo = { t: '!', until: performance.now() + 800 }; await gsleep(900); if (!ok()) return;
  // 리본 풀고 열어 보기
  GC.box = { st: 'open' }; GC.shake = 120; burst('star', 4, { life: 1 }); await gsleep(500);
  GC.cookie = { t: performance.now() }; await gsleep(800); if (!ok()) return;
  // NPC마다 다른 반응
  if (tier === 3){
    NP.sweat = true; GC.emo = { t: '....', c: '#BDB0D6', until: performance.now() + 1400 }; await gsleep(1500); NP.sweat = false;
  } else if (tier === 2){
    GC.emo = { t: R.emo, until: performance.now() + 1000 }; burst(R.fx === 'crow' || R.fx === 'bunny' ? 'heart' : R.fx, 2); await gsleep(1200);
  } else {
    GC.emo = { t: R.emo, until: performance.now() + 1400 }; const nfx = big ? 1 : .5, dur = big ? 2400 : 1400;
    GC.box = { st: 'none' };
    if (R.act === 'roll'){ for (let i = 0; i < (big ? 2 : 1); i++){ const t0 = performance.now(); await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / 700); GC.rot = k * 6.283; GC.lift = Math.sin(k * Math.PI) * 8; if (k < 1 && GC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); } GC.rot = 0; GC.lift = 0; burst('heart', Math.round(8 * nfx)); await gsleep(800); }
    if (R.act === 'fly'){ GC.flap = true; orbit('bat', Math.round(4 * nfx) || 2, { r: 22 }); const t0 = performance.now(), x0 = NP.x, y0 = NP.y; await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / dur), an = k * 6.283 * (big ? 2 : 1); NP.x = x0 + Math.cos(an) * 1.6 - 1.6; NP.y = y0 + Math.sin(an) * 1.6; GC.lift = 10 + Math.sin(k * 12) * 2; NP.dir = Math.cos(an + 1.57) > 0 ? 15 : 10; if (k < 1 && GC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); NP.x = x0; NP.y = y0; GC.lift = 0; GC.flap = false; NP.dir = 10; }
    if (R.act === 'head'){ GC.onHead = true; burst('drop', Math.round(5 * nfx), { g: 30 }); await gsleep(dur); GC.onHead = false; }
    if (R.act === 'tilt'){ for (let i = 0; i < (big ? 4 : 2); i++){ GC.rot = (i % 2 ? -1 : 1) * .45; burst('feather', 1, { g: 4, life: 2 }); await gsleep(350); } GC.rot = 0; burst('heart', Math.round(5 * nfx)); await gsleep(700); }
    if (R.act === 'blush'){ const t0 = performance.now(); await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / 600); GC.blush = k; if (k < 1 && GC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); burst('flower', Math.round(10 * nfx), { gap: .12, life: 2 }); NP.jump = big; await gsleep(dur); NP.jump = false; }
    if (R.act === 'shoo'){ const t = (performance.now() - GC.t0) / 1000; for (let i = 0; i < (big ? 3 : 2); i++) GC.fx.push({ kind: 'flyby', k: 'crow', t0: t + i * .2, life: 1.4, x0: 60 + i * 8, x1: 6, y0: -40 - i * 6, y1: -30 }); await gsleep(1500); NP.jump = true; GC.emo = { t: '훠이!', until: performance.now() + 900 }; const t2 = (performance.now() - GC.t0) / 1000; for (let i = 0; i < (big ? 3 : 2); i++) GC.fx.push({ kind: 'flyby', k: 'crow', t0: t2, life: 1.2, x0: 6, x1: 70 + i * 10, y0: -30, y1: -70 - i * 8 }); await gsleep(1000); NP.jump = false; burst('heart', Math.round(4 * nfx)); await gsleep(600); }
    if (R.act === 'stamp'){ NP.jump = true; await gsleep(500); NP.jump = false; GC.stamp = { at: performance.now(), tx: R.stamp }; GC.shake = 200; burst(R.fx, Math.round(6 * nfx)); await gsleep(dur); GC.stamp = null; }
    if (R.act === 'spin'){ orbit('star', big ? 7 : 4, { r: 18, sp: 5, life: dur / 1000 + .4 }); const dirs = [0, 15, 5, 10]; for (let i = 0; i < (big ? 8 : 4); i++){ NP.dir = dirs[i % 4]; await gsleep(dur / (big ? 8 : 4)); } NP.dir = 10; }
    if (R.act === 'bunny'){ const t = (performance.now() - GC.t0) / 1000; for (let i = 0; i < (big ? 4 : 2); i++) GC.fx.push({ kind: 'walk', ground: true, k: 'bunny', t0: t + i * .25, life: 2.4, x0: -70 - i * 8, x1: -8 - i * 9 }); NP.jump = true; await gsleep(dur); NP.jump = false; }
    if (R.act === 'zap'){ NP.jump = true; for (let i = 0; i < (big ? 6 : 3); i++){ burst('spark', 2, { life: .6, g: 0 }); GC.shake = 80; await gsleep(260); } NP.jump = false; burst('heart', Math.round(5 * nfx)); await gsleep(800); }
    GC.bub = { a: NP, text: R.say, until: performance.now() + 1300 }; await gsleep(1300);
  }
  if (!ok()) return;
  // 냠냠
  GC.box = { st: 'none' };
  for (let i = 1; i <= 4; i++){ GC.bites = i; const [cx0, cy0] = GC.cpos || [0, 0]; for (let j = 0; j < 5; j++) GC.crumbs.push({ t: performance.now(), x: cx0 + (Math.random() - .5) * 40, y: cy0, vx: (Math.random() - .5) * 4, vy: -2 - Math.random() * 2, c: FL.find(f => f.id === GC.ck.f).c }); GC.emo = { t: '냠!', until: performance.now() + 300 }; await gsleep(tier === 3 ? 480 : 340); if (!ok()) return; }
  GC.cookie = null; await gsleep(300); if (!ok()) return;
  await say(n.row, n.n, line); if (!ok()) return;
  await gsleep(200);
}
