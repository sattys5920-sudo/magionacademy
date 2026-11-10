// 2차 직업(영웅의 혼) 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/newjobs/test/j2.js
//   새 직업 데이터 · 스킬 설명 · 이펙트 · 관리자 열기(한 명씩) · 탐사 문 연출 · 혼 고르기(추천/비추천 · 주인 있는 혼 · 겹침 막기)
//   · 저장(ex.jo · jobs/ · j2/got) · 1차/2차 바꾸기 · 막히는 때 · 경험치(100 % / 20 % / Lv 12 까지 3 배) · 트리 · 스탯 탭 · 전투 · 관리자 목록
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = __dirname + '/../shots'; fs.mkdirSync(OUT, { recursive: true });
const spec = fs.readFileSync(__dirname + '/../../../tests/ui.spec.js', 'utf8');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const NEW = ['paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
(async () => {
  const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
  const me = seed.players.me1; me.ex = { job: 'knight', exp: 200000, xv: 3, d: '', n: 0, sk: { '0_0': 1 } }; me.coin = 50000;
  seed.players.fr1 = { ...JSON.parse(JSON.stringify(me)), nick: '하늘', ex: { job: 'black', exp: 0, xv: 3 } }; seed.approved = { me1: true, fr1: true };
  seed.pub = { fr1: { nick: '하늘', look: me.look, ex: { job: 'black', wp: 0, j1: 'black', j2: 'archer' } } }; seed.jobs = { knight: 'me1', black: 'fr1', archer: 'fr1' };
  const br = await chromium.launch(); const ctx = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const errs = [];
  const page = async u => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept()); await p.addInitScript(([sd, u]) => { window.__seed = sd; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T && window.World && World.Avatar, null, { timeout: 30000 }); await p.waitForTimeout(4000); for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const A = await page('me1'), C = (f, a) => A.evaluate(f, a);
  const until = async (f, n = 60, ms = 300, a) => { for (let i = 0; i < n; i++){ if (await C(f, a)) return true; await A.waitForTimeout(ms); } return false; };
  // 1 데이터: 새 직업 12 · 스킬 15 개씩 · 설명 · 이펙트
  const D = await C(NEW => { const XJ = __T.XJ_, out = { n: 0, bad: [], fx: [], hp: [] }; NEW.forEach(j => { if (!XJ[j]) out.bad.push('XJ ' + j); __T.xAll_(j).forEach(o => { out.n++; for (let L = 1; L <= 5; L++){ const d = __T.xDesc_(o, L); if (!d || /undefined|NaN/.test(d)) out.bad.push(j + '.' + o.n + ' ' + d); } if (!o.pas && !XFXJOB.SK[j + '.' + o.n]) out.fx.push(j + '.' + o.n); }); const u = __T.xMk(j, 30, 'x', true); if (!(u.hp > 0 && u.sks.length)) out.hp.push(j); }); return out; }, NEW);
  ok(D.n === 180, `새 직업 스킬 180 개 (${D.n})`); ok(!D.bad.length, '스킬 설명에 빈 값 없음 ' + D.bad.slice(0, 3)); ok(!D.fx.length, '패시브 빼고 전부 이펙트 ' + D.fx.slice(0, 3)); ok(!D.hp.length, '전투 유닛 만들기 ' + D.hp);
  ok(await C(() => !document.querySelector('.jgrid') || ![...document.querySelectorAll('.jgrid [data-job]')].some(b => ['paladin', 'miko'].includes(b.dataset.job))), '1차 직업 고르기에는 새 직업이 없어요');
  // 2 열기 전: 탐사 문 → 그냥 탐사 창
  await C(() => World.onExplore(0)); await A.waitForTimeout(1500);
  ok(await C(() => !document.querySelector('.j2cut') && /가는 곳/.test(document.querySelector('.panel').innerText) && !document.querySelector('.x2w')), '열기 전에는 연출 없이 탐사 창 (1차만)');
  await C(() => __T.closeSheet()); await A.waitForTimeout(500);
  // 3 관리자: 한 명씩 열기
  const Ad = await page('admin'); await Ad.setViewportSize({ width: 1000, height: 1000 });
  await Ad.evaluate(() => __T.showAdmin()); await Ad.waitForTimeout(1500); await Ad.evaluate(() => window.__adPoll && window.__adPoll()); await Ad.click('[data-adtab="event"]'); await Ad.waitForTimeout(2000);
  const card = () => Ad.evaluate(() => { const c = [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('영웅의 혼')); if (!c) return ''; if (c.classList.contains('shut')) c.querySelector('.abhead b').click(); const d = [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('영웅의 혼')); return d ? d.innerText : ''; });
  ok(/2차 직업 · 영웅의 혼/.test(await card()), '관리자: 2차 직업 카드'); await Ad.waitForTimeout(500);
  ok(await Ad.evaluate(() => !!document.querySelector('[data-j2a="open:me1"]')), '관리자: 학생마다 열기 버튼');
  await Ad.click('[data-j2a="open:me1"]'); await Ad.waitForTimeout(1500);
  ok(await Ad.evaluate(() => !!(window.__tree && __tree.j2 && __tree.j2.open && __tree.j2.open.me1) || /고르는 중/.test([...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('영웅의 혼')).innerText)), '관리자가 열면 j2/open/me1 · 고르는 중');
  ok(await Ad.evaluate(() => { const b = document.querySelector('[data-j2a="open:fr1"]'); return !b || b.disabled; }), '고르는 중인 학생이 있으면 다른 학생은 못 열어요 (한 명씩)');
  // 4 학생: 탐사 문 → 연출 → 혼 고르기
  await A.waitForTimeout(1500); await C(() => World.onExplore(0));
  ok(await until(() => !!document.querySelector('.j2cut')), '열린 뒤 탐사 문을 지나면 영웅의 혼 연출');
  ok(await until(() => !!document.querySelector('.j2cut .sjpick.on'), 80), '혼 고르는 칸이 나와요'); await A.waitForTimeout(600);
  const P = await C(() => Object.fromEntries([...document.querySelectorAll('.j2cut .sjc')].map(b => [b.dataset.sj, b.innerText.replace(/\s+/g, ' ') + (b.classList.contains('off') ? ' OFF' : '')])));
  ok(Object.keys(P).length === 12, '혼 12 개');
  ok(/비추천/.test(P.paladin) && /비추천/.test(P.guardian) && /비추천/.test(P.darkknight), '1차 기사(탱커) → 탱커 셋은 비추천');
  ok(/추천/.test(P.miko) && !/비추천/.test(P.miko) && /추천/.test(P.dancer) && !/비추천/.test(P.dancer), '힐러 · 지원은 추천');
  ok(!/추천/.test(P.fighter) && !/추천/.test(P.elemental), '딜러는 뱃지 없음');
  ok(/OFF/.test(P.archer) && /주인: 하늘/.test(P.archer), '다른 친구가 받은 혼은 흐리게 · 주인 이름');
  await A.screenshot({ path: OUT + '/j2_pick.png' });
  await C(() => document.querySelector('.j2cut [data-sj="archer"]').click()); await A.waitForTimeout(300);
  ok(await C(() => !document.querySelector('.j2cut [data-ok]')), '주인 있는 혼은 못 골라요');
  await C(() => document.querySelector('.j2cut [data-sj="guardian"]').click()); await A.waitForTimeout(300);
  ok(/기사와 같은 탱커예요/.test(await C(() => document.querySelector('.j2cut .sjdet').innerText)), '비추천 이유: 1차 기사와 같은 탱커예요');
  // 겹침: 고르는 사이에 다른 친구가 무녀를 가져가요 → 받아들이기 실패 · 목록 다시
  await C(() => document.querySelector('.j2cut [data-sj="miko"]').click()); await A.waitForTimeout(200);
  await C(() => __T.pkSet('jobs/miko', 'fr9')); await A.waitForTimeout(300);
  await C(() => document.querySelector('.j2cut [data-ok]').click()); await A.waitForTimeout(1500);
  ok(await C(() => document.querySelector('.j2cut [data-sj="miko"]').classList.contains('off') && !(__T.xEx_().jo)), '동시에 고른 혼은 겹치지 않아요 (먼저 가져간 친구 것)');
  await C(() => document.querySelector('.j2cut [data-sj="shaman"]').click()); await A.waitForTimeout(300);
  await A.screenshot({ path: OUT + '/j2_detail.png' });
  await C(() => document.querySelector('.j2cut [data-ok]').click()); await A.waitForTimeout(1200);
  const E1 = await C(() => JSON.parse(JSON.stringify(__T.xEx_())));
  ok(E1.jo && E1.jo.job === 'shaman' && E1.job === 'knight' && !E1.cur, '받아들이면 바로 저장 (ex.jo = 주술사 · 지금은 1차)');
  ok(await C(() => window.__tree && __tree.jobs && __tree.jobs.shaman === 'me1' && __tree.j2 && __tree.j2.got && __tree.j2.got.me1 === 'shaman'), 'jobs/shaman · j2/got 기록');
  await A.waitForTimeout(5000); await A.screenshot({ path: OUT + '/j2_enter.png' });
  ok(await until(() => !document.querySelector('.j2cut') && !!document.querySelector('.x2w'), 60), '연출이 끝나면 탐사 창 (1차 / 2차 두 칸)');
  await A.screenshot({ path: OUT + '/j2_lobby1.png' });
  const L = await C(() => document.querySelector('.x2w').innerText.replace(/\s+/g, ' '));
  ok(/1차 기사/.test(L) && /2차 주술사/.test(L) && /이번에 가요/.test(L) && /쉬는 중 · 경험치 20 %/.test(L) && /경험치 3 배/.test(L), '두 칸: 1차 기사 이번에 가요 · 2차 주술사 쉬는 중 · 3 배 표시 ' + L);
  // 5 바꾸기
  await C(() => document.querySelector('[data-x2="1"]').click()); await A.waitForTimeout(800);
  const E2 = await C(() => JSON.parse(JSON.stringify(__T.xEx_())));
  ok(E2.job === 'shaman' && E2.cur === 1 && E2.jo.job === 'knight' && E2.jo.exp === 200000 && (E2.exp || 0) === 0, '2차로 바꾸면 주술사가 위로 · 기사는 쉬는 칸 (경험치 그대로)');
  ok(/주술사 무기 강화/.test(await C(() => document.querySelector('#xwp').innerText)), '아래 버튼도 고른 직업 이름');
  await A.screenshot({ path: OUT + '/j2_lobby2.png' });
  // 6 경험치: 2차 Lv 12 미만 3 배 · 쉬는 직업 20 %
  await C(() => __T.xGain_(1000)); let E = await C(() => JSON.parse(JSON.stringify(__T.xEx_())));
  ok(E.exp === 3000 && E.jo.exp === 200200, `2차로 가면 3 배 · 쉬는 1차 20 % (${E.exp} · ${E.jo.exp})`);
  await C(() => { const ex = __T.xEx_(); let t = 0; for (let l = 1; l < 12; l++) t += [0, 1500, 2000, 2600, 3300, 4200][l] || Math.round((5250 + 13.5 * l ** 2.3) / 10) * 10; ex.exp = t; });
  ok(await C(() => __T.xLv_(__T.xEx_().exp).L === 12), '2차 Lv 12'); const e0 = await C(() => __T.xEx_().exp);
  await C(() => __T.xGain_(1000)); ok(await C(e0 => __T.xEx_().exp === e0 + 1000, e0), 'Lv 12 부터는 원래대로 (1 배)');
  await C(() => document.querySelector('[data-x2="0"]').click()); await A.waitForTimeout(600); const j0 = await C(() => __T.xEx_().jo.exp);
  await C(() => __T.xGain_(1000)); E = await C(() => JSON.parse(JSON.stringify(__T.xEx_())));
  ok(E.job === 'knight' && E.exp === 201400 && E.jo.exp === j0 + 200, '1차로 가면 1차 100 % · 쉬는 2차 20 % (3 배 없음) ' + JSON.stringify([E.job, E.exp, E.jo.exp, j0]));
  // 7 트리 · 스탯 탭
  await C(() => document.querySelector('#xtree').click()); await A.waitForTimeout(800);
  ok(await C(() => !!document.querySelector('.x2tab') && /기사/.test(document.querySelector('.panel').innerText)), '스킬 트리 위 1차 / 2차 탭');
  await C(() => document.querySelector('.x2tab [data-x2="1"]').click()); await A.waitForTimeout(800);
  ok(await C(() => /주술사/.test(document.querySelector('.panel').innerText) && /치유 토템/.test(document.querySelector('.panel').innerText) && __T.xEx_().cur === 1), '탭을 누르면 주술사 트리 (치유 토템)');
  await A.screenshot({ path: OUT + '/j2_tree.png' });
  // 8 막히는 때: 탐사 중
  await C(() => { __T.xEx_().run = { rg: 0, loot: { gold: 0, exp: 0, items: {} }, start: Date.now(), end: Date.now() + 6e5, prog: 0 }; });
  ok(!(await C(() => __T.xSwap_(0))) && (await C(() => __T.xEx_().cur)) === 1, '탐사 중에는 못 바꿔요');
  await C(() => { __T.xEx_().run = null; });
  // 8.5 파티 로비: 바꾸면 방 기록도 바뀌고, 준비를 누르면 잠겨요
  await C(() => __T.closeSheet()); await A.waitForTimeout(400); await C(() => World.onExplore(0)); await A.waitForTimeout(900);
  await C(() => [...document.querySelectorAll('.panel button')].find(b => /파티 모집하기/.test(b.textContent)).click()); await A.waitForTimeout(1500);
  const room = () => C(() => { const x = window.__tree.xparty || {}; const k = Object.keys(x).find(k => x[k].p && x[k].p.me1); return k ? x[k].p.me1 : null; });
  ok(((await room()) || {}).job === 'shaman', '파티 방에 지금 직업(주술사) ' + JSON.stringify(await room()));
  await C(() => document.querySelector('[data-x2="0"]') && document.querySelector('[data-x2="0"]').click()); await A.waitForTimeout(1200);
  ok(((await room()) || {}).job === 'knight', '파티 로비에서 1차로 바꾸면 방 기록도 기사 ' + JSON.stringify(await room()));
  const rk = await C(() => { const x = window.__tree.xparty; return Object.keys(x).find(k => x[k].p && x[k].p.me1); });
  await C(k => __T.pkSet('xparty/' + k + '/p/me1/rdy', 1), rk); await A.waitForTimeout(800);
  ok(!(await C(() => __T.xSwap_(1))) && (await C(() => __T.xEx_().cur)) === 0, '준비를 누르면 못 바꿔요');
  await C(k => __T.pkSet('xparty/' + k + '/p/me1/rdy', 0), rk); await A.waitForTimeout(800);
  ok(await C(() => __T.xSwap_(1)) && (await C(() => __T.xEx_().cur)) === 1, '준비를 풀면 다시 바꿀 수 있어요');
  await C(k => __T.pkSet('xparty/' + k, null), rk); await A.waitForTimeout(600); await C(() => __T.closeSheet());
  // 9 전투: 주술사로 싸워요 (무기 · 스킬 이펙트 오류 없이)
  await C(() => __T.closeSheet()); await A.waitForTimeout(400);
  const bt = await C(async () => { const ex = __T.xEx_(); ex.sk = { '0_0': 3, '0_1': 2, '2_0': 2, '2_1': 1 }; World.onExplore(0); await new Promise(r => setTimeout(r, 800)); [...document.querySelectorAll('.panel button')].find(b => /혼자 가기|출발하기/.test(b.textContent)).click(); await new Promise(r => setTimeout(r, 1500)); __T.xSB('battle'); await new Promise(r => setTimeout(r, 4000)); const B = __T.xbGet(); return B ? { me: B.party[0] && B.party[0].job, sks: B.party[0] && B.party[0].sks.map(o => o.n) } : null; });
  ok(bt && bt.me === 'shaman' && bt.sks.includes('치유 토템'), '전투에 주술사로 나가요 ' + JSON.stringify(bt));
  await A.waitForTimeout(3000); await A.screenshot({ path: OUT + '/j2_battle.png' });
  // 10 관리자 목록
  await Ad.waitForTimeout(1000); await Ad.evaluate(() => window.__adPoll && window.__adPoll()); await Ad.waitForTimeout(1500); await Ad.evaluate(() => [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent).click()); await Ad.waitForTimeout(1200);
  const c2 = await card(); await Ad.waitForTimeout(300); ok(/주술사/.test(c2) && /받은 학생 1/.test(c2), '관리자 카드: 받은 직업 · 받은 학생 수');
  ok(await Ad.evaluate(() => { const b = document.querySelector('[data-j2a="open:fr1"]'); return !!b && !b.disabled; }), '고르고 나면 다음 학생을 열 수 있어요');
  await Ad.evaluate(() => { const b = [...document.querySelectorAll('[data-adtab="students"]')].find(b => b.offsetParent); b && b.click(); }); await Ad.waitForTimeout(1500);
  const pl = await Ad.evaluate(() => document.querySelector('#adminv') ? document.querySelector('#adminv').innerText : '');
  ok(/기사 · 주술사/.test(pl) || /주술사/.test(pl), '관리자 플레이어 목록에 2차 직업');
  await Ad.screenshot({ path: OUT + '/j2_admin.png', fullPage: false });
  // 11 다시 열려도 연출은 한 번만 (이미 2차가 있어요)
  await C(() => __T.closeSheet()); await C(() => { if (__T.xbGet()) {} }); ok(!(await C(() => __T.J2_().can())), '2차가 있으면 다시 연출 없음');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3).join(' | '));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await br.close(); process.exit(fail ? 1 : 0);
})();
