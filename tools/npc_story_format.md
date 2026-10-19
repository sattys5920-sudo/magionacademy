# NPC 하트 이벤트 데이터 형식 (작가용)

원래 기획서는 `tools/npc_story_spec.md`예요. 거기 적힌 캐릭터 설계, 국어 규칙, 분량 규칙을 그대로 지켜 주세요.
이 문서는 **실제 게임 엔진에 맞춘 형식**이에요. 기획서의 예시 형식과 다른 부분은 이 문서를 따르세요.
검증은 `python3 scripts/validate_npc.py <npc_id>`로 해요. **위반 0 건**이 될 때까지 고쳐 주세요.

## 파일
```
public/data/npc/<npc_id>/profile.json
public/data/npc/<npc_id>/events/heart_01.json … heart_10.json
```
npc_id: nabi, batri, kappa, aula, mandi, jipsin, sera, madeleine, stella, leo

## 게임 시간·날씨 (실제 시계 기준)
- 시간대 `time`: `morning`(5~10 시, 새벽·아침), `day`(10~16 시, 낮·점심), `evening`(16~21 시, 저녁·노을), `night`(21~5 시, 밤)
- 날씨 `weather`: `clear`, `rain`, `fog`, `snow`. 날마다 모두에게 같은 날씨가 정해져요(비 약 25 %, 안개 약 15 %, 눈은 겨울에만).
  - **폭풍우 장면**은 조건을 `"weather": ["rain"]`로 두고, 장면에서 `"scene": {"weather": "storm"}` 또는 `move`의 `"weather": "storm"`으로 연출해요.
  - **눈만** 조건으로 두지 마세요. 겨울에만 열려서 사실상 못 봐요.
- `"moon": "full"`은 보름 전후 3 일이에요. **호박달 축제**는 `"festival": true`이고, 매달 보름 3 일 동안 열려요.
- `"dow": [0,6]` 요일(0 일요일), `"afterDays": n` 이 NPC의 바로 앞 하트 이벤트를 본 날에서 n 일이 지난 뒤, `"after": ["aula:8"]` 다른 NPC의 하트 이벤트를 본 뒤.
- 조건은 너무 빡빡하지 않게 해 주세요. 시간대 1~2 개, 날씨는 꼭 필요한 이벤트만(NPC당 2~4 개 정도).

## 장소 (`public/data/npc/places.json`)
- `conditions.location`(이벤트가 시작되는 곳)은 **`서 있음` 장소만** 쓸 수 있어요. 조건이 맞으면 NPC가 그 시간에 그 장소에 서 있고, 머리 위에 ❗가 떠요.
- `move`, `follow`로는 아래 **모든 장소**에 갈 수 있어요. 배경은 그 장소를 잘라 온 그림이에요.
- 기획서의 장소 ID가 여기 있으면 그대로 써요. 없는 곳(예: 할머니 집 마루)은 이 목록에서 고르세요.

| id | 이름 | 종류 |
|---|---|---|
| `lantern_market` | 등불 시장 | 서 있음 |
| `fish_stall` | 생선 가게 | 서 있음 |
| `market_alley` | 시장 뒷골목 | 서 있음 |
| `market_roof` | 시장 지붕 | 서 있음 |
| `owl_post` | 부엉이 우체국 | 서 있음 |
| `village_square` | 마을 광장 | 서 있음 |
| `ghost_lake_pier` | 유령 호수 잔교 | 서 있음 |
| `lakeside` | 호숫가 | 서 있음 |
| `main_hall` | 본관 | 서 있음 |
| `potion_class` | 물약 교실 | 서 있음 |
| `infirmary` | 양호실 | 서 있음 |
| `library_stacks` | 도서관 서고 | 서 있음 |
| `aula_study` | 아울라 연구실 | 서 있음 |
| `poison_greenhouse` | 독초 온실 | 서 있음 |
| `pumpkin_field` | 호박밭 | 서 있음 |
| `old_windmill` | 낡은 풍차 | 서 있음 |
| `candy_class` | 과자 교실 | 서 있음 |
| `craft_class` | 공예 교실 | 서 있음 |
| `witch_hut` | 마녀의 오두막 | 서 있음 |
| `hill_ruin` | 언덕 위 무너진 오두막 | 서 있음 |
| `menagerie` | 사육장 | 서 있음 |
| `pen` | 방목장 | 서 있음 |
| `swamp` | 늪지 | 서 있음 |
| `cemetery` | 묘지 | 서 있음 |
| `vamp_manor` | 뱀파이어 저택 앞 | 서 있음 |
| `ghost_tea` | 유령 찻집 | 서 있음 |
| `bakery` | 호박 빵집 | 서 있음 |
| `candy_shop` | 사탕 가게 | 서 있음 |
| `dorm_street` | 기숙사 거리 | 서 있음 |
| `station` | 마차 정류장 | 서 있음 |
| `wolf_cabin` | 늑대인간 통나무집 앞 | 서 있음 |
| `player_room` | 내 방 | 서 있음 |
| `optician` | 시장 안경점 | 이동 전용 |
| `flower_shop` | 광장 꽃집 | 이동 전용 |
| `owl_post_inside` | 우체국 안 | 이동 전용 |
| `owl_post_back` | 우체국 뒤편 | 이동 전용 |
| `clock_tower` | 시계탑 | 이동 전용 |
| `hall_corridor` | 본관 복도 | 이동 전용 |
| `empty_classroom` | 본관 빈 교실 | 이동 전용 |
| `ghost_lake_cave` | 유령 호수 동굴 | 이동 전용 |
| `lake_hut` | 호숫가 오두막 | 이동 전용 |
| `sera_home` | {sera.name}의 집 | 이동 전용 |
| `grandma_house` | 할머니 집 마루 | 이동 전용 |
| `greenhouse_back` | 온실 뒤뜰 | 이동 전용 |
| `barn_burnt` | 그을린 헛간 | 이동 전용 |
| `hill_top` | 별 보는 언덕 | 이동 전용 |

### NPC 평소 루틴 (시간대별로 서 있는 곳, 그 안에서 계속 돌아다녀요)
| NPC | 아침 | 낮 | 저녁 | 밤 |
|---|---|---|---|---|
| nabi | fish_stall | lantern_market | fish_stall | market_roof |
| batri | owl_post | village_square | dorm_street | owl_post |
| kappa | ghost_lake_pier | lakeside | ghost_lake_pier | lakeside |
| aula | potion_class | potion_class | potion_class | library_stacks |
| mandi | poison_greenhouse | poison_greenhouse | swamp | poison_greenhouse |
| jipsin | pumpkin_field | pumpkin_field | pumpkin_field | pumpkin_field |
| sera | infirmary | infirmary | ghost_tea | infirmary |
| madeleine | bakery | candy_class | lantern_market | candy_class |
| stella | vamp_manor | witch_hut | village_square | hill_ruin |
| leo | pen | menagerie | swamp | menagerie |

하트 이벤트 조건이 맞으면 NPC는 루틴 대신 그 이벤트 장소에 서 있어요. 그래서 이벤트 장소를 루틴과 꼭 맞출 필요는 없어요. 다만 맞추면 자연스러워요.

## 등장인물 (`who`) — `public/data/npc/cast.json`
| id | 이름 | 메모 |
|---|---|---|
| `player` | {player} |  |
| `nabi` | 나비 |  |
| `batri` | 배트리 |  |
| `kappa` | 캇파 |  |
| `aula` | 아울라 |  |
| `mandi` | 맨디 |  |
| `jipsin` | 짚신 |  |
| `sera` | {sera.name} |  |
| `madeleine` | {madeleine.name} |  |
| `stella` | {stella.name} |  |
| `leo` | {leo.name} |  |
| `fish_owner` | 생선 가게 주인 |  |
| `apprentice` | 생선 가게 견습생 |  |
| `orsola` | 오르솔라 | 나비의 첫 주인, 늙은 마녀 (회상) |
| `gray` | 그레이 국장 | 부엉이 우체국장 |
| `kkaksun` | 깍순 | 선배 우체부 까치 |
| `grandma` | 호박밭 할머니 |  |
| `rina` | 리나 | 아울라의 옛 제자 |
| `husband` | {sera.husband} | 세라의 배우자 |
| `elder_a` | 마을 어르신 |  |
| `elder_b` | 시장 노인 |  |
| `merchant` | 시장 상인 |  |
| `kids` | 아이들 |  |
| `optician` | 안경점 주인 |  |
| `florist` | 꽃집 주인 |  |
| `old_lady` | 편지 속 할머니 |  |
| `grandson` | 손자 |  |
| `mentor` | 늙은 제빵사 | 마들렌의 스승 (회상) |
| `stella_sib` | {stella.name}의 동생 |  |
| `kongal` | 콩알 | 레오의 아기 용 |
| `baby_goat` | 아기 염소 |  |
| `crow` | 까마귀 |  |
| `baby_crow` | 아기 까마귀 |  |
| `lake_lord` | 호수의 주인 |  |
| `bees` | 벌들 |  |
| `voice` | 목소리 |  |

- 주인공은 `player`예요. 이름은 `{player}`. 주인공의 성별을 단정하지 마세요(외모를 꾸밀 수 있어요).
- 사람 NPC 이름은 바뀔 수 있어요. 대사에서는 항상 변수로 쓰세요: `{npc.name}`(이벤트 주인 자기 이름), `{sera.name}`, `{madeleine.name}`, `{stella.name}`, `{leo.name}`, `{sera.husband}`(세라 이벤트 안에서는 `{npc.husband}`도 돼요). 동물 NPC 이름(나비, 배트리, 캇파, 아울라, 맨디, 짚신)은 그대로 써도 돼요.
- **이름 뒤 조사는 함수로 써요.** 이름은 바뀔 수 있어서 받침 유무를 미리 알 수 없어요. `{player|이/가}`, `{npc.name|은/는}`, `{sera.husband|을/를}`처럼 **받침 있을 때/없을 때** 순서로 쓰면 엔진이 실제 이름을 보고 골라요. 쓸 수 있는 쌍: 이/가, 은/는, 을/를, 과/와, 아/야, 이랑/랑, 으로/로(ㄹ 받침은 '로'), 이에요/예요, 이야/야, 이나/나, 이라는/라는, 이라면/라면, 이다/다, 이었/였, 이구나/구나, 이요/요, 이네/네. 변수 바로 뒤에 조사를 그냥 붙이거나 "을(를)"처럼 병기하면 검증 스크립트가 잡아요. 의/도/만/에게/한테처럼 받침과 상관없는 조사는 그냥 붙여요.
- 표에 없는 조연이 필요하면 `profile.json`의 `"cast"`에 추가하세요: `"cast": {"fish_wife": {"name": "생선 가게 안주인", "look": 201}}`. 사람은 `look`(아무 숫자, 생김새 씨앗), 동물은 `"cr": "sheep|rabbit|lizard|chicken|cat|toad|bee|spider|owl|goat"`, 목소리만 나오면 `"kind": "voice"`예요. 이름에 성별을 단정하는 말(아저씨 등)은 넣지 마세요.

## profile.json
```json
{
  "id": "nabi", "name": "나비", "title": "매점 고양이",
  "likes": ["f_crucian", "d_minnowfry", "g2_catnip"], "dislikes": ["j_weed"],
  "vars": {},
  "tone": {"A": "호칭 야·인간 / 짧은 반말 …", "B": "…", "C": "…", "D": "…"},
  "daily": {"A": ["…12 줄 이상"], "B": ["…"], "C": ["…"], "D": ["…"]},
  "ambient": {"morning": ["…"], "day": ["…"], "evening": ["…"], "night": ["…"], "rain": ["…"], "fog": ["…"], "snow": ["…"], "clear": ["…"]},
  "gift": {"love": ["…3 줄 이상"], "like": ["…"], "hate": ["…"]},
  "recall": {"2": ["♥2 이벤트를 본 뒤 평소에 섞이는 말"], "5": ["…"], "flag:nabi_promise_stay": ["그 플래그가 있을 때만"]},
  "cast": {}
}
```
- `likes`/`dislikes`는 `tools/npc_items.json`의 아이템 id예요. 기획서의 좋아함·싫어함 이름과 같은 아이템을 찾아 쓰세요.
- `daily`는 말투 단계(A 하트 0~2, B 3~5, C 6~8, D 9~10)마다 12 줄 이상이에요. 한 줄 = 말풍선 하나.
- `ambient`의 키는 위 8 개 중에서 고르세요. `morning`, `day`, `evening`, `night`, `rain`, `fog`는 꼭 있어야 해요. 값은 문자열 배열이고, 말투 단계를 섞지 않게 너무 친하거나 너무 차갑지 않은 말로 써요.
- `recall`은 하트 이벤트를 본 뒤 평소 대사에 섞여 나오는 회상이에요. 키 5 개 이상.
- 사람 NPC는 `vars`에 이야기 속 변수 기본값을 넣어요(예: 세라 `{"husband": "루카스"}`).

## heart_XX.json
```json
{
  "id": "nabi_heart_03", "npc": "nabi", "heart": 3, "title": "비 오는 날의 상자",
  "conditions": {"minHeart": 3, "location": "lantern_market", "time": ["evening"], "weather": ["rain"]},
  "scene": {"weather": "rain"},
  "rewards": {"coin": 50, "mana": 0, "know": 0, "items": {"f_crucian": 1}, "flags": [], "perk": null},
  "script": [ … ],
  "cold": [ {"cmd": "line", "who": "nabi", "face": "annoyed", "text": "……"}, … 5~10 줄 ]
}
```
- `scene`(선택): 처음 장면의 `time`·`weather`를 연출용으로 바꿔요(회상 장면 등). 없으면 실제 시간·날씨예요.
- `rewards.perk`는 ♥10 같은 큰 보상에만 쓰세요. 쓸 수 있는 값: `cat_furniture`, `bait`, `free_post`, `rod_bonus`, `lord_hint`, `potion_hint`, `know_bonus`, `greenhouse_growth`, `pumpkin_race`, `scarecrow_hat`, `tasty_potion`, `cake_recipe`, `fortune`, `rare_egg`. 여러 개면 배열로 써요.

### 스크립트 실행 방식
- 배열을 **위에서부터 차례로** 실행해요. `{"label": "이름"}`은 자리 표시예요(아무것도 안 해요).
- `choice`, `if_flag`, `if_heart`는 지정한 라벨로 **점프**해요. 각 분기 장면의 끝에는 반드시 `{"cmd": "goto", "to": "합류라벨"}`을 넣어서 합류시키세요. 그러지 않으면 다음 분기 장면으로 흘러 들어가요(검증 스크립트가 잡아요).
- 모든 이벤트에는 `{"label": "ending"}`이 있어야 해요. 이벤트 안에서 받은 호감도 합이 **−30 이하**면, `ending` 지점부터는 원래 대사 대신 `cold`(서먹한 결말 5~10 줄)가 나오고 끝나요. 그러니까 `ending`은 마지막 장면(보통 마지막 10~20 줄)의 시작에 두세요.
- 엔진이 자동으로 만드는 플래그도 있어요.
  - `<npc>_was_cold`: 바로 앞 이벤트가 서먹하게 끝났으면 켜져요. **♥2부터는 첫머리에** `{"cmd": "if_flag", "flag": "<npc>_was_cold", "then": "cold_open", "else": "warm_open"}`처럼 분기해서, 서먹했던 일을 몇 줄 언급하세요.
  - `<npc>_h<k>`: 그 NPC의 ♥k 이벤트를 봤으면 켜져요(예: `aula_h8`). 다른 NPC 이벤트를 봤는지에 따라 대사를 바꿀 때 `if_flag`로 쓰세요.

### 명령
| cmd | 필드 | 설명 |
|---|---|---|
| `line` | `who`, `face`(선택), `text` | 대사 |
| `narration` | `text` | 지문 |
| `choice` | `id`, `options`: [{`text`, `affinity`(30/15/0/-15/-30), `next`, `flag`(선택)}] | 선택지. `flag`를 넣으면 그 보기를 고를 때 플래그가 켜져요 |
| `goto` | `to` | 라벨로 이동 |
| `if_flag` | `flag`, `then`, `else` | 플래그로 분기 |
| `if_heart` | `min`, `then`, `else`, `npc`(선택: 다른 NPC 하트로 분기) | 하트 수로 분기 |
| `move` | `to`(장소), `transition`(`fade`/`cut`), `time`·`weather`(선택), `clear`(선택: true면 무대의 인물을 다 내보내요) | 장면 이동. 기본은 무대의 인물이 같이 이동해요 |
| `follow` | `who`, `to` | `who`가 앞장서서 화면 밖으로 나가고, 주인공이 따라가 새 장소에 함께 들어와요 |
| `show` / `hide` | `who`, `at`(위치) | 인물을 바로 세우거나 내보내요 |
| `walk` | `who`, `to`(위치) | 걸어서 이동. 무대에 없던 인물은 가까운 화면 밖에서 걸어 들어와요 |
| `emote` | `who`, `icon` | 머리 위 아이콘: heart, sweat, angry, music, question, exclaim, zzz, tear, sparkle |
| `camera` | `action` | shake, zoom_in, zoom_out, pan_left, pan_right, reset |
| `flash` | | 화면 번쩍(번개 등) |
| `sfx` | `id` | rain_heavy, rain, thunder, wind, door, bell, chime, splash, water, step, run, pop, sparkle, magic, explosion, scream, crow, fire, paper, glass_break, knock, heart, gulp, cat, owl, bird, goat, dragon, crowd, fireworks, clock, wing, bubble, sing, cough, creak |
| `bgm` | `id` | calm, sad, tense, happy, night, festival, mystery, warm, none |
| `wait` | `sec`(0~5) | 침묵 |
| `give_item` / `take_item` | `item`, `n` | 아이템 주기(주인공이 받음) / 가져가기 |
| `set_flag` | `flag` | 플래그 켜기 |
| `affinity` | `value` | 선택지 밖에서 호감도 바꾸기 |
| `fade_in` / `fade_out` | | 화면 전환 |

- 위치(`at`, `walk.to`): `far_left`, `left`, `center`, `right`, `far_right`, `off_left`, `off_right`
- 표정(`face`): neutral, happy, smile, laugh, sad, cry, angry, annoyed, surprised, shy, embarrassed, worried, tired, sleepy, serious, scared, proud, smug, thinking, determined, soft, pain
- 이벤트를 시작하면 무대에는 이벤트 주인 NPC(`center`)와 주인공(`left`)이 서 있어요. 처음에 `fade_in`을 넣으세요.
- 플래그 이름은 `<npc>_`로 시작해요(예: `nabi_fish_promise`). 분기 플래그 3 개 이상, 만든 플래그는 뒤 이벤트의 `if_flag`에서 꼭 쓰세요.

## 교차 장면 약속 (NPC끼리 맞물리는 곳)
- 배트리 ♥2: 짚신이 등장해 편지를 처음 받아 봐요(`who: "jipsin"`).
- 배트리 ♥8: 양호실에서 `sera`가 등장해 고마워해요.
- 아울라 ♥9: `batri`가 등장해 "주소가 '바람 부는 곳'인데요?"
- 맨디 ♥5: 호박밭에서 `jipsin`과 친해져요. 짚신 ♥10에는 맨디·할머니·아기 까마귀가 와요.
- 세라: `{npc.husband}`(`husband`)는 아울라에게 금서 책장을(`if_flag aula_h8`로 대사 변화), 맨디에게 뿌리 한 조각을, 캇파에게 달빛 이슬을 얻었어요. 세라 ♥5에 `aula`와 `husband`가 서고에서 속삭이는 장면이 있어요.
- 마들렌 ♥5: `stella`에게 점을 봐 달라고 해요. ♥6~7: `grandma`가 "그때 호박을 가져간 게 나였지." ♥9: 나비(호박 붕어 비늘 장식), 캇파(달빛 이슬), 맨디(박하 잎) 등에게 재료를 부탁해요. `{"cmd": "if_heart", "npc": "nabi", "min": 4, …}`로 그 NPC 하트가 낮으면 다른 재료로 대체해요.
- 스텔라 ♥7: 마들렌의 야식(선택). ♥9: `batri`와 함께 `sera`에게 달려가요.
- 나비 ♥9: `fish_owner`가 견습생 이야기를 들려줘요.
- 별자리 징조 떡밥: 스텔라 이야기에서 가장 많이 다루고, 다른 NPC는 전체 이벤트 중 1~2 번만 지나가는 말로 언급해요.
- 다른 NPC를 대사에서 언급할 때, 그 NPC의 성격·설정은 기획서 5 장을 참고하세요.

## 분량 세기
- `line`과 `narration` 하나가 1 줄이에요. 검증 스크립트는 **모든 경로**의 줄 수를 세서, 가장 짧은 경로와 가장 긴 경로가 모두 기준(90~120 줄, ♥5·♥8·♥10은 110~140 줄) 안에 들어와야 통과시켜요.
- 그래서 분기마다 길이를 비슷하게 맞추세요. 분기 하나는 보통 4~12 줄로 쓰고 바로 합류시키는 게 좋아요.
