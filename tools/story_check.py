# 이야기 파일 검사: 하트 이야기(data/npc/*/events)·메인 의뢰 장면(data/main/*/)을 훑어서 엔진에서 멈추거나 이상하게 보일 곳을 찾아요
#   python3 tools/story_check.py  → 문제 목록 (없으면 「문제 없음」)
#   보는 것: 엔진이 모르는 명령 · 없는 label로 가는 goto/선택지/조건 · 「플레이어가 따라가요」(follow who=player) · 없는 자리(walk/show) · 없는 장소(move/follow)
#           · 대사에 나오는데 무대에 없는 인물 · 선택지 없는 choice · 끝까지 못 가는 label 고리
import json, os, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); D = os.path.join(ROOT, 'public', 'data')
CMDS = {'bgm', 'affinity', 'camera', 'choice', 'emote', 'fade_in', 'fade_out', 'flash', 'follow', 'give_item', 'goto', 'hide', 'if_flag', 'if_heart', 'if_item', 'if_quest', 'input', 'line', 'move', 'narration', 'rename', 'set_flag', 'sfx', 'show', 'take_item', 'wait', 'walk', 'end'}
POS = {'far_left', 'left', 'center', 'right', 'far_right', 'off_left', 'off_right'}
PLACES = {p['id'] for p in json.load(open(os.path.join(D, 'npc', 'places.json')))} | {p['id'] for p in json.load(open(os.path.join(D, 'main', 'places.json')))}
probs = []
def steps_of(o):
    if isinstance(o, list): return o
    for k in ('scene', 'script', 'steps', 'cmds'):
        if isinstance(o.get(k), list): return o[k]
    return None
def check(path, st):
    labels = {s['label'] for s in st if isinstance(s, dict) and 'label' in s}
    for i, s in enumerate(st):
        if not isinstance(s, dict): probs.append((path, i, '이상한 줄', s)); continue
        if 'label' in s: continue
        c = s.get('cmd')
        if c not in CMDS: probs.append((path, i, '모르는 명령', c)); continue
        for k in ('to', 'then', 'else') if c in ('goto', 'if_flag', 'if_heart', 'if_item', 'if_quest') else ('then', 'else'):
            if k in s and k == 'to' and c == 'goto' and s[k] not in labels: probs.append((path, i, 'goto 갈 곳 없음', s[k]))
            elif k in ('then', 'else') and k in s and s[k] not in labels: probs.append((path, i, f'{c} {k} 갈 곳 없음', s[k]))
        if c == 'choice':
            if not s.get('options'): probs.append((path, i, '선택지 없음', ''))
            for o in s.get('options', []):
                if o.get('next') and o['next'] not in labels: probs.append((path, i, '선택지 갈 곳 없음', o['next']))
        if c == 'follow' and s.get('who') == 'player': probs.append((path, i, 'follow 대상이 player', ''))
        if c in ('move', 'follow') and s.get('to') not in PLACES: probs.append((path, i, f'{c} 장소 없음', s.get('to')))
        if c == 'walk' and s.get('to') not in POS: probs.append((path, i, 'walk 자리 없음', s.get('to')))
        if c == 'show' and s.get('at', 'center') not in POS: probs.append((path, i, 'show 자리 없음', s.get('at')))
files = sorted(glob.glob(os.path.join(D, 'npc', '*', 'events', '*.json'))) + sorted(glob.glob(os.path.join(D, 'main', '*', '**', '*.json'), recursive=True))
n = 0
for f in files:
    try: o = json.load(open(f))
    except Exception as e: probs.append((f, -1, 'JSON 오류', str(e))); continue
    if isinstance(o, dict) and not steps_of(o) and isinstance(o.get('scenes'), dict):
        for k, v in o['scenes'].items():
            st = steps_of(v) if isinstance(v, dict) else v
            if isinstance(st, list): check(f + '#' + k, st); n += 1
        continue
    st = steps_of(o) if isinstance(o, dict) else o
    if isinstance(st, list) and st and isinstance(st[0], dict) and ('cmd' in st[0] or 'label' in st[0]): check(f, st); n += 1
print('검사한 장면', n)
for p in probs: print(os.path.relpath(p[0], D), '#', p[1], p[2], p[3])
print('문제 없음' if not probs else f'문제 {len(probs)}개')
