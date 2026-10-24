#!/bin/sh
# 모의 서버로 게임을 띄워요 (Firebase 대신 window.__seed 메모리 DB). 사용: tools/ui_mock.sh [저장소 루트] [포트]
#   사이트는 /tmp/.../scratchpad/mtest_<포트>/site 에 복사돼요. 페이지에서 window.__seed = { players: { me1: {...} } }, window.__uid = 'me1' 로 시드를 넣어요.
#   테스트용 손잡이 window.__T (openSheet·closeSheet·npcGet·evPlay·storyPlay 등)도 같이 넣어요
ROOT=${1:-/home/user/magionacademy}; PORT=${2:-8766}
S=/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/mtest_$PORT; mkdir -p $S/site/mock
cd $ROOT/public && cp -r art audio data world.js fonts credits.json firebase-config.js manifest.webmanifest $S/site/ 2>/dev/null; cp $ROOT/tools/mock/*.js $S/site/mock/
sed "s#const FB = 'https://www.gstatic.com/firebasejs/10.12.2/';#const FB = './mock/';#" index.html > $S/site/index.html
sed -i "s#^document.addEventListener('keydown', e => { if (evOn#window.__T = { xbGet: () => xb, BGM, penDoor: i => World.onPenDoor(i), penClaim: i => penClaim(i), myPen: () => myPenIdx(), evPlay: (...a) => evPlay(...a), npcGet: id => npcGet(id), npcEvent: (...a) => npcEvent(...a), NL, me: () => me, syncNpcs: () => syncNpcs(), npcMenu: n => npcMenu(n), hearts: id => hearts(id), weatherToday: () => weatherToday(), bandNow: () => bandNow(), castSprite: (id) => castSprite(id, {}), fill: (t, id) => fillVars(t, id), openSheet: (a, b) => openSheet(a, b), closeSheet: () => closeSheet(), storyPlay: (c) => storyPlay(c, STORY[c - 1].intro.concat(STORY[c - 1].ending), STORY[c - 1].name), render: () => render(), save: () => save(), toast: t => toast(t), openRoom: g => openRoom(g), hostStart: () => hostStart(), leaveRoom: () => leaveRoom(), xPoseDbg: (...a) => xPoseDbg(...a), xHandScan: () => xHandScan(), gameInfo: () => ({ room, g: G ? G.g : null, score: G ? G.score : null, ret: gameRet, spots: World.getSpots().length }) };\n&#" $S/site/index.html
cd $S/site && (curl -s -o /dev/null http://localhost:$PORT/ || (nohup python3 -m http.server $PORT >/dev/null 2>&1 &)); sleep 1
echo "http://localhost:$PORT/  (site: $S/site)"
