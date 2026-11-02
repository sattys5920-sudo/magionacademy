// ===== 시작 연출: 과자 교실 · 마들렌이 오븐 앞에서 리본만 고르다가 쿠키를 다 태움 → 플레이어가 들어옴 → 같이 굽자 · 레시피 카드
const CM = { OX: 164, OY: 82 };
const IZ = 3;
let IC = null;
const ctp = (x, y) => [CM.OX + (x - y) * 8, CM.OY + (x + y) * 4];
const OVEN = [288, 131];
function introStart(){
  const o = $('#cine'); o.hidden = false;
  const cw = document.querySelector('.cwrap'), cc = $('#ccv'); cc.width = cw.clientWidth; cc.height = cw.clientHeight;
  IC = { t0: performance.now(), me: { x: 10.6, y: 10.6, dir: 15, row: 11 }, mad: { x: 15.3, y: 1.9, dir: 5, row: 7, bob: true }, smoke: 0, puffs: [], last: 0, bang: null, shake: 0, bub: null, cloud: 0, emo: null, skip: false };
  requestAnimationFrame(introLoop);
}
function introLoop(now){
  if (!IC) return; requestAnimationFrame(introLoop);
  const c = $('#ccv'), q = c.getContext('2d'); q.imageSmoothingEnabled = false; const t = (now - IC.t0) / 1000;
  const sh = IC.shake > 0 ? Math.random() * 6 - 3 : 0; IC.shake = Math.max(0, IC.shake - 16);
  const fx = 256, fy = 140, ox = fx - c.width / IZ / 2 + sh, oy = fy - c.height / IZ * .5;
  const S = (px, py) => [(px - ox) * IZ, (py - oy) * IZ], W2 = (x, y) => S(...ctp(x, y));
  q.fillStyle = '#120C18'; q.fillRect(0, 0, c.width, c.height);
  if (CANDY.complete) q.drawImage(CANDY, -ox * IZ, -oy * IZ, CANDY.width * IZ, CANDY.height * IZ);
  // 오븐 불빛
  const [gx, gy] = S(...OVEN); q.fillStyle = `rgba(255,${IC.smoke > 1 ? 80 : 150},40,${.18 + Math.sin(t * 8) * .05 + IC.smoke * .08})`; q.beginPath(); q.arc(gx, gy + 6 * IZ, 16 * IZ, 0, 7); q.fill();
  // 연기
  if (IC.smoke > 0 && now - IC.last > 140 / IC.smoke){ IC.last = now; IC.puffs.push({ x: OVEN[0] + (Math.random() * 8 - 4), y: OVEN[1], vx: -2 - Math.random() * 4, vy: -6 - Math.random() * 5, r: 2 + Math.random() * 2, t0: t, dark: IC.smoke > 1.2 }); }
  IC.puffs = IC.puffs.filter(p => t - p.t0 < 3.2);
  IC.puffs.forEach(p => { const a = t - p.t0, [px, py] = S(p.x + p.vx * a, p.y + p.vy * a), r = (p.r + a * 3) * IZ; q.fillStyle = p.dark ? `rgba(48,40,44,${.75 - a * .22})` : `rgba(200,196,200,${.6 - a * .18})`; q.fillRect(Math.round(px - r), Math.round(py - r), Math.round(r * 2), Math.round(r * 2)); q.fillStyle = p.dark ? `rgba(80,70,74,${.5 - a * .15})` : `rgba(240,236,240,${.4 - a * .12})`; q.fillRect(Math.round(px - r * .5), Math.round(py - r * .9), Math.round(r), Math.round(r * .6)); });
  // 사람들
  [IC.me, IC.mad].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(a => {
    const [px, py] = W2(a.x, a.y), hop = a.bob ? Math.abs(Math.sin(t * 6)) * 1.5 * IZ : a.jump ? Math.abs(Math.sin(t * 14)) * 3 * IZ : 0;
    q.fillStyle = 'rgba(0,0,0,.25)'; q.beginPath(); q.ellipse(px, py, 6 * IZ, 2.2 * IZ, 0, 0, 7); q.fill();
    const col = a.walk ? a.dir + 1 + (Math.floor(t * 8) % 4) : a.bob ? a.dir + 1 + (Math.floor(t * 4) % 2) * 2 : a.dir;
    if (SHEET.complete) q.drawImage(SHEET, col * 64, a.row * 64, 64, 64, Math.round(px - 16 * IZ), Math.round(py - 28 * IZ - hop), 32 * IZ, 32 * IZ);
    if (a.tray){ const ty = py - 10 * IZ; q.fillStyle = '#2A1A2E'; q.fillRect(px - 9 * IZ, ty - 1 * IZ, 18 * IZ, 5 * IZ); q.fillStyle = '#A8A8B8'; q.fillRect(px - 8 * IZ, ty, 16 * IZ, 3 * IZ); q.fillStyle = '#2A1C18'; [-6, -1, 4].forEach(dx => q.fillRect(px + dx * IZ, ty - 2 * IZ, 3 * IZ, 2 * IZ)); q.fillStyle = 'rgba(90,80,84,.6)'; q.fillRect(px - 4 * IZ, ty - (6 + (t * 6 % 4)) * IZ, 2 * IZ, 2 * IZ); }
    if (a.sweat){ q.fillStyle = '#9AD4F0'; const dy = (t * 20) % 10; q.fillRect(px + 9 * IZ, py - 26 * IZ + dy, 2 * IZ, 3 * IZ); }
    if (a.tear){ q.fillStyle = '#9AD4F0'; const dy = (t * 14) % 8; q.fillRect(px - 4 * IZ, py - 18 * IZ + dy, IZ, 2 * IZ); q.fillRect(px + 3 * IZ, py - 18 * IZ + (dy + 4) % 8, IZ, 2 * IZ); }
    if (IC.emo && IC.emo.a === a && now < IC.emo.until){ q.font = `${9 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 5; q.strokeStyle = '#3A2414'; q.strokeText(IC.emo.t, px, py - 32 * IZ); q.fillStyle = IC.emo.c || '#FFE9A0'; q.fillText(IC.emo.t, px, py - 32 * IZ); q.textAlign = 'left'; }
  });
  if (IC.cloud > 0){ q.fillStyle = `rgba(40,32,36,${Math.min(.85, IC.cloud)})`; q.fillRect(0, 0, c.width, c.height); IC.cloud = Math.max(0, IC.cloud - .006); }
  if (IC.bang){ q.font = `${12 * IZ}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 7; q.strokeStyle = '#3A2414'; q.strokeText(IC.bang, gx, gy - 6 * IZ); q.fillStyle = '#FFB060'; q.fillText(IC.bang, gx, gy - 6 * IZ); q.textAlign = 'left'; }
  if (IC.bub && now < IC.bub.until){ const [px, py] = W2(IC.bub.a.x, IC.bub.a.y); q.font = '14px G11, sans-serif'; const w = Math.ceil(q.measureText(IC.bub.text).width) + 16, bx = Math.max(4, Math.min(c.width - w - 4, px - w / 2)), by = py - 36 * IZ - 10;
    q.fillStyle = '#22183F'; q.fillRect(bx - 2, by - 2, w + 4, 26); q.fillStyle = '#FFFFFF'; q.fillRect(bx, by, w, 22); q.fillStyle = '#22183F'; q.fillRect(px - 3, by + 24, 6, 2); q.fillText(IC.bub.text, bx + 8, by + 16); }
}
async function iwalk(a, x, y, ms){ const x0 = a.x, y0 = a.y, t0 = performance.now(), dx = x - x0, dy = y - y0, sx = (dx - dy) * 8, sy = (dx + dy) * 4; a.dir = Math.abs(sx) > Math.abs(sy) ? (sx > 0 ? 15 : 10) : (sy > 0 ? 0 : 5); a.walk = true; a.bob = false;
  await new Promise(r => { const f = now => { const k = Math.min(1, (now - t0) / ms); a.x = x0 + dx * k; a.y = y0 + dy * k; if (k < 1 && IC) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); }); a.walk = false; }
function itoast(t){ const el = $('#ctoast'); el.textContent = t; el.classList.add('on'); clearTimeout(itoast.t); itoast.t = setTimeout(() => el.classList.remove('on'), 2400); }
const bub = (a, text, ms = 1600) => { IC.bub = { a, text, until: performance.now() + ms }; return sleep(ms); };
const emo = (a, t, c, ms = 900) => { IC.emo = { a, t, c, until: performance.now() + ms }; };
let introRun = 0;
async function playIntro(){
  const run = ++introRun; introStart(); const M = IC.mad, ME = IC.me;
  const alive = () => run === introRun && IC;
  $('#cskip').onclick = () => { introRun++; IC = null; $('#cine').hidden = true; $('#blsay').style.display = 'none'; };
  await sleep(600); if (!alive()) return;
  itoast('과자 교실에서 달콤한 냄새가 나요'); await bub(M, '흥흥.... 리본은 분홍이 좋을까, 노랑이 좋을까.......', 2200); if (!alive()) return;
  IC.smoke = .6; await bub(M, '아니야, 이 친구는 하늘색이야. 그럼 저 친구는.......', 2200); if (!alive()) return;
  itoast('....아니, 타는 냄새예요'); IC.smoke = 1.6; await sleep(1600); if (!alive()) return;
  IC.bang = '펑!'; IC.shake = 500; IC.cloud = .9; IC.smoke = 2.2; M.bob = false; M.jump = true; emo(M, '!', '#FF8A8A', 1200); await sleep(900); IC.bang = null; if (!alive()) return;
  await bub(M, '콜록, 콜록.... 내 쿠키.......', 1500); M.jump = false; if (!alive()) return;
  M.tray = true; M.dir = 0; IC.smoke = .7; M.tear = true; itoast('쟁반 위 쿠키가 전부 새까맣게 탔어요'); await sleep(1800); if (!alive()) return;
  IC.smoke = .3; await iwalk(ME, 13.3, 4.5, 2200); ME.dir = 15; if (!alive()) return;
  emo(M, '!', '#FFE9A0'); M.dir = 10; await sleep(700); M.tray = false; M.tear = false; M.sweat = true; if (!alive()) return;
  for (const t of ['앗.... 언제부터 거기 있었어요.......', '이거요? ....쿠키예요. 아니, 쿠키였어요.', '반 친구들 한 명 한 명한테 다 다른 쿠키 상자를 만들어 주고 싶었는데.... 오븐 앞에서 리본만 고르다가 다 태워 버렸어요.']){ await say(7, '마들렌', t); if (!alive()) return; }
  M.sweat = false;
  await say(7, '마들렌', '그래서 말인데요.... 같이 구워 줄래요? 혼자 하면 또 리본만 고를 것 같아서요.'); if (!alive()) return;
  await bub(ME, '좋아, 같이 굽자!', 1500); if (!alive()) return;
  emo(M, '♥', '#FF9EC0', 1200); await say(7, '마들렌', '고마워요. 그럼.... 이거 받아요. 원래 당신 상자에 넣으려던 쿠키 레시피예요.'); if (!alive()) return;
  const R = myRec();
  await famCard(`<div class="rcard"><canvas id="rccv2" width="72" height="72"></canvas><div><b>${R.n}</b><p>${R.why}</p><small>${FL.find(f => f.id === R.f).n} 반죽 · ${SH.find(s => s[0] === R.s)[1]} 틀 · ${ICE[R.ice][0]} 아이싱 · ${TOP.find(t => t[0] === R.top)[1]}</small></div></div>`); if (!alive()) return;
  for (const t of ['맛도, 모양도, 위에 올릴 것도.... 다 당신 생각하면서 골랐어요.', '첫 판은 이걸로 같이 구워요. 그다음엔 마음껏 구워서, 주고 싶은 사람한테 상자째 선물해요.', '아, 오븐 볼 때는.... 리본 고르지 말고요.']){ await say(7, '마들렌', t); if (!alive()) return; }
  await sleep(300); if (run !== introRun) return; $('#cine').hidden = true; IC = null; ST.tab = 'note'; render();
}
