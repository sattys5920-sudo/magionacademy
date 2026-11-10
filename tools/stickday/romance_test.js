// 오투모 연애 상대 막대과자 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/stickday/romance_test.js
//   연애 상대는 하트와 상관없이 오투모의 고백 쪽지 상자를 받아요 · 아닌 학생은 원래 쪽지 · 줄 때 대사도 연애 버전
const { chromium } = require('playwright'); const fs = require('fs');
const seed0 = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const run = async (br, rom) => {
  const seed = JSON.parse(JSON.stringify(seed0)), errs = [];
  seed.npcs = { ...(seed.npcs || {}), __romance: rom ? { otumo: 'me1' } : {} }; seed.players.me1.otumo = { met: 1 };
  seed.stick = { ctl: { open: true, at: 1 }, hold: { me1: { h1: { c: 6, t: 0, b: 0, k: 0, r: 0, s: 3, at: 1, m: '받아 줘' } } } };
  const ctx = await br.newContext({ viewport: { width: 1000, height: 900 } }), p = await ctx.newPage();
  p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(([s]) => { window.__seed = s; window.__uid = 'me1'; }, [seed]);
  await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(5000);
  const box = await p.evaluate(() => JSON.parse(JSON.stringify(((window.__tree.stick || {}).box || {}).me1 || {})));
  const o = box.n_otumo;
  if (rom) ok(o && /고백 신호/.test(o.m) && o.b === 4, '연애 상대: 고백 쪽지 상자 ' + JSON.stringify(o));
  else ok(!o || !/고백 신호/.test(o.m), '연애 상대 아님: 고백 쪽지 없음 ' + JSON.stringify(o));
  await p.evaluate(() => __stk.npcGive('otumo', 'h1')); await p.waitForTimeout(2500);
  const say = await p.evaluate(() => document.body.innerText);
  if (rom) ok(/연인에게서 막대과자|당신이 준 거니까요/.test(say), '연애 상대: 받을 때 연애 대사');
  else ok(/삐빅. (캐러멜|막대과자 수령)/.test(say), '연애 상대 아님: 원래 대사');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3)); await ctx.close();
};
(async () => { const br = await chromium.launch(); await run(br, true); await run(br, false);
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await br.close(); process.exit(fail ? 1 : 0); })();
