// 자동 이벤트 화면 쪽 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/auto_client_test.js
//   한국 시간 20:01 이면 유령 열차 신호 · 21:05 이면 별 보는 밤 신호를 autoreq 에 한 번 남겨요 · 관리자 카드 · 끄면 안 남겨요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  const at = (h, m) => `(() => { const n = Date.now(), d = new Date(n + 9 * 3600e3), want = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), ${h}, ${m}) - 9 * 3600e3; srvOff = want - n; return autoKst(now2()); })()`;
  const reqs = () => ev(`new Promise(r => F.onValue(F.ref(db, 'autoreq'), s => r(Object.keys(s.val() || {}))))`);
  const k1 = await ev(at(20, 1)); await ev('autoTick()'); await p.waitForTimeout(500);
  let R = await reqs(); ok(R.includes(`gt_${k1.ymd}_2000`), '20:01 → 유령 열차 신호 ' + R);
  ok(!R.some(x => x.startsWith('sg_')), '20:01 엔 별 보는 밤 신호 없음');
  await ev(at(21, 5)); await ev('autoTick()'); await p.waitForTimeout(500);
  R = await reqs(); ok(R.includes(`sg_${k1.ymd}`), '21:05 → 별 보는 밤 신호');
  await ev(at(20, 30)); await ev('(autoTick.sent = {}, autoTick())'); await p.waitForTimeout(300);
  ok((await reqs()).length === R.length, '20:30 (5 분 지남) → 새 신호 없음');
  await ev(`F.update(F.ref(db, 'autocfg'), { gtOff: true })`); await p.waitForTimeout(300);
  await ev(at(22, 2)); await ev('autoTick()'); await p.waitForTimeout(300);
  ok(!(await reqs()).some(x => x.endsWith('_2200')), '관리자가 끄면 22:02 신호 없음');
  ok(await ev(`/자동 이벤트/.test(adminAutoHTML()) && /유령 열차/.test(adminAutoHTML()) && /꺼짐/.test(adminAutoHTML())`), '관리자 카드: 자동 이벤트 · 꺼짐 표시');
  ok(await ev(`(sgCtl = { open: true, srv: 1, ph: 'gather', at: now2(), c: 'teacup' }, sgAdminTick() === undefined)`), '서버가 진행 중인 별 보는 밤은 관리자 화면이 손대지 않아요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
