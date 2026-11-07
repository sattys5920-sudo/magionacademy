// 겨울잠 준비 전체 흐름 (휴대폰 화면 + 터치): 닫힘 → 관리자 시작 → 시작 연출 → 지도 → 넣기 (좋아하는 것 · 아닌 것 · 독 · 하루 15 점) → 굴 단계 → 가득 참 → 잠드는 장면 → 방 앞 선물 → 다른 학생 → 곰 (반 전체) → 관리자 카드 → 닫기
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const { mkSeed } = require('./common.js');
const OUT = '/home/user/magionacademy/tools/hibernate/shots'; const res = []; const ok = (c, m) => { res.push([!!c, m]); console.log(c ? '  ok ' : '  XX ', m); };
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const seed = mkSeed(); for (const u of ['me1', 'me2', 'me3']){ const m = seed.players[u]; m.babySeen = 'x'; m.inv = { ...(m.inv || {}), g2_acorn: 8, g2_chest: 3, g2_reed: 4, g2_mushred: 2, g2_frostleaf: 4, g2_snowdrop: 3, f_frostcarp: 2, honey: 2, g2_birch: 2 }; }
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const ctx = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const errs = [];
  const page = async u => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept()); await p.addInitScript(([sd, u]) => { window.__seed = sd; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000); for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const hibProps = p => p.evaluate(() => ['campus', 'town'].flatMap(m => World.propsAt(m).filter(o => /^hib_/.test(o.id)).map(o => o.id)));
  const A = await page('me1'), B = await page('me2'), C = await page('me3');   // 모의 DB는 열린 창끼리만 나눠 써요 → 처음부터 띄워 둬요
  // 1 닫힘
  ok(!(await A.evaluate(() => window.__hib.open())) && (await hibProps(A)).length === 0, '닫혀 있으면 굴이 없어요');
  ok(!(await A.evaluate(() => window.__hib.state().hibOn)) && !(await A.evaluate(() => World.cutBusy && World.cutBusy())), '닫혀 있으면 연출이 없어요');
  await A.evaluate(() => __T.openSheet('home', 'journal')); await A.waitForTimeout(600);
  ok(!(await A.evaluate(() => !!document.querySelector('[data-jnt="hib"]'))), '닫혀 있으면 일지 탭이 없어요'); await A.evaluate(() => __T.closeSheet()); await A.waitForTimeout(300);
  ok(await A.evaluate(() => __T.npcGet('batri') && !window.__hib.line('batri')), '닫혀 있으면 배트리 대사가 그대로예요');
  // 2 관리자 시작
  const Ad = await page('admin'); await Ad.setViewportSize({ width: 1000, height: 1000 });
  await Ad.evaluate(() => __T.showAdmin()); await Ad.waitForTimeout(1500); await Ad.click('[data-adtab="event"]'); await Ad.waitForTimeout(2000);
  const card = async () => { const h = await Ad.evaluateHandle(() => [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('겨울잠 준비'))); return h.asElement(); };
  let c = await card(); await c.scrollIntoViewIfNeeded(); if ((await Ad.evaluate(e => e.innerText.length, c)) < 120){ await Ad.evaluate(e => e.querySelector('.abhead b').click(), c); await Ad.waitForTimeout(600); }
  await Ad.click('[data-hiba="go"]'); await Ad.waitForTimeout(800);
  ok((await Ad.evaluate(() => window.__tree.hib && window.__tree.hib.ctl && window.__tree.hib.ctl.open)) === true, '관리자가 시작하면 hib/ctl.open');
  // 3 시작 연출
  for (let i = 0; i < 40; i++){ if (await A.evaluate(() => !!(World.cutBusy && World.cutBusy()))) break; await A.waitForTimeout(300); }
  ok(await A.evaluate(() => !!(World.cutBusy && World.cutBusy())), '시작 연출이 나와요');
  await A.waitForTimeout(6200); await A.screenshot({ path: OUT + '/intro.png' });
  for (let i = 0; i < 80; i++){ if (await A.evaluate(() => !!document.getElementById('hibmap'))) break; await A.waitForTimeout(400); }
  await A.waitForTimeout(1500); await A.screenshot({ path: OUT + '/map.png' });
  ok(await A.evaluate(() => !!document.getElementById('hibmap') && window.__hib.state().hib.hi === 1), '연출 뒤 겨울잠 지도');
  ok((await hibProps(A)).length === 6, '굴 여섯 곳이 맵에 놓여요');
  // 지도 「가기」 → 겨울잠쥐 굴 앞 (터치)
  await A.tap('[data-hibgo="dormouse"]'); await A.waitForTimeout(3200);
  const t = await A.evaluate(() => World.meTile()); ok(t.m === 'campus' && Math.abs(t.x - 45) + Math.abs(t.y - 100) <= 2, '가기 → 굴 앞 ' + JSON.stringify(t));
  await A.screenshot({ path: OUT + '/den_stage0.png' });
  // 4 넣기
  await A.evaluate(() => window.__hib.openWin('dormouse')); await A.waitForTimeout(600);
  await A.tap('[data-hibk="g2_mushred"]'); await A.waitForTimeout(200); ok((await A.textContent('#hibv .hmsg')).includes('배 아파'), '독버섯은 안 받아요');
  await A.screenshot({ path: OUT + '/give_poison.png' });
  await A.tap('[data-hibk="g2_acorn"]'); await A.tap('[data-hibk="g2_acorn"]'); await A.tap('[data-hibk="g2_snowdrop"]'); await A.waitForTimeout(200);
  ok((await A.textContent('[data-hibx="give"]')).includes('8 점'), '도토리 (좋아해요 1 × 2) × 2 + 설강화 (드묾 4) = 8 점');
  await A.screenshot({ path: OUT + '/give.png' });
  await A.tap('[data-hibx="give"]'); await A.waitForTimeout(900);
  let H = await A.evaluate(() => window.__tree.hib); ok(H.den.dormouse.f === 8 && H.give.dormouse.me1 === 8, '게이지 8 · 내 기록 8');
  await A.tap('[data-hibt="b"]'); await A.waitForTimeout(200); await A.tap('[data-hibk="g2_reed"]'); await A.tap('[data-hibk="g2_reed"]'); await A.tap('[data-hibk="g2_reed"]'); await A.tap('[data-hibk="g2_reed"]'); await A.waitForTimeout(200);
  ok((await A.textContent('[data-hibx="give"]')).includes('7 점'), '하루 15 점: 마른 갈대 넷 (8 점) 중 7 점만 · ' + (await A.textContent('[data-hibx="give"]')));
  await A.tap('[data-hibx="give"]'); await A.waitForTimeout(900);
  H = await A.evaluate(() => window.__tree.hib); ok(H.den.dormouse.b === 7 && H.give.dormouse.me1 === 15 && Object.values(H.day.me1)[0].dormouse === 15, '이불 7 · 합계 15 · 오늘 15');
  await A.tap('[data-hibt="f"]'); await A.waitForTimeout(200); await A.tap('[data-hibk="g2_chest"]'); await A.waitForTimeout(200);
  ok((await A.textContent('#hibv .hmsg')).includes('내일') && await A.evaluate(() => document.querySelector('[data-hibx="give"]').disabled), '오늘은 더 못 넣어요');
  await A.screenshot({ path: OUT + '/give_cap.png' });
  ok(await A.evaluate(() => __T.me().cos.tag.hib === 1), '처음 넣기 → 이름표 「숲 지킴이」');
  await A.tap('[data-hibx="close"]'); await A.waitForTimeout(500);
  // 5 굴 단계 (먹이 절반 → 1 단계, 둘 다 절반 → 2 단계)
  await A.evaluate(() => __T.pkSet('hib/den/dormouse/f', 44)); await A.waitForTimeout(1200); ok((await A.evaluate(() => window.__hib.stage('dormouse'))) === 1, '1 단계'); await A.screenshot({ path: OUT + '/den_stage1.png' });
  await A.evaluate(() => __T.pkSet('hib/den/dormouse/b', 22)); await A.waitForTimeout(1500); ok((await A.evaluate(() => window.__hib.stage('dormouse'))) === 2, '2 단계'); await A.screenshot({ path: OUT + '/den_stage2.png' });
  // 6 다른 학생이 마지막으로 채워요
  await A.evaluate(() => { __T.pkSet('hib/den/dormouse/f', 78); __T.pkSet('hib/den/dormouse/b', 40); }); await A.waitForTimeout(600);
  for (let i = 0; i < 60; i++){ if (await B.evaluate(() => window.__hib.state().hib && window.__hib.state().hib.hi === 1 && !World.cutBusy())) break; await B.evaluate(() => document.querySelector('.mqskip')?.click()); await B.waitForTimeout(500); }
  for (let i = 0; i < 10; i++){ if (await B.evaluate(() => !!document.getElementById('hibmap'))) break; await B.waitForTimeout(300); } await B.evaluate(() => document.querySelector('[data-hibmx]')?.click()); await B.waitForTimeout(500);
  await B.evaluate(() => World.teleport('campus', [46, 100])); await B.waitForTimeout(3000);
  await B.evaluate(() => window.__hib.openWin('dormouse')); await B.waitForTimeout(500); await B.tap('[data-hibk="g2_snowdrop"]'); await B.waitForTimeout(100);
  ok((await B.textContent('[data-hibx="give"]')).includes('2 점'), '마지막은 남은 만큼만 (2 점) · ' + (await B.textContent('[data-hibx="give"]')));
  await B.tap('[data-hibx="give"]'); await B.waitForTimeout(1200);
  H = await A.evaluate(() => window.__tree.hib); ok(H.den.dormouse.f === 80 && H.den.dormouse.slept > 0, '가득 차면 잠든 시각');
  // 7 잠드는 장면 (A: 굴 앞)
  for (let i = 0; i < 30; i++){ if (await A.evaluate(() => !!document.getElementById('hibsc'))) break; await A.waitForTimeout(300); }
  ok(await A.evaluate(() => !!document.getElementById('hibsc')), 'A 화면에 잠드는 장면');
  await A.waitForTimeout(3600); await A.screenshot({ path: OUT + '/sleep_bow.png' });
  ok(await A.evaluate(() => window.__hib.state().SC), '');
  await A.waitForTimeout(3600); await A.screenshot({ path: OUT + '/sleep_scene.png' });
  for (let i = 0; i < 30; i++){ if (!(await A.evaluate(() => !!document.getElementById('hibsc')))) break; await A.waitForTimeout(400); }
  ok(await A.evaluate(() => window.__hib.state().hib.seen.dormouse === 1), '장면은 한 번만 (seen)');
  await A.waitForTimeout(800); await A.screenshot({ path: OUT + '/den_stage3.png' });
  ok(await A.evaluate(() => window.__hib.pending().includes('dormouse')), '선물이 기다려요');
  // 8 방 앞 선물
  await A.evaluate(() => document.getElementById('tHome')?.click()); await A.waitForTimeout(4000); await A.evaluate(() => window.__hib.door()); await A.waitForTimeout(400);
  ok(await A.evaluate(() => World.propsAt(World.where()).some(o => o.id === 'hibdoor')), '방 문 옆에 선물 꾸러미');
  await A.screenshot({ path: OUT + '/gift_door.png' });
  await A.evaluate(() => window.__hib.takeGift()); await A.waitForTimeout(900); await A.screenshot({ path: OUT + '/gift.png' });
  ok(await A.evaluate(() => __T.me().fbag.hib_cushion === 1 && __T.me().hib.gift.dormouse === 1 && !World.propsAt(World.where()).some(o => o.id === 'hibdoor')), '겨울잠쥐 쿠션을 받았어요');
  // 9 세 번째 학생 (안 넣었어요): 장면은 보지만 선물은 없어요 · 누르면 쉿
  for (let i = 0; i < 60; i++){ if (await C.evaluate(() => window.__hib.state().hib && window.__hib.state().hib.hi === 1 && !World.cutBusy())) break; await C.evaluate(() => document.querySelector('.mqskip')?.click()); await C.waitForTimeout(500); }
  for (let i = 0; i < 10; i++){ if (await C.evaluate(() => !!document.getElementById('hibmap'))) break; await C.waitForTimeout(300); } await C.evaluate(() => document.querySelector('[data-hibmx]')?.click()); await C.waitForTimeout(400);
  await C.evaluate(() => World.teleport('campus', [45, 101])); await C.waitForTimeout(3500);
  for (let i = 0; i < 20; i++){ if (await C.evaluate(() => !!document.getElementById('hibsc'))) break; await C.waitForTimeout(300); }
  ok(await C.evaluate(() => !!document.getElementById('hibsc')), '다른 학생도 굴 앞에 가면 장면 (한 번)');
  await C.click('[data-hibs="skip"]'); await C.waitForTimeout(800);
  ok(!(await C.evaluate(() => window.__hib.pending().length)), '안 넣은 학생은 선물 없음');
  ok((await C.evaluate(() => World.onProp('hib_dormouse'))) === '쉿, 자고 있어요', '잠든 굴은 쉿');
  ok((await B.evaluate(() => window.__hib.pending())).includes('dormouse'), '마지막에 넣은 학생도 선물');
  // 10 곰 (반 전체 장면 · 첫눈 · 채집량)
  await A.evaluate(() => { __T.pkSet('hib/den/bear/f', 160); __T.pkSet('hib/den/bear/b', 78); }); await A.waitForTimeout(800);
  await C.evaluate(() => World.teleport('campus', [53, 5])); await C.waitForTimeout(3200);
  await C.evaluate(() => window.__hib.openWin('bear')); await C.waitForTimeout(500); await C.tap('[data-hibt="b"]'); await C.waitForTimeout(150);
  await C.tap('[data-hibk="g2_frostleaf"]'); await C.waitForTimeout(150); ok((await C.textContent('[data-hibx="give"]')).includes('2 점'), '곰 이불: 서리 낙엽 (좋아해요) 2 점');
  await C.tap('[data-hibx="give"]'); await C.waitForTimeout(1500);
  for (let i = 0; i < 40; i++){ if (await A.evaluate(() => !!document.getElementById('hibsc'))) break; await A.waitForTimeout(300); }
  ok(await A.evaluate(() => !!document.getElementById('hibsc') && World.where() !== 'campus'), '곰은 다른 곳에 있어도 반 전체 장면');
  await A.waitForTimeout(10000); await A.screenshot({ path: OUT + '/sleep_bear.png' });
  for (let i = 0; i < 30; i++){ if (!(await A.evaluate(() => !!document.getElementById('hibsc')))) break; await A.waitForTimeout(400); }
  ok(await A.evaluate(() => (__T.me().buffs || {}).hib > Date.now() + 2.9 * 864e5), '모두 3 일 동안 채집량 +10 %');
  ok((await A.evaluate(() => window.__hib.line('batri'))).includes('다 찼다'), '배트리 마지막 대사');
  ok((await A.evaluate(() => window.__hib.pending())).length === 0, 'A는 곰에 안 넣어서 곰 선물 없음');
  // 일지
  await A.evaluate(() => __T.openSheet('home', 'journal')); await A.waitForTimeout(700); await A.evaluate(() => document.querySelector('[data-jnt="hib"]')?.click()); await A.waitForTimeout(700);
  await A.screenshot({ path: OUT + '/journal.png' }); ok(await A.evaluate(() => !!document.querySelector('[data-hibj]')), '일지 「겨울잠」 탭'); await A.evaluate(() => __T.closeSheet());
  // 11 관리자 카드 (±10)
  c = await card(); await c.scrollIntoViewIfNeeded(); await Ad.click('[data-hibadj="badger:f:10"]'); await Ad.waitForTimeout(600); ok((await Ad.evaluate(() => window.__tree.hib.den.badger.f)) === 10, '관리자 +10');
  await Ad.click('[data-hibadj="badger:f:-10"]'); await Ad.waitForTimeout(600); ok((await Ad.evaluate(() => window.__tree.hib.den.badger.f)) === 0, '관리자 −10');
  c = await card(); await c.scrollIntoViewIfNeeded(); await c.screenshot({ path: OUT + '/admin.png' });
  const txt = await Ad.evaluate(e => e.innerText, c); ok(/민준[\s\S]*넣은 점수 15 · 굴 1 곳/.test(txt), '학생별 합계 · 굴 수');
  // 12 닫기: 안 잠든 굴은 사라지고 잠든 굴은 남아요
  await Ad.click('[data-hiba="stop"]'); await Ad.waitForTimeout(1500);
  const pr = await hibProps(A); ok(pr.length === 2 && pr.includes('hib_dormouse') && pr.includes('hib_bear'), '닫으면 잠든 굴만 ' + JSON.stringify(pr));
  ok(await A.evaluate(() => { window.__hib.openWin('badger'); return !document.getElementById('hibv'); }), '닫으면 넣기 창이 안 열려요');
  console.log('errs', errs.filter(e => !/404/.test(e)));
  console.log(`\n${res.filter(r => r[0]).length} / ${res.length} ok`); await br.close(); })();
