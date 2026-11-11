// 시안: 「시련의 탑」 (게임 코드 아님 · 모의 서버 화면에 넣어서 찍어요)
//   window.__tower = { load, place(), open(층), card(층), battle(층), clear(층), close() }
(() => {
  // 부류: 이름 · 아이콘 칸 · 몬스터 그림 칸(monsters_lpc 뒤 32 + i) · 설명 · 유리한 쪽 판정 (주 능력치 · 역할 · 직업)
  const T = [
    { k: 'armor', n: '철갑', mon: '강철 딱정벌레', d: '물리 피해를 절반만 받아요', good: j => j.m === 'mag', bad: j => j.m === 'atk', hp: 1.2, atk: .9, spd: 6 },
    { k: 'giant', n: '거대', mon: '이끼 바위 거인', d: '체력이 세 배예요 · 느려요', good: j => j.r === 'heal' || ['paladin', 'guardian', 'knight', 'darkknight'].includes(j.j), bad: () => false, hp: 3, atk: 1.1, spd: 4, big: 1 },
    { k: 'swift', n: '날쌘', mon: '그림자 박쥐', d: '공격을 셋 중 하나 피해요', good: j => ['thief', 'fighter', 'bladedancer', 'gunner', 'archer'].includes(j.j), bad: j => j.m === 'mag', hp: .8, atk: 1, spd: 18 },
    { k: 'swarm', n: '무리', mon: '꼬마 슬라임', d: '작은 몬스터가 다섯 마리 나와요', good: j => ['black', 'elemental', 'sage', 'bard', 'dancer'].includes(j.j), bad: j => j.r === 'melee', hp: .45, atk: .5, spd: 10, n: 5 },
    { k: 'regen', n: '재생', mon: '덩굴 정령', d: '차례마다 체력이 10 % 차요', good: j => j.m === 'atk' || j.m === 'mag', bad: j => j.m === 'heal', hp: 1.3, atk: .9, spd: 7 },
    { k: 'drain', n: '마나 먹기', mon: '보라 도깨비불', d: '때릴 때마다 내 MP 를 빼앗아요', good: j => j.m === 'atk', bad: j => j.m === 'mag', hp: 1, atk: 1, spd: 11 },
    { k: 'mirror', n: '반사', mon: '거울 수정', d: '받은 피해의 30 % 를 되돌려요', good: j => j.m === 'heal' || ['darkknight', 'paladin'].includes(j.j), bad: j => ['warrior', 'fighter', 'bladedancer'].includes(j.j), hp: 1.1, atk: .8, spd: 8 },
    { k: 'rage', n: '광폭', mon: '성난 뿔멧돼지', d: '5 차례 뒤 공격이 두 배가 돼요', good: j => j.m === 'atk' || j.m === 'mag', bad: j => j.m === 'heal', hp: 1, atk: 1.3, spd: 9 },
  ];
  const BOSS = { n: '탑지기 석상', d: '10 층마다 지키는 석상 · 부류 둘을 같이 가져요' };
  // 층 → 부류 (1~2 개) · 10 층마다 보스
  const FLOOR = f => { if (f % 10 === 0) return { boss: 1, t: [T[(f / 10) % 8], T[(f / 10 + 3) % 8]] }; const a = T[(f * 3) % 8], b = f > 12 ? T[(f * 5 + 2) % 8] : null; return { t: b && b !== a ? [a, b] : [a] }; };
  let MON = null, ICON = null, BLD = null; const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = s; });
  async function load(){ MON = await img('/__tower/tower_mon.png?' + Date.now()); ICON = await img('/__tower/tower_icons.png?' + Date.now()); BLD = await img('/__tower/tower_building.png?' + Date.now()); }
  const cv = (im, sx, sy, w, h, sc) => { const c = document.createElement('canvas'); c.width = w * sc; c.height = h * sc; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(im, sx, sy, w, h, 0, 0, w * sc, h * sc); c.style.imageRendering = 'pixelated'; return c; };
  const iconUrl = i => cv(ICON, i * 16, 0, 16, 16, 2).toDataURL();
  const monUrl = (i, sc = 1) => cv(MON, i * 64, 0, 64, 64, sc).toDataURL();
  // ---------- 맵에 탑 ----------
  let spot = null;
  function place(at){ if (at) spot = at;
    if (!spot){ const c = [40, 45]; for (let r = 0; r < 30 && !spot; r++) for (let dx = -r; dx <= r && !spot; dx++) for (let dy = -r; dy <= r && !spot; dy++){ const x = c[0] + dx, y = c[1] + dy; let ok = true; for (let a = -3; a <= 3 && ok; a++) for (let b = -6; b <= 2 && ok; b++) if (!World.isFree(x + a, y + b)) ok = false; if (ok) spot = [x, y]; } }
    const K = 1.5, c = document.createElement('canvas'); c.width = 56 * K; c.height = 120 * K; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BLD, 0, 0, 56 * K, 120 * K);
    World.setProps('campus', [{ id: 'tower', x: spot[0], y: spot[1], img: c, pxc: g, sw: c.width, sh: c.height, ax: c.width / 2, ay: c.height - 6 * K, solid: 1 }], 'tower'); return spot;
  }
  // ---------- 창 ----------
  const CSS = `<style>#twv{position:fixed;inset:0;z-index:300;background:rgba(10,6,24,.72);display:flex;align-items:flex-end;justify-content:center;font-family:var(--f-pxb);color:#F1E9FF}
    #twv .card{width:100%;max-width:520px;max-height:92vh;overflow:auto;background:#1c1530;border:2px solid #4E3C72;border-radius:18px 18px 0 0;padding:14px 14px calc(16px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:10px;box-sizing:border-box}
    #twv .hd{display:flex;align-items:center;gap:8px}#twv .hd b{flex:1;font-size:18px}#twv .x{width:40px;height:40px;border-radius:12px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-size:18px}
    #twv .sub{font-size:12px;color:#c8bce0}#twv .tag{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;font-size:12px;background:#2E2248;border:1px solid #4E3C72}
    #twv .jobs{display:grid;grid-template-columns:1fr 1fr;gap:8px}#twv .job{background:#120c22;border:1px solid #2E2248;border-radius:12px;padding:8px 10px;display:flex;flex-direction:column;gap:2px}#twv .job small{font-size:11px;color:#c8bce0}#twv .job b{font-size:15px}
    #twv .lad{display:flex;flex-direction:column-reverse;gap:4px;max-height:300px;overflow:auto;padding:4px;background:#120c22;border-radius:14px}
    #twv .fl{display:flex;align-items:center;gap:8px;min-height:44px;padding:0 10px;border-radius:10px;border:1px solid #2E2248;background:#1c1530;font-size:14px;color:#F1E9FF;font-family:var(--f-pxb)}
    #twv .fl .no{width:44px;text-align:left}#twv .fl .ics{flex:1;display:flex;gap:4px}#twv .fl .ics img{width:20px;height:20px;image-rendering:pixelated}#twv .fl small{font-size:11px;color:#9a8cb8}
    #twv .fl.done{opacity:.6}#twv .fl.done small{color:#8adc9a}#twv .fl.now{border-color:#FF9A3C;background:#2a1c38;opacity:1}#twv .fl.now small{color:#FF9A3C}#twv .fl.lock{opacity:.35}#twv .fl.boss{border-style:dashed}
    #twv .mons{display:flex;gap:6px;justify-content:center;background:radial-gradient(circle at 50% 70%,#3a2c5a,#120c22 70%);border-radius:14px;padding:6px}#twv .mons img{width:112px;height:112px;image-rendering:pixelated}
    #twv .tr{display:flex;gap:8px;align-items:flex-start;background:#120c22;border-radius:12px;padding:8px 10px}#twv .tr img{width:28px;height:28px;image-rendering:pixelated;flex:none}#twv .tr b{font-size:15px}#twv .tr div{display:flex;flex-direction:column;gap:2px}
    #twv .pick{display:grid;grid-template-columns:1fr 1fr;gap:8px}#twv .pk{min-height:72px;border-radius:14px;border:2px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-family:var(--f-pxb);font-size:15px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px}
    #twv .bd{font-size:11px;padding:1px 8px;border-radius:999px}#twv .bd.g{background:#2E6A3E;color:#C8FFD0}#twv .bd.b{background:#7A2E3A;color:#FFD0D6}#twv .bd.n{background:#3A3458;color:#D8D0F0}
    #twv .pk.g{border-color:#5AC46E}#twv .rw{display:flex;gap:6px;flex-wrap:wrap}
    #twv .go{min-height:48px;border-radius:14px;border:1px solid #C86A1E;background:#FF9A3C;color:#2A1506;font-family:var(--f-pxb);font-size:16px}
    #twv.res{align-items:center}#twv.res .card{border-radius:18px;max-width:360px;text-align:center;align-items:center}#twv.res .big{font-size:26px;color:#FFD878}
  </style>`;
  const close = () => { const v = document.getElementById('twv'); if (v) v.remove(); };
  const open0 = (html, cls = '') => { close(); const v = document.createElement('div'); v.id = 'twv'; v.className = cls; v.innerHTML = CSS + html; document.body.appendChild(v); const x = v.querySelector('[data-x]'); if (x) x.onclick = close; return v; };
  const J = () => { const o = __tw.jobs(); return [{ j: o.j1, n: o.n1, r: o.r1, m: o.m1, L: o.L1, t: '1차' }, o.j2 ? { j: o.j2, n: o.n2, r: o.r2, m: o.m2, L: o.L2, t: '2차' } : null].filter(Boolean); };
  const fit = (j, F) => { let s = 0; F.t.forEach(t => { if (t.good(j)) s++; else if (t.bad(j)) s--; }); return s > 0 ? ['g', '유리'] : s < 0 ? ['b', '불리'] : ['n', '보통']; };
  const ROLE_KO = { melee: '근접', ranged: '원거리', heal: '치유' };
  // ---------- 탑 입구 창: 층 사다리 ----------
  function open(now = 14, best = 13){
    const js = J(), rows = []; for (let f = 1; f <= 50; f++){ const F = FLOOR(f), st = f <= best ? 'done' : f === now ? 'now' : 'lock';
      rows.push(`<button class="fl ${st}${F.boss ? ' boss' : ''}" data-f="${f}"><span class="no">${f} 층</span><span class="ics">${F.t.map(t => `<img src="${iconUrl(T.indexOf(t))}" alt="">`).join('')}${F.boss ? '<span class="tag">보스</span>' : ''}</span><small>${st === 'done' ? '깼어요' : st === 'now' ? '도전' : ''}</small></button>`); }
    const v = open0(`<div class="card"><div class="hd"><b>시련의 탑</b><span class="tag">오늘 도전 2 / 3</span><button class="x" data-x>✕</button></div>
      <div class="jobs">${js.map(j => `<div class="job"><small>${j.t} · ${ROLE_KO[j.r]}</small><b>${j.n} Lv ${j.L}</b></div>`).join('')}</div>
      <div class="sub">가장 높이 간 층 ${best} 층 · 반 1 등 27 층</div>
      <div class="lad">${rows.join('')}</div></div>`);
    const n = v.querySelector('.fl.now'); if (n) n.scrollIntoView({ block: 'center' });
    v.querySelectorAll('[data-f]').forEach(b => b.onclick = () => card(+b.dataset.f)); return v;
  }
  // ---------- 층 카드: 부류 · 직업 고르기 ----------
  function card(f = 14){
    const F = FLOOR(f), js = J(), mi = F.boss ? [8] : F.t.map(t => T.indexOf(t));
    const rw = F.boss ? ['골드 3000', '탑 장신구 상자', '강화석 5'] : ['골드 ' + (200 + f * 40), '강화석 ' + (1 + (f / 5 | 0))];
    const v = open0(`<div class="card"><div class="hd"><b>${f} 층${F.boss ? ' · ' + BOSS.n : ''}</b><button class="x" data-x>✕</button></div>
      <div class="mons">${mi.map(i => `<img src="${monUrl(i)}" alt="">`).join('')}</div>
      ${F.t.map(t => `<div class="tr"><img src="${iconUrl(T.indexOf(t))}" alt=""><div><b>${t.n}${F.boss ? "" : " · " + t.mon}</b><span class="sub">${t.d}</span></div></div>`).join('')}
      <div class="sub">처음 깨면</div><div class="rw">${rw.map(r => `<span class="tag">${r}</span>`).join('')}</div>
      <div class="sub">어느 직업으로 오를까요</div>
      <div class="pick">${js.map(j => { const [c, w] = fit(j, F); return `<button class="pk ${c}" data-go="${j.t}"><span>${j.t} ${j.n}</span><span class="sub">Lv ${j.L}</span><span class="bd ${c}">${w}</span></button>`; }).join('')}</div></div>`);
    v.querySelectorAll('[data-go]').forEach(b => b.onclick = () => battle(f)); return v;
  }
  // ---------- 전투 (게임 전투 화면에 탑 몬스터를 넣어요) ----------
  function battle(f = 14, L = 34){
    close(); const F = FLOOR(f), out = [];
    const mk = (t, i, nm, li, hm = 1, sc) => { const H = Math.round(55 * (1 + .35 * (L - 1)) * 1.4 * t.hp * hm), A = Math.round(10 * (1 + .25 * (L - 1)) * 1.5 * t.atk); return { id: 'e' + i, name: nm, ic: '', lp: 32 + li, big: 0, sc: sc || (t.big ? 2 : 1), hh: 56 * (sc || (t.big ? 2 : 1)), team: 'e', mhp: H, hp: H, atk: A, spd: t.spd, g: Math.random() * 60, k: sc === 2 && !t.big ? 8 : t.big ? 3 : 1, aoe: false, sk: '', skn: '', bm: null, mL: L, fx: {} }; };
    if (F.boss) out.push(mk({ hp: 6, atk: 1.4, spd: 7 }, 0, BOSS.n, 8, 1, 2));
    else F.t.forEach(t => { const n = t.k === 'swarm' ? 3 : 1; for (let i = 0; i < n; i++) out.push(mk(t, out.length, t.mon, T.indexOf(t), 1)); });
    __tw.battle(out, F.t.map(t => t.n + ': ' + t.d).join(' · '), [`시련의 탑 ${f} 층`, F.t.map(t => t.n).join(' · ') + (F.boss ? ' · 보스' : '')]);
  }
  // ---------- 깬 뒤 ----------
  function clear(f = 14){
    const F = FLOOR(f), v = open0(`<div class="card"><span class="sub">시련의 탑</span><div class="big">${f} 층 돌파</div>
      <div class="rw" style="justify-content:center"><span class="tag">골드 ${200 + f * 40}</span><span class="tag">강화석 ${1 + (f / 5 | 0)}</span></div>
      <div class="sub">다음: ${f + 1} 층 · ${FLOOR(f + 1).t.map(t => t.n).join(' · ')}${FLOOR(f + 1).boss ? ' · 보스' : ''}</div>
      <button class="go" data-x style="width:100%">좋아요</button></div>`, 'res'); return v;
  }
  window.__tower = { load, place, open, card, battle, clear, close, T, FLOOR };
})();
