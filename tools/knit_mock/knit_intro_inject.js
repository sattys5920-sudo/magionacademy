// 시안: 겨울 뜨개질 시작 연출 — 사육장에서 뜨개질하던 레오 → 「....어떻게 하는지 알려 줄까.」 → 두 손 뜨개 배우기(단계마다 레오 한마디) → 털실 네 뭉치 → 목도리 선물하면 레오가 두르고 다녀요
//   목업 사이트 폴더에 knit_view.html (두 손 뜨개 화면) · window.__kiGo() · window.__kiLog · window.__kiDone
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__kiLog = [], T0 = performance.now();
const mark = k => { LOG.push([(performance.now() - T0) / 1000, k]); const d = document.getElementById('vmk'); if (d) d.style.background = LOG.length % 2 ? '#FF0000' : '#0000FF'; };
if (!document.getElementById('vmk')) document.body.insertAdjacentHTML('beforeend', '<div id="vmk" style="position:fixed;left:0;top:0;width:6px;height:6px;z-index:99999;background:#00FF00;pointer-events:none"></div>');
const css = document.createElement('style'); css.textContent = `
#kidim{position:fixed;inset:0;background:rgba(10,8,24,.45);opacity:0;transition:opacity .6s;z-index:300;pointer-events:none}
#kisay{position:fixed;left:10px;right:10px;bottom:150px;z-index:340;display:none}#kisay .bx{max-width:370px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.97);border:2px solid #C8B8E8;border-radius:14px;padding:10px 12px}
#kisay .fc{width:54px;height:54px;flex:none;border-radius:10px;background:#3A2E58;overflow:hidden}#kisay .fc img{width:100%;height:100%;image-rendering:pixelated}#kisay b{display:block;font-family:var(--f-pxb);font-size:14px;color:#FFD8A8;margin-bottom:2px}#kisay p{margin:0;font-family:var(--f-px);font-size:14px;line-height:21px;color:#F1E9FF}
#kiask{position:fixed;left:50%;bottom:96px;transform:translateX(-50%);z-index:341;display:none;gap:8px}#kiask span{padding:9px 16px;border-radius:12px;background:#2A2040;border:2px solid #6A5A90;font-family:var(--f-pxb);font-size:14px;color:#F1E9FF;white-space:nowrap}#kiask span.go{background:#FFB8A8;border-color:#FFB8A8;color:#3A1A14}#kiask span.hit{transform:scale(.93)}
#kiv{position:fixed;left:50%;top:40%;transform:translate(-50%,-50%) scale(.9);opacity:0;transition:all .4s cubic-bezier(.2,1.3,.4,1);z-index:330;width:min(94vw,370px);background:rgba(20,13,34,.97);border:2px solid #FFB8A8;border-radius:16px;padding:10px;text-align:center;box-shadow:0 0 24px rgba(255,184,168,.3)}#kiv.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
#kiv h3{margin:0 0 6px;font-family:var(--f-pxb);font-size:16px;color:#FFE0C8}#kiv iframe{width:100%;aspect-ratio:240/230;border:0;display:block;border-radius:10px;background:#2A1E3A}#kiv .st{font-family:var(--f-pxb);font-size:17px;color:#FFE9A0;margin-top:6px;min-height:22px}
#kicard{position:fixed;left:50%;top:40%;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .45s cubic-bezier(.2,1.3,.4,1);z-index:345;background:rgba(20,13,34,.97);border:2px solid #FFE9A0;border-radius:16px;padding:14px 18px;text-align:center;font-family:var(--f-pxb);color:#FFF3C8;width:min(80vw,280px)}#kicard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#kicard small{display:block;font-family:var(--f-px);font-size:13px;color:#E0D4F4;margin-top:6px;line-height:19px}#kicard canvas{display:block;margin:6px auto;image-rendering:pixelated}
#kitoast{position:fixed;left:50%;top:76px;transform:translate(-50%,-10px);z-index:345;background:rgba(20,13,34,.95);border:2px solid #FFB8A8;border-radius:12px;padding:8px 14px;font-family:var(--f-px);font-size:13px;color:#F1E9FF;opacity:0;transition:all .3s;white-space:nowrap}#kitoast.on{opacity:1;transform:translate(-50%,0)}`;
document.head.appendChild(css);
const el = (id, h = '') => { const d = document.createElement('div'); d.id = id; d.innerHTML = h; document.body.appendChild(d); return d; };
const dim = el('kidim'), say = el('kisay', '<div class="bx"><div class="fc"><img></div><div><b></b><p></p></div></div>'), ask = el('kiask'), v = el('kiv'), card = el('kicard'), tst = el('kitoast');
const A = World.Avatar, LEO = A.fromLook(5), NECK = A.meta.parts.neck.findIndex(p => p.id === 'neck_4');
async function line(t, hold = 1400, who = '레오', face = 1){ say.querySelector('img').src = face ? A.head(LEO) : A.head(__T.me().av) || ''; say.querySelector('b').textContent = who; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; mark('line');
  for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(30); } await sleep(hold + t.length * 20); say.style.display = 'none'; await sleep(140); }
const toast = async (t, ms = 2200) => { tst.textContent = t; tst.classList.add('on'); mark('toast'); await sleep(ms); tst.classList.remove('on'); await sleep(300); };
// 레오: 의자에 앉아 뜨개질 (손에 바늘 두 개가 딸깍딸깍 · 아래로 빨간 뜨개가 늘어져요) / 목도리 두른 레오
let knitting = true, scarfOn = false, tick = 0;
function leoProp(){ const t = World.meTile(), S = A.compose(scarfOn ? { ...LEO, neck: NECK } : LEO); if (!S) return; const HB = A.meta.head, fx = Math.floor(HB.x / A.FW) * A.FW, fy = Math.floor(HB.y / A.FH) * A.FH;
  const K = .68, W = Math.round(A.FW * K), H = Math.round(A.FH * K), c = document.createElement('canvas'); c.width = W; c.height = H; const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(S, fx, fy, A.FW, A.FH, 0, 0, W, H);
  if (knitting){ const s = K, ph = tick % 2, L_ = (x0, y0, x1, y1, col) => { q.strokeStyle = col; q.lineWidth = 1; q.beginPath(); q.moveTo(x0 * s, y0 * s); q.lineTo(x1 * s, y1 * s); q.stroke(); };
    q.fillStyle = '#E0505A'; q.fillRect(28 * s, 45 * s, 8 * s, (5 + (tick % 8) / 4) * s); q.fillStyle = '#F4F0E8'; q.fillRect(28 * s, 47 * s, 8 * s, 1);   // 뜨는 중인 줄무늬 천
    L_(23, 46 - ph, 37, 41 + ph, '#E8DCC0'); L_(41, 46 + ph, 27, 41 - ph, '#E8DCC0'); q.fillStyle = '#E0505A'; q.beginPath(); q.arc(44 * s, 56 * s, 2.4, 0, 7); q.fill(); }
  World.setProps(t.m, [{ id: 'kileo', x: t.x + 1, y: t.y - 1, img: c, pxc: q, sw: W, sh: H, ax: W / 2, ay: H - 3, solid: false }], 'kileo'); }
let clickT = 0;
window.__kiGo = async () => {
  try { World.setWeather('snow'); } catch(e){}
  const iv = setInterval(() => { tick++; leoProp(); if (knitting && tick % 2 === 0) mark('click'); }, 280);
  await sleep(500); await toast('오늘 밤은 유난히 추워요.......', 2000);
  await sleep(1600);   // 레오가 혼자 딸깍딸깍
  World.say('me', '.......?'); await sleep(1200);
  dim.style.opacity = 1;
  await line('....뭐. 보지 마. 양들 겨울 털 남은 걸로 뜨는 거야.', 1400);
  await line('....어떻게 하는지 알려 줄까.', 900);
  ask.innerHTML = '<span>다음에</span><span class="go">응</span>'; ask.style.display = 'flex'; mark('open'); await sleep(1300); const b = ask.querySelector('.go'); b.classList.add('hit'); mark('pick'); await sleep(200); ask.style.display = 'none';
  World.say('me', '응, 알려 줘.......'); await sleep(1000);
  knitting = false;
  await line('바늘 두 개 쥐어. 왼손은 꽉, 오른손은 부드럽게.', 1000);
  // 두 손 뜨개 화면 (knit_view.html) — 단계마다 레오 한마디
  v.innerHTML = '<h3>레오와 뜨개질 배우기</h3><iframe src="knit_view.html?embed=1"></iframe><div class="st"></div>'; v.classList.add('on'); mark('open');
  const fr = v.querySelector('iframe'); await new Promise(r => fr.onload = r); await sleep(400); const W_ = fr.contentWindow, kn = W_.__kn, st = v.querySelector('.st');
  kn.set({ reset: 1 }); kn.set({ phase: 'knit', L: { cx: 30, cy: 200 } }); const K = kn.K; K.cast = 0; K.j = 8; K.rt = kn.RT0.slice();
  const tw = (ms, fn) => new Promise(res => { const t0 = performance.now(); const f = () => { const p = Math.min(1, (performance.now() - t0) / ms); fn(p); if (p < 1) requestAnimationFrame(f); else res(); }; requestAnimationFrame(f); });
  const R = { cx: 190, cy: 170 };
  async function stitch(slow){
    const l0 = kn.leftLoopPos(0), r0 = K.rt.slice(), ms = slow ? 900 : 260;
    if (slow){ st.textContent = '쏙 · 찔러 넣기'; } kn.set({ st: 'insert', R }); await tw(ms, p => { K.rt = [r0[0] + (l0[0] - 1 - r0[0]) * p, r0[1] + (l0[1] + 1 - r0[1]) * p]; R.cx = 190 - 60 * p; R.cy = 170 - 50 * p; }); K.inserted = true; mark('insert');
    if (slow){ await line('끝을 고리에 넣어. 앞에서 뒤로.', 500); st.textContent = '빙글 · 실 감기'; } kn.set({ st: 'wrap' }); await tw(slow ? 1000 : 300, p => { K.wrapA = p * 6.4; R.cx = 130 + Math.cos(p * 6.3) * 10; R.cy = 120 + Math.sin(p * 6.3) * 10; }); K.newLoop = .4; mark('wrap');
    if (slow){ await line('실 한 바퀴 감고.', 400); st.textContent = '쭉 · 빼내기'; } kn.set({ st: 'pull' }); const pin = K.rt.slice(); await tw(slow ? 800 : 240, p => { K.rt = [pin[0] + 14 * p, pin[1] + 10 * p]; K.newLoop = .4 + .6 * p; R.cx = 130 + 40 * p; R.cy = 120 + 40 * p; }); K.inserted = false; mark('pull');
    if (slow){ await line('빼내고.... 헌 고리는 왼손으로 밀어서 빼.', 500); st.textContent = '툭 · 헌 고리 빼기'; } kn.set({ st: 'slip', L: { cx: 22, cy: 208 } }); await tw(slow ? 700 : 220, p => { K.lpull = 12 * Math.sin(p * 3.14); K.drop = p; }); K.drop = null; K.newLoop = 0; K.wrapA = 0; K.j--; kn.set({ L: { cx: 30, cy: 200 } }); mark('slip');
    const back = K.rt.slice(); await tw(slow ? 300 : 120, p => { K.rt = [back[0] + (kn.RT0[0] - back[0]) * p, back[1] + (kn.RT0[1] - back[1]) * p]; R.cx = 190; R.cy = 170; });
  }
  await stitch(true); st.textContent = '한 코 완성!'; mark('perfect');
  await line('....그래, 그거야. 한 코 뜬 거다.', 900);
  st.textContent = '쏙 · 빙글 · 쭉 · 툭'; for (let i = 0; i < 7; i++) await stitch(false);
  st.textContent = '한 줄 완성!'; mark('perfect'); await sleep(1100); v.classList.remove('on'); await sleep(450); v.innerHTML = '';
  await line('....손이 빠르네. 처음치곤 나쁘지 않아.', 900);
  await line('털실 네 뭉치 줄게. 다 쓰면 양털로 물레 돌려서 만들어.', 1100);
  card.innerHTML = '<canvas width="64" height="24" id="kiyarn" style="width:192px;height:72px"></canvas>털실 4 뭉치<small>빨강 2 · 하양 2 · 목도리는 털실 10 뭉치 · 인형은 20 뭉치<br>사육장 물레에서 양털로 더 만들 수 있어요</small>'; const yc = card.querySelector('canvas').getContext('2d');
  [['#E0505A', 8], ['#E0505A', 24], ['#F4F0E8', 40], ['#F4F0E8', 56]].forEach(([c, x]) => { yc.fillStyle = '#1a1024'; yc.beginPath(); yc.arc(x, 12, 7, 0, 7); yc.fill(); yc.fillStyle = c; yc.beginPath(); yc.arc(x, 12, 6, 0, 7); yc.fill(); yc.strokeStyle = 'rgba(0,0,0,.2)'; for (let k = -4; k < 6; k += 3){ yc.beginPath(); yc.moveTo(x - 5, 12 + k); yc.quadraticCurveTo(x, 12 + k + 2, x + 5, 12 + k); yc.stroke(); } });
  card.classList.add('on'); mark('card'); await sleep(2600); card.classList.remove('on'); await sleep(450);
  dim.style.opacity = 0; await sleep(500);
  // 며칠 뒤: 목도리를 떠서 레오에게 선물
  await toast('며칠 뒤.......', 1600);
  dim.style.opacity = 1; World.say('me', '레오, 이거.......'); await sleep(1200);
  card.innerHTML = '<canvas width="24" height="24" id="kisc" style="width:96px;height:96px"></canvas>빨강 · 하양 줄무늬 목도리<small>레오에게 선물했어요</small>'; const sc = card.querySelector('canvas').getContext('2d'), Rr = (x, y, w, h, c) => { sc.fillStyle = c; sc.fillRect(x, y, w, h); };
  Rr(3, 4, 18, 6, '#1a1024'); for (let i = 0; i < 4; i++) Rr(4 + i * 4, 5, 4, 4, i % 2 ? '#F4F0E8' : '#E0505A'); Rr(14, 9, 6, 12, '#1a1024'); for (let i = 0; i < 3; i++) Rr(15, 10 + i * 3, 4, 3, i % 2 ? '#F4F0E8' : '#E0505A'); Rr(15, 21, 1, 2, '#E0505A'); Rr(17, 21, 1, 2, '#E0505A');
  card.classList.add('on'); mark('gift'); await sleep(2000); card.classList.remove('on'); await sleep(400);
  await line('....이거, 나 주는 거야.', 900);
  await line('누가 나한테 뭘 떠 준 건.... 처음이다. 생물들한텐 매일 뭘 챙겨 주면서, 정작 내 목은 늘 비어 있었거든.', 1500);
  scarfOn = true; leoProp(); mark('sparkle');
  await line('밤에 알 지키러 나갈 때 바람이 제일 매서웠는데.... 이제 괜찮겠다.', 1300);
  await line('....고맙다. 내일부터 하고 다닐게. 아니, 지금부터.', 1500);
  dim.style.opacity = 0; await toast('레오가 목도리를 두르고 다녀요', 2400);
  clearInterval(iv); await sleep(600); window.__kiDone = true;
};
})();
