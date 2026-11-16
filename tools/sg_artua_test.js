// 별 보는 밤 + 아르투아 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/sg_artua_test.js [그림 저장 폴더]
//   아르투아를 만난 학생: 스텔라 옆에 아르투아 · 모이기 / 별 켜기 / 하늘 / 이야기 끝 / 끝 인사에 아르투아 대사 · 하트 단계마다 다른 스텔라 ↔ 아르투아 이야기
//   별자리를 완성하면 별 지도 조각(me.smap) → 아르투아 NPC 창 「별 지도」 · 5 / 10 / 전부 보상 · 서버가 연 밤(ctl.srv = 1)과 관리자 진행 둘 다 · 못 만난 학생은 예전 그대로
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const OUT = process.argv[2] || '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad'; fs.mkdirSync(OUT, { recursive: true });
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
seed.players.me1.nnpc = Object.fromEntries(['bau', 'kael', 'artua', 'grego'].map(id => [id, { met: 1, at: 1 }]));
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await p.waitForFunction(() => __tw.ev("!!npcGet('artua') && !!sgData"), null, { timeout: 20000 }).catch(() => {});
  const say = () => ev(`({ who: $('#sgsay b').textContent, t: $('#sgtx').textContent })`);
  const AN = await ev(`npcGet('artua').name`), SN = await ev(`npcGet('stella').name`);
  const line = (k, T) => ev(`fillVars(SG_ART.${k}${T ? '.' + T : ''}, 'artua').replace(/\\{c\\}/g, sgConst(sgCtl.c).name)`);
  const ctl = o => ev(`(F.update(F.ref(db, 'stargaze/ctl'), ${o}), 1)`);
  ok(await ev(`['A','B','C','D'].every(T => SG_ART.talk[T].length === 4 && ['light','sky','done','gift','reply','bye'].every(k => SG_ART[k][T])) && JSON.stringify(SG_ART).match(/\\?!|!!/) === null`), '아르투아 대사 표: 단계 넷 다 있음');
  async function night(cid, srv, T, tag){
    await ev(`(npcSt('artua').a = ${{ A: 50, B: 350, C: 650, D: 950 }[T]}, sgClose(), sgLoadDlg('${cid}'), 1)`);
    await p.waitForFunction(c => __tw.ev(`!!sgDlg['${c}'] && !!sgDlg.common`), cid, { timeout: 10000 }).catch(() => {});
    const introN = await ev(`(sgDlg['${cid}'].intro || []).length`);
    // 모이기: 소개 뒤 쉬는 동안 스텔라 ↔ 아르투아 이야기 (7 초씩 번갈아)
    await ev(`(F.set(F.ref(db, 'stargaze/join'), null), F.set(F.ref(db, 'stargaze/lit'), null), F.set(F.ref(db, 'stargaze/ctl'), { open: true, id: now2(), c: '${cid}', ph: 'gather', at: now2() - (${introN} * 5500 + 7500), gm: 180000, lm: 60000, bm: 86400000, sm: 6000${srv ? ', srv: 1' : ''} }), 1)`); await p.waitForTimeout(400);
    await ev(`(F.set(F.ref(db, 'stargaze/join/' + myId()), { n: me.nick, at: now2() }), sgOpen(), 1)`); await p.waitForTimeout(900);
    ok(await ev(`sgModel().crowd.some(c => c.artua) && sgModel().crowd.findIndex(c => c.artua) === sgModel().crowd.findIndex(c => c.stella) + 1`), `${tag} 스텔라 옆에 아르투아`);
    let s = await say(); const X = await ev(`SG_ART.talk.${T}.map(([w, t]) => [w, fillVars(t, 'artua')])`);
    ok(X.some(([w, t]) => t === s.t && (w === 'artua' ? AN : SN) === s.who), `${tag} 모이기: ${T} 단계 이야기 「${s.who}」 ${s.t.slice(0, 30)}`);
    if (tag.includes('첫')) await p.screenshot({ path: OUT + `/sga_gather_${T}.png` });
    await ev(`(F.update(F.ref(db, 'stargaze/ctl'), { at: now2() - 1000 }), 1)`); await p.waitForTimeout(400);
    s = await say(); ok(s.who === SN, `${tag} 소개 중엔 스텔라 그대로`);
    // 별 나눠 주기 → 별 켜기: 내 별을 눌러요
    if (srv){ const C = await ev(`sgConst('${cid}').stars.map(x => x.id)`), asg = Object.fromEntries(C.map((id, i) => [id, i === 0 ? 'me1' : 'stella']));
      await ctl(`{ ph: 'assign', at: now2(), asg: ${JSON.stringify(asg)}, ord: ['me1'], full: false }`); await p.waitForTimeout(300); await ctl(`{ ph: 'light', at: now2() }`); }
    else { await ev(`sgAdminAct('assign')`); await p.waitForTimeout(300); await ev(`sgDoLight()`); }
    await p.waitForTimeout(700); await p.evaluate(() => { const s = document.querySelector('.sgstar'); if (s) s.click(); }); await p.waitForTimeout(300);
    ok(await ev(`sgModel().mine.every(k => sgLit[k])`), `${tag} 내 별 켜기`);
    await ctl(`{ at: now2() - 12500 }`); await p.waitForTimeout(400); s = await say();
    ok(s.who === AN && s.t === await line('light', T), `${tag} 별 켜는 중 아르투아 한마디`);
    // 하늘: 선이 다 이어진 뒤
    await ev(`(sgLitAll(), 1)`); await p.waitForTimeout(200); await ctl(`{ ph: 'sky', at: now2() - (sgConst('${cid}').order.length * SG_LINE + 2000) }`); await p.waitForTimeout(400); s = await say();
    ok(s.who === AN && s.t === await line('sky', T), `${tag} 하늘: 아르투아가 옮겨 그려요`);
    if (tag.includes('첫')) await p.screenshot({ path: OUT + `/sga_sky_${T}.png` });
    // 이야기: 스텔라 이야기 동안은 스텔라 · 끝난 뒤 아르투아
    const dn = await ev(`sgDoneLines(sgConst('${cid}')).length`), had = await ev(`!!(me.smap || {})['${cid}']`);
    await ctl(`{ ph: 'done', at: now2(), dn: ${dn} }`); await p.waitForTimeout(600); s = await say();
    ok(s.who === SN, `${tag} 이야기 시작은 스텔라`);
    ok(await ev(`!!me.smap && me.smap['${cid}'] === 1 && me.smapLast.c === '${cid}' && me.smapLast.nw === ${had ? 0 : 1}`), `${tag} 별 지도 조각 「${cid}」 ${had ? '(이미 있음)' : '새로'}`);
    await ctl(`{ at: now2() - ${dn} * 6000 - 800 }`); await p.waitForTimeout(400); s = await say();
    ok(s.who === AN && s.t === await line('done', T), `${tag} 이야기 끝: 아르투아`);
    // 끝: 조각 건네기 → 스텔라 대답 → 아르투아 인사
    await ctl(`{ ok: 1, ph: 'end', open: false }`); await p.waitForTimeout(500); s = await say();
    ok(s.who === AN && s.t === await line(had ? 'again' : 'gift', had ? '' : T), `${tag} 끝: ${s.t.slice(0, 34)}`);
    if (tag.includes('첫')) await p.screenshot({ path: OUT + `/sga_end_${T}.png` });
    await ev(`(sgSay.e0 -= 5500, 1)`); await p.waitForTimeout(300); s = await say(); ok(s.who === SN && s.t === await line('reply', T), `${tag} 끝: 스텔라 대답 (${T})`);
    await ev(`(sgSay.e0 -= 5000, 1)`); await p.waitForTimeout(300); s = await say(); ok(s.who === AN && s.t === await line('bye', T), `${tag} 끝: 아르투아 인사 (${T})`);
    await ev(`(sgClose(), 1)`); await p.waitForTimeout(300);
  }
  await night('lantern', true, 'A', '[서버 · 첫]');
  await night('teacup', false, 'D', '[관리자 · 첫]');
  await night('lantern', true, 'C', '[서버 · 두 번째]');
  // 별 지도 화면: 아르투아 NPC 창 → 모은 조각 / 전체 · 5 장 보상
  await ev(`(npcMenu(npcGet('artua')), 1)`); await p.waitForTimeout(300);
  ok(!!(await p.$('#npcui [data-smo]')), '아르투아 NPC 창에 「별 지도」 ' + await ev(`$('#npcui [data-smo]') ? $('#npcui [data-smo]').textContent : ''`));
  await p.click('#npcui [data-smo]'); await p.waitForTimeout(500);
  ok(await ev(`sheetOn && sub === 'smap' && document.querySelectorAll('.smc').length === sgData.length && document.querySelectorAll('.smc:not(.no)').length === 2`), '별 지도: 24 칸 중 모은 2 칸');
  ok(await ev(`!!document.querySelector('[data-smr="5"][disabled]')`), '5 장 전엔 보상 못 받아요');
  await ev(`(['pumpkin_cart', 'witch_broom', 'sleepy_owl'].forEach(k => { me.smap[k] = 1; }), render(), 1)`); await p.waitForTimeout(300);
  await p.screenshot({ path: OUT + '/sga_map.png' });
  const c0 = await ev('me.coin'); await p.click('[data-smr="5"]'); await p.waitForTimeout(300);
  ok(await ev(`me.coin === ${c0} + 150 && me.smapr['5'] === 1 && !document.querySelector('[data-smr="5"]')`), '5 장 보상 받기 (150 골드 · 별가루 병)');
  await ev(`(sgData.forEach(C => { me.smap[C.id] = 1; }), render(), 1)`); await p.waitForTimeout(200);
  const c1 = await ev('me.coin'); await p.click('[data-smr="10"]'); await p.click('[data-smr="all"]'); await p.waitForTimeout(300);
  ok(await ev(`me.coin === ${c1} + 1300 && me.smapr['10'] && me.smapr.all && document.querySelectorAll('.smc.no').length === 0`), '10 장 · 전부 보상');
  await ev(`(app.querySelector('.panel').scrollTop = 520, 1)`); await p.waitForTimeout(200); await p.screenshot({ path: OUT + '/sga_map_full.png' }); await ev(`(closeSheet(), 1)`);
  // 아르투아를 못 만난 학생: 예전 그대로 · 조각 없음
  await ev(`(me.nnpc.artua.met = 0, me.smap = {}, me.smapLast = null, syncNpcs(), 1)`);
  await ev(`(F.set(F.ref(db, 'stargaze/join'), null), F.set(F.ref(db, 'stargaze/ctl'), { open: true, id: now2(), c: 'teacup', ph: 'gather', at: now2() - 60000, gm: 180000, lm: 60000, bm: 86400000, sm: 6000, srv: 1 }), 1)`); await p.waitForTimeout(400);
  await ev(`(F.set(F.ref(db, 'stargaze/join/' + myId()), { n: me.nick, at: now2() }), sgOpen(), 1)`); await p.waitForTimeout(600);
  ok(await ev(`!sgModel().crowd.some(c => c.artua)`), '못 만난 학생: 아르투아 없음');
  let seen = new Set(); for (let k = 0; k < 6; k++){ await ctl(`{ at: now2() - ${(k + 6) * 7000 + 500} }`); await p.waitForTimeout(250); seen.add((await say()).who); }
  ok(seen.size === 1 && seen.has(SN), '못 만난 학생: 대사는 스텔라만');
  await ctl(`{ ph: 'done', at: now2(), dn: 5 }`); await p.waitForTimeout(500);
  ok(await ev(`!Object.keys(me.smap || {}).length && me.sgd === sgCtl.id`), '못 만난 학생: 별빛은 받고 조각은 없음');
  await ev(`(sgClose(), F.update(F.ref(db, 'stargaze/ctl'), { ph: 'end', open: false }), me.nnpc.artua.met = 1, 1)`);
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개 · 그림: ${OUT}/sga_*.png`); await b.close(); process.exit(fail ? 1 : 0);
})();
