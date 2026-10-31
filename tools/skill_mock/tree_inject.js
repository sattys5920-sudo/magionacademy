// 시안: 스킬 트리 화면에 「빠른 스킬 4칸」 고르기 — 실제 게임 스킬 트리 위에 덧붙여 보여 줘요 (목업 전용)
//   위: 빠른 칸 4개(자동으로 채운 칸은 「자동」 표시) · 아래 스킬 설명 칸: 「빠른 칸에 넣기」 → 바꿀 칸 고르기 · 새로 배우면 빈칸에 저절로
(function(){
const css = document.createElement('style'); css.textContent = `
.qs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:4px}.qsh{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--gold);margin:0 2px 4px}.qsh span{color:var(--sub);font-size:11px}
.qc{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 2px;border-radius:10px;border:2px solid #6a4ab0;background:rgba(106,74,176,.18);font-size:10px;min-height:66px;color:inherit;font-family:inherit}.qc .sic{width:32px;height:32px}
.qc.empty{border-style:dashed;opacity:.6;justify-content:center}.qc em{position:absolute;left:3px;top:2px;font-style:normal;font-size:9px;background:#3a2c18;color:#ffd866;border-radius:4px;padding:0 3px}.qc b.n{position:absolute;right:3px;top:2px;font-size:9px;color:#cbb8ff}
.qc.pick{border-color:var(--gold);box-shadow:0 0 10px rgba(255,216,102,.6);animation:qp 1s infinite}@keyframes qp{50%{transform:translateY(-2px)}}
.tn .qm{position:absolute;left:4px;top:2px;font-size:11px;color:#ffd866}
.qtoast{position:fixed;left:50%;bottom:120px;transform:translateX(-50%);background:#2a1e44;border:2px solid var(--gold);color:#fff;border-radius:12px;padding:8px 14px;font-size:13px;z-index:999}`;
document.head.appendChild(css);
const ico = el => el ? el.outerHTML : '';
let Q = [{ k: '0_0', auto: 1 }, { k: '1_0', auto: 1 }, { k: '0_1', auto: 1 }, null], picking = null;
const node = k => document.querySelector(`[data-ts="${k}"]`);
const name = k => node(k)?.querySelector('small')?.textContent || '';
function bar(){
  const sec = document.querySelector('.tcol')?.closest('.sec'); if (!sec) return;
  let w = document.getElementById('qsw'); if (!w){ w = document.createElement('section'); w.className = 'sec'; w.id = 'qsw'; sec.parentNode.insertBefore(w, sec); }
  w.innerHTML = `<div class="qsh">빠른 스킬 4칸 <span>${picking ? '바꿀 칸을 눌러요' : '전투 첫 화면에 바로 나와요'}</span></div><div class="qs">${Q.map((q, i) => q ? `<button class="qc${picking ? ' pick' : ''}" data-q="${i}">${q.auto ? '<em>자동</em>' : ''}<b class="n">${i + 1}</b>${ico(node(q.k)?.querySelector('.sic'))}<span>${name(q.k)}</span></button>` : `<button class="qc empty${picking ? ' pick' : ''}" data-q="${i}">빈칸<br>＋</button>`).join('')}</div>`;
  w.querySelectorAll('[data-q]').forEach(b => b.onclick = () => { if (!picking) return; Q[+b.dataset.q] = { k: picking }; picking = null; toast(`「${name(Q[+b.dataset.q].k)}」을 빠른 칸에 넣었어요`); paint(); });
  document.querySelectorAll('.tn').forEach(t => { t.querySelector('.qm')?.remove(); if (Q.some(q => q && q.k === t.dataset.ts)){ const m = document.createElement('span'); m.className = 'qm'; m.textContent = '★'; t.appendChild(m); } });
}
function detail(){
  const up = document.getElementById('tup'); if (!up) return; let b = document.getElementById('qput');
  const sel = document.querySelector('.tn.sel')?.dataset.ts, inQ = Q.findIndex(q => q && q.k === sel), learned = !/0\/5/.test(document.querySelector('.tn.sel i')?.textContent || '');
  if (!b){ b = document.createElement('button'); b.id = 'qput'; b.className = 'btn'; b.style.cssText = 'width:100%;margin-top:6px'; up.after(b); }
  b.disabled = !learned; b.textContent = !learned ? '배운 스킬만 빠른 칸에 넣을 수 있어요' : inQ >= 0 ? `★ 빠른 칸 ${inQ + 1}번에서 빼기` : '☆ 빠른 칸에 넣기';
  b.onclick = () => { if (inQ >= 0){ Q[inQ] = null; paint(); return; } const e = Q.findIndex(q => !q); if (e >= 0){ Q[e] = { k: sel }; toast(`빈칸 ${e + 1}번에 넣었어요`); paint(); } else { picking = sel; paint(); } };
}
function toast(t){ const d = document.createElement('div'); d.className = 'qtoast'; d.textContent = t; document.body.appendChild(d); setTimeout(() => d.remove(), 1800); }
function paint(){ bar(); detail(); }
window.__qsLearn = k => { const e = Q.findIndex(q => !q); if (e >= 0){ Q[e] = { k, auto: 1 }; toast(`새로 배운 「${name(k)}」이 빈칸 ${e + 1}번에 들어갔어요`); } paint(); };
window.__qsPaint = paint; window.__qsPick = k => { picking = k; paint(); };
new MutationObserver(() => { if (document.querySelector('.tcol') && !document.getElementById('qsw')) paint(); else if (document.getElementById('tup') && !document.getElementById('qput')) paint(); }).observe(document.body, { childList: true, subtree: true });
paint();
})();
