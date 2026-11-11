// 탑 자리 후보: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/tower/tower_spots.js
//   학교(campus)에서 탑 둘레 (가로 7 · 세로 9 칸) 가 모두 빈 곳을 찾아 서로 떨어진 후보마다 탑을 세우고 shot_spot_*.png
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => { const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage();
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => new Promise(r => World.teleport('campus', [40, 45], () => setTimeout(r, 1500))));
  const cand = await p.evaluate(() => { const out = []; for (let y = 8; y < 105; y++) for (let x = 6; x < 88; x++){ let ok = true; for (let a = -3; a <= 3 && ok; a++) for (let c = -6; c <= 2 && ok; c++) if (!World.isFree(x + a, y + c)) ok = false; if (ok) out.push([x, y]); }
    const pick = []; out.forEach(([x, y]) => { if (pick.every(([a, c]) => Math.abs(a - x) + Math.abs(c - y) > 16)) pick.push([x, y]); }); return pick.slice(0, 8); });
  console.log(JSON.stringify(cand));
  const im = await p.evaluate(() => new Promise(r => { const i = new Image(); i.onload = () => r(true); i.src = 'art/tower_building.png?v=1'; window.__twi = i; }));
  for (const [i, s] of cand.entries()){
    await p.evaluate(s => { const K = 1.5, cv = document.createElement('canvas'); cv.width = 56 * K; cv.height = 120 * K; const g = cv.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(window.__twi, 0, 0, cv.width, cv.height);
      World.setProps('campus', [{ id: 'tower', x: s[0], y: s[1], img: cv, pxc: g, sw: cv.width, sh: cv.height, ax: cv.width / 2, ay: cv.height - 9, solid: true }], 'tower'); }, s);
    await p.evaluate(s => new Promise(r => World.teleport('campus', [s[0] + 2, s[1] + 7], () => setTimeout(r, 1400))), s);
    await p.screenshot({ path: __dirname + `/shot_spot_${i}.png` }); }
  await b.close(); })();
