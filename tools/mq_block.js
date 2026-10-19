// ----- 메인 의뢰 「일곱 등불의 의뢰」 (지시서 tools/main_quest_spec.md) -----
// 데이터: data/main/index.json(순서) · cast.json(의뢰인·조연) · <qid>/quest.json · stage_N_request.json / stage_N_complete.json · idle.json · npc_lines.json
// 상태: me.mq = { q: 지금 의뢰 id, st: 단계(1~5), ph: 'arrive'(등장 대기) | 'pre'(부탁 전) | 'go'(목표 수행) | 'ready'(보고 전), prog: {}, done: { qid: 끝낸 날 }, dl: 기한 날, sawFull, named: {} }
const MQ = { list: [], q: {}, cast: {}, items: {}, scenes: {}, idle: {}, lines: {}, ready: null, loaded: false };
const MQ_V = 1;
const mqFetch = async p => { try { const r = await fetch(`data/main/${p}?v=${MQ_V}`); return r.ok ? await r.json() : null; } catch(e){ return null; } };
MQ.ready = (async () => {
  const idx = await mqFetch('index.json'); if (!idx) return;
  MQ.list = idx.quests || idx; MQ.cast = (await mqFetch('cast.json')) || {}; MQ.lines = (await mqFetch('npc_lines.json')) || {};
  await Promise.all(MQ.list.map(async id => { const q = await mqFetch(`${id}/quest.json`); if (q){ MQ.q[id] = q; Object.entries(q.items || {}).forEach(([k, v]) => { MQ.items[k] = v; ITEM[k] = v.name; }); } }));
  Object.entries(MQ.cast).forEach(([id, c]) => { if (!NL.cast[id]) NL.cast[id] = { name: c.name, av: c.av, look: c.look }; });
  MQ.loaded = true; if (me) { mqSky(); syncNpcs(); mqTick(); }
})();
const mqState = () => { if (!me.mq) me.mq = { q: null, st: 1, ph: 'arrive', prog: {}, done: {}, named: {} }; me.mq.prog = me.mq.prog || {}; me.mq.done = me.mq.done || {}; me.mq.named = me.mq.named || {}; return me.mq; };
const mqQuest = () => { const s = mqState(); return s.q ? MQ.q[s.q] : null; };
const mqStage = () => { const q = mqQuest(); return q ? q.stages.find(x => x.n === mqState().st) : null; };
const mqClient = q => (q = q || mqQuest()) ? MQ.cast[q.client] : null;
const mqName = id => { const c = MQ.cast[id]; if (!c) return id; const nm = mqState().named?.[id]; return nm || c.name; };
const mqShards = () => me.inv.lantern_shard || 0;
const mqDoneN = () => Object.keys(mqState().done).length;
// 달: 실제 달 (관리자·시험용 강제: localStorage['magion-moon'] = full | new | other)
const moonNow = () => { const f = localStorage.getItem('magion-moon'); if (f) return f; if (isFullMoon()) return 'full'; const a = moonAge(); return a <= 1.5 || a >= 28 ? 'new' : 'other'; };
const MOON_KO = { full: '보름', new: '그믐', other: '반달' };
// ---- 밤하늘: 끝낸 의뢰 수만큼 별이 켜져요 ----
function mqSky(){ if (!World.setSky || !me) return; const d = mqState().done, lit = MQ.list.slice(0, 6).map(id => !!d[id]); World.setSky({ lit, jack: !!d[MQ.list[6]], done: !!d[MQ.list[6]], hint: mqShards() >= 6 }); }
// ---- 의뢰인·조연을 맵에 세우기 (syncNpcs가 불러요) ----
function mqNpcs(){
  if (!me || !MQ.loaded) return []; const s = mqState(), out = [], seen = {};
  const put = (id, pl, mark, dir) => { const c = MQ.cast[id]; if (!c || seen[id]) return; const p = mqPlace(pl); if (!p) return; seen[id] = 1;
    out.push({ id: 'mq:' + id, name: mqName(id), map: p.map, x: p.x, y: p.y, r: 0, mark, wander: false, dir: dir || 'down', ...(c.av ? { av: World.Avatar.fix(c.av) } : { spr: c.spr, float: c.float, alpha: c.alpha }) }); };
  if (s.q && MQ.q[s.q]){ const q = MQ.q[s.q], st = mqStage();
    if (s.ph !== 'arrive'){ const pl = (st && st.place) || q.place; put(q.client, pl, s.ph === 'pre' || s.ph === 'ready' ? '❗' : '', st && st.dir); }
    (st && st.actors || []).forEach(a => put(a.id, a.place, a.mark ? '❗' : '', a.dir));
  }
  // 끝낸 의뢰인은 마을에 남아요
  MQ.list.forEach(id => { const q = MQ.q[id]; if (q && s.done[id] && q.after && !(s.q === id)) put(q.client, q.after.place, '', q.after.dir); });
  return out;
}
const mqPlace = pl => { if (!pl) return null; if (typeof pl === 'string'){ const p = NL.places[pl]; return p ? { map: p.map, x: p.x, y: p.y } : null; } return pl.place ? { ...mqPlace(pl.place), ...(pl.x !== undefined ? { x: pl.x, y: pl.y } : {}) } : pl; };
// ---- 장면 불러오기 ----
async function mqScene(qid, n, kind){ const k = `${qid}/stage_${n}_${kind}.json`; if (!MQ.scenes[k]) MQ.scenes[k] = await mqFetch(k); return MQ.scenes[k]; }
async function mqIdle(qid){ if (!MQ.idle[qid]) MQ.idle[qid] = (await mqFetch(`${qid}/idle.json`)) || {}; return MQ.idle[qid]; }
// ---- 열기: 다음 의뢰가 올 때가 됐나 (매일 아침 · 15초마다 · 들어올 때) ----
function mqTick(){
  if (!me || !MQ.loaded) return; const s = mqState();
  if (s.q){ if (s.ph === 'arrive') mqArrive(); else mqCheck(); mqDeadline(); return; }
  if (Object.keys(s.done).length >= 6 && moonNow() === 'full') s.sawFull = 1;   // 여섯째 의뢰 뒤 호박달 축제를 봤어요
  const next = MQ.list.find(id => !s.done[id]); if (!next) return; const q = MQ.q[next]; if (!q) return;
  const u = q.unlock || {}; if (u.afterQuest && !s.done[u.afterQuest]) return;
  const base = u.afterQuest ? s.done[u.afterQuest] : 0; if (me.day < (base || 0) + (u.daysAfter || 0) || me.day < (u.minDay || 0)) return;
  if (u.time && bandNow() !== u.time && !(u.time === 'morning' && ['day', 'evening', 'night'].includes(bandNow()))) return;   // 아침에 온다 = 그날 아무 때나
  if (u.afterFestival && !(s.sawFull && moonNow() !== 'full')) return;
  s.q = next; s.st = 1; s.ph = 'arrive'; s.prog = {}; s.dl = null; save(); mqArrive();
}
let mqArriving = false;
async function mqArrive(){
  const s = mqState(), q = mqQuest(); if (!q || s.ph !== 'arrive' || mqArriving || evOn || sheetOn || $('#storyui').classList.contains('on') || $('#npcui').classList.contains('on') || (World.cutBusy && World.cutBusy())) return;
  mqArriving = true;
  try {
    const sc = await mqScene(q.id, 1, 'request'); if (!sc){ mqArriving = false; return; }
    const arr = sc.arrival || []; const at = q.arrival || {};
    const go = () => new Promise(r => { const pl = mqPlace(at.player || at.place || 'main_hall'); if (!pl) return r(); if (World.where() === pl.map){ World.teleport(pl.map, [pl.x, pl.y], r); } else World.teleport(pl.map, [pl.x, pl.y], r); });
    closeSheet(); npcClose(); await go(); await sleep(400);
    let skip = false; const sk = document.createElement('button'); sk.className = 'btn sm mqskip'; sk.textContent = '건너뛰기'; sk.onclick = () => { skip = true; }; $('#stage').appendChild(sk);
    await World.cut(arr, { sfx: id => sfx(id), skip: () => skip }); sk.remove();
    s.ph = 'pre'; save(); syncNpcs();
    await mqPlay(q, 1, 'request', sc);
  } catch(e){ console.error(e); }
  mqArriving = false;
}
// ---- 장면 재생: 부탁 → 'go', 완료 → 보상 → 다음 단계 'pre' (5단계면 의뢰 완료) ----
async function mqPlay(q, n, kind, sc){
  sc = sc || await mqScene(q.id, n, kind); if (!sc) return toast('장면 파일이 아직 없어요');
  const c = MQ.cast[q.client], who = { id: q.client, name: mqName(q.client), title: c.title || '', spr: c.spr, av: c.av };
  const ev = { title: sc.title || '', conditions: { location: sc.scene?.location || (mqStage()?.place?.place) || q.place || 'main_hall' }, scene: sc.scene || {}, script: sc.script || [], cold: [] };
  mqSceneQ = q; await evPlay(who, n, ev, { main: true, replay: !!sc.replay, then: () => mqAfter(q, n, kind, sc) });
}
let mqSceneQ = null;
function mqAfter(q, n, kind, sc){
  const s = mqState(); if (sc.replay || s.q !== q.id) return;
  if (kind === 'request'){ s.st = n; s.ph = 'go'; s.prog = {}; const st = q.stages.find(x => x.n === n); s.dl = st && st.deadline ? me.day + st.deadline : null; s.prog.__day = me.day;
    (st && st.actors || []).forEach(a => { if (a.spawnOnly) return; });
    save(); syncNpcs(); mqMarks(); mqCheck(true); toast(`일지에 새 목표가 생겼어요 · ${st ? esc(st.title || '') : ''}`); }
  else {
    const st = q.stages.find(x => x.n === n), r = st && st.rewards || {}, got = [];
    if (r.gold){ me.coin += r.gold; got.push(`${r.gold}G`); } if (r.mana){ me.mana += r.mana; got.push(`마력 +${r.mana}`); } if (r.know){ me.know = (me.know || 0) + r.know; got.push(`지식 +${r.know}`); }
    [].concat(r.items || []).forEach(it => { const [k, cnt] = typeof it === 'string' ? [it, 1] : [it.id, it.n || 1]; mqGive(k, cnt); got.push(`${ITEM[k] || k} ×${cnt}`); });
    if (n >= 5 || n >= q.stages.length){   // 의뢰 완료
      const cr = q.completion_reward || {}; [].concat(cr.items || []).forEach(k => { mqGive(k, 1); got.push(ITEM[k] || k); });
      s.done[q.id] = me.day; s.q = null; s.st = 1; s.ph = 'arrive'; s.prog = {}; s.dl = null;
      mqSky(); if (World.setMarks) World.setMarks([]);
      toast(`「${esc(q.name || q.id)}」 의뢰를 끝냈어요${got.length ? ' · ' + got.join(', ') : ''}`);
      if (q.order === 7){ me.nflag = me.nflag || {}; me.nflag.main_done = 1; }
    } else { s.st = n + 1; s.ph = 'pre'; s.prog = {}; s.dl = null; toast(`${n}단계 끝! ${got.length ? got.join(', ') + ' · ' : ''}${mqName(q.client)}에게 다시 말을 걸면 다음 부탁을 들어요`); }
    save(); hud(); syncNpcs(); mqMarks();
  }
  if (sheetOn && sub === 'journal') render();
}
function mqGive(k, n = 1){ const it = MQ.items[k]; if (it && it.furn){ me.fbag = me.fbag || {}; me.fbag[it.furn] = (me.fbag[it.furn] || 0) + n; return; } if (it && it.cloth){ me.closet = me.closet || {}; me.closet[it.cloth] = 1; return; } me.inv[k] = (me.inv[k] || 0) + n; }
// ---- 목표 ----
const OBJ_KO = { collect: '모으기', craft: '만들기', deliver: '전하기', visit: '가기', talk: '이야기하기', clue: '단서 찾기', puzzle: '퍼즐', wait_moon: '달 기다리기', defend: '지키기', choice: '선택' };
function mqObjs(){ const st = mqStage(); return st ? (st.objectives || []) : []; }
function mqObjState(o, i){   // → { done, cur, need, text, hint }
  const s = mqState(), P = s.prog, t = o.type, h = o.hint ? fillVars(o.hint, null) : '';
  if (t === 'collect'){ const cur = me.inv[o.item] || 0; return { done: cur >= o.count, cur, need: o.count, text: `${ITEM[o.item] || o.item} ${o.count}개 모으기`, hint: h || (o.hint_location && NL.places[o.hint_location] ? `${NL.places[o.hint_location].name}에 있어요` : '') }; }
  if (t === 'craft'){ const cur = P['craft:' + o.item] || 0, n = o.count || 1; return { done: cur >= n, cur, need: n, text: `${ITEM[o.item] || o.item} ${n > 1 ? n + '개 ' : ''}만들기${o.quality ? ` (품질 ${MQ_Q[o.quality]} 이상)` : ''}`, hint: h || `${o.place === 'candy' ? '과자 교실 오븐' : '물약 교실 솥'}에서 「의뢰 제조」` }; }
  if (t === 'deliver'){ const cur = P['deliver:' + i] || 0, n = o.count || 1; return { done: cur >= n, cur, need: n, text: `${mqName(o.to)}에게 ${ITEM[o.item] || o.item} ${n}개 전하기`, hint: h || `가진 것 ${me.inv[o.item] || 0}개` }; }
  if (t === 'visit'){ const d = !!P['visit:' + i]; const p = NL.places[o.place]; return { done: d, cur: d ? 1 : 0, need: 1, text: `${p ? fillVars(p.name) : o.place}에 가기${o.time ? ' · ' + o.time.map(x => BAND_KO[x]).join('이나 ') : ''}${o.weather ? ' · ' + o.weather.map(x => WX_KO[x]).join('이나 ') : ''}${o.moon ? ' · ' + MOON_KO[o.moon] : ''}`, hint: h }; }
  if (t === 'talk'){ const d = !!P['talk:' + (o.who)]; return { done: d, cur: d ? 1 : 0, need: 1, text: `${mqName(o.who) === o.who ? (npcGet(o.who)?.name || o.who) : mqName(o.who)}${withJosa(mqName(o.who) === o.who ? (npcGet(o.who)?.name || o.who) : mqName(o.who), '과', '와')} 이야기하기`, hint: h || (o.where ? `${NL.places[o.where]?.name || ''}에 있어요` : '') }; }
  if (t === 'clue'){ const cur = (o.spots || []).filter(sp => P['clue:' + sp.id]).length, n = o.count || (o.spots || []).length; return { done: cur >= n, cur, need: n, text: `${o.text || '단서'} ${n}개 찾기`, hint: h || (o.spots || []).filter(sp => !P['clue:' + sp.id]).slice(0, 2).map(sp => sp.hint || NL.places[sp.place]?.name || '').filter(Boolean).join(' · ') }; }
  if (t === 'puzzle'){ const d = !!P['puzzle:' + i]; return { done: d, cur: d ? 1 : 0, need: 1, text: o.text || (o.kind === 'stars' ? '별자리 잇기' : '순서 맞추기'), hint: h || '일지에서 「풀기」를 눌러요' }; }
  if (t === 'wait_moon'){ const d = moonNow() === o.moon || !!P['moon:' + i]; return { done: d, cur: d ? 1 : 0, need: 1, text: `${MOON_KO[o.moon]}까지 기다리기`, hint: h || `지금은 ${MOON_KO[moonNow()]}이에요` }; }
  if (t === 'defend'){ const d = !!P['defend:' + i]; return { done: d, cur: d ? 1 : 0, need: 1, text: o.text || '등불 지키기', hint: h || (o.place ? `${NL.places[o.place]?.name || ''}에서 시작해요` : '') }; }
  if (t === 'choice'){ const d = (o.flags || []).some(f => flagOn(f)); return { done: d, cur: d ? 1 : 0, need: 1, text: o.text || '마음을 정하기', hint: h || `${mqName(mqQuest()?.client)}에게 말을 걸어요` }; }
  return { done: true, cur: 1, need: 1, text: t, hint: '' };
}
const MQ_Q = { normal: '보통', good: '좋음', best: '최고' }, MQ_QN = { normal: 0, good: 1, best: 2 };
function mqCheck(quiet){
  const s = mqState(); if (!s.q || s.ph !== 'go') return;
  const objs = mqObjs(); if (!objs.length) return;
  // 가 보기 목표: 지금 있는 곳
  objs.forEach((o, i) => { if (o.type === 'visit' && !s.prog['visit:' + i]){ const p = NL.places[o.place]; if (!p) return; const here = World.where && World.where() === p.map && World.myPos && (() => { const m = World.myPos(); return Math.hypot(m.x - p.x, m.y - p.y) <= (p.r || 2) + 3; })();
    const ok = here && (!o.time || o.time.includes(bandNow())) && (!o.weather || o.weather.includes(weatherToday())) && (!o.moon || moonNow() === o.moon);
    if (ok){ s.prog['visit:' + i] = 1; toast(`${fillVars(p.name)}에 왔어요 ✓`); save(); } }
    if (o.type === 'wait_moon' && !s.prog['moon:' + i] && moonNow() === o.moon){ s.prog['moon:' + i] = 1; save(); } });
  const all = objs.every((o, i) => mqObjState(o, i).done);
  if (all){ s.ph = 'ready'; save(); syncNpcs(); if (World.setMarks) World.setMarks([]); toast(`목표를 다 했어요! ${mqName(mqQuest().client)}에게 알려요`); if (sheetOn && sub === 'journal') render(); }
}
function mqDeadline(){ const s = mqState(); if (!s.q || s.ph !== 'go' || !s.dl) return; if (me.day > s.dl){ const st = mqStage(); s.dl = me.day + (st.deadline || 5); Object.keys(s.prog).filter(k => k.startsWith('craft:')).forEach(k => delete s.prog[k]); save(); toast('기한이 지나 제조를 처음부터 다시 해요'); } }
// 조사 지점(clue)을 맵에 띄워요
function mqMarks(){ if (!World.setMarks) return; const s = mqState(); if (!s.q || s.ph !== 'go') return World.setMarks([]); const list = [];
  mqObjs().forEach(o => { if (o.type !== 'clue') return; (o.spots || []).forEach(sp => { if (s.prog['clue:' + sp.id]) return; const p = mqPlace(sp.place ? { place: sp.place, x: sp.x, y: sp.y } : sp); if (p) list.push({ id: sp.id, map: p.map, x: p.x, y: p.y, label: sp.label || '조사하기' }); }); });
  World.setMarks(list); }
World.onMark = id => { const s = mqState(); let hit = null; mqObjs().forEach(o => { if (o.type === 'clue') (o.spots || []).forEach(sp => { if (sp.id === id) hit = sp; }); }); if (!hit || s.prog['clue:' + id]) return;
  s.prog['clue:' + id] = 1; save(); mqMarks(); const o = mqObjs().find(x => x.type === 'clue' && (x.spots || []).includes(hit)), st = mqObjState(o, mqObjs().indexOf(o));
  mqPanelText(hit.title || '단서', fillVars(hit.text || ''), `<span class="tag">${st.cur} / ${st.need}</span>`); if (hit.item) mqGive(hit.item, 1); mqCheck(); };
// 제조·요리에서 불러요: 의뢰 제조는 mqCraft가, 일반 요리·물약도 셀 수 있게
function mqOnCraft(item, quality = 'normal'){ const s = mqState(); if (!s.q || s.ph !== 'go') return; mqObjs().forEach(o => { if (o.type === 'craft' && o.item === item && (!o.quality || MQ_QN[quality] >= MQ_QN[o.quality])){ s.prog['craft:' + item] = (s.prog['craft:' + item] || 0) + 1; } }); save(); mqCheck(); }
function mqOnTalk(id){ const s = mqState(); if (!s.q || s.ph !== 'go') return null; let line = null; mqObjs().forEach((o, i) => { if (o.type === 'talk' && o.who === id && !s.prog['talk:' + id]){ s.prog['talk:' + id] = 1; line = o.line || null; }
  if (o.type === 'deliver' && o.to === id){ const have = me.inv[o.item] || 0, need = (o.count || 1) - (s.prog['deliver:' + i] || 0); if (have > 0 && need > 0){ const n = Math.min(have, need); me.inv[o.item] -= n; s.prog['deliver:' + i] = (s.prog['deliver:' + i] || 0) + n; line = o.line || `${ITEM[o.item]} ${n}개를 건넸어요`; } } });
  save(); mqCheck(); return line ? fillVars(line) : null; }
// ---- 말 걸기 (World.onNpc 이 'mq:' 머리글자로 불러요) ----
async function mqTalk(id){
  const s = mqState(), q = mqQuest(), c = MQ.cast[id]; if (!c) return;
  if (q && q.client === id){
    if (s.ph === 'pre') return mqPlay(q, s.st, 'request');
    if (s.ph === 'ready') return mqPlay(q, s.st, 'complete');
    const ex = mqOnTalk(id); if (ex) return mqPanel(id, ex);
    const idle = await mqIdle(q.id), set = idle[String(s.st)] || {}, lines = set[s.ph === 'go' ? 'a' : 'b'] || set.a || ['……'];
    return mqPanel(id, lines.map(l => fillVars(l)).join(' '));
  }
  const ex = mqOnTalk(id); if (ex) return mqPanel(id, ex);
  // 끝낸 의뢰인 · 조연
  const dq = MQ.list.map(k => MQ.q[k]).find(x => x && x.client === id && s.done[x.id]);
  if (dq){ const idle = await mqIdle(dq.id), lines = idle.done || ['……']; return mqPanel(id, lines.map(l => fillVars(l)).join(' ')); }
  if (q){ const st = mqStage(), a = (st && st.actors || []).find(x => x.id === id); if (a && a.lines) return mqPanel(id, [].concat(a.lines).map(l => fillVars(l)).join(' ')); }
  mqPanel(id, c.idle ? [].concat(c.idle).map(l => fillVars(l)).join(' ') : '……');
}
function mqFace(id, size = 48){ const c = MQ.cast[id]; if (!c) return ''; if (c.portrait) return `<i class="mqport" style="width:${size}px;height:${size}px;background-image:url(art/portraits/${c.portrait}.png?v=${PORTRAIT_V})"></i>`; return c.av ? `<img src="${World.Avatar.head(World.Avatar.fix(c.av))}" alt="">` : c.spr !== undefined ? npcFace(c.spr, size) : ''; }
function mqPanel(id, text, btns = ''){ const c = MQ.cast[id] || {}; npcUI().innerHTML = `<div class="npcp px"><div class="npch"><div class="npcf">${mqFace(id)}</div><div><b>${esc(mqName(id))}</b><span class="s sub">${esc(c.title || '')}</span></div><button class="sx" data-nx="close">✕</button></div><div class="npct">${esc(text)}</div><div class="frow">${btns}<button class="btn sm" data-nx="close">알겠어요</button></div></div>`; npcUI().dataset.id = 'mq:' + id; npcUI().classList.add('on'); }
function mqPanelText(title, text, extra = ''){ npcUI().innerHTML = `<div class="npcp px"><div class="npch"><div class="npcf"><span style="font-size:28px">🔍</span></div><div><b>${esc(title)}</b>${extra}</div><button class="sx" data-nx="close">✕</button></div><div class="npct">${esc(text)}</div><div class="frow"><button class="btn sm" data-nx="close">알겠어요</button></div></div>`; npcUI().dataset.id = 'mq:'; npcUI().classList.add('on'); }
// 서브 NPC와 이야기할 때(npcMenu) 의뢰 목표가 있으면 한마디 더
function mqNpcHook(n){ const ex = mqOnTalk(n.id); return ex; }
// 메인에서 알게 된 사실 뒤의 서브 NPC 평소 대사 추가분 (npc_lines.json: { npc: [{ flag, lines }] })
function mqNpcExtra(id){ const L = MQ.lines[id]; if (!L) return []; return L.filter(x => !x.flag || flagOn(x.flag) || (x.quest && mqState().done[x.quest])).flatMap(x => x.lines || []); }
// ---- 일지 「이야기」 탭 ----
function mqJournalHTML(){
  const s = mqState(), q = mqQuest(), n = mqDoneN(), shards = mqShards();
  const sky = `<div class="mqsky"><div class="mqstars">${[0, 1, 2, 3, 4, 5].map(i => `<i class="${s.done[MQ.list[i]] ? 'on' : ''}" style="left:${[8, 22, 36, 50, 64, 78][i]}%;top:${[55, 30, 50, 25, 45, 20][i]}%"></i>`).join('')}<i class="lantern ${s.done[MQ.list[6]] ? 'on' : ''}" style="left:90%;top:38%"></i></div><div class="main"><span class="t">등불자리</span><span class="d">등불 조각 ${shards} / 6 · 밝아진 별 ${Math.min(6, n)}개${s.done[MQ.list[6]] ? ' · 불씨가 켜졌어요' : ''}</span></div></div>`;
  const past = MQ.list.filter(id => s.done[id]).map(id => { const P = MQ.q[id]; return `<button class="tag jn-past" data-mqre="${id}">${P.order}. ${esc(P.name)} ✔</button>`; }).join('');
  if (!q){ const nextId = MQ.list.find(id => !s.done[id]), nq = nextId && MQ.q[nextId];
    let when = '아직 손님이 오지 않았어요';
    if (nq){ const u = nq.unlock || {}; const base = u.afterQuest ? s.done[u.afterQuest] : 0; const d = (base || 0) + (u.daysAfter || 0) - me.day;
      when = n >= 7 ? '일곱 등불의 의뢰를 모두 끝냈어요' : u.afterFestival && !(s.sawFull && moonNow() !== 'full') ? '호박달 축제가 지나면 마지막 손님이 와요' : d > 0 ? `${d}일 뒤 아침에 다음 손님이 와요` : '곧 다음 손님이 학교에 와요'; }
    return `<section class="sec">${secH('메인 이야기', n ? `${n} / 7 의뢰` : '')}${sky}<div class="hint ${nq ? 'on' : ''}">${when}</div>${past ? `<div class="jn-tags">${past}</div>` : ''}${n >= 7 ? '<div class="hint on">등불자리 옆에, 처음 보는 희미한 별 하나가 떠 있어요……</div>' : ''}</section>`; }
  const c = mqClient(q), st = mqStage(), objs = mqObjs();
  const head = `<div class="jn-npc"><div class="npcf">${mqFace(q.client)}</div><div class="main"><b>${q.order}. ${esc(q.name)}</b><span class="d">${esc(mqName(q.client))} · ${esc(c.title || '')} · ${s.st} / 5 단계</span></div></div>`;
  const body = s.ph === 'arrive' ? '<div class="hint on">손님이 학교로 오고 있어요. 마을로 나가 보세요</div>'
    : s.ph === 'pre' ? `<div class="hint on">${esc(mqName(q.client))}에게 말을 걸면 ${s.st}단계 부탁을 들어요</div><button class="btn go" data-mqgo="client">${esc(mqName(q.client))}에게 가기</button>`
    : `<div class="box px">${objs.map((o, i) => { const z = mqObjState(o, i); const act = o.type === 'puzzle' && !z.done ? `<button class="btn sm go" data-mqpz="${i}">풀기</button>` : o.type === 'defend' && !z.done ? `<button class="btn sm go" data-mqdf="${i}">시작</button>` : o.type === 'craft' && !z.done ? `<button class="btn sm" data-mqcraft="${o.place || 'lab'}">만들러</button>` : (o.hint_location || o.place || o.where) && !z.done ? `<button class="btn sm" data-mqgo="${o.hint_location || o.place || o.where}">가기</button>` : z.done ? '<span class="tag">완료</span>' : '';
        return `<div class="li ${z.done ? 'done' : ''}"><span class="gic">${z.done ? '✅' : { collect: '🧺', craft: '⚗️', deliver: '🎁', visit: '🚶', talk: '💬', clue: '🔍', puzzle: '🧩', wait_moon: '🌙', defend: '🏮', choice: '💭' }[o.type] || '•'}</span><div class="main"><span class="t">${esc(z.text)}${z.need > 1 ? ` <span class="num">${z.cur} / ${z.need}</span>` : ''}</span>${z.hint ? `<span class="d">${esc(z.hint)}</span>` : ''}</div>${act}</div>`; }).join('')}</div>
      ${s.ph === 'ready' ? `<div class="hint on">목표를 다 했어요. ${esc(mqName(q.client))}에게 알려요</div><button class="btn go" data-mqgo="client">${esc(mqName(q.client))}에게 가기</button>` : s.dl ? `<div class="hint">기한: ${s.dl - me.day}일 남음</div>` : ''}`;
  return `<section class="sec">${secH('메인 이야기', `${s.st}단계 · ${esc(st?.title || '')}`)}<div class="box px jn-card">${head}${body}</div>${sky}${past ? `<div class="jn-tags">${past}</div>` : ''}</section>`;
}
function mqJournalBind(){
  on('[data-mqgo]', b => { const k = b.dataset.mqgo; closeSheet(); if (k === 'client'){ const q = mqQuest(); const p = mqPlace((mqStage() && mqStage().place) || q.place); if (p) goPlace(p.map, [p.x, p.y]); return; } const p = NL.places[k]; if (p) goPlace(p.map, [p.x, p.y]); });
  on('[data-mqpz]', b => { mqPz = +b.dataset.mqpz; openSheet('home', 'mqpuzzle'); });
  on('[data-mqdf]', b => { const i = +b.dataset.mqdf; closeSheet(); mqDefend(i); });
  on('[data-mqcraft]', b => { mqCraftPlace = b.dataset.mqcraft; openSheet('home', 'mqcraft'); });
  on('[data-mqre]', async b => { const q = MQ.q[b.dataset.mqre]; closeSheet(); mqReplay(q); });
}
async function mqReplay(q){ const picks = []; for (let n = 1; n <= 5; n++){ picks.push([n, 'request']); picks.push([n, 'complete']); }
  mqPanel(q.client, `「${q.name}」 어느 장면을 다시 볼까요?`, picks.map(([n, k]) => `<button class="btn sm" data-mqrp="${q.id},${n},${k}">${n}단계 ${k === 'request' ? '부탁' : '완료'}</button>`).join('')); }
document.addEventListener('click', e => { const b = e.target.closest('[data-mqrp]'); if (!b) return; const [id, n, k] = b.dataset.mqrp.split(','); npcClose(); mqScene(id, +n, k).then(sc => { if (sc) mqPlay(MQ.q[id], +n, k, { ...sc, replay: true }); }); });
// ---- 의뢰 제조 (물약 교실 솥 · 과자 교실 오븐): 단계마다 때맞춰 누르기 → 품질 ----
let mqCraftPlace = 'lab', mqCraftSel = null, mqCraftRun = null;
function mqRecipes(){ const q = mqQuest(); if (!q) return []; const st = mqStage(); const ids = new Set((st && st.objectives || []).filter(o => o.type === 'craft').map(o => o.item)); return (q.recipes || []).filter(r => ids.has(r.id) && (r.place || 'lab') === mqCraftPlace); }
function renderMqCraft(){
  const R = mqRecipes(), r = R.find(x => x.id === mqCraftSel) || R[0]; mqCraftSel = r && r.id;
  const can = r && Object.entries(r.mats || {}).every(([k, n]) => (me.inv[k] || 0) >= n) && me.mana >= (r.mana || 0);
  const run = mqCraftRun;
  frame(null, '의뢰 제조', mqCraftPlace === 'candy' ? '과자 교실 오븐' : '물약 교실 솥', !R.length ? '<div class="hint on">지금 만들 의뢰 물건이 없어요</div>' : `
    <div class="seg scroll">${R.map(x => `<button data-mqr="${x.id}" class="${x.id === mqCraftSel ? 'on' : ''}">${esc(x.name || ITEM[x.id])}</button>`).join('')}</div>
    <div class="box px"><div class="li"><span class="gic">⚗️</span><div class="main"><span class="t">${esc(r.name || ITEM[r.id])}</span><span class="d">${esc(r.desc || '')}</span></div></div>
      ${Object.entries(r.mats || {}).map(([k, n]) => `<div class="li"><span class="gic">${ic(k)}</span><div class="main"><span class="t">${esc(ITEM[k] || k)} ${n}개</span><span class="d">가진 것 ${me.inv[k] || 0}개</span></div>${(me.inv[k] || 0) >= n ? '<span class="tag">✓</span>' : ''}</div>`).join('')}
      ${r.mana ? `<div class="li"><span class="gic">✨</span><div class="main"><span class="t">마력 ${r.mana}</span><span class="d">지금 ${me.mana}</span></div></div>` : ''}</div>
    ${run ? `<div class="mqbar"><div class="mqtrack"><i class="zone" style="left:${run.z0}%;width:${run.zw}%"></i><i class="pin" id="mqpin"></i></div><div class="s">단계 ${run.k + 1} / ${run.steps} · 초록 칸에서 「지금!」 · 맞힌 ${run.hit}</div><button class="btn go" id="mqhit">지금!</button></div>`
      : `<div class="hint">${r.steps > 1 ? `${r.steps}단계로 만들어요. 단계마다 움직이는 점이 초록 칸에 들어왔을 때 눌러요. 다 맞히면 품질 「최고」, 절반 넘게 맞히면 「좋음」` : '움직이는 점이 초록 칸에 들어왔을 때 눌러요'}</div><button class="btn go" id="mqstart" ${can ? '' : 'disabled'}>${can ? '만들기 시작' : '재료나 마력이 모자라요'}</button>`}`);
  on('[data-mqr]', b => { mqCraftSel = b.dataset.mqr; mqCraftRun = null; render(); });
  const st = $('#mqstart'); if (st) st.onclick = () => { Object.entries(r.mats || {}).forEach(([k, n]) => me.inv[k] -= n); me.mana -= (r.mana || 0); save(); hud(); mqCraftRun = { steps: r.steps || 1, k: 0, hit: 0, z0: 35 + Math.random() * 30, zw: 18, t0: performance.now(), sp: 1.1 + (r.steps || 1) * .15 }; render(); mqCraftAnim(); };
  const ht = $('#mqhit'); if (ht) ht.onclick = () => { const p = mqPinPos(); const ok = p >= run.z0 && p <= run.z0 + run.zw; if (ok){ run.hit++; sfx('pop'); } else sfx('gulp'); run.k++;
    if (run.k >= run.steps){ const q = run.hit >= run.steps ? 'best' : run.hit * 2 >= run.steps ? 'good' : 'normal'; mqCraftRun = null; mqGive(r.id, 1); me.mqQ = me.mqQ || {}; me.mqQ[r.id] = Math.max(MQ_QN[me.mqQ[r.id] || 'normal'] >= MQ_QN[q] ? MQ_QN[me.mqQ[r.id] || 'normal'] : MQ_QN[q]); mqOnCraft(r.id, q); save(); sfx('magic'); toast(`${ITEM[r.id]} 완성 · 품질 ${MQ_Q[q]}`); render(); }
    else { run.z0 = 25 + Math.random() * 45; run.t0 = performance.now(); render(); mqCraftAnim(); } };
}
const mqPinPos = () => { const r = mqCraftRun; if (!r) return 0; const t = (performance.now() - r.t0) / 1000 * r.sp; return (1 - Math.abs((t % 2) - 1)) * 100; };
function mqCraftAnim(){ const pin = $('#mqpin'); if (!pin || !mqCraftRun) return; pin.style.left = mqPinPos() + '%'; requestAnimationFrame(mqCraftAnim); }
// ---- 퍼즐: 별자리 잇기 · 순서 맞추기 ----
let mqPz = 0, mqPzPick = [];
function renderMqPuzzle(){
  const o = mqObjs()[mqPz]; if (!o || o.type !== 'puzzle') return closeSheet();
  const s = mqState();
  if (o.kind === 'stars'){
    const pts = o.stars || [[12, 20], [30, 12], [50, 18], [66, 10], [80, 26], [60, 44], [40, 62], [22, 78], [70, 70]], n = o.count || 7, order = o.order || pts.slice(0, n).map((_, i) => i);
    const next = order[mqPzPick.length];
    frame(null, o.title || '별자리 잇기', o.sub || `별 ${n}개를 순서대로 눌러요`, `<div class="hint ${o.hintText ? 'on' : ''}">${esc(o.hintText || '첫 별부터 차례로. 틀리면 처음부터예요')}</div>
      <div class="mqstarbox">${pts.map((p, i) => { const k = mqPzPick.indexOf(i); return `<button class="mqstar ${k >= 0 ? 'on' : ''} ${i === next && o.showNext !== false ? 'next' : ''}" style="left:${p[0]}%;top:${p[1]}%" data-mqs="${i}" aria-label="별 ${i + 1}">${k >= 0 ? k + 1 : ''}</button>`; }).join('')}
        <svg class="mqlines" viewBox="0 0 100 100" preserveAspectRatio="none">${mqPzPick.slice(1).map((i, j) => `<line x1="${pts[mqPzPick[j]][0]}" y1="${pts[mqPzPick[j]][1]}" x2="${pts[i][0]}" y2="${pts[i][1]}"/>`).join('')}</svg></div>
      <div class="s" style="text-align:center">${mqPzPick.length} / ${n}</div><button class="btn" id="mqpzreset">처음부터</button>`);
    on('[data-mqs]', b => { const i = +b.dataset.mqs; if (mqPzPick.includes(i)) return; if (i === order[mqPzPick.length]){ mqPzPick.push(i); sfx('sparkle'); if (mqPzPick.length >= n){ s.prog['puzzle:' + mqPz] = 1; save(); sfx('magic'); toast(o.doneText || '별자리가 이어졌어요!'); mqPzPick = []; mqCheck(); jnTab = 'story'; return openSheet('home', 'journal'); } } else { mqPzPick = []; sfx('gulp'); toast('그 별이 아니에요. 처음부터!'); } render(); });
    $('#mqpzreset').onclick = () => { mqPzPick = []; render(); };
  } else {
    const items = o.items || [], ans = o.answer || items.map((_, i) => i);
    frame(null, o.title || '순서 맞추기', o.sub || '차례대로 눌러요', `<div class="hint ${o.hintText ? 'on' : ''}">${esc(o.hintText || '맞는 순서로 하나씩 골라요')}</div>
      <div class="tiles">${items.map((t, i) => { const k = mqPzPick.indexOf(i); return `<button class="tile ${k >= 0 ? 'sel' : ''}" data-mqo="${i}" ${k >= 0 ? 'disabled' : ''}><span class="main"><span class="b">${k >= 0 ? k + 1 + '. ' : ''}${esc(t)}</span></span></button>`; }).join('')}</div>
      <div class="s" style="text-align:center">${mqPzPick.length} / ${items.length}</div><button class="btn" id="mqpzreset">처음부터</button>`);
    on('[data-mqo]', b => { const i = +b.dataset.mqo; if (i === ans[mqPzPick.length]){ mqPzPick.push(i); sfx('pop'); if (mqPzPick.length >= items.length){ s.prog['puzzle:' + mqPz] = 1; save(); sfx('magic'); toast(o.doneText || '순서를 맞췄어요!'); mqPzPick = []; mqCheck(); jnTab = 'story'; return openSheet('home', 'journal'); } } else { mqPzPick = []; sfx('gulp'); toast('순서가 달라요. 처음부터!'); } render(); });
    $('#mqpzreset').onclick = () => { mqPzPick = []; render(); };
  }
}
// ---- 지키기: 등불을 향해 오는 바람·그림자를 눌러 흩어요. 제한 시간을 버티면 성공 ----
function mqDefend(i){
  const o = mqObjs()[i]; if (!o || o.type !== 'defend') return; const s = mqState();
  if (o.place){ const p = NL.places[o.place]; const m = World.myPos && World.myPos(); if (p && (World.where() !== p.map || Math.hypot(m.x - p.x, m.y - p.y) > (p.r || 2) + 3)) return toast(`${fillVars(p.name)}에서 시작해요`); }
  const sec = o.sec || 30, ov = document.createElement('div'); ov.id = 'mqdef'; ov.className = 'px';
  ov.innerHTML = `<div class="mqdhud"><b>${esc(o.text || '등불 지키기')}</b><span class="num" id="mqdt">${sec}</span></div><div class="mqdmeter"><i id="mqdf" style="width:100%"></i></div><div class="mqdstage" id="mqds"><div class="mqlamp" id="mqlamp">🏮</div></div><div class="s mqdhint">${esc(o.hintText || '등불 쪽으로 오는 바람을 눌러서 흩어요')}</div>`;
  $('#stage').appendChild(ov); sfx('wind');
  let flame = 100, t0 = performance.now(), last = t0, spawnAt = 0, gusts = [], over = false;
  const stg = ov.querySelector('#mqds'), lamp = ov.querySelector('#mqlamp');
  const end = ok => { if (over) return; over = true; gusts.forEach(g => g.el.remove()); ov.remove(); if (ok){ s.prog['defend:' + i] = 1; save(); sfx('magic'); toast(o.doneText || '등불을 지켰어요!'); mqCheck(); } else { sfx('thunder'); toast('등불이 꺼졌어요…… 다시 해 봐요'); } };
  const tick = now => { if (over) return; const dt = (now - last) / 1000; last = now; const el = (now - t0) / 1000, left = Math.max(0, sec - el); ov.querySelector('#mqdt').textContent = Math.ceil(left);
    if (now > spawnAt){ spawnAt = now + Math.max(500, 1500 - el * 25); const g = document.createElement('button'); g.className = 'mqgust'; g.textContent = ['🌬️', '🌫️', '👻', '🍂'][Math.floor(Math.random() * 4)]; const ang = Math.random() * Math.PI * 2; const r = 1.1; g.ax = .5 + Math.cos(ang) * r; g.ay = .5 + Math.sin(ang) * r; g.sp = (.12 + Math.random() * .08) * (1 + el / sec); stg.appendChild(g); const G = { el: g, x: g.ax, y: g.ay }; gusts.push(G); g.onclick = e => { e.stopPropagation(); G.dead = true; g.remove(); sfx('pop'); }; g.onpointerdown = g.onclick; }
    gusts.forEach(G => { if (G.dead) return; const dx = .5 - G.x, dy = .5 - G.y, d = Math.hypot(dx, dy) || 1; G.x += dx / d * G.sp * dt; G.y += dy / d * G.sp * dt; G.el.style.left = G.x * 100 + '%'; G.el.style.top = G.y * 100 + '%'; if (d < .06){ G.dead = true; G.el.remove(); flame -= o.hitDamage || 18; lamp.classList.add('hit'); setTimeout(() => lamp.classList.remove('hit'), 300); sfx('gulp'); } });
    gusts = gusts.filter(G => !G.dead); ov.querySelector('#mqdf').style.width = Math.max(0, flame) + '%';
    if (flame <= 0) return end(false); if (left <= 0) return end(true); requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
}
// ---- 상황 버튼: 솥·오븐 옆에서 「의뢰 제조」 ----
function mqCtxExtra(t){ const s = mqState(); if (!s.q || s.ph !== 'go' || !t || t.kind !== 'act') return ''; const nm = t.o && t.o.name; const pl = nm === 'cauldron' ? 'lab' : (nm === 'oven' || nm === 'stove') ? 'candy' : null; if (!pl) return ''; mqCraftPlace = pl; return mqRecipes().length ? `<button data-ctx="mqcraft">⚗️ 의뢰 제조</button>` : ''; }
// ---- 가방 「중요」 탭 항목 ----
function mqBagKeys(){ return Object.keys(MQ.items).filter(k => MQ.items[k].key && me.inv[k] > 0).map(k => ({ id: k, kind: 'inv', n: me.inv[k], name: ITEM[k], ico: mqIc(k) })); }
const mqIc = k => { const it = MQ.items[k]; return it && it.emoji ? `<i class="ic mqic">${it.emoji}</i>` : ic(k); };
// ---- 시험용 손잡이 ----
window.__mq = { state: () => mqState(), set: (q, st, ph) => { const s = mqState(); s.q = q; s.st = st || 1; s.ph = ph || 'pre'; s.prog = {}; save(); syncNpcs(); mqMarks(); }, done: q => { const s = mqState(); s.done[q] = me.day; save(); mqSky(); }, play: (q, n, k) => mqPlay(MQ.q[q], n, k), tick: () => mqTick(), check: () => mqCheck(), moon: m => { if (m) localStorage.setItem('magion-moon', m); else localStorage.removeItem('magion-moon'); }, MQ };
// ----- /메인 의뢰 -----
