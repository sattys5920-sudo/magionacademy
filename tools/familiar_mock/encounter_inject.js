// 시안: 정령과 처음 만나는 이벤트 「꺼지지 않는 불씨」 (실제 캠퍼스 맵 위에서 연출만 흉내 내요)
//   world.js 에 World.__cam · World.__P 손잡이가 있어야 해요. window.__encGo() 로 시작하고, 끝나면 window.__encDone = true
(function(){
const SPR = new Image(); SPR.src = 'wisps3_anim.png';
const cv = document.getElementById('cv'), ov = document.createElement('canvas'), g = ov.getContext('2d');
ov.style.cssText = 'position:fixed;pointer-events:none;z-index:5;image-rendering:pixelated'; document.body.appendChild(ov);
const dark = document.createElement('div'); dark.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:6;opacity:0;transition:opacity 1.6s'; document.body.appendChild(dark);
const top = document.createElement('canvas'); top.style.cssText = 'position:fixed;pointer-events:none;z-index:7;image-rendering:pixelated'; document.body.appendChild(top); const g2 = top.getContext('2d');
const nameEl = document.createElement('div'); nameEl.style.cssText = 'position:fixed;left:0;right:0;z-index:26;text-align:center;font-family:var(--f-pxb);font-size:40px;letter-spacing:10px;color:#fff;pointer-events:none';
document.body.appendChild(nameEl);
const dlg = document.createElement('div'); dlg.style.cssText = 'position:fixed;left:0;right:0;bottom:64px;z-index:25;display:none;justify-content:center';
dlg.innerHTML = '<div class="evwrap"><div class="evbox"><div class="evname"></div><div class="evtext"></div><div class="evch"></div><div class="evtap">▼</div></div></div>'; document.body.appendChild(dlg);
const bub = document.createElement('div'); bub.style.cssText = 'position:fixed;z-index:9;display:none;gap:6px;transform:translate(-50%,-100%);padding:6px;border-radius:12px;background:rgba(20,13,30,.92);border:1px solid #5A8CFF;box-shadow:0 0 10px #5A8CFF88';
bub.innerHTML = '<button class="encch" style="padding:0 12px;white-space:nowrap">사역마 창</button><button class="encch" style="padding:0 12px;white-space:nowrap">선물하기</button>'; document.body.appendChild(bub);
const gift = document.createElement('div'); gift.style.cssText = 'position:fixed;left:0;right:0;bottom:64px;z-index:9;display:none;justify-content:center';
const GI = [['I19', '달빛 이슬', 6], [26, '은방울꽃', 2], [24, '고추', 3], [7, '당근', 5], [12, '해바라기 씨', 2], [44, '꿈꽃', 1]];
const gic = n => typeof n === 'string' ? `background:url(art/icons.png?v=4) ${-(+n.slice(1)) * 32}px 0 no-repeat` : `background:url(art/plants.png?v=4) ${-(n % 10) * 32}px ${-Math.floor(n / 10) * 32}px no-repeat`;
gift.innerHTML = `<div style="width:100%;max-width:560px;margin:0 10px;background:#211733;border:1px solid #4E3C72;border-radius:16px;padding:12px;font-family:var(--f-px);color:#F1E9FF"><div style="display:flex;align-items:center"><b style="flex:1;font-family:var(--f-pxb);font-size:16px;color:#FFE9A0">Vael에게 선물하기</b><span style="font-size:13px;color:#BFB0E0">오늘 1번 줄 수 있어요</span></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px">${GI.map(([n, nm, c], i) => `<div class="encch" data-g="${i}" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:74px;gap:2px"><span style="width:32px;height:32px;image-rendering:pixelated;${gic(n)}"></span><span style="font-size:13px">${nm} ×${c}</span></div>`).join('')}</div></div>`; document.body.appendChild(gift);
const scene = document.createElement('div'); scene.style.cssText = 'position:fixed;inset:0;z-index:20;background:#05030A;display:none;opacity:0;transition:opacity .9s';
const sc = document.createElement('canvas'); sc.width = 320; sc.height = 180; sc.style.cssText = 'position:absolute;left:50%;top:7%;height:58vh;transform:translateX(-50%);image-rendering:pixelated'; scene.appendChild(sc); document.body.appendChild(scene);
const sg = sc.getContext('2d'); sg.imageSmoothingEnabled = false; const BG = new Image(); BG.src = 'familiar_altar.png';
const fade = document.createElement('div'); fade.style.cssText = 'position:fixed;inset:0;z-index:30;background:#000;opacity:0;pointer-events:none;transition:opacity .9s'; document.body.appendChild(fade);
const C = window.__encS = { on: 0, ember: [160, 60], sz: 10, hue: null, spirit: -1, burst: 0, sparks: [], av: null, dark: 0 };
function sceneDraw(now){ requestAnimationFrame(sceneDraw); if (!C.on) return; sg.clearRect(0, 0, 320, 180); if (BG.complete) sg.drawImage(BG, 0, 0);
  if (C.dark){ sg.fillStyle = `rgba(4,2,10,${.6 * C.dark})`; sg.fillRect(0, 0, 320, 180); }
  // 룬이 숨 쉬듯
  sg.globalCompositeOperation = 'lighter'; const rp = .25 + .35 * Math.abs(Math.sin(now / 700)) + (C.glow || 0) * .4; { const gr = sg.createRadialGradient(160, 110, 0, 160, 110, 22); gr.addColorStop(0, `rgba(90,128,200,${rp * .45})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); sg.fillStyle = gr; sg.fillRect(130, 90, 60, 40); } sg.globalCompositeOperation = 'source-over';
  if (C.av){ const fr = World.Avatar.meta.dirs.up * 64; sg.drawImage(C.av, fr, 0, 64, 64, 128, 118, 64, 64); }
  const [ex, ey] = [C.ember[0], C.ember[1] + Math.sin(now / 380) * 1.2], col = C.spirit >= 0 ? '90,140,255' : '255,232,176';
  sg.globalCompositeOperation = 'lighter'; const rad = C.sz * 2.4 * (.85 + .15 * Math.sin(now / 260));
  let rg = sg.createRadialGradient(ex, ey, 0, ex, ey, rad); rg.addColorStop(0, C.hue !== null ? `hsla(${C.hue},90%,65%,.6)` : `rgba(${col},.55)`); rg.addColorStop(1, 'rgba(0,0,0,0)'); sg.fillStyle = rg; sg.beginPath(); sg.arc(ex, ey, rad, 0, 7); sg.fill();
  if (C.burst){ const k = (now - C.burst) / 900; if (k < 1){ sg.strokeStyle = `rgba(200,225,255,${1 - k})`; sg.lineWidth = 2 * (1 - k); sg.beginPath(); sg.arc(ex, ey, 6 + k * 90, 0, 7); sg.stroke(); sg.fillStyle = `rgba(255,255,255,${.3 * (1 - k)})`; sg.fillRect(0, 0, 320, 180); } }
  if (C.ritual) for (let i = 0; i < 2; i++) C.sparks.push({ x: ex + (Math.random() - .5) * 26, y: ey + 10, vy: -.015 - Math.random() * .03, t: now, life: 900 + Math.random() * 700, h: C.hue });
  C.sparks = C.sparks.filter(p => now - p.t < p.life); for (const p of C.sparks){ const dt = now - p.t; sg.globalAlpha = 1 - dt / p.life; sg.fillStyle = p.h !== null && C.spirit < 0 ? `hsl(${p.h},90%,70%)` : '#A8D0FF'; sg.fillRect(Math.round(p.x), Math.round(p.y + p.vy * dt), 1, 1); }
  sg.globalAlpha = 1; sg.globalCompositeOperation = 'source-over';
  if (SPR.complete){ const fi = Math.floor(now / 110) % 8, sz = Math.round(C.sz * 1.9); sg.filter = C.spirit >= 0 ? 'none' : C.hue !== null ? `hue-rotate(${C.hue - 220}deg) saturate(1.6) brightness(1.15)` : 'saturate(0) brightness(1.7) sepia(.5)';
    sg.drawImage(SPR, fi * 64, (C.spirit >= 0 ? C.spirit : 0) * 64, 64, 64, Math.round(ex - sz / 2), Math.round(ey - sz * .62), sz, sz); sg.filter = 'none'; }
}
requestAnimationFrame(sceneDraw);
const css = document.createElement('style'); css.textContent = `.encch{min-height:44px;border-radius:12px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-family:var(--f-pxb);font-size:15px;transition:all .2s}.encch.on{background:#FF9A3C;border-color:#C86A1E;color:#2A1606;transform:scale(1.02)}
.enclt{display:inline-block;opacity:0;transform:translateY(8px) scale(1.4);filter:blur(4px);transition:all .7s}.enclt.on{opacity:1;transform:none;filter:none;text-shadow:0 0 12px var(--c),0 0 26px var(--c)}`; document.head.appendChild(css);
// 제단의 물음 10개 (실제 배정은 관리자가 미리 정해 두고, 물음은 분위기용. 매번 5개를 뽑아요)
const ENC_Q = [
  ['어둠 속에서 길을 잃었다. 너는?', ['가만히 기다린다', '크게 소리친다', '더듬어 걷는다']],
  ['「열지 마시오」라고 적힌 낡은 상자가 있다.', ['그대로 둔다', '살짝 열어 본다', '누군가에게 묻는다']],
  ['밤하늘에서 가장 먼저 찾는 것은?', ['가장 밝은 별', '둥근 달', '별 사이의 어둠']],
  ['꿈속에서 누군가 네 이름을 부른다.', ['대답한다', '숨는다', '소리 나는 쪽으로 간다']],
  ['불 하나만 가질 수 있다면?', ['흔들리지 않는 촛불', '타닥이는 모닥불', '떠도는 도깨비불']],
  ['거울 속의 네가 먼저 웃었다.', ['같이 웃어 준다', '거울을 덮는다', '말을 걸어 본다']],
  ['오래된 숲의 나무가 길을 막아섰다.', ['돌아서 간다', '지나가도 되냐고 묻는다', '틈을 비집고 지난다']],
  ['잃어버려도 괜찮은 것 하나를 고른다면?', ['기억 한 조각', '하루 동안의 목소리', '내 그림자']],
  ['비가 그치지 않는 밤, 너는 어디에 있는가?', ['창가에 앉아', '이불 속에', '빗속 한가운데']],
  ['마지막으로, 너는 무엇이 되고 싶은가?', ['길을 비추는 빛', '곁을 지키는 불', '아무도 모르는 불씨']],
];
const sleep = ms => new Promise(r => setTimeout(r, ms));
const E = window.__enc = { ember: null, sz: 14, hue: null, spirit: -1, sparks: [], trail: [], altar: null, glow: 0, burst: 0, grey: 1 };
const ease = t => t < .5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2;
function flyTo(x, y, ms){ const s = [...E.ember], t0 = performance.now(); return new Promise(res => { const st = () => { const k = Math.min(1, (performance.now() - t0) / ms), e = ease(k);
  E.ember = [s[0] + (x - s[0]) * e, s[1] + (y - s[1]) * e - Math.sin(k * Math.PI) * 14]; if (Math.random() < .9) E.trail.push({ x: E.ember[0] + (Math.random() - .5) * 3, y: E.ember[1] + 8 + Math.random() * 3, t: performance.now() });
  if (k < 1) requestAnimationFrame(st); else res(); }; st(); }); }
async function walk(tx, ty){ World.walkToTile(tx, ty); await sleep(250); for (let i = 0; i < 80; i++){ const p = World.myPos(), m = World.meAt(); await sleep(100); const q = World.meAt(); if (Math.abs(q.x - m.x) < .1 && Math.abs(q.y - m.y) < .1) break; } }
const meNear = d => { const m = World.meAt(); return Math.hypot(m.x - E.ember[0], m.y + 18 - E.ember[1]) < d; };
function say(name, text, choices, pick){ return new Promise(async res => {
  dlg.style.display = 'flex'; const nm = dlg.querySelector('.evname'); nm.textContent = name; nm.style.display = name ? '' : 'none'; const tx = dlg.querySelector('.evtext'), ch = dlg.querySelector('.evch'), tap = dlg.querySelector('.evtap');
  tx.style.color = '#F1E9FF'; ch.innerHTML = ''; tap.style.display = 'none'; tx.textContent = '';
  for (let i = 1; i <= text.length; i++){ tx.textContent = text.slice(0, i); await sleep(45); }
  if (choices){ await sleep(350); ch.innerHTML = choices.map(c => `<button class="encch">${c}</button>`).join(''); await sleep(1500); ch.children[pick].classList.add('on'); await sleep(700); }
  else { tap.style.display = ''; await sleep(1600); }
  res(); }); }
function draw(now){
  requestAnimationFrame(draw);
  const r = cv.getBoundingClientRect(); if (!r.width || !World.__cam) return;
  for (const c of [ov, top]){ if (c.width !== cv.width || c.height !== cv.height){ c.width = cv.width; c.height = cv.height; } Object.assign(c.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' }); }
  const [cx, cy, K] = World.__cam, S = (x, y) => [(x - cx) * K, (y - cy) * K], s = r.width / cv.width;
  g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, ov.width, ov.height); g2.setTransform(1, 0, 0, 1, 0, 0); g2.clearRect(0, 0, top.width, top.height); g.imageSmoothingEnabled = g2.imageSmoothingEnabled = false;
  // 제단: 이끼 낀 돌 받침 + 얕은 그릇 + 룬 두 개
  if (E.altar){ const [ax, ay] = S(E.altar[0], E.altar[1]), u = K;
    const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(Math.round(ax + x * u), Math.round(ay + y * u), Math.ceil(w * u), Math.ceil(h * u)); };
    R(-13, -3, 26, 6, 'rgba(0,0,0,.35)'); R(-10, -14, 20, 13, '#4A4658'); R(-10, -14, 20, 2, '#6A6680'); R(-10, -3, 20, 2, '#2E2A3A'); R(-12, -18, 24, 5, '#5C5872'); R(-12, -18, 24, 1, '#8A86A2'); R(-12, -14, 24, 1, '#34304A');
    R(-20, -26, 6, 24, '#4A4658'); R(-20, -26, 6, 2, '#6A6680'); R(-20, -4, 6, 2, '#2E2A3A'); R(-19, -20, 1, 6, '#8AC4FF55'); R(14, -22, 5, 20, '#4A4658'); R(14, -22, 5, 2, '#6A6680'); R(14, -4, 5, 2, '#2E2A3A'); R(15, -16, 1, 5, '#8AC4FF55');
    R(-7, -21, 14, 3, '#3A364C'); R(-6, -22, 12, 1, '#6A6680'); R(-10, -8, 4, 2, '#3E6A3A'); R(5, -12, 5, 2, '#3E6A3A'); R(-12, -16, 3, 2, '#4E7A44');
    const rg = .4 + .6 * Math.abs(Math.sin(now / 700)) * (E.glow ? 1 : .35); g.globalAlpha = rg; R(-6, -11, 1, 4, '#8AC4FF'); R(-7, -10, 3, 1, '#8AC4FF'); R(5, -11, 1, 4, '#8AC4FF'); R(4, -9, 3, 1, '#8AC4FF'); g.globalAlpha = 1; }
  // 불티 자국 (몇 초 동안 땅 위에 남아 반짝)
  E.trail = E.trail.filter(p => now - p.t < 7000);
  g.globalCompositeOperation = 'lighter';
  for (const p of E.trail){ const a = 1 - (now - p.t) / 7000, [px, py] = S(p.x, p.y); g.globalAlpha = a * (.6 + .4 * Math.sin(now / 150 + p.x)); g.fillStyle = '#FFE8B0'; g.fillRect(Math.round(px), Math.round(py), Math.max(1, Math.round(K)), Math.max(1, Math.round(K))); }
  g.globalAlpha = 1;
  if (E.follow && E.ember){ const m = World.meAt(); E.fhist = E.fhist || []; E.fhist.push([now, m.x, m.y + 6]); while (E.fhist.length > 2 && E.fhist[1][0] < now - 600) E.fhist.shift();
    const o = E.fhist[0], mv = Math.hypot(m.x - o[1], m.y + 6 - o[2]) > 3, ia = now / 1400, tx = mv ? o[1] + Math.sign(o[1] - m.x || 1) * 6 : m.x + 11 * Math.cos(ia), ty = mv ? o[2] - 6 : m.y - 2 + 2 * Math.sin(ia * 2);
    E.ember[0] += (tx - E.ember[0]) * .06; E.ember[1] += (ty - E.ember[1]) * .06; }
  if (E.ember){ const [ex, ey] = S(E.ember[0], E.ember[1] + Math.sin(now / 380) * 1.5), col = E.spirit >= 0 ? '#5A8CFF' : '#FFE8B0', rad = (E.sz + 12) * K * (.85 + .15 * Math.sin(now / 260));
    const ctx = E.ritual ? g2 : g; ctx.globalCompositeOperation = 'lighter';
    let rg = ctx.createRadialGradient(ex, ey, 0, ex, ey, rad); rg.addColorStop(0, (E.hue !== null ? `hsla(${E.hue},90%,65%,.55)` : col + '88')); rg.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(ex, ey, rad, 0, 7); ctx.fill();
    if (E.burst){ const k = (now - E.burst) / 900; if (k < 1){ ctx.strokeStyle = `rgba(200,225,255,${1 - k})`; ctx.lineWidth = 3 * K * (1 - k); ctx.beginPath(); ctx.arc(ex, ey, (8 + k * 70) * K, 0, 7); ctx.stroke(); ctx.fillStyle = `rgba(255,255,255,${.35 * (1 - k)})`; ctx.fillRect(0, 0, top.width, top.height); } }
    ctx.globalCompositeOperation = 'source-over';
    if (SPR.complete){ const fi = Math.floor(now / 110) % 8, sz = E.sz * K * 1.9, row = E.spirit >= 0 ? E.spirit : 0;
      ctx.filter = E.spirit >= 0 ? 'none' : E.hue !== null ? `hue-rotate(${E.hue - 220}deg) saturate(1.6) brightness(1.15)` : 'saturate(0) brightness(1.7) sepia(.5)';
      ctx.drawImage(SPR, fi * 64, row * 64, 64, 64, Math.round(ex - sz / 2), Math.round(ey - sz * .62), Math.round(sz), Math.round(sz)); ctx.filter = 'none'; }
    if (E.ritual) for (let i = 0; i < 2; i++) E.sparks.push({ x: E.ember[0] + (Math.random() - .5) * 30, y: E.ember[1] + 14, vy: -.02 - Math.random() * .04, t: now, life: 900 + Math.random() * 700, h: E.hue });
    E.sparks = E.sparks.filter(p => now - p.t < p.life); g2.globalCompositeOperation = 'lighter';
    for (const p of E.sparks){ const dt = now - p.t, [px, py] = S(p.x, p.y + p.vy * dt); g2.globalAlpha = 1 - dt / p.life; g2.fillStyle = p.h !== null && E.spirit < 0 ? `hsl(${p.h},90%,70%)` : '#A8D0FF'; g2.fillRect(Math.round(px), Math.round(py), Math.round(K), Math.round(K)); }
    g2.globalAlpha = 1; g2.globalCompositeOperation = 'source-over';
    E.floats = (E.floats || []).filter(f => now - f.t < 1600);
    for (const f of E.floats){ const k = (now - f.t) / 1600; g2.globalAlpha = 1 - k; g2.font = `bold ${Math.round(9 * K)}px G11B, sans-serif`; g2.textAlign = 'center'; g2.fillStyle = '#8AC4FF'; g2.fillText(f.txt, ex, ey - (14 + k * 16) * K); g2.globalAlpha = 1; }
    E.scr = [r.left + ex * s, r.top + ey * s];
    if (E.ritual){ dark.style.background = `radial-gradient(circle at ${r.left + ex * s}px ${r.top + ey * s}px, rgba(4,2,10,0) 0, rgba(4,2,10,.55) 90px, rgba(4,2,10,.94) 260px)`; nameEl.style.top = (r.top + ey * s - 150) + 'px'; }
  }
}
requestAnimationFrame(draw);
window.__encGo = async (o) => {
  const T = (x, y) => World.__P(x + .5, y + .5), me0 = World.meAt();
  // 1) 맵: 하얀 불씨가 다가와요 (말 없이, 내 머리 위에 「.......!」)
  E.ember = [me0.x - 150, me0.y - 120]; await sleep(1500);
  await flyTo(me0.x + 26, me0.y + 4, 2600); await sleep(500);
  World.say('me', '.......!'); await sleep(1800);
  // 2) 불씨가 멀어지고, 따라가요
  const p2 = T(39, 53); await flyTo(p2[0], p2[1] - 14, 1800);
  await walk(40, 51); const p3 = T(36, 57); await flyTo(p3[0], p3[1] - 14, 1600); await walk(38, 56); await sleep(300);
  // 3) 어딘가로: 화면이 어두워지고 덩굴에 감긴 제단 (연출 컷)
  fade.style.opacity = 1; await sleep(1100); E.ember = null;
  C.av = World.Avatar.compose(o.av || World.__myAv); C.on = 1; C.ember = [130, 40]; scene.style.display = 'block'; scene.style.opacity = 1; fade.style.opacity = 0; await sleep(1200);
  await new Promise(res => { const t0 = performance.now(), s0 = [...C.ember]; const st = () => { const k = Math.min(1, (performance.now() - t0) / 2200), e = ease(k); C.ember = [s0[0] + (160 - s0[0]) * e, s0[1] + (78 - s0[1]) * e - Math.sin(k * Math.PI) * 10]; if (k < 1) requestAnimationFrame(st); else res(); }; st(); });
  C.glow = 1; await sleep(900);
  for (const q of ENC_Q) await say('잊힌 제단', q[0], q[1], Math.floor(Math.random() * 3));
  dlg.style.display = 'none';
  // 4) 계약 의식
  C.ritual = 1; { const t0 = performance.now(); await new Promise(res => { const st = () => { const k = Math.min(1, (performance.now() - t0) / 4200); C.dark = Math.min(1, k * 3); C.sz = 10 + 14 * ease(k); C.hue = (k < .8 ? (k / .8) * 720 : 720 + (k - .8) / .2 * 220) % 360; if (k < 1) requestAnimationFrame(st); else res(); }; st(); }); }
  await sleep(400); C.burst = performance.now(); C.spirit = 0; C.hue = null; C.sz = 18; C.ritual = 0; await sleep(900);
  nameEl.style.top = '9%'; nameEl.style.setProperty('--c', '#5A8CFF'); nameEl.innerHTML = 'Vael'.split('').map(c => `<span class="enclt">${c}</span>`).join('');
  for (const sp of nameEl.children){ await sleep(380); sp.classList.add('on'); }
  await sleep(1400);
  await say('Vael', o.first); dlg.style.display = 'none';
  // 5) 맵으로 돌아오면 정령이 곁에
  fade.style.opacity = 1; await sleep(1100); scene.style.display = 'none'; C.on = 0; nameEl.innerHTML = '';
  const m2 = World.meAt(); E.ember = [m2.x + 12, m2.y - 2]; E.sz = 9; E.spirit = 0; E.follow = 1; E.burst = performance.now();
  fade.style.opacity = 0; await sleep(1600);
  await walk(42, 52); await sleep(1500);
  window.__encDone = true;
};
})();
