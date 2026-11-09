// 요일 던전 입구 시안: 묘지 뒤 마른 우물 (등불 마을 12, 55)
//   tools/daydungeon/well_run.js 가 화면에 넣어 찍어요. 게임 코드 아님.
(() => {
  const WX = 12, WY = 55;
  // 우물 그림 (지도 픽셀 그대로 · 30 × 34)
  const well = (open, t = 0) => {
    const c = document.createElement('canvas'); c.width = 30; c.height = 34; const g = c.getContext('2d');
    const px = (x, y, col, w = 1, h = 1) => { g.fillStyle = col; g.fillRect(x, y, w, h); };
    // 그림자
    g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.ellipse(15, 29, 13, 4.5, 0, 0, 7); g.fill();
    // 몸통 (앞면 돌담)
    const ST = ['#6b6878', '#5a5868', '#7a7688', '#4e4c5c'];
    for (let y = 19; y < 29; y++) for (let x = 3; x < 27; x++){
      const dx = (x - 15) / 12, top = 19 + Math.round(4 * Math.sqrt(Math.max(0, 1 - dx * dx))), bot = 25 + Math.round(4 * Math.sqrt(Math.max(0, 1 - dx * dx)));
      if (y < top - 4 || y > bot) continue;
      const row = Math.floor((y - 19) / 3), brick = Math.floor((x + (row % 2) * 2) / 4);
      let col = ST[(brick + row) % 4]; if ((x + (row % 2) * 2) % 4 === 0 || (y - 19) % 3 === 0) col = '#2e2c3a';
      if (y >= bot - 1) col = '#2a2834';
      if ((brick * 7 + row * 3) % 9 === 0 && (y - 19) % 3 === 1) col = '#4f6a3a';   // 이끼
      px(x, y, col);
    }
    // 테두리 (위에서 본 돌 고리)
    g.save(); g.translate(15, 19);
    g.fillStyle = '#2e2c3a'; g.beginPath(); g.ellipse(0, 0, 12.5, 5.5, 0, 0, 7); g.fill();
    g.fillStyle = '#8a8698'; g.beginPath(); g.ellipse(0, 0, 12, 5, 0, 0, 7); g.fill();
    g.fillStyle = '#9c98aa'; g.beginPath(); g.ellipse(0, -.6, 11, 4.2, 0, 0, 7); g.fill();
    // 안쪽 구멍
    g.fillStyle = '#0c0814'; g.beginPath(); g.ellipse(0, .4, 8.5, 3.2, 0, 0, 7); g.fill();
    if (open){   // 바닥에서 새어 나오는 빛
      const a = .55 + .25 * Math.sin(t / 400), gr = g.createRadialGradient(0, .6, 0, 0, .6, 8);
      gr.addColorStop(0, `rgba(190,150,255,${a})`); gr.addColorStop(.6, `rgba(120,90,220,${a * .45})`); gr.addColorStop(1, 'rgba(60,40,140,0)');
      g.fillStyle = gr; g.beginPath(); g.ellipse(0, .4, 8.5, 3.2, 0, 0, 7); g.fill();
    } else {   // 주말: 판자로 덮어 둠
      g.fillStyle = '#5a3a24'; for (let i = -2; i <= 2; i++) g.fillRect(i * 3.4 - 1.5, -3, 3, 6.6); g.fillStyle = '#2a1a10'; for (let i = -2; i <= 2; i++) g.fillRect(i * 3.4 + 1.5, -3, .6, 6.6);
    }
    g.restore();
    // 돌 테두리 무늬 (금 간 곳)
    [[5, 18], [9, 15], [20, 15], [24, 18], [14, 23], [19, 22]].forEach(([x, y]) => px(x, y, '#5e5a6c'));
    // 부러진 도르래 기둥 (왼쪽은 성하고 오른쪽은 부러졌어요)
    px(4, 5, '#3a2416', 2, 15); px(5, 5, '#6a4428', 1, 15); px(4, 4, '#2a1a10', 2, 1);
    px(24, 12, '#3a2416', 2, 8); px(25, 12, '#6a4428', 1, 8); px(24, 11, '#6a4428'); px(25, 10, '#6a4428');   // 부러진 끝
    px(4, 6, '#3a2416', 13, 2); px(5, 6, '#7a5232', 11, 1); px(17, 7, '#3a2416', 2, 1); px(18, 8, '#3a2416');   // 꺾인 가로대
    // 밧줄: 가로대에서 우물 안으로
    for (let y = 8; y < 20; y++) px(12 + (y % 3 === 0 ? 1 : 0), y, y % 2 ? '#c8a878' : '#a88858');
    px(11, 8, '#c8a878', 3, 1);
    if (open){   // 위로 떠오르는 빛 알갱이
      for (let i = 0; i < 4; i++){ const k = ((t / 1400 + i / 4) % 1), y = 18 - k * 16, x = 15 + Math.sin(i * 2.3 + t / 500) * 5;
        g.fillStyle = `rgba(210,180,255,${(1 - k) * .9})`; g.fillRect(Math.round(x), Math.round(y), 1, 1); }
    }
    return c;
  };
  const place = (open, t) => World.setProps('town', [{ id: 'daywell', x: WX, y: WY, img: well(open, t), sw: 30, sh: 34, ax: 15, ay: 30, solid: true, light: open ? { r: 36, c: [180, 140, 255], a: .55 } : null }], 'daywell');

  // 들여다보는 창 (레이드 거울 탑 창과 같은 틀)
  const DAYS = [
    { d: '월', n: '철갑 거북 「바위등」', k: '체력이 엄청 많아요', c: '#9fe08a', f: 0 },
    { d: '화', n: '붉은 늑대왕 「송곳니」', k: '한 방이 아파요', c: '#ff5a4a', f: 2 },
    { d: '수', n: '늪 마녀 「독버섯 할멈」', k: '독이 쌓여요', c: '#9cff6a', f: 4 },
    { d: '목', n: '그림자 쌍둥이 「낮과 밤」', k: '둘이 함께 와요', c: '#e8e4ff', f: 6 },
    { d: '금', n: '시계 장인 인형 「태엽공」', k: '빠르고 졸개를 불러요', c: '#ffc84a', f: 8 }];
  const LV = [['쉬움', 20, '처음 깨면 3,000 G'], ['보통', 35, '처음 깨면 6,000 G'], ['어려움', 45, '처음 깨면 장신구 강화 재료']];
  const st = document.createElement('style'); st.textContent = `#dwx{position:fixed;inset:0;z-index:9000;background:rgba(8,6,20,.72);display:flex;align-items:center;justify-content:center;padding:16px}
.dwbox{width:min(420px,100%);background:#1c1430;border:2px solid #4a3a6a;border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:8px;color:#f4ecff}
.dwhd{display:flex;align-items:center;gap:8px}.dwhd b{font-family:G11B,Pretendard,sans-serif;font-size:16px;flex:1}.dwhd span{font-size:12px;color:#cbbbe8}.dwcl{background:none;border:0;color:#cbbbe8;font-size:18px}
.dwwk{display:flex;gap:4px}.dwwk i{flex:1;font-style:normal;text-align:center;font-size:11px;padding:3px 0;border-radius:6px;background:#2a1f44;color:#8a7aa8}.dwwk i.on{background:var(--c);color:#1c1430;font-family:G11B,Pretendard,sans-serif}
.dwbs{display:flex;align-items:center;gap:10px;border:2px solid var(--c);border-radius:10px;padding:6px 10px;background:rgba(255,255,255,.03)}
.dwbs i{width:80px;height:80px;flex:none;background:url(art/day_bosses.png) 0 0/800px 80px no-repeat;image-rendering:pixelated}
.dwbs div{flex:1;display:flex;flex-direction:column;gap:3px}.dwbs b{font-size:14px}.dwbs span{font-size:12px;color:var(--c)}
.dwlv{display:flex;align-items:center;gap:10px;border:2px solid #4a3a6a;border-radius:10px;padding:6px 10px}
.dwlv div{flex:1;display:flex;flex-direction:column;gap:2px}.dwlv b{font-size:14px}.dwlv span{font-size:11px;color:#cbbbe8}.dwlv em{font-style:normal;font-size:11px;color:#ffd27a}.dwlv em.done{color:#8a7aa8}
.dwft{text-align:center;font-size:11px;color:#b9a8d8}`; document.head.appendChild(st);
  const panel = (di, left = 3, done = []) => {
    const D = DAYS[di], o = document.getElementById('dwx') || document.body.appendChild(Object.assign(document.createElement('div'), { id: 'dwx' }));
    o.innerHTML = `<div class="dwbox" style="--c:${D.c}"><div class="dwhd"><b>마른 우물 아래</b><span>오늘 ${left} / 3</span><button class="dwcl">✕</button></div>
      <div class="dwwk">${DAYS.map((x, i) => `<i class="${i === di ? 'on' : ''}">${x.d}</i>`).join('')}</div>
      <div class="dwbs"><i style="background-position:${-D.f * 80}px 0"></i><div><b>${D.d}요일 · ${D.n}</b></div></div>
      ${LV.map(([n, l, r], i) => `<div class="dwlv"><div><b>${n}</b><span>권장 레벨 ${l}</span>${done.includes(i) ? '<em class="done">처음 보상 받음</em>' : `<em>${r}</em>`}</div><button class="btn go">내려가기</button></div>`).join('')}
      <div class="dwft">1 ~ 4 명</div></div>`;
  };
  window.__wellMock = { place, panel, tile: [WX, WY] };
})();
