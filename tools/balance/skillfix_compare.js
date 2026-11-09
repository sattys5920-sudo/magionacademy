// 스킬 버그 수정 전후 비교: 탐사(동굴 · 신전, 최대 버프 · 버프 없음) + 레이드(최대 버프 얼음 왕관) 승률
//   node tools/balance/run_bal.js tools/balance/skillfix_compare.js [포트]   (TAG=before|after 로 out/skillfix_<TAG>.json)
//   수정 전 값은 수정 전 커밋을 git worktree 로 꺼내 그쪽 run_bal.js 로 돌려요
const X = require('./explore_cfg.js'), R = require('./raid_cfg.js'), fs = require('fs');
module.exports = async (ev, log) => {
  const out = { explore: [], raid: [] }, N = 150;
  for (const rg of [2, 3]) for (const [kind, L, mL] of X.SC[rg]) for (const pt of Object.keys(X.PT)) {
    const mx = await X.run(ev, rg, kind, L, mL, pt, X.max(rg, L, kind), null, N), bn = await X.run(ev, rg, kind, L, mL, pt, X.base(rg, L), null, N);
    out.explore.push({ stage: rg + 1, kind, pt, max: mx, base: bn }); log(`${rg + 1} ${kind.padEnd(6)} ${pt.padEnd(4)} 최대버프 ${mx.win}/${mx.hp}  장비만 ${bn.win}/${bn.hp}`); }
  const { RD_BOSS, RD_MATK } = await ev(() => __bal.RD_());
  for (let f = 0; f < 4; f++){ const r = await R.sim(ev, f, { n: 200, ...R.max(R.LV[f], 'crown'), hpAbs: RD_BOSS[f][0], atkAbs: RD_BOSS[f][1], matk: RD_MATK[f] }); out.raid.push({ f: f + 1, r }); log(`raid ${f + 1}F ${JSON.stringify(r)}`); }
  fs.writeFileSync(__dirname + `/out/skillfix_${process.env.TAG || 'run'}.json`, JSON.stringify(out, null, 1));
};
