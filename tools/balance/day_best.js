// 요일 던전 「제일 좋은 조합」 찾기 (지금 DD_K · 목표 레벨 · 최대 장비): 혼자 24 직업 · 2 ~ 4 명 후보 파티 승률
//   node tools/balance/run_bal.js tools/balance/day_best.js
const R = require('./raid_cfg.js');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
const CAND = {
  2: [['knight', 'shaman'], ['knight', 'druid'], ['darkknight', 'shaman'], ['paladin', 'shaman'], ['shaman', 'druid'], ['warrior', 'shaman'], ['knight', 'white']],
  3: [['knight', 'black', 'shaman'], ['knight', 'black', 'druid'], ['knight', 'sage', 'shaman'], ['knight', 'dancer', 'shaman'], ['darkknight', 'black', 'shaman'], ['knight', 'shaman', 'druid'], ['fighter', 'knight', 'shaman']],
  4: [['warrior', 'knight', 'black', 'shaman'], ['warrior', 'knight', 'black', 'druid'], ['warrior', 'knight', 'sage', 'shaman'], ['warrior', 'knight', 'dancer', 'shaman'], ['fighter', 'knight', 'sage', 'shaman'], ['warrior', 'darkknight', 'black', 'shaman'], ['knight', 'black', 'shaman', 'druid'], ['warrior', 'knight', 'shaman', 'druid'], ['fighter', 'darkknight', 'sage', 'shaman']]
};
module.exports = async (ev, log) => {
  const T = [30, 40, 50], avg = async jobs => { let w = 0; for (let d = 0; d < 5; d++) for (let lv = 0; lv < 3; lv++){ const r = await ev(o => __bal.ddSim(o), { w: d, lv, L: T[lv], n: 24, jobs, ...R.max(T[lv], 'mix') }); w += r.win; } return +(w / 15).toFixed(3); };
  const solo = []; for (const j of ALL) solo.push([j, await avg([j])]); solo.sort((a, b) => b[1] - a[1]); log('혼자', JSON.stringify(solo.slice(0, 6)));
  for (const n of [2, 3, 4]){ const r = []; for (const p of CAND[n]) r.push([p.join(','), await avg(p)]); r.sort((a, b) => b[1] - a[1]); log(n + ' 명', JSON.stringify(r.slice(0, 4))); }
};
