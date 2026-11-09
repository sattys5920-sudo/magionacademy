// 요일 던전 보스 이펙트 시안 찍기: 모의 서버(tools/ui_mock.sh <루트> 8822)를 먼저 띄운 뒤
//   node tools/daydungeon/day_fx_run.js [포트]  →  tools/daydungeon/fx/*.png (장면별) + tools/daydungeon/day_fx_sheet.png (한 장)
//   모의 사이트 복사본 옆에 day.html 을 만들어 day_fx.js 를 모듈 스크립트 안에 넣어요 (public/index.html · 복사본 index.html 은 그대로)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const PORT = +(process.argv[2] || 8822), ROOT = '/home/user/magionacademy', OUT = ROOT + '/tools/daydungeon/fx';
const SITE = '/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_' + PORT + '/site';
const ROWS = [
  ['월 · 철갑 거북 「바위등」 (체력이 엄청 많음)', ['등껍질 방어 자세 (받는 피해 −50 %)', '껍질이 열렸어요 (몰아칠 틈)', '큰 기술: 지진 구르기 (피하기 원)']],
  ['화 · 붉은 늑대왕 「송곳니」 (공격력이 엄청 셈)', ['앞열 한입 물기 (큰 한 방)', '큰 기술: 물어뜯기 (피하기 원)', '25 % 포효 (공격 +20 %)']],
  ['수 · 늪 마녀 「독버섯 할멈」 (지속 피해)', ['독이 쌓여요 (겹 수 · 초록 숫자)', '독 안개 (전체 지속 피해)', '정화 · 치유로 독을 지워요']],
  ['목 · 그림자 쌍둥이 「낮과 밤」 (둘이 함께)', ['체력 바 둘 · 비슷하게 깎아요', '서로 보호막 (끊기 게이지)', '남은 쪽이 화가 났어요 (공격 +50 %)']],
  ['금 · 시계 장인 인형 「태엽공」 (빠르고 졸개를 불러요)', ['태엽 졸개가 나와요', '졸개 3 → 폭주 경고', '광역으로 졸개 정리']]];
(async () => {
  const html = fs.readFileSync(SITE + '/index.html', 'utf8'), fx = fs.readFileSync(ROOT + '/tools/daydungeon/day_fx.js', 'utf8');
  const m0 = html.indexOf('<script type="module">'), m1 = html.indexOf('</script>', m0);
  fs.writeFileSync(SITE + '/day.html', html.slice(0, m1) + '\n' + fx + '\n' + html.slice(m1));
  const seed = eval('(' + fs.readFileSync(ROOT + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});/)[1] + ')');
  fs.mkdirSync(OUT, { recursive: true });
  const br = await chromium.launch(), pg = await br.newPage({ viewport: { width: 400, height: 900 }, deviceScaleFactor: 1 }); const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  await pg.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed);
  await pg.goto('http://localhost:' + PORT + '/day.html'); await pg.waitForFunction(() => window.__dayFx && window.World && World.Avatar, null, { timeout: 30000 }); await pg.waitForTimeout(3000);
  await pg.evaluate(() => document.fonts.ready);
  const shots = [];
  for (let b = 0; b < 5; b++) for (const sc of ['a', 'b', 'c']){
    await pg.evaluate(o => window.__dayFx(o), { b, sc, t: .55 }); await pg.waitForTimeout(150);
    const f = `${OUT}/day_${b}${sc}.png`; await pg.locator('#dayov').screenshot({ path: f }); shots.push(f);
  }
  // 한 장으로: 보스마다 한 줄 (제목 + 장면 이름 + 그림 3 개)
  const imgs = shots.map(f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64'));
  await pg.setViewportSize({ width: 1300, height: 900 }); await pg.goto('http://localhost:' + PORT + '/fonts/Galmuri-LICENSE.txt');
  await pg.setContent(`<html><body style="margin:0;background:#140e22;color:#f4ecff;font-family:G11,sans-serif"><div id="sh" style="display:inline-block;padding:16px 18px 20px">
    <style>@font-face{font-family:G11B;src:url(/fonts/Galmuri11-Bold.full.woff2)}@font-face{font-family:G11;src:url(/fonts/Galmuri11.full.woff2)}h1{font:22px G11B,sans-serif;margin:0 0 4px}h2{font:18px G11B,sans-serif;margin:18px 0 6px}.r{display:flex;gap:14px;align-items:flex-start}.p small{display:block;font:12px G11B,sans-serif;color:#cbbbe8;margin-bottom:4px}.p img{display:block;border-radius:6px}</style>
    <h1>요일 던전 · 보스 이펙트 시안</h1><div style="font-size:12px;color:#9a8ab8">우물 아래 돌방 · 파티 4 명 (앞열 기사 · 전사, 뒤열 흑마법사 · 성직자) · 그림만 (게임 코드 아님)</div>
    ${ROWS.map(([t, ls], b) => `<h2>${t}</h2><div class="r">${ls.map((l, k) => `<div class="p"><small>${'ABC'[k]}. ${l}</small><img src="${imgs[b * 3 + k]}"></div>`).join('')}</div>`).join('')}</div></body></html>`);
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(800);
  await pg.locator('#sh').screenshot({ path: ROOT + '/tools/daydungeon/day_fx_sheet.png' });
  console.log('done', shots.length, errs.length ? 'errors: ' + errs.slice(0, 5).join(' | ') : 'no errors');
  await br.close();
})();
