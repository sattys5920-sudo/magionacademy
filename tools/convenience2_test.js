// 편의 기능 2 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/convenience2_test.js
//   메뉴 「오늘」(열린 이벤트 · 할 일 · 가기) · 꾸미기 모자 · 액세서리 「없음」 · 가방 찾기 · 정렬 · 가판대 「최대」 · 전투 2 배속 (혼자만)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.tw = { ctl: { open: true, at: 1 } };
seed.players.me1.tw = { best: 2, seen: 1, d: '', n: 0, rw: {} };
seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 } };
seed.players.me1.inv.herb = 12;
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const C = (f, a) => p.evaluate(f, a), ev = s => C(s => __tw.ev(s), s);
  // 1 오늘
  await ev("(tab = 'home', sub = null, openSheet('home', 'menu'))").catch(() => {}); await ev("render()"); await p.waitForTimeout(300);
  await ev("openSheet('home', 'today')"); await p.waitForTimeout(500);
  const t = await C(() => document.querySelector('.panel') ? document.querySelector('.panel').innerText : '');
  ok(/지금 열린 이벤트/.test(t) && /시련의 탑/.test(t) && /최고 2 층/.test(t) && /오늘 할 일/.test(t) && /탐사/.test(t) && /남음/.test(t) && /오늘의 운세/.test(t), '오늘: 열린 이벤트 · 할 일 ' + t.replace(/\n/g, ' / ').slice(0, 200));
  await p.screenshot({ path: __dirname + '/shot_today.png' });
  await C(() => [...document.querySelectorAll('[data-today]')].find(b => b.dataset.today === 'x').click()); await p.waitForTimeout(600);
  ok(await ev("sheetOn && sub === 'explore'"), '할 일 「탐사」 → 탐사 창');
  // 2 꾸미기 모자 · 액세서리
  await ev("(closeSheet(), me.closet = me.closet || {}, me.closet['hat:' + World.Avatar.meta.parts.hat[1].id] = 1, me.av.hat = 1, save())");
  await ev("(avDraft = null, avSel = AV_SHEET_CATS.findIndex(x => x[1] === 'hat'), openSheet('home', 'avatar'))"); await p.waitForTimeout(800);
  const av = await C(() => ({ tabs: [...document.querySelectorAll('[data-avs]')].map(b => b.textContent), opts: [...document.querySelectorAll('[data-avp]')].map(b => b.innerText) }));
  ok(av.tabs.includes('모자') && av.tabs.includes('액세서리') && av.opts.includes('없음') && av.opts.includes('비니'), '꾸미기 소품: 모자 · 액세서리 칸 · 「없음」 ' + JSON.stringify(av));
  await C(() => document.querySelector('[data-avp="hat,0"]').click()); await p.waitForTimeout(300);
  ok(await ev("avDraft.hat === 0"), '「없음」을 고르면 모자를 벗어요');
  await p.screenshot({ path: __dirname + '/shot_avatar_hat.png' });
  // 3 가방 찾기 · 정렬
  await ev("(closeSheet(), bagTab = 'all', bagQ = '', openSheet('home', 'bag'))").catch(() => {}); await p.waitForTimeout(600);
  if (!(await C(() => !!document.getElementById('bagQ')))) await ev("(tab = 'home', openSheet('home', 'bag'))");
  const n0 = await C(() => document.querySelectorAll('[data-bsel]').length);
  await p.fill('#bagQ', '약초'); await p.waitForTimeout(400);
  const n1 = await C(() => document.querySelectorAll('[data-bsel]').length);
  ok(n0 > 1 && n1 === 1, `가방 찾기: ${n0} 칸 → 「약초」 ${n1} 칸`);
  await p.fill('#bagQ', ''); await p.waitForTimeout(300); await C(() => document.querySelector('[data-bsort="n"]').click()); await p.waitForTimeout(300);
  const ns = await C(() => [...document.querySelectorAll('[data-bsel] .n')].map(x => +x.textContent));
  ok(ns.length > 1 && ns.every((x, i) => !i || ns[i - 1] >= x), '많은 순 정렬 ' + ns.slice(0, 6));
  await p.screenshot({ path: __dirname + '/shot_bag_tools.png' });
  // 4 가판대 최대
  await ev("(closeSheet(), marketTab = 'mine', sellPick = 'herb', openSheet('market'))"); await p.waitForTimeout(600);
  await C(() => document.getElementById('qtyMax').click());
  ok(await C(() => document.getElementById('qty').value) === '12', '가판대 「최대」 → 12');
  // 5 2 배속 (시련의 탑 · 혼자)
  await ev("closeSheet()"); await C(() => __tw.TW().go(1, 0)); await p.waitForTimeout(1200);
  ok(await C(() => !!document.getElementById('xfast')), '혼자 전투에 2 배속 버튼');
  await C(() => document.getElementById('xfast').click()); await p.waitForTimeout(300);
  ok(await ev("me.xfast === 1 && xFastK(xb) === 2"), '켜면 2 배');
  ok(await ev("!xFastOk({ raid: {} }) && !xFastOk({ mirror: true }) && !xFastOk({ gr: {} })"), '레이드 · 파티 화면 · 승급 시험은 2 배속 없음');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
