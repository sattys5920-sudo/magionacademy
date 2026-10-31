// 시안: 「첫눈의 소원」 — 첫눈 오는 밤, 하늘에서 소원 쪽지가 눈처럼 내려요 → 주워서 읽고 응원 → 내 소원 쓰기 → 별이 되어 날아가요 → 응원 받음 → 마지막 밤 별자리
//   window.__wsGo() · window.__wsLog (소리 넣을 시각)
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__wsLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const css = document.createElement('style'); css.textContent = `
#wsfx{position:fixed;inset:0;width:100vw;height:100vh;z-index:300;pointer-events:none;image-rendering:pixelated}
#wscard{position:fixed;left:50%;top:42%;z-index:360;transform:translate(-50%,-50%) scale(.5) rotate(-6deg);opacity:0;transition:all .5s cubic-bezier(.2,1.3,.4,1);pointer-events:none;width:min(84vw,300px)}
#wscard.on{opacity:1;transform:translate(-50%,-50%) scale(1) rotate(-1.5deg)}
#wscard .pp{position:relative;background:#FBF6EA;border:3px solid #3A2C4A;border-radius:4px;padding:22px 18px 16px;box-shadow:0 0 0 3px #CFE0F4,0 0 26px rgba(190,220,255,.7);font-family:var(--f-px);color:#3A2C4A;font-size:16px;line-height:25px;text-align:center;min-height:96px}
#wscard .pp:before{content:'';position:absolute;left:0;right:0;top:0;height:8px;background:repeating-linear-gradient(90deg,#CFE0F4 0 6px,transparent 6px 12px)}
#wscard .pp small{display:block;margin-top:10px;font-size:12px;color:#8A7AA0}
#wscard .bt{display:flex;gap:8px;margin-top:10px}#wscard .bt span{flex:1;min-height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:var(--f-pxb);font-size:14px;border:2px solid #B8D8FF;background:rgba(30,22,52,.96);color:#F1E9FF}
#wscard .bt span.go{background:#FFE9A0;color:#3A2414;border-color:#E8B84A}#wscard .bt span.hit{transform:scale(.92);filter:brightness(1.2)}
#wswrite{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:362;max-width:560px;margin:0 auto;background:rgba(20,13,34,.97);border:2px solid #B8D8FF;border-radius:16px;padding:14px;display:none;font-family:var(--f-px);color:#F1E9FF}
#wswrite b{font-family:var(--f-pxb);font-size:15px;color:#CFE6FF}#wswrite .in{margin:10px 0;background:#FBF6EA;color:#3A2C4A;border-radius:8px;padding:10px 12px;min-height:44px;font-size:15px;line-height:22px}
#wswrite .in i{display:inline-block;width:2px;height:16px;background:#3A2C4A;vertical-align:-2px;animation:wsb 1s infinite}@keyframes wsb{50%{opacity:0}}
#wswrite .rw{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#B8A8D8}#wswrite .rw span.go{min-height:40px;padding:0 16px;border-radius:12px;display:flex;align-items:center;font-family:var(--f-pxb);font-size:14px;background:#FFE9A0;color:#3A2414}
#wswrite .rw span.hit{transform:scale(.92)}
#wstoast{position:fixed;left:50%;top:76px;transform:translateX(-50%) translateY(-10px);z-index:365;background:rgba(20,13,34,.95);border:2px solid #FFE9A0;border-radius:999px;padding:7px 14px;font-family:var(--f-px);font-size:13px;color:#FFF3C8;opacity:0;transition:all .4s;white-space:nowrap;box-shadow:0 0 14px rgba(255,233,160,.5)}#wstoast.on{opacity:1;transform:translateX(-50%) translateY(0)}
#wsw{}.wsw{position:fixed;z-index:364;transform:translate(-50%,-160%);font-family:var(--f-px);font-size:13px;color:#EAF2FF;text-shadow:0 0 8px #8FB8FF,0 1px 0 #1A1440;white-space:nowrap;opacity:0;transition:opacity .7s,transform 2.6s;pointer-events:none}.wsw.on{opacity:.95;transform:translate(-50%,-230%)}
#wsttl{position:fixed;left:0;right:0;top:9%;z-index:366;text-align:center;font-family:var(--f-pxb);color:#EAF4FF;font-size:24px;text-shadow:0 0 14px #9CC8FF,0 2px 0 #1A1440;opacity:0;transition:opacity 1s;pointer-events:none}#wsttl small{display:block;font-family:var(--f-px);font-size:13px;color:#D8E4FF;margin-top:6px;text-shadow:none}#wsttl.on{opacity:1}
#wsrw{position:fixed;left:50%;top:44%;z-index:367;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 18px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #B8D8FF;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(184,216,255,.45);pointer-events:none;width:min(86vw,320px);text-align:center}#wsrw.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#wsrw small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}#wsrw canvas{image-rendering:pixelated}`;
document.head.appendChild(css);
const el = (id, tag = 'div') => { const d = document.createElement(tag); d.id = id; document.body.appendChild(d); return d; };
const fx = el('wsfx', 'canvas'), card = el('wscard'), wr = el('wswrite'), tst = el('wstoast'), ttl = el('wsttl'), rw = el('wsrw');
// ---------- 쪽지 그림 (픽셀) ----------
function note(c, x, y, s, rot, a, glow){   // 접힌 소원 쪽지: 진한 테두리 · 하얀 종이 · 하늘색 접힌 선 · 은은한 빛
  c.save(); c.translate(x, y); c.rotate(rot); c.globalAlpha = a;
  if (glow){ const g = c.createRadialGradient(0, 0, 1, 0, 0, 9 * s); g.addColorStop(0, 'rgba(200,225,255,.55)'); g.addColorStop(1, 'rgba(200,225,255,0)'); c.fillStyle = g; c.fillRect(-9 * s, -9 * s, 18 * s, 18 * s); }
  c.fillStyle = '#2A2040'; c.fillRect(-4 * s, -3 * s, 8 * s, 6 * s); c.fillStyle = '#FBF6EA'; c.fillRect(-3 * s, -2 * s, 6 * s, 4 * s); c.fillStyle = '#CFE0F4'; c.fillRect(-3 * s, -2 * s, 6 * s, s); c.fillRect(0, -2 * s, s, 4 * s);
  c.fillStyle = '#FF9AB8'; c.fillRect(-s, 0, s, s); c.restore(); }
function star(c, x, y, s, col, a = 1){ c.globalAlpha = a; c.fillStyle = col; c.fillRect(x - s, y, s * 3, s); c.fillRect(x, y - s, s, s * 3); c.fillStyle = '#FFFFFF'; c.fillRect(x, y, s, s); c.globalAlpha = 1; }
// ---------- 하늘에서 쪽지가 눈처럼 ----------
let notes = [], flyers = [], sky = null, raf = 0; const L = 3;
for (let i = 0; i < 14; i++) notes.push({ x: Math.random(), y: -Math.random() * 1.2, v: .025 + Math.random() * .03, sw: Math.random() * 6, r: Math.random() * 6 });
function draw(now){
  const w = innerWidth, h = innerHeight; fx.width = Math.ceil(w / L); fx.height = Math.ceil(h / L); fx.style.width = w + 'px'; fx.style.height = h + 'px'; const c = fx.getContext('2d'); c.imageSmoothingEnabled = false; const W = fx.width, H = fx.height, t = now / 1000;
  if (sky){ const k = Math.min(1, (now - sky.t0) / 1500); c.globalAlpha = k * .92; for (let i = 0; i < 8; i++){ c.fillStyle = `rgb(${10 + i * 5},${12 + i * 6},${34 + i * 8})`; c.fillRect(0, i * H / 8, W, H / 8 + 1); } c.globalAlpha = 1;
    for (let i = 0; i < 70; i++) star(c, (i * 53) % W, (i * 29) % (H * .75), 1, '#BFD4FF', k * (.25 + .5 * Math.abs(Math.sin(t * 1.5 + i))));
    sky.draw(c, W, H, now); }
  if (!sky || sky.notes) notes.forEach(n => { if (n.land) return; n.y += n.v / 60; const x = (n.x + Math.sin(t * .9 + n.sw) * .03) * W, y = n.y * H; if (n.y > 1.05){ n.y = -.1; n.x = Math.random(); } note(c, x, y, 1, Math.sin(t * 1.3 + n.r) * .5, .95, true); });
  flyers = flyers.filter(f => { const k = Math.min(1, (now - f.t0) / f.d); const e = k * k * (3 - 2 * k); const x = f.x0 + (f.x1 - f.x0) * e + Math.sin(k * 9) * 6 * (1 - k), y = f.y0 + (f.y1 - f.y0) * e - Math.sin(e * Math.PI) * f.arc;
    if (f.kind === 'note'){ note(c, x, y, 1 + (1 - k), k * 4, 1, true); if (k > .85) star(c, x, y, 2, '#FFE9A0', (k - .85) / .15); }
    else { star(c, x, y, k > .9 ? 3 : 2, '#FFE9A0'); for (let j = 1; j < 6; j++){ const kk = Math.max(0, k - j * .03), ee = kk * kk * (3 - 2 * kk); star(c, f.x0 + (f.x1 - f.x0) * ee, f.y0 + (f.y1 - f.y0) * ee - Math.sin(ee * Math.PI) * f.arc, 1, '#FFF6C8', .7 - j * .12); } }
    if (k >= 1 && f.done){ f.done(); f.done = null; } return k < 1 || (f.hold && now - f.t0 < f.d + f.hold); });
  raf = requestAnimationFrame(draw); }
raf = requestAnimationFrame(draw);
const fly = (o) => new Promise(r => flyers.push({ ...o, t0: performance.now(), done: r }));
// 땅에 떨어진 쪽지: 맵 소품 (반짝 · 누르면 주워요)
const NOTE_IMG = (() => { const c = document.createElement('canvas'); c.width = c.height = 24; const q = c.getContext('2d'); q.imageSmoothingEnabled = false; note(q, 12, 14, 1.6, -.3, 1, true); return c; })();
let ground = []; const putG = () => World.setProps('town', ground.map(([x, y], i) => ({ id: 'wsn' + i, x, y, img: NOTE_IMG, pxc: NOTE_IMG.getContext('2d'), sw: 24, sh: 24, ax: 12, ay: 18, solid: false, light: { r: 14, c: [210, 230, 255], a: .6 } })), 'wsn');
const scr = () => { const r = (document.querySelector('#cv') || document.body).getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
async function readNote(text, who, cheer){
  mark('open'); card.innerHTML = `<div class="pp">「${text}」<small>${who}</small></div><div class="bt"><span class="go">★ 응원하기</span><span>다음에</span></div>`; card.classList.add('on'); await sleep(2600);
  if (cheer){ const b = card.querySelector('.go'); b.classList.add('hit'); mark('cheer'); await sleep(250); card.classList.remove('on'); const [cx, cy] = scr(); fly({ kind: 'star', x0: cx / L, y0: (cy - 40) / L, x1: (cx / L) + 30 - Math.random() * 60, y1: 18, d: 1400, arc: 20 }); await sleep(1500); }
  else { card.querySelector('.bt span:last-child').classList.add('hit'); await sleep(250); card.classList.remove('on'); await sleep(500); }
}
const toast = async (t, ms = 2600) => { tst.textContent = t; tst.classList.add('on'); mark('toast'); await sleep(ms); tst.classList.remove('on'); await sleep(400); };
window.__wsGo = async () => {
  World.setWeather('snow'); await sleep(2600);
  // 하늘에서 쪽지가 하나둘 내려와서 광장에 떨어져요
  mark('fall'); World.say('me', '....어, 눈 사이에 뭐가 같이 내려와.'); await sleep(2600);
  ground = [[43, 47], [40, 50], [46, 51]]; putG(); mark('land'); await sleep(1200);
  World.walkToTile(43, 48); await sleep(1800); World.faceTo(43, 47); await sleep(400);
  ground = ground.filter(g => !(g[0] === 43 && g[1] === 47)); putG(); mark('pick');
  await readNote('내일 수학 시험 잘 보게 해 주세요. 진짜 진짜로요.', '어느 학생의 소원', true);
  await toast('응원 별을 보냈어요 ★');
  World.walkToTile(40, 51); await sleep(2400); World.faceTo(40, 50); await sleep(300);
  ground = ground.filter(g => !(g[0] === 40 && g[1] === 50)); putG(); mark('pick');
  await readNote('이사 간 친구가 새 학교에서도 외롭지 않았으면 좋겠어요.', '어느 학생의 소원', true);
  // 내 소원 쓰기
  World.say('me', '나도 써 볼까.'); await sleep(1400);
  wr.innerHTML = `<b>내 소원 쓰기</b><div class="in"><span></span><i></i></div><div class="rw"><span>이름은 안 보여요 · <em>0</em> / 40</span><span class="go">날려 보내기</span></div>`; wr.style.display = 'block'; mark('write');
  const wish = '우리 반 모두 겨울 방학까지 안 아프게 해 주세요.', sp = wr.querySelector('.in span'), cnt = wr.querySelector('em');
  for (let k = 1; k <= wish.length; k++){ sp.textContent = wish.slice(0, k); cnt.textContent = k; if (k % 3 === 0) mark('type'); await sleep(85); } await sleep(900);
  wr.querySelector('.go').classList.add('hit'); await sleep(250); wr.style.display = 'none';
  // 쪽지가 접혀서 하늘로 → 별이 돼요
  const [cx, cy] = scr(); mark('send'); World.say('me', '닿아라.......'); await fly({ kind: 'note', x0: cx / L, y0: (cy - 30) / L, x1: cx / L + 10, y1: 14, d: 2600, arc: 30, hold: 1200 }); mark('starborn'); await sleep(1000);
  // 시간이 흘러.... 응원이 도착해요
  await sleep(800); World.say('me', '★'); await toast('누군가 내 소원을 응원했어요 ★ 1'); await toast('누군가 내 소원을 응원했어요 ★ 4', 2200); await toast('내 소원 응원 ★ 12 · 별이 조금 더 밝아졌어요', 2600);
  // 마지막 밤: 응원 받은 소원들이 별자리가 돼요
  await sleep(600); mark('sky');
  const PTS = [[.5, .28], [.5, .40], [.5, .52], [.5, .64], [.38, .46], [.62, .46], [.30, .40], [.70, .40], [.30, .54], [.70, .54], [.40, .32], [.60, .32], [.40, .60], [.60, .60]];   // 눈송이 모양
  const LINES = [[0, 1], [1, 2], [2, 3], [1, 4], [1, 5], [4, 6], [5, 7], [2, 8], [2, 9], [0, 10], [0, 11], [3, 12], [3, 13]];
  const WISH = ['시험 잘 보게 해 주세요', '할머니가 빨리 나으셨으면', '고양이 키우게 해 주세요', '친구랑 화해하고 싶어요', '우리 반 모두 안 아프게', '눈사람 크게 만들고 싶어', '키가 1 cm만 더', '엄마가 웃었으면 좋겠어요'];
  sky = { t0: performance.now(), notes: false, draw: (c, W, H, now) => { const t = (now - sky.t0) / 1000;
    PTS.forEach(([x, y], i) => { const k = Math.min(1, Math.max(0, (t - .8 - i * .18) / .5)); if (k > 0) star(c, x * W, y * H, i === 2 ? 3 : 2, '#FFE9A0', k); });
    c.strokeStyle = 'rgba(255,233,160,.55)'; c.lineWidth = 1; LINES.forEach(([a, b], j) => { const k = Math.min(1, Math.max(0, (t - 3.6 - j * .15) / .4)); if (k <= 0) return; const [x0, y0] = PTS[a], [x1, y1] = PTS[b]; c.beginPath(); c.moveTo(x0 * W, y0 * H); c.lineTo((x0 + (x1 - x0) * k) * W, (y0 + (y1 - y0) * k) * H); c.stroke(); });
  } };
  await sleep(4200); mark('link'); await sleep(2400); mark('words');
  for (let i = 0; i < WISH.length; i++){ const [x, y] = PTS[[6, 7, 8, 9, 10, 11, 12, 13][i]], d = document.createElement('div'); d.className = 'wsw'; d.textContent = WISH[i]; d.style.left = (x * 100) + '%'; d.style.top = (y * 100) + '%'; document.body.appendChild(d); requestAnimationFrame(() => d.classList.add('on')); setTimeout(() => { d.classList.remove('on'); setTimeout(() => d.remove(), 900); }, 1900); await sleep(950); }
  await sleep(2200);
  ttl.innerHTML = '첫눈 별자리<small>응원 받은 소원 128 개 · 응원 별 1,024 개</small>'; ttl.classList.add('on'); mark('title'); await sleep(3600); ttl.classList.remove('on'); await sleep(800);
  // 보상
  rw.innerHTML = `<canvas id="wsjar" width="32" height="32" style="width:112px;height:112px"></canvas>소원 유리병<small>방 가구 · 내가 응원한 소원 쪽지가 별빛으로 담겨 반짝여요<br>+ 말풍선 꾸미기 「눈송이 말풍선」</small>`;
  const q = rw.querySelector('#wsjar').getContext('2d'); q.imageSmoothingEnabled = false; const R = (x, y, w, h, col) => { q.fillStyle = col; q.fillRect(x, y, w, h); };
  R(9, 4, 14, 3, '#7A4A22'); R(10, 3, 12, 2, '#9A6A3A'); R(7, 7, 18, 22, '#2A2040'); R(8, 8, 16, 20, '#CFE4F8'); R(9, 9, 14, 18, '#E8F2FC'); R(9, 9, 3, 16, '#FFFFFF');
  [[13, 14], [18, 12], [16, 19], [20, 22], [12, 23], [15, 25]].forEach(([x, y], i) => { R(x - 1, y, 3, 1, i % 2 ? '#FFE9A0' : '#FFCFE0'); R(x, y - 1, 1, 3, i % 2 ? '#FFE9A0' : '#FFCFE0'); });
  R(8, 26, 16, 2, '#B8D0EC'); rw.classList.add('on'); mark('reward'); await sleep(3600); rw.classList.remove('on'); await sleep(600);
  sky.done = 1; cancelAnimationFrame(raf); window.__wsDone = true;
};
})();
