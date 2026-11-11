// 거대 알 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/egg_mock/egg_test.js
//   시작 연출 · 돌봐 주기 (하루 한 번 · 골드 · 이야기) · 금 단계 · 부화 (가장 많은 기운 · 고르면 무지개) · 부화 연출 · 이름 후보 · 투표 · 마스코트 · 관리자 카드
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const K = new Date(Date.now() + 9 * 3600e3), TD = `${K.getUTCFullYear()}-${K.getUTCMonth() + 1}-${K.getUTCDate()}`;
seed.egg = { ctl: { open: true, d0: TD, at: 1 } };
(async () => {
  const b = await chromium.launch(), errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'] });
  const page = async (u, opt) => { const p = await ctx.newPage(); if (opt && opt.viewport) await p.setViewportSize(opt.viewport); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const ad = await page('admin', { viewport: { width: 1000, height: 900 } });
  const p = await page('me1', { ...devices['iPhone 13'] }), C = (f, a) => p.evaluate(f, a), E = () => '__tw.EG()';
  await p.waitForFunction(() => document.getElementById('famcut'), null, { timeout: 20000 }).catch(() => {});
  ok(await C(() => !!document.getElementById('famcut')), '처음 들어오면 별똥별 시작 연출');
  await p.waitForTimeout(5000); await p.screenshot({ path: __dirname + '/shot_e_intro.png' });
  await p.waitForFunction(() => __tw.EG().S().seen, null, { timeout: 30000 }); await p.waitForTimeout(800);
  await C(() => new Promise(r => World.teleport('town', [44, 51], () => setTimeout(r, 1500)))); await p.waitForTimeout(1500);
  await p.screenshot({ path: __dirname + '/shot_e_map.png' });
  await C(() => World.onProp('egg')); await p.waitForTimeout(500);
  const w = await C(() => ({ t: (document.querySelector('#eggv .hd b') || {}).textContent, n: document.querySelectorAll('#eggv [data-ega]').length }));
  ok(/1 일째/.test(w.t) && w.n === 3, '알을 누르면 돌봐 주기 창 (1 일째 · 세 가지) ' + JSON.stringify(w));
  const coin0 = await C(() => __T.meGet().coin);
  await C(() => document.querySelector('#eggv [data-ega="star"]').click()); await p.waitForTimeout(300);
  await C(() => { document.querySelector('#eggv textarea').value = '오늘 탑 3 층까지 갔어'; document.querySelector('#eggv [data-egs]').click(); }); await p.waitForTimeout(1200);
  const r1 = await C(() => ({ coin: __T.meGet().coin, care: JSON.parse(JSON.stringify(((window.__tree.egg || {}).care || {}).me1 || {})), story: JSON.parse(JSON.stringify(((window.__tree.egg || {}).story || {}).me1 || {})), dis: [...document.querySelectorAll('#eggv [data-ega]')].every(b => b.disabled) }));
  const d = Object.keys(r1.care)[0];
  ok(r1.coin === coin0 + 30 && r1.care[d] && r1.care[d].k === 'star' && r1.story[d] === '오늘 탑 3 층까지 갔어' && r1.dis, '이야기로 돌봐 주면 별 기운 · 골드 +30 · 이야기는 따로 저장 · 오늘은 끝 ' + JSON.stringify(r1));
  await p.screenshot({ path: __dirname + '/shot_e_care.png' });
  // 여러 날 · 여러 친구가 돌봤다고 치고 금 단계 · 부화할 아이
  const st = await C(() => { const cr = {}; for (let i = 0; i < 12; i++){ const u = 'u' + i; cr[u] = {}; for (let d = 1; d <= 6; d++) cr[u]['2026-1-' + d] = { k: i < 6 ? 'fire' : i < 9 ? 'wind' : 'star', at: 1 }; } const E = __tw.EG(); E._set(undefined, cr); const T = E.tot(); return { T, k: E.kind() }; });
  ok(st.T.n === 72 && st.k === 0, '가장 많은 기운으로 태어날 아이가 정해져요 (불 → 아기 불새) ' + JSON.stringify(st));
  const rb = await C(() => { const cr = {}; for (let i = 0; i < 12; i++){ cr['u' + i] = { '2026-1-1': { k: ['fire', 'wind', 'star'][i % 3], at: 1 } }; } const E = __tw.EG(); E._set(undefined, cr); return E.kind(); });
  ok(rb === 3, '세 기운이 고르면 아기 무지개 용');
  // 부화
  await C(td => { const E = __tw.EG(); const cr = {}; for (let i = 0; i < 9; i++) cr['u' + i] = { '2026-1-1': { k: i < 5 ? 'wind' : 'fire', at: 1 } }; E._set({ open: true, d0: td, hd: td, kind: 1 }, cr, {}); E.S().hs = 0; }, TD);
  await p.waitForFunction(() => document.getElementById('famcut'), null, { timeout: 15000 }).catch(() => {});
  ok(await C(() => !!document.getElementById('famcut')), '부화하면 광장에서 부화 연출');
  await p.waitForTimeout(6500); await p.screenshot({ path: __dirname + '/shot_e_hatch.png' });
  await p.waitForFunction(() => __tw.EG().S().hs, null, { timeout: 30000 }); await p.waitForTimeout(1500);
  await p.screenshot({ path: __dirname + '/shot_e_baby.png' });
  await C(() => World.onProp('egg')); await C(() => __tw.EG().win()); await p.waitForTimeout(400);
  const v0 = await C(() => ({ t: document.querySelector('#eggv .card').innerText, inp: !!document.querySelector('#eggv [data-egn]') }));
  ok(/아기 구름 고래/.test(v0.t) && v0.inp, '아기 창: 이름 후보 내기 ' + v0.t.slice(0, 60).replace(/\n/g, ' / '));
  await C(() => { document.querySelector('#eggv [data-egn]').value = '몽실이'; document.querySelector('#eggv [data-egc]').click(); }); await p.waitForTimeout(800);
  await C(() => document.querySelector('#eggv [data-egv]').click()); await p.waitForTimeout(800);
  const v1 = await C(() => ({ t: document.querySelector('#eggv .card').innerText, vote: JSON.parse(JSON.stringify((window.__tree.egg || {}).vote || {})) }));
  ok(v1.vote.cand && v1.vote.cand.me1 === '몽실이' && v1.vote.pick && v1.vote.pick.me1 === 'me1' && /1 표/.test(v1.t), '후보 내고 한 표 ' + JSON.stringify(v1.vote));
  await p.screenshot({ path: __dirname + '/shot_e_vote.png' });
  await C(() => { const v = document.getElementById('eggv'); if (v) v.remove(); __tw.EG()._set({ open: true, d0: '2026-1-1', hd: '2026-1-1', kind: 1, vc: true, name: '몽실이' }); });
  ok(await C(() => __tw.EG().name()) === '몽실이', '투표가 끝나면 1 등 이름');
  await C(() => World.onProp('eggpet')); await p.waitForTimeout(400);
  const pb = await C(() => ({ pd: __tw.EG().S().pd, b: (document.getElementById('buffChip') || {}).textContent || '' }));
  await C(() => World.onProp('eggpet')); await p.waitForTimeout(300);
  ok(!!pb.pd && /입질/.test(pb.b), '아기를 누르면 하루 한 번 버프 (구름 고래 → 입질↑) ' + JSON.stringify(pb));
  ok(await C(() => !document.querySelector('[data-egf]')), '같이 걷기는 없어요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  // 관리자 카드
  await ad.evaluate(() => __T.showAdmin()); await ad.waitForTimeout(1500); await ad.evaluate(() => window.__adPoll && window.__adPoll()); await ad.waitForTimeout(800);
  await ad.evaluate(() => [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent).click()); await ad.waitForTimeout(1500);
  const card = await ad.evaluate(() => { const c = [...document.querySelectorAll('.adcard')].find(c => c.querySelector('.abhead') && c.querySelector('.abhead').textContent.includes('거대 알')); if (!c) return ''; if (c.classList.contains('shut')) c.querySelector('.abhead b').click(); return [...document.querySelectorAll('.adcard')].find(c => c.querySelector('.abhead') && c.querySelector('.abhead').textContent.includes('거대 알')).innerText; });
  ok(/일째|태어났어요/.test(card) && /오늘 탑 3 층까지 갔어/.test(card) && /몽실이/.test(card), '관리자 카드: 진행 · 이야기 · 이름 후보 ' + card.slice(0, 160).replace(/\n/g, ' / '));
  await ad.screenshot({ path: __dirname + '/shot_e_admin.png' });
  ok(!errs.length, '페이지 오류 없음 (관리자) ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
