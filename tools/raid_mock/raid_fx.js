// 레이드 스킬 이펙트 시안: 모의 사이트 index.html 끝에 붙여서 window.__raidFx({ b: 0~3, sc: 'tele' | 'side' | 'all' | 'big', t: 0~1 }) 로 장면을 그려요
//   보스 그림: art/raid_bosses.png (LPC 64 칸 × 2 동작 × 4 종, tools/iso/lpc/raid_boss_lpc.py)
window.__raidFx = async (o) => {
  const A = World.Avatar, W = 480, H = 270, b = o.b || 0, sc = o.sc || 'tele', T = o.t ?? .5;
  const BS = [
    { n: '얼음 거인', c: '#7FE6FF', side: '눈보라', all: '얼음 비', big: '빙하 내려찍기', warnA: '얼음 거인이 숨을 크게 들이마셔요....', warnS: '얼음 거인이 오른쪽을 노려봐요....', sky: ['#1c2a4a', '#3a5a86'], gr: ['#cfe6f6', '#8fb4d8'] },
    { n: '불꽃 용', c: '#FF8A3A', side: '불꽃 숨결', all: '불비', big: '화산 포효', warnA: '불꽃 용이 날개를 활짝 펼쳐요....', warnS: '불꽃 용의 목이 붉게 달아올라요....', sky: ['#2a0a10', '#7a2416'], gr: ['#6a3420', '#3a1a12'] },
    { n: '그림자 마녀', c: '#C08AFF', side: '그림자 손', all: '저주 안개', big: '분신 셋', warnA: '그림자 마녀가 주문을 길게 외워요....', warnS: '발밑 그림자가 꿈틀거려요....', sky: ['#100820', '#3a1a4a'], gr: ['#3a2a4a', '#1e1428'] },
    { n: '시계탑 골렘', c: '#FFD24A', side: '톱니 날', all: '시간 멈춤', big: '되감기', warnA: '시계 소리가 점점 커져요.... 째깍, 째깍', warnS: '어깨 톱니가 빠르게 돌아요....', sky: ['#20160c', '#6a4a22'], gr: ['#a08050', '#6a5030'] }][b];
  document.getElementById('raidov')?.remove();
  const ov = document.createElement('div'); ov.id = 'raidov';
  const hpPct = { tele: 63, side: 58, all: 47, big: 21 }[sc], ph = sc === 'big' ? 3 : sc === 'all' ? 2 : 2;
  const log = { tele: '', side: `${BS.n}의 <b style="color:${BS.c}">${BS.side}</b>! 뒤쪽 파티 · 하랑 「완벽하게 피했어요」`, all: `${BS.n}의 <b style="color:${BS.c}">${BS.all}</b>! 12 명 모두 · 나 「조금 늦었어요」 피해 60 %`, big: `3 단계 · ${BS.n}의 <b style="color:${BS.c}">${BS.big}</b>! 끊기에 실패했어요....` }[sc];
  ov.innerHTML = `<style>
#raidov{position:fixed;inset:0;z-index:99999;background:#140e22;color:#f4ecff;font-family:G11,Pretendard,sans-serif;display:flex;flex-direction:column;gap:6px;padding:10px 8px}#raidov>*{flex:none}
#raidov .rtop{display:flex;align-items:center;gap:8px;font-family:G11B,Pretendard,sans-serif;font-size:13px}
#raidov .bar{flex:1;height:14px;background:#2a1838;border:2px solid #1a1024;border-radius:3px;position:relative;overflow:hidden}
#raidov .bar i{position:absolute;inset:0;width:${hpPct}%;background:linear-gradient(#ffe07a,#f0a43a)}
#raidov .bar u{position:absolute;top:0;bottom:0;left:${hpPct}%;width:${sc === 'big' && b === 3 ? 9 : 0}%;background:repeating-linear-gradient(90deg,#fff6c0 0 3px,#d8a840 3px 6px);opacity:.85}
#raidov .bar b{position:absolute;inset:0;text-align:center;font-size:10px;line-height:14px;color:#1a1024}
#raidov canvas{width:100%;image-rendering:pixelated;border:2px solid #2a1838;border-radius:4px}
#raidov .log{font-size:10px;color:#cbbbe8;background:#1c1430;border-radius:6px;padding:5px 7px}
#raidov .dodge{display:flex;align-items:center;gap:12px;background:#22183a;border:2px solid ${BS.c};border-radius:8px;padding:10px}
#raidov .ring{position:relative;width:96px;height:96px;flex:none}
#raidov .ring .o{position:absolute;inset:${Math.round(2 + T * 14)}px;border:4px solid ${BS.c};border-radius:50%;opacity:.9}
#raidov .ring .z{position:absolute;inset:24px;border:4px solid #fff;border-radius:50%;box-shadow:0 0 10px ${BS.c}}
#raidov .ring .btn{position:absolute;inset:29px;border-radius:50%;background:#3a2a5a;display:flex;align-items:center;justify-content:center;font-family:G11B;font-size:12px;white-space:nowrap;color:#fff}
#raidov .dodge p{margin:0;font-size:12px;line-height:1.6}
#raidov .dodge small{color:#b9a8d8;font-size:10px}
</style>
<div class="rtop">${BS.n}<div class="bar"><i></i><u></u><b>${hpPct} %</b></div><span style="color:#9fd8ff">${ph} 단계</span></div>
<canvas id="rcv" width="${W}" height="${H}"></canvas>
${log ? `<div class="log">${log}</div>` : ''}
${sc === 'tele' ? `<div class="dodge"><div class="ring"><div class="o"></div><div class="z"></div><div class="btn">피하기</div></div><p><b>${BS.warnA}</b></p></div>` : ''}`;
  document.body.appendChild(ov);
  const cv = ov.querySelector('#rcv'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
  const R = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(7 + b * 31 + sc.length);
  // ---- 배경 ----
  const sky = g.createLinearGradient(0, 0, 0, 130); sky.addColorStop(0, BS.sky[0]); sky.addColorStop(1, BS.sky[1]); g.fillStyle = sky; g.fillRect(0, 0, W, 130);
  const gr = g.createLinearGradient(0, 130, 0, H); gr.addColorStop(0, BS.gr[0]); gr.addColorStop(1, BS.gr[1]); g.fillStyle = gr; g.fillRect(0, 130, W, H - 130);
  if (b === 0){ for (let i = 0; i < 14; i++){ const x = i * 37 + (i % 3) * 7, h = 40 + (i * 53 % 50); g.fillStyle = i % 2 ? '#5a82b4' : '#6e98c8'; g.beginPath(); g.moveTo(x, 130); g.lineTo(x + 14, 130 - h); g.lineTo(x + 28, 130); g.fill(); } g.fillStyle = 'rgba(255,255,255,.5)'; for (let i = 0; i < 60; i++) g.fillRect((i * 97) % W, (i * 53) % 110, 1, 1); }
  if (b === 1){ [[60, 70], [190, 95], [330, 60], [440, 85]].forEach(([x, h]) => { g.fillStyle = '#3a1410'; g.beginPath(); g.moveTo(x - 60, 130); g.lineTo(x - 10, 130 - h); g.lineTo(x + 10, 130 - h); g.lineTo(x + 60, 130); g.fill(); g.fillStyle = '#ff7a2a'; g.fillRect(x - 8, 130 - h, 16, 3); }); g.strokeStyle = '#ff8a3a'; g.lineWidth = 2; for (let i = 0; i < 9; i++){ g.beginPath(); let x = R() * W, y = 140 + R() * 120; g.moveTo(x, y); for (let k = 0; k < 4; k++){ x += 10 + R() * 14; y += (R() - .5) * 10; g.lineTo(x, y); } g.stroke(); } }
  if (b === 2){ g.fillStyle = '#1e1030'; for (let i = 0; i < 12; i++){ const x = i * 42 + 10, h = 40 + (i * 29 % 40); g.beginPath(); g.moveTo(x - 18, 0); g.lineTo(x, h); g.lineTo(x + 18, 0); g.fill(); g.fillRect(x - 1, 0, 3, h + 14); } g.fillStyle = 'rgba(200,150,255,.6)'; for (let i = 0; i < 40; i++) g.fillRect((i * 83) % W, 20 + (i * 47) % 100, 1, 1); }
  if (b === 3){ const gearS = (cx, cy, r, c) => { g.fillStyle = c; g.beginPath(); for (let k = 0; k < 24; k++){ const a = k / 24 * Math.PI * 2, rr = k % 2 ? r : r * 1.18; g.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } g.fill(); g.fillStyle = BS.sky[1]; g.beginPath(); g.arc(cx, cy, r * .45, 0, 7); g.fill(); }; gearS(70, 60, 34, '#4a3418'); gearS(400, 50, 44, '#4a3418'); gearS(250, 100, 22, '#5a4020'); for (let x = 0; x < W; x += 24) for (let y = 136; y < H; y += 12){ g.fillStyle = ((x / 24 + y / 12) % 2) ? 'rgba(0,0,0,.08)' : 'rgba(255,255,255,.05)'; g.fillRect(x + ((y / 12) % 2) * 12, y, 24, 12); } }
  // ---- 사람 12 ----
  const jobs = ['knight', 'warrior', 'thief', 'white', 'black', 'bard', 'knight', 'warrior', 'summon', 'alch', 'druid', 'time'], FW = A.FW, FH = A.FH, dirL = A.meta.dirs.left;
  const pos = []; for (let i = 0; i < 12; i++){ const side = i >= 6 ? 1 : 0, j = i % 6, front = j < 3, k = j % 3, xo = (front ? 160 : 80) + (k - 1) * -16; pos.push({ i, side, x: side ? W - xo : xo, y: 168 + k * 34 }); }
  const hit = p => sc === 'all' || sc === 'big' || (sc === 'side' && p.side === 1);
  const tmp = document.createElement('canvas'); tmp.width = FW; tmp.height = FH; const tq = tmp.getContext('2d');
  const drawPeople = async () => { for (const p of pos.slice().sort((a, b) => a.y - b.y)){
    const av = A.fromLook(ORDER_J.indexOf(jobs[p.i]) * 131 + 7 + p.i * 3); try { await A.need(av); } catch (e) {} const sp = A.compose(av); if (!sp) continue;
    tq.clearRect(0, 0, FW, FH); tq.globalCompositeOperation = 'source-over'; tq.drawImage(sp, dirL * FW, 0, FW, FH, 0, 0, FW, FH);
    const h = hit(p);
    if (h && b === 0 && sc === 'side'){ tq.globalCompositeOperation = 'source-atop'; tq.fillStyle = 'rgba(150,220,255,.55)'; tq.fillRect(0, 0, FW, FH); }     // 얼어붙음
    if (h && b === 1){ tq.globalCompositeOperation = 'source-atop'; tq.fillStyle = 'rgba(255,90,30,.35)'; tq.fillRect(0, 0, FW, FH); }
    if (b === 3 && sc === 'all'){ const d = tq.getImageData(0, 0, FW, FH); for (let k = 0; k < d.data.length; k += 4){ const v = (d.data[k] + d.data[k + 1] + d.data[k + 2]) / 3; d.data[k] = v * 1.05 + 20; d.data[k + 1] = v * .95 + 12; d.data[k + 2] = v * .7; } tq.putImageData(d, 0, 0); }   // 시간이 멈춰 빛바랜 색
    const s = .8, w = FW * s, hh = FH * s; g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(p.x, p.y, 11, 3, 0, 0, 7); g.fill();
    const dodge = sc === 'side' && p.i === 8 || sc === 'all' && p.i === 3; const dx = dodge ? (p.side ? 10 : -10) : 0;
    g.save(); g.translate(p.x + dx, 0); if (!p.side) g.scale(-1, 1); if (dodge) g.globalAlpha = .55; g.drawImage(tmp, -w / 2, p.y - hh + 5, w, hh); g.restore();
    if (dodge){ g.save(); g.translate(p.x, 0); if (!p.side) g.scale(-1, 1); g.globalAlpha = .25; g.drawImage(tmp, -w / 2, p.y - hh + 5, w, hh); g.restore(); }   // 피한 잔상
    const bw = 24, bx = Math.round(p.x - bw / 2), by = Math.round(p.y - hh + 4), f = [78, 90, 64, 78, 40, 82, 70, 95, 22, 77, 88, 58][p.i] / 100 * (h && !dodge ? .7 : 1);
    g.fillStyle = '#1a1024'; g.fillRect(bx - 1, by - 1, bw + 2, 5); g.fillStyle = '#4a2a3a'; g.fillRect(bx, by, bw, 3); g.fillStyle = f > .3 ? '#7affb0' : '#ff6a4a'; g.fillRect(bx, by, Math.round(bw * f), 3);
    if (dodge){ g.font = '9px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; g.lineWidth = 3; g.strokeStyle = '#1a1024'; const t = sc === 'side' ? '완벽!' : '조금 늦음'; g.strokeText(t, p.x, by - 4); g.fillStyle = sc === 'side' ? '#7affb0' : '#ffe07a'; g.fillText(t, p.x, by - 4); }
  } };
  // ---- 보스 ----
  const bim = await new Promise(r => { const im = new Image(); im.onload = () => r(im); im.src = 'art/raid_bosses.png?v=' + Date.now(); });
  const cast = sc !== 'side' && sc !== 'all' ? 1 : 1, BX = W / 2, BY = 216, BW = 160;
  const drawBoss = (x, y, a = 1, fr = cast) => { g.save(); g.globalAlpha = a; g.drawImage(bim, (b * 2 + fr) * 64, 0, 64, 64, x - BW / 2, y - BW + 6, BW, BW); g.restore(); };
  g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.ellipse(BX, BY, 40, 9, 0, 0, 7); g.fill();
  if (sc === 'big' && b === 2){ drawBoss(BX - 92, BY - 6, .45, 0); drawBoss(BX + 92, BY - 6, .45, 0); }   // 분신
  // 큰 기술 · 예고 때 머리 위 끊기 게이지
  const gauge = (v, lbl) => { const w = 120, x = BX - w / 2, y = 22; g.fillStyle = '#1a1024'; g.fillRect(x - 2, y - 2, w + 4, 11); g.fillStyle = '#3a2440'; g.fillRect(x, y, w, 7); g.fillStyle = '#fff6c0'; g.fillRect(x, y, w * v, 7); g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(x, y, w * v, 2); for (let k = 1; k < 4; k++){ g.fillStyle = '#1a1024'; g.fillRect(x + w * k / 4, y, 1, 7); } g.font = '9px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText(lbl, BX, y - 4); g.fillStyle = '#fff6c0'; g.fillText(lbl, BX, y - 4); };
  // ---- 이펙트 ----
  const fxBefore = () => {
    if (sc === 'big' && b === 1){ for (let i = 0; i < 7; i++){ const x = 40 + i * 66 + (R() - .5) * 20, h = 90 + R() * 60; const lg = g.createLinearGradient(0, BY + 20 - h, 0, BY + 20); lg.addColorStop(0, 'rgba(255,240,160,0)'); lg.addColorStop(.3, 'rgba(255,150,40,.85)'); lg.addColorStop(1, 'rgba(200,40,20,.95)'); g.fillStyle = lg; g.beginPath(); g.moveTo(x - 14, BY + 30); g.quadraticCurveTo(x, BY + 20 - h * 1.2, x + 14, BY + 30); g.fill(); } }
    if (sc === 'side' && b === 2){ pos.filter(p => p.side).forEach(p => { g.fillStyle = 'rgba(20,6,34,.9)'; g.beginPath(); g.ellipse(p.x, p.y + 1, 16, 5, 0, 0, 7); g.fill(); }); }
  };
  const fxAfter = () => {
    const edge = (c, a) => { const e = g.createRadialGradient(W / 2, H / 2, 120, W / 2, H / 2, 300); e.addColorStop(0, 'rgba(0,0,0,0)'); e.addColorStop(1, c.replace('A', a)); g.fillStyle = e; g.fillRect(0, 0, W, H); };
    if (sc === 'tele'){
      edge(['rgba(120,220,255,A)', 'rgba(255,120,40,A)', 'rgba(190,120,255,A)', 'rgba(255,210,80,A)'][b], .55);
      [[-1], [1]].forEach(([d]) => { g.fillStyle = '#ff6a4a'; g.globalAlpha = .9; const x = BX + d * 80; g.beginPath(); g.moveTo(x, 70); g.lineTo(x + d * 24, 82); g.lineTo(x, 94); g.fill(); g.globalAlpha = 1; });
      gauge(.62, '끊기 62 %'); g.save(); g.globalAlpha = .55; g.strokeStyle = BS.c; g.lineWidth = 2; for (let k = 0; k < 3; k++){ g.beginPath(); g.ellipse(BX, BY - 90, 60 + k * 16, 70 + k * 16, 0, 0, 7); g.stroke(); } g.restore();
      g.font = '12px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; [['-38', BX - 30, 110], ['-41', BX + 26, 128], ['-52', BX - 6, 96]].forEach(([t, x, y]) => { g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText(t, x, y); g.fillStyle = '#fff6c0'; g.fillText(t, x, y); });
    }
    if (b === 0 && sc === 'side'){   // 눈보라: 보스에서 오른쪽으로 흰 바람 · 눈송이 · 얼음 조각
      for (let i = 0; i < 70; i++){ const y = 90 + R() * 150, x = BX + 30 + R() * 230, l = 8 + R() * 18; g.strokeStyle = `rgba(230,248,255,${.35 + R() * .5})`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x + l, y + l * .18); g.stroke(); }
      for (let i = 0; i < 50; i++){ g.fillStyle = '#ffffff'; const x = BX + 30 + R() * 230, y = 80 + R() * 170; g.fillRect(x, y, 2, 2); }
      pos.filter(p => p.side).forEach(p => { if (p.i === 8) return; g.fillStyle = 'rgba(190,240,255,.75)'; g.strokeStyle = '#eaf8ff'; g.lineWidth = 1; g.beginPath(); g.moveTo(p.x - 12, p.y + 2); g.lineTo(p.x - 9, p.y - 20); g.lineTo(p.x, p.y - 26); g.lineTo(p.x + 10, p.y - 18); g.lineTo(p.x + 12, p.y + 2); g.closePath(); g.fill(); g.stroke(); });
    }
    if (b === 0 && sc === 'all'){ edge('rgba(120,220,255,A)', .5); for (let i = 0; i < 46; i++){ const x = R() * W, y = R() * 230, l = 14 + R() * 10; g.save(); g.translate(x, y); g.rotate(.35); g.fillStyle = 'rgba(200,240,255,.9)'; g.beginPath(); g.moveTo(0, -l); g.lineTo(3, 0); g.lineTo(0, 4); g.lineTo(-3, 0); g.fill(); g.fillStyle = '#fff'; g.fillRect(-1, -l + 3, 1, l - 4); g.restore(); } }
    if (b === 0 && sc === 'big'){ const x = BX, top = 0; const lg = g.createLinearGradient(x - 40, 0, x + 40, 0); lg.addColorStop(0, '#8ac4ee'); lg.addColorStop(.4, '#e8f8ff'); lg.addColorStop(1, '#5a96d0'); g.fillStyle = 'rgba(255,255,255,.35)'; g.fillRect(0, 0, W, H); g.fillStyle = lg; g.beginPath(); g.moveTo(x - 34, top); g.lineTo(x + 34, top); g.lineTo(x + 26, BY - 40); g.lineTo(x, BY - 10); g.lineTo(x - 26, BY - 40); g.fill();
      for (let k = 0; k < 3; k++){ g.strokeStyle = `rgba(230,250,255,${.9 - k * .25})`; g.lineWidth = 3 - k; g.beginPath(); g.ellipse(x, BY - 4, 90 + k * 70, 18 + k * 12, 0, 0, 7); g.stroke(); }
      g.strokeStyle = '#eaf8ff'; g.lineWidth = 2; for (let i = 0; i < 10; i++){ const a = i / 10 * Math.PI * 2; g.beginPath(); g.moveTo(x, BY); let px = x, py = BY; for (let k = 0; k < 4; k++){ px += Math.cos(a + (R() - .5)) * 30; py += Math.sin(a) * 6; g.lineTo(px, py); } g.stroke(); } }
    if (b === 1 && sc === 'side'){   // 불꽃 숨결: 입에서 오른쪽 아래로 퍼지는 불길
      const mx = BX, my = BY - 132;
      for (let i = 0; i < 260; i++){ const t = R(), sp = (R() - .5) * (14 + t * 120); const x = mx + 10 + t * 260, y = my + t * 90 + sp; const r = 2 + t * 9 * R(); const c = t < .25 ? '#fff6c0' : t < .55 ? '#ffc040' : t < .8 ? '#ff7a2a' : '#d83a20'; g.globalAlpha = .5 + R() * .4; g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); } g.globalAlpha = 1;
      edge('rgba(255,120,40,A)', .25);
    }
    if (b === 1 && sc === 'all'){ edge('rgba(255,90,30,A)', .5); for (let i = 0; i < 11; i++){ const x = 20 + R() * 440, y = 60 + R() * 160; g.strokeStyle = 'rgba(255,190,90,.75)'; g.lineWidth = 3; g.beginPath(); g.moveTo(x - 40, y - 60); g.lineTo(x, y); g.stroke(); g.fillStyle = '#ffe080'; g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); g.fillStyle = '#ff6a2a'; g.beginPath(); g.arc(x + 1, y + 1, 4, 0, 7); g.fill(); } }
    if (b === 1 && sc === 'big'){ g.fillStyle = 'rgba(255,60,20,.22)'; g.fillRect(0, 0, W, H); for (let i = 0; i < 30; i++){ g.fillStyle = '#ffb040'; g.fillRect(R() * W, R() * 140, 3, 3); } }
    if (b === 2 && sc === 'side'){ pos.filter(p => p.side).forEach(p => { if (p.i === 8) return; for (const d of [-7, 6]){ g.fillStyle = 'rgba(30,10,50,.92)'; g.beginPath(); g.moveTo(p.x + d - 4, p.y + 2); g.quadraticCurveTo(p.x + d - 6, p.y - 18, p.x + d - 2, p.y - 26); g.lineTo(p.x + d + 4, p.y - 26); g.quadraticCurveTo(p.x + d + 6, p.y - 18, p.x + d + 4, p.y + 2); g.fill(); for (let k = 0; k < 3; k++) g.fillRect(p.x + d - 3 + k * 3, p.y - 31, 2, 6); } g.fillStyle = '#e0a0ff'; g.fillRect(p.x - 1, p.y - 40, 2, 2); }); }
    if (b === 2 && sc === 'all'){ for (let i = 0; i < 14; i++){ const y = 120 + i * 10 + Math.sin(i) * 6; const lg = g.createLinearGradient(0, y - 20, 0, y + 20); lg.addColorStop(0, 'rgba(120,60,180,0)'); lg.addColorStop(.5, 'rgba(120,60,180,.32)'); lg.addColorStop(1, 'rgba(120,60,180,0)'); g.fillStyle = lg; g.fillRect(0, y - 20, W, 40); } for (let i = 0; i < 8; i++){ const x = 40 + i * 58, y = 120 + R() * 90; g.fillStyle = 'rgba(230,200,255,.8)'; g.beginPath(); g.arc(x, y, 6, Math.PI, 0); g.lineTo(x + 6, y + 8); g.lineTo(x - 6, y + 8); g.fill(); g.fillStyle = '#2a1040'; g.fillRect(x - 3, y - 2, 2, 2); g.fillRect(x + 1, y - 2, 2, 2); } edge('rgba(150,80,220,A)', .45); }
    if (b === 2 && sc === 'big'){ [BX - 92, BX + 92].forEach(x => { g.strokeStyle = 'rgba(200,140,255,.8)'; g.lineWidth = 1; g.beginPath(); g.moveTo(BX, BY - 100); g.lineTo(x, BY - 100); g.stroke(); }); g.font = '10px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; ['진짜는 하나!', '', '진짜는 하나!'].forEach((t, k) => { if (!t) return; g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText('?', BX + (k - 1) * 92, 40); g.fillStyle = '#e0b0ff'; g.fillText('?', BX + (k - 1) * 92, 40); }); g.fillStyle = 'rgba(80,30,120,.18)'; g.fillRect(0, 0, W, H); }
    if (b === 3 && sc === 'side'){ for (let i = 0; i < 5; i++){ const x = BX + 70 + i * 40, y = 110 + (i % 3) * 30; g.strokeStyle = 'rgba(255,230,150,.5)'; g.lineWidth = 2; g.beginPath(); g.moveTo(BX + 30, BY - 150); g.quadraticCurveTo(x - 20, y - 40, x, y); g.stroke(); g.save(); g.translate(x, y); g.rotate(i); g.fillStyle = '#e8b858'; g.beginPath(); for (let k = 0; k < 16; k++){ const a = k / 16 * Math.PI * 2, rr = k % 2 ? 8 : 11; g.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } g.fill(); g.fillStyle = '#7a5420'; g.beginPath(); g.arc(0, 0, 3, 0, 7); g.fill(); g.restore(); } }
    if (b === 3 && sc === 'all'){ g.save(); g.globalAlpha = .38; g.strokeStyle = '#fff4c0'; g.lineWidth = 4; g.beginPath(); g.arc(BX, 120, 110, 0, 7); g.stroke(); for (let k = 0; k < 12; k++){ const a = k / 12 * Math.PI * 2; g.fillStyle = '#fff4c0'; g.fillRect(BX + Math.cos(a) * 98 - 3, 120 + Math.sin(a) * 98 - 3, 6, 6); } g.lineWidth = 6; g.beginPath(); g.moveTo(BX, 120); g.lineTo(BX, 40); g.stroke(); g.lineWidth = 4; g.beginPath(); g.moveTo(BX, 120); g.lineTo(BX + 60, 150); g.stroke(); g.restore(); g.fillStyle = 'rgba(255,220,120,.12)'; g.fillRect(0, 0, W, H); g.font = '14px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText('째깍....', BX, 246); g.fillStyle = '#fff4c0'; g.fillText('째깍....', BX, 246); }
    if (b === 3 && sc === 'big'){ g.save(); g.globalAlpha = .5; g.strokeStyle = '#ffd24a'; g.lineWidth = 3; for (let k = 0; k < 3; k++){ g.beginPath(); g.arc(BX, BY - 96, 60 + k * 22, -Math.PI * .1 - k * .4, Math.PI * 1.2 - k * .4, true); g.stroke(); const a = Math.PI * 1.2 - k * .4, x = BX + Math.cos(a) * (60 + k * 22), y = BY - 96 + Math.sin(a) * (60 + k * 22); g.fillStyle = '#ffd24a'; g.beginPath(); g.moveTo(x - 6, y); g.lineTo(x + 6, y); g.lineTo(x, y + 9); g.fill(); } g.restore(); g.font = '12px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText('+9 % 되돌아가요', BX, 30); g.fillStyle = '#fff4c0'; g.fillText('+9 % 되돌아가요', BX, 30); }
    if (sc === 'big' && b !== 3){ gauge(.81, '끊기 실패 81 %'); }
  };
  fxBefore(); await drawPeople(); drawBoss(BX, BY); fxAfter();
  return 1;
};
