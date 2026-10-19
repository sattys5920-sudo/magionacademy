# NPC 호감도 스토리 검증: python3 scripts/validate_npc.py [npc_id ...]
#   public/data/npc/<id>/profile.json, events/heart_01~10.json 을 읽어서 규칙 위반을 출력해요 (0 건이면 통과)
#   형식은 tools/npc_story_format.md
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import josa
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA = os.path.join(ROOT, 'public', 'data', 'npc')
NPCS = ['nabi', 'batri', 'kappa', 'aula', 'mandi', 'jipsin', 'sera', 'madeleine', 'stella', 'leo']
HUMAN = ['sera', 'madeleine', 'stella', 'leo']
BIG = (5, 8, 10)
PLACES = {p['id']: p for p in json.load(open(os.path.join(DATA, 'places.json')))}
CAST = json.load(open(os.path.join(DATA, 'cast.json')))
ITEMS = json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json')))
TIMES = {'morning', 'day', 'evening', 'night'}
WEATHER = {'clear', 'rain', 'fog', 'snow'}
FACES = {'neutral', 'happy', 'smile', 'laugh', 'sad', 'cry', 'angry', 'annoyed', 'surprised', 'shy', 'embarrassed', 'worried',
         'tired', 'sleepy', 'serious', 'scared', 'proud', 'smug', 'thinking', 'determined', 'soft', 'pain'}
EMOTES = {'heart', 'sweat', 'angry', 'music', 'question', 'exclaim', 'zzz', 'tear', 'sparkle'}
POS = {'far_left', 'left', 'center', 'right', 'far_right', 'off_left', 'off_right'}
SFX = {'rain_heavy', 'rain', 'thunder', 'wind', 'door', 'bell', 'chime', 'splash', 'water', 'step', 'run', 'pop', 'sparkle', 'magic',
       'explosion', 'scream', 'crow', 'fire', 'paper', 'glass_break', 'knock', 'heart', 'gulp', 'cat', 'owl', 'bird', 'goat', 'dragon',
       'crowd', 'fireworks', 'clock', 'wing', 'bubble', 'sing', 'cough', 'creak'}
BGM = {'calm', 'sad', 'tense', 'happy', 'night', 'festival', 'mystery', 'warm', 'none'}
CAMERA = {'shake', 'zoom_in', 'zoom_out', 'pan_left', 'pan_right', 'reset'}
AFF = {30, 15, 0, -15, -30}
CMDS = {'line', 'narration', 'choice', 'goto', 'if_flag', 'if_heart', 'move', 'walk', 'follow', 'show', 'hide', 'emote', 'camera',
        'sfx', 'bgm', 'wait', 'give_item', 'take_item', 'set_flag', 'affinity', 'fade_in', 'fade_out', 'flash'}
UNIT = re.compile(r'\d+(일|번|째|개|마리|년|명|시|분|초|장|권|살|층|그릇|걸음|골드|주년|군데|송이|잔|병|통|칸|줄|쪽|달|주)')
WRONG = ['몇 일', '몇일', '금새', '왠일', '웬지', '어떻해', '할께', '설레임', '바램', '일부로', '오랫만', '구지', '역활', '희안',
         '되요', '돼서는 안 되', '안돼', '됬', '될께', '갈께', '줄께', '볼께', '먹을께', '할려고', '되가', '돼었', '않되', '않돼']
GENDER = re.compile(r'(?<![가-힣])(그녀|그는|그가|그를|그의|아저씨|아줌마|언니|오빠|누나|형)(?=$|[^가-힣]|[은는이가을를의도한께에님아야])')
NAMES = ['세라', '루카스', '마들렌', '스텔라', '레오']
AUTO = re.compile(r'[a-z]+_(h\d+|was_cold)')
PERKS = {'cat_furniture', 'bait', 'free_post', 'rod_bonus', 'lord_hint', 'potion_hint', 'know_bonus', 'greenhouse_growth', 'pumpkin_race', 'scarecrow_hat', 'tasty_potion', 'cake_recipe', 'fortune', 'rare_egg'}
VAR = re.compile(r'\{([a-z_]+)(?:\.([a-z_]+))?(?:\|([^{}]*))?\}')

def texts_of(o):
    if isinstance(o, str): yield o
    elif isinstance(o, list):
        for v in o: yield from texts_of(v)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('text', 'title', 'name') or isinstance(v, (list, dict)): yield from texts_of(v)

def korean(where, t, human_ctx, errs):
    for m in UNIT.finditer(t): errs.append(f'{where}: 숫자와 단위를 띄어 쓰세요 「{m.group(0)}」 → {t[:40]}')
    for run in re.findall(r'…+', t):
        if len(run) != 2: errs.append(f'{where}: 말줄임표는 「……」(2 글자)로 → {t[:40]}')
    for bad in ('...', '?!', '!?', '!!', '??', '~~'):
        if bad in t: errs.append(f'{where}: 「{bad}」 금지 → {t[:40]}')
    if '..' in t and '...' not in t: errs.append(f'{where}: 마침표 겹침 → {t[:40]}')
    for w in WRONG:
        if (re.search(r'(?<![가-힣])' + w, t) if w in ('구지', '바램', '되요') else w in t): errs.append(f'{where}: 틀린 표기 「{w}」 → {t[:40]}')
    for n in NAMES:
        if n in t: errs.append(f'{where}: 사람 NPC 이름은 변수로 ({{sera.name}} 등) 「{n}」 → {t[:40]}')
    if human_ctx:
        m = GENDER.search(t)
        if m: errs.append(f'{where}: 사람 NPC 이야기에 성별 단정 표현 「{m.group(1)}」 → {t[:40]}')
    for m in VAR.finditer(t):
        a, b = m.group(1), m.group(2)
        ok = (a == 'player' and not b) or (a == 'npc' and b) or (a in NPCS and b)
        if not ok: errs.append(f'{where}: 모르는 변수 {m.group(0)}')
        if m.group(3) is not None and not re.fullmatch(r'[가-힣]+/[가-힣]+', m.group(3)): errs.append(f'{where}: 조사 표기는 {{변수|받침O/받침X}} 「{m.group(0)}」')
    for m in josa.BARE.finditer(t): errs.append(f'{where}: 변수 뒤 조사는 함수로 써요 (예: {{player|이/가}}) 「{m.group(0)}」 → {t[:40]}')
    for m in josa.PAREN.finditer(t): errs.append(f'{where}: 조사 병기 「{m.group(0)}」 금지 → {t[:40]}')
    for nm in ('하루', '민준', '하늘'):   # 받침 없음 · 받침 있음 · ㄹ 받침 이름으로 렌더링해서 조사 확인
        vals = {'player': nm, 'npc.name': nm, 'npc.husband': nm, 'sera.husband': nm, **{f'{x}.name': nm for x in NPCS}}
        out, marks = josa.render(t, vals)
        for e in josa.check_rendered(out, marks): errs.append(f'{where}: 「{nm}」로 렌더링하면 조사 오류 {e} → {t[:40]}')

def paths_info(script, errs, where):
    """라벨 위치, 경로별 대사 줄 수 (최소·최대). 순서대로 실행, choice/if는 라벨로 점프, goto로 합류"""
    lab = {}
    for i, n in enumerate(script):
        if 'label' in n:
            if n['label'] in lab: errs.append(f'{where}: 라벨 중복 {n["label"]}')
            lab[n['label']] = i
    targets = set()
    for i, n in enumerate(script):
        c = n.get('cmd')
        nexts = []
        if c == 'choice': nexts = [o.get('next') for o in n.get('options', [])]
        elif c in ('if_flag', 'if_heart'): nexts = [n.get('then'), n.get('else')]
        elif c == 'goto': nexts = [n.get('to')]
        for t in nexts:
            if t not in lab: errs.append(f'{where}: 없는 라벨로 이동 「{t}」 (#{i})')
            elif c != 'goto': targets.add(t)
    # 분기 라벨에 앞 분기가 흘러 들어오는지 (분기 끝은 goto로 합류해야 해요)
    for t in targets:
        i = lab[t]; j = i - 1
        while j >= 0 and 'label' in script[j] and 'cmd' not in script[j]: j -= 1
        if j >= 0 and script[j].get('cmd') not in ('goto', 'choice', 'if_flag', 'if_heart'):
            errs.append(f'{where}: 분기 라벨 「{t}」 앞에 goto가 없어서 앞 장면이 흘러 들어와요')
    memo, stack = {}, set()
    def run(i):
        if i >= len(script): return (0, 0)
        if i in memo: return memo[i]
        if i in stack: errs.append(f'{where}: 되돌아가는 고리 (#{i})'); return (0, 0)
        stack.add(i); n = script[i]; c = n.get('cmd'); here = 1 if c in ('line', 'narration') else 0
        if c == 'choice': outs = [lab[o['next']] for o in n.get('options', []) if o.get('next') in lab]
        elif c in ('if_flag', 'if_heart'): outs = [lab[x] for x in (n.get('then'), n.get('else')) if x in lab]
        elif c == 'goto': outs = [lab[n['to']]] if n.get('to') in lab else []
        else: outs = [i + 1]
        rs = [run(o) for o in outs] or [(0, 0)]
        r = (here + min(a for a, _ in rs), here + max(b for _, b in rs))
        stack.discard(i); memo[i] = r; return r
    return lab, run(0)

def check_event(npc, k, ev, flags_set, flags_used, prof_cast, errs):
    w = f'{npc} ♥{k}'
    if ev.get('npc') != npc or ev.get('heart') != k: errs.append(f'{w}: npc/heart 값이 파일과 달라요')
    if ev.get('id') != f'{npc}_heart_{k:02d}': errs.append(f'{w}: id는 {npc}_heart_{k:02d}')
    if not ev.get('title'): errs.append(f'{w}: 제목 없음')
    cd = ev.get('conditions') or {}
    if cd.get('minHeart') != k: errs.append(f'{w}: conditions.minHeart = {k}')
    loc = cd.get('location')
    if loc not in PLACES or not PLACES[loc]['stand']: errs.append(f'{w}: conditions.location은 서 있을 수 있는 장소(stand) 「{loc}」')
    for t in cd.get('time', []):
        if t not in TIMES: errs.append(f'{w}: 시간대 「{t}」')
    for t in cd.get('weather', []):
        if t not in WEATHER: errs.append(f'{w}: 날씨 「{t}」')
    if cd.get('weather') == ['snow']: errs.append(f'{w}: 눈 오는 날만으로는 열리기 너무 어려워요')
    for a in cd.get('after', []):
        m = re.fullmatch(r'([a-z]+):(\d+)', a)
        if not m or m.group(1) not in NPCS: errs.append(f'{w}: after 형식 「{a}」 (예: aula:8)')
    allowed = set(cd) - {'minHeart', 'location', 'time', 'weather', 'moon', 'festival', 'dow', 'story', 'after', 'afterDays', 'hidden'}
    if allowed: errs.append(f'{w}: 모르는 조건 {sorted(allowed)}')
    rw = ev.get('rewards') or {}
    for it in (rw.get('items') or {}):
        if it not in ITEMS: errs.append(f'{w}: 보상 아이템 id 「{it}」')
    for f in rw.get('flags', []): flags_set.setdefault(f, []).append(w)
    pk = rw.get('perk'); pk = [] if pk is None else pk if isinstance(pk, list) else [pk]
    for x in pk:
        if x not in PERKS: errs.append(f'{w}: 모르는 perk 「{x}」')
    for key in ('coin', 'mana', 'know'):
        if not isinstance(rw.get(key, 0), int): errs.append(f'{w}: rewards.{key}는 숫자')
    scn = ev.get('scene') or {}
    if scn.get('time') and scn['time'] not in TIMES: errs.append(f'{w}: scene.time')
    if scn.get('weather') and scn['weather'] not in WEATHER | {'storm'}: errs.append(f'{w}: scene.weather')
    sc = ev.get('script') or []
    lab, (lo, hi) = paths_info(sc, errs, w)
    a, b = (110, 140) if k in BIG else (90, 120)
    if lo < a or hi > b: errs.append(f'{w}: 분량 — 가장 짧은 경로 {lo} 줄 / 가장 긴 경로 {hi} 줄 (기준 {a}~{b} 줄)')
    if 'ending' not in lab: errs.append(f'{w}: 「ending」 라벨이 없어요 (서먹한 결말이 끼어들 자리)')
    cold = ev.get('cold') or []
    nc = sum(1 for n in cold if n.get('cmd') in ('line', 'narration'))
    if not 5 <= nc <= 10: errs.append(f'{w}: cold(서먹한 결말) 대사 {nc} 줄 (5~10 줄)')
    if k > 1 and not any(n.get('cmd') == 'if_flag' and n.get('flag') == f'{npc}_was_cold' for n in sc):
        errs.append(f'{w}: 첫머리에 if_flag {npc}_was_cold 분기가 없어요 (지난 이벤트가 서먹하게 끝났을 때)')
    chs = [n for n in sc if n.get('cmd') == 'choice']
    if not 3 <= len(chs) <= 5: errs.append(f'{w}: 선택지 지점 {len(chs)} 개 (3~5 개)')
    signs = set()
    for n in chs:
        ops = n.get('options') or []
        if not 2 <= len(ops) <= 4: errs.append(f'{w}: 선택지 {n.get("id")} 보기 {len(ops)} 개 (2~4 개)')
        for o in ops:
            v = o.get('affinity')
            if v not in AFF: errs.append(f'{w}: 호감도 값은 +30/+15/0/-15/-30 「{v}」')
            else: signs.add((v > 0) - (v < 0))
            if o.get('flag'): flags_set.setdefault(o['flag'], []).append(w)
            if not o.get('text'): errs.append(f'{w}: 보기 문구 없음')
    if signs != {1, 0, -1}: errs.append(f'{w}: 상승·유지·하락 보기가 모두 있어야 해요 (지금 {sorted(signs)})')
    if not any(n.get('cmd') in ('move', 'follow') for n in sc): errs.append(f'{w}: 장면 이동(move·follow)이 없어요')
    who_ok = set(CAST) | set(prof_cast)
    for i, n in enumerate(sc + cold):
        c = n.get('cmd')
        if c is None:
            if 'label' not in n: errs.append(f'{w}: #{i} cmd 없음')
            continue
        if c not in CMDS: errs.append(f'{w}: #{i} 모르는 명령 「{c}」'); continue
        if c == 'line':
            if n.get('who') not in who_ok: errs.append(f'{w}: #{i} who 「{n.get("who")}」 (cast.json 또는 profile.cast)')
            if n.get('face') and n['face'] not in FACES: errs.append(f'{w}: #{i} face 「{n["face"]}」')
            if not n.get('text'): errs.append(f'{w}: #{i} 대사 비어 있음')
        if c == 'narration' and not n.get('text'): errs.append(f'{w}: #{i} 지문 비어 있음')
        if c in ('walk', 'show', 'hide', 'emote', 'follow') and n.get('who') not in who_ok: errs.append(f'{w}: #{i} who 「{n.get("who")}」')
        if c in ('walk',) and n.get('to') not in POS: errs.append(f'{w}: #{i} walk.to는 {sorted(POS)}')
        if c == 'show' and n.get('at', 'center') not in POS: errs.append(f'{w}: #{i} show.at')
        if c in ('move', 'follow') and n.get('to') not in PLACES: errs.append(f'{w}: #{i} 장소 「{n.get("to")}」 (places.json)')
        if c == 'move' and n.get('time') and n['time'] not in TIMES: errs.append(f'{w}: #{i} move.time')
        if c == 'move' and n.get('weather') and n['weather'] not in WEATHER | {'storm'}: errs.append(f'{w}: #{i} move.weather')
        if c == 'emote' and n.get('icon') not in EMOTES: errs.append(f'{w}: #{i} 감정 아이콘 「{n.get("icon")}」')
        if c == 'sfx' and n.get('id') not in SFX: errs.append(f'{w}: #{i} 효과음 「{n.get("id")}」')
        if c == 'bgm' and n.get('id') not in BGM: errs.append(f'{w}: #{i} 음악 「{n.get("id")}」')
        if c == 'camera' and n.get('action') not in CAMERA: errs.append(f'{w}: #{i} camera.action')
        if c == 'wait' and not (isinstance(n.get('sec'), (int, float)) and 0 < n['sec'] <= 5): errs.append(f'{w}: #{i} wait.sec (0~5)')
        if c in ('give_item', 'take_item') and n.get('item') not in ITEMS: errs.append(f'{w}: #{i} 아이템 id 「{n.get("item")}」')
        if c == 'set_flag': flags_set.setdefault(n.get('flag'), []).append(w)
        if c == 'affinity' and not isinstance(n.get('value'), int): errs.append(f'{w}: #{i} affinity.value')
        if c == 'if_flag' and not AUTO.fullmatch(n.get('flag') or ''): flags_used.setdefault(n.get('flag'), []).append(w)
        if c == 'if_flag' and not re.fullmatch(r'[a-z]+_[a-z0-9_]+', n.get('flag') or ''): errs.append(f'{w}: #{i} 플래그 이름 「{n.get("flag")}」')
        if c == 'if_heart' and (not isinstance(n.get('min'), int) or (n.get('npc') and n['npc'] not in NPCS)): errs.append(f'{w}: #{i} if_heart (min, npc)')
    for t in texts_of({'title': ev.get('title'), 's': sc, 'c': cold, 'f': ev.get('fail') or []}):
        korean(w, t, npc in HUMAN, errs)
    return lo, hi, len(chs)

def check_profile(npc, p, errs):
    w = f'{npc} profile'
    for k in ('id', 'name', 'title', 'likes', 'dislikes', 'daily', 'ambient', 'gift', 'recall'):
        if k not in p: errs.append(f'{w}: 「{k}」 없음')
    for st in 'ABCD':
        n = len((p.get('daily') or {}).get(st, []))
        if n < 12: errs.append(f'{w}: 말투 {st} 단계 일상 대사 {n} 줄 (12 줄 이상)')
    am = p.get('ambient') or {}
    for k in ('morning', 'day', 'evening', 'night', 'rain', 'fog'):
        if not am.get(k): errs.append(f'{w}: ambient.{k} 대사 없음')
    if sum(len(v) for v in am.values()) < 6: errs.append(f'{w}: 날씨·시간대 대사 6 줄 이상')
    for k in ('love', 'like', 'hate'):
        if len((p.get('gift') or {}).get(k, [])) < 3: errs.append(f'{w}: 선물 반응 {k} 3 줄 이상')
    if len(p.get('recall') or {}) < 5: errs.append(f'{w}: recall(하트 이벤트를 본 뒤 떠올리는 평소 대사) 5 개 이상의 하트에')
    for it in (p.get('likes') or []) + (p.get('dislikes') or []):
        if it not in ITEMS: errs.append(f'{w}: 아이템 id 「{it}」')
    for t in texts_of({'d': p.get('daily'), 'a': p.get('ambient'), 'g': p.get('gift'), 'r': p.get('recall'), 'title': p.get('title')}):
        korean(w, t, npc in HUMAN, errs)
    return p.get('cast') or {}

def main(ids):
    total = 0; summary = []; all_set, all_used = {}, {}
    for npc in ids:
        errs = []; d = os.path.join(DATA, npc)
        try: prof = json.load(open(os.path.join(d, 'profile.json')))
        except Exception as e: print(f'[{npc}] profile.json 읽기 실패: {e}'); total += 1; continue
        pc = check_profile(npc, prof, errs); fs, fu = {}, {}; rows = []
        for k in range(1, 11):
            fn = os.path.join(d, 'events', f'heart_{k:02d}.json')
            try: ev = json.load(open(fn))
            except Exception as e: errs.append(f'{npc} ♥{k}: 파일 읽기 실패 {e}'); continue
            lo, hi, nch = check_event(npc, k, ev, fs, fu, pc, errs); rows.append((k, ev.get('title'), lo, hi, nch))
        own = [f for f in fs if f.startswith(npc + '_')]
        if len(own) < 3: errs.append(f'{npc}: 분기 플래그 {len(own)} 개 (3 개 이상, 이름은 {npc}_로 시작)')
        for f in fs:
            if not f: errs.append(f'{npc}: 이름 없는 플래그'); continue
            if not f.startswith(npc + '_'): errs.append(f'{npc}: 플래그 이름은 {npc}_로 시작 「{f}」')
        for f, ws in fs.items(): all_set.setdefault(f, []).extend(ws)
        for f, ws in fu.items(): all_used.setdefault(f, []).extend(ws)
        summary.append((npc, rows, sorted(fs)))
        for e in errs: print('  ✗', e)
        print(f'[{npc}] 위반 {len(errs)} 건'); total += len(errs)
    # 플래그: 만든 건 어딘가에서 쓰여야 하고, 쓰는 건 어딘가에서 만들어져야 해요 (검사한 NPC 범위 안에서)
    for f, ws in all_set.items():
        if f and f not in all_used: print(f'  ✗ 플래그 「{f}」를 만들었는데 쓰는 곳이 없어요 ({ws[0]})'); total += 1
    for f, ws in all_used.items():
        if f not in all_set and f.split('_')[0] in ids: print(f'  ✗ 플래그 「{f}」를 쓰는데 만드는 곳이 없어요 ({ws[0]})'); total += 1
    if '-v' in sys.argv:
        for npc, rows, fl in summary:
            print(f'\n## {npc}')
            for k, t, lo, hi, nch in rows: print(f'  ♥{k:<2} {t}  {lo}~{hi} 줄  선택지 {nch}')
            print('  플래그:', ', '.join(fl))
    print(f'\n총 위반 {total} 건')
    return total

if __name__ == '__main__':
    ids = [a for a in sys.argv[1:] if not a.startswith('-')] or NPCS
    sys.exit(1 if main(ids) else 0)
