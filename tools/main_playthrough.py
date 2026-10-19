# 메인 의뢰를 정해진 방식으로 끝까지 자동 플레이해서 대사를 이어 붙인 글로: python3 tools/main_playthrough.py <출력 폴더>
#   경로: 1 모든 결말 A(첫 번째 결말 플래그) · 2 모든 결말 B(두 번째) · 3 서브 NPC 하트 전부 0 (결말은 A)
#   엔진(index.html evRun)과 같은 규칙으로 label/goto/if_flag/if_heart/if_quest/if_item 을 따라가요
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from josa import VAR as JVAR, pick as jpick
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, 'public', 'data', 'main'); ND = os.path.join(ROOT, 'public', 'data', 'npc')
IDX = json.load(open(os.path.join(D, 'index.json'))); QUESTS = IDX['quests'] if isinstance(IDX, dict) else IDX
CAST = {**json.load(open(os.path.join(ND, 'cast.json'))), **json.load(open(os.path.join(D, 'cast.json')))}
PLACES = {p['id']: p['name'] for p in json.load(open(os.path.join(ND, 'places.json')))}
PLACES.update({p['id']: p['name'] for p in json.load(open(os.path.join(D, 'places.json')))})
ITEMS = dict(json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json'))))
NAME = {'nabi': '나비', 'batri': '배트리', 'kappa': '캇파', 'aula': '아울라', 'mandi': '맨디', 'jipsin': '짚신', 'sera': '세라', 'madeleine': '마들렌', 'stella': '스텔라', 'leo': '레오'}
VARS = {'player': '민준', 'sera.name': '세라', 'madeleine.name': '마들렌', 'stella.name': '스텔라', 'leo.name': '레오', 'sera.husband': '루카스', 'npc.husband': '루카스'}
Q = {}
for q in QUESTS:
    try: Q[q] = json.load(open(os.path.join(D, q, 'quest.json')))
    except Exception: continue
    for k, v in (Q[q].get('items') or {}).items(): ITEMS[k] = v.get('name', k)
    for k, v in (Q[q].get('cast') or {}).items(): CAST.setdefault(k, v)
for k, v in CAST.items(): NAME.setdefault(k, re.sub(r'\{[^}]*\}', '', v.get('name', k)) or k)

class Game:
    def __init__(s, hearts): s.flags = set(); s.hearts = hearts; s.named = {}; s.inv = {}; s.out = []; s.done = set()
    def name(s, k): return s.named.get(k) or NAME.get(k, k)
    def fill(s, t):
        def r(m):
            k = m.group(1); v = VARS.get(k, s.name(k.split('.')[0]) if k.endswith('.name') else k)
            return v + (jpick(v, m.group(2), m.group(3)) if m.group(2) is not None else '')
        return JVAR.sub(r, t)
    def who(s, w): return '민준' if w == 'player' else '목소리' if w == 'voice' else s.fill(CAST.get(w, {}).get('name', s.name(w)))
    def play(s, qid, n, kind, policy):
        try: sc = json.load(open(os.path.join(D, qid, f'stage_{n}_{kind}.json')))
        except Exception: s.out.append(f'\n(장면 없음: {qid} {n} {kind})'); return
        P = s.out.append; script = sc.get('script') or []; lab = {x['label']: i for i, x in enumerate(script) if 'label' in x}
        P(f'\n\n━━━━━━━━ {Q[qid].get("name")} · {n}단계 {"부탁" if kind == "request" else "완료"} 「{s.fill(sc.get("title", ""))}」 ━━━━━━━━')
        if kind == 'request' and sc.get('arrival'):
            P('  [등장 컷신] ' + ' / '.join(f'{s.who(c.get("who"))}: {s.fill(c.get("text", ""))}' for c in sc['arrival'] if c.get('cmd') == 'say'))
        i = 0; guard = 0
        while i < len(script) and guard < 5000:
            guard += 1; x = script[i]; i += 1; c = x.get('cmd')
            if c == 'line': P(f'{s.who(x.get("who"))}: {s.fill(re.sub(r"^\[(기본|웃음|화남|놀람|부끄러움)\]\s*", "", x.get("text", "")))}')
            elif c == 'narration': P(f'  ({s.fill(x.get("text", ""))})')
            elif c == 'choice':
                ops = x.get('options') or []; o = policy(qid, n, kind, ops)
                P('  [선택지] ' + ' / '.join(f'{"▶" if y is o else " "}{s.fill(y.get("text", ""))}' for y in ops))
                if o.get('confirm'): P(f'  [확인 창] {s.fill(o["confirm"])} → 네')
                if o.get('flag'): s.flags.add(o['flag']); P(f'  ▶ 플래그: {o["flag"]}')
                if o.get('next') in lab: i = lab[o['next']]
            elif c == 'goto':
                if x.get('to') in lab: i = lab[x['to']]
            elif c == 'if_flag':
                v = x.get('flag') in s.flags or bool(re.fullmatch(r'([a-z]+)_h(\d+)', x.get('flag') or '') and s.hearts >= int(x['flag'].split('_h')[1]))
                P(f'  [분기 {x.get("flag")} = {"있음" if v else "없음"}]'); t = x.get('then') if v else x.get('else')
                if t in lab: i = lab[t]
            elif c == 'if_heart':
                v = s.hearts >= (x.get('min') or 0); P(f'  [서브 NPC {NAME.get(x.get("npc"), x.get("npc"))} ♥{x.get("min")} = {"됨" if v else "안 됨"}]'); t = x.get('then') if v else x.get('else')
                if t in lab: i = lab[t]
            elif c == 'if_quest':
                v = x.get('quest') in s.done; t = x.get('then') if v else x.get('else')
                if t in lab: i = lab[t]
            elif c == 'if_item':
                v = s.inv.get(x.get('item'), 0) >= (x.get('n') or 1); t = x.get('then') if v else x.get('else')
                if t in lab: i = lab[t]
            elif c in ('move', 'follow'): P(f'  📍 {s.fill(PLACES.get(x.get("to"), x.get("to", "")))}')
            elif c == 'set_flag': s.flags.add(x.get('flag')); P(f'  ▶ 플래그: {x.get("flag")}')
            elif c == 'give_item': s.inv[x.get('item')] = s.inv.get(x.get('item'), 0) + (x.get('n') or 1); P(f'  🎁 {ITEMS.get(x.get("item"), x.get("item"))} ×{x.get("n", 1)}')
            elif c == 'take_item': s.inv[x.get('item')] = max(0, s.inv.get(x.get('item'), 0) - (x.get('n') or 1)); P(f'  ↪ {ITEMS.get(x.get("item"), x.get("item"))} 건넴')
            elif c == 'input': s.named[x.get('key')] = x.get('default', ''); P(f'  ✍ 이름: {x.get("default", "")}')
            elif c == 'rename': s.named[x.get('who')] = x.get('name'); P(f'  ✨ {NAME.get(x.get("who"))} → {x.get("name")}')
    def quest(s, qid, policy):
        q = Q.get(qid)
        if not q: return
        s.out.append(f'\n\n████████ 의뢰 {q.get("order")} 「{q.get("name")}」 ({s.name(q.get("client"))}) ████████')
        for n in range(1, 6):
            st = next((z for z in q.get('stages') or [] if z.get('n') == n), {})
            s.play(qid, n, 'request', policy)
            s.out.append('  [목표] ' + ' · '.join(o.get('type', '') + (' ' + ITEMS.get(o.get('item'), o.get('item', '')) if o.get('item') else '') for o in st.get('objectives') or []))
            s.play(qid, n, 'complete', policy)
        for it in (q.get('completion_reward') or {}).get('items') or []: s.inv[it] = s.inv.get(it, 0) + 1
        s.done.add(qid)

def pol_idx(j):
    def p(qid, n, kind, ops):
        ef = Q[qid].get('ending_flags') or []
        fl = [o for o in ops if o.get('flag') in ef]
        if fl: want = ef[min(j, len(ef) - 1)]; return next((o for o in fl if o.get('flag') == want), fl[0])
        return ops[j % len(ops)] if ops else {}
    return p

def main(out):
    os.makedirs(out, exist_ok=True)
    routes = [('1_모든결말_A.txt', 10, pol_idx(0), '모든 결말 A (첫 번째 결말 플래그) · 서브 NPC 하트 10'), ('2_모든결말_B.txt', 10, pol_idx(1), '모든 결말 B (두 번째 결말 플래그) · 서브 NPC 하트 10'), ('3_하트0_결말A.txt', 0, pol_idx(0), '서브 NPC 하트 전부 0 · 결말 A')]
    for fn, h, pol, desc in routes:
        g = Game(h); g.out.append(f'# 호박달 일곱 등불의 의뢰 · 대표 경로: {desc}\n# 주인공 이름 민준, 사람 NPC 이름은 기본값')
        for qid in QUESTS: g.quest(qid, pol)
        txt = '\n'.join(g.out); open(os.path.join(out, fn), 'w').write(txt); print(fn, len(txt) // 1024, 'KB', sum(1 for l in g.out if l and not l.startswith('  ') and not l.startswith('\n')), '대사 줄')

if __name__ == '__main__': main(sys.argv[1])
