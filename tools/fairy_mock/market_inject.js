// 시안: 「요정 시장」 (보름달 밤 숲 가장자리) · 실제 게임 위에서 연출만 · window.__T.ic / itemId 손잡이가 있어야 해요
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ease = t => t < .5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2;
const FY = [   // 요정 셋: 이름 · 색 · 노점 자리(320×180) · 좋아하는 기억 · 파는 것
  { n: '미엘', c: '#FFC060', x: 72, y: 106, like: '따뜻함', item: '별사과', ln: { hi: '어머, 사람 아이다! 보름달 밤에 길을 찾아오다니, 운이 좋네요~', like: '어머어머, 따뜻해라.... 이런 기억은 꿀보다 달아요! 하나 더 얹어 줄게요~', meh: '음~ 나쁘지 않은 맛이에요. 고마워요~', bye: '다음 보름달에 또 와요~ 기억은 매일 새로 생기니까요' } },
  { n: '로웬', c: '#90D8FF', x: 160, y: 104, like: '고요', item: '꿈꽃', ln: { hi: '여기선 골드는 안 받아.... 오늘 있었던 일, 하나만 주면 돼', like: '....조용한 밤이었구나. 좋은 기억이야. 아껴 쓸게', meh: '....응. 받을게. 조금 시끄럽지만.......' } },
  { n: '시슬', c: '#E070C0', x: 248, y: 106, like: '장난', item: '그림자 버섯', ln: { hi: '키키! 재미없는 기억은 사절이다!', like: '키키키! 이거 맛있다! 들킬 뻔했지? 하나 더 얹어 주지!', meh: '흥, 착한 기억은 싱거워.... 그래도 받아 두지' } },
];
const MEM = [['연못에서 은빛 붕어를 낚았다', '기쁨'], ['Ignis에게 화룡초를 선물했다', '따뜻함'], ['민준에게 몰래 장난 마법을 걸었다', '장난'], ['혼자 언덕에서 별을 봤다', '고요']];
const css = document.createElement('style'); css.textContent = `
#fmcut{position:fixed;inset:0;z-index:310;background:#05030A;opacity:0;transition:opacity .9s;overflow:hidden;font-family:var(--f-px);color:#F1E9FF}#fmcut.on{opacity:1}
#fmcut canvas{position:absolute;left:50%;top:7%;height:55vh;width:auto;max-width:none;transform:translateX(-50%);image-rendering:pixelated}@media (min-aspect-ratio:1/1){#fmcut canvas{height:auto;width:min(100vw,1100px);top:4%}}
#fmsay{position:absolute;left:10px;right:10px;bottom:calc(24px + env(safe-area-inset-bottom));display:none}#fmsay .evbox{position:relative;max-width:560px;margin:0 auto;background:rgba(20,13,34,.96);border:2px solid var(--c);border-radius:14px;padding:14px 14px 12px}
#fmsay .evtext{font-size:15px;line-height:22px;min-height:44px;color:#F1E9FF}#fmsay .fqn{position:absolute;left:10px;top:-14px;background:var(--c);color:#14081E;border-radius:8px;padding:2px 10px;font-family:var(--f-pxb);font-size:var(--fs-s)}
#fmpick{position:absolute;left:10px;right:10px;bottom:calc(24px + env(safe-area-inset-bottom));display:none}#fmpick .box{max-width:560px;margin:0 auto;background:rgba(20,13,34,.96);border:2px solid #6A5A9A;border-radius:14px;padding:12px}
#fmpick .h{font-family:var(--f-pxb);font-size:15px;margin-bottom:8px;color:#FFE8A0}
#fmpick .items{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}#fmpick .it{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px;border-radius:12px;border:2px solid var(--c);background:#241A3C;color:#F1E9FF;font-family:var(--f-pxb);font-size:13px;min-height:44px}
#fmpick .it small{font-family:var(--f-px);opacity:.8;font-size:12px}#fmpick .it.on{background:#3A2C5A;box-shadow:0 0 12px var(--c)}
#fmpick .mem{display:flex;flex-direction:column;gap:6px}#fmpick .mem button{display:flex;justify-content:space-between;align-items:center;min-height:44px;padding:0 12px;border-radius:12px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-family:var(--f-px);font-size:14px;text-align:left}
#fmpick .mem button span{font-size:12px;color:#C8B8F0}#fmpick .mem button.on{background:#4A3A78;border-color:#FFE8A0}
.fmfly{position:fixed;z-index:330;font-family:var(--f-pxb);font-size:14px;color:#FFF6D0;text-shadow:0 0 8px #FFE8A0,0 0 16px #C8A0FF;white-space:nowrap;transition:all 1.4s cubic-bezier(.5,0,.3,1)}
#fmgot{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;align-items:center;gap:10px;padding:12px 18px;border-radius:16px;background:rgba(20,13,34,.95);border:2px solid #FFE8A0;font-family:var(--f-pxb);font-size:16px;box-shadow:0 0 22px rgba(255,232,160,.5)}#fmgot.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
#fmfx{position:fixed;inset:0;z-index:300;pointer-events:none}
.fmfade{position:fixed;inset:0;z-index:340;background:#000;opacity:0;pointer-events:none;transition:opacity .9s}`;
document.head.appendChild(css);
const fade = document.createElement('div'); fade.className = 'fmfade'; document.body.appendChild(fade);
// 맵 위: 요정 불빛 셋이 날아와 맴돌다 숲 쪽으로
async function mapLights(){
  const cv = document.createElement('canvas'); cv.id = 'fmfx'; cv.width = innerWidth; cv.height = innerHeight; document.body.appendChild(cv); const g = cv.getContext('2d');
  const cx = innerWidth / 2, cy = innerHeight * .47, L = FY.map((f, i) => ({ f, x: [-30, innerWidth / 2, innerWidth + 30][i], y: [innerHeight * .3, -30, innerHeight * .25][i], tr: [] })); let ph = 0, t0 = performance.now(), live = true;
  const draw = now => { if (!live) return; requestAnimationFrame(draw); g.clearRect(0, 0, cv.width, cv.height); const t = (now - t0) / 1000;
    L.forEach((l, i) => { let tx, ty; if (ph === 0){ const a = t * 1.6 + i * 2.1; tx = cx + Math.cos(a) * 34; ty = cy - 30 + Math.sin(a * 1.3) * 16; } else { tx = -60; ty = innerHeight * .38 - i * 14; }
      l.x += (tx - l.x) * (ph ? .025 : .045); l.y += (ty - l.y) * (ph ? .025 : .045); l.tr.push([l.x, l.y, now]); l.tr = l.tr.filter(p => now - p[2] < 700);
      g.globalCompositeOperation = 'lighter'; l.tr.forEach(p => { g.globalAlpha = (1 - (now - p[2]) / 700) * .7; g.fillStyle = l.f.c; g.fillRect(Math.round(p[0] + (Math.random() - .5) * 4), Math.round(p[1] + (Math.random() - .5) * 4), 2, 2); });
      g.globalAlpha = 1; const rg = g.createRadialGradient(l.x, l.y, 0, l.x, l.y, 14); rg.addColorStop(0, l.f.c); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.beginPath(); g.arc(l.x, l.y, 14, 0, 7); g.fill();
      g.fillStyle = '#fff'; g.fillRect(Math.round(l.x) - 1, Math.round(l.y) - 1, 3, 3); g.globalCompositeOperation = 'source-over'; }); };
  requestAnimationFrame(draw);
  await sleep(3200); World.say('me', '......?'); await sleep(2600); ph = 1; await sleep(1200);
  const p = World.myPos(); World.walkToTile(p.x - 4, p.y + 1); await sleep(2400);
  fade.style.opacity = 1; await sleep(1000); live = false; cv.remove();
}
window.__fmGo = async () => {
  await sleep(1500); await mapLights();
  const v = document.createElement('div'); v.id = 'fmcut'; v.innerHTML = `<canvas width="320" height="180"></canvas><div id="fmsay"><div class="evbox"><div class="fqn"></div><div class="evtext"></div></div></div><div id="fmpick"><div class="box"></div></div><div id="fmgot"></div>`; document.body.appendChild(v);
  const cv = v.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false; const BG = new Image(); BG.src = 'fairy_market.png';
  const S = { talk: -1, sp: [], pull: null }; let live = true;
  const fairy = (f, i, now) => { const bob = Math.sin(now / 420 + i * 1.7) * 2, x = f.x, y = f.y + bob, on = S.talk === i, fl = Math.abs(Math.sin(now / (on ? 45 : 70) + i));
    g.globalCompositeOperation = 'lighter'; const r = on ? 16 : 11, rg = g.createRadialGradient(x, y, 0, x, y, r); rg.addColorStop(0, f.c + (on ? 'cc' : '88')); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
    g.globalAlpha = .55; g.fillStyle = '#E8F0FF'; for (const s of [-1, 1]){ g.beginPath(); g.ellipse(x + s * 4, y - 2, 4, 1 + 3 * fl, s * .5, 0, 7); g.fill(); g.beginPath(); g.ellipse(x + s * 3, y + 2, 2.5, .6 + 2 * fl, -s * .4, 0, 7); g.fill(); }
    g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.fillStyle = f.c; g.fillRect(Math.round(x) - 1, Math.round(y) - 1, 3, 5); g.fillStyle = '#FFF6E0'; g.fillRect(Math.round(x) - 1, Math.round(y) - 4, 3, 3);
    if (Math.random() < .25) S.sp.push({ x: x + (Math.random() - .5) * 6, y: y + 3, vy: .01 + Math.random() * .02, t: now, life: 900, c: f.c }); };
  const draw = now => { if (!live) return; requestAnimationFrame(draw); g.clearRect(0, 0, 320, 180); if (BG.complete) g.drawImage(BG, 0, 0);
    FY.forEach((f, i) => fairy(f, i, now));
    if (S.pull){ const q = Math.min(1, (now - S.pull.t) / 1400), f = FY[S.pull.i]; for (let k = 0; k < 3; k++) S.sp.push({ x: 160 + (f.x - 160) * q + (Math.random() - .5) * 18 * (1 - q), y: 170 + (f.y - 170) * q + (Math.random() - .5) * 10, vy: -.01, t: now, life: 600, c: '#FFF6D0' }); if (q >= 1) S.pull = null; }
    g.globalCompositeOperation = 'lighter'; S.sp = S.sp.filter(p => now - p.t < p.life); S.sp.forEach(p => { const dt = now - p.t; g.globalAlpha = 1 - dt / p.life; g.fillStyle = p.c; g.fillRect(Math.round(p.x), Math.round(p.y + p.vy * dt), 1, 1); }); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; };
  requestAnimationFrame(draw); requestAnimationFrame(() => v.classList.add('on')); fade.style.opacity = 0; await sleep(1800);
  const say = v.querySelector('#fmsay'), pick = v.querySelector('#fmpick'), box = pick.querySelector('.box'), got = v.querySelector('#fmgot');
  const talk = async (i, t, hold = 1500) => { S.talk = i; say.style.setProperty('--c', FY[i].c); say.querySelector('.fqn').textContent = FY[i].n; say.style.display = 'block'; const tx = say.querySelector('.evtext'); tx.textContent = ''; for (let k = 1; k <= t.length; k++){ tx.textContent = t.slice(0, k); await sleep(38); } await sleep(hold); say.style.display = 'none'; S.talk = -1; await sleep(200); };
  const wait = sel => new Promise(res => box.querySelectorAll(sel).forEach(b => b.onclick = () => { b.classList.add('on'); setTimeout(() => res(b), 450); }));
  for (let i = 0; i < 3; i++) await talk(i, FY[i].ln.hi, 1300);
  const mem = MEM.slice();
  for (let round = 0; round < 2; round++){
    pick.style.display = 'block';
    box.innerHTML = `<div class="h">무엇과 바꿀까요?</div><div class="items">${FY.map((f, i) => `<button class="it" style="--c:${f.c}" data-fi="${i}">${__T.ic(__T.itemId(f.item))}${f.item}<small>${f.n} · 기억 1개</small></button>`).join('')}</div>`;
    const fi = +(await wait('[data-fi]')).dataset.fi, f = FY[fi];
    box.innerHTML = `<div class="h">오늘의 기억 하나를 건네요</div><div class="mem">${mem.map(([t, tag], i) => `<button data-mi="${i}">${t}<span>${tag}</span></button>`).join('')}</div>`;
    const bi = await wait('[data-mi]'), mi = +bi.dataset.mi, [mt, tag] = mem[mi], r = bi.getBoundingClientRect();
    const fl = document.createElement('div'); fl.className = 'fmfly'; fl.textContent = mt; fl.style.left = r.left + 12 + 'px'; fl.style.top = r.top + 12 + 'px'; document.body.appendChild(fl);
    pick.style.display = 'none'; const cr = cv.getBoundingClientRect(), fx = cr.left + f.x / 320 * cr.width, fy = cr.top + f.y / 180 * cr.height;
    await sleep(60); fl.style.left = fx - 40 + 'px'; fl.style.top = fy + 'px'; fl.style.opacity = 0; fl.style.transform = 'scale(.3)'; fl.style.filter = 'blur(3px)'; S.pull = { i: fi, t: performance.now() };
    await sleep(1500); fl.remove(); mem.splice(mi, 1);
    const like = tag === f.like; await talk(fi, like ? f.ln.like : f.ln.meh, 1600);
    got.innerHTML = `${__T.ic(__T.itemId(f.item))}${f.item} ×${like ? 2 : 1}`; got.classList.add('on'); await sleep(1900); got.classList.remove('on'); await sleep(500);
  }
  await talk(0, FY[0].ln.bye, 1600);
  fade.style.opacity = 1; await sleep(1000); live = false; v.remove(); fade.style.opacity = 0; await sleep(1600);
  World.say('me', '....어라, 어젯밤에 별을 봤던가?'); await sleep(3500); window.__fmDone = true;
};
})();
