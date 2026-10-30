// 시안: 「마법 씨앗 대회」 (5일) · 1일째 맨디에게 씨앗 → 하루 한 번 돌보기(물·햇빛·노래·달빛) → 5일째 꽃 피움 → 광장 전시·투표
//   씨앗은 12종 중 하나가 학생마다 겹치지 않게 정해져 있어요(꽃이 필 때까지 비밀, 꽃봉오리 색이 힌트) · 돌보기는 반짝임(등급)을 정해요
//   실제 게임 위에서 연출만 · 하루하루는 빨리 감아서 보여 줘요 · window.__sdGo()
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms));
const iga = w => { const c = w.charCodeAt(w.length - 1) - 0xAC00; return c >= 0 && c % 28 ? '이' : '가'; };
const CARE = [['water', '물 주기', '#5AB8F0'], ['sun', '햇빛 쬐기', '#FFC838'], ['song', '노래 불러 주기', '#B070F0'], ['moon', '달빛 비추기', '#D8E0FF']];
const MOOD = { water: '....목말라.', sun: '....추워. 따뜻했으면.', song: '....심심해.', moon: '....눈부셔. 조용한 빛이 좋아.' };
const FINAL = ['물방울 백합', '햇살 왕관꽃', '노래하는 종꽃', '달빛 장미', '무지개 꽃', '불꽃 튤립', '별사탕 열매나무', '유령 난초', '호박 덩굴꽃', '박쥐 날개 고사리', '구름 솜꽃', '수정 선인장'], MINE = 3;   // 그림 칸: 0 씨앗 · 1 새싹 · 2 잎 · 3+i 꽃봉오리 · 15+i 최종 꽃
const css = document.createElement('style'); css.textContent = `
#sdsay{position:fixed;left:10px;right:10px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:320;display:none}#sdsay .evbox{position:relative;max-width:560px;margin:0 auto;background:rgba(20,13,34,.96);border:2px solid #6ACA5A;border-radius:14px;padding:14px 14px 12px}
#sdsay .evtext{font-size:15px;line-height:22px;min-height:44px;color:#F1E9FF;font-family:var(--f-px)}#sdsay .fqn{position:absolute;left:10px;top:-14px;background:#6ACA5A;color:#102010;border-radius:8px;padding:2px 10px;font-family:var(--f-pxb);font-size:var(--fs-s)}
#sdv{position:fixed;inset:0;z-index:310;background:rgba(10,6,20,.82);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .5s}#sdv.on{opacity:1}
#sdv .p{width:min(94vw,420px);background:#1E1530;border:2px solid #6ACA5A;border-radius:16px;overflow:hidden;font-family:var(--f-px);color:#F1E9FF}
#sdv .hd{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;font-family:var(--f-pxb);font-size:15px;color:#C8F0B0}#sdv .hd span{font-family:var(--f-px);font-size:12px;color:#C8B8F0}
#sdv canvas{display:block;width:100%;image-rendering:pixelated}
#sdv .st{display:flex;gap:6px;padding:8px 14px 0;font-size:12px;color:#C8B8F0}#sdv .st i{font-style:normal;padding:2px 8px;border-radius:999px;background:#2E2248}
#sdv .bt{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px 14px 14px}#sdv .bt button{min-height:44px;border-radius:12px;border:2px solid var(--c);background:#241A3C;color:#F1E9FF;font-family:var(--f-pxb);font-size:14px}#sdv .bt button.on{background:#3A2C5A;box-shadow:0 0 12px var(--c)}
#sdv .msg{padding:0 14px 14px;font-size:13px;color:#FFE8A0;min-height:18px}
#sdday{position:fixed;inset:0;z-index:330;display:flex;align-items:center;justify-content:center;background:#05030A;color:#FFF1C1;font-family:var(--f-pxb);font-size:28px;letter-spacing:4px;opacity:0;pointer-events:none;transition:opacity .5s}
#sdcard{position:fixed;left:50%;top:40%;z-index:325;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .5s;display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 20px;border-radius:16px;background:rgba(20,13,34,.96);border:2px solid #FFE8A0;font-family:var(--f-pxb);font-size:16px;color:#F1E9FF;box-shadow:0 0 22px rgba(255,232,160,.5);pointer-events:none}#sdcard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#sdcard small{font-family:var(--f-px);font-size:12px;color:#C8B8F0}`;
document.head.appendChild(css);
const say = document.createElement('div'); say.id = 'sdsay'; say.innerHTML = '<div class="evbox"><div class="fqn">맨디</div><div class="evtext"></div></div>'; document.body.appendChild(say);
const dayEl = document.createElement('div'); dayEl.id = 'sdday'; document.body.appendChild(dayEl);
const card = document.createElement('div'); card.id = 'sdcard'; document.body.appendChild(card);
const talk = async (t, hold = 1400) => { say.style.display = 'block'; const tx = say.querySelector('.evtext'); tx.textContent = ''; for (let k = 1; k <= t.length; k++){ tx.textContent = t.slice(0, k); await sleep(36); } await sleep(hold); say.style.display = 'none'; await sleep(150); };
const SP = new Image(); SP.src = 'seed_plants.png'; const BG = new Image(); BG.src = 'seed_bg.png';
const showCard = async (html, ms = 2200) => { card.innerHTML = html; paintIcons(); card.classList.add('on'); await sleep(ms); card.classList.remove('on'); await sleep(400); };
const plantIcon = (i, w = 72) => `<canvas width="40" height="56" data-sp="${i}" style="width:${w}px;height:${w * 1.4}px;image-rendering:pixelated"></canvas>`;
function paintIcons(){ return paintIcons0(); }
const paintIcons0 = () => document.querySelectorAll('canvas[data-sp]').forEach(c => { const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(SP, +c.dataset.sp * 40, 0, 40, 56, 0, 0, 40, 56); });
window.__sdGo = async () => {
  await sleep(1200);
  await talk('학생! 오늘 아주 신기한 씨앗이 들어왔어요.'); await talk('닷새 동안 정성껏 돌보면, 무슨 꽃이 필지는 아무도 몰라요.'); await talk('하루에 한 번만 돌볼 수 있어요. 씨앗 기분을 잘 살펴봐요!', 1500);
  await showCard(`${plantIcon(0)}수수께끼 씨앗<small>맨디에게 받았어요</small>`, 2000); paintIcons();
  // 돌보기 창
  const v = document.createElement('div'); v.id = 'sdv'; v.innerHTML = `<div class="p"><div class="hd"><b>마법 씨앗</b><span></span></div><canvas width="320" height="180"></canvas><div class="st"></div><div class="msg"></div><div class="bt">${CARE.map(([k, n, c]) => `<button data-sc="${k}" style="--c:${c}">${n}</button>`).join('')}</div></div>`; document.body.appendChild(v);
  const cv = v.querySelector('canvas'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
  const S = { stage: 0, fx: null, bubble: '', burst: 0 }; let live = true;
  const draw = now => { if (!live) return; requestAnimationFrame(draw); g.clearRect(0, 0, 320, 180); if (BG.complete) g.drawImage(BG, 0, 0);
    const bob = Math.sin(now / 600) * (S.stage ? .6 : 0); if (SP.complete) g.drawImage(SP, S.stage * 40, 0, 40, 56, 124, 18 + bob, 72, 101);
    if (S.fx){ const q = (now - S.fx.t) / 1400; if (q > 1) S.fx = null; else { const k = S.fx.k; g.save();
      if (k === 'water') for (let i = 0; i < 14; i++){ const x = 150 + (i * 37 % 24), y = 40 + ((q * 90 + i * 13) % 60); g.fillStyle = '#7AC8F8'; g.fillRect(x, y, 1, 3); }
      else if (k === 'sun'){ g.globalAlpha = .5 * Math.sin(q * Math.PI); const gr = g.createRadialGradient(160, 30, 0, 160, 30, 90); gr.addColorStop(0, '#FFE070'); gr.addColorStop(1, 'rgba(255,224,112,0)'); g.fillStyle = gr; g.fillRect(0, 0, 320, 180); }
      else if (k === 'song') for (let i = 0; i < 5; i++){ const x = 130 + i * 15 + Math.sin(q * 8 + i) * 4, y = 90 - q * 60 - i * 4; g.fillStyle = '#D8A8FF'; g.fillRect(x, y, 2, 2); g.fillRect(x + 1, y - 5, 1, 5); g.fillRect(x + 2, y - 5, 2, 1); }
      else { g.globalAlpha = .6 * Math.sin(q * Math.PI); g.fillStyle = 'rgba(20,20,60,.6)'; g.fillRect(0, 0, 320, 180); g.globalAlpha = Math.sin(q * Math.PI); for (let i = 0; i < 20; i++){ g.fillStyle = '#E8ECFF'; g.fillRect(140 + (i * 53 % 40), 50 + (i * 31 % 60) - q * 10, 1, 1); } }
      g.restore(); } }
    if (S.burst){ const q = (now - S.burst) / 1200; if (q < 1){ g.strokeStyle = `rgba(255,240,200,${1 - q})`; g.lineWidth = 2; g.beginPath(); g.arc(160, 80, 10 + q * 90, 0, 7); g.stroke(); g.fillStyle = `rgba(255,255,255,${.5 * (1 - q)})`; g.fillRect(0, 0, 320, 180); } }
    if (S.bubble){ g.font = '10px G11B, Pretendard, sans-serif'; const w = g.measureText(S.bubble).width + 12, x = Math.min(314 - w, 196); g.fillStyle = 'rgba(255,255,255,.96)'; g.fillRect(x, 26, w, 17); g.fillRect(x + 4, 43, 4, 3); g.fillStyle = '#2A1830'; g.fillText(S.bubble, x + 6, 38); } };
  requestAnimationFrame(draw); requestAnimationFrame(() => v.classList.add('on'));
  const hd = v.querySelector('.hd span'), st = v.querySelector('.st'), msg = v.querySelector('.msg'), cnt = { water: 0, sun: 0, song: 0, moon: 0 }; let shine = 0;
  const plan = [['water', 'water'], ['song', 'moon'], ['moon', 'moon'], ['sun', 'moon']];   // [그날 씨앗 기분, 고를 것]
  for (let d = 0; d < 4; d++){
    const [mood] = plan[d]; hd.textContent = `${d + 1}일째 · 오늘 1번 돌볼 수 있어요`; S.bubble = MOOD[mood]; msg.textContent = '';
    st.innerHTML = `<i>반짝임 ${'✦'.repeat(shine) || '-'}</i><i>${Object.entries(cnt).filter(([, n]) => n).map(([k, n]) => `${CARE.find(c => c[0] === k)[1].split(' ')[0]} ${n}`).join(' · ') || '아직 안 돌봤어요'}</i>`;
    v.querySelectorAll('[data-sc]').forEach(b => { b.classList.remove('on'); b.disabled = false; });
    const k = await new Promise(res => v.querySelectorAll('[data-sc]').forEach(b => b.onclick = () => { v.querySelectorAll('[data-sc]').forEach(x => x.disabled = true); b.classList.add('on'); res(b.dataset.sc); }));
    cnt[k]++; S.bubble = ''; S.fx = { k, t: performance.now() }; await sleep(1500);
    if (k === mood){ shine++; msg.textContent = '씨앗이 기분 좋아해요! 반짝임 +1'; } else msg.textContent = '씨앗이 조용히 받아들였어요.';
    await sleep(1400);
    dayEl.textContent = `${d + 2}일째`; dayEl.style.opacity = 1; await sleep(1000);
    S.stage = d === 0 ? 1 : d === 1 ? 2 : d === 2 ? 3 + MINE : S.stage;   // 넷째 날 아침 꽃봉오리: 꽃 색이 살짝 비쳐요
    dayEl.style.opacity = 0; await sleep(700);
  }
  // 5일째: 꽃 피움
  hd.textContent = '5일째 · 꽃이 피려고 해요'; st.innerHTML = `<i>반짝임 ${'✦'.repeat(shine)}</i>`; msg.textContent = ''; v.querySelector('.bt').style.visibility = 'hidden';
  await sleep(1400); S.burst = performance.now(); S.stage = 15 + MINE; await sleep(1300);
  msg.textContent = `「${FINAL[MINE]}」${iga(FINAL[MINE])} 피었어요! 반짝임 ${shine}개`; await sleep(2600);
  v.classList.remove('on'); await sleep(500); live = false; v.remove();
  // 광장 전시 · 투표
  await talk('열두 명 모두 다른 꽃이 피었어요! 광장에 전시해 둘게요.'); await talk('가장 마음에 드는 꽃에 하트를 하나 눌러 줘요. 자기 꽃은 안 돼요!', 1500);
  const ex = document.createElement('div'); ex.id = 'sdv'; const NM = ['민준 (나)', '하늘', '서연', '도윤', '지우', '수아', '예준', '하은', '시우', '유나', '지호', '서아'], SPC = [3, 4, 1, 2, 9, 0, 6, 11, 7, 5, 10, 8], HT = [0, 9, 5, 7, 3, 4, 2, 6, 1, 3, 2, 4];
  ex.innerHTML = `<div class="p"><div class="hd"><b>광장 꽃 전시</b><span>하트는 한 번만</span></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:2px 8px 8px">${NM.map((n, i) => `<div style="display:flex;flex-direction:column;align-items:center;background:#2A2040;border-radius:10px;padding:4px 1px">${plantIcon(15 + SPC[i], 46)}<b style="font-family:var(--f-pxb);font-size:11px">${n}</b><span style="font-size:10px;color:#C8B8F0;white-space:nowrap">${FINAL[SPC[i]]}</span><button data-sv="${i}" ${i === 0 ? 'disabled' : ''} style="margin-top:3px;min-height:30px;min-width:56px;border-radius:9px;border:1px solid #6A4A8A;background:#3A2C52;color:#FFB0D0;font-family:var(--f-pxb);font-size:12px">♥ <span>${HT[i]}</span></button></div>`).join('')}</div><div class="msg"></div></div>`;
  document.body.appendChild(ex); paintIcons(); requestAnimationFrame(() => ex.classList.add('on'));
  await new Promise(res => ex.querySelectorAll('[data-sv]').forEach(b => b.onclick = () => { const s = b.querySelector('span'); s.textContent = +s.textContent + 1; b.style.background = '#6A3A6A'; ex.querySelectorAll('[data-sv]').forEach(x => x.disabled = true); res(); }));
  ex.querySelector('.msg').textContent = '하트를 눌렀어요. 저녁에 결과가 나와요.'; await sleep(2200);
  dayEl.textContent = '그날 저녁'; dayEl.style.opacity = 1; await sleep(1100); dayEl.style.opacity = 0;
  ex.querySelector('.msg').innerHTML = '1등 하늘 · 무지개 꽃 ♥9 · 공동 2등 도윤 · 노래하는 종꽃 ♥7, 하은 · 수정 선인장 ♥7'; await sleep(2600);
  ex.classList.remove('on'); await sleep(500); ex.remove();
  await showCard(`${plantIcon(15 + MINE)}「${FINAL[MINE]} 화분」<small>참가 선물 · 내 방 가구 가방에 넣었어요</small>`, 2600); paintIcons();
  await sleep(600); window.__sdDone = true;
};
})();
