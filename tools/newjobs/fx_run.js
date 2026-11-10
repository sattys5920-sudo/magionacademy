// 새 직업 시안 찍기: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/newjobs/fx_run.js [포트] → fx_sheet.png · fx_video.mp4
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process'); const R = __dirname + '/../..', PORT = process.argv[2] || 8822;
const SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_' + PORT + '/site';
fs.mkdirSync(SITE + '/__newjobs', { recursive: true }); fs.copyFileSync(__dirname + '/weapons_new.png', SITE + '/__newjobs/weapons_new.png'); fs.copyFileSync(__dirname + '/xw_new.json', SITE + '/__newjobs/xw_new.json');
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 768, height: 432 }, recordVideo: { dir: __dirname + '/vid', size: { width: 768, height: 432 } } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.World && World.Avatar, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  await p.addScriptTag({ path: __dirname + '/fx_mock.js' }); await p.evaluate(() => __nj.load());
  // 한 장: 줄마다 직업 · 무기 든 모습 + 스킬 셋
  const url = await p.evaluate(async () => { const { JOBS, scene, W, H } = __nj, s = .8, out = document.createElement('canvas'); out.width = W * 4 * s + 30; out.height = H * JOBS.length * s + JOBS.length * 6; const o = out.getContext('2d'); o.fillStyle = '#100c1c'; o.fillRect(0, 0, out.width, out.height); o.imageSmoothingEnabled = false;
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    for (let j = 0; j < JOBS.length; j++) for (let si = -1; si < 3; si++){ await scene(c, JOBS[j], si, .55); o.drawImage(c, (si + 1) * (W * s + 10), j * (H * s + 6), W * s, H * s); }
    return out.toDataURL(); });
  fs.writeFileSync(__dirname + '/fx_sheet.png', Buffer.from(url.split(',')[1], 'base64'));
  // 영상: 직업마다 스킬 셋 (한 스킬 1.2 초)
  await p.evaluate(() => { const c = document.createElement('canvas'); c.id = 'njv'; c.width = __nj.W; c.height = __nj.H; c.style.cssText = 'position:fixed;inset:0;width:768px;height:432px;z-index:99999;image-rendering:pixelated;background:#000'; document.body.appendChild(c); });
  const t0 = Date.now();
  await p.evaluate(async () => { const { JOBS, scene } = __nj, c = document.getElementById('njv'); for (const J of JOBS){ await scene(c, J, -1, 0); await new Promise(r => setTimeout(r, 700)); for (let si = 0; si < 3; si++){ const s0 = performance.now(); while (performance.now() - s0 < 1200){ await scene(c, J, si, Math.min(1, (performance.now() - s0) / 1000)); await new Promise(r => requestAnimationFrame(r)); } } } });
  const v = p.video(); await ctx.close(); await b.close(); const src = await v.path();
  execSync(`ffmpeg -loglevel error -y -ss 4.5 -i "${src}" -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart "${__dirname}/fx_video.mp4"`); fs.rmSync(__dirname + '/vid', { recursive: true, force: true });
  console.log('ok', (Date.now() - t0) / 1000, JSON.stringify(errs.slice(0, 3)));
})();
