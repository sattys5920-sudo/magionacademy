// 책 맞추기 빛나기: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/bm_glow_test.js
//   한 쪽이 다 맞으면 그 쪽 단어가 금빛으로 빛나요 · 하나라도 틀리면 안 빛나요 · 고른 글자 테두리 · 친구가 놓은 칸 표시 (스크린숏 tools/shot_bm_glow.png)
const { chromium, devices } = require('playwright'); const fs = require('fs');
const seed = eval('(' + fs.readFileSync(__dirname + '/../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
seed.players.me1.bm = { met: 1 };
const src = fs.readFileSync(__dirname + '/../public/index.html', 'utf8'), BOOK = src.match(/const BOOK = `([\s\S]*?)`;/)[1];
const PAGES = BOOK.trim().split(/\n\s*\n/).map(par => par.split('\n').map(line => line.split(/\s+/).filter(Boolean).map(tok => { const m = tok.match(/^(["“.…]*)(.*?)(["”.,!?…]*)$/); return { pre: m[1], w: m[2], post: m[3] }; })));
const ALL = [...new Set(PAGES.flat(2).map(t => t.w).filter(Boolean))], SL = PAGES.map(p => p.flat());
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const b = await chromium.launch(), errs = [], p = await (await b.newContext({ ...devices['iPhone 13'] })).newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('dialog', d => d.accept());
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.World && window.__tw, null, { timeout: 30000 }); await p.waitForTimeout(3000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const ev = s => p.evaluate(s => __tw.ev(s), s);
  const got = {}; ALL.forEach((_, i) => got[i] = { u: 'me1', by: '나', at: 1 });
  const pl = {}; SL[0].forEach((t, k) => { if (t.w) pl['0_' + k] = { w: ALL.indexOf(t.w), u: k % 2 ? 'me1' : 'fr', by: '친구', at: 1 }; });
  const wrongK = Object.keys(pl)[0], right = pl[wrongK].w;
  pl[wrongK] = { ...pl[wrongK], w: (right + 1) % ALL.length };   // 하나만 틀리게
  await ev(`F.set(F.ref(db, 'bm/ctl'), { open: true, id: 1, at: now2() })`); await ev(`F.set(F.ref(db, 'bm/got'), ${JSON.stringify(got)})`); await ev(`F.set(F.ref(db, 'bm/place'), ${JSON.stringify(pl)})`); await p.waitForTimeout(600);
  await ev(`(BM.open('book'), 1)`); await p.waitForTimeout(800);
  const glow = () => ev(`getComputedStyle(document.querySelector('#bmv .bmslot.on')).boxShadow`);
  ok(!/255, 216, 102/.test(await glow()), '하나 틀리면 안 빛나요');
  ok(await ev(`/90, 120, 200/.test(getComputedStyle(document.querySelector('#bmv .bmslot.bmfr')).boxShadow)`), '친구가 놓은 칸 표시');
  await ev(`F.set(F.ref(db, 'bm/place/${wrongK}'), ${JSON.stringify({ ...pl[wrongK], w: right })})`); await p.waitForTimeout(800);
  ok(/255, 216, 102/.test(await glow()), '다 맞으면 금빛으로 빛나요');
  ok(await ev(`document.querySelector('#bmv .pnav button.ok') !== null`), '쪽 번호 금테');
  await ev(`(document.querySelector('#bmv [data-bmpg="1"]').click(), 1)`); await p.waitForTimeout(400);
  const t = await p.$('#bmtray [data-bmw]'); const bx = await t.boundingBox(); await p.mouse.click(bx.x + bx.width / 2, bx.y + bx.height / 2); await p.waitForTimeout(400);
  ok(await ev(`getComputedStyle(document.querySelector('#bmtray .bmwd.bmsel')).outlineStyle === 'solid'`), '고른 글자 테두리');
  ok(await ev(`getComputedStyle(document.querySelector('#bmtray .bmwd.bmflap'), '::before').animationName === 'bmflapL'`), '글자 날갯짓');
  await ev(`(document.querySelector('#bmv [data-bmpg="0"]').click(), 1)`); await p.waitForTimeout(400);
  await p.screenshot({ path: __dirname + '/shot_bm_glow.png' });
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await b.close(); process.exit(fail ? 1 : 0);
})();
