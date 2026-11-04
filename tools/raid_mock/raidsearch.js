const { chromium } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});/)[1] + ')');
const ST = [[15, 0, 1, 256.92, 220], [25, 1, 2, 140.04, 235], [35, 2, 3, 95.58, 250], [45, 3, 4, 70.25, 265]];
(async () => { const b = await chromium.launch(); const p = await b.newPage(); p.on('pageerror', e => console.log('ERR', e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; window.sfx = () => {}; }, seed);
  await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000);
  const out = [];
  for (const [L, bi, eq, t30, want] of ST){ const s = +(30 * want / t30).toFixed(2); let lo = Math.log(.5), hi = Math.log(500), best;
    for (let k = 0; k < 13; k++){ const m = (lo + hi) / 2, am = Math.exp(m); const r = await p.evaluate(o => window.__raidSim(o), { L, b: bi, s, am, n: 100, hpK: 310, atK: 17, wp: eq, ar: eq }); best = { am: +am.toFixed(3), ...r }; if (r.win > .5) lo = m; else hi = m; }
    let fin; for (let k = 0; k < 5; k++){ fin = await p.evaluate(o => window.__raidSim(o), { L, b: bi, s, am: best.am, n: 400, hpK: 310, atK: 17, wp: eq, ar: eq }); if (Math.abs(fin.win - .5) < .03) break; best.am = +(best.am * (fin.win > .5 ? 1.04 : .96)).toFixed(3); }
    out.push({ L, b: bi, s, am: best.am, ...fin }); console.log(JSON.stringify(out[out.length - 1])); }
  fs.writeFileSync(process.argv[2], JSON.stringify(out)); await b.close(); })();
