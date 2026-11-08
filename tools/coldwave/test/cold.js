// 양호실 겨울 감기 전체 흐름 (휴대폰 화면 + 터치): 닫힘 → 관리자 시작 → 세라 시작 연출 → 진료 수첩 → 아픈 NPC (말풍선 · 대사 · 진료하기)
//   → 틀린 증상 · 틀린 물약 (물약 없어짐) · 맞는 물약 (나음 · 하트 · 이름표) → 솥에서 감기 물약 끓이기 → 이튿날 쪽지 → 차 장면 → 15 명 → 끝 장면 (세라 네 가지) → 보상 → 관리자 카드 → 닫기
// 사용: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/coldwave/test/cold.js
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs');
const OUT = '/home/user/magionacademy/tools/coldwave/shots'; fs.mkdirSync(OUT, { recursive: true });
const spec = fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8');
const res = []; const ok = (c, m) => { res.push([!!c, m]); console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
  const me = seed.players.me1; me.babySeen = 'x'; me.mana = 500;
  me.inv = { ...me.inv, honey: 2, g2_rasp: 1, g2_bell: 1, cp_fever: 3, cp_throat: 3, cp_nose: 3, cp_chill: 3 };
  me.npc = { ...me.npc, sera: { a: 120 } };
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const ctx = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const errs = [];
  const page = async u => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept()); await p.addInitScript(([sd, u]) => { window.__seed = sd; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000); for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const A = await page('me1');
  const C = (f, ...a) => A.evaluate(f, ...a);
  // 1 닫힘
  ok(!(await C(() => window.__cold.open())) && !Object.keys(await C(() => window.__cold.state().sick)).length, '닫혀 있으면 아픈 NPC가 없어요');
  ok(await C(() => !window.__cold.line('leo')), '닫혀 있으면 대사가 그대로예요');
  ok(await C(() => window.__cold.recipe(['honey', 'honey', 'g2_rasp', 'g2_bell']) === null), '닫혀 있으면 감기 물약이 안 끓어요');
  // 2 관리자 시작
  const Ad = await page('admin'); await Ad.setViewportSize({ width: 1000, height: 1000 });
  await Ad.evaluate(() => __T.showAdmin()); await Ad.waitForTimeout(1500); await Ad.click('[data-adtab="event"]'); await Ad.waitForTimeout(2000);
  const card = async () => (await Ad.evaluateHandle(() => [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('양호실 겨울 감기') && c.querySelector('[data-colda]')))).asElement();
  let c = await card(); await c.scrollIntoViewIfNeeded(); if ((await Ad.evaluate(e => e.innerText.length, c)) < 80){ await Ad.evaluate(e => e.querySelector('.abhead b').click(), c); await Ad.waitForTimeout(600); }
  await Ad.click('[data-colda="go"]'); await Ad.waitForTimeout(800);
  const ctl = await Ad.evaluate(() => window.__tree.cold && window.__tree.cold.ctl);
  ok(ctl && ctl.open === true && ctl.id && ctl.n === 3, '관리자가 시작하면 cold/ctl { open, id, n: 3 }');
  // 3 시작 연출
  for (let i = 0; i < 40; i++){ if (await C(() => !!(World.cutBusy && World.cutBusy()))) break; await A.waitForTimeout(300); }
  ok(await C(() => !!(World.cutBusy && World.cutBusy())), '세라 시작 연출이 나와요');
  await A.waitForTimeout(5200); await A.screenshot({ path: OUT + '/intro.png' });
  for (let i = 0; i < 80; i++){ if (await C(() => !!document.getElementById('coldv'))) break; await A.waitForTimeout(400); }
  await A.waitForTimeout(900); await A.screenshot({ path: OUT + '/chart.png' });
  const st = await C(() => window.__cold.state().cold);
  ok(st && st.hi === 1 && st.d0 > 0 && st.pd.split(',').length === 3 && st.cs === '000', '연출 뒤 진료 수첩 · 오늘 환자 3 명 ' + (st && st.pd));
  ok(!/sera/.test(st.pd), '세라 선생님은 환자가 아니에요');
  await C(() => document.querySelector('#coldv').scrollTo({ top: 999 })); await A.waitForTimeout(300); await A.screenshot({ path: OUT + '/chart_bottom.png' });
  await A.tap('[data-cdx="close"]'); await A.waitForTimeout(500);
  // 5 일 계획: 13 명이 모두 한 번씩 (새 친구는 만난 학생만)
  const plan = await C(() => window.__cold.planAll());
  const ids = new Set(plan.map(x => x.id)), avail = await C(() => window.__cold.PIDS.filter(id => __T.npcGet(id)));
  ok(plan.length === 15 && avail.every(id => ids.has(id)), `5 일 15 명 · 만날 수 있는 ${avail.length} 명이 모두 나와요 (${[...ids].join(',')})`);
  ok(await C(() => window.__cold.slots().length === 3), '미리 보기는 오늘 환자를 바꾸지 않아요');
  // 4 아픈 NPC: 말풍선 · 대사
  const pat = st.pd.split(',')[0].split('.'), pid = pat[0], sym = ({ f: 'fever', t: 'throat', n: 'nose', c: 'chill' })[pat[1]];
  ok(await C(id => !!window.__cold.sick(id) && !!window.__cold.line(id), pid), `${pid} 아파요 (${sym}) · 대사 「${await C(id => window.__cold.line(id), pid)}」`);
  await C(id => { const n = window.__cold.spot(id); World.teleport(n.map, [n.x + 2, n.y + 1]); }, pid); await A.waitForTimeout(3500);
  await A.screenshot({ path: OUT + '/sick_npc.png' });
  await A.screenshot({ path: OUT + '/sick_zoom.png', clip: { x: 55, y: 230, width: 280, height: 280 } });
  await C(id => __T.npcMenu(__T.npcGet(id)), pid); await A.waitForTimeout(600);
  ok(await C(() => !!document.querySelector('#npcui [data-nx="cold"]')), 'NPC 메뉴에 「진료하기」');
  await A.screenshot({ path: OUT + '/npc_menu.png' });
  // 틀린 증상
  await A.tap('#npcui [data-nx="cold"]'); await A.waitForTimeout(800); await A.screenshot({ path: OUT + '/diagnose.png' });
  const wrongSym = ['fever', 'throat', 'nose', 'chill'].find(k => k !== sym);
  await A.tap(`[data-cds="${wrongSym}"]`); await A.waitForTimeout(800);
  ok(await C(id => !!window.__cold.sick(id) && !document.getElementById('coldv'), pid), '틀린 증상: 낫지 않아요');
  // 맞는 증상 → 틀린 물약
  await C(id => window.__cold.treat(id), pid); await A.waitForTimeout(500); await A.tap(`[data-cds="${sym}"]`); await A.waitForTimeout(500);
  await A.screenshot({ path: OUT + '/potion_pick.png' });
  const wp = 'cp_' + wrongSym, before = await C(k => __T.me().inv[k], wp);
  await A.tap(`[data-cdp="${wrongSym}"]`); await A.waitForTimeout(900);
  ok(await C(([id, k, b]) => !!window.__cold.sick(id) && __T.me().inv[k] === b - 1, [pid, wp, before]), '틀린 물약: 낫지 않고 물약은 없어져요');
  await A.screenshot({ path: OUT + '/wrong.png' });
  // 맞는 물약
  const h0 = await C(id => __T.me().npc[id] ? __T.me().npc[id].a || 0 : 0, pid);
  await C(id => window.__cold.treat(id), pid); await A.waitForTimeout(500); await A.tap(`[data-cds="${sym}"]`); await A.waitForTimeout(400); await A.tap(`[data-cdp="${sym}"]`); await A.waitForTimeout(1200);
  await A.screenshot({ path: OUT + '/cured.png' });
  const s2 = await C(() => window.__cold.state().cold);
  ok(!(await C(id => window.__cold.sick(id), pid)) && s2.cs[0] === '1' && s2.cured[pid] === 1, '맞는 물약: 나았어요');
  ok((await C(id => __T.me().npc[id].a, pid)) >= h0 + 20, '하트 +20');
  ok(await C(() => __T.me().cos.tag.nurse === 1), '처음 고치기 → 이름표 「꼬마 간호사」');
  await A.waitForTimeout(3500); await A.screenshot({ path: OUT + '/reward_tag.png' });
  await A.waitForTimeout(2000);
  // 솥에서 감기 물약
  await C(() => __T.openSheet('lab')); await A.waitForTimeout(700); await A.tap('#recipePick'); await A.waitForTimeout(400);
  ok(await C(() => !!document.querySelector('[data-recipe="cp_throat"]')), '레시피 목록에 감기 물약');
  await A.screenshot({ path: OUT + '/lab_recipes.png' });
  await A.tap('[data-recipe="cp_throat"]'); await A.waitForTimeout(400); const ct = await C(() => __T.me().inv.cp_throat || 0);
  await A.tap('#brew'); await A.waitForTimeout(700);
  ok(await C(n => (__T.me().inv.cp_throat || 0) === n + 1 && !__T.me().found.includes('cp_throat') && (__T.me().inv.honey || 0) === 0, ct), '꿀 목 물약 = 벌꿀 × 2 · 산딸기 · 은방울꽃 (도감에는 안 들어가요)');
  ok(await C(() => window.__cold.recipe(['g2_bell', 'honey', 'g2_rasp']) === null), '벌꿀 하나면 체리 물약 (감기 물약 아님)');
  await A.screenshot({ path: OUT + '/lab_brew.png' }); await C(() => __T.closeSheet()); await A.waitForTimeout(400);
  // 이튿날 쪽지
  await C(() => { __T.me().cold.d0 -= 1; }); for (let i = 0; i < 20; i++){ if (await C(() => !!document.querySelector('.sdcardv'))) break; await A.waitForTimeout(400); }
  await A.waitForTimeout(700); await A.screenshot({ path: OUT + '/note_day2.png' });
  const s3 = await C(() => window.__cold.state().cold);
  ok(s3.nd === 1 && s3.pd.split(';').length === 2 && s3.cs.length === 6, '이튿날: 새 환자 3 명 · 쪽지 · 어제 못 고친 환자도 아파요 ' + s3.pd);
  ok(await C(() => Object.keys(window.__cold.state().sick).length >= 4), '못 고친 환자는 계속 아파요');
  await A.waitForTimeout(4500);
  // 차 장면 (세라 자리 · 양호실)
  await C(() => { const n = window.__cold.spot('sera'); World.teleport(n.map, [n.x + 2, n.y]); }); await A.waitForTimeout(3000);
  await C(() => window.__cold.tea()); await A.waitForTimeout(4200); await A.screenshot({ path: OUT + '/tea.png' });
  for (let i = 0; i < 40; i++){ if (await C(() => !window.__cold.state().coldOn)) break; await A.waitForTimeout(400); }
  ok(await C(() => window.__cold.state().cold.tea === 1), '차 장면');
  // 15 명 → 끝 장면
  await C(() => window.__cold.cureAll());
  for (let i = 0; i < 40; i++){ if (await C(() => window.__cold.state().SC === 'end')) break; await A.waitForTimeout(400); }
  ok(await C(() => window.__cold.state().SC === 'end'), '15 명을 다 고치면 양호실에서 끝 장면이 나와요');
  for (let i = 0; i < 40; i++){ if (await C(() => (window.__cold.sick('sera') || []).length === 4)) break; await A.waitForTimeout(300); }
  await A.waitForTimeout(1500); await A.screenshot({ path: OUT + '/sera_sick.png' });
  await A.screenshot({ path: OUT + '/sera_zoom.png', clip: { x: 55, y: 230, width: 280, height: 280 } });
  for (let i = 0; i < 40; i++){ if (await C(() => !window.__cold.state().coldOn)) break; await A.waitForTimeout(400); }
  ok(await C(() => window.__cold.state().cold.end === 1 && window.__cold.sick('sera').length === 4), '세라 선생님 머리 위에 증상 네 가지');
  await C(() => __T.npcMenu(__T.npcGet('sera'))); await A.waitForTimeout(500);
  await A.tap('#npcui [data-nx="cold"]'); await A.waitForTimeout(800); await A.screenshot({ path: OUT + '/sera_give.png' });
  const ha = await C(() => __T.me().npc.sera.a);
  for (const k of ['fever', 'throat', 'nose']){ await A.tap(`[data-cdg="${k}"]`); await A.waitForTimeout(700); }
  ok(await C(() => window.__cold.sick('sera').length === 1), '하나씩 건네면 말풍선이 하나씩 없어져요');
  await A.tap('#coldv [data-cdx="close"]'); await A.waitForTimeout(800); await A.screenshot({ path: OUT + '/sera_one_left.png' });
  await C(() => window.__cold.treat('sera')); await A.waitForTimeout(600); await A.tap('[data-cdg="chill"]');
  for (let i = 0; i < 30; i++){ if (await C(() => window.__cold.state().cold.end === 2)) break; await A.waitForTimeout(500); }
  await A.waitForTimeout(500); await A.screenshot({ path: OUT + '/ending_card.png' });
  for (let i = 0; i < 40; i++){ if (await C(() => !window.__cold.state().coldOn)) break; await A.waitForTimeout(400); }
  const fin = await C(() => ({ c: __T.me().cold, fb: __T.me().fbag, buff: (__T.me().buffs || {}).cold, a: __T.me().npc.sera.a, bub: __T.me().cos.bub }));
  ok(fin.c.end === 2 && fin.c.rw.end === 1 && fin.fb.cold_blanket === 1 && fin.fb.cold_cabinet === 1 && fin.bub.bandage === 1 && fin.buff > Date.now() + 2.9 * 864e5, '끝: 담요 · 약장 · 반창고 말풍선 · 3 일 물약 회복량 +10 %');
  ok(fin.a >= ha + 60, '세라 선생님 하트 +60');
  await A.waitForTimeout(1200); await A.screenshot({ path: OUT + '/ending_joke.png' });
  let joke = false; for (let i = 0; i < 30 && !joke; i++) joke = await C(() => window.__cold.line('sera') === '후후, 이번 물약은.... 조금 덜 써. 정말이란다.');
  ok(joke, '그 뒤로 세라 선생님 농담 대사');
  // 일지
  await C(() => __T.openSheet('home', 'journal')); await A.waitForTimeout(600);
  ok(await C(() => !!document.querySelector('[data-jnt="cold"]')), '일지에 「감기」 탭'); await A.tap('[data-jnt="cold"]'); await A.waitForTimeout(500); await A.screenshot({ path: OUT + '/journal.png' }); await C(() => __T.closeSheet()); await A.waitForTimeout(400);
  // 관리자 카드
  await Ad.waitForTimeout(1200); c = await card(); await c.scrollIntoViewIfNeeded(); await Ad.waitForTimeout(300);
  ok((await Ad.evaluate(e => e.innerText, c)).includes('봄'), '관리자 카드: 학생별 며칠째 · 고친 수 · 끝 장면');
  await c.screenshot({ path: OUT + '/admin_card.png' });
  await Ad.click('[data-coldn="1"]'); await Ad.waitForTimeout(500); ok((await Ad.evaluate(() => window.__tree.cold.ctl.n)) === 4, '하루 환자 수 바꾸기');
  await Ad.click('[data-colda="stop"]'); await Ad.waitForTimeout(1200);
  ok(!(await C(() => window.__cold.open())) && !Object.keys(await C(() => window.__cold.state().sick)).length, '닫으면 아픈 NPC가 없어요');
  ok(await C(() => __T.me().cos.tag.nurse === 1 && __T.me().fbag.cold_blanket === 1), '닫아도 보상은 그대로');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3).join(' | '));
  const bad = res.filter(r => !r[0]); console.log(`\n${res.length - bad.length} / ${res.length} 통과`); await br.close(); process.exit(bad.length ? 1 : 0);
})();
