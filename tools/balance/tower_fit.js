// 시련의 탑 층마다 직업별 유리 · 보통 · 불리 뱃지: node tools/balance/run_bal.js tools/balance/tower_fit.js [포트]
//   그 층 기준 레벨 · 장비로 직업마다 TW_N 판 (기본 20) → 승률 85 % 이상 유리 (g) · 50 % 미만 불리 (b) · 그 사이 보통 (n)
//   결과: out/tw_fit.json { 층: 'gnb…' (TW_FJ 순서) , 층_w: [승률…] }  (환경 변수 TW_FL="1-10")
const fs = require('fs');
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
module.exports = async (ev, log) => {
  const [a, b] = (process.env.TW_FL || '1-50').split('-').map(Number), OUTF = __dirname + '/out/' + (process.env.TW_OUT || 'tw_fit.json'), out = fs.existsSync(OUTF) ? JSON.parse(fs.readFileSync(OUTF)) : {};
  for (let f = a; f <= (b || a); f++){ const v = await ev(o => __bal.twSim(o), { f, n: +(process.env.TW_N || 20), lim: 300, jobs: ALL });
    const w = ALL.map(j => +v.per[j].toFixed(2)); out[f] = w.map(x => x >= .85 ? 'g' : x < .5 ? 'b' : 'n').join(''); out[f + '_w'] = w; log(f, out[f], v.win); fs.writeFileSync(OUTF, JSON.stringify(out)); }
};
