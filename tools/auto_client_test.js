// 자동 이벤트 (서버 없이 학생 화면이 시간표로 계산): sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/auto_client_test.js
//   유령 열차: 한국 시간 10 · 14 · 19 · 23 시에 같은 번호 · 같은 행선지로 와요 · 운행이 끝나면 사라져요 · 관리자가 끄면 안 와요
//   별 보는 밤: 22:30 모이기 → 참가 → 별 나눠 주기 → 내 별 켜기(alit) · 스텔라 별 · 남은 별 저절로 → 하늘 → 이야기(별빛 효과 받음) → 끝 · 관리자가 연 밤이 먼저
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  const at = (h, m, sec = 0) => ev(`(() => { const n = Date.now(), d = new Date(n + 9 * 3600e3), want = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), ${h}, ${m}, ${sec}) - 9 * 3600e3; srvOff = want - n; return want; })()`);
  const wait = ms => p.waitForTimeout(ms);
  // 1 유령 열차
  const T19 = await at(19, 1); await ev('(gtChoose(), gtTick(), 1)');
  const g = await ev('JSON.stringify({ c: gtCtl, ph: gtPhase(), again: gtAuto() })'), G = JSON.parse(g);
  ok(G.c && G.c.auto && G.c.id === T19 - 60e3 && G.ph === 'board', '19:01 → 자동 열차가 승강장에 (번호 = 19:00) · ' + G.c?.dest);
  ok(G.again && G.again.dest === G.c.dest && G.again.id === G.c.id, '다시 계산해도 같은 번호 · 같은 행선지 (모든 학생이 같아요)');
  await at(19, 7); await ev('(gtChoose(), 1)'); ok(await ev("gtPhase() === 'dest'"), '19:07 → 목적지에서 채집 중');
  await at(19, 30); await ev('(gtChoose(), 1)'); ok(await ev("!gtAuto() && !['board','out','dest','in','back'].includes(gtPhase())"), '19:30 → 운행 끝 (열차 없음)');
  await at(23, 2); await ev('(gtChoose(), 1)'); ok(await ev("gtCtl && gtCtl.auto && gtPhase() === 'board'"), '23:02 → 밤 11 시 열차');
  await ev(`F.update(F.ref(db, 'autocfg'), { gtOff: true })`); await wait(300); await ev('(gtChoose(), 1)');
  ok(await ev("!gtAuto() && !(gtCtl && gtCtl.auto)"), '관리자가 끄면 자동 열차 없음');
  await ev(`F.update(F.ref(db, 'autocfg'), { gtOff: false })`); await wait(300);
  // 2 별 보는 밤
  await ev(`new Promise(r => { const t = setInterval(() => { if (sgData) { clearInterval(t); r(1); } }, 100); })`);
  const T = await at(22, 30, 30); await ev('(sgPick(true), sgSync(), 1)');
  ok(await ev("sgCtl && sgCtl.auto && sgCtl.open && sgCtl.ph === 'gather'"), '22:30 → 별 보는 밤 모이기 · 별자리 ' + await ev('sgCtl && sgCtl.c'));
  await ev(`F.set(F.ref(db, 'stargaze/join/old1'), { n: '어제', at: ${T} - 864e5 })`);   // 어제 참가 기록은 안 세요
  await ev(`F.set(F.ref(db, 'stargaze/join/' + myId()), { n: me.nick, at: now2() })`); await wait(400); await ev('(sgPick(true), 1)');
  ok(await ev("Object.keys(sgJoin).length === 1 && sgJoin[myId()]"), '참가 (어제 기록은 빼고 1 명)');
  await at(22, 33, 5); await ev('(sgPick(true), sgSync(), 1)');
  ok(await ev("sgCtl.ph === 'assign' && Object.values(sgCtl.asg).includes(myId())"), '별 나눠 주기 → 내 별 받음');
  await at(22, 33, 12); await ev('(sgPick(true), sgSync(), 1)');
  const mine = await ev("Object.keys(sgCtl.asg).find(k => sgCtl.asg[k] === myId())");
  await at(22, 33, 20); await ev('(sgPick(true), 1)');
  ok(await ev("sgCtl.ph === 'light' && Object.keys(sgLit).length >= 1 && !sgLit['" + mine + "']"), '별 켜기: 스텔라 별이 차례로 켜져요 · 내 별은 아직');
  await ev(`sgLight('${mine}')`); await wait(500); await ev('(sgPick(true), 1)');
  ok(await ev(`!!sgLit['${mine}'] && new Promise(r => F.onValue(F.ref(db, 'stargaze/alit/' + sgCtl.id), s => r(!!(s.val() || {})['${mine}'])))`), '내 별 켜기 → alit 에 기록');
  await at(22, 34, 13); await ev('(sgPick(true), sgSync(), 1)');
  ok(await ev("sgCtl.ph === 'sky' && Object.keys(sgLit).length === sgConst(sgCtl.c).stars.length"), '하늘 보기: 남은 별도 다 켜짐');
  const P = JSON.parse(await ev('JSON.stringify(sgAutoPlan())'));
  await ev(`(srvOff += ${P.d0 + 1000} - now2(), sgPick(true), sgSync(), 1)`); await wait(1200);
  ok(await ev("sgCtl.ph === 'done' && me.sgd === sgCtl.id && Object.keys(me.buffs || {}).some(k => k.startsWith('buff_'))"), '이야기 → 별빛 효과 받음');
  await ev(`(srvOff += ${P.e0 + 1000} - now2(), sgPick(true), sgSync(), 1)`);
  ok(await ev("sgCtl.ph === 'end' && !sgCtl.open"), '끝 (' + Math.round((P.e0 - P.T) / 1000) + ' 초)');
  await ev(`(srvOff += ${P.e0 + 60000} - now2(), sgPick(true), 1)`); ok(await ev('!sgAutoPlan()'), '조금 뒤엔 자동 밤이 사라져요');
  await at(22, 31); await ev(`F.set(F.ref(db, 'stargaze/ctl'), { open: true, id: 5, c: 'teacup', ph: 'gather', at: now2() })`); await wait(400); await ev('(sgPick(true), 1)');
  ok(await ev("sgCtl.id === 5 && !sgCtl.auto"), '관리자가 연 밤이 있으면 그쪽이 먼저');
  ok(await ev(`/관리자 화면을 켜 두지 않아도/.test(adminAutoHTML())`), '관리자 카드');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
