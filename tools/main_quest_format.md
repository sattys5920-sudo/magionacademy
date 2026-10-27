# 메인 의뢰 데이터 형식 (작가용)

기획서는 `tools/main_quest_spec.md`(캐릭터·단계 설계·국어 규칙). 이 문서는 **엔진에 맞춘 형식**이에요. 기획서와 다른 부분은 이 문서를 따르세요.
명령어·장소·조연·국어 규칙은 서브 NPC 형식 문서 `tools/npc_story_format.md`와 같아요(그 문서의 장소 표, 명령 표, 국어 규칙을 꼭 읽으세요).
검증: `python3 scripts/validate_main.py <quest_id>` → **위반 0 건**이 될 때까지 고쳐요.

## 설정 조정 (0 장 조사로 기획서에서 바뀐 것 — 꼭 지켜요)
- **등불자리**: 스텔라 대본에서 "등불을 든 사람 모양 · 일곱 개의 별 · 소맷자락 끝 흐린 별 · 등불 끝의 작은 별 · 빈자리 하나"로 이미 정해져 있어요. 그래서 **일곱 별 = 여섯 몬스터 가문 + 첫 마녀(학교)의 서약별**, **잭의 별 = 등불 안의 불씨 자리 = 지금 비어 있는 자리(빈자리)**예요. 잭은 가문이 아니라 "등불을 든 사람" 그 자체(스텔라 ♥3 옛날이야기의 "길 잃은 아이를 찾으러 밤새 등불을 들고 걷던 사람"). 의뢰 1~6을 끝낼 때마다 가문 별이 하나씩 밝아지고(여섯째 가문 = 조각이 속한 "불꽃 가문", 골렘·되살아난 자들), 마지막에 빈자리에 불씨가 켜져요. "일곱 등불의 서약" = 여섯 가문 + 첫 마녀가 든 일곱 등불이고, 그 등불들에 불을 붙인 게 잭의 불씨예요.
- **우르**는 사냥꾼(겸 나무꾼)이에요. 캇파 ♥8 "통나무집 사냥꾼 친구가 보름이면 여기 와서 같이 달 구경, 그 친구 말로는 늑대 울음은 다 바람 소리라더군"과 맞춰요. 별이 흐려지기 전엔 보름을 다스릴 수 있어 캇파와 달을 봤고, 요즘은 못 가요. "늑대 울음은 바람 소리"는 자기를 감추던 말이었다는 걸 4~5 단계에서 회수해요.
- **의뢰인 이름·아이디(고정)**: `blady` 블라디 · `yeoreum` 유령(5 단계에서 "썸머") · `beatrix` 베아트릭스 · `ur` 우르 · `somi` 리코 · `nefer` 네페르 · `piece` 조각(5 단계에서 주인공이 이름 지음, 기본값 "프랭") · `jack` 잭. 초상화는 옛 캐릭터 그림을 역할대로 재사용해요(루시안→블라디, 부우→썸머, 헤이즐→베아트릭스, 울프강→우르, 미라벨→네페르, 프랭키→조각). 대사에서 이름을 부를 때는 **`{blady.name}`처럼 변수로** 써요(조사도 `{blady.name|이/가}`). 유령·조각은 이름이 바뀌니까 꼭 변수로.
- 의뢰인 사이의 호칭: 블라디는 자기를 "이 몸", 남을 "학생", "그대"가 아니라 "너"; 네페르만 "그대"를 써요.
- 달은 **실제 달**이에요. `wait_moon`은 실제 보름(±1.5 일)·그믐(월령 ≤1.5 또는 ≥28)을 기다려요. 그믐꽃 같은 "그믐에만" 재료는 `wait_moon` 뒤에 `collect`로 받아요(조사 지점 `source`로 줍기).
- 호박달 축제 = 보름 전후 3 일. 잭 의뢰의 "등불 거두는 밤"은 **여섯째 의뢰를 끝낸 뒤 처음 맞는 축제가 끝난 첫 밤**이에요(`unlock.afterFestival`).

## 파일
```
public/data/main/index.json                 # 의뢰 순서 (이미 있음, 건드리지 마세요)
public/data/main/cast.json                  # 의뢰인·공통 조연 (이미 있음. 더 필요한 조연은 자기 quest.json 의 "cast"에)
public/data/main/places.json                # 추가 장소 (school_gate 학교 정문, hall_front 본관 앞, castle_hall 낡은 성 만찬장, museum 학교 박물관, old_lab 지하 실험실)
public/data/main/<quest_id>/quest.json
public/data/main/<quest_id>/stage_1_request.json … stage_5_request.json
public/data/main/<quest_id>/stage_1_complete.json … stage_5_complete.json
public/data/main/<quest_id>/idle.json
```
quest_id: `main_01_dracula` `main_02_ghost` `main_03_witch` `main_04_werewolf` `main_05_mummy` `main_06_frankenstein` `main_07_jack`

## quest.json
```json
{
  "id": "main_01_dracula", "order": 1, "name": "피가 무서운 흡혈귀", "client": "blady",
  "unlock": { "afterQuest": null, "daysAfter": 0, "time": "morning", "minDay": 1 },      // 2~6: afterQuest 앞 의뢰 id, daysAfter 3 · 7: "afterFestival": true
  "arrival": { "player": "hall_front" },          // 등장 컷신이 시작될 때 주인공이 서 있을 곳 (장소 id)
  "place": "hall_front",                          // 의뢰 중 의뢰인이 서 있는 기본 자리 (단계마다 stages[].place 로 바꿀 수 있어요)
  "after": { "place": "vamp_manor" },             // 의뢰를 끝낸 뒤 의뢰인이 남는 자리 (없으면 사라져요)
  "cast": { "countess": { "name": "백작 부인", "title": "블라디의 어머니", "look": 0 } },   // 이 의뢰만의 조연. look 0~3 (학생 기본 모습) 또는 "av": {...}
  "items": { "tomato": { "name": "토마토", "emoji": "🍅" }, "furn_coffin_bed": { "name": "블라디의 관 침대", "emoji": "⚰️", "furn": "bed" }, "cloth_x": { "name": "…", "emoji": "🧥", "cloth": "hat:hat_03" }, "pact_copy": { "name": "서약문 사본", "emoji": "📜", "key": true } },
  "recipes": [ { "id": "j_tomato", "name": "토마토 주스", "mats": { "tomato": 3 }, "mana": 2, "steps": 1, "place": "lab", "desc": "토마토를 솥에 넣고 한 번 휘저어요" } ],
  "stages": [
    { "n": 1, "title": "붉지만 무섭지 않은 것", "place": "hall_front",
      "actors": [ { "id": "somi", "place": "school_gate", "lines": ["아빠는…… 곧 올 거예요."], "mark": false } ],   // 이 단계 동안 맵에 서 있는 조연 (talk 목표의 상대)
      "deadline": 5,                                                        // 기한(일). 넘기면 craft 진행만 처음부터
      "objectives": [ … ], "rewards": { "gold": 50, "items": ["herb"] } }
  ],
  "completion_reward": { "items": ["lantern_shard", "furn_coffin_bed"] },
  "ending_flags": ["blady_spoke_himself", "player_spoke_for_blady"]
}
```
- `items`: 이 의뢰에서 새로 쓰는 아이템. `emoji`로 아이콘. `key: true`면 가방 「중요」 탭. `furn`은 내 방 가구 종류(bed, chair, table, lamp, rug, shelf, plant, …: `World.FURN.items` 의 id), `cloth`는 옷장 열쇠(`"hat:hat_03"` 같은 `종류:부품id`). **등불 조각은 `lantern_shard`** (이미 main_01에 정의됨, 다른 의뢰는 `completion_reward.items`에 `"lantern_shard"`만 넣으면 돼요).
- `recipes`: `craft` 목표가 만들 물건. `steps` 1~3(단계마다 때맞춰 누르기 → 다 맞히면 품질 `best`, 절반 넘게 `good`, 아니면 `normal`). `place`: `lab`(물약 교실 솥) 또는 `candy`(과자 교실 오븐).
- 기존 게임 아이템도 쓸 수 있어요: 재료 `herb drop mush honey silk wool milk hegg feather scale slime` …, 채집 `g_*`(온실 씨앗), `g2_*`(들판 채집), 물고기 `f_*`, 물약 `p_*`, 요리 `d_*`. 이름은 index.html 의 `ITEM`에 있어요(`grep -o "'[a-z0-9_]*': *'[^']*'" public/index.html | head`로 찾기).

### objectives (단계마다 1~3 개)
| type | 필드 | 뜻 |
|---|---|---|
| `collect` | `item`, `count`, `hint_location`(장소 id), `source: { "place": 장소 id, "x","y"(선택), "price": 5, "label": "토마토 사기" }` | `source`가 있으면 그 자리에 조사 지점이 떠서 하나씩 사거나 주워요(없는 아이템은 꼭 `source`를 주세요). 기존 재료는 평소대로 모아도 돼요 |
| `craft` | `item`, `count`, `quality`("normal"/"good"/"best"), `place` | `recipes`에 같은 id가 있어야 해요 |
| `deliver` | `to`(의뢰인·조연·서브 NPC id), `item`, `count`, `line` | 그 사람에게 말을 걸면 건네져요. `line`은 그때 한마디 |
| `visit` | `place`, `time`: ["night"], `weather`: ["rain"], `moon`: "full" | 그 자리 근처에 조건이 맞을 때 가면 돼요 |
| `talk` | `who`(서브 NPC id 또는 조연 id), `line`, `where`(힌트 장소) | 조연이면 이 단계 `actors`에 세워 두세요. 서브 NPC는 평소 자리에서 말을 걸면 `line`이 나와요 |
| `clue` | `count`, `text`("단서"), `spots: [ { "id": "c1", "place": "clock_tower", "x","y"(선택), "label": "조사하기", "title": "시계탑 종 밑", "text": "…흔적 설명 (1~3 문장)…", "hint": "시계탑", "item": 선택 } ]` | 조사 지점마다 물음표가 떠요 |
| `puzzle` | `kind`: "stars"(별자리 잇기: `count` 7, `stars` [[x%,y%]…], `order` [번호…], `hintText`, `showNext` true/false, `doneText`) 또는 "order"(순서 맞추기: `items` ["…"], `answer` [번호…]), `title`, `sub`, `text` | 일지에서 「풀기」 |
| `wait_moon` | `moon`: "full" 또는 "new" | |
| `defend` | `sec` 30, `place`(시작 장소), `text`, `hintText`, `doneText`, `hitDamage` 18 | 등불 지키기 미니 이벤트 |
| `choice` | `flags`: [결말 플래그 2 개], `text` | 5 단계 **부탁 장면**의 `choice`에서 플래그가 세워지면 끝나요 |

흐름: 부탁 장면이 끝나면 목표가 열려요 → 다 하면 의뢰인 머리 위에 ❗ → 말을 걸면 완료 장면 → 보상 → 다음 단계는 의뢰인에게 다시 말을 걸면 부탁 장면. 5 단계 완료 장면 뒤에 등불 조각·기념품을 받고 별이 켜져요.

## 장면 파일 (stage_N_request.json / stage_N_complete.json)
```json
{ "title": "정문의 망토", "scene": { "location": "hall_front", "time": "morning", "weather": "fog" },
  "arrival": [ …맵 컷신 명령 (1 단계 부탁 장면만)… ],
  "script": [ …서브 NPC와 같은 명령… ] }
```
- `script` 명령은 서브 NPC와 같아요: `line narration choice goto if_flag if_heart move follow walk show hide emote camera sfx wait fade_in fade_out flash give_item take_item set_flag`. (`bgm`은 써도 소리는 안 나요. `affinity`는 쓰지 마세요.)
- 메인에서 더 쓸 수 있는 것:
  - `{ "cmd": "if_quest", "quest": "main_01_dracula", "then": "a", "else": "b" }` 그 의뢰를 끝냈는지
  - `{ "cmd": "if_item", "item": "pact_copy", "n": 1, "then": "a", "else": "b" }`
  - `choice`의 선택지에 `"confirm": "되돌릴 수 없어요. 블라디가 직접 말하게 둘까요?"` 를 주면 확인 창이 떠요(**5 단계 결말 선택에 꼭**). `"flag"`로 결말 플래그.
  - `{ "cmd": "input", "key": "piece", "prompt": "이름을 지어 줘", "default": "프랭", "max": 6 }` 이름 짓기(조각). 그 뒤 `{piece.name}`이 바뀐 이름이 돼요.
  - `{ "cmd": "rename", "who": "yeoreum", "name": "썸머" }` 이름 되찾기.
- 말하는 사람 `who`: `player`, 의뢰인·조연 id(cast.json, quest.json cast), 서브 NPC id(`nabi` …), places/cast 의 조연(`fish_owner`, `grandma` …), `voice`. 의뢰인이 말하면 초상화가 뜨고 표정은 대사로 골라져요. 표정을 정하고 싶으면 대사 맨 앞에 `[기본]` `[웃음]` `[화남]` `[놀람]` `[부끄러움]`을 붙여요(화면엔 안 보여요).
- 장면이 시작될 때 의뢰인이 가운데, 주인공이 왼쪽에 서 있어요. 없어야 하면 첫 줄에 `hide`.
- **줄 수 세는 법**은 서브 NPC와 같아요: `line`과 `narration`만 세고, 한 경로(선택지를 하나씩 골라 끝까지 간 길) 기준이에요. 분기는 라벨로 뛰고 `goto`로 합류해요.

### 맵 컷신 `arrival` 명령 (1 단계 부탁 장면 첫머리. 실제 마을 맵 위에서 돌아가요)
| 명령 | 예 |
|---|---|
| `spawn` | `{ "cmd": "spawn", "who": "blady", "x": 7, "y": 27, "spr": 6, "name": "???" }` 의뢰인은 `spr`(blady 6 · yeoreum 7 · beatrix 8 · ur 9 · nefer 10 · piece 11 · jack 12), 조연은 `"av"` 또는 `"look": 0~3`. `name`을 비우면 이름표가 없어요. `"float": true, "alpha": .8` 유령 |
| `player` | `{ "cmd": "player", "x": 19, "y": 30, "dir": "left" }` 주인공 자리 |
| `walk` | `{ "cmd": "walk", "who": "blady", "x": 17, "y": 30, "run": false }` 걸어가요(끝날 때까지 기다림) |
| `face` | `{ "cmd": "face", "who": "blady", "to": "player" }` |
| `cam` | `{ "cmd": "cam", "who": "blady" }` 카메라가 따라가요 · `{ "cmd": "cam" }` 주인공으로 되돌림 |
| `say` | `{ "cmd": "say", "who": "blady", "text": "하하하! 이 몸이 왔다!", "ms": 2600 }` 머리 위 말풍선 |
| `emote` | `{ "cmd": "emote", "who": "blady", "icon": 4 }` 0 손인사 1 웃음 2 깔깔 3 하트눈 4 놀람 5 눈물 6 화남 7 하트 8 엄지척 9 반짝 10 호박 11 유령 |
| `crowd` | `{ "cmd": "crowd", "n": 5, "from": [13, 28], "react": "scream" | "flee" | "watch", "text": "뭐야 저거…", "hold": 2 }` 학생 구경꾼 |
| `fx` | `{ "cmd": "fx", "kind": "bats" | "lightning" | "bell" | "wind" | "dark" | "light", "sec": 4, "wait": 1 }` |
| `sfx` | `{ "cmd": "sfx", "id": "wing" }` 서브 NPC와 같은 효과음 id |
| `wait` | `{ "cmd": "wait", "sec": 1 }` |
| `fade` | `{ "cmd": "fade", "v": 1, "text": "안개 낀 아침" }` 어둡게 · `{ "cmd": "fade", "v": 0 }` 밝게 |
| `despawn` | `{ "cmd": "despawn", "who": "somi" }` |
컷신이 끝나면 임시 배우는 사라지고, 의뢰인은 `stages[0].place` 자리에 다시 서요. 마을 맵(campus) 좌표: 학교 정문 (12, 28), 마차 정류장 (6, 27), 본관 앞 (19, 30), 시계탑 (20, 16), 마을 광장 (61, 32), 등불 시장 (56, 28), 호박밭 (9, 60), 묘지 (48, 52), 유령 호수 잔교 (57, 56), 늑대인간 통나무집 앞 (78, 61), 뱀파이어 저택 앞 (67, 14), 마녀의 오두막 (73, 51), 언덕 위 무너진 오두막 (7, 7). 그 밖의 장소는 `public/data/npc/places.json`의 x, y.

## idle.json (반복 대사)
```json
{ "1": { "a": ["진행 중 한 줄", "둘째 줄엔 지금 목표 힌트"], "b": ["다 했는데 보고 전"], "c": ["이 단계 끝난 뒤 다음 부탁 전"] }, "2": {…}, … "5": {…},
  "done": ["의뢰 완료 후 한 줄", "둘째 줄"] }
```
각 상황 1~2 줄. 매번 같은 내용이 나와요.

## 서브 NPC 연결
- 하트 조건 분기는 `if_heart`(`"npc": "nabi", "min": 8, "then": …, "else": …)로, **else 쪽에도 꼭 대체 장면**을 둬요.
- 서브 NPC에게 재료를 받는 목표는 `talk`(하트가 되면 `line`에서 받았다고 하고 `rewards`로 주지 말고 `script`의 `give_item`으로) 대신 간단히: 부탁 장면에서 `if_heart` → `give_item`으로 주고, 안 되면 `collect`+`source`(시장 대체 재료)로 받도록 설계해요. 목표 하나로 막히지 않게.
- 서브 NPC가 말할 때는 그 NPC의 말투 단계(하트 A~D)를 따르되, 하트를 모르면 B(존댓말, 조금 친근) 말투로.
- 메인에서 새로 드러난 사실 뒤에 서브 NPC가 평소에 할 한 줄은 **`public/data/main/npc_lines.json`에 모아요**: `{ "stella": [ { "quest": "main_05_mummy", "lines": ["빈자리에 이름이 생겼어요. 잭이래요."] } ] }` (`"flag": "…"` 조건도 가능). 각 작가는 자기 의뢰 보고에 추가할 줄을 적어 주면 코디네이터가 합쳐요. 서브 NPC 대본 파일(`public/data/npc/…`)은 **절대 고치지 마세요**.
- 고정 사실(바꾸지 마세요): 캇파는 호수에서 30 년 · 나비의 첫 주인 오르솔라(늙은 약초 마녀, 초록 물든 손, 방울, 초록 잉크 쪽지, 몇 해 전 떠남, 견습생이 있었음) · 아울라의 제자 리나와 돌아온 책장 · 스텔라의 동생과 "걷는 건 우리" · 레오의 콩알(아기 까마귀) · 마들렌의 스승 늙은 제빵사와 호박달 케이크 · 스트로는 허수아비, 호박밭 할머니 · 배트리는 우체부 박쥐 · 맨디는 독초 온실의 맨드레이크 · 세라는 양호 선생님.

## 쓰는 법·시험
1. `quest.json` → `stage_1_request.json`(arrival 포함) … `stage_5_complete.json` → `idle.json`.
2. `python3 scripts/validate_main.py <quest_id>` 위반 0 건.
3. 실제로 돌려 보기: `tools/ui_mock.sh <저장소> <포트>` 로 모의 서버를 띄우고 Playwright로 `page.evaluate(() => __mq.set('<quest_id>', 1, 'pre'))` 뒤 `page.evaluate(() => { World.onNpc('mq:<client>'); return 1; })` 로 부탁 장면을 열어요(장면은 `document.querySelector('#evstage .evbox').click()`으로 넘기고, 선택지는 `.evo` 클릭). 상태는 `__mq.state()`, 완료 처리는 `__mq.state().ph = 'ready'` 뒤 다시 말 걸기. 등장 컷신은 `__mq.set('<quest_id>', 1, 'arrive'); __mq.tick()`. 스크린숏을 `audit/main/<quest_id>/`에 남겨요. (`__mq`, `World`, `__T`는 모의 페이지의 전역이에요. `p.evaluate`에 async 함수를 넘기면 장면이 끝날 때까지 기다리니 `return 1`로 끝내세요.)
4. 보고: 장면 제목·줄 수(검증 출력), 선택지와 플래그, 서브 NPC 연결, 새 조연·아이템·장소, npc_lines.json 에 넣을 줄, 다른 의뢰에 알려야 할 것(앞 의뢰 결말 플래그 이름 등).
