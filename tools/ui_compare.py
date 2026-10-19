# 개선 전·후 스크린숏을 나란히 놓은 비교 페이지와 수치 표: python3 tools/ui_compare.py → audit/compare.html
import json, os, html
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'audit')
SIZES = [('phone', '휴대폰 390×844'), ('tablet', '태블릿 820×1180'), ('pc', 'PC 1440×900')]
KO = {'login': '로그인', 'world': '마을 맵', 'map': '지도', 'talk': '말하기', 'npc_talk': 'NPC 대화', 'heart_event': '하트 이벤트', 'story_vn': '이야기 장면', 'sheet_home': '오늘의 정보', 'sheet_lab': '물약 교실', 'sheet_green': '온실', 'sheet_ranch': '사육장', 'sheet_market': '시장',
      'sub_avatar': '캐릭터 꾸미기', 'sub_clothes': '옷 가게', 'sub_class': '수업', 'sub_dorm': '내 방', 'sub_fish': '낚시·채집', 'sub_games': '같이 놀기', 'sub_cook': '요리', 'sub_npcgift': 'NPC 선물', 'sub_npcstory': 'NPC 이야기', 'sub_bag': '가방', 'sub_profile': '내 정보', 'sub_rel': '관계', 'sub_journal': '일지', 'sub_menu': '메뉴', 'sub_settings': '설정'}
def load(p):
    try: return {(r['size'], r['screen']): r for r in json.load(open(p))}
    except Exception: return {}
B, A = load(os.path.join(R, 'before', 'metrics.json')), load(os.path.join(R, 'after', 'metrics.json'))
def cell(r, k):
    if not r: return '-'
    v = r.get(k)
    if k == 'innerScroll': return '-' if v is None else (f'{v[0]}/{v[1]}' if isinstance(v, list) else ('있음' if v else '없음'))
    if k == 'pageScroll': return '있음' if v else '없음'
    return str(v)
rows, imgs = [], []
screens = []
for s in list(KO):
    if any((z, s) in A or (z, s) in B for z, _ in SIZES): screens.append(s)
for s in screens:
    for z, zn in SIZES:
        b, a = B.get((z, s)), A.get((z, s))
        rows.append(f'<tr><td>{html.escape(KO.get(s, s))}</td><td>{zn.split()[0]}</td>' + ''.join(f'<td class="b">{cell(b, k)}</td><td class="a">{cell(a, k)}</td>' for k in ['pageScroll', 'innerScroll', 'small', 'contrast', 'touch']) + '</tr>')
    pics = ''.join(f'<figure><figcaption>{zn}</figcaption><div class="pair"><img src="before/{z}/{s}.png" alt="" loading="lazy"><img src="after/{z}/{s}.png" alt="" loading="lazy"></div></figure>' for z, zn in SIZES)
    imgs.append(f'<section><h2>{html.escape(KO.get(s, s))}</h2>{pics}</section>')
perf = ''
for nm, f in [('휴대폰', 'perf_phone.json'), ('PC', 'perf_pc.json')]:
    try:
        pb, pa = json.load(open(os.path.join(R, 'before', f))), json.load(open(os.path.join(R, 'after', f)))
        for cpu in ['cpu1', 'cpu4']:
            perf += f'<tr><td>{nm}</td><td>{cpu[3:]}배</td><td class="b">{pb[cpu]["walk"]["fps"]}</td><td class="a">{pa[cpu]["walk"]["fps"]}</td><td class="b">{pb[cpu]["walk"]["long"]}</td><td class="a">{pa[cpu]["walk"]["long"]}</td><td class="b">{pb[cpu]["ui"]["longMax"]}</td><td class="a">{pa[cpu]["ui"]["longMax"]}</td><td class="b">{pb[cpu]["ui"]["inputDelay"]}</td><td class="a">{pa[cpu]["ui"]["inputDelay"]}</td></tr>'
    except Exception: pass
lh = ''
for f, nm in [('lh_mobile.json', '모바일')]:
    try:
        lb, la = json.load(open(os.path.join(R, 'before', f))), json.load(open(os.path.join(R, 'after', f)))
        g = lambda d, k: round((d.get('categories', {}).get(k, {}).get('score') or 0) * 100)
        lh = f'<tr><td>Lighthouse {nm}</td><td class="b">성능 {g(lb, "performance")} · 접근성 {g(lb, "accessibility")}</td><td class="a">성능 {g(la, "performance")} · 접근성 {g(la, "accessibility")}</td></tr>'
    except Exception: pass
page = f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UI 개선 전·후 비교</title>
<style>body{{font-family:system-ui,sans-serif;background:#140D1E;color:#F6F0FF;margin:0;padding:20px}}h1,h2{{font-weight:600}}table{{border-collapse:collapse;font-size:13px;margin:12px 0 28px}}td,th{{border:1px solid #3A2A55;padding:4px 8px;text-align:center}}th{{background:#211733}}td.b{{color:#BDB0D6}}td.a{{color:#6FD08C;font-weight:600}}
.pair{{display:flex;gap:8px;align-items:flex-start;overflow-x:auto}}.pair img{{max-height:520px;border:1px solid #3A2A55;border-radius:8px;background:#000}}figure{{margin:0 0 16px}}figcaption{{font-size:13px;color:#BDB0D6;margin-bottom:4px}}section{{margin-bottom:36px}}.note{{color:#BDB0D6;font-size:13px}}</style>
<h1>호박달 마녀학교 UI 개선 전·후</h1><p class="note">왼쪽 전(회색) · 오른쪽 후(초록). 전: main 12b6084 · 후: ui-overhaul</p>
<h2>화면별 수치</h2><table><tr><th rowspan="2">화면</th><th rowspan="2">크기</th><th colspan="2">페이지 스크롤</th><th colspan="2">패널 안 스크롤(내용/보임)</th><th colspan="2">13px 미만 글씨</th><th colspan="2">대비 위반</th><th colspan="2">44px 미만 터치</th></tr><tr>{'<th>전</th><th>후</th>' * 5}</tr>{''.join(rows)}</table>
<h2>성능 (10초 걷기)</h2><table><tr><th>기기</th><th>CPU 감속</th><th colspan="2">평균 FPS</th><th colspan="2">걷기 중 긴 작업</th><th colspan="2">화면 열기 긴 작업 최대(ms)</th><th colspan="2">입력 지연 최대(ms)</th></tr><tr><th></th><th></th>{'<th>전</th><th>후</th>' * 4}</tr>{perf}</table>
<table><tr><th>항목</th><th>전</th><th>후</th></tr>{lh}</table>
<h2>스크린숏</h2>{''.join(imgs)}</html>'''
open(os.path.join(R, 'compare.html'), 'w').write(page); print('audit/compare.html', len(page) // 1024, 'KB', len(screens), '화면')
