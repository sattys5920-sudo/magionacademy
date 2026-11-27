// 메인 의뢰 7 「호박밭의 작별 인사」 도착 연출: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/mq7_arrive_test.js
//   잭의 호박밭(quarter 38, 24)에서 연출이 나오고 · 잭과 말풍선이 화면 안에 보여요 (스크린숏 tools/shot_mq7_*.png)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  for (let k = 0; k < 40 && await ev('World.cutBusy()'); k++){ await ev(`(document.querySelector('.mqskip')?.click(), 1)`); await p.waitForTimeout(500); }
  if (process.argv[2] === 'free'){   // 호박밭 둘레 걸을 수 있는 칸
    await ev(`new Promise(r => World.teleport('quarter', [38, 24], r))`); await p.waitForTimeout(1500);
    const g = await ev(`(() => { let s = ''; for (let y = 18; y <= 32; y++){ let l = String(y).padStart(2) + ' '; for (let x = 30; x <= 46; x++) l += World.isFree(x, y) ? '.' : '#'; s += l + '\\n'; } return s; })()`); console.log('    x 30..46\n' + g); await b.close(); return;
  }
  await ev(`(me.mq = { q: 'main_07_jack', st: 1, ph: 'arrive', prog: {}, done: {} }, mqRel = 99, MQ.list.includes('main_07_jack') || MQ.list.push('main_07_jack'), save(), 1)`).catch(e => console.log('  setq', e.message));
  await ev(`(mqArriving = false, mqArrive(), 1)`); await p.waitForTimeout(2500);
  ok(await ev(`World.where() === 'quarter'`), '잭의 호박밭 지도로 옮겨졌어요');
  const shots = [];
  for (let k = 0; k < 10; k++){
    await p.waitForTimeout(1300);
    const bub = await ev(`[...document.querySelectorAll('.say')].filter(e => e.offsetParent && e.textContent.trim()).map(e => { const r = e.getBoundingClientRect(); return { t: e.textContent.trim().slice(0, 20), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width) }; })`);
    if (bub.length){ shots.push(bub); if (shots.length === 1) await p.screenshot({ path: __dirname + '/shot_mq7_say.png' }); }
  }
  console.log('    말풍선', JSON.stringify(shots.slice(0, 4)));
  const vw = await p.evaluate(() => innerWidth), vh = await p.evaluate(() => innerHeight);
  ok(shots.length > 0 && shots.flat().every(s => s.x >= 0 && s.x + s.w <= vw && s.y >= 0 && s.y <= vh), '말풍선이 화면 안에 보여요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
