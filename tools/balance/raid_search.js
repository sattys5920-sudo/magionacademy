// 레이드: 공격 ×1.15 로 두고 최대 버프 12 명 승률 50 % 가 되는 체력 배율을 층마다 이분 탐색 (RB = v1 값 기준) → out/raid_new.json
const R = require('./raid_cfg.js'), fs = require('fs');
module.exports = async (ev, log) => { const AK = 1.15, out = [];
  for (let f = 0; f < 4; f++) { const cfg = R.max(R.LV[f], 'crown'); let lo = 1, hi = 2.5, best;
    const run = (h, n) => R.sim(ev, f, { n, ...cfg, hpAbs: Math.round(R.RB[f][0] * h), atkAbs: Math.round(R.RB[f][1] * AK), matk: Math.round(R.RB[f][2] * AK) });
    for (let k = 0; k < 8; k++) { const h = (lo + hi) / 2, r = await run(h, 120); if (r.win > .5) lo = h; else hi = h; best = { h, ...r }; }
    let h = +((lo + hi) / 2).toFixed(3), fin = await run(h, 400);
    for (let k = 0; k < 4 && Math.abs(fin.win - .5) > .03; k++) { h = +(h * (fin.win > .5 ? 1.01 : .99)).toFixed(3); fin = await run(h, 400); }
    const o = { f: f + 1, L: R.LV[f], hK: h, aK: AK, hp: Math.round(R.RB[f][0] * h), atk: Math.round(R.RB[f][1] * AK), matk: Math.round(R.RB[f][2] * AK), ...fin }; log(JSON.stringify(o)); out.push(o); }
  fs.writeFileSync(__dirname + '/out/raid_new.json', JSON.stringify(out)); };
