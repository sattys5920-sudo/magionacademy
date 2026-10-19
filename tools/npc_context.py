# 하트 이벤트 맥락 검사 (validate_npc.py가 불러요)
#   1-1 분기 한정 표현: 앞 이벤트(또는 같은 이벤트 앞부분)의 한 선택지 분기에서만 나온 말을, 그 분기 플래그 조건 없이 되받는 대사 → 경고
#   다른 NPC 진행 플래그(xxx_hN) 분기에 「없을 때」 대사가 있는지 → 위반
#   서먹한 결말 플래그(xxx_was_cold)가 이벤트마다 새로 정해지는지(엔진 코드) → 위반
import json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def graph(sc):
    """이벤트 흐름 그래프. 노드: 명령 번호(int)와 선택 보기 ('o', 명령 번호, 보기 번호), 플래그 분기 ('f', 명령 번호, 참/거짓)"""
    lab = {n['label']: i for i, n in enumerate(sc) if 'label' in n}
    succ = {}
    for i, n in enumerate(sc):
        c = n.get('cmd')
        if c == 'choice':
            succ[i] = []
            for j, o in enumerate(n.get('options', [])):
                p = ('o', i, j); succ[i].append(p); succ[p] = [lab[o['next']]] if o.get('next') in lab else []
        elif c in ('if_flag', 'if_heart'):
            succ[i] = []
            for v, key in ((True, 'then'), (False, 'else')):
                p = ('f', i, v); succ[i].append(p); succ[p] = [lab[n[key]]] if n.get(key) in lab else []
        elif c == 'goto': succ[i] = [lab[n['to']]] if n.get('to') in lab else []
        else: succ[i] = [i + 1] if i + 1 < len(sc) else []
    return succ

def dominators(succ, start=0):
    nodes = list(succ); pred = {x: [] for x in nodes}
    for a, bs in succ.items():
        for b in bs: pred.setdefault(b, []).append(a)
    # 도달 가능한 노드만
    seen, st = {start}, [start]
    while st:
        a = st.pop()
        for b in succ.get(a, []):
            if b not in seen: seen.add(b); st.append(b)
    dom = {x: set(seen) for x in seen}; dom[start] = {start}
    order = [x for x in nodes if x in seen]
    changed = True
    while changed:
        changed = False
        for x in order:
            if x == start: continue
            ps = [p for p in pred.get(x, []) if p in seen]
            new = set.intersection(*(dom[p] for p in ps)) | {x} if ps else {x}
            if new != dom[x]: dom[x] = new; changed = True
    return dom

def option_flag(sc, succ, i, j):
    """보기를 고르면 켜지는 플래그: 보기의 flag + 그 분기 안(다른 보기와 합류하기 전)의 set_flag"""
    o = sc[i]['options'][j]; fl = {o['flag']} if o.get('flag') else set()
    k = succ.get(('o', i, j), [None])[0] if succ.get(('o', i, j)) else None
    steps = 0
    while isinstance(k, int) and k < len(sc) and steps < 60:
        n = sc[k]; c = n.get('cmd')
        if c == 'set_flag': fl.add(n.get('flag'))
        if c in ('goto', 'choice', 'if_flag', 'if_heart'): break
        k += 1; steps += 1
    return fl

QUOTE = re.compile(r"[‘'“\"「]([^’'”\"」]{3,40})[’'”\"」]")
MARK = re.compile(r'(라며|다며|랬지|랬잖아|말랬|하랬|했잖아|했었지|했지|잖아|했던|그때|처음 만난 날|그날|지난번)')
def key_phrases(t):
    out = [m.group(1) for m in QUOTE.finditer(t)]
    for m in MARK.finditer(t):
        pre = t[max(0, m.start() - 16):m.start()]
        pre = re.split(r'[.!?。,…]', pre)[-1].strip()
        if len(pre.replace(' ', '')) >= 4: out.append(pre)
    return out
BR = .5
def grams(s, n=3):
    s = re.sub(r'[^가-힣A-Za-z0-9]', '', s)
    return {s[i:i + n] for i in range(len(s) - n + 1)}

def branch_check(npc, events):
    """events: {k: ev}. 경고 목록"""
    warns = []
    info = {}
    for k, ev in events.items():
        sc = ev.get('script') or []; succ = graph(sc); dom = dominators(succ)
        nodes = {}
        for i, n in enumerate(sc):
            if n.get('cmd') not in ('line', 'narration') or i not in dom: continue
            opts = [d for d in dom[i] if isinstance(d, tuple) and d[0] == 'o']
            flags = {(sc[d[1]].get('flag'), d[2]) for d in dom[i] if isinstance(d, tuple) and d[0] == 'f' and sc[d[1]].get('cmd') == 'if_flag'}
            nodes[i] = (opts, flags)
        info[k] = (sc, succ, nodes)
    # 분기 한정 글(3-글자 조각)과 공통 글
    branch_text = {}   # (k, i, j) → grams
    common = {}        # k → grams (모든 경로 공통 대사)
    for k, (sc, succ, nodes) in info.items():
        cg = set()
        for i, (opts, flags) in nodes.items():
            g = grams(sc[i].get('text', ''))
            if opts:
                for d in opts: branch_text.setdefault((k, d[1], d[2]), set()).update(g)
            elif not flags: cg |= g
        for n in (events[k].get('cold') or []): cg |= grams(n.get('text', ''))   # 서먹한 결말은 따로라서 공통으로 쳐요(느슨하게)
        common[k] = cg
    for k2, (sc2, succ2, nodes2) in info.items():
        for i2, (opts2, flags2) in nodes2.items():
            t = sc2[i2].get('text', '')
            for ph in key_phrases(t):
                pg = grams(ph)
                if len(pg) < 3: continue
                com = set().union(*(common[k] for k in common if k < k2)) if k2 > 1 else set()
                # 같은 이벤트: 이 대사보다 앞의 공통 대사
                com_same = set()
                for i, (opts, flags) in info[k2][2].items():
                    if i < i2 and not opts and not flags: com_same |= grams(sc2[i].get('text', ''))
                if len(pg & (com | com_same)) / len(pg) >= .5: continue
                for (k, ci, oj), bg in branch_text.items():
                    if k > k2 or (k == k2 and ci >= i2): continue
                    if k == k2 and ('o', ci, oj) in opts2: continue   # 그 분기 안의 대사
                    if len(pg & bg) / len(pg) < BR: continue
                    sc = info[k][0]; fl = option_flag(sc, info[k][1], ci, oj)
                    guarded = any(f in fl and v for f, v in flags2)
                    # 다른 보기에도 같은 말이 있으면 분기 한정이 아님
                    sib = [bg2 for (kk, cc, jj), bg2 in branch_text.items() if kk == k and cc == ci and jj != oj]
                    if sib and all(len(pg & s) / len(pg) >= .5 for s in sib): continue
                    if guarded: continue
                    lab = sc[ci]['options'][oj].get('next', '?'); cid = sc[ci].get('id', '?')
                    warns.append(f'{npc} ♥{k2} #{i2}: 「{ph}」 ← ♥{k} {cid}/{lab} 분기에서만 나온 말 (플래그 {",".join(sorted(fl)) or "없음"}) → {t[:50]}')
                    break
    return warns

def cross_check(npc, events):
    """다른 NPC 진행 플래그 분기: 없을 때(else) 쪽에 대사가 있어야 해요"""
    errs = []
    for k, ev in events.items():
        sc = ev.get('script') or []; lab = {n['label']: i for i, n in enumerate(sc) if 'label' in n}
        for i, n in enumerate(sc):
            if n.get('cmd') != 'if_flag': continue
            m = re.fullmatch(r'([a-z]+)_h(\d+)', n.get('flag') or '')
            if not m or m.group(1) == npc: continue
            for side in ('then', 'else'):
                j = lab.get(n.get(side)); has = False
                while j is not None and j + 1 < len(sc):
                    j += 1; c = sc[j].get('cmd')
                    if c in ('line', 'narration', 'choice', 'if_flag', 'if_heart'): has = True; break   # 대사가 있거나, 다음 분기로 이어지면(중첩) 통과
                    if c == 'goto' or 'label' in sc[j]: break
                if not has: errs.append(f'{npc} ♥{k} #{i}: 다른 NPC 진행 플래그 {n["flag"]} 분기의 {"있을" if side == "then" else "없을"} 때 쪽에 대사가 없어요 (→ {n.get(side)})')
    return errs

def engine_check():
    """xxx_was_cold: 바로 앞 이벤트 결과만 남는지 (evFinish가 이벤트마다 cold를 새로 써요)"""
    s = open(os.path.join(ROOT, 'public', 'index.html'), encoding='utf-8').read(); errs = []
    if not re.search(r'st\.cold\s*=\s*!?!?ctx\.cold', s): errs.append('엔진: evFinish에서 이벤트마다 st.cold = ctx.cold로 서먹 플래그를 새로 정하지 않아요')
    if not re.search(r'_was_cold\$/\.exec\(f\); if \(c\) return !!me\.npc\?\.\[c\[1\]\]\?\.cold', s): errs.append('엔진: flagOn이 xxx_was_cold를 그 NPC의 마지막 이벤트 결과(st.cold)로 읽지 않아요')
    if not re.search(r'_h\(\\d\+\)\$/\.exec\(f\); if \(m\) return !!me\.npc\?\.\[m\[1\]\]\?\.seen', s): errs.append('엔진: xxx_hN 자동 플래그(본 이벤트)를 읽지 않아요')
    return errs
