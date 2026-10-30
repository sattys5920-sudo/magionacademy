// 정령 만남 시안 영상 찍기: node encounter_video.js <포트> <저장 폴더>  → encounter.webm (앞쪽 로딩은 ffmpeg로 잘라요)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8792, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'encounter_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 23, 20); World.zoomStep(-1); });
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(1500);
  const start = (Date.now() - T0) / 1000;
  const L = JSON.parse(fs.readFileSync(path.join(__dirname, 'lines', 'vael.json'), 'utf8')), PJ = fs.readFileSync(path.join(__dirname, 'panel_inject.js'), 'utf8');
  await p.evaluate(o => window.__encGo(o), { first: '....너구나. 이제부터 같이 간다', idle: L.idle[0][1], like: L.gift.like[0][0], panel: L.greet[0], panelJs: PJ });
  await p.waitForFunction(() => window.__encDone, null, { timeout: 200000 });
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'encounter.webm'));
  fs.writeFileSync(path.join(OUT, 'encounter.start'), String(start)); console.log('start', start);
  await b.close();
})();
