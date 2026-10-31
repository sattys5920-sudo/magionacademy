// 시안: 무슈 블랑 (식당 요리장 유령) 첫 만남 · 할로윈 요리 건네기 · 맛보기 · 별점·한 줄 평 · 꾸미기 보상 — 실제 게임 위에서 연출만
//   목업 사이트 폴더에 blanc_lpc.png · seed_dishes.png · hw_tags.png가 있어야 해요 · window.__blGo()
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const SPOT = [14, 11];   // 과자 교실 가운데 (조리대 사이)
const css = document.createElement('style'); css.textContent = `
#blsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:320;display:none}
#blsay .bx{position:relative;max-width:560px;margin:0 auto;display:flex;gap:10px;background:rgba(20,13,34,.96);border:2px solid #9AC8F0;border-radius:14px;padding:12px}
#blsay .fc{width:60px;height:60px;flex:none;border-radius:10px;background:#1E2A44;overflow:hidden;image-rendering:pixelated}
#blsay .fc canvas{width:60px;height:60px;image-rendering:pixelated}
#blsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:#BFE0FF;margin-bottom:3px}#blsay p{margin:0;font-family:var(--f-px);font-size:15px;line-height:22px;color:#F1E9FF;min-height:44px}
#blpick{position:fixed;inset:0;z-index:330;background:rgba(8,6,16,.6);display:none;align-items:flex-end;justify-content:center;padding:0 10px calc(84px + env(safe-area-inset-bottom))}
#blpick .p{width:min(100%,560px);background:#1E1530;border:2px solid #9AC8F0;border-radius:16px;padding:12px;font-family:var(--f-px);color:#F1E9FF}
#blpick .h{font-family:var(--f-pxb);font-size:15px;color:#BFE0FF;margin-bottom:8px;display:flex;justify-content:space-between}#blpick .h span{font-family:var(--f-px);font-size:12px;color:#C8B8F0}
#blpick .g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}#blpick button{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 4px;border-radius:12px;border:2px solid #4E3C72;background:#2A2040;color:#F1E9FF;font-family:var(--f-pxb);font-size:12px;min-height:44px}
#blpick button canvas{width:48px;height:48px;image-rendering:pixelated}#blpick button small{font-family:var(--f-px);font-size:11px;color:#C8B8F0}#blpick button.on{border-color:#BFE0FF;box-shadow:0 0 12px #9AC8F0}
#blcard{position:fixed;left:50%;top:38%;z-index:340;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 22px;border-radius:16px;background:rgba(20,13,34,.97);border:2px solid #FFE8A0;font-family:var(--f-pxb);color:#F1E9FF;box-shadow:0 0 22px rgba(255,232,160,.5);pointer-events:none;text-align:center;max-width:86vw}
#blcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#blcard .st{font-size:26px;letter-spacing:4px;color:#FFD866;text-shadow:0 0 10px #FFB020}#blcard small{font-family:var(--f-px);font-size:13px;color:#E0D4F4;line-height:19px}
#blcard canvas{image-rendering:pixelated}#blfade{position:fixed;inset:0;z-index:300;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(160,200,255,0) 0,rgba(10,14,30,.55) 70%);opacity:0;transition:opacity 1.2s}`;
document.head.appendChild(css);
const say = document.createElement('div'); say.id = 'blsay'; say.innerHTML = '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b>무슈 블랑</b><p></p></div></div>'; document.body.appendChild(say);
const pick = document.createElement('div'); pick.id = 'blpick'; document.body.appendChild(pick);
const card = document.createElement('div'); card.id = 'blcard'; document.body.appendChild(card);
const dim = document.createElement('div'); dim.id = 'blfade'; document.body.appendChild(dim);
const SH = new Image(); SH.src = 'blanc_lpc.png'; const DI = new Image(); DI.src = 'seed_dishes.png'; const TG = new Image(); TG.src = 'hw_tags.png';
const frameCanvas = (i, a = 1) => { const c = document.createElement('canvas'); c.width = c.height = 32; const g = c.getContext('2d'); g.globalAlpha = a; g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high'; g.drawImage(SH, i * 64, 0, 64, 64, 0, 0, 32, 32); return c; };   // 캐릭터처럼 세계에선 반 크기
let bob = null;
const place = (i, a) => { const img = frameCanvas(i, a); World.setProps('candy', [{ id: 'blanc', x: SPOT[0], y: SPOT[1], img, pxc: img.getContext('2d'), sw: 32, sh: 32, ax: 16, ay: 30, solid: true }], 'blanc'); };
const face = () => { const g = say.querySelector('canvas').getContext('2d'); g.imageSmoothingEnabled = false; g.clearRect(0, 0, 32, 32); g.drawImage(SH, 16, 6, 32, 32, 0, 0, 32, 32); };
const talk = async (t, hold = 1500) => { face(); say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(36); } await sleep(hold); say.style.display = 'none'; await sleep(160); };
const showCard = async (html, ms) => { card.innerHTML = html; card.classList.add('on'); await sleep(ms); card.classList.remove('on'); await sleep(450); };
const DISH = ['잭오랜턴 파이', '검은 장미 사탕', '피빛 장미 타르트', '눈알 젤리', '유령 눈알 푸딩', '유령 솜사탕', '거미줄 해골 쿠키', '해골 박쥐 수프', '박쥐 모자 머핀', '도깨비불 마녀 차', '도깨비불 사과 사이다', '독사과 호박 수프', '마녀의 대솥 스튜', '유령 파티 푸딩', '뱀파이어 만찬 젤리', '잭의 사탕 사과', '열두 밤 만찬'];
window.__blGo = async () => {
  await sleep(1500);
  dim.style.opacity = 1; await sleep(700);
  for (let k = 1; k <= 10; k++){ place(0, k / 10); await sleep(120); }   // 스르륵 나타나요
  let t = 0; bob = setInterval(() => place(1 + (t++ % 4), 1), 260);
  World.say('me', '.......!'); await sleep(1600);
  await talk('....흠? 이 늦은 시간에, 산 사람이 내 주방에 들어오다니.');
  await talk('놀라지 마시게. 나는 블랑. 백 년 전 이 학교 식당의 요리장이었지.');
  await talk('죽은 뒤로는 무엇을 먹어도 맛이 느껴지지 않았다네.... 그런데 오늘, 할로윈 열매 냄새가 코끝에 닿더군.');
  await talk('그 열매로 요리를 만들어 오게. 맛을 볼 수만 있다면.... 이 블랑, 섭섭지 않게 보답하겠네.', 1800);
  // 요리 건네기
  pick.innerHTML = `<div class="p"><div class="h">무슈 블랑에게 요리 건네기<span>오늘 1번</span></div><div class="g">${[0, 5, 12].map(i => `<button data-bd="${i}"><canvas width="32" height="32" data-di="${i}"></canvas>${DISH[i]}<small>${i === 12 ? '특별 요리' : '일반 요리'} ×1</small></button>`).join('')}</div></div>`;
  pick.querySelectorAll('canvas[data-di]').forEach(c => { const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(DI, +c.dataset.di * 32, 0, 32, 32, 0, 0, 32, 32); });
  pick.style.display = 'flex';
  const di = await new Promise(res => pick.querySelectorAll('[data-bd]').forEach(b => b.onclick = () => { b.classList.add('on'); setTimeout(() => res(+b.dataset.bd), 450); }));
  pick.style.display = 'none';
  await showCard(`<canvas width="32" height="32" id="bldish" style="width:96px;height:96px"></canvas>${DISH[di]}<small>무슈 블랑에게 건넸어요</small>`, 10); 
  card.classList.add('on'); { const g = document.getElementById('bldish').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(DI, di * 32, 0, 32, 32, 0, 0, 32, 32); } await sleep(1800); card.classList.remove('on'); await sleep(400);
  await talk('(킁킁).... 이 향은.......', 1300);
  await talk('음.... 음!! ....잠깐, 조용히 해 보게.', 1500);
  clearInterval(bob); for (let k = 0; k < 6; k++){ place(k % 2 ? 0 : 2, 1); await sleep(140); } bob = setInterval(() => place(1 + (t++ % 4), 1), 200);   // 들썩들썩
  await talk('바삭한 껍질에 달콤한 호박, 그리고 사탕옥수수의 고소함.... 백 년 만에 혀가 깨어났구먼!', 1800);
  await showCard(`<div class="st">★★★</div>무슈 블랑의 한 줄 평<small>「백 년을 기다린 보람이 있는 파이로군. 내일도 오게, 꼬마 요리사.」</small>`, 2800);
  await showCard(`<canvas width="48" height="25" id="bltag" style="width:192px;height:100px"></canvas>「호박 이름표」<small>꾸미기 보상 · 프로필에서 끼울 수 있어요<br>무슈 블랑이 맛본 요리 1 / 17</small>`, 10);
  card.classList.add('on'); { const g = document.getElementById('bltag').getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(TG, 0, 0, 48, 25, 0, 0, 48, 25); } await sleep(2800); card.classList.remove('on'); await sleep(500);
  await talk('다음엔 다른 요리를 가져와 보게. 열두 가지 열매를 다 쓴 만찬이라면.... 흠, 꿈같은 이야기군.', 1800);
  clearInterval(bob); for (let k = 10; k >= 0; k--){ place(0, k / 10); await sleep(110); } World.setProps('candy', [], 'blanc'); dim.style.opacity = 0;
  await sleep(1200); window.__blDone = true;
};
})();
