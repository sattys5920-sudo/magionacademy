// 새 직업 스킬 이펙트 영상: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/newjobs/fx_run2.js [포트]
//   → tools/newjobs/fx/<직업>.mp4 (직업마다 스킬 전부) · fx/sheet_<직업>.png
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process'); const R = __dirname + '/../..', PORT = process.argv[2] || 8822;
const SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_' + PORT + '/site', OUT = __dirname + '/fx', ONLY = process.argv[3];
fs.mkdirSync(SITE + '/__newjobs', { recursive: true }); fs.mkdirSync(OUT, { recursive: true });
fs.copyFileSync(__dirname + '/weapons_new.png', SITE + '/__newjobs/weapons_new.png'); fs.copyFileSync(__dirname + '/xw_new.json', SITE + '/__newjobs/xw_new.json'); fs.copyFileSync(R + '/public/xfx2.js', SITE + '/xfx2.js');
// skills_plan.md 읽기: 직업 → [{ n 이름, t 종류, b 줄기 }]
const KEY = { 성기사: 'paladin', 수호자: 'guardian', 암흑기사: 'darkknight', 무희: 'dancer', 현자: 'sage', 주술사: 'shaman', 무녀: 'miko', 궁수: 'archer', 총잡이: 'gunner', 정령술사: 'elemental', 격투가: 'fighter', 검무사: 'bladedancer' };
const PLAN = {}; let cur = null, br = null;
for (const ln of fs.readFileSync(__dirname + '/skills_plan.md', 'utf8').split('\n')){
  const h = ln.match(/^## (\S+) \(/); if (h){ cur = KEY[h[1]]; br = null; if (cur) PLAN[cur] = []; continue; }
  if (!cur || !ln.startsWith('|') || ln.startsWith('|---')) continue; const cells = ln.split('|').slice(1, -1).map(s => s.trim());
  if (!br){ br = cells; continue; } cells.forEach((cl, i) => { const m = cl.match(/^(.+?) \((.+)\)$/); if (m) PLAN[cur].push({ n: m[1], t: m[2], b: br[i], i }); });
}
Object.values(PLAN).forEach(a => a.sort((x, y) => x.i - y.i));
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
(async () => {
  const b = await chromium.launch(); const errs = [], miss = [];
  for (const [jk, list] of Object.entries(PLAN)){
    if (ONLY && ONLY !== jk) continue;
    const ctx = await b.newContext({ viewport: { width: 768, height: 432 }, recordVideo: { dir: OUT + '/vid', size: { width: 768, height: 432 } } }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.World && World.Avatar && window.XFXJOB, null, { timeout: 30000 }); await p.waitForTimeout(2500);
    await p.addScriptTag({ path: __dirname + '/fx_mock.js' }); await p.addScriptTag({ path: __dirname + '/../../public/xfx3.js' }); await p.evaluate(() => __nj.load());
    await p.evaluate(() => { const c = document.createElement('canvas'); c.id = 'njv'; c.width = __nj.W; c.height = __nj.H; c.style.cssText = 'position:fixed;inset:0;width:768px;height:432px;z-index:99999;image-rendering:pixelated;background:#000'; document.body.appendChild(c); });
    const t0 = Date.now();
    const r = await p.evaluate(async ({ jk, list }) => {
      const { JOBS, scene } = __nj, X = XFXJOB, Jb = JOBS.find(j => j.k === jk), c = document.getElementById('njv'), g = c.getContext('2d'), miss = [];
      const E = [[278, 176], [318, 158], [326, 196]], A = [[118, 178], [72, 158], [62, 194]];
      const tg = t => /부활/.test(t) ? [A[2]] : /^나 |도발/.test(t) ? [A[0]] : /^아군|광역 회복|마력 회복/.test(t) ? A : /단일 회복/.test(t) ? [A[1]] : /광역 공격|적 전체|^적 느리게/.test(t) ? E : [E[0]];
      const label = (s, s2, col) => { g.fillStyle = '#100c1c'; g.globalAlpha = .85; g.fillRect(0, 0, 384, 36); g.globalAlpha = 1; g.font = '11px G11B, Pretendard, sans-serif'; g.textAlign = 'left'; g.fillStyle = col; g.fillText(s, 8, 15); g.fillStyle = '#c8c0e0'; g.font = '9px G11B, Pretendard, sans-serif'; g.fillText(s2, 8, 29); };
      await scene(c, Jb, -1, 0); label(`${Jb.n} · ${Jb.r}`, '스킬 ' + list.length + ' 개', Jb.c); await new Promise(r => setTimeout(r, 900));
      const shots = [];
      for (const s of list){
        const key = jk + '.' + s.n, m = X.T2[key];
        if (/패시브/.test(s.t)){ continue; }
        if (!m){ miss.push(s.n); continue; }
        const T = m.once || m.g && tg(s.t).length > 1 ? [tg(s.t)[0]] : tg(s.t), st = performance.now(), dur = m.d, F = T.map((P, n) => ({ k: 'sk:' + key, t0: st + n * 70, dur, seed: 3 + n, n }));
        let snapped = false;
        while (performance.now() - st < dur + 350){ const now = performance.now(); await scene(c, Jb, -1, 0); F.forEach((f, n) => X.drawSk(g, f, T[n][0], T[n][1], now)); label(`${Jb.n} · ${s.n}`, `${s.b} · ${s.t}`, Jb.c);
          if (!snapped && now - st > dur * (m.g ? .5 : .42)){ snapped = true; shots.push(c.toDataURL()); } await new Promise(r => requestAnimationFrame(r)); }
      }
      await scene(c, Jb, -1, 0); label(`${Jb.n}`, '끝', Jb.c); await new Promise(r => setTimeout(r, 500));
      // 한 장: 스킬 순간 모음 (4 열)
      const cols = 4, rows = Math.ceil(shots.length / cols), sh = document.createElement('canvas'); sh.width = cols * 388; sh.height = rows * 220; const o = sh.getContext('2d'); o.fillStyle = '#100c1c'; o.fillRect(0, 0, sh.width, sh.height);
      for (let i = 0; i < shots.length; i++){ const im = new Image(); await new Promise(r => { im.onload = r; im.src = shots[i]; }); o.drawImage(im, (i % cols) * 388 + 2, Math.floor(i / cols) * 220 + 2); }
      return { miss, sheet: sh.toDataURL(), n: shots.length };
    }, { jk, list });
    fs.writeFileSync(`${OUT}/sheet_${jk}.png`, Buffer.from(r.sheet.split(',')[1], 'base64')); miss.push(...r.miss.map(n => jk + '.' + n));
    const v = p.video(); await ctx.close(); const src = await v.path(); const pre = ((Date.now() - t0) / 1000);
    const total = Number(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${src}"`).toString()); const ss = Math.max(0, total - pre).toFixed(2);
    execSync(`ffmpeg -loglevel error -y -ss ${ss} -i "${src}" -c:v libx264 -pix_fmt yuv420p -crf 24 -movflags +faststart "${OUT}/${jk}.mp4"`); fs.rmSync(src, { force: true });
    console.log(jk, r.n, 'skills', pre.toFixed(1) + 's');
  }
  await b.close(); fs.rmSync(OUT + '/vid', { recursive: true, force: true });
  console.log('miss', JSON.stringify(miss), 'errs', JSON.stringify(errs.slice(0, 5)));
})();
