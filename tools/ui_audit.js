// UI 측정: 3 가지 화면 크기 × 모든 화면 → 스크린숏 + 수치 (JSON). 사용: node tools/ui_audit.js <출력 폴더> [포트] [axe.min.js 경로]
//   먼저 tools/ui_mock.sh 로 모의 서버를 띄워요. 출력: <폴더>/{phone,tablet,pc}/<화면>.png, <폴더>/metrics.json
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const OUT = process.argv[2], PORT = process.argv[3] || 8766, AXE_PATH = process.argv[4] || '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/audtools/node_modules/axe-core/axe.min.js';
const AXE = fs.existsSync(AXE_PATH) ? fs.readFileSync(AXE_PATH, 'utf8') : '';
const SIZES = [['phone', 390, 844], ['tablet', 820, 1180], ['pc', 1440, 900]];
const seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 55, inv: { herb: 5, drop: 4, mush: 3, g_mint: 6, f_crucian: 2, p_red: 1 }, cr: [], eggs: [], orders: [], hints: ['p_red'], found: ['p_red'], fdex: {}, rod: 1, closet: {}, fbag: { candle: 1 }, npc: { nabi: { a: 250, seen: { 1: 'ok' } } } } }, story: { live: { ch: 1, at: 1 } } };
const skipStory = async p => { for (let i = 0; i < 12; i++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } };
const SCREENS = [
  ['world', null], ['map', async p => p.click('#tMap')], ['talk', async p => p.click('#tChat')],
  ['npc_talk', async p => p.evaluate(() => __T.npcMenu(__T.npcGet('nabi')))],
  ['heart_event', async p => p.evaluate(async () => { const ev = await __T.npcEvent('nabi', 1); __T.evPlay(__T.npcGet('nabi'), 1, ev, { replay: true }); })],
  ['story_vn', async p => p.evaluate(() => __T.storyPlay(1))],
  ...['home', 'lab', 'green', 'ranch', 'market'].map(t => ['sheet_' + t, async p => p.evaluate(t => __T.openSheet(t, null), t)]),
  ...['avatar', 'clothes', 'class', 'dorm', 'fish', 'games', 'cook', 'npcgift', 'npcstory', 'bag', 'profile', 'rel', 'journal', 'menu', 'settings'].map(s => ['sub_' + s, async p => p.evaluate(s => __T.openSheet('home', s), s)]),
];
async function measure(p){
  if (AXE) await p.addScriptTag({ content: AXE });
  return p.evaluate(async () => {
    const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0 && r.bottom > 0 && r.right > 0 && r.top < innerHeight && r.left < innerWidth; };
    const D = document.documentElement, pageScroll = D.scrollHeight > innerHeight + 1 || D.scrollWidth > innerWidth + 1;
    const panel = document.querySelector('#app.open .panel'); const innerScroll = panel ? [panel.scrollHeight, panel.clientHeight] : null;
    const pnl = document.querySelector('#app.open .pnl'); const pr = pnl && pnl.getBoundingClientRect(); const pnlIn = pr ? pr.left >= -1 && pr.top >= -1 && pr.right <= innerWidth + 1 && pr.bottom <= innerHeight + 1 : null;
    let small = 0, small15 = 0; const smallEx = [];
    document.querySelectorAll('body *').forEach(el => { if (!vis(el)) return; const t = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()); if (!t) return; const fsz = parseFloat(getComputedStyle(el).fontSize); if (fsz < 13){ small++; if (smallEx.length < 5) smallEx.push(el.className + ':' + fsz); } if (fsz < 15 && (el.matches('.vntx, .evtext, .npct, p, .t') )) small15++; });
    let touch = 0; const touchEx = []; document.querySelectorAll('button, a[href], input, select, textarea, [role=button]').forEach(el => { if (!vis(el)) return; const r = el.getBoundingClientRect(); if (r.width < 44 || r.height < 44){ touch++; if (touchEx.length < 5) touchEx.push((el.id || el.className) + ':' + Math.round(r.width) + 'x' + Math.round(r.height)); } });
    let contrast = -1; if (typeof axe !== 'undefined'){ try { const r = await axe.run(document, { runOnly: ['color-contrast'] }); contrast = r.violations.reduce((t, v) => t + v.nodes.length, 0); } catch(e){} }
    return { pageScroll, innerScroll, pnlIn, small, smallEx, touch, touchEx, contrast };
  });
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const rows = [];
  for (const [nm, w, h] of SIZES){
    fs.mkdirSync(`${OUT}/${nm}`, { recursive: true });
    { const p = await b.newPage({ viewport: { width: w, height: h } }); await p.addInitScript(() => { window.__seed = { players: {} }; }); await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(2500);
      await p.screenshot({ path: `${OUT}/${nm}/login.png` }); rows.push({ size: nm, screen: 'login', ...(await measure(p)) }); await p.close(); }
    for (const [sc, open] of SCREENS){
      const p = await b.newPage({ viewport: { width: w, height: h } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
      await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
      await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500); if (sc !== 'story_vn') await skipStory(p);
      try { if (open) await open(p); } catch(e){ errs.push('open: ' + e.message.split('\n')[0]); }
      await p.waitForTimeout(1200);
      await p.screenshot({ path: `${OUT}/${nm}/${sc}.png` });
      rows.push({ size: nm, screen: sc, ...(await measure(p)), errs }); await p.close();
    }
  }
  fs.writeFileSync(`${OUT}/metrics.json`, JSON.stringify(rows, null, 1)); console.log('done', rows.length); await b.close();
})();
