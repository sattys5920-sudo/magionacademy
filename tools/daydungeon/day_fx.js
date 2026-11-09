// 요일 던전 보스 이펙트 시안 (그림만, 게임 코드 아님): 모의 사이트 index.html 의 모듈 스크립트 안에 넣어서
//   window.__dayFx({ b: 0~4, sc: 'a' | 'b' | 'c', t: 0~1 }) 로 장면을 그려요. 돌리기: node tools/daydungeon/day_fx_run.js
//   보스 그림: art/day_bosses.png (64 칸 × 2 동작 × 5 종: 서 있기 · 기술). 전투 화면 크기 · 파티 자리(앞열 · 뒤열)는 게임 탐사 전투(xLayout)와 같아요
window.__dayFx = async (o) => {
  const A = World.Avatar, W = 384, H = 216, b = o.b || 0, sc = o.sc || 'a', T = o.t ?? .5;
  const BS = [
    { day: '월', n: '바위등', full: '철갑 거북 「바위등」', c: '#9fe08a', wall: ['#2e3a30', '#1c241e'], fl: ['#3a4636', '#1e261c'], torch: '#ffd27a', moss: 1 },
    { day: '화', n: '송곳니', full: '붉은 늑대왕 「송곳니」', c: '#ff5a4a', wall: ['#3a1e1c', '#20100f'], fl: ['#46261f', '#22110d'], torch: '#ff9a4a' },
    { day: '수', n: '독버섯 할멈', full: '늪 마녀 「독버섯 할멈」', c: '#9cff6a', wall: ['#24301f', '#1c1428'], fl: ['#2a3a22', '#1a1424'], torch: '#b8ff7a' },
    { day: '목', n: '낮과 밤', full: '그림자 쌍둥이 「낮과 밤」', c: '#e8e4ff', wall: ['#3a3848', '#1a1824'], fl: ['#3e3c4a', '#1c1a26'], torch: '#fff4d0' },
    { day: '금', n: '태엽공', full: '시계 장인 인형 「태엽공」', c: '#ffc84a', wall: ['#3e2c1a', '#22180e'], fl: ['#4a3420', '#26190e'], torch: '#ffc060' }][b];
  // 장면별 숫자 · 글
  const S = {
    '0a': { hp: 82, chips: [['등껍질 방어 자세', '#9fe08a'], ['받는 피해 −50 %', '#ffe07a']], log: `바위등이 등껍질 속으로 쏙 들어갔어요.... 지금은 <b style="color:#ffe07a">피해가 반만</b> 들어가요` },
    '0b': { hp: 64, chips: [['껍질이 열렸어요', '#ff9a6a'], ['받는 피해 +30 %', '#ffb0a0'], ['남은 시간 6 초', '#cbbbe8']], log: `껍질이 열렸어요. 지금 <b style="color:#ff9a6a">몰아쳐요</b>.......` },
    '0c': { hp: 47, chips: [['50 % · 화가 났어요', '#ff8a6a']], log: '', dodge: '바위등이 몸을 웅크려요.... 곧 굴러와요' },
    '1a': { hp: 71, chips: [['앞열을 노려요', '#ff8a7a']], log: `송곳니의 <b style="color:#ff5a4a">한입 물기</b>. 기사 「하랑」 이 크게 다쳤어요.......` },
    '1b': { hp: 52, chips: [['큰 기술 준비', '#ff5a4a']], log: '', dodge: '송곳니가 낮게 엎드려요.... 앞열을 노려요' },
    '1c': { hp: 25, chips: [['25 % · 포효', '#ff5a4a'], ['공격 +20 %', '#ffb0a0'], ['속도 +10 %', '#ffb0a0']], log: `송곳니가 <b style="color:#ff5a4a">포효</b>해요. 눈이 붉게 빛나요.......` },
    '2a': { hp: 76, chips: [['모든 공격에 독', '#9cff6a'], ['독 3 겹 · 1 초마다 −9', '#c8ffb0']], log: `독이 쌓일수록 더 아파요.... 정화가 필요해요` },
    '2b': { hp: 49, chips: [['독 안개 · 10 초', '#9cff6a'], ['모두 1 초마다 −14', '#c8ffb0']], log: `독버섯 할멈이 <b style="color:#9cff6a">독 안개</b> 를 깔았어요.......` },
    '2c': { hp: 44, chips: [['정화 · 독이 사라졌어요', '#fff2a0']], log: `성직자 「소이」 의 <b style="color:#fff2a0">정화의 빛</b>. 파티의 독이 모두 사라졌어요.......` },
    '3a': { hp: 68, hp2: 61, chips: [['둘을 비슷하게 깎아요', '#e8e4ff']], log: `한쪽만 쓰러뜨리면 남은 쪽이 화가 나요.... 체력을 맞춰 가며 쳐요` },
    '3b': { hp: 54, hp2: 50, chips: [['서로 보호막', '#e8e4ff'], ['피해를 막아요', '#cbbbe8']], log: '', gauge: '낮과 밤이 손을 맞잡았어요.... 끊어서 보호막을 막아요' },
    '3c': { hp: 0, hp2: 38, chips: [['낮이 쓰러졌어요', '#cbbbe8'], ['밤 공격 +50 %', '#ff9ad0']], log: `<b style="color:#ff9ad0">남은 쪽이 화가 났어요</b>.......` },
    '4a': { hp: 83, chips: [['아주 빨라요', '#ffc84a'], ['졸개 2', '#e8d0a0']], log: `태엽공이 태엽을 감아요.... <b style="color:#ffc84a">태엽 졸개</b> 가 나와요` },
    '4b': { hp: 61, chips: [['졸개 3', '#ff8a5a'], ['하나 더 나오면 폭주', '#ffb090']], log: '', warn: '졸개가 셋을 넘으면 태엽공이 폭주해요.... 광역으로 정리해요' },
    '4c': { hp: 55, chips: [['졸개 0', '#9fe08a'], ['폭주 막았어요', '#e8ffd0']], log: `흑마법사 「도윤」 의 <b style="color:#ff9a4a">불꽃 폭풍</b>. 졸개가 모두 부서졌어요.......` }}[b + sc];
  document.getElementById('dayov')?.remove();
  const ov = document.createElement('div'); ov.id = 'dayov';
  const hpBar = (nm, v, c1, c2) => `<div class="dq-rtop"><span class="dq-nm">${nm}</span><div class="dq-bar"><i style="width:${v}%;background:linear-gradient(${c1},${c2})"></i><b>${v ? v + ' %' : '쓰러짐'}</b></div></div>`;
  const top = b === 3 ? `<div class="dq-two">${hpBar('낮', S.hp, '#ffffff', '#c8c4e0')}${hpBar('밤', S.hp2, '#8a7ab8', '#3a2e5a')}</div>` : hpBar(BS.n, S.hp, '#ffe07a', '#f0a43a');
  ov.innerHTML = `<style>
#dayov{position:fixed;left:0;top:0;width:400px;box-sizing:border-box;z-index:99999;background:#140e22;color:#f4ecff;font-family:G11,Pretendard,sans-serif;display:flex;flex-direction:column;gap:6px;padding:8px}#dayov>*{flex:none}
#dayov .dq-hd{display:flex;align-items:center;gap:6px;font-family:G11B,Pretendard,sans-serif;font-size:12px;color:#cbbbe8}
#dayov .dq-hd .d{background:${BS.c};color:#1a1024;border-radius:4px;padding:1px 6px}
#dayov .dq-two{display:flex;gap:8px}#dayov .dq-two .dq-rtop{flex:1}
#dayov .dq-rtop{display:flex;align-items:center;gap:6px;font-family:G11B,Pretendard,sans-serif;font-size:13px}
#dayov .dq-bar{flex:1;height:14px;background:#2a1838;border:2px solid #1a1024;border-radius:3px;position:relative;overflow:hidden}
#dayov .dq-bar i{position:absolute;left:0;top:0;bottom:0}
#dayov .dq-bar b{position:absolute;inset:0;text-align:center;font-size:10px;line-height:14px;color:#1a1024;text-shadow:0 0 2px #fff8}
#dayov .dq-chips{display:flex;gap:4px;flex-wrap:wrap}
#dayov .dq-chips span{font-size:10px;border:1px solid currentColor;border-radius:9px;padding:1px 7px;background:#1c1430}
#dayov canvas{width:384px;height:216px;image-rendering:pixelated;border:0;border-radius:4px}
#dayov .dq-log{font-size:10px;color:#cbbbe8;background:#1c1430;border-radius:6px;padding:5px 7px}
#dayov .dq-dodge{display:flex;align-items:center;gap:12px;background:#22183a;border:2px solid ${BS.c};border-radius:8px;padding:8px 10px}
#dayov .dq-ring{position:relative;width:80px;height:80px;flex:none}
#dayov .dq-ring .o{position:absolute;inset:${Math.round(2 + T * 12)}px;border:4px solid ${BS.c};border-radius:50%;opacity:.9}
#dayov .dq-ring .z{position:absolute;inset:20px;border:4px solid #fff;border-radius:50%;box-shadow:0 0 10px ${BS.c}}
#dayov .dq-ring .dq-btn{position:absolute;inset:25px;border-radius:50%;background:#3a2a5a;display:flex;align-items:center;justify-content:center;font-family:G11B;font-size:11px;white-space:nowrap;color:#fff}
#dayov .dq-dodge p{margin:0;font-size:12px;line-height:1.6}#dayov .dq-dodge small{color:#b9a8d8;font-size:10px}
#dayov .dq-gb{flex:1}#dayov .dq-gb .g{height:12px;background:#2a1838;border:2px solid #1a1024;border-radius:3px;position:relative;overflow:hidden;margin-top:4px}
#dayov .dq-gb .g i{position:absolute;left:0;top:0;bottom:0;width:58%;background:linear-gradient(#fff6c0,#d8b050)}
#dayov .dq-gb .g u{position:absolute;top:0;bottom:0;width:2px;background:#1a1024}
#dayov .dq-kb{flex:none;background:#3a2a5a;border:2px solid #fff;border-radius:8px;padding:8px 12px;font-family:G11B;font-size:12px;color:#fff}
#dayov .dq-warn{background:#3a1410;border:2px solid #ff6a3a;border-radius:8px;padding:8px 10px;font-size:12px;line-height:1.6}
</style>
<div class="dq-hd"><span class="d">${BS.day}</span>요일 던전 · 보통 · ${BS.full}</div>
${top}
<div class="dq-chips">${S.chips.map(([t, c]) => `<span style="color:${c}">${t}</span>`).join('')}</div>
<canvas id="dcv" width="${W}" height="${H}"></canvas>
${S.log ? `<div class="dq-log">${S.log}</div>` : ''}
${S.dodge ? `<div class="dq-dodge"><div class="dq-ring"><div class="o"></div><div class="z"></div><div class="dq-btn">피하기</div></div><p><b>${S.dodge}</b><br><small>고리가 흰 원에 닿을 때 눌러요</small></p></div>` : ''}
${S.gauge ? `<div class="dq-dodge"><div class="dq-gb"><b style="font-size:12px">${S.gauge}</b><div class="g"><i></i><u style="left:25%"></u><u style="left:50%"></u><u style="left:75%"></u></div><small>끊기 58 % · 100 % 가 되면 보호막이 깨져요</small></div><div class="dq-kb">끊기</div></div>` : ''}
${S.warn ? `<div class="dq-warn"><b style="color:#ffb090">폭주 직전....</b> ${S.warn}</div>` : ''}`;
  document.body.appendChild(ov);
  const cv = ov.querySelector('#dcv'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
  const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(11 + b * 37 + sc.charCodeAt(0));
  const txt = (t, x, y, c, sz = 10, al = 'center') => { g.font = `${sz}px G11B, Pretendard, sans-serif`; g.textAlign = al; g.lineJoin = 'round'; g.lineWidth = sz > 12 ? 4 : 3; g.strokeStyle = '#1a1024'; g.strokeText(t, x, y); g.fillStyle = c; g.fillText(t, x, y); };
  const edge = (c, a) => { const e = g.createRadialGradient(W / 2, H / 2, 90, W / 2, H / 2, 240); e.addColorStop(0, 'rgba(0,0,0,0)'); e.addColorStop(1, c.replace('A', a)); g.fillStyle = e; g.fillRect(0, 0, W, H); };
  const GY = 122;   // 벽과 바닥 경계
  // ---- 배경: 우물 아래 돌방 (벽 · 바닥 판석 · 위에서 내려오는 빛 · 횃불) ----
  const bg = (wall, fl, x0 = 0, x1 = W) => {
    const wg = g.createLinearGradient(0, 0, 0, GY); wg.addColorStop(0, wall[1]); wg.addColorStop(1, wall[0]); g.fillStyle = wg; g.fillRect(x0, 0, x1 - x0, GY);
    for (let r = 0; r * 14 < GY; r++) for (let k = -1; k * 30 < W; k++){ const x = k * 30 + (r % 2) * 15, y = r * 14; if (x + 30 < x0 || x > x1) continue; g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(Math.max(x0, x), y + 13, Math.min(30, x1 - x), 1); g.fillRect(x, y, 1, 14); g.fillStyle = 'rgba(255,255,255,.05)'; g.fillRect(Math.max(x0, x + 1), y, Math.min(28, x1 - x - 1), 1); if (((r * 7 + k * 3) % 5) === 0){ g.fillStyle = 'rgba(0,0,0,.12)'; g.fillRect(Math.max(x0, x + 1), y + 1, Math.min(28, x1 - x - 1), 12); } }
    const fg = g.createLinearGradient(0, GY, 0, H); fg.addColorStop(0, fl[0]); fg.addColorStop(1, fl[1]); g.fillStyle = fg; g.fillRect(x0, GY, x1 - x0, H - GY);
    g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(x0, GY, x1 - x0, 3);
    for (let r = 0, y = GY + 3; y < H; r++){ const hh = 8 + r * 4; g.fillStyle = 'rgba(0,0,0,.22)'; g.fillRect(x0, y + hh - 1, x1 - x0, 1); const w = 34 + r * 10; for (let x = -((r * 13) % w); x < W; x += w){ if (x < x0 || x > x1) continue; g.fillRect(x, y, 1, hh); } y += hh; }
  };
  const shaft = (x, c = '255,244,210', a = .22) => {   // 우물에서 내려오는 빛기둥
    g.fillStyle = '#0a0812'; g.beginPath(); g.ellipse(x, 0, 30, 9, 0, 0, 7); g.fill(); g.fillStyle = `rgba(${c},.75)`; g.beginPath(); g.ellipse(x, 0, 22, 6, 0, 0, 7); g.fill();
    const lg = g.createLinearGradient(0, 0, 0, H); lg.addColorStop(0, `rgba(${c},${a * 1.6})`); lg.addColorStop(1, `rgba(${c},${a * .3})`); g.fillStyle = lg; g.beginPath(); g.moveTo(x - 22, 0); g.lineTo(x + 22, 0); g.lineTo(x + 60, H); g.lineTo(x - 40, H); g.fill();
    g.fillStyle = `rgba(${c},.12)`; g.beginPath(); g.ellipse(x + 10, H - 26, 62, 14, 0, 0, 7); g.fill();
    for (let i = 0; i < 18; i++){ const t = R(), y = t * H, xx = x - 20 + t * 10 + R() * (44 + t * 50); g.fillStyle = `rgba(${c},${.3 + R() * .5})`; g.fillRect(xx, y, 1, 1); }
  };
  const torch = (x, y, c) => {
    const rg = g.createRadialGradient(x, y, 2, x, y, 46); rg.addColorStop(0, c + 'aa'); rg.addColorStop(1, c + '00'); g.fillStyle = rg; g.fillRect(x - 46, y - 46, 92, 92);
    g.fillStyle = '#2a1a10'; g.fillRect(x - 2, y + 2, 4, 12); g.fillStyle = '#5a4030'; g.fillRect(x - 4, y, 8, 3);
    g.fillStyle = c; g.beginPath(); g.moveTo(x - 4, y); g.quadraticCurveTo(x - 4, y - 8, x, y - 13); g.quadraticCurveTo(x + 4, y - 8, x + 4, y); g.fill(); g.fillStyle = '#fff8e0'; g.fillRect(x - 1, y - 5, 2, 4);
  };
  if (b === 3){   // 낮과 밤: 왼쪽 반은 하얀 돌방, 오른쪽 반은 검은 돌방
    bg(['#b8b4c8', '#7a768c'], ['#c4c0d0', '#8a8698'], 0, W / 2); bg(['#24203a', '#0c0a16'], ['#2a2640', '#100e1c'], W / 2, W);
    g.fillStyle = 'rgba(255,250,230,.8)'; g.beginPath(); g.arc(96, 46, 16, 0, 7); g.fill(); for (let k = 0; k < 8; k++){ const a = k * Math.PI / 4; g.fillRect(96 + Math.cos(a) * 22 - 2, 46 + Math.sin(a) * 22 - 2, 4, 4); }
    g.fillStyle = '#e8e4ff'; g.beginPath(); g.arc(290, 46, 15, 0, 7); g.fill(); g.fillStyle = '#24203a'; g.beginPath(); g.arc(297, 42, 13, 0, 7); g.fill();
    for (let i = 0; i < 30; i++){ g.fillStyle = 'rgba(232,228,255,.6)'; g.fillRect(W / 2 + R() * W / 2, R() * GY, 1, 1); }
    g.fillStyle = '#1a1024'; g.fillRect(W / 2 - 1, 0, 2, H);
    shaft(192, '255,250,235', .16); torch(28, 70, '#fff0c0'); torch(356, 70, '#a8a0ff');
  } else {
    bg(BS.wall, BS.fl);
    if (b === 0){ for (let i = 0; i < 22; i++){ const x = R() * W, y = R() * GY; g.fillStyle = i % 2 ? 'rgba(110,160,80,.45)' : 'rgba(80,130,60,.4)'; g.beginPath(); g.ellipse(x, y, 6 + R() * 10, 3 + R() * 3, 0, 0, 7); g.fill(); } for (let i = 0; i < 9; i++){ const x = 20 + i * 42; g.fillStyle = 'rgba(90,140,70,.6)'; g.fillRect(x, 0, 2, 10 + (i * 7) % 18); g.fillStyle = 'rgba(160,220,255,.6)'; g.fillRect(x + 8, 30 + (i * 13) % 40, 1, 3); } for (let i = 0; i < 8; i++){ g.fillStyle = 'rgba(100,150,80,.5)'; g.fillRect(R() * W, GY + 4 + R() * 80, 5, 2); } }
    if (b === 1){ [[70, 18], [314, 18]].forEach(([x, y]) => { g.fillStyle = '#6a1814'; g.fillRect(x - 12, y, 24, 46); g.beginPath(); g.moveTo(x - 12, y + 46); g.lineTo(x, y + 38); g.lineTo(x + 12, y + 46); g.lineTo(x + 12, y + 54); g.lineTo(x, y + 46); g.lineTo(x - 12, y + 54); g.fill(); g.fillStyle = '#e0a040'; g.fillRect(x - 12, y, 24, 2); g.fillStyle = '#20100f'; g.beginPath(); g.arc(x, y + 22, 7, 0, 7); g.fill(); g.fillRect(x - 6, y + 24, 3, 6); g.fillRect(x + 3, y + 24, 3, 6); }); g.strokeStyle = 'rgba(0,0,0,.45)'; g.lineWidth = 2; [[180, 40], [240, 70]].forEach(([x, y]) => { for (let k = 0; k < 3; k++){ g.beginPath(); g.moveTo(x + k * 6, y); g.lineTo(x + k * 6 + 10, y + 26); g.stroke(); } }); for (let i = 0; i < 6; i++){ g.fillStyle = '#d8cdb8'; g.fillRect(40 + R() * 300, GY + 20 + R() * 70, 6, 2); } }
    if (b === 2){ for (let i = 0; i < 7; i++){ const x = 16 + i * 58 + R() * 10, y = GY - 4; const s = 4 + R() * 6; g.fillStyle = '#d8d0b8'; g.fillRect(x - 1, y - s, 3, s); g.fillStyle = i % 2 ? '#a83a5a' : '#7a3aa8'; g.beginPath(); g.ellipse(x, y - s, s, s * .6, 0, Math.PI, 0); g.fill(); g.fillStyle = '#f0e0ff'; g.fillRect(x - 2, y - s - 2, 2, 1); } for (let i = 0; i < 10; i++){ g.strokeStyle = 'rgba(40,60,30,.8)'; g.lineWidth = 2; const x = R() * W; g.beginPath(); g.moveTo(x, 0); g.quadraticCurveTo(x + 10, 20, x - 4, 30 + R() * 30); g.stroke(); } const pg = g.createLinearGradient(0, H - 40, 0, H); pg.addColorStop(0, 'rgba(90,40,120,0)'); pg.addColorStop(1, 'rgba(90,40,120,.45)'); g.fillStyle = pg; g.fillRect(0, H - 40, W, 40); }
    if (b === 4){ const gear = (cx, cy, r, c, hole) => { g.fillStyle = c; g.beginPath(); for (let k = 0; k < 24; k++){ const a = k / 24 * Math.PI * 2, rr = k % 2 ? r : r * 1.18; g.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } g.fill(); g.fillStyle = hole; g.beginPath(); g.arc(cx, cy, r * .42, 0, 7); g.fill(); }; gear(60, 40, 22, '#5a4024', '#2e2012'); gear(330, 34, 28, '#6a4c26', '#2e2012'); gear(296, 76, 14, '#7a5a2a', '#2e2012');
      g.fillStyle = '#5a3a1e'; [[120, 50], [210, 74]].forEach(([x, y]) => { g.fillRect(x, y, 70, 4); g.fillStyle = '#3a2410'; g.fillRect(x + 4, y + 4, 3, 6); g.fillRect(x + 63, y + 4, 3, 6); g.fillStyle = '#c89a4a'; for (let k = 0; k < 4; k++) g.fillRect(x + 8 + k * 15, y - 6, 6, 6); g.fillStyle = '#5a3a1e'; });
      g.fillStyle = '#9a7a3a'; g.fillRect(0, 98, W, 4); g.fillStyle = '#c8a050'; g.fillRect(0, 98, W, 1); for (let x = 20; x < W; x += 60) g.fillRect(x, 96, 4, 8); }
    shaft(176, b === 1 ? '255,220,190' : b === 2 ? '220,255,200' : '255,244,210'); torch(30, 70, BS.torch); torch(354, 70, BS.torch);
  }
  // ---- 파티 4 명 (게임과 같은 자리: 앞열은 적 쪽, 뒤열은 그 뒤) ----
  const party = [
    { job: 'knight', nm: '하랑', row: 'f', x: 94, y: 140 }, { job: 'warrior', nm: '지호', row: 'f', x: 114, y: 200 },
    { job: 'black', nm: '도윤', row: 'b', x: 42, y: 140 }, { job: 'cleric', nm: '소이', row: 'b', x: 62, y: 200 }];
  const hpOf = { '0a': [92, 95, 100, 100], '0b': [80, 88, 100, 96], '0c': [70, 64, 82, 90], '1a': [24, 78, 100, 90], '1b': [55, 62, 88, 92], '1c': [48, 40, 70, 76], '2a': [62, 58, 70, 74], '2b': [46, 42, 50, 58], '2c': [70, 66, 76, 82], '3a': [84, 80, 92, 95], '3b': [72, 70, 80, 88], '3c': [44, 52, 66, 74], '4a': [88, 90, 96, 100], '4b': [70, 64, 80, 86], '4c': [66, 60, 78, 84] }[b + sc];
  const FW = A.FW, FH = A.FH, dirL = A.meta.dirs.left, PAD = 48;
  const q = document.createElement('canvas'); q.width = FW + PAD * 2; q.height = FH + PAD * 2; const t = q.getContext('2d'); t.imageSmoothingEnabled = false;
  const tintP = { '1a': [0, 'rgba(255,60,40,.45)'], '2a': [-1, 'rgba(120,255,80,.28)'], '2b': [-1, 'rgba(120,255,80,.35)'] }[b + sc];
  const drawPeople = async () => { for (const [i, p] of party.map((p, i) => [i, p]).sort((a, c) => a[1].y - c[1].y)){
    const av = A.fromLook(ORDER_J.indexOf(p.job) * 131 + 7 + i * 3); try { await A.need(av); } catch (e) {} const sp = A.compose(av); if (!sp) continue;
    const u = { job: p.job, av, wp: 2 }; t.setTransform(1, 0, 0, 1, 0, 0); t.globalCompositeOperation = 'source-over'; t.clearRect(0, 0, q.width, q.height);
    try { xHandOf(u, sp); xArmLayer(t, u, PAD, PAD, null, 'b', 0, sp, dirL * FW); } catch (e) {}
    t.drawImage(sp, dirL * FW, 0, FW, FH, PAD, PAD, FW, FH);
    try { xArmLayer(t, u, PAD, PAD, null, 'f', 0, sp, dirL * FW); } catch (e) {}
    if (tintP && (tintP[0] === -1 || tintP[0] === i)){ t.globalCompositeOperation = 'source-atop'; t.fillStyle = tintP[1]; t.fillRect(0, 0, q.width, q.height); t.globalCompositeOperation = 'source-over'; }
    g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.ellipse(p.x, p.y, 11, 3, 0, 0, 7); g.fill();
    const lunge = b === 4 && sc === 'c' && i === 2 ? 6 : 0;
    g.save(); g.translate(p.x + lunge, 0); g.scale(-1, 1); g.drawImage(q, -(PAD + FW / 2), p.y - FH + 6 - PAD); g.restore();
    const bw = 24, bx = Math.round(p.x - bw / 2), by = Math.round(p.y - FH + 2), f = hpOf[i] / 100;   // 머리 위 체력
    g.fillStyle = '#1a1024'; g.fillRect(bx - 1, by - 1, bw + 2, 5); g.fillStyle = '#4a2a3a'; g.fillRect(bx, by, bw, 3); g.fillStyle = f > .3 ? '#7affb0' : '#ff6a4a'; g.fillRect(bx, by, Math.round(bw * f), 3);
    p.hy = by;
  } };
  // ---- 보스 그림 ----
  const bim = await new Promise(r => { const im = new Image(); im.onload = () => r(im); im.src = 'art/day_bosses.png?v=' + Date.now(); });
  const BX = 272, BY = 204, BW = 128;
  // 프레임 하나(또는 일부 sx0..sx1)를 그리기. fl = 좌우 뒤집기 (그림이 오른쪽을 보면 뒤집어 파티 쪽을 보게)
  const off = document.createElement('canvas'); off.width = off.height = 64; const oq = off.getContext('2d'); oq.imageSmoothingEnabled = false;
  const frame = (fr, sx0 = 0, sx1 = 64, sy0 = 0, sy1 = 64, tint, gray) => { oq.globalCompositeOperation = 'source-over'; oq.clearRect(0, 0, 64, 64); oq.drawImage(bim, fr * 64 + sx0, sy0, sx1 - sx0, sy1 - sy0, sx0, sy0, sx1 - sx0, sy1 - sy0);
    if (gray){ const d = oq.getImageData(0, 0, 64, 64); for (let k = 0; k < d.data.length; k += 4){ const v = (d.data[k] + d.data[k + 1] + d.data[k + 2]) / 3 * .6 + 30; d.data[k] = d.data[k + 1] = v; d.data[k + 2] = v + 10; } oq.putImageData(d, 0, 0); }
    if (tint){ oq.globalCompositeOperation = 'source-atop'; oq.fillStyle = tint; oq.fillRect(0, 0, 64, 64); } return off; };
  const drawSpr = (fr, x, y, s, o2 = {}) => { const c = frame(fr, o2.sx0, o2.sx1, o2.sy0, o2.sy1, o2.tint, o2.gray), w = 64 * s; g.save(); g.globalAlpha = o2.a ?? 1; g.translate(x, y); if (o2.rot) g.rotate(o2.rot); if (o2.fl) g.scale(-1, 1); g.drawImage(c, -w / 2, -w + 2 * s, w, w); g.restore(); };
  const shadow = (x, y, rx) => { g.fillStyle = 'rgba(0,0,0,.4)'; g.beginPath(); g.ellipse(x, y, rx, rx * .22, 0, 0, 7); g.fill(); };
  const aura = (x, y, rx, ry, c, a = .5) => { const rg = g.createRadialGradient(x, y, 4, x, y, Math.max(rx, ry)); rg.addColorStop(0, c.replace('A', a)); rg.addColorStop(1, c.replace('A', 0)); g.save(); g.translate(x, y); g.scale(rx / Math.max(rx, ry), ry / Math.max(rx, ry)); g.translate(-x, -y); g.fillStyle = rg; g.beginPath(); g.arc(x, y, Math.max(rx, ry), 0, 7); g.fill(); g.restore(); };
  // 미니언 그림은 칸 아래쪽 구석에 있어서, 위치를 칸 기준으로 옮겨 그려요
  const mini = (x, y, s, k, o2 = {}) => { const L = k % 2 === 0, x0 = L ? 9 : 42, x1 = L ? 22 : 56, cx = (x0 + x1) / 2; shadow(x, y, 7 * s / 2); drawSpr(9, x + (32 - cx) * s, y, s, { sx0: x0, sx1: x1, sy0: L ? 44 : 46, sy1: 64, ...o2 }); };
  // ---- 보스별 장면 ----
  const P = party, num = (v, x, y, c = '#fff6c0', sz = 12) => txt(v, x, y, c, sz);
  const bossNameTag = (nm, x, y) => txt(nm, x, y, '#f4ecff', 9);
  if (b === 0){
    if (sc === 'a'){   // 등껍질 방어 자세: 껍질 그림 + 초록 방패 기운 + 작은 숫자
      shadow(BX, BY, 52); await drawPeople();
      aura(BX, BY - 50, 86, 62, 'rgba(160,240,140,A)', .38); drawSpr(1, BX, BY, 2);
      g.save(); g.strokeStyle = 'rgba(200,255,170,.85)'; g.lineWidth = 2; g.beginPath(); g.ellipse(BX, BY - 46, 76, 54, 0, Math.PI * 1.02, Math.PI * 1.98); g.stroke(); g.globalAlpha = .5; g.beginPath(); g.ellipse(BX, BY - 46, 84, 62, 0, Math.PI * 1.05, Math.PI * 1.95); g.stroke();
      for (let k = 0; k < 7; k++){ const a = Math.PI * (1.1 + k * .13), x = BX + Math.cos(a) * 76, y = BY - 46 + Math.sin(a) * 54; g.globalAlpha = .9; g.fillStyle = '#e8ffd0'; g.beginPath(); for (let j = 0; j < 6; j++){ const aa = j * Math.PI / 3; g.lineTo(x + Math.cos(aa) * 4, y + Math.sin(aa) * 4); } g.fill(); } g.restore();
      [['-18', BX - 46, 120], ['-21', BX - 10, 104], ['-16', BX + 28, 116]].forEach(([v, x, y]) => num(v, x, y, '#c8d8c0', 10));
      txt('반만 들어가요', BX - 6, 88, '#9fe08a', 9);
      // 칼끝이 튕겨 나가는 불꽃
      [[BX - 70, 150], [BX - 64, 132]].forEach(([x, y]) => { g.fillStyle = '#fff6c0'; for (let k = 0; k < 5; k++){ const a = Math.PI * (.7 + k * .15); g.fillRect(x + Math.cos(a) * 6, y + Math.sin(a) * 6, 2, 2); } });
    }
    if (sc === 'b'){   // 껍질이 열렸어요: 서 있는 그림 · 빈틈 표시 · 큰 숫자
      shadow(BX, BY, 52); await drawPeople();
      drawSpr(0, BX, BY, 2);
      g.save(); g.strokeStyle = '#ff9a6a'; g.lineWidth = 2; g.setLineDash([4, 3]); g.beginPath(); g.arc(BX - 6, BY - 46, 22, 0, 7); g.stroke(); g.restore();
      g.strokeStyle = '#ff9a6a'; g.lineWidth = 2; [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(([dx, dy]) => { g.beginPath(); g.moveTo(BX - 6 + dx * 16, BY - 46 + dy * 16); g.lineTo(BX - 6 + dx * 28, BY - 46 + dy * 28); g.stroke(); });
      txt('빈틈', BX - 6, BY - 78, '#ff9a6a', 10);
      // 베기 · 마법 궤적
      g.save(); g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 3; g.beginPath(); g.arc(BX - 30, BY - 60, 34, -.4, 1.2); g.stroke(); g.strokeStyle = 'rgba(255,170,90,.9)'; g.lineWidth = 2; g.beginPath(); g.moveTo(P[2].x + 10, P[2].y - 26); g.quadraticCurveTo(160, 80, BX - 20, BY - 50); g.stroke(); g.restore();
      [['-142', BX - 34, 98, 16], ['-168', BX + 18, 82, 18], ['-121', BX - 66, 124, 15], ['-155', BX + 40, 120, 16]].forEach(([v, x, y, s]) => num(v, x, y, '#ffe07a', s));
      txt('약점', BX + 18, 64, '#ff9a6a', 9);
    }
    if (sc === 'c'){   // 지진 구르기: 등껍질로 빙글 구르며 다가와요 + 바닥에 굴러올 길 표시
      g.save(); const lg = g.createLinearGradient(BX, 0, 40, 0); lg.addColorStop(0, 'rgba(255,90,60,.0)'); lg.addColorStop(.2, 'rgba(255,90,60,.35)'); lg.addColorStop(1, 'rgba(255,90,60,.15)'); g.fillStyle = lg; g.fillRect(20, 128, BX - 40, 84); g.strokeStyle = 'rgba(255,140,100,.9)'; g.setLineDash([6, 4]); g.lineWidth = 2; g.strokeRect(20, 128, BX - 40, 84); g.restore();
      for (let k = 0; k < 3; k++){ g.fillStyle = 'rgba(255,170,130,.8)'; const x = 190 - k * 50; g.beginPath(); g.moveTo(x, 162); g.lineTo(x - 14, 170); g.lineTo(x, 178); g.fill(); }
      await drawPeople();
      shadow(BX, BY, 44); drawSpr(1, BX, BY - 4, 1.8, { rot: -.5 });
      g.strokeStyle = 'rgba(230,230,200,.7)'; g.lineWidth = 2; for (let k = 0; k < 4; k++){ g.beginPath(); g.arc(BX, BY - 56, 64 + k * 4, Math.PI * (.6 + k * .1), Math.PI * (1.1 + k * .1)); g.stroke(); }
      for (let i = 0; i < 14; i++){ g.fillStyle = i % 2 ? '#6a6a58' : '#8a8a70'; g.fillRect(BX - 50 + R() * 100, BY - 4 - R() * 26, 3 + R() * 4, 3); }
      g.strokeStyle = '#1a1024'; g.lineWidth = 2; for (let i = 0; i < 5; i++){ g.beginPath(); let x = BX - 20 - i * 10, y = BY + 2; g.moveTo(x, y); for (let k = 0; k < 3; k++){ x -= 8 + R() * 8; y += (R() - .5) * 8; g.lineTo(x, y); } g.stroke(); }
      edge('rgba(255,120,80,A)', .4); txt('3 초 뒤 굴러와요', 150, 120, '#ffb090', 11);
    }
  }
  if (b === 1){
    if (sc === 'a'){   // 한입 물기: 기사에게 덥석, 큰 빨간 숫자
      shadow(P[0].x + 66, P[0].y + 4, 40); drawSpr(3, P[0].x + 66, P[0].y + 10, 1.7); await drawPeople();
      g.save(); g.fillStyle = '#ffffff'; for (const d of [-1, 1]){ for (let k = 0; k < 4; k++){ const x = P[0].x - 10 + k * 7, y = P[0].y - 26 + d * 12; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 3, y - d * 9); g.lineTo(x + 6, y); g.fill(); } } g.restore();
      g.strokeStyle = 'rgba(255,60,40,.95)'; g.lineWidth = 3; for (let k = 0; k < 3; k++){ g.beginPath(); g.moveTo(P[0].x - 16 + k * 8, P[0].y - 40); g.lineTo(P[0].x - 6 + k * 8, P[0].y - 12); g.stroke(); }
      num('-312', P[0].x - 2, P[0].hy - 10, '#ff4a3a', 22); txt('아파요', P[0].x - 2, P[0].hy - 32, '#ffb0a0', 9);
      edge('rgba(255,40,30,A)', .35);
    }
    if (sc === 'b'){   // 물어뜯기 예고: 앞열 줄에 붉은 이빨 표시 · 피하기 원
      g.save(); g.fillStyle = 'rgba(255,40,30,.22)'; g.fillRect(70, 112, 70, 100); g.strokeStyle = 'rgba(255,80,60,.95)'; g.setLineDash([5, 3]); g.lineWidth = 2; g.strokeRect(70, 112, 70, 100); g.restore();
      await drawPeople();
      [P[0], P[1]].forEach(p => { g.fillStyle = 'rgba(255,60,40,.9)'; g.beginPath(); g.moveTo(p.x - 7, p.hy - 16); g.lineTo(p.x + 7, p.hy - 16); g.lineTo(p.x, p.hy - 6); g.fill(); txt('!', p.x, p.hy - 18, '#fff', 11); });
      shadow(BX + 6, BY, 50); aura(BX, BY - 40, 80, 50, 'rgba(255,40,30,A)', .45); drawSpr(3, BX + 6, BY, 2);
      g.save(); g.globalAlpha = .7; g.strokeStyle = '#ff5a4a'; g.lineWidth = 2; for (let k = 0; k < 3; k++){ g.beginPath(); g.ellipse(BX, BY - 46, 60 + k * 14, 40 + k * 10, 0, 0, 7); g.stroke(); } g.restore();
      for (let k = 0; k < 2; k++){ g.fillStyle = '#ff6a4a'; const x = 196 - k * 26; g.beginPath(); g.moveTo(x, 150); g.lineTo(x - 18, 160); g.lineTo(x, 170); g.fill(); }
      edge('rgba(255,60,30,A)', .5); txt('물어뜯기', BX, 40, '#ff5a4a', 14);
    }
    if (sc === 'c'){   // 포효: 붉은 기운 · 소리 고리 · 공격 오름
      await drawPeople(); shadow(BX, BY, 46);
      aura(BX, BY - 64, 100, 90, 'rgba(255,30,20,A)', .6);
      for (let i = 0; i < 9; i++){ const x = BX - 50 + i * 12 + (R() - .5) * 6, h = 30 + R() * 50; g.fillStyle = 'rgba(255,90,50,.55)'; g.beginPath(); g.moveTo(x - 5, BY - 6); g.quadraticCurveTo(x, BY - 6 - h * 1.3, x + 5, BY - 6); g.fill(); }
      drawSpr(2, BX, BY, 2, { tint: 'rgba(255,40,30,.18)' });
      g.save(); g.strokeStyle = 'rgba(255,200,180,.75)'; g.lineWidth = 2; for (let k = 0; k < 4; k++){ g.globalAlpha = .9 - k * .2; g.beginPath(); g.arc(BX - 18, BY - 106, 16 + k * 18, Math.PI * .55, Math.PI * 1.45); g.stroke(); } g.restore();
      g.fillStyle = '#ff2a1a'; g.fillRect(BX - 22, BY - 110, 3, 2); g.fillRect(BX - 13, BY - 110, 3, 2);
      txt('공격 +20 %', BX + 36, 40, '#ffb0a0', 12); txt('▲', BX + 82, 40, '#ff5a4a', 12);
      P.forEach(p => { g.fillStyle = 'rgba(255,90,60,.8)'; g.fillRect(p.x - 6, p.hy - 10, 2, 4); g.fillRect(p.x + 4, p.hy - 10, 2, 4); });
      txt('파티가 움찔해요', 80, 110, '#ffd0c0', 9);
      g.fillStyle = 'rgba(255,40,20,.12)'; g.fillRect(0, 0, W, H); edge('rgba(200,0,0,A)', .55);
    }
  }
  if (b === 2){
    const bubbles = (x, y, n, sz = 3) => { for (let k = 0; k < n; k++){ const bx = x + (R() - .5) * 22, by = y - R() * 30, r = 1 + R() * sz; g.fillStyle = 'rgba(150,255,100,.75)'; g.beginPath(); g.arc(bx, by, r, 0, 7); g.fill(); g.fillStyle = 'rgba(230,255,210,.9)'; g.fillRect(bx - r * .4, by - r * .5, 1, 1); } };
    const stack = (p, n) => { const x = p.x + 14, y = p.hy - 4; g.fillStyle = '#1a1024'; g.beginPath(); g.arc(x, y, 7, 0, 7); g.fill(); g.fillStyle = '#5ad03a'; g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); g.fillStyle = '#c8ff9a'; g.fillRect(x - 3, y - 4, 2, 2); txt(String(n), x, y + 4, '#ffffff', 10); };
    if (sc === 'a'){   // 독이 쌓여요: 초록 거품 · 머리 위 겹 수 · 똑똑 초록 숫자
      shadow(BX, BY, 40); await drawPeople(); drawSpr(4, BX, BY, 2);
      g.strokeStyle = 'rgba(150,255,100,.6)'; g.lineWidth = 2; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(BX - 40, BY - 70); g.quadraticCurveTo(170, 60, P[0].x + 10, P[0].y - 30); g.stroke(); g.setLineDash([]);
      [3, 2, 1, 2].forEach((n, i) => { bubbles(P[i].x, P[i].y - 6, 4 + n * 3); stack(P[i], n); });
      [['-9', 0, -14], ['-9', 0, -28], ['-6', 1, -16], ['-3', 2, -14], ['-6', 3, -16]].forEach(([v, i, dy], k) => num(v, P[i].x - 6 + (k % 2) * 4, P[i].hy + dy, '#8aff5a', 11));
    }
    if (sc === 'b'){   // 독 안개: 온 바닥에 초록 안개 · 해골 거품
      shadow(BX, BY, 40); await drawPeople(); drawSpr(5, BX, BY, 2);
      for (let i = 0; i < 16; i++){ const y = 110 + i * 7 + Math.sin(i) * 5; const lg = g.createLinearGradient(0, y - 20, 0, y + 20); lg.addColorStop(0, 'rgba(110,220,70,0)'); lg.addColorStop(.5, 'rgba(110,220,70,.2)'); lg.addColorStop(1, 'rgba(110,220,70,0)'); g.fillStyle = lg; g.fillRect(0, y - 20, W, 40); }
      for (let i = 0; i < 26; i++){ const x = R() * W, y = 120 + R() * 90, r = 8 + R() * 14; g.fillStyle = `rgba(${i % 3 ? '140,230,90' : '170,110,220'},.16)`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
      for (let i = 0; i < 6; i++){ const x = 30 + i * 62 + R() * 10, y = 130 + R() * 70; g.fillStyle = 'rgba(210,255,190,.85)'; g.beginPath(); g.arc(x, y, 5, Math.PI, 0); g.lineTo(x + 5, y + 6); g.lineTo(x - 5, y + 6); g.fill(); g.fillStyle = '#2a4020'; g.fillRect(x - 3, y - 2, 2, 2); g.fillRect(x + 1, y - 2, 2, 2); }
      P.forEach((p, i) => { stack(p, [4, 4, 3, 3][i]); num(['-14', '-14', '-11', '-11'][i], p.x - 4, p.hy - 14, '#8aff5a', 11); });
      g.fillStyle = 'rgba(80,180,50,.14)'; g.fillRect(0, 0, W, H); edge('rgba(60,160,40,A)', .55); txt('독 안개', BX, 36, '#9cff6a', 14);
    }
    if (sc === 'c'){   // 정화: 성직자에게서 빛이 퍼지며 독 거품이 흩어져요
      shadow(BX, BY, 40); await drawPeople(); drawSpr(4, BX, BY, 2, { a: .95 });
      const cx = P[3].x, cy = P[3].y - 24;
      aura(cx + 30, cy - 10, 110, 70, 'rgba(255,245,180,A)', .45);
      g.save(); g.strokeStyle = 'rgba(255,248,200,.9)'; g.lineWidth = 2; for (let k = 0; k < 3; k++){ g.globalAlpha = .9 - k * .25; g.beginPath(); g.ellipse(cx + 20, cy + 22, 40 + k * 26, 12 + k * 8, 0, 0, 7); g.stroke(); } g.restore();
      for (let i = 0; i < 26; i++){ const a = R() * Math.PI * 2, r = 30 + R() * 70, x = cx + 30 + Math.cos(a) * r, y = cy - 10 + Math.sin(a) * r * .6; g.fillStyle = '#fff6c0'; g.fillRect(x, y, 2, 2); if (i % 3 === 0){ g.fillRect(x - 2, y, 6, 1); g.fillRect(x + 1, y - 3, 1, 7); } }
      P.forEach((p, i) => { for (let k = 0; k < 3; k++){ const x = p.x - 10 + k * 9 + (R() - .5) * 4, y = p.hy - 8 - k * 5; g.strokeStyle = 'rgba(150,255,100,.45)'; g.lineWidth = 1; g.beginPath(); g.arc(x, y, 2 + k, 0, 7); g.stroke(); } num(['+48', '+52', '+40', '+44'][i], p.x - 2, p.hy - 14, '#7affb0', 11); });
      txt('독 0 겹', P[0].x + 8, P[0].hy - 28, '#fff2a0', 9);
      for (let k = 0; k < 6; k++){ g.fillStyle = 'rgba(255,250,210,.5)'; g.fillRect(cx - 2 + (k - 3) * 6, 0, 2, cy - 10); }
    }
  }
  if (b === 3){
    const LX = 232, RX = 318, sh2 = (x, c1, c2) => { const rg = g.createRadialGradient(x, BY - 34, 8, x, BY - 34, 46); rg.addColorStop(0, c1); rg.addColorStop(.8, c2); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.beginPath(); g.ellipse(x, BY - 36, 40, 50, 0, 0, 7); g.fill(); };
    const bar2 = (x, y, v, c) => { const bw = 46, bx = x - bw / 2; g.fillStyle = '#1a1024'; g.fillRect(bx - 1, y - 1, bw + 2, 7); g.fillStyle = '#4a2a3a'; g.fillRect(bx, y, bw, 5); g.fillStyle = c; g.fillRect(bx, y, Math.round(bw * v / 100), 5); };
    if (sc === 'a'){   // 둘이 나란히, 체력 바 두 개
      await drawPeople(); shadow(LX, BY, 30); shadow(RX, BY, 30);
      drawSpr(6, LX + 22, BY, 2, { sx0: 0, sx1: 32 }); drawSpr(6, RX - 42, BY, 2, { sx0: 32, sx1: 64 });
      bossNameTag('낮', LX, 82); bossNameTag('밤', RX, 82); bar2(LX, 88, 68, '#ffffff'); bar2(RX, 88, 61, '#a89ae0');
      [['-64', LX - 12, 112], ['-58', RX + 14, 116]].forEach(([v, x, y]) => num(v, x, y, '#fff6c0', 12));
      g.strokeStyle = 'rgba(255,255,255,.5)'; g.setLineDash([2, 3]); g.lineWidth = 1; g.beginPath(); g.moveTo(LX + 26, 92); g.lineTo(RX - 26, 92); g.stroke(); g.setLineDash([]); txt('7 % 차이', (LX + RX) / 2, 104, '#cbbbe8', 9);
    }
    if (sc === 'b'){   // 서로 보호막: 낮은 밤에게 빛 막, 밤은 낮에게 그림자 막 + 끊기 게이지
      await drawPeople(); shadow(LX, BY, 30); shadow(RX, BY, 30);
      drawSpr(6, LX + 22, BY, 2, { sx0: 0, sx1: 32 }); drawSpr(6, RX - 42, BY, 2, { sx0: 32, sx1: 64 });
      sh2(LX, 'rgba(60,40,120,.05)', 'rgba(60,40,120,.55)'); sh2(RX, 'rgba(255,250,220,.05)', 'rgba(255,250,220,.5)');
      g.lineWidth = 2; g.strokeStyle = '#3a2e6a'; g.beginPath(); g.ellipse(LX, BY - 36, 40, 50, 0, 0, 7); g.stroke(); g.strokeStyle = '#fff8e0'; g.beginPath(); g.ellipse(RX, BY - 36, 40, 50, 0, 0, 7); g.stroke();
      g.save(); g.lineWidth = 3; g.strokeStyle = 'rgba(255,250,220,.9)'; g.beginPath(); g.moveTo(LX + 10, BY - 70); g.quadraticCurveTo((LX + RX) / 2, BY - 120, RX - 6, BY - 80); g.stroke(); g.strokeStyle = 'rgba(80,60,160,.95)'; g.beginPath(); g.moveTo(RX - 10, BY - 60); g.quadraticCurveTo((LX + RX) / 2, BY - 20, LX + 6, BY - 54); g.stroke(); g.restore();
      const gw = 120, gx = (LX + RX) / 2 - gw / 2, gy = 30; g.fillStyle = '#1a1024'; g.fillRect(gx - 2, gy - 2, gw + 4, 11); g.fillStyle = '#3a2440'; g.fillRect(gx, gy, gw, 7); g.fillStyle = '#fff6c0'; g.fillRect(gx, gy, gw * .58, 7); g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(gx, gy, gw * .58, 2); for (let k = 1; k < 4; k++){ g.fillStyle = '#1a1024'; g.fillRect(gx + gw * k / 4, gy, 1, 7); }
      txt('끊기 58 %', (LX + RX) / 2, gy - 4, '#fff6c0', 10);
      [['막힘', LX - 18, 120], ['막힘', RX + 18, 118]].forEach(([v, x, y]) => txt(v, x, y, '#b8b0d0', 10));
      g.strokeStyle = '#ffd24a'; g.lineWidth = 2; g.beginPath(); g.moveTo(P[1].x + 14, P[1].y - 20); g.lineTo((LX + RX) / 2 - 4, BY - 46); g.stroke(); txt('끊기 +14 %', 168, 160, '#ffd24a', 9);
    }
    if (sc === 'c'){   // 낮이 쓰러짐 · 밤이 화가 남
      await drawPeople(); shadow(LX, BY, 30);
      drawSpr(6, LX + 40, BY - 46, 2, { sx0: 0, sx1: 32, gray: 1, a: .9, rot: -Math.PI / 2 });
      for (let i = 0; i < 8; i++){ g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(LX - 30 + R() * 60, BY - 30 - R() * 40, 2, 2); }
      shadow(RX, BY, 34); aura(RX, BY - 46, 70, 80, 'rgba(255,40,140,A)', .55);
      for (let i = 0; i < 8; i++){ const x = RX - 30 + i * 9, h = 30 + R() * 40; g.fillStyle = 'rgba(140,40,200,.55)'; g.beginPath(); g.moveTo(x - 5, BY - 4); g.quadraticCurveTo(x, BY - 4 - h * 1.4, x + 5, BY - 4); g.fill(); }
      drawSpr(6, RX - 42 - 8, BY, 2.3, { sx0: 32, sx1: 64, tint: 'rgba(255,40,120,.15)' });
      g.fillStyle = '#ff3a6a'; g.fillRect(RX - 6, BY - 116, 4, 2); g.fillRect(RX + 4, BY - 116, 4, 2);
      bossNameTag('밤', RX - 66, 74); bar2(RX - 66, 80, 38, '#a89ae0'); txt('공격 +50 %', RX - 66, 60, '#ff9ad0', 12);
      txt('쓰러졌어요', LX - 4, 150, '#b8b0d0', 9);
      g.fillStyle = 'rgba(120,20,80,.12)'; g.fillRect(W / 2, 0, W / 2, H); edge('rgba(160,30,120,A)', .45);
      num('-186', P[0].x, P[0].hy - 10, '#ff4a7a', 18);
      g.strokeStyle = 'rgba(200,60,220,.85)'; g.lineWidth = 3; g.beginPath(); g.moveTo(RX - 30, BY - 60); g.quadraticCurveTo(200, 90, P[0].x + 12, P[0].y - 26); g.stroke();
    }
  }
  if (b === 4){
    if (sc === 'a'){   // 졸개를 불러요: 태엽 감기 + 김 뿜으며 졸개 둘 등장
      await drawPeople(); shadow(BX + 20, BY, 34);
      drawSpr(9, BX + 20, BY, 2, { sy1: 44 });   // 기술 프레임에서 졸개 부분은 빼고 본체만
      drawSpr(9, BX + 20, BY, 2, { sx0: 22, sx1: 42, sy0: 44, sy1: 64 });
      [[196, 168, 0], [210, 206, 1]].forEach(([x, y, k], i) => { for (let j = 0; j < 7; j++){ g.fillStyle = `rgba(240,240,230,${.25 + R() * .3})`; g.beginPath(); g.arc(x + (R() - .5) * 26, y - 4 - R() * 18, 4 + R() * 6, 0, 7); g.fill(); } mini(x, y, 2.5, k); txt('째깍', x, y - 44, '#ffe0a0', 9); });
      g.strokeStyle = 'rgba(255,220,140,.8)'; g.lineWidth = 2; for (let k = 0; k < 3; k++){ g.beginPath(); g.arc(BX + 30, BY - 104, 10 + k * 7, -.8, 1.4); g.stroke(); }
      txt('빨라요', BX + 54, 40, '#ffc84a', 11); for (let k = 0; k < 3; k++){ g.fillStyle = 'rgba(255,200,80,.7)'; g.fillRect(BX + 44 - k * 10, 60 + k * 6, 10 - k * 2, 2); }
      txt('졸개 2', 150, 128, '#e8d0a0', 10);
    }
    if (sc === 'b'){   // 졸개 3 · 폭주 경고
      await drawPeople(); shadow(BX + 30, BY, 34);
      aura(BX + 30, BY - 50, 60, 70, 'rgba(255,100,40,A)', .45); drawSpr(8, BX + 30, BY, 2, { tint: 'rgba(255,80,40,.12)' });
      [[176, 152, 0], [200, 190, 1], [222, 214, 0]].forEach(([x, y, k]) => { mini(x, y, 2.5, k); g.fillStyle = '#ff6a3a'; g.fillRect(x - 1, y - 44, 3, 3); });
      // 4 번째 자리: 점선 실루엣 + 경고
      g.save(); g.strokeStyle = '#ff6a3a'; g.setLineDash([3, 3]); g.lineWidth = 2; g.strokeRect(232, 136, 24, 30); g.restore(); txt('4', 244, 158, '#ff6a3a', 12);
      const bw = 110, bx = BX + 30 - bw / 2; g.fillStyle = '#1a1024'; g.fillRect(bx - 2, 22, bw + 4, 22); g.fillStyle = '#5a1810'; g.fillRect(bx, 24, bw, 18); g.fillStyle = '#ff6a3a'; for (let k = 0; k < bw; k += 10){ g.fillRect(bx + k, 24, 5, 2); g.fillRect(bx + k + 5, 40, 5, 2); }
      txt('졸개 3 / 3', BX + 30, 38, '#ffd0a0', 12); txt('폭주 직전', BX + 30, 60, '#ff6a3a', 13);
      for (let i = 0; i < 6; i++){ g.fillStyle = `rgba(240,230,220,${.3 + R() * .3})`; g.beginPath(); g.arc(BX + 10 + R() * 40, BY - 110 - R() * 20, 4 + R() * 5, 0, 7); g.fill(); }
      edge('rgba(255,90,30,A)', .5);
    }
    if (sc === 'c'){   // 광역으로 졸개 정리: 불꽃 폭풍 + 부서지는 톱니
      await drawPeople(); shadow(BX + 30, BY, 34); drawSpr(8, BX + 30, BY, 2);
      const cx = 200, cy = 184; for (let k = 0; k < 3; k++){ g.strokeStyle = `rgba(255,${180 - k * 50},60,${.9 - k * .2})`; g.lineWidth = 4 - k; g.beginPath(); g.ellipse(cx, cy, 40 + k * 16, 16 + k * 6, 0, 0, 7); g.stroke(); }
      for (let i = 0; i < 140; i++){ const a = R() * Math.PI * 2, r = R() * 56, x = cx + Math.cos(a) * r, y = cy - 10 + Math.sin(a) * r * .55 - R() * 30; const c = r < 18 ? '#fff6c0' : r < 34 ? '#ffc040' : r < 46 ? '#ff7a2a' : '#d83a20'; g.globalAlpha = .45 + R() * .45; g.fillStyle = c; g.beginPath(); g.arc(x, y, 1.5 + R() * 3.5, 0, 7); g.fill(); } g.globalAlpha = 1;
      [[176, 160, 0], [200, 196, 1], [226, 176, 0]].forEach(([x, y, k], i) => { mini(x + (i - 1) * 6, y, 2, k, { a: .45, rot: (i - 1) * .7, tint: 'rgba(40,20,10,.35)' }); for (let j = 0; j < 4; j++){ g.save(); g.translate(x + (R() - .5) * 36, y - 20 - R() * 30); g.rotate(R() * 6); g.fillStyle = '#c8a050'; g.beginPath(); for (let m = 0; m < 12; m++){ const aa = m / 12 * Math.PI * 2, rr = m % 2 ? 3 : 4.5; g.lineTo(Math.cos(aa) * rr, Math.sin(aa) * rr); } g.fill(); g.restore(); } num(['-96', '-102', '-88'][i], x, y - 46 - (i % 2) * 10, '#ffb04a', 12); });
      num('-64', BX + 30, 92, '#fff6c0', 12);
      g.strokeStyle = 'rgba(255,170,90,.9)'; g.lineWidth = 2; g.beginPath(); g.moveTo(P[2].x + 16, P[2].y - 30); g.quadraticCurveTo(110, 70, cx, cy - 40); g.stroke();
      txt('졸개 0', 150, 108, '#9fe08a', 11);
    }
  }
  return 1;
};
