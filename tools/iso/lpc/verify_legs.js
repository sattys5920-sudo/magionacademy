// 다리 Y존·세로선 검증 (게임 코드 그대로): node verify_legs.js <사이트 주소>
// 앞·뒤 모습 10프레임, 다리 구간(가랑이 2줄 아래 ~ 신발 바로 위, 치마·원피스 천 줄 제외) 전체에서
// 가운데 열 = 바지 그림자색 1px 선인지 (외곽선색 아님, 그 줄 바지색의 70%), 바로 옆 칸에 진한 틈이 없는지.
// legline 2면 신발 바로 위 3줄만 외곽선색인지.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const url = process.argv[2] || 'http://localhost:8766/';
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage();
  await p.goto(url); await p.waitForFunction(() => window.World && World.Avatar); await p.evaluate(() => World.Avatar.ready);
  for (const opt of [1, 2]){
    const r = await p.evaluate(async opt => {
      const A = World.Avatar, M = A.meta, FW = A.FW, FH = A.FH, W = FW * M.frames; M.legline = opt; A.clear();
      const L = (c, i) => .299 * c[i] + .587 * c[i + 1] + .114 * c[i + 2];
      const feet = ['로퍼', '로퍼 + 무릎 양말', '운동화', '부츠', '흰 양말 + 운동화'].map(n => M.parts.feet.findIndex(q => q.n === n));
      const tee = M.parts.top.findIndex(q => q.n === '티셔츠');
      let rows = 0, bad = []; const fails = {}, st = { rows: 0, bad: 0 }, STAND = new Set([M.dirs.down, M.dirs.up]);
      for (let body = 0; body < 2; body++) for (let li = 0; li < M.parts.legs.length; li++) for (const fi of feet){
        const lp = M.parts.legs[li]; if (!lp.L[M.bodies[body]]) continue;
        for (const lcI of [0, 10, 13]){ const av = { body, top: tee, legs: li, feet: fi, hair: 0, house: 'moon', legsC: lcI, feetC: 0, topC: 18 };
        await A.need(av); const cv = A.compose(av), d = cv.getContext('2d').getImageData(0, 0, W, FH).data, own = A.debugOwn();
        for (const [k, [lc, cr]] of Object.entries(M.leg)){
          const xc = +k * FW + lc; let top = FH;
          for (let y = cr + 2; y < FH; y++) if (own[y * W + xc] === 1){ top = y; break; }
          for (let y = cr + 2; y < top; y++){
            const i = (y * W + xc) * 4; if (!d[i + 3] || own[y * W + xc]) continue;
            const isOut = Math.abs(d[i] - 40) <= 3 && Math.abs(d[i + 1] - 24) <= 3 && Math.abs(d[i + 2] - 32) <= 3;
            let ok;
            if (opt === 2 && top < FH && y >= top - 3) ok = isOut;
            else {
              const dk = j => .299 * d[j] + .587 * d[j + 1] + .114 * d[j + 2] < 45;
              if (dk(i) && dk(i - 4) && dk(i + 4)) continue;          // 바지 밑단 외곽선 줄 (다리가 아니에요)
              let nd = 0, nt = 0; for (let x = +k * FW; x < (+k + 1) * FW; x++){ const j = (y * W + x) * 4; if (!d[j + 3] || own[y * W + x]) continue; nt++; if (L(d, j) < 60) nd++; }
              if (nd * 10 > nt * 6) continue;                              // 밑단 띠 줄 (대부분 외곽선·그림자)
              // 선 색 = 그 줄 바지(다리)색 중 하나의 70% (채널마다 ±3)
              let match = false;
              for (let x = +k * FW; x < (+k + 1) * FW && !match; x++){
                if (x === xc) continue; const j = (y * W + x) * 4; if (!d[j + 3] || own[y * W + x] || dk(j)) continue;
                match = [0, 1, 2].every(c => Math.abs(d[i + c] - d[j + c] * .7) <= 3);
              }
              ok = !isOut && match;
            }
            rows++; if (STAND.has(+k)){ st.rows++; if (!ok) st.bad++; } if (!ok){ bad.push([lp.n, M.parts.feet[fi].n, M.colors.bottom[lcI], +k, y]); fails[lp.n] = (fails[lp.n] || 0) + 1; }
          }
        }
      }}
      return { rows, bad: bad.length, st, fails, sample: bad.filter(q => STAND.has(q[3])).slice(0, 8) };
    }, opt);
    console.log('legline', opt, '| 서 있는 앞·뒤:', r.st.rows, '줄 중 실패', r.st.bad, '| 걷기 포함 전체:', r.rows, '줄 중 실패', r.bad, '| 서기 실패 예:', JSON.stringify(r.sample));
  }
  await b.close();
})();
