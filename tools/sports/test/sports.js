// 동물 운동회 검사: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/sports/test/sports.js [포트]
//   천막 · 처음 알림 · 창(여섯 종목 · 아기 동물) · 종목마다 미니게임 · 기록 · 종목마다 3 번 · 친밀도 +1 (하루 한 번) · 12 명 한 트랙 · 기숙사 점수 · 관리자가 연 시상식 · 보상 · 관리자 카드
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../../..', PORT = process.argv[2] || 8822, SH = __dirname + '/../shots'; fs.mkdirSync(SH, { recursive: true });
const seed0 = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('  실패:', m); } };
(async () => {
  const b = await chromium.launch(); const seed = JSON.parse(JSON.stringify(seed0)), me = seed.players.me1, now = Date.now();
  me.baby = { k: 3, adopt: 1, name: '토토', love: 30 };   // 입양한 아기 토끼 · 친밀도 ♥3
  const H = ['ember', 'moon', 'dusk', 'dew'], NK = ['서연', '지호', '하린', '도윤', '수아', '예준', '지아', '시우', '하은', '주원', '유나'];
  const run = {}; NK.forEach((n, i) => { run['u' + i] = { s: 50 + i * 6, h: H[i % 4], k: i % 12, n: '아기' + i, nk: n }; });   // 달리기에 11 명 → 나까지 12 명
  seed.sports = { ctl: { open: true, id: 777, at: now }, rec: { 777: { 0: run } } };
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__spt && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(6000);
  const st = () => p.evaluate(() => window.__spt.st());
  const press = () => p.evaluate(() => { const b = document.querySelector('#spbtn'); b && b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); });
  const release = () => p.evaluate(() => { const b = document.querySelector('#spbtn'); b && b.dispatchEvent(new PointerEvent('pointerup', { bubbles: true })); });
  ok(await p.evaluate(() => World.propsAt('town').some(x => x.id === 'sptent')), '광장에 천막');
  ok(await p.evaluate(() => !!(__T.meRaw().spt && __T.meRaw().spt.hi)), '처음 알림 카드'); await p.waitForTimeout(4500);
  await p.evaluate(() => World.teleport('town', [44, 48])); await p.waitForTimeout(2000); await p.screenshot({ path: SH + '/tent.png' });
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(600); await p.screenshot({ path: SH + '/view.png' });
  ok(await p.evaluate(() => document.querySelectorAll('[data-spe]').length === 6), '여섯 종목 한꺼번에');
  ok(await p.evaluate(() => /토토/.test(document.querySelector('#spv .sppet').innerText) && !/잘해요|서툴러요|보통이에요/.test(document.querySelector('#spv').innerText)), '아기 동물 · 잘해요 같은 말 없음');
  // 0 달리기 (12 명 한 트랙)
  const go = async e => { await p.waitForTimeout(1600); await p.evaluate(e => window.__spt.sel(e), e); await p.waitForTimeout(200); await p.click('[data-spx="go"]'); await p.waitForTimeout(300); };
  await go(0); for (let i = 0; i < 50; i++){ await press(); await p.waitForTimeout(110); if (i === 30) await p.screenshot({ path: SH + '/run.png' }); } await p.waitForTimeout(3000);
  let s = await st(); ok(s.recs[0] && s.recs[0].me1 && s.recs[0].me1.s > 60, '달리기 기록 ' + JSON.stringify(s.recs[0] && s.recs[0].me1));
  ok(await p.evaluate(() => /반 \d+ 등 \/ 12 명/.test(document.querySelector('#spmsg').textContent)), '반 등수 · 12 명 ' + await p.evaluate(() => document.querySelector('#spmsg').textContent));
  ok(await p.evaluate(() => __T.meRaw().baby.love === 31), '하루 처음 뛰면 친밀도 +1');
  // 1 장애물 넘기: 장애물마다 맞춰 점프
  await go(1); const t0 = Date.now(); for (let k = 0; k < 9; k++){ const at = 900 + k * 1100 - 600; const w = at - (Date.now() - t0); if (w > 0) await p.waitForTimeout(w); await press(); if (k === 3) await p.screenshot({ path: SH + '/hurdle.png' }); } await p.waitForTimeout(2500);
  s = await st(); ok(s.recs[1] && s.recs[1].me1 && s.recs[1].me1.s > 0, '장애물 넘기 기록 ' + JSON.stringify(s.recs[1] && s.recs[1].me1));
  ok(await p.evaluate(() => __T.meRaw().baby.love === 31), '친밀도는 하루 한 번만');
  // 2 공 굴리기
  await go(2); for (let k = 0; k < 3; k++){ await p.waitForTimeout(800); await press(); if (k === 1) await p.screenshot({ path: SH + '/ball.png' }); } await p.waitForTimeout(2500);
  s = await st(); ok(s.recs[2] && s.recs[2].me1, '공 굴리기 기록');
  // 3 콩주머니 던지기
  await go(3); for (let i = 0; i < 22; i++){ await press(); await p.waitForTimeout(460); if (i === 8) await p.screenshot({ path: SH + '/toss.png' }); } await p.waitForTimeout(1500);
  s = await st(); ok(s.recs[3] && s.recs[3].me1 && s.recs[3].me1.s > 0, '콩주머니 기록 ' + JSON.stringify(s.recs[3] && s.recs[3].me1));
  // 4 줄다리기
  await go(4); for (let i = 0; i < 30; i++){ await press(); await p.waitForTimeout(300); if (i === 15) await p.screenshot({ path: SH + '/tug.png' }); } await p.waitForTimeout(1500);
  s = await st(); ok(s.recs[4] && s.recs[4].me1, '줄다리기 기록');
  // 5 높이뛰기: 꾹 눌렀다 꼭대기에서 떼기
  await go(5); for (let k = 0; k < 3; k++){ await press(); await p.waitForTimeout(880); await release(); await p.waitForTimeout(300); if (k === 1) await p.screenshot({ path: SH + '/high.png' }); await p.waitForTimeout(1000); } await p.waitForTimeout(1500);
  s = await st(); ok(s.recs[5] && s.recs[5].me1 && s.recs[5].me1.s > 60, '높이뛰기 기록 ' + JSON.stringify(s.recs[5] && s.recs[5].me1));
  // 종목마다 3 번
  await p.evaluate(() => { __T.meRaw().spt.t[0] = 3; window.__spt.sel(0); }); await p.waitForTimeout(300);
  ok(await p.evaluate(() => document.querySelector('[data-spx="go"]').disabled), '한 종목 3 번 뒤에는 막힘');
  await p.evaluate(() => { window.__spt.sel(1); }); ok(await p.evaluate(() => !document.querySelector('[data-spx="go"]').disabled), '다른 종목은 그대로');
  await p.screenshot({ path: SH + '/view_after.png' });
  ok(s.total.some(t => t.p > 0), '기숙사 점수 ' + JSON.stringify(s.total));
  await p.evaluate(() => document.querySelector('[data-spx="x"]').click());
  // 관리자가 시상식을 열면
  const coin0 = await p.evaluate(() => __T.meRaw().coin);
  await p.evaluate(() => __T.pkSet('sports/ctl', { open: true, id: 777, at: Date.now(), end: Date.now() })); await p.waitForTimeout(800);
  for (let i = 0; i < 20 && !(await p.evaluate(() => !!document.querySelector('#spv .pod'))); i++) await p.waitForTimeout(500);
  ok(await p.evaluate(() => !!document.querySelector('#spv .pod')), '시상식이 모두에게 떠요'); await p.waitForTimeout(2000); await p.screenshot({ path: SH + '/ceremony.png' });
  s = await st(); const m = await p.evaluate(() => ({ coin: __T.meRaw().coin, tag: __T.meRaw().cos && __T.meRaw().cos.tag })), win = s.total[0].h === 'dew';
  ok(m.coin - coin0 === (win ? 1500 : 500), `보상 골드 ${m.coin - coin0}`); ok(m.tag && m.tag.sports && (!win || m.tag.sportswin), '이름표 ' + JSON.stringify(m.tag));
  // 관리자 카드
  await p.evaluate(() => document.querySelector('#spv [data-spx="x"]').click()); await p.evaluate(() => __T.showAdmin()); await p.waitForTimeout(1500);
  await p.evaluate(() => { const t = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === '게임'); t && t.click(); }); await p.waitForTimeout(500);
  await p.evaluate(() => { const t = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === '이벤트'); t && t.click(); }); await p.waitForTimeout(800);
  ok(await p.evaluate(() => /동물 운동회/.test(document.body.innerText) && !!document.querySelector('[data-spa="uncer"]')), '관리자 카드 (시상식 중)');
  ok(errs.length === 0, '오류 없음 ' + JSON.stringify(errs.slice(0, 3)));
  console.log(`${pass} / ${pass + fail} 통과`); await b.close(); process.exit(fail ? 1 : 0);
})();
