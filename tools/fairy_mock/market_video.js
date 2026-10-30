// 요정 시장 시안 영상 찍기: node market_video.js <포트> <저장 폴더> → market.webm + market.start (앞쪽 로딩은 ffmpeg로 잘라요)
//   목업 사이트 폴더에 fairy_market.png가 있어야 해요 (cp fairy_market.png <사이트>/)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'market_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 23, 20); World.zoomStep(-1); World.teleport('campus', [76, 44]); }); await p.waitForTimeout(2500);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  p.evaluate(() => window.__fmGo());
  const click = async sel => { await p.waitForSelector(sel, { state: 'visible', timeout: 90000 }); await p.waitForTimeout(1300); await p.click(sel); };
  await click('[data-fi="1"]'); await click('[data-mi="3"]');
  await click('[data-fi="2"]'); await click('[data-mi="2"]');
  await p.waitForFunction(() => window.__fmDone, null, { timeout: 120000 });
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'market.webm'));
  fs.writeFileSync(path.join(OUT, 'market.start'), String(start)); console.log('start', start);
  await b.close();
})();
