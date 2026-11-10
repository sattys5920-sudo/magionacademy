// 요일 던전 × 2차 직업: 4 명 파티에서 한 자리를 새 직업으로 바꾸면 승률이 얼마나 오르는지 (목표 레벨 · 최대 장비)
//   node tools/balance/run_bal.js tools/balance/day_newjobs.js
const R = require('./raid_cfg.js');
const SETS = process.env.OLD ? { cleric: ['warrior', 'knight', 'black', 'cleric'], white: ['warrior', 'knight', 'black', 'white'], druid: ['warrior', 'knight', 'black', 'druid'], bard: ['warrior', 'knight', 'black', 'bard'], time: ['warrior', 'knight', 'time', 'cleric'] } : { base: ['warrior', 'knight', 'black', 'cleric'], shaman: ['warrior', 'knight', 'black', 'shaman'], miko: ['warrior', 'knight', 'black', 'miko'], dancer: ['warrior', 'knight', 'dancer', 'cleric'], sage: ['warrior', 'knight', 'sage', 'cleric'], darkknight: ['warrior', 'darkknight', 'black', 'cleric'], gunner: ['warrior', 'knight', 'gunner', 'cleric'], fighter: ['fighter', 'knight', 'black', 'cleric'] };
module.exports = async (ev, log) => {
  const T = [30, 40, 50];
  for (const [k, jobs] of Object.entries(SETS)){
    const row = [];
    for (let lv = 0; lv < 3; lv++){ let w = 0; for (let d = 0; d < 5; d++){ const r = await ev(o => __bal.ddSim(o), { w: d, lv, L: T[lv], n: 80, jobs, ...R.max(T[lv], 'mix') }); w += r.win; } row.push(+(w / 5).toFixed(2)); }
    log(k.padEnd(11), jobs.join(','), '쉬움 · 보통 · 어려움 승률', row.join(' · '));
  }
};
