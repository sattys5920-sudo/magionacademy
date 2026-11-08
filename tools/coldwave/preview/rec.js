// 「양호실 겨울 감기」 미리 보기 영상: node rec.js intro|treat|ending → vid/<이름>.webm (모의 서버 8822 위에서)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const WHO = process.argv[2], OUT = __dirname + '/vid', SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_8822/site';
// 모의 사이트에 미리 보기 코드 · 그림 넣기
let html = fs.readFileSync(SITE + '/index.html', 'utf8'); if (!html.includes('__coldPv')){ html = html.replace('function rdShowBattle(){', fs.readFileSync(__dirname + '/pv.js', 'utf8') + '\nfunction rdShowBattle(){'); fs.writeFileSync(SITE + '/index.html', html); }
let wj = fs.readFileSync(SITE + '/world.js', 'utf8'); if (!wj.includes('__people')){ wj = wj.replace(/^const people = \[\];/m, 'const people = []; window.__people = people;'); fs.writeFileSync(SITE + '/world.js', wj); }
fs.mkdirSync(SITE + '/art/cold', { recursive: true }); const AO = path.join(__dirname, '../out'); fs.readdirSync(AO).filter(f => f.endsWith('.png')).forEach(f => fs.copyFileSync(path.join(AO, f), SITE + '/art/cold/' + f));
const seed = eval('(' + fs.readFileSync('/home/user/magionacademy/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => {
  const me = seed.players.me1; me.babySeen = 'x';
  const b = await chromium.launch(); fs.mkdirSync(OUT, { recursive: true });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, recordVideo: { dir: OUT, size: { width: 390, height: 844 } } });
  const T0 = Date.now(); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(([sd, dt]) => { window.__seed = sd; window.__uid = 'me1'; const D = Date, off = new D(dt).getTime() - D.now(); window.Date = class extends D { constructor(...a){ super(...(a.length ? a : [D.now() + off])); } static now(){ return D.now() + off; } }; }, [seed, '2026-12-02T14:20:00+09:00']);
  await p.goto('http://localhost:8822/'); await p.waitForTimeout(4000);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  const go = async (m, x, y) => { await p.evaluate(([m, x, y]) => World.teleport(m, [x, y]), [m, x, y]); await p.waitForTimeout(2600); };
  let cut = 0;
  if (WHO === 'intro'){ await go('campus', 46, 40); cut = (Date.now() - T0) / 1000 - .5; console.error(await p.evaluate(() => window.__coldPv.intro().then(r => r || 'ok'))); }
  if (WHO === 'treat' || WHO === 'ending'){
    const id = WHO === 'treat' ? 'leo' : 'sera';
    const loc = await p.evaluate(id => { const n = (window.__people || []).find(q => q.npc && q.npc.id === id); return n ? null : __T.npcGet(id) && [__T.npcGet(id).map, __T.npcGet(id).x, __T.npcGet(id).y]; }, id);
    if (loc) await go(loc[0], loc[1] + 2, loc[2]);
    console.error('where', await p.evaluate(id => { const n = (window.__people || []).find(q => q.npc && q.npc.id === id); return World.where() + ' ' + (n ? [n.x, n.y] : 'none'); }, id));
    cut = (Date.now() - T0) / 1000 - .5; console.error(await p.evaluate(w => window.__coldPv[w]().then(r => r || 'ok'), WHO));
  }
  await p.waitForTimeout(800);
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), `${OUT}/${WHO}.webm`); console.log(cut.toFixed(1)); console.error(WHO, 'errs', JSON.stringify(errs)); await b.close(); })();
