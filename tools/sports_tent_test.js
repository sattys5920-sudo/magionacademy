// 운동회 천막 누르기: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/sports_tent_test.js
//   천막 그림 위 어디를 눌러도 열려요 · 앞에 사람이 서 있어도 천막이 먼저 (스크린숏 tools/shot_sptent.png)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await ev(`F.set(F.ref(db, 'sports/ctl'), { open: true, id: now2(), at: now2() })`); await p.waitForTimeout(500);
  await ev(`(async () => { await tpSafe('town', [44, 50]); })()`); await p.waitForTimeout(3000);
  for (let k = 0; k < 40 && await ev('World.cutBusy()'); k++){ await ev(`(document.querySelector('.mqskip')?.click(), 1)`).catch(() => {}); await p.waitForTimeout(500); }
  await ev(`(async () => { await tpSafe('town', [44, 50]); })()`); await p.waitForTimeout(2500);
  await ev("document.querySelectorAll('.toast,#toast').forEach(t => t.remove())");
  await p.screenshot({ path: __dirname + '/shot_sptent.png' });
  const pt = await ev(`World.propClient('sptent')`); ok(!!pt, '천막이 화면에 있어요 ' + JSON.stringify(pt));
  const spots = [[0, -30], [-22, -12], [22, -12], [0, -4], [-14, -36]];
  for (const [dx, dy] of spots){
    await ev(`(document.querySelector('[data-spx="x"]')?.click(), 1)`); await p.waitForTimeout(400); await p.mouse.click(pt[0] + dx, pt[1] + dy); await p.waitForTimeout(700);
    ok(await ev(`!!$('#spv')`), `천막 (${dx}, ${dy}) 눌러서 열림`);
  }
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
