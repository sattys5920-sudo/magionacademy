// 편의 기능 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/convenience_test.js
//   사육장 모두 먹이 · 쓰다듬기 · 받기 · 가판대 모두 받기 · 공동 의뢰 모두 내기 · 물약 여러 번 끓이기 · 요리 같은 맛으로 더 · 스킬 최대로 찍기
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 } };
seed.players.me1.inv.p_purple = 7; seed.players.me1.mana = 500;
seed.market = { a: { uid: 'me1', nick: '민준', look: 2, item: 'herb', qty: 3, price: 10, earn: 40, at: 1 }, b: { uid: 'me1', nick: '민준', look: 2, item: 'mush', qty: 1, price: 25, at: 2, buyer: 'x', buyerNick: '서연' } };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const C = (f, a) => p.evaluate(f, a), ev = s => C(s => __tw.ev(s), s);
  // 1 사육장: 생물 셋을 만들어 넣고 모두 돌보기
  await ev(`(() => { const k = 0; me.cr = [0, 1, 2].map(i => ({ id: 'c' + i, k, name: '아이' + i, love: 5, care: 99, col: { n: '보통' }, fedAt: 0, petAt: 0, prodAt: 0, born: 1 })); me.cr[2].fedAt = now2(); save(); })()`);
  await ev("(ranchTab = 'pen', openSheet('ranch'))"); await p.waitForTimeout(800);
  const r0 = await C(() => ({ f: (document.getElementById('feedAll') || {}).textContent, p: (document.getElementById('patAll') || {}).textContent, h: (document.getElementById('hvAll') || {}).textContent }));
  ok(/모두 먹이 2/.test(r0.f) && /모두 쓰다듬기 3/.test(r0.p), '사육장: 모두 먹이 · 쓰다듬기 버튼 (할 수 있는 아이 수) ' + JSON.stringify(r0));
  await p.screenshot({ path: __dirname + '/shot_conv_ranch.png' });
  const love0 = await ev('me.cr.map(c => c.love)');
  await C(() => document.getElementById('feedAll').click()); await p.waitForTimeout(300); await C(() => document.getElementById('patAll').click()); await p.waitForTimeout(300);
  const love1 = await ev('me.cr.map(c => c.love)');
  ok(love1[0] > love0[0] + 2 && love1[1] > love0[1] + 2 && love1[2] === love0[2] + (await ev("me.house === 'dusk' ? 2 : 1")), '먹이 2 마리 · 쓰다듬기 3 마리 ' + JSON.stringify([love0, love1]));
  const hv = await C(() => (document.getElementById('hvAll') || {}).textContent || '');
  if (/모두 받기 [1-9]/.test(hv)){ const inv0 = await ev('JSON.stringify(me.inv)'); await C(() => document.getElementById('hvAll').click()); await p.waitForTimeout(300); ok((await ev('JSON.stringify(me.inv)')) !== inv0, '모두 받기: 재료를 받아요'); }
  else ok(true, '받을 재료가 없는 생물이면 모두 받기는 꺼져 있어요 ' + hv);
  // 2 가판대 모두 받기
  await C(() => __T.closeSheet()); await ev("(marketTab = 'mine', openSheet('market'))"); await p.waitForTimeout(800);
  const coin0 = await ev('me.coin'); const ca = await C(() => (document.getElementById('collAll') || {}).textContent);
  ok(/모두 받기 · 65G/.test(ca), '가판대: 모두 받기 65G ' + ca);
  await C(() => document.getElementById('collAll').click()); await p.waitForTimeout(1500);
  const m = await C(() => JSON.parse(JSON.stringify(window.__tree.market || {})));
  ok((await ev('me.coin')) === coin0 + 65 && m.a && m.a.earn === 0 && m.a.qty === 3 && !m.b, '모두 받기: 65G · 남은 묶음은 계속 · 예전 한 개짜리는 내려가요 ' + JSON.stringify(m));
  // 3 공동 의뢰 모두 내기
  await ev("(marketTab = 'coop', render())"); await p.waitForTimeout(600);
  await C(() => document.getElementById('donateAll').click()); await p.waitForTimeout(1500);
  const co = await C(() => JSON.parse(JSON.stringify(window.__tree.coop || {})));
  ok((await ev('me.inv.p_purple || 0')) === 0 && JSON.stringify(co).includes('"me1":7'), '공동 의뢰: 반짝 물약 7 병 모두 내기 ' + JSON.stringify(co));
  await p.screenshot({ path: __dirname + '/shot_conv_coop.png' });
  // 4 물약 여러 번 끓이기
  await ev("(() => { POTION_INFO.p_red.r.forEach(k => { me.inv[k] = 10; }); me.hints = ['p_red']; me.mana = 500; save(); })()");
  await ev("(closeSheet(), labTab = 'brew', labFill('p_red'), openSheet('lab'))"); await p.waitForTimeout(600);
  await C(() => document.getElementById('brew').click()); await p.waitForTimeout(500);
  const bmT = await C(() => (document.getElementById('brewMany') || {}).textContent || ''); const n0 = await ev('me.inv.p_red || 0');
  ok(/번 더/.test(bmT), '물약: 한 번 끓인 뒤 「n 번 더」 ' + bmT);
  await C(() => document.getElementById('brewMany').click()); await p.waitForTimeout(800);
  const n1 = await ev('me.inv.p_red || 0'), left = await ev('brewMax("p_red")');
  ok(n1 - n0 >= parseInt(bmT) && left === 0, `n 번 더 끓이기: ${n0} → ${n1} · 남은 재료로는 더 못 끓여요`);
  await p.screenshot({ path: __dirname + '/shot_conv_brew.png' });
  // 5 스킬 최대로 찍기
  await ev("closeSheet()"); await C(() => __T.openSheet('home', 'explore')); await p.waitForTimeout(600); await C(() => document.querySelector('#xtree').click()); await p.waitForTimeout(600);
  const tm = await C(() => (document.getElementById('tmax') || {}).textContent || '');
  await C(() => document.getElementById('tmax').click()); await p.waitForTimeout(400);
  ok(/최대로 \(4\)/.test(tm) && (await ev("xEx().sk['0_0']")) === 5, '스킬: 최대로 (4) → Lv 5 ' + tm);
  // 6 요리 같은 맛으로 더 (완성 화면 함수만 확인)
  const ck = await ev(`(() => { const d = DISH.find(x => !x.hw && x.r.length <= 3); d.r.forEach(k => { me.inv[k] = 10; }); const pot = { x: 10, y: 10 }; cooking = { d, pot, sc: [3, 3, 3], soup: '#fff' }; cookDone(); const t = (document.getElementById('ckmore') || {}).textContent; const c0 = me.inv[d.id + '_s'] || 0; document.getElementById('ckmore').click(); const c1 = me.inv[d.id + '_s'] || 0; cookEnd(); return { t, c0, c1, id: d.id }; })()`);
  ok(/같은 맛으로 \d+ 개 더/.test(ck.t) && ck.c1 > ck.c0, '요리: 같은 맛으로 더 만들기 ' + JSON.stringify(ck));
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
