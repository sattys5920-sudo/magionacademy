# 걸어 다니는 학교 그림 만들기 (호박달 마녀학교 · 몬스터 마을)

Python 3 + Pillow. `halloween.py`·`school.py`는 `world.py`의 그리기 도구를 빌려 써요.

```
python3 halloween.py   # 학교 + 몬스터 마을(84×72, 늘 밤): out/hw_bg.png, out/hw_obj.png, out/hw.json
python3 quarter.py     # 그림자 골목(72×42): 시장 거리 동쪽 끝 문으로 이어지는 의뢰인 마을 (뱀파이어 저택·박물관·번개 탑·마녀 오두막·늑대 통나무집·일곱 등불 광장): out/quarter_bg.png, out/quarter_obj.png, out/quarter.json
                          # halloween.py의 문 기둥(80,25)·(80,29)과 짝이에요. 문의 walk:true = 기둥 사이를 걸으면 바로 넘어가요
python3 interiors.py      # 물약·과자·공예 교실, 독초 온실, 사육장(우리 12칸)·내 우리 + 아래 두 개도 함께: out/*_bg.png·_obj.png·.json
python3 -c "import dorms; dorms.main()"   # 기숙사 휴게실 4곳 × 6단계(dorm_{witch,vamp,wolf,ghost}_{1..6}) + 개인 방(myroom_*) · 기숙사마다 분위기가 달라요
python3 furniture.py      # 개인 방 가구 50종: out/furn.png + furn.json (게임에서 놓는 가구)
python3 ../creatures.py   # 생물 10종 + 알 + 이벤트 용 그림 (양·도마뱀·용은 tools/creature_base.png에서): public/art/iso/creatures_w.png, public/art/creatures.png, 재료 아이콘을 icons.png에 덧붙임
python3 avatar_gen/assemble.py   # 캐릭터 부품: 이미지 생성기로 뽑은 시트(머리 40·눈 15·입 10·교복 5, 앞·뒤·옆)를 조립 → out/avatar_parts.png + .json
                          # (avatar_gen/extract.py가 원본 시트에서 cells.npz를 뽑아요. 원본 시트는 저장소에 없어요)
python3 chars6.py         # (예전) 직접 그린 2등신 캐릭터 부품 (앞·뒤·옆 9프레임): out/avatar_parts.png + .json (머리 40·눈 15·입 10·교복 5)
python3 prev6.py hair     # 미리보기 (hair / face / rand)
(chars3.py: 예전 고정 학생 8명, 이제 안 써요)
python3 build_halloween.py ../../public/world.js   # 지도 + world_tpl.js → public/world.js (index.html이 불러요)
```
만든 png는 `public/art/iso/`에 복사해요.

이전 시안: 별빛고등학교(`school.py`, `sci.py`, `chars2.py`, `school_tpl.html`, `build_school.py`), 마법학교(`world.py`, `campus.py`, `chars.py`, `world2_tpl.html`, `build_walk.py`)
