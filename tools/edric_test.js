// 「녹슨 검의 대장장이」 (tools/edric/story.md): sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/edric_test.js
//   관리자가 켜기 → 학생 셋이 7 일씩 (A · B · C 결말 경로) · 하루에 한 장면 (같은 날엔 다음 날이 안 열려요) · 4 · 7 일째는 밤에만
//   6 일째 편지 (믿음 2 이상이면 열림, 아니면 7 일째) · 언덕 기념물 (A가 많으면 검 · B가 많으면 종 · 같으면 둘 다) · 관리자 카드 · 페이지 오류 없음
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const SHOT = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/';
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
// 고르는 번호 (0 부터): A = 믿음 3 · 용기 4 · B = 진실 7 · C = 믿음 5 · 용기 1
const PATHS = {
  A: { picks: [0, 2, 1, 0, 2, 0, 0], letter6: true, sc: { trust: 3, truth: 0, brave: 4 } },
  B: { picks: [1, 1, 2, 1, 1, 1, 2], letter6: false, sc: { trust: 0, truth: 7, brave: 0 } },
  C: { picks: [2, 0, 0, 0, 0, 2, 1], letter6: true, sc: { trust: 5, truth: 0, brave: 1 } },
};
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s), wait = ms => p.waitForTimeout(ms);
  const base = await ev('now2()');
  // k 일 뒤 한국 시각 h 시
  const at = (k, h) => ev(`(() => { const d = new Date(${base} + ${k} * 864e5 + 9 * 3600e3), want = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), ${h}, 5) - 9 * 3600e3; srvOff += want - now2(); return todayKey(); })()`);
  const goTo = async (m, x, y) => { await ev(`new Promise(r => { if (World.where() === '${m}') return r(1); World.teleport('${m}', null, () => r(1)); })`); await wait(700); await ev(`(World.setMe(${x}, ${y}), 1)`); await wait(300); };
  const tick = async (n = 2) => { for (let i = 0; i < n; i++){ await ev('(evqGapUntil = 0, __ed.tick(), 1)'); await wait(250); } };
  const E = () => ev('JSON.stringify(me.edric || null)').then(JSON.parse);
  // 장면 끝까지: 선택지는 picks 순서대로 · shots: [[글 정규식, 파일]] 그 줄에서 사진
  async function drive(picks = [], shots = []){
    await p.waitForFunction(() => __tw.ev('!!evOn'), null, { timeout: 20000 });
    const seen = []; let guard = 0;
    while (guard++ < 600){
      const st = await ev(`(() => { if (!evOn) return edHook('busy') ? 'wait' : 'done'; if (document.querySelector('#evstage [data-evo]')) return 'choice'; return 'line:' + (document.querySelector('#evstage .evname')?.textContent || '') + '|' + (document.querySelector('#evstage .evtext')?.textContent || ''); })()`);
      if (st === 'done') break;
      if (st === 'wait'){ await wait(150); continue; }
      if (st === 'choice'){ const i = picks.shift(); await p.click(`#evstage [data-evo="${i}"]`); await wait(120); continue; }
      const sh = shots.find(([re]) => re.test(st)); if (sh){ shots.splice(shots.indexOf(sh), 1); await ev('(evOn.tapR && evOn.tapR(), 1)'); await wait(700); await p.screenshot({ path: SHOT + sh[1] }); }
      if (!seen.length || seen[seen.length - 1] !== st) seen.push(st);
      await ev('(evOn && evOn.tapR && evOn.tapR(), 1)'); await wait(40);
    }
    return seen;
  }
  const tapPanel = async a => { await ev(`(npcClose(), __ed.panel(), 1)`); await wait(150); await p.click(`#npcui [data-edp="${a}"]`); await wait(200); };
  const F = await ev('JSON.stringify(__ed.FORGE)').then(JSON.parse);
  const atForge = () => goTo(F[0], F[1] + 1, F[2] + 2);

  // 관리자가 켜기
  await ev(`GDB.set('edric/ctl', { open: true, id: 777, at: now2() })`); await wait(500);
  const results = {};
  let off = 0;
  for (const [K, P] of Object.entries(PATHS)){
    console.log(`— 학생 ${K} 경로`);
    const picks = P.picks.slice();
    await at(off, 12); await ev('(me.edric = null, me.inv.g2_pebble = 2, me.inv.j_can = 1, 1)'); await goTo('town', 40, 50); await tick(3);
    let s = await E(); ok(s && s.ev === 777 && s.done === 0 && s.d0 === await ev('todayKey()'), `${K}: 켜면 그 학생의 1 일째가 시작돼요 (d0 = 오늘)`);
    await tick(2); s = await E(); ok(s.gd === 1, `${K}: 1 일째 하루 할 일 알림`);
    // 1 일째: 대장간 찾아가기 → 등불 맡기기
    await atForge(); await tick(2); s = await E(); ok(s.g.go === 1, `${K}: 1 일째 · 대장간 찾아가기 ✔`);
    await tapPanel('lamp'); const L1 = await drive([picks[0]], K === 'A' ? [[/문 닫았다/, 'edric_d1_forge.png']] : []);
    s = await E(); ok(s.done === 1 && s.g.lamp === 1 && s.pick.d1 === P.picks[0], `${K}: 1 일째 장면 (대사 ${L1.length} 줄) · 고른 것 ${s.pick.d1 + 1}`);
    if (K === 'A') ok(L1.some(x => x.includes('에드릭|') && x.includes('....문 닫았다.')) && L1.some(x => x.includes('값은 됐어. 불 꺼지지 않게만 해.')), '대본 대사 그대로 (에드릭 · 「....문 닫았다.」)');
    await tick(2); s = await E(); ok(s.done === 1 && s.gd === 1 && !(await ev('__ed.ready(me.edric)')), `${K}: 같은 날에는 2 일째가 안 열려요`);
    // 2 일째: 재료 3 개 · 풀무
    await at(off + 1, 12); await atForge(); await tick(2); s = await E(); ok(s.gd === 2, `${K}: 다음 날 → 2 일째`);
    await tapPanel('mat'); s = await E(); ok(s.g.mat === 3 && (await ev('me.inv.g2_pebble + me.inv.j_can')) === 0, `${K}: 쇠붙이 재료 3 개 건넴 (조약돌 2 · 깡통 1)`);
    await tapPanel('bel'); for (let i = 0; i < 12 && await p.$('#npcui [data-edp="push"]'); i++){ await p.click('#npcui [data-edp="push"]'); await wait(60); }
    await drive([picks[1]]); s = await E(); ok(s.done === 2 && s.g.bel === 1, `${K}: 풀무 누르기 → 2 일째 장면`);
    // 3 일째: 광장 → 어르신
    await at(off + 2, 12); await goTo('town', 40, 50); await tick(2); await goTo('town', 42, 49); await tick(2);
    await drive([]); s = await E(); ok(s.g.play === 1 && s.done === 2, `${K}: 3 일째 · 광장에서 아이들 놀이 보기 ✔`);
    const el = await ev(`JSON.stringify(townList().find(o => o.id === 't:elder_a'))`).then(JSON.parse);
    ok(el && el.map === 'town' && el.mark, `${K}: 어르신이 광장에 ❗와 서 있어요 (${el && [el.map, el.x, el.y]})`);
    await ev(`(townTalk('t:elder_a'), 1)`); await drive([picks[2]]); s = await E(); ok(s.done === 3 && s.g.eld === 1, `${K}: 어르신 이야기 → 3 일째 끝`);
    // 4 일째: 밤에만
    await at(off + 3, 12); await goTo('campus', 22, 12); await tick(3); s = await E(); ok(s.gd === 4 && s.done === 3 && !(await ev('!!evOn')), `${K}: 4 일째 낮에 언덕 → 안 열려요 (밤에만)`);
    await at(off + 3, 22); await goTo('campus', 22, 11); await tick(2);
    await drive([picks[3]], K === 'A' ? [[/잔 세 개를/, 'edric_d4_hill.png']] : []); s = await E(); ok(s.done === 4, `${K}: 4 일째 밤 언덕 장면`);
    // 5 일째: 어른 셋 → 대장간
    await at(off + 4, 12); await atForge(); await tick(3); s = await E(); ok(s.gd === 5 && !s.g.go && !(await ev('!!evOn')), `${K}: 5 일째 · 어른 셋 이야기 전엔 대장간 장면이 안 나와요`);
    const lines = [];
    for (const id of ['merchant', 'elder_b', 'elder_a']){ await ev(`(npcClose(), townTalk('t:${id}'), 1)`); await wait(150); lines.push(await ev(`document.querySelector('#npcui .npct')?.textContent || ''`)); }
    await ev('npcClose()');
    ok(lines.join('/') === '북쪽 봉인이 풀린대. 이십 년 만에./그때 도망친 그 검사, 요즘 뒷골목에 있다며. 이번에도 도망칠 거야./쉿. 애들 듣는다.', `${K}: 마을 어른 셋 한마디 (대본 그대로)`);
    s = await E(); ok(s.g.adult === 3, `${K}: 마을 어른 셋 3 / 3`);
    await tick(2); await drive([picks[4]]); s = await E(); ok(s.done === 5, `${K}: 5 일째 대장간 장면`);
    // 6 일째: 우체국 → 편지
    await at(off + 5, 12); await goTo('town', 62, 56); await tick(3); await drive([]); s = await E(); ok(s.lt === 1 && s.g.post === 1, `${K}: 6 일째 · 부엉이 우체국에서 편지 받음`);
    const trust6 = s.sc.trust;
    await atForge(); await tapPanel('give'); const L6 = await drive([picks[5]], K === 'A' ? [[/그날 네가 물러난 건/, 'edric_d6_letter.png']] : K === 'B' ? [[/꿈쩍도/, 'edric_d6_closed.png']] : []);
    s = await E(); const opened6 = s.letter === 6, saw = L6.some(x => x.includes('올가의 편지|'));
    ok(opened6 === P.letter6 && opened6 === (trust6 >= 2) && saw === opened6, `${K}: 6 일째 편지 규칙 · 믿음 ${trust6} → ${opened6 ? '열림' : '안 열림'}`);
    // 7 일째: 밤 대장간 → 언덕
    await at(off + 6, 22); await atForge(); await tick(3);
    const L7 = await drive([picks[6]], K === 'B' ? [[/저절로 풀린다. 마지막 기회/, 'edric_d7_letter.png']] : []);
    s = await E(); ok(s.end === K && s.g.forge === 1, `${K}: 7 일째 대장간 · 결말 ${s.end} (믿음 ${s.sc.trust} · 진실 ${s.sc.truth} · 용기 ${s.sc.brave})`);
    ok(JSON.stringify(s.sc) === JSON.stringify(P.sc) || (s.sc.trust === P.sc.trust && s.sc.truth === P.sc.truth && s.sc.brave === P.sc.brave), `${K}: 점수 ${JSON.stringify(s.sc)}`);
    if (!P.letter6) ok(s.letter === 7 && L7.some(x => x.includes('그러니까 미안해하지 마.')), `${K}: 6 일째 못 연 편지가 7 일째에 열려요 (전문)`);
    else ok(!L7.some(x => x.includes('|에드릭에게.')) && L7.some(x => x.includes('언젠가 또 재가 내리면')), `${K}: 6 일째 연 편지는 7 일째 나머지만`);
    await goTo('campus', 22, 11); await tick(2);
    const shotE = { A: [[/거봐. 혼자가 아니잖아/, 'edric_endA_hill.png'], [/이건 너희 몫이다/, 'edric_endA_forge.png']], B: [[/작은 종 하나가/, 'edric_endB_bell.png']], C: [[/엽서\|대신 너는/, 'edric_endC_card.png']] }[K];
    const LE = await drive([], shotE); s = await E(); ok(s.fin && s.done === 7 && s.g.hill === 1, `${K}: 결말 장면 (${LE.length} 줄) → 끝`);
    ok(K !== 'A' || LE.some(x => x.includes('올가|거봐. 혼자가 아니잖아.')), `${K}: 회상 인물은 목소리만 (올가)`);
    // 이벤트 뒤 대장간
    await atForge(); await wait(300); await ev('__ed.props()');
    const pr = await ev(`JSON.stringify(World.propsAt('${F[0]}').map(x => x.id))`).then(JSON.parse);
    await ev('(npcClose(), __ed.panel(), 1)'); const pline = await ev(`document.querySelector('#npcui .npct')?.textContent || ''`); await ev('npcClose()');
    if (K === 'C') ok(pr.includes('edforge') && !pr.includes('edman') && /비어 있어요/.test(pline), `C: 이벤트 뒤 대장간은 비어 있어요 · 「${pline}」`);
    else ok(pr.includes('edforge') && pr.includes('edman') && pline.length > 3, `${K}: 이벤트 뒤 에드릭은 대장간에 · 「${pline}」`);
    if (K === 'A'){ await wait(600); await p.screenshot({ path: SHOT + 'edric_forge_after_A.png' }); }
    if (K === 'C'){ await wait(600); await p.screenshot({ path: SHOT + 'edric_forge_after_C.png' }); }
    results[K] = s; off += 10;
  }
  // 내 결말이 C 일 때 반 전체 기념물: 다른 학생 결말을 넣어서 세어 봐요
  const memo = async (ends) => { await ev(`(() => { Object.keys(playersList).filter(k => k.startsWith('fake')).forEach(k => delete playersList[k]); ${JSON.stringify(ends)}.forEach((e, i) => { playersList['fake' + i] = { nick: '친구' + i, edric: { ev: 777, end: e, fin: '2026-1-1' } }; }); __ed.props(); return 1; })()`);
    return { t: await ev('JSON.stringify(__ed.tally())').then(JSON.parse), k: await ev('JSON.stringify(__ed.memoKinds(__ed.tally()))').then(JSON.parse), pr: await ev(`JSON.stringify(World.propsAt('campus').map(x => x.id).filter(x => x.startsWith('edmemo')))`).then(JSON.parse) }; };
  let m = await memo(['A', 'A', 'B']); ok(m.k.join() === 'sword' && m.pr.join() === 'edmemo_sword', `A가 많으면 「다섯 홈 검」 (A ${m.t.A} · B ${m.t.B} · C ${m.t.C})`);
  m = await memo(['B', 'B', 'A']); ok(m.k.join() === 'bell' && m.pr.join() === 'edmemo_bell', `B가 많으면 「수호대의 종」 (A ${m.t.A} · B ${m.t.B})`);
  m = await memo(['A', 'B']); ok(m.k.join() === 'sword,bell' && m.pr.length === 2, `같으면 둘 다 (A ${m.t.A} · B ${m.t.B})`);
  m = await memo([]); ok(m.k.length === 0 && m.pr.length === 0, '결말 A · B가 없으면 기념물 없음 (C는 안 세요)');
  await memo(['A', 'B', 'B', 'A']); await goTo('campus', 23, 12); await wait(1200); await p.screenshot({ path: SHOT + 'edric_memorial.png' });
  ok(await ev(`World.onProp('edmemo_bell') === '「수호대의 종」 · 올가. 마리엔. 토비.'`), '종을 누르면 이름 셋');
  // 결말 기준
  ok(await ev(`[__ed.ending({ trust: 3, brave: 4, truth: 0 }), __ed.ending({ truth: 3, trust: 2, brave: 2 }), __ed.ending({ trust: 2, brave: 2, truth: 2 }), __ed.ending({ trust: 6, brave: 0, truth: 1 }), __ed.ending({ truth: 3, trust: 3, brave: 1 })].join('') === 'ABCCC'`), '결말 기준 (A · B · 낮음 C · 한쪽만 C · 동점 C)');
  // 일지
  await ev(`(jnTab = 'edric', openSheet('home', 'journal'), render(), 1)`); await wait(400);
  ok(await ev(`/녹슨 검의 대장장이/.test(document.body.innerText) && /떠난 뒷모습/.test(document.body.innerText)`), '일지 「대장간」 탭 (결말 C)');
  await ev('closeSheet()');
  // 진행 중인 날의 일지 · 할 일
  await ev(`(me.edric = { ...me.edric, done: 1, dt: '2000-1-1', gd: 2, g: { mat: 1 }, fin: null, end: null }, jnTab = 'edric', openSheet('home', 'journal'), render(), 1)`); await wait(400);
  ok(await ev(`/2 \\/ 7 일째/.test(document.body.innerText) && /쇠붙이 재료/.test(document.body.innerText) && /1 \\/ 3/.test(document.body.innerText)`), '일지에 오늘 할 일 (2 일째 · 재료 1 / 3)');
  await p.screenshot({ path: SHOT + 'edric_journal.png' }); await ev('closeSheet()');
  // 관리자 카드
  await ev(`(() => { AD.edctl = { open: true, id: 777 }; AD.players = { s1: { nick: '가람', edric: ${JSON.stringify(results.A)} }, s2: { nick: '나래', edric: ${JSON.stringify(results.B)} }, s3: { nick: '다온', edric: ${JSON.stringify(results.C)} }, s4: { nick: '라온', edric: { ev: 777, d0: todayKey(), done: 2, dt: todayKey(), gd: 3, g: { play: 1 }, sc: { trust: 1, truth: 1, brave: 0 }, pick: { d1: 0, d2: 1 } } }, s5: { nick: '마루' } }; return 1; })()`);
  const card = await ev('EDR.adminHTML()');
  ok(/켜기|끄기/.test(card) && /처음부터/.test(card) && /결말 A 「검을 든 대장장이」/.test(card) && /결말 B/.test(card) && /결말 C/.test(card) && /3 \/ 7 일째/.test(card) && /오늘 할 일 1 \/ 2/.test(card) && /믿음 3 · 진실 0 · 용기 4/.test(card) && /아직 시작 전/.test(card), '관리자 카드: 학생마다 날 · 할 일 · 점수 · 결말');
  ok(/「다섯 홈 검」 · 「수호대의 종」/.test(card), '관리자 카드: 언덕 기념물 (A 1 · B 1 → 둘 다)');
  ok(/녹슨 검의 대장장이/.test(await ev('adminEventHTML()')), '관리자 이벤트 탭에 카드가 들어가요');
  await ev(`(() => { const d = document.createElement('div'); d.id = 'adminv'; d.style.cssText = 'position:fixed;inset:0;overflow:auto;background:#fff;z-index:999;padding:8px'; d.innerHTML = EDR.adminHTML(); document.body.appendChild(d); return 1; })()`); await wait(300);
  await p.screenshot({ path: SHOT + 'edric_admin.png' });
  await p.click('#adminv [data-eda="close"]'); await wait(400); ok(await ev(`!__ed.ctl().open`), '관리자 「끄기」');
  await p.click('#adminv [data-eda="reset"]'); await wait(400); ok(await ev(`__ed.ctl().open && __ed.ctl().id !== 777`), '관리자 「처음부터」 (새 번호로 다시 켜요)');
  await ev(`document.getElementById('adminv').remove()`);
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
