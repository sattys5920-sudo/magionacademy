// 시련의 탑 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/tower/tower_test.js
//   탑 열림 · 창 · 층 카드 · 직업 고르기 (2차로 바꾸기) · 이기면 기록과 첫 보상 · 지면 기록 그대로 · 하루 3 번 · 부류 효과 · 관리자 카드
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 }, cur: 0, jo: { job: 'elemental', exp: 9000, xv: 3, sk: { '0_0': 1 } } };
seed.tw = { ctl: { open: true, at: 1 } };
(async () => {
  const b = await chromium.launch(), errs = [];
  const page = async (u, opt) => { const ctx = await b.newContext(opt), p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3500);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const p = await page('me1', { ...devices['iPhone 13'] }), C = (f, a) => p.evaluate(f, a);
  await p.waitForTimeout(2500);
  ok(await C(() => __tw.TW().open()), '관리자가 열면 탑이 열려요');
  await C(() => World.onProp('tower')); await p.waitForTimeout(500);
  const w0 = await C(() => ({ n: document.querySelectorAll('#twv .fl').length, now: (document.querySelector('#twv .fl.now') || {}).textContent, lock: document.querySelectorAll('#twv .fl.lock').length, left: (document.querySelector('#twv .tag') || {}).textContent }));
  ok(w0.n === 50 && /1 층/.test(w0.now) && w0.lock === 49 && /3 \/ 3/.test(w0.left), '탑 창: 50 층 · 1 층 도전 · 나머지 잠김 · 오늘 3 / 3 ' + JSON.stringify(w0));
  await p.screenshot({ path: __dirname + '/shot_t_tower.png' });
  await C(() => document.querySelector('#twv .fl.now').click()); await p.waitForTimeout(400);
  const c1 = await C(() => ({ pk: [...document.querySelectorAll('#twv [data-twgo]')].map(b => b.innerText.replace(/\n/g, ' ')), rw: document.querySelector('#twv .rw').innerText }));
  ok(c1.pk.length === 2 && /1차 기사/.test(c1.pk[0]) && /2차 정령술사/.test(c1.pk[1]) && /골드 240/.test(c1.rw), '층 카드: 1차 · 2차 버튼 · 첫 보상 ' + JSON.stringify(c1));
  await p.screenshot({ path: __dirname + '/shot_t_card.png' });
  // 2차로 도전 → 직업이 바뀌고 전투가 시작돼요
  const coin0 = await C(() => __tw.jobs() && window.__T.meGet().coin);
  await C(() => document.querySelector('#twv [data-twgo="1"]').click()); await p.waitForTimeout(1500);
  const b1 = await C(() => { const B = __tw.xb(); return B && { tw: B.tw, foes: B.foes.map(f => ({ n: f.name, tw: Object.keys(f.tw), hp: f.mhp, lp: f.lp })), job: B.party[0].job, title: (document.querySelector('.panel h2,.panel .ttl,.panel b') || {}).textContent }; });
  ok(b1 && b1.tw.f === 1 && b1.job === 'elemental' && b1.foes.length && b1.foes.every(f => f.tw.length), '2차로 고르면 직업이 바뀌고 탑 전투가 시작돼요 ' + JSON.stringify(b1));
  await p.waitForTimeout(800); await p.screenshot({ path: __dirname + '/shot_t_battle.png' });
  await C(() => { const B = __tw.xb(); B.foes.forEach(f => { f.hp = 0; }); }); await p.waitForTimeout(2500);
  const r1 = await C(() => ({ log: (document.getElementById('xlog') || {}).textContent, btn: (document.getElementById('xnext') || {}).textContent, s: JSON.parse(JSON.stringify(__tw.TW().S())), coin: window.__T.meGet().coin }));
  ok(r1.s.best === 1 && r1.s.n === 1 && /1 층 돌파/.test(r1.log) && r1.coin === coin0 + 240 && /탑으로/.test(r1.btn), '이기면 1 층 기록 · 골드 +240 · 도전 1 번 ' + JSON.stringify(r1));
  await C(() => document.getElementById('xnext').click()); await p.waitForTimeout(500);
  ok(await C(() => /1 층 돌파/.test((document.querySelector('#twv') || {}).innerText || '')), '첫 돌파 결과 창');
  await p.screenshot({ path: __dirname + '/shot_t_clear.png' });
  await C(() => document.querySelector('#twv [data-twok]').click()); await p.waitForTimeout(400);
  ok(await C(() => /2 층/.test(document.querySelector('#twv .fl.now').textContent) && document.querySelectorAll('#twv .fl.done').length === 1), '다음 층(2 층)이 열려요');
  // 지기
  await C(() => __tw.TW().go(2, 0)); await p.waitForTimeout(1200);
  ok(await C(() => __tw.xb().party[0].job === 'knight'), '1차로 고르면 다시 기사로 바뀌어요');
  await C(() => { const B = __tw.xb(); B.party.forEach(u => { u.hp = 0; }); }); await p.waitForTimeout(2500);
  const r2 = await C(() => ({ log: (document.getElementById('xlog') || {}).textContent, s: JSON.parse(JSON.stringify(__tw.TW().S())) }));
  ok(r2.s.best === 1 && r2.s.n === 2 && /쓰러졌어요/.test(r2.log), '지면 기록은 그대로 · 도전은 줄어요 ' + JSON.stringify(r2));
  await C(() => document.getElementById('xnext').click()); await p.waitForTimeout(500);
  await C(() => __tw.TW().go(2, 0)); await p.waitForTimeout(800); await C(() => { const B = __tw.xb(); B.party.forEach(u => { u.hp = 0; }); }); await p.waitForTimeout(2500); await C(() => document.getElementById('xnext').click()); await p.waitForTimeout(500);
  await C(() => __tw.TW().card(2)); await p.waitForTimeout(300);
  const c3 = await C(() => ({ dis: [...document.querySelectorAll('#twv [data-twgo]')].every(b => b.disabled), t: document.querySelector('#twv .card').innerText }));
  ok(c3.dis && /오늘 도전을 다 썼어요/.test(c3.t), '하루 3 번을 다 쓰면 못 올라가요');
  await C(() => __tw.TW().go(2, 0)); ok(await C(() => !__tw.xb()), '도전이 없으면 전투가 시작되지 않아요');
  // 층 구성 · 부류 효과
  const fl = await C(() => [1, 7, 12, 13, 20, 37, 50].map(f => ({ f, foes: __tw.twFoes(f).map(x => x.name + ':' + Object.keys(x.tw).join('+') + ':' + x.mhp + '/' + x.atk) })));
  ok(fl.find(x => x.f === 20).foes.length === 1 && /탑지기 석상/.test(fl.find(x => x.f === 20).foes[0]) && fl.find(x => x.f === 13).foes.length >= 2, '층 구성: 10 층마다 보스 · 13 층부터 두 부류 ' + JSON.stringify(fl));
  // 부류 효과 (전투 코드 xHit · xAct 를 그대로 불러요)
  const fx = await C(() => { const T = __tw, P = () => ({ id: 'p0', team: 'a', name: '나', hp: 1000, mhp: 1000, mp: 100, mmp: 100, atk: 100, mag: 10, crit: 0, fx: {}, g: 0, L: 30, job: 'knight' });
    const foe = k => Object.assign(T.twFoes(1)[0], { id: 'e0', tw: { [k]: 1 }, hp: 1e6, mhp: 1e6, atk: 50 });
    const set = (pa, fo) => T.setXb({ party: pa, foes: fo, kind: 'elite', log: '', def: {}, fxs: [], floats: [], proj: [], n0: 1, over: false });
    const o = {};
    { const u = P(), e = foe('armor'); set([u], [e]); o.armorPh = T.xHit(u, e, 100, '#fff', { st: 'atk' }); o.armorMag = T.xHit(u, e, 100, '#fff', { st: 'mag' }); }
    { const u = P(), e = foe('swift'); set([u], [e]); let z = 0; for (let i = 0; i < 600; i++) if (T.xHit(u, e, 100, '#fff', { st: 'atk' }) === 0) z++; o.swift = z / 600; }
    { const u = P(), e = foe('mirror'); set([u], [e]); T.xHit(u, e, 100, '#fff', { st: 'atk' }); o.mirror = 1000 - u.hp; }
    { const u = P(), e = foe('drain'); set([u], [e]); T.xHit(e, u, 50, '#f00'); o.drain = 100 - u.mp; }
    { const u = P(), e = foe('regen'); e.hp = 5e5; set([u], [e]); e.g = 100; T.xAct(e); o.regen = e.hp - 5e5; }
    { const u = P(), e = foe('rage'); e.atk = 100; set([u], [e]); const hits = []; for (let i = 0; i < 8; i++){ const h0 = u.hp; e.g = 100; T.xAct(e); hits.push(h0 - u.hp); u.hp = 1000; } o.rage = hits; }
    T.setXb(null); return o; });
  ok(fx.armorPh === 60 && fx.armorMag === 100, '철갑: 물리 40 % 덜 · 마법 그대로 ' + JSON.stringify([fx.armorPh, fx.armorMag]));
  ok(fx.swift > .25 && fx.swift < .42, '날쌘: 셋 중 하나쯤 피해요 ' + fx.swift.toFixed(2));
  ok(fx.mirror === 30, '반사: 30 % 되돌려요 ' + fx.mirror);
  ok(fx.drain === 12, '마나 먹기: 맞으면 MP 12 % ' + fx.drain);
  ok(fx.regen === 7e4, '재생: 차례마다 7 % ' + fx.regen);
  ok(fx.rage.slice(0, 5).every(h => h > 0 && h < 140) && fx.rage.slice(6).every(h => h > 150), '광폭: 6 번째부터 두 배 ' + JSON.stringify(fx.rage));
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  // 관리자 카드
  const ad = await page('admin', { viewport: { width: 1000, height: 900 } });
  await ad.evaluate(() => __T.showAdmin()); await ad.waitForTimeout(1500); await ad.evaluate(() => window.__adPoll && window.__adPoll()); await ad.waitForTimeout(800);
  await ad.evaluate(() => [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent).click()); await ad.waitForTimeout(1500);
  const card = await ad.evaluate(() => { const c = [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('시련의 탑')); if (!c) return ''; if (c.classList.contains('shut')) c.querySelector('.abhead b').click(); return [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('시련의 탑')).innerText; });
  ok(/열려 있어요/.test(card) && /탑 닫기/.test(card), '관리자 카드: 열림 · 닫기 버튼 ' + card.slice(0, 120).replace(/\n/g, ' / '));
  ok(!errs.length, '페이지 오류 없음 (관리자) ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
