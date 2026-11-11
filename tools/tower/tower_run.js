// 시안 찍기: python3 tools/tower/tower_art.py && sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/tower/tower_run.js
//   → tools/tower/shot_*.png (휴대폰) · 모의 사이트의 monsters_lpc.png 뒤에 탑 몬스터 9 칸을 이어 붙여요 (진짜 게임 파일은 안 건드려요)
const { chromium, devices } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process');
const R = __dirname + '/../..', SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_8822/site';
fs.mkdirSync(SITE + '/__tower', { recursive: true }); ['tower_mon.png', 'tower_icons.png', 'tower_building.png'].forEach(f => fs.copyFileSync(__dirname + '/' + f, SITE + '/__tower/' + f));
execSync(`python3 -c "
from PIL import Image
a = Image.open('${R}/public/art/monsters_lpc.png').convert('RGBA'); b = Image.open('${__dirname}/tower_mon.png').convert('RGBA')
o = Image.new('RGBA', (32 * 64 + b.width, 64), (0, 0, 0, 0)); o.alpha_composite(a.crop((0, 0, 32 * 64, 64)), (0, 0)); o.alpha_composite(b, (32 * 64, 0)); o.save('${SITE}/art/monsters_lpc.png')"`);
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 }, cur: 0, jo: { job: 'elemental', exp: 9000, xv: 3, sk: { '0_0': 1 } } };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(), errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.addScriptTag({ path: __dirname + '/tower_inject.js' }); await p.evaluate(() => __tower.load());
  console.log('jobs', JSON.stringify(await p.evaluate(() => __tw.jobs())));
  const sp = await p.evaluate(() => __tower.place()); console.log('spot', sp);
  await p.evaluate(s => new Promise(r => World.teleport('campus', [s[0] + 2, s[1] + 8], () => setTimeout(r, 1500))), sp); await p.evaluate(s => __tower.place(s), sp); await p.waitForTimeout(800);
  await p.screenshot({ path: __dirname + '/shot_map.png' });
  const C = f => p.evaluate(f);
  await C(() => __tower.open(14, 13)); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_tower.png' });
  for (const f of [14, 7, 20]){ await p.evaluate(f => __tower.card(f), f); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + `/shot_floor${f}.png` }); }
  for (const f of [14, 7, 20]){ await p.evaluate(f => __tower.battle(f), f); await p.waitForTimeout(1700); await p.screenshot({ path: __dirname + `/shot_battle${f}.png` }); await C(() => __tw.freeze()); await C(() => __T.closeSheet && __T.closeSheet()); await p.waitForTimeout(300); }
  await C(() => __tower.clear(14)); await p.waitForTimeout(400); await p.screenshot({ path: __dirname + '/shot_clear.png' });
  console.log('errs', JSON.stringify(errs.slice(0, 5))); await b.close();
})();
