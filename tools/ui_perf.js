// 성능: 맵에서 10 초 걷기 + 지도 열고 닫기 + 물약 교실 열기 → 평균 FPS, 긴 작업(50ms+), 입력 지연. CPU 1배·4배 감속
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 12, inv: { herb: 5, drop: 4 }, cr: [], eggs: [], orders: [], hints: [], fdex: {}, rod: 1, closet: {} } } };
(async () => {
  const [vw, vh] = (process.argv[2] || '390x844').split('x').map(Number);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const out = {};
  for (const rate of [1, 4]){
    const p = await b.newPage({ viewport: { width: vw, height: vh }, hasTouch: false });
    const cdp = await p.context().newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate });
    await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1';
      window.__perf = { frames: [], long: [], ev: [] };
      new PerformanceObserver(l => l.getEntries().forEach(e => __perf.long.push(e.duration))).observe({ type: 'longtask', buffered: true });
      try { new PerformanceObserver(l => l.getEntries().forEach(e => __perf.ev.push({ n: e.name, d: e.duration, delay: e.processingStart - e.startTime }))).observe({ type: 'event', durationThreshold: 16, buffered: true }); } catch(e){}
    }, seed);
    await p.goto('http://localhost:'+(process.env.PORT||8766)+'/'); await p.waitForTimeout(4500);
    await p.evaluate(() => { __perf.long = []; __perf.ev = []; __perf.frames = []; let last = performance.now(); const f = t => { __perf.frames.push(t - last); last = t; if (__perf.on) requestAnimationFrame(f); }; __perf.on = true; requestAnimationFrame(f); });
    // 10 초 걷기: 화면을 번갈아 눌러요
    const pts = [[vw * .2, vh * .3], [vw * .8, vh * .7], [vw * .75, vh * .25], [vw * .25, vh * .75]];
    for (let i = 0; i < 7; i++){ await p.mouse.click(...pts[i % 4]); await p.waitForTimeout(1430); }
    const walk = await p.evaluate(() => { __perf.on = false; const fr = __perf.frames.slice(5), avg = fr.reduce((a, b) => a + b, 0) / fr.length; return { fps: +(1000 / avg).toFixed(1), worst: Math.round(Math.max(...fr)), jank: fr.filter(x => x > 50).length, long: __perf.long.length, longMax: Math.round(Math.max(0, ...__perf.long)) }; });
    // 지도 열고 닫기, 물약 교실 열기
    await p.evaluate(() => { __perf.long = []; __perf.ev = []; });
    await p.evaluate(() => { document.querySelector('#npcui [data-nx="close"]')?.click(); __T.closeSheet(); }); await p.waitForTimeout(300);
    for (let i = 0; i < 3; i++){ await p.evaluate(() => document.querySelector('#tMap').click()); await p.waitForTimeout(700); await p.evaluate(() => document.querySelector('#mClose').click()); await p.waitForTimeout(400); }
    await p.evaluate(() => __T.openSheet('lab', null)); await p.waitForTimeout(800);
    const ui = await p.evaluate(() => ({ long: __perf.long.length, longMax: Math.round(Math.max(0, ...__perf.long)), inputDelay: Math.round(Math.max(0, ...__perf.ev.map(e => e.delay))), inputDur: Math.round(Math.max(0, ...__perf.ev.map(e => e.d))) }));
    const dom = await p.evaluate(() => document.querySelectorAll('*').length);
    out['cpu' + rate] = { walk, ui, dom }; await p.close();
  }
  console.log(JSON.stringify(out)); await b.close();
})();
