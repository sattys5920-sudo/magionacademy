// 「용의 알 지키기」 실제 화면 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/df_qa_test.js
//   관리자 열기 → 학생 3 명 (기사 · 백마법사 · 흑마법사) 버튼 · 자리 고르기 · 스킬 자동 켬 · 시작 → 웨이브 → 쉬는 시간이 끝나면 저절로 다음 웨이브
//   → 빨리 감아 끝까지 → 결과 기록 → 용의 동굴 문 · 용의 가호
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const base = seed.players.me1, JOBS = { me1: 'knight', me2: 'white', me3: 'black' };
['me2', 'me3'].forEach((u, i) => { seed.players[u] = JSON.parse(JSON.stringify(base)); seed.players[u].nick = ['서연', '지호'][i]; });
Object.entries(JOBS).forEach(([u, j]) => { seed.players[u].ex = { job: j, exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 } }; });
(async () => {
  const b = await chromium.launch(), errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'] });
  const page = async (u, opt) => { const p = await ctx.newPage(); if (opt && opt.viewport) await p.setViewportSize(opt.viewport); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const ad = await page('admin', { viewport: { width: 1000, height: 900 } });
  await ad.evaluate(() => __T.showAdmin()); await ad.waitForTimeout(1200); await ad.evaluate(() => window.__adPoll && window.__adPoll()); await ad.waitForTimeout(500);
  await ad.evaluate(() => { const t = [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent) || document.querySelector('[data-adtab="event"]'); if (t) t.click(); }); await ad.waitForTimeout(1000);
  await ad.evaluate(() => { const c = [...document.querySelectorAll('#adminv .adcard')].find(c => /용의 알 지키기/.test(c.textContent)); if (c && c.classList.contains('shut')) c.querySelector('.abhead b, b').click(); }); await ad.waitForTimeout(400);
  await ad.evaluate(() => document.querySelector('#adminv [data-dfa="open"]').click()); await ad.waitForTimeout(1500);
  const H = () => ad.evaluate(() => { const h = __T.dfGet().host; if (!h) return null; const S = h.S; return { ph: S.phase, w: S.wave, eggs: S.eggs.map(Math.round), pl: Object.values(S.players).map(p => [p.uid, p.zone, p.slot, p.job, p.cat, p.auto, p.ready]), rest: S.rest }; });
  ok(!!(await H()), '관리자: 「이벤트 열기」 → 이 화면이 진행을 맡아요 ' + JSON.stringify(await H()));
  const st = {}; for (const u of ['me1', 'me2', 'me3']){ st[u] = await page(u); }
  for (const [i, u] of ['me1', 'me2', 'me3'].entries()){
    const p = st[u]; await p.waitForFunction(() => document.getElementById('dfbtn'), null, { timeout: 15000 }).catch(() => {});
    ok(await p.evaluate(() => !!document.getElementById('dfbtn')), `${u}: 오른쪽 위 「용의 알 지키기」 버튼`);
    await p.evaluate(() => document.getElementById('dfbtn').click()); await p.waitForTimeout(800);
    await p.evaluate(i => __tw.ev(`dfSeat(${i}, 0)`), i); await p.waitForTimeout(1200);
  }
  await ad.waitForTimeout(1500);
  const h1 = await H();
  ok(h1 && h1.pl.length === 3 && h1.pl.every(q => q[5] === 1), '자리 3 명 · 모두 스킬 자동 켬으로 시작 ' + JSON.stringify(h1 && h1.pl));
  ok(h1 && h1.pl.map(q => q[4]).join() === 'melee,heal,ranged', '직업 → 역할 (기사 근접 · 백마법사 치유 · 흑마법사 원거리) ' + (h1 && h1.pl.map(q => q[4])));
  await st.me2.screenshot({ path: __dirname + '/shot_df_seat.png' });
  // 시작
  for (const u of ['me1', 'me2', 'me3']) { await st[u].waitForFunction(() => document.getElementById('dfready'), null, { timeout: 10000 }).catch(() => {}); await st[u].evaluate(() => { const r = document.getElementById('dfready'); if (r) r.click(); }); await st[u].waitForTimeout(400); }
  await ad.waitForTimeout(2500);
  ok((await H()).ph === 'wave' && (await H()).w === 1, '모두 「시작」 → 웨이브 1 ' + JSON.stringify(await H()));
  await ad.waitForTimeout(6000);
  const k1 = await ad.evaluate(() => __T.dfGet().host.S.kz.reduce((a, x) => a + x, 0));
  ok(k1 > 0, '웨이브 중 몬스터를 잡아요 (자동 스킬 · 기본 공격) ' + k1);
  await ad.evaluate(() => { const S = __T.dfGet().host.S; Object.values(S.players).forEach(p => { p.gold += 2000; }); }); await ad.waitForTimeout(4500);
  const ups = await ad.evaluate(() => Object.values(__T.dfGet().host.S.players).map(p => p.up.reduce((a, u) => a + u.pow + u.rng + u.cd, 0)));
  ok(ups.every(n => n > 0), '「자동」이면 번 골드로 올리기도 알아서 ' + ups);
  await st.me1.screenshot({ path: __dirname + '/shot_df_wave.png' });
  // 웨이브 1 을 빨리 끝내고 쉬는 시간 → 아무도 안 눌러도 30 초 뒤 웨이브 2
  await ad.evaluate(() => { const S = __T.dfGet().host.S; for (let i = 0; i < 3000 && S.phase === 'wave'; i++) TD.step(S, .1); });
  await ad.waitForTimeout(1500);
  const r1 = await H(); ok(r1.ph === 'rest' && r1.w === 1, '웨이브 1 끝 → 쉬는 시간 ' + JSON.stringify(r1));
  const restTxt = await st.me1.evaluate(() => (document.getElementById('dftx') || {}).textContent || '');
  ok(/초 뒤 다음 웨이브/.test(restTxt), '학생 화면: 「n 초 뒤 다음 웨이브」 ' + restTxt);
  await ad.evaluate(() => { __T.dfGet().host.S.rest = 1; }); await ad.waitForTimeout(2500);
  ok((await H()).w === 2 && (await H()).ph === 'wave', '쉬는 시간이 끝나면 저절로 웨이브 2 ' + JSON.stringify(await H()));
  // 끝까지 빨리 감기 (쉬는 시간 건너뛰기)
  await ad.evaluate(() => { const S = __T.dfGet().host.S; for (let i = 0; i < 200000 && S.phase !== 'over'; i++){ if (S.phase === 'rest') S.rest = 0; TD.step(S, .1); } });
  await ad.waitForTimeout(3000);
  const end = await H(); ok(end.ph === 'over', '15 웨이브 끝 ' + JSON.stringify(end));
  const res = await st.me1.evaluate(() => __tw.ev('JSON.stringify(dfRes)'));
  ok(!!JSON.parse(res) && JSON.parse(res).eggs.length === 3, '결과 기록 defense/res ' + res);
  const alive = JSON.parse(res).eggs.some(e => e > 0);
  ok((await st.me1.evaluate(() => __tw.ev("World.canEnter('dragon')"))) === (alive ? true : '굳게 닫힌 바위 문이에요. 안에서 무언가 잠들어 있는 것 같아요.......'), `용의 동굴 문: 알이 ${alive ? '남아 열려요' : '없어 닫혀 있어요'}`);
  await st.me1.screenshot({ path: __dirname + '/shot_df_end.png' });
  // 알이 남은 경우의 용의 가호 (결과를 하나 남긴 걸로 두고)
  await st.me1.evaluate(() => __tw.ev("(dfRes = { id: 1, eggs: [60, 0, 30], win: 1, at: now2() }, 1)"));
  ok((await st.me1.evaluate(() => __tw.ev("World.canEnter('dragon')"))) === true, '알이 남으면 용의 동굴 문이 열려요');
  ok(await st.me1.evaluate(() => __tw.ev("World.reqOk('alive:0') && !World.reqOk('alive:1') && World.reqOk('dead:1')")), '지킨 알의 용만 있고 깨진 알 자리는 껍데기');
  await st.me1.evaluate(() => __tw.ev('(setTimeout(() => dfDragonOffer(0), 0), 1)')); await st.me1.waitForTimeout(500); await st.me1.evaluate(() => { const o = document.getElementById('cfOk'); if (o) o.click(); }); await st.me1.waitForTimeout(500);
  ok(await st.me1.evaluate(() => __tw.ev('(me.buffs.dfire || 0) > now2() && me.dfb.n === 1')), '화륵이 가호 2 시간 (오늘 1 / 2 번)');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
