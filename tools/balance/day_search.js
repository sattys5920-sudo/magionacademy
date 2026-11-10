// 요일 던전 세기 찾기: node tools/balance/run_bal.js tools/balance/day_search.js
//   요일 · 난이도 · 인원(1 ~ 4)마다 체력 배율을 찾아 「최대로 갖춘 학생이 그 난이도 목표 레벨(30 · 40 · 50)에서 반쯤 이기게」 맞춰요
//   파티: 혼자는 24 직업(1차 · 2차)을 돌아가며 · 2 명 기사 + 힐러 · 3 명 기사 + 흑마법사 + 힐러 · 4 명 전사 + 기사 + 흑마법사 + 힐러
//   힐러 자리는 판마다 성직자 · 백마법사 · 드루이드 · 음유시인 · 주술사 · 무녀를 돌아가며 (예전엔 성직자만이라 다른 힐러가 있으면 거의 다 이겼어요)
//   (DD_AVG=1 이면 예전처럼 힐러 6 종 평균)
//   1) 보스가 거의 안 때릴 때 잡는 데 평균 200 초가 걸리게 체력 배율 · 2) 그다음 이길 확률이 50 % 가 되게 공격 배율 (제한 300 초)
//   결과: tools/balance/out/day_k.json · tools/daydungeon/day_balance.json
const R = require('./raid_cfg.js'), fs = require('fs');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
const HEAL = ['cleric', 'white', 'druid', 'bard', 'shaman', 'miko'];
const PARTY = [null, ['knight'], ['knight', 'black'], ['warrior', 'knight', 'black']];   // + 힐러 한 명 (판마다 돌아가며)
// 지금 기준: 「제일 좋은 조합」 (tools/balance/day_best.js 로 찾음) 이 반쯤 이기게 · 판마다 아래 조합을 돌아가며
const BEST = [[['warrior'], ['fighter'], ['bladedancer']], [['knight', 'druid'], ['darkknight', 'shaman'], ['warrior', 'shaman']], [['knight', 'black', 'shaman'], ['knight', 'sage', 'shaman']], [['knight', 'black', 'shaman', 'druid'], ['warrior', 'knight', 'sage', 'shaman'], ['fighter', 'knight', 'sage', 'shaman']]];
const ONLY = process.env.DD_ONLY ? JSON.parse(process.env.DD_ONLY) : null;   // 예: [[0,0,1]] 요일 · 난이도 · 인원
module.exports = async (ev, log) => {
  const T = [30, 40, 50], OUTF = __dirname + '/out/' + (process.env.DD_OUT || 'day_k.json'), out = fs.existsSync(OUTF) ? JSON.parse(fs.readFileSync(OUTF)) : {};
  const sim = (w, lv, n, hK, aK, N, lim) => ev(o => { const A = o.all, H = o.heal, P = o.base, Bs = o.best; o.jobs = Bs ? it => Bs[it % Bs.length] : o.solo ? it => [A[it % A.length]] : it => [...P, H[it % H.length]]; return __bal.ddSim(o); }, { w, lv, L: T[lv], n: N, lim, K: [hK, aK], ...R.max(T[lv], 'mix'), all: ALL, heal: HEAL, base: PARTY[n - 1], solo: n === 1 ? 1 : 0, best: process.env.DD_AVG ? null : BEST[n - 1] });
  for (let w = 0; w < 5; w++) for (let lv = 0; lv < 3; lv++) for (let n = 1; n <= 4; n++){
    if (ONLY && !ONLY.some(x => x[0] === w && x[1] === lv && x[2] === n)) continue;
    let lo = .02, hi = 50; for (let k = 0; k < 12; k++){ const m = Math.sqrt(lo * hi), r = await sim(w, lv, n, m, .001, 24, 2000); if (r.t < 200) lo = m; else hi = m; } const hK = +Math.sqrt(lo * hi).toFixed(3);
    lo = .05; hi = 40; for (let k = 0; k < 11; k++){ const m = Math.sqrt(lo * hi), r = await sim(w, lv, n, hK, m, 60, 300); if (r.win > .5) lo = m; else hi = m; } const aK = +Math.sqrt(lo * hi).toFixed(3), v = await sim(w, lv, n, hK, aK, 300, 300);
    out[`${w}_${lv}_${n}`] = { hK, aK, ...v }; log(JSON.stringify({ w, lv, n, hK, aK, ...v })); fs.writeFileSync(OUTF, JSON.stringify(out));
  }
  if (!process.env.DD_OUT) fs.writeFileSync(__dirname + '/../daydungeon/day_balance.json', JSON.stringify(out, null, 1));
};
