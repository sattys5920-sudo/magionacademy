// 막대과자 답례 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/stickday/reply_test.js
//   이미 오투모에게 준 연애 상대 → 새로고침하면 고백 답례 상자가 내 방에 · 상자를 안 준 NPC 에게 주면 답례 · 이미 준 NPC 는 또 안 줘요
const { chromium } = require('playwright'); const fs = require('fs');
const seed0 = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const bx = (m, st) => ({ c: 1, t: 0, b: 0, k: 0, r: 0, s: 3, at: 1, m, st });
(async () => {
  const br = await chromium.launch(), seed = JSON.parse(JSON.stringify(seed0)), errs = [];
  seed.npcs = { ...(seed.npcs || {}), __romance: { otumo: 'me1' } };
  Object.assign(seed.players.me1, { otumo: { met: 1 }, stk: { ev: '2026-11-11', gv: 1, hi: 1, npc: { otumo: 7 }, rw: {} } });
  seed.stick = { ctl: { open: true, at: 1 },
    box: { me1: { mad: bx('마들렌', '마들렌'), n_otumo: bx('삐빅. 막대 다섯 개 포장 완료. 기쁨도 같이 넣었습니다.', '오투모'), n_kappa: bx('갓파 쪽지', '갓파') } },
    hold: { me1: { h1: bx('나비 받아'), h2: bx('갓파 받아') } } };
  const ctx = await br.newContext({ viewport: { width: 1000, height: 900 } }), p = await ctx.newPage();
  p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(([s]) => { window.__seed = s; window.__uid = 'me1'; }, [seed]);
  await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(6000);
  const get = () => p.evaluate(() => JSON.parse(JSON.stringify(((window.__tree.stick || {}).box || {}).me1 || {})));
  let b = await get();
  ok(b.n_otumolove && /고백 신호/.test(b.n_otumolove.m) && b.n_otumo.m.startsWith('삐빅. 막대 다섯'), '이미 준 연애 상대: 새로고침하면 고백 답례 상자 ' + JSON.stringify(b.n_otumolove));
  await p.evaluate(() => __stk.npcGive('nabi', 'h1')); await p.waitForTimeout(2500);
  await p.evaluate(() => __stk.npcGive('kappa', 'h2')); await p.waitForTimeout(2500);
  b = await get();
  ok(b.n_nabi && b.n_nabi.st && b.n_nabi.m, '상자 안 준 NPC 에게 주면 답례 상자 ' + JSON.stringify(b.n_nabi));
  ok(b.n_kappa.m === '갓파 쪽지' && Object.keys(b).filter(k => /kappa/.test(k)).length === 1, '이미 준 NPC 는 또 안 줘요');
  ok(Object.keys(b).length === 5, '상자 수 ' + Object.keys(b).join(','));
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await br.close(); process.exit(fail ? 1 : 0);
})();
