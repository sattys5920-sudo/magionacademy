// 움직이는 시안: node follow_gif.js <포트> <저장 폴더>  → 정령불이 따라다니는 장면을 연속으로 찍어 칸 파일(gN_k.png)로 저장
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8791, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const INJ = fs.readFileSync(path.join(__dirname, 'follow_inject.js'), 'utf8');
const CLIPS = [
  { n: 'g1', i: 0, col: '#5A8CFF', script: [[0, 'walk', [3, 2]], [26, 'walk', [-2, 1]], [52, 'say', '이 근처.... 마력이 고여 있어요.......']], len: 80 },
  { n: 'g2', i: 9, col: '#6A7CFF', night: 1, script: [[4, 'say', '별이 많은 밤엔.... 나도 조금 더 밝아져요.......']], len: 40 },
  { n: 'g3', i: 10, col: '#8A5AE0', script: [[0, 'walk', [-3, 2]], [30, 'say', '....조용히. 누가 지켜보고 있어요.......']], len: 56 },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const c of CLIPS){
    const p = await b.newPage({ viewport: { width: 390, height: 844 } }); p.on('pageerror', e => console.log('err', e.message));
    await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
    await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
    for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
    await p.evaluate(c => { if (c.night) World.kNow = () => new Date(2026, 9, 30, 22, 10); World.zoomStep(-1); }, c);
    await p.addScriptTag({ content: INJ }); await p.evaluate(c => { __wisp.i = c.i; __wisp.col = c.col; }, c); await p.waitForTimeout(1800);
    for (let k = 0; k < c.len; k++){
      for (const [at, kind, v] of c.script) if (at === k) await p.evaluate(([kind, v, col]) => { if (kind === 'walk'){ const m = World.myPos(); World.walkToTile(m.x + v[0], m.y + v[1]); } else __wisp.setSay(v, col); }, [kind, v, c.col]);
      await p.screenshot({ path: path.join(OUT, `${c.n}_${String(k).padStart(3, '0')}.png`), clip: { x: 0, y: 190, width: 390, height: 330 } });
      await p.waitForTimeout(40);
    }
    await p.close();
  }
  await b.close();
})();
