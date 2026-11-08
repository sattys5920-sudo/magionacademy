// 스킬 트리 화면 캡처 (390×844): node tools/balance/skill_tree_shots.js [포트] → tools/balance/shots/tree_<직업>.png
//   먼저 `sh tools/ui_mock.sh /home/user/magionacademy <포트>` · 스킬을 몇 개 배운 학생으로 열어서 설명 · 다음 레벨 · 늦추기 안내 줄이 넘치지 않는지 봐요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const PORT = process.argv[2] || 8822, OUT = __dirname + '/shots';
const SHOTS = [['black', '1_2'], ['time', '2_4'], ['gadget', '1_0'], ['cleric', '0_1']];   // [직업, 고른 칸]
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [job, sel] of SHOTS){
    const sk = { '0_0': 2, '0_1': 1, '1_0': 3, '1_1': 2, '1_2': 2, '2_0': 1, '2_1': 1, '2_2': 1, '2_3': 1, '2_4': 1 };
    const seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 55, inv: {}, cr: [], eggs: [], orders: [], hints: [], found: [], fdex: {}, rod: 1, closet: {}, fbag: {}, npc: {}, mq: { q: null, st: 1, ph: 'arrive', prog: {}, done: {}, named: {}, dl: null }, ex: { exp: 40000, d: '', n: 0, xv: 3, job, sk, spx: 0 } } }, story: { live: { ch: 1, at: 1 } } };
    const p = await b.newPage({ viewport: { width: 390, height: 844 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
    await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
    for (let i = 0; i < 12; i++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
    await p.evaluate(() => __T.openSheet('home', 'explore')); await p.waitForTimeout(600);
    await p.click('#xtree'); await p.waitForTimeout(300);
    await p.click(`[data-ts="${sel}"]`); await p.waitForTimeout(300);
    const box = await p.$('#tup'); if (box) await box.scrollIntoViewIfNeeded();
    const over = await p.evaluate(() => { const a = [...document.querySelectorAll('.pnl *')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'auto' && getComputedStyle(e).overflowX !== 'scroll' && e.clientWidth > 0); return { pageX: document.documentElement.scrollWidth > innerWidth + 1, els: a.slice(0, 5).map(e => e.className) }; });
    await p.screenshot({ path: `${OUT}/tree_${job}.png` });
    console.log(job, sel, JSON.stringify(over), errs.length ? 'errors: ' + errs.slice(0, 2).join(' | ') : '');
    await p.close();
  }
  await b.close();
})();
