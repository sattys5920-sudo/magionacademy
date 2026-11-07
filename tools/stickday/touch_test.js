// 휴대폰 화면 + 터치 흉내로 굽기 미니게임 시험: 단계 8 가지 · 완벽 순간 · 판정 가장자리(여유) · 너무 이른 터치 · 두 번 들어오기 · 두 번째 손가락 · 진짜 터치(touchscreen.tap)
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const { mkSeed } = require('/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/stk/common.js'); const fs = require('fs');
const OUT = '/home/user/magionacademy/tools/stickday/shots'; const res = []; const ok = (c, m) => { res.push([!!c, m]); console.log(c ? '  ok ' : '  ✗  ', m); };
const LIB = () => {
  const W_ = () => document.getElementById('stkmgw');
  const at = (abs) => new Promise(r => { const f = () => { const d = abs - performance.now(); if (d > 6) setTimeout(f, Math.max(0, d - 6)); else { while (performance.now() < abs); r(); } }; f(); });
  const ev = (type, x, y, id = 7) => { const w = W_(), c = w.querySelector('canvas').getBoundingClientRect(); w.dispatchEvent(new PointerEvent(type, { pointerId: id, pointerType: 'touch', isPrimary: id === 7, clientX: c.left + x / 160 * c.width, clientY: c.top + y / 112 * c.height, bubbles: true, cancelable: true })); };
  const tapAt = async (abs, x = 80, y = 60, id = 7) => { await at(abs); ev('pointerdown', x, y, id); await new Promise(r => setTimeout(r, 40)); ev('pointerup', x, y, id); };
  window.__tl = { at, ev, tapAt, W_ };
};
async function waitStep(p, key){ for (let i = 0; i < 200; i++){ const g = await p.evaluate(() => window.__stk.mg()); if (g && g.key === key && !g.done) return g; await p.waitForTimeout(50); } throw new Error('no step ' + key + ' ' + JSON.stringify(await p.evaluate(() => [window.__stk.mg(), window.__stk.W.step, window.__stk.W.cur && window.__stk.W.cur.plan]))); }
async function waitDone(p, i){ for (let i2 = 0; i2 < 300; i2++){ const g = await p.evaluate(() => window.__stk.mg()); if (!g || g.i !== i || g.done) return g; await p.waitForTimeout(50); } }
// 단계마다 몰기 (mode: 'perfect' | 'edge' ...)
async function play(p, key, i, opts = {}){
  const g = await waitStep(p, key); const shot = opts.shot ? OUT + '/step_' + key + '.png' : null;
  const r = await p.evaluate(async ([key, opts]) => { const S = window.__stk, T = window.__tl, G0 = S.mg(), t0 = G0.t0, out = { scores: [] }; await T.at(t0 + 60);
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    if (key === 'knead'){ let n = 0; while (true){ const g = S.mg(); if (!g || g.done || g.i !== G0.i) break; const h = g.hint; if (!h) break;
        let off = 0; if (opts.edge){ off = [100, -100, 200, 0, 0, 0][n] || 0; }
        if (opts.early && n === 0){ await T.tapAt(t0 + h.t - 450); out.earlyScores = S.mg().scores.length; }
        if (opts.dbl && n === 1){ await T.tapAt(t0 + h.t); await sleep(20); T.ev('pointerdown', 80, 60); T.ev('pointerup', 80, 60); out.afterDbl = S.mg().scores.length; n++; await sleep(200); continue; }
        await T.tapAt(t0 + h.t + off); n++; await sleep(260); } }
    if (key === 'oven'){ const h = S.mg().hint; if (opts.early){ await T.tapAt(t0 + h.tAt(10)); out.earlyScores = S.mg().scores.length; }
      const v = opts.v || 66; if (!opts.realTouch) await T.tapAt(t0 + h.tAt(v)); else { await T.at(t0 + h.tAt(v) - 40); out.ready = true; return out; } }
    if (key === 'stretch'){ for (let n = 0; n < 3; n++){ let g = S.mg(); while (g.hint.wait && performance.now() < t0 + g.hint.wait) { await sleep(30); g = S.mg(); } await sleep(80); g = S.mg(); const h = g.hint, L = opts.edge && n === 0 ? h.zone[1] + 2 : opts.edge && n === 1 ? h.zone[0] - 8 : h.len, d = (-44 + Math.sqrt(44 * 44 + 88 * L)) / 44 * 1000;
        const st = performance.now() + 30; await T.at(st); T.ev('pointerdown', 80, 60); if (opts.multi && n === 0){ T.ev('pointerdown', 40, 60, 9); T.ev('pointerup', 40, 60, 9); } await T.at(st + d); T.ev('pointerup', 80, 60); await sleep(100); } }
    if (key === 'dip'){ for (let n = 0; n < 2; n++){ let g = S.mg(); while (g.hint.wait && performance.now() < t0 + g.hint.wait){ await sleep(30); g = S.mg(); } await sleep(80); const st = performance.now() + 30; await T.at(st); T.ev('pointerdown', 80, 60); await T.at(st + g.hint.ms + (opts.edge && n === 0 ? 3 / 26 * 1000 : 0)); T.ev('pointerup', 80, 60); await sleep(100); } }
    if (key === 'cut'){ while (true){ const g = S.mg(); if (!g || g.done || g.i !== G0.i) break; const h = g.hint; if (!h) break; const now = performance.now() - t0 + 120;
        let best = 1e12; h.marks.forEach(m => { const u1 = (m - 20) / 240, u2 = 1 - u1; for (let k = Math.floor(now / h.P); k < Math.floor(now / h.P) + 2; k++) [u1, u2].forEach(u => { const tt = (k + u) * h.P; if (tt > now && tt < best) best = tt; }); });
        await T.tapAt(t0 + best + (opts.edge ? 30 : 0)); await sleep(150); } }
    if (key === 'drizzle'){ const pts = S.mg().hint.pts; await T.at(t0 + 200); T.ev('pointerdown', pts[0][0], pts[0][1]); for (const [x, y] of pts){ await sleep(14); T.ev('pointermove', x, y + (opts.edge ? 6 : 0)); } T.ev('pointerup', pts[pts.length - 1][0], pts[pts.length - 1][1]); }
    if (key === 'sprinkle'){ let sn = 0; while (true){ const g = S.mg(); if (!g || g.done || g.i !== G0.i) break; const h = g.hint; if (!h) break; await T.tapAt(t0 + h.t + (opts.edge ? (sn++ ? 200 : 120) : 0)); await sleep(120); } }
    if (key === 'cool' && !opts.realTouch){ for (let n = 0; n < 40; n++){ const g = S.mg(); if (!g || g.done) break; T.ev('pointerdown', 80, 60); T.ev('pointerup', 80, 60); await sleep(110); } }
    if (key === 'cool' && opts.realTouch){ await T.at(t0 + 50); out.ready = true; return out; }
    out.scores = S.mg() ? S.mg().scores : null; return out; }, [key, opts]);
  if (shot && !r.ready) {}
  if (r.ready && key === 'oven'){ const box = await (await p.$('#stkmgw')).boundingBox(); await p.touchscreen.tap(box.x + box.width / 2, box.y + box.height / 2); await p.waitForTimeout(100); r.scores = (await p.evaluate(() => window.__stk.mg().scores)); }
  if (r.ready && key === 'cool'){ const box = await (await p.$('#stkmgw')).boundingBox(); for (let n = 0; n < 40; n++){ const g = await p.evaluate(() => window.__stk.mg()); if (!g || g.done) break; await p.touchscreen.tap(box.x + 60 + (n % 5) * 30, box.y + box.height / 2); await p.waitForTimeout(90); } r.scores = (await p.evaluate(() => window.__stk.mg() && window.__stk.mg().scores)); }
  await waitDone(p, i); return r;
}
async function bake(p, plan, opts){
  await p.evaluate(pl => { window.__stkPlan = pl; window.__stk.openWin('bake'); }, plan); await p.waitForTimeout(500);
  await p.click('[data-stkc="2"]'); await p.waitForTimeout(150); await p.click('[data-stkx="start"]');
  const t0 = Date.now(), out = [];
  for (let i = 0; i < plan.length; i++){ const o = (opts[plan[i]] || {}); if (o.shot){ await waitStep(p, plan[i]); await p.waitForTimeout(1500); await p.screenshot({ path: OUT + '/step_' + plan[i] + '.png' }); }
    out.push([plan[i], await play(p, plan[i], i, o)]); }
  for (let k = 0; k < 40; k++){ if (await p.evaluate(() => window.__stk.W.step === window.__stk.W.cur.plan.length)) break; await p.waitForTimeout(100); }
  const cur = await p.evaluate(() => window.__stk.W.cur); const sec = (Date.now() - t0) / 1000;
  await p.evaluate(() => { window.__stk.W.step = -1; window.__stk.W.cur = null; document.querySelector('[data-stkx="close"]')?.click(); }); await p.waitForTimeout(400);
  return { out, cur, sec };
}
(async () => {
  const seed = mkSeed(); const me = seed.players.me1; me.stk = { ev: '2026-11-11', hi: 1, gv: 1, npc: {}, rw: {} }; me.inv = { ...me.inv, g_wheat: 40, milk: 20, honey: 20, g2_rasp: 20 };
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const ctx = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; window.__stkForce = true; }, seed); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => World.teleport('candy', [12, 8])); await p.waitForTimeout(2500); await p.evaluate(LIB);
  // 1 완벽하게: 모든 단계 (화면도 찍어요)
  let r = await bake(p, ['knead', 'cut', 'oven', 'dip'], {});
  console.log('A', JSON.stringify(r.out.map(([k, o]) => [k, o.scores])), r.cur.res, 'stars', r.cur.s, r.sec + 's');
  ok(r.cur.res.every(x => x === '완벽') && r.cur.s === 3, '완벽 순간 터치 → 네 단계 모두 완벽 · 별 3 (반죽 치대기 · 자르기 · 굽기 · 초콜릿)'); ok(r.sec >= 20 && r.sec <= 40, `한 판 시간 ${r.sec} 초`);
  r = await bake(p, ['stretch', 'oven', 'drizzle', 'sprinkle'], {});
  console.log('B', JSON.stringify(r.out.map(([k, o]) => [k, o.scores])), r.cur.res, 'stars', r.cur.s, r.sec + 's');
  ok(r.cur.res.every(x => x === '완벽') && r.cur.s === 3, '완벽 순간 터치 → 반죽 늘이기 · 굽기 · 줄무늬 · 뿌리개 모두 완벽'); ok(r.sec >= 20 && r.sec <= 40, `한 판 시간 ${r.sec} 초`);
  // 2 진짜 터치(touchscreen.tap): 굽기 · 식히기
  r = await bake(p, ['knead', 'oven', 'dip', 'cool'], { oven: { realTouch: 1, v: 66 }, cool: { realTouch: 1 } });
  console.log('C', JSON.stringify(r.out.map(([k, o]) => [k, o.scores])), r.cur.res, 'stars', r.cur.s, r.sec + 's');
  ok(r.out[1][1].scores && r.out[1][1].scores.length === 1 && r.out[1][1].scores[0] >= 1, `진짜 터치로 굽기 판정 들어감 (점수 ${r.out[1][1].scores})`); ok(r.cur.res[3] !== '아쉬워', `진짜 터치 연타로 식히기 (${r.cur.res[3]})`);
  // 3 가장자리 · 이른 터치 · 두 번 · 두 번째 손가락
  r = await bake(p, ['knead', 'oven', 'dip', 'sprinkle'], { knead: { edge: 1, early: 1 }, oven: { v: 59, early: 1 }, dip: { edge: 1 }, sprinkle: { edge: 1 } });
  const kn = r.out[0][1], ov = r.out[1][1], dp = r.out[2][1], sp = r.out[3][1]; console.log('D', JSON.stringify(r.out.map(([k, o]) => [k, o])));
  ok(kn.earlyScores === 0, '박자보다 한참 이른 터치 → 「아직이에요」 · 판정 없음 · 그다음 박자는 그대로');
  ok(kn.scores[0] === 2 && kn.scores[1] === 2, '박자 ±100 ms (보이는 칸 밖, 여유 안) → 완벽'); ok(kn.scores[2] === 1, '박자 +200 ms → 좋아');
  ok(ov.earlyScores === 0 && ov.scores[0] === 2, '굽기: 너무 이른 터치는 「아직이에요」, 바늘 59 (초록 칸 60 바로 앞, 여유 안) → 완벽');
  ok(dp.scores[0] === 2, '초콜릿: 선보다 3 칸 깊게 → 여유 안 완벽'); ok(sp.scores[0] === 2 && sp.scores.slice(1).every(s => s === 1), `뿌리개: 120 ms 늦게(약 4 칸) → 여유 안 완벽, 200 ms 늦게(약 6 칸) → 좋아 (${sp.scores})`);
  r = await bake(p, ['knead', 'oven', 'dip', 'cool'], { knead: { dbl: 1 } });
  ok(r.out[0][1].afterDbl === 2, `40 ms 안에 두 번 들어온 터치 → 한 번만 (판정 ${r.out[0][1].afterDbl} 개)`);
  r = await bake(p, ['stretch', 'oven', 'dip', 'cool'], { stretch: { multi: 1, edge: 1 } });
  ok(r.out[0][1].scores.length === 3, `늘이는 중 두 번째 손가락 → 무시 (판정 ${r.out[0][1].scores.length} 개)`); ok(r.out[0][1].scores[0] === 2 && r.out[0][1].scores[1] === 1, `늘이기 가장자리: 칸 끝 +2 → 완벽, 칸 앞 −8 → 좋아 (${r.out[0][1].scores})`);
  // 손가락이 판 밖으로 미끄러져도 (setPointerCapture) 놓을 때 판정
  r = await bake(p, ['stretch', 'oven', 'dip', 'cool'], {});
  ok(r.cur.res[0] === '완벽', '늘이기 완벽');
  // 4 화면 찍기 (단계마다)
  await bake(p, ['knead', 'cut', 'oven', 'dip'], { knead: { shot: 1 }, cut: { shot: 1 }, oven: { shot: 1 }, dip: { shot: 1 } });
  await bake(p, ['stretch', 'oven', 'drizzle', 'sprinkle'], { stretch: { shot: 1 }, drizzle: { shot: 1 }, sprinkle: { shot: 1 } });
  await bake(p, ['knead', 'oven', 'dip', 'cool'], { cool: { shot: 1 } });
  ok(errs.length === 0, '페이지 오류 없음 ' + JSON.stringify(errs));
  fs.writeFileSync(__dirname + '/touch_res.json', JSON.stringify(res)); console.log(`${res.filter(x => x[0]).length} / ${res.length} 통과`); await br.close();
})();
