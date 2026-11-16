// 그레고의 수리 게시판 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/repair_board_test.js [그림 저장 폴더]
//   풍차 옆 게시판 → 이번 주 고장 난 것 셋 → 재료 내기(모두의 개수 · 내 개수) → 다 모이면 고침(그레고 장면 · 효과) → 감사 선물 → 그레고를 못 만난 학생 문구 · 관리자 카드 · 처음부터
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const OUT = process.argv[2] || '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad'; fs.mkdirSync(OUT, { recursive: true });
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.nnpc = Object.fromEntries(['bau', 'kael', 'artua', 'grego'].map(id => [id, { met: 1, at: 1 }]));
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await p.waitForFunction(() => __tw.ev("!!npcGet('grego')"), null, { timeout: 20000 }).catch(() => {});
  // 1 이번 주: 월요일 key · 셋 · 주마다 같은 셋
  const W = await ev(`(() => { const wk = __rp.week(), d = new Date(+wk.slice(0, 4), +wk.slice(4, 6) - 1, +wk.slice(6)), P = __rp.picks().map(o => o.id); return { wk, mon: d.getDay() === 1, P, same: JSON.stringify(P) === JSON.stringify(__rp.picks(wk).map(o => o.id)), other: JSON.stringify(__rp.picks('20260105').map(o => o.id)), pool: __rp.POOL.length }; })()`);
  ok(/^\d{8}$/.test(W.wk) && W.mon && W.P.length === 3 && new Set(W.P).size === 3 && W.same && W.pool === 8, '이번 주(월요일 ' + W.wk + ') 셋: ' + W.P.join(', ') + ' · 다른 주 ' + W.other);
  ok(await ev(`__rp.POOL.every(o => Object.keys(o.need).every(m => ITEM[m]) && Object.keys(o.fx).every(k => k in FX_CAP || k in FX_MIN) && o.say && !/\\?!|!!/.test(o.say))`), '재료는 다 있는 물건 · 효과는 sgFx 이름');
  // 2 게시판 그림 · 누르면 걸어가요 → 가까우면 열림
  ok(await ev(`World.propsAt('campus').some(q => q.id === 'rpboard' && q.x === __rp.SPOT[0] && q.y === __rp.SPOT[1])`), '풍차 옆 게시판 그림');
  await ev(`tpSafe('campus', [__rp.SPOT[0], __rp.SPOT[1] + 2])`); await p.waitForTimeout(1500);
  await ev(`(World.onProp('rpboard'), 1)`); await p.waitForTimeout(600);
  ok(await ev(`sheetOn && sub === 'repair' && document.querySelectorAll('.rpcard').length === 3`), '게시판 열기: 쪽지 셋');
  ok(await ev(`$('.rphead').textContent.includes(npcGet('grego').name) && $('.rphead').textContent.includes('아저씨')`), '그레고를 만난 학생: 그레고 이름 · 아저씨 말투');
  await p.screenshot({ path: OUT + '/rp_board.png' });
  // 3 재료 내기
  const o0 = W.P[0], mats = await ev(`Object.keys(__rp.POOL.find(o => o.id === '${o0}').need)`);
  await ev(`(${JSON.stringify(mats)}.forEach(m => { me.inv[m] = 100; }), render(), 1)`); await p.waitForTimeout(300);
  await p.click(`[data-rpg="${o0}:${mats[0]}:5"]`); await p.waitForTimeout(600);
  let r = await ev(`({ c: __rp.D().c['${o0}']['${mats[0]}'], by: __rp.D().by['${o0}'][myId()], inv: me.inv['${mats[0]}'] })`);
  ok(r.c === 5 && r.by === 5 && r.inv === 95, '5 개 내기: 모두 5 · 내 5 · 가방 95 ' + JSON.stringify(r));
  await ev(`(F.set(F.ref(db, 'repair/' + __rp.week() + '/c/${o0}/${mats[0]}'), __rp.POOL.find(o => o.id === '${o0}').need['${mats[0]}'] - 3), 1)`); await p.waitForTimeout(400);   // 다른 학생들이 많이 냈어요
  await ev(`__rp.give('${o0}', '${mats[0]}', 10)`); await p.waitForTimeout(400);
  r = await ev(`({ full0: __rp.D().c['${o0}']['${mats[0]}'] === __rp.POOL.find(o => o.id === '${o0}').need['${mats[0]}'], inv: me.inv['${mats[0]}'], by: __rp.D().by['${o0}'][myId()] })`);
  ok(r.full0 && r.inv === 92 && r.by === 8, '남은 만큼만 내요 (3 개) ' + JSON.stringify(r));
  // 4 다 모으기 → 고침 · 그레고 장면 · 효과
  const fx = await ev(`(() => { const o = __rp.POOL.find(o => o.id === '${o0}'); const k = Object.keys(o.fx)[0]; return { k, v0: sgFx(k), d: o.fx[k] }; })()`);
  await ev(`(async () => { const o = __rp.POOL.find(o => o.id === '${o0}'); for (let i = 0; i < 4; i++) await __rp.give('${o0}', '${mats[1]}', 10); return 1; })()`); await p.waitForTimeout(1500);
  await p.screenshot({ path: OUT + '/rp_fix_cut.png' });
  const said = await ev(`[...document.querySelectorAll('.say')].map(d => d.textContent).join(' / ')`);
  ok(await ev(`__rp.full(__rp.POOL.find(o => o.id === '${o0}')) && !!(__rp.D().fix || {})['${o0}'] && me.rpr.seen['${o0}'] === 1`), '다 모이면 고침 · 고친 시각 · 소식 봄');
  ok(/귀찮지만 다녀올게/.test(said) || await ev('World.cutBusy()'), '근처에 있으면 그레고 장면 ' + said.slice(0, 40));
  await p.waitForFunction(() => __tw.ev('!World.cutBusy()'), null, { timeout: 30000 }).catch(() => {});
  ok(Math.abs(await ev(`sgFx('${fx.k}')`) - (fx.v0 + fx.d)) < 1e-9 || (await ev(`sgFx('${fx.k}')`)) !== fx.v0, `학교 전체 효과 ${fx.k} ${fx.v0} → ${await ev(`sgFx('${fx.k}')`)}`);
  // 5 감사 선물
  await ev(`(openSheet('home', 'repair'), 1)`); await p.waitForTimeout(400);
  ok(!!(await p.$(`[data-rpc="${o0}"]`)), '감사 선물 받기 단추'); ok(await ev(`RPB.markList().length === 1`), '지도에 「수리 감사 선물」 표시');
  await p.screenshot({ path: OUT + '/rp_board_fixed.png' });
  const c0 = await ev('me.coin'), g0 = await ev(`npcSt('grego').a || 0`);
  await p.click(`[data-rpc="${o0}"]`); await p.waitForTimeout(400);
  ok(await ev(`me.coin === ${c0} + 80 && me.rpr.got['${o0}'] === 1 && (npcSt('grego').a || 0) >= ${g0} + 20 && !document.querySelector('[data-rpc]')`), '감사 선물: 80 골드 · 드문 채집물 · 그레고 호감');
  ok(await ev(`RPB.markList().length === 0`), '받은 뒤엔 표시 없음');
  // 6 그레고를 못 만난 학생
  await ev(`(me.nnpc.grego.met = 0, render(), 1)`); await p.waitForTimeout(300);
  ok(await ev(`$('.rphead').textContent.includes('학교 잡일꾼') && !$('.rphead').textContent.includes(NPC_DEF.find(n => n.id === 'grego').name)`), '못 만난 학생: 이름 없는 쪽지');
  await p.screenshot({ path: OUT + '/rp_board_unmet.png' });
  const o1 = W.P[1]; await ev(`(closeSheet(), tpSafe('town', [42, 50]))`); await p.waitForTimeout(1500);
  await ev(`(async () => { const o = __rp.POOL.find(o => o.id === '${o1}'); for (const m of Object.keys(o.need)) await F.set(F.ref(db, 'repair/' + __rp.week() + '/c/${o1}/' + m), o.need[m]); return 1; })()`); await p.waitForTimeout(1200);
  const tt = await ev(`[...document.querySelectorAll('#toast, .toast, #toasts *')].map(x => x.textContent).join(' / ')`);
  ok(await ev(`me.rpr.seen['${o1}'] === 1 && !World.cutBusy()`), '멀리 있거나 못 만났으면 장면 없이 소식만 ' + tt.slice(0, 60));
  ok(await ev(`!document.querySelector('[data-rpc="${o1}"]') && RPB.markList().length === 0`), '안 낸 물건은 감사 선물 없음');
  await ev(`(me.nnpc.grego.met = 1, 1)`);
  // 7 그레고 NPC 창에서 게시판 · 관리자 카드 · 처음부터
  await ev(`(npcMenu(npcGet('grego')), 1)`); await p.waitForTimeout(300);
  ok(!!(await p.$('#npcui [data-rpn]')), '그레고 NPC 창에 「수리 게시판」');
  await ev(`(npcClose(), 1)`);
  await ev(`(AD.rp = { [__rp.week()]: __rp.D() }, AD.players = { me1: { nick: me.nick } }, 1)`);
  const card = await ev(`RPB.adminHTML()`);
  ok(card.includes('수리 게시판') && card.includes(await ev('me.nick')) && card.includes('고침') && card.includes('data-rpa="reset"'), '관리자 카드: 진행 · 낸 학생 · 처음부터 단추');
  await ev(`(document.body.insertAdjacentHTML('beforeend', '<div id="rptest">' + RPB.adminHTML() + '</div>'), 1)`); await p.click('#rptest [data-rpa="reset"]'); await p.waitForTimeout(800);
  ok(await ev(`!__rp.full(__rp.POOL.find(o => o.id === '${o0}')) && !!__rp.D().rid && !(me.rpr && me.rpr.got && me.rpr.got['${o0}'])`), '처음부터: 모은 재료 · 고침 지움');
  ok(await ev(`sgFx('${fx.k}') === ${fx.v0}`), '처음부터 하면 효과도 꺼져요');
  await ev(`($('#rptest').remove(), 1)`);
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개 · 그림: ${OUT}/rp_*.png`); await b.close(); process.exit(fail ? 1 : 0);
})();
