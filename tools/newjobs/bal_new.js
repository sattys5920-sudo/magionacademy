// 새 직업 12 종 밸런스: node tools/balance/run_bal.js tools/newjobs/bal_new.js
//   1) 허수아비: 초당 피해 · 버티는 시간 (Lv 30 · 40, 무기 3 · 방어구 그 레벨 최대) — 같은 역할 기존 직업 평균과 비교
//   2) 파티 승률: 기본 파티 [기사 · 전사 · 흑마법사 · 백마법사] 에서 한 자리를 새 직업으로 바꿔 보스전 승률 비교
const ROLE = { tank: ['knight'], melee: ['warrior', 'thief'], ranged: ['black', 'gadget', 'summon', 'alch'], heal: ['white', 'druid', 'cleric'], support: ['bard', 'time'] };
const NEW = { paladin: 'tank', guardian: 'tank', darkknight: 'tank', dancer: 'support', sage: 'support', shaman: 'heal', miko: 'heal', archer: 'ranged', gunner: 'ranged', elemental: 'ranged', fighter: 'melee', bladedancer: 'melee' };
const SLOT = { tank: 0, melee: 1, ranged: 2, heal: 3, support: 3 };
module.exports = async (ev, log) => {
  const out = { power: {}, party: {} };
  for (const L of (process.env.NOPOW ? [] : [30, 40])){
    const arc = await ev(L => __bal.arCap(L), L), cfg = { wp: 3, ar: arc }, P = j => ev(([j, L, c]) => __bal.power(j, L, c, 20), [j, L, cfg]);
    const pw = {}; for (const j of [...new Set(Object.values(ROLE).flat()), ...Object.keys(NEW)]) pw[j] = await P(j);
    out.power[L] = pw;
    for (const [j, r] of Object.entries(NEW)){ const base = ROLE[r], avg = k => base.reduce((s, b) => s + pw[b][k], 0) / base.length;
      log(`L${L} ${j.padEnd(12)} ${r.padEnd(8)} dps ${pw[j].dps.toFixed(0).padStart(5)} (기존 ${avg('dps').toFixed(0)} → ${(pw[j].dps / avg('dps')).toFixed(2)}) · 버티기 ${pw[j].surv.toFixed(0).padStart(4)} (기존 ${avg('surv').toFixed(0)} → ${(pw[j].surv / avg('surv')).toFixed(2)})`); }
  }
  // 파티 강한 몬스터전 (고대 신전 · Lv 45 · 몬스터 Lv 45 · 최대 버프 장비 · 물약 1)
  const { max } = require(__dirname + '/../balance/explore_cfg.js'), sim = jobs => ev(o => __bal.xSim(o), { rg: 3, L: 45, mL: 45, kind: 'elite', jobs, pot: 1, n: 240, ...max(3, 45, 'elite') });
  const base = ['knight', 'warrior', 'black', 'white'], b0 = await sim(base); log('기본 파티', base.join(','), JSON.stringify(b0)); out.party.base = b0;
  const alt = { tank: 'knight', melee: 'warrior', ranged: 'black', heal: 'white', support: 'bard' };
  for (const r of ['support']){ const j = base.slice(); j[SLOT[r]] = alt[r]; const x = await sim(j); log('기존', r, j.join(','), JSON.stringify(x)); out.party['old_' + r] = x; }
  for (const [nj, r] of Object.entries(NEW)){ const j = base.slice(); j[SLOT[r]] = nj; const x = await sim(j); log('새', nj.padEnd(12), j.join(','), JSON.stringify(x)); out.party[nj] = x; }
  require('fs').writeFileSync(__dirname + '/bal_new.json', JSON.stringify(out));
};
