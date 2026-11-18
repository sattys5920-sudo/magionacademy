// 「녹슨 검의 대장장이」 장면 대본 (원본: tools/edric/story.md · 대사는 대본 그대로) · index.html 의 하트 이벤트 무대(evPlay)로 돌려요
//   [기본] [웃음] [화남] [놀람] [부끄러움] 은 에드릭 초상화 표정 (화면에는 안 나와요)
//   choice 의 id 는 날 번호 (1 ~ 7) · 고른 번호로 index.html 이 믿음 · 진실 · 용기 점수를 올려요
(() => {
  const FACE = ['기본', '웃음', '화남', '놀람', '부끄러움'];
  const E = (f, text) => ({ cmd: 'line', who: 'edric', text: `[${FACE[f]}] ${text}` });
  const P = text => ({ cmd: 'line', who: 'player', text });
  const L = (who, text) => ({ cmd: 'line', who, text });
  const N = text => ({ cmd: 'narration', text });
  const show = (who, at) => ({ cmd: 'show', who, at }), hide = who => ({ cmd: 'hide', who }), walk = (who, to) => ({ cmd: 'walk', who, to });
  const sfx = id => ({ cmd: 'sfx', id }), lab = label => ({ label }), go = to => ({ cmd: 'goto', to }), wait = sec => ({ cmd: 'wait', sec });
  const wx = weather => ({ cmd: 'wx', weather }), tint = v => ({ cmd: 'tint', v });
  const pick = (id, opts) => ({ cmd: 'choice', id, options: opts.map((text, i) => ({ text, next: `c${id}${'abc'[i]}` })) });
  const forge = (lit = true) => [show(lit ? 'ed_furnace' : 'ed_furnace_cold', 'right'), show('ed_sword', 'far_right')];
  const LETTER_HEAD = ['에드릭에게.', '네가 이걸 읽는다면, 살아서 마을에 갔다는 뜻이겠지. 다행이다.', '그날 네가 물러난 건 네 발이 아니라 내 마법이었어.'];
  const LETTER_REST = ['봉인에는 셋이면 충분했어. 그리고 누군가는 살아서 마을 사람들을 피신시켜야 했고.', '넌 제일 빨랐고, 제일 무서워했고, 그래서 제일 오래 살아 줄 사람이었어.', '마리엔은 반대했고, 토비는 울었어. 그래도 셋이 같이 정했어.',
    '그러니까 미안해하지 마. 우리가 너를 보낸 거야.', '대신 부탁 하나만 할게.', '언젠가 또 재가 내리면, 그땐 혼자 서 있지 마.'];
  const letter = lines => [sfx('paper'), ...lines.map(t => L('letter', t))];

  const S = {
    // 1 일째 · 대장간의 불 (고장 난 등불 맡기기)
    d1: () => ({ loc: 'market_alley', script: [
      ...forge(), { cmd: 'fade_in' }, sfx('hit'),
      N('밤마다 시장 뒷골목에서 망치 소리가 들린다. 비어 있던 창고에 불이 켜져 있다.'),
      N('화로 앞에서 덩치 큰 사람이 등을 돌린 채 쇠를 두드리고 있다.'),
      P('저기요.'), E(0, '....문 닫았다.'), P('불은 켜져 있는데요.'), E(0, '불이 켜져 있다고 문이 열린 건 아니야.'),
      sfx('hit'), N('쾅. 쾅. 망치가 멈추지 않는다. 벽에는 천으로 감싼 길쭉한 무언가가 걸려 있다.'),
      P('등불이 고장 나서요. 시장에선 여기 가 보라고 해서.'),
      N('망치가 멈춘다. 에드릭이 처음으로 돌아본다. 눈 밑이 깊게 꺼져 있다.'),
      E(0, '줘 봐.'),
      N('손등에 오래된 화상 자국이 있다. 큰 손이 작은 등불을 아주 조심스럽게 돌려 본다.'),
      E(0, '심지 받침이 휘었네. 이거 떨어뜨렸지.'), P('어떻게 알았어요.'), E(1, '쇠는 거짓말을 안 해.'),
      sfx('hit'), N('집게로 받침을 잡고 몇 번 두드리자, 등불이 다시 곧게 선다.'),
      E(0, '됐다. 가.'), P('얼마예요.'),
      pick(1, ['「그럼 내일 또 올게요.」', '「벽에 걸린 건 뭐예요.」', '(말없이 고개 숙여 인사하고 나간다)']),
      lab('c1a'), E(4, '....오지 마. 귀찮다.'), N('그런데 문을 닫지 않는다.'), go('j1'),
      lab('c1b'), E(2, '볼일 끝났으면 가라.'), N('목소리가 한 칸 낮아진다.'), go('j1'),
      lab('c1c'), walk('player', 'off_left'), N('나가는 등 뒤에서 망치 소리가 잠깐 멈췄다가, 다시 울린다.'), sfx('hit'), go('j1'),
      lab('j1'), E(0, '값은 됐어. 불 꺼지지 않게만 해.'),
    ] }),
    // 2 일째 · 녹슨 검 (재료를 건네고 풀무를 누른 뒤)
    d2: () => ({ loc: 'market_alley', script: [
      ...forge(), { cmd: 'fade_in' },
      N('대장간. 에드릭이 시장 사람들 냄비를 줄줄이 고치고 있다. 검은 하나도 없다.'),
      P('대장간인데 검은 안 만들어요.'), E(0, '냄비가 더 쓸모 있어.'),
      P('마을 아이들이 그러던데요. 진짜 대장장이면 검을 만든대요.'), E(1, '그럼 난 가짜 대장장이 해야겠다.'),
      sfx('fire'), N('풀무를 대신 눌러 준다. 불이 확 살아난다. 에드릭이 한 번 끄덕인다.'),
      E(1, '....손 괜찮네. 불 무서워하는 애들 많은데.'),
      sfx('wind'), hide('ed_sword'), show('ed_sword_bare', 'far_right'),
      N('바람에 벽의 천이 들린다. 녹슨 검이 보인다. 손잡이 아래에 홈이 네 개 새겨져 있다.'),
      pick(2, ['「물어봐도 돼요?」 하고 기다린다', '「그 홈 네 개는 뭐예요.」', '(천을 바로 하려고 검에 손을 뻗는다)']),
      lab('c2a'), E(0, '....안 돼.'), wait(1), N('한참 뒤에.'), E(4, '아직은.'), go('j2'),
      lab('c2b'), E(0, '숫자 셀 줄 알면 됐다. 네 개야.'), N('그 뒤로는 대답이 없다.'), go('j2'),
      lab('c2c'), walk('player', 'right'), N('손끝이 칼집에 닿는 순간.'), { cmd: 'camera', action: 'shake' }, E(2, '손대지 마.'),
      N('처음 듣는 큰 소리. 화로 불까지 흔들린다. 에드릭이 스스로 놀란 얼굴로 숨을 고른다.'),
      E(4, '....미안하다. 소리 질러서. 그건 내 것도 아니야.'), walk('player', 'left'), go('j2'),
      lab('j2'), hide('ed_sword_bare'), show('ed_sword', 'far_right'),
      N('에드릭이 천을 다시 덮는다. 아주 오래 된 버릇처럼, 매듭을 두 번 묶는다.'),
    ] }),
    // 3 일째 앞 · 광장의 수호대 놀이
    d3a: () => ({ loc: 'village_square', script: [
      hide('edric'), show('kid1', 'center'), show('kid2', 'right'), show('kid3', 'far_left'), show('kid4', 'far_right'), { cmd: 'fade_in' },
      N('마을 광장. 아이들이 나무 막대를 들고 놀고 있다.'),
      L('kid1', '나는 올가 대장. 불의 마법!'), L('kid2', '난 마리엔. 방패 쾅!'), L('kid3', '나 토비 할래. 활 쏘는 거.'),
      L('kid1', '그럼 너는 검사 해. 도망치는 검사.'), L('kid4', '싫어. 맨날 나만 도망쳐.'),
      { cmd: 'walk', who: 'kid4', to: 'off_right' }, L('kids_v', '도망쳐라, 겁쟁이 검사. 도망쳐라.'),
      walk('edric', 'far_right'),
      N('광장 끝, 냄비 꾸러미를 든 에드릭이 멈춰 서 있다. 표정이 보이지 않는다.'),
    ] }),
    // 3 일째 뒤 · 마을 어르신의 이야기
    d3b: () => ({ loc: 'village_square', script: [
      hide('edric'), show('elder_a', 'center'), show('kid1', 'right'), show('edric', 'far_right'), { cmd: 'fade_in' },
      L('elder_a', '아이고, 또 그 놀이네. 이십 년 전에 진짜 있던 일이야. 넷이 나가서 셋은 못 돌아왔지.'),
      L('elder_a', '하나는 살아 돌아왔는데, 다들 그러더라. 도망쳤다고. 그 뒤로 마을을 떠났다던데.'),
      pick(3, ['아이들에게 「그 역은 빼자」고 한다', '아이들 놀이에 같이 끼어 검사 역을 맡는다', '돌아서는 에드릭을 따라간다']),
      lab('c3a'), L('kid4', '진짜? 그럼 나도 방패 할래.'), N('에드릭이 아주 잠깐 이쪽을 본다.'), go('j3'),
      lab('c3b'), P('내가 검사 할게. 근데 이번엔 안 도망쳐.'), sfx('crowd'), N('아이들이 와 하고 웃는다. 에드릭이 냄비를 고쳐 든다.'), go('j3'),
      lab('c3c'), walk('edric', 'off_right'), { cmd: 'move', to: 'market_alley', clear: true }, show('edric', 'right'), walk('player', 'left'),
      N('골목 모퉁이. 에드릭이 벽에 이마를 대고 서 있다.'),
      E(4, '....따라오지 마라.'), P('그 검사, 아저씨예요.'), E(0, '.......'), go('j3'),
      lab('j3'), { cmd: 'fade_out' }, { cmd: 'move', to: 'market_alley', clear: true, time: 'night', transition: 'dark' }, ...forge(false), { cmd: 'fade_in' },
      N('그날 밤 대장간은 일찍 불이 꺼졌다.'),
    ] }),
    // 4 일째 · 언덕의 세 잔 (밤)
    d4: () => ({ loc: 'hill_top', time: 'night', script: [
      hide('player'), show('ed_cups', 'right'), { cmd: 'fade_in' }, sfx('wind'),
      N('별 보는 언덕. 바람이 차다. 에드릭이 바위 위에 작은 잔 세 개를 나란히 놓는다.'),
      E(0, '올가. 올해도 왔어. 마리엔, 네가 좋아하던 사과주. 토비, 넌 아직 어리니까 물.'),
      E(4, '....나는 이십 년째 같은 말만 하네.'),
      sfx('step'), N('발밑에서 나뭇가지가 부러진다. 에드릭이 돌아본다.'),
      E(0, '....거기 있는 거 안다.'), walk('player', 'left'),
      pick(4, ['말없이 곁에 앉는다', '「정말 도망쳤어요?」', '바위에 잔 하나를 더 놓는다']),
      lab('c4a'), N('한참을 같이 별을 본다.'), E(1, '....너 같은 애가 하나 있었지. 말없이 옆에 앉는 애. 토비였어.'), go('j4'),
      lab('c4b'), E(1, '(웃음 같은 숨) 다들 돌려 말하는데. 넌 바로 묻네.'), go('j4'),
      lab('c4c'), hide('ed_cups'), show('ed_cups4', 'right'), sfx('pop'), E(3, '....그건 누구 거냐.'),
      P('아저씨 거요. 아저씨도 그날 거기 있었잖아요.'), N('에드릭이 그 잔을 오래 내려다본다.'), go('j4'),
      lab('j4'), E(0, '잿빛 날개 앞에서, 올가가 그랬어. 「다 같이 버티자.」'),
      E(4, '그런데 난 한 발 물러났어. 딱 한 발.'),
      E(0, '그다음에 기억나는 건, 산 아래 마을 입구에 쓰러져 있던 거야. 뒤에서 하늘이 하얗게 타고 있었고.'),
      E(0, '셋은 거기 남았고, 난 여기 있어. 그게 다야.'),
      wx('ash'), tint('rgba(170,50,40,.16)'),
      N('잔 위로 재 한 점이 내려앉는다. 북쪽 하늘이 희미하게 붉다.'),
    ] }),
    // 5 일째 · 다시 오는 재 (마을 어른 셋에게 들은 뒤 대장간)
    d5: () => ({ loc: 'market_alley', weather: 'ash', script: [
      ...forge(false), show('ed_bag', 'left'), { cmd: 'fade_in' },
      N('대장간. 화로가 꺼져 있다. 에드릭이 짐을 꾸리고 있다. 녹슨 검만 벽에 그대로다.'),
      P('어디 가요.'), E(0, '여기 있으면 또 기대하잖아. 내가 뭘 할 거라고.'),
      E(4, '난 그때도 물러났어. 이번에도 물러날 거야. 그럴 바엔 먼저 가는 게 낫지.'),
      pick(5, ['짐 가방을 붙잡는다', '「가요. 대신 진짜 이유는 말하고 가요.」', '「그럼 가기 전에 저희한테 싸우는 법 알려 줘요.」']),
      lab('c5a'), E(2, '놔라.'), N('놓지 않는다. 에드릭이 가방을 내려놓는다.'), E(4, '....고집은.'), go('j5'),
      lab('c5b'), E(3, '진짜 이유.'), wait(1), N('한참 뒤.'), E(4, '무서워. 다시 그 자리에 서는 게. 그게 진짜야.'), go('j5'),
      lab('c5c'), E(0, '검 쥐는 법은 안 알려 줘.'), sfx('fire'), hide('ed_furnace_cold'), show('ed_furnace', 'right'),
      N('그런데 화로에 다시 불을 붙인다.'), E(1, '등불 드는 법은 알려 주지. 불은 앞이 아니라 옆 사람을 비추는 거다.'), go('j5'),
      lab('j5'), N('그날 에드릭은 떠나지 않았다. 짐 가방은 문 옆에 그대로 놓여 있다.'),
    ] }),
    // 6 일째 앞 · 부엉이 우체국의 편지
    d6a: () => ({ loc: 'owl_post_inside', script: [
      hide('edric'), show('batri', 'center'), { cmd: 'fade_in' }, sfx('wing'),
      N('부엉이 우체국. 배트리가 먼지투성이 편지를 들고 날개를 퍼덕인다.'),
      L('batri', '[놀람] 이거, 우체국 맨 안쪽 서랍에서 나왔어요. 받는 사람은 에드릭. 그런데 주소가 이상해요.'),
      L('batri', '[기본] 「그가 스스로를 용서할 수 있을 때.」'),
      L('batri', '[기본] 그레이 국장님 말로는, 이런 주소는 그 사람이 준비가 돼야만 배달된대요. 그래서 이십 년 동안 한 번도 도착 못 했대요.'),
    ] }),
    // 6 일째 뒤 · 이십 년 늦은 편지 (믿음 2 이상이면 열려요)
    d6b: open => ({ loc: 'market_alley', script: [
      ...forge(), { cmd: 'fade_in' },
      N('대장간. 에드릭이 봉투에 적힌 글씨를 보자마자 얼굴이 하얘진다.'),
      E(3, '....올가 글씨야.'),
      ...(open ? [N('봉투가 저절로 풀린다. 에드릭의 손이 떨린다. 편지를 대신 읽어 달라고 내민다.'), ...letter(LETTER_HEAD), E(3, '....뭐라고.')]
        : [N('봉투는 꿈쩍도 하지 않는다. 에드릭이 봉투를 화로 옆에 내려놓는다.'), E(4, '그렇지. 나는 아직이지.')]),
      pick(6, ['「끝까지 같이 읽어요.」', '「아저씨는 도망친 게 아니었어요.」', '「이제 어떻게 할 거예요.」']),
      lab('c6a'), lab('c6b'), lab('c6c'), wait(1),
    ] }),
    // 7 일째 앞 · 마지막 불 (밤의 대장간 · 편지 · 마지막 선택)
    d7: opened => ({ loc: 'market_alley', time: 'night', weather: 'ash', script: [
      ...forge(), tint('rgba(190,40,30,.22)'), { cmd: 'fade_in' }, { cmd: 'flash' }, sfx('thunder'), { cmd: 'camera', action: 'shake' },
      N('밤. 북쪽 하늘이 붉게 갈라진다. 거대한 재의 날개 그림자가 마을 위로 드리운다.'),
      sfx('crowd'), N('시장 사람들이 등불을 들고 우왕좌왕한다. 대장간 문이 열려 있다. 에드릭이 녹슨 검 앞에 서 있다.'),
      E(0, '이십 년 전이랑 똑같아. 하늘도, 냄새도.'),
      E(4, '이번엔 물러나지 말라고, 누가 좀 말해 주면 좋겠는데.'),
      ...(opened ? letter(LETTER_REST) : [N('화로 옆 봉투가 저절로 풀린다. 마지막 기회.'), ...letter([...LETTER_HEAD, ...LETTER_REST])]),
      pick(7, ['녹슨 검을 건넨다', '등불을 건넨다', '「검 말고, 다른 걸로 지켜요.」']),
      lab('c7a'), lab('c7b'), lab('c7c'),
    ] }),
    // 7 일째 · 결말이 정해진 뒤 대장간에서
    d7A: () => ({ loc: 'market_alley', time: 'night', weather: 'ash', script: [
      ...forge(), tint('rgba(190,40,30,.22)'), { cmd: 'fade_in' },
      sfx('magic'), hide('ed_sword'), show('ed_sword_glow', 'far_right'), { cmd: 'flash' },
      N('에드릭이 천을 풀고 검을 든다. 녹이 부서져 내리며, 아래에서 희미한 빛이 새어 나온다.'),
      E(0, '혼자 서 있지 말라고 했지. ....따라와. 대신 내 뒤 말고, 옆에.'),
    ] }),
    d7B: () => ({ loc: 'market_alley', time: 'night', weather: 'ash', script: [
      ...forge(), tint('rgba(190,40,30,.22)'), { cmd: 'fade_in' },
      E(0, '검으로 막으면, 또 누군가 남겠지. 이번엔 다르게 할 거야.'),
      sfx('fire'), hide('ed_sword'),
      N('에드릭이 녹슨 검을 화로에 넣는다. 쇠가 붉게 녹는다. 망치 소리가 밤새 울린다.'), sfx('hit'), wait(1), sfx('hit'),
    ] }),
    // 결말 A · 검을 든 대장장이 (언덕)
    endA: () => ({ loc: 'hill_top', time: 'night', weather: 'ash', script: [
      tint('rgba(190,40,30,.24)'), show('st1', 'far_left'), show('ed_sword_glow', 'right'), show('st2', 'far_right'), { cmd: 'fade_in' },
      N('언덕. 학생들이 등불을 들고 반원으로 선다. 에드릭이 맨 앞에서 검을 든다.'),
      sfx('wing'), { cmd: 'camera', action: 'shake' }, sfx('dragon'),
      N('재의 날개가 내려앉는 순간, 등불 빛이 한데 모여 검끝으로 흘러든다. 하얀 빛. 이십 년 전과 같은 빛.'),
      sfx('magic'), { cmd: 'flash' }, { cmd: 'flash' },
      L('olga', '거봐. 혼자가 아니잖아.'),
      wx(null), tint(null),
      N('날개가 재가 되어 흩어진다. 조용해진 언덕에서 에드릭이 무릎을 꿇는다.'),
      E(4, '....다녀왔어.'),
      { cmd: 'fade_out' }, { cmd: 'move', to: 'market_alley', clear: true, time: 'day', weather: 'clear', transition: 'dark' }, ...forge(), hide('ed_sword'), show('ed_sword5', 'far_right'), show('edric', 'center'), { cmd: 'fade_in' },
      N('다음 날. 녹슨 검 손잡이 아래에 홈이 하나 늘어 있다. 다섯 개.'),
      E(1, '이건 너희 몫이다.'),
    ] }),
    // 결말 B · 검을 녹인 날 (언덕 · 새벽)
    endB: () => ({ loc: 'hill_top', time: 'morning', script: [
      show('ed_bell', 'right'), show('st1', 'far_left'), show('st2', 'far_right'), { cmd: 'fade_in' },
      N('새벽. 언덕 위에 작은 종 하나가 걸린다. 종 옆면에 이름 셋이 새겨져 있다. 올가. 마리엔. 토비.'),
      E(4, '너희가 울려 줘. 내 손으로는 못 하겠다.'),
      sfx('bell'), wait(1), sfx('bell'), wait(1), sfx('bell'),
      N('학생들이 한 명씩 종을 울린다. 소리가 북쪽 하늘까지 번진다. 종소리에 남아 있던 올가의 마법이 깨어나 봉인이 다시 감긴다.'),
      { cmd: 'flash' }, sfx('magic'),
      N('에드릭이 처음으로 소리 내어 운다. 세 사람 이름을 하나씩 부르며.'),
      E(4, '미안했어. 아니, 고마웠어. 이게 맞는 말이지.'),
    ] }),
    // 결말 C · 떠난 뒷모습
    endC: () => ({ loc: 'hill_top', time: 'night', weather: 'ash', script: [
      hide('edric'), tint('rgba(190,40,30,.22)'), show('st1', 'far_left'), show('st2', 'center'), show('st3', 'right'), show('elder_a', 'far_right'), { cmd: 'fade_in' },
      sfx('wing'), { cmd: 'camera', action: 'shake' },
      N('그날 밤, 재의 날개는 마을 학생들과 어른들의 등불 앞에서 물러간다. 봉인은 겨우 다시 걸린다.'),
      wx(null), tint(null),
      { cmd: 'fade_out' }, { cmd: 'move', to: 'market_alley', clear: true, time: 'day', weather: 'clear', transition: 'dark' }, show('ed_furnace_cold', 'right'), { cmd: 'fade_in' },
      N('하지만 대장간은 비어 있다. 녹슨 검도, 짐 가방도 없다. 화로만 아직 따뜻하다.'),
      N('며칠 뒤, 우체국을 거쳐 엽서 한 장이 온다.'), sfx('paper'),
      L('card', '아직은 못 하겠다. 미안하다.'), L('card', '대신 너는 물러나지 마라.'), L('card', '불 꺼지지 않게 해라.'),
    ] }),
  };
  // 마을 어른 셋 (5 일째 · 말을 걸면 한마디씩)
  const ADULT = { merchant: '북쪽 봉인이 풀린대. 이십 년 만에.', elder_b: '그때 도망친 그 검사, 요즘 뒷골목에 있다며. 이번에도 도망칠 거야.', elder_a: '쉿. 애들 듣는다.' };
  window.EdricFX = { S, ADULT, LETTER: [...LETTER_HEAD, ...LETTER_REST], LETTER_HEAD };
})();
