// 시안: 창밖 정원 창의 「도감」 탭 — 손님 20 칸 · 손님 자세히(조건 · 좋아하는 요리 2 · 온 횟수 · 단골 · 사진 3) · 못 만난 손님 힌트 · 채운 수 보상(꾸미기 · 가구만)
//   목업 사이트 폴더에 gi_bg.png · gi_items.png · gi_guests.png · gi.json · window.__gxGo() · window.__gxLog
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__gxLog = [], T0 = performance.now(), mark = k => LOG.push([(performance.now() - T0) / 1000, k]);
const img = s => Object.assign(new Image(), { src: s }), BG = img('gi_bg.png'), IT = img('gi_items.png'), GU = img('gi_guests.png'), DS = img('art/dishes.png?v=5'), GF = img('art/forage.png');
let GI = null; fetch('gi.json').then(r => r.json()).then(j => { GI = j; });
const CW = 144, CH = 88, CY = 8, PP = (tx, ty) => [GI.OX + (tx - ty) * 8, GI.OY + (tx + ty) * 4 - CY];
// 손님 20 (gi_guests.png 순서) · 조건 · 좋아하는 요리 2 (dishes.png 칸) · 선물 (forage.png 칸)
const G = [
 ['참새', '먹이 그루터기 · 아침', [63, 1], 16], ['까치', '등불 · 맑은 날', [4, 66], 38], ['파랑새', '등불 · 저녁', [11, 70], 9], ['딱따구리', '그네 · 낮', [13, 65], 13], ['비둘기', '먹이 그루터기 + 호박 의자 · 낮', [0, 67], 0],
 ['앵무새', '바람 종 · 맑은 낮', [5, 77], 9], ['벌새', '꽃 화분 · 아침', [59, 80], 4], ['울새', '연못 · 비 온 뒤', [12, 69], 6], ['홍학', '연못 + 등불 · 저녁', [60, 18], 31], ['공작새', '연못 + 바람 종 + 꽃 화분 · 맑은 날', [83, 86], 46],
 ['생쥐', '호박 의자 · 밤', [71, 27], 12], ['햄스터', '먹이 그루터기 · 저녁', [62, 65], 16], ['수달', '연못 · 아침', [68, 81], 41], ['아기 사슴', '꽃 화분 + 그네 · 안개 낀 아침', [73, 82], 4], ['레서판다', '그네 + 호박 의자 · 바람 부는 날', [67, 3], 5],
 ['오소리', '먹이 그루터기 · 한밤', [15, 74], 21], ['도마뱀', '빈 칸이 많을 때 · 맑은 낮', [58, 23], 3], ['꼬마 두더지', '먹이 그루터기 · 아침', [61, 8], 0], ['꼬마 거북', '연못 + 먹이 그루터기 · 아침', [2, 76], 38], ['이끼 달팽이', '연못 · 비 온 뒤', [9, 6], 6]];
const DN = ['호박씨 크림수프', '도토리 쿠키', '유령 피라미 튀김', '버섯 꼬치구이', '산딸기 잼 토스트', '당근 머핀', '세잎클로버 차', '피처럼 붉은 토마토주스', '호박 붕어 버섯 조림', '박쥐 날개 잎 쌈', '거미 버섯 마카롱', '블루베리 파이', '이끼 송사리 오믈렛', '꿀 군밤 꼬치', '유령 마시멜로', '늪지 추어탕', '독사과 캔디', '옥수수 달빛수프', '젤리 해파리 젤리', '거미 가재 매운찜', '해골 메기 사골탕', '솜사탕 넙치 푸딩', '달빛 송어 구이', '반딧불이 리소토'];
const NEWN = ['박하 소다', '민들레 솜털 차', '딸기 우유', '당근 수프', '완두콩 죽', '해바라기씨 강정', '카모마일 컵케이크', '호두 빵', '단풍 시럽 토스트', '대나무 통밥', '촛불 빙어 튀김', '구름 게 크로켓', '라벤더 쿠키', '옥수수 버터빵', '인삼 꿀차', '튤립 꽃잎 샐러드', '마법 문어 볶음', '등불 새우 꼬치', '알로에 젤리', '선인장 에이드', '눈송이 꽃 셔벗', '구름 목화 팬케이크', '반딧불 꽃가루 소다', '오로라 연어 스테이크', '종꽃 찹쌀떡', '꿈꽃 타르트', '서리 딸기 케이크', '별빛 청새치 스테이크', '바다 포도 파르페'];
const dname = i => i >= 58 ? NEWN[i - 58] : DN[i] || '';
const MET = { 0: { n: 9, reg: 1, fd: [1, 1] }, 2: { n: 4, fd: [1, 0] }, 4: { n: 2, fd: [0, 1] }, 11: { n: 6, reg: 1, fd: [1, 0] }, 12: { n: 5, reg: 1, fd: [1, 1] }, 17: { n: 3, fd: [1, 0] }, 19: { n: 7, fd: [0, 1] } };   // fd: 그 요리를 먹으러 온 적 있으면 밝혀짐   // 만난 손님 7 종 (단골 3)
const REW = [[5, '이름표', '새 모이 이름표', 'tag'], [10, '방 가구', '손님 사진 액자', 'frame'], [15, '말풍선', '정원 말풍선', 'bub'], [20, '방 가구', '나무 새집', 'house']];
const css = document.createElement('style'); css.textContent = `
#gx{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%) scale(.9);opacity:0;transition:all .4s cubic-bezier(.2,1.3,.4,1);z-index:350;width:min(94vw,380px);max-height:calc(100vh - 150px);overflow:auto;background:rgba(20,13,34,.97);border:2px solid #9AE07A;border-radius:16px;padding:10px;font-family:var(--f-px);color:#F1E9FF;box-shadow:0 0 24px rgba(154,224,122,.3)}
#gx.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#gx .hd{display:flex;justify-content:space-between;align-items:center}#gx .hd b{font-family:var(--f-pxb);font-size:16px;color:#CFF5B8}#gx .hd i{font-style:normal;width:32px;height:32px;border-radius:16px;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center}
#gx .tabs{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0}#gx .tabs span{text-align:center;padding:8px 0;border-radius:10px;background:#2A2040;font-family:var(--f-pxb);font-size:14px;color:#B8A8D8}#gx .tabs span.on{background:#9AE07A;color:#1E2A14}
#gx canvas.g{width:100%;aspect-ratio:144/88;image-rendering:pixelated;border-radius:6px;display:block;background:#140D1E}
#gx .rw{display:flex;gap:6px;margin-bottom:8px}#gx .rw div{flex:1;background:#2A2040;border-radius:10px;padding:5px 2px 4px;text-align:center;font-size:10px;line-height:13px;color:#C8B8E8;border:2px solid transparent;position:relative}#gx .rw div.got{border-color:#9AE07A;color:#E8FFD8}#gx .rw div.next{border-color:#FFE9A0}#gx .rw div b{display:block;font-family:var(--f-pxb);font-size:12px;color:#FFF3C8}#gx .rw canvas{width:34px;height:22px;image-rendering:pixelated;display:block;margin:2px auto}#gx .rw .rq{display:block;height:22px;margin:2px auto;font-family:var(--f-pxb);font-size:16px;line-height:22px;color:#6A5A90}#gx .rw div.got:after{content:'✓';position:absolute;right:4px;top:2px;color:#9AE07A;font-family:var(--f-pxb)}
#gx .bar{height:8px;border-radius:4px;background:#2A2040;margin:0 2px 8px;overflow:hidden}#gx .bar i{display:block;height:100%;background:linear-gradient(90deg,#7AC85A,#C8F07A)}
#gx .gr{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}#gx .gr div{aspect-ratio:1;border-radius:10px;background:#2A2040;border:2px solid #3A2E58;display:flex;align-items:center;justify-content:center;font-family:var(--f-pxb);color:#5A4A80;font-size:18px;position:relative}#gx .gr div.on{background:#24402A;border-color:#5AA84A}#gx .gr div.sel{outline:3px solid #FFE9A0}#gx .gr canvas{width:78%;height:78%;image-rendering:pixelated}#gx .gr div em{position:absolute;right:2px;top:0;font-style:normal;font-size:11px;color:#FFD866}
#gx .dt{margin-top:8px;background:#FBF6EA;color:#3A2C4A;border-radius:12px;padding:10px;font-size:12px;line-height:18px}#gx .dt .dtop{display:flex;gap:10px;align-items:center}#gx .dt .dtop canvas{width:64px;height:64px;image-rendering:pixelated;background:#E4F2D8;border-radius:10px;border:2px solid #9AC87A}#gx .dt .dtop b{display:block;font-family:var(--f-pxb);font-size:15px}#gx .dt .gtag{display:inline-block;background:#FFE9A0;color:#5A3A12;border-radius:999px;padding:0 7px;font-size:11px;margin-left:4px;font-family:var(--f-pxb)}
#gx .dt .li{display:flex;justify-content:space-between;gap:6px;margin-top:6px;border-top:1px dashed #D8CCB0;padding-top:6px}#gx .dt .li span:first-child{color:#8A7AA0;white-space:nowrap}#gx .dt .fd{display:flex;gap:6px;align-items:center}#gx .dt .fd .dq{font-style:normal;width:24px;height:24px;border-radius:6px;background:#E8DCC4;color:#8A7AA0;display:inline-flex;align-items:center;justify-content:center;font-family:var(--f-pxb)}#gx .dt .fd canvas{width:24px;height:24px;image-rendering:pixelated}
#gx .dt .ph{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px}#gx .dt .ph canvas,#gx .dt .ph div{width:100%;aspect-ratio:4/3;image-rendering:pixelated;border:2px solid #3A2C4A;border-radius:3px;background:#E8DCC4;display:flex;align-items:center;justify-content:center;font-size:10px;color:#8A7AA0}
#gx .hint{margin-top:8px;background:#3A2C4A;color:#FFF3C8;border-radius:10px;padding:8px 10px;font-size:12px;line-height:18px}
#gxpop{position:fixed;left:50%;top:44%;z-index:360;transform:translate(-50%,-50%) scale(.6);opacity:0;transition:all .45s cubic-bezier(.2,1.3,.4,1);background:rgba(20,13,34,.97);border:2px solid #FFE9A0;border-radius:16px;padding:14px 18px;text-align:center;font-family:var(--f-pxb);color:#FFF3C8;width:min(80vw,300px);box-shadow:0 0 22px rgba(255,233,160,.4);pointer-events:none}#gxpop.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#gxpop small{display:block;font-family:var(--f-px);font-size:12px;color:#E0D4F4;margin-top:6px;line-height:18px}#gxpop canvas{width:120px;height:80px;image-rendering:pixelated;display:block;margin:4px auto}`;
document.head.appendChild(css);
const v = Object.assign(document.createElement('div'), { id: 'gx' }); document.body.appendChild(v); const pop = Object.assign(document.createElement('div'), { id: 'gxpop' }); document.body.appendChild(pop);
const gIcon = (c, i, sz = 14) => { const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, c.width, c.height); q.drawImage(GU, i * 28, 0, 14, 14, (c.width - sz) / 2, (c.height - sz) / 2, sz, sz); };
// 보상 그림 (작게): 이름표 · 액자 · 말풍선 · 새집
function rewIcon(c, k){ const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, c.width, c.height); const R = (x, y, w, h, col) => { q.fillStyle = col; q.fillRect(x, y, w, h); };
  if (k === 'tag'){ R(4, 7, 26, 9, '#1a1024'); R(5, 8, 24, 7, '#3A5A2A'); R(6, 9, 22, 1, '#9AE07A'); [8, 13, 18, 23].forEach(x => R(x, 11, 2, 2, '#F0D070')); R(1, 9, 3, 3, '#E8902A'); R(30, 9, 3, 3, '#E8902A'); }
  if (k === 'frame'){ R(9, 2, 16, 18, '#5A3A12'); R(10, 3, 14, 16, '#E8B84A'); R(12, 5, 10, 12, '#D8C49A'); q.drawImage(GU, 12 * 28, 0, 14, 14, 10, 4, 14, 14); }
  if (k === 'bub'){ R(4, 3, 26, 12, '#1a1024'); R(5, 4, 24, 10, '#E8FFD8'); R(7, 15, 4, 3, '#1a1024'); R(8, 15, 2, 2, '#E8FFD8'); R(25, 2, 4, 4, '#5AA84A'); R(26, 1, 2, 1, '#9AE07A'); [9, 14, 19].forEach(x => R(x, 8, 2, 2, '#5AA84A')); }
  if (k === 'house'){ R(14, 12, 4, 10, '#6A4428'); R(8, 4, 16, 10, '#B87A3A'); R(7, 2, 18, 3, '#7A3A2A'); R(14, 7, 4, 4, '#2A1A10'); R(20, 9, 3, 1, '#6A4428'); q.drawImage(GU, 2 * 28, 0, 14, 14, 18, -2, 14, 14); } }
// 사진 (정원 장면 속 손님)
const PLACED = [{ k: 'pond', tx: 1.6, ty: 3.6 }, { k: 'lamp', tx: 1, ty: 1.6 }, { k: 'feeder', tx: 5, ty: 4.6 }, { k: 'swing', tx: 5.2, ty: 1 }];
function shot(c, gi, at){ const t = document.createElement('canvas'); t.width = CW; t.height = CH; const g = t.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BG, 0, CY, CW, CH, 0, 0, CW, CH);
  PLACED.forEach(o => { const m = GI.items[o.k], [x, y] = PP(o.tx, o.ty); g.drawImage(IT, m.sx, 0, m.sw, m.sh, Math.round(x - m.ax), Math.round(y - m.ay), m.sw, m.sh); });
  const [x, y] = PP(at[0], at[1]); g.drawImage(GU, gi * 28 + (at[2] || 0) * 14, 0, 14, 14, Math.round(x - 7), Math.round(y - 13), 14, 14);
  const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(t, Math.max(0, Math.min(CW - 48, x - 24)), Math.max(0, Math.min(CH - 36, y - 26)), 48, 36, 0, 0, c.width, c.height); q.fillStyle = 'rgba(255,240,200,.12)'; q.fillRect(0, 0, c.width, c.height); }
let raf = 0; function garden(c){ cancelAnimationFrame(raf); const loop = now => { if (!GI || !c.isConnected) return; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BG, 0, CY, CW, CH, 0, 0, CW, CH);
  PLACED.forEach(o => { const m = GI.items[o.k], [x, y] = PP(o.tx, o.ty); g.drawImage(IT, m.sx, 0, m.sw, m.sh, Math.round(x - m.ax), Math.round(y - m.ay), m.sw, m.sh); });
  const [x, y] = PP(4.4, 4.9); g.drawImage(GU, 11 * 28 + (Math.floor(now / 450) % 2) * 14, 0, 14, 14, Math.round(x - 7), Math.round(y - 13), 14, 14); raf = requestAnimationFrame(loop); }; raf = requestAnimationFrame(loop); }
const metN = Object.keys(MET).length; let RV = metN;   // 보상은 받은 것만 보여요
function render(tab, sel){
  const head = `<div class="hd"><b>창밖 정원</b><i>✕</i></div><div class="tabs"><span class="${tab === 'g' ? 'on' : ''}">정원</span><span class="${tab === 'd' ? 'on' : ''}">도감 ${metN} / 20</span></div>`;
  if (tab === 'g'){ v.innerHTML = head + '<canvas class="g" width="144" height="88"></canvas>'; garden(v.querySelector('canvas.g')); return; }
  const rw = `<div class="rw">${REW.map(([n, kind, nm, ic]) => RV >= n ? `<div class="got"><b>${n} 종</b><canvas width="34" height="22" data-ri="${ic}"></canvas>${kind}<br>${nm}</div>` : `<div class="${(REW.find(r => r[0] > RV) || [])[0] === n ? 'next' : ''}"><b>${n} 종</b><span class="rq">?</span>???</div>`).join('')}</div><div class="bar"><i style="width:${metN / 20 * 100}%"></i></div>`;
  const grid = `<div class="gr">${G.map((g, i) => `<div class="${MET[i] ? 'on' : ''} ${sel === i ? 'sel' : ''}">${MET[i] ? `<canvas width="20" height="20" data-gi="${i}"></canvas>${MET[i].reg ? '<em>★</em>' : ''}` : '?'}</div>`).join('')}</div>`;
  let dt = '';
  if (sel != null && MET[sel]){ const g = G[sel], m = MET[sel];
    dt = `<div class="dt"><div class="dtop"><canvas width="16" height="16" data-big="${sel}"></canvas><div><b>${g[0]}${m.reg ? '<span class="gtag">★ 단골</span>' : ''}</b>온 횟수 ${m.n} 번 · 선물 ${m.reg ? 3 : 2} 개씩</div></div>
      <div class="li"><span>오는 조건</span><span>${g[1]}</span></div>
      <div class="li"><span>좋아하는 요리</span><span class="fd">${[0, 1].map(j => m.fd && m.fd[j] ? `<canvas width="32" height="32" data-dish="${g[2][j]}"></canvas>${dname(g[2][j])}` : '<i class="dq">?</i>???').join('')}</span></div>
      <div class="li"><span>두고 가는 선물</span><span class="fd"><canvas width="32" height="32" data-gift="${g[3]}"></canvas></span></div>
      <div class="ph"><canvas width="96" height="72" data-ph="0"></canvas><canvas width="96" height="72" data-ph="1"></canvas>${m.reg ? '<canvas width="96" height="72" data-ph="2"></canvas>' : '<div>단골이 되면<br>한 장 더</div>'}</div></div>`; }
  else if (sel != null) dt = `<div class="hint">??? · ${G[sel][1].split(' · ').map((s, i) => i === 0 ? s.split(' + ')[0] : s).join(' · ')} · ${['곡물', '열매', '물고기', '꽃'][sel % 4]} 요리를 좋아해요</div>`;
  v.innerHTML = head + rw + grid + dt;
  v.querySelectorAll('[data-gi]').forEach(c => gIcon(c, +c.dataset.gi)); v.querySelectorAll('[data-ri]').forEach(c => rewIcon(c, c.dataset.ri));
  v.querySelectorAll('[data-big]').forEach(c => gIcon(c, +c.dataset.big)); v.querySelectorAll('[data-dish]').forEach(c => { const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(DS, +c.dataset.dish * 32, 0, 32, 32, 0, 0, 32, 32); });
  v.querySelectorAll('[data-gift]').forEach(c => { const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.drawImage(GF, +c.dataset.gift * 32, 0, 32, 32, 0, 0, 32, 32); });
  const SPOT = { 12: [[2.3, 3.9, 0], [1.2, 4.4, 1], [2.6, 3.2, 0]], 11: [[4.4, 4.9, 0], [4.7, 5.3, 1], [3.9, 4.6, 0]] };
  v.querySelectorAll('[data-ph]').forEach(c => shot(c, sel, (SPOT[sel] || [[3, 3, 0], [3.5, 3.4, 1], [2.5, 2.8, 0]])[+c.dataset.ph]));
}
window.__gxGo = async () => {
  await sleep(700); render('g'); v.classList.add('on'); mark('open'); await sleep(2400);
  render('d'); mark('tab'); await sleep(2800);
  render('d', 12); mark('pick'); await sleep(4200);
  for (let k = 0; k <= 30; k++){ v.scrollTop = 400 * k / 30; await sleep(25); } await sleep(1800); for (let k = 30; k >= 0; k--){ v.scrollTop = 400 * k / 30; await sleep(15); } await sleep(500);
  render('d', 11); mark('pick'); await sleep(3600);
  render('d', 9); mark('pick'); await sleep(2600);
  render('d', 3); mark('pick'); await sleep(2200);
  // 다음 보상: 10 종 「손님 사진 액자」 받는 장면
  pop.innerHTML = `도감 10 종 달성!<canvas width="34" height="22"></canvas>방 가구 「손님 사진 액자」<small>정원에서 찍은 손님 사진이 액자에 차례로 걸려요</small>`; rewIcon(pop.querySelector('canvas'), 'frame'); pop.classList.add('on'); RV = 10; render('d', 3); mark('reward'); await sleep(3400); pop.classList.remove('on'); await sleep(600);
  v.classList.remove('on'); await sleep(500); window.__gxDone = true;
};
})();
