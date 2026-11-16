// 자동 이벤트 서버: 관리자 화면을 켜 두지 않아도 정해진 시각에 「유령 열차」가 오고 「별 보는 밤」이 열려서 끝까지 진행돼요.
//   학생 화면이 정해진 시각에 autoreq/<키> 에 한 번만 쓸 수 있는 신호를 남기면 (index.js 의 autorun) 이 파일이 받아서 처리해요.
//   키: gt_<YYYYMMDD>_<HHMM> 유령 열차 · sg_<YYYYMMDD> 별 보는 밤
//   별 보는 밤 진행은 public/index.html 의 sgAdminTick 과 같은 규칙이에요 (ctl.srv = 1 이면 관리자 화면은 진행을 손대지 않아요)
const fs = require('fs'), path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const GT_BOARD = 300e3, GT_RUN = 8e3 * 2 + 300e3 + 20e3, GT_DEST = ['lake', 'field', 'grave', 'forest', 'cave'];
const SG_LINE = 600, SG_STORY = 6000, SG_ASSIGN = 10000, SG_CFG = { buffH: 24, lightS: 60, gatherS: 180 }, HARD = 520e3;
const SGDIR = path.join(__dirname, 'sg');   // 배포 직전에 public/data/events/stargazing 을 복사해 와요 (firebase.json predeploy)
const load = f => JSON.parse(fs.readFileSync(path.join(SGDIR, f), 'utf8'));

async function openTrain(db){
  const c = (await db.ref('gtrain/ctl').get()).val();
  if (c && c.open && c.id && Date.now() < (c.go || c.t0 + GT_BOARD) + GT_RUN) return 'busy';   // 열차가 이미 운행 중이면 그대로 둬요
  const t = Date.now(), dest = GT_DEST[Math.floor(Math.random() * GT_DEST.length)];
  await db.ref('gtrain/ctl').set({ open: true, id: t, dest, t0: t, go: t + GT_BOARD, auto: 1 });
  return 'open ' + dest;
}

function hours(ms){ const h = ms / 3600e3; return h >= 1 ? `${Math.round(h * 10) / 10} 시간` : `${Math.round(ms / 6e4)} 분`; }   // index.html 의 sgHours 와 같아요

async function runStargaze(db){
  const ref = p => db.ref('stargaze/' + p);
  const cur = (await ref('ctl').get()).val(); if (cur && cur.open) return 'busy';
  const data = load('constellations.json').constellations, hist = (await ref('hist').get()).val() || {}, cfg = { ...SG_CFG, ...((await ref('cfg').get()).val() || {}) };
  const cnt = hist.c || {}, cand = data.filter(c => c.id !== hist.last), low = Math.min(...cand.map(c => cnt[c.id] || 0));
  const pool = cand.filter(c => (cnt[c.id] || 0) === low), C = pool[Math.floor(Math.random() * pool.length)] || data[0];   // 덜 해 본 별자리부터 무작위로 (바로 전 별자리는 빼고)
  let D = {}; try { D = load(`dialogue/${C.id}.json`); } catch(e){}
  const bm = cfg.buffH * 3600e3, b = C.buff, rep = t => t.replace('{buff}', b.name).replace('{desc}', b.desc).replace('{hours}', hours(bm));
  const doneN = [...(D.done || []), ...(D.story || []), ...(D.buff || []).map(rep)].length;
  await ref('join').set(null); await ref('lit').set(null); await ref('hist').update({ last: C.id });
  const id = Date.now();
  let ctl = { open: true, id, c: C.id, ph: 'gather', at: Date.now(), gm: cfg.gatherS * 1000, lm: cfg.lightS * 1000, bm, sm: SG_STORY, srv: 1 };
  await ref('ctl').set(ctl);
  let join = {}, lit = {}; const offs = [];
  const on = (p, fn) => { const r = ref(p), h = r.on('value', s => fn(s.val())); offs.push(() => r.off('value', h)); };
  on('join', v => { join = v || {}; }); on('lit', v => { lit = v || {}; }); on('ctl', v => { ctl = v || {}; });
  const upd = o => ref('ctl').update(o), t0 = Date.now();
  try {
    while (Date.now() - t0 < HARD){
      await sleep(500);
      if (!ctl || !ctl.open || ctl.id !== id) return 'stopped';   // 관리자가 끝냈거나 새로 열었어요
      const el = Date.now() - ctl.at, n = C.order.length, asg = ctl.asg || {};
      if (ctl.ph === 'gather' && el >= (ctl.gm || 18e4)){
        const joins = Object.entries(join).sort((a, b) => (a[1].at || 0) - (b[1].at || 0)).map(([u]) => u).slice(0, 12), ids = C.stars.map(s => s.id), r = Math.floor(Math.random() * 4) * 3, sr = [...ids.slice(r), ...ids.slice(0, r)], A = {};
        sr.forEach((s, i) => { A[s] = joins[i] || 'stella'; });
        await ref('lit').set(null); await upd({ ph: 'assign', at: Date.now(), asg: A, ord: joins, full: joins.length >= 12 });
      } else if (ctl.ph === 'assign' && el >= SG_ASSIGN){ await ref('lit').set(null); await upd({ ph: 'light', at: Date.now() }); }
      else if (ctl.ph === 'light'){
        const up = {}, st = Object.keys(asg).filter(x => asg[x] === 'stella');
        C.stars.forEach(s => { if (lit[s.id]) return; if (asg[s.id] === 'stella'){ if (el >= 3000 + st.indexOf(s.id) * 2500) up[s.id] = Date.now(); } else if (el >= (ctl.lm || 6e4)) up[s.id] = Date.now(); });
        if (Object.keys(up).length){ await ref('lit').update(up); Object.assign(lit, up); }
        if (C.stars.every(s => lit[s.id]) && Date.now() - Math.max(...Object.values(lit)) >= 1800) await upd({ ph: 'sky', at: Date.now() });
      }
      else if (ctl.ph === 'sky' && el >= n * SG_LINE + 4000) await upd({ ph: 'done', at: Date.now(), dn: doneN });
      else if (ctl.ph === 'done' && el >= (ctl.dn || doneN) * (ctl.sm || SG_STORY) + 5000){
        await upd({ ok: 1, ph: 'end', open: false });
        const h = (await ref('hist').get()).val() || {}; await ref('hist').update({ total: (+h.total || 0) + 1 }); await ref('hist/c/' + C.id).set(((h.c || {})[C.id] || 0) + 1);
        return 'done ' + C.id;
      }
    }
    await upd({ ok: 0, ph: 'end', open: false }); return 'timeout';   // 너무 오래 걸리면 닫아요 (보통 6 분 안에 끝나요)
  } finally { offs.forEach(f => f()); }
}

async function runAuto(db, key){
  const old = (await db.ref('autoreq').get()).val() || {}, cut = Date.now() - 3 * 864e5, del = {};
  Object.entries(old).forEach(([k, v]) => { if (typeof v !== 'number' || v < cut) del[k] = null; });   // 사흘 지난 신호는 지워요
  if (Object.keys(del).length) await db.ref('autoreq').update(del);
  const cfg = (await db.ref('autocfg').get()).val() || {};
  if (key.startsWith('gt_')) return cfg.gtOff ? 'off' : openTrain(db);
  if (key.startsWith('sg_')) return cfg.sgOff ? 'off' : runStargaze(db);
  return 'unknown';
}
module.exports = { runAuto };
