// 스킬 트리 「−1」 · 「최소로」 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/skill_down_test.js
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 3, '0_1': 4, '1_0': 2 }, qs: ['0_1', null, null, null] }; seed.players.me1.coin = 5000;
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s), sel = async k => { await p.click(`[data-ts="${k}"]`); await p.waitForTimeout(300); };
  await ev("(xv = { view: 'tree', sel: '0_0' }, openSheet('home', 'explore'))"); await p.waitForTimeout(800);
  const pts0 = await ev('xPts(xEx())');
  await sel('0_0'); ok(await p.evaluate(() => /−1 · 100G/.test(document.getElementById('tdn').textContent) && /최소로 \(−2/.test((document.getElementById('tmin') || {}).textContent || '')), '첫 스킬 Lv 3: −1 · 최소로 (−2) (Lv 1 까지)');
  await p.click('#tdn'); await p.waitForTimeout(400);
  ok(await ev("xEx().sk['0_0'] === 2 && me.coin === 4900") && (await ev('xPts(xEx())')) === pts0 + 1, '−1 → Lv 2 · 100G · 포인트 +1');
  await sel('0_1'); ok(await p.evaluate(() => /최소로 \(−4 · 400G\)/.test(document.getElementById('tmin').textContent)), '다음 칸을 안 배운 스킬은 0 까지 (−4)');
  await p.click('#tmin'); await p.waitForTimeout(400); await p.click('#cfOk').catch(() => {}); await p.waitForTimeout(500);
  ok(await ev("!xEx().sk['0_1'] && me.coin === 4500 && !(xEx().qs || []).includes('0_1')"), '최소로 → 배우기 전 · 400G · 빠른 칸에서도 빠져요');
  await sel('1_0'); await p.click('#tdn'); await p.waitForTimeout(300);
  ok(await ev("xEx().sk['1_0'] === 1"), '다른 줄 스킬도 −1');
  await ev("(xEx().sk['1_1'] = 1, renderExplore())"); await p.waitForTimeout(300); await sel('1_0');
  ok(await p.evaluate(() => document.getElementById('tdn').disabled && /다음 칸을 배워서 Lv 1 까지/.test(document.getElementById('tdn').textContent)), '다음 칸을 배웠으면 Lv 1 아래로는 못 내려요');
  await p.screenshot({ path: __dirname + '/shot_skill_down.png' });
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
