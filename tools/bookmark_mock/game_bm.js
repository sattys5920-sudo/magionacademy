let bmOn = false;
const BM = (() => {
  // ---------- 원고 「열두 개의 밤」 (tools/bookmark_mock/book.md) · 문단 = 쪽 · 단어 = 칸 ----------
  const BOOK = `이 책은 올해 호박달 마녀학교에 온 열두 명의 기록이에요.
사서는 원래 남의 이야기를 정리하는 사람이라.... 저도 모르게 매일 밤 조금씩 적어 버렸어요.

처음 정문이 열리던 날, 열두 명은 서로의 이름도 몰랐어요.
누구는 지도를 거꾸로 들고 있었고, 누구는 솥을 처음 보고 뒷걸음질 쳤고, 누구는 운동장 한가운데서 그냥 하늘을 보고 있었어요.
저는 도서관 창가에서 그 모습을 보며 생각했어요. 이 아이들이 이 학교에서 무엇을 찾게 될까.

이 학교에는 저마다 말 못 할 고민을 하나씩 품은 사람들이 있었어요.
너무 오래 품고 있어서, 다들 혼자 들고 있는 데 익숙해져 있었어요.
그런데 열두 명은 그냥 지나치지 않았어요.
문을 두드렸고, 앉아서 들었고, 같이 걸었어요.
대단한 마법을 쓴 게 아니에요. 대부분은 "괜찮아요?" 한마디였고, 같이 끓인 물약 한 솥이었고, 말없이 옆에 있어 준 저녁이었어요.

매점 지붕 위에서도, 온실에서도, 연못가에서도, 들판에서도.
다들 겉으로는 괜찮은 척 하루를 보내고 있었어요.
열두 명은 그 사람들 곁에 하나씩 자리를 만들었어요.
편지에 답장을 했고, 꽃말을 찾아 주었고, 탄 쿠키도 맛있다고 먹어 주었어요.

저는 그걸 다 적었어요. 하루도 빠짐없이요.
적다 보니 알게 됐어요.
이 책에 적힌 건 열두 명이 해낸 큰일이 아니라, 열두 명이 놓치지 않은 작은 마음들이라는 걸요.

누군가의 고민을 들어 준다는 건, 그 사람의 내일을 조금 바꾸는 일이에요.
그 내일들이 모이면 학교의 내일이 되고, 학교의 내일이 모이면.... 아마 미래라고 부르는 게 되겠죠.
열두 명은 미래를 만들겠다고 한 적이 없어요.
그냥 오늘 옆에 있는 사람을 잘 대했을 뿐이에요.
그런데 저는 그게 이 학교에서 일어난 가장 큰 마법이라고 생각해요.

언젠가 열두 명도 이 학교를 떠나겠죠.
그날이 오면 이 책을 펼쳐 보세요.
여러분이 여기 있었다는 것, 여러분 덕분에 덜 외로웠던 사람들이 있었다는 것.
그건 시간이 지나도 지워지지 않는 글자예요.

....재채기 한 번에 다 날아가 버리긴 했지만요.
※ 다시 모아 주면, 이번엔 꼭 코를 막고 읽을게요.`;
  const PAGES = BOOK.trim().split(/\n\s*\n/).map(par => par.split('\n').map(line => line.split(/\s+/).filter(Boolean).map(tok => { const m = tok.match(/^(["“.…]*)(.*?)(["”.,!?…]*)$/); return { pre: m[1], w: m[2], post: m[3] }; })));
  const ALL = [...new Set(PAGES.flat(2).map(t => t.w).filter(Boolean))], SL = PAGES.map(p => p.flat()), TOTAL = SL.reduce((a, p) => a + p.filter(t => t.w).length, 0);
  const WC = ['#FBF3DE', '#FCE1E8', '#DDF2E2', '#E6DDF8', '#DCECFA', '#FFF0C8'], wc = w => WC[[...w].reduce((a, c) => a + c.charCodeAt(0), 0) % WC.length];
  // ---------- 책갈피 · 기본 20 · NPC 11 (그 NPC ♥5부터) · 열두 개의 밤 (완성 선물) · 36 × 92 도트 ----------
  const BASIC = [
    ['moon', '달밤', '#2A3268', '#E8C468', { drop: 3, g2_moonst: 1 }, '달빛 이슬로 그린 초승달. 밤에 읽는 책에 꽂아요.'],
    ['star', '별자리', '#1E2448', '#9AC8F0', { g2_stardust: 2, drop: 2 }, '별가루를 콕콕 찍어 이은 별자리.'],
    ['pumpkin', '호박등', '#F08A3A', '#2A1A2E', { g2_pseed: 5, honey: 1 }, '웃고 있는 호박등. 호박씨로 눈을 붙였어요.'],
    ['bat', '박쥐', '#5A3A8A', '#E8C468', { g2_batleaf: 3, silk: 1 }, '박쥐 날개 잎을 눌러 만든 박쥐 그림자.'],
    ['paw', '고양이 발자국', '#F6ECD6', '#C86A4A', { whisker: 3, wool: 2 }, '책 위를 지나간 고양이 발자국. 범인은 아마 그 애.'],
    ['feather', '부엉이 깃털', '#E8DCC0', '#7A5A3A', { feather: 3, silk: 1 }, '진짜 부엉이 깃털을 붙였어요. 아울라가 제일 좋아해요.'],
    ['clover', '네잎클로버', '#D8F0DC', '#3A8A4A', { g_clover: 3, herb: 2 }, '책 사이에 눌러 말린 네잎클로버.'],
    ['rose', '들장미', '#FCE1E8', '#D84A6A', { g_rose: 4, honey: 1 }, '들장미 꽃잎 압화. 은은한 향이 나요.'],
    ['lav', '라벤더', '#E6DDF8', '#7A5AB0', { g_lav: 4, g_chamo: 2 }, '라벤더 한 줄기. 졸린 밤에 딱이에요.'],
    ['maple', '단풍잎', '#FFE8C8', '#D8642A', { g_maple: 4, honey: 1 }, '붉게 물든 단풍잎을 그대로 눌렀어요.'],
    ['lily', '은방울꽃', '#E8F4FA', '#3A7A5A', { g_lily: 3, drop: 1 }, '작은 종 같은 은방울꽃.'],
    ['mush', '보라 버섯', '#2E4A3A', '#B87AE8', { mush: 4, g2_moss: 2 }, '숲속 보라 버섯 셋. 먹으면 안 돼요.'],
    ['hat', '마녀 모자', '#6A3A6A', '#2A1A2E', { silk: 3, mana: 1 }, '거미줄 실로 수놓은 마녀 모자.'],
    ['potion', '물약병', '#2E6A6A', '#9AE8A8', { slime: 3, herb: 3 }, '보글보글 초록 물약병.'],
    ['candle', '촛불', '#5A3A2A', '#FFD27A', { honey: 4, wool: 1 }, '밀랍으로 만든 촛불. 끝까지 읽게 지켜 줘요.'],
    ['cloud', '구름', '#CFE6F8', '#FFFFFF', { g_cloud: 3, drop: 2 }, '구름 목화로 만든 몽실몽실 구름.'],
    ['rainbow', '무지개', '#FBF6EE', '#E8645A', { g_rainbow: 2, g2_stardust: 1 }, '무지개 콩 즙으로 그린 무지개.'],
    ['snow', '눈송이', '#DCEFF8', '#FFFFFF', { g_snow: 3, g_cloud: 1 }, '녹지 않는 눈송이 꽃.'],
    ['check', '체크무늬', '#C84A4A', '#F6ECD6', { wool: 4, silk: 2 }, '털실로 짠 따뜻한 체크무늬.'],
    ['crystal', '수정', '#3A2E5A', '#C8B8F8', { mana: 3, g2_moonst: 1 }, '마나석 조각이 반짝여요.'],
  ].map(([id, n, bg, fg, m, d]) => ({ id, n, bg, fg, m: { g_cotton: 3, ...m }, d }));
  const NPCB = [
    ['nabi', '나비', 0, '#F6E6C8', '#E8A060', { whisker: 4, f_minnow: 3 }, '생선 뼈 무늬. 나비가 보면 모른 척하며 가져갈지도.'],
    ['batri', '배트리', 1, '#E6DDF8', '#6A4A9A', { g2_batleaf: 3, feather: 2, silk: 1 }, '우표와 봉투 무늬. 배달 가방에 꽂기 좋아요.'],
    ['kappa', '캇파', 2, '#D8F0DC', '#3A8A5A', { g2_moss: 4, g_mint: 3 }, '연못 물결과 접시 무늬.'],
    ['aula', '아울라', 3, '#1E2448', '#E8C468', { feather: 4, g2_moonst: 1, drop: 2 }, '책과 달 무늬. 사서의 책갈피.'],
    ['mandi', '맨디', 4, '#E2F2D6', '#E86A8A', { g_rose: 3, g_dandel: 3, g_lily: 1 }, '들꽃이 가득한 무늬.'],
    ['jipsin', '스트로', 5, '#F2E2A8', '#5A3A24', { g2_straw: 5, g2_pseed: 3 }, '들판과 까마귀 무늬.'],
    ['sera', '세라 선생님', 6, '#FBFBF8', '#E05A5A', { herb: 4, g_chamo: 3, honey: 1 }, '하트와 반창고 무늬.'],
    ['madeleine', '마들렌', 7, '#FCE1E8', '#B8743A', { g_wheat: 4, honey: 3 }, '쿠키와 거품기 무늬.'],
    ['stella', '스텔라', 8, '#2A1E48', '#FFD866', { g2_stardust: 3, g2_moonst: 2 }, '별과 달 무늬.'],
    ['leo', '레오', 9, '#DFF0C8', '#7A5A3A', { wool: 4, g_carrot: 4 }, '토끼와 당근 무늬.'],
    ['otumo', '오투모', 10, '#C8D8E8', '#3A6AB0', { mana: 3, g_thunder: 2, slime: 1 }, '번개와 나사 무늬.'],
  ].map(([id, n, row, bg, fg, m, d]) => ({ id, n, row, bg, fg, m: { g_cotton: 3, ...m }, d, npc: true }));
  const RIB = { moon: '#E8C468', star: '#9AC8F0', pumpkin: '#5A3A24', bat: '#E8C468', paw: '#C86A4A', feather: '#7A5A3A', clover: '#3A8A4A', rose: '#D84A6A', lav: '#7A5AB0', maple: '#D8642A', lily: '#3A7A5A', mush: '#B87AE8', hat: '#E8C468', potion: '#9AE8A8', candle: '#C8643A', cloud: '#7AA8D8', rainbow: '#6A9FE8', snow: '#7AA8D8', check: '#F6ECD6', crystal: '#C8B8F8' };
  // ===== 도트 (36 × 92)
  const OL = '#2A1A2E';
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t)), rgb = c => `rgb(${c[0]},${c[1]},${c[2]})`;
  const shade = (h, k) => rgb(mix(hex(h), k > 0 ? [255, 255, 255] : [30, 20, 40], Math.abs(k)));
  function draw(q, B){
    const P = (x, y, w, h, c) => { q.fillStyle = c; q.fillRect(x, y, w, h); }, C = (cx, cy, r, c) => { for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++) if (x * x + y * y <= r * r + r * .6) P(cx + x, cy + y, 1, 1, c); };
    const BM = (rows, x, y, cols) => rows.forEach((row, j) => [...row].forEach((v, i) => { if (v !== '.') P(x + i, y + j, 1, 1, cols[v]); }));
    q.clearRect(0, 0, 36, 92);
    const rib = B.npc ? B.fg : RIB[B.id] || '#C8A050';
    // 종이
    P(2, 12, 32, 79, OL); P(3, 13, 30, 77, B.bg); P(3, 13, 30, 1, shade(B.bg, .3)); P(3, 88, 30, 2, shade(B.bg, -.15));
    for (let y = 15; y < 88; y += 3) for (let x = 4 + (y % 2); x < 32; x += 6) P(x, y, 1, 1, shade(B.bg, B.bg === '#1E2448' || B.bg === '#2A3268' || B.bg === '#2A1E48' || B.bg === '#3A2E5A' || B.bg === '#2E4A3A' ? .08 : -.05));
    P(5, 15, 26, 1, shade(B.bg, -.12)); P(5, 86, 26, 1, shade(B.bg, -.12));
    // 구멍 · 끈 · 술
    C(18, 18, 2, OL); C(18, 18, 1, shade(B.bg, -.4)); P(17, 4, 2, 14, OL); P(17, 5, 1, 12, rib); P(14, 2, 8, 4, OL); P(15, 3, 6, 2, rib);
    for (let k = 0; k < 4; k++){ P(10 + k * 2 - (k > 1 ? 0 : 0), 5 + k, 2, 7 - k, OL); P(11 + k * 2, 6 + k, 1, 6 - k, shade(rib, .2)); }
    if (B.npc){
      C(18, 38, 13, OL); C(18, 38, 12, shade(B.fg, .55));
      q.save(); q.beginPath(); q.arc(18.5, 38.5, 12, 0, 7); q.clip(); faceAt(q, B.id, 5, 25, 27); q.restore();
      npcMotif(q, B, P, C, BM); return;
    }
    motif(q, B, P, C, BM);
  }
  function motif(q, B, P, C, BM){
    const f = B.fg, dk = shade(f, -.3), lt = shade(f, .35), cx = 18;
    const star = (x, y, c) => { P(x, y - 1, 1, 3, c); P(x - 1, y, 3, 1, c); };
    switch (B.id){
      case 'twelve': { P(cx - 7, 38, 14, 18, OL); P(cx - 6, 39, 12, 16, '#2A3A6A'); P(cx - 6, 39, 2, 16, '#141C3A'); P(cx - 3, 41, 7, 1, f); P(cx - 3, 52, 7, 1, f); P(cx, 44, 1, 5, '#FFF4C8'); P(cx - 2, 46, 5, 1, '#FFF4C8'); P(cx + 6, 40, 1, 14, '#F6ECD6');
        for (let k = 0; k < 12; k++){ const a = k / 12 * 6.283 - 1.57, x = Math.round(cx + Math.cos(a) * 13), y = Math.round(47 + Math.sin(a) * 15); C(x, y, 1, k % 3 ? f : '#FFF4C8'); }
        C(cx, 74, 4, f); C(cx + 2, 72, 4, B.bg); [[9, 30], [27, 66], [10, 82]].forEach(([x, y]) => star(x, y, '#FFF4C8')); break; }
      case 'moon': C(cx, 46, 9, f); C(cx + 4, 43, 8, B.bg); [[8, 30], [27, 28], [10, 66], [25, 70], [16, 78], [26, 56]].forEach(([x, y]) => star(x, y, '#FFF4C8')); break;
      case 'star': { const S = [[9, 30], [16, 38], [24, 34], [26, 48], [14, 56], [22, 64], [11, 74], [24, 80]]; q.strokeStyle = shade(f, -.2); S.slice(1).forEach((p, i) => { const a = S[i]; for (let t = 0; t <= 1; t += .1) P(Math.round(a[0] + (p[0] - a[0]) * t), Math.round(a[1] + (p[1] - a[1]) * t), 1, 1, shade(f, -.35)); }); S.forEach(([x, y]) => { star(x, y, '#FFF4C8'); P(x, y, 1, 1, f); }); break; }
      case 'pumpkin': C(cx, 50, 11, '#2A1A2E'); C(cx, 50, 10, '#C8642A'); P(cx - 6, 41, 2, 18, '#B85A22'); P(cx + 5, 41, 2, 18, '#B85A22'); P(cx - 1, 37, 3, 4, '#3A6A2A'); BM(['1...1', '11.11'], cx - 6, 47, { 1: '#FFE07A' }); BM(['1...1', '11.11'], cx + 2, 47, { 1: '#FFE07A' }); BM(['1.1.1.1', '1111111', '.1.1.1.'], cx - 3, 54, { 1: '#FFE07A' }); break;
      case 'bat': BM(['1.........1', '11.1...1.11', '111111111.1', '11111111111', '.111111111.', '..1.1.1.1..'].map(r => r), cx - 5, 46, { 1: OL }); P(cx - 2, 48, 1, 1, f); P(cx + 2, 48, 1, 1, f); C(cx, 30, 4, f); C(cx + 2, 28, 4, B.bg); [[8, 72], [26, 66], [12, 80]].forEach(([x, y]) => star(x, y, f)); break;
      case 'paw': [[11, 32], [22, 46], [12, 60], [23, 74]].forEach(([x, y]) => { C(x, y + 3, 3, f); [-3, -1, 1, 3].forEach(dx => P(x + dx, y - 2 + (Math.abs(dx) === 3 ? 1 : 0), 2, 2, f)); }); break;
      case 'feather': for (let y = 28; y < 82; y++){ const t = (y - 28) / 54, w = Math.round(Math.sin(t * Math.PI) * 7) + 1; P(cx - w + Math.round(t * 4), y, w * 2, 1, (y % 4 < 2) ? f : lt); P(cx + Math.round(t * 4), y, 1, 1, dk); } break;
      case 'clover': [[-4, -4], [4, -4], [-4, 4], [4, 4]].forEach(([dx, dy]) => C(cx + dx, 44 + dy, 4, f)); C(cx, 44, 2, lt); P(cx, 52, 1, 22, dk); P(cx + 1, 66, 2, 1, dk); break;
      case 'rose': for (let r = 7; r > 0; r -= 2) C(cx, 42, r, r % 4 === 3 ? f : lt); C(cx, 42, 1, dk); P(cx, 50, 1, 26, '#3A7A3A'); C(cx - 4, 60, 2, '#4A8A4A'); C(cx + 4, 68, 2, '#4A8A4A'); break;
      case 'lav': P(cx, 34, 1, 46, '#4A7A4A'); for (let y = 30; y < 58; y += 3){ C(cx - 2, y, 1, f); C(cx + 2, y + 1, 1, lt); } P(cx - 4, 64, 3, 1, '#4A7A4A'); P(cx + 2, 70, 3, 1, '#4A7A4A'); break;
      case 'maple': { const L = ['....1....', '...111...', '1..111..1', '111111111', '.1111111.', '..11111..', '.1111111.', '11.111.11', '....1....', '....1....', '....1....']; L.forEach((row, j) => [...row].forEach((v, i) => { if (v === '1'){ P(cx - 9 + i * 2, 34 + j * 2, 2, 2, (i + j) % 5 ? f : lt); } })); break; }
      case 'lily': P(cx, 30, 1, 48, '#3A7A5A'); for (let k = 0; k < 5; k++){ const x = cx + (k % 2 ? 3 : -3), y = 34 + k * 7; P(x - (k % 2 ? 0 : 1), y - 1, 2, 1, '#3A7A5A'); C(x, y + 2, 2, '#FFFFFF'); P(x - 1, y + 4, 3, 1, '#D8E8F0'); } C(cx - 5, 72, 3, '#4A9A6A'); break;
      case 'mush': [[cx - 5, 46, 6], [cx + 6, 58, 5], [cx - 3, 72, 4]].forEach(([x, y, r]) => { C(x, y, r, OL); C(x, y, r - 1, f); P(x - r + 1, y, r * 2 - 1, r, B.bg); P(x - 1, y, 3, r + 3, '#E8DCC0'); P(x - 2, y - r + 2, 2, 1, '#FFFFFF'); P(x + 2, y - 2, 1, 1, '#FFFFFF'); }); break;
      case 'hat': for (let y = 30; y < 60; y++){ const w = Math.round((y - 30) / 30 * 8); P(cx - w + Math.round((60 - y) / 10), y, w * 2 + 1, 1, OL); } P(cx - 13, 60, 27, 3, OL); P(cx - 7, 54, 15, 3, '#E8C468'); P(cx - 1, 54, 3, 3, '#FFF4C8'); [[8, 72], [26, 74], [17, 82]].forEach(([x, y]) => star(x, y, '#E8C468')); break;
      case 'potion': P(cx - 2, 32, 5, 8, '#E8DCC0'); P(cx - 3, 30, 7, 3, '#8A5A34'); C(cx, 50, 10, OL); C(cx, 50, 9, '#E8F4F0'); C(cx, 52, 7, f); P(cx - 7, 46, 15, 2, '#E8F4F0'); C(cx - 3, 54, 1, lt); C(cx + 3, 50, 1, lt); [[cx - 2, 38], [cx + 3, 34], [cx, 30]].forEach(([x, y]) => C(x - 6, y - 6, 1, lt)); break;
      case 'candle': P(cx - 4, 46, 9, 30, '#F2E6C8'); P(cx - 4, 46, 2, 30, '#D8C8A8'); P(cx - 6, 76, 13, 3, '#8A5A34'); P(cx, 42, 1, 4, OL); C(cx, 38, 3, '#FF9A3C'); C(cx, 37, 2, f); C(cx, 36, 8, 'rgba(255,220,120,.15)'); P(cx + 2, 50, 2, 6, '#F8EED8'); break;
      case 'cloud': [[cx - 6, 40, 5], [cx + 2, 37, 6], [cx + 7, 42, 4], [cx - 4, 64, 4], [cx + 3, 62, 5]].forEach(([x, y, r]) => C(x, y, r, f)); P(cx - 10, 42, 20, 4, f); P(cx - 8, 64, 16, 4, f); [[10, 78], [24, 80], [16, 52]].forEach(([x, y]) => P(x, y, 1, 3, '#7AA8D8')); break;
      case 'rainbow': ['#E8645A', '#F0A040', '#F2D84A', '#6AC86A', '#6A9FE8', '#9A6AD8'].forEach((c, i) => { for (let a = Math.PI; a <= Math.PI * 2; a += .02) P(Math.round(cx + Math.cos(a) * (12 - i * 1.6)), Math.round(58 + Math.sin(a) * (12 - i * 1.6)), 2, 2, c); }); C(cx - 11, 60, 3, '#FFFFFF'); C(cx + 11, 60, 3, '#FFFFFF'); break;
      case 'snow': [[cx, 40, 7], [cx - 6, 64, 4], [cx + 6, 74, 4]].forEach(([x, y, r]) => { for (let k = 0; k < 6; k++){ const a = k * Math.PI / 3; for (let t = 0; t <= r; t++) P(Math.round(x + Math.cos(a) * t), Math.round(y + Math.sin(a) * t), 1, 1, k % 2 ? '#7AA8D8' : f); } P(x, y, 1, 1, '#7AA8D8'); }); break;
      case 'check': for (let y = 14; y < 89; y++) for (let x = 3; x < 33; x++){ const a = Math.floor((x - 3) / 5) % 2, b = Math.floor((y - 14) / 5) % 2; if (a || b) P(x, y, 1, 1, a && b ? shade(B.bg, .45) : shade(B.bg, .2)); } C(18, 18, 2, OL); C(18, 18, 1, shade(B.bg, -.4)); break;
      case 'crystal': [[cx, 44, 8], [cx - 6, 66, 5], [cx + 6, 70, 5]].forEach(([x, y, h]) => { for (let k = 0; k < h * 2; k++){ const w = Math.round((k < h ? k : h * 2 - k) * .7); P(x - w, y - h + k, w * 2 + 1, 1, k < h ? lt : f); } P(x, y - h, 1, h * 2, '#FFFFFF'); }); [[8, 30], [27, 34]].forEach(([x, y]) => { P(x, y - 1, 1, 3, '#FFFFFF'); P(x - 1, y, 3, 1, '#FFFFFF'); }); break;
    }
  }
  function npcMotif(q, B, P, C, BM){
    const f = B.fg, lt = shade(f, .4), y0 = 56;
    const star = (x, y, c) => { P(x, y - 1, 1, 3, c); P(x - 1, y, 3, 1, c); };
    switch (B.id){
      case 'nabi': [[10, 64], [22, 78]].forEach(([x, y]) => { P(x, y, 8, 1, f); for (let k = 1; k < 7; k += 2){ P(x + k, y - 2, 1, 5, f); } C(x + 9, y, 2, f); P(x - 2, y - 2, 2, 5, f); }); [[24, 62], [12, 80]].forEach(([x, y]) => { C(x, y + 2, 2, '#C86A4A'); P(x - 2, y - 1, 1, 1, '#C86A4A'); P(x + 2, y - 1, 1, 1, '#C86A4A'); }); break;
      case 'batri': P(8, 62, 14, 10, OL); P(9, 63, 12, 8, '#FBF6EE'); for (let k = 0; k < 6; k++){ P(9 + k, 63 + k, 1, 1, f); P(20 - k, 63 + k, 1, 1, f); } P(20, 74, 9, 10, OL); P(21, 75, 7, 8, '#E8645A'); for (let x = 20; x < 30; x += 2){ P(x, 74, 1, 1, B.bg); P(x, 84, 1, 1, B.bg); } C(24, 79, 2, '#FFF4C8'); break;
      case 'kappa': for (let r = 3; r < 14; r += 4) for (let a = 0; a < 6.3; a += .06) P(Math.round(18 + Math.cos(a) * r), Math.round(72 + Math.sin(a) * r * .5), 1, 1, r % 8 === 3 ? f : lt); C(18, 72, 2, '#E8E0D0'); P(6, 62, 4, 10, '#4A9A4A'); P(7, 63, 2, 8, '#7AC87A'); break;
      case 'aula': [[7, 66, '#7A2A30'], [12, 64, '#2E5A6E'], [17, 67, '#7A6A2A'], [22, 63, '#4A2E6A']].forEach(([x, y, c]) => { P(x, y, 5, 84 - y, OL); P(x + 1, y + 1, 3, 82 - y, c); P(x + 1, y + 3, 3, 1, f); }); C(27, 62, 4, f); C(29, 60, 4, B.bg); star(9, 58, '#FFF4C8'); break;
      case 'mandi': [[9, 64, '#E86A8A'], [18, 70, '#F2D84A'], [26, 64, '#9A7AE8'], [13, 78, '#FFFFFF'], [24, 80, '#E86A8A']].forEach(([x, y, c]) => { P(x, y + 2, 1, 6, '#4A8A4A'); [[-2, 0], [2, 0], [0, -2], [0, 2]].forEach(([dx, dy]) => C(x + dx, y + dy, 1, c)); P(x, y, 1, 1, '#F2D84A'); }); break;
      case 'jipsin': for (let x = 3; x < 33; x++){ const h = 6 + ((x * 7) % 5); P(x, 86 - h, 1, h, (x % 3) ? '#C8A040' : '#A88030'); } [[10, 62], [22, 66]].forEach(([x, y]) => BM(['11...11', '.11111.', '..111..'], x - 3, y, { 1: OL })); break;
      case 'sera': [[10, 64], [24, 72]].forEach(([x, y]) => { C(x - 2, y, 2, f); C(x + 2, y, 2, f); for (let k = 0; k < 4; k++) P(x - 4 + k, y + 1 + k, 9 - k * 2, 1, f); }); P(8, 76, 18, 6, OL); P(9, 77, 16, 4, '#F2D8B8'); P(15, 77, 4, 4, '#E8C8A8'); [[10, 78], [12, 79], [21, 78], [23, 79]].forEach(([x, y]) => P(x, y, 1, 1, '#C8A888')); break;
      case 'madeleine': [[11, 66], [24, 72], [14, 80]].forEach(([x, y]) => { C(x, y, 4, OL); C(x, y, 3, '#E8B868'); [[-1, -1], [1, 1], [-2, 1]].forEach(([dx, dy]) => P(x + dx, y + dy, 1, 1, '#5A3420')); }); P(26, 58, 1, 8, '#A8A8B8'); for (let k = 0; k < 3; k++) P(24 + k * 2, 62 - k, 1, 6, '#C8C8D8'); break;
      case 'stella': [[8, 62], [26, 60], [14, 72], [24, 78], [10, 82], [18, 64]].forEach(([x, y], i) => { star(x, y, i % 2 ? f : lt); }); C(22, 70, 3, f); C(23, 69, 3, B.bg); break;
      case 'leo': BM(['.1...1.', '.1...1.', '.11111.', '1111111', '1.111.1', '1111111', '.11111.'], 8, 64, { 1: '#FFFFFF' }); P(10, 67, 1, 1, OL); P(13, 67, 1, 1, OL); P(22, 66, 3, 14, OL); P(23, 67, 1, 12, '#F08A4A'); P(20, 62, 2, 4, '#4A9A4A'); P(24, 61, 2, 5, '#4A9A4A'); break;
      case 'otumo': BM(['..11', '.11.', '1111', '.11.', '11..'], 8, 62, { 1: '#FFE860' }); BM(['..11', '.11.', '1111', '.11.', '11..'], 24, 76, { 1: '#FFE860' }); [[22, 64], [12, 78]].forEach(([x, y]) => { C(x, y, 3, OL); C(x, y, 2, '#A8B8C8'); P(x - 1, y, 3, 1, OL); }); break;
    }
  }
  const FX = {
    moon: { t: "밤 채집 가끔 +1", night:1,v:{nightg:.25} },
    star: { t: "밤 낚시 입질 빨라짐", night:1,v:{bite:.25} },
    pumpkin: { t: "호박 채집물 가끔 +1", v:{pump:.5} },
    bat: { t: "밤에 걸음 +12 %", night:1,s:{move_speed:.12} },
    paw: { t: "낚시 입질 빨라짐", v:{bite:.15} },
    feather: { t: "쪽지시험 힌트 1번", b:'hint' },
    clover: { t: "드문 채집물 ↑", b:'fluck' },
    rose: { t: "선물 호감도 +10 %", s:{gift_affection:.1} },
    lav: { t: "쉬기 회복 +10 %", v:{rest:.1} },
    maple: { t: "채집 · 수확 가끔 +1", s:{gather_yield:.08} },
    lily: { t: "온실 작물 10 % 빨리", s:{crop_growth:.1} },
    mush: { t: "버섯 채집 ↑", v:{mush:1} },
    hat: { t: "주문 납품 골드 +10 %", v:{order:.1} },
    potion: { t: "지식 얻는 양 +10 %", v:{know:.1} },
    candle: { t: "탐사 회복 +10 %", v:{heal:.1} },
    cloud: { t: "비 오는 날 희귀 물고기 ↑", rain:1,s:{rare_fish:.3} },
    rainbow: { t: "팔 때 값 +5 %", v:{sell:.05} },
    snow: { t: "요리 별 가끔 +1", s:{craft_success:.1} },
    check: { t: "친구 곁 보상 +5 %", s:{party_reward:.05} },
    crystal: { t: "물 주기 마력 가끔 0", s:{stamina_cost:-.2} },
    nabi: { t: "나비 호감 ↑ · 물고기 크기 ↑", aff:'nabi',v:{fsize:1} },
    batri: { t: "배트리 호감 ↑ · 걸음 +6 %", aff:'batri',s:{move_speed:.06} },
    kappa: { t: "캇파 호감 ↑ · 입질 빨라짐", aff:'kappa',v:{bite:.1} },
    aula: { t: "아울라 호감 ↑ · 탐사 경험치 +5 %", aff:'aula',s:{exp_gain:.05} },
    mandi: { t: "맨디 호감 ↑ · 온실 작물 빨리", aff:'mandi',s:{crop_growth:.06} },
    jipsin: { t: "스트로 호감 ↑ · 호박 채집물 +1", aff:'jipsin',v:{pump:.3} },
    sera: { t: "세라 선생님 호감 ↑ · 탐사 회복 +5 %", aff:'sera',v:{heal:.05} },
    madeleine: { t: "마들렌 호감 ↑ · 요리 별 가끔 +1", aff:'madeleine',s:{craft_success:.06} },
    stella: { t: "스텔라 호감 ↑ · 희귀 물고기 ↑", aff:'stella',s:{rare_fish:.15} },
    leo: { t: "레오 호감 ↑ · 채집 · 수확 가끔 +1", aff:'leo',s:{gather_yield:.05} },
    otumo: { t: "오투모 호감 ↑ · 물 주기 마력 가끔 0", aff:'otumo',s:{stamina_cost:-.12} },
    twelve: { t: "모든 NPC 호감 +10 %" },
  };
  const TWELVE = { id: 'twelve', n: '열두 개의 밤', bg: '#1E2448', fg: '#E8C468', m: {}, d: '다시 책이 된 날, 아울라가 반 전체에게 하나씩 준 책갈피.', gift: true };
  const all = () => [...BASIC, ...NPCB, TWELVE], byId = id => all().find(b => b.id === id);
  const bkName = B => B.n + (B.npc ? ' 책갈피' : '');
  // ---------- 얼굴 (NPC 책갈피 동그라미 안) ----------
  const faces = {};
  function faceCv(id){ if (faces[id]) return faces[id]; const n = npcGet(id); if (!n) return null; const c = document.createElement('canvas'); c.width = c.height = 32; try { knFace(n)(c.getContext('2d')); } catch(e){ return null; } return faces[id] = c; }
  const faceAt = (q, id, dx, dy, d) => { const c = faceCv(id); if (c) q.drawImage(c, 0, 0, 32, 32, dx, dy, d, d); };
  function sil(c){ const q = c.getContext('2d'); q.globalCompositeOperation = 'source-atop'; q.fillStyle = '#3A2A55'; q.fillRect(0, 0, c.width, c.height); q.fillStyle = '#4E3C72'; q.fillRect(3, 13, 30, 2); q.globalCompositeOperation = 'source-over'; }
  function bkTo(c, B, hide){ const q = c.getContext('2d'); q.imageSmoothingEnabled = false; draw(q, B); if (hide) sil(c); }

  // ---------- 상태 ----------
  let cardN = 0, ctl = null, got = {}, place = {}, done = null, offs = [], doneSeenEmpty = false, skipUntil = 0, OV = null;
  const W = { tab: 'book', page: 0, sel: null, q: '', bk: 'basic', bsel: 'moon', rp: 0, drop: 0 };
  const st = () => { const s = me.bm || (me.bm = {}); if (!s.made || typeof s.made !== 'object') s.made = {}; return s; };
  const has = k => typeof haveSame === 'function' ? haveSame(k) : (me.inv[k] || 0), take = (k, n = 1) => typeof takeSame === 'function' ? takeSame(k, n) : (me.inv[k] = Math.max(0, (me.inv[k] || 0) - n));
  const inm = k => (typeof ITEM !== 'undefined' && ITEM[k]) || k;
  const met = () => !!(me && me.bm && me.bm.met);
  const gotN = () => Object.keys(got || {}).length;
  const mine = () => Object.entries(got || {}).filter(([, v]) => v && v.u === uid).map(([k]) => ALL[+k]).filter(Boolean);
  const pv = (pi, k) => { const o = place[pi + '_' + k]; return o && ALL[o.w] !== undefined ? o : null; };
  const pageOK = pi => SL[pi].every((t, k) => !t.w || (pv(pi, k) && ALL[pv(pi, k).w] === t.w));
  const rightN = () => SL.reduce((a, p, pi) => a + p.filter((t, k) => t.w && pv(pi, k) && ALL[pv(pi, k).w] === t.w).length, 0);
  const allOK = () => rightN() >= TOTAL;
  const live = () => !!(ctl && ctl.open && !done);

  // ---------- 책갈피 효과 ----------
  const pinned = () => { if (!me || !me.bm) return null; const p = me.bm.pin; return p && me.bm.made && me.bm.made[p] && FX[p] ? p : null; };
  const fxOn = F => !(F.night && bandNow() !== 'night') && !(F.rain && weatherToday() !== 'rain');
  function stat(s){ const p = pinned(); if (!p) return 0; const F = FX[p]; return F.s && F.s[s] && fxOn(F) ? F.s[s] : 0; }
  function val(k){ const p = pinned(); if (!p) return 0; const F = FX[p]; return F.v && F.v[k] && fxOn(F) ? F.v[k] : 0; }
  const buff = k => { const p = pinned(); return !!(p && FX[p].b === k); };
  const aff = id => { const p = pinned(); return !p ? 1 : p === 'twelve' ? 1.1 : FX[p].aff === id ? 1.2 : 1; };
  const PUMP = ['g2_pseed', 'g2_amber', 'g2_pumpmoon'], MUSH = ['g2_mushred', 'g2_mushpine', 'g2_spider', 'g2_moonm'];
  const spotW = x => val('mush') && MUSH.includes(x.id) ? { ...x, w: x.w * 1.8 } : x;
  function spotExtra(it){   // 채집 하나 더: 달밤(밤) · 호박등 · 스트로
    let n = 0; if (val('nightg') && Math.random() < val('nightg')) n++; if (val('pump') && PUMP.includes(it.id) && Math.random() < val('pump')) n++;
    if (n){ me.inv[it.id] = (me.inv[it.id] || 0) + n; setTimeout(() => toast(`책갈피 덕분에 ${withJosa(it.name, '을', '를')} 하나 더 주웠어요`), 900); } return n;
  }
  function examHint(ex, Qn){
    if (!buff('hint') || !ex || ex.picked !== null) return ''; ex.bmCut = ex.bmCut || {};
    if (ex.bmUsed && ex.bmCut[ex.i] === undefined) return `<div class="hint">부엉이 깃털 책갈피 힌트는 이번 시험에 다 썼어요</div>`;
    if (ex.bmCut[ex.i] !== undefined){ setTimeout(() => { const b = document.querySelector(`[data-ans="${ex.bmCut[ex.i]}"]`); if (b){ b.disabled = true; b.style.opacity = '.35'; b.style.textDecoration = 'line-through'; } }, 0); return `<div class="hint">부엉이 깃털이 틀린 답 하나를 지웠어요</div>`; }
    setTimeout(() => { const b = document.getElementById('bmhint'); if (b) b.onclick = () => { const wrong = Qn.choices.map((c, j) => j).filter(j => Qn.choices[j] !== Qn.a); if (!wrong.length) return; ex.bmCut[ex.i] = wrong[Math.floor(Math.random() * wrong.length)]; ex.bmUsed = 1; sfx('sparkle'); renderExam(); }; }, 0);
    return `<button class="btn sm" id="bmhint" style="align-self:flex-start">부엉이 깃털 힌트 · 틀린 답 하나 지우기</button>`;
  }

  // ---------- 글자가 나와요 (채집 · 낚시) ----------
  function drop(kind){
    if (!me || !met() || !live() || bmOn || Math.random() > .25) return;
    const left = ALL.map((w, i) => i).filter(i => !got[i]); if (!left.length) return;
    const i = left[Math.floor(Math.random() * left.length)], w = ALL[i];
    GDB.tx('bm/got/' + i, cur => cur ? undefined : { u: uid, by: me.nick || '친구', at: now2() }).then(r => {
      if (!r || !r.committed) return; got[i] = { u: uid, by: me.nick || '친구', at: now2() }; W.fresh = w;
      setTimeout(() => { famCard(`<div class="bmfly"><span class="bmwd bmflap bmbob bmnew" style="--wc:${wc(w)}">${esc(w)}</span></div><b>날아간 단어를 찾았어요</b><small>${kind === 'fish' ? '물속' : '덤불'}에서 「${esc(w)}」가 파닥파닥 날아왔어요 · 도서관 사서 책상에 모여요 (반 전체 ${gotN()} / ${ALL.length})</small>`, null, 2600); sfx('sparkle'); }, 1300);
    }).catch(() => {});
  }

  // ---------- 창 (도서관 사서 책상 · 독서대) ----------
  const tabsNow = () => { const T = []; if (met() && !done) T.push(['book', '책 맞추기'], ['bag', '내 글자']); if (done) T.push(['read', '읽기']); if (met() || done) T.push(['mark', '책갈피']); return T; };
  function open(tab){
    if (!me || (uiBusy() && !bmOn)) return; const T = tabsNow(); if (!T.length) return;
    W.tab = T.some(t => t[0] === tab) ? tab : T.some(t => t[0] === W.tab) ? W.tab : T[0][0]; bmOn = true;
    let v = $('#bmv'); if (!v){ v = document.createElement('div'); v.id = 'bmv'; document.body.appendChild(v); } render(); requestAnimationFrame(() => v.classList.add('on'));
  }
  function close(){ const v = $('#bmv'); if (v){ v.classList.remove('on'); setTimeout(() => v.remove(), 300); } bmOn = false; drag = null; }
  const sec = (title, body, aside = '') => `<section class="cd"><div class="cdh"><h3>${title}</h3>${aside}</div>${body}</section>`;
  const tile = (w, cls = '', attr = '') => `<span class="bmwd ${cls}" style="--wc:${wc(w)}" ${attr}>${esc(w)}</span>`;
  const tipHTML = t => `<div class="tip2"><canvas data-bmface="1" width="32" height="32"></canvas><p>${t}</p></div>`;
  function render(){
    const v = $('#bmv'); if (!v) return; const T = tabsNow(); if (!T.some(t => t[0] === W.tab)){ if (!T.length) return close(); W.tab = T[0][0]; }
    const keep = $('#bmtray') ? $('#bmtray').scrollLeft : 0, keepB = v.querySelector('.bd') ? v.scrollTop : 0;
    v.innerHTML = `<div class="hd"><b>${W.tab === 'mark' ? '아울라의 책갈피' : '열두 개의 밤'}</b><button data-bmx="close" aria-label="닫기">✕</button></div><div class="tabs">${T.map(([k, n]) => `<button data-bmtab="${k}" class="${W.tab === k ? 'on' : ''}">${n}</button>`).join('')}</div>
      <div class="bd">${W.tab === 'book' ? bookHTML() : W.tab === 'bag' ? bagHTML() : W.tab === 'read' ? readHTML() : markHTML()}</div>`;
    v.querySelectorAll('[data-bmface]').forEach(c => { const g = c.getContext('2d'); g.imageSmoothingEnabled = false; try { knFace(npcGet('aula'))(g); } catch(e){} });
    v.querySelectorAll('[data-bkc]').forEach(c => { const B = byId(c.dataset.bkc); if (B) bkTo(c, B, !st().made[B.id]); });
    const tr = $('#bmtray'); if (tr) tr.scrollLeft = keep; v.scrollTop = keepB;
  }
  function bookHTML(){
    const pi = Math.min(W.page, PAGES.length - 1), ok = pageOK(pi); let k = 0;
    const lines = PAGES[pi].map(line => line.map(t => { const i = k++; if (!t.w) return esc(t.pre + t.post); const o = pv(pi, i), w = o ? ALL[o.w] : '';
      return `${esc(t.pre)}<span class="bmslot ${o ? 'on' : ''} ${o && o.u !== uid ? 'bmfr' : ''}" data-slot="${i}" ${o ? `title="${esc(o.by || '친구')} 님이 놓았어요"` : ''} style="${o ? `--wc:${wc(w)};` : ''}min-width:${Math.max(2.2, [...t.w].length * 1.05)}em">${o ? esc(w) : '　'}</span>${esc(t.post)}`; }).join(' ')).join('<br>');
    const total = SL[pi].filter(t => t.w).length, filled = SL[pi].filter((t, k) => t.w && pv(pi, k)).length;
    const list = ALL.filter((w, i) => got[i] && (!W.q || w.includes(W.q))).sort((a, b) => a.localeCompare(b, 'ko'));
    const feed = Object.values(place).filter(o => o && o.at).sort((a, b) => b.at - a.at).slice(0, 4);
    const pct = Math.floor(rightN() / TOTAL * 100);
    return `<div class="pnav">${PAGES.map((_, i) => `<button data-bmpg="${i}" class="${i === pi ? 'on' : ''} ${pageOK(i) ? 'ok' : ''}">${i + 1}</button>`).join('')}</div>
      <div class="bmbook ${ok ? 'bmok' : ''}"><div class="pgno"><span>『열두 개의 밤』</span><span>${pi + 1} 쪽 · ${filled} / ${total}</span></div><div class="txt">${lines}</div></div>
      <p class="s">${!ctl || !ctl.open ? '지금은 책을 맞출 수 없어요. 다시 열리면 이어서 맞춰요.' : ok ? '이 쪽은 글자가 다 돌아왔어요. 반짝반짝.' : '반 전체가 같은 책 한 권을 맞춰요. 글자를 끌어다 빈칸에 놓거나, 글자를 누른 다음 칸을 눌러요. 칸을 누르면 빠져요. 맞아야 빛나요.'}</p>
      <div class="bmfeed"><b>책 ${pct} %</b>${feed.map(f => `<span><i>${esc(f.by || '친구')}</i> 「${esc(ALL[f.w] || '')}」</span>`).join('')}</div>
      <div class="bmtray"><div class="bmtrh"><input id="bmq" placeholder="글자 찾기" value="${esc(W.q)}" aria-label="글자 찾기"><span>반 전체 ${gotN()} / ${ALL.length}</span></div>
        <div class="bmtrw" id="bmtray">${list.map(w => tile(w, `bmflap ${W.sel === w ? 'bmsel' : ''}`, `data-bmw="${esc(w)}"`)).join('') || '<p class="empty">아직 모인 글자가 없어요. 채집 · 낚시를 해 봐요</p>'}</div></div>`;
  }
  function bagHTML(){
    const M = mine();
    return sec('내가 찾은 글자', `<div class="bagg">${M.map(w => tile(w, `bmbob bmflap ${W.fresh === w ? 'bmnew' : ''}`)).join('') || '<p class="empty">아직 없어요</p>'}</div>`, `<span class="aside">${M.length} 개</span>`)
      + sec('반 전체', `<div class="pgb one"><i style="width:${gotN() / ALL.length * 100}%"></i></div><p class="s">모은 단어 ${gotN()} / ${ALL.length} · 책 ${Math.floor(rightN() / TOTAL * 100)} %</p>`)
      + tipHTML(gotN() >= ALL.length ? '단어가 전부 돌아왔어요. 이제 책에 맞춰 넣기만 하면 돼요.' : '채집하거나 낚시하다 보면 가끔 단어가 파닥파닥 나와요. 아직 아무도 못 찾은 단어만 나와요. 찾은 단어는 사서 책상에 저절로 모여요.');
  }
  function readHTML(){
    const n = PAGES.length + 1, p = Math.min(W.rp, n - 1);
    const body = p === 0 ? `<div class="bmcover"><b>열두 개의 밤</b><span>아울라 씀</span><i>※ 이 책은 대출되지 않아요</i></div>` : `<div class="pgno"><span>『열두 개의 밤』</span><span>${p} / ${PAGES.length}</span></div><div class="txt">${PAGES[p - 1].map(l => esc(l.map(t => t.pre + t.w + t.post).join(' '))).join('<br>')}</div>`;
    return `<div class="bmbook bmrd ${p === 0 ? 'bmcv' : ''}">${body}</div><div class="row"><button class="btn" data-bmrp="-1" ${p ? '' : 'disabled'} style="flex:1">이전 쪽</button><button class="btn go" data-bmrp="1" ${p < n - 1 ? '' : 'disabled'} style="flex:1">다음 쪽</button></div>`;
  }
  const canMake = B => !B.gift && !st().made[B.id] && Object.entries(B.m).every(([k, n]) => has(k) >= n) && (!B.npc || hearts(B.id) >= 5);
  function markHTML(){
    const S = st(), L = W.bk === 'basic' ? BASIC : W.bk === 'npc' ? NPCB : all().filter(b => S.made[b.id]);
    const B = byId(W.bsel) && L.includes(byId(W.bsel)) ? byId(W.bsel) : L[0], P = pinned();
    const atDesk = World.where() === 'library';
    const det = B ? sec(B.npc ? 'NPC 책갈피' : '책갈피', `<div class="det"><canvas data-bkc="${B.id}" width="36" height="92"></canvas><div class="bminfo"><h4>${esc(bkName(B))}</h4><span class="bmfx">${S.made[B.id] ? esc(FX[B.id].t) : '효과 ???'}</span><p>${S.made[B.id] ? esc(B.d) : '만들면 무늬와 효과를 알 수 있어요.'}</p>
      ${B.gift ? '' : `<div class="mats">${Object.entries(B.m).map(([k, n]) => `<div class="${has(k) >= n ? 'yes' : 'no'}">${ic(k)}${esc(inm(k))}<b>${has(k)} / ${n}</b></div>`).join('')}</div>`}
      ${B.npc && hearts(B.id) < 5 ? `<p class="warn">${esc(B.n)} 호감 ♥5부터 만들 수 있어요 · 지금 ♥${hearts(B.id)}</p>` : ''}
      ${S.made[B.id] ? `<button class="btn ${P === B.id ? '' : 'go'} wide" data-bmpin="${B.id}">${P === B.id ? '일지에서 빼기' : '일지에 꽂기'}</button>` : `<button class="btn go wide" data-bmmake="${B.id}" ${canMake(B) && atDesk ? '' : 'disabled'}>${!atDesk ? '사서 책상에서 만들 수 있어요' : canMake(B) ? '만들기' : '재료가 모자라요'}</button>`}</div></div>`) : '';
    return `<div class="seg">${[['basic', '기본 20'], ['npc', 'NPC 11'], ['mine', '내 책갈피']].map(([k, n]) => `<button data-bmbk="${k}" class="${W.bk === k ? 'on' : ''}">${n}</button>`).join('')}</div>`
      + (W.bk === 'mine' && !L.length ? '<p class="empty">아직 만든 책갈피가 없어요</p>' : det + `<div class="bkg">${L.map(b => { const lock = b.npc && hearts(b.id) < 5; return `<button class="bk ${b.id === (B && B.id) ? 'on' : ''} ${lock ? 'lock' : ''}" data-bmsel="${b.id}"><canvas data-bkc="${b.id}" width="36" height="92"></canvas>${esc(b.n)}<em class="bmfx">${S.made[b.id] ? esc(FX[b.id].t) : '???'}</em>${P === b.id ? '<span class="bmown">꽂음</span>' : ''}${lock ? '<span class="lk">♥5</span>' : ''}</button>`; }).join('')}</div>`)
      + `<p class="s">만든 책갈피 하나를 일지에 꽂아 두면 밑에 적힌 효과를 받아요. 한 번에 하나만 꽂을 수 있어요.</p>`;
  }
  function make(id){
    const B = byId(id); if (!B || !canMake(B) || World.where() !== 'library') return;
    Object.entries(B.m).forEach(([k, n]) => take(k, n)); st().made[B.id] = 1; save(); sfx('sparkle'); render();
    famCard(`<canvas id="bmcard${++cardN}" width="36" height="92" style="width:54px;height:138px;image-rendering:pixelated"></canvas><b>「${esc(bkName(B))}」</b><small>${esc(FX[B.id].t)} · 일지에 꽂으면 효과를 받아요</small>`, () => { const c = $('#bmcard' + cardN); if (c) bkTo(c, B); }, 2400);
  }
  function pin(id){
    const S = st(); if (S.pin === id){ S.pin = null; toast('책갈피를 뺐어요'); } else if (S.made[id]){ S.pin = id; W.drop = 1; toast(`「${bkName(byId(id))}」를 일지에 꽂았어요 · ${FX[id].t}`); sfx('pop'); }
    save(); if (typeof syncBuffs === 'function') syncBuffs(); render(); if (sheetOn && sub === 'journal') renderJournal();
  }
  // 일지 맨 위: 꽂은 책갈피가 종이에 꽂혀 있어요
  function pinHTML(){
    if (!me || !(met() || done)) return ''; const P = pinned(), B = P && byId(P);
    setTimeout(() => { const c = document.getElementById('bmjpc'); if (c && B) bkTo(c, B); const el = document.querySelector('.bmjp .bmpn.drop'); if (el) requestAnimationFrame(() => requestAnimationFrame(() => { el.classList.remove('drop'); W.drop = 0; })); const b = document.querySelector('[data-bmjp]'); if (b) b.onclick = () => { W.bk = 'mine'; closeSheet(); setTimeout(() => open('mark'), 250); }; }, 0);
    return `<div class="bmjp ${B ? '' : 'none'}">${B ? `<div class="bmpn ${W.drop ? 'drop' : ''}"><canvas id="bmjpc" width="36" height="92"></canvas></div>` : ''}<div class="pg"><b>${B ? esc(bkName(B)) : '꽂은 책갈피가 없어요'}</b><span class="bmfx">${B ? esc(FX[P].t) : '책갈피를 꽂으면 효과를 받아요'}</span><button class="lnk" data-bmjp="1">${B ? '바꿔 꽂기' : '책갈피 고르기'}</button></div></div>`;
  }

  // ---------- 끌어다 놓기 · 눌러서 고르고 칸 누르기 ----------
  let drag = null;
  document.addEventListener('pointerdown', e => { const t = e.target.closest && e.target.closest('#bmv .bmtrw .bmwd'); if (!t) return; e.preventDefault(); drag = { w: t.dataset.bmw, x0: e.clientX, y0: e.clientY, el: null, moved: false }; });
  document.addEventListener('pointermove', e => {
    if (!drag) return; if (!drag.moved && Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) > 8){ drag.moved = true; drag.el = document.createElement('div'); drag.el.className = 'bmghost'; drag.el.innerHTML = tile(drag.w, 'bmflap'); document.body.appendChild(drag.el); }
    if (drag.el){ drag.el.style.left = e.clientX + 'px'; drag.el.style.top = e.clientY + 'px'; document.querySelectorAll('#bmv .bmslot.bmhot').forEach(s => s.classList.remove('bmhot')); const s = document.elementFromPoint(e.clientX, e.clientY)?.closest('#bmv .bmslot'); if (s) s.classList.add('bmhot'); }
  });
  document.addEventListener('pointerup', e => {
    if (!drag) return; const D = drag; drag = null; if (D.el) D.el.remove(); document.querySelectorAll('#bmv .bmslot.bmhot').forEach(s => s.classList.remove('bmhot'));
    if (!D.moved){ W.sel = W.sel === D.w ? null : D.w; render(); return; }
    const s = document.elementFromPoint(e.clientX, e.clientY)?.closest('#bmv .bmslot'); if (s) put(+s.dataset.slot, D.w);
  });
  function put(k, w){
    if (!live()) return toast('지금은 책을 맞출 수 없어요'); const i = ALL.indexOf(w); if (i < 0 || !got[i]) return;
    const pi = W.page, was = pageOK(pi), key = pi + '_' + k, o = { w: i, by: me.nick || '친구', u: uid, at: now2() };
    place[key] = o; W.sel = null; GDB.set('bm/place/' + key, o).catch(() => toast('놓지 못했어요. 다시 해 봐요')); sfx('pop'); render();
    if (!was && pageOK(pi)){ toast(`${pi + 1} 쪽 글자가 다 돌아왔어요`); sfx('chime'); }
    checkDone();
  }
  function pull(k){ if (!live()) return; const key = W.page + '_' + k; if (!place[key]) return; delete place[key]; GDB.set('bm/place/' + key, null).catch(() => {}); render(); }
  function checkDone(){ if (done || !allOK()) return; GDB.tx('bm/done', cur => cur ? undefined : { at: now2(), by: me.nick || '친구' }).catch(() => {}); }
  document.addEventListener('click', e => {
    const v = $('#bmv'); if (!v || !v.contains(e.target)) return;
    const s = e.target.closest('.bmslot'); if (s && W.tab === 'book'){ const k = +s.dataset.slot; if (W.sel) put(k, W.sel); else pull(k); return; }
    const b = e.target.closest('button'); if (!b) return; const D = b.dataset;
    if (D.bmx === 'close') return close();
    if (D.bmtab){ W.tab = D.bmtab; render(); return; }
    if (D.bmpg){ W.page = +D.bmpg; render(); v.scrollTop = 0; return; }
    if (D.bmrp){ W.rp = Math.max(0, W.rp + +D.bmrp); render(); return; }
    if (D.bmbk){ W.bk = D.bmbk; render(); return; }
    if (D.bmsel){ W.bsel = D.bmsel; render(); return; }
    if (D.bmmake) return make(D.bmmake);
    if (D.bmpin) return pin(D.bmpin);
  });
  document.addEventListener('input', e => { if (e.target.id === 'bmq'){ W.q = e.target.value.trim(); const pos = e.target.selectionStart; render(); const q = $('#bmq'); if (q){ q.focus(); q.setSelectionRange(pos, pos); } } });

  // ---------- 맵 위 연출 (World.onOverlay): 독서대 책 · 먼지 · 날개 단 단어 ----------
  const BOOKP = [260, 135];
  const ltp = (x, y) => { const m = World.meta && World.meta('library'); return [(m ? m.OX : 180) + (x - y) * 8, (m ? m.OY : 96) + (x + y) * 4]; };
  function wordAt(q, t, x, y, k, c = '#FFE9A0', size = 8){ q.font = `${size * k}px G11B, sans-serif`; q.textAlign = 'center'; q.lineWidth = Math.max(3, k * 1.6); q.strokeStyle = '#3A2414'; q.strokeText(t, x, y); q.fillStyle = c; q.fillText(t, x, y); q.textAlign = 'left'; }
  function wingTile(q, w, x, y, k, c, now, s){
    q.font = `${Math.round(4.4 * k)}px G11B, sans-serif`; q.textAlign = 'center'; const tw = Math.ceil(q.measureText(w).width) + 4 * k, h = 6 * k, flap = Math.sin(now / 70 + s) * k;
    q.fillStyle = '#FFFFFF'; q.strokeStyle = '#2A1A2E'; q.lineWidth = Math.max(1, k * .7);
    [[-1, x - tw / 2], [1, x + tw / 2]].forEach(([d, wx]) => { q.beginPath(); q.moveTo(wx, y - 1.4 * k); q.lineTo(wx + d * 3 * k, y - 3.4 * k - flap); q.lineTo(wx + d * 2.4 * k, y + .6 * k); q.closePath(); q.fill(); q.stroke(); });
    q.fillStyle = '#2A1A2E'; q.fillRect(x - tw / 2 - k * .7, y - h / 2 - k * .7, tw + k * 1.4, h + k * 1.4); q.fillStyle = c; q.fillRect(x - tw / 2, y - h / 2, tw, h); q.fillStyle = '#3A2A40'; q.fillText(w, x, y + 1.6 * k); q.textAlign = 'left';
  }
  function overlay(q, toS, k){
    const I = OV; if (!I || World.where() !== 'library') return; const now = performance.now(), t = (now - I.t0) / 1000;
    const [bx, by] = toS(BOOKP[0], BOOKP[1] - (I.rise || 0)), R = (x, y, w, h, col) => { q.fillStyle = col; q.fillRect(Math.round(bx + x * k), Math.round(by + y * k), Math.ceil(w * k), Math.ceil(h * k)); };
    if (I.glow > 0){ const g = q.createRadialGradient(bx, by, 2, bx, by, 60 * k * I.glow); g.addColorStop(0, `rgba(255,232,150,${.5 * I.glow})`); g.addColorStop(1, 'rgba(255,232,150,0)'); q.fillStyle = g; q.fillRect(bx - 60 * k, by - 60 * k, 120 * k, 120 * k); }
    if (I.book === 'closed'){ R(-7, -9, 14, 18, '#2A1A2E'); R(-6, -8, 12, 16, '#2A3A6A'); R(-6, -8, 2, 16, '#1E2A50'); R(-3, -6, 7, 1, '#E8C468'); R(-3, 5, 7, 1, '#E8C468'); R(0, -2, 1, 4, '#FFF4C8'); R(-1, -1, 3, 2, '#FFF4C8'); }
    else if (I.book){ R(-9, -3, 18, 6, '#2A1A2E'); R(-8, -3, 8, 5, '#F6ECD6'); R(1, -3, 7, 5, '#EADBBE'); if (I.book === 'full') for (let j = 0; j < 4; j++){ R(-7, -2 + j, 6, .4, '#8A7A6A'); R(2, -2 + j, 5, .4, '#8A7A6A'); } }
    I.dust = (I.dust || []).filter(d => t - d.t0 < 2.4); I.dust.forEach(d => { const a = (t - d.t0) / 2.4; if (a < 0) return; const [px, py] = toS(d.x + (BOOKP[0] - d.x) * a, d.y + (BOOKP[1] - 3 - d.y) * a + Math.sin(a * 9 + d.s) * 3); q.fillStyle = `rgba(240,230,200,${.75 - a * .4})`; q.fillRect(px, py, k, k); });
    I.words = (I.words || []).filter(w => !w.dead); const cw = q.canvas.width, ch = q.canvas.height;
    I.words.forEach(w => { const a = t - w.t0; if (a < 0) return; let x, y;
      if (w.mode === 'out'){ x = bx + w.vx * a * k; y = by + (w.vy * a - 10 * a + Math.sin(a * 6 + w.s) * 3) * k; if (a > 3.5) w.dead = true; }
      else { const p = Math.min(1, a / w.dur), e = p * p * (3 - 2 * p); x = w.x0 * cw + (bx - w.x0 * cw) * e + Math.sin(p * Math.PI) * w.curve * k; y = w.y0 * ch + (by - w.y0 * ch) * e - Math.sin(p * Math.PI) * 20 * k; if (p >= 1) w.dead = true; }
      wingTile(q, w.w, x, y, k, w.c, now, w.s); });
    if (I.ring > 0){ q.globalAlpha = I.ring; for (let j = 0; j < 16; j++){ const a = j / 16 * 6.283 + t * 1.5, r = (14 + Math.sin(t * 3 + j) * 2) * k; q.fillStyle = j % 2 ? '#FFE9A0' : '#FFFFFF'; q.fillRect(bx + Math.cos(a) * r, by + Math.sin(a) * r * .6, k, k); } q.globalAlpha = 1; }
    if (I.flash > 0){ q.fillStyle = `rgba(255,248,220,${I.flash})`; q.fillRect(0, 0, cw, ch); I.flash = Math.max(0, I.flash - .02); }
    const ap = World.npcAt('cut:aula'); if (ap){ const [ax, ay] = toS(ap.x, ap.y);
      if (I.bang) wordAt(q, I.bang, ax, ay - 8 * k, k, '#FFE9A0', I.bang === '에취!' ? 13 : 9);
      if (I.sweat){ q.fillStyle = '#9AD4F0'; q.fillRect(ax + 7 * k, ay + 4 * k + ((t * 20) % 8) * k / 2, k * 1.5, k * 2); }
      if (I.heart && now < I.heart) wordAt(q, '♥', ax + 10 * k, ay + 2 * k, k, '#FF9EC0', 10); }
  }
  const cv$ = () => $('#cv'), shake = () => { const c = cv$(); if (c){ c.classList.add('otshake'); setTimeout(() => c.classList.remove('otshake'), 420); } };
  const outWords = n => { const t = (performance.now() - OV.t0) / 1000, L = [...ALL].sort(() => Math.random() - .5).slice(0, n); L.forEach((w, i) => { const a = Math.random() * 6.283, sp = 40 + Math.random() * 80; OV.words.push({ w, mode: 'out', vx: Math.cos(a) * sp, vy: Math.sin(a) * sp * .7 - 20, t0: t + i * .035, s: i, c: wc(w) }); }); };
  const inWords = n => { const t = (performance.now() - OV.t0) / 1000, L = [...ALL].sort(() => Math.random() - .5).slice(0, n); L.forEach((w, i) => { const side = i % 4, x0 = side === 0 ? -.1 : side === 1 ? 1.1 : Math.random(), y0 = side < 2 ? Math.random() : side === 2 ? -.1 : 1.1; OV.words.push({ w, mode: 'in', x0, y0, dur: 1.6 + Math.random() * .8, curve: (Math.random() - .5) * 40, t0: t + i * .05, s: i, c: i % 5 ? wc(w) : '#FFF4C8' }); }); };
  async function toLibrary(){
    if (World.where() === 'library') return null; const cover = document.createElement('div'); cover.className = 'bldim'; cover.style.background = '#140E1E'; document.body.appendChild(cover); requestAnimationFrame(() => cover.style.opacity = 1); await famSleep(700);
    for (let i = 0; i < 60 && World.where() !== 'library'; i++){ if (i % 10 === 0) World.teleport('library', [13, 12]); await famSleep(200); }
    if (World.where() !== 'library'){ cover.remove(); throw new Error('도서관으로 못 옮겼어요'); }
    await famSleep(500); cover.style.opacity = 0; setTimeout(() => cover.remove(), 800); return null;
  }
  const aSpawn = (x, y, dir) => { const n = npcGet('aula'); return n ? { cmd: 'spawn', who: 'aula', name: n.name, ...(n.av ? { av: npcAv(n) } : { spr: n.spr, float: n.float, flap: n.flap }), x, y, dir } : { cmd: 'wait', sec: 0 }; };
  const say = (text, ms) => ({ cmd: 'say', who: 'aula', text, ms: ms || Math.max(2200, text.length * 100) }), me$ = (text, ms) => ({ cmd: 'say', who: 'player', text, ms: ms || 1600 }), hk = id => ({ cmd: 'sfx', id }), wait = sec => ({ cmd: 'wait', sec });
  async function runCut(cmds, H){
    let skip = false; const sk = document.createElement('button'); sk.className = 'btn sm mqskip'; sk.textContent = '건너뛰기'; sk.onclick = () => { skip = true; }; $('#stage') && $('#stage').appendChild(sk);
    try { await World.cut(cmds, { sfx: id => H[id] ? H[id]() : sfx(id), skip: () => skip }); } finally { sk.remove(); }
  }
  // 시작: 재채기 한 번에 단어들이 날개를 달고 날아가요
  async function intro(){
    if (bmOn) return; bmOn = true;
    try {
      closeSheet(); npcClose(); await toLibrary();
      OV = { t0: performance.now(), book: 'full', words: [], dust: [], glow: .35 }; const I = OV;
      const H = {
        hush: () => toast('한밤 도서관.... 책장 넘기는 소리만 들려요'),
        dust: () => { const t = (performance.now() - I.t0) / 1000; for (let i = 0; i < 26; i++){ const [x, y] = ltp([4, 20, 6, 18][i % 4] + Math.random() * 2, [5, 5, 9, 9][i % 4] + Math.random() * 2); I.dust.push({ x, y: y - 20, t0: t + i * .07, s: i }); } },
        b1: () => { I.bang = '부.... 부엉.......'; }, b2: () => { I.bang = '에.... 에.......'; },
        achoo: () => { I.bang = '에취!'; I.flash = .7; I.book = 'blank'; I.glow = 0; shake(); sfx('hit'); outWords(48); setTimeout(() => { I.bang = null; }, 1100); },
        flew: () => toast('책 속 단어들이 날개를 달고 사방으로 날아갔어요'), sweat: () => { I.sweat = true; }, unsweat: () => { I.sweat = false; }, heart: () => { I.heart = performance.now() + 1400; sfx('heart'); },
      };
      await runCut([
        aSpawn(12, 3, 'up'), { cmd: 'player', x: 13, y: 12, dir: 'up' }, { cmd: 'cam', x: 12, y: 6 }, hk('hush'), wait(1.4),
        say('....후후. 여기는 몇 번을 읽어도 좋네요.', 2400), { cmd: 'walk', who: 'player', x: 13, y: 7, wait: false }, hk('dust'), wait(1.8),
        { cmd: 'face', who: 'aula', to: 'player' }, say('코가.... 간질간질.......', 1800), hk('b1'), wait(.9), hk('b2'), wait(.8), hk('achoo'), wait(2.4), hk('flew'), wait(1.6),
        hk('sweat'), { cmd: 'emote', who: 'aula', icon: 4 },
        say('....앗. 아, 안 돼요. 글자들이.......'), say('제가 새로 쓴 책이었어요. 이제 막 마지막 장까지 다 썼는데.......'), say('재채기 한 번에 단어들이 날개를 달고 다 날아가 버렸어요. 책장이 하얘요.'), hk('unsweat'),
        say('단어들은 겁이 많아서, 덤불 속이나 물속에 숨어 있을 거예요. 채집하거나 낚시하다 보면.... 파닥파닥 나올 거예요.', 4200),
        say('찾은 단어는 사서 책상에 모여요. 반 전체가 같이 맞추면, 다시 책이 될 거예요.', 3600),
        me$('같이 찾아볼게요!', 1600), hk('heart'), say('고마워요. 아, 그리고.... 기다리는 동안 책갈피도 만들어 보세요. 사서 책상에 만드는 법 적어 뒀어요.', 4000),
        say('※ 이번엔 코를 꼭 막고 기다릴게요.', 2400), wait(.4),
      ], H);
      introDone();
      famCard(`<div class="bmfly"><span class="bmwd bmflap bmbob" style="--wc:${wc('열두')}">열두</span><span class="bmwd bmflap bmbob" style="--wc:${wc('밤')}">밤</span></div><b>날아간 단어 ${ALL.length} 개</b><small>채집 · 낚시에서 가끔 나와요 · 도서관 사서 책상에서 반 전체가 같이 책을 맞춰요 · 책갈피도 만들 수 있어요</small>`, null, 3400);
    } catch(e){ if (/못 옮겼어요/.test(e.message)){ skipUntil = Date.now() + 20000; return; } errReport('bm', '책 시작 연출 오류: ' + e.message, e.stack || ''); introDone(); }
    finally { OV = null; bmOn = false; }
  }
  function introDone(){ const S = st(); S.met = 1; S.ev = ctl ? ctl.id : now2(); save(); }
  // 끝: 마지막 단어가 맞는 순간, 접속한 모두에게
  async function ending(){
    if (bmOn || !done) return; bmOn = true; const at = done.at;
    try {
      closeSheet(); npcClose(); close(); bmOn = true; await toLibrary();
      OV = { t0: performance.now(), book: 'blank', words: [], dust: [], glow: 0 }; const I = OV;
      const H = {
        last: () => toast('마지막 단어가 제자리를 찾았어요'),
        come: () => { inWords(64); (async () => { for (let j = 0; j < 40 && OV === I; j++){ I.glow = Math.min(1, .3 + j / 40); await famSleep(100); } })(); },
        full: () => { I.book = 'full'; I.flash = .9; shake(); sfx('sparkle'); setTimeout(() => { I.book = 'closed'; (async () => { for (let j = 0; j <= 30; j++){ I.rise = Math.sin(j / 30 * Math.PI / 2) * 14; I.ring = j / 30; await famSleep(40); } await famSleep(1200); for (let j = 30; j >= 0; j--){ I.rise = Math.sin(j / 30 * Math.PI / 2) * 14; await famSleep(30); } I.ring = .6; I.glow = .5; })(); }, 500); },
        heart: () => { I.heart = performance.now() + 1400; sfx('heart'); },
      };
      await runCut([
        aSpawn(12, 3, 'down'), { cmd: 'player', x: 13, y: 7, dir: 'up' }, { cmd: 'cam', x: 12, y: 5 }, hk('last'), wait(1),
        say('....들려요? 파닥파닥.......', 2000), hk('come'), wait(4.2), hk('full'), wait(4.2), hk('heart'),
        say('....다 돌아왔어요. 한 글자도 빠짐없이.', 2600), say('다 같이 하나씩 주워 와서 맞춰 줬네요. 정말 고마워요.', 3000),
        say('이 책은 대출되지 않아요. 대신.... 언제든 와서 읽어 주세요. 독서대 위에 둘게요.', 3800),
        me$('이번엔 코 막고 읽어요!', 1600), say('....네. 꼭 막을게요.', 2000),
        say('아, 이건 고마운 마음이에요. 반 전체에 하나씩 드려요.', 3000), wait(.3),
      ], H);
    } catch(e){ if (/못 옮겼어요/.test(e.message)){ skipUntil = Date.now() + 20000; return; } errReport('bm', '책 끝 연출 오류: ' + e.message, e.stack || ''); }
    finally { OV = null; bmOn = false; }
    const S = st(); S.end = at; save(); grant(true);
  }
  function grant(show){
    const S = st(); if (!done || S.made.twelve) return; S.made.twelve = 1; if (!S.pin) S.pin = 'twelve'; save(); if (typeof syncBuffs === 'function') syncBuffs();
    famCard(`<canvas id="bmcard${++cardN}" width="36" height="92" style="width:54px;height:138px;image-rendering:pixelated"></canvas><b>「열두 개의 밤」 책갈피</b><small>${esc(FX.twelve.t)} · 도서관 독서대에서 책을 언제든 읽을 수 있어요</small>`, () => { const c = $('#bmcard' + cardN); if (c) bkTo(c, TWELVE); }, show ? 3200 : 2800); sfx('sparkle');
  }

  // ---------- 매 순간 ----------
  function tick(){
    if (me && done && me.bm && me.bm.end !== done.at && !OV && $('#bmv') && now2() - done.at < 30 * 6e4) close();   // 책상 창을 보던 중에 완성되면 창을 닫고 끝 연출로
    if (!me || bmOn || Date.now() < skipUntil || !(World.meAt && World.meAt())) return;
    const S = me.bm || {}, where = World.where() || '';
    if (done && S.made && !S.made.twelve && S.end === done.at) grant(false);
    if (uiBusy() || /^(gt_|arena|room_)/.test(where)) return;
    if (done){
      if (S.end !== done.at && (doneSeenEmpty || now2() - done.at < 3 * 6e4) && now2() - done.at < 30 * 6e4){ if (evTurn('bm')) ending(); return; }
      if (!(S.made && S.made.twelve)) grant(false); return;
    }
    if (ctl && ctl.open && S.ev !== ctl.id && evTurn('bm')) intro();
  }
  function listen(){
    if (offs.length) return;
    offs.push(GDB.on('bm/ctl', v => { ctl = v || null; }), GDB.on('bm/got', v => { got = v || {}; if ($('#bmv') && !drag) render(); }), GDB.on('bm/place', v => { place = v || {}; if ($('#bmv') && !drag && W.tab === 'book') render(); checkDone(); }),
      GDB.on('bm/done', v => { if (!v) doneSeenEmpty = true; const was = done; done = v || null; if (done && !was && $('#bmv')) render(); }));
    const ao = World.actOk; World.actOk = (o, a, m) => (m === 'library' && (a[0] === '사서 책상' || a[0] === '아울라의 독서대')) || (ao ? ao(o, a, m) : false);
    const oa = World.onAct; World.onAct = (m, o, a) => {
      if (m === 'library' && a[0] === '사서 책상'){ if (!tabsNow().length) return '<b>사서 책상</b><br>대출 카드가 가지런히 꽂혀 있어요. 「반납일을 지켜 주세요 · 아울라」'; open(done ? 'read' : 'book'); return; }
      if (m === 'library' && a[0] === '아울라의 독서대'){ if (done){ W.rp = 0; open('read'); return; } return met() ? '<b>아울라의 독서대</b><br>책장이 하얘요. 단어들이 돌아오면 다시 읽을 수 있어요' : '<b>아울라의 독서대</b><br>펼쳐진 책 옆에 깃털 펜이 놓여 있어요'; }
      return oa ? oa(m, o, a) : undefined;
    };
    const po = World.onOverlay; World.onOverlay = (q, toS, k) => { try { overlay(q, toS, k); } catch(e){} if (po) po(q, toS, k); };
    setInterval(() => { try { tick(); } catch(e){ errReport('bm', '책 tick 오류: ' + e.message, e.stack || ''); } }, 1500);
  }
  // ---------- 관리자 ----------
  function adminHTML(){
    const c = AD.bmctl || {}, G = AD.bmgot || {}, PL = AD.bmplace || {}, D = AD.bmdone || null, P = AD.players || {}, ids = Object.keys(P).filter(id => P[id]?.nick).sort((a, b) => P[a].nick.localeCompare(P[b].nick, 'ko'));
    const right = SL.reduce((a, p, pi) => a + p.filter((t, k) => { const o = PL[pi + '_' + k]; return t.w && o && ALL[o.w] === t.w; }).length, 0), pct = Math.floor(right / TOTAL * 100);
    const S = id => P[id].bm || {}, sawS = ids.filter(id => S(id).met), sawE = D ? ids.filter(id => S(id).end === D.at) : [];
    const cnt = id => Object.values(G).filter(v => v && v.u === id).length, pl = id => Object.values(PL).filter(v => v && v.u === id).length;
    return `<div class="adcard sdad"><div class="abhead"><b>아울라의 한밤 도서관 · 열두 개의 밤</b>${c.open ? '<button class="btn sm" data-bma="off">끄기</button>' : '<button class="btn sm go" data-bma="on">켜기</button>'}${c.open && !D ? '<button class="btn sm" data-bma="again">시작 연출 다시 보내기</button>' : ''}<button class="btn sm" data-bma="reset">처음부터</button></div>
      <div class="abchips"><span>${c.open ? '켜짐' : '꺼짐'}</span><span>책 완성 <b>${pct} %</b> (${right} / ${TOTAL} 칸)</span><span>모은 단어 <b>${Object.keys(G).length}</b> / ${ALL.length}</span>${D ? `<span>완성 ${new Date(D.at).toLocaleString('ko-KR')} · 마지막 ${esc(D.by || '')}</span>` : ''}</div>
      <div class="abchips"><span>시작 연출 본 학생 <b>${sawS.length}</b> / ${ids.length}</span><span>끝 연출 본 학생 <b>${sawE.length}</b> / ${ids.length}</span></div>
      ${ids.map(id => `<div class="sdarow"><span><b>${esc(P[id].nick)}</b></span><span class="s">시작 ${S(id).met ? '봄' : '–'} · 끝 ${D && S(id).end === D.at ? '봄' : '–'} · 찾은 단어 ${cnt(id)} · 놓은 칸 ${pl(id)} · 책갈피 ${Object.keys(S(id).made || {}).length}${S(id).pin && FX[S(id).pin] ? ` · 꽂음 「${esc(byId(S(id).pin).n)}」` : ''}</span></div>`).join('')}
      <div class="s" style="margin-top:6px">켜면 접속한 학생은 바로 도서관으로 옮겨져 아울라의 재채기 연출이 나와요. 연출을 본 학생은 채집 · 낚시에서 25 % 확률로 단어를 찾고(반 전체에 없는 단어만, 다 모이면 더 안 나와요), 사서 책상에서 다 같이 책을 맞춰요. 마지막 칸이 맞는 순간 접속한 학생 모두에게 끝 연출이 나오고, 모두 「열두 개의 밤」 책갈피를 받아요. 책갈피 만들기는 꺼도 계속돼요.</div></div>`;
  }
  document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-bma]'); if (!b) return; const a = b.dataset.bma, c = AD.bmctl || {};
    if (a === 'on'){ if (confirm('「열두 개의 밤」을 켤까요? 접속한 학생은 바로 도서관으로 옮겨져 재채기 연출이 나와요.')) GDB.set('bm/ctl', { open: true, id: c.id || now2(), at: now2() }).then(() => toast('켰어요')); }
    else if (a === 'again'){ if (confirm('시작 연출을 모든 학생에게 한 번 더 보낼까요? (모은 단어와 책은 그대로예요)')) GDB.upd('bm/ctl', { id: now2() }).then(() => toast('연출을 다시 보냈어요')); }
    else if (a === 'reset'){ if (confirm('모은 단어 · 맞춘 책 · 완성 기록을 다 지우고 처음부터 할까요? 만든 책갈피는 그대로예요.') && confirm('정말 지울까요? 되돌릴 수 없어요.')) Promise.all([GDB.set('bm/got', null), GDB.set('bm/place', null), GDB.set('bm/done', null), GDB.upd('bm/ctl', { id: now2() })]).then(() => toast('처음부터 다시 시작해요')); }
    else if (confirm('끌까요? 단어가 더 안 나오고 책도 못 맞춰요. 모은 것은 그대로 남고, 책갈피는 계속 만들 수 있어요.')) GDB.upd('bm/ctl', { open: false }).then(() => toast('껐어요')); });
  window.__bm = { admin: () => adminHTML(), give: w => GDB.set('bm/got/' + ALL.indexOf(w), { u: uid, by: me.nick, at: now2() }), intro: () => intro(), ending: () => ending(), open: t => open(t), put: (k, w) => put(k, w), drop: k => drop(k), W, ALL, PAGES, SL, TOTAL, FX, state: () => ({ bmOn, OV: !!OV, ctl, gotN: gotN(), right: rightN(), done }), fill: (n = TOTAL) => { let c = 0; SL.forEach((p, pi) => p.forEach((t, k) => { if (t.w && c < n){ c++; const i = ALL.indexOf(t.w); GDB.set('bm/got/' + i, { u: uid, by: me.nick, at: now2() }); GDB.set('bm/place/' + pi + '_' + k, { w: i, by: me.nick, u: uid, at: now2() }); } })); } };   // 시험용
  return { listen, open, drop, stat, val, buff, aff, spotW, spotExtra, examHint, pinHTML, adminHTML };
})();
