// 탐사 모의 전투 공통 설정: 장면(일반 · 강한 몬스터 · 보스 · 레벨) · 파티(혼자 · 2~5 명) · 기준 cfg(예전 가정: 무기 황금(동굴)·미스릴(신전) + 그 레벨 방어구) · 최대 버프 cfg
// 공통: 탐사 시나리오 · 기준(원래 가정) · 최대 버프 cfg
const SC = { 2: [['battle', 30, 30], ['elite', 34, 34], ['boss', 35, 38]], 3: [['battle', 43, 43], ['elite', 45, 45], ['boss', 47, 50]] };
const PT = { solo: null, p2: ['knight', 'white'], p3: ['knight', 'black', 'white'], p4: ['knight', 'black', 'white', 'alch'], p5: ['knight', 'warrior', 'black', 'white', 'summon'] };
const SOLO = ['knight', 'warrior', 'black', 'white', 'summon', 'alch'];
const arCap = L => [10, 20, 30, 40, 48].filter(x => L >= x).length;
const base = (rg, L) => ({ cfg: { wp: rg === 2 ? 3 : 4, ar: arCap(L) } });
const max = (rg, L, kind) => { const c = a => ({ wp: 4, ar: arCap(L), dfire: 1, dwater: 1, nb: 1, fam: kind === 'boss' ? 'xboss' : 'xmain', acc: a, accSt: 5 }); return { cfgRole: { melee: c('cape'), ranged: c('crown'), heal: c('cape') }, hostPotK: .924 }; };
async function run(ev, rg, kind, L, mL, pt, cfg, m, n) {
  const jobsets = pt === 'solo' ? SOLO.map(j => [j]) : [PT[pt]]; let w = 0, h = 0;
  for (const jobs of jobsets) { const r = await ev(o => __bal.xSim(o), { rg, L, mL, kind, jobs, n, m, pot: 1, ...cfg }); w += r.win; h += r.hp; }
  return { win: +(w / jobsets.length).toFixed(3), hp: +(h / jobsets.length).toFixed(3) };
}
module.exports = { SC, PT, SOLO, arCap, base, max, run };
