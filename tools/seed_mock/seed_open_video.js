// 씨앗 대회 처음 연출 시안 영상: node seed_open_video.js <포트> <저장 폴더> [식물 번호=4] → seed_open.webm + seed_open.start
//   목업 사이트 폴더에 blanc_lpc.png · seed_plants.png가 있어야 해요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.', MINE = +(process.argv[4] || 4);
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'seed_open_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 22, 20); World.zoomStep(-1); World.zoomStep(-1); World.teleport('campus', [18, 59]); }); await p.waitForTimeout(2800);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  p.evaluate(m => window.__soGo(m), MINE);
  await p.waitForFunction(() => window.__soDone, null, { timeout: 180000 });
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'seed_open.webm'));
  fs.writeFileSync(path.join(OUT, 'seed_open.start'), String(start)); console.log('start', start);
  await b.close();
})();
