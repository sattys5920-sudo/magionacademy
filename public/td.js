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
  const posAt = (z, s) => { const Z = ZONES[z]; s = Math.max(0, Math.min(Z.len, s)); for (let i = 0; i < Z.seg.length; i++){ if (s <= Z.seg[i] || i === Z.seg.length - 1){ const a = Z.path[i], b = Z.path[i + 1], t = Z.seg[i] ? s / Z.seg[i] : 0; return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]; } s -= Z.seg[i]; } return Z.path[Z.path.length - 1]; };
  // 직업 → 역할 (근접 · 원거리 · 치유)
  const CAT = { warrior: 'melee', knight: 'melee', thief: 'melee', black: 'ranged', summon: 'ranged', gadget: 'ranged', alch: 'ranged', time: 'ranged', white: 'heal', druid: 'heal', cleric: 'heal', bard: 'heal' };
  // 스킬 2개 + 기본 공격. 올릴 수 있는 것: pow(공격력/치유량/지속) · rng(사거리/범위) · cd(쿨타임 감소)
  const SK = {
    melee: [{ n: '강타', t: 'hit', pow: 70, rng: 15, cd: 2.2, tg: 1 }, { n: '막기', t: 'slow', pow: .6, rng: 18, cd: 8, dur: 3 }],
    ranged: [{ n: '마법탄', t: 'hit', pow: 50, rng: 30, cd: 2.4, tg: 1 }, { n: '폭발', t: 'aoe', pow: 75, rng: 26, cd: 7, rad: 12 }],
    heal: [{ n: '치유의 빛', t: 'eggheal', pow: 14, rng: 99, cd: 9 }, { n: '응원', t: 'buff', pow: .25, rng: 40, cd: 12, dur: 5 }],
  };
  const UP_COST = [200, 350, 550, 800], UP_MAX = 5, UP_PER = { pow: .25, rng: .12, cd: .08 };
  // 웨이브: 1~15, 차수(1·2·3)마다 세져요. 일반(1·2) · 정예(3·4) · 보스(5)
  const TIER_HP = [1, 2.4, 4.6], TIER_GOLD = [[8, 30, 150], [10, 40, 150], [14, 55, 300]];
  const MON = { n: { hp: 70, spd: 7.5, egg: 8 }, e: { hp: 260, spd: 6.5, egg: 22 }, b: { hp: 1100, spd: 4.8, egg: 60 } };
  function waveDef(w){   // w: 1~15 → [종류, 마릿수, 간격(초)] 목록
    const tier = Math.floor((w - 1) / 5), k = (w - 1) % 5;
    if (k < 2) return { tier, list: [['n', 8 + tier * 3 + k * 2, .9]] };
    if (k < 4) return { tier, list: [['e', 3 + tier * 2 + (k - 2), 2.4], ['n', 6 + tier * 2, .8]] };
    return { tier, list: [['b', 1, 1], ['n', 6 + tier * 3, .9], ['e', 2 + tier, 2.4]] };
  }
  function newState(players, opt){   // players: [{ uid, zone(0~2), slot, job }]
    opt = opt || {};
    const S = { t: 0, wave: 0, phase: 'ready', rest: 0, mons: [], q: [], nid: 1, eggs: [100, 100, 100], leaks: 0, players: {}, hpK: opt.hpK || 1, hpN: Math.max(1, players.length) / 9, log: [] };
    players.forEach(p => { S.players[p.uid] = { uid: p.uid, zone: p.zone, slot: p.slot, job: p.job, cat: CAT[p.job] || 'melee', gold: 0, earned: 0, up: [{ pow: 0, rng: 0, cd: 0 }, { pow: 0, rng: 0, cd: 0 }], cd: [0, 0], buff: 0, basic: 0 }; });
    return S;
  }
  const skillOf = (p, i) => { const b = SK[p.cat][i], u = p.up[i]; return { ...b, pow: b.pow * (1 + UP_PER.pow * u.pow), rng: b.rng * (1 + UP_PER.rng * u.rng), cd: Math.max(.6, b.cd * (1 - UP_PER.cd * u.cd)), dur: b.dur ? b.dur * (1 + UP_PER.pow * u.pow) : undefined, rad: b.rad ? b.rad * (1 + UP_PER.rng * u.rng) : undefined }; };
  const upCost = (p, i, k) => p.up[i][k] >= UP_MAX - 1 ? null : UP_COST[p.up[i][k]];
  function upgrade(S, uid, i, k){ const p = S.players[uid], c = p && upCost(p, i, k); if (!p || c == null || p.gold < c) return false; p.gold -= c; p.up[i][k]++; return true; }
  function startWave(S){ if (S.phase === 'over' || S.wave >= 15) return false; S.wave++; const d = waveDef(S.wave); S.phase = 'wave'; S.tier = d.tier; S.q = []; let t = 0; d.list.forEach(([type, n, gap]) => { for (let i = 0; i < n; i++){ S.q.push({ at: t, type }); t += gap; } t += 1.5; }); S.q.sort((a, b) => a.at - b.at); S.wt = 0; S.spawned = 0; S.total = S.q.length; return true; }
  function spawn(S, type){ const m = MON[type], tier = S.tier, wk = 1 + ((S.wave - 1) % 5) * .06, hp = Math.round(m.hp * TIER_HP[tier] * wk * S.hpN * S.hpK); S.mons.push({ id: S.nid++, type, zone: 0, s: 0, hp, mhp: hp, spd: m.spd * (1 + tier * .06), egg: m.egg * (1 + tier * .35), slow: 0, slowT: 0, gold: Math.round(TIER_GOLD[tier][type === 'n' ? 0 : type === 'e' ? 1 : 2] * K.gold) }); }
  const K = { gold: 3, dmg: 1, bonus: 30 };   // 균형 조절용
  const alive = S => S.mons.filter(m => m.hp > 0);
  function hurt(S, m, dmg, by){ if (m.hp <= 0) return; m.hp -= dmg * K.dmg; if (m.hp <= 0 && by){ by.gold += m.gold; by.earned += m.gold; } }
  function step(S, dt){
    if (S.phase === 'over' || S.phase === 'ready') return;
    S.t += dt;
    if (S.phase === 'wave'){ S.wt += dt; while (S.q.length && S.q[0].at <= S.wt){ spawn(S, S.q.shift().type); S.spawned++; } }
    // 몬스터 이동 (막기 중이면 느려져요)
    S.mons.forEach(m => { if (m.hp <= 0) return; if (m.slowT > 0){ m.slowT -= dt; if (m.slowT <= 0) m.slow = 0; } m.s += m.spd * (1 - m.slow) * dt;
      while (m.s >= ZONES[m.zone].len){ if (m.zone === 2){ // 알이 맞아요
          const e = S.eggs.findIndex(v => v > 0); if (e >= 0){ S.eggs[e] = Math.max(0, S.eggs[e] - m.egg); } S.leaks++; m.hp = 0; m.leak = 1; break; }
        m.s -= ZONES[m.zone].len; m.zone++; } });
    // 스킬 (쿨타임이 차면 알아서)
    Object.values(S.players).forEach(p => {
      p.buff = Math.max(0, p.buff - dt); const pos = ZONES[p.zone].slots[p.slot], mult = p.buff > 0 ? 1.25 : 1;
      const near = (rng) => alive(S).filter(m => m.zone === p.zone && Math.hypot(posAt(m.zone, m.s)[0] - pos[0], posAt(m.zone, m.s)[1] - pos[1]) <= rng);
      // 기본 공격 (아주 약해요, 1초에 한 번)
      p.basic -= dt; if (p.basic <= 0){ const t = near(p.cat === 'melee' ? 12 : 24).sort((a, b) => b.s - a.s)[0]; if (t){ hurt(S, t, 9 * mult, p); p.basic = 1; } else p.basic = .25; }
      for (let i = 0; i < 2; i++){ p.cd[i] -= dt; if (p.cd[i] > 0) continue; const s = skillOf(p, i);
        if (s.t === 'hit'){ const t = near(s.rng).sort((a, b) => b.s - a.s)[0]; if (t){ hurt(S, t, s.pow * mult, p); p.cd[i] = s.cd; } }
        else if (s.t === 'aoe'){ const ts = near(s.rng).sort((a, b) => b.s - a.s); if (ts[0]){ const c = posAt(ts[0].zone, ts[0].s); ts.filter(m => { const q = posAt(m.zone, m.s); return Math.hypot(q[0] - c[0], q[1] - c[1]) <= s.rad; }).forEach(m => hurt(S, m, s.pow * mult, p)); p.cd[i] = s.cd; } }
        else if (s.t === 'slow'){ const ts = near(s.rng); if (ts.length){ ts.forEach(m => { m.slow = Math.max(m.slow, s.pow); m.slowT = Math.max(m.slowT, s.dur); }); p.cd[i] = s.cd; } }
        else if (s.t === 'eggheal'){ const e = S.eggs.findIndex(v => v > 0 && v < 100); if (e >= 0){ S.eggs[e] = Math.min(100, S.eggs[e] + s.pow); p.cd[i] = s.cd; } }
        else if (s.t === 'buff'){ Object.values(S.players).forEach(q => { if (q.zone === p.zone && Math.hypot(ZONES[q.zone].slots[q.slot][0] - pos[0], ZONES[q.zone].slots[q.slot][1] - pos[1]) <= s.rng) q.buff = Math.max(q.buff, s.dur); }); p.cd[i] = s.cd; } } });
    S.mons = S.mons.filter(m => m.hp > 0);
    if (!S.eggs.some(v => v > 0)){ S.phase = 'over'; S.win = false; return; }
    if (S.phase === 'wave' && !S.q.length && !S.mons.length){   // 웨이브 끝: 막은 보너스 · 쉬는 시간
      Object.values(S.players).forEach(p => { p.gold += S.wave * K.bonus; p.earned += S.wave * K.bonus; });
      if (S.wave >= 15){ S.phase = 'over'; S.win = true; } else { S.phase = 'rest'; S.rest = S.wave % 5 === 0 ? 60 : 30; } }
    else if (S.phase === 'rest'){ S.rest -= dt; if (S.rest <= 0) startWave(S); }
  }
  return { K, W, H, ZONES, CAT, SK, UP_COST, UP_MAX, waveDef, newState, startWave, step, upgrade, upCost, skillOf, posAt };
});
