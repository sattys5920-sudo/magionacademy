// 동물 운동회 검사: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/sports/test/sports.js [포트]
//   천막 · 처음 알림 · 창 · 세 종목 미니게임 (응원 · 타이밍) · 기록 · 하루 3 번 · 애정 +1 · 기숙사 점수 · 시상식 보상 · 관리자 카드
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../../..', PORT = process.argv[2] || 8822, SH = __dirname + '/../shots'; fs.mkdirSync(SH, { recursive: true });
const seed0 = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('  실패:', m); } };
(async () => {
  const b = await chromium.launch(); const seed = JSON.parse(JSON.stringify(seed0)), me = seed.players.me1, now = Date.now();
  me.cr = [{ id: 'a1', k: 1, col: {}, name: '깡총', love: 10, care: 999, bornAt: 0, prodAt: 0, fedAt: 0, petAt: 0, bredAt: 0 }, { id: 'a2', k: 9, col: { n: '노을빛', p: .75, s: 2.6, h: -35, b: 1 }, name: '수염', love: 20, care: 999, bornAt: 0 }, { id: 'a3', k: 0, col: {}, name: '아기', love: 0, care: 0, bornAt: now }];
  seed.sports = { ctl: { open: true, id: 777, at: now }, rec: { 777: { 0: { u2: { s: 80, h: 'ember', k: 4, c: null, n: '까망', nk: '서연' }, u3: { s: 60, h: 'moon', k: 8, c: null, n: '부엉', nk: '지호' } } } } };
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__spt && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(6000);
  const st = () => p.evaluate(() => window.__spt.st());
  ok(await p.evaluate(() => World.propsAt('town').some(x => x.id === 'sptent')), '광장에 천막');
  ok(await p.evaluate(() => !!(__T.meRaw().spt && __T.meRaw().spt.hi)), '처음 알림 카드');
  await p.waitForTimeout(4500);
  await p.evaluate(() => World.teleport('town', [44, 48])); await p.waitForTimeout(2000); await p.screenshot({ path: SH + '/tent.png' });
  // 창
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(600); await p.screenshot({ path: SH + '/view_day1.png' });
  ok(await p.evaluate(() => document.querySelectorAll('[data-spc]').length === 3), '내 생물 셋이 보여요');
  ok(await p.evaluate(() => document.querySelector('[data-spc].on')?.dataset.spc === '0'), '달리기는 토끼가 먼저 골라져요');
  // 1 일째 달리기: 응원 연타
  await p.click('[data-spx="go"]'); await p.waitForTimeout(300);
  const box = await p.evaluate(() => { const r = document.querySelector('#spbtn').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
  for (let i = 0; i < 50; i++){ await p.mouse.move(box.x, box.y); await p.mouse.down(); await p.mouse.up(); await p.waitForTimeout(110); if (i === 25) await p.screenshot({ path: SH + '/run.png' }); }
  await p.waitForTimeout(3000); let s = await st();
  ok(s.recs[0] && s.recs[0].me1 && s.recs[0].me1.s > 60, '달리기 기록 ' + JSON.stringify(s.recs[0] && s.recs[0].me1));
  ok(s.spt.t[0] === 1, '하루 횟수 하나 씀'); ok(await p.evaluate(() => __T.meRaw().cr[0].love === 11), '처음 뛰면 애정 +1');
  await p.screenshot({ path: SH + '/run_end.png' });
  const r0 = s.recs[0].me1.s;
  // 두 번째: 거의 안 눌러요 → 기록은 그대로 (더 좋을 때만)
  await p.evaluate(() => window.__spt.view()); await p.click('[data-spx="go"]'); await p.waitForTimeout(9500); s = await st();
  ok(s.recs[0].me1.s === r0 && s.spt.t[0] === 2, '더 나쁜 기록은 안 바뀌어요');
  ok(s.rank[0][0].h === 'dew', '오늘 기숙사 1 등 ' + JSON.stringify(s.rank[0]));
  // 2 일째 공 굴리기
  await p.evaluate(() => __T.pkSet('sports/ctl', { open: true, id: 777, at: Date.now() - 864e5 })); await p.waitForTimeout(800);
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(400); await p.screenshot({ path: SH + '/view_day2.png' });
  ok(await p.evaluate(() => document.querySelector('[data-spc].on')?.dataset.spc === '1'), '공 굴리기는 염소가 먼저 골라져요');
  await p.click('[data-spx="go"]'); for (let k = 0; k < 3; k++){ await p.waitForFunction(() => { const s = window.__spt.st(); return true; }); await p.waitForTimeout(800); await p.evaluate(() => document.querySelector('#spbtn').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); if (k === 1) await p.screenshot({ path: SH + '/ball.png' }); }
  await p.waitForTimeout(2500); s = await st(); ok(s.recs[1] && s.recs[1].me1 && s.recs[1].me1.s > 0, '공 굴리기 기록 ' + JSON.stringify(s.recs[1] && s.recs[1].me1));
  // 3 일째 줄다리기
  await p.evaluate(() => __T.pkSet('sports/ctl', { open: true, id: 777, at: Date.now() - 2 * 864e5 })); await p.waitForTimeout(800);
  await p.evaluate(() => window.__spt.view()); await p.click('[data-spx="go"]');
  for (let i = 0; i < 30; i++){ await p.evaluate(() => document.querySelector('#spbtn') && document.querySelector('#spbtn').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(300); if (i === 15) await p.screenshot({ path: SH + '/tug.png' }); }
  await p.waitForTimeout(2000); s = await st(); ok(s.recs[2] && s.recs[2].me1, '줄다리기 기록 ' + JSON.stringify(s.recs[2] && s.recs[2].me1));
  ok(s.total[0].p > 0, '기숙사 합계 ' + JSON.stringify(s.total));
  // 하루 3 번
  await p.evaluate(() => { __T.meRaw().spt.t[2] = 3; window.__spt.view(); }); await p.waitForTimeout(300);
  ok(await p.evaluate(() => document.querySelector('[data-spx="go"]').disabled), '하루 3 번 뒤에는 출전 막힘');
  await p.evaluate(() => document.querySelector('[data-spx="x"]').click());
  // 시상식
  const coin0 = await p.evaluate(() => __T.meRaw().coin);
  await p.evaluate(() => __T.pkSet('sports/ctl', { open: true, id: 777, at: Date.now() - 3 * 864e5 })); await p.waitForTimeout(800);
  for (let i = 0; i < 20 && !(await p.evaluate(() => !!document.querySelector('#spv .pod'))); i++) await p.waitForTimeout(500);
  ok(await p.evaluate(() => !!document.querySelector('#spv .pod')), '넷째 날 시상식이 저절로 떠요'); await p.waitForTimeout(2000); await p.screenshot({ path: SH + '/ceremony.png' });
  const m = await p.evaluate(() => ({ coin: __T.meRaw().coin, tag: __T.meRaw().cos && __T.meRaw().cos.tag }));
  const win = s.total[0].h === 'dew'; ok(m.coin - coin0 === (win ? 1500 : 500), `보상 골드 ${m.coin - coin0}`); ok(m.tag && m.tag.sports && (!win || m.tag.sportswin), '이름표 ' + JSON.stringify(m.tag));
  // 관리자 카드
  await p.evaluate(() => document.querySelector('#spv [data-spx="x"]').click()); await p.evaluate(() => __T.showAdmin()); await p.waitForTimeout(1500);
  await p.evaluate(() => { const t = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === '게임'); t && t.click(); }); await p.waitForTimeout(500);
  await p.evaluate(() => { const t = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === '이벤트'); t && t.click(); }); await p.waitForTimeout(800);
  ok(await p.evaluate(() => /동물 운동회/.test(document.body.innerText) && !!document.querySelector('[data-spa]')), '관리자 카드');
  ok(errs.length === 0, '오류 없음 ' + JSON.stringify(errs.slice(0, 3)));
  console.log(`${pass} / ${pass + fail} 통과`); await b.close(); process.exit(fail ? 1 : 0);
})();
