# NPC 하트 이벤트 대사·선택지 전문을 한 장짜리 HTML 문서로: python3 tools/npc_story_doc.py <출력.html>
import json, os, sys, html, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, 'public', 'data', 'npc')
NPCS = [('nabi', '나비', '매점 고양이'), ('batri', '배트리', '우체부 박쥐'), ('kappa', '캇파', '낚시꾼 갓파'), ('aula', '아울라', '사서 부엉이'), ('mandi', '맨디', '정원사 맨드레이크'),
        ('jipsin', '짚신', '꼬마 허수아비'), ('sera', '세라', '양호 선생님'), ('madeleine', '마들렌', '과자 교실 제빵사'), ('stella', '스텔라', '점성술사'), ('leo', '레오', '사육장 관리인')]
NAME = {i: n for i, n, _ in NPCS}
PLACES = {p['id']: p['name'] for p in json.load(open(os.path.join(D, 'places.json')))}
CAST = json.load(open(os.path.join(D, 'cast.json')))
ITEMS = json.load(open(os.path.join(ROOT, 'tools', 'npc_items.json')))
T = {'morning': '아침', 'day': '낮', 'evening': '저녁', 'night': '밤'}
W = {'clear': '맑음', 'rain': '비', 'fog': '안개', 'snow': '눈', 'storm': '폭풍우'}
VARS = {'player': '주인공', 'sera.name': '세라', 'madeleine.name': '마들렌', 'stella.name': '스텔라', 'leo.name': '레오', 'sera.husband': '루카스', 'npc.husband': '루카스'}
e = lambda s: html.escape(str(s), quote=False)

def fill(t, npc):
    def r(m):
        k = m.group(1)
        if k == 'npc.name': k = npc + '.name'
        v = VARS.get(k, NAME.get(k.split('.')[0], k) if k.endswith('.name') else k)
        return f'\x00{v}\x01'
    s = e(re.sub(r'\{([a-z_.]+)\}', r, t))
    return s.replace('\x00', '<b class="v">').replace('\x01', '</b>')

def who_name(w, npc, cast):
    if w == 'player': return '주인공'
    if w in NAME: return NAME[w]
    c = cast.get(w) or CAST.get(w) or {}
    return re.sub(r'<[^>]+>', '', fill(c.get('name', w), npc))

def place(p, npc): return re.sub(r'<[^>]+>', '', fill(PLACES.get(p, p), npc))

def cond_text(c, npc):
    out = [f'♥{c.get("minHeart")}', place(c.get('location'), npc)]
    if c.get('time'): out.append('·'.join(T[x] for x in c['time']))
    if c.get('weather'): out.append('·'.join(W[x] for x in c['weather']))
    if c.get('festival'): out.append('호박달 축제')
    elif c.get('moon'): out.append('보름')
    if c.get('afterDays'): out.append(f'앞 이벤트 {c["afterDays"]} 일 뒤')
    if c.get('after'): out.append('먼저 볼 것: ' + ', '.join(f'{NAME.get(a.split(":")[0])} ♥{a.split(":")[1]}' for a in c['after']))
    if c.get('hidden'): out.append(f'숨바꼭질 {c["hidden"].get("days", 3)} 일')
    return ' · '.join(out)

def reward_text(r):
    out = []
    if r.get('coin'): out.append(f'{r["coin"]}G')
    if r.get('mana'): out.append(f'마력 {r["mana"]}')
    if r.get('know'): out.append(f'지식 {r["know"]}')
    for k, n in (r.get('items') or {}).items(): out.append(f'{ITEMS.get(k, k)} ×{n}')
    pk = r.get('perk'); pk = [] if not pk else pk if isinstance(pk, list) else [pk]
    out += [f'특별 보상: {p}' for p in pk]
    return ', '.join(out) or '없음'

def aff(v): return f'<span class="aff {"up" if v > 0 else "down" if v < 0 else "keep"}">{"+" if v > 0 else ""}{v}</span>'

def render(sc, npc, cast):
    o = []
    for n in sc:
        c = n.get('cmd')
        if c is None and 'label' in n:
            o.append(f'<div class="lab" id="{npc}-{e(n["label"])}">▸ {e(n["label"])}</div>'); continue
        if c == 'line':
            o.append(f'<p class="ln{" me" if n["who"] == "player" else ""}"><span class="who">{e(who_name(n["who"], npc, cast))}</span><span class="tx">{fill(n.get("text", ""), npc)}</span></p>')
        elif c == 'narration': o.append(f'<p class="nar">{fill(n.get("text", ""), npc)}</p>')
        elif c == 'choice':
            ops = ''.join(f'<li>{aff(op.get("affinity", 0))}<span class="otx">{fill(op.get("text", ""), npc)}</span><span class="nx">→ {e(op.get("next", ""))}{f" · 플래그 <code>{e(op["flag"])}</code>" if op.get("flag") else ""}</span></li>' for op in n.get('options', []))
            o.append(f'<div class="ch"><div class="chh">선택지</div><ol>{ops}</ol></div>')
        elif c == 'goto': o.append(f'<div class="sys">↪ {e(n.get("to"))}(으)로</div>')
        elif c == 'if_flag': o.append(f'<div class="sys br">분기: 플래그 <code>{e(n["flag"])}</code> 있으면 → {e(n.get("then"))} / 없으면 → {e(n.get("else"))}</div>')
        elif c == 'if_heart': o.append(f'<div class="sys br">분기: {NAME.get(n.get("npc") or npc)} ♥{n.get("min")} 이상이면 → {e(n.get("then"))} / 아니면 → {e(n.get("else"))}</div>')
        elif c in ('move', 'follow'):
            extra = ' · '.join(x for x in [T.get(n.get('time'), ''), W.get(n.get('weather'), '')] if x)
            lead = f'{who_name(n["who"], npc, cast)}을(를) 따라 ' if c == 'follow' else ''
            o.append(f'<div class="scene">📍 {lead}{e(place(n.get("to"), npc))}{f" ({extra})" if extra else ""}</div>')
        elif c == 'give_item': o.append(f'<div class="sys">🎁 {e(ITEMS.get(n.get("item"), n.get("item")))} ×{n.get("n", 1)} 받음</div>')
        elif c == 'take_item': o.append(f'<div class="sys">{e(ITEMS.get(n.get("item"), n.get("item")))} ×{n.get("n", 1)} 건넴</div>')
        elif c == 'set_flag': o.append(f'<div class="sys">플래그 <code>{e(n.get("flag"))}</code> 켜짐</div>')
        elif c == 'affinity': o.append(f'<div class="sys">호감도 {aff(n.get("value", 0))}</div>')
    return '\n'.join(o)

def main(out):
    toc, body, total_ev, total_ln = [], [], 0, 0
    for npc, nm, title in NPCS:
        d = os.path.join(D, npc); evs = []
        for k in range(1, 11):
            f = os.path.join(d, 'events', f'heart_{k:02d}.json')
            if os.path.exists(f):
                try: evs.append(json.load(open(f)))
                except Exception: pass
        prof = json.load(open(os.path.join(d, 'profile.json'))) if os.path.exists(os.path.join(d, 'profile.json')) else {}
        cast = prof.get('cast') or {}
        toc.append(f'<li><a href="#{npc}">{nm}</a> <span class="cnt">{len(evs)}/10</span></li>')
        sec = [f'<section class="npc" id="{npc}"><header class="nh"><h2>{nm}</h2><span class="nt">{e(title)}</span></header>']
        sec.append('<nav class="evtoc">' + ''.join(f'<a href="#{npc}-h{ev["heart"]}">♥{ev["heart"]} {e(ev.get("title", ""))}</a>' for ev in evs) + '</nav>')
        for ev in evs:
            k = ev['heart']; lines = sum(1 for n in ev.get('script', []) if n.get('cmd') in ('line', 'narration'))
            total_ev += 1; total_ln += lines
            flags = sorted({op['flag'] for n in ev.get('script', []) if n.get('cmd') == 'choice' for op in n.get('options', []) if op.get('flag')} | {n['flag'] for n in ev.get('script', []) if n.get('cmd') == 'set_flag'})
            sec.append(f'<article class="ev" id="{npc}-h{k}"><header><span class="hk">♥{k}</span><h3>{fill(ev.get("title", ""), npc)}</h3></header>'
                       f'<dl class="meta"><div><dt>열리는 조건</dt><dd>{e(cond_text(ev.get("conditions", {}), npc))}</dd></div><div><dt>보상</dt><dd>{e(reward_text(ev.get("rewards") or {}))}</dd></div>'
                       f'{f"<div><dt>남기는 플래그</dt><dd>{chr(32).join(f"<code>{e(x)}</code>" for x in flags)}</dd></div>" if flags else ""}<div><dt>대사</dt><dd>{lines} 줄(모든 분기 포함)</dd></div></dl>'
                       f'<div class="script">{render(ev.get("script", []), npc, cast)}</div>')
            if ev.get('cold'): sec.append(f'<div class="cold"><div class="ch2">서먹한 결말 (이벤트 안 호감도 합이 −30 이하면 「ending」부터 이걸로 끝나요)</div>{render(ev["cold"], npc, cast)}</div>')
            if ev.get('fail'): sec.append(f'<div class="cold"><div class="ch2">찾지 못했을 때 (3 일 안에 못 찾으면)</div>{render(ev["fail"], npc, cast)}</div>')
            sec.append('</article>')
        if len(evs) < 10: sec.append(f'<p class="wip">아직 쓰는 중이에요 ({len(evs)}/10).</p>')
        sec.append('</section>'); body.append('\n'.join(sec))
    tpl = open(os.path.join(ROOT, 'tools', 'npc_story_doc.tpl.html')).read()
    page = tpl.replace('%%TOC%%', '\n'.join(toc)).replace('%%BODY%%', '\n'.join(body)).replace('%%SUM%%', f'이벤트 {total_ev} 개 · 대사와 지문 {total_ln:,} 줄')
    open(out, 'w').write(page); print(out, len(page) // 1024, 'KB', total_ev, total_ln)

if __name__ == '__main__': main(sys.argv[1])
