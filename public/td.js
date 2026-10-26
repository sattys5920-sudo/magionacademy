// 이벤트 「용의 알 지키기」 디펜스 엔진 — 화면·네트워크와 상관없는 계산만 (브라우저와 node 둘 다에서 돌아요)
//   상태는 평범한 객체라서 그대로 DB에 올릴 수 있고, step(S, dt) 한 번이 dt초만큼 시간을 흘려요.
(function (root, f) { const T = f(); if (typeof module !== 'undefined' && module.exports) module.exports = T; else root.TD = T; })(this, function () {
  const W = 130, H = 147;   // 지도 칸 (그림과 같은 좌표)
  // 장소 3곳: 길(꺾이는 점)과 서는 자리 6곳
  const ZONES = [
    { id: 'forest', name: '숲길', path: [[100, -8], [100, 26], [30, 34], [30, 68], [100, 76], [100, 104], [62, 112], [62, 156]], slots: [[64, 16], [10, 52], [66, 53], [114, 50], [76, 92], [28, 98]] },
    { id: 'cave', name: '둥지 입구', path: [[-8, 24], [88, 28], [88, 64], [34, 72], [34, 104], [88, 112], [88, 132], [64, 150]], slots: [[52, 10], [110, 48], [62, 46], [10, 90], [62, 90], [112, 98]] },
    { id: 'nest', name: '둥지 앞', path: [[24, -8], [24, 34], [98, 44], [98, 84], [40, 94], [40, 106], [64, 112]], slots: [[60, 22], [10, 66], [62, 68], [114, 62], [88, 112], [112, 98]] },
  ];
  ZONES.forEach(z => { z.seg = []; z.len = 0; for (let i = 1; i < z.path.length; i++) { const a = z.path[i - 1], b = z.path[i], l = Math.hypot(b[0] - a[0], b[1] - a[1]); z.seg.push(l); z.len += l; } });
  const segD = (px, py, a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], l = dx * dx + dy * dy; let t = l ? ((px - a[0]) * dx + (py - a[1]) * dy) / l : 0; t = Math.max(0, Math.min(1, t)); return Math.hypot(px - a[0] - dx * t, py - a[1] - dy * t); };
  ZONES.forEach(z => { z.d0 = z.slots.map(q => { let m = 1e9; for (let i = 1; i < z.path.length; i++) m = Math.min(m, segD(q[0], q[1], z.path[i - 1], z.path[i])); return Math.round(m * 10) / 10; }); });   // 자리마다 가장 가까운 길까지 거리
  const posAt = (z, s) => { const Z = ZONES[z]; s = Math.max(0, Math.min(Z.len, s)); for (let i = 0; i < Z.seg.length; i++){ if (s <= Z.seg[i] || i === Z.seg.length - 1){ const a = Z.path[i], b = Z.path[i + 1], t = Z.seg[i] ? s / Z.seg[i] : 0; return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]; } s -= Z.seg[i]; } return Z.path[Z.path.length - 1]; };
  // 직업 → 역할 (근접 · 원거리 · 치유)
  const CAT = { warrior: 'melee', knight: 'melee', thief: 'melee', black: 'ranged', summon: 'ranged', gadget: 'ranged', alch: 'ranged', time: 'ranged', white: 'heal', druid: 'heal', cleric: 'heal', bard: 'heal' };
  // 이벤트 전용 스킬 2개 (직업·레벨·습득과 상관없이 모두 똑같아요) + 기본 공격
  //   1 가까운 한 명에게 센 공격 · 2 넓은 범위 모두에게 약한 공격. 올릴 수 있는 것: pow(공격력) · rng(사거리/범위) · cd(쿨타임 감소)
  const SKA = [{ n: '일격', t: 'hit', pow: 95, rng: 18, cd: 3 }, { n: '번개비', t: 'aoe', pow: 32, rng: 55, cd: 7 }];
  const SK = { melee: SKA, ranged: SKA, heal: SKA };
  const UP_COST = [200, 350, 550, 800], UP_MAX = 5, UP_PER = { pow: .25, rng: .12, cd: .08 };
  // 웨이브: 1~15, 차수(1·2·3)마다 세져요. 일반(1·2) · 정예(3·4) · 보스(5)
  const TIER_HP = [1, 2.4, 4.6], TIER_GOLD = [[8, 30, 150], [10, 40, 150], [14, 55, 300]];
  const MON = { n: { hp: 70, spd: 10.5, egg: 8 }, e: { hp: 260, spd: 9, egg: 22 }, b: { hp: 1100, spd: 6.7, egg: 60 } };
  const WAVE_TAB = [[20, 0, 0], [40, 0, 0], [20, 20, 0], [30, 20, 0], [30, 30, 1], [30, 0, 0], [40, 0, 0], [30, 20, 0], [30, 30, 0], [30, 40, 1], [40, 0, 0], [50, 0, 0], [40, 30, 0], [40, 40, 0], [50, 50, 2]];   // 웨이브별 [일반, 정예, 보스] 마릿수
  function waveDef(w){   // w: 1~15 → [종류, 마릿수, 간격(초)] 목록
    const tier = Math.floor((w - 1) / 5), [n, e, b] = WAVE_TAB[w - 1], list = [];
    if (b) list.push(['b', b, 4]); if (n) list.push(['n', n, .5]); if (e) list.push(['e', e, 1.1]);
    return { tier, list };
  }
  function newState(players, opt){   // players: [{ uid, zone(0~2), slot, job }]
    opt = opt || {};
    const S = { t: 0, wave: 0, phase: 'ready', rest: 0, mons: [], q: [], nid: 1, eggs: [100, 100, 100], leaks: 0, players: {}, hpK: opt.hpK || 1, hpN: Math.max(1, players.length) / 9, log: [], fx: [], kz: [0, 0, 0] };
    players.forEach(p => { S.players[p.uid] = { uid: p.uid, zone: p.zone, slot: p.slot, job: p.job, cat: CAT[p.job] || 'melee', gold: 0, earned: 0, up: [{ pow: 0, rng: 0, cd: 0 }, { pow: 0, rng: 0, cd: 0 }], cd: [0, 0], buff: 0, basic: 0, ready: 0, auto: opt.auto !== undefined ? opt.auto : 1 }; });
    S.autoReady = opt.auto !== undefined ? !!opt.auto : true;
    return S;
  }
  const skillOf = (p, i) => { const b = SK[p.cat][i], u = p.up[i]; return { ...b, pow: b.pow * (1 + UP_PER.pow * u.pow), rng: b.rng * (1 + UP_PER.rng * u.rng), cd: Math.max(.6, b.cd * (1 - UP_PER.cd * u.cd)) }; };
  const upCost = (p, i, k) => p.up[i][k] >= UP_MAX - 1 ? null : UP_COST[p.up[i][k]];
  function seat(S, uid, zone, slot, job){   // 자리 고르기 · 새로 들어오기 · 자리 옮기기 (이미 앉은 사람이 있으면 못 앉아요)
  if (S.phase === 'wave' || S.phase === 'over') return false; if (Object.values(S.players).some(q => q.uid !== uid && q.zone === zone && q.slot === slot)) return false;
  let p = S.players[uid]; if (!p){ p = S.players[uid] = { uid, gold: 0, earned: 0, up: [{ pow: 0, rng: 0, cd: 0 }, { pow: 0, rng: 0, cd: 0 }], cd: [0, 0], buff: 0, basic: 0, ready: 0, auto: 0 }; }
  p.zone = zone; p.slot = slot; p.job = job; p.cat = CAT[job] || 'melee'; p.ready = 0; return true; }
function unseat(S, uid){ if (S.phase !== 'wave') delete S.players[uid]; }
const setReady = (S, uid, v) => { const p = S.players[uid]; if (p && (S.phase === 'ready' || S.phase === 'rest')) p.ready = v ? 1 : 0; };
const allReady = S => { const a = Object.values(S.players); return a.length > 0 && a.every(q => q.ready); };
function upgrade(S, uid, i, k){ const p = S.players[uid], c = p && upCost(p, i, k); if (!p || c == null || p.gold < c) return false; p.gold -= c; p.up[i][k]++; return true; }
  function startWave(S){ if (S.phase === 'over' || S.wave >= 15) return false; S.wave++; Object.values(S.players).forEach(q => { q.ready = 0; }); { const n = Object.keys(S.players).length / 9; S.hpN = n >= 1 ? n : Math.max(.3, Math.pow(n, 1.15)); } const cf = .85 + .15 * Math.min(2, Math.max(1, S.hpN)), d = waveDef(S.wave); S.phase = 'wave'; S.tier = d.tier; S.q = []; let t = 0; d.list.forEach(([type, n0, gap]) => { const n = n0; for (let i = 0; i < n; i++){ S.q.push({ at: t, type }); t += gap; } t += 1.5; }); S.q.sort((a, b) => a.at - b.at); S.wt = 0; S.spawned = 0; S.total = S.q.length; return true; }
  function spawn(S, type){ const m = MON[type], tier = S.tier, wk = 1 + ((S.wave - 1) % 5) * .06, hp = Math.round(m.hp * TIER_HP[tier] * wk * S.hpN * S.hpK * K.hp); S.mons.push({ id: S.nid++, type, zone: 0, s: 0, hp, mhp: hp, spd: m.spd * (1 + tier * .06), egg: m.egg * (1 + tier * .35), slow: 0, slowT: 0, gold: Math.round(TIER_GOLD[tier][type === 'n' ? 0 : type === 'e' ? 1 : 2] * K.gold) }); }
  const K = { gold: 3, dmg: 1.15, bonus: 30, hp: 2.1, egg: .08, basic: 10, reach: 16 };   // 균형 조절용
  const alive = S => S.mons.filter(m => m.hp > 0);
  function hurt(S, m, dmg, by, kind){ if (m.hp <= 0) return; if (by && S.fx) S.fx.push([by.uid, m.id, kind || 0]); m.hp -= dmg * K.dmg; if (m.hp <= 0 && by){ by.gold += m.gold; by.earned += m.gold; if (S.kz) S.kz[by.zone]++; } }
  const nearOf = (S, p, rng) => { const pos = ZONES[p.zone].slots[p.slot], R = rng + ZONES[p.zone].d0[p.slot]; return alive(S).filter(m => m.zone === p.zone && (m.atk || Math.hypot(posAt(m.zone, m.s)[0] - pos[0], posAt(m.zone, m.s)[1] - pos[1]) <= R)); };   // 알을 때리는 중인 몬스터는 둥지 앞 자리 누구든 때릴 수 있어요 · 사거리는 가장 가까운 길에서부터 재요 (어느 자리든 길 가까이에는 닿아요)
  // 스킬 쓰기: 성공하면 true, 못 쓰면 이유('cd' 쿨타임 · 'none' 쏠 곳이 없음 · 'wave' 웨이브가 아님)
  function cast(S, uid, i){
    const p = S.players[uid]; if (!p || S.phase !== 'wave') return 'wave'; if (p.cd[i] > 0) return 'cd';
    const s = skillOf(p, i), pos = ZONES[p.zone].slots[p.slot], ts = nearOf(S, p, s.rng); if (!ts.length) return 'none';
    const dist = m => { const q = posAt(m.zone, m.s); return Math.hypot(q[0] - pos[0], q[1] - pos[1]); };
    if (s.t === 'hit') hurt(S, ts.sort((a, b) => dist(a) - dist(b))[0], s.pow, p, 1);   // 가까운 한 명에게 센 공격
    else ts.forEach(m => hurt(S, m, s.pow, p, 2));   // 넓은 범위 모두에게 약한 공격
    p.cd[i] = s.cd; return true;
  }
  function step(S, dt){
    if (S.phase === 'over') return;
    if (S.phase === 'ready' || S.phase === 'rest'){ if (S.autoReady) Object.values(S.players).forEach(q => { q.ready = 1; }); if (allReady(S)) startWave(S); return; }   // 자리를 정하고 모두가 시작을 누르면 웨이브가 와요
    S.t += dt;
    if (S.phase === 'wave'){ S.wt += dt; while (S.q.length && S.q[0].at <= S.wt){ spawn(S, S.q.shift().type); S.spawned++; } }
    // 몬스터 이동 (막기 중이면 느려져요)
    S.mons.forEach(m => { if (m.hp <= 0) return; if (m.slowT > 0){ m.slowT -= dt; if (m.slowT <= 0) m.slow = 0; }
      if (m.atk){ const e = S.eggs.findIndex(v => v > 0); if (e >= 0) S.eggs[e] = Math.max(0, S.eggs[e] - m.egg * K.egg * dt); return; }   // 알 앞에 닿은 몬스터는 알을 때려요 (죽일 때까지)
      m.s += m.spd * (1 - m.slow) * dt;
      while (m.s >= ZONES[m.zone].len){ if (m.zone === 2){ m.s = ZONES[2].len; m.atk = 1; S.leaks++; break; }   // 마지막 곳도 지나면 알에 닿아요
        m.s -= ZONES[m.zone].len; m.zone++; } });   // 앞 곳에서 못 잡은 몬스터는 다음 곳으로 가요
    // 기본 공격은 늘 알아서 · 스킬은 직접 누르거나(cast) 「자동」을 켠 사람만 쿨타임이 차면 알아서
    Object.values(S.players).forEach(p => {
      p.buff = Math.max(0, p.buff - dt); const pos = ZONES[p.zone].slots[p.slot], mult = p.buff > 0 ? 1.25 : 1;
      p.basic -= dt; if (p.basic <= 0){ const t = nearOf(S, p, K.reach).sort((a, b) => b.s - a.s)[0]; if (t){ hurt(S, t, K.basic * mult, p, 0); p.basic = 2; } else p.basic = .2; }   // 직업 상관없이 사거리 같고 2초에 한 번
      for (let i = 0; i < 2; i++){ p.cd[i] -= dt; if (p.auto && p.cd[i] <= 0) cast(S, p.uid, i); } });
    S.mons = S.mons.filter(m => m.hp > 0);
    if (!S.eggs.some(v => v > 0)){ S.phase = 'over'; S.win = false; return; }
    if (S.phase === 'wave' && !S.q.length && !S.mons.length){   // 웨이브 끝: 막은 보너스 · 쉬는 시간
      Object.values(S.players).forEach(p => { p.gold += S.wave * K.bonus; p.earned += S.wave * K.bonus; });
      if (S.wave >= 15){ S.phase = 'over'; S.win = true; } else { S.phase = 'rest'; S.rest = S.wave % 5 === 0 ? 60 : 30; } }
  }
  const r1 = v => Math.round(v * 10) / 10;
  function snap(S){ const p = {}; Object.values(S.players).forEach(q => { p[q.uid] = [q.zone, q.slot, q.job, Math.round(q.gold), q.up.map(u => [u.pow, u.rng, u.cd]), q.buff > 0 ? 1 : 0, q.cd.map(c => Math.max(0, r1(c))), q.auto ? 1 : 0, q.ready ? 1 : 0]; });
    const out = { t: Math.round(S.t), w: S.wave, ph: S.phase, r: Math.max(0, Math.round(S.rest || 0)), e: S.eggs.map(Math.round), win: S.win ? 1 : 0, left: S.q ? S.q.length : 0, m: S.mons.map(m => [m.id, m.type, m.zone, r1(m.s), Math.max(1, Math.round(m.hp / m.mhp * 100)), m.atk ? 0 : r1(m.spd * (1 - m.slow))]), p, f: S.fx.slice(-24) }; S.fx = []; return out; }
  return { cast, setReady, allReady, K, MON, W, H, ZONES, snap, seat, unseat, CAT, SK, UP_COST, UP_MAX, waveDef, newState, startWave, step, upgrade, upCost, skillOf, posAt };
});
