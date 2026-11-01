// 시안: 창밖 정원 시작 연출 — 관리자가 「시작하기」를 누르면 피스(이어 붙인 거인)가 찾아와 정원을 시공해 줘요
//   똑똑 → 피스 등장 → 「정원 하나 만들어 드릴까요?」 → 부탁해요 → 뚝딱뚝딱 시공 → 「다 됐어요」 → 정원 공개 → 피스 퇴장 → 창문 → 정원 창
//   목업 사이트 폴더에 gi_bg.png · gi_items.png · gi_guests.png · gi.json · window.__gbGo() · window.__gbLog
(function(){
const sleep = ms => new Promise(r => setTimeout(r, ms)), LOG = window.__gbLog = [], T0 = performance.now(), mark = k => { LOG.push([(performance.now() - T0) / 1000, k]); const d = document.getElementById('vmk'); if (d) d.style.background = LOG.length % 2 ? '#FF0000' : '#0000FF'; };
if (!document.getElementById('vmk')) document.body.insertAdjacentHTML('beforeend', '<div id="vmk" style="position:fixed;left:0;top:0;width:6px;height:6px;z-index:99999;background:#00FF00;pointer-events:none"></div>');
const img = s => Object.assign(new Image(), { src: s }), BG = img('gi_bg.png'), IT = img('gi_items.png'), GU = img('gi_guests.png'), NP = img('art/npcs.webp?v=' + (window.NPC_ART_V || 1));
let GI = null; fetch('gi.json').then(r => r.json()).then(j => { GI = j; });
const CW = 144, CH = 88, CY = 8, PP = (tx, ty) => [GI.OX + (tx - ty) * 8, GI.OY + (tx + ty) * 4 - CY];
const SPR = 11, FW = 64;   // 피스 (npcs.webp 줄)
const css = document.createElement('style'); css.textContent = `
#gbdim{position:fixed;inset:0;background:rgba(10,6,20,.55);opacity:0;transition:opacity .6s;z-index:300;pointer-events:none}
#gbsay{position:fixed;left:50%;bottom:150px;transform:translateX(-50%);z-index:340;width:min(92vw,370px);display:none}
#gbsay .bx{display:flex;gap:10px;align-items:flex-start;background:rgba(20,13,34,.97);border:2px solid #C8B8E8;border-radius:14px;padding:10px 12px}
#gbsay .fc{width:52px;height:52px;flex:none;border-radius:10px;background:#3A2E58;overflow:hidden}#gbsay canvas{width:52px;height:52px;image-rendering:pixelated}
#gbsay b{display:block;font-family:var(--f-pxb);font-size:14px;color:#CFF5B8;margin-bottom:2px}#gbsay p{margin:0;font-family:var(--f-px);font-size:14px;line-height:21px;color:#F1E9FF}
#gbask{position:fixed;left:50%;bottom:96px;transform:translateX(-50%);z-index:341;display:none;gap:8px}#gbask span{padding:9px 16px;border-radius:12px;background:#2A2040;border:2px solid #6A5A90;font-family:var(--f-pxb);font-size:14px;color:#F1E9FF}#gbask span.go{background:#9AE07A;border-color:#9AE07A;color:#1E2A14}#gbask span.hit{transform:scale(.94)}
#gbyard{position:fixed;left:50%;top:44%;transform:translate(-50%,-50%) scale(.9);opacity:0;transition:all .5s cubic-bezier(.2,1.3,.4,1);z-index:330;width:min(94vw,380px);background:rgba(20,13,34,.97);border:2px solid #9AE07A;border-radius:16px;padding:10px;text-align:center;box-shadow:0 0 24px rgba(154,224,122,.3)}
#gbyard.on{opacity:1;transform:translate(-50%,-50%) scale(1)}#gbyard canvas{width:100%;aspect-ratio:144/88;image-rendering:pixelated;border-radius:6px;display:block;background:#140D1E}
#gbyard b{display:block;font-family:var(--f-pxb);font-size:16px;color:#CFF5B8;margin:2px 0 8px}#gbyard .pb{height:8px;border-radius:4px;background:#2A2040;margin-top:8px;overflow:hidden}#gbyard .pb i{display:block;height:100%;width:0;background:linear-gradient(90deg,#7AC85A,#C8F07A)}
#gbbang{position:fixed;left:50%;top:22%;transform:translate(-50%,-50%);z-index:332;font-family:var(--f-pxb);font-size:22px;color:#FFE9A0;text-shadow:0 2px 0 #3A2414;opacity:0;transition:opacity .15s;pointer-events:none;white-space:nowrap}
#gbtoast{position:fixed;left:50%;top:76px;transform:translate(-50%,-10px);z-index:345;background:rgba(20,13,34,.95);border:2px solid #9AE07A;border-radius:12px;padding:8px 14px;font-family:var(--f-px);font-size:13px;color:#F1E9FF;opacity:0;transition:all .3s;white-space:nowrap}#gbtoast.on{opacity:1;transform:translate(-50%,0)}`;
document.head.appendChild(css);
const el = (id, html = '') => { const d = document.createElement('div'); d.id = id; d.innerHTML = html; document.body.appendChild(d); return d; };
const dim = el('gbdim'), say = el('gbsay', '<div class="bx"><div class="fc"><canvas width="32" height="32"></canvas></div><div><b></b><p></p></div></div>'), ask = el('gbask'), yard = el('gbyard'), bang = el('gbbang'), tst = el('gbtoast');
// 피스 얼굴 (npcs.webp 정면 칸에서 머리만)
const face = () => { const q = say.querySelector('canvas').getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, 32, 32); q.drawImage(NP, 16, SPR * FW + 6, 32, 32, 0, 0, 32, 32); };
async function line(t, hold = 1500){ face(); say.querySelector('b').textContent = '피스'; say.style.display = 'block'; const p = say.querySelector('p'); p.textContent = ''; mark('line');
  for (let k = 1; k <= t.length; k++){ p.textContent = t.slice(0, k); await sleep(32); } await sleep(hold + t.length * 22); say.style.display = 'none'; await sleep(140); }
const toast = async (t, ms = 2600) => { tst.textContent = t; tst.classList.add('on'); mark('toast'); await sleep(ms); tst.classList.remove('on'); await sleep(300); };
// 방 안에 피스 세우기 (프롭)
let pis = null, pisA = 0, pisCol = 0, pisRaf = 0;
function pisDraw(){ if (!pis) return; const c = document.createElement('canvas'); c.width = FW; c.height = FW; const q = c.getContext('2d'); q.imageSmoothingEnabled = false; q.globalAlpha = pisA; q.drawImage(NP, pisCol * FW, SPR * FW, FW, FW, 0, 0, FW, FW);
  World.setProps(pis.m, [{ id: 'pis', x: pis.x, y: pis.y, img: c, pxc: q, sw: FW, sh: FW, ax: 32, ay: 58, solid: false }], 'gbpis'); }
// 마당 그리기: 잡초 → 치우기 → 물건
const WEED = []; for (let i = 0; i < 46; i++) WEED.push([Math.random() * 6.4 - .2, Math.random() * 6.4 - .2, Math.random()]);
let st = { weed: 1, dust: 0, items: [], shine: 0 };
const ITEMS = [{ k: 'feeder', tx: 4.6, ty: 4.4 }, { k: 'lamp', tx: 1.2, ty: 1.6 }, { k: 'pumpkin', tx: 4.8, ty: 1.6 }];
function yardDraw(c, now){ const g = c.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(BG, 0, CY, CW, CH, 0, 0, CW, CH);
  if (st.weed > 0){ g.fillStyle = `rgba(40,30,20,${.55 * st.weed})`; g.fillRect(0, 0, CW, CH);
    WEED.forEach(([tx, ty, r], i) => { if (r > st.weed) return; const [x, y] = PP(tx, ty), h = 5 + Math.round(r * 5), sw = Math.sin(now / 400 + i) * .8;
      [[-2, 0, '#3E5A1E'], [0, 1, '#6A8A2A'], [2, 2, '#4E6E22']].forEach(([dx, dh, col], j) => { const bx = Math.round(x + dx + (j === 1 ? sw : -sw * .5)), bh = h - dh; g.fillStyle = col; g.fillRect(bx, Math.round(y - bh), 1, bh); g.fillStyle = '#9AAA4A'; g.fillRect(bx, Math.round(y - bh), 1, 1); });
      }); }
  st.items.forEach(o => { const m = GI.items[o.k], [x, y] = PP(o.tx, o.ty), s = o.s == null ? 1 : o.s; const w = m.sw * s, h = m.sh * s;
    g.drawImage(IT, m.sx, 0, m.sw, m.sh, Math.round(x - m.ax * s), Math.round(y - m.ay * s), Math.round(w), Math.round(h)); });
  if (st.dust > 0){ for (let i = 0; i < 7; i++){ const ph = (now / 900 + i / 7) % 1, a = i * 2.1, x = CW / 2 + Math.cos(a) * (14 + i * 5), y = CH / 2 + 10 + Math.sin(a) * 10 - ph * 10, r = 3 + ph * 5;
      g.globalAlpha = st.dust * (1 - ph) * .85; g.fillStyle = '#F4ECDA'; [[0, 0, 1], [-.7, .3, .7], [.7, .3, .7], [0, -.5, .6]].forEach(([dx, dy, k]) => { g.beginPath(); g.arc(x + dx * r, y + dy * r, r * k, 0, 7); g.fill(); }); g.globalAlpha = 1; } }
  if (st.shine > 0){ for (let i = 0; i < 14; i++){ const x = (i * 37 + now / 30) % CW, y = (i * 23) % CH, k = (Math.sin(now / 160 + i) + 1) / 2; g.globalAlpha = st.shine * k; g.fillStyle = '#FFF3C8'; g.fillRect(Math.round(x), Math.round(y), 1, 3); g.fillRect(Math.round(x) - 1, Math.round(y) + 1, 3, 1); } g.globalAlpha = 1; } }
let yRaf = 0; const yardLoop = c => { const f = now => { if (!GI) return (yRaf = requestAnimationFrame(f)); yardDraw(c, now); yRaf = requestAnimationFrame(f); }; yRaf = requestAnimationFrame(f); };
async function bonk(t){ bang.textContent = t; bang.style.opacity = 1; bang.style.transform = `translate(-50%,-50%) rotate(${Math.random() * 16 - 8}deg)`; mark('bonk'); const c = yard.querySelector('canvas'); yard.style.transform = 'translate(-50%,-50%) translate(2px,1px)'; await sleep(70); yard.style.transform = 'translate(-50%,-50%) translate(-2px,0)'; await sleep(70); yard.style.transform = ''; await sleep(160); bang.style.opacity = 0; }
window.__gbGo = async () => {
  const t = World.meTile(); pis = { m: t.m, x: t.x + 1, y: t.y - 1 };
  await sleep(500); mark('knock'); await toast('똑, 똑똑.......', 1800);
  dim.style.opacity = 1; for (let k = 1; k <= 12; k++){ pisA = k / 12; pisDraw(); await sleep(70); } World.say('me', '.......!'); await sleep(1100);
  await line('안녕하세요.... {player} 님. 저 피스예요.'.replace('{player}', (window.__T && __T.me && __T.me().nick) || '민준'));
  await line('요즘 밤마다 푹 자서요.... 힘이 남아돌아요. 그래서 학생들 방을 돌면서 작은 정원을 만들어 주고 있어요.', 1700);
  await line('창밖 빈터가 풀만 무성하던데.... 정원 하나 만들어 드릴까요?', 1200);
  ask.innerHTML = '<span>다음에요</span><span class="go">부탁해요</span>'; ask.style.display = 'flex'; await sleep(1300); const b = ask.querySelector('.go'); b.classList.add('hit'); mark('pick'); await sleep(200); ask.style.display = 'none';
  World.say('me', '부탁해요.......'); await sleep(1000);
  await line('네.... 금방 해 드릴게요. 뚝딱뚝딱.......', 900);
  // 시공
  yard.innerHTML = '<b>창밖 빈터</b><canvas width="144" height="88"></canvas><div class="pb"><i></i></div>'; const yc = yard.querySelector('canvas'); yardLoop(yc); yard.classList.add('on'); mark('yard'); await sleep(1600);
  yard.querySelector('b').textContent = '시공 중.......'; st.dust = 1; const pb = yard.querySelector('.pb i');
  const W = ['뚝딱!', '쿵!', '뚝딱뚝딱!', '탕!', '쓱싹쓱싹', '뚝딱!', '쿵쿵!', '뚝딱!'];
  for (let i = 0; i < W.length; i++){ await bonk(W[i]); st.weed = Math.max(0, 1 - (i + 1) / 5); pb.style.width = ((i + 1) / W.length * 100) + '%';
    if (i >= 5){ const o = { ...ITEMS[i - 5], s: .2 }; st.items.push(o); for (let k = 0; k <= 6; k++){ o.s = .2 + k / 6 * .8 + (k === 5 ? .15 : 0); await sleep(30); } o.s = 1; mark('place'); }
    await sleep(320); }
  st.dust = 0; st.weed = 0; yard.querySelector('b').textContent = '창밖 정원'; st.shine = 1; mark('done'); await sleep(1600);
  yard.classList.remove('on'); await sleep(500);
  await line('후우.... 시공 다 됐어요.', 1100);
  await line('먹이 접시에 요리를 올려 두면.... 손님이 찾아올 거예요. 손님마다 좋아하는 요리가 달라요.', 1700);
  await line('호박 의자랑 등불은 덤이에요. 그럼.... 저는 다음 방으로 가 볼게요. 쿨.......', 1300);
  for (let k = 12; k >= 0; k--){ pisA = k / 12; pisDraw(); await sleep(70); } World.setProps(pis.m, [], 'gbpis'); dim.style.opacity = 0; await sleep(600);
  await toast('창밖 정원이 생겼어요 · 내 방 창문을 누르면 볼 수 있어요', 2800);
  // 그 뒤: 창문을 누르면 정원 창
  if (window.__gxShow){ mark('open'); window.__gxN = 0; window.__gxShow([{ k: 'feeder', tx: 4.6, ty: 4.4 }, { k: 'lamp', tx: 1.2, ty: 1.6 }, { k: 'pumpkin', tx: 4.8, ty: 1.6 }], 1); await sleep(3200); }
  cancelAnimationFrame(yRaf); window.__gbDone = true;
};
})();
