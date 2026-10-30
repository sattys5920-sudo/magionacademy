// 시안: 실제 맵 위에서 정령불 사역마가 플레이어 뒤를 따라다니는 모습 (world.js 의 World.__cam 손잡이가 필요해요)
(function(){
const SPR = new Image(); SPR.src = 'wisps3_anim.png';   // 세로 = 정령 12종, 가로 = 일렁임 8칸
const cv = document.getElementById('cv'), ov = document.createElement('canvas'), g = ov.getContext('2d');
ov.style.cssText = 'position:fixed;pointer-events:none;z-index:5;image-rendering:pixelated'; document.body.appendChild(ov);
const bub = document.createElement('div');
bub.style.cssText = 'position:fixed;z-index:6;pointer-events:none;transform:translate(-50%,-100%);max-width:190px;padding:6px 10px;font:14px/18px G11,Pretendard,sans-serif;color:#F4EEFF;text-align:center;word-break:keep-all;background:rgba(14,10,30,.82);border:1px solid var(--wc,#7AA8FF);box-shadow:0 0 10px var(--wc,#7AA8FF),inset 0 0 8px rgba(120,160,255,.25);border-radius:10px;opacity:0;transition:opacity .4s';
document.body.appendChild(bub);
const W = window.__wisp = { i: 0, col: '#6A9CFF', say: null, trail: [], pos: null, sparks: [], t0: performance.now() };
W.setSay = (t, c) => { W.say = t; bub.textContent = t || ''; bub.style.opacity = t ? 1 : 0; if (c) bub.style.setProperty('--wc', c); };
function frame(now){
  requestAnimationFrame(frame);
  const r = cv.getBoundingClientRect(); if (!r.width || !window.World || !World.__cam || !World.meAt || !World.meAt()) return;
  if (ov.width !== cv.width || ov.height !== cv.height){ ov.width = cv.width; ov.height = cv.height; }
  Object.assign(ov.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' });
  const [cx, cy, K] = World.__cam, me = World.meAt(), hx = me.x, hy = me.y + 6;   // 머리 높이쯤
  W.trail.push([now, hx, hy]); while (W.trail.length > 2 && W.trail[1][0] < now - 700) W.trail.shift();
  const old = W.trail[0], mv = Math.hypot(hx - old[1], hy - old[2]) > 3;
  // 목표: 0.5초 전 자리에서 살짝 옆·위 (멈추면 어깨 뒤에서 천천히 맴돌기)
  const side = mv ? Math.sign(old[1] - hx || 1) : 1, idleA = (now - W.t0) / 1400;
  const tx = mv ? old[1] + side * 6 : hx + 11 * Math.cos(idleA) , ty = mv ? old[2] - 6 : hy - 8 + 2 * Math.sin(idleA * 2);
  if (!W.pos) W.pos = [tx, ty]; W.pos[0] += (tx - W.pos[0]) * .06; W.pos[1] += (ty - W.pos[1]) * .06;
  const bob = Math.sin(now / 420) * 1.6, wx = W.pos[0], wy = W.pos[1] + bob;
  if (Math.random() < (mv ? .5 : .15)) W.sparks.push({ x: wx + (Math.random() - .5) * 4, y: wy + 2, vx: (Math.random() - .5) * .1, vy: -.12 - Math.random() * .1, t: now, life: 700 + Math.random() * 600 });
  g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, ov.width, ov.height); g.imageSmoothingEnabled = false;
  const S = (x, y) => [(x - cx) * K, (y - cy) * K];
  // 땅에 비치는 빛
  const [gx, gy] = S(wx, hy + 20), pulse = .8 + .2 * Math.sin(now / 300);
  g.globalCompositeOperation = 'lighter';
  let rg = g.createRadialGradient(gx, gy, 0, gx, gy, 14 * K); rg.addColorStop(0, W.col + '60'); rg.addColorStop(1, W.col + '00');
  g.save(); g.translate(gx, gy); g.scale(1, .4); g.translate(-gx, -gy); g.fillStyle = rg; g.beginPath(); g.arc(gx, gy, 14 * K, 0, 7); g.fill(); g.restore();
  // 몸 둘레 빛
  const [sx, sy] = S(wx, wy); rg = g.createRadialGradient(sx, sy, 0, sx, sy, 11 * K * pulse); rg.addColorStop(0, W.col + '80'); rg.addColorStop(1, W.col + '00'); g.fillStyle = rg; g.beginPath(); g.arc(sx, sy, 11 * K, 0, 7); g.fill();
  // 남는 불티
  W.sparks = W.sparks.filter(p => now - p.t < p.life);
  for (const p of W.sparks){ const a = 1 - (now - p.t) / p.life, dt = now - p.t, [px, py] = S(p.x + p.vx * dt, p.y + p.vy * dt); g.fillStyle = W.col; g.globalAlpha = a; g.fillRect(Math.round(px), Math.round(py), Math.max(1, Math.round(K)), Math.max(1, Math.round(K))); }
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  // 정령불 본체 (64칸 → 세계 30픽셀, 살짝 일렁이게 세로로 늘었다 줄었다)
  if (SPR.complete){ const sz = 17 * K, st = 1 + .05 * Math.sin(now / 160); const fi = Math.floor(now / 110) % 8; g.drawImage(SPR, fi * 64, W.i * 64, 64, 64, Math.round(sx - sz / 2), Math.round(sy - sz * .62 * st), Math.round(sz), Math.round(sz * st)); }
  if (W.say){ const s = cv.getBoundingClientRect().width / cv.width; bub.style.left = r.left + sx * s + 'px'; bub.style.top = r.top + (sy - 12 * K) * s + 'px'; }
}
requestAnimationFrame(frame);
})();
