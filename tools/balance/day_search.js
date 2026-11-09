// 요일 던전 세기 찾기: node tools/balance/run_bal.js tools/balance/day_search.js
//   요일 · 난이도 · 인원(1 ~ 4)마다 체력 배율을 찾아 「최대로 갖춘 학생이 그 난이도 목표 레벨(30 · 40 · 50)에서 반쯤 이기게」 맞춰요
//   파티: 혼자는 12 직업을 돌아가며 · 2 명 기사 + 성직자 · 3 명 기사 + 흑마법사 + 성직자 · 4 명 전사 + 기사 + 흑마법사 + 성직자
//   1) 보스가 거의 안 때릴 때 잡는 데 평균 200 초가 걸리게 체력 배율 · 2) 그다음 이길 확률이 50 % 가 되게 공격 배율 (제한 300 초)
//   결과: tools/balance/out/day_k.json · tools/daydungeon/day_balance.json
const R = require('./raid_cfg.js'), fs = require('fs');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard'];
const PARTY = [null, ['knight', 'cleric'], ['knight', 'black', 'cleric'], ['warrior', 'knight', 'black', 'cleric']];
const ONLY = process.env.DD_ONLY ? JSON.parse(process.env.DD_ONLY) : null;   // 예: [[0,0,1]] 요일 · 난이도 · 인원
module.exports = async (ev, log) => {
  const T = [30, 40, 50], out = fs.existsSync(__dirname + '/out/day_k.json') ? JSON.parse(fs.readFileSync(__dirname + '/out/day_k.json')) : {};
  const sim = (w, lv, n, hK, aK, N, lim) => ev(o => { if (o.solo) o.jobs = it => [o.all[it % 12]]; return __bal.ddSim(o); }, { w, lv, L: T[lv], n: N, lim, K: [hK, aK], ...R.max(T[lv], 'mix'), ...(n === 1 ? { solo: 1, all: ALL } : { jobs: PARTY[n - 1] }) });
  for (let w = 0; w < 5; w++) for (let lv = 0; lv < 3; lv++) for (let n = 1; n <= 4; n++){
    if (ONLY && !ONLY.some(x => x[0] === w && x[1] === lv && x[2] === n)) continue;
    let lo = .02, hi = 50; for (let k = 0; k < 12; k++){ const m = Math.sqrt(lo * hi), r = await sim(w, lv, n, m, .001, 24, 2000); if (r.t < 200) lo = m; else hi = m; } const hK = +Math.sqrt(lo * hi).toFixed(3);
    lo = .05; hi = 40; for (let k = 0; k < 11; k++){ const m = Math.sqrt(lo * hi), r = await sim(w, lv, n, hK, m, 60, 300); if (r.win > .5) lo = m; else hi = m; } const aK = +Math.sqrt(lo * hi).toFixed(3), v = await sim(w, lv, n, hK, aK, 300, 300);
    out[`${w}_${lv}_${n}`] = { hK, aK, ...v }; log(JSON.stringify({ w, lv, n, hK, aK, ...v })); fs.writeFileSync(__dirname + '/out/day_k.json', JSON.stringify(out));
  }
  fs.writeFileSync(__dirname + '/../daydungeon/day_balance.json', JSON.stringify(out, null, 1));
};
