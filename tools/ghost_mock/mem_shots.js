// 추억 조각 4 장을 실제 게임 화면에서 찍어요 (내 아바타 그대로 + 마틸다 LPC + 그 장소 그 시간)
//   node mem_shots.js <포트> <저장 폴더> → mem0..3.png (게임 그림 그대로 잘라 낸 것 · 사진 틀은 grad_inject.js가 씌워요)
//   목업 사이트 폴더에 ghost_lpc.png가 있어야 해요
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8822, OUT = process.argv[3] || '.';
const spec = fs.readFileSync(path.join(__dirname, '../../tests/ui.spec.js'), 'utf8');
const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
// 장면: 맵 · 내 자리 · 마틸다 자리 · 마틸다 방향 칸(0 아래 5 위 10 왼 15 오른) · 내가 볼 곳 · 시각 · 말풍선 · 요리 소품
const SC = [
  { m: 'campus', me: [41, 39], gh: [42, 39], gf: 10, look: [42, 39], h: 21, say: '틸다!' },
  { m: 'candy', me: [12, 13], gh: [13, 13], gf: 10, look: [12, 12], h: 18, dish: [13, 12], dy: 80, say: '맛있다!' },
  { m: 'campus', me: [39, 37], gh: [40, 36], gf: 10, look: [39, 35], h: 23, dy: 10 },
  { m: 'town', me: [41, 49], gh: [42, 49], gf: 5, look: [41, 46], h: 23, star: true },
];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('err', e.message));
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500);
  for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); }
  await p.evaluate(() => new Promise(r => { const GH = window.__GH = new Image(); GH.onload = r; GH.src = 'ghost_lpc.png'; const D = window.__DS = new Image(); D.src = 'art/dishes.png'; }));
  for (let i = 0; i < SC.length; i++){
    const s = SC[i];
    await p.evaluate(s => { World.kNow = () => new Date(2026, 9, 30, s.h, 10); World.zoomStep(-2); World.tagsOff(true); World.setNpcs([]); World.teleport(s.m, s.me); }, s); await p.waitForTimeout(1800);
    await p.evaluate(s => {
      const c = document.createElement('canvas'); c.width = c.height = 48; const q = c.getContext('2d'); const rg = q.createRadialGradient(24, 26, 2, 24, 26, 22); rg.addColorStop(0, 'rgba(200,230,255,.28)'); rg.addColorStop(1, 'rgba(200,230,255,0)'); q.fillStyle = rg; q.fillRect(0, 0, 48, 48);
      q.imageSmoothingQuality = 'high'; q.drawImage(window.__GH, s.gf * 64, 0, 64, 64, 8, 8, 32, 32); q.globalCompositeOperation = 'lighter'; q.globalAlpha = .15; q.drawImage(window.__GH, s.gf * 64, 0, 64, 64, 8, 8, 32, 32);
      const L = [{ id: 'mt', x: s.gh[0], y: s.gh[1], img: c, pxc: q, sw: 48, sh: 48, ax: 24, ay: 38, solid: false, light: { r: 24, c: [190, 225, 255], a: .45 } }];
      if (s.dish){ const d = document.createElement('canvas'); d.width = d.height = 32; const g = d.getContext('2d'); g.drawImage(window.__DS, 32 * 7, 0, 32, 32, 0, 0, 32, 32); L.push({ id: 'ds', x: s.dish[0], y: s.dish[1], img: d, pxc: g, sw: 32, sh: 32, ax: 16, ay: 34, solid: false }); }
      World.setProps(s.m, L, 'mem'); World.faceTo(s.look[0], s.look[1]); if (s.say) World.say('me', s.say);
    }, s); await p.waitForTimeout(900);
    const box = await p.evaluate(() => { const c = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0].getBoundingClientRect(); return { x: c.x, y: c.y, w: c.width, h: c.height }; });
    const cx = box.x + box.w / 2, cy = box.y + box.h / 2;
    if (s.full) await p.screenshot({ path: path.join(OUT, `full${i}.png`) });
    await p.screenshot({ path: path.join(OUT, `mem${i}.png`), clip: { x: Math.round(cx - 120), y: Math.round(cy - 110 + (s.dy || 0)), width: 240, height: 160 } });
    await p.evaluate(s => World.setProps(s.m, [], 'mem'), s);
  }
  await b.close();
})();
