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
GT = [('like','좋아하는 것'),('meh','보통인 것'),('hate','싫어하는 것')]
TIER = ['경계~관심','익숙~신뢰','맹약']
sheet = Image.open(os.path.join(HERE, '..', 'iso', 'out', 'wisps3.png')).convert('RGBA')
def img(i):
    b = io.BytesIO(); sheet.crop((i * 64, 0, i * 64 + 64, 64)).save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
e = html.escape
tabs, secs = [], []
def count(x): return 1 if isinstance(x, str) else sum(count(y) for y in (x.values() if isinstance(x, dict) else x))
TOTAL = 0
for k, sid in enumerate(IDS):
    d = json.load(open(os.path.join(HERE, 'lines', sid + '.json'))); TOTAL += count({k: v for k, v in d.items() if k not in ('id', 'name')})
    tabs.append(f'<a href="#s{k}" style="--c:{COL[k]}"><img src="{img(k)}">{e(d["name"])}</a>')
    def blk(lab, items):   # 상황 하나: 단계별 줄을 세로로
        return f'<div class="bk"><h4>{lab}</h4>' + ''.join(f'<p><span class="st">{n}</span><span class="tx">{t}</span></p>' for n, t in items) + '</div>'
    sit = ''.join(blk(lab, [(STN[s], '<br>'.join(e(x) for x in d[key][s]) if key == 'idle' else e(d[key][s])) for s in range(5)]) for key, lab in SIT)
    hint = '<div class="bk"><h4>좋아하는 것을 은근히 (평소 대사에 섞여 나와요)</h4>' + ''.join(f'<p><span class="st it">{e(k)}</span><span class="tx">{e(v)}</span></p>' for k, v in d['hint'].items()) + '</div>'
    gift = ''.join(blk('선물: ' + lab, [(TIER[t], '<br>'.join(e(x) for x in d['gift'][key][t])) for t in range(3)]) for key, lab in GT)
    lv = blk('단계가 오를 때', [('→ ' + STN[s + 1], e(d['levelup'][s])) for s in range(4)])
    secs.append(f'''<section id="s{k}" style="--c:{COL[k]}"><div class="hd"><img src="{img(k)}"><div><h2>{e(d["name"])} <small>{SUB[k]}</small></h2><p class="mood">{MOOD[k]}</p>
<p><b>좋아함</b> {LIKE[k]}</p><p><b>싫어함</b> {HATE[k]}</p></div></div>
<h3>상황별 대사</h3><div class="gr">{sit}</div><h3>은근한 힌트 · 선물 반응</h3><div class="gr">{hint}{gift}{lv}</div><a class="top" href="#top">▲ 맨 위로</a></section>''')
doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>사역마 대사집</title>
<style>
:root{{--bg:#120C1E;--pn:#1E1530;--ln:#3A2C58;--tx:#F2ECFC;--mu:#B8AAD6}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--tx);font:16px/1.65 Pretendard,system-ui,sans-serif;word-break:keep-all}}
header,.rule,nav,section{{max-width:900px;margin:0 auto;padding-left:16px;padding-right:16px}}
header{{padding-top:20px}} h1{{margin:0 0 6px;font-size:22px;color:#FFE9A0}} header p{{margin:4px 0;color:var(--mu);font-size:15px}}
.rule{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;margin-top:10px}}
.rule div{{background:var(--pn);border:1px solid var(--ln);border-radius:10px;padding:10px 12px;font-size:15px}} .rule b{{color:#FFE9A0}}
nav{{display:flex;flex-wrap:wrap;gap:6px;padding-top:14px;padding-bottom:6px}}
nav a{{display:flex;align-items:center;gap:4px;padding:4px 12px 4px 4px;border-radius:20px;border:1px solid var(--c);background:var(--pn);color:var(--tx);text-decoration:none;font-weight:700}}
nav a img{{width:30px;height:30px;image-rendering:pixelated}}
section{{padding-top:24px;padding-bottom:16px;border-top:1px solid var(--ln);margin-top:18px}}
.hd{{display:flex;gap:14px;align-items:center;background:var(--pn);border:1px solid var(--c);border-radius:14px;padding:12px}}
.hd img{{width:96px;height:96px;image-rendering:pixelated;flex:none}}
h2{{margin:0;color:var(--c);font-size:24px}} h2 small{{font-size:14px;color:var(--mu);font-weight:400}} .mood{{margin:2px 0 6px;font-weight:700}} .hd p{{margin:2px 0;font-size:15px}} .hd b{{color:var(--mu);margin-right:6px}}
h3{{font-size:18px;margin:22px 0 10px;color:#FFE9A0}}
.gr{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px}}
.bk{{background:var(--pn);border:1px solid var(--ln);border-radius:12px;padding:10px 12px}}
.bk h4{{margin:0 0 6px;font-size:15px;color:var(--c)}}
.bk p{{display:flex;gap:10px;margin:0;padding:6px 0;border-top:1px solid #2C2244}} .bk p:first-of-type{{border-top:0}}
.it{{width:96px!important;color:var(--c)!important}} .st{{flex:none;width:72px;font-size:13px;color:var(--mu);padding-top:2px}} .tx{{flex:1}}
mark{{background:none;color:var(--c);font-weight:700}} .top{{display:block;margin-top:14px;color:var(--mu);font-size:14px;text-decoration:none}}
</style></head><body>
<header id="top"><h1>사역마 대사집 · 정령불 12종</h1><p>정령이 혼자 말을 걸어요(플레이어는 대답하지 않아요). 친밀도가 오를수록 말투가 풀리지만 성격은 그대로예요. 모두 {TOTAL}줄.</p></header>
<div class="rule"><div><b>친밀도</b><br>100점마다 한 단계: 경계 → 관심 → 익숙 → 신뢰 → 맹약 (400)</div><div><b>하루 최대 30점</b><br>좋아하는 것 +10 · 보통 +3 · 싫어하는 것 −5</div><div><b>대화</b><br>상황·단계에 맞는 줄 중 무작위로 혼자 말을 걸어요. 읽고 넘기면 돼요</div><div><b>좋아하는 것</b><br>화면에 표시하지 않아요. 평소 대사에 아주 은근하게 섞여 나와요</div></div>
<nav>{''.join(tabs)}</nav>{''.join(secs)}
</body></html>'''
open(os.path.join(HERE, 'lines.html'), 'w').write(doc); print('ok')
