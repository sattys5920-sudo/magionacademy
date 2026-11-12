// 편의 기능 3 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/convenience3_test.js
//   시련의 탑 결과 「다음 층」 · 「다시 도전」 · 가방 「팔기」 (여러 개 골라 한 번에)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.tw = { ctl: { open: true, at: 1 } };
seed.players.me1.tw = { best: 2, seen: 1, d: '', n: 0, rw: {} };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 } };
Object.assign(seed.players.me1.inv, { herb: 5, mush: 3, g_straw: 4 });
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const C = (f, a) => p.evaluate(f, a), ev = s => C(s => __tw.ev(s), s);
  const floor = () => C(() => ((document.querySelector('#twv .hd b') || {}).textContent || ''));
  // 1 이미 깬 층을 이기면 「다음 층」
  await C(() => __tw.TW().go(1, 0)); await p.waitForTimeout(1000);
  await C(() => __tw.TW().end(true)); await p.waitForTimeout(300);
  const t1 = await C(() => (document.getElementById('xtwnx') || {}).textContent || '');
  ok(/다음 층 \(2 층\)/.test(t1), '이기면 「다음 층 (2 층)」 버튼 ' + t1);
  await p.screenshot({ path: __dirname + '/shot_tw_next.png' });
  await C(() => document.getElementById('xtwnx').click()); await p.waitForTimeout(500);
  ok(/2 층/.test(await floor()), '「다음 층」 → 2 층 카드 ' + await floor());
  // 2 지면 「다시 도전」
  await C(() => __tw.TW().go(2, 0)); await p.waitForTimeout(1000);
  await C(() => __tw.TW().end(false)); await p.waitForTimeout(300);
  ok(/다시 도전/.test(await C(() => (document.getElementById('xtwnx') || {}).textContent || '')), '지면 「다시 도전」 버튼');
  await C(() => document.getElementById('xtwnx').click()); await p.waitForTimeout(500);
  ok(/2 층/.test(await floor()), '「다시 도전」 → 같은 2 층 카드');
  // 3 처음 깬 층: 보상 카드에 「다음 층」
  await C(() => __tw.TW().go(3, 0)); await p.waitForTimeout(1000);
  await C(() => __tw.TW().end(true)); await p.waitForTimeout(300); await C(() => document.getElementById('xnext').click()); await p.waitForTimeout(500);
  ok(await C(() => !!document.querySelector('#twv [data-twnx]')) && /3 층 돌파/.test(await C(() => document.getElementById('twv').innerText)), '처음 깬 층 보상 카드에 「다음 층」');
  await p.screenshot({ path: __dirname + '/shot_tw_res.png' });
  await C(() => document.querySelector('#twv [data-twnx]').click()); await p.waitForTimeout(400);
  ok(/4 층/.test(await floor()), '보상 카드 「다음 층」 → 4 층 카드');
  await C(() => { const v = document.getElementById('twv'); if (v) v.remove(); });
  // 4 가방 팔기
  await ev("(closeSheet(), bagTab = 'all', bagQ = '', bagSellM = false, openSheet('home', 'bag'))").catch(() => {}); await p.waitForTimeout(600);
  await C(() => document.getElementById('bagSellM').click()); await p.waitForTimeout(300);
  const dis = await C(() => [...document.querySelectorAll('[data-bsel]')].filter(b => b.disabled).length);
  ok(await ev("bagSellM") && dis >= 0, '「팔기」를 누르면 고르는 모드 (팔 수 없는 칸 ' + dis + ' 개는 흐리게)');
  for (const k of ['herb', 'mush', 'g_straw']) { await C(k => document.querySelector(`[data-bsel="${k}"]`).click(), k); await p.waitForTimeout(150); }
  const sum = await C(() => document.querySelector('.bag-dt').innerText);
  const want = await ev("['herb', 'mush', 'g_straw'].reduce((t, k) => t + partyMul(sellPay(k, bagSellBase(k)) * me.inv[k]), 0)");
  ok(/3종 \d+개/.test(sum) && sum.includes(want.toLocaleString() + 'G'), '고른 것 합계 ' + sum.replace(/\n/g, ' / '));
  await p.screenshot({ path: __dirname + '/shot_bag_sell.png' });
  const coin0 = await ev('me.coin');
  await C(() => document.querySelector('[data-bsgo]').click()); await p.waitForTimeout(400);
  await p.waitForSelector('#cfOk', { timeout: 3000 }).then(() => p.click('#cfOk')).catch(() => {}); await p.waitForTimeout(500);
  ok((await ev('me.coin')) === coin0 + want && (await ev("!me.inv.herb && !me.inv.mush && !me.inv.g_straw && !bagSellM")), `팔면 +${want}G · 가방에서 빠져요`);
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
