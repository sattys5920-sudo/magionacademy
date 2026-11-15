// 새 친구 넷 (바우 · 카엘 · 아르투아 · 그레고) 등록 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/newnpc4_test.js
//   만나기 전엔 안 보임 · 만난 뒤엔 시간대별 루틴 장소에 서 있음 · 프로필 · 하트 이야기 불러옴 · 바우 그림 줄
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const IDS = ['bau', 'kael', 'artua', 'grego'];
const R = { bau: { morning: 'main_hall', day: 'main_hall', evening: 'main_hall', night: 'menagerie' }, kael: { morning: 'library_stacks', day: 'library_stacks', evening: 'main_hall', night: 'main_hall' },
  artua: { morning: 'dorm_street', day: 'library_stacks', evening: 'village_square', night: 'hill_top' }, grego: { morning: 'old_windmill', day: 'old_windmill', evening: 'village_square', night: 'old_windmill' } };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  ok(await ev(`${JSON.stringify(IDS)}.every(id => !npcGet(id))`), '만나기 전엔 학생에게 안 보여요');
  ok(await ev(`${JSON.stringify(IDS)}.every(id => !NEWNPC.filter(n => NN_ARR[n]).includes(id))`), '도착 장면이 없으니 관리자 「새 친구 맞이하기」에도 아직 안 나와요');
  await ev(`(me.nnpc = me.nnpc || {}, ${JSON.stringify(IDS)}.forEach(id => { me.nnpc[id] = { met: 1, at: now2() }; }), npcSig = '', syncNpcs(), 1)`);
  await p.waitForTimeout(1500);
  ok(await ev(`${JSON.stringify(IDS)}.every(id => !!npcGet(id))`), '만난 뒤엔 보여요');
  await p.waitForFunction(() => __tw.ev("['bau','kael','artua','grego'].every(id => NL.prof[id])"), null, { timeout: 15000 }).catch(() => {});
  ok(await ev(`${JSON.stringify(IDS)}.every(id => NL.prof[id] && NL.prof[id].daily && NL.prof[id].daily.A.length >= 12)`), '프로필 넷 다 불러와요');
  for (const id of IDS) for (const band of ['morning', 'day', 'evening', 'night']){
    const at = await ev(`ROUTINE['${id}'] && ROUTINE['${id}']['${band}']`);
    ok(at === R[id][band] && await ev(`!!NL.places['${at}']`), `${id} ${band} → ${at}`);
  }
  ok(await ev(`['kael','artua','grego'].every(id => HUMAN_NPC.includes(id) && npcAv(npcGet(id)))`), '사람 셋은 아바타로 그려요');
  ok(await ev(`npcGet('bau').spr === 17`) && await p.evaluate(async () => { const i = new Image(); i.src = 'art/npcs.webp?v=' + Date.now(); await i.decode(); return i.height >= 64 * 18; }), '바우는 NPC 그림 18 번째 줄');
  const sp = await ev(`JSON.stringify(${JSON.stringify(IDS)}.map(id => [id, __nn.spot(id)]))`); console.log('  지금 자리', sp);
  ok(JSON.parse(sp).every(([, s]) => s), '넷 다 지금 서 있을 자리가 있어요');
  const evs = await p.evaluate(async ids => { const out = {}; for (const id of ids){ let n = 0; for (let k = 1; k <= 10; k++){ const r = await fetch(`data/npc/${id}/events/heart_${String(k).padStart(2, '0')}.json`); if (r.ok){ const j = await r.json(); if (j.script && j.script.length) n++; } } out[id] = n; } return out; }, IDS);
  ok(IDS.every(id => evs[id] === 10), '하트 이야기 넷 × 10 ' + JSON.stringify(evs));
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
