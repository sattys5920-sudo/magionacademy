// 새 직업 12 종 스킬 이펙트 (xfx2.js 뒤에 불러와요). xfx2 의 부품(LIB)에 새 부품을 더하고, 스킬마다 층을 겹쳐요.
// 아직 게임에는 안 붙였어요. tools/newjobs/fx_run.js 가 모의 화면에서 영상으로 찍어요.
(function(){
  const X = window.XFXJOB; if (!X || !X.LIB2) return;
  const S = Math.sin, K = Math.cos, PI = Math.PI, L = X.LIB2, T = X.T2;
  const FI3 = ['#ff5a2a', '#ff9a3a', '#ffd04a'];
  const ease = t => t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t);
  // ---------- 새 부품 ----------
  Object.assign(L, {
    arrow(c, q, o){ const N = o.n || 1, Z = o.s || 1; for (let i = 0; i < N; i++){ const qq = (q - i * .1) / .38; if (qq < 0) continue; const ay = c.cy - 6 + (i - (N - 1) / 2) * 6;
      if (qq < 1){ const ax = c.cx - 120 + 120 * qq, col = o.c; c.R(ax - 16 * Z, ay, 16 * Z, Z > 1.2 ? 2 : 1, '#c8a878'); c.R(ax, ay - 1, 4 * Z, 3, o.k ? col : '#dfe6f0'); c.R(ax - 18 * Z, ay - 2, 3, 2, col); c.R(ax - 18 * Z, ay + 1, 3, 2, col);
        if (o.k === 'fire') for (let k = 0; k < 8; k++) c.R(ax - c.rn(k + i * 9) * 22, ay - 3 + c.rn(k + 30) * 6, 3, 3, k % 2 ? '#ff7a2a' : '#ffd04a', .9);
        if (o.k === 'ice') for (let k = 0; k < 6; k++) c.plus(ax - k * 5, ay + S(k * 2 + q * 20) * 3, '#dff8ff', .8);
        if (o.k === 'bolt') for (let k = 0; k < 5; k++) c.R(ax - k * 5, ay + ((k + Math.floor(q * 30)) % 3 - 1) * 3, 4, 1, '#fff6a0', .9);
        if (Z > 1.2) c.R(ax - 60, ay, 44, 1, '#fff', .4); }
      else { const e = Math.min(1, (qq - 1) * 2.6); if (e < 1) for (let k = 0; k < 8; k++){ const a = k * PI / 4; c.R(c.cx + K(a) * e * 16 * Z, ay + S(a) * e * 14 * Z, 2, 2, k % 2 ? o.c : '#fff', 1 - e); } } } },
    arrows(c, q, o){ for (let i = 0; i < (o.n || 10); i++){ const t0 = c.rn(i) * .5, qq = (q - t0) / .3; if (qq < 0) continue; const gx = c.cx - 30 + c.rn(i + 9) * 60;
      if (qq < 1){ const x = gx + (1 - qq) * 22, y = c.y - 112 + qq * 104; if (o.k === 'sword'){ c.R(x - 1, y - 4, 3, 16, '#e8f4ff'); c.R(x, y - 4, 1, 16, '#fff'); c.R(x - 3, y - 6, 7, 2, o.c); c.R(x - 1, y - 10, 3, 4, '#8a6a4a'); } else { c.R(x, y, 1, 12, '#c8a878'); c.R(x - 1, y + 12, 3, 3, '#dfe6f0'); c.R(x - 1, y - 2, 3, 3, o.c); } }
      else if (qq < 1.7){ const e = (qq - 1) / .7; c.star(gx, c.y - 6, o.c, 1 - e, 2); c.R(gx, c.y - 16, 1, 10, o.k === 'sword' ? '#e8f4ff' : '#c8a878', 1 - e); } } },
    bullet(c, q, o){ const N = o.n || 3, gap = o.gap || .1, Z = o.s || 1; for (let i = 0; i < N; i++){ const qq = (q - i * gap) / .14; if (qq < 0) continue; const jy = o.v === 1 ? (c.rn(i + 3) - .5) * 22 : (i % 3 - 1) * 3;
      if (o.v === 2){ if (qq < 1) for (let k = 0; k < 9; k++){ const a = (k - 4) * .07; c.R(c.cx - 130 + 130 * qq, c.cy - 6 + S(a) * 130 * qq, 4, 2, k % 2 ? o.c : '#ffe07a'); } else if (qq < 3) for (let k = 0; k < 5; k++) c.plus(c.cx - 10 + c.rn(k) * 24, c.cy - 16 + c.rn(k + 5) * 24, '#fff', 1 - (qq - 1) / 2); continue; }
      if (qq < 1){ const bx = c.cx - 130 + 130 * qq; c.R(bx - 14 * Z, c.cy - 6 + jy, 14 * Z, 2 * Z, o.c, .5); c.R(bx - 4 * Z, c.cy - 6 + jy, 5 * Z, 2 * Z, '#fff'); }
      else if (qq < 2.5){ const e = (qq - 1) / 1.5; c.star(c.cx - 2, c.cy - 6 + jy, '#ffe07a', 1 - e, 3 * Z); for (let k = 0; k < 4; k++) c.R(c.cx - 4 - e * 10 * Z, c.cy - 8 + jy + (k - 1.5) * 4 * e, 2, 2, o.c, 1 - e); } } },
    scope(c, q, o){ const sh = o.v === 1 ? 2 : .6, cy = c.cy - 8; if (q < sh){ const e = ease(q / Math.min(sh, .55)), r = 24 - 14 * e; c.ring(c.cx, cy, r, r, 24, o.c, .9, q * 2, 1); c.R(c.cx - r - 6, cy, r * 2 + 13, 1, o.c, .9); c.R(c.cx, cy - r - 6, 1, r * 2 + 13, o.c, .9); c.R(c.cx - 1, cy - 1, 3, 3, '#fff', S(q * 40) > 0 ? 1 : .3); if (o.v === 1) for (let i = 0; i < 4; i++) c.R(c.cx - r - 2 + (i % 2) * (r * 2 + 2), cy - r - 2 + (i > 1) * (r * 2 + 2), 3, 3, '#fff', c.fade(q)); }
      else { const e = (q - sh) / (1 - sh); c.R(c.cx - 150, cy, 150, 2, '#fff', 1 - e); c.R(c.cx - 150, cy - 2, 150, 6, o.c, (1 - e) * .3); c.star(c.cx, cy, '#fff', 1 - e, 10 - e * 6); c.shock(4 + e * 30, o.c, 1 - e, c.cx, cy + 10); } },
    fist(c, q, o){ const N = o.n || 3, Z = o.s || 1; for (let i = 0; i < N; i++){ const qq = (q - i * (.62 / N)) / .26; if (qq < 0 || qq > 1) continue; const px = c.cx - 8 + (i % 2) * 12 + (c.rn(i) - .5) * 8, py = c.cy - 10 + ((i * 7) % 3 - 1) * 7 - (o.v === 1 ? qq * 26 : 0), e = ease(qq * 3);
      c.R(px - 16 * (1 - e) - 5 * Z, py - 4 * Z, 10 * Z, 8 * Z, o.c2 || '#ffd8b0', 1 - qq * .6); c.R(px - 16 * (1 - e) + 3 * Z, py - 4 * Z, 2, 8 * Z, '#c89a70', 1 - qq * .6); c.R(px - 16 * (1 - e) - 9 * Z, py - 3 * Z, 4, 6 * Z, o.c, 1 - qq);
      if (e >= 1) for (let k = 0; k < 8; k++){ const a = k * PI / 4, r0 = 6 * Z, r1 = (8 + qq * 14) * Z; c.line(px + K(a) * r0, py + S(a) * r0, px + K(a) * r1, py + S(a) * r1, k % 2 ? o.c : '#fff', 1 - qq, 2, 1); } } },
    fan(c, q, o){ const N = o.n || 1; for (let i = 0; i < N; i++){ const qq = (q - i * .1) / .45; if (qq < 0) continue; if (qq < 1){ const x = c.cx - 110 + 110 * qq, y = c.cy - 10 - S(qq * PI) * 18 + (i - (N - 1) / 2) * 8;
        for (let a = 0; a < 6; a++){ const ang = q * 22 + i + a * .45; c.line(x, y, x + K(ang) * 9, y + S(ang) * 9, a % 2 ? o.c : o.c2 || '#ffe6a0', 1, 2, 1); } c.R(x - 1, y - 1, 3, 3, '#8a4a2a'); }
      else { const e = Math.min(1, (qq - 1) * 2); for (let k = 0; k < 7; k++){ const a = k * .9 + i; c.R(c.cx + K(a) * e * 22, c.cy - 8 + S(a) * e * 16 + e * 6, 3, 2, k % 2 ? o.c : '#fff0f8', 1 - e); } } } },
    hearts(c, q, o){ for (let i = 0; i < (o.n || 5); i++){ const t = (q * 1.2 + i / (o.n || 5)) % 1, hx = c.cx - 16 + i * 8 + S(t * 6 + i) * 4, hy = c.cy - 14 - t * 30; const a = (1 - t) * c.fade(q); c.R(hx - 3, hy, 3, 3, o.c, a); c.R(hx + 1, hy, 3, 3, o.c, a); c.R(hx - 2, hy + 3, 5, 2, o.c, a); c.R(hx, hy + 5, 1, 1, o.c, a); c.R(hx - 2, hy, 1, 1, '#fff', a); } },
    ribbon(c, q, o){ for (let k = 0; k < 2; k++) for (let i = 0; i < 30; i++){ const t = i / 30, a = q * 10 + t * 6 + k * PI, r = (14 + t * 6) * (o.s || 1); c.R(c.cx + K(a) * r, c.cy + 6 + S(a) * r * .4 - t * 26, 3, 2, k ? o.c : o.c2 || '#fff', c.fade(q) * (1 - t * .5)); } },
    haste(c, q, o){ for (let i = 0; i < 6; i++){ const yy = c.cy - 22 + i * 7, l = 8 + ((q * 70 + i * 13) % 20); c.R(c.cx - 22 - l, yy, l, 2, i % 2 ? o.c : '#fff', c.fade(q) * .85); }
      for (let k = 0; k < 2; k++){ const ax = c.cx + 12 + k * 6, ay = c.cy - 20 - ((q * 1.5 + k * .5) % 1) * 16; c.R(ax, ay, 2, 6, o.c, c.fade(q)); c.R(ax - 2, ay + 2, 6, 1, o.c, c.fade(q)); c.R(ax - 1, ay + 1, 4, 1, o.c, c.fade(q)); } },
    totem(c, q, o){ const tx = c.cx - 24, h = 30 * ease(q * 3), a = c.fade(Math.max(0, q - .5) * 2); c.R(tx - 3, c.y - h, 7, h, '#7a4a2a', a); c.R(tx - 3, c.y - h + 10, 7, 2, '#5a3218', a); c.R(tx - 5, c.y - h - 9, 11, 10, o.c2 || '#c83a3a', a); c.R(tx - 3, c.y - h - 6, 2, 2, '#fff', a); c.R(tx + 2, c.y - h - 6, 2, 2, '#fff', a); c.R(tx - 2, c.y - h - 2, 5, 1, '#1a0a0a', a); c.R(tx - 10, c.y - h - 6, 5, 3, o.c, a); c.R(tx + 6, c.y - h - 6, 5, 3, o.c, a);
      if (q > .3) for (let i = 0; i < 2; i++){ const k = ((q - .3) * 2 + i / 2) % 1; c.ring(tx, c.y - 2, 6 + k * 34, 2 + k * 10, 18, o.c, (1 - k) * a, 0); } },
    ofuda(c, q, o){ const N = o.n || 2; for (let i = 0; i < N; i++){ const qq = (q - i * .1) / .35; if (qq < 0) continue; const e = ease(Math.min(1, qq)), fx = c.cx - 100 * (1 - e) + (i - (N - 1) / 2) * 11, fy = c.cy - 12 + (i % 2) * 8 - S(e * PI) * 14, al = c.fade(q) * (qq >= 1 && S(q * 40) < -.6 ? .5 : 1);
      c.R(fx - 3, fy - 6, 7, 14, '#fff8e8', al); c.R(fx - 3, fy - 6, 7, 2, o.c, al); c.R(fx - 1, fy - 2, 3, 1, o.c, al); c.R(fx, fy - 2, 1, 7, o.c, al); c.R(fx - 1, fy + 3, 3, 1, o.c, al); if (qq >= 1) c.ring(fx, fy, 8 + (qq - 1) * 6, 8 + (qq - 1) * 6, 10, o.c, al * .6, q * 3, 1); } },
    kekkai(c, q, o){ const e = ease(q * 3), r = 26 * e; c.g.globalAlpha = .18 * c.fade(q); c.g.fillStyle = o.c; c.g.fillRect(c.cx - r, c.y - 52, r * 2, 52); c.g.globalAlpha = 1; c.ring(c.cx, c.y, r, r * .3, 26, o.c2 || '#fff', c.fade(q), 0, 2); c.R(c.cx - r, c.y - 54, r * 2, 2, '#e8d8a0', c.fade(q)); for (let i = 0; i < 4; i++) c.R(c.cx - r + 4 + i * r * .55, c.y - 52, 2, 6, '#fff8e8', c.fade(q));
      for (let i = 0; i < 4; i++){ const a = i * PI / 2 + q * 2, fx = c.cx + K(a) * r, fy = c.y - 26 + S(a) * 6; c.R(fx - 3, fy - 7, 7, 14, '#fff8e8', c.fade(q)); c.R(fx - 1, fy - 5, 3, 9, o.c, c.fade(q)); } },
    foxfire(c, q, o){ const N = o.n || 4; for (let i = 0; i < N; i++){ const a = q * 7 + i * 2 * PI / N, r = 26 * (1 - Math.max(0, q - .55) * 2.2), fx = c.cx + K(a) * r, fy = c.cy - 8 + S(a) * r * .5 - S(q * 9 + i) * 3, al = c.fade(Math.max(0, q - .3) / .7);
      c.R(fx - 3, fy - 2, 6, 6, o.c, al); c.R(fx - 2, fy - 5, 4, 3, o.c2 || '#fff', al); c.R(fx - 1, fy - 8, 2, 3, o.c2 || '#fff', al * .8); c.R(fx - 1, fy, 2, 2, '#fff', al); for (let k = 1; k < 4; k++) c.R(fx - K(a) * k * 3, fy - S(a) * k * 2, 3 - k * .6, 3 - k * .6, o.c, al * (.6 - k * .15)); } },
    shield(c, q, o){ const e = ease(q * 4), Z = (o.s || 1) * e, sx = c.cx + (o.v === 1 ? 8 + q * 14 : 14), sy = c.cy - 10, a = c.fade(q); if (Z <= 0) return; c.R(sx - 6 * Z, sy - 9 * Z, 13 * Z, 14 * Z, o.c, a * .55); c.R(sx - 4 * Z, sy + 5 * Z, 9 * Z, 3 * Z, o.c, a * .55); c.R(sx - 2 * Z, sy + 8 * Z, 5 * Z, 2 * Z, o.c, a * .55);
      c.R(sx - 6 * Z, sy - 9 * Z, 13 * Z, 2, '#fff', a); c.R(sx - 6 * Z, sy - 9 * Z, 2, 14 * Z, '#fff', a); c.R(sx + 6 * Z, sy - 9 * Z, 2, 14 * Z, o.c2 || '#fff', a); c.R(sx - 1, sy - 5 * Z, 2, 10 * Z, '#fff', a * .8); c.R(sx - 4 * Z, sy - 1, 9 * Z, 2, '#fff', a * .8); if (q > .2) c.star(sx - 4 * Z, sy - 7 * Z, '#fff', a * Math.abs(S(q * 12)), 2); },
    wave(c, q, o){ const Z = o.s || 1, wx = c.cx - 70 + q * 100; for (let j = 0; j < 3; j++) for (let yy = c.y - 46 * Z; yy < c.y; yy += 4){ const off = S(yy / 8 + q * 12) * 4 + (yy - c.y) * -.25; c.R(wx + off - j * 9, yy, 5, 4, j === 0 ? o.c2 || '#fff' : o.c, c.fade(q) * (.95 - j * .25)); }
      for (let i = 0; i < 6; i++) c.R(wx + 4 + c.rn(i) * 10, c.y - 46 * Z - 4 + c.rn(i + 4) * 8, 2, 2, '#fff', c.fade(q)); },
    drain(c, q, o){ for (let i = 0; i < (o.n || 18); i++){ const t = (q * 1.4 + c.rn(i)) % 1, sx = c.cx + (c.rn(i + 3) - .5) * 22, sy = c.cy - 8 + (c.rn(i + 5) - .5) * 22; c.R(sx - 140 * t, sy - S(t * PI) * 22, 3, 3, i % 3 ? o.c : o.c2 || '#fff', c.fade(q) * (1 - t * .4)); } },
    taunt(c, q, o){ const by = c.cy - 40 - Math.abs(S(q * 14)) * 4, a = c.fade(q); c.R(c.cx - 1, by, 4, 9, o.c, a); c.R(c.cx - 1, by + 11, 4, 3, o.c, a); for (let i = 0; i < 3; i++){ const ang = -PI / 2 + (i - 1) * .7; c.line(c.cx + 1 + K(ang) * 12, by + 6 + S(ang) * 12, c.cx + 1 + K(ang) * 18, by + 6 + S(ang) * 18, o.c, a, 2, 1); }
      for (let i = 0; i < 3; i++){ const t = Math.max(0, q * 1.5 - i * .2); if (t <= 1) c.ring(c.cx, c.cy - 8, 8 + t * 30, 6 + t * 22, 20, o.c, 1 - t, 0, 2); } },
    dash(c, q, o){ const e = ease(q * 2.2); for (let i = 1; i < 5; i++){ const x = c.cx - 20 - 90 * (1 - e) - i * 16; c.R(x - 5, c.cy - 22, 11, 34, o.c, (.3 / i) * c.fade(q)); c.R(x - 3, c.cy - 28, 7, 7, o.c, (.3 / i) * c.fade(q)); }
      if (o.v !== 1 && q > .4){ const k = (q - .4) / .6; c.R(c.cx - 26, c.cy - 8, 52, 2, '#fff', 1 - k); c.R(c.cx - 22, c.cy - 4, 44, 1, o.c, 1 - k); } },
    wind(c, q, o){ const N = o.n || 1; for (let i = 0; i < N; i++){ const qq = (q - i * .1) / .45; if (qq < 0) continue; const yy = c.cy - 8 + (i - (N - 1) / 2) * 12;
      if (qq < 1){ const x = c.cx - 110 + 110 * qq; for (let k = 0; k < 14; k++){ const a = -1.2 + k * .18; c.R(x + K(a) * 14 - 8, yy + S(a) * 16, 3, 2, k % 3 ? o.c : '#fff', .9); c.R(x + K(a) * 10 - 14, yy + S(a) * 12, 2, 2, o.c, .4); } }
      else { const e = Math.min(1, (qq - 1) * 2); c.line(c.cx - 16, yy - 10, c.cx + 16, yy + 10, '#fff', 1 - e, 2, 1); for (let k = 0; k < 6; k++) c.R(c.cx + (c.rn(k + i) - .5) * 30 + e * 12, yy + (c.rn(k + 7) - .5) * 24, 3, 1, o.c, 1 - e); } } },
    lance(c, q, o){ const Z = o.s || 1, e = q < .35 ? ease(q / .35) : q < .6 ? 1 : 1 - ease((q - .6) / .4), tip = c.cx - 70 + e * (o.v === 1 ? 100 : 76), yy = c.cy - 8, a = c.fade(Math.max(0, q - .5) * 2); c.R(tip - 80 * Z, yy - 1, 72 * Z, 3, '#8a6a4a', a); c.R(tip - 9 * Z, yy - 3 * Z, 9 * Z, 7 * Z, '#dfe6f0', a); c.R(tip, yy - 1, 3 * Z, 3, '#fff', a); c.R(tip - 11 * Z, yy - 4 * Z, 2, 9 * Z, o.c, a);
      if (q > .3 && q < .75){ const k = (q - .3) / .45; for (let i = 0; i < 8; i++){ const an = i * PI / 4; c.R(c.cx + 6 + K(an) * k * 18 * Z, yy + S(an) * k * 14 * Z, 3, 3, i % 2 ? o.c : '#fff', 1 - k); } c.shock(4 + k * 18 * Z, o.c, 1 - k, c.cx + 4, yy + 8); } },
    firewall(c, q, o){ const e = ease(q * 3); for (let i = 0; i < 6; i++){ const bx = c.cx - 30 + i * 12, H = (26 + c.rn(i) * 22) * e * (o.s || 1); for (let k = 0; k < 7; k++){ const t = (q * 1.6 + c.rn(i * 7 + k)) % 1; c.R(bx + S(t * 9 + k) * 3, c.y - 2 - t * H, 4 - (t > .6) , 4, FI3[(k + i) % 3], c.fade(q) * (1 - t * .5)); } c.R(bx - 3, c.y - 4, 10, 4, '#ff5a2a', c.fade(q) * .7); } },
    kiball(c, q, o){ const Z = o.s || 1, t = Math.min(1, q / .45); if (q < .45){ const x = c.cx - 110 + 110 * t, yy = c.cy - 8, r = 7 * Z + S(q * 40) * 1; for (let k = 1; k < 6; k++){ c.g.globalAlpha = .35 - k * .06; c.g.fillStyle = o.c; c.g.beginPath(); c.g.arc(x - k * 7, yy, r - k * .8, 0, 7); c.g.fill(); }
        c.g.globalAlpha = .45; c.g.fillStyle = o.c; c.g.beginPath(); c.g.arc(x, yy, r + 4, 0, 7); c.g.fill(); c.g.globalAlpha = 1; c.g.fillStyle = o.c2 || '#fff'; c.g.beginPath(); c.g.arc(x, yy, r - 2, 0, 7); c.g.fill(); }
      else { const e = (q - .45) / .55; c.ring(c.cx, c.cy - 8, 6 + e * 30 * Z, 6 + e * 26 * Z, 24, o.c, 1 - e, 0, 3); c.ring(c.cx, c.cy - 8, 3 + e * 18 * Z, 3 + e * 16 * Z, 16, '#fff', 1 - e, 0, 2); } },
    bigspear(c, q, o){ const e = ease(q * 1.6), ty = c.y - 140 + e * 132, a = c.fade(q); c.R(c.cx - 2, ty - 110, 5, 96, '#8a6a4a', a); c.R(c.cx - 5, ty - 18, 11, 4, '#ffd866', a); c.R(c.cx - 4, ty - 14, 9, 12, '#e8f4ff', a); c.R(c.cx - 2, ty - 2, 5, 6, '#e8f4ff', a); c.R(c.cx, ty + 4, 1, 3, '#fff', a); c.R(c.cx - 1, ty - 14, 1, 14, '#fff', a);
      for (let i = 0; i < 6; i++) c.R(c.cx - 1 + (i % 2 ? -4 : 4), ty - 90 - i * 6, 2, 10, o.c, a * .5); }
  });
  // ---------- 스킬 표 ----------
  const add = (key, layers, o = {}) => { T[key] = { layers, d: o.d || (o.g ? 2300 : 1000), g: !!o.g, once: !!o.once }; };
  const J = (job, items) => Object.entries(items).forEach(([n, v]) => add(job + '.' + n, v[0], v[1]));
  const W = '#fff', FI = ['#ff5a2a', '#ff9a3a', '#ffd04a'], MP = '#4a8aff', HL = '#bfffe0', G = { g: 1, d: 2400 }, GO = { g: 1, d: 2400, once: 1 };
  const flash = (t0, c, a = .55) => ['flash', { t0, t1: t0 + .15, c, a }];
  // 성기사
  const Y = '#ffe27a', Y2 = '#fff6c0';
  J('paladin', {
    '신성 일격': [[['crossf', { c: Y, s: .9 }], ['burst', { c: Y, c2: W, n: 10, t0: .2 }], ['starburst', { c: Y2, n: 6, s: .6, t0: .15 }]]],
    '빛의 철퇴': [[['giant', { k: 'hammer', s: .7, t1: .7 }], ['ground', { c: Y, c2: W, s: .7, t0: .35 }], ['burst', { c: Y2, t0: .4, n: 10 }]]],
    '정화의 불꽃': [[['flame', { c: ['#fff6c0', '#ffe27a', '#ffb040'], n: 22 }], ['crossf', { c: Y2, s: .6, t0: .1 }], ['sparkle', { c: Y, n: 6, t0: .3 }]]],
    '심판': [[['beams', { c: Y2, n: 3 }], ['crossf', { c: Y, s: .8, t0: .25 }], ['burst', { c: Y, t0: .4, n: 8 }]]],
    '신성 폭발': [[['dim', { a: .45 }], ['godray', { c: Y2 }], ['column', { c: Y, t0: .05, t1: .7 }], ['bigring', { c: Y, t0: .3, s: 1.1 }], ['burst', { c: Y, c2: W, n: 24, s: 2.2, t0: .35 }], flash(.3, '#fffbe0', .6)], GO],
    '수호의 빛': [[['shield', { c: Y }], ['ring', { c: Y2, t0: .2 }]]],
    '신성 방패': [[['dome', { c: Y, c2: W, s: 1.1 }], ['shield', { c: Y2, s: 1.2, t0: .1 }], ['sparkle', { c: W, n: 8, t0: .3 }]]],
    '헌신': [[['taunt', { c: Y }], ['wings', { c: Y2, s: .8, t0: .1 }], ['aura', { c: Y, n: 4, t0: .2 }]]],
    '치유의 손': [[['hand', { c: '#7affb0', c2: W }], ['heal', { c: HL, t0: .2 }]]],
    '축복의 빛': [[['pillar', { c: Y2, w: 8, h: 70 }], ['heal', { c: HL, n: 8, t0: .2 }], ['sparkle', { c: Y, n: 6, t0: .3 }]]],
    '되살리는 기도': [[['revive', { c: Y, w: 14 }], ['crossf', { c: W, s: .9, t0: .3 }], ['feathers', { c: Y2, t0: .3 }]]],
    '성역': [[['dim', { a: .4 }], ['rune', { c: Y, c2: W, s: 2.4 }], ['dome', { c: Y, c2: W, s: 2, t0: .2 }], ['crossf', { c: Y2, s: 1.6, t0: .3 }], ['sparkle', { c: W, n: 22, t0: .2 }], ['bigring', { c: Y, t0: .35, s: 1 }]], GO],
  });
  // 수호자
  const B = '#7ab8ff', B2 = '#cfe6ff', RE = '#ff5a4a';
  J('guardian', {
    '도발 외침': [[['taunt', { c: RE }], ['shout', { c: B, c2: RE, t0: .1 }]]],
    '시선 끌기': [[['taunt', { c: RE }], ['ring', { c: RE, t0: .1 }], ['down', { c: B, n: 4, t0: .3 }]]],
    '위협': [[['shout', { c: RE, c2: B }], ['down', { c: '#ff7a6a', n: 5, t0: .25 }]]],
    '집결': [[['shield', { c: B }], ['aura', { c: B2, n: 4, t0: .2 }], ['ring', { c: B, t0: .2 }]]],
    '방패벽': [[['shield', { c: B, s: 1.4 }], ['shards', { c: B, c2: B2, s: 1.3, t0: .1 }]]],
    '막기 태세': [[['ground', { c: B, c2: B2, s: .4 }], ['shield', { c: B2, s: 1.1, t0: .1 }]]],
    '방패 밀치기': [[['shield', { c: B, v: 1, t1: .6 }], ['burst', { c: W, c2: B, t0: .3, n: 8 }], ['stars', { c: '#ffe07a', t0: .35 }]]],
    '반사 방패': [[['shield', { c: B2, s: 1.2 }], ['starburst', { c: B, n: 8, t0: .3 }], ['burst', { c: W, c2: B, t0: .35, n: 10 }]]],
    '창 찌르기': [[['lance', { c: B }]]],
    '꿰뚫기': [[['lance', { c: B, v: 1, s: 1.3 }], ['laser', { c: B2, c2: B, w: 1, t0: .3, t1: .7 }]]],
    '창 휘두르기': [[['arc', { c: B, v: 1, s: 1.4 }], ['lance', { c: B2, t1: .5 }]]],
    '돌진 찌르기': [[['dash', { c: B, v: 1, t1: .5 }], ['lance', { c: B, v: 1, s: 1.4, t0: .2 }], ['starburst', { c: W, n: 8, s: 1, t0: .45 }]]],
    '수호자의 창': [[['dim', { a: .45 }], ['bigspear', { c: B, t1: .6 }], ['pillar', { c: B, c2: W, w: 20, h: 150, t0: .38 }], ['ground', { c: B, c2: W, s: 1.2, t0: .38 }], ['bigring', { c: B, t0: .4, s: 1 }], flash(.38, '#e8f6ff', .6)], G],
  });
  // 암흑기사
  const P = '#b04aff', BL = '#ff3a5a', PD = '#3a1060';
  J('darkknight', {
    '생명 흡수': [[['drain', { c: BL, c2: P }], ['burst', { c: P, n: 8 }]]],
    '흡혈 일격': [[['cross', { c: BL, n: 2, w: 3 }], ['drain', { c: BL, c2: '#ff8aa0', t0: .25, n: 12 }]]],
    '영혼 착취': [[['skulls', { n: 3 }], ['drain', { c: P, c2: '#d09aff', t0: .2 }]]],
    '피의 축제': [[['dim', { a: .5, c: '#200008' }], ['rune', { c: BL, c2: P, s: 2.4 }], ['cross', { c: BL, n: 4, s: 2, w: 4, t0: .2 }], ['drain', { c: BL, c2: '#ff8aa0', n: 30, t0: .3 }], ['bigring', { c: BL, t0: .35, s: 1.1 }], flash(.3, BL, .35)], GO],
    '암흑 파동': [[['ground', { c: P, c2: PD, s: .8 }], ['cloud', { c: PD, c2: P }]]],
    '저주': [[['rune', { c: P, c2: PD }], ['down', { c: P, t0: .2 }], ['skulls', { n: 2, t0: .2 }]]],
    '공포': [[['skulls', { n: 4 }], ['down', { c: '#8a3ac0', t0: .2 }]]],
    '그림자 속박': [[['chains', { c: P, c2: PD }], ['stars', { c: '#d09aff', t0: .4 }]]],
    '어둠의 군주': [[['dim', { a: .55, c: '#0a0018' }], ['pillar', { c: PD, c2: P, w: 24, h: 150 }], ['skulls', { n: 6, t0: .15 }], ['bigring', { c: P, t0: .35, s: 1.2 }], ['burst', { c: P, c2: '#d09aff', n: 22, s: 2, t0: .4 }], flash(.35, '#8a3ac0', .4)], GO],
    '피의 각성': [[['aura', { c: BL, c2: P, n: 5 }], ['flame', { c: [PD, BL, '#ff8aa0'], h: 36 }]]],
    '고통 인내': [[['cloud', { c: PD, c2: P }], ['shield', { c: P, t0: .1 }]]],
    '최후의 저항': [[['aura', { c: BL, n: 6 }], ['flame', { c: ['#200008', BL, '#ffd0d8'], h: 56, n: 24 }], ['ring', { c: BL, t0: .2, s: 1.2 }]]],
  });
  // 무희
  const PK = '#ff8ac8';
  J('dancer', {
    '마나의 춤': [[['ribbon', { c: PK, c2: '#fff0f8' }], ['mp', { c: MP, t0: .15 }]]],
    '물결 춤': [[['ribbon', { c: '#6ac8ff', c2: PK }], ['bubbles', { c: MP, n: 6 }], ['mp', { c: '#6ac8ff', t0: .2 }]]],
    '회복의 춤': [[['ribbon', { c: '#7affb0', c2: PK }], ['heal', { c: HL, t0: .2 }]]],
    '생명의 춤': [[['dim', { a: .35 }], ['ribbon', { c: PK, c2: '#7affb0', s: 1.6 }], ['bloom', { c: PK, c2: '#fff6c0', s: 2, t0: .2 }], ['rain', { c: '#ffc0e0', n: 26, t0: .2 }], ['heal', { c: HL, n: 14, t0: .3 }], ['bigring', { c: PK, t0: .35 }]], GO],
    '빠른 스텝': [[['haste', { c: PK }], ['notes', { c: PK, t0: .1 }]]],
    '열정의 춤': [[['ribbon', { c: '#ff6a4a', c2: PK }], ['aura', { c: '#ff6a4a', c2: PK, t0: .2 }], ['notes', { c: '#ff6a4a', t0: .1 }]]],
    '전장의 무희': [[['haste', { c: '#ffe07a' }], ['ribbon', { c: '#ffe07a', c2: PK, t0: .1 }]]],
    '불꽃 춤': [[['ribbon', { c: '#ff9a3a', c2: '#ffd04a' }], ['flame', { c: FI, h: 34 }], ['aura', { c: '#ff9a3a', t0: .2 }]]],
    '부채 날리기': [[['fan', { c: PK }], ['burst', { c: PK, t0: .45, n: 8 }]]],
    '회오리 부채': [[['fan', { c: PK, n: 2 }], ['swirl', { c: PK, t0: .35 }]]],
    '홀리는 춤': [[['notes', { c: PK }], ['clock', { c: PK, t0: .2 }], ['down', { c: '#c07aff', t0: .3 }]]],
    '매혹': [[['hearts', { c: PK }], ['down', { c: PK, t0: .3 }]]],
    '부채 폭풍': [[['dim', { a: .4 }], ['fan', { c: PK, n: 4, t1: .6 }], ['swirl', { c: PK, s: 2, t0: .3 }], ['blades', { c: PK, n: 10, t0: .3 }], ['hearts', { c: '#ffc0e0', n: 6, t0: .4 }], ['bigring', { c: PK, t0: .4 }]], G],
  });
  // 현자
  const CY = '#7ae6ff';
  J('sage', {
    '마나 나눔': [[['mp', { c: MP }], ['sparkle', { c: CY, n: 6 }]]],
    '마나의 샘': [[['fountain', { c: MP, c2: CY }], ['mp', { c: '#6ac8ff', t0: .2 }]]],
    '지혜의 룬': [[['rune', { c: CY, c2: W }], ['aura', { c: CY, t0: .2 }]]],
    '마력 폭류': [[['dim', { a: .4, c: '#04102a' }], ['column', { c: MP }], ['mp', { c: CY, t0: .1 }], ['fountain', { c: MP, c2: CY, n: 24, t0: .2 }], ['sparkle', { c: CY, n: 20 }], ['bigring', { c: MP, t0: .35 }]], GO],
    '보호 룬': [[['rune', { c: '#9ad0ff' }], ['shield', { c: CY, t0: .2 }]]],
    '신속 룬': [[['rune', { c: '#ffe07a' }], ['haste', { c: CY, t0: .15 }]]],
    '둔화 룬': [[['rune', { c: '#9a7aff' }], ['clock', { c: CY, t0: .15 }], ['down', { c: '#9a7aff', t0: .3 }]]],
    '약화 룬': [[['rune', { c: '#ff7a9a' }], ['down', { c: '#ff7a9a', t0: .2 }]]],
    '대현자의 룬': [[['dim', { a: .4 }], ['rune', { c: CY, c2: W, s: 2.6 }], ['rune', { c: '#ffe07a', s: 1.6, t0: .15 }], ['aura', { c: CY, n: 6, t0: .3 }], ['sparkle', { c: W, n: 22 }], ['bigring', { c: CY, t0: .35 }]], GO],
    '비전 화살': [[['orb', { c: CY, c2: '#9ad8ff', s: .8 }], ['rune', { c: CY, s: .7, t0: .45 }]]],
    '비전 폭발': [[['rune', { c: CY, s: .9 }], ['bloom', { c: CY, c2: W, t0: .15 }], ['burst', { c: CY, n: 14, s: 1.2, t0: .2 }]]],
    '마력 구체': [[['orb', { c: '#c07aff', c2: CY, s: 1.4 }], ['ring', { c: '#c07aff', t0: .45, s: 1.2 }], ['mp', { c: CY, t0: .5 }]]],
    '별의 비': [[['meteors', { c: '#ffe07a', c2: CY, n: 3, s: .6 }], ['sparkle', { c: CY, t0: .3 }]]],
    '진리의 빛': [[['dim', { a: .5 }], ['laser', { c: CY, c2: '#9ad8ff', w: 6 }], ['starburst', { c: W, n: 12, s: 1.6, t0: .3 }], ['bigring', { c: CY, t0: .35 }], flash(.25, '#e0faff', .6)], G],
  });
  // 주술사
  const GN = '#7aef6a', LT = '#fff6a0';
  J('shaman', {
    '치유 토템': [[['totem', { c: GN, c2: '#3aa84a' }], ['heal', { c: HL, t0: .3 }]]],
    '마나 토템': [[['totem', { c: MP, c2: '#3a6ac8' }], ['mp', { c: MP, t0: .3 }]]],
    '수호 토템': [[['totem', { c: '#ffd866', c2: '#c89a3a' }], ['shield', { c: '#ffd866', t0: .3 }]]],
    '바람 토템': [[['totem', { c: '#bfefff', c2: '#6ac8c8' }], ['haste', { c: '#bfefff', t0: .3 }]]],
    '정령의 비': [[['rain', { c: '#9fe8ff', n: 18 }], ['heal', { c: GN, t0: .25 }]]],
    '물의 정령': [[['wave', { c: '#6ac8ff', c2: W, s: .6 }], ['heal', { c: HL, t0: .3 }]]],
    '조상의 영혼': [[['smoke', { c: '#d0f0d8', c2: GN }], ['revive', { c: GN, w: 12, t0: .1 }], ['skulls', { n: 2, t0: .3 }]]],
    '정화의 연기': [[['smoke', { c: '#d0f0d8', c2: '#9aa8a0' }], ['cleanse', { c: GN, t0: .2 }]]],
    '생명의 고리': [[['dim', { a: .35 }], ['ring', { c: GN, s: 1.4 }], ['regen', { c: GN }], ['bloom', { c: GN, c2: '#e0ffb0', s: 1.6, t0: .2 }], ['heal', { c: HL, n: 14, t0: .3 }], ['bigring', { c: GN, t0: .35, s: .9 }]], G],
    '번개 토템': [[['totem', { c: LT, c2: '#8a7a3a' }], ['bolt', { c: LT, t0: .3, t1: .9 }]]],
    '천둥': [[['bolt', { c: LT }], ['ground', { c: LT, s: .6, t0: .3 }]]],
    '연쇄 낙뢰': [[['chain', { c: LT, c2: '#9ad8ff' }], ['bolt', { c: '#cfe8ff', t0: .1 }]]],
    '폭풍 부름': [[['cloud', { c: '#5a6a80', c2: '#8a9ab0' }], ['rain', { c: '#9fd0ff', n: 16 }], ['down', { c: '#9fd0ff', t0: .3 }]]],
  });
  // 무녀
  const RD = '#ff6a6a';
  J('miko', {
    '부정 씻기': [[['ofuda', { c: RD, n: 1, t1: .6 }], ['cleanse', { c: '#ffe8e8', t0: .3 }], ['feathers', { c: RD, n: 8, t0: .3 }]]],
    '액막이': [[['ofuda', { c: RD, n: 2 }], ['shield', { c: '#ffe8e8', t0: .3 }]]],
    '신성한 물': [[['fountain', { c: '#9fe8ff', c2: W }], ['heal', { c: HL, t0: .2 }]]],
    '청정 결계': [[['rune', { c: RD, c2: W }], ['heal', { c: HL, t0: .2 }], ['sparkle', { c: W, n: 6, t0: .2 }]]],
    '결계': [[['kekkai', { c: RD }]]],
    '봉인 부적': [[['ofuda', { c: RD, n: 3 }], ['chains', { c: RD, c2: '#ffe8e8', t0: .3 }]]],
    '부적 화살': [[['ofuda', { c: RD, n: 1 }], ['burst', { c: RD, c2: W, t0: .4 }]]],
    '경계 부적': [[['ofuda', { c: '#ffd866', n: 2 }], ['down', { c: RD, t0: .3 }]]],
    '혼 부르기': [[['bell', { c: '#ffd866', c2: W }], ['revive', { c: RD, w: 12, t0: .1 }]]],
    '방울 소리': [[['bell', { c: '#ffd866' }], ['heal', { c: HL, t0: .3 }]]],
    '신령의 춤': [[['foxfire', { c: RD, c2: W, n: 3 }], ['aura', { c: RD, t0: .2 }]]],
    '여우불': [[['foxfire', { c: '#6ac8ff', c2: '#c8f0ff' }], ['burst', { c: '#6ac8ff', t0: .65, n: 10 }]]],
    '천상의 방울': [[['dim', { a: .4 }], ['godray', { c: '#ffe8e8' }], ['bell', { c: '#ffd866', c2: W }], ['foxfire', { c: '#ffb0c0', c2: W, n: 6 }], ['heal', { c: HL, n: 14, t0: .3 }], ['bigring', { c: RD, t0: .3 }]], GO],
  });
  // 궁수
  const AR = '#c8e86a';
  J('archer', {
    '조준 사격': [[['arrow', { c: AR }]]],
    '연발': [[['arrow', { c: AR, n: 3 }], ['burst', { c: AR, t0: .6, n: 8 }]]],
    '꿰뚫는 화살': [[['arrow', { c: AR, s: 1.5 }], ['thrust', { c: AR, c2: W, t0: .3 }], ['starburst', { c: W, n: 8, t0: .4 }]]],
    '화살비': [[['arrows', { c: AR, n: 10 }]]],
    '일격필살': [[['dim', { a: .5 }], ['scope', { c: '#ff4a4a', t1: .45 }], ['arrow', { c: AR, s: 2, t0: .4, t1: .85 }], ['bigring', { c: AR, t0: .55 }], flash(.55, '#fff', .55), ['starburst', { c: W, n: 12, s: 1.8, t0: .55 }]], G],
    '불화살': [[['arrow', { c: '#ff7a2a', k: 'fire' }], ['flame', { c: FI, t0: .35, n: 14 }]]],
    '얼음 화살': [[['arrow', { c: '#9fe8ff', k: 'ice' }], ['shards', { c: '#9fe8ff', t0: .35 }], ['snow', { c: '#bfefff', t0: .35 }]]],
    '번개 화살': [[['arrow', { c: LT, k: 'bolt' }], ['chain', { c: LT, t0: .35 }]]],
    '폭발 화살': [[['arrow', { c: '#ff9a3a', k: 'fire' }], ['bloom', { c: '#ff9a3a', c2: '#ffd04a', t0: .35 }], ['burst', { c: '#ff5a2a', t0: .4 }]]],
    '원소 폭풍': [[['dim', { a: .45 }], ['arrows', { c: '#ff7a2a', n: 8 }], ['arrows', { c: '#9fe8ff', n: 8, t0: .1 }], ['arrows', { c: LT, n: 8, t0: .2 }], ['bloom', { c: '#ff9a3a', s: 1.6, t0: .5 }], ['bigring', { c: AR, t0: .5 }]], GO],
    '그물 화살': [[['arrow', { c: AR }], ['net', { c: '#c8a878', t0: .3 }]]],
    '약점 표시': [[['scope', { c: '#ff4a4a', v: 1 }], ['down', { c: '#ff7a6a', t0: .3 }]]],
    '사냥꾼의 집중': [[['scope', { c: AR, v: 1 }], ['aura', { c: AR, t0: .2 }]]],
  });
  // 총잡이
  const GU = '#ffb040';
  J('gunner', {
    '연사': [[['bullet', { c: GU, n: 4 }]]],
    '쌍권총': [[['bullet', { c: GU, n: 7, gap: .07 }], ['starburst', { c: '#ffe07a', t0: .7, n: 6, s: .6 }]]],
    '난사': [[['bullet', { c: GU, n: 6, gap: .08, v: 1 }], ['crack', { c: GU, t0: .5 }]]],
    '탄막': [[['bullet', { c: '#ffe07a', n: 9, gap: .06, v: 1 }], ['smoke', { c: '#9a9aa8', t0: .4 }]]],
    '마지막 한 발': [[['dim', { a: .5 }], ['scope', { c: '#ff4a4a', t1: .5 }], ['bullet', { c: W, n: 1, s: 3, t0: .48, t1: .8 }], ['bigring', { c: GU, t0: .55 }], flash(.55, '#fff', .6), ['burst', { c: GU, n: 22, s: 2, t0: .55 }]], G],
    '산탄': [[['bullet', { c: GU, n: 1, v: 2, t1: .6 }], ['burst', { c: GU, t0: .12, n: 8 }]]],
    '섬광탄': [[['starburst', { c: W, n: 12, s: 1.2 }], flash(.1, '#fff', .5), ['stars', { c: '#ffe07a', t0: .3 }]]],
    '냉각탄': [[['bullet', { c: '#9fe8ff', n: 1 }], ['shards', { c: '#9fe8ff', t0: .2 }], ['down', { c: '#9fe8ff', t0: .3 }]]],
    '철갑탄': [[['bullet', { c: '#cfd6e0', n: 1, s: 2 }], ['thrust', { c: '#cfd6e0', c2: W, t0: .15 }], ['starburst', { c: GU, t0: .25, n: 8 }]]],
    '폭발탄': [[['bullet', { c: GU, n: 1 }], ['bloom', { c: '#ff9a3a', c2: '#ffd04a', t0: .15 }], ['burst', { c: '#ff5a2a', t0: .2, n: 14 }], ['smoke', { c: '#7a7a88', t0: .35 }]]],
    '저격': [[['scope', { c: '#ff4a4a' }], ['starburst', { c: W, n: 8, t0: .6 }]]],
    '숨 고르기 사격': [[['haste', { c: GU }], ['ring', { c: GU }]]],
    '급소 사격': [[['scope', { c: '#ff4a4a', t1: .7 }], ['burst', { c: '#ff4a4a', t0: .45, n: 8 }]]],
  });
  // 정령술사
  const WA = '#6ac8ff', WI = '#bfffe8';
  J('elemental', {
    '불덩이': [[['orb', { c: '#ff7a2a', c2: '#ffd04a', s: 1.2 }], ['bloom', { c: '#ff7a2a', c2: '#ffd04a', t0: .45, s: .7 }], ['flame', { c: FI, t0: .5, n: 10 }]]],
    '불꽃 폭발': [[['bloom', { c: '#ff7a2a', c2: '#ffd04a' }], ['burst', { c: '#ff5a2a', n: 14, t0: .1 }]]],
    '불의 벽': [[['firewall', {}]]],
    '화염 폭풍': [[['swirl', { c: '#ff7a2a' }], ['flame', { c: FI, t0: .1 }]]],
    '태양 화염': [[['dim', { a: .5, c: '#200800' }], ['meteors', { c: '#ff9a3a', c2: '#ff5a2a', n: 1, s: 2.4, t1: .7 }], ['bloom', { c: '#ff7a2a', c2: '#ffe07a', s: 2.6, t0: .3 }], ['flame', { c: FI, h: 70, n: 30, s: 2, t0: .32 }], ['bigring', { c: '#ff9a3a', t0: .32, s: 1.2 }], flash(.3, '#ffd8a0', .6)], GO],
    '물결': [[['wave', { c: WA, c2: '#cfeeff' }]]],
    '얼음 감옥': [[['shards', { c: '#9fe8ff', s: 1.4 }], ['dome', { c: '#9fe8ff', c2: W, s: .9, t0: .2 }]]],
    '치유의 물': [[['fountain', { c: WA, c2: W }], ['bubbles', { c: WA, t0: .2 }], ['heal', { c: HL, t0: .3 }]]],
    '해일': [[['wave', { c: '#3a8aff', c2: '#cfeeff', s: 1.6 }], ['bubbles', { c: '#9fe8ff', t0: .4 }]]],
    '서리': [[['snow', { c: '#bfefff' }], ['down', { c: '#9fe8ff', t0: .3 }]]],
    '바람 칼날': [[['wind', { c: WI }]]],
    '돌풍': [[['wind', { c: '#e8f8ff', n: 3 }], ['down', { c: WI, t0: .3 }]]],
    '회오리': [[['swirl', { c: WI }]]],
    '순풍': [[['haste', { c: WI }], ['feathers', { c: WI }]]],
    '폭풍의 눈': [[['dim', { a: .45, c: '#041814' }], ['swirl', { c: WI, s: 2.6 }], ['wind', { c: W, n: 4, t0: .1 }], ['blades', { c: WI, n: 12, t0: .3 }], ['bigring', { c: WI, t0: .4 }]], GO],
  });
  // 격투가
  const FT = '#ff7a3a', KI = '#7ae6ff';
  J('fighter', {
    '연속 주먹': [[['fist', { c: FT, n: 4 }]]],
    '정권': [[['fist', { c: FT, n: 1, s: 1.6, t1: .7 }], ['starburst', { c: '#ffe07a', n: 10, t0: .2 }], ['ground', { c: FT, s: .6, t0: .25 }]]],
    '올려치기': [[['fist', { c: FT, n: 1, v: 1, s: 1.2 }], ['fountain', { c: '#ffe07a', t0: .2 }]]],
    '백열권': [[['fist', { c: '#ffd04a', n: 6 }], ['flame', { c: FI, t0: .2, h: 30 }]]],
    '필살 연타': [[['dim', { a: .5 }], ['fist', { c: FT, n: 10, t1: .75 }], ['burst', { c: '#ffe07a', n: 20, s: 2, t0: .6 }], ['bigring', { c: FT, t0: .6 }], flash(.6, '#ffe8d0', .5)], G],
    '기공파': [[['kiball', { c: KI, c2: '#e8fcff' }]]],
    '기 모으기': [[['mp', { c: KI }], ['aura', { c: KI, n: 5, t0: .2 }]]],
    '기공 장벽': [[['dome', { c: KI, c2: W }], ['aura', { c: KI, n: 3, t0: .1 }], ['mp', { c: KI, t0: .1 }]]],
    '대기공포': [[['dim', { a: .45 }], ['laser', { c: KI, c2: '#c8f8ff', w: 10 }], ['bloom', { c: KI, s: 2, t0: .3 }], ['bigring', { c: KI, t0: .35 }], flash(.3, '#e0faff', .5)], GO],
    '회축': [[['spin', { c: FT, c2: '#ffe07a', s: 1.2 }], ['ground', { c: FT, s: .5, t0: .3 }]]],
    '발차기': [[['arc', { c: '#ffe07a', v: 2, s: .8 }], ['fist', { c: FT, c2: '#8a5a3a', n: 1, t0: .1 }]]],
    '투지': [[['aura', { c: FT }], ['flame', { c: FI, h: 30, n: 12 }], ['shout', { c: FT, t0: .1 }]]],
  });
  // 검무사
  const BD = '#e8e4ff', SH = '#6a5aa0';
  J('bladedancer', {
    '검무': [[['blades', { c: BD, n: 6 }]]],
    '쌍검 베기': [[['cross', { c: BD, n: 2, w: 3 }], ['burst', { c: W, t0: .3, n: 6 }]]],
    '회전 칼날': [[['spin', { c: BD, c2: '#9a8aff', s: 1.1 }], ['blades', { c: '#9a8aff', n: 4, t0: .2 }]]],
    '검의 비': [[['arrows', { c: '#9a8aff', n: 9, k: 'sword' }], ['shards', { c: BD, c2: '#9a8aff', t0: .5 }]]],
    '천검무': [[['dim', { a: .5 }], ['arrows', { c: '#9a8aff', n: 16, k: 'sword' }], ['blades', { c: BD, n: 12, t0: .3 }], ['cross', { c: W, n: 5, s: 1.8, w: 3, t0: .5 }], ['bigring', { c: BD, t0: .55 }], flash(.55, '#f0eeff', .5)], GO],
    '그림자 돌진': [[['dash', { c: SH }], ['cross', { c: BD, n: 1, t0: .4 }]]],
    '기습': [[['smoke', { c: '#3a3050', c2: SH }], ['cross', { c: '#ff5a7a', n: 2, s: 1.3, w: 3, t0: .3 }], ['starburst', { c: W, t0: .4 }]]],
    '그림자 분신': [[['dash', { c: SH, v: 1 }], ['haste', { c: '#9a8aff', t0: .1 }]]],
    '암살': [[['dim', { a: .6, c: '#000' }], ['smoke', { c: '#1a1028', c2: '#3a3050' }], ['dash', { c: '#3a3050', v: 1, t0: .2, t1: .6 }], ['cross', { c: BL, n: 1, s: 2.4, w: 5, t0: .5 }], flash(.5, '#ffd0d8', .5), ['burst', { c: BL, n: 18, s: 1.8, t0: .55 }]], G],
    '검기 날리기': [[['wind', { c: BD }], ['burst', { c: BD, t0: .45 }]]],
    '칼바람': [[['wind', { c: BD, n: 3 }], ['clock', { c: '#9a8aff', t0: .3 }]]],
    '춤사위': [[['ribbon', { c: BD, c2: '#9a8aff' }], ['haste', { c: BD }], ['feathers', { c: '#9a8aff', n: 6 }]]],
    '일섬': [[['laser', { c: BD, c2: '#9a8aff', w: 2 }], ['cross', { c: W, n: 1, s: 3, w: 4, t0: .35 }], ['burst', { c: BD, t0: .4, n: 12 }]], { d: 1300 }],
  });
  Object.keys(T).forEach(k => { if (!X.SK[k]) X.SK[k] = { dur: T[k].d, grand: T[k].g, once: T[k].once, v2: 1 }; });
})();
