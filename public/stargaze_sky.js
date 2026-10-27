// 별 보는 밤 · 하늘 화면 그리기 (시안용, 게임에 붙일 때 그대로 가져가요)
//   STARSKY.draw(g, W, H, C, S)  C: 별자리 데이터 · S: { lit:[별 id], own:{별 id: 이름}, drawn: 이어진 선 수(소수면 그리는 중), outline: 0~1, title: 0~1, t: 초, names: 이름표를 보일지 }
const STARSKY = (() => {
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
  // 아래 풍경: 도트 그림(art/stargaze_horizon_390·720.png, tools/stargaze/horizon.py)을 정수 배로 키워 찍어요
  function horizon(g, W, H, img){
    if (!img || !img.complete || !img.naturalWidth) return;
    const sc = Math.max(1, Math.floor(W / img.naturalWidth)), dw = img.naturalWidth * sc, dh = img.naturalHeight * sc, x0 = Math.round((W - dw) / 2), y0 = H - dh;
    g.imageSmoothingEnabled = false; g.fillStyle = '#0C0F28'; g.fillRect(0, H - 14 * sc, W, 14 * sc); g.fillStyle = '#131840'; g.fillRect(0, H - 30 * sc, x0, 16 * sc); g.fillRect(x0 + dw, H - 30 * sc, W - x0 - dw, 16 * sc);
    g.drawImage(img, x0, y0, dw, dh);
  }

  // 언덕에 선 학생들: 플레이어가 만든 캐릭터를 열 맞춰 세워요 (하늘을 보느라 뒷모습). 자기 별을 켠 학생은 손을 들고 흔들어요
  //   S.crowd = [{ img: 걷기 그림줄(64칸 × 20), lit: 자기 별을 켰는지, mag: 맡은 별 밝기 }]
  function skinOf(g2, img){ const c = document.createElement('canvas'); c.width = c.height = 64; const q = c.getContext('2d'); q.drawImage(img, 0, 0, 64, 64, 0, 0, 64, 64); const d = q.getImageData(29, 27, 6, 3).data, px = []; for (let i = 0; i < d.length; i += 4) px.push([d[i], d[i + 1], d[i + 2]]); px.sort((a, b) => (a[0] + a[1] + a[2]) - (b[0] + b[1] + b[2])); return px[px.length >> 1]; }
  function person(img, lit, t, k){
    const c = document.createElement('canvas'); c.width = c.height = 64; const q = c.getContext('2d'); q.drawImage(img, 5 * 64, 0, 64, 64, 0, 0, 64, 64);
    if (lit){ const sk = skinOf(null, img), slv = q.getImageData(36, 33, 1, 1).data, w = Math.round(Math.sin(t * 5 + k) * 1.2);
      const sl = `rgb(${slv[0]},${slv[1]},${slv[2]})`, kn = `rgb(${sk[0]},${sk[1]},${sk[2]})`, hx = 43 + w;   // 어깨에서 위로 쭉 뻗은 팔 + 손 (흔들흔들)
      const line = (x0, y0, x1, y1, col, th) => { const n = y0 - y1; for (let i = 0; i <= n; i++){ const x = Math.round(x0 + (x1 - x0) * i / n); q.fillStyle = col; q.fillRect(x, y0 - i, th, 1); } };
      line(37, 33, hx - 1, 11, 'rgba(30,16,20,.7)', 4); line(38, 33, hx, 11, kn, 2); line(38, 33, 40, 26, sl, 2);
      q.fillStyle = 'rgba(30,16,20,.7)'; q.fillRect(hx - 2, 5, 5, 6); q.fillStyle = kn; q.fillRect(hx - 1, 6, 3, 4); q.fillStyle = 'rgba(255,255,255,.3)'; q.fillRect(hx - 1, 6, 1, 2); }
    return c;
  }
  function crowd(g, W, H, S, t){
    const L = S.crowd || []; if (!L.length) return; const sc = W < 700 ? 1 : 2, n = L.length, gap = Math.min(W < 700 ? 34 : 70, (W - 28) / n), x0 = W / 2 - (n - 1) / 2 * gap, base = H - (W < 700 ? 40 : 72), U = W < 700 ? 2 : 3;
    g.imageSmoothingEnabled = false;
    L.forEach((p, i) => { const x = Math.round(x0 + i * gap), cv = person(p.img, p.lit, t, i), y = base - 56 * sc;
      g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(x - 11 * sc, base - 1, 22 * sc, 3 * sc);
      g.drawImage(cv, x - 32 * sc, y, 64 * sc, 64 * sc);
      const sx = x, sy = y + 4 * sc - 14, col = p.lit ? '#FFF6D0' : '#6C7AA8';   // 머리 위에 맡은 별
      g.globalAlpha = p.lit ? 1 : .6; g.fillStyle = col; g.fillRect(sx - U / 2, sy - U / 2, U, U); for (let k = 1; k <= (p.mag || 1); k++){ g.fillRect(sx - U / 2 + k * U, sy - U / 2, U, U); g.fillRect(sx - U / 2 - k * U, sy - U / 2, U, U); g.fillRect(sx - U / 2, sy - U / 2 + k * U, U, U); g.fillRect(sx - U / 2, sy - U / 2 - k * U, U, U); } g.globalAlpha = 1; });
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
    g.clearRect(0, 0, W, H); background(g, W, H, t); horizon(g, W, H, S.horizon);
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
      if (!L && S.mine && S.mine.includes(s.id)){ g.save(); g.globalAlpha = .9; g.strokeStyle = '#FFF1C1'; g.lineWidth = 2; g.beginPath(); g.arc(x, y, 14 + 3 * Math.sin(t * 5), 0, 7); g.stroke(); g.restore(); }
      px(g, x - U / 2, y - U / 2, U, U, col); for (let k = 1; k <= arm; k++){ px(g, x - U / 2 + k * U, y - U / 2, U, U, col); px(g, x - U / 2 - k * U, y - U / 2, U, U, col); px(g, x - U / 2, y - U / 2 + k * U, U, U, col); px(g, x - U / 2, y - U / 2 - k * U, U, U, col); }
      g.globalAlpha = 1;
    });
    crowd(g, W, H, S, t);
    if (head){ for (let i = 0; i < 6; i++){ const a = i * 1.1 + t * 6; g.fillStyle = 'rgba(255,241,193,.8)'; g.fillRect(Math.round(head[0] + Math.cos(a) * 7), Math.round(head[1] + Math.sin(a) * 7), 2, 2); } }
    if (S.title > 0){ g.save(); g.globalAlpha = S.title; g.textAlign = 'center'; g.font = `${W < 700 ? 28 : 42}px G11B, Pretendard, sans-serif`; g.shadowColor = 'rgba(255,220,130,.85)'; g.shadowBlur = 18; g.fillStyle = '#FFF1C1'; g.fillText(C.name, W / 2, B.y + B.h + (W < 700 ? 52 : 70)); g.restore(); }
  }
  return { draw, box, pos };
})();
if (typeof module !== 'undefined') module.exports = STARSKY;
