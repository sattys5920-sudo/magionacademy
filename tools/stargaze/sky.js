// 별 보는 밤 · 하늘 화면 그리기 (시안용, 게임에 붙일 때 그대로 가져가요)
//   skyDraw(g, W, H, C, S)  C: 별자리 데이터 · S: { lit:[별 id], own:{별 id: 이름}, drawn: 이어진 선 수(소수면 그리는 중), outline: 0~1, title: 0~1, t: 초, names: 이름표를 보일지 }
const SKY = (() => {
  const rnd = seed => () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
  const px = (g, x, y, w, h, c) => { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), w, h); };
  function box(W, H){ const bw = Math.min(W - 56, 1000), bh = Math.min(H * .46, bw * .86); return { x: (W - bw) / 2, y: Math.max(150, H * .17), w: bw, h: bh }; }
  const pos = (B, s) => [B.x + s.x / 100 * B.w, B.y + s.y / 60 * B.h];
  function background(g, W, H, t){
    const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#060B22'); gr.addColorStop(.55, '#142257'); gr.addColorStop(.85, '#2C3B7E'); gr.addColorStop(1, '#3A4686'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    const r = rnd(7), U = W < 700 ? 2 : 3;
    for (let i = 0; i < 150; i++){ const x = r() * W, y = r() * H * .78, a = .2 + r() * .5, big = r() < .12, tw = .5 + .5 * Math.sin(t * (1 + r() * 2) + i); g.globalAlpha = a * (.6 + .4 * tw); px(g, x, y, big ? U : 1, big ? U : 1, '#C9D6FF'); if (big){ px(g, x - 1, y + U / 2 - .5, U + 2, 1, '#C9D6FF'); } }
    g.globalAlpha = 1;
  }
  function horizon(g, W, H){
    const U = W < 700 ? 4 : 6, base = H - Math.round(H * .17);
    g.fillStyle = '#0A0F26'; for (let x = 0; x < W; x += U){ const h = Math.round((Math.sin(x / W * 5.1 + 1) * .5 + Math.sin(x / W * 11) * .2) * 18 / U) * U; g.fillRect(x, base - h - 10, U, H - base + h + 10); }
    // 학교 실루엣: 본관 + 탑 두 개 (계단식 지붕), 불 켜진 창
    const cx = W * .72, by = base - 30; g.fillStyle = '#070B1D';
    g.fillRect(cx - 62, by - 26, 124, 40);
    for (let k = 0; k < 6; k++) g.fillRect(cx - 62 + k * 5, by - 26 - (k + 1) * 4, 124 - k * 10, 4);
    g.fillRect(cx - 80, by - 66, 18, 80); for (let k = 0; k < 4; k++) g.fillRect(cx - 80 + k * 2, by - 66 - (k + 1) * 4, 18 - k * 4, 4);
    g.fillRect(cx + 62, by - 52, 16, 66); for (let k = 0; k < 4; k++) g.fillRect(cx + 62 + k * 2, by - 52 - (k + 1) * 4, 16 - k * 4, 4);
    const r = rnd(3); for (let i = 0; i < 14; i++) px(g, cx - 56 + i * 8 + (i % 2) * 2, by - 14 + (i % 3) * 8, 3, 4, r() < .7 ? '#F6B24C' : '#8A5A24');
    px(g, cx - 75, by - 50, 3, 5, '#F6B24C'); px(g, cx + 67, by - 36, 3, 5, '#F6B24C');
    // 언덕 위 작은 사람들 (참가자)
    for (let i = 0; i < 9; i++){ const x = W * .08 + i * (W * .056), y = base - 6 + (i % 2) * 5; px(g, x, y - 7, 4, 4, '#04060F'); px(g, x - 1, y - 3, 6, 6, '#04060F'); }
  }
  // 별자리 그림 윤곽 (얇은 선화) — 별 좌표 기준으로 그려요
  const OUT = {
    pumpkin_cart(g, P){ g.beginPath(); g.ellipse(...P(51, 21), P.w(15), P.h(11), 0, 0, 7); g.moveTo(...P(51, 10)); g.quadraticCurveTo(...P(44, 21), ...P(51, 32)); g.moveTo(...P(51, 10)); g.quadraticCurveTo(...P(58, 21), ...P(51, 32)); g.moveTo(...P(51, 10)); g.lineTo(...P(50, 4)); g.lineTo(...P(53, 3)); g.moveTo(...P(28, 38)); g.lineTo(...P(74, 38)); g.lineTo(...P(70, 44)); g.lineTo(...P(32, 44)); g.closePath(); g.moveTo(...P(41.5, 49)); g.arc(...P(36, 49), P.w(5.5), 0, 7); g.moveTo(...P(71.5, 49)); g.arc(...P(66, 49), P.w(5.5), 0, 7); g.moveTo(...P(74, 38)); g.lineTo(...P(92, 25)); },
    witch_broom(g, P){ g.beginPath(); g.moveTo(...P(14, 52)); g.lineTo(...P(63, 20)); g.moveTo(...P(15, 48)); g.lineTo(...P(61, 16)); g.moveTo(...P(63, 18)); [[70, 6], [79, 10], [82, 20], [75, 27]].forEach(([x, y]) => { g.moveTo(...P(63, 18)); g.quadraticCurveTo(...P((63 + x) / 2 + 2, (18 + y) / 2 - 2), ...P(x, y)); }); g.moveTo(...P(70, 6)); g.quadraticCurveTo(...P(82, 6), ...P(79, 10)); g.moveTo(...P(82, 20)); g.quadraticCurveTo(...P(82, 26), ...P(75, 27)); [[8, 40], [4, 30], [10, 33], [3, 44]].forEach(([x, y]) => { g.moveTo(...P(x + 2, y)); g.lineTo(...P(x, y - 2)); g.lineTo(...P(x - 2, y)); g.lineTo(...P(x, y + 2)); g.closePath(); }); },
    sleepy_owl(g, P){ g.beginPath(); g.moveTo(...P(30, 22)); g.lineTo(...P(34, 8)); g.lineTo(...P(50, 14)); g.lineTo(...P(66, 8)); g.lineTo(...P(70, 22)); g.quadraticCurveTo(...P(74, 46), ...P(66, 52)); g.quadraticCurveTo(...P(50, 60), ...P(34, 52)); g.quadraticCurveTo(...P(26, 46), ...P(30, 22)); g.moveTo(...P(47, 24)); g.arc(...P(42, 24), P.w(5), 0, 7); g.moveTo(...P(63, 24)); g.arc(...P(58, 24), P.w(5), 0, 7); g.moveTo(...P(47, 29)); g.lineTo(...P(50, 34)); g.lineTo(...P(53, 29)); g.moveTo(...P(44, 56)); g.lineTo(...P(41, 59)); g.moveTo(...P(44, 56)); g.lineTo(...P(47, 59)); g.moveTo(...P(56, 56)); g.lineTo(...P(53, 59)); g.moveTo(...P(56, 56)); g.lineTo(...P(59, 59)); },
    bell_cat(g, P){ g.beginPath(); g.moveTo(...P(26, 20)); g.lineTo(...P(30, 8)); g.lineTo(...P(37, 14)); g.lineTo(...P(44, 8)); g.lineTo(...P(48, 20)); g.quadraticCurveTo(...P(49, 29), ...P(37, 30)); g.quadraticCurveTo(...P(25, 29), ...P(26, 20)); g.moveTo(...P(40, 34)); g.arc(...P(37, 34), P.w(3), 0, 7); g.moveTo(...P(34, 31)); g.quadraticCurveTo(...P(20, 42), ...P(28, 52)); g.lineTo(...P(60, 52)); g.quadraticCurveTo(...P(66, 40), ...P(58, 30)); g.moveTo(...P(58, 30)); g.quadraticCurveTo(...P(76, 34), ...P(72, 24)); g.quadraticCurveTo(...P(70, 12), ...P(80, 12)); g.moveTo(...P(33, 20)); g.lineTo(...P(34, 20)); g.moveTo(...P(41, 20)); g.lineTo(...P(42, 20)); },
    twelve_friends(g, P, C){ g.beginPath(); C.stars.forEach((s, i) => { const n = C.stars[(i + 1) % 12]; g.moveTo(...P(s.x + 2.2, s.y - 3)); g.arc(...P(s.x, s.y - 3), P.w(2.2), 0, 7); g.moveTo(...P(s.x - 2.5, s.y + 5)); g.quadraticCurveTo(...P(s.x, s.y - .5), ...P(s.x + 2.5, s.y + 5)); g.moveTo(...P(s.x + 1.5, s.y + .5)); g.quadraticCurveTo(...P((s.x + n.x) / 2, (s.y + n.y) / 2 + 2), ...P(n.x - 1.5, n.y + .5)); }); },
  };
  function draw(g, W, H, C, S){
    const t = S.t || 0, B = box(W, H), U = W < 700 ? 3 : 4, byId = Object.fromEntries(C.stars.map(s => [s.id, s]));
    g.clearRect(0, 0, W, H); background(g, W, H, t); horizon(g, W, H);
    if (S.outline > 0){ const P = (x, y) => [B.x + x / 100 * B.w, B.y + y / 60 * B.h]; P.w = v => v / 100 * B.w; P.h = v => v / 60 * B.h;
      g.save(); g.globalAlpha = .34 * S.outline; g.strokeStyle = '#E6EEFF'; g.lineWidth = 2; g.lineJoin = 'round'; g.setLineDash([]); OUT[C.id](g, P, C); g.stroke(); g.restore(); }
    // 선 (순서대로, 앞 별에서 뒤 별로 뻗어 나가요)
    const n = S.drawn || 0; let head = null;
    C.order.forEach((e, i) => { const k = Math.max(0, Math.min(1, n - i)); if (k <= 0) return; const a = pos(B, byId[e[0]]), b = pos(B, byId[e[1]]), x = a[0] + (b[0] - a[0]) * k, y = a[1] + (b[1] - a[1]) * k;
      g.save(); g.lineCap = 'round'; g.strokeStyle = 'rgba(255,241,193,.28)'; g.lineWidth = 7; g.beginPath(); g.moveTo(...a); g.lineTo(x, y); g.stroke(); g.strokeStyle = '#FFF1C1'; g.lineWidth = 2; g.stroke(); g.restore(); if (k < 1) head = [x, y]; });
    const lit = new Set(S.lit || []);
    C.stars.forEach(s => { const [x, y] = pos(B, s), L = lit.has(s.id), r = s.mag, arm = r + 0, tw = L ? .8 + .2 * Math.sin(t * 2.4 + x) : 1, col = L ? '#FFF6D0' : '#7C8BBA';
      if (L){ const gr = g.createRadialGradient(x, y, 0, x, y, (8 + r * 5) * U / 2); gr.addColorStop(0, `rgba(255,236,170,${.55 * tw})`); gr.addColorStop(1, 'rgba(255,236,170,0)'); g.fillStyle = gr; g.fillRect(x - 40, y - 40, 80, 80); }
      else { g.globalAlpha = .55 + .35 * Math.sin(t * 3 + x); }
      px(g, x - U / 2, y - U / 2, U, U, col); for (let k = 1; k <= arm; k++){ px(g, x - U / 2 + k * U, y - U / 2, U, U, col); px(g, x - U / 2 - k * U, y - U / 2, U, U, col); px(g, x - U / 2, y - U / 2 + k * U, U, U, col); px(g, x - U / 2, y - U / 2 - k * U, U, U, col); }
      g.globalAlpha = 1;
      if (S.names && S.own && S.own[s.id]){ g.font = (W < 700 ? '11' : '14') + 'px G11, Pretendard, sans-serif'; g.textAlign = 'center'; const tx = S.own[s.id], w = g.measureText(tx).width + 10, ty = y + (arm + 1) * U + 6, hot = S.hot && S.hot.includes(s.id);
        g.fillStyle = hot ? 'rgba(255,241,193,.9)' : 'rgba(10,14,40,.62)'; g.fillRect(Math.round(x - w / 2), Math.round(ty), Math.round(w), W < 700 ? 16 : 20); g.fillStyle = hot ? '#1A1A3A' : L ? '#FFF1C1' : '#9FB0E0'; g.fillText(tx, x, ty + (W < 700 ? 12 : 15)); } });
    if (head){ for (let i = 0; i < 6; i++){ const a = i * 1.1 + t * 6; g.fillStyle = 'rgba(255,241,193,.8)'; g.fillRect(Math.round(head[0] + Math.cos(a) * 7), Math.round(head[1] + Math.sin(a) * 7), 2, 2); } }
    if (S.title > 0){ g.save(); g.globalAlpha = S.title; g.textAlign = 'center'; g.font = `${W < 700 ? 28 : 42}px G11B, Pretendard, sans-serif`; g.shadowColor = 'rgba(255,220,130,.85)'; g.shadowBlur = 18; g.fillStyle = '#FFF1C1'; g.fillText(C.name, W / 2, B.y + B.h + (W < 700 ? 52 : 70)); g.restore(); }
  }
  return { draw, box, pos };
})();
if (typeof module !== 'undefined') module.exports = SKY;
