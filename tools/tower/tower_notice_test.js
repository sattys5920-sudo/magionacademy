// 시련의 탑 알림 검사: 탑이 열렸는데 연출을 못 본 학생에게 어디에 있든 「가 보기」 알림 → 강가로 가서 시작 연출
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.tw = { ctl: { open: true, at: 1 } };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => new Promise(r => World.teleport('town', [44, 52], () => setTimeout(r, 1000))));
  await p.waitForFunction(() => /시련의 문/.test((document.getElementById('confirm') || {}).innerText || ''), null, { timeout: 15000 }).catch(() => {});
  ok(await p.evaluate(() => /시련의 문/.test(document.getElementById('confirm').innerText)), '다른 곳(마을)에 있어도 알림이 떠요');
  await p.screenshot({ path: __dirname + '/shot_t_notice.png' });
  await p.click('#cfOk'); await p.waitForFunction(() => __tw.TW().S().seen, null, { timeout: 60000 }).catch(() => {});
  ok(await p.evaluate(() => World.where() === 'campus' && __tw.TW().S().seen === 1), '「가 보기」 → 강가로 가서 시작 연출을 봐요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
