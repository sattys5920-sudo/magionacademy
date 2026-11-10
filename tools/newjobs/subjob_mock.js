// 부직업 시안 (게임 코드 아님 · 모의 서버 화면 안에서 돌려요)
//   1) 「영웅의 혼」 연출: 탐사 문 기둥이 빛나고 → 혼 12 개가 나와 맴돌고 → 하나 고르면 몸으로 들어와요
//   2) 탐사 로비 위쪽: 1차 / 2차 직업 두 칸 (떠나기 전에 눌러서 바꿔요)
(() => {
  const JOBS = [['paladin', '성기사', '탱커', '#ffe27a', '신성 · 가호 · 치유'], ['guardian', '수호자', '탱커', '#7ab8ff', '위압 · 방패 · 창술'], ['darkknight', '암흑기사', '탱커', '#c07aff', '흡수 · 어둠 · 각성'],
    ['dancer', '무희', '지원', '#ff8ac8', '마나의 춤 · 열정 · 부채'], ['sage', '현자', '지원', '#7ae6ff', '지혜 · 룬 · 비전'], ['shaman', '주술사', '힐러', '#7aef6a', '토템 · 영혼 · 번개'], ['miko', '무녀', '힐러', '#ff7a7a', '정결 · 결계 · 신령'],
    ['archer', '궁수', '원거리', '#c8e86a', '사격 · 원소 화살 · 사냥꾼'], ['gunner', '총잡이', '원거리', '#ffb040', '연사 · 특수탄 · 저격'], ['elemental', '정령술사', '원거리', '#6ad8ff', '불 · 물 · 바람'],
    ['fighter', '격투가', '근거리', '#ff7a3a', '권법 · 기공 · 몸놀림'], ['bladedancer', '검무사', '근거리', '#e8e4ff', '칼춤 · 잔영 · 검기']];
  const TAKEN = { archer: '하늘', shaman: '도토리', bladedancer: '민트' };   // 다른 친구가 이미 받은 혼 (직업은 반에 하나씩)
  const RC = { 탱커: '#7ab8ff', 지원: '#ff8ac8', 힐러: '#7aef6a', 원거리: '#ffb040', 근거리: '#ff7a3a' };
  // 추천 · 비추천: 1차 직업 역할과 같으면 비추천, 파티에 모자라기 쉬운 역할(탱커 · 힐러 · 지원)이 내 역할과 다르면 추천
  const R1 = j => ({ warrior: 'melee', thief: 'melee', knight: 'tank', bard: 'support', time: 'support', white: 'heal', druid: 'heal', cleric: 'heal' })[j] || 'ranged';
  const R2 = { 탱커: 'tank', 지원: 'support', 힐러: 'heal', 원거리: 'ranged', 근거리: 'melee' }, RN = { tank: '탱커', support: '지원', heal: '힐러', ranged: '원거리', melee: '근거리' };
  const rec = (first, r) => { const a = R1(first), b = R2[r]; return a === b ? -1 : ['tank', 'heal', 'support'].includes(b) ? 1 : 0; };
  const why = (first, r, n1) => { const k = rec(first, r); return k < 0 ? `1차 ${n1}${(n1.charCodeAt(n1.length - 1) - 44032) % 28 ? "과" : "와"} 같은 ${RN[R1(first)]}예요` : k > 0 ? '파티에 모자라기 쉬운 역할이에요' : ''; };
  let WPN = null; const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = s; });
  const sleep = ms => new Promise(r => setTimeout(r, ms)), ease = q => q < .5 ? 2 * q * q : 1 - (-2 * q + 2) ** 2 / 2;
  const rgb = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)).join(',');
  function soul(g, x, y, c, s, now, ji, a = 1){   // 혼 하나: 빛무리 + 흰 속 + 무기 그림자
    if (a <= 0) return; const R = 9 * s, fl = Math.sin(now / 160 + ji) * .12 + 1; g.save(); g.globalAlpha = a; g.globalCompositeOperation = 'lighter';
    const rg = g.createRadialGradient(x, y, 0, x, y, R * 2.4 * fl); rg.addColorStop(0, `rgba(${rgb(c)},.75)`); rg.addColorStop(.45, `rgba(${rgb(c)},.25)`); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.beginPath(); g.arc(x, y, R * 2.4 * fl, 0, 7); g.fill();
    g.fillStyle = c; g.beginPath(); g.moveTo(x - R * .55, y); g.quadraticCurveTo(x, y - R * 2 * fl, x + R * .55, y); g.arc(x, y, R * .55, 0, Math.PI); g.fill();   // 불꽃 모양
    g.fillStyle = '#fff'; g.beginPath(); g.arc(x, y + R * .1, R * .3, 0, 7); g.fill(); g.globalCompositeOperation = 'source-over';
    if (WPN && ji >= 0){ g.globalAlpha = a * .9; g.imageSmoothingEnabled = false; const w = 26 * s; g.drawImage(WPN, 0, ji * 64, 64, 64, x - w / 2, y - w * .62, w, w); }
    g.restore();
  }
  function iconCv(ji, c){ const cv = document.createElement('canvas'); cv.width = 40; cv.height = 40; const g = cv.getContext('2d'); soul(g, 20, 24, c, 1.05, 0, ji); return cv; }
  async function load(){ WPN = await img('/__newjobs/weapons_new.png?' + Date.now()); }
  // ---------- 1) 연출 ----------
  async function cut(o = {}){
    const bd = k => k > 0 ? '<span class="bdg y">추천</span>' : k < 0 ? '<span class="bdg n">비추천</span>' : '';
    await load(); const A = World.Avatar, av = A.fromLook(o.look || 12); await A.need(av);
    const v = document.createElement('div'); v.id = 'famcut'; v.className = 'sjcut'; v.innerHTML = `<canvas width="320" height="180"></canvas><div class="fname"></div><div class="fline"></div><div class="ffade"></div>
      <style>.sjcut .sjpick{position:absolute;left:0;right:0;bottom:0;top:min(58%,calc(100% - 230px));padding:8px 12px calc(10px + env(safe-area-inset-bottom));background:linear-gradient(#05030a00,#05030af0 18%);opacity:0;transition:opacity .6s;display:flex;flex-direction:column;gap:6px}.sjcut .sjpick.on{opacity:1}
      .sjgrid{flex:1;min-height:0;padding-top:7px;align-content:start;display:grid;grid-template-columns:repeat(auto-fill,minmax(98px,1fr));gap:5px;overflow:auto}.sjc{display:flex;align-items:center;gap:4px;min-height:44px;padding:2px 6px 2px 2px;border-radius:10px;border:1px solid #4E3C72;background:#1c1530;color:#F1E9FF;font-family:var(--f-pxb);text-align:left}
      #famcut .sjc canvas{position:static;transform:none;left:auto;top:auto;width:36px;height:36px;flex:none}.sjc>span:last-child{min-width:0}.sjc i{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.sjc b{display:block;white-space:nowrap;font-size:13px;line-height:16px}.sjc i{font-style:normal;font-size:10px;line-height:13px;color:var(--rc)}.sjc.on{border-color:#FF9A3C;background:#3a2448;box-shadow:0 0 0 2px #FF9A3C55}.sjc.off{opacity:.38}.sjc.off i{color:#b8acd0}.sjc{position:relative}.sjc .bdg{margin-left:4px;padding:0 4px;border-radius:6px;font-size:10px;line-height:14px;font-style:normal}.bdg.y{background:#3fae5a;color:#06210d}.bdg.n{background:#d04a4a;color:#fff}.sjdet .bdg{display:inline-block;margin-left:4px;padding:0 6px;border-radius:6px;font-size:11px;line-height:16px}
      .sjdet{display:flex;align-items:center;gap:8px;min-height:44px}.sjdet .t{flex:1;font-size:14px;line-height:18px;word-break:keep-all}.sjdet .t small{display:block;font-size:11px;color:#c8bce0}.sjdet button{min-height:44px;padding:0 14px;border-radius:12px;border:1px solid #C86A1E;background:#FF9A3C;color:#2A1506;font-family:var(--f-pxb);font-size:15px}.sjdet button.g{background:#2E2248;border-color:#4E3C72;color:#F1E9FF}</style>
      <div class="sjpick"><div class="sjgrid">${JOBS.map(([k, n, r, c], i) => `<button class="sjc${TAKEN[k] ? ' off' : ''}" data-sj="${i}" style="--rc:${RC[r]}"><span data-ic="${i}"></span><span><b>${n}</b><i>${TAKEN[k] ? '주인: ' + TAKEN[k] : r}${TAKEN[k] ? '' : bd(rec(o.first, r))}</i></span></button>`).join('')}</div><div class="sjdet"><div class="t">혼을 하나 골라요<small>고르면 바꿀 수 없어요</small></div></div></div>`;
    document.body.appendChild(v); v.querySelectorAll('[data-ic]').forEach(s => s.replaceWith(iconCv(+s.dataset.ic, JOBS[+s.dataset.ic][3])));
    const cv = v.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
    const S = { dark: 0, rune: 0, rise: 0, ring: 1, sel: -1, selK: 0, gone: 0, enter: 0, burst: 0, glow: 0, wpn: 0, ang: 0, tA: performance.now() }; let live = true;
    const P0 = [[112, 150], [208, 150]], C0 = [160, 112], st = [...Array(40)].map((_, i) => [(i * 73) % 320, (i * 37) % 60, i % 3]);
    const pos = (i, now) => { const a = S.ang + i / 12 * Math.PI * 2, e = ease(Math.min(1, Math.max(0, S.rise * 1.6 - i * .05))), src = P0[i % 2], tx = C0[0] + Math.cos(a) * 92 * S.ring, ty = C0[1] + Math.sin(a) * 26 * S.ring + Math.sin(now / 400 + i) * 2;
      return [src[0] + (tx - src[0]) * e, src[1] - 30 + (ty - src[1] + 30) * e, Math.sin(a), e]; };
    const draw = now => { if (!live) return; requestAnimationFrame(draw); S.ang += S.sel < 0 ? .004 : .0015;
      const sk = g.createLinearGradient(0, 0, 0, 150); sk.addColorStop(0, '#0b0820'); sk.addColorStop(1, '#2a2350'); g.fillStyle = sk; g.fillRect(0, 0, 320, 150); g.fillStyle = '#1a2a24'; g.fillRect(0, 150, 320, 30); g.fillStyle = '#22382e'; g.fillRect(0, 150, 320, 2);
      st.forEach(([x, y, k]) => { g.globalAlpha = .4 + .4 * Math.sin(now / 500 + x); g.fillStyle = '#fff'; g.fillRect(x, y, 1, 1); }); g.globalAlpha = 1;
      for (let t = 0; t < 9; t++){ g.fillStyle = '#15241e'; g.beginPath(); g.moveTo(t * 40 - 22, 150); g.lineTo(t * 40, 112 + (t % 3) * 7); g.lineTo(t * 40 + 22, 150); g.fill(); }
      // 탐사 문: 돌기둥 둘 + 위 들보 + 글자 띠
      [P0[0][0], P0[1][0]].forEach((x, s) => { g.fillStyle = '#4a4658'; g.fillRect(x - 9, 62, 18, 88); g.fillStyle = '#5e5a70'; g.fillRect(x - 9, 62, 4, 88); g.fillStyle = '#34303f'; g.fillRect(x + 6, 62, 3, 88); g.fillStyle = '#5e5a70'; g.fillRect(x - 12, 144, 24, 6);
        for (let k = 0; k < 6; k++){ const on = Math.min(1, Math.max(0, S.rune * 7 - k - s * .5)); g.fillStyle = on ? `rgba(255,216,102,${on})` : '#2a2734'; const y = 72 + k * 12; g.fillRect(x - 3, y, 6, 2); g.fillRect(x - (k % 2 ? 3 : -1), y + 2, 2, 5); g.fillRect(x - 3, y + 7, 6, 1);
          if (on){ g.globalCompositeOperation = 'lighter'; g.fillStyle = `rgba(255,200,90,${.18 * on})`; g.fillRect(x - 8, y - 3, 16, 13); g.globalCompositeOperation = 'source-over'; } } });
      g.fillStyle = '#4a4658'; g.fillRect(96, 52, 128, 11); g.fillStyle = '#5e5a70'; g.fillRect(96, 52, 128, 3); g.fillStyle = '#34303f'; g.fillRect(100, 63, 120, 2);
      if (S.rune){ g.globalCompositeOperation = 'lighter'; const gr = g.createRadialGradient(160, 110, 0, 160, 110, 70); gr.addColorStop(0, `rgba(255,216,140,${.25 * S.rune})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(80, 40, 160, 120); g.globalCompositeOperation = 'source-over'; }
      g.fillStyle = `rgba(4,2,10,${.45 * S.dark})`; g.fillRect(0, 0, 320, 180);
      // 혼: 뒤쪽 → 나 → 앞쪽 순서로 그려요
      const P = JOBS.map((J, i) => pos(i, now)), back = [], front = [];
      JOBS.forEach((J, i) => { if (i === S.sel) return; (P[i][2] < 0 ? back : front).push(i); });
      const one = i => { const [x, y, , e] = P[i], tk = TAKEN[JOBS[i][0]], a = e * (1 - S.gone) * (tk ? .35 : 1) * (S.sel >= 0 && S.sel !== i ? .55 : 1); if (S.gone && i !== S.sel){ const src = P0[i % 2]; soul(g, x + (src[0] - x) * S.gone, y + (src[1] - 40 - y) * S.gone, JOBS[i][3], .7, now, i, a); } else soul(g, x, y, JOBS[i][3], .7 + (P[i][2] > 0 ? .1 : 0), now, i, a); };
      back.forEach(one);
      // 나 (앞을 봐요)
      const sp = A.compose(av); if (sp){ const FW = A.FW, FH = A.FH, d = A.meta.dirs.down; if (S.glow){ g.globalCompositeOperation = 'lighter'; const J = JOBS[S.sel], gr = g.createRadialGradient(160, 130, 0, 160, 130, 40); gr.addColorStop(0, `rgba(${rgb(J[3])},${.6 * S.glow})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(110, 80, 100, 100); g.globalCompositeOperation = 'source-over'; }
        g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.ellipse(160, 151, 11, 3, 0, 0, 7); g.fill(); g.drawImage(sp, d * FW, 0, FW, FH, 160 - FW / 2, 156 - FH, FW, FH);
        if (S.glow){ g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = .35 * S.glow * (.7 + .3 * Math.sin(now / 120)); g.drawImage(sp, d * FW, 0, FW, FH, 160 - FW / 2, 156 - FH, FW, FH); g.restore(); } }
      front.forEach(one);
      if (S.sel >= 0){ const J = JOBS[S.sel], [x0, y0] = P[S.sel], k = S.selK, tx = 160, ty = 86, x1 = x0 + (tx - x0) * k, y1 = y0 + (ty - y0) * k;
        if (S.enter < 1){ const e = S.enter, a = e * 9, r = 30 * (1 - e), ex = x1 + (160 - x1) * e + Math.cos(a) * r, ey = y1 + (128 - y1) * e + Math.sin(a) * r * .5; soul(g, ex, ey, J[3], (.7 + .5 * k) * (1 - e * .6), now, S.sel, 1);
          if (e > 0) for (let t = 1; t < 9; t++){ const ee = Math.max(0, e - t * .025), aa = ee * 9, rr = 30 * (1 - ee); g.globalAlpha = .5 - t * .05; g.fillStyle = J[3]; g.fillRect(x1 + (160 - x1) * ee + Math.cos(aa) * rr, y1 + (128 - y1) * ee + Math.sin(aa) * rr * .5, 2, 2); } g.globalAlpha = 1; } }
      if (S.burst){ const q = (now - S.burst) / 1100; if (q < 1){ const J = JOBS[S.sel]; g.strokeStyle = `rgba(255,255,255,${1 - q})`; g.lineWidth = 3 * (1 - q); g.beginPath(); g.arc(160, 128, 6 + q * 120, 0, 7); g.stroke(); g.strokeStyle = `rgba(${rgb(J[3])},${1 - q})`; g.beginPath(); g.ellipse(160, 150, 8 + q * 70, 3 + q * 22, 0, 0, 7); g.stroke(); g.fillStyle = `rgba(255,255,255,${.5 * (1 - q) ** 2})`; g.fillRect(0, 0, 320, 180);
        for (let i = 0; i < 16; i++){ const a = i / 16 * 7, r = q * 50; g.fillStyle = i % 2 ? '#fff' : J[3]; g.globalAlpha = 1 - q; g.fillRect(160 + Math.cos(a) * r, 128 + Math.sin(a) * r * .7, 2, 2); } g.globalAlpha = 1; } }
      if (S.wpn && WPN){ const q = S.wpn, y = 70 + (1 - Math.min(1, q * 1.6)) * -20, a = q < .7 ? Math.min(1, q * 4) : (1 - q) / .3; g.globalAlpha = a; g.drawImage(WPN, 0, S.sel * 64, 64, 64, 160 - 32, y, 64, 64); g.globalAlpha = 1; } };
    requestAnimationFrame(draw);
    const anim = (ms, fn) => new Promise(res => { const t0 = performance.now(); const s = () => { const q = Math.min(1, (performance.now() - t0) / ms); fn(ease(q), q); if (q < 1) requestAnimationFrame(s); else res(); }; s(); });
    const fl = v.querySelector('.fline'), nm = v.querySelector('.fname'), say = async (t, hold = 1800) => { fl.style.opacity = 1; fl.innerHTML = [...t].map(c => `<span>${c === ' ' ? ' ' : c}</span>`).join(''); for (const s of fl.children){ await sleep(s.textContent === '.' ? 140 : 80); s.classList.add('on'); } await sleep(hold); fl.style.opacity = 0; await sleep(700); };
    const fade = v.querySelector('.ffade'); fade.style.opacity = 1; requestAnimationFrame(() => v.classList.add('on')); await sleep(800); fade.style.opacity = 0; await sleep(900);
    const r1 = anim(2600, e => { S.rune = e; S.dark = e; }); await say('....탐사 문 기둥에 새겨진 글자가 빛나요.', 900); await r1;
    const r2 = anim(3200, e => { S.rise = e; }); await say('옛 모험가들의 혼이에요. 하나가 나와 함께 가 줄 거예요.', 1200); await r2;
    // 고르기
    const pk = v.querySelector('.sjpick'), det = pk.querySelector('.sjdet'); pk.classList.add('on'); fl.style.opacity = 0;
    const pick = await new Promise(res => { let cur = -1; const show = i => { cur = i; S.sel = -1; pk.querySelectorAll('.sjc').forEach(b => b.classList.toggle('on', +b.dataset.sj === i)); const [k, n, r, c, br] = JOBS[i];
        det.innerHTML = `<div class="t" style="color:${c}">${n} <span style="color:${RC[r]};font-size:12px">${r}</span>${bd(rec(o.first, r))}<small>${br}${why(o.first, r, o.firstN) ? ' · ' + why(o.first, r, o.firstN) : ''}</small></div><button class="g" data-no>다시 볼래요</button><button data-ok>받아들이기</button>`; S.hl = i;
        det.querySelector('[data-ok]').onclick = () => res(cur); det.querySelector('[data-no]').onclick = () => { pk.querySelectorAll('.sjc').forEach(b => b.classList.remove('on')); det.innerHTML = '<div class="t">혼을 하나 골라요<small>고르면 바꿀 수 없어요</small></div>'; }; };
      pk.querySelectorAll('.sjc').forEach(b => b.onclick = () => { const i = +b.dataset.sj; if (TAKEN[JOBS[i][0]]) return; show(i); });
      if (o.auto) (async () => { for (const i of o.auto.slice(0, -1)){ await sleep(1400); pk.querySelector(`[data-sj="${i}"]`).click(); } await sleep(1800); pk.querySelector(`[data-sj="${o.auto.at(-1)}"]`).click(); await sleep(2200); det.querySelector('[data-ok]').click(); })(); });
    pk.classList.remove('on'); S.sel = pick; const J = JOBS[pick];
    await anim(1400, e => { S.selK = e; S.gone = e; S.dark = 1 + e * .4; });
    await sleep(400); await anim(1700, e => { S.enter = e; });
    S.burst = performance.now(); S.glow = 1; await sleep(500); await anim(1500, e => { S.wpn = e; }); S.wpn = 0;
    nm.style.cssText = `color:${J[3]};opacity:1`; nm.innerHTML = J[1].split('').map(c => `<span>${c}</span>`).join(''); for (const s of nm.children){ await sleep(300); s.classList.add('on'); }
    await sleep(900); nm.style.opacity = .4; await say(`${J[1]}의 혼이 깃들었어요.`, 1000); await say('이제 떠나기 전에 두 직업 중 하나를 골라 가요.', 1600);
    fade.style.opacity = 1; await anim(600, e => { S.glow = 1 - e; }); await sleep(400); live = false; v.remove(); return J[0];
  }
  // ---------- 2) 탐사 로비 위쪽: 1차 / 2차 ----------
  const CSS = `<style>.sjsw{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sjj{position:relative;display:flex;align-items:center;gap:8px;min-height:64px;padding:8px 10px;border-radius:12px;border:2px solid var(--line,#4E3C72);background:var(--panel2,#211a36);color:inherit;font:inherit;text-align:left}
    .sjj .tg{position:absolute;left:8px;top:-9px;padding:0 7px;border-radius:7px;font-size:11px;line-height:17px;background:#4E3C72;color:#F1E9FF}.sjj b{display:block;font-size:15px;line-height:19px}.sjj small{display:block;font-size:11px;line-height:15px;opacity:.85}.sjj .ic{width:40px;height:40px;flex:none;display:grid;place-items:center}.sjj .ic img,.sjj .ic canvas,.sjj .ic svg{width:40px;height:40px}
    .sjj.on{border-color:var(--gold,#FFB84D);background:rgba(255,184,77,.13);box-shadow:0 0 0 2px rgba(255,184,77,.25)}.sjj.on .tg{background:var(--gold,#FFB84D);color:#2A1506}.sjj .go{margin-left:auto;font-size:11px;color:var(--gold,#FFB84D);font-weight:800}.sjj.lock{opacity:.55;border-style:dashed}.sjj:disabled{cursor:default}.sjst{margin-top:6px;font-size:12px;opacity:.8}</style>`;
  function lobby(st){   // st: { cur: 0|1, sub: 'paladin' | null, lv1, lv2, locked }
    const box = [...document.querySelectorAll('.box.px')].find(b => /HP \d/.test(b.textContent)); if (!box) return false; if (!box.dataset.orig) box.dataset.orig = box.innerHTML;
    const tmp = document.createElement('div'); tmp.innerHTML = box.dataset.orig; const ic1 = tmp.querySelector('.big')?.firstElementChild?.outerHTML || '', m = tmp.querySelector('b').textContent.match(/· (\S+) Lv (\d+)/), n1 = m ? m[1] : '1차', L1 = st.lv1 || (m ? +m[2] : 1);
    const sj = st.sub && JOBS.find(j => j[0] === st.sub), ji = sj ? JOBS.indexOf(sj) : -1, rest = '쉬는 중 · 경험치 20 %', dis = st.locked ? ' disabled' : '';
    const stat = st.cur ? 'HP 1820 · 공 96 · 마 64 · 치 88 · 속 41' : (tmp.querySelector('.s.sub')?.textContent || '');
    box.innerHTML = `${CSS}<div class="sjsw"><button class="sjj${st.cur ? '' : ' on'}" data-sjc="0"${dis}><span class="tg">1차</span><span class="ic">${ic1}</span><span><b>${n1}</b><small>Lv ${L1}</small><small>${st.cur ? rest : '이번에 가요'}</small></span></button>
      ${sj ? `<button class="sjj${st.cur ? ' on' : ''}" data-sjc="1"${dis}><span class="tg">2차</span><span class="ic" data-sjic></span><span><b style="color:${sj[3]}">${sj[1]}</b><small>Lv ${st.lv2 || 1}</small><small>${st.cur ? '이번에 가요' : rest}</small></span></button>`
        : `<button class="sjj lock" disabled><span class="tg">2차</span><span class="ic" style="font-size:22px;opacity:.6">?</span><span><b>비어 있어요</b><small>1차 Lv 20 에 열려요</small></span></button>`}</div>
      <div class="sjst">${st.locked ? '준비를 누르면 직업을 바꿀 수 없어요 · ' : ''}${stat}</div>`;
    if (sj){ const c = box.querySelector('[data-sjic]'); c.replaceWith(iconCv(ji, sj[3])); }
    box.querySelectorAll('[data-sjc]').forEach(b => b.onclick = () => lobby({ ...st, cur: +b.dataset.sjc }));
    // 아래 버튼 이름도 고른 직업을 따라가요
    const nm = st.cur && sj ? sj[1] : n1; [['#xwp', '무기 강화'], ['#xar', '방어구 강화'], ['#xst', '스탯'], ['#xtree', '스킬 트리']].forEach(([s, t]) => { const b = document.querySelector(s); if (!b) return; if (!b.dataset.orig) b.dataset.orig = b.textContent; b.textContent = b.dataset.orig.replace(t, `${nm} ${t}`); });
    return true;
  }
  window.__sj = { JOBS, cut, lobby, load };
})();
