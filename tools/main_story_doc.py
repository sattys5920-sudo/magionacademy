# 메인 의뢰 대본 전문을 한 장짜리 HTML 문서로: python3 tools/main_story_doc.py <출력.html>
#   목차 · 의뢰인별 단계별 부탁·완료 장면 · 분기(모든 갈래) · 반복 대사 · 서브 NPC 조건부 장면 표시 · 목표·보상
import json, os, sys, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from josa import VAR as JVAR, pick as jpick
import npc_story_doc as ND
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, 'public', 'data', 'main'); ND_D = os.path.join(ROOT, 'public', 'data', 'npc')
IDX = json.load(open(os.path.join(D, 'index.json'))); QUESTS = IDX['quests'] if isinstance(IDX, dict) else IDX
CAST = {**json.load(open(os.path.join(ND_D, 'cast.json'))), **json.load(open(os.path.join(D, 'cast.json')))}
PLACES = {p['id']: p['name'] for p in json.load(open(os.path.join(ND_D, 'places.json')))}
PLACES.update({p['id']: p['name'] for p in json.load(open(os.path.join(D, 'places.json')))})
ITEMS = dict(json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json'))))
T, W = ND.T, ND.W; e = ND.e
NAME = dict(ND.NAME)
VARS = dict(ND.VARS)
OBJ_KO = {'collect': '모으기', 'craft': '만들기', 'deliver': '전하기', 'visit': '가기', 'talk': '이야기하기', 'clue': '단서 찾기', 'puzzle': '퍼즐', 'wait_moon': '달 기다리기', 'defend': '지키기', 'choice': '선택'}
MOON = {'full': '보름', 'new': '그믐'}
def load_items():
    s = open(os.path.join(ROOT, 'public', 'index.html'), encoding='utf-8').read(); i = s.find('const ITEM = {'); j = s.find('};', i)
    for m in re.finditer(r"\b([a-z][a-z0-9_]*): *'([^']*)'", s[i:j]): ITEMS.setdefault(m.group(1), m.group(2))
load_items()
for q in QUESTS:
    try: d = json.load(open(os.path.join(D, q, 'quest.json')))
    except Exception: continue
    for k, v in (d.get('items') or {}).items(): ITEMS[k] = v.get('name', k)
    for k, v in (d.get('cast') or {}).items(): CAST.setdefault(k, v)
for k, v in CAST.items():
    if k not in NAME: NAME[k] = re.sub(r'\{[^}]*\}', '', v.get('name', k)) or k
NAME['yeoreum'] = '유령(여름)'; NAME['piece'] = '조각(프랭)'

def fill(t):
    def r(m):
        k = m.group(1); v = VARS.get(k, NAME.get(k.split('.')[0], k) if k.endswith('.name') else k)
        j = jpick(v, m.group(2), m.group(3)) if m.group(2) is not None else ''
        return f'\x00{v}\x01{j}'
    return e(JVAR.sub(r, t)).replace('\x00', '<b class="v">').replace('\x01', '</b>')
def who_name(w):
    if w == 'player': return '민준(주인공)'
    if w == 'voice': return '목소리'
    return re.sub(r'<[^>]+>', '', fill(CAST.get(w, {}).get('name', NAME.get(w, w))))
def place(p): return re.sub(r'<[^>]+>', '', fill(PLACES.get(p, p or '')))

def render(sc, qid, n, kind):
    o = []; pre = f'{qid}-{n}{kind[0]}'
    for s in sc:
        c = s.get('cmd')
        if c is None and 'label' in s: o.append(f'<div class="lab" id="{pre}-{e(s["label"])}">▸ {e(s["label"])}</div>'); continue
        if c == 'line': o.append(f'<p class="ln{" me" if s.get("who") == "player" else ""}"><span class="who">{e(who_name(s.get("who", "")))}</span><span class="tx">{fill(re.sub(r"^\[(기본|웃음|화남|놀람|부끄러움)\]\s*", "", s.get("text", "")))}</span></p>')
        elif c == 'narration': o.append(f'<p class="nar">{fill(s.get("text", ""))}</p>')
        elif c == 'choice':
            ops = ''.join(f'<li><span class="otx">{fill(op.get("text", ""))}</span>{f"<span class=fl> ▶ 결말 플래그 <code>{e(op[chr(102)+chr(108)+chr(97)+chr(103)])}</code></span>" if op.get("flag") else ""}{f"<span class=cf>확인 창: {fill(op[chr(99)+chr(111)+chr(110)+chr(102)+chr(105)+chr(114)+chr(109)])}</span>" if op.get("confirm") else ""}<span class="nx">→ {e(op.get("next", "다음"))}</span></li>' for op in s.get('options') or [])
            o.append(f'<div class="ch"><div class="chh">선택지</div><ol>{ops}</ol></div>')
        elif c == 'goto': o.append(f'<div class="sys">↪ 「{e(s.get("to"))}」 로</div>')
        elif c == 'if_flag': o.append(f'<div class="sys br">분기: 플래그 <code>{e(s.get("flag"))}</code> 있으면 → {e(s.get("then"))} / 없으면 → {e(s.get("else"))}</div>')
        elif c == 'if_heart': o.append(f'<div class="sys br sub">서브 NPC 조건: {e(NAME.get(s.get("npc"), s.get("npc")))} ♥{s.get("min")} 이상 → {e(s.get("then"))} / 아니면 → {e(s.get("else"))}</div>')
        elif c == 'if_quest': o.append(f'<div class="sys br">분기: 의뢰 {e(s.get("quest"))} 끝냈으면 → {e(s.get("then"))} / 아니면 → {e(s.get("else"))}</div>')
        elif c == 'if_item': o.append(f'<div class="sys br">분기: {e(ITEMS.get(s.get("item"), s.get("item")))} 있으면 → {e(s.get("then"))} / 없으면 → {e(s.get("else"))}</div>')
        elif c in ('move', 'follow'):
            extra = ' · '.join(x for x in [T.get(s.get('time'), ''), W.get(s.get('weather'), '')] if x); wn = who_name(s.get('who', '')) if c == 'follow' else ''
            o.append(f'<div class="scene">📍 {(wn + jpick(wn, "을", "를") + " 따라 ") if wn else ""}{e(place(s.get("to")))}{f" ({extra})" if extra else ""}</div>')
        elif c == 'give_item': o.append(f'<div class="sys">🎁 {e(ITEMS.get(s.get("item"), s.get("item")))} ×{s.get("n", 1)} 받음</div>')
        elif c == 'take_item': o.append(f'<div class="sys">{e(ITEMS.get(s.get("item"), s.get("item")))} ×{s.get("n", 1)} 건넴</div>')
        elif c == 'set_flag': o.append(f'<div class="fl">▶ 플래그: <code>{e(s.get("flag"))}</code></div>')
        elif c == 'input': o.append(f'<div class="sys">✍ 이름 짓기 ({e(s.get("key"))}, 기본값 「{e(s.get("default", ""))}」)</div>')
        elif c == 'rename': o.append(f'<div class="sys">✨ {e(NAME.get(s.get("who"), s.get("who")))} → 「{e(s.get("name"))}」</div>')
    return '\n'.join(o)

def arrival_html(arr):
    if not arr: return ''
    rows = []
    for c in arr:
        k = c.get('cmd')
        if k == 'say': rows.append(f'<li>💬 {e(who_name(c.get("who")))}: {fill(c.get("text", ""))}</li>')
        elif k == 'spawn': rows.append(f'<li>{e(who_name(c.get("who")))} 등장 ({c.get("x")}, {c.get("y")})</li>')
        elif k == 'walk': rows.append(f'<li>{e(who_name(c.get("who")))} 이동 → ({c.get("x")}, {c.get("y")})</li>')
        elif k == 'crowd': rows.append(f'<li>구경꾼 {c.get("n", 4)} 명: {dict(scream="비명", flee="도망", watch="구경")[c.get("react", "watch")]}{(" 「" + fill(c["text"]) + "」") if c.get("text") else ""}</li>')
        elif k == 'fx': rows.append(f'<li>효과: {e(c.get("kind"))}</li>')
        elif k == 'fade' and c.get('text'): rows.append(f'<li>자막: {fill(c["text"])}</li>')
    return f'<div class="cut"><div class="ch2">맵 컷신 (등장 연출)</div><ol>{"".join(rows)}</ol></div>'

def obj_text(o):
    t = o.get('type')
    if t == 'collect': return f'{ITEMS.get(o.get("item"), o.get("item"))} {o.get("count")}개 모으기' + (f' ({place(o["source"].get("place"))}에서 {"사기" if o["source"].get("price") else "줍기"})' if o.get('source') else '')
    if t == 'craft': return f'{ITEMS.get(o.get("item"), o.get("item"))} {o.get("count", 1)}개 만들기' + (f' (품질 {dict(normal="보통", good="좋음", best="최고")[o["quality"]]} 이상)' if o.get('quality') else '')
    if t == 'deliver': return f'{NAME.get(o.get("to"), o.get("to"))}에게 {ITEMS.get(o.get("item"), o.get("item"))} {o.get("count", 1)}개 전하기'
    if t == 'visit': return f'{place(o.get("place"))}에 가기' + (' · ' + '·'.join(T[x] for x in o['time']) if o.get('time') else '') + (' · ' + '·'.join(W[x] for x in o['weather']) if o.get('weather') else '') + (f' · {MOON[o["moon"]]}' if o.get('moon') else '')
    if t == 'talk': return f'{NAME.get(o.get("who"), o.get("who"))}{jpick(NAME.get(o.get("who"), o.get("who")), "과", "와")} 이야기하기'
    if t == 'clue': return f'{o.get("text", "단서")} {o.get("count") or len(o.get("spots") or [])}개 찾기: ' + ' · '.join(place(sp.get('place')) for sp in o.get('spots') or [])
    if t == 'puzzle': return o.get('title') or ('별자리 잇기' if o.get('kind') == 'stars' else '순서 맞추기')
    if t == 'wait_moon': return f'{MOON.get(o.get("moon"), o.get("moon"))}까지 기다리기'
    if t == 'defend': return o.get('text') or '등불 지키기'
    if t == 'choice': return o.get('text') or '결말 선택' + ' (' + ' / '.join(o.get('flags') or []) + ')'
    return t

def reward_text(r):
    out = []
    if r.get('gold'): out.append(f'{r["gold"]}G')
    if r.get('mana'): out.append(f'마력 {r["mana"]}')
    if r.get('know'): out.append(f'지식 {r["know"]}')
    for it in r.get('items') or []: k = it if isinstance(it, str) else it.get('id'); out.append(ITEMS.get(k, k))
    return ', '.join(out) or '없음'

def main(out):
    toc, body, total_sc, total_ln = [], [], 0, 0
    for qid in QUESTS:
        d = os.path.join(D, qid)
        try: q = json.load(open(os.path.join(d, 'quest.json')))
        except Exception: continue
        cl = q.get('client'); cn = NAME.get(cl, cl); title = CAST.get(cl, {}).get('title', '')
        toc.append(f'<li><a href="#{qid}">{q.get("order")}. {e(q.get("name", ""))}</a> <span class="cnt">{e(cn)}</span></li>')
        sec = [f'<section class="npc" id="{qid}"><header class="nh"><h2>{q.get("order")}. {e(q.get("name", ""))}</h2><span class="nt">{e(cn)} · {e(title)}</span></header>']
        u = q.get('unlock') or {}
        sec.append(f'<dl class="meta"><div><dt>열리는 때</dt><dd>{"처음부터" if not u.get("afterQuest") else f"{e(u['afterQuest'])} 를 끝내고 {u.get('daysAfter', 0)} 일 뒤 아침"}{" · 호박달 축제가 지난 뒤" if u.get("afterFestival") else ""}</dd></div><div><dt>완료 보상</dt><dd>{e(reward_text(q.get("completion_reward") or {}))}</dd></div><div><dt>결말 플래그</dt><dd>{" / ".join(f"<code>{e(f)}</code>" for f in q.get("ending_flags") or [])}</dd></div></dl>')
        sec.append('<nav class="evtoc">' + ''.join(f'<a href="#{qid}-{st["n"]}">{st["n"]}단계 {e(st.get("title", ""))}</a>' for st in q.get('stages') or []) + '</nav>')
        try: idle = json.load(open(os.path.join(d, 'idle.json')))
        except Exception: idle = {}
        for st in q.get('stages') or []:
            n = st['n']
            sec.append(f'<article class="ev" id="{qid}-{n}"><header><span class="hk">{n}단계</span><h3>{e(st.get("title", ""))}</h3></header>'
                       f'<dl class="meta"><div><dt>목표</dt><dd>{" · ".join(e(obj_text(o)) for o in st.get("objectives") or [])}</dd></div><div><dt>단계 보상</dt><dd>{e(reward_text(st.get("rewards") or {}))}</dd></div>'
                       f'{f"<div><dt>기한</dt><dd>{st['deadline']} 일</dd></div>" if st.get("deadline") else ""}</dl>')
            for kind, kn in (('request', '부탁 장면'), ('complete', '완료 장면')):
                try: sc = json.load(open(os.path.join(d, f'stage_{n}_{kind}.json')))
                except Exception: sec.append(f'<p class="wip">{kn}: 아직 없어요</p>'); continue
                lines = sum(1 for s in sc.get('script', []) if s.get('cmd') in ('line', 'narration')); total_sc += 1; total_ln += lines
                scn = sc.get('scene') or {}
                sec.append(f'<div class="stage"><h4>{kn} 「{fill(sc.get("title", ""))}」 <span class="cnt">{lines} 줄</span> <span class="where">{e(place(scn.get("location")))}{(" · " + T.get(scn.get("time"), "")) if scn.get("time") else ""}{(" · " + W.get(scn.get("weather"), "")) if scn.get("weather") else ""}</span></h4>'
                           f'{arrival_html(sc.get("arrival")) if kind == "request" else ""}<div class="script">{render(sc.get("script", []), qid, n, kind)}</div></div>')
            idl = idle.get(str(n)) or {}
            sec.append('<div class="cold"><div class="ch2">반복 대사</div>' + ''.join(f'<p class="nar"><b>{lab}</b> {fill(" ".join(idl.get(k) or []))}</p>' for k, lab in (('a', '(가) 목표 진행 중'), ('b', '(나) 보고 전'), ('c', '(다) 다음 단계 전'))) + '</div>')
            sec.append('</article>')
        if idle.get('done'): sec.append(f'<div class="cold"><div class="ch2">의뢰 완료 후 반복 대사</div><p class="nar">{fill(" ".join(idle["done"]))}</p></div>')
        sec.append('</section>'); body.append('\n'.join(sec))
    tpl = open(os.path.join(ROOT, 'tools', 'npc_story_doc.tpl.html')).read()
    tpl = tpl.replace('호박달 하트 이야기 대본', '호박달 일곱 등불의 의뢰 대본').replace('서브 NPC 10명의 ♥1~♥10 하트 이벤트 대사·지문·선택지 전문', '메인 의뢰 7 개 × 5 단계의 부탁·완료 장면, 등장 컷신, 반복 대사, 선택지 전문')
    extra_css = '<style>.cut{margin:8px 0;padding:8px 12px;border:1px dashed #8a7cb0;border-radius:8px;font-size:13px}.cut ol{margin:4px 0 0 18px;padding:0}.stage h4{margin:18px 0 6px;font-size:15px}.stage .where{font-weight:normal;color:#8a7cb0;font-size:12px}.sys.sub{background:#f3e9ff}.cf{display:block;font-size:12px;color:#8a5a2a}</style></head>'
    page = tpl.replace('</head>', extra_css, 1).replace('%%TOC%%', '\n'.join(toc)).replace('%%BODY%%', '\n'.join(body)).replace('%%FIX%%', '').replace('%%SUM%%', f'장면 {total_sc} 개 · 대사와 지문 {total_ln:,} 줄')
    open(out, 'w').write(page); print(out, len(page) // 1024, 'KB', total_sc, total_ln)

if __name__ == '__main__': main(sys.argv[1])
