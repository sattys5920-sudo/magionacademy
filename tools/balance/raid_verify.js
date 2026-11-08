// 레이드 확인: 지금 게임 값(RD_BOSS · RD_MATK)으로 최대 버프 12 명 400 판 · 다른 장신구 조합 · 장비만 · 맨몸 → tools/raid_mock/raid_balance.json
const R = require('./raid_cfg.js'), fs = require('fs');
module.exports = async (ev, log) => { const { RD_BOSS, RD_MATK } = await ev(() => __bal.RD_()); log(JSON.stringify({ RD_BOSS, RD_MATK })); const out = [];
  for (let f = 0; f < 4; f++) { const L = R.LV[f], o = { hpAbs: RD_BOSS[f][0], atkAbs: RD_BOSS[f][1], matk: RD_MATK[f] };
    const mx = await R.sim(ev, f, { n: 400, ...R.max(L, 'crown'), ...o }), mix = await R.sim(ev, f, { n: 200, ...R.max(L, 'mix'), ...o }), eq = await R.sim(ev, f, { n: 200, cfg: { wp: f + 1, ar: f + 1 }, ...o }), none = await R.sim(ev, f, { n: 100, cfg: {}, ...o });
    const old = await R.sim(ev, f, { n: 200, ...R.max(L, 'crown') });
    const r = { L, b: f, hp: o.hpAbs, atk: o.atkAbs, matk: o.matk, hpK: [1.43, 1.345, 1.26, 1.2][f], atkK: 1.15, party: '12 명 · 직업 12 개 · 무기 4 · 방어구 ' + R.arCap(L) + ' · 장신구 ★5 얼음 왕관 · 용의 가호 둘 · 사역마 맹약(보스전 +10 %) · 누비 헝겊 · 방장 물약 92 %', ...mx, win_mixAcc: mix.win, win_eqOnly: eq.win, win_noGear: none.win, win_maxAtOldStats: old.win };
    log(JSON.stringify(r)); out.push(r); }
  fs.writeFileSync(__dirname + '/out/raid_final.json', JSON.stringify(out)); fs.writeFileSync(__dirname + '/../raid_mock/raid_balance.json', JSON.stringify(out.map(r => ({ L: r.L, b: r.b, hpK: r.hpK, atkK: r.atkK, hp: r.hp, atk: r.atk, matk: r.matk, win: r.win, t: r.t, left: r.left, dead: r.dead, acts: r.acts, win_mixAcc: r.win_mixAcc, win_eqOnly: r.win_eqOnly, win_noGear: r.win_noGear, party: r.party })))); };
