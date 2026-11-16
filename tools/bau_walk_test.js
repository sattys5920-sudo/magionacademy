// 바우 산책 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/bau_walk_test.js [그림 저장 폴더]
//   바우 NPC 창의 「산책」 → 짧은 장면 → 채집물을 물어 와요 (하루 한 번) · 잃어버린 물건은 그 친구에게 돌려주면 호감 ↑ · 하트 단계마다 대사 · 바우를 못 만난 학생은 단추 없음
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
  await p.waitForFunction(() => __tw.ev("!!npcGet('bau') && !!NL.prof.bau"), null, { timeout: 20000 }).catch(() => {});
  // 대사 표: 단계마다 다 있고, 채우면 빈칸이 안 남아요
  ok(await ev(`['A','B','C','D'].every(T => ['start','sniff','fun','find','end'].every(k => __bw.L[T][k].length >= 2 && __bw.L[T][k].every(t => !/[{}]/.test(fillVars(t, 'bau')) && !/\\?!|!!/.test(t))))`), '하트 단계 A ~ D 대사 다 있음 · 빈칸 없음');
  ok(await ev(`Object.entries(__bw.LOST).every(([id, x]) => NPC_DEF.some(n => n.id === id) && x.n && x.thx && !/\\?!|!!/.test(x.thx))`), '잃어버린 물건 표 (친구마다 돌려받는 말)');
  // 1 산책 단추
  await ev(`(me.bwalk = null, npcMenu(npcGet('bau')), 1)`); await p.waitForTimeout(400);
  ok(!!(await p.$('#npcui [data-bw="walk"].go')), '바우 NPC 창에 「산책」');
  await p.screenshot({ path: OUT + '/bw_menu.png' });
  // 2 산책 → 흔한 채집물
  const a0 = await ev(`npcSt('bau').a || 0`), inv0 = await ev(`JSON.stringify(me.inv)`);
  await ev(`(__bw.force('common'), 1)`); await p.click('#npcui [data-bw="walk"]');
  await p.waitForTimeout(5200); await p.screenshot({ path: OUT + '/bw_walk_mid.png' });
  ok(await ev(`bwOn && World.cutBusy()`), '산책 장면이 돌아가요');
  await p.waitForFunction(() => __tw.ev('!bwOn'), null, { timeout: 60000 }).catch(() => {});
  const r1 = await ev(`(() => { const s = me.bwalk, k = s.last, i0 = ${inv0}; return { day: s.day === todayKey(), n: s.n, k, grade: (FORAGE.find(x => x.id === k) || {}).grade, gain: (me.inv[k] || 0) - (i0[k] || 0) }; })()`);
  ok(r1.day && r1.n === 1 && r1.grade === 1 && r1.gain === 1, '흔한 채집물 하나 ' + JSON.stringify(r1));
  ok(await ev(`(npcSt('bau').a || 0) > ${a0}`), '바우 호감 조금 ↑');
  ok(await ev(`$('#npcui').classList.contains('on') && !!$('#npcui [data-bw="walk"]') && !$('#npcui [data-bw="walk"].go') && /오늘 함/.test($('#npcui [data-bw="walk"]').textContent)`), '끝나면 바우 창이 다시 · 「산책 (오늘 함)」');
  await p.screenshot({ path: OUT + '/bw_after.png' });
  // 3 하루 한 번
  await p.click('#npcui [data-bw="walk"]'); await p.waitForTimeout(500);
  ok(await ev(`!bwOn && !World.cutBusy() && me.bwalk.n === 1`), '오늘 두 번째는 장면 없이 말만');
  // 4 드문 것 (D 단계: 건너뛰기 단추로)
  await ev(`(npcSt('bau').a = 950, me.bwalk.day = '', __bw.force('rare'), npcClose(), npcMenu(npcGet('bau')), 1)`); await p.waitForTimeout(300);
  await p.click('#npcui [data-bw="walk"]'); await p.waitForTimeout(2500); await p.screenshot({ path: OUT + '/bw_walk_D.png' });
  const sayD = await ev(`[...document.querySelectorAll('.say')].map(d => d.textContent).join(' / ')`);
  const sk = await p.$('.mqskip'); if (sk) await sk.click();
  await p.waitForFunction(() => __tw.ev('!bwOn'), null, { timeout: 30000 }).catch(() => {});
  ok(await ev(`[2, 3].includes((FORAGE.find(x => x.id === me.bwalk.last) || {}).grade) && me.bwalk.n === 2`), '드문 채집물 (2 ~ 3 등급) · 건너뛰기 ' + await ev('me.bwalk.last'));
  ok(await ev(`__bw.L.D.start.map(t => fillVars(t, 'bau')).some(t => ${JSON.stringify(sayD)}.includes(t))`), 'D 단계 첫 말 ' + sayD.slice(0, 60));
  // 5 잃어버린 물건 → 돌려주기
  await ev(`(me.bwalk.day = '', __bw.force('lost'), npcClose(), npcMenu(npcGet('bau')), 1)`); await p.waitForTimeout(300);
  await p.click('#npcui [data-bw="walk"]'); await p.waitForTimeout(1500); const sk2 = await p.$('.mqskip'); if (sk2) await sk2.click();
  await p.waitForFunction(() => __tw.ev('!bwOn'), null, { timeout: 30000 }).catch(() => {});
  const lost = await ev(`JSON.stringify(me.bwalk.lost || null)`); const L = JSON.parse(lost);
  ok(!!L && !!(await ev(`!!npcGet(${JSON.stringify(L && L.id)})`)), '잃어버린 물건 찾음 ' + lost);
  if (L){
    await ev(`(npcClose(), npcMenu(npcGet('${L.id}')), 1)`); await p.waitForTimeout(400);
    ok(!!(await p.$('#npcui [data-bw="ret"]')), `${L.id} NPC 창에 「돌려주기」`); await p.screenshot({ path: OUT + '/bw_return_btn.png' });
    const b0 = await ev(`npcSt('${L.id}').a || 0`); await p.click('#npcui [data-bw="ret"]'); await p.waitForTimeout(500);
    ok(await ev(`!me.bwalk.lost && me.bwalk.ret === 1 && (npcSt('${L.id}').a || 0) >= ${b0} + 40`), '돌려주면 호감 ↑ · 물건 정리');
    ok(await ev(`$('#npcui .npct').textContent.startsWith(fillVars(__bw.LOST['${L.id}'].thx, '${L.id}'))`), '고맙다는 말 ' + (await ev(`$('#npcui .npct').textContent`)).slice(0, 50));
    await p.screenshot({ path: OUT + '/bw_return_thx.png' });
  }
  // 6 못 만난 학생: 단추 없음
  await ev(`(npcClose(), me.nnpc.bau.met = 0, 1)`);
  ok(await ev(`!npcGet('bau') && BWALK.btn(NPC_DEF.find(n => n.id === 'bau')) === ''`), '바우를 못 만난 학생은 산책 없음');
  await ev(`(me.nnpc.bau.met = 1, 1)`);
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개 · 그림: ${OUT}/bw_*.png`); await b.close(); process.exit(fail ? 1 : 0);
})();
