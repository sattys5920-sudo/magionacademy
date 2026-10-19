# 메인 의뢰 검증: python3 scripts/validate_main.py [quest_id ...] [-v]
#   public/data/main/<quest_id>/quest.json · stage_N_request/complete.json · idle.json 을 읽어 규칙 위반을 출력해요 (0 건이면 통과)
#   형식은 tools/main_quest_format.md. 국어 규칙·줄 세기는 scripts/validate_npc.py 와 같아요
import json, os, re, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import validate_npc as V
ROOT = os.path.join(HERE, '..'); DATA = os.path.join(ROOT, 'public', 'data', 'main'); NDATA = os.path.join(ROOT, 'public', 'data', 'npc')
IDX = json.load(open(os.path.join(DATA, 'index.json'))); QUESTS = IDX['quests'] if isinstance(IDX, dict) else IDX
CAST = json.load(open(os.path.join(DATA, 'cast.json')))
PLACES = {p['id']: p for p in json.load(open(os.path.join(NDATA, 'places.json')))}
for p in json.load(open(os.path.join(DATA, 'places.json'))): PLACES[p['id']] = {**p, 'stand': True}
NCAST = json.load(open(os.path.join(NDATA, 'cast.json')))
OBJ = {'collect', 'craft', 'deliver', 'visit', 'talk', 'clue', 'puzzle', 'wait_moon', 'defend', 'choice'}
CMDS = V.CMDS | {'if_quest', 'if_item', 'input', 'rename'}
CUT = {'spawn', 'walk', 'face', 'cam', 'say', 'emote', 'crowd', 'fx', 'sfx', 'wait', 'fade', 'despawn', 'player', 'end'}
FX = {'bats', 'lightning', 'bell', 'wind', 'dark', 'light'}
FACTS = ['30 년', '오르솔라', '리나', '콩알', '방울', '초록 잉크', '쪽지', '견습생', '책장', '동생', '걷는 건 우리', '늙은 제빵사', '호박달 케이크', '할머니', '허수아비', '사냥꾼', '달 구경', '바람 소리', '별자리', '빈자리', '등불자리', '소맷자락']
ITEM_RE = re.compile(r"\b([a-z][a-z0-9_]*): *'([^']*)'")
def game_items():
    s = open(os.path.join(ROOT, 'public', 'index.html'), encoding='utf-8').read()
    i = s.find('const ITEM = {'); j = s.find('};', i)
    return set(m.group(1) for m in ITEM_RE.finditer(s[i:j])) | set(json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json'))).keys())
GAME_ITEMS = game_items()
NPCS = V.NPCS

def mq_items():
    out = {}
    for q in QUESTS:
        try: d = json.load(open(os.path.join(DATA, q, 'quest.json')))
        except Exception: continue
        out.update(d.get('items') or {})
    return out
ALL_ITEMS = mq_items()
ALL_CAST = {**NCAST, **CAST}
for q in QUESTS:
    try: ALL_CAST.update(json.load(open(os.path.join(DATA, q, 'quest.json'))).get('cast') or {})
    except Exception: pass
VAR_OK = set(NPCS) | set(ALL_CAST) | {'player', 'npc'}

def korean(where, t, errs, human):
    # validate_npc.korean 은 변수 이름을 서브 NPC로만 허용해요 → 메인 조연 변수는 여기서 미리 걸러요
    t2 = re.sub(r'\{(' + '|'.join(sorted(set(ALL_CAST) - set(NPCS), key=len, reverse=True)) + r')\.name(\|[^{}]*)?\}', lambda m: '{npc.name' + (m.group(2) or '') + '}', t)
    V.korean(where, t2, human, errs)

def count_paths(script, errs, where):
    lab, (lo, hi) = V.paths_info(script, errs, where); return lab, lo, hi

def check_script(where, sc, q, errs, flags_set, flags_used, hearts, uses):
    ids = set()
    for i, s in enumerate(sc):
        c = s.get('cmd')
        if not c and 'label' in s: continue
        if c not in CMDS: errs.append(f'{where}: 모르는 명령 「{c}」 (#{i})'); continue
        if c in ('line',):
            w = s.get('who')
            if w not in VAR_OK and w != 'voice': errs.append(f'{where}: 모르는 말하는 사람 「{w}」 (#{i})')
            if w and w != 'player' and w != 'voice': uses.add(w)
            if not s.get('text'): errs.append(f'{where}: 빈 대사 (#{i})')
        if c == 'narration' and not s.get('text'): errs.append(f'{where}: 빈 지문 (#{i})')
        if c in ('line', 'narration'):
            t = s.get('text', ''); human = s.get('who') in V.HUMAN or any(f'{{{h}.' in t for h in V.HUMAN)
            korean(f'{where} #{i}', t, errs, human)
            if len(t) > 90: errs.append(f'{where} #{i}: 한 줄이 너무 길어요 ({len(t)}자, 90자 이하)')
        if c == 'choice':
            for o in s.get('options', []):
                if not o.get('text'): errs.append(f'{where}: 빈 선택지 (#{i})')
                else: korean(f'{where} #{i} 선택', o['text'], errs, False)
                if 'affinity' in o: errs.append(f'{where}: 메인에는 호감도가 없어요 (#{i})')
                if o.get('flag'): flags_set.setdefault(o['flag'], []).append(where)
                if o.get('confirm'): korean(f'{where} #{i} 확인', o['confirm'], errs, False)
        if c == 'set_flag': flags_set.setdefault(s.get('flag'), []).append(where)
        if c == 'if_flag': flags_used.setdefault(s.get('flag'), []).append(where)
        if c == 'if_heart':
            if s.get('npc') not in NPCS: errs.append(f'{where}: if_heart 에는 서브 NPC id 「{s.get("npc")}」 (#{i})')
            if not s.get('else'): errs.append(f'{where}: if_heart 는 else(하트가 안 될 때 장면)가 꼭 있어야 해요 (#{i})')
            hearts.append((where, s.get('npc'), s.get('min'), s.get('then'), s.get('else')))
        if c == 'if_quest' and s.get('quest') not in QUESTS: errs.append(f'{where}: if_quest 모르는 의뢰 「{s.get("quest")}」')
        if c in ('move', 'follow') and s.get('to') not in PLACES: errs.append(f'{where}: 모르는 장소 「{s.get("to")}」 (#{i})')
        if c in ('give_item', 'take_item') and s.get('item') not in GAME_ITEMS and s.get('item') not in ALL_ITEMS: errs.append(f'{where}: 모르는 아이템 「{s.get("item")}」 (#{i})')
        if c == 'sfx' and s.get('id') not in V.SFX: errs.append(f'{where}: 모르는 효과음 「{s.get("id")}」 (#{i})')
        if c == 'camera' and s.get('action') not in V.CAMERA: errs.append(f'{where}: 모르는 카메라 「{s.get("action")}」 (#{i})')
        if c in ('show', 'walk', 'hide', 'emote') and s.get('who') not in VAR_OK: errs.append(f'{where}: 모르는 배우 「{s.get("who")}」 (#{i})')
        if c == 'input' and not s.get('key'): errs.append(f'{where}: input 에 key 가 없어요')
        if c == 'rename' and s.get('who') not in CAST: errs.append(f'{where}: rename 대상 「{s.get("who")}」')
    return ids

def check_arrival(where, arr, errs):
    if not arr: errs.append(f'{where}: 1 단계 부탁 장면엔 등장 컷신 arrival 이 있어야 해요'); return
    kinds = [c.get('cmd') for c in arr]
    for i, c in enumerate(arr):
        k = c.get('cmd')
        if k not in CUT: errs.append(f'{where} arrival: 모르는 컷신 명령 「{k}」 (#{i})')
        if k == 'fx' and c.get('kind') not in FX: errs.append(f'{where} arrival: 모르는 효과 「{c.get("kind")}」')
        if k == 'sfx' and c.get('id') not in V.SFX: errs.append(f'{where} arrival: 모르는 효과음 「{c.get("id")}」')
        if k == 'say': korean(f'{where} arrival #{i}', c.get('text', ''), errs, False)
        if k == 'crowd' and c.get('react') not in ('scream', 'flee', 'watch'): errs.append(f'{where} arrival: crowd.react')
    if 'spawn' not in kinds: errs.append(f'{where} arrival: 의뢰인이 나타나는 spawn 이 없어요')
    if 'walk' not in kinds: errs.append(f'{where} arrival: 걸어가는 walk 가 없어요')
    if 'crowd' not in kinds: errs.append(f'{where} arrival: 학생·마을 사람 반응 crowd 가 없어요')

def check_quest(qid, verbose=False):
    errs, warns = [], []; d = os.path.join(DATA, qid)
    try: q = json.load(open(os.path.join(d, 'quest.json')))
    except Exception as e: print(f'[{qid}] quest.json 읽기 실패: {e}'); return 1, None
    w = qid
    if q.get('id') != qid: errs.append(f'{w}: id 가 폴더 이름과 달라요')
    if q.get('order') != QUESTS.index(qid) + 1: errs.append(f'{w}: order 는 {QUESTS.index(qid) + 1}')
    if q.get('client') not in CAST: errs.append(f'{w}: client 「{q.get("client")}」 는 cast.json 에 있어야 해요')
    if not q.get('name'): errs.append(f'{w}: name 없음')
    u = q.get('unlock') or {}
    if q.get('order', 0) > 1 and u.get('afterQuest') != QUESTS[q['order'] - 2]: errs.append(f'{w}: unlock.afterQuest 는 {QUESTS[q["order"] - 2]}')
    if 2 <= q.get('order', 0) <= 6 and u.get('daysAfter') != 3: errs.append(f'{w}: unlock.daysAfter 는 3')
    if q.get('order') == 7 and not u.get('afterFestival'): errs.append(f'{w}: 잭 의뢰는 unlock.afterFestival = true')
    for pl in [q.get('place'), (q.get('arrival') or {}).get('player'), (q.get('after') or {}).get('place')]:
        if pl and pl not in PLACES: errs.append(f'{w}: 모르는 장소 「{pl}」')
    items = {**ALL_ITEMS, **(q.get('items') or {})}
    recipes = {r['id']: r for r in q.get('recipes') or []}
    for rid, r in recipes.items():
        if rid not in items and rid not in GAME_ITEMS: errs.append(f'{w}: 레시피 「{rid}」 가 items 에 없어요')
        for m in (r.get('mats') or {}):
            if m not in items and m not in GAME_ITEMS: errs.append(f'{w}: 레시피 재료 「{m}」 모르는 아이템')
        if r.get('steps', 1) not in (1, 2, 3): errs.append(f'{w}: 레시피 steps 는 1~3')
        if r.get('place', 'lab') not in ('lab', 'candy'): errs.append(f'{w}: 레시피 place 는 lab/candy')
    stages = q.get('stages') or []
    if [s.get('n') for s in stages] != [1, 2, 3, 4, 5]: errs.append(f'{w}: stages 는 n 1~5 다섯 개')
    types_used = set(); flags_set, flags_used, hearts, uses = {}, {}, [], set()
    rows = []
    for st in stages:
        n = st.get('n'); ws = f'{w} {n}단계'
        if not st.get('title'): errs.append(f'{ws}: title 없음')
        if st.get('place') and st['place'] not in PLACES: errs.append(f'{ws}: 모르는 장소 「{st["place"]}」')
        for a in st.get('actors') or []:
            if a.get('id') not in ALL_CAST: errs.append(f'{ws}: 모르는 조연 「{a.get("id")}」')
            if a.get('place') not in PLACES: errs.append(f'{ws}: 조연 자리 모르는 장소 「{a.get("place")}」')
            for l in a.get('lines') or []: korean(f'{ws} 조연 {a.get("id")}', l, errs, False)
        objs = st.get('objectives') or []
        if not 1 <= len(objs) <= 3: errs.append(f'{ws}: 목표는 1~3 개 ({len(objs)})')
        for o in objs:
            t = o.get('type'); types_used.add(t)
            if t not in OBJ: errs.append(f'{ws}: 모르는 목표 종류 「{t}」'); continue
            if t in ('collect', 'craft', 'deliver'):
                it = o.get('item')
                if it not in items and it not in GAME_ITEMS: errs.append(f'{ws}: 모르는 아이템 「{it}」')
                if t == 'collect' and it not in GAME_ITEMS and not o.get('source'): errs.append(f'{ws}: 새 아이템 「{it}」 은 source(어디서 얻는지)가 있어야 해요')
                if t == 'collect' and o.get('source') and o['source'].get('place') not in PLACES: errs.append(f'{ws}: source.place')
                if t == 'craft' and it not in recipes: errs.append(f'{ws}: craft 「{it}」 레시피가 quest.json recipes 에 없어요')
                if t == 'craft' and o.get('quality') not in (None, 'normal', 'good', 'best'): errs.append(f'{ws}: quality')
                if t == 'deliver' and o.get('to') not in ALL_CAST and o.get('to') not in NPCS: errs.append(f'{ws}: deliver.to 「{o.get("to")}」')
            if t == 'visit':
                if o.get('place') not in PLACES: errs.append(f'{ws}: visit 모르는 장소 「{o.get("place")}」')
                for x in o.get('time') or []:
                    if x not in V.TIMES: errs.append(f'{ws}: visit.time 「{x}」')
                for x in o.get('weather') or []:
                    if x not in V.WEATHER: errs.append(f'{ws}: visit.weather 「{x}」')
            if t == 'talk':
                who = o.get('who')
                if who not in NPCS and who not in ALL_CAST: errs.append(f'{ws}: talk.who 「{who}」')
                if who in ALL_CAST and who not in NPCS and who != q.get('client') and not any(a.get('id') == who for a in st.get('actors') or []): errs.append(f'{ws}: talk 상대 조연 「{who}」 가 이 단계 actors 에 없어요')
                if o.get('line'): korean(f'{ws} talk', o['line'], errs, who in V.HUMAN)
            if t == 'clue':
                sps = o.get('spots') or []
                if not sps: errs.append(f'{ws}: clue 에 spots 가 없어요')
                if (o.get('count') or len(sps)) > len(sps): errs.append(f'{ws}: clue count 가 spots 보다 많아요')
                for sp in sps:
                    if sp.get('place') not in PLACES: errs.append(f'{ws}: 조사 지점 모르는 장소 「{sp.get("place")}」')
                    if not sp.get('text'): errs.append(f'{ws}: 조사 지점 「{sp.get("id")}」 설명이 없어요')
                    else: korean(f'{ws} 단서 {sp.get("id")}', sp['text'], errs, False)
            if t == 'puzzle':
                if o.get('kind') not in ('stars', 'order'): errs.append(f'{ws}: puzzle.kind')
                if o.get('kind') == 'order' and len(o.get('items') or []) != len(o.get('answer') or []): errs.append(f'{ws}: order 퍼즐 items/answer 길이')
                for k in ('hintText', 'doneText', 'title', 'sub'):
                    if o.get(k): korean(f'{ws} 퍼즐', o[k], errs, False)
            if t == 'wait_moon' and o.get('moon') not in ('full', 'new'): errs.append(f'{ws}: wait_moon.moon 은 full/new')
            if t == 'defend' and o.get('place') and o['place'] not in PLACES: errs.append(f'{ws}: defend.place')
            if t == 'choice':
                if n != 5: errs.append(f'{ws}: choice 목표는 5 단계에만')
                if len(o.get('flags') or []) != 2: errs.append(f'{ws}: choice.flags 는 결말 플래그 2 개')
                for f in o.get('flags') or []: flags_used.setdefault(f, []).append(ws)
        if n == 5 and not any(o.get('type') == 'choice' for o in objs): errs.append(f'{ws}: 5 단계엔 결말 choice 목표가 있어야 해요')
        for it in [].concat if False else ((st.get('rewards') or {}).get('items') or []):
            k = it if isinstance(it, str) else it.get('id')
            if k not in items and k not in GAME_ITEMS: errs.append(f'{ws}: 보상 아이템 「{k}」')
        # 장면
        for kind in ('request', 'complete'):
            fn = os.path.join(d, f'stage_{n}_{kind}.json'); wk = f'{ws} {"부탁" if kind == "request" else "완료"}'
            try: sc = json.load(open(fn))
            except Exception as e: errs.append(f'{wk}: 파일 읽기 실패 {e}'); rows.append((n, kind, '-', 0, 0)); continue
            if not sc.get('title'): errs.append(f'{wk}: 제목 없음')
            loc = (sc.get('scene') or {}).get('location')
            if loc and loc not in PLACES: errs.append(f'{wk}: scene.location 「{loc}」')
            script = sc.get('script') or []
            check_script(wk, script, q, errs, flags_set, flags_used, hearts, uses)
            lab, lo, hi = count_paths(script, errs, wk)
            big = (n == 1 and kind == 'request') or (n == 5 and kind == 'complete')
            a, b = (110, 140) if big else (90, 120)
            if not a <= hi <= b: errs.append(f'{wk}: 한 경로 대사 {hi} 줄 (가장 긴 경로, {a}~{b} 줄이어야 해요)')
            if lo < a * .7: warns.append(f'{wk}: 가장 짧은 경로가 {lo} 줄이라 너무 짧아요')
            if n >= 2 and kind == 'request' and not any(s.get('cmd') in ('move', 'follow') for s in script): errs.append(f'{wk}: 2~5 단계 부탁 장면엔 장면 이동(move/follow)이 1 번 이상')
            if kind == 'request' and n == 1: check_arrival(wk, sc.get('arrival'), errs)
            if kind == 'request' and n == 5:
                ch = [o for s in script if s.get('cmd') == 'choice' for o in s.get('options', []) if o.get('flag') in (q.get('ending_flags') or [])]
                if len(ch) < 2: errs.append(f'{wk}: 5 단계 부탁 장면에 결말 플래그({q.get("ending_flags")})를 세우는 선택이 있어야 해요')
                if any(not o.get('confirm') for o in ch): errs.append(f'{wk}: 결말 선택지에는 confirm(확인 창 글)이 있어야 해요')
            rows.append((n, kind, sc.get('title'), lo, hi))
    # 반복 대사
    try: idle = json.load(open(os.path.join(d, 'idle.json')))
    except Exception as e: errs.append(f'{w}: idle.json 읽기 실패 {e}'); idle = {}
    for n in range(1, 6):
        for k, nm in (('a', '진행 중'), ('b', '보고 전'), ('c', '다음 단계 전')):
            ls = (idle.get(str(n)) or {}).get(k)
            if not ls or not 1 <= len(ls) <= 2: errs.append(f'{w}: 반복 대사 {n}단계 ({nm}) 는 1~2 줄')
            for l in ls or []: korean(f'{w} 반복 {n}{k}', l, errs, False)
    if not idle.get('done') or not 1 <= len(idle['done']) <= 2: errs.append(f'{w}: 반복 대사 done(완료 후) 1~2 줄')
    for l in idle.get('done') or []: korean(f'{w} 반복 done', l, errs, False)
    # 결말 플래그
    ef = q.get('ending_flags') or []
    if len(ef) != 2: errs.append(f'{w}: ending_flags 는 2 개')
    for f in ef:
        if f not in flags_set: errs.append(f'{w}: 결말 플래그 「{f}」 를 세우는 선택지가 없어요')
    for f in flags_set:
        if not f: errs.append(f'{w}: 이름 없는 플래그')
    # 서브 NPC 고정 사실 문맥 (사람이 읽어요)
    facts = []
    for st in stages:
        for kind in ('request', 'complete'):
            try: sc = json.load(open(os.path.join(d, f'stage_{st["n"]}_{kind}.json')))
            except Exception: continue
            for s in sc.get('script') or []:
                t = s.get('text') or ''
                for f in FACTS:
                    if f in t: facts.append((f'{st["n"]}단계 {kind}', s.get('who', ''), t))
    for e in errs: print('  ✗', e)
    for e in warns: print('  ⚠', e)
    print(f'[{qid}] 위반 {len(errs)} 건 · 목표 종류 {len(types_used)} 가지 {sorted(types_used)} · 서브 NPC 하트 분기 {len(hearts)} 곳')
    if verbose:
        for n, kind, t, lo, hi in rows: print(f'  {n}단계 {"부탁" if kind == "request" else "완료"}  {t}  {lo}~{hi} 줄')
        print('  플래그 세움:', ', '.join(sorted(k for k in flags_set if k)), '| 씀:', ', '.join(sorted(k for k in flags_used if k)))
        for h in hearts: print('  하트 분기:', h)
        if facts:
            print('  고정 사실 문맥:')
            for a, b, t in facts: print(f'    {a} [{b}] {t[:70]}')
    return len(errs), dict(types=types_used, flags_set=flags_set, flags_used=flags_used, rows=rows)

def finale_sim(results):
    """결말 플래그 조합(의뢰별 2 갈래)으로 모든 장면을 끝까지 돌려 봐요: 라벨 없는 점프·고리가 없는지"""
    combos = 0; bad = 0
    flags = []
    for qid in QUESTS:
        try: q = json.load(open(os.path.join(DATA, qid, 'quest.json')))
        except Exception: continue
        if q.get('ending_flags'): flags.append(q['ending_flags'])
    for pick in itertools.product(*flags):
        on = set(pick); combos += 1
        for mode in ('h0', 'h10'):
            for qid in QUESTS:
                d = os.path.join(DATA, qid)
                for n in range(1, 6):
                    for kind in ('request', 'complete'):
                        try: sc = json.load(open(os.path.join(d, f'stage_{n}_{kind}.json')))
                        except Exception: continue
                        script = sc.get('script') or []; lab = {s['label']: i for i, s in enumerate(script) if 'label' in s}
                        i = 0; guard = 0; seen_choice = 0
                        while i < len(script) and guard < 3000:
                            guard += 1; s = script[i]; i += 1; c = s.get('cmd')
                            if c == 'choice':
                                opts = s.get('options') or []; o = next((o for o in opts if o.get('flag') in on), opts[0] if opts else None)
                                if o and o.get('flag'): on.add(o['flag'])
                                if o and o.get('next') in lab: i = lab[o['next']]
                            elif c == 'goto': i = lab.get(s.get('to'), i)
                            elif c == 'if_flag': t = s.get('then') if s.get('flag') in on else s.get('else'); i = lab.get(t, i)
                            elif c == 'if_heart': t = s.get('then') if mode == 'h10' else s.get('else'); i = lab.get(t, i)
                            elif c == 'if_quest': t = s.get('then'); i = lab.get(t, i)
                            elif c == 'if_item': t = s.get('else'); i = lab.get(t, i)
                            elif c == 'set_flag': on.add(s.get('flag'))
                        if guard >= 3000: print(f'  ✗ {qid} {n}단계 {kind}: 결말 조합 {pick} 에서 끝나지 않아요'); bad += 1
    print(f'결말 조합 {combos} 가지 × 하트 0/10 자동 진행: 막힘 {bad} 건')
    return bad

def main(ids):
    v = '-v' in sys.argv; total = 0; res = {}
    for qid in ids:
        n, r = check_quest(qid, v); total += n; res[qid] = r
    # 뒤 의뢰일수록 목표 종류가 늘어나는지
    prev = 0
    for qid in QUESTS:
        r = res.get(qid)
        if not r: continue
        k = len(r['types'])
        if k < prev: print(f'  ⚠ {qid}: 목표 종류 {k} 가지 (앞 의뢰 {prev} 가지보다 적어요)')
        prev = max(prev, k)
    print('의뢰별 목표 종류:', {q: sorted(r['types']) for q, r in res.items() if r})
    # 플래그: 세운 건 쓰이고, 쓰는 건 세워지는지 (검사한 의뢰 범위 + 다른 의뢰 파일)
    all_set, all_used = {}, {}
    for q, r in res.items():
        if not r: continue
        for f, w in r['flags_set'].items(): all_set.setdefault(f, []).extend(w)
        for f, w in r['flags_used'].items(): all_used.setdefault(f, []).extend(w)
    for qid in QUESTS:
        if qid in res: continue
        d = os.path.join(DATA, qid)
        for n in range(1, 6):
            for kind in ('request', 'complete'):
                try: sc = json.load(open(os.path.join(d, f'stage_{n}_{kind}.json')))
                except Exception: continue
                for s in sc.get('script') or []:
                    if s.get('cmd') == 'if_flag': all_used.setdefault(s.get('flag'), []).append(qid)
                    if s.get('cmd') == 'set_flag': all_set.setdefault(s.get('flag'), []).append(qid)
                    if s.get('cmd') == 'choice':
                        for o in s.get('options') or []:
                            if o.get('flag'): all_set.setdefault(o['flag'], []).append(qid)
    for f, w in all_set.items():
        if f and f not in all_used and not V.AUTO.fullmatch(f or ''): print(f'  ⚠ 플래그 「{f}」 를 세웠는데 쓰는 곳이 없어요 ({w[0]})')
    for f, w in all_used.items():
        if f and f not in all_set and not V.AUTO.fullmatch(f or '') and not f.startswith(tuple(n + '_' for n in NPCS)): print(f'  ✗ 플래그 「{f}」 를 쓰는데 세우는 곳이 없어요 ({w[0]})'); total += 1
    total += finale_sim(res)
    print(f'\n총 위반 {total} 건')
    return total

if __name__ == '__main__':
    ids = [a for a in sys.argv[1:] if not a.startswith('-')] or QUESTS
    sys.exit(1 if main(ids) else 0)
