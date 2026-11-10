// 시안 찍기: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/egg_mock/egg_run.js
//   → tools/egg_mock/shot_*.png (휴대폰) · egg.mp4 (시작 연출 · 부화 연출)
const { chromium, devices } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process');
const R = __dirname + '/../..', SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_8822/site';
fs.mkdirSync(SITE + '/__egg', { recursive: true }); ['egg_stages.png', 'egg_babies.png'].forEach(f => fs.copyFileSync(__dirname + '/' + f, SITE + '/__egg/' + f));
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
async function page(b, opt){ const ctx = await b.newContext(opt), p = await ctx.newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && World.Avatar && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.addScriptTag({ path: __dirname + '/egg_inject.js' }); await p.evaluate(() => __egg.load()); return [ctx, p]; }
(async () => {
  const b = await chromium.launch();
  { const [ctx, p] = await page(b, { ...devices['iPhone 13'] }); const C = f => p.evaluate(f);
    const sp = await C(() => __egg.place(0, '')); await p.evaluate(s => new Promise(r => World.teleport('campus', [s[0], s[1] + 3], () => setTimeout(r, 1500))), sp); await p.waitForTimeout(800);
    await p.screenshot({ path: __dirname + '/shot_map0.png' });
    await C(() => __egg.place(2, 'fire')); await p.waitForTimeout(600); await p.screenshot({ path: __dirname + '/shot_map2.png' });
    await C(() => __egg.place(4, 'wind')); await p.waitForTimeout(600); await p.screenshot({ path: __dirname + '/shot_map4.png' });
    await C(() => __egg.care()); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_care.png' });
    await p.click('#eggv [data-a="star"]'); await p.fill('#eggv textarea', '오늘 처음으로 요일 던전을 깼어'); await p.waitForTimeout(300); await p.screenshot({ path: __dirname + '/shot_story.png' });
    await C(() => __egg.care({ day: 5, stage: 3, fire: 22, wind: 30, star: 18, today: 9, done: 'wind' })); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_cared.png' });
    await C(() => __egg.vote(1)); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_vote.png' });
    await C(() => __egg.close()); await p.setViewportSize({ width: 900, height: 700 }); await C(() => __egg.admin()); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_admin.png' });
    console.log('phone errs', JSON.stringify(p.errs.slice(0, 3))); await ctx.close(); }
  { const [ctx, p] = await page(b, { viewport: { width: 768, height: 432 }, recordVideo: { dir: __dirname + '/vid', size: { width: 768, height: 432 } } }); const t0 = Date.now();
    await p.evaluate(() => __egg.intro()); await p.evaluate(() => __egg.hatch(1)); await p.evaluate(() => __egg.hatch(3));
    const pre = (Date.now() - t0) / 1000, v = p.video(); console.log('video errs', JSON.stringify(p.errs.slice(0, 3))); await ctx.close(); const src = await v.path();
    const tot = Number(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${src}"`).toString());
    execSync(`ffmpeg -loglevel error -y -ss ${Math.max(0, tot - pre).toFixed(2)} -i "${src}" -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart "${__dirname}/egg.mp4"`); fs.rmSync(__dirname + '/vid', { recursive: true, force: true }); }
  await b.close(); console.log('ok');
})();
