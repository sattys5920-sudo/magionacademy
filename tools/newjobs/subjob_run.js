// 부직업 시안 찍기: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/newjobs/subjob_run.js [포트]
//   → tools/newjobs/subjob/cut.mp4 (연출 + 로비) · pick_phone.png · lobby_*.png
const { chromium, devices } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process'); const R = __dirname + '/../..', PORT = process.argv[2] || 8822;
const SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_' + PORT + '/site', OUT = __dirname + '/subjob';
fs.mkdirSync(SITE + '/__newjobs', { recursive: true }); fs.mkdirSync(OUT, { recursive: true }); fs.copyFileSync(__dirname + '/weapons_new.png', SITE + '/__newjobs/weapons_new.png');
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')'); seed.players.me1.ex = { job: 'knight', exp: 0, xv: 3 }; seed.players.me1.coin = 5000;
const FIRST = { first: 'knight', firstN: '기사' };
async function page(b, opt){ const ctx = await b.newContext(opt); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.errs = errs;
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.World && World.Avatar, null, { timeout: 30000 }); await p.waitForTimeout(2500);
  await p.addScriptTag({ path: __dirname + '/subjob_mock.js' }); return [ctx, p]; }
(async () => {
  const b = await chromium.launch();
  // 1) 폰: 고르는 화면
  { const [ctx, p] = await page(b, { ...devices['iPhone 13'] });
    p.evaluate(o => __sj.cut(o), { ...FIRST, look: 12 }).catch(() => {}); await p.waitForSelector('.sjpick.on', { timeout: 30000 }); await p.waitForTimeout(800);
    await p.click('[data-sj="4"]'); await p.waitForTimeout(500); await p.screenshot({ path: OUT + '/pick_phone.png' });
    await p.click('[data-sj="1"]'); await p.waitForTimeout(500); await p.screenshot({ path: OUT + '/pick_phone_bad.png' }); console.log('phone errs', JSON.stringify(p.errs)); await ctx.close(); }
  // 2) 영상: 연출 → 탐사 로비에서 1차 / 2차 바꾸기
  const [ctx, p] = await page(b, { viewport: { width: 768, height: 432 }, recordVideo: { dir: OUT + '/vid', size: { width: 768, height: 432 } } }); const t0 = Date.now();
  const got = await p.evaluate(o => __sj.cut(o), { ...FIRST, look: 12, auto: [1, 4, 6] });
  await p.evaluate(() => World.onExplore(0)); await p.waitForTimeout(1500);
  const st = { cur: 0, sub: got, lv1: 32, lv2: 1 }; await p.evaluate(s => __sj.lobby(s), st); await p.waitForTimeout(1600); await p.screenshot({ path: OUT + '/lobby_1.png' });
  await p.click('[data-sjc="1"]'); await p.waitForTimeout(1800); await p.screenshot({ path: OUT + '/lobby_2.png' });
  await p.click('[data-sjc="0"]'); await p.waitForTimeout(1400);
  await p.evaluate(s => __sj.lobby(s), { ...st, cur: 1, locked: 1 }); await p.waitForTimeout(1600); await p.screenshot({ path: OUT + '/lobby_ready.png' });
  await p.evaluate(s => __sj.lobby(s), { cur: 0, sub: null, lv1: 14 }); await p.waitForTimeout(1600); await p.screenshot({ path: OUT + '/lobby_none.png' });
  const v = p.video(); const pre = (Date.now() - t0) / 1000; await ctx.close(); const src = await v.path(); await b.close();
  const total = Number(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${src}"`).toString());
  execSync(`ffmpeg -loglevel error -y -ss ${Math.max(0, total - pre).toFixed(2)} -i "${src}" -c:v libx264 -pix_fmt yuv420p -crf 23 -movflags +faststart "${OUT}/cut.mp4"`); fs.rmSync(OUT + '/vid', { recursive: true, force: true });
  console.log('ok', got, pre.toFixed(1), JSON.stringify(p.errs.slice(0, 3)));
})();
