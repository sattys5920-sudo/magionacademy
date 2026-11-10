// 동물 운동회 시작 연출 영상 (레오): node tools/sports/test/video_intro.js [포트] → tools/sports/shots/intro_leo.mp4
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process'); const R = __dirname + '/../../..', PORT = process.argv[2] || 8822, OUT = __dirname + '/../shots';
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.baby = { k: 3, adopt: 1, name: '토토', love: 30, follow: 1 }; seed.sports = { ctl: { open: true, id: 777, at: Date.now() } };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, recordVideo: { dir: OUT + '/vid', size: { width: 390, height: 844 } } }); const p = await ctx.newPage();
  const t0 = Date.now(); await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__spt, null, { timeout: 30000 });
  let st = 0; for (let i = 0; i < 40 && !st; i++){ if (await p.evaluate(() => World.cutBusy())) st = Date.now() - t0; else await p.waitForTimeout(250); }
  for (let i = 0; i < 120 && await p.evaluate(() => World.cutBusy()); i++) await p.waitForTimeout(500);
  await p.waitForTimeout(3000);
  const v = p.video(); await ctx.close(); await b.close(); const src = await v.path();
  execSync(`ffmpeg -loglevel error -y -ss ${Math.max(0, st / 1000 - 3)} -i "${src}" -c:v libx264 -pix_fmt yuv420p -crf 24 -movflags +faststart "${OUT}/intro_leo.mp4"`); fs.rmSync(OUT + '/vid', { recursive: true, force: true }); console.log('ok', st);
})();
