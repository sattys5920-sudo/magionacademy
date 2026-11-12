// 스킬 설명 점검: 모든 직업 · 모든 스킬의 설명(xDesc)을 Lv 1 · 2 · 5에서 전투에 실제로 쓰이는 값(xMkUnit이 만든 스킬)과 나란히 놓고 어긋나면 표시해요
//   먼저 `sh tools/ui_mock.sh /home/user/magionacademy 8822` 로 모의 서버를 띄우고 `node tools/balance/skill_desc_audit.js 8822` → tools/balance/skill_desc_audit.txt
//   「실제 값」은 아래 real() 이 전투 코드(xAct0 · xApply · xPets · xCdOf)와 같은 식으로 스킬 객체에서 다시 계산해요 (xDesc 코드는 쓰지 않아요)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const PORT = process.argv[2] || 8822;
const seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 55, inv: {}, cr: [], eggs: [], orders: [], hints: [], found: [], fdex: {}, rod: 1, closet: {}, fbag: {}, npc: {}, mq: { q: null, st: 1, ph: 'arrive', prog: {}, done: {}, named: {}, dl: null } } }, story: { live: { ch: 1, at: 1 } } };
const LVS = [1, 2, 5];
const mul = n => String(Math.round(n * 100) / 100), pct = v => Math.round(Math.round(v * 1000) / 10);
const SN = { atk: '공격', mag: '마법', heal: '치유' };
const PAS = { def: .05, hp: .06, atk: .05, mag: .05, spd: .05, vamp: .06, crit: .06, surv: 1, dodge: .05 };

// 전투가 실제로 하는 일 → 설명에 꼭 들어가야 할 조각들
function real(o, sk, lv, pasV){
  const T = [], N = [];   // T: 설명에 있어야 할 글자 · N: 참고 (설명 검사는 안 하는 실제 값)
  if (o.pas){ T.push(`${pct(pasV)}%`); if (o.pas === 'surv') T.push('버티고'); return { T, N }; }
  const foe = sk.tg === 'all' ? '적 전체' : '적 하나', ally = sk.tg === 'all' ? '아군 전체' : sk.tg === 'self' ? '나' : '아군 하나';
  if (sk.t === 'dmg'){ T.push(`${foe} ${SN[sk.st]} ×${mul(sk.p)}`); if (sk.hits > 1) T.push(`×${sk.hits}회`); if (sk.exec) T.push('40% 미만', '×1.8'); if (sk.fcrit) T.push('반드시 치명타');
    if (sk.petb) T.push(`+${pct(sk.petb)}%`);
    (sk.ap || []).forEach(([k, v, s]) => { if (k === 'stun') T.push(`행동 늦추기 ${v}`); else if (k === 'dot') T.push(`${s}초간 2초마다 ${SN[sk.st]} ×${mul(v)}`); else if (k === 'bomb') T.push(`${s}초 뒤 폭발 ${SN[sk.st]} ×${mul(v)}`); else T.push(`${{ slow: '속도 -', weak: '공격 -', vuln: '받는 피해 +' }[k]}${pct(v)}% (${s}초)`); });
    if (sk.drain) T.push(`MP ${pct(sk.drain)}%`); if (sk.steal) T.push('훔쳐요'); if (sk.gold) T.push('골드 +'); if (sk.w < 0) T.push(`내 행동 늦추기 ${-sk.w}`); }
  else if (sk.t === 'heal'){ T.push(`${ally} 치유 ×${mul(sk.p)}`); if (sk.pct) T.push(`최대 체력의 ${pct(sk.pct)}%`); if (sk.cl) T.push('나쁜 효과'); if (sk.mpb) T.push(`MP ${pct(sk.mpb)}%`); }
  else if (sk.t === 'revive'){ T.push(sk.all ? '전부' : '하나', `체력 ${pct(sk.pct || .5)}%`); if (sk.hl) T.push(`치유 ×${mul(sk.hl)}`); }
  else if (sk.t === 'buff'){ const k = sk.key; T.push(`${sk.sec}초`);
    if (k === 'shield') T.push(`보호막 (${SN[sk.st || 'heal']} ×${mul(sk.sv || 2)}`); else if (k === 'regen') T.push(`2초마다 치유 ×${mul(sk.v)}`); else if (k === 'counter') T.push(`${pct(sk.v)}%`); else if (k === 'taunt') T.push(`${sk.sec}초간 적 공격의 80%`); else if (k === 'cover') T.push(`${sk.sec}초간 아군을 노린 공격의 65%`);
    else if (k === 'dodge') T.push(`회피 ${Math.min(50, pct(sk.v))}%`); else T.push(`${sk.tg === 'self' ? { atk: '내가 주는 피해 +', spd: '내 속도 +', dmgIn: '내가 받는 피해 -' }[k] : ally + ' ' + { atk: '주는 피해 +', spd: '속도 +', dmgIn: '받는 피해 -' }[k]}${pct(sk.v)}%`);
    (sk.also || []).forEach(([k2, v2]) => T.push(k2 === 'dmgIn' ? `받는 피해 -${pct(v2)}%` : `${{ atk: '주는 피해', spd: '속도', dodge: '회피' }[k2] || k2} +${pct(v2)}%`)); }
  else if (sk.t === 'deb'){ T.push(`${sk.sec}초`); T.push(sk.key === 'blind' ? `${pct(sk.v)}% 확률로 빗나가요` : `${foe} ${{ slow: '속도 -', weak: '공격 -', vuln: '받는 피해 +' }[sk.key]}${pct(sk.v)}%`); }
  else if (sk.t === 'dot') T.push(`${foe} 8초간 2초마다 ${SN[sk.st]} ×${mul(sk.p)}`);
  else if (sk.t === 'stun') T.push(`${foe} ${SN[sk.st]} ×${mul(sk.p)}`, '행동 늦추기 60');
  else if (sk.t === 'burst') T.push(`×${mul(1.5 * (sk.p || 1))}`);
  else if (sk.t === 'cleanse'){ T.push('나쁜 효과'); if (sk.regen) T.push(`10초간 2초마다 치유 ×${mul(sk.regen)}`); }
  else if (sk.t === 'encore') T.push(lv > 1 ? `세기 ×${mul(1 + ((sk.p || 1) - 1) * .5)}` : 'MP 없이 한 번 더');
  else if (sk.t === 'recall') T.push(`${pct(.12 * (sk.p || 1))}%`);
  else if (sk.t === 'leap') T.push('곧바로 다시 행동', `속도 +${pct(sk.v)}% (${sk.sec}초)`);
  else if (sk.t === 'tstop'){ const ts = +(4 * (1 + .2 * (lv - 1))).toFixed(1); T.push('곧바로 행동', `행동 늦추기 ${Math.round(150 * ts / 4)}`); }
  else if (sk.t === 'mp') T.push(`MP ${pct(sk.v)}%`);   // xAct0: t.mmp * sk.v
  else if (sk.t === 'summon'){ const q = sk.pet; T.push(`${Math.round(q.sec * (1 + .1 * (lv - 1)) * 10) / 10}초간`, `${q.every}초마다`, `×${mul(q.kind === 'dmgall' ? q.k * .8 : q.k)}`); }
  else N.push('알 수 없는 종류 ' + sk.t);
  if (sk.mp) T.push(`MP ${Math.ceil(sk.mp)}`);
  const m0 = sk.mp0 ?? sk.mp ?? 0, cd = sk.cd != null ? sk.cd : m0 >= 18 ? 4 : m0 >= 14 ? 3 : m0 >= 8 ? 2 : m0 >= 4 ? 1 : 0; if (cd) T.push(`쿨 ${cd}턴`);
  if (sk.t !== 'dmg' && sk.ap) N.push(`ap ${JSON.stringify(sk.ap)} 는 전투에서 안 쓰여요 (t=${sk.t})`);
  if (!['dmg', 'heal', 'stun', 'dot'].includes(sk.t) && o.p != null && o.t === 'deb') N.push(`p ${o.p} 는 전투에서 안 쓰여요 (t=${sk.t}, 피해 없음)`);
  if (sk.t === 'buff' && sk.key === 'dodge' && pct(sk.v) > 50) N.push(`회피는 최대 50%라 ${pct(sk.v)}%는 50%로 잘려요`);
  return { T, N };
}
// 레벨이 바뀌면 달라지는 실제 값: 그 종류의 스킬이 전투에서 실제로 쓰는 값만 (MP · lv 빼고)
const sig = (sk, lv) => { const t = sk.t, k = sk.key;
  const u = t === 'dmg' || t === 'dot' || t === 'stun' ? [sk.p] : t === 'heal' ? [sk.p, sk.pct] : t === 'buff' ? (k === 'shield' ? [sk.sv] : k === 'taunt' || k === 'cover' ? [] : k === 'dodge' ? [Math.min(.5, sk.v)] : [sk.v]) : t === 'deb' || t === 'leap' ? [sk.v] : t === 'tstop' ? [lv] : t === 'mp' ? [sk.v] : t === 'revive' ? [sk.pct, sk.hl] : t === 'cleanse' ? [sk.regen] : t === 'summon' ? [sk.pet.k, sk.pet.sec * (1 + .1 * (lv - 1))] : [];
  return JSON.stringify(u); };

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  const data = await p.evaluate(LVS => { const out = {}; const strip = o => JSON.parse(JSON.stringify(o));
    Object.keys(__T.XJ_).forEach(job => { out[job] = { n: __T.XJ_[job].n, sks: __T.xAll_(job).map(o => ({ o: strip(o), lv: LVS.concat([3, 4]).sort().map(lv => { const sk = {}; sk[o.b + '_' + o.r] = lv; const u = __T.xMk(job, 1, 'a', true, undefined, undefined, sk);
      return { lv, desc: __T.xDesc_(o, lv).replace(/\u00a0/g, ' '), sk: o.pas ? null : strip(u.sks.find(s => s.n === o.n)), pas: o.pas ? u.pas[o.pas] : null }; }) })) }; }); return out; }, LVS);
  await b.close();
  const L = [], bad = [], notes = new Set(); let n = 0;
  L.push('스킬 설명 점검 (Lv 1 · 2 · 5) · 「설명」= 화면에 나오는 글 · 「실제」= 전투 코드가 쓰는 값에서 다시 계산한 조각 (전부 설명에 있어야 해요)');
  L.push('행동 늦추기 N = 행동 게이지(100이면 차례)를 -N까지 되돌려요 · 속도 -% = 그동안 게이지가 느리게 차요', '');
  for (const [job, J] of Object.entries(data)){
    L.push(`==== ${J.n} (${job})`);
    for (const S of J.sks){ n++; const o = S.o; L.push(`-- ${o.n} [${o.code}${o.pas ? '' : ' · ' + (S.lv[0].sk || {}).t}]`);
      S.lv.forEach((x, i) => { const r = real(o, x.sk || {}, x.lv, x.pas), miss = r.T.filter(t => !x.desc.includes(t)), fl = [];
        if (miss.length) fl.push('없음: ' + miss.join(' | '));
        if (/행동이 잠깐|늦어져요|지연/.test(x.desc)) fl.push('예전 늦추기 표현');
        if (/\d+\.\d+%|\d\.\d{3,}/.test(x.desc)) fl.push('소수점 %');
        if (/undefined|NaN|null/.test(x.desc)) fl.push('undefined');
        const nx = S.lv[i + 1]; if (nx && !o.pas && x.lv < 5){ const same = x.desc.replace(/ · MP \d+/, '') === nx.desc.replace(/ · MP \d+/, ''), diff = sig(x.sk, x.lv) !== sig(nx.sk, nx.lv); if (same && diff) fl.push('다음 레벨 설명이 같은데 실제 값은 달라요'); }
        r.N.forEach(t => notes.add(`${J.n} · ${o.n}: ${t}`));
        if (LVS.includes(x.lv)){ L.push(`  Lv${x.lv} 설명: ${x.desc}`); L.push(`       실제: ${r.T.join(' / ')}${fl.length ? '\n       !! ' + fl.join(' · ') : ''}`); }
        else if (fl.length) L.push(`  Lv${x.lv} !! ${fl.join(' · ')}`);
        if (fl.length) bad.push(`${J.n} · ${o.n} Lv${x.lv}: ${fl.join(' · ')}`); });
    }
    L.push('');
  }
  L.push(`==== 결과: 스킬 ${n}개 · 어긋남 ${bad.length}건`); bad.forEach(x => L.push('  ' + x));
  L.push('', '==== 참고: 전투 코드에서 쓰이지 않는 값 · 잘리는 값 (설명은 실제 동작을 따라요 · 고칠지 정해 주세요)'); [...notes].forEach(x => L.push('  ' + x));
  fs.writeFileSync(__dirname + '/skill_desc_audit.txt', L.join('\n') + '\n');
  console.log(`skills ${n} · mismatches ${bad.length}`); bad.slice(0, 40).forEach(x => console.log('  ' + x));
})();
