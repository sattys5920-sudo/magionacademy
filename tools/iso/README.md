# 걸어 다니는 학교 그림 만들기 (호박달 마녀학교 · 몬스터 마을)

Python 3 + Pillow. `halloween.py`·`school.py`는 `world.py`의 그리기 도구를 빌려 써요.

```
python3 halloween.py   # 학교 + 몬스터 마을(84×72, 늘 밤): out/hw_bg.png, out/hw_obj.png, out/hw.json
python3 interiors.py      # 물약·과자·공예 교실, 기숙사 4개, 독초 온실 (크게): out/{pclass,candy,craft,dorm_*,toxic}_bg.png·_obj.png·.json
(캐릭터 부품: avatar_gen/README.md — 생성 이미지에서 뽑아요)
(chars3.py: 예전 고정 학생 8명, 이제 안 써요)
python3 build_halloween.py ../../public/world.js   # 지도 + world_tpl.js → public/world.js (index.html이 불러요)
```
만든 png는 `public/art/iso/`에 복사해요.

이전 시안: 별빛고등학교(`school.py`, `sci.py`, `chars2.py`, `school_tpl.html`, `build_school.py`), 마법학교(`world.py`, `campus.py`, `chars.py`, `world2_tpl.html`, `build_walk.py`)
