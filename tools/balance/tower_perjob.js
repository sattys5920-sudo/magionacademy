// 시련의 탑 층마다 직업별 승률 보기: TW_FL="4,12,40" node tools/balance/run_bal.js tools/balance/tower_perjob.js [포트]
const fs = require('fs'), K = JSON.parse(fs.readFileSync(__dirname + '/out/tw_k.json'));
const ALL = ['warrior', 'knight', 'thief', 'black', 'summon', 'gadget', 'alch', 'time', 'white', 'druid', 'cleric', 'bard', 'paladin', 'guardian', 'darkknight', 'dancer', 'sage', 'shaman', 'miko', 'archer', 'gunner', 'elemental', 'fighter', 'bladedancer'];
module.exports = async (ev, log) => { for (const f of (process.env.TW_FL || '4').split(',').map(Number)){ const k = K[f]; const v = await ev(o => __bal.twSim(o), { f, K: [k.hK, k.aK], n: 20, lim: 300, jobs: ALL }); log(f, JSON.stringify(Object.fromEntries(Object.entries(v.per).map(([j, w]) => [j, +w.toFixed(2)])))); } };
