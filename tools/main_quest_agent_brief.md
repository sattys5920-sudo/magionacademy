# 메인 의뢰 작가 공통 안내 (내부용)

You are one of seven writers for the main story 「일곱 등불의 의뢰」 of 호박달 마녀학교 (Korean browser game, repo /home/user/magionacademy). You write ONE quest: all its data files under `public/data/main/<quest_id>/`. Another writer does each of the other quests in parallel, so touch nothing outside your folder (exceptions below).

Read first, in this order:
1. `tools/main_quest_format.md` — the data format, the engine's commands, the lore adjustments (설정 조정) and the testing recipe. Follow it exactly.
2. `tools/main_quest_spec.md` — the user's design. Your quest's section 3-N is your story skeleton; also read 1 (lore), 2 (system), 4 (sub-NPC rules), 6 (Korean rules), and the other clients' sections so you can write cameo lines in their voice.
3. `tools/npc_story_format.md` — commands, places table, Korean rules (the main validator applies the same rules).
4. The sub-NPC scripts you connect to: `public/data/npc/<npc>/events/heart_NN.json` and `profile.json` (tone by heart stage `daily.A~D`). Quote their facts, never contradict them.
5. The skeleton `public/data/main/main_01_dracula/` (a working but placeholder example of every file; the dracula writer replaces it).

## Shared names (all writers use these — do not invent others)
- Clients: `blady` 블라디 · `yeoreum` 유령→여름 · `beatrix` 베아트릭스 · `ur` 우르 · `somi` 솜이 · `nefer` 네페르 · `piece` 조각→(player names, default 프랭) · `jack` 잭. Common cast in `public/data/main/cast.json`: `principal` 교장 선생님, `countess` 백작 부인, `hunter` 사냥꾼, `alchemist` 연금술 선생님(일지 속). Sub-NPC cast in `public/data/npc/cast.json` (`fish_owner`, `grandma`, `orsola`, `elder_a`, `elder_b`, `merchant`, `kids` …). Need more? add to your quest.json `"cast"`.
- Ending flags (5 단계 choice, exactly these):
  - main_01 `blady_spoke_himself` / `player_spoke_for_blady`
  - main_02 `yeoreum_named_by_player` / `yeoreum_remembered`
  - main_03 `beatrix_apologized_herself` / `player_explained_to_nabi`
  - main_04 `player_defended_ur` / `somi_spoke_for_ur` (plus 3 단계 설득 결과 `ur_town_wait` 하루 더 지켜보기 / `ur_town_hunt` 사냥꾼 부르기, set with `set_flag` after the talk choices)
  - main_05 `nefer_page_public` / `nefer_page_to_player`
  - main_06 `piece_flame_now` (A) / `piece_flame_later` (B)
  - main_07 `jack_go` / `jack_stay`
  Later quests branch on earlier flags with `if_flag` (both branches must exist; if the player somehow has neither, `else` must still read naturally).
- Shared items: `lantern_shard` 등불 조각 (defined in main_01; other quests just put `"lantern_shard"` in `completion_reward.items`), `pact_copy` 서약문 사본 (main_05 defines, `key: true`), `jack_ember` 조각의 불씨 (main_06 defines, `key: true`, given only on path B).
- Trust flags you may set freely: prefix with your client id (`blady_…`, `yeoreum_…`). Unused flags only produce warnings, but every `if_flag` must have a setter somewhere.

## Rules
- Volume per the spec: 부탁 90~120 / 완료 90~120 lines on the longest path (1 단계 부탁, 5 단계 완료: 110~140). Only `line` and `narration` count. Write real scenes: concrete sensory detail, humor between heavy beats, choices with warm/playful/awkward player options, no preaching. Each client's voice must be unmistakable.
- Korean: 해요체 UI; dialogue in each character's voice. Numbers with a space before units (`3 일`, `300 년`), ellipsis `……`, no `...`/`?!`/`!!`. Human sub-NPCs by variable (`{sera.name}`, `{madeleine.name}`, `{stella.name}`, `{leo.name}`) with josa helpers `{player|이/가}`; clients by variable too (`{blady.name}`, `{yeoreum.name|이/가}`, `{piece.name}`). No gendered words for human NPCs.
- Sub-NPC cameos: follow the tone of their heart stage; every `if_heart` has an `else`. Objectives must never be blocked by hearts (alternatives via `source` items or `else` branches).
- Objectives: use the required types from your spec table; 1~3 per stage; make hints concrete (`hint_location`, `source`, `where`). Place coordinates come from `public/data/npc/places.json` and `public/data/main/places.json`.
- Do NOT edit: `public/index.html`, `public/world.js`, `tools/iso/*`, `public/data/npc/*`, `public/data/main/index.json`, `cast.json`, `places.json`, `npc_lines.json`, other quests' folders. If you need a new place or a shared cast change, put it in your report (and use the nearest existing place meanwhile).
- Do NOT run git commit/push; the coordinator commits.

## Verify before you finish
1. `python3 scripts/validate_main.py <quest_id> -v` → 위반 0 건 (warnings are OK if you judge them false positives; say so).
2. Play it in the mock (see format doc §쓰는 법·시험): `bash tools/ui_mock.sh /home/user/magionacademy <your port>` then Playwright (`require('/opt/node-tools/node_modules/playwright')`, `chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })`, seed as in the format doc: `page.addInitScript(() => { window.__seed = { players: { me1: { nick: '민준', look: 2, house: 'dew', coin: 1200, mana: 30, day: 4, know: 55, inv: {}, cr: [], npc: {}, story: { seen: { '1in': 1 } } } } }; window.__uid = 'me1'; })`, goto `http://localhost:<port>/`, wait ~4.5 s, click `#stnext` while it exists). Run at least: the arrival cutscene (`__mq.set('<qid>',1,'arrive'); __mq.tick()` — wait ~12 s, screenshot), stage 1 request scene to the end, one complete scene, the stage 5 request choice with its confirm box, and any puzzle/defend/craft you use (open with `__T.openSheet('home','journal')` → 이야기 tab buttons, or `__T.openSheet('home','mqpuzzle')` after setting `window`-less state via journal). No `pageerror`. Save 4~8 screenshots to `audit/main/<quest_id>/`. Re-run `tools/ui_mock.sh` after every data change (it copies `public/`).
3. Final report (Korean): 장면 제목과 줄 수 표(검증 출력), 선택지·플래그, 서브 NPC 연결(하트 조건과 대체), 새 조연·아이템·레시피·장소, `npc_lines.json`에 넣을 서브 NPC 평소 대사 추가분(NPC id, 조건 quest/flag, 줄), 다른 의뢰 작가에게 알릴 것, 스크린숏 경로, 검증·실행 결과.
