// 마법 씨앗 대회 시안 영상 찍기: node seed_video.js <포트> <저장 폴더> → seed.webm + seed.start (앞쪽 로딩은 ffmpeg로 잘라요)
//   목업 사이트 폴더에 seed_plants.png · seed_bg.png가 있어야 해요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'seed_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.zoomStep(-1); World.teleport('campus', [76, 44]); }); await p.waitForTimeout(2500);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  p.evaluate(() => window.__sdGo());
  const click = async sel => { await p.waitForSelector(sel + ':not([disabled])', { state: 'visible', timeout: 90000 }); await p.waitForTimeout(2600); await p.click(sel); };   // 씨앗 기분 말풍선을 읽을 틈을 줘요
  for (const k of ['water', 'moon', 'moon', 'moon']) await click(`[data-sc="${k}"]`);
  await click('[data-sv="7"]');
  await p.waitForFunction(() => window.__sdDone, null, { timeout: 120000 });
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'seed.webm'));
  fs.writeFileSync(path.join(OUT, 'seed.start'), String(start)); console.log('start', start);
  await b.close();
})();
