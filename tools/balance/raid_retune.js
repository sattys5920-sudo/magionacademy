// 레이드 체력 배율 다시 맞추기 (공격은 그대로): 최대 버프 12 명 얼음 왕관 승률 50 % ± 3 % 가 될 때까지 체력 배율을 고쳐 가며 400 판씩
//   F=층(1~4) K0=시작 배율 AK=공격 배율 node tools/balance/run_bal.js tools/balance/raid_retune.js [포트] → out/raid_retune_<F>.json (층마다 따로 돌려도 돼요)
const R = require('./raid_cfg.js'), fs = require('fs');
module.exports = async (ev, log) => { const f = +process.env.F - 1, AK = +(process.env.AK || 1.15), cfg = R.max(R.LV[f], 'crown'), hist = [];
  const run = (h, n) => R.sim(ev, f, { n, ...cfg, hpAbs: Math.round(R.RB[f][0] * h), atkAbs: Math.round(R.RB[f][1] * AK), matk: Math.round(R.RB[f][2] * AK) });
  let h = +process.env.K0, r;
  for (let k = 0; k < 8; k++){ r = await run(h, 400); hist.push({ h, ...r }); log(`${f + 1}F h ${h} → ${JSON.stringify(r)}`); if (Math.abs(r.win - .5) <= .03) break; h = +(h * (1 + (r.win - .5) * .07)).toFixed(4); }
  fs.writeFileSync(__dirname + `/out/raid_retune_${f + 1}.json`, JSON.stringify({ f: f + 1, h, r, hist })); };
