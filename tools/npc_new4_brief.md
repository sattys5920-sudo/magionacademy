# 새 NPC 넷 (바우 · 카엘 · 아르투아 · 그레고) 하트 이야기 작성 지시서

## 꼭 먼저 읽을 것
- `tools/npc_story_format.md` : 실제 엔진 형식 (명령, 장소, 표정, 효과음, 분량, 검사) — 이 문서를 그대로 따라요
- `tools/npc_story_spec.md` 4 장 : 국어 규칙과 글쓰기 원칙
- 분위기와 분량 견본: `public/data/npc/leo/events/heart_02.json`, `heart_05.json`, `public/data/npc/stella/events/heart_01.json`, `heart_05.json`, `heart_10.json`, `public/data/npc/leo/profile.json`
- 다른 NPC 성격은 `tools/npc_story_spec.md` 5 장과 각 `profile.json`의 tone

## 만들 파일
- `public/data/npc/<id>/profile.json` (형식 문서의 profile 절 그대로: tone A~D, daily 단계마다 12 줄 이상, ambient, gift, recall 5 키 이상, cast)
- `public/data/npc/<id>/events/heart_01.json` ~ `heart_10.json`
- 저장 모양은 `python3 tools/npc_fmt.py` 가 만드는 모양(한 줄에 명령 하나). 사용법은 파일 머리 주석을 보세요.

## 검사 (모두 통과할 때까지)
- `python3 scripts/validate_npc.py <id>` → 위반 0 건. 경고(⚠)도 읽고 진짜면 고쳐요.
- `python3 tools/story_check.py` → 내 파일에 관한 문제 0 개
- 분량: 기존 NPC와 같아요. 경로마다 90~120 줄, ♥5 · ♥8 · ♥10은 110~140 줄. 장면 이동(move/follow) 최소 1 번.

## 사용자 요청 (가장 중요)
- **숫자에 집착하지 마세요.** 「세 번이나」, 「열두 번 연습했어」, 「이백십삼 계단」처럼 횟수 · 개수를 세서 강조하거나 웃기는 대사를 쓰지 마세요. 숫자는 꼭 필요할 때만, 지나가듯이.
- **최대한 자연스럽게.** 사람이 실제로 할 법한 말. 설명조 · 연설조 금지. 감정은 행동과 침묵으로.
- 말줄임표: 말 중간 `....` (점 4), 말 끝 `.......` (점 7). `?!`, `!!` 금지. 이모지 금지.
- 사람 NPC 이름은 변수: `{kael.name}`, `{artua.name}`, `{grego.name}`, `{stella.name}`, `{leo.name}`, `{sera.name}`, `{madeleine.name}`, 이벤트 주인은 `{npc.name}`. 조사는 `{npc.name|이/가}` 함수로. 바우 · 나비 · 배트리 · 아울라 같은 동물 NPC 이름은 그대로 써요.
- 주인공(`player`)의 성별을 단정하지 마세요.

## 등장인물 id
- 새 NPC: `bau`(바우, 강아지), `kael`, `artua`, `grego` — `public/data/npc/cast.json` 에 이미 있어요. cast.json 은 고치지 마세요.
- 이야기에만 나오는 조연은 자기 `profile.json` 의 `"cast"` 에 추가해요 (형식 문서 참고).
- 다른 NPC 파일은 고치지 마세요 (아르투아 담당만 예외: 아래 참고).

## 평소 자리 (루틴) — 하트 이벤트 location 은 「서 있음」 장소에서 골라요
| NPC | 아침 | 낮 | 저녁 | 밤 |
|---|---|---|---|---|
| bau | main_hall (학교 정문 앞) | main_hall | main_hall | menagerie (사육장 처마 밑 낡은 상자) |
| kael | library_stacks (책 펴 놓고 졸아요) | library_stacks | main_hall | main_hall (등불 들고 순찰, 본관 복도는 hall_corridor 로 이동) |
| artua | dorm_street (묵는 숙소) | library_stacks | village_square | hill_ruin (언덕, 관측은 hill_top · clock_tower 로 이동) |
| grego | old_windmill (낡은 풍차 옆 창고가 그레고의 집 겸 작업장) | old_windmill | village_square (광장 벤치) | old_windmill |

## 교차 장면 약속 (서로 맞춰요. 상대 이벤트를 봤는지는 `<id>_hN` 플래그로, 봤을 때 · 안 봤을 때 양쪽 대사를 모두 넣어요)
- 바우 ♥5: 양호실에서 `sera` 가 다리를 치료해 줘요.
- 바우 ♥7: `leo` 가 몰래 밥과 담요를 놓아 주고 있었어요.
- 바우 ♥10: 그레고가 만든 개집이 있어요 (`grego_h9` 있으면 그레고가 만든 집, 없으면 학생과 바우가 같이 꾸민 상자 집).
- 카엘 ♥7: 폭풍 치는 밤(조건 rain, 연출 storm) 겁먹고 숨은 `bau` 를 같이 찾아요.
- 카엘 ♥8 · 그레고 ♥7: 밤에 그레고 창고에서 둘이 차를 마셔요. 그레고는 카엘이 학생일 때부터 알았어요.
- 그레고 ♥2: `madeleine` 이 과자를 두고 가며 잔소리. ♥4: `nabi` 가 창고 지붕 단골. ♥9: 바우에게 비 안 새는 개집을 만들어 줘요.
- 아르투아: `stella` 가 자주 나와요. 스텔라의 성격 · 말투는 `public/data/npc/stella/profile.json` tone 과 하트 이야기를 꼭 읽고 맞춰요 (길치, 신비로운 예언체 존댓말이 자꾸 깨짐, 높은 데 무서워함). 스텔라 이야기의 큰 사건(동생, 시계탑, 축제 밤 부상)은 건드리지 말고 언급하지도 마세요.

## 보상
- coin · mana · know 는 기존 NPC 와 비슷하게 (♥1 30 전후 ~ ♥10 200).
- items 는 `tools/npc_items.json` 에 있는 id 만. ♥10 의 방 가구 보상은 나중에 따로 넣어요 (지금은 비워 둬요).
- perk 는 ♥10 만, 형식 문서의 목록에서 어울리는 것 하나 또는 null.
