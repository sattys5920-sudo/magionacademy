// 막대과자 쪽지 관리자 보기 검사: sh tools/ui_mock.sh /home/user/magionacademy 8822 && node tools/stickday/note_test.js
//   NPC 에게 준 상자 쪽지 → stick/npc 에 남고 관리자 카드에 보여요 · 손에 든 상자 쪽지도 관리자 카드에 보여요 · 친구 쪽지는 원래대로
const { chromium } = require('playwright'); const fs = require('fs');
const seed0 = eval('(' + fs.readFileSync(__dirname + '/../../tests/ui.spec.js', 'utf8').match(/const seed = (\{.*\});\n/)[1] + ')');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else fail++; console.log(c ? '  ok ' : '  XX ', m); };
(async () => {
  const seed = JSON.parse(JSON.stringify(seed0)), box = (m, at) => ({ c: 1, t: 0, b: 0, k: 0, r: 0, s: 3, at, m });
  seed.players.me1.npc = { ...(seed.players.me1.npc || {}), nabi: { a: 50 } };
  seed.stick = { ctl: { open: true, at: 1 }, hold: { me1: { h1: box('나비야 늘 고마워', 1), h2: box('아직 못 준 상자', 2) } } };
  const br = await chromium.launch(), ctx = await br.newContext({ viewport: { width: 1000, height: 900 } }), errs = [];
  const page = async u => { const p = await ctx.newPage(); p.on('pageerror', e => errs.push(u + ': ' + e.message)); p.on('dialog', d => d.accept()); await p.addInitScript(([s, u]) => { window.__seed = s; window.__uid = u; }, [seed, u]); await p.goto('http://localhost:8822/'); await p.waitForFunction(() => window.__T, null, { timeout: 30000 }); await p.waitForTimeout(4000); return p; };
  const Ad = await page('admin'), A = await page('me1');
  await A.evaluate(() => window.__stk && __stk.npcGive('nabi', 'h1')); await A.waitForTimeout(2500);
  const t = await A.evaluate(() => JSON.parse(JSON.stringify((window.__tree.stick || {}).npc || {})));
  ok(t.me1 && t.me1.nabi && t.me1.nabi.m === '나비야 늘 고마워', 'NPC 에게 준 상자 쪽지가 stick/npc 에 남아요 ' + JSON.stringify(t));
  await Ad.evaluate(() => __T.showAdmin()); await Ad.waitForTimeout(1500); await Ad.evaluate(() => window.__adPoll && window.__adPoll()); await Ad.waitForTimeout(800);
  await Ad.evaluate(() => [...document.querySelectorAll('[data-adtab="event"]')].find(b => b.offsetParent).click()); await Ad.waitForTimeout(1500);
  const card = await Ad.evaluate(() => { const c = [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('막대과자의 날')); if (!c) return ''; if (c.classList.contains('shut')) c.querySelector('.abhead b').click(); return [...document.querySelectorAll('.adcard')].find(c => c.textContent.includes('막대과자의 날')).innerText; });
  if (process.env.DBG) console.log(card.slice(0, 1500));
  ok(/NPC 에게 준 쪽지 1 개/.test(card) && /나비야 늘 고마워/.test(card) && /→ 나비/.test(card), '관리자 카드: NPC 에게 준 쪽지 (학생 → NPC · 내용)');
  ok(/아직 손에 든 상자 쪽지 1 개/.test(card) && /아직 못 준 상자/.test(card), '관리자 카드: 아직 손에 든 상자 쪽지');
  ok(!errs.length, '페이지 오류 없음 ' + errs.slice(0, 3));
  console.log(`검사 ${pass + fail}개 · 실패 ${fail}개`); await br.close(); process.exit(fail ? 1 : 0);
})();
