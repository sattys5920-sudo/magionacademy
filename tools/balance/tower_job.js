// 시련의 탑 직업 배율 찾기: node tools/balance/run_bal.js tools/balance/tower_job.js [포트]
//   직업마다 몬스터 세기 배율 m 을 찾아요: 여러 층 (부류가 고르게 섞이게) 평균 승률이 TW_TGT (기본 75 %) 가 되게 · 층 세기는 out/tw_k.json
//   결과: out/tw_jm.json  (환경 변수 TW_JOBS="cleric,bard" 로 일부만)
const fs = require('fs'), K = JSON.parse(fs.readFileSync(__dirname + '/out/tw_k.json'));
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
const FL = [3, 6, 9, 11, 14, 16, 19, 22, 24, 27, 29, 31, 33, 35, 38, 41, 43, 46, 48, 50], TGT = +(process.env.TW_TGT || .75);
module.exports = async (ev, log) => {
  const OUTF = __dirname + '/out/' + (process.env.TW_JOUT || 'tw_jm.json'), out = fs.existsSync(OUTF) ? JSON.parse(fs.readFileSync(OUTF)) : {};
  const jobs = process.env.TW_JOBS ? process.env.TW_JOBS.split(',') : ALL;
  const sim = async (job, m, n) => { let w = 0; for (const f of FL){ const r = await ev(o => __bal.twSim(o), { f, K: [K[f].hK, K[f].aK], n, lim: 300, jobs: [job], JM: { [job]: m } }); w += r.win; } return w / FL.length; };
  for (const job of jobs){ let lo = .08, hi = 12; for (let k = 0; k < 9; k++){ const m = Math.sqrt(lo * hi), w = await sim(job, m, 3); if (w > TGT) lo = m; else hi = m; } const m = +Math.sqrt(lo * hi).toFixed(3), v = await sim(job, m, 6);
    out[job] = m; log(JSON.stringify({ job, m, win: +v.toFixed(2) })); fs.writeFileSync(OUTF, JSON.stringify(out)); }
};
