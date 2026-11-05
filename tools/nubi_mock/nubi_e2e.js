// 누비 이벤트 끝까지 돌려 보기: 같은 브라우저 창 N 개 = 학생 N 명 (모의 DB가 창끼리 이어져요)
//   node tools/nubi_mock/nubi_e2e.js <저장 폴더> [인원 2] [포트 8822]
const { chromium } = require('playwright'); const fs = require('fs');
const base = eval('(' + fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});/)[1] + ')');
const D = process.argv[2] || '.', N = +(process.argv[3] || 2), PORT = process.argv[4] || 8822;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const key = dd => { const d = new Date(Date.now() - dd * 864e5); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 430, height: 860 }, deviceScaleFactor: 1 }); const errs = [];
  const seed = JSON.parse(JSON.stringify(base)); const p0 = seed.players.me1; const ids = [];
  for (let i = 0; i < N; i++){ const id = 'me' + (i + 1); ids.push(id); seed.players[id] = { ...JSON.parse(JSON.stringify(p0)), nick: ['하린', '도윤', '서아', '지호'][i] }; seed.players[id].inv = { ...(seed.players[id].inv || {}), d_pseedsoup: 2 }; }
  seed.nubi = { ctl: { open: true, id: 777, d0: key(9), ids } };
  const P = []; for (let i = 0; i < N; i++){ const p = await ctx.newPage(); p.on('pageerror', e => errs.push(i + ': ' + e.message)); p.on('console', m => { if (m.type() === 'error' && /nubi|누비/.test(m.text())) errs.push(i + ' console: ' + m.text().slice(0, 200)); });
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; window.__nbAuto = true;
      setInterval(() => { const s2 = document.getElementById('nbsay'); if (s2 && s2.style.display === 'block') s2.click(); const pk = document.querySelector('#nbpick'); if (pk && pk.style.display === 'flex'){ const bs = pk.querySelectorAll('button'); bs[bs.length > 1 ? 0 : 0].click(); } }, 90); }, [seed, ids[i]]);
    await p.goto(`http://localhost:${PORT}/`); P.push(p); }
  await sleep(6000);
  const T = p => p.evaluate(() => JSON.parse(JSON.stringify(window.__T.me().nubi || null)));
  const waitS = async (p, f, ms = 60000) => { const t0 = Date.now(); while (Date.now() - t0 < ms){ const t = await T(p); if (t && f(t)) return t; await sleep(400); } throw new Error('기다림 초과: ' + f + ' ' + JSON.stringify(await T(p)).slice(0, 300)); };
  const room = p => p.evaluate(() => World.teleport('old_infirmary', [9, 11]));
  const tap = p => p.evaluate(() => World.onProp('nubi'));
  const sera = async p => { await p.evaluate(() => World.teleport('lab', [8, 11])); await sleep(1500); await p.evaluate(() => World.onNpc('sera')); await sleep(600); await p.click('[data-nx="nbsera"]', { timeout: 4000 }); };
  const shot = async (p, n) => p.screenshot({ path: D + '/nb_' + n + '.png' });
  // 책장 문으로 들어가요 (첫 학생은 문으로, 나머지는 바로)
  for (const [i, p] of P.entries()){
    await p.evaluate(() => World.teleport('lab', [1, 3])); await sleep(1800); await shot(p, 'lab_' + i);
    const ok = await p.evaluate(() => World.enterDoorAt(0, 2)); console.log('door', i, ok); await sleep(2500);
    await waitS(p, t => t.s === 0); console.log('intro done', i);
  }
  await shot(P[0], 'room');
  for (const [i, p] of P.entries()){
    // 1 일째
    await p.evaluate(() => World.teleport('craft', [12, 16])); await sleep(1500); await p.evaluate(() => World.onProp('nbbtn')); await room(p); await sleep(1500); await tap(p); await waitS(p, t => t.s === 1);
    // 2 일째: 어깨에 태우고 다섯 군데
    await tap(p); await sleep(1500);
    for (const m of ['town', 'toxic', 'barn', 'library', 'classroom']){ await p.evaluate(m => World.teleport(m, null), m); await sleep(2200); if (i === 0 && m === 'town') await shot(p, 'ride'); }
    await room(p); await waitS(p, t => t.s === 2);
    // 3 일째
    await tap(p); await sleep(2500); for (const k of [0, 1, 2]){ await p.evaluate(k => World.onProp('nbdust' + k), k); await sleep(200); } await waitS(p, t => t.s === 3);
    // 4 일째: 꿰매기
    await tap(p); if (i === 0){ await sleep(1800); await shot(p, 'sew'); } await waitS(p, t => t.s === 4);
    // 5 일째: 한밤의 이름 (반 날짜가 6 일째를 넘었으니 바로)
    await waitS(p, t => t.s === 5);
    // 6 일째
    await sera(p); await waitS(p, t => t.sr6); await room(p); await sleep(1500); await tap(p); await waitS(p, t => t.s === 6);
    // 7 일째: 터진 날 → 솜
    await room(p); await waitS(p, t => t.b7); await p.evaluate(() => World.onProp('nbcot')); await room(p); await sleep(1200); await tap(p); await waitS(p, t => t.cot);
    console.log('cot', i, await p.evaluate(() => document.querySelector('#toast')?.textContent || ''));
  }
  for (const [i, p] of P.entries()){ const t = await waitS(p, t => t.rev && t.s === 7, 90000); console.log('reveal', i, Object.keys(t.bad || {}).length); }
  for (const [i, p] of P.entries()){
    await room(p); await waitS(p, t => t.n8); await sera(p); await waitS(p, t => t.sr8); await room(p); await sleep(1500); await tap(p); await waitS(p, t => t.s === 8);
    await tap(p); if (i === 0){ await sleep(2200); await shot(p, 'unpick'); } await waitS(p, t => t.un);
  }
  for (const [i, p] of P.entries()){ const t = await waitS(p, t => t.fin, 90000); console.log('fin', i, t.s, await p.evaluate(() => [window.__T.me().inv.nb_heart, (window.__T.me().fbag || {}).nubidoll])); }
  for (const p of P){ await sera(p); await waitS(p, t => t.thr); }
  for (const [i, p] of P.entries()){ const t = await waitS(p, t => t.gy, 90000); console.log('gy', i); }
  await P[0].evaluate(() => World.teleport('lab', [1, 3])); await sleep(1500); await P[0].evaluate(() => World.enterDoorAt(0, 2)); await sleep(3000); await shot(P[0], 'warm');
  console.log('where', await P[0].evaluate(() => World.where()));
  const errTree = await P[0].evaluate(() => JSON.stringify(window.__tree && window.__tree.errs || {}).slice(0, 600));
  console.log('errs', JSON.stringify(errs.slice(0, 12)), 'tree errs', errTree); await b.close(); })().catch(e => { console.error('FAIL', e.message); process.exit(1); });
