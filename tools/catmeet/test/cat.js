// 달밤 고양이 집회 전체 흐름 (휴대폰 화면 + 터치): 닫힘 → 관리자 시작 → 밤 시작 연출 (아기 고양이 · 나비) → 따라다니기 → 동네 고양이 다섯
//   (생선 · 옛날이야기 · 숨바꼭질 · 털실 공 · 잔교 30 초) → 아기 고양이 단계 → 이름 후보 · 글 검사 → 낮의 나비 힌트 → 광장 지붕 끝 장면 (친구 아기 고양이) → 보상 → 일지 → 창가 가구 → 관리자 카드 · 이름 숨기기 → 닫기
// 사용: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/catmeet/test/cat.js
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs');
const OUT = '/home/user/magionacademy/tools/catmeet/shots'; fs.mkdirSync(OUT, { recursive: true });
const spec = fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8');
const res = []; const ok = (c, m) => { res.push([!!c, m]); console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
  const me = seed.players.me1; me.babySeen = 'x'; me.npc = { ...me.npc, nabi: { a: 120 } };
  seed.players.fr1 = { ...JSON.parse(JSON.stringify(me)), nick: '서연' }; seed.approved = { me1: true, fr1: true };   // 학생 화면은 pub 만 들어요: pub 없는 친구는 approved 로 찾아 한 번 받아요
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const ctx = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const errs = [];
  const page = async (u, night) => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept()); await p.addInitScript(([sd, u, n]) => { window.__seed = sd; window.__uid = u; window.__catNight = n; }, [seed, u, night]); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000); for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } return p; };
  const A = await page('me1', 0);
  const C = (f, ...a) => A.evaluate(f, ...a);
  const until = async (f, n = 60, ms = 300, a) => { for (let i = 0; i < n; i++){ if (await C(f, a)) return true; await A.waitForTimeout(ms); } return false; };
  const props = () => C(() => { const t = World.meTile(); return World.propsAt(t.m).map(p => p.id); });
  const tp = (m, x, y) => C(([m, x, y]) => new Promise(r => World.teleport(m, [x, y], () => setTimeout(r, 1800))), [m, x, y]);
  const zoom = async () => { await C(() => World.zoomStep && World.zoomStep(-3)); await A.waitForTimeout(500); };
  // 1 닫힘
  ok(!(await C(() => window.__cat.open())), '닫혀 있으면 이벤트가 없어요');
  await C(() => { window.__catNight = 1; }); await A.waitForTimeout(2000);
  ok(!(await C(() => window.__cat.state().SC)) && !(await props()).some(id => /^cat/.test(id)), '닫혀 있으면 밤이어도 연출 · 고양이가 없어요');
  await C(() => { window.__catNight = 0; });
  // 2 관리자 시작
  const Ad = await page('admin', 0); await Ad.setViewportSize({ width: 1000, height: 1000 });
  await Ad.evaluate(() => __T.showAdmin()); await Ad.waitForTimeout(1500); await Ad.click('[data-adtab="event"]'); await Ad.waitForTimeout(2000);
  const card = async () => (await Ad.evaluateHandle(() => [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('달밤 고양이 집회') && c.querySelector('[data-cata]')))).asElement();
  let c = await card(); ok(!!c, '관리자: 아직 안 연 일회성 이벤트에 「달밤 고양이 집회」 카드');
  await c.scrollIntoViewIfNeeded(); if ((await Ad.evaluate(e => e.innerText.length, c)) < 80){ await Ad.evaluate(e => e.querySelector('.abhead b').click(), c); await Ad.waitForTimeout(600); }
  await Ad.click('[data-cata="go"]'); await Ad.waitForTimeout(800);
  const ctl = await Ad.evaluate(() => window.__tree.cat && window.__tree.cat.ctl);
  ok(ctl && ctl.open === true && ctl.id, '관리자가 시작하면 cat/ctl { open, id }');
  await A.waitForTimeout(3000);
  ok(await C(() => window.__cat.open() && !window.__cat.state().SC && !(__T.me().cat && __T.me().cat.seen)), '낮에는 시작 연출이 안 나와요');
  // 3 밤: 시작 연출
  await tp('town', 44, 47); await zoom();
  await C(() => { window.__catNight = 1; });
  ok(await until(() => window.__cat.state().SC === 'intro'), '밤이 되면 시작 연출이 나와요 (학생이 서 있는 자리)');
  await A.waitForTimeout(4200); await A.screenshot({ path: OUT + '/intro_baby.png' });
  await A.waitForTimeout(5500); await A.screenshot({ path: OUT + '/intro_nabi.png' });
  ok(await until(() => !!document.querySelector('.sdcardv'), 100), '연출 뒤 안내 카드'); await A.waitForTimeout(800); await A.screenshot({ path: OUT + '/intro_card.png' });
  await until(() => !window.__cat.state().catOn && !document.querySelector('.sdcardv'), 60);
  let st = await C(() => window.__cat.state());
  ok(st.cat.seen === 1 && st.cat.d0 === await C(() => window.__cat.nd()) && st.stage === 1, '시작한 밤 저장 · 아기 고양이 부스스 (1 단계)');
  await A.waitForTimeout(1200);
  ok((await props()).includes('catbaby'), '아기 고양이가 따라와요 (내 화면 소품)');
  await C(() => World.walkToTile(World.meTile().x + 3, World.meTile().y)); await A.waitForTimeout(1500);
  ok((await props()).includes('catbaby'), '걸어도 따라와요');
  ok(JSON.stringify(st.avail) === '["cheese"]', '첫날 밤엔 뚱보 치즈만 ' + JSON.stringify(st.avail));
  // 4 뚱보 치즈: 생선
  const AT = await C(() => window.__cat.AT);
  await tp(...AT.cheese.slice(0, 2), AT.cheese[2] + 2); await zoom();
  ok((await props()).includes('cat:cheese'), '생선 가게 지붕에 뚱보 치즈');
  await A.screenshot({ path: OUT + '/cheese_roof.png' });
  { // 화면에서 손가락으로 고양이를 눌러요 (크기를 줄여 그린 소품도 눌려야 해요): 멀면 걸어가고, 닿으면 창이 열려요
    for (let t = 0; t < 6 && !(await C(() => !!document.getElementById('catv'))); t++){ const xy = await C(() => World.propClient('cat:cheese')); if (xy) await A.touchscreen.tap(xy[0], xy[1]); await A.waitForTimeout(2500); }
    ok(await C(() => !!document.getElementById('catv')), '화면에서 뚱보 치즈를 누르면 창이 열려요');
    await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(500); }
  await C(() => { const I = __T.me().inv; Object.keys(I).forEach(k => { if (window.__cat.isFish(k)) I[k] = 0; }); });
  await C(() => window.__cat.tap('cat:cheese')); await A.waitForTimeout(700);
  ok(await C(() => !!document.getElementById('catv') && !document.querySelector('[data-ctf]')), '생선이 없으면 줄 수 없어요');
  await A.screenshot({ path: OUT + '/cheese_nofish.png' });
  await A.tap('[data-ctx="close"]'); await A.waitForTimeout(500);
  ok(await C(() => window.__cat.isFish('f_crucian') && window.__cat.isFish('f_trout') && !window.__cat.isFish('f_witch') && !window.__cat.isFish('d_moontrout')), '붕어 · 송어만 (금붕어 · 요리는 빼요)');
  await C(() => { __T.setInv('f_crucian', 2); __T.setInv('f_trout', 1); });
  await C(() => window.__cat.tap('cat:cheese')); await A.waitForTimeout(700); await A.screenshot({ path: OUT + '/cheese_fish.png' });
  await A.tap('[data-ctf="f_crucian"]'); await A.waitForTimeout(900);
  st = await C(() => window.__cat.state());
  ok(st.cat.rec.cheese === 1 && (await C(() => __T.me().inv.f_crucian)) === 1, '붕어 한 마리 → 추천');
  ok(await C(() => __T.me().cos.tag.catfriend === 1 && (__T.me().inv.whisker || 0) >= 2), '첫 추천 → 이름표 「고양이 친구」 · 선물 고양이 수염');
  await A.screenshot({ path: OUT + '/cheese_rec.png' }); await A.waitForTimeout(1500); await A.screenshot({ path: OUT + '/reward_tag.png' });
  await A.waitForTimeout(2500); await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(600);
  // 5 줄무늬 할배 (2 일째 밤): 옛날이야기 선택지 3 번
  await C(() => { __T.me().cat.d0 -= 1; });
  ok(JSON.stringify(await C(() => window.__cat.state().avail)) === '["grandpa"]', '이튿날 밤: 줄무늬 할배');
  await tp(...AT.grandpa.slice(0, 2), AT.grandpa[2] + 2); await zoom();
  ok((await props()).includes('cat:grandpa'), '시계탑 처마에 줄무늬 할배'); await A.screenshot({ path: OUT + '/grandpa_eaves.png' });
  await C(() => window.__cat.tap('cat:grandpa')); await A.waitForTimeout(600); await A.tap('[data-ctx="listen"]'); await A.waitForTimeout(300);
  await A.screenshot({ path: OUT + '/grandpa_story.png' });
  await A.tap('[data-ctx="close"]'); await A.waitForTimeout(500);
  await C(() => window.__cat.tap('cat:grandpa')); await A.waitForTimeout(600);
  ok(await C(() => !!document.querySelector('[data-ctx="listen"]')), '중간에 닫으면 처음부터 다시 들어요');
  await A.tap('[data-ctx="listen"]'); await A.waitForTimeout(300);
  for (let i = 0; i < 3; i++){ await A.tap(`[data-ctc="${i % 2}"]`); await A.waitForTimeout(300); if (i === 2) await A.screenshot({ path: OUT + '/grandpa_last.png' }); if (i < 2) ok(await C(() => !window.__cat.state().cat.rec.grandpa), `선택지 ${i + 1} 번째 · 아직 추천 전`); await A.tap('[data-ctx="next"]'); await A.waitForTimeout(400); }
  st = await C(() => window.__cat.state());
  ok(st.cat.rec.grandpa === 1 && st.stage === 2, '끝까지 들으면 추천 · 아기 고양이 털이 조금 정리 (2 단계)');
  await A.waitForTimeout(1500); await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(600);
  // 6 검은 망토 (3 일째 밤): 숨바꼭질 세 번
  await C(() => { __T.me().cat.d0 -= 1; });
  await tp(...AT.cloak.slice(0, 2), AT.cloak[2] + 2); await zoom();
  ok((await props()).includes('cat:cloak'), '묘지 담장에 검은 망토'); await A.screenshot({ path: OUT + '/cloak_wall.png' });
  await C(() => window.__cat.tap('cat:cloak')); await A.waitForTimeout(600); await A.tap('[data-ctx="hide"]'); await A.waitForTimeout(2000);
  st = await C(() => window.__cat.state());
  ok(st.hs && st.hs.at.length === 3 && !(await props()).includes('cat:cloak') && (await props()).filter(x => /^catsh:/.test(x)).length === 3, '그림자 세 곳 · 검은 망토는 숨었어요');
  await A.screenshot({ path: OUT + '/cloak_shadows.png' });
  { const w = [0, 1, 2].find(i => i !== st.hs.i), [x, y] = st.hs.at[w]; await tp('town', x, y + 1); await C(i => window.__cat.tap('catsh:' + i), w); await A.waitForTimeout(500);
    ok(await C(() => window.__cat.state().hs.n === 0), '빈 그림자: 아무도 없어요'); }
  for (let r = 0; r < 3; r++){ const h = await C(() => window.__cat.state().hs), [x, y] = h.at[h.i]; await tp('town', x, y + 1); await C(i => window.__cat.tap('catsh:' + i), h.i); await A.waitForTimeout(1200); if (r === 0) await A.screenshot({ path: OUT + '/cloak_found.png' }); await until(() => !window.__cat.state().SC, 40); await A.waitForTimeout(400); }
  st = await C(() => window.__cat.state());
  ok(!st.hs && st.cat.rec.cloak === 1, '세 번 찾으면 추천');
  await A.waitForTimeout(1500); await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(600);
  // 7 방울 삼색이 (4 일째 밤): 털실 공
  await C(() => { __T.me().cat.d0 -= 1; __T.setInv('wool', 0); const K = __T.me(); K.knit = null; });
  await tp(...AT.calico.slice(0, 2), AT.calico[2] + 2); await zoom();
  ok((await props()).includes('cat:calico'), '등불 시장 차양에 방울 삼색이'); await A.screenshot({ path: OUT + '/calico_awning.png' });
  await C(() => window.__cat.tap('cat:calico')); await A.waitForTimeout(600);
  ok(await C(() => document.querySelector('[data-ctx="yarn"]').disabled), '털실 · 양털이 없으면 못 만들어요'); await A.screenshot({ path: OUT + '/calico_none.png' });
  await A.tap('[data-ctx="close"]'); await A.waitForTimeout(400);
  await C(() => { __T.me().knit = { yarn: { red: 2, white: 1 } }; });
  await C(() => window.__cat.tap('cat:calico')); await A.waitForTimeout(600); await A.screenshot({ path: OUT + '/calico_yarn.png' });
  await A.tap('[data-ctx="yarn"]'); await A.waitForTimeout(900);
  ok(await C(() => window.__cat.state().cat.rec.calico === 1 && __T.me().knit.yarn.red === 1), '뜨개질 털실 1 뭉치 → 털실 공 → 추천');
  await A.waitForTimeout(1500); await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(600);
  // 8 하얀 공주 (5 일째 밤): 30 초 가만히
  await C(() => { __T.me().cat.d0 -= 1; });
  await tp('town', AT.princess[1], AT.princess[2] + 2); await zoom();
  ok((await props()).includes('cat:princess'), '잔교 끝에 하얀 공주'); await A.screenshot({ path: OUT + '/princess_pier.png' });
  await C(() => window.__cat.tap('cat:princess')); await A.waitForTimeout(600); await A.screenshot({ path: OUT + '/princess_hi.png' });
  await A.tap('[data-ctx="wait"]'); await A.waitForTimeout(700);
  await C(() => World.walkToTile(World.meTile().x - 1, World.meTile().y)); await A.waitForTimeout(1500);
  ok(await C(() => !window.__cat.state().wait), '움직이면 아기 고양이가 다시 숨어요');
  await C(() => window.__cat.tap('cat:princess')); await A.waitForTimeout(500); await A.tap('[data-ctx="wait"]'); await A.waitForTimeout(1200);
  ok(await C(() => !window.__cat.state().cat.rec.princess && !!window.__cat.state().wait), '30 초 전에는 아직이에요');
  await C(() => window.__cat.waitT(29000));
  ok(await until(() => window.__cat.state().SC === 'wait', 20), '30 초 가만히 서 있으면 아기 고양이가 직접 인사해요');
  await A.waitForTimeout(2500); await A.screenshot({ path: OUT + '/princess_greet.png' });
  ok(await until(() => window.__cat.state().cat.rec.princess === 1, 40), '하얀 공주의 추천');
  await A.waitForTimeout(1500); await A.screenshot({ path: OUT + '/princess_rec.png' });
  await until(() => !document.querySelector('.sdcardv'), 30); await A.waitForTimeout(3000);
  st = await C(() => window.__cat.state());
  ok(Object.keys(st.cat.rec).length === 5 && (await C(() => __T.me().fbag.cat_window)) === 1, '추천 다섯 → 가구 「창가의 아기 고양이」');
  await A.tap('[data-ctx="close"]').catch(() => {}); await A.waitForTimeout(500);
  // 9 이름 후보 · 글 검사
  await C(() => window.__cat.ev('fish', { k: 'f_crucian' })); await C(() => window.__cat.ev('harvest', { k: 'g_sung' }));
  ok(await C(() => { const n = window.__cat.state().cat.names; return n.includes('붕어빵') && n.includes('호박'); }), '붕어를 낚으면 「붕어빵」 · 호박을 캐면 「호박」 후보');
  ok(await C(() => !!window.__cat.nameErr('바보') && !!window.__cat.nameErr('abc1') && !!window.__cat.nameErr('일곱글자이름요') && !window.__cat.nameErr('까망이')), '직접 쓰는 이름은 글 검사 (욕 · 숫자 · 6 자 넘음)');
  // 10 낮의 나비 힌트
  await C(() => { window.__catNight = 0; });
  ok(await C(() => /광장 지붕/.test(window.__cat.line())), `낮에 나비: 「${await C(() => window.__cat.line())}」`);
  await C(() => { __T.npcMenu(__T.npcGet('nabi')); }); await A.waitForTimeout(600); await A.screenshot({ path: OUT + '/nabi_hint.png' }); await C(() => document.querySelector('#npcui .sx, #npcui [data-nx="close"]') && document.querySelector('#npcui .sx, #npcui [data-nx="close"]').click()); await A.waitForTimeout(400);
  // 11 끝 장면: 같은 날 끝낸 친구 아기 고양이
  const nd = await C(() => window.__cat.nd());
  await C(([id, nd]) => { __T.pkSet('players/fr1/cat', { ev: id, seen: 1, d0: nd - 4, rec: { cheese: 1, grandpa: 1, cloak: 1, calico: 1, princess: 1 }, names: [], name: '치즈볼', done: nd, rw: 'tfe' }); __T.pkSet('pub/fr1/cat', { ev: id, done: nd }); __T.pkSet('cat/names/fr1', '치즈볼'); }, [ctl.id, nd]);
  await A.waitForTimeout(1200);
  ok((await C(() => window.__cat.friends())).length === 1, '같은 날 끝낸 친구 아기 고양이 1 마리');
  await C(() => { window.__catNight = 1; }); await tp('town', 42, 49);
  ok(await until(() => window.__cat.state().SC === 'end', 40), '밤 · 광장에 가면 지붕 위 집회');
  await A.waitForTimeout(6000); await A.screenshot({ path: OUT + '/end_meeting.png' });
  ok(await until(() => !!document.querySelector('[data-ctn]'), 60), '이름 고르기'); await A.waitForTimeout(300); await A.screenshot({ path: OUT + '/end_pick.png' });
  await A.fill('#catsc .nin input', '바보'); await A.tap('#catsc [data-ctn=""]'); await A.waitForTimeout(300);
  ok(await C(() => !!document.querySelector('#catsc .err').textContent && !!document.querySelector('[data-ctn]')), '글 검사에 걸리면 다시 써요');
  await A.tap('[data-ctn="붕어빵"]'); await A.waitForTimeout(3500); await A.screenshot({ path: OUT + '/end_nya.png' });
  await A.waitForTimeout(6500); await A.screenshot({ path: OUT + '/end_wrap.png' });
  ok(await until(() => window.__cat.state().cat.done > 0, 60), '끝 장면 끝');
  await A.waitForTimeout(1200); await A.screenshot({ path: OUT + '/end_reward.png' });
  await until(() => !window.__cat.state().catOn, 60);
  const fin = await C(() => ({ c: __T.me().cat, a: __T.me().npc.nabi.a, bub: __T.me().cos.bub, nm: window.__tree.cat.names.me1 }));
  ok(fin.c.name === '붕어빵' && fin.nm === '붕어빵' && fin.c.done === nd, '이름 저장 (me.cat.name · cat/names)');
  ok(fin.a >= 200 && fin.bub.paw === 1, '나비 하트 +80 · 말풍선 「고양이 발자국 말풍선」');
  ok(!(await props()).includes('catbaby'), '끝나면 아기 고양이는 더는 따라다니지 않아요 (창가로)');
  ok(await C(() => window.__cat.state().stage === 3), '아기 고양이 회원 (3 단계 · 목줄)');
  // 12 이름표 · 말풍선
  await C(() => { __T.me().cosOn = { ...(__T.me().cosOn || {}), tg: 'catfriend', bb: 'paw' }; World.setMyCos('catfriend', 'paw'); }); await A.waitForTimeout(1500); await C(() => { World.setMyCos('catfriend', 'paw'); World.say('me', '냐옹, 회원이 됐어요'); }); await A.waitForTimeout(300);
  await A.screenshot({ path: OUT + '/tag_bubble.png', clip: { x: 45, y: 250, width: 300, height: 260 } });
  // 13 일지
  await C(() => __T.openSheet('home', 'journal')); await A.waitForTimeout(600);
  ok(await C(() => !!document.querySelector('[data-jnt="cat"]')), '일지에 「고양이」 탭'); await A.tap('[data-jnt="cat"]'); await A.waitForTimeout(500);
  ok(await C(() => document.querySelector('#app').innerText.includes('치즈볼')), '일지: 반 아기 고양이 이름');
  await A.screenshot({ path: OUT + '/journal.png' }); await C(() => __T.closeSheet()); await A.waitForTimeout(400);
  // 14 창가 가구
  await C(() => __T.placeFurn('cat_window')); await A.waitForTimeout(3000);
  ok(await C(() => !!World.furnDyn.cat_window), '창가 가구 그림');
  await C(() => { World.cancelPlace(); const t = World.meTile(), c = World.freeNear(t.x, t.y, 3).find(([x, y]) => Math.abs(x - t.x) + Math.abs(y - t.y) >= 2) || [t.x + 2, t.y]; const k = World.FURN.items.findIndex(i => i.id === 'cat_window'); __T.me().room.push({ id: 'cw1', f: 'cat_window', x: c[0], y: c[1] }); World.setFurniture(__T.me().room.map(r => ({ id: r.id, k: World.FURN.items.findIndex(i => i.id === r.f), x: r.x, y: r.y, r: 0 }))); });
  await A.waitForTimeout(1200); await C(() => World.zoomStep && World.zoomStep(-3)); await A.waitForTimeout(600);
  await A.screenshot({ path: OUT + '/room_window.png' });
  ok(await C(() => /창가에서|놀러 오지/.test((World.onFurn('cw1') || {}).text || '')), '창가 가구를 누르면 「붕어빵」 소식 ' + await C(() => ((World.onFurn('cw1') || {}).text || '').replace(/<[^>]+>/g, ' ')));
  // 15 관리자 카드 · 이름 숨기기
  await Ad.waitForTimeout(1500); c = await card(); await c.scrollIntoViewIfNeeded(); await Ad.waitForTimeout(300);
  const tx = await Ad.evaluate(e => e.innerText, c);
  ok(tx.includes('추천 5 / 5') && tx.includes('붕어빵') && tx.includes('끝냄') && tx.includes('치즈볼'), '관리자 카드: 추천 수 · 이름 · 끝냄 · 이름 목록');
  await c.screenshot({ path: OUT + '/admin_card.png' });
  await Ad.click('[data-cath="fr1:1"]'); await Ad.waitForTimeout(800);
  ok(await Ad.evaluate(() => window.__tree.cat.hide && window.__tree.cat.hide.fr1 === true), '이름 숨기기 → cat/hide/fr1');
  await A.waitForTimeout(800);
  ok((await C(() => window.__cat.friends())).length === 0 && !(await C(() => Object.keys(window.__cat.state().hide).length === 0)), '숨긴 이름은 안 보여요');
  c = await card(); await c.screenshot({ path: OUT + '/admin_hidden.png' });
  ok(await Ad.evaluate(() => __T.admOv().includes('달밤 고양이 집회')), '이벤트 한눈에: 달밤 고양이 집회');
  // 16 닫기
  await Ad.click('[data-cata="stop"]'); await Ad.waitForTimeout(1200);
  ok(!(await C(() => window.__cat.open())), '닫으면 이벤트 끝');
  ok(await C(() => __T.me().cos.tag.catfriend === 1 && __T.me().cos.bub.paw === 1), '닫아도 보상은 그대로');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3).join(' | '));
  const bad = res.filter(r => !r[0]); console.log(`\n${res.length - bad.length} / ${res.length} 통과`); await br.close(); process.exit(bad.length ? 1 : 0);
})();
