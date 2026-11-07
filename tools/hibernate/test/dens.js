const { boot, mkSeed } = require('./common.js'); const OUT = '/home/user/magionacademy/tools/hibernate/shots';
(async () => { const seed = mkSeed(); seed.players.me1.babySeen = 'x'; seed.players.me1.hib = { ev: 'force', hi: 1, seen: {}, gift: {}, rw: {} };
  seed.hib = { den: { turtle: { f: 50, b: 10 }, salamander: { f: 50, b: 30 } } };
  const { b, p, errs } = await boot({ seed, force: 'hib' });
  for (const [a, m, x, y] of [['badger', 'campus', 11, 18], ['turtle', 'town', 19, 94], ['salamander', 'town', 18, 88], ['ladybug', 'town', 14, 56], ['bear', 'campus', 52, 4]]){
    await p.evaluate(([m, x, y]) => World.teleport(m, [x + 2, y + 3]), [m, x, y]); await p.waitForTimeout(3000);
    await p.screenshot({ path: OUT + '/den_' + a + '.png', clip: { x: 65, y: 250, width: 300, height: 260 } }); }
  console.log(errs.filter(e => !/404/.test(e))); await b.close(); })();
