// 하트 이야기를 실제 엔진(evPlay)으로 처음부터 끝까지 자동으로 넘겨서, 중간에 멈추는 이야기를 찾아요
//   node tools/story_run.js <목업 포트> [동시에 띄울 창 수=5] [선택지: first|last|mix] [NPC 목록 쉼표로 · 비우면 전부] [처음 ♥ 번호=1]
//   목업: bash tools/ui_mock.sh <저장소> <포트> (window.__T.evPlay · npcGet 손잡이)
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8820, PAR = +(process.argv[3] || 5), MODE = process.argv[4] || 'mix';
const spec = fs.readFileSync(path.join(__dirname, '../tests/ui.spec.js'), 'utf8'); const seed = eval('(' + spec.match(/const seed = (\{.*\});\n/)[1] + ')');
const NPCS = ['nabi', 'batri', 'kappa', 'aula', 'mandi', 'jipsin', 'sera', 'madeleine', 'stella', 'leo'];
const ONLY = (process.argv[5] || '').split(',').filter(Boolean), FROM = +(process.argv[6] || 1);
const jobs = []; NPCS.filter(n => !ONLY.length || ONLY.includes(n)).forEach((n, i) => { for (let k = (i === 0 && ONLY.length ? FROM : 1); k <= 10; k++) jobs.push([n, k]); });
const res = [];
async function boot(p){ await p.goto(`http://localhost:${PORT}/`); await p.waitForTimeout(3500); for (let k = 0; k < 12; k++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } await p.waitForTimeout(1500); }
async function worker(b, wi){
  const p = await b.newPage({ viewport: { width: 390, height: 844 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(sd => { window.__seed = sd; window.__uid = 'me1'; }, seed);
  await boot(p);
  while (jobs.length){
    const [n, k] = jobs.shift(); errs.length = 0;
    try { await runOne(p, n, k, errs); } catch(e){ console.log(`${n} ♥${k}: 창이 새로 고쳐져서 다시 해요 (${String(e.message).slice(0, 40)})`); jobs.push([n, k]); await p.waitForTimeout(1500); try { await boot(p); } catch(e2){} }
  }
}
async function runOne(p, n, k, errs){
  {
    await p.evaluate(async ([n, k]) => { const ev = await (await fetch(`data/npc/${n}/events/heart_${String(k).padStart(2, '0')}.json?t=${Date.now()}`)).json(); window.__evDone = false; __T.evPlay(__T.npcGet(n), k, ev, {}); }, [n, k]);
    await p.waitForTimeout(800);
    let last = '', since = Date.now(), steps = 0, status = 'ok', where = '';
    while (true){
      await p.waitForTimeout(90);
      const st = await p.evaluate(mode => {
        const ui = document.querySelector('#evstage'); if (!ui || !ui.classList.contains('on') || getComputedStyle(ui).display === 'none') return { end: 1 };
        const ch = [...document.querySelectorAll('.evch button')]; const tx = (document.querySelector('.evbox .evtext') || {}).textContent || '';
        if (ch.length){ const i = mode === 'first' ? 0 : mode === 'last' ? ch.length - 1 : (tx.length % ch.length); ch[i].click(); return { t: 'CH:' + tx }; }
        const inp = document.querySelector('#evstage input'); if (inp){ inp.value = '테스트'; const ok = document.querySelector('#evstage .evin button, #evstage button.go'); if (ok) ok.click(); return { t: 'IN:' + tx }; }
        (document.querySelector('.evbox') || ui).click(); return { t: tx };
      }, MODE);
      if (st.end) break; steps++;
      if (st.t !== last){ last = st.t; since = Date.now(); }
      else if (Date.now() - since > 15000){ status = 'STUCK'; where = last.slice(0, 60); break; }
      if (steps > 4000){ status = 'TOO_LONG'; where = last.slice(0, 60); break; }
    }
    if (status !== 'ok'){ await p.evaluate(() => { try { document.querySelector('#evstage')?.classList.remove('on'); } catch(e){} }); await p.reload(); await p.waitForTimeout(3500); for (let q = 0; q < 12; q++){ const bb = await p.$('#stnext'); if (!bb) break; await bb.click(); await p.waitForTimeout(100); } }
    res.push({ n, k, status, where, steps, errs: errs.slice(0, 2) }); console.log(`${n} ♥${k}: ${status}${where ? ' @ ' + where : ''}${errs.length ? ' · 오류 ' + errs[0].slice(0, 80) : ''}`);
  }
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  await Promise.all(Array.from({ length: PAR }, (_, i) => worker(b, i)));
  const bad = res.filter(r => r.status !== 'ok' || r.errs.length); console.log(`\n끝까지 간 이야기 ${res.filter(r => r.status === 'ok').length} / ${res.length} · 문제 ${bad.length}개`);
  bad.forEach(r => console.log(' -', r.n, '♥' + r.k, r.status, r.where, r.errs.join(' | ')));
  await b.close();
})();
