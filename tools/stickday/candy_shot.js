// 과자 교실 쿠키 오븐 · 막대 틀 겹침 확인: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/stickday/candy_shot.js [이름]
//   → tools/stickday/shot_candy_<이름>.png · 두 소품 위치와 눌렀을 때 열리는 창을 찍어요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const tag = process.argv[2] || 'now';
seed.players.me1.ck = { met: 1 }; seed.players.me1.stk = { ev: '2026-11-11', hi: 1, gv: 1, npc: {}, rw: {} }; seed.stick = { ctl: { open: true, at: 1 } };
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(), errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => { const v = document.getElementById('stkv'); if (v) v.remove(); });
  await p.waitForTimeout(3000); await p.evaluate(() => { World.teleport('candy', [17, 8]); }); await p.waitForTimeout(3500);
  console.log('where', await p.evaluate(() => World.where()));
  await p.evaluate(() => { document.querySelectorAll('#stkv,.mqskip').forEach(e => e.remove()); });
  await p.waitForTimeout(2500);
  const info = await p.evaluate(() => { const o = (World.propsDbg && World.propsDbg()) || null; return { o }; });
  console.log(JSON.stringify(info)); console.log('free', JSON.stringify(await p.evaluate(() => { const o = []; for (let y = 1; y < 16; y++){ let r = ''; for (let x = 1; x < 30; x++) r += World.isFree(x, y) ? '.' : '#'; o.push(y + ' ' + r); } return o; })));
  await p.evaluate(() => World.teleport('candy', [17, 10])); await p.waitForTimeout(2000);
  console.log('ctx', await p.evaluate(() => document.getElementById('ctx').innerText));
  await p.screenshot({ path: __dirname + `/shot_candy_${tag}.png` });
  await p.evaluate(() => World.onProp('stkmold')); await p.waitForTimeout(800); console.log('mold →', await p.evaluate(() => { const v = document.getElementById('stkv'); return v ? v.innerText.slice(0, 60).replace(/\n/g, ' / ') : '창 없음'; }));
  await p.evaluate(() => { const v = document.getElementById('stkv'); if (v) v.remove(); }); await p.evaluate(() => World.onProp('ckoven')); await p.waitForTimeout(800); console.log('oven →', await p.evaluate(() => (document.querySelector('.panel') || document.body).innerText.slice(0, 40).replace(/\n/g, ' / ')));
  console.log('errs', JSON.stringify(errs.slice(0, 3))); await b.close();
})();
