// 시안: 씨앗 대회 처음 연출 — 관리자가 이벤트를 열면 학생 화면에서 한 번
//   ① 광장에 무슈 블랑이 스르륵 → ② 씨앗 열두 개가 빙글빙글 → 한 개가 나를 골라 날아옴 → ③ 씨앗이 첫마디(성격대로)
//   → ④ 블랑이 키우는 법 안내 → ⑤ 내 방으로 이동, 화분이 놓여 있음 → ⑥ 화분 카드(물 0/2 · 말 0/2 · 6시간 간격 · 1/5일째)
//   목업 사이트 폴더에 blanc_lpc.png · seed_plants.png가 있어야 해요 · window.__soGo(plant 번호)
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const PL = [['잭오랜턴 호박꽃', '#FF8A2A'], ['박쥐 날개 고사리', '#8A5AC8'], ['유령 난초', '#E8F0FF'], ['해골 양귀비', '#F0E8D8'], ['거미줄 백합', '#C8C4E0'], ['마녀 모자 버섯', '#7A4AB8'],
  ['눈알 열매덩굴', '#E8486A'], ['사탕옥수수 튤립', '#FFD84A'], ['도깨비불 등불초', '#6AE8FF'], ['검은 장미', '#5A2A4A'], ['독사과 나무', '#7AE05A'], ['뱀파이어 송곳니 끈끈이', '#C81E3A']];
const FIRST = {   // 씨앗이 나를 고를 때 첫마디 (seed_plant_lines.json 말투 그대로)
  0: ['야아아아! 너다! 너로 정했어! 내가 골랐어! 최고의 선택이야!', '빨리 가자! 방 어디야?! 나 달려갈게! 다리는 없지만!'],
  1: ['어.... 여기가 어디야? 아, 너한테 떨어졌구나. 일부러 그런 거야. 아마.', '나 씨앗 맞지? 아까 블랑 아저씨가 그렇다고 했어. 그럼 맞아.'],
  4: ['어머, 하필 너야? ....뭐, 다른 애들은 더 별로였으니까.', '열심히 키워 봐. 기대는 안 할게. 실망하기 싫거든.'],
  6: ['....드디어 만났네. 사실 아까부터 계속 보고 있었어.', '....네 방 가는 길 알아. 침대 밑에 뭐 있는지도 알아.']
};
const css = document.createElement('style'); css.textContent = `
#sosay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:320;display:none}
#sosay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid var(--bc,#9AC8F0);border-radius:14px;padding:12px}
#sosay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden}#sosay .fc canvas{width:60px;height:60px;image-rendering:pixelated}
#sosay b{display:block;font-family:var(--f-pxb);font-size:14px;color:var(--bc,#BFE0FF);margin-bottom:3px}#sosay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px}
#sofx{position:fixed;inset:0;z-index:305;pointer-events:none}
#sodim{position:fixed;inset:0;z-index:300;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(160,200,255,0) 0,rgba(10,14,30,.6) 70%);opacity:0;transition:opacity 1.2s}
#socard{position:fixed;left:50%;top:40%;z-index:340;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 22px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #9AE07A;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(154,224,122,.45);pointer-events:none;text-align:center;width:min(86vw,330px)}
#socard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#socard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}#socard canvas{image-rendering:pixelated}
#socard .rw{display:flex;gap:8px;width:100%}#socard .rw i{flex:1;font-style:normal;padding:7px 4px;border-radius:10px;background:#2A2040;font-size:13px}#socard .rw i em{display:block;font-style:normal;font-family:var(--f-px);font-size:11px;color:#C8B8F0;margin-top:2px}
#sotitle{position:fixed;left:0;right:0;top:24%;z-index:338;text-align:center;font-family:var(--f-pxb);color:#FFE9A0;font-size:24px;letter-spacing:2px;text-shadow:0 0 14px #FF9A3A,0 2px 0 #2A1440;opacity:0;transition:opacity .8s;pointer-events:none}
#sotitle small{display:block;font-family:var(--f-px);font-size:13px;color:#E8DCFF;letter-spacing:0;margin-top:6px;text-shadow:none}#sotitle.on{opacity:1}`;
document.head.appendChild(css);
const el = (id, html, tag = 'div') => { const d = document.createElement(tag); d.id = id; if (html) d.innerHTML = html; document.body.appendChild(d); return d; };
const say = el('sosay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div></div>');
const dim = el('sodim'), card = el('socard'), title = el('sotitle');
const fx = el('sofx', '', 'canvas'); const fg = fx.getContext('2d');
const SH = new Image(); SH.src = 'blanc_lpc.png'; const PI = new Image(); PI.src = 'seed_plants.png';
const blancFrame = (i, a = 1) => { const c = document.createElement('canvas'); c.width = c.height = 32; const g = c.getContext('2d'); g.globalAlpha = a; g.imageSmoothingQuality = 'high'; g.drawImage(SH, i * 64, 0, 64, 64, 0, 0, 32, 32); return c; };
let MAP = 'campus', SPOT = [18, 57], bob = null;
const placeBlanc = (i, a) => { const img = blancFrame(i, a); World.setProps(MAP, [{ id: 'blanc', x: SPOT[0], y: SPOT[1], img, pxc: img.getContext('2d'), sw: 32, sh: 32, ax: 16, ay: 30, solid: true }], 'blanc'); };
const seedFace = (g, col) => { g.clearRect(0, 0, 32, 32); g.fillStyle = '#1E2A20'; g.fillRect(0, 0, 32, 32); g.imageSmoothingEnabled = false; g.drawImage(PI, 0, 14, 40, 40, -4, -2, 40, 40); g.fillStyle = col; g.globalAlpha = .25; g.fillRect(0, 0, 32, 32); g.globalAlpha = 1; };
const talk = async (who, t, hold = 1500, col) => {
  const g = say.querySelector('canvas').getContext('2d'); say.style.setProperty('--bc', col || '#9AC8F0'); say.querySelector('b').textContent = who;
  if (col){ seedFace(g, col); } else { g.imageSmoothingEnabled = false; g.clearRect(0, 0, 32, 32); g.drawImage(SH, 16, 6, 32, 32, 0, 0, 32, 32); }
  say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(34); } await sleep(hold); say.style.display = 'none'; await sleep(150);
};
const center = () => { const c = document.querySelector('canvas#world, #game canvas, canvas') ; const r = c ? c.getBoundingClientRect() : { left: 0, top: 0, width: innerWidth, height: innerHeight }; return [r.left + r.width / 2, r.top + r.height / 2]; };
// 씨앗 열두 개: 블랑 앞에서 원을 그리며 돌다가, 하나가 나에게 날아와요
const seedDot = (x, y, col, s = 1, a = 1) => {
  fg.globalAlpha = a * .35; fg.fillStyle = col; fg.beginPath(); fg.arc(x, y, 9 * s, 0, 7); fg.fill();
  fg.globalAlpha = a; fg.fillStyle = '#3A2414'; fg.beginPath(); fg.ellipse(x, y, 3.2 * s, 4.4 * s, .4, 0, 7); fg.fill();
  fg.fillStyle = col; fg.beginPath(); fg.ellipse(x - .8 * s, y - 1 * s, 1.6 * s, 2.2 * s, .4, 0, 7); fg.fill(); fg.globalAlpha = 1;
};
async function swirl(mine){
  fx.width = innerWidth * 2; fx.height = innerHeight * 2; fx.style.width = innerWidth + 'px'; fx.style.height = innerHeight + 'px'; fg.setTransform(2, 0, 0, 2, 0, 0);
  const [cx, cy0] = center(), cy = cy0 - 50, t0 = performance.now(); let done = false;
  await new Promise(res => { const step = now => {
    const t = (now - t0) / 1000; fg.clearRect(0, 0, innerWidth, innerHeight);
    const R = Math.min(70, 20 + t * 40), sp = 1.2 + t * .5;
    PL.forEach(([, col], i) => {
      let a = t * sp + i * Math.PI * 2 / 12, x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R * .55 - Math.sin(t * 3 + i) * 4;
      if (i === mine && t > 3.2){ const k = Math.min(1, (t - 3.2) / .9), e = k * k * (3 - 2 * k); x = x + (cx - x) * e; y = y + (cy0 + 2 - y) * e - Math.sin(e * Math.PI) * 40; seedDot(x, y, col, 1 + e * .6); }
      else seedDot(x, y, col, 1, t > 3.6 ? Math.max(0, 1 - (t - 3.6) / .6) : Math.min(1, t * 2));
    });
    if (t > 4.15){ fg.globalAlpha = Math.max(0, 1 - (t - 4.15) / .6); fg.fillStyle = PL[mine][1]; fg.beginPath(); fg.arc(cx, cy0 + 2, 10 + (t - 4.15) * 60, 0, 7); fg.fill(); fg.globalAlpha = 1; }
    if (t < 4.8) requestAnimationFrame(step); else { fg.clearRect(0, 0, innerWidth, innerHeight); res(); }
  }; requestAnimationFrame(step); });
}
const potProp = (k, col, glow = 1) => { const c = document.createElement('canvas'); c.width = 48; c.height = 48; const g = c.getContext('2d');
  const rg = g.createRadialGradient(24, 36, 2, 24, 36, 22); rg.addColorStop(0, col + 'CC'); rg.addColorStop(1, col + '00'); g.globalAlpha = .55 * glow; g.fillStyle = rg; g.fillRect(0, 0, 48, 48); g.globalAlpha = 1;
  g.imageSmoothingQuality = 'high'; g.drawImage(PI, 4, 24, 32, 32, 12, 18, 24, 24);
  for (let i = 0; i < 4; i++){ const a = glow * 6 + i * 1.6; g.fillStyle = '#FFF6C8'; g.globalAlpha = .5 + .5 * Math.sin(a * 2); g.fillRect(24 + Math.round(Math.cos(a) * 14), 22 + Math.round(Math.sin(a) * 8), 1, 1); } g.globalAlpha = 1; return c; };
window.__soGo = async (mine = 4) => {
  const [nm, col] = PL[mine], [L1, L2] = FIRST[mine] || FIRST[4];
  await sleep(1200);
  dim.style.opacity = 1; await sleep(600);
  for (let k = 1; k <= 10; k++){ placeBlanc(0, k / 10); await sleep(110); }
  let t = 0; bob = setInterval(() => placeBlanc(1 + (t++ % 4), 1), 260);
  World.say('me', '.......!'); await sleep(1300);
  await talk('무슈 블랑', '봉수아르, 젊은 마녀님. 놀라지 마시게. 오늘 밤은 부탁이 있어 왔다네.');
  await talk('무슈 블랑', '백 년 만에 할로윈 만찬을 차리고 싶은데.... 이 세상에 없는 열매가 필요하지.');
  await talk('무슈 블랑', '여기 열두 개의 씨앗이 있네. 성미가 아주 고약한 녀석들이라.... 주인은 씨앗이 직접 고른다네.', 1700);
  title.innerHTML = '마법 씨앗 대회<small>씨앗이 주인을 고르는 중.......</small>'; title.classList.add('on');
  await swirl(mine); title.classList.remove('on');
  World.say('me', '?!'); await sleep(900);
  card.innerHTML = `<canvas width="32" height="32" id="sopot" style="width:112px;height:112px"></canvas>${nm} 씨앗<small>이 씨앗이 나를 골랐어요</small>`;
  card.classList.add('on'); { const g = document.getElementById('sopot').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(PI, 4, 24, 32, 32, 0, 0, 32, 32); } await sleep(2200); card.classList.remove('on'); await sleep(450);
  await talk(nm, L1, 1600, col);
  await talk(nm, L2, 1600, col);
  await talk('무슈 블랑', '흠, 벌써 마음이 맞는 것 같군. 씨앗은 그대 방 화분에 심어 두겠네.');
  await talk('무슈 블랑', '물은 하루 두 번, 말도 하루 두 번이라네. 한 번 하고 나면 여섯 시간은 쉬게 해 주게.', 1800);
  await talk('무슈 블랑', '닷새 동안 하루도 빠짐없이 돌보면 꽃이 피고, 열매가 열리지. 그 열매로 만든 요리.... 기다리겠네.', 1800);
  clearInterval(bob); for (let k = 10; k >= 0; k--){ placeBlanc(0, k / 10); await sleep(100); } World.setProps(MAP, [], 'blanc'); dim.style.opacity = 0;
  await sleep(500);
  // 내 방으로: 창가에 화분
  World.teleport('myroom_witch', [8, 9]); await sleep(1800);
  let pk = 0; const putPot = () => { const pot = potProp(0, col, .6 + .4 * Math.sin(pk++ / 3)); World.setProps('myroom_witch', [{ id: 'pot', x: 10, y: 7, img: pot, pxc: pot.getContext('2d'), sw: 48, sh: 48, ax: 24, ay: 42, solid: true }], 'seedpot'); };
  for (let k = 0; k < 8; k++){ putPot(); await sleep(60); } const potT = setInterval(putPot, 120);
  World.walkToTile(9, 8); await sleep(1400);
  await sleep(900); World.say('me', '화분이다.'); await sleep(1400);
  await talk(nm, mine === 4 ? '어머, 방이 생각보다 좁네. 뭐, 너한테 딱 맞는 크기다.' : mine === 0 ? '여기가 우리 집이야?! 좋아! 완전 좋아! 창문도 있어!' : mine === 1 ? '여기 어디야? 아, 화분이구나. 흙 맛있다.' : '....좋은 방이네. 잘 보여. 전부 다.', 1600, col);
  card.innerHTML = `<canvas width="32" height="32" id="sopot2" style="width:80px;height:80px"></canvas>${nm}<small>씨앗 · 1 / 5일째</small><div class="rw"><i>💧 물 0 / 2<em>6시간 간격</em></i><i>💬 말 0 / 2<em>6시간 간격</em></i></div><small>둘 다 채우면 자정에 자라요</small>`;
  card.classList.add('on'); { const g = document.getElementById('sopot2').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(PI, 4, 24, 32, 32, 0, 0, 32, 32); } await sleep(3600); card.classList.remove('on');
  await sleep(1000); clearInterval(potT); window.__soDone = true;
};
})();
