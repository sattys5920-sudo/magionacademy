// UI 검증 (지시서 9장): node tests/ui.spec.js [포트]
//   먼저 `tools/ui_mock.sh <저장소> <포트>` 로 모의 서버를 띄워요. 3 가지 화면 크기에서 모든 화면과 패널을 열어 확인해요.
//   1 페이지 스크롤 없음 · 2 패널이 화면 안 · 3 13px 미만 글씨 0 (대사·본문 15px 미만 0) · 4 명도 대비 위반 0 · 5 44px 미만 버튼 0
//   6 가방·내 정보·관계·일지·설정 열고 Esc·✕로 닫기 · 7 로그아웃 → 타이틀(모의: 확인 창까지) · 8 물약 제조 흐름 · 9 걷기 FPS(별도: tools/ui_perf.js)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const PORT = process.argv[2] || 8766;
const AXE_PATH = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/audtools/node_modules/axe-core/axe.min.js';
const AXE = fs.existsSync(AXE_PATH) ? fs.readFileSync(AXE_PATH, 'utf8') : '';
const SIZES = [[390, 844], [820, 1180], [1440, 900]];
const seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 55, inv: { herb: 5, drop: 4, mush: 3, g_mint: 6, f_crucian: 2, p_red: 1 }, cr: [], eggs: [], orders: [], hints: ['p_red'], found: ['p_red'], fdex: {}, rod: 1, closet: {}, fbag: { candle: 1 }, npc: { nabi: { a: 250, seen: { 1: 'ok' } } }, mq: { q: null, st: 1, ph: 'arrive', prog: {}, done: { main_01_dracula: 1, main_02_ghost: 1, main_03_witch: 1, main_04_werewolf: 1, main_05_mummy: 1, main_06_frankenstein: 1, main_07_jack: 1 }, named: {}, dl: null } } }, story: { live: { ch: 1, at: 1 } } };
const PANELS = ['bag', 'profile', 'rel', 'journal', 'menu', 'settings', 'avatar', 'clothes', 'class', 'dorm', 'fish', 'games', 'cook', 'npcgift', 'npcstory'];
const TABS = ['home', 'lab', 'green', 'ranch', 'market'];
let fails = 0, checks = 0;
const ok = (cond, msg) => { checks++; if (!cond){ fails++; console.log('  ✗', msg); } };
const skipStory = async p => { for (let i = 0; i < 12; i++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } };
async function metrics(p){
  if (AXE) await p.addScriptTag({ content: AXE });
  return p.evaluate(async () => {
    const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0 && r.bottom > 0 && r.right > 0 && r.top < innerHeight && r.left < innerWidth; };
    const D = document.documentElement;
    const pnl = document.querySelector('#app.open .pnl'); const r = pnl && pnl.getBoundingClientRect();
    let small = 0, talk = 0; const ex = [];
    document.querySelectorAll('body *').forEach(el => { if (!vis(el)) return; if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return; const f = parseFloat(getComputedStyle(el).fontSize); if (f < 13){ small++; ex.push(el.className + ':' + f); } if (f < 15 && el.matches('.vntx, .evtext, .npct, .sttx')) talk++; });
    let touch = 0; const tex = []; document.querySelectorAll('button, a[href], input, select, [role=button]').forEach(el => { if (!vis(el)) return; const b = el.getBoundingClientRect(); if (b.width < 44 || b.height < 44){ touch++; tex.push((el.id || el.className || el.tagName) + ':' + Math.round(b.width) + 'x' + Math.round(b.height)); } });
    let contrast = 0; if (typeof axe !== 'undefined'){ const a = await axe.run(document, { runOnly: ['color-contrast'] }); contrast = a.violations.reduce((t, v) => t + v.nodes.length, 0); }
    return { pageScroll: D.scrollHeight > innerHeight + 1 || D.scrollWidth > innerWidth + 1, pnlIn: r ? r.left >= -1 && r.top >= -1 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1 : true, small, ex: ex.slice(0, 4), talk, touch, tex: tex.slice(0, 4), contrast };
  });
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [w, h] of SIZES){
    console.log(`\n== ${w}×${h}`);
    const p = await b.newPage({ viewport: { width: w, height: h } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
    await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500); await skipStory(p);
    const screens = [['world', async () => {}], ['map', async () => { await p.click('#tMap'); }], ['talk', async () => { await p.click('#cH'); }], ['npc', async () => p.evaluate(() => __T.npcMenu(__T.npcGet('nabi')))],
      ...TABS.map(t => [t, async () => p.evaluate(t => __T.openSheet(t), t)]), ...PANELS.map(s => [s, async () => p.evaluate(s => { if (s === 'npcgift' || s === 'npcstory'){ __T.npcMenu(__T.npcGet('nabi')); document.querySelector('#npcui [data-nx="' + (s === 'npcgift' ? 'gift' : 'story') + '"]')?.click(); } else __T.openSheet('home', s); }, s)])];
    for (const [name, open] of screens){
      try { await open(); } catch(e){ ok(false, `${name}: 열기 실패 ${e.message.split('\n')[0]}`); }
      await p.waitForTimeout(500);
      const m = await metrics(p);
      ok(!m.pageScroll, `${name}: 페이지 스크롤 생김`);
      ok(m.pnlIn, `${name}: 패널이 화면 밖으로 나감`);
      ok(m.small === 0, `${name}: 13px 미만 글씨 ${m.small}개 ${m.ex.join(' ')}`);
      ok(m.talk === 0, `${name}: 대사 15px 미만 ${m.talk}`);
      ok(m.contrast === 0, `${name}: 명도 대비 위반 ${m.contrast}`);
      ok(m.touch === 0, `${name}: 44px 미만 버튼 ${m.touch}개 ${m.tex.join(' ')}`);
      // 닫기: 패널은 Esc, 그 밖은 각자
      if (name === 'world') {} else if (name === 'map') await p.click('#mClose'); else if (name === 'talk') await p.click('#cH'); else if (name === 'npc') await p.evaluate(() => document.querySelector('#npcui [data-nx="close"]')?.click());
      else { await p.keyboard.press('Escape'); await p.waitForTimeout(250); ok(!(await p.evaluate(() => document.querySelector('#app').classList.contains('open'))), `${name}: Esc로 안 닫힘`); }
      await p.waitForTimeout(200);
    }
    // 6. 새 패널: ✕로 닫기
    for (const s of ['bag', 'profile', 'rel', 'journal', 'settings']){ await p.evaluate(s => __T.openSheet('home', s), s); await p.waitForTimeout(300); await p.click('#sclose'); await p.waitForTimeout(250); ok(!(await p.evaluate(() => document.querySelector('#app').classList.contains('open'))), `${s}: ✕로 안 닫힘`); }
    // 7. 로그아웃 확인 창 (모의 서버라 실제 로그아웃 대신 확인 창까지)
    await p.evaluate(() => __T.openSheet('home', 'menu')); await p.waitForTimeout(300);
    const lo = await p.$('#logout, [data-menu="logout"], button:has-text("로그아웃")'); ok(!!lo, '메뉴: 로그아웃 버튼 없음');
    if (lo){ await lo.click(); await p.waitForTimeout(300); ok(await p.evaluate(() => document.querySelector('#confirm').classList.contains('on')), '로그아웃: 확인 창 안 뜸'); await p.evaluate(() => document.querySelector('#cfNo')?.click()); }
    await p.keyboard.press('Escape');
    // 8. 물약 제조: 레시피 → 끓이기 → 가방
    await p.evaluate(() => __T.openSheet('lab')); await p.waitForTimeout(300);
    await p.click('#recipePick'); await p.click('[data-recipe="p_red"]'); await p.waitForTimeout(200); await p.click('#brew'); await p.waitForTimeout(400);
    ok((await p.evaluate(() => __T.me().inv.p_red)) === 2, '물약 제조: 치유 물약이 가방에 안 들어감');
    ok(!(await p.evaluate(() => document.documentElement.scrollHeight > innerHeight + 1)), '물약 제조 중 페이지 스크롤');
    await p.evaluate(() => document.querySelector('#brewBag')?.click()); await p.keyboard.press('Escape');
    ok(errs.length === 0, `페이지 오류: ${errs.slice(0, 3).join(' | ')}`);
    await p.close();
  }
  console.log(`\n검사 ${checks}개 · 실패 ${fails}개`); await b.close(); process.exit(fails ? 1 : 0);
})();
