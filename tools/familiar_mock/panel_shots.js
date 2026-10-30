// 사역마 창 시안 찍기: node panel_shots.js <포트> <저장 폴더>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8791, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'panel_inject.js'), 'utf8');
const LN = id => { try { return JSON.parse(fs.readFileSync(path.join(__dirname, 'lines', id + '.json'), 'utf8')); } catch (e) { return null; } };
const cu = LN('chungun'), dh = LN('danhwa');
const SHOTS = [
  { f: 'p1_main', cfg: { view: 'main', i: 0, stage: 1, pts: 214, gifts: 2, line: cu ? cu.hint[0].replace('{item}', '달빛 이슬') : '....' } },
  { f: 'p2_gift', cfg: { view: 'gift', i: 0, stage: 1, pts: 239, gifts: 3, giftLine: cu ? cu.gift.want[0] : '....' } },
  { f: 'p3_danhwa', cfg: { view: 'main', i: 6, stage: 3, pts: 1312, gifts: 5, line: dh ? dh.idle[3][0] : '....' } },
  { f: 'p4_list', cfg: { view: 'list', i: 0 } },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const s of SHOTS){
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('err', e.message));
    await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
    await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
    await p.evaluate(c => { window.__famCfg = c; }, s.cfg); await p.addScriptTag({ content: INJ }); await p.waitForTimeout(900);
    await p.screenshot({ path: path.join(OUT, s.f + '.png') }); await p.close();
  }
  await b.close();
})();
