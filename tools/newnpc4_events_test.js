// 새 친구 넷 (바우 · 카엘 · 아르투아 · 그레고)이 기존 NPC 이벤트 · 시스템에 다 들어갔는지 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/newnpc4_events_test.js [그림 저장 폴더]
//   뜨개(인형 · 목도리 · 좋아하는 색 · 키링) · 꽃다발 · 마음 풍선(새 풍선 넷 + 이야기) · 편지 · 쿠키 상자 · 막대과자 · 겨울잠 · 감기 · 책갈피 · 응원 · 승급 축하 · 인형 소문
//   표마다 넷 다 있는지 보고, 풍선 이야기 · 꽃다발 · 편지 · 책갈피 · 쿠키 화면을 실제로 열어서 페이지 오류가 없는지 봐요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const OUT = process.argv[2] || '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad'; fs.mkdirSync(OUT, { recursive: true });
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
const IDS = ['bau', 'kael', 'artua', 'grego'], J = JSON.stringify(IDS);
seed.players.me1.nnpc = Object.fromEntries(['dodo', 'selin', 'bone', ...IDS].map(id => [id, { met: 1, at: 1 }]));   // 새 친구를 다 만난 학생
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__T && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  const src = await p.evaluate(() => fetch('index.html').then(r => r.text()));   // 함수 안에 숨은 표(쿠키 · 막대과자 · 겨울잠 · 책갈피 · 응원)는 소스에서 찾아요
  await p.waitForFunction(() => __tw.ev("['bau','kael','artua','grego'].every(id => npcGet(id) && NL.prof[id])"), null, { timeout: 20000 }).catch(() => {});
  ok(await ev(`${J}.every(id => !!npcGet(id))`), '만난 학생에게 넷 다 보여요');
  // ---------- 표마다 넷 다 있는지 ----------
  const T = {
    '뜨개 인형 KN_DOLLS': `${J}.every(id => KN_DOLLS.some(d => d[0] === id))`,
    '뜨개 인형 가구 (world.js)': `${J}.every(id => World.FURN.items.some(f => f.id === 'kn_doll_' + id && f.dyn === id))`,
    '목도리 대사 KN_THX': `${J}.every(id => KN_THX[id] && KN_THX[id].first.length === 5 && KN_THX[id].again.length === 3)`,
    '좋아하는 목도리 색 KN_FAV · KN_FAV_SAY': `${J}.every(id => KN_COL.some(c => c[0] === KN_FAV[id]) && KN_FAV_SAY[id])`,
    '바우 목도리 자리 KN_SP[17] · 얼굴 틀 NPC_FACE[17]': `KN_SP[17] && KN_SP[17].length === 3 && NPC_FACE[17] && NPC_ROWS === 18`,
    '키링 KR_ANCH · KR_THX': `${J}.every(id => KR_ANCH[id] && [0, 5, 10, 15].every(k => KR_ANCH[id][k]) && KR_THX[id])`,
    '꽃다발 BQ_NPCS': `${J}.every(id => { const R = BQ_NPCS.find(x => x.id === id); return R && BQ_PAGE[R.like] && BQ_PAGE[R.hate] && ['like', 'hate', 'love', 'prank', 'base'].every(k => R.say[k]); })`,
    '꽃다발 그 뒤 BQ_RECALL': `${J}.every(id => BQ_RECALL[id] && BQ_RECALL[id].length === 3)`,
    '풍선 이야기 BLN_STORY': `${J}.every(id => { const D = BLN_STORY[id]; return D && D.part1.length > 20 && D.retry && D.ok && D.no && Object.keys(D.near).length >= 3 && D.wait && D.after && BLN_BY[D.ans] && NL.places[D.loc] && Object.keys(D.near).every(k => BLN_BY[k]); })`,
    '새 풍선 넷 BLN_F · BLN_MASK · BLN_TAPS · ITEM': `['relief', 'warm', 'regard', 'rest'].every(f => BLN_BY[f] && BLN_MASK[BLN_BY[f].sh] && BLN_TAPS[BLN_BY[f].sh] && ITEM['bl_' + f] && ITEM[BLN_BY[f].dye]) && new Set(BLN_F.map(f => f.sh)).size === BLN_F.length`,
    '풍선 이야기 조연 (프로필 cast)': `${J}.every(id => { const c = NL.prof[id].cast || {}, D = BLN_STORY[id]; return [...D.part1, ...D.ok].filter(x => x.cmd === 'show').every(x => c[x.who]); })`,
    '편지 LT_LETTERS · LT_NPC · LT_THANKS': `${J}.every(id => LT_LETTERS[id] && LT_LETTERS[id].length === 3 && LT_LETTERS[id].every(L => L.t && L.r.length === 3) && ltNpc(id) && ltNpc(id).deco.every(d => LT_PX[d[0]]) && LT_THANKS[id])`,
    '감기 환자 PIDS': `${J}.every(id => __cold.PIDS.includes(id))`,
    '책갈피 효과 FX': `${J}.every(id => __bm.FX[id] && __bm.FX[id].aff === id)`,
    '승급 축하 GR_HI_N': `${J}.every(id => GR_HI_N[id] && GR_HI_N[id][2] && GR_HI_N[id][3] && GR_HI_N[id][4])`,
    '인형 소문 NB_RUMOR': `${J}.every(id => NB_RUMOR[id])`,
    '도착 장면 차례 EVQ': `${J}.every(id => EVQ.includes('nn_' + id))`,
    '쿠키 뼈다귀 모양 도감': `__ck.DEX.some(d => d.id === 'butter_bone')`,
  };
  for (const [k, s] of Object.entries(T)) ok(await ev(s), k);
  const S = {   // 함수 안 표: 소스에서 「<id>: {」 또는 「'<id>'」가 그 표 안에 있는지
    '쿠키 상자 NPCS (맛 · 모양 · 힌트)': [/const NPCS = \{[\s\S]*?\n  \};/, id => new RegExp(`\\n    ${id}: \\{ f: '`)],
    '쿠키 그림 칭찬 DRAWN': [/const DRAWN = \{.*\};/, id => new RegExp(`${id}: '`)],
    '쿠키 받는 연출 REACT': [/const REACT = \{[\s\S]*?\n  \};/, id => new RegExp(`${id}: \\{ act: '`)],
    '막대과자 NP': [/const NP = \{[\s\S]*?\n  \};/, id => new RegExp(`\\n    ${id}: \\{ f: '`)],
    '겨울잠 대사 LINES': [/const LINES = \{[\s\S]*?\n  \};/, id => new RegExp(`\\n    ${id}: \\[`)],
    '감기 대사 SICK': [/const SICK = \{[\s\S]*?\n  \};/, id => new RegExp(`\\n    ${id}: '`)],
    '감기 나은 대사 THANK': [/const THANK = \{[\s\S]*?\n  \};/, id => new RegExp(`\\n    ${id}: '`)],
    '책갈피 NPCB': [/const NPCB = \[[\s\S]*?\n  \]/, id => new RegExp(`\\['${id}', '`)],
    '책갈피 그림 npcMotif': [/function npcMotif[\s\S]*?\n  \}\n/, id => new RegExp(`case '${id}':`)],
    '응원 G · order': [/const G = \{\n    blady:[\s\S]*?const order = \[.*\]/, id => new RegExp(`${id}: \\['[\\s\\S]*'${id}'`)],
  };
  for (const [k, [re, f]] of Object.entries(S)){ const m = src.match(re); ok(!!m && IDS.every(id => f(id).test(m[0])), k); }
  ok(await p.evaluate(() => fetch('world.js').then(r => r.text())).then(w => ['bone', 'lamp', 'cup', 'letter'].every(g => new RegExp(`\\b${g}: \\['`).test(w.match(/const GLYPH = \{[\s\S]*?\n\};/)[0]))), '응원 머리 위 그림 GLYPH 넷 (뼈다귀 · 등불 · 찻잔 · 편지)');
  // ---------- 그림: 새 풍선 넷 · 바우 목도리 · 키링 자리 · 뜨개 인형 ----------
  await p.waitForFunction(ids => __tw.ev(`${JSON.stringify(ids)}.every(id => knitDoll(npcGet(id), 1))`), IDS, { timeout: 15000, polling: 500 }).catch(() => {});   // 사람 친구 머리 그림이 다 올 때까지
  const pics = await p.evaluate(ids => __tw.ev(`(() => { const out = {};
    const bl = document.createElement('canvas'), S = 8, F = BLN_F.slice(-8); bl.width = F.length * 15 * S; bl.height = 18 * S; const g = bl.getContext('2d'); g.imageSmoothingEnabled = false; g.fillStyle = '#2A2040'; g.fillRect(0, 0, bl.width, bl.height);
    F.forEach((f, i) => { const c = blnImg(f.id); g.drawImage(c, i * 15 * S + (15 - c.width) * S / 2, S, c.width * S, c.height * S); }); out.bln = bl.toDataURL();
    const sh = knSprSheet(npcGet('bau'), ['red', 'white']), k = document.createElement('canvas'); k.width = 20 * 64 * 2; k.height = 64 * 2; const q = k.getContext('2d'); q.imageSmoothingEnabled = false; q.fillStyle = '#3A3050'; q.fillRect(0, 0, k.width, k.height); if (sh) q.drawImage(sh, 0, 0, k.width, k.height);
    out.scarf = sh ? k.toDataURL() : ''; const d = document.createElement('canvas'); d.width = ${JSON.stringify(ids)}.length * 64 * 3; d.height = 64 * 3; const dq = d.getContext('2d'); dq.fillStyle = '#3A3050'; dq.fillRect(0, 0, d.width, d.height);
    out.dolls = ${JSON.stringify(ids)}.map((id, i) => { const c = knitDoll(npcGet(id), 3); if (c) dq.drawImage(c, i * 192, 0); return !!c; }); out.doll = d.toDataURL(); return out; })()`), IDS);
  const png = (name, url) => fs.writeFileSync(OUT + '/' + name, Buffer.from(url.split(',')[1], 'base64'));
  png('nn4_balloons.png', pics.bln); if (pics.scarf) png('nn4_bau_scarf.png', pics.scarf); png('nn4_knit_dolls.png', pics.doll);
  ok(!!pics.scarf, '바우 목도리 시트 그려져요'); ok(pics.dolls.every(Boolean), '뜨개 인형 넷 다 그려져요 ' + JSON.stringify(pics.dolls));
  // ---------- 화면 열어 보기 ----------
  await ev(`window.__auto = setInterval(() => { if (!evOn) return; const o = document.querySelector('#evstage [data-evo]'); if (o) o.click(); else evOn.tapR && evOn.tapR(); }, 25), 1`);
  for (const id of IDS){   // 풍선 이야기: 처음 · 다시 · 맞음 · 아님 · 거의
    const e0 = errs.length;
    const r = await p.evaluate(id => __tw.ev(`(async () => { const n = npcGet('${id}'), D = BLN_STORY['${id}'], t0 = Date.now(); await blnRun(n, D, D.part1); await blnRun(n, D, D.retry);
      const sc = D.ok.slice(); sc.splice(1, 0, { cmd: 'show', who: 'bln_' + D.ans, at: D.balAt }); await blnRun(n, D, sc); await blnRun(n, D, D.no); for (const k of Object.keys(D.near)) await blnRun(n, D, D.near[k]); return Date.now() - t0; })()`), id).catch(e => 'ERR ' + e.message);
    ok(typeof r === 'number' && errs.length === e0, `${id} 풍선 이야기 끝까지 (${r} ms)`);
  }
  await ev(`(me.bq ||= {}, me.bq.pg ||= {}, me.bq.held = ${J}.map(() => ({ slots: ['daisy', 'eve', 'firefly'], base: 'white', rib: 'red', deco: [], card: '' })), 1)`);
  for (const id of IDS){
    const e0 = errs.length; ok((await ev(`bqGiftHTML(npcGet('${id}'))`)).includes('꽃다발'), `${id} 선물 창에 꽃다발 칸`);
    await p.evaluate(id => Promise.race([__tw.ev(`bqGive(npcGet('${id}'), 0)`), new Promise(r => setTimeout(r, 8000))]), id).catch(e => errs.push(e.message));
    ok(errs.length === e0 && await ev(`!!(me.bq.gift && me.bq.gift['${id}'])`), `${id} 꽃다발 받기`);
    await ev(`(document.querySelector('#blsay') && (document.querySelector('#blsay').style.display = 'none'), 1)`);
  }
  await p.waitForTimeout(800);
  for (const [i, id] of IDS.entries()){   // 편지: 그날 편지가 새 친구 편지가 되게 배정하고 열어 봐요
    const e0 = errs.length;
    await ev(`(ltAssign = { me1: ['${id}', '${id}', '${id}'] }, me.ltr = { got: {}, rep: {} }, ltOpen(${i % 3}), 1)`); await p.waitForTimeout(700);
    const tx = await ev(`document.querySelector('#ltv .tx') ? document.querySelector('#ltv .tx').textContent : ''`);
    if (process.env.DBG) console.log(id, JSON.stringify(tx).slice(0, 80), await ev(`JSON.stringify(ltLetter(uid, ${i % 3}).id)`));
    ok(errs.length === e0 && await ev(`LT_LETTERS['${id}'].some(L => L.t.replace(/\\{name\\}/g, me.nick) === ${JSON.stringify(tx)})`), `${id} 편지 열기`); await p.screenshot({ path: OUT + '/nn4_letter_' + id + '.png' }); await ev(`(ltClose(), 1)`); await p.waitForTimeout(500);
  }
  const e1 = errs.length; await ev(`(closeSheet(), __bm.W.bk = 'npc', me.bm = me.bm || {}, me.bm.met = 1, __bm.open('mark'), 1)`); await p.waitForTimeout(800); await p.screenshot({ path: OUT + '/nn4_bookmarks.png' });
  ok(errs.length === e1 && await ev(`${J}.every(id => document.querySelector('[data-bkc="' + id + '"]'))`), '책갈피 NPC 칸에 넷 다');
  await ev(`(document.querySelector('#bmv') && document.querySelector('#bmv').remove(), 1)`);
  const e2 = errs.length; await ev(`(__ck.open('dex'), 1)`); await p.waitForTimeout(800); await p.screenshot({ path: OUT + '/nn4_cookie_dex.png' }); ok(errs.length === e2, '쿠키 도감 열기 (뼈다귀 모양)');
  ok(await ev(`${J}.every(id => typeof __hib.line === 'function') && ${J}.every(id => !!npcGet(id))`), '겨울잠 대사 함수');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개 · 그림: ${OUT}/nn4_*.png`); await b.close(); process.exit(fail ? 1 : 0);
})();
