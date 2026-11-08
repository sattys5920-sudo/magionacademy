// 「양호실 겨울 감기」 연출 미리 보기 (모의 서버 전용 · 게임 코드 아님). rec.js 가 모의 index.html 모듈 안에 끼워 넣어요.
window.__coldPv = (() => {
  const IMG = {}; ['breath', 'thermo', 'chart', 'cabinet', 'blanket', 'bandage', 'bubble_fever', 'bubble_throat', 'bubble_nose', 'bubble_chill', 'potion_fever', 'potion_throat', 'potion_nose', 'potion_chill'].forEach(k => { const i = new Image(); i.src = 'art/cold/' + k + '.png'; IMG[k] = i; });
  const POT = { fever: ['열 내림 물약', '촉촉 이끼 · 고사리 · 달맞이꽃'], throat: ['꿀 목 물약', '벌꿀 · 산딸기 · 은방울꽃'], nose: ['콧물 뚝 물약', '블루베리 · 개박하 · 들꽃'], chill: ['따끈 찜질 물약', '호박씨 · 서리 낙엽 · 해바라기씨'] };
  const SYM = { fever: '열', throat: '목감기', nose: '콧물', chill: '오한' };
  const sick = {};   // npc id → [증상 ...]
  const prev = World.onNpcDrawn;
  World.onNpcDrawn = (cx, id, x0, y0, cp, view, p) => {
    if (prev) prev(cx, id, x0, y0, cp, view, p);
    const L = sick[id]; if (!L || !L.length) return; const q = Math.max(1, Math.round(cp * 1.4)), t = performance.now() / 1000, mid = x0 + 32 * cp;
    cx.save(); cx.imageSmoothingEnabled = false;
    const n = L.length, gap = 17 * q, bob = Math.round(Math.sin(t * 2.4) * q);
    L.forEach((k, i) => { const bx = Math.round(mid - (n * gap) / 2 + i * gap + q), by = Math.round(y0 - 7 * cp - 16 * q + bob - (n > 1 ? Math.abs(i - (n - 1) / 2) * -2 * q : 0)); cx.drawImage(IMG['bubble_' + k], bx, by, 16 * q, 15 * q); });
    if (n === 1) cx.drawImage(IMG.thermo, Math.round(mid + 10 * q), Math.round(y0 - 7 * cp - 13 * q + bob), 7 * q, 14 * q);
    const ph = (t * .7 + id.length * .3) % 1; cx.globalAlpha = ph < .7 ? Math.sin(ph / .7 * Math.PI) : 0;
    const side = view >= 15 ? -1 : 1; cx.drawImage(IMG.breath, Math.round(mid + side * 6 * cp - (side < 0 ? 14 * q : 0) + side * ph * 4 * q), Math.round(y0 + 20 * cp - ph * 3 * q), 14 * q, 9 * q);
    cx.restore();
  };
  const P = () => window.__people || [];
  const npcP = id => P().find(q => q.npc && q.npc.id === id && !q.npc.cut);
  const css = document.createElement('style'); css.textContent = `
    #hibv .cw{display:flex;flex-direction:column;gap:8px}
    #hibv .pt{display:flex;align-items:center;gap:10px;background:var(--panel2);border-radius:12px;padding:8px 10px;font:14px var(--f-pxb);color:var(--text)}
    #hibv .pt img{width:40px;height:40px;image-rendering:pixelated}#hibv .pt small{display:block;font:12px var(--f-px,inherit);color:var(--sub)}
    #hibv .pt .ok{margin-left:auto;color:#9ADC7A}#hibv .pt .no{margin-left:auto;color:var(--sub)}
    #hibv .g4{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
    #hibv .g4 button{min-height:64px;border:0;border-radius:12px;background:var(--panel2);color:var(--text);font:14px var(--f-pxb);display:flex;align-items:center;gap:8px;padding:6px 10px}
    #hibv .g4 button img{width:32px;height:30px;image-rendering:pixelated}#hibv .g4 button.on{box-shadow:inset 0 0 0 2px #E8A040}
    #hibv h4{margin:2px 0 0;font:13px var(--f-pxb);color:#FFE2B0}
    #hibv .face{display:flex;justify-content:center;background:#1E2A36;border-radius:12px;padding:6px}#hibv .face canvas{width:128px;height:128px;image-rendering:pixelated}
    .pvtap{position:fixed;z-index:9999;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;border:3px solid rgba(255,255,255,.9);pointer-events:none;animation:pvtap .5s ease-out forwards}
    @keyframes pvtap{from{transform:scale(.4);opacity:1}to{transform:scale(1.3);opacity:0}}`;
  document.head.appendChild(css);
  const tapFx = el => { if (!el) return; const r = el.getBoundingClientRect(), d = document.createElement('div'); d.className = 'pvtap'; d.style.left = (r.left + r.width / 2) + 'px'; d.style.top = (r.top + r.height / 2) + 'px'; document.body.appendChild(d); setTimeout(() => d.remove(), 600); };
  const tap = async (sel, ms = 700) => { const el = typeof sel === 'string' ? document.querySelector(sel) : sel; tapFx(el); await famSleep(250); el && el.click(); await famSleep(ms); };
  const win = (title, body) => { let v = $('#hibv'); if (!v){ v = document.createElement('div'); v.id = 'hibv'; document.body.appendChild(v); requestAnimationFrame(() => v.classList.add('on')); } v.innerHTML = `<div class="hd"><b>${title}</b><button data-cpx="close" aria-label="닫기">✕</button></div><div class="cw">${body}</div>`; return v; };
  const closeW = async () => { const v = $('#hibv'); if (v){ tapFx(v.querySelector('[data-cpx]')); await famSleep(250); v.classList.remove('on'); await famSleep(320); v.remove(); } };
  const card = (img, t, s, w = 64, ms = 2400) => famCard(`<img src="art/cold/${img}.png" style="width:${w}px;image-rendering:pixelated"><b>${t}</b><small>${s}</small>`, null, ms);
  const textCard = (t, s, ms = 2200) => famCard(`<b>${t}</b><small>${s}</small>`, null, ms);
  const chartHTML = (pts) => `<h4>오늘 맡은 환자</h4>${pts.map(([n, k, done]) => `<div class="pt"><img src="art/cold/bubble_${k}.png"><div>${n}<small>${done ? '다 나았어요' : '아파요'}</small></div>${done ? '<span class="ok">고침</span>' : '<span class="no">1 일째</span>'}</div>`).join('')}
    <h4>증상 · 물약</h4>${Object.keys(POT).map(k => `<div class="pt"><img src="art/cold/bubble_${k}.png" style="width:32px;height:30px"><img src="art/cold/potion_${k}.png" style="width:32px;height:32px"><div>${POT[k][0]}<small>${POT[k][1]}</small></div></div>`).join('')}`;

  // ---------- 1. 시작 연출 ----------
  async function intro(){
    closeSheet(); npcClose(); const n = npcGet('sera'), t = World.meTile();
    const far = (World.freeNear(t.x, t.y, 6) || []).map(([x, y]) => [x, y, Math.abs(x - t.x) + Math.abs(y - t.y)]).filter(q => q[2] >= 4).sort((p, q) => q[2] - p[2])[0] || [t.x + 4, t.y];
    const near = (World.freeNear(t.x, t.y, 1) || []).filter(([x, y]) => x !== t.x || y !== t.y).sort((p, q) => (Math.abs(p[0] - far[0]) + Math.abs(p[1] - far[1])) - (Math.abs(q[0] - far[0]) + Math.abs(q[1] - far[1])))[0] || [t.x + 1, t.y];
    const say = (text, ms) => ({ cmd: 'say', who: 'sera', text, ms: ms || Math.max(2600, text.length * 105) });
    toast('바람이 차가워졌어요.......'); await famSleep(1600);
    await World.cut([{ cmd: 'spawn', who: 'sera', name: n.name, av: npcAv(n), x: far[0], y: far[1], dir: 'down' },
      { cmd: 'walk', who: 'sera', x: near[0], y: near[1], run: true, timeout: 6 }, { cmd: 'face', who: 'sera', to: 'player' }, { cmd: 'face', who: 'player', to: 'sera' },
      { cmd: 'emote', who: 'sera', icon: 4 }, say('어머, 마침 잘 왔구나. 선생님 좀 도와줄 수 있겠니?'), say('어제부터 마을에 감기가 돌고 있어. 레오는 콜록콜록, 마들렌은 훌쩍훌쩍.... 캇파는 접시 물이 펄펄 끓는단다.', 4200),
      say('아파 보이는 친구를 잘 살펴보고, 맞는 물약을 갖다주렴. 맛은.... 보장 못 하지만.', 3600), say('선생님? 선생님은 괜찮아. 양호 선생님이 감기 걸리면 큰일이잖니.', 3000), say('....에취.', 1800), { cmd: 'emote', who: 'sera', icon: 5 }, { cmd: 'wait', sec: 1 }]);
    sfx('sparkle'); await card('chart', '진료 수첩', '감기 물약 레시피와 증상 표가 적혀 있어요', 72, 2600); toast('「진료 수첩」을 받았어요'); await famSleep(900);
    win('진료 수첩', chartHTML([['레오', 'throat', 0], ['캇파', 'fever', 0], ['나비', 'nose', 0]])); await famSleep(3200);
    const v = $('#hibv'); if (v) v.scrollTo({ top: 400, behavior: 'smooth' }); await famSleep(3000); await closeW(); await famSleep(800);
  }

  // ---------- 2. 진료 · 보상 ----------
  async function treat(){
    sick.leo = ['throat']; sick.kappa = ['fever']; sick.nabi = ['nose'];
    const p = npcP('leo'); if (!p) return 'no leo'; const lx = Math.round(p.x), ly = Math.round(p.y);
    World.teleport(World.where(), [lx + 2, ly + 1]); await famSleep(2600);
    World.sayNpc('leo', '....콜록. 생물들한텐 옮기면 안 되는데.', 3000); await famSleep(3200);
    const face = n => `<div class="face"><canvas id="cpface" width="64" height="64"></canvas></div>`;
    const drawFace = () => { const c = $('#cpface'); if (!c) return; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; const S = World.Avatar && World.Avatar.compose && World.Avatar.compose(npcAv(npcGet('leo'))); if (S) g.drawImage(S, 0, 0, 64, 64, 0, 0, 64, 64); g.drawImage(IMG.bubble_throat, 24, 0, 16, 15); };
    let v = win('레오 · 진료하기', `${face()}<h4>어디가 아파 보여요</h4><div class="g4">${Object.keys(SYM).map(k => `<button data-cps="${k}"><img src="art/cold/bubble_${k}.png">${SYM[k]}</button>`).join('')}</div>`); drawFace(); await famSleep(2200);
    await tap('[data-cps="throat"]', 300); $('[data-cps="throat"]').classList.add('on'); await famSleep(700);
    // 잘못된 물약
    v = win('레오 · 목감기', `<h4>건넬 물약을 골라요</h4><div class="g4">${Object.keys(POT).map(k => `<button data-cpp="${k}"><img src="art/cold/potion_${k}.png" style="width:32px;height:32px">${POT[k][0]}</button>`).join('')}</div>`); await famSleep(1500);
    await tap('[data-cpp="chill"]', 300); await closeW(); World.sayNpc('leo', '....조금 나아진 것 같기도 하고.......', 3000); await famSleep(1400); toast('따끈 찜질 물약이 없어졌어요. 다시 끓여 와야 해요'); await famSleep(3000);
    // 맞는 물약
    v = win('레오 · 목감기', `<h4>건넬 물약을 골라요</h4><div class="g4">${Object.keys(POT).map(k => `<button data-cpp="${k}"><img src="art/cold/potion_${k}.png" style="width:32px;height:32px">${POT[k][0]}</button>`).join('')}</div>`); await famSleep(1400);
    await tap('[data-cpp="throat"]', 300); await closeW();
    sfx('sparkle'); sick.leo = []; World.sayNpc('leo', '목이 시원해. ....쓰긴 쓰다. 그래도 고마워.', 3200); await famSleep(1800); toast('레오가 나았어요 · 하트 +20'); await famSleep(2600);
    sfx('win'); await textCard('이름표 「꼬마 간호사」', '처음으로 환자를 고쳤어요', 2600); await famSleep(600);
    await textCard('서로 다른 5 명을 고치면', '', 1600);
    await card('cabinet', '가구 「작은 약장」', '감기 물약 네 병이 들어 있어요', 66, 2600); await famSleep(400);
    await textCard('서로 다른 10 명을 고치면', '', 1600);
    await card('bandage', '말풍선 「반창고 말풍선」', '내 말풍선을 바꿀 수 있어요', 78, 2600); await famSleep(800);
    win('진료 수첩', chartHTML([['레오', 'throat', 1], ['캇파', 'fever', 0], ['나비', 'nose', 0]])); await famSleep(3000); await closeW(); await famSleep(600);
  }

  // ---------- 3. 끝 연출 ----------
  async function ending(){
    const p = npcP('sera'); if (!p) return 'no sera'; p.path = []; const sx = Math.round(p.x), sy = Math.round(p.y);
    World.teleport(World.where(), [sx + 2, sy]); await famSleep(2600);
    const say = (text, ms) => ({ cmd: 'say', who: 'sera', text, ms: ms || Math.max(2600, text.length * 105) });
    await World.cut([{ cmd: 'face', who: 'sera', to: 'player' }, { cmd: 'face', who: 'player', to: 'sera' }, say('다들 나았구나. 이제 마을에 감기는....', 3000), { cmd: 'emote', who: 'sera', icon: 4 }, { cmd: 'wait', sec: .6 }]);
    sick.sera = ['fever', 'throat', 'nose', 'chill']; sfx('pop'); World.sayNpc('sera', '어머.... 바닥이 빙글빙글 도는구나.......', 3000); await famSleep(3400);
    World.sayNpc('sera', '에취. ....콜록. 이번엔 선생님 차례인가 봐.......', 3000); await famSleep(3600);
    for (const k of ['fever', 'throat', 'nose', 'chill']){
      win('세라 선생님 · 물약 건네기', `<div class="g4">${Object.keys(POT).map(q => `<button data-cpp="${q}" ${sick.sera.includes(q) ? '' : 'style="opacity:.35"'}><img src="art/cold/potion_${q}.png" style="width:32px;height:32px">${POT[q][0]}</button>`).join('')}</div>`); await famSleep(900);
      await tap(`[data-cpp="${k}"]`, 200); await closeW(); sfx('sparkle'); sick.sera = sick.sera.filter(q => q !== k); toast(POT[k][0] + '을 건넸어요'); await famSleep(1500);
    }
    await World.cut([{ cmd: 'emote', who: 'sera', icon: 6 }, say('....이렇게 쓴 걸 선생님이 매일 먹였구나. 미안해.......', 3600), say('그래도 잘 듣네. 선생님 레시피가 맞았다는 증거야. 고마워, 꼬마 간호사님.', 3400), { cmd: 'emote', who: 'sera', icon: 7 }, { cmd: 'wait', sec: 1 }]);
    sfx('win'); await textCard('세라 선생님 하트 +60', '', 2000);
    await card('blanket', '가구 「양호실 담요」', '세라 선생님이 덮던 담요예요', 84, 2600);
    await textCard('3 일 동안 물약 회복량 +10 %', '세라 선생님의 처방이에요', 2400); await famSleep(800);
    World.sayNpc('sera', '후후, 이번 물약은.... 조금 덜 써. 정말이란다.', 3000); await famSleep(3600);
  }
  return { intro, treat, ending, sick };
})();
