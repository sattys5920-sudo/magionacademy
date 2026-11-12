// 관리자 학생 표: 1차 · 2차 직업 레벨 검사 (sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/admin_job_test.js)
const { chromium } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'elemental', exp: 9000, xv: 3, cur: 1, sk: { '0_0': 1 }, jo: { job: 'knight', exp: 200000, xv: 3, sk: { '0_0': 1 } } };
(async () => {
  const b = await chromium.launch(), errs = [], p = await b.newPage({ viewport: { width: 1200, height: 900 } }); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'admin'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => __T.showAdmin()); await p.waitForTimeout(1500); await p.evaluate(() => window.__adPoll && window.__adPoll()); await p.waitForTimeout(800);
  if (!(await p.$('.adtbl'))) await p.evaluate(() => { const t = [...document.querySelectorAll('[data-adtab]')].find(b => b.offsetParent && /학생/.test(b.textContent)); if (t) t.click(); });
  await p.waitForTimeout(1200);
  const row = await p.evaluate(() => { const r = [...document.querySelectorAll('.adtbl > div')].find(d => /민준/.test(d.textContent)); return r ? r.children[2].textContent : ''; });
  const want = await p.evaluate(() => __tw.ev("`기사 Lv ${xLv(200000).L} · 정령술사 Lv ${xLv(9000).L}`")).catch(() => '');
  ok(row && row === want, '직업 칸: ' + row + ' (기대 ' + want + ')');
  const el = await p.$('.adtbl'); if (el) await el.screenshot({ path: __dirname + '/shot_admin_job.png' });
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
