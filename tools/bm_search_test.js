// 책 맞추기 「글자 찾기」 한글 입력: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/bm_search_test.js
//   한글을 조합하는 동안(받침 붙이기) 입력칸이 다시 그려지지 않아요 · 친구가 글자를 놓아도 쓰는 중이면 미뤘다가 다 쓰고 나서 다시 그려요
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.bm = { met: 1 };
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], ctx = await b.newContext({ ...devices['iPhone 13'] }), p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  await ev(`F.set(F.ref(db, 'bm/ctl'), { open: true, id: 1, at: now2() })`);
  await ev(`(() => { const o = {}; for (let i = 0; i < 400; i++) o[i] = { u: 'me1', by: '나', at: now2() }; return F.set(F.ref(db, 'bm/got'), o); })()`); await p.waitForTimeout(600);
  await ev(`(BM.open('book'), 1)`); await p.waitForTimeout(800);
  ok(await ev(`!!$('#bmq')`), '책 맞추기 · 글자 찾기 칸');
  const words = JSON.parse(await ev(`JSON.stringify([...document.querySelectorAll('#bmtray [data-bmw]')].map(e => e.dataset.bmw))`));
  const target = words.find(w => /[가-힣]/.test(w) && ((w.charCodeAt(0) - 0xAC00) % 28) > 0);   // 첫 글자에 받침이 있는 단어
  ok(!!target, '받침 있는 단어 ' + target);
  const ch = target[0], code = ch.charCodeAt(0) - 0xAC00, noJ = String.fromCharCode(0xAC00 + code - (code % 28));
  const inp0 = await p.$('#bmq'); await inp0.focus();
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Input.imeSetComposition', { text: noJ, selectionStart: 1, selectionEnd: 1 }); await p.waitForTimeout(200);
  const same1 = await p.evaluate(el => el === document.getElementById('bmq'), inp0);
  await ev(`F.set(F.ref(db, 'bm/place/0_0'), { w: 0, u: 'fr', by: '친구', at: now2() })`); await p.waitForTimeout(400);   // 쓰는 도중 친구가 글자를 놓아요
  await cdp.send('Input.imeSetComposition', { text: ch, selectionStart: 1, selectionEnd: 1 }); await p.waitForTimeout(200);
  await cdp.send('Input.insertText', { text: ch }); await p.waitForTimeout(300);
  const same2 = await p.evaluate(el => el === document.getElementById('bmq'), inp0);
  ok(same1 && same2, '조합하는 동안 입력칸이 그대로예요 (다시 그려지지 않음)');
  ok(await ev(`$('#bmq').value`) === ch, `입력칸에 「${ch}」 (받침까지)`);
  const shown = JSON.parse(await ev(`JSON.stringify([...document.querySelectorAll('#bmtray [data-bmw]')].map(e => e.dataset.bmw))`));
  ok(shown.length > 0 && shown.every(w => w.includes(ch)) && shown.includes(target), `「${ch}」가 든 단어만 ${shown.length} 개`);
  await ev(`(document.activeElement.blur(), 1)`); await p.waitForTimeout(300);
  ok(await ev(`!!document.querySelector('#bmv [data-slot="0"].on')`), '다 쓰고 나니 친구가 놓은 글자가 책에 보여요');
  ok(await ev(`$('#bmq').value`) === ch, '다시 그려도 찾던 글자가 남아 있어요');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
