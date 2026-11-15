// 새 친구 넷 ♥10 방 가구: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/newnpc4_furn_test.js
//   ♥10 보상으로 가방에 들어오고 · 방에 놓이고 · 그림이 그려져요 (스크린숏 tools/shot_furn_new4.png)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.nnpc = Object.fromEntries(['bau', 'kael', 'artua', 'grego'].map(id => [id, { met: 1, at: 1 }]));
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const F = { bau: 'bau_house', kael: 'kael_lantern', artua: 'artua_starmap', grego: 'grego_sofa' };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  ok(await ev(`${JSON.stringify(Object.values(F))}.every(f => FURN_BY[f] && FURN_BY[f].sw > 1 && FURN_BY[f].ev)`), '가구 넷이 가구 목록에 있어요');
  for (const [n, f] of Object.entries(F)){   // ♥10 보상 → 가방
    await ev(`(async () => { const ev = await (await fetch('data/npc/${n}/events/heart_10.json')).json(); me.fbag = me.fbag || {}; const b = me.fbag['${f}'] || 0; evFinish({ n: npcGet('${n}'), k: 10, ev, sum: 0, cold: false }); window.__fb = [b, me.fbag['${f}']]; })()`); await p.waitForTimeout(300);
    const fb = await ev('window.__fb'); ok(fb && fb[1] === fb[0] + 1, `${n} ♥10 → 가방에 「${f}」`);
  }
  await ev(`(me.room = me.room || [], [['bau_house', 8, 6], ['kael_lantern', 5, 2], ['artua_starmap', 11, 2], ['grego_sofa', 4, 6]].forEach(([f, x, y]) => { me.fbag[f]--; me.room.push({ id: crId(), f, x, y }); }), save(), World.teleport(myRoomId(), 'bed', () => {}), 1)`);
  await p.waitForTimeout(3500); await ev('syncRoom()'); await ev("document.querySelectorAll('.toast,#toast').forEach(t => t.remove())"); await p.waitForTimeout(9000);
  await p.screenshot({ path: __dirname + '/shot_furn_new4.png' });
  ok(await ev(`me.room.filter(r => ${JSON.stringify(Object.values(F))}.includes(r.f)).length === 4`), '방에 넷 다 놓였어요');
  ok(await ev(`(() => { const c = document.createElement('div'); c.innerHTML = ${JSON.stringify(Object.values(F))}.map(f => furnPic(f)).join(''); return c.querySelectorAll('i').length === 4; })()`), '가구 그림(가방 아이콘) 넷');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
