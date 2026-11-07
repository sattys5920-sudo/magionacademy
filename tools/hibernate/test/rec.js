// 겨울잠 준비 연출 영상: node rec.js start|sleep|end → vid/<이름>.webm + 앞부분 자를 초 (stdout)
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const { mkSeed } = require('./common.js'); const fs = require('fs');
const WHO = process.argv[2], OUT = __dirname + '/vid';
(async () => {
  const seed = mkSeed(), me = seed.players.me1; me.babySeen = 'x';
  me.inv = { ...me.inv, g2_acorn: 8, g2_frostleaf: 4, g2_reed: 4 };
  if (WHO === 'start') seed.hib = { ctl: { open: true, id: 111, at: 1 } };
  if (WHO === 'sleep'){ seed.hib = { ctl: { open: true, id: 111, at: 1 }, den: { dormouse: { f: 78, b: 40 } }, give: { dormouse: { me1: 6, me2: 20, me3: 2, u4: 1 } } }; me.hib = { ev: 111, hi: 1, seen: {}, gift: {}, rw: { tag: 1 } }; }
  if (WHO === 'end'){ const t = Date.now() - 3600e3, den = {}; ['dormouse', 'badger', 'turtle', 'salamander', 'ladybug'].forEach(a => den[a] = { f: 80, b: 40, slept: t }); den.bear = { f: 160, b: 78 };
    seed.hib = { ctl: { open: true, id: 111, at: 1 }, den }; me.hib = { ev: 111, hi: 1, seen: { dormouse: 1, badger: 1, turtle: 1, salamander: 1, ladybug: 1 }, gift: { dormouse: 1, badger: 1, turtle: 1, salamander: 1, ladybug: 1 }, rw: { tag: 1 } }; }
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const T0 = Date.now(); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(([sd]) => { window.__seed = sd; window.__uid = 'me1'; }, [seed]); await p.goto('http://localhost:8822/'); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  let cut = 0;
  if (WHO === 'start'){
    for (let i = 0; i < 60; i++){ if (await p.evaluate(() => !!(World.cutBusy && World.cutBusy()))) break; await p.waitForTimeout(200); }
    cut = (Date.now() - T0) / 1000 - 1.2;
    for (let i = 0; i < 120; i++){ if (await p.evaluate(() => !!document.getElementById('hibmap'))) break; await p.waitForTimeout(300); }
    await p.waitForTimeout(4000);
  }
  if (WHO === 'sleep'){
    await p.evaluate(() => World.teleport('campus', [45, 100])); await p.waitForTimeout(3000); cut = (Date.now() - T0) / 1000 - 1;
    await p.waitForTimeout(1200); await p.evaluate(() => window.__hib.openWin('dormouse')); await p.waitForTimeout(1500);
    await p.tap('[data-hibk="g2_acorn"]'); await p.waitForTimeout(900); await p.tap('[data-hibx="give"]'); await p.waitForTimeout(1800);
    await p.tap('[data-hibx="close"]').catch(() => {});
    for (let i = 0; i < 40; i++){ if (await p.evaluate(() => !!document.getElementById('hibsc'))) break; await p.waitForTimeout(300); }
    for (let i = 0; i < 60; i++){ if (!(await p.evaluate(() => !!document.getElementById('hibsc')))) break; await p.waitForTimeout(300); }
    await p.waitForTimeout(3500);
  }
  if (WHO === 'end'){
    await p.evaluate(() => World.teleport('campus', [53, 5])); await p.waitForTimeout(3000); cut = (Date.now() - T0) / 1000 - 1;
    await p.waitForTimeout(1000); await p.evaluate(() => window.__hib.openWin('bear')); await p.waitForTimeout(1200);
    await p.tap('[data-hibt="b"]'); await p.waitForTimeout(600); await p.tap('[data-hibk="g2_frostleaf"]'); await p.waitForTimeout(900); await p.tap('[data-hibx="give"]'); await p.waitForTimeout(1800);
    await p.tap('[data-hibx="close"]').catch(() => {});
    for (let i = 0; i < 40; i++){ if (await p.evaluate(() => !!document.getElementById('hibsc'))) break; await p.waitForTimeout(300); }
    for (let i = 0; i < 80; i++){ if (!(await p.evaluate(() => !!document.getElementById('hibsc')))) break; await p.waitForTimeout(300); }
    await p.waitForTimeout(3500);
    await p.evaluate(() => World.teleport('town', [62, 55])); await p.waitForTimeout(4500);
    await p.evaluate(() => { const n = __T.npcGet('batri'); if (n) __T.npcMenu(n); }); await p.waitForTimeout(4500);
  }
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), `${OUT}/${WHO}.webm`); console.log(cut.toFixed(1)); console.error(WHO, 'errs', JSON.stringify(errs)); await b.close(); })();
