// 정원 손님 도감 탭 시안 영상: node garden_dex_video.js <포트> <저장 폴더>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.', LIST = (process.argv[4] || '0,12,16').split(',').map(Number);
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'garden_dex_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 10, 2, 19, 10); World.zoomStep(-2); World.tagsOff(true); World.teleport('myroom_witch', [8, 8]); }); await p.waitForTimeout(2500);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  p.evaluate(() => window.__gxGo());
  await p.waitForFunction(() => window.__gxDone, null, { timeout: 300000 });
  fs.writeFileSync(path.join(OUT, 'dex_log.json'), JSON.stringify(await p.evaluate(() => window.__gxLog)));
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'dex.webm'));
  fs.writeFileSync(path.join(OUT, 'dex.start'), String(start)); console.log('start', start);
  await b.close();
})();
