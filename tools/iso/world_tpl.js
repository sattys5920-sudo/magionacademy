
// 걸어 다니는 세계 (tools/iso/build_halloween.py가 MAPS를 채워서 public/world.js로 써요)
// 게임(index.html)과는 window.World로 이어져요: World.start / setPlayer / teleport / onAct
const MAPS = __MAPS__;
const World = window.World = { onAct: null, onMove: null };
// art/iso·art/lpc·npcs·cast_animals 그림은 무손실 WebP로 받아요 (같은 이름 .webp, 60% 작음)
const webp = s => /^art\/(iso|lpc)\/|^art\/(npcs|cast_animals)\.png/.test(s) ? s.replace(/\.png(?=\?|$)/, '.webp') : s;
World.webp = webp;
// ---------- 캐릭터 조합 (LPC 부품: tools/iso/lpc/build_lpc.py) ----------
// av = { body: 체형(0 여·1 남), hair, face, top, legs, feet, cape, neck, hat, acc(액세서리): 부품 번호,
//        skinC, hairC, eyeC, legsC, feetC, topC(사복), hatC, accC: 색 번호, house: 넥타이·망토 안감 색이 될 기숙사 }
// 부품 그림은 필요할 때 불러와요 (art/lpc/*.png). 색은 LPC 팔레트를 바꿔 칠해요
const AVM = __AVATAR__;
const ASC = AVM.scale || .5;   // 캐릭터 그림 1픽셀 = 세계 픽셀의 몇 배
// 캐릭터 입 13종 (0 없음): 앞모습 6×3칸(x29~34, y32~34), 옆모습 3×3칸(왼쪽 보기 x25~27, 오른쪽은 거울)
// # 입술선(피부색을 어둡게) r 입속 w 이 t 혀 d 침
const MOUTHS = [
  { n: '없음' },
  { n: '미소', f: ['.#..#.', '..##..', '......'], s: ['#..', '.#.', '...'] },
  { n: '활짝', f: ['.####.', '.#rr#.', '..##..'], s: ['##.', 'r#.', '...'] },
  { n: '헤헤', f: ['.####.', '.#ww#.', '..##..'], s: ['##.', 'w#.', '...'] },
  { n: '아', f: ['..##..', '.#rr#.', '..##..'], s: ['.#.', '#r.', '.#.'] },
  { n: '오', f: ['......', '..##..', '..##..'], s: ['...', '.#.', '.#.'] },
  { n: '고양이', f: ['...#..', '..#.#.', '......'], s: ['.#.', '#..', '...'] },
  { n: '고양이 2', f: ['.#.#.#', '..#.#.', '......'], s: ['#.#', '.#.', '...'] },
  { n: '뾰로통', f: ['..##..', '.#..#.', '......'], s: ['.#.', '#..', '...'] },
  { n: '메롱', f: ['.####.', '...tt.', '...t..'], s: ['##.', 't..', 't..'] },
  { n: '송곳니', f: ['.####.', '.w..w.', '......'], s: ['##.', 'w..', '...'] },
  { n: '꾹', f: ['......', '.####.', '......'], s: ['...', '##.', '...'] },
  { n: '씩', f: ['....#.', '.###..', '......'], s: ['.#.', '#..', '...'] },
  { n: '당황', f: ['..#.#.', '.#.#..', '......'], s: ['.#.', '#.#', '...'] },
  { n: '헤벌쭉', f: ['.#..#.', '..##..', '....d.'], s: ['#..', '.#.', 'd..'] },
];
const MOUTH_DY = [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0];   // 걷기 칸마다 머리가 1px 내려가는 칸
function drawMouth(o, W, FW, m){   // o: ImageData.data (가로 W = FW×20)
  const M = MOUTHS[m]; if (!M || !M.f) return;
  const P = (x, y) => (y * W + x) * 4;
  const skinAt = (col, x, y) => { const d = P(col * FW + x, y); return o[d + 3] ? [o[d], o[d + 1], o[d + 2]] : null; };
  for (let col = 0; col < 20; col++){
    if (col >= 5 && col < 10) continue;   // 뒷모습
    const dy = MOUTH_DY[col], side = col >= 10, right = col >= 15;
    const sk = skinAt(col, side ? (right ? 36 : 27) : 31, 33 + dy) || skinAt(col, 31, 32 + dy); if (!sk) continue;
    const C = { '#': [sk[0] * .5 + 8, sk[1] * .27, sk[2] * .3], r: [122, 34, 54], w: [255, 246, 236], t: [232, 112, 126], d: [150, 210, 255] };
    const g = side ? M.s : M.f;
    g.forEach((row, ry) => [...row].forEach((ch, rx) => {
      if (ch === '.') return; const x = side ? (right ? 38 - rx : 25 + rx) : 29 + rx, y = 32 + ry + dy, d = P(col * FW + x, y);
      if (!o[d + 3]) return;   // 얼굴 밖은 안 그려요
      const c = C[ch]; o[d] = c[0]; o[d + 1] = c[1]; o[d + 2] = c[2];
    }));
  }
}
World.Avatar = (() => {
  const FW = AVM.fw, FH = AVM.fh, NF = AVM.frames, CATS = ['hair', 'face', 'top', 'legs', 'feet', 'cape', 'neck', 'hat', 'acc'], HOUSES = Object.keys(AVM.house);
  const COLORS = { skinC: 'skin', hairC: 'hair', eyeC: 'eye', legsC: 'bottom', feetC: 'shoe', topC: 'cloth', hatC: 'cloth', accC: 'cloth' };   // topC: 사복·잠옷 색   // 색 키 → 고를 수 있는 색 목록
  const SLOTC = { skin: 'skinC', hair: 'hairC', eye: 'eyeC', legs: 'legsC', feet: 'feetC', cas: 'topC', hat: 'hatC', acc: 'accC' };
  const MAT = { skin: 'skin', eye: 'eye', hair: 'hair', top: 'cloth', legs: 'bottom', feet: 'shoe', hat: 'cloth', acc: 'cloth' };
  let lastOwn = null;   // 검증용 (tools/iso/lpc/verify_legs.js)
  const imgs = {}, cache = new Map(), heads = new Map(), maps = new Map(), subs = [];
  const bodyName = av => AVM.bodies[av.body] || AVM.bodies[0];
  function load(f){
    if (!f) return Promise.resolve();
    if (imgs[f]) return imgs[f].p;
    const e = imgs[f] = { data: null };
    e.p = new Promise(r => { const i = new Image(); i.onload = () => { const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0); e.data = g.getImageData(0, 0, i.width, i.height); cache.clear(); heads.clear(); subs.forEach(fn => fn()); r(); }; i.onerror = () => r(); i.src = webp(f); });
    return e.p;
  }
  const ready = load(AVM.parts.body[0].f);
  AVM.parts.lip = MOUTHS.map((M, i) => ({ id: 'lip' + i, n: M.n, f: null, L: {} }));   // 입: 그림 파일 없이 compose에서 그려요 (av.lip)
  const mod = (v, n) => ((v | 0) % n + n) % n;
  const has = (cat, i, body) => { const p = AVM.parts[cat][i]; return p && (p.f === null || !!p.L[body]); };
  function fix(av){
    const a = Object.assign({}, av || {});
    if (a.face === undefined && a.eyes !== undefined) a.face = a.eyes;   // 옛 캐릭터 (눈 번호 → 표정)
    a.body = mod(a.body, AVM.bodies.length); const body = AVM.bodies[a.body];
    CATS.forEach(c => { const n = AVM.parts[c].length; let i = mod(a[c], n); for (let k = 0; k < n && !has(c, i, body); k++) i = (i + 1) % n; a[c] = i; });
    Object.entries(COLORS).forEach(([k, p]) => { a[k] = mod(a[k], AVM.colors[p].length); });
    a.lip = mod(a.lip, MOUTHS.length);   // 입 (예전 캐릭터는 0 = 없음)
    if (!HOUSES.includes(a.house)) delete a.house;
    delete a.eyes; delete a.mouth; delete a.uni; delete a.shoeC; delete a.neckC;
    return a;
  }
  const rnd = seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  function fromLook(look){
    const r = rnd(((look | 0) + 7) * 9973 + 1), a = { body: Math.floor(r() * 2) };
    CATS.forEach(c => { const ok = AVM.parts[c].map((p, i) => i).filter(i => !AVM.parts[c][i].k || AVM.parts[c][i].k === 'uni'); a[c] = ok[Math.floor(r() * ok.length)]; });   // 다른 학생은 교복
    a.cape = r() < .6 ? 0 : a.cape; a.hat = 0; a.acc = 0; a.neck = r() < .3 ? 0 : a.neck; a.face = r() < .6 ? 0 : a.face;
    Object.entries(COLORS).forEach(([k, p]) => { a[k] = Math.floor(r() * AVM.colors[p].length); });
    a.skinC = Math.floor(r() * 7);
    a.lip = r() < .5 ? 1 : 1 + Math.floor(r() * (MOUTHS.length - 1));   // 새 캐릭터·다른 학생은 입이 있어요 (반은 기본 미소)
    a.legsC = Math.floor(r() * 3); a.feetC = Math.floor(r() * 2);   // 교복은 다들 비슷하게: 하의 차콜·검정·남색, 구두 검정·갈색
    return fix(a);
  }
  const random = () => ({ ...fromLook(Math.floor(Math.random() * 1e6)), house: HOUSES[Math.floor(Math.random() * HOUSES.length)] });
  const hexn = h => parseInt(h.slice(1), 16);
  function colorMap(slot, src, av){
    const mat = MAT[slot] || 'cloth';
    const tgtName = slot === 'top' ? AVM.house[HOUSES.includes(av.house) ? av.house : 'moon'] : slot.startsWith('fix:') ? slot.slice(4) : AVM.fixed[slot] || AVM.colors[mat][av[SLOTC[slot]] || 0];   // fix:색 = 정해진 색
    const k = slot + '|' + src + '|' + tgtName; if (maps.has(k)) return maps.get(k);
    const P = AVM.pal[mat], S = P[src] || [], T = P[tgtName] || S, m = new Map();
    S.forEach((h, i) => { const t = hexn(T[Math.min(i, T.length - 1)]); m.set(hexn(h), [t >> 16, (t >> 8) & 255, t & 255]); });
    maps.set(k, m); return m;
  }
  function layersOf(av){
    const body = bodyName(av), out = [];
    ['body', ...CATS].forEach(c => { const p = AVM.parts[c][c === 'body' ? 0 : av[c]]; if (p && p.f) (p.L[body] || []).forEach(([row, z, mp]) => out.push({ f: p.f, row, z, mp, shoe: c === 'feet' && z >= 15, sk: !!(p.sk && p.sk.includes(z)) })); });
    return out.sort((a, b) => a.z - b.z);
  }
  // 다리 Y존 (앞·뒤 모습): 두 다리 사이 진한 틈(외곽선·진한 그림자·빈칸)을 그 줄에서 가장 많이 쓰인 바지 색으로 메우고,
  // 다리 가운데 1열(meta.leg)에 가랑이 2줄 아래부터 신발 바로 위까지 1px 세로선 = 그 픽셀 색 70% 밝기.
  // 치마·원피스 천이 덮은 줄은 건너뛰어요 (선은 밑단 바로 아래 줄부터). legline 2면 신발 바로 위 3줄은 외곽선색
  const LUM = (r, g, b) => .299 * r + .587 * g + .114 * b;
  function legFix(o, own, W){
    Object.entries(AVM.leg || {}).forEach(([k, [lc, crotch]]) => {
      const X0 = +k * FW, xc = X0 + lc, P = (y, x) => (y * W + x) * 4;
      let top = FH;
      for (let y = crotch + 2; y < FH; y++) if (own[y * W + xc] === 1){ top = y; break; }
      for (let y = crotch; y < top; y++){
        const cnt = new Map();
        for (let x = X0; x < X0 + FW; x++){ const d = P(y, x); if (!o[d + 3] || own[y * W + x]) continue; const l = LUM(o[d], o[d + 1], o[d + 2]); if (l < 45) continue; const key = (o[d] << 16) | (o[d + 1] << 8) | o[d + 2]; cnt.set(key, (cnt.get(key) || 0) + 1); }
        if (!cnt.size) for (let x = X0; x < X0 + FW; x++){ const d = P(y, x); if (!o[d + 3] || own[y * W + x]) continue; const key = (o[d] << 16) | (o[d + 1] << 8) | o[d + 2]; cnt.set(key, (cnt.get(key) || 0) + 1); }   // 아주 진한 바지 (검정 등)
        if (!cnt.size) continue;
        const ls = []; cnt.forEach((n, key) => { for (let i = 0; i < n; i++) ls.push(LUM(key >> 16, (key >> 8) & 255, key & 255)); }); ls.sort((a, b) => a - b);
        const med = ls[ls.length >> 1];   // 가장 많이 쓰인 색 (같으면 그 줄 가운데 밝기에 가까운 색)
        let mode = 0, best = -1e9; cnt.forEach((n, key) => { const sc = n * 1000 - Math.abs(LUM(key >> 16, (key >> 8) & 255, key & 255) - med); if (sc > best){ best = sc; mode = key; } });
        const mr = mode >> 16, mg = (mode >> 8) & 255, mb = mode & 255, ml = LUM(mr, mg, mb);
        const dark = x => { const d = P(y, x); return !o[d + 3] || LUM(o[d], o[d + 1], o[d + 2]) < Math.max(45, ml * .65); };   // 외곽선·진한 그림자(그 줄 바지색의 65% 미만)·빈칸
        // Y존: 다리 가운데의 진한 틈을 양옆 다리 픽셀 사이(가운데 ±4칸 안)만큼 메워요
        const legAt = x => { const d = P(y, x); return o[d + 3] && !own[y * W + x] && !dark(x); };
        if (!own[y * W + xc]){
          let Lx = -1, Rx = -1;
          for (let x = xc; x >= xc - 4; x--) if (legAt(x)){ Lx = x; break; }
          for (let x = xc; x <= xc + 4; x++) if (legAt(x)){ Rx = x; break; }
          if (Lx >= 0 && Rx >= 0 && Rx - Lx > 1) for (let x = Lx + 1; x < Rx; x++){ const d = P(y, x); o[d] = mr; o[d + 1] = mg; o[d + 2] = mb; o[d + 3] = 255; }
        }
        const d = P(y, xc);
        if (y < crotch + 2 || own[y * W + xc] || !o[d + 3]) continue;
        if (AVM.legline === 2 && top < FH && y >= top - 3){ o[d] = 40; o[d + 1] = 24; o[d + 2] = 32; continue; }
        if (dark(xc)) continue;   // 밑단 외곽선 줄
        o[d] = o[d] * .7; o[d + 1] = o[d + 1] * .7; o[d + 2] = o[d + 2] * .7;
      }
      // 신발(부츠)끼리 붙은 줄: 두 짝 사이 검은 틈은 신발색으로 메우고 가운데 1px만 60% 밝기 (두 짝은 그대로, 검은 Y자 틈만 없애기)
      let sole = -1; for (let y = FH - 1; y >= crotch; y--){ let any = false; for (let x = X0; x < X0 + FW; x++) if (own[y * W + x] === 1){ any = true; break; } if (any){ sole = y; break; } }
      for (let y = crotch; y < FH; y++){
        const cnt = new Map(), bottom = y >= sole - 1;   // 신발 맨 아래 2줄 = 발바닥 쪽: 두 발 사이 빈칸은 그대로
        for (let x = X0; x < X0 + FW; x++){ const d = P(y, x); if (!o[d + 3] || own[y * W + x] !== 1 || LUM(o[d], o[d + 1], o[d + 2]) < 45) continue; const key = (o[d] << 16) | (o[d + 1] << 8) | o[d + 2]; cnt.set(key, (cnt.get(key) || 0) + 1); }
        if (!cnt.size) continue;
        let mode = 0, best = -1; cnt.forEach((n, key) => { if (n > best){ best = n; mode = key; } });
        const ml = LUM(mode >> 16, (mode >> 8) & 255, mode & 255);
        const dk = x => { const d = P(y, x); return !o[d + 3] || LUM(o[d], o[d + 1], o[d + 2]) < Math.max(45, ml * .65); };
        const shoeAt = x => own[y * W + x] === 1 && !dk(x);
        let Lx = -1, Rx = -1;
        for (let x = xc; x >= xc - 4; x--) if (shoeAt(x)){ Lx = x; break; }
        for (let x = xc + 1; x <= xc + 4; x++) if (shoeAt(x)){ Rx = x; break; }
        if (Lx < 0 || Rx < 0 || Rx - Lx < 2) continue;
        let ok = true; for (let x = Lx + 1; x < Rx; x++){ const d = P(y, x); if ((bottom && !o[d + 3]) || !dk(x) || own[y * W + x] === 2) ok = false; }
        if (!ok) continue;
        for (let x = Lx + 1; x < Rx; x++){ const d = P(y, x); o[d] = mode >> 16; o[d + 1] = (mode >> 8) & 255; o[d + 2] = mode & 255; o[d + 3] = 255; }
        const d = P(y, xc); o[d] = (mode >> 16) * .6; o[d + 1] = ((mode >> 8) & 255) * .6; o[d + 2] = (mode & 255) * .6;   // 두 짝은 그대로 보이게 가운데 1px만 어둡게
      }
    });
  }
  // 부품 그림이 다 오면 resolve (캐릭터 꾸미기 화면 썸네일 전에)
  const need = av => Promise.all(layersOf(fix(av)).map(l => load(l.f)));
  const preload = cats => Promise.all(cats.flatMap(c => (AVM.parts[c] || []).filter(p => p.f).map(p => load(p.f))));
  function compose(av){
    av = fix(av); const key = JSON.stringify(av); if (cache.has(key)) return cache.get(key);
    const W = FW * NF, out = new ImageData(W, FH), o = out.data; let done = true;
    const own = new Uint8Array(W * FH);   // 칸마다 맨 위 층: 1 신발, 2 치마·원피스 천 (다리 Y존·세로선용)
    layersOf(av).forEach(L => {
      const e = imgs[L.f]; if (!e || !e.data){ load(L.f); done = false; return; }
      const src = e.data.data, SW = e.data.width, ms = L.mp.map(([slot, sp]) => colorMap(slot, sp, av));
      for (let y = 0; y < FH; y++) for (let x = 0; x < W; x++){
        const s = ((L.row * FH + y) * SW + x) * 4, a = src[s + 3]; if (!a) continue;
        let r = src[s], g = src[s + 1], b = src[s + 2];
        const kk = (r << 16) | (g << 8) | b;
        for (const m of ms){ const t = m.get(kk); if (t){ [r, g, b] = t; break; } }
        const d = (y * W + x) * 4;
        if (a < 255 && o[d + 3]){ const t = a / 255; o[d] += (r - o[d]) * t; o[d + 1] += (g - o[d + 1]) * t; o[d + 2] += (b - o[d + 2]) * t; continue; }
        o[d] = r; o[d + 1] = g; o[d + 2] = b; o[d + 3] = 255;
        own[y * W + x] = L.shoe ? 1 : L.sk ? 2 : 0;
      }
    });
    legFix(o, own, W); drawMouth(o, W, FW, av.lip || 0); lastOwn = own;
    const c = document.createElement('canvas'); c.width = W; c.height = FH; c.getContext('2d').putImageData(out, 0, 0);
    if (done) cache.set(key, c);
    return c;
  }
  // 얼굴 동그라미용 (정면 서기 프레임의 머리 부분)
  const HB = AVM.head;
  function head(av){
    if (!imgs[AVM.parts.body[0].f] || !imgs[AVM.parts.body[0].f].data) return '';
    const key = JSON.stringify(fix(av)); if (heads.has(key)) return heads.get(key);
    const S = compose(av), c = document.createElement('canvas'); c.width = HB.s; c.height = HB.s; c.getContext('2d').drawImage(S, HB.x, HB.y, HB.s, HB.s, 0, 0, HB.s, HB.s);
    const u = c.toDataURL(); if (cache.has(JSON.stringify(fix(av)))) heads.set(key, u); return u;
  }
  const onLoad = fn => subs.push(fn);
  return { ready, compose, debugOwn: () => lastOwn, clear: () => { cache.clear(); heads.clear(); }, head, fix, fromLook, random, need, preload, onLoad, meta: AVM, FW, FH, CATS, HOUSES, headBox: { x: HB.x, y: HB.y, s: HB.s },
           get loaded(){ return !!(imgs[AVM.parts.body[0].f] && imgs[AVM.parts.body[0].f].data); } };
})();
let sc;
// 배율: 그림 1픽셀 = 화면 실제 픽셀의 정수배(k)로 그려서 선명하게. 목표 가로 픽셀 수에 가장 가까운 k를 골라요.
const ZOOMS = [['보통', 300], ['멀리', 420], ['가까이', 210]];
let zi = 0, VW = 300, KPX = 1, viewOverride = null;
World.setView = vw => { viewOverride = vw || null; if (started){ resize(); camX = null; } };   // 요리처럼 가까이 볼 때 (null이면 원래대로)
const cv = document.getElementById('cv'), out = cv.getContext('2d');
const world = document.getElementById('world'), fadeEl = document.getElementById('fade');
let VH = 220;
function resize(){
  const dpr = window.devicePixelRatio || 1, dw = world.clientWidth * dpr, dh = world.clientHeight * dpr;
  const target = viewOverride || ((M && M.vw && zi !== 1) ? M.vw : ZOOMS[zi][1]);
  // 캐릭터 그림은 세계의 ASC배: KPX × ASC 가 정수여야 픽셀이 고르게 보여요 (홀수 배면 줄이 두 겹씩 섞여 길쭉해 보여요)
  const step = Math.max(1, Math.round(1 / ASC)); KPX = Math.max(step, Math.round(dw / target / step) * step);
  VW = Math.ceil(dw / KPX); VH = Math.ceil(dh / KPX);
  cv.width = VW * KPX; cv.height = VH * KPX;   // 캔버스는 기기 픽셀 그대로: 세계는 KPX배, 캐릭터는 더 촘촘하게 그려요
  cv.style.width = (VW * KPX / dpr) + 'px'; cv.style.height = (VH * KPX / dpr) + 'px';
  out.imageSmoothingEnabled = false;
}
addEventListener('resize', resize);
const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = webp(s); });
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
    if (!m.meta.indoor){   // 바깥 맵: 그림에 칠해진 어두운 빈 땅(#140E1E)을 투명하게 → 그 자리에 시간대 하늘색이 보여요
      const bc = document.createElement('canvas'); bc.width = bg.width; bc.height = bg.height; const bx = bc.getContext('2d', { willReadFrequently: true }); bx.drawImage(bg, 0, 0);
      const id = bx.getImageData(0, 0, bc.width, bc.height), d = id.data, hx = m.meta.fill || '#140E1E', R = parseInt(hx.slice(1, 3), 16), G = parseInt(hx.slice(3, 5), 16), B = parseInt(hx.slice(5, 7), 16);
      for (let i = 0; i < d.length; i += 4) if (d[i] === R && d[i + 1] === G && d[i + 2] === B) d[i + 3] = 0;
      bx.putImageData(id, 0, 0); m.bg = bc;
    }
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
// 같은 곳에 있는 친구들 (실시간 위치). 다른 사람 화면에서는 내가 이렇게 보여요
const peers = {}; let peerList = [];
// 이름표는 캔버스에 그려요 (DOM을 매 프레임 옮기지 않아요). tags[i] = { t: 글, k: 종류(me·peer·npc·''), ev: 이벤트 표시 }
function retag(){ tags = people.map(p => p.pet || (p.npc && p.npc.cut && !p.name) ? null : { t: (p.npc && p.npc.mark ? '❗' : '') + p.name, k: p.me ? 'me' : p.peer ? 'peer' : p.npc ? 'npc' : '', ev: !!(p.npc && p.npc.mark) }); }
const TAG_COL = { me: '#FFD866', peer: '#9CF0FF', npc: '#F6F0FF', '': '#F6F0FF' }, tagW = new Map();
let dpr = 1;
function drawTag(tag, sx, sy, now){   // sx, sy: 세계 픽셀(이름표 아래 가운데). 화면 좌표계(setTransform 1)에서 불러요
  if (!tag) return;
  const f = Math.round(13 * dpr), px = Math.round(5 * dpr), py = Math.round(3 * dpr), r = Math.round(4 * dpr);
  out.font = `${f}px G11, Pretendard, sans-serif`; let w = tagW.get(tag.t + f); if (w === undefined){ w = Math.ceil(out.measureText(tag.t).width); tagW.set(tag.t + f, w); }
  const x = Math.round((sx - camIX) * KPX - w / 2 - px), y = Math.round((sy - camIY) * KPX - f - py * 2), W = w + px * 2, H = f + py * 2;
  out.fillStyle = 'rgba(20,13,30,.8)'; out.beginPath(); out.roundRect(x, y, W, H, r); out.fill();
  if (tag.k === 'peer' || tag.ev){ out.strokeStyle = tag.ev ? '#FFD866' : '#4FB8D8'; out.lineWidth = dpr; if (!tag.ev || Math.floor(now / 600) % 2 === 0) out.stroke(); }
  out.fillStyle = tag.ev ? '#FFD866' : TAG_COL[tag.k]; out.textBaseline = 'top'; out.textAlign = 'left'; out.fillText(tag.t, x + px, y + py + Math.round(dpr));
}
// 지금 있는 곳 열쇠: 개인 방은 방 주인마다 달라요
const placeKey = () => map + (M && M.furn ? ':' + (roomView.own ? World.myUid : roomView.uid) : '');
World.placeKey = () => started ? placeKey() : null;
World.myPos = () => { const t = me.path.length ? me.path[me.path.length - 1] : [Math.round(me.x), Math.round(me.y)]; return { m: placeKey(), x: t[0], y: t[1] }; };
World.setPeers = list => { peerList = list || []; if (started && M) syncPeers(); };
const peerSpot = q => free(q.x, q.y) ? [q.x, q.y] : [Math.round(me.x), Math.round(me.y)];
function addPeer(q){ const [x, y] = peerSpot(q), p = mk(q.name, q.av, x, y, false); p.peer = q.uid; peers[q.uid] = p; people.push(p); }
function syncPeers(){
  const key = placeKey(), here = peerList.filter(q => q.m === key && q.uid !== World.myUid);
  let changed = false;
  Object.keys(peers).forEach(id => { if (!here.find(q => q.uid === id)){ const i = people.indexOf(peers[id]); if (i >= 0) people.splice(i, 1); sayOff(peers[id]); delete peers[id]; changed = true; } });
  here.forEach(q => {
    const p = peers[q.uid];
    if (!p){ addPeer(q); changed = true; return; }
    if (p.name !== q.name){ p.name = q.name; changed = true; }
    p.av = q.av;
    const [tx, ty] = peerSpot(q), g = p.path.length ? p.path[p.path.length - 1] : [Math.round(p.x), Math.round(p.y)];
    if (g[0] !== tx || g[1] !== ty){ if (Math.hypot(tx - p.x, ty - p.y) > 25 || !goto(p, tx, ty)){ p.x = tx; p.y = ty; p.path = []; } }
  });
  if (changed) retag();
}
// 머리 위 말풍선 (채팅·이모티콘). 몇 초 뒤에 사라져요
const says = [];
function sayOff(p){ if (p && p.say){ p.say.el.remove(); const i = says.indexOf(p); if (i >= 0) says.splice(i, 1); p.say = null; } }
World.say = (id, text, big) => {   // big: 이모티콘 번호(art/emo.png 칸)면 그림으로
  const p = id === World.myUid || id === 'me' ? me : peers[id]; if (!p || !text) return;
  sayOff(p);
  const emo = typeof big === 'number' ? big : null, d = document.createElement('div'); d.className = 'say' + (emo !== null ? ' emo' : '');
  if (emo !== null){ const i = document.createElement('i'); i.className = 'emi'; i.style.setProperty('--i', emo); d.appendChild(i); } else d.textContent = text;
  world.appendChild(d); p.say = { el: d, until: performance.now() + (emo !== null ? 3500 : 5500) }; says.push(p);
};
World.onPeer = null;   // (친구 uid) 친구를 눌렀을 때
World.peerAt = id => { const p = peers[id]; if (!p) return null; return { get x(){ return P(p.x + .5, p.y + .5)[0]; }, get y(){ return P(p.x + .5, p.y + .5)[1] - World.Avatar.FH * ASC + 2; }, sw: 0 }; };   // 친구를 따라 움직여요
// 칸으로 걸어가요 (같은 맵일 때). 목적지에 작은 표시가 떠요
let dest = null;
World.walkToTile = (x, y) => { if (!started || busy) return false; const c = free(x, y) ? [x, y] : near([[x, y]])[0]; if (!c) return false; if (goto(me, c[0], c[1])){ dest = { x: c[0], y: c[1], t0: performance.now() }; return true; } return false; };
World.walkTo = id => { const p = peers[id]; if (!p) return; const c = near([[Math.round(p.x), Math.round(p.y)]])[0]; if (c) goto(me, c[0], c[1]); };
World.bubble = (o, text, btn, fn) => showBubble(o, text, btn, fn);
World.hideBubble = () => hideBubble();
// ---------- 낚시 · 채집 ----------
// 물을 누르면 물가로 걸어가서 World.onWater(물 x, y), 반짝이는 채집 지점을 누르면 그 칸으로 가서 World.onSpot(번호)
World.onWater = null; World.onSpot = null;
let bobber = null, spots = [], spotMap = null;
const isWater = (x, y) => !!(M && M.water && M.water.some(w => w[0] === x && w[1] === y));
World.setBobber = b => { bobber = b; };   // { x, y, bite } 물 칸에 찌 (없애려면 null)
World.setSpots = (mapId, list) => { spotMap = mapId; spots = list || []; };
World.getSpots = () => spotMap === map ? spots : [];   // [{ x, y, k }] k: 그림 칸(없으면 반짝이만)
World.faceTo = (x, y) => { const DV = World.Avatar.meta.dirs, dx = x - me.x, dy = y - me.y; me.view = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? DV.right : DV.left) : (dy < 0 ? DV.up : DV.down); me.flip = false; };
// 요리: 솥(물건 이름 + 칸) 위에 국물·김·거품·날아드는 재료·국자·불빛을 세계 픽셀 크기로 그려요
let cook = null, cookImg = {};
World.setCook = c => { cook = c; if (c && c.drop && c.drop.src && !cookImg[c.drop.src]){ const im = new Image(); im.src = c.drop.src; cookImg[c.drop.src] = im; } };
World.cookPot = () => { const o = M && M.objs.find(o => o.name === 'cauldron' && Math.abs(o.box[0] - me.x) + Math.abs(o.box[1] - me.y) < 4); return o ? { x: o.box[0], y: o.box[1] } : null; };
// 날씨: 비·폭풍·안개·눈 (바깥에서만)
let weather = null, wx = [], flashT = 0;
World.setWeather = w => { if (w !== weather){ weather = w; wx = []; } };
function drawWeather(cx, ix, iy, dt){
  if (!weather || weather === 'clear' || M.indoor) return;
  const rain = weather === 'rain' || weather === 'storm', n = weather === 'storm' ? 160 : rain ? 90 : weather === 'snow' ? 70 : 0;
  while (wx.length < n) wx.push({ x: Math.random() * (VW + 40) - 20, y: Math.random() * VH, v: .7 + Math.random() * .6, p: Math.random() * 6 });
  cx.save();
  if (rain){ cx.strokeStyle = 'rgba(180,200,255,.45)'; cx.lineWidth = 1; cx.beginPath();
    wx.forEach(d => { d.y += 260 * d.v * dt; d.x -= 50 * d.v * dt; if (d.y > VH){ d.y -= VH + 10; d.x = Math.random() * (VW + 40) - 20; } const X = Math.round(ix + d.x) + .5, Y = Math.round(iy + d.y); cx.moveTo(X, Y); cx.lineTo(X - 2, Y + 6); }); cx.stroke();
    if (weather === 'storm'){ flashT -= dt; if (flashT < -6 - Math.random() * 8) flashT = .25; if (flashT > 0){ cx.fillStyle = `rgba(230,235,255,${flashT * 1.6})`; cx.fillRect(ix, iy, VW, VH); } } }
  if (weather === 'snow'){ cx.fillStyle = 'rgba(255,255,255,.85)';
    wx.forEach(d => { d.y += 22 * d.v * dt; d.p += dt; if (d.y > VH){ d.y -= VH + 4; d.x = Math.random() * (VW + 40) - 20; } cx.fillRect(Math.round(ix + d.x + Math.sin(d.p) * 3), Math.round(iy + d.y), 1, 1); }); }
  if (weather === 'fog'){ const t = performance.now() / 1000; cx.fillStyle = 'rgba(205,200,225,.16)'; cx.fillRect(ix, iy, VW, VH);
    for (let i = 0; i < 4; i++){ cx.fillStyle = 'rgba(220,215,235,.10)'; cx.beginPath(); cx.ellipse(ix + ((i * 97 + t * 6) % (VW + 120)) - 60, iy + VH * (.2 + i * .2), 90, 14, 0, 0, Math.PI * 2); cx.fill(); } }
  cx.restore();
}
World.setMe = (x, y) => { me.x = x; me.y = y; me.path = []; };
let speedK = 1; World.setSpeedK = k => { speedK = k || 1; };   // 요리 효과: 빠른 걸음
// ---------- 이야기 NPC: 한자리에 서 있어요. 사람은 아바타(av), 동물은 그림(spr: art 칸) ----------
let npcList = [], NPC_IMG = null;
World.onNpc = null;   // (npc id) 눌렀을 때
let PIX_IMG = null;   // 조연 동물 그림 (32칸)
World.setNpcs = (list, sprSrc, pixSrc) => { npcList = list || []; if (sprSrc && (!NPC_IMG || NPC_IMG.src.indexOf(webp(sprSrc)) < 0)){ NPC_IMG = new Image(); NPC_IMG.src = webp(sprSrc); } if (pixSrc && !PIX_IMG){ PIX_IMG = new Image(); PIX_IMG.src = webp(pixSrc); } if (started && M){ placeNpcs(); retag(); } };
function placeNpcs(){
  for (let i = people.length - 1; i >= 0; i--) if (people[i].npc && !people[i].npc.cut) people.splice(i, 1);
  npcList.filter(n => (n.map === map || n.map === rmap) && (!n.own || roomView.own)).forEach(n => {
    let x = n.x, y = n.y;
    if (!free(x, y)){ outer: for (let r = 1; r < 4; r++) for (let dx = -r; dx <= r; dx++) for (let dy = -r; dy <= r; dy++) if (free(x + dx, y + dy)){ x += dx; y += dy; break outer; } }
    const p = mk(n.name, n.av || null, x, y, false); p.npc = n; p.home = [x, y]; p.idle = 2 + Math.random() * 5; p.view = World.Avatar.meta.dirs[n.dir || 'down'] || 0; people.push(p); if (!n.wander) blocked.add(x + ',' + y);
  });
}
World.npcAt = id => { const p = people.find(q => q.npc && q.npc.id === id); if (!p) return null; return { get x(){ return P(p.x + .5, p.y + .5)[0]; }, get y(){ return P(p.x + .5, p.y + .5)[1] - World.Avatar.FH * ASC + 2; }, sw: 0 }; };
World.busyFish = false;   // 낚시하는 동안은 바닥을 눌러도 안 걸어가요
World.isFree = (x, y) => !!M && free(x, y);
World.freeNear = (x, y, r = 3) => { const out = []; for (let a = x - r; a <= x + r; a++) for (let b = y - r; b <= y + r; b++) if (free(a, b)) out.push([a, b]); return out; };
let crowd = {};
function rebuildObjs(){   // 지도 물건 + (개인 방이면) 놓은 가구
  const fo = M.furn ? furnObjs() : [];
  blocked = new Set(M.water ? M.water.map(w => w[0] + ',' + w[1]) : []); [...M.objs, ...fo].forEach(o => { if (o.solid !== false) for (let x = Math.floor(o.box[0]); x < Math.ceil(o.box[2]); x++) for (let y = Math.floor(o.box[1]); y < Math.ceil(o.box[3]); y++) blocked.add(x + ',' + y); });
  flats = fo.filter(o => o.flat);
  objOrder = fo.length ? orderObjs([...M.objs, ...fo.filter(o => !o.flat)]) : (MAPS[rmap].order || (MAPS[rmap].order = orderObjs(M.objs)));
}
function setMap(id, spawn){
  map = id; rmap = real(id); M = MAPS[rmap].meta; resize(); placing = null;
  rebuildObjs();
  if (!spawn || !free(spawn[0], spawn[1])) spawn = M.spawnIn || M.start || spawn;
  me.x = spawn[0]; me.y = spawn[1]; me.path = []; me.view = 0; me.flip = false;
  // 의미 없이 걸어 다니는 학생은 없어요 (이야기 NPC는 따로: World.setNpcs)
  if (!crowd[id]){ crowd[id] = []; const n = 0; for (let i = 0; i < n; i++){ for (let k = 0; k < 50; k++){ const x = Math.floor(Math.random() * M.NX), y = Math.floor(Math.random() * M.NY); if (free(x, y)){ crowd[id].push(mk(NAMES[(i + (id === 'lab' ? 3 : 0)) % NAMES.length], World.Avatar.random(), x, y, false)); break; } } } }
  people.length = 0; people.push(me, ...crowd[id]);
  if (M.pets) people.push(...spawnPets());
  placeNpcs();
  Object.keys(peers).forEach(id => { sayOff(peers[id]); delete peers[id]; }); sayOff(me);
  peerList.filter(q => q.m === placeKey() && q.uid !== World.myUid).forEach(addPeer);
  retag();
  roomTags = M.rooms ? M.rooms.map(rm => { const nm = (hallNames[M.house] || [])[rm.i]; return { t: nm || '빈 방', k: nm && nm === me.name ? 'me' : '' }; }) : [];
  penTags = M.pens ? M.pens.map(pn => ({ t: penNames[pn.i] || '빈 우리', k: pn.i === myPen ? 'me' : '' })) : [];
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
World.setHallNames = names => { hallNames = names || {}; if (M && M.rooms) roomTags.forEach((t, i) => { t.t = (hallNames[M.house] || [])[M.rooms[i].i] || '빈 방'; }); };
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
World.setPenLabels = (names, mine) => { penNames = names; myPen = mine; penTags.forEach((t, i) => { t.t = names[M.pens[i].i] || '빈 우리'; t.k = M.pens[i].i === mine ? 'me' : ''; }); };
World.setPenExit = spawn => { const ex = MAPS.pen && MAPS.pen.meta.objs.find(o => o.name === 'exit'); if (ex) ex.door.spawn = spawn; };
World.setPets = list => {
  petData = list;
  if (!M || !M.pets) return;
  const keep = people.filter(p => !p.pet), add = spawnPets();
  people.length = 0; people.push(...keep, ...add);
  retag();
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
const clockEl = document.getElementById('clock'); let clockTick = 0, clockLast = '';
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
  if (typeof r === 'string'){ if (bubble) bubble.el.innerHTML = r; else showBubble(o, r); } else hideBubble();
}
// ---- 근처 대상(상황 버튼): 서 있는 칸에서 바로 닿는 NPC·채집 지점·물건·물가를 찾아 World.onNear(대상 | null)에 알려요 ----
World.onNear = null; let nearKey = '', nearT = null, nearTick = 0;
function findNear(){
  if (busy || !M || placing) return null;
  const mx = Math.round(me.x), my = Math.round(me.y);
  const np = people.filter(p => p.npc && Math.abs(Math.round(p.x) - mx) + Math.abs(Math.round(p.y) - my) <= 1).sort((a, b) => (Math.abs(a.x - mx) + Math.abs(a.y - my)) - (Math.abs(b.x - mx) + Math.abs(b.y - my)))[0];
  if (np) return { kind: 'npc', id: np.npc.id, name: np.name, key: 'n' + np.npc.id };
  if (spotMap === map){ const si = spots.findIndex(sp => Math.abs(sp.x - mx) + Math.abs(sp.y - my) <= 1); if (si >= 0) return { kind: 'spot', i: si, sp: spots[si], key: 's' + si }; }
  { const mi = marks.findIndex(q => (q.map === map || q.map === rmap) && Math.abs(q.x - mx) + Math.abs(q.y - my) <= 1); if (mi >= 0) return { kind: 'mark', id: marks[mi].id, label: marks[mi].label || '조사하기', key: 'm' + marks[mi].id }; }
  for (const o of [...objOrder, ...flats]){ const a = o.act || ACTS[o.name]; if (!a || !o.box || o.furn) continue;
    const dx = Math.max(Math.floor(o.box[0]) - mx, 0, mx - (Math.ceil(o.box[2]) - 1)), dy = Math.max(Math.floor(o.box[1]) - my, 0, my - (Math.ceil(o.box[3]) - 1));
    if (dx + dy === 1) return { kind: 'act', o, label: a[1], text: a[0], key: 'a' + o.name + o.x + ',' + o.y }; }
  if (World.onWater && !World.busyFish) for (const [dx, dy] of [[0, 1], [1, 0], [0, -1], [-1, 0]]) if (isWater(mx + dx, my + dy)) return { kind: 'water', wx: mx + dx, wy: my + dy, key: 'w' };
  return null;
}
function nearCheck(){ if (!World.onNear || !started) return; const t = findNear(), k = t ? t.key : ''; if (k !== nearKey){ nearKey = k; nearT = t; World.onNear(t); } }
World.nearRefresh = () => { nearKey = '\0'; nearCheck(); };
World.doNear = () => { const t = nearT; if (!t) return; hideBubble();
  if (t.kind === 'npc'){ const np = people.find(q => q.npc && q.npc.id === t.id); if (np) World.faceTo(np.x, np.y); World.onNpc && World.onNpc(t.id); }
  else if (t.kind === 'spot'){ World.onSpot && World.onSpot(t.i, t.sp); }
  else if (t.kind === 'mark'){ World.onMark && World.onMark(t.id); }
  else if (t.kind === 'act'){ useObj(t.o, t.o.act || ACTS[t.o.name]); }
  else if (t.kind === 'water'){ World.faceTo(t.wx, t.wy); World.onWater && World.onWater(t.wx, t.wy); } };
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
  if (!door.to){ if (World.onLockedDoor && World.onLockedDoor(door.label)) return; showBubble(o, `<b>${door.label}</b><br>아직 문이 잠겨 있어요 · 곧 열려요`); return; }
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
  // 이야기 NPC를 누르면 (판정은 발부터 머리 위 이름표까지: 얼굴을 눌러도 잡혀요)
  const np = people.filter(p => p.npc && (() => { const [sx, sy] = P(p.x + .5, p.y + .5), h = World.Avatar.FH * ASC + 10; return x >= sx - 10 && x <= sx + 10 && y >= sy - h && y <= sy + 3; })()).sort((a, b) => (b.x + b.y) - (a.x + a.y))[0];
  if (np && World.onNpc){ const n = np.npc, d = Math.abs(Math.round(me.x) - np.x) + Math.abs(Math.round(me.y) - np.y); if (d <= 1) World.onNpc(n.id); else { const c = near([[np.x, np.y]])[0]; if (c && goto(me, c[0], c[1])) pending = { npcTalk: n.id }; } return; }
  // 친구를 누르면 (겹치면 앞에 있는 사람)
  const pr = people.filter(p => p.peer && (() => { const [sx, sy] = P(p.x + .5, p.y + .5); return x >= sx - 9 && x <= sx + 9 && y >= sy - World.Avatar.FH * ASC - 10 && y <= sy + 3; })()).sort((a, b) => (b.x + b.y) - (a.x + a.y))[0];
  if (pr && World.onPeer){ World.onPeer(pr.peer); return; }
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
  if (World.busyFish) return;
  // 채집 지점은 조금 빗나가게 눌러도 돼요 (한 칸 안)
  const si = spotMap === map ? spots.map((sp, i) => [i, Math.hypot(sp.x - tx, sp.y - ty)]).filter(([, d]) => d <= 1.5).sort((p1, p2) => p1[1] - p2[1]).map(([i]) => i)[0] ?? -1 : -1;
  { const mi = marks.map((q, i) => [i, (q.map === map || q.map === rmap) ? Math.hypot(q.x - tx, q.y - ty) : 99]).filter(([, d]) => d <= 1.5).sort((p1, p2) => p1[1] - p2[1]).map(([i]) => i)[0] ?? -1;
    if (mi >= 0){ const q = marks[mi]; if (Math.abs(Math.round(me.x) - q.x) + Math.abs(Math.round(me.y) - q.y) <= 1){ World.onMark && World.onMark(q.id); } else { const c = near([[q.x, q.y]])[0]; if (c && goto(me, c[0], c[1])) pending = { mark: q.id }; } return; } }
  if (si >= 0 && World.onSpot){ const sp = spots[si]; if (Math.round(me.x) === sp.x && Math.round(me.y) === sp.y) World.onSpot(si, sp); else if (goto(me, sp.x, sp.y)) pending = { spot: si, sp }; return; }
  if (isWater(tx, ty) && World.onWater){   // 물가 바로 옆 칸, 없으면 가까운 물가로 (그 칸에서 낚시할 물을 다시 골라요)
    let wx = tx, wy = ty, st = near([[tx, ty]])[0];
    if (!st){ const c = World.freeNear(tx, ty, 4).sort((p1, p2) => Math.hypot(p1[0] - tx, p1[1] - ty) - Math.hypot(p2[0] - tx, p2[1] - ty)).find(([a, b]) => [[1,0],[-1,0],[0,1],[0,-1]].some(([dx, dy]) => isWater(a + dx, b + dy)));
      if (c){ st = c; const w = [[1,0],[-1,0],[0,1],[0,-1]].map(([dx, dy]) => [c[0] + dx, c[1] + dy]).find(([a, b]) => isWater(a, b)); wx = w[0]; wy = w[1]; } }
    if (st){ if (Math.round(me.x) === st[0] && Math.round(me.y) === st[1]){ World.faceTo(wx, wy); World.onWater(wx, wy); } else if (goto(me, st[0], st[1])) pending = { water: [wx, wy] }; }
    return;
  }
  const door = M.objs.find(o => o.door && o.door.tile[0] === tx && o.door.tile[1] === ty);
  if (goto(me, tx, ty) && door) pending = { door: door.door, o: door };
});
const SPEED = 6.5, RUN = 10;   // 타일/초. 멀리 갈 때(남은 길 10칸 넘게)는 달려요
function step(p, dt){
  if (!p.path.length){
    if (p.me && pending){ const pd = pending; pending = null; if (pd.water){ World.faceTo(pd.water[0], pd.water[1]); World.onWater && World.onWater(pd.water[0], pd.water[1]); } else if (pd.mark){ World.onMark && World.onMark(pd.mark); } else if (pd.npcTalk){ const np = people.find(q => q.npc && q.npc.id === pd.npcTalk); if (np) World.faceTo(np.x, np.y); World.onNpc && World.onNpc(pd.npcTalk); } else if (pd.spot !== undefined){ World.onSpot && World.onSpot(pd.spot, pd.sp); } else if (pd.door) goDoor(pd.door, pd.o); else { const a = pd.act.act || ACTS[pd.act.name]; showBubble(pd.act, a[0], a[1], () => useObj(pd.act, a)); } }
    if (p.npc && p.npc.wander && !p.path.length && (p.idle -= dt) < 0){ const r = p.npc.r ?? 2; p.idle = 1.5 + Math.random() * 3.5; for (let i = 0; i < 12; i++){ const gx = p.home[0] + Math.floor(Math.random() * (r * 2 + 1)) - r, gy = p.home[1] + Math.floor(Math.random() * (r * 2 + 1)) - r; if (goto(p, gx, gy)) break; } }   // 루틴 장소 안에서 계속 돌아다녀요
    if (!p.me && !p.peer && !p.npc && (p.idle -= dt) < 0){ p.idle = 2 + Math.random() * 5; for (let i = 0; i < 20; i++){ const gx = Math.round(p.x) + Math.floor(Math.random() * 13) - 6, gy = Math.round(p.y) + Math.floor(Math.random() * 13) - 6; if (goto(p, gx, gy)) break; } }
    p.t = 0; return;
  }
  const [gx, gy] = p.path[0], dx = gx - p.x, dy = gy - p.y, d = Math.hypot(dx, dy);
  // 쿼터뷰 네 방향: x+ (오른쪽 아래) 오른쪽 옆, x- (왼쪽 위) 왼쪽 옆, y+ (왼쪽 아래) 앞, y- (오른쪽 위) 뒤
  // view: 프레임 첫 칸 (아래·위·왼쪽·오른쪽 보기). LPC 부품은 네 방향 그림이 다 있어서 뒤집지 않아요
  const DV = World.Avatar.meta.dirs;
  if (Math.abs(dx) > Math.abs(dy)){ p.view = dx > 0 ? DV.right : DV.left; p.flip = false; }
  else if (d > 0){ p.view = dy < 0 ? DV.up : DV.down; p.flip = false; }
  if (p.pet && d > 0) p.flip = dx - dy > 0;   // 생물은 화면에서 오른쪽으로 가면 뒤집어요
  const mv = (p.run ? RUN : (p.me || p.peer) && p.path.length > 10 ? RUN : (p.me || p.peer) ? SPEED : SPEED * (p.npc && !p.npc.cut ? .35 : .6)) * dt * (p.me ? speedK : 1); if (d <= mv){ p.x = gx; p.y = gy; p.path.shift(); } else { p.x += dx / d * mv; p.y += dy / d * mv; } p.t += dt;
}
// 할로윈 효과: 박쥐 떼, 보라 안개, 도깨비불
const bats = Array.from({ length: 7 }, (_, i) => ({ x: 0, y: 0, vx: 0, vy: 0, ph: i, init: false }));
const fogs = Array.from({ length: 6 }, (_, i) => ({ x: Math.random(), y: Math.random(), s: 60 + Math.random() * 50, v: 4 + Math.random() * 6 }));
const wisps = Array.from({ length: 10 }, () => ({ x: Math.random(), y: Math.random(), ph: Math.random() * 6 }));
function spooky(now, dt, view){
  const cx = out;
  bats.forEach(b => {
    if (skyN < .55) return;   // 박쥐는 해가 지면 나와요
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
    cx.globalAlpha = (.35 + .3 * Math.sin(now / 300 + w.ph)) * Math.max(0, (skyN - .4) / .6); if (cx.globalAlpha > .01) cx.drawImage(glow(4, [170, 255, 230]), x - 4, y - 4);
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
// 하늘: 현실 시간을 따라가요 (World.hourNow 로 시각을 바꿀 수 있어요: 관리자가 시간대를 정할 때). rgb = 곱하기 색, n = 밤 정도 0~1 (null = 밤색)
World.hourNow = () => { const d = new Date(); return d.getHours() + d.getMinutes() / 60; };
const SKYK = [   // [시각, 곱하기 색(null=밤색), 밤 정도, 밝기 배율(그림 자체를 밝혀요: 0=그대로, 1=2배)]
  [0, null, 1, 0], [4.5, null, 1, 0], [5.6, [175, 145, 190], .85, .15], [6.6, [255, 190, 175], .6, .55], [7.8, [255, 232, 200], .28, 1.15],
  [9.5, [255, 246, 232], .08, 1.5], [11.5, [236, 246, 255], 0, 1.75], [15.5, [255, 250, 236], 0, 1.6], [17.3, [255, 205, 150], .25, 1.0],
  [18.8, [245, 140, 125], .6, .35], [20.2, [190, 135, 185], .85, 0], [21.5, null, 1, 0], [24, null, 1, 0]];
let skyTmp = null;
function skyNow(){
  const h = ((World.hourNow() % 24) + 24) % 24, N = BRIGHT[bright]; let i = 1; while (i < SKYK.length - 1 && SKYK[i][0] <= h) i++;
  const a = SKYK[i - 1], b = SKYK[i], k = (h - a[0]) / (b[0] - a[0] || 1), A = a[1] || N, B = b[1] || N;
  return { c: A.map((v, j) => Math.round(v + (B[j] - v) * k)), n: a[2] + (b[2] - a[2]) * k, g: a[3] + (b[3] - a[3]) * k };
}

const fx = [];
let last = performance.now(), camIX = 0, camIY = 0;
function drawPerson(p){ const cx = out;
  if (p.pet) return drawPet(p);
  if (p.npc && p.npc.pix !== undefined){   // 조연 동물: 32칸 그림, 걸을 때 콩콩 뛰어요
    const [sx, sy] = P(p.x + .5, p.y + .5); cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 5, 2, 0, 0, Math.PI * 2); cx.fill();
    if (!PIX_IMG || !PIX_IMG.complete) return; const cp = KPX * ASC, w = 32 * cp, hop = p.path.length ? Math.abs(Math.sin(p.t * 9)) * 2 * cp : 0;
    const dx = Math.round((sx - camIX) * KPX), dy = Math.round((sy - camIY) * KPX - 31 * cp - hop), left = p.view === World.Avatar.meta.dirs.left;
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); if (left){ cx.translate(dx, 0); cx.scale(-1, 1); cx.drawImage(PIX_IMG, p.npc.pix * 32, 0, 32, 32, -w / 2, dy, w, w); } else cx.drawImage(PIX_IMG, p.npc.pix * 32, 0, 32, 32, Math.round(dx - w / 2), dy, w, w); cx.restore(); return;
  }
  if (p.npc && p.npc.spr !== undefined){   // 이야기 NPC: LPC로 조립한 그림 (tools/iso/lpc/npc_lpc.py), 한 줄 = 한 명, 칸 배치는 캐릭터와 같아요
    const [sx, sy] = P(p.x + .5, p.y + .5); cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 6, 2.5, 0, 0, Math.PI * 2); cx.fill();
    if (!NPC_IMG || !NPC_IMG.complete) return; const A = World.Avatar, cp = KPX * ASC, w = A.FW * cp, h = A.FH * cp, WK = A.meta.walk, col = (p.view || 0) + (p.path.length ? WK[Math.floor(p.t * 7) % WK.length] : p.npc.flap ? WK[Math.floor(performance.now() / 140) % WK.length] : 0);
    const dx = Math.round((sx - camIX) * KPX), dy = Math.round((sy - camIY) * KPX - (A.FH - 1.5) * cp) + (p.npc.float ? Math.round(Math.sin(performance.now() / 600 + p.npc.spr) * 2) * cp : 0);
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); if (p.npc.alpha) cx.globalAlpha = p.npc.alpha; cx.drawImage(NPC_IMG, col * A.FW, p.npc.spr * A.FH, A.FW, A.FH, Math.round(dx - w / 2), dy, w, h); cx.restore(); return;
  }
  const [sx, sy] = P(p.x + .5, p.y + .5);
  cx.fillStyle = 'rgba(10,5,20,.3)'; cx.beginPath(); cx.ellipse(sx, sy, 6, 2.5, 0, 0, Math.PI * 2); cx.fill();
  const WK = World.Avatar.meta.walk, f = p.path.length ? WK[Math.floor(p.t * (p.me || p.peer ? 10 : 7)) % WK.length] : 0, col = (p.view || 0) + f;
  const A = World.Avatar, S = A.compose(p.av), cp = KPX * ASC, w = A.FW * cp, h = A.FH * cp;
  const dx = Math.round((sx - camIX) * KPX), dy = Math.round((sy - camIY) * KPX - (A.FH - 1.5) * cp);
  cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0);
  if (p.flip){ cx.translate(dx, dy); cx.scale(-1, 1); cx.drawImage(S, col * A.FW, 0, A.FW, A.FH, -w / 2, 0, w, h); } else cx.drawImage(S, col * A.FW, 0, A.FW, A.FH, Math.round(dx - w / 2), dy, w, h);
  cx.restore();
}
function frame(now){
  const dt = Math.min(.05, (now - last) / 1000); last = now;
  people.forEach(p => step(p, dt));
  if (dest && (!me.path.length || performance.now() - dest.t0 > 20000)) dest = null;
  if ((nearTick = (nearTick + 1) % 6) === 0) nearCheck();
  const A = MAPS[rmap];
  // 카메라 먼저: 맵이 화면보다 작으면 가운데에, 크면 내 캐릭터를 따라가요
  { const ct = camTarget && (camTarget.p || camTarget.x !== undefined) ? (camTarget.p ? [camTarget.p.x, camTarget.p.y] : [camTarget.x, camTarget.y]) : [me.x, me.y]; const [mx, my] = P(ct[0] + .5, ct[1] + .5);
    const tx = M.W <= VW ? (M.W - VW) / 2 : Math.max(0, Math.min(M.W - VW, mx - VW / 2));
    const ty = M.H <= VH ? (M.H - VH) / 2 - 10 : Math.max(0, Math.min(M.H - VH, my - 14 - VH / 2));
    if (camX === null){ camX = tx; camY = ty; } camX += (tx - camX) * Math.min(1, dt * 8); camY += (ty - camY) * Math.min(1, dt * 8); }
  const ix = Math.round(camX), iy = Math.round(camY); camIX = ix; camIY = iy;
  const view = { x: ix - 4, y: iy - 4, w: VW + 8, h: VH + 8 };
  out.setTransform(KPX, 0, 0, KPX, 0, 0); out.fillStyle = M.indoor ? (M.fill || '#0C0715') : (() => { const q = skyNow(), d = Math.max(0, 1 - q.n), hx = M.fill || '#1E2A1C', N = [1, 3, 5].map(i => parseInt(hx.slice(i, i + 2), 16)), D = [62, 96, 134]; return `rgb(${N.map((v, j) => Math.round(v + (D[j] - v) * d))})`; })(); out.fillRect(0, 0, VW, VH);
  out.setTransform(KPX, 0, 0, KPX, -ix * KPX, -iy * KPX);
  const cx = out;
  cx.drawImage(A.bg, Math.max(0, ix), Math.max(0, iy), VW, VH, Math.max(0, ix), Math.max(0, iy), VW, VH);
  // 물결 반짝임
  if (M.water) for (let i = 0; i < 6; i++){ const w = M.water[(Math.random() * M.water.length) | 0]; const [wx, wy] = P(w[0] + Math.random(), w[1] + Math.random()); if (wx > view.x && wx < view.x + view.w && wy > view.y && wy < view.y + view.h) fx.push({ x: wx, y: wy, v: 0, life: .5, c: '#DFF2FF' }); }
  if (dest){ const [dx, dy] = P(dest.x + .5, dest.y + .5), ph = (performance.now() / 500) % 1; cx.strokeStyle = `rgba(255,154,60,${1 - ph * .7})`; cx.lineWidth = 1; cx.beginPath(); cx.ellipse(dx, dy, 6 + ph * 5, 3 + ph * 2.5, 0, 0, Math.PI * 2); cx.stroke(); cx.fillStyle = '#FF9A3C'; cx.fillRect(dx - 1, dy - 9 - Math.round(ph * 3), 2, 6); }
  // 문 표시 (반짝이는 발판)
  const pulse = .5 + .5 * Math.sin(now / 300);
  M.objs.forEach(o => { if (!o.door) return; const [x, y] = P(o.door.tile[0] + .5, o.door.tile[1] + .5); cx.fillStyle = `rgba(255,216,102,${.25 + .35 * pulse})`; cx.beginPath(); cx.moveTo(x, y - 4); cx.lineTo(x + 8, y); cx.lineTo(x, y + 4); cx.lineTo(x - 8, y); cx.fill(); });
  // 바닥에 깔린 가구 (러그)
  flats.forEach(o => cx.drawImage(FURN_IMG, o.sx, 0, o.sw, o.sh, o.x, o.y, o.sw, o.sh));
  // 낚시 찌 (입질하면 쏙 들어가고 물결)
  if (bobber){ const [x, y] = P(bobber.x + .5, bobber.y + .5), bob = bobber.bite ? 1 + Math.round(Math.abs(Math.sin(now / 60))) : Math.round(Math.sin(now / 400));
    const [mx, my] = P(me.x + .5, me.y + .5); cx.strokeStyle = 'rgba(230,230,240,.55)'; cx.lineWidth = .5; cx.beginPath(); cx.moveTo(mx + (bobber.x > me.x ? 6 : -6), my - 22); cx.lineTo(x, y - 2 + bob); cx.stroke();
    cx.fillStyle = 'rgba(200,240,255,.5)'; const rr = bobber.bite ? 4 + (now / 80 % 4) : 3; cx.beginPath(); cx.ellipse(x, y + 1, rr, rr / 2, 0, 0, Math.PI * 2); cx.fill();
    cx.fillStyle = '#F2EAD8'; cx.fillRect(Math.round(x) - 1, Math.round(y) - 2 + bob, 3, 2); cx.fillStyle = '#E0303A'; cx.fillRect(Math.round(x) - 1, Math.round(y) - 4 + bob, 3, 2); }
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
  const SK = M.indoor ? { c: [150, 130, 175], n: 1, g: 0 } : skyNow(); skyN = SK.n;
  SK.g *= (World.skyGain ?? .8);   // 조정용 손잡이 (시험용)
  if (SK.g > .03){   // 낮에는 그림 자체를 밝혀요 (안개를 덮는 게 아니라 색을 키워서 또렷하게)
    const W = cv.width, H = cv.height; if (!skyTmp || skyTmp.width !== W || skyTmp.height !== H){ skyTmp = document.createElement('canvas'); skyTmp.width = W; skyTmp.height = H; }
    const t = skyTmp.getContext('2d'); t.globalCompositeOperation = 'copy'; t.drawImage(cv, 0, 0);
    cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.globalCompositeOperation = 'lighter';
    for (let r = SK.g; r > .02; r -= 1){ cx.globalAlpha = Math.min(1, r); cx.drawImage(skyTmp, 0, 0); }
    const con = (World.skyCon ?? .45) * Math.min(1, SK.g);   // 대비: 밝힌 그림에 자기 자신을 곱해서 어두운 곳은 다시 어둡게 (뿌옇지 않게)
    if (con > .01){ t.globalCompositeOperation = 'copy'; t.drawImage(cv, 0, 0); cx.globalCompositeOperation = 'multiply'; cx.globalAlpha = con; cx.drawImage(skyTmp, 0, 0); cx.globalCompositeOperation = 'lighter'; }
    const lf = Math.min(1, SK.g); cx.globalAlpha = 1; cx.globalCompositeOperation = 'screen'; cx.fillStyle = `rgb(${Math.round(38 * lf)},${Math.round(50 * lf)},${Math.round(70 * lf)})`; cx.fillRect(0, 0, cv.width, cv.height);   // 가장 어두운 그림자만 하늘빛으로 살짝
    cx.restore();
  }
  if (SK.n > .02 || SK.c.some(v => v < 254)){
    cx.globalCompositeOperation = 'multiply'; cx.fillStyle = `rgb(${SK.c})`; cx.fillRect(ix, iy, VW, VH);
    cx.globalCompositeOperation = 'lighter';
    M.lights.forEach((L, i) => { if (L.p[0] + L.r < view.x || L.p[0] - L.r > view.x + view.w || L.p[1] + L.dy + L.r < view.y || L.p[1] + L.dy - L.r > view.y + view.h) return; const fl = L.f ? .85 + .15 * Math.sin(now / 130 + i * 1.7) * Math.sin(now / 370 + i) : 1; cx.globalAlpha = L.a * fl * Math.min(1, SK.n * 1.15); cx.drawImage(glow(L.r, L.c), L.p[0] - L.r, L.p[1] + L.dy - L.r); });
    cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over';
  }
  drawWeather(cx, ix, iy, dt);
  if (cook){ const o = M.objs.find(q => q.name === 'cauldron' && q.box[0] === cook.x && q.box[1] === cook.y);
    if (o){ const cxp = o.x + o.sw / 2, top = o.y + (cook.top ?? 6), t = now / 1000, X = Math.round(cxp);
      // 불빛 (세기에 따라)
      cx.globalCompositeOperation = 'lighter'; cx.globalAlpha = .25 + .45 * (cook.heat || 0); cx.drawImage(glow(18, [255, 140, 60]), X - 18, o.y + o.sh - 22); cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over';
      // 국물 면 + 거품
      cx.fillStyle = cook.soup || '#C8642A'; cx.beginPath(); cx.ellipse(cxp, top + 2, o.sw / 2 - 4, 2.5, 0, 0, Math.PI * 2); cx.fill();
      cx.fillStyle = 'rgba(255,255,255,.55)'; const nb = 2 + Math.round((cook.heat || 0) * 4);
      for (let i = 0; i < nb; i++){ const ph = (t * (1 + (cook.heat || 0) * 2) + i * .37) % 1, bx = X - 6 + ((i * 5) % 12); cx.fillRect(bx, top + 1, 1, 1); if (ph > .6) cx.fillRect(bx - 1, top, 3, 1); }
      // 김
      cx.fillStyle = 'rgba(255,255,255,.35)'; for (let i = 0; i < (cook.steam ?? 3); i++){ const ph = (t * .6 + i / 3) % 1, sx = X - 5 + i * 5 + Math.round(Math.sin(t * 2 + i) * 1.5), sy = top - 3 - ph * 14; cx.globalAlpha = 1 - ph; cx.fillRect(sx, Math.round(sy), 2, 1); cx.fillRect(sx + 1, Math.round(sy) - 1, 1, 1); } cx.globalAlpha = 1;
      // 날아드는 재료 (그림 16px → 세계 8px: 캐릭터와 같은 픽셀 크기)
      if (cook.drop){ const d = cook.drop, im = cookImg[d.src], k = Math.min(1, d.t), fx = cxp + 26 * (1 - k), fy = top - 6 - Math.sin(k * Math.PI) * 18 + k * 4;
        if (im && im.complete) cx.drawImage(im, d.sx ?? d.i * 16, d.sy || 0, d.sw || 16, d.sh || 16, Math.round(fx * 2) / 2 - 4, Math.round(fy * 2) / 2 - 8, 8, 8); }
      if (cook.splash){ cx.fillStyle = cook.splashC || '#FFD0A0'; [[-5, -3], [4, -4], [-2, -6], [6, -1], [-7, 0]].forEach(([dx, dy]) => cx.fillRect(X + dx, top + dy, 1, 1)); }
      // 국자: 빙글빙글
      if (cook.stir !== undefined && cook.stir !== null){ const a = cook.stir, lx = Math.round(cxp + Math.cos(a) * 5), ly = Math.round(top + 2 + Math.sin(a) * 1.5);
        cx.fillStyle = '#22183F'; cx.fillRect(lx - 1, ly - 13, 3, 13); cx.fillStyle = '#B8875A'; cx.fillRect(lx, ly - 12, 1, 12); cx.fillStyle = '#22183F'; cx.fillRect(lx - 2, ly - 1, 5, 3); cx.fillStyle = '#B8875A'; cx.fillRect(lx - 1, ly, 3, 1); }
      // 젓는 방향 안내 점선
      if (cook.guide){ cx.fillStyle = '#FFE070'; for (let i = 0; i < 12; i++){ if ((i + Math.floor(t * 8)) % 3) continue; const a = i / 12 * Math.PI * 2; cx.fillRect(Math.round(cxp + Math.cos(a) * 12), Math.round(top + 2 + Math.sin(a) * 5), 1, 1); } }
    } }
  drawMarks(now, view); drawBats(now); if (fxDark){ cx.globalAlpha = fxDark; cx.fillStyle = '#05030A'; cx.fillRect(ix, iy, VW, VH); cx.globalAlpha = 1; }
  // 채집 지점: 밤에도 잘 보이게 빛 다음에 그려요
  if (spotMap === map) spots.forEach((sp, i) => { const [x, y] = P(sp.x + .5, sp.y + .5), t = now / 260 + i * 1.3, a = .6 + .4 * Math.sin(t), sy = y - 7 - Math.round(Math.sin(t * .7) * 2);
    if (x < view.x || x > view.x + view.w || y < view.y || y > view.y + view.h) return;
    if (sp.k){   // 놀이 호박: 보통 · 황금 · 썩은
      const C = { p: ['#F08A2A', '#C8641A'], g: ['#FFD040', '#E0A020'], r: ['#7A8A4A', '#56603A'] }[sp.k] || ['#F08A2A', '#C8641A'], X = Math.round(x), Y = Math.round(y) - 1 - Math.max(0, Math.round(Math.sin(t * 2) * 1.5));
      { cx.globalCompositeOperation = 'lighter'; cx.globalAlpha = (sp.k === 'g' ? .6 : .35) * a; cx.drawImage(glow(10, sp.k === 'r' ? [140, 255, 120] : [255, 210, 90]), X - 10, Y - 12); cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over'; }
      cx.fillStyle = '#FFF6D0'; if (Math.sin(t * 3) > 0){ cx.fillRect(X + 5, Y - 12, 1, 3); cx.fillRect(X + 4, Y - 11, 3, 1); }
      cx.fillStyle = '#22183F'; cx.fillRect(X - 5, Y - 7, 11, 8); cx.fillRect(X - 4, Y - 8, 9, 10);
      cx.fillStyle = C[0]; cx.fillRect(X - 4, Y - 7, 9, 8); cx.fillRect(X - 3, Y - 8, 7, 10); cx.fillStyle = C[1]; cx.fillRect(X - 1, Y - 7, 1, 8); cx.fillRect(X + 2, Y - 7, 1, 8);
      cx.fillStyle = '#4A8A3A'; cx.fillRect(X, Y - 10, 2, 3);
      if (sp.k === 'r'){ cx.fillStyle = '#3A3A2A'; cx.fillRect(X - 2, Y - 5, 1, 1); cx.fillRect(X + 2, Y - 3, 2, 1); }
      return;
    }
    cx.globalCompositeOperation = 'lighter'; cx.globalAlpha = .55 * a; cx.drawImage(glow(10, [255, 220, 120]), x - 10, sy - 10); cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over';
    cx.fillStyle = `rgba(255,250,215,${a})`; cx.fillRect(Math.round(x), sy - 3, 1, 7); cx.fillRect(Math.round(x) - 3, sy, 7, 1); cx.fillRect(Math.round(x) - 1, sy - 1, 3, 3);
    if (Math.sin(t * 1.7) > .5){ cx.fillRect(Math.round(x) + 5, sy - 5, 1, 1); cx.fillRect(Math.round(x) - 5, sy + 3, 1, 1); } });
  if (!M.indoor) spooky(now, dt, view);
  drawSky(now);
  out.setTransform(1, 0, 0, 1, 0, 0);
  const k = cv.clientWidth / VW; dpr = window.devicePixelRatio || 1;
  if (M.rooms) M.rooms.forEach((rm, i) => { const [sx, sy] = P(rm.door[0] + .5, rm.door[1] + .5); if (sx > view.x && sx < view.x + view.w) drawTag(roomTags[i], sx, sy - 52, now); });
  if (M.pens) M.pens.forEach((pn, i) => { const [sx, sy] = P(pn.sign[0] + .5, pn.sign[1] + .5); if (sx > view.x && sx < view.x + view.w) drawTag(penTags[i], sx, sy - 20, now); });
  people.forEach((p, i) => { const [sx, sy] = P(p.x + .5, p.y + .5); if (sx > view.x - 40 && sx < view.x + view.w + 40 && sy > view.y && sy < view.y + view.h + 60) drawTag(tags[i], sx, sy - World.Avatar.FH * ASC + 4, now); });
  const tn = performance.now();
  for (let i = says.length - 1; i >= 0; i--){ const p = says[i]; if (tn > p.say.until || (!p.me && !people.includes(p))){ sayOff(p); continue; } const [sx, sy] = P(p.x + .5, p.y + .5); p.say.el.style.left = (sx - ix) * k + 'px'; p.say.el.style.top = (sy - World.Avatar.FH * ASC - 2 - iy) * k + 'px'; }
  if (bubble){ const o = bubble.o; bubble.el.style.left = Math.max(90, Math.min(cv.clientWidth - 90, (o.x + o.sw / 2 - ix) * k)) + 'px'; bubble.el.style.top = Math.max(70, (o.y - 2 - iy) * k) + 'px'; }
  if ((clockTick = (clockTick + 1) % 30) === 0){ const d = new Date(), t = World.clockText ? World.clockText(d) : `🌕 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')} · 보름밤`; if (t !== clockLast){ clockLast = t; clockEl.textContent = t; } }
  requestAnimationFrame(frame);
}
document.getElementById('tDay').onclick = e => { bright = (bright + 1) % 3; e.target.textContent = BRIGHT_NEXT[bright]; };
const ZL = [2, 0, 1];   // 단계(가까이·보통·멀리) → ZOOMS 번호
const zoomLabel = () => { const b = document.getElementById('tZoom'); if (b) b.textContent = ZOOMS[(zi + 1) % ZOOMS.length][0]; };
World.zoomStep = dir => { const lv = Math.max(0, Math.min(2, ZL.indexOf(zi) + dir)); if (ZL[lv] === zi) return; zi = ZL[lv]; zoomLabel(); resize(); camX = null; };
World.zoomLevel = () => ZL.indexOf(zi);
document.getElementById('tZoom').onclick = () => { zi = (zi + 1) % ZOOMS.length; zoomLabel(); resize(); camX = null; };
// 두 손가락으로 벌리면 가까이, 오므리면 멀리. 마우스 휠도 같아요
{ const pts = new Map(); let base = 0, wheelAt = 0;
  const dist = () => { const [a, b] = [...pts.values()]; return Math.hypot(a.x - b.x, a.y - b.y); };
  cv.addEventListener('pointerdown', e => { pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); if (pts.size === 2){ base = dist(); me.path = []; pending = null; hideBubble(); } }, true);
  cv.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); if (pts.size === 2 && base){ const r = dist() / base; if (r > 1.3){ World.zoomStep(-1); base = dist(); } else if (r < .77){ World.zoomStep(1); base = dist(); } } });
  const up = e => { pts.delete(e.pointerId); if (pts.size < 2) base = 0; }; cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up); cv.addEventListener('pointerleave', up);
  cv.addEventListener('wheel', e => { e.preventDefault(); const t = performance.now(); if (t - wheelAt < 250) return; wheelAt = t; World.zoomStep(e.deltaY > 0 ? 1 : -1); }, { passive: false }); }
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
// 관리자 페이지: 그 방 전체 그림(바닥 + 물건)과 좌표 정보
World.mapCanvas = async id => { await World.ready; const rid = real(id); if (!MAPS[rid]) return null; await ensureMap(rid); const A = MAPS[rid], m = A.meta;
  const c = document.createElement('canvas'); c.width = m.W; c.height = m.H; const g = c.getContext('2d'); g.fillStyle = m.fill || '#140E1E'; g.fillRect(0, 0, m.W, m.H); g.drawImage(A.bg, 0, 0);
  (A.order || (A.order = orderObjs(m.objs))).forEach(o => g.drawImage(A.obj, o.sx, o.sy, o.sw, o.sh, o.x, o.y, o.sw, o.sh)); return { canvas: c, meta: m }; };
World.mapIds = () => Object.keys(MAPS);
World.objSprite = async (id, name) => { await World.ready; const rid = real(id); if (!MAPS[rid]) return null; await ensureMap(rid); const A = MAPS[rid], o = A.meta.objs.find(q => q.name === name); return o ? { img: A.obj, sx: o.sx, sy: o.sy, sw: o.sw, sh: o.sh } : null; };   // 이벤트 무대용 (까마귀 등)
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
World.setPlayer = (name, av) => { me.name = name; me.av = av; if (tags[0]) tags[0].t = name; };
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
    const o = Array.isArray(objName) ? null : M.objs.find(x => x.name === objName);
    if (Array.isArray(objName)){ me.x = objName[0]; me.y = objName[1]; me.path = []; camX = null; }   // 바로 가기: 좌표로
    if (o){ const tiles = []; for (let a = Math.floor(o.box[0]); a < Math.ceil(o.box[2]); a++) for (let b = Math.floor(o.box[1]); b < Math.ceil(o.box[3]); b++) tiles.push([a, b]); const c = near(tiles)[0]; if (c){ me.x = c[0]; me.y = c[1]; me.path = []; camX = null; } }
    setTimeout(() => { fadeEl.style.opacity = 0; busy = false; then && then(); }, 150);
  }, 380));
};

// ========== 메인 의뢰: 맵 컷신 · 조사 지점 · 밤하늘 등불자리 ==========
// 컷신 명령 (index.html의 메인 의뢰 실행기가 불러요): spawn / walk / cam / say / emote / crowd / fx / player / despawn / wait / fade / end
let cutOn = false, camTarget = null, cutActors = {}, crowdPeople = [], skyCfg = null, marks = [], markPulse = 0;
const cutMk = (id, spec, x, y) => { const p = mk(spec.name || id, spec.av || null, x, y, false); p.npc = { id: 'cut:' + id, cut: true, spr: spec.spr, float: spec.float, alpha: spec.alpha, flap: spec.flap, wander: false, r: 0 }; p.home = [x, y]; p.idle = 1e9; p.view = World.Avatar.meta.dirs[spec.dir || 'down'] || 0; return p; };
const walkDone = (p, timeout = 12000) => new Promise(r => { const t0 = performance.now(); const tick = () => { if (!p.path.length || performance.now() - t0 > timeout || !cutOn){ p.path = []; r(); } else requestAnimationFrame(tick); }; tick(); });
const spawnAt = (x, y) => { if (free(x, y)) return [x, y]; return World.freeNear(x, y, 3).sort((a, b) => Math.hypot(a[0] - x, a[1] - y) - Math.hypot(b[0] - x, b[1] - y))[0] || [x, y]; };
const personOf = id => id === 'player' || id === 'me' ? me : cutActors[id] || people.find(p => p.npc && (p.npc.id === id || p.npc.id === 'cut:' + id)) || null;
World.cutBusy = () => cutOn;
World.cut = async (cmds, hooks = {}) => {   // hooks: { sfx(id), skip() → true면 바로 끝 }
  if (!started || cutOn) return false;
  cutOn = true; busy = true; hideBubble(); dest = null; me.path = [];
  const skip = () => hooks.skip && hooks.skip();
  try {
    for (const c of cmds || []){
      if (skip()) break;
      const k = c.cmd, who = c.who;
      if (k === 'spawn'){ const [x, y] = spawnAt(c.x, c.y); const p = cutMk(who, c, x, y); cutActors[who] = p; people.push(p); retag(); }
      else if (k === 'despawn'){ const p = cutActors[who]; if (p){ const i = people.indexOf(p); if (i >= 0) people.splice(i, 1); sayOff(p); delete cutActors[who]; retag(); } }
      else if (k === 'walk'){ const p = personOf(who); if (p){ const t = spawnAt(c.x, c.y); if (c.run) p.run = true; if (goto(p, t[0], t[1])){ if (c.wait !== false) await walkDone(p, (c.timeout || 12) * 1000); } else { p.x = t[0]; p.y = t[1]; } p.run = false; if (c.dir) p.view = World.Avatar.meta.dirs[c.dir] || p.view; } }
      else if (k === 'face'){ const p = personOf(who), q = personOf(c.to); if (p && q){ const DV = World.Avatar.meta.dirs, dx = q.x - p.x, dy = q.y - p.y; p.view = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? DV.right : DV.left) : (dy < 0 ? DV.up : DV.down); } }
      else if (k === 'cam'){ if (who){ camTarget = { p: personOf(who) }; } else if (c.x !== undefined){ camTarget = { x: c.x, y: c.y }; } else camTarget = null; if (c.wait) await new Promise(r => setTimeout(r, c.wait * 1000)); }
      else if (k === 'say'){ const p = personOf(who); if (p) sayOn(p, c.text, c.ms || 2600, c.big); if (c.wait !== false) await new Promise(r => setTimeout(r, (c.ms || 2600) * .9)); }
      else if (k === 'emote'){ const p = personOf(who); if (p) sayOn(p, '', 2000, c.icon ?? 4); await new Promise(r => setTimeout(r, 600)); }
      else if (k === 'crowd'){ await crowdDo(c); }
      else if (k === 'wait'){ await new Promise(r => setTimeout(r, Math.min(6, c.sec || 1) * 1000)); }
      else if (k === 'sfx'){ hooks.sfx && hooks.sfx(c.id); }
      else if (k === 'fx'){ fxDo(c); if (c.wait) await new Promise(r => setTimeout(r, c.wait * 1000)); }
      else if (k === 'player'){ const t = spawnAt(c.x, c.y); me.x = t[0]; me.y = t[1]; me.path = []; if (c.dir) me.view = World.Avatar.meta.dirs[c.dir] || 0; camX = null; }
      else if (k === 'fade'){ fadeEl.textContent = c.text || ''; fadeEl.style.opacity = c.v ? 1 : 0; await new Promise(r => setTimeout(r, c.v ? 400 : 420)); }
      else if (k === 'end') break;
    }
  } catch(e){ console.error('cut', e); }
  // 정리: 임시 배우는 keep이 아니면 지워요
  Object.keys(cutActors).forEach(id => { const p = cutActors[id]; if (!p.npc.keep){ const i = people.indexOf(p); if (i >= 0) people.splice(i, 1); sayOff(p); delete cutActors[id]; } });
  crowdPeople.forEach(p => { const i = people.indexOf(p); if (i >= 0) people.splice(i, 1); sayOff(p); }); crowdPeople = [];
  camTarget = null; cutOn = false; busy = false; fadeEl.style.opacity = 0; retag(); World.nearRefresh();
  return true;
};
World.cutKeep = id => { const p = cutActors[id]; if (p) p.npc.keep = true; };
World.cutClear = () => { Object.keys(cutActors).forEach(id => { const p = cutActors[id]; const i = people.indexOf(p); if (i >= 0) people.splice(i, 1); sayOff(p); delete cutActors[id]; }); retag(); };
function sayOn(p, text, ms, big){   // 누구든(NPC도) 머리 위 말풍선
  sayOff(p); const emo = typeof big === 'number' ? big : null, d = document.createElement('div'); d.className = 'say' + (emo !== null ? ' emo' : '');
  if (emo !== null){ const i = document.createElement('i'); i.className = 'emi'; i.style.setProperty('--i', emo); d.appendChild(i); } else d.textContent = text;
  world.appendChild(d); p.say = { el: d, until: performance.now() + ms }; says.push(p);
}
World.sayNpc = (id, text, ms = 3000) => { const p = personOf(id); if (p) sayOn(p, text, ms); };
// 구경꾼: 학생 n명이 from 근처에서 나타나 react 대로 움직여요 (flee: 멀어짐 · watch: 가까이 와서 봄 · scream: 제자리에서 놀람 뒤 흩어짐)
async function crowdDo(c){
  const n = Math.min(8, c.n || 4), [fx0, fy0] = c.from || [Math.round(me.x), Math.round(me.y)], cells = World.freeNear(fx0, fy0, c.r || 5).filter(([x, y]) => Math.hypot(x - fx0, y - fy0) >= 2);
  for (let i = 0; i < n && cells.length; i++){ const [x, y] = cells.splice(Math.floor(Math.random() * cells.length), 1)[0]; const p = mk('', World.Avatar.fromLook(Math.floor(Math.random() * 4)), x, y, false); p.npc = { id: 'crowd' + i, cut: true, wander: false, r: 0 }; p.home = [x, y]; p.idle = 1e9; p.pet = false; crowdPeople.push(p); people.push(p); }
  retag();
  const react = c.react || 'watch';
  if (react === 'scream'){ crowdPeople.forEach((p, i) => setTimeout(() => sayOn(p, '', 1800, 4), i * 120)); await new Promise(r => setTimeout(r, 1200)); }
  if (react === 'flee' || react === 'scream'){ crowdPeople.forEach(p => { const dx = p.x - fx0, dy = p.y - fy0, d = Math.hypot(dx, dy) || 1; const t = spawnAt(Math.round(p.x + dx / d * 7), Math.round(p.y + dy / d * 7)); p.run = true; goto(p, t[0], t[1]); }); await new Promise(r => setTimeout(r, 1800)); }
  else if (react === 'watch'){ crowdPeople.forEach(p => { const t = spawnAt(Math.round(fx0 + (p.x - fx0) * .5), Math.round(fy0 + (p.y - fy0) * .5)); goto(p, t[0], t[1]); }); await new Promise(r => setTimeout(r, 1500)); crowdPeople.forEach((p, i) => setTimeout(() => sayOn(p, c.text || '', 2000, c.text ? undefined : 9), i * 200)); await new Promise(r => setTimeout(r, c.hold ? c.hold * 1000 : 2200)); }
  if (c.keep) return;
  crowdPeople.forEach(p => { const i = people.indexOf(p); if (i >= 0) people.splice(i, 1); sayOff(p); }); crowdPeople = []; retag();
}
// 효과: bats 박쥐 떼 · bell 종소리 번쩍 · lightning 번개 · wind 바람(안개 빠르게) · dark 어둡게 / light 원래대로
let fxBats = 0, fxDark = 0, skyN = 1;
function fxDo(c){ const k = c.kind; if (k === 'bats') fxBats = performance.now() + (c.sec || 4) * 1000; else if (k === 'lightning' || k === 'bell') flashT = performance.now() + 260; else if (k === 'dark') fxDark = c.v ?? .45; else if (k === 'light') fxDark = 0; else if (k === 'wind'){ fogs.forEach(f => f.v *= 4); setTimeout(() => fogs.forEach(f => f.v /= 4), (c.sec || 4) * 1000); } }
// 조사 지점: 물음표가 떠 있고, 옆에 가면 상황 버튼 「조사하기」
World.setMarks = list => { marks = list || []; World.nearRefresh(); };
World.onMark = null;
// 밤하늘 등불자리: lit = 일곱 별 중 밝은 것(true/false ×7), jack = 등불 불씨(빈자리) 켜짐, done = 완성 연출
World.setSky = cfg => { skyCfg = cfg; };
const SKY = [[0, 0], [10, 7], [22, 2], [12, 18], [20, 30], [6, 32], [-4, 20]];   // 등불을 든 사람: 머리·어깨·팔·허리·다리 (상대 좌표)
const SKY_LANTERN = [30, 10], SKY_FLAME = [31, 15];
function drawSky(now){
  if (!skyCfg || M.indoor || skyN < .3) return;
  const ox = VW - 48, oy = 10, t = now / 1000; out.save(); out.setTransform(KPX, 0, 0, KPX, 0, 0);
  const lit = skyCfg.lit || [];
  out.globalCompositeOperation = 'lighter';
  SKY.forEach(([dx, dy], i) => { const on = !!lit[i], tw = (.75 + .25 * Math.sin(t * 2 + i)) * Math.max(0, Math.min(1, (skyN - .35) / .5)); const x = ox + dx, y = oy + dy;
    if (on){ out.globalAlpha = .7 * tw; out.drawImage(glow(6, [255, 236, 170]), x - 6, y - 6); out.globalAlpha = 1; out.fillStyle = '#FFF8DC'; out.fillRect(x, y, 1, 1); out.fillRect(x - 1, y, 1, 1); out.fillRect(x + 1, y, 1, 1); out.fillRect(x, y - 1, 1, 1); out.fillRect(x, y + 1, 1, 1); }
    else { out.globalAlpha = .35 + .15 * tw; out.fillStyle = '#B9A8D8'; out.fillRect(x, y, 1, 1); } });
  // 등불 끝의 작은 별(첫 마녀의 등불)은 늘 보여요
  { const x = ox + SKY_LANTERN[0], y = oy + SKY_LANTERN[1]; out.globalAlpha = .6; out.drawImage(glow(4, [255, 220, 120]), x - 4, y - 4); out.globalAlpha = 1; out.fillStyle = '#FFE8A0'; out.fillRect(x, y, 1, 1); }
  // 빈자리(잭의 불씨): 켜지면 가장 밝게
  if (skyCfg.jack){ const x = ox + SKY_FLAME[0], y = oy + SKY_FLAME[1], tw = .8 + .2 * Math.sin(t * 3); out.globalAlpha = .9 * tw; out.drawImage(glow(9, [255, 170, 60]), x - 9, y - 9); out.globalAlpha = 1; out.fillStyle = '#FFF2C0'; out.fillRect(x - 1, y - 1, 3, 3); }
  else if (skyCfg.hint && Math.sin(t * .7) > .95){ const x = ox + SKY_FLAME[0], y = oy + SKY_FLAME[1]; out.globalAlpha = .5; out.fillStyle = '#FFD090'; out.fillRect(x, y, 1, 1); }
  // 완성 뒤: 등불자리 옆에 처음 보는 희미한 별 하나 (다음 이야기의 떡밥)
  if (skyCfg.done && Math.sin(t * .9) > .2){ const x = ox - 16, y = oy + 38; out.globalAlpha = .25 + .25 * Math.sin(t * .9); out.fillStyle = '#D8CCFF'; out.fillRect(x, y, 1, 1); }
  // 완성: 별 사이를 잇는 선
  if (skyCfg.done){ out.globalAlpha = .25 + .1 * Math.sin(t * 2); out.strokeStyle = '#FFE8B0'; out.lineWidth = 1; out.beginPath(); SKY.forEach(([dx, dy], i) => { if (i === 0) out.moveTo(ox + dx + .5, oy + dy + .5); else out.lineTo(ox + dx + .5, oy + dy + .5); }); out.moveTo(ox + SKY[2][0] + .5, oy + SKY[2][1] + .5); out.lineTo(ox + SKY_LANTERN[0] + .5, oy + SKY_LANTERN[1] + .5); out.stroke(); }
  out.globalAlpha = 1; out.globalCompositeOperation = 'source-over'; out.restore();
}
function drawMarks(now, view){
  if (!marks.length) return;
  marks.forEach((mk_, i) => { if (mk_.map !== map && mk_.map !== rmap) return; const [x, y] = P(mk_.x + .5, mk_.y + .5); if (x < view.x || x > view.x + view.w || y < view.y || y > view.y + view.h) return;
    const t = now / 300 + i, a = .6 + .4 * Math.sin(t), X = Math.round(x), Y = Math.round(y) - 14 - Math.round(Math.sin(t * .8) * 2);
    out.globalCompositeOperation = 'lighter'; out.globalAlpha = .5 * a; out.drawImage(glow(10, [180, 220, 255]), X - 10, Y - 10); out.globalAlpha = 1; out.globalCompositeOperation = 'source-over';
    out.fillStyle = '#22183F'; out.fillRect(X - 3, Y - 6, 7, 9); out.fillStyle = '#CFEFFF';
    out.fillRect(X - 2, Y - 5, 5, 1); out.fillRect(X + 2, Y - 4, 1, 2); out.fillRect(X, Y - 2, 2, 1); out.fillRect(X, Y - 1, 1, 1); out.fillRect(X, Y + 1, 1, 1); });
}
function drawBats(now){
  if (fxBats < now) return; const t = now / 1000;
  out.fillStyle = '#1A1026'; for (let i = 0; i < 9; i++){ const x = camIX + ((t * 70 + i * 37) % (VW + 40)) - 20, y = camIY + 20 + i * 9 + Math.sin(t * 6 + i) * 8, w = Math.sin(t * 12 + i) > 0 ? 3 : 1; out.fillRect(Math.round(x) - w, Math.round(y), w, 1); out.fillRect(Math.round(x) + 1, Math.round(y), w, 1); out.fillRect(Math.round(x), Math.round(y) - 1, 1, 2); }
}
