// 스킬 · 스탯 세트 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/newjobs/test/preset_test.js
//   세 칸 · 이름 정해 저장 · 바꾸면 그대로 돌아와요 · 1차 / 2차 따로 · 탐사 중에는 못 바꿔요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1, '0_1': 1, '1_0': 1 }, sp: { atk: 3 }, cur: 0, jo: { job: 'elemental', exp: 9000, xv: 3, sk: { '0_0': 1 } } };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const C = (f, a) => p.evaluate(f, a), E = () => C(() => JSON.parse(JSON.stringify(__T.xEx_())));
  await C(() => __T.openSheet('home', 'explore')); await p.waitForTimeout(800); await C(() => document.querySelector('#xtree').click()); await p.waitForTimeout(800);
  ok(await C(() => document.querySelectorAll('.xps [data-xps]').length === 3), '스킬 트리 위 세트 세 칸');
  await C(() => document.querySelector('[data-xps="0"]').click()); await p.waitForTimeout(400);
  await C(() => { document.getElementById('nbIn').value = '레이드용'; }); await p.keyboard.press('Enter'); await p.waitForTimeout(300);
  if (await C(() => !!document.getElementById('nbIn'))) await C(() => [...document.querySelectorAll('#confirm button')].find(b => /확인|좋아요|저장|네/.test(b.textContent)).click());
  await p.waitForTimeout(500);
  let e = await E(); ok(e.ps && e.ps[0] && e.ps[0].n === '레이드용' && e.ps[0].sk['0_1'] === 1 && e.ps[0].sp.atk === 3, '이름 정해 저장 ' + JSON.stringify(e.ps));
  ok(await C(() => /레이드용/.test(document.querySelector('.xps').innerText)), '칸에 이름이 보여요');
  await p.screenshot({ path: __dirname + '/../shots/preset_tree.png' });
  await C(() => { const x = __T.xEx_(); x.sk = { '0_0': 1, '2_0': 1, '2_1': 1 }; x.sp = { hp: 3 }; });
  await C(() => document.querySelector('[data-xps="0"]').click()); await p.waitForTimeout(400);
  await C(() => document.querySelector('[data-psa="load"]').click()); await p.waitForTimeout(500);
  e = await E(); ok(e.sk['0_1'] === 1 && !e.sk['2_0'] && e.sp.atk === 3 && !e.sp.hp, '세트로 바꾸면 그대로 돌아와요 ' + JSON.stringify([e.sk, e.sp]));
  await C(() => document.querySelector('.x2tab [data-x2="1"]').click()); await p.waitForTimeout(800);
  e = await E(); ok(e.job === 'elemental' && !e.ps && e.jo.ps && e.jo.ps[0].n === '레이드용', '2차는 세트가 따로예요');
  await C(() => document.querySelector('.x2tab [data-x2="0"]').click()); await p.waitForTimeout(600);
  await C(() => { __T.xEx_().run = { rg: 0, loot: { gold: 0, exp: 0, items: {} }, start: Date.now(), end: Date.now() + 6e5, prog: 0 }; __T.xEx_().sk = { '0_0': 1 }; });
  await C(() => document.querySelector('[data-xps="0"]') ? document.querySelector('[data-xps="0"]').click() : 0); await p.waitForTimeout(300);
  await C(() => { const b = document.querySelector('[data-psa="load"]'); if (b) b.click(); }); await p.waitForTimeout(300);
  e = await E(); ok(!e.sk['0_1'], '탐사 중에는 못 바꿔요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
