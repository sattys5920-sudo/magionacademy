// 자동 이벤트 서버(functions/autohost.js) 검사: 가짜 데이터베이스 + 빨리 가는 시계로 유령 열차 · 별 보는 밤을 끝까지 돌려요
//   cp -r public/data/events/stargazing functions/sg && node tools/auto_event_test.js
let NOW = Date.UTC(2026, 10, 16, 12, 0, 0); const realNow = Date.now; Date.now = () => NOW;
global.setTimeout = (fn, ms) => { NOW += ms || 0; Promise.resolve().then(fn); return 0; };   // 기다리는 만큼 시계를 앞으로
const { runAuto } = require('../functions/autohost.js');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
function fakeDb(init = {}){
  const root = JSON.parse(JSON.stringify(init)), subs = [];
  const parts = p => p.split('/').filter(Boolean);
  const getAt = p => parts(p).reduce((o, k) => (o && typeof o === 'object' ? o[k] : undefined), root);
  const setAt = (p, v) => { const ks = parts(p); let o = root; ks.slice(0, -1).forEach(k => { if (typeof o[k] !== 'object' || o[k] === null) o[k] = {}; o = o[k]; }); if (v === null || v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = JSON.parse(JSON.stringify(v)); };
  const fire = () => subs.forEach(s => s.fn({ val: () => { const v = getAt(s.p); return v === undefined ? null : JSON.parse(JSON.stringify(v)); } }));
  const ref = p => ({
    get: async () => ({ val: () => { const v = getAt(p); return v === undefined ? null : JSON.parse(JSON.stringify(v)); } }),
    set: async v => { setAt(p, v); fire(); },
    update: async o => { Object.entries(o).forEach(([k, v]) => setAt(p + '/' + k, v)); fire(); },
    on: (ev, fn) => { const s = { p, fn }; subs.push(s); s.fn({ val: () => { const v = getAt(p); return v === undefined ? null : JSON.parse(JSON.stringify(v)); } }); return fn; },
    off: (ev, fn) => { const i = subs.findIndex(s => s.fn === fn); if (i >= 0) subs.splice(i, 1); },
  });
  return { ref, root };
}
(async () => {
  // 1 유령 열차
  let db = fakeDb({ autoreq: { gt_20261116_2000: NOW, gt_20261110_2000: NOW - 6 * 864e5 } });
  let r = await runAuto(db, 'gt_20261116_2000');
  const c = db.root.gtrain && db.root.gtrain.ctl;
  ok(/^open /.test(r) && c && c.open && c.auto && c.go - c.t0 === 300e3 && ['lake', 'field', 'grave', 'forest', 'cave'].includes(c.dest), '유령 열차 자동 도착: ' + r);
  ok(!db.root.autoreq.gt_20261110_2000, '사흘 지난 신호는 지워져요');
  r = await runAuto(db, 'gt_20261116_2200'); ok(r === 'busy', '운행 중이면 새로 부르지 않아요');
  NOW += 700e3; r = await runAuto(db, 'gt_20261116_2200'); ok(/^open /.test(r), '운행이 끝난 뒤엔 다시 와요');
  db = fakeDb({ autocfg: { gtOff: true } }); ok(await runAuto(db, 'gt_20261116_2000') === 'off' && !db.root.gtrain, '관리자가 끄면 안 와요');
  // 2 별 보는 밤: 참가자 셋 → 별 나눠 주기 → 학생은 자기 별을 켜요 → 하늘 → 이야기 → 끝
  db = fakeDb({ stargaze: { hist: { last: 'teacup', total: 3 } } });
  const t0 = NOW, phases = []; let ctl0 = null, lit = false;
  const sub = db.ref('stargaze/ctl'); sub.on('value', s => { const v = s.val(); if (!v) return; if (!phases.includes(v.ph)) phases.push(v.ph);
    if (v.ph === 'gather' && !ctl0){ ctl0 = v; db.ref('stargaze/join').set({ u1: { n: '가', at: 1 }, u2: { n: '나', at: 2 }, u3: { n: '다', at: 3 } }); }   // 모이는 동안 학생 셋이 참가
    if (v.ph === 'light' && !lit){ lit = true; const up = {}; Object.entries(v.asg || {}).forEach(([star, u]) => { if (u !== 'stella') up[star] = NOW; }); db.ref('stargaze/lit').update(up); } });   // 받은 별을 바로 켜요
  const p = runAuto(db, 'sg_20261116');
  r = await p;
  ok(ctl0 && ctl0.open && ctl0.srv === 1 && ctl0.c !== 'teacup', '별 보는 밤 자동 열기 (어제와 다른 별자리): ' + (ctl0 && ctl0.c));
  const end = db.root.stargaze.ctl;
  ok(/^done /.test(r) && end.ph === 'end' && end.open === false && end.ok === 1, '끝까지 진행: ' + r + ' · ' + Math.round((NOW - t0) / 1000) + ' 초');
  ok(['gather', 'assign', 'light', 'sky', 'done', 'end'].every(x => phases.includes(x)), '단계: ' + phases.join(' → '));
  ok(Object.values(end.asg).filter(u => u !== 'stella').length === 3 && end.ord.length === 3, '참가자 셋에게 별이 나눠졌어요');
  ok(db.root.stargaze.hist.total === 4 && db.root.stargaze.hist.c[end.c] === 1, '완성 횟수 기록');
  ok(NOW - t0 < 520e3, '함수 시간 안에 끝나요 (9 분 미만)');
  db = fakeDb({ stargaze: { ctl: { open: true, ph: 'light', id: 1 } } }); ok(await runAuto(db, 'sg_20261116') === 'busy', '이미 열려 있으면 건너뛰어요');
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); process.exit(fail ? 1 : 0);
})();
