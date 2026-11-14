// 동네 고양이 다섯 자리에 실제로 걸어서 닿을 수 있는지: 지역 시작 자리에서 고양이 옆 빈칸(freeNear)으로 걸어가 3 칸 안에 닿는지 봐요
// 사용: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/catmeet/test/reach.js
const { chromium } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.babySeen = 'x'; seed.approved = { me1: true };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }), p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; window.__catNight = 0; }, seed); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const AT = { cheese: ['town', 39, 54], grandpa: ['campus', 40, 36], cloak: ['town', 24, 57], calico: ['town', 33, 40], princess: ['town', 34, 81] };
  let bad = 0;
  for (const [k, [m, x, y]] of Object.entries(AT)){
    await p.evaluate(m => new Promise(r => World.teleport(m, m === 'town' ? [44, 52] : [44, 46], () => setTimeout(r, 1500))), m);
    const fr = await p.evaluate(([x, y]) => (World.freeNear(x, y, 2) || []).sort((a, b) => (Math.abs(a[0] - x) + Math.abs(a[1] - y)) - (Math.abs(b[0] - x) + Math.abs(b[1] - y))), [x, y]);
    let dist = null;
    if (fr.length){ await p.evaluate(c => World.walkToTile(c[0], c[1]), fr[0]);
      for (let t = 0; t < 40; t++){ await p.waitForTimeout(1000); dist = await p.evaluate(([x, y]) => { const t = World.meTile(); return t ? Math.abs(t.x - x) + Math.abs(t.y - y) : null; }, [x, y]); if (dist != null && dist <= 3) break; } }
    const ok = dist != null && dist <= 3; if (!ok) bad++;
    console.log(`${ok ? 'ok' : 'XX'} ${k}: ${m} [${x},${y}] · 옆 빈칸 ${fr.length} 개 · 걸어간 뒤 거리 ${dist}`);
  }
  console.log('오류', errs.slice(0, 3)); await b.close(); process.exit(bad ? 1 : 0);
})();
