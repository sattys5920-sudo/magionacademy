// 시안: 사역마 각성 「정령의 시련」 (실제 게임 위에서 연출만). world.js 사본에 World.__setWisp · World.__fsz 손잡이가 있어야 해요
(function(){
const C = '#FF5A28', NAME = 'Ignis', TITLE = '불사조';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ease = t => t < .5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2;
const css = document.createElement('style'); css.textContent = `
#awsay{position:fixed;left:0;right:0;bottom:calc(72px + env(safe-area-inset-bottom));z-index:305;display:none;justify-content:center;padding:0 10px}#awsay .evbox{width:100%;max-width:560px;margin:0;background:rgba(20,13,34,.96);border-color:${C}}#awsay .evtext{color:#F1E9FF;font-size:15px;line-height:22px;min-height:44px}#awsay .fqn{position:absolute;left:8px;top:-14px;background:${C};color:#14081E;border-radius:8px;padding:2px 10px;font-family:var(--f-pxb);font-size:var(--fs-s);line-height:1.4}
#awq{position:fixed;right:10px;top:64px;z-index:30;display:none;max-width:230px;padding:8px 10px;border-radius:12px;background:rgba(20,13,34,.92);border:1px solid ${C};box-shadow:0 0 10px ${C}66;font-family:var(--f-px);color:#F1E9FF;font-size:13px;line-height:18px}#awq b{display:block;font-family:var(--f-pxb);color:#FFB070;font-size:14px}#awq i{display:block;height:6px;border-radius:3px;background:#3A2C58;margin-top:6px;overflow:hidden}#awq i u{display:block;height:100%;background:${C};text-decoration:none;transition:width .5s}
#awcut{position:fixed;inset:0;z-index:310;background:#05030A;opacity:0;transition:opacity .9s;font-family:var(--f-pxb);color:#F1E9FF}#awcut canvas{position:absolute;left:50%;top:6%;height:56vh;transform:translateX(-50%);image-rendering:pixelated}
#awcut .tt{position:absolute;left:0;right:0;top:8%;text-align:center;font-size:34px;letter-spacing:6px;color:#fff}#awcut .tt span{display:inline-block;opacity:0;transform:translateY(8px) scale(1.3);filter:blur(4px);transition:all .6s;white-space:pre}#awcut .tt span.on{opacity:1;transform:none;filter:none;text-shadow:0 0 12px ${C},0 0 26px ${C}}
#awcut .st{position:absolute;left:0;right:0;top:15%;text-align:center;font-size:16px;color:#FFD0B0;opacity:0;transition:opacity .8s}
#awcut .fl{position:absolute;left:16px;right:16px;top:66%;text-align:center;font-size:21px;line-height:32px;color:#FFF0E6;word-break:keep-all}#awcut .fl span{display:inline-block;opacity:0;transform:translateY(6px);filter:blur(3px);transition:all .5s;white-space:pre}#awcut .fl span.on{opacity:1;transform:none;filter:none;text-shadow:0 0 8px ${C},0 0 18px ${C}}
#awfade{position:fixed;inset:0;z-index:320;background:#000;opacity:0;pointer-events:none;transition:opacity .9s}`;
document.head.appendChild(css);
const say = document.createElement('div'); say.id = 'awsay'; say.innerHTML = `<div class="evbox" style="position:relative"><div class="fqn">${NAME}</div><div class="evtext"></div><div class="evtap">▼</div></div>`; document.body.appendChild(say);
const q = document.createElement('div'); q.id = 'awq'; document.body.appendChild(q);
const fade = document.createElement('div'); fade.id = 'awfade'; document.body.appendChild(fade);
async function talk(t, hold = 1500){ say.style.display = 'flex'; const tx = say.querySelector('.evtext'); tx.textContent = ''; for (let i = 1; i <= t.length; i++){ tx.textContent = t.slice(0, i); await sleep(42); } await sleep(hold); say.style.display = 'none'; await sleep(250); }
function quest(n, tot){ q.style.display = 'block'; q.innerHTML = `<b>${NAME}의 시련 · 꺼지지 않는 불</b>요리를 성공하기 ${n} / ${tot}<i><u style="width:${n / tot * 100}%"></u></i>`; }
window.__awGo = async o => {
  await sleep(2500);
  await talk('....야. 부탁 하나만 하자. 딱히 너한테만 하는 건 아니고.');
  await talk('불을 다루는 걸 보고 싶어. 요리, 다섯 번. 태우면 처음부터다!', 1800);
  quest(0, 5); await sleep(1400);
  for (let i = 1; i <= 5; i++){ quest(i, 5); await sleep(700); }
  await sleep(600);
  await talk('....흥, 제법이네. 따라와. 보여 줄 게 있어.', 1600);
  q.style.display = 'none';
  // 각성 연출 컷
  fade.style.opacity = 1; await sleep(1000);
  const v = document.createElement('div'); v.id = 'awcut'; v.innerHTML = `<canvas width="320" height="180"></canvas><div class="tt"></div><div class="st"></div><div class="fl"></div>`; document.body.appendChild(v);
  const cv = v.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
  const BG = new Image(); BG.src = 'art/fam_altar.png?v=1'; const SP = new Image(); SP.src = 'art/wisps.png?v=1'; const SA = new Image(); SA.src = 'wisps_awake_anim.png';
  const S = { y: 70, sz: 12, ring: 0, dark: 0, pillar: 0, aw: 0, burst: 0, sp: [] }; let live = true;
  const draw = now => { if (!live) return; requestAnimationFrame(draw); g.clearRect(0, 0, 320, 180); if (BG.complete) g.drawImage(BG, 0, 0);
    g.fillStyle = `rgba(6,2,4,${.65 * S.dark})`; g.fillRect(0, 0, 320, 180);
    g.globalCompositeOperation = 'lighter';
    if (S.ring){ const t = now / 900; g.save(); g.translate(160, 140); g.scale(1, .32); for (let r = 0; r < 2; r++){ g.strokeStyle = `rgba(255,120,60,${.55 * S.ring})`; g.lineWidth = 2; g.beginPath(); g.arc(0, 0, 44 + r * 10, t * (r ? -1 : 1), t * (r ? -1 : 1) + Math.PI * 1.7); g.stroke(); }
      for (let i = 0; i < 8; i++){ const a = t + i / 8 * Math.PI * 2; g.fillStyle = `rgba(255,200,140,${S.ring})`; g.fillRect(Math.cos(a) * 49 - 1, Math.sin(a) * 49 - 1, 3, 3); } g.restore(); }
    if (S.pillar){ const gr = g.createLinearGradient(0, 0, 0, 180); gr.addColorStop(0, 'rgba(255,90,40,0)'); gr.addColorStop(.6, `rgba(255,120,60,${.35 * S.pillar})`); gr.addColorStop(1, 'rgba(255,90,40,0)'); g.fillStyle = gr; g.fillRect(160 - 20 * S.pillar, 0, 40 * S.pillar, 180); }
    const ey = S.y + Math.sin(now / 380) * 1.2, rad = S.sz * 2.6; const rg = g.createRadialGradient(160, ey, 0, 160, ey, rad); rg.addColorStop(0, 'rgba(255,110,50,.6)'); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.beginPath(); g.arc(160, ey, rad, 0, 7); g.fill();
    if (Math.random() < .7 * (S.ring + S.pillar)) S.sp.push({ x: 160 + (Math.random() - .5) * 60, y: 150, vy: -.04 - Math.random() * .05, t: now, life: 1400 });
    S.sp = S.sp.filter(p => now - p.t < p.life); S.sp.forEach(p => { const dt = now - p.t; g.globalAlpha = 1 - dt / p.life; g.fillStyle = '#FFB070'; g.fillRect(Math.round(p.x), Math.round(p.y + p.vy * dt), 1, 1); }); g.globalAlpha = 1;
    if (S.burst){ const k = (now - S.burst) / 1000; if (k < 1){ g.strokeStyle = `rgba(255,220,180,${1 - k})`; g.lineWidth = 3 * (1 - k); g.beginPath(); g.arc(160, ey, 8 + k * 110, 0, 7); g.stroke(); g.fillStyle = `rgba(255,240,220,${.45 * (1 - k)})`; g.fillRect(0, 0, 320, 180); } }
    g.globalCompositeOperation = 'source-over';
    const img = S.aw ? SA : SP; if (img.complete){ const fi = Math.floor(now / 110) % 8, sz = Math.round(S.sz * 1.9); g.drawImage(img, fi * 64, 6 * 64, 64, 64, Math.round(160 - sz / 2), Math.round(ey - sz * .62), sz, sz); } };
  requestAnimationFrame(draw); requestAnimationFrame(() => { v.style.opacity = 1; }); fade.style.opacity = 0; await sleep(1200);
  const anim = (ms, fn) => new Promise(res => { const t0 = performance.now(); const st = () => { const k = Math.min(1, (performance.now() - t0) / ms); fn(ease(k), k); if (k < 1) requestAnimationFrame(st); else res(); }; st(); });
  await anim(1500, e => { S.dark = e; S.ring = e; });
  await anim(2000, e => { S.y = 70 - 14 * e; S.pillar = e; S.sz = 12 + 6 * e; });
  await anim(1600, (e, k) => { S.sz = 18 + 6 * e + Math.sin(k * 30) * 1.5; });
  S.burst = performance.now(); S.aw = 1; S.sz = 30; await sleep(1100); await anim(900, e => { S.pillar = 1 - e * .6; });
  const tt = v.querySelector('.tt'); tt.innerHTML = NAME.split('').map(c => `<span>${c}</span>`).join(''); for (const s of tt.children){ await sleep(300); s.classList.add('on'); }
  await sleep(1200);
  const fl = v.querySelector('.fl'); fl.innerHTML = [...o.line].map(c => `<span>${c === ' ' ? ' ' : c}</span>`).join(''); for (const s of fl.children){ await sleep(s.textContent === '.' ? 150 : 105); s.classList.add('on'); }
  await sleep(2600);
  fade.style.opacity = 1; await sleep(1000); live = false; v.remove();
  World.__setWisp('wisps_awake_anim.png'); fade.style.opacity = 0; await sleep(1500);
  World.walkToTile(World.myPos().x + 3, World.myPos().y + 2); await sleep(3000);
  await talk('....뭘 봐. 멋있다고? ....알아, 나도.', 1600);
  await sleep(800); window.__awDone = true;
};
})();
