// 요일 던전 처음 찾는 연출 영상: sh tools/ui_mock.sh <repo> 8822 를 켜 두고 node tools/daydungeon/well_intro_run.js
const { chromium } = require('playwright'); const fs = require('fs'); const R = __dirname + '/../..';
const seed = eval('(' + fs.readFileSync(R + '/tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
const OUT = __dirname + '/well'; fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, recordVideo: { dir: OUT + '/vid', size: { width: 390, height: 844 } } });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(s => { window.__seed = s; window.__uid = 'me1'; }, seed); await p.goto('http://localhost:8822/'); await p.waitForTimeout(4500);
  await p.addScriptTag({ path: __dirname + '/well_mock.js' });
  await p.evaluate(() => { World.teleport('town', [18, 56]); window.__glow = setInterval(() => __wellMock.place(true, performance.now()), 120); }); await p.waitForTimeout(2500);
  const t0 = Date.now();
  await p.evaluate(async () => {
    const say = t => ({ cmd: 'say', who: 'bone', text: t, ms: 3600 });
    await World.cut([
      { cmd: 'player', x: 17, y: 56, dir: 'left' }, { cmd: 'cam', x: 14, y: 55 }, { cmd: 'wait', sec: 1 },
      { cmd: 'fx', kind: 'dark', v: .45 }, { cmd: 'wait', sec: 1.2 }, { cmd: 'emote', who: 'player' }, { cmd: 'wait', sec: .8 },
      { cmd: 'spawn', who: 'bone', name: '본', spr: 16, x: 20, y: 58, dir: 'left' }, { cmd: 'walk', who: 'bone', x: 16, y: 57 },
      { cmd: 'face', who: 'bone', to: 'player' }, { cmd: 'face', who: 'player', to: 'bone' },
      say('「마른 우물 깊은 밑에, 불빛 하나 깜빡이네」. 오, 길손도 봤어? 축하해.'),
      say('이 우물, 물은 다 말랐는데 밑에서 쿵, 쿵 소리가 나. 요일마다 장단이 달라.'),
      say('월요일엔 느릿느릿 쿵.... 화요일엔 으르렁 쿵쿵. 날마다 다른 손님이 사는 거야.'),
      say('밧줄은 튼튼해. 어제 내가 매달려 봤거든. 떨어지긴 했는데 밧줄 탓은 아니야.'),
      say('혼자 가도 되고 넷까지 같이 가도 돼. 손님은 하루에 세 번만 받아 준대.'),
      say('「들어간 손 셋이라도, 나온 손 셋이길 비네」. 내려가면 축하해. 안 내려가도 축하해.'),
      { cmd: 'walk', who: 'bone', x: 24, y: 56, timeout: 5 }, { cmd: 'despawn', who: 'bone' },
      { cmd: 'face', who: 'player', to: 'player' }, { cmd: 'walk', who: 'player', x: 13, y: 56 }, { cmd: 'wait', sec: .6 },
      { cmd: 'fade', v: 1, text: '밧줄을 타고 천천히 내려가요.......' }, { cmd: 'wait', sec: 2 }, { cmd: 'fx', kind: 'light' }, { cmd: 'fade', v: 0 }, { cmd: 'cam' }]);
    __wellMock.panel(0, 3, []);
  });
  await p.waitForTimeout(3000);
  console.log('cut sec', (Date.now() - t0) / 1000, 'errs', JSON.stringify(errs));
  const v = p.video(); await ctx.close(); await b.close(); fs.renameSync(await v.path(), OUT + '/intro.webm');
})();
