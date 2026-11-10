// 새 별자리 12 개 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/stargaze/test_more.js
//   데이터 · 대사 파일 · 관리자 고르기 목록 · 별빛 효과(전투 능력치 · 2차 직업 경험치 · 쉬는 직업 몫 · 상한)
const { chromium } = require('playwright'); const fs = require('fs');
const spec = fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')'); seed.players.me1.ex = { job: 'knight', exp: 200000, xv: 3, sk: { '0_0': 1 }, cur: 1, jo: null };
  seed.players.me1.ex = { job: 'shaman', exp: 0, xv: 3, sk: { '0_0': 1 }, cur: 1, jo: { job: 'knight', exp: 200000, xv: 3, sk: { '0_0': 1 } } };
  const br = await chromium.launch(), p = await br.newPage(), errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(5000);
  const C = (f, a) => p.evaluate(f, a);
  const D = await C(async () => { const d = await (await fetch('data/events/stargazing/constellations.json')).json(); const out = []; for (const c of d.constellations){ let dl = null; try { dl = await (await fetch(`data/events/stargazing/dialogue/${c.id}.json`)).json(); } catch(e){} out.push({ id: c.id, n: c.stars.length, dl: !!dl && ['intro', 'assign', 'story', 'buff', 'done'].every(k => (dl[k] || []).length), st: c.buff.effects.map(e => e.stat) }); } return out; });
  ok(D.length === 24, '별자리 24 개 (' + D.length + ')'); ok(D.every(x => x.n === 12 && x.dl), '모두 별 12 개 · 대사 파일 있음 ' + D.filter(x => !(x.n === 12 && x.dl)).map(x => x.id));
  const stats = [...new Set(D.flatMap(x => x.st))]; ok(['x_main', 'x_hp', 'x_dr', 'x_crit', 'x_spd', 'x_healin', 'x_mpreg', 'j2_main', 'j2_exp', 'idle_exp', 'x_gold', 'x_loot'].every(k => stats.includes(k)), '새 효과 12 종 ' + stats.join(','));
  // 효과: 별빛을 켜고 전투 유닛 · 경험치 비교
  const unit = () => C(() => { const u = __T.xMk(__T.xEx_().job, 20, 'me', false); return { heal: u.heal, mhp: u.mhp, dr: u.dr, crit: u.crit, spd: u.spd, healIn: u.healIn || 0, mpReg: u.mpReg || 0 }; });
  await C(() => window.__T.sgSync && 0); const u0 = await unit();
  await C(() => { const t = Date.now() + 864e5, b = __T.meRaw().buffs = __T.meRaw().buffs || {}; ['buff_soul', 'buff_guard', 'buff_blade', 'buff_dance', 'buff_spirit', 'buff_paths'].forEach(k => { b[k] = t; }); });
  const u1 = await unit();
  ok(u1.heal > u0.heal * 1.15, `주 능력치(치유) 올라요 · 2차라서 혼 별빛도 (${u0.heal} → ${u1.heal})`);
  ok(u1.mhp > u0.mhp * 1.05 && u1.dr > u0.dr + .07 && u1.crit >= u0.crit + .06 && u1.spd > u0.spd && u1.healIn >= .1 && u1.mpReg >= .3, '체력 · 받는 피해 · 치명 · 속도 · 받는 회복 · MP 회복 ' + JSON.stringify([u0, u1]));
  const g = await C(() => { const ex = __T.xEx_(), e0 = ex.exp, j0 = ex.jo.exp; __T.xGain_(1000); return [ex.exp - e0, ex.jo.exp - j0]; });
  ok(g[0] === 4200 && g[1] === 300, `2차 경험치 +30 % · 혼 +10 % (× 3 배 구간) · 쉬는 직업 몫 30 % (${g})`);
  await C(() => { const t = Date.now() + 864e5, b = __T.meRaw().buffs; ['buff_dragon', 'buff_mirror', 'buff_aim', 'buff_bellflower'].forEach(k => { b[k] = t; }); });
  const u2 = await unit(); ok(u2.heal <= Math.round(u0.heal * 1.42) + 2 && u2.crit - u0.crit <= .151 && u2.dr - u0.dr <= .151, '여러 별빛이 겹쳐도 상한 (주 +20 % · 혼 +20 % · 치명 +15 % · 받는 피해 -15 %) ' + JSON.stringify(u2));
  // 관리자 고르기 목록
  const ad = await br.newPage(); await ad.addInitScript(s => { window.__seed = s; window.__uid = 'admin'; }, seed); await ad.goto('http://localhost:8822/'); await ad.waitForFunction(() => window.__T, null, { timeout: 30000 }); await ad.waitForTimeout(4000);
  const card = await ad.evaluate(() => { window.__T.showAdmin(); return new Promise(r => setTimeout(() => r(window.__T.sgCard()), 1500)); });
  ok(/두 갈래 길자리/.test(card) && /초롱꽃자리/.test(card) && /· 전투/.test(card), '관리자 별자리 고르기에 새 별자리 (태그 「전투」 등)');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await br.close(); process.exit(fail ? 1 : 0);
})();
