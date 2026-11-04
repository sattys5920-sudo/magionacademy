// 레이드 2 단계 시험: 같은 브라우저 창 N 개 = 학생 N 명 (모의 DB가 창끼리 이어져요)
//   node rd_p2_test.js <저장 폴더> <인원> <exp> <돌릴 ms> [low]   low = 시작하자마자 보스 체력 30 % (전체 공격·큰 기술·끊기·이기기 확인)
const { chromium } = require('playwright'); const fs = require('fs');
const base = eval('(' + fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});/)[1] + ')');
const D = process.argv[2], N = +(process.argv[3] || 4), EXP = +(process.argv[4] || 30000), WAIT = +(process.argv[5] || 50000), LOW = process.argv[6] === 'low';
const JOBS = ['knight', 'white', 'black', 'warrior', 'bard', 'thief', 'druid', 'alch', 'summon', 'time', 'cleric', 'gadget'];
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 430, height: 860 }, deviceScaleFactor: 1 }); const errs = [];
  const seed = JSON.parse(JSON.stringify(base)); const p0 = seed.players.me1;
  for (let i = 0; i < N; i++){ const id = 'me' + (i + 1); seed.players[id] = { ...JSON.parse(JSON.stringify(p0)), nick: '학생' + (i + 1), ex: { job: JOBS[i], exp: EXP, xv: 3, n: 0, d: '' }, raid: { seen: 777 } }; }
  seed.raid = { ctl: { open: true, id: 777, at: Date.now() } };
  const P = []; for (let i = 0; i < N; i++){ const p = await ctx.newPage(); p.on('pageerror', e => errs.push(i + ': ' + e.message)); await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, 'me' + (i + 1)]); await p.goto('http://localhost:8822/'); P.push(p); }
  await P[0].waitForTimeout(5000);
  for (const p of P){ await p.evaluate(() => World.teleport('mirrorland', [20, 20])); }
  await P[0].waitForTimeout(1500);
  const tower = async p => { await p.evaluate(() => World.onAct('mirrorland', null, ['거울 탑', '올라가기'])); await p.waitForTimeout(300); await p.click('[data-rdf="1"]'); await p.waitForTimeout(400); };
  await tower(P[0]); await P[0].click('[data-rdl="make"]'); await P[0].waitForTimeout(800);
  for (let i = 1; i < N; i++){ await tower(P[i]); await P[i].click('[data-rdl="join"]'); await P[i].waitForTimeout(600); }
  for (let i = 1; i < N; i++){ if (i === N - 1) await P[i].click('[data-rdl="side"]').catch(() => {}); await P[i].click('[data-rdl="ready"]'); await P[i].waitForTimeout(300); }
  await P[0].waitForTimeout(800); await P[0].screenshot({ path: D + '/p2_lobby.png' }); await P[1].screenshot({ path: D + '/p2_lobby_m.png' });
  await P[0].click('[data-rdl="start"]'); await P[0].waitForTimeout(6500);
  for (const p of P) await p.evaluate(() => { setInterval(() => {   // 자동으로 누르기: 빠른 스킬 → 공격 · 대상 카드 · 피하기는 고리에 닿을 때
    const pk = document.querySelector('#xstat .xs.xpick'); if (pk){ pk.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); return; }
    const q = [...document.querySelectorAll('#xcmd .xb.xq:not([disabled])')]; const b = q.length && Math.random() < .7 ? q[Math.floor(Math.random() * q.length)] : document.querySelector('#xcmd [data-xc="atk"]'); if (b) b.click();
    const c = document.querySelector('#xcmd [data-xc="cancel"]'); if (c && Math.random() < .2) c.click(); }, 400);
    setInterval(() => { const o = document.querySelector('#rddg .o'), btn = document.querySelector('#rddg button'); if (!o || !btn || btn.dataset.done) return; const m = o.style.transform.match(/scale\(([\d.]+)/), s = m ? parseFloat(m[1]) : 9; if (s <= 1.03 && Math.random() < .8){ btn.dataset.done = 1; btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); } }, 30); });
  console.log('L', await P[0].evaluate(() => window.__T.xbGet() && window.__T.xbGet().party.map(u => u.L).join(',')));
  await P[0].screenshot({ path: D + '/p2_host_0.png' }); await P[1].screenshot({ path: D + '/p2_mem_0.png' });
  if (LOW) await P[0].evaluate(() => { const B = window.__T.xbGet(); B.foes[0].hp = Math.round(B.foes[0].mhp * .3); });
  let shot = 0, big = 0, all = 0; const t0 = Date.now();
  while (Date.now() - t0 < WAIT){ await P[0].waitForTimeout(1500);
    const st = await P[0].evaluate(() => { const B = window.__T.xbGet(); if (!B) return null; return { hp: B.foes[0] && Math.round(B.foes[0].hp / B.foes[0].mhp * 100), alive: B.party.filter(u => u.hp > 0).length, tele: B.raid && B.raid.tele && B.raid.tele.k, over: B.over, log: B.log }; });
    const ms = await P[1].evaluate(() => { const B = window.__T.xbGet(); return B ? { hp: B.foes[0] && Math.round(B.foes[0].hp / B.foes[0].mhp * 100), dg: !!document.querySelector('#rddg') } : null; });
    if (st && (st.tele || /끊|「/.test(st.log) || st.over)) console.log(Math.round((Date.now() - t0) / 1000), JSON.stringify(st), JSON.stringify(ms));
    if (ms && ms.dg && shot < 1){ await P[1].screenshot({ path: D + '/p2_dodge.png' }); shot++; }
    if (st && st.tele === 'big' && big < 2){ await P[1].screenshot({ path: D + '/p2_big_' + big + '.png' }); big++; }
    if (st && st.tele === 'all' && all < 1){ await P[0].screenshot({ path: D + '/p2_all.png' }); all++; }
    if (LOW && Date.now() - t0 > 45000) await P[0].evaluate(() => { const B = window.__T.xbGet(); if (B && B.foes[0].hp > 50) B.foes[0].hp = 50; });
    if (!st || st.over) break; }
  await P[0].waitForTimeout(1500); await P[0].screenshot({ path: D + '/p2_host_end.png' }); await P[1].screenshot({ path: D + '/p2_mem_end.png' });
  console.log('room', await P[0].evaluate(() => JSON.stringify(window.__tree.raid && window.__tree.raid.room && Object.values(window.__tree.raid.room).map(r => [r.st, r.win]))));
  console.log('count', await P[1].evaluate(() => JSON.stringify(window.__T.me().raid)));
  if (fs.existsSync(D + '/p2_mem_end.png')){ await P[1].click('#rdout').catch(() => {}); await P[1].waitForTimeout(800); console.log('after out', await P[1].evaluate(() => [World.where(), !!window.__T.xbGet()].join(' '))); }
  console.log('errs', JSON.stringify(errs.slice(0, 10))); await b.close(); })();
