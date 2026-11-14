// 디펜스 균형 시뮬 (사람처럼 손으로 누르기): node tools/td_sim_h.js <전체 인원> <판 수> <몬스터 체력 배율>
//   스킬: 쿨타임이 차면 반응 시간(0.3 초 + 평균 RX 초) 뒤에 눌러요 · 가끔(DIST) 한눈팔아 5 초 늦어요 · 쏠 곳이 없으면 0.5 초 뒤 다시
//   올리기: UPT 초마다 UPP 확률로 살 수 있는 것 중 하나 · 환경 변수 RX(1) DIST(.1) UPT(5) UPP(.5) GAP
const TD = require('../public/td.js');
if (process.env.GAP) TD.K.gap = +process.env.GAP;
const PER = +process.argv[2] || 12, N = +process.argv[3] || 40, HPK = +process.argv[4] || 1;
const RX = +(process.env.RX || 1), DIST = +(process.env.DIST || .1), UPT = +(process.env.UPT || 5), UPP = +(process.env.UPP || .5);
const JOBS = ['knight', 'white', 'black', 'thief', 'druid', 'gunner'];
function run(seed){ let r = seed; const rnd = () => (r = (r * 16807) % 2147483647) / 2147483647;
  const pl = []; for (let n = 0; n < PER; n++){ const z = n % 3, i = Math.floor(n / 3); pl.push({ uid: z + '_' + i, zone: z, slot: i, job: JOBS[n % 6] }); }
  const S = TD.newState(pl, { hpK: HPK, auto: 0 }); S.autoReady = true; TD.startWave(S); let tt = 0;
  const H = {}; Object.keys(S.players).forEach(u => { H[u] = { w: [null, null], up: rnd() * UPT }; });
  const react = () => .3 + -Math.log(1 - rnd()) * RX + (rnd() < DIST ? 5 : 0);
  while (S.phase !== 'over' && tt < 9000){ TD.step(S, .1); tt += .1;
    if (S.phase !== 'wave') continue;
    Object.values(S.players).forEach(p => { const h = H[p.uid];
      for (let i = 0; i < 2; i++){ if (p.cd[i] > 0){ h.w[i] = null; continue; } if (h.w[i] == null) h.w[i] = react(); h.w[i] -= .1; if (h.w[i] <= 0){ const ok = TD.cast(S, p.uid, i); h.w[i] = ok === true ? null : .5; } }
      h.up -= .1; if (h.up <= 0){ h.up = UPT; if (rnd() < UPP){ const o = []; for (let i = 0; i < 2; i++) for (const k of ['pow', 'rng', 'cd']){ const c = TD.upCost(p, i, k); if (c != null && p.gold >= c) o.push([i, k]); } if (o.length){ const [i, k] = o[rnd() * o.length | 0]; TD.upgrade(S, p.uid, i, k); } } } }); }
  return { win: S.win ? 1 : 0, wave: S.wave, eggs: S.eggs.reduce((a, b) => a + b, 0), t: tt };
}
const R = []; for (let i = 1; i <= N; i++) R.push(run(i * 7919));
const avg = f => Math.round(R.reduce((a, x) => a + f(x), 0) / R.length * 10) / 10;
console.log(`인원 ${PER} 명 hpK ${HPK} 승 ${Math.round(avg(x => x.win) * 100) / 1}% 도달 웨이브 ${avg(x => x.wave)} 남은 알 합 ${avg(x => x.eggs)} 시간(초) ${avg(x => x.t)}`);
