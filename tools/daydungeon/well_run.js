// 우물 입구 시안 찍기: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/daydungeon/well_run.js
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../..';
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const OUT = __dirname + '/well'; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4500);
  await p.addScriptTag({ path: __dirname + '/well_mock.js' });
  const shot = n => p.screenshot({ path: `${OUT}/${n}.png` });
  await p.evaluate(() => { __wellMock.place(true, 0); World.teleport('town', [15, 57]); }); await p.waitForTimeout(2500);
  await p.evaluate(() => World.walkToTile(16, 54)); await p.waitForTimeout(1500);
  await shot('1_map');
  await p.evaluate(() => { const [x, y] = World.tilePx(12, 55); World.bubble({ x, y: y - 34, sw: 0 }, '<b>마른 우물</b>', '밧줄 타고 내려가기', () => {}); }); await p.waitForTimeout(500);
  await shot('2_tap');
  await p.evaluate(() => { World.hideBubble(); __wellMock.panel(0, 3, []); }); await p.waitForTimeout(800); await shot('3_panel_mon');
  await p.evaluate(() => __wellMock.panel(2, 1, [0])); await p.waitForTimeout(500); await shot('4_panel_wed');
  await p.evaluate(() => { document.getElementById('dwx').remove(); __wellMock.place(false); const [x, y] = World.tilePx(12, 55); World.bubble({ x, y: y - 34, sw: 0 }, '<b>마른 우물</b><br>판자로 덮여 있어요.......'); }); await p.waitForTimeout(800);
  await shot('5_weekend');
  console.log('errs', JSON.stringify(errs)); await b.close();
})();
