// 3) 탐사 확인: 기준(예전 세기) · 최대 버프(예전) · 최대 버프(지금 게임 값) · 기준 장비만(지금) → out/xverify.json
const X = require('./explore_cfg.js'), fs = require('fs');
const OLD = { 2: { hpm: 3.5, ehm: 1.8, atkm: 3, bat: 1.6, bhm: 2 }, 3: { hpm: 4.5, ehm: 2.7, atkm: 5.2, bat: .6, bhm: 1.2 } };
module.exports = async (ev, log) => { log(JSON.stringify(await ev(() => __bal.XRG_())));
  const out = [];
  for (const rg of [2, 3]) for (const [kind, L, mL] of X.SC[rg]) for (const pt of Object.keys(X.PT)) {
    const N = 150, b = await X.run(ev, rg, kind, L, mL, pt, X.base(rg, L), OLD[rg], N), mo = await X.run(ev, rg, kind, L, mL, pt, X.max(rg, L, kind), OLD[rg], N), mn = await X.run(ev, rg, kind, L, mL, pt, X.max(rg, L, kind), null, N), bn = await X.run(ev, rg, kind, L, mL, pt, X.base(rg, L), null, N);
    const o = { stage: rg + 1, kind, pt, base_old: b, max_old: mo, max_new: mn, base_new: bn }; out.push(o);
    log(`${rg + 1} ${kind.padEnd(6)} ${pt.padEnd(4)} 기준(예전) ${b.win}/${b.hp}  최대버프(예전) ${mo.win}/${mo.hp}  최대버프(새) ${mn.win}/${mn.hp}  버프없음(새) ${bn.win}/${bn.hp}`); }
  fs.writeFileSync(__dirname + '/out/xverify.json', JSON.stringify(out)); };
