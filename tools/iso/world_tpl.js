
// 걸어 다니는 세계 (tools/iso/build_halloween.py가 MAPS를 채워서 public/world.js로 써요)
// 게임(index.html)과는 window.World로 이어져요: World.start / setPlayer / teleport / onAct
const MAPS = __MAPS__;
const World = window.World = { onAct: null, onMove: null };
// ---------- 캐릭터 조합 (tools/iso/chars4.py 부품) ----------
// av = { eyes, hair, hat, top, bottom, shoes, acc: 부품 번호, skinC, eyeC, hairC, topC, bottomC, shoesC, hatC, accC: 색 번호 }
const AVM = __AVATAR__;
World.Avatar = (() => {
  const FW = AVM.fw, FH = AVM.fh, CATS = ['eyes', 'hair', 'hat', 'top', 'bottom', 'shoes', 'acc'];
  const COLOR = { skin: 'skinC', eye: 'eyeC', hair: 'hairC', top: 'topC', bottom: 'bottomC', shoes: 'shoesC', hat: 'hatC', acc: 'accC' };
  const palOf = slot => AVM.pal[slot] || AVM.pal.cloth;
  const KEY = { 240: 0, 200: 1, 150: 2, 100: 3 };
  let data = null; const cache = new Map(), heads = new Map();
  const ready = new Promise(r => { const i = new Image(); i.onload = () => { const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0); data = g.getImageData(0, 0, i.width, i.height); r(); }; i.src = AVM.src; });
  const rgb = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const ramps = {}; const rampOf = (slot, n) => { const p = palOf(slot), k = slot + (n % p.length); return ramps[k] || (ramps[k] = p[n % p.length].map(rgb)); };
  const rnd = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647);
  function fix(av){
    const a = Object.assign({}, av || {});
    CATS.forEach(c => { const n = AVM.parts[c].length; a[c] = ((a[c] | 0) % n + n) % n; });
    Object.values(COLOR).forEach(k => { a[k] = Math.max(0, a[k] | 0); });
    return a;
  }
  // 옛 캐릭터(look 번호)는 그 번호로 정해진 조합을 줘요
  function fromLook(look){
    const r = rnd(((look | 0) + 7) * 9973 + 1), pick = n => Math.floor(r() * n), a = {};
    CATS.forEach(c => { a[c] = pick(AVM.parts[c].length); });
    if (r() < .5) a.hat = 0; if (r() < .5) a.acc = 0;
    a.skinC = pick(4); a.eyeC = pick(AVM.pal.eye.length); a.hairC = pick(AVM.pal.hair.length);
    ['topC', 'bottomC', 'shoesC', 'hatC', 'accC'].forEach(k => { a[k] = pick(AVM.pal.cloth.length); });
    return a;
  }
  const random = () => fromLook(Math.floor(Math.random() * 1e6));
  function compose(av){
    av = fix(av); const key = JSON.stringify(av); if (cache.has(key)) return cache.get(key);
    const W = FW * 6, out = new ImageData(W, FH), o = out.data, src = data.data, SW = data.width;
    const P = { body: AVM.parts.body[0] }; CATS.forEach(c => { P[c] = AVM.parts[c][av[c]]; });
    const hide = new Set(); Object.values(P).forEach(p => (p.hide || []).forEach(h => hide.add(h)));
    const layers = [];
    ['hair', 'acc', 'hat'].forEach(c => P[c].u !== undefined && layers.push([P[c].u, P[c].slot]));
    ['body', 'bottom', 'shoes', 'top', 'eyes'].forEach(c => { if (hide.has(c)) return; ['u', 'o'].forEach(k => P[c][k] !== undefined && layers.push([P[c][k], P[c].slot])); });
    ['acc', 'hair', 'hat'].forEach(c => P[c].o !== undefined && layers.push([P[c].o, P[c].slot]));
    layers.forEach(([row, slot]) => {
      const ramp = slot ? rampOf(slot, av[COLOR[slot]]) : null;
      for (let y = 0; y < FH; y++) for (let x = 0; x < W; x++){
        const s = ((row * FH + y) * SW + x) * 4; if (!src[s + 3]) continue;
        const d = (y * W + x) * 4, r = src[s], g = src[s + 1], b = src[s + 2], k = r === g && g === b ? KEY[r] : undefined;
        if (ramp && k !== undefined){ const c = ramp[k]; o[d] = c[0]; o[d + 1] = c[1]; o[d + 2] = c[2]; } else { o[d] = r; o[d + 1] = g; o[d + 2] = b; }
        o[d + 3] = 255;
      }
    });
    // 바깥 테두리
    const edge = [];
    for (let y = 0; y < FH; y++) for (let x = 0; x < W; x++){
      if (o[(y * W + x) * 4 + 3]) continue; const fx = x % FW;
      if ((fx > 0 && o[(y * W + x - 1) * 4 + 3]) || (fx < FW - 1 && o[(y * W + x + 1) * 4 + 3]) || (y > 0 && o[((y - 1) * W + x) * 4 + 3]) || (y < FH - 1 && o[((y + 1) * W + x) * 4 + 3])) edge.push((y * W + x) * 4);
    }
    edge.forEach(d => { o[d] = 42; o[d + 1] = 24; o[d + 2] = 48; o[d + 3] = 255; });
    const c = document.createElement('canvas'); c.width = W; c.height = FH; c.getContext('2d').putImageData(out, 0, 0);
    cache.set(key, c); return c;
  }
  // 얼굴 동그라미용 (첫 프레임 윗부분)
  function head(av){
    if (!data) return '';
    const key = JSON.stringify(fix(av)); if (heads.has(key)) return heads.get(key);
    const c = document.createElement('canvas'); c.width = FW; c.height = FW; c.getContext('2d').drawImage(compose(av), 0, 1, FW, FW, 0, 0, FW, FW);
    const u = c.toDataURL(); heads.set(key, u); return u;
  }
  return { ready, compose, head, fix, fromLook, random, meta: AVM, FW, FH, CATS, COLOR, palOf, get loaded(){ return !!data; } };
})();
let sc;
// 배율: 그림 1픽셀 = 화면 실제 픽셀의 정수배(k)로 그려서 선명하게. 목표 가로 픽셀 수에 가장 가까운 k를 골라요.
const ZOOMS = [['보통', 300], ['멀리', 420], ['가까이', 210]];
let zi = 0, VW = 300, KPX = 1;
const cv = document.getElementById('cv'), out = cv.getContext('2d');
const world = document.getElementById('world'), fadeEl = document.getElementById('fade');
let VH = 220;
function resize(){
  const dpr = window.devicePixelRatio || 1, dw = world.clientWidth * dpr, dh = world.clientHeight * dpr;
  const target = (M && M.vw && zi !== 1) ? M.vw : ZOOMS[zi][1];
  KPX = Math.max(1, Math.round(dw / target));
  VW = Math.ceil(dw / KPX); VH = Math.ceil(dh / KPX);
  cv.width = VW; cv.height = VH;
  cv.style.width = (VW * KPX / dpr) + 'px'; cv.style.height = (VH * KPX / dpr) + 'px';
  out.imageSmoothingEnabled = false;
}
addEventListener('resize', resize);
const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = s; });
let map, M, blocked, objOrder;
const P = (tx, ty) => [M.OX + (tx - ty) * 8, M.OY + (tx + ty) * 4];
const free = (x, y) => x >= 0 && y >= 0 && x < M.NX && y < M.NY && !blocked.has(x + ',' + y);
function path(sx, sy, gx, gy){
  if (!free(gx, gy)) return null;
  const prev = new Map([[sx + ',' + sy, null]]), q = [[sx, sy]];
  for (let i = 0; i < q.length; i++){
    const [x, y] = q[i]; if (x === gx && y === gy) break;
    for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const k = (x + dx) + ',' + (y + dy); if (free(x + dx, y + dy) && !prev.has(k)){ prev.set(k, [x, y]); q.push([x + dx, y + dy]); } }
  }
  if (!prev.has(gx + ',' + gy)) return null;
  const r = []; let c = [gx, gy]; while (c && !(c[0] === sx && c[1] === sy)){ r.unshift(c); c = prev.get(c[0] + ',' + c[1]); } return r;
}
// a가 b보다 뒤(먼저 그림)인가: 발판 상자로 판단
const behind = (a, b) => (a[2] <= b[0] && a[1] < b[3] && b[1] < a[3]) || (a[3] <= b[1] && a[0] < b[2] && b[0] < a[2]) || ((a[2] <= b[0] || a[3] <= b[1]) && !(b[2] <= a[0] || b[3] <= a[1]));
const sOver = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
function orderObjs(objs){   // 한 번만: 겹치는 것끼리 위상 정렬
  const n = objs.length, after = objs.map(() => []), indeg = new Array(n).fill(0);
  const R = o => ({ x: o.x, y: o.y, w: o.sw, h: o.sh });
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if (i !== j && sOver(R(objs[i]), R(objs[j])) && behind(objs[i].box, objs[j].box)){ after[i].push(j); indeg[j]++; }
  const key = o => o.box[2] + o.box[3];
  const ready = objs.map((o, i) => i).filter(i => !indeg[i]), outL = [];
  while (ready.length){ ready.sort((a, b) => key(objs[b]) - key(objs[a])); const i = ready.pop(); outL.push(i); after[i].forEach(j => { if (!--indeg[j]) ready.push(j); }); }
  objs.forEach((o, i) => { if (!outL.includes(i)) outL.push(i); });
  return outL.map(i => objs[i]);
}
const people = [];
const NAMES = ['루나', '블러드', '울피', '부우', '마리', '호박이', '라벤', '드라코', '미라', '젤리', '스푸키'];
const mk = (name, av, x, y, me) => ({ name, av, x, y, path: [], back: false, flip: false, me, t: 0, idle: Math.random() * 3 });
const me = mk('나', null, 0, 0, true);
let started = false;
let crowd = {};
function setMap(id, spawn){
  map = id; M = MAPS[id].meta; resize();
  blocked = new Set(); M.objs.forEach(o => { if (o.solid !== false) for (let x = Math.floor(o.box[0]); x < Math.ceil(o.box[2]); x++) for (let y = Math.floor(o.box[1]); y < Math.ceil(o.box[3]); y++) blocked.add(x + ',' + y); });
  objOrder = MAPS[id].order || (MAPS[id].order = orderObjs(M.objs));
  me.x = spawn[0]; me.y = spawn[1]; me.path = []; me.back = false; me.flip = false;
  if (!crowd[id]){ crowd[id] = []; const n = id === 'campus' ? 9 : 2; for (let i = 0; i < n; i++){ for (let k = 0; k < 50; k++){ const x = Math.floor(Math.random() * M.NX), y = Math.floor(Math.random() * M.NY); if (free(x, y)){ crowd[id].push(mk(NAMES[(i + (id === 'lab' ? 3 : 0)) % NAMES.length], World.Avatar.random(), x, y, false)); break; } } } }
  people.length = 0; people.push(me, ...crowd[id]);
  tags.forEach(t => t.remove()); tags = people.map(p => { const d = document.createElement('div'); d.className = 'ntag' + (p.me ? ' me' : ''); d.textContent = p.name; world.appendChild(d); return d; });
  document.getElementById('place').textContent = M.title; document.getElementById('sub').textContent = M.sub;
  camX = camY = null; hideBubble();
}
let tags = [], bubble = null, pending = null, busy = false, camX = null, camY = null, forceNight = null;
function showBubble(o, text, btn, fn){
  hideBubble();
  const b = document.createElement('div'); b.className = 'bubble'; b.innerHTML = text + (btn ? `<button>${btn}</button>` : '');
  if (btn) b.querySelector('button').onclick = e => { e.stopPropagation(); fn && fn(); };
  world.appendChild(b); bubble = { el: b, o };
}
function hideBubble(){ bubble?.el.remove(); bubble = null; }
const ACTS = {};
// 물건을 쓰면 게임에 물어봐요: 글을 돌려주면 말풍선에 보여 주고, 아니면 (화면이 열렸으니) 말풍선을 닫아요
function useObj(o, a){
  const r = World.onAct ? World.onAct(map, o, a) : null;
  if (typeof r === 'string' && bubble){ bubble.el.innerHTML = r; } else hideBubble();
}
function goDoor(door, o){
  if (!door.to){ showBubble(o, `<b>${door.label}</b><br>아직 문이 잠겨 있어요 · 곧 열려요`); return; }
  busy = true; fadeEl.textContent = door.label; fadeEl.style.opacity = 1;
  setTimeout(() => { setMap(door.to, door.spawn); setTimeout(() => { fadeEl.style.opacity = 0; busy = false; }, 150); }, 380);
}
function goto(p, gx, gy){ const r = path(Math.round(p.x), Math.round(p.y), gx, gy); if (r){ p.path = r; return true; } return false; }
function near(tiles){ const c = []; tiles.forEach(([a, b]) => [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx, dy]) => free(a + dx, b + dy) && c.push([a + dx, b + dy]))); return c.sort((p1, p2) => Math.hypot(p1[0] - me.x, p1[1] - me.y) - Math.hypot(p2[0] - me.x, p2[1] - me.y)); }
cv.addEventListener('pointerdown', e => {
  if (busy) return;
  const r = cv.getBoundingClientRect(), x = (e.clientX - r.left) * VW / r.width + Math.round(camX), y = (e.clientY - r.top) * VH / r.height + Math.round(camY);
  hideBubble(); pending = null;
  const hit = [...objOrder].reverse().find(o => (o.door || o.act || ACTS[o.name]) && x >= o.x && y >= o.y && x < o.x + o.sw && y < o.y + o.sh && (() => { const px = MAPS[map].px; const d = px.getImageData(o.sx + (x - o.x) | 0, o.sy + (y - o.y) | 0, 1, 1).data; return d[3] > 0; })());
  if (hit){
    if (hit.door){ const [dx, dy] = hit.door.tile; if (Math.round(me.x) === dx && Math.round(me.y) === dy) return goDoor(hit.door, hit); if (goto(me, dx, dy)) pending = { door: hit.door, o: hit }; return; }
    const tiles = []; for (let a = Math.floor(hit.box[0]); a < Math.ceil(hit.box[2]); a++) for (let b = Math.floor(hit.box[1]); b < Math.ceil(hit.box[3]); b++) tiles.push([a, b]);
    for (const c of near(tiles)) if (goto(me, c[0], c[1])){ pending = { act: hit }; return; }
    return;
  }
  const tx = Math.floor(((x - M.OX) / 8 + (y - M.OY) / 4) / 2), ty = Math.floor(((y - M.OY) / 4 - (x - M.OX) / 8) / 2);
  const door = M.objs.find(o => o.door && o.door.tile[0] === tx && o.door.tile[1] === ty);
  if (goto(me, tx, ty) && door) pending = { door: door.door, o: door };
});
const SPEED = 6.5, RUN = 10;   // 타일/초. 멀리 갈 때(남은 길 10칸 넘게)는 달려요
function step(p, dt){
  if (!p.path.length){
    if (p.me && pending){ const pd = pending; pending = null; if (pd.door) goDoor(pd.door, pd.o); else { const a = pd.act.act || ACTS[pd.act.name]; showBubble(pd.act, a[0], a[1], () => useObj(pd.act, a)); } }
    if (!p.me && (p.idle -= dt) < 0){ p.idle = 2 + Math.random() * 5; for (let i = 0; i < 20; i++){ const gx = Math.round(p.x) + Math.floor(Math.random() * 13) - 6, gy = Math.round(p.y) + Math.floor(Math.random() * 13) - 6; if (goto(p, gx, gy)) break; } }
    p.t = 0; return;
  }
  const [gx, gy] = p.path[0], dx = gx - p.x, dy = gy - p.y, d = Math.hypot(dx, dy);
  if (Math.abs(dx) > Math.abs(dy)){ p.back = dx < 0; p.flip = dx < 0; } else if (d > 0){ p.back = dy < 0; p.flip = dy > 0; }
  const mv = (p.me && p.path.length > 10 ? RUN : p.me ? SPEED : SPEED * .6) * dt; if (d <= mv){ p.x = gx; p.y = gy; p.path.shift(); } else { p.x += dx / d * mv; p.y += dy / d * mv; } p.t += dt;
}
// 할로윈 효과: 박쥐 떼, 보라 안개, 도깨비불
const bats = Array.from({ length: 7 }, (_, i) => ({ x: 0, y: 0, vx: 0, vy: 0, ph: i, init: false }));
const fogs = Array.from({ length: 6 }, (_, i) => ({ x: Math.random(), y: Math.random(), s: 60 + Math.random() * 50, v: 4 + Math.random() * 6 }));
const wisps = Array.from({ length: 10 }, () => ({ x: Math.random(), y: Math.random(), ph: Math.random() * 6 }));
function spooky(now, dt, view){
  const cx = out;
  bats.forEach(b => {
    if (!b.init || b.x < view.x - 40 || b.x > view.x + view.w + 40 || b.y < view.y - 40 || b.y > view.y + view.h + 40){
      const left = Math.random() < .5; b.x = left ? view.x - 20 : view.x + view.w + 20; b.y = view.y + Math.random() * view.h * .6;
      b.vx = (left ? 1 : -1) * (25 + Math.random() * 25); b.vy = (Math.random() - .5) * 10; b.init = true;
    }
    b.x += b.vx * dt; b.y += b.vy * dt + Math.sin(now / 200 + b.ph) * .4;
    const flap = Math.floor(now / 90 + b.ph) % 2, x = Math.round(b.x), y = Math.round(b.y);
    cx.fillStyle = '#120A18';
    cx.fillRect(x - 1, y, 3, 2);
    if (flap){ cx.fillRect(x - 4, y - 2, 3, 1); cx.fillRect(x + 2, y - 2, 3, 1); cx.fillRect(x - 3, y - 1, 2, 1); cx.fillRect(x + 2, y - 1, 2, 1); }
    else { cx.fillRect(x - 4, y + 1, 3, 1); cx.fillRect(x + 2, y + 1, 3, 1); }
  });
  cx.globalCompositeOperation = 'lighter';
  wisps.forEach((w, i) => {
    const x = view.x + ((w.x * view.w + now / 90 * (i % 2 ? 1 : -1)) % view.w + view.w) % view.w, y = view.y + w.y * view.h + Math.sin(now / 700 + w.ph) * 6;
    cx.globalAlpha = .35 + .3 * Math.sin(now / 300 + w.ph); cx.drawImage(glow(4, [170, 255, 230]), x - 4, y - 4);
  });
  cx.globalCompositeOperation = 'source-over';
  fogs.forEach(f => {
    const x = view.x + ((f.x * (view.w + 200) + now / 1000 * f.v) % (view.w + 200)) - 100, y = view.y + f.y * view.h;
    cx.globalAlpha = .1; cx.drawImage(glow(Math.round(f.s), [200, 170, 230]), x - f.s, y - f.s * .5, f.s * 2, f.s);
  });
  cx.globalAlpha = 1;
}
const glowCache = {};
function glow(r, c){ const k = r + c.join(); if (glowCache[k]) return glowCache[k]; const g = document.createElement('canvas'); g.width = g.height = r * 2; const x = g.getContext('2d'); const gr = x.createRadialGradient(r, r, 0, r, r, r); gr.addColorStop(0, `rgba(${c},1)`); gr.addColorStop(.35, `rgba(${c},.45)`); gr.addColorStop(1, `rgba(${c},0)`); x.fillStyle = gr; x.fillRect(0, 0, r * 2, r * 2); return glowCache[k] = g; }
// 할로윈 마을은 늘 밤이에요. 버튼으로 밝기만 바꿔요
let bright = 0; const BRIGHT = [[160, 140, 200], [205, 190, 230], [120, 100, 165]], BRIGHT_NEXT = ['밝게', '어둡게', '보통'];
function phase(){ return 'night'; }
const fx = [];
let last = performance.now();
function drawPerson(p){ const cx = out;
  const [sx, sy] = P(p.x + .5, p.y + .5);
  cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 5, 2, 0, 0, Math.PI * 2); cx.fill();
  const f = p.path.length ? 1 + Math.floor(p.t * (p.me ? 12 : 8)) % 2 : 0, col = (p.back ? 3 : 0) + f, X = Math.round(sx), Y = Math.round(sy) - 34;
  const S = World.Avatar.compose(p.av), FW = World.Avatar.FW, FH = World.Avatar.FH;
  if (p.flip){ cx.save(); cx.translate(X + 11, Y); cx.scale(-1, 1); cx.drawImage(S, col * FW, 0, FW, FH, 0, 0, FW, FH); cx.restore(); } else cx.drawImage(S, col * FW, 0, FW, FH, X - 11, Y, FW, FH);
}
function frame(now){
  const dt = Math.min(.05, (now - last) / 1000); last = now;
  people.forEach(p => step(p, dt));
  const A = MAPS[map];
  // 카메라 먼저: 맵이 화면보다 작으면 가운데에, 크면 내 캐릭터를 따라가요
  { const [mx, my] = P(me.x + .5, me.y + .5);
    const tx = M.W <= VW ? (M.W - VW) / 2 : Math.max(0, Math.min(M.W - VW, mx - VW / 2));
    const ty = M.H <= VH ? (M.H - VH) / 2 - 10 : Math.max(0, Math.min(M.H - VH, my - 14 - VH / 2));
    if (camX === null){ camX = tx; camY = ty; } camX += (tx - camX) * Math.min(1, dt * 8); camY += (ty - camY) * Math.min(1, dt * 8); }
  const ix = Math.round(camX), iy = Math.round(camY);
  const view = { x: ix - 4, y: iy - 4, w: VW + 8, h: VH + 8 };
  out.setTransform(1, 0, 0, 1, 0, 0); out.fillStyle = M.fill || (M.indoor ? '#0C0715' : '#1E2A1C'); out.fillRect(0, 0, VW, VH);
  out.setTransform(1, 0, 0, 1, -ix, -iy);
  const cx = out;
  cx.drawImage(A.bg, Math.max(0, ix), Math.max(0, iy), VW, VH, Math.max(0, ix), Math.max(0, iy), VW, VH);
  // 물결 반짝임
  if (M.water) for (let i = 0; i < 6; i++){ const w = M.water[(Math.random() * M.water.length) | 0]; const [wx, wy] = P(w[0] + Math.random(), w[1] + Math.random()); if (wx > view.x && wx < view.x + view.w && wy > view.y && wy < view.y + view.h) fx.push({ x: wx, y: wy, v: 0, life: .5, c: '#DFF2FF' }); }
  // 문 표시 (반짝이는 발판)
  const pulse = .5 + .5 * Math.sin(now / 300);
  M.objs.forEach(o => { if (!o.door) return; const [x, y] = P(o.door.tile[0] + .5, o.door.tile[1] + .5); cx.fillStyle = `rgba(255,216,102,${.25 + .35 * pulse})`; cx.beginPath(); cx.moveTo(x, y - 4); cx.lineTo(x + 8, y); cx.lineTo(x, y + 4); cx.lineTo(x - 8, y); cx.fill(); });
  // 사람을 정렬된 물건 사이에 끼워 넣기
  const R = o => ({ x: o.x, y: o.y, w: o.sw, h: o.sh });
  const list = objOrder.filter(o => sOver(R(o), view)).map(o => ({ o }));
  [...people].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(p => {
    const [sx, sy] = P(p.x + .5, p.y + .5), pr = { x: sx - 11, y: sy - 35, w: 22, h: 36 }, pb = [p.x + .15, p.y + .15, p.x + .85, p.y + .85];
    let idx = 0; list.forEach((it, i) => { if (it.o && sOver(R(it.o), pr) && behind(it.o.box, pb)) idx = i + 1; });
    list.splice(idx, 0, { p });
  });
  list.forEach(it => it.o ? cx.drawImage(A.obj, it.o.sx, it.o.sy, it.o.sw, it.o.sh, it.o.x, it.o.y, it.o.sw, it.o.sh) : drawPerson(it.p));
  // 효과: 연구실 솥 거품, 분수 물방울
  const src = M.objs.find(o => o.name === 'cauldron' || o.name === 'fountain');
  if (src && Math.random() < .2){ const bx = src.x + src.sw / 2, by = src.y + (src.name === 'fountain' ? 4 : 10); fx.push({ x: bx - 5 + Math.random() * 10, y: by, v: 8 + Math.random() * 8, life: 1.2, c: src.name === 'fountain' ? '#C8EEFF' : '#9CFFD0' }); }
  fx.forEach(b => { b.y -= b.v * dt; b.life -= dt; }); while (fx.length && fx[0].life <= 0) fx.shift();
  fx.forEach(b => { cx.fillStyle = b.c; cx.fillRect(Math.round(b.x), Math.round(b.y), 1, 1); });
  // 빛: 실내는 늘 어둑, 바깥은 시간대에 따라
  const ph = M.indoor ? 'night' : phase();
  if (ph !== 'day'){
    cx.globalCompositeOperation = 'multiply'; cx.fillStyle = M.indoor ? 'rgb(150,130,175)' : `rgb(${BRIGHT[bright]})`; cx.fillRect(ix, iy, VW, VH);
    cx.globalCompositeOperation = 'lighter';
    M.lights.forEach((L, i) => { if (L.p[0] + L.r < view.x || L.p[0] - L.r > view.x + view.w || L.p[1] + L.dy + L.r < view.y || L.p[1] + L.dy - L.r > view.y + view.h) return; const fl = L.f ? .85 + .15 * Math.sin(now / 130 + i * 1.7) * Math.sin(now / 370 + i) : 1; cx.globalAlpha = L.a * fl * (ph === 'dusk' ? .5 : 1); cx.drawImage(glow(L.r, L.c), L.p[0] - L.r, L.p[1] + L.dy - L.r); });
    cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over';
  }
  if (!M.indoor) spooky(now, dt, view);
  out.setTransform(1, 0, 0, 1, 0, 0);
  const k = cv.clientWidth / VW;
  people.forEach((p, i) => { const [sx, sy] = P(p.x + .5, p.y + .5); tags[i].style.left = (sx - ix) * k + 'px'; tags[i].style.top = (sy - 36 - iy) * k + 'px'; });
  if (bubble){ const o = bubble.o; bubble.el.style.left = Math.max(90, Math.min(cv.clientWidth - 90, (o.x + o.sw / 2 - ix) * k)) + 'px'; bubble.el.style.top = Math.max(70, (o.y - 2 - iy) * k) + 'px'; }
  const d = new Date(); document.getElementById('clock').textContent = `🌕 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')} · 보름밤`;
  requestAnimationFrame(frame);
}
document.getElementById('tDay').onclick = e => { bright = (bright + 1) % 3; e.target.textContent = BRIGHT_NEXT[bright]; };
document.getElementById('tZoom').onclick = e => { zi = (zi + 1) % ZOOMS.length; e.target.textContent = ZOOMS[(zi + 1) % ZOOMS.length][0]; resize(); camX = null; };
// 지도: 캠퍼스 전체를 작게 그려서 보여 주고, 누르면 그곳으로 걸어가요
const mapv = document.getElementById('mapv'), mcv = document.getElementById('mcv');
let mapImg = null;
function openMap(){
  if (map !== 'campus'){ showBubble({ x: 0, y: 0, sw: 0 }, '지도는 바깥에서 볼 수 있어요'); return; }
  const C = MAPS.campus, m = C.meta;
  if (!mapImg){ mapImg = document.createElement('canvas'); mapImg.width = m.W; mapImg.height = m.H; const g = mapImg.getContext('2d'); g.drawImage(C.bg, 0, 0); C.order.forEach(o => g.drawImage(C.obj, o.sx, o.sy, o.sw, o.sh, o.x, o.y, o.sw, o.sh)); }
  mcv.width = m.W; mcv.height = m.H; const g = mcv.getContext('2d'); g.drawImage(mapImg, 0, 0);
  mapv.classList.add('on'); document.querySelectorAll('.mlabel').forEach(e => e.remove());
  requestAnimationFrame(() => {
    // 화면 높이에 맞춰 크게 그리고, 옆으로 밀어서 봐요
    const wrap = document.getElementById('mwrap'), inner = document.getElementById('minner'), k = Math.min(wrap.clientHeight / m.H, 1.2);
    const w = Math.floor(m.W * k), h = Math.floor(m.H * k);
    mcv.style.width = w + 'px'; mcv.style.height = h + 'px'; inner.style.width = w + 'px'; inner.style.height = h + 'px';
    const lab = (t, txt, cls) => { const [x, y] = P(t[0] + .5, t[1] + .5); const d = document.createElement('div'); d.className = 'mlabel' + (cls ? ' ' + cls : ''); d.textContent = txt; d.style.left = x * k + 'px'; d.style.top = (y * k - 4) + 'px'; inner.appendChild(d); };
    m.areas.forEach(a => lab(a.t, a.n)); lab([me.x, me.y], '나', 'me');
    const [px_, py_] = P(me.x + .5, me.y + .5); wrap.scrollLeft = px_ * k - wrap.clientWidth / 2; wrap.scrollTop = py_ * k - wrap.clientHeight / 2;
  });
}
mcv.addEventListener('click', e => {   // 탭할 때만 (밀어서 볼 때는 안 움직여요)
  const m = MAPS.campus.meta, r = mcv.getBoundingClientRect(), x = (e.clientX - r.left) * m.W / r.width, y = (e.clientY - r.top) * m.H / r.height;
  // 가장 가까운 장소로, 없으면 누른 곳 근처 빈칸으로
  let best = null, bd = 1e9; m.areas.forEach(a => { const [ax, ay] = P(a.t[0] + .5, a.t[1] + .5), d = Math.hypot(ax - x, ay - y); if (d < bd){ bd = d; best = a.t; } });
  let tgt = bd < 30 ? best : [Math.floor(((x - m.OX) / 8 + (y - m.OY) / 4) / 2), Math.floor(((y - m.OY) / 4 - (x - m.OX) / 8) / 2)];
  for (let rr = 0; rr < 6 && !free(tgt[0], tgt[1]); rr++) for (const [dx, dy] of [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1]]) if (free(tgt[0] + dx * rr, tgt[1] + dy * rr)){ tgt = [tgt[0] + dx * rr, tgt[1] + dy * rr]; break; }
  mapv.classList.remove('on'); hideBubble(); pending = null;
  const door = m.objs.find(o => o.door && o.door.tile[0] === tgt[0] && o.door.tile[1] === tgt[1]);
  if (goto(me, tgt[0], tgt[1]) && door) pending = { door: door.door, o: door };
});
document.getElementById('tMap').onclick = openMap;
document.getElementById('mClose').onclick = () => mapv.classList.remove('on');
World.ready = (async () => {
  await World.Avatar.ready;
  for (const [id, m] of Object.entries(MAPS)){
    const [bg, obj] = await Promise.all([img(m.meta.bgSrc), img(m.meta.objSrc)]);
    m.bg = bg; m.obj = obj;
    const pc = document.createElement('canvas'); pc.width = obj.width; pc.height = obj.height; m.px = pc.getContext('2d', { willReadFrequently: true }); m.px.drawImage(obj, 0, 0);
  }
})();
World.start = async (id = 'campus', spawn) => {
  await World.ready; if (started) return; started = true;
  resize(); setMap(id, spawn || MAPS[id].meta.start || MAPS[id].meta.spawnIn);
  requestAnimationFrame(frame);
};
World.setPlayer = (name, av) => { me.name = name; me.av = av; if (tags[0]) tags[0].textContent = name; };
World.resize = () => { if (started){ resize(); camX = null; } };
World.where = () => map;
// 그 방의 물건 옆으로 순간 이동 (홈 화면의 바로 가기)
World.teleport = (id, objName, then) => {
  if (!started || busy) return;
  busy = true; fadeEl.textContent = MAPS[id].meta.title; fadeEl.style.opacity = 1;
  setTimeout(() => {
    if (map !== id) setMap(id, MAPS[id].meta.start || MAPS[id].meta.spawnIn);
    const o = M.objs.find(x => x.name === objName);
    if (o){ const tiles = []; for (let a = Math.floor(o.box[0]); a < Math.ceil(o.box[2]); a++) for (let b = Math.floor(o.box[1]); b < Math.ceil(o.box[3]); b++) tiles.push([a, b]); const c = near(tiles)[0]; if (c){ me.x = c[0]; me.y = c[1]; me.path = []; camX = null; } }
    setTimeout(() => { fadeEl.style.opacity = 0; busy = false; then && then(); }, 150);
  }, 380);
};
