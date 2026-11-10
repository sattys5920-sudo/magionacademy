// 시안: 「반이 같이 품는 거대 알」 (게임 코드 아님 · 모의 서버 화면에 넣어서 찍어요)
//   window.__egg = { load, place(단계 0~4, 기운 'fire'|'wind'|'star'|''), intro(), care(상태), hatch(종류 0~3), vote(), admin() }
(() => {
  const KIND = [{ k: 'fire', n: '아기 불새', c: '#FF8A3A' }, { k: 'wind', n: '아기 구름 고래', c: '#9FD8FF' }, { k: 'star', n: '아기 별 여우', c: '#B9A0FF' }, { k: 'rainbow', n: '아기 무지개 용', c: '#FFB0E0' }];
  const AURA = { fire: ['#FF8A3A', '따뜻하게', '불 기운'], wind: ['#9FD8FF', '노래', '바람 기운'], star: ['#C9A9FF', '이야기', '별 기운'] };
  let EGG = null, BABY = null; const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = s; });
  async function load(){ EGG = await img('/__egg/egg_stages.png?' + Date.now()); BABY = await img('/__egg/egg_babies.png?' + Date.now()); }
  const sleep = ms => new Promise(r => setTimeout(r, ms)), ease = q => q < .5 ? 2 * q * q : 1 - (-2 * q + 2) ** 2 / 2;
  const rgb = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)).join(',');
  function eggCv(stage, aura, sc = 2, t = 0){   // 알 + 아래 빛무리 (기운 색)
    const W = 32 * sc + 24, Hh = 40 * sc + 18, c = document.createElement('canvas'); c.width = W; c.height = Hh; const g = c.getContext('2d'); g.imageSmoothingEnabled = false;
    if (aura){ const col = AURA[aura][0], gr = g.createRadialGradient(W / 2, Hh - 12, 2, W / 2, Hh - 12, W / 2); gr.addColorStop(0, `rgba(${rgb(col)},.55)`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, Hh); }
    g.fillStyle = 'rgba(0,0,0,.28)'; g.beginPath(); g.ellipse(W / 2, Hh - 9, 13 * sc, 3 * sc, 0, 0, 7); g.fill();
    g.fillStyle = '#C8B48A'; g.beginPath(); g.ellipse(W / 2, Hh - 11, 15 * sc, 4 * sc, 0, 0, 7); g.fill(); g.fillStyle = '#E8D8B0'; g.beginPath(); g.ellipse(W / 2, Hh - 12, 13 * sc, 3 * sc, 0, 0, 7); g.fill();   // 짚 둥지
    const wob = stage >= 3 ? Math.sin(t / 90) * 1.5 : 0; g.save(); g.translate(W / 2, Hh - 12); g.rotate(wob * .03); g.drawImage(EGG, stage * 32, 0, 32, 40, -16 * sc, -40 * sc + 4, 32 * sc, 40 * sc); g.restore();
    return c;
  }
  // ---------- 맵에 놓기 (학교 안뜰) ----------
  let spot = null;
  function place(stage = 0, aura = ''){
    if (!spot){ const c = [40, 42]; for (let r = 0; r < 8 && !spot; r++) for (let dx = -r; dx <= r && !spot; dx++) for (let dy = -r; dy <= r && !spot; dy++){ const x = c[0] + dx, y = c[1] + dy; if (World.isFree(x, y) && World.isFree(x + 1, y)) spot = [x, y]; } }
    const cv = eggCv(stage, aura, 1); World.setProps('campus', [{ id: 'egg', x: spot[0], y: spot[1], img: cv, pxc: cv.getContext('2d'), sw: cv.width, sh: cv.height, ax: cv.width / 2, ay: cv.height - 8, solid: 1 }], 'egg');
    return spot;
  }
  // ---------- 창 공통 ----------
  const CSS = `<style>#eggv{position:fixed;inset:0;z-index:300;background:rgba(10,6,24,.72);display:flex;align-items:flex-end;justify-content:center;font-family:var(--f-pxb);color:#F1E9FF}
    #eggv .card{width:100%;max-width:520px;background:#1c1530;border:2px solid #4E3C72;border-radius:18px 18px 0 0;padding:14px 14px calc(16px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:10px}
    #eggv .hd{display:flex;align-items:center;gap:8px}#eggv .hd b{flex:1;font-size:18px}#eggv .x{width:40px;height:40px;border-radius:12px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-size:18px}
    #eggv .stage{display:flex;align-items:center;gap:12px;background:#120c22;border-radius:14px;padding:10px}#eggv .stage canvas{image-rendering:pixelated;flex:none}
    #eggv .bars{flex:1;display:flex;flex-direction:column;gap:6px;font-size:13px}#eggv .bar{display:flex;align-items:center;gap:6px}#eggv .bar span{width:58px}#eggv .bar i{flex:1;height:10px;border-radius:5px;background:#2E2248;overflow:hidden;position:relative}#eggv .bar i em{position:absolute;inset:0;width:var(--w);background:var(--c);border-radius:5px}#eggv .bar b{width:28px;text-align:right;font-size:12px}
    #eggv .acts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}#eggv .act{min-height:64px;border-radius:14px;border:2px solid var(--c);background:rgba(255,255,255,.04);color:#F1E9FF;font-family:var(--f-pxb);font-size:15px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px}#eggv .act small{font-size:11px;color:var(--c)}#eggv .act.on{background:var(--c);color:#1c1530}#eggv .act.on small{color:#1c1530}#eggv .act:disabled{opacity:.4}
    #eggv .sub{font-size:12px;color:#c8bce0}#eggv textarea,#eggv input{width:100%;min-height:44px;border-radius:12px;border:1px solid #4E3C72;background:#120c22;color:#F1E9FF;font-family:var(--f-pxb);font-size:15px;padding:10px;box-sizing:border-box}
    #eggv .go{min-height:48px;border-radius:14px;border:1px solid #C86A1E;background:#FF9A3C;color:#2A1506;font-family:var(--f-pxb);font-size:16px}#eggv .go:disabled{opacity:.45}
    #eggv .vl{display:flex;flex-direction:column;gap:6px}#eggv .vr{display:flex;align-items:center;gap:8px;min-height:48px;padding:0 10px;border-radius:12px;background:#120c22;border:1px solid #2E2248}#eggv .vr.on{border-color:#FF9A3C}#eggv .vr b{flex:1;font-size:16px}#eggv .vr small{font-size:12px;color:#c8bce0}#eggv .vr button{min-width:64px;min-height:36px;border-radius:10px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-family:var(--f-pxb)}#eggv .vr.on button{background:#FF9A3C;color:#2A1506;border-color:#C86A1E}
    #eggv.adm{align-items:center;background:#F4F0FA;color:#22183F;font-family:Pretendard,sans-serif}#eggv.adm .card{background:#fff;border:1px solid #E2D8EE;border-radius:12px;color:#22183F;max-width:760px}#eggv.adm .sub{color:#7A6A8A}#eggv.adm table{border-collapse:collapse;width:100%;font-size:13px}#eggv.adm td,#eggv.adm th{border-bottom:1px solid #EEE6F4;padding:5px 4px;text-align:left}#eggv.adm .btns{display:flex;gap:6px;flex-wrap:wrap}#eggv.adm .btns button{min-height:36px;padding:0 12px;border-radius:10px;border:1px solid #D8CCE8;background:#fff;font-weight:700}#eggv.adm .btns .p{background:#FF9A3C;border-color:#C86A1E}#eggv.adm .chips{display:flex;gap:6px;flex-wrap:wrap}#eggv.adm .chips span{background:#F4F0FA;border-radius:8px;padding:2px 8px;font-size:12px}</style>`;
  const close = () => { const v = document.getElementById('eggv'); if (v) v.remove(); };
  const open = (html, cls = '') => { close(); const v = document.createElement('div'); v.id = 'eggv'; v.className = cls; v.innerHTML = CSS + html; document.body.appendChild(v); return v; };
  const bars = S => { const tot = Math.max(1, S.fire + S.wind + S.star); return `<div class="bars">${['fire', 'wind', 'star'].map(k => `<div class="bar" style="--c:${AURA[k][0]}"><span>${AURA[k][2]}</span><i><em style="--w:${Math.round(S[k] / tot * 100)}%"></em></i><b>${S[k]}</b></div>`).join('')}<div class="sub">금 ${S.stage} / 4 · 오늘 돌본 친구 ${S.today} / 12</div></div>`; };
  // ---------- 돌봐 주기 창 ----------
  function care(S = { day: 3, stage: 1, fire: 14, wind: 9, star: 11, today: 5, done: '' }){
    const lead = ['fire', 'wind', 'star'].sort((a, b) => S[b] - S[a])[0];
    const v = open(`<div class="card"><div class="hd"><b>안뜰의 거대 알 · ${S.day} 일째</b><button class="x" data-x>✕</button></div>
      <div class="stage"><span data-egg></span>${bars(S)}</div>
      <div class="acts">${['fire', 'wind', 'star'].map(k => `<button class="act${S.done === k ? ' on' : ''}" data-a="${k}" style="--c:${AURA[k][0]}" ${S.done && S.done !== k ? 'disabled' : ''}>${AURA[k][1]}<small>${AURA[k][2]}</small></button>`).join('')}</div>
      <div class="sub" data-msg>${S.done ? '오늘은 돌봐 줬어요. 내일 또 와 주세요' : '하루에 한 번 돌봐 줄 수 있어요'}</div><div data-story></div></div>`);
    v.querySelector('[data-egg]').replaceWith(eggCv(S.stage, lead, 2));
    v.querySelector('[data-x]').onclick = close;
    v.querySelectorAll('[data-a]').forEach(b => b.onclick = () => { if (b.dataset.a === 'star'){ v.querySelector('[data-story]').innerHTML = `<textarea maxlength="30" placeholder="오늘 있었던 일을 한 줄 들려줘요 (알만 들어요)"></textarea><button class="go" style="width:100%;margin-top:6px">들려주기</button>`; return; } b.classList.add('on'); v.querySelectorAll('[data-a]').forEach(x => { if (x !== b) x.disabled = true; }); v.querySelector('[data-msg]').textContent = b.dataset.a === 'fire' ? '알을 꼭 끌어안았어요. 따뜻해졌어요' : '알에게 노래를 불러 줬어요. 알이 살짝 흔들렸어요'; });
    return v;
  }
  // ---------- 이름 투표 ----------
  function vote(kind = 1){
    const K = KIND[kind], C = [['몽실이', 5], ['구름빵', 3], ['하늘이', 2], ['뭉게', 1]];
    const v = open(`<div class="card"><div class="hd"><b>${K.n}의 이름 짓기</b><button class="x" data-x>✕</button></div>
      <div class="stage"><span data-b></span><div class="bars"><div class="sub">후보를 하나 내거나, 마음에 드는 이름에 한 표를 줘요. 한 사람 한 표예요</div><div class="sub">투표 마감: 부화 다음 날 밤 9 시</div></div></div>
      <div class="vl">${C.map(([n, c], i) => `<div class="vr${i === 1 ? ' on' : ''}"><b>${n}</b><small>${c} 표</small><button>${i === 1 ? '골랐어요' : '한 표'}</button></div>`).join('')}</div>
      <input maxlength="6" placeholder="새 이름 후보 내기 (6 자까지)"><button class="go">후보 내기</button></div>`);
    const c = document.createElement('canvas'); c.width = 72; c.height = 72; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BABY, 0, kind * 32, 32, 32, 4, 4, 64, 64); c.style.imageRendering = 'pixelated'; v.querySelector('[data-b]').replaceWith(c);
    v.querySelector('[data-x]').onclick = close; return v;
  }
  // ---------- 관리자 카드 ----------
  function admin(){
    const R = [['니콜라스', 3, 1, 1, '6 / 7'], ['닝닝', 1, 4, 2, '7 / 7'], ['모카', 2, 2, 3, '7 / 7'], ['사나', 0, 5, 1, '6 / 7'], ['샤넬', 4, 0, 2, '6 / 7'], ['안나', 1, 1, 4, '6 / 7']];
    return open(`<div class="card"><div class="hd"><b>이벤트 「반이 같이 품는 거대 알」</b></div>
      <div class="chips"><span>4 일째 · 금 2 / 4</span><span>불 기운 31</span><span>바람 기운 27</span><span>별 기운 24</span><span>오늘 돌본 학생 8 / 12</span><span>이대로면: 아기 불새</span></div>
      <div class="btns"><button>이벤트 끝내기</button><button class="p">지금 부화</button><button>이름 투표 마감</button></div>
      <div class="sub">7 일째 밤에 알아서 부화해요. 「지금 부화」를 누르면 바로 깨어나요. 이야기 내용은 학생끼리 볼 수 없고 여기서만 보여요.</div>
      <table><tr><th>학생</th><th>따뜻하게</th><th>노래</th><th>이야기</th><th>돌본 날</th></tr>${R.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`).join('')}</table>
      <div class="sub">이름 후보: 불꽃이 5 표 · 호떡이 3 표 · 반짝이 2 표</div></div>`, 'adm');
  }
  // ---------- 연출 (320×180 캔버스 · 사역마 연출과 같은 틀) ----------
  function cutBase(){
    const v = document.createElement('div'); v.id = 'famcut'; v.innerHTML = `<canvas width="320" height="180"></canvas><div class="fname"></div><div class="fline"></div><div class="ffade"></div>`;
    document.body.appendChild(v); const cv = v.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
    const fl = v.querySelector('.fline'), nm = v.querySelector('.fname'), fade = v.querySelector('.ffade');
    const say = async (t, hold = 1600) => { fl.style.opacity = 1; fl.innerHTML = [...t].map(c => `<span>${c === ' ' ? ' ' : c}</span>`).join(''); for (const s of fl.children){ await sleep(s.textContent === '.' ? 130 : 75); s.classList.add('on'); } await sleep(hold); fl.style.opacity = 0; await sleep(600); };
    return { v, cv, g, fl, nm, fade, say };
  }
  function yard(g, t, night){   // 학교 안뜰 (밤 · 아침)
    const sk = g.createLinearGradient(0, 0, 0, 120); if (night){ sk.addColorStop(0, '#0b0820'); sk.addColorStop(1, '#2a2350'); } else { sk.addColorStop(0, '#7ab8f0'); sk.addColorStop(1, '#ffe0c0'); } g.fillStyle = sk; g.fillRect(0, 0, 320, 120);
    if (night) for (let i = 0; i < 40; i++){ g.globalAlpha = .4 + .4 * Math.sin(t / 500 + i); g.fillStyle = '#fff'; g.fillRect((i * 73) % 320, (i * 37) % 70, 1, 1); } g.globalAlpha = 1;
    g.fillStyle = night ? '#2a2440' : '#9a8a7a'; g.fillRect(40, 40, 240, 80); g.fillStyle = night ? '#3a3450' : '#b8a898'; for (let x = 52; x < 270; x += 30){ g.fillRect(x, 54, 14, 20); g.fillStyle = night ? '#ffd86a' : '#6a8ab0'; g.fillRect(x + 2, 56, 10, 16); g.fillStyle = night ? '#3a3450' : '#b8a898'; }   // 학교 건물 · 창
    g.fillStyle = night ? '#1e3a2e' : '#5aa04a'; g.fillRect(0, 118, 320, 62); g.fillStyle = night ? '#2a4a38' : '#78c060'; for (let x = 0; x < 320; x += 6) g.fillRect(x, 118 + (x % 12 ? 0 : 2), 3, 2);
    g.fillStyle = night ? '#3a3a4a' : '#c8b898'; g.beginPath(); g.ellipse(160, 150, 70, 14, 0, 0, 7); g.fill();   // 돌 마당
  }
  async function intro(){
    await load(); const { v, g, say, fade } = cutBase(); let live = true, ph = 0, t0 = performance.now(), star = null, egg = 0, morning = 0;
    const draw = now => { if (!live) return; requestAnimationFrame(draw); const t = now - t0; yard(g, t, !morning); if (morning < 1 && morning > 0){ g.fillStyle = `rgba(255,240,220,${morning})`; g.fillRect(0, 0, 320, 180); }
      if (star){ const q = Math.min(1, (now - star) / 1400), x = 300 - 140 * q, y = 10 + 132 * q; for (let k = 0; k < 14; k++){ g.globalAlpha = (1 - k / 14) * (1 - Math.max(0, q - .95) * 20); g.fillStyle = k < 3 ? '#fff' : '#ffe07a'; g.fillRect(x + k * 4, y - k * 3.8, 3, 3); } g.globalAlpha = 1;
        if (q >= 1){ const e = Math.min(1, (now - star - 1400) / 700); if (e < 1){ g.strokeStyle = `rgba(255,240,180,${1 - e})`; g.lineWidth = 3; g.beginPath(); g.ellipse(160, 146, 10 + e * 80, 3 + e * 20, 0, 0, 7); g.stroke(); g.fillStyle = `rgba(255,255,255,${.6 * (1 - e)})`; g.fillRect(0, 0, 320, 180); } } }
      if (egg){ const c = eggCv(0, '', 1.6, now); g.drawImage(c, 160 - c.width / 2, 152 - c.height); } };
    requestAnimationFrame(draw); fade.style.opacity = 1; requestAnimationFrame(() => v.classList.add('on')); await sleep(700); fade.style.opacity = 0; await sleep(800);
    await say('....한밤중, 학교 위로 별 하나가 길게 꼬리를 그었어요.', 600); star = performance.now(); await sleep(1500); egg = 1; await sleep(1200);
    fade.style.opacity = 1; await sleep(900); morning = 1; star = null; fade.style.opacity = 0; await sleep(900);
    await say('다음 날 아침, 안뜰 한가운데에 커다란 알이 놓여 있었어요.', 900); await say('따뜻하게 품어 주면.... 무언가가 깨어날 것 같아요.', 1400);
    fade.style.opacity = 1; await sleep(800); live = false; v.remove();
  }
  async function hatch(kind = 1){
    await load(); const K = KIND[kind]; const { v, g, say, fade, nm } = cutBase(); let live = true, t0 = performance.now(), st = 3, shake = 0, burst = 0, baby = 0, jump = 0;
    const kids = []; for (let i = 0; i < 6; i++){ const av = World.Avatar.fromLook(7 + i * 13); await World.Avatar.need(av); kids.push(av); }
    const draw = now => { if (!live) return; requestAnimationFrame(draw); const t = now - t0; yard(g, t, false);
      kids.forEach((av, i) => { const A = World.Avatar, sp = A.compose(av); if (!sp) return; const x = [70, 100, 220, 250, 120, 200][i], y = [150, 166, 150, 166, 172, 172][i], d = x < 160 ? A.meta.dirs.right : A.meta.dirs.left; g.drawImage(sp, d * A.FW, 0, A.FW, A.FH, x - A.FW / 2, y - A.FH + 4 - (jump ? Math.abs(Math.sin(now / 150 + i)) * 4 : 0), A.FW, A.FH); });
      if (!baby){ const c = eggCv(st, kind < 3 ? ['fire', 'wind', 'star'][kind] : 'star', 1.6, now * (shake ? 3 : 1)); g.save(); g.translate(shake ? Math.sin(now / 30) * shake : 0, 0); g.drawImage(c, 160 - c.width / 2, 152 - c.height); g.restore(); }
      if (burst){ const q = (now - burst) / 1200; if (q < 1){ g.fillStyle = `rgba(255,255,255,${.7 * (1 - q) ** 2})`; g.fillRect(0, 0, 320, 180); for (let i = 0; i < 18; i++){ const a = i / 18 * 7, r = q * 70; g.fillStyle = i % 3 ? K.c : '#fff'; g.globalAlpha = 1 - q; g.fillRect(160 + Math.cos(a) * r, 120 + Math.sin(a) * r * .7, 3, 3); } g.globalAlpha = 1;
        for (let i = 0; i < 6; i++){ const a = -.4 - i * .5, r = q * 40; g.fillStyle = '#F2E6CC'; g.fillRect(160 + Math.cos(a) * r * (i % 2 ? 1 : -1), 130 + Math.sin(a) * r + q * q * 50, 5, 4); } } }
      if (baby){ const b = Math.abs(Math.sin(now / 260)) * 6, fr = Math.floor(now / 300) % 2; g.fillStyle = 'rgba(0,0,0,.25)'; g.beginPath(); g.ellipse(160, 150, 16, 4, 0, 0, 7); g.fill(); g.drawImage(BABY, fr * 32, kind * 32, 32, 32, 160 - 32, 150 - 64 - b, 64, 64);
        for (let i = 0; i < 8; i++){ const a = now / 700 + i * .785; g.fillStyle = i % 2 ? K.c : '#fff'; g.fillRect(160 + Math.cos(a) * 44, 112 + Math.sin(a) * 14, 2, 2); } } };
    requestAnimationFrame(draw); fade.style.opacity = 1; requestAnimationFrame(() => v.classList.add('on')); await sleep(700); fade.style.opacity = 0; await sleep(800);
    await say('일곱째 날. 알이 아까부터 쉬지 않고 들썩여요.', 500); shake = 1.5; await sleep(1200); st = 4; shake = 3; await sleep(1400);
    burst = performance.now(); baby = 1; await sleep(900); jump = 1;
    nm.style.cssText = `color:${K.c};opacity:1;font-size:30px;letter-spacing:4px`; nm.innerHTML = [...K.n].map(c => `<span>${c === ' ' ? ' ' : c}</span>`).join(''); for (const s of nm.children){ await sleep(160); s.classList.add('on'); }
    await sleep(900); nm.style.opacity = .35; await say(kind === 3 ? '세 가지 기운이 고루 모여서.... 아주 드문 아이가 태어났어요.' : `${AURA[['fire', 'wind', 'star'][kind]][2]}이 가장 많이 모였어요.`, 900);
    await say('이 아이에게 이름을 지어 줘요. 반 친구들 투표로 정해요.', 1400); fade.style.opacity = 1; await sleep(800); live = false; v.remove();
  }
  window.__egg = { load, place, care, vote, admin, intro, hatch, close, KIND };
})();
