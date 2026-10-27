// 별 보는 밤 시안 사진 찍기: node tools/stargaze/shot.js <저장 폴더>
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const fs = require('fs'), path = require('path');
const out = process.argv[2] || '.', url = 'file://' + path.resolve(__dirname, 'preview.html');
const data = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../../public/data/events/stargazing/constellations.json'), 'utf8'));
const TXT = { pumpkin_cart: '호박 수레자리예요!', witch_broom: '마녀 빗자루자리예요!', sleepy_owl: '졸린 부엉이자리예요!', bell_cat: '방울 고양이자리예요!', twelve_friends: '열두 친구자리예요!' };
// 학생 캐릭터는 게임 화면(모의 서버 GAME, 기본 http://localhost:8230/)에서 실제 아바타 그림을 받아와요
const GAME = process.env.GAME || 'http://localhost:8230/';
async function crowdUrls(b){
  const pg = await b.newPage({ viewport: { width: 390, height: 740 } }), seed = { players: { u0: { nick: '민준', look: 2, house: 'dew', coin: 1, mana: 1, day: 1, inv: {}, cr: [], eggs: [], ex: { exp: 0, job: 'warrior', sp: {}, sk: {} } } }, story: { live: { ch: 1, at: 1 } } };
  await pg.addInitScript(([s]) => { window.__seed = s; window.__uid = 'u0'; }, [seed]); await pg.goto(GAME); await pg.waitForTimeout(3000);
  const urls = await pg.evaluate(async () => { const out = []; for (const lk of [3, 10, 17, 24, 31, 38, 45, 52, 59, 3]){ const av = World.Avatar.fix(World.Avatar.fromLook(lk)); await World.Avatar.need(av); out.push(World.Avatar.compose(av).toDataURL()); } return out; });
  await pg.close(); return urls;
}
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }), CROWD = await crowdUrls(b);
  async function shot(name, q, W = 390, H = 844){ const pg = await b.newPage({ viewport: { width: W, height: H } }); q = { ...q, W, H, data, crowd: CROWD.slice(0, (q.people ?? 9) + 1) };
    await pg.goto(url + '#' + encodeURIComponent(JSON.stringify(q))); await pg.waitForFunction(() => window.__ready); await pg.waitForTimeout(250); await pg.screenshot({ path: path.join(out, name + '.png') }); await pg.close(); }
  const C0 = 'pumpkin_cart';
  await shot('sky_a_light', { c: C0, lit: 7, people: 9, text: '자기 별을 눌러서 켜 주세요. 켜진 별은 제가 다 보고 있어요.', count: '켜진 별 7 / 12' });
  await shot('sky_b_drawing', { c: C0, lit: 12, drawn: 7.45, text: '자, 이제 다 같이 하늘을 보세요.', noNames: false, hot: ['P6', 'C1'], t: 1.6 });
  await shot('sky_c_done', { c: C0, lit: 12, drawn: 12, outline: 1, title: 1, text: TXT[C0] });
  for (const c of data.constellations) await shot('sky_done_' + c.id, { c: c.id, lit: 12, drawn: c.order.length, outline: 1, title: 1, text: TXT[c.id], people: c.id === 'twelve_friends' ? 12 : 9 });
  await shot('sky_pc_done', { c: C0, lit: 12, drawn: 12, outline: 1, title: 1, text: TXT[C0] }, 1440, 900);
  await b.close();
})();
