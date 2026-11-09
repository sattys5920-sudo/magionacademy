// 레이드만 다시 (층 1~4 · 최대 버프 얼음 왕관 · n 판): node tools/balance/run_bal.js tools/balance/skillfix_raid.js [포트]   (N=판 수 · F=층만)
const R = require('./raid_cfg.js');
module.exports = async (ev, log) => { const { RD_BOSS, RD_MATK } = await ev(() => __bal.RD_()), n = +(process.env.N || 300);
  for (let f = 0; f < 4; f++){ if (process.env.F && +process.env.F !== f + 1) continue; const r = await R.sim(ev, f, { n, ...R.max(R.LV[f], 'crown'), hpAbs: RD_BOSS[f][0], atkAbs: RD_BOSS[f][1], matk: RD_MATK[f] }); log(`${process.env.TAG || ''} raid ${f + 1}F ${JSON.stringify(r)}`); } };
