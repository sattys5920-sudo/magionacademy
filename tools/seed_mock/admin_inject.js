// 시안: 관리자 「씨앗 대회 · 무슈 블랑」 진행도 카드 (목업 전용 · 예시 학생 데이터)
(function(){
const css = document.createElement('style'); css.textContent = `
#sdad{margin:10px 0}#sdad .hd{display:flex;justify-content:space-between;align-items:center;gap:8px}#sdad .hd b{font-size:15px}#sdad .sum{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:8px 0}
#sdad .sum div{background:#F6F0FC;border-radius:10px;padding:6px;text-align:center;font-size:11px;color:#6A5A8A}#sdad .sum div b{display:block;font-size:16px;color:#2A1A4A}
#sdad .flt{display:flex;gap:6px;margin-bottom:6px;flex-wrap:wrap}#sdad .flt button{border:1px solid #D8CCEA;background:#fff;border-radius:999px;padding:4px 10px;font-size:12px;color:#5A4A7A}#sdad .flt button.on{background:#2A1A4A;color:#FFD866;border-color:#2A1A4A}
#sdad .row{display:grid;grid-template-columns:72px 1fr;gap:8px;padding:8px 0;border-top:1px solid #EEE6F6;font-size:12px;color:#3A2A5A}#sdad .row .nm b{display:block;font-size:13px}#sdad .row .nm span{font-size:11px;color:#8A7AA8}
#sdad .ln{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center}#sdad .tag{border-radius:6px;padding:1px 6px;font-size:11px;background:#EEE6F6;color:#4A3A6A}#sdad .tag.g{background:#FFF0B0;color:#7A5A00}#sdad .tag.r{background:#FFE0E4;color:#A0203A}#sdad .tag.ok{background:#E0F6E4;color:#1A6A2A}
#sdad .dots{display:flex;gap:2px;flex-wrap:wrap}#sdad .dots i{width:9px;height:9px;border-radius:2px;background:#E6DEF0}#sdad .dots i.on{background:#7A4AC8}#sdad .dots i.sp{background:#E8A020}
#sdad .bar{height:6px;background:#EEE6F6;border-radius:3px;overflow:hidden;width:90px}#sdad .bar i{display:block;height:100%;background:#5AB83A}
#sdad .btns{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}#sdad .btns button{border:1px solid #D8CCEA;background:#fff;border-radius:8px;padding:6px 10px;font-size:12px}`;
document.head.appendChild(css);
const ST = ['씨앗', '새싹', '새싹', '꽃봉오리', '꽃봉오리', '꽃'];
const S = [   // 이름 · 식물 · 단계(0~5) · 오늘 물 · 오늘 말 · 빠진 날 · 열매(딴/가진) · 블랑 요리(준 번호들) · 마지막 인사
  ['민준', '거미줄 백합', 5, 2, 2, 0, [6, 2], [0, 1, 4, 5, 6, 12], 0], ['하늘', '잭오랜턴 호박꽃', 5, 1, 2, 0, [9, 3], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 1],
  ['레오', '박쥐 날개 고사리', 3, 2, 1, 1, [0, 0], [], 0], ['이로하', '눈알 열매덩굴', 4, 0, 0, 2, [0, 0], [], 0], ['세나', '사탕옥수수 튤립', 5, 2, 2, 0, [4, 1], [0, 3, 7], 0],
  ['도윤', '해골 양귀비', 1, 0, 1, 3, [0, 0], [], 0]];
const gold = r => r[2] === 5 && r[5] === 0;
let f = 'all';
function html(){
  const L = S.filter(r => f === 'all' || (f === 'need' && (r[3] < 2 || r[4] < 2) && r[2] < 5) || (f === 'bloom' && r[2] === 5) || (f === 'done' && r[8]));
  return `<div class="adcard" id="sdad"><div class="hd"><b>씨앗 대회 · 무슈 블랑</b><span class="s">10월 27일 시작 · 5일째</span></div>
  <div class="sum"><div><b>${S.filter(r => r[2] === 5).length}/${S.length}</b>꽃 피움</div><div><b>${S.filter(gold).length}</b>금화분</div><div><b>${S.reduce((a, r) => a + r[7].length, 0)}</b>블랑에게 준 요리</div><div><b>${S.filter(r => r[8]).length}</b>마지막 인사</div></div>
  <div class="flt">${[['all', '전체'], ['need', '오늘 덜 돌봄'], ['bloom', '꽃 핀 학생'], ['done', '17가지 다 줌']].map(([k, n]) => `<button class="${f === k ? 'on' : ''}" data-sdf="${k}">${n}</button>`).join('')}</div>
  ${L.map(r => `<div class="row"><div class="nm"><b>${r[0]}</b><span>${r[1]}</span></div><div>
    <div class="ln"><span class="tag ${r[2] === 5 ? (gold(r) ? 'g' : 'ok') : ''}">${gold(r) ? '★ 금화분 · ' : ''}${ST[r[2]]}${r[2] < 5 ? ` (${r[2] + 1}/5일째)` : ''}</span>
      ${r[2] < 5 ? `<span>💧 ${r[3]}/2</span><span>💬 ${r[4]}/2</span>${r[5] ? `<span class="tag r">빠진 날 ${r[5]}</span>` : ''}` : `<span>열매 딴 수 ${r[6][0]} · 가진 ${r[6][1]}</span>`}</div>
    <div class="ln" style="margin-top:4px"><span>블랑 ${r[7].length}/17</span><span class="dots">${Array.from({ length: 17 }, (_, i) => `<i class="${r[7].includes(i) ? (i >= 12 ? 'sp on' : 'on') : ''}" title="${i + 1}"></i>`).join('')}</span>${r[8] ? '<span class="tag ok">마지막 인사 봄</span>' : ''}</div>
  </div></div>`).join('') || '<div class="s">해당하는 학생이 없어요</div>'}
  <div class="btns"><button>이벤트 닫기</button><button>학생 한 명 진행 맞추기</button><button>식물 다시 나눠 주기</button></div></div>`;
}
function paint(){ let el = document.getElementById('sdad'); const host = document.querySelector('.adcard')?.parentNode || document.body; if (el) el.outerHTML = html(); else host.insertAdjacentHTML('afterbegin', html()); document.querySelectorAll('[data-sdf]').forEach(b => b.onclick = () => { f = b.dataset.sdf; paint(); }); }
window.__sdAdPaint = paint; window.__sdAdF = k => { f = k; paint(); }; paint();
})();
