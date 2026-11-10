// 동물 운동회 연출 영상: 시작 알림 카드 → 천막 → 달리기 한 판 → 시상식 · node tools/sports/test/video.js [포트] → tools/sports/shots/sports.mp4 (webm)
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../../..', PORT = process.argv[2] || 8822, OUT = __dirname + '/../shots';
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.baby = { k: 3, adopt: 1, name: '토토', love: 30 };
const H = ['ember', 'moon', 'dusk', 'dew'], run = {}; ['서연', '지호', '하린', '도윤', '수아', '예준', '지아', '시우', '하은', '주원', '유나'].forEach((n, i) => { run['u' + i] = { s: 50 + i * 6, h: H[i % 4], k: i % 12, n: '아기' + i, nk: n }; });
const rec = { 0: run }; for (let e = 1; e < 6; e++){ rec[e] = {}; Object.entries(run).forEach(([u, x], i) => { rec[e][u] = { ...x, s: 20 + ((i * 7 + e * 5) % 40) }; }); }
seed.sports = { ctl: { open: true, id: 777, at: Date.now() }, rec: { 777: rec } };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, recordVideo: { dir: OUT + '/vid', size: { width: 390, height: 844 } } }); const p = await ctx.newPage();
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__spt, null, { timeout: 30000 });
  await p.waitForTimeout(9000);   // 시작 알림 카드
  await p.evaluate(() => World.teleport('town', [44, 49])); await p.waitForTimeout(2500);
  await p.evaluate(() => window.__spt.view()); await p.waitForTimeout(2500);
  await p.click('[data-spx="go"]'); for (let i = 0; i < 56; i++){ await p.evaluate(() => { const b = document.querySelector('#spbtn'); b && b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await p.waitForTimeout(140); } await p.waitForTimeout(3000);
  await p.evaluate(() => document.querySelector('[data-spx="back"]') && document.querySelector('[data-spx="back"]').click()); await p.waitForTimeout(2000);
  await p.evaluate(() => document.querySelector('[data-spx="x"]').click());
  await p.evaluate(() => __T.pkSet('sports/ctl', { open: true, id: 777, at: Date.now(), end: Date.now() })); await p.waitForTimeout(9000);
  const v = p.video(); await ctx.close(); await b.close(); fs.renameSync(await v.path(), OUT + '/sports.webm'); console.log('ok');
})();
