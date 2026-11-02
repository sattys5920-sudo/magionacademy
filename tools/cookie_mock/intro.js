// ===== 시작 연출: 과자 교실 · 마들렌이랑 제일 쉬운 버터 동그라미 쿠키를 같이 굽는 튜토리얼 → 오븐 열림 · 쿠키 도감
const CM = { OX: 164, OY: 82 };
const IZ = 3;
let IC = null;
const ctp = (x, y) => [CM.OX + (x - y) * 8, CM.OY + (x + y) * 4];
const OVEN = [288, 131], CT = [247, 162];
function introStart(){
  const o = $('#cine'); o.hidden = false;
  const cw = document.querySelector('.cwrap'), cc = $('#ccv'); cc.width = cw.clientWidth; cc.height = cw.clientHeight;
  IC = { t0: performance.now(), me: { x: 10.4, y: 11.4, dir: 15, row: 11 }, mad: { x: 15.3, y: 1.9, dir: 5, row: 7 }, smoke: 0, puffs: [], last: 0, bang: null, shake: 0, bub: null, emo: null, words: [],
    bowl: 0, flour: 0, fly: [], dough: 0, tray: null, glow: 0, carry: null, myTray: true };
  requestAnimationFrame(introLoop);
}
function cookieDot(q, x, y, b, z){ const c = rgb(doughCol('butter', b, 0)), r = rgb(doughCol('butter', b, 1)); q.fillStyle = '#3A2414'; q.fillRect(x - 3 * z, y - 2 * z, 6 * z, 4 * z); q.fillRect(x - 2 * z, y - 3 * z, 4 * z, 6 * z); q.fillStyle = r; q.fillRect(x - 2 * z, y - 2 * z, 4 * z, 4 * z); q.fillStyle = c; q.fillRect(x - 1 * z, y - 1 * z, 2 * z, 2 * z); }
function trayDraw(q, x, y, b, z){ q.fillStyle = '#2A1A2E'; q.fillRect(x - 13 * z, y - 5 * z, 26 * z, 10 * z); q.fillStyle = '#B8B8C8'; q.fillRect(x - 12 * z, y - 4 * z, 24 * z, 8 * z); q.fillStyle = '#9898A8'; q.fillRect(x - 12 * z, y + 2 * z, 24 * z, 2 * z); [-7, 0, 7].forEach(dx => cookieDot(q, x + dx * z, y - z, b, z)); }
function introLoop(now){
  if (!IC) return; requestAnimationFrame(introLoop);
  const c = $('#ccv'), q = c.getContext('2d'); q.imageSmoothingEnabled = false; const t = (now - IC.t0) / 1000;
  const sh = IC.shake > 0 ? Math.random() * 6 - 3 : 0; IC.shake = Math.max(0, IC.shake - 16);
  const fx = 248, fy = 150, ox = fx - c.width / IZ / 2 + sh, oy = fy - c.height / IZ * .5;
  const S = (px, py) => [(px - ox) * IZ, (py - oy) * IZ], W2 = (x, y) => S(...ctp(x, y));
  q.fillStyle = '#120C18'; q.fillRect(0, 0, c.width, c.height);
  if (CANDY.complete) q.drawImage(CANDY, -ox * IZ, -oy * IZ, CANDY.width * IZ, CANDY.height * IZ);
  // 오븐 불빛
  const [gx, gy] = S(...OVEN); q.fillStyle = `rgba(255,150,40,${.15 + Math.sin(t * 8) * .04 + IC.glow * .2})`; q.beginPath(); q.arc(gx, gy + 6 * IZ, (16 + IC.glow * 6) * IZ, 0, 7); q.fill();
  // 작업대 위: 반죽 그릇 · 쟁반
  const [bx, by] = S(...CT);
  if (IC.bowl){ const wob = IC.bowl > 1 ? Math.round(Math.sin(t * 30)) * IZ : 0, R = (x, y, w, h, c) => { q.fillStyle = c; q.fillRect(bx + x * IZ + wob, by + y * IZ, w * IZ, h * IZ); };
    R(-9, -5, 18, 3, '#2A1A2E'); R(-8, -2, 16, 2, '#2A1A2E'); R(-7, 0, 14, 2, '#2A1A2E'); R(-5, 2, 10, 2, '#2A1A2E'); R(-8, -4, 16, 1, '#C86A7A'); R(-7, -2, 14, 2, '#F49AAA'); R(-6, 0, 12, 1, '#F49AAA'); R(-6, 1, 12, 1, '#D87888'); R(-4, 2, 8, 1, '#D87888'); R(-6, -2, 3, 1, '#FFD0D8'); R(-8, -5, 16, 1, '#FFE8EC');
    if (IC.dough){ R(-6, -6, 12, 2, '#3A2414'); R(-5, -6, 10, 2, '#F0CC86'); R(-3, -7, 6, 1, '#3A2414'); R(-2, -7, 4, 1, '#F8E0AA'); } }
  if (IC.tray) trayDraw(q, ...S(CT[0] + 18, CT[1] + 6), IC.tray.b, IZ * .75);
  // 밀가루 풀풀
  if (IC.flour > 0){ for (let i = 0; i < 8; i++){ const a = t * 3 + i * .8, r = (t * 14 + i * 5) % 14; q.fillStyle = `rgba(255,255,255,${.7 - r / 20})`; q.fillRect(bx + Math.cos(a) * r * IZ, by - 6 * IZ - r * IZ * .6, IZ * 2, IZ * 2); } }
  // 날아가는 재료
  IC.fly = IC.fly.filter(f => t - f.t0 < f.dur + .1);
  IC.fly.forEach(f => { const k = Math.min(1, (t - f.t0) / f.dur), x = f.x0 + (CT[0] - f.x0) * k, y = f.y0 + (CT[1] - 4 - f.y0) * k - Math.sin(k * Math.PI) * 18, [px, py] = S(x, y); if (ICIMG.complete) q.drawImage(ICIMG, f.i * 32, 0, 32, 32, px - 8 * IZ, py - 8 * IZ, 16 * IZ, 16 * IZ); });
  // 연기
  if (IC.smoke > 0 && now - IC.last > 140 / IC.smoke){ IC.last = now; IC.puffs.push({ x: OVEN[0] + (Math.random() * 8 - 4), y: OVEN[1], vx: -2 - Math.random() * 4, vy: -6 - Math.random() * 5, r: 2 + Math.random() * 2, t0: t, dark: IC.smoke > 1.2 }); }
  IC.puffs = IC.puffs.filter(p => t - p.t0 < 3.2);
  IC.puffs.forEach(p => { const a = t - p.t0, [px, py] = S(p.x + p.vx * a, p.y + p.vy * a), r = (p.r + a * 3) * IZ; q.fillStyle = p.dark ? `rgba(60,50,54,${.7 - a * .2})` : `rgba(210,206,210,${.55 - a * .17})`; q.fillRect(Math.round(px - r), Math.round(py - r), Math.round(r * 2), Math.round(r * 2)); });
  // 사람들
  [IC.me, IC.mad].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(a => {
    const [px, py] = W2(a.x, a.y), hop = a.jump ? Math.abs(Math.sin(t * 12)) * 3 * IZ : a.nod ? Math.abs(Math.sin(t * 7)) * 1.5 * IZ : 0;
    q.fillStyle = 'rgba(0,0,0,.25)'; q.beginPath(); q.ellipse(px, py, 6 * IZ, 2.2 * IZ, 0, 0, 7); q.fill();
    const col = a.walk ? a.dir + 1 + (Math.floor(t * (a.run ? 14 : 8)) % 4) : a.dir;
    if (SHEET.complete) q.drawImage(SHEET, col * 64, a.row * 64, 64, 64, Math.round(px - 16 * IZ), Math.round(py - 28 * IZ - hop), 32 * IZ, 32 * IZ);
    if (a.carry) trayDraw(q, px, py - 11 * IZ - hop, a.carry.b, IZ * .6);
    if (a.sweat){ q.fillStyle = '#9AD4F0'; const dy = (t * 20) % 10; q.fillRect(px + 9 * IZ, py - 26 * IZ + dy, 2 * IZ, 3 * IZ); }
    if (IC.emo && IC.emo.a === a && now < IC.emo.until){ q.font = `${9 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 5; q.strokeStyle = '#3A2414'; q.strokeText(IC.emo.t, px, py - 32 * IZ); q.fillStyle = IC.emo.c || '#FFE9A0'; q.fillText(IC.emo.t, px, py - 32 * IZ); q.textAlign = 'left'; }
  });
  // 효과음 글자 (촵촵 · 뿅 · 띵)
  IC.words = IC.words.filter(w => now < w.until);
  IC.words.forEach(w => { const [px, py] = S(w.x, w.y), k = 1 - (w.until - now) / w.ms, rise = k * 10 * IZ; q.globalAlpha = Math.min(1, (1 - k) * 3); q.font = `${(w.big ? 11 : 8) * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 6; q.strokeStyle = '#3A2414'; q.strokeText(w.t, px, py - rise); q.fillStyle = w.c || '#FFE9A0'; q.fillText(w.t, px, py - rise); q.textAlign = 'left'; q.globalAlpha = 1; });
  if (IC.bub && now < IC.bub.until){ const [px, py] = W2(IC.bub.a.x, IC.bub.a.y); q.font = '14px G11, sans-serif'; const w = Math.ceil(q.measureText(IC.bub.text).width) + 16, bx2 = Math.max(4, Math.min(c.width - w - 4, px - w / 2)), by2 = py - 36 * IZ - 10;
    q.fillStyle = '#22183F'; q.fillRect(bx2 - 2, by2 - 2, w + 4, 26); q.fillStyle = '#FFFFFF'; q.fillRect(bx2, by2, w, 22); q.fillStyle = '#22183F'; q.fillRect(px - 3, by2 + 24, 6, 2); q.fillText(IC.bub.text, bx2 + 8, by2 + 16); }
}
async function iwalk(a, x, y, ms){ const x0 = a.x, y0 = a.y, t0 = performance.now(), dx = x - x0, dy = y - y0, sx = (dx - dy) * 8, sy = (dx + dy) * 4; a.dir = Math.abs(sx) > Math.abs(sy) ? (sx > 0 ? 15 : 10) : (sy > 0 ? 0 : 5); a.walk = true;
  await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / ms); a.x = x0 + dx * k; a.y = y0 + dy * k; if (k < 1 && IC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); a.walk = false; }
function itoast(t){ const el = $('#ctoast'); el.textContent = t; el.classList.add('on'); clearTimeout(itoast.t); itoast.t = setTimeout(() => el.classList.remove('on'), 2400); }
const bub = (a, text, ms = 1600) => { IC.bub = { a, text, until: performance.now() + ms }; return sleep(ms); };
const emo = (a, t, c, ms = 900) => { IC.emo = { a, t, c, until: performance.now() + ms }; };
const word = (t, x, y, c, big, ms = 900) => IC.words.push({ t, x, y, c, big, ms, until: performance.now() + ms });
let introRun = 0;
async function playIntro(){
  const run = ++introRun; introStart(); const M = IC.mad, ME = IC.me;
  const ok = () => run === introRun && IC;
  const ms = async (t, hold) => { await say(7, '마들렌', t, hold); return ok(); };
  $('#cskip').onclick = () => { introRun++; IC = null; $('#cine').hidden = true; $('#blsay').style.display = 'none'; $('#fam').hidden = true; };
  await sleep(500); if (!ok()) return;
  // 바쁘게 오가는 마들렌
  itoast('과자 교실에서 고소한 냄새가 나요');
  M.carry = { b: 60 }; M.run = true; await iwalk(M, 18.6, 5.2, 900); if (!ok()) return; M.carry = null; IC.tray = { b: 60 };
  M.dir = 5; word('탁!', CT[0] + 18, CT[1], '#FFE9A0', false); await sleep(300);
  await iwalk(M, 15.0, 1.4, 900); if (!ok()) return; M.dir = 5; IC.glow = 1; await bub(M, '한 판, 두 판, 세 판.... 좋아, 다음 판!', 1700); if (!ok()) return;
  M.carry = { b: 0 }; await iwalk(M, 18.6, 5.2, 800); M.carry = null; M.run = false; IC.tray = null; if (!ok()) return;
  // 플레이어 들어옴
  iwalk(ME, 14.4, 9.6, 2000); await sleep(1200); if (!ok()) return;
  emo(M, '!', '#FFE9A0'); M.dir = 10; M.jump = true; await bub(M, '어, 왔다!', 1000); M.jump = false; await sleep(900); if (!ok()) return;
  ME.dir = 15;
  if (!await ms('마침 잘 왔어! 오늘부터 과자 교실 오븐을 다 같이 쓰기로 했거든.')) return;
  if (!await ms('쿠키 구워서 예쁜 상자에 담고, 리본 묶어서 주고 싶은 사람한테 선물하는 거야. 재밌겠지?')) return;
  if (!await ms('쿠키 구워 본 적 없지? 괜찮아. 제일 쉬운 걸로 같이 해 보자. 버터 동그라미 쿠키!')) return;
  // 1 반죽
  await Promise.all([iwalk(M, 18.7, 6.6, 900), iwalk(ME, 16.4, 8.8, 900)]); M.dir = 10; ME.dir = 5; IC.bowl = 1; await sleep(300); if (!ok()) return;
  if (!await ms('먼저 반죽. 밀 이삭 가루에 달걀 하나, 염소젖 조금.')) return;
  const t = (performance.now() - IC.t0) / 1000; [[3, -20], [0, -6], [1, 8]].forEach(([i, dx], k) => IC.fly.push({ i, t0: t + k * .35, dur: .7, x0: CT[0] + dx, y0: CT[1] - 34 }));
  await sleep(1500); if (!ok()) return;
  IC.bowl = 2; IC.flour = 1; IC.dough = 1; word('촵촵', CT[0], CT[1] - 12, '#FFFFFF', true, 1200); M.nod = true; await sleep(700); word('촵촵', CT[0] + 6, CT[1] - 14, '#FFFFFF', true, 1200); await sleep(900); IC.bowl = 1; IC.flour = 0; M.nod = false; if (!ok()) return;
  await bub(ME, '촵촵.......', 1100); if (!ok()) return;
  // 2 모양 틀
  if (!await ms('반죽 다 됐다. 다음은 틀! 동그라미는 제일 쉬워. 꾹 눌렀다가.......')) return;
  IC.tray = { b: 0 }; IC.dough = 0; word('뿅!', CT[0] + 18, CT[1] - 4, '#FFB0C8', true, 1000); IC.shake = 120; await sleep(1100); if (!ok()) return;
  if (!await ms('뿅! 봐, 벌써 쿠키 같지?', 900)) return;
  // 3 오븐
  IC.tray = null; ME.carry = { b: 0 }; await Promise.all([iwalk(M, 14.8, 1.3, 1500), iwalk(ME, 17.7, 1.7, 1500)]); M.dir = 5; ME.dir = 5; if (!ok()) return;
  ME.carry = null; ME.dir = 10; word('쏙', OVEN[0], OVEN[1] - 4, '#FFE9A0', false); IC.glow = 1.5; await sleep(600); M.dir = 15;
  if (!await ms('이제부터가 진짜야. 노릇노릇해질 때 딱 꺼내야 해. 너무 일찍도, 너무 늦게도 안 돼.')) return;
  await bub(ME, '지금?', 900); if (!ok()) return;
  await bub(M, '....조금만 더.', 1300); if (!ok()) return;
  await bub(M, '....지금!', 700); if (!ok()) return;
  word('띵!', OVEN[0], OVEN[1] - 6, '#FFE9A0', true, 1100); IC.glow = 1; M.dir = 5; await sleep(500); M.carry = { b: 66 }; M.dir = 15; await sleep(700); if (!ok()) return;
  // 4 맛보기
  M.nod = true; await sleep(800); M.nod = false; emo(M, '♥', '#FF9EC0', 1200);
  if (!await ms('음.... 합격! 처음인데 엄청 잘 구웠다. 가장자리 색 봐, 완전 노릇해.')) return;
  M.carry = null;
  if (!await ms('오늘부터 과자 교실 오븐은 마음대로 써. 맛도 바꾸고, 모양도 바꾸고, 아이싱으로 그림도 그리고.')) return;
  await famCard(`<div class="rcard"><canvas id="rccv2" width="72" height="72"></canvas><div><b>쿠키 틀 세트 · 쿠키 도감</b><p>과자 교실 오븐을 쓸 수 있어요. 처음 구운 쿠키는 도감에 남아요.</p><small>버터 동그라미 쿠키 · 도감 1 / 50</small></div></div>`, { f: 'butter', s: 'circle', b: 66 }); if (!ok()) return;
  if (!await ms('도감 다 채우면.... 나도 아직 못 본 쿠키가 나올지도 몰라. 그건 꼭 나한테 제일 먼저 보여 줘.')) return;
  // 마들렌 쿠키가 탈 뻔
  IC.smoke = 1.6; await sleep(900); if (!ok()) return;
  emo(M, '!', '#FF8A8A', 1000); M.sweat = true; await bub(M, '아, 맞다. 내 쿠키!', 1000); if (!ok()) return;
  M.dir = 5; M.jump = true; word('후다닥', OVEN[0] - 10, OVEN[1] + 6, '#FFE9A0', false, 800); await sleep(800); M.jump = false; IC.smoke = .3; M.carry = { b: 84 }; M.dir = 15; await sleep(500); if (!ok()) return;
  if (!await ms('휴, 살았다. ....가장자리만 살짝 탔네. 이건 내가 먹을게. 비밀이야.')) return;
  M.sweat = false; IC.smoke = 0;
  itoast('이제 과자 교실 오븐에서 쿠키를 구울 수 있어요'); await sleep(2200);
  if (run !== introRun) return; $('#cine').hidden = true; IC = null; render();
}
