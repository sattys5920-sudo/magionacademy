// 레이드 모의 전투 (게임 전투 코드를 그대로 써요): 모의 사이트 index.html 끝에 붙여서 window.__raidSim(o) 로 돌려요
//   o = { L 레벨, b 보스 0~3, s 세기 배율, n 판 수, hpK 체력 기준, atK 공격 기준, wp 무기, ar 방어구, lim 제한 시간(초) }
//   12 명 = 직업 12 개 하나씩 (앞쪽 6 · 뒤쪽 6) · 사람마다 물약 2 개 · 피하기는 완벽 30 % (20 %) · 조금 어긋남 40 % (60 %) · 놓침 30 % (100 %)
window.__raidSim = (o) => {
  const N = o.n || 40, L = o.L, lim = o.lim || 300, res = { win: 0, t: [], left: [], dead: [], acts: 0 };
  const JOBS = ['knight', 'warrior', 'thief', 'white', 'black', 'bard', 'knight', 'summon', 'alch', 'druid', 'time', 'cleric', 'gadget', 'warrior'].slice(0, 0);
  const SIDE = [['knight', 'white', 'black', 'warrior', 'thief', 'bard'], ['cleric', 'summon', 'druid', 'time', 'alch', 'gadget']];   // 적은 인원도 치유사가 들어가게
  const dodge = () => { const r = Math.random(); return r < .3 ? .2 : r < .7 ? .6 : 1; };
  for (let it = 0; it < N; it++){
    const party = [];
    const SZ = o.size || 12; SIDE.forEach((js, side) => js.slice(0, side ? Math.floor(SZ / 2) : Math.ceil(SZ / 2)).forEach((job, j) => {
      const sk = { '0_0': 1 }; { let pts = xSkp(L); for (let lv = 1; lv <= XMAXLV && pts > 0; lv++) for (let r = 0; r < 5 && pts > 0; r++) for (let b = 0; b < 3 && pts > 0; b++){ const k = b + '_' + r; if ((sk[k] || 0) < lv){ sk[k] = lv; pts--; } } }
      const u = xMkUnit(job, L, job + side + j, true, undefined, undefined, sk); u.id = 'p' + side + j;
      const wm = (1 + .08 * (o.wp || 0)) / (1 + .08 * Math.min(4, Math.floor((L - 1) / 12))); ['atk', 'mag', 'heal'].forEach(k => { u[k] = Math.round(u[k] * wm); });
      const A = XAV[o.ar || 0]; u.mhp = Math.round(u.mhp * (1 + A[0])); u.dr += A[1]; u.hp = u.mhp; u.mp = u.mmp; u.cdn = {}; u.row = XROLE[job] === 'melee' ? 'f' : 'b'; u.pot = 2; u.side = side; party.push(u); }));
    const bL = o.bL || L, f = (1 + .35 * (bL - 1)) * XFOE, a = (1 + .25 * (bL - 1)) * XFOE_A;   // bL: 보스 레벨 (층 레벨) · L: 학생 레벨
    const boss = { id: 'e0', name: '보스', ic: '', lp: 16, big: 1, sc: 3, hh: 168, team: 'e', mhp: Math.round(o.hpK * f * o.s), atk: Math.round(o.atK * a * (o.am ?? Math.sqrt(o.s))), spd: o.spd || 12, g: 30, k: 8, aoe: false, sk: '', skn: '', mL: L, fx: {} };
    boss.hp = boss.mhp;
    const B = xb = { party, foes: [boss], kind: 'boss', log: '', turn: null, pick: null, over: false, last: 0, buff: false, def: {}, fxs: [], floats: [], proj: [], n0: 1 };
    let t = 0, fin = '', bc = 0, big = null; const dt = .25;
    const hitSome = (L2, k, fx) => L2.forEach(tg => { if (tg.hp <= 0) return; xHit(boss, tg, boss.atk * k * (.85 + Math.random() * .3) * dodge(), '#ff6a6a'); if (tg.hp > 0 && fx) fx(tg); });
    const bfx = [t2 => { t2.fx.slow = { v: .3, t: 8 }; }, t2 => { t2.fx.dot = { v: Math.max(1, Math.round(boss.atk * .25)), t: 8, acc: 0 }; }, t2 => { t2.fx.vuln = { v: .15, t: 8 }; }, t2 => { t2.g = Math.min(t2.g, -20); }][o.b || 0];
    while (t < lim){ t += dt;
      if (!xAlive(party).length){ fin = 'wipe'; break; }
      party.concat(B.foes).forEach(x => { if (x.hp <= 0) return; if (x.team === 'a' && x.mp < x.mmp) x.mp = Math.min(x.mmp, x.mp + dt * (.6 + x.L * .03) * (XMPR[XROLE[x.job]] || 1)); x.g = Math.min(100, x.g + x.spd * (1 + xFm(x, 'spd') - xFm(x, 'slow')) * XGSPD * dt); const fx = x.fx; for (const k in fx){ fx[k].t -= dt; if (k === 'dot'){ fx[k].acc = (fx[k].acc || 0) + dt; while (fx[k].acc >= 2 && fx[k].t > -2){ fx[k].acc -= 2; x.hp = Math.max(0, x.hp - fx[k].v); } } if (k === 'regen'){ fx[k].acc = (fx[k].acc || 0) + dt; while (fx[k].acc >= 2){ fx[k].acc -= 2; x.hp = Math.min(x.mhp, x.hp + fx[k].v); } } if (fx[k].t <= 0) delete fx[k]; } xPets(x, dt); });
      // 레이드 보스 저항: 느려짐 15 % · 약해짐 15 % · 실명 10 % 까지만 들어가요 (12 명이 겹쳐 걸어도)
      [['slow', .15], ['weak', .15], ['blind', .1]].forEach(([k, m]) => { if (boss.fx[k] && boss.fx[k].v > m) boss.fx[k].v = m; });
      if (big && t >= big.at){   // 큰 기술: 준비 중에 체력 8 % 이상 깎으면 끊겨요
        if (big.hp0 - boss.hp >= boss.mhp * .08){ boss.g = 0; } else hitSome(xAlive(party), 2.0, bfx);
        big = null; }
      const g0 = boss.g; let acted = false;
      for (const x of party.concat(B.foes)){ if (x.hp <= 0 || x.g < 100) continue;
        if (x.team === 'e'){ x.g = 0; acted = true; if (big) continue; bc++; const ph = boss.hp / boss.mhp > .7 ? 1 : boss.hp / boss.mhp > .35 ? 2 : 3, A2 = xAlive(party);
          if (ph === 3 && bc % 4 === 0){ big = { at: t + 6, hp0: boss.hp }; continue; }                 // 큰 기술 준비 (6 초)
          if (ph >= 2 && bc % 3 === 0){ hitSome(A2, .55, bfx); continue; }                              // 전체 공격
          if (bc % 2 === 0){ const sd = Math.random() < .5 ? 0 : 1; hitSome(A2.filter(p => p.side === sd), .9, bfx); continue; }   // 한쪽 공격
          const tg = xFoeTarget() || A2[0]; if (!tg || tg.hp <= 0) continue; xHit(boss, tg, boss.atk * 1.5 * (.85 + Math.random() * .3) * dodge(), '#ff6a6a'); continue; }   // 한 명 세게
        if (x.pot > 0 && x.hp / x.mhp < .35){ x.pot--; x.hp = Math.min(x.mhp, x.hp + Math.round(x.mhp * .5)); x.g = 0; } else xAI(x);
        if (boss.hp <= 0) break; }
      if (!acted && boss.g < g0 - 8) boss.g = g0 - 8;   // 지연을 여러 번 맞아도 한 번에 8 칸까지만 밀려요
      if (boss.hp <= 0){ fin = 'win'; break; } }
    res.acts += bc; if (fin === 'win') res.win++; res.t.push(t); res.left.push(Math.max(0, boss.hp) / boss.mhp); res.dead.push(party.filter(p => p.hp <= 0).length);
  }
  xb = null; const avg = a => +(a.reduce((x, y) => x + y, 0) / a.length).toFixed(2);
  return { acts: +(res.acts / N).toFixed(1), win: res.win / N, t: avg(res.t), left: avg(res.left), dead: avg(res.dead) };
};
