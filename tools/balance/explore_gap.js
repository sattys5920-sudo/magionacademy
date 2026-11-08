// 1) 탐사: 예전 세기에서 기준 cfg 와 최대 버프 cfg 의 차이 → out/xgap.json   (node tools/balance/run_bal.js tools/balance/explore_gap.js)
const X = require('./explore_cfg.js');
module.exports = async (ev, log) => {
  const out = {};
  for (const rg of [2, 3]) for (const [kind, L, mL] of X.SC[rg]) for (const pt of Object.keys(X.PT)) {
    const b = await X.run(ev, rg, kind, L, mL, pt, X.base(rg, L), null, 80), m = await X.run(ev, rg, kind, L, mL, pt, X.max(rg, L, kind), null, 80);
    log(rg, kind, pt, 'base', JSON.stringify(b), 'max', JSON.stringify(m)); out[[rg, kind, pt].join('_')] = { b, m };
  }
  require('fs').writeFileSync(__dirname + '/out/xgap.json', JSON.stringify(out));
};
