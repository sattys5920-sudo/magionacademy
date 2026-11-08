// 레이드 모의 전투 공통 설정: RB = 버프 반영 전(v1) 층마다 [체력, 일반 공격, 다인 공격] · max() = 최대 버프 12 명 (장신구 조합 LOAD)
const RB = [[88877, 130, 2400], [257188, 210, 4000], [547171, 270, 5200], [871997, 340, 6400]], LV = [15, 25, 35, 45];
const arCap = L => [10, 20, 30, 40, 48].filter(x => L >= x).length;
const LOAD = { cape: { melee: 'cape', ranged: 'cape', heal: 'cape' }, mix: { melee: 'cape', ranged: 'crown', heal: 'cape' }, crown: { melee: 'crown', ranged: 'crown', heal: 'crown' }, mix2: { melee: 'crown', ranged: 'crown', heal: 'cape' }, neck: { melee: 'neck', ranged: 'neck', heal: 'neck' } };
const max = (L, ld = 'mix') => { const c = a => ({ wp: 4, ar: arCap(L), dfire: 1, dwater: 1, nb: 1, fam: 'xboss', acc: a, accSt: 5 }); const T = LOAD[ld]; return { cfgRole: { melee: c(T.melee), ranged: c(T.ranged), heal: c(T.heal) }, hostPotK: .924 }; };
const sim = (ev, f, o) => ev(o => __bal.raidSim(o), { L: LV[f], b: f, hpAbs: RB[f][0], atkAbs: RB[f][1], matk: RB[f][2], ...o });
module.exports = { RB, LV, arCap, max, sim, LOAD };
