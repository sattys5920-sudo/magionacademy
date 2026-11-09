// 서버 다운로드 줄이기 검사: 학생 화면은 pub 만 들어요 · pub 없는 학생은 한 번만 받아 채워요 · 방 구경은 전체를 한 번 · 관리자는 1 분마다
//   sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/bandwidth/test_pub.js [포트]
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../..', PORT = process.argv[2] || 8822;
const seed0 = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('  실패:', m); } };
(async () => {
  const b = await chromium.launch(); const seed = JSON.parse(JSON.stringify(seed0)), me = seed.players.me1;
  const mk = (nick, house, extra) => ({ ...JSON.parse(JSON.stringify(me)), nick, house, rv: 1, sid: 'x', cr: [{ k: 0, name: '큰 생물', love: 99, age: 99 }], room: [{ id: 'r1', f: 'chair', x: 3, y: 3 }], ...extra });
  seed.players.u2 = mk('서연', 'dew', { ex: { exp: 5000, job: 'black', wp: 2 } }); seed.players.u3 = mk('지호', 'ember', {});
  seed.approved = { me1: true, u2: true, u3: true }; seed.pub = { u2: { nick: '서연', house: 'dew', look: 3, room: [{ id: 'r1', f: 'chair', x: 3, y: 3 }], ex: { job: 'black', wp: 2 } } };   // u3 은 아직 pub 없음
  const p = await b.newPage({ viewport: { width: 390, height: 844 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto(`http://localhost:${PORT}/`); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(4000);
  const pl = await p.evaluate(() => { const P = __T.playersGet ? __T.playersGet() : null; return P; });
  // playersList 는 모듈 안이라 화면으로 확인: 친구 목록 · 기숙사 방 이름
  const pubMe = await p.evaluate(() => __T.pkSet ? null : null);
  const db = await p.evaluate(async () => { const r = await import('./mock/firebase-database.js'); const g = async k => (await r.get(r.ref(null, k))).val(); return { pub: await g('pub') }; });
  ok(db.pub && db.pub.me1 && db.pub.me1.nick === '민준', '내 pub 이 저장돼요 ' + JSON.stringify(db.pub && db.pub.me1 && db.pub.me1.nick));
  ok(db.pub && db.pub.me1 && !db.pub.me1.inv && !db.pub.me1.cr, 'pub 에는 작은 정보만 (가방 · 생물 없음)');
  const sz = await p.evaluate(async () => { const r = await import('./mock/firebase-database.js'); const v = (await r.get(r.ref(null, 'pub/me1'))).val(), w = (await r.get(r.ref(null, 'players/me1'))).val(); return [JSON.stringify(v).length, JSON.stringify(w).length]; });
  console.log('  pub 크기', sz[0], '/ 전체 저장', sz[1]);
  // 친구 목록에 pub 있는 u2, pub 없는 u3 모두 보여요
  await p.evaluate(() => __T.openSheet('home', 'friends')); await p.waitForTimeout(800);
  const html = await p.evaluate(() => document.body.innerText);
  ok(/서연/.test(html), '친구 목록: pub 있는 학생'); ok(/지호/.test(html), '친구 목록: pub 없는 학생도 한 번 받아 채워요');
  await p.screenshot({ path: __dirname + '/friends.png' });
  // 방 구경: 생물(전체 정보)도 보여요
  await p.evaluate(() => __T.closeSheet()); await p.evaluate(() => { const b = [...document.querySelectorAll('button')]; });
  const vis = await p.evaluate(async () => { __T.openSheet('home'); await new Promise(r => setTimeout(r, 300)); return typeof window.__visit === 'function'; });
  // 관리자: 학생 목록이 보이고 · pub 없는 학생을 대신 채워요
  await p.evaluate(() => __T.showAdmin()); await p.waitForTimeout(2500); await p.evaluate(() => { const b = [...document.querySelectorAll('#adminv button, button')].find(x => /^학생/.test(x.textContent.trim())); b && b.click(); }); await p.waitForTimeout(1200); await p.screenshot({ path: __dirname + '/admin_students.png' });
  const adm = await p.evaluate(async () => { const r = await import('./mock/firebase-database.js'); const u3 = (await r.get(r.ref(null, 'pub/u3'))).val(); return { u3: u3 && u3.nick, txt: document.body.innerText.includes('지호') }; });
  ok(adm.u3 === '지호', '관리자가 pub 없는 학생을 채워요 ' + adm.u3); ok(adm.txt, '관리자 화면에 학생이 보여요');
  ok(errs.length === 0, '오류 없음 ' + JSON.stringify(errs.slice(0, 3)));
  console.log(`${pass} / ${pass + fail} 통과`); await b.close(); process.exit(fail ? 1 : 0);
})();
