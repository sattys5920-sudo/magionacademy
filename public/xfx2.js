// 직업별 스킬 이펙트 2: 스킬마다 모양이 다르게 (소환사를 뺀 11개 직업). xfx.js 뒤에 불러와요.
// 이펙트 부품(motif)을 겹쳐서 만들어요: 층 = [부품, {c 색, c2 보조색, t0 시작, t1 끝, s 크기, n 개수, v 변형}]
(function(){
  const X = window.XFXJOB; if (!X) return;
  const S = Math.sin, K = Math.cos, PI = Math.PI;
  const ease = t => t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t);
  const LIB = {
    // ----- 공격 -----
    arc(c, q, o){ const r = (o.s || 1) * 24, n = 26, v = o.v || 0; for (let i = 0; i < n * ease(q * 1.6); i++){ const a = (v === 1 ? -2.4 : v === 2 ? 2.4 : -1.4) + i * (v ? (v === 1 ? .09 : -.09) : .11); c.R(c.cx + K(a - 1.57 * (v === 0)) * r, c.cy + S(a - 1.57 * (v === 0)) * r * .85 - 4, 4, 4, i > n * ease(q * 1.6) - 6 ? '#fff' : o.c, c.fade(q)); } },
    cross(c, q, o){ const N = o.n || 3; for (let i = 0; i < N; i++){ const t0 = i * .12, qq = Math.min(1, Math.max(0, (q - t0) / .22)); if (!qq) continue; const a = -.9 + c.rn(i + (o.seed || 0)) * 1.8 + (i % 2 ? 1.2 : -.3), dx = K(a) * 24 * (o.s || 1), dy = S(a) * 24 * (o.s || 1); c.line(c.cx - dx, c.cy - dy, c.cx + dx, c.cy + dy, i % 2 ? '#fff' : o.c, Math.max(0, 1 - (q - t0) * 1.5), o.w || 2, qq); } },
    thrust(c, q, o){ for (let i = -1; i <= 1; i++) c.line(c.cx - 58 * (o.s || 1), c.cy + i * 3 - 4, c.cx + 6, c.cy + i * 3 - 4, i ? o.c2 || o.c : '#fff', c.fade(q) * (i ? .5 : 1), i ? 2 : 3, Math.min(1, q * 3)); if (q > .3) for (let i = 0; i < 5; i++) c.plus(c.cx + 6 + (q - .3) * 22 * (c.rn(i) + .3), c.cy - 12 + c.rn(i + 4) * 16, '#fff', c.fade(q)); },
    chop(c, q, o){ const w = o.w || 4; c.line(c.cx - 22, c.y - 50, c.cx + 12, c.y - 6, o.c, c.fade(q), w, Math.min(1, q * 2.5)); c.line(c.cx - 20, c.y - 50, c.cx + 14, c.y - 6, '#fff0c0', c.fade(q), 2, Math.min(1, q * 2.5)); if (q > .4) for (let i = 0; i < 5; i++) c.R(c.cx - 12 + c.rn(i) * 24, c.y - 4 - S(Math.min(1, (q - .4) * 2) * PI) * (6 + c.rn(i + 5) * 14), 3, 3, i % 2 ? '#8a6a4a' : '#c0a070', c.fade(q)); },
    spin(c, q, o){ const R2 = (o.s || 1) * 22; for (let i = 0; i < 20; i++){ const a = q * 14 - i * .17; c.R(c.cx + K(a) * R2, c.cy + S(a) * R2 * .35 + 6, 4 - (i > 10), 3, i < 3 ? '#fff' : o.c, c.fade(q) * (1 - i / 20)); c.R(c.cx + K(a + PI) * R2 * .8, c.cy + S(a + PI) * R2 * .3 - 4, 3, 3, i < 3 ? '#fff' : o.c2 || o.c, c.fade(q) * (1 - i / 20)); } },
    burst(c, q, o){ const n = o.n || 12, r = (o.s || 1) * 26; for (let i = 0; i < n; i++){ const a = i * 2 * PI / n + (o.rot || 0); c.R(c.cx + K(a) * q * r - 1, c.cy + S(a) * q * r * .85 - 1, 4, 4, i % 2 ? o.c : o.c2 || '#fff', 1 - q); } },
    starburst(c, q, o){ const n = o.n || 8, L = (o.s || 1) * 30 * Math.min(1, q * 4); for (let i = 0; i < n; i++){ const a = i * 2 * PI / n + (o.rot || 0); c.line(c.cx, c.cy, c.cx + K(a) * L, c.cy + S(a) * L, i % 2 ? o.c2 || o.c : o.c, c.fade(q), i % 2 ? 2 : 3, 1); } c.R(c.cx - 4, c.cy - 4, 9, 9, '#fff', c.fade(q)); },
    ground(c, q, o){ const r = (o.s || 1) * 56; c.shock(6 + q * r, o.c, c.fade(q)); c.shock(3 + q * r * .6, o.c2 || '#fff', c.fade(q)); for (let i = 0; i < 8; i++) c.R(c.cx - 20 + c.rn(i) * 40, c.y - 4 - S(Math.min(1, q * 1.5) * PI) * (6 + c.rn(i + 4) * 22), 3, 3, i % 2 ? '#8a6a4a' : '#c0a070', c.fade(q)); },
    pillar(c, q, o){ const w = (o.w || 10), H = o.h || 110, a = (q < .15 ? q / .15 : 1) * c.fade(q); c.R(c.cx - w / 2, c.y - H, w, H - 2, o.c, a * .55); c.R(c.cx - w / 4, c.y - H, w / 2, H - 2, o.c2 || '#fff', a); c.ring(c.cx, c.y, w + q * 18, (w + q * 18) * .3, 16, o.c, a, 0); },
    beams(c, q, o){ const N = o.n || 5; for (let i = 0; i < N; i++){ const t0 = i * .09, qq = Math.min(1, Math.max(0, (q - t0) / .28)); if (!qq) continue; const bx = c.cx - 22 + i * (44 / Math.max(1, N - 1)); c.line(bx, c.y - 90, bx, c.y - 6, o.c, c.fade(q) * .6, 5, qq); c.line(bx, c.y - 90, bx, c.y - 6, '#fff', c.fade(q), 2, qq); if (qq >= 1) c.star(bx, c.y - 4, o.c2 || o.c, c.fade(q), 4); } },
    orb(c, q, o){ const t = Math.min(1, q / .45); if (q < .5){ const ox = c.cx - 70 + 70 * t, oy = c.cy - 8 + S(t * 3) * -10, r = (o.s || 1) * 5; c.R(ox - r, oy - r, r * 2 + 1, r * 2 + 1, o.c); c.R(ox - r / 2, oy - r / 2, r + 1, r + 1, '#fff'); for (let k = 1; k < 6; k++) c.R(ox - k * 6, oy + S(k) * 2, r * 2 - k, r * 2 - k, o.c2 || o.c, .8 - k * .13); } else { const e = (q - .5) * 2; c.shock(4 + e * 30 * (o.s || 1), o.c, 1 - e); c.star(c.cx, c.cy - 4, '#fff', 1 - e, 8 - e * 5); for (let i = 0; i < 8; i++) c.R(c.cx + K(i * .785) * e * 26, c.cy + S(i * .785) * e * 22, 3, 3, o.c, 1 - e); } },
    bolt(c, q, o){ const N = o.n || 1; for (let k = 0; k < N; k++){ if (q > .55 + k * .05) continue; let ax = c.cx + (k - (N - 1) / 2) * 16, ay = c.y - 92; const tx = ax, ty = c.cy; for (let i = 1; i <= 8; i++){ const nx = tx + (i < 8 ? (c.rn(i + k * 9 + (o.seed || 0)) - .5) * 16 : 0), ny = ay + (ty - c.y + 92) / 8; c.line(ax, ay, nx, ny, o.c, 1, 3, 1); c.line(ax, ay, nx, ny, '#fff', 1, 1, 1); ax = nx; ay = ny; } } if (q > .1) c.shock(4 + q * 26, o.c, c.fade(q)); },
    chain(c, q, o){ const fr = Math.floor(q * 14); for (let i = 0; i < 4; i++){ const a = i * PI / 2 + .6 + fr * .2, ex = c.cx + K(a) * 26, ey = c.cy + S(a) * 22; let ax = ex, ay = ey; for (let k = 1; k <= 5; k++){ const nx = ex + (c.cx - ex) * k / 5 + ((fr * 7 + i * 3 + k * 5) % 9 - 4), ny = ey + (c.cy - ey) * k / 5 + ((fr * 5 + i * 7 + k * 3) % 9 - 4); c.line(ax, ay, nx, ny, k % 2 ? o.c : o.c2 || '#fff', c.fade(q), 2, 1); ax = nx; ay = ny; } } c.star(c.cx, c.cy, '#fff', c.fade(q), 5); },
    flame(c, q, o){ const cols = o.c, H = (o.h || 44) * (o.s || 1); for (let k = 0; k < (o.n || 18); k++) c.R(c.cx + (c.rn(k) - .5) * 20 * (o.s || 1), c.y - 2 - ((q * 1.4 + c.rn(k + 40)) % 1) * H, 3 + (k % 3 === 0), 3, cols[k % cols.length], c.fade(q)); },
    shards(c, q, o){ for (let i = 0; i < 7; i++){ const h = (10 + c.rn(i) * 24 * (o.s || 1)) * ease(q * 2.5), bx = c.cx - 18 + i * 6; c.R(bx, c.y - h, 3, h, i % 2 ? o.c : o.c2 || '#fff', c.fade(q)); c.R(bx, c.y - h - 3, 1, 3, '#fff', c.fade(q)); } c.shock(4 + q * 26, o.c, c.fade(q) * .8); for (let i = 0; i < 6; i++) c.plus(c.cx - 16 + c.rn(i + 9) * 32, c.y - 10 - q * 24 * c.rn(i + 3), '#fff', c.fade(q)); },
    snow(c, q, o){ for (let i = 0; i < (o.n || 14); i++){ const t = (q * 1.2 + c.rn(i) * .5) % 1; c.plus(c.cx - 22 + c.rn(i + 3) * 44 + S(t * 8 + i) * 3, c.y - 70 + t * 66, i % 2 ? o.c : '#fff', c.fade(q)); } },
    meteors(c, q, o){ const N = o.n || 3; for (let i = 0; i < N; i++){ const t0 = i * .15, qq = (q - t0) / .38; if (qq < 0) continue; const tx = c.cx - 14 + i * 14; if (qq < 1){ const Z = o.s || 1, mx = tx + 70 * (1 - qq), my = c.y - 12 - 90 * (1 - qq); for (let k = 0; k < 9; k++) c.R(mx + k * 3.5 * Z, my - k * 4.5 * Z, (6 - k * .6) * Z, (6 - k * .6) * Z, k < 2 ? '#fff' : k < 4 ? o.c : o.c2 || '#6a2aa0', .9 - k * .1); c.R(mx - 3 * Z, my - 3 * Z, 8 * Z, 8 * Z, o.c2 || '#3a1a10'); c.R(mx - 2 * Z, my - 2 * Z, 6 * Z, 6 * Z, o.c); } else { const e = Math.min(1, (qq - 1) * 2.4); c.shock(4 + e * 24, o.c, 1 - e); c.star(tx, c.y - 8, '#fff', 1 - e, 6 - e * 4); } } },
    cloud(c, q, o){ for (let i = 0; i < 8; i++){ const t = (q * 1.1 + i / 8) % 1; c.g.globalAlpha = ((1 - t) * .45 + .05) * c.fade(q); c.g.fillStyle = i % 2 ? o.c : o.c2 || o.c; c.g.beginPath(); c.g.ellipse(c.cx + (c.rn(i) - .5) * 26 + S(q * 7 + i) * 4, c.y - 4 - t * 38, (6 + t * 9) * (o.s || 1), (4 + t * 6) * (o.s || 1), 0, 0, 7); c.g.fill(); } c.g.globalAlpha = 1; for (let i = 0; i < 5; i++) c.R(c.cx - 12 + i * 6, c.y - 20 - q * 14, 2, 2, '#fff', c.fade(q)); },
    bubbles(c, q, o){ for (let i = 0; i < (o.n || 12); i++){ const t = (q * 1.2 + c.rn(i) * .5) % 1, bx = c.cx - 14 + c.rn(i + 3) * 28 + S(t * 8 + i) * 3, by = c.y - t * 40 - 2, s = 4 + (i % 3) * 2; c.g.globalAlpha = (1 - t) * c.fade(q); c.g.strokeStyle = i % 2 ? o.c : o.c2 || o.c; c.g.lineWidth = 1; c.g.strokeRect(Math.round(bx) + .5, Math.round(by) + .5, s, s); c.g.globalAlpha = 1; c.R(bx + 1, by + 1, 1, 1, '#fff', (1 - t) * c.fade(q)); } },
    thorns(c, q, o){ for (let i = 0; i < 9; i++){ const a = i * PI / 4.5, L = (6 + 22 * Math.min(1, q * 3)) * (i % 2 ? .75 : 1) * (o.s || 1); c.line(c.cx + K(a) * 5, c.y - 4 + S(a) * 2, c.cx + K(a) * L, c.y - 4 + S(a) * L * .35 - L * .4, o.c, c.fade(q), 3, 1); c.R(c.cx + K(a) * L - 1, c.y - 4 + S(a) * L * .35 - L * .4 - 1, 3, 3, o.c2 || '#e0ffb0', c.fade(q)); } },
    blades(c, q, o){ const N = o.n || 8; for (let i = 0; i < N; i++){ const a = i * 2 * PI / N + q * 14, r = 34 * (1 - q * .7); const bx = c.cx + K(a) * r, by = c.cy + S(a) * r * .7; c.line(bx, by, bx + K(a + 1.57) * 7, by + S(a + 1.57) * 7, '#e8f8ff', c.fade(q), 2, 1); c.R(bx - 1, by - 1, 3, 3, o.c, c.fade(q)); } if (q > .72) c.star(c.cx, c.cy, '#fff', 1, 12 * (1 - (q - .72) * 3)); },
    hand(c, q, o){ for (let i = 0; i < 5; i++){ const e = ease(q * 2), bx = c.cx - 10 + i * 5, h = (14 + (i === 2 ? 8 : i % 2 ? 0 : 4)) * e; c.R(bx, c.y - h, 3, h, o.c, c.fade(q)); c.R(bx + (i < 2 ? 1 : i > 2 ? -1 : 0), c.y - h - 2, 2, 3, o.c2 || '#fff', c.fade(q)); } c.ring(c.cx, c.y, 6 + q * 22, 2 + q * 7, 16, o.c, c.fade(q), q * 3); },
    skulls(c, q, o){ for (let i = 0; i < (o.n || 4); i++){ const t = (q * 1.2 + i / (o.n || 4)) % 1, sx = c.cx - 18 + i * 12 + S(t * 6 + i) * 4, sy = c.y - 6 - t * 50; c.R(sx - 3, sy - 3, 7, 6, '#e8e0ff', c.fade(q)); c.R(sx - 2, sy + 3, 5, 3, '#e8e0ff', c.fade(q)); c.R(sx - 2, sy - 1, 2, 2, '#1a0a20', c.fade(q)); c.R(sx + 1, sy - 1, 2, 2, '#1a0a20', c.fade(q)); } },
    bell(c, q, o){ const by = c.cy - 26 + S(q * 30) * 1, a = Math.sin(q * PI); c.R(c.cx - 6, by, 13, 12, o.c, a); c.R(c.cx - 8, by + 12, 17, 3, o.c, a); c.R(c.cx - 1, by - 4, 3, 5, o.c2 || '#fff', a); c.R(c.cx - 1, by + 14, 3, 3, '#a07020', a); for (let i = 0; i < 3; i++) c.ring(c.cx, by + 8, 8 + Math.max(0, q - i * .12) * 34, 6 + Math.max(0, q - i * .12) * 26, 20, o.c, c.fade(q) * (1 - i * .25), 0, 2); },
    crossf(c, q, o){ const L = (o.s || 1) * 22, a = (q < .2 ? q * 5 : 1) * c.fade(q); c.R(c.cx - 2, c.cy - L, 5, L * 2, o.c, a); c.R(c.cx - L * .6, c.cy - 8, L * 1.2, 5, o.c, a); c.R(c.cx - 1, c.cy - L, 3, L * 2, '#fff', a); c.R(c.cx - L * .6, c.cy - 7, L * 1.2, 3, '#fff', a); },
    notes(c, q, o){ for (let i = 0; i < (o.n || 6); i++){ const a = i * 2 * PI / (o.n || 6) + .3, r = 8 + q * 28, nx = c.cx + K(a) * r, ny = c.cy + S(a) * r * .8 - q * 6; c.R(nx, ny, 3, 3, [o.c, '#ff9ac0', '#9ad8ff'][i % 3], c.fade(q)); c.R(nx + 2, ny - 5, 1, 5, '#fff', c.fade(q)); } },
    clock(c, q, o){ const r = (o.s || 1) * 16; c.ring(c.cx, c.cy, r, r, 24, o.c, Math.min(1, q * 5) * c.fade(q)); for (let i = 0; i < 12; i++){ const b = i * PI / 6; c.R(c.cx + K(b) * (r - 4) - 1, c.cy + S(b) * (r - 4) - 1, 2, 2, '#fff', c.fade(q)); } const h = q * 12 - PI / 2; c.line(c.cx, c.cy, c.cx + K(h) * r * .5, c.cy + S(h) * r * .5, '#fff', c.fade(q), 2); c.line(c.cx, c.cy, c.cx + K(h * 6) * r * .8, c.cy + S(h * 6) * r * .8, o.c, c.fade(q), 2); },
    swirl(c, q, o){ for (let k = 0; k < 3; k++) for (let i = 0; i < 24; i++){ const t = i / 24, a = t * 9 + q * 14 + k * 2.1, r = 4 + t * 16 * (o.s || 1); c.R(c.cx + K(a) * r, c.y - 4 - t * 44, 3, 2, k % 2 ? '#fff' : o.c, c.fade(q) * (.4 + t * .6)); } },
    fountain(c, q, o){ for (let i = 0; i < (o.n || 14); i++){ const t = (q * 1.2 + c.rn(i) * .4) % 1, a = -PI / 2 + (c.rn(i + 3) - .5) * 2.4; c.star(c.cx + K(a) * t * 32, c.y - t * 46 + 6 + Math.abs(S(a)) * 8, i % 2 ? o.c : o.c2 || '#fff', c.fade(q), 1 + (i % 2)); } },
    crack(c, q, o){ for (let i = 0; i < 7; i++){ const a = i * PI / 3.5 + .2, L = 40 * ease(q * 2); c.line(c.cx, c.y, c.cx + K(a) * L, c.y + S(a) * L * .28, o.c, c.fade(q), 2, 1); c.line(c.cx, c.y, c.cx + K(a) * L * .8, c.y + S(a) * L * .22, o.c2 || '#ffd866', c.fade(q), 1, 1); } },
    missiles(c, q, o){ for (let i = 0; i < (o.n || 4); i++){ const t0 = i * .13, qq = (q - t0) / .36; if (qq < 0) continue; const tx = c.cx - 18 + i * 12; if (qq < 1){ const my = c.y - 100 + (c.y - 108 + 100) * qq; for (let k = 0; k < 6; k++) c.R(tx + k * .8, my - k * 5, 3, 3, k < 2 ? '#fff6a0' : k < 4 ? '#ff9a3a' : '#8a8a96', .9 - k * .12); c.R(tx - 1, my, 5, 7, '#dfe6f0'); c.R(tx, my + 7, 3, 3, '#ff5a3a'); } else { const e = Math.min(1, (qq - 1) * 2.2); c.ring(tx, c.y - 6, 4 + e * 18, 2 + e * 8, 14, i % 2 ? '#ffd04a' : '#ff7a2a', 1 - e, i); } } },
    laser(c, q, o){ const gw = Math.min(1, q * 4), th = (o.w || 5) + S(Math.min(1, q) * PI) * 8; c.R(c.cx - 130, c.cy - th * 2, 130 * gw + 6, th * 4, o.c2 || o.c, c.fade(q) * .3); c.R(c.cx - 130, c.cy - th, 130 * gw + 6, th * 2, o.c, c.fade(q) * .7); c.R(c.cx - 130, c.cy - th * .4, 130 * gw + 6, th * .8, '#fff', c.fade(q)); if (q > .2) { const e = (q - .2) / .8; c.shock(4 + e * 40, o.c, 1 - e); c.star(c.cx, c.cy, '#fff', 1 - e, 10 - e * 6); } },
    bloom(c, q, o){ const e = Math.min(1, q * 2.2); c.g.globalAlpha = (1 - q) * .6; c.g.fillStyle = o.c; c.g.beginPath(); c.g.ellipse(c.cx, c.cy, 8 + e * 30 * (o.s || 1), 6 + e * 24 * (o.s || 1), 0, 0, 7); c.g.fill(); c.g.fillStyle = o.c2 || '#fff6c0'; c.g.beginPath(); c.g.ellipse(c.cx, c.cy, 4 + e * 18 * (o.s || 1), 3 + e * 14 * (o.s || 1), 0, 0, 7); c.g.fill(); c.g.globalAlpha = 1; c.ring(c.cx, c.cy, 10 + e * 36 * (o.s || 1), 8 + e * 28 * (o.s || 1), 22, '#fff', 1 - e, 0, 3); for (let i = 0; i < 8; i++) c.star(c.cx + K(i * .785) * e * 36, c.cy + S(i * .785) * e * 28, o.c, 1 - e, 2); },
    dome(c, q, o){ const a = Math.sin(q * PI), r = (o.s || 1); c.g.globalAlpha = a * .3; c.g.fillStyle = o.c; c.g.beginPath(); c.g.ellipse(c.cx, c.cy - 2, 18 * r, 24 * r, 0, 0, 7); c.g.fill(); c.g.globalAlpha = 1; c.ring(c.cx, c.cy - 2, 18 * r, 24 * r, 28, o.c2 || '#fff', a, q * 2, 2); for (let i = 0; i < 6; i++) c.star(c.cx - 14 + c.rn(i) * 28, c.cy - 26 + ((q * 1.4 + c.rn(i + 7)) % 1) * 44, o.c, c.fade(q), 1); },
    wings(c, q, o){ for (let s = -1; s <= 1; s += 2) for (let i = 0; i < 6; i++){ const e = Math.min(1, q * 4) * (1 - Math.max(0, q - .7) * 3); c.line(c.cx + s * 4, c.cy - 6, c.cx + s * (10 + i * 5 * (o.s || 1)) * e, c.cy - 6 - (14 - i * 3) * e - i * 2, i % 2 ? '#fff' : o.c, .9 * Math.max(0, e), 3, 1); } },
    // ----- 지원 -----
    aura(c, q, o){ for (let k = 0; k < (o.n || 4); k++){ const ax = c.cx - 12 + k * 8, ay = c.y + 2 - q * 34 - k * 3; c.R(ax, ay, 1, 5, o.c, c.fade(q)); c.R(ax - 1, ay + 1, 3, 1, o.c, c.fade(q)); c.R(ax - 2, ay + 2, 5, 1, o.c, c.fade(q)); } c.ring(c.cx, c.y, 8 + q * 14, 3 + q * 5, 14, o.c2 || o.c, c.fade(q) * .7, 0); },
    down(c, q, o){ for (let k = 0; k < (o.n || 4); k++){ const ax = c.cx - 12 + k * 8, ay = c.y - 38 + q * 34 + k * 3; c.R(ax, ay, 1, 5, o.c, c.fade(q)); c.R(ax - 1, ay + 3, 3, 1, o.c, c.fade(q)); c.R(ax - 2, ay + 2, 5, 1, o.c, c.fade(q)); } c.ring(c.cx, c.cy, 18 - q * 8, 18 - q * 8, 16, o.c2 || o.c, c.fade(q) * .6, q * 4); },
    heal(c, q, o){ for (let k = 0; k < (o.n || 7); k++) c.plus(c.cx - 14 + (k * 5) % 28 + S(q * 6 + k) * 2, c.y + 4 - q * 34 * (.5 + c.rn(k) * .7), o.c, c.fade(q)); },
    feathers(c, q, o){ for (let i = 0; i < (o.n || 10); i++){ const t = (q * 1.1 + c.rn(i) * .35) % 1, fx = c.cx - 16 + c.rn(i + 2) * 32 + S(q * 7 + i) * 4, fy = c.cy - 36 + t * 46; c.R(fx, fy, 3, 1, '#fff', c.fade(q)); c.R(fx + 1, fy + 1, 2, 1, o.c, c.fade(q)); } },
    cleanse(c, q, o){ const r = 6 + q * 30; c.ring(c.cx, c.cy, r, r * .8, 22, o.c, c.fade(q), q * 3); c.ring(c.cx, c.cy, r * .6, r * .5, 14, '#fff', c.fade(q), -q * 3); for (let i = 0; i < 6; i++) c.star(c.cx - 14 + c.rn(i) * 28, c.cy + 16 - q * 36 * (.5 + c.rn(i + 5)), o.c, c.fade(q), 1); },
    revive(c, q, o){ const a = Math.sin(q * PI), W = o.w || 12; c.R(c.cx - W / 2, c.y - 100, W, 96, o.c, a * .5); c.R(c.cx - W / 4, c.y - 100, W / 2, 96, '#fff', a * .9); c.ring(c.cx, c.cy - 26 - q * 4, 11, 4, 14, '#ffe27a', a, q * 4); for (let i = 0; i < 8; i++) c.star(c.cx - 14 + c.rn(i) * 28, c.y - 4 - q * 40 * (.4 + c.rn(i + 3)), '#fff6c0', c.fade(q), 1); },
    mp(c, q, o){ for (let i = 0; i < 8; i++){ const a = i * .8 + q * 6, t = (q * 1.3 + i / 8) % 1, r = 30 * (1 - t); c.R(c.cx + K(a) * r - 1, c.cy + S(a) * r * .7 - 1, 4, 4, i % 2 ? o.c : '#fff', c.fade(q)); } c.ring(c.cx, c.y, 12 + q * 10, 4 + q * 3, 14, o.c, c.fade(q), 0); },
    shout(c, q, o){ for (let i = 0; i < 4; i++){ const t = Math.max(0, q * 1.4 - i * .18); if (t > 1) continue; c.ring(c.cx, c.cy - 8, 6 + t * 38, 6 + t * 30, 22, i % 2 ? o.c2 || '#ffd866' : o.c, 1 - t, i, 3); } for (let i = 0; i < 6; i++){ const a = i * PI / 3; c.line(c.cx + K(a) * 8, c.cy - 8 + S(a) * 8, c.cx + K(a) * (14 + q * 28), c.cy - 8 + S(a) * (14 + q * 28), o.c, c.fade(q), 2, 1); } },
    smoke(c, q, o){ for (let i = 0; i < 7; i++){ const t = (q * .9 + i / 7) % 1; c.g.globalAlpha = (1 - t) * .55; c.g.fillStyle = i % 2 ? o.c : o.c2 || '#9a9aa8'; c.g.beginPath(); c.g.ellipse(c.cx + (c.rn(i) - .5) * 28 + t * 8, c.cy - t * 18 + 4, 7 + t * 9, 5 + t * 6, 0, 0, 7); c.g.fill(); } c.g.globalAlpha = 1; },
    trap(c, q, o){ const t = ease(q * 2.5), r = 22 * (1 - t * .55); c.ring(c.cx, c.y, r, r * .32, 20, o.c, c.fade(q), 0, 3); for (let i = 0; i < 10; i++){ const a = i * PI / 5; c.R(c.cx + K(a) * r - 1, c.y + S(a) * r * .32 - 4 * t, 2, 4 * t + 2, '#cfd6e0', c.fade(q)); } if (q > .4) c.star(c.cx, c.y - 4, o.c2 || '#fff', c.fade(q), 5); },
    net(c, q, o){ const t = ease(q * 2), W = 40, H = 30; for (let i = 0; i <= 5; i++){ c.R(c.cx - W / 2 + i * W / 5, c.y - 50 + t * 40, 1, H, o.c, c.fade(q)); c.R(c.cx - W / 2, c.y - 50 + t * 40 + i * H / 5, W, 1, o.c, c.fade(q)); } if (q > .4) for (let i = 0; i < 6; i++) c.R(c.cx - 18 + c.rn(i) * 36, c.y - 30 + c.rn(i + 4) * 24, 2, 2, o.c2 || '#fff', c.fade(q) * (S(q * 40 + i) > 0 ? 1 : .2)); },
    stars(c, q, o){ for (let i = 0; i < 4; i++){ const a = i * PI / 2 + q * 10; c.star(c.cx + K(a) * 12, c.cy - 22 + S(a) * 4, o.c, c.fade(q), 2); } },
    chains(c, q, o){ for (let i = -1; i <= 1; i++){ const e = ease(q * 2.4); for (let k = 0; k < 10 * e; k++) c.R(c.cx + i * 9 + (k % 2) * 1, c.y - 70 + k * 6, 4, 4, k % 2 ? o.c : o.c2 || '#8a8a96', c.fade(q)); } c.shock(4 + q * 20, o.c, c.fade(q)); },
    regen(c, q, o){ for (let i = 0; i < 12; i++){ const a = i * .7 + q * 6; c.R(c.cx + K(a) * (8 + (i % 3) * 3), c.y + 4 - ((q * 1.1 + i / 12) % 1) * 40, 3, 2, i % 2 ? o.c : o.c2 || '#b9ff8a', c.fade(q)); } },
    sparkle(c, q, o){ for (let i = 0; i < (o.n || 10); i++) c.star(c.cx - 18 + c.rn(i) * 36, c.cy - 20 + c.rn(i + 7) * 36, i % 2 ? o.c : o.c2 || '#fff', c.fade(q) * Math.abs(S(q * 9 + i)), 1 + (i % 2)); },
    ring(c, q, o){ const r = 8 + q * 30 * (o.s || 1); c.ring(c.cx, c.cy, r, r * .8, 22, o.c, c.fade(q), q * 2, 2); },
    rune(c, q, o){ const e = ease(q * 4), r = (o.s || 1) * 24 * e; c.ring(c.cx, c.y, r, r * .3, 22, o.c, c.fade(q), q * 3); c.ring(c.cx, c.y, r * .6, r * .2, 14, o.c2 || '#fff', c.fade(q), -q * 4); for (let i = 0; i < 6; i++){ const a = i * PI / 3 + q * 3; c.R(c.cx + K(a) * r, c.y + S(a) * r * .3, 3, 3, '#fff', c.fade(q)); } },
    // ----- 연출 (웅장한 스킬용) -----
    flash(c, q, o){ if (!c.first) return; c.flash(o.c || '#fff', (1 - q) * (o.a || .6)); },
    dim(c, q, o){ if (!c.first) return; c.flash(o.c || '#0a0418', Math.sin(q * PI) * (o.a || .4)); },
    bigring(c, q, o){ c.shock(8 + q * (o.s || 1) * 150, o.c, 1 - q, c.cx, c.y); c.shock(4 + q * (o.s || 1) * 100, o.c2 || '#fff', 1 - q, c.cx, c.y); },
    godray(c, q, o){ const a = Math.sin(q * PI); for (let i = 0; i < 7; i++){ const x0 = c.cx - 60 + i * 20, w = 5 + (i % 3) * 3; c.line(x0 + 20, c.y - 150, x0 - 10, c.y - 4, o.c, a * .35, w, 1); } },
    column(c, q, o){ const a = Math.sin(q * PI), H = 150; for (let i = 0; i < 6; i++) c.R(c.cx - 14 + i * 5, c.y - H, 5, H, [o.c, '#fff6c0', '#fff', '#fff', '#fff6c0', o.c][i], a * .75); },
    rain(c, q, o){ for (let i = 0; i < (o.n || 24); i++){ const t = (q * 1.5 + c.rn(i)) % 1; c.R(c.cx - 50 + c.rn(i + 5) * 100, c.y - 100 + t * 96, 2, 6, o.c, c.fade(q)); } },
    giant(c, q, o){ const e = ease(q * 1.6), sc = o.s || 1; // 거대한 무기 그림자: 위에서 내려와 박힘
      const ty = c.y - 130 + e * 120; if (o.k === 'axe'){ c.R(c.cx - 2, ty - 30, 5, 50, '#6a4a2a', c.fade(q)); c.R(c.cx - 24, ty - 36, 26, 16, '#cfd6e0', c.fade(q)); c.R(c.cx - 24, ty - 36, 26, 3, '#fff', c.fade(q)); c.R(c.cx + 3, ty - 32, 8, 8, '#9aa3b8', c.fade(q)); } else if (o.k === 'sword'){ c.R(c.cx - 4, ty - 70, 9, 70, '#e8f4ff', c.fade(q)); c.R(c.cx - 12, ty - 4, 25, 5, '#ffd866', c.fade(q)); c.R(c.cx - 2, ty + 1, 5, 14, '#8a6a4a', c.fade(q)); } else { c.R(c.cx - 2, ty - 10, 5, 50, '#8a6a4a', c.fade(q)); c.R(c.cx - 16, ty - 24, 33, 16, '#d0d8e0', c.fade(q)); c.R(c.cx - 16, ty - 24, 33, 3, '#fff', c.fade(q)); } },
  };
  // ----- 스킬 표: [층...] (층 = [부품, 옵션]) · g: 웅장함 · d: 길이(ms) · once: 대상이 여럿이어도 한 번만
  const T = {};
  const add = (key, layers, o = {}) => { T[key] = { layers, d: o.d || (o.g ? 2300 : 1000), g: !!o.g, once: !!o.once }; };
  const J = (job, items) => Object.entries(items).forEach(([n, v]) => add(job + '.' + n, v[0], v[1]));
  const W = '#fff', FI = ['#ff5a2a', '#ff9a3a', '#ffd04a'], PU = ['#3a1060', '#8a3ac0', '#d09aff', '#ff5aa0'], GR = ['#2f8a3a', '#5fcf5a', '#b9ff8a'];
  // 전사
  J('warrior', {
    '강타': [[['burst', { c: '#ffd866', n: 10 }], ['starburst', { c: '#fff', n: 6, s: .6 }]]],
    '차지 베기': [[['thrust', { c: '#ff7a3a', c2: '#ffd866', s: 1.2 }], ['burst', { c: '#ff9a3a', t0: .35, n: 10 }]]],
    '대지 가르기': [[['crack', { c: '#ff7a3a' }], ['ground', { c: '#c0a070', s: .8 }]]],
    '분노의 일격': [[['chop', { c: '#ff3a2a', w: 5 }], ['starburst', { c: '#ff5a3a', t0: .35, n: 8 }]]],
    '극한 차지': [[['dim', { a: .4 }], ['thrust', { c: '#ff3a1a', c2: '#ffd04a', s: 1.6, n: 3 }], ['bigring', { c: '#ff5a2a', t0: .35, t1: 1, s: 1 }], ['crack', { c: '#ff3a1a', t0: .35 }], ['flash', { t0: .3, t1: .5, c: '#fff6c0' }]], { g: 1 }],
    '되받아치기': [[['dome', { c: '#ffb070', c2: '#fff', s: .8 }], ['shout', { c: '#ff7a3a', t0: .4 }]]],
    '전장의 포효': [[['shout', { c: '#ff5a2a', c2: '#ffd04a' }], ['aura', { c: '#ff7a3a', t0: .2 }]]],
    '회전 베기': [[['spin', { c: '#ffd866', c2: '#ff9a3a', s: 1.2 }]]],
    '투척 도끼': [[['orb', { c: '#cfd6e0', c2: '#8a6a4a', s: 1 }], ['burst', { c: '#ffd866', t0: .5 }]]],
    '파쇄': [[['chop', { c: '#9aa3b8', w: 3 }], ['down', { c: '#ff7a3a', t0: .4 }]]],
    '학살자': [[['cross', { c: '#ff2a2a', n: 4, w: 3 }], ['skulls', { n: 3, t0: .3 }]]],
    '폭풍 도끼': [[['dim', { a: .35 }], ['spin', { c: '#ff9a3a', c2: '#ffd04a', s: 1.5 }], ['swirl', { c: '#ffb070', s: 1.4 }], ['rain', { c: '#cfd6e0', n: 20, t0: .2 }], ['bigring', { c: '#ff7a3a', t0: .5, s: .8 }]], { g: 1 }],
  });
  // 흑마법사
  J('black', {
    '불꽃탄': [[['orb', { c: '#ff7a2a', c2: '#ffd04a', s: 1 }]]],
    '화염구': [[['orb', { c: '#ff5a2a', c2: '#ff9a3a', s: 1.6 }], ['flame', { c: FI, t0: .5, h: 30 }]]],
    '불씨': [[['flame', { c: FI, n: 10, h: 22 }], ['sparkle', { c: '#ffd04a', n: 8 }]]],
    '지옥불': [[['flame', { c: ['#3a1060', '#c82a3a', '#ff5a2a', '#ffb040'], n: 28, h: 56, s: 1.3 }], ['rune', { c: '#c82a3a', s: 1.2 }], ['bloom', { c: '#ff3a2a', t0: .3, s: .8 }]]],
    '메테오': [[['dim', { a: .45 }], ['meteors', { c: '#ff7a2a', c2: '#5a2a10', n: 5, s: 2 }], ['bigring', { c: '#ff5a2a', t0: .55, s: .9 }], ['flash', { t0: .5, t1: .7, c: '#fff0c0' }], ['crack', { c: '#ff3a1a', t0: .55 }]], { g: 1, d: 2600 }],
    '서리 화살': [[['thrust', { c: '#8adfff', c2: '#fff', s: 1 }], ['snow', { c: '#8adfff', n: 8, t0: .4 }]]],
    '얼음 창': [[['shards', { c: '#6ad0ff', c2: '#e8fbff', s: 1.3 }]]],
    '번개': [[['bolt', { c: '#ffe650' }]]],
    '연쇄 번개': [[['bolt', { c: '#ffe650', n: 3 }], ['chain', { c: '#9ad8ff', t0: .3 }], ['flash', { c: '#fff8c0', t1: .25, a: .35 }]]],
    '눈보라': [[['snow', { c: '#bfefff', n: 24 }], ['swirl', { c: '#dff4ff', s: 1.4 }]]],
    '마력 흡수': [[['mp', { c: '#b070ff' }], ['hand', { c: '#6a2aa0', t0: .2 }]]],
    '약점 간파': [[['down', { c: '#d0a0ff', c2: '#ff5aa0' }], ['stars', { c: '#ff5aa0', t0: .3 }]]],
    '암흑 구체': [[['orb', { c: '#6a2aa0', c2: '#d09aff', s: 1.7 }], ['burst', { c: '#ff5aa0', t0: .5, n: 12 }]]],
    '공허의 손': [[['hand', { c: '#3a1060', c2: '#d09aff' }], ['skulls', { n: 3, t0: .3 }], ['stars', { c: '#ffe650', t0: .5 }]]],
  });
  // 도적
  J('thief', {
    '찌르기': [[['thrust', { c: '#7ae8ff', s: .8 }]]],
    '이중 베기': [[['cross', { c: '#7ae8ff', n: 2 }]]],
    '칼춤': [[['spin', { c: '#7ae8ff', c2: '#fff', s: 1.3 }], ['cross', { c: '#fff', n: 3, t0: .3 }]]],
    '연환': [[['cross', { c: '#7ae8ff', n: 5, seed: 3 }]]],
    '난도질': [[['cross', { c: '#7ae8ff', n: 7, seed: 7, w: 3 }], ['burst', { c: '#ff4a5a', t0: .55, n: 12 }]]],
    '출혈': [[['cross', { c: '#c0203a', n: 2, w: 3 }], ['cloud', { c: '#8a0a1a', c2: '#ff4a5a', s: .6 }]]],
    '급소 찌르기': [[['thrust', { c: '#ff4a5a', s: 1 }], ['starburst', { c: '#ff4a5a', t0: .4, n: 4, rot: .78 }]]],
    '처형자': [[['cross', { c: '#e8e0ff', n: 2, w: 4, seed: 11 }], ['skulls', { n: 2, t0: .3 }]]],
    '피 웅덩이': [[['cloud', { c: '#8a0a1a', c2: '#ff4a5a', s: 1.2 }], ['ring', { c: '#ff4a5a', t0: .4 }], ['burst', { c: '#c0203a', t0: .5 }]]],
    '연막': [[['smoke', { c: '#6a6a78', c2: '#9a9aa8' }]]],
    '그림자 걸음': [[['smoke', { c: '#2a2040', c2: '#1a1030' }], ['aura', { c: '#7a5aa0', t0: .3, n: 3 }]]],
    '훔치기': [[['thrust', { c: '#ffd866', s: .8 }], ['sparkle', { c: '#ffd866', n: 8, t0: .3 }]]],
    '뒤잡기': [[['blades', { c: '#7ae8ff', n: 6 }], ['stars', { c: '#ffe650', t0: .4 }]]],
  });
  // 음유시인
  J('bard', {
    '용기의 노래': [[['notes', { c: '#ffd866' }], ['aura', { c: '#ffb04a', t0: .3 }]]],
    '승리의 행진': [[['thrust', { c: '#ffd866', s: .8 }], ['notes', { c: '#ff9ac0', n: 5, t0: .2 }], ['aura', { c: '#ffd866', t0: .4, n: 3 }]]],
    '전장의 북소리': [[['shout', { c: '#a0522d', c2: '#ffd866' }], ['aura', { c: '#7aef6a', t0: .3 }]]],
    '불꽃의 변주': [[['notes', { c: '#ff7a2a', n: 8 }], ['flame', { c: FI, n: 16, h: 40, t0: .2 }], ['burst', { c: '#ffd04a', t0: .5 }]]],
    '영웅의 서사시': [[['dim', { a: .3 }], ['notes', { c: '#ffd866', n: 10 }], ['column', { c: '#ffe27a', t0: .15 }], ['aura', { c: '#ffd866', t0: .3 }]], { g: 0 }],
    '수호의 노래': [[['dome', { c: '#9ad8ff', c2: '#fff', s: .9 }], ['notes', { c: '#9ad8ff', n: 4, t0: .3 }]]],
    '자장가': [[['stars', { c: '#c8a0ff' }], ['notes', { c: '#c8a0ff', n: 4 }], ['regen', { c: '#9affc8', t0: .3 }]]],
    '평온의 선율': [[['heal', { c: '#7affb0' }], ['notes', { c: '#ffb0d8', n: 5, t0: .2 }]]],
    '되살림의 화음': [[['revive', { c: '#ffe27a', w: 8 }], ['notes', { c: '#ffd866', n: 6, t0: .3 }]]],
    '별빛 합창': [[['dim', { a: .35 }], ['notes', { c: '#9ad8ff', n: 12 }], ['sparkle', { c: '#fff6c0', n: 20 }], ['heal', { c: '#bfffe0', t0: .3, n: 10 }], ['bigring', { c: '#9ad8ff', t0: .4, s: .6 }]], { g: 1 }],
    '불협화음': [[['down', { c: '#a05ad0', c2: '#ff4a5a' }], ['chain', { c: '#c8a0ff', t0: .2 }]]],
    '도발의 곡': [[['shout', { c: '#ff5a5a', c2: '#ffd866' }], ['notes', { c: '#ff5a5a', n: 4, t0: .2 }]]],
    '흥겨운 춤': [[['notes', { c: '#ffb0d8', n: 8 }], ['spin', { c: '#ffd866', c2: '#ff9ac0', s: 1 }], ['aura', { c: '#7aef6a', t0: .4, n: 3 }]]],
    '앙코르': [[['ring', { c: '#ffd866', s: 1 }], ['notes', { c: '#ffd866', n: 6, t0: .2 }]]],
    '대합창': [[['dim', { a: .4 }], ['godray', { c: '#ffe0a0' }], ['notes', { c: '#ffd866', n: 14 }], ['bigring', { c: '#ffd866', t0: .35, s: 1 }], ['burst', { c: '#ff9ac0', t0: .5, n: 16, s: 1.8 }], ['flash', { t0: .35, t1: .55, c: '#fff6d0' }]], { g: 1 }],
  });
  // 시간술사
  J('time', {
    '서두르기': [[['aura', { c: '#9ad8ff', n: 4 }], ['clock', { c: '#9ad8ff', s: .6 }]]],
    '연속 가속': [[['clock', { c: '#9ad8ff', s: 1 }], ['aura', { c: '#bfefff', t0: .3 }]]],
    '시간 도약': [[['burst', { c: '#9ad8ff', n: 12 }], ['aura', { c: '#fff', t0: .2, n: 3 }]]],
    '가속 영역': [[['rune', { c: '#9ad8ff', s: 1.3 }], ['clock', { c: '#9ad8ff', s: 1.3 }], ['aura', { c: '#bfefff', t0: .3 }]]],
    '늦추기': [[['down', { c: '#6aa8e8' }], ['clock', { c: '#6aa8e8', s: .8 }]]],
    '정지': [[['clock', { c: '#fff', s: 1.1 }], ['shards', { c: '#bfefff', t0: .4, s: .8 }], ['stars', { c: '#ffe650', t0: .5 }]]],
    '늪 같은 시간': [[['cloud', { c: '#4a6aa8', c2: '#9ad8ff', s: 1.1 }], ['down', { c: '#6aa8e8', t0: .3 }]]],
    '시간 정체': [[['rune', { c: '#6aa8e8', s: 1.5 }], ['snow', { c: '#bfefff', n: 12 }], ['down', { c: '#9ad8ff', t0: .3 }]]],
    '영원한 정오': [[['flash', { c: '#fff6c0', a: .7, t1: .35 }], ['clock', { c: '#ffe27a', s: 2.2 }], ['bigring', { c: '#ffe27a', t0: .3, s: 1 }], ['godray', { c: '#fff0b0', t0: .2 }], ['rain', { c: '#ffe6a0', n: 20, t0: .3 }]], { g: 1, d: 2500 }],
    '되감기': [[['heal', { c: '#9ad8ff' }], ['clock', { c: '#9ad8ff', s: .8 }]]],
    '시계 소환': [[['clock', { c: '#fff', s: 1.6 }], ['ring', { c: '#9ad8ff', t0: .3, s: 1.2 }], ['stars', { c: '#ffe650', t0: .5 }]]],
    '시간 균열': [[['crack', { c: '#bfefff', c2: '#fff' }], ['bolt', { c: '#9ad8ff', t0: .1 }], ['burst', { c: '#fff', t0: .4 }]]],
    '시간 정지': [[['dim', { a: .5, c: '#101830' }], ['flash', { c: '#fff', t1: .15, a: .8 }], ['bigring', { c: '#9ad8ff', s: 1.1 }], ['clock', { c: '#fff', s: 2.4 }], ['snow', { c: '#bfefff', n: 24, t0: .2 }]], { g: 1, d: 2500 }],
  });
  // 연금술사
  J('alch', {
    '산성 플라스크': [[['orb', { c: '#9aff4a', c2: '#cfefff', s: 1 }], ['bubbles', { c: '#9aff4a', t0: .5 }]]],
    '독 병': [[['orb', { c: '#7adf5a', c2: '#2f8a3a', s: 1 }], ['cloud', { c: '#4a9a3a', c2: '#a05ad0', t0: .5 }]]],
    '불안정 용액': [[['down', { c: '#ff9ac0', c2: '#ff4aff' }], ['bubbles', { c: '#ff9ac0', n: 8 }]]],
    '부식': [[['orb', { c: '#c0ff4a', c2: '#6a8a1a', s: 1.2 }], ['down', { c: '#c0ff4a', t0: .5 }]]],
    '약점 증폭': [[['down', { c: '#ffb04a', c2: '#ff5a2a' }], ['starburst', { c: '#ffd04a', t0: .4, n: 6, s: .7 }]]],
    '응급 물약': [[['heal', { c: '#ff9ac0', n: 6 }], ['bubbles', { c: '#ff7aa8', n: 6 }]]],
    '마력 물약': [[['mp', { c: '#6aa8ff' }], ['bubbles', { c: '#6aa8ff', n: 8 }]]],
    '혼합 약': [[['regen', { c: '#7adf5a', c2: '#a05ad0' }], ['bubbles', { c: '#c07aff', n: 8 }]]],
    '엘릭서': [[['cleanse', { c: '#ffd866' }], ['sparkle', { c: '#fff6c0', n: 14 }], ['heal', { c: '#bfffe0', t0: .2 }], ['bigring', { c: '#ffd866', t0: .3, s: .5 }]]],
    '변이약': [[['aura', { c: '#c07aff', c2: '#7adf5a', n: 4 }], ['bubbles', { c: '#c07aff', n: 10 }], ['burst', { c: '#ff9aff', t0: .5 }]]],
    '폭죽탄': [[['orb', { c: '#ff5aa0', c2: '#ffd04a', s: .8 }], ['burst', { c: '#ffd04a', c2: '#ff5aa0', t0: .5, n: 16, rot: .2 }], ['sparkle', { c: '#fff', t0: .5 }]]],
    '점착 폭탄': [[['orb', { c: '#ffb04a', c2: '#8a6a1a', s: 1 }], ['cloud', { c: '#c0a040', t0: .5, s: .8 }], ['down', { c: '#ffd04a', t0: .6, n: 3 }]]],
    '연쇄 반응': [[['bloom', { c: '#ff7a2a', c2: '#ffd04a', s: .8 }], ['chain', { c: '#ffb04a', t0: .2 }], ['bloom', { c: '#8aff6a', t0: .4, s: .7 }]]],
    '황금 폭발': [[['bloom', { c: '#ffd04a', c2: '#fff6c0', s: 1.2 }], ['fountain', { c: '#ffd866', n: 16, t0: .2 }], ['starburst', { c: '#ffd04a', t0: .2, n: 10 }]]],
    '연금 대폭발': [[['dim', { a: .45 }], ['bloom', { c: '#ff7ac0', c2: '#ffd04a', s: 2.2 }], ['flash', { t0: .15, t1: .4, c: '#fff6d0' }], ['bigring', { c: '#8aff6a', t0: .2, s: 1 }], ['cloud', { c: '#8aff6a', c2: '#c07aff', t0: .25, s: 2 }], ['fountain', { c: '#ffd866', n: 24, t0: .25 }]], { g: 1, d: 2500 }],
  });
  // 백마법사
  J('white', {
    '치유': [[['heal', { c: '#7affb0' }]]],
    '큰 치유': [[['heal', { c: '#9affc8', n: 10 }], ['ring', { c: '#bfffe0', t0: .3 }]]],
    '집단 치유': [[['feathers', { c: '#fff0a0' }], ['heal', { c: '#7affb0', t0: .2 }], ['ring', { c: '#fff', t0: .3 }]]],
    '신성한 비': [[['rain', { c: '#fff6c0', n: 22 }], ['sparkle', { c: '#fff', n: 12, t0: .2 }]]],
    '기적의 손길': [[['pillar', { c: '#fff6c0', w: 8, h: 80 }], ['heal', { c: '#bfffe0', t0: .2, n: 9 }], ['crossf', { c: '#ffe27a', t0: .3, s: .8 }]]],
    '되살리기': [[['revive', { c: '#fff0a0' }]]],
    '완전 소생': [[['revive', { c: '#ffe27a', w: 16 }], ['wings', { c: '#fff0a0', t0: .3, s: .8 }], ['feathers', { c: '#fff', t0: .3 }]]],
    '전체 소생': [[['dim', { a: .35 }], ['godray', { c: '#fff6c0' }], ['revive', { c: '#ffe27a', w: 14 }], ['feathers', { c: '#fff', n: 16, t0: .2 }], ['bigring', { c: '#fff0a0', t0: .4, s: .8 }]], { g: 1 }],
    '천사의 숨결': [[['dim', { a: .45 }], ['flash', { c: '#fff', t1: .3, a: .6 }], ['wings', { c: '#fff6c0', s: 2.4 }], ['column', { c: '#ffe27a', t0: .1 }], ['feathers', { c: '#fff', n: 22, t0: .2 }], ['bigring', { c: '#ffe27a', t0: .35, s: 1.1 }], ['heal', { c: '#bfffe0', n: 12, t0: .3 }]], { g: 1, d: 2600 }],
    '성광탄': [[['orb', { c: '#fff6c0', c2: '#ffe27a', s: 1.1 }], ['starburst', { c: '#fff', t0: .5, n: 8 }]]],
    '정화': [[['cleanse', { c: '#bfffe0' }], ['sparkle', { c: '#fff', n: 10 }]]],
    '빛의 장막': [[['dome', { c: '#fff6c0', c2: '#fff', s: 1.2 }], ['sparkle', { c: '#ffe27a', n: 8 }]]],
    '심판의 빛': [[['beams', { c: '#fff6c0', n: 6 }], ['bigring', { c: '#ffe27a', t0: .5, s: .5 }], ['flash', { t0: .3, t1: .5, c: '#fffbe0', a: .4 }]]],
    '광휘의 후광': [[['ring', { c: '#ffe27a', s: 1.2 }], ['aura', { c: '#fff0a0', n: 4, t0: .2 }], ['sparkle', { c: '#fff', n: 8, t0: .3 }]]],
  });
  // 드루이드
  J('druid', {
    '새싹': [[['regen', { c: '#7aef6a' }], ['sparkle', { c: '#c8ffd0', n: 6 }]]],
    '재생의 숲': [[['regen', { c: '#5fcf5a', c2: '#b9ff8a' }], ['heal', { c: '#7affb0', t0: .2 }], ['ring', { c: '#7aef6a', t0: .3 }]]],
    '뿌리 속박': [[['thorns', { c: '#8a6a3a', c2: '#c0a070', s: 1.1 }], ['down', { c: '#8a6a3a', t0: .4, n: 3 }]]],
    '생명의 나무': [[['pillar', { c: '#5fcf5a', c2: '#b9ff8a', w: 10, h: 90 }], ['feathers', { c: '#7aef6a', t0: .2 }], ['heal', { c: '#bfffe0', t0: .3, n: 10 }]]],
    '만개': [[['bloom', { c: '#ff9ac8', c2: '#ffe04a', s: 1.1 }], ['regen', { c: '#7aef6a', t0: .2 }], ['sparkle', { c: '#fff', n: 10, t0: .3 }]]],
    '자연 보호막': [[['dome', { c: '#5fcf5a', c2: '#b9ff8a', s: 1 }], ['regen', { c: '#7aef6a', t0: .2 }]]],
    '이슬': [[['bubbles', { c: '#9ad8ff', c2: '#fff', n: 10 }], ['heal', { c: '#bfffe0', n: 5, t0: .2 }]]],
    '독 제거': [[['cleanse', { c: '#9affc8' }], ['cloud', { c: '#7adf5a', c2: '#bfffe0', s: .6, t0: .2 }]]],
    '태양의 은총': [[['pillar', { c: '#ffd866', w: 12, h: 110 }], ['starburst', { c: '#ffe27a', t0: .3, n: 12 }], ['aura', { c: '#ffd866', t0: .3 }]]],
    '가시 덩굴': [[['thorns', { c: '#2f8a3a', c2: '#e0ffb0', s: 1.2 }], ['burst', { c: '#7aef6a', t0: .4, n: 8 }]]],
    '곰의 가죽': [[['dome', { c: '#8a6a4a', c2: '#c0a070', s: .8 }], ['shout', { c: '#a07a4a', t0: .3 }]]],
    '늑대의 울음': [[['shout', { c: '#cfe0ff', c2: '#7a8ab0' }], ['aura', { c: '#cfe0ff', t0: .3 }], ['sparkle', { c: '#fff', n: 6, t0: .3 }]]],
    '야생의 화신': [[['dim', { a: .4 }], ['swirl', { c: '#5fcf5a', s: 2 }], ['thorns', { c: '#2f8a3a', s: 2.2, t0: .1 }], ['bloom', { c: '#ff9ac8', c2: '#ffe04a', s: 1.8, t0: .35 }], ['bigring', { c: '#7aef6a', t0: .4, s: 1 }], ['rain', { c: '#b9ff8a', n: 28, t0: .2 }]], { g: 1, d: 2500 }],
  });
  // 성직자
  J('cleric', {
    '수호의 기도': [[['dome', { c: '#ffe27a', c2: '#fff', s: .9 }], ['sparkle', { c: '#fff6c0', n: 8 }]]],
    '성스러운 방패': [[['dome', { c: '#9ad0ff', c2: '#fff', s: .8 }], ['crossf', { c: '#fff', t0: .3, s: .6 }]]],
    '대신 맞기': [[['shout', { c: '#9ad0ff', c2: '#fff' }], ['dome', { c: '#ffe27a', t0: .3, s: .8 }]]],
    '피해 흡수 막': [[['dome', { c: '#c8a0ff', c2: '#fff', s: 1.2 }], ['ring', { c: '#ffe27a', t0: .3 }]]],
    '해제': [[['cleanse', { c: '#fff6c0' }], ['burst', { c: '#fff', t0: .3, n: 10 }]]],
    '축복': [[['aura', { c: '#ffe27a', n: 5 }], ['sparkle', { c: '#fff', n: 10, t0: .1 }], ['cleanse', { c: '#fff0a0', t0: .3 }]]],
    '안식': [[['feathers', { c: '#bfefff' }], ['dome', { c: '#bfefff', t0: .2, s: 1 }]]],
    '순백의 종': [[['bell', { c: '#fff', c2: '#ffe27a' }], ['heal', { c: '#bfffe0', t0: .3 }]]],
    '구원의 빛': [[['revive', { c: '#ffe27a', w: 10 }], ['crossf', { c: '#fff', t0: .3, s: .9 }]]],
    '철퇴': [[['thrust', { c: '#d0d8e0', s: .6 }], ['starburst', { c: '#ffe27a', t0: .35, n: 6 }]]],
    '응징': [[['crossf', { c: '#ffe27a', s: 1.1 }], ['burst', { c: '#fff', t0: .3 }], ['shout', { c: '#ff9a3a', t0: .4 }]]],
    '신벌': [[['bolt', { c: '#ffe27a', n: 2 }], ['crossf', { c: '#fff', t0: .3, s: .8 }]]],
    '성스러운 낙인': [[['crossf', { c: '#ff5a5a', s: .9 }], ['down', { c: '#ffe27a', t0: .3 }], ['ring', { c: '#ff5a5a', t0: .4 }]]],
    '심판의 종': [[['dim', { a: .45 }], ['bell', { c: '#ffe27a', c2: '#fff' }], ['godray', { c: '#fff0a0', t0: .2 }], ['bigring', { c: '#ffe27a', t0: .4, s: 1 }], ['beams', { c: '#fff6c0', n: 7, t0: .4 }], ['flash', { t0: .4, t1: .6, c: '#fffbe0' }]], { g: 1, d: 2500 }],
  });
  // 기사
  J('knight', {
    '도발': [[['shout', { c: '#ff5a5a', c2: '#ffd866' }], ['stars', { c: '#ffd866', t0: .4 }]]],
    '방패 치기': [[['dome', { c: '#9ad0ff', c2: '#fff', s: .7 }], ['burst', { c: '#fff', t0: .3, n: 8 }], ['stars', { c: '#ffe650', t0: .4 }]]],
    '전열': [[['aura', { c: '#9ad0ff', n: 5 }], ['thrust', { c: '#9ad0ff', s: .6, t0: .2 }]]],
    '불굴의 외침': [[['shout', { c: '#ffd866', c2: '#ff7a3a' }], ['aura', { c: '#ffb04a', t0: .3 }], ['starburst', { c: '#fff', t0: .3, n: 8, s: .6 }]]],
    '막아서기': [[['dome', { c: '#7aa8e8', c2: '#fff', s: 1 }], ['ring', { c: '#fff', t0: .3, s: .7 }]]],
    '방어 태세': [[['dome', { c: '#9ad0ff', c2: '#cfe8ff', s: 1.1 }], ['aura', { c: '#cfe8ff', t0: .3, n: 3 }]]],
    '반격 태세': [[['dome', { c: '#ffb070', c2: '#fff', s: .8 }], ['arc', { c: '#ffd866', t0: .4 }]]],
    '수호의 서약': [[['rune', { c: '#ffd866', s: 1.3 }], ['dome', { c: '#ffe27a', t0: .3, s: 1.1 }], ['sparkle', { c: '#fff', t0: .2 }]]],
    '베기': [[['arc', { c: '#9ad0ff', s: 1 }]]],
    '돌격': [[['thrust', { c: '#9ad0ff', c2: '#fff', s: 1.5, n: 3 }], ['burst', { c: '#fff', t0: .4, n: 10 }]]],
    '방패 돌진': [[['thrust', { c: '#7aa8e8', s: 1.2 }], ['dome', { c: '#9ad0ff', t0: .3, s: .8 }], ['stars', { c: '#ffe650', t0: .5 }]]],
    '정의의 칼날': [[['arc', { c: '#fff', s: 1.4, v: 1 }], ['pillar', { c: '#9ad0ff', w: 6, h: 90, t0: .3 }], ['burst', { c: '#ffe27a', t0: .5 }]]],
    '기사의 일격': [[['dim', { a: .4 }], ['giant', { k: 'sword', t1: .55 }], ['bigring', { c: '#9ad0ff', t0: .4, s: 1 }], ['flash', { t0: .35, t1: .55, c: '#e8f6ff' }], ['crack', { c: '#9ad0ff', c2: '#fff', t0: .4 }], ['burst', { c: '#fff', t0: .4, n: 18, s: 1.8 }]], { g: 1 }],
  });
  // 기공사
  J('gadget', {
    '번개 쥐': [[['rune', { c: '#ffe650', s: .8 }], ['bolt', { c: '#ffe650', t0: .3 }], ['sparkle', { c: '#fff6a0', t0: .3, n: 6 }]]],
    '수호 쥐': [[['rune', { c: '#9ad0ff', s: .8 }], ['dome', { c: '#9ad0ff', t0: .3, s: .7 }]]],
    '광선 도마뱀': [[['rune', { c: '#ff5a5a', s: .9 }], ['laser', { c: '#ff5a5a', c2: '#ffb0b0', w: 3, t0: .3 }]]],
    '철갑 멧돼지': [[['rune', { c: '#cfd6e0', s: 1.2 }], ['ground', { c: '#cfd6e0', t0: .3, s: .8 }], ['dome', { c: '#8a95a8', t0: .4, s: .8 }]]],
    '덫 설치': [[['trap', { c: '#cfd6e0', c2: '#ffd04a' }]]],
    '지뢰': [[['trap', { c: '#8a95a8', c2: '#ffb040' }], ['bloom', { c: '#ff7a2a', t0: .5, s: .7 }]]],
    '전기 그물': [[['net', { c: '#9ad8ff', c2: '#ffe650' }], ['chain', { c: '#ffe650', t0: .4 }]]],
    '연쇄 함정': [[['trap', { c: '#cfd6e0' }], ['chain', { c: '#ffe650', t0: .2 }], ['bloom', { c: '#ff7a2a', t0: .5, s: .9 }], ['bubbles', { c: '#cfd6e0', n: 6, t0: .5 }]]],
    '대지 폭파': [[['dim', { a: .45 }], ['crack', { c: '#ff7a2a', c2: '#ffe27a' }], ['bloom', { c: '#ff5a2a', c2: '#ffe27a', s: 2.2, t0: .25 }], ['bigring', { c: '#ff7a2a', t0: .25, s: 1 }], ['flash', { t0: .25, t1: .45, c: '#fff0c0' }], ['meteors', { c: '#8a6a4a', c2: '#3a2a1a', n: 4, t0: .15 }]], { g: 1, d: 2500 }],
    '수류탄': [[['orb', { c: '#6a8a4a', c2: '#cfd6e0', s: 1 }], ['bloom', { c: '#ff9a3a', t0: .5, s: .7 }]]],
    '접착탄': [[['orb', { c: '#c0a040', c2: '#8a6a1a', s: 1 }], ['cloud', { c: '#c0a040', t0: .5, s: .8 }]]],
    '연막탄': [[['orb', { c: '#9a9aa8', c2: '#5a5a68', s: 1 }], ['smoke', { c: '#7a7a88', c2: '#aaaab8', t0: .4 }]]],
    '시한폭탄': [[['orb', { c: '#ff4a4a', c2: '#2a2a2a', s: 1.1 }], ['ring', { c: '#ff4a4a', t0: .5, s: .8 }], ['bloom', { c: '#ff7a2a', c2: '#ffe27a', t0: .7, s: 1.2 }]]],
    '집중 포화': [[['dim', { a: .4 }], ['missiles', { n: 6 }], ['thrust', { c: '#ffb040', s: 1.4, n: 3, t0: .2 }], ['bigring', { c: '#ff7a2a', t0: .5, s: .9 }], ['flash', { t0: .5, t1: .65, c: '#fff0c0', a: .5 }]], { g: 1, d: 2400 }],
  });

  // ----- 직업마다 가장 센 스킬 3개 (MP가 가장 큰 순서): 웅장한 연출로 덮어써요 (소환사는 xfx.js)
  const G = { g: 1, d: 2400 };
  add('warrior.대지 가르기', [['dim', { a: .45 }], ['giant', { k: 'axe', t1: .5 }], ['crack', { c: '#ff7a3a', c2: '#ffd866', t0: .38 }], ['bigring', { c: '#c0a070', t0: .38, s: 1 }], ['meteors', { c: '#8a6a4a', c2: '#3a2a1a', n: 4, t0: .3 }], ['flash', { t0: .36, t1: .55, c: '#fff0c0' }]], G);
  add('black.지옥불', [['dim', { a: .5 }], ['rune', { c: '#c82a3a', c2: '#ffb040', s: 2 }], ['flame', { c: ['#3a1060', '#c82a3a', '#ff5a2a', '#ffb040', '#fff6c0'], n: 40, h: 80, s: 2 }], ['bloom', { c: '#ff3a2a', c2: '#ffd04a', s: 1.8, t0: .3 }], ['bigring', { c: '#ff3a2a', t0: .35, s: 1 }], ['flash', { t0: .3, t1: .5, c: '#ffd0a0', a: .5 }]], G);
  add('black.연쇄 번개', [['dim', { a: .5, c: '#08041a' }], ['bolt', { c: '#ffe650', n: 5, seed: 3 }], ['chain', { c: '#9ad8ff', t0: .2 }], ['flash', { t0: .12, t1: .28, c: '#fff8c0', a: .8 }], ['flash', { t0: .45, t1: .6, c: '#fff8c0', a: .6 }], ['bigring', { c: '#ffe650', t0: .4, s: 1 }], ['bolt', { c: '#9ad8ff', n: 3, seed: 9, t0: .35, t1: .9 }]], G);
  add('thief.난도질', [['dim', { a: .4 }], ['cross', { c: '#7ae8ff', n: 10, seed: 5, w: 3 }], ['blades', { c: '#7ae8ff', n: 8, t0: .3 }], ['cross', { c: '#ff4a5a', n: 2, s: 1.8, w: 5, t0: .62, seed: 2 }], ['flash', { t0: .62, t1: .78, c: '#fff' }], ['bigring', { c: '#ff4a5a', t0: .65, s: .7 }]], G);
  add('thief.피 웅덩이', [['dim', { a: .5, c: '#1a0408' }], ['rune', { c: '#c0203a', c2: '#ff4a5a', s: 2 }], ['cloud', { c: '#8a0a1a', c2: '#ff4a5a', s: 2 }], ['hand', { c: '#8a0a1a', c2: '#ff9aa8', t0: .2 }], ['skulls', { n: 5, t0: .3 }], ['bigring', { c: '#ff4a5a', t0: .5, s: 1 }], ['flash', { t0: .5, t1: .65, c: '#ff4a5a', a: .45 }]], G);
  add('thief.급소 찌르기', [['dim', { a: .55, c: '#05030c' }], ['thrust', { c: '#ff2a3a', c2: '#fff', s: 1.7, n: 3 }], ['starburst', { c: '#ff2a3a', c2: '#fff', t0: .35, n: 4, s: 1.6, rot: .78 }], ['skulls', { n: 3, t0: .45 }], ['flash', { t0: .33, t1: .5, c: '#fff', a: .8 }], ['bigring', { c: '#ff2a3a', t0: .38, s: .8 }]], G);
  add('bard.불꽃의 변주', [['dim', { a: .4 }], ['notes', { c: '#ff7a2a', n: 14 }], ['flame', { c: FI, n: 34, h: 70, s: 1.8, t0: .1 }], ['column', { c: '#ff7a2a', t0: .2 }], ['bigring', { c: '#ffd04a', t0: .4, s: 1 }], ['burst', { c: '#ff5a2a', c2: '#ffd04a', t0: .45, n: 20, s: 2 }]], G);
  add('time.시간 정체', [['dim', { a: .5, c: '#0a1428' }], ['rune', { c: '#6aa8e8', c2: '#fff', s: 2 }], ['clock', { c: '#9ad8ff', s: 2 }], ['snow', { c: '#bfefff', n: 26, t0: .1 }], ['bigring', { c: '#9ad8ff', t0: .3, s: 1 }], ['down', { c: '#6aa8e8', t0: .35, n: 5 }], ['flash', { t0: .25, t1: .4, c: '#dff4ff', a: .5 }]], G);
  add('alch.엘릭서', [['dim', { a: .4 }], ['godray', { c: '#ffe27a' }], ['bloom', { c: '#ffd866', c2: '#fff6c0', s: 2 }], ['cleanse', { c: '#ffd866', t0: .1 }], ['heal', { c: '#bfffe0', n: 14, t0: .2 }], ['sparkle', { c: '#fff6c0', n: 24 }], ['bigring', { c: '#ffd866', t0: .3, s: .9 }]], G);
  add('alch.변이약', [['dim', { a: .45 }], ['bubbles', { c: '#c07aff', c2: '#7adf5a', n: 24 }], ['bloom', { c: '#c07aff', c2: '#7adf5a', s: 2, t0: .25 }], ['aura', { c: '#c07aff', c2: '#7adf5a', n: 6, t0: .3 }], ['bigring', { c: '#7adf5a', t0: .35, s: 1 }], ['burst', { c: '#ff9aff', c2: '#9aff4a', t0: .45, n: 20, s: 2 }]], G);
  add('white.심판의 빛', [['dim', { a: .5 }], ['godray', { c: '#fff6c0' }], ['beams', { c: '#fff6c0', n: 9 }], ['crossf', { c: '#ffe27a', s: 2.4, t0: .3 }], ['flash', { t0: .3, t1: .5, c: '#fffbe0', a: .7 }], ['bigring', { c: '#ffe27a', t0: .35, s: 1.1 }]], G);
  add('druid.만개', [['dim', { a: .4 }], ['regen', { c: '#7aef6a' }], ['bloom', { c: '#ff9ac8', c2: '#ffe04a', s: 2.4, t0: .2 }], ['rain', { c: '#ffc0e0', n: 30, t0: .2 }], ['sparkle', { c: '#fff', n: 22, t0: .3 }], ['bigring', { c: '#ff9ac8', t0: .35, s: 1 }], ['heal', { c: '#bfffe0', n: 12, t0: .3 }]], G);
  add('druid.생명의 나무', [['dim', { a: .45 }], ['pillar', { c: '#5fcf5a', c2: '#e0ffb0', w: 26, h: 150, t1: .8 }], ['rain', { c: '#b9ff8a', n: 30, t0: .15 }], ['regen', { c: '#7aef6a', c2: '#b9ff8a', t0: .15 }], ['heal', { c: '#bfffe0', n: 14, t0: .3 }], ['bigring', { c: '#7aef6a', t0: .3, s: 1 }], ['thorns', { c: '#2f8a3a', s: 1.6, t0: .05, t1: .5 }]], G);
  add('cleric.순백의 종', [['dim', { a: .4 }], ['godray', { c: '#fff0a0' }], ['bell', { c: '#fff', c2: '#ffe27a' }], ['bigring', { c: '#ffe27a', t0: .3, s: 1 }], ['heal', { c: '#bfffe0', n: 14, t0: .3 }], ['feathers', { c: '#fff0a0', n: 18, t0: .2 }]], G);
  add('cleric.구원의 빛', [['dim', { a: .5 }], ['flash', { c: '#fff', t1: .25, a: .6 }], ['revive', { c: '#ffe27a', w: 24 }], ['crossf', { c: '#fff', s: 2, t0: .25 }], ['wings', { c: '#fff0a0', s: 2, t0: .3 }], ['godray', { c: '#fff6c0', t0: .15 }], ['bigring', { c: '#ffe27a', t0: .4, s: 1 }]], G);
  add('knight.정의의 칼날', [['dim', { a: .45 }], ['giant', { k: 'sword', t1: .5 }], ['cross', { c: '#9ad0ff', n: 2, s: 2, w: 5, t0: .42, seed: 4 }], ['pillar', { c: '#9ad0ff', c2: '#fff', w: 22, h: 150, t0: .4 }], ['bigring', { c: '#9ad0ff', t0: .42, s: 1 }], ['flash', { t0: .4, t1: .6, c: '#e8f6ff', a: .7 }]], G);
  add('knight.수호의 서약', [['dim', { a: .4 }], ['rune', { c: '#ffd866', c2: '#fff', s: 2.2 }], ['dome', { c: '#ffe27a', c2: '#fff', s: 1.8, t0: .25 }], ['pillar', { c: '#ffe27a', w: 14, h: 130, t0: .15 }], ['sparkle', { c: '#fff', n: 22, t0: .2 }], ['bigring', { c: '#ffd866', t0: .35, s: .9 }]], G);
  add('gadget.철갑 멧돼지', [['dim', { a: .45 }], ['rune', { c: '#cfd6e0', c2: '#ffb040', s: 2 }], ['ground', { c: '#cfd6e0', c2: '#ffb040', s: 1.6, t0: .3 }], ['crack', { c: '#cfd6e0', c2: '#ffb040', t0: .3 }], ['dome', { c: '#8a95a8', c2: '#fff', s: 1.4, t0: .45 }], ['meteors', { c: '#8a95a8', c2: '#2a2a2a', n: 3, t0: .2 }], ['bigring', { c: '#ffb040', t0: .4, s: 1 }]], G);

  // ----- 그리기 -----
  function draw(g, f, x, y, now, key, meta){
    const p = (now - f.t0) / f.dur; if (p < 0) return true; if (p >= 1) return false;
    const R = (a, b, w, h, col, al) => { g.globalAlpha = Math.max(0, Math.min(1, al ?? 1)); g.fillStyle = col; g.fillRect(Math.round(a), Math.round(b), w, h); g.globalAlpha = 1; };
    const rn = i => { const t = Math.sin(f.seed * 97 + i * 12.9898) * 43758.5453; return t - Math.floor(t); };
    const c = { g, x, y, cx: x, cy: y - 14, R, rn, first: !(f.n > 0), fade: q => 1 - q * q };
    c.plus = (a, b, col, al) => { R(a - 1, b, 3, 1, col, al); R(a, b - 1, 1, 3, col, al); };
    c.star = (a, b, col, al, s = 2) => { R(a - s, b, s * 2 + 1, 1, col, al); R(a, b - s, 1, s * 2 + 1, col, al); R(a - 1, b - 1, 3, 3, '#fff', al); };
    c.ring = (ox, oy, rx, ry, n, col, al, ph = 0, s = 2) => { for (let i = 0; i < n; i++){ const a = i * 2 * PI / n + ph; R(ox + K(a) * rx, oy + S(a) * ry, s, s, col, al); } };
    c.line = (x0, y0, x1, y1, col, al, s = 3, t = 1) => { const n = Math.max(2, Math.round(Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)) / 2)); for (let i = 0; i <= n * t; i++){ const q = i / n; R(x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, s, s, i > n * t - 3 ? '#fff' : col, al); } };
    c.shock = (r, col, al, ox = x, oy = y) => c.ring(ox, oy, r, r * .32, Math.max(10, Math.round(r / 2)), col, al, 0, 2);
    c.flash = (col, al) => { g.globalAlpha = Math.max(0, Math.min(1, al)); g.fillStyle = col; g.fillRect(0, 0, 384, 216); g.globalAlpha = 1; };
    meta.layers.forEach(([m, o]) => { const t0 = o.t0 || 0, t1 = o.t1 || 1, q = (p - t0) / (t1 - t0); if (q < 0 || q > 1) return; const fn = LIB[m]; if (fn) fn(c, q, o); });
    return true;
  }
  Object.keys(T).forEach(k => { X.SK[k] = { dur: T[k].d, grand: T[k].g, once: T[k].once, v2: 1 }; });
  const base = X.drawSk;
  X.drawSk = (g, f, x, y, now) => { const key = f.k.slice(3), m = T[key]; return m ? draw(g, f, x, y, now, key, m) : base(g, f, x, y, now); };
  X.T2 = T;
})();
