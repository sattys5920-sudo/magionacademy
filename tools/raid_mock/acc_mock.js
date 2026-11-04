// 보스 기념품(장신구) 시안: 모의 사이트에서 window.__accMock('lobby' | 'view' | 'pick') 로 화면을 보여 줘요
//   기념품 그림: art/raid_acc.png (LPC 부품에서 잘라 만든 32 칸 × 4, tools/iso/lpc/raid_acc_lpc.py)
window.__accIcs = {};
window.__accLoad = () => new Promise(r => { const im = new Image(); im.onload = () => { ['crown', 'cape', 'hat', 'neck'].forEach((k, i) => [true, false].forEach(own => { const c = document.createElement('canvas'); c.width = c.height = 32; const g = c.getContext('2d'); g.drawImage(im, i * 32, 0, 32, 32, 0, 0, 32, 32);
  if (!own){ const d = g.getImageData(0, 0, 32, 32); for (let j = 0; j < d.data.length; j += 4) if (d.data[j + 3]) { d.data[j] = d.data[j + 1] = d.data[j + 2] = 60; d.data[j + 3] = 160; } g.putImageData(d, 0, 0); }
  __accIcs[k + own] = c.toDataURL(); })); r(); }; im.src = 'art/raid_acc.png?v=' + Date.now(); });
window.__accIc = (k, own = true) => __accIcs[k + own];
window.__ACC = [   // 장신구마다 능력 하나 · 별(★1~5)이 오를수록 커져요
  { k: 'crown', n: '얼음 왕관', b: '얼음 거인', st: 2, cp: 1, own: true, on: true, e: s => `MP 사용량 −${4 + s * 3} %` },
  { k: 'cape', n: '용 비늘 망토', b: '불꽃 용', st: 1, cp: 0, own: true, e: s => `쓰러질 때 한 번 버티기 · 체력 ${15 + s * 10} % 남김` },
  { k: 'hat', n: '그림자 모자', b: '그림자 마녀', own: false, e: s => `MP 회복량 +${5 + s * 5} %` },
  { k: 'neck', n: '톱니 시계 목걸이', b: '시계탑 골렘', own: false, e: s => `스킬 재사용 대기 −${2 + s * 3} %` }];
window.__accMock = async (mode) => {
  await __accLoad();
  const ex = window.__T.meRaw().ex = Object.assign(window.__T.meRaw().ex || {}, { job: 'black', exp: 60000, ar: 2, wp: 2, n: 0, xv: 3 });
  window.__T.openSheet('home', 'explore'); await new Promise(r => setTimeout(r, 600));
  const hideToast = () => [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && /희미한 마법/.test(e.textContent)).forEach(e => { let q = e; while (q.parentElement && q.parentElement !== document.body) q = q.parentElement; q.style.display = 'none'; }); hideToast(); setTimeout(hideToast, 300);
  const st = document.createElement('style'); st.textContent = `.acic{width:40px;height:40px;image-rendering:pixelated;display:block}.acbig{width:84px;height:84px;image-rendering:pixelated;filter:drop-shadow(0 0 6px #7fe6ff88)}
  .acgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.acc{border:2px solid var(--line,#3a2e56);border-radius:10px;padding:8px;display:flex;flex-direction:column;gap:4px;background:rgba(255,255,255,.03)}
  .acc.on{border-color:#7fe6ff;box-shadow:0 0 0 1px #7fe6ff55}.acc.no{opacity:.7}.acc .h{display:flex;gap:8px;align-items:center}.acc b{font-size:13px}.acc .s{font-size:11px}
  .acst{color:#ffd24a;letter-spacing:1px;font-size:12px}.acst i{color:#4a3e60;font-style:normal}.actag{font-size:10px;padding:1px 6px;border-radius:8px;background:#7fe6ff;color:#14202e;margin-left:auto}
  .acbar{height:8px;border-radius:4px;background:#2a2040;overflow:hidden;margin-top:4px}.acbar i{display:block;height:100%;background:linear-gradient(90deg,#7fe6ff,#c08aff,#ffd24a)}
  .aclist{display:flex;flex-direction:column;gap:6px;margin-top:12px}.acrow{display:flex;align-items:center;gap:10px;border:2px solid var(--line,#3a2e56);border-radius:10px;padding:6px 10px}.acrow.on{border-color:#7fe6ff}.acrow.no{opacity:.6}.acrow b{font-size:13px}.acslot{display:inline-flex;align-items:center;gap:4px}.acslot img{width:20px;height:20px;image-rendering:pixelated}`; document.head.appendChild(st);
  const stars = (s) => `<span class="acst">${'★'.repeat(s)}<i>${'★'.repeat(5 - s)}</i></span>`;
  if (mode === 'lobby'){
    const ar = document.getElementById('xar'); const row = ar.parentElement;
    const b = document.createElement('button'); b.className = 'btn'; b.style.cssText = 'width:100%'; b.innerHTML = `<span class="acslot"><img src="${__accIc('crown')}"> 장신구 · 얼음 왕관 ★2</span>`;
    row.insertAdjacentElement('afterend', b); return 1; }
  document.getElementById('xar').click(); await new Promise(r => setTimeout(r, 400));
  [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && e.textContent.trim() === '방어구 강화').forEach(e => { e.textContent = '장신구'; });
  const sub = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && /흑마법사 ·/.test(e.textContent)); if (sub) sub.textContent = '보스 기념품 · 한 번에 하나만 찰 수 있어요';
  const sec = document.querySelector('.sec .box.px'); const A = __ACC, on = A[0];
  sec.innerHTML = `<div style="display:flex;gap:14px;align-items:center"><div class="xarbox t4" style="display:flex;align-items:center;justify-content:center"><img class="acbig" src="${__accIc(on.k)}"></div>
    <div style="flex:1"><b>${on.n}</b> ${stars(on.st)}<div class="s" style="margin-top:4px">${on.e(on.st)}</div><div class="s sub" style="margin-top:6px">★${on.st + 1} 이면 ${on.e(on.st + 1)} · 같은 기념품 ${on.cp} / ${on.st}</div><div class="acbar"><i style="width:${on.cp / on.st * 100}%"></i></div></div></div>
    <div class="aclist">${A.map(a => `<div class="acrow${a.on ? ' on' : ''}${a.own ? '' : ' no'}"><img class="acic" src="${__accIc(a.k, a.own)}"><div style="flex:1;min-width:0"><b>${a.own ? a.n : '???'}</b> ${a.own ? stars(a.st) : ''}<div class="s ${a.own ? '' : 'sub'}">${a.own ? a.e(a.st) : `${a.b} 레이드에서 얻어요`}</div></div>${a.on ? '<span class="actag">차는 중</span>' : a.own ? '<button class="btn go" style="padding:6px 12px">차기</button>' : ''}</div>`).join('')}</div>
    <div class="s sub" style="margin-top:10px">한 번에 하나만 찰 수 있어요 · 탐사와 레이드에서 모두 효과가 있어요</div>`;
  const ok = document.getElementById('aok'); if (ok) ok.textContent = '돌아가기';
  return 1;
};
