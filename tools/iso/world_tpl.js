
// 걸어 다니는 세계 (tools/iso/build_halloween.py가 MAPS를 채워서 public/world.js로 써요)
// 게임(index.html)과는 window.World로 이어져요: World.start / setPlayer / teleport / onAct
const MAPS = __MAPS__;
const World = window.World = { onAct: null, onMove: null };
// ---------- 캐릭터 조합 (tools/iso/chars5.py 부품) ----------
// av = { hair, eyes, mouth, uni: 부품 번호, skinC, eyeC, hairC, shoeC: 색 번호, house: 교복 색이 될 기숙사 }
const AVM = __AVATAR__;
const ASC = AVM.scale || .5;   // 캐릭터 그림 1픽셀 = 세계 픽셀의 몇 배
World.Avatar = (() => {
  const FW = AVM.fw, FH = AVM.fh, CATS = ['hair', 'eyes', 'mouth', 'uni'], HOUSES = Object.keys(AVM.pal.house);
  const COLORS = { skinC: 'skin', eyeC: 'eye', hairC: 'hair', shoeC: 'shoes' };
  let data = null; const cache = new Map(), heads = new Map();
  const ready = new Promise(r => { const i = new Image(); i.onload = () => { const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0); data = g.getImageData(0, 0, i.width, i.height); r(); }; i.src = AVM.src; });
  const rgb = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  // 회색 밝기 → 색: 팔레트 4색을 기준 밝기(stops)에 놓고 사이는 이어서 칠해요 (원래 음영을 그대로 살려요)
  const luts = {};
  function lutOf(slot, colors){
    const k = slot + colors.join(); if (luts[k]) return luts[k];
    const st = AVM.stops[slot], cs = colors.map(rgb), T = new Uint8ClampedArray(256 * 3);
    for (let v = 0; v < 256; v++){
      let c;
      if (v >= st[0]){ const t = (v - st[0]) / Math.max(1, 255 - st[0]) * .6; c = cs[0].map(a => a + (255 - a) * t); }
      else if (v <= st[3]){ const t = v / Math.max(1, st[3]); c = cs[3].map(a => a * (.55 + .45 * t)); }
      else { let i = 0; while (!(st[i + 1] <= v && v <= st[i])) i++; const t = (st[i] - v) / Math.max(1, st[i] - st[i + 1]); c = cs[i].map((a, j) => a + (cs[i + 1][j] - a) * t); }
      T[v * 3] = c[0]; T[v * 3 + 1] = c[1]; T[v * 3 + 2] = c[2];
    }
    return luts[k] = T;
  }
  const rnd = seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const mod = (v, n) => ((v | 0) % n + n) % n;
  function fix(av){
    const a = Object.assign({}, av || {});
    CATS.forEach(c => { a[c] = mod(a[c], AVM.parts[c].length); });
    Object.entries(COLORS).forEach(([k, p]) => { a[k] = mod(a[k], AVM.pal[p].length); });
    if (!HOUSES.includes(a.house)) delete a.house;
    return a;
  }
  // 옛 캐릭터(look 번호)도 그 번호로 정해진 조합을 줘요
  function fromLook(look){
    const r = rnd(((look | 0) + 7) * 9973 + 1), a = {};
    CATS.forEach(c => { a[c] = Math.floor(r() * AVM.parts[c].length); });
    Object.entries(COLORS).forEach(([k, p]) => { a[k] = Math.floor(r() * AVM.pal[p].length); });
    return a;
  }
  const random = () => ({ ...fromLook(Math.floor(Math.random() * 1e6)), house: HOUSES[Math.floor(Math.random() * HOUSES.length)] });
  function compose(av){
    av = fix(av); const key = JSON.stringify(av); if (cache.has(key)) return cache.get(key);
    const W = FW * (AVM.frames || 6), out = new ImageData(W, FH), o = out.data, src = data.data, SW = data.width;
    const P = AVM.pal, ramp = { skin: lutOf('skin', P.skin[av.skinC]), eye: lutOf('eye', P.eye[av.eyeC]), hair: lutOf('hair', P.hair[av.hairC]), shoes: lutOf('shoes', P.shoes[av.shoeC]), cloth: lutOf('cloth', P.cloth[0]), house: lutOf('house', P.house[HOUSES.includes(av.house) ? av.house : 'moon']) };
    const layers = AVM.base.concat(...CATS.map(c => AVM.parts[c][av[c]].L)).sort((a, b) => AVM.z.indexOf(a[2]) - AVM.z.indexOf(b[2]));
    layers.forEach(([row, slot]) => {
      const rp = slot ? ramp[slot] : null;
      for (let y = 0; y < FH; y++) for (let x = 0; x < W; x++){
        const s = ((row * FH + y) * SW + x) * 4; if (!src[s + 3]) continue;
        const d = (y * W + x) * 4, r = src[s], g = src[s + 1], b = src[s + 2];
        if (rp && r === g && g === b){ o[d] = rp[r * 3]; o[d + 1] = rp[r * 3 + 1]; o[d + 2] = rp[r * 3 + 2]; } else { o[d] = r; o[d + 1] = g; o[d + 2] = b; }
        o[d + 3] = 255;
      }
    });
    if (AVM.outline){   // 다 합친 뒤 바깥 테두리
      const edge = [];
      for (let y = 0; y < FH; y++) for (let x = 0; x < W; x++){
        if (o[(y * W + x) * 4 + 3]) continue; const fx = x % FW;
        if ((fx > 0 && o[(y * W + x - 1) * 4 + 3]) || (fx < FW - 1 && o[(y * W + x + 1) * 4 + 3]) || (y > 0 && o[((y - 1) * W + x) * 4 + 3]) || (y < FH - 1 && o[((y + 1) * W + x) * 4 + 3])) edge.push((y * W + x) * 4);
      }
      edge.forEach(d => { o[d] = 42; o[d + 1] = 24; o[d + 2] = 48; o[d + 3] = 255; });
    }
    const c = document.createElement('canvas'); c.width = W; c.height = FH; c.getContext('2d').putImageData(out, 0, 0);
    cache.set(key, c); return c;
  }
  // 얼굴 동그라미용 (앞모습 머리 부분을 정사각형으로)
  const HB = AVM.head, HS = HB.b - HB.t, HX = Math.round((FW - HS) / 2);
  function head(av){
    if (!data) return '';
    const key = JSON.stringify(fix(av)); if (heads.has(key)) return heads.get(key);
    const c = document.createElement('canvas'); c.width = HS; c.height = HS; c.getContext('2d').drawImage(compose(av), HX, HB.t, HS, HS, 0, 0, HS, HS);
    const u = c.toDataURL(); heads.set(key, u); return u;
  }
  return { ready, compose, head, fix, fromLook, random, meta: AVM, FW, FH, CATS, HOUSES, headBox: { x: HX, y: HB.t, s: HS }, get loaded(){ return !!data; } };
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
  cv.width = VW * KPX; cv.height = VH * KPX;   // 캔버스는 기기 픽셀 그대로: 세계는 KPX배, 캐릭터는 더 촘촘하게 그려요
  cv.style.width = (VW * KPX / dpr) + 'px'; cv.style.height = (VH * KPX / dpr) + 'px';
  out.imageSmoothingEnabled = false;
}
addEventListener('resize', resize);
const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = s; });
let map, M, blocked, objOrder, rmap;
// 기숙사 휴게실은 단계마다 다른 방이에요: 'dorm_witch' → 'dorm_witch_3' 처럼 바꿔 보여 줘요
const ALIAS = {}; Object.keys(MAPS).forEach(k => { const m = k.match(/^(dorm_\w+?)_1$/); if (m) ALIAS[m[1]] = k; });
const real = id => ALIAS[id] || id;
// 휴게실·개인 방 그림은 들어갈 때 불러와요 (처음 열 때 빠르게)
async function ensureMap(id){
  const m = MAPS[real(id)]; if (m.bg) return;
  if (!m.loading) m.loading = (async () => {
    const [bg, obj] = await Promise.all([img(m.meta.bgSrc), img(m.meta.objSrc)]);
    const pc = document.createElement('canvas'); pc.width = obj.width; pc.height = obj.height; const px = pc.getContext('2d', { willReadFrequently: true }); px.drawImage(obj, 0, 0);
    m.px = px; m.obj = obj; m.bg = bg;
  })();
  return m.loading;
}
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
const mk = (name, av, x, y, me) => ({ name, av, x, y, path: [], view: 0, flip: false, me, t: 0, idle: Math.random() * 3 });
const me = mk('나', null, 0, 0, true);
let started = false;
let crowd = {};
function rebuildObjs(){   // 지도 물건 + (개인 방이면) 놓은 가구
  const fo = M.furn ? furnObjs() : [];
  blocked = new Set(); [...M.objs, ...fo].forEach(o => { if (o.solid !== false) for (let x = Math.floor(o.box[0]); x < Math.ceil(o.box[2]); x++) for (let y = Math.floor(o.box[1]); y < Math.ceil(o.box[3]); y++) blocked.add(x + ',' + y); });
  flats = fo.filter(o => o.flat);
  objOrder = fo.length ? orderObjs([...M.objs, ...fo.filter(o => !o.flat)]) : (MAPS[rmap].order || (MAPS[rmap].order = orderObjs(M.objs)));
}
function setMap(id, spawn){
  map = id; rmap = real(id); M = MAPS[rmap].meta; resize(); placing = null;
  rebuildObjs();
  if (!spawn || !free(spawn[0], spawn[1])) spawn = M.spawnIn || M.start || spawn;
  me.x = spawn[0]; me.y = spawn[1]; me.path = []; me.view = 0; me.flip = false;
  if (!crowd[id]){ crowd[id] = []; const n = id === 'campus' ? 9 : (id === 'barn' || id === 'pen' || M.furn || M.rooms) ? 0 : 2; for (let i = 0; i < n; i++){ for (let k = 0; k < 50; k++){ const x = Math.floor(Math.random() * M.NX), y = Math.floor(Math.random() * M.NY); if (free(x, y)){ crowd[id].push(mk(NAMES[(i + (id === 'lab' ? 3 : 0)) % NAMES.length], World.Avatar.random(), x, y, false)); break; } } } }
  people.length = 0; people.push(me, ...crowd[id]);
  if (M.pets) people.push(...spawnPets());
  tags.forEach(t => t.remove()); tags = people.map(p => { const d = document.createElement('div'); d.className = 'ntag' + (p.me ? ' me' : ''); d.textContent = p.name; if (p.pet) d.style.display = 'none'; world.appendChild(d); return d; });
  penTags.forEach(t => t.remove()); penTags = [];
  roomTags.forEach(t => t.remove()); roomTags = [];
  if (M.rooms) roomTags = M.rooms.map(rm => { const nm = (hallNames[M.house] || [])[rm.i]; const d = document.createElement('div'); d.className = 'ntag' + (nm && nm === me.name ? ' me' : ''); d.textContent = nm || '빈 방'; world.appendChild(d); return d; });
  if (M.pens) penTags = M.pens.map(pn => { const d = document.createElement('div'); d.className = 'ntag' + (pn.i === myPen ? ' me' : ''); d.textContent = penNames[pn.i] || '빈 우리'; world.appendChild(d); return d; });
  document.getElementById('place').textContent = M.title; document.getElementById('sub').textContent = M.sub;
  if (M.furn){ document.getElementById('place').textContent = roomView.own ? '내 방' : (roomView.name || '친구') + '의 방'; document.getElementById('sub').textContent = roomView.own ? M.sub : '방명록에 한 줄 남겨 봐요'; }
  camX = camY = null; hideBubble();
}
// ---------- 개인 방 가구 (tools/iso/furniture.py) ----------
const FURN = __FURN__; World.FURN = FURN;
let FURN_IMG = null, FURN_PX = null, furnData = [], flats = [], placing = null, roomView = { own: true };
const shownFurn = () => roomView.own ? furnData : (roomView.furn || []);
World.onFurn = null;      // (가구 id) 놓은 가구를 눌렀을 때 → 글이면 말풍선, {text, btn, fn}이면 버튼 말풍선
World.onPlaced = null;
function furnObjs(){
  return shownFurn().map(f => { const it = FURN.items[f.k]; if (!it) return null; const [px, py] = P(f.x, f.y);
    return { name: 'furn', fid: f.id, furn: it, box: [f.x, f.y, f.x + it.w, f.y + it.d], x: px - it.ax, y: py - it.ay, sx: it.sx, sy: 0, sw: it.sw, sh: it.sh, solid: !!it.solid, flat: !!it.flat }; }).filter(Boolean);
}
World.setFurniture = list => { furnData = list || []; if (M && M.furn && roomView.own){ rebuildObjs(); } };
World.roomOwner = () => (M && M.furn) ? roomView : null;   // 지금 보고 있는 방 주인 { own, uid, name }
World.onRoomDoor = null;   // (기숙사, 문 번호) → { own, uid, name, furn } 이면 들어가요, 글이면 말풍선
let hallNames = {};
World.setHallNames = names => { hallNames = names || {}; if (M && M.rooms) roomTags.forEach((t, i) => { t.textContent = (hallNames[M.house] || [])[M.rooms[i].i] || '빈 방'; }); };
// 바로 가기: 그 기숙사 복도의 i번째 방으로
World.goRoom = (house, i) => {
  const hid = 'hall_' + ({ ember: 'witch', moon: 'vamp', dusk: 'wolf', dew: 'ghost' })[house]; if (!MAPS[hid]) return;
  const d = MAPS[hid].meta.objs.find(o => o.door && o.door.room === i); if (!d) return;
  World.teleport(hid, null, () => { me.x = d.door.tile[0]; me.y = d.door.tile[1] + 1; camX = null; goDoor(d.door, d); });
};
// 놓을 수 있나: 방 안, 막힌 곳·문·나 있는 칸이 아니어야 해요 (바닥 러그끼리는 겹치지 않게)
function canPlace(k, x, y, skip){
  const it = FURN.items[k]; if (!it) return false;
  const taken = new Set(); M.objs.forEach(o => { if (o.door || o.solid !== false) for (let a = Math.floor(o.box[0]); a < Math.ceil(o.box[2]); a++) for (let b = Math.floor(o.box[1]); b < Math.ceil(o.box[3]); b++) taken.add(a + ',' + b); });
  furnObjs().forEach(o => { if (o.fid === skip || (!!o.flat !== !!it.flat)) return; for (let a = o.box[0]; a < o.box[2]; a++) for (let b = o.box[1]; b < o.box[3]; b++) taken.add(a + ',' + b); });
  for (let a = x; a < x + it.w; a++) for (let b = y; b < y + it.d; b++){
    if (a < 0 || b < 0 || a >= M.NX || b >= M.NY - 1 || taken.has(a + ',' + b)) return false;
    if (it.solid && Math.round(me.x) === a && Math.round(me.y) === b) return false;
  }
  return true;
}
// 가구 놓기: 바닥을 누르면 그 자리에 미리 보여 주고, [여기 놓기]를 누르면 놓아요
World.place = (k, cb) => { if (!roomView.own) return; placing = { k, at: null, cb }; hideBubble(); showBubble({ x: P(me.x + .5, me.y + .5)[0], y: P(me.x + .5, me.y + .5)[1] - 30, sw: 0 }, `<b>${FURN.items[k].name}</b><br>놓을 곳을 눌러요`, '그만두기', () => { placing = null; hideBubble(); }); };
World.cancelPlace = () => { placing = null; hideBubble(); };
// ---------- 사육장: 우리 문 · 이름표 · 내 생물 ----------
const CR_SRC = __CRSRC__, CR_W = 40, CR_H = 34;
let CR_IMG = null, penNames = [], myPen = 0, petData = [], penTags = [], roomTags = [];
const petPos = {};
World.onPenDoor = null;   // (우리 번호) → true면 들어가요, 글이면 말풍선
World.onPet = null;       // (생물 id) 생물을 눌렀을 때
World.setPenLabels = (names, mine) => { penNames = names; myPen = mine; penTags.forEach((t, i) => { t.textContent = names[M.pens[i].i] || '빈 우리'; t.className = 'ntag' + (M.pens[i].i === mine ? ' me' : ''); }); };
World.setPenExit = spawn => { const ex = MAPS.pen && MAPS.pen.meta.objs.find(o => o.name === 'exit'); if (ex) ex.door.spawn = spawn; };
World.setPets = list => {
  petData = list;
  if (!M || !M.pets) return;
  const keep = people.filter(p => !p.pet), add = spawnPets();
  people.length = 0; people.push(...keep, ...add);
  tags.forEach(t => t.remove()); tags = people.map(p => { const d = document.createElement('div'); d.className = 'ntag' + (p.me ? ' me' : ''); d.textContent = p.name; if (p.pet) d.style.display = 'none'; world.appendChild(d); return d; });
};
function spawnPets(){
  return petData.map(d => {
    let pos = petPos[d.id];
    if (!pos || !free(Math.round(pos.x), Math.round(pos.y))){ for (let k = 0; k < 80; k++){ const x = 2 + Math.floor(Math.random() * (M.NX - 4)), y = 6 + Math.floor(Math.random() * (M.NY - 9)); if (free(x, y)){ pos = { x, y }; break; } } }
    const p = mk(d.name || '', null, pos ? pos.x : 10, pos ? pos.y : 10, false); p.pet = d; petPos[d.id] = p; p.idle = Math.random() * 4; return p;
  });
}
// 생물 색: CSS filter(sepia·saturate·hue-rotate·brightness)와 같은 계산으로 픽셀을 물들여요
function colorMatrix(c){
  if (!c || c.p === undefined) return null;
  const mul = (A, B) => A.map((_, i) => { const r = Math.floor(i / 3), k = i % 3; return A[r * 3] * B[k] + A[r * 3 + 1] * B[3 + k] + A[r * 3 + 2] * B[6 + k]; });
  const q = 1 - c.p, sep = [.393 + .607 * q, .769 - .769 * q, .189 - .189 * q, .349 - .349 * q, .686 + .314 * q, .168 - .168 * q, .272 - .272 * q, .534 - .534 * q, .131 + .869 * q];
  const s = c.s, sat = [.213 + .787 * s, .715 - .715 * s, .072 - .072 * s, .213 - .213 * s, .715 + .285 * s, .072 - .072 * s, .213 - .213 * s, .715 - .715 * s, .072 + .928 * s];
  const a = c.h * Math.PI / 180, co = Math.cos(a), si = Math.sin(a);
  const hue = [.213 + co * .787 - si * .213, .715 - co * .715 - si * .715, .072 - co * .072 + si * .928, .213 - co * .213 + si * .143, .715 + co * .285 + si * .140, .072 - co * .072 - si * .283, .213 - co * .213 - si * .787, .715 - co * .715 + si * .715, .072 + co * .928 + si * .072];
  return mul(mul(hue, sat), sep).map(v => v * c.b);
}
const petSprites = {};
function petSprite(k, col){
  const key = k + JSON.stringify(col || {}); if (petSprites[key]) return petSprites[key];
  const c = document.createElement('canvas'); c.width = CR_W; c.height = CR_H; const g = c.getContext('2d'); g.drawImage(CR_IMG, k * CR_W, 0, CR_W, CR_H, 0, 0, CR_W, CR_H);
  const m = colorMatrix(col);
  if (m){ const d = g.getImageData(0, 0, CR_W, CR_H), a = d.data; for (let i = 0; i < a.length; i += 4){ if (!a[i + 3]) continue; const r = a[i], gg = a[i + 1], b = a[i + 2]; a[i] = m[0] * r + m[1] * gg + m[2] * b; a[i + 1] = m[3] * r + m[4] * gg + m[5] * b; a[i + 2] = m[6] * r + m[7] * gg + m[8] * b; } g.putImageData(d, 0, 0); }
  return petSprites[key] = c;
}
function drawPet(p){
  const cx = out, [sx, sy] = P(p.x + .5, p.y + .5), d = p.pet, sc = d.adult ? 1 : .7;
  cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 7 * sc, 2.5 * sc, 0, 0, Math.PI * 2); cx.fill();
  const S = petSprite(d.k, d.col), cp = KPX / 2 * sc, w = CR_W * cp, h = CR_H * cp;
  const bob = p.path.length ? Math.round(Math.abs(Math.sin(p.t * 10)) * 2 * cp) : 0;
  const dx = Math.round((sx - camIX) * KPX), dy = Math.round((sy - camIY) * KPX - h + cp) - bob;
  cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
  if (p.flip){ cx.translate(dx, dy); cx.scale(-1, 1); cx.drawImage(S, -w / 2, 0, w, h); } else cx.drawImage(S, Math.round(dx - w / 2), dy, w, h);
  cx.restore();
}
let tags = [], bubble = null, pending = null, busy = false, camX = null, camY = null, forceNight = null, backStack = [];
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
  if (door.pen !== undefined && World.onPenDoor){   // 사육장 우리: 주인만 들어가요
    const r = World.onPenDoor(door.pen);
    if (r !== true){ const [bx, by] = P(door.tile[0] + .5, door.tile[1] + .5); showBubble({ x: bx, y: by - 26, sw: 0 }, r); return; }
  }
  let label = door.label, view = null;
  if (door.room !== undefined){   // 기숙사 복도의 학생 방 문
    const r = World.onRoomDoor ? World.onRoomDoor(M.house, door.room) : null;
    if (!r || typeof r === 'string'){ const [bx, by] = P(door.tile[0] + .5, door.tile[1] + .5); showBubble({ x: bx, y: by - 30, sw: 0 }, r || '<b>빈 방</b>'); return; }
    view = r; label = r.own ? '내 방' : r.name + '의 방';
  }
  if (!door.to){ showBubble(o, `<b>${door.label}</b><br>아직 문이 잠겨 있어요 · 곧 열려요`); return; }
  let to = door.to, spawn = door.spawn;
  // 돌아가는 문: 들어온 순서를 거꾸로 (없으면 그 방의 바깥 방으로)
  if (to === '@back'){ const b = backStack.pop(); to = b ? b.map : (M.backTo || 'campus'); spawn = b ? b.pos : null; label = (MAPS[real(to)] || MAPS.campus).meta.title; }
  else if (door.back) backStack.push({ map, pos: [Math.round(me.x), Math.round(me.y + (door.tile[1] === 0 ? 1 : 0))] });
  if (view) roomView = view;
  busy = true; fadeEl.textContent = label; fadeEl.style.opacity = 1;
  const t0 = Date.now(); ensureMap(to).then(() => setTimeout(() => { setMap(to, spawn); setTimeout(() => { fadeEl.style.opacity = 0; busy = false; }, 150); }, Math.max(0, 380 - (Date.now() - t0))));
}
function goto(p, gx, gy){ const r = path(Math.round(p.x), Math.round(p.y), gx, gy); if (r){ p.path = r; return true; } return false; }
function near(tiles){ const c = []; tiles.forEach(([a, b]) => [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx, dy]) => free(a + dx, b + dy) && c.push([a + dx, b + dy]))); return c.sort((p1, p2) => Math.hypot(p1[0] - me.x, p1[1] - me.y) - Math.hypot(p2[0] - me.x, p2[1] - me.y)); }
cv.addEventListener('pointerdown', e => {
  if (busy) return;
  const r = cv.getBoundingClientRect(), x = (e.clientX - r.left) * VW / r.width + Math.round(camX), y = (e.clientY - r.top) * VH / r.height + Math.round(camY);
  const tileAt = () => [Math.floor(((x - M.OX) / 8 + (y - M.OY) / 4) / 2), Math.floor(((y - M.OY) / 4 - (x - M.OX) / 8) / 2)];
  if (placing){
    const [tx, ty] = tileAt(), it = FURN.items[placing.k], gx = tx - Math.floor((it.w - 1) / 2), gy = ty - Math.floor((it.d - 1) / 2);
    placing.at = [gx, gy]; const ok = canPlace(placing.k, gx, gy);
    const [bx, by] = P(gx + it.w / 2, gy + it.d / 2), pl = placing;
    hideBubble(); showBubble({ x: bx, y: by - it.ay - 6, sw: 0 }, `<b>${it.name}</b><br>${ok ? '여기에 놓을까요?' : '여기엔 놓을 수 없어요'}`, ok ? '여기 놓기' : '그만두기', () => { placing = null; hideBubble(); if (ok && pl.cb) pl.cb(gx, gy); });
    return;
  }
  hideBubble(); pending = null;
  // 우리 안의 생물을 누르면 돌보기 화면
  const pet = people.find(p => p.pet && (() => { const [sx, sy] = P(p.x + .5, p.y + .5), w = p.pet.adult ? 11 : 8, h = p.pet.adult ? 18 : 13; return x >= sx - w && x <= sx + w && y >= sy - h && y <= sy + 2; })());
  if (pet && World.onPet){ World.onPet(pet.pet.id); return; }
  const hit = [...objOrder, ...flats.slice().reverse()].reverse().find(o => (o.door || o.act || o.furn || ACTS[o.name]) && x >= o.x && y >= o.y && x < o.x + o.sw && y < o.y + o.sh && (() => { const px = o.furn ? FURN_PX : MAPS[rmap].px; const d = px.getImageData(o.sx + (x - o.x) | 0, o.sy + (y - o.y) | 0, 1, 1).data; return d[3] > 0; })());
  if (hit && hit.furn){   // 놓은 가구
    const r = World.onFurn ? World.onFurn(hit.fid) : null;
    if (r) showBubble(hit, typeof r === 'string' ? r : r.text, r.btn, r.fn);
    return;
  }
  if (hit){
    if (hit.door){ const [dx, dy] = hit.door.tile; if (Math.round(me.x) === dx && Math.round(me.y) === dy) return goDoor(hit.door, hit); if (goto(me, dx, dy)) pending = { door: hit.door, o: hit }; return; }
    const tiles = []; for (let a = Math.floor(hit.box[0]); a < Math.ceil(hit.box[2]); a++) for (let b = Math.floor(hit.box[1]); b < Math.ceil(hit.box[3]); b++) tiles.push([a, b]);
    for (const c of near(tiles)) if (goto(me, c[0], c[1])){ pending = { act: hit }; return; }
    return;
  }
  const [tx, ty] = tileAt();
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
  // 쿼터뷰 네 방향: x+ (오른쪽 아래) 오른쪽 옆, x- (왼쪽 위) 왼쪽 옆, y+ (왼쪽 아래) 앞, y- (오른쪽 위) 뒤
  // view: 0 앞, 3 뒤, 6 옆(왼쪽 보기). 옆 그림이 없는 옛 부품이면 앞·뒤로 대신해요
  const hasSide = (World.Avatar.meta.frames || 6) >= 9;
  if (Math.abs(dx) > Math.abs(dy)){ if (hasSide){ p.view = 6; p.flip = dx > 0; } else { p.view = dx < 0 ? 3 : 0; p.flip = dx < 0; } }
  else if (d > 0){ p.view = dy < 0 ? 3 : 0; p.flip = false; }
  if (p.pet && d > 0) p.flip = dx - dy > 0;   // 생물은 화면에서 오른쪽으로 가면 뒤집어요
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
let last = performance.now(), camIX = 0, camIY = 0;
function drawPerson(p){ const cx = out;
  if (p.pet) return drawPet(p);
  const [sx, sy] = P(p.x + .5, p.y + .5);
  cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 6, 2.5, 0, 0, Math.PI * 2); cx.fill();
  const f = p.path.length ? 1 + Math.floor(p.t * (p.me ? 12 : 8)) % 2 : 0, col = (p.view || 0) + f;
  const A = World.Avatar, S = A.compose(p.av), cp = KPX * ASC, w = A.FW * cp, h = A.FH * cp;
  const dx = Math.round((sx - camIX) * KPX), dy = Math.round((sy - camIY) * KPX - (A.FH - 1.5) * cp);
  cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
  if (p.flip){ cx.translate(dx, dy); cx.scale(-1, 1); cx.drawImage(S, col * A.FW, 0, A.FW, A.FH, -w / 2, 0, w, h); } else cx.drawImage(S, col * A.FW, 0, A.FW, A.FH, Math.round(dx - w / 2), dy, w, h);
  cx.restore();
}
function frame(now){
  const dt = Math.min(.05, (now - last) / 1000); last = now;
  people.forEach(p => step(p, dt));
  const A = MAPS[rmap];
  // 카메라 먼저: 맵이 화면보다 작으면 가운데에, 크면 내 캐릭터를 따라가요
  { const [mx, my] = P(me.x + .5, me.y + .5);
    const tx = M.W <= VW ? (M.W - VW) / 2 : Math.max(0, Math.min(M.W - VW, mx - VW / 2));
    const ty = M.H <= VH ? (M.H - VH) / 2 - 10 : Math.max(0, Math.min(M.H - VH, my - 14 - VH / 2));
    if (camX === null){ camX = tx; camY = ty; } camX += (tx - camX) * Math.min(1, dt * 8); camY += (ty - camY) * Math.min(1, dt * 8); }
  const ix = Math.round(camX), iy = Math.round(camY); camIX = ix; camIY = iy;
  const view = { x: ix - 4, y: iy - 4, w: VW + 8, h: VH + 8 };
  out.setTransform(KPX, 0, 0, KPX, 0, 0); out.fillStyle = M.fill || (M.indoor ? '#0C0715' : '#1E2A1C'); out.fillRect(0, 0, VW, VH);
  out.setTransform(KPX, 0, 0, KPX, -ix * KPX, -iy * KPX);
  const cx = out;
  cx.drawImage(A.bg, Math.max(0, ix), Math.max(0, iy), VW, VH, Math.max(0, ix), Math.max(0, iy), VW, VH);
  // 물결 반짝임
  if (M.water) for (let i = 0; i < 6; i++){ const w = M.water[(Math.random() * M.water.length) | 0]; const [wx, wy] = P(w[0] + Math.random(), w[1] + Math.random()); if (wx > view.x && wx < view.x + view.w && wy > view.y && wy < view.y + view.h) fx.push({ x: wx, y: wy, v: 0, life: .5, c: '#DFF2FF' }); }
  // 문 표시 (반짝이는 발판)
  const pulse = .5 + .5 * Math.sin(now / 300);
  M.objs.forEach(o => { if (!o.door) return; const [x, y] = P(o.door.tile[0] + .5, o.door.tile[1] + .5); cx.fillStyle = `rgba(255,216,102,${.25 + .35 * pulse})`; cx.beginPath(); cx.moveTo(x, y - 4); cx.lineTo(x + 8, y); cx.lineTo(x, y + 4); cx.lineTo(x - 8, y); cx.fill(); });
  // 바닥에 깔린 가구 (러그)
  flats.forEach(o => cx.drawImage(FURN_IMG, o.sx, 0, o.sw, o.sh, o.x, o.y, o.sw, o.sh));
  // 사람을 정렬된 물건 사이에 끼워 넣기
  const R = o => ({ x: o.x, y: o.y, w: o.sw, h: o.sh });
  const list = objOrder.filter(o => sOver(R(o), view)).map(o => ({ o }));
  [...people].sort((a, b) => (a.x + a.y) - (b.x + b.y)).forEach(p => {
    const [sx, sy] = P(p.x + .5, p.y + .5), pr = { x: sx - World.Avatar.FW * ASC / 2, y: sy - World.Avatar.FH * ASC, w: World.Avatar.FW * ASC, h: World.Avatar.FH * ASC + 1 }, pb = [p.x + .15, p.y + .15, p.x + .85, p.y + .85];
    let idx = 0; list.forEach((it, i) => { if (it.o && sOver(R(it.o), pr) && behind(it.o.box, pb)) idx = i + 1; });
    list.splice(idx, 0, { p });
  });
  list.forEach(it => it.o ? cx.drawImage(it.o.furn ? FURN_IMG : A.obj, it.o.sx, it.o.sy, it.o.sw, it.o.sh, it.o.x, it.o.y, it.o.sw, it.o.sh) : drawPerson(it.p));
  // 가구 놓기: 고른 자리에 반투명하게 미리 보여 줘요
  if (placing && placing.at){ const it = FURN.items[placing.k], [gx, gy] = placing.at, ok = canPlace(placing.k, gx, gy), [px, py] = P(gx, gy);
    cx.fillStyle = ok ? 'rgba(140,230,176,.45)' : 'rgba(230,90,110,.45)';
    for (let a = gx; a < gx + it.w; a++) for (let b = gy; b < gy + it.d; b++){ const [qx, qy] = P(a, b); cx.beginPath(); cx.moveTo(qx, qy); cx.lineTo(qx + 8, qy + 4); cx.lineTo(qx, qy + 8); cx.lineTo(qx - 8, qy + 4); cx.fill(); }
    cx.globalAlpha = .75; cx.drawImage(FURN_IMG, it.sx, 0, it.sw, it.sh, px - it.ax, py - it.ay, it.sw, it.sh); cx.globalAlpha = 1; }
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
  if (M.rooms) M.rooms.forEach((rm, i) => { const [sx, sy] = P(rm.door[0] + .5, rm.door[1] + .5); roomTags[i].style.left = (sx - ix) * k + 'px'; roomTags[i].style.top = (sy - 52 - iy) * k + 'px'; });
  if (M.pens) M.pens.forEach((pn, i) => { const [sx, sy] = P(pn.sign[0] + .5, pn.sign[1] + .5); penTags[i].style.left = (sx - ix) * k + 'px'; penTags[i].style.top = (sy - 20 - iy) * k + 'px'; });
  people.forEach((p, i) => { const [sx, sy] = P(p.x + .5, p.y + .5); tags[i].style.left = (sx - ix) * k + 'px'; tags[i].style.top = (sy - World.Avatar.FH * ASC + 4 - iy) * k + 'px'; });
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
  CR_IMG = await img(CR_SRC);
  FURN_IMG = await img(FURN.src); { const pc = document.createElement('canvas'); pc.width = FURN_IMG.width; pc.height = FURN_IMG.height; FURN_PX = pc.getContext('2d', { willReadFrequently: true }); FURN_PX.drawImage(FURN_IMG, 0, 0); }
  await Promise.all(Object.keys(MAPS).filter(id => !MAPS[id].meta.lazy).map(ensureMap));
})();
World.start = async (id = 'campus', spawn) => {
  await World.ready; if (started) return; started = true;
  await ensureMap(id); resize(); setMap(id, spawn || MAPS[real(id)].meta.start || MAPS[real(id)].meta.spawnIn);
  requestAnimationFrame(frame);
};
World.setPlayer = (name, av) => { me.name = name; me.av = av; if (tags[0]) tags[0].textContent = name; };
World.resize = () => { if (started){ resize(); camX = null; } };
World.where = () => map;
World.meta = id => MAPS[real(id)] && MAPS[real(id)].meta;
// 휴게실 단계: 그 기숙사 휴게실을 n단계 방으로 (지금 그 방에 있으면 바로 바꿔요)
World.setStage = async (base, n) => {
  const id = base + '_' + Math.max(1, Math.min(6, n)); if (!MAPS[id] || ALIAS[base] === id) return;
  ALIAS[base] = id; delete crowd[base];
  if (started && map === base){ const p = [Math.round(me.x), Math.round(me.y)]; await ensureMap(base); setMap(base, p); }
};
// 그 방의 물건 옆으로 순간 이동 (홈 화면의 바로 가기)
World.teleport = (id, objName, then) => {
  if (!started || busy) return;
  busy = true; fadeEl.textContent = MAPS[real(id)].meta.title; fadeEl.style.opacity = 1;
  ensureMap(id).then(() => setTimeout(() => {
    if (map !== id || (MAPS[real(id)].meta.furn && !roomView.own)){ backStack = []; roomView = { own: true }; setMap(id, MAPS[real(id)].meta.start || MAPS[real(id)].meta.spawnIn); }
    const o = M.objs.find(x => x.name === objName);
    if (o){ const tiles = []; for (let a = Math.floor(o.box[0]); a < Math.ceil(o.box[2]); a++) for (let b = Math.floor(o.box[1]); b < Math.ceil(o.box[3]); b++) tiles.push([a, b]); const c = near(tiles)[0]; if (c){ me.x = c[0]; me.y = c[1]; me.path = []; camX = null; } }
    setTimeout(() => { fadeEl.style.opacity = 0; busy = false; then && then(); }, 150);
  }, 380));
};
