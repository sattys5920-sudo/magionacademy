// 「별빛 소원」 화면과 연출 (index.html이 필요할 때 불러요) — 처음 쪽지가 내리는 장면 · 쪽지 읽기와 응원(50 자 응원 글) · 내 소원 날려 보내기 · 마지막 별자리와 보상
//   window.WishFX = { intro, read, write, send, finale, note }
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
let AC = null, VOL = 1;
const ac = () => { try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); if (AC.state === 'suspended') AC.resume(); return AC; } catch(e){ return null; } };
function tone(f, d, type = 'sine', v = .1, at = 0){ const C = ac(); if (!C || !(VOL > 0)) return; const t = C.currentTime + at, o = C.createOscillator(), g = C.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); g.gain.setValueAtTime(.0001, t); g.gain.linearRampToValueAtTime(v * VOL, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(g); g.connect(C.destination); o.start(t); o.stop(t + d + .05); }
function noise(d, v = .1, at = 0){ const C = ac(); if (!C || !(VOL > 0)) return; const t = C.currentTime + at, b = C.createBuffer(1, Math.max(1, C.sampleRate * d), C.sampleRate), a = b.getChannelData(0); for (let i = 0; i < a.length; i++) a[i] = (Math.random() * 2 - 1) * (1 - i / a.length); const s = C.createBufferSource(), f = C.createBiquadFilter(), g = C.createGain(); s.buffer = b; f.type = 'highpass'; f.frequency.value = 2500; g.gain.value = v * VOL; s.connect(f); f.connect(g); g.connect(C.destination); s.start(t); }
const SND = {
  fall: () => { for (let k = 0; k < 6; k++) tone(2093 + k * 220, .8, 'sine', .03, k * .35); },
  open: () => { noise(.35, .08); tone(659, .4, 'triangle', .04, .1); },
  cheer: () => { for (let k = 0; k < 10; k++) tone(1046 * Math.pow(2, k / 12), .6, 'triangle', .05, k * .05); },
  send: () => { noise(2.2, .05); for (let k = 0; k < 14; k++) tone(880 * Math.pow(2, k / 12), 1, 'triangle', .04, .3 + k * .14); },
  star: () => [1568, 2093, 2637, 3136].forEach((f, k) => tone(f, .8, 'triangle', .06, k * .06)),
  sky: () => { [[130.8, .08], [196, .05], [261.6, .04]].forEach(([f, v]) => tone(f, 6, 'sine', v)); for (let k = 0; k < 14; k++) tone(1046 * Math.pow(2, [0, 4, 7, 12, 7, 4, 0, 2, 5, 9, 12, 9, 5, 2][k] / 12), .9, 'triangle', .04, .8 + k * .18); },
  title: () => [261.6, 329.6, 392, 523.3].forEach(f => tone(f, 3, 'sine', .06)),
  card: () => [1047, 1319, 1568, 2093].forEach((f, k) => tone(f, .6, 'triangle', .06, k * .07)),
};
// 오르골 (직접 만든 겨울 가락)
const MB = [76, 79, 81, 79, 76, 74, 76, 0, 72, 74, 76, 79, 77, 76, 74, 0, 74, 77, 79, 77, 74, 72, 74, 0, 71, 72, 74, 76, 72, 0, 0, 0];
let mbT = null; function musicbox(on, slow){ clearTimeout(mbT); if (!on) return; let i = 0; const nt = m => 440 * Math.pow(2, (m - 69) / 12); const go = () => { const m = MB[i % MB.length]; if (m){ tone(nt(m), 1.3, 'sine', .07); tone(nt(m + 12), .5, 'triangle', .02); } if (i % 4 === 0) tone(nt((i / 4) % 2 ? 48 : 52), 1.8, 'sine', .04); i++; mbT = setTimeout(go, slow ? 600 : 460); }; go(); }
// ---------- 그림 ----------
function note(c, x, y, s, rot, a, glow){ c.save(); c.translate(x, y); c.rotate(rot); c.globalAlpha = a;
  if (glow){ const g = c.createRadialGradient(0, 0, 1, 0, 0, 9 * s); g.addColorStop(0, 'rgba(200,225,255,.55)'); g.addColorStop(1, 'rgba(200,225,255,0)'); c.fillStyle = g; c.fillRect(-9 * s, -9 * s, 18 * s, 18 * s); }
  c.fillStyle = '#2A2040'; c.fillRect(-4 * s, -3 * s, 8 * s, 6 * s); c.fillStyle = '#FBF6EA'; c.fillRect(-3 * s, -2 * s, 6 * s, 4 * s); c.fillStyle = '#CFE0F4'; c.fillRect(-3 * s, -2 * s, 6 * s, s); c.fillRect(0, -2 * s, s, 4 * s); c.fillStyle = '#FF9AB8'; c.fillRect(-s, 0, s, s); c.restore(); }
function star(c, x, y, s, col, a = 1){ c.globalAlpha = a; c.fillStyle = col; c.fillRect(x - s, y, s * 3, s); c.fillRect(x, y - s, s, s * 3); c.fillStyle = '#FFFFFF'; c.fillRect(x, y, s, s); c.globalAlpha = 1; }
const NOTE = (() => { const c = document.createElement('canvas'); c.width = c.height = 24; const q = c.getContext('2d'); q.imageSmoothingEnabled = false; note(q, 12, 14, 1.6, -.3, 1, true); return c; })();
// ---------- 화면 ----------
const css = document.createElement('style'); css.textContent = `
#wsfx{position:fixed;inset:0;width:100vw;height:100vh;z-index:11;pointer-events:none;image-rendering:pixelated}
#wsread{position:fixed;inset:0;z-index:430;display:flex;align-items:center;justify-content:center;background:rgba(10,8,24,.45)}
#wsread .bx{width:min(88vw,320px);transform:rotate(-1deg);animation:wsin .45s cubic-bezier(.2,1.3,.4,1)}@keyframes wsin{from{transform:scale(.5) rotate(-6deg);opacity:0}}
#wsread .pp{position:relative;background:#FBF6EA;border:3px solid #3A2C4A;border-radius:4px;padding:22px 16px 14px;box-shadow:0 0 0 3px #CFE0F4,0 0 26px rgba(190,220,255,.7);font-family:var(--f-px);color:#3A2C4A;font-size:16px;line-height:25px;text-align:center;word-break:keep-all}
#wsread .pp:before{content:'';position:absolute;left:0;right:0;top:0;height:8px;background:repeating-linear-gradient(90deg,#CFE0F4 0 6px,transparent 6px 12px)}
#wsread .pp small{display:block;margin-top:8px;font-size:12px;color:#8A7AA0}
#wsread .shh{margin-top:10px;background:rgba(30,22,52,.96);border:2px dashed #FFE9A0;border-radius:10px;padding:7px 10px;font-family:var(--f-px);font-size:12px;line-height:18px;color:#FFF3C8}#wsread .shh b{font-family:var(--f-pxb);color:#FFE9A0;margin-right:3px}
#wsread textarea{display:block;width:100%;box-sizing:border-box;margin-top:10px;min-height:58px;resize:none;border-radius:10px;border:2px solid #B8D8FF;background:rgba(30,22,52,.96);color:#F1E9FF;font-family:var(--f-px);font-size:14px;line-height:20px;padding:8px 10px}
#wsread .cnt{text-align:right;font-family:var(--f-px);font-size:11px;color:#C8B8E8;margin-top:3px}#wsread .err{font-family:var(--f-px);font-size:12px;color:#FF9A9A;margin-top:4px;min-height:16px}
#wsread .bt{display:flex;gap:8px;margin-top:6px}#wsread .bt button{flex:1;min-height:44px;border-radius:12px;font-family:var(--f-pxb);font-size:14px;border:2px solid #B8D8FF;background:rgba(30,22,52,.96);color:#F1E9FF}
#wsread .bt button.go{background:#FFE9A0;color:#3A2414;border-color:#E8B84A}#wsread .bt button:disabled{opacity:.55}
#wsread .mine{margin-top:10px;background:rgba(30,22,52,.96);border:2px solid #FFE9A0;border-radius:10px;padding:8px 10px;font-family:var(--f-px);font-size:13px;color:#FFF3C8;line-height:19px}
#wsttl{position:fixed;left:0;right:0;top:9%;z-index:440;text-align:center;font-family:var(--f-pxb);color:#EAF4FF;font-size:24px;text-shadow:0 0 14px #9CC8FF,0 2px 0 #1A1440;opacity:0;transition:opacity 1s;pointer-events:none}#wsttl small{display:block;font-family:var(--f-px);font-size:13px;color:#D8E4FF;margin-top:6px;text-shadow:none}#wsttl.on{opacity:1}
.wsw{position:fixed;z-index:438;transform:translate(-50%,-160%);font-family:var(--f-px);font-size:13px;color:#EAF2FF;text-shadow:0 0 8px #8FB8FF,0 1px 0 #1A1440;white-space:nowrap;opacity:0;transition:opacity .7s,transform 2.6s;pointer-events:none;max-width:70vw;overflow:hidden;text-overflow:ellipsis}.wsw.on{opacity:.95;transform:translate(-50%,-230%)}.wsw.wsme{white-space:normal;width:min(80vw,320px);text-align:center;font-size:15px;line-height:22px;color:#FFF3C8;text-shadow:0 0 10px #E8B84A,0 1px 0 #1A1440}
#wsrw{position:fixed;left:50%;top:44%;z-index:441;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 18px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #B8D8FF;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(184,216,255,.45);pointer-events:none;width:min(86vw,320px);text-align:center}#wsrw.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#wsrw small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}`;
document.head.appendChild(css);
// 하늘 레이어 (쪽지가 내리고 · 별이 날아가요)
let fx = null, raf = 0, falling = [], flyers = [], sky = null; const L = 3;
function layer(on){ if (on && !fx){ fx = document.createElement('canvas'); fx.id = 'wsfx'; document.body.appendChild(fx); raf = requestAnimationFrame(draw); } if (!on && fx && !falling.length && !flyers.length && !sky){ cancelAnimationFrame(raf); fx.remove(); fx = null; } }
function draw(now){
  if (!fx) return; const w = innerWidth, h = innerHeight; fx.width = Math.ceil(w / L); fx.height = Math.ceil(h / L); fx.style.width = w + 'px'; fx.style.height = h + 'px'; const c = fx.getContext('2d'); c.imageSmoothingEnabled = false; const W = fx.width, H = fx.height, t = now / 1000;
  if (sky){ const k = Math.min(1, (now - sky.t0) / 1500); c.globalAlpha = k * .92; for (let i = 0; i < 8; i++){ c.fillStyle = `rgb(${10 + i * 5},${12 + i * 6},${34 + i * 8})`; c.fillRect(0, i * H / 8, W, H / 8 + 1); } c.globalAlpha = 1;
    for (let i = 0; i < 70; i++) star(c, (i * 53) % W, (i * 29) % (H * .75), 1, '#BFD4FF', k * (.25 + .5 * Math.abs(Math.sin(t * 1.5 + i)))); sky.draw(c, W, H, now); }
  falling = falling.filter(n => { n.y += n.v / 60; if (n.y > 1.05) return false; note(c, (n.x + Math.sin(t * .9 + n.sw) * .03) * W, n.y * H, 1, Math.sin(t * 1.3 + n.r) * .5, .95, true); return true; });
  flyers = flyers.filter(f => { const k = Math.min(1, (now - f.t0) / f.d), e = k * k * (3 - 2 * k), x = f.x0 + (f.x1 - f.x0) * e + Math.sin(k * 9) * 6 * (1 - k), y = f.y0 + (f.y1 - f.y0) * e - Math.sin(e * Math.PI) * f.arc;
    if (f.kind === 'note'){ note(c, x, y, 1 + (1 - k), k * 4, 1, true); if (k > .85) star(c, x, y, 2, '#FFE9A0', (k - .85) / .15); }
    else { star(c, x, y, k > .9 ? 3 : 2, '#FFE9A0'); for (let j = 1; j < 6; j++){ const kk = Math.max(0, k - j * .03), ee = kk * kk * (3 - 2 * kk); star(c, f.x0 + (f.x1 - f.x0) * ee, f.y0 + (f.y1 - f.y0) * ee - Math.sin(ee * Math.PI) * f.arc, 1, '#FFF6C8', .7 - j * .12); } }
    if (k >= 1 && f.done){ f.done(); f.done = null; } return k < 1; });
  if (!falling.length && !flyers.length && !sky){ fx.remove(); fx = null; return; }
  raf = requestAnimationFrame(draw);
}
const fly = o => new Promise(r => { layer(true); flyers.push({ ...o, t0: performance.now(), done: r }); });
const mid = () => { const r = (document.getElementById('cv') || document.body).getBoundingClientRect(); return [(r.left + r.width / 2) / L, (r.top + r.height / 2 - 40) / L]; };
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
// ================= 처음: 눈 사이로 쪽지가 같이 내려와요 =================
async function intro(api){ VOL = api.vol ?? 1; layer(true); for (let i = 0; i < 14; i++) falling.push({ x: Math.random(), y: -Math.random() * 1.2, v: .03 + Math.random() * .03, sw: Math.random() * 6, r: Math.random() * 6 }); SND.fall(); await sleep(1500); api.W.say('me', '....어, 눈 사이에 뭐가 같이 내려와.'); await sleep(4500); }
// ================= 누가 새 소원을 쓰면: 쪽지 몇 장이 하늘에서 내려와요 =================
async function fall(api){ VOL = api.vol ?? 1; layer(true); for (let i = 0; i < 6; i++) falling.push({ x: .2 + Math.random() * .6, y: -Math.random() * .4, v: .09 + Math.random() * .05, sw: Math.random() * 6, r: Math.random() * 6 }); SND.fall(); await sleep(2600); }
// ================= 쪽지 읽기 + 응원 (응원 글 50 자) =================
// o = { t 소원, n 응원 수, my { m } 이미 응원했으면, check(text) → 막을 까닭 또는 '' }  → { cheer: true, m } 또는 null
function read(api, o){ VOL = api.vol ?? 1; SND.open(); return new Promise(res => {
  const v = document.createElement('div'); v.id = 'wsread';
  v.innerHTML = `<div class="bx"><div class="pp">「${esc(o.t)}」<small>익명의 소원</small></div><div class="shh"><b>쉿!</b> 읽은 소원은 비밀이에요. 누구 소원인지 짐작하거나 다른 곳에서 말하지 않기로 약속해요.</div>
    ${o.my ? `<div class="mine">내가 보낸 응원 ★${o.my.m ? `<br>「${esc(o.my.m)}」` : ''}</div><div class="bt"><button data-x>닫기</button></div>`
      : `<textarea maxlength="50" placeholder="응원 한마디를 꼭 써 주세요 (익명 · 50 자까지)"></textarea><div class="cnt">0 / 50</div><div class="err"></div><div class="bt"><button class="go" data-go>★ 응원하기</button><button data-x>다음에</button></div>`}</div>`;
  document.body.appendChild(v); const ta = v.querySelector('textarea'), cnt = v.querySelector('.cnt'), err = v.querySelector('.err');
  if (ta) ta.oninput = () => { cnt.textContent = `${ta.value.length} / 50`; err.textContent = ''; };
  const close = r => { v.remove(); res(r); };
  v.querySelector('[data-x]').onclick = () => close(null); v.onclick = e => { if (e.target === v) close(null); };
  const go = v.querySelector('[data-go]'); if (go) go.onclick = async () => { const m = ta.value.trim().slice(0, 50); if (!m){ err.textContent = '응원 한마디를 써 주세요.'; ta.focus(); return; } const bad = o.check ? o.check(m) : ''; if (bad){ err.textContent = bad; return; }
    v.remove(); SND.cheer(); const [x, y] = mid(); fly({ kind: 'star', x0: x, y0: y, x1: x + 30 - Math.random() * 60, y1: 18, d: 1400, arc: 20 }); res({ cheer: true, m }); };
}); }
// ================= 내 소원: 쪽지가 접혀서 하늘로 → 별 =================
async function send(api){ VOL = api.vol ?? 1; SND.send(); const [x, y] = mid(); api.W.say('me', '닿아라.......'); await fly({ kind: 'note', x0: x, y0: y + 10, x1: x + 10, y1: 14, d: 2600, arc: 30 }); SND.star(); }
// ================= 마지막 밤: 내 소원 별자리 (내 소원 · 내게 온 응원만) + 보상 =================
async function finale(api, o){   // o = { mine 내 소원 글, cheers [내게 온 응원 글], n 응원 수, reward: html } · 다른 친구의 소원과 응원은 안 보여요
  VOL = api.vol ?? 1; api.bgm(true); musicbox(true, true); layer(true); fx.style.zIndex = 400;
  const PTS = [[.5, .28], [.5, .40], [.5, .52], [.5, .64], [.38, .46], [.62, .46], [.30, .40], [.70, .40], [.30, .54], [.70, .54], [.40, .32], [.60, .32], [.40, .60], [.60, .60]];
  const LINES = [[0, 1], [1, 2], [2, 3], [1, 4], [1, 5], [4, 6], [5, 7], [2, 8], [2, 9], [0, 10], [0, 11], [3, 12], [3, 13]];
  const ttl = document.createElement('div'); ttl.id = 'wsttl'; document.body.appendChild(ttl); const rw = document.createElement('div'); rw.id = 'wsrw'; document.body.appendChild(rw);
  try {
    SND.sky(); sky = { t0: performance.now(), draw: (c, W, H, now) => { const t = (now - sky.t0) / 1000;
      PTS.forEach(([x, y], i) => { const k = Math.min(1, Math.max(0, (t - .8 - i * .18) / .5)); if (k > 0) star(c, x * W, y * H, i === 2 ? 3 : 2, '#FFE9A0', k); });
      c.strokeStyle = 'rgba(255,233,160,.55)'; c.lineWidth = 1; LINES.forEach(([a, b], j) => { const k = Math.min(1, Math.max(0, (t - 3.6 - j * .15) / .4)); if (k <= 0) return; const [x0, y0] = PTS[a], [x1, y1] = PTS[b]; c.beginPath(); c.moveTo(x0 * W, y0 * H); c.lineTo((x0 + (x1 - x0) * k) * W, (y0 + (y1 - y0) * k) * H); c.stroke(); }); } };
    await sleep(6600);
    if (o.mine){ const d = document.createElement('div'); d.className = 'wsw wsme'; d.textContent = `「${o.mine}」`; d.style.left = '50%'; d.style.top = '20%'; document.body.appendChild(d); requestAnimationFrame(() => d.classList.add('on')); setTimeout(() => { d.classList.remove('on'); setTimeout(() => d.remove(), 900); }, 3200); await sleep(3400); }
    for (let i = 0; i < Math.min(8, o.cheers.length); i++){ const [x, y] = PTS[[6, 7, 8, 9, 10, 11, 12, 13][i]], d = document.createElement('div'); d.className = 'wsw'; d.textContent = '★ ' + o.cheers[i]; d.style.left = '50%'; d.style.top = (y * 100) + '%'; document.body.appendChild(d); requestAnimationFrame(() => d.classList.add('on')); setTimeout(() => { d.classList.remove('on'); setTimeout(() => d.remove(), 900); }, 1900); await sleep(950); }
    await sleep(1800); SND.title(); ttl.innerHTML = o.mine ? `나의 별빛 소원<small>응원 별 ${o.n} 개 · 쉿, 나만 보는 별자리</small>` : `별빛 소원<small>친구들의 소원이 별이 되어 올라갔어요</small>`; ttl.classList.add('on'); await sleep(3600); ttl.classList.remove('on'); await sleep(700);
    if (o.reward){ SND.card(); rw.innerHTML = o.reward; rw.classList.add('on'); await sleep(3800); rw.classList.remove('on'); await sleep(500); }
  } finally { sky = null; musicbox(false); ttl.remove(); rw.remove(); document.querySelectorAll('.wsw').forEach(x => x.remove()); api.bgm(false); }
}
window.WishFX = { intro, fall, read, send, finale, NOTE, SND };
})();
