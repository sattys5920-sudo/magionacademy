// 누비 7 일째 솜 찾기: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/nubi_cotton_test.js
//   본관 앞 돌길에 솜이 보이고 · 손가락으로 눌러 주울 수 있고 · 누비에게 주면 우리 반 수에 들어가요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  const spots = await ev(`JSON.stringify(NB_COT)`); console.log('  솜 자리', spots);
  for (const uid of ['me1']){
    await ev(`(nbCtl = { open: true, id: 777, d0: dayKey(dayNo(todayKey()) - 6), ids: [myId()] }, me.nubi = { ev: 777, s: 6, b7: 1 }, nbPropSig = '', 1)`).catch(async () => {
      await ev(`(nbCtl = { open: true, id: 777, d0: (() => { const d = new Date(now2() - 6 * 864e5 + 9 * 3600e3); return d.toISOString().slice(0, 10); })(), ids: [myId()] }, me.nubi = { ev: 777, s: 6, b7: 1 }, nbPropSig = '', 1)`); });
  }
  ok(await ev('nbCD() >= 7 && nbCur(nbT()) === 7'), '7 일째 · 솜 찾는 날 (d0 ' + await ev('nbCtl.d0') + ')');
  const cs = JSON.parse(await ev('JSON.stringify(NB_COT[nbHash(myId()) % NB_COT.length])'));
  await ev(`(async () => { await tpSafe('campus', [${cs[1] + 3}, ${cs[2] + 2}]); })()`); await p.waitForTimeout(2500); await ev('(nbPropSig = "", nbProps(), 1)'); await p.waitForTimeout(800);
  await p.screenshot({ path: __dirname + '/shot_nubi_cot.png' });
  const pt = await ev(`World.propClient('nbcot')`); ok(!!pt, '솜이 화면에 있어요 ' + JSON.stringify(pt));
  if (pt){ await p.mouse.click(pt[0], pt[1]); await p.waitForTimeout(3500); }
  ok(await ev('!!nbT().hc'), '손가락으로 눌러서 주웠어요');
  ok(await ev(`(nbTap(), new Promise(r => setTimeout(() => r(!!nbT().cot && nbCnt('cot') === 1), 800)))`), '누비에게 줬어요 · 우리 반 1 / 1');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
