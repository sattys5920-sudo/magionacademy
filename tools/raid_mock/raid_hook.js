window.__raidMock = async () => {
  const A = World.Avatar, W = 480, H = 270;
  const ov = document.createElement('div'); ov.id = 'raidov';
  ov.innerHTML = `<style>
#raidov{position:fixed;inset:0;z-index:99999;background:#140e22;color:#f4ecff;font-family:G11,Pretendard,sans-serif;display:flex;flex-direction:column;gap:6px;padding:10px 8px}#raidov>*{flex:none}
#raidov .rtop{display:flex;align-items:center;gap:8px;font-family:G11B,Pretendard,sans-serif;font-size:13px}
#raidov .bar{flex:1;height:14px;background:#2a1838;border:2px solid #1a1024;border-radius:3px;position:relative;overflow:hidden}
#raidov .bar i{position:absolute;inset:0;width:63%;background:linear-gradient(#ffe07a,#f0a43a)}
#raidov .bar b{position:absolute;inset:0;text-align:center;font-size:10px;line-height:14px;color:#1a1024}
#raidov .ph{font-size:11px;color:#9fd8ff}
#raidov canvas{width:100%;image-rendering:pixelated;border:2px solid #2a1838;border-radius:4px}
#raidov .pk{background:#3a2a10;border:2px solid #ffd866;border-radius:6px;padding:6px 8px;font-size:12px;color:#ffe9a8;font-family:G11B;display:flex;justify-content:space-between}
#raidov .pk small{font-family:G11;color:#d8c08a;font-size:10px}
#raidov .cards{display:grid;grid-template-columns:1fr 1fr;gap:6px}
#raidov .side{background:#1c1430;border-radius:6px;padding:4px}
#raidov .side>b{display:block;font-size:10px;color:#b9a8d8;padding:0 2px 3px}
#raidov .sg{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}
#raidov .rc{background:#2a1f42;border:2px solid #3a2e56;border-radius:5px;padding:3px;font-size:9px;position:relative}
#raidov .rc .h{display:flex;align-items:center;gap:3px;white-space:nowrap;overflow:hidden}
#raidov .rc img{width:18px;height:18px;image-rendering:pixelated;border-radius:3px;background:#1a1024}
#raidov .rc b{font-family:G11B;font-size:10px}
#raidov .rc .j{display:block;color:#9f90c0;font-size:8px}
#raidov .rc .hb,#raidov .rc .mb{height:4px;background:#3a2440;border-radius:2px;margin-top:2px;overflow:hidden}
#raidov .rc .hb i{display:block;height:100%;background:#7affb0}
#raidov .rc .mb i{display:block;height:100%;background:#6ab8ff}
#raidov .rc.low .hb i{background:#ff6a4a}
#raidov .rc.mine{border-color:#4fd8ff}
#raidov .rc.pick{border-color:#ffd866;box-shadow:0 0 0 1px #ffd866,0 0 8px rgba(255,216,102,.55)}
#raidov .rc.pick.low{animation:none;border-color:#ff9a6a;box-shadow:0 0 0 1px #ffd866,0 0 10px rgba(255,120,80,.8)}
#raidov .rc .rst{position:absolute;right:-2px;top:-7px;border:1px solid #ffd866;font-size:8px;line-height:1;padding:1px 2px;border-radius:2px;background:#1a1024;color:#ffd866}
#raidov .cmd{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}
#raidov .cmd button{background:#2e2248;color:#f4ecff;border:2px solid #4a3a6a;border-radius:6px;padding:9px 2px;font-family:G11B;font-size:12px}
#raidov .cmd button small{display:block;font-family:G11;font-size:9px;color:#b9a8d8}
#raidov .log{font-size:10px;color:#cbbbe8;background:#1c1430;border-radius:6px;padding:5px 7px;line-height:1.5}
</style>
<div class="rtop">얼음 거인<div class="bar"><i></i><b>63 %</b></div><span class="ph">2 단계</span></div>

<div style="display:grid;grid-template-columns:1fr auto 1fr;font-size:11px;color:#b9a8d8"><span>앞쪽 파티 6 명</span><span style="color:#ffe07a">남은 시간 4 분 12 초</span><span style="text-align:right">뒤쪽 파티 6 명</span></div>
<canvas id="rcv" width="${W}" height="${H}"></canvas>
<div class="log">얼음 거인이 <b style="color:#9fd8ff">눈보라</b>를 준비해요.... 뒤쪽을 보고 있어요! &nbsp;· 루나의 치유 +42</div>
<div class="pk">치유할 친구를 눌러요 · 치유의 빛<small>캔버스의 사람을 눌러도 돼요 · 취소</small></div>
<div class="cards" id="rcards"></div>
<div class="cmd"><button>공격<small>기본</small></button><button style="border-color:#ffd866;background:#4a3a18">치유의 빛<small>MP 6</small></button><button>보호막<small>MP 10</small></button><button>물약<small>×2</small></button></div>`;
  document.body.appendChild(ov);
  const cv = ov.querySelector('#rcv'), g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
  // 배경: 얼음 동굴 (하늘 · 얼음 기둥 · 눈 바닥)
  const sky = g.createLinearGradient(0, 0, 0, H); sky.addColorStop(0, '#1c2a4a'); sky.addColorStop(.47, '#3a5a86'); sky.addColorStop(.48, '#cfe6f6'); sky.addColorStop(1, '#8fb4d8'); g.fillStyle = sky; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 14; i++){ const x = i * 37 + (i % 3) * 7, h = 40 + (i * 53 % 50); g.fillStyle = i % 2 ? '#5a82b4' : '#6e98c8'; g.beginPath(); g.moveTo(x, 130); g.lineTo(x + 14, 130 - h); g.lineTo(x + 28, 130); g.fill(); g.fillStyle = 'rgba(255,255,255,.35)'; g.fillRect(x + 12, 130 - h + 6, 2, h - 10); }
  for (let i = 0; i < 18; i++){ g.fillStyle = '#a8cce8'; g.fillRect((i * 29) % W, 0, 6, 8 + (i * 7 % 14)); }
  g.fillStyle = 'rgba(255,255,255,.5)'; for (let i = 0; i < 60; i++) g.fillRect((i * 97) % W, (i * 53) % 120, 1, 1);
  // 가운데 얼음 마법진
  g.strokeStyle = 'rgba(160,220,255,.7)'; g.lineWidth = 1; g.beginPath(); g.ellipse(W / 2, 210, 74, 18, 0, 0, 7); g.stroke(); g.beginPath(); g.ellipse(W / 2, 210, 50, 12, 0, 0, 7); g.stroke();
  // 보스 (얼음빛을 입힌 돌 거인 ×3)
  const bim = await new Promise(r => { const im = new Image(); im.onload = () => r(im); im.src = 'art/raid_bosses.png?v=' + Date.now(); });   // LPC 보스 (tools/iso/lpc/raid_boss_lpc.py)
  g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(W / 2, 214, 40, 9, 0, 0, 7); g.fill();
  g.drawImage(bim, 64, 0, 64, 64, W / 2 - 80, 214 - 160 + 6, 160, 160);
  // 뒤쪽을 노리는 표시 (빨간 화살표)
  g.fillStyle = '#ff6a4a'; g.globalAlpha = .85; g.beginPath(); g.moveTo(W / 2 + 62, 80); g.lineTo(W / 2 + 84, 90); g.lineTo(W / 2 + 62, 100); g.fill(); g.globalAlpha = 1;
  // 12 명: 왼쪽 6 (오른쪽 보기), 오른쪽 6 (왼쪽 보기) · 앞열 3 + 뒷열 3
  const jobs = ['knight', 'warrior', 'thief', 'white', 'black', 'bard', 'knight', 'warrior', 'summon', 'alch', 'druid', 'time'];   // 앞열 3 = 앞에서 막고 · 뒷열 3 = 뒤에서 쏘고 고쳐요
  const names = ['지호', '루나', '하늘', '나', '미르', '서아', '도윤', '별이', '하랑', '유나', '라온', '새봄'];
  const meJ = { 0: 'black' }; const FW = A.FW, FH = A.FH, dirL = A.meta.dirs.left;
  const pos = []; for (let i = 0; i < 12; i++){ const side = i >= 6 ? 1 : 0, j = i % 6, front = j < 3, k = j % 3, xo = (front ? 160 : 80) + (k - 1) * -16; pos.push({ i, side, x: side ? W - xo : xo, y: 168 + k * 34 }); }
  for (const p of pos.slice().sort((a, b) => a.y - b.y)){ const i = p.i;
    const job = jobs[i], av = A.fromLook(ORDER_J.indexOf(job) * 131 + 7 + i * 3); try { await A.need(av); } catch (e) {}
    p.av = av; const sp = A.compose(av); g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(p.x, p.y, 11, 3, 0, 0, 7); g.fill();
    if (i === 3){ g.strokeStyle = '#4fd8ff'; g.lineWidth = 2; g.beginPath(); g.ellipse(p.x, p.y, 18, 5.5, 0, 0, 7); g.stroke(); }
    const s = .8, w = FW * s, h = FH * s;
    if (sp){ g.save(); g.translate(p.x, 0); if (!p.side) g.scale(-1, 1); g.drawImage(sp, dirL * FW, 0, FW, FH, -w / 2, p.y - h + 5, w, h); g.restore(); }
    const bw = 24, bx = Math.round(p.x - bw / 2), by = Math.round(p.y - h + 4), f = [78, 90, 64, 78, 40, 82, 70, 95, 22, 77, 88, 58][i] / 100;
    if (i === 3 || f <= .3){ g.font = '8px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; g.lineJoin = 'round'; g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText(names[i], p.x, by - 3); g.fillStyle = i === 3 ? '#7fe6ff' : '#ffb0a0'; g.fillText(names[i], p.x, by - 3); }   // 이름은 나 · 위험한 친구만
    g.fillStyle = '#1a1024'; g.fillRect(bx - 1, by - 1, bw + 2, 5); g.fillStyle = '#4a2a3a'; g.fillRect(bx, by, bw, 3); g.fillStyle = f > .3 ? '#7affb0' : '#ff6a4a'; g.fillRect(bx, by, Math.round(bw * f), 3);
  }
  // 숫자 띄우기
  g.font = '12px G11B, Pretendard, sans-serif'; g.textAlign = 'center'; [['-128', W / 2 - 40, 90, '#ffe07a'], ['-96', W / 2 + 34, 112, '#ffe07a'], ['+42', 120, 150, '#7affb0']].forEach(([t, x, y, c]) => { g.lineWidth = 3; g.strokeStyle = '#1a1024'; g.strokeText(t, x, y); g.fillStyle = c; g.fillText(t, x, y); });
  const hp = [78, 90, 64, 78, 40, 82, 70, 95, 22, 77, 88, 58], fx = { 1: '보호', 6: '도발', 8: '독' };
  for (const p of pos){ const y = p.y - FH * .8 - 14; g.fillStyle = '#1a1024'; g.fillRect(p.x - 6, y - 1, 13, 8); g.fillStyle = '#ffd866'; g.fillRect(p.x - 5, y, 11, 3); g.fillRect(p.x - 3, y + 3, 7, 2); g.fillRect(p.x - 1, y + 5, 3, 1); }
  const card = i => { const p = pos[i]; return `<div class="rc pick${i === 3 ? ' mine' : ''}${hp[i] <= 30 || hp[i] <= 40 ? ' low' : ''}"><div class="h">${headImg(p.av)}<span><b>${names[i]}</b><span class="j">${XJ[jobs[i]].n}</span></span></div><div class="hb"><i style="width:${hp[i]}%"></i></div><div class="mb"><i style="width:${[50, 30, 70, 55, 80, 60, 40, 90, 65, 35, 75, 50][i]}%"></i></div>${fx[i] ? `<span class="rst">${fx[i]}</span>` : ''}</div>`; };
  const grp = (t, a) => `<div class="side"><b>${t}</b><div class="sg">${a.map(card).join('')}</div></div>`;
  ov.querySelector('#rcards').innerHTML = grp('앞쪽 파티', [0, 1, 2, 3, 4, 5]) + grp('뒤쪽 파티', [6, 7, 8, 9, 10, 11]);
  return 1;
};
