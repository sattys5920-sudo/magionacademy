// 광장(town) 쪽 알 자리 후보 사진: shot_town_*.png
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => { const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage();
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.addScriptTag({ path: __dirname + '/egg_inject.js' }); await p.evaluate(() => __egg.load());
  await p.evaluate(() => new Promise(r => World.teleport('town', [44, 50], () => setTimeout(r, 1500))));
  const cand = await p.evaluate(() => { const out = []; for (let y = 30; y < 70; y++) for (let x = 25; x < 65; x++){ let ok = true; for (let dy = -2; dy <= 2 && ok; dy++) for (let dx = -2; dx <= 2 && ok; dx++) if (!World.isFree(x + dx, y + dy)) ok = false; if (ok) out.push([x, y]); }
    out.sort((a, b) => Math.hypot(a[0] - 44, a[1] - 48) - Math.hypot(b[0] - 44, b[1] - 48)); const pick = []; out.forEach(([x, y]) => { if (pick.every(([a, c]) => Math.abs(a - x) + Math.abs(c - y) > 8)) pick.push([x, y]); }); return pick.slice(0, 4); });
  console.log(JSON.stringify(cand));
  for (const [i, s] of cand.entries()){ await p.evaluate(s => new Promise(r => World.teleport('town', [s[0], s[1] + 3], () => setTimeout(r, 1400))), s); await p.evaluate(s => __egg.place(1, 'fire', s, 'town'), s); await p.waitForTimeout(700); await p.screenshot({ path: __dirname + `/shot_town_${i}.png` }); }
  await b.close(); })();
