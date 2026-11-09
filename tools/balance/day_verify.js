// 요일 던전 확인: 지금 게임 값(DD_K)으로 · 목표 레벨(최대 장비) · 권장 레벨(최대 장비) · 목표 레벨(장비만) 승률 → tools/daydungeon/day_verify.json
//   node tools/balance/run_bal.js tools/balance/day_verify.js
const R = require('./raid_cfg.js'), fs = require('fs');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard'];
const PARTY = [null, ['knight', 'cleric'], ['knight', 'black', 'cleric'], ['warrior', 'knight', 'black', 'cleric']];
module.exports = async (ev, log) => {
  const T = [30, 40, 50], REC = [20, 35, 45], out = [];
  const sim = (w, lv, n, L, cfg, N) => ev(o => { if (o.solo) o.jobs = it => [o.all[it % 12]]; return __bal.ddSim(o); }, { w, lv, L, n: N, ...cfg, ...(n === 1 ? { solo: 1, all: ALL } : { jobs: PARTY[n - 1] }) });
  for (let w = 0; w < 5; w++) for (let lv = 0; lv < 3; lv++) for (let n = 1; n <= 4; n++){
    const a = await sim(w, lv, n, T[lv], R.max(T[lv], 'mix'), 300), b = await sim(w, lv, n, REC[lv], R.max(REC[lv], 'mix'), 120), c = await sim(w, lv, n, T[lv], { cfg: { wp: 2 + lv, ar: R.arCap(T[lv]) } }, 120);
    const r = { w, lv, n, win: a.win, t: a.t, dead: a.dead, win_rec: b.win, win_eqOnly: c.win }; out.push(r); log(JSON.stringify(r)); }
  fs.writeFileSync(__dirname + '/../daydungeon/day_verify.json', JSON.stringify(out, null, 1));
};
