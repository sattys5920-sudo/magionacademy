// 무슈 블랑 맛 표현 시안 영상: node blanc_feast_video.js <포트> <저장 폴더> [요리 번호 쉼표] → feast.webm + feast.wav(소리) + feast.start
//   목업 사이트 폴더에 blanc_lpc.png · seed_dishes.png · blanc_reactions.json이 있어야 해요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8813, OUT = process.argv[3] || '.', LIST = (process.argv[4] || '0,12,16').split(',').map(Number);
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'blanc_feast_inject.js'), 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); p.on('pageerror', e => console.log('err', e.message)); const T0 = Date.now();
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { World.kNow = () => new Date(2026, 9, 30, 23, 20); World.zoomStep(-1); World.teleport('candy', [16, 13]); }); await p.waitForTimeout(2500);
  await p.addScriptTag({ content: INJ }); await p.waitForTimeout(800);
  const start = (Date.now() - T0) / 1000;
  if (process.argv[4] === 'finale') p.evaluate(() => window.__bfFinale()); else p.evaluate(l => window.__bfGo(l), LIST);
  await p.waitForFunction(() => window.__bfDone, null, { timeout: 300000 });
  const total = (Date.now() - T0) / 1000 - start + 1;
  const wav = await p.evaluate(t => window.__bfSnd.render(t, 'audio/bgm_main.mp3'), total);   // 영상에는 소리가 안 담겨서 같은 합성을 다시 그려 붙여요
  fs.writeFileSync(path.join(OUT, 'feast.wav'), Buffer.from(wav, 'base64'));
  fs.writeFileSync(path.join(OUT, 'feast_log.json'), JSON.stringify(await p.evaluate(() => window.__bfSnd.log())));
  fs.writeFileSync(path.join(OUT, 'feast_bgm.wav'), Buffer.from(await p.evaluate(t => window.__bfSnd.render(t, 'audio/bgm_main.mp3', true), total), 'base64'));
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(OUT, 'feast.webm'));
  fs.writeFileSync(path.join(OUT, 'feast.start'), String(start)); console.log('start', start);
  await b.close();
})();
