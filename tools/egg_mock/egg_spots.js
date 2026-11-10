// 알 놓을 자리 후보 찾기: 학교(campus) 안에서 둘레 3 칸이 모두 비어 있는 넓은 곳 → 후보마다 사진 shot_spot_*.png
const { chromium, devices } = require('playwright'); const fs = require('fs');
const SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_8822/site'; fs.mkdirSync(SITE + '/__egg', { recursive: true }); ['egg_stages.png', 'egg_babies.png'].forEach(f => fs.copyFileSync(__dirname + '/' + f, SITE + '/__egg/' + f));
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => { const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage();
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.addScriptTag({ path: __dirname + '/egg_inject.js' }); await p.evaluate(() => __egg.load());
  await p.evaluate(() => new Promise(r => World.teleport('campus', [40, 45], () => setTimeout(r, 1500))));
  const cand = await p.evaluate(() => { const out = []; for (let y = 5; y < 105; y++) for (let x = 5; x < 90; x++){ let ok = true; for (let dy = -3; dy <= 3 && ok; dy++) for (let dx = -3; dx <= 3 && ok; dx++) if (!World.isFree(x + dx, y + dy)) ok = false; if (ok) out.push([x, y]); }
    const pick = []; out.forEach(([x, y]) => { if (pick.every(([a, b]) => Math.abs(a - x) + Math.abs(b - y) > 14)) pick.push([x, y]); }); return { n: out.length, pick: pick.slice(0, 8) }; });
  console.log(JSON.stringify(cand));
  for (const [i, s] of cand.pick.entries()){ await p.evaluate(s => new Promise(r => World.teleport('campus', [s[0], s[1] + 3], () => setTimeout(r, 1400))), s);
    await p.evaluate(s => __egg.place(1, 'fire', s), s); await p.waitForTimeout(700); await p.screenshot({ path: __dirname + `/shot_spot_${i}.png` }); }
  await b.close(); })();
