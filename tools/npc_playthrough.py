# 하트 이벤트를 정해진 방식으로 끝까지 자동 플레이해서 대사를 이어 붙인 글로: python3 tools/npc_playthrough.py <출력 폴더>
#   엔진(public/index.html evRun)과 같은 규칙: 선택지 → 호감도 합, 「ending」에서 합이 −30 이하면 서먹한 결말(cold),
#   플래그는 NPC끼리 공유, xxx_hN = 그 이벤트를 봤음, xxx_was_cold = 그 NPC의 바로 앞 이벤트가 서먹하게 끝났음
#   경로: 1 모든 선택 최고점 · 2 모든 선택 0점 · 3 서먹한 결말 섞기 · 4 NPC 순서 거꾸로(레오→나비, 한 명씩 끝까지)
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from josa import VAR as JVAR, pick as jpick
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, 'public', 'data', 'npc')
NPCS = ['nabi', 'batri', 'kappa', 'aula', 'mandi', 'jipsin', 'sera', 'madeleine', 'stella', 'leo']
KO = {'nabi': '나비', 'batri': '배트리', 'kappa': '캇파', 'aula': '아울라', 'mandi': '맨디', 'jipsin': '짚신', 'sera': '세라', 'madeleine': '마들렌', 'stella': '스텔라', 'leo': '레오'}
VARS = {'player': '민준', 'sera.name': '세라', 'madeleine.name': '마들렌', 'stella.name': '스텔라', 'leo.name': '레오', 'sera.husband': '루카스', 'npc.husband': '루카스'}
PLACES = {p['id']: p['name'] for p in json.load(open(os.path.join(D, 'places.json')))}
CAST = json.load(open(os.path.join(D, 'cast.json')))
ITEMS = json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json')))
EV = {(n, k): json.load(open(os.path.join(D, n, 'events', f'heart_{k:02d}.json'))) for n in NPCS for k in range(1, 11)}
PCAST = {n: (json.load(open(os.path.join(D, n, 'profile.json'))).get('cast') or {}) for n in NPCS}

def fill(t, npc):
    def r(m):
        k = m.group(1)
        if k == 'npc.name': k = npc + '.name'
        v = VARS.get(k, KO.get(k.split('.')[0], k) if k.endswith('.name') else k)
        return v + (jpick(v, m.group(2), m.group(3)) if m.group(2) is not None else '')
    return JVAR.sub(r, t)

def who(w, npc):
    if w == 'player': return '민준'
    if w in KO: return KO[w]
    c = PCAST[npc].get(w) or CAST.get(w) or {}
    return fill(c.get('name', w), npc)

class Game:
    def __init__(s): s.flags, s.seen, s.cold, s.out = set(), {n: {} for n in NPCS}, {n: False for n in NPCS}, []
    def on(s, f, npc):
        m = re.fullmatch(r'([a-z]+)_h(\d+)', f)
        if m: return int(m.group(2)) in s.seen.get(m.group(1), {})
        m = re.fullmatch(r'([a-z]+)_was_cold', f)
        if m: return s.cold.get(m.group(1), False)
        return f in s.flags
    def can_open(s, npc, k):
        for a in (EV[(npc, k)].get('conditions') or {}).get('after', []):
            o, h = a.split(':')
            if int(h) not in s.seen[o]: return False
        return True
    def play(s, npc, k, policy):
        ev = EV[(npc, k)]; sc = ev['script']; lab = {n['label']: i for i, n in enumerate(sc) if 'label' in n}
        P = s.out.append; total = 0; cold = False
        P(f'\n\n━━━━━━━━ {KO[npc]} ♥{k} 「{fill(ev.get("title", ""), npc)}」 ━━━━━━━━')
        c = ev.get('conditions') or {}; P(f'(열리는 곳: {fill(PLACES.get(c.get("location"), ""), npc)}{" · 먼저 볼 것: " + ", ".join(c["after"]) if c.get("after") else ""}{" · 앞 이벤트 " + str(c["afterDays"]) + " 일 뒤" if c.get("afterDays") else ""})')
        def run(seq, i=0, top=True):
            nonlocal total, cold
            guard = 0
            while i < len(seq) and guard < 5000:
                guard += 1; n = seq[i]; i += 1
                if top and n.get('label') == 'ending' and total <= -30 and ev.get('cold'):
                    P('\n  ── 서먹한 결말 ──'); cold = True; run(ev['cold'], 0, False); return
                cmd = n.get('cmd')
                if cmd == 'line': P(f'{who(n["who"], npc)}: {fill(n.get("text", ""), npc)}')
                elif cmd == 'narration': P(f'  ({fill(n.get("text", ""), npc)})')
                elif cmd == 'choice':
                    ops = n.get('options') or []; o = policy(npc, k, ops)
                    P('  [선택지] ' + ' / '.join(f'{"▶" if x is o else " "}{fill(x.get("text", ""), npc)} ({x.get("affinity", 0):+d})' for x in ops))
                    total += o.get('affinity', 0)
                    if o.get('flag'): s.flags.add(o['flag']); P(f'  ▶ 플래그: {o["flag"]}')
                    if o.get('next') in lab: i = lab[o['next']]
                elif cmd == 'goto':
                    if n.get('to') in lab: i = lab[n['to']]
                elif cmd == 'if_flag':
                    v = s.on(n['flag'], npc); P(f'  [분기 {n["flag"]} = {"있음" if v else "없음"}]')
                    t = n['then'] if v else n['else']
                    if t in lab: i = lab[t]
                elif cmd == 'if_heart':
                    who_ = n.get('npc') or npc; hv = k if who_ == npc else len(s.seen[who_])
                    t = n['then'] if hv >= n.get('min', 0) else n['else']
                    if t in lab: i = lab[t]
                elif cmd in ('move', 'follow'): P(f'  📍 {fill(PLACES.get(n.get("to"), n.get("to", "")), npc)}')
                elif cmd == 'set_flag': s.flags.add(n['flag']); P(f'  ▶ 플래그: {n["flag"]}')
                elif cmd == 'give_item': P(f'  🎁 {ITEMS.get(n.get("item"), n.get("item"))} ×{n.get("n", 1)}')
        run(sc)
        s.seen[npc][k] = 'cold' if cold else 'ok'; s.cold[npc] = cold
        for f in (ev.get('rewards') or {}).get('flags') or []: s.flags.add(f)
        P(f'\n  → 호감도 합 {total:+d}{" · 서먹하게 끝남" if cold else ""}')
        return cold

def best(npc, k, ops): return max(ops, key=lambda o: o.get('affinity', 0))
def zero(npc, k, ops):
    z = [o for o in ops if o.get('affinity', 0) == 0]
    return z[0] if z else min(ops, key=lambda o: (abs(o.get('affinity', 0)), -o.get('affinity', 0)))
COLD_AT = {('kappa', 7), ('stella', 8), ('leo', 9)}
def mixed(npc, k, ops): return min(ops, key=lambda o: o.get('affinity', 0)) if (npc, k) in COLD_AT else best(npc, k, ops)

def route(policy, order, by_npc):
    g = Game(); done = {n: 0 for n in NPCS}; colds = []
    def step(n):
        k = done[n] + 1
        if k > 10 or not g.can_open(n, k): return False
        if g.play(n, k, policy): colds.append(f'{KO[n]} ♥{k}')
        done[n] = k; return True
    if by_npc:   # 한 명씩 끝까지, 막히면 다음 사람으로 넘어갔다가 다시
        while any(done[n] < 10 for n in order):
            moved = False
            for n in order:
                while step(n): moved = True
            if not moved: break
    else:        # 하트 단계별로 돌아가며
        while any(done[n] < 10 for n in order):
            moved = False
            for n in order:
                if step(n): moved = True
            if not moved: break
    left = [f'{KO[n]} ♥{done[n] + 1}' for n in order if done[n] < 10]
    return g.out, colds, left

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    R = [('1_모든선택_최고점', best, NPCS, False, '모든 선택지에서 호감도가 가장 높은 보기를 고름 · 하트 단계별로 10 명을 돌아가며 진행'),
         ('2_모든선택_0점', zero, NPCS, False, '모든 선택지에서 호감도 0 보기를 고름(없으면 0에 가장 가까운 것) · 하트 단계별로 돌아가며'),
         ('3_서먹한결말_섞기', mixed, NPCS, False, '최고점으로 가다가 캇파 ♥7 · 스텔라 ♥8 · 레오 ♥9에서만 가장 낮은 보기를 골라 서먹하게 끝냄 · 하트 단계별로 돌아가며'),
         ('4_순서_거꾸로', best, NPCS[::-1], True, 'NPC 순서를 거꾸로(레오 → 나비), 한 명씩 ♥1~♥10을 끝까지 · 선택은 최고점 · 다른 NPC 이벤트가 먼저 필요하면 그 사람 차례까지 미룸')]
    for name, pol, order, by, desc in R:
        out, colds, left = route(pol, order, by)
        head = [f'# 플레이 경로 {name.replace("_", " ")}', f'# {desc}', f'# 주인공 이름 미리 보기: 민준 · 서먹하게 끝난 이벤트: {", ".join(colds) or "없음"}' + (f' · 못 연 이벤트: {", ".join(left)}' if left else '')]
        open(os.path.join(outdir, name + '.txt'), 'w').write('\n'.join(head + out) + '\n')
        print(name, len(out), '줄', '서먹:', colds, '못 연 것:', left)

if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'audit', 'story_paths'))
