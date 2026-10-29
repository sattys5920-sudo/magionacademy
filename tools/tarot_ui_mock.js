// 오늘의 운세 뽑기 화면 시안 (페이지에 넣어서 써요)
window.tarotMock = function(){
  const N = 22, W = 60, H = 90, NAMES = ['The Fool','The Magician','The High Priestess','The Empress','The Emperor','The Hierophant','The Lovers','The Chariot','Strength','The Hermit','Wheel of Fortune','Justice','The Hanged Man','Death','Temperance','The Devil','The Tower','The Star','The Moon','The Sun','Judgement','The World'];
  const RO = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI'];
  const FX = {19:'요리할 때 별이 하나 더 나올 확률 ↑', 17:'희귀 물고기 확률 ↑', 0:'걷는 속도 +15%'};
  const st = document.createElement('style'); st.textContent = `
  #tr2{position:absolute;inset:0;z-index:50;background:radial-gradient(ellipse at 50% 40%,rgba(58,36,99,.96),rgba(12,8,24,.97));overflow:hidden;font-family:var(--f-pxb);color:#F1E9FF}
  #tr2 h2{position:absolute;top:28px;left:0;right:0;text-align:center;margin:0;font-size:20px;color:#FFD866}
  #tr2 .trtip{position:absolute;left:50%;top:calc(50% + 150px);transform:translateX(-50%);white-space:nowrap;padding:9px 18px;border-radius:20px;background:rgba(20,12,36,.85);border:2px solid #8A6AC8;font-size:15px;color:#FFE9A0;opacity:0;transition:opacity .4s}
  #tr2 .c{position:absolute;left:50%;top:50%;width:${W}px;height:${H}px;margin:-${H/2}px 0 0 -${W/2}px;transform-style:preserve-3d;transition:transform .55s cubic-bezier(.3,1.2,.5,1),opacity .4s,filter .3s;cursor:pointer}
  #tr2 .c i{position:absolute;inset:0;backface-visibility:hidden;image-rendering:pixelated;background:url(art/tarot.png) 0 0/${23*W}px ${H}px;filter:drop-shadow(0 3px 0 rgba(0,0,0,.35))}
  #tr2 .c i.b{background-position:-${22*W}px 0}#tr2 .c i.f{transform:rotateY(180deg)}
  #tr2 .c.hov{filter:brightness(1.25)}
  #tr2 .res{position:absolute;left:0;right:0;bottom:70px;text-align:center;opacity:0;transition:opacity .5s}#tr2 .res b{display:block;font-size:22px;color:#FFD866;margin-bottom:8px}#tr2 .res span{display:inline-block;font-size:15px;background:rgba(255,255,255,.1);padding:8px 14px;border-radius:12px}
  #tr2 .ok{display:block;margin:14px auto 0;min-height:48px;padding:0 34px;border-radius:24px;border:2px solid #2A1E3A;background:#FFD866;color:#2A1E3A;font-family:var(--f-pxb);font-size:16px;box-shadow:0 3px 0 #B8862E}
  #tr2 .glow{position:absolute;left:50%;top:44%;width:260px;height:260px;margin:-130px;border-radius:50%;background:radial-gradient(circle,rgba(255,216,102,.45),rgba(255,216,102,0) 70%);opacity:0;transition:opacity .6s}`;
  document.head.appendChild(st);
  const v = document.createElement('div'); v.id = 'tr2'; v.innerHTML = '<h2>오늘의 운세</h2><div class="glow"></div><div class="trtip">한 장을 골라요</div><div class="res"></div>'; document.querySelector('#stage').appendChild(v);
  const deck = [...Array(N).keys()].sort(() => Math.random() - .5);   // 섞인 순서 (뒤집으면 나오는 카드)
  const cs = deck.map((k, i) => { const c = document.createElement('div'); c.className = 'c'; c.innerHTML = `<i class="b"></i><i class="f" style="background-position:-${k*W}px 0"></i>`; c.style.transform = `translate(0px,${-i*.6}px)`; c.dataset.k = k; v.appendChild(c); return c; });
  const VW = v.clientWidth, VH = v.clientHeight;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  // 1) 섞기: 반씩 갈라졌다 합쳐지기 3번
  (async () => {
    await sleep(500);
    for (let r = 0; r < 3; r++){
      cs.forEach((c, i) => { const s = i % 2 ? 1 : -1; c.style.transform = `translate(${s*46}px,${-i*.6 + (r%2?6:-6)}px) rotate(${s*8}deg)`; }); await sleep(380);
      cs.forEach((c, i) => { c.style.transform = `translate(0px,${-i*.6}px) rotate(${(Math.random()-.5)*6}deg)`; c.style.zIndex = Math.floor(Math.random()*N); }); await sleep(380);
    }
    // 2) 펼치기: 아래쪽을 중심으로 부채꼴
    const R = Math.min(VW * .45, 230), cx = 0, cy = R * .9 + 20, a0 = -55, a1 = 55;
    cs.forEach((c, i) => { const a = a0 + (a1 - a0) * i / (N - 1), rad = a * Math.PI / 180, x = cx + Math.sin(rad) * R, y = cy - Math.cos(rad) * R; c.dataset.t = `translate(${x}px,${y - 10}px) rotate(${a}deg)`; c.style.zIndex = i; setTimeout(() => { c.style.transform = c.dataset.t; }, i * 35); });
    await sleep(N * 35 + 500); v.querySelector('.trtip').style.opacity = 1;
    cs.forEach(c => { c.onmouseenter = () => { c.style.transform = c.dataset.t + ' translateY(-14px)'; c.classList.add('hov'); }; c.onmouseleave = () => { c.style.transform = c.dataset.t; c.classList.remove('hov'); }; c.onclick = () => pick(c); });
  })();
  // 3) 고르면: 나머지는 아래로 사라지고, 고른 카드가 가운데로 와서 뒤집혀요
  async function pick(c){
    cs.forEach(o => { o.onclick = o.onmouseenter = o.onmouseleave = null; if (o !== c){ o.style.transition = 'transform .5s ease-in,opacity .4s'; o.style.transform = o.dataset.t + ` translateY(${VH}px)`; o.style.opacity = 0; } });
    v.querySelector('.trtip').style.opacity = 0; c.style.zIndex = 99;
    c.style.transform = `translate(0px,-40px) scale(1.3)`; await sleep(600);
    c.style.transition = 'transform .7s cubic-bezier(.3,1.3,.5,1)'; c.style.transform = `translate(0px,-60px) scale(2.6) rotateY(180deg)`; v.querySelector('.glow').style.opacity = 1; await sleep(800);
    const k = +c.dataset.k, r = v.querySelector('.res'); r.innerHTML = `<b>${RO[k]} ${NAMES[k]}</b><span>${FX[k] || '오늘 하루 작은 행운이 따라와요'}</span><button class="ok">받기</button>`; r.style.opacity = 1;
  }
  window.__tarotPick = i => pick(cs[i]);
};
