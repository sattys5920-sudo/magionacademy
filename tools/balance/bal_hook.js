// 버프 · 장비 최대 가정 밸런스 모의 전투 (게임 전투 코드를 그대로 써요)
//   모의 사이트 index.html 의 큰 <script type="module"> 끝(</script> 바로 앞)에 붙여서 써요 → tools/balance/run_bal.js 가 알아서 붙여요
//   window.__bal.unit(job, L, cfg)   : 동료(AI) 방식 스킬 · 스탯 포인트로 만들고 cfg 의 장비 · 버프를 게임과 같은 순서로 얹어요
//   window.__bal.xSim(o)             : 탐사 한 판 (일반 · 강한 몬스터 · 보스) 승률 · 남은 체력
//   window.__bal.raidSim(o)          : 레이드 12 명 (tools/raid_mock/raidsim_hook.js 를 고쳐 씀: 버프 · 장비 · 물약 배율 · MP 회복 버프)
//   window.__bal.power(job, L, cfg)  : 허수아비 상대로 초당 피해 · 버티는 시간
//   cfg = { wp 무기 0~4, ar 방어구 0~5, dfire, dwater, fam 'xmain'·'xboss'·…, nb 누비 하트 헝겊, acc 'crown'·'cape'·'hat'·'neck', accSt 별, potK 물약 회복 비율 }
window.__bal = (() => {
  const FAMV = { xspd: .05, xmain: .08, xheal: .1, xhp: .08, xres: .15, xboss: .1, xdr: .08, xdodge: .05 };
  const skOf = L => { const sk = { '0_0': 1 }; let pts = xSkp(L); for (let lv = 1; lv <= XMAXLV && pts > 0; lv++) for (let r = 0; r < 5 && pts > 0; r++) for (let b = 0; b < 3 && pts > 0; b++){ const k = b + '_' + r; if ((sk[k] || 0) < lv){ sk[k] = lv; pts--; } } return sk; };
  const arCap = L => XAC.filter(c => L >= c.L).length;   // 그 레벨에서 낄 수 있는 가장 높은 방어구 단계
  function unit(job, L, cfg = {}, id){
    const u = xMkUnit(job, L, id || job, true, undefined, undefined, skOf(L));
    const wp = cfg.wp || 0, wm = (1 + .08 * wp) * (cfg.dfire ? 1.05 : 1) / (1 + .08 * u.wp); u.wp = wp; ['atk', 'mag', 'heal'].forEach(k => { u[k] = Math.round(u[k] * wm); });   // 무기 · 불의 용
    const fv = k => cfg.fam === k ? FAMV[k] : 0, ms = XROLE[job] === 'melee' ? 'atk' : XROLE[job] === 'heal' ? 'heal' : 'mag';   // 사역마 맹약 (게임과 같은 순서)
    u.spd = Math.round(u.spd * (1 + fv('xspd'))); u[ms] = Math.round(u[ms] * (1 + fv('xmain'))); u.mhp = Math.round(u.mhp * (1 + fv('xhp'))); u.dr += fv('xdr'); u.dodge += fv('xdodge'); u.res = fv('xres'); u.bossK = fv('xboss'); u.healIn = fv('xheal');
    const A = XAV[cfg.ar || 0]; u.mhp = Math.round(u.mhp * (1 + A[0])); u.dr += A[1];   // 방어구
    if (cfg.nb) u.mhp = Math.round(u.mhp * 1.1);   // 누비의 하트 헝겊
    if (cfg.acc){ const D = RD_ACC.find(d => d.k === cfg.acc); if (D) D.ap(u, cfg.accSt || 5); }   // 레이드 장신구
    u.dw = cfg.dwater ? 1.1 : 1; u.potK = cfg.potK || .5; u.hp = u.mhp; u.mp = u.mmp; u.cdn = {}; u.row = XROLE[job] === 'melee' ? 'f' : 'b'; return u;
  }
  // 전투 한 칸 (xLoop0 와 같아요: MP 회복 · 게이지 · 지속 효과 · 소환수)
  function tick(B, dt){
    B.party.concat(B.foes).forEach(x => { if (x.hp <= 0) return; if (x.team === 'a' && x.mp < x.mmp) x.mp = Math.min(x.mmp, x.mp + dt * (.6 + x.L * .03) * (1 + (x.mpReg || 0)) * (XMPR[XROLE[x.job]] || 1) * (x.dw || 1)); x.g = Math.min(100, x.g + x.spd * (1 + xFm(x, 'spd') - xFm(x, 'slow')) * XGSPD * dt); const fx = x.fx; for (const k in fx){ fx[k].t -= dt; if (k === 'dot'){ fx[k].acc = (fx[k].acc || 0) + dt; while (fx[k].acc >= 2 && fx[k].t > -2){ fx[k].acc -= 2; x.hp = Math.max(0, x.hp - fx[k].v); } } if (k === 'regen'){ fx[k].acc = (fx[k].acc || 0) + dt; while (fx[k].acc >= 2){ fx[k].acc -= 2; x.hp = Math.min(x.mhp, x.hp + fx[k].v); } } if (fx[k].t <= 0){ if (k === 'bomb' && typeof xBomb === 'function') xBomb(x, fx[k]); delete fx[k]; } } xPets(x, dt); });
  }
  const potOr = x => { if (x.pot > 0 && x.hp / x.mhp < .35){ x.pot--; x.hp = Math.min(x.mhp, x.hp + Math.round(x.mhp * x.potK * (1 + (x.healIn || 0)))); x.g = 0; return true; } return false; };
  // ---------- 탐사 한 판 ----------
  //   o = { rg 지역, L 학생 레벨, mL 몬스터 레벨, kind battle·elite·boss, jobs [...], cfg, n 판 수, m { hpm, ehm, atkm, bat, bhm } (안 주면 지금 값), pot 사람마다 물약 수, lim 초 }
  function xSim(o){
    const R = XRG[o.rg], M = { hpm: R.hpm, ehm: R.ehm, atkm: R.atkm, bat: R.bat, bhm: R.bhm, ...(o.m || {}) }, N = o.n || 100, mL = o.mL, lim = o.lim || 240;
    const mk = (m, i, hm = 1) => { const k = m.k || 1, f = (1 + .35 * (mL - 1)) * hm * (k >= 3 ? M.ehm || 1 : M.hpm || 1) * (k >= 8 ? M.bhm || 1 : 1), a = (1 + .25 * (mL - 1)) * (k >= 3 ? Math.sqrt(M.atkm || 1) : M.atkm || 1) * (k >= 8 ? M.bat || 1 : 1); return { id: 'e' + i, name: m.n, ic: '', lp: m.lp, big: m.big, sc: 1, hh: 56, team: 'e', mhp: Math.round(m.hp * f * XFOE), hp: Math.round(m.hp * f * XFOE), atk: Math.round(m.atk * a * XFOE_A), spd: m.spd, g: Math.random() * 60, k, aoe: !!m.aoe, sk: m.sk || '', skn: m.skn || '', bm: m.bm || null, mL, fx: {} }; };
    let win = 0, hpl = 0, tt = 0, dead = 0;
    for (let it = 0; it < N; it++){
      const party = o.jobs.map((j, i) => { const u = unit(j, o.L, o.cfg, j + i); u.id = 'p' + i; u.pot = o.pot ?? 1; u.g = Math.random() * 40; return u; }), sz = party.length, pool = R.mon;
      const foes = o.kind === 'boss' ? [mk(R.boss, 0, 1 + .4 * (sz - 1)), ...Array.from({ length: Math.min(4, sz - 1) }, (_, i) => mk(xRand(pool), i + 1))] : o.kind === 'elite' ? [mk(R.elite, 0, 1 + .5 * (sz - 1)), ...Array.from({ length: Math.min(4, sz - 1) }, (_, i) => mk(xRand(pool), i + 1))]
        : Array.from({ length: Math.min(6, sz >= 2 ? sz + 1 : 1) }, (_, i) => mk(xRand(pool), i));
      const B = xb = { party, foes, kind: o.kind, log: '', turn: null, pick: null, over: false, last: 0, buff: false, def: {}, fxs: [], floats: [], proj: [], n0: sz };
      let t = 0; const dt = .25;
      while (t < lim){ t += dt; tick(B, dt);
        for (const x of party.concat(foes)){ if (x.hp <= 0 || x.g < 100) continue; if (x.team === 'e') xAct(x, null); else if (!potOr(x)) xAI(x); if (!xAlive(foes).length || !xAlive(party).length) break; }
        if (!xAlive(foes).length || !xAlive(party).length) break; }
      if (!xAlive(foes).length && xAlive(party).length) win++; tt += t; dead += party.filter(p => p.hp <= 0).length;
      hpl += party.reduce((s, p) => s + Math.max(0, p.hp) / p.mhp, 0) / sz;
    }
    xb = null; return { win: +(win / N).toFixed(3), hp: +(hpl / N).toFixed(3), t: +(tt / N).toFixed(1), dead: +(dead / N).toFixed(2) };
  }
  // ---------- 힘 비교: 허수아비 상대 ----------
  //   피해: 체력이 아주 많은 몬스터 하나를 60 초 동안 때린 양 · 버티기: 같은 공격을 계속 맞으며 쓰러질 때까지 걸린 시간 (혼자, 치유 스킬 포함)
  function power(job, L, cfg, n = 30){
    let dmg = 0, surv = 0;
    for (let it = 0; it < n; it++){
      { const u = unit(job, L, cfg, 'p0'); u.id = 'p0'; u.pot = 0; const f = { id: 'e0', name: 'dummy', team: 'e', mhp: 1e9, hp: 1e9, atk: 0, spd: 0.0001, g: 0, k: 8, big: 1, mL: L, fx: {}, sk: '' };
        const B = xb = { party: [u], foes: [f], kind: 'boss', log: '', over: false, last: 0, buff: false, def: {}, fxs: [], floats: [], proj: [], n0: 1 }; let t = 0; while (t < 60){ t += .25; tick(B, .25); if (u.g >= 100) xAI(u); } dmg += (1e9 - f.hp) / 60; }
      { const u = unit(job, L, cfg, 'p0'); u.id = 'p0'; u.pot = 0; const a = Math.round(17 * (1 + .25 * (L - 1)) * XFOE_A * 2.5); const f = { id: 'e0', name: 'dummy', team: 'e', mhp: 1e12, hp: 1e12, atk: a, spd: 10, g: 0, k: 1, mL: L, fx: {}, sk: '' };
        const B = xb = { party: [u], foes: [f], kind: 'battle', log: '', over: false, last: 0, buff: false, def: {}, fxs: [], floats: [], proj: [], n0: 1 }; let t = 0; while (t < 600 && u.hp > 0){ t += .25; tick(B, .25); for (const x of [u, f]){ if (x.hp <= 0 || x.g < 100) continue; if (x.team === 'e') xAct(x, null); else xAI(x); } } surv += t; }
    }
    xb = null; return { dps: +(dmg / n).toFixed(1), surv: +(surv / n).toFixed(1) };
  }
  // ---------- 레이드 12 명 (raidsim_hook.js 와 같은 보스 행동) ----------
  //   o = { L, b, n, lim, size, cfg (모두 같은 버프 · 장비), host 방장 한 명만 받는 물약 배율, hpAbs, atkAbs, matk, mk }
  function raidSim(o){
    const N = o.n || 40, L = o.L, lim = o.lim || 300, res = { win: 0, t: [], left: [], dead: [], acts: 0 };
    const SIDE = [['knight', 'white', 'black', 'warrior', 'thief', 'bard'], ['cleric', 'summon', 'druid', 'time', 'alch', 'gadget']];
    const dodge = () => { const r = Math.random(); return r < .3 ? .2 : r < .7 ? .6 : 1; };
    const MK = o.mk || { side: 1, all: 1, big: 2 };
    for (let it = 0; it < N; it++){
      const party = [], SZ = o.size || 12;
      SIDE.forEach((js, side) => js.slice(0, side ? Math.floor(SZ / 2) : Math.ceil(SZ / 2)).forEach((job, j) => { const c = (o.cfgOf && o.cfgOf(job)) || o.cfg || {}; const u = unit(job, L, c, job + side + j); u.id = 'p' + side + j; u.pot = 2; u.side = side; u.g = Math.random() * 40; party.push(u); }));
      if (o.hostPotK) party[0].potK = o.hostPotK;
      const boss = { id: 'e0', name: '보스', ic: '', lp: 16, big: 1, sc: 3, hh: 168, team: 'e', mhp: o.hpAbs, atk: o.atkAbs, spd: o.spd || 12, g: 30, k: 8, aoe: false, sk: '', skn: '', mL: L, fx: {} };
      boss.hp = boss.mhp; boss.matk = o.matk;
      const B = xb = { party, foes: [boss], kind: 'boss', log: '', turn: null, pick: null, over: false, last: 0, buff: false, def: {}, fxs: [], floats: [], proj: [], n0: 1 };
      let t = 0, fin = '', bc = 0, big = null; const dt = .25;
      const hitSome = (L2, k, fx) => L2.forEach(tg => { if (tg.hp <= 0) return; xHit(boss, tg, boss.matk * k / party.length * (.85 + Math.random() * .3) * dodge(), '#ff6a6a'); if (tg.hp > 0 && fx) fx(tg); });
      const bfx = [t2 => { t2.fx.slow = { v: .3, t: 8 }; }, t2 => { t2.fx.dot = { v: Math.max(1, Math.round(boss.atk * .25)), t: 8, acc: 0 }; }, t2 => { t2.fx.vuln = { v: .15, t: 8 }; }, t2 => { t2.g = Math.min(t2.g, -20); }][o.b || 0];
      while (t < lim){ t += dt;
        if (!xAlive(party).length){ fin = 'wipe'; break; }
        tick(B, dt);
        [['slow', .15], ['weak', .15], ['blind', .1]].forEach(([k, m]) => { if (boss.fx[k] && boss.fx[k].v > m) boss.fx[k].v = m; });
        if (big && t >= big.at){ if (big.hp0 - boss.hp >= boss.mhp * .08){ boss.g = 0; } else hitSome(xAlive(party), MK.big, bfx); big = null; }
        const g0 = boss.g; let acted = false;
        for (const x of party.concat(B.foes)){ if (x.hp <= 0 || x.g < 100) continue;
          if (x.team === 'e'){ x.g = 0; acted = true; if (big) continue; bc++; const ph = boss.hp / boss.mhp > .7 ? 1 : boss.hp / boss.mhp > .35 ? 2 : 3, A2 = xAlive(party);
            if (ph === 3 && bc % 4 === 0){ big = { at: t + 6, hp0: boss.hp }; continue; }
            if (ph >= 2 && bc % 3 === 0){ hitSome(A2, MK.all, bfx); continue; }
            if (bc % 2 === 0){ const sd = Math.random() < .5 ? 0 : 1; hitSome(A2.filter(p => p.side === sd), MK.side, bfx); continue; }
            const fr = A2.filter(p => !p.side), tg = (fr.length ? fr : A2)[Math.floor(Math.random() * (fr.length || A2.length))]; if (!tg || tg.hp <= 0) continue; xHit(boss, tg, boss.atk * (.85 + Math.random() * .3) * dodge(), '#ff6a6a'); continue; }
          if (!potOr(x)) xAI(x);
          if (boss.hp <= 0) break; }
        if (!acted && boss.g < g0 - 8) boss.g = g0 - 8;
        if (boss.hp <= 0){ fin = 'win'; break; } }
      res.acts += bc; if (fin === 'win') res.win++; res.t.push(t); res.left.push(Math.max(0, boss.hp) / boss.mhp); res.dead.push(party.filter(p => p.hp <= 0).length);
    }
    xb = null; const avg = a => +(a.reduce((x, y) => x + y, 0) / a.length).toFixed(2);
    return { acts: +(res.acts / N).toFixed(1), win: res.win / N, t: avg(res.t), left: avg(res.left), dead: avg(res.dead) };
  }
  return { unit, xSim, power, raidSim, arCap, FAMV, XRG_: () => XRG.map(r => ({ hpm: r.hpm, ehm: r.ehm, atkm: r.atkm, bat: r.bat, bhm: r.bhm })), RD_: () => ({ RD_BOSS, RD_MATK }) };
})();
