// ===== 마들렌의 쿠키 상자: 관리자가 켜면 과자 교실에서 마들렌이랑 버터 동그라미 쿠키를 같이 굽는 연출(튜토리얼) → 과자 교실 오븐 열림
//   굽기 미니게임 5 단계(재료 · 젓기 · 밀기 · 틀 · 오븐, 별이 많을수록 어려워요) → 아이싱 꾸미기 → 상자 포장 → NPC에게 선물 (NPC마다 받는 연출)
//   ck/ctl { open, id } · ck/yum/<id> = { by, npc, from, at, ts: [시각 ×25] } (선물한 날부터 5 일 동안 하루 5 번 전체 채팅에 「(이름)이 준 쿠키 냠냠!」)
//   me.ck = { ev 본 연출, met, dex { 맛_모양: 등급 }, tray [쿠키], boxes [{ c, r, p, cks }], found { npc: { f, s } }, gave }
//   쿠키 = { f 맛, s 모양, b 구운 정도, q 등급, i 아이싱(줄인 글자), t 토핑 [[k, x, y, 색, 세로]] }
let ckOn = false;
const CK = (() => {
  const FL = [
    { id: 'butter', n: '버터', it: 'milk', c: '#F0CC86' }, { id: 'straw', n: '딸기', it: 'g_straw', c: '#F6AEB8' }, { id: 'mint', n: '박하', it: 'g_mint', c: '#B4E4BE' },
    { id: 'honey', n: '꿀', it: 'honey', c: '#E8A848' }, { id: 'pseed', n: '호박씨', it: 'g2_pseed', c: '#C8C084' }, { id: 'blueb', n: '블루베리', it: 'g_blueb', c: '#8C88CC' },
    { id: 'carrot', n: '당근', it: 'g_carrot', c: '#F08A4A' }, { id: 'maple', n: '단풍 시럽', it: 'g_maple', c: '#B86A3A' }, { id: 'chamo', n: '카모마일', it: 'g_chamo', c: '#F6EAB0' },
    { id: 'rasp', n: '산딸기', it: 'g2_rasp', c: '#D8506E' }, { id: 'lav', n: '라벤더', it: 'g_lav', c: '#CDB0EE' }, { id: 'chest', n: '알밤', it: 'g2_chest', c: '#94683E' },
  ];
  const BASE = ['g_wheat', 'hegg'];
  const SH = [['circle', '동그라미'], ['heart', '하트'], ['moon', '달'], ['drop', '물방울'], ['cloud', '구름'], ['leaf', '나뭇잎'], ['star', '별'], ['ghost', '유령'], ['pumpkin', '호박'], ['mushroom', '버섯'], ['hat', '마녀 모자'], ['fish', '물고기'], ['flower', '꽃'], ['cat', '고양이'], ['bat', '박쥐'], ['bear', '곰'], ['rabbit', '토끼'], ['crown', '왕관'], ['bolt', '번개'], ['candy', '사탕']];
  const SH_STAR = { circle: 1, heart: 1, moon: 1, drop: 1, cloud: 1, leaf: 1, star: 2, ghost: 2, pumpkin: 2, mushroom: 2, hat: 2, fish: 2, flower: 2, cat: 3, bat: 3, bear: 3, rabbit: 3, crown: 3, bolt: 3, candy: 3 };
  const ICE = [['하양', '#FFF8F0'], ['분홍', '#FF9EC0'], ['민트', '#9FE8C8'], ['노랑', '#FFE27A'], ['하늘', '#9FD0FF'], ['초코', '#6A3A24']];
  const TOP = [['spr', '스프링클'], ['chip', '초코 칩'], ['pearl', '설탕 진주']];
  const SPR = ['#FF6B8A', '#6FD0FF', '#FFE27A', '#9FE8A8', '#C8A8F0'];
  const BOXC = ['#F4A0B8', '#9FD0FF', '#B8E6A8', '#FFE08A', '#C8A8F0', '#F6F0E8'], RIB = ['#E8455A', '#FFFFFF', '#FFD24A', '#6A9FE8', '#7A4A2E'], PAT = [['none', '민무늬'], ['dot', '물방울'], ['stripe', '줄무늬'], ['heart', '하트']];
  const DEX = []; FL.forEach(f => SH.forEach(([s, sn]) => DEX.push({ id: f.id + '_' + s, f: f.id, s, n: `${f.n} ${sn} 쿠키` })));
  DEX.push({ id: 'coal', f: 'butter', s: 'circle', n: '숯 쿠키', hid: '오븐에 너무 오래 두면.......', b: 100 }, { id: 'moon_mad', f: 'honey', s: 'moon', n: '마들렌의 달빛 쿠키', hid: '별 셋 쿠키를 「최고」로 구우면.......', b: 68, gold: true });
  const UNLOCK = { 1: 0, 2: 5, 3: 15 }, STEP_N = ['재료', '젓기', '밀기', '틀', '오븐', '꾸미기'], GPT = { 완벽: 2, 좋아: 1, 아쉬워: 0, 탐: 0 }, TRAY_MAX = 16, BOX_MAX = 8;
  const TIPS = [
    s => s === 1 ? '순서는 상관없어. 레시피에 있는 것만 그릇에 쏙쏙 넣어.' : s === 2 ? '이번엔 순서대로 넣어야 해. 순서 틀리면 반죽이 삐져.' : '순서대로, 시간 안에! 찬장에 헷갈리는 게 많으니까 잘 봐.',
    s => s === 3 ? '그릇 안을 손가락으로 빙글빙글. 너무 세게 돌리면 반죽이 튀어.' : '그릇 안을 손가락으로 빙글빙글 저어. 손목으로!',
    () => '밀대를 위아래로 밀어. 너무 얇으면 찢어지고, 너무 두꺼우면 안 익어. 초록 칸에서 멈춰.',
    s => s === 1 ? '틀이 지나갈 때 콕. 겹치게 찍으면 못 써.' : s === 2 ? '틀이 조금 빨라. 사이를 띄워서 콕콕.' : '빨라도 침착하게. 네 개, 안 겹치게!',
    s => s === 3 ? '별 셋은 노릇한 순간이 진짜 짧아. 눈 떼지 마.' : '노릇노릇할 때 딱 꺼내.',
  ];
  // NPC마다 좋아하는 맛 · 모양 · 마들렌 단골 수첩 힌트 · 반응 대사 (최고 · 좋음 · 보통 · 탐)
  const NPCS = {
    nabi: { f: 'butter', s: 'cat', hint: '우유 냄새 나는 건 뭐든 좋아해요. 그리고 자기 닮은 모양이면.... 모른 척하면서 제일 먼저 집어요.', r: ['고양이 모양에 버터 냄새.... 이건 반칙이다냥. 귀는 아껴 두고 꼬리부터 먹을 거다냥.', '버터 냄새가 난다냥. ....하나만 먹을 거다냥. 아마도.', '쿠키다냥. 생선은 아니지만.... 받아 두겠다냥.', '까맣다냥. 숯인 줄 알았다냥. ....그래도 다 먹었다냥.'] },
    batri: { f: 'straw', s: 'bat', hint: '새콤한 빨간 열매를 좋아해요. 모양은.... 거울 보면 나오는 그거요.', r: ['박쥐 모양이다. 딸기 맛이고. 이거 나 주려고 구운 거 맞지? 날개 한쪽은 아껴 둘래.', '딸기 냄새 좋다. 배달 가방 맨 위에 넣어 둘게. 안 부서지게.', '고마워. 배달하다 배고플 때 먹을게.', '어.... 밤하늘 색이네. 나는 밤을 좋아하니까 괜찮아.'] },
    kappa: { f: 'mint', s: 'fish', hint: '시원한 풀 향을 좋아해요. 모양은.... 연못에서 매일 못 잡는 그거요.', r: ['물고기다. 시원하다. ....드디어 한 마리 잡았군. 먹겠다.', '박하 향이 난다. 연못 바람 같다. 나쁘지 않다.', '쿠키군. 오이는 아니지만.... 고맙다.', '탔다. ....물에 적시면 괜찮을지도 모른다. 아니, 아니겠군.'] },
    aula: { f: 'lav', s: 'moon', hint: '밤에 깨어 있는 사람이라 밤하늘 닮은 걸 좋아해요. 잠 잘 오는 보라색 꽃 맛이요.', r: ['달 모양 라벤더 쿠키.... 밤에 책 읽을 때 하나씩 꺼내 먹을게요. 서른 밤은 버틸 것 같아요.', '라벤더 향이네요. 책갈피 옆에 두고 아껴 먹을게요.', '고마워요. 부스러기가 책에 떨어지지 않게 조심할게요.', '....조금 탔네요. 괜찮아요. 오래된 책 냄새랑 비슷해서 오히려 좋아요.'] },
    mandi: { f: 'chamo', s: 'flower', hint: '꽃잎 우린 차 같은 맛을 좋아해요. 모양도.... 온실에 가득한 그거요.', r: ['꽃 모양에.... 카모마일 맛. 이거 꽃말로 치면.... 아, 아니에요. 그냥 너무 좋아서요.', '카모마일 향이 나요. 저녁에 차랑 같이 먹어야겠다.', '고마워요. 온실 창가에 두고 보다가 먹을게요.', '앗.... 괜찮아요, 괜찮아요. 저도 꽃 말리다가 태운 적 있어요.'] },
    jipsin: { f: 'pseed', s: 'pumpkin', hint: '머리에 쓴 거랑 같은 모양이면 좋아해요. 그 안에 든 씨앗 맛이면 더요.', r: ['호박이다. 호박씨로 만든 호박이다. 내 머리랑 사촌이다. 잘 먹겠다.', '호박씨. 고소하다. 들판 냄새가 난다.', '고맙다. 까마귀한테는 안 뺏기겠다.', '....까맣다. 까마귀가 좋아하겠다. 나도 먹겠다.'] },
    sera: { f: 'rasp', s: 'heart', hint: '아픈 애들 돌보느라 마음이 말랑해요. 마음 모양, 숲에서 따는 새콤한 빨간 열매 맛이요.', r: ['하트 모양 산딸기 쿠키네. 양호실 오는 애들 하나씩 주고 싶을 만큼 예쁘다. ....근데 내가 다 먹을 거야.', '산딸기네. 비타민이 들었으니까 이건 약이야. 그렇게 치자.', '고마워. 단 건 하루에 하나만. 오늘 건 이걸로 할게.', '음.... 이건 진료가 필요하겠는데. 그래도 마음은 건강하게 받았어.'] },
    madeleine: { f: 'maple', s: 'crown', hint: '나? ....단풍 시럽 듬뿍. 모양은.... 과자 교실의 주인한테 어울리는 거.', r: ['왕관 모양 단풍 쿠키.... 내가 과자 교실의 왕이라는 거지? 맞아. 오늘부터 이 쿠키가 내 왕관이야.', '단풍 시럽 향 좋다. 반죽 잘했네. 제자 하나 생긴 기분이야.', '고마워. 남이 구워 준 쿠키는.... 이상하게 더 맛있어.', '....우리 동지네. 괜찮아. 나도 오늘 아침에 한 판 태웠어.'] },
    stella: { f: 'blueb', s: 'star', hint: '하늘에서 반짝이는 그 모양이요. 맛은.... 밤하늘 색 열매요.', r: ['별 모양 블루베리.... 밤하늘을 반죽한 맛이야. 오늘 운세에 달콤한 선물이 있었거든.', '별이다. 별은 언제 받아도 좋아. 하나는 망원경 옆에 둘게.', '고마워. 별 보면서 하나씩 먹을게.', '어머, 까만 쿠키네. 흑점 같아. ....별에도 그런 날이 있지.'] },
    leo: { f: 'carrot', s: 'rabbit', hint: '사육장 토끼들 간식을 매일 챙겨요. 그 간식 맛이랑, 그 친구들 모양이요.', r: ['토끼 모양 당근 쿠키! 우리 애들 닮았다. 애들한테도 한 입씩.... 아니, 이건 내 거다.', '당근 냄새. 토끼들이 줄 서겠다. 나 먼저 먹을게.', '고마워. 사육장 애들 밥 주고 나서 먹을게.', '하하, 탔네. 닭들은 이런 거 좋아해. 아, 아니, 내가 먹을게.'] },
    otumo: { f: 'honey', s: 'bolt', hint: '삐빅거리는 그 친구는 번개 콩을 좋아하잖아요. 번쩍하는 그 모양이랑, 꽃에서 온 단맛이요.', r: ['삐빅. 번개 모양, 꿀 성분 감지. 만족도 측정 불가. 측정기가 녹았습니다.......', '삐빅. 단맛 수치 높음. 연료로는 못 쓰지만 저장합니다.', '삐빅. 쿠키 수령. 감사 회로 작동 중.......', '경고. 탄소 함량 높음. ....그래도 먹습니다. 기분은 맛있음으로 기록.'] },
  };
  const DRAWN = { otumo: '그림도 감지. 저장.', nabi: '....그림도 그렸냐냥.', kappa: '그림도 있군.', jipsin: '그림도 있다.' };
  const REACT = {
    nabi: { act: 'burst', fx: 'heart', emo: '냥!', say: '골골골.......' }, batri: { act: 'orbit', fx: 'bat', emo: '와!', say: '빙글빙글!' },
    kappa: { act: 'head', fx: 'drop', emo: '오.', say: '....균형 잡는 중이다.' }, aula: { act: 'fall', fx: 'feather', emo: '어머.', say: '부엉.......' },
    mandi: { act: 'blush', fx: 'flower', emo: '♥', say: '헤헤.......' }, jipsin: { act: 'shoo', fx: 'crow', emo: '!', say: '저리 가라, 내 쿠키다.' },
    sera: { act: 'stamp', fx: 'heart', emo: '어머', say: '진찰 결과.... 합격!', stamp: '건강 합격' }, madeleine: { act: 'stamp', fx: 'crown', emo: '오!', say: '심사 결과.......', stamp: '합격!' },
    stella: { act: 'orbit', fx: 'star', emo: '☆', say: '별이 반짝반짝.......' }, leo: { act: 'bunny', fx: 'bunny', emo: '하하!', say: '얘들아, 이거 봐라!' },
    otumo: { act: 'zap', fx: 'spark', emo: '삐빅!', say: '기쁨 회로 과열.......' },
  };
  // ---------- 쿠키 도트 (24 × 24) ----------
  const N = 24;
  const inPoly = (x, y, P) => { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++){ const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; };
  const STAR = Array.from({ length: 10 }, (_, i) => { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? 6.4 : 12.2; return [11.5 + Math.cos(a) * r, 12.9 + Math.sin(a) * r]; });
  const BATL = [[8, 8], [0.5, 4.5], [1, 11], [3.5, 9.5], [3.5, 14], [6.5, 12.5], [8.5, 16.5]], BATR = BATL.map(([x, y]) => [23 - x, y]);
  const C = (x, y, cx, cy, r) => (x - cx) ** 2 + (y - cy) ** 2 <= r * r, E = (x, y, cx, cy, rx, ry) => ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1;
  const SHAPE_FN = {
    circle: (x, y) => C(x, y, 11.5, 11.5, 10.6),
    heart: (x, y) => { const X = (x - 11.5) / 9.0, Y = -(y - 11.8) / 9.0; return (X * X + Y * Y - 1) ** 3 - X * X * Y * Y * Y <= 0; },
    moon: (x, y) => C(x, y, 11.5, 11.5, 10.6) && !C(x, y, 16.5, 7.5, 8.6),
    drop: (x, y) => C(x, y, 11.5, 15, 7.6) || inPoly(x, y, [[11.5, 1], [4.4, 12.8], [18.6, 12.8]]),
    cloud: (x, y) => C(x, y, 6.5, 14, 5.2) || C(x, y, 12, 10, 6.8) || C(x, y, 17.5, 13.5, 5.2) || (x >= 3 && x <= 20.5 && y >= 13 && y <= 19.2),
    leaf: (x, y) => { const u = (x - 11.5 + y - 11.5) / 1.414, v = (x - y) / 1.414; return (u / 11.2) ** 2 + (v / 5.6) ** 2 <= 1; },
    star: (x, y) => inPoly(x, y, STAR),
    ghost: (x, y) => (y <= 11 && C(x, y, 11.5, 11, 9.2)) || (y > 11 && Math.abs(x - 11.5) <= 9.2 && y <= 21.5 - (Math.floor((x - 2.3) / 3.1) % 2 ? 2.5 : 0)),
    pumpkin: (x, y) => E(x, y, 11.5, 14, 11.2, 8.6) || (x >= 10 && x <= 13 && y >= 1.5 && y <= 6),
    mushroom: (x, y) => (y <= 12.5 && E(x, y, 11.5, 12.5, 11.2, 10)) || (x >= 7.5 && x <= 15.5 && y > 12 && y <= 21.5),
    hat: (x, y) => inPoly(x, y, [[13, 1], [6, 17], [17.5, 17], [15, 9], [19.5, 6]]) || E(x, y, 11.5, 18.5, 11.3, 3.4),
    fish: (x, y) => E(x, y, 10, 12, 8.6, 6.4) || inPoly(x, y, [[16, 12], [22.8, 5.5], [22.8, 18.5]]),
    flower: (x, y) => C(x, y, 11.5, 11.5, 4.4) || [0, 1, 2, 3, 4].some(i => { const a = -Math.PI / 2 + i * 1.2566; return C(x, y, 11.5 + Math.cos(a) * 6.6, 12 + Math.sin(a) * 6.6, 4.8); }),
    cat: (x, y) => (x - 11.5) ** 2 + ((y - 13.5) * 1.08) ** 2 <= 9.4 ** 2 || inPoly(x, y, [[3, 10], [3.5, 1.5], [10, 6]]) || inPoly(x, y, [[13, 6], [19.5, 1.5], [20, 10]]),
    bat: (x, y) => E(x, y, 11.5, 12.5, 4.4, 6.6) || inPoly(x, y, BATL) || inPoly(x, y, BATR) || inPoly(x, y, [[8.5, 7], [9.5, 2.5], [11, 6.5]]) || inPoly(x, y, [[12, 6.5], [13.5, 2.5], [14.5, 7]]),
    bear: (x, y) => C(x, y, 11.5, 13.2, 8.8) || C(x, y, 4.6, 5.6, 3.7) || C(x, y, 18.4, 5.6, 3.7),
    rabbit: (x, y) => C(x, y, 11.5, 16, 7.2) || E(x, y, 8.3, 6, 2.6, 6) || E(x, y, 14.7, 6, 2.6, 6),
    crown: (x, y) => inPoly(x, y, [[1.5, 20], [1.5, 6.5], [7, 12.5], [11.5, 3], [16, 12.5], [21.5, 6.5], [21.5, 20]]),
    bolt: (x, y) => inPoly(x, y, [[13.5, .5], [3.5, 13.5], [10.5, 13.5], [7.5, 23.5], [20, 9], [13, 9], [17, .5]]),
    candy: (x, y) => E(x, y, 11.5, 11.5, 6.4, 5.8) || inPoly(x, y, [[6.5, 11.5], [.5, 5.5], [.5, 17.5]]) || inPoly(x, y, [[16.5, 11.5], [22.5, 5.5], [22.5, 17.5]]),
  };
  const EYES = { bear: [[8, 12], [15, 12], [11, 15], [12, 15]], rabbit: [[9, 16], [14, 16]], fish: [[6, 11]], cat: [[8, 13], [8, 14], [15, 13], [15, 14]], ghost: [[8, 10], [9, 10], [8, 11], [9, 11], [14, 10], [15, 10], [14, 11], [15, 11]], bat: [[10, 10], [13, 10]], pumpkin: [[11, 3], [12, 3]] };
  const MASKS = {};
  function mask(s){
    if (MASKS[s]) return MASKS[s]; const fn = SHAPE_FN[s] || SHAPE_FN.circle;
    const m = new Uint8Array(N * N); for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) m[y * N + x] = fn(x, y) ? 1 : 0;
    const at = (x, y) => x >= 0 && y >= 0 && x < N && y < N && m[y * N + x], d = new Uint8Array(N * N);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++){ if (!m[y * N + x]) continue; let k = 9; for (let r = 1; r <= 3 && k === 9; r++) for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) if (Math.abs(dx) + Math.abs(dy) <= r && !at(x + dx, y + dy)) k = Math.min(k, r); d[y * N + x] = k; }
    return MASKS[s] = { m, d };
  }
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t)), rgb = c => `rgb(${c[0]},${c[1]},${c[2]})`;
  const grade = b => b < 40 ? 'raw' : b < 62 ? 'gold' : b < 75 ? 'perfect' : b < 86 ? 'gold' : 'burnt';
  const flOf = f => FL.find(x => x.id === f) || FL[0], flN = f => flOf(f).n, shN = s => (SH.find(x => x[0] === s) || SH[0])[1];
  function doughCol(f, b, ring){
    const c = hex(flOf(f).c), brown = [168, 104, 52], dark = [46, 28, 20];
    let t = b < 40 ? b / 40 * .05 : b < 62 ? .05 + (b - 40) / 22 * .1 : b < 75 ? .16 : b < 86 ? .16 + (b - 75) / 11 * .14 : .32;
    t += ring * (b < 40 ? .03 : .14); let o = mix(c, brown, Math.min(.7, t));
    if (b >= 86) o = mix(o, dark, Math.min(.92, .55 + (b - 86) / 14 * .35 + ring * .1)); if (b < 25) o = mix(o, [250, 240, 225], .25 - b / 100);
    return o;
  }
  function drawCookie(q, ck, ox, oy, z){
    const { m, d } = mask(ck.s), OL = '#3A2414', ice = ck.ice || [], eyes = EYES[ck.s] || [], cols = {};
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++){
      const k = y * N + x; if (!m[k]) continue; let c;
      if (d[k] === 1) c = OL; else if (ice[k]) c = ICE[ice[k] - 1][1]; else if (eyes.some(([ex, ey]) => ex === x && ey === y)) c = OL;
      else { const ring = d[k] === 2 || (ck.s === 'pumpkin' && (x === 7 || x === 16) && y > 8 && y < 20) || (ck.s === 'candy' && (x === 6 || x === 17 || ((x - y + 40) % 5 === 0 && x > 6 && x < 17))) || (ck.s === 'mushroom' && y === 12 && x > 7 && x < 16) ? 1 : 0, hi = d[k] >= 3 && x + y < 14 && (x + y) % 5 === 0;
        const key = ring + ':' + hi; c = cols[key] || (cols[key] = rgb(mix(doughCol(ck.f, ck.b, ring), [255, 250, 235], hi ? .18 : 0))); }
      q.fillStyle = c; q.fillRect(ox + x * z, oy + y * z, z, z);
    }
    if (ck.b >= 86){ q.fillStyle = 'rgba(20,10,8,.55)'; for (let i = 0; i < 9; i++){ const x = (i * 7 + 5) % 18 + 3, y = (i * 11 + 3) % 17 + 4; if (m[y * N + x] && d[y * N + x] > 1) q.fillRect(ox + x * z, oy + y * z, z, z); } }
    (ck.top || []).forEach(t => {
      if (t.k === 'spr'){ q.fillStyle = t.c; if (t.v) q.fillRect(ox + t.x * z, oy + t.y * z, z, z * 2); else q.fillRect(ox + t.x * z, oy + t.y * z, z * 2, z); }
      else if (t.k === 'chip'){ q.fillStyle = '#4A2614'; q.fillRect(ox + t.x * z, oy + t.y * z, z * 2, z * 2); q.fillStyle = '#7A4A2E'; q.fillRect(ox + t.x * z, oy + t.y * z, z, z); }
      else { q.fillStyle = '#FFFFFF'; q.fillRect(ox + t.x * z, oy + t.y * z, z * 2, z * 2); q.fillStyle = '#D8D0E8'; q.fillRect(ox + (t.x + 1) * z, oy + (t.y + 1) * z, z, z); }
    });
  }
  function cookieImg(ck){ const c = document.createElement('canvas'); c.width = N; c.height = N; drawCookie(c.getContext('2d'), ck, 0, 0, 1); return c; }
  // 저장: 아이싱은 같은 칸이 이어지면 줄여서 「색 개수」로
  function enc(c){ let s = '', i = 0; const a = c.ice || []; while (i < N * N){ const v = a[i] || 0; let j = i; while (j < N * N && (a[j] || 0) === v) j++; s += v + (j - i).toString(36) + '.'; i = j; } return { f: c.f, s: c.s, b: Math.round(c.b), q: c.q || '보통', i: s, t: (c.top || []).map(t => [t.k, t.x, t.y, Math.max(0, SPR.indexOf(t.c)), t.v ? 1 : 0]) }; }
  function dec(o){ if (!o) return null; const ice = new Uint8Array(N * N); let p = 0; String(o.i || '').split('.').forEach(seg => { if (!seg) return; const v = +seg[0], n = parseInt(seg.slice(1), 36) || 0; for (let k = 0; k < n && p < N * N; k++) ice[p++] = v; }); return { f: o.f, s: o.s, b: o.b, q: o.q, ice, top: (o.t || []).map(([k, x, y, c, v]) => ({ k, x, y, c: SPR[c] || SPR[0], v })) }; }
  // ---------- 상자 그림 (위 · 앞 · 옆이 보이는 입체 도트) ----------
  const BOX_OL = '#2A1A2E', HEART5 = ['01010', '11111', '11111', '01110', '00100'];
  function fillShape(g, inside, x0, y0, x1, y1, fn, edge){ for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++){ if (!inside(x + .5, y + .5)) continue; const e = edge && (!inside(x - .5, y + .5) || !inside(x + 1.5, y + .5) || !inside(x + .5, y - .5) || !inside(x + .5, y + 1.5)); const c = e ? edge : fn(x, y); if (c){ g.fillStyle = c; g.fillRect(x, y, 1, 1); } } }
  function boxPat(P, u, v){ u = Math.floor(u); v = Math.floor(v);
    if (P === 'dot'){ const r = Math.floor(v / 5), uu = (u + (r % 2) * 3) % 6, vv = ((v % 5) + 5) % 5; return (uu === 1 || uu === 2) && (vv === 1 || vv === 2); }
    if (P === 'stripe') return ((u % 6) + 6) % 6 < 2;
    if (P === 'heart'){ const r = Math.floor(v / 7), uu = ((u + (r % 2) * 4) % 8 + 8) % 8, vv = ((v % 7) + 7) % 7; return uu < 5 && vv < 5 && HEART5[vv][uu] === '1'; }
    return false; }
  function boxCols(B){ const base = hex(BOXC[B.c] || BOXC[0]), lum = base[0] * .3 + base[1] * .59 + base[2] * .11, light = lum > 225, sh = (c, k) => rgb(mix(c, [60, 30, 50], k)), hi = (c, k) => rgb(mix(c, [255, 255, 255], k));
    const motif = c => light ? rgb(mix(hex('#F4A0B8'), c, .25)) : rgb(mix(c, [255, 255, 255], .5)), r = hex(RIB[B.r] || RIB[0]);
    return { top: hi(base, .25), front: rgb(base), side: sh(base, .22), lid: hi(base, .1), seam: sh(base, .35), mTop: motif(mix(base, [255, 255, 255], .25)), mFront: motif(base), mSide: motif(mix(base, [60, 30, 50], .22)), r: rgb(r), rTop: hi(r, .25), rSide: sh(r, .25), rDark: sh(r, .45), P: (PAT[B.p] || PAT[0])[0] }; }
  function drawBoxClosed(g, B){ const K = boxCols(B), P = K.P;
    fillShape(g, (x, y) => ((x - 31) / 25) ** 2 + ((y - 43) / 3.2) ** 2 <= 1, 4, 39, 58, 47, () => 'rgba(0,0,0,.28)');
    fillShape(g, (x, y) => x >= 50 && x <= 57 && y >= 22 - (x - 50) * 10 / 7 && y <= 42 - (x - 50) * 10 / 7, 50, 11, 57, 42, (x, y) => { const v = y - (22 - (x - 50) * 10 / 7); if (x >= 53 && x <= 55) return x === 55 ? K.rDark : K.rSide; if (v < 4) return v === 3 ? K.seam : K.side; return boxPat(P, x * 2, v) ? K.mSide : K.side; }, BOX_OL);
    fillShape(g, (x, y) => y >= 12 && y <= 22 && x >= 8 + (22 - y) * .6 && x <= 50 + (22 - y) * .6 + .01, 8, 12, 57, 22, (x, y) => { const v = 22 - y, u = x - 8 - v * .6; if (u >= 19 && u < 24) return u >= 23 ? K.r : K.rTop; if (v >= 4 && v <= 6) return v === 4 ? K.r : K.rTop; return boxPat(P, u, v) ? K.mTop : K.top; }, BOX_OL);
    fillShape(g, (x, y) => x >= 8 && x <= 50.01 && y >= 22 && y <= 42, 8, 22, 50, 42, (x, y) => { const u = x - 8, v = y - 22; if (u >= 19 && u < 24) return u === 23 ? K.rDark : K.r; if (v < 4) return v === 3 ? K.seam : (boxPat(P, u, v + 20) ? K.mFront : K.lid); return boxPat(P, u, v) ? K.mFront : K.front; }, BOX_OL);
    const tail = pts => fillShape(g, (x, y) => inPoly(x, y, pts), 20, 14, 44, 32, () => K.r, BOX_OL); tail([[30, 16], [33, 16], [27, 30], [25, 27]]); tail([[31, 16], [34, 16], [39, 27], [37, 30]]);
    const loop = cx => fillShape(g, (x, y) => ((x - cx) / 6) ** 2 + ((y - 13) / 4) ** 2 <= 1, cx - 7, 8, cx + 7, 18, (x, y) => ((x - cx) / 3.2) ** 2 + ((y - 13) / 1.8) ** 2 <= 1 ? K.rDark : (y < 12 ? K.rTop : K.r), BOX_OL); loop(26.5); loop(37.5);
    fillShape(g, (x, y) => x >= 29.5 && x <= 34.5 && y >= 10.5 && y <= 16.5, 29, 10, 35, 17, (x, y) => y < 13 ? K.rTop : K.r, BOX_OL);
    g.fillStyle = 'rgba(255,255,255,.7)'; g.fillRect(31, 12, 1, 1); g.fillRect(24, 11, 2, 1); }
  function drawBoxOpen(g, B, cks){ const K = boxCols(B), P = K.P;
    fillShape(g, (x, y) => ((x - 60) / 50) ** 2 + ((y - 87) / 5) ** 2 <= 1, 8, 80, 116, 93, () => 'rgba(0,0,0,.28)');
    fillShape(g, (x, y) => inPoly(x, y, [[34, 6], [108, 6], [110, 40], [32, 40]]), 31, 5, 111, 41, (x, y) => { const u = x - 33; if (u >= 36 && u < 42) return u === 41 ? K.rDark : K.r; if (y > 36) return K.seam; return boxPat(P, u, y) ? K.mTop : K.top; }, BOX_OL);
    fillShape(g, (x, y) => y >= 38 && y <= 62 && x >= 14 + (62 - y) * .58 && x <= 92 + (62 - y) * .58, 14, 38, 107, 62, (x, y) => y < 43 ? K.seam : x > 88 + (62 - y) * .58 ? K.seam : ((x + y) % 6 === 0 ? '#F0DCC6' : '#FFF6EC'), BOX_OL);
    [[34, 33], [62, 33], [24, 45], [52, 45]].forEach(([x, y], i) => { const ck = cks[i]; if (ck) drawCookie(g, ck, x, y, 1); else { g.fillStyle = 'rgba(120,80,60,.12)'; g.fillRect(x + 3, y + 8, 18, 10); } });
    fillShape(g, (x, y) => x >= 92 && x <= 106 && y >= 62 - (x - 92) * 24 / 14 && y <= 86 - (x - 92) * 24 / 14, 92, 37, 106, 87, (x, y) => boxPat(P, x * 2, y - (92 - x)) ? K.mSide : K.side, BOX_OL);
    fillShape(g, (x, y) => x >= 14 && x <= 92.01 && y >= 62 && y <= 86, 14, 62, 92, 86, (x, y) => { const u = x - 14, v = y - 62; if (v < 3) return K.lid; return boxPat(P, u, v) ? K.mFront : K.front; }, BOX_OL);
    fillShape(g, (x, y) => y >= 85 + Math.sin(x / 5) * 2 && y <= 89 + Math.sin(x / 5) * 2 && x >= 66 && x <= 116, 66, 80, 116, 93, (x, y) => y > 87 + Math.sin(x / 5) * 2 ? K.rDark : K.r, BOX_OL); }
  const boxCache = new Map();
  function boxImg(B, open, cks){ const key = open ? null : `${B.c}:${B.r}:${B.p}`; if (key && boxCache.has(key)) return boxCache.get(key); const c = document.createElement('canvas'); c.width = open ? 120 : 60; c.height = open ? 96 : 48; const g = c.getContext('2d'); if (open) drawBoxOpen(g, B, cks || []); else drawBoxClosed(g, B); if (key) boxCache.set(key, c); return c; }
  function boxTo(cv, B, open, cks){ const q = cv.getContext('2d'); q.imageSmoothingEnabled = false; q.clearRect(0, 0, cv.width, cv.height); q.drawImage(boxImg(B, open, cks), 0, 0, cv.width, cv.height); }
  // ---------- 재료 아이콘 (캔버스에 그릴 때) ----------
  const imgs = {}; const icImg = k => { const s = iconSrc(k); if (!s) return null; const im = imgs[s.src] || (imgs[s.src] = Object.assign(new Image(), { src: s.src })); return im.complete && im.naturalWidth ? [im, s] : null; };
  const icon = (q, k, x, y, sz = 16) => { const r = icImg(k); if (r) q.drawImage(r[0], r[1].sx, r[1].sy, r[1].sw, r[1].sh, Math.round(x), Math.round(y), sz, sz); };

  // ---------- 상태 ----------
  let ctl = null, yum = {}, offs = [], yumChk = 0, W = { tab: 'bake', step: -1, cur: null, pickF: 'butter', pickS: null, tier: 1, tool: 'ice0', sel: [], bc: 0, br: 0, bp: 0, last: null }, MG = null, ovenOK = '';
  const ck = () => me.ck || (me.ck = { dex: {}, tray: [], boxes: [], found: {}, gave: 0 });
  const dexN = () => Object.keys(ck().dex || {}).length;
  const starOpen = s => dexN() >= UNLOCK[s];
  const inm = k => (typeof ITEM !== 'undefined' && ITEM[k]) || k;
  const has = k => typeof haveSame === 'function' ? haveSame(k) : (me.inv[k] || 0), take = (k, n = 1) => typeof takeSame === 'function' ? takeSame(k, n) : (me.inv[k] = Math.max(0, (me.inv[k] || 0) - n));
  const canBake = f => BASE.every(k => has(k) > 0) && has(flOf(f).it) > 0;

  // ---------- 창 ----------
  function open(tab){ if (!(me.ck && me.ck.met)) return; if (uiBusy() && !ckOn) return; W.tab = tab || W.tab; ckOn = true; let v = $('#ckv'); if (!v){ v = document.createElement('div'); v.id = 'ckv'; document.body.appendChild(v); } render(); requestAnimationFrame(() => v.classList.add('on')); sfx('pop'); }
  function close(){ stopMG(); const v = $('#ckv'); if (v){ v.classList.remove('on'); setTimeout(() => v.remove(), 300); } if (W.step >= 0 && W.step < 6 && W.cur) W.keep = true; ckOn = false; }
  const sec = (title, body, aside = '') => `<section class="cd"><div class="cdh"><h3>${title}</h3>${aside}</div>${body}</section>`;
  const tipHTML = t => `<div class="tip2"><canvas data-ckface="1" width="32" height="32"></canvas><p>${t}</p></div>`;
  function stepBar(){ const i = Math.min(W.step, 5); return `<div class="pg"><div class="pgt"><b>${flN(W.cur.f)} ${shN(W.cur.s)} 쿠키</b><span class="st">${'★'.repeat(SH_STAR[W.cur.s])}</span><em id="ckmgst"></em><span class="pgn">${W.step <= 4 ? `${W.step + 1} / 5 · ${STEP_N[W.step]}` : W.step === 5 ? '완성' : '꾸미기'}</span></div><div class="pgb">${[0, 1, 2, 3, 4].map(k => `<i class="${k < i ? 'd' : k === i ? 'o' : ''}"></i>`).join('')}</div></div>`; }
  function render(){
    const v = $('#ckv'); if (!v) return; stopMG(); const K = ck();
    const T = [['bake', '굽기', ''], ['box', '상자', (K.tray || []).length || ''], ['dex', '도감', '']];
    v.innerHTML = `<div class="hd"><b>마들렌의 쿠키 상자</b><button data-ckx="close" aria-label="닫기">✕</button></div><div class="tabs">${T.map(([k, n, b]) => `<button data-cktab="${k}" class="${W.tab === k ? 'on' : ''}">${n}${b ? `<i>${b}</i>` : ''}</button>`).join('')}</div><div class="bd">${W.tab === 'bake' ? bakeHTML() : W.tab === 'box' ? boxHTML() : dexHTML()}</div>`;
    after(); if (W.tab === 'bake' && W.step >= 0 && W.step <= 4) startMG(W.step);
  }
  function bakeHTML(){
    if (W.step === -1){
      const atOven = World.where() === 'candy'; if (!atOven) return `<p class="empty">쿠키는 과자 교실 오븐에서 구워요. 과자 교실에 가서 오븐을 눌러 주세요.</p>`;
      const f = W.pickF, tier = W.tier, op = starOpen(tier), selS = W.pickS && SH_STAR[W.pickS] === tier ? W.pickS : null, can = canBake(f);
      return sec('반죽', `<div class="chips">${FL.map(x => `<button class="chip ${f === x.id ? 'on' : ''}" data-ckfl="${x.id}" ${has(x.it) ? '' : 'disabled'}><i style="background:${x.c}"></i>${x.n}<small>${has(x.it)}</small></button>`).join('')}</div><p class="s">한 판에 밀 이삭 1 · 달걀 1 · ${esc(inm(flOf(f).it))} 1 → 쿠키 2 개</p>`,
          `<span class="aside">밀 이삭 ${has('g_wheat')} · 달걀 ${has('hegg')}</span>`)
        + sec('모양 틀', `<div class="seg">${[1, 2, 3].map(t => `<button data-cktier="${t}" class="${tier === t ? 'on' : ''}">${'★'.repeat(t)}${starOpen(t) ? '' : ' <small>잠김</small>'}</button>`).join('')}</div>
          ${op ? `<div class="shapes">${SH.filter(([k]) => SH_STAR[k] === tier).map(([k, n]) => `<button class="shp2 ${selS === k ? 'on' : ''}" data-cksh="${k}"><canvas data-ckpv="${f}:${k}" width="48" height="48"></canvas><span>${n}</span>${K_dex()[f + '_' + k] ? '<i class="dot"></i>' : ''}</button>`).join('')}</div>` : `<p class="empty">도감 ${UNLOCK[tier]} 종을 채우면 열려요 · 지금 ${dexN()} 종</p>`}`)
        + `<button class="btn go wide" data-ckx="start" ${selS && can && (ck().tray || []).length < TRAY_MAX ? '' : 'disabled'}>${(ck().tray || []).length >= TRAY_MAX ? '쟁반이 꽉 찼어요 · 상자에 담아 주세요' : !can ? '재료가 모자라요' : selS ? `${flN(f)} ${shN(selS)} 쿠키 굽기 · 2 개` : '모양 틀을 골라요'}</button>`;
    }
    const s = SH_STAR[W.cur.s];
    if (W.step <= 4) return `${stepBar()}<div class="mgw"><canvas id="ckmg" width="480" height="336"></canvas><div class="mgmsg" id="ckmgmsg"></div></div>${tipHTML(TIPS[W.step](s))}<div class="row" id="ckmgbar"></div>`;
    if (W.step === 5){ const c = W.cur, R = c.res, d = W.last; return `${stepBar()}<div class="res2"><canvas id="ckres" width="96" height="96"></canvas><b class="q q${c.q}">${c.q === '숯' ? '숯 쿠키' : c.q}</b>${d ? `<p class="new">도감 등록 · ${esc(d)}</p>` : ''}<div class="rl">${STEP_N.slice(0, 5).map((n, i) => `<span class="g${R[i]}">${n}<b>${R[i]}</b></span>`).join('')}</div></div>
      ${tipHTML(c.q === '최고' ? '와.... 이건 진열대 맨 앞에 둘 쿠키야. 나보다 잘 구운 거 아니야?' : c.q === '맛있음' ? '맛있다! 가장자리까지 고르게 잘 익었어.' : c.q === '보통' ? '먹을 만해. 다음엔 젓는 거랑 미는 거 조금만 더 꼼꼼히.' : '....괜찮아. 나도 오늘 아침에 한 판 태웠어. 이건 도감에 「숯 쿠키」로 남겨 둘게.')}<button class="btn go wide" data-ckx="todeco">꾸미러 가기</button>`; }
    return `${stepBar()}<div class="deco2"><canvas class="big" id="ckdcv" width="240" height="240"></canvas></div>
      <div class="tool2"><span>아이싱</span><div class="sw">${ICE.map(([n, c], i) => `<button data-ckice="${i}" style="background:${c}" class="${W.tool === 'ice' + i ? 'on' : ''}" aria-label="${n}"></button>`).join('')}<button data-ckice="x" class="er ${W.tool === 'erase' ? 'on' : ''}">지움</button></div></div>
      <div class="tool2"><span>토핑</span><div class="tb">${TOP.map(([k, n]) => `<button data-cktop="${k}" class="${W.tool === k ? 'on' : ''}">${n}</button>`).join('')}</div></div>
      <div class="row sm"><button class="lnk" data-ckx="undo">토핑 하나 빼기</button><button class="lnk" data-ckx="clr">처음부터</button></div><button class="btn go wide" data-ckx="decodone">쟁반에 올리기</button>`;
  }
  const K_dex = () => ck().dex || (ck().dex = {});
  function boxHTML(){
    const K = ck(), tray = K.tray || [], boxes = K.boxes || [];
    return sec('쟁반', tray.length ? `<div class="tray2">${tray.map((c, i) => `<button class="ck2 ${W.sel.includes(i) ? 'on' : ''}" data-ckck="${i}" aria-label="${flN(c.f)} ${shN(c.s)}"><canvas data-ckc="${i}" width="48" height="48"></canvas>${W.sel.includes(i) ? `<i>${W.sel.indexOf(i) + 1}</i>` : ''}</button>`).join('')}</div>` : '<p class="empty">구운 쿠키가 없어요</p>', `<span class="aside">${W.sel.length} / 4</span>`)
      + sec('상자', `<div class="boxed2"><canvas id="ckbx" width="120" height="96"></canvas><div class="opts">
        <div class="tool2"><span>색</span><div class="sw">${BOXC.map((c, i) => `<button data-ckbc="${i}" style="background:${c}" class="${W.bc === i ? 'on' : ''}" aria-label="상자 색 ${i + 1}"></button>`).join('')}</div></div>
        <div class="tool2"><span>리본</span><div class="sw">${RIB.map((c, i) => `<button data-ckrb="${i}" style="background:${c}" class="${W.br === i ? 'on' : ''}" aria-label="리본 ${i + 1}"></button>`).join('')}</div></div>
        <div class="tool2"><span>무늬</span><div class="tb">${PAT.map(([k, n], i) => `<button data-ckpt="${i}" class="${W.bp === i ? 'on' : ''}">${n}</button>`).join('')}</div></div></div></div>`)
      + `<button class="btn go wide" data-ckx="pack" ${W.sel.length && boxes.length < BOX_MAX ? '' : 'disabled'}>${boxes.length >= BOX_MAX ? `상자는 ${BOX_MAX} 개까지 들고 있을 수 있어요` : W.sel.length ? `포장하기 · ${W.sel.length} 개` : '쟁반에서 쿠키를 골라요'}</button>`
      + sec('포장한 상자', boxes.length ? `<div class="boxes2">${boxes.map((b, i) => `<span><canvas data-ckbxi="${i}" width="60" height="48"></canvas></span>`).join('')}</div><p class="s">NPC에게 말을 걸고 「선물」에서 줄 수 있어요 · 하루 한 번과 상관없어요</p>` : '<p class="empty">아직 없어요</p>', `<span class="aside">${boxes.length} / ${BOX_MAX}</span>`);
  }
  function dexHTML(){
    const n = dexN(), D = K_dex(), found = ck().found || {};
    return `<div class="dexsum"><b>${n}</b><span>/ ${DEX.length}</span><div class="pgb one"><i style="width:${n / DEX.length * 100}%"></i></div></div>`
      + sec('모양별', `<div class="dex2">${SH.map(([k, nm]) => { const got = FL.filter(f => D[f.id + '_' + k]); return `<div class="dx2 ${got.length ? 'on' : ''}"><canvas data-ckdexs="${k}" width="48" height="48"></canvas><span>${nm}</span><b class="dots">${FL.map(f => `<i style="${D[f.id + '_' + k] ? `background:${f.c};border-color:${f.c}` : ''}" title="${f.n}"></i>`).join('')}</b></div>`; }).join('')}</div><div class="dlg">${FL.map(f => `<span><i style="background:${f.c}"></i>${f.n}</span>`).join('')}</div>`)
      + sec('숨은 쿠키', `<div class="hid2">${DEX.slice(-2).map(d => { const g = D[d.id]; return `<div class="${g ? 'on' : ''}"><canvas data-ckdex="${d.id}" width="48" height="48"></canvas><div><b>${g ? d.n : '???'}</b><p>${g ? g : d.hid}</p></div></div>`; }).join('')}</div>`)
      + `<details class="cd note"><summary>마들렌의 단골 수첩</summary><div class="hints2">${Object.entries(NPCS).map(([id, x]) => { const g = found[id] || {}, nn = npcGet(id); return `<div><canvas data-cknf="${id}" width="32" height="32"></canvas><div><b>${esc(nn ? nn.name : id)}</b><span class="${g.f ? 'got' : ''}">${g.f ? flN(x.f) : '맛 ?'}</span><span class="${g.s ? 'got' : ''}">${g.s ? shN(x.s) : '모양 ?'}</span><p>${x.hint}</p></div></div>`; }).join('')}</div></details>`;
  }
  const faceTo = (cv, id) => { const g = cv.getContext('2d'); g.imageSmoothingEnabled = false; try { knFace(npcGet(id))(g); } catch(e){} };
  function after(){
    const v = $('#ckv'); if (!v) return; const K = ck();
    v.querySelectorAll('[data-ckface]').forEach(c => faceTo(c, 'madeleine'));
    v.querySelectorAll('[data-cknf]').forEach(c => faceTo(c, c.dataset.cknf));
    v.querySelectorAll('[data-ckpv]').forEach(c => { const [f, s] = c.dataset.ckpv.split(':'); drawCookie(c.getContext('2d'), { f, s, b: 0 }, 0, 0, 2); });
    v.querySelectorAll('[data-ckc]').forEach(c => { const o = dec(K.tray[+c.dataset.ckc]); if (o) drawCookie(c.getContext('2d'), o, 0, 0, 2); });
    v.querySelectorAll('[data-ckdexs]').forEach(c => { const k = c.dataset.ckdexs, f = FL.find(f => K_dex()[f.id + '_' + k]), q = c.getContext('2d'); drawCookie(q, { f: f ? f.id : 'butter', s: k, b: 62 }, 0, 0, 2); if (!f){ q.globalCompositeOperation = 'source-atop'; q.fillStyle = '#3A2A55'; q.fillRect(0, 0, 48, 48); q.globalCompositeOperation = 'source-over'; } });
    v.querySelectorAll('[data-ckdex]').forEach(c => { const d = DEX.find(x => x.id === c.dataset.ckdex), q = c.getContext('2d'); drawCookie(q, { f: d.f, s: d.s, b: d.b ?? 66, ice: d.gold ? goldIce(d.s) : null }, 0, 0, 2); if (!K_dex()[d.id]){ q.globalCompositeOperation = 'source-atop'; q.fillStyle = '#3A2A55'; q.fillRect(0, 0, 48, 48); q.globalCompositeOperation = 'source-over'; } });
    v.querySelectorAll('[data-ckbxi]').forEach(c => boxTo(c, K.boxes[+c.dataset.ckbxi], false));
    const bx = $('#ckbx'); if (bx) boxTo(bx, { c: W.bc, r: W.br, p: W.bp }, true, W.sel.map(i => dec(K.tray[i])));
    const rs = $('#ckres'); if (rs){ const q = rs.getContext('2d'); q.clearRect(0, 0, 96, 96); drawCookie(q, W.cur, 0, 0, 4); }
    if ($('#ckdcv')) decoDraw();
  }
  function goldIce(s){ const { m, d } = mask(s), a = new Uint8Array(N * N); for (let k = 0; k < N * N; k++) if (m[k] && d[k] === 2) a[k] = 4; return a; }

  // ---------- 굽기 미니게임 (작업대 도트 160 × 112) ----------
  const MW = 160, MH = 112, OL = '#3A2414';
  function stopMG(){ if (MG){ MG.dead = true; MG = null; } }
  const px = (q, x, y, w, h, c) => { q.fillStyle = c; q.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h)); };
  function board(q){ px(q, 0, 0, MW, MH, '#E2BE8C'); for (let y = 0; y < MH; y += 14){ px(q, 0, y, MW, 1, '#C89C68'); for (let x = (y / 14 % 2) * 37 + 11; x < MW; x += 74) px(q, x, y, 1, 14, '#C89C68'); } px(q, 0, 0, MW, 2, '#A87A4A'); }
  function bowlBig(q, x, y, r, wob = 0){ x += wob; [[-r, -4, r * 2, 2], [-r + 1, -2, r * 2 - 2, 6], [-r + 3, 4, r * 2 - 6, 6], [-r + 7, 10, r * 2 - 14, 4]].forEach(([dx, dy, w, h]) => px(q, x + dx - 1, y + dy - 1, w + 2, h + 2, OL));
    px(q, x - r, y - 4, r * 2, 2, '#FFE8EC'); px(q, x - r + 1, y - 2, r * 2 - 2, 6, '#F49AAA'); px(q, x - r + 3, y + 4, r * 2 - 6, 6, '#E4889A'); px(q, x - r + 7, y + 10, r * 2 - 14, 4, '#C86A7A'); px(q, x - r + 4, y, 6, 2, '#FFD0D8'); }
  function bowlTop(q, x, y, rx, ry){ q.fillStyle = OL; q.beginPath(); q.ellipse(x, y, rx + 2, ry + 2, 0, 0, 7); q.fill(); q.fillStyle = '#F49AAA'; q.beginPath(); q.ellipse(x, y, rx, ry, 0, 0, 7); q.fill(); q.fillStyle = '#FFE8EC'; q.beginPath(); q.ellipse(x, y, rx - 4, ry - 3, 0, 0, 7); q.fill(); }
  function sheet(q, x, y, w, h, th, col){ const t = Math.max(1, Math.round(th / 5)); px(q, x - 1, y - 1, w + 2, h + t + 2, OL); px(q, x, y + h, w, t, rgb(mix(hex(col), [120, 70, 30], .35))); px(q, x, y, w, h, col); px(q, x + 2, y + 2, w - 4, 1, rgb(mix(hex(col), [255, 255, 255], .35))); }
  function pin(q, x, y, w){ px(q, x - w / 2 - 9, y - 3, w + 18, 7, OL); px(q, x - w / 2 - 8, y - 2, 8, 5, '#8A5A34'); px(q, x + w / 2, y - 2, 8, 5, '#8A5A34'); px(q, x - w / 2, y - 3, w, 7, OL); px(q, x - w / 2 + 1, y - 2, w - 2, 5, '#E8B878'); px(q, x - w / 2 + 1, y - 2, w - 2, 1, '#F8D8A8'); }
  function cutterAt(q, s, x, y, col){ const { m, d } = mask(s); for (let k = 0; k < N * N; k++) if (m[k] && d[k] === 1) px(q, x + k % N - 12, y + (k / N | 0) - 12, 1, 1, col); }
  function mgText(q, t, x, y, c = '#FFE9A0', sz = 9){ q.font = `${sz}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = 3; q.strokeStyle = OL; q.strokeText(t, x, y); q.fillStyle = c; q.fillText(t, x, y); q.textAlign = 'left'; }
  function bar(q, x, y, w, h, k, col){ px(q, x - 1, y - 1, w + 2, h + 2, OL); px(q, x, y, w, h, '#4A3828'); px(q, x, y, Math.round(w * Math.max(0, Math.min(1, k))), h, col); }
  function mgPos(e){ const c = $('#ckmg'), r = c.getBoundingClientRect(); return [(e.clientX - r.left) / r.width * MW, (e.clientY - r.top) / r.height * MH]; }
  function mgMsg(t, ms = 900){ const el = $('#ckmgmsg'); if (!el) return; el.textContent = t; el.classList.add('on'); clearTimeout(mgMsg.t); mgMsg.t = setTimeout(() => el && el.classList.remove('on'), ms); }
  function startMG(step){
    const c = $('#ckmg'); if (!c) return; const q = c.getContext('2d'); q.setTransform(3, 0, 0, 3, 0, 0); q.imageSmoothingEnabled = false;
    const cur = W.cur, s = SH_STAR[cur.s], fl = flOf(cur.f), dc = fl.c; MG = { step, t0: performance.now(), miss: 0, done: false }; const G = MG;
    const finish = (gr, msg) => { if (G.done) return; G.done = true; cur.res[step] = gr; mgMsg(msg || gr, 1100); sfx(gr === '완벽' ? 'sparkle' : gr === '탐' ? 'hurt' : 'pop'); setTimeout(() => { if (G.dead) return; W.step = step + 1; if (step === 4) settle(); render(); }, 1150); };
    const gradeOf = m => m === 0 ? '완벽' : m === 1 ? '좋아' : '아쉬워', bar$ = $('#ckmgbar');
    if (step === 0){
      const pool = ['milk', 'honey', 'hegg', 'g_wheat', ...FL.map(f => f.it)], extra = ['milk', 'honey', 'hegg'].filter(k => k !== fl.it);
      G.need = s === 1 ? ['g_wheat', 'hegg', fl.it] : s === 2 ? ['g_wheat', 'hegg', extra[0], fl.it] : ['g_wheat', 'hegg', extra[0], fl.it, extra[1]];
      const shelf = [...new Set([...G.need, ...[...new Set(pool)].filter(k => !G.need.includes(k)).sort(() => Math.random() - .5).slice(0, s === 1 ? 1 : s === 2 ? 2 : 3)])].sort(() => Math.random() - .5);
      G.shelf = shelf.map((k, i) => ({ k, x: 8 + i * (144 / shelf.length) + (144 / shelf.length - 18) / 2, y: 14, used: false })); G.got = []; G.lim = s === 3 ? 10 : 0; G.fly = [];
      G.tap = (x, y) => { if (G.done) return; const it = G.shelf.find(o => !o.used && x >= o.x - 2 && x <= o.x + 20 && y >= o.y - 2 && y <= o.y + 22); if (!it) return;
        const want = s === 1 ? G.need.filter((k, i) => G.got.filter(g => g === k).length < G.need.filter(n => n === k).length) : [G.need[G.got.length]], cnt = G.need.filter(k => k === it.k).length, hv = G.got.filter(k => k === it.k).length;
        if (want.includes(it.k) && hv < cnt){ G.got.push(it.k); sfx('pop'); if (G.got.filter(k => k === it.k).length >= cnt) it.used = true; G.fly.push({ k: it.k, x0: it.x, y0: it.y, t0: performance.now() }); if (G.got.length === G.need.length) setTimeout(() => finish(gradeOf(G.miss)), 500); }
        else { G.miss++; G.shake = performance.now(); mgMsg(G.need.includes(it.k) ? '순서가 달라' : '그건 안 넣어'); } };
      G.draw = now => { board(q); px(q, 0, 0, MW, 40, '#C89C68'); px(q, 0, 38, MW, 3, '#8A5A34'); px(q, 0, 41, MW, 2, OL);
        G.shelf.forEach(o => { if (!o.used) icon(q, o.k, o.x, o.y, 18); });
        G.need.forEach((k, i) => { const x = 6 + i * 14, y = 48; px(q, x - 1, y - 1, 14, 14, OL); px(q, x, y, 12, 12, '#FFF6E8'); icon(q, k, x, y, 12); if (i < G.got.length){ px(q, x, y, 12, 12, 'rgba(111,208,140,.55)'); mgText(q, '✓', x + 6, y + 10, '#FFFFFF', 9); } else if (s > 1 && i === G.got.length) px(q, x - 1, y + 13, 14, 2, '#FF9A3C'); });
        const wob = G.shake && now - G.shake < 300 ? Math.sin(now / 20) * 2 : 0; bowlBig(q, 80, 86, 30, wob); if (G.got.length) px(q, 58 + wob, 82, 44, 4, G.got.length === G.need.length ? dc : '#F4EAD8');
        G.fly = G.fly.filter(f => now - f.t0 < 520); G.fly.forEach(f => { const k = (now - f.t0) / 500; icon(q, f.k, f.x0 + (72 - f.x0) * k, f.y0 + (74 - f.y0) * k - Math.sin(k * Math.PI) * 24, 18 - k * 6); });
        if (G.lim && !G.done){ const left = G.lim - (now - G.t0) / 1000; bar(q, 100, 50, 54, 5, left / G.lim, left < 3 ? '#FF6B6B' : '#FFD866'); if (left <= 0){ G.miss += 2; finish('아쉬워', '시간 끝'); } } };
    }
    if (step === 1){
      G.need = [3, 5, 7][s - 1]; G.turn = 0; G.ang = 0; G.prev = null; G.lastSpill = 0; G.drops = []; const cx = 80, cy = 60;
      G.move = (x, y, now) => { if (G.done) return; const a = Math.atan2(y - cy, (x - cx) * .8); if (G.prev){ let da = a - G.prev.a; if (da > Math.PI) da -= 7; if (da < -Math.PI) da += 7; const dt = Math.max(1, now - G.prev.t) / 1000, sp = Math.abs(da) / dt;
          if (s === 3 && sp > 16){ if (now - G.lastSpill > 500){ G.lastSpill = now; G.miss++; mgMsg('철퍽! 살살'); for (let i = 0; i < 4; i++) G.drops.push({ x: cx + Math.cos(a) * 40, y: cy + Math.sin(a) * 26, vx: Math.cos(a + i) * 30, vy: -20 - i * 6, t0: now }); } }
          else { G.turn += Math.abs(da) / 6.283; G.ang += da; } }
        G.prev = { a, t: now }; if (G.turn >= G.need) finish(gradeOf(G.miss)); };
      G.up = () => { G.prev = null; };
      G.alt = () => { if (G.done) return; G.turn += .34; G.ang += 2.1; if (G.turn >= G.need) finish(G.miss ? '좋아' : '완벽'); };
      bar$.innerHTML = '<button class="btn" data-ckx="mgalt" style="flex:1">손가락이 어려우면 · 휘휘 젓기 버튼</button>';
      G.draw = now => { board(q); bowlTop(q, cx, cy, 52, 34); const k = Math.min(1, G.turn / G.need), base = mix(hex('#F4EAD8'), hex(dc), k);
        q.fillStyle = OL; q.beginPath(); q.ellipse(cx, cy + 2, 42, 26, 0, 0, 7); q.fill(); q.fillStyle = rgb(base); q.beginPath(); q.ellipse(cx, cy + 2, 40, 24, 0, 0, 7); q.fill();
        q.strokeStyle = rgb(mix(base, [255, 255, 255], .4)); q.lineWidth = 2; for (let i = 0; i < 3; i++){ q.beginPath(); q.ellipse(cx, cy + 2, 30 - i * 9, 18 - i * 5.5, 0, G.ang + i * 2, G.ang + i * 2 + 2.2); q.stroke(); }
        if (k < .6) for (let i = 0; i < 6; i++){ const a = i * 1.1 + G.ang * .7; px(q, cx + Math.cos(a) * 20, cy + Math.sin(a) * 12, 3, 2, 'rgba(255,255,255,.8)'); }
        const wa = G.ang; px(q, cx + Math.cos(wa) * 26 - 2, cy + Math.sin(wa) * 15 - 22, 4, 22, '#8A5A34'); px(q, cx + Math.cos(wa) * 26 - 4, cy + Math.sin(wa) * 15 - 2, 8, 6, OL); px(q, cx + Math.cos(wa) * 26 - 3, cy + Math.sin(wa) * 15 - 1, 6, 4, '#E8B878');
        if (G.turn < .2){ q.strokeStyle = 'rgba(255,255,255,.85)'; q.setLineDash([3, 3]); q.lineWidth = 1.5; q.beginPath(); q.ellipse(cx, cy + 2, 34, 20, 0, now / 300, now / 300 + 5); q.stroke(); q.setLineDash([]); mgText(q, '빙글빙글', cx, cy + 5, '#FFFFFF', 9); }
        G.drops = G.drops.filter(d => now - d.t0 < 700); G.drops.forEach(d => { const t = (now - d.t0) / 1000; px(q, d.x + d.vx * t, d.y + d.vy * t + 60 * t * t, 3, 3, dc); });
        bar(q, 8, 102, 144, 5, k, '#6FD08C'); mgText(q, `${Math.min(G.need, Math.floor(G.turn))} / ${G.need} 바퀴`, 80, 98, '#FFFFFF', 8); };
    }
    if (step === 2){
      G.th = 30; G.zone = [[7, 17], [9, 14], [10, 13]][s - 1]; G.py = 50; G.sw = null; G.flat = 0;
      G.down = (x, y) => { G.sw = { y0: y }; G.py = y; };
      G.move = (x, y) => { if (!G.sw || G.done) return; G.py = Math.max(30, Math.min(92, y)); if (Math.abs(y - G.sw.y0) > 22){ G.th = Math.max(2, G.th - (1 + (G.th - 8) * .2) * (.85 + Math.random() * .3)); G.flat = performance.now(); G.sw.y0 = y; if (G.th < G.zone[0]){ G.miss += 2; finish('아쉬워', '앗, 찢어졌어'); } } };
      G.up = () => { G.sw = null; }; G.roll = () => { G.down(0, 40); G.move(0, 70); G.up(); };
      bar$.innerHTML = '<button class="btn" data-ckx="mgroll" style="flex:1">밀대 한 번 밀기</button><button class="btn go" data-ckx="mgok" style="flex:1">다 밀었어</button>';
      G.ok = () => { if (G.done) return; const [a, b] = G.zone; if (G.th > b){ G.miss++; mgMsg('아직 두꺼워'); if (G.miss >= 3) finish('아쉬워'); return; } finish(gradeOf(G.miss), G.th > a + (b - a) * .3 && G.th < b - (b - a) * .3 ? '딱 좋아' : null); };
      G.draw = now => { board(q); const w = 70 + (30 - G.th) * 2.6, h = 30 + (30 - G.th) * 1.6; sheet(q, 70 - w / 2, 62 - h / 2, w, h, G.th, dc); pin(q, 70, G.py + (now - G.flat < 160 ? 2 : 0), Math.min(118, w + 10));
        const gx = 140, gy = 14, gh = 84, to = v => gy + gh - (v / 30) * gh; px(q, gx - 1, gy - 1, 12, gh + 2, OL); px(q, gx, gy, 10, gh, '#4A3828'); px(q, gx, to(G.zone[1]), 10, to(G.zone[0]) - to(G.zone[1]), '#6FD08C'); px(q, gx, to(G.zone[0]), 10, gy + gh - to(G.zone[0]), '#FF6B6B');
        px(q, gx - 4, to(G.th) - 1, 18, 3, '#FFFFFF'); px(q, gx - 4, to(G.th) - 1, 2, 3, OL); mgText(q, '두께', gx + 5, gy - 3, '#FFFFFF', 7); if (!G.sw && G.th === 30) mgText(q, '위아래로 쓱쓱', 70, 104, '#FFFFFF', 8); };
    }
    if (step === 3){
      G.need = [2, 3, 4][s - 1]; G.speed = [42, 62, 84][s - 1]; G.x = 30; G.dir = 1; G.cuts = []; G.last = performance.now(); G.stamp = 0;
      G.tap = () => { if (G.done) return; const x = G.x, bad = G.cuts.some(cx => Math.abs(cx - x) < 25); G.stamp = performance.now(); if (bad){ G.miss++; mgMsg('겹쳤어'); } else { G.cuts.push(x); sfx('pop'); if (G.cuts.length >= G.need) finish(gradeOf(G.miss)); } };
      G.draw = now => { const dt = (now - G.last) / 1000; G.last = now; if (!G.done){ G.x += G.dir * G.speed * dt; if (G.x > 136){ G.x = 136; G.dir = -1; } if (G.x < 24){ G.x = 24; G.dir = 1; } }
        board(q); sheet(q, 10, 46, 140, 40, 11, dc); G.cuts.forEach(cx => drawCookie(q, { f: cur.f, s: cur.s, b: 0 }, Math.round(cx - 12), 54, 1));
        const press = now - G.stamp < 150 ? 6 : 0; cutterAt(q, cur.s, G.x, 44 + press, '#2A1A2E'); cutterAt(q, cur.s, G.x - 1, 43 + press, '#D8E0F0'); px(q, G.x - 1, 30 + press, 2, 12, '#8890A8'); px(q, G.x - 4, 28 + press, 8, 3, '#B8C0D8');
        mgText(q, `${G.cuts.length} / ${G.need}`, 80, 104, '#FFFFFF', 8); mgText(q, '화면을 콕', 80, 22, '#FFFFFF', 8); };
    }
    if (step === 4){
      const pw = [13, 9, 6][s - 1], z = [[0, 40], [40, 62], [62, 62 + pw], [62 + pw, 86], [86, 100]]; G.b = 0; G.on = false; G.last = performance.now(); G.sp = [1, 1.2, 1.45][s - 1];
      bar$.innerHTML = '<button class="btn go" data-ckx="mgoven" style="flex:1">오븐 켜기</button>';
      const take_ = () => { const b = Math.round(G.b); cur.b = b; const k = b < z[1][0] ? '아쉬워' : b < z[2][0] ? '좋아' : b < z[3][0] ? '완벽' : b < z[4][0] ? '좋아' : '탐'; finish(k, { 아쉬워: '아직 말랑해', 좋아: '노릇노릇', 완벽: '완벽하게 구워졌어', 탐: '앗, 탔어' }[k]); };
      G.tap = () => { if (G.done) return; if (!G.on){ G.on = true; G.last = performance.now(); const b = document.querySelector('[data-ckx="mgoven"]'); if (b) b.textContent = '꺼내기'; return; } G.on = false; take_(); };
      G.draw = now => { const dt = (now - G.last) / 1000; G.last = now; if (G.on && !G.done){ G.b = Math.min(100, G.b + dt * (11 + G.b * .22) * G.sp); if (G.b >= 100){ G.on = false; take_(); } }
        px(q, 0, 0, MW, MH, '#5A2E1E'); for (let y = 0; y < MH; y += 8) for (let x = (y / 8 % 2) * 8; x < MW; x += 16) px(q, x, y, 15, 7, '#6E3A26');
        px(q, 14, 8, 132, 76, OL); px(q, 16, 10, 128, 72, '#2A1410'); const glow = G.on ? .5 + Math.sin(now / 120) * .1 : .15, g = q.createLinearGradient(0, 82, 0, 10); g.addColorStop(0, `rgba(255,120,40,${glow})`); g.addColorStop(1, 'rgba(255,120,40,0)'); q.fillStyle = g; q.fillRect(16, 10, 128, 72);
        px(q, 22, 66, 116, 4, '#9898A8'); const k_ = { f: cur.f, s: cur.s, b: G.b }; drawCookie(q, k_, 38, 41, 1); drawCookie(q, k_, 68, 41, 1); drawCookie(q, k_, 98, 41, 1);
        if (G.b > 86) for (let i = 0; i < 5; i++){ const t = now / 600 + i; px(q, 40 + i * 20 + Math.sin(t) * 4, 34 - (t * 16 % 22), 6, 6, `rgba(70,60,60,${Math.min(.6, (G.b - 86) / 14)})`); }
        const gx = 10, gy = 92, gw = 140, cols = ['#E8DCC8', '#E8B868', '#6FD08C', '#E8B868', '#4A2A1E']; px(q, gx - 1, gy - 1, gw + 2, 10, OL); z.forEach(([a, b], i) => px(q, gx + a / 100 * gw, gy, (b - a) / 100 * gw, 8, cols[i]));
        px(q, gx + G.b / 100 * gw - 1, gy - 3, 3, 14, '#FFFFFF'); mgText(q, '완벽', gx + (62 + pw / 2) / 100 * gw, gy - 3, '#C8F0B0', 7); };
    }
    c.onpointerdown = e => { c.setPointerCapture(e.pointerId); const [x, y] = mgPos(e); if (step === 4){ G.tap(); return; } G.down && G.down(x, y); G.tap && G.tap(x, y); G.move && step !== 2 && G.move(x, y, performance.now()); };
    c.onpointermove = e => { if (!e.buttons && e.pointerType === 'mouse') return; const [x, y] = mgPos(e); G.move && G.move(x, y, performance.now()); };
    c.onpointerup = () => { G.up && G.up(); };
    const loop = now => { if (G.dead || !$('#ckmg')) return; G.draw(now); const st = $('#ckmgst'); if (st) st.textContent = G.miss ? `실수 ${G.miss}` : ''; requestAnimationFrame(loop); }; requestAnimationFrame(loop);
  }
  function settle(){
    const c = W.cur, R = c.res; if (R[4] === '탐') c.q = '숯'; else { const p = R.reduce((a, g) => a + (GPT[g] ?? 0), 0); c.q = p >= 9 ? '최고' : p >= 6 ? '맛있음' : '보통'; }
    W.last = null; const D = K_dex(), ord = ['보통', '맛있음', '최고'], add = (id, g) => { const d = DEX.find(x => x.id === id); if (!D[id]){ D[id] = g; W.last = (W.last ? W.last + ' · ' : '') + d.n; } else if (ord.indexOf(g) > ord.indexOf(D[id])) D[id] = g; };
    if (c.q === '숯') add('coal', '숯'); else add(c.f + '_' + c.s, c.q); if (c.q === '최고' && SH_STAR[c.s] === 3) add('moon_mad', '최고');
    save(); if (W.last) sfx('sparkle');
  }
  function decoDraw(){ const c = $('#ckdcv'), q = c.getContext('2d'); q.fillStyle = '#F6E6D2'; q.fillRect(0, 0, 240, 240); q.fillStyle = '#EED8BE'; for (let y = 0; y < 240; y += 20) for (let x = (y / 20) % 2 * 20; x < 240; x += 40) q.fillRect(x, y, 20, 20); drawCookie(q, W.cur, 0, 0, 10); }
  function decoAt(e){ const c = $('#ckdcv'); if (!c || !W.cur) return; const r = c.getBoundingClientRect(), x = Math.floor((e.clientX - r.left) / r.width * N), y = Math.floor((e.clientY - r.top) / r.height * N); if (x < 0 || y < 0 || x >= N || y >= N) return;
    const { m, d } = mask(W.cur.s), k = y * N + x, t = W.tool || 'ice0'; if (!m[k] || d[k] === 1) return;
    if (t.startsWith('ice')) W.cur.ice[k] = +t.slice(3) + 1; else if (t === 'erase') W.cur.ice[k] = 0; else if (e.type === 'pointerdown' && W.cur.top.length < 30) W.cur.top.push({ k: t, x: Math.min(x, N - 2), y: Math.min(y, N - 2), c: SPR[W.cur.top.length % 5], v: W.cur.top.length % 2 });
    decoDraw(); }
  let drawing = false;
  document.addEventListener('pointerdown', e => { if (e.target.id === 'ckdcv'){ drawing = true; e.target.setPointerCapture(e.pointerId); decoAt(e); } });
  document.addEventListener('pointermove', e => { if (drawing && e.target.id === 'ckdcv' && /^ice|erase/.test(W.tool || 'ice0')) decoAt(e); });
  document.addEventListener('pointerup', () => { drawing = false; });
  document.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('#ckv button'); if (!b || b.disabled) return; const D = b.dataset, K = ck();
    if (D.cktab){ W.tab = D.cktab; render(); return; }
    if (D.ckfl){ W.pickF = D.ckfl; render(); return; }
    if (D.cktier){ W.tier = +D.cktier; render(); return; }
    if (D.cksh){ W.pickS = D.cksh; render(); return; }
    if (D.ckice){ W.tool = D.ckice === 'x' ? 'erase' : 'ice' + D.ckice; document.querySelectorAll('#ckv [data-ckice],#ckv [data-cktop]').forEach(x => x.classList.toggle('on', x === b)); return; }
    if (D.cktop){ W.tool = D.cktop; document.querySelectorAll('#ckv [data-ckice],#ckv [data-cktop]').forEach(x => x.classList.toggle('on', x === b)); return; }
    if (D.ckck){ const i = +D.ckck, S = W.sel; if (S.includes(i)) S.splice(S.indexOf(i), 1); else if (S.length < 4) S.push(i); else toast('상자에는 4 개까지 들어가요'); render(); return; }
    if (D.ckbc){ W.bc = +D.ckbc; render(); return; } if (D.ckrb){ W.br = +D.ckrb; render(); return; } if (D.ckpt){ W.bp = +D.ckpt; render(); return; }
    const x = D.ckx; if (!x) return;
    if (x === 'close') return close();
    if (x === 'start'){ const f = W.pickF, it = flOf(f).it; if (!canBake(f) || !W.pickS || World.where() !== 'candy') return; BASE.forEach(k => take(k)); take(it); save(); W.cur = { f, s: W.pickS, b: 0, ice: new Uint8Array(N * N), top: [], res: [] }; W.step = 0; render(); return; }
    if (x === 'mgalt' && MG && MG.alt) return MG.alt();
    if (x === 'mgroll' && MG && MG.roll) return MG.roll();
    if (x === 'mgok' && MG && MG.ok) return MG.ok();
    if (x === 'mgoven' && MG && MG.step === 4) return MG.tap();
    if (x === 'todeco'){ W.step = 6; W.tool = 'ice0'; render(); return; }
    if (x === 'undo' && W.cur){ W.cur.top.pop(); decoDraw(); return; }
    if (x === 'clr' && W.cur){ W.cur.ice.fill(0); W.cur.top = []; decoDraw(); return; }
    if (x === 'decodone' && W.cur){ (K.tray ||= []); for (let i = 0; i < 2 && K.tray.length < TRAY_MAX; i++) K.tray.push(enc(W.cur)); W.step = -1; W.cur = null; save(); toast('쿠키 2 개가 쟁반에 올라갔어요'); render(); return; }
    if (x === 'pack'){ if (!W.sel.length) return; const cks = W.sel.map(i => K.tray[i]).filter(Boolean); K.tray = K.tray.filter((_, i) => !W.sel.includes(i)); (K.boxes ||= []).push({ c: W.bc, r: W.br, p: W.bp, cks }); W.sel = []; save(); sfx('sparkle'); toast('리본을 묶었어요. NPC에게 말을 걸고 「선물」에서 줄 수 있어요'); render(); return; }
  });

  // ---------- 맵 위에 그리는 연출 (world.js World.onOverlay) ----------
  const BMP = { heart: ['0110110', '1221221', '1222221', '0122210', '0012100', '0001000'], star: ['0001000', '0012100', '1122211', '0122210', '0121210', '0100010'], flower: ['0011100', '0132310', '1323231', '0132310', '0011100'], drop: ['00100', '01210', '12221', '12221', '01110'], feather: ['0001', '0012', '0122', '1220', '1200', '1000'], crow: ['1100011', '0111110', '0012100', '0001000'], bunny: ['01010', '01010', '12221', '12321', '12221', '01110'], spark: ['0010', '0110', '1111', '0110', '0100'], sweat: ['010', '121', '121', '010'], bat: ['1000001', '1101011', '1122211', '0112110', '0001000'], crown: ['1010101', '1212121', '1222221', '1111111'] };
  const FXC = { heart: ['#FF6B8A', '#FFB0C4'], star: ['#FFD866', '#FFF4B8'], flower: ['#FF9EC0', '#FFE27A'], drop: ['#7CC8F0', '#D8F0FF'], feather: ['#C8A878', '#F0DCB8'], crow: ['#2A1A2E', '#2A1A2E'], bunny: ['#FFFFFF', '#FFC8D8'], spark: ['#FFE860', '#FFFFFF'], sweat: ['#9AD4F0', '#E0F4FF'], bat: ['#6A4A9A', '#9A7AC8'], crown: ['#FFD24A', '#FFF0A0'] };
  function bmp(q, k, x, y, s, a = 1){ const B = BMP[k], Cc = FXC[k]; q.globalAlpha = a; B.forEach((row, j) => [...row].forEach((v, i) => { if (v === '0') return; q.fillStyle = v === '1' ? '#2A1A2E' : v === '2' ? Cc[0] : Cc[1]; q.fillRect(Math.round(x + (i - row.length / 2) * s), Math.round(y + (j - B.length / 2) * s), Math.ceil(s), Math.ceil(s)); })); q.globalAlpha = 1; }
  let OV = null;   // 지금 그리는 연출 { kind: 'gift' | 'intro', ... }
  function overlay(q, toS, k){
    if (!OV) return; const now = performance.now(), t = (now - OV.t0) / 1000;
    if (OV.kind === 'gift') drawGift(q, toS, k, now, t); else if (OV.kind === 'intro') drawIntro(q, toS, k, now, t);
  }
  function wordAt(q, t, x, y, k, c = '#FFE9A0', size = 8){ q.font = `${size * k}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = Math.max(3, k * 1.6); q.strokeStyle = '#3A2414'; q.strokeText(t, x, y); q.fillStyle = c; q.fillText(t, x, y); q.textAlign = 'left'; }
  // 선물: 상자가 플레이어 품 → NPC 머리 위로 날아가 동동 떠서 빙글빙글 → 열림 → 쿠키 → NPC마다 반응 → 냠냠
  function drawGift(q, toS, k, now, t){
    const G = OV, np = World.npcAt(G.id), mp = World.meAt(); if (!np || !mp) return;
    const [nx, ny] = toS(np.x, np.y), [mx, my] = toS(mp.x, mp.y), bob = Math.sin(t * 3) * 2 * k, hx = nx, hy = ny - 10 * k;   // np.y: 머리 위쪽 끝
    const B = G.box, bw = 20 * k, bh = 16 * k;
    if (G.st === 'held'){ q.drawImage(boxImg(B, false), mx - bw / 2 + 3 * k, my + 16 * k, bw, bh); }
    if (G.st === 'fly'){ const a = Math.min(1, (now - G.at) / 600), x = mx + (hx - mx) * a, y = my + 18 * k + (hy - my - 18 * k) * a - Math.sin(a * Math.PI) * 10 * k; q.drawImage(boxImg(B, false), x - bw / 2, y - bh / 2, bw, bh); }
    if (G.st === 'float'){ const sx = Math.cos(t * 4); q.save(); q.translate(hx, hy + bob); q.scale(Math.abs(sx) < .12 ? .12 * Math.sign(sx || 1) : sx, 1); q.drawImage(boxImg(B, false), -bw / 2, -bh / 2, bw, bh); q.restore(); q.fillStyle = 'rgba(255,240,180,.6)'; for (let i = 0; i < 3; i++){ const an = t * 3 + i * 2.1; q.fillRect(hx + Math.cos(an) * 12 * k, hy + bob + Math.sin(an) * 4 * k, k, k); } }
    if (G.st === 'open'){ q.drawImage(boxImg(B, true, G.cks), hx - 18 * k, hy - 14 * k + bob, 36 * k, 29 * k); }
    if (G.onHead){ q.save(); q.translate(nx, ny + 2 * k); q.rotate(Math.sin(t * 5) * .25); q.drawImage(boxImg(B, false), -bw / 2, -bh, bw, bh); q.restore(); }
    if (G.cookie){ const a = Math.min(1, (now - G.cookie) / 500), cy = hy - 14 * k - a * 6 * k, sz = 16 * k; G.cpos = [hx, cy]; if (!G.cimg){ G.cimg = cookieImg(G.ck); }
      if (G.bites < 4){ q.fillStyle = 'rgba(255,240,180,.35)'; q.beginPath(); q.arc(hx, cy, sz * .75, 0, 7); q.fill(); const c = G.cimg; q.drawImage(c, hx - sz / 2, cy - sz / 2, sz, sz); } }
    G.crumbs = (G.crumbs || []).filter(f => now - f.t < 700); G.crumbs.forEach(f => { const a = (now - f.t) / 1000; q.fillStyle = f.c; q.fillRect(f.x + f.vx * a * 20 * k, f.y + f.vy * a * 20 * k + 100 * k * a * a, k, k); });
    G.fx = (G.fx || []).filter(f => t - f.t0 < f.life); G.fx.forEach(f => { const a = t - f.t0; if (a < 0) return; const p = a / f.life;
      if (f.kind === 'orbit'){ const an = f.a0 + a * f.sp; bmp(q, f.k, hx + Math.cos(an) * f.r * k, hy + Math.sin(an) * f.r * .45 * k - a * 4 * k, k, Math.min(1, (1 - p) * 2)); return; }
      if (f.kind === 'walk'){ const x = nx + (f.x0 + (f.x1 - f.x0) * p) * k, hop = Math.abs(Math.sin(a * 10)) * 4 * k; bmp(q, f.k, x, ny + 28 * k - hop, k); return; }
      if (f.kind === 'flyby'){ bmp(q, f.k, nx + (f.x0 + (f.x1 - f.x0) * p) * k, ny + (f.y0 + (f.y1 - f.y0) * p) * k + Math.sin(a * 14) * 2 * k, k); return; }
      bmp(q, f.k, nx + (f.x + f.vx * a) * k, ny + 6 * k + (f.y + f.vy * a + (f.g || 0) * a * a) * k, k, Math.min(1, (1 - p) * 2.5)); });
    if (G.blush){ q.fillStyle = `rgba(255,120,150,${G.blush * .7})`; q.fillRect(nx - 6 * k, ny + 12 * k, 3 * k, 2 * k); q.fillRect(nx + 3 * k, ny + 12 * k, 3 * k, 2 * k); }
    if (G.stamp){ const a = Math.min(1, (now - G.stamp.at) / 200), sc = 2.2 - a * 1.2; q.save(); q.translate(nx, ny - 20 * k); q.rotate(-.18); q.scale(sc, sc); q.font = `${8 * k}px G11B, sans-serif`; q.textAlign = 'center'; const w = q.measureText(G.stamp.tx).width + 8 * k; q.strokeStyle = '#E8455A'; q.lineWidth = k * 1.2; q.strokeRect(-w / 2, -8 * k, w, 11 * k); q.fillStyle = '#E8455A'; q.fillText(G.stamp.tx, 0, 0); q.restore(); q.textAlign = 'left'; }
    if (G.emo && now < G.emo.until) wordAt(q, G.emo.t, nx + 14 * k, ny + 2 * k, k, G.emo.c);
    if (G.sweat) bmp(q, 'sweat', nx + 9 * k, ny + 6 * k + (t * 10 % 4) * k / 2, k);
  }
  const gsleep = ms => new Promise(r => setTimeout(r, ms));
  function burst(k, n, opt = {}){ const t = (performance.now() - OV.t0) / 1000; for (let i = 0; i < n; i++) OV.fx.push({ k, t0: t + i * (opt.gap || .08), life: opt.life || 1.6, x: (Math.random() - .5) * 16, y: -4 - Math.random() * 6, vx: (Math.random() - .5) * 26, vy: -14 - Math.random() * 14, g: opt.g ?? 6 }); }
  function orbit(k, n, opt = {}){ const t = (performance.now() - OV.t0) / 1000; for (let i = 0; i < n; i++) OV.fx.push({ kind: 'orbit', k, t0: t, life: opt.life || 2.2, a0: i / n * 6.283, sp: opt.sp || 4, r: opt.r || 16 }); }
  // ---------- 선물 (NPC 선물 창에서) ----------
  function giftHTML(n){
    const L = (me.ck && me.ck.boxes) || []; if (!L.length || !NPCS[n.id]) return '';
    setTimeout(() => document.querySelectorAll('[data-ckgc]').forEach(c => boxTo(c, L[+c.dataset.ckgc], false)), 0);
    return `<div class="kngift"><b>쿠키 상자</b><div class="row">${L.map((b, i) => `<button data-ckgive="${i}" aria-label="쿠키 상자 주기"><canvas width="60" height="48" data-ckgc="${i}" style="width:60px;height:48px;image-rendering:pixelated"></canvas></button>`).join('')}</div><span class="s sub">하루 한 번과 상관없이 줄 수 있어요 · 좋아하는 맛과 모양이면 더 기뻐해요</span></div>`;
  }
  async function give(n, i){
    const K = ck(), B = (K.boxes || [])[i], X = NPCS[n.id]; if (!B || !X || ckOn) return;
    const cks = B.cks.map(dec).filter(Boolean); if (!cks.length) return;
    const sc = cks.map(c => ({ c, burnt: grade(c.b) === 'burnt', m: (c.f === X.f ? 1 : 0) + (c.s === X.s ? 1 : 0) })), best = sc.filter(x => !x.burnt).sort((a, b) => b.m - a.m)[0];
    let tier, h; if (!best){ tier = 3; h = 15; } else { tier = best.m === 2 ? 0 : best.m === 1 ? 1 : 2; h = [60, 40, 20][tier] + (best.m && best.c.q === '최고' ? 15 : 0); }
    const g = (K.found ||= {})[n.id] || (K.found[n.id] = {}); cks.forEach(c => { if (grade(c.b) !== 'burnt'){ if (c.f === X.f) g.f = 1; if (c.s === X.s) g.s = 1; } });
    let line = X.r[tier]; if (tier < 3 && cks.some(c => c.ice && c.ice.some(v => v))) line += ' ' + (DRAWN[n.id] || '그림까지 그려 줬네.');
    K.boxes.splice(i, 1); K.gave = (K.gave || 0) + 1; npcAddA(n.id, h); save(); closeSheet(); npcSig = ''; syncNpcs();
    yumAdd(n.id);
    await giftCine(n, B, cks, tier, best ? best.c : cks[0], line);
    toast(`${withJosa(n.name, '이', '가')} 쿠키 상자를 받았어요 · 호감도 +${h}${tier === 0 ? ' · 최고의 선물' : ''}`);
  }
  async function giftCine(n, B, cks, tier, ckk, line){
    ckOn = true; const R = REACT[n.id] || REACT.nabi, big = tier === 0;
    OV = { kind: 'gift', id: n.id, t0: performance.now(), st: 'held', box: B, cks, ck: ckk, fx: [], crumbs: [], bites: 0 };
    const G = OV, emo = (t, c, ms = 1000) => { G.emo = { t, c, until: performance.now() + ms }; }, cv = $('#cv'), shake = () => { if (cv){ cv.classList.add('otshake'); setTimeout(() => cv.classList.remove('otshake'), 420); } };
    try {
      const np = World.npcAt(n.id); if (np && World.meTile){ const m = World.meTile(); World.faceTo && World.faceTo(m.x + Math.sign(np.x - World.meAt().x), m.y); }
      World.say('me', '이거, 내가 구운 쿠키야!'); await gsleep(1300);
      G.st = 'fly'; G.at = performance.now(); sfx('pop'); await gsleep(620); G.st = 'float'; emo('!'); await gsleep(1300);
      G.st = 'open'; sfx('sparkle'); burst('star', 4, { life: 1 }); await gsleep(500); G.cookie = performance.now(); await gsleep(800);
      if (tier === 3){ G.sweat = true; emo('....', '#BDB0D6', 1400); await gsleep(1500); G.sweat = false; }
      else if (tier === 2){ emo(R.emo); burst(['crow', 'bunny'].includes(R.fx) ? 'heart' : R.fx, 2); sfx('heart'); await gsleep(1200); }
      else {
        emo(R.emo, null, 1400); sfx('heart'); const nf = big ? 1 : .5, dur = big ? 2400 : 1400; G.st = 'none';
        if (R.act === 'burst'){ burst(R.fx, Math.round(10 * nf), { gap: .1, life: 2 }); await gsleep(dur); }
        if (R.act === 'orbit'){ orbit(R.fx, big ? 6 : 3, { r: 16, sp: 5, life: dur / 1000 + .4 }); await gsleep(dur); }
        if (R.act === 'head'){ G.onHead = true; burst('drop', Math.round(5 * nf), { g: 30 }); await gsleep(dur); G.onHead = false; }
        if (R.act === 'fall'){ for (let i = 0; i < (big ? 5 : 3); i++){ burst('feather', 1, { g: 4, life: 2 }); await gsleep(320); } burst('heart', Math.round(5 * nf)); await gsleep(700); }
        if (R.act === 'blush'){ const t0 = performance.now(); while (performance.now() - t0 < 600){ G.blush = (performance.now() - t0) / 600; await gsleep(30); } G.blush = 1; burst('flower', Math.round(10 * nf), { gap: .12, life: 2 }); await gsleep(dur); }
        if (R.act === 'shoo'){ const t = (performance.now() - G.t0) / 1000; for (let i = 0; i < (big ? 3 : 2); i++) G.fx.push({ kind: 'flyby', k: 'crow', t0: t + i * .2, life: 1.4, x0: 60 + i * 8, x1: 6, y0: -24 - i * 6, y1: -14 }); await gsleep(1500); emo('훠이!'); const t2 = (performance.now() - G.t0) / 1000; for (let i = 0; i < (big ? 3 : 2); i++) G.fx.push({ kind: 'flyby', k: 'crow', t0: t2, life: 1.2, x0: 6, x1: 70 + i * 10, y0: -14, y1: -54 - i * 8 }); await gsleep(1000); burst('heart', Math.round(4 * nf)); await gsleep(600); }
        if (R.act === 'stamp'){ await gsleep(400); G.stamp = { at: performance.now(), tx: R.stamp }; sfx('hit'); shake(); burst(R.fx, Math.round(6 * nf)); await gsleep(dur); G.stamp = null; }
        if (R.act === 'bunny'){ const t = (performance.now() - G.t0) / 1000; for (let i = 0; i < (big ? 4 : 2); i++) G.fx.push({ kind: 'walk', k: 'bunny', t0: t + i * .25, life: 2.4, x0: -60 - i * 8, x1: -8 - i * 9 }); await gsleep(dur); }
        if (R.act === 'zap'){ for (let i = 0; i < (big ? 6 : 3); i++){ burst('spark', 2, { life: .6, g: 0 }); shake(); await gsleep(260); } burst('heart', Math.round(5 * nf)); await gsleep(800); }
        World.sayNpc && World.sayNpc(n.id, R.say, 1600); await gsleep(1500);
      }
      G.st = 'none';
      for (let i = 1; i <= 4; i++){ G.bites = i; const [cx, cy] = G.cpos || [0, 0]; for (let j = 0; j < 5; j++) G.crumbs.push({ t: performance.now(), x: cx + (Math.random() - .5) * 30, y: cy, vx: (Math.random() - .5) * 4, vy: -2 - Math.random() * 2, c: flOf(ckk.f).c }); emo('냠!', null, 300); sfx('pop'); await gsleep(tier === 3 ? 480 : 340); }
      G.cookie = null; await gsleep(300);
      await blancSay(n.name, line, 1600, knFace(n));
    } catch(e){ errReport('cookie', '쿠키 선물 연출 오류: ' + e.message, e.stack || ''); }
    finally { OV = null; $('#blsay') && ($('#blsay').style.display = 'none'); ckOn = false; }
  }
  // ---------- 전체 채팅 냠냠: 선물한 날부터 5 일 동안 하루 5 번 ----------
  function yumAdd(npc){
    const now = now2(), d = kNow(), sinceMid = ((d.getHours() * 60 + d.getMinutes()) * 60 + d.getSeconds()) * 1000 + d.getMilliseconds(), mid = now - sinceMid, ts = [];
    for (let day = 0; day < 5; day++){ const lo = day === 0 ? Math.max(now + 6e4, mid + 8 * 36e5) : mid + day * 864e5 + 8 * 36e5, hi = mid + day * 864e5 + 22 * 36e5, a = new Set();
      const span = Math.max(5 * 6e4, hi - lo); for (let k = 0; k < 5; k++) a.add(Math.round(lo + Math.random() * span)); ts.push(...[...a].sort((x, y) => x - y)); }
    const id = uid + '_' + now; GDB.set('ck/yum/' + id, { by: uid, npc, from: me.nick || '친구', at: now, ts }).catch(() => {});
  }
  function yumTick(){
    if (!me) return; const now = now2(), from = yumChk || now; yumChk = now; if (from === now) return;
    Object.values(yum || {}).forEach(y => { if (!y || !Array.isArray(y.ts) || now - (y.at || 0) > 6 * 864e5) return; const nn = npcGet(y.npc); if (!nn) return;
      y.ts.forEach(t => { if (t > from && t <= now){ const msg = `${withJosa(String(y.from || '친구'), '이', '가')} 준 쿠키 냠냠!`; pushLog(nn.name, msg); World.sayNpc && World.sayNpc(y.npc, '냠냠!', 2400); } }); });
  }
  // ---------- 시작 연출 (과자 교실 · 튜토리얼) ----------
  const CANDY = { OX: 164, OY: 82 }, CT = [247, 162], OVEN = [288, 131];
  function drawIntro(q, toS, k, now, t){
    const I = OV, S = (x, y) => toS(x, y);
    if (I.glow){ const [gx, gy] = S(OVEN[0], OVEN[1]); q.fillStyle = `rgba(255,150,40,${.12 + Math.sin(t * 8) * .04 + I.glow * .15})`; q.beginPath(); q.arc(gx, gy + 6 * k, (14 + I.glow * 5) * k, 0, 7); q.fill(); }
    const [bx, by] = S(CT[0], CT[1]);
    if (I.bowl){ const wob = I.bowl > 1 ? Math.round(Math.sin(t * 30)) * k : 0, R = (x, y, w, h, c) => { q.fillStyle = c; q.fillRect(bx + x * k + wob, by + y * k, w * k, h * k); };
      R(-9, -5, 18, 3, '#2A1A2E'); R(-8, -2, 16, 2, '#2A1A2E'); R(-7, 0, 14, 2, '#2A1A2E'); R(-5, 2, 10, 2, '#2A1A2E'); R(-8, -4, 16, 1, '#C86A7A'); R(-7, -2, 14, 2, '#F49AAA'); R(-6, 0, 12, 1, '#F49AAA'); R(-6, 1, 12, 1, '#D87888'); R(-4, 2, 8, 1, '#D87888'); R(-8, -5, 16, 1, '#FFE8EC');
      if (I.dough){ R(-6, -6, 12, 2, '#3A2414'); R(-5, -6, 10, 2, '#F0CC86'); R(-3, -7, 6, 1, '#3A2414'); R(-2, -7, 4, 1, '#F8E0AA'); } }
    const tray = (x, y, b, z) => { q.fillStyle = '#2A1A2E'; q.fillRect(x - 13 * z, y - 5 * z, 26 * z, 10 * z); q.fillStyle = '#B8B8C8'; q.fillRect(x - 12 * z, y - 4 * z, 24 * z, 8 * z); [-7, 0, 7].forEach(dx => { const cx = x + dx * z, cy = y - z; q.fillStyle = '#3A2414'; q.fillRect(cx - 3 * z, cy - 2 * z, 6 * z, 4 * z); q.fillRect(cx - 2 * z, cy - 3 * z, 4 * z, 6 * z); q.fillStyle = rgb(doughCol('butter', b, 1)); q.fillRect(cx - 2 * z, cy - 2 * z, 4 * z, 4 * z); q.fillStyle = rgb(doughCol('butter', b, 0)); q.fillRect(cx - z, cy - z, 2 * z, 2 * z); }); };
    if (I.tray){ const [tx, ty] = S(CT[0] + 18, CT[1] + 6); tray(tx, ty, I.tray, k * .75); }
    if (I.carry){ const p = World.npcAt('cut:madeleine'); if (p){ const [x, y] = S(p.x, p.y); tray(x, y + 18 * k, I.carry, k * .6); } }
    if (I.flour) for (let i = 0; i < 8; i++){ const a = t * 3 + i * .8, r = (t * 14 + i * 5) % 14; q.fillStyle = `rgba(255,255,255,${.7 - r / 20})`; q.fillRect(bx + Math.cos(a) * r * k, by - 6 * k - r * k * .6, k * 2, k * 2); }
    I.fly = (I.fly || []).filter(f => t - f.t0 < f.dur + .1); I.fly.forEach(f => { const a = Math.min(1, Math.max(0, (t - f.t0) / f.dur)), x = f.x0 + (CT[0] - f.x0) * a, y = f.y0 + (CT[1] - 4 - f.y0) * a - Math.sin(a * Math.PI) * 18, [px_, py_] = S(x, y), r = icImg(f.k); if (r) q.drawImage(r[0], r[1].sx, r[1].sy, 32, 32, px_ - 8 * k, py_ - 8 * k, 16 * k, 16 * k); });
    if (I.smoke > 0 && now - (I.last || 0) > 140 / I.smoke){ I.last = now; (I.puffs ||= []).push({ x: OVEN[0] + (Math.random() * 8 - 4), y: OVEN[1], vx: -2 - Math.random() * 4, vy: -6 - Math.random() * 5, r: 2 + Math.random() * 2, t0: t, dark: I.smoke > 1.2 }); }
    I.puffs = (I.puffs || []).filter(p => t - p.t0 < 3.2); I.puffs.forEach(p => { const a = t - p.t0, [px_, py_] = S(p.x + p.vx * a, p.y + p.vy * a), r = (p.r + a * 3) * k; q.fillStyle = p.dark ? `rgba(60,50,54,${.7 - a * .2})` : `rgba(210,206,210,${.55 - a * .17})`; q.fillRect(Math.round(px_ - r), Math.round(py_ - r), Math.round(r * 2), Math.round(r * 2)); });
    I.words = (I.words || []).filter(w => now < w.until); I.words.forEach(w => { const [px_, py_] = S(w.x, w.y), a = 1 - (w.until - now) / w.ms; q.globalAlpha = Math.min(1, (1 - a) * 3); wordAt(q, w.t, px_, py_ - a * 10 * k, k, w.c, w.big ? 11 : 8); q.globalAlpha = 1; });
  }
  const word = (t, x, y, c, big, ms = 900) => OV && OV.words && OV.words.push({ t, x, y, c, big, ms, until: performance.now() + ms });
  async function intro(){
    if (ckOn) return; ckOn = true; let cover = null;
    try {
      if (World.where() !== 'candy'){
        cover = document.createElement('div'); cover.className = 'bldim'; cover.style.background = '#140E1E'; document.body.appendChild(cover); requestAnimationFrame(() => cover.style.opacity = 1); await famSleep(700);
        for (let i = 0; i < 60 && World.where() !== 'candy'; i++){ if (i % 10 === 0) World.teleport('candy', [12, 16]); await famSleep(200); }
        if (World.where() !== 'candy') throw new Error('과자 교실로 못 옮겼어요');
        await famSleep(500); cover.style.opacity = 0; setTimeout(() => cover && cover.remove(), 800); cover = null;
      }
      closeSheet(); npcClose(); OV = { kind: 'intro', t0: performance.now(), words: [], fly: [], puffs: [] }; const I = OV, n = npcGet('madeleine');
      const sp = (x, y, dir) => n ? { cmd: 'spawn', who: 'madeleine', name: n.name, av: npcAv(n), x, y, dir } : { cmd: 'wait', sec: 0 };
      const say = (text, ms) => ({ cmd: 'say', who: 'madeleine', text, ms: ms || Math.max(2200, text.length * 95) }), hk = id => ({ cmd: 'sfx', id });
      const H = {
        go: () => { toast('과자 교실에서 고소한 냄새가 나요'); },
        carry: () => { I.carry = 60; }, drop: () => { I.carry = 0; I.tray = 60; word('탁!', CT[0] + 18, CT[1], '#FFE9A0'); sfx('pop'); },
        glow: () => { I.glow = 1; }, take: () => { I.tray = 0; I.carry = 1; }, put: () => { I.carry = 0; },
        bowl: () => { I.bowl = 1; sfx('pop'); },
        items: () => { const t = (performance.now() - I.t0) / 1000; [['g_wheat', -20], ['hegg', -6], ['milk', 8]].forEach(([kk, dx], j) => I.fly.push({ k: kk, t0: t + j * .35, dur: .7, x0: CT[0] + dx, y0: CT[1] - 34 })); sfx('pop'); },
        mix: () => { I.bowl = 2; I.flour = 1; I.dough = 1; word('촵촵', CT[0], CT[1] - 12, '#FFFFFF', true, 1200); setTimeout(() => word('촵촵', CT[0] + 6, CT[1] - 14, '#FFFFFF', true, 1200), 700); setTimeout(() => { I.bowl = 1; I.flour = 0; }, 1700); },
        cut: () => { I.tray = 1; I.dough = 0; word('뿅!', CT[0] + 18, CT[1] - 4, '#FFB0C8', true, 1000); sfx('pop'); },
        oven: () => { I.tray = 0; I.glow = 1.5; word('쏙', OVEN[0], OVEN[1] - 4, '#FFE9A0'); },
        ding: () => { word('띵!', OVEN[0], OVEN[1] - 6, '#FFE9A0', true, 1100); sfx('chime'); I.glow = 1; setTimeout(() => { I.carry = 66; }, 500); },
        card: () => { I.carry = 0; sfx('sparkle'); famCard(`<canvas id="ckcard" width="72" height="72" style="width:96px;height:96px;image-rendering:pixelated"></canvas><b>쿠키 틀 세트 · 쿠키 도감</b><small>과자 교실 오븐을 쓸 수 있어요 · 처음 구운 쿠키는 도감에 남아요</small>`, () => { const c = $('#ckcard'); if (c) drawCookie(c.getContext('2d'), { f: 'butter', s: 'circle', b: 66 }, 0, 0, 3); }, 2800); },
        smoke: () => { I.smoke = 1.6; }, save: () => { I.smoke = .3; I.carry = 84; word('후다닥', OVEN[0] - 10, OVEN[1] + 6, '#FFE9A0', false, 800); }, end: () => { I.smoke = 0; I.carry = 0; },
      };
      const cmds = [
        sp(18, 6, 'up'), { cmd: 'cam', x: 15, y: 6 }, hk('go'), hk('carry'),
        { cmd: 'walk', who: 'madeleine', x: 16, y: 3, run: true, dir: 'up' }, hk('glow'), say('한 판, 두 판, 세 판.... 좋아, 다음 판!', 2200),
        { cmd: 'walk', who: 'madeleine', x: 18, y: 6, run: true }, hk('drop'), { cmd: 'wait', sec: .6 },
        { cmd: 'player', x: 12, y: 14, dir: 'up' }, { cmd: 'walk', who: 'player', x: 15, y: 9 }, { cmd: 'face', who: 'madeleine', to: 'player' }, { cmd: 'emote', who: 'madeleine', icon: 4 }, say('어, 왔다!', 1400),
        say('마침 잘 왔어! 오늘부터 과자 교실 오븐을 다 같이 쓰기로 했거든.'), say('쿠키 구워서 예쁜 상자에 담고, 리본 묶어서 주고 싶은 사람한테 선물하는 거야. 재밌겠지?'),
        say('구워 본 적 없지? 괜찮아. 제일 쉬운 걸로 같이 해 보자. 버터 동그라미 쿠키!'), { cmd: 'say', who: 'player', text: '좋아!', ms: 1400 },
        hk('bowl'), say('먼저 반죽. 밀 이삭 가루에 달걀 하나, 염소젖 조금.'), hk('items'), { cmd: 'wait', sec: 1.5 }, hk('mix'), { cmd: 'wait', sec: 2 }, { cmd: 'say', who: 'player', text: '촵촵.......', ms: 1300 },
        say('반죽 다 됐다. 다음은 틀! 동그라미는 제일 쉬워. 꾹 눌렀다가.......'), hk('cut'), { cmd: 'wait', sec: 1.1 }, say('뿅! 봐, 벌써 쿠키 같지?', 1800),
        hk('take'), { cmd: 'walk', who: 'madeleine', x: 16, y: 3 }, hk('oven'), { cmd: 'walk', who: 'player', x: 17, y: 4 }, { cmd: 'face', who: 'madeleine', to: 'player' },
        say('이제부터가 진짜야. 노릇노릇해질 때 딱 꺼내야 해. 너무 일찍도, 너무 늦게도 안 돼.'), { cmd: 'say', who: 'player', text: '지금?', ms: 1200 }, say('....조금만 더.', 1400), say('....지금!', 1000),
        hk('ding'), { cmd: 'wait', sec: 1.2 }, { cmd: 'emote', who: 'madeleine', icon: 7 }, say('음.... 합격! 처음인데 엄청 잘 구웠다. 가장자리 색 봐, 완전 노릇해.'),
        say('오늘부터 과자 교실 오븐은 마음대로 써. 맛도 바꾸고, 모양도 바꾸고, 아이싱으로 그림도 그리고.'), hk('card'), { cmd: 'wait', sec: 3.4 },
        say('도감 다 채우면.... 나도 아직 못 본 쿠키가 나올지도 몰라. 그건 꼭 나한테 제일 먼저 보여 줘.'),
        hk('smoke'), { cmd: 'wait', sec: 1 }, { cmd: 'emote', who: 'madeleine', icon: 4 }, say('아, 맞다. 내 쿠키!', 1300), { cmd: 'walk', who: 'madeleine', x: 15, y: 2, run: true, dir: 'up' }, hk('save'), { cmd: 'wait', sec: .6 }, { cmd: 'face', who: 'madeleine', to: 'player' },
        say('휴, 살았다. ....가장자리만 살짝 탔네. 이건 내가 먹을게. 비밀이야.'), hk('end'), { cmd: 'wait', sec: .4 },
      ];
      let skip = false; const sk = document.createElement('button'); sk.className = 'btn sm mqskip'; sk.textContent = '건너뛰기'; sk.onclick = () => { skip = true; }; $('#stage') && $('#stage').appendChild(sk);
      await World.cut(cmds, { sfx: id => H[id] ? H[id]() : sfx(id), skip: () => skip }); sk.remove();
      done();
      toast('이제 과자 교실 오븐에서 쿠키를 구울 수 있어요. 오븐이나 마들렌을 눌러요');
    } catch(e){ if (cover) cover.remove(); if (/못 옮겼어요/.test(e.message)){ skipUntil = Date.now() + 20000; ckOn = false; OV = null; return; } errReport('cookie', '쿠키 시작 연출 오류: ' + e.message, e.stack || ''); done(); }
    finally { OV = null; ckOn = false; }
  }
  function done(){ const K = ck(), first = !K.met; K.met = 1; K.ev = ctl ? ctl.id : now2(); if (first){ K.dex = K.dex || {}; K.dex.butter_circle = K.dex.butter_circle || '맛있음'; (K.tray ||= []).push(enc({ f: 'butter', s: 'circle', b: 66, q: '맛있음' }), enc({ f: 'butter', s: 'circle', b: 66, q: '맛있음' })); } save(); placeOven(); }
  let skipUntil = 0;
  // ---------- 과자 교실 오븐 (누르면 창이 열려요) ----------
  function ovenImg(){ const c = document.createElement('canvas'); c.width = 20; c.height = 22; const g = c.getContext('2d'); const R = (x, y, w, h, col) => { g.fillStyle = col; g.fillRect(x, y, w, h); };
    R(3, 9, 14, 13, '#2A1A2E'); R(4, 10, 12, 11, '#C8946A'); R(4, 10, 12, 2, '#E0B088'); R(5, 21, 2, 1, '#2A1A2E'); R(13, 21, 2, 1, '#2A1A2E');
    R(1, 6, 18, 5, '#2A1A2E'); R(2, 7, 16, 3, '#B8B8C8'); [[5, 5], [10, 4], [15, 5]].forEach(([x, y]) => { R(x - 2, y - 1, 4, 3, '#3A2414'); R(x - 1, y - 2, 2, 5, '#3A2414'); R(x - 1, y - 1, 2, 3, '#F0CC86'); R(x - 2, y, 4, 1, '#E8B868'); });
    R(7, 13, 6, 5, '#3A2414'); R(8, 14, 4, 3, '#F49AAA'); return c; }
  function placeOven(){ if (!(me.ck && me.ck.met)) return World.setProps('candy', [], 'ckoven'); if (ovenOK === 'candy:' + World.where()) return;
    if (World.where() !== 'candy') return; const spot = [[17, 3], [18, 3], [16, 4], [19, 4], [18, 4]].find(([x, y]) => World.isFree(x, y)) || [18, 4];
    const img = ovenImg(); World.setProps('candy', [{ id: 'ckoven', x: spot[0], y: spot[1], img, pxc: img.getContext('2d'), sw: 20, sh: 22, ax: 10, ay: 20, solid: true }], 'ckoven'); ovenOK = 'candy:candy'; }
  function tick(){
    if (!me) return; if (World.where() !== 'candy') ovenOK = ''; placeOven(); yumTick();
    if (ckOn || !ctl || !ctl.open || Date.now() < skipUntil || uiBusy() || !(World.meAt && World.meAt())) return;
    const K = me.ck; if (K && K.ev === ctl.id) return; const where = World.where();
    if (!/^(gt_|arena|room_)/.test(where || '') && evTurn('ck')) intro();
  }
  function listen(){
    if (offs.length) return; offs.push(GDB.on('ck/ctl', v => { ctl = v || null; }), GDB.on('ck/yum', v => { yum = v || {}; }));
    const pp = World.onProp; World.onProp = id => id === 'ckoven' ? (open('bake'), null) : pp ? pp(id) : null;
    const po = World.onOverlay; World.onOverlay = (q, toS, k) => { try { overlay(q, toS, k); } catch(e){} if (po) po(q, toS, k); };
    setInterval(() => { try { tick(); } catch(e){ errReport('cookie', '쿠키 tick 오류: ' + e.message, e.stack || ''); } }, 1500);
  }
  const madBtn = () => me && me.ck && me.ck.met ? '<button class="btn sm go" data-nx="ckoven">쿠키 굽기</button>' : '';
  // ---------- 관리자 ----------
  function adminHTML(){
    const c = AD.ckctl || {}, P = AD.players || {}, ids = Object.keys(P).filter(id => P[id]?.nick).sort((a, b) => P[a].nick.localeCompare(P[b].nick, 'ko'));
    const st = id => { const k = P[id].ck || {}; return k.met ? `도감 ${Object.keys(k.dex || {}).length}/${DEX.length} · 쟁반 ${(k.tray || []).length} · 상자 ${(k.boxes || []).length} · 선물 ${k.gave || 0}` : '아직 연출 안 봄'; };
    return `<div class="adcard sdad"><div class="abhead"><b>마들렌의 쿠키 상자</b>${c.open ? '<button class="btn sm" data-cka="off">끄기</button>' : '<button class="btn sm go" data-cka="on">켜기</button>'}${c.open ? '<button class="btn sm" data-cka="again">연출 다시 보내기</button>' : ''}</div>
      <div class="abchips"><span>${c.open ? '켜짐' : '꺼짐'}</span><span>연출 본 학생 <b>${ids.filter(id => P[id].ck && P[id].ck.met).length}</b> / ${ids.length}</span></div>
      ${ids.map(id => `<div class="sdarow"><span><b>${esc(P[id].nick)}</b></span><span class="s">${st(id)}</span></div>`).join('')}
      <div class="s" style="margin-top:6px">켜면 아직 연출을 못 본 학생은 바로 과자 교실로 옮겨져 마들렌이랑 버터 동그라미 쿠키를 같이 굽는 연출이 나와요. 연출을 보면 과자 교실 오븐이 열리고, 꺼도 계속 구울 수 있어요. 끄면 새로 연출이 나오지 않아요. NPC가 쿠키 상자를 받으면 5 일 동안 하루 5 번 전체 채팅에 「(이름)이 준 쿠키 냠냠!」이 떠요 (이미 받은 건 꺼도 5 일을 다 채워요).</div></div>`;
  }
  document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-cka]'); if (!b) return; const a = b.dataset.cka, c = AD.ckctl || {};
    if (a === 'on'){ if (confirm('「마들렌의 쿠키 상자」를 켤까요? 아직 연출을 못 본 학생은 바로 과자 교실로 옮겨져 연출이 나와요.')) GDB.set('ck/ctl', { open: true, id: c.id || now2(), at: now2() }).then(() => toast('쿠키 상자를 켰어요')); }
    else if (a === 'again'){ if (confirm('연출을 다시 보낼까요? 모든 학생에게 마들렌 연출이 한 번 더 나와요 (구운 쿠키와 도감은 그대로예요).')) GDB.upd('ck/ctl', { id: now2() }).then(() => toast('연출을 다시 보냈어요')); }
    else if (confirm('끌까요? 새로 연출이 나오지 않아요. 이미 연출을 본 학생은 계속 쿠키를 구울 수 있어요.')) GDB.upd('ck/ctl', { open: false }).then(() => toast('쿠키 상자를 껐어요')); });
  window.__ck = { intro: () => intro(), open: t => open(t), give: (id, i) => give(npcGet(id), i), W, enc, dec, DEX, yumTick: () => yumTick(), yumAdd: id => yumAdd(id), state: () => ({ ckOn, OV: !!OV, ctl }) };   // 시험용
  return { listen, giftHTML, give, madBtn, open, adminHTML };
})();
