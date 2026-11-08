// 2) 탐사: 최대 버프 cfg 가 기준(out/xgap.json)과 비슷해지는 배율 찾기 (일반 hpm·atkm → 강한 몬스터 ehm → 보스 bhm·bat) → out/xsearch.json · 그다음 보스는 체력 · 공격 합계 배율 격자를 따로 봤어요
const X = require('./explore_cfg.js'), fs = require('fs');
const gap = JSON.parse(fs.readFileSync(__dirname + '/out/xgap.json'));
module.exports = async (ev, log) => {
  const M0 = { 2: { hpm: 3.5, ehm: 1.8, atkm: 3, bat: 1.6, bhm: 2 }, 3: { hpm: 4.5, ehm: 2.7, atkm: 5.2, bat: .6, bhm: 1.2 } }, N = 100, res = {};   // 예전(버프 반영 전) 값에서 출발
  const loss = async (rg, kind, m) => { let l = 0, det = []; for (const [k, L, mL] of X.SC[rg]) { if (k !== kind) continue; for (const pt of Object.keys(X.PT)) { const b = gap[[rg, k, pt].join('_')].b, r = await X.run(ev, rg, k, L, mL, pt, X.max(rg, L, k), m, N); l += (r.hp - b.hp) ** 2 + (r.win - b.win) ** 2; det.push(pt + ':' + r.win + '/' + b.win); } } return [l, det.join(' ')]; };
  for (const rg of [2, 3]) {
    const m0 = M0[rg]; let best;
    // 1) 일반 몬스터: 체력(hpm) · 공격(atkm)
    best = null; for (const h of [1, 1.15, 1.3, 1.45, 1.6]) for (const a of [1, 1.15, 1.3, 1.45, 1.6]) { const m = { ...m0, hpm: m0.hpm * h, atkm: m0.atkm * a }; const [l, d] = await loss(rg, 'battle', m); if (!best || l < best.l) best = { l, h, a, d }; }
    log(rg, 'battle', JSON.stringify(best)); const hN = best.h, aN = best.a;
    // 2) 강한 몬스터: 체력(ehm) (공격은 sqrt(atkm) 를 따라가요)
    best = null; for (const h of [1, 1.15, 1.3, 1.45, 1.6, 1.8, 2]) { const m = { ...m0, hpm: m0.hpm * hN, atkm: m0.atkm * aN, ehm: m0.ehm * h }; const [l, d] = await loss(rg, 'elite', m); if (!best || l < best.l) best = { l, h, d }; }
    log(rg, 'elite', JSON.stringify(best)); const hE = best.h;
    // 3) 보스: 체력(bhm) · 공격(bat)
    best = null; for (const h of [.9, 1, 1.15, 1.3, 1.45]) for (const a of [1, 1.15, 1.3, 1.45, 1.6]) { const m = { ...m0, hpm: m0.hpm * hN, atkm: m0.atkm * aN, ehm: m0.ehm * hE, bhm: m0.bhm * h, bat: m0.bat * a }; const [l, d] = await loss(rg, 'boss', m); if (!best || l < best.l) best = { l, h, a, d }; }
    log(rg, 'boss', JSON.stringify(best));
    res[rg] = { hN, aN, hE, hB: best.h, aB: best.a };
  }
  log(JSON.stringify(res)); fs.writeFileSync(__dirname + '/out/xsearch.json', JSON.stringify(res));
};
