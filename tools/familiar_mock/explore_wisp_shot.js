const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs');
const spec = fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8'); const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const MODE = process.argv[2] || 'none';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('err', e.message));
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto('http://localhost:8792/'); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const r = await p.evaluate(async (MODE) => {
    const me = __T.me(); const t = Date.now();
    me.ex = { exp: 20000, job: 'warrior', d: '', n: 0, xv: 3, run: { rg: 0, mod: null, start: t, end: t + 3600000, prog: 30, loot: { gold: 0, exp: 0, items: {} }, buff: 0, p: null, node: null } };
    __T.openSheet('home', 'explore'); await new Promise(r => setTimeout(r, 400));
    const RR = me.ex.run; if (!RR) return 'norun'; window.__dbg = JSON.stringify({pool: RR.pool, rg: RR.rg, keys: Object.keys(RR)}); RR.pool = [{ n: '숲 요정', lp: 17, hp: 32, atk: 8, spd: 13 }, { n: '들토끼', lp: 18, hp: 34, atk: 7, spd: 11 }, { n: '잠자리 도깨비', lp: 19, hp: 30, atk: 8, spd: 12 }]; RR.nextMon = null; try { __T.xSB('normal'); } catch (e) { return window.__dbg + ' ' + e.stack.slice(0, 300); } await new Promise(r => setTimeout(r, 400));
    const B = __T.xbGet(); const base = B.party[0]; const npcs = ['nabi', 'mandi', 'stella'];
    for (let i = 0; i < 3; i++){ const c = JSON.parse(JSON.stringify(base)); c.id = 'p' + i; c.name = ['하나', '두리', '세리'][i]; c.hum = false; try { c.av = __T.npcAvOf(npcs[i]) || c.av; } catch (e) {} B.party.push(c); }
    B.party.forEach((u, i) => u.row = i < 2 ? 'f' : 'b');
    __T.xLayout_(B);
    const IMG = new Image(); IMG.src = 'wisps3_anim.png'; await new Promise(r => IMG.onload = r);
    const rows = [0, 6, 9, 10];
    if (MODE !== 'none') window.__wispBack = (g, B, now) => { B.party.forEach((u, i) => { if (u.hp <= 0) return; const f = Math.floor(now / 110) % 8, sz = 22, bob = Math.sin(now / 400 + i) * 1.5;
      const x = MODE === 'behind' ? u.bx - 20 : u.bx - 4, y = MODE === 'behind' ? u.by - 30 + bob : u.by - 62 + bob;
      g.save(); g.globalCompositeOperation = 'lighter'; const rg = g.createRadialGradient(x, y, 0, x, y, 14); rg.addColorStop(0, 'rgba(120,160,255,.35)'); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.fillRect(x - 14, y - 14, 28, 28); g.restore();
      g.drawImage(IMG, f * 64, rows[i] * 64, 64, 64, Math.round(x - sz / 2), Math.round(y - sz * .62), sz, sz); }); };
    return B.party.map(u => [u.bx, u.by, u.row]);
  }, MODE);
  console.log(JSON.stringify(r));
  await p.waitForTimeout(1200);
  const cv = await p.$('#xcv'); await (cv || p).screenshot({ path: '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/x_' + MODE + '.png' });
  await b.close();
})();
