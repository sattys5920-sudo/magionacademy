// 요일 던전 검사: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/daydungeon/test/day.js [포트]
//   우물 모양(빛 · 판자 · 마른 우물) · 처음 연출 → 창 · 혼자 방 만들기 → 요일마다 전투 → 이기면 카드 · 보상 · 횟수 · 닫힌 뒤에도 입장
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../../..';
const PORT = process.argv[2] || 8822, SH = __dirname + '/../shots'; fs.mkdirSync(SH, { recursive: true });
const seed0 = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('  실패:', m); } };
async function page(b, seed){ const p = await b.newPage({ viewport: { width: 390, height: 844 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__dd && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(2500); p.errs = errs; return p; }
const st = p => p.evaluate(() => __dd.st());
async function fight(p, w, lv, shot){
  await p.evaluate(w => { const c = __T.meRaw(); }, w);
  await p.evaluate(() => __dd.panel()); await p.waitForTimeout(400);
  await p.click(`[data-ddl="${lv + 1}"]`); await p.waitForTimeout(500);
  await p.click('[data-rdl="make"]'); await p.waitForTimeout(800);
  await p.click('[data-rdl="start"]'); await p.waitForTimeout(5000);
  let s = await st(p); ok(s.xb && s.xb.R.w === w && s.xb.R.lv === lv, `전투 시작 (요일 ${w})`); if (!s.xb) return null;
  ok(s.xb.foes.length === (w === 3 ? 2 : 1), `보스 수 (요일 ${w}) ${s.xb.foes.length}`);
  await p.evaluate(() => { const B = __T.xbGet(); B.party.forEach(u => { u.mhp = Math.max(u.mhp, 1e7); u.hp = u.mhp; }); }); await p.waitForTimeout(9000);
  s = await st(p); if (shot) await p.screenshot({ path: `${SH}/battle_${w}.png` });
  return s;
}
(async () => {
  const b = await chromium.launch();
  // 1. 닫힌 채 못 본 학생: 마른 우물 · 열면 빛 · 연출 → 창
  { const seed = JSON.parse(JSON.stringify(seed0)); seed.day = { ctl: { open: false, test: 0 } }; seed.players.me1.ex = { exp: 300000, job: 'knight', d: '', n: 0, xv: 3 }; const p = await page(b, seed);
    let s = await st(p); ok(s.mode === 'dry', '닫힘 · 못 봄 → 마른 우물 ' + s.mode);
    await p.evaluate(() => __T.pkSet('day/ctl', { open: true, at: 1, test: 0 })); await p.waitForTimeout(800);
    s = await st(p); ok(s.mode === 'glow', '열림 → 빛 ' + s.mode);
    await p.evaluate(() => { World.teleport('town', [14, 57]); }); await p.waitForTimeout(3500);
    await p.evaluate(() => { const b = [...document.querySelectorAll('.ddskip')][0]; }); await p.waitForTimeout(500);
    let cut = await p.evaluate(() => World.cutBusy()); ok(cut, '가까이 가면 처음 연출');
    await p.screenshot({ path: SH + '/intro.png' });
    await p.evaluate(() => { const k = document.querySelector('.ddskip'); if (k) k.click(); }); await p.waitForTimeout(4000);
    s = await st(p); ok(s.seen, '건너뛰어도 본 걸로'); ok(await p.evaluate(() => !!document.querySelector('[data-ddl="1"]')), '연출 뒤 창이 열려요');
    await p.screenshot({ path: SH + '/panel.png' });
    await p.evaluate(() => { const x = document.querySelector('[data-rdx]'); x && x.click(); });
    // 닫아도 들어가요
    await p.evaluate(() => __T.pkSet('day/ctl', { open: false, at: 2, test: 0 })); await p.waitForTimeout(800);
    s = await st(p); ok(s.mode === 'glow', '연출 본 학생은 닫아도 빛 ' + s.mode);
    // 요일마다 전투
    for (const w of [0, 1, 2, 3, 4]){
      await p.evaluate(w => __T.pkSet('day/ctl', { open: false, at: 3, test: w }), w); await p.evaluate(() => { __T.meRaw().dd.n = 0; }); await p.waitForTimeout(600);
      const left0 = (await st(p)).left, coin0 = await p.evaluate(() => __T.meRaw().coin);
      const s2 = await fight(p, w, w === 4 ? 2 : 0, true); if (!s2) continue;
      ok(s2.xb.R.bc > 0, `보스가 움직여요 (요일 ${w}) bc ${s2.xb.R.bc} · ${s2.xb.log}`);
      if (w === 4) ok(s2.xb.foes.length > 1, `태엽 졸개 ${s2.xb.foes.length - 1}`);
      // 이기기
      await p.evaluate(() => { const B = __T.xbGet(); B.foes.forEach(f => { f.hp = 0; delete f.fx.shield; }); }); await p.waitForTimeout(4000);
      let s3 = await st(p); ok(s3.xb && s3.xb.over, `이겼어요 (요일 ${w}) ${s3.xb && s3.xb.log}`);
      await p.waitForTimeout(1500); const cards = await p.$$('[data-ddc]'); ok(cards.length === 3, `카드 셋 (요일 ${w}) ${cards.length}`);
      if (w === 0) await p.screenshot({ path: SH + '/cards.png' });
      if (cards.length) { await p.evaluate(() => document.querySelectorAll('[data-ddc]')[1].click()); await p.waitForTimeout(350); if (w === 0) await p.screenshot({ path: SH + '/cards_flip.png' }); await p.waitForTimeout(1800); }
      if (w === 0) await p.screenshot({ path: SH + '/cards_open.png' });
      const s4 = await st(p); ok(s4.left === left0 - 1, `횟수 하나 씀 (요일 ${w}) ${left0} → ${s4.left}`);
      const coin1 = await p.evaluate(() => __T.meRaw().coin); ok(coin1 > coin0, `골드 받음 (요일 ${w}) ${coin0} → ${coin1}`);
      await p.evaluate(() => { const o = document.querySelector('#ddout'); o && o.click(); }); await p.waitForTimeout(800);
      ok(!(await st(p)).xb, '우물 위로 나옴');
    }
    const s5 = await st(p); ok(s5.dd.fc && s5.dd.fc['0_0'] && s5.dd.fc['4_2'], '처음 보상 기록');
    // 지면: 깎은 만큼 골드 (횟수는 그대로)
    await p.evaluate(() => { __T.meRaw().dd.n = 0; __T.meRaw().dd.ln = 0; __T.pkSet('day/ctl', { open: false, at: 6, test: 2 }); }); await p.waitForTimeout(600);
    { await fight(p, 2, 0, false); const c0 = await p.evaluate(() => __T.meRaw().coin);
      await p.evaluate(() => { const B = __T.xbGet(); B.foes.forEach(f => { f.hp = Math.round(f.mhp / 2); }); B.party.forEach(u => { u.hp = 0; }); }); await p.waitForTimeout(6000);
      const c1 = await p.evaluate(() => __T.meRaw().coin), s7 = await st(p); ok(c1 - c0 === 400, `진 판 골드 (쉬움 800 의 절반) ${c1 - c0}`); ok(s7.dd.n === 0 && s7.dd.ln === 1, `진 판은 횟수 그대로 · 진 판 골드 1 번 ${s7.dd.n} ${s7.dd.ln}`); ok(!s7.xb, '지면 우물 위로'); }
    // 오늘 3 번 다 쓰면: 도울 수는 있고 카드는 없어요
    await p.evaluate(() => { __T.meRaw().dd.n = 3; __T.pkSet('day/ctl', { open: false, at: 5, test: 1 }); }); await p.waitForTimeout(600);
    { await fight(p, 1, 0, false); await p.evaluate(() => { const B = __T.xbGet(); B.foes.forEach(f => { f.hp = 0; }); }); await p.waitForTimeout(5000);
      ok((await p.$$('[data-ddc]')).length === 0, '다 쓰면 카드 없음'); ok((await st(p)).dd.n === 3, '횟수 그대로');
      await p.evaluate(() => { const o = document.querySelector('#ddout'); o && o.click(); }); await p.waitForTimeout(800); }
    // 주말: 판자
    await p.evaluate(() => __T.pkSet('day/ctl', { open: true, at: 4, test: null })); await p.waitForTimeout(600);
    ok(p.errs.length === 0, '오류 없음 ' + JSON.stringify(p.errs.slice(0, 3))); await p.close(); }
  console.log(`${pass} / ${pass + fail} 통과`); await b.close(); process.exit(fail ? 1 : 0);
})();
