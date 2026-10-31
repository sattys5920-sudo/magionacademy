// 유령 전학생 시안 영상: node ghost_video.js <포트> <저장 폴더> → ghost.webm + ghost.start
//   목업 사이트 폴더에 ghost_lpc.png가 있어야 해요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.', LIST = (process.argv[4] || '0,12,16').split(',').map(Number);
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'ghost_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 21, 40); World.zoomStep(-1); World.tagsOff(true); World.setNpcs([]); World.teleport('campus', [44, 46]); }); await p.waitForTimeout(2500);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  p.evaluate(() => window.__ghGo());
  await p.waitForFunction(() => window.__ghDone, null, { timeout: 300000 });
  fs.writeFileSync(path.join(OUT, 'ghost_log.json'), JSON.stringify(await p.evaluate(() => window.__ghLog)));
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'ghost.webm'));
  fs.writeFileSync(path.join(OUT, 'ghost.start'), String(start)); console.log('start', start);
  await b.close();
})();
