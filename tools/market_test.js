// 가판대 묶음 판매 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/market_test.js
//   여러 개 올리기 · 친구가 개수 골라 사기 · 판 만큼 골드 쌓임 · 받기 · 남은 것 내리기 · 다 팔리면 받기 뒤 사라져요 · 예전 한 개짜리도 그대로
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me2 = JSON.parse(JSON.stringify(seed.players.me1)); seed.players.me2.nick = '서연'; seed.players.me2.coin = 1000;
seed.players.me1.inv.herb = 20;
seed.market = { old1: { uid: 'me2', nick: '서연', look: 2, item: 'mush', qty: 1, price: 15, at: 1 } };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] });
  const page = async u => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(3000);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const S = await page('me1'), B = await page('me2');
  const goTab = async (p, t) => { await p.evaluate(() => __T.openSheet('market')); await p.waitForTimeout(600); await p.evaluate(t => { const x = document.querySelector(`[data-mtab="${t}"]`); if (x) x.click(); }, t); await p.waitForTimeout(500); };
  const M = p => p.evaluate(() => JSON.parse(JSON.stringify(window.__tree.market || {})));
  // 1 올리기: 약초 12 개 · 1 개 10G
  await goTab(S, 'mine'); await S.evaluate(() => document.querySelector('[data-pick="herb"]').click()); await S.waitForTimeout(300);
  await S.evaluate(() => { document.getElementById('qty').value = 12; document.getElementById('price').value = 10; document.getElementById('list').click(); }); await S.waitForTimeout(1200);
  let m = await M(S), id = Object.keys(m).find(k => m[k].uid === 'me1');
  ok(id && m[id].qty === 12 && m[id].price === 10 && m[id].earn === 0, '12 개를 한 칸에 올려요 ' + JSON.stringify(m[id]));
  await S.screenshot({ path: __dirname + '/shot_market_mine.png' });
  // 2 친구가 5 개 사기
  await goTab(B, 'shop'); const row = await B.evaluate(() => [...document.querySelectorAll('.li')].map(l => l.innerText.replace(/\n/g, ' ')).find(t => /약초/.test(t)));
  ok(/12 개 남음/.test(row) && /10 \/ 개/.test(row), '친구 가게: 남은 개수 · 1 개 값 ' + row);
  await B.screenshot({ path: __dirname + '/shot_market_shop.png' });
  const coin0 = await B.evaluate(() => __T.meGet().coin);
  await B.evaluate(id => document.querySelector(`[data-buy="${id}"]`).click(), id); await B.waitForTimeout(400);
  await B.evaluate(() => { document.getElementById('nbIn').value = '5'; }); await B.keyboard.press('Enter'); await B.waitForTimeout(1200);
  m = await M(B);
  ok(m[id].qty === 7 && m[id].earn === 50 && (await B.evaluate(() => __T.meGet().coin)) === coin0 - 50, '5 개 사면 7 개 남고 50G 쌓여요 ' + JSON.stringify(m[id]));
  // 3 판 사람: 받기 (남은 7 개는 그대로)
  await goTab(S, 'mine'); const t3 = await S.evaluate(() => document.querySelector('.box.px').innerText.replace(/\n/g, ' '));
  ok(/7 개 남음/.test(t3) && /50G 쌓임/.test(t3), '내 가판대: 남은 개수 · 쌓인 골드 ' + t3);
  const c1 = await S.evaluate(() => __T.meGet().coin); await S.evaluate(id => document.querySelector(`[data-collect="${id}"]`).click(), id); await S.waitForTimeout(1000);
  m = await M(S); ok(m[id] && m[id].qty === 7 && m[id].earn === 0 && (await S.evaluate(() => __T.meGet().coin)) === c1 + 50, '받기: 50G 받고 남은 7 개는 계속 팔아요');
  // 4 남은 것 다 사기 → 다 팔림 → 받기 뒤 사라져요
  await goTab(B, 'shop'); await B.evaluate(id => document.querySelector(`[data-buy="${id}"]`).click(), id); await B.waitForTimeout(400);
  await B.evaluate(() => { document.getElementById('nbIn').value = '7'; }); await B.keyboard.press('Enter'); await B.waitForTimeout(1200);
  m = await M(B); ok(m[id].qty === 0 && m[id].earn === 70, '7 개 다 사기');
  ok(!(await B.evaluate(() => /약초/.test((document.querySelector('.box.px') || {}).innerText || ''))), '다 팔리면 친구 가게에서 안 보여요');
  await goTab(S, 'mine'); await S.evaluate(id => document.querySelector(`[data-collect="${id}"]`).click(), id); await S.waitForTimeout(1000);
  m = await M(S); ok(!m[id], '다 팔린 묶음은 받기 뒤 사라져요');
  // 5 예전 한 개짜리 사기 · 내리기
  await goTab(S, 'shop'); await S.evaluate(() => document.querySelector('[data-buy="old1"]').click()); await S.waitForTimeout(1200);
  m = await M(S); ok(m.old1 && m.old1.buyer === 'me1', '예전 한 개짜리도 바로 사져요');
  await goTab(S, 'mine'); await S.evaluate(() => document.querySelector('[data-pick="herb"]').click()); await S.waitForTimeout(300);
  await S.evaluate(() => { document.getElementById('qty').value = 3; document.getElementById('price').value = 20; document.getElementById('list').click(); }); await S.waitForTimeout(1200);
  m = await M(S); const id2 = Object.keys(m).find(k => m[k].uid === 'me1' && m[k].qty === 3); const h0 = await S.evaluate(() => (__T.meGet().inv || {}).herb);
  await S.evaluate(id => document.querySelector(`[data-cancel="${id}"]`).click(), id2); await S.waitForTimeout(1200);
  m = await M(S); ok(!m[id2], '내리기: 남은 3 개를 돌려받아요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
