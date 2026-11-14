// 편의 기능 4 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/convenience4_test.js
//   스탯 「−1」 (방금 올린 건 무료 · 예전 것은 30G) · 물약 · 요리 즐겨찾기 (목록 맨 위)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 }, sp: { atk: 3 } }; seed.players.me1.coin = 1000;
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  // 1 스탯 −1
  await ev("(xv = { view: 'stats', sel: 'atk' }, openSheet('home', 'explore'))"); await p.waitForTimeout(800);
  ok(await p.evaluate(() => !document.getElementById('sm1').disabled && /30G/.test(document.getElementById('sm1').textContent)), '예전에 찍은 스탯: 「−1 · 30G」');
  await p.click('#sm1'); await p.waitForTimeout(300);
  ok(await ev("xEx().sp.atk === 2 && me.coin === 970"), '−1 → 공격 3 → 2 · 30G');
  await p.click('#sp1'); await p.waitForTimeout(300); await p.click('#sm1'); await p.waitForTimeout(300);
  ok(await ev("xEx().sp.atk === 2 && me.coin === 970"), '방금 올린 건 −1 이 무료');
  await p.screenshot({ path: __dirname + '/shot_stat_down.png' });
  // 2 물약 즐겨찾기
  const pk = await ev("me.hints.filter(p => POTION_INFO[p]).slice(-1)[0]");
  await ev(`(POTION_INFO['${pk}'].r.forEach(k => { me.inv[k] = 5; }), closeSheet(), labTab = 'brew', labFill('${pk}'), openSheet('lab'))`); await p.waitForTimeout(600);
  await p.click(`[data-pfav="${pk}"]`); await p.waitForTimeout(300);
  ok(await ev(`favOn('p', '${pk}')`), '물약 ☆ → 즐겨찾기 ' + pk);
  await p.click('#recipePick'); await p.waitForTimeout(300);
  ok(await p.evaluate(pk => { const r = document.querySelectorAll('.reclist [data-recipe]'); const f = [...r].findIndex(x => x.dataset.recipe === pk); return f >= 0 && [...r].slice(0, f).every(x => !/^★/.test(x.innerText.trim()) ? false : true) && /★/.test(r[f].innerText); }, pk), '레시피 목록에서 즐겨찾기가 위로 · ★');
  await p.screenshot({ path: __dirname + '/shot_fav_potion.png' });
  // 3 요리 즐겨찾기
  await ev("(closeSheet(), ckTab = 'book', openSheet('home', 'cook'))"); await p.waitForTimeout(600);
  const last = await p.evaluate(() => { const c = [...document.querySelectorAll('[data-cksel]')]; return c[c.length - 1].dataset.cksel; });
  await p.click(`[data-cksel="${last}"]`); await p.waitForTimeout(300); await p.click(`[data-ckfav="${last}"]`); await p.waitForTimeout(300);
  ok(await p.evaluate(k => document.querySelector('[data-cksel]').dataset.cksel === k && /★/.test(document.querySelector('[data-cksel]').innerText), last), '요리 ☆ → 맨 앞 칸 · ★ ' + last);
  await p.screenshot({ path: __dirname + '/shot_fav_dish.png' });
  await p.click(`[data-ckfav="${last}"]`); await p.waitForTimeout(300);
  ok(await ev(`!favOn('d', '${last}')`), '한 번 더 누르면 빠져요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
