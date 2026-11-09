// 고친 스킬을 전투 코드로 직접 써 보기 (Lv 1 · 5): node tools/balance/run_bal.js tools/balance/skillfix_check.js [포트] → out/skillfix_check.txt
//   피해가 실제로 들어가는지 · 붙는 효과 · 회복 MP · 회피 · 소생 체력 · 버티기 체력 · 쿨타임을 기대값과 비교해요 (피해는 ±15% 흔들림이 있어서 배율 범위로 봐요)
const fs = require('fs');
const C = [
  ['warrior', '파쇄', { dmgK: [1, 1.72], fx: { vuln: [.3, 12] } }],
  ['alch', '부식', { dmgK: [.8, 1.38], fx: { vuln: [.3, 12], dot: [null, 8] } }],
  ['gadget', '접착탄', { dmgK: [1.6, 2.75], fx: { slow: [.4, 8] } }],
  ['alch', '마력 물약', { mp: [.25, .4] }],
  ['summon', '마력 연결', { mp: [.25, .4] }],
  ['black', '마력 흡수', { dmgK: [.7, 1.2], cd: 3 }],
  ['thief', '그림자 걸음', { dodge: [.3125, .5] }],
  ['warrior', '불굴', { surv: [.05, .25] }],
  ['white', '가호', { surv: [.05, .25] }],
  ['white', '되살리기', { rev: [.5, .7] }],
  ['white', '완전 소생', { rev: [.75, 1] }],
  ['white', '전체 소생', { rev: [.4, .56] }],
  ['white', '천사의 숨결', { rev: [.3, .42], hl: [1.2, 2.064] }],
  ['bard', '되살림의 화음', { rev: [.4, .56] }],
  ['cleric', '구원의 빛', { rev: [.6, .8] }],
  ['cleric', '축복', { regen: [.5, .86] }],
];
module.exports = async (ev, log) => {
  const L = [], bad = [];
  for (const [job, n, E] of C) for (const [i, lv] of [[0, 1], [1, 5]]){
    const r = await ev(o => __bal.skCheck(o), { job, n, lv, L: 30, dead: !!E.rev });
    const fl = [], line = [`${job} ${n} Lv${lv}:`];
    if (E.dmgK){ const k = r.dmg / r.stat; line.push(`피해 ${r.dmg} = ${r.sk ? '' : ''}능력치 ×${k.toFixed(2)} (기대 ×${E.dmgK[i]} ±15%)`); if (!(k > E.dmgK[i] * .84 && k < E.dmgK[i] * 1.16 + (E.fx && E.fx.vuln ? 0 : 0))) fl.push('피해'); }
    if (E.fx) Object.entries(E.fx).forEach(([k, [v, t]]) => { const f = r.foeFx[k]; line.push(`${k} ${f ? `v ${+f.v.toFixed(2)} · ${+f.t.toFixed(1)}초` : '없음'}`); if (!f || (v != null && Math.abs(f.v - v) > 1e-6) || Math.abs(f.t - t) > .01) fl.push(k); });
    if (E.mp){ line.push(`MP 회복 ${(r.mpGain[1] * 100).toFixed(1)}% (기대 ${E.mp[i] * 100}%)`); if (Math.abs(r.mpGain[1] - E.mp[i]) > .002) fl.push('MP'); }
    if (E.cd != null){ line.push(`쿨 ${r.cdLeft}턴`); if (r.cdLeft !== E.cd) fl.push('쿨'); }
    if (E.dodge){ const v = Math.min(.5, (r.myFx.dodge || {}).v || 0); line.push(`회피 ${(v * 100).toFixed(1)}% (기대 ${(E.dodge[i] * 100).toFixed(1)}%)`); if (Math.abs(v - E.dodge[i]) > .002) fl.push('회피'); }
    if (E.surv){ line.push(`버틴 체력 ${(r.surviveHp * 100).toFixed(1)}% (기대 ${E.surv[i] * 100}%)`); if (Math.abs(r.surviveHp - E.surv[i]) > .01) fl.push('버티기'); }
    if (E.rev){ const heal = E.hl ? Math.round(r.heal * E.hl[i]) / r.mhp2 : 0, ex = Math.min(1, E.rev[i] + heal); line.push(`소생 체력 ${(r.revHp * 100).toFixed(1)}% (기대 ${(ex * 100).toFixed(1)}%${E.hl ? ` = ${E.rev[i] * 100}% + 치유 ×${E.hl[i]}` : ''})`); if (Math.abs(r.revHp - ex) > .01) fl.push('소생'); }
    if (E.regen){ const g = r.a2fx.regen; line.push(`재생 ${g ? g.v : '없음'} / 2초 (기대 치유 ${r.heal} ×${E.regen[i]} = ${Math.round(r.heal * E.regen[i])})`); if (!g || Math.abs(g.v - Math.round(r.heal * E.regen[i])) > 1) fl.push('재생'); }
    if (fl.length){ line.push('!! ' + fl.join(' · ')); bad.push(`${n} Lv${lv}: ${fl.join(' · ')}`); }
    L.push(line.join(' · ')); log(line.join(' · '));
  }
  L.push('', `어긋남 ${bad.length}건`, ...bad);
  fs.writeFileSync(__dirname + '/out/skillfix_check.txt', L.join('\n') + '\n'); log(`mismatches ${bad.length}`);
};
