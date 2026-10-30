// 시안: 사역마 창 (실제 게임 화면 위에 올려요). window.__famCfg 로 어떤 장면인지 정해요
//   { view: 'main' | 'gift' | 'list', i: 정령 번호, stage, pts, line, gifts, owned: [번호…] }
(function(){
const C = window.__famCfg || {}, L = window.__famLines || {};
const NM = ['Vael','Ixi','Puck','Lotis','Sol','Lune','Ignis','Rill','Orbi','Eon','Nyx','Iris'], SUB = ['푸른 혼불','보라 나선불','초록 도깨비불','분홍 연꽃불','금빛 햇무리불','은빛 달불','붉은 불기둥','청록 물결불','주황 고리불','남색 성운불','칠흑 그림자불','오로라 무지갯불'];
const MOOD = ['과묵한','장난꾸러기 쌍둥이','능글맞은','다정한','오만한','몽환적인','까칠한','느긋한','호기심 많은','늙은 현자','냉소적인','변덕쟁이'];
const COL = ['#5A8CFF','#A070FF','#40D070','#FF6AB8','#FFC838','#C8D8FF','#FF5A28','#30D8C8','#FF9030','#7088FF','#9A60F0','#E0C8FF'];
const STN = ['경계','관심','익숙','신뢰','맹약'], NEED = [0, 100, 200, 300, 400];
const ABIL = [['걷기 속도가 조금 빨라져요','탐사에서 함정 칸을 미리 알려 줘요','낚시 입질이 잦아져요','탐사 전투에서 첫 공격을 한 번 막아 줘요'],,,,,,['탐사 공격력이 조금 올라요','요리 불 조절이 쉬워져요','탐사 전투 치명타가 잦아져요','탐사 보스에게 더 큰 피해']];
const RARE = ['영혼 연꽃',,,,,,'화룡초'], RAREIC = [58,,,,,,43];
const BAG = [['I19', 6, 1], [26, 2, 1], [35, 1, 1], ['I1', 4, 0], [24, 3, -1], [7, 5, 0]];   // [아이콘, 개수, 알게 된 취향 1좋아함 -1싫어함 0모름]
const i = C.i || 0, st = C.stage ?? 1, pts = C.pts ?? 210, col = COL[i];
const css = `
#famv{position:fixed;left:0;right:0;top:56px;bottom:64px;z-index:400;display:flex;justify-content:center;align-items:flex-end;background:rgba(8,5,16,.55);font-family:var(--f-px);color:#F1E9FF}
#famv .fp{width:100%;max-width:560px;height:100%;background:#211733;border-top:1px solid #4E3C72;display:flex;flex-direction:column;overflow:hidden}
#famv .fh{display:flex;align-items:center;height:48px;padding:0 6px 0 16px;flex:none}
#famv .fh b{font-family:var(--f-pxb);font-size:18px;flex:1;color:#FFE9A0}
#famv .x{width:44px;height:44px;border:0;background:none;color:#CFC3EE;font-size:20px}
#famv .bd{flex:1;overflow:hidden;padding:0 14px 10px;display:flex;flex-direction:column;gap:8px}
#famv .hero{position:relative;height:150px;border-radius:14px;flex:none;overflow:hidden;background:radial-gradient(circle at 50% 62%, ${col}38 0, ${col}10 32%, transparent 60%),linear-gradient(#120C22,#1A1230);border:1px solid #3A2C58}
#famv .hero i{position:absolute;width:2px;height:2px;background:#fff;opacity:.5}
#famv .hero canvas{position:absolute;left:50%;top:40px;width:108px;height:108px;margin-left:-54px;image-rendering:pixelated}
#famv .hero .nm{position:absolute;left:12px;bottom:10px}
#famv .hero .nm b{display:block;font-family:var(--f-pxb);font-size:20px;color:#fff;text-shadow:0 0 8px ${col}}
#famv .hero .nm span{font-size:13px;color:#BFB0E0}
#famv .fsay{position:absolute;left:50%;top:8px;transform:translateX(-50%);width:max-content;max-width:300px;padding:6px 10px;font-size:14px;line-height:18px;text-align:center;word-break:keep-all;background:rgba(14,10,30,.85);border:1px solid ${col};box-shadow:0 0 10px ${col}88;border-radius:10px}
#famv .card{background:#2A1E40;border:1px solid #3E2E5E;border-radius:12px;padding:8px 12px;flex:none}
#famv .row{display:flex;align-items:center;gap:8px}
#famv .t{font-family:var(--f-pxb);font-size:15px;color:#FFE9A0;flex:1}
#famv .m{font-size:13px;color:#BFB0E0}
#famv .pips{display:flex;gap:4px;margin:6px 0 2px}
#famv .pip{flex:1;text-align:center;font-size:13px;color:#7A6A9A}
#famv .pip u{display:block;height:6px;border-radius:3px;background:#3A2C58;margin-bottom:4px;text-decoration:none}
#famv .pip.on{color:#F1E9FF} #famv .pip.on u{background:${col};box-shadow:0 0 6px ${col}}
#famv .pip.cur{color:${col}}
#famv .fbar{height:10px;border-radius:5px;background:#18102A;overflow:hidden;margin-top:6px}
#famv .fbar i{display:block;height:100%;background:linear-gradient(90deg,${col}99,${col});text-decoration:none}
#famv .gate{display:flex;align-items:center;gap:8px;margin-top:8px;padding:6px 8px;border-radius:8px;background:#1C1430;font-size:13px;color:#CFC3EE}
#famv .ic{width:32px;height:32px;background:url(art/plants.png?v=4) no-repeat;image-rendering:pixelated;flex:none}
#famv .gifts{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin-top:8px}
#famv .g{position:relative;height:50px;border-radius:10px;background:#1C1430;border:1px solid #3A2C58;display:flex;align-items:center;justify-content:center}
#famv .g em{position:absolute;right:4px;bottom:2px;font-style:normal;font-size:13px;color:#E8E0FF}
#famv .g s{position:absolute;left:4px;top:2px;text-decoration:none;font-size:13px}
#famv .ab{display:flex;gap:8px;align-items:flex-start;font-size:13px;line-height:16px;padding:1px 0;color:#E8E0FF}
#famv .ab b{flex:none;width:44px;font-size:13px;color:${col};font-family:var(--f-pxb)}
#famv .ab.lk{color:#6E5E8E} #famv .ab.lk b{color:#6E5E8E}
#famv .btns{display:flex;gap:8px;flex:none}
#famv .bt{flex:1;height:44px;border-radius:12px;border:1px solid #4E3C72;background:#2E2248;color:#F1E9FF;font-family:var(--f-pxb);font-size:15px}
#famv .bt.go{background:#FF9A3C;border-color:#C86A1E;color:#2A1606}
#famv .pop{position:absolute;inset:0;background:rgba(8,5,16,.72);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
#famv .plus{font-family:var(--f-pxb);font-size:28px;color:${col};text-shadow:0 0 12px ${col}}
#famv .grid12{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
#famv .sp{position:relative;height:132px;border-radius:12px;background:#1C1430;border:1px solid #3A2C58;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:8px}
#famv .sp canvas{position:absolute;top:6px;left:50%;margin-left:-40px;width:80px;height:80px;image-rendering:pixelated}
#famv .sp b{font-family:var(--f-pxb);font-size:14px} #famv .sp span{font-size:13px;color:#BFB0E0}
#famv .sp.cur{border-color:#FFD866;box-shadow:0 0 0 1px #FFD866 inset}
#famv .sp.no b{color:#6E5E8E} #famv .sp.no canvas{filter:brightness(0) opacity(.35)}`;
const st_ = document.createElement('style'); st_.textContent = css; document.head.appendChild(st_);
const v = document.createElement('div'); v.id = 'famv'; document.body.appendChild(v);
const icon = n => typeof n === 'string' ? `<span class="ic" style="background:url(art/icons.png?v=4) ${-(+n.slice(1)) * 32}px 0 no-repeat"></span>` : `<span class="ic" style="background-position:${-(n % 10) * 32}px ${-Math.floor(n / 10) * 32}px"></span>`;   // 'I19' = icons.png 칸
const stars = Array.from({ length: 26 }, (_, k) => `<i style="left:${(k * 37) % 100}%;top:${(k * 53) % 100}%;opacity:${.2 + (k % 5) * .12}"></i>`).join('');
const line = C.line || '';
let html = '';
if (C.view === 'list'){
  const own = C.owned || [0, 6, 9, 10];
  html = `<div class="fh"><b>사역마</b><button class="x">✕</button></div><div class="bd"><div class="row"><span class="t">계약한 정령</span><span class="m">${own.length} / 12</span></div><div class="grid12">` +
    NM.map((n, k) => { const o = own.includes(k); return `<div class="sp ${o ? '' : 'no'} ${k === i ? 'cur' : ''}"><canvas data-w="${k}" width="64" height="64"></canvas><b>${o ? n : '???'}</b><span>${o ? STN[[1, 0, 0, 0, 0, 0, 3, 0, 0, 2, 0, 0][k]] : '아직 만나지 못함'}</span></div>`; }).join('') + `</div></div>`;
} else {
  const lo = NEED[st], hi = NEED[Math.min(4, st + 1)], pct = st >= 4 ? 100 : Math.round((pts - lo) / (hi - lo) * 100);
  const gateTxt = '';
  html = `<div class="fh"><b>사역마</b><button class="x">✕</button></div><div class="bd">
  <div class="hero">${stars}<canvas data-w="${i}" width="64" height="64"></canvas>${line ? `<div class="fsay">${line}</div>` : ''}<div class="nm"><b>${NM[i]}</b><span>${SUB[i]} · ${MOOD[i]}</span></div></div>
  <div class="card"><div class="row"><span class="t">친밀도 · ${STN[st]}</span><span class="m">${st >= 4 ? pts : pts + ' / ' + hi}</span></div>
   <div class="pips">${STN.map((n, k) => `<div class="pip ${k <= st ? 'on' : ''} ${k === st ? 'cur' : ''}"><u></u>${n}</div>`).join('')}</div>
   <div class="fbar"><i style="width:${pct}%"></i></div>${gateTxt ? `<div class="gate">${gateTxt}</div>` : ''}</div>
  <div class="card"><div class="row"><span class="t">선물하기</span><span class="m">오늘 친해진 정도 ${C.today ?? 13} / 30</span></div>
   <div class="gifts">${BAG.map(([n, c, k]) => `<div class="g">${k === 1 ? '<s style="color:' + col + '">♥</s>' : k === -1 ? '<s style="color:#8A7AAA">✕</s>' : ''}${icon(n)}<em>${c}</em></div>`).join('')}</div></div>
  <div class="card"><div class="row" style="margin-bottom:4px"><span class="t">함께하는 힘</span></div>
   ${(ABIL[i] || ABIL[0]).map((a, k) => `<div class="ab ${k + 1 <= st ? '' : 'lk'}"><b>${STN[k + 1]}</b><span>${k + 1 <= st ? a : '🔒 ' + STN[k + 1] + '이 되면 열려요'}</span></div>`).join('')}</div>
  <div class="btns"><button class="bt">정령 바꾸기</button><button class="bt go">따라다니는 중</button></div></div>`;
  if (C.view === 'gift') html += `<div class="pop"><canvas data-w="${i}" width="64" height="64" style="width:160px;height:160px;image-rendering:pixelated"></canvas><div class="fsay" style="position:static;transform:none">${C.giftLine}</div><div class="row">${icon('I19')}<span class="plus">+10</span></div></div>`;
}
v.innerHTML = `<div class="fp" style="position:relative">${html}</div>`;
const SPR = new Image(); SPR.src = 'wisps3_anim.png';
const tick = now => { requestAnimationFrame(tick); if (!SPR.complete) return; const f = Math.floor(now / 110) % 8;
  v.querySelectorAll('canvas[data-w]').forEach(c => { const g = c.getContext('2d'); g.clearRect(0, 0, 64, 64); g.drawImage(SPR, f * 64, +c.dataset.w * 64, 64, 64, 0, 0, 64, 64); }); };
requestAnimationFrame(tick);
})();
