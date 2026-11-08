// 밸런스 모의 전투 돌리기: node tools/balance/run_bal.js <작업.js> [포트=8823]
//   모의 사이트를 띄우고 (tools/ui_mock.sh) bal_hook.js 를 큰 module 스크립트 끝에 붙인 뒤, 작업 파일의 module.exports = async (ev, log) => {...} 를 돌려요
//   ev(fn, arg) = page.evaluate(fn, arg) · 페이지에서는 window.__bal 을 써요
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process'); const path = require('path');
const ROOT = path.resolve(__dirname, '../..'), PORT = +(process.argv[3] || 8823);
const out = execSync(`sh ${ROOT}/tools/ui_mock.sh ${ROOT} ${PORT}`).toString(); const site = out.match(/site: (.*)\)/)[1];
{ const f = site + '/index.html', s = fs.readFileSync(f, 'utf8'), i = s.indexOf('<script type="module">'); const end = s.indexOf('</script>', i);
  const hook = fs.readFileSync(__dirname + '/bal_hook.js', 'utf8'); if (!s.includes('window.__bal =')) fs.writeFileSync(f, s.slice(0, end) + '\n' + hook + '\n' + s.slice(end)); }
const seed = eval('(' + fs.readFileSync(ROOT + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});/)[1] + ')');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__bal && window.__T, null, { timeout: 30000 }); await p.waitForTimeout(1500);
  await p.evaluate(() => { window.sfx = () => {}; });
  const job = require(path.resolve(process.argv[2])); await job((fn, arg) => p.evaluate(fn, arg), (...a) => console.log(...a));
  await b.close(); })().catch(e => { console.error(e); process.exit(1); });
