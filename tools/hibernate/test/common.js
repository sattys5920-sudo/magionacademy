const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs');
const spec = fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8');
const mkSeed = () => { const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
  const me = seed.players.me1; me.inv = { ...me.inv, g_wheat: 6, milk: 3, honey: 3, g2_rasp: 2, g2_stardust: 2, g2_pseed: 1 };
  me.npc = { ...me.npc, nabi: { a: 350, seen: { 1: 'ok' } }, kappa: { a: 420 }, sera: { a: 120 } };
  seed.players.me2 = { nick: '서연', look: 3, house: 'dew', coin: 100, mana: 10, day: 2, know: 1, inv: {}, cr: [], eggs: [], orders: [], hints: [], found: [], fdex: {}, rod: 0, closet: {}, fbag: {}, npc: {}, mq: { q: null, st: 1, ph: 'arrive', prog: {}, done: { main_01_dracula: 1, main_02_ghost: 1, main_03_witch: 1, main_04_werewolf: 1, main_05_mummy: 1, main_06_frankenstein: 1, main_07_jack: 1 }, named: {}, dl: null } };
  seed.players.me3 = { ...JSON.parse(JSON.stringify(seed.players.me2)), nick: '하준', house: 'ember' };
  return seed; };
async function boot({ seed, uid = 'me1', force = true, date = null, vp = [430, 860] } = {}){
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage({ viewport: { width: vp[0], height: vp[1] } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await p.addInitScript(([sd, u, f, dt]) => { window.__seed = sd; window.__uid = u; if (f === 'hib') window.__hibForce = true; else if (f) window.__stkForce = true;
    if (dt){ const D = Date, t0 = new D(dt).getTime(), off = t0 - D.now(); window.Date = class extends D { constructor(...a){ super(...(a.length ? a : [D.now() + off])); } static now(){ return D.now() + off; } }; } }, [seed, uid, force, date]);
  await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  return { b, p, errs };
}
module.exports = { boot, mkSeed, fs };
