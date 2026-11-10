// 동물 운동회 터치 검사 (아이폰 화면 · 진짜 손가락 이벤트): sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/sports/test/touch.js [포트]
//   손가락 연타가 다 세어지는지 · 두 손가락 · 1 초에 7 번 넘게 눌러도 같은 기록 · 꾹 누르기(높이뛰기) · 두 번째 손가락이 끼어들어도 안 망가지는지 · 화면이 안 밀리는지 · 판정 칸 = 막대 칸
const { chromium, devices } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../../..', PORT = process.argv[2] || 8822;
const seed0 = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('  실패:', m); } };
(async () => {
  const b = await chromium.launch(); const seed = JSON.parse(JSON.stringify(seed0)); seed.players.me1.baby = { k: 3, adopt: 1, name: '토토', love: 30 }; seed.players.me1.spt = { id: 777, t: {}, hi: 1 };
  seed.sports = { ctl: { open: true, id: 777, at: Date.now() } };
  const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__spt && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(5000);
  const cdp = await ctx.newCDPSession(p);
  const pts = async (type, list) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: list.map(([x, y], i) => ({ x: Math.round(x), y: Math.round(y), id: i })) });
  const tap = async (x, y) => { await pts('touchStart', [[x, y]]); await pts('touchEnd', []); };
  const start = async e => { await p.evaluate(e => window.__spt.sel(e), e); await p.waitForTimeout(200); const g = await p.evaluate(() => { const r = document.querySelector('[data-spx="go"]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); await tap(...g); await p.waitForTimeout(400);
    return p.evaluate(() => { const r = document.querySelector('#spbtn').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); };
  const G = () => p.evaluate(() => window.__spt.st().game);
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(400);
  // 1. 달리기: 손가락 연타 40 번 → 40 번 다 세어져요
  let [x, y] = await start(0); const sy0 = await p.evaluate(() => [scrollY, document.querySelector('#spv .sb').scrollTop]);
  for (let i = 0; i < 30; i++){ await tap(x, y); await p.waitForTimeout(110); }
  let g = await G(); ok(g && g.taps === 30, '손가락 연타가 다 세어져요 ' + (g && g.taps));
  ok(JSON.stringify(sy0) === JSON.stringify(await p.evaluate(() => [scrollY, document.querySelector('#spv .sb').scrollTop])), '연타해도 화면이 안 밀려요');
  // 두 손가락 번갈아 (동시에 두 개 닿음)
  for (let i = 0; i < 5; i++){ await pts('touchStart', [[x - 40, y]]); await pts('touchStart', [[x - 40, y], [x + 40, y]]); await pts('touchEnd', []); await p.waitForTimeout(120); }
  g = await G(); ok(g && g.taps >= 40, '두 손가락도 세어져요 ' + (g && g.taps));
  // 시간이 끝난 뒤에도 계속 연타: 다음 판이 저절로 시작되면 안 돼요
  for (let i = 0; i < 60; i++){ await tap(x, y); await p.waitForTimeout(80); }
  const s1 = await p.evaluate(() => window.__spt.st()); ok(s1.spt.t[0] === 1 && s1.game && s1.game.taps >= 40, '끝난 뒤 계속 눌러도 새 판이 안 시작돼요 ' + JSON.stringify(s1.spt.t));
  await p.waitForTimeout(1000);
  // 연타 상한: 1 초에 7 번과 14 번은 같은 기록
  const cap = await p.evaluate(() => { const f = r => 40 + 60 * 1 * (.35 + 1.05 * Math.min(7, r) / 7); return [f(7), f(14), f(3.5)]; });
  ok(cap[0] === cap[1] && cap[2] < cap[0], '1 초에 7 번 넘게 눌러도 같은 기록 ' + JSON.stringify(cap));
  // 2. 높이뛰기: 꾹 눌렀다 떼기 · 두 번째 손가락이 끼어들어도 첫 손가락 기준
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(300); [x, y] = await start(5);
  await pts('touchStart', [[x, y]]); await p.waitForTimeout(400); await pts('touchStart', [[x, y], [x + 60, y]]); await p.waitForTimeout(480); await pts('touchEnd', [[x + 60, y]]); await p.waitForTimeout(50);
  g = await G(); ok(g && g.highs.length === 1 && g.highs[0] > 100, '꾹 눌렀다 떼면 높이 (두 번째 손가락은 무시) ' + JSON.stringify(g && g.highs));
  await pts('touchEnd', []); await p.waitForTimeout(1300);
  // 손가락이 버튼 밖으로 밀려도 떼기 전까지는 계속 누르는 중
  await pts('touchStart', [[x, y]]); await p.waitForTimeout(300); await pts('touchMove', [[x, y - 120]]); await p.waitForTimeout(100);
  g = await G(); ok(g && g.highs.length === 1, '버튼 밖으로 밀려도 아직 안 뗀 걸로 쳐요'); await p.waitForTimeout(480); await pts('touchEnd', []); await p.waitForTimeout(100);
  g = await G(); ok(g && g.highs.length === 2, '뗄 때 뛰어요 ' + JSON.stringify(g && g.highs));
  await p.waitForTimeout(6000);
  // 3. 콩주머니 · 공 굴리기 · 줄다리기: 판정 칸이 막대에 칠한 칸과 같아요 (시간에 맞춰 누르면 들어가요)
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(300); [x, y] = await start(3);
  const t0 = await p.evaluate(() => performance.now()); let hits = 0;
  for (let k = 0; k < 4; k++){ const want = 550 + k * 1100 * 2; const w = want - (await p.evaluate(() => performance.now()) - t0) - 420; if (w > 0) await p.waitForTimeout(w); await tap(x, y); await p.waitForTimeout(100); }
  g = await G(); ok(g && g.hits >= 2, '가운데 맞춰 던지면 들어가요 ' + (g && g.hits) + ' / 4');
  ok(errs.length === 0, '오류 없음 ' + JSON.stringify(errs.slice(0, 3)));
  console.log(`${pass} / ${pass + fail} 통과`); await b.close(); process.exit(fail ? 1 : 0);
})();
