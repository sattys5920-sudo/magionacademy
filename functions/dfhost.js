// 이벤트 계산 본체 (public/index.html 의 관리자 기기용 dfHost 와 같은 일을 서버에서 해요)
const TD = require('./td.js');

const TICK = 100, HANDOFF = 450e3, HARD = 525e3, OVER_CLOSE = 30 * 60e3;
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function runHost(db, R){
  const ref = p => db.ref('defense/' + p), inst = Math.random().toString(36).slice(2), t0 = Date.now();
  const lk = (await ref('lock').get()).val();
  if (lk && lk.n === R.n) return;   // 같은 신호가 두 번 온 경우
  const sv = (await ref('host').get()).val();
  const H = { S: null, id: R.n, intro: 0, startAt: 0, paused: false, admN: 0, seen: {}, pub: 9, hb: 9, ph: '', w: -1, overAt: 0 };
  if (R.fresh || !sv || !sv.S){ H.S = TD.newState([], { auto: 0 }); H.S.phase = 'ready'; ref('res').set(null); }
  else { H.S = JSON.parse(sv.S); H.S.q = H.S.q || []; H.S.mons = H.S.mons || []; H.S.fx = H.S.fx || []; H.id = sv.id; H.intro = sv.intro || 0; H.paused = !!sv.paused; H.admN = sv.admN || 0; H.startAt = sv.startAt || 0; }
  await ref('lock').set({ inst, n: R.n, at: Date.now() });
  let alive = true, pick = {}, last = Date.now(), handed = false, closing = false, saveT = 0;
  const offs = [];
  const on = (p, fn) => { const r = ref(p), h = r.on('value', s => fn(s.val())); offs.push(() => r.off('value', h)); };
  on('lock', v => { if (v && v.inst !== inst) alive = false; });
  on('pick', v => { pick = v || {}; });
  on('cmd', v => { v = v || {}; Object.entries(v).forEach(([u, c]) => {
    if (!c || H.seen[u] === c.n) return; const first = !(u in H.seen); H.seen[u] = c.n;
    if (first && Date.now() - c.n > 5000) return;   // 켜기 전에 눌린 오래된 명령은 버려요
    const p = H.S.players[u]; if (!p) return;
    if (c.a !== undefined) p.auto = c.a ? 1 : 0;
    if (c.r !== undefined) TD.setReady(H.S, u, c.r);
    if (c.i !== undefined && !H.paused) TD.cast(H.S, u, c.i);
    if (c.u && (c.u[0] === 0 || c.u[0] === 1) && ['pow', 'rng', 'cd'].includes(c.u[1])) TD.upgrade(H.S, u, c.u[0], c.u[1]); }); });
  on('adm', v => { if (!v || !v.n || v.n <= H.admN) return; H.admN = v.n; const S = H.S;
    if (v.a === 'start'){ H.intro = Date.now(); H.startAt = Date.now() + 26000; H.hb = 9; }
    else if (v.a === 'force') TD.startWave(S);
    else if (v.a === 'pause'){ H.paused = !H.paused; H.hb = 9; }
    else if (v.a === 'reset'){ H.S = TD.newState([], { auto: 0 }); H.S.phase = 'ready'; H.ph = ''; H.intro = 0; H.startAt = 0; H.id = Date.now(); H.hb = 9; ref('res').set(null); }
    else if (v.a === 'close') closing = true; });
  const save = () => ref('host').set({ id: H.id, intro: H.intro, paused: H.paused ? 1 : 0, admN: H.admN, startAt: H.startAt, at: Date.now(), S: JSON.stringify(H.S) });
  await save();
  while (alive && !closing && Date.now() - t0 < HARD){
    await sleep(TICK);
    const now = Date.now(), dt = Math.min(.5, (now - last) / 1000), S = H.S; last = now;
    if (S.phase === 'ready' || S.phase === 'rest'){
      Object.entries(pick).forEach(([u, p]) => { const q = S.players[u]; if (!q || q.zone !== p.z || q.slot !== p.s || q.job !== p.job) TD.seat(S, u, p.z, p.s, p.job); });
      Object.keys(S.players).forEach(u => { if (!pick[u]) TD.unseat(S, u); }); }
    if (H.startAt && now >= H.startAt) H.startAt = 0;
    if (!H.paused) TD.step(S, dt);
    H.pub += dt; if (H.pub >= .25){ H.pub = 0; ref('st').set(TD.snap(S)); }
    H.hb += dt; if (H.hb >= 2 || S.phase !== H.ph || S.wave !== H.w){ const ch = S.phase !== H.ph || S.wave !== H.w; H.hb = 0; H.ph = S.phase; H.w = S.wave;
      ref('ctl').set({ open: true, srv: 1, id: H.id, intro: H.intro || 0, cut: H.startAt ? 1 : 0, ph: S.phase, w: S.wave, win: S.win ? 1 : 0, hb: now, pause: H.paused ? 1 : 0 });
      ref('lock').set({ inst, n: R.n, at: now });
      if (ch && S.phase === 'over') ref('res').set({ id: H.id, eggs: S.eggs.map(Math.round), win: S.win ? 1 : 0, at: now }); }
    saveT += dt; if (saveT >= 1){ saveT = 0; save(); }
    if (S.phase === 'over'){ if (!H.overAt) H.overAt = now; if (now - H.overAt > OVER_CLOSE) closing = true; } else H.overAt = 0;
    if (!handed && now - t0 > HANDOFF){ handed = true; await save(); await ref('run').set({ n: Date.now(), resume: 1 }); }   // 다음 실행이 이어받아요
  }
  offs.forEach(f => f());
  if (closing){ await Promise.all(['ctl', 'st', 'pick', 'cmd', 'host', 'lock', 'adm', 'run'].map(p => ref(p).set(p === 'ctl' ? { open: false } : null))); }
}
module.exports = { runHost };
