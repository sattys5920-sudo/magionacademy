// 직업별 스킬 이펙트 (탐사 전투). 키는 `직업:모양` — 모양 첫 글자 n 보통 · b 센 스킬, h 가 붙으면 회복.
// 2~4px 네모 점만 써서 그려요. 그림 크기: 몸 가운데 = (x, y-14), 발밑 = (x, y).
(function(){
  const COL = { warrior: '#ff7a3a', black: '#b070ff', thief: '#7ae8ff', bard: '#ffb0d8', time: '#9ad8ff', alch: '#8aff6a', white: '#fff0a0', druid: '#7aef6a', cleric: '#ffe27a', knight: '#9ad0ff', summon: '#6affd8', gadget: '#ffb040' };
  const HEAL = { white: 1, druid: 1, cleric: 1, bard: 1 };
  const kind = (job, sk) => {
    if (!COL[job]) return null; const t = sk && sk.t;
    if (t === 'heal' || t === 'revive') return HEAL[job] ? `${job}:${(sk.mp || 0) >= 14 ? 'b' : 'n'}h` : null;
    if (t === 'buff' || t === 'mp' || t === 'deb' || t === 'summon' || t === 'leap' || t === 'tstop' || t === 'encore') return null;
    return `${job}:${(sk.mp || 0) >= 14 ? 'b' : 'n'}`;
  };
  function draw(g, f, x, y, now){
    const p = (now - f.t0) / f.dur; if (p < 0) return true; if (p >= 1) return false;
    const [job, v] = f.k.split(':'), big = v[0] === 'b', heal = v.includes('h'), C = COL[job], cx = x, cy = y - 14, fade = 1 - p * p, S = Math.sin, K = Math.cos, PI = Math.PI;
    const R = (a, b, w, h, c, al) => { g.globalAlpha = al ?? 1; g.fillStyle = c; g.fillRect(Math.round(a), Math.round(b), w, h); g.globalAlpha = 1; };
    const rn = i => { const t = Math.sin(f.seed * 97 + i * 12.9898) * 43758.5453; return t - Math.floor(t); };
    const plus = (a, b, c, al) => { R(a - 1, b, 3, 1, c, al); R(a, b - 1, 1, 3, c, al); };
    const star = (a, b, c, al, s = 2) => { R(a - s, b, s * 2 + 1, 1, c, al); R(a, b - s, 1, s * 2 + 1, c, al); R(a - 1, b - 1, 3, 3, '#fff', al); };
    const ring = (ox, oy, rx, ry, n, c, al, ph = 0, s = 2) => { for (let i = 0; i < n; i++){ const a = i * 2 * PI / n + ph; R(ox + K(a) * rx, oy + S(a) * ry, s, s, c, al); } };
    const line = (x0, y0, x1, y1, c, al, s = 3, t = 1) => { const n = Math.max(2, Math.round(Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)) / 2)); for (let i = 0; i <= n * t; i++){ const q = i / n; R(x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, s, s, i > n * t - 3 ? '#fff' : c, al); } };
    const shock = (r, c, al) => ring(cx, y, r, r * .32, Math.max(10, Math.round(r / 2)), c, al, 0, 2);
    const q1 = Math.min(1, p / .4), q2 = Math.min(1, p / .6);
    const sway = (i, a) => S(p * 7 + i * 2) * a;
    switch (job + (heal ? 'h' : '')){
      case 'warrior': {   // 묵직한 도끼 내려찍기
        const n = big ? 3 : 1;
        for (let i = 0; i < n; i++) line(cx - 22 + i * 8, y - 50 + i * 3, cx + 12 + i * 8, y - 6 + i * 3, i === 1 ? '#fff0c0' : C, fade, big ? 4 : 3, q1);
        if (p > .3){ const q = (p - .3) / .7; for (let i = 0; i < (big ? 5 : 3); i++){ const a = -PI * .5 + (i - (big ? 2 : 1)) * .55; line(cx, y, cx + K(a) * 30 * q * (big ? 1.4 : 1), y + S(a) * 6 * q + 2, '#ffb070', fade, 2, 1); } }
        if (big && p > .3){ shock(8 + (p - .3) * 70, C, fade); shock(4 + (p - .3) * 46, '#fff0c0', fade * .8); }
        for (let i = 0; i < (big ? 12 : 5); i++){ const q = Math.max(0, p - .3) / .7; R(cx - 14 + rn(i) * 28, y - 4 - S(q * PI) * (10 + rn(i + 9) * 20), 3, 3, i % 2 ? '#8a6a4a' : '#c0a070', fade * (p > .3 ? 1 : 0)); }
        if (p < .45 && p > .3) R(cx - 16, y - 10, 32, 10, '#fff', .45 - (p - .3) * 3);
        break; }
      case 'knight': {   // 푸른 칼날 + 방패 번쩍
        if (!big){ const a0 = -1.3, a1 = 1.3; for (let i = 0; i < 22 * q1; i++){ const a = a0 + (a1 - a0) * i / 22; R(cx + K(a - 1.57) * 22 + 2, cy + S(a - 1.57) * 20 - 6, 4, 4, i > 22 * q1 - 6 ? '#fff' : C, fade); } plus(cx + 12, cy + 2, '#fff', fade * (p > .3 ? 1 : 0)); }
        else { const dq = Math.min(1, p / .3); const by = y - 100 + dq * 94; R(cx - 3, by - 40, 7, 40, '#e8f4ff', p < .45 ? 1 : fade * .5); R(cx - 5, by - 6, 11, 3, '#ffd866', p < .45 ? 1 : 0); R(cx - 1, by, 3, 6, '#fff', p < .45 ? 1 : 0);
          if (p > .28){ const q = (p - .28) / .72; shock(6 + q * 54, C, fade); shock(3 + q * 34, '#fff', fade); for (let i = 0; i < 14; i++) plus(cx + K(i * .45) * (6 + q * 38), y - 6 - S(i * .45) * q * 24 - q * 10, i % 2 ? '#fff' : C, fade); if (p < .4) R(cx - 20, y - 24, 40, 24, '#e8f6ff', .6 - (p - .28) * 5); } }
        break; }
      case 'thief': {   // 번쩍이는 연속 베기
        const N = big ? 6 : 3;
        for (let i = 0; i < N; i++){ const t0 = i * (big ? .09 : .14); if (p < t0) continue; const q = Math.min(1, (p - t0) / .16), a = -.9 + rn(i) * 1.8 + (i % 2 ? 1.2 : -.3), dx = K(a) * 24, dy = S(a) * 24; line(cx - dx, cy - dy, cx + dx, cy + dy, i % 2 ? '#ffffff' : C, Math.max(0, 1 - (p - t0) * 1.6), 2, q); }
        if (big && p > .55){ const q = Math.min(1, (p - .55) / .12); line(cx - 22, cy - 22, cx + 22, cy + 22, '#ff4a5a', fade + .2, 4, q); line(cx + 22, cy - 22, cx - 22, cy + 22, '#ff4a5a', fade + .2, 4, q); if (p < .75) R(cx - 6, cy - 6, 12, 12, '#fff', .8 - (p - .55) * 4); }
        for (let i = 0; i < 6; i++) R(cx - 20 + rn(i + 30) * 40, cy - 16 + rn(i + 40) * 32, 2, 2, '#1a2a3a', fade * .7);
        break; }
      case 'black': {   // 어둠 불꽃 구슬 → 폭발
        if (big){ ring(cx, y, 30, 9, 28, '#8a3ac0', Math.min(1, p * 4) * fade, p * 3); ring(cx, y, 20, 6, 18, '#d09aff', Math.min(1, p * 4) * fade, -p * 4); for (let i = 0; i < 6; i++){ const a = i * 1.047 + p * 3; R(cx + K(a) * 26 - 1, y + S(a) * 8 - 1, 3, 3, '#fff', fade); }
          if (p > .25){ const q = Math.min(1, (p - .25) / .3); const h = 78 * q; for (let i = 0; i < 4; i++) R(cx - 8 + i * 4, y - h, 4, h, ['#3a1060', '#6a2aa0', '#b070ff', '#6a2aa0'][i], fade * .9); for (let i = 0; i < 16; i++) R(cx - 10 + rn(i) * 20, y - ((p * 90 + i * 17) % 80), 3, 3, i % 2 ? '#ff5aa0' : '#d09aff', fade); } }
        else { if (p < .5){ for (let i = 0; i < 10; i++){ const a = i * .63 + p * 12, r = 30 * (1 - p * 2) + 4; R(cx + K(a) * r, cy + S(a) * r * .8, 4, 4, i % 2 ? '#6a2aa0' : '#d09aff', 1); } R(cx - 4, cy - 4, 9, 9, '#2a0a40'); ring(cx, cy, 8, 8, 10, '#ff5aa0', 1, p * 9, 2); }
          else { const q = (p - .5) / .5; for (let i = 0; i < 12; i++){ const a = i * .52; R(cx + K(a) * q * 28, cy + S(a) * q * 25, 4, 4, i % 2 ? '#ff5aa0' : '#b070ff', 1 - q); if (i % 3 === 0) plus(cx + K(a) * q * 18, cy + S(a) * q * 16, '#fff', 1 - q); } } }
        break; }
      case 'time': {   // 시계 고리 + 돌아가는 바늘
        const r = big ? 26 : 15, a = Math.min(1, p * 5) * fade;
        ring(cx, cy, r, r, big ? 36 : 24, C, a, 0); for (let i = 0; i < 12; i++){ const b = i * PI / 6; R(cx + K(b) * (r - 4) - 1, cy + S(b) * (r - 4) - 1, i % 3 ? 2 : 3, i % 3 ? 2 : 3, '#fff', a); }
        const h1 = p * (big ? 18 : 12) - PI / 2, h2 = h1 * 6 - PI / 2 * 5; line(cx, cy, cx + K(h1) * r * .5, cy + S(h1) * r * .5, '#fff', a, 2); line(cx, cy, cx + K(h2) * r * .8, cy + S(h2) * r * .8, C, a, 2);
        if (big){ ring(cx, cy, r + 8 + p * 20, r + 8 + p * 20, 28, '#d8f0ff', fade * .6, p, 2); for (let i = 0; i < 12; i++) R(cx - 12 + rn(i) * 24, cy - 40 + ((p * 60 + i * 11) % 52), 2, 2, '#ffe6a0', fade); for (let i = 0; i < 3; i++) R(cx - 10 - i * 4, cy - 2 - i * 5, 1 + i * 2, 1, '#9ad8ff', fade * .5 * (1 - i / 3)); }
        break; }
      case 'alch': {   // 보글보글 용액 튀김
        for (let i = 0; i < (big ? 18 : 13); i++){ const t = (p * 1.2 + rn(i) * .5) % 1, bx = cx - 14 + rn(i + 3) * 28 + S(t * 8 + i) * 3, by = y - t * (big ? 52 : 34) - 2, s = 4 + (i % 3) * (big ? 2 : 2); g.globalAlpha = (1 - t) * fade; g.strokeStyle = i % 2 ? '#bfff9a' : '#c07aff'; g.lineWidth = 1; g.strokeRect(Math.round(bx) + .5, Math.round(by) + .5, s, s); g.globalAlpha = 1; R(bx + 1, by + 1, 1, 1, '#fff', (1 - t) * fade); }
        for (let i = 0; i < 10; i++){ const a = i * .63, q = Math.min(1, p * 2.4); R(cx + K(a) * q * (big ? 26 : 16), y - 6 + S(a) * q * (big ? 8 : 5), 3, 3, i % 2 ? '#7adf5a' : '#a05ad0', (1 - q * .7) * fade); }
        if (big){ g.globalAlpha = .35 * Math.sin(p * PI); g.fillStyle = '#8aff6a'; g.beginPath(); g.ellipse(cx, cy, 24 + p * 10, 18, 0, 0, 7); g.fill(); g.globalAlpha = 1; for (let i = 0; i < 6; i++) star(cx - 20 + rn(i + 50) * 40, cy - 20 + rn(i + 60) * 30, '#ffd866', fade, 2); }
        break; }
      case 'bard': {   // 소리 파동 + 음표
        for (let i = 0; i < (big ? 5 : 3); i++){ const t = p * 1.3 - i * .15; if (t < 0 || t > 1) continue; const r = 5 + t * (big ? 34 : 22); ring(cx, cy, r, r * .8, Math.round(8 + r / 2), i % 2 ? '#ffd866' : C, (1 - t) * .9, i); }
        for (let i = 0; i < (big ? 9 : 5); i++){ const a = i * (2 * PI / (big ? 9 : 5)) + .3, r = 8 + p * (big ? 38 : 24), nx = cx + K(a) * r, ny = cy + S(a) * r * .8 - p * 6; R(nx, ny, 3, 3, ['#ffd866', '#ff9ac0', '#9ad8ff'][i % 3], fade); R(nx + 2, ny - 5, 1, 5, '#fff', fade); if (i % 2) R(nx + 2, ny - 5, 3, 1, '#fff', fade); }
        break; }
      case 'bardh': {   // 부드러운 선율
        for (let i = 0; i < 4; i++) R(cx - 18, cy - 14 + i * 5 - p * 4, 36, 1, '#ffe0f0', fade * .6);
        for (let i = 0; i < (big ? 9 : 6); i++){ const nx = cx - 16 + i * (big ? 4 : 6) + sway(i, 2), ny = cy + 8 - p * 40 * (.5 + rn(i) * .7); R(nx, ny, 3, 3, i % 2 ? '#7affb0' : '#ffb0d8', fade); R(nx + 2, ny - 5, 1, 5, '#fff', fade); plus(nx + 5, ny + 3, '#fff', fade); }
        if (big) ring(cx, y, 10 + p * 28, 3 + p * 9, 20, '#ffd8ec', fade, 0);
        break; }
      case 'white': {   // 성스러운 빛줄기
        const w = big ? 16 : 6; R(cx - w / 2, y - 80, w, 76 + 6, '#fffbe0', fade * .55); R(cx - w / 4, y - 80, w / 2, 80, '#fff', fade * .9);
        for (let i = 0; i < (big ? 14 : 6); i++) star(cx - 16 + rn(i) * 32, y - 4 - p * 36 * (.4 + rn(i + 9)), '#fff6c0', fade, 1 + (i % 2));
        if (big) shock(6 + p * 40, '#fff0a0', fade);
        break; }
      case 'whiteh': {   // 깃털과 날개
        if (big){ for (let s = -1; s <= 1; s += 2) for (let i = 0; i < 6; i++){ const e = Math.min(1, p * 4) * (1 - Math.max(0, p - .7) * 3); line(cx + s * 4, cy - 6, cx + s * (10 + i * 5) * e, cy - 6 - (14 - i * 3) * e - i * 2, i % 2 ? '#fff' : '#fff0a0', .9 * Math.max(0, e), 3, 1); } shock(4 + p * 30, '#fff0a0', fade * .7); }
        for (let i = 0; i < (big ? 14 : 8); i++){ const t = (p * 1.1 + rn(i) * .35) % 1, fx = cx - 16 + rn(i + 2) * 32 + sway(i, 4), fy = cy - 34 + t * 44; R(fx, fy, 3, 1, '#fff', fade); R(fx + 1, fy + 1, 2, 1, '#e0f0ff', fade); }
        for (let i = 0; i < 5; i++) plus(cx - 12 + i * 6, y - 2 - p * 24 * (.5 + rn(i + 20)), '#9affc8', fade);
        break; }
      case 'druid': {   // 가시덩굴
        for (let i = 0; i < (big ? 6 : 3); i++){ const bx = cx - (big ? 20 : 10) + i * (big ? 8 : 10), h = (big ? 56 : 34) * Math.min(1, p * 2.4) * (.7 + rn(i) * .5); for (let k = 0; k < h; k += 2){ const sx = bx + S(k * .22 + i + p * 4) * (3 + k * .06); R(sx, y - k, 3, 2, k % 6 < 2 ? '#2f8a3a' : '#5fcf5a', fade); if (k % 8 === 4) R(sx + (i % 2 ? 3 : -2), y - k - 1, 2, 2, '#e0ffb0', fade); } R(bx - 1, y - h - 2, 4, 3, '#b9ff8a', fade); }
        if (big){ shock(6 + p * 36, '#5fcf5a', fade); for (let i = 0; i < 12; i++) R(cx - 20 + rn(i + 5) * 40, y - 4 - S(Math.min(1, p * 1.6) * PI) * (12 + rn(i) * 26), 3, 2, i % 2 ? '#5fcf5a' : '#b9ff8a', fade); }
        break; }
      case 'druidh': {   // 초록 나선
        for (let i = 0; i < (big ? 16 : 9); i++){ const a = i * .7 + p * 6, r = 8 + (i % 3) * 3 + (big ? 6 : 0); R(cx + K(a) * r, y + 4 - ((p * 1.1 + i / (big ? 16 : 9)) % 1) * 40, 3, 2, i % 2 ? '#5fcf5a' : '#b9ff8a', fade); }
        for (let i = 0; i < 4; i++) plus(cx - 10 + i * 7, y - 6 - p * 26 * (.5 + rn(i)), '#c8ffd0', fade);
        if (big){ shock(4 + p * 30, '#5fcf5a', fade); g.globalAlpha = .3 * Math.sin(p * PI); g.fillStyle = '#7aef6a'; g.beginPath(); g.ellipse(cx, y - 2, 24, 8, 0, 0, 7); g.fill(); g.globalAlpha = 1; }
        break; }
      case 'cleric': {   // 금빛 십자 응징
        const L = big ? 34 : 20, a = (p < .2 ? p * 5 : 1) * fade; R(cx - 2, cy - L, 5, L * 2, C, a); R(cx - L * .6, cy - 8, L * 1.2, 5, C, a); R(cx - 1, cy - L, 3, L * 2, '#fff', a); R(cx - L * .6, cy - 7, L * 1.2, 3, '#fff', a);
        if (p < .3) R(cx - 12, cy - 12, 24, 24, '#fffbd0', .6 - p * 2);
        if (big){ R(cx - 8, y - 110, 16, 104, '#fff4b0', fade * .45); shock(6 + p * 44, C, fade); for (let i = 0; i < 8; i++){ const b = i * PI / 4 + .2; line(cx + K(b) * 8, cy + S(b) * 8, cx + K(b) * (16 + p * 26), cy + S(b) * (16 + p * 26), '#fff0a0', fade * .8, 2, 1); } }
        break; }
      case 'clerich': {   // 금빛 십자 + 반짝임
        const a = Math.sin(p * PI); R(cx - 1, cy - (big ? 28 : 18) - p * 10, 3, (big ? 34 : 22), C, a); R(cx - (big ? 8 : 5), cy - (big ? 18 : 10) - p * 10, (big ? 17 : 11), 3, C, a);
        for (let i = 0; i < (big ? 10 : 6); i++) star(cx - 14 + rn(i) * 28, y - 2 - p * 34 * (.4 + rn(i + 4)), '#fff6c0', fade, 1);
        if (big){ shock(4 + p * 30, C, fade * .8); R(cx - 6, y - 90, 12, 86, '#fff4b0', a * .4); }
        break; }
      case 'summon': {   // 소환진 + 영혼불 · 센 스킬은 영혼의 발톱
        const e = Math.min(1, p * 4); ring(cx, y, (big ? 28 : 18) * e, (big ? 9 : 6) * e, big ? 26 : 16, C, fade, p * 4); ring(cx, y, (big ? 16 : 10) * e, (big ? 5 : 3) * e, 12, '#fff', fade * .8, -p * 5);
        for (let i = 0; i < (big ? 10 : 6); i++){ const a = i * 1.1 + p * 6, r = 14 * (1 - p * .6), py = y - 4 - ((p * 1.2 + i * .17) % 1) * 44; R(cx + K(a) * r, py, 3, 3, i % 2 ? C : '#c0ffee', fade); R(cx + K(a) * r + 1, py + 3, 1, 3, C, fade * .5); }
        if (big && p > .25) for (let i = -1; i <= 1; i++){ const q = Math.min(1, (p - .25) / .25); line(cx + i * 9 - 14, cy - 28, cx + i * 9 + 8, cy + 14, i ? '#a070ff' : '#fff', fade, 3, q); }
        break; }
      case 'gadget': {   // 불꽃 + 톱니 튀김 · 센 스킬은 로켓 폭격
        if (!big){ if (p < .3) star(cx, cy, '#fff6a0', 1 - p * 2, 5); for (let i = 0; i < 8; i++){ const a = i * .8, r = 3 + p * 20; R(cx + K(a) * r - 1, cy + S(a) * r - 1, 3, 3, i % 3 ? '#ffb040' : '#cfd6e0', fade); }
          for (let i = 0; i < 3; i++){ const gx = cx - 10 + i * 10 + sway(i, 3), gy = cy - p * 20 - i * 3; R(gx - 2, gy - 2, 5, 5, '#8a95a8', fade); R(gx, gy, 1, 1, '#1a1024', fade); } }
        else for (let i = 0; i < 4; i++){ const t0 = i * .15, q = (p - t0) / .4; if (q < 0) continue; const bx = cx - 18 + i * 12, tx = bx, sy2 = y - 100;
          if (q < 1){ const my = sy2 + (y - 8 - sy2) * q; for (let k = 0; k < 6; k++) R(tx + k * .8, my - k * 5, 3, 3, k < 2 ? '#fff6a0' : k < 4 ? '#ff9a3a' : '#8a8a96', .9 - k * .12); R(tx - 1, my, 5, 7, '#dfe6f0'); R(tx, my + 7, 3, 3, '#ff5a3a'); }
          else { const e = Math.min(1, (q - 1) * 2.2); ring(tx, y - 6, 4 + e * 18, 2 + e * 8, 14, i % 2 ? '#ffd04a' : '#ff7a2a', 1 - e, i); R(tx - 6 + e * 4, y - 14 + e * 4, 12 - e * 8, 10 - e * 8, '#fff6d0', (1 - e) * .9); for (let k = 0; k < 4; k++) R(tx - 8 + k * 5, y - 12 - e * 20 - k * 2, 5, 5, '#6a6a76', (1 - e) * .6); } }
        break; }
    }
    return true;
  }
  window.XFXJOB = { kind, draw, COL };
})();
