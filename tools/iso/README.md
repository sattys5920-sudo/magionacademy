# 걸어 다니는 학교 그림 만들기 (호박달 마녀학교 · 몬스터 마을)

Python 3 + Pillow. `halloween.py`·`school.py`는 `world.py`의 그리기 도구를 빌려 써요.

```
python3 halloween.py   # 학교 + 몬스터 마을(84×72, 늘 밤): out/hw_bg.png, out/hw_obj.png, out/hw.json
python3 room.py        # 물약 교실(실내): out/lab_bg.png, out/lab_obj.png, out/lab.json
python3 chars2.py && python3 chars3.py   # 몬스터 학생: out/students3.png (→ public/art/iso/students.png)
python3 build_halloween.py ../../public/walk.html
```
만든 png는 `public/art/iso/`에 복사해요.

이전 시안: 별빛고등학교(`school.py`, `sci.py`, `chars2.py`, `school_tpl.html`, `build_school.py`), 마법학교(`world.py`, `campus.py`, `chars.py`, `world2_tpl.html`, `build_walk.py`)
