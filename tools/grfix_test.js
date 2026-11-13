// 승급 시험 점수 고치기 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/grfix_test.js
//   관리자 「점수 고치기」 → 학생 기기에 알림 없이 성적표 점수만 바뀌어요 · 결과 공개 뒤에 고치면 합격 · 망토 · 골드도 맞춰져요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const CID = 1700000000000;
seed.promo = { ctl: { open: true, id: CID, at: Date.now() } };
seed.players.me1.gr = { y: 1, g: {}, used: { [CID]: 1 }, hist: [], hi: {}, d: {}, seen: CID, pend: { cid: CID, y: 2, t: [60, 65, 70, 55, 60, 50], tot: 60, g: '', at: 5 } };
(async () => {
  const b = await chromium.launch(), errs = [], toasts = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'] });
  const page = async (u, opt) => { const p = await ctx.newPage(); if (opt && opt.viewport) await p.setViewportSize(opt.viewport); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept());
    await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const ad = await page('admin', { viewport: { width: 1000, height: 900 } });
  const p = await page('me1'); const S = () => p.evaluate(() => __tw.ev('JSON.parse(JSON.stringify(me.gr))'));
  await p.exposeFunction('__toastSeen', t => toasts.push(t)); await p.evaluate(() => new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => { if (n.classList && n.classList.contains('toast')) __toastSeen(n.textContent); }))).observe(document.getElementById('stage'), { childList: true }));
  const openGr = async () => { await ad.evaluate(() => __T.showAdmin()); await ad.waitForTimeout(1200); await ad.evaluate(() => window.__adPoll && window.__adPoll()); await ad.waitForTimeout(600);
    await ad.evaluate(() => { const t = [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent); if (t) t.click(); }); await ad.waitForTimeout(1200); };
  const row = () => ad.evaluate(() => { const r = [...document.querySelectorAll('#adminv .grr')].find(d => /민준/.test(d.textContent)); return r ? r.innerText.replace(/\n/g, ' ') : ''; });
  await openGr();
  ok(/점수 고치기/.test(await row()), '관리자: 응시한 학생 줄에 「점수 고치기」 ' + (await row()).slice(0, 120));
  // 1 결과 공개 전: 70 점으로 고치기
  await ad.evaluate(() => [...document.querySelectorAll('#adminv [data-grfx]')].find(b => b.dataset.grfx === 'me1').click()); await ad.waitForTimeout(300);
  const n = await ad.evaluate(() => document.querySelectorAll('#adminv [data-grfxi]').length);
  ok(n === 6, '과목 6 개 점수 칸');
  await ad.evaluate(() => { const v = [80, 75, 70, 70, 70, 60]; [...document.querySelectorAll('#adminv [data-grfxi]')].forEach((x, i) => { x.value = v[i]; x.dispatchEvent(new Event('input', { bubbles: true })); }); });
  
  await ad.evaluate(() => document.querySelector('#adminv [data-grfxs]').click()); await ad.waitForTimeout(1500);
  await p.waitForFunction(() => __tw.ev('me.gr.pend.tot') === 71, null, { timeout: 15000 }).catch(() => {});
  const s1 = await S();
  ok(s1.pend.tot === 71 && s1.pend.g === 'C' && JSON.stringify(s1.pend.t) === '[80,75,70,70,70,60]' && !s1.pend.shown && s1.y === 1, '학생 기기: 성적표 점수만 바뀌어요 (총점 71 · C) ' + JSON.stringify(s1.pend));
  ok(!toasts.some(t => /점수|시험|성적/.test(t)), '학생에게 알림 없음 ' + toasts.join(' / '));
  await openGr(); ok(/총점\s*71/.test(await row()) && /점수 고침/.test(await row()), '관리자 줄: 고친 점수 · 「점수 고침」 ' + (await row()).slice(0, 160));
  // 2 결과 공개 → 편지로 합격 C
  await ad.evaluate(() => __tw.ev("GDB.upd('promo/ctl', { pub: now2() })")).catch(() => {});
  await p.waitForFunction(() => document.getElementById('grenv'), null, { timeout: 20000 }).catch(() => {});
  await p.evaluate(() => { const e = document.getElementById('grenv'); if (e) e.click(); }); await p.waitForTimeout(1500);
  await p.evaluate(() => { const x = document.getElementById('grx'); if (x) x.remove(); });
  const coin0 = await p.evaluate(() => __tw.ev('me.coin')), s2 = await S();
  ok(s2.y === 2 && s2.g[2] === 'C', '공개 뒤 2 학년 C ' + JSON.stringify({ y: s2.y, g: s2.g }));
  // 3 공개 뒤 B 로 올리기 → 등급 · 망토 · 골드 차이
  await openGr();
  await ad.evaluate(() => [...document.querySelectorAll('#adminv [data-grfx]')].find(b => b.dataset.grfx === 'me1').click()); await ad.waitForTimeout(300);
  await ad.evaluate(() => { const v = [90, 85, 80, 80, 80, 75]; [...document.querySelectorAll('#adminv [data-grfxi]')].forEach((x, i) => { x.value = v[i]; x.dispatchEvent(new Event('input', { bubbles: true })); }); document.querySelector('#adminv [data-grfxs]').click(); }); await ad.waitForTimeout(1500);
  await p.waitForFunction(() => __tw.ev('me.gr.pend.g') === 'B', null, { timeout: 15000 }).catch(() => {});
  const s3 = await S(), coin1 = await p.evaluate(() => __tw.ev('me.coin')), cl = await p.evaluate(() => __tw.ev('Object.keys(me.closet || {}).filter(k => /cape_g/.test(k))'));
  ok(s3.g[2] === 'B' && coin1 - coin0 === 400 && cl.includes('cape:cape_g2B') && !cl.includes('cape:cape_g2C'), `공개 뒤 B 로: 등급 B · 골드 +${coin1 - coin0} · 망토 ${cl}`);
  // 4 공개 뒤 불합격으로 내리기
  await openGr();
  await ad.evaluate(() => [...document.querySelectorAll('#adminv [data-grfx]')].find(b => b.dataset.grfx === 'me1').click()); await ad.waitForTimeout(300);
  await ad.evaluate(() => { [...document.querySelectorAll('#adminv [data-grfxi]')].forEach(x => { x.value = 50; x.dispatchEvent(new Event('input', { bubbles: true })); }); document.querySelector('#adminv [data-grfxs]').click(); }); await ad.waitForTimeout(1500);
  await p.waitForFunction(() => __tw.ev('me.gr.y') === 1, null, { timeout: 15000 }).catch(() => {});
  const s4 = await S(), cl2 = await p.evaluate(() => __tw.ev('Object.keys(me.closet || {}).filter(k => /cape_g/.test(k))'));
  ok(s4.y === 1 && !s4.g[2] && !cl2.length && s4.pend.pass === 0, '공개 뒤 불합격으로: 1 학년 · 망토 빠짐 ' + JSON.stringify({ y: s4.y, g: s4.g, cl2 }));
  ok(!toasts.some(t => /점수|시험|성적/.test(t)), '끝까지 학생에게 점수 알림 없음');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
