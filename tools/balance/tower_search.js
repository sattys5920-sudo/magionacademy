// 시련의 탑 세기 찾기: node tools/balance/run_bal.js tools/balance/tower_search.js [포트]
//   층마다: 그 층 기준 레벨 (1 층 Lv 16 → 50 층 Lv 50) · 그만큼 갖춘 장비 (__bal.twCfg) 로 24 직업이 혼자 올라가요
//   1) 몬스터가 거의 안 때릴 때 「불리 아닌 직업」이 평균 TW_T 초 (기본 45 초) 만에 잡게 체력 배율
//   2) 그다음 「불리 아닌 직업」 승률이 TW_TGT (기본 75 %) 가 되게 공격 배율
//   환경 변수: TW_FL="1-10" 층 범위 · TW_OUT 결과 파일 이름 (기본 tw_k.json) → tools/balance/out/
const fs = require('fs');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
const TGT = +(process.env.TW_TGT || .75), TT = +(process.env.TW_T || 45);
module.exports = async (ev, log) => {
  const [a, b] = (process.env.TW_FL || '1-50').split('-').map(Number), OUTF = __dirname + '/out/' + (process.env.TW_OUT || 'tw_k.json');
  const out = fs.existsSync(OUTF) ? JSON.parse(fs.readFileSync(OUTF)) : {};
  for (let f = a; f <= (b || a); f++){
    const ok = await ev(o => __bal.twOk(o.f, o.all), { f, all: ALL });
    const sim = (K, n, lim, jobs) => ev(o => __bal.twSim(o), { f, K, n, lim, jobs: jobs || ok });
    let lo = .05, hi = 20; for (let k = 0; k < 10; k++){ const m = Math.sqrt(lo * hi), r = await sim([m, .001], 3, 2000); if (r.t < TT) lo = m; else hi = m; } const hK = +Math.sqrt(lo * hi).toFixed(3);
    lo = .05; hi = 20; for (let k = 0; k < 10; k++){ const m = Math.sqrt(lo * hi), r = await sim([hK, m], 5, 300); if (r.win > TGT) lo = m; else hi = m; } const aK = +Math.sqrt(lo * hi).toFixed(3);
    const v = await sim([hK, aK], 10, 300, ALL), okW = ok.reduce((s, j) => s + v.per[j], 0) / ok.length, bad = ALL.filter(j => !ok.includes(j)), badW = bad.length ? bad.reduce((s, j) => s + v.per[j], 0) / bad.length : null;
    const lowL = await ev(o => __bal.twSim(o), { f, K: [hK, aK], n: 6, lim: 300, jobs: ok, L: Math.max(1, Math.round(16 + (f - 1) * 34 / 49) - 3) });
    out[f] = { hK, aK, ok: +okW.toFixed(2), bad: badW == null ? null : +badW.toFixed(2), all: v.win, t: v.t, low3: lowL.win };
    log(JSON.stringify({ f, ...out[f] })); fs.writeFileSync(OUTF, JSON.stringify(out));
  }
};
