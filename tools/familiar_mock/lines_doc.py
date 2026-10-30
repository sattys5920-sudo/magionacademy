# 사역마 대사 문서 만들기: python3 lines_doc.py → tools/familiar_mock/lines.html (12종 × 친밀도 5단계 × 상황)
import json, os, base64, io, html
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
IDS = ['vael','ixi','puck','lotis','sol','lune','ignis','rill','orbi','eon','nyx','iris']
SUB = ['푸른 혼불','보라 나선불','초록 도깨비불','분홍 연꽃불','금빛 햇무리불','은빛 달불','붉은 불기둥','청록 물결불','주황 고리불','남색 성운불','칠흑 그림자불','오로라 무지갯불']
MOOD = ['과묵','쌍둥이 장난꾸러기','능글맞은 도깨비','다정한 언니','오만한 고대의 왕','몽환적인 예언자','츤데레 다혈질','느긋한 잠꾸러기','호기심 많은 꼬마 학자','늙은 별의 현자','냉소적인 그림자','변덕쟁이 하이텐션']
COL = ['#5A8CFF','#A070FF','#40D070','#FF6AB8','#FFC838','#C8D8FF','#FF5A28','#30D8C8','#FF9030','#7088FF','#9A60F0','#E0C8FF']
LIKE = ['달빛 이슬, 은방울꽃, 눈송이 꽃, 월하향, 영혼 연꽃, 마나석','라벤더, 나팔꽃, 속삭임 덩굴, 꿈꽃, 거울 잎, 별가루','도토리, 네잎클로버, 황금 버섯, 요정 버섯, 반딧불 꽃가루, 이끼','들장미 꽃잎, 연꽃 씨, 카모마일, 벌꿀, 수정 장미, 딸기','해바라기 씨, 해님 호박, 황금 버섯, 별사과, 밀 이삭, 혜성 씨앗','달맞이꽃, 달빛 이슬, 월하향, 서리 딸기, 꿈 조각, 유리 열매','고추, 화룡초, 생강, 번개 콩, 마나석, 해님 호박','바다 포도, 연꽃 씨, 알로에, 선인장 즙, 박하 잎, 구름 목화','시간의 꽃, 노래하는 종꽃, 무지개 콩, 옥수수, 단풍잎, 토마토','혜성 씨앗, 별가루, 별사과, 소원 민들레, 반딧불 꽃가루, 등불 조각','그림자 버섯, 광대버섯, 속삭임 덩굴, 거울 잎, 보라 버섯, 꿈 조각','오로라 꽃잎, 무지개 콩, 수정 장미, 블루베리, 소원 민들레, 유리 열매']
HATE = ['고추, 화룡초','생강, 솔잎','박하 잎, 알로에','광대버섯, 그림자 버섯','이끼, 그림자 버섯','해바라기 씨, 고추','눈송이 꽃, 서리 딸기','화룡초, 고추','이끼, 보라 버섯','당근, 완두콩','해님 호박, 들장미 꽃잎','날마다 바뀜']
STN = ['경계','관심','익숙','신뢰','맹약']
SIT = [('greet','접속·불러냈을 때'),('idle','걷는 중'),('still','가만히 서 있을 때'),('gather','낚시·채집'),('explore','탐사·전투'),('night','밤'),('weather','비·눈·안개')]
GT = [('want','오늘 원하던 것'),('like','좋아하는 것'),('meh','그 밖의 것'),('hate','싫어하는 것')]
TIER = ['경계~관심','익숙~신뢰','맹약']
sheet = Image.open(os.path.join(HERE, '..', 'iso', 'out', 'wisps3.png')).convert('RGBA')
def img(i):
    b = io.BytesIO(); sheet.crop((i * 64, 0, i * 64 + 64, 64)).save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
e = html.escape
tabs, secs = [], []
for k, sid in enumerate(IDS):
    d = json.load(open(os.path.join(HERE, 'lines', sid + '.json')))
    tabs.append(f'<button data-t="{k}" style="--c:{COL[k]}"><img src="{img(k)}">{e(d["name"])}</button>')
    rows = ''.join(f'<tr><th>{lab}</th>' + ''.join('<td>' + ('<br>'.join(e(x) for x in d[key][s]) if key == 'idle' else e(d[key][s])) + '</td>' for s in range(5)) + '</tr>' for key, lab in SIT)
    gift = ''.join(f'<tr><th>{lab}</th>' + ''.join(f'<td>{e(d["gift"][key][t])}</td>' for t in range(3)) + '</tr>' for key, lab in GT)
    hint = '<tr><th>원하는 것 암시</th>' + ''.join(f'<td>{e(d["hint"][t]).replace("{item}", "<mark>{재료}</mark>")}</td>' for t in range(3)) + '</tr>'
    lv = ''.join(f'<tr><th>→ {STN[s + 1]}</th><td>{e(d["levelup"][s])}</td></tr>' for s in range(4))
    secs.append(f'''<section data-s="{k}" style="--c:{COL[k]}"><div class="hd"><img src="{img(k)}"><div><h2>{e(d["name"])} <small>{SUB[k]}</small></h2><p class="mood">{MOOD[k]}</p>
<p><b>좋아함</b> {LIKE[k]}</p><p><b>싫어함</b> {HATE[k]}</p></div></div>
<h3>상황별 대사 (친밀도 단계별)</h3><div class="sc"><table class="m"><tr><th></th>{''.join(f'<th>{n}</th>' for n in STN)}</tr>{rows}</table></div>
<h3>선물 반응 · 암시</h3><div class="sc"><table class="m g"><tr><th></th>{''.join(f'<th>{n}</th>' for n in TIER)}</tr>{hint}{gift}</table></div>
<h3>단계가 오를 때</h3><table class="m l">{lv}</table></section>''')
doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>사역마 대사집</title>
<style>
:root{{--bg:#120C1E;--pn:#1E1530;--ln:#3A2C58;--tx:#EDE6FA;--mu:#A898C8}}
body{{margin:0;background:var(--bg);color:var(--tx);font:15px/1.6 Pretendard,system-ui,sans-serif}}
header{{padding:20px 16px 8px;max-width:1100px;margin:auto}} h1{{margin:0 0 6px;font-size:22px;color:#FFE9A0}} header p{{margin:4px 0;color:var(--mu);font-size:14px}}
.rule{{max-width:1100px;margin:8px auto;padding:0 16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px}}
.rule div{{background:var(--pn);border:1px solid var(--ln);border-radius:10px;padding:10px 12px;font-size:14px}} .rule b{{color:#FFE9A0}}
nav{{position:sticky;top:0;z-index:2;background:var(--bg);padding:8px 16px;display:flex;gap:6px;overflow-x:auto;max-width:1100px;margin:auto}}
nav button{{flex:none;display:flex;align-items:center;gap:4px;padding:4px 10px 4px 4px;border-radius:20px;border:1px solid var(--ln);background:var(--pn);color:var(--tx);font:inherit;cursor:pointer}}
nav button img{{width:28px;height:28px;image-rendering:pixelated}} nav button.on{{border-color:var(--c);box-shadow:0 0 8px var(--c)}}
section{{display:none;max-width:1100px;margin:auto;padding:8px 16px 40px}} section.on{{display:block}}
.hd{{display:flex;gap:14px;align-items:center;background:var(--pn);border:1px solid var(--ln);border-radius:14px;padding:12px}}
.hd img{{width:112px;height:112px;image-rendering:pixelated;flex:none;filter:drop-shadow(0 0 10px var(--c))}}
h2{{margin:0;color:var(--c)}} h2 small{{font-size:14px;color:var(--mu);font-weight:400}} .mood{{margin:2px 0 6px;font-weight:700}} .hd p{{margin:2px 0;font-size:14px}} .hd b{{color:var(--mu);margin-right:6px}}
h3{{font-size:16px;margin:20px 0 8px;color:#FFE9A0}}
.sc{{overflow-x:auto}} table.m{{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}} table.g{{min-width:560px}} table.l{{min-width:0}}
.m th,.m td{{border:1px solid var(--ln);padding:8px;vertical-align:top;text-align:left}} .m tr:first-child th{{background:#2A1E40;color:var(--c)}} .m th{{background:#1A1228;color:var(--mu);font-weight:600;white-space:nowrap}}
mark{{background:none;color:var(--c);font-weight:700}}
</style></head><body>
<header><h1>사역마 대사집 · 정령불 12종</h1><p>정령이 혼자 말을 걸어요(플레이어는 대답하지 않아요). 친밀도가 오를수록 말투가 풀리지만 성격은 그대로예요. 모두 {12 * 59}줄.</p></header>
<div class="rule"><div><b>친밀도</b><br>경계 0 → 관심 120 → 익숙 400 → 신뢰 900 → 맹약 1800</div><div><b>선물(하루 5번)</b><br>오늘 원하던 것 +25 · 좋아하는 것 +8 · 그 밖 +1 · 싫어하는 것 −10</div><div><b>공물</b><br>익숙: 귀한 것 3개 · 신뢰: 꿈 조각 5 + 별가루 5 · 맹약: 정령마다 아주 귀한 재료 1개</div><div><b>원하는 것</b><br>좋아하는 것 6개 중 날마다 하나. 화면에 표시하지 않고 대사로만 암시해요</div></div>
<nav>{''.join(tabs)}</nav>{''.join(secs)}
<script>const B=[...document.querySelectorAll('nav button')],S=[...document.querySelectorAll('section')];function go(k){{B.forEach((b,i)=>b.classList.toggle('on',i==k));S.forEach((s,i)=>s.classList.toggle('on',i==k));}}B.forEach(b=>b.onclick=()=>go(+b.dataset.t));go(0);</script>
</body></html>'''
open(os.path.join(HERE, 'lines.html'), 'w').write(doc); print('ok')
