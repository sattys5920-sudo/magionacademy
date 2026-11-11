// 시련의 탑 층 카드에서 스킬 세트 바꾸기 · 스킬 트리 고치고 돌아오기 검사
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.tw = { ctl: { open: true, at: 1 } };
seed.players.me1.tw = { best: 3, seen: 1, d: '', n: 0, rw: {} };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 }, cur: 0, ps: { 0: { n: '탑용', sk: { '0_0': 1, '0_1': 1, '1_0': 2 }, sp: { atk: 3 } } },
  jo: { job: 'elemental', exp: 9000, xv: 3, sk: { '0_0': 1 }, ps: { 1: { n: '광역', sk: { '0_0': 1, '1_0': 1 }, sp: {} } } } };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await p.evaluate(() => __tw.TW().card(4)); await p.waitForTimeout(400);
  const btns = await p.evaluate(() => [...document.querySelectorAll('#twv [data-twps]')].map(b => b.textContent));
  ok(btns.join(',') === '탑용,광역', '층 카드에 1차 · 2차 세트 버튼 ' + btns);
  await p.screenshot({ path: __dirname + '/shot_t_preset.png' });
  await p.click('#twv [data-twps="0:0"]'); await p.waitForTimeout(400);
  ok(await ev("xEx().sk['1_0'] === 2 && xEx().sp.atk === 3"), '1차 「탑용」으로 바뀌어요');
  await p.click('#twv [data-twps="1:1"]'); await p.waitForTimeout(400);
  ok(await ev("xEx().jo.sk['1_0'] === 1 && xEx().job === 'knight'"), '쉬는 2차 세트도 바로 바꿔 둬요 (지금 직업은 그대로)');
  ok(await p.evaluate(() => /4 층/.test(document.querySelector('#twv .hd b').textContent)), '바꾼 뒤에도 그 층 카드에 있어요');
  await p.click('#twv [data-twtree]'); await p.waitForTimeout(800);
  ok(await p.evaluate(() => !document.getElementById('twv') && !!document.getElementById('tok')), '「스킬 트리 고치기」 → 스킬 트리');
  await p.click('#tok'); await p.waitForTimeout(600);
  ok(await p.evaluate(() => /4 층/.test((document.querySelector('#twv .hd b') || {}).textContent || '')), '돌아가기 → 다시 4 층 카드');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
