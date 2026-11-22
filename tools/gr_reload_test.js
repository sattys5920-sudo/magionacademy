// 승급 시험 도중 새 버전이 나와도 시험 창은 새로 고쳐지지 않아요: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/gr_reload_test.js
//   시험 창이 열려 있으면 기다렸다가 · 창을 닫은 뒤에 새로 고쳐요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; window.__loads = (window.__loads || 0); }, seed);
  let newV = false; await p.route(/version\.json/, r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({ v: newV ? 'NEW' : 'OLD' }) }));
  let loads = 0; p.on('load', () => loads++);
  await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await ev(`(F.set(F.ref(db, 'promo/ctl'), { open: true, id: 4242, at: now2() }), 1)`); await p.waitForTimeout(800);
  await ev(`(xEx().job = xEx().job || 'warrior', grOpen(), grBegin(grY() + 1), 1)`); await p.waitForTimeout(800);
  ok(await ev('!!G2 && !!document.getElementById("grx")'), '시험 시작');
  const l0 = loads; newV = true;
  await p.evaluate(() => document.dispatchEvent(new Event('visibilitychange'))); await p.waitForTimeout(4000);
  ok(loads === l0 && await ev('!!G2'), '새 버전이 나와도 시험 중엔 새로 고치지 않아요');
  await ev('(grFinish(), 1)'); await p.waitForTimeout(500); await ev(`(document.querySelector('[data-grx]').click(), 1)`); await p.waitForTimeout(300);
  ok(await ev('!document.getElementById("grx") && grSt().pend && grSt().pend.cid == 4242'), '시험 끝 · 답안 저장');
  await p.evaluate(() => document.dispatchEvent(new Event('visibilitychange'))); await p.waitForTimeout(5000);
  ok(loads > l0, '창을 닫은 뒤엔 새 버전으로 새로 고쳐요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
