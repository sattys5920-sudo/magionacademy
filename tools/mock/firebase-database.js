const tree = window.__seed || {};
const ls = [];
const parts = p => p.split('/').filter(Boolean);
const getAt = p => parts(p).reduce((o, k) => o == null ? undefined : o[k], tree);
const setAt = (p, v, remote) => { if (!remote && bc) bc.postMessage({ p, v: v === undefined ? null : v }); const ks = parts(p); let o = tree; ks.slice(0, -1).forEach(k => { if (typeof o[k] !== 'object' || !o[k]) o[k] = {}; o = o[k]; }); if (v === null || v === undefined) delete o[ks.at(-1)]; else { const c = fbPrune(JSON.parse(JSON.stringify(v))); if (c === undefined) delete o[ks.at(-1)]; else o[ks.at(-1)] = c; } };
// 진짜 Firebase처럼 빈 배열·빈 객체는 남기지 않아요
function fbPrune(v){ if (!v || typeof v !== 'object') return v; for (const k of Object.keys(v)){ const c = fbPrune(v[k]); if (c === undefined) delete v[k]; else v[k] = c; } if (Array.isArray(v)){ const a = v.filter(x => x !== undefined); return a.length ? a : undefined; } return Object.keys(v).length ? v : undefined; }
const snap = p => { const v = getAt(p); return { exists: () => v !== undefined, val: () => v === undefined ? null : JSON.parse(JSON.stringify(v)) }; };
const bc = typeof BroadcastChannel !== 'undefined' ? new BroadcastChannel('mockdb') : null;   // 같은 브라우저의 다른 창과 DB를 나눠 써요 (협동 시험용)
if (bc) bc.onmessage = e => { setAt(e.data.p, e.data.v, true); notify(e.data.p); };
const notify = p => ls.forEach(l => { if (p.startsWith(l.p) || l.p.startsWith(p)) l.cb(snap(l.p)); });
window.__tree = tree;
export const getDatabase = () => ({});
export const ref = (db, p) => ({ p });
export const query = r => r; export const limitToLast = () => null;
export const get = async r => snap(r.p);
// 진짜 Firebase처럼 저장할 수 없는 값은 거절해요 (이름에 . # $ / [ ] · undefined · NaN)
const fbCheck = (v, path) => { if (v === undefined) throw new Error('mock: undefined at ' + path); if (typeof v === 'number' && !isFinite(v)) throw new Error('mock: NaN at ' + path); if (v && typeof v === 'object') for (const k in v){ if (!k || /[.#$\/\[\]]/.test(k)) throw new Error('mock: invalid key (' + k + ') at ' + path); fbCheck(v[k], path + '/' + k); } };
export const set = async (r, v) => { fbCheck(v, r.p); setAt(r.p, v); notify(r.p); };
export const update = async (r, v) => { Object.entries(v).forEach(([k, x]) => fbCheck(x, r.p + '/' + k)); Object.entries(v).forEach(([k, x]) => setAt(r.p + '/' + k, x)); notify(r.p); };
export const remove = async r => { setAt(r.p, null); notify(r.p); };
let n = 0; export const push = async (r, v) => { const id = 'k' + (++n); setAt(r.p + '/' + id, v); notify(r.p); return { key: id }; };
export const onValue = (r, cb) => { const l = { p: r.p, cb }; ls.push(l); setTimeout(() => cb(snap(r.p)), 0); return () => ls.splice(ls.indexOf(l), 1); };
export const onDisconnect = () => ({ remove() {} });
export const runTransaction = async (r, fn) => { const v = fn(getAt(r.p)); if (v === undefined) return { committed: false }; fbCheck(v, r.p); setAt(r.p, v); notify(r.p); return { committed: true }; };
