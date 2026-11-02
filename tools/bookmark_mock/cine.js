// ===== 연출: 한밤 도서관 맵 위에서 · 시작(재채기) / 끝(책이 돌아옴)
const LIB = Object.assign(new Image(), { src: 'data:image/png;base64,__LIB__' });
const LM = { OX: 180, OY: 96 }, IZ = 3;
const ltp = (x, y) => [LM.OX + (x - y) * 8, LM.OY + (x + y) * 4];
const BOOKP = [260, 135];   // 독서대 위 책 (세계 좌표)
let IC = null, cineRun = 0;
const csleep = ms => new Promise(r => setTimeout(r, ms));
const FC = { 3: [19, 24, 28], 11: [16, 10, 32] };
function cfaceTo(cv, row){ const q = cv.getContext('2d'); q.imageSmoothingEnabled = false; q.fillStyle = '#1E2A44'; q.fillRect(0, 0, cv.width, cv.height); const [x, y, z] = FC[row] || [16, 10, 32]; if (SHEET.complete) q.drawImage(SHEET, x, row * 64 + y, z, z, 0, 0, cv.width, cv.height); }
function cineStart(kind){
  const o = $('#cine'); o.hidden = false; const cw = document.querySelector('.cwrap'), cc = $('#ccv'); cc.width = cw.clientWidth; cc.height = cw.clientHeight;
  IC = { kind, t0: performance.now(), aula: { x: 12.4, y: 3.7, dir: 0, row: 3 }, me: { x: 13, y: 17.5, dir: 5, row: 11 }, words: [], dust: [], shake: 0, flash: 0, bang: null, bub: null, emo: null, book: kind === 'end' ? 'empty' : 'full', glow: 0, rise: 0, ring: 0 };
  requestAnimationFrame(cineLoop);
}
function cineLoop(now){
  if (!IC) return; requestAnimationFrame(cineLoop);
  const c = $('#ccv'), q = c.getContext('2d'); q.imageSmoothingEnabled = false; const t = (now - IC.t0) / 1000;
  const sh = IC.shake > 0 ? Math.random() * 8 - 4 : 0; IC.shake = Math.max(0, IC.shake - 16);
  const fx = 244, fy = 158, ox = fx - c.width / IZ / 2 + sh, oy = fy - c.height / IZ * .5;
  const S = (px, py) => [(px - ox) * IZ, (py - oy) * IZ], W2 = (x, y) => S(...ltp(x, y));
  q.fillStyle = '#0C0715'; q.fillRect(0, 0, c.width, c.height);
  if (LIB.complete) q.drawImage(LIB, -ox * IZ, -oy * IZ, LIB.width * IZ, LIB.height * IZ);
  q.fillStyle = 'rgba(14,10,40,.32)'; q.fillRect(0, 0, c.width, c.height);
  // 독서대 위 책 · 빛
  const [bx, by] = S(BOOKP[0], BOOKP[1] - IC.rise);
  if (IC.glow > 0){ const g = q.createRadialGradient(bx, by, 4, bx, by, 60 * IZ * IC.glow); g.addColorStop(0, `rgba(255,232,150,${.55 * IC.glow})`); g.addColorStop(1, 'rgba(255,232,150,0)'); q.fillStyle = g; q.fillRect(0, 0, c.width, c.height); }
  const R = (x, y, w, h, col) => { q.fillStyle = col; q.fillRect(Math.round(bx + x * IZ), Math.round(by + y * IZ), w * IZ, h * IZ); };
  if (IC.book === 'closed'){ R(-7, -9, 14, 18, '#2A1A2E'); R(-6, -8, 12, 16, '#2A3A6A'); R(-6, -8, 2, 16, '#1E2A50'); R(-3, -6, 7, 1, '#E8C468'); R(-3, 5, 7, 1, '#E8C468'); R(0, -2, 1, 4, '#FFF4C8'); R(-1, -1, 3, 2, '#FFF4C8'); }
  else { R(-9, -3, 18, 6, '#2A1A2E'); R(-8, -3, 8, 5, '#F6ECD6'); R(1, -3, 7, 5, '#EADBBE'); if (IC.book === 'full'){ for (let k = 0; k < 4; k++){ R(-7, -2 + k, 6, .4, '#8A7A6A'); R(2, -2 + k, 5, .4, '#8A7A6A'); } } }
  // 먼지 (코가 간질간질)
  IC.dust = IC.dust.filter(d => t - d.t0 < 2.4); IC.dust.forEach(d => { const a = (t - d.t0) / 2.4, [px, py] = S(d.x + (d.tx - d.x) * a, d.y + (d.ty - d.y) * a + Math.sin(a * 9 + d.s) * 3); q.fillStyle = `rgba(240,230,200,${.7 - a * .4})`; q.fillRect(px, py, IZ, IZ); });
  // 사람들
  [IC.me, IC.aula].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(a => {
    const [px, py] = W2(a.x, a.y), hop = a.jump ? Math.abs(Math.sin(t * 14)) * 3 * IZ : 0;
    q.fillStyle = 'rgba(0,0,0,.28)'; q.beginPath(); q.ellipse(px, py, 6 * IZ, 2.2 * IZ, 0, 0, 7); q.fill();
    const col = a.walk ? a.dir + 1 + (Math.floor(t * 8) % 4) : a.dir;
    if (SHEET.complete) q.drawImage(SHEET, col * 64, a.row * 64, 64, 64, Math.round(px - 16 * IZ), Math.round(py - 28 * IZ - hop), 32 * IZ, 32 * IZ);
    if (a.sweat){ q.fillStyle = '#9AD4F0'; q.fillRect(px + 9 * IZ, py - 22 * IZ + (t * 20) % 10, 2 * IZ, 3 * IZ); }
    if (IC.emo && IC.emo.a === a && now < IC.emo.until){ q.font = `${9 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 5; q.strokeStyle = '#3A2414'; q.strokeText(IC.emo.t, px + 12 * IZ, py - 26 * IZ); q.fillStyle = IC.emo.c || '#FFE9A0'; q.fillText(IC.emo.t, px + 12 * IZ, py - 26 * IZ); q.textAlign = 'left'; }
  });
  // 날개 단 글자들
  IC.words = IC.words.filter(w => !w.dead); q.font = '13px G11B, sans-serif'; q.textAlign = 'center';
  IC.words.forEach(w => { const a = (t - w.t0); if (a < 0) return; let x, y;
    if (w.mode === 'out'){ x = w.x0 + w.vx * a; y = w.y0 + w.vy * a - 30 * a + Math.sin(a * 6 + w.s) * 8; if (a > 3.5) w.dead = true; }
    else { const k = Math.min(1, a / w.dur), e = k * k * (3 - 2 * k); x = w.x0 + (bx - w.x0) * e + Math.sin(k * Math.PI) * w.curve; y = w.y0 + (by - w.y0) * e - Math.sin(k * Math.PI) * 60; if (k >= 1) w.dead = true; }
    const tw = Math.ceil(q.measureText(w.w).width) + 12, flap = Math.sin(now / 70 + w.s) * 3;
    q.fillStyle = '#FFFFFF'; q.strokeStyle = '#2A1A2E'; q.lineWidth = 2;
    [[-1, x - tw / 2], [1, x + tw / 2]].forEach(([d, wx]) => { q.beginPath(); q.moveTo(wx, y - 4); q.lineTo(wx + d * 9, y - 10 - flap); q.lineTo(wx + d * 7, y + 2); q.closePath(); q.fill(); q.stroke(); });
    q.fillStyle = '#2A1A2E'; q.fillRect(x - tw / 2 - 2, y - 11, tw + 4, 20); q.fillStyle = w.c; q.fillRect(x - tw / 2, y - 9, tw, 16); q.fillStyle = '#3A2A40'; q.fillText(w.w, x, y + 4);
    if (w.mode === 'in' && w.c === '#FFF4C8'){ q.fillStyle = '#FFE9A0'; q.fillRect(x + tw / 2 + 4, y - 12, 2, 2); } });
  q.textAlign = 'left';
  if (IC.ring > 0){ for (let i = 0; i < 16; i++){ const a = i / 16 * 6.283 + t * 1.5, r = (30 + Math.sin(t * 3 + i) * 4) * IZ; q.fillStyle = i % 2 ? '#FFE9A0' : '#FFFFFF'; q.globalAlpha = IC.ring; q.fillRect(bx + Math.cos(a) * r, by + Math.sin(a) * r * .6, IZ * 2, IZ * 2); } q.globalAlpha = 1; }
  if (IC.flash > 0){ q.fillStyle = `rgba(255,248,220,${IC.flash})`; q.fillRect(0, 0, c.width, c.height); IC.flash = Math.max(0, IC.flash - .02); }
  if (IC.bang){ const [px, py] = W2(IC.aula.x, IC.aula.y); q.font = `${13 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 8; q.strokeStyle = '#3A2414'; q.strokeText(IC.bang, px, py - 34 * IZ); q.fillStyle = '#FFE9A0'; q.fillText(IC.bang, px, py - 34 * IZ); q.textAlign = 'left'; }
  if (IC.bub && now < IC.bub.until){ const a = IC.bub.a, [px, py] = W2(a.x, a.y); q.font = '14px G11, sans-serif'; const w = Math.ceil(q.measureText(IC.bub.text).width) + 16, bx2 = Math.max(4, Math.min(c.width - w - 4, px - w / 2)), by2 = py - 34 * IZ - 10;
    q.fillStyle = '#22183F'; q.fillRect(bx2 - 2, by2 - 2, w + 4, 26); q.fillStyle = '#FFFFFF'; q.fillRect(bx2, by2, w, 22); q.fillStyle = '#22183F'; q.fillRect(px - 3, by2 + 24, 6, 2); q.fillText(IC.bub.text, bx2 + 8, by2 + 16); }
}
async function cwalk(a, x, y, ms){ const x0 = a.x, y0 = a.y, t0 = performance.now(), dx = x - x0, dy = y - y0, sx = (dx - dy) * 8, sy = (dx + dy) * 4; a.dir = Math.abs(sx) > Math.abs(sy) ? (sx > 0 ? 15 : 10) : (sy > 0 ? 0 : 5); a.walk = true;
  await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / ms); a.x = x0 + dx * k; a.y = y0 + dy * k; if (k < 1 && IC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); a.walk = false; }
function ctoast(t){ const el = $('#ctoast'); el.textContent = t; el.classList.add('on'); clearTimeout(ctoast.t); ctoast.t = setTimeout(() => el.classList.remove('on'), 2600); }
async function csay(t, hold = 1500, row = 3, name = '아울라'){
  const v = $('#blsay'), p = v.querySelector('p'); v.querySelector('b').textContent = name; cfaceTo(v.querySelector('canvas'), row);
  v.style.display = 'block'; p.textContent = ''; let skip = false; v.onclick = () => { skip = true; };
  for (let k = 1; k <= t.length && !skip; k++){ p.textContent = t.slice(0, k); await csleep(28); } p.textContent = t;
  await new Promise(r => { let done = false; const go = () => { if (done) return; done = true; r(); }; v.onclick = go; setTimeout(go, hold + t.length * 45); });
  v.style.display = 'none'; await csleep(100);
}
const cbub = (a, text, ms = 1600) => { IC.bub = { a, text, until: performance.now() + ms }; return csleep(ms); };
function cineSkip(){ cineRun++; IC = null; $('#cine').hidden = true; $('#blsay').style.display = 'none'; }
// ---------- 시작: 재채기
async function playSneeze(){
  const run = ++cineRun; cineStart('start'); const A = IC.aula, ME = IC.me, ok = () => run === cineRun && IC; $('#cskip').onclick = cineSkip;
  await csleep(500); if (!ok()) return; ctoast('한밤 도서관.... 책장 넘기는 소리만 들려요');
  A.dir = 5; await csleep(1800); if (!ok()) return;
  await cbub(A, '....후후. 여기는 몇 번을 읽어도 좋네요.', 2200); if (!ok()) return;
  cwalk(ME, 13, 8.5, 2600);
  const t = (performance.now() - IC.t0) / 1000; for (let i = 0; i < 26; i++){ const sx = [180, 330, 140, 360][i % 4], sy = [110, 120, 150, 140][i % 4]; IC.dust.push({ x: sx + Math.random() * 30, y: sy + Math.random() * 30, tx: 252, ty: 132, t0: t + i * .07, s: i }); }
  await csleep(1600); if (!ok()) return;
  A.dir = 0; await cbub(A, '코가.... 간질간질.......', 1600); if (!ok()) return;
  IC.bang = '부.... 부엉.......'; await csleep(900); IC.bang = '에.... 에.......'; await csleep(800); if (!ok()) return;
  IC.bang = '에취!'; IC.shake = 600; IC.flash = .7; A.jump = true; IC.book = 'blank';
  const t2 = (performance.now() - IC.t0) / 1000, [bx, by] = [$('#ccv').width / 2 + 40, $('#ccv').height * .4];
  const W = ALL.slice(0, 48); W.forEach((w, i) => { const a = Math.random() * 6.283, sp = 140 + Math.random() * 260; IC.words.push({ w, mode: 'out', x0: bx, y0: by, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp * .7 - 60, t0: t2 + i * .035, s: i, c: wc(w) }); });
  await csleep(900); IC.bang = null; A.jump = false; await csleep(1500); if (!ok()) return;
  ctoast('책 속 단어들이 날개를 달고 사방으로 날아갔어요'); await csleep(1800); if (!ok()) return;
  A.sweat = true; IC.emo = { a: A, t: '!', until: performance.now() + 900 }; A.dir = 10; await csleep(900);
  for (const s of ['....앗. 아, 안 돼요. 글자들이.......', '제가 새로 쓴 책이었어요. 이제 막 마지막 장까지 다 썼는데.......', '재채기 한 번에 단어들이 날개를 달고 다 날아가 버렸어요. 책장이 하얘요.']){ await csay(s); if (!ok()) return; }
  A.sweat = false;
  for (const s of ['단어들은 겁이 많아서, 덤불 속이나 물속에 숨어 있을 거예요. 채집하거나 낚시하다 보면.... 파닥파닥 나올 거예요.', '주우면 사서 책상에 모아 주세요. 반 전체가 같이 맞추면, 다시 책이 될 거예요.']){ await csay(s, 1700); if (!ok()) return; }
  await cbub(ME, '같이 찾아볼게요!', 1500); if (!ok()) return;
  IC.emo = { a: A, t: '♥', c: '#FF9EC0', until: performance.now() + 1200 };
  for (const s of ['고마워요. 아, 그리고.... 기다리는 동안 책갈피도 만들어 보세요. 사서 책상에 만드는 법 적어 뒀어요.', '※ 이번엔 코를 꼭 막고 기다릴게요.']){ await csay(s); if (!ok()) return; }
  await csleep(400); if (run !== cineRun) return; $('#cine').hidden = true; IC = null; ST.tab = 'bag'; render();
}
// ---------- 끝: 반 전체가 다 맞추면 글자들이 돌아와 책이 돼요
async function playReturn(){
  const run = ++cineRun; cineStart('end'); const A = IC.aula, ME = IC.me, ok = () => run === cineRun && IC; $('#cskip').onclick = cineSkip;
  ME.x = 13; ME.y = 8.5; ME.dir = 5; A.dir = 0;
  await csleep(600); if (!ok()) return; ctoast('마지막 단어가 제자리를 찾았어요');
  await cbub(A, '....들려요? 파닥파닥.......', 1800); if (!ok()) return;
  const c = $('#ccv'), t = (performance.now() - IC.t0) / 1000, W = ALL.slice(0, 64);
  W.forEach((w, i) => { const side = i % 4, x0 = side === 0 ? -60 : side === 1 ? c.width + 60 : Math.random() * c.width, y0 = side < 2 ? Math.random() * c.height : side === 2 ? -40 : c.height + 40; IC.words.push({ w, mode: 'in', x0, y0, dur: 1.6 + Math.random() * .8, curve: (Math.random() - .5) * 120, t0: t + i * .05, s: i, c: i % 5 ? wc(w) : '#FFF4C8' }); });
  IC.glow = .3; for (let k = 0; k < 40; k++){ IC.glow = Math.min(1, .3 + k / 40); await csleep(100); if (!ok()) return; }
  IC.book = 'full'; IC.flash = .9; IC.shake = 300; await csleep(500); IC.book = 'closed';
  for (let k = 0; k <= 30; k++){ IC.rise = Math.sin(k / 30 * Math.PI / 2) * 14; IC.ring = k / 30; await csleep(40); } if (!ok()) return;
  await csleep(1200); for (let k = 30; k >= 0; k--){ IC.rise = Math.sin(k / 30 * Math.PI / 2) * 14; await csleep(30); } IC.ring = .6; IC.glow = .5; if (!ok()) return;
  IC.emo = { a: A, t: '♥', c: '#FF9EC0', until: performance.now() + 1400 };
  for (const s of ['....다 돌아왔어요. 한 글자도 빠짐없이.', '다 같이 하나씩 주워 와서 맞춰 줬네요. 정말 고마워요.', '이 책은 대출되지 않아요. 대신.... 언제든 서고에 와서 읽어 주세요. 독서대 위에 둘게요.']){ await csay(s, 1700); if (!ok()) return; }
  await cbub(ME, '이번엔 코 막고 읽어요!', 1500); if (!ok()) return;
  await csay('....네. 꼭 막을게요.', 1300); if (!ok()) return;
  await csleep(300); if (run !== cineRun) return; $('#cine').hidden = true; IC = null; ST.done = true; ST.tab = 'read'; ST.rp = 0; render();
}
