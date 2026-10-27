#!/usr/bin/env python3
"""별 보는 밤 별자리 5개 데이터를 만들고 검사해요 → public/data/events/stargazing/constellations.json
   검사: 별 12개 · 별끼리 거리 6 이상 · 선이 모든 별을 지남 · order 가 edges 와 같은 선들 · 좌표가 0~100 × 0~60 안"""
import json, math, itertools, os
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'data', 'events', 'stargazing', 'constellations.json')
def S(spec, mags):  # spec: "P1 40 14, P2 51 9 ..." mags: {id: mag}, 기본 1
    out = []
    for p in spec.split(','):
        i, x, y = p.split(); out.append({'id': i, 'x': float(x), 'y': float(y), 'mag': mags.get(i, 1)})
    return out
def E(txt): return [t.strip().split('-') for t in txt.split(',')]
C = []
C.append({'id': 'pumpkin_cart', 'name': '호박 수레자리', 'tag': '첫 회 추천',
  'stars': S('P1 40 14,P2 51 9,P3 62 14,P4 64 26,P5 52 31,P6 40 26,C1 28 38,C2 74 38,W1 36 49,W2 66 49,H1 82 32,H2 92 25', {'P2': 3, 'W1': 3, 'W2': 3, 'P1': 2, 'P3': 2, 'C1': 2, 'C2': 2}),
  'order': E('P1-P2,P2-P3,P3-P4,P4-P5,P5-P6,P6-P1,P6-C1,C1-C2,C1-W1,C2-W2,C2-H1,H1-H2'),
  'outline_art': 'pumpkin_cart_outline.png',
  'buff': {'id': 'buff_harvest', 'name': '풍작의 별빛', 'desc': '채집·수확량 +20%, 작물 성장 속도 +10%', 'effects': [{'stat': 'gather_yield', 'value': .2}, {'stat': 'crop_growth', 'value': .1}], 'icon': 'buff_pumpkin_cart.png'}})
C.append({'id': 'witch_broom', 'name': '마녀 빗자루자리', 'tag': '',
  'stars': S('S1 14 50,S2 25 43,S3 36 36,S4 47 29,S5 56 23,S6 63 18,B1 70 6,B2 79 10,B3 82 20,B4 75 27,T1 8 40,T2 4 30', {'S6': 3, 'B2': 3, 'S1': 2, 'T2': 2}),
  'order': E('T2-T1,T1-S1,S1-S2,S2-S3,S3-S4,S4-S5,S5-S6,S6-B1,S6-B2,S6-B3,S6-B4,B1-B2,B3-B4'),
  'outline_art': 'witch_broom_outline.png',
  'buff': {'id': 'buff_wind', 'name': '밤바람의 별빛', 'desc': '이동 속도 +15%, 기력 소모 -20%', 'effects': [{'stat': 'move_speed', 'value': .15}, {'stat': 'stamina_cost', 'value': -.2}], 'icon': 'buff_witch_broom.png'}})
C.append({'id': 'sleepy_owl', 'name': '졸린 부엉이자리', 'tag': '',
  'stars': S('E1 34 8,E2 66 8,C 50 14,H1 30 22,H2 70 22,L 42 24,R 58 24,K 50 31,BL 34 44,BR 66 44,FL 44 56,FR 56 56', {'L': 3, 'R': 3, 'C': 2, 'K': 2}),
  'order': E('H1-E1,E1-C,C-E2,E2-H2,H2-BR,BR-FR,FR-FL,FL-BL,BL-H1,L-K,K-R,L-R'),
  'outline_art': 'sleepy_owl_outline.png',
  'buff': {'id': 'buff_wisdom', 'name': '지혜의 별빛', 'desc': '제조 성공률 +15%, 획득 경험치 +15%', 'effects': [{'stat': 'craft_success', 'value': .15}, {'stat': 'exp_gain', 'value': .15}], 'icon': 'buff_sleepy_owl.png'}})
C.append({'id': 'bell_cat', 'name': '방울 고양이자리', 'tag': '',
  'stars': S('e1 30 10,e2 44 10,ht 37 15,h1 26 20,h2 48 20,c 37 28,b 37 34,bk 58 30,bl 28 52,br 60 52,t1 72 24,t2 80 12', {'b': 3, 'e1': 2, 'e2': 2, 't2': 2}),
  'order': E('h1-e1,e1-ht,ht-e2,e2-h2,h2-c,c-h1,c-b,h2-bk,bk-br,br-bl,bl-h1,bk-t1,t1-t2'),
  'outline_art': 'bell_cat_outline.png',
  'buff': {'id': 'buff_bell', 'name': '방울 소리의 별빛', 'desc': '낚시 희귀 물고기 확률 +20%, 선물로 오르는 호감도 +10%', 'effects': [{'stat': 'rare_fish', 'value': .2}, {'stat': 'gift_affection', 'value': .1}], 'icon': 'buff_bell_cat.png'}})
jit = [1, -1.5, 1.5, -1, 2, -2, 1, -1.5, 1.5, -1, 1.5, -1.5]   # 손을 잡은 사람들처럼 위아래로 살짝
st = []
for k in range(12):
    a = math.radians(30 * k); st.append({'id': f'F{k+1}', 'x': round(50 + 32 * math.cos(a), 1), 'y': round(30 + 22 * math.sin(a) + jit[k], 1), 'mag': 3 if k == 9 else 2})
C.append({'id': 'twelve_friends', 'name': '열두 친구자리', 'tag': '마지막 회 추천', 'keepNames': True,
  'stars': st, 'order': [[f'F{k+1}', f'F{(k+1) % 12 + 1}'] for k in range(12)],
  'outline_art': 'twelve_friends_outline.png',
  'buff': {'id': 'buff_friends', 'name': '열두 친구의 별빛', 'desc': '다른 플레이어와 같은 장소에 있으면 모든 활동 보상 +10%, 둘이 함께 제조·요리하면 결과물 1개 추가', 'effects': [{'stat': 'party_reward', 'value': .1}, {'stat': 'co_craft_extra', 'value': 1}], 'icon': 'buff_twelve_friends.png'}})
bad = 0
for c in C:
    ids = [s['id'] for s in c['stars']]; P = {s['id']: (s['x'], s['y']) for s in c['stars']}
    chk = []
    if len(ids) != 12 or len(set(ids)) != 12: chk.append('별 12개 아님')
    for a, b in itertools.combinations(ids, 2):
        d = math.dist(P[a], P[b])
        if d < 6: chk.append(f'{a}-{b} 거리 {d:.1f}')
    for i, (x, y) in P.items():
        if not (0 <= x <= 100 and 0 <= y <= 60): chk.append(f'{i} 범위 밖')
    used = {i for e in c['order'] for i in e}
    if used != set(ids): chk.append('선에 안 닿은 별 ' + str(set(ids) - used))
    if any(i not in P for e in c['order'] for i in e): chk.append('없는 별 이름')
    c['edges'] = [list(e) for e in c['order']]
    print(c['name'], '별', len(ids), '선', len(c['order']), '문제:', chk or '없음'); bad += len(chk)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({'constellations': C}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
raise SystemExit(1 if bad else 0)
