# 장소 목록(public/data/npc/places.json) 만들기 + 서 있을 칸이 비었는지 확인
#   stand: NPC가 실제로 서 있고 돌아다닐 수 있는 곳 (루틴·하트 이벤트 시작 장소)
#   bg: 이벤트 장면 배경으로 잘라 올 지도와 칸, tint: 배경 색조
import json, math, sys
s = open('public/world.js').read(); i = s.index('const MAPS = ') + 13
D, _ = json.JSONDecoder().raw_decode(s[i:])
def blocked(k):
    m = D[k]['meta']; b = set(tuple(w[:2]) for w in (m.get('water') or []))
    for o in m['objs']:
        if o.get('solid', True) is not False:
            x0, y0, x1, y1 = o['box']
            for x in range(math.floor(x0), math.ceil(x1)):
                for y in range(math.floor(y0), math.ceil(y1)): b.add((x, y))
    return m, b
P = [
 # id, 이름, 지도, x, y, 돌아다니는 반경, stand, 배경 칸(없으면 x,y), 색조
 ('lantern_market', '등불 시장', 'campus', 56, 28, 3, 1, None, None),
 ('fish_stall', '생선 가게', 'campus', 49, 37, 2, 1, (49, 34), None),
 ('market_alley', '시장 뒷골목', 'campus', 53, 21, 1, 1, None, 'dim'),
 ('market_roof', '시장 지붕', 'campus', 70, 16, 2, 1, (71, 20), None),
 ('owl_post', '부엉이 우체국', 'campus', 71, 37, 2, 1, (71, 34), None),
 ('village_square', '마을 광장', 'campus', 61, 32, 3, 1, (61, 29), None),
 ('ghost_lake_pier', '유령 호수 잔교', 'campus', 57, 56, 1, 1, None, None),
 ('lakeside', '호숫가', 'campus', 48, 57, 2, 1, (51, 57), None),
 ('main_hall', '본관', 'campus', 19, 27, 3, 1, (19, 22), None),
 ('potion_class', '물약 교실', 'lab', 15, 11, 3, 1, None, None),
 ('infirmary', '양호실', 'lab', 7, 9, 2, 1, None, 'warm'),
 ('library_stacks', '도서관 서고', 'lab', 21, 6, 1, 1, None, 'dim'),
 ('aula_study', '아울라 연구실', 'lab', 5, 15, 1, 1, None, 'warm'),
 ('poison_greenhouse', '독초 온실', 'toxic', 12, 10, 3, 1, None, None),
 ('pumpkin_field', '호박밭', 'campus', 9, 60, 1, 1, None, None),
 ('old_windmill', '낡은 풍차', 'campus', 22, 65, 2, 1, None, 'dim'),
 ('candy_class', '과자 교실', 'candy', 12, 9, 3, 1, None, None),
 ('craft_class', '공예 교실', 'craft', 12, 9, 3, 1, None, None),
 ('witch_hut', '마녀의 오두막', 'campus', 73, 51, 2, 1, (73, 47), None),
 ('hill_ruin', '언덕 위 무너진 오두막', 'campus', 7, 7, 2, 1, None, 'dim'),
 ('menagerie', '사육장', 'barn', 16, 20, 3, 1, None, None),
 ('pen', '방목장', 'pen', 14, 12, 3, 1, None, None),
 ('swamp', '늪지', 'campus', 53, 64, 2, 1, (54, 60), 'green'),
 ('cemetery', '묘지', 'campus', 48, 52, 2, 1, (51, 45), 'dim'),
 ('vamp_manor', '뱀파이어 저택 앞', 'campus', 67, 14, 2, 1, (64, 8), None),
 ('ghost_tea', '유령 찻집', 'campus', 78, 37, 2, 1, (78, 33), None),
 ('bakery', '호박 빵집', 'campus', 78, 27, 2, 1, (78, 23), None),
 ('candy_shop', '사탕 가게', 'campus', 49, 27, 2, 1, (49, 23), None),
 ('dorm_street', '기숙사 거리', 'campus', 21, 51, 3, 1, (18, 46), None),
 ('station', '마차 정류장', 'campus', 6, 27, 2, 1, None, None),
 ('wolf_cabin', '늑대인간 통나무집 앞', 'campus', 78, 61, 2, 1, (79, 57), None),
 ('player_room', '내 방', 'myroom', 8, 9, 2, 1, None, 'warm'),
 # 장면 이동(move·follow)으로만 가는 곳 (지도에 따로 서 있지 않아요)
 ('optician', '시장 안경점', 'campus', 49, 23, 0, 0, None, 'warm'),
 ('flower_shop', '광장 꽃집', 'campus', 71, 23, 0, 0, None, 'warm'),
 ('owl_post_inside', '우체국 안', 'campus', 71, 32, 0, 0, None, 'indoor'),
 ('owl_post_back', '우체국 뒤편', 'campus', 71, 29, 0, 0, None, 'dim'),
 ('clock_tower', '시계탑', 'campus', 20, 16, 0, 0, None, 'sky'),
 ('hall_corridor', '본관 복도', 'lab', 13, 5, 0, 0, None, 'indoor'),
 ('empty_classroom', '본관 빈 교실', 'craft', 12, 9, 0, 0, None, 'dim'),
 ('ghost_lake_cave', '유령 호수 동굴', 'campus', 55, 60, 0, 0, None, 'cave'),
 ('lake_hut', '호숫가 오두막', 'campus', 46, 58, 0, 0, None, 'warm'),
 ('sera_home', '{sera.name}의 집', 'dorm_witch_3', 7, 6, 0, 0, None, 'warm'),
 ('grandma_house', '할머니 집 마루', 'dorm_wolf_3', 7, 6, 0, 0, None, 'warm'),
 ('greenhouse_back', '온실 뒤뜰', 'toxic', 18, 13, 0, 0, None, 'green'),
 ('barn_burnt', '그을린 헛간', 'barn', 25, 10, 0, 0, None, 'dim'),
 ('hill_top', '별 보는 언덕', 'campus', 9, 5, 0, 0, None, 'sky'),
]
out, bad = [], []
for pid, name, mp, x, y, r, stand, bg, tint in P:
    if stand and mp in D:
        m, b = blocked(mp)
        if (x, y) in b: bad.append(f'{pid} 서는 칸 막힘 {x},{y}')
        free = sum(1 for a in range(x - r, x + r + 1) for c in range(y - r, y + r + 1) if (a, c) not in b and 0 <= a < m['NX'] and 0 <= c < m['NY'])
        if free < max(2, (2 * r + 1) ** 2 // 3): bad.append(f'{pid} 빈칸 적음 {free}')
    o = {'id': pid, 'name': name, 'map': mp, 'x': x, 'y': y, 'r': r, 'stand': bool(stand), 'bg': list(bg or (x, y))}
    if tint: o['tint'] = tint
    out.append(o)
json.dump(out, open('public/data/npc/places.json', 'w'), ensure_ascii=False, indent=1)
print('\n'.join(bad) or 'ok', len(out))
