// 각성 시안 영상: node awaken_video.js <포트> <저장 폴더>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8801, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.fam = { k: 6, at: Date.now(), tk: Date.now(), pts: 320 };
const INJ = fs.readFileSync(path.join(__dirname, 'awaken_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 22, 20); World.zoomStep(-1); }); await p.addScriptTag({ content: INJ }); await p.waitForTimeout(1500);
  const start = (Date.now() - T0) / 1000;
  await p.evaluate(() => window.__awGo({ line: '....흥. 이 모습, 너한테만 보여 주는 거니까.' }));
  await p.waitForFunction(() => window.__awDone, null, { timeout: 200000 });
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'awaken.webm')); fs.writeFileSync(path.join(OUT, 'awaken.start'), String(start)); await b.close();
})();
