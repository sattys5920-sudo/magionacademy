// 시안 찍기: node follow_shots.js <포트> <저장 폴더>  (먼저 tools/ui_mock.sh 로 띄우고 world.js 에 World.__cam, wisps3.png 를 넣어요)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8791, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'follow_inject.js'), 'utf8');
const SHOTS = [
  { f: 'f1_walk', i: 0, col: '#5A8CFF', walk: [3, 2] },
  { f: 'f2_talk', i: 0, col: '#5A8CFF', say: '이 근처.... 마력이 고여 있어요.......' },
  { f: 'f3_night', i: 9, col: '#6A7CFF', night: 1, walk: [-3, 2], say: '별이 많은 밤엔.... 나도 조금 더 밝아져요.......' },
  { f: 'f4_shadow', i: 10, col: '#8A5AE0', night: 1, say: '....조용히. 누가 지켜보고 있어요.......' },
  { f: 'f5_ring', i: 8, col: '#FF8A30', say: '오늘은 따뜻한 쪽으로 가 봐요.......' },
  { f: 'f6_rain', i: 11, col: '#C8B8FF', walk: [-3, -2] },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const s of SHOTS){
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('err', e.message));
    await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
    await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
    await p.evaluate(s => { if (s.night){ World.kNow = () => new Date(2026, 9, 30, 22, 10); } }, s);
    await p.evaluate(() => { World.zoomStep(-1); });
    await p.addScriptTag({ content: INJ });
    await p.evaluate(s => { __wisp.i = s.i; __wisp.col = s.col; }, s);
    await p.waitForTimeout(1500);
    if (s.walk){ await p.evaluate(w => { const m = World.myPos(); World.walkToTile(m.x + w[0], m.y + w[1]); }, s.walk); await p.waitForTimeout(1300); }
    else await p.waitForTimeout(1800);
    if (s.say) { await p.evaluate(s => __wisp.setSay(s.say, s.col), s); await p.waitForTimeout(600); }
    await p.screenshot({ path: path.join(OUT, s.f + '.png') }); await p.close();
  }
  await b.close();
})();
