// 직업 · 레벨별 힘 비교: 허수아비 상대로 초당 피해 · 버티는 시간 (맨몸 z · 예전 가정 장비 o · 최대 버프 m) → out/power.json
module.exports = async (ev, log) => {
  const jobs = ['knight', 'warrior', 'black', 'gadget', 'white', 'cleric', 'summon', 'alch'];
  const LVS = [[30, 's3', 3], [38, 's3', 3], [43, 's4', 4], [50, 's4', 4], [15, 'r1', 1], [25, 'r2', 2], [35, 'r3', 3], [45, 'r4', 4]];
  const res = {};
  for (const [L, tag, eq] of LVS) {
    const arc = await ev(L => __bal.arCap(L), L);
    const orig = tag[0] === 's' ? { wp: eq, ar: arc } : { wp: eq, ar: eq };
    const mx = a => ({ wp: 4, ar: arc, dfire: 1, dwater: 1, nb: 1, fam: tag[0] === 'r' ? 'xboss' : 'xmain', acc: a, accSt: 5 });
    for (const j of jobs) {
      const n = 24, P = c => ev(([j, L, c, n]) => __bal.power(j, L, c, n), [j, L, c, n]);
      const z = await P({}), o = await P(orig), m = {};
      for (const a of ['crown', 'cape', 'hat', 'neck']) m[a] = await P(mx(a));
      const bestD = Math.max(...Object.values(m).map(x => x.dps)), bestS = Math.max(...Object.values(m).map(x => x.surv));
      const r = { L, tag, j, z, o, m, dZ: +(bestD / z.dps).toFixed(3), sZ: +(bestS / z.surv).toFixed(3), dO: +(bestD / o.dps).toFixed(3), sO: +(bestS / o.surv).toFixed(3), cape: { d: +(m.cape.dps / o.dps).toFixed(3), s: +(m.cape.surv / o.surv).toFixed(3) }, crown: { d: +(m.crown.dps / o.dps).toFixed(3), s: +(m.crown.surv / o.surv).toFixed(3) } };
      log(JSON.stringify({ L, tag, j, dZ: r.dZ, sZ: r.sZ, dO: r.dO, sO: r.sO, cape: r.cape, crown: r.crown, accD: Object.fromEntries(Object.entries(m).map(([k, v]) => [k, v.dps])) }));
      (res[tag + L] = res[tag + L] || []).push(r);
    }
  }
  require('fs').writeFileSync(__dirname + '/out/power.json', JSON.stringify(res));
};
